import os
import json
import sys


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"running ": True, os.environ["ENV_TEST_VAL"]:1}),
    }
