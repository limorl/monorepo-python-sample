
# Variant suitable fo Apple Silicone
#ARG VARIANT=3.10-bullseye 
#FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

# Default image for DevContainer: Python 3.10 for Apple Silicone
ARG IMAGE="mcr.microsoft.com/vscode/devcontainers/python"
ARG VERSION="3.10"
ARG VARIANT="-bullseye"

FROM ${IMAGE}:${VERSION}${VARIANT}

# Node.js version: none, lts/*, 16, 14, 12, 10
#ARG NODE_VERSION="lts/*"
#RUN su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"

# Default target architecture. For another architecture, change .env file
ARG TARGETARCH="arm64"

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
ARG TERRAFORM_VERSION="1.7.5"

# Install terraform
RUN curl "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_${TARGETARCH}.zip" -o "terraform.zip" \
    && unzip terraform.zip \
    && mv terraform /usr/local/bin/ \
    && rm -rf terraform.zip

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common zip unzip && \
    apt-get clean

# Install AWS CLI v2
RUN if [ "${TARGETARCH}" == "arm64" ]; then \
    export AWS_CLI_ARCH="aarch64"; \
    else \
        export AWS_CLI_ARCH="x86_64"; \
    fi
RUN echo :"*******  ${AWS_CLI_ARCH}    ***************"

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscli-exe-linux-aarch64.zip" \
    && unzip awscli-exe-linux-aarch64.zip \
    && ./aws/install \
    && rm -rf aws && rm awscli-exe-linux-aarch64.zip

# Install AWS SAM CLI
RUN pip install aws-sam-cli

# Install Localstack and Localstack cli tools
RUN pip install localstack
RUN pip install awscli-local
ENV PATH="${PATH}:~/.local/bin"

# making git case sensetive, so rename from File.js to file.js will be makred as a change
RUN git config --global core.ignorecase false

