# coding=utf-8
# *** WARNING: this file was generated by Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ContainerFunctionArgs', 'ContainerFunction']

@pulumi.input_type
class ContainerFunctionArgs:
    def __init__(__self__, *,
                 ecr_repository_name: pulumi.Input[str],
                 architecture: Optional[pulumi.Input[str]] = None,
                 context: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dockerfile: Optional[pulumi.Input[str]] = None,
                 environment: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 keep_warm: Optional[pulumi.Input[bool]] = None,
                 memory_size: Optional[pulumi.Input[float]] = None,
                 policy_document: Optional[pulumi.Input[str]] = None,
                 repository: Optional[pulumi.Input[str]] = None,
                 timeout: Optional[pulumi.Input[float]] = None,
                 url: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a ContainerFunction resource.
        :param pulumi.Input[str] ecr_repository_name: ECR repository name for new definition.
        :param pulumi.Input[str] architecture: Architecture, either `X86_64` or `ARM64`. Defaults to `x86_64`
        :param pulumi.Input[str] context: Dockerfile context path.
        :param pulumi.Input[str] description: Description of the function.
        :param pulumi.Input[str] dockerfile: Dockerfile path. Defaults to `./Dockerfile`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] environment: Environment Variables
        :param pulumi.Input[bool] keep_warm: Keep warm by refreshing the lambda function every 5 minutes. Defaults to `false`
        :param pulumi.Input[float] memory_size: Amount of memory in MB your Lambda Function can use at runtime. Defaults to `512`.
        :param pulumi.Input[str] policy_document: Policy Document for lambda.
        :param pulumi.Input[str] repository: Existing ECR repository name
        :param pulumi.Input[float] timeout: Amount of time your Lambda Function has to run in seconds. Defaults to `3`
        :param pulumi.Input[bool] url: Use Lambda URL. Defaults to `false`
        """
        pulumi.set(__self__, "ecr_repository_name", ecr_repository_name)
        if architecture is not None:
            pulumi.set(__self__, "architecture", architecture)
        if context is not None:
            pulumi.set(__self__, "context", context)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if dockerfile is not None:
            pulumi.set(__self__, "dockerfile", dockerfile)
        if environment is not None:
            pulumi.set(__self__, "environment", environment)
        if keep_warm is not None:
            pulumi.set(__self__, "keep_warm", keep_warm)
        if memory_size is not None:
            pulumi.set(__self__, "memory_size", memory_size)
        if policy_document is not None:
            pulumi.set(__self__, "policy_document", policy_document)
        if repository is not None:
            pulumi.set(__self__, "repository", repository)
        if timeout is not None:
            pulumi.set(__self__, "timeout", timeout)
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter(name="ecrRepositoryName")
    def ecr_repository_name(self) -> pulumi.Input[str]:
        """
        ECR repository name for new definition.
        """
        return pulumi.get(self, "ecr_repository_name")

    @ecr_repository_name.setter
    def ecr_repository_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "ecr_repository_name", value)

    @property
    @pulumi.getter
    def architecture(self) -> Optional[pulumi.Input[str]]:
        """
        Architecture, either `X86_64` or `ARM64`. Defaults to `x86_64`
        """
        return pulumi.get(self, "architecture")

    @architecture.setter
    def architecture(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "architecture", value)

    @property
    @pulumi.getter
    def context(self) -> Optional[pulumi.Input[str]]:
        """
        Dockerfile context path.
        """
        return pulumi.get(self, "context")

    @context.setter
    def context(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "context", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the function.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def dockerfile(self) -> Optional[pulumi.Input[str]]:
        """
        Dockerfile path. Defaults to `./Dockerfile`
        """
        return pulumi.get(self, "dockerfile")

    @dockerfile.setter
    def dockerfile(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dockerfile", value)

    @property
    @pulumi.getter
    def environment(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Environment Variables
        """
        return pulumi.get(self, "environment")

    @environment.setter
    def environment(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "environment", value)

    @property
    @pulumi.getter(name="keepWarm")
    def keep_warm(self) -> Optional[pulumi.Input[bool]]:
        """
        Keep warm by refreshing the lambda function every 5 minutes. Defaults to `false`
        """
        return pulumi.get(self, "keep_warm")

    @keep_warm.setter
    def keep_warm(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "keep_warm", value)

    @property
    @pulumi.getter(name="memorySize")
    def memory_size(self) -> Optional[pulumi.Input[float]]:
        """
        Amount of memory in MB your Lambda Function can use at runtime. Defaults to `512`.
        """
        return pulumi.get(self, "memory_size")

    @memory_size.setter
    def memory_size(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "memory_size", value)

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> Optional[pulumi.Input[str]]:
        """
        Policy Document for lambda.
        """
        return pulumi.get(self, "policy_document")

    @policy_document.setter
    def policy_document(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_document", value)

    @property
    @pulumi.getter
    def repository(self) -> Optional[pulumi.Input[str]]:
        """
        Existing ECR repository name
        """
        return pulumi.get(self, "repository")

    @repository.setter
    def repository(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "repository", value)

    @property
    @pulumi.getter
    def timeout(self) -> Optional[pulumi.Input[float]]:
        """
        Amount of time your Lambda Function has to run in seconds. Defaults to `3`
        """
        return pulumi.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "timeout", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[bool]]:
        """
        Use Lambda URL. Defaults to `false`
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "url", value)


class ContainerFunction(pulumi.ComponentResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 architecture: Optional[pulumi.Input[str]] = None,
                 context: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dockerfile: Optional[pulumi.Input[str]] = None,
                 ecr_repository_name: Optional[pulumi.Input[str]] = None,
                 environment: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 keep_warm: Optional[pulumi.Input[bool]] = None,
                 memory_size: Optional[pulumi.Input[float]] = None,
                 policy_document: Optional[pulumi.Input[str]] = None,
                 repository: Optional[pulumi.Input[str]] = None,
                 timeout: Optional[pulumi.Input[float]] = None,
                 url: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Create a ContainerFunction resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] architecture: Architecture, either `X86_64` or `ARM64`. Defaults to `x86_64`
        :param pulumi.Input[str] context: Dockerfile context path.
        :param pulumi.Input[str] description: Description of the function.
        :param pulumi.Input[str] dockerfile: Dockerfile path. Defaults to `./Dockerfile`
        :param pulumi.Input[str] ecr_repository_name: ECR repository name for new definition.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] environment: Environment Variables
        :param pulumi.Input[bool] keep_warm: Keep warm by refreshing the lambda function every 5 minutes. Defaults to `false`
        :param pulumi.Input[float] memory_size: Amount of memory in MB your Lambda Function can use at runtime. Defaults to `512`.
        :param pulumi.Input[str] policy_document: Policy Document for lambda.
        :param pulumi.Input[str] repository: Existing ECR repository name
        :param pulumi.Input[float] timeout: Amount of time your Lambda Function has to run in seconds. Defaults to `3`
        :param pulumi.Input[bool] url: Use Lambda URL. Defaults to `false`
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ContainerFunctionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a ContainerFunction resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param ContainerFunctionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ContainerFunctionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 architecture: Optional[pulumi.Input[str]] = None,
                 context: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dockerfile: Optional[pulumi.Input[str]] = None,
                 ecr_repository_name: Optional[pulumi.Input[str]] = None,
                 environment: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 keep_warm: Optional[pulumi.Input[bool]] = None,
                 memory_size: Optional[pulumi.Input[float]] = None,
                 policy_document: Optional[pulumi.Input[str]] = None,
                 repository: Optional[pulumi.Input[str]] = None,
                 timeout: Optional[pulumi.Input[float]] = None,
                 url: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is not None:
            raise ValueError('ComponentResource classes do not support opts.id')
        else:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ContainerFunctionArgs.__new__(ContainerFunctionArgs)

            __props__.__dict__["architecture"] = architecture
            __props__.__dict__["context"] = context
            __props__.__dict__["description"] = description
            __props__.__dict__["dockerfile"] = dockerfile
            if ecr_repository_name is None and not opts.urn:
                raise TypeError("Missing required property 'ecr_repository_name'")
            __props__.__dict__["ecr_repository_name"] = ecr_repository_name
            __props__.__dict__["environment"] = environment
            __props__.__dict__["keep_warm"] = keep_warm
            __props__.__dict__["memory_size"] = memory_size
            __props__.__dict__["policy_document"] = policy_document
            __props__.__dict__["repository"] = repository
            __props__.__dict__["timeout"] = timeout
            __props__.__dict__["url"] = url
            __props__.__dict__["arn"] = None
            __props__.__dict__["function_url"] = None
            __props__.__dict__["name"] = None
        super(ContainerFunction, __self__).__init__(
            'nuage:aws:ContainerFunction',
            resource_name,
            __props__,
            opts,
            remote=True)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def function_url(self) -> pulumi.Output[str]:
        return pulumi.get(self, "function_url")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

