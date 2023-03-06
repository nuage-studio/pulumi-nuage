import pulumi
import pulumi_docker
from nuage_provider.image import (
    Image,
    ImageArgs,
)
from .ecr import repository

image_args = pulumi_docker.docker.DockerBuild(
    dockerfile="./files/lambda/Dockerfile.lambda",
    context="./files/lambda/",
    extra_options=[],
)
IMAGE_NAME = "foo-test-image"
image = Image(
    IMAGE_NAME,
    args=ImageArgs(args=image_args, repository_url=repository.url),
)
pulumi.export("image_uri", image.uri)
# pulumi.export("ecr_registry_id", repository.registry_id)
