# S3 — object storage

Amazon S3 stores objects inside buckets. It is object storage rather than a normal mounted block disk. Applications typically access it through HTTPS APIs or the AWS CLI.

| Assignment topic | Explanation |
|---|---|
| Bucket | A regional container for objects. General-purpose bucket names must be globally unique within the AWS partition. The lab therefore uses a unique suffix, rather than the generic name `demo`. |
| Object | Data plus metadata and a key identifying its location in a bucket. Prefixes organize keys; the console's folder display does not make S3 a traditional directory filesystem. |
| Storage classes | Classes balance access patterns, retrieval behavior and cost. Standard suits frequent access; Intelligent-Tiering adjusts tiers; infrequent-access and archive choices require attention to retrieval and minimum-duration rules. |
| Versioning | Keeps different versions of an object key. A delete can add a delete marker rather than removing older data. Deleting a versioned bucket requires removing all versions and delete markers. |
| Lifecycle policy | Rules transition or expire objects, including noncurrent versions, after defined conditions. Review their effect before using them on valuable data. |
| Encryption | Server-side options include S3-managed AES256 keys and KMS-based options. Encryption protects data at rest; use TLS for transport. KMS requires its own permissions and can add charges. |
| Bucket policy | Resource-based JSON permissions covering principals, actions, object/bucket resources and conditions. A policy can enforce secure transport or authorize a specific cross-account role. |

## Security and the Terraform demo

Public access is blocked explicitly. The demo uses AES256 server-side encryption and enables versioning. Credentials remain outside Git. It creates an empty lab bucket, verifies AWS configuration and destroys it after taking evidence.

`force_destroy=false` means Terraform will not silently empty a bucket with unexpected contents. This is intentional: if objects were added, inspect and deliberately remove the appropriate versions before destroying the lab bucket. An S3 bucket's existence does not mean objects are public, and server-side encryption does not grant access.

## Common use cases

Application assets, backups, data lakes, analytics input/output, log archives and Terraform remote state. State may contain sensitive values; a production remote backend needs access controls and locking in addition to a bucket.

## Sources

[S3 user guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) · [Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html) · [Storage classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html) · [S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
