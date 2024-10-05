#!/bin/bash

# Script for Terraform Pre-requisites on each environment
# This script should run by Account Administrators after they logged in using `aws sso login`
# It creates the necessary resources to allow managing terraform backend on AWS S3 using Github Actions:
#   1. S3 bucket - to store bacend state
#   2. DynamoDB table - to store lock keys
#   3. Open ID Provider for Github Actions - to allow access from Github Actions
#   4. GithubActions Role with relevant permissions and trust policy
#
# Running the script:
#   1. Ensure you configured AWS SSO for each environment and saved the profile as dev, staging and prod (see README.md)
#   2. terraform-setup.sh <dev|staging|prod>

# Load account variables
source account-setup.env

check_env_vars() {
    local vars=("AWS_PRIMARY_REGION_DEV" "AWS_PRIMARY_REGION_STAGING" "AWS_PRIMARY_REGION_PROD"
                "AWS_ACCOUNT_ID_DEV" "AWS_ACCOUNT_ID_STAGING" "AWS_ACCOUNT_ID_PROD")
    for var in "${vars[@]}"; do
        if [ -z "${!var}" ]; then
            echo "Error: $var is not set"
            exit 1
        fi
    done
}

# Create S3 Bucket on primary region (on dev, staging and prod).
# Source: https://developer.hashicorp.com/terraform/language/settings/backends/s3
create_s3_bucket() {
    if aws s3api head-bucket --bucket "$TERRAFORM_BACKEND_BUCKET_NAME" --profile "$ENVIRONMENT" &> /dev/null; then

        echo "Bucket $TERRAFORM_BACKEND_BUCKET_NAME already exists. Skipping creation."
    else
        echo "Creating bucket $TERRAFORM_BACKEND_BUCKET_NAME"
        if [ "$AWS_PRIMARY_REGION" = "us-east-1" ]; then
        aws s3api create-bucket \
            --bucket "$TERRAFORM_BACKEND_BUCKET_NAME" \
            --region "$AWS_PRIMARY_REGION" \
            --profile "$ENVIRONMENT" || { echo "Failed to create S3 bucket"; exit 1; }
        else
            aws s3api create-bucket \
                --bucket "$TERRAFORM_BACKEND_BUCKET_NAME" \
                --region "$AWS_PRIMARY_REGION" \
                --create-bucket-configuration LocationConstraint="$AWS_PRIMARY_REGION" \
                --profile "$ENVIRONMENT" || { echo "Failed to create S3 bucket"; exit 1; }
        fi
    fi

    aws s3api put-bucket-versioning \
        --bucket "$TERRAFORM_BACKEND_BUCKET_NAME" \
        --versioning-configuration Status=Enabled \
        --profile "$ENVIRONMENT" || { echo "Failed to enable bucket versioning"; exit 1; }

    aws s3api put-bucket-ownership-controls \
        --bucket "$TERRAFORM_BACKEND_BUCKET_NAME" \
        --ownership-controls '{"Rules":[{"ObjectOwnership":"BucketOwnerEnforced"}]}' \
        --profile "$ENVIRONMENT" || { echo "Failed to set bucket ownership controls"; exit 1; }

    aws s3api put-public-access-block \
        --bucket "$TERRAFORM_BACKEND_BUCKET_NAME" \
        --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true" \
        --profile "$ENVIRONMENT" || { echo "Failed to set public access block"; exit 1; }
}


# Create DynamoDB table on primary region (for dev, staging, prod), to store state lock keys.
# Source: https://developer.hashicorp.com/terraform/language/settings/backends/s3
create_dynamodb_table() {
    local table_name="tfstate-lock-$ENVIRONMENT"

    if aws dynamodb describe-table --table-name "$table_name" --profile "$ENVIRONMENT" &> /dev/null; then
        echo "DynamoDB table $table_name already exists. Checking deletion protection."

        # Check if deletion protection is enabled
        if aws dynamodb describe-table --table-name "$table_name" --profile "$ENVIRONMENT" | grep -q '"DeletionProtectionEnabled": true'; then
            echo "Deletion protection is already enabled for $table_name."
        else
            echo "Enabling deletion protection for $table_name"
            aws dynamodb update-table \
                --table-name "$table_name" \
                --deletion-protection-enabled \
                --profile "$ENVIRONMENT" || { echo "Failed to enable deletion protection"; exit 1; }
        fi
    else
        echo "Creating DynamoDB Table for Lock Key with deletion protection"
        aws dynamodb create-table \
            --table-name "$table_name" \
            --attribute-definitions AttributeName=LockID,AttributeType=S \
            --key-schema AttributeName=LockID,KeyType=HASH \
            --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
            --deletion-protection-enabled \
            --region "$AWS_PRIMARY_REGION" \
            --profile "$ENVIRONMENT" || { echo "Failed to create DynamoDB table"; exit 1; }

        echo "Waiting for table to be created..."
        aws dynamodb wait table-exists \
            --table-name "$table_name" \
            --profile "$ENVIRONMENT" || { echo "Failed to wait for table creation"; exit 1; }

        echo "Table created successfully with deletion protection enabled."
    fi
}

