#!/usr/bin/env node
/**
 * Create (or reuse) IoT certs for Instasign matrix + publisher Things,
 * attach policies, write PEM files under certs/, generate firmware secrets.
 */
import {
  IoTClient,
  CreateKeysAndCertificateCommand,
  AttachPolicyCommand,
  AttachThingPrincipalCommand,
  ListThingPrincipalsCommand,
  DescribeCertificateCommand,
  DescribeEndpointCommand,
  ListCertificatesCommand,
} from "@aws-sdk/client-iot";
import {
  CloudFormationClient,
  DescribeStacksCommand,
} from "@aws-sdk/client-cloudformation";
import { mkdir, writeFile, readFile, access } from "node:fs/promises";
import { constants as fsConstants } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const CERTS = path.join(ROOT, "certs");
const STACK = "InstasignMqttStack";

const MATRIX_THING = "instasign-matrix";
const PUBLISHER_THING = "instasign-publisher";
const MATRIX_POLICY = "instasign-matrix-policy";
const PUBLISHER_POLICY = "instasign-publisher-policy";
const AMAZON_ROOT_CA_URL =
  "https://www.amazontrust.com/repository/AmazonRootCA1.pem";

const iot = new IoTClient({});
const cfn = new CloudFormationClient({});

async function exists(p) {
  try {
    await access(p, fsConstants.F_OK);
    return true;
  } catch {
    return false;
  }
}

async function stackOutputs() {
  const res = await cfn.send(
    new DescribeStacksCommand({ StackName: STACK }),
  );
  const outs = res.Stacks?.[0]?.Outputs ?? [];
  const map = Object.fromEntries(outs.map((o) => [o.OutputKey, o.OutputValue]));
  return map;
}

async function ensureRootCa() {
  const dest = path.join(CERTS, "AmazonRootCA1.pem");
  if (await exists(dest)) return dest;
  const res = await fetch(AMAZON_ROOT_CA_URL);
  if (!res.ok) throw new Error(`Failed to download Amazon Root CA: ${res.status}`);
  await writeFile(dest, await res.text(), "utf8");
  console.log("Wrote", dest);
  return dest;
}

async function provisionRole(role) {
  const dir = path.join(CERTS, role.name);
  await mkdir(dir, { recursive: true });
  const marker = path.join(dir, "certificateArn.txt");
  const keyPath = path.join(dir, "private.pem.key");
  const certPath = path.join(dir, "certificate.pem.crt");

  if ((await exists(marker)) && (await exists(keyPath)) && (await exists(certPath))) {
    const arn = (await readFile(marker, "utf8")).trim();
    console.log(`[${role.name}] Reusing existing cert ${arn}`);
    // Ensure attachments (idempotent-ish: ignore already-attached errors).
    await attachAll(role, arn);
    return { arn, keyPath, certPath };
  }

  // If thing already has a principal but local files are missing, we must create new certs
  // (private key is only returned once). Detach old principals is out of scope; create fresh.
  const created = await iot.send(
    new CreateKeysAndCertificateCommand({ setAsActive: true }),
  );
  if (!created.certificateArn || !created.certificatePem || !created.keyPair?.PrivateKey) {
    throw new Error(`CreateKeysAndCertificate incomplete for ${role.name}`);
  }

  await writeFile(certPath, created.certificatePem, "utf8");
  await writeFile(keyPath, created.keyPair.PrivateKey, "utf8");
  await writeFile(marker, created.certificateArn + "\n", "utf8");
  if (created.certificateId) {
    await writeFile(path.join(dir, "certificateId.txt"), created.certificateId + "\n", "utf8");
  }

  await attachAll(role, created.certificateArn);
  console.log(`[${role.name}] Created and attached ${created.certificateArn}`);
  return { arn: created.certificateArn, keyPath, certPath };
}

async function attachAll(role, certificateArn) {
  try {
    await iot.send(
      new AttachPolicyCommand({
        policyName: role.policy,
        target: certificateArn,
      }),
    );
  } catch (e) {
    if (!String(e.name || e).includes("ResourceAlreadyExists")) {
      // AttachPolicy throws if already attached on some SDKs — continue if so.
      const msg = String(e.message || e);
      if (!msg.includes("already")) throw e;
    }
  }

  try {
    await iot.send(
      new AttachThingPrincipalCommand({
        thingName: role.thing,
        principal: certificateArn,
      }),
    );
  } catch (e) {
    const msg = String(e.message || e);
    if (!msg.includes("already")) throw e;
  }
}

async function main() {
  await mkdir(CERTS, { recursive: true });

  const outputs = await stackOutputs();
  const endpoint =
    outputs.IotEndpoint ||
    (
      await iot.send(
        new DescribeEndpointCommand({ endpointType: "iot:Data-ATS" }),
      )
    ).endpointAddress;

  if (!endpoint) throw new Error("Could not resolve IoT ATS endpoint");

  await writeFile(path.join(CERTS, "endpoint.txt"), endpoint + "\n", "utf8");
  await writeFile(path.join(CERTS, "topic.txt"), "wled/matrix/scene\n", "utf8");
  await ensureRootCa();

  await provisionRole({
    name: "matrix",
    thing: MATRIX_THING,
    policy: MATRIX_POLICY,
  });
  await provisionRole({
    name: "publisher",
    thing: PUBLISHER_THING,
    policy: PUBLISHER_POLICY,
  });

  // Generate firmware secrets header.
  const gen = spawnSync("node", [path.join(__dirname, "generate-firmware-secrets.mjs")], {
    stdio: "inherit",
    cwd: ROOT,
  });
  if (gen.status !== 0) process.exit(gen.status ?? 1);

  console.log("\nInstasign MQTT ready.");
  console.log("  Endpoint:", endpoint);
  console.log("  Topic:   wled/matrix/scene");
  console.log("  Certs:  ", CERTS);
  console.log("\nPublish demo:");
  console.log("  npm run publish-demo");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
