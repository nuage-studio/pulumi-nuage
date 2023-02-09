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
from dataclasses import dataclass
from typing import Any, Dict, Optional

import pulumi
import pulumi_aws as aws

from .base.PrefixedComponentResource import (
    PrefixedComponentResource,
    PrefixedComponentResourceArgs,
)


@dataclass
class RepositoryArgs(PrefixedComponentResourceArgs):
    expire_in_days: Optional[pulumi.Input[int]]

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "RepositoryArgs":
        return RepositoryArgs(
            name=inputs.get("name", None),
            name_prefix=inputs.get("namePrefix", None),
            expire_in_days=inputs.get("expireInDays", 30),
        )


class Repository(PrefixedComponentResource):
    registry_id: pulumi.Output[str]
    name: pulumi.Output[str]
    url: pulumi.Output[str]
    id: pulumi.Output[int]
    arn: pulumi.Output[int]

    def __init__(
        self,
        resource_name: str,
        args: RepositoryArgs,
        props: Optional[dict] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:

        super().__init__("nuage:aws:Repository", resource_name, args, props, opts)

        # Create repository. Adding force_delete to allow deletion even if it contains images.
        repository = aws.ecr.Repository(
            resource_name, name=self.name, force_delete=True
        )

        # If expire days is greater than zero, define LifecyclePolicy.
        if args.expire_in_days > 0:
            repository_lifecycle = aws.ecr.LifecyclePolicy(
                resource_name,
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
            "id": repository.id,
            "arn": repository.arn,
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
