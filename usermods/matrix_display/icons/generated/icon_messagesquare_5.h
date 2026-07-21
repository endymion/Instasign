#pragma once
#include "../../IconTypes.h"

// Lucide 'message-square' @ 5px
static const uint8_t icon_messagesquare_5_bits[5] PROGMEM = {
  0x1f, 0x1b, 0x1b, 0x1b, 0x1f
};

static const BitmapIcon icon_messagesquare_5 = {
  "messagesquare",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_messagesquare_5_bits
};
