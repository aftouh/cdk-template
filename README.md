# cdk template application

This repository contains an AWS infrastructure composed of a VPC and its subresources, a kubrnetes cluster and an elasticsearch cluster.  
This infrastructure is developed in python based on the AWS CDK framework.

## Prerequisities:

To deploy this application, you will need these elements

- an AWS account
- aws cli installed and configured
- cdk cli
- python3

## Stage bootstrapping

Make sur that you have your stage config file under `config` dir. Then update it's content according to your context (AWS account id, cluster size...)

Allow ES AWS service to access your vpc resource by running this command:

```bash
aws iam create-service-linked-role --aws-service-name es.amazonaws.com
```

Bootstrap the cdk toolkit. This is needed for the ComputeStack as we are using some assets

```bash
make bootstrapp-cdk-toolkit
```

Create a python virualenv and install dependencies using this command:

```bash
make local-venv
source .venv/bin/activate
make install-dependencies
```

## Stage lifecycle

- `make diff STAGE=dev` show cdk diff for the dev stage and all cdks stacks
- `make deploy STAGE=dev STACKS=NetworkStack` synthesize cloudformation template then deploy the NetworkStack of the dev stage
- `make destroy` will destroy all the stacks of the dev stage
