#pragma once
#include "../../IconTypes.h"

// Lucide 'battery-warning' @ 5px
static const uint8_t icon_batterywarning_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1e
};

static const BitmapIcon icon_batterywarning_5 = {
  "batterywarning",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_batterywarning_5_bits
};
