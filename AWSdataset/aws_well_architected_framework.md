# AWS Well-Architected Framework

The AWS Well-Architected Framework helps you understand the pros and cons of decisions you
make while building systems on AWS. By using the Framework you will learn architectural best
practices for designing and operating reliable, secure, efficient, cost-effective, and sustainable systems in the cloud.

## Introduction

The AWS Well-Architected Framework helps you understand the pros and cons of decisions
you make while building systems on AWS. Using the Framework helps you learn architectural
best practices for designing and operating secure, reliable, efficient, cost-effective, and
sustainable workloads in the AWS Cloud. It provides a way for you to consistently measure
your architectures against best practices and identify areas for improvement. The process for
reviewing an architecture is a constructive conversation about architectural decisions, and is
not an audit mechanism. We believe that having well-architected systems greatly increases the
likelihood of business success.

AWS Solutions Architects have years of experience architecting solutions across a wide
variety of business verticals and use cases. We have helped design and review thousands of
customers' architectures on AWS. From this experience, we have identified best practices and
core strategies for architecting systems in the cloud.

The AWS Well-Architected Framework documents a set of foundational questions that help
you to understand if a specific architecture aligns well with cloud best practices. The
framework provides a consistent approach to evaluating systems against the qualities you expect
from modern cloud-based systems, and the remediation that would be required to achieve those
qualities. As AWS continues to evolve, and we continue to learn more from working with our
customers, we will continue to refine the definition of well-architected.

This framework is intended for those in technology roles, such as chief technology
officers (CTOs), architects, developers, and operations team members. It describes AWS best
practices and strategies to use when designing and operating a cloud workload, and provides
links to further implementation details and architectural patterns.

AWS also provides a service for reviewing your workloads at no charge. The AWS Well-Architected
Tool (AWS WA Tool) is a service in the cloud that provides a consistent process for
you to review and measure your architecture using the AWS Well-Architected Framework. The AWS WA
Tool provides recommendations for making your workloads more reliable, secure, efficient, and
cost-effective.

To help you apply best practices, we have created AWS Well-Architected
Labs, which provides you with a repository of code and documentation to give you
hands-on experience implementing best practices. We also have teamed up with select AWS Partner
Network (APN) Partners, who are members of the AWS Well-Architected
Partner program. These AWS Partners have deep AWS knowledge, and can help you review
and improve your workloads.

# The pillars of the framework

Creating a software system is a lot like constructing a building. If the foundation is
not solid, structural problems can undermine the integrity and function of the building. When
architecting technology solutions, if you neglect the six pillars of operational excellence,
security, reliability, performance efficiency, cost optimization, and sustainability, it can become challenging
to build a system that delivers on your expectations and requirements. Incorporating these
pillars into your architecture will help you produce stable and efficient systems. This will
allow you to focus on the other aspects of design, such as functional requirements.

## Operational Excellence

The operational excellence pillar focuses on running and monitoring systems, and continually improving processes and procedures. Key topics include automating changes, responding to events, and defining standards to manage daily operations.

### Design Principles

**Perform operations as code**
In the cloud, you can apply the same engineering discipline that you use for application code to your entire environment. You can define your entire workload (applications, infrastructure) as code and update it with code.

**Make frequent, small, reversible changes**
Design workloads to allow components to be updated regularly. Make changes in small increments that can be reversed if they fail (without affecting customers when possible).

**Refine operations procedures frequently**
As you use operations procedures, look for opportunities to improve them. As you evolve your workload, evolve your procedures appropriately.

**Anticipate failure**
Perform "pre-mortem" exercises to identify potential sources of failure so that they can be removed or mitigated. Test your failure scenarios and validate your understanding of their impact.

**Learn from all operational failures**
Drive improvement through lessons learned from all operational events and failures. Share what is learned across teams and through the entire organization.

### Best Practices

**Organization**
- Understand your organizational priorities
- Design for operations
- Evaluate operational readiness
- Understand operational health

**Prepare**
- Design telemetry
- Implement application telemetry
- Implement user activity telemetry
- Implement dependency telemetry
- Implement distributed tracing

**Operate**
- Utilize workload observability
- Understand operational health
- Respond to unplanned operational events
- Use runbooks for well-understood events
- Use playbooks to investigate issues

**Evolve**
- Learn from experience
- Share learnings
- Perform post-incident analysis
- Implement feedback loops

