#!/usr/bin/env python3
"""
AWS Documentation RAG (Retrieval-Augmented Generation) System

This script creates a complete RAG system that:
1. Takes user questions about AWS services
2. Searches your S3 Vectors index for relevant documentation
3. Uses Claude 3.5 Sonnet to generate comprehensive answers
4. Provides source attribution and follow-up suggestions

Features:
- Natural language question processing
- Semantic search with S3 Vectors
- Claude 3.5 Sonnet for intelligent responses
- Source attribution and confidence scoring
- Interactive chat interface
- Context-aware follow-up questions

Usage:
    python3 aws_docs_rag_system.py
    python3 aws_docs_rag_system.py --question "How do I scale Lambda functions?"
"""

import json
import boto3
import argparse
import logging
from typing import List, Dict, Any, Tuple
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AWSDocsRAGSystem:
    def __init__(self, 
                 vector_bucket_name: str, 
                 index_name: str, 
                 s3vectors_region: str = "us-east-1",
                 bedrock_region: str = "us-east-1"):
        """Initialize the AWS Documentation RAG System."""
        
        self.vector_bucket_name = vector_bucket_name
        self.index_name = index_name
        self.s3vectors_region = s3vectors_region
        self.bedrock_region = bedrock_region
        
        # Initialize AWS clients
        self.s3vectors_client = boto3.client('s3vectors', region_name=s3vectors_region)
        self.bedrock_client = boto3.client('bedrock-runtime', region_name=bedrock_region)
        
        # Model configurations
        self.embedding_model = "amazon.titan-embed-text-v2:0"
        self.llm_model = "anthropic.claude-3-5-sonnet-20240620-v1:0"
        
        logger.info(f"Initialized RAG System:")
        logger.info(f"  - Vector Bucket: {vector_bucket_name}")
        logger.info(f"  - Vector Index: {index_name}")
        logger.info(f"  - S3 Vectors Region: {s3vectors_region}")
        logger.info(f"  - Bedrock Region: {bedrock_region}")
        logger.info(f"  - LLM Model: {self.llm_model}")

    def generate_query_embedding(self, query_text: str) -> List[float]:
        """Generate embedding for query text using Titan Text Embeddings V2."""
        try:
            # Use us-west-2 for Titan embeddings (where it's available)
            titan_client = boto3.client('bedrock-runtime', region_name='us-west-2')
            
            body = json.dumps({
                "inputText": query_text,
                "dimensions": 1024,
                "normalize": True,
                "embeddingTypes": ["float"]
            })
            
            response = titan_client.invoke_model(
                body=body,
                modelId=self.embedding_model,
                accept="application/json",
                contentType="application/json"
            )
            
            response_body = json.loads(response["body"].read())
            embedding = response_body["embedding"]
            
            logger.info(f"Generated embedding for query: '{query_text[:50]}...'")
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating query embedding: {str(e)}")
            return None

    def search_relevant_docs(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant documentation using S3 Vectors."""
        try:
            # Generate query embedding
            query_embedding = self.generate_query_embedding(query_text)
            if not query_embedding:
                return []
            
            # Search vectors
            response = self.s3vectors_client.query_vectors(
                vectorBucketName=self.vector_bucket_name,
                indexName=self.index_name,
                queryVector={'float32': query_embedding},
                topK=top_k,
                returnDistance=True,
                returnMetadata=True
            )
            
            vectors = response.get('vectors', [])
            logger.info(f"Found {len(vectors)} relevant documents")
            
            # Process and enrich results
            processed_results = []
            for i, vector in enumerate(vectors, 1):
                metadata = vector.get('metadata', {})
                distance = vector.get('distance', 1.0)
                similarity = (1 - distance) * 100
                
                processed_result = {
                    'rank': i,
                    'key': vector.get('key', 'unknown'),
                    'similarity_score': round(similarity, 1),
                    'service_name': metadata.get('service_name', 'Unknown'),
                    'document_type': metadata.get('document_type', 'documentation'),
                    'content_preview': metadata.get('content_preview', ''),
                    'content_length': metadata.get('content_length', 0),
                    'source_file': metadata.get('source_file', ''),
                    'raw_distance': distance
                }
                processed_results.append(processed_result)
            
            return processed_results
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []

    def generate_rag_response(self, user_question: str, relevant_docs: List[Dict[str, Any]]) -> str:
        """Generate comprehensive response using Claude 3.5 Sonnet with retrieved context."""
        try:
            # Prepare context from retrieved documents
            context_parts = []
            for doc in relevant_docs:
                context_parts.append(f"""
**Source {doc['rank']}** (Similarity: {doc['similarity_score']}%)
Service: {doc['service_name']}
Type: {doc['document_type']}
Content: {doc['content_preview']}
""")
            
            context = "\n".join(context_parts)
            
            # Create comprehensive prompt for Claude
            prompt = f"""You are an expert AWS solutions architect and documentation assistant. A user has asked a question about AWS services, and I've retrieved the most relevant documentation sections using semantic search.

**User Question:** {user_question}

**Retrieved AWS Documentation Context:**
{context}

**Instructions:**
1. Provide a comprehensive, accurate answer to the user's question based on the retrieved documentation
2. Structure your response with clear headings and bullet points where appropriate
3. Include specific AWS service names, features, and best practices mentioned in the context
4. If the context doesn't fully answer the question, acknowledge what information is available and what might be missing
5. Provide actionable recommendations and next steps where relevant
6. At the end, include a "Sources" section referencing which retrieved documents you used
7. Suggest 2-3 related follow-up questions the user might want to ask

**Response Format:**
## Answer

[Your comprehensive answer here]

## Key Points
- [Important point 1]
- [Important point 2]
- [Important point 3]

## Recommendations
- [Actionable recommendation 1]
- [Actionable recommendation 2]

## Sources
- Source 1: [Service Name] - [Document Type] (Similarity: X%)
- Source 2: [Service Name] - [Document Type] (Similarity: X%)

## Related Questions You Might Ask
1. [Related question 1]
2. [Related question 2]
3. [Related question 3]

Please provide a helpful, accurate, and well-structured response based on the AWS documentation context provided."""

            # Call Claude 3.5 Sonnet
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
            
            response = self.bedrock_client.invoke_model(
                body=body,
                modelId=self.llm_model,
                accept="application/json",
                contentType="application/json"
            )
            
            response_body = json.loads(response["body"].read())
            claude_response = response_body["content"][0]["text"]
            
            logger.info("Generated RAG response using Claude 3.5 Sonnet")
            return claude_response
            
        except Exception as e:
            logger.error(f"Error generating RAG response: {str(e)}")
            return f"I apologize, but I encountered an error while generating a response: {str(e)}"

    def process_question(self, user_question: str, top_k: int = 5) -> Dict[str, Any]:
        """Process a user question through the complete RAG pipeline."""
        logger.info(f"Processing question: '{user_question}'")
        
        # Step 1: Search for relevant documentation
        print("🔍 Searching AWS documentation...")
        relevant_docs = self.search_relevant_docs(user_question, top_k)
        
        if not relevant_docs:
            return {
                'question': user_question,
                'answer': "I couldn't find relevant documentation for your question. Please try rephrasing or asking about a different AWS topic.",
                'sources': [],
                'timestamp': datetime.now().isoformat()
            }
        
        # Step 2: Generate comprehensive response
        print("🧠 Generating comprehensive answer with Claude 3.5 Sonnet...")
        rag_response = self.generate_rag_response(user_question, relevant_docs)
        
        # Step 3: Prepare final response
        result = {
            'question': user_question,
            'answer': rag_response,
            'sources': relevant_docs,
            'timestamp': datetime.now().isoformat(),
            'model_used': self.llm_model,
            'documents_retrieved': len(relevant_docs)
        }
        
        return result

    def interactive_chat(self):
        """Interactive chat interface for the RAG system."""
        print("🚀 AWS Documentation RAG System - Interactive Chat")
        print("=" * 60)
        print("💡 Ask me anything about AWS services!")
        print("📚 I'll search through your documentation and provide comprehensive answers.")
        print("\n💡 Example questions:")
        print("   • How do I scale Lambda functions automatically?")
        print("   • What are S3 security best practices?")
        print("   • How to optimize DynamoDB performance?")
        print("   • When should I use ECS vs EKS?")
        print("\n⌨️  Commands: 'quit' to exit, 'help' for more info")
        print("-" * 60)
        
        while True:
            try:
                # Get user input
                user_question = input("\n🤔 Your AWS question: ").strip()
                
                if user_question.lower() in ['quit', 'exit', 'q']:
                    print("👋 Thank you for using the AWS Documentation RAG System!")
                    break
                
                if user_question.lower() == 'help':
                    self.show_help()
                    continue
                
                if not user_question:
                    continue
                
                # Process the question
                print(f"\n⏳ Processing: '{user_question}'")
                result = self.process_question(user_question)
                
                # Display the response
                print("\n" + "="*80)
                print("🎯 AWS DOCUMENTATION RAG RESPONSE")
                print("="*80)
                print(result['answer'])
                print("\n" + "="*80)
                print(f"📊 Retrieved {result['documents_retrieved']} relevant documents")
                print(f"🤖 Generated by: {result['model_used']}")
                print(f"⏰ Timestamp: {result['timestamp']}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")

    def show_help(self):
        """Show help information."""
        help_text = """
🆘 AWS Documentation RAG System Help

🎯 What This System Does:
   • Searches your AWS documentation using semantic similarity
   • Uses Claude 3.5 Sonnet to generate comprehensive answers
   • Provides source attribution and confidence scores
   • Suggests related follow-up questions

📝 Question Examples:
   • "How do I scale Lambda functions automatically?"
   • "What are the security best practices for S3 buckets?"
   • "How to optimize DynamoDB read performance?"
   • "When should I use ECS instead of EKS?"
   • "What are the cost optimization strategies for EC2?"

🔧 System Details:
   • Vector Search: S3 Vectors with 1024D Titan embeddings
   • LLM: Claude 3.5 Sonnet for response generation
   • Knowledge Base: 139 AWS documentation chunks
   • Search Method: Cosine similarity with semantic understanding

⌨️  Commands:
   • 'help' - Show this help
   • 'quit' or 'q' - Exit the system
        """
        print(help_text)

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="AWS Documentation RAG System with Claude 3.5 Sonnet")
    parser.add_argument("--question", "-q", help="Ask a single question")
    parser.add_argument("--top-k", "-k", type=int, default=5, help="Number of documents to retrieve")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive chat mode")
    
    args = parser.parse_args()
    
    # Configuration
    VECTOR_BUCKET_NAME = "vibhup-aws-docs-vectors"
    INDEX_NAME = "aws-documentation"
    
    # Initialize RAG system
    rag_system = AWSDocsRAGSystem(
        vector_bucket_name=VECTOR_BUCKET_NAME,
        index_name=INDEX_NAME,
        s3vectors_region="us-east-1",
        bedrock_region="us-east-1"
    )
    
    if args.question:
        # Single question mode
        print(f"🤔 Question: {args.question}")
        result = rag_system.process_question(args.question, args.top_k)
        
        print("\n" + "="*80)
        print("🎯 AWS DOCUMENTATION RAG RESPONSE")
        print("="*80)
        print(result['answer'])
        print("\n" + "="*80)
        print(f"📊 Retrieved {result['documents_retrieved']} relevant documents")
        print(f"🤖 Generated by: {result['model_used']}")
        print(f"⏰ Timestamp: {result['timestamp']}")
        
    else:
        # Interactive mode
        rag_system.interactive_chat()

if __name__ == "__main__":
    main()
