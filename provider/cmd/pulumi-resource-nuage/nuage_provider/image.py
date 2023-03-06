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
import tempfile
from dataclasses import dataclass
from typing import Any, List, Dict, Optional

import pulumi
import pulumi_aws as aws
import pulumi_docker as docker
from pulumi_command import local

from .prefixed_component_resource import (
    PrefixedComponentResource,
    PrefixedComponentResourceArgs,
)


@dataclass
class ImageArgs:
    args: pulumi.Input[docker.docker.DockerBuild]
    repository_url: pulumi.Input[str]
    # args: Optional[pulumi.Input[Dict[str, str]]] = None
    # cache_from: Optional[pulumi.Input[docker.CacheFrom]] = None
    # context: Optional[pulumi.Input[str]] = None
    # dockerfile: Optional[pulumi.Input[str]] = None
    # env: Optional[pulumi.Input[Dict[str, str]]] = None
    # extra_options: Optional[pulumi.Input[List[str]]] = None
    # target: Optional[pulumi.Input[str]] = None

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "ImageArgs":
        return ImageArgs(
            args=docker.docker.DockerBuild(
                args=inputs.get("args", None),
                cache_from=inputs.get("cacheFrom", None),
                context=inputs.get("context", None),
                dockerfile=inputs.get("dockerfile", None),
                env=inputs.get("env", None),
                extra_options=inputs.get("extraOptions", []),
                target=inputs.get("target", None),
            ),
            repository_url=inputs.get("repositoryUrl", None),
        )


class Image(pulumi.ComponentResource):
    name: pulumi.Output[str]
    uri: pulumi.Output[str]

    def __init__(
        self,
        resource_name: str,
        args: ImageArgs,
        props: Optional[dict] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        super().__init__("nuage:aws:Image", resource_name, props, opts)

        docker_args: docker.docker.DockerBuild = args.args

        if not docker_args.extra_options:
            docker_args.extra_options = []
        if "--platform" not in docker_args.extra_options:
            docker_args.extra_options += ["--platform", "linux/amd64"]
        if "--quiet" not in docker_args.extra_options:
            docker_args.extra_options.append("--quiet")

        if os.getenv("GITHUB_ACTIONS"):
            # If we're running on a GitHub Actions runner, enable Caching API
            extra_options += ["--cache-to=type=gha,mode=max", "--cache-from=type=gha"]

        if docker_args.dockerfile:
            # Use specified dockerfile.
            build = docker.DockerBuild(
                context=docker_args.context or "./",
                dockerfile=docker_args.dockerfile,
                extra_options=docker_args.extra_options,
                target=docker_args.target,
                env=docker_args.env,
                cache_from=docker_args.cache_from,
                args=docker_args.args,
            )
            image_ignore_changes = []
        else:
            tmp = tempfile.NamedTemporaryFile(dir="./", delete=True)
            # Use default aws lambda docker image.
            with open(tmp.name, "w") as f:
                f.writelines(
                    [
                        "FROM public.ecr.aws/lambda/provided:al2",
                        "\n" 'CMD [ "function.handler" ]',
                    ]
                )

            build = docker.DockerBuild(
                context="./",
                dockerfile=tmp.name,
                extra_options=extra_options,
            )
            # Ignore changes on image_name if default docker image is used.
            image_ignore_changes = ["image_name"]

        # Authenticate with ECR and get cridentals.
        registry_id = args.repository_url.apply(lambda x: x.split(".")[0])
        auth = aws.ecr.get_authorization_token(registry_id=registry_id)

        self.image_uri = pulumi.Output.all(
            url=args.repository_url, name=resource_name
        ).apply(lambda args: f"{args['url']}:{args['name']}")
        # Build and Push docker Image.
        image = docker.Image(
            resource_name,
            build=build,
            image_name=self.image_uri,
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

        # Untag ecs urls and keep only {pulumi.get_organization()}:{resource_name}.
        image.image_name.apply(
            lambda generated_image_name: (
                local.Command(
                    resource_name,
                    create=self.image_uri.apply(
                        lambda image_uri: f"docker rmi {image_uri} && docker rmi {generated_image_name}"
                    ),
                    opts=pulumi.ResourceOptions(parent=image),
                )
            )
        )

        outputs = {
            "name": image.image_name,
            "uri": self.image_uri,
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
