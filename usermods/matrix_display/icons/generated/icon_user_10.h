#pragma once
#include "../../IconTypes.h"

// Lucide 'user' @ 10px
static const uint8_t icon_user_10_bits[20] PROGMEM = {
  0x00, 0x00, 0x80, 0x03, 0xc0, 0x03, 0x7e, 0x00, 0x7b, 0x00, 0x7b, 0x00, 0x7e, 0x00, 0xc0, 0x03, 0x80, 0x03, 0x00, 0x00
};

static const BitmapIcon icon_user_10 = {
  "user",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_user_10_bits
};
