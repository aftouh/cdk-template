#!/usr/bin/env python3

from aws_cdk import core

from cdk_template.cdk_template_stack import CdkTemplateStack


app = core.App()
CdkTemplateStack(app, "cdk-template", env={'region': 'us-west-2'})

app.synth()
