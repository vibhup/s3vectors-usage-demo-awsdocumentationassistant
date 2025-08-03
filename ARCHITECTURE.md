# 🏗️ System Architecture

This document provides a detailed technical overview of the AWS Documentation Assistant RAG system architecture, design decisions, and implementation details.

## 📊 High-Level Architecture

```mermaid
graph TB
    User[👤 User] --> CF[☁️ CloudFront]
    CF --> S3[📦 S3 Static Website]
    S3 --> React[⚛️ React UI]
    
    React --> APIGW[🚪 API Gateway]
    APIGW --> Lambda[⚡ Lambda Function]
    
    Lambda --> Bedrock1[🧠 Bedrock - Titan Embeddings]
    Lambda --> S3V[🗄️ S3 Vectors]
    Lambda --> Bedrock2[🧠 Bedrock - Claude 3.5 Sonnet]
    
    S3V --> VectorDB[(Vector Database)]
    
    subgraph "AWS Services"
        CF
        S3
        APIGW
        Lambda
        Bedrock1
        Bedrock2
        S3V
        VectorDB
    end
    
    subgraph "External"
        User
        React
    end
```

## 🔄 RAG Pipeline Flow

### 1. Query Processing Pipeline

```mermaid
sequenceDiagram
    participant U as User
    participant UI as React UI
    participant AG as API Gateway
    participant L as Lambda
    participant T as Titan Embeddings
    participant SV as S3 Vectors
    participant C as Claude 3.5 Sonnet
    
    U->>UI: Ask Question
    UI->>AG: POST /ask
    AG->>L: Invoke Function
    
    Note over L: Start Execution Tracking
    L->>L: Process Query (0.1s)
    
    L->>T: Generate Embeddings (0.8s)
    T-->>L: Query Vector [1024 dims]
    
    L->>SV: Query Vectors (1.2s)
    SV-->>L: Top 5 Documents + Similarity Scores
    
    L->>L: Assemble Context (0.3s)
    
    L->>C: Generate Answer (8.5s)
    C-->>L: Comprehensive Response
    
    Note over L: Complete Execution Tracking
    L-->>AG: Response + Technical Details
    AG-->>UI: JSON Response
    UI-->>U: Display Answer + Technical Panel
```

### 2. Data Flow Architecture

```mermaid
graph LR
    subgraph "Data Ingestion"
        MD[📄 Markdown Docs] --> PP[🔄 Preprocessing]
        PP --> Chunks[📝 Text Chunks]
        Chunks --> TE[🧠 Titan Embeddings]
        TE --> Vectors[🔢 Vector Embeddings]
        Vectors --> S3V[🗄️ S3 Vectors Index]
    end
    
    subgraph "Query Processing"
        Q[❓ User Query] --> QE[🧠 Query Embedding]
        QE --> VS[🔍 Vector Search]
        VS --> S3V
        S3V --> Results[📊 Search Results]
        Results --> Context[📋 Context Assembly]
        Context --> LLM[🧠 Claude 3.5 Sonnet]
        LLM --> Answer[💬 Final Answer]
    end
```

## 🧩 Component Architecture

### Frontend Components

```
React Application
├── App.js (Main Application)
├── Components/
│   ├── ChatMessage (Message Display)
│   ├── TechnicalDetailsPanel (Transparency View)
│   ├── ExamplesSection (Knowledge Base Coverage)
│   └── LoadingIndicator (Progress Display)
├── Styles/
│   └── App.css (AWS-themed Styling)
└── Utils/
    └── api.js (API Communication)
```

### Backend Components

```
Lambda Function
├── lambda_rag_handler.py (Main Handler)
├── Classes/
│   ├── AWSDocsRAGSystem (Core RAG Logic)
│   └── ExecutionTracker (Performance Monitoring)
├── Functions/
│   ├── generate_query_embedding()
│   ├── search_relevant_docs()
│   ├── generate_rag_response()
│   └── process_question()
└── Utilities/
    ├── get_example_questions()
    └── health_check()
```

## 🔧 Technical Implementation Details

### S3 Vectors Integration

```python
class S3VectorsClient:
    def __init__(self, region='us-east-1'):
        self.client = boto3.client('s3vectors', region_name=region)
    
    def query_vectors(self, bucket_name, index_name, query_vector, top_k=5):
        """
        Query S3 Vectors for semantic similarity search
        
        Args:
            bucket_name: S3 bucket containing the vector index
            index_name: Name of the vector index
            query_vector: Query embedding (1024 dimensions)
            top_k: Number of results to return
            
        Returns:
            List of similar documents with similarity scores
        """
        response = self.client.query_vectors(
            vectorBucketName=bucket_name,
            indexName=index_name,
            queryVector={'float32': query_vector},
            topK=top_k,
            returnDistance=True,
            returnMetadata=True
        )
        return response.get('vectors', [])
```

### Bedrock Integration

