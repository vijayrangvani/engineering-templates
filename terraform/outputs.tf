# TEMPLATE: values printed after apply (and readable by other modules / scripts).
output "bucket_name" {
  value = aws_s3_bucket.data.bucket
}

output "api_public_ip" {
  value = aws_instance.api.public_ip
}
