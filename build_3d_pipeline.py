import os
import subprocess
import argparse
import random

# We are inside 'Antigravity Skin Generation'
pipeline_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(pipeline_folder)

assets_folder = os.path.join(root_folder, "Assets")
input_folder = os.path.join(pipeline_folder, "Input_Textures")
out_folder = os.path.join(pipeline_folder, "Output_Renders")
blend_folder = os.path.join(pipeline_folder, "Output_Project_Files")
blender_exe = r"C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe"

os.makedirs(out_folder, exist_ok=True)
os.makedirs(blend_folder, exist_ok=True)

parser = argparse.ArgumentParser(description='Automated CS2 Skin Pipeline')
parser.add_argument('--save-blend', action='store_true', default=True, help='Save the .blend project files alongside renders')
args = parser.parse_args()

jpeg_files = [f for f in os.listdir(input_folder) if f.endswith('.jpeg') or f.endswith('.jpg')]

if not jpeg_files:
    print(f"No textures found in {input_folder}. Please add some artwork and run again.")
    exit()

all_weapons = [
    {
        "name": "ak47",
        "obj": os.path.join(assets_folder, r"Official Resources\CS2 Models\weapon_rif_ak47.obj"),
        "normal": os.path.join(assets_folder, r"CS2_Weapon\CS2_Weapon\Rifles\textures\ak47_default_normal_png_c8c5793e.png"),
        "rough": os.path.join(assets_folder, r"CS2_Weapon\CS2_Weapon\Rifles\textures\ak47_default_rough_png_c514dd82.png"),
    },
    {
        "name": "glock18",
        "obj": os.path.join(assets_folder, r"Official Resources\CS2 Models\weapon_pist_glock18.obj"),
        "normal": os.path.join(assets_folder, r"CS2_Weapon\CS2_Weapon\Pistols\textures\glock_default_normal_png_377c3eb8.png"),
        "rough": os.path.join(assets_folder, r"CS2_Weapon\CS2_Weapon\Pistols\textures\glock_default_rough_png_25868aaf.png"),
    },
    {
        "name": "awp",
        "obj": os.path.join(assets_folder, r"Official Resources\CS2 Models\weapon_snip_awp.obj"),
        "normal": os.path.join(assets_folder, r"CS2_Weapon\CS2_Weapon\Rifles\textures\awp_default_normal_png_e882fc00.png"),
        "rough": os.path.join(assets_folder, r"CS2_Weapon\CS2_Weapon\Rifles\textures\awp_default_rough_png_90b89d30.png"),
    }
]

