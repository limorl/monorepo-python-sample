#!/bin/bash
set -ex

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

# Create Aliases
echo "alias aws-localstack='AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1 AWS_ENDPOINT_URL=$CLOUD_ENDPOINT_OVERRIDE aws'" >> ~/.bashrc
echo "alias sam-localstack='AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1 AWS_ENDPOINT_URL=$CLOUD_ENDPOINT_OVERRIDE sam'" >> ~/.bashrc

echo "post_create Done!"aws-localstack 