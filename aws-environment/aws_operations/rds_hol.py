import boto3
import time

# Configuration
REGION = 'ap-south-1'
CLUSTER_ID = 'rds-hol-cluster'
SUBNET_GROUP_NAME = 'vpc-hol'
DB_NAME = 'rds_hol_db'
USERNAME = 'admin'
PASSWORD = 'Password1234'

rds = boto3.client('rds', region_name=REGION)
ec2 = boto3.client('ec2', region_name=REGION)

# 1. Get VPC and Subnets
vpcs = ec2.describe_vpcs(Filters=[{'Name': 'is-default', 'Values': ['true']}])
vpc_id = vpcs['Vpcs'][0]['VpcId']
print(f"Using VPC: {vpc_id}")

subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
subnet_ids = [sn['SubnetId'] for sn in subnets['Subnets']]

# 2. Create Subnet Group
rds.create_db_subnet_group(
    DBSubnetGroupName=SUBNET_GROUP_NAME,
    DBSubnetGroupDescription='HOL Subnet Group',
    SubnetIds=subnet_ids[:3]
)
print("Subnet Group created.")

# 3. Create Aurora Cluster
rds.create_db_cluster(
    DBClusterIdentifier=CLUSTER_ID,
    Engine='aurora-mysql',
    EngineVersion='8.0.mysql_aurora.3.04.0',
    DatabaseName=DB_NAME,
    MasterUsername=USERNAME,
    MasterUserPassword=PASSWORD,
    DBSubnetGroupName=SUBNET_GROUP_NAME,
    EngineMode='provisioned', 
    ServerlessV2ScalingConfiguration={'MinCapacity': 0.5, 'MaxCapacity': 10.0}
)
print(f"Cluster {CLUSTER_ID} creation initiated.")

# 4. Create the Serverless Instance
rds.create_db_instance(
    DBInstanceIdentifier=f"{CLUSTER_ID}-instance-1",
    DBClusterIdentifier=CLUSTER_ID,
    Engine='aurora-mysql',
    DBInstanceClass='db.serverless'
)
print("Instance added. Wait 5-10 minutes for availability.")