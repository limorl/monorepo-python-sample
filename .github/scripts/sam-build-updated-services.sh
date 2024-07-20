#!/bin/bash

# This file runs in the context of Github Actions inside dev container 
# It runs sam build for lambdas which have changed in recent pull request

# Ensure an environment argument is provided
if [ -z "$1" ]; then
  echo "No environment provided. Usage: ./sam-build-updated-services.sh <environment>"
  exit 1
fi

# Ensure an AWS account id argument is provided
if [ -z "$2" ]; then
  echo "No AWS account id provided. Usage: ./sam-build-updated-services.sh <environment> <aws-account-id>"
  exit 1
fi

ENVIRONMENT=$1
AWS_ACCOUNT_ID=$2

# Identify impacted Lambda services
changed_files=$(git diff --name-only origin/${GITHUB_BASE_REF} ${GITHUB_SHA})
echo "Changed files: $changed_files"

# Adjust grep and cut to correctly identify nested service directories
impacted_lambdas=$(echo "$changed_files" | grep -E '^services/[^/]+/' | cut -d'/' -f1,2 | sort | uniq)
echo "Impacted Lambda services: $impacted_lambdas"

# Clear the file before writing new content
> changed_lambdas.txt

# Build impacted Lambda services
for lambda in $impacted_lambdas; do
  echo "Building $lambda for environment $ENVIRONMENT"
  cd $lambda
  package_version=$(poetry version --short)
  sam build --config-env $ENVIRONMENT --parameter-overrides "DockerTag=$package_version"
  
  # Output lambda path and version to the file
  echo "$lambda:$package_version" >> ../changed_lambdas.txt
  
  cd -
done