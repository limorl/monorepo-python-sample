# Scripts

## Installing Scripts

This section in `pyproject.toml` file configures scripts that can be run using `poetry sun <script>` after the package is installed using `poetry install`:

```shell
[tool.poetry.scripts]
install-all = "scripts.poetry.install_all:install_all"
build-all = "scripts.poetry.build_all:build_all"
pytest-all = "scripts.testing.pytest_all:main"
pytest-impacted-only = "scripts.testing.pytest_impacted_only:pytest_impacted_only"
deploy-service-configuration = "scripts.deployment.deploy_service_configuration:main" # args --service-name <service-name> --stage <stage> --region <region>
```

To run those scripts from the root folder or from a sub directory, we had to wrap those scripts and locate it under the root repo: `monorepo-python-sample/run_script.py`.

## Adding/Updating scripts

If you are adding or updatimg scripts, you need to add them to `[tool.poetry.scripts]` configuration and re-install the scripts package before you can run them via `run_script.py`

## Running Scripts

Run the script from the monorepo root using `poetry run <
