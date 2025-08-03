# 🚀 Complete Deployment Guide

This guide provides step-by-step instructions to deploy the AWS Documentation Assistant RAG system in your own AWS account.

## 📋 Prerequisites

### AWS Account Setup
- AWS Account with administrative access
- AWS CLI installed and configured
- Access to the following AWS services:
  - Amazon S3 Vectors (Preview)
  - Amazon Bedrock (Claude 3.5 Sonnet, Titan Embeddings V2)
  - AWS Lambda
  - Amazon API Gateway
  - Amazon S3
  - Amazon CloudFront
  - Amazon Route 53 (optional, for custom domain)
  - AWS Certificate Manager (optional, for SSL)

### Local Development Environment
```bash
# Required software
- Python 3.9+
- Node.js 18+
- npm or yarn
- Git
- jq (for JSON processing)

# Verify installations
python3 --version
node --version
npm --version
aws --version
```

### Bedrock Model Access
Enable access to required models in Amazon Bedrock:
1. Go to Amazon Bedrock console
2. Navigate to "Model access"
3. Request access to:
   - `anthropic.claude-3-5-sonnet-20240620-v1:0`
   - `amazon.titan-embed-text-v2:0`

## 🏗️ Step 1: Infrastructure Setup

### 1.1 Create IAM Role for Lambda

```bash
# Create trust policy
cat > lambda-trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create IAM role
aws iam create-role \
  --role-name lambda-rag-execution-role \
  --assume-role-policy-document file://lambda-trust-policy.json

# Create policy for Lambda permissions
cat > lambda-rag-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
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
      "Resource": "*"
    }
  ]
}
EOF

# Attach policy to role
aws iam put-role-policy \
  --role-name lambda-rag-execution-role \
  --policy-name lambda-rag-policy \
  --policy-document file://lambda-rag-policy.json
```

### 1.2 Create S3 Bucket for Frontend

```bash
# Create unique bucket name
BUCKET_NAME="aws-docs-rag-ui-$(date +%s)"
echo "Bucket name: $BUCKET_NAME"

# Create S3 bucket
aws s3 mb s3://$BUCKET_NAME

# Configure bucket for static website hosting
aws s3 website s3://$BUCKET_NAME \
  --index-document index.html \
  --error-document index.html

# Create bucket policy for CloudFront access
cat > s3-bucket-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudFrontAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity YOUR-OAI-ID"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::$BUCKET_NAME/*"
    }
  ]
}
EOF
```

## 📊 Step 2: Data Preparation and S3 Vectors Setup

### 2.1 Prepare AWS Documentation Dataset

```bash
# Clone the repository
git clone https://github.com/vibhup/s3vectors-usage-demo-awsdocumentationassistant.git
cd s3vectors-usage-demo-awsdocumentationassistant

# Install Python dependencies
pip3 install -r requirements.txt

# Process AWS documentation
python3 preprocess_aws_docs.py
```

### 2.2 Create S3 Vectors Index

```bash
# Set your S3 Vectors configuration
export VECTOR_BUCKET_NAME="your-vector-bucket-name"
export INDEX_NAME="aws-docs-index"
export AWS_REGION="us-east-1"

# Create S3 Vectors index and insert embeddings
python3 insert_embeddings_to_s3_vectors.py

# Verify the index creation
aws s3vectors describe-index \
  --vector-bucket-name $VECTOR_BUCKET_NAME \
  --index-name $INDEX_NAME \
  --region $AWS_REGION
```

## ⚡ Step 3: Backend Deployment

### 3.1 Package Lambda Function

```bash
# Create deployment directory
mkdir lambda-deployment
cd lambda-deployment

# Copy Lambda function and dependencies
cp ../lambda_rag_handler.py .
cp ../aws_docs_rag_system.py .

# Install dependencies in deployment directory
pip3 install boto3 -t .

# Create deployment package
zip -r ../lambda-rag-function.zip .
cd ..
```

### 3.2 Deploy Lambda Function

```bash
# Get the IAM role ARN
ROLE_ARN=$(aws iam get-role --role-name lambda-rag-execution-role --query 'Role.Arn' --output text)

# Create Lambda function
aws lambda create-function \
  --function-name aws-docs-rag-api \
  --runtime python3.11 \
  --role $ROLE_ARN \
  --handler lambda_rag_handler.lambda_handler \
  --zip-file fileb://lambda-rag-function.zip \
  --timeout 60 \
  --memory-size 1024 \
  --environment Variables="{VECTOR_BUCKET_NAME=$VECTOR_BUCKET_NAME,INDEX_NAME=$INDEX_NAME}" \
  --region us-east-1

# Test the Lambda function
aws lambda invoke \
  --function-name aws-docs-rag-api \
  --payload '{"httpMethod":"GET","path":"/health"}' \
  response.json

cat response.json
```

