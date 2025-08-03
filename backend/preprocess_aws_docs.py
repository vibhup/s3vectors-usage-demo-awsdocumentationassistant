#!/usr/bin/env python3
"""
AWS Documentation Preprocessing Script

This script processes AWS documentation files and chunks them into smaller segments
optimized for Amazon Titan Text Embeddings. It creates logical chunks based on
markdown structure while preserving context and metadata.

Features:
- Chunks documents by headers and sections
- Maintains context with overlapping content
- Preserves metadata for each chunk
- Optimizes chunk size for Titan Text Embeddings (up to 8192 tokens)
- Creates JSON output with structured metadata
"""

import os
import re
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, asdict
import tiktoken

@dataclass
class DocumentChunk:
    """Represents a chunk of a document with metadata"""
    chunk_id: str
    source_file: str
    title: str
    section: str
    content: str
    token_count: int
    char_count: int
    chunk_index: int
    total_chunks: int
    overlap_with_previous: bool
    metadata: Dict[str, Any]

class AWSDocumentChunker:
    """Chunks AWS documentation for optimal embedding generation"""
    
    def __init__(self, 
                 max_tokens: int = 6000,  # Conservative limit for 8192 token max
                 overlap_tokens: int = 200,
                 min_chunk_tokens: int = 100):
        """
        Initialize the chunker with configuration parameters
        
        Args:
            max_tokens: Maximum tokens per chunk (conservative for 8192 limit)
            overlap_tokens: Number of tokens to overlap between chunks
            min_chunk_tokens: Minimum tokens required for a chunk
        """
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.min_chunk_tokens = min_chunk_tokens
        
        # Initialize tokenizer for accurate token counting
        try:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")  # GPT-4 tokenizer
        except Exception:
            print("Warning: tiktoken not available, using character-based estimation")
            self.tokenizer = None
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken or estimation"""
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        else:
            # Fallback: estimate 4.7 characters per token (AWS documentation states this for English)
            return int(len(text) / 4.7)
    
    def extract_title_from_content(self, content: str) -> str:
        """Extract the main title from markdown content"""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# ') and not line.startswith('## '):
                return line[2:].strip()
        return "Untitled Document"
    
    def split_by_headers(self, content: str) -> List[Tuple[str, str, int]]:
        """
        Split content by markdown headers, returning (section_title, content, header_level)
        """
        sections = []
        lines = content.split('\n')
        current_section = []
        current_title = ""
        current_level = 0
        
        for line in lines:
            # Check if line is a header
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
            
            if header_match:
                # Save previous section if it exists
                if current_section and current_title:
                    section_content = '\n'.join(current_section).strip()
                    if section_content:
                        sections.append((current_title, section_content, current_level))
                
                # Start new section
                header_level = len(header_match.group(1))
                current_title = header_match.group(2).strip()
                current_level = header_level
                current_section = [line]  # Include the header in the section
            else:
                current_section.append(line)
        
        # Add the last section
        if current_section and current_title:
            section_content = '\n'.join(current_section).strip()
            if section_content:
                sections.append((current_title, section_content, current_level))
        
        return sections
    
    def chunk_large_section(self, title: str, content: str) -> List[Tuple[str, str]]:
        """
        Chunk a large section that exceeds token limits
        Returns list of (chunk_title, chunk_content) tuples
        """
        chunks = []
        
        # Split by paragraphs first
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        current_chunk = []
        current_tokens = 0
        chunk_index = 1
        
        for paragraph in paragraphs:
            paragraph_tokens = self.count_tokens(paragraph)
            
            # If single paragraph exceeds limit, split by sentences
            if paragraph_tokens > self.max_tokens:
                # Save current chunk if it has content
                if current_chunk:
                    chunk_content = '\n\n'.join(current_chunk)
                    chunk_title = f"{title} (Part {chunk_index})"
                    chunks.append((chunk_title, chunk_content))
                    chunk_index += 1
                    current_chunk = []
                    current_tokens = 0
                
                # Split large paragraph by sentences
                sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                sentence_chunk = []
                sentence_tokens = 0
                
                for sentence in sentences:
                    sentence_token_count = self.count_tokens(sentence)
                    
                    if sentence_tokens + sentence_token_count > self.max_tokens and sentence_chunk:
                        # Save sentence chunk
                        chunk_content = ' '.join(sentence_chunk)
                        chunk_title = f"{title} (Part {chunk_index})"
                        chunks.append((chunk_title, chunk_content))
                        chunk_index += 1
                        sentence_chunk = [sentence]
                        sentence_tokens = sentence_token_count
                    else:
                        sentence_chunk.append(sentence)
                        sentence_tokens += sentence_token_count
                
                # Add remaining sentences as a chunk
                if sentence_chunk:
                    chunk_content = ' '.join(sentence_chunk)
                    chunk_title = f"{title} (Part {chunk_index})"
                    chunks.append((chunk_title, chunk_content))
                    chunk_index += 1
            
            # Check if adding this paragraph would exceed the limit
            elif current_tokens + paragraph_tokens > self.max_tokens:
                # Save current chunk
                if current_chunk:
                    chunk_content = '\n\n'.join(current_chunk)
                    chunk_title = f"{title} (Part {chunk_index})" if chunk_index > 1 else title
                    chunks.append((chunk_title, chunk_content))
                    chunk_index += 1
                
                # Start new chunk with overlap
                if current_chunk and self.overlap_tokens > 0:
                    # Add last paragraph from previous chunk for context
                    overlap_content = current_chunk[-1]
                    overlap_tokens = self.count_tokens(overlap_content)
                    if overlap_tokens <= self.overlap_tokens:
                        current_chunk = [overlap_content, paragraph]
                        current_tokens = overlap_tokens + paragraph_tokens
                    else:
                        current_chunk = [paragraph]
                        current_tokens = paragraph_tokens
                else:
                    current_chunk = [paragraph]
                    current_tokens = paragraph_tokens
            else:
                current_chunk.append(paragraph)
                current_tokens += paragraph_tokens
        
        # Add final chunk
        if current_chunk:
            chunk_content = '\n\n'.join(current_chunk)
            chunk_title = f"{title} (Part {chunk_index})" if chunk_index > 1 else title
            chunks.append((chunk_title, chunk_content))
        
        return chunks
    
    def process_document(self, file_path: str, content: str) -> List[DocumentChunk]:
        """
        Process a single document and return list of chunks
        """
        chunks = []
        file_name = os.path.basename(file_path)
        doc_title = self.extract_title_from_content(content)
        
        # Split document by headers
        sections = self.split_by_headers(content)
        
        if not sections:
            # If no sections found, treat entire document as one section
            sections = [(doc_title, content, 1)]
        
        chunk_id_base = hashlib.md5(file_path.encode()).hexdigest()[:8]
        
        all_section_chunks = []
        
        # Process each section
        for section_title, section_content, header_level in sections:
            section_tokens = self.count_tokens(section_content)
            
            if section_tokens <= self.max_tokens:
                # Section fits in one chunk
                all_section_chunks.append((section_title, section_content, False))
            else:
                # Section needs to be chunked
                section_chunks = self.chunk_large_section(section_title, section_content)
                for i, (chunk_title, chunk_content) in enumerate(section_chunks):
                    has_overlap = i > 0  # First chunk has no overlap
                    all_section_chunks.append((chunk_title, chunk_content, has_overlap))
        
        # Create DocumentChunk objects
        total_chunks = len(all_section_chunks)
        
        for i, (section_title, chunk_content, has_overlap) in enumerate(all_section_chunks):
            # Skip chunks that are too small unless they're the only chunk
            if total_chunks > 1 and self.count_tokens(chunk_content) < self.min_chunk_tokens:
                continue
            
            chunk_id = f"{chunk_id_base}_{i+1:03d}"
            token_count = self.count_tokens(chunk_content)
            char_count = len(chunk_content)
            
            # Extract service name from filename
            service_name = file_name.replace('_intro.md', '').replace('_', ' ').replace('-', ' ').title()
            
            metadata = {
                'service_name': service_name,
                'document_type': 'introduction' if 'intro' in file_name else 'guide',
                'header_level': 1,  # Could be enhanced to track actual header levels
                'file_size_chars': len(content),
                'processing_timestamp': None  # Will be set during processing
            }
            
            chunk = DocumentChunk(
                chunk_id=chunk_id,
                source_file=file_name,
                title=doc_title,
                section=section_title,
                content=chunk_content,
                token_count=token_count,
                char_count=char_count,
                chunk_index=i + 1,
                total_chunks=total_chunks,
                overlap_with_previous=has_overlap,
                metadata=metadata
            )
            
            chunks.append(chunk)
        
        return chunks
    
    def process_directory(self, input_dir: str, output_dir: str) -> Dict[str, Any]:
        """
        Process all markdown files in input directory and save chunks to output directory
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        # Create output directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Statistics tracking
        stats = {
            'total_files': 0,
            'total_chunks': 0,
            'total_tokens': 0,
            'total_chars': 0,
            'files_processed': [],
            'processing_errors': []
        }
        
        # Process each markdown file
        for md_file in input_path.glob('*.md'):
            try:
                print(f"Processing: {md_file.name}")
                
                # Read file content
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Process document into chunks
                chunks = self.process_document(str(md_file), content)
                
                # Save chunks to individual JSON files
                file_chunks = []
                for chunk in chunks:
                    # Add processing timestamp
                    chunk.metadata['processing_timestamp'] = str(pd.Timestamp.now()) if 'pd' in globals() else "2025-08-02"
                    
                    # Save individual chunk file
                    chunk_filename = f"{chunk.chunk_id}.json"
                    chunk_path = output_path / chunk_filename
                    
                    with open(chunk_path, 'w', encoding='utf-8') as f:
                        json.dump(asdict(chunk), f, indent=2, ensure_ascii=False)
                    
                    file_chunks.append(asdict(chunk))
                    
                    # Update statistics
                    stats['total_tokens'] += chunk.token_count
                    stats['total_chars'] += chunk.char_count
                
                # Save file summary
                file_summary = {
                    'source_file': md_file.name,
                    'total_chunks': len(chunks),
                    'chunks': file_chunks
                }
                
                summary_filename = f"{md_file.stem}_chunks.json"
                summary_path = output_path / summary_filename
                
                with open(summary_path, 'w', encoding='utf-8') as f:
                    json.dump(file_summary, f, indent=2, ensure_ascii=False)
                
                # Update statistics
                stats['total_files'] += 1
                stats['total_chunks'] += len(chunks)
                stats['files_processed'].append({
                    'filename': md_file.name,
                    'chunks_created': len(chunks),
                    'total_tokens': sum(chunk.token_count for chunk in chunks)
                })
                
                print(f"  Created {len(chunks)} chunks")
                
            except Exception as e:
                error_msg = f"Error processing {md_file.name}: {str(e)}"
                print(f"  ERROR: {error_msg}")
                stats['processing_errors'].append(error_msg)
        
        # Save overall statistics
        stats_path = output_path / 'processing_stats.json'
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        return stats

