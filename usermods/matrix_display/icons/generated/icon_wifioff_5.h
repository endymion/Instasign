#pragma once
#include "../../IconTypes.h"

// Lucide 'wifi-off' @ 5px
static const uint8_t icon_wifioff_5_bits[5] PROGMEM = {
  0x0f, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_wifioff_5 = {
  "wifioff",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_wifioff_5_bits
};
