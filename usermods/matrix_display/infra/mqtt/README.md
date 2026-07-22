# Instasign MQTT (AWS IoT Core)

CDK stack: **`InstasignMqttStack`**

Provides a managed MQTT broker endpoint for the Instasign matrix display.

## Deploy

```bash
cd infra/mqtt
npm install
npx cdk bootstrap   # once per account/region
npm run deploy      # cdk deploy + provision certs + generate firmware secrets
```

## Outputs

- ATS endpoint → `certs/endpoint.txt`
- Board certs → `certs/matrix/`
- Publisher certs → `certs/publisher/`
- Firmware header → `wled/usermods/matrix_display/secrets/mqtt_iot_secrets.h` (gitignored)

## Publish a scene

```bash
npm run publish-demo
```

Or manually:

```bash
mosquitto_pub -h "$(cat certs/endpoint.txt)" -p 8883 \
  --cafile certs/AmazonRootCA1.pem \
  --cert certs/publisher/certificate.pem.crt \
  --key certs/publisher/private.pem.key \
  -i instasign-publisher \
  -t wled/matrix/scene \
  -m '{"type":"warning","title":"WARNING","message":"hello","duration":15000}'
```
