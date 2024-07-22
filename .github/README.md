# Github

## Github Workflows

We are using Github Workflow to manage our CI and Deployment pipelines.

Pre-requisite:

1. Setup Terraform per each AWS environment (dev. staging and prod) using [terraform-setup.sh](../infra/scripts/terraform-setup.sh)
2. Create 3 environments for the repo: dev, staging and prod. In each encronment devinf environment variables:
```
AWS_ACCOUNT_ID = your environment acount id (12 digits)
AWS_PRIMARY_REGION = your environment primary region (e.g. us-east1)
AWS_GITHUB_ACTIONS_ROLE = The ARN of the GithubActions Role created in step 1 (should look like `arn:aws:iam::__AWS_ACCOUNT_ID__:role/GithubActionsRole`)
```
3. **GH_Actions_PAT** - A Github Personal Access Token to allow Github Workflow Access the repo. Go to Account --> Settings --> Developer Settings --> Personal Access Tokens and create a token (classic) with `repo` and `read:org` scope. Then go to the Repository settings and repo secret named `GH_REPO_PAT` with the copied token value.
