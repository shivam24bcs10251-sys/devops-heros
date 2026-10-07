variable "aws_region" {
  description = "Region for this isolated S3 lab."
  type        = string
  default     = "ap-south-1"
}
variable "aws_profile" {
  description = "Existing local AWS CLI profile; credentials remain outside Git."
  type        = string
  default     = "default"
}
variable "bucket_name" {
  description = "Globally unique, lowercase S3 bucket name for this lab only."
  type        = string
  validation {
    condition     = can(regex("^devops-session18-[a-z0-9-]+$", var.bucket_name)) && length(var.bucket_name) <= 63
    error_message = "Use a globally unique devops-session18- prefix, lowercase letters, numbers and hyphens, at most 63 characters."
  }
}
