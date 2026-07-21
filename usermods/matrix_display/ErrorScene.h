#pragma once
#include "Scene.h"
#include "Typography.h"
#include "Animation.h"
#include "FontRegistry.h"
#include "Icons.h"
#include "MatrixCanvas.h"

// Compact alert screen: Pixeloid title + Tiny5 body + Lucide icon, red palette.
class ErrorScene : public Scene {
  private:
    String title = "ERROR";
    String message = "Something went wrong.";
    uint32_t titleColor = RGBW32(255, 70, 70, 0);   // Red
    uint32_t messageColor = RGBW32(255, 200, 200, 0); // Light red

    int titlePaddingTop = 0;
    int titlePaddingBottom = 2; // blank rows under icon/title before HR (+ body follows)
    int separatorHeight = 1;
    int messagePaddingTop = 0;
    int messagePaddingSides = 1;
    int lineHeight = 0;
    int titleLineHeight = 0;
    int messageLineHeight = 0; // Tiny5 default line height

    const BitmapFont* titleFont = &font_pixeloid;
    const BitmapFont* messageFont = &font_tiny5;
    uint8_t titleScale = 1;
    uint8_t messageScale = 1;

    const BitmapIcon* icon = nullptr;
    uint8_t iconSize = 10;
    int iconPadding = 2;
    uint32_t iconColor = RGBW32(255, 70, 70, 0);

    uint32_t backgroundColor = RGBW32(0, 0, 0, 0);
    uint32_t titleBackgroundColor = RGBW32(0, 0, 0, 0);
    uint32_t messageBackgroundColor = RGBW32(32, 8, 8, 0); // Cool dark red

    uint32_t separatorBrightColor = RGBW32(255, 50, 50, 0);
    uint32_t separatorDimColor = RGBW32(60, 12, 12, 0);
    unsigned long separatorAnimStart = 0;
    unsigned long separatorAnimDuration = 0;

    static uint32_t colorFromJson(JsonArray c, uint32_t fallback) {
      if (c.size() >= 3) return RGBW32(c[0], c[1], c[2], 0);
      return fallback;
    }

    int effectiveTitleLineHeight() const {
      if (titleLineHeight > 0) return titleLineHeight;
      if (lineHeight > 0) return lineHeight;
      return Typography::scaledLineHeight(titleFont, titleScale);
    }

    int effectiveMessageLineHeight() const {
      if (messageLineHeight > 0) return messageLineHeight;
      if (lineHeight > 0) return lineHeight;
      return Typography::scaledLineHeight(messageFont, messageScale);
    }

    void drawSeparatorProgress(WS2812FX& strip, const MatrixCanvas& canvas, int y, const SceneTime& time) {
      if (separatorHeight <= 0) return;

      float progress = animationProgress(time, separatorAnimStart, separatorAnimDuration);
      int wipeX = (int)(progress * (float)canvas.w + 0.5f);
      if (wipeX < 0) wipeX = 0;
      if (wipeX > canvas.w) wipeX = canvas.w;

      if (wipeX > 0) {
        canvas.fillRect(strip, 0, y, wipeX, separatorHeight, separatorDimColor);
      }
      if (wipeX < canvas.w) {
        canvas.fillRect(strip, wipeX, y, canvas.w - wipeX, separatorHeight, separatorBrightColor);
      }
    }

  public:
    ErrorScene() {
      icon = findIcon("alert-octagon", iconSize);
    }

    void draw(WS2812FX& strip, const SceneTime& time) override {
      const MatrixCanvas canvas = MatrixCanvas::fromStrip(strip);
      canvas.clear(strip, backgroundColor);

      const int titleLH = effectiveTitleLineHeight();
      const int messageLH = effectiveMessageLineHeight();
      int cursorY = titlePaddingTop;

      const int iconW = icon ? icon->width : 0;
      const int iconH = icon ? icon->height : 0;
      const int titleX = icon ? (1 + iconW + iconPadding) : 0;
      const int titleMaxW = canvas.w - titleX;
      const int titleInkH = title.length()
        ? Typography::measureBlockInkHeight(titleFont, title, titleMaxW, titleLH, titleScale)
        : 0;
      const int headerH = titleInkH > iconH ? titleInkH : iconH;

      if (headerH > 0 && titleBackgroundColor != backgroundColor) {
        canvas.fillRect(strip, 0, cursorY, canvas.w, headerH, titleBackgroundColor);
      }

      int titleY = cursorY;
      if (title.length() && titleMaxW > 0) {
        titleY = cursorY + (headerH - titleInkH) / 2;
        if (titleY < cursorY) titleY = cursorY;
      }

      if (icon) {
        int iconY = cursorY + (headerH - iconH) / 2;
        if (title.length()) {
          const int inkTop = Typography::measureInkTop(titleFont, title, titleScale);
          const int inkBottom = Typography::measureInkHeight(titleFont, title, titleScale);
          if (inkBottom > inkTop) {
            iconY = titleY + (inkTop + inkBottom - iconH) / 2;
          }
        }
        if (iconY < cursorY) iconY = cursorY;
        Icons::drawIcon(strip, canvas, icon, 1, iconY, iconColor);
      }

      if (title.length() && titleMaxW > 0) {
        Typography::drawText(strip, canvas, titleFont, title, titleX, titleY, titleMaxW, titleLH,
                             ALIGN_CENTER, titleColor, titleScale);
      }

      if (headerH > 0) {
        cursorY += headerH + titlePaddingBottom;
      }

      if (separatorHeight > 0) {
        drawSeparatorProgress(strip, canvas, cursorY, time);
        cursorY += separatorHeight;
      }

      cursorY += messagePaddingTop;

      int maxMessageWidth = canvas.w - (messagePaddingSides * 2);
      int messageHeight = Typography::measureTextBackgroundHeight(messageFont, message, maxMessageWidth, messageLH, messageScale);

      if (messageBackgroundColor != backgroundColor) {
        canvas.fillRect(strip, 0, cursorY, canvas.w, messageHeight, messageBackgroundColor);
      }

      Typography::drawText(strip, canvas, messageFont, message, messagePaddingSides, cursorY,
                           maxMessageWidth, messageLH, ALIGN_LEFT, messageColor, messageScale);
    }

    void updateParams(JsonObject params) override {
      if (params.containsKey("title")) title = params["title"].as<String>();
      if (params.containsKey("message")) message = params["message"].as<String>();

      if (params.containsKey("titlePaddingTop")) titlePaddingTop = params["titlePaddingTop"].as<int>();
      if (params.containsKey("titlePaddingBottom")) titlePaddingBottom = params["titlePaddingBottom"].as<int>();
      if (params.containsKey("messagePaddingTop")) messagePaddingTop = params["messagePaddingTop"].as<int>();
      if (params.containsKey("messagePaddingSides")) messagePaddingSides = params["messagePaddingSides"].as<int>();
      if (params.containsKey("separatorHeight")) separatorHeight = params["separatorHeight"].as<int>();

      if (params.containsKey("lineHeight")) lineHeight = params["lineHeight"].as<int>();
      if (params.containsKey("titleLineHeight")) titleLineHeight = params["titleLineHeight"].as<int>();
      if (params.containsKey("messageLineHeight")) messageLineHeight = params["messageLineHeight"].as<int>();

      // Defaults stay Pixeloid title / Tiny5 message unless explicitly overridden.
      if (params.containsKey("font")) {
        const BitmapFont* font = findFontByName(params["font"].as<String>());
        titleFont = font;
        messageFont = font;
      }
      if (params.containsKey("titleFont")) {
        titleFont = findFontByName(params["titleFont"].as<String>());
      }
      if (params.containsKey("messageFont")) {
        messageFont = findFontByName(params["messageFont"].as<String>());
      }

      if (params.containsKey("scale")) {
        uint8_t s = params["scale"].as<uint8_t>();
        if (s < 1) s = 1;
        titleScale = s;
        messageScale = s;
      }
      if (params.containsKey("titleScale")) {
        uint8_t s = params["titleScale"].as<uint8_t>();
        titleScale = s < 1 ? 1 : s;
      }
      if (params.containsKey("messageScale")) {
        uint8_t s = params["messageScale"].as<uint8_t>();
        messageScale = s < 1 ? 1 : s;
      }

      if (params.containsKey("iconSize")) {
        iconSize = params["iconSize"].as<uint8_t>();
      }
      if (params.containsKey("iconPadding")) {
        iconPadding = params["iconPadding"].as<int>();
      }
      if (params.containsKey("iconColor")) {
        iconColor = colorFromJson(params["iconColor"].as<JsonArray>(), iconColor);
      }
      if (params.containsKey("icon")) {
        String iconName = params["icon"].as<String>();
        if (iconName.length() == 0) {
          icon = nullptr;
        } else {
          icon = findIcon(iconName, iconSize);
        }
      } else if (params.containsKey("iconSize")) {
        // Keep error icon family; re-resolve at new size.
        const char* name = icon ? icon->name : "alert-octagon";
        icon = findIcon(name, iconSize);
      }

      if (params.containsKey("titleColor")) {
        titleColor = colorFromJson(params["titleColor"].as<JsonArray>(), titleColor);
      }
      if (params.containsKey("messageColor")) {
        messageColor = colorFromJson(params["messageColor"].as<JsonArray>(), messageColor);
      }
      if (params.containsKey("messageBackgroundColor")) {
        messageBackgroundColor = colorFromJson(params["messageBackgroundColor"].as<JsonArray>(), messageBackgroundColor);
      }
      if (params.containsKey("titleBackgroundColor")) {
        titleBackgroundColor = colorFromJson(params["titleBackgroundColor"].as<JsonArray>(), titleBackgroundColor);
      }
      if (params.containsKey("backgroundColor")) {
        backgroundColor = colorFromJson(params["backgroundColor"].as<JsonArray>(), backgroundColor);
      }

      if (params.containsKey("separatorBrightColor")) {
        separatorBrightColor = colorFromJson(params["separatorBrightColor"].as<JsonArray>(), separatorBrightColor);
      }
      if (params.containsKey("separatorDimColor")) {
        separatorDimColor = colorFromJson(params["separatorDimColor"].as<JsonArray>(), separatorDimColor);
      }
      if (params.containsKey("separatorAnimStart")) {
        separatorAnimStart = params["separatorAnimStart"].as<unsigned long>();
      }
      if (params.containsKey("separatorAnimDuration")) {
        separatorAnimDuration = params["separatorAnimDuration"].as<unsigned long>();
      }

      JsonObject sep = params["separator"];
      if (!sep.isNull()) {
        if (sep.containsKey("height")) separatorHeight = sep["height"].as<int>();
        if (sep.containsKey("brightColor")) {
          separatorBrightColor = colorFromJson(sep["brightColor"].as<JsonArray>(), separatorBrightColor);
        }
        if (sep.containsKey("dimColor")) {
          separatorDimColor = colorFromJson(sep["dimColor"].as<JsonArray>(), separatorDimColor);
        }
        if (sep.containsKey("animStart")) {
          separatorAnimStart = sep["animStart"].as<unsigned long>();
        }
        if (sep.containsKey("animDuration")) {
          separatorAnimDuration = sep["animDuration"].as<unsigned long>();
        }
      }
    }
};
