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

import json
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, Optional, Union

import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx

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
    resource_name: Optional[pulumi.Input[str]]
    description: Optional[pulumi.Input[str]]
    dockerfile: Optional[pulumi.Input[str]]
    context: Optional[pulumi.Input[str]]
    repository: pulumi.Input[str]    
    ecr_repository_name: pulumi.Input[str]    
    architecture: Optional[str]
    memory_size: Optional[pulumi.Input[int]]
    timeout: Optional[pulumi.Input[int]]    
    environment: Optional[pulumi.Input[Dict[str, pulumi.Input[str]]]]
    policy_document: Optional[pulumi.Input[str]]
    keep_warm: pulumi.Input[bool]
    url: pulumi.Input[bool]
    #cors_configuration: Optional[pulumi.Input[aws.lambda_.FunctionUrlCorsArgs]]

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> 'ContainerFunctionArgs':
        return ContainerFunctionArgs(
            resource_name = inputs.get('resourceName', None),
            description = inputs.get('description', None),
            dockerfile = inputs.get('dockerfile', "./Dockerfile"),
            context = inputs.get('context', None),
            repository = inputs['repository'],
            ecr_repository_name = inputs['ecrRepositoryName'],
            architecture = inputs.get('architecture', "x86_64"),
            memory_size = inputs.get('memorySize', 512),
            timeout = inputs.get('timeout', 3),            
            environment = inputs.get('environment', None),
            policy_document = inputs.get('policyDocument', None),
            keep_warm = inputs.get('keepWarm', False),
            url = inputs.get('url', False),
            #cors_configuration = None,#inputs['corsConfiguration'],
        )        

    def __init__(
        self,         
        resource_name: Optional[pulumi.Input[str]],
        description: Optional[pulumi.Input[str]],
        dockerfile: Optional[pulumi.Input[Union[str, Path]]],
        context: Optional[pulumi.Input[Union[str, Path]]],
        repository: Optional[pulumi.Input[str]],
        ecr_repository_name: Optional[pulumi.Input[str]], 
        memory_size: Optional[pulumi.Input[int]],
        timeout: Optional[pulumi.Input[int]],
        architecture: Optional[pulumi.Input[str]],
        environment: Optional[pulumi.Input[Dict[str, pulumi.Input[str]]]],
        policy_document: Optional[pulumi.Input[str]],
        keep_warm: pulumi.Input[bool],
        url: pulumi.Input[bool]
        #cors_configuration: Optional[pulumi.Input[aws.lambda_.FunctionUrlCorsArgs]] = None,
    ) -> None:
        self.resource_name = resource_name
        self.description = description
        self.dockerfile = dockerfile
        self.context = context
        self.repository = repository
        self.ecr_repository_name = ecr_repository_name                
        self.architecture = architecture
        self.memory_size = memory_size
        self.timeout = timeout        
        self.environment = environment
        self.policy_document = policy_document
        self.keep_warm = keep_warm
        self.url = url
        #self.cors_configuration = cors_configuration

