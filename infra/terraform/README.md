# Terraform [Work in Progress]
Here, we are using 'vanila' terrafirm with S3 bucket backend.
Github Actions are used to deploy infrastructure using terraform.

## Terraform Deployment using Github Actions
### Pre-requisite
* Manually create S3 Bucket on primary region (on dev, staging and prod), as explained [here](https://developer.hashicorp.com/terraform/language/settings/backends/s3).
* Manually create DynamoDB tableon primary region (for dev, staging, prod), to store state lock keys, as explained [here](https://developer.hashicorp.com/terraform/language/settings/backends/s3).
* Manually create OIDC IAM Role on primary region (for dev, staging and prod) to allow Github Actions to provision resources on AWS (see below for more details).
Follow guidelines here: [Open ID Connect identity provider (OIDC)](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)


Terraform deployment is done by github workflow `terraform-deployment.yml`.
To test the `terraform-deployment.yml`, a pull request to main needs to be created, and then the workflow appears on the Github Actions tab and can be triggered manually.

In any case, it's recommended to add lock key management using DynamoDB.

>>Note: A common practice when the RnD team and the project grows significantly, is manage all environments from a centralized account.


## Environments
In this sample repo we use 3 environment, one environment on each account per the three stages: dev, staging and prod.
In addition, we use local dev environment for local development and testing.
In the code we use the combination of `Platform` (local,AWS) and `Stage` (dev, staging, prod) enums to indicate these environments.

- **Local Dev** - Code developed and tested by developers working on changes, leveraging dev container and local stack to run and test services. Code is not yet merged to man. Testing locally and in CI.
- **AWS Dev** - Sandbox for developers with the latest code. Once PR has been merged to main, the code is deployed to Dev.
- **AWS Staging** - Pre-production environment, configured similarly. Integration and E2E tests are run periodically against this environment. Promoting to production will require an approval.
- **AWS Prod** - Production environment. At this point we

## Multi-region deployment
In this example we are using multi-regions (primary and secondary) for prod and staging and a single region for dev.

- Every environment has has a primary region `AWS_PRIMARY_REGION`
- In `AWS_PRIMARY_REGION` we manage centrally the shared resources for the environment:  ECR, AppConfig, SecretsManager, Terraform S3 BAckend, DynamoDB lock table for terraform state
- `AWS_REGION` is the region where the resource is actually deployed

>> Note: In general it's better to have staging and prod environment as similar as possible and preferably on the same regions. In this example we used other regions as the different environments are simulated on the same account.

| Env | Primary Region | Secondary Region | Notes |
| --- | --- | --- | --- |
| dev |  us-east-1 | N\A | Should be close to dev teams |
| staging | eu-west-1 | eu-west-2 | Preferably similar to prod* |
| prod | us-west-1 | us-west-2 | Main region, should be optimized for the location of the majority of customers |
