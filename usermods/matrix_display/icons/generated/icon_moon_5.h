#pragma once
#include "../../IconTypes.h"

// Lucide 'moon' @ 5px
static const uint8_t icon_moon_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1d, 0x1c
};

static const BitmapIcon icon_moon_5 = {
  "moon",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_moon_5_bits
};