## Security

The security pillar focuses on protecting information and systems. Key topics include confidentiality and integrity of data, managing user permissions, and establishing controls to detect security events.

### Design Principles

**Implement a strong identity foundation**
Implement the principle of least privilege and enforce separation of duties with appropriate authorization for each interaction with your AWS resources.

**Apply security at all layers**
Apply a defense in depth approach with multiple security controls. Apply to all layers (edge network, VPC, subnet, load balancer, every instance, operating system, and application).

**Automate security best practices**
Automated software-based security mechanisms improve your ability to securely scale more rapidly and cost-effectively.

**Protect data in transit and at rest**
Classify your data into sensitivity levels and use mechanisms, such as encryption, tokenization, and access control, where appropriate.

**Keep people away from data**
Reduce or eliminate the need for direct access or manual processing of data to reduce the risk of mishandling or modification and human error when handling sensitive data.

**Prepare for security events**
Prepare for an incident by having incident management and investigation policy and processes that align to your organizational requirements.

### Best Practices

**Security Foundations**
- Implement AWS account management and separation
- Implement identity and access management
- Automate deployment of standard security controls
- Identify threats and prioritize mitigations using a threat model

**Identity and Access Management**
- Use strong sign-in mechanisms
- Use temporary credentials
- Store and use secrets securely
- Rely on a centralized identity provider
- Audit and rotate credentials regularly

**Detection**
- Configure service and application logging
- Analyze logs, findings, and metrics centrally
- Automate response to events
- Implement actionable security events

**Infrastructure Protection**
- Create network layers
- Control traffic at all layers
- Automate network protection
- Implement inspection and protection

**Data Protection**
- Identify and classify your data
- Protect data at rest
- Protect data in transit
- Automate data protection
- Prepare for incident response

**Incident Response**
- Ensure personnel know how to respond to an incident
- Automate containment capability
- Identify forensic capabilities
- Automate recovery capability
- Pre-provision access and tools

## Reliability

The reliability pillar focuses on workloads performing their intended functions and how to recover quickly from failure to meet demands. Key topics include distributed system design, recovery planning, and adapting to changing requirements.

### Design Principles

**Automatically recover from failure**
By monitoring a workload for key performance indicators (KPIs), you can trigger automation when a threshold is breached.

**Test recovery procedures**
In an on-premises environment, testing is often conducted to prove that the workload works in a particular scenario. Testing is not typically used to validate recovery strategies.

**Scale horizontally to increase aggregate workload availability**
Replace one large resource with multiple small resources to reduce the impact of a single failure on the overall workload.

**Stop guessing capacity**
A common cause of failure in on-premises workloads is resource saturation, when the demands placed on a workload exceed the capacity of that workload.

**Manage change in automation**
Changes to your infrastructure should be made using automation. The changes that need to be managed include changes to the automation, which then can be tracked and reviewed.

### Best Practices

**Foundations**
- Manage service quotas and constraints
- Plan your network topology
- Design your workload service architecture
- Design interactions in a distributed system to prevent failures
- Design interactions in a distributed system to mitigate or withstand failures

**Workload Architecture**
- Design your workload to withstand component failures
- Design your workload to withstand high-availability, multi-AZ, and multi-region scenarios
- Implement loosely coupled dependencies
- Design interactions in a distributed system to prevent failures
- Design interactions in a distributed system to mitigate or withstand failures

**Change Management**
- Monitor workload resources
- Design your workload to adapt to changes in demand
- Implement change
- Back up data
- Use fault isolation to protect your workload

**Failure Management**
- Monitor workload resources
- Design your workload to withstand component failures
- Test reliability
- Plan for disaster recovery (DR)
- Implement change

## Performance Efficiency

The performance efficiency pillar focuses on structured and streamlined allocation of IT and computing resources. Key topics include selecting resource types and sizes optimized for workload requirements, monitoring performance, and maintaining efficiency as business needs evolve.

### Design Principles

**Democratize advanced technologies**
Make advanced technology implementation easier for your team by delegating complex tasks to your cloud vendor.

**Go global in minutes**
Deploying your workload in multiple AWS Regions around the world allows you to provide lower latency and a better experience for your customers at minimal cost.

**Use serverless architectures**
Serverless architectures remove the need for you to run and maintain physical servers for traditional compute activities.

**Experiment more often**
With virtual and automatable resources, you can quickly carry out comparative testing using different types of instances, storage, or configurations.

