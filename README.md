# CDK template application

This repository hosts a CDK project that provison a multi-stage AWS infrastructure composed of a VPC, a kubrnetes cluster and an elasticsearch cluster.

## Dev tools:

Need tools:

- aws cli
- aws account
- cdk cli
- python3

## Stage bootstrapping

Before trying to deploy a stage, go through these steps:

- Create your stage config file under `config` dir. Then update its content according to your context (account id, cluster size, ...)

- Allow ES AWS service to access your vpc resources by running this command:

```bash
aws iam create-service-linked-role --aws-service-name es.amazonaws.com
```

- Bootstrap the cdk toolkit. This step is needed for the ComputeStack as we are using assets.

```bash
make bootstrapp-cdk-toolkit
```

- Create a python virualenv and install dependencies using this command:

```bash
make local-venv
source .venv/bin/activate
make install-dependencies
```

That's it! Now you are ready to provision your stage.

## Stage lifecycle

- `make diff STAGE=dev` display cdk diff for the dev stage and all cdk stacks
- `make deploy STAGE=dev STACKS=NetworkStack` synthesize cloudformation template then deploy the NetworkStack of the dev stage
- `make destroy` destroy the 3 stacks of the dev stage
