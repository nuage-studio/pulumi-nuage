import string
from dataclasses import dataclass
from typing import Any, Optional

import pulumi
import pulumi_aws as aws
import pulumi_random

from .bastion import Bastion, BastionArgs

from .prefixed_component_resource import PrefixedComponentResource, PrefixedComponentResourceArgs


@dataclass
class BastionConfig:
    enabled: pulumi.Input[bool]
    subnet_id: Optional[pulumi.Input[str]] = None

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "BastionConfig":
        return BastionConfig(
            enabled=inputs.get("enabled"),
            subnet_id=inputs.get("subnetId", None),
        )


@dataclass
class ServerlessDatabaseArgs(PrefixedComponentResourceArgs):
    vpc_id: pulumi.Input[str]
    subnet_ids: pulumi.Input[list[str]]
    database_type: pulumi.Input[str]

    database_name: Optional[pulumi.Input[str]] = None
    master_username: Optional[pulumi.Input[str]] = None
    ip_whitelist: Optional[pulumi.Input[list[str]]] = None
    skip_final_snapshot: Optional[pulumi.Input[bool]] = None

    bastion: Optional[pulumi.Input[BastionConfig]] = None

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "ServerlessDatabaseArgs":
        bastion = inputs.get("bastion", None)

        return ServerlessDatabaseArgs(
            name=inputs.get("name", None),
            name_prefix=inputs.get("namePrefix", None),
            vpc_id=inputs["vpcId"],
            subnet_ids=inputs["subnetIds"],
            database_type=inputs["databaseType"],
            database_name=inputs.get("databaseName", None),
            master_username=inputs.get("masterUserName", None),
            ip_whitelist=inputs.get("ipWhitelist", None),
            skip_final_snapshot=inputs.get("skipFinalSnapshot", False),
            bastion=BastionConfig.from_inputs(bastion) if bastion else BastionConfig(enabled=False),
        )


