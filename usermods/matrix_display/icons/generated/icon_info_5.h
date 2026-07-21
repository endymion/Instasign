#pragma once
#include "../../IconTypes.h"

// Lucide 'info' @ 5px
static const uint8_t icon_info_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_info_5 = {
  "info",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_info_5_bits
};
