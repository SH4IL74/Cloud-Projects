import boto3

def lambda_handler(event, context):
    ec2_resource = boto3.resource('ec2',region_name = 'ap-south-1')
    for elastic_ip in ec2_resource.vpc_addresses.all():
        if elastic_ip.instance_id is None:
            print(f"No association for elastic IP :{elastic_ip} . Releasing .....")
            elastic_ip.release()

    
    return {
        'statusCode': 200,
        'body': 'Process elastic IPs'

    }
