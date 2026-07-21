#pragma once
#include "../../IconTypes.h"

// Lucide 'bell-off' @ 10px
static const uint8_t icon_belloff_10_bits[20] PROGMEM = {
  0x43, 0x00, 0xf7, 0x00, 0xfe, 0x00, 0xdf, 0x01, 0xfb, 0x03, 0xf3, 0x03, 0xe7, 0x01, 0xfe, 0x01, 0xf0, 0x03, 0x00, 0x03
};

static const BitmapIcon icon_belloff_10 = {
  "belloff",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_belloff_10_bits
};
