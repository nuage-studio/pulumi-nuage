import pulumi
from typing import Any, Optional, Dict
from dataclasses import dataclass


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
