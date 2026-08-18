# Serverless Password & Credential Vault (Terraform + LocalStack)

![LocalStack](https://img.shields.io/badge/LocalStack-Local_Cloud-0052CC?style=flat&logo=docker&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-1.5+-7B42BC?style=flat&logo=terraform&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-Python_3.11-FF9900?style=flat&logo=awslambda&logoColor=white)
![DynamoDB](https://img.shields.io/badge/Amazon_DynamoDB-NoSQL-4053D6?style=flat&logo=amazondynamodb&logoColor=white)
![API Gateway](https://img.shields.io/badge/API_Gateway-REST_API-FF4F8B?style=flat&logo=amazon-aws&logoColor=white)
![S3](https://img.shields.io/badge/AWS_S3-Static_Hosting-569A31?style=flat&logo=amazons3&logoColor=white)

A full-stack, event-driven serverless application that generates cryptographically strong passwords, calculates entropy strength scores, and tracks audit records in a NoSQL database. Built with Python and fully provisioned using Terraform on LocalStack for zero-cost cloud development.

---

## 🏗️ Architecture

```text
[ Browser / Single Page App ]
            │
            ▼ (Static Assets via S3 Website Hosting)
  [ Amazon S3 Bucket ]
            │
            ▼ (AJAX REST Requests)
  [ AWS API Gateway (v1 REST) ]
            │
            ▼ (Proxy Integration)
  [ AWS Lambda (Python 3.11) ]
            │
            ▼ (PutItem / Scan)
  [ Amazon DynamoDB (`vault-records`) ]