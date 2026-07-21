#pragma once
#include "../../IconTypes.h"

// Lucide 'star' @ 5px
static const uint8_t icon_star_5_bits[5] PROGMEM = {
  0x1e, 0x1f, 0x1f, 0x1f, 0x1e
};

static const BitmapIcon icon_star_5 = {
  "star",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_star_5_bits
};
