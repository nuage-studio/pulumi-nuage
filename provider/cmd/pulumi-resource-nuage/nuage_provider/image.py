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
from typing import Any, Dict, Optional

import pulumi
import pulumi_aws as aws
import pulumi_docker as docker
from pulumi_command import local

from .models import Architecture, DockerBuild


@dataclass
class ImageArgs:
    build_args: pulumi.Input[DockerBuild]
    repository_url: pulumi.Input[str]

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "ImageArgs":
        return ImageArgs(
            build_args=DockerBuild.from_inputs(inputs.get("buildArgs")),
            repository_url=inputs.get("repositoryUrl"),
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

        architecture = Architecture[args.build_args.architecture]

        # FIXME: There is no cache-to and extra_options parameter in Pulumi Docker 4.0 (Only cache_from)
        # if os.getenv("GITHUB_ACTIONS"):
        #    # If we're running on a GitHub Actions runner, enable Caching API
        #    extra_options += ["--cache-to=type=gha,mode=max", "--cache-from=type=gha"]

        if args.build_args.dockerfile:
            # Use specified dockerfile.
            build = docker.DockerBuildArgs(
                context=args.build_args.context or "./",
                dockerfile=args.build_args.dockerfile,
                target=args.build_args.target,
                platform=architecture.docker_value,
                # cache_from=docker.CacheFromArgs(images=["type=gha"]),
            )
            image_ignore_changes = []
        else:
            tmp = tempfile.NamedTemporaryFile(dir="./", delete=True)
            # Use default aws lambda docker image.
            with open(tmp.name, "w") as f:
                f.writelines(
                    [
                        "FROM public.ecr.aws/lambda/provided:al2",
                        '\nCMD [ "function.handler" ]',
                    ]
                )

            build = docker.DockerBuildArgs(context="./", dockerfile=tmp.name, platform=architecture.docker_value)
            # Ignore changes on image_name if default docker image is used.
            image_ignore_changes = ["image_name"]

        # Authenticate with ECR and get cridentals.
        registry_id = args.repository_url.apply(lambda x: x.split(".")[0])
        auth = aws.ecr.get_authorization_token(registry_id=registry_id)

        self.image_uri = pulumi.Output.all(url=args.repository_url, name=resource_name).apply(
            lambda args: f"{args['url']}:{args['name']}"
        )

        self.name = f"{pulumi.get_organization()}:{resource_name}"
        # Build and Push docker Image.
        image = docker.Image(
            resource_name,
            build=build,
            image_name=self.image_uri,
            # FIXME: local_image_name doesn't exists in Docker 4.0 yet
            # local_image_name=self.name,
            registry=docker.RegistryArgs(
                server=auth.proxy_endpoint,
                username=auth.user_name,
                password=auth.password,
            ),
            opts=pulumi.ResourceOptions(parent=self, ignore_changes=image_ignore_changes),
        )

        outputs = {
            "uri": image.image_name,
            "name": self.name,
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
