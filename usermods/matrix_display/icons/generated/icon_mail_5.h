#pragma once
#include "../../IconTypes.h"

// Lucide 'mail' @ 5px
static const uint8_t icon_mail_5_bits[5] PROGMEM = {
  0x1f, 0x1f, 0x1f, 0x1f, 0x1f
};

static const BitmapIcon icon_mail_5 = {
  "mail",
  5, /* size */
  5, /* width */
  5, /* height */
  1, /* bytesPerColumn */
  icon_mail_5_bits
};
