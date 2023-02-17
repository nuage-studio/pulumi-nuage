import boto3
import pytest
from ..constants import GLOBAL, BUCKET_NAME

"""
class TestBucket:
    FILE_NAME = "bucket-test.txt"
    # class: the fixture is destroyed during teardown of the last test in the class.
    @pytest.fixture(scope="class")
    def s3_client(self):
        return boto3.Session(profile_name=GLOBAL["AWS_PROFILE"]).resource("s3")

    def test_s3_output_name(self, stack_outputs):
        # Test if bucket name setting is valid.
        bucket_name = stack_outputs.get("bucketName").value

        assert f"{BUCKET_NAME}-bucket" in bucket_name

    def test_s3_exist(self, stack_outputs, s3_client):
        # Test if bucket is created successfully.
        buckets = s3_client.buckets.all()
        bucket_names = []
        for bucket in buckets:
            bucket_names.append(bucket.name)

        bucket_name = stack_outputs.get("bucketName").value
        assert bucket_name in bucket_names

    def test_s3_create_permission(self, stack_outputs, s3_client):
        # Test creating a file in new s3 bucket.
        bucket_name = stack_outputs.get("bucketName").value
        created_response = s3_client.Bucket(bucket_name).put_object(
            Key=self.FILE_NAME, Body="Hi"
        )
        assert created_response.key == self.FILE_NAME

    def test_s3_delete_permission(self, stack_outputs, s3_client):
        # Test deleting the created file in new s3 bucket.
        bucket_name = stack_outputs.get("bucketName").value
        delete_response = s3_client.meta.client.delete_object(
            Bucket=bucket_name, Key=self.FILE_NAME
        )
        assert delete_response is not None
"""
