#pragma once
#include "../../IconTypes.h"

// Lucide 'circle-help' @ 5px
static const uint8_t icon_circlehelp_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_circlehelp_5 = {
  "circlehelp",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_circlehelp_5_bits
};
