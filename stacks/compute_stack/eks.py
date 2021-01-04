from typing import Dict
from http.client import HTTPS_PORT, HTTP_PORT

from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_iam as iam,
)


class Eks(core.Construct):
    _config: Dict
    _cluster: eks.Cluster
    _node_group: eks.Nodegroup

    def __init__(self, scope: core.Construct, id: str,
                 config: Dict,
                 vpc: ec2.Vpc,
                 es_sg: ec2.ISecurityGroup,
                 ) -> None:
        super().__init__(scope, id)
        self._config = config

        # Create cluster control plane
        self.__create_eks_control_plane(vpc)

        # Create cluster worker nodes
        self.__create_eks_worker_nodes()
        self._node_group.node.add_dependency(self._cluster)

        # Update ES ingress security group by allowing traffic from EKS on port 443 and 80
        self.__update_es_sg(es_sg)

    def __create_eks_control_plane(self, vpc: ec2.Vpc) -> eks.Cluster:
        # This role is used to connect to the cluster with admin access
        # It is be associated to system:masters kubernetes RBAC group
        masters_role = iam.Role(
            self,
            'eksClusterAdmin',
            role_name='eks-cluster-admin-'+self._config['stage'],
            assumed_by=iam.AccountRootPrincipal()
        )

        # Control plane role
        # It provides permissions for the Kubernetes control plane
        # to make calls to AWS API operations on your behalf.
        role = self.__create_eks_control_plane_role()

        eks_config = self._config['compute']['eks']
        self._cluster = eks.Cluster(
            scope=self,
            id="ControlPlane",
            cluster_name=self._config['name'],
            role=role,
            masters_role=masters_role,
            version=eks.KubernetesVersion.of(eks_config['version']),
            vpc=vpc,
            vpc_subnets=list(
                map(lambda group_name: ec2.SubnetSelection(subnet_group_name=group_name),
                    eks_config['subnetGroupNames'])
            ),
            default_capacity=0,
        )

    def __create_eks_worker_nodes(self):
        ng_config = self._config['compute']['eks']['nodeGroup']
        self._node_group = eks.Nodegroup(
            scope=self,
            id=ng_config['name'],
            cluster=self._cluster,
            nodegroup_name=ng_config['name'],
            instance_types=[ec2.InstanceType(ng_config['instanceType'])],
            ami_type=eks.NodegroupAmiType.AL2_X86_64,
            min_size=ng_config['minCapacity'],
            max_size=ng_config['maxCapacity'],
            desired_size=ng_config['desiredCapacity'],
            subnets=ec2.SubnetSelection(subnet_group_name=ng_config['subnetGroupName']),
            node_role=self.__create_eks_nodegroup_role(),
        )

    def __create_eks_nodegroup_role(self) -> iam.Role:
        worker_role = iam.Role(
            self,
            'NodeGroupRole',
            role_name='eks-nodegroup-role-'+self._config['stage'],
            description='Allows EC2 instances to call AWS services on your behalf.',
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com')
        )
        worker_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEKSWorkerNodePolicy'))
        worker_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEC2ContainerRegistryReadOnly'))
        worker_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEKS_CNI_Policy'))

        return worker_role

    def __create_eks_control_plane_role(self) -> iam.Role:
        eks_role = iam.Role(
            self,
            'eksRole',
            role_name='eks-role-'+self._config['stage'],
            assumed_by=iam.ServicePrincipal('eks.amazonaws.com')
        )
        eks_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEKSServicePolicy'))
        eks_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEKSClusterPolicy'))

        return eks_role

    def __update_es_sg(self, es_sg: ec2.ISecurityGroup):
        cluster_sg = ec2.SecurityGroup.from_security_group_id(
            self,
            "ClusterSg",
            security_group_id=self._cluster.cluster_security_group_id
        )

        es_sg.add_ingress_rule(
            peer=cluster_sg,
            connection=ec2.Port.tcp(HTTPS_PORT),
            description='Accept traffic from the eks cluster in https'
        )
        es_sg.add_ingress_rule(
            peer=cluster_sg,
            connection=ec2.Port.tcp(HTTP_PORT),
            description='Accept traffic from the eks cluster in http'
        )