blender_script = os.path.join(pipeline_folder, "blender_headless_render.py")
blender_code = f'''import bpy
import sys
import os
import math
import mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
obj_path, normal_path, rough_path, tex_path, out_path, blend_path = argv

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.cycles.samples = 64
bpy.context.scene.cycles.use_denoising = True
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.film_transparent = True

try:
    bpy.ops.import_scene.obj(filepath=obj_path)
except:
    bpy.ops.wm.obj_import(filepath=obj_path)

meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')

for m in meshes:
    for v in m.bound_box:
        vec = m.matrix_world @ mathutils.Vector(v)
        min_x = min(min_x, vec.x)
        min_y = min(min_y, vec.y)
        min_z = min(min_z, vec.z)
        max_x = max(max_x, vec.x)
        max_y = max(max_y, vec.y)
        max_z = max(max_z, vec.z)

size_x = max_x - min_x
size_y = max_y - min_y
size_z = max_z - min_z
global_bbox_center = mathutils.Vector(((min_x + max_x)/2, (min_y + max_y)/2, (min_z + max_z)/2))
max_dim = max(size_x, size_y, size_z)

cam_data = bpy.data.cameras.new("RenderCam")
cam_data.type = 'ORTHO'
render_ratio = 1920.0 / 1080.0
w_dim = max(size_x, size_y)

if "glock" in obj_path.lower():
    cam_data.ortho_scale = size_z * render_ratio * 1.15
else:
    cam_data.ortho_scale = w_dim * 1.05

cam_obj = bpy.data.objects.new("RenderCam", object_data=cam_data)
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj
cam_dist = max_dim * 2.0

if size_x > size_y:
    cam_obj.location = (global_bbox_center.x, global_bbox_center.y + cam_dist, global_bbox_center.z)
    cam_obj.rotation_euler = (math.radians(90), 0, math.radians(180))
else:
    cam_obj.location = (global_bbox_center.x + cam_dist, global_bbox_center.y, global_bbox_center.z)
    cam_obj.rotation_euler = (math.radians(90), 0, math.radians(90))

mat = bpy.data.materials.new(name="SkinMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
nodes.clear()

bsdf = nodes.new("ShaderNodeBsdfPrincipled")
out_node = nodes.new("ShaderNodeOutputMaterial")
links.new(bsdf.outputs[0], out_node.inputs[0])

tex_node = nodes.new("ShaderNodeTexImage")
tex_node.image = bpy.data.images.load(tex_path)
tc_node = nodes.new("ShaderNodeTexCoord")
map_node = nodes.new("ShaderNodeMapping")
tex_ratio = tex_node.image.size[0] / tex_node.image.size[1]
scale_x = render_ratio / tex_ratio
map_node.inputs['Scale'].default_value = (scale_x, 1.0, 1.0)

links.new(tc_node.outputs["Window"], map_node.inputs["Vector"])
links.new(map_node.outputs["Vector"], tex_node.inputs["Vector"])
links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])

norm_tex = nodes.new("ShaderNodeTexImage")
norm_tex.image = bpy.data.images.load(normal_path)
norm_tex.image.colorspace_settings.name = "Non-Color"
norm_map = nodes.new("ShaderNodeNormalMap")
links.new(norm_tex.outputs["Color"], norm_map.inputs["Color"])
links.new(norm_map.outputs["Normal"], bsdf.inputs["Normal"])

rough_tex = nodes.new("ShaderNodeTexImage")
rough_tex.image = bpy.data.images.load(rough_path)
rough_tex.image.colorspace_settings.name = "Non-Color"
links.new(rough_tex.outputs["Color"], bsdf.inputs["Roughness"])
bsdf.inputs['Metallic'].default_value = 0.5

for m in meshes:
    m.data.materials.clear()
    m.data.materials.append(mat)

def add_light(name, base_energy, offset_x, offset_y, offset_z, radius_mult):
    l_data = bpy.data.lights.new(name=name, type="AREA")
    l_data.energy = base_energy * (max_dim ** 2) * 5.0
    l_data.shape = "DISK"
    l_data.size = max_dim * radius_mult
    loc = (
        global_bbox_center.x + offset_x * max_dim,
        global_bbox_center.y + offset_y * max_dim,
        global_bbox_center.z + offset_z * max_dim
    )
    l_obj = bpy.data.objects.new(name=name, object_data=l_data)
    l_obj.location = loc
    bpy.context.scene.collection.objects.link(l_obj)
    
    track_target = bpy.data.objects.new("Target", None)
    track_target.location = global_bbox_center
    bpy.context.scene.collection.objects.link(track_target)
    
    tt = l_obj.constraints.new(type="TRACK_TO")
    tt.target = track_target
    tt.track_axis = "TRACK_NEGATIVE_Z"
    tt.up_axis = "UP_Y"

add_light("Key", 50, -0.5, 1.0, 0.5, 0.5)
add_light("Fill", 10, 0.5, 1.0, -0.5, 1.0)
add_light("Rim", 250, 0.2, -0.8, 0.5, 0.2)

bpy.ops.file.pack_all()
if blend_path != "SKIP":
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)

bpy.context.scene.render.filepath = out_path
bpy.ops.render.render(write_still=True)
'''

with open(blender_script, 'w') as f:
    f.write(blender_code)

# Randomize! Pick 3 random weapons (or fewer if the list is smaller)
num_to_render = min(3, len(all_weapons))
selected_weapons = random.sample(all_weapons, num_to_render)

print(f"Randomly selected {num_to_render} weapons to render!")

for w in selected_weapons:
    # Pick a random texture for this specific weapon
    tex_name = random.choice(jpeg_files)
    tex_path = os.path.join(input_folder, tex_name)
    out_img = os.path.join(out_folder, f"True3D_{w['name']}_{tex_name.split('_')[0]}_PlaySide.png")
    
    blend_out = "SKIP"
    if args.save_blend:
        blend_out = os.path.join(blend_folder, f"True3D_{w['name']}_{tex_name.split('_')[0]}_Project.blend")
    
    cmd = [
        blender_exe, "-b", "--python-exit-code", "1", "-P", blender_script, "--",
        w["obj"], w["normal"], w["rough"], tex_path, out_img, blend_out
    ]
    
    print(f"Rendering {w['name']} with {tex_name}...")
    try:
        subprocess.run(cmd, check=True)
        
        from PIL import Image
        render = Image.open(out_img).convert("RGBA")
        bg = Image.new("RGBA", render.size, (20, 20, 24, 255))
        bg.paste(render, (0, 0), render)
        bg.save(out_img)
    except Exception as e:
        print(f"Failed to render {w['name']} with {tex_name}. Error: {e}")

print("Automation script complete. 3 Random combinations generated!")
