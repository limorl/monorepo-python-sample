# Github

## Github Workflows

We are using Github Workflow to manage our CI and Deployment pipelines.

Pre-requisite:

1. **Setup Terraform** - Read [terraform-setup README](../infra/scripts/README.md) and run `terraform-setup.sh` as described, per each AWS account (dev. staging and prod).
2. On Github Repo Settings:
* Create 3 environments: dev, staging and prod. In each environment define the following environment variables:
```
AWS_ACCOUNT_ID = your environment account id (12 digits)
AWS_PRIMARY_REGION = your environment primary region (e.g. us-east1)
AWS_GITHUB_ACTIONS_ROLE = The ARN of the GithubActions Role created in step 1 (should look like `arn:aws:iam::__AWS_ACCOUNT_ID__:role/GithubActionsRole`)
```
3. **GH_ACTIONS_PAT** - A Github Personal Access Token to allow Github Workflow Access the repo. Go to Account --> Settings --> Developer Settings --> Personal Access Tokens and create a token (classic) with `repo` and `read:org` scope. Then go to the Repository settings and repo secret named `GH_ACTIONS_PAT` with the copied token value.
4. **Require Status Checks** - Update Repo Setings with Branch policies for `main`:
- Require status checks to pass before merging
- Require branches to be up to date before merging: `Terraform Plan (dev) / Plan`, `Terraform Plan (staging) / Plan` and `Validate Code`
