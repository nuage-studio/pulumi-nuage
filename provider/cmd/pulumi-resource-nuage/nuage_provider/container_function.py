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
import os
import tempfile
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Dict, List, Optional

import pulumi
import pulumi_aws as aws
import pulumi_docker as docker
from pulumi_command import local

from .models import Architecture, ScheduleConfig, UrlConfig
from .prefixed_component_resource import PrefixedComponentResource, PrefixedComponentResourceArgs


@dataclass
class ContainerFunctionArgs(PrefixedComponentResourceArgs):
    description: Optional[pulumi.Input[str]]
    image_uri: pulumi.Input[str]
    architecture: Optional[str]
    memory_size: Optional[pulumi.Input[int]]
    timeout: Optional[pulumi.Input[int]]
    environment: Optional[pulumi.Input[Dict[str, pulumi.Input[str]]]]
    policy_document: Optional[pulumi.Input[str]]
    keep_warm: pulumi.Input[bool]
    log_retention_in_days: pulumi.Input[int]
    # Schedule
    schedule_config: Optional[pulumi.Input[ScheduleConfig]]
    url_config: Optional[pulumi.Input[UrlConfig]]

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "ContainerFunctionArgs":
        schedule_config = inputs.get("scheduleConfig", None)
        url_config = inputs.get("urlConfig", UrlConfig(url_enabled=False))

        return ContainerFunctionArgs(
            name=inputs.get("name", None),
            name_prefix=inputs.get("namePrefix", None),
            description=inputs.get("description", None),
            image_uri=inputs.get("imageUri"),
            architecture=inputs.get("architecture", "X86_64"),
            memory_size=int(inputs.get("memorySize", 512)),
            timeout=int(inputs.get("timeout", 3)),
            environment=inputs.get("environment", None),
            policy_document=inputs.get("policyDocument", None),
            keep_warm=inputs.get("keepWarm", False),
            log_retention_in_days=int(inputs.get("logRetentionInDays", 90)),
            schedule_config=ScheduleConfig.from_inputs(schedule_config) if schedule_config else None,
            url_config=UrlConfig.from_inputs(url_config) if url_config else None,
        )


