
# Default image for DevContainer: Python 3.12 for Apple Silicone
ARG IMAGE="mcr.microsoft.com/vscode/devcontainers/python"
ARG VERSION="3.12"
ARG VARIANT="-bullseye"

FROM ${IMAGE}:${VERSION}${VARIANT}

ARG TARGETARCH
RUN echo "TARGETARCH is: ${TARGETARCH}"

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

RUN ARCH=${TARGETARCH:-$(dpkg --print-architecture)} && \
    echo "ARCH is set to: $ARCH" && \
    case $ARCH in \
        "x86_64") TF_ARCH="amd64" ;; \
        "amd64")  TF_ARCH="amd64" ;; \
        "arm64")  TF_ARCH="arm64" ;; \
        *)        echo "Unsupported architecture: $ARCH"; exit 1 ;; \
    esac && \
    echo "Installing Terraform for architecture: $TF_ARCH" && \
    curl "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_${TF_ARCH}.zip" -o "terraform.zip" \
    && unzip terraform.zip \
    && mv terraform /usr/local/bin/ \
    && rm -rf terraform.zip

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common zip unzip && \
    apt-get clean

# Install AWS CLI
RUN ARCH=${TARGETARCH:-$(dpkg --print-architecture)} && \
    echo "ARCH is set to: $ARCH" && \
    case $ARCH in \
        "x86_64") AWS_CLI_ARCH="x86_64" ;; \
        "amd64")  AWS_CLI_ARCH="x86_64" ;; \
        "arm64")  AWS_CLI_ARCH="aarch64" ;; \
        *)        echo "Unsupported architecture: $ARCH"; exit 1 ;; \
    esac && \
    echo "Installing AWS CLI for architecture: $AWS_CLI_ARCH" && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-${AWS_CLI_ARCH}.zip" -o "awscli.zip" && \
    unzip awscli.zip && \
    ./aws/install && \
    rm -rf aws && rm awscli.zip ;

# Github CLI Default Version
ARG GH_CLI_VERSION=2.32.1

# Install Github CLI (used by Github Actions)
RUN apt-get update && apt-get install -y \
    curl \
    gpg \
    && rm -rf /var/lib/apt/lists/*


RUN ARCH=${TARGETARCH:-$(dpkg --print-architecture)} && \
    echo "ARCH is set to: $ARCH" && \
    if [ "$ARCH" != "arm64" ]; then \
        case $ARCH in \
            "x86_64") GH_ARCH="amd64" ;; \
            "amd64")  GH_ARCH="amd64" ;; \
            *)        echo "Unsupported architecture: $ARCH" && exit 1 ;; \
        esac && \
        echo "Installing GitHub CLI for architecture: $GH_ARCH" && \
        curl -fsSL https://github.com/cli/cli/releases/download/v${GH_CLI_VERSION}/gh_${GH_CLI_VERSION}_linux_${GH_ARCH}.deb -o gh.deb && \
        dpkg -i gh.deb && \
        rm gh.deb; \
    else \
        echo "Skipping GitHub CLI installation for arm64 architecture"; \
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

