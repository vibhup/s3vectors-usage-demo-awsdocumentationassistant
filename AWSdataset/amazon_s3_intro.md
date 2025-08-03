# What is Amazon S3?

Amazon Simple Storage Service (Amazon S3) is an object storage service that offers industry-leading scalability,
data availability, security, and performance. Customers of all sizes and industries can use
Amazon S3 to store and protect any amount of data for a range of use cases, such as data lakes,
websites, mobile applications, backup and restore, archive, enterprise applications, IoT
devices, and big data analytics. Amazon S3 provides management features so that you can optimize,
organize, and configure access to your data to meet your specific business, organizational,
and compliance requirements.

## Features of Amazon S3

### Storage classes

Amazon S3 offers a range of storage classes designed for different use cases. For
example, you can store mission-critical production data in S3 Standard or S3 Express One Zone for frequent
access, save costs by storing infrequently accessed data in S3 Standard-IA or
S3 One Zone-IA, and archive data at the lowest costs in S3 Glacier Instant Retrieval,
S3 Glacier Flexible Retrieval, and S3 Glacier Deep Archive.

Amazon S3 Express One Zone is a high-performance, single-zone Amazon S3 storage class that is purpose-built
to deliver consistent, single-digit millisecond data access for your most
latency-sensitive applications. S3 Express One Zone is the lowest latency cloud object
storage class available today, with data access
speeds
up to 10x faster and with request costs
50
percent lower than S3 Standard. S3 Express One Zone is the first S3 storage class where you can select a single Availability Zone with
the option to co-locate your object storage with your compute resources, which provides the highest possible access speed.
Additionally, to further increase access speed and support hundreds of thousands of
requests per second, data is stored in a new bucket type: an
Amazon S3 directory bucket.

You can store data with changing or unknown access patterns in
S3 Intelligent-Tiering, which optimizes storage costs by automatically moving your
data between four access tiers when your access patterns change. These four access
tiers include two low-latency access tiers optimized for frequent and infrequent
access, and two opt-in archive access tiers designed for asynchronous access for
rarely accessed data.

### Storage management

Amazon S3 has storage management features that you can use to manage costs, meet
regulatory requirements, reduce latency, and save multiple distinct copies of your
data for compliance requirements.

* **S3 Lifecycle** – Configure a lifecycle configuration to manage
  your objects and store them cost effectively throughout their lifecycle. You
  can transition objects to other S3 storage classes or expire objects that
  reach the end of their lifetimes.
* **S3 Object Lock** – Prevent Amazon S3 objects from being
  deleted or overwritten for a fixed amount of time or indefinitely. You can
  use Object Lock to help meet regulatory requirements that require *write-once-read-many*
  *(WORM)* storage or to simply add another
  layer of protection against object changes and deletions.
* **S3 Replication** – Replicate objects and their respective metadata and object tags to
  one or more destination buckets in the same or different AWS Regions for
  reduced latency, compliance, security, and other use cases.
* **S3 Batch Operations** – Manage billions of objects at scale
  with a single S3 API request or a few clicks in the Amazon S3 console. You can
  use Batch Operations to perform operations such as **Copy**, **Invoke AWS Lambda
  function**, and **Restore** on
  millions or billions of objects.

### Access management and security

Amazon S3 provides features for auditing and managing access to your buckets and
objects. By default, S3 buckets and the objects in them are private. You have access
only to the S3 resources that you create. To grant granular resource permissions
that support your specific use case or to audit the permissions of your Amazon S3
resources, you can use the following features.

* **S3 Block Public Access** – Block public access to S3
  buckets and objects. By default, Block Public Access settings are turned on
  at the bucket level. We recommend that you keep all Block Public Access
  settings enabled unless you know that you need to turn off one or more of
  them for your specific use case.
* **AWS Identity and Access Management (IAM)** – IAM is a web service that helps
  you securely control access to AWS resources, including your Amazon S3
  resources. With IAM, you can centrally manage permissions that control
  which AWS resources users can access. You use IAM to control who is
  authenticated (signed in) and authorized (has permissions) to use
  resources.
* **Bucket policies** – Use IAM-based policy language to configure
  resource-based permissions for your S3 buckets and the objects in
  them.
* **Amazon S3 access points** – Configure named network endpoints with dedicated access policies to
  manage data access at scale for shared datasets in Amazon S3.
* **Access control lists (ACLs)** – Grant read and write permissions for
  individual buckets and objects to authorized users. As a general rule, we
  recommend using S3 resource-based policies (bucket policies and access point
  policies) or IAM user policies for access control instead of ACLs.
  Policies are a simplified and more flexible access control option.
