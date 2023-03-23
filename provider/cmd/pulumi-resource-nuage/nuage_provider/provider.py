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

import pulumi.provider as provider
from pulumi import Inputs, ResourceOptions
from pulumi.provider import ConstructResult

import nuage_provider
from nuage_provider.bastion import Bastion, BastionArgs
from nuage_provider.container_function import ContainerFunction, ContainerFunctionArgs
from nuage_provider.image import Image, ImageArgs
from nuage_provider.repository import Repository, RepositoryArgs
from nuage_provider.serverless_database import ServerlessDatabase, ServerlessDatabaseArgs


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
        if resource_type == "nuage:aws:ContainerFunction":
            return _create_function(name, inputs, options)
        elif resource_type == "nuage:aws:Repository":
            return _create_repository(name, inputs, options)
        elif resource_type == "nuage:aws:ServerlessDatabase":
            return _create_database(name, inputs, options)
        elif resource_type == "nuage:aws:Bastion":
            return _create_bastion(name, inputs, options)
        elif resource_type == "nuage:aws:Image":
            return _create_image(name, inputs, options)

        raise Exception(f"Unknown resource type {resource_type}")


def _create_bastion(name: str, inputs: Inputs, options: Optional[ResourceOptions] = None):
    bastion = Bastion(name, BastionArgs.from_inputs(inputs), dict(inputs), options)
    return provider.ConstructResult(
        urn=bastion.urn,
        state={
            "private_key_pem": bastion.private_key_pem,
            "public_ip": bastion.public_ip,
        },
    )


def _create_database(name: str, inputs: Inputs, options: Optional[ResourceOptions] = None) -> ConstructResult:
    database = ServerlessDatabase(name, ServerlessDatabaseArgs.from_inputs(inputs), dict(inputs), options)
    return provider.ConstructResult(
        urn=database.urn,
        state={
            "user": database.user,
            "host": database.host,
            "port": database.port,
            "name": database.name,
            "cluster_arn": database.cluster_arn,
            "uri": database.uri,
            "bastion_ip": database.bastion_ip,
            "bastion_private_key": database.bastion_private_key,
        },
    )


def _create_repository(name: str, inputs: Inputs, options: Optional[ResourceOptions] = None) -> ConstructResult:
    repository = Repository(name, RepositoryArgs.from_inputs(inputs), dict(inputs), options)

    return provider.ConstructResult(
        urn=repository.urn,
        state={
            "arn": repository.arn,
            "id": repository.id,
            "url": repository.url,
            "registry_id": repository.registry_id,
        },
    )


def _create_image(name: str, inputs: Inputs, options: Optional[ResourceOptions] = None) -> ConstructResult:
    image = Image(name, ImageArgs.from_inputs(inputs), dict(inputs), options)
    return provider.ConstructResult(
        urn=image.urn,
        state={
            "name": image.name,
            "uri": image.uri,
        },
    )


def _create_function(name: str, inputs: Inputs, options: Optional[ResourceOptions] = None) -> ConstructResult:
    function = ContainerFunction(name, ContainerFunctionArgs.from_inputs(inputs), dict(inputs), options)

    return provider.ConstructResult(
        urn=function.urn,
        state={
            "arn": function.arn,
            "name": function.name,
            "url": function.url,
        },
    )