### 3.3 Create API Gateway

```bash
# Create REST API
API_ID=$(aws apigateway create-rest-api \
  --name aws-docs-rag-api \
  --description "AWS Documentation RAG API" \
  --query 'id' --output text)

echo "API ID: $API_ID"

# Get root resource ID
ROOT_RESOURCE_ID=$(aws apigateway get-resources \
  --rest-api-id $API_ID \
  --query 'items[0].id' --output text)

# Create resources and methods
# /ask resource
ASK_RESOURCE_ID=$(aws apigateway create-resource \
  --rest-api-id $API_ID \
  --parent-id $ROOT_RESOURCE_ID \
  --path-part ask \
  --query 'id' --output text)

# /examples resource
EXAMPLES_RESOURCE_ID=$(aws apigateway create-resource \
  --rest-api-id $API_ID \
  --parent-id $ROOT_RESOURCE_ID \
  --path-part examples \
  --query 'id' --output text)

# /health resource
HEALTH_RESOURCE_ID=$(aws apigateway create-resource \
  --rest-api-id $API_ID \
  --parent-id $ROOT_RESOURCE_ID \
  --path-part health \
  --query 'id' --output text)

# Create methods and integrations (detailed commands in scripts/setup-api-gateway.sh)
```

### 3.4 Deploy API Gateway

```bash
# Create deployment
aws apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name prod

# Get API endpoint
API_ENDPOINT="https://$API_ID.execute-api.us-east-1.amazonaws.com/prod"
echo "API Endpoint: $API_ENDPOINT"
```

## 🎨 Step 4: Frontend Deployment

### 4.1 Build React Application

```bash
cd react-ui

# Install dependencies
npm install

# Update API endpoint in src/App.js
sed -i "s|const API_BASE_URL = .*|const API_BASE_URL = '$API_ENDPOINT';|" src/App.js

# Build production version
npm run build
```

### 4.2 Deploy to S3

```bash
# Upload build files to S3
aws s3 sync build/ s3://$BUCKET_NAME/ --delete

# Verify upload
aws s3 ls s3://$BUCKET_NAME/
```

### 4.3 Create CloudFront Distribution

```bash
# Create CloudFront Origin Access Identity
OAI_ID=$(aws cloudfront create-cloud-front-origin-access-identity \
  --cloud-front-origin-access-identity-config \
  CallerReference=$(date +%s),Comment="OAI for AWS Docs RAG UI" \
  --query 'CloudFrontOriginAccessIdentity.Id' --output text)

# Create CloudFront distribution configuration
cat > cloudfront-config.json << EOF
{
  "CallerReference": "aws-docs-rag-ui-$(date +%s)",
  "Comment": "AWS Docs RAG UI Distribution",
  "DefaultRootObject": "index.html",
  "Origins": {
    "Quantity": 1,
    "Items": [
      {
        "Id": "S3-$BUCKET_NAME",
        "DomainName": "$BUCKET_NAME.s3.amazonaws.com",
        "S3OriginConfig": {
          "OriginAccessIdentity": "origin-access-identity/cloudfront/$OAI_ID"
        }
      }
    ]
  },
  "DefaultCacheBehavior": {
    "TargetOriginId": "S3-$BUCKET_NAME",
    "ViewerProtocolPolicy": "redirect-to-https",
    "TrustedSigners": {
      "Enabled": false,
      "Quantity": 0
    },
    "ForwardedValues": {
      "QueryString": false,
      "Cookies": {
        "Forward": "none"
      }
    },
    "MinTTL": 0
  },
  "CustomErrorResponses": {
    "Quantity": 1,
    "Items": [
      {
        "ErrorCode": 404,
        "ResponsePagePath": "/index.html",
        "ResponseCode": "200",
        "ErrorCachingMinTTL": 300
      }
    ]
  },
  "Enabled": true,
  "PriceClass": "PriceClass_100"
}
EOF

# Create CloudFront distribution
DISTRIBUTION_ID=$(aws cloudfront create-distribution \
  --distribution-config file://cloudfront-config.json \
  --query 'Distribution.Id' --output text)

echo "Distribution ID: $DISTRIBUTION_ID"

# Get CloudFront domain name
CLOUDFRONT_DOMAIN=$(aws cloudfront get-distribution \
  --id $DISTRIBUTION_ID \
  --query 'Distribution.DomainName' --output text)

echo "CloudFront URL: https://$CLOUDFRONT_DOMAIN"
```

