#pragma once

#include <Arduino.h>

// Fetches url over HTTP or HTTPS. For https:// uses WiFiClientSecure (insecure/skip verify to save RAM).
// Returns true on HTTP 200 with a non-empty body.
bool onlineLookupHttpsGet(const char* url, String& outBody, int& outStatus);
