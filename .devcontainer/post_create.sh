#!/bin/bash
set -ex

echo "User during post_create.sh: $(whoami)"

# Convenience workspace directory for later use
echo "Workspace directory: ${WORKSPACE_DIR}"
git config --global --add safe.directory ${WORKSPACE_DIR}

## Bash aliases: general
echo 'alias ll="ls -alF"' >> "$HOME/.bashrc"
echo 'alias la="ls -A"'   >> "$HOME/.bashrc"
echo 'alias l="ls -CF"'   >> "$HOME/.bashrc"
echo 'alias lg="lazygit"' >> "$HOME/.bashrc"
echo 'alias python="poetry run python"' >> "$HOME/.bashrc"

# Enabling sharing the same host
sudo chmod 666 /var/run/docker.sock

chmod +x .devcontainer/install_packages.sh
./.devcontainer/install_packages.sh

# Temporarily disabled localstack
# Localstack - Validation
# localstack config validate --file .devcontainer/docker-compose.yml # Validate Localstack configuration

# Create Aliases
# echo "alias aws-localstack='AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1 AWS_ENDPOINT_URL=$CLOUD_ENDPOINT_OVERRIDE aws'" >> ~/.bash_aliases
# echo "alias sam-localstack='AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1 AWS_ENDPOINT_URL=$CLOUD_ENDPOINT_OVERRIDE sam'" >> ~/.bash_aliases
