# Importing th boto3 library
import boto3

# Creating an ec2 instance for creation of vpc and intializing localstack endpint url 
Localstack_endpoint = "http://localhost:4566"
ec2 = boto3.client(
    'ec2',
    aws_access_key_id = 'test',
    aws_secret_access_key = 'test',
    region_name = 'ap-south-1',
    endpoint_url = Localstack_endpoint
)
vpc_name = 'vpc-ops'

response = ec2.describe_vpcs(Filters = [{ 'Name': 'tag:Name', 'Values': [vpc_name]}])
vpcs = response.get('Vpcs',[])

# Checking if the vpc already exists
# If not creating a new one

if vpcs:
    vpc_id = vpcs[0]['VpcId']
    print(f"Vpc with name {vpc_name} and Id {vpc_id} already exists")
else:
    vpc_response = ec2.create_vpc(CidrBlock = '10.0.0.0/16')
    vpc_id = vpc_response['Vpc']['VpcId']
    ec2.create_tags(Resources = [vpc_id] , Tags = [{'Key':'Name', 'Value': vpc_name}])
    print(f"Vpc with name {vpc_name} and Id {vpc_id} is created successfully")

# Creating an Internet Gateway
ig_name = 'ig-vpc-ops'
response = ec2.describe_internet_gateways(Filters = [{ 'Name':'tag:Name', 'Values': [ig_name]}])
internet_gateways = response.get('InternetGateways',[])

# Checking if internet gateway exists , if not creating a new one
if internet_gateways:
    ig_id = internet_gateways[0]['InternetGatewayId']
    print(f"InternetGateway with name {ig_name} and Id {ig_id} already exists")
else:
    ig_response = ec2.create_internet_gateway()
    ig_id = ig_response['InternetGateway']['InternetGatewayId']
    ec2.create_tags(Resources = [ig_id] , Tags = [{'Key':'Name', 'Value': ig_name}])
    ec2.attach_internet_gateway(InternetGatewayId = ig_id, VpcId = vpc_id)
    print(f"InternetGateway with name {ig_name} and Id {ig_id} is created successfully")

# Creating a route table
rt_response = ec2.create_route_table(VpcId = vpc_id)
rt_id = rt_response['RouteTable']['RouteTableId']
route = ec2.create_route(
    RouteTableId = rt_id,
    DestinationCidrBlock = '0.0.0.0/0',
    GatewayId = ig_id
)
print(f"RouteTable with Id {rt_id} is created successfully and a public route has been added to it")

# Creating 3 subnets for the virtual private cloud vpc-ops
subnet_1 = ec2.create_subnet(VpcId = vpc_id,CidrBlock = '10.0.1.0/24',AvailabilityZone = 'ap-south-1a')
subnet_2 = ec2.create_subnet(VpcId = vpc_id,CidrBlock = '10.0.2.0/24',AvailabilityZone = 'ap-south-1b')
subnet_3 = ec2.create_subnet(VpcId = vpc_id,CidrBlock = '10.0.3.0/24',AvailabilityZone = 'ap-south-1c')
print(f"Subnet with Id {subnet_1['Subnet']['SubnetId']} has been created successfully in availability zone ap-south-1a")
print(f"Subnet with Id {subnet_2['Subnet']['SubnetId']} has been created successfully in availability zone ap-south-1b")
print(f"Subnet with Id {subnet_3['Subnet']['SubnetId']} has been created successfully in availability zone ap-south-1c")


