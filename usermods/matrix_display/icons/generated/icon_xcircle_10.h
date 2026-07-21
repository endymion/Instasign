#pragma once
#include "../../IconTypes.h"

// Lucide 'x-circle' @ 10px
static const uint8_t icon_xcircle_10_bits[20] PROGMEM = {
  0x78, 0x00, 0xfe, 0x01, 0x86, 0x01, 0x7b, 0x03, 0x7b, 0x03, 0x7b, 0x03, 0x7b, 0x03, 0x86, 0x01, 0xfe, 0x01, 0x78, 0x00
};

static const BitmapIcon icon_xcircle_10 = {
  "xcircle",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_xcircle_10_bits
};
