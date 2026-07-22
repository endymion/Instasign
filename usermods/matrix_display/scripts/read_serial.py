import serial
import sys
import glob

ports = glob.glob('/dev/cu.usbserial*') + glob.glob('/dev/cu.usbmodem*') + glob.glob('/dev/cu.wchusbserial*')
if not ports:
    print("No serial ports found")
    sys.exit(1)

port = ports[0]
print(f"Reading from {port}")
try:
    with serial.Serial(port, 115200, timeout=2) as ser:
        for _ in range(20):
            line = ser.readline()
            if line:
                print(line.decode('utf-8', errors='ignore').strip())
except Exception as e:
    print(f"Error: {e}")
