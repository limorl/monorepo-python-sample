#!/bin/bash

# This file runs in the context of Github Actions inside dev container 
# It runs sam build and sam deployed for selected lambda services

# Exit immediately if a command exits with a non-zero status
set -e


# Ensure correct number of arguments
if [ $# -ne 4 ]; then
    echo "Usage: $0 <dev|staging|prod> <aws-account-id> <aws-region> <update-config>"
    exit 1
fi

ENVIRONMENT=$1
AWS_ACCOUNT_ID=$2
AWS_REGION=$3
UPDATE_CONFIG=$4

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

deploy_service_configuration() {
    local service_name=$1

    if [ "$UPDATE_CONFIG" = "true" ]; then
        echo "Deploying configuration for service $service_name"

        if ! ./deploy-service-configuration.sh --service-name "$service_name" --stage "$ENVIRONMENT" --region "$AWS_REGION" --platform AWS; then
            echo "Error: Failed to deploy configuratio for service $service_name on environment $ENVIRONMENT in region $AWS_REGION. Aborting."
            return 1
        fi
    else
        echo "Skipping configuration deployment for service $service_name"
    fi
}

build_and_deploy_service() {
    local service_name=$1
    cd "services/$service_name"
    
    echo "Building and Deploying $service_name"
    
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
    
    echo "SAM Building $service_name:$package_version"
    echo "> sam build --config-env $ENVIRONMENT --parameter-overrides \"Stage=$ENVIRONMENT DockerTag=$package_version\""
    sam build --config-env "$ENVIRONMENT" --region "$AWS_REGION" --parameter-overrides "Stage=$ENVIRONMENT DockerTag=$package_version"

    echo "SAM Deploying $service_name:$package_version"
    echo "> sam deploy --config-env $ENVIRONMENT --parameter-overrides \"Stage=$ENVIRONMENT DockerTag=$package_version\""
    sam deploy --config-env "$ENVIRONMENT" --region "$AWS_REGION" --parameter-overrides "Stage=$ENVIRONMENT DockerTag=$package_version"
}

echo "Starting Build & Deploy deploy process for environment: $ENVIRONMENT on region $AWS_REGION"

repo_root=$PWD

# For now, we are deploying greeting only, should be changed to iterate over all services under ./services 
services_to_deploy=("greeting")

for service in "${services_to_deploy[@]}"; do
    deploy_service_configuration $service 
    build_and_deploy_service $service
    cd "$repo_root"
done

echo "Build and deploy process completed."