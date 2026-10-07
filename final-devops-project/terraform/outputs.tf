output "vpc_id" { value = aws_vpc.lab.id }
output "public_subnet_ids" { value = aws_subnet.public[*].id }
output "cluster_name" { value = aws_eks_cluster.lab.name }
output "cluster_endpoint" { value = aws_eks_cluster.lab.endpoint }
output "node_group" { value = aws_eks_node_group.lab.node_group_name }
output "kubectl_command" { value = "aws eks update-kubeconfig --name ${var.cluster_name} --region ${var.aws_region} --profile ${var.aws_profile}" }
