#pragma once
#include "../../IconTypes.h"

// Lucide 'circle-help' @ 10px
static const uint8_t icon_circlehelp_10_bits[20] PROGMEM = {
  0x78, 0x00, 0xfe, 0x01, 0x86, 0x01, 0x1f, 0x03, 0xef, 0x03, 0xff, 0x03, 0x3b, 0x03, 0x86, 0x01, 0xfe, 0x01, 0x78, 0x00
};

static const BitmapIcon icon_circlehelp_10 = {
  "circlehelp",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_circlehelp_10_bits
};
