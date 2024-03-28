
ARG VARIANT=0-3.10-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

# Set the working directory in the container to /workspace
# This creates the directory if it does not already exist
WORKDIR /workspace

# making git case sensetive, so rename from File.js to file.js will be makred as a change
RUN git config --global core.ignorecase false

# Install Docker CE CLI
RUN apt-get update \
    && apt-get install -y apt-transport-https ca-certificates curl gnupg2 lsb-release \
    && curl -fsSL https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]')/gpg | apt-key add - 2>/dev/null \
    && echo "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]') $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce-cli

# Install Docker Compose
RUN export LATEST_COMPOSE_VERSION=$(curl -sSL "https://api.github.com/repos/docker/compose/releases/latest" | grep -o -P '(?<="tag_name": ").+(?=")') \
    && curl -sSL "https://github.com/docker/compose/releases/download/${LATEST_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

# Install terraform
ENV TERRAFORM_VERSION "1.7.5"
RUN curl "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_arm64.zip" -o "terraform_${TERRAFORM_VERSION}_linux_arm64.zip" \
     && unzip terraform_${TERRAFORM_VERSION}_linux_arm64.zip \
     && mv terraform /usr/local/bin/ \
     && rm -rf terraform_${TERRAFORM_VERSION}_linux_arm64.zip

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common zip unzip && \
    apt-get clean

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf aws && rm awscliv2.zip

# Install AWS SAM CLI
RUN pip install aws-sam-cli

# Verify the installation
RUN aws --version && sam --version

# Install Localstack and Localstack cli tools
RUN pip install localstack
RUN pip install awscli-local
ENV PATH="${PATH}:~/.local/bin"

# DebugPy
EXPOSE 5678

# Add a non-root user for better security
RUN useradd -m developer && chown -R developer /workspace
USER developer



