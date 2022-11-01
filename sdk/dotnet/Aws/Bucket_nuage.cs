// *** WARNING: this file was generated by Pulumi SDK Generator. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Pulumi.Serialization;

namespace Pulumi.Nuage.Aws
{
    [NuageResourceType("nuage:aws:bucket_nuage")]
    public partial class Bucket_nuage : Pulumi.ComponentResource
    {
        /// <summary>
        /// The bucket resource.
        /// </summary>
        [Output("bucket")]
        public Output<Pulumi.Aws.S3.Bucket> Bucket { get; private set; } = null!;


        /// <summary>
        /// Create a Bucket_nuage resource with the given unique name, arguments, and options.
        /// </summary>
        ///
        /// <param name="name">The unique name of the resource</param>
        /// <param name="args">The arguments used to populate this resource's properties</param>
        /// <param name="options">A bag of options that control this resource's behavior</param>
        public Bucket_nuage(string name, Bucket_nuageArgs? args = null, ComponentResourceOptions? options = null)
            : base("nuage:aws:bucket_nuage", name, args ?? new Bucket_nuageArgs(), MakeResourceOptions(options, ""), remote: true)
        {
        }

        private static ComponentResourceOptions MakeResourceOptions(ComponentResourceOptions? options, Input<string>? id)
        {
            var defaultOptions = new ComponentResourceOptions
            {
                Version = Utilities.Version,
            };
            var merged = ComponentResourceOptions.Merge(defaultOptions, options);
            // Override the ID if one was specified for consistency with other language SDKs.
            merged.Id = id ?? merged.Id;
            return merged;
        }
    }

    public sealed class Bucket_nuageArgs : Pulumi.ResourceArgs
    {
        public Bucket_nuageArgs()
        {
        }
    }
}