#pragma once
#include "../../IconTypes.h"

// Lucide 'home' @ 5px
static const uint8_t icon_home_5_bits[5] PROGMEM = {
  0x1e, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_home_5 = {
  "home",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_home_5_bits
};
