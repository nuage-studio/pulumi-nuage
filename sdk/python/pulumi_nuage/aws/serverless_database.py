# coding=utf-8
# *** WARNING: this file was generated by Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ServerlessDatabaseArgs', 'ServerlessDatabase']

@pulumi.input_type
class ServerlessDatabaseArgs:
    def __init__(__self__, *,
                 database_type: pulumi.Input[str],
                 vpc_id: pulumi.Input[str],
                 vpc_subnets: pulumi.Input[Sequence[pulumi.Input[str]]],
                 bastion_enabled: Optional[pulumi.Input[bool]] = None,
                 bastion_subnets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_api: Optional[pulumi.Input[bool]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 ip_whitelist: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 master_user_name: Optional[pulumi.Input[str]] = None,
                 skip_final_snapshot: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a ServerlessDatabase resource.
        :param pulumi.Input[str] database_type: Database type. `mysql` or `postgresql`
        :param pulumi.Input[str] vpc_id: Vpc id.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] vpc_subnets: List of subnet ip addresses.
        :param pulumi.Input[bool] bastion_enabled: Enable data api. Defaults to `false`
        :param pulumi.Input[Sequence[pulumi.Input[str]]] bastion_subnets: List of public subnet ip addresses for the bastion host.
        :param pulumi.Input[bool] data_api: Enable data api. Defaults to `false`
        :param pulumi.Input[str] database_name: Name of the database.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_whitelist: List of whitelisted IP addresses. If not specified, it will be public 0.0.0.0/0
        :param pulumi.Input[str] master_user_name: Master user name of the db.
        :param pulumi.Input[bool] skip_final_snapshot: Determines whether a final DB snapshot is created before the DB instance is deleted. Defaults to `false`
        """
        pulumi.set(__self__, "database_type", database_type)
        pulumi.set(__self__, "vpc_id", vpc_id)
        pulumi.set(__self__, "vpc_subnets", vpc_subnets)
        if bastion_enabled is not None:
            pulumi.set(__self__, "bastion_enabled", bastion_enabled)
        if bastion_subnets is not None:
            pulumi.set(__self__, "bastion_subnets", bastion_subnets)
        if data_api is not None:
            pulumi.set(__self__, "data_api", data_api)
        if database_name is not None:
            pulumi.set(__self__, "database_name", database_name)
        if ip_whitelist is not None:
            pulumi.set(__self__, "ip_whitelist", ip_whitelist)
        if master_user_name is not None:
            pulumi.set(__self__, "master_user_name", master_user_name)
        if skip_final_snapshot is not None:
            pulumi.set(__self__, "skip_final_snapshot", skip_final_snapshot)

    @property
    @pulumi.getter(name="databaseType")
    def database_type(self) -> pulumi.Input[str]:
        """
        Database type. `mysql` or `postgresql`
        """
        return pulumi.get(self, "database_type")

    @database_type.setter
    def database_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "database_type", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Input[str]:
        """
        Vpc id.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_id", value)

    @property
    @pulumi.getter(name="vpcSubnets")
    def vpc_subnets(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        List of subnet ip addresses.
        """
        return pulumi.get(self, "vpc_subnets")

    @vpc_subnets.setter
    def vpc_subnets(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "vpc_subnets", value)

    @property
    @pulumi.getter(name="bastionEnabled")
    def bastion_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable data api. Defaults to `false`
        """
        return pulumi.get(self, "bastion_enabled")

    @bastion_enabled.setter
    def bastion_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "bastion_enabled", value)

    @property
    @pulumi.getter(name="bastionSubnets")
    def bastion_subnets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of public subnet ip addresses for the bastion host.
        """
        return pulumi.get(self, "bastion_subnets")

    @bastion_subnets.setter
    def bastion_subnets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "bastion_subnets", value)

    @property
    @pulumi.getter(name="dataApi")
    def data_api(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable data api. Defaults to `false`
        """
        return pulumi.get(self, "data_api")

    @data_api.setter
    def data_api(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "data_api", value)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the database.
        """
        return pulumi.get(self, "database_name")

    @database_name.setter
    def database_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_name", value)

    @property
    @pulumi.getter(name="ipWhitelist")
    def ip_whitelist(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of whitelisted IP addresses. If not specified, it will be public 0.0.0.0/0
        """
        return pulumi.get(self, "ip_whitelist")

    @ip_whitelist.setter
    def ip_whitelist(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_whitelist", value)

    @property
    @pulumi.getter(name="masterUserName")
    def master_user_name(self) -> Optional[pulumi.Input[str]]:
        """
        Master user name of the db.
        """
        return pulumi.get(self, "master_user_name")

    @master_user_name.setter
    def master_user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "master_user_name", value)

    @property
    @pulumi.getter(name="skipFinalSnapshot")
    def skip_final_snapshot(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines whether a final DB snapshot is created before the DB instance is deleted. Defaults to `false`
        """
        return pulumi.get(self, "skip_final_snapshot")

    @skip_final_snapshot.setter
    def skip_final_snapshot(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "skip_final_snapshot", value)


class ServerlessDatabase(pulumi.ComponentResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bastion_enabled: Optional[pulumi.Input[bool]] = None,
                 bastion_subnets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_api: Optional[pulumi.Input[bool]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 database_type: Optional[pulumi.Input[str]] = None,
                 ip_whitelist: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 master_user_name: Optional[pulumi.Input[str]] = None,
                 skip_final_snapshot: Optional[pulumi.Input[bool]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 vpc_subnets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        The ServerlessDatabase component is a convenient and efficient solution for creating serverless databases using Amazon RDS Aurora. It automatically creates components such as subnet group, security group, security group rules, and RDS cluster, and securely manages the DB credentials. With support for both MySQL and PostgreSQL, it provides a fully configured serverless database resource for your serverless database needs.

        ## Example Usage
        ### Basic Example

        ```python
        import pulumi_nuage as nuage
        
        db = nuage.aws.ServerlessDatabase(
            "foo",
            vpc_id=my_vpc.id,
            vpc_subnets=my_vpc.private_subnet_ids,
            database_type="mysql",
            database_name="bar",
            master_username="root",
            ip_whitelist=["0.0.0.0/0"],
            skip_final_snapshot=True
        )
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] bastion_enabled: Enable data api. Defaults to `false`
        :param pulumi.Input[Sequence[pulumi.Input[str]]] bastion_subnets: List of public subnet ip addresses for the bastion host.
        :param pulumi.Input[bool] data_api: Enable data api. Defaults to `false`
        :param pulumi.Input[str] database_name: Name of the database.
        :param pulumi.Input[str] database_type: Database type. `mysql` or `postgresql`
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_whitelist: List of whitelisted IP addresses. If not specified, it will be public 0.0.0.0/0
        :param pulumi.Input[str] master_user_name: Master user name of the db.
        :param pulumi.Input[bool] skip_final_snapshot: Determines whether a final DB snapshot is created before the DB instance is deleted. Defaults to `false`
        :param pulumi.Input[str] vpc_id: Vpc id.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] vpc_subnets: List of subnet ip addresses.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServerlessDatabaseArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The ServerlessDatabase component is a convenient and efficient solution for creating serverless databases using Amazon RDS Aurora. It automatically creates components such as subnet group, security group, security group rules, and RDS cluster, and securely manages the DB credentials. With support for both MySQL and PostgreSQL, it provides a fully configured serverless database resource for your serverless database needs.

        ## Example Usage
        ### Basic Example

        ```python
        import pulumi_nuage as nuage
        
        db = nuage.aws.ServerlessDatabase(
            "foo",
            vpc_id=my_vpc.id,
            vpc_subnets=my_vpc.private_subnet_ids,
            database_type="mysql",
            database_name="bar",
            master_username="root",
            ip_whitelist=["0.0.0.0/0"],
            skip_final_snapshot=True
        )
        ```

        :param str resource_name: The name of the resource.
        :param ServerlessDatabaseArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServerlessDatabaseArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bastion_enabled: Optional[pulumi.Input[bool]] = None,
                 bastion_subnets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_api: Optional[pulumi.Input[bool]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 database_type: Optional[pulumi.Input[str]] = None,
                 ip_whitelist: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 master_user_name: Optional[pulumi.Input[str]] = None,
                 skip_final_snapshot: Optional[pulumi.Input[bool]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 vpc_subnets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
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
            __props__ = ServerlessDatabaseArgs.__new__(ServerlessDatabaseArgs)

            __props__.__dict__["bastion_enabled"] = bastion_enabled
            __props__.__dict__["bastion_subnets"] = bastion_subnets
            __props__.__dict__["data_api"] = data_api
            __props__.__dict__["database_name"] = database_name
            if database_type is None and not opts.urn:
                raise TypeError("Missing required property 'database_type'")
            __props__.__dict__["database_type"] = database_type
            __props__.__dict__["ip_whitelist"] = ip_whitelist
            __props__.__dict__["master_user_name"] = master_user_name
            __props__.__dict__["skip_final_snapshot"] = skip_final_snapshot
            if vpc_id is None and not opts.urn:
                raise TypeError("Missing required property 'vpc_id'")
            __props__.__dict__["vpc_id"] = vpc_id
            if vpc_subnets is None and not opts.urn:
                raise TypeError("Missing required property 'vpc_subnets'")
            __props__.__dict__["vpc_subnets"] = vpc_subnets
            __props__.__dict__["bastion_ip"] = None
            __props__.__dict__["bastion_private_key"] = None
            __props__.__dict__["cluster_arn"] = None
            __props__.__dict__["host"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["password"] = None
            __props__.__dict__["policy_document"] = None
            __props__.__dict__["port"] = None
            __props__.__dict__["uri"] = None
            __props__.__dict__["user"] = None
        super(ServerlessDatabase, __self__).__init__(
            'nuage:aws:ServerlessDatabase',
            resource_name,
            __props__,
            opts,
            remote=True)

    @property
    @pulumi.getter
    def bastion_ip(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "bastion_ip")

    @property
    @pulumi.getter
    def bastion_private_key(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "bastion_private_key")

    @property
    @pulumi.getter
    def cluster_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "cluster_arn")

    @property
    @pulumi.getter
    def host(self) -> pulumi.Output[str]:
        return pulumi.get(self, "host")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def policy_document(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "policy_document")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[float]:
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def uri(self) -> pulumi.Output[str]:
        return pulumi.get(self, "uri")

    @property
    @pulumi.getter
    def user(self) -> pulumi.Output[str]:
        return pulumi.get(self, "user")

