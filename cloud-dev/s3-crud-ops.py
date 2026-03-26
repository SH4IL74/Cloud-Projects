import boto3
from botocore.exceptions import ClientError

# 1. Configuration for LocalStack
# We use 'test' for credentials because LocalStack doesn't validate them
LOCALSTACK_ENDPOINT = "http://localhost:4566"
REGION = "ap-south-1"

# 2. Initialize the S3 Client
s3_client = boto3.client(
    "s3",
    endpoint_url=LOCALSTACK_ENDPOINT,
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name=REGION
)

def create_my_bucket(bucket_name):
    """Creates an S3 bucket in LocalStack."""
    try:
        print(f"--- Creating Bucket: {bucket_name} ---")
        s3_client.create_bucket(Bucket=bucket_name)
        print(f" Success! Bucket '{bucket_name}' is ready.")
    except ClientError as e:
        print(f" Error: {e}")

def list_my_buckets():
    """Lists all buckets currently in LocalStack."""
    print("\n--- Current Buckets ---")
    response = s3_client.list_buckets()
    for bucket in response.get('Buckets', []):
        print(f" {bucket['Name']}")

if __name__ == "__main__":
    # You can change this name to whatever you like
    MY_BUCKET = "shail-cloud-project"
    
    create_my_bucket(MY_BUCKET)
    list_my_buckets()