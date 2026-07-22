import serial, time
try:
    with serial.Serial('/dev/cu.usbmodem1101', 115200, timeout=2) as s:
        print(s.read(1000).decode('utf-8', errors='ignore'))
except Exception as e:
    print(e)
