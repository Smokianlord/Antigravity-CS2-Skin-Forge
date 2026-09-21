from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGBA', (256, 256), (30, 30, 36, 255))
d = ImageDraw.Draw(img)

# Draw a sleek abstract geometry (e.g. a crosshair or minimalist gun shape)
d.rectangle([96, 64, 160, 192], fill=(255, 100, 100, 255))
d.rectangle([64, 128, 192, 160], fill=(255, 100, 100, 255))
d.ellipse([64, 64, 192, 192], outline=(200, 200, 200, 255), width=8)

img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
