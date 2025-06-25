// @ts-nocheck
import { BedrockChatParametersInput } from "./lib/utils/parameter-models";

export const bedrockChatParams = new Map<string, BedrockChatParametersInput>();
// You can define multiple environments and their parameters here
bedrockChatParams.set("dev", {
  enableRagReplicas: false,
  enableBotStore: false,
  enableBotStoreReplicas: false,
});

// If you define "default" environment here, parameters in cdk.json are ignored
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["0.0.0.0/1", "128.0.0.0/1"],
  allowedIpV6AddressRanges: [
    "0000:0000:0000:0000:0000:0000:0000:0000/1",
    "8000:0000:0000:0000:0000:0000:0000:0000/1",
  ],
  identityProviders: [],
  userPoolDomainPrefix: "",
  allowedSignUpEmailDomains: [],
  autoJoinUserGroups: ["CreatingBotAllowed"],
  selfSignUpEnabled: false,
  publishedApiAllowedIpV4AddressRanges: ["0.0.0.0/1", "128.0.0.0/1"],
  publishedApiAllowedIpV6AddressRanges: [
    "0000:0000:0000:0000:0000:0000:0000:0000/1",
    "8000:0000:0000:0000:0000:0000:0000:0000/1",
  ],
  enableRagReplicas: false,
  enableBedrockCrossRegionInference: true,
  enableLambdaSnapStart: true,
  enableBotStore: false,
  enableBotStoreReplicas: false,
  botStoreLanguage: "en",
  tokenValidMinutes: 30,
  alternateDomainName: "",
  hostedZoneId: "",
  devAccessIamRoleArn: "",
});
