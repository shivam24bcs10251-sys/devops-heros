output "bucket_name" {
  description = "Created S3 bucket name."
  value       = aws_s3_bucket.demo.id
}
output "bucket_arn" {
  description = "Created S3 bucket ARN."
  value       = aws_s3_bucket.demo.arn
}
output "bucket_region" {
  description = "AWS deployment region."
  value       = var.aws_region
}
