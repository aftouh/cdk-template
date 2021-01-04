from typing import Dict
from aws_cdk.core import (
    Tags,
    Stack
)


# Add tags to each element of the stack.
def add_tags_to_stack(stack: Stack, config: Dict) -> None:
    # Add common tags
    for tag_key in config['tags']:
        Tags.of(stack).add(key=tag_key, value=config['tags'][tag_key])

    # Add environment in the tags
    Tags.of(stack).add(key='stage', value=config['stage'])
