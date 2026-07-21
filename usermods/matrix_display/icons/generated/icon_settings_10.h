#pragma once
#include "../../IconTypes.h"

// Lucide 'settings' @ 10px
static const uint8_t icon_settings_10_bits[20] PROGMEM = {
  0x48, 0x00, 0xfc, 0x00, 0xb4, 0x00, 0xfe, 0x01, 0xff, 0x03, 0xff, 0x03, 0xfe, 0x01, 0xb4, 0x00, 0xfc, 0x00, 0x48, 0x00
};

static const BitmapIcon icon_settings_10 = {
  "settings",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_settings_10_bits
};
