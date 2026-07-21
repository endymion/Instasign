#pragma once
#include "../../IconTypes.h"

// Lucide 'bell-off' @ 5px
static const uint8_t icon_belloff_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_belloff_5 = {
  "belloff",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_belloff_5_bits
};
