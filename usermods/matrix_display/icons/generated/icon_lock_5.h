#pragma once
#include "../../IconTypes.h"

// Lucide 'lock' @ 5px
static const uint8_t icon_lock_5_bits[5] PROGMEM = {
  0x1e, 0x1f, 0x17, 0x1f, 0x1f
};

static const BitmapIcon icon_lock_5 = {
  "lock",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_lock_5_bits
};
