output "website_url" {
  description = "Path-style URL to open in browser"
  value       = "http://localhost:4566/${aws_s3_bucket.website.id}/index.html"
}

output "lambda_invoke_command" {
  description = "CLI test command for Lambda"
  value       = "awslocal lambda invoke --function-name ${aws_lambda_function.visitor_counter.function_name} response.json"
}