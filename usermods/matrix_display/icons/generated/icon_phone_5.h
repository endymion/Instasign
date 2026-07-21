#pragma once
#include "../../IconTypes.h"

// Lucide 'phone' @ 5px
static const uint8_t icon_phone_5_bits[5] PROGMEM = {
  0x0f, 0x1f, 0x1f, 0x1c, 0x1c
};

static const BitmapIcon icon_phone_5 = {
  "phone",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_phone_5_bits
};
