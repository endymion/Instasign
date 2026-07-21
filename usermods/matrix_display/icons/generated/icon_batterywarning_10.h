#pragma once
#include "../../IconTypes.h"

// Lucide 'battery-warning' @ 10px
static const uint8_t icon_batterywarning_10_bits[20] PROGMEM = {
  0xfc, 0x00, 0xfc, 0x00, 0x84, 0x00, 0xfc, 0x00, 0xfc, 0x00, 0x84, 0x00, 0x84, 0x00, 0xfc, 0x00, 0x78, 0x00, 0x78, 0x00
};

static const BitmapIcon icon_batterywarning_10 = {
  "batterywarning",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_batterywarning_10_bits
};
