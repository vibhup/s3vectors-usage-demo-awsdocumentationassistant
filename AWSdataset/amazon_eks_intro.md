# What is Amazon EKS?

## Amazon EKS: Simplified Kubernetes Management

Amazon Elastic Kubernetes Service (EKS) provides a fully managed Kubernetes service that eliminates the complexity of operating Kubernetes clusters. With EKS, you can:

* Deploy applications faster with less operational overhead
* Scale seamlessly to meet changing workload demands
* Improve security through AWS integration and automated updates
* Choose between standard EKS or fully automated EKS Auto Mode

Amazon Elastic Kubernetes Service (Amazon EKS) is the premiere platform for running Kubernetes clusters, both in the Amazon Web Services (AWS) cloud and in your own data centers (EKS Anywhere and Amazon EKS Hybrid Nodes).

Amazon EKS simplifies building, securing, and maintaining Kubernetes clusters. It can be more cost effective at providing enough resources to meet peak demand than maintaining your own data centers. Two of the main approaches to using Amazon EKS are as follows:

* **EKS standard**: AWS manages the Kubernetes control plane when you create a cluster with EKS. Components that manage nodes, schedule workloads, integrate with the AWS cloud, and store and scale control plane information to keep your clusters up and running, are handled for you automatically.
* **EKS Auto Mode**: Using the EKS Auto Mode feature, EKS extends its control to manage Nodes (Kubernetes data plane) as well.
  It simplifies Kubernetes management by automatically provisioning infrastructure, selecting optimal compute instances, dynamically scaling resources, continuously optimizing costs, patching operating systems, and integrating with AWS security services.

Amazon EKS helps you accelerate time to production, improve performance, availability and resiliency, and enhance system security.

## Features of Amazon EKS

Amazon EKS provides the following high-level features:

**Management interfaces**
:   EKS offers multiple interfaces to provision, manage, and maintain clusters, including AWS Management Console, Amazon EKS API/SDKs, CDK, AWS CLI, eksctl CLI, AWS CloudFormation, and Terraform.

**Access control tools**
:   EKS relies on both Kubernetes and AWS Identity and Access Management (AWS IAM) features to manage access
    from users and workloads.

**Compute resources**
:   For compute resources, EKS allows the full range of Amazon EC2 instance types and AWS innovations such as Nitro and Graviton with Amazon EKS for you to optimize the compute for your workloads.

**Storage**
:   EKS Auto Mode automatically creates storage classes using EBS volumes.
    Using Container Storage Interface (CSI) drivers, you can also use Amazon S3, Amazon EFS, Amazon FSX, and Amazon File Cache for your application storage needs.

**Security**
:   The shared responsibility model is employed as it relates to Security in Amazon EKS.

**Monitoring tools**
:   Use the observability dashboard to monitor Amazon EKS clusters.
    Monitoring tools include Prometheus, CloudWatch, Cloudtrail,
    and ADOT Operator.

**Kubernetes compatibility and support**
:   Amazon EKS is certified Kubernetes-conformant, so you can deploy Kubernetes-compatible applications without refactoring and use Kubernetes community tooling and plugins.
    EKS offers both standard support and extended support for Kubernetes.

## Related services

### Services to use with Amazon EKS

You can use other AWS services with the clusters that you deploy using Amazon EKS:

**Amazon EC2**
:   Obtain on-demand, scalable compute capacity with Amazon EC2.

**Amazon EBS**
:   Attach scalable, high-performance block storage resources with Amazon EBS.

**Amazon ECR**
:   Store container images securely with Amazon ECR.

**Amazon CloudWatch**
:   Monitor AWS resources and applications in real time with Amazon CloudWatch.

**Amazon Prometheus**
:   Track metrics for containerized applications with Amazon Managed Service for Prometheus.

**Elastic Load Balancing**
:   Distribute incoming traffic across multiple targets with Elastic Load Balancing.

**Amazon GuardDuty**
:   Detect threats to EKS clusters with Amazon GuardDuty.

**AWS Resilience Hub**
:   Assess EKS cluster resiliency with AWS Resilience Hub.

## Amazon EKS Pricing

Amazon EKS has per cluster pricing based on Kubernetes cluster version support, pricing for Amazon EKS Auto Mode, and per vCPU pricing for Amazon EKS Hybrid Nodes.

When using Amazon EKS, you pay separately for the AWS resources you use to run your applications on Kubernetes worker nodes. For example, if you are running Kubernetes worker nodes as Amazon EC2 instances with Amazon EBS volumes and public IPv4 addresses, you are charged for the instance capacity through Amazon EC2, the volume capacity through Amazon EBS, and the IPv4 address through Amazon VPC.

Visit the respective pricing pages of the AWS services you are using with your Kubernetes applications for detailed pricing information.

## Key EKS Concepts

