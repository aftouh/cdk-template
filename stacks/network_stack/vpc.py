from typing import Dict, List

from aws_cdk import (
    core,
    aws_ec2 as ec2
)


class Vpc(core.Construct):
    config: Dict
    vpc: ec2.Vpc
    subnet_configuration: List[ec2.SubnetConfiguration] = []

    def __init__(self, scope: core.Construct, id: str, config: Dict) -> None:
        super().__init__(scope, id)
        self.config = config

        self.__build_subnets_config()
        self.__create_vpc()

    def __create_vpc(self):
        vpc_config = self.config['network']['vpc']
        self.vpc = ec2.Vpc(
            scope=self,
            id=self.config['name'],
            subnet_configuration=self.subnet_configuration,
            max_azs=vpc_config['maxAzs'],
            cidr=vpc_config['cidr'],
            nat_gateway_subnets=ec2.SubnetSelection(
                subnet_group_name=vpc_config['natGatewaySubnetName']
            ),
            enable_dns_hostnames=True,
            enable_dns_support=True,
        )

    def __build_subnets_config(self):
        for subnet in self.config['network']['subnets']:
            self.subnet_configuration.append(ec2.SubnetConfiguration(
                name=subnet['name'],
                subnet_type=ec2.SubnetType[subnet['subnetType']],
                cidr_mask=subnet['cidrMask']
            ))
