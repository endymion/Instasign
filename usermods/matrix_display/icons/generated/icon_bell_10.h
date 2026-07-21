#pragma once
#include "../../IconTypes.h"

// Lucide 'bell' @ 10px
static const uint8_t icon_bell_10_bits[20] PROGMEM = {
  0x40, 0x00, 0xf0, 0x00, 0xfe, 0x00, 0xc7, 0x01, 0xc3, 0x03, 0xc3, 0x03, 0xc7, 0x01, 0xfe, 0x00, 0xf0, 0x00, 0x40, 0x00
};

static const BitmapIcon icon_bell_10 = {
  "bell",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_bell_10_bits
};
