# Permissions needed to execute Session 18

The default local profile currently authenticates as IAM user `satyam`, but the real Terraform apply was denied at `s3:CreateBucket`. Login success is not proof of resource permissions.

[Policy for administrator review](terraform-s3-lab-policy.json) grants bucket lifecycle/configuration actions only on the `devops-session18-` prefix. It deliberately grants no global bucket listing, object access, IAM mutation or EC2 permission. This lab creates an empty bucket, so object deletion permissions are unnecessary.

An AWS account administrator can attach this policy to the intended lab identity, or provide an already authorized local profile/role. Existing permission boundaries, session policies, resource policies or organization controls can still restrict the effective permission. This policy has not been attached automatically.

After access changes, rerun `terraform plan -out=create.tfplan` and apply the newly saved plan. Successful creation must be followed by AWS verification, screenshots and `terraform destroy`. The current denied apply is evidence of the access limitation, not a completed cloud demo.
