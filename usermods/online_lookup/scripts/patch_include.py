with open('usermods/online_lookup/online_lookup.h', 'r') as f:
    content = f.read()

if '<WiFiClientSecure.h>' not in content:
    content = content.replace('#include "wled.h"', '#include "wled.h"\n#include <WiFiClientSecure.h>')

with open('usermods/online_lookup/online_lookup.h', 'w') as f:
    f.write(content)
