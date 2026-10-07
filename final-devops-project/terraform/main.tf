data "aws_availability_zones" "available" { state = "available" }
resource "aws_vpc" "lab" {
  cidr_block           = "10.21.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags                 = { Name = var.cluster_name }
}
resource "aws_internet_gateway" "lab" { vpc_id = aws_vpc.lab.id }
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.lab.id
  cidr_block              = cidrsubnet(aws_vpc.lab.cidr_block, 8, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  tags                    = { Name = "${var.cluster_name}-public-${count.index}", "kubernetes.io/role/elb" = "1" }
}
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.lab.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.lab.id
  }
}
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
data "aws_iam_policy_document" "cluster_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["eks.amazonaws.com"]
    }
  }
}
resource "aws_iam_role" "cluster" {
  name               = "${var.cluster_name}-control-plane"
  assume_role_policy = data.aws_iam_policy_document.cluster_trust.json
}
resource "aws_iam_role_policy_attachment" "cluster" {
  role       = aws_iam_role.cluster.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}
resource "aws_eks_cluster" "lab" {
  name     = var.cluster_name
  role_arn = aws_iam_role.cluster.arn
  version  = var.kubernetes_version
  access_config {
    authentication_mode                         = "API_AND_CONFIG_MAP"
    bootstrap_cluster_creator_admin_permissions = true
  }
  vpc_config {
    subnet_ids              = aws_subnet.public[*].id
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = [var.admin_cidr]
  }
  depends_on = [aws_iam_role_policy_attachment.cluster]
}
data "aws_iam_policy_document" "node_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}
resource "aws_iam_role" "node" {
  name               = "${var.cluster_name}-worker"
  assume_role_policy = data.aws_iam_policy_document.node_trust.json
}
resource "aws_iam_role_policy_attachment" "node" {
  for_each   = toset(["AmazonEKSWorkerNodePolicy", "AmazonEKS_CNI_Policy", "AmazonEC2ContainerRegistryReadOnly"])
  role       = aws_iam_role.node.name
  policy_arn = "arn:aws:iam::aws:policy/${each.key}"
}
resource "aws_eks_node_group" "lab" {
  cluster_name    = aws_eks_cluster.lab.name
  node_group_name = "classroom"
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = aws_subnet.public[*].id
  instance_types  = [var.node_type]
  ami_type        = "AL2023_x86_64_STANDARD"
  disk_size       = 20
  scaling_config {
    desired_size = 1
    min_size     = 1
    max_size     = 2
  }
  depends_on = [aws_iam_role_policy_attachment.node, aws_route_table_association.public]
}
resource "aws_eks_addon" "storage" {
  cluster_name = aws_eks_cluster.lab.name
  addon_name   = "aws-ebs-csi-driver"
  depends_on   = [aws_eks_node_group.lab, aws_eks_pod_identity_association.ebs]
}
data "aws_iam_policy_document" "pod_trust" {
  statement {
    actions = ["sts:AssumeRole", "sts:TagSession"]
    principals {
      type        = "Service"
      identifiers = ["pods.eks.amazonaws.com"]
    }
  }
}
resource "aws_iam_role" "ebs" {
  name               = "${var.cluster_name}-ebs-csi"
  assume_role_policy = data.aws_iam_policy_document.pod_trust.json
}
resource "aws_iam_role_policy_attachment" "ebs" {
  role       = aws_iam_role.ebs.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"
}
resource "aws_eks_addon" "pod_identity" {
  cluster_name = aws_eks_cluster.lab.name
  addon_name   = "eks-pod-identity-agent"
  depends_on   = [aws_eks_node_group.lab]
}
resource "aws_eks_pod_identity_association" "ebs" {
  cluster_name    = aws_eks_cluster.lab.name
  namespace       = "kube-system"
  service_account = "ebs-csi-controller-sa"
  role_arn        = aws_iam_role.ebs.arn
  depends_on      = [aws_iam_role_policy_attachment.ebs, aws_eks_addon.pod_identity]
}
resource "aws_eks_addon" "metrics" {
  cluster_name = aws_eks_cluster.lab.name
  addon_name   = "metrics-server"
  depends_on   = [aws_eks_node_group.lab]
}
