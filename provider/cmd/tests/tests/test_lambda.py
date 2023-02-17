import json
import boto3
import pytest
from ..constants import GLOBAL, LAMBDA

"""
class TestLambda:
    # class: the fixture is destroyed during teardown of the last test in the class.
    @pytest.fixture(scope="class")
    def lambda_client(self):
        return boto3.Session(profile_name=GLOBAL["AWS_PROFILE"]).client(
            "lambda", region_name=GLOBAL["REGION_NAME"]
        )

    def test_lambda_output_name(self, stack_outputs):
        # Test if lambda name setting is valid.
        lambda_name = stack_outputs.get("lambda_name").value
        assert LAMBDA["NAME"] == lambda_name

    def test_lambda_exists(self, stack_outputs, lambda_client):
        # Test if lambda function is created successfully.
        functions = lambda_client.list_functions()["Functions"]
        function_names = [function["FunctionName"] for function in functions]

        lambda_name = stack_outputs.get("lambda_name").value
        assert lambda_name in function_names

    def test_lambda_role(self, stack_outputs, lambda_client):
        # Test if lambda has true role linked.
        functions = lambda_client.list_functions()["Functions"]
        lambda_name = stack_outputs.get("lambda_name").value
        role_arn = stack_outputs.get("lambda_role_arn").value

        function_role = None
        for function in functions:
            if function["FunctionName"] == lambda_name:
                function_role = function["Role"]
                break

        assert function_role == role_arn

    def test_lambda_timeout(self, stack_outputs, lambda_client):
        # Test if lambda has correct timeout value.
        functions = lambda_client.list_functions()["Functions"]
        lambda_name = stack_outputs.get("lambda_name").value

        timeout = None
        for function in functions:
            if function["FunctionName"] == lambda_name:
                timeout = function["Timeout"]
                break

        assert timeout == LAMBDA["TIMEOUT"]

    def test_lambda_memory(self, stack_outputs, lambda_client):
        # Test if lambda has correct memory value.
        functions = lambda_client.list_functions()["Functions"]
        lambda_name = stack_outputs.get("lambda_name").value

        memory = None
        for function in functions:
            if function["FunctionName"] == lambda_name:
                memory = function["MemorySize"]
                break

        assert memory == LAMBDA["MEMORY"]

    def test_lambda_architecture(self, stack_outputs, lambda_client):
        # Test if lambda has correct architecture type.
        functions = lambda_client.list_functions()["Functions"]
        lambda_name = stack_outputs.get("lambda_name").value

        architecture = None
        for function in functions:
            if function["FunctionName"] == lambda_name:
                architecture = function["Architectures"][0]
                break

        assert architecture.upper() == LAMBDA["ARCHITECTURE"]

    def test_lambda_envvar_in_function(self, stack_outputs, lambda_client):
        # Test environment variables in lambda.
        functions = lambda_client.list_functions()["Functions"]
        lambda_name = stack_outputs.get("lambda_name").value

        env = {}
        for function in functions:
            if function["FunctionName"] == lambda_name:
                env = function["Environment"]["Variables"]
                break

        assert "ENV_TEST_VAL" in env

    def test_lambda_requests(self, stack_outputs, lambda_client):
        # Test lambda response is valid and can access the environment variables.
        lambda_name = stack_outputs.get("lambda_name").value

        response = lambda_client.invoke(
            FunctionName=lambda_name,
            Payload=json.dumps({}),
        )
        response_payload = json.loads(response["Payload"].read().decode("utf-8"))[
            "body"
        ]
        assert LAMBDA["ENV_TEST_VAL"] in response_payload
"""
