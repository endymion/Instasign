#pragma once
#include "wled.h"
#include "Animation.h"

class Scene {
  public:
    virtual ~Scene() {}
    virtual void draw(WS2812FX& strip, const SceneTime& time) = 0;
    virtual void updateParams(JsonObject params) = 0;
};
