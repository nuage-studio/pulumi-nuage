"""An AWS Python Pulumi program"""

# Append provider root to path.
import sys

sys.path.append("../pulumi-resource-nuage")

# Import required resources for tests
from resources import s3, lambda_container, database
