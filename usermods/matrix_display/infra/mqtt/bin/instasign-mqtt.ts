#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { InstasignMqttStack } from "../lib/instasign-mqtt-stack";

const app = new cdk.App();

new InstasignMqttStack(app, "InstasignMqttStack", {
  description: "Instasign matrix display MQTT broker (AWS IoT Core)",
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION ?? "us-east-1",
  },
});
