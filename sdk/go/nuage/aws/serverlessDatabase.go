// Code generated by Pulumi SDK Generator DO NOT EDIT.
// *** WARNING: Do not edit by hand unless you're certain you know what you are doing! ***

package aws

import (
	"context"
	"reflect"

	"github.com/pkg/errors"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

// The ServerlessDatabase component is a convenient and efficient solution for creating serverless databases using Amazon RDS Aurora. It automatically creates components such as subnet group, security group, security group rules, and RDS cluster, and securely manages the DB credentials. With support for both MySQL and PostgreSQL, it provides a fully configured serverless database resource for your serverless database needs.
//
// ## Example Usage
type ServerlessDatabase struct {
	pulumi.ResourceState

	// IP address of the bastion host. Exists only if bastion is enabled
	Bastion_ip pulumi.StringPtrOutput `pulumi:"bastion_ip"`
	// Private key to connect bastion host over SSH. Exists only if bastion is enabled.
	Bastion_private_key pulumi.StringPtrOutput `pulumi:"bastion_private_key"`
	// ARN (Amazon Resource Name) of the RDS cluster.
	Cluster_arn pulumi.StringOutput `pulumi:"cluster_arn"`
	// Name of the database
	Database_name pulumi.StringOutput `pulumi:"database_name"`
	// Host address of DB server
	Host pulumi.StringOutput `pulumi:"host"`
	// Password of DB credentials
	Password pulumi.StringPtrOutput `pulumi:"password"`
	// Port number of DB
	Port pulumi.Float64Output `pulumi:"port"`
	// Database URI for connection.
	Uri pulumi.StringOutput `pulumi:"uri"`
	// Username of DB credentials.
	User pulumi.StringOutput `pulumi:"user"`
}

// NewServerlessDatabase registers a new resource with the given unique name, arguments, and options.
func NewServerlessDatabase(ctx *pulumi.Context,
	name string, args *ServerlessDatabaseArgs, opts ...pulumi.ResourceOption) (*ServerlessDatabase, error) {
	if args == nil {
		return nil, errors.New("missing one or more required arguments")
	}

	if args.DatabaseName == nil {
		return nil, errors.New("invalid value for required argument 'DatabaseName'")
	}
	if args.DatabaseType == nil {
		return nil, errors.New("invalid value for required argument 'DatabaseType'")
	}
	if args.MasterUserName == nil {
		return nil, errors.New("invalid value for required argument 'MasterUserName'")
	}
	if args.SubnetIds == nil {
		return nil, errors.New("invalid value for required argument 'SubnetIds'")
	}
	if args.VpcId == nil {
		return nil, errors.New("invalid value for required argument 'VpcId'")
	}
	opts = pkgResourceDefaultOpts(opts)
	var resource ServerlessDatabase
	err := ctx.RegisterRemoteComponentResource("nuage:aws:ServerlessDatabase", name, args, &resource, opts...)
	if err != nil {
		return nil, err
	}
	return &resource, nil
}

type serverlessDatabaseArgs struct {
	// Configure the bastion host for connecting the db.
	Bastion *BastionConfig `pulumi:"bastion"`
	// Name of the database.
	DatabaseName string `pulumi:"databaseName"`
	// Database type. `mysql` or `postgresql`
	DatabaseType string `pulumi:"databaseType"`
	// List of whitelisted IP addresses. If not specified, it will be public 0.0.0.0/0
	IpWhitelist []string `pulumi:"ipWhitelist"`
	// Master user name of the db.
	MasterUserName string `pulumi:"masterUserName"`
	// Determines whether a final DB snapshot is created before the DB instance is deleted. Defaults to `false`
	SkipFinalSnapshot *bool `pulumi:"skipFinalSnapshot"`
	// List of subnet ip addresses. If you want your database will be accessible from the internet, it should be public (`vpc.public_subnet_ids`). Otherwise, you can use private subnets (`vpc.private_subnet_ids`).
	SubnetIds []string `pulumi:"subnetIds"`
	// Vpc id.
	VpcId string `pulumi:"vpcId"`
}

// The set of arguments for constructing a ServerlessDatabase resource.
type ServerlessDatabaseArgs struct {
	// Configure the bastion host for connecting the db.
	Bastion BastionConfigPtrInput
	// Name of the database.
	DatabaseName pulumi.StringInput
	// Database type. `mysql` or `postgresql`
	DatabaseType pulumi.StringInput
	// List of whitelisted IP addresses. If not specified, it will be public 0.0.0.0/0
	IpWhitelist pulumi.StringArrayInput
	// Master user name of the db.
	MasterUserName pulumi.StringInput
	// Determines whether a final DB snapshot is created before the DB instance is deleted. Defaults to `false`
	SkipFinalSnapshot pulumi.BoolPtrInput
	// List of subnet ip addresses. If you want your database will be accessible from the internet, it should be public (`vpc.public_subnet_ids`). Otherwise, you can use private subnets (`vpc.private_subnet_ids`).
	SubnetIds pulumi.StringArrayInput
	// Vpc id.
	VpcId pulumi.StringInput
}

func (ServerlessDatabaseArgs) ElementType() reflect.Type {
	return reflect.TypeOf((*serverlessDatabaseArgs)(nil)).Elem()
}

type ServerlessDatabaseInput interface {
	pulumi.Input

	ToServerlessDatabaseOutput() ServerlessDatabaseOutput
	ToServerlessDatabaseOutputWithContext(ctx context.Context) ServerlessDatabaseOutput
}

func (*ServerlessDatabase) ElementType() reflect.Type {
	return reflect.TypeOf((**ServerlessDatabase)(nil)).Elem()
}

func (i *ServerlessDatabase) ToServerlessDatabaseOutput() ServerlessDatabaseOutput {
	return i.ToServerlessDatabaseOutputWithContext(context.Background())
}

func (i *ServerlessDatabase) ToServerlessDatabaseOutputWithContext(ctx context.Context) ServerlessDatabaseOutput {
	return pulumi.ToOutputWithContext(ctx, i).(ServerlessDatabaseOutput)
}

// ServerlessDatabaseArrayInput is an input type that accepts ServerlessDatabaseArray and ServerlessDatabaseArrayOutput values.
// You can construct a concrete instance of `ServerlessDatabaseArrayInput` via:
//
//	ServerlessDatabaseArray{ ServerlessDatabaseArgs{...} }
type ServerlessDatabaseArrayInput interface {
	pulumi.Input

	ToServerlessDatabaseArrayOutput() ServerlessDatabaseArrayOutput
	ToServerlessDatabaseArrayOutputWithContext(context.Context) ServerlessDatabaseArrayOutput
}

type ServerlessDatabaseArray []ServerlessDatabaseInput

func (ServerlessDatabaseArray) ElementType() reflect.Type {
	return reflect.TypeOf((*[]*ServerlessDatabase)(nil)).Elem()
}

func (i ServerlessDatabaseArray) ToServerlessDatabaseArrayOutput() ServerlessDatabaseArrayOutput {
	return i.ToServerlessDatabaseArrayOutputWithContext(context.Background())
}

func (i ServerlessDatabaseArray) ToServerlessDatabaseArrayOutputWithContext(ctx context.Context) ServerlessDatabaseArrayOutput {
	return pulumi.ToOutputWithContext(ctx, i).(ServerlessDatabaseArrayOutput)
}

// ServerlessDatabaseMapInput is an input type that accepts ServerlessDatabaseMap and ServerlessDatabaseMapOutput values.
// You can construct a concrete instance of `ServerlessDatabaseMapInput` via:
//
//	ServerlessDatabaseMap{ "key": ServerlessDatabaseArgs{...} }
type ServerlessDatabaseMapInput interface {
	pulumi.Input

	ToServerlessDatabaseMapOutput() ServerlessDatabaseMapOutput
	ToServerlessDatabaseMapOutputWithContext(context.Context) ServerlessDatabaseMapOutput
}

type ServerlessDatabaseMap map[string]ServerlessDatabaseInput

func (ServerlessDatabaseMap) ElementType() reflect.Type {
	return reflect.TypeOf((*map[string]*ServerlessDatabase)(nil)).Elem()
}

func (i ServerlessDatabaseMap) ToServerlessDatabaseMapOutput() ServerlessDatabaseMapOutput {
	return i.ToServerlessDatabaseMapOutputWithContext(context.Background())
}

func (i ServerlessDatabaseMap) ToServerlessDatabaseMapOutputWithContext(ctx context.Context) ServerlessDatabaseMapOutput {
	return pulumi.ToOutputWithContext(ctx, i).(ServerlessDatabaseMapOutput)
}

type ServerlessDatabaseOutput struct{ *pulumi.OutputState }

func (ServerlessDatabaseOutput) ElementType() reflect.Type {
	return reflect.TypeOf((**ServerlessDatabase)(nil)).Elem()
}

func (o ServerlessDatabaseOutput) ToServerlessDatabaseOutput() ServerlessDatabaseOutput {
	return o
}

func (o ServerlessDatabaseOutput) ToServerlessDatabaseOutputWithContext(ctx context.Context) ServerlessDatabaseOutput {
	return o
}

type ServerlessDatabaseArrayOutput struct{ *pulumi.OutputState }

func (ServerlessDatabaseArrayOutput) ElementType() reflect.Type {
	return reflect.TypeOf((*[]*ServerlessDatabase)(nil)).Elem()
}

func (o ServerlessDatabaseArrayOutput) ToServerlessDatabaseArrayOutput() ServerlessDatabaseArrayOutput {
	return o
}

func (o ServerlessDatabaseArrayOutput) ToServerlessDatabaseArrayOutputWithContext(ctx context.Context) ServerlessDatabaseArrayOutput {
	return o
}

func (o ServerlessDatabaseArrayOutput) Index(i pulumi.IntInput) ServerlessDatabaseOutput {
	return pulumi.All(o, i).ApplyT(func(vs []interface{}) *ServerlessDatabase {
		return vs[0].([]*ServerlessDatabase)[vs[1].(int)]
	}).(ServerlessDatabaseOutput)
}

type ServerlessDatabaseMapOutput struct{ *pulumi.OutputState }

func (ServerlessDatabaseMapOutput) ElementType() reflect.Type {
	return reflect.TypeOf((*map[string]*ServerlessDatabase)(nil)).Elem()
}

func (o ServerlessDatabaseMapOutput) ToServerlessDatabaseMapOutput() ServerlessDatabaseMapOutput {
	return o
}

func (o ServerlessDatabaseMapOutput) ToServerlessDatabaseMapOutputWithContext(ctx context.Context) ServerlessDatabaseMapOutput {
	return o
}

func (o ServerlessDatabaseMapOutput) MapIndex(k pulumi.StringInput) ServerlessDatabaseOutput {
	return pulumi.All(o, k).ApplyT(func(vs []interface{}) *ServerlessDatabase {
		return vs[0].(map[string]*ServerlessDatabase)[vs[1].(string)]
	}).(ServerlessDatabaseOutput)
}

func init() {
	pulumi.RegisterInputType(reflect.TypeOf((*ServerlessDatabaseInput)(nil)).Elem(), &ServerlessDatabase{})
	pulumi.RegisterInputType(reflect.TypeOf((*ServerlessDatabaseArrayInput)(nil)).Elem(), ServerlessDatabaseArray{})
	pulumi.RegisterInputType(reflect.TypeOf((*ServerlessDatabaseMapInput)(nil)).Elem(), ServerlessDatabaseMap{})
	pulumi.RegisterOutputType(ServerlessDatabaseOutput{})
	pulumi.RegisterOutputType(ServerlessDatabaseArrayOutput{})
	pulumi.RegisterOutputType(ServerlessDatabaseMapOutput{})
}
