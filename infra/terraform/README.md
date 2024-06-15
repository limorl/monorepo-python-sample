# Terraform [Work in Progress]
Here, we are using 'vanila' terrafirm with S3 bucket backend.

## Pre-requisite
* Manually create S3 Bucket on AWS Dev, Staging and PRod Environment as explained [here](https://developer.hashicorp.com/terraform/language/settings/backends/s3).
* Manually create OIDC IAM Role on each environment to allow Github Actions to provision resources on AWS (see below for more details).

## Terraform Deployment using Github Actions
Terraform deployment is done by github workflow `terraform-deployment.yml`.
To enable that, an IAM Role was created with [Open ID Connect identity provider (OIDC)](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)

To test the `terraform-deployment.yml`, a pull request to main needs to be created, and then the workflow appears on the Github Actions tab and can be triggered manually.

In any case, it's recommended to add lock key management using DynamoDB.

For AWS Dev:
```shell
terraform init -backend-config=backend.dev.tfvars
```

For AWS Staging:
```shell
terraform init -backend-config=backend.staging.tfvars
```

For AWS Prod:
```shell
terraform init -backend-config=backend.prod.tfvars
```

>>Note: A common practice when the RnD team and the project grows significantly, is manage all environments from a centralized account. Therefore we are storing the backend state in a file with `stage` suffix.

## Environments (env per stage)

We use the following environments :

- **Local Dev** - Code developed and tested by developers working on changes, leveraging dev container and local stack to run and test services. Code is not yet merged to man. Testing locally and in CI.
- **AWS Dev** - Sandbox for developers with the latest code. Once PR has been merged to main, the code is deployed to Dev.
- **AWS Staging** - Pre-production environment, configured similarly. Integration and E2E tests are run periodically against this environment. Promoting to production will require an approval.
- **AWS Prod** - Production environment. At this point we

**>> Note:** In the code we use the combination of `Platform` and `Stage` enums to indicate the above environments. 

## Single-region with Multi-region Naming

We are using a **Single-region** approach with two availability zones at this stage.

However, we are using a **resource naming convention that assumes a multi-region** approach in which:

- Every environment has has a primary region `AWS_PRIMARY_REGION`
- In `AWS_PRIMARY_REGION` we manage centrally the shared resources for the environment:  ECR, AppConfig, SecretsManager
- `AWS_REGION` is the region where the resource is deployed

**>> Note:** In a Single-region `Approach AWS_REGION` == `AWS_PRIMARY_REGION`

| Env | Primary Region | Notes |
| --- | --- | --- |
| dev |  us-east-1 | Should be close to dev teams |
| staging | us-east-2  | Preferably similar to prod |
| prod | us-east-2 | Main region, should be optimized for the location of the majority of customers |

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.54.1 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_services"></a> [services](#module\_services) | ./modules/service | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_appconfig_deployment_strategy.dev_deployment_strategy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/appconfig_deployment_strategy) | resource |
| [aws_appconfig_deployment_strategy.prod_deployment_strategy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/appconfig_deployment_strategy) | resource |
| [aws_appconfig_deployment_strategy.staging_deployment_strategy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/appconfig_deployment_strategy) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_aws_primary_region"></a> [aws\_primary\_region](#input\_aws\_primary\_region) | Primary Region - for ECR, AppConfig, SecretsManager | `string` | `null` | no |
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | Region to deploy to | `string` | `null` | no |
| <a name="input_stage"></a> [stage](#input\_stage) | General | `string` | `null` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->