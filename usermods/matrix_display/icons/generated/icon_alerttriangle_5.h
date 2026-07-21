#pragma once
#include "../../IconTypes.h"

// Lucide 'alert-triangle' @ 5px
static const uint8_t icon_alerttriangle_5_bits[5] PROGMEM = {
  0x1c, 0x1f, 0x1f, 0x1f, 0x1e
};

static const BitmapIcon icon_alerttriangle_5 = {
  "alerttriangle",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_alerttriangle_5_bits
};
