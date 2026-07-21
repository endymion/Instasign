#pragma once
#include "../../IconTypes.h"

// Lucide 'mail' @ 10px
static const uint8_t icon_mail_10_bits[20] PROGMEM = {
  0xfe, 0x01, 0xfe, 0x01, 0x1a, 0x01, 0x3a, 0x01, 0x32, 0x01, 0x32, 0x01, 0x3a, 0x01, 0x1a, 0x01, 0xfe, 0x01, 0xfe, 0x01
};

static const BitmapIcon icon_mail_10 = {
  "mail",
  10, /* size */
  10, /* width */
  10, /* height */
  2, /* bytesPerColumn */
  icon_mail_10_bits
};
