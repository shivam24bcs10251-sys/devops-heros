mock_provider "aws" {
  mock_resource "aws_iam_role" { defaults = { arn = "arn:aws:iam::123456789012:role/lab" } }
  mock_data "aws_iam_policy_document" { defaults = { json = "{\"Version\":\"2012-10-17\",\"Statement\":[]}" } }

  mock_data "aws_availability_zones" { defaults = { names = ["ap-south-1a", "ap-south-1b"] } }
}
variables { admin_cidr = "203.0.113.10/32" }
run "restricted_two_subnet_cluster" {
  command = plan
  assert {
    condition     = length(aws_subnet.public) == 2
    error_message = "Two subnets are required."
  }
  assert {
    condition     = aws_eks_cluster.lab.vpc_config[0].public_access_cidrs == toset(["203.0.113.10/32"])
    error_message = "EKS API must use the supplied /32."
  }
  assert {
    condition     = aws_eks_node_group.lab.scaling_config[0].desired_size == 1
    error_message = "Keep the lab at one initial worker."
  }
}
run "reject_world_open_api" {
  command = plan
  variables { admin_cidr = "0.0.0.0/0" }
  expect_failures = [var.admin_cidr]
}
