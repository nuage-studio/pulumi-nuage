# pulumi-nuage

Pulumi components carefully crafted by Nuage

TODO: use [the official repo](https://github.com/pulumi/pulumi-component-provider-py-boilerplate) to build a Pulumi Component Provider

# Install the Pulumi Plugin

To use this resource, you need to install Pulumi plugin first (independent from the development language).

1. Download the latest release from https://github.com/nuage-studio/pulumi-nuage/releases/
2. Install the .tar.gz package using Pulumi
```
pulumi plugin install resource nuage 0.0.1 --file pulumi-resource-nuage-v0.0.1-darwin-amd64.tar.gz
```

You may also automate this process via Taskfile. Here is an example:
```
version: "3"

tasks:
  pulumi_install:
    desc: Downloads binary
    env:
      FILE_NAME: "pulumi-resource-nuage-v0.0.1-darwin-amd64.tar.gz"
    cmds:
      - curl -L -o $FILE_NAME https://github.com/nuage-studio/pulumi-nuage/releases/download/0.0.1/${FILE_NAME}
      - pulumi plugin install resource nuage 0.0.1 --file $FILE_NAME
      - rm $FILE_NAME
```

# Setup Instructions for Python SDK

* You can add following line under the `[tool.poetry.dependencies]`, to use Python package.
```
pulumi-nuage = { git = "https://github.com/nuage-studio/pulumi-nuage.git", subdirectory = "sdk/python" }
```
* Then you need to run `poetry install`


# Start Working with us
You can configure your Nuage SSO with the pre-prepared Cloudformation template using the following link:

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=nuage-sso&templateURL=https://s3.eu-west-1.amazonaws.com/nuage.studio/nuage-sso-template.yml)
