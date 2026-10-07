# IAM — governance and access control

IAM determines which identities can perform which actions on AWS resources. Authentication establishes identity; authorization evaluates whether the requested action is permitted.

| Concept | Meaning and practical example |
|---|---|
| User | An identity belonging to an AWS account. It can have console access or access keys. A human's preferred access pattern is federation/SSO with temporary credentials. |
| Group | A collection of IAM users with shared permission policies, such as a student-lab group. Groups are not identities that can assume roles. |
| Role | An assumable identity with a trust policy and permission policies. STS issues temporary credentials; an EC2 application can use a role instead of embedded keys. |
| Policy | A JSON document describing allowed or denied actions, resources and conditions. Identity policies attach to users/groups/roles; resource policies attach to supported resources such as S3 buckets. |
| Permission | Authorization for an action on a resource, for example `s3:GetObject` on one bucket's objects. Explicit denies override applicable allows; boundaries and organization policies can further restrict access. |
| Least privilege | Grant only the actions, resource scope and conditions required for the task. Terraform needs lifecycle/read operations, not just permission to create a resource. |

## Applying IAM to this assignment

`aws sts get-caller-identity` confirms that a configured identity can authenticate. It does not prove that the identity can create S3 buckets or EC2 instances. A denied `ec2:DescribeVpcs` means a valid login still lacks a required resource permission.

A Session 18 policy should cover the lab bucket's creation, tagging, configuration reads/writes and deletion. Bucket actions use a bucket ARN; object actions use an ARN ending in `/*`. Restrict the bucket name prefix to `devops-session18-` where possible. Session 19 additionally needs EC2/VPC lifecycle and describe permissions. Role trust controls who can assume a role; permission policies control what the assumed role can do.

## Best practices

Use temporary credentials, MFA and narrowly scoped roles. Protect the root user, reserve it for root-only operations and avoid creating root access keys. Store credentials in the supported AWS credential configuration, not source files, Terraform variables, screenshots or commits. Review unused permissions and rotate/revoke compromised credentials. An administrator should grant missing access; a lab should not escalate its own permissions.

## Common use cases

A developer assumes a lab role, an EC2 workload reads selected S3 objects through an instance role, a CI runner uses an OIDC trust relationship, and a security reviewer has read-only visibility. These separate identities and scopes reduce the effect of a compromised credential.

## Sources

[IAM security best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) · [IAM policies and permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html) · [AWS CLI credential configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
