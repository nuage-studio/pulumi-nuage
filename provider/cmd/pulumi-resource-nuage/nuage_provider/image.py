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

from dataclasses import dataclass
from typing import Any, Dict, Optional

import pulumi
import pulumi_aws as aws
import pulumi_docker as docker

from .models import Architecture


@dataclass
class ImageArgs:
    context: Optional[pulumi.Input[str]]
    dockerfile: pulumi.Input[str]
    target: Optional[pulumi.Input[str]]
    architecture: Optional[str]
    repository_url: pulumi.Input[str]

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "ImageArgs":
        return ImageArgs(
            context=inputs.get("context", "./"),
            dockerfile=inputs.get("dockerfile"),
            target=inputs.get("target", None),
            architecture=inputs.get("architecture", Architecture.X86_64.value),
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

        architecture = Architecture[args.architecture]

        # FIXME: There is no cache-to and extra_options parameter in Pulumi Docker 4.0 (Only cache_from)
        # if os.getenv("GITHUB_ACTIONS"):
        #    # If we're running on a GitHub Actions runner, enable Caching API
        #    extra_options += ["--cache-to=type=gha,mode=max", "--cache-from=type=gha"]

        build = docker.DockerBuildArgs(
            context=args.context,
            dockerfile=args.dockerfile,
            target=args.target,
            platform=architecture.docker_value,
            # cache_from=docker.CacheFromArgs(images=["type=gha"]),
        )

        # Authenticate with ECR and get credentials
        registry_id = args.repository_url.apply(lambda x: x.split(".")[0])
        auth = aws.ecr.get_authorization_token(registry_id=registry_id)

        ecr_uri = pulumi.Output.all(url=args.repository_url, name=resource_name).apply(
            lambda args: f"{args['url']}:{args['name']}"
        )

        self.name = f"{pulumi.get_organization()}:{resource_name}"
        # Build and Push docker Image.
        image = docker.Image(
            resource_name,
            build=build,
            image_name=ecr_uri,
            # FIXME: local_image_name doesn't exists in Docker 4.0 yet
            # local_image_name=self.name,
            registry=docker.RegistryArgs(
                server=auth.proxy_endpoint,
                username=auth.user_name,
                password=auth.password,
            ),
            opts=pulumi.ResourceOptions(parent=self, ignore_changes=[]),
        )

        outputs = {
            "uri": image.image_name,
            "repo_digest": image.repo_digest,
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
