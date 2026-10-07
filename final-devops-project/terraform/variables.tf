variable "aws_region" {
  type    = string
  default = "ap-south-1"
}
variable "aws_profile" {
  type    = string
  default = "default"
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
  default = "t3.medium"
}
