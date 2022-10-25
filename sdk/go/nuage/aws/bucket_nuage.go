// Code generated by Pulumi SDK Generator DO NOT EDIT.
// *** WARNING: Do not edit by hand unless you're certain you know what you are doing! ***

package aws

import (
	"context"
	"reflect"

	"github.com/pulumi/pulumi-aws/sdk/v4/go/aws/s3"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

type Bucket_nuage struct {
	pulumi.ResourceState

	// The bucket resource.
	Bucket s3.BucketOutput `pulumi:"bucket"`
}

// NewBucket_nuage registers a new resource with the given unique name, arguments, and options.
func NewBucket_nuage(ctx *pulumi.Context,
	name string, args *Bucket_nuageArgs, opts ...pulumi.ResourceOption) (*Bucket_nuage, error) {
	if args == nil {
		args = &Bucket_nuageArgs{}
	}

	var resource Bucket_nuage
	err := ctx.RegisterRemoteComponentResource("nuage:aws:bucket_nuage", name, args, &resource, opts...)
	if err != nil {
		return nil, err
	}
	return &resource, nil
}

type bucket_nuageArgs struct {
}

// The set of arguments for constructing a Bucket_nuage resource.
type Bucket_nuageArgs struct {
}

func (Bucket_nuageArgs) ElementType() reflect.Type {
	return reflect.TypeOf((*bucket_nuageArgs)(nil)).Elem()
}

type Bucket_nuageInput interface {
	pulumi.Input

	ToBucket_nuageOutput() Bucket_nuageOutput
	ToBucket_nuageOutputWithContext(ctx context.Context) Bucket_nuageOutput
}

func (*Bucket_nuage) ElementType() reflect.Type {
	return reflect.TypeOf((**Bucket_nuage)(nil)).Elem()
}

func (i *Bucket_nuage) ToBucket_nuageOutput() Bucket_nuageOutput {
	return i.ToBucket_nuageOutputWithContext(context.Background())
}

func (i *Bucket_nuage) ToBucket_nuageOutputWithContext(ctx context.Context) Bucket_nuageOutput {
	return pulumi.ToOutputWithContext(ctx, i).(Bucket_nuageOutput)
}

// Bucket_nuageArrayInput is an input type that accepts Bucket_nuageArray and Bucket_nuageArrayOutput values.
// You can construct a concrete instance of `Bucket_nuageArrayInput` via:
//
//	Bucket_nuageArray{ Bucket_nuageArgs{...} }
type Bucket_nuageArrayInput interface {
	pulumi.Input

	ToBucket_nuageArrayOutput() Bucket_nuageArrayOutput
	ToBucket_nuageArrayOutputWithContext(context.Context) Bucket_nuageArrayOutput
}

type Bucket_nuageArray []Bucket_nuageInput

func (Bucket_nuageArray) ElementType() reflect.Type {
	return reflect.TypeOf((*[]*Bucket_nuage)(nil)).Elem()
}

func (i Bucket_nuageArray) ToBucket_nuageArrayOutput() Bucket_nuageArrayOutput {
	return i.ToBucket_nuageArrayOutputWithContext(context.Background())
}

func (i Bucket_nuageArray) ToBucket_nuageArrayOutputWithContext(ctx context.Context) Bucket_nuageArrayOutput {
	return pulumi.ToOutputWithContext(ctx, i).(Bucket_nuageArrayOutput)
}

// Bucket_nuageMapInput is an input type that accepts Bucket_nuageMap and Bucket_nuageMapOutput values.
// You can construct a concrete instance of `Bucket_nuageMapInput` via:
//
//	Bucket_nuageMap{ "key": Bucket_nuageArgs{...} }
type Bucket_nuageMapInput interface {
	pulumi.Input

	ToBucket_nuageMapOutput() Bucket_nuageMapOutput
	ToBucket_nuageMapOutputWithContext(context.Context) Bucket_nuageMapOutput
}

type Bucket_nuageMap map[string]Bucket_nuageInput

func (Bucket_nuageMap) ElementType() reflect.Type {
	return reflect.TypeOf((*map[string]*Bucket_nuage)(nil)).Elem()
}

func (i Bucket_nuageMap) ToBucket_nuageMapOutput() Bucket_nuageMapOutput {
	return i.ToBucket_nuageMapOutputWithContext(context.Background())
}

func (i Bucket_nuageMap) ToBucket_nuageMapOutputWithContext(ctx context.Context) Bucket_nuageMapOutput {
	return pulumi.ToOutputWithContext(ctx, i).(Bucket_nuageMapOutput)
}

type Bucket_nuageOutput struct{ *pulumi.OutputState }

func (Bucket_nuageOutput) ElementType() reflect.Type {
	return reflect.TypeOf((**Bucket_nuage)(nil)).Elem()
}

func (o Bucket_nuageOutput) ToBucket_nuageOutput() Bucket_nuageOutput {
	return o
}

func (o Bucket_nuageOutput) ToBucket_nuageOutputWithContext(ctx context.Context) Bucket_nuageOutput {
	return o
}

type Bucket_nuageArrayOutput struct{ *pulumi.OutputState }

func (Bucket_nuageArrayOutput) ElementType() reflect.Type {
	return reflect.TypeOf((*[]*Bucket_nuage)(nil)).Elem()
}

func (o Bucket_nuageArrayOutput) ToBucket_nuageArrayOutput() Bucket_nuageArrayOutput {
	return o
}

func (o Bucket_nuageArrayOutput) ToBucket_nuageArrayOutputWithContext(ctx context.Context) Bucket_nuageArrayOutput {
	return o
}

func (o Bucket_nuageArrayOutput) Index(i pulumi.IntInput) Bucket_nuageOutput {
	return pulumi.All(o, i).ApplyT(func(vs []interface{}) *Bucket_nuage {
		return vs[0].([]*Bucket_nuage)[vs[1].(int)]
	}).(Bucket_nuageOutput)
}

type Bucket_nuageMapOutput struct{ *pulumi.OutputState }

func (Bucket_nuageMapOutput) ElementType() reflect.Type {
	return reflect.TypeOf((*map[string]*Bucket_nuage)(nil)).Elem()
}

func (o Bucket_nuageMapOutput) ToBucket_nuageMapOutput() Bucket_nuageMapOutput {
	return o
}

func (o Bucket_nuageMapOutput) ToBucket_nuageMapOutputWithContext(ctx context.Context) Bucket_nuageMapOutput {
	return o
}

func (o Bucket_nuageMapOutput) MapIndex(k pulumi.StringInput) Bucket_nuageOutput {
	return pulumi.All(o, k).ApplyT(func(vs []interface{}) *Bucket_nuage {
		return vs[0].(map[string]*Bucket_nuage)[vs[1].(string)]
	}).(Bucket_nuageOutput)
}

func init() {
	pulumi.RegisterInputType(reflect.TypeOf((*Bucket_nuageInput)(nil)).Elem(), &Bucket_nuage{})
	pulumi.RegisterInputType(reflect.TypeOf((*Bucket_nuageArrayInput)(nil)).Elem(), Bucket_nuageArray{})
	pulumi.RegisterInputType(reflect.TypeOf((*Bucket_nuageMapInput)(nil)).Elem(), Bucket_nuageMap{})
	pulumi.RegisterOutputType(Bucket_nuageOutput{})
	pulumi.RegisterOutputType(Bucket_nuageArrayOutput{})
	pulumi.RegisterOutputType(Bucket_nuageMapOutput{})
}
