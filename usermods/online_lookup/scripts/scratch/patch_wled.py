with open("wled00/wled.h", "r") as f:
    content = f.read()

if "#include <WiFiClientSecure.h>" not in content:
    content = content.replace("#ifdef ARDUINO_ARCH_ESP32\n#endif", "#ifdef ARDUINO_ARCH_ESP32\n#include <WiFiClientSecure.h>\n#endif")

with open("wled00/wled.h", "w") as f:
    f.write(content)
