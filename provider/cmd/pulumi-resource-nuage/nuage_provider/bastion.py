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
from typing import List, Optional
from dataclasses import dataclass

import pulumi
import pulumi_tls as tls

import pulumi_aws as aws
from pulumi import Inputs, ResourceOptions


@dataclass
class BastionArgs:
    resource_name: pulumi.Input[str]
    vpc_id: pulumi.Input[str]
    vpc_subnets: pulumi.Input[List[str]]
    ssh_port: pulumi.Input[int]

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "BastionArgs":
        return BastionArgs(
            resource_name=inputs["resourceName"],
            vpc_id=inputs["vpcId"],
            vpc_subnets=inputs["vpcSubnets"],
        )


class bucket_nuage(pulumi.ComponentResource):
    bucket: s3.Bucket

    def __init__(
        self,
        name: str,
        args: BastionArgs,
        props: Optional[dict] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        super().__init__("nuage:aws:Bastion", name, props, opts)

        private_key = tls.PrivateKey("my-private-key",
            algorithm="RSA",
            rsa_bits=4096
        )
        key_pair = aws.ec2.KeyPair("deployer", public_key=private_key.public_key_openssh) # key_name_prefix = f"{project}-{stack}""

        security_group = aws.ec2.SecurityGroup(
            f"{name}/security-group",
            vpc_id=args.vpc_id,
            tags={"Name": name},
            ingress=aws.ec2.SecurityGroupIngressArgs(
                from_port=args.ssh_port,
                to_port=args.ssh_port0,
                protocol="tcp",
                cidr_blocks=["0.0.0.0/0"],
            ),
            egress=aws.ec2.SecurityGroupIngressArgs(
                from_port=0,
                to_port=0,
                protocol="-1",
                cidr_blocks=["0.0.0.0/0"],
            ),
        )

        bastion_ami = aws.ec2.get_ami(most_recent=True,
            filters=[
                aws.ec2.GetAmiFilterArgs(
                    name="name",
                    values=["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"],
                ),
                aws.ec2.GetAmiFilterArgs(
                    name="virtualization-type",
                    values=["hvm"],
                ),
            ],
            owners=["099720109477"]
        )
        web = aws.ec2.Instance(f"{name}-instance",
            instance_type="t4g.nano",
            ami=bastion_ami.id,
            key_name=key_pair.key_name,
            tags={"Name":""},
            user_data="""#!/bin/bash
            echo "PubkeyAcceptedKeyTypes +ssh-rsa" > /etc/ssh/sshd_config.d/heex_rsa.conf
            systemctl restart ssh.service
            """,
            user_data_replace_on_change=True,
            vpc_security_group_ids=[security_group.id]
            subnet_id=args.vpc_subnets[0],
            associate_public_ip_address=True,            
        )