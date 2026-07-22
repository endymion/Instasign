import serial
import sys
import glob

ports = glob.glob('/dev/cu.usbserial*') + glob.glob('/dev/cu.usbmodem*') + glob.glob('/dev/cu.wchusbserial*')
port = ports[0]
with serial.Serial(port, 115200, timeout=1) as ser:
    for _ in range(10):
        line = ser.readline()
        if line:
            print(line.decode('utf-8', errors='ignore').strip())
