#pragma once
#include "../../IconTypes.h"

// Lucide 'home' @ 10px
static const uint8_t icon_home_10_bits[20] PROGMEM = {
  0xf8, 0x01, 0xfc, 0x03, 0x0e, 0x03, 0xf6, 0x03, 0xf3, 0x03, 0xf3, 0x03, 0xf6, 0x03, 0x0e, 0x03, 0xfc, 0x03, 0xf8, 0x01
};

static const BitmapIcon icon_home_10 = {
  "home",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_home_10_bits
};
