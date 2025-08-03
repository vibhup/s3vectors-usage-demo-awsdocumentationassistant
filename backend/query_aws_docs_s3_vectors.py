#!/usr/bin/env python3
"""
AWS Documentation S3 Vectors Query Script

This script provides semantic search capabilities over your AWS documentation
embeddings stored in S3 Vectors using Amazon Titan Text Embeddings V2.

Features:
- Natural language queries
- Metadata filtering by AWS service
- Similarity scoring
- Rich result formatting
- Interactive query mode

Usage:
    python query_aws_docs_s3_vectors.py
    python query_aws_docs_s3_vectors.py --query "How do I scale Lambda functions?"
"""

import json
import boto3
import argparse
import numpy as np
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSDocsVectorSearch:
    def __init__(self, vector_bucket_name: str, index_name: str, region_name: str = "us-east-1"):
        """Initialize the AWS Documentation Vector Search."""
        self.vector_bucket_name = vector_bucket_name
        self.index_name = index_name
        self.region_name = region_name
        
        # Initialize clients
        self.s3vectors_client = boto3.client('s3vectors', region_name=region_name)
        self.bedrock_client = boto3.client('bedrock-runtime', region_name="us-west-2")  # Titan model region
        
        logger.info(f"Initialized AWS Docs Vector Search for bucket: {vector_bucket_name}, index: {index_name}")

    def generate_query_embedding(self, query_text: str) -> List[float]:
        """Generate embedding for query text using Titan Text Embeddings V2."""
        try:
            # Prepare request body
            body = json.dumps({
                "inputText": query_text,
                "dimensions": 1024,
                "normalize": True,
                "embeddingTypes": ["float"]
            })
            
            # Call Bedrock
            response = self.bedrock_client.invoke_model(
                body=body,
                modelId="amazon.titan-embed-text-v2:0",
                accept="application/json",
                contentType="application/json"
            )
            
            # Parse response
            response_body = json.loads(response["body"].read())
            embedding = response_body["embedding"]
            
            logger.info(f"Generated embedding for query: '{query_text[:50]}...'")
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating query embedding: {str(e)}")
            return None

    def search_vectors(self, query_text: str, top_k: int = 5, service_filter: str = None) -> List[Dict[str, Any]]:
        """Search for similar vectors in the S3 Vectors index."""
        try:
            # Generate query embedding
            query_embedding = self.generate_query_embedding(query_text)
            if not query_embedding:
                return []
            
            # Prepare query parameters
            query_params = {
                'vectorBucketName': self.vector_bucket_name,
                'indexName': self.index_name,
                'queryVector': {'float32': query_embedding},
                'topK': top_k,
                'returnDistance': True,
                'returnMetadata': True
            }
            
            # Add service filter if specified
            if service_filter:
                query_params['filter'] = {'service_name': service_filter}
            
            # Execute query
            response = self.s3vectors_client.query_vectors(**query_params)
            
            logger.info(f"Found {len(response.get('vectors', []))} similar documents")
            return response.get('vectors', [])
            
        except Exception as e:
            logger.error(f"Error searching vectors: {str(e)}")
            return []

    def format_search_results(self, results: List[Dict[str, Any]], query: str) -> str:
        """Format search results for display."""
        if not results:
            return "❌ No results found for your query."
        
        output = []
        output.append("🔍 AWS DOCUMENTATION SEARCH RESULTS")
        output.append("=" * 60)
        output.append(f"📝 Query: \"{query}\"")
        output.append(f"📊 Found: {len(results)} relevant documents")
        output.append("")
        
        for i, result in enumerate(results, 1):
            metadata = result.get('metadata', {})
            distance = result.get('distance', 0)
            similarity = (1 - distance) * 100  # Convert distance to similarity percentage
            
            output.append(f"🏆 Result #{i} (Similarity: {similarity:.1f}%)")
            output.append("-" * 40)
            output.append(f"🔧 Service: {metadata.get('service_name', 'Unknown')}")
            output.append(f"📄 Source: {metadata.get('source_file', 'Unknown')}")
            output.append(f"📝 Type: {metadata.get('document_type', 'Documentation')}")
            output.append(f"🔢 Tokens: {metadata.get('token_count', 0)}")
            
            # Show content preview
            content_preview = metadata.get('content_preview', '')
            if content_preview:
                output.append(f"📖 Preview: {content_preview}...")
            
            output.append("")
        
        return "\n".join(output)

    def interactive_search(self):
        """Interactive search mode."""
        print("🚀 AWS Documentation Interactive Search")
        print("💡 Ask questions about AWS services in natural language!")
        print("📝 Examples:")
        print("   - 'How do I scale Lambda functions?'")
        print("   - 'S3 bucket security best practices'")
        print("   - 'DynamoDB performance optimization'")
        print("   - 'VPC networking configuration'")
        print("\n💡 Type 'quit' to exit, 'help' for commands")
        print("-" * 60)
        
        while True:
            try:
                # Get user input
                query = input("\n🔍 Enter your AWS question: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if query.lower() == 'help':
                    self.show_help()
                    continue
                
                if not query:
                    continue
                
                # Check for service filter
                service_filter = None
                if query.startswith('@'):
                    parts = query.split(' ', 1)
                    if len(parts) == 2:
                        service_filter = parts[0][1:]  # Remove @
                        query = parts[1]
                        print(f"🎯 Filtering by service: {service_filter}")
                
                # Perform search
                print("⏳ Searching AWS documentation...")
                results = self.search_vectors(query, top_k=5, service_filter=service_filter)
                
                # Display results
                formatted_results = self.format_search_results(results, query)
                print(formatted_results)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")

    def show_help(self):
        """Show help information."""
        help_text = """
🆘 AWS Documentation Search Help

📝 Query Examples:
   • "How do I scale Lambda functions?"
   • "S3 bucket security best practices"
   • "DynamoDB performance optimization"
   • "VPC networking configuration"

🎯 Service Filtering:
   • Use @service_name to filter by specific AWS service
   • Example: "@lambda How to set memory limits?"
   • Example: "@s3 How to enable versioning?"

🔧 Available Services:
   • lambda, s3, ec2, rds, dynamodb, vpc, iam
   • cloudformation, cloudwatch, sns, sqs, kinesis
   • ecs, eks, api-gateway, route53

⌨️  Commands:
   • 'help' - Show this help
   • 'quit' or 'q' - Exit the program
        """
        print(help_text)

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Search AWS Documentation using S3 Vectors")
    parser.add_argument("--query", "-q", help="Search query")
    parser.add_argument("--service", "-s", help="Filter by AWS service")
    parser.add_argument("--top-k", "-k", type=int, default=5, help="Number of results to return")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    # Configuration
    VECTOR_BUCKET_NAME = "vibhup-aws-docs-vectors"
    INDEX_NAME = "aws-documentation"
    
    # Initialize search
    search = AWSDocsVectorSearch(
        vector_bucket_name=VECTOR_BUCKET_NAME,
        index_name=INDEX_NAME,
        region_name="us-east-1"
    )
    
    if args.query:
        # Single query mode
        print(f"🔍 Searching for: '{args.query}'")
        if args.service:
            print(f"🎯 Filtering by service: {args.service}")
        
        results = search.search_vectors(args.query, top_k=args.top_k, service_filter=args.service)
        formatted_results = search.format_search_results(results, args.query)
        print(formatted_results)
        
    else:
        # Interactive mode
        search.interactive_search()

if __name__ == "__main__":
    main()
