#  Copyright 2016-2021, Pulumi Corporation.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import Optional
from venv import create

import pulumi.provider as provider
from pulumi import Inputs, ResourceOptions
from pulumi.provider import ConstructResult

import nuage_provider
from nuage_provider.bucket_nuage import bucket_nuage
from nuage_provider.container_function import ContainerFunction, ContainerFunctionArgs
from nuage_provider.serverless_database import (
    ServerlessDatabase,
    ServerlessDatabaseArgs,
)
from nuage_provider.bastion import Bastion, BastionArgs


class Provider(provider.Provider):
    def __init__(self) -> None:
        super().__init__(nuage_provider.__version__, nuage_provider.__schema__)

    def construct(
        self,
        name: str,
        resource_type: str,
        inputs: Inputs,
        options: Optional[ResourceOptions] = None,
    ) -> ConstructResult:

        if resource_type == "nuage:aws:bucket_nuage":
            return _create_bucket(name, inputs, options)
        elif resource_type == "nuage:aws:ContainerFunction":
            return _create_container(name, inputs, options)
        elif resource_type == "nuage:aws:ServerlessDatabase":
            return _create_database(name, inputs, options)
        elif resource_type == "nuage:aws:Bastion":
            return _create_bastion(name, inputs, options)

        raise Exception(f"Unknown resource type {resource_type}")


def _create_bastion(
    name: str, inputs: Inputs, options: Optional[ResourceOptions] = None
):
    created_resource = Bastion(
        name, BastionArgs.from_inputs(inputs), dict(inputs), options
    )
    return provider.ConstructResult(
        urn=created_resource.urn,
        state={
            "private_key_pem": created_resource.private_key_pem,
            "public_ip": created_resource.public_ip,
        },
    )


def _create_database(
    name: str, inputs: Inputs, options: Optional[ResourceOptions] = None
) -> ConstructResult:
    created_resource = ServerlessDatabase(
        name, ServerlessDatabaseArgs.from_inputs(inputs), dict(inputs), options
    )
    return provider.ConstructResult(
        urn=created_resource.urn,
        state={
            "user": created_resource.user,
            "host": created_resource.host,
            "port": created_resource.port,
            "name": created_resource.name,
            "cluster_arn": created_resource.cluster_arn,
            "uri": created_resource.uri,
            "bastion_ip": created_resource.bastion_ip,
            "bastion_private_key": created_resource.bastion_private_key,
        },
    )


def _create_container(
    name: str, inputs: Inputs, options: Optional[ResourceOptions] = None
) -> ConstructResult:
    created_container = ContainerFunction(
        name, ContainerFunctionArgs.from_inputs(inputs), dict(inputs), options
    )

    return provider.ConstructResult(
        urn=created_container.urn,
        state={
            "arn": created_container.function.arn,
            "name": created_container.function.name,
        },
    )


def _create_bucket(
    name: str, inputs: Inputs, options: Optional[ResourceOptions] = None
) -> ConstructResult:

    # Create the component resource
    created_bucket = bucket_nuage(name, dict(inputs), options)

    # Return the component resource's URN and outputs as its state.
    return provider.ConstructResult(
        urn=created_bucket.urn, state={"bucket": created_bucket.bucket}
    )
