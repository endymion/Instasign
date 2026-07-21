#pragma once
#include "../../IconTypes.h"

// Lucide 'clock' @ 5px
static const uint8_t icon_clock_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_clock_5 = {
  "clock",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_clock_5_bits
};