# Create OIDC IAM Role on primary region (for dev, staging and prod) to allow Github Actions
# to provision resources on AWS (see below for more details).
# Guidelines here:
# https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
create_github_actions_role() {
    local role_name="GithubActionsRole"

    if ! aws iam get-role --role-name "$role_name" --profile "$ENVIRONMENT" &> /dev/null; then
        echo "Creating an OIDC provider for GithubActions"
        aws iam create-open-id-connect-provider \
            --url "https://token.actions.githubusercontent.com" \
            --client-id-list "sts.amazonaws.com" \
            --thumbprint-list "$GITHUB_OIDC_THUMBPRINT" \
            --region "$AWS_PRIMARY_REGION" \
            --profile "$ENVIRONMENT" || { echo "Failed to create OIDC provider"; exit 1; }

        echo "Creating an IAM Role for Github Actions"
        local trust_policy=$(generate_github_actions_trust_policy)
        aws iam create-role --role-name "$role_name" \
            --assume-role-policy-document "$trust_policy" \
            --description "IAM role for GitHub Actions" \
            --region "$AWS_PRIMARY_REGION" \
            --profile "$ENVIRONMENT" || { echo "Failed to create IAM role"; exit 1; }
    else
        echo "IAM role $role_name already exists. Updating trust policy."
        manage_github_actions_trust_policy
    fi

    # Manage the Terraform policy
    manage_terraform_policy
}

generate_github_actions_trust_policy() {
    cat << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::$AWS_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                },
                "StringLike": {
                    "token.actions.githubusercontent.com:sub": [
                        "repo:limorl/monorepo-python-sample:environment:dev",
                        "repo:limorl/monorepo-python-sample:environment:staging",
                        "repo:limorl/monorepo-python-sample:environment:prod"
                    ]
                }
            }
        }
    ]
}
EOF
}

manage_terraform_policy() {
    local policy_name="TerraformPolicy"
    local policy_arn="arn:aws:iam::$AWS_ACCOUNT_ID:policy/$policy_name"
    local policy_document="terraform-iam-policy.json"

    if aws iam get-policy --policy-arn "$policy_arn" --profile "$ENVIRONMENT" &> /dev/null; then
        echo "Updating existing policy: $policy_name"

        local version_id=$(aws iam get-policy --policy-arn "$policy_arn" --profile "$ENVIRONMENT" --query 'Policy.DefaultVersionId' --output text)

        aws iam create-policy-version \
            --policy-arn "$policy_arn" \
            --policy-document file://$policy_document \
            --set-as-default \
            --profile "$ENVIRONMENT" || { echo "Failed to update policy"; exit 1; }

        aws iam delete-policy-version \
            --policy-arn "$policy_arn" \
            --version-id "$version_id" \
            --profile "$ENVIRONMENT" || { echo "Failed to delete old policy version"; exit 1; }

        echo "Policy updated successfully"
    else
        echo "Creating new policy: $policy_name"
        aws iam create-policy \
            --policy-name "$policy_name" \
            --policy-document file://$policy_document \
            --profile "$ENVIRONMENT" || { echo "Failed to create policy"; exit 1; }
        echo "Policy created successfully"
    fi

    if ! aws iam list-attached-role-policies --role-name GithubActionsRole --profile "$ENVIRONMENT" | grep -q "$policy_arn"; then
        echo "Attaching policy to GithubActionsRole"
        aws iam attach-role-policy \
            --role-name GithubActionsRole \
            --policy-arn "$policy_arn" \
            --profile "$ENVIRONMENT" || { echo "Failed to attach policy to role"; exit 1; }
    else
        echo "Policy already attached to GithubActionsRole"
    fi
}

manage_github_actions_trust_policy() {
    local role_name="GithubActionsRole"
    local trust_policy=$(generate_github_actions_trust_policy)

    if aws iam get-role --role-name "$role_name" --profile "$ENVIRONMENT" &> /dev/null; then
        echo "Updating trust policy for role: $role_name"
        aws iam update-assume-role-policy \
            --role-name "$role_name" \
            --policy-document "$trust_policy" \
            --profile "$ENVIRONMENT" || { echo "Failed to update trust policy"; exit 1; }
        echo "Trust policy updated successfully"
    else
        echo "Role $role_name does not exist. It will be created with this trust policy."
    fi
}

# Main script execution
if [ $# -eq 0 ]; then
    echo "Please provide environment: dev, staging or prod"
    exit 1
fi

readonly ENVIRONMENT=$1
readonly TERRAFORM_BACKEND_BUCKET_NAME="$ENVIRONMENT-terraform-backend-450y5"
readonly GITHUB_OIDC_THUMBPRINT="1b511abead59c6ce207077c0bf0e0043b1382612" # This thumbrint is not a secret, it's public

check_env_vars

if [ "$ENVIRONMENT" = "dev" ]; then
  AWS_PRIMARY_REGION=$AWS_PRIMARY_REGION_DEV
  AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID_DEV
  export AWS_REGION=$AWS_PRIMARY_REGION # This way, no need to specifu region in each command
elif [ "$ENVIRONMENT" = "staging" ]; then
  AWS_PRIMARY_REGION=$AWS_PRIMARY_REGION_STAGING
  AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID_STAGING
elif [ "$ENVIRONMENT" = "prod" ]; then
  AWS_PRIMARY_REGION=$AWS_PRIMARY_REGION_PROD
  AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID_PROD
else
    echo "Unknown environment, value must be 'dev', 'staging' or 'prod'"
    exit 1
fi

echo "Setting up terraform backend for ENVIRONMENT=$ENVIRONMENT on region $AWS_PRIMARY_REGION"

create_s3_bucket
create_dynamodb_table
create_github_actions_role

echo "Terraform Setup Completed!"
