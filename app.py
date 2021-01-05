#!/usr/bin/env python3

import sys
from aws_cdk import core

from stacks.network_stack.network_stack import NetworkStack
from stacks.compute_stack.compute_stack import ComputeStack
from stacks.data_stack.data_stack import DataStack
from utils import config_util

app = core.App()

# Get target stage from cdk context
stage = app.node.try_get_context('stage')
if stage is None or stage == "unknown":
    sys.exit('You need to set the target stage.'
             ' USAGE: cdk <command> -c stage=dev <stack>')

# Load stage config and set cdk environment
config = config_util.load_config(stage)
env = core.Environment(account=config['awsAccount'],
                       region=config["awsRegion"],
                       )

network_stack = NetworkStack(app,
                             "NetworkStack",
                             config=config,
                             env=env
                             )

ComputeStack(app,
             "ComputeStack",
             config=config,
             vpc=network_stack.vpc,
             es_sg_id=network_stack.es_sg_id,
             env=env
             )

DataStack(app,
          "DataStack",
          config=config,
          vpc=network_stack.vpc,
          es_sg_id=network_stack.es_sg_id,
          env=env
          )

app.synth()
