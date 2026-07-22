import re

with open('usermods/online_lookup/online_lookup.h', 'r') as f:
    content = f.read()

new_content = re.sub(
    r'#ifdef ARDUINO_ARCH_ESP32\s+HTTPClient http;\s+http\.begin\(apiUrl\);\s+#else\s+WiFiClientSecure client;\s+client\.setInsecure\(\);\s+HTTPClient http;\s+http\.begin\(client, apiUrl\);\s+#endif',
    r'WiFiClientSecure client;\n    client.setInsecure();\n    HTTPClient http;\n    http.begin(client, apiUrl);',
    content
)

with open('usermods/online_lookup/online_lookup.h', 'w') as f:
    f.write(new_content)
