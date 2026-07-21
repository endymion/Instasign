#pragma once
#include "../../IconTypes.h"

// Lucide 'moon' @ 10px
static const uint8_t icon_moon_10_bits[20] PROGMEM = {
  0x30, 0x00, 0xfc, 0x00, 0xce, 0x01, 0x86, 0x01, 0x1f, 0x03, 0x3e, 0x03, 0xb0, 0x01, 0xf0, 0x01, 0xf0, 0x00, 0x20, 0x00
};

static const BitmapIcon icon_moon_10 = {
  "moon",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_moon_10_bits
};
