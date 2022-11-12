import json
from constants import LAMBDA, DB


class TestsLambda:
    def test_lambda_output_name(self):
        # Test if lambda name setting is valid.
        lambda_name = self.outputs.get("lambda_name").value
        self.assertEqual(LAMBDA["NAME"], lambda_name)

    def test_lambda_exists(self):
        # Test if lambda function is created successfully.
        functions = self.lambda_client.list_functions()["Functions"]
        function_names = [function["FunctionName"] for function in functions]

        lambda_name = self.outputs.get("lambda_name").value
        self.assertIn(lambda_name, function_names)

    def test_lambda_role(self):
        # Test if lambda has true role linked.
        functions = self.lambda_client.list_functions()["Functions"]
        lambda_name = self.outputs.get("lambda_name").value
        role_arn = self.outputs.get("lambda_role_arn").value

        function_role = None
        for function in functions:
            if function["FunctionName"] == lambda_name:
                function_role = function["Role"]
                break

        self.assertEqual(function_role, role_arn)

    def test_lambda_timeout(self):
        # Test if lambda has correct timeout value.
        functions = self.lambda_client.list_functions()["Functions"]
        lambda_name = self.outputs.get("lambda_name").value

        timeout = None
        for function in functions:
            if function["FunctionName"] == lambda_name:
                timeout = function["Timeout"]
                break

        self.assertEqual(timeout, LAMBDA["TIMEOUT"])

    def test_lambda_memory(self):
        # Test if lambda has correct memory value.
        functions = self.lambda_client.list_functions()["Functions"]
        lambda_name = self.outputs.get("lambda_name").value

        memory = None
        for function in functions:
            if function["FunctionName"] == lambda_name:
                memory = function["MemorySize"]
                break

        self.assertEqual(memory, LAMBDA["MEMORY"])

    def test_lambda_architecture(self):
        # Test if lambda has correct architecture type.
        functions = self.lambda_client.list_functions()["Functions"]
        lambda_name = self.outputs.get("lambda_name").value

        architecture = None
        for function in functions:
            if function["FunctionName"] == lambda_name:
                architecture = function["Architectures"][0]
                break

        self.assertEqual(architecture.upper(), LAMBDA["ARCHITECTURE"])

    def test_lambda_envvar_in_function(self):
        # Test environment variables in lambda.
        functions = self.lambda_client.list_functions()["Functions"]
        lambda_name = self.outputs.get("lambda_name").value

        env = {}
        for function in functions:
            if function["FunctionName"] == lambda_name:
                env = function["Environment"]["Variables"]
                break

        self.assertIn("ENV_TEST_VAL", env)

    def test_lambda_requests(self):
        # Test lambda response is valid and can access the environment variables.
        lambda_name = self.outputs.get("lambda_name").value

        response = self.lambda_client.invoke(
            FunctionName=lambda_name,
            Payload=json.dumps({}),
        )
        response_payload = json.loads(response["Payload"].read().decode("utf-8"))[
            "body"
        ]
        self.assertIn(LAMBDA["ENV_TEST_VAL"], response_payload)
