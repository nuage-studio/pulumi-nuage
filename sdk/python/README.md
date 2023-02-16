# pulumi-nuage

Pulumi components carefully crafted by Nuage

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
