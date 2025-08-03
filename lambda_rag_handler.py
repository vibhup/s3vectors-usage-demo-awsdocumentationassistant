#!/usr/bin/env python3
"""
AWS Documentation RAG System - Lambda Handler

Lambda function to handle RAG queries from the React UI.
Provides API endpoints for:
- /ask - Process user questions
- /examples - Get example questions
- /health - Health check
"""

import json
import boto3
import logging
import time
from typing import List, Dict, Any
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ExecutionTracker:
    """Track execution steps and AWS API calls for transparency."""
    
    def __init__(self):
        self.steps = []
        self.api_calls = []
        self.start_time = time.time()
        self.metrics = {}
    
    def add_step(self, step_name: str, description: str = ""):
        """Add an execution step with timestamp."""
        current_time = time.time()
        duration = current_time - self.start_time
        
        step = {
            "step": step_name,
            "description": description,
            "timestamp": current_time,
            "duration_from_start": round(duration, 3),
            "status": "completed"
        }
        self.steps.append(step)
        logger.info(f"Step: {step_name} - {description} ({duration:.3f}s)")
    
    def add_api_call(self, service: str, operation: str, details: Dict = None):
        """Track AWS API calls with exact details."""
        api_call = {
            "service": service,
            "operation": operation,
            "timestamp": time.time(),
            "duration_from_start": round(time.time() - self.start_time, 3),
            "details": details or {}
        }
        self.api_calls.append(api_call)
        logger.info(f"AWS API: {service}:{operation} - {details}")
    
    def add_metric(self, key: str, value: Any):
        """Add performance metrics."""
        self.metrics[key] = value
    
    def get_summary(self):
        """Get complete execution summary."""
        total_duration = time.time() - self.start_time
        return {
            "total_duration": round(total_duration, 3),
            "steps": self.steps,
            "api_calls": self.api_calls,
            "metrics": self.metrics,
            "timestamp": datetime.utcnow().isoformat()
        }

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
        
        logger.info(f"Initialized RAG System for Lambda")

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

    def search_relevant_docs(self, query_text: str, top_k: int = 5, tracker: ExecutionTracker = None) -> List[Dict[str, Any]]:
        """Search for relevant documentation using S3 Vectors."""
        try:
            if tracker:
                tracker.add_step("query_processing", f"Processing user query: '{query_text[:50]}...'")
            
            # Generate query embedding
            if tracker:
                tracker.add_step("embedding_generation", "Generating query embedding with Titan Text V2")
                tracker.add_api_call("bedrock-runtime", "InvokeModel", {
                    "model": "amazon.titan-embed-text-v2:0",
                    "region": "us-west-2",
                    "input_text_length": len(query_text),
                    "embedding_dimensions": 1024
                })
            
            query_embedding = self.generate_query_embedding(query_text)
            if not query_embedding:
                return []
            
            if tracker:
                tracker.add_step("vector_search", f"Searching S3 Vectors index for top {top_k} matches")
                tracker.add_api_call("s3vectors", "QueryVectors", {
                    "bucket": self.vector_bucket_name,
                    "index": self.index_name,
                    "region": self.s3vectors_region,
                    "top_k": top_k,
                    "vector_dimensions": len(query_embedding)
                })
            
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
            
            if tracker:
                tracker.add_step("document_retrieval", f"Retrieved {len(vectors)} relevant documents")
                tracker.add_api_call("s3vectors", "GetVectors", {
                    "bucket": self.vector_bucket_name,
                    "index": self.index_name,
                    "region": self.s3vectors_region,
                    "documents_retrieved": len(vectors)
                })
                tracker.add_metric("documents_found", len(vectors))
                tracker.add_metric("query_vector_dimensions", len(query_embedding))
            
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

    def generate_rag_response(self, user_question: str, relevant_docs: List[Dict[str, Any]], tracker: ExecutionTracker = None) -> str:
        """Generate comprehensive response using Claude 3.5 Sonnet with retrieved context."""
        try:
            if tracker:
                tracker.add_step("context_assembly", f"Assembling context from {len(relevant_docs)} documents")
            
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

            # Calculate token counts for tracking
            input_tokens = len(prompt.split()) * 1.3  # Rough estimate
            
            if tracker:
                tracker.add_step("claude_generation", "Generating comprehensive answer with Claude 3.5 Sonnet")
                tracker.add_api_call("bedrock-runtime", "InvokeModel", {
                    "model": "anthropic.claude-3-5-sonnet-20240620-v1:0",
                    "region": self.bedrock_region,
                    "max_tokens": 4000,
                    "temperature": 0.1,
                    "estimated_input_tokens": int(input_tokens)
                })
                tracker.add_metric("context_documents", len(relevant_docs))
                tracker.add_metric("estimated_input_tokens", int(input_tokens))

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
            
            if tracker:
                output_tokens = len(claude_response.split()) * 1.3  # Rough estimate
                tracker.add_metric("estimated_output_tokens", int(output_tokens))
                tracker.add_step("response_complete", "RAG response generation completed")
            
            logger.info("Generated RAG response using Claude 3.5 Sonnet")
            return claude_response
            
        except Exception as e:
            logger.error(f"Error generating RAG response: {str(e)}")
            return f"I apologize, but I encountered an error while generating a response: {str(e)}"

    def process_question(self, user_question: str, top_k: int = 5) -> Dict[str, Any]:
        """Process a user question through the complete RAG pipeline."""
        logger.info(f"Processing question: '{user_question}'")
        
        # Initialize execution tracker
        tracker = ExecutionTracker()
        tracker.add_step("request_received", f"Processing user question: '{user_question[:50]}...'")
        
        # Step 1: Search for relevant documentation
        relevant_docs = self.search_relevant_docs(user_question, top_k, tracker)
        
        if not relevant_docs:
            tracker.add_step("no_results", "No relevant documents found")
            return {
                'question': user_question,
                'answer': "I couldn't find relevant documentation for your question. Please try rephrasing or asking about a different AWS topic.",
                'sources': [],
                'timestamp': datetime.now().isoformat(),
                'technical_details': tracker.get_summary()
            }
        
        # Step 2: Generate comprehensive response
        rag_response = self.generate_rag_response(user_question, relevant_docs, tracker)
        
        # Step 3: Prepare final response
        execution_summary = tracker.get_summary()
        
        result = {
            'question': user_question,
            'answer': rag_response,
            'sources': relevant_docs,
            'timestamp': datetime.now().isoformat(),
            'model_used': self.llm_model,
            'documents_retrieved': len(relevant_docs),
            'technical_details': execution_summary
        }
        
        return result

