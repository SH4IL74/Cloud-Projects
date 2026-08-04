# LocalStack S3 Static Web Hosting with Terraform

![LocalStack](https://img.shields.io/badge/LocalStack-Local_Cloud-0052CC?style=flat&logo=docker&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-1.5+-7B42BC?style=flat&logo=terraform&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS_S3-Emulated-232F3E?style=flat&logo=amazon-aws&logoColor=white)

An IaC project that provisions a static website locally using **Terraform** and **LocalStack** (emulating Amazon S3 and CloudFront/S3 web endpoints) without consuming real AWS cloud credits.

---

## 🏗️ Architecture Overview

```text
[ Local Browser / Client ]
       │
       ▼
[ LocalStack Gateway ] ──► http://localhost:4566
       │
       ▼
[ Emulated S3 Website Bucket ] ──► (Local Static Asset Hosting)