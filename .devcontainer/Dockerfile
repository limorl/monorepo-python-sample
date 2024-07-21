# syntax=docker/dockerfile:1

# Default image for DevContainer: Python 3.12 for Apple Silicone
ARG IMAGE="mcr.microsoft.com/vscode/devcontainers/python"
ARG VERSION="3.12"
ARG VARIANT="-bullseye"

FROM ${IMAGE}:${VERSION}${VARIANT}

ARG TARGETARCH
ENV DEBIAN_FRONTEND=noninteractive

# Install common dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    lsb-release \
    software-properties-common \
    zip \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CE CLI
RUN curl -fsSL https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]')/gpg | apt-key add - 2>/dev/null \
    && echo "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]') $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# Install Docker Compose
RUN LATEST_COMPOSE_VERSION=$(curl -sSL "https://api.github.com/repos/docker/compose/releases/latest" | grep -o -P '(?<="tag_name": ").+(?=")') \
    && curl -sSL "https://github.com/docker/compose/releases/download/${LATEST_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose


# Install terraform
ARG TERRAFORM_VERSION="1.7.5"
RUN ARCH=${TARGETARCH:-$(dpkg --print-architecture)} && \
    echo "ARCH is set to: $ARCH" && \
    case $ARCH in \
        "x86_64") TF_ARCH="amd64" ;; \
        "amd64")  TF_ARCH="amd64" ;; \
        "arm64")  TF_ARCH="arm64" ;; \
        *)        echo "Unsupported architecture: $ARCH"; exit 1 ;; \
    esac \
    && echo "Installing Terraform for architecture: $TF_ARCH" \
    && curl "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_${TF_ARCH}.zip" -o "terraform.zip" \
    && unzip terraform.zip \
    && mv terraform /usr/local/bin/ \
    && rm -rf terraform.zip

# Install AWS CLI
RUN ARCH=${TARGETARCH:-$(dpkg --print-architecture)} && \
    echo "ARCH is set to: $ARCH" && \
    case $ARCH in \
        "x86_64") AWS_CLI_ARCH="x86_64" ;; \
        "amd64")  AWS_CLI_ARCH="x86_64" ;; \
        "arm64")  AWS_CLI_ARCH="aarch64" ;; \
        *)        echo "Unsupported architecture: $ARCH"; exit 1 ;; \
    esac \
    && echo "Installing AWS CLI for architecture: $AWS_CLI_ARCH" \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-${AWS_CLI_ARCH}.zip" -o "awscli.zip" \
    && unzip awscli.zip \
    && ./aws/install \
    && rm -rf aws \
    && rm awscli.zip

# Install Github CLI
ARG GH_CLI_VERSION=2.32.1
RUN ARCH=${TARGETARCH:-$(dpkg --print-architecture)} && \
    echo "ARCH is set to: $ARCH" && \
    if [ "$ARCH" != "arm64" ]; then \
        GH_ARCH="amd64" \
        && echo "Installing GitHub CLI for architecture: $GH_ARCH" \
        && curl -fsSL https://github.com/cli/cli/releases/download/v${GH_CLI_VERSION}/gh_${GH_CLI_VERSION}_linux_${GH_ARCH}.deb -o gh.deb \
        && dpkg -i gh.deb \
        && rm gh.deb; \
    else \
        echo "Skipping GitHub CLI installation for arm64 architecture"; \
    fi

# Install Python packages
RUN pip install poetry aws-sam-cli localstack awscli-local
# No need to create virtual env since we are running inside a dev container
# RUN poetry config virtualenvs.create false --local

# Configure git
RUN git config --global core.ignorecase false

ENV PATH="${PATH}:~/.local/bin"