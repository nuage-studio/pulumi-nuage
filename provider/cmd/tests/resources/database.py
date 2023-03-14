"""An AWS Python Pulumi program"""

import pulumi

# Import pulumi provider methods.
from nuage_provider.serverless_database import ServerlessDatabase, ServerlessDatabaseArgs

from constants import DB

# Linked resources
from .vpc import private_subnet_1, private_subnet_2, public_subnet_1, public_subnet_2, vpc

# MySQL DATABASE
database = ServerlessDatabase(
    DB["MYSQL_NAME"],
    args=ServerlessDatabaseArgs(
        name=DB["MYSQL_NAME"],
        name_prefix=None,
        vpc_id=vpc.id,
        subnet_ids=[public_subnet_1.id, public_subnet_2.id],
        database_type="mysql",
        database_name=DB["MYSQL_NAME"],
        master_username=DB["USER"],
        ip_whitelist=None,
        skip_final_snapshot=True,
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

# # PostgreSQL DATABASE
database = ServerlessDatabase(
    DB["POSTGRESQL_NAME"],
    args=ServerlessDatabaseArgs(
        name=DB["POSTGRESQL_NAME"],
        name_prefix=None,
        vpc_id=vpc.id,
        subnet_ids=[private_subnet_1.id, private_subnet_2.id],
        database_type="postgresql",
        database_name=DB["POSTGRESQL_NAME"],
        master_username=DB["USER"],
        ip_whitelist=None,
        skip_final_snapshot=True,
        bastion_enabled=True,
        bastion_subnet_id=public_subnet_1.id,
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
