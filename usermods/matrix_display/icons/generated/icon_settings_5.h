#pragma once
#include "../../IconTypes.h"

// Lucide 'settings' @ 5px
static const uint8_t icon_settings_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_settings_5 = {
  "settings",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_settings_5_bits
};