* **S3 Object Ownership** – Take ownership of every object
  in your bucket, simplifying access management for data stored in Amazon S3.
  S3 Object Ownership is an Amazon S3 bucket-level setting that you can use to
  disable or enable ACLs. By default, ACLs are disabled.
* **IAM Access Analyzer for S3** – Evaluate and monitor your S3 bucket access policies, ensuring that
  the policies provide only the intended access to your S3 resources.

### Data processing

To transform data and trigger workflows to automate a variety of other processing
activities at scale, you can use the following features.

* **S3 Object Lambda** – Add your own code to S3 GET, HEAD, and LIST requests to modify and process data as
  it is returned to an application. Filter rows, dynamically resize images,
  redact confidential data, and much more.
* **Event notifications** – Trigger workflows that use Amazon Simple Notification Service
  (Amazon SNS), Amazon Simple Queue Service (Amazon SQS), and AWS Lambda when a change is made to your S3
  resources.

### Storage logging and monitoring

Amazon S3 provides logging and monitoring tools that you can use to monitor and control
how your Amazon S3 resources are being used.

**Automated monitoring tools**

* **Amazon CloudWatch metrics for Amazon S3** – Track the operational health of your
  S3 resources and configure billing alerts when estimated charges reach a
  user-defined threshold.
* **AWS CloudTrail** – Record actions taken by a user, a role, or an AWS service in
  Amazon S3. CloudTrail logs provide you with detailed API tracking for S3 bucket-level
  and object-level operations.

**Manual monitoring tools**

* **Server access logging** – Get detailed records for the requests that are
  made to a bucket. You can use server access logs for many use cases, such as
  conducting security and access audits, learning about your customer base,
  and understanding your Amazon S3 bill.
* **AWS Trusted Advisor** – Evaluate your account by using AWS best
  practice checks to identify ways to optimize your AWS infrastructure,
  improve security and performance, reduce costs, and monitor service quotas.

### Analytics and insights

Amazon S3 offers features to help you gain visibility into your storage usage, which
empowers you to better understand, analyze, and optimize your storage at
scale.

* **Amazon S3 Storage Lens** – Understand, analyze, and optimize your storage. S3 Storage Lens provides
  60+ usage and activity metrics and interactive dashboards to aggregate data
  for your entire organization, specific accounts, AWS Regions, buckets, or
  prefixes.
* **Storage Class Analysis** – Analyze storage access patterns to
  decide when it's time to move data to a more cost-effective storage class.
* **S3 Inventory with Inventory reports** – Audit and report on objects and their
  corresponding metadata and configure other Amazon S3 features to take action in
  Inventory reports.

### Strong consistency

Amazon S3 provides strong read-after-write consistency for PUT and DELETE requests of
objects in your Amazon S3 bucket in all AWS Regions. This behavior applies to both
writes of new objects as well as PUT requests that overwrite existing objects and
DELETE requests.

## How Amazon S3 works

Amazon S3 is an object storage service that stores data as objects within buckets. An
*object* is a file and any metadata that describes
the file. A *bucket* is a container for objects.

To store your data in Amazon S3, you first create a bucket and specify a bucket name and
AWS Region. Then, you upload your data to that bucket as objects in Amazon S3. Each object
has a *key* (or *key name*), which is the unique identifier for the object within the
bucket.

S3 provides features that you can configure to support your specific use case. For
example, you can use S3 Versioning to keep multiple versions of an object in the same
bucket, which allows you to restore objects that are accidentally deleted or
overwritten.

Buckets and the objects in them are private and can be accessed only if you explicitly
grant access permissions. You can use bucket policies, AWS Identity and Access Management (IAM) policies,
access control lists (ACLs), and S3 Access Points to manage access.

### Buckets

Amazon S3 supports four types of buckets—general purpose buckets, directory buckets, table buckets, and vector buckets. Each type of bucket provides a unique set of features for different use cases.

**General purpose buckets** – General purpose buckets are recommended for most use cases and access patterns and are the original S3 bucket type.
A general purpose bucket is a container for objects stored in Amazon S3, and you can store any number of objects in a bucket and across all storage classes (except for
S3 Express One Zone), so you can redundantly store objects across multiple Availability Zones.

**Directory buckets** – Recommended for low-latency use cases and data-residency use cases. By default, you can create up to 100 directory buckets in your
AWS account, with no limit on the number of objects that you can store in a directory bucket. Directory buckets organize objects into hierarchical directories (prefixes) instead of the flat storage structure
of general purpose buckets.

* For low-latency use cases, you can create a directory bucket in a single AWS Availability Zone to store data. Directory buckets in Availability Zones support the
  S3 Express One Zone storage class.
* For data-residency use cases, you can create a directory bucket in a single AWS Dedicated Local Zone (DLZ) to store data.
