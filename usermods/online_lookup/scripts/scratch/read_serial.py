import serial
import time
import sys

try:
    ser = serial.Serial('/dev/cu.usbmodem21101', 115200, timeout=1)
    print("Connected to serial port")
    start = time.time()
    while time.time() - start < 5:
        line = ser.readline()
        if line:
            print(line.decode('utf-8', errors='replace').strip())
except Exception as e:
    print(e)
