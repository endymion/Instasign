#pragma once
#include "../../IconTypes.h"

// Lucide 'bookmark' @ 10px
static const uint8_t icon_bookmark_10_bits[20] PROGMEM = {
  0x00, 0x00, 0xfe, 0x01, 0xff, 0x03, 0x83, 0x01, 0x83, 0x01, 0x83, 0x01, 0x83, 0x01, 0xff, 0x03, 0xfe, 0x01, 0x00, 0x00
};

static const BitmapIcon icon_bookmark_10 = {
  "bookmark",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_bookmark_10_bits
};
