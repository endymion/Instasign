import serial
import time
import sys

def read_boot():
    port = '/dev/cu.usbmodem21101'
    baudrate = 115200
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to {port}. Resetting board...")
        
        # Reset the board
        ser.setDTR(False)
        ser.setRTS(True)
        time.sleep(0.1)
        ser.setDTR(False)
        ser.setRTS(False)
        
        print("Reading serial output...")
        
        start_time = time.time()
        timeout = 20  # Read for 20 seconds
        
        while time.time() - start_time < timeout:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print(line)
                    sys.stdout.flush()
            else:
                time.sleep(0.1)
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    read_boot()
