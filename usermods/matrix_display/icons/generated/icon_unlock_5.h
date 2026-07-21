#pragma once
#include "../../IconTypes.h"

// Lucide 'unlock' @ 5px
static const uint8_t icon_unlock_5_bits[5] PROGMEM = {
  0x1e, 0x1f, 0x17, 0x1f, 0x1f
};

static const BitmapIcon icon_unlock_5 = {
  "unlock",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_unlock_5_bits
};
