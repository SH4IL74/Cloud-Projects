output "api_endpoint" {
  description = "Base API Gateway REST Endpoint URL"
  value       = "http://localhost:4566/_aws/execute-api/${aws_api_gateway_rest_api.vault_api.id}/prod"
}
output "website_url" {
  description = "Frontend S3 Static Website URL"
  value       = "http://${aws_s3_bucket.frontend_bucket.id}.s3-website.localhost.localstack.cloud:4566"
}