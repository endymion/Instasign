#pragma once
#include "../../IconTypes.h"

// Lucide 'battery' @ 5px
static const uint8_t icon_battery_5_bits[5] PROGMEM = {
  0x1f, 0x1b, 0x1b, 0x1f, 0x1e
};

static const BitmapIcon icon_battery_5 = {
  "battery",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_battery_5_bits
};