```python
class BedrockClient:
    def __init__(self, region='us-east-1'):
        self.client = boto3.client('bedrock-runtime', region_name=region)
    
    def generate_embeddings(self, text):
        """Generate embeddings using Titan Text Embeddings V2"""
        body = json.dumps({
            "inputText": text,
            "dimensions": 1024,
            "normalize": True,
            "embeddingTypes": ["float"]
        })
        
        response = self.client.invoke_model(
            body=body,
            modelId="amazon.titan-embed-text-v2:0",
            accept="application/json",
            contentType="application/json"
        )
        
        return json.loads(response["body"].read())["embedding"]
    
    def generate_response(self, prompt):
        """Generate response using Claude 3.5 Sonnet"""
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "temperature": 0.1,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        response = self.client.invoke_model(
            body=body,
            modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
            accept="application/json",
            contentType="application/json"
        )
        
        return json.loads(response["body"].read())["content"][0]["text"]
```

### Execution Tracking System

```python
class ExecutionTracker:
    """Track execution steps and AWS API calls for transparency"""
    
    def __init__(self):
        self.steps = []
        self.api_calls = []
        self.start_time = time.time()
        self.metrics = {}
    
    def add_step(self, step_name, description=""):
        """Add an execution step with timestamp"""
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
    
    def add_api_call(self, service, operation, details=None):
        """Track AWS API calls with exact details"""
        api_call = {
            "service": service,
            "operation": operation,
            "timestamp": time.time(),
            "duration_from_start": round(time.time() - self.start_time, 3),
            "details": details or {}
        }
        self.api_calls.append(api_call)
    
    def get_summary(self):
        """Get complete execution summary"""
        return {
            "total_duration": round(time.time() - self.start_time, 3),
            "steps": self.steps,
            "api_calls": self.api_calls,
            "metrics": self.metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
```

## 📊 Data Architecture

### Vector Index Structure

```json
{
  "index_name": "aws-docs-index",
  "dimensions": 1024,
  "vector_count": 139,
  "metadata_schema": {
    "chunk_id": "string",
    "source_file": "string",
    "title": "string",
    "section": "string",
    "service_name": "string",
    "document_type": "string",
    "token_count": "integer",
    "char_count": "integer",
    "processing_timestamp": "string"
  }
}
```

### Document Chunk Format

```json
{
  "chunk_id": "42cff905_003",
  "source_file": "aws_services_comprehensive_overview.md",
  "title": "Comprehensive AWS Services Overview",
  "section": "Amazon EC2 (Elastic Compute Cloud)",
  "content": "Amazon EC2 provides secure, resizable compute capacity...",
  "service_name": "EC2",
  "document_type": "guide",
  "token_count": 245,
  "char_count": 1038,
  "chunk_index": 3,
  "total_chunks": 81,
  "metadata": {
    "header_level": 1,
    "file_size_chars": 25294,
    "processing_timestamp": "2025-08-02"
  }
}
```

## 🔐 Security Architecture

### IAM Permissions Model

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0",
        "arn:aws:bedrock:*::foundation-model/amazon.titan-embed-text-v2:0"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3vectors:QueryVectors",
        "s3vectors:GetVectors"
      ],
      "Resource": "arn:aws:s3vectors:*:*:index/*"
    }
  ]
}
```

### Network Security

```mermaid
graph TB
    Internet[🌐 Internet] --> CF[☁️ CloudFront]
    CF --> |HTTPS Only| S3[📦 S3 Bucket]
    
    Internet --> |HTTPS Only| APIGW[🚪 API Gateway]
    APIGW --> |Private| Lambda[⚡ Lambda]
    
    Lambda --> |IAM Roles| Bedrock[🧠 Bedrock]
    Lambda --> |IAM Roles| S3V[🗄️ S3 Vectors]
    
    subgraph "Security Layers"
        WAF[🛡️ WAF]
        IAM[🔐 IAM Roles]
        VPC[🏠 VPC Endpoints]
    end
    
    CF -.-> WAF
    Lambda -.-> IAM
    Lambda -.-> VPC
```

## 📈 Performance Architecture

### Caching Strategy

```mermaid
graph LR
    User[👤 User] --> CF[☁️ CloudFront Cache]
    CF --> |Cache Miss| S3[📦 S3]
    
    User --> API[🚪 API Gateway]
    API --> |Cache Miss| Lambda[⚡ Lambda]
    
    Lambda --> |Frequent Queries| Cache[💾 ElastiCache]
    Lambda --> |Cache Miss| Bedrock[🧠 Bedrock]
    Lambda --> |Vector Search| S3V[🗄️ S3 Vectors]
    
    subgraph "Caching Layers"
        CF
        Cache
        S3V
    end
```

### Performance Metrics

| Component | Metric | Target | Actual |
|-----------|--------|--------|--------|
| CloudFront | Cache Hit Ratio | >90% | 95% |
| API Gateway | Response Time | <100ms | 85ms |
| Lambda | Cold Start | <2s | 1.5s |
| Lambda | Warm Execution | <15s | 11s |
| S3 Vectors | Query Time | <2s | 1.2s |
| Bedrock Titan | Embedding Time | <1s | 0.8s |
| Bedrock Claude | Generation Time | <10s | 8.5s |

## 🔄 Scalability Architecture

### Auto-Scaling Components

```mermaid
graph TB
    subgraph "Auto-Scaling Services"
        CF[☁️ CloudFront - Global]
        APIGW[🚪 API Gateway - Regional]
        Lambda[⚡ Lambda - Auto-scale]
        Bedrock[🧠 Bedrock - Managed]
        S3V[🗄️ S3 Vectors - Managed]
    end
    
    subgraph "Scaling Triggers"
        CW[📊 CloudWatch Metrics]
        Alarms[🚨 CloudWatch Alarms]
        ASG[📈 Auto Scaling Groups]
    end
    
    Lambda --> CW
    CW --> Alarms
    Alarms --> ASG
