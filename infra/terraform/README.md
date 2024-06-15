# Terraform [Work in Progress]

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


## Terraform Deployment using Github Actions
We have two Github Workflows which runs upon a change in files under `infra/terraform`:
* `terraform-plan.yml` - Runs on pull requests and executes `terraform plan`
* `terraform-apply.yml` - Runc on push to merge and executes `terraform apply`

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