# Github Workflows

We are using Github Workflow to manage our CI and Deployment pipelines.

Pre-requisite:

* **GH_Actions_PAT** - A Github Personal Access Token to allow Github Workflow Access the repo. Go to Account --> Settings --> Developer Settings --> Personal Access Tokens and create a token (classic) with repo `and `read:org scope. Then go to the Repository settings and repo secret named `GH_REPO_PAT` with the copied token value.

<!-- *`GH_TOKEN` - A Github access token to publish packages associated with the workflow repository such as package registry and container registry. We are using the container registry to cache the dev container, to enable reusing in CI and Deployment workflows. More info is available on [working with the container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).-->

* **Terraform Setup** - Run `terraform-setup.sh` as described in [infra/terraform/README.md](../../infra/terraform/README.md).
