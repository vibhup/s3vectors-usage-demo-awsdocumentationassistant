#!/usr/bin/env python3
"""
Example script for generating embeddings from chunked AWS documentation
using Amazon Titan Text Embeddings V2

This script demonstrates how to:
1. Load chunked documents
2. Generate embeddings using Amazon Bedrock
3. Store embeddings with metadata for vector search

Prerequisites:
- AWS credentials configured (aws configure)
- Amazon Bedrock access to Titan Text Embeddings V2
- boto3 installed (pip install boto3)
"""

import json
import boto3
import os
from pathlib import Path
from typing import List, Dict, Any
import time

class EmbeddingGenerator:
    """Generate embeddings for chunked AWS documentation"""
    
    def __init__(self, region_name: str = "us-west-2"):
        """Initialize the embedding generator with AWS Bedrock client"""
        self.bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=region_name
        )
        self.model_id = "amazon.titan-embed-text-v2:0"
        
    def generate_embedding(self, text: str, dimensions: int = 1024) -> Dict[str, Any]:
        """
        Generate embedding for a single text using Titan Text Embeddings V2
        
        Args:
            text: Input text to embed
            dimensions: Output dimensions (256, 512, or 1024)
            
        Returns:
            Dictionary containing embedding and metadata
        """
        try:
            # Prepare request body
            body = json.dumps({
                "inputText": text,
                "dimensions": dimensions,
                "normalize": True,
                "embeddingTypes": ["float"]
            })
            
            # Call Bedrock API
            response = self.bedrock_runtime.invoke_model(
                body=body,
                modelId=self.model_id,
                accept="application/json",
                contentType="application/json"
            )
            
            # Parse response
            response_body = json.loads(response.get('body').read())
            
            return {
                'embedding': response_body['embedding'],
                'input_token_count': response_body['inputTextTokenCount'],
                'embedding_dimensions': len(response_body['embedding']),
                'model_id': self.model_id,
                'success': True
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }
    
    def process_chunk_file(self, chunk_file_path: str, dimensions: int = 1024) -> Dict[str, Any]:
        """
        Process a single chunk file and generate embedding
        
        Args:
            chunk_file_path: Path to the chunk JSON file
            dimensions: Output dimensions for embedding
            
        Returns:
            Dictionary with chunk data and embedding
        """
        try:
            # Load chunk data
            with open(chunk_file_path, 'r', encoding='utf-8') as f:
                chunk_data = json.load(f)
            
            # Generate embedding for the chunk content
            embedding_result = self.generate_embedding(
                chunk_data['content'], 
                dimensions=dimensions
            )
            
            if embedding_result['success']:
                # Combine chunk data with embedding
                result = {
                    'chunk_id': chunk_data['chunk_id'],
                    'source_file': chunk_data['source_file'],
                    'title': chunk_data['title'],
                    'section': chunk_data['section'],
                    'content': chunk_data['content'],
                    'token_count': chunk_data['token_count'],
                    'char_count': chunk_data['char_count'],
                    'metadata': chunk_data['metadata'],
                    'embedding': embedding_result['embedding'],
                    'embedding_dimensions': embedding_result['embedding_dimensions'],
                    'embedding_token_count': embedding_result['input_token_count'],
                    'model_id': embedding_result['model_id'],
                    'processing_success': True
                }
            else:
                result = {
                    'chunk_id': chunk_data.get('chunk_id', 'unknown'),
                    'error': embedding_result['error'],
                    'processing_success': False
                }
            
            return result
            
        except Exception as e:
            return {
                'chunk_file': chunk_file_path,
                'error': str(e),
                'processing_success': False
            }
    
    def process_chunks_directory(self, 
                                chunks_dir: str, 
                                output_dir: str,
                                dimensions: int = 1024,
                                max_chunks: int = None) -> Dict[str, Any]:
        """
        Process all chunk files in a directory and generate embeddings
        
        Args:
            chunks_dir: Directory containing chunk JSON files
            output_dir: Directory to save embeddings
            dimensions: Output dimensions for embeddings
            max_chunks: Maximum number of chunks to process (for testing)
            
        Returns:
            Processing statistics
        """
        chunks_path = Path(chunks_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find all chunk files (exclude summary files)
        chunk_files = [f for f in chunks_path.glob("*.json") if "_chunks.json" not in f.name and "processing_stats.json" not in f.name]
        
        if max_chunks:
            chunk_files = chunk_files[:max_chunks]
        
        print(f"Found {len(chunk_files)} chunk files to process")
        
        # Statistics tracking
        stats = {
            'total_chunks': len(chunk_files),
            'successful_embeddings': 0,
            'failed_embeddings': 0,
            'total_tokens_processed': 0,
            'total_embedding_dimensions': dimensions,
            'processing_errors': []
        }
        
        # Process each chunk
        for i, chunk_file in enumerate(chunk_files, 1):
            print(f"Processing chunk {i}/{len(chunk_files)}: {chunk_file.name}")
            
            try:
                # Generate embedding for chunk
                result = self.process_chunk_file(str(chunk_file), dimensions)
                
                if result['processing_success']:
                    # Save embedding with metadata
                    embedding_filename = f"{result['chunk_id']}_embedding.json"
                    embedding_path = output_path / embedding_filename
                    
                    with open(embedding_path, 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
                    
                    stats['successful_embeddings'] += 1
                    stats['total_tokens_processed'] += result['embedding_token_count']
                    
                    print(f"  ✓ Generated {result['embedding_dimensions']}D embedding ({result['embedding_token_count']} tokens)")
                else:
                    stats['failed_embeddings'] += 1
                    stats['processing_errors'].append({
                        'chunk_file': chunk_file.name,
                        'error': result.get('error', 'Unknown error')
                    })
                    print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")
                
                # Add small delay to avoid rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                stats['failed_embeddings'] += 1
                error_msg = f"Error processing {chunk_file.name}: {str(e)}"
                stats['processing_errors'].append({
                    'chunk_file': chunk_file.name,
                    'error': str(e)
                })
                print(f"  ✗ Error: {error_msg}")
        
        # Save processing statistics
        stats_path = output_path / 'embedding_stats.json'
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        return stats

def main():
    """Main function to generate embeddings for all chunks"""
    
    # Configuration
    chunks_directory = "/Users/vibhup/Downloads/embeddingdataset/AWSDataset-chunked"
    embeddings_directory = "/Users/vibhup/Downloads/embeddingdataset/AWSDataset-embeddings"
    
    print("AWS Documentation Embedding Generation")
    print("=" * 60)
    print(f"Input directory: {chunks_directory}")
    print(f"Output directory: {embeddings_directory}")
    print()
    
    # Initialize embedding generator
    try:
        generator = EmbeddingGenerator(region_name="us-west-2")
        print("✓ Initialized Amazon Bedrock client")
    except Exception as e:
        print(f"✗ Failed to initialize Bedrock client: {e}")
        print("Please ensure AWS credentials are configured and you have access to Amazon Bedrock")
        return 1
    
    # Process ALL chunks
    print("\nProcessing all chunks to generate embeddings...")
    
    try:
        stats = generator.process_chunks_directory(
            chunks_dir=chunks_directory,
            output_dir=embeddings_directory,
            dimensions=1024,  # Use 1024 dimensions for good balance of quality and cost
            max_chunks=None   # Process ALL chunks
        )
        
        # Print results
        print("\nProcessing Complete!")
        print("=" * 60)
        print(f"Total chunks processed: {stats['total_chunks']}")
        print(f"Successful embeddings: {stats['successful_embeddings']}")
        print(f"Failed embeddings: {stats['failed_embeddings']}")
        print(f"Total tokens processed: {stats['total_tokens_processed']:,}")
        print(f"Embedding dimensions: {stats['total_embedding_dimensions']}")
        
        if stats['processing_errors']:
            print(f"\nErrors encountered: {len(stats['processing_errors'])}")
            for error in stats['processing_errors'][:5]:  # Show first 5 errors
                print(f"  - {error['chunk_file']}: {error['error']}")
        
        print(f"\nEmbeddings saved to: {embeddings_directory}")
        print("Ready for vector search applications!")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
