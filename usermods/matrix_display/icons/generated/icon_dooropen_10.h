#pragma once
#include "../../IconTypes.h"

// Lucide 'door-open' @ 10px
static const uint8_t icon_dooropen_10_bits[20] PROGMEM = {
  0x00, 0x01, 0x00, 0x01, 0xfe, 0x01, 0x06, 0x01, 0xff, 0x03, 0x33, 0x03, 0x33, 0x03, 0xfe, 0x01, 0xfe, 0x01, 0x00, 0x01
};

static const BitmapIcon icon_dooropen_10 = {
  "dooropen",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_dooropen_10_bits
};
