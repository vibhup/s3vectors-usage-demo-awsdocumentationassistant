#!/bin/bash

# AWS Documentation Assistant - Complete Deployment Script
# This script deploys the entire S3 Vectors RAG system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REGION="us-east-1"
BUCKET_PREFIX="aws-docs-rag-ui"
VECTOR_BUCKET_PREFIX="aws-docs-vectors"
INDEX_NAME="aws-docs-index"
LAMBDA_FUNCTION_NAME="aws-docs-rag-api"
API_NAME="aws-docs-rag-api"

echo -e "${BLUE}🚀 AWS Documentation Assistant - S3 Vectors RAG Deployment${NC}"
echo "=================================================================="

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found. Please install AWS CLI first.${NC}"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.9+ first.${NC}"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found. Please install Node.js 18+ first.${NC}"
    exit 1
fi

# Check jq
if ! command -v jq &> /dev/null; then
    echo -e "${RED}❌ jq not found. Please install jq for JSON processing.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites met${NC}"

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo -e "${BLUE}📋 AWS Account ID: $ACCOUNT_ID${NC}"

# Generate unique names
TIMESTAMP=$(date +%s)
BUCKET_NAME="${BUCKET_PREFIX}-${TIMESTAMP}"
VECTOR_BUCKET_NAME="${VECTOR_BUCKET_PREFIX}-${TIMESTAMP}"

echo -e "${BLUE}📋 Generated resource names:${NC}"
echo "   S3 Bucket: $BUCKET_NAME"
echo "   Vector Bucket: $VECTOR_BUCKET_NAME"
echo "   Lambda Function: $LAMBDA_FUNCTION_NAME"

# Step 1: Create IAM Role
echo -e "${YELLOW}🔐 Step 1: Creating IAM role...${NC}"

# Create trust policy
cat > /tmp/lambda-trust-policy.json << EOF
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
  --assume-role-policy-document file:///tmp/lambda-trust-policy.json \
  --region $REGION || echo "Role may already exist"

# Create policy
cat > /tmp/lambda-rag-policy.json << EOF
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

# Attach policy
aws iam put-role-policy \
  --role-name lambda-rag-execution-role \
  --policy-name lambda-rag-policy \
  --policy-document file:///tmp/lambda-rag-policy.json

echo -e "${GREEN}✅ IAM role created successfully${NC}"

# Step 2: Create S3 Vectors Index and Insert Data
echo -e "${YELLOW}📊 Step 2: Setting up S3 Vectors and data...${NC}"

# Install Python dependencies
pip3 install boto3 numpy

# Set environment variables for data processing
export VECTOR_BUCKET_NAME=$VECTOR_BUCKET_NAME
export INDEX_NAME=$INDEX_NAME
export AWS_REGION=$REGION

# Process AWS documentation and create embeddings
echo "Processing AWS documentation..."
python3 backend/preprocess_aws_docs.py

echo "Creating S3 Vectors index and inserting embeddings..."
python3 backend/insert_embeddings_to_s3_vectors.py

echo -e "${GREEN}✅ S3 Vectors setup completed${NC}"

# Step 3: Deploy Lambda Function
echo -e "${YELLOW}⚡ Step 3: Deploying Lambda function...${NC}"

# Create deployment directory
mkdir -p /tmp/lambda-deployment
cd /tmp/lambda-deployment

# Copy Lambda files
cp ../backend/lambda_rag_handler.py .
cp ../backend/aws_docs_rag_system.py .

# Install dependencies
pip3 install boto3 -t .

# Create deployment package
zip -r lambda-rag-function.zip .

# Get IAM role ARN
ROLE_ARN=$(aws iam get-role --role-name lambda-rag-execution-role --query 'Role.Arn' --output text)

# Wait for role to be ready
echo "Waiting for IAM role to be ready..."
sleep 10

# Create Lambda function
aws lambda create-function \
  --function-name $LAMBDA_FUNCTION_NAME \
  --runtime python3.11 \
  --role $ROLE_ARN \
  --handler lambda_rag_handler.lambda_handler \
  --zip-file fileb://lambda-rag-function.zip \
  --timeout 60 \
  --memory-size 1024 \
  --environment Variables="{VECTOR_BUCKET_NAME=$VECTOR_BUCKET_NAME,INDEX_NAME=$INDEX_NAME,BEDROCK_REGION=$REGION,S3VECTORS_REGION=$REGION}" \
  --region $REGION

