# Creating S3 Bucket for Static Website
resource "aws_s3_bucket" "website"{
    bucket = "my-cloud-resume-bucket"
}

resource "aws_s3_bucket_website_configuration" "website_config"{
    bucket = aws_s3_bucket.website.id

    index_document{
        suffix = "index.html"
    }
}

# Creating DynamoDB table for Visitor Count
resource "aws_s3_bucket_policy" "public_read"{
    bucket = aws_s3_bucket.website.id
    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Sud = "PublicReadGetObject"
                Effect = "Allow"
                Principal = "*"
                Action = "s3:GetObject"
                Resource = "${aws_s3_bucket.website.arn}/*"
            }
        ]
    })
}

resource "aws_dynamodb_table" "visitor_count"{
    name = "visitor_count"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "id"

    attribute {
        name = "id"
        type = "S"
    }
}

# Package the Python file into a ZIP
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "lambda_function.py"
  output_path = "lambda_function.zip"
}

# IAM Role for Lambda Execution
resource "aws_iam_role" "lambda_role" {
  name = "cloud_resume_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# Lambda Function Definition
resource "aws_lambda_function" "visitor_counter" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "visitor_counter"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  timeout          = 10
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      LOCALSTACK_HOSTNAME = "localhost.localstack.cloud"
}
  }
}

resource "aws_s3_object" "index_html" {
  bucket       = aws_s3_bucket.website.id
  key          = "index.html"
  source       = "${path.module}/index.html"
  content_type = "text/html"
  etag         = filemd5("${path.module}/index.html")
}