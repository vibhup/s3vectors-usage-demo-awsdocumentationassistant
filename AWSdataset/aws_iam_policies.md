# What is IAM?

AWS Identity and Access Management (IAM) is a web service that helps you securely control access to AWS
resources. With IAM, you can manage permissions that control which AWS resources users can
access. You use IAM to control who is authenticated (signed in) and authorized (has
permissions) to use resources. IAM provides the infrastructure necessary to control
authentication and authorization for your AWS accounts.

## Identities

When you create an AWS account, you begin with one sign-in identity that has complete access to all AWS services
and resources in the account. This identity is called the AWS account *root user* and is accessed by
signing in with the email address and password that you used to create the account. We
strongly recommend that you don't use the root user for your everyday tasks. Safeguard your root user credentials and use them to
perform the tasks that only the root user can perform.

Use IAM to set up other identities in addition to your
root user, such as administrators, analysts, and developers, and grant them access to the resources
they need to succeed in their tasks.

## Access management

After a user is set up in IAM, they use their sign-in credentials to authenticate with
AWS. Authentication is provided by matching the sign-in credentials to a principal (an
IAM user, AWS STS federated principal, IAM role, or application) trusted by the AWS account. Next, a
request is made to grant the principal access to resources. Access is granted in response to an
authorization request if the user has been given permission to the resource. For example, when
you first sign in to the console and are on the console Home page, you aren't accessing a
specific service. When you select a service, the request for authorization is sent to that
service and it looks to see if your identity is on the list of authorized users, what policies
are being enforced to control the level of access granted, and any other policies that might be
in effect. Authorization requests can be made by principals within your AWS account or from
another AWS account that you trust.

Once authorized, the principal can take action or perform operations on resources in your
AWS account. For example, the principal could launch a new Amazon Elastic Compute Cloud instance, modify
IAM group membership, or delete Amazon Simple Storage Service buckets.

## Service availability

IAM, like many other AWS services, is eventually consistent.
IAM achieves high availability by replicating data across multiple servers within
Amazon's data centers around the world. If a request to change some data is successful,
the change is committed and safely stored. However, the change must be replicated across
IAM, which can take some time. Such changes include creating or updating users,
groups, roles, or policies. We recommend that you do not include such IAM changes in the
critical, high-availability code paths of your application. Instead, make IAM changes in
a separate initialization or setup routine that you run less frequently. Also, be sure
to verify that the changes have been propagated before production workflows depend on
them.

## Service cost information

AWS Identity and Access Management (IAM), AWS IAM Identity Center and AWS Security Token Service (AWS STS) are features of your AWS account offered at no additional charge. You are
charged only when you access other AWS services using your IAM users or AWS STS temporary security credentials.

IAM Access Analyzer external access analysis is offered at no additional charge. However, you will incur charges for unused access analysis and customer policy checks.

## Integration with other AWS services

IAM is integrated with many AWS services. For a list of AWS services that work with IAM and the IAM features the services support, see AWS services that work with
IAM.

# Policies and permissions in AWS Identity and Access Management

Manage access in AWS by creating policies and attaching them to IAM identities (users,
groups of users, or roles) or AWS resources. A policy is an object in AWS that, when
associated with an identity or resource, defines their permissions. AWS evaluates these
policies when an IAM principal (user or role) makes a request. Permissions in the policies
determine whether the request is allowed or denied. Most policies are stored in AWS as JSON
documents. AWS supports seven types of policies: identity-based policies, resource-based
policies, permissions boundaries, AWS Organizations service control policies (SCPs), AWS Organizations resource control
policies (RCPs), access control lists (ACLs), and session policies.

IAM policies define permissions for an action regardless of the method that you use to
perform the operation. For example, if a policy allows the GetUser action, then a user with that policy can
get user information from the AWS Management Console, the AWS CLI, or the AWS API. When you create an IAM
user, you can choose to allow console or programmatic access. If console access is allowed, the
IAM user can sign in to the console using their sign-in credentials. If programmatic access is
allowed, the user can use access keys to work with the CLI or API.

## Policy types

The following policy types, listed in order from most frequently used to less frequently
used, are available for use in AWS. For more details, see the sections below for each policy
type.

* **Identity-based policies** – Attach managed
  and inline policies to IAM identities (users, groups to
  which users belong, or roles). Identity-based policies grant permissions to an
  identity.
