#pragma once
#include "../../IconTypes.h"

// Lucide 'users' @ 10px
static const uint8_t icon_users_10_bits[20] PROGMEM = {
  0xc0, 0x03, 0xcc, 0x01, 0x7e, 0x00, 0x73, 0x00, 0x7f, 0x00, 0x7e, 0x00, 0xd3, 0x03, 0x7e, 0x00, 0xcc, 0x01, 0xc0, 0x03
};

static const BitmapIcon icon_users_10 = {
  "users",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_users_10_bits
};
