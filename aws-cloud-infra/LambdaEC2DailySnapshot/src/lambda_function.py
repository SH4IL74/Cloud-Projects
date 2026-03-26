import json
import boto3
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    current_date = datetime.now().strftime('%Y-%m-%d')

    try:
        response = ec2.create_snapshot(
            VolumeId = 'vol-0acec8011444de8a3',
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
        
    except Exception as e:  
        logger.error(f'Error creating snapshot: {str(e)}')
        


