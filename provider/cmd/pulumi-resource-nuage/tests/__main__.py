"""An AWS Python Pulumi program"""

import pulumi
from constants import BUCKET_NAME

# Append provider root to path.
import sys
sys.path.append('../')
# Import pulumi provider methods.
from nuage_provider.bucket_nuage import bucket_nuage

# Create new bucket
bucket = bucket_nuage(name= BUCKET_NAME)
pulumi.export("bucketName", bucket.bucket.bucket)