from typing import Any, Dict, Optional
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
            self.suffix = random.RandomString(
                f"{args.name_prefix}-suffix", length=5, special=False
            ).result
            self.name_prefix = pulumi.Output.from_input(args.name_prefix)
            self.name_: str = self.suffix.apply(
                lambda suffix: f"{args.name_prefix}-{suffix}"
            )
        else:
            # Set empty suffix if explicit `name` is given.
            self.suffix = None
            self.name_ = pulumi.Output.from_input(
                args.name if args.name else resource_name
            )
            self.name_prefix = self.name_
        super().__init__(resource_type, resource_name, props, opts)

    def get_suffixed_name(self, resource_name):
        """
        Add name prefix and random suffix to the resource name for child resources.
        """
        if self.suffix:
            return pulumi.Output.all(
                name_prefix=self.name_prefix, suffix=self.suffix
            ).apply(
                lambda args: f"{args['name_prefix']}-{resource_name}-{args['suffix']}"
            )
        else:
            return self.name_.apply(lambda name: f"{name}-{resource_name}")
