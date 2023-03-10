import pulumi
import pulumi_aws as aws
from nuage_provider.container_function import ContainerFunction, ContainerFunctionArgs
from nuage_provider.models import ScheduleConfig, UrlConfig

from constants import LAMBDA

# Import pulumi provider methods.
from .ecr import repository
from .image import image

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
        schedule_config=ScheduleConfig(
            schedule_expression="rate(5 minutes)",
            schedule_input=None,
        ),
        url_config=UrlConfig(
            url_enabled=False,
            cors_configuration=aws.lambda_.FunctionUrlCorsArgs(
                allow_credentials=True,
                allow_origins=["*"],
                allow_methods=["*"],
                allow_headers=[
                    "date",
                    "keep-alive",
                ],
                expose_headers=[
                    "keep-alive",
                    "date",
                ],
                max_age=86400,
            ),
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
