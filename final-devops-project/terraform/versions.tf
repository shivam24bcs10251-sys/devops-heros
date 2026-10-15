terraform {
  required_version = ">= 1.7.0, < 2.0.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "6.67.0" }
  }
}
provider "aws" {
  region              = var.aws_region
  profile             = var.aws_profile
  allowed_account_ids = [var.expected_account_id]
  default_tags { tags = { Project = "labledger-session21", Environment = "classroom", ManagedBy = "Terraform" } }
}
