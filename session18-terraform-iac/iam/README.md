# IAM access notes

The live Session 18 lab was completed on **15 October 2026**, through profile `scaler-sst` in AWS account `499567237930`, Sydney. The provider enforces that account with `allowed_account_ids`. Its temporary credentials come from the AWS CLI login cache and never appear in Terraform variables or screenshots.

The earlier 7 October default-profile attempt failed at `s3:CreateBucket`. That historical failure is retained in the session evidence. It was resolved by selecting the authorized Scaler account, without changing or reusing the other account's resources.

The [prefix-scoped example policy](terraform-s3-lab-policy.json) is retained for reference. It was not attached automatically. Authentication via STS proves identity; successful AWS lifecycle calls establish the permissions needed by the actual lab. Organization controls and permission boundaries can still restrict a role.

If the temporary session expires, run `aws login --profile scaler-sst-login --region ap-southeast-2`, then verify `aws sts get-caller-identity --profile scaler-sst` returns the expected account. Never copy AWS access keys into this repository.
