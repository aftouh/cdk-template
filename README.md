# CDK template application

This repository hosts a CDK project that provison a multi-stage AWS infrastructure composed of a VPC, a kubrnetes cluster and an elasticsearch cluster.

Learn more about this project setup by reading this [article](https://medium.com/better-programming/how-to-organize-your-aws-cdk-project-f1c463aa966e).

## Dev tools:

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

- `make diff STAGE=pro` display cdk diff of all stacks of the pro stage
- `make deploy STAGE=dev STACKS=NetworkStack` synthesize cloudformation template then deploy the NetworkStack to the dev stage
- `make destroy` destroy the 3 stacks of the dev stage
