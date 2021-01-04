from typing import Dict

from aws_cdk import (
    core,
    aws_ec2 as ec2,
)
from utils.stack_util import add_tags_to_stack
from .elasticsearch import Elasticsearch


class DataStack(core.Stack):
    vpc: ec2.IVpc

    def __init__(self, scope: core.Construct, id: str,
                 config: Dict,
                 vpc: ec2.Vpc,
                 es_sg_id: str,
                 ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Apply common tags to stack resources.
        add_tags_to_stack(self, config)

        # Get elasticsearch security group created in tne network stack
        es_sg = ec2.SecurityGroup.from_security_group_id(
            self,
            "ElasticsearchSG",
            security_group_id=es_sg_id
        )

        # Create Elasticsearch cluster
        Elasticsearch(self, 'Vpc', config, vpc, es_sg)
