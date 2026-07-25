# This sets up the VPC,Internet Gateway,Public/Private Subnets and Route Tables

import sys
sys.path.append('..')
from config.localstack_client import get_boto_client

ec2 = get_boto_client('ec2')

def create_network():
    print(" Creating Network Core ")

    # 1.VPC
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
    vpc_id = vpc['Vpc']['VpcId']

    # 2.Subnets
    public_sub = ec2.create_subnet(VpcId=vpc_id,CidrBlock="10.0.1.0/24",AvailabilityZone="ap-south-1a")
    private_sub1 = ec2.create_subnet(VpcId=vpc_id,CidrBlock="10.0.2.0/24",AvailabilityZone="ap-south-1b")
    private_sub2 = ec2.create_subnet(VpcId=vpc_id,CidrBlock="10.0.3.0/24",AvailabilityZone="ap-south-1b")

    # 3.InternetGateway
    igw = ec2.create_internet_gateway()
    igw_id = igw['InternetGateway']['InternetGatewayId']
    ec2.attach_internet_gateway(InternetGatewayId=igw_id,VpcId=vpc_id)

    # 4.Route Table for Public Subnet
    rt = ec2.create_route_table(VpcId=vpc_id)
    rt_id = rt['RouteTable']['RouteTableId']
    ec2.create_route(RouteTableId=rt_id,DestinationCidrBlock='0.0.0.0/0',GatewayId=igw_id)
    ec2.associate_route_table(SubnetId=public_sub['Subnet']['SubnetId'],RouteTableId=rt_id)

    print(f"Network Ready ! VPC: {vpc_id}")
    return vpc_id,public_sub['Subnet']['SubnetId'],[private_sub1['Subnet']['SubnetId'],private_sub2['Subnet']['SubnetId']]

if __name__ == "__main__":
    create_network()

