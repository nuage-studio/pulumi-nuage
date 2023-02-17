import json
import boto3
import pytest
from ..constants import GLOBAL, ECR_NAME

"""
class TestEcrRepository:
    # class: the fixture is destroyed during teardown of the last test in the class.
    @pytest.fixture(scope="class")
    def ecr_client(self):
        return boto3.Session(profile_name=GLOBAL["AWS_PROFILE"]).client(
            "ecr", region_name=GLOBAL["REGION_NAME"]
        )

    def test_lifecycle_policy_days(self, stack_outputs, ecr_client):
        # Test if lambda name setting is valid.
        response = ecr_client.get_lifecycle_policy(
            registryId=stack_outputs.get("ecr_registry_id").value,
            repositoryName=stack_outputs.get("ecr_repository_name").value,
        )
        policy = json.loads(response["lifecyclePolicyText"])
        assert policy["rules"][0]["selection"]["countNumber"] == 30

    def test_repository_exists(self, stack_outputs, ecr_client):
        # Test if lambda function is created successfully.
        response = ecr_client.describe_repositories(
            registryId=stack_outputs.get("ecr_registry_id").value,
            repositoryNames=[
                stack_outputs.get("ecr_repository_name").value,
            ],
        )
        assert len(response["repositories"]) > 0
"""
