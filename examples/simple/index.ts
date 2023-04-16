import * as nuage from "@pulumi/nuage";

const random = new nuage.Random("my-random", { length: 24 });

export const output = random.result;