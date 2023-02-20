from typing import Optional
from dataclasses import dataclass

import pulumi
import pulumi_random as random


@dataclass
class PrefixedComponentResourceArgs:
    """
    Either `name` or `name_prefix` should be given.
    If `name_prefix` is used, 5 char length suffix will be added to end of it.
    """

    name: Optional[pulumi.Input[str]]
    name_prefix: Optional[pulumi.Input[str]]


class PrefixedComponentResource(pulumi.ComponentResource):
    def __init__(
        self,
        resource_type: str,
        resource_name: str,
        args: PrefixedComponentResourceArgs,
        props: Optional[pulumi.Inputs] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        """
        We use `name_` to not collide with the Pulumi's internal variables.
        self.name_ will contain the full name of the resource. (It will be suffixed in case `args.name_prefix` used)
        """
        if args.name_prefix and args.name:
            raise Exception("name and name_prefix cannot be set at the same time.")

        if args.name_prefix:
            suffix = random.RandomString(
                f"{args.name_prefix}-suffix", length=5, special=False
            ).result
            self.name_: str = suffix.apply(
                lambda suffix: f"{args.name_prefix}-{suffix}"
            )
        else:
            self.name_ = pulumi.Output.from_input(
                args.name if args.name else resource_name
            )
        super().__init__(resource_type, resource_name, props, opts)
