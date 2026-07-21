#pragma once
#include "../../IconTypes.h"

// Lucide 'unlock' @ 10px
static const uint8_t icon_unlock_10_bits[20] PROGMEM = {
  0xe0, 0x01, 0xf0, 0x03, 0x1e, 0x03, 0x1f, 0x03, 0x13, 0x03, 0x13, 0x03, 0x17, 0x03, 0x16, 0x03, 0xf0, 0x03, 0xe0, 0x01
};

static const BitmapIcon icon_unlock_10 = {
  "unlock",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_unlock_10_bits
};
