#!/bin/bash

# This file runs in the context of Github Actions inside dev container 
# It runs sam build and sam deployed for selected lambda services

# Exit immediately if a command exits with a non-zero status
set -e


# Ensure correct number of arguments
if [ $# -ne 2 ]; then
    echo "Usage: ./sam-build-and-deploy-services.sh <dev|staging|prod> <aws-account-id>"
    exit 1
fi

ENVIRONMENT=$1
AWS_ACCOUNT_ID=$2

ENVIRONMENT_UPPER=$(echo "$ENVIRONMENT" | tr '[:lower:]' '[:upper:]')
ACCOUNT_ID_PLACEHOLDER="__${ENVIRONMENT_UPPER}_ACCOUNT_ID__"

add_write_permissions() {
    local file=$1
    chmod u+w "$file"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to add write permissions to $file"
        return 1
    fi
    return 0
}

replace_placeholder_with_value() {
    local file=$1
    local placeholder=$2
    local value=$3

    sed -i "s/$placeholder/$value/g" "$file"
    if grep -q "$placeholder" "$file"; then
        echo "Error: $placeholder still exists in $file. Replacement failed."
        return 1
    else
        echo "Successfully replaced $placeholder with $value in $file"
        return 0
    fi
}

build_and_deploy_service() {
    local service_name=$(basename "$PWD")
    
    echo "Processing $service_name"
    
    # Check if samconfig.toml exists
    if [ ! -f "samconfig.toml" ]; then
        echo "Warning: samconfig.toml not found in $service_name. Skipping."
        return
    fi
    
    # Add write permissions and replace account ID
    if ! add_write_permissions "samconfig.toml"; then
        echo "Error: Failed to add write permissions to samconfig.toml in $service_name. Skipping."
        return
    fi
    
    if ! replace_placeholder_with_value "samconfig.toml" "$ACCOUNT_ID_PLACEHOLDER" "$AWS_ACCOUNT_ID"; then
        echo "Error: Failed to replace Account ID in samconfig.toml in $service_name. Skipping."
        return
    fi
    
    # Get package version
    if [ -f "pyproject.toml" ]; then
        package_version=$(poetry version --short)
    else
        package_version="latest"
        echo "Warning: pyproject.toml not found in $service_name. Using 'latest' as version."
    fi
    
    echo "Building $service_name:$package_version"
    sam build --config-env "$ENVIRONMENT" --parameter-overrides "Stage=$ENVIRONMENT DockerTag=$package_version"
    
    echo "Deploying $service_name:$package_version"
    sam deploy --config-env "$ENVIRONMENT" --parameter-overrides "Stage=$ENVIRONMENT DockerTag=$package_version"
}

echo "Starting build and deploy process for environment: $ENVIRONMENT"

repo_root=$PWD

# Iterate over all directories in the services folder
# For now, we are deploying greeting only, for all services, uncomment this block
# while IFS= read -r -d '' service_dir; do
#     if [ -d "$service_dir" ]; then
#         cd "$service_dir" || continue
#         build_and_deploy_service
#         cd "$repo_root" || exit
#     fi
# done < <(find ./services -mindepth 1 -maxdepth 1 -type d -print0)

cd ./services/greeting
build_and_deploy_service
cd "$repo_root"

echo "Build and deploy process completed."