**Consider mechanical sympathy**
Understand how cloud services are consumed and always use the technology approach that aligns best with your workload goals.

### Best Practices

**Architecture Selection**
- Understand the available cloud services and resources
- Define a process for architectural choices
- Factor cost requirements into decisions
- Use policies or reference architectures
- Use guidance from your cloud provider or an appropriate partner

**Compute and Hardware**
- Select the best compute solution for your workload
- Understand the available compute configuration options
- Collect compute-related metrics
- Determine the required configuration by right-sizing
- Use the available elasticity of resources

**Data Management**
- Select the best performing data store for your workload
- Understand how consistency affects performance
- Collect data store performance metrics
- Determine the required configuration by right-sizing
- Use the available elasticity of resources

**Networking and Content Delivery**
- Understand how networking impacts performance
- Evaluate available networking features
- Choose appropriate dedicated connectivity or VPN for your workload
- Use load balancing to distribute traffic across multiple resources
- Choose appropriate protocols

**Process and Culture**
- Establish key performance indicators (KPIs) to measure workload performance
- Use monitoring to understand performance over time
- Proactively improve performance
- Use automation to proactively remediate performance issues

## Cost Optimization

The cost optimization pillar focuses on avoiding unnecessary costs. Key topics include understanding spending over time and controlling fund allocation, selecting resources of the right type and size, and scaling to meet business needs without overspending.

### Design Principles

**Implement cloud financial management**
To achieve financial success and accelerate business value realization in the cloud, invest in Cloud Financial Management and Cost Optimization.

**Adopt a consumption model**
Pay only for the computing resources you consume, and increase or decrease usage depending on business requirements.

**Measure overall efficiency**
Measure the business output of the workload and the costs associated with delivery. Use this data to make informed decisions about future resource investments.

**Stop spending money on undifferentiated heavy lifting**
AWS does the heavy lifting of data center operations like racking, stacking, and powering servers. It also removes the operational burden of managing operating systems and applications with managed services.

**Analyze and attribute expenditure**
The cloud makes it easier to accurately identify the cost and usage of workloads, which then allows transparent attribution of IT costs to revenue streams and individual workload owners.

### Best Practices

**Practice Cloud Financial Management**
- Establish a cost optimization function
- Establish a partnership between finance and technology
- Establish cloud budgets and forecasts
- Implement cost awareness in your organizational processes
- Report and notify on cost optimization
- Monitor cost proactively
- Keep up to date with new service releases

**Expenditure and Usage Awareness**
- Govern usage
- Monitor cost and usage
- Decommission resources
- Evaluate new services

**Cost-Effective Resources**
- Evaluate cost when selecting services
- Select the correct resource type, size, and number
- Select the best pricing model
- Plan for data transfer charges

**Manage Demand and Supply Resources**
- Perform analysis on the workload demand
- Implement a buffer or throttle to manage demand
- Supply resources dynamically

**Optimize Over Time**
- Review and analyze this workload regularly
- Implement a process to evaluate new services
- Implement a process to evaluate the workload and implement optimization

## Sustainability

The sustainability pillar focuses on environmental impacts, especially energy consumption and efficiency, since they are important levers for architects to inform direct action to reduce resource usage.

### Design Principles

**Understand your impact**
Establish performance indicators, evaluate improvements, and estimate the impact of proposed changes over the full lifecycle of a workload.

**Establish sustainability goals**
Establish long-term sustainability goals for each workload, model return on investment (ROI), and give owners the resources they need to invest in sustainability goals.

**Maximize utilization**
Right size each workload to maximize the energy efficiency of the underlying hardware and minimize idle resources.

**Anticipate and adopt new, more efficient hardware and software offerings**
Design for flexibility to adopt new technologies over time, and support the upstream improvements your partners and suppliers make to help you reduce the impact of your cloud workloads.

**Use managed services**
Managed services shift responsibility for maintaining high average utilization and sustainability optimization of the deployed hardware to AWS.

**Reduce the downstream impact of your cloud workloads**
Reduce the amount of energy or resources required to use your services and reduce the need for your customers to upgrade their hardware.

### Best Practices

**Region Selection**
- Choose Regions near your users for reduced latency
- Choose Regions based on your sustainability goals
- Use Regions with published PUE and carbon intensity information

