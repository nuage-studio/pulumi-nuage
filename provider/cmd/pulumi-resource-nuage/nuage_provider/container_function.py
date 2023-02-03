# Copyright 2016-2021, Pulumi Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import string
from enum import IntEnum
from pathlib import Path
from typing import Dict, Optional, Union

import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx
import pulumi_docker as docker
import random

# from pulumi_command import local


class Architecture(IntEnum):
    """CPU architecture & instruction set to use"""

    X86_64 = 1
    ARM64 = 2

    @property
    def lambda_value(self) -> str:
        """AWS Lambda value for the `architectures` argument"""
        mapping = {self.X86_64.value: "x86_64", self.ARM64.value: "arm64"}
        return mapping[self.value]

    @property
    def docker_value(self) -> str:
        """Docker value for the `--platform` flag"""
        mapping = {self.X86_64.value: "linux/amd64", self.ARM64.value: "linux/arm64"}
        return mapping[self.value]


class ContainerFunctionArgs:
    name: Optional[pulumi.Input[str]]
    name_prefix: Optional[pulumi.Input[str]]
    description: Optional[pulumi.Input[str]]
    dockerfile: Optional[pulumi.Input[str]]
    context: Optional[pulumi.Input[str]]
    ecr_repository_name: pulumi.Input[str]
    architecture: Optional[str]
    memory_size: Optional[pulumi.Input[int]]
    timeout: Optional[pulumi.Input[int]]
    environment: Optional[pulumi.Input[Dict[str, pulumi.Input[str]]]]
    policy_document: Optional[pulumi.Input[str]]
    keep_warm: pulumi.Input[bool]
    url: pulumi.Input[bool]
    log_retention_in_days: pulumi.Input[int]
    # cors_configuration: Optional[pulumi.Input[aws.lambda_.FunctionUrlCorsArgs]]

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "ContainerFunctionArgs":
        return ContainerFunctionArgs(
            name=inputs.get("name", None),
            name_prefix=inputs.get("namePrefix", None),
            description=inputs.get("description", None),
            dockerfile=inputs.get("dockerfile", None),
            context=inputs.get("context", None),
            ecr_repository_name=inputs.get("ecrRepositoryName", None),
            architecture=inputs.get("architecture", "x86_64"),
            memory_size=inputs.get("memorySize", 512),
            timeout=inputs.get("timeout", 3),
            environment=inputs.get("environment", None),
            policy_document=inputs.get("policyDocument", None),
            keep_warm=inputs.get("keepWarm", False),
            url=inputs.get("url", False),
            log_retention_in_days=inputs.get("logRetentionInDays",90)
            # cors_configuration = None,#inputs['corsConfiguration'],
        )

    def __init__(
        self,
        name: Optional[pulumi.Input[str]],
        name_prefix: Optional[pulumi.Input[str]],
        description: Optional[pulumi.Input[str]],
        dockerfile: Optional[pulumi.Input[Union[str, Path]]],
        context: Optional[pulumi.Input[Union[str, Path]]],
        ecr_repository_name: Optional[pulumi.Input[str]],
        memory_size: Optional[pulumi.Input[int]],
        timeout: Optional[pulumi.Input[int]],
        architecture: Optional[pulumi.Input[str]],
        environment: Optional[pulumi.Input[Dict[str, pulumi.Input[str]]]],
        policy_document: Optional[pulumi.Input[str]],
        keep_warm: pulumi.Input[bool],
        url: pulumi.Input[bool],
        log_retention_in_days: pulumi.Input[int]
        # cors_configuration: Optional[pulumi.Input[aws.lambda_.FunctionUrlCorsArgs]] = None,
    ) -> None:
        self.name = name
        self.name_prefix = name_prefix
        self.description = description
        self.dockerfile = dockerfile
        self.context = context
        self.ecr_repository_name = ecr_repository_name
        self.architecture = architecture
        self.memory_size = memory_size
        self.timeout = timeout
        self.environment = environment
        self.policy_document = policy_document
        self.keep_warm = keep_warm
        self.url = url
        self.log_retention_in_days = log_retention_in_days
        # self.cors_configuration = cors_configuration


