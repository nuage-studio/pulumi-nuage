import pathlib
import pytest
from ..constants import GLOBAL
from pulumi import automation as auto

# session: the fixture is destroyed at the end of the test session.
@pytest.fixture(scope="session")
def stack_outputs():
    # Create stack on first call
    STACK_NAME = GLOBAL["STACK_NAME"]
    REGION_NAME = GLOBAL["REGION_NAME"]
    AWS_PROFILE = GLOBAL["AWS_PROFILE"]
    WORK_DIR = str(pathlib.Path(__file__).parent.parent.resolve())

    stack = auto.create_or_select_stack(stack_name=STACK_NAME, work_dir=WORK_DIR)
    stack.set_config("aws:region", auto.ConfigValue(value=REGION_NAME))
    stack.set_config("aws:profile", auto.ConfigValue(value=AWS_PROFILE))
    stack.up(on_output=print)

    outputs = stack.outputs()
    yield outputs

    # Teardown - Destroy stack
    # stack.destroy(on_output=print)
    # stack.workspace.remove_stack(STACK_NAME)
