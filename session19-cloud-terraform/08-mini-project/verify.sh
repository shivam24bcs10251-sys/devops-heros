#!/usr/bin/env bash
set -euo pipefail
export AWS_REGION="$(terraform output -raw region)"
export AWS_DEFAULT_REGION="$AWS_REGION"
export AWS_PROFILE="$(terraform output -raw aws_profile)"
INSTANCE_ID="$(terraform output -raw instance_id)"
VPC_ID="$(terraform output -raw vpc_id)"
BUCKET_NAME="$(terraform output -raw bucket_name)"
WEBSITE_URL="$(terraform output -raw website_url)"
aws ec2 wait instance-status-ok --instance-ids "$INSTANCE_ID"
aws ec2 describe-vpcs --vpc-ids "$VPC_ID" --query 'Vpcs[].{ID:VpcId,CIDR:CidrBlock,State:State}'
aws ec2 describe-instances --instance-ids "$INSTANCE_ID" --query 'Reservations[].Instances[].{ID:InstanceId,State:State.Name,PublicIP:PublicIpAddress,MetadataTokens:MetadataOptions.HttpTokens}'
aws s3api get-public-access-block --bucket "$BUCKET_NAME"
aws s3api get-bucket-encryption --bucket "$BUCKET_NAME"
aws s3api get-bucket-versioning --bucket "$BUCKET_NAME"
for attempt in {1..60}; do
  if curl --fail --silent --connect-timeout 5 "$WEBSITE_URL" -o /tmp/session19-page.html; then
    if rg -q 'Shivam Jaiswal.*Session 19' /tmp/session19-page.html; then
      cat /tmp/session19-page.html
      printf '\nSession 19 cloud verification passed.\n'
      exit 0
    fi
  fi
  sleep 5
done
printf 'HTTP verification failed; inspect instance console and cloud-init output.\n' >&2
exit 1
