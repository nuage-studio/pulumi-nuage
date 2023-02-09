GLOBAL = {
    "STACK_NAME": "nuage/staging",
    "REGION_NAME": "eu-west-1",
    "AWS_PROFILE": "nuage-dev",
}
BUCKET_NAME = "itest-nuage"

ECR_NAME = "ecr-itest-nuage"

LAMBDA = {
    "NAME": "itest-lambda-nuage",
    "TIMEOUT": 30,
    "MEMORY": 512,
    "ARCHITECTURE": "X86_64",
    "ENV_TEST_VAL": "env_ok",
}

DB = {
    "POSTGRESQL_NAME": "itestpostgresqldb",
    "MYSQL_NAME": "itestmysqldb",
    "USER": "itestdatabaseuser",
}
