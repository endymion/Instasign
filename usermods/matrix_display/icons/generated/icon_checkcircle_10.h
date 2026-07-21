#pragma once
#include "../../IconTypes.h"

// Lucide 'check-circle' @ 10px
static const uint8_t icon_checkcircle_10_bits[20] PROGMEM = {
  0x78, 0x00, 0xfe, 0x01, 0x86, 0x01, 0x33, 0x03, 0x73, 0x03, 0x33, 0x03, 0x1b, 0x03, 0x86, 0x01, 0xfe, 0x01, 0x78, 0x00
};

static const BitmapIcon icon_checkcircle_10 = {
  "checkcircle",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_checkcircle_10_bits
};
