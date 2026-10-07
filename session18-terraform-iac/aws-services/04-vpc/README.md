# VPC — networking

A Virtual Private Cloud is a logically isolated network in an AWS region. A VPC contains subnets and routing/security configuration; it is not itself an application server.

| Assignment topic | Explanation |
|---|---|
| CIDR | An address range written as a prefix, such as `10.18.0.0/16`. Subnet ranges must fit inside the VPC range and must not overlap each other. |
| Subnet | An address range in one Availability Zone. A VPC can contain multiple subnets across zones. |
| Route table | Rules choosing the target for a destination range. A route to `0.0.0.0/0` is the IPv4 default route. Associate the intended route table with the subnet. |
| Internet gateway | A VPC gateway used for internet communication. A public route alone is insufficient: an IPv4 instance also needs a public address and permissive security rules for the required traffic. |
| NAT gateway | Enables outbound connections from private IPv4 resources while preventing unsolicited inbound connections through it. It has usage charges and is unnecessary for this single public-subnet classroom lab. |
| Security group | Stateful allow rules applying at the network-interface/resource level. Restrict inbound HTTP to the student's current address; no SSH rule is required for a user-data deployment. |
| Network ACL | Stateless subnet-level allow/deny rules evaluated in number order. Both directions, including return ephemeral ports, must be considered. |
| Public subnet | Has a route to an internet gateway. Instances do not become internet reachable unless their addressing and security settings also allow it. |
| Private subnet | Does not have a direct default route to an internet gateway. It may use NAT, VPC endpoints or private connectivity for selected communication. |

## Example lab network

A `/16` VPC contains one `/24` public subnet. An internet gateway and associated route table provide the default route. One EC2 network interface has a public IPv4 address and a security group accepting HTTP only from an explicit `/32` source. The web server starts through user data. These resources are created and destroyed together by Terraform.

A production design normally separates tiers and uses more than one Availability Zone. This teaching exercise is intentionally a single-instance architecture; it does not demonstrate high availability.

## Common use cases

Isolating application environments, separating web/application/database tiers, connecting on-premises networks privately and controlling access to managed services.

## Sources

[Create a VPC](https://docs.aws.amazon.com/vpc/latest/userguide/create-vpc.html) · [Subnets](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html) · [Route tables](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html) · [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
