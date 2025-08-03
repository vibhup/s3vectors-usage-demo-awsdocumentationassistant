# What is Amazon SNS?

Amazon Simple Notification Service (Amazon SNS) is a fully managed service that provides message delivery from
publishers (producers) to subscribers (consumers). Publishers communicate asynchronously
with subscribers by sending messages to a *topic*, which is
a logical access point and communication channel.

## How it works

In SNS, publishers send messages to a topic, which acts as a communication channel.
The topic acts as a logical access point, ensuring messages are delivered to multiple
subscribers across different platforms.

Subscribers to an SNS topic can receive messages through different endpoints,
depending on their use case, such as:

* Amazon SQS
* Lambda
* HTTP(S) endpoints
* Email
* Mobile push notifications
* Mobile text messages (SMS)
* Amazon Data Firehose
* Service providers (For example, Datadog, MongoDB, Splunk)

SNS supports both Application-to-Application (A2A) and Application-to-Person (A2P)
messaging, giving flexibility to send messages between different applications or
directly to mobile phones, email addresses, and more.

## Accessing Amazon SNS

You can access and manage Amazon SNS through the console, AWS CLI, or AWS SDKs, depending
on your preferred method of interaction. The console offers a graphical interface for
basic tasks, while the AWS CLI and SDKs provide advanced configuration and automation
capabilities for more complex use cases.

* The Amazon SNS console
  provides a convenient user interface for creating topics and subscriptions,
  sending and receiving messages, and monitoring events and logs.
* The AWS Command Line Interface (AWS CLI) gives you direct access to the Amazon SNS API for advanced
  configuration and automation use cases.
* AWS provides SDKs in various languages.

## Common Amazon SNS scenarios

Use these common Amazon SNS scenarios to implement scalable, event-driven architectures and
ensure reliable, real-time communication between applications and users.

### Application integration

The *Fanout* scenario is when a message published
to an SNS topic is replicated and pushed to multiple endpoints, such as Firehose
delivery streams, Amazon SQS queues, HTTP(S) endpoints, and Lambda functions. This allows
for parallel asynchronous processing.

For example, you can develop an application that publishes a message to an SNS
topic whenever an order is placed for a product. Then, SQS queues that are
subscribed to the SNS topic receive identical notifications for the new order. An
Amazon Elastic Compute Cloud (Amazon EC2) server instance attached to one of the SQS queues can handle the
processing or fulfillment of the order. And you can attach another Amazon EC2 server
instance to a data warehouse for analysis of all orders received.

You can also use fanout to replicate data sent to your production environment with
your test environment. Expanding upon the previous example, you can subscribe
another SQS queue to the same SNS topic for new incoming orders. Then, by attaching
this new SQS queue to your test environment, you can continue to improve and test
your application using data received from your production environment.

**Important**

Make sure that you consider data privacy and security before you send any
production data to your test environment.

### Application alerts

Application and system alerts are notifications that are triggered by predefined
thresholds. Amazon SNS can send these notifications to specified users via SMS and email.
For example, you can receive immediate notification when an event occurs, such as a
specific change to your Amazon EC2 Auto Scaling group, a new file uploaded to an Amazon S3 bucket, or a
metric threshold breached in Amazon CloudWatch.

### User notifications

Amazon SNS can send push email messages and text messages (SMS messages) to individuals
or groups. For example, you could send e-commerce order confirmations as user
notifications.

### Mobile push notifications

Mobile push notifications enable you to send messages directly to mobile apps. For
example, you can use Amazon SNS to send update notifications to an app. The notification
message can include a link to download and install the update.

## Pricing for Amazon SNS

Amazon SNS has no upfront costs. You pay based on the number of messages that you publish,
the number of notifications that you deliver, and any additional API calls for managing
topics and subscriptions. Delivery pricing varies by endpoint type. You can get started
for free with the Amazon SNS free tier.

## Key SNS Concepts

### Topics
Topics are communication channels that act as access points for publishers and subscribers. Publishers send messages to topics, and all subscribers to that topic receive the message.

### Subscriptions
Subscriptions define the endpoints that receive messages published to a topic. Each subscription specifies a protocol (like email, SMS, or SQS) and an endpoint address.

### Publishers
Publishers are applications or services that send messages to SNS topics. Publishers don't need to know about subscribers - they simply publish to the topic.

### Subscribers
Subscribers are endpoints that receive messages from topics they're subscribed to. Subscribers can be AWS services, applications, or individuals.

## Message Delivery Features

### Message Filtering
SNS supports message filtering, allowing subscribers to receive only the messages they're interested in based on message attributes.

### Message Attributes
You can include structured metadata with your messages using message attributes, which can be used for filtering and routing.

### Dead Letter Queues
Configure dead letter queues to capture messages that couldn't be delivered to subscribers after multiple retry attempts.

### Message Ordering
SNS FIFO topics provide message ordering and exactly-once delivery for applications that require these guarantees.

## Security Features

### Encryption
- Encryption in transit using HTTPS
- Encryption at rest using AWS KMS
- Server-side encryption for stored messages

### Access Control
- IAM policies for fine-grained access control
- Topic policies for resource-based permissions
- VPC endpoints for private connectivity

### Compliance
- HIPAA eligible service
- SOC, PCI DSS, and ISO compliance
- AWS CloudTrail integration for audit logging

## Integration Patterns

### Event-Driven Architecture
Use SNS as the central nervous system for event-driven applications, decoupling components and enabling scalable, resilient architectures.

### Microservices Communication
Enable loose coupling between microservices by using SNS topics for asynchronous communication.

### Workflow Orchestration
Trigger workflows and business processes by publishing events to SNS topics that multiple services can react to.

### Monitoring and Alerting
Integrate with CloudWatch to send alerts and notifications when metrics exceed thresholds or when system events occur.

## Best Practices

### Topic Design
- Use descriptive topic names that reflect their purpose
- Organize topics by business domain or application boundary
- Consider using FIFO topics when message ordering is important

### Subscription Management
- Regularly review and clean up unused subscriptions
- Use subscription filters to reduce unnecessary message delivery
- Implement proper error handling in subscriber applications

### Security
- Use least privilege access principles
- Enable encryption for sensitive data
- Monitor topic access and usage patterns
- Use VPC endpoints for internal communications

### Cost Optimization
- Use message filtering to reduce unnecessary deliveries
- Monitor usage patterns and optimize subscription strategies
- Consider batching messages when appropriate
- Use appropriate retry policies to avoid excessive charges
