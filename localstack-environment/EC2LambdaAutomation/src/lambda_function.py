import json
import boto3
import logging
import os
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Check if we are running inside LocalStack
    # LocalStack automatically sets LOCALSTACK_HOSTNAME in the Lambda container
    localstack_host = os.environ.get('LOCALSTACK_HOSTNAME')
    
    if localstack_host:
       # Use 'localhost.localstack.cloud' or just the host provided by the env var
        localstack_host = os.environ.get('LOCALSTACK_HOSTNAME','localhost')
        endpoint_url = f"http://{localstack_host}:4566" 
        ec2 = boto3.client('ec2', endpoint_url=endpoint_url, region_name='ap-south-1')
    else:
        # Connect to real AWS Console
        ec2 = boto3.client('ec2', region_name='ap-south-1')

    current_date = datetime.now().strftime('%Y-%m-%d')

    try:
        # Note: In LocalStack, you must first create this Volume ID via CLI 
        # or the snapshot will fail because the 'vol-xxx' doesn't exist yet!
        response = ec2.create_snapshot(
            VolumeId = 'vol-7128ab7f4759d5f08',
            Description = 'My Ec2 Snapshot',
            TagSpecifications = [
                {
                    'ResourceType': 'snapshot',
                    'Tags':[
                        {
                            'Key': 'Name',
                            'Value': f'My Ec2 Snapshot {current_date}'
                        }
                    ]
                }
            ]
        )
        logger.info(f' Successfully created snapshot: {json.dumps(response, default=str)}')
        return response 
        
    except Exception as e:  
        logger.error(f'Error creating snapshot: {str(e)}')
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }