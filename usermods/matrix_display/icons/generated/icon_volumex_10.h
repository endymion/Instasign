#pragma once
#include "../../IconTypes.h"

// Lucide 'volume-x' @ 10px
static const uint8_t icon_volumex_10_bits[20] PROGMEM = {
  0x78, 0x00, 0x78, 0x00, 0xcc, 0x00, 0xce, 0x01, 0xfe, 0x01, 0x00, 0x00, 0x78, 0x00, 0x78, 0x00, 0x78, 0x00, 0x78, 0x00
};

static const BitmapIcon icon_volumex_10 = {
  "volumex",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_volumex_10_bits
};
