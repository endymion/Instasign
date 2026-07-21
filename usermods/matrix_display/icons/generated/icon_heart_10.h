#pragma once
#include "../../IconTypes.h"

// Lucide 'heart' @ 10px
static const uint8_t icon_heart_10_bits[20] PROGMEM = {
  0x3c, 0x00, 0x7e, 0x00, 0xe6, 0x00, 0xc6, 0x01, 0x86, 0x03, 0x86, 0x03, 0xc6, 0x01, 0xe6, 0x00, 0x7e, 0x00, 0x3c, 0x00
};

static const BitmapIcon icon_heart_10 = {
  "heart",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_heart_10_bits
};
