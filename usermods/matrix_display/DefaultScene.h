#pragma once
#include "Scene.h"
#include "MatrixCanvas.h"

// Idle scene: full-panel black so WLED's underlying effect never shows.
class DefaultScene : public Scene {
  public:
    void draw(WS2812FX& strip, const SceneTime& time) override {
      (void)time;
      MatrixCanvas::fromStrip(strip).clear(strip, 0);
    }

    void updateParams(JsonObject params) override {
      (void)params;
    }
};
