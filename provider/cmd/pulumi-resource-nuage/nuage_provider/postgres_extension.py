from typing import Any, Dict, List, Optional

import boto3
from pulumi import Input, ResourceOptions, dynamic


class PgExtensionProvider(dynamic.ResourceProvider):
    def execute_sql(self, props: Dict[str, Any], sql: str, parameters: List[Dict[str, Any]]):
        session = boto3.Session(profile_name=props["aws_profile"], region_name=props["aws_region"])
        client = session.client("rds-data")  # type: ignore
        result = client.execute_statement(
            resourceArn=props["cluster_arn"],
            secretArn=props["secret_arn"],
            sql=sql,
            parameters=parameters,  # type: ignore
        )
        return result

    def create(self, props: Dict[str, Any]) -> dynamic.CreateResult:
        self.execute_sql(
            props=props,
            sql=f"CREATE EXTENSION {props['name']};",
            parameters=[],
        )
        return dynamic.CreateResult(id_=props["name"], outs=props)

    def diff(self, id_: str, olds: Dict[str, Any], news: Dict[str, Any]) -> dynamic.DiffResult:
        if olds.get("name") != news.get("name"):
            return dynamic.DiffResult(changes=True, replaces=["name"])
        return dynamic.DiffResult(changes=False)

    def delete(self, id_: str, props: Dict[str, Any]):
        self.execute_sql(
            props=props,
            sql=f"DROP EXTENSION {props['name']};",
            parameters=[],
        )


class PgExtension(dynamic.Resource):
    def __init__(
        self,
        resource_name: str,
        name: Input[str],
        cluster_arn: Input[str],
        secret_arn: Input[str],
        aws_region: Input[str],
        aws_profile: Input[str],
        opts: Optional[ResourceOptions] = None,
    ):
        super().__init__(
            provider=PgExtensionProvider(),
            name=resource_name,
            props={
                "name": name,
                "cluster_arn": cluster_arn,
                "secret_arn": secret_arn,
                "aws_region": aws_region,
                "aws_profile": aws_profile,
            },
            opts=opts,
        )
