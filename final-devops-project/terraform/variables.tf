variable "aws_region" {
  type    = string
  default = "ap-southeast-2"
}
variable "aws_profile" {
  type    = string
  default = "scaler-sst"
}
variable "cluster_name" {
  type    = string
  default = "labledger-session21"
}
variable "kubernetes_version" {
  type    = string
  default = "1.35"
}
variable "admin_cidr" {
  type        = string
  description = "Current workstation public IPv4/32 for the EKS API"
  validation {
    condition     = can(cidrnetmask(var.admin_cidr)) && endswith(var.admin_cidr, "/32")
    error_message = "Use your current IPv4/32; the EKS API must not be world-open."
  }
}
variable "node_type" {
  type    = string
  default = "c7i-flex.large"
}

variable "expected_account_id" {
  description = "Only this AWS account may be used for the submission labs."
  type        = string
  default     = "499567237930"
  validation {
    condition     = can(regex("^[0-9]{12}$", var.expected_account_id))
    error_message = "Provide a 12-digit AWS account ID."
  }
}
