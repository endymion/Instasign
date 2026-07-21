#!/usr/bin/env python3
"""Convert a TTF into a PROGMEM BitmapFont C++ header for the matrix display."""

from PIL import ImageFont, ImageDraw, Image
import argparse
import math
import os


def render_glyphs(font, threshold=128):
    """Render ASCII 32-126 into aligned bitmaps.

    Returns (height, glyphs) where glyphs is a list of (width, 2D list [x][y] of 0/1).
    """
    bboxes = {}
    min_top = None
    max_bottom = None
    for i in range(32, 127):
        ch = chr(i)
        bbox = font.getbbox(ch)
        if bbox is None:
            bbox = (0, 0, 1, 1)
        bboxes[ch] = bbox
        left, top, right, bottom = bbox
        if ch == " ":
            continue
        if min_top is None or top < min_top:
            min_top = top
        if max_bottom is None or bottom > max_bottom:
            max_bottom = bottom

    if min_top is None:
        min_top, max_bottom = 0, 8

    height = max(1, max_bottom - min_top)
    glyphs = []
    for i in range(32, 127):
        ch = chr(i)
        left, top, right, bottom = bboxes[ch]
        width = max(1, right - left)
        if ch == " ":
            width = max(2, width)

        img = Image.new("L", (width, height), 0)
        ImageDraw.Draw(img).text((-left, -min_top), ch, font=font, fill=255)

        grid = []
        for x in range(width):
            col = []
            for y in range(height):
                col.append(1 if img.getpixel((x, y)) >= threshold else 0)
            grid.append(col)
        glyphs.append((width, grid))

    return height, glyphs


def downsample_glyphs(height, glyphs, factor):
    """Majority-downsample glyph grids by an integer factor."""
    if factor <= 1:
        return height, glyphs

    new_height = max(1, (height + factor - 1) // factor)
    out = []
    for width, grid in glyphs:
        new_width = max(1, (width + factor - 1) // factor)
        new_grid = []
        for nx in range(new_width):
            col = []
            for ny in range(new_height):
                on = 0
                total = 0
                for dx in range(factor):
                    for dy in range(factor):
                        x = nx * factor + dx
                        y = ny * factor + dy
                        if x < width and y < height:
                            total += 1
                            on += grid[x][y]
                col.append(1 if total and on * 2 >= total else 0)
            new_grid.append(col)
        out.append((new_width, new_grid))
    return new_height, out


def pack_columns(height, glyphs):
    bytes_per_col = math.ceil(height / 8)
    max_width = max(w for w, _ in glyphs)
    packed = []
    for width, grid in glyphs:
        columns = []
        for x in range(width):
            col_bytes = [0] * bytes_per_col
            for y in range(height):
                if grid[x][y]:
                    col_bytes[y // 8] |= 1 << (y % 8)
            columns.append(col_bytes)
        packed.append((width, columns))
    return bytes_per_col, max_width, packed


def generate_header(ttf_path, font_size, output_path, array_name, display_name, threshold=128, downsample=1):
    font = ImageFont.truetype(ttf_path, font_size)
    height, glyphs = render_glyphs(font, threshold=threshold)
    height, glyphs = downsample_glyphs(height, glyphs, downsample)
    bytes_per_col, max_width, packed = pack_columns(height, glyphs)
    default_line_height = height + 1

    with open(output_path, "w") as f:
        f.write("#pragma once\n")
        f.write('#include "FontTypes.h"\n\n')
        f.write(f"// Generated from {os.path.basename(ttf_path)} @ {font_size}px")
        if downsample > 1:
            f.write(f", downsampled {downsample}x")
        f.write(f"\n// Display name: {display_name}\n")

        f.write(f"static const uint8_t {array_name}_widths[95] PROGMEM = {{\n  ")
        f.write(", ".join(str(w) for w, _ in packed))
        f.write("\n};\n\n")

        f.write(
            f"static const uint8_t {array_name}_bitmaps[95 * {max_width} * {bytes_per_col}] PROGMEM = {{\n"
        )
        for idx, (width, columns) in enumerate(packed):
            ch = chr(idx + 32)
            flat = []
            for col in range(max_width):
                if col < width:
                    flat.extend(f"0x{b:02x}" for b in columns[col])
                else:
                    flat.extend(["0x00"] * bytes_per_col)
            f.write(f"  {', '.join(flat)}, // {idx + 32} '{ch}' w={width}\n")
        f.write("};\n\n")

        f.write(f"static const BitmapFont {array_name} = {{\n")
        f.write(f'  "{display_name}",\n')
        f.write(f"  {height}, /* height */\n")
        f.write(f"  {default_line_height}, /* defaultLineHeight */\n")
        f.write(f"  {bytes_per_col}, /* bytesPerColumn */\n")
        f.write(f"  {max_width}, /* maxWidth */\n")
        f.write(f"  {array_name}_widths,\n")
        f.write(f"  {array_name}_bitmaps\n")
        f.write("};\n")

    print(
        f"Generated {output_path}: height={height} maxWidth={max_width} "
        f"bpc={bytes_per_col} lineHeight={default_line_height} downsample={downsample}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert TTF to BitmapFont header")
    parser.add_argument("ttf_file")
    parser.add_argument("size", type=int)
    parser.add_argument("output")
    parser.add_argument("array_name")
    parser.add_argument("display_name")
    parser.add_argument("--threshold", type=int, default=128)
    parser.add_argument("--downsample", type=int, default=1)
    args = parser.parse_args()
    generate_header(
        args.ttf_file,
        args.size,
        args.output,
        args.array_name,
        args.display_name,
        args.threshold,
        args.downsample,
    )
