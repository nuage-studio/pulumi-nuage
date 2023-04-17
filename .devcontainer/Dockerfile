# https://hub.docker.com/_/microsoft-vscode-devcontainers
FROM mcr.microsoft.com/vscode/devcontainers/base

# Install pulumictl
ARG PULUMICTL_VERSION="0.0.42"
RUN ARCH=$(uname -m | sed 's/aarch64/arm64/') \
    && PULUMICTL_RELEASE="https://github.com/pulumi/pulumictl/releases/download/v${PULUMICTL_VERSION}/pulumictl-v${PULUMICTL_VERSION}-linux-${ARCH}.tar.gz" \
    && wget ${PULUMICTL_RELEASE} --output-document /tmp/pulumictl.tar.gz \
    && mkdir -p /home/vscode/.local/bin \
    && tar -xzf /tmp/pulumictl.tar.gz --directory /home/vscode/.local/bin \
    && rm /tmp/pulumictl.tar.gz
