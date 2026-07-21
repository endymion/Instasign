#pragma once
#include "../../IconTypes.h"

// Lucide 'door-closed' @ 10px
static const uint8_t icon_doorclosed_10_bits[20] PROGMEM = {
  0x00, 0x01, 0x00, 0x01, 0xfe, 0x01, 0x36, 0x01, 0x32, 0x01, 0x02, 0x01, 0x06, 0x01, 0xfe, 0x01, 0x00, 0x01, 0x00, 0x01
};

static const BitmapIcon icon_doorclosed_10 = {
  "doorclosed",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_doorclosed_10_bits
};
