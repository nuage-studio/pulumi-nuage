"""An AWS Python Pulumi program"""

from os import name

import pulumi
import pulumi_awsx as awsx
from constants import BUCKET_NAME, LAMBDA

# Append provider root to path.
import sys
sys.path.append('../')

# Import pulumi provider methods.
from nuage_provider.bucket_nuage import bucket_nuage
from nuage_provider.container_function import ContainerFunction,ContainerFunctionArgs,Architecture

# S3 Bucket
bucket = bucket_nuage(name= BUCKET_NAME)
pulumi.export("bucketName", bucket.bucket.bucket)

# Lambda Container
function = ContainerFunction(
    name=LAMBDA["NAME"], 
    args= ContainerFunctionArgs(
        description="Integration Tests Lambda Function",
        dockerfile="./lambda/Dockerfile.lambda",
        context="./lambda/",
        ecr_repository_name="itest-lambda-ecr",
        architecture=LAMBDA["ARCHITECTURE"],
        memory_size=LAMBDA["MEMORY"],
        timeout=LAMBDA["TIMEOUT"],
        environment={LAMBDA["ENV_TEST_KEY"]:1},
        policy_document=None,
        keep_warm=True,
        url=False,    
))
pulumi.export("lambda_arn", function.function.arn)
pulumi.export("lambda_name", function.function.name)
pulumi.export("lambda_role_arn", function.role.arn)
if function.function_url:
    pulumi.export("lambda_function_url", function.function_url)