echo -e "${GREEN}✅ Lambda function deployed successfully${NC}"

# Step 4: Create API Gateway
echo -e "${YELLOW}🚪 Step 4: Creating API Gateway...${NC}"

# Create REST API
API_ID=$(aws apigateway create-rest-api \
  --name $API_NAME \
  --description "AWS Documentation RAG API" \
  --region $REGION \
  --query 'id' --output text)

echo "API ID: $API_ID"

# Get root resource ID
ROOT_RESOURCE_ID=$(aws apigateway get-resources \
  --rest-api-id $API_ID \
  --region $REGION \
  --query 'items[0].id' --output text)

# Create resources
ASK_RESOURCE_ID=$(aws apigateway create-resource \
  --rest-api-id $API_ID \
  --parent-id $ROOT_RESOURCE_ID \
  --path-part ask \
  --region $REGION \
  --query 'id' --output text)

EXAMPLES_RESOURCE_ID=$(aws apigateway create-resource \
  --rest-api-id $API_ID \
  --parent-id $ROOT_RESOURCE_ID \
  --path-part examples \
  --region $REGION \
  --query 'id' --output text)

HEALTH_RESOURCE_ID=$(aws apigateway create-resource \
  --rest-api-id $API_ID \
  --parent-id $ROOT_RESOURCE_ID \
  --path-part health \
  --region $REGION \
  --query 'id' --output text)

# Get Lambda function ARN
LAMBDA_ARN=$(aws lambda get-function \
  --function-name $LAMBDA_FUNCTION_NAME \
  --region $REGION \
  --query 'Configuration.FunctionArn' --output text)

