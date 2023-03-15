// *** WARNING: this file was generated by Pulumi SDK Generator. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***

import * as pulumi from "@pulumi/pulumi";
import * as utilities from "../utilities";

// Export members:
export * from "./bastion";
export * from "./containerFunction";
export * from "./image";
export * from "./repository";
export * from "./serverlessDatabase";

// Export enums:
export * from "../types/enums/aws";

// Import resources to register:
import { Bastion } from "./bastion";
import { ContainerFunction } from "./containerFunction";
import { Image } from "./image";
import { Repository } from "./repository";
import { ServerlessDatabase } from "./serverlessDatabase";

const _module = {
    version: utilities.getVersion(),
    construct: (name: string, type: string, urn: string): pulumi.Resource => {
        switch (type) {
            case "nuage:aws:Bastion":
                return new Bastion(name, <any>undefined, { urn })
            case "nuage:aws:ContainerFunction":
                return new ContainerFunction(name, <any>undefined, { urn })
            case "nuage:aws:Image":
                return new Image(name, <any>undefined, { urn })
            case "nuage:aws:Repository":
                return new Repository(name, <any>undefined, { urn })
            case "nuage:aws:ServerlessDatabase":
                return new ServerlessDatabase(name, <any>undefined, { urn })
            default:
                throw new Error(`unknown resource type ${type}`);
        }
    },
};
pulumi.runtime.registerResourceModule("nuage", "aws", _module)
