# destroy.py
import time
from config.localstack_client import get_boto_client


def destroy_private_cloud():
    print(" Starting Private Cloud Teardown Process...\n")

    ec2 = get_boto_client("ec2")
    s3 = get_boto_client("s3")
    sns = get_boto_client("sns")

    # 1. Terminate EC2 Instances
    print(" Terminating EC2 Instances...")
    instances = ec2.describe_instances()["Reservations"]
    instance_ids = [
        inst["InstanceId"]
        for res in instances
        for inst in res["Instances"]
        if inst["State"]["Name"] != "terminated"
    ]
    if instance_ids:
        ec2.terminate_instances(InstanceIds=instance_ids)
        print(f"  Terminated instances: {instance_ids}")
        # Small wait for instance ENIs (network interfaces) to release
        time.sleep(2)

    # 2. Delete S3 Objects & Bucket
    print(" Deleting S3 Buckets...")
    bucket_name = "private-cloud-app-media"
    try:
        objects = s3.list_objects_v2(Bucket=bucket_name).get("Contents", [])
        for obj in objects:
            s3.delete_object(Bucket=bucket_name, Key=obj["Key"])
        s3.delete_bucket(Bucket=bucket_name)
        print(f" Deleted bucket: {bucket_name}")
    except Exception as e:
        print(f" S3 Note: {e}")

    # 3. Delete SNS Topics
    print(" Deleting SNS Topics...")
    topics = sns.list_topics()["Topics"]
    for t in topics:
        sns.delete_topic(TopicArn=t["TopicArn"])
        print(f" Deleted topic: {t['TopicArn']}")

    # 4. Clean up VPC Dependencies and VPCs
    print(" Detaching Gateways, Cleaning Route Tables & VPCs...")
    vpcs = ec2.describe_vpcs()["Vpcs"]

    for vpc in vpcs:
        vpc_id = vpc["VpcId"]

        # A. Detach and delete Internet Gateways
        igws = ec2.describe_internet_gateways(
            Filters=[{"Name": "attachment.vpc-id", "Values": [vpc_id]}]
        )["InternetGateways"]
        for igw in igws:
            igw_id = igw["InternetGatewayId"]
            ec2.detach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
            ec2.delete_internet_gateway(InternetGatewayId=igw_id)
            print(f" Detached & Deleted IGW: {igw_id}")

        # B. Delete Custom Route Tables (exclude main table)
        rts = ec2.describe_route_tables(
            Filters=[{"Name": "vpc-id", "Values": [vpc_id]}]
        )["RouteTables"]
        for rt in rts:
            is_main = any(assoc.get("Main", False) for assoc in rt.get("Associations", []))
            if not is_main:
                for assoc in rt.get("Associations", []):
                    ec2.disassociate_route_table(AssociationId=assoc["RouteTableAssociationId"])
                ec2.delete_route_table(RouteTableId=rt["RouteTableId"])
                print(f" Deleted Route Table: {rt['RouteTableId']}")

        # C. Delete Subnets
        subnets = ec2.describe_subnets(
            Filters=[{"Name": "vpc-id", "Values": [vpc_id]}]
        )["Subnets"]
        for sub in subnets:
            ec2.delete_subnet(SubnetId=sub["SubnetId"])
            print(f" Deleted Subnet: {sub['SubnetId']}")

        # D. Delete Custom Security Groups
        sgs = ec2.describe_security_groups(
            Filters=[{"Name": "vpc-id", "Values": [vpc_id]}]
        )["SecurityGroups"]
        for sg in sgs:
            if sg["GroupName"] != "default":
                try:
                    ec2.delete_security_group(GroupId=sg["GroupId"])
                    print(f" Deleted SG: {sg['GroupId']}")
                except Exception:
                    pass

        # E. Delete VPC
        try:
            ec2.delete_vpc(VpcId=vpc_id)
            print(f"  Deleted VPC: {vpc_id}")
        except Exception as e:
            print(f"  Error deleting VPC {vpc_id}: {e}")

    print("\n Teardown complete. Workspace completely reset!")


if __name__ == "__main__":
    destroy_private_cloud()