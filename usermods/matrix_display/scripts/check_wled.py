import serial
import time
import sys
import json

def fetch_cfg():
    port = '/dev/cu.usbmodem21101'
    baudrate = 115200
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        ser.write(b'{"v":true}\n') # to get state, but wait, to get cfg we can send {"v":true} and see if it replies with state
        # Wait, there's a serial command to get config? No, usually HTTP `/json/cfg`. 
        # Is there a serial command for it?
        # Not sure, but we can just use HTTP since AP is up!
        # But wait, my computer is not connected to the AP.
    except Exception as e:
        pass
        
if __name__ == "__main__":
    fetch_cfg()
