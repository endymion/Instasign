#pragma once
#include "../../IconTypes.h"

// Lucide 'heart' @ 5px
static const uint8_t icon_heart_5_bits[5] PROGMEM = {
  0x0f, 0x1f, 0x1b, 0x1f, 0x0f
};

static const BitmapIcon icon_heart_5 = {
  "heart",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_heart_5_bits
};
