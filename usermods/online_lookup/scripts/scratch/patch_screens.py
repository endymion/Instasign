import re

with open("usermods/online_lookup/online_lookup.h", "r") as f:
    content = f.read()

# Add drawScrollingString4x5
new_funcs = """  void drawString4x5(int16_t x, int16_t y, const String& text, uint32_t color) {
    for (unsigned int i = 0; i < text.length(); i++) {
      drawChar4x5(x + (i * 5), y, text[i], color); // 4px char + 1px spacing
    }
  }

  void drawScrollingString4x5(const String& text, uint32_t color, int yOffset = 1) {
    int textWidth = text.length() * 5 - 1;
    int scrollX = 0;
    
    if (textWidth > 64) {
      int maxScroll = textWidth - 64;
      long cycle = (millis() / 50) % (maxScroll + 40); // 50ms per pixel, 40 ticks padding
      if (cycle < 20) scrollX = 0;
      else if (cycle < 20 + maxScroll) scrollX = cycle - 20;
      else scrollX = maxScroll;
    } else {
      scrollX = -(64 - textWidth) / 2;
    }
    
    for (unsigned int i = 0; i < text.length(); i++) {
      int charX = (i * 5) - scrollX;
      if (charX > -5 && charX < 64) {
        drawChar4x5(charX, yOffset, text[i], color);
      }
    }
  }"""

content = re.sub(r"  void drawString4x5.*?  }", new_funcs, content, flags=re.DOTALL)

# Fix pages logic from 2 to 4
content = content.replace("currentPage = (currentPage + 1) % 2; // Only 2 pages", "currentPage = (currentPage + 1) % 4;")

# Replace handleOverlayDraw page rendering
old_render = r"    if \(currentPage == 0\) \{.*?if \(isPast\) diff = -diff;"
new_render = """    if (currentPage == 0) {
      String dt = launchDate + " " + launchTime;
      dt.replace(" UTC", ""); // Too long for one line
      dt.replace(" EDT", "");
      int textWidth = dt.length() * 5 - 1;
      int startX = (64 - textWidth) / 2;
      if (startX < 0) startX = 0;
      drawString4x5(startX, yOffset, dt, statusColor);
    } else if (currentPage == 1) {
      drawScrollingString4x5(launchName, greyColor, yOffset);
    } else if (currentPage == 2) {
      drawScrollingString4x5(launchVehicle, greyColor, yOffset);
    } else {
      if (launchUnixTime == 0 || currentUnixTime == 0) {
        String tStr = "T- TBD";
        int textWidth = tStr.length() * 5 - 1;
        drawString4x5((64 - textWidth) / 2, yOffset, tStr, statusColor);
      } else {
        long diff = launchUnixTime - currentUnixTime;
        bool isPast = (diff <= 0);
        if (isPast) diff = -diff;"""

content = re.sub(old_render, new_render, content, flags=re.DOTALL)

with open("usermods/online_lookup/online_lookup.h", "w") as f:
    f.write(content)