* **Resource-based policies** – Attach inline policies to resources. The most
  common examples of resource-based policies are Amazon S3 bucket policies and IAM role trust
  policies. Resource-based policies grant permissions to the principal that is specified in
  the policy. Principals can be in the same account as the resource or in other
  accounts.
* **Permissions boundaries** – Use a managed policy as the permissions boundary
  for an IAM entity (user or role). That policy defines the maximum permissions that the
  identity-based policies can grant to an entity, but does not grant permissions.
  Permissions boundaries do not define the maximum permissions that a resource-based policy
  can grant to an entity.
* **AWS Organizations SCPs**
  – Use an AWS Organizations service control policy (SCP) to define the maximum permissions
  for IAM users and IAM roles within accounts in your organization or organizational
  unit (OU). SCPs limit permissions that identity-based policies or resource-based policies
  grant to IAM users or IAM roles within the account. SCPs do not grant
  permissions.
* **AWS Organizations RCPs**
  – Use an AWS Organizations resource control policy (RCP) to define the maximum permissions
  for resources within accounts in your organization or organizational unit (OU). RCPs limit
  permissions that identity-based and resource-based policies can grant to resources in
  accounts within your organization. RCPs do not grant permissions.
* **Access control lists (ACLs)** – Use ACLs to control which principals in other accounts
  can access the resource to which the ACL is attached. ACLs are similar to resource-based
  policies, although they are the only policy type that does not use the JSON policy
  document structure. ACLs are cross-account permissions policies that grant permissions to
  the specified principal. ACLs cannot grant permissions to entities within the same
  account.
* **Session policies** – Pass advanced session policies when you use the
  AWS CLI or AWS API to assume a role or a federated user. Session policies limit the
  permissions that the role or user's identity-based policies grant to the session. Session
  policies limit permissions for a created session, but do not grant permissions.

### Identity-based policies

Identity-based policies are JSON permissions policy documents that control what actions
an identity (users, groups of users, and roles) can perform, on which resources, and under
what conditions. Identity-based policies can be further categorized:

* **Managed policies** – Standalone identity-based policies that you can attach to
  multiple users, groups, and roles in your AWS account. There are two types of managed
  policies:

  + **AWS managed policies** – Managed
    policies that are created and managed by AWS.
  + **Customer managed policies** – Managed
    policies that you create and manage in your AWS account. Customer managed policies
    provide more precise control over your policies than AWS managed policies.
* **Inline policies** – Policies that you add directly to a single user, group,
  or role. Inline policies maintain a strict one-to-one relationship between a policy and
  an identity. They are deleted when you delete the identity.

### Resource-based policies

Resource-based policies are JSON policy documents that you attach to a resource such as
an Amazon S3 bucket. These policies grant the specified principal permission to perform specific
actions on that resource and defines under what conditions this applies. Resource-based
policies are inline policies. There are no managed resource-based policies.

To enable cross-account access, you can specify an entire account or IAM entities in
another account as the principal in a resource-based policy. Adding a cross-account
principal to a resource-based policy is only half of establishing the trust relationship.
When the principal and the resource are in separate AWS accounts, you must also use an
identity-based policy to grant the principal access to the resource. However, if a
resource-based policy grants access to a principal in the same account, no additional
identity-based policy is required.

The IAM service supports only one type of resource-based policy called a role
*trust policy*, which is attached to an IAM role. An
IAM role is both an identity and a resource that supports resource-based policies. For
that reason, you must attach both a trust policy and an identity-based policy to an IAM
role. Trust policies define which principal entities (accounts, users, roles, and federated
users) can assume the role.

### IAM permissions boundaries

A permissions boundary is an advanced feature in which you set the maximum permissions
that an identity-based policy can grant to an IAM entity. When you set a permissions
boundary for an entity, the entity can perform only the actions that are allowed by both its
identity-based policies and its permissions boundaries. If you specify a role session or
user in the principal element of a resource-based policy, an explicit allow in the
permission boundary is not required. However, if you specify a role ARN in the principal
element of a resource-based policy, an explicit allow in the permission boundary is
required. In both cases, an explicit deny in the permission boundary is effective. An
explicit deny in any of these policies overrides the allow.

### AWS Organizations service control policies (SCPs)

If you enable all features in an organization, then you can apply service control
policies (SCPs) to any or all of your accounts. SCPs are JSON policies that specify the
maximum permissions for IAM users and IAM roles within accounts of an organization or
organizational unit (OU). The SCP limits permissions for principals in member accounts,
including each AWS account root user. An explicit deny in any of these policies overrides an allow in
other policies.
