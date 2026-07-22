import re

with open("usermods/online_lookup/online_lookup.h", "r") as f:
    content = f.read()

# Replace font
font_pattern = r"const uint16_t customFont3x5\[256\].*?};"
with open("scratch/font4x5.h", "r") as f:
    font_data = f.read()
    
# Extract font array from font4x5.h
font_data = font_data[font_data.find("const uint32_t font4x5[256] = {"):]
font_data = font_data.replace("uint32_t font4x5", "uint32_t customFont4x5")

content = re.sub(font_pattern, font_data, content, flags=re.DOTALL)

# Replace drawing functions
draw_funcs = r"void drawChar3x5\(int16_t x, int16_t y, char c, uint32_t color\).*?void drawString3x5\(int16_t x, int16_t y, const String& text, uint32_t color\) \{[^\}]*\}"

new_draw_funcs = """void drawChar4x5(int16_t x, int16_t y, char c, uint32_t color) {
    uint32_t bitmap = customFont4x5[(uint8_t)c];
    for (int col = 0; col < 4; col++) {
      for (int row = 0; row < 5; row++) {
        if (bitmap & (1 << (col * 5 + row))) {
          int pixelIdx = getPixelIndex(x + col, y + row);
          if (pixelIdx >= 0) {
            strip.setPixelColor(pixelIdx, color);
          }
        }
      }
    }
  }

  void drawString4x5(int16_t x, int16_t y, const String& text, uint32_t color) {
    for (unsigned int i = 0; i < text.length(); i++) {
      drawChar4x5(x + (i * 5), y, text[i], color); // 4px char + 1px spacing
    }
  }"""

content = re.sub(r"void drawChar3x5.*?void drawString3x5[^}]+}", new_draw_funcs, content, flags=re.DOTALL)
content = re.sub(r"void drawScrollingString3x5[^}]+}", "", content, flags=re.DOTALL)

# Replace parsing
parsing_old = r"StaticJsonDocument<400> filter;.*?updateInProgress = false;"
parsing_new = """      DynamicJsonDocument doc(2048);
      DeserializationError error = deserializeJson(doc, http.getStream());
      
      if (!error) {
        launchName = doc["name"] | "Unknown";
        launchVehicle = doc["vehicle"] | "Unknown";
        launchStatusId = doc["status_id"] | 2;
        String dateStr = doc["date"] | "TBD";
        String timeStr = doc["time"] | "TBD";
        
        launchDate = dateStr;
        launchTime = timeStr;
        launchUnixTime = doc["net_unix"] | 0;
        currentProxyUnixTime = doc["current_unix"] | 0;
        lastProxyFetchMillis = millis();
      } else {
        launchName = "Parse Err";
      }
    } else {
      launchName = "HTTP " + String(httpCode) + " " + http.errorToString(httpCode);
    }
    http.end();
    updateInProgress = false;"""

content = re.sub(parsing_old, parsing_new, content, flags=re.DOTALL)

# Add currentProxyUnixTime to class
content = content.replace("long launchUnixTime = 0;", "long launchUnixTime = 0;\n    long currentProxyUnixTime = 0;\n    unsigned long lastProxyFetchMillis = 0;")

# Fix Page interval logic
page_logic = r"// Page flipping logic.*?if \(lockedToCountdown\).*?currentPage = \(currentPage \+ 1\) % 7;\n      \}\n    \}"
new_page_logic = """// Page flipping logic
    if (millis() - lastPageSwitch > (pageIntervalSeconds * 1000)) {
      lastPageSwitch = millis();
      currentPage = (currentPage + 1) % 2; // Only 2 pages now
    }"""
content = re.sub(page_logic, new_page_logic, content, flags=re.DOTALL)

# Replace handleOverlayDraw
draw_old = r"void handleOverlayDraw\(\) override \{.*?void addToConfig"
new_draw = """void handleOverlayDraw() override {
    if (!enabled) return;

    for (int i = 0; i < 512; i++) {
      strip.setPixelColor(i, 0);
    }

    uint32_t statusColor = RGBW32(170, 170, 170, 0); // Default Light Grey
    if (launchStatusId == 1 || launchStatusId == 3) statusColor = RGBW32(0, 255, 0, 0); // Green (Go or Success)
    else if (launchStatusId == 4) statusColor = RGBW32(255, 0, 0, 0);  // Red
    else if (launchStatusId == 5) statusColor = RGBW32(255, 255, 0, 0); // Yellow

    uint32_t greyColor = RGBW32(170, 170, 170, 0);
    
    // In-flight / Post-launch logic
    long currentUnixTime = 0;
    if (currentProxyUnixTime > 0) {
      currentUnixTime = currentProxyUnixTime + ((millis() - lastProxyFetchMillis) / 1000);
    }

    if (launchUnixTime != 0 && currentUnixTime != 0) {
      long diff = launchUnixTime - currentUnixTime;
      // If success and within 1 hour after launch, turn everything green
      if (launchStatusId == 3 && diff < 0 && diff >= -3600) {
        greyColor = RGBW32(0, 255, 0, 0);
      }
    }

    int yOffset = 1; // Center vertically on 8px height (8 - 5 = 3; 3/2 = 1)
    
    if (currentPage == 0) {
      // Date and Time
      String dt = launchDate + " " + launchTime;
      dt.replace(" UTC", ""); // Too long for one line, remove UTC
      int textWidth = dt.length() * 5 - 1;
      int startX = (64 - textWidth) / 2;
      if (startX < 0) startX = 0;
      drawString4x5(startX, yOffset, dt, statusColor);
    } else {
      // Countdown
      if (launchUnixTime == 0 || currentUnixTime == 0) {
        String tStr = "T- TBD";
        int textWidth = tStr.length() * 5 - 1;
        drawString4x5((64 - textWidth) / 2, yOffset, tStr, statusColor);
      } else {
        long diff = launchUnixTime - currentUnixTime;
        bool isPast = (diff <= 0);
        if (isPast) diff = -diff;
        
        long days = diff / 86400;
        long hours = (diff % 86400) / 3600;
        long minutes = (diff % 3600) / 60;
        long seconds = diff % 60;
        
        String tStr = isPast ? "T+ " : "T- ";
        
        if (days > 0) {
          tStr += String(days) + "d " + String(hours) + "h";
        } else if (hours > 0) {
          tStr += String(hours) + "h " + String(minutes) + "m";
        } else {
          char buf[10];
          sprintf(buf, "%02ld:%02ld:%02ld", hours, minutes, seconds);
          tStr += String(buf);
        }
        
        int textWidth = tStr.length() * 5 - 1;
        int startX = (64 - textWidth) / 2;
        if (startX < 0) startX = 0;
        drawString4x5(startX, yOffset, tStr, statusColor);
      }
    }

    // Status bar on bottom row if within 24 hours
    if (launchUnixTime != 0 && currentUnixTime != 0) {
      long diff = launchUnixTime - currentUnixTime;
      if (diff > -86400 && diff <= 86400) {
        for (int i = 0; i < 64; i++) {
          int pixelIdx = getPixelIndex(i, 7);
          if (pixelIdx >= 0) strip.setPixelColor(pixelIdx, statusColor);
        }
      }
    }
  }

  void addToConfig"""
content = re.sub(draw_old, new_draw, content, flags=re.DOTALL)

with open("usermods/online_lookup/online_lookup.h", "w") as f:
    f.write(content)
