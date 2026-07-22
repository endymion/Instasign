import serial
import time
import sys

try:
    ser = serial.Serial('/dev/cu.usbmodem21101', 115200, timeout=1)
    ser.dtr = False
    ser.rts = False
    print("Connected to serial port, reading logs...")
    start = time.time()
    while time.time() - start < 10:
        line = ser.readline()
        if line:
            print(line.decode('utf-8', errors='replace').strip())
except Exception as e:
    print(e)
