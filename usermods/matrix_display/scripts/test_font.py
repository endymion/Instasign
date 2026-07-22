from PIL import ImageFont, ImageDraw, Image
font = ImageFont.truetype("wled/usermods/matrix_display/Tiny5-Regular.ttf", 5)
char = 'A'
bbox = font.getbbox(char)
print(f"bbox: {bbox}")
img = Image.new("1", (8, 8), 0)
draw = ImageDraw.Draw(img)
draw.text((-bbox[0], 0), char, font=font, fill=1)
for y in range(8):
    row = ""
    for x in range(8):
        row += "#" if img.getpixel((x, y)) else "."
    print(row)
