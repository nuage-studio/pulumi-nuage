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

import pulumi
import pulumi_aws as aws
import pulumi_docker as docker

from .models import Architecture


@dataclass
class ImageArgs:
    dockerfile: pulumi.Input[str]
    repository_url: pulumi.Input[str]
    context: pulumi.Input[str] | None = "./"
    target: pulumi.Input[str] | None
    architecture: str = Architecture.ARM64.value

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "ImageArgs":
        return ImageArgs(**inputs)


class Image(pulumi.ComponentResource):
    uri: pulumi.Output[str]

    def __init__(
        self,
        resource_name: str,
        args: ImageArgs,
        props: dict | None = None,
        opts: pulumi.ResourceOptions | None = None,
    ) -> None:
        super().__init__("nuage:aws:Image", resource_name, props, opts)

        self.uri = args.repository_url.apply(lambda url: f"{url}:{resource_name}")

        # FIXME: There is no cache-to and extra_options parameter in Pulumi Docker 4.0 (Only cache_from)
        # if os.getenv("GITHUB_ACTIONS"):
        #    # If we're running on a GitHub Actions runner, enable Caching API
        #    extra_options += ["--cache-to=type=gha,mode=max", "--cache-from=type=gha"]

        architecture = Architecture[args.architecture]
        build = docker.DockerBuildArgs(
            dockerfile=args.dockerfile,
            context=args.context,
            target=args.target,
            platform=architecture.docker_value,
            # cache_from=docker.CacheFromArgs(images=["type=gha"]),
            # cache_to=docker.CacheToArgs(mode="max", type="gha"),
        )

        # Authenticate with ECR and get credentials
        auth = aws.ecr.get_authorization_token()
        # Build and Push docker Image.
        image = docker.Image(
            resource_name,
            build=build,
            image_name=self.uri,
            # FIXME: local_image_name doesn't exists in Docker 4.0 yet
            # local_image_name=self.name,
            registry=docker.RegistryArgs(
                server=auth.proxy_endpoint,
                username=auth.user_name,
                password=auth.password,
            ),
            opts=pulumi.ResourceOptions(parent=self, ignore_changes=[]),
        )
        self.repo_digest = image.repo_digest
        self.register_outputs({"uri": self.uri, "repo_digest": self.repo_digest})
