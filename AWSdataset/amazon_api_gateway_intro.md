# What is Amazon API Gateway?

Amazon API Gateway is an AWS service for creating, publishing, maintaining, monitoring, and
securing REST, HTTP, and WebSocket APIs at any scale. API developers can create APIs that
access AWS or other web services, as well as data stored in the AWS Cloud. As an API Gateway
API developer, you can create APIs for use in your own client applications. Or you can make
your APIs available to third-party app developers.

API Gateway creates RESTful APIs that:

* Are HTTP-based.
* Enable stateless client-server communication.
* Implement standard HTTP methods such as GET, POST, PUT, PATCH, and DELETE.

API Gateway creates WebSocket APIs that:

* Adhere to the WebSocket
  protocol, which enables stateful, full-duplex communication between client and
  server.
* Route incoming messages based on message content.

## Architecture of API Gateway

API Gateway architecture shows how the APIs you build in Amazon API Gateway provide you or your
developer customers with an integrated and consistent developer experience for building
AWS serverless applications. API Gateway handles all the tasks involved in accepting and
processing up to hundreds of thousands of concurrent API calls. These tasks include
traffic management, authorization and access control, monitoring, and API version
management.

API Gateway acts as a "front door" for applications to access data, business logic, or
functionality from your backend services, such as workloads running on Amazon Elastic Compute Cloud
(Amazon EC2), code running on AWS Lambda, any web application, or real-time communication
applications.

## Features of API Gateway

Amazon API Gateway offers features such as the following:

* Support for stateful (WebSocket) and stateless (HTTP and
  REST) APIs.
* Powerful, flexible authentication mechanisms, such as AWS Identity and Access Management policies, Lambda
  authorizer functions, and Amazon Cognito user pools.
* Canary release deployments for safely
  rolling out changes.
* CloudTrail logging and monitoring of API usage and
  API changes.
* CloudWatch access logging and execution logging, including the ability to set
  alarms.
* Ability to use AWS CloudFormation templates to enable API creation.
* Support for custom domain
  names.
* Integration with AWS WAF for protecting your APIs against common web exploits.
* Integration with AWS X-Ray for
  understanding and triaging performance latencies.

## Accessing API Gateway

You can access Amazon API Gateway in the following ways:

* **AWS Management Console** – The AWS Management Console provides a web interface for creating
  and managing APIs. After you complete the setup steps, you can access the API Gateway
  console.
* **AWS SDKs** – If you're using a
  programming language that AWS provides an SDK for, you can use an SDK to access
  API Gateway. SDKs simplify authentication, integrate easily with your development
  environment, and provide access to API Gateway commands.
* **API Gateway V1 and V2 APIs** – If you're using
  a programming language that an SDK isn't available for, see the Amazon API Gateway Version 1 API Reference
  and Amazon API Gateway Version 2 API Reference.
* **AWS Command Line Interface** – For more information, see
  Getting Set Up with the AWS Command Line Interface in the
  *AWS Command Line Interface User Guide*.
* **AWS Tools for Windows PowerShell** – For more information, see
  Setting Up the AWS Tools for Windows PowerShell in the
  *AWS Tools for PowerShell User Guide*.

## Part of AWS serverless infrastructure

Together with AWS Lambda, API Gateway forms the app-facing
part of the AWS serverless infrastructure. To learn more about getting started with serverless, see the
Serverless Developer Guide.

For an app to call publicly available AWS services, you can use Lambda to interact
with required services and expose Lambda functions through API methods in API Gateway.
AWS Lambda runs your code on a highly available computing infrastructure. It performs the
necessary execution and administration of computing resources. To enable serverless
applications, API Gateway supports streamlined
proxy integrations with AWS Lambda and HTTP endpoints.

## How to get started with Amazon API Gateway

For an introduction to Amazon API Gateway, see the following:

* Get started with API Gateway, which provides a walkthrough for creating an HTTP API.
* Serverless land, which provides instructional videos.
* Happy Little API
  Shorts, which is a series of brief instructional videos.

## API Gateway Use Cases

### Serverless Web Applications
Build serverless web applications by combining API Gateway with AWS Lambda. API Gateway handles HTTP requests and routes them to Lambda functions that contain your business logic.

### Mobile Backends
Create scalable mobile backends that can handle authentication, data storage, and push notifications. API Gateway can integrate with Amazon Cognito for user authentication and AWS Lambda for backend processing.

### Real-time Applications
Use WebSocket APIs to build real-time applications like chat applications, live dashboards, or collaborative tools that require bidirectional communication between clients and servers.

### Microservices Architecture
API Gateway serves as a single entry point for microservices, providing routing, authentication, rate limiting, and monitoring across multiple backend services.

### Legacy System Integration
Modernize legacy systems by exposing their functionality through modern REST APIs without changing the underlying systems.

## API Types Comparison

### REST APIs
- Full-featured APIs with extensive customization options
- Support for request/response transformations
- Built-in caching capabilities
- Comprehensive monitoring and logging
- Support for API keys and usage plans

### HTTP APIs
- Lower cost and higher performance than REST APIs
- Optimized for serverless workloads
- Built-in support for CORS
- Automatic deployments
- JWT authorizers

### WebSocket APIs
- Persistent connections for real-time communication
- Route selection based on message content
- Support for custom authorizers
- Integration with AWS Lambda and HTTP backends

## Security Features

### Authentication and Authorization
- AWS IAM integration for fine-grained access control
- Amazon Cognito user pools for user authentication
- Lambda authorizers for custom authentication logic
- API keys for simple access control

### Data Protection
- SSL/TLS encryption for data in transit
- Integration with AWS Certificate Manager for SSL certificates
- Request and response data validation
- Input sanitization and output encoding

### Monitoring and Compliance
- AWS CloudTrail integration for API call logging
- Amazon CloudWatch metrics and alarms
- AWS X-Ray tracing for performance analysis
- VPC endpoints for private API access

## Pricing Model

API Gateway pricing is based on:
- Number of API calls received
- Amount of data transferred out
- Optional features like caching and dedicated tenancy
- WebSocket connection minutes and messages

The service offers a free tier with 1 million API calls per month for the first 12 months.
