import pulumi
from constants import LAMBDA

# Import pulumi provider methods.
from .ecr import repository
from .image import image
from nuage_provider.container_function import ContainerFunction, ContainerFunctionArgs
from nuage_provider.models import ScheduleConfig

# Lambda Container
function = ContainerFunction(
    LAMBDA["NAME"],
    args=ContainerFunctionArgs(
        name=LAMBDA["NAME"],
        name_prefix=None,
        description="Integration Tests Lambda Function",
        image_uri=image.uri,
        architecture=LAMBDA["ARCHITECTURE"],
        memory_size=LAMBDA["MEMORY"],
        timeout=LAMBDA["TIMEOUT"],
        environment={"ENV_TEST_VAL": LAMBDA["ENV_TEST_VAL"]},
        policy_document=None,
        keep_warm=True,
        url_enabled=False,
        schedule_config=ScheduleConfig(
            schedule_expression="rate(5 minutes)",
            schedule_input=None,
        ),
        log_retention_in_days=90,
    ),
    opts=pulumi.ResourceOptions(parent=repository),
)
pulumi.export("lambda_arn", function.function.arn)
pulumi.export("lambda_name", function.function.name)
pulumi.export("lambda_role_arn", function.role.arn)
if function.url:
    pulumi.export("lambda_function_url", function.url)
