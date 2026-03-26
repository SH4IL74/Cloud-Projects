# import statements

import boto3

# Create a resource for ec2 and an instance name 
ec2 = boto3.resource('ec2', region_name='ap-south-1')
instance_name = 'ec2-practise-instance'

# store the instance id in a variable
instance_id = None

# Check if the instance we are trying to create already exists
# Only work with instance which is not terminated

all_my_instances = ec2.instances.all()
instance_exists = False

for instance in all_my_instances:
    for tags in instance.tags:
        if tags['Key'] == 'Name' and tags['Value'] == instance_name:
            instance_exists = True
            instance_id = instance.id
            print(f" Instance with name {instance_name} already exists with id {instance_id}")
            break

    if instance_exists:
        break

if not instance_exists: 
    # Launch a new ec2 instance if not already created
    new_instance = ec2.create_instances(
        ImageId = 'ami-0317b0f0a0144b137', #Replace with valid AMI id
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't3.micro',
        KeyName = 'asia-pacific-kp', #Enter valid key pair name
        TagSpecifications = [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                     }
                 ]
             }
         ]
    )
    instance_id = new_instance[0].id
    print(f" Instance with name {instance_name} created with id {instance_id}")
'''
# Stop an instance
ec2.Instance(instance_id).stop()
print(f"Instance with instance name {instance_name} has been stopped")
'''
'''
# Start an instance
ec2.Instance(instance_id).start()
print(f"Instance with instance name {instance_name} has been started")
'''

# Terminate the instance
ec2.Instance(instance_id).terminate()
print(f"Instance with instance name {instance_name} has been terminated")


