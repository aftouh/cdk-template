import json

from aws_cdk import core
from stacks.network_stack import network_stack
from utils import config_util


def get_template():
    app = core.App()
    network_stack.NetworkStack(app, "cdk-template", config_util.load_config("dev"))
    return json.dumps(app.synth().get_stack("cdk-template").template)


def test_vpc_created():
    assert("AWS::EC2::VPC" in get_template())
