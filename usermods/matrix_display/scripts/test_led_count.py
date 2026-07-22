import serial
import time
import sys

port = '/dev/cu.usbmodem21101'
baudrate = 115200

try:
    ser = serial.Serial(port, baudrate, timeout=1)
    
    print(f"Connected to {port}. Reading serial output...", file=sys.stderr)
    for _ in range(500):
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            print(line)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
