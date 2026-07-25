# Deploy the EC2 instance,SNS notification topic and SES email identity

import sys
sys.path.append('..')
from config.localstack_client import get_boto_client

ec2 = get_boto_client('ec2')
sns = get_boto_client('sns')
ses = get_boto_client('ses')

def deploy_compute_and_messaging(public_subnet_id,web_sg_id):
    print(" Deploying Compute and Messaging Infrastructure")

    # 1.EC2 Web Server
    instance = ec2.run_instances(
        ImageId="ami-12345678",  # Mock AMI for Localstack
        InstanceType='t3.micro',
        MinCount=1,
        MaxCount=1,
        SubnetId=public_subnet_id,
        SecurityGroupIds=[web_sg_id]

    )

    # 2.SNS Topic
    topic = sns.create_topic(Name="system-alerts")

    # 3.SES Email Identity
    ses.verify_email_identity(EmailAddress="admin@privatecloud.local")

    print(f" Compute and Messaging Live! EC2 ID : {instance['Instances'][0]['InstanceId']}")
    


