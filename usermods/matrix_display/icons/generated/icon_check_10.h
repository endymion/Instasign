#pragma once
#include "../../IconTypes.h"

// Lucide 'check' @ 10px
static const uint8_t icon_check_10_bits[20] PROGMEM = {
  0x00, 0x00, 0x30, 0x00, 0x70, 0x00, 0xe0, 0x00, 0xe0, 0x00, 0x70, 0x00, 0x38, 0x00, 0x1c, 0x00, 0x0c, 0x00, 0x00, 0x00
};

static const BitmapIcon icon_check_10 = {
  "check",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_check_10_bits
};
