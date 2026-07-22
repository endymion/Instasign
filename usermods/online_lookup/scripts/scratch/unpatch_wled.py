with open("wled00/wled.h", "r") as f:
    content = f.read()

content = content.replace("#ifdef ARDUINO_ARCH_ESP32\n#include <WiFiClientSecure.h>\n#endif\n", "#ifdef ARDUINO_ARCH_ESP32\n#endif\n")

with open("wled00/wled.h", "w") as f:
    f.write(content)
