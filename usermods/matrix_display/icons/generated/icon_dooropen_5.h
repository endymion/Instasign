#pragma once
#include "../../IconTypes.h"

// Lucide 'door-open' @ 5px
static const uint8_t icon_dooropen_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_dooropen_5 = {
  "dooropen",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_dooropen_5_bits
};
