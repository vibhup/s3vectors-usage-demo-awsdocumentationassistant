# What is Amazon CloudWatch?

Amazon CloudWatch monitors your Amazon Web Services (AWS) resources and the applications you run on
AWS in real time, and offers many tools to give
you system-wide observability of your
application performance, operational health, and resource utilization.

## Operational visibility with metrics, alarms, and dashboards

Metrics collect and track key performance data at user-defined intervals. Many AWS services automatically report metrics into CloudWatch, and you can also publish
custom metrics in CloudWatch from your applications.

Dashboards offer a unified view of your resources and applications with visualizations of your metrics and logs in a single location. You can also
share dashboards across accounts and Regions for enhanced operational awareness. CloudWatch provides curated automatic dashboards for many AWS services,
so that you don't have to build them yourself.

You can set up alarms that continuously monitor CloudWatch metrics against user-defined thresholds. They can automatically alert you to breaches of the thresholds, and
can also automatically respond to changes in your resources' behavior by triggering automated actions.

## Application performance monitoring (APM)

With Application Signals
you can automatically detect and monitor your applications' key performance indicators like latency, error rates, and request rates without manual instrumentation or code changes. Application Signals
also provides curated dashboards so you can begin monitoring with a minimum of setup.

CloudWatch Synthetics complements this by enabling you to proactively monitor your endpoints and APIs through configurable scripts called *canaries* that simulate user behavior and alert you to availability
issues or performance degradation before they impact real users. You
can also use CloudWatch RUM to gather performance data from real user sessions.

Use Service Level Objectives (SLOs) in CloudWatch to define, track, and alert on specific reliability targets for your applications, helping you maintain service quality commitments by
setting error budgets and monitoring SLO compliance over time.

## Infrastructure monitoring

Many AWS services automatically send basic metrics to CloudWatch for free. Services that send metrics are listed here. Additionally, CloudWatch provides additional monitoring capabilities
for several key pieces of AWS infrastructure:

* **Database Insights** allows you to monitor database performance metrics in real time, analyze SQL query performance, and troubleshoot database load issues for
  AWS database services.
* **Lambda Insights** provides system-level metrics for Lambda functions, including memory and CPU utilization tracking, and cold start detection and analysis.
* **Container Insights** allows you to collect and analyze metrics from containerized applications,
  on Amazon ECS clusters, Amazon EKS clusters, and self-managed Kubernetes clusters on Amazon EC2.

## Collect, store, and query logs

CloudWatch Logs offers a suite of powerful features for comprehensive log management and analysis. Logs ingested from AWS services and custom applications are stored in
log groups and streams for easy organization.
Use CloudWatch Logs Insights to perform interactive, fast queries on your log data, with a choice of three query languages including SQL and PPL.
Use log anomaly detection to find unusual patterns in log events in a log group, which can indicate issues.
Create metric filters to extract numerical values from logs and generate CloudWatch metrics, which you can use for alerting and dashboards.
Set up subscription filters to process and analyze logs in real-time or route them to other services like Amazon S3 or Firehose.

## Use the CloudWatch agent to gather metrics, logs, and traces from Amazon EC2 fleets

Use the CloudWatch agent to collect detailed system
metrics about processes, CPU, memory, disk usage, and network performance from your fleets of Amazon EC2 instances and on-premises servers.
You can also collect and monitor custom metrics from your applications, aggregate logs from multiple sources, and configure alarms based on the collected data.
You can also use the agent to gather GPU metrics. The agent supports both Windows and Linux operating systems and can integrate with Systems Manager for centralized configuration management.

## Cross-account monitoring

CloudWatch cross-account observability lets you
set up a central monitoring account to monitor and troubleshoot applications that span multiple accounts.
From the central account, you can view metrics, logs, and traces from source
accounts across your organization. This centralized approach enables you to create cross-account dashboards,
set up alarms that watch metrics from multiple accounts, and perform root-cause analysis across account
boundaries. With CloudWatch cross-account observability, you can link source accounts either individually or
link them automatically through AWS Organizations.

## Solutions catalog

CloudWatch offers a catalog of readily available configurations to help you quickly implement monitoring for various AWS services and common workloads, such as Java Virtual Machines (JVM), NVIDIA GPU, Apache Kafka,
Apache Tomcat, and
NGINX. These solutions provide focused guidance, including instructions for installing and configuring the CloudWatch agent, deploying pre-defined custom dashboards, and setting up related alarms.

