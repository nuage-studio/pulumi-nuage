"""An AWS Python Pulumi program"""

from os import name
import pulumi
import pulumi_awsx as awsx
from constants import BUCKET_NAME, LAMBDA_NAME

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
    name=LAMBDA_NAME, 
    args= ContainerFunctionArgs(
    description="Integration Tests Lambda Function",
    timeout=30,
    keep_warm=True,
    architecture=Architecture.X86_64,
    ecr_repository_name="itest-lambda-ecr",
    ecr_repository_resource_name="itest-lambda-ecr-repository",
    dockerfile="./lambda/Dockerfile.lambda",
    context="./lambda/",
    url=False,
    environment={"TEST":1}
))
pulumi.export("lambda_arn", function.function.arn)
pulumi.export("lambda_name", function.function.name)
if function.function_url:
    pulumi.export("lambda_function_url", function.function_url)