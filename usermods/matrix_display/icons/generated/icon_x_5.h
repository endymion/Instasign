#pragma once
#include "../../IconTypes.h"

// Lucide 'x' @ 5px
static const uint8_t icon_x_5_bits[5] PROGMEM = {
  0x1b, 0x1f, 0x0e, 0x1f, 0x1b
};

static const BitmapIcon icon_x_5 = {
  "x",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_x_5_bits
};
