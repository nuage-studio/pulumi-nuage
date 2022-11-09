import os
import unittest

import boto3
from pulumi import automation as auto

from constants import GLOBAL
from test_database import TestsDB


class TestS3(unittest.TestCase, TestsDB):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Setup Pulumi stack
        """
        cls.STACK_NAME = GLOBAL["STACK_NAME"]
        cls.REGION_NAME = GLOBAL["REGION_NAME"]
        cls.WORK_DIR = os.path.join(os.path.dirname(__file__))

        cls.stack = auto.create_or_select_stack(
            stack_name=cls.STACK_NAME, work_dir=cls.WORK_DIR
        )
        cls.stack.set_config("aws:region", auto.ConfigValue(value=cls.REGION_NAME))

        cls.stack.up(on_output=print)
        cls.outputs = cls.stack.outputs()

        # S3 related config.
        cls.FILE_NAME = "bucket-test.txt"
        cls.s3 = boto3.resource("s3")
        cls.lambda_client = boto3.client("lambda")

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Destroy the current stack.
        """
        cls.stack.destroy(on_output=print)
        cls.stack.workspace.remove_stack(cls.STACK_NAME)


if __name__ == "__main__":
    unittest.main()
