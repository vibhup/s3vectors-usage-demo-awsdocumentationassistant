# What is Amazon Simple Queue Service?

Amazon Simple Queue Service (Amazon SQS) offers a secure, durable, and available hosted queue that lets you
integrate and decouple distributed software systems and components. Amazon SQS offers common
constructs such as dead-letter queues and
cost allocation tags. It provides a generic web
services API that you can access using any programming language that the AWS SDK
supports.

## Benefits of using Amazon SQS

* **Security** – You control who can
  send messages to and receive messages from an Amazon SQS queue. You can choose to
  transmit sensitive data by protecting the contents of messages in queues by
  using default Amazon SQS managed server-side encryption (SSE), or by using custom
  SSE keys managed in
  AWS Key Management Service (AWS KMS).
* **Durability** – For the safety of your
  messages, Amazon SQS stores them on multiple servers. Standard queues support at-least-once message
  delivery, and FIFO queues support exactly-once message
  processing and high-throughput mode.
* **Availability** – Amazon SQS uses redundant infrastructure to provide
  highly-concurrent access to messages and high availability for producing and
  consuming messages.
* **Scalability** – Amazon SQS can process each
  buffered
  request independently, scaling transparently to handle any load
  increases or spikes without any provisioning instructions.
* **Reliability** – Amazon SQS locks your messages
  during processing, so that multiple producers can send and multiple consumers
  can receive messages at the same time.
* **Customization** – Your queues don't
  have to be exactly alike—for example, you can set a default delay on a queue. You can
  store the contents of messages larger than 256 KB using Amazon Simple Storage Service (Amazon S3) or Amazon DynamoDB, with
  Amazon SQS holding a pointer to the Amazon S3 object, or you can split a large message
  into smaller messages.

## Basic Amazon SQS architecture

This section describes the components of a distributed messaging system and explains the
lifecycle of an Amazon SQS message.

### Distributed queues

There are three main parts in a distributed messaging system: the **components of
your distributed system**, your **queue** (distributed on Amazon SQS servers), and the **messages
in the queue**.

In the following scenario, your system has several *producers* (components that send messages
to the queue) and *consumers* (components that receive messages from the queue). The queue (which
holds messages A through E) redundantly stores the messages across multiple Amazon SQS servers.

### Message lifecycle

The following scenario describes the lifecycle of an Amazon SQS message in a queue, from
creation to deletion.

1. A producer (Component 1) sends message A to a queue, and the
message is distributed across the Amazon SQS servers redundantly.

2. When a consumer (Component 2) is ready to process messages, it
consumes messages from the queue, and message A is returned. While message A is being
processed, it remains in the queue and isn't returned to subsequent receive requests for
the duration of the visibility
timeout.

3. The consumer (Component 2) deletes message A from the queue to
prevent the message from being received and processed again when the visibility timeout
expires.

**Note**

Amazon SQS automatically deletes messages that have been in a queue for more than the
maximum message retention period. The default message retention period is 4 days.
However, you can set the message retention period to a value from 60 seconds to
1,209,600 seconds (14 days) using the `SetQueueAttributes` action.

## Differences between Amazon SQS, Amazon MQ, and Amazon SNS

Amazon SQS, Amazon SNS, and Amazon MQ offer highly scalable and easy-to-use
managed messaging services, each designed for specific roles within distributed systems.
Here's an enhanced overview of the differences between these services:

**Amazon SQS** decouples and scales distributed software systems
and components as a queue service. It processes messages through a single subscriber
typically, ideal for workflows where order and loss prevention are critical. For wider
distribution, integrating Amazon SQS with Amazon SNS enables a fanout messaging pattern, effectively pushing messages to multiple
subscribers at once.

**Amazon SNS** allows publishers to send messages to multiple
subscribers through topics, which serve as communication channels. Subscribers receive
published messages using a supported endpoint type, such as Amazon Data Firehose, Amazon SQS,
Lambda, HTTP,
email, mobile push notifications, and mobile text messages (SMS). This service is ideal
for scenarios requiring immediate notifications, such as real-time user engagement or
alarm systems. To prevent message loss when subscribers are offline, integrating Amazon SNS
with Amazon SQS queue messages ensures consistent delivery.

