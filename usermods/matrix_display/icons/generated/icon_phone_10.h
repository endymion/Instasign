#pragma once
#include "../../IconTypes.h"

// Lucide 'phone' @ 10px
static const uint8_t icon_phone_10_bits[20] PROGMEM = {
  0x1f, 0x00, 0x7f, 0x00, 0xfb, 0x00, 0xff, 0x01, 0xee, 0x01, 0xc0, 0x03, 0xe0, 0x03, 0x60, 0x03, 0xe0, 0x03, 0xc0, 0x03
};

static const BitmapIcon icon_phone_10 = {
  "phone",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_phone_10_bits
};
