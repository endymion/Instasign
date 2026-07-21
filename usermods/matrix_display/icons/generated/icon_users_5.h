#pragma once
#include "../../IconTypes.h"

// Lucide 'users' @ 5px
static const uint8_t icon_users_5_bits[5] PROGMEM = {
  0x1f, 0x0f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_users_5 = {
  "users",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_users_5_bits
};
