from typing import Optional
from dataclasses import dataclass

import pulumi
import pulumi_random as random


@dataclass
class PrefixedComponentResourceArgs:
    name: Optional[pulumi.Input[str]]
    name_prefix: Optional[pulumi.Input[str]]


class PrefixedComponentResource(pulumi.ComponentResource):
    def __init__(
        self,
        tag: str,
        resource_name: str,
        args: PrefixedComponentResourceArgs,
        props: Optional[pulumi.Inputs] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        if args.name_prefix and args.name:
            raise Exception("name and name_prefix cannot be set at the same time.")

        if args.name_prefix:
            suffix = random.RandomString(
                f"{args.name_prefix}-suffix", length=5, special=False
            ).result
            self._name: str = suffix.apply(
                lambda suffix: f"{args.name_prefix}-{suffix}"
            )
        else:
            self._name = pulumi.Output.from_input(
                args.name if args.name else resource_name
            )

        super().__init__(tag, resource_name, props, opts)
