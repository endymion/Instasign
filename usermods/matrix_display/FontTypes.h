#pragma once
#include <stdint.h>
#include <pgmspace.h>

// Column-major bitmap font: each glyph has `width` columns, and each column
// is `bytesPerColumn` bytes (bit 0 of byte 0 = top pixel).
struct BitmapFont {
  const char* name;           // canonical lowercase id, e.g. "jersey10"
  uint8_t height;             // glyph cell height in pixels
  uint8_t defaultLineHeight;  // suggested line height (usually height + 1)
  uint8_t bytesPerColumn;     // ceil(height / 8)
  uint8_t maxWidth;           // max glyph width (bitmap stride)
  const uint8_t* widths;      // PROGMEM [95] ASCII 32..126
  const uint8_t* bitmaps;     // PROGMEM [95 * maxWidth * bytesPerColumn]
};
