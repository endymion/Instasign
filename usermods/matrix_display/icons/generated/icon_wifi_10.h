#pragma once
#include "../../IconTypes.h"

// Lucide 'wifi' @ 10px
static const uint8_t icon_wifi_10_bits[20] PROGMEM = {
  0x08, 0x00, 0x2c, 0x00, 0x3c, 0x00, 0xde, 0x00, 0x7e, 0x01, 0x7e, 0x01, 0xde, 0x00, 0x3c, 0x00, 0x2c, 0x00, 0x08, 0x00
};

static const BitmapIcon icon_wifi_10 = {
  "wifi",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_wifi_10_bits
};