class ContainerFunction(PrefixedComponentResource):
    arn: pulumi.Output[str]
    name: pulumi.Output[str]
    url: Optional[pulumi.Output[str]]

    def __init__(
        self,
        resource_name: str,
        args: ContainerFunctionArgs,
        props: Optional[dict] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        super().__init__("nuage:aws:ContainerFunction", resource_name, args, props, opts)
        architecture = Architecture[args.architecture]

        # Define inline policies for role definition
        log_group = aws.cloudwatch.LogGroup(
            resource_name,
            name=self.name_.apply(lambda name: f"/aws/lambda/{name}"),
            retention_in_days=args.log_retention_in_days,
            opts=pulumi.ResourceOptions(parent=self),
        )

        policy_documents: List[str] = [
            # Can write logs to CloudWatch
            aws.iam.RoleInlinePolicyArgs(
                name=self.get_suffixed_name("logging-policy"),
                policy=aws.iam.get_policy_document(
                    version="2012-10-17",
                    statements=[
                        aws.iam.GetPolicyDocumentStatementArgs(
                            actions=["logs:CreateLogStream", "logs:PutLogEvents"],
                            resources=log_group.arn.apply(lambda arn: [f"{arn}:*"]),
                            effect="Allow",
                        ),
                    ],
                ).json,
            ),
        ]
        if args.policy_document:
            # If we have a custom policy document, add it to the list
            policy_documents.append(
                aws.iam.RoleInlinePolicyArgs(
                    name=self.get_suffixed_name("custom-policy"),
                    policy=args.policy_document,
                )
            )

        self.role = aws.iam.Role(
            resource_name,
            name=self.name_,
            description=self.name_.apply(lambda name: f"Role used by {name}"),
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
            managed_policy_arns=[
                # FIXME: Right now, AWS_CLOUD_WATCH_LAMBDA_INSIGHTS_EXECUTION_ROLE_POLICY returns a wrong stirng with AWS prefix.
                # See https://github.com/pulumi/pulumi-aws/issues/2269
                "arn:aws:iam::aws:policy/CloudWatchLambdaInsightsExecutionRolePolicy",
                aws.iam.ManagedPolicy.AWSX_RAY_DAEMON_WRITE_ACCESS,
            ],
            inline_policies=policy_documents,
            opts=pulumi.ResourceOptions(parent=self),
        )

        # Lambda Function
        self.function = aws.lambda_.Function(
            resource_name,
            name=self.name_,
            description=args.description,
            package_type="Image",
            image_uri=args.image_uri,
            memory_size=args.memory_size,
            timeout=args.timeout,
            architectures=[architecture.lambda_value],
            role=self.role.arn,
            environment=(aws.lambda_.FunctionEnvironmentArgs(variables=args.environment) if args.environment else None),
            tracing_config=aws.lambda_.FunctionTracingConfigArgs(mode="Active"),
            opts=pulumi.ResourceOptions(parent=self, depends_on=[self.role]),
        )

        if args.keep_warm:
            # Keep warm by refreshing the lambda function every 5 minutes
            rule = aws.cloudwatch.EventRule(
                f"{resource_name}-keep-warm",
                name=self.get_suffixed_name("keep-warm"),
                description=self.name_.apply(lambda name: f"Refreshes {name} regularly to keep the container warm"),
                is_enabled=True,
                role_arn=None,
                schedule_expression="rate(5 minutes)",
                opts=pulumi.ResourceOptions(parent=self.function),
            )
            aws.lambda_.Permission(
                f"{resource_name}-keep-warm",
                action="lambda:InvokeFunction",
                function=self.function.arn,
                principal="events.amazonaws.com",
                source_arn=rule.arn,
                opts=pulumi.ResourceOptions(parent=rule),
            )
            aws.cloudwatch.EventTarget(
                f"{resource_name}-keep-warm",
                arn=self.function.arn,
                input=json.dumps({"keep-warm": True}),
                rule=rule.id,
                opts=pulumi.ResourceOptions(parent=rule),
            )

        if args.schedule_config:
            schedule_rule = aws.cloudwatch.EventRule(
                resource_name=f"{resource_name}-schedule",
                name=self.get_suffixed_name("schedule"),
                schedule_expression=args.schedule_config.schedule_expression,
                description=args.description,
                opts=pulumi.ResourceOptions(parent=self),
            )

            aws.cloudwatch.EventTarget(
                resource_name=f"{resource_name}-schedule",
                arn=self.function.arn,
                rule=schedule_rule.id,
                input=json.dumps(args.schedule_config.schedule_input or {}),
                opts=pulumi.ResourceOptions(parent=schedule_rule),
            )

            aws.lambda_.Permission(
                resource_name=f"{resource_name}-schedule",
                function=self.function.arn,
                action="lambda:InvokeFunction",
                principal="events.amazonaws.com",
                source_arn=schedule_rule.arn,
                opts=pulumi.ResourceOptions(parent=schedule_rule),
            )

        outputs = {"arn": self.function.arn, "name": self.function.name}

        if args.url_config.url_enabled:
            # Lambda URL
            self.function_url = aws.lambda_.FunctionUrl(
                resource_name,
                function_name=self.function.name,
                authorization_type="NONE",
                cors=args.url_config.cors_configuration,
                opts=pulumi.ResourceOptions(parent=self.function),
            )
            outputs["url"] = self.function_url.function_url
        else:
            outputs["url"] = None

        # Untag ecs urls and keep only {pulumi.get_organization()}:{resource_name}.
        # rsplit is because the generated name contains suffix at the end and we also need to untag image without that suffix
        args.image_uri.apply(
            lambda generated_image_name: (
                local.Command(
                    resource_name,
                    create=f"docker rmi {generated_image_name.rsplit('-', 1)[0]} && docker rmi {generated_image_name}",
                    opts=pulumi.ResourceOptions(parent=self.function),
                )
            )
        )

        self.set_outputs(outputs)

    def set_outputs(self, outputs: Dict[str, Any]):
        """
        Adds the Pulumi outputs as attributes on the current object so they can be
        used as outputs by the caller, as well as registering them.
        """
        for output_name in outputs.keys():
            setattr(self, output_name, outputs[output_name])

        self.register_outputs(outputs)
