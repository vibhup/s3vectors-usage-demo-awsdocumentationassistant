# What is Amazon Kinesis Data Streams?

You can use Amazon Kinesis Data Streams to collect and process large streams of data records in real time. You
can create data-processing applications, known as *Kinesis Data Streams applications*. A
typical Kinesis Data Streams application reads data from a *data stream* as data
records. These applications can use the Kinesis Client Library, and they can run on Amazon EC2
instances. You can send the processed records to dashboards, use them to generate alerts,
dynamically change pricing and advertising strategies, or send data to a variety of other
AWS services.

Kinesis Data Streams is part of the Kinesis streaming data platform, along with Firehose, Kinesis Video Streams, and Managed Service for Apache Flink.

## What can I do with Kinesis Data Streams?

You can use Kinesis Data Streams for rapid and continuous data intake and aggregation. The type of
data used can include IT infrastructure log data, application logs, social media, market
data feeds, and web clickstream data. Because the response time for the data intake and
processing is in real time, the processing is typically lightweight.

The following are typical scenarios for using Kinesis Data Streams:

**Accelerated log and data feed intake and processing**
:   You can have producers push data directly into a stream. For example, push
    system and application logs and they are available for processing in
    seconds. This prevents the log data from being lost if the front end or
    application server fails. Kinesis Data Streams provides accelerated data feed intake
    because you don't batch the data on the servers before you submit it for
    intake.

**Real-time metrics and reporting**
:   You can use data collected into Kinesis Data Streams for simple data analysis and
    reporting in real time. For example, your data-processing application can
    work on metrics and reporting for system and application logs as the data is
    streaming in, rather than wait to receive batches of data.

**Real-time data analytics**
:   This combines the power of parallel processing with the value of real-time
    data. For example, process website clickstreams in real time, and then
    analyze site usability engagement using multiple different Kinesis Data Streams
    applications running in parallel.

**Complex stream processing**
:   You can create Directed Acyclic Graphs (DAGs) of Kinesis Data Streams applications and
    data streams. This typically involves putting data from multiple Kinesis Data Streams
    applications into another stream for downstream processing by a different
    Kinesis Data Streams application.

## Benefits of using Kinesis Data Streams

Although you can use Kinesis Data Streams to solve a variety of streaming data problems, a common use
is the real-time aggregation of data followed by loading the aggregate data into a data
warehouse or map-reduce cluster.

Data is put into Kinesis data streams, which ensures durability and elasticity. The delay
between the time a record is put into the stream and the time it can be retrieved
(put-to-get delay) is typically less than 1 second. In other words, a Kinesis Data Streams application
can start consuming the data from the stream almost immediately after the data is added.
The managed service aspect of Kinesis Data Streams relieves you of the operational burden of creating
and running a data intake pipeline. You can create streaming map-reduce–type
applications. The elasticity of Kinesis Data Streams enables you to scale the stream up or down, so
that you never lose data records before they expire.

Multiple Kinesis Data Streams applications can consume data from a stream, so that multiple actions,
like archiving and processing, can take place concurrently and independently. For
example, two applications can read data from the same stream. The first application
calculates running aggregates and updates an Amazon DynamoDB table, and the second application
compresses and archives data to a data store like Amazon Simple Storage Service (Amazon S3). The DynamoDB table with
running aggregates is then read by a dashboard for up-to-the-minute reports.

The Kinesis Client Library enables fault-tolerant consumption of data from streams and
provides scaling support for Kinesis Data Streams applications.

## Related services

For information about using Amazon EMR clusters to read and process Kinesis data streams
directly, see Kinesis
Connector.

## Key Concepts

### Data Streams
A data stream is a set of shards. Each shard has a sequence of data records. Each data record has a sequence number that is assigned by Kinesis Data Streams.

### Shards
A shard is a uniquely identified sequence of data records in a stream. A stream is composed of one or more shards, each of which provides a fixed unit of capacity.

### Data Records
A data record is the unit of data stored in a Kinesis data stream. Data records are composed of a sequence number, a partition key, and a data blob.

