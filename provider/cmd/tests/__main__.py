"""An AWS Python Pulumi program"""
import os

full_test = os.environ.get("FULL_TEST", False)
# Import required resources for tests
if full_test:
    from resources import database

from resources import ecr, image, lambda_container
