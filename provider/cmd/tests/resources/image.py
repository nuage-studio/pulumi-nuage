import pulumi
import pulumi_docker
from nuage_provider.image import Image, ImageArgs
from nuage_provider.models import DockerBuild

from constants import LAMBDA

from .ecr import repository

image_args = DockerBuild(
    dockerfile="./Dockerfile.lambda",
    context="./files/lambda/",
    extra_options=[],
    env=None,
    target=None,
    architecture=LAMBDA["ARCHITECTURE"],
)
IMAGE_NAME = "foo-test-image"
image = Image(
    IMAGE_NAME,
    args=ImageArgs(build_args=image_args, repository_url=repository.url),
)
pulumi.export("image_uri", image.uri)
pulumi.export("image_name", image.name)
