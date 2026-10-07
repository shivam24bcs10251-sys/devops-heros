# EC2 — compute

Amazon EC2 runs virtual machines called instances. It supplies compute capacity; operating-system configuration and application deployment remain part of the project.

| Assignment topic | Explanation |
|---|---|
| AMI | A machine image containing an operating system and launch configuration. Select an image available in the region and matching the instance's CPU architecture. |
| Instance types | Families provide different balances of CPU, memory, storage and networking. A small general-purpose instance suits a short classroom web-server lab. CPU-credit behavior matters for burstable types. |
| Key pairs | A public key can be placed on a Linux instance to allow SSH using the matching private key. A key pair is unnecessary when the lab uses boot-time user data and verifies HTTP without SSH. |
| Security groups | Stateful allow rules attached to network interfaces. Restrict inbound access to the required protocol, port and source. Return traffic for an allowed connection is tracked automatically. |
| EBS | Persistent block volumes attached to EC2. A root volume holds the OS; encryption and delete-on-termination are useful explicit lab settings. Storage billing can continue for volumes left behind. |
| Public IP | Allows internet communication when the subnet route, gateway and security rules also permit it. An ordinary assigned public IPv4 address can change after stop/start. |
| Private IP | Used within the VPC and reachable private networks. The primary private address persists across stop/start while the network interface exists. |
| Lifecycle | Instances move through pending, running, stopping/stopped, shutting-down and terminated states. Stopping is different from terminating, and it does not remove every associated billable resource. |

## Typical launch workflow

Choose a region and AMI; select an instance type; create or choose a subnet and security group; configure the root volume and user data; launch; wait for status checks; verify the application; terminate and verify cleanup. Terraform represents these choices as resources, variables and references.

For Session 19, a separate VPC and subnet keep the lab isolated from existing infrastructure. A public route makes the demonstration HTTP endpoint reachable, and its security group should admit port 80 only from the student's current public IPv4 address. No SSH private key needs to be created or committed.

## Common use cases

Web servers, application workers, development environments, batch computation and custom software requiring OS-level control. Containers can run on EC2, but using EC2 alone does not automatically provide Kubernetes orchestration or managed database behavior.

## Sources

[What is EC2?](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html) · [Instance lifecycle](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html) · [Security groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html) · [Amazon EBS](https://docs.aws.amazon.com/ebs/latest/userguide/what-is-ebs.html)
