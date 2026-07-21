#pragma once
#include "../../IconTypes.h"

// Lucide 'check-circle' @ 5px
static const uint8_t icon_checkcircle_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_checkcircle_5 = {
  "checkcircle",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_checkcircle_5_bits
};
