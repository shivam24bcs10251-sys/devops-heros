# DynamoDB and RDS — database services

DynamoDB provides a managed NoSQL key-value/document database. RDS manages relational database infrastructure. Choose according to data relationships, query patterns, consistency requirements and operating needs, rather than treating them as interchangeable storage.

## DynamoDB

| Topic | Explanation |
|---|---|
| NoSQL | Data is accessed through keys and supported indexes rather than arbitrary relational joins. Model the application's access patterns before selecting keys. |
| Table | A collection of items sharing a primary-key structure. Capacity can use on-demand or provisioned settings. |
| Item | A record identified by its primary key. Different items can have different non-key attributes. |
| Attribute | A named value, such as user ID, order time, status or a document field. |
| Partition key | Required part of the primary key, used to distribute and identify data. Avoid heavily concentrating traffic on a small set of values. |
| Sort key | Optional second primary-key component that distinguishes items sharing a partition key and enables ordered range queries within it. |
| Use cases | Session stores, shopping carts, game state, event metadata and high-throughput applications with known access patterns. |

For orders, `customer_id` as partition key and `order_timestamp` as sort key can support querying one customer's orders by time. Additional query requirements may need secondary indexes or a different data model. Backups, encryption, capacity and access controls still require deliberate configuration.

## RDS

| Topic | Explanation |
|---|---|
| Relational database | Structured tables, relationships and SQL capabilities determined by the selected engine. |
| Supported engines | RDS offers engines including PostgreSQL, MySQL, MariaDB, Oracle, SQL Server and Db2; Aurora is a related managed relational option with its own architecture. Availability and versions depend on region and offering. |
| DB instance | Managed database compute/storage configuration. Instance class, storage and engine settings affect performance and cost. |
| Security | Place databases in appropriate VPC subnets, limit security-group sources, use encrypted storage and TLS, and manage credentials through a supported secret mechanism. |
| Backups | Automated backups and snapshots support recovery within their configured retention and supported capabilities. Verify restoration, not just backup creation. |
| Multi-AZ | Deployment options provide redundancy and failover; a classic standby is not the same as a read replica. Exact behavior differs between Multi-AZ instances and clusters. |
| Read replicas | Copies used for read scaling and selected recovery/migration workflows, usually with replication lag and engine-specific behavior. They are not a replacement for every high-availability feature. |
| Use cases | Transactional business applications, relational reporting and applications depending on a supported SQL engine. |

## Comparison

| Choice | DynamoDB | RDS |
|---|---|---|
| Data model | Key-value/document | Relational tables |
| Main query design | Keys and indexes | Engine-supported SQL |
| Typical modeling focus | Explicit access patterns | Relationships and constraints |
| Operating choices | Capacity, keys/indexes, backup settings | Engine, instance/storage, backups and availability |

This is a research task. Creating database instances is not needed for Sessions 18 or 19's suggested infrastructure lab.

## Sources

[What is DynamoDB?](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) · [DynamoDB core components](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html) · [What is RDS?](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html) · [RDS Multi-AZ](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)
