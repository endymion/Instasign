import serial
import time
import sys

try:
    ser = serial.Serial('/dev/cu.usbmodem21101', 115200, timeout=2)
    ser.dtr = False
    ser.rts = False
    
    # Wait for Wi-Fi to connect
    time.sleep(5)
    
    # Send JSON status request
    ser.write(b'{"v":true}\n')
    
    # Read response
    start = time.time()
    while time.time() - start < 3:
        line = ser.readline()
        if line:
            print(line.decode('utf-8', errors='replace').strip())
except Exception as e:
    print(e)
