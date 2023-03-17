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
class BastionConfig:
    enabled: pulumi.Input[bool]
    subnet_id: Optional[pulumi.Input[str]]

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "BastionConfig":
        return BastionConfig(
            enabled=inputs.get("enabled"),
            subnet_id=inputs.get("subnetId", None),
        )
