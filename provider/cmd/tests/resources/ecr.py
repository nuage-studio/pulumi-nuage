"""An AWS Python Pulumi program"""

import pulumi
from constants import ECR_NAME

# Import pulumi provider methods.
from nuage_provider.ecr_repository import (
    EcrRepository,
    EcrRepositoryArgs,
)

repository = EcrRepository(
    ECR_NAME,
    args=EcrRepositoryArgs(name=ECR_NAME, name_prefix=None, expire_in_days=30),
)
pulumi.export("ecr_repository_name", repository.name)
pulumi.export("ecr_registry_id", repository.registry_id)
