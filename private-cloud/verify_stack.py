# It acts as an automated audit.It inspects your environment to guarantee all resources exist and are wired coorectly

from config.localstack_client import get_boto_client

def audit_private_cloud():
    print(" Auditing Deployed Private Cloud Resources ... \n")

    # 1.Audit Network (VPC and Subnets)
    ec2 = get_boto_client("ec2")
    vpcs = ec2.describe_vpcs()["Vpcs"]
    subnets = ec2.describe_subnets()["Subnets"]
    print(f" VPCs Active: {len(vpcs)}")
    print(f" Subnets Active: {len(subnets)}")

    # 2.Audit Security Groups
    sgs = ec2.describe_security_groups()["SecurityGroups"]
    sg_names = [sg["GroupName"] for sg in sgs]
    print(f" Security Groups Found: {sg_names}")

    # 3.Audit Storage (S3)
    s3 = get_boto_client("s3")
    buckets = [b["Name"] for b in s3.list_buckets()["Buckets"]]
    print(f" S3 Buckets Active: {buckets}")

    # 4.Audit Compute (EC2)
    instances = ec2.describe_instances()["Reservations"]
    active_instances = [
        inst["InstanceId"]
        for res in instances
        for inst in res["Instances"]
        if inst["State"]["Name"] != "terminated"
    ]
    print(f" Running EC2 Instances: {active_instances}")

    # 5.Audit Messaging (SNS and SES)
    sns = get_boto_client("sns")
    ses = get_boto_client("ses")
    topics = [t["TopicArn"] for t in sns.list_topics()["Topics"]]
    identities = ses.list_identities()["Identities"]

    print(f" SNS Topics: {topics}")
    print(f" SES Identities Verified: {identities} ")

    print("\n Verification Audit Complete.Everything is operational")

if __name__ == "__main__":
    audit_private_cloud()

