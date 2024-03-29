# coding=utf-8
# *** WARNING: this file was generated by Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._inputs import *
import pulumi_aws

__all__ = ['ContainerFunctionArgs', 'ContainerFunction']

@pulumi.input_type
class ContainerFunctionArgs:
    def __init__(__self__, *,
                 image_uri: pulumi.Input[str],
                 architecture: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 environment: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 keep_warm: Optional[pulumi.Input[bool]] = None,
                 log_retention_in_days: Optional[pulumi.Input[int]] = None,
                 memory_size: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 policy_document: Optional[pulumi.Input[str]] = None,
                 schedule_config: Optional[pulumi.Input['FunctionScheduleArgs']] = None,
                 timeout: Optional[pulumi.Input[int]] = None,
                 url_config: Optional[pulumi.Input['FunctionUrlArgs']] = None):
        """
        The set of arguments for constructing a ContainerFunction resource.
        :param pulumi.Input[str] image_uri: Image uri of the docker image.
        :param pulumi.Input[str] architecture: Architecture, either `X86_64` or `ARM64`. Defaults to `X86_64`
        :param pulumi.Input[str] description: Description of the function.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] environment: Environment Variables
        :param pulumi.Input[bool] keep_warm: Keep warm by refreshing the lambda function every 5 minutes. Defaults to `false`
        :param pulumi.Input[int] log_retention_in_days: Number of days for log retention to pass in cloudwatch log group. Defaults to `90`
        :param pulumi.Input[int] memory_size: Amount of memory in MB your Lambda Function can use at runtime. Defaults to `512`.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] name_prefix: Name prefix as an alternative to name and adds random suffix at the end.
        :param pulumi.Input[str] policy_document: Policy Document for lambda.
        :param pulumi.Input['FunctionScheduleArgs'] schedule_config: Configure the function's cloudwatch event rule schedule.
        :param pulumi.Input[int] timeout: Amount of time your Lambda Function has to run in seconds. Defaults to `3`
        :param pulumi.Input['FunctionUrlArgs'] url_config: Configure lambda function url.
        """
        pulumi.set(__self__, "image_uri", image_uri)
        if architecture is not None:
            pulumi.set(__self__, "architecture", architecture)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if environment is not None:
            pulumi.set(__self__, "environment", environment)
        if keep_warm is not None:
            pulumi.set(__self__, "keep_warm", keep_warm)
        if log_retention_in_days is not None:
            pulumi.set(__self__, "log_retention_in_days", log_retention_in_days)
        if memory_size is not None:
            pulumi.set(__self__, "memory_size", memory_size)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if name_prefix is not None:
            pulumi.set(__self__, "name_prefix", name_prefix)
        if policy_document is not None:
            pulumi.set(__self__, "policy_document", policy_document)
        if schedule_config is not None:
            pulumi.set(__self__, "schedule_config", schedule_config)
        if timeout is not None:
            pulumi.set(__self__, "timeout", timeout)
        if url_config is not None:
            pulumi.set(__self__, "url_config", url_config)

    @property
    @pulumi.getter(name="imageUri")
    def image_uri(self) -> pulumi.Input[str]:
        """
        Image uri of the docker image.
        """
        return pulumi.get(self, "image_uri")

    @image_uri.setter
    def image_uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "image_uri", value)

    @property
    @pulumi.getter
    def architecture(self) -> Optional[pulumi.Input[str]]:
        """
        Architecture, either `X86_64` or `ARM64`. Defaults to `X86_64`
        """
        return pulumi.get(self, "architecture")

    @architecture.setter
    def architecture(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "architecture", value)

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
    @pulumi.getter(name="logRetentionInDays")
    def log_retention_in_days(self) -> Optional[pulumi.Input[int]]:
        """
        Number of days for log retention to pass in cloudwatch log group. Defaults to `90`
        """
        return pulumi.get(self, "log_retention_in_days")

    @log_retention_in_days.setter
    def log_retention_in_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "log_retention_in_days", value)

    @property
    @pulumi.getter(name="memorySize")
    def memory_size(self) -> Optional[pulumi.Input[int]]:
        """
        Amount of memory in MB your Lambda Function can use at runtime. Defaults to `512`.
        """
        return pulumi.get(self, "memory_size")

    @memory_size.setter
    def memory_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "memory_size", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="namePrefix")
    def name_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Name prefix as an alternative to name and adds random suffix at the end.
        """
        return pulumi.get(self, "name_prefix")

    @name_prefix.setter
    def name_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name_prefix", value)

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
    @pulumi.getter(name="scheduleConfig")
    def schedule_config(self) -> Optional[pulumi.Input['FunctionScheduleArgs']]:
        """
        Configure the function's cloudwatch event rule schedule.
        """
        return pulumi.get(self, "schedule_config")

    @schedule_config.setter
    def schedule_config(self, value: Optional[pulumi.Input['FunctionScheduleArgs']]):
        pulumi.set(self, "schedule_config", value)

    @property
    @pulumi.getter
    def timeout(self) -> Optional[pulumi.Input[int]]:
        """
        Amount of time your Lambda Function has to run in seconds. Defaults to `3`
        """
        return pulumi.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout", value)

    @property
    @pulumi.getter(name="urlConfig")
    def url_config(self) -> Optional[pulumi.Input['FunctionUrlArgs']]:
        """
        Configure lambda function url.
        """
        return pulumi.get(self, "url_config")

    @url_config.setter
    def url_config(self, value: Optional[pulumi.Input['FunctionUrlArgs']]):
        pulumi.set(self, "url_config", value)


class ContainerFunction(pulumi.ComponentResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 architecture: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 environment: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 image_uri: Optional[pulumi.Input[str]] = None,
                 keep_warm: Optional[pulumi.Input[bool]] = None,
                 log_retention_in_days: Optional[pulumi.Input[int]] = None,
                 memory_size: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 policy_document: Optional[pulumi.Input[str]] = None,
                 schedule_config: Optional[pulumi.Input[pulumi.InputType['FunctionScheduleArgs']]] = None,
                 timeout: Optional[pulumi.Input[int]] = None,
                 url_config: Optional[pulumi.Input[pulumi.InputType['FunctionUrlArgs']]] = None,
                 __props__=None):
        """
        Provides an AWS Lambda Function with additional necesary resources. It bundles several resources such as `Lambda Functions`, `Function URLs`, `CloudWatch keep-warm rules`, `Log Group with a Retention Policy`, `Role to run Lambda and Write Logs`. It also has a feature for schedule (cron) definitions and automated X-Ray tracing.

        ## Example Usage
        ### Basic Example

        ```python
        import pulumi_nuage as nuage
        
        repository = nuage.aws.Repository(
            "foo",
            name="repository",
            expire_in_days=30,
        )
        
        image = nuage.aws.Image(
            "foo",
            build_args=nuage.aws.DockerBuildArgs(
                dockerfile="../api/Dockerfile",
                context="../"
            ),
            repository_url=repository.url,
        )
        
        container_function = nuage.aws.ContainerFunction("foo",
            name="lambda-function",
            description="Nuage AWS ContainerFunction resource.",
            image_uri=image.uri,
            architecture="X86_64",
            memory_size=512,
            timeout=30,
            environment={"bar":"baz"},
            keep_warm=True,
            url=True,
            log_retention_in_days=90,
            schedule_config=nuage.aws.FunctionScheduleArgs(
                schedule_expression="rate(5 minutes)"
            ),
        )
        ```
        ### Custom Policy Document Example

        ```python
        import pulumi_nuage as nuage
        
        policy_doc = aws.iam.get_policy_document(
            version="2012-10-17",
            statements=[
                aws.iam.GetPolicyDocumentStatementArgs(
                    effect="Allow",
                    actions=["s3:*"],
                    resources=[
                        bucket.arn
                    ],
                ),
            ],
        ).json
        
        container_function = nuage.aws.ContainerFunction("foo",
            name="lambda-function",
            description="Nuage AWS ContainerFunction resource.",
            image_uri=image.uri,
            architecture="X86_64",
            memory_size=512,
            timeout=30,
            environment={"bar":"baz"},
            keep_warm=True,
            url=True,
            log_retention_in_days=90,
            schedule_config=nuage.aws.FunctionScheduleArgs(
                schedule_expression="rate(5 minutes)"
            ),
            policy_document=policy_doc
        )
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] architecture: Architecture, either `X86_64` or `ARM64`. Defaults to `X86_64`
        :param pulumi.Input[str] description: Description of the function.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] environment: Environment Variables
        :param pulumi.Input[str] image_uri: Image uri of the docker image.
        :param pulumi.Input[bool] keep_warm: Keep warm by refreshing the lambda function every 5 minutes. Defaults to `false`
        :param pulumi.Input[int] log_retention_in_days: Number of days for log retention to pass in cloudwatch log group. Defaults to `90`
        :param pulumi.Input[int] memory_size: Amount of memory in MB your Lambda Function can use at runtime. Defaults to `512`.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] name_prefix: Name prefix as an alternative to name and adds random suffix at the end.
        :param pulumi.Input[str] policy_document: Policy Document for lambda.
        :param pulumi.Input[pulumi.InputType['FunctionScheduleArgs']] schedule_config: Configure the function's cloudwatch event rule schedule.
        :param pulumi.Input[int] timeout: Amount of time your Lambda Function has to run in seconds. Defaults to `3`
        :param pulumi.Input[pulumi.InputType['FunctionUrlArgs']] url_config: Configure lambda function url.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ContainerFunctionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an AWS Lambda Function with additional necesary resources. It bundles several resources such as `Lambda Functions`, `Function URLs`, `CloudWatch keep-warm rules`, `Log Group with a Retention Policy`, `Role to run Lambda and Write Logs`. It also has a feature for schedule (cron) definitions and automated X-Ray tracing.

        ## Example Usage
        ### Basic Example

        ```python
        import pulumi_nuage as nuage
        
        repository = nuage.aws.Repository(
            "foo",
            name="repository",
            expire_in_days=30,
        )
        
        image = nuage.aws.Image(
            "foo",
            build_args=nuage.aws.DockerBuildArgs(
                dockerfile="../api/Dockerfile",
                context="../"
            ),
            repository_url=repository.url,
        )
        
        container_function = nuage.aws.ContainerFunction("foo",
            name="lambda-function",
            description="Nuage AWS ContainerFunction resource.",
            image_uri=image.uri,
            architecture="X86_64",
            memory_size=512,
            timeout=30,
            environment={"bar":"baz"},
            keep_warm=True,
            url=True,
            log_retention_in_days=90,
            schedule_config=nuage.aws.FunctionScheduleArgs(
                schedule_expression="rate(5 minutes)"
            ),
        )
        ```
        ### Custom Policy Document Example

        ```python
        import pulumi_nuage as nuage
        
        policy_doc = aws.iam.get_policy_document(
            version="2012-10-17",
            statements=[
                aws.iam.GetPolicyDocumentStatementArgs(
                    effect="Allow",
                    actions=["s3:*"],
                    resources=[
                        bucket.arn
                    ],
                ),
            ],
        ).json
        
        container_function = nuage.aws.ContainerFunction("foo",
            name="lambda-function",
            description="Nuage AWS ContainerFunction resource.",
            image_uri=image.uri,
            architecture="X86_64",
            memory_size=512,
            timeout=30,
            environment={"bar":"baz"},
            keep_warm=True,
            url=True,
            log_retention_in_days=90,
            schedule_config=nuage.aws.FunctionScheduleArgs(
                schedule_expression="rate(5 minutes)"
            ),
            policy_document=policy_doc
        )
        ```

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
                 description: Optional[pulumi.Input[str]] = None,
                 environment: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 image_uri: Optional[pulumi.Input[str]] = None,
                 keep_warm: Optional[pulumi.Input[bool]] = None,
                 log_retention_in_days: Optional[pulumi.Input[int]] = None,
                 memory_size: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 policy_document: Optional[pulumi.Input[str]] = None,
                 schedule_config: Optional[pulumi.Input[pulumi.InputType['FunctionScheduleArgs']]] = None,
                 timeout: Optional[pulumi.Input[int]] = None,
                 url_config: Optional[pulumi.Input[pulumi.InputType['FunctionUrlArgs']]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.plugin_download_url is None:
            opts.plugin_download_url = _utilities.get_plugin_download_url()
        if opts.id is not None:
            raise ValueError('ComponentResource classes do not support opts.id')
        else:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ContainerFunctionArgs.__new__(ContainerFunctionArgs)

            __props__.__dict__["architecture"] = architecture
            __props__.__dict__["description"] = description
            __props__.__dict__["environment"] = environment
            if image_uri is None and not opts.urn:
                raise TypeError("Missing required property 'image_uri'")
            __props__.__dict__["image_uri"] = image_uri
            __props__.__dict__["keep_warm"] = keep_warm
            __props__.__dict__["log_retention_in_days"] = log_retention_in_days
            __props__.__dict__["memory_size"] = memory_size
            __props__.__dict__["name"] = name
            __props__.__dict__["name_prefix"] = name_prefix
            __props__.__dict__["policy_document"] = policy_document
            __props__.__dict__["schedule_config"] = schedule_config
            __props__.__dict__["timeout"] = timeout
            __props__.__dict__["url_config"] = url_config
            __props__.__dict__["arn"] = None
            __props__.__dict__["url"] = None
        super(ContainerFunction, __self__).__init__(
            'nuage:aws:ContainerFunction',
            resource_name,
            __props__,
            opts,
            remote=True)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN (Amazon Resource Name) of the Lambda Function.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the Lambda Function.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[Optional[str]]:
        """
        Lambda Function URL (Only valid if `urlEnabled` is used).
        """
        return pulumi.get(self, "url")

