import serial
import json
import time

port = "/dev/cu.usbmodem21101"
baudrate = 115200

try:
    with serial.Serial(port, baudrate, timeout=1) as ser:
        print(f"Connected to {port}. Waiting 2s...")
        time.sleep(2) # Wait for device to reset/ready
        
        # Send a request for config
        ser.write(b'{"v":true}\n')
        time.sleep(1)
        
        while ser.in_waiting:
            print(ser.readline().decode('utf-8', errors='ignore').strip())
            
except Exception as e:
    print(f"Error: {e}")
