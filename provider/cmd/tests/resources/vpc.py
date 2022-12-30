import pulumi_awsx as awsx

vpc = awsx.ec2.Vpc(
    resource_name=f"itest-vpc",
    enable_dns_hostnames=True,
    number_of_availability_zones=2,
    nat_gateways=awsx.ec2.NatGatewayConfigurationArgs(
        strategy=awsx.ec2.NatGatewayStrategy.NONE
    ),
    subnet_specs=[
        awsx.ec2.SubnetSpecArgs(
            cidr_mask=24,
            type=awsx.ec2.SubnetType.PUBLIC,
        ),
        awsx.ec2.SubnetSpecArgs(
            cidr_mask=24,
            type=awsx.ec2.SubnetType.PRIVATE,
        ),
    ],
)
