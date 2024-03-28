# Sample Python Monorepo [A work in progress]

This is a sample monorepo that can be used as a reference to get familiar with the concept of:
* Developing inside Devcontainer (dockerized development environment)
* Python monorepo and solution structure
* pre-commit hooks
* Building and running locally
* Unit testing lambda services
* Terraform

### TODO
It's partial and still a few TODOS to complete the sample:
1. Adding Docker file for windows environment (currently for Mac with Apple Silicone) and update Wiki acordingly
2. Extract configuration-provide.py into a dedicated package under packages/
3. Use Poetry to manage package versions and to manage scripts reunning recursively (similarly to pnpm for javascript).
   Once done, the pre-commit hook for unit tests can be updated to run pytest recursively.
4. Use Terraform to deploy infra on local stack and on AWS
5. Add a deployment.yml workflow to deploy to AWS
6. Define Branch policy to require PR approval and squash and rebase merge 
7. Add e2e.yml workflow with a simple e2e test which runs nightly (every night)


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
3. Setup your git credentials by completing: [set](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) [](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)[credentials](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token), and [cache credentials](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git)
4. Install [Docker for Mac](https://docs.docker.com/desktop/mac/release-notes/) or [Docker for Windows](https://docs.docker.com/desktop/install/windows-install/) and make sure the docker daemon is started

### Initial Setup
1. Clone the [DevContainer](https://github.com/vox-studio/dev-container) repo.
2. Open the repo in visual studio code
3. Press `CMD SHIFT P` and then type `reopen in container`
4. Once the container is ready you should have a working dev-environment.
5. If you are running into `Remote-Containers CLI: RPC pipe not configured` error, please [follow this fix](https://rexbytes.com/2022/08/23/visual-studio-docker-container-target-stop-importing-local-git-config/)

## Running Locally
### Local Dev environment
We're using VS Code DevContainer to run our dockerized development environment.
To run the development environment locally, click `Shift+Command+p -> Reopen in Container`

### Running cloud resources locally
We're leveraging AWS Localstack to emulate a cloud environment locally.
To do so, we are using docker-compose to setup the DevContainer and the Localstack container.

### Running lambda locally
* On MacOS
   Make sure your workspace folder is shared from the docker host. 
  * Lambda handler with API: ```cd services/<service-folder>  sam build && sudo sam local start-api --container-host host.docker.internal```
  * Lambda handler without API: ```cd services/<service-folder>  sam build && sudo sam local invoke --container-host host.docker.internal```

* On Windows
  * Lambda handler with API: ```cd services/<service-folder>  sam build && sudo sam local start-api```
  * Lambda handler without  API: ```cd services/<service-folder>  sam build && sudo sam  local invoke```

You can also run the flask application directly without invoking the lambda: `flask --app <file-with-flask-app> run --debug`

## Package and project versioning
TBD
## Release a new Solution version
TBD