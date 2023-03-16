# coding=utf-8
# *** WARNING: this file was generated by Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from . import _utilities
import typing
# Export this package's modules as members:
from .provider import *

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_nuage.aws as __aws
    aws = __aws
else:
    aws = _utilities.lazy_import('pulumi_nuage.aws')

_utilities.register(
    resource_modules="""
[
 {
  "pkg": "nuage",
  "mod": "aws",
  "fqn": "pulumi_nuage.aws",
  "classes": {
   "nuage:aws:Bastion": "Bastion",
   "nuage:aws:ContainerFunction": "ContainerFunction",
   "nuage:aws:Image": "Image",
   "nuage:aws:Repository": "Repository",
   "nuage:aws:ServerlessDatabase": "ServerlessDatabase"
  }
 }
]
""",
    resource_packages="""
[
 {
  "pkg": "nuage",
  "token": "pulumi:providers:nuage",
  "fqn": "pulumi_nuage",
  "class": "Provider"
 }
]
"""
)
