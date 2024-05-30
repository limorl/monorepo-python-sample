
# Default image for DevContainer: Python 3.12 for Apple Silicone
ARG IMAGE="mcr.microsoft.com/vscode/devcontainers/python"
ARG VERSION="3.12"
ARG VARIANT="-bullseye"

FROM ${IMAGE}:${VERSION}${VARIANT}

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

RUN if [ "${TARGETARCH}" = "arm64" ]; then \
        export AWS_CLI_ARCH="aarch64" && \
        curl "https://awscli.amazonaws.com/awscli-exe-linux-${AWS_CLI_ARCH}.zip" -o "awscli.zip" && \
        unzip awscli.zip && \
        ./aws/install && \
        rm -rf aws && rm awscli.zip ; \
    else \
        export AWS_CLI_ARCH="x86_64" && \
        curl "https://awscli.amazonaws.com/awscli-exe-linux-${AWS_CLI_ARCH}.zip" -o "awscli.zip" && \
        unzip awscli.zip && \
        ./aws/install && \
        rm -rf aws && rm awscli.zip ; \
    fi

# Install AWS SAM CLI
RUN pip install aws-sam-cli

# Install Localstack and Localstack cli tools
RUN pip install localstack
RUN pip install awscli-local
ENV PATH="${PATH}:~/.local/bin"

# Install Poetry
RUN pip install poetry
# No need to create virtual env since we are running inside a dev container
# RUN poetry config virtualenvs.create false --local

# making git case sensitive, so rename from File.js to file.js will be makred as a change
RUN git config --global core.ignorecase false