## Network and internet monitoring

CloudWatch provides comprehensive network and internet monitoring capabilities through CloudWatch Network Monitoring.

Internet Monitor uses AWS global networking data to analyze
internet performance and availability between your applications and end users. With an internet monitor,
you can identify or get notifications for increased latency or regional disruptions that impact your customers.
Internet monitors work by analyzing your VPC flow logs to provide automated insights about network traffic
patterns and performance. You can also get suggestions for how to optimize application performance for your
clients.

Network Flow Monitor displays network performance
information gathered by lightweight software agents that you install on your instances. Using a flow monitor,
you can quickly visualize packet loss and latency of your network connections over a time
frame that
you specify. Each monitor also generates a network health indicator (NHI), which tells you whether there
were AWS network issues for the network flows tracked by your monitor during the time period that you're
evaluating.

When you connect by using AWS Direct Connect, you can use synthetic monitors in Network Synthetic Monitor to proactively monitor network connectivity
by running synthetic tests between a VPC and on-premises endpoints. When you create a synthetic monitor, you
specify probes by providing a VPC subnet and on-premises IP addresses. AWS creates and manages the
infrastructure in the background that is required to perform round-trip time and packet loss measurements
with the probes. These tests detect issues with connectivity, DNS, and latency before they impact your
applications, so that you can take action to improve your end users' experience.

## Billing and costs

For complete information about CloudWatch pricing, see Amazon CloudWatch Pricing.

For information that can help you analyze your bill and possibly optimize and reduce costs,
see Analyzing, optimizing, and reducing CloudWatch costs.

## Amazon CloudWatch resources

The following related resources
can help you as you work with this service.

| Resource | Description |
| --- | --- |
| Amazon CloudWatch FAQs | The FAQ covers the top questions developers have asked about this product. |
| AWS Developer Center | A central starting point to find documentation, code examples, release notes, and other information to help you build innovative applications with AWS. |
| AWS Management Console | The console allows you to perform most of the functions of Amazon CloudWatch and various other AWS offerings without programming. |
| Amazon CloudWatch Discussion Forums | Community-based forum for developers to discuss technical questions related to Amazon CloudWatch. |
| AWS Support | The hub for creating and managing your AWS Support cases. Also includes links to other helpful resources, such as forums, technical FAQs, service health status, and AWS Trusted Advisor. |
| Amazon CloudWatch product information | The primary web page for information about Amazon CloudWatch. |
| Contact Us | A central contact point for inquiries concerning AWS billing, account, events, abuse, etc. |

## Key CloudWatch Concepts

### Metrics
Metrics are data points that represent the performance of your systems over time. Each metric has a name, namespace, and one or more dimensions. CloudWatch stores metrics for up to 15 months, allowing you to view both recent and historical data.

### Namespaces
Namespaces are containers for CloudWatch metrics. AWS services use specific namespaces (like AWS/EC2 for EC2 metrics), and you can create custom namespaces for your application metrics.

### Dimensions
Dimensions are name-value pairs that help identify a metric. For example, an EC2 metric might have dimensions for InstanceId and InstanceType.

### Alarms
CloudWatch alarms watch metrics and trigger actions when thresholds are breached. Actions can include sending notifications, auto-scaling, or stopping/starting instances.

### Events and EventBridge
CloudWatch Events (now Amazon EventBridge) enables you to respond to state changes in your AWS resources by triggering automated actions.

## Integration with AWS Services

CloudWatch integrates with virtually all AWS services, providing:
- Automatic metric collection from AWS services
- Log aggregation from applications and services
- Custom metric publishing from applications
- Alarm-based automated responses
- Cross-service monitoring and correlation

## Best Practices

### Metric Management
- Use appropriate metric resolution (standard vs. high-resolution)
- Implement custom metrics for application-specific monitoring
- Use metric filters to extract metrics from logs
- Set up composite alarms for complex monitoring scenarios

### Cost Optimization
- Use metric filters instead of custom metrics when possible
- Implement log retention policies
- Use CloudWatch Logs Insights for ad-hoc queries instead of continuous monitoring
- Monitor your CloudWatch usage and costs regularly

### Alerting Strategy
- Create meaningful alarm names and descriptions
- Use appropriate alarm states and actions
- Implement escalation procedures for critical alarms
- Test alarm notifications regularly
