#pragma once
#include "../../IconTypes.h"

// Lucide 'cloud' @ 10px
static const uint8_t icon_cloud_10_bits[20] PROGMEM = {
  0x78, 0x00, 0xfc, 0x00, 0xce, 0x01, 0x86, 0x01, 0x86, 0x01, 0x8c, 0x01, 0x9c, 0x01, 0x98, 0x01, 0xf0, 0x01, 0xf0, 0x00
};

static const BitmapIcon icon_cloud_10 = {
  "cloud",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_cloud_10_bits
};
