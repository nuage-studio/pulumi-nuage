"""An AWS Python Pulumi program"""

import sys
sys.path.append('../')

import pulumi
from nuage_provider.bucket_nuage import bucket_nuage

bucket = bucket_nuage(name="nuage")
pulumi.export("bucketName", bucket.bucket.bucket)