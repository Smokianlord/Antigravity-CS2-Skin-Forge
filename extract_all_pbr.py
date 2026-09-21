import os
import subprocess
import glob

assets_folder = r"c:\Users\Showrav Zaman\My Drive\Giveaway Hunting\SkinClub Contests\Skin Design\Assets\CS2_Weapon\CS2_Weapon"
blender_exe = r"C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe"
blend_files = glob.glob(os.path.join(assets_folder, "**", "*.blend"), recursive=True)

# Ignore Knives and Other
blend_files = [b for b in blend_files if "Knifes" not in b and "Other" not in b]

blender_script = os.path.abspath("blender_unpack.py")
with open(blender_script, 'w') as f:
    f.write('''import bpy
import sys
try:
    bpy.ops.file.unpack_all(method='USE_LOCAL')
    print("Unpacked successfully.")
except Exception as e:
    print(e)
    sys.exit(1)
''')

print(f"Starting extraction for {len(blend_files)} weapons...")
for i, b_file in enumerate(blend_files):
    print(f"[{i+1}/{len(blend_files)}] Unpacking {os.path.basename(b_file)}...")
    cmd = [blender_exe, "-b", b_file, "-P", blender_script]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
print("All textures extracted!")
