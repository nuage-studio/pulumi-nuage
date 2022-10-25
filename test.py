# import boto3
# lambda_client = boto3.client('lambda')
# functions = lambda_client.list_functions()['Functions']

# function_names = [function['FunctionName'] for function in functions]

# for function in functions:
#     if function['FunctionName'] == 'CapitaineStudyBanner':
#         arn = function['FunctionArn']
#         role = function['Role']
#         handler = function['Handler']
#         timeout = function['Timeout']
#         memory = function['MemorySize']
#         env = function['Environment']
#         architecture = function['Architectures'][0]
        
#         print(arn) #arn:aws:lambda:eu-west-1:683449672851:function:CapitaineStudyBanner
#         print(role) #arn:aws:iam::683449672851:role/service-role/CapitaineStudyBanner-role-hvk6nc2c
#         print(handler) #lambda_function.lambda_handler
#         print(timeout) #10
#         print(memory) #128
#         print(env) #{'Variables': {'FLASK_APP': 'app.py', 'STRIP_STAGE_PATH': '1', 'FLASK_ENV': 'production'}}
#         print(architecture) #x86_64