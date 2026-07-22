from PIL import ImageFont, ImageDraw, Image
for sz in [5, 6, 7, 8, 10]:
    print(f"--- Size {sz} ---")
    font = ImageFont.truetype("wled/usermods/matrix_display/Tiny5-Regular.ttf", sz)
    char = 'A'
    bbox = font.getbbox(char)
    print(f"bbox: {bbox}")
    img = Image.new("1", (8, 12), 0)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), char, font=font, fill=1)
    for y in range(8):
        row = ""
        for x in range(8):
            row += "#" if img.getpixel((x, y)) else "."
        print(row)
