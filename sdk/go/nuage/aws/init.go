// Code generated by Pulumi SDK Generator DO NOT EDIT.
// *** WARNING: Do not edit by hand unless you're certain you know what you are doing! ***

package aws

import (
	"fmt"

	"github.com/blang/semver"
	"github.com/pulumi/pulumi-nuage/sdk/go/nuage"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

type module struct {
	version semver.Version
}

func (m *module) Version() semver.Version {
	return m.version
}

func (m *module) Construct(ctx *pulumi.Context, name, typ, urn string) (r pulumi.Resource, err error) {
	switch typ {
	case "nuage:aws:Bastion":
		r = &Bastion{}
	case "nuage:aws:ContainerFunction":
		r = &ContainerFunction{}
	case "nuage:aws:Image":
		r = &Image{}
	case "nuage:aws:Repository":
		r = &Repository{}
	case "nuage:aws:ServerlessDatabase":
		r = &ServerlessDatabase{}
	default:
		return nil, fmt.Errorf("unknown resource type: %s", typ)
	}

	err = ctx.RegisterResource(typ, name, nil, r, pulumi.URN_(urn))
	return
}

func init() {
	version, err := nuage.PkgVersion()
	if err != nil {
		version = semver.Version{Major: 1}
	}
	pulumi.RegisterResourceModule(
		"nuage",
		"aws",
		&module{version},
	)
}
