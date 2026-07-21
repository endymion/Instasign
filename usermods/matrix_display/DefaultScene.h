#pragma once
#include "Scene.h"

// Idle scene: full-panel black so WLED's underlying effect never shows.
class DefaultScene : public Scene {
  public:
    void draw(WS2812FX& strip, const SceneTime& time) override {
      (void)time;
      for (unsigned i = 0; i < 4096; i++) {
        strip.setPixelColor(i, 0);
      }
    }

    void updateParams(JsonObject params) override {
      (void)params;
    }
};
