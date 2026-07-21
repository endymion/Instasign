#pragma once
#include "../../IconTypes.h"

// Lucide 'wifi' @ 5px
static const uint8_t icon_wifi_5_bits[5] PROGMEM = {
  0x0f, 0x1f, 0x1f, 0x1f, 0x0f
};

static const BitmapIcon icon_wifi_5 = {
  "wifi",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_wifi_5_bits
};
