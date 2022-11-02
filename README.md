# pulumi-nuage

Pulumi components carefully crafted by Nuage

## Install the Pulumi Plugin

To use this resource, you need to install Pulumi plugin first (independent from the development language).

1. Download the latest release from <https://github.com/nuage-studio/pulumi-nuage/releases/>
2. Install the .tar.gz package using Pulumi

```bash
pulumi plugin install resource nuage 0.0.1 --file pulumi-resource-nuage-v0.0.1-darwin-amd64.tar.gz
```

You may also automate this process via Taskfile. Here is an example:

```yaml
version: "3"

tasks:
  pulumi_install:
    desc: Downloads binary
    vars:
      VERSION: 0.0.1
      FILE_NAME: "pulumi-resource-nuage-v0.0.1-darwin-amd64.tar.gz"
    cmds:
      - curl -L -o {{.FILE_NAME}} https://github.com/nuage-studio/pulumi-nuage/releases/download/{{.VERSION}}/{{.FILE_NAME}}
      - pulumi plugin install resource nuage {{.VERSION}} --file {{.FILE_NAME}}
      - rm {{.FILE_NAME}}
```

## Setup Instructions for Python SDK

You can use the following command to add python library via Poetry:

```bash
poetry add "https://github.com/nuage-studio/pulumi-nuage.git#subdirectory=sdk/python"
```

You can check related [Poetry Docs](https://python-poetry.org/docs/dependency-specification/) for more detailed information about subdirectory dependency.

## Start Working with us

If you want to collaborate with us, feel free to contact us at contact@nuage.studio

Should you need to give us access to your existing AWS account, you can use the Cloudformation link below which will deploy an AWS IdentityProvider that trusts our SSO.

You will need a SAML Metadata document (XML) which we'll happily provide you via email.

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=nuage-sso&templateURL=https://s3.eu-west-1.amazonaws.com/nuage.studio/nuage-sso-template.yml)
