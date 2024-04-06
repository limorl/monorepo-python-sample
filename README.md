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
3. [Done] [Still need to fix folder structure for poetry packaging]Use Poetry to manage package versions and to manage scripts reunning recursively (similarly to pnpm for javascript).
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
3. Install [Docker for Mac](https://docs.docker.com/desktop/mac/release-notes/) or [Docker for Windows](https://docs.docker.com/desktop/install/windows-install/) and make sure the docker daemon is started
<!-- 
4. Setup your git credentials by completing: [set](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) [](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)[credentials](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token), and [cache credentials](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git)
-->

### Initial Setup
1. Clone the [DevContainer](https://github.com/vox-studio/dev-container) repo.
2. Open the repo in visual studio code
3. Create and edit .devcontainer/.env based on the .env.sample file. Set TARGETARCH and VARIANT based on your computer architecture, as explaind in the comments on .env.sample.
3. Press `CMD SHIFT P` and then type `reopen in container`
4. Once the container is ready you should have a working dev-environment.
5. If you are running into `Remote-Containers CLI: RPC pipe not configured` error, please [follow this fix](https://rexbytes.com/2022/08/23/visual-studio-docker-container-target-stop-importing-local-git-config/)

### Dependency Management, Packaging and Versioning 
[Poetry](https://python-poetry.org/) is used for dependency management in the monorepo instead of `pip`.
Potery settings and list of dependencies is managed in `pyproject.toml` file for each package, in addition to the root.
To install a package, add  `<package-name> = "<verion>"` to the `pyproject.toml` file and install using `poetry install`.
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

#### Commit Messages Format (to be inforced through Code Review):
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
By default, poetry creates a python virtualenv.

### Local Dev environment
We're using VS Code DevContainer to run our dockerized development environment.
To run the development environment locally, click `Shift+Command+p -> Reopen in Container`

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

### Running cloud resources locally
We're leveraging AWS Localstack to emulate a cloud environment locally.
To do so, we are using docker-compose to setup the DevContainer and the Localstack container.

### Running lambda locally
* On MacOS
   Make sure your workspace folder is shared from the docker host.
  * Lambda handler with API:
    ```shell
    cd services/<service-folder> 
    poetry install
    poetry run python ../../packages/scripts/scripts/poetry/export_requirements.py  
    sam build
    sudo sam local start-api --container-host host.docker.internal
   ```
  * Lambda handler without API:
  ```shell
  cd services/<service-folder>
  poetry install
  poetry run python ../../packages/scripts/scripts/poetry/export_requirements.py  
  sam build
  sudo sam local invoke --container-host host.docker.internal
  ```

* On Windows
  * Lambda handler with API:
  ```shell
  cd services/<service-folder>
  poetry install
  poetry run python ../../packages/scripts/scripts/poetry/export_requirements.py  
  sam build
  sudo sam local start-api
  ```
  * Lambda handler without  API:
  ```shell
  cd services/<service-folder>
  poetry install
  poetry run python ../../packages/scripts/scripts/poetry/export_requirements.py 
  sam build
  sudo sam local invoke
  ```

You can also run the flask application directly without invoking the lambda: `flask --app <file-with-flask-app> run --debug`
