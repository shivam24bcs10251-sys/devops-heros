provider "aws" {
  region              = var.aws_region
  profile             = var.aws_profile
  allowed_account_ids = [var.expected_account_id]
  default_tags {
    tags = {
      Project   = "Session18"
      ManagedBy = "Terraform"
      Owner     = "ShivamJaiswal"
    }
  }
}
