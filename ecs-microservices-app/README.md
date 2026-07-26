# Serverless FastAPI Microservice on LocalStack with Terraform

A serverless REST microservice built with FastAPI, packaged for AWS Lambda using Mangum, and provisioned with Terraform on LocalStack.

## Architecture
- **Infrastructure Provisioning:** Terraform
- **Cloud Emulation:** LocalStack (API Gateway REST API, AWS Lambda, DynamoDB)
- **Application Framework:** FastAPI + Mangum (ASGI adapter)
- **Database:** Amazon DynamoDB (`items-table`)

## How to Build and Deploy

1. Package the Lambda application:
   ```bash
   rm -rf build lambda.zip
   mkdir build
   pip install -r app/requirements.txt -t build/
   cp app/main.py build/main.py
   cd build && zip -q -r ../lambda.zip . && cd ..