#pragma once
#include "wled.h"

// Logical drawing surface for matrix_display scenes.
// Sized from WLED's 2D matrix config when available; pixel addressing uses
// this canvas width as the row stride (same model as the old hardcoded 64),
// not Segment::setPixelColorXY — which is segment-relative and can disagree
// with overlay drawing on HUB75.
struct MatrixCanvas {
  int w = 64;
  int h = 64;

  static MatrixCanvas fromStrip(WS2812FX& strip) {
    MatrixCanvas c;
    const int mw = (int)Segment::maxWidth;
    const int mh = (int)Segment::maxHeight;
    const unsigned total = strip.getLengthTotal();

    if (strip.isMatrix && mw > 1 && mh > 1 && (unsigned)mw * (unsigned)mh <= total) {
      c.w = mw;
      c.h = mh;
    } else if (total >= 64 * 64 && total % 64 == 0) {
      // Common Instasign / HUB75 bring-up: width 64, height = count/64
      c.w = 64;
      c.h = (int)(total / 64);
    } else {
      c.w = 64;
      c.h = 64;
    }
    if (c.w < 1) c.w = 1;
    if (c.h < 1) c.h = 1;
    return c;
  }

  unsigned length() const { return (unsigned)w * (unsigned)h; }

  bool contains(int x, int y) const {
    return x >= 0 && x < w && y >= 0 && y < h;
  }

  // Absolute framebuffer index for (x,y) on this canvas.
  unsigned index(int x, int y) const {
    return (unsigned)y * (unsigned)w + (unsigned)x;
  }

  void setPixel(WS2812FX& strip, int x, int y, uint32_t color) const {
    if (!contains(x, y)) return;
    strip.setPixelColor(index(x, y), color);
  }

  void clear(WS2812FX& strip, uint32_t color = 0) const {
    const unsigned n = length();
    const unsigned lim = strip.getLengthTotal();
    const unsigned count = n < lim ? n : lim;
    for (unsigned i = 0; i < count; i++) {
      strip.setPixelColor(i, color);
    }
  }

  void fillRect(WS2812FX& strip, int x, int y, int rw, int rh, uint32_t color) const {
    if (rw <= 0 || rh <= 0) return;
    const int x1 = x + rw;
    const int y1 = y + rh;
    for (int py = y; py < y1; py++) {
      if (py < 0 || py >= h) continue;
      for (int px = x; px < x1; px++) {
        if (px < 0 || px >= w) continue;
        strip.setPixelColor(index(px, py), color);
      }
    }
  }
};
