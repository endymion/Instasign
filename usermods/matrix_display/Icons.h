#pragma once
#include <Arduino.h>
#include "FX.h"
#include "IconTypes.h"
#include "IconRegistry.h"

class Icons {
public:
  // Draw icon with top-left at (x,y). Returns width drawn (0 if null).
  static int drawIcon(WS2812FX& strip, const BitmapIcon* icon, int x, int y, uint32_t color) {
    if (!icon || !icon->bits) return 0;

    for (uint8_t col = 0; col < icon->width; col++) {
      for (uint8_t b = 0; b < icon->bytesPerColumn; b++) {
        uint8_t bits = pgm_read_byte(&icon->bits[col * icon->bytesPerColumn + b]);
        for (uint8_t bit = 0; bit < 8; bit++) {
          int srcY = (int)b * 8 + bit;
          if (srcY >= icon->height || !(bits & (1 << bit))) continue;
          int px = x + col;
          int py = y + srcY;
          if (px >= 0 && px < 64 && py >= 0 && py < 64) {
            strip.setPixelColor((unsigned)(py * 64 + px), color);
          }
        }
      }
    }
    return icon->width;
  }
};
