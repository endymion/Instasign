#pragma once
#include "../../IconTypes.h"

// Lucide 'door-closed' @ 5px
static const uint8_t icon_doorclosed_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_doorclosed_5 = {
  "doorclosed",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_doorclosed_5_bits
};
