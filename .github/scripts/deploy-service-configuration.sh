#!/bin/bash

set -e

# Function to display usage information
# Assumed to be executed from repo root
usage() {
    echo "Usage: $0 --service-name <service-name> --stage <stage> --region <region> [--platform <platform>]"
    echo "  --service-name: The name of the service package, for example: greeting"
    echo "  --stage: Stage in [prod|dev|staging]"
    echo "  --region: Region e.g., us-east-1"
    echo "  --platform: The platform to deploy to, default is AWS"
    exit 1
}

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --service-name) SERVICE_NAME="$2"; shift ;;
        --stage) STAGE="$2"; shift ;;
        --region) REGION="$2"; shift ;;
        --platform) PLATFORM="$2"; shift ;;
        *) usage ;;
    esac
    shift
done

# Check required arguments
if [ -z "$SERVICE_NAME" ] || [ -z "$STAGE" ] || [ -z "$REGION" ]; then
    usage
fi

# Set default values and convert to lowercase
PLATFORM=${PLATFORM:-AWS}
PLATFORM_LOWER=$(echo "$PLATFORM" | tr '[:upper:]' '[:lower:]')
STAGE_LOWER=$(echo "$STAGE" | tr '[:upper:]' '[:lower:]')
REGION_LOWER=$(echo "$REGION" | tr '[:upper:]' '[:lower:]')

APP_NAME="${SERVICE_NAME}-service"
CONFIG_NAME="${PLATFORM_LOWER}.${STAGE_LOWER}.${REGION_LOWER}"
CONFIG_DIR="services/${SERVICE_NAME}/config"
CONFIG_FILE="${CONFIG_DIR}/${CONFIG_NAME}.json"

echo "APP_NAME=$APP_NAME"
echo "CONFIG_NAME=$CONFIG_NAME"
echo "CONFIG_DIR=$CONFIG_DIR"
echo "CONFIG_FILE=$CONFIG_FILE"

# Function to get or create AppConfig resource
get_or_create_resource() {
    local resource_type="$1"
    local name="$2"
    local list_args="${3:-}"
    local create_args="${4:-}"
    local warn_if_not_exists="${5:-true}"
    
    resource_id=$(aws appconfig list-${resource_type}s $list_args --query "Items[?Name=='$name'].Id" --output text)
    
    if [ -z "$resource_id" ]; then
        if [ "$warn_if_not_exists" = true ]; then
            echo "WARNING: $resource_type '$name' does not exist. Ensure it is included in Terraform configuration."
        fi
        echo "Creating $resource_type: $name"
        resource_id=$(aws appconfig create-${resource_type} --name "$name" $create_args --query "Id" --output text)
    fi
    
    echo "$resource_id"
}

# Get or create application
APP_ID=$(get_or_create_resource "application" "$APP_NAME")

# Get or create environment
ENV_ID=$(get_or_create_resource "environment" "$STAGE" "--application-id $APP_ID" "--application-id $APP_ID")

# Get or create configuration profile
PROFILE_ID=$(get_or_create_resource "configuration-profile" "$CONFIG_NAME" "--application-id $APP_ID" "--application-id $APP_ID --location-uri hosted")

# Create hosted configuration version
if [ -f "$CONFIG_FILE" ]; then
    echo "Creating new configuration version from $CONFIG_FILE"

    CONTENT_BASE64=$(base64 -w 0 "$CONFIG_FILE")
    TEMP_OUTPUT_FILE=$(mktemp)
    
    # Create the hosted configuration version and capture the output
    CLI_OUTPUT=$(aws appconfig create-hosted-configuration-version \
        --application-id "$APP_ID" \
        --configuration-profile-id "$PROFILE_ID" \
        --content "$CONTENT_BASE64" \
        --content-type "application/json" \
        $TEMP_OUTPUT_FILE)
    
    # Check if the command was successful
    if [ $? -ne 0 ]; then
        echo "Failed to create hosted configuration version"
        exit 1
    fi
    
    # Extract the version number from the CLI output
    VERSION=$(echo "$CLI_OUTPUT" | jq -r '.VersionNumber')
    
    if [ -z "$VERSION" ] || [ "$VERSION" == "null" ]; then
        echo "Failed to extract version number from response"
        exit 1
    fi
    
    echo "Created version: $VERSION"
    echo "Full CLI output:"
    echo "$CLI_OUTPUT" | jq '.'
else
    echo "Configuration file not found: $CONFIG_FILE"
    exit 1
fi

# Get deployment strategy
STRATEGY_NAME="${STAGE}-deployment-strategy"
STRATEGY_ID=$(aws appconfig list-deployment-strategies --query "Items[?Name=='$STRATEGY_NAME'].Id" --output text)

if [ -z "$STRATEGY_ID" ]; then
    echo "Deployment strategy not found: $STRATEGY_NAME"
    exit 1
fi

# Start deployment
echo "Starting deployment"
DEPLOYMENT=$(aws appconfig start-deployment \
    --application-id "$APP_ID" \
    --environment-id "$ENV_ID" \
    --deployment-strategy-id "$STRATEGY_ID" \
    --configuration-profile-id "$PROFILE_ID" \
    --configuration-version "$VERSION")

DEPLOYMENT_ID=$(echo "$DEPLOYMENT" | jq -r '.DeploymentNumber')

# Wait for deployment to complete
echo "Waiting for deployment to complete..."
while true; do
    STATUS=$(aws appconfig get-deployment \
        --application-id "$APP_ID" \
        --environment-id "$ENV_ID" \
        --deployment-number "$DEPLOYMENT_ID" \
        --query "State" \
        --output text)
    
    if [ "$STATUS" == "COMPLETE" ]; then
        echo "Deployment completed successfully"
        break
    elif [ "$STATUS" == "ROLLED_BACK" ] || [ "$STATUS" == "ROLLING_BACK" ]; then
        echo "Deployment failed"
        exit 1
    fi
    
    sleep 10
done

echo "Service configuration deployed successfully"