"""An AWS Python Pulumi program"""

from os import name

import pulumi
import pulumi_awsx as awsx
from constants import BUCKET_NAME, LAMBDA, DB

# Append provider root to path.
import sys

sys.path.append("../")

# Import pulumi provider methods.
from nuage_provider.bucket_nuage import bucket_nuage
from nuage_provider.serverless_database import (
    ServerlessDatabase,
    ServerlessDatabaseArgs,
)
from nuage_provider.container_function import (
    ContainerFunction,
    ContainerFunctionArgs,
    Architecture,
)


# S3 Bucket
bucket = bucket_nuage(name=BUCKET_NAME)
pulumi.export("bucketName", bucket.bucket.bucket)

# Lambda Container
function = ContainerFunction(
    name=LAMBDA["NAME"],
    args=ContainerFunctionArgs(
        resource_name=None,
        description="Integration Tests Lambda Function",
        dockerfile="./lambda/Dockerfile.lambda",
        context="./lambda/",
        repository=None,  # "test-ecr"
        ecr_repository_name="itest-lambda-ecr",
        architecture=LAMBDA["ARCHITECTURE"],
        memory_size=LAMBDA["MEMORY"],
        timeout=LAMBDA["TIMEOUT"],
        environment={"ENV_TEST_VAL": LAMBDA["ENV_TEST_VAL"]},
        policy_document=None,
        keep_warm=True,
        url=False,
    ),
)
pulumi.export("lambda_arn", function.function.arn)
pulumi.export("lambda_name", function.function.name)
pulumi.export("lambda_role_arn", function.role.arn)
if function.function_url:
    pulumi.export("lambda_function_url", function.function_url)

# DATABASE
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
        )
    ],
)

database = ServerlessDatabase(
    name=DB["MYSQL_NAME"],
    args=ServerlessDatabaseArgs(
        resource_name="mysqldatabase",
        vpc_id=vpc.vpc_id,
        vpc_subnets=vpc.subnets,
        database_type="mysql",
        database_name=DB["MYSQL_NAME"],
        master_username=DB["USER"],
        ip_whitelist=None,
        skip_final_snapshot=True,
        data_api=False,
    ),
)
pulumi.export("database_mysql_user", database.user)
pulumi.export("database_mysql_password", database.password)
pulumi.export("database_mysql_name", database.name)
pulumi.export("database_mysql_port", database.port)
pulumi.export("database_mysql_host", database.host)
pulumi.export("database_mysql_uri", database.uri)
pulumi.export("database_mysql_cluster_arn", database.cluster_arn)


database = ServerlessDatabase(
    name=DB["POSTGRESQL_NAME"],
    args=ServerlessDatabaseArgs(
        resource_name="postgresqldatabase",
        vpc_id=vpc.vpc_id,
        vpc_subnets=vpc.subnets,
        database_type="postgresql",
        database_name=DB["POSTGRESQL_NAME"],
        master_username=DB["USER"],
        ip_whitelist=None,
        skip_final_snapshot=True,
        data_api=False,
        s3_extension=False,
    ),
)

pulumi.export("database_postgresql_user", database.user)
pulumi.export("database_postgresql_password", database.password)
pulumi.export("database_postgresql_name", database.name)
pulumi.export("database_postgresql_port", database.port)
pulumi.export("database_postgresql_host", database.host)
pulumi.export("database_postgresql_uri", database.uri)
pulumi.export("database_postgresql_cluster_arn", database.cluster_arn)
