resource "aws_api_gateway_rest_api" "vault_api" {
  name        = "password-vault-api"
  description = "Serverless Password Vault REST API"
}

# Proxy resource to capture all paths (e.g., /generate, /passwords)
resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.vault_api.id
  parent_id   = aws_api_gateway_rest_api.vault_api.root_resource_id
  path_part   = "{proxy+}"
}

# Catch-all ANY method for the proxy path
resource "aws_api_gateway_method" "proxy_any" {
  rest_api_id   = aws_api_gateway_rest_api.vault_api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

# Lambda integration for proxy path
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.vault_api.id
  resource_id             = aws_api_gateway_resource.proxy.id
  http_method             = aws_api_gateway_method.proxy_any.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.vault_function.invoke_arn
}

# ANY method on root path (/)
resource "aws_api_gateway_method" "root_any" {
  rest_api_id   = aws_api_gateway_rest_api.vault_api.id
  resource_id   = aws_api_gateway_rest_api.vault_api.root_resource_id
  http_method   = "ANY"
  authorization = "NONE"
}

# Lambda integration for root path
resource "aws_api_gateway_integration" "lambda_root_integration" {
  rest_api_id             = aws_api_gateway_rest_api.vault_api.id
  resource_id             = aws_api_gateway_rest_api.vault_api.root_resource_id
  http_method             = aws_api_gateway_method.root_any.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.vault_function.invoke_arn
}

# Deployment & Stage
resource "aws_api_gateway_deployment" "deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda_integration,
    aws_api_gateway_integration.lambda_root_integration
  ]
  rest_api_id = aws_api_gateway_rest_api.vault_api.id
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.deployment.id
  rest_api_id   = aws_api_gateway_rest_api.vault_api.id
  stage_name    = "prod"
}

# Permission for API Gateway to invoke Lambda
resource "aws_lambda_permission" "api_gw_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.vault_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.vault_api.execution_arn}/*/*"
}