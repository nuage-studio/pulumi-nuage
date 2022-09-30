# Copyright 2016-2021, Pulumi Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from typing import Optional

import pulumi
from pulumi import Inputs, ResourceOptions
from pulumi_aws import s3


class bucket_nuage(pulumi.ComponentResource):
    bucket: s3.Bucket

    def __init__(self, name: str, props: Optional[dict] = None, opts: Optional[ResourceOptions] = None) -> None:

        super().__init__("nuage:index:bucket", name, props, opts)

        # Create a bucket
        bucket = s3.Bucket(
            f"{name}-bucket",
            acl="private",
            opts=ResourceOptions(parent=self),
        )

        # Set the access policy for the bucket so all objects are readable.
        s3.BucketPolicy(
            f"{name}-bucket-policy",
            bucket=bucket.bucket,
            policy=bucket.bucket.apply(_allow_getobject_policy),
            opts=ResourceOptions(parent=bucket),
        )

        self.bucket = bucket

        self.register_outputs(
            {
                "bucket": bucket,
            }
        )


def _allow_getobject_policy(bucket_name: str) -> str:
    return json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [
                        f"arn:aws:s3:::{bucket_name}/*",  # policy refers to bucket name explicitly
                    ],
                },
            ],
        }
    )
