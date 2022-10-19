
import os
import unittest

import boto3
from pulumi import automation as auto

from constants import BUCKET_NAME, GLOBAL

class TestS3(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
        Setup Pulumi stack
        """
        cls.STACK_NAME = GLOBAL['STACK_NAME']
        cls.REGION_NAME = GLOBAL['REGION_NAME']
        cls.WORK_DIR = os.path.join(os.path.dirname(__file__))

        cls.stack = auto.create_or_select_stack(stack_name=cls.STACK_NAME, work_dir=cls.WORK_DIR)
        cls.stack.set_config("aws:region", auto.ConfigValue(value=cls.REGION_NAME))
        
        cls.stack.up(on_output=print)
        cls.outputs = cls.stack.outputs()

        # S3 related config.
        cls.FILE_NAME = 'bucket-test.txt'
        cls.s3 = boto3.resource('s3')

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Destroy the current stack.
        """
        cls.stack.destroy(on_output=print)
        cls.stack.workspace.remove_stack(cls.STACK_NAME)

    def test_s3_output_name(self):
        # Test if bucket name setting is valid.
        bucket_name = self.outputs.get("bucketName").value
        self.assertIn(f"{BUCKET_NAME}-bucket", bucket_name)

    def test_s3_exist(self):
        # Test if bucket is created successfully.
        buckets = self.s3.buckets.all()
        bucket_names = []
        for bucket in buckets:
            bucket_names.append(bucket.name)
        
        bucket_name = self.outputs.get("bucketName").value
        self.assertIn(bucket_name, bucket_names)

    def test_s3_create_permission(self):
        # Test creating a file in new s3 bucket.
        bucket_name = self.outputs.get("bucketName").value
        created_response = self.s3.Bucket(bucket_name).put_object(Key=self.FILE_NAME, Body='Hi')
        self.assertEqual(created_response.key, self.FILE_NAME)

    def test_s3_delete_permission(self):
        # Test deleting the created file in new s3 bucket.
        bucket_name = self.outputs.get("bucketName").value
        delete_response = self.s3.meta.client.delete_object(Bucket=bucket_name, Key=self.FILE_NAME)
        self.assertIsNotNone(delete_response)


if __name__ == '__main__':
    unittest.main()