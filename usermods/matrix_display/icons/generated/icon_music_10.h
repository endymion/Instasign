#pragma once
#include "../../IconTypes.h"

// Lucide 'music' @ 10px
static const uint8_t icon_music_10_bits[20] PROGMEM = {
  0x80, 0x00, 0xc0, 0x01, 0x60, 0x03, 0xfe, 0x01, 0xfe, 0x00, 0xc6, 0x00, 0xe6, 0x01, 0xa2, 0x01, 0xff, 0x01, 0xfe, 0x00
};

static const BitmapIcon icon_music_10 = {
  "music",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_music_10_bits
};
