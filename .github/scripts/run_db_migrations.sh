#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Pipe failures in a pipeline will also exit the script
set -o pipefail

# Check if required arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Error: Incorrect number of arguments, expected 3" >&2
    echo "Usage: $0 <alembic-command> <folder> <env> <ssm_instance_id>" >&2
    echo "Example: $0 "alembic upgrade head" ./dbs/maindb dev i-099dd0000882737" >&2

    exit 1
fi

ALEMBIC_COMMAND=$1
FOLDER=$2
ENV=$3
SSM_INSTANCE_ID=$4

cleanup() {
    echo "Cleaning up..."
    unset DB_USER DB_PASS DB_HOST DB_PORT DB_NAME

    # Kill the SSM session if it exists
    if [ ! -z "$SSM_PID" ]; then
        kill $SSM_PID || true
    fi
}

# Set up trap to call cleanup function on script exit
trap cleanup EXIT

echo "Retrieving database credentials from secrets manager..."
DB_CREDENTIALS=$(aws secretsmanager get-secret-value --secret-id ${ENV}/rds/credentials/maindb-${ENV} --query SecretString --output text)

# Check if credentials were retrieved successfully
if [ -z "$DB_CREDENTIALS" ]; then
    echo "Error: Failed to retrieve database credentials from Secrets Manager" >&2
    exit 1
fi

# Parse the JSON and set environment variables, used by alembic
export DB_USER=$(echo "$DB_CREDENTIALS" | jq -r .username)
export DB_PASS=$(echo "$DB_CREDENTIALS" | jq -r .password)
export DB_HOST=$(echo "$DB_CREDENTIALS" | jq -r .host)
export DB_PORT=$(echo "$DB_CREDENTIALS" | jq -r .port)
export DB_NAME=$(echo "$DB_CREDENTIALS" | jq -r .dbname)

# Check if all required environment variables are set
for var in DB_USER DB_PASS DB_HOST DB_PORT DB_NAME; do
    if [ -z "${!var}" ]; then
        echo "Error: $var is not set or empty" >&2
        exit 1
    fi
done

echo "Starting SSM session for port forwarding..."

# override DB_PORT and DB_HOST with SSM Tunnel local port and local host
SSM_PORT=$DB_PORT
SSM_LOCAL_PORT="1${SSM_PORT}"
SSM_HOST=$DB_HOST
export DB_PORT=$SSM_LOCAL_PORT  # make sure alembic uses ssm local port
export DB_HOST='localhost'

aws ssm start-session --target $SSM_INSTANCE_ID \
    --document-name AWS-StartPortForwardingSessionToRemoteHost \
    --parameters "{\"host\":[\"$SSM_HOST\"], \"portNumber\":[\"$SSM_PORT\"], \"localPortNumber\":[\"$SSM_LOCAL_PORT\"]}" &

SSM_PID=$!

echo "SSM Process id = $SSM_PID"

# Check if the SSM session is still running
if ! kill -0 $SSM_PID 2>/dev/null; then
    echo "Error: SSM session failed to start or terminated unexpectedly" >&2
    exit 1
fi


echo "Waiting for SSM tunnel to be established..."
sleep 5

echo "Running '$ALEMBIC_COMMAND' for package $FOLDER"
cd "$FOLDER" || { echo "Error: Failed to change to directory $FOLDER" >&2; exit 1; }
eval "$ALEMBIC_COMMAND"

echo "Database migration completed successfully"

# The cleanup function will be called automatically due to the trap