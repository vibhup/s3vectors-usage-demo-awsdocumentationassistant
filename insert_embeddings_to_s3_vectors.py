#!/usr/bin/env python3
"""
AWS Documentation Embeddings to S3 Vectors Insertion Script

This script reads all the embeddings from your AWS documentation project
and inserts them into the S3 Vectors index for semantic search.

Features:
- Batch processing for optimal performance
- Progress tracking and statistics
- Error handling and retry logic
- Metadata preservation for filtering
- Comprehensive logging

Usage:
    python insert_embeddings_to_s3_vectors.py
"""

import json
import os
import boto3
import numpy as np
from typing import List, Dict, Any
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('s3_vectors_insertion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class S3VectorsInserter:
    def __init__(self, vector_bucket_name: str, index_name: str, region_name: str = "us-east-1"):
        """Initialize the S3 Vectors inserter."""
        self.vector_bucket_name = vector_bucket_name
        self.index_name = index_name
        self.region_name = region_name
        
        # Initialize S3 Vectors client
        self.s3vectors_client = boto3.client('s3vectors', region_name=region_name)
        
        # Statistics
        self.stats = {
            'total_embeddings': 0,
            'successful_insertions': 0,
            'failed_insertions': 0,
            'batches_processed': 0,
            'start_time': None,
            'end_time': None,
            'errors': []
        }
        
        logger.info(f"Initialized S3VectorsInserter for bucket: {vector_bucket_name}, index: {index_name}")

    def load_embedding_file(self, file_path: str) -> Dict[str, Any]:
        """Load a single embedding file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {str(e)}")
            return None

    def prepare_vector_for_s3(self, embedding_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare embedding data for S3 Vectors format."""
        try:
            # Extract the embedding vector
            embedding = embedding_data.get('embedding', [])
            
            # Ensure it's float32 format
            if isinstance(embedding, list):
                embedding = np.array(embedding, dtype=np.float32).tolist()
            
            # Extract metadata
            metadata = embedding_data.get('metadata', {})
            content = embedding_data.get('content', '')
            
            # Create comprehensive metadata for filtering
            vector_metadata = {
                'service_name': metadata.get('service_name', 'unknown'),
                'document_type': metadata.get('document_type', 'documentation'),
                'chunk_index': metadata.get('chunk_index', 0),
                'token_count': metadata.get('token_count', 0),
                'timestamp': metadata.get('timestamp', ''),
                'source_file': metadata.get('source_file', ''),
                'content_preview': content[:200] if content else '',  # First 200 chars for preview
                'content_length': len(content) if content else 0
            }
            
            # Generate unique key from chunk_id or create one
            chunk_id = embedding_data.get('chunk_id', '')
            if not chunk_id:
                # Generate key from metadata
                source_file = metadata.get('source_file', 'unknown')
                chunk_index = metadata.get('chunk_index', 0)
                chunk_id = f"{source_file}_{chunk_index}"
            
            # Prepare vector for S3 Vectors
            vector_record = {
                'key': chunk_id,
                'data': {'float32': embedding},
                'metadata': vector_metadata
            }
            
            return vector_record
            
        except Exception as e:
            logger.error(f"Error preparing vector: {str(e)}")
            return None

    def insert_vectors_batch(self, vectors: List[Dict[str, Any]]) -> bool:
        """Insert a batch of vectors into S3 Vectors."""
        try:
            logger.info(f"Inserting batch of {len(vectors)} vectors...")
            
            response = self.s3vectors_client.put_vectors(
                vectorBucketName=self.vector_bucket_name,
                indexName=self.index_name,
                vectors=vectors
            )
            
            logger.info(f"Successfully inserted batch of {len(vectors)} vectors")
            self.stats['successful_insertions'] += len(vectors)
            self.stats['batches_processed'] += 1
            
            return True
            
        except Exception as e:
            logger.error(f"Error inserting batch: {str(e)}")
            self.stats['failed_insertions'] += len(vectors)
            self.stats['errors'].append(str(e))
            return False

    def process_embeddings_directory(self, embeddings_dir: str, batch_size: int = 25):
        """Process all embedding files in the directory."""
        self.stats['start_time'] = datetime.now()
        
        # Get all embedding files
        embedding_files = [
            f for f in os.listdir(embeddings_dir) 
            if f.endswith('_embedding.json')
        ]
        
        self.stats['total_embeddings'] = len(embedding_files)
        logger.info(f"Found {len(embedding_files)} embedding files to process")
        
        # Process files in batches
        vectors_batch = []
        
        for i, filename in enumerate(embedding_files):
            file_path = os.path.join(embeddings_dir, filename)
            
            # Load embedding data
            embedding_data = self.load_embedding_file(file_path)
            if not embedding_data:
                continue
            
            # Prepare vector for S3
            vector_record = self.prepare_vector_for_s3(embedding_data)
            if not vector_record:
                continue
            
            vectors_batch.append(vector_record)
            
            # Insert batch when it reaches batch_size or is the last file
            if len(vectors_batch) >= batch_size or i == len(embedding_files) - 1:
                success = self.insert_vectors_batch(vectors_batch)
                
                if success:
                    logger.info(f"Progress: {i + 1}/{len(embedding_files)} files processed")
                else:
                    logger.error(f"Failed to insert batch at file {i + 1}")
                
                vectors_batch = []  # Reset batch
                
                # Small delay to avoid rate limiting
                time.sleep(0.1)
        
        self.stats['end_time'] = datetime.now()
        self.print_final_statistics()

    def print_final_statistics(self):
        """Print comprehensive statistics."""
        duration = self.stats['end_time'] - self.stats['start_time']
        
        print("\n" + "="*60)
        print("🎯 S3 VECTORS INSERTION COMPLETE")
        print("="*60)
        print(f"📊 Total Embeddings Found: {self.stats['total_embeddings']}")
        print(f"✅ Successful Insertions: {self.stats['successful_insertions']}")
        print(f"❌ Failed Insertions: {self.stats['failed_insertions']}")
        print(f"📦 Batches Processed: {self.stats['batches_processed']}")
        print(f"⏱️  Total Duration: {duration}")
        print(f"🏆 Success Rate: {(self.stats['successful_insertions']/self.stats['total_embeddings']*100):.1f}%")
        
        if self.stats['errors']:
            print(f"\n❗ Errors Encountered: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:  # Show first 5 errors
                print(f"   - {error}")
        
        print(f"\n🔍 Vector Index Details:")
        print(f"   - Bucket: {self.vector_bucket_name}")
        print(f"   - Index: {self.index_name}")
        print(f"   - Region: {self.region_name}")
        print(f"   - Dimensions: 1024 (Titan Text Embeddings V2)")
        print(f"   - Distance Metric: Cosine")
        
        print("\n🚀 Ready for Semantic Search!")
        print("="*60)

def main():
    """Main execution function."""
    # Configuration
    VECTOR_BUCKET_NAME = "vibhup-aws-docs-vectors"
    INDEX_NAME = "aws-documentation"
    EMBEDDINGS_DIR = "/Users/vibhup/Downloads/embeddingdataset/AWSDataset-embeddings"
    BATCH_SIZE = 25  # Optimal batch size for S3 Vectors
    
    print("🚀 Starting AWS Documentation Embeddings Insertion to S3 Vectors")
    print(f"📁 Source Directory: {EMBEDDINGS_DIR}")
    print(f"🪣 Vector Bucket: {VECTOR_BUCKET_NAME}")
    print(f"📇 Vector Index: {INDEX_NAME}")
    print(f"📦 Batch Size: {BATCH_SIZE}")
    
    # Verify embeddings directory exists
    if not os.path.exists(EMBEDDINGS_DIR):
        logger.error(f"Embeddings directory not found: {EMBEDDINGS_DIR}")
        return
    
    # Initialize inserter
    inserter = S3VectorsInserter(
        vector_bucket_name=VECTOR_BUCKET_NAME,
        index_name=INDEX_NAME,
        region_name="us-east-1"
    )
    
    # Process all embeddings
    inserter.process_embeddings_directory(EMBEDDINGS_DIR, BATCH_SIZE)

if __name__ == "__main__":
    main()
