# Sample Python Monorepo [A work in progress]

This is a sample monorepo that can be used as a starting point for a python project, to ramp up on the following concepts:
* Developing inside Devcontainer (dockerized development environment)
* Working with Localstack
* Building and running serverlass apps locally using sam cli
* Poetry for dependency management and packaging
* pre-commit hooks
* Unit testing lambda services
* Terraform
* Github wrkflows
* Changeset for package versions

### Next Steps
The monorepo will be extendedt to support:
1. Implement AppConfigConfigurationProvider based on AWS AppConfig and SSM - Start Lambda with AppConfigConfigurationProvider when runs on AWS + Define IAM role to access AppConfig and SSM
2. Logging using [aws-powertools] (https://github.com/aws-powertools/powertools-lambda-python)
3. Use Lambda Extensions to better handle calls to AppConfig and SSM
4. Semantic release using [changeset](https://github.com/changesets/changesets) - blogpost [here](https://lirantal.com/blog/introducing-changesets-simplify-project-versioning-with-semantic-releases/
5. Terraform to deploy infra on localstack and on AWS
6. Add a deployment.yml workflow to deploy to AWS and to Localstack
7. Add e2e.yml workflow with a simple e2e test which runs nightly (every night)

## Issues
* Semantic released was not tested / verified

## Sample
The sample includes two lambda services:
1. hello_world - a simple lambda handler without API
2. greeting - a simple lambda service with API, using Flask service framework

## Setup Development Environment

### Intro to Dev containers

In order to ease the setup time of new development environment, we are using [dev containers](https://code.visualstudio.com/docs/remote/containers) while developing, thus by leveraging docker, we have a unified docker image that automatically installs anything that we need to be able to develop.

This requires *all of our developers* to use docker and Visual Studio Code, to get optimized development environment.

### Prerequisites

1. Install [Git](https://git-scm.com/download/)
2. Install [Visual Studio Code](https://code.visualstudio.com/) and install the [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. Install [Docker for Mac](https://docs.docker.com/desktop/mac/release-notes/) or [Docker for Windows](https://docs.docker.com/desktop/install/windows-install/) and make sure the docker daemon is started
<!-- 
4. Setup your git credentials by completing: [set](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) [](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)[credentials](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token), and [cache credentials](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git)
-->

### Initial Setup
1. Clone the [DevContainer](https://github.com/vox-studio/dev-container) repo.
2. Open the repo in visual studio code
3. Create and edit .devcontainer/.env based on the .env.sample file. Set TARGETARCH and VARIANT based on your computer architecture, as explained in the comments on .env.sample.
3. Press `CMD SHIFT P` and then type `reopen in container`
4. Once the container is ready you should have a working dev-environment.
5. If you are running into `Remote-Containers CLI: RPC pipe not configured` error, please [follow this fix](https://rexbytes.com/2022/08/23/visual-studio-docker-container-target-stop-importing-local-git-config/)

### Dependency Management, Packaging and Versioning 
[Poetry](https://python-poetry.org/) is used for dependency management in the monorepo instead of `pip`.
Potery settings and list of dependencies is managed in `pyproject.toml` file for each package, in addition to the root.
To install a package, add  `<package-name> = "<version>"` to the `pyproject.toml` file and install using `poetry install`.
Make sure you distinguish dev and prod dependencies.

In the long run, we aim to release packages into a private Github package registry and install them from the registry.
In the short term, we'll keep it simple and won't publish the packages, but rather install them locally.
For example:
```python
[tool.poetry.dependencies]
python = "^3.10"
my_local_package = { path = "../packages/my_local_package", develop = false }
```

#### Package versioning
We will use [python-semantic-release](https://python-semantic-release.readthedocs.io/en/latest/) to automatically manage package versioning per package.
The configuration of `python-semantic-release` this will be centralized in the root's `pyproject.toml` file.

There are several approaches to bumping versions:
1. **Manual Bumping** - Manually bumping version in the `pyproject.toml` file
2. **Selective Release Rules** - Use python-semantic-release configuration options for selective release rules.
3. **Custom Release Script** - For more control, a custom release script using the semantic_release library.

**We will start with option 2**
This approach will help starting with a basic `release_rules` configuration.
As the project grows, we will refine the rules to handle more complex scenarios, and consider using a custom script for intricate versioning logic if needed.

Following the [Semantic Versioning Convention](https://semver.org/) this is how version is incremented:
Given a version number MAJOR.MINOR.PATCH, increment the:
* MAJOR version when you make incompatible API changes
* MINOR version when you add functionality in a backward compatible manner
* PATCH version when you make backward compatible bug fixes

#### Commit Messages Format (to be enforced through Code Review):
To allow automatic versioning, we'll need to follow commit message format.

1. **Commit Message Format:** `<type>(<scope>): <short summary>`.
  * **type**: This denotes the kind of change the commit introduces. Common types include **feat** (new feature), **fix** (bug fix), **docs** (documentation changes), **style** (style changes that do not affect the meaning of the code), **refactor** (code change that neither fixes a bug nor adds a feature), **test** (adding missing tests or correcting existing ones), **chore** (updates to the build process, auxiliary tools, and libraries such as documentation generation).
  * **scope**  (optional): A scope may be provided to indicate a more specific part of the codebase the change affects.
  * **short summary**: A concise description of the changes.

  * Examples:
    feat(authentication): add jwt support
    fix(database): resolve connection leak

2. **Automated Version Management**
 python-semantic-release will analyze these commit messages from the main branch (or whichever branch is configured) to automatically determine the type of version bump required for the next release:
  Commits with **feat** will trigger a minor version bump.
  Commits with **fix** will trigger a patch version bump.
  Commits that include a **BREAKING CHANGE** footer will trigger a major version bump, regardless of the commit type.
  Custom rules in the [tool.semantic_release.release_rules] section can further refine how other types of commits (like docs, style, or chore) influence the version bump.

3. **Release Process**
Upon merging changes into the release branch (e.g., main), the CI pipeline should include a step that runs python-semantic-release. This tool will:
- Analyze commits since the last release.
- Determine the next version number based on the commit messages.
- Update the version in pyproject.toml and any other configured version_variable files.
- Generate or update the CHANGELOG.md.
- Tag the release in the VCS (Version Control System, e.g., Git).
- Optionally, upload the package to PyPI or another package repository if configured.


## Running Locally
### Local Dev environment
We're using VS Code DevContainer to run our dockerized development environment.
To run the development environment locally, click `Shift+Command+p -> Reopen in Container`

We're leveraging AWS Localstack to emulate a cloud environment locally.
To do so, we are using docker-compose to setup the DevContainer and Localstack containers on your host machine.

After the DevContainer is created, we run the script `./devcontainer/post_create.sh` in which we install all the dependencies and build the packages.
In addition, it creates two aliases, which allows running aws and sam commands against the local stack.
So instead of `aws` or `sam`, you can use `aws-localstack` and `sam-localstack`.

**NOTE:** In order for these aliases to be available, open a new bash terminal and try them.
If for some reason the aliases are not recognized, you can set them up naually as follows:
```shell
echo "alias aws-localstack='AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1 AWS_ENDPOINT_URL=$CLOUD_ENDPOINT_OVERRIDE aws'" >> ~/.bash_aliases
echo "alias sam-localstack='AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1 AWS_ENDPOINT_URL=$CLOUD_ENDPOINT_OVERRIDE sam'" >> ~/.bash_aliases
```

Once we add terraform files to create the infrastructure, we'll be able to deploy the infra on our localstack.

### Local Packages
To install, build and test a local package, do the following from the repo root:
```shell
cd packages/<your-package>
poetry install
poetry run pytest
```

If you have package sependency, such as packages.package-a dependes on package-b, poetry can install the local packages and they can be imported. See package-a and package-b examples.

>> NOTE: When running on S code, you may see that the dependency local package is not recognized by pylance. Please ignore it.

To install *all packages* run from the monorepo root:

```shell
python run_script.py install-all
```

In general, every script defined in `packages/scripts` pyproject.toml can be run similarly:
```shell
python run_script.py <script-name>
```
### Running Service Locally

There are several options to run services locally:
1. Run the flask app
2. Run local lambda using sam cli
3. Deploy the lambda to localstack 

#### 1. Running the flask application directly

```shell
cd services/<my-service>
flask --app app.py run --debug
```

#### 2.Running lambda locally using SAM CLI
* On MacOS
   Make sure your workspace folder is shared from the docker host.
  * Lambda handler with API:
  ```shell
  cd services/<service-folder> 
  sam build
  sudo sam local start-api --container-host host.docker.internal --env-vars local.dev.env.json
  ```
  * Lambda handler without API:
  ```shell
  cd services/<service-folder>  
  sam build
  sudo sam local invoke --container-host host.docker.internal --env-vars local.dev.env.json
  ```

* Other Linux machines
  * Lambda handler with API:
  ```shell
  cd services/<service-folder>
  sam build
  sudo sam local start-api --env-vars local.dev.env.json
  ```
  * Lambda handler without  API:
  ```shell
  cd services/<service-folder>
  sam build
  sudo sam local invoke --env-vars local.dev.env.json
  ```

#### 3. Deploying lambda to Localstack using SAM CLI
To deploy using SAM CLI to LocalStack, set the --endpoint-url parameter to point to LocalStack for all service commands. Here's how you can package and deploy your application (Greeting service for example).

First, create an S3 bucket in local stack for the lambdas packaged using sam cli:
```shell
aws-localstack s3api create-bucket --bucket sam-build-lambdas
```

Here's an example on how to build and deploy the greeting service:

```shell
cd services/greeting
sam build
```

Then, deploy using sam deploy:
```shell
sam-localstack deploy \
--stack-name greeting-service \
--capabilities CAPABILITY_IAM \
--region us-east-1 \
--s3-bucket sam-build-lambdas \
--parameter-overrides 'Stage=dev Platform=local'
```

**NOTE:** If you want to deploy the lambda functions with production configuration, then use `--parameter-overrides Stage=prod Platform=aws`

Once deployed to localstack, all lambdas are available on a single endpoint and can be invoked using function name.

You can list all functions by running:
```shell
aws-localstack lambda list-functions
```

Use the `FunctionName` in the returned list when invoking the lambda.
For example, for greeting service, invoke the lambda function:
```shell
aws-localstack lambda invoke \
--function-name greeting-service-GreetingLambda-3497da7d \
--payload '{"headers": {}, "path": "/hello", "httpMethod": "GET"}' \
--cli-binary-format raw-in-base64-out \
output.txt

aws-localstack lambda invoke \
--function-name greeting-service-GreetingLambda-3497da7d \
--payload '{"headers": {}, "path": "/hello/Danny", "httpMethod": "GET"}' \
--cli-binary-format raw-in-base64-out \
output.txt
```

<!--Get the id of your service and your service is available on this endpoint:
`http://localhost:4566/restapis/<restapi-id>/dev/_user_request_/hello`
-->

To view localstack logs run:
```shell
sudo docker logs localstack-main
```

## Deploying services to AWS using Sam CLI

Make sure you are logged in to AWS:
```shell
    aws configure sso
```

Skip SSO session name and set the profile name to `default`.
If you are using multiple profiles, add `--profile-name <profile>` to each command.

Then build and deploy:
```shell
sam build
sam deploy \
--stack-name greeting-service \
--capabilities CAPABILITY_IAM \
--region us-east-1 \
--s3-bucket sam-build-lambdas
```

Deploy will [automatically use the template under .aws-sam/build](https://stackoverflow.com/questions/59815363/aws-sam-cli-ignoring-my-python-dependencies-during-build-package-and-deplo).

You can issue an http request against the lambda:
```shell
curl https://8fwcdbjd95.execute-api.us-east-1.amazonaws.com/prod/hello
```

```shell
curl https://8fwcdbjd95.execute-api.us-east-1.amazonaws.com/prod/hello/Danny
```

**NOTE:** When deployed remotely, the greeting message returns with 5 exclamation points, according to the remote config, but when running locally or on local stack, it is returned with a single exclamation point. 
