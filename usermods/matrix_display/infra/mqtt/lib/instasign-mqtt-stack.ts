import * as cdk from "aws-cdk-lib";
import * as iot from "aws-cdk-lib/aws-iot";
import * as cr from "aws-cdk-lib/custom-resources";
import { Construct } from "constructs";

export const SCENE_TOPIC = "wled/matrix/scene";
export const MATRIX_THING = "instasign-matrix";
export const PUBLISHER_THING = "instasign-publisher";

export class InstasignMqttStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const account = cdk.Stack.of(this).account;
    const region = cdk.Stack.of(this).region;

    const matrixThing = new iot.CfnThing(this, "MatrixThing", {
      thingName: MATRIX_THING,
      attributePayload: {
        attributes: { role: "display", project: "instasign" },
      },
    });

    const publisherThing = new iot.CfnThing(this, "PublisherThing", {
      thingName: PUBLISHER_THING,
      attributePayload: {
        attributes: { role: "publisher", project: "instasign" },
      },
    });

    // ClientId must match Thing name for Connect.
    const matrixPolicyDoc = {
      Version: "2012-10-17",
      Statement: [
        {
          Effect: "Allow",
          Action: ["iot:Connect"],
          Resource: [`arn:aws:iot:${region}:${account}:client/${MATRIX_THING}`],
        },
        {
          Effect: "Allow",
          Action: ["iot:Subscribe"],
          Resource: [
            `arn:aws:iot:${region}:${account}:topicfilter/${SCENE_TOPIC}`,
          ],
        },
        {
          Effect: "Allow",
          Action: ["iot:Receive"],
          Resource: [`arn:aws:iot:${region}:${account}:topic/${SCENE_TOPIC}`],
        },
      ],
    };

    const publisherPolicyDoc = {
      Version: "2012-10-17",
      Statement: [
        {
          Effect: "Allow",
          Action: ["iot:Connect"],
          Resource: [
            `arn:aws:iot:${region}:${account}:client/${PUBLISHER_THING}`,
          ],
        },
        {
          Effect: "Allow",
          Action: ["iot:Publish"],
          Resource: [`arn:aws:iot:${region}:${account}:topic/${SCENE_TOPIC}`],
        },
      ],
    };

    const matrixPolicy = new iot.CfnPolicy(this, "MatrixPolicy", {
      policyName: "instasign-matrix-policy",
      policyDocument: matrixPolicyDoc,
    });

    const publisherPolicy = new iot.CfnPolicy(this, "PublisherPolicy", {
      policyName: "instasign-publisher-policy",
      policyDocument: publisherPolicyDoc,
    });

    // Account-specific ATS MQTT endpoint.
    const endpoint = new cr.AwsCustomResource(this, "IotDataEndpoint", {
      onUpdate: {
        service: "Iot",
        action: "describeEndpoint",
        parameters: { endpointType: "iot:Data-ATS" },
        physicalResourceId: cr.PhysicalResourceId.of("InstasignIotDataAts"),
      },
      policy: cr.AwsCustomResourcePolicy.fromSdkCalls({
        resources: cr.AwsCustomResourcePolicy.ANY_RESOURCE,
      }),
    });

    new cdk.CfnOutput(this, "IotEndpoint", {
      value: endpoint.getResponseField("endpointAddress"),
      description: "AWS IoT Core ATS MQTT endpoint (port 8883)",
      exportName: "InstasignMqttEndpoint",
    });

    new cdk.CfnOutput(this, "SceneTopic", {
      value: SCENE_TOPIC,
      exportName: "InstasignSceneTopic",
    });

    new cdk.CfnOutput(this, "MatrixThingName", {
      value: matrixThing.thingName!,
      exportName: "InstasignMatrixThing",
    });

    new cdk.CfnOutput(this, "PublisherThingName", {
      value: publisherThing.thingName!,
      exportName: "InstasignPublisherThing",
    });

    new cdk.CfnOutput(this, "MatrixPolicyName", {
      value: matrixPolicy.policyName!,
      exportName: "InstasignMatrixPolicy",
    });

    new cdk.CfnOutput(this, "PublisherPolicyName", {
      value: publisherPolicy.policyName!,
      exportName: "InstasignPublisherPolicy",
    });

    // Ensure policies exist before cert provisioning script runs.
    matrixThing.node.addDependency(matrixPolicy);
    publisherThing.node.addDependency(publisherPolicy);
  }
}
