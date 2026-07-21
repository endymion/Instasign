#pragma once
#include "../../IconTypes.h"

// Lucide 'x-circle' @ 5px
static const uint8_t icon_xcircle_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_xcircle_5 = {
  "xcircle",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_xcircle_5_bits
};
