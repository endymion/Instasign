#pragma once
#include "../../IconTypes.h"

// Lucide 'calendar' @ 5px
static const uint8_t icon_calendar_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x17, 0x1f, 0x1f
};

static const BitmapIcon icon_calendar_5 = {
  "calendar",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_calendar_5_bits
};
