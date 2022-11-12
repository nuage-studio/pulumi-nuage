"""An AWS Python Pulumi program"""

import pulumi
from constants import DB

# Linked resources
from .vpc import vpc

# Import pulumi provider methods.
from nuage_provider.serverless_database import (
    ServerlessDatabase,
    ServerlessDatabaseArgs,
)

# MySQL DATABASE
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

# PostgreSQL DATABASE
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
    ),
)

pulumi.export("database_postgresql_user", database.user)
pulumi.export("database_postgresql_password", database.password)
pulumi.export("database_postgresql_name", database.name)
pulumi.export("database_postgresql_port", database.port)
pulumi.export("database_postgresql_host", database.host)
pulumi.export("database_postgresql_uri", database.uri)
pulumi.export("database_postgresql_cluster_arn", database.cluster_arn)
