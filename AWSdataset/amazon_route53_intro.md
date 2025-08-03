# What is Amazon Route 53?

Amazon Route 53 is a highly available and scalable Domain Name System (DNS) web service. You can use Route 53 to perform three main functions
in any combination: domain registration, DNS routing, and health checking.

If you choose to use Route 53 for all three functions, be sure to follow the order below:

**1. Register domain names**
:   Your website needs a name, such as example.com. Route 53 lets you register a name for your website or web application,
    known as a *domain name*.

**2. Route internet traffic to the resources for your domain**
:   When a user opens a web browser and enters your domain name (example.com) or subdomain name (acme.example.com) in the address bar,
    Route 53 helps connect the browser with your website or web application.

**3. Check the health of your resources**
:   Route 53 sends automated requests over the internet to a resource, such as a web server, to verify that it's reachable, available,
    and functional. You also can choose to receive notifications when a resource becomes unavailable and choose to route internet traffic
    away from unhealthy resources.

## Other Route 53 features

In addition to being a Domain Name System (DNS) web service, Route 53 offers the following
features:

**Route 53 Resolver**
:   Get recursive DNS for your Amazon VPCs in AWS Regions, VPCs in AWS Outposts racks, or any other on-premises networks.
    Create conditional forwarding rules and
    Route 53 endpoints to resolve custom names mastered in Route 53 private hosted zones or in your on-premises DNS servers.

**Amazon Route 53 Resolver on Outposts**
:   Connect Route 53 Resolver on Outpost racks with DNS servers in your on-premises data
    centers through Route 53 Resolver endpoints. This enables resolution of DNS queries between
    the Outposts racks and your other on-premises resources.

**Route 53 Resolver DNS Firewall**
:   Protect your recursive DNS queries within the Route 53 Resolver. Create domain lists and build firewall rules that filter outbound DNS traffic against these rules.

**Traffic Flow**
:   Easy-to-use and cost-effective global traffic management: route end users to the best endpoint for your application based on geoproximity, latency, health, and other considerations.

**Amazon Route 53 Profiles**
:   With Route 53 Profiles, you can apply and manage DNS-related Route 53 configurations across many VPCs and in different AWS account.

## Core DNS Concepts

### Domain Name System (DNS)
DNS is a hierarchical naming system that translates human-readable domain names (like example.com) into IP addresses (like 192.0.2.1) that computers use to identify each other on the network.

### Hosted Zones
A hosted zone is a container for DNS records for a particular domain. For example, you might create a hosted zone for example.com and use it to store DNS records for example.com and its subdomains.

### DNS Records
DNS records contain information about how you want to route traffic for a domain. Each record includes:
- Name (the domain or subdomain name)
- Type (such as A, AAAA, CNAME, MX)
- Value (such as an IP address)
- TTL (Time to Live)

### Common Record Types

**A Record**
Maps a domain name to an IPv4 address.

**AAAA Record**
Maps a domain name to an IPv6 address.

**CNAME Record**
Maps a domain name to another domain name (canonical name).

**MX Record**
Specifies mail servers responsible for accepting email for the domain.

**NS Record**
Identifies the name servers for the hosted zone.

**SOA Record**
Provides information about the domain and the hosted zone.

**TXT Record**
Contains text information for sources outside your domain.

## Routing Policies

Route 53 supports several routing policies that determine how Route 53 responds to DNS queries:

### Simple Routing
Use when you have a single resource that performs a given function for your domain.

### Weighted Routing
Route traffic to multiple resources in proportions that you specify. Useful for load balancing and testing new versions of software.

### Latency-Based Routing
Route traffic based on the lowest network latency for your end user. Route 53 serves the resource from the AWS Region that provides the lowest latency.

### Failover Routing
Configure active-passive failover. Route 53 monitors the health of your primary resource and routes traffic to a backup resource when the primary is unavailable.

### Geolocation Routing
Route traffic based on the geographic location of your users. You can specify geographic locations by continent, country, or state.

### Geoproximity Routing
Route traffic based on the geographic location of your resources and, optionally, shift traffic from resources in one location to resources in another.

### Multivalue Answer Routing
Return multiple values in response to DNS queries. Route 53 returns only values for healthy resources.

## Health Checks