```

### Capacity Planning

| Service | Current Capacity | Max Capacity | Scaling Method |
|---------|------------------|--------------|----------------|
| Lambda | 1000 concurrent | 10000 concurrent | Automatic |
| API Gateway | 10000 RPS | 50000 RPS | Request increase |
| Bedrock | 100 TPM | 1000 TPM | Request increase |
| S3 Vectors | 1000 QPS | 10000 QPS | Automatic |
| CloudFront | Unlimited | Unlimited | Global CDN |

## 🔍 Monitoring Architecture

### Observability Stack

```mermaid
graph TB
    subgraph "Application"
        Lambda[⚡ Lambda Function]
        APIGW[🚪 API Gateway]
        CF[☁️ CloudFront]
    end
    
    subgraph "Monitoring"
        CW[📊 CloudWatch Metrics]
        Logs[📝 CloudWatch Logs]
        XRay[🔍 X-Ray Tracing]
        Dashboard[📈 CloudWatch Dashboard]
    end
    
    subgraph "Alerting"
        SNS[📧 SNS Topics]
        Alarms[🚨 CloudWatch Alarms]
    end
    
    Lambda --> CW
    Lambda --> Logs
    Lambda --> XRay
    APIGW --> CW
    CF --> CW
    
    CW --> Dashboard
    CW --> Alarms
    Alarms --> SNS
```

### Key Metrics Tracked

1. **Application Metrics**
   - Request count and rate
   - Response time (p50, p95, p99)
   - Error rate and types
   - Token usage and costs

2. **Infrastructure Metrics**
   - Lambda duration and memory usage
   - API Gateway latency
   - CloudFront cache hit ratio
   - S3 Vectors query performance

3. **Business Metrics**
   - User engagement
   - Question categories
   - Response quality scores
   - Cost per query

## 🚀 Deployment Architecture

### CI/CD Pipeline

```mermaid
graph LR
    Dev[👨‍💻 Developer] --> Git[📚 GitHub]
    Git --> |Webhook| Pipeline[🔄 GitHub Actions]
    
    Pipeline --> Test[🧪 Unit Tests]
    Test --> Build[🏗️ Build]
    Build --> Package[📦 Package]
    
    Package --> |Backend| LambdaDeploy[⚡ Lambda Deploy]
    Package --> |Frontend| S3Deploy[📦 S3 Deploy]
    
    LambdaDeploy --> Prod[🌐 Production]
    S3Deploy --> CFInvalidate[☁️ CloudFront Invalidate]
    CFInvalidate --> Prod
```

### Environment Strategy

| Environment | Purpose | Resources | Deployment |
|-------------|---------|-----------|------------|
| Development | Local testing | Local/Docker | Manual |
| Staging | Integration testing | AWS (reduced) | Automated |
| Production | Live system | AWS (full) | Automated |

## 💰 Cost Architecture

### Cost Breakdown

```mermaid
pie title Monthly Cost Distribution
    "Bedrock (40%)" : 40
    "S3 Vectors (25%)" : 25
    "Lambda (15%)" : 15
    "CloudFront (10%)" : 10
    "API Gateway (5%)" : 5
    "Other (5%)" : 5
```

### Cost Optimization Strategies

1. **Caching Implementation**
   - CloudFront for static content
   - API Gateway caching for common queries
   - Lambda result caching

2. **Resource Optimization**
   - Right-sizing Lambda memory
   - Optimizing Bedrock token usage
   - Efficient vector search queries

3. **Usage Monitoring**
   - Cost alerts and budgets
   - Usage analytics and optimization
   - Reserved capacity where applicable

## 🔮 Future Architecture Considerations

### Planned Enhancements

1. **Multi-Region Deployment**
   - Global S3 Vectors replication
   - Regional Bedrock endpoints
   - Cross-region failover

2. **Advanced Caching**
   - Redis/ElastiCache integration
   - Intelligent cache warming
   - Query result caching

3. **Enhanced Security**
   - VPC endpoints
   - Private subnets
   - Enhanced monitoring

4. **Performance Optimization**
   - Connection pooling
   - Batch processing
   - Async processing

### Scalability Roadmap

| Phase | Target Scale | Key Changes |
|-------|--------------|-------------|
| Phase 1 | 1K users/day | Current architecture |
| Phase 2 | 10K users/day | Add caching layer |
| Phase 3 | 100K users/day | Multi-region deployment |
| Phase 4 | 1M users/day | Microservices architecture |

---

This architecture provides a solid foundation for a production-ready RAG system while maintaining flexibility for future enhancements and scaling requirements.
