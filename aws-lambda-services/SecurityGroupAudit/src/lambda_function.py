import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2', region_name='ap-south-1')
    sns_client = boto3.client('sns', region_name='ap-south-1')
    sns_topic_arn = 'arn:aws:sns:ap-south-1:018763152546:SecurityGroupAuditAlerts'

    security_groups = ec2.security_groups.all()
    
    for sg in security_groups:
        print(f"Checking security group '{sg.id}' ({sg.group_name})")
        
        # This loop must be inside the SG loop!
        for rule in sg.ip_permissions:
            for ip_range in rule.get('IpRanges', []):
                if ip_range.get('CidrIp') == '0.0.0.0/0':
                    message = (f"WARNING: Inbound rule in security group '{sg.id}' "
                               f"({sg.group_name}) allows traffic from any IP address: {rule}")
                    print(message)
                    sns_client.publish(TopicArn=sns_topic_arn, Message=message)

    return {
        'statusCode': 200,
        'body': 'Security Audit Complete'
    }