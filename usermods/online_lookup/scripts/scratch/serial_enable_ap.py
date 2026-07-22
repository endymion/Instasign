import serial
import time

try:
    ser = serial.Serial('/dev/cu.usbmodem21101', 115200, timeout=2)
    ser.dtr = False
    ser.rts = False
    time.sleep(1)
    
    # Send JSON command to force AP mode
    ser.write(b'{"nw":{"ap":{"ssid":"WLED-AP","psk":"wled1234","behav":0},"ssid":"","psk":""}}\n')
    time.sleep(1)
    
    # Send reboot command
    ser.write(b'{"rb":true}\n')
    time.sleep(1)
    
    print("Sent AP enablement and reboot commands.")
except Exception as e:
    print(e)