Route 53 health checks monitor the health and performance of your web applications, web servers, and other resources.

### Types of Health Checks

**HTTP/HTTPS Health Checks**
Monitor the health of web servers by sending HTTP or HTTPS requests.

**TCP Health Checks**
Monitor the health of resources by attempting to establish a TCP connection.

**Calculated Health Checks**
Monitor the health of multiple resources and determine the overall health based on the health of the individual resources.

**CloudWatch Alarm Health Checks**
Monitor the health of resources based on CloudWatch alarms.

### Health Check Features
- Configurable request intervals
- Failure threshold settings
- String matching for HTTP/HTTPS checks
- SNS notifications for health check failures
- Health check metrics in CloudWatch

## Domain Registration

Route 53 provides domain registration services for hundreds of top-level domains (TLDs).

### Domain Registration Process
1. Check domain availability
2. Register the domain
3. Configure DNS settings
4. Set up auto-renewal (optional)

### Domain Management Features
- Domain transfer to Route 53
- Domain transfer away from Route 53
- Domain renewal and auto-renewal
- Domain contact information updates
- Domain locking for security

## Route 53 Resolver

Route 53 Resolver provides recursive DNS resolution for your VPCs and on-premises networks.

### Resolver Features
- Automatic DNS resolution for VPC resources
- Conditional forwarding rules
- Inbound and outbound endpoints
- DNS query logging
- Integration with on-premises DNS servers

### Resolver Endpoints

**Inbound Endpoints**
Allow DNS resolvers on your on-premises network to resolve DNS queries for AWS resources.

**Outbound Endpoints**
Allow DNS queries originating in your VPCs to be resolved by DNS resolvers on your on-premises network.

## Security Features

### Access Control
- IAM policies for fine-grained access control
- Resource record set permissions
- Cross-account access for hosted zones

### DNS Security
- DNSSEC support for domain validation
- DNS Firewall for filtering malicious domains
- Query logging for security monitoring

### Compliance
- SOC, PCI DSS, and HIPAA compliance
- AWS CloudTrail integration for audit logging

## Monitoring and Logging

### CloudWatch Metrics
Route 53 provides CloudWatch metrics for:
- Query count by hosted zone
- Health check status
- Resolver query volume
- DNS Firewall rule matches

### Query Logging
Log DNS queries that Route 53 receives for your domains to help with:
- Security analysis
- Troubleshooting
- Compliance requirements

### Health Check Monitoring
- Real-time health check status
- Health check failure notifications
- Historical health check data

## Best Practices

### DNS Design
- Use appropriate TTL values for your records
- Implement health checks for critical resources
- Use alias records for AWS resources when possible
- Plan for DNS propagation delays

### Performance Optimization
- Use latency-based routing for global applications
- Implement geolocation routing for compliance requirements
- Use weighted routing for gradual deployments
- Configure appropriate health check intervals

### Security
- Enable DNSSEC where supported
- Use DNS Firewall to block malicious domains
- Monitor DNS query logs for suspicious activity
- Implement least privilege access policies

### Cost Optimization
- Use alias records to avoid charges for AWS resource queries
- Optimize health check frequency based on requirements
- Monitor usage and adjust configurations as needed

## Integration with AWS Services

### Elastic Load Balancing
Create alias records that route traffic to Application Load Balancers, Network Load Balancers, and Classic Load Balancers.

### CloudFront
Route traffic to CloudFront distributions using alias records for improved performance and reduced costs.

### S3 Website Hosting
Route traffic to S3 buckets configured for static website hosting.

### API Gateway
Route traffic to API Gateway endpoints for serverless applications.

### AWS Certificate Manager
Automatically validate domain ownership for SSL/TLS certificates.

## Common Use Cases

### Website Hosting
Route traffic to web servers or load balancers hosting your website or web application.

### Email Routing
Configure MX records to route email to your mail servers or email services.

### Global Load Balancing
Distribute traffic across multiple regions based on latency, geography, or health.

### Disaster Recovery
Implement failover routing to automatically redirect traffic during outages.

### Blue-Green Deployments
Use weighted routing to gradually shift traffic between different versions of your application.

### Subdomain Management
Organize different services or environments using subdomains with appropriate routing policies.