## 🌐 Step 5: Custom Domain Setup (Optional)

### 5.1 Request SSL Certificate

```bash
# Request ACM certificate
CERT_ARN=$(aws acm request-certificate \
  --domain-name your-domain.com \
  --validation-method DNS \
  --region us-east-1 \
  --query 'CertificateArn' --output text)

echo "Certificate ARN: $CERT_ARN"

# Get DNS validation records
aws acm describe-certificate \
  --certificate-arn $CERT_ARN \
  --region us-east-1 \
  --query 'Certificate.DomainValidationOptions[0].ResourceRecord'
```

### 5.2 Create Route 53 Records

```bash
# Get hosted zone ID
HOSTED_ZONE_ID=$(aws route53 list-hosted-zones \
  --query "HostedZones[?Name=='your-domain.com.'].Id" \
  --output text)

# Create DNS validation record (use output from previous command)
cat > dns-validation.json << EOF
{
  "Comment": "DNS validation for SSL certificate",
  "Changes": [
    {
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "VALIDATION_RECORD_NAME",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [
          {
            "Value": "VALIDATION_RECORD_VALUE"
          }
        ]
      }
    }
  ]
}
EOF

aws route53 change-resource-record-sets \
  --hosted-zone-id $HOSTED_ZONE_ID \
  --change-batch file://dns-validation.json

# Wait for certificate validation
aws acm wait certificate-validated \
  --certificate-arn $CERT_ARN \
  --region us-east-1

# Create ALIAS record for your domain
cat > domain-alias.json << EOF
{
  "Comment": "ALIAS record for custom domain",
  "Changes": [
    {
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "your-domain.com",
        "Type": "A",
        "AliasTarget": {
          "DNSName": "$CLOUDFRONT_DOMAIN",
          "EvaluateTargetHealth": false,
          "HostedZoneId": "Z2FDTNDATAQYW2"
        }
      }
    }
  ]
}
EOF

aws route53 change-resource-record-sets \
  --hosted-zone-id $HOSTED_ZONE_ID \
  --change-batch file://domain-alias.json
```

### 5.3 Update CloudFront with Custom Domain

```bash
# Get current distribution config
aws cloudfront get-distribution --id $DISTRIBUTION_ID > current-dist.json

# Extract ETag and config
ETAG=$(jq -r '.ETag' current-dist.json)
jq '.Distribution.DistributionConfig' current-dist.json > dist-config.json

# Update config with custom domain and SSL certificate
jq '.Aliases = {"Quantity": 1, "Items": ["your-domain.com"]} | 
    .ViewerCertificate = {
      "ACMCertificateArn": "'$CERT_ARN'",
      "SSLSupportMethod": "sni-only",
      "MinimumProtocolVersion": "TLSv1.2_2021",
      "CertificateSource": "acm"
    }' dist-config.json > updated-dist-config.json

# Update distribution
aws cloudfront update-distribution \
  --id $DISTRIBUTION_ID \
  --distribution-config file://updated-dist-config.json \
  --if-match $ETAG
```

## ✅ Step 6: Testing and Verification

### 6.1 Test Backend API

```bash
# Test health endpoint
curl -X GET "$API_ENDPOINT/health"

# Test examples endpoint
curl -X GET "$API_ENDPOINT/examples"

# Test ask endpoint
curl -X POST "$API_ENDPOINT/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I scale Lambda functions?"}'
```

### 6.2 Test Frontend

```bash
# Test CloudFront URL
curl -I "https://$CLOUDFRONT_DOMAIN"

# Test custom domain (if configured)
curl -I "https://your-domain.com"
```

### 6.3 Verify S3 Vectors Integration

```bash
# Check vector index status
aws s3vectors describe-index \
  --vector-bucket-name $VECTOR_BUCKET_NAME \
  --index-name $INDEX_NAME \
  --region $AWS_REGION

# Test vector query
python3 -c "
import boto3
import json

client = boto3.client('s3vectors', region_name='us-east-1')
response = client.query_vectors(
    vectorBucketName='$VECTOR_BUCKET_NAME',
    indexName='$INDEX_NAME',
    queryVector={'float32': [0.1] * 1024},
    topK=5
)
print(json.dumps(response, indent=2, default=str))
"
```

## 🔧 Step 7: Configuration and Customization

### 7.1 Environment Variables

