import pulumi
import pulumi_docker
from nuage_provider.image import Image, ImageArgs

from constants import LAMBDA

from .ecr import repository

IMAGE_NAME = "foo-test-image"
image = Image(
    IMAGE_NAME,
    args=ImageArgs(
        dockerfile="./Dockerfile.lambda",
        context="./files/lambda/",
        target=None,
        architecture=LAMBDA["ARCHITECTURE"],
        repository_url=repository.url,
    ),
)
pulumi.export("image_uri", image.uri)
pulumi.export("image_name", image.name)
