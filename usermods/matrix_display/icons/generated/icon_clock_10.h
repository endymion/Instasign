#pragma once
#include "../../IconTypes.h"

// Lucide 'clock' @ 10px
static const uint8_t icon_clock_10_bits[20] PROGMEM = {
  0x78, 0x00, 0xfe, 0x01, 0x86, 0x01, 0x03, 0x03, 0x3f, 0x03, 0x3f, 0x03, 0x63, 0x03, 0x86, 0x01, 0xfe, 0x01, 0x78, 0x00
};

static const BitmapIcon icon_clock_10 = {
  "clock",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_clock_10_bits
};
