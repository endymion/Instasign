#pragma once
#include "../../IconTypes.h"

// Lucide 'alert-triangle' @ 10px
static const uint8_t icon_alerttriangle_10_bits[20] PROGMEM = {
  0xc0, 0x01, 0xe0, 0x03, 0x78, 0x03, 0x1e, 0x03, 0xff, 0x03, 0xff, 0x03, 0x1e, 0x03, 0x78, 0x03, 0xe0, 0x03, 0xc0, 0x01
};

static const BitmapIcon icon_alerttriangle_10 = {
  "alerttriangle",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_alerttriangle_10_bits
};
