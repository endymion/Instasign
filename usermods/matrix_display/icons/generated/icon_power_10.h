#pragma once
#include "../../IconTypes.h"

// Lucide 'power' @ 10px
static const uint8_t icon_power_10_bits[20] PROGMEM = {
  0x30, 0x00, 0xfc, 0x01, 0x8c, 0x01, 0x00, 0x03, 0x3f, 0x03, 0x3f, 0x03, 0x00, 0x03, 0x8c, 0x01, 0xfc, 0x01, 0x70, 0x00
};

static const BitmapIcon icon_power_10 = {
  "power",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_power_10_bits
};
