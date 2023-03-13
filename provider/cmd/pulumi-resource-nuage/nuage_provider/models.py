from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Dict, List, Optional

import pulumi
import pulumi_aws as aws


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


@dataclass
class ScheduleConfig:
    schedule_expression: pulumi.Input[str]
    schedule_input: Optional[pulumi.Input[Dict[str, pulumi.Input[Any]]]] = None

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "ScheduleConfig":
        return ScheduleConfig(
            schedule_expression=inputs.get("scheduleExpression"),
            schedule_input=inputs.get("scheduleInput", None),
        )


@dataclass
class UrlConfig:
    url_enabled: pulumi.Input[bool]
    cors_configuration: Optional[pulumi.Input[aws.lambda_.FunctionUrlCorsArgs]] = None

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "UrlConfig":
        return UrlConfig(
            url_enabled=inputs.get("urlEnabled", False),
            cors_configuration=inputs.get("corsConfiguration", None),
        )


@dataclass
class DockerBuild:
    context: Optional[pulumi.Input[str]]
    dockerfile: Optional[pulumi.Input[str]]
    env: Optional[pulumi.Input[Dict[str, Any]]]
    extra_options: Optional[pulumi.Input[List[str]]]
    target: Optional[pulumi.Input[str]]
    architecture: Optional[str]

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "DockerBuild":
        return DockerBuild(
            context=inputs.get("context", None),
            dockerfile=inputs.get("dockerfile", None),
            env=inputs.get("env", None),
            extra_options=inputs.get("extraOptions", []),
            target=inputs.get("target", None),
            architecture=inputs.get("architecture", "X86_64"),
        )
