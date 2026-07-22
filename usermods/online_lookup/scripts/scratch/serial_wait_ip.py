import serial
import time
import sys

try:
    ser = serial.Serial('/dev/cu.usbmodem21101', 115200, timeout=1)
    ser.dtr = False
    ser.rts = False
    print("Waiting for IP...")
    
    start = time.time()
    while time.time() - start < 30:
        ser.write(b'{"v":true}\n')
        time.sleep(0.1)
        # Read all lines currently in buffer
        while ser.in_waiting:
            line = ser.readline().decode('utf-8', errors='replace').strip()
            if '"ip":"' in line and '"ip":""' not in line:
                print("FOUND IP!")
                print(line)
                sys.exit(0)
        time.sleep(2)
    print("No IP found within 30s")
except Exception as e:
    print(e)