class ContainerFunction(pulumi.ComponentResource):

    def __init__(self, name: str, args: ContainerFunctionArgs, props: Optional[dict] = None, opts: Optional[pulumi.ResourceOptions] = None) -> None:

        super().__init__("nuage:aws:ContainerFunction", name, props, opts)
        
        if args.repository:
            repository = aws.ecr.get_repository(name=args.repository).repository_url
        else:
            repository = awsx.ecr.Repository(
                resource_name=f"{args.ecr_repository_name}-repository",
                name=args.ecr_repository_name,
            ).url
        architecture = Architecture[args.architecture] 
        #if args.architecture == "x86_64":
        #    architecture = Architecture.X86_64
        #else:
        #    architecture = Architecture.ARM64
        
        image = awsx.ecr.Image(
            resource_name=f"{name}-image",
            repository_url=repository,
            path=args.context,
            dockerfile=args.dockerfile,
            extra_options=["--platform", architecture.docker_value, "--quiet"],
            opts=pulumi.ResourceOptions(parent=self),
        )

        policy_documents = [
            # Can write logs to CloudWatch
            aws.iam.RoleInlinePolicyArgs(   
                name="PolicyAWSLambdaBasicExecutionRole",
                policy=aws.iam.get_policy(name="AWSLambdaBasicExecutionRole").policy,
            ),
            aws.iam.RoleInlinePolicyArgs(   
                name="PolicyCloudWatchLambdaInsightsExecutionRolePolicy",
                policy=aws.iam.get_policy(name="CloudWatchLambdaInsightsExecutionRolePolicy").policy,
            ),
            aws.iam.RoleInlinePolicyArgs(   
                name="PolicyAWSXRayDaemonWriteAccess",
                policy=aws.iam.get_policy(name="AWSXRayDaemonWriteAccess").policy,
            )
        ]
        if args.policy_document:
            # If we have a custom policy document, add it to the list
            policy_documents.append(aws.iam.RoleInlinePolicyArgs(   
                name="PolicyCustom",
                policy=args.policy_document,
            ))

        self.role = aws.iam.Role(
            resource_name=f"{name}-lambda-role",
            name=f"{name}-lambda-role",
            description=f"Role used by {name}",
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
                

        #policy = aws.iam.Policy(
        #    resource_name=f"{name}-lambda-policy",
        #    name=f"{name}-lambda-policy",
        #    description=f"Policy for {name}-lambda-function",
        #    policy=aws.iam.get_policy_document(source_policy_documents=policy_documents).json,
        #    opts=pulumi.ResourceOptions(parent=self.role),
        #)

        #aws.iam.RolePolicyAttachment(
        #    resource_name=f"{name}-lambda-role-policy-attachment",
        #    role=self.role.id,
        #    policy_arn=policy.arn,
        #    opts=pulumi.ResourceOptions(parent=self.role),
        #)

        self.function = aws.lambda_.Function(
            resource_name=args.resource_name or name,
            name=name,
            description=args.description,
            package_type="Image",
            image_uri=image.image_uri,
            memory_size=args.memory_size,
            timeout=args.timeout,
            architectures=[architecture.lambda_value],
            role=self.role.arn,
            environment=aws.lambda_.FunctionEnvironmentArgs(variables=args.environment) if args.environment else None,
            tracing_config=aws.lambda_.FunctionTracingConfigArgs(mode="Active"),
            opts=pulumi.ResourceOptions(parent=self),
        )

        if args.keep_warm:
            # Keep warm by refreshing the lambda function every 5 minutes
            rule = aws.cloudwatch.EventRule(
                resource_name=f"{name}-keep-warm-rule",
                description=f"Refreshes {name} regularly to keep the container warm",
                is_enabled=True,
                role_arn=None,
                schedule_expression="rate(5 minutes)",
                opts=pulumi.ResourceOptions(parent=self.function),
            )
            aws.lambda_.Permission(
                resource_name=f"{name}-cloudwatch-invoke-permission",
                action="lambda:InvokeFunction",
                function=self.function.arn,
                principal="events.amazonaws.com",
                source_arn=rule.arn,
                opts=pulumi.ResourceOptions(parent=rule),
            )
            aws.cloudwatch.EventTarget(
                resource_name=f"{name}-keep-warm-target",
                arn=self.function.arn,
                input=json.dumps({"keep-warm":True}),
                rule=rule.id,
                opts=pulumi.ResourceOptions(parent=rule),
            )

        outputs = {"arn": self.function.arn, "name": self.function.name}

        if args.url:
            # Lambda URL
            self.function_url = aws.lambda_.FunctionUrl(
                resource_name=f"{name}/url",
                function_name=self.function.name,
                authorization_type="NONE",
                cors=None,#args.cors_configuration,
                opts=pulumi.ResourceOptions(parent=self.function),
            )
            outputs["function_url"] = self.function_url.function_url
        else:
            self.function_url = None

        self.register_outputs(outputs)
