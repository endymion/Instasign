#pragma once
#include "../../IconTypes.h"

// Lucide 'calendar' @ 10px
static const uint8_t icon_calendar_10_bits[20] PROGMEM = {
  0xfc, 0x01, 0xfe, 0x03, 0x1e, 0x03, 0x1f, 0x03, 0x1a, 0x03, 0x1a, 0x03, 0x1f, 0x03, 0x1e, 0x03, 0xfe, 0x03, 0xfc, 0x01
};

static const BitmapIcon icon_calendar_10 = {
  "calendar",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_calendar_10_bits
};
