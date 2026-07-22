import serial
import json
import time

port = "/dev/cu.usbmodem21101"
baudrate = 115200

# JSON payload to set up HUB75 Matrix (Type 65) with 4096 LEDs, and 2D matrix 64x64
payload = {
  "hw": {
    "led": {
      "total": 4096,
      "maxpwr": 2000,
      "ledma": 20,
      "ins": [
        {"start": 0, "len": 4096, "pin": [-1], "type": 65, "color": {"order": 0}, "skip": 0}
      ]
    }
  }
}

try:
    with serial.Serial(port, baudrate, timeout=1) as ser:
        print(f"Connected to {port}. Waiting 2s...")
        time.sleep(2) # Wait for device to reset/ready
        
        json_str = json.dumps(payload) + "\n"
        print(f"Sending: {json_str}")
        ser.write(json_str.encode('utf-8'))
        time.sleep(1)
        
        while ser.in_waiting:
            print(ser.readline().decode('utf-8', errors='ignore').strip())
            
except Exception as e:
    print(f"Error: {e}")
