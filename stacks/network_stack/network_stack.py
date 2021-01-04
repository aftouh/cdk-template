from typing import Dict

from aws_cdk import (
    core,
    aws_ec2 as ec2,
)
from utils.stack_util import add_tags_to_stack
from .vpc import Vpc
from .security_group import SecurityGourp


class NetworkStack(core.Stack):
    vpc: ec2.IVpc
    es_sg_id: str

    def __init__(self, scope: core.Construct, id: str, config: Dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Apply common tags to stack resources.
        add_tags_to_stack(self, config)

        vpcConstruct = Vpc(self, 'Vpc', config)
        self.vpc = vpcConstruct.vpc

        sg = SecurityGourp(self, "SecurityGroups", self.vpc)
        self.es_sg_id = sg.es_sg.security_group_id
