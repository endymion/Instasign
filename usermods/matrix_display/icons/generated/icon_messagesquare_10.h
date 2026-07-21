#pragma once
#include "../../IconTypes.h"

// Lucide 'message-square' @ 10px
static const uint8_t icon_messagesquare_10_bits[20] PROGMEM = {
  0xfe, 0x03, 0xff, 0x03, 0x83, 0x01, 0x83, 0x01, 0x83, 0x01, 0x83, 0x01, 0x83, 0x01, 0x83, 0x01, 0xff, 0x01, 0xfe, 0x00
};

static const BitmapIcon icon_messagesquare_10 = {
  "messagesquare",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_messagesquare_10_bits
};
