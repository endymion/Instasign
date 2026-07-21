#pragma once
#include "../../IconTypes.h"

// Lucide 'wifi-off' @ 10px
static const uint8_t icon_wifioff_10_bits[20] PROGMEM = {
  0x0b, 0x00, 0x2f, 0x00, 0x3e, 0x00, 0xdc, 0x00, 0x7e, 0x01, 0x76, 0x01, 0xf6, 0x00, 0xfc, 0x01, 0xac, 0x03, 0x08, 0x03
};

static const BitmapIcon icon_wifioff_10 = {
  "wifioff",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_wifioff_10_bits
};
