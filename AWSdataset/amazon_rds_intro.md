# What is Amazon Relational Database Service (Amazon RDS)?

Amazon Relational Database Service (Amazon RDS) is a web service that makes it easier to set up, operate, and scale a
relational database in the AWS Cloud. It provides cost-efficient, resizable capacity for an
industry-standard relational database and manages common database administration tasks.

## Advantages of Amazon RDS

Amazon RDS is a managed database service. It's responsible for most management tasks. By
eliminating tedious manual processes, Amazon RDS frees you to focus on your application and
your users.

Amazon RDS provides the following principal advantages over database deployments that aren't
fully managed:

* You can use database engines that you are already familiar with: IBM Db2, MariaDB,
  Microsoft SQL Server, MySQL, Oracle Database, and PostgreSQL.
* Amazon RDS manages backups, software patching, automatic failure detection, and
  recovery.
* You can turn on automated backups, or manually create your own backup
  snapshots. You can use these backups to restore a database. The Amazon RDS restore
  process works reliably and efficiently.
* You can get high availability with a primary DB instance and a synchronous secondary
  DB instance that you can fail over to when problems occur. You can also use read
  replicas to increase read scaling.
* In addition to the security in your database package, you can control access by using
  AWS Identity and Access Management (IAM) to define users and permissions. You can also help protect
  your databases by putting them in a virtual private cloud (VPC).

## Comparison of responsibilities with Amazon EC2 and on-premises deployments

We recommend Amazon RDS as your default choice for most relational database deployments.
The following alternatives have the disadvantage of making you spend more time managing
software and hardware:

**On-premises deployment**
:   When you buy an on-premises server, you get CPU, memory, storage, and
    IOPS, all bundled together. You assume full responsibility for the server,
    operating system, and database software.

**Amazon EC2**
:   Amazon Elastic Compute Cloud (Amazon EC2) provides scalable computing capacity in the AWS Cloud.
    Unlike in an on-premises server, CPU, memory, storage, and IOPS are
    separated so that you can scale them independently. AWS manages the
    hardware layers, which eliminates some of the burden of managing an
    on-premises database server.

    The disadvantage to running a database on Amazon EC2 is that you're more prone to user errors.
    For example, when you update the operating system or database software
    manually, you might accidentally cause application downtime.

The following table compares the management models for on-premises databases, Amazon EC2,
and Amazon RDS.

| Feature | On-premises management | Amazon EC2 management | Amazon RDS management |
| --- | --- | --- | --- |
| Application optimization | Customer | Customer | Customer |
| Scaling | Customer | Customer | AWS |
| High availability | Customer | Customer | AWS |
| Database backups | Customer | Customer | AWS |
| Database software patching | Customer | Customer | AWS |
| Database software install | Customer | Customer | AWS |
| Operating system (OS) patching | Customer | Customer | AWS |
| OS installation | Customer | Customer | AWS |
| Server maintenance | Customer | AWS | AWS |
| Hardware lifecycle | Customer | AWS | AWS |
| Power, network, and cooling | Customer | AWS | AWS |

## Amazon RDS shared responsibility model

Amazon RDS is responsible for hosting the software components and infrastructure of DB instances and
DB clusters. You are responsible for query tuning, which is the process of adjusting SQL queries
to improve performance. Query performance is highly dependent on database design, data size,
data distribution, application workload, and query patterns, which can vary greatly.
Monitoring and tuning are highly individualized processes that you own for your RDS
databases. You can use Amazon RDS Performance Insights and other tools to identify problematic
queries.

## Amazon RDS DB instances

A *DB instance* is an isolated database environment in the
AWS Cloud. The basic building block of Amazon RDS is the DB instance. Your DB instance can contain one or
more user-created databases.

You can access your DB instances by using the same tools and applications that you use with a
standalone database instance. You can create and modify a DB instance by using the AWS Command Line Interface
(AWS CLI), the Amazon RDS API, or the AWS Management Console.

### Amazon RDS application architecture: example

The following components are typical in an Amazon RDS architecture:

**Elastic Load Balancing**
:   AWS routes user traffic through Elastic Load Balancing. A load balancer
    distributes workloads across multiple compute resources, such as virtual
    servers. In this sample use case, the Elastic Load Balancer forwards client
    requests to application servers.

**Application servers**
:   Application servers interact with RDS DB instances. An application server in
    AWS is typically hosted on EC2 instances, which provide scalable computing
    capacity. The application servers reside in public subnets with different
    Availability Zones (AZs) within the same Virtual Private Cloud (VPC).

**RDS DB instances**
:   The EC2 application servers interact with RDS DB instances. The DB instances reside in
    private subnets within different Availability Zones (AZs) within the same
    Virtual Private Cloud (VPC). Because the subnets are private, no requests
    from the internet are permitted.

    The primary DB instance replicates to another DB instance, called a *read
    replica*. Both DB instances are in private subnets within the VPC,
    which means that Internet users can't access them directly.

### DB engines

A *DB engine* is the specific relational database software
that runs on your DB instance. Amazon RDS supports the following database engines:

* **IBM Db2** - Enterprise-grade database for mission-critical applications
* **MariaDB** - Open-source relational database, MySQL-compatible
* **Microsoft SQL Server** - Microsoft's relational database management system
* **MySQL** - Popular open-source relational database
* **Oracle Database** - Enterprise database with advanced features
* **PostgreSQL** - Advanced open-source object-relational database

Each DB engine has its own supported features, and each version of a DB engine can include
specific features. Support for Amazon RDS features varies across AWS Regions and specific
versions of each DB engine.

Additionally, each DB engine has a set of parameters in a DB parameter group that control the behavior of the
databases that it manages.

### DB instance classes

A *DB instance class* determines the computation and memory
capacity of a DB instance. A DB instance class consists of both the DB instance type and the size.
Each instance type offers different compute, memory, and storage capabilities.

### DB instance storage

Amazon RDS provides three storage types: General Purpose SSD (gp2 and gp3), Provisioned IOPS SSD (io1 and io2), and Magnetic (standard).
They differ in performance characteristics and price, allowing you to tailor your storage performance and cost to the needs of your database.

### DB instances in an Amazon Virtual Private Cloud (Amazon VPC)

You can run a DB instance on the Amazon Virtual Private Cloud (Amazon VPC) service. When you use a VPC, you have control over your virtual networking environment.
You can choose your own IP address range, create subnets, and configure routing and access control lists.
The basic functionality of Amazon RDS is the same whether it runs in a VPC or not.