### Partition Key
A partition key is used to group data by shard within a stream. Kinesis Data Streams segregates the data records belonging to a stream into multiple shards, using the partition key associated with each data record to determine the shard to which a given data record belongs.

### Sequence Number
Each data record has a sequence number that is unique per partition-key within its shard. Kinesis Data Streams assigns this sequence number after you write to the stream with client.putRecords or client.putRecord.

## Kinesis Data Streams Architecture

### Producers
Producers put records into Amazon Kinesis Data Streams. For example, a web server sending log data to a stream is a producer.

### Consumers
Consumers get records from Amazon Kinesis Data Streams and process them. These consumers are also known as Amazon Kinesis Data Streams Applications.

### Data Flow
1. Producers continuously push data to Kinesis Data Streams
2. Data is stored in shards for up to 365 days
3. Consumers process data in real time
4. Multiple consumers can process the same data stream simultaneously

## Capacity Management

### Provisioned Mode
In provisioned mode, you specify the number of shards for the data stream. Each shard can support:
- Up to 1,000 records per second for writes
- Up to 2 MB per second data input
- Up to 2 MB per second data output

### On-Demand Mode
In on-demand mode, Kinesis Data Streams automatically manages the shards to provide the necessary capacity. You don't need to specify or manage the capacity.

## Data Retention and Replay

### Retention Period
Data records are accessible for a default of 24 hours from the time they are added to a stream. You can increase this to up to 365 days by enabling extended data retention.

### Data Replay
You can replay data within the retention period. This is useful for:
- Recovering from application failures
- Running multiple analytics applications on the same data
- Reprocessing data with updated algorithms

## Security Features

### Encryption
- Server-side encryption using AWS KMS
- Client-side encryption for additional security
- Encryption in transit using HTTPS/TLS

### Access Control
- IAM policies for fine-grained access control
- VPC endpoints for private connectivity
- Resource-based policies for cross-account access

### Monitoring and Logging
- CloudWatch metrics for stream monitoring
- CloudTrail logging for API calls
- Enhanced fan-out monitoring

## Integration with AWS Services

### AWS Lambda
Process streaming data with serverless functions that automatically scale based on the incoming data rate.

### Amazon Kinesis Data Firehose
Easily load streaming data into data lakes, data stores, and analytics services.

### Amazon Kinesis Data Analytics
Analyze streaming data in real time with SQL queries or Apache Flink applications.

### Amazon S3
Archive streaming data for long-term storage and batch analytics.

### Amazon Redshift
Load processed streaming data into a data warehouse for business intelligence.

## Best Practices

### Shard Management
- Monitor shard utilization and split hot shards
- Merge underutilized shards to optimize costs
- Use appropriate partition keys for even distribution

### Producer Optimization
- Use batch operations to improve throughput
- Implement retry logic with exponential backoff
- Monitor producer metrics and error rates

### Consumer Optimization
- Use the Kinesis Client Library for fault tolerance
- Implement checkpointing for progress tracking
- Scale consumers based on shard count

### Cost Optimization
- Choose appropriate retention periods
- Use on-demand mode for variable workloads
- Monitor and optimize shard utilization

## Common Use Cases

### Real-time Analytics
Process and analyze data as it arrives to generate immediate insights and trigger real-time actions.

### Log and Event Data Collection
Collect and process log files, events, and other time-series data from multiple sources.

### IoT Data Processing
Handle high-volume, high-velocity data from IoT devices and sensors.

### Gaming Data Analytics
Process player actions, game events, and telemetry data in real time.

### Financial Data Processing
Handle trading data, fraud detection, and risk analysis with low-latency requirements.

### Social Media Analytics
Process social media feeds, sentiment analysis, and trending topic detection.

## Performance Considerations

### Throughput Limits
- Each shard supports up to 1,000 PUT records per second
- Maximum of 1 MB per second or 1,000 records per second per shard for writes
- Maximum of 2 MB per second per shard for reads

### Latency
- Typical put-to-get latency is less than 1 second
- Enhanced fan-out provides dedicated throughput per consumer

### Scaling
- Scale by adding or removing shards
- Use resharding operations during low-traffic periods
- Monitor CloudWatch metrics to determine scaling needs
