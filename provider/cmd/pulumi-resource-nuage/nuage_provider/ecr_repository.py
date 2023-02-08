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
from typing import Any, Dict, Optional
from dataclasses import dataclass

import pulumi
import pulumi_aws as aws
import pulumi_random as random


@dataclass
class EcrRepositoryArgs:
    name: Optional[pulumi.Input[str]]
    name_prefix: Optional[pulumi.Input[str]]
    expire_in_days: Optional[pulumi.Input[int]]
    # cors_configuration: Optional[pulumi.Input[aws.lambda_.FunctionUrlCorsArgs]]

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "EcrRepositoryArgs":
        return EcrRepositoryArgs(
            name=inputs.get("name", None),
            name_prefix=inputs.get("namePrefix", None),
            expire_in_days=inputs.get("expireInDays", 30)
            # cors_configuration = None,#inputs['corsConfiguration'],
        )


class EcrRepository(pulumi.ComponentResource):
    registry_id: pulumi.Output[str]
    name: pulumi.Output[str]
    url: pulumi.Output[str]
    repository_id: pulumi.Output[int]
    repository_arn: pulumi.Output[int]

    def __init__(
        self,
        resource_name: str,
        args: EcrRepositoryArgs,
        props: Optional[dict] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:

        super().__init__("nuage:aws:EcrRepository", resource_name, props, opts)
        # Use either name or name prefix.
        if args.name_prefix and args.name:
            raise Exception("name and name_prefix cannot be set at the same time.")

        # Parse name_prefix or name
        if args.name_prefix:
            suffix = random.RandomString(
                f"{args.name_prefix}-suffix", length=5, special=False
            ).result
            name: str = suffix.apply(lambda suffix: f"{args.name_prefix}-{suffix}")
        else:
            name = args.name if args.name else resource_name

        # Create repository. Adding force_delete to allow deletion even if it contains images.
        repository = aws.ecr.Repository(
            f"{resource_name}-ecr-repository", name=name, force_delete=True
        )

        # If expire days is greater than zero, define LifecyclePolicy.
        if args.expire_in_days > 0:
            repository_lifecycle = aws.ecr.LifecyclePolicy(
                f"{resource_name}-ecr-lifecycle",
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
                                    "countNumber": args.expire_in_days,
                                },
                                "action": {"type": "expire"},
                            }
                        ]
                    }
                ),
                opts=pulumi.ResourceOptions(parent=repository),
            )

        outputs = {
            "registry_id": repository.registry_id,
            "name": repository.name,
            "url": repository.repository_url,
            "repository_id": repository.id,
            "repository_arn": repository.arn,
        }

        self.set_outputs(outputs)

    def set_outputs(self, outputs: Dict[str, Any]):
        """
        Adds the Pulumi outputs as attributes on the current object so they can be
        used as outputs by the caller, as well as registering them.
        """
        for output_name in outputs.keys():
            setattr(self, output_name, outputs[output_name])

        self.register_outputs(outputs)
