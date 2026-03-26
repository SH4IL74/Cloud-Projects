import boto3
import time
from botocore.exceptions import ClientError

# Configuration
REGION = 'ap-south-1'  # Mumbai
CLUSTER_ID = 'rds-hol-cluster'
SUBNET_GROUP_NAME = 'vpc-hol'
DB_NAME = 'rds_hol_db'
USERNAME = 'admin'
PASSWORD = 'Password1234'

rds = boto3.client('rds', region_name=REGION)
ec2 = boto3.client('ec2', region_name=REGION)

def setup_aurora_v2():
    print(f"--- Starting Setup in {REGION} ---")
    
    # 1. Get a single VPC (Default VPC is safest for labs)
    vpc_name = 'vpc-hol'
    vpcs = ec2.describe_vpcs(Filters=[{'Name': 'is-default', 'Values': [vpc_name]}])
    if not vpcs['Vpcs']:
        # If no default VPC, just grab the first one available
        vpcs = ec2.describe_vpcs()
    
    vpc_id = vpcs['Vpcs'][0]['VpcId']
    print(f"Targeting VPC: {vpc_id}")

    # 2. Create Subnet Group with subnets ONLY from that VPC
    try:
        rds.describe_db_subnet_groups(DBSubnetGroupName=SUBNET_GROUP_NAME)
        print(f"Subnet group '{SUBNET_GROUP_NAME}' already exists.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'DBSubnetGroupNotFoundFault':
            print("Creating Subnet Group...")
            subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            subnet_ids = [sn['SubnetId'] for sn in subnets['Subnets']]
            
            if len(subnet_ids) < 2:
                print("Error: VPC needs at least 2 subnets in different AZs.")
                return

            rds.create_db_subnet_group(
                DBSubnetGroupName=SUBNET_GROUP_NAME,
                DBSubnetGroupDescription='HOL Subnet Group',
                SubnetIds=subnet_ids[:3] # Use up to 3
            )
        else: raise e

    # 3. Create Aurora Cluster
    try:
        rds.describe_db_clusters(DBClusterIdentifier=CLUSTER_ID)
        print(f"Cluster '{CLUSTER_ID}' already exists.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'DBClusterNotFoundFault':
            print(f"Creating Cluster '{CLUSTER_ID}'...")
            rds.create_db_cluster(
                DBClusterIdentifier=CLUSTER_ID,
                Engine='aurora-mysql',
                EngineVersion='8.0.mysql_aurora.3.04.0',
                DatabaseName=DB_NAME,
                MasterUsername=USERNAME,
                MasterUserPassword=PASSWORD,
                DBSubnetGroupName=SUBNET_GROUP_NAME,
                EngineMode='provisioned', # Required for V2
                ServerlessV2ScalingConfiguration={'MinCapacity': 0.5, 'MaxCapacity': 10.0}
            )
            
            # 4. Create the Serverless Instance
            print("Adding DB Instance (db.serverless)...")
            rds.create_db_instance(
                DBInstanceIdentifier=f"{CLUSTER_ID}-instance-1",
                DBClusterIdentifier=CLUSTER_ID,
                Engine='aurora-mysql',
                DBInstanceClass='db.serverless'
            )
            print("Creation initiated. This usually takes 5-10 minutes.")
        else: raise e

def cleanup_aurora():
    print(f"\n--- Starting Cleanup for {CLUSTER_ID} ---")
    try:
        # Check if cluster exists
        cluster = rds.describe_db_clusters(DBClusterIdentifier=CLUSTER_ID)
        members = cluster['DBClusters'][0]['DBClusterMembers']

        # 1. Delete Instances first
        for member in members:
            ins_id = member['DBInstanceIdentifier']
            print(f"Deleting instance: {ins_id}")
            try:
                rds.delete_db_instance(DBInstanceIdentifier=ins_id, SkipFinalSnapshot=True)
            except ClientError as e:
                print(f"Instance {ins_id} could not be deleted yet: {e.response['Error']['Message']}")

        # 2. Wait for instances to be fully gone
        print("Waiting for all instances to be deleted...")
        waiter = rds.get_waiter('db_instance_deleted')
        for member in members:
            try:
                waiter.wait(DBInstanceIdentifier=member['DBInstanceIdentifier'], WaiterConfig={'Delay': 30, 'MaxAttempts': 20})
            except: pass # It might already be gone

        # 3. Delete Cluster
        print(f"Deleting Cluster: {CLUSTER_ID}")
        rds.delete_db_cluster(DBClusterIdentifier=CLUSTER_ID, SkipFinalSnapshot=True)
        print("Cleanup initiated successfully.")

    except ClientError as e:
        if e.response['Error']['Code'] == 'DBClusterNotFoundFault':
            print("Cluster not found, nothing to clean up.")
        else: print(f"Cleanup Error: {e}")

# --- EXECUTION ---
cleanup_aurora()

# UNCOMMENT the line below to delete everything after it's created
# cleanup_aurora()