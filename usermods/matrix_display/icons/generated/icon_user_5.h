#pragma once
#include "../../IconTypes.h"

// Lucide 'user' @ 5px
static const uint8_t icon_user_5_bits[5] PROGMEM = {
  0x18, 0x1f, 0x0f, 0x1f, 0x1c
};

static const BitmapIcon icon_user_5 = {
  "user",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_user_5_bits
};
