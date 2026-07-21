#pragma once
#include "../../IconTypes.h"

// Lucide 'zap' @ 5px
static const uint8_t icon_zap_5_bits[5] PROGMEM = {
  0x0e, 0x1f, 0x1f, 0x1f, 0x0e
};

static const BitmapIcon icon_zap_5 = {
  "zap",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_zap_5_bits
};
