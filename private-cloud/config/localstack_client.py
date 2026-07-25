import boto3
import os
from dotenv import load_dotenv

# Load variables from .env into os.environ
load_dotenv()


def get_boto_client(service_name):
    """ Creates a boto3 client pointing to LocalStack"""
    return boto3.client(
        service_name,
        endpoint_url=os.environ.get("AWS_ENDPOINT_URL","http://localhost:4566"),
        region_name=os.environ.get("AWS_DEFAULT_REGION","ap-south-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID","test"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY","test")
    )