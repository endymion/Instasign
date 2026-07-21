#pragma once
#include "../../IconTypes.h"

// Lucide 'trash-2' @ 10px
static const uint8_t icon_trash2_10_bits[20] PROGMEM = {
  0x04, 0x00, 0xfc, 0x01, 0xfc, 0x03, 0xf7, 0x03, 0xf7, 0x03, 0xf7, 0x03, 0xf7, 0x03, 0xfc, 0x03, 0xfc, 0x01, 0x04, 0x00
};

static const BitmapIcon icon_trash2_10 = {
  "trash2",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_trash2_10_bits
};
