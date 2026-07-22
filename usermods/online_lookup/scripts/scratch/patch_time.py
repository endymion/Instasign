import re

with open("usermods/online_lookup/online_lookup.h", "r") as f:
    content = f.read()

# Replace currentProxyUnixTime with toki.second() in loop() dynamic brightness
content = content.replace("currentProxyUnixTime", "toki.second()")

# Remove the line `long currentUnixTime = currentProxyUnixTime + ((millis() - lastProxyFetchMillis) / 1000);`
content = re.sub(r"        long currentUnixTime = toki\.second\(\) \+ \(\(millis\(\) - lastProxyFetchMillis\) / 1000\);\n", "        long currentUnixTime = toki.second();\n", content)

# In handleOverlayDraw, replace time tracking
old_handle_time = """    long currentUnixTime = 0;
    if (toki.second() > 0) {
      currentUnixTime = toki.second() + ((millis() - lastProxyFetchMillis) / 1000);
    }"""
new_handle_time = """    long currentUnixTime = toki.second();"""
content = content.replace(old_handle_time, new_handle_time)

with open("usermods/online_lookup/online_lookup.h", "w") as f:
    f.write(content)
