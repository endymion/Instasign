#pragma once
#include "../../IconTypes.h"

// Lucide 'star' @ 10px
static const uint8_t icon_star_10_bits[20] PROGMEM = {
  0x18, 0x00, 0x38, 0x00, 0xf8, 0x03, 0xce, 0x01, 0x8f, 0x01, 0x8f, 0x01, 0xce, 0x01, 0xf8, 0x03, 0x38, 0x00, 0x18, 0x00
};

static const BitmapIcon icon_star_10 = {
  "star",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_star_10_bits
};
