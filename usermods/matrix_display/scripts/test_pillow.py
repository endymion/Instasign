from PIL import ImageFont, ImageDraw, Image
font = ImageFont.truetype("wled/usermods/matrix_display/Tiny5-Regular.ttf", 5)
for char in ['i', 'W']:
    bbox = font.getbbox(char)
    # getbbox returns (left, top, right, bottom)
    print(f"'{char}' bbox: {bbox}, width: {bbox[2] - bbox[0]}")
