import json
import pytest

from aws_cdk import core
from cdk-template.cdk_template_stack import CdkTemplateStack


def get_template():
    app = core.App()
    CdkTemplateStack(app, "cdk-template")
    return json.dumps(app.synth().get_stack("cdk-template").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
