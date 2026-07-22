import serial, time
try:
    with serial.Serial('/dev/cu.usbmodem1101', 115200, timeout=5) as s:
        start_time = time.time()
        while time.time() - start_time < 10:
            line = s.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(line)
except Exception as e:
    print(e)