# Global RAG system instance (initialized once per Lambda container)
rag_system = None

def get_rag_system():
    """Get or initialize the RAG system instance."""
    global rag_system
    if rag_system is None:
        rag_system = AWSDocsRAGSystem(
            vector_bucket_name="vibhup-aws-docs-vectors",
            index_name="aws-documentation",
            s3vectors_region="us-east-1",
            bedrock_region="us-east-1"
        )
    return rag_system

def get_example_questions():
    """Return example questions organized by AWS service category."""
    return {
        "compute": [
            "How do I scale Lambda functions automatically?",
            "What are the best practices for EC2 instance optimization?",
            "When should I use ECS vs EKS for containerized applications?",
            "How to implement auto-scaling for EC2 instances?"
        ],
        "storage": [
            "What are S3 security best practices?",
            "How to optimize S3 costs with storage classes?",
            "What's the difference between EBS volume types?",
            "How to implement S3 cross-region replication?"
        ],
        "database": [
            "How to optimize DynamoDB performance?",
            "What are RDS backup and recovery options?",
            "When to use DynamoDB vs RDS?",
            "How to implement DynamoDB global tables?"
        ],
        "networking": [
            "How to set up VPC peering connections?",
            "What are CloudFront caching strategies?",
            "How to configure Application Load Balancer?",
            "What are VPC security group best practices?"
        ],
        "security": [
            "How to implement IAM least privilege access?",
            "What are AWS security monitoring best practices?",
            "How to use AWS Secrets Manager effectively?",
            "What are CloudTrail logging recommendations?"
        ]
    }

def lambda_handler(event, context):
    """Main Lambda handler for API Gateway requests."""
    try:
        # Parse the request
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        body = event.get('body')
        
        # Add CORS headers
        cors_headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        }
        
        # Handle preflight OPTIONS requests
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': cors_headers,
                'body': json.dumps({'message': 'CORS preflight'})
            }
        
        # Route requests
        if path == '/ask' and http_method == 'POST':
            return handle_ask_question(body, cors_headers)
        elif path == '/examples' and http_method == 'GET':
            return handle_get_examples(cors_headers)
        elif path == '/health' and http_method == 'GET':
            return handle_health_check(cors_headers)
        else:
            return {
                'statusCode': 404,
                'headers': cors_headers,
                'body': json.dumps({'error': 'Endpoint not found'})
            }
            
    except Exception as e:
        logger.error(f"Lambda handler error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': 'Internal server error'})
        }

def handle_ask_question(body, cors_headers):
    """Handle /ask endpoint - process user questions."""
    try:
        if not body:
            return {
                'statusCode': 400,
                'headers': cors_headers,
                'body': json.dumps({'error': 'Request body is required'})
            }
        
        request_data = json.loads(body)
        question = request_data.get('question', '').strip()
        
        if not question:
            return {
                'statusCode': 400,
                'headers': cors_headers,
                'body': json.dumps({'error': 'Question is required'})
            }
        
        # Process the question through RAG system
        rag_system = get_rag_system()
        result = rag_system.process_question(question)
        
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({
                'success': True,
                'data': result
            })
        }
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': f'Error processing question: {str(e)}'})
        }

def handle_get_examples(cors_headers):
    """Handle /examples endpoint - return example questions."""
    try:
        examples = get_example_questions()
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({
                'success': True,
                'data': examples
            })
        }
    except Exception as e:
        logger.error(f"Error getting examples: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': 'Error getting examples'})
        }

def handle_health_check(cors_headers):
    """Handle /health endpoint - health check."""
    return {
        'statusCode': 200,
        'headers': cors_headers,
        'body': json.dumps({
            'success': True,
            'message': 'AWS Documentation RAG System is healthy',
            'timestamp': datetime.now().isoformat()
        })
    }
