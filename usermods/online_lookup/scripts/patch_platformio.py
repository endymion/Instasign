import configparser

config = configparser.ConfigParser(strict=False, allow_no_value=True)
config.read('platformio_override.ini')

if config.has_option('env:esp32c3dev', 'build_flags'):
    existing = config.get('env:esp32c3dev', 'build_flags')
    config.set('env:esp32c3dev', 'build_flags', f"{existing} -D ARDUINO_USB_MODE=1 -D ARDUINO_USB_CDC_ON_BOOT=1")

with open('platformio_override.ini', 'w') as f:
    config.write(f)

print("Patched platformio_override.ini")
