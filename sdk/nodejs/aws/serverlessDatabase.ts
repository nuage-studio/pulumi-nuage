// *** WARNING: this file was generated by Pulumi SDK Generator. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

import * as pulumi from "@pulumi/pulumi";
import * as utilities from "../utilities";

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

    public /*out*/ readonly cluster_arn!: pulumi.Output<string>;
    public /*out*/ readonly host!: pulumi.Output<string>;
    public /*out*/ readonly name!: pulumi.Output<string>;
    public /*out*/ readonly password!: pulumi.Output<string | undefined>;
    public /*out*/ readonly policy_document!: pulumi.Output<string | undefined>;
    public /*out*/ readonly port!: pulumi.Output<number>;
    public /*out*/ readonly uri!: pulumi.Output<string>;
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
            if ((!args || args.databaseType === undefined) && !opts.urn) {
                throw new Error("Missing required property 'databaseType'");
            }
            if ((!args || args.resourceName === undefined) && !opts.urn) {
                throw new Error("Missing required property 'resourceName'");
            }
            if ((!args || args.vpcId === undefined) && !opts.urn) {
                throw new Error("Missing required property 'vpcId'");
            }
            if ((!args || args.vpcSubnets === undefined) && !opts.urn) {
                throw new Error("Missing required property 'vpcSubnets'");
            }
            resourceInputs["dataApi"] = args ? args.dataApi : undefined;
            resourceInputs["databaseName"] = args ? args.databaseName : undefined;
            resourceInputs["databaseType"] = args ? args.databaseType : undefined;
            resourceInputs["ipWhitelist"] = args ? args.ipWhitelist : undefined;
            resourceInputs["masterUserName"] = args ? args.masterUserName : undefined;
            resourceInputs["resourceName"] = args ? args.resourceName : undefined;
            resourceInputs["s3Extension"] = args ? args.s3Extension : undefined;
            resourceInputs["skipFinalSnapshot"] = args ? args.skipFinalSnapshot : undefined;
            resourceInputs["vpcId"] = args ? args.vpcId : undefined;
            resourceInputs["vpcSubnets"] = args ? args.vpcSubnets : undefined;
            resourceInputs["cluster_arn"] = undefined /*out*/;
            resourceInputs["host"] = undefined /*out*/;
            resourceInputs["name"] = undefined /*out*/;
            resourceInputs["password"] = undefined /*out*/;
            resourceInputs["policy_document"] = undefined /*out*/;
            resourceInputs["port"] = undefined /*out*/;
            resourceInputs["uri"] = undefined /*out*/;
            resourceInputs["user"] = undefined /*out*/;
        } else {
            resourceInputs["cluster_arn"] = undefined /*out*/;
            resourceInputs["host"] = undefined /*out*/;
            resourceInputs["name"] = undefined /*out*/;
            resourceInputs["password"] = undefined /*out*/;
            resourceInputs["policy_document"] = undefined /*out*/;
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
     * Enable data api. Defaults to `false`
     */
    dataApi?: pulumi.Input<boolean>;
    /**
     * Name of the database.
     */
    databaseName?: pulumi.Input<string>;
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
    masterUserName?: pulumi.Input<string>;
    /**
     * Resource name.
     */
    resourceName: pulumi.Input<string>;
    /**
     * Enable s3 extension. Defaults to `false`
     */
    s3Extension?: pulumi.Input<boolean>;
    /**
     * Determines whether a final DB snapshot is created before the DB instance is deleted. Defaults to `false`
     */
    skipFinalSnapshot?: pulumi.Input<boolean>;
    /**
     * Vpc id.
     */
    vpcId: pulumi.Input<string>;
    /**
     * List of subnet ip addresses.
     */
    vpcSubnets: pulumi.Input<pulumi.Input<string>[]>;
}
