# syntax=docker/dockerfile:1

# Default image for DevContainer: Python 3.12 for Apple Silicone
ARG IMAGE="mcr.microsoft.com/vscode/devcontainers/python"
ARG VERSION="3.12"
ARG VARIANT="-bullseye"

FROM ${IMAGE}:${VERSION}${VARIANT} as base

ARG TARGETARCH=${TARGETARCH}
ARG WORKSPACE_DIR=${WORKSPACE_DIR}
ENV DEBIAN_FRONTEND=noninteractive

RUN echo "User during build: $(whoami)"

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

ENV PATH="${PATH}:~/.local/bin"


FROM base AS ci

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

# Install Session Manager plugin
RUN ARCH=${TARGETARCH:-$(dpkg --print-architecture)} && \
echo "ARCH is set to: $ARCH" && \
case $ARCH in \
    "x86_64") SSM_ARCH="64bit" ;; \
    "amd64")  SSM_ARCH="64bit" ;; \
    "arm64")  SSM_ARCH="arm64" ;; \
    *)        echo "Unsupported architecture: $ARCH"; exit 1 ;; \
esac \
&& echo "Installing Session Manager plugin for architecture: $SSM_ARCH" \
&& curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_${SSM_ARCH}/session-manager-plugin.deb" -o "session-manager-plugin.deb" \
&& dpkg -i session-manager-plugin.deb \
&& rm session-manager-plugin.deb

# Install packages
RUN pip install poetry

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

# Install Git
RUN apt update \
&& apt install git -y && (type -p wget >/dev/null || ( apt update &&  apt-get install wget -y)) \
&& git config --global core.ignorecase false \
&& git config --global pull.rebase false

# Instacll and Cache Packages 
# ENV POETRY_CACHE_DIR=/opt/poetry/cache

# ARG TEMP_WORKSPACE=/tmp/workspace
# WORKDIR $TEMP_WORKSPACE
# COPY . $TEMP_WORKSPACE

# RUN echo "Installing packages and caching under ${POETRY_CACHE_DIR}..." \
# && mkdir -p ${POETRY_CACHE_DIR} \
# && chmod +x $TEMP_WORKSPACE/.devcontainer/install_packages.sh \
# && $TEMP_WORKSPACE/.devcontainer/install_packages.sh \
# && chmod -R 777 ${POETRY_CACHE_DIR} \
# && chown -R vscode:vscode ${POETRY_CACHE_DIR} \
# && rm -rf $TEMP_WORKSPACE


FROM ci AS dev
# Install terraform
ARG TERRAFORM_VERSION="1.9.3"
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


# Install Github CLI
RUN mkdir -p -m 755 /etc/apt/keyrings \
&& wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg |  tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
&&  chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" |  tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&&  apt update \
&&  apt install gh -y
