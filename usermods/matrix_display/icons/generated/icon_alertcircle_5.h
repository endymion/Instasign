#pragma once
#include "../../IconTypes.h"

// Lucide 'alert-circle' @ 5px
static const uint8_t icon_alertcircle_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_alertcircle_5 = {
  "alertcircle",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_alertcircle_5_bits
};
