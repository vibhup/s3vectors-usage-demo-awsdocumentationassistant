# What is Amazon Elastic Container Service?

Amazon Elastic Container Service (Amazon ECS) is a fully managed container orchestration service that helps you easily
deploy, manage, and scale containerized applications. As a fully managed service, Amazon ECS
comes with AWS configuration and operational best practices built-in. It's integrated with
both AWS tools, such as Amazon Elastic Container Registry, and third-party tools, such as Docker. This integration
makes it easier for teams to focus on building the applications, not the environment. You
can run and scale your container workloads across AWS Regions in the cloud, and
on-premises, without the complexity of managing a control plane.

## Terminology and components

There are three layers in Amazon ECS:

* **Capacity** - The infrastructure where your containers run
* **Controller** - Deploy and manage your applications that run on the
  containers
* **Provisioning** - The tools that you can use to interface with the scheduler to
  deploy and manage your applications and containers

The capacity is the infrastructure where your containers run. The following is an
overview of the capacity options:

* **Amazon EC2 instances in the AWS cloud**

  You choose the instance type, the number of instances, and manage the
  capacity.
* **Serverless (AWS Fargate) in the AWS cloud**

  Fargate is a serverless, pay-as-you-go compute engine. With Fargate you
  don't need to manage servers, handle capacity planning, or isolate container
  workloads for security.
* **On-premises virtual machines (VM) or servers**

  Amazon ECS Anywhere provides support for registering an external instance such as
  an on-premises server or virtual machine (VM), to your Amazon ECS cluster.

The Amazon ECS scheduler is the software that manages your applications.

## Features

Amazon ECS provides the following high-level features:

**Task definition**
:   The blueprint for the application.

**Cluster**
:   The infrastructure your application runs on.

**Task**
:   An application such as a batch job that performs work, and then
    stops.

**Service**
:   A long running stateless application.

**Account Setting**
:   Allows access to features.

**Cluster Auto Scaling**
:   Amazon ECS manages the scaling of Amazon EC2 instances that are registered to your
    cluster.

**Service Auto Scaling**
:   Amazon ECS increases or decreases the desired number of tasks in your service
    automatically.

## Provisioning

There are multiple options for provisioning Amazon ECS:

* **AWS Management Console** — Provides a web interface
  that you can use to access your Amazon ECS resources.
* **AWS Command Line Interface (AWS CLI)** — Provides commands
  for a broad set of AWS services, including Amazon ECS. It's supported on Windows,
  Mac, and Linux.
* **AWS SDKs** — Provides
  language-specific APIs and takes care of many of the connection details. These
  include calculating signatures, handling request retries, and error handling.
* **AWS CDK** — Provides an open-source
  software development framework that you can use to model and provision your
  cloud application resources using familiar programming languages. The AWS CDK
  provisions your resources in a safe, repeatable manner through
  AWS CloudFormation.

## Pricing

Amazon ECS pricing depends on the capacity option you choose for your containers.

* Amazon ECS pricing –
  Pricing information for Amazon ECS.
* AWS Fargate pricing
  – Pricing information for Fargate.

## Related services

### Services to use with Amazon ECS

You can use other AWS services to help you deploy yours tasks and services on
Amazon ECS.

**Amazon EC2 Auto Scaling**
:   Helps ensure you have the correct number of Amazon EC2 instances available to
    handle the load for your application.

**Amazon CloudWatch**
:   Monitor your services and tasks.

**Amazon Elastic Container Registry**
:   Store and manage container images.

**Elastic Load Balancing**
:   Automatically distribute incoming service traffic.

**Amazon GuardDuty**
:   Detect potentially unauthorized or malicious use of your container
    instances and workloads.

## Core Concepts

### Clusters
A cluster is a logical grouping of tasks or services. You can register one or more Amazon EC2 instances (also referred to as container instances) with your cluster to run tasks on them.

### Task Definitions
A task definition is a blueprint that describes how a Docker container should run. It includes details such as which Docker image to use, how much CPU and memory to use, networking mode, and logging configuration.

### Tasks
A task is the instantiation of a task definition within a cluster. After you create a task definition for your application, you can specify the number of tasks to run on your cluster.

### Services
A service allows you to run and maintain a specified number of instances of a task definition simultaneously in an Amazon ECS cluster. If any of your tasks should fail or stop for any reason, the Amazon ECS service scheduler launches another instance of your task definition to replace it.

