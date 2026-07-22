#!/usr/bin/env node
/**
 * Publish a demo scene to Instasign MQTT using publisher certs + mosquitto_pub.
 */
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CERTS = path.resolve(__dirname, "../certs");

const payload = {
  type: "warning",
  title: "WARNING",
  message: "Instasign cloud MQTT OK",
  duration: 20000,
};

async function main() {
  const endpoint = (await readFile(path.join(CERTS, "endpoint.txt"), "utf8")).trim();
  const topic = (await readFile(path.join(CERTS, "topic.txt"), "utf8")).trim();
  const ca = path.join(CERTS, "AmazonRootCA1.pem");
  const cert = path.join(CERTS, "publisher", "certificate.pem.crt");
  const key = path.join(CERTS, "publisher", "private.pem.key");

  const args = [
    "-h",
    endpoint,
    "-p",
    "8883",
    "--cafile",
    ca,
    "--cert",
    cert,
    "--key",
    key,
    "-i",
    "instasign-publisher",
    "-t",
    topic,
    "-m",
    JSON.stringify(payload),
  ];

  console.log("mosquitto_pub", args.join(" "));
  const res = spawnSync("mosquitto_pub", args, { stdio: "inherit" });
  process.exit(res.status ?? 1);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
