import os
import glob

assets_folder = r"c:\Users\Showrav Zaman\My Drive\Giveaway Hunting\SkinClub Contests\Skin Design\Assets"
models_dir = os.path.join(assets_folder, r"Official Resources\CS2 Models")
tex_dir = os.path.join(assets_folder, r"CS2_Weapon\CS2_Weapon")

weapons = []
for obj_file in os.listdir(models_dir):
    if not obj_file.endswith('.obj'): continue
    
    # Extract short name (e.g., 'weapon_rif_ak47.obj' -> 'ak47')
    name_parts = obj_file.replace('.obj', '').split('_')
    short_name = name_parts[-1]
    
    # Some weapons might have different texture naming? Let's search recursively
    search_pattern_norm = os.path.join(tex_dir, "**", f"{short_name}_default_normal*.png")
    search_pattern_rough = os.path.join(tex_dir, "**", f"{short_name}_default_rough*.png")
    
    norms = glob.glob(search_pattern_norm, recursive=True)
    roughs = glob.glob(search_pattern_rough, recursive=True)
    
    if norms and roughs:
        weapons.append(short_name)
    else:
        print(f"Missing textures for: {short_name}")

print(f"Found {len(weapons)} fully complete weapons!")
