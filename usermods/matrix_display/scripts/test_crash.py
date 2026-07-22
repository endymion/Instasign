import serial
import sys
import glob
import time
import json

ports = glob.glob('/dev/cu.usbserial*') + glob.glob('/dev/cu.usbmodem*') + glob.glob('/dev/cu.wchusbserial*')
port = ports[0]
with serial.Serial(port, 115200, timeout=1) as ser:
    # Send payload
    payload = {"MatrixDisplay": {"type": "notification", "title": "TEST", "message": "Crash test.", "duration": 5000}}
    json_str = json.dumps(payload) + "\n"
    ser.write(json_str.encode('utf-8'))
    ser.flush()
    
    # Read output for 5 seconds to catch stack trace
    start = time.time()
    while time.time() - start < 5:
        line = ser.readline()
        if line:
            print(line.decode('utf-8', errors='ignore').strip())
