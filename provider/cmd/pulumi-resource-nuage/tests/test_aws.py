
import os
import json
import unittest

import boto3
from pulumi import automation as auto
from pulumi_aws.s3.bucket import Bucket

from constants import BUCKET_NAME, GLOBAL, LAMBDA

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
        cls.lambda_client = boto3.client('lambda')

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

    def test_lambda_output_name(self):
        # Test if lambda name setting is valid.
        lambda_name = self.outputs.get("lambda_name").value
        self.assertEqual(LAMBDA["NAME"], lambda_name)

    def test_lambda_exists(self):
        # Test if lambda function is created successfully.
        functions = self.lambda_client.list_functions()['Functions']
        function_names = [function['FunctionName'] for function in functions]
        
        lambda_name = self.outputs.get("lambda_name").value
        self.assertIn(lambda_name, function_names)

    def test_lambda_role(self):
        # Test if lambda has true role linked.
        functions = self.lambda_client.list_functions()['Functions']
        lambda_name = self.outputs.get("lambda_name").value
        role_arn = self.outputs.get("lambda_role_arn").value
        
        function_role = None
        for function in functions:
            if function['FunctionName'] == lambda_name:
                function_role = function['Role']
                break 

        self.assertEqual(function_role, role_arn)   

    def test_lambda_timeout(self):
        # Test if lambda has correct timeout value.
        functions = self.lambda_client.list_functions()['Functions']
        lambda_name = self.outputs.get("lambda_name").value
        
        timeout = None
        for function in functions:
            if function['FunctionName'] == lambda_name:
                timeout = function['Timeout']
                break 

        self.assertEqual(timeout, LAMBDA["TIMEOUT"])  

    def test_lambda_memory(self):
        # Test if lambda has correct memory value.
        functions = self.lambda_client.list_functions()['Functions']
        lambda_name = self.outputs.get("lambda_name").value
        
        memory = None
        for function in functions:
            if function['FunctionName'] == lambda_name:
                memory = function['MemorySize']
                break 

        self.assertEqual(memory, LAMBDA["MEMORY"])    

    def test_lambda_architecture(self):
        # Test if lambda has correct memory value.
        functions = self.lambda_client.list_functions()['Functions']
        lambda_name = self.outputs.get("lambda_name").value
        
        architecture = None
        for function in functions:
            if function['FunctionName'] == lambda_name:
                architecture = function['Architectures'][0]        
                break 

        self.assertEqual(architecture, LAMBDA["ARCHITECTURE"]) 


    def test_lambda_envvar_in_function(self):
        # Test environment variables in lambda.
        functions = self.lambda_client.list_functions()['Functions']
        lambda_name = self.outputs.get("lambda_name").value
        
        env = {}
        for function in functions:
            if function['FunctionName'] == lambda_name:
                env = function['Environment']['Variables']
                break 
        
        self.assertIn("ENV_TEST_VAL",env)

    def test_lambda_requests(self):
        # Test lambda response is valid and can access the environment variables.
        lambda_name = self.outputs.get("lambda_name").value

        response = self.lambda_client.invoke(
            FunctionName = lambda_name,
            Payload = json.dumps({}),
        )
        response_payload = json.loads(response['Payload'].read().decode("utf-8"))['body']
        self.assertIn(LAMBDA["ENV_TEST_VAL"],response_payload)

if __name__ == '__main__':
    unittest.main()

    