# Importing essential libraries
import boto3

# Creating a user defined function to locate any elastic ip and delete it if it is not in use
def lambda_handler(event,context):
    # Creating an ec2 resource
    LOCALSTACK_ENDPOINT = "http://localhost:4566"
    REGION_NAME = "ap-south-1"
    ec2 = boto3.resource(
        'ec2',
        region_name = REGION_NAME,
        endpoint_url = LOCALSTACK_ENDPOINT,
        aws_access_key_id = "test",
        aws_secret_access_key = "test"
    )
    
    all_ips = list(ec2.vpc_addresses.all())
    print(f"Total Elastic IPs found in LocalStack: {len(all_ips)}")
    
    # Creating a loop to check all the elastic ips 
    for elastic_ip in ec2.vpc_addresses.all():
        if not  elastic_ip.instance_id is None:
            print(f"No association for elastic IP :{elastic_ip}.Releasing ")
            elastic_ip.release()

    return{
        'statuscode':200,
        'body':'Process Elastic IPs'
    }

if __name__ == "__main__":
    print(lambda_handler(None,None))
