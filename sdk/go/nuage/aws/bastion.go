// Code generated by Pulumi SDK Generator DO NOT EDIT.
// *** WARNING: Do not edit by hand unless you're certain you know what you are doing! ***

package aws

import (
	"context"
	"reflect"

	"github.com/pkg/errors"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

// Pulumi Nuage's Bastion resource enables the creation of a bastion host through the submission of provided VPC information. The resource creates a private key, security group, and an AWS EC2 `t4g.nano` instance that can serve as the bastion host. This allows secure connectivity to sensitive resources within the VPC, while maintaining isolation from the public internet. You can leverage the outputted private key to establish a connection to the bastion host.
//
// ## Example Usage
type Bastion struct {
	pulumi.ResourceState

	Private_key_pem pulumi.StringOutput `pulumi:"private_key_pem"`
	Public_ip       pulumi.StringOutput `pulumi:"public_ip"`
}

// NewBastion registers a new resource with the given unique name, arguments, and options.
func NewBastion(ctx *pulumi.Context,
	name string, args *BastionArgs, opts ...pulumi.ResourceOption) (*Bastion, error) {
	if args == nil {
		return nil, errors.New("missing one or more required arguments")
	}

	if args.SubnetId == nil {
		return nil, errors.New("invalid value for required argument 'SubnetId'")
	}
	if args.VpcId == nil {
		return nil, errors.New("invalid value for required argument 'VpcId'")
	}
	opts = pkgResourceDefaultOpts(opts)
	var resource Bastion
	err := ctx.RegisterRemoteComponentResource("nuage:aws:Bastion", name, args, &resource, opts...)
	if err != nil {
		return nil, err
	}
	return &resource, nil
}

type bastionArgs struct {
	// Ssh port for bastion host. Defaults to 22
	SshPort *float64 `pulumi:"sshPort"`
	// Public subnet id of the Vpc.
	SubnetId string `pulumi:"subnetId"`
	// Vpc id.
	VpcId string `pulumi:"vpcId"`
}

// The set of arguments for constructing a Bastion resource.
type BastionArgs struct {
	// Ssh port for bastion host. Defaults to 22
	SshPort pulumi.Float64PtrInput
	// Public subnet id of the Vpc.
	SubnetId pulumi.StringInput
	// Vpc id.
	VpcId pulumi.StringInput
}

func (BastionArgs) ElementType() reflect.Type {
	return reflect.TypeOf((*bastionArgs)(nil)).Elem()
}

type BastionInput interface {
	pulumi.Input

	ToBastionOutput() BastionOutput
	ToBastionOutputWithContext(ctx context.Context) BastionOutput
}

func (*Bastion) ElementType() reflect.Type {
	return reflect.TypeOf((**Bastion)(nil)).Elem()
}

func (i *Bastion) ToBastionOutput() BastionOutput {
	return i.ToBastionOutputWithContext(context.Background())
}

func (i *Bastion) ToBastionOutputWithContext(ctx context.Context) BastionOutput {
	return pulumi.ToOutputWithContext(ctx, i).(BastionOutput)
}

// BastionArrayInput is an input type that accepts BastionArray and BastionArrayOutput values.
// You can construct a concrete instance of `BastionArrayInput` via:
//
//	BastionArray{ BastionArgs{...} }
type BastionArrayInput interface {
	pulumi.Input

	ToBastionArrayOutput() BastionArrayOutput
	ToBastionArrayOutputWithContext(context.Context) BastionArrayOutput
}

type BastionArray []BastionInput

func (BastionArray) ElementType() reflect.Type {
	return reflect.TypeOf((*[]*Bastion)(nil)).Elem()
}

func (i BastionArray) ToBastionArrayOutput() BastionArrayOutput {
	return i.ToBastionArrayOutputWithContext(context.Background())
}

func (i BastionArray) ToBastionArrayOutputWithContext(ctx context.Context) BastionArrayOutput {
	return pulumi.ToOutputWithContext(ctx, i).(BastionArrayOutput)
}

// BastionMapInput is an input type that accepts BastionMap and BastionMapOutput values.
// You can construct a concrete instance of `BastionMapInput` via:
//
//	BastionMap{ "key": BastionArgs{...} }
type BastionMapInput interface {
	pulumi.Input

	ToBastionMapOutput() BastionMapOutput
	ToBastionMapOutputWithContext(context.Context) BastionMapOutput
}

type BastionMap map[string]BastionInput

func (BastionMap) ElementType() reflect.Type {
	return reflect.TypeOf((*map[string]*Bastion)(nil)).Elem()
}

func (i BastionMap) ToBastionMapOutput() BastionMapOutput {
	return i.ToBastionMapOutputWithContext(context.Background())
}

func (i BastionMap) ToBastionMapOutputWithContext(ctx context.Context) BastionMapOutput {
	return pulumi.ToOutputWithContext(ctx, i).(BastionMapOutput)
}

type BastionOutput struct{ *pulumi.OutputState }

func (BastionOutput) ElementType() reflect.Type {
	return reflect.TypeOf((**Bastion)(nil)).Elem()
}

func (o BastionOutput) ToBastionOutput() BastionOutput {
	return o
}

func (o BastionOutput) ToBastionOutputWithContext(ctx context.Context) BastionOutput {
	return o
}

type BastionArrayOutput struct{ *pulumi.OutputState }

func (BastionArrayOutput) ElementType() reflect.Type {
	return reflect.TypeOf((*[]*Bastion)(nil)).Elem()
}

func (o BastionArrayOutput) ToBastionArrayOutput() BastionArrayOutput {
	return o
}

func (o BastionArrayOutput) ToBastionArrayOutputWithContext(ctx context.Context) BastionArrayOutput {
	return o
}

func (o BastionArrayOutput) Index(i pulumi.IntInput) BastionOutput {
	return pulumi.All(o, i).ApplyT(func(vs []interface{}) *Bastion {
		return vs[0].([]*Bastion)[vs[1].(int)]
	}).(BastionOutput)
}

type BastionMapOutput struct{ *pulumi.OutputState }

func (BastionMapOutput) ElementType() reflect.Type {
	return reflect.TypeOf((*map[string]*Bastion)(nil)).Elem()
}

func (o BastionMapOutput) ToBastionMapOutput() BastionMapOutput {
	return o
}

func (o BastionMapOutput) ToBastionMapOutputWithContext(ctx context.Context) BastionMapOutput {
	return o
}

func (o BastionMapOutput) MapIndex(k pulumi.StringInput) BastionOutput {
	return pulumi.All(o, k).ApplyT(func(vs []interface{}) *Bastion {
		return vs[0].(map[string]*Bastion)[vs[1].(string)]
	}).(BastionOutput)
}

func init() {
	pulumi.RegisterInputType(reflect.TypeOf((*BastionInput)(nil)).Elem(), &Bastion{})
	pulumi.RegisterInputType(reflect.TypeOf((*BastionArrayInput)(nil)).Elem(), BastionArray{})
	pulumi.RegisterInputType(reflect.TypeOf((*BastionMapInput)(nil)).Elem(), BastionMap{})
	pulumi.RegisterOutputType(BastionOutput{})
	pulumi.RegisterOutputType(BastionArrayOutput{})
	pulumi.RegisterOutputType(BastionMapOutput{})
}
