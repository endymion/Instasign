import re

with open("usermods/online_lookup/online_lookup.h", "r") as f:
    content = f.read()

# Add WiFiClientSecure
content = content.replace("#include <HTTPClient.h>", "#include <HTTPClient.h>\n#include <WiFiClientSecure.h>\n#include <time.h>\n#include <string.h>")

# Remove apiUrl from user configuration
content = content.replace('String apiUrl = "http://192.168.1.93:8080/";\n', "")
content = content.replace('top["apiUrl"] = apiUrl;\n', "")
content = content.replace('configComplete &= getJsonValue(top["apiUrl"], apiUrl);\n', "")

# Replace time tracking variables
old_vars = """    // Time tracking to bypass NTP
    long currentProxyUnixTime = 0;
    unsigned long lastProxyFetchMillis = 0;"""
content = content.replace(old_vars, "")

# Insert parseISO8601 helper
parse_helper = """  long parseISO8601(const char* time_str) {
    struct tm tm;
    memset(&tm, 0, sizeof(tm));
    if (strptime(time_str, "%Y-%m-%dT%H:%M:%SZ", &tm) != NULL) {
        // Simple manual conversion to unix epoch for UTC
        int year = tm.tm_year + 1900;
        int month = tm.tm_mon + 1;
        int day = tm.tm_mday;
        
        int a = (14 - month) / 12;
        int y = year + 4800 - a;
        int m = month + 12 * a - 3;
        
        int Jd = day + (153 * m + 2) / 5 + 365 * y + y / 4 - y / 100 + y / 400 - 32045;
        long unixTime = (Jd - 2440588) * 86400L;
        
        unixTime += tm.tm_hour * 3600L;
        unixTime += tm.tm_min * 60L;
        unixTime += tm.tm_sec;
        
        return unixTime;
    }
    return 0;
  }
"""
content = re.sub(r"(?<=  #ifdef ARDUINO_ARCH_ESP32\n  TaskHandle_t updateTaskHandle = nullptr;)", "\n" + parse_helper, content)


# Rewrite performUpdate
old_perform = r"  void performUpdate\(\) \{.*?    updateInProgress = false;\n  \}"
new_perform = """  void performUpdate() {
    if (!WLED_CONNECTED) {
      launchName = "No WiFi";
      updateInProgress = false;
      return;
    }
    
    #ifdef ARDUINO_ARCH_ESP32
    WiFiClientSecure *client = new WiFiClientSecure;
    if (client) {
      client->setInsecure(); // Skip certificate verification to save RAM
      HTTPClient http;
      if (http.begin(*client, "https://ll.thespacedevs.com/2.3.0/launches/upcoming/?limit=1&location__ids=12")) {
        int httpCode = http.GET();
        if (httpCode == HTTP_CODE_OK) {
          StaticJsonDocument<256> filter;
          filter["results"][0]["name"] = true;
          filter["results"][0]["net"] = true;
          filter["results"][0]["status"]["id"] = true;
          filter["results"][0]["rocket"]["configuration"]["name"] = true;
          filter["results"][0]["launch_service_provider"]["name"] = true;
          
          DynamicJsonDocument doc(1024);
          DeserializationError error = deserializeJson(doc, http.getStream(), DeserializationOption::Filter(filter));
          
          if (!error && doc["results"].size() > 0) {
            JsonObject result = doc["results"][0];
            
            String fullName = result["name"] | "Unknown";
            // abbreviate "Falcon 9 Block 5 | MRV-1" -> "MRV-1"
            int pipeIdx = fullName.indexOf('|');
            if (pipeIdx > 0 && pipeIdx + 2 < fullName.length()) {
              launchName = fullName.substring(pipeIdx + 2);
            } else {
              launchName = fullName;
            }
            
            String provider = result["launch_service_provider"]["name"] | "Unknown";
            String rocket = result["rocket"]["configuration"]["name"] | "Unknown";
            
            if (provider == "SpaceX" && rocket.indexOf("Falcon 9") >= 0) launchVehicle = "SpaceX Falcon 9";
            else if (provider == "SpaceX" && rocket.indexOf("Falcon Heavy") >= 0) launchVehicle = "SpX Falcon Heavy";
            else if (provider == "United Launch Alliance") launchVehicle = "ULA " + rocket;
            else if (provider == "Rocket Lab") launchVehicle = "RL " + rocket;
            else launchVehicle = provider + " " + rocket;
            
            if (launchVehicle.length() > 16) launchVehicle = launchVehicle.substring(0, 16);
            
            launchStatusId = result["status"]["id"] | 2;
            
            const char* net_str = result["net"] | "";
            launchUnixTime = parseISO8601(net_str);
            
            if (launchUnixTime > 0) {
              // Convert to local time for strings
              time_t localLaunchTime = launchUnixTime + utcOffsetSecs;
              struct tm tm_local;
              gmtime_r(&localLaunchTime, &tm_local);
              
              char dateBuf[16];
              strftime(dateBuf, sizeof(dateBuf), "%b %d", &tm_local);
              launchDate = String(dateBuf);
              
              char timeBuf[16];
              strftime(timeBuf, sizeof(timeBuf), "%H:%M", &tm_local);
              launchTime = String(timeBuf);
            }
          } else {
            launchName = "Parse Err";
          }
        } else {
          launchName = "HTTP " + String(httpCode);
        }
        http.end();
      } else {
        launchName = "Conn Err";
      }
      delete client;
    }
    #endif
    
    updateInProgress = false;
  }"""
content = re.sub(old_perform, new_perform, content, flags=re.DOTALL)

with open("usermods/online_lookup/online_lookup.h", "w") as f:
    f.write(content)
