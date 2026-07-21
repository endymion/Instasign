#pragma once
#include "../../IconTypes.h"

// Lucide 'cloud' @ 5px
static const uint8_t icon_cloud_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1e
};

static const BitmapIcon icon_cloud_5 = {
  "cloud",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_cloud_5_bits
};