# Create methods and integrations for each resource
for RESOURCE_ID in $ASK_RESOURCE_ID $EXAMPLES_RESOURCE_ID $HEALTH_RESOURCE_ID; do
  # Determine HTTP method based on resource
  if [ "$RESOURCE_ID" = "$ASK_RESOURCE_ID" ]; then
    HTTP_METHOD="POST"
  else
    HTTP_METHOD="GET"
  fi
  
  # Create method
  aws apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method $HTTP_METHOD \
    --authorization-type NONE \
    --region $REGION
  
  # Create integration
  aws apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method $HTTP_METHOD \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri "arn:aws:apigateway:$REGION:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations" \
    --region $REGION
  
  # Add Lambda permission
  aws lambda add-permission \
    --function-name $LAMBDA_FUNCTION_NAME \
    --statement-id "apigateway-$RESOURCE_ID-$HTTP_METHOD" \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:$REGION:$ACCOUNT_ID:$API_ID/*/$HTTP_METHOD/*" \
    --region $REGION
  
  # Enable CORS
  aws apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method OPTIONS \
    --authorization-type NONE \
    --region $REGION
  
  aws apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method OPTIONS \
    --type MOCK \
    --integration-http-method OPTIONS \
    --request-templates '{"application/json": "{\"statusCode\": 200}"}' \
    --region $REGION
  
  aws apigateway put-method-response \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method OPTIONS \
    --status-code 200 \
    --response-parameters '{"method.response.header.Access-Control-Allow-Headers": false, "method.response.header.Access-Control-Allow-Methods": false, "method.response.header.Access-Control-Allow-Origin": false}' \
    --region $REGION
  
  aws apigateway put-integration-response \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method OPTIONS \
    --status-code 200 \
    --response-parameters '{"method.response.header.Access-Control-Allow-Headers": "'\''Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'\''", "method.response.header.Access-Control-Allow-Methods": "'\''GET,POST,OPTIONS'\''", "method.response.header.Access-Control-Allow-Origin": "'\''*'\''"}' \
    --region $REGION
done

# Deploy API
aws apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name prod \
  --region $REGION

API_ENDPOINT="https://$API_ID.execute-api.$REGION.amazonaws.com/prod"
echo -e "${GREEN}✅ API Gateway created successfully${NC}"
echo -e "${BLUE}🔗 API Endpoint: $API_ENDPOINT${NC}"

# Step 5: Deploy Frontend
echo -e "${YELLOW}🎨 Step 5: Deploying frontend...${NC}"

# Create S3 bucket for frontend
aws s3 mb s3://$BUCKET_NAME --region $REGION

# Configure bucket for static website hosting
aws s3 website s3://$BUCKET_NAME \
  --index-document index.html \
  --error-document index.html

# Build React application
cd frontend

# Install dependencies
npm install

# Update API endpoint in the app
sed -i.bak "s|const API_BASE_URL = .*|const API_BASE_URL = '$API_ENDPOINT';|" src/App.js

# Build production version
npm run build

# Upload to S3
aws s3 sync build/ s3://$BUCKET_NAME/ --delete

echo -e "${GREEN}✅ Frontend uploaded to S3${NC}"

# Step 6: Create CloudFront Distribution
echo -e "${YELLOW}☁️ Step 6: Creating CloudFront distribution...${NC}"

# Create CloudFront Origin Access Identity
OAI_ID=$(aws cloudfront create-cloud-front-origin-access-identity \
  --cloud-front-origin-access-identity-config \
  CallerReference=$TIMESTAMP,Comment="OAI for AWS Docs RAG UI" \
  --query 'CloudFrontOriginAccessIdentity.Id' --output text)

# Update S3 bucket policy
cat > /tmp/s3-bucket-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudFrontAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity $OAI_ID"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::$BUCKET_NAME/*"
    }
  ]
}
EOF

aws s3api put-bucket-policy \
  --bucket $BUCKET_NAME \
  --policy file:///tmp/s3-bucket-policy.json

# Create CloudFront distribution
cat > /tmp/cloudfront-config.json << EOF
{
  "CallerReference": "$BUCKET_NAME-$TIMESTAMP",
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

DISTRIBUTION_ID=$(aws cloudfront create-distribution \
  --distribution-config file:///tmp/cloudfront-config.json \
  --query 'Distribution.Id' --output text)

CLOUDFRONT_DOMAIN=$(aws cloudfront get-distribution \
  --id $DISTRIBUTION_ID \
  --query 'Distribution.DomainName' --output text)

echo -e "${GREEN}✅ CloudFront distribution created successfully${NC}"
echo -e "${BLUE}🔗 CloudFront URL: https://$CLOUDFRONT_DOMAIN${NC}"

# Step 7: Test the deployment
echo -e "${YELLOW}🧪 Step 7: Testing deployment...${NC}"

echo "Waiting for API Gateway to be ready..."
sleep 10

# Test health endpoint
echo "Testing health endpoint..."
curl -s "$API_ENDPOINT/health" | jq .

# Test examples endpoint
echo "Testing examples endpoint..."
curl -s "$API_ENDPOINT/examples" | jq .

echo -e "${GREEN}✅ Backend tests completed${NC}"

# Step 8: Display deployment summary
echo -e "${BLUE}"
echo "=================================================================="
echo "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo "=================================================================="
echo -e "${NC}"

echo -e "${GREEN}📋 Deployment Summary:${NC}"
echo "   AWS Account: $ACCOUNT_ID"
echo "   Region: $REGION"
echo ""
echo -e "${GREEN}🔗 Access URLs:${NC}"
echo "   CloudFront: https://$CLOUDFRONT_DOMAIN"
echo "   API Gateway: $API_ENDPOINT"
echo "   S3 Website: http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com"
echo ""
echo -e "${GREEN}📊 Resources Created:${NC}"
echo "   S3 Bucket: $BUCKET_NAME"
echo "   Vector Bucket: $VECTOR_BUCKET_NAME"
echo "   Lambda Function: $LAMBDA_FUNCTION_NAME"
echo "   API Gateway: $API_ID"
echo "   CloudFront Distribution: $DISTRIBUTION_ID"
echo "   IAM Role: lambda-rag-execution-role"
echo ""
echo -e "${GREEN}⏱️ Note:${NC}"
echo "   CloudFront distribution may take 10-15 minutes to fully deploy."
echo "   You can check the status in the AWS Console."
echo ""
echo -e "${GREEN}🎯 Next Steps:${NC}"
echo "   1. Wait for CloudFront deployment to complete"
echo "   2. Visit the CloudFront URL to test the application"
echo "   3. (Optional) Set up custom domain with Route 53"
echo "   4. (Optional) Configure monitoring and alerts"
echo ""
echo -e "${BLUE}🎊 Your AWS Documentation Assistant is ready!${NC}"

# Cleanup temporary files
rm -f /tmp/lambda-trust-policy.json
rm -f /tmp/lambda-rag-policy.json
rm -f /tmp/s3-bucket-policy.json
rm -f /tmp/cloudfront-config.json
rm -rf /tmp/lambda-deployment

echo -e "${GREEN}✅ Cleanup completed${NC}"