class ContainerFunction(pulumi.ComponentResource):
    def __init__(
        self,
        resource_name: str,
        args: ContainerFunctionArgs,
        props: Optional[dict] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:

        super().__init__("nuage:aws:ContainerFunction", resource_name, props, opts)
        if args.name_prefix and args.name:
            raise Exception("name and name_prefix cannot be set at the same time.")

        if args.name_prefix:
            suffix = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=5)
            )
            common_name: str = f"{args.name_prefix}-{suffix}"
        elif args.name:
            common_name = args.name
        else:
            common_name = resource_name

        if args.ecr_repository_name:
            # Get existing repository using repository name.
            repository = aws.ecr.get_repository_output(name=args.ecr_repository_name)
        else:
            # If repository is not defined, create new ecr repository using `name`.
            repository = aws.ecr.Repository(
                f"{common_name}-ecr-repository",
                name=f"{common_name}-repo",
            )

            repository_lifecycle = aws.ecr.LifecyclePolicy(
                f"{common_name}-ecr-lifecycle",
                repository=repository.name,
                policy=json.dumps(
                    {
                        "rules": [
                            {
                                "rulePriority": 1,
                                "description": "Expire images older than 30 days",
                                "selection": {
                                    "tagStatus": "untagged",
                                    "countType": "sinceImagePushed",
                                    "countUnit": "days",
                                    "countNumber": 30,
                                },
                                "action": {"type": "expire"},
                            }
                        ]
                    }
                ),
                opts=pulumi.ResourceOptions(parent=repository),
            )

        architecture = Architecture[args.architecture]

        extra_options = ["--platform", architecture.docker_value, "--quiet"]
        if os.getenv("GITHUB_ACTIONS"):
            # If we're running on a GitHub Actions runner, enable Caching API
            extra_options += ["--cache-to=type=gha,mode=max", "--cache-from=type=gha"]

        if args.dockerfile:
            # Use specified dockerfile.
            build = docker.DockerBuild(
                context=args.context or "./",
                dockerfile=args.dockerfile,
                extra_options=extra_options,
            )
            image_ignore_changes = []
        else:
            # Use default aws lambda docker image.
            with open("Dockerfile.awslambda.generated", "w") as f:
                f.writelines(
                    [
                        "FROM public.ecr.aws/lambda/provided:al2",
                        "\n" 'CMD [ "function.handler" ]',
                    ]
                )

            build = docker.DockerBuild(
                context="./",
                dockerfile="./Dockerfile.awslambda.generated",
                extra_options=extra_options,
            )
            # Ignore changes on image_name if default docker image is used.
            image_ignore_changes = ["image_name"]

        # Authenticate with ECR and get cridentals.
        registry_id = repository.repository_url.apply(lambda x: x.split(".")[0])
        auth = aws.ecr.get_authorization_token(registry_id=registry_id)

        # Build and Push docker Image.
        image = docker.Image(
            name=f"{common_name}-image",
            build=build,
            image_name=repository.repository_url,
            local_image_name=f"{pulumi.get_organization()}:{resource_name}",
            registry=docker.ImageRegistry(
                server=auth.proxy_endpoint,
                username=auth.user_name,
                password=auth.password,
            ),
            opts=pulumi.ResourceOptions(
                parent=self, ignore_changes=image_ignore_changes
            ),
        )

        # FIXME: Thhis doesn't work because pulumi Command doesn't have option to run on update right now
        # As it work only on create, it keeps having the same tag on updates
        # untag_command = local.Command(
        #    f"untag-{name}-image",
        #    create=repository_url.apply(
        #        lambda repository_url: f"docker rmi {repository_url}"
        #    ),
        #    opts=pulumi.ResourceOptions(depends_on=[image])
        # )

        # Define inline policies for role definition
        log_group = aws.cloudwatch.LogGroup(
            f"{common_name}-log-group",
            name=f"/aws/lambda/{common_name}",
            retention_in_days=args.log_retention_in_days,
        )
        lambda_logging = aws.iam.Policy(
            f"{common_name}-logging-policy",
            name=f"{common_name}-logging",
            path="/",
            description="IAM policy for logging from a lambda",
            policy=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
                            "Resource": "arn:aws:logs:*:*:*",
                            "Effect": "Allow",
                        }
                    ],
                }
            ),
        )

        policy_documents = [
            # Can write logs to CloudWatch
            aws.iam.RoleInlinePolicyArgs(
                name=f"{common_name}-logging-policy",
                policy=lambda_logging.policy,
            ),
            aws.iam.RoleInlinePolicyArgs(
                name=f"{common_name}-PolicyCloudWatchLambdaInsightsExecutionRolePolicy",
                policy=aws.iam.get_policy(
                    name="CloudWatchLambdaInsightsExecutionRolePolicy"
                ).policy,
            ),
            aws.iam.RoleInlinePolicyArgs(
                name=f"{common_name}-PolicyAWSXRayDaemonWriteAccess",
                policy=aws.iam.get_policy(name="AWSXRayDaemonWriteAccess").policy,
            ),
        ]
        if args.policy_document:
            # If we have a custom policy document, add it to the list
            policy_documents.append(
                aws.iam.RoleInlinePolicyArgs(
                    name=f"{common_name}-PolicyCustom",
                    policy=args.policy_document,
                )
            )

        self.role = aws.iam.Role(
            resource_name=f"{common_name}-lambda-role",
            name=f"{common_name}-lambda-role",
            description=f"Role used by {common_name}",
            assume_role_policy=aws.iam.get_policy_document(
                version="2012-10-17",
                statements=[
                    aws.iam.GetPolicyDocumentStatementArgs(
                        actions=["sts:AssumeRole"],
                        effect="Allow",
                        sid="",
                        principals=[
                            aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                                type="Service", identifiers=["lambda.amazonaws.com"]
                            ),
                        ],
                    ),
                ],
            ).json,
            inline_policies=policy_documents,
            opts=pulumi.ResourceOptions(parent=self),
        )

        # Lambda Function
        self.function = aws.lambda_.Function(
            resource_name=f"{common_name}-function",
            name=f"{common_name}",
            description=args.description,
            package_type="Image",
            image_uri=image.image_name,
            memory_size=args.memory_size,
            timeout=args.timeout,
            architectures=[architecture.lambda_value],
            role=self.role.arn,
            environment=(
                aws.lambda_.FunctionEnvironmentArgs(variables=args.environment)
                if args.environment
                else None
            ),
            tracing_config=aws.lambda_.FunctionTracingConfigArgs(mode="Active"),
            opts=pulumi.ResourceOptions(parent=self),
        )

        if args.keep_warm:
            # Keep warm by refreshing the lambda function every 5 minutes
            rule = aws.cloudwatch.EventRule(
                resource_name=f"{common_name}-keep-warm-rule",
                name=f"{common_name}-keep-warm",
                description=f"Refreshes {common_name} regularly to keep the container warm",
                is_enabled=True,
                role_arn=None,
                schedule_expression="rate(5 minutes)",
                opts=pulumi.ResourceOptions(parent=self.function),
            )
            aws.lambda_.Permission(
                resource_name=f"{common_name}-cloudwatch-invoke-permission",
                action="lambda:InvokeFunction",
                function=self.function.arn,
                principal="events.amazonaws.com",
                source_arn=rule.arn,
                opts=pulumi.ResourceOptions(parent=rule),
            )
            aws.cloudwatch.EventTarget(
                resource_name=f"{common_name}-keep-warm-target",
                arn=self.function.arn,
                input=json.dumps({"keep-warm": True}),
                rule=rule.id,
                opts=pulumi.ResourceOptions(parent=rule),
            )

        outputs = {"arn": self.function.arn, "name": self.function.name}

        if args.url:
            # Lambda URL
            self.function_url = aws.lambda_.FunctionUrl(
                resource_name=f"{common_name}-url",
                function_name=self.function.name,
                authorization_type="NONE",
                cors=None,  # args.cors_configuration,
                opts=pulumi.ResourceOptions(parent=self.function),
            )
            outputs["function_url"] = self.function_url.function_url
        else:
            self.function_url = None

        self.register_outputs(outputs)
