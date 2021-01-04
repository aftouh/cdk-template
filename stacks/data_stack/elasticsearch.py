from typing import Dict

from aws_cdk import (
    core,
    aws_elasticsearch as es,
    aws_ec2 as ec2,
    aws_iam as iam,
)


class Elasticsearch(core.Construct):

    def __init__(self, scope: core.Construct, id: str,
                 config: Dict,
                 vpc: ec2.Vpc,
                 es_sg: ec2.SecurityGroup) -> None:
        super().__init__(scope, id)

        es_config = config['data']['elasticsearch']

        # Build ES domain construct parameter
        capacity_config = es.CapacityConfig(
            master_node_instance_type=es_config['capacity']['masterNodes']['instanceType'],
            master_nodes=es_config['capacity']['masterNodes']['count'],
            data_node_instance_type=es_config['capacity']['dataNodes']['instanceType'],
            data_nodes=es_config['capacity']['dataNodes']['count'],
        )

        vpc_options = es.VpcOptions(
            security_groups=[es_sg],
            subnets=vpc.select_subnets(subnet_group_name=es_config['subnetGroupName']).subnets,
        )

        ebs_options = es.EbsOptions(volume_size=es_config['ebs']['volumeSize'])

        zone_awareness = es.ZoneAwarenessConfig(
            availability_zone_count=es_config['zoneAwareness']['count'],
            enabled=es_config['zoneAwareness']['enabled'],
        )

        logging_options = es.LoggingOptions(
            app_log_enabled=es_config['logging']['appLogEnabled'],
            audit_log_enabled=es_config['logging']['auditLogEnabled'],
            slow_index_log_enabled=es_config['logging']['slowIndexLogEnabled'],
            slow_search_log_enabled=es_config['logging']['slowIearchLogEnabled']
        )

        access_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            principals=[iam.AnyPrincipal()],
            actions=['es:*'],
            resources=["arn:aws:es:" + config['awsRegion'] + ":" +
                       config['awsAccount'] + ":domain/" + es_config['domainName'] + "/*"]

        )

        # Create ES domain
        es.Domain(self, 'Domain',
                  domain_name=es_config['domainName'],
                  version=es.ElasticsearchVersion.of(es_config['version']),
                  capacity=capacity_config,
                  ebs=ebs_options,
                  zone_awareness=zone_awareness,
                  vpc_options=vpc_options,
                  logging=logging_options,
                  access_policies=[access_policy],
                  )
