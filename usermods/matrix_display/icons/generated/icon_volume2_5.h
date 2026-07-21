#pragma once
#include "../../IconTypes.h"

// Lucide 'volume-2' @ 5px
static const uint8_t icon_volume2_5_bits[5] PROGMEM = {
  0x0e, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_volume2_5 = {
  "volume2",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_volume2_5_bits
};
