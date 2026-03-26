# Import the library 
import boto3

# Create resource for instance and name it 
# Configuration for Localstack and using test for credentials
localstack_endpoint = "http://localhost:4566"
region = "ap-south-1"
ec2 = boto3.resource(
    'ec2',
    aws_access_key_id ="test",          # Added 'aws_' prefix
    aws_secret_access_key ="test",      # Fixed the name and added 'aws_'
    region_name=region,
    endpoint_url=localstack_endpoint   # Make sure this line is also here!
)

instance_name = "my-ec2-instance"
# Check if the instance we want to create already exists 
# If not create the instance user wants 

all_my_instances = ec2.instances.all()
instance_exists = False
instance_id = None

for instance in all_my_instances:
    if instance.tags:
        for tags in instance.tags:
            if tags['Key'] == 'Name' and tags['Value'] == instance_name:
                instance_exists = True
                instance_id = instance.id
                print(f"Instance with name {instance_name} already exists")
                break
    if instance_exists:
        break

if not instance_exists:
    new_instance = ec2.create_instances(
        ImageId = "ami-1234567890",
        MinCount = 1,
        MaxCount = 1,
        InstanceType = "t3.micro",
        KeyName = "test",
        TagSpecifications = [
            {
                'ResourceType':'instance',
                'Tags':[
                    {
                        'Key':'Name',
                        'Value':instance_name
                    }
                ]
            }
        ]
    )
    instance_id = new_instance[0].id
    print(f"Instance with name {instance_name} and id {instance_id} is created successfully")

    
# Stop an instance 
ec2.Instance(instance_id).stop()
print(f"Instance with id {instance_id} has been stopped") 

# Start an instance 
ec2.Instance(instance_id).start()
print(f"Instance with id {instance_id} has been started") 

# Terminate an instance
ec2.Instance(instance_id).terminate()
print(f"Instance with id {instance_id} has been terminate")
