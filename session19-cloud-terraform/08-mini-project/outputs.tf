output "vpc_id" {
  value = aws_vpc.main.id
}
output "vpc_cidr" {
  value = aws_vpc.main.cidr_block
}
output "subnet_id" {
  value = aws_subnet.public.id
}
output "security_group_id" {
  value = aws_security_group.web.id
}
output "instance_id" {
  value = aws_instance.web.id
}
output "public_ip" {
  value = aws_instance.web.public_ip
}
output "website_url" {
  value = "http://${aws_instance.web.public_ip}"
}
output "bucket_name" {
  value = aws_s3_bucket.demo.id
}
output "region" {
  value = var.aws_region
}
output "aws_profile" {
  value = var.aws_profile
}
