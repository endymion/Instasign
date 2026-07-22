import requests
import sys

ip = "192.168.1.112"
firmware_path = ".pio/build/esp32c3dev/firmware.bin"

print(f"Uploading {firmware_path} to {ip}...")
try:
    with open(firmware_path, 'rb') as f:
        files = {'update': f}
        r = requests.post(f"http://{ip}/update", files=files, timeout=30)
    print("Upload complete!")
    print("Status code:", r.status_code)
except requests.exceptions.Timeout:
    print("Upload timed out - this usually means it succeeded and the device is rebooting.")
except Exception as e:
    print("Error:", e)
