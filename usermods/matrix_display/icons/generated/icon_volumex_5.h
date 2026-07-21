#pragma once
#include "../../IconTypes.h"

// Lucide 'volume-x' @ 5px
static const uint8_t icon_volumex_5_bits[5] PROGMEM = {
  0x0e, 0x1f, 0x1f, 0x0e, 0x0e
};

static const BitmapIcon icon_volumex_5 = {
  "volumex",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_volumex_5_bits
};
