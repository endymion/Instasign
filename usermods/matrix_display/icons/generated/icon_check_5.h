#pragma once
#include "../../IconTypes.h"

// Lucide 'check' @ 5px
static const uint8_t icon_check_5_bits[5] PROGMEM = {
  0x0c, 0x1c, 0x1e, 0x0f, 0x07
};

static const BitmapIcon icon_check_5 = {
  "check",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_check_5_bits
};
