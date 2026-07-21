#pragma once
#include <stdint.h>
#include <pgmspace.h>

// Square-ish Lucide icon bitmap (column-major, bit0 = top), same packing as fonts.
struct BitmapIcon {
  const char* name;       // canonical lowercase id, e.g. "bell"
  uint8_t size;           // nominal size bucket: 5, 10, 15, or 25
  uint8_t width;
  uint8_t height;
  uint8_t bytesPerColumn;
  const uint8_t* bits;    // PROGMEM [width * bytesPerColumn]
};