class ServerlessDatabase(PrefixedComponentResource):
    user: pulumi.Output[str]
    password: pulumi.Output[str]
    host: pulumi.Output[str]
    port: pulumi.Output[int]
    database_name: pulumi.Output[str]
    cluster_arn: pulumi.Output[str]
    uri: pulumi.Output[str]

    bastion_private_key: pulumi.Output[str]
    bastion_ip: pulumi.Output[str]

    def __init__(
        self,
        resource_name: str,
        args: ServerlessDatabaseArgs,
        props: Optional[dict] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        super().__init__("nuage:aws:ServerlessDatabase", resource_name, args, props, opts)

        # RDS subnet group
        subnet_group = aws.rds.SubnetGroup(
            resource_name=resource_name,
            name=self.name_,
            description=self.name_.apply(lambda name: f"{name} subnet group"),
            subnet_ids=args.subnet_ids,
            tags={"Name": self.name_.apply(lambda name: f"{name} subnet group")},
            opts=pulumi.ResourceOptions(parent=self, replace_on_changes=["subnet_ids"]),
        )

        # Cluster master password
        aurora_master_password = pulumi_random.RandomPassword(
            resource_name=resource_name,
            length=30,
            special=True,
            # https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Limits.html#RDS_Limits.Constraints
            override_special=string.punctuation.translate(str.maketrans("", "", '/"@')),
            opts=pulumi.ResourceOptions(parent=self),
        )

        security_group = aws.ec2.SecurityGroup(
            resource_name=resource_name,
            name=self.name_,
            vpc_id=args.vpc_id,
            opts=pulumi.ResourceOptions(parent=self),
        )

        # mysql and psotgresql default ports
        port = 3306 if args.database_type == "mysql" else 5432

        aws.ec2.SecurityGroupRule(
            resource_name=resource_name,
            security_group_id=security_group.id,
            type="ingress",
            protocol=aws.ec2.ProtocolType.TCP,
            from_port=port,
            to_port=port,
            cidr_blocks=args.ip_whitelist or ["0.0.0.0/0"],
            description="Allow inbound connectivity to the database",
            opts=pulumi.ResourceOptions(parent=security_group),
        )

        if args.database_type == "mysql":
            engine_version = aws.rds.get_engine_version(
                engine=aws.rds.EngineType.AURORA_MYSQL,
                version="8.0",
                default_only=True,
            )
        else:
            engine_version = aws.rds.get_engine_version(
                engine=aws.rds.EngineType.AURORA_POSTGRESQL,
                version="13",
                default_only=True,
            )

        cluster_parameter_group = aws.rds.ClusterParameterGroup(
            resource_name=resource_name,
            family=engine_version.parameter_group_family,
            description=f"{self._name} cluster parameter group",
        )

        cluster = aws.rds.Cluster(
            resource_name=resource_name,
            cluster_identifier=self.name_,
            database_name=args.database_name,
            master_username=args.master_username,
            master_password=aurora_master_password.result,
            # Aurora Serverless v2 does not currently support the Data API
            enable_http_endpoint=False,
            iam_database_authentication_enabled=True,
            vpc_security_group_ids=[security_group.id],
            db_subnet_group_name=subnet_group.name,
            db_cluster_parameter_group_name=cluster_parameter_group.name,
            engine=engine_version.engine,
            engine_version=engine_version.version,
            port=port,
            serverlessv2_scaling_configuration=aws.rds.ClusterServerlessv2ScalingConfigurationArgs(
                min_capacity=0.5,
                max_capacity=128,
            ),
            # iam_roles=[aws.iam.get_role(name="AWSServiceRoleForRDS").arn],
            # https://github.com/terraform-aws-modules/terraform-aws-rds-aurora/issues/129
            skip_final_snapshot=args.skip_final_snapshot,
            storage_encrypted=True,
            opts=pulumi.ResourceOptions(parent=self),
        )
        # Create a cluster instance

        aws.rds.ClusterInstance(
            resource_name=resource_name,
            identifier=self.name_,
            cluster_identifier=cluster.id,
            engine=cluster.engine,
            db_subnet_group_name=cluster.db_subnet_group_name,
            instance_class="db.serverless",
            performance_insights_enabled=True,
            publicly_accessible=True,
            opts=pulumi.ResourceOptions(parent=cluster, depends_on=[cluster]),
        )

        # Build outputs

        outputs = {
            "user": cluster.master_username,
            "password": cluster.master_password,
            "host": cluster.endpoint,
            "port": cluster.port,
            "database_name": cluster.database_name,
            "cluster_arn": cluster.arn,
        }

        # Build the URI for convenience
        outputs["uri"] = pulumi.Output.all(
            database_type=args.database_type,
            user=cluster.master_username,
            password=cluster.master_password,
            host=cluster.endpoint,
            port=cluster.port,
            name=cluster.database_name,
        ).apply(lambda kwargs: "{database_type}://{user}:{password}@{host}:{port}/{name}".format(**kwargs))

        if args.bastion.enabled and args.bastion.subnet_id:
            bastion = Bastion(
                resource_name,
                args=BastionArgs(
                    name=self.get_suffixed_name("bastion"),
                    name_prefix=None,
                    vpc_id=args.vpc_id,
                    subnet_id=args.bastion.subnet_id,
                ),
                opts=pulumi.ResourceOptions(parent=self),
            )
            outputs["bastion_ip"] = bastion.public_ip
            outputs["bastion_private_key"] = bastion.private_key_pem

        self.set_outputs(outputs)

    def set_outputs(self, outputs: dict[str, Any]):
        """
        Adds the Pulumi outputs as attributes on the current object so they can be
        used as outputs by the caller, as well as registering them.
        """
        for output_name in outputs.keys():
            setattr(self, output_name, outputs[output_name])

        self.register_outputs(outputs)
