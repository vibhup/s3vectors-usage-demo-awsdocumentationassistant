# What is Amazon DynamoDB?

Amazon DynamoDB is a serverless, NoSQL, fully managed database with single-digit millisecond performance at any scale.

DynamoDB addresses your needs to overcome scaling and operational complexities of relational
databases. DynamoDB is purpose-built and optimized for operational workloads that require
consistent performance at any scale. For example, DynamoDB delivers consistent single-digit
millisecond performance for a shopping cart use case, whether you've 10 or 100 million
users. Launched in 2012, DynamoDB continues to help you move away from relational
databases while reducing cost and improving performance at scale.

Customers across all sizes, industries, and geographies use DynamoDB to build modern, serverless applications that can start small and scale globally. DynamoDB scales to support tables of virtually any size while
providing consistent single-digit millisecond performance and high availability.

For events, such as Amazon Prime Day, DynamoDB
powers multiple high-traffic Amazon properties and systems, including Alexa, Amazon.com sites, and all Amazon fulfillment
centers. For such events, DynamoDB APIs have handled trillions of calls from Amazon
properties and systems. DynamoDB continuously serves hundreds of customers with tables that
have peak traffic of over half a million requests per second. It also serves hundreds of
customers whose table sizes exceed 200 TB, and processes over one billion requests per hour.

## Characteristics of DynamoDB

### Serverless

With DynamoDB, you don't need to provision any servers, or patch, manage, install,
maintain, or operate any software. DynamoDB provides zero downtime maintenance. It has
no versions (major, minor, or patch), and there are no maintenance windows.

DynamoDB's on-demand capacity mode
offers pay-as-you-go pricing for read and write requests so you only pay for what
you use. With on-demand, DynamoDB instantly scales up or down your tables to adjust for
capacity and maintains performance with zero administration. It also scales down to
zero so you don't pay for throughput when your table doesn't have traffic and there
are no cold starts.

### NoSQL

As a NoSQL database, DynamoDB is purpose-built to deliver improved performance,
scalability, manageability, and flexibility compared to traditional relational
databases. To support a wide variety of use cases, DynamoDB supports both key-value and
document data models.

Unlike relational databases, DynamoDB doesn't support a JOIN operator. We recommend
that you denormalize your data model to reduce database round trips and processing
power needed to answer queries. As a NoSQL database, DynamoDB provides strong read consistency and ACID
transactions to build enterprise-grade applications.

### Fully managed

As a fully managed database service, DynamoDB handles the undifferentiated heavy
lifting of managing a database so that you can focus on building value for your
customers. It handles setup, configurations, maintenance, high availability,
hardware provisioning, security, backups, monitoring, and more. This ensures that
when you create a DynamoDB table, it's instantly ready for production workloads. DynamoDB
constantly improves its availability, reliability, performance, security, and
functionality without requiring upgrades or downtime.

### Single-digit millisecond performance at any scale

DynamoDB was purpose-built to improve upon the performance and scalability of
relational databases to deliver single-digit millisecond performance at any scale.
To achieve this scale and performance, DynamoDB is optimized for high-performance
workloads and provides APIs that encourage efficient database usage. It omits
features that are inefficient and non-performing at scale, for example, JOIN
operations. DynamoDB delivers consistent single-digit millisecond performance for your
application, whether you've 100 or 100 million users.

## DynamoDB use cases

Customers across all sizes, industries, and geographies use DynamoDB to build modern, serverless applications that can start small and scale globally. DynamoDB is ideal for use cases that require consistent
performance at any scale with little to zero operational overhead. The following list
presents some use cases where you can use DynamoDB:

* **Financial service applications** –
  Suppose you're a financial services company building applications, such as live
  trading and routing, loan management, token generation, and transaction ledgers.
  With DynamoDB global tables, your applications
  can respond to events and serve traffic from your chosen AWS Regions with
  fast, local read and write performance.

  DynamoDB is suitable for applications with the most stringent availability
  requirements. It removes the operational burden of manually scaling instances
  for increased storage or throughput, versioning, and licensing.

  You can use DynamoDB transactions to achieve
  atomicity, consistency, isolation, and durability (ACID) across one or more
  tables with a single request. ACID
  transactions suit workloads that include processing financial
  transactions or fulfilling orders. DynamoDB instantly accommodates your workloads
  as they ramp up or down, enabling you to efficiently scale your database for
  market conditions, such as trading hours.

* **Gaming applications** – As a gaming
  company, you can use DynamoDB for all parts of game platforms, for example, game
  state, player data, session history, and leaderboards. Choose DynamoDB for its
  scale, consistent performance, and the ease of operations provided by its
  serverless architecture. DynamoDB is well suited for scale-out architectures needed
  to support successful games. It quickly scales your game's throughput both in
  and out (scale to zero with no cold start). This scalability optimizes your
  architecture's efficiency whether you're scaling out for peak traffic or scaling
  back when gameplay usage is low.

* **Streaming applications** – Media and
  entertainment companies use DynamoDB as a metadata index for content, content
  management service, or to serve near real-time sports statistics. They also use
  DynamoDB to run user watchlist and bookmarking services and process billions of
  daily customer events for generating recommendations. These customers benefit
  from DynamoDB's scalability, performance, and resiliency. DynamoDB scales to workload
  changes as they ramp up or down, enabling streaming media use cases that can
  support any levels of demand.

## Capabilities of DynamoDB

### Multi-active replication with global tables

Global tables provide multi-active replication
of your data across your chosen AWS Regions with 99.999% availability. Global
tables deliver a fully managed solution for deploying a multi-Region, multi-active
database, without building and maintaining your own replication solution. With
global tables, you can specify the AWS Regions where you want the tables to be
available. DynamoDB replicates ongoing data changes to all of these tables.

Your globally distributed applications can access data locally in your selected
Regions to achieve single-digit millisecond read and write performance. Because
global tables are multi-active, you don't need a primary table. This means there are
no complicated or delayed fail-overs, or database downtime when failing over an
application between Regions.

### ACID transactions

DynamoDB is built for mission-critical workloads, including support for ACID transactions.
DynamoDB transactions provide the ability to perform coordinated, all-or-nothing changes to multiple items both within and across tables.
Transactions provide atomicity, consistency, isolation, and durability (ACID) in DynamoDB, helping you to maintain data correctness in your applications.

### Point-in-time recovery

DynamoDB point-in-time recovery (PITR) provides automatic backups of your DynamoDB table data.
When enabled, DynamoDB maintains incremental backups of your table for the last 35 days until you explicitly disable it.
You can recover your table to any point in time during that 35-day period.

### On-demand backup and restore

You can create on-demand backups and restore your Amazon DynamoDB tables at any point in time.
On-demand backups help with long-term archival requirements for regulatory compliance.
You can back up tables from a few megabytes to hundreds of terabytes of data, with no impact on the performance or availability of your production applications.

### Encryption at rest

DynamoDB encryption at rest provides an additional layer of data protection by securing your data in the underlying storage.
Organizational policies, industry or government regulations, and compliance requirements often require the use of encryption at rest to increase the data security of your applications.
