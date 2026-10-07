# Offline configuration tests only: this provider does not contact AWS.
mock_provider "aws" {
  mock_data "aws_ami" {
    defaults = {
      id = "ami-00000000000000000"
    }
  }
}
run "security_contract" {
  command = plan
  variables {
    aws_region       = "ap-south-1"
    aws_profile      = "default"
    instance_type    = "t3.micro"
    http_source_cidr = "203.0.113.10/32"
    bucket_name      = "devops-session19-offline-test"
  }
  assert {
    condition     = length(aws_security_group.web.ingress) == 1 && one(aws_security_group.web.ingress).from_port == 80 && one(aws_security_group.web.ingress).to_port == 80 && contains(one(aws_security_group.web.ingress).cidr_blocks, "203.0.113.10/32")
    error_message = "Expose only HTTP to the specified host; SSH or broad inbound access must not be added."
  }
  assert {
    condition     = aws_instance.web.metadata_options[0].http_tokens == "required"
    error_message = "Instance metadata must require IMDSv2 tokens."
  }
  assert {
    condition     = aws_instance.web.root_block_device[0].encrypted && aws_instance.web.root_block_device[0].delete_on_termination
    error_message = "Encrypt the root volume and remove it when terminating this lab instance."
  }
  assert {
    condition     = aws_s3_bucket_public_access_block.demo.block_public_acls && aws_s3_bucket_public_access_block.demo.block_public_policy && aws_s3_bucket_public_access_block.demo.ignore_public_acls && aws_s3_bucket_public_access_block.demo.restrict_public_buckets
    error_message = "All four S3 public-access block settings must remain enabled."
  }
  assert {
    condition     = !aws_s3_bucket.demo.force_destroy
    error_message = "Do not silently delete unexpected S3 objects during cleanup."
  }
}
run "reject_world_open_http" {
  command = plan
  variables {
    http_source_cidr = "0.0.0.0/0"
    bucket_name      = "devops-session19-offline-test"
  }
  expect_failures = [var.http_source_cidr]
}
