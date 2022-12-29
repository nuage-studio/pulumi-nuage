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


from typing import Any, Dict, List, Optional
from dataclasses import dataclass

import pulumi
import pulumi_tls as tls

import pulumi_aws as aws


@dataclass
class BastionArgs:
    vpc_id: pulumi.Input[str]
    vpc_subnets: pulumi.Input[List[str]]
    ssh_port: pulumi.Input[int]

    @staticmethod
    def from_inputs(inputs: pulumi.Inputs) -> "BastionArgs":
        return BastionArgs(
            vpc_id=inputs["vpcId"],
            vpc_subnets=inputs["vpcSubnets"],
            ssh_port=inputs.get("sshPort", 22),
        )


class Bastion(pulumi.ComponentResource):
    public_ip: pulumi.Output[str]
    private_key_pem: pulumi.Output[str]

    def __init__(
        self,
        name: str,
        args: BastionArgs,
        props: Optional[dict] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        super().__init__("nuage:aws:Bastion", name, props, opts)

        private_key = tls.PrivateKey(
            f"{name}-private-key",
            algorithm="RSA",
            rsa_bits=4096,
            opts=pulumi.ResourceOptions(parent=self),
        )
        key_pair = aws.ec2.KeyPair(
            f"{name}-keypair",
            public_key=private_key.public_key_openssh,
            opts=pulumi.ResourceOptions(parent=private_key),
        )

        security_group = aws.ec2.SecurityGroup(
            f"{name}/security-group",
            vpc_id=args.vpc_id,
            tags={"Name": f"Security group for ssh {name}"},
            ingress=[
                aws.ec2.SecurityGroupIngressArgs(
                    from_port=args.ssh_port,
                    to_port=args.ssh_port,
                    protocol="tcp",
                    cidr_blocks=["0.0.0.0/0"],
                )
            ],
            egress=[
                aws.ec2.SecurityGroupIngressArgs(
                    from_port=0,
                    to_port=0,
                    protocol="-1",
                    cidr_blocks=["0.0.0.0/0"],
                )
            ],
            opts=pulumi.ResourceOptions(parent=self),
        )

        bastion_ami = aws.ec2.get_ami(
            most_recent=True,
            filters=[
                aws.ec2.GetAmiFilterArgs(
                    name="name",
                    values=["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-arm64-server-*"],
                ),
                aws.ec2.GetAmiFilterArgs(
                    name="virtualization-type",
                    values=["hvm"],
                ),
            ],
            owners=["099720109477"],
        )
        bastion = aws.ec2.Instance(
            f"{name}-instance",
            instance_type="t4g.nano",
            ami=bastion_ami.id,
            key_name=key_pair.key_name,
            tags={"Name": f"{name} bastion instance"},
            # user_data="""#!/bin/bash
            # echo "PubkeyAcceptedKeyTypes +ssh-rsa" > /etc/ssh/sshd_config.d/heex_rsa.conf
            # systemctl restart ssh.service
            # """,
            user_data_replace_on_change=True,
            vpc_security_group_ids=[security_group.id],
            subnet_id=args.vpc_subnets[0],
            associate_public_ip_address=True,
            opts=pulumi.ResourceOptions(parent=self),
        )

        # Build outputs

        outputs = {
            "public_ip": bastion.public_ip,
            "private_key_pem": private_key.private_key_pem,
        }

        self.set_outputs(outputs)

    def set_outputs(self, outputs: Dict[str, Any]):
        """
        Adds the Pulumi outputs as attributes on the current object so they can be
        used as outputs by the caller, as well as registering them.
        """
        for output_name in outputs.keys():
            setattr(self, output_name, outputs[output_name])

        self.register_outputs(outputs)
