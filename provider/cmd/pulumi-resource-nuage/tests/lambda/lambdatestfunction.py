import json
import sys

def lambda_handler(event, context):
    print("Hello AWS!")
    print("event = {}".format(event))
    return {
        'statusCode': 200,
    }
