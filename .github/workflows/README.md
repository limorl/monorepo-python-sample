# Github Workflows

We are using Github Workflow to manage our CI and Deployment pipelines.

Pre-requisite:

* `GH_TOKEN` - A Github access token to publish packages associated with the workflow repository such as package registry and container registry. We are using the container registry to cache the dev container, to enable reusing in CI and Deployment workflows. More info is available on [working with the container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).
* **OIDC Access to AWS** - To allow Github Workflow steps to access AWS account, an OIDC provider and an IAM role needs to be created.
Please follow this blog post: https://aws.amazon.com/blogs/security/use-iam-roles-to-connect-github-actions-to-actions-in-aws/.