## Launch Types

### EC2 Launch Type
With the EC2 launch type, you can run your containerized applications on a cluster of Amazon EC2 instances that you manage. This launch type is well-suited for large workloads that need to be optimized for price.

**Key Features:**
- Full control over the infrastructure
- Ability to use Spot instances for cost optimization
- Support for GPU instances
- Custom AMIs and instance configurations

### Fargate Launch Type
AWS Fargate is a serverless compute engine for containers that works with Amazon ECS. Fargate makes it easy to focus on building your applications without managing servers.

**Key Features:**
- No infrastructure management required
- Pay only for the resources your containers use
- Automatic scaling and patching
- Built-in security isolation

### ECS Anywhere
Amazon ECS Anywhere provides the ability to run and manage container workloads on your on-premises infrastructure using the same APIs and cluster management capabilities of Amazon ECS.

**Key Features:**
- Hybrid cloud deployments
- Consistent management experience
- Support for on-premises and edge locations
- Integration with AWS services

## Networking

### VPC Integration
Amazon ECS is deeply integrated with Amazon VPC, providing network isolation for your containers. You can specify VPC subnets and security groups for your tasks.

### Service Discovery
Amazon ECS integrates with AWS Cloud Map to provide service discovery for your containerized services. This allows services to discover and connect to each other without hard-coding IP addresses.

### Load Balancing
Amazon ECS integrates with Elastic Load Balancing to distribute traffic across your containers. You can use Application Load Balancers, Network Load Balancers, or Classic Load Balancers.

## Security Features

### IAM Integration
Amazon ECS is integrated with AWS Identity and Access Management (IAM) so you can assign granular permissions for each of your containers and use IAM to restrict access to each service and the resources it accesses.

### Task Roles
You can specify an IAM role for each task in your task definition. This allows the containers in that task to access only the AWS resources that you specify.

### Secrets Management
Amazon ECS integrates with AWS Secrets Manager and AWS Systems Manager Parameter Store to securely inject sensitive data into your containers.

### Container Image Scanning
Integration with Amazon ECR provides vulnerability scanning for your container images, helping you identify and remediate security issues.

## Monitoring and Logging

### CloudWatch Integration
Amazon ECS automatically sends metrics to Amazon CloudWatch for monitoring cluster and service performance. You can create alarms and dashboards to track the health of your applications.

### Container Insights
Container Insights provides monitoring and troubleshooting capabilities for containerized applications and microservices. It collects, aggregates, and summarizes metrics and logs.

### AWS X-Ray Integration
Amazon ECS integrates with AWS X-Ray to provide distributed tracing capabilities, helping you analyze and debug distributed applications.

## Best Practices

### Task Definition Design
- Use specific image tags instead of 'latest'
- Set appropriate CPU and memory limits
- Use health checks to ensure container health
- Implement proper logging configuration

### Service Configuration
- Use multiple Availability Zones for high availability
- Configure appropriate auto scaling policies
- Implement circuit breakers and retry logic
- Use blue/green deployments for zero-downtime updates

### Security Best Practices
- Use least privilege IAM policies
- Scan container images for vulnerabilities
- Use secrets management for sensitive data
- Enable logging and monitoring

### Cost Optimization
- Use Spot instances for fault-tolerant workloads
- Right-size your containers
- Use Fargate for variable workloads
- Monitor and optimize resource utilization

## Common Use Cases

### Microservices Architecture
Deploy and manage microservices with independent scaling, deployment, and monitoring capabilities.

### Batch Processing
Run batch jobs that can scale up and down based on workload requirements.

### Web Applications
Host scalable web applications with automatic load balancing and health monitoring.

### Machine Learning Workloads
Deploy ML models and training jobs with GPU support and auto scaling.

### CI/CD Pipelines
Use ECS as part of continuous integration and deployment pipelines for containerized applications.

## Integration Patterns

### ECS with ALB
Use Application Load Balancers to distribute traffic across multiple containers and enable advanced routing capabilities.

### ECS with RDS
Connect containerized applications to managed databases with proper security and networking configurations.

### ECS with S3
Store and retrieve data from S3 buckets using IAM roles for secure access.

### ECS with Lambda
Combine containers and serverless functions for hybrid architectures that optimize for both performance and cost.
