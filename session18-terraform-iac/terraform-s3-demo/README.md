# Terraform S3 demo

The supplied example has been corrected: Terraform outputs do not accept a `type` argument, and a globally unique bucket name replaces the invalid generic `demo` default. The AWS provider is pinned to 6.67.0 and its dependency lock file is committed. `provider.tf` uses the existing local AWS profile; keys are never stored in Terraform variables.

The bucket has explicit public-access blocking, AES256 server-side encryption and versioning. `force_destroy=false` protects unexpected objects: an empty lab bucket can be destroyed normally. Resources refer to the bucket ID, so Terraform creates the bucket first and deletes dependent configurations before the bucket.

```bash
terraform init
terraform fmt
terraform validate
terraform plan -out=create.tfplan
terraform apply create.tfplan
terraform show
terraform output
terraform state list
terraform plan -detailed-exitcode
terraform destroy -auto-approve
terraform state list
```

The final destroy is required by this assignment. State and saved plans stay local and ignored by Git. The committed `terraform.tfvars` contains only region, profile name and a disposable bucket name; use a new globally unique name for another run. See the [session submission](../README.md) for actual execution evidence and the AWS research deliverables.
