#!/bin/bash
set -ex

##
## Create some aliases
##
echo 'alias ll="ls -alF"' >> "$HOME/.bashrc"
echo 'alias la="ls -A"' >> "$HOME/.bashrc"
echo 'alias l="ls -CF"' >> "$HOME/.bashrc"

# Convenience workspace directory for later use
WORKSPACE_DIR=$(pwd)

# Change some Poetry settings to better deal with working in a container
poetry config cache-dir "${WORKSPACE_DIR}/.cache"
poetry config virtualenvs.in-project true

# Install all dependencies
poetry install
python run_script.py install-all

# Build all packages
python run_script.py build-all

# Install pre-commit and pre-push hooks
poetry run pre-commit install
poetry run pre-commit install --hook-type pre-push

# Localstack - Validation
localstack config validate --file .devcontainer/docker-compose.yml # Validate Localstack configuration

# Localstack - Aliases
echo "alias aws-localstack='AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1 AWS_ENDPOINT_URL=\\$CLOUD_ENDPOINT_OVERRIDE aws'" >> ~/.bashrc
echo "alias sam-localstack='AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1 AWS_ENDPOINT_URL=\\$CLOUD_ENDPOINT_OVERRIDE sam'" >> ~/.bashrc

# Localstack - Create initial resources (once terraform is added, it can be used to deploy all resources instead)
aws-localstack s3api create-bucket --bucket sam-lambdas

echo "post_create Done!"