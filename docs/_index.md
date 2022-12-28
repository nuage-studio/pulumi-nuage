---
title: Pulumi Nuage
meta_desc: Provides an overview of the Nuage Provider for Pulumi.
layout: overview
---

Pulumi Nuage provider can be used to provision AWS cloud resources.

## Example

{{< chooser language "typescript,python" >}}
{{% choosable language typescript %}}

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as nuage from "@pulumi/nuage";

const lambdaContainer = new nuage.aws.ContainerFunction("myfunction",{
    ecrRepositoryName:"ecr-repo-name",
    dockerfile:"./Dockerfile"    
});
```
 
{{% /choosable %}}
{{% choosable language python %}}

```python
import pulumi_nuage

container_function = pulumi_nuage.aws.ContainerFunction("myfunction",
    ecr_repository_name="ecr-repo-name",
    dockerfile="./Dockerfile"
)
```

{{% /choosable %}}

{{< /chooser >}}
