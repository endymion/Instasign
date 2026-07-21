#pragma once
#include "../../IconTypes.h"

// Lucide 'trash-2' @ 5px
static const uint8_t icon_trash2_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_trash2_5 = {
  "trash2",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_trash2_5_bits
};