**Amazon MQ** fits best with enterprises looking to migrate
from traditional message brokers, supporting standard messaging protocols like AMQP and
MQTT, along with Apache ActiveMQ and
RabbitMQ. It offers compatibility
with legacy systems needing stable, reliable messaging without significant
reconfiguration.

The following chart provides an overview of each services' resource type:

| Resource type | Amazon SNS | Amazon SQS | Amazon MQ |
| --- | --- | --- | --- |
| Synchronous | No | No | Yes |
| Asynchronous | Yes | Yes | Yes |
| Queues | No | Yes | Yes |
| Publisher-subscriber messaging | Yes | No | Yes |
| Message brokers | No | No | Yes |

Both Amazon SQS and Amazon SNS are recommended for new applications that can benefit from nearly
unlimited scalability and simple APIs. They generally offer more cost-effective
solutions for high-volume applications with their pay-as-you-go pricing. We recommend
Amazon MQ for migrating applications from existing message brokers that rely on
compatibility with APIs such as JMS or protocols such as Advanced Message Queuing
Protocol (AMQP), MQTT, OpenWire, and Simple Text Oriented Message Protocol
(STOMP).

## Queue Types

### Standard Queues
Standard queues provide maximum throughput, best-effort ordering, and at-least-once delivery. They support nearly unlimited number of transactions per second (TPS) per API action.

**Key Features:**
- Unlimited throughput
- At-least-once delivery
- Best-effort ordering
- Duplicate messages possible

**Use Cases:**
- Decouple live user requests from intensive background work
- Allocate tasks to multiple worker nodes
- Batch messages for future processing

### FIFO Queues
FIFO (First-In-First-Out) queues are designed to enhance messaging between applications when the order of operations and events is critical, or where duplicates can't be tolerated.

**Key Features:**
- Exactly-once processing
- First-in-first-out delivery
- Limited to 300 TPS (or 3,000 TPS with batching)
- Message deduplication

**Use Cases:**
- E-commerce order management
- Financial transaction processing
- User-generated content processing

## Key SQS Concepts

### Visibility Timeout
The visibility timeout is the period of time during which Amazon SQS prevents other consumers from receiving and processing a message that has already been received by another consumer.

### Message Retention Period
The message retention period is the amount of time that Amazon SQS retains a message if it doesn't get deleted. The default is 4 days, with a range from 60 seconds to 14 days.

### Dead Letter Queues
Dead letter queues are used to handle message processing failures. When a message can't be processed successfully after a specified number of attempts, it's moved to a dead letter queue.

### Long Polling
Long polling helps reduce the cost of using Amazon SQS by eliminating the number of empty responses and false empty responses.

### Short Polling
Short polling returns immediately, even if the message queue being polled is empty.

## Security Features

### Encryption
- Server-side encryption using AWS KMS
- Client-side encryption for additional security
- Encryption in transit using HTTPS

### Access Control
- IAM policies for fine-grained access control
- Queue policies for resource-based permissions
- VPC endpoints for private connectivity

### Monitoring and Logging
- CloudWatch metrics for queue monitoring
- CloudTrail logging for API calls
- Dead letter queue monitoring

## Best Practices

### Message Design
- Keep messages small (under 256 KB)
- Use message attributes for metadata
- Implement idempotent message processing
- Use appropriate message retention periods

### Queue Configuration
- Choose the right queue type for your use case
- Configure appropriate visibility timeouts
- Set up dead letter queues for error handling
- Use long polling to reduce costs

### Performance Optimization
- Use batching for higher throughput
- Implement exponential backoff for retries
- Monitor queue depth and processing times
- Scale consumers based on queue metrics

### Cost Management
- Use long polling to reduce API calls
- Delete processed messages promptly
- Monitor and optimize message retention
- Use appropriate instance types for consumers

## Integration Patterns

### Producer-Consumer Pattern
The basic pattern where producers send messages to a queue and consumers process them asynchronously.

### Work Queue Pattern
Distribute time-consuming tasks among multiple workers to achieve parallelism and load distribution.

### Request-Response Pattern
Implement synchronous-like communication using two queues - one for requests and another for responses.

### Priority Queue Pattern
Use multiple queues with different priorities to ensure critical messages are processed first.
