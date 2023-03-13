import pulumi
import pulumi_aws as aws

vpc = aws.ec2.Vpc(
    "foo-vpc-test",
    cidr_block="10.0.0.0/16",
    instance_tenancy="default",
    enable_dns_hostnames=True,
    tags={
        "Name": "main",
    },
)
public_subnet_1 = aws.ec2.Subnet(
    "foo-vpc-test-subnet-public-az1",
    vpc_id=vpc.id,
    availability_zone="eu-west-1a",
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,
    tags={
        "Name": "foo-vpc-test-public-subnet-az1",
    },
)

public_subnet_2 = aws.ec2.Subnet(
    "foo-vpc-test-subnet-public-az2",
    vpc_id=vpc.id,
    availability_zone="eu-west-1b",
    cidr_block="10.0.2.0/24",
    map_public_ip_on_launch=True,
    tags={
        "Name": "foo-vpc-test-public-subnet-az2",
    },
)


private_subnet_1 = aws.ec2.Subnet(
    "foo-vpc-test-subnet-private-az1",
    vpc_id=vpc.id,
    cidr_block="10.0.3.0/24",
    availability_zone="eu-west-1a",
    map_public_ip_on_launch=False,
    tags={
        "Name": "foo-vpc-test-private-subnet-az1",
    },
)
private_subnet_2 = aws.ec2.Subnet(
    "foo-vpc-test-subnet-private-az2",
    vpc_id=vpc.id,
    cidr_block="10.0.4.0/24",
    availability_zone="eu-west-1b",
    map_public_ip_on_launch=False,
    tags={
        "Name": "foo-vpc-test-private-subnet-az2",
    },
)


route_table = aws.ec2.RouteTable(
    "foo-vpc-test-routetable",
    vpc_id=vpc.id,
    tags={
        "Name": "foo-vpc-test-routetable",
    },
)
aws.ec2.RouteTableAssociation(
    "routeTableAssociation-public-az1", subnet_id=public_subnet_1.id, route_table_id=route_table.id
)
aws.ec2.RouteTableAssociation(
    "routeTableAssociation-public-az2", subnet_id=public_subnet_2.id, route_table_id=route_table.id
)
aws.ec2.RouteTableAssociation(
    "routeTableAssociation-private-az1", subnet_id=private_subnet_1.id, route_table_id=route_table.id
)
aws.ec2.RouteTableAssociation(
    "routeTableAssociation-private-az2", subnet_id=private_subnet_2.id, route_table_id=route_table.id
)

eip = aws.ec2.Eip("foo-vpc-test-eip")


igw = aws.ec2.InternetGateway(
    "foo-vpc-test-gw",
    vpc_id=vpc.id,
    tags={
        "Name": "foo-vpc-test-gw",
    },
)


ngw = aws.ec2.NatGateway(
    "foo-vpc-test-natgateway",
    allocation_id=eip.id,
    subnet_id=public_subnet_1.id,
    tags={
        "Name": "foo-vpc nat gw",
    },
    opts=pulumi.ResourceOptions(depends_on=[igw]),
)


route = aws.ec2.Route(
    "foo-vpc-test-route", route_table_id=route_table.id, destination_cidr_block="0.0.0.0/0", gateway_id=igw.id
)

# vpc = awsx.ec2.Vpc(
#     resource_name=f"itest-vpc",
#     enable_dns_hostnames=True,
#     number_of_availability_zones=2,
#     nat_gateways=awsx.ec2.NatGatewayConfigurationArgs(strategy=awsx.ec2.NatGatewayStrategy.NONE),
#     subnet_specs=[
#         awsx.ec2.SubnetSpecArgs(
#             cidr_mask=24,
#             type=awsx.ec2.SubnetType.PUBLIC,
#         ),
#         awsx.ec2.SubnetSpecArgs(
#             cidr_mask=24,
#             type=awsx.ec2.SubnetType.PRIVATE,
#         ),
#     ],
# )
