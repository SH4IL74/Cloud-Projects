# Importing essential libraries
import boto3
import time

# Configuration
REGION = 'ap-south-1'
CLUSTER_ID = 'rds-ops-cluster'
SUBNET_GROUP_NAME = 'vpc-ops'
DB_NAME = 'rds-ops-db'
LOCALSTACK_ENDPOINT = 'http://localhost:4566'
USERNAME = 'admin'
PASSWORD = 'password1234'

# Intializing the ec2 and rds clients 
rds = boto3.client(
    'rds',
    region_name = REGION,
    endpoint_url = LOCALSTACK_ENDPOINT,
    aws_access_key_id = 'test',
    aws_secret_access_key = 'test'
)
ec2 = boto3.client(
    'ec2',
    region_name = REGION,
    endpoint_url = LOCALSTACK_ENDPOINT,
    aws_access_key_id = 'test',
    aws_secret_access_key = 'test'
)

# Getting the existing VPC or creating a new one if none exists
vpcs = ec2.describe_vpcs().get('Vpcs', [])
if not vpcs:
    vpc_id = ec2.create_vpc(CidrBlock='10.0.0.0/16')['Vpc']['VpcId']
    # Add subnets so the Subnet Group has something to use
    ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.1.0/24', AvailabilityZone=f'{REGION}a')
    ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.2.0/24', AvailabilityZone=f'{REGION}b')
else:
    vpc_id = vpcs[0]['VpcId']

subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
subnet_ids = [sn['SubnetId'] for sn in subnets['Subnets']]

# Create Subnet Group
rds.create_db_subnet_group(
    DBSubnetGroupName = SUBNET_GROUP_NAME,
    DBSubnetGroupDescription = 'Ops Subnet Group',
    SubnetIds = subnet_ids[:2]
)
print("Subnet group created")

# Create Aurora Cluster
rds.create_db_cluster(
    DBClusterIdentifier = CLUSTER_ID,
    Engine = 'aurora-mysql',
    EngineVersion = '8.0.mysql_aurora.3.04.0',
    DatabaseName = DB_NAME,
    MasterUsername = USERNAME,
    MasterUserPassword = PASSWORD,
    DBSubnetGroupName = SUBNET_GROUP_NAME,
    EngineMode = 'provisioned',
    ServerlessV2ScalingConfiguration = {'MinCapacity':0.5,'MaxCapacity':10.0}
)
print(f"Cluster {CLUSTER_ID} creation intiated")

# Create the Serverless Instance 
rds.create_db_instance(
    DBInstanceIdentifier = f"{CLUSTER_ID}-instance-1",
    DBClusterIdentifier = CLUSTER_ID,
    Engine = 'aurora-sql',
    DBInstanceClass = 'db.serverless'
)
print("Instance added")
