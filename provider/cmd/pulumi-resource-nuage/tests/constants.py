GLOBAL = {
    "STACK_NAME": "nuage/staging",
    "REGION_NAME": "eu-west-1",   
}
BUCKET_NAME = "itest-nuage"

LAMBDA = {
    "NAME": "itest-lambda-nuage",
    "TIMEOUT":30,
    "MEMORY":512,
    "ARCHITECTURE":"x86_64",
    "ENV_TEST_VAL":"env_ok"
}