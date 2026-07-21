#pragma once
#include "../../IconTypes.h"

// Lucide 'volume-2' @ 10px
static const uint8_t icon_volume2_10_bits[20] PROGMEM = {
  0x78, 0x00, 0x78, 0x00, 0xcc, 0x00, 0xce, 0x01, 0xfe, 0x01, 0x00, 0x00, 0x78, 0x00, 0xfc, 0x00, 0xfc, 0x00, 0x78, 0x00
};

static const BitmapIcon icon_volume2_10 = {
  "volume2",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_volume2_10_bits
};
