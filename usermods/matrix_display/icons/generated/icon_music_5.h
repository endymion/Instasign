#pragma once
#include "../../IconTypes.h"

// Lucide 'music' @ 5px
static const uint8_t icon_music_5_bits[5] PROGMEM = {
  0x1c, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_music_5 = {
  "music",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_music_5_bits
};