Update Lambda environment variables:
```bash
aws lambda update-function-configuration \
  --function-name aws-docs-rag-api \
  --environment Variables="{
    VECTOR_BUCKET_NAME=$VECTOR_BUCKET_NAME,
    INDEX_NAME=$INDEX_NAME,
    BEDROCK_REGION=us-east-1,
    S3VECTORS_REGION=us-east-1
  }"
```

### 7.2 Monitoring Setup

```bash
# Create CloudWatch dashboard
aws cloudwatch put-dashboard \
  --dashboard-name "AWS-Docs-RAG-Dashboard" \
  --dashboard-body file://cloudwatch-dashboard.json

# Set up alarms
aws cloudwatch put-metric-alarm \
  --alarm-name "Lambda-Errors" \
  --alarm-description "Lambda function errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=FunctionName,Value=aws-docs-rag-api \
  --evaluation-periods 2
```

## 🚨 Troubleshooting

### Common Issues

1. **Bedrock Access Denied**
   - Ensure model access is enabled in Bedrock console
   - Check IAM permissions for bedrock:InvokeModel

2. **S3 Vectors Not Found**
   - Verify S3 Vectors service is available in your region
   - Check vector bucket name and index name

3. **Lambda Timeout**
   - Increase timeout to 60 seconds
   - Check memory allocation (recommend 1024MB)

4. **CORS Issues**
   - Verify API Gateway CORS configuration
   - Check preflight OPTIONS method setup

5. **CloudFront 403 Errors**
   - Verify S3 bucket policy allows CloudFront OAI
   - Check default root object configuration

### Debug Commands

```bash
# Check Lambda logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/aws-docs-rag-api"
aws logs tail "/aws/lambda/aws-docs-rag-api" --follow

# Check API Gateway logs
aws logs describe-log-groups --log-group-name-prefix "API-Gateway-Execution-Logs"

# Test S3 Vectors connectivity
aws s3vectors list-indexes --vector-bucket-name $VECTOR_BUCKET_NAME --region $AWS_REGION
```

## 💰 Cost Estimation

### Monthly Cost Breakdown (Moderate Usage)
- **S3 Vectors**: $20-40 (query-based pricing)
- **Lambda**: $10-20 (execution time and requests)
- **Bedrock**: $30-80 (model invocations)
- **API Gateway**: $5-10 (API calls)
- **CloudFront**: $5-15 (data transfer)
- **S3**: $2-5 (storage and requests)
- **Route 53**: $0.50 (hosted zone)

**Total Estimated Cost**: $72.50-170.50/month

### Cost Optimization Tips
- Use Lambda provisioned concurrency for consistent performance
- Implement caching for frequently asked questions
- Monitor and optimize Bedrock token usage
- Use CloudFront caching effectively

## 🔒 Security Checklist

- [ ] IAM roles follow least privilege principle
- [ ] S3 buckets are not publicly accessible
- [ ] API Gateway has rate limiting enabled
- [ ] CloudFront uses HTTPS only
- [ ] Lambda environment variables are encrypted
- [ ] Bedrock model access is restricted
- [ ] CloudWatch logging is enabled
- [ ] VPC endpoints configured (if using VPC)

## 📈 Performance Optimization

### Lambda Optimization
```bash
# Enable X-Ray tracing
aws lambda update-function-configuration \
  --function-name aws-docs-rag-api \
  --tracing-config Mode=Active

# Set reserved concurrency
aws lambda put-reserved-concurrency \
  --function-name aws-docs-rag-api \
  --reserved-concurrent-executions 10
```

### API Gateway Optimization
```bash
# Enable caching
aws apigateway put-method \
  --rest-api-id $API_ID \
  --resource-id $EXAMPLES_RESOURCE_ID \
  --http-method GET \
  --caching-enabled \
  --cache-ttl 3600
```

## 🎯 Next Steps

1. **Add More Documentation**: Expand the knowledge base with additional AWS services
2. **Implement Caching**: Add Redis or ElastiCache for frequently asked questions
3. **Add Authentication**: Integrate with Amazon Cognito for user management
4. **Enhance UI**: Add more interactive features and visualizations
5. **Multi-language Support**: Add support for multiple languages
6. **Advanced Analytics**: Implement detailed usage analytics and insights

---

**Deployment Complete! 🎉**

Your AWS Documentation Assistant RAG system should now be fully functional. Visit your CloudFront URL or custom domain to start using the system.

For support and questions, please refer to the [GitHub Issues](https://github.com/vibhup/s3vectors-usage-demo-awsdocumentationassistant/issues) page.
