from PIL import ImageFont, ImageDraw, Image
font = ImageFont.truetype("wled/usermods/matrix_display/Tiny5-Regular.ttf", 8)
for char in ['A', 'W', 'i']:
    bbox = font.getbbox(char)
    print(f"--- {char} ---")
    print(f"font.getbbox: {bbox}, width: {bbox[2] - bbox[0]}")
    img = Image.new("1", (8, 8), 0)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), char, font=font, fill=1)
    tight_bbox = img.getbbox()
    print(f"img.getbbox (tight): {tight_bbox}")
    
    for y in range(8):
        row = "".join("#" if img.getpixel((x, y)) else "." for x in range(8))
        print(row)
