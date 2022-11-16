import pulumi
from constants import BUCKET_NAME

# Import pulumi provider methods.
from nuage_provider.bucket_nuage import bucket_nuage

# S3 Bucket
bucket = bucket_nuage(name=BUCKET_NAME)
pulumi.export("bucketName", bucket.bucket.bucket)
