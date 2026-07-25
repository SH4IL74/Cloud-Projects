# Set up Security Groups to enforce isolation between the web app and database layers

import sys
sys.path.append('..')
from config.localstack_client import get_boto_client

ec2 = get_boto_client('ec2')

def create_security_groups(vpc_id):
    print(" Directing Firewall / Security Groups")

    # Web Security Group (Public)
    web_sg = ec2.create_security_group(
        GroupName="web-tier-sg",Description="Allow HTTP inbound",VpcId=vpc_id
    )
    web_sg_id = web_sg['GroupId']
    ec2.authorize_security_group_ingress(
        GroupId=web_sg_id,
        IpPermissions=[{'IpProtocol':'tcp',
                        'FromPort':80,
                        'ToPort':80,
                        'IpRanges':[{'CidrIp':'0.0.0.0/0'}]
        }]
    )

    # Databse Security Group (Private - Only accepts traffic from web_sg)
    db_sg = ec2.create_security_group(
        GroupName="db-tier-sg",Description="Allow DB access from Web tier only",VpcId=vpc_id
    )
    db_sg_id = db_sg['GroupId']
    ec2.authorize_security_group_ingress(
        GroupId=db_sg_id,
        IpPermissions=[{
            'IpProtocol':'tcp',
            'FromPort':5432,
            'ToPort':5432,
            'UserIdGroupPairs':[{'GroupId':web_sg_id}]
        }]
    )

    print(" Security Groups Created")
    return web_sg_id,db_sg_id
