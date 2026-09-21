from PIL import Image

try:
    img = Image.open(r"Output_Renders\True3D_ak47_ABSOLUTE_Graffiti_PlaySide.png")
    
    # It's a 1920x1080 (or 2560x1440) image. Let's crop a square from the center.
    width, height = img.size
    min_dim = min(width, height)
    
    left = (width - min_dim) / 2
    top = (height - min_dim) / 2
    right = (width + min_dim) / 2
    bottom = (height + min_dim) / 2
    
    cropped = img.crop((left, top, right, bottom))
    cropped = cropped.resize((256, 256), Image.Resampling.LANCZOS)
    
    cropped.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
    print("Icon generated from AK-47 render!")
except Exception as e:
    print(e)
