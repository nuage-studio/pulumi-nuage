import * as pulumi from "@pulumi/pulumi";
import * as pulumiAws from "@pulumi/aws";
export declare class Bucket_nuage extends pulumi.ComponentResource {
    /**
     * Returns true if the given object is an instance of Bucket_nuage.  This is designed to work even
     * when multiple copies of the Pulumi SDK have been loaded into the same process.
     */
    static isInstance(obj: any): obj is Bucket_nuage;
    /**
     * The bucket resource.
     */
    readonly bucket: pulumi.Output<pulumiAws.s3.Bucket>;
    /**
     * Create a Bucket_nuage resource with the given unique name, arguments, and options.
     *
     * @param name The _unique_ name of the resource.
     * @param args The arguments to use to populate this resource's properties.
     * @param opts A bag of options that control this resource's behavior.
     */
    constructor(name: string, args?: Bucket_nuageArgs, opts?: pulumi.ComponentResourceOptions);
}
/**
 * The set of arguments for constructing a Bucket_nuage resource.
 */
export interface Bucket_nuageArgs {
}
