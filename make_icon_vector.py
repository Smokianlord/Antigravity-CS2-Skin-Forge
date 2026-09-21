from PIL import Image, ImageDraw

# Create a sleek dark background
img = Image.new('RGBA', (256, 256), (20, 20, 24, 255))
d = ImageDraw.Draw(img)

# Draw a stylized glowing red/orange gradient or crosshair
# Outer circle
d.ellipse([32, 32, 224, 224], outline=(255, 80, 80, 255), width=8)

# Stylized gun silhouette (AK-like)
gun_color = (200, 200, 200, 255)
# Barrel
d.rectangle([140, 110, 220, 120], fill=gun_color)
# Receiver
d.rectangle([80, 105, 140, 130], fill=gun_color)
# Magazine
d.polygon([(100, 130), (120, 130), (110, 160), (90, 160)], fill=gun_color)
# Stock
d.polygon([(80, 105), (80, 130), (40, 135), (40, 115)], fill=gun_color)
# Grip
d.polygon([(80, 130), (90, 130), (85, 150), (75, 150)], fill=gun_color)

# Add some techy details
d.line([(32, 128), (12, 128)], fill=(255, 80, 80, 255), width=4)
d.line([(224, 128), (244, 128)], fill=(255, 80, 80, 255), width=4)
d.line([(128, 32), (128, 12)], fill=(255, 80, 80, 255), width=4)
d.line([(128, 224), (128, 244)], fill=(255, 80, 80, 255), width=4)

img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
