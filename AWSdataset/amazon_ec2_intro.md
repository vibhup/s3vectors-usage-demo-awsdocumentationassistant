# What is Amazon EC2?

Amazon Elastic Compute Cloud (Amazon EC2) provides on-demand, scalable computing capacity in the Amazon Web
Services (AWS) Cloud. Using Amazon EC2 reduces hardware costs so you can develop and deploy
applications faster. You can use Amazon EC2 to launch as many or as few virtual servers as you
need, configure security and networking, and manage storage. You can add capacity (scale up)
to handle compute-heavy tasks, such as monthly or yearly processes, or spikes in website
traffic. When usage decreases, you can reduce capacity (scale down) again.

An EC2 instance is a virtual server in the AWS Cloud. When you launch an EC2 instance,
the instance type that you specify determines the hardware available to your instance.
Each instance type offers a different balance of compute, memory, network, and storage
resources.

## Features of Amazon EC2

Amazon EC2 provides the following high-level features:

**Instances**
:   Virtual servers.

**Amazon Machine Images (AMIs)**
:   Preconfigured templates for your instances that package the components you
    need for your server (including the operating system and additional
    software).

**Instance types**
:   Various configurations of CPU, memory, storage, networking capacity, and
    graphics hardware for your instances.

**Amazon EBS volumes**
:   Persistent storage volumes for your data using Amazon Elastic Block Store (Amazon EBS).

**Instance store volumes**
:   Storage volumes for temporary data that is deleted when you stop,
    hibernate, or terminate your instance.

**Key pairs**
:   Secure login information for your instances. AWS stores the public key
    and you store the private key in a secure place.

**Security groups**
:   A virtual firewall that allows you to specify the protocols, ports, and
    source IP ranges that can reach your instances, and the destination IP
    ranges to which your instances can connect.

Amazon EC2 supports the processing, storage, and transmission
of credit card data by a merchant or service provider, and has been
validated as being compliant with Payment Card Industry (PCI) Data Security Standard (DSS).

## Related services

### Services to use with Amazon EC2

You can use other AWS services with the instances that you deploy using Amazon EC2.

**Amazon EC2 Auto Scaling**
:   Helps ensure you have the correct number of Amazon EC2 instances available to
    handle the load for your application.

**AWS Backup**
:   Automate backing up your Amazon EC2 instances and the Amazon EBS volumes attached to
    them.

**Amazon CloudWatch**
:   Monitor your instances and Amazon EBS volumes.

**Elastic Load Balancing**
:   Automatically distribute incoming application traffic across multiple
    instances.

**Amazon GuardDuty**
:   Detect potentially unauthorized or malicious use of your EC2 instances.

**EC2 Image Builder**
:   Automate the creation, management, and deployment of customized, secure, and
    up-to-date server images.

**AWS Launch Wizard**
:   Size, configure, and deploy AWS resources for third-party applications
    without having to manually identify and provision individual AWS
    resources.

**AWS Systems Manager**
:   Perform operations at scale on EC2 instances with this secure end-to-end
    management solution.

### Additional compute services

You can launch instances using another AWS compute service instead of using Amazon EC2.

**Amazon Lightsail**
:   Build websites or web applications using Amazon Lightsail, a cloud platform
    that provides the resources that you need to deploy your project quickly, for
    a low, predictable monthly price.

**Amazon Elastic Container Service (Amazon ECS)**
:   Deploy, manage, and scale containerized applications on a cluster of EC2
    instances.

**Amazon Elastic Kubernetes Service (Amazon EKS)**
:   Run your Kubernetes applications on AWS.

## Access Amazon EC2

You can create and manage your Amazon EC2 instances using the following interfaces:

**Amazon EC2 console**
:   A simple web interface to create and manage Amazon EC2 instances and resources.
    If you've signed up for an AWS account, you can access the Amazon EC2 console
    by signing into the AWS Management Console and selecting **EC2** from
    the console home page.

**AWS Command Line Interface**
:   Enables you to interact with AWS services using commands in your command-line shell. It
    is supported on Windows, Mac, and Linux.

**AWS CloudFormation**
:   Amazon EC2 supports creating resources using AWS CloudFormation. You create a template, in JSON or YAML
    format, that describes your AWS resources, and AWS CloudFormation provisions and
    configures those resources for you.

**AWS SDKs**
:   If you prefer to build applications using language-specific APIs instead
    of submitting a request over HTTP or HTTPS, AWS provides libraries, sample
    code, tutorials, and other resources for software developers.

**AWS Tools for PowerShell**
:   A set of PowerShell modules that are built on the functionality exposed by
    the SDK for .NET. The Tools for PowerShell enable you to script operations on your AWS
    resources from the PowerShell command line.

**Query API**
:   Amazon EC2 provides a Query API. These requests are HTTP or HTTPS requests that
    use the HTTP verbs GET or POST and a Query parameter named
    `Action`.

## Pricing for Amazon EC2

Amazon EC2 provides the following pricing options:

**Free Tier**
:   You can get started with Amazon EC2 for free. To explore the Free Tier options,
    see AWS Free Tier.

**On-Demand Instances**
:   Pay for compute capacity by the hour or second with no long-term commitments.

**Reserved Instances**
:   Make a low, one-time payment and receive a significant discount on the hourly charge for that instance.

**Spot Instances**
:   Request unused EC2 instances, which can lower your Amazon EC2 costs significantly.

**Dedicated Hosts**
:   Pay for a physical host that is fully dedicated to running your instances, and bring your existing per-socket, per-core, or per-VM software licenses to reduce costs.

**Dedicated Instances**
:   Pay, by the hour, for instances that run on single-tenant hardware.

**Capacity Reservations**
:   Reserve capacity for your EC2 instances in a specific Availability Zone for any duration.
