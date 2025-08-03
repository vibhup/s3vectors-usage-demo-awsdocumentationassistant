# What is AWS Lambda?

You can use AWS Lambda to run code without provisioning or managing servers. Lambda runs your code on a high-availability compute infrastructure and manages all the computing resources,
including server and operating system maintenance, capacity provisioning, automatic scaling, and logging. You organize your code into Lambda functions.
The Lambda service runs your function only when needed and scales automatically. For pricing information, see [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/ "https://aws.amazon.com/lambda/pricing/") for details.

When using Lambda, you are responsible only for your code. Lambda manages the compute fleet that offers a
balance of memory, CPU, network, and other resources to run your code. Because Lambda manages these resources, you
cannot log in to compute instances or customize the operating system on provided
runtimes.

## When to use Lambda

Lambda is an ideal compute service for application scenarios that need to scale up rapidly, and scale down to
zero when not in demand. For example, you can use Lambda for:

* **Stream processing:** Use Lambda and Amazon Kinesis to process real-time streaming data for application activity tracking, transaction order processing, clickstream analysis, data cleansing, log filtering, indexing, social media analysis, Internet of Things (IoT) device data telemetry, and metering.
* **Web applications:** Combine Lambda with other AWS services to build powerful web applications that automatically scale up and down and run in a highly available configuration across multiple data centers.
  To build web applications with AWS services, developers can use infrastructure as code (IaC) and orchestration tools such as [AWS CloudFormation](https://aws.amazon.com/cloudformation "https://aws.amazon.com/cloudformation"), [AWS Cloud Development Kit (AWS CDK)](https://aws.amazon.com/cdk "https://aws.amazon.com/cdk"), [AWS Serverless Application Model](https://aws.amazon.com/serverless/sam "https://aws.amazon.com/serverless/sam"), or coordinate complex workflows using
  [AWS Step Functions](https://aws.amazon.com/step-functions "https://aws.amazon.com/step-functions").
* **Mobile backends:** Build backends using Lambda and Amazon API Gateway to authenticate and process API requests. Use AWS Amplify to easily integrate with your iOS, Android, Web, and React Native frontends.
* **[IoT backends](./services-iot.html "./services-iot.html"):** Build serverless backends using Lambda to handle web, mobile, IoT, and third-party API requests.
* **[File processing:](./example-apps.html#examples-apps-file "./example-apps.html#examples-apps-file"):** Use Amazon Simple Storage Service (Amazon S3) to trigger Lambda data processing in real time after an upload.
* **[Database Operations and Integration:](./example-apps.html#examples-apps-database "./example-apps.html#examples-apps-database"):** Use Lambda to process database interactions both reactively and proactively, from handling queue messages for Amazon RDS operations like user registrations and order submissions,
  to responding to DynamoDB changes for audit logging, data replication, and automated workflows.
* **[Scheduled and Periodic Tasks:](./example-apps.html#examples-apps-scheduled "./example-apps.html#examples-apps-scheduled"):** Use Lambda with EventBridge rules to execute time-based operations such as database maintenance, data archiving, report generation, and other scheduled business processes using cron-like expressions.

## How Lambda works

Because Lambda is a serverless, event-driven compute service, it uses a different programming paradigm than traditional web applications.
The following model illustrates how Lambda fundamentally works:

1. You write and organize your code in [Lambda functions](./concepts-basics.html#gettingstarted-concepts-function "./concepts-basics.html#gettingstarted-concepts-function"), which are the basic building blocks you use to create a Lambda application.
2. You control security and access through [Lambda permissions](./lambda-permissions.html "./lambda-permissions.html"), using [execution roles](./lambda-intro-execution-role.html "./lambda-intro-execution-role.html") to manage what AWS services your functions can interact with and what resource policies can interact with your code.
3. Event sources and AWS services [trigger](./concepts-event-driven-architectures.html "./concepts-event-driven-architectures.html") your Lambda functions, passing event data in JSON format, which your functions process (this includes event source mappings).
4. [Lambda runs your code](./concepts-how-lambda-runs-code.html "./concepts-how-lambda-runs-code.html") with language-specific runtimes (like Node.js and Python) in execution environments that package your runtime, layers, and extensions.

###### Tip

To learn how to build **serverless solutions**, check out the [Serverless Developer Guide](https://docs.aws.amazon.com/serverless/latest/devguide/ "https://docs.aws.amazon.com/serverless/latest/devguide/").

## Key features

**Configure, control, and deploy secure applications:**

* [Environment variables](./configuration-envvars.html "./configuration-envvars.html") modify application behavior without new code deployments.
* [Versions](./configuration-versions.html "./configuration-versions.html") safely test new features while maintaining stable production environments.
* [Lambda layers](./chapter-layers.html "./chapter-layers.html") optimize code reuse and maintenance by sharing common components across multiple functions.
* [Code signing](./configuration-codesigning.html "./configuration-codesigning.html") enforce security compliance by ensuring only approved code reaches production systems.

**Scale and perform reliably:**

* [Concurrency and scaling controls](./lambda-concurrency.html "./lambda-concurrency.html") precisely manage application responsiveness and resource utilization during traffic spikes.
* [Lambda SnapStart](./snapstart.html "./snapstart.html") significantly reduce cold start times. Lambda SnapStart can provide as low as sub-second startup performance, typically with no changes to your function code.
* [Response streaming](./configuration-response-streaming.html "./configuration-response-streaming.html") optimize function performance by delivering large payloads incrementally for real-time processing.
* [Container images](./images-create.html "./images-create.html") package functions with complex dependencies using container workflows.

**Connect and integrate seamlessly:**

* [VPC networks](./configuration-vpc.html "./configuration-vpc.html") secure sensitive resources and internal services.
* [File system](./configuration-filesystem.html "./configuration-filesystem.html") integration that shares persistent data and manage stateful operations across function invocations.
* [Function URLs](./urls-configuration.html "./urls-configuration.html") create public-facing APIs and endpoints without additional services.
* [Lambda extensions](./lambda-extensions.html "./lambda-extensions.html") augment functions with monitoring, security, and operational tools.

## Related information

* For information on how Lambda works, see [How Lambda works](./concepts-basics.html "./concepts-basics.html").
* To start using Lambda, see [Create your first Lambda function](./getting-started.html "./getting-started.html").
* For a list of example applications, see [Getting started with example applications and patterns](./example-apps.html "./example-apps.html").
