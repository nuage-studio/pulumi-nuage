import pulumi
from constants import LAMBDA

# Import pulumi provider methods.
from nuage_provider.container_function import ContainerFunction, ContainerFunctionArgs

# Lambda Container
function = ContainerFunction(
    LAMBDA["NAME"],
    args=ContainerFunctionArgs(
        name=LAMBDA["NAME"],
        name_prefix=None,
        description="Integration Tests Lambda Function",
        dockerfile="./files/lambda/Dockerfile.lambda",
        context="./files/lambda/",
        repository_id="test-ecr",
        architecture=LAMBDA["ARCHITECTURE"],
        memory_size=LAMBDA["MEMORY"],
        timeout=LAMBDA["TIMEOUT"],
        environment={"ENV_TEST_VAL": LAMBDA["ENV_TEST_VAL"]},
        policy_document=None,
        keep_warm=True,
        url=False,
        log_retention_in_days=90,
    ),
)
pulumi.export("lambda_arn", function.function.arn)
pulumi.export("lambda_name", function.function.name)
pulumi.export("lambda_role_arn", function.role.arn)
pulumi.export("ecr_image_name", function.ecr_image_name)
if function.function_url:
    pulumi.export("lambda_function_url", function.function_url)
