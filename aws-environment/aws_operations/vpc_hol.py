import boto3

# Create a VPC

ec2 = boto3.client('ec2', region_name = 'ap-south-1')
vpc_name = 'vpc-hol'

response = ec2.describe_vpcs(Filters = [{  'Name': 'tag:Name', 'Values': [vpc_name]}])
vpcs = response.get('Vpcs', [])

if vpcs:
    vpc_id = vpcs[0]['VpcId']
    print(f"Vpc with name {vpc_name} and id {vpc_id} already exists")
else:
    vpc_response = ec2.create_vpc(CidrBlock = '10.0.0.0/16')
    vpc_id = vpc_response['Vpc']['VpcId']
    ec2.create_tags(Resources = [vpc_id] , Tags = [{'Key' : 'Name', 'Value': vpc_name}])
    print(f"Vpc with name {vpc_name} and id {vpc_id} has been created")

# Create an Internet Gateway

ig_name = "ig-vpc-hol"
response = ec2.describe_internet_gateways(Filters = [{  'Name': 'tag:Name', 'Values': [ig_name]}])
internet_gateways = response.get('InternetGateways', [])

if internet_gateways:
    ig_id = internet_gateways[0]['InternetGatewayId']
    print(f"Internet Gateway with name {ig_name} and id {ig_id} already exists")
else:
    ig_response = ec2.create_internet_gateway()
    ig_id = ig_response['InternetGateway']['InternetGatewayId']
    ec2.create_tags(Resources = [ig_id] , Tags = [{'Key' : 'Name', 'Value': ig_name}])
    ec2.attach_internet_gateway(InternetGatewayId = ig_id, VpcId = vpc_id)
    print(f"Internet Gateway with name {ig_name} and id {ig_id} has been created")


# Create a route table and a public route

rt_response = ec2.create_route_table(VpcId = vpc_id)
rt_id = rt_response['RouteTable']['RouteTableId']
route = ec2.create_route(
    RouteTableId = rt_id,
    DestinationCidrBlock = '0.0.0.0/0',
    GatewayId = ig_id
)
print(f"Route table with id {rt_id} has been created and a public route has been added to it")

# Creating 3 subnets

subnet_1 = ec2.create_subnet(VpcId = vpc_id , CidrBlock = '10.0.1.0/24' , AvailabilityZone = 'ap-south-1a')
subnet_2 = ec2.create_subnet(VpcId = vpc_id , CidrBlock = '10.0.2.0/24' , AvailabilityZone = 'ap-south-1b')
subnet_3 = ec2.create_subnet(VpcId = vpc_id , CidrBlock = '10.0.3.0/24' , AvailabilityZone = 'ap-south-1c')

print(f"Subnet with id {subnet_1['Subnet']['SubnetId']} has been created in availability zone ap-south-1a")
print(f"Subnet with id {subnet_2['Subnet']['SubnetId']} has been created in availability zone ap-south-1b")
print(f"Subnet with id {subnet_3['Subnet']['SubnetId']} has been created in availability zone ap-south-1c")