### Control Plane
The Kubernetes control plane manages the Kubernetes API server, etcd, and other control plane components. Amazon EKS runs the control plane across multiple AWS Availability Zones to ensure high availability.

### Worker Nodes
Worker nodes are EC2 instances that run your containerized applications. You can use managed node groups, self-managed nodes, or AWS Fargate for serverless containers.

### Node Groups
A node group is a group of EC2 instances that serve as worker nodes for your EKS cluster. Amazon EKS managed node groups automate the provisioning and lifecycle management of nodes.

### Pods
Pods are the smallest deployable units in Kubernetes. A pod represents a single instance of a running process in your cluster and can contain one or more containers.

### Services
Kubernetes services provide stable network endpoints for accessing pods. Services enable load balancing and service discovery within your cluster.

## EKS Deployment Options

### Managed Node Groups
Amazon EKS managed node groups automate the provisioning and lifecycle management of nodes (Amazon EC2 instances) for Amazon EKS clusters.

**Benefits:**
- Automated node provisioning and management
- Built-in support for Kubernetes cluster autoscaler
- Automatic security updates and patching
- Integration with AWS services

### Self-Managed Nodes
You can also create and manage your own worker nodes using EC2 instances that you configure and manage yourself.

**Use Cases:**
- Custom AMIs or specialized configurations
- Specific instance types not available in managed node groups
- Advanced networking requirements
- Cost optimization strategies

### AWS Fargate
AWS Fargate provides serverless compute for containers, allowing you to run pods without managing EC2 instances.

**Benefits:**
- No infrastructure management
- Pay only for pod resources
- Automatic scaling
- Built-in security isolation

## Networking in EKS

### VPC Integration
EKS clusters run within your Amazon VPC, providing network isolation and security. You can configure subnets, security groups, and network ACLs to control traffic.

### CNI Plugin
Amazon EKS uses the Amazon VPC CNI plugin to provide native VPC networking for Kubernetes pods. Each pod receives an IP address from your VPC.

### Load Balancing
EKS integrates with AWS Load Balancer Controller to provision Application Load Balancers and Network Load Balancers for your services.

### Ingress Controllers
You can use various ingress controllers like AWS Load Balancer Controller, NGINX Ingress Controller, or Istio Gateway to manage external access to your services.

## Security Features

### IAM Integration
EKS integrates with AWS IAM to provide authentication and authorization for both cluster access and pod-level permissions.

### RBAC
Kubernetes Role-Based Access Control (RBAC) provides fine-grained permissions for cluster resources.

### Pod Security Standards
EKS supports Kubernetes Pod Security Standards to enforce security policies for pods.

### Network Policies
Use Kubernetes Network Policies to control traffic between pods and external endpoints.

### Secrets Management
Integrate with AWS Secrets Manager and AWS Systems Manager Parameter Store to securely manage sensitive data.

## Monitoring and Observability

### CloudWatch Container Insights
Provides monitoring and troubleshooting capabilities for containerized applications running on EKS.

### Prometheus Integration
Amazon Managed Service for Prometheus provides a fully managed Prometheus-compatible monitoring service.

### Logging
EKS integrates with CloudWatch Logs, Fluent Bit, and other logging solutions to collect and analyze cluster and application logs.

### Distributed Tracing
Use AWS X-Ray or other tracing solutions to analyze and debug distributed applications.

## Best Practices

### Cluster Design
- Use multiple Availability Zones for high availability
- Implement proper resource quotas and limits
- Use namespaces to organize resources
- Plan for cluster upgrades and maintenance

### Security
- Enable audit logging
- Use least privilege IAM policies
- Implement network segmentation
- Regularly update cluster and node versions

### Performance
- Right-size your nodes and pods
- Use horizontal pod autoscaling
- Implement cluster autoscaling
- Monitor resource utilization

### Cost Optimization
- Use Spot instances for fault-tolerant workloads
- Implement resource requests and limits
- Use Fargate for variable workloads
- Monitor and optimize resource usage

## Common Use Cases

### Microservices Architecture
Deploy and manage microservices with Kubernetes-native service discovery, load balancing, and scaling capabilities.

### Machine Learning Workloads
Run ML training and inference workloads with support for GPUs and specialized instance types.

### Batch Processing
Execute batch jobs using Kubernetes Jobs and CronJobs with automatic scaling and resource management.

### CI/CD Pipelines
Integrate EKS with CI/CD tools for automated application deployment and testing.

### Hybrid and Multi-Cloud
Use EKS Anywhere to run Kubernetes clusters on-premises or in other cloud environments with consistent management.

## Migration Strategies

### Lift and Shift
Migrate existing containerized applications to EKS with minimal changes.

### Modernization
Refactor applications to take advantage of Kubernetes-native features and AWS services.

### Gradual Migration
Migrate applications incrementally using blue-green or canary deployment strategies.

### Hybrid Approach
Run some workloads on EKS while maintaining others on existing infrastructure during transition periods.
