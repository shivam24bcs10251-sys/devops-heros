# Session 19 cloud mini-project

The supplied six-resource network example is extended into the assignment's complete proposed architecture: VPC, subnet, internet gateway, route table/association, security group, EC2 and S3 with three explicit bucket configuration resources. This produces eleven managed resources after a successful apply.

EC2 uses the latest matching Amazon-owned AL2023 x86_64 AMI and a small t3.micro instance. User data installs Nginx and a Session 19 page. HTTP is limited to the current student's IPv4 /32; no SSH or unused HTTPS port is opened. IMDSv2 is required. The 8 GiB gp3 root volume is encrypted and deleted on termination. S3 blocks public access, uses AES256 encryption and enables versioning. No IAM role or key-pair creation is needed.

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit your current HTTP source IPv4 /32, unique bucket name and AWS profile.
terraform init
terraform fmt
terraform validate
terraform test
terraform plan -out=create.tfplan
terraform apply create.tfplan
terraform show
terraform output
terraform state list
bash verify.sh
terraform plan -detailed-exitcode
terraform plan -destroy -out=destroy.tfplan
terraform apply destroy.tfplan
terraform state list
```

`terraform test` here uses a mocked provider solely to check configuration/security contracts without AWS access. It is not evidence that AWS resources exist. The live plan/apply and HTTP verification remain separate operations. A no-change plan returns detailed exit code 0; proposed changes return 2; errors return 1.

Resource references establish dependencies. EC2 explicitly waits for the subnet's public route association before boot-time package installation. The S3 bucket is independent of the web application's serving path; its outputs and AWS configuration checks demonstrate object-storage provisioning, not app-to-S3 integration.

State and saved plans remain local and ignored. The dependency lock file is committed. The supplied example tfvars contains only placeholder values; real lab tfvars are not committed. EC2, EBS and public IPv4 can incur charges while provisioned; cleanup removes the resources created by this project. See the [session submission](../README.md) for architecture, actual execution status and screenshots.
