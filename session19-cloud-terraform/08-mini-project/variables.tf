variable "aws_region" {
  description = "Region for the short-lived isolated lab."
  type        = string
  default     = "ap-south-1"
}
variable "aws_profile" {
  description = "Existing local AWS CLI profile, without credentials in source."
  type        = string
  default     = "default"
}
variable "instance_type" {
  description = "Small x86_64 EC2 instance for the web demonstration."
  type        = string
  default     = "t3.micro"
  validation {
    condition     = contains(["t3.micro", "t3.small"], var.instance_type)
    error_message = "Choose t3.micro or t3.small for this bounded classroom lab."
  }
}
variable "http_source_cidr" {
  description = "Student's current public IPv4 address as /32; only this source can reach HTTP."
  type        = string
  validation {
    condition     = can(cidrnetmask(var.http_source_cidr)) && endswith(var.http_source_cidr, "/32")
    error_message = "Set your current public IPv4 address with a /32 suffix, not a broad internet range."
  }
}
variable "bucket_name" {
  description = "Globally unique disposable S3 name prefixed devops-session19-."
  type        = string
  validation {
    condition     = can(regex("^devops-session19-[a-z0-9-]+$", var.bucket_name)) && length(var.bucket_name) <= 63
    error_message = "Use a unique devops-session19- prefix, lowercase letters, digits and hyphens, maximum 63 characters."
  }
}
