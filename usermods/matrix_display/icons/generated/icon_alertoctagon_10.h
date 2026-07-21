#pragma once
#include "../../IconTypes.h"

// Lucide 'alert-octagon' @ 10px
static const uint8_t icon_alertoctagon_10_bits[20] PROGMEM = {
  0xfc, 0x00, 0xfe, 0x01, 0x87, 0x03, 0x03, 0x03, 0x7b, 0x03, 0x7b, 0x03, 0x03, 0x03, 0x87, 0x03, 0xfe, 0x01, 0xfc, 0x00
};

static const BitmapIcon icon_alertoctagon_10 = {
  "alertoctagon",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_alertoctagon_10_bits
};
