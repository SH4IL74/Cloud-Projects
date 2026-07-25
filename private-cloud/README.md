# Local AWS Private Cloud Ecosystem

A complete, modular Virtual Private Cloud (VPC) environment built locally using **Python (Boto3)** and **LocalStack**.

## Architecture Overview
- **VPC & Subnets**: Multi-AZ setup with isolated public and private subnets.
- **Security Groups**: Granular firewall restrictions between Web Tier and DB Tier.
- **Compute & Storage**: EC2 instance deployment and S3 object storage bucket.
- **Messaging & Alerts**: Integration with AWS SNS and SES for automated notifications.

## Quickstart Guide

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.10+

### 2. Setup Environment
```bash
# Clone repository and enter directory
cd cloud-workspace/private-cloud

# Create Virtual Environment & Install Dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start LocalStack Emulator
docker-compose up -d