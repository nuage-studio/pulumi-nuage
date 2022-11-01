// *** WARNING: this file was generated by Pulumi SDK Generator. ***
// *** Do not edit by hand unless you're certain you know what you are doing! ***


export const ArchitectureType = {
    /**
     * X86_64 architecture.
     */
    X86_64: "X86_64",
    /**
     * ARM64 architecture.
     */
    ARM64: "ARM64",
} as const;

/**
 * Architecture, either 'X86_64' or 'arm64'.
 */
export type ArchitectureType = (typeof ArchitectureType)[keyof typeof ArchitectureType];