#pragma once
#include "../../IconTypes.h"

// Lucide 'sun' @ 5px
static const uint8_t icon_sun_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_sun_5 = {
  "sun",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_sun_5_bits
};
