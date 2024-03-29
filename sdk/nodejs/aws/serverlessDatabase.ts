// *** WARNING: this file was generated by Pulumi SDK Generator. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

import * as pulumi from "@pulumi/pulumi";
import { input as inputs, output as outputs, enums } from "../types";
import * as utilities from "../utilities";

/**
 * The ServerlessDatabase component is a convenient and efficient solution for creating serverless databases using Amazon RDS Aurora. It automatically creates components such as subnet group, security group, security group rules, and RDS cluster, and securely manages the DB credentials. With support for both MySQL and PostgreSQL, it provides a fully configured serverless database resource for your serverless database needs.
 *
 * ## Example Usage
 */
export class ServerlessDatabase extends pulumi.ComponentResource {
    /** @internal */
    public static readonly __pulumiType = 'nuage:aws:ServerlessDatabase';

    /**
     * Returns true if the given object is an instance of ServerlessDatabase.  This is designed to work even
     * when multiple copies of the Pulumi SDK have been loaded into the same process.
     */
    public static isInstance(obj: any): obj is ServerlessDatabase {
        if (obj === undefined || obj === null) {
            return false;
        }
        return obj['__pulumiType'] === ServerlessDatabase.__pulumiType;
    }

    /**
     * IP address of the bastion host. Exists only if bastion is enabled
     */
    public /*out*/ readonly bastion_ip!: pulumi.Output<string | undefined>;
    /**
     * Private key to connect bastion host over SSH. Exists only if bastion is enabled.
     */
    public /*out*/ readonly bastion_private_key!: pulumi.Output<string | undefined>;
    /**
     * ARN (Amazon Resource Name) of the RDS cluster.
     */
    public /*out*/ readonly cluster_arn!: pulumi.Output<string>;
    /**
     * Name of the database
     */
    public /*out*/ readonly database_name!: pulumi.Output<string>;
    /**
     * Host address of DB server
     */
    public /*out*/ readonly host!: pulumi.Output<string>;
    /**
     * Password of DB credentials
     */
    public /*out*/ readonly password!: pulumi.Output<string | undefined>;
    /**
     * Port number of DB
     */
    public /*out*/ readonly port!: pulumi.Output<number>;
    /**
     * Database URI for connection.
     */
    public /*out*/ readonly uri!: pulumi.Output<string>;
    /**
     * Username of DB credentials.
     */
    public /*out*/ readonly user!: pulumi.Output<string>;

    /**
     * Create a ServerlessDatabase resource with the given unique name, arguments, and options.
     *
     * @param name The _unique_ name of the resource.
     * @param args The arguments to use to populate this resource's properties.
     * @param opts A bag of options that control this resource's behavior.
     */
    constructor(name: string, args: ServerlessDatabaseArgs, opts?: pulumi.ComponentResourceOptions) {
        let resourceInputs: pulumi.Inputs = {};
        opts = opts || {};
        if (!opts.id) {
            if ((!args || args.databaseName === undefined) && !opts.urn) {
                throw new Error("Missing required property 'databaseName'");
            }
            if ((!args || args.databaseType === undefined) && !opts.urn) {
                throw new Error("Missing required property 'databaseType'");
            }
            if ((!args || args.masterUserName === undefined) && !opts.urn) {
                throw new Error("Missing required property 'masterUserName'");
            }
            if ((!args || args.subnetIds === undefined) && !opts.urn) {
                throw new Error("Missing required property 'subnetIds'");
            }
            if ((!args || args.vpcId === undefined) && !opts.urn) {
                throw new Error("Missing required property 'vpcId'");
            }
            resourceInputs["bastion"] = args ? args.bastion : undefined;
            resourceInputs["databaseName"] = args ? args.databaseName : undefined;
            resourceInputs["databaseType"] = args ? args.databaseType : undefined;
            resourceInputs["ipWhitelist"] = args ? args.ipWhitelist : undefined;
            resourceInputs["masterUserName"] = args ? args.masterUserName : undefined;
            resourceInputs["skipFinalSnapshot"] = args ? args.skipFinalSnapshot : undefined;
            resourceInputs["subnetIds"] = args ? args.subnetIds : undefined;
            resourceInputs["vpcId"] = args ? args.vpcId : undefined;
            resourceInputs["bastion_ip"] = undefined /*out*/;
            resourceInputs["bastion_private_key"] = undefined /*out*/;
            resourceInputs["cluster_arn"] = undefined /*out*/;
            resourceInputs["database_name"] = undefined /*out*/;
            resourceInputs["host"] = undefined /*out*/;
            resourceInputs["password"] = undefined /*out*/;
            resourceInputs["port"] = undefined /*out*/;
            resourceInputs["uri"] = undefined /*out*/;
            resourceInputs["user"] = undefined /*out*/;
        } else {
            resourceInputs["bastion_ip"] = undefined /*out*/;
            resourceInputs["bastion_private_key"] = undefined /*out*/;
            resourceInputs["cluster_arn"] = undefined /*out*/;
            resourceInputs["database_name"] = undefined /*out*/;
            resourceInputs["host"] = undefined /*out*/;
            resourceInputs["password"] = undefined /*out*/;
            resourceInputs["port"] = undefined /*out*/;
            resourceInputs["uri"] = undefined /*out*/;
            resourceInputs["user"] = undefined /*out*/;
        }
        opts = pulumi.mergeOptions(utilities.resourceOptsDefaults(), opts);
        super(ServerlessDatabase.__pulumiType, name, resourceInputs, opts, true /*remote*/);
    }
}

/**
 * The set of arguments for constructing a ServerlessDatabase resource.
 */
export interface ServerlessDatabaseArgs {
    /**
     * Configure the bastion host for connecting the db.
     */
    bastion?: pulumi.Input<inputs.aws.BastionConfigArgs>;
    /**
     * Name of the database.
     */
    databaseName: pulumi.Input<string>;
    /**
     * Database type. `mysql` or `postgresql`
     */
    databaseType: pulumi.Input<string>;
    /**
     * List of whitelisted IP addresses. If not specified, it will be public 0.0.0.0/0
     */
    ipWhitelist?: pulumi.Input<pulumi.Input<string>[]>;
    /**
     * Master user name of the db.
     */
    masterUserName: pulumi.Input<string>;
    /**
     * Determines whether a final DB snapshot is created before the DB instance is deleted. Defaults to `false`
     */
    skipFinalSnapshot?: pulumi.Input<boolean>;
    /**
     * List of subnet ip addresses. If you want your database will be accessible from the internet, it should be public (`vpc.public_subnet_ids`). Otherwise, you can use private subnets (`vpc.private_subnet_ids`).
     */
    subnetIds: pulumi.Input<pulumi.Input<string>[]>;
    /**
     * Vpc id.
     */
    vpcId: pulumi.Input<string>;
}
