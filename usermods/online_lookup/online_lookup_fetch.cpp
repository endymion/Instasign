#include "online_lookup_fetch.h"

#ifdef ARDUINO_ARCH_ESP32
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <WiFiClient.h>

namespace {

struct ParsedUrl {
  bool tls = false;
  String host;
  uint16_t port = 0;
  String path;
};

bool parseUrl(const char* url, ParsedUrl& out) {
  String u(url);
  if (u.startsWith("https://")) {
    out.tls = true;
    out.port = 443;
    u.remove(0, 8);
  } else if (u.startsWith("http://")) {
    out.tls = false;
    out.port = 80;
    u.remove(0, 7);
  } else {
    return false;
  }

  int slash = u.indexOf('/');
  String hostPort = (slash < 0) ? u : u.substring(0, slash);
  out.path = (slash < 0) ? "/" : u.substring(slash);

  int colon = hostPort.indexOf(':');
  if (colon >= 0) {
    out.host = hostPort.substring(0, colon);
    out.port = (uint16_t)hostPort.substring(colon + 1).toInt();
  } else {
    out.host = hostPort;
  }
  return out.host.length() > 0;
}

// Manual HTTP GET over a raw (already-connected) Client -- bypasses
// Arduino's HTTPClient, whose Tasmota-patched header unconditionally
// #defines HTTPCLIENT_NOSECURE, making HTTPClient::begin() always reject
// https:// regardless of whether the underlying WiFiClientSecure/TLS stack
// actually works (it does; matrix_display's PubSubClient+WiFiClientSecure
// MQTT connection over TLS 8883 proves the same TLS stack functions fine --
// it never goes through HTTPClient at all, which is why it isn't affected).
bool httpGetOverClient(Client& client, const ParsedUrl& url, String& outBody, int& outStatus) {
  client.setTimeout(20000);
  bool connected = client.connect(url.host.c_str(), url.port);
  if (!connected) {
    // TEMP DIAGNOSTIC (see kanbus-2c3584): TLS connect() fails fast against every host
    // tried (thespacedevs.com, google.com) with legitimate mbedTLS handshake errors
    // (MBEDTLS_ERR_SSL_INVALID_RECORD / MBEDTLS_ERR_SSL_FATAL_ALERT_MESSAGE) even after
    // matching the mbedtls config header to the vendored .a files. Plain HTTP (this same
    // function, useTls=false) works perfectly, isolating the bug to the TLS handshake
    // itself. Root cause not yet found -- would benefit from packet capture or a from-
    // scratch mbedTLS build rather than further guessing. Remove this Serial.printf once
    // resolved.
    Serial.printf("DEBUG httpGetOverClient: connect() failed for host=%s port=%u\n", url.host.c_str(), url.port);
    outStatus = -1;
    return false;
  }

  client.print(F("GET "));
  client.print(url.path);
  client.print(F(" HTTP/1.1\r\nHost: "));
  client.print(url.host);
  client.print(F("\r\nUser-Agent: WLED-OnlineLookup\r\nAccept: application/json\r\nConnection: close\r\n\r\n"));

  unsigned long start = millis();
  while (!client.available() && client.connected()) {
    if (millis() - start > 20000) {
      outStatus = -11; // timeout, mirrors HTTPC_ERROR_READ_TIMEOUT
      client.stop();
      return false;
    }
    delay(10);
  }

  String statusLine = client.readStringUntil('\n');
  int firstSpace = statusLine.indexOf(' ');
  int secondSpace = statusLine.indexOf(' ', firstSpace + 1);
  if (firstSpace < 0 || secondSpace < 0) {
    outStatus = -2;
    client.stop();
    return false;
  }
  outStatus = statusLine.substring(firstSpace + 1, secondSpace).toInt();

  // Skip headers up to the blank line, noting chunked transfer-encoding.
  bool chunked = false;
  while (client.connected() || client.available()) {
    String line = client.readStringUntil('\n');
    if (line.length() <= 1) break; // just "\r"
    String lower = line;
    lower.toLowerCase();
    if (lower.startsWith("transfer-encoding:") && lower.indexOf("chunked") >= 0) {
      chunked = true;
    }
  }

  outBody = "";
  if (chunked) {
    // Chunked transfer encoding: each chunk is "<hex size>\r\n<data>\r\n",
    // terminated by a zero-size chunk.
    while (client.connected() || client.available()) {
      String sizeLine = client.readStringUntil('\n');
      sizeLine.trim();
      int semi = sizeLine.indexOf(';'); // chunk extensions, if any
      if (semi >= 0) sizeLine = sizeLine.substring(0, semi);
      long chunkSize = strtol(sizeLine.c_str(), nullptr, 16);
      if (chunkSize <= 0) break;
      long remaining = chunkSize;
      while (remaining > 0) {
        if (client.available()) {
          outBody += (char)client.read();
          remaining--;
        } else if (!client.connected()) {
          break;
        }
      }
      client.read(); // trailing \r
      client.read(); // trailing \n
    }
  } else {
    while (client.connected() || client.available()) {
      while (client.available()) {
        outBody += (char)client.read();
      }
    }
  }
  client.stop();

  return outStatus == 200 && outBody.length() > 0;
}

}  // namespace

bool onlineLookupHttpsGet(const char* url, String& outBody, int& outStatus) {
  outBody = "";
  outStatus = 0;
  if (!url || !url[0]) return false;

  ParsedUrl parsed;
  if (!parseUrl(url, parsed)) return false;

  if (parsed.tls) {
    WiFiClientSecure secure;
    secure.setInsecure(); // skip cert verify — saves RAM on ESP32-C3
    bool ok = httpGetOverClient(secure, parsed, outBody, outStatus);
    if (!ok) {
      char errBuf[128];
      int err = secure.lastError(errBuf, sizeof(errBuf));
      Serial.printf("DEBUG onlineLookupHttpsGet: TLS lastError=%d %s\n", err, errBuf);
    }
    return ok;
  } else {
    WiFiClient client;
    return httpGetOverClient(client, parsed, outBody, outStatus);
  }
}

#else

bool onlineLookupHttpsGet(const char* url, String& outBody, int& outStatus) {
  (void)url;
  outBody = "";
  outStatus = 0;
  return false;
}

#endif
