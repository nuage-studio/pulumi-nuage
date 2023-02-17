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
    DB["MYSQL_NAME"],
    args=ServerlessDatabaseArgs(
        name=DB["MYSQL_NAME"],
        name_prefix=None,
        vpc_id=vpc.vpc_id,
        vpc_subnets=vpc.public_subnet_ids,
        database_type="mysql",
        database_name=DB["MYSQL_NAME"],
        master_username=DB["USER"],
        ip_whitelist=None,
        skip_final_snapshot=True,
        data_api=False,
        bastion_enabled=False,
        bastion_subnet_id=None,
    ),
)
pulumi.export("database_mysql_user", database.user)
pulumi.export("database_mysql_password", database.password)
pulumi.export("database_mysql_name", database.database_name)
pulumi.export("database_mysql_port", database.port)
pulumi.export("database_mysql_host", database.host)
pulumi.export("database_mysql_uri", database.uri)
pulumi.export("database_mysql_cluster_arn", database.cluster_arn)

# PostgreSQL DATABASE
database = ServerlessDatabase(
    DB["POSTGRESQL_NAME"],
    args=ServerlessDatabaseArgs(
        name=DB["POSTGRESQL_NAME"],
        name_prefix=None,
        vpc_id=vpc.vpc_id,
        vpc_subnets=vpc.private_subnet_ids,
        database_type="postgresql",
        database_name=DB["POSTGRESQL_NAME"],
        master_username=DB["USER"],
        ip_whitelist=None,
        skip_final_snapshot=True,
        data_api=False,
        bastion_enabled=True,
        bastion_subnet_id=vpc.public_subnet_ids[0],
    ),
)

pulumi.export("database_postgresql_user", database.user)
pulumi.export("database_postgresql_password", database.password)
pulumi.export("database_postgresql_name", database.database_name)
pulumi.export("database_postgresql_port", database.port)
pulumi.export("database_postgresql_host", database.host)
pulumi.export("database_postgresql_uri", database.uri)
pulumi.export("database_postgresql_bastion_ip", database.bastion_ip)
pulumi.export("database_postgresql_bastion_private_key", database.bastion_private_key)