**User Behavior Patterns**
- Scale infrastructure with user load
- Align SLA with sustainability goals
- Eliminate or reduce the need for customers to upgrade hardware

**Software and Architecture Patterns**
- Optimize software and architecture for asynchronous and scheduled jobs
- Remove or refactor workload components with low or no use
- Optimize areas of code that consume the most time or resources
- Optimize impact on customer devices and equipment
- Use software patterns and architectures that best support data access and storage patterns

**Data Patterns**
- Implement a data classification policy
- Use technologies that support data access and storage patterns
- Use lifecycle policies to delete unnecessary data
- Minimize over-provisioning in block storage
- Remove unneeded data in snapshots

**Hardware Patterns**
- Use the minimum amount of hardware to meet your needs
- Use instance types with the least impact
- Use managed services
- Optimize your use of hardware-based compute accelerators

**Development and Deployment Patterns**
- Adopt methods that can rapidly introduce sustainability improvements
- Keep your workload up-to-date
- Increase utilization of build environments
- Use managed device farms for testing

## Well-Architected Tool

The AWS Well-Architected Tool is available at no charge in the AWS Management Console. It provides a central place for architectural best practices, measurement, and improvement.

### Features

**Workload Documentation**
Document your workloads and applications in the tool to track architectural decisions and improvements over time.

**Review Process**
Answer a series of questions about your architecture across the six pillars to identify areas for improvement.

**Improvement Plans**
Receive prioritized improvement plans with specific guidance on how to address identified issues.

**Milestone Tracking**
Track your progress over time by creating milestones that capture the state of your workload at specific points.

**Custom Lenses**
Create custom lenses to address specific industry requirements or organizational standards.

**Reporting**
Generate reports to share findings and track improvements across your organization.

### Best Practices for Using the Tool

**Regular Reviews**
Conduct Well-Architected reviews regularly, especially when making significant changes to your architecture.

**Cross-Functional Teams**
Include team members from different disciplines (development, operations, security, etc.) in the review process.

**Action-Oriented**
Focus on actionable improvements rather than just identifying issues.

**Continuous Improvement**
Use the tool as part of a continuous improvement process rather than a one-time assessment.

## Implementation Strategies

### Getting Started

**Assess Current State**
Begin by documenting your current architecture and conducting an initial Well-Architected review.

**Prioritize Improvements**
Focus on high-impact, low-effort improvements first to build momentum and demonstrate value.

**Create a Roadmap**
Develop a roadmap for implementing improvements across all six pillars.

**Establish Governance**
Create processes and governance structures to ensure ongoing adherence to Well-Architected principles.

### Organizational Adoption

**Training and Education**
Provide training on Well-Architected principles to all relevant team members.

**Integration with Processes**
Integrate Well-Architected reviews into your existing development and deployment processes.

**Metrics and KPIs**
Establish metrics to track your progress in implementing Well-Architected principles.

**Culture Change**
Foster a culture of continuous improvement and architectural excellence.

## Common Anti-Patterns

### Operational Excellence Anti-Patterns
- Manual processes that could be automated
- Lack of monitoring and observability
- No disaster recovery planning
- Insufficient documentation

### Security Anti-Patterns
- Overly permissive access controls
- Unencrypted data at rest or in transit
- Lack of security monitoring
- Hardcoded credentials

### Reliability Anti-Patterns
- Single points of failure
- Lack of redundancy
- No automated recovery mechanisms
- Insufficient testing of failure scenarios

### Performance Efficiency Anti-Patterns
- Over-provisioned resources
- Inappropriate instance types
- Lack of performance monitoring
- No optimization based on usage patterns

### Cost Optimization Anti-Patterns
- Unused or underutilized resources
- Inappropriate pricing models
- Lack of cost monitoring
- No regular cost reviews

### Sustainability Anti-Patterns
- Inefficient resource utilization
- Lack of sustainability metrics
- No consideration of environmental impact
- Overprovisioning without justification

## Conclusion

The AWS Well-Architected Framework provides a comprehensive approach to building and operating workloads in the cloud. By following the principles and best practices outlined in the six pillars, organizations can create systems that are secure, reliable, performant, cost-effective, operationally excellent, and sustainable.

Regular application of the framework through reviews and continuous improvement helps ensure that architectures evolve with changing requirements and take advantage of new AWS capabilities. The framework is not a one-time checklist but rather a continuous journey toward architectural excellence.
