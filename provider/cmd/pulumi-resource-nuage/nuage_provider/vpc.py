from dataclasses import dataclass
from typing import Optional

import pulumi
import pulumi_aws as aws

from .prefixed_component_resource import PrefixedComponentResource, PrefixedComponentResourceArgs

aws_config = pulumi.Config("aws")
region = aws_config.require("region")


@dataclass
class VpcArgs(PrefixedComponentResourceArgs):
    cidr_block: Optional[pulumi.Input[str]] = "10.0.0.0/16"

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "VpcArgs":
        return VpcArgs(
            name=inputs.get("name", None),
            name_prefix=inputs.get("namePrefix", None),
            cidr_block=inputs["cidrBlock"],
        )


class Vpc(PrefixedComponentResource):
    id: pulumi.Output[str]
    arn: pulumi.Output[str]
    vpc: aws.ec2.Vpc
    public_subnets: list[aws.ec2.Subnet]
    private_subnets: list[aws.ec2.Subnet]
    public_subnet_ids: list[pulumi.Output[str]]
    private_subnet_ids: list[pulumi.Output[str]]

    def __init__(
        self,
        resource_name: str,
        args: VpcArgs,
        props: Optional[dict] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        super().__init__("nuage:aws:Vpc", resource_name, args, props, opts)

        self.vpc = aws.ec2.Vpc(
            resource_name=resource_name,
            cidr_block=args.cidr_block,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            tags={"Name": self.name_},
            opts=pulumi.ResourceOptions(parent=self),
        )
        self.id = self.vpc.id
        self.arn = self.vpc.arn

        # Subnets

        self.private_subnets = []
        self.private_subnet_ids = []
        for i, az in enumerate(["a", "b", "c"]):
            private_subnet = aws.ec2.Subnet(
                resource_name=f"{resource_name}-private-{az}",
                cidr_block=f"10.0.{i}.0/24",  # TODO: increment from cidr_block
                vpc_id=self.vpc.id,
                availability_zone=f"{region}{az}",
                map_public_ip_on_launch=False,
                tags={"Name": f"{self.name_}-private-{az}", "SubnetType": "private"},
                opts=pulumi.ResourceOptions(parent=self.vpc),
            )
            self.private_subnets.append(private_subnet)
            self.private_subnet_ids.append(private_subnet.id)

        self.public_subnets = []
        self.public_subnet_ids = []
        for i, az in enumerate(["a", "b", "c"]):
            public_subnet = aws.ec2.Subnet(
                resource_name=f"{resource_name}-public-{az}",
                cidr_block=f"10.0.{i+128}.0/24",  # TODO: increment from cidr_block
                vpc_id=self.vpc.id,
                availability_zone=f"{region}{az}",
                map_public_ip_on_launch=True,
                tags={"Name": f"{self.name_}-public-{az}", "SubnetType": "public"},
                opts=pulumi.ResourceOptions(parent=self.vpc),
            )
            self.public_subnets.append(public_subnet)
            self.public_subnet_ids.append(public_subnet.id)

        # NAT & Internet Gateways

        nat_ip = aws.ec2.Eip(
            resource_name=f"{resource_name}-nat",
            vpc=True,
            tags={"Name": self.name_},
            opts=pulumi.ResourceOptions(parent=self.public_subnets[0]),
        )

        nat = aws.ec2.NatGateway(
            resource_name=f"{resource_name}-nat",
            allocation_id=nat_ip.allocation_id,
            subnet_id=self.public_subnets[0].id,
            tags={"Name": self.name_},
            opts=pulumi.ResourceOptions(parent=self.public_subnets[0]),
        )

        internet_gateway = aws.ec2.InternetGateway(
            resource_name=f"{resource_name}-igw",
            vpc_id=self.id,
            tags={"Name": self.name_},
            opts=pulumi.ResourceOptions(parent=self.vpc),
        )

        # Route tables
        for private_subnet in self.private_subnets:
            route_table = aws.ec2.RouteTable(
                resource_name=private_subnet._name,
                vpc_id=self.vpc.id,
                routes=[
                    aws.ec2.RouteTableRouteArgs(
                        cidr_block="0.0.0.0/0",
                        nat_gateway_id=nat.id,
                    )
                ],
                tags=private_subnet.tags,
                opts=pulumi.ResourceOptions(parent=private_subnet),
            )

            aws.ec2.RouteTableAssociation(
                resource_name=private_subnet._name,
                subnet_id=private_subnet.id,
                route_table_id=route_table.id,
                opts=pulumi.ResourceOptions(parent=route_table),
            )

        for public_subnet in self.public_subnets:
            route_table = aws.ec2.RouteTable(
                resource_name=public_subnet._name,
                vpc_id=self.vpc.id,
                routes=[
                    aws.ec2.RouteTableRouteArgs(
                        cidr_block="0.0.0.0/0",
                        gateway_id=internet_gateway.id,
                    )
                ],
                tags=public_subnet.tags,
                opts=pulumi.ResourceOptions(parent=public_subnet),
            )

            aws.ec2.RouteTableAssociation(
                resource_name=public_subnet._name,
                subnet_id=public_subnet.id,
                route_table_id=route_table.id,
                opts=pulumi.ResourceOptions(parent=route_table),
            )

        # Build outputs

        self.register_outputs(
            {
                "id": self.vpc.id,
                "arn": self.vpc.arn,
                "vpc": self.vpc,
                "public_subnets": self.public_subnets,
                "public_subnet_ids": self.public_subnet_ids,
                "private_subnets": self.private_subnets,
                "private_subnet_ids": self.private_subnet_ids,
            }
        )