def main():
    """Main function to run the preprocessing"""
    
    # Configuration
    input_directory = "/Users/vibhup/Downloads/embeddingdataset/AWSdataset"
    output_directory = "/Users/vibhup/Downloads/embeddingdataset/AWSDataset-chunked"
    
    print("AWS Documentation Preprocessing Script")
    print("=" * 50)
    print(f"Input directory: {input_directory}")
    print(f"Output directory: {output_directory}")
    print()
    
    # Initialize chunker
    chunker = AWSDocumentChunker(
        max_tokens=6000,      # Conservative limit for Titan's 8192 token max
        overlap_tokens=200,   # Overlap for context preservation
        min_chunk_tokens=100  # Minimum viable chunk size
    )
    
    # Process documents
    try:
        stats = chunker.process_directory(input_directory, output_directory)
        
        # Print summary
        print("\nProcessing Complete!")
        print("=" * 50)
        print(f"Files processed: {stats['total_files']}")
        print(f"Total chunks created: {stats['total_chunks']}")
        print(f"Total tokens: {stats['total_tokens']:,}")
        print(f"Total characters: {stats['total_chars']:,}")
        print(f"Average tokens per chunk: {stats['total_tokens'] // stats['total_chunks'] if stats['total_chunks'] > 0 else 0}")
        
        if stats['processing_errors']:
            print(f"\nErrors encountered: {len(stats['processing_errors'])}")
            for error in stats['processing_errors']:
                print(f"  - {error}")
        
        print(f"\nChunked files saved to: {output_directory}")
        print("Ready for embedding generation with Amazon Titan Text Embeddings!")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
