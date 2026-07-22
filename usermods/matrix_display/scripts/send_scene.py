#!/usr/bin/env python3
"""Send a MatrixDisplay scene over USB serial (works without WiFi/MQTT)."""

from __future__ import annotations

import argparse
import glob
import json
import sys
import time

try:
    import serial
except ImportError:
    print("Install pyserial: pip install pyserial", file=sys.stderr)
    sys.exit(1)


def find_port() -> str:
    ports = sorted(
        glob.glob("/dev/cu.usbmodem*")
        + glob.glob("/dev/cu.usbserial*")
        + glob.glob("/dev/cu.wchusbserial*")
    )
    if not ports:
        raise SystemExit("No USB serial device found.")
    return ports[0]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--port", help="Serial port (default: auto-detect)")
    p.add_argument("--title", default="TEST")
    p.add_argument("--message", default="serial demo")
    p.add_argument("--icon", default="bell")
    p.add_argument("--icon-size", type=int, default=15)
    p.add_argument("--title-font", default="Jersey 15")
    p.add_argument("--message-font", default="bytesized")
    p.add_argument("--duration", type=int, default=20000)
    p.add_argument("--mqtt-server", help="Retarget MQTT broker (optional)")
    p.add_argument("--mqtt-port", type=int, default=1883)
    p.add_argument("--mqtt-topic", default="wled/matrix/scene")
    p.add_argument("--json", help="Raw MatrixDisplay JSON object (overrides flags)")
    p.add_argument("--config-only", action="store_true", help="Only update MQTT config")
    args = p.parse_args()

    if args.json:
        matrix = json.loads(args.json)
    elif args.config_only:
        matrix = {"type": "config"}
    else:
        matrix = {
            "type": "notification",
            "title": args.title,
            "message": args.message,
            "titleFont": args.title_font,
            "messageFont": args.message_font,
            "icon": args.icon,
            "iconSize": args.icon_size,
            "duration": args.duration,
        }

    if args.mqtt_server:
        matrix["mqttServer"] = args.mqtt_server
        matrix["mqttPort"] = args.mqtt_port
        matrix["mqttTopic"] = args.mqtt_topic

    port = args.port or find_port()
    payload = json.dumps({"MatrixDisplay": matrix}) + "\n"
    print(f"Port: {port}")
    print(f"Send: {payload.strip()}")

    with serial.Serial(port, 115200, timeout=0.5) as ser:
        time.sleep(0.2)
        ser.reset_input_buffer()
        ser.write(payload.encode("utf-8"))
        end = time.time() + 2.5
        while time.time() < end:
            line = ser.readline()
            if not line:
                continue
            text = line.decode("utf-8", "ignore").rstrip()
            if "UsermodMatrixDisplay" in text or text.startswith("{"):
                print(text)


if __name__ == "__main__":
    main()
