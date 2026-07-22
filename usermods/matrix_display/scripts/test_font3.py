from PIL import ImageFont, ImageDraw, Image
font = ImageFont.truetype("wled/usermods/matrix_display/Tiny5-Regular.ttf", 8)
for char in ['A', '!', 'i', 'W']:
    bbox = font.getbbox(char)
    print(f"'{char}' bbox: {bbox}")
    img = Image.new("1", (8, 8), 0)
    draw = ImageDraw.Draw(img)
    draw.text((0, -2), char, font=font, fill=1)
    for y in range(8):
        row = ""
        for x in range(8):
            row += "#" if img.getpixel((x, y)) else "."
        print(row)
