import re

with open("usermods/online_lookup/online_lookup.h", "r") as f:
    content = f.read()

# Replace getPixelIndex and drawChar4x5
new_get_pixel = """
  // Set pixel natively handling 2D segments in WLED
  void setPixelXY(int16_t x, int16_t y, uint32_t color) {
    if (x < 0 || x >= 64 || y < 0 || y >= 8) return;
    Segment& seg = strip.getMainSegment();
    if (seg.is2D()) {
      seg.setPixelColorXY(x, y, color);
    } else {
      // Fallback 1D mapping for 8x64 if not configured as 2D
      int local_x = x < 32 ? x : x - 32;
      int base_idx = x < 32 ? 0 : 256;
      bool goingUp = matrixStartBottom;
      if (matrixSerpentine && (local_x % 2 == 1)) goingUp = !goingUp;
      int local_y = goingUp ? (7 - y) : y;
      int index = base_idx + (local_x * 8) + local_y;
      if (index < strip.getLengthTotal()) strip.setPixelColor(index, color);
    }
  }

  void drawChar4x5(int16_t x, int16_t y, char c, uint32_t color) {
    uint32_t bitmap = font4x5[(uint8_t)c];
    for (int col = 0; col < 4; col++) {
      for (int row = 0; row < 5; row++) {
        if (bitmap & (1 << (19 - (row * 4 + col)))) {
          setPixelXY(x + col, y + row, color);
        }
      }
    }
  }
"""

content = re.sub(r"  int getPixelIndex\(int x, int y\) \{.*?void drawChar4x5\(int16_t x, int16_t y, char c, uint32_t color\) \{.*?\}\n  \}", new_get_pixel, content, flags=re.DOTALL)

# Replace strip.setPixelColor calls in status bar and clear
content = re.sub(r"for \(int i = 0; i < 512; i\+\+\) \{\n\s*strip\.setPixelColor\(i, 0\);\n\s*\}", r"for (int i = 0; i < strip.getLengthTotal(); i++) strip.setPixelColor(i, 0);", content)
content = re.sub(r"int pixelIdx = getPixelIndex\(i, 7\);\n\s*if \(pixelIdx >= 0\) strip\.setPixelColor\(pixelIdx, statusColor\);", r"setPixelXY(i, 7, statusColor);", content)

with open("usermods/online_lookup/online_lookup.h", "w") as f:
    f.write(content)
