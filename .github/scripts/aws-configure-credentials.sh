#!/bin/bash

set -e

role_arn=""
role_session_name=""
aws_region=""
duration_seconds=3600

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --role-to-assume)
        role_arn="$2"
        shift; shift
        ;;
        --role-session-name)
        role_session_name="$2"
        shift; shift
        ;;
        --aws-region)
        aws_region="$2"
        shift; shift
        ;;
        --role-duration-seconds)
        duration_seconds="$2"
        shift; shift
        ;;
        *)
        echo "Unknown option: $1"
        exit 1
        ;;
    esac
done

# Validate required inputs
if [ -z "$role_arn" ] || [ -z "$role_session_name" ] || [ -z "$aws_region" ]; then
    echo "Error: Missing required parameters"
    echo "Usage: $0 --role-to-assume <role_arn> --role-session-name <session_name> --aws-region <region> [--role-duration-seconds <duration>]"
    exit 1
fi

echo "Assuming role: $role_arn"
if ! creds=$(aws sts assume-role \
    --role-arn "$role_arn" \
    --role-session-name "$role_session_name" \
    --duration-seconds "$duration_seconds"); then
    echo "Failed to assume role"
    exit 1
fi

# Export the credentials
export AWS_ACCESS_KEY_ID=$(echo "$creds" | jq -r .Credentials.AccessKeyId)
export AWS_SECRET_ACCESS_KEY=$(echo "$creds" | jq -r .Credentials.SecretAccessKey)
export AWS_SESSION_TOKEN=$(echo "$creds" | jq -r .Credentials.SessionToken)
export AWS_DEFAULT_REGION="$aws_region"

# Verify the credentials are set
if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ] || [ -z "$AWS_SESSION_TOKEN" ]; then
    echo "Error: Failed to set AWS credentials"
    exit 1
fi

echo "AWS credentials configured successfully"
echo "Region set to: $aws_region"
echo "Role session will expire in $duration_seconds seconds"

# Verify the assumed role
echo "Verifying assumed role:"
if ! aws sts get-caller-identity; then
    echo "Error: Failed to verify AWS credentials"
    exit 1
fi

echo "AWS credentials verified successfully"