#!/usr/bin/env python3
"""Rasterize curated Lucide SVGs into PROGMEM BitmapIcon C++ headers.

Sizes: 5, 10, 15, 25 (matching Soft Type / pixel font scale).
"""

from __future__ import annotations

import argparse
import io
import math
import os
import re
from pathlib import Path

import cairosvg
from PIL import Image

SIZES = (5, 10, 15, 25)


def normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def prepare_svg(svg_text: str, stroke_width: float) -> str:
    """Force opaque black strokes sized for the target pixel grid."""
    # Strip width/height attributes that fight our output size; keep viewBox.
    svg_text = re.sub(r'\s(width|height)="[^"]*"', "", svg_text, count=2)
    # Ensure root has explicit stroke defaults.
    if "stroke=" not in svg_text.split(">", 1)[0]:
        svg_text = svg_text.replace(
            "<svg",
            f'<svg stroke="#000000" fill="none" stroke-width="{stroke_width:.3f}" '
            f'stroke-linecap="round" stroke-linejoin="round"',
            1,
        )
    else:
        svg_text = re.sub(
            r'stroke-width="[^"]*"',
            f'stroke-width="{stroke_width:.3f}"',
            svg_text,
            count=1,
        )
        svg_text = re.sub(r'stroke="[^"]*"', 'stroke="#000000"', svg_text, count=1)
    # currentColor → black
    svg_text = svg_text.replace("currentColor", "#000000")
    return svg_text


def rasterize_icon(svg_path: Path, size: int, threshold: int = 64) -> Image.Image:
    """Render Lucide SVG to a size×size 1-bit image.

    Stroke width is chosen so strokes land near ~1px after downsampling.
    Render at 4× then OR-downsample so thin features survive.
    """
    # Lucide viewBox is 24×24; target ~1px strokes in final bitmap.
    stroke_width = 24.0 / max(size, 1)
    # Slightly thicker at the tiniest size so icons remain readable.
    if size <= 5:
        stroke_width *= 1.25

    svg_text = prepare_svg(svg_path.read_text(encoding="utf-8"), stroke_width)
    render_size = max(size * 4, 32)

    png = cairosvg.svg2png(
        bytestring=svg_text.encode("utf-8"),
        output_width=render_size,
        output_height=render_size,
        background_color="white",
    )
    img = Image.open(io.BytesIO(png)).convert("L")

    # OR-downsample to size×size
    out = Image.new("1", (size, size), 0)
    factor = render_size / size
    for y in range(size):
        for x in range(size):
            x0 = int(x * factor)
            y0 = int(y * factor)
            x1 = int((x + 1) * factor)
            y1 = int((y + 1) * factor)
            block = img.crop((x0, y0, max(x1, x0 + 1), max(y1, y0 + 1)))
            # Dark ink on white bg
            if any(p < threshold for p in block.getdata()):
                out.putpixel((x, y), 1)
    return out


def pack_bitmap(img: Image.Image) -> tuple[int, int, int, list[int]]:
    """Column-major pack matching BitmapFont layout."""
    width, height = img.size
    bytes_per_col = math.ceil(height / 8)
    data = []
    for x in range(width):
        col_bytes = [0] * bytes_per_col
        for y in range(height):
            if img.getpixel((x, y)):
                col_bytes[y // 8] |= 1 << (y % 8)
        data.extend(col_bytes)
    return width, height, bytes_per_col, data


def c_ident(name: str, size: int) -> str:
    ident = normalize_name(name)
    if ident[0].isdigit():
        ident = "i" + ident
    return f"icon_{ident}_{size}"


def write_icon_header(out_path: Path, name: str, size: int, img: Image.Image) -> str:
    width, height, bpc, data = pack_bitmap(img)
    ident = c_ident(name, size)
    canon = normalize_name(name)

    lines = [
        "#pragma once",
        '#include "../../IconTypes.h"',
        "",
        f"// Lucide '{name}' @ {size}px",
        f"static const uint8_t {ident}_bits[{width * bpc}] PROGMEM = {{",
        "  " + ", ".join(f"0x{b:02x}" for b in data),
        "};",
        "",
        f"static const BitmapIcon {ident} = {{",
        f'  "{canon}",',
        f"  {size}, /* size */",
        f"  {width}, /* width */",
        f"  {height}, /* height */",
        f"  {bpc}, /* bytesPerColumn */",
        f"  {ident}_bits",
        "};",
        "",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return ident


def write_registry(out_path: Path, entries: list[tuple[str, int, str]]) -> None:
    """entries: (canonical_name, size, c_ident)"""
    includes = sorted({f'#include "icons/generated/{ident}.h"' for _, _, ident in entries})
    lines = [
        "#pragma once",
        "#include <Arduino.h>",
        '#include "IconTypes.h"',
        *includes,
        "",
        "inline String normalizeIconName(const String& name) {",
        "  String out;",
        "  out.reserve(name.length());",
        "  for (unsigned i = 0; i < name.length(); i++) {",
        "    char c = name.charAt(i);",
        "    if (c == ' ' || c == '\\t' || c == '\\n' || c == '\\r' || c == '-' || c == '_') continue;",
        "    if (c >= 'A' && c <= 'Z') c = c - 'A' + 'a';",
        "    out += c;",
        "  }",
        "  return out;",
        "}",
        "",
        "inline const BitmapIcon* findIcon(const String& name, uint8_t size) {",
        "  String key = normalizeIconName(name);",
        "  if (key.length() == 0) return nullptr;",
        "  // Prefer exact size; fall back to nearest available size for that icon.",
        "",
    ]

    # Group by canonical name
    by_name: dict[str, list[tuple[int, str]]] = {}
    for canon, size, ident in entries:
        by_name.setdefault(canon, []).append((size, ident))

    for canon in sorted(by_name.keys()):
        sizes = sorted(by_name[canon], key=lambda t: t[0])
        lines.append(f'  if (key == "{canon}") {{')
        # exact match
        for size, ident in sizes:
            lines.append(f"    if (size == {size}) return &{ident};")
        # nearest fallback
        lines.append("    // nearest size fallback")
        lines.append("    const BitmapIcon* best = nullptr;")
        lines.append("    int bestDist = 1000;")
        for size, ident in sizes:
            lines.append(f"    {{ int d = (int)size - (int){size}; if (d < 0) d = -d;")
            lines.append(f"      if (d < bestDist) {{ bestDist = d; best = &{ident}; }} }}")
        lines.append("    return best;")
        lines.append("  }")

    lines += [
        '  Serial.printf("UsermodMatrixDisplay: Unknown icon \'%s\'\\n", name.c_str());',
        "  return nullptr;",
        "}",
        "",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--svg-dir",
        type=Path,
        default=Path(__file__).parent / "icons" / "svg",
    )
    parser.add_argument(
        "--allowlist",
        type=Path,
        default=Path(__file__).parent / "icons" / "allowlist.txt",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).parent / "icons" / "generated",
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path(__file__).parent / "IconRegistry.h",
    )
    args = parser.parse_args()

    names = [
        line.strip()
        for line in args.allowlist.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    entries: list[tuple[str, int, str]] = []

    for name in names:
        svg_path = args.svg_dir / f"{name}.svg"
        if not svg_path.exists():
            print(f"WARN: missing SVG for {name}, skipping")
            continue
        for size in SIZES:
            img = rasterize_icon(svg_path, size)
            ident = c_ident(name, size)
            out = args.out_dir / f"{ident}.h"
            write_icon_header(out, name, size, img)
            entries.append((normalize_name(name), size, ident))
            print(f"Generated {out.name} ({img.size[0]}x{img.size[1]})")

    write_registry(args.registry, entries)
    print(f"Wrote registry {args.registry} with {len(entries)} icon bitmaps")


if __name__ == "__main__":
    main()
