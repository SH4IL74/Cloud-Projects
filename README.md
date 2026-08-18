# ☁️ Cloud & DevOps Projects Monorepo

![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat&logo=terraform&logoColor=white)
![LocalStack](https://img.shields.io/badge/LocalStack-0052CC?style=flat&logo=docker&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=flat&logo=ansible&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=github-actions&logoColor=white)

A monorepo of Infrastructure as Code (IaC), serverless architectures, configuration management, and GitOps pipelines tested locally using **LocalStack** and **Terraform**.

---

## 📂 Projects

| Project | Stack | Description |
| :--- | :--- | :--- |
| **[private-cloud](./private-cloud)** | Terraform, Ansible, Docker, Jinja2, Nginx | Provisions compute nodes, generates dynamic inventories, and configures reverse proxy routing. |
| **[static-website-hosting](./static-website-hosting)** | Terraform, S3, LocalStack | Automates S3 static site hosting, bucket policies, and local asset deployment. |
| **[serverless-password-vault](./serverless-password-vault)** | Lambda, DynamoDB, API Gateway, S3, Python | Full-stack serverless app with S3 frontend, entropy scoring engine, and NoSQL audit logs. |
| **[terraform-ci-cd-pipeline](./terraform-ci-cd-pipeline)** | GitHub Actions, Terraform, S3, DynamoDB | Automated GitOps pipeline with format/validation checks, remote state, and DynamoDB locks. |

---

## ⚡ Quick Start

### 1. Prerequisites
* Docker
* Terraform (v1.5+)
* LocalStack CLI & `awslocal`

### 2. Run LocalStack
```bash
localstack start -d