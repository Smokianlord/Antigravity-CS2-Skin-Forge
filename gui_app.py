import os
import sys
import subprocess
import random
import threading
import glob
import shutil
import math
from PIL import Image, ImageDraw, ImageEnhance
import customtkinter as ctk

if getattr(sys, 'frozen', False):
    pipeline_folder = os.path.dirname(sys.executable)
    icon_path = os.path.join(sys._MEIPASS, 'icon.ico') if hasattr(sys, '_MEIPASS') else os.path.join(pipeline_folder, 'icon.ico')
else:
    pipeline_folder = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(pipeline_folder, 'icon.ico')

root_folder = os.path.dirname(pipeline_folder)
assets_folder = os.path.join(pipeline_folder, "Assets")
default_input_folder = os.path.join(pipeline_folder, "Input_Textures")
default_out_folder = os.path.join(pipeline_folder, "Output_Renders")
default_blend_folder = os.path.join(pipeline_folder, "Output_Project_Files")

def find_blender():
    if "BLENDER_PATH" in os.environ and os.path.exists(os.environ["BLENDER_PATH"]):
        return os.environ["BLENDER_PATH"]
    which_b = shutil.which("blender") or shutil.which("blender.exe")
    if which_b and os.path.exists(which_b):
        return which_b
    candidates = [
        r"C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe",
        r"C:\Program Files\Steam\steamapps\common\Blender\blender.exe",
        r"D:\SteamLibrary\steamapps\common\Blender\blender.exe",
        r"E:\SteamLibrary\steamapps\common\Blender\blender.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    bf_dir = r"C:\Program Files\Blender Foundation"
    if os.path.exists(bf_dir):
        try:
            for s in sorted(os.listdir(bf_dir), reverse=True):
                cand = os.path.join(bf_dir, s, "blender.exe")
                if os.path.exists(cand):
                    return cand
        except Exception:
            pass
    return candidates[0]

blender_exe = find_blender()

os.makedirs(default_input_folder, exist_ok=True)
os.makedirs(default_out_folder, exist_ok=True)
os.makedirs(default_blend_folder, exist_ok=True)

cs2_names = {
    "weapon_rif_ak47": "AK-47", "weapon_snip_awp": "AWP", "weapon_pist_glock18": "Glock-18",
    "weapon_rif_m4a1_silencer": "M4A1-S", "weapon_rif_m4a4": "M4A4", "weapon_pist_usp_silencer": "USP-S",
    "weapon_pist_deagle": "Desert Eagle", "weapon_mach_m249": "M249", "weapon_mach_negev": "Negev",
    "weapon_pist_cz75a": "CZ75-Auto", "weapon_pist_elite": "Dual Berettas", "weapon_pist_fiveseven": "Five-SeveN",
    "weapon_pist_hkp2000": "P2000", "weapon_pist_p250": "P250", "weapon_pist_revolver": "R8 Revolver",
    "weapon_pist_tec9": "Tec-9", "weapon_pist_taser": "Zeus x27", "weapon_rif_aug": "AUG",
    "weapon_rif_famas": "FAMAS", "weapon_rif_galilar": "Galil AR", "weapon_rif_sg556": "SG 553",
    "weapon_shot_mag7": "MAG-7", "weapon_shot_nova": "Nova", "weapon_shot_sawedoff": "Sawed-Off",
    "weapon_shot_xm1014": "XM1014", "weapon_smg_bizon": "PP-Bizon", "weapon_smg_mac10": "MAC-10",
    "weapon_smg_mp5sd": "MP5-SD", "weapon_smg_mp7": "MP7", "weapon_smg_mp9": "MP9",
    "weapon_smg_p90": "P90", "weapon_smg_ump45": "UMP-45", "weapon_snip_g3sg1": "G3SG1",
    "weapon_snip_scar20": "SCAR-20", "weapon_snip_ssg08": "SSG 08"
}

def resolve_asset_dir(primary_subpath, fallback_subpaths=None):
    if fallback_subpaths is None:
        fallback_subpaths = []
    candidates = [primary_subpath] + fallback_subpaths
    if hasattr(sys, '_MEIPASS'):
        for sub in candidates:
            p = os.path.join(sys._MEIPASS, sub)
            if os.path.exists(p):
                return p
    for sub in candidates:
        p = os.path.join(pipeline_folder, sub)
        if os.path.exists(p):
            return p
    parent_dir = os.path.dirname(pipeline_folder)
    for sub in candidates:
        p = os.path.join(parent_dir, sub)
        if os.path.exists(p):
            return p
    return os.path.join(pipeline_folder, primary_subpath)

models_dir = resolve_asset_dir(r"Assets\Models", [r"Assets\Official Resources\CS2 Models", r"Assets\CS2 Models"])
tex_dir = resolve_asset_dir(r"Assets\Textures", [r"Assets\CS2_Weapon\CS2_Weapon", r"Assets\CS2_Weapon"])
all_weapons = []

if os.path.exists(models_dir):
    for obj_file in os.listdir(models_dir):
        if not obj_file.endswith('.obj'):
            continue
        base_name = obj_file.replace('.obj', '')
        display_name = cs2_names.get(base_name, base_name.replace('weapon_', '').title())
        short_name = base_name.split('_')[-1]
        search_name = short_name
        if short_name == "glock18":
            search_name = "glock"
        if short_name == "m4a1_silencer":
            search_name = "m4a1"
        if short_name == "usp_silencer":
            search_name = "usp"
        if short_name == "elite":
            search_name = "beretta"
        if short_name == "hkp2000":
            search_name = "p2000"
        
        norms = glob.glob(os.path.join(tex_dir, "**", f"*{search_name}*normal*.png"), recursive=True)
        roughs = glob.glob(os.path.join(tex_dir, "**", f"*{search_name}*rough*.png"), recursive=True)
        normal_path = norms[0] if norms else "NONE"
        rough_path = roughs[0] if roughs else "NONE"
        
        all_weapons.append({
            "id": base_name,
            "name": display_name,
            "obj": os.path.join(models_dir, obj_file),
            "normal": normal_path,
            "rough": rough_path
        })
all_weapons.sort(key=lambda x: x["name"])

blender_script = os.path.join(pipeline_folder, "blender_headless_render.py")
blender_code = '''import bpy
import sys
import os
import math
import mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
flip_x = "False"
flip_y = "False"
if len(argv) >= 17:
    obj_path, normal_path, rough_path, tex_path, out_path, blend_path, quality, transparent, engine, lighting, fmt, compute_device, tex_offset_x, tex_offset_y, tex_scale, flip_x, flip_y = argv[:17]
elif len(argv) >= 15:
    obj_path, normal_path, rough_path, tex_path, out_path, blend_path, quality, transparent, engine, lighting, fmt, compute_device, tex_offset_x, tex_offset_y, tex_scale = argv[:15]
else:
    obj_path, normal_path, rough_path, tex_path, out_path, blend_path, quality, transparent, engine, lighting, fmt, compute_device, tex_offset_x, tex_offset_y = argv[:14]
    tex_scale = "1.0"

tex_offset_x = -float(tex_offset_x)
tex_offset_y = -float(tex_offset_y)
try:
    tex_scale = float(tex_scale)
    if tex_scale <= 0.001:
        tex_scale = 1.0
except Exception:
    tex_scale = 1.0

is_flip_x = str(flip_x).lower() in ("true", "1", "yes")
is_flip_y = str(flip_y).lower() in ("true", "1", "yes")

bpy.ops.wm.read_factory_settings(use_empty=True)
if "Cycles" in engine:
    try:
        import addon_utils
        addon_utils.enable('cycles')
    except Exception:
        pass
    bpy.context.scene.render.engine = 'CYCLES'
    prefs = bpy.context.preferences.addons['cycles'].preferences
    
    # Priority hardware acceleration: OptiX (RTX hardware RT) -> CUDA -> HIP -> ONEAPI
    for dev_type in ['OPTIX', 'CUDA', 'HIP', 'ONEAPI']:
        try:
            prefs.compute_device_type = dev_type
            prefs.get_devices()
            if prefs.devices:
                break
        except Exception:
            pass

    comp_lower = compute_device.lower()
    if "cpu" in comp_lower and "gpu" not in comp_lower and "hybrid" not in comp_lower:
        bpy.context.scene.cycles.device = 'CPU'
        for d in prefs.devices:
            if d.type == 'CPU':
                d.use = True
    else:
        bpy.context.scene.cycles.device = 'GPU'
        # Enable both GPU and CPU for Hybrid acceleration
        use_cpu = "cpu" in comp_lower or "hybrid" in comp_lower or compute_device == "GPU" or "gpu + cpu" in comp_lower
        for d in prefs.devices:
            if d.type in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI'):
                d.use = True
            elif d.type == 'CPU' and use_cpu:
                d.use = True

    # Real-time hardware AI denoising
    bpy.context.scene.cycles.use_denoising = True
    try:
        bpy.context.scene.cycles.denoiser = 'OPTIX'
    except Exception:
        try:
            bpy.context.scene.cycles.denoiser = 'OPENIMAGEDENOISE'
        except Exception:
            pass

    try:
        bpy.context.scene.render.threads_mode = 'AUTO'
    except Exception:
        pass
else:
    for eng_candidate in ['BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT']:
        try:
            bpy.context.scene.render.engine = eng_candidate
            break
        except Exception:
            pass

bpy.context.scene.render.film_transparent = True if transparent == "True" else False
bpy.context.scene.view_settings.view_transform = 'Standard'

is_preview = "Preview" in quality
if is_preview:
    res_x, res_y, samples = 960, 540, 4
    if bpy.context.scene.render.engine == 'CYCLES':
        bpy.context.scene.cycles.max_bounces = 2
        bpy.context.scene.cycles.diffuse_bounces = 1
        bpy.context.scene.cycles.glossy_bounces = 1
        bpy.context.scene.cycles.transmission_bounces = 0
        bpy.context.scene.cycles.transparent_max_bounces = 2
        bpy.context.scene.cycles.use_adaptive_sampling = True
        bpy.context.scene.cycles.adaptive_threshold = 0.1
elif "Fast" in quality: res_x, res_y, samples = 1280, 720, 16
elif "Standard" in quality: res_x, res_y, samples = 1920, 1080, 32
elif "High" in quality: res_x, res_y, samples = 2560, 1440, 48
elif "Ultra" in quality: res_x, res_y, samples = 3840, 2160, 64
elif "Masterpiece" in quality: res_x, res_y, samples = 7680, 4320, 96
else: res_x, res_y, samples = 1920, 1080, 32

bpy.context.scene.render.resolution_x = res_x
bpy.context.scene.render.resolution_y = res_y
if bpy.context.scene.render.engine == 'CYCLES':
    bpy.context.scene.cycles.samples = samples
else:
    try:
        bpy.context.scene.eevee.taa_render_samples = samples
    except Exception:
        pass

try: bpy.ops.wm.obj_import(filepath=obj_path)
except Exception:
    try: bpy.ops.import_scene.obj(filepath=obj_path)
    except Exception: pass

meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')
for m in meshes:
    for v in m.bound_box:
        vec = m.matrix_world @ mathutils.Vector(v)
        min_x = min(min_x, vec.x); min_y = min(min_y, vec.y); min_z = min(min_z, vec.z)
        max_x = max(max_x, vec.x); max_y = max(max_y, vec.y); max_z = max(max_z, vec.z)

size_x = max_x - min_x
size_y = max_y - min_y
size_z = max_z - min_z
global_bbox_center = mathutils.Vector(((min_x + max_x)/2, (min_y + max_y)/2, (min_z + max_z)/2))
max_dim = max(size_x, size_y, size_z)

cam_data = bpy.data.cameras.new("RenderCam")
cam_data.type = 'ORTHO'
render_ratio = res_x / res_y
cam_data.ortho_scale = max(max(size_x, size_y), size_z * render_ratio) * 1.15
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
tc_node.object = cam_obj
map_node = nodes.new("ShaderNodeMapping")
tex_ratio = tex_node.image.size[0] / tex_node.image.size[1]

# Center-anchored Texture Scaling, Translation & Flipping via Camera Object Space
sx = (render_ratio / tex_ratio) / tex_scale
sy = 1.0 / tex_scale

eff_sx = -sx if is_flip_x else sx
eff_sy = -sy if is_flip_y else sy

ortho_scale = cam_data.ortho_scale
scale_x = eff_sx / ortho_scale
scale_y = (eff_sy * render_ratio) / ortho_scale

map_node.inputs['Scale'].default_value = (scale_x, scale_y, 1.0)
map_node.inputs['Location'].default_value = (0.5 + tex_offset_x, 0.5 + tex_offset_y, 0.0)
links.new(tc_node.outputs["Object"], map_node.inputs["Vector"])
links.new(map_node.outputs["Vector"], tex_node.inputs["Vector"])
links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])

if normal_path != "NONE" and os.path.exists(normal_path):
    norm_tex = nodes.new("ShaderNodeTexImage")
    norm_tex.image = bpy.data.images.load(normal_path)
    norm_tex.image.colorspace_settings.name = "Non-Color"
    norm_map = nodes.new("ShaderNodeNormalMap")
    links.new(norm_tex.outputs["Color"], norm_map.inputs["Color"])
    links.new(norm_map.outputs["Normal"], bsdf.inputs["Normal"])

if rough_path != "NONE" and os.path.exists(rough_path):
    rough_tex = nodes.new("ShaderNodeTexImage")
    rough_tex.image = bpy.data.images.load(rough_path)
    rough_tex.image.colorspace_settings.name = "Non-Color"
    links.new(rough_tex.outputs["Color"], bsdf.inputs["Roughness"])
else:
    bsdf.inputs['Roughness'].default_value = 0.4
bsdf.inputs['Metallic'].default_value = 0.02
if 'Specular IOR Level' in bsdf.inputs:
    bsdf.inputs['Specular IOR Level'].default_value = 0.25
elif 'Specular' in bsdf.inputs:
    bsdf.inputs['Specular'].default_value = 0.25

for m in meshes:
    m.data.materials.clear()
    m.data.materials.append(mat)

def add_light(name, base_energy, offset_x, offset_y, offset_z, radius_mult, mult=1.2):
    l_data = bpy.data.lights.new(name=name, type="AREA")
    l_data.energy = base_energy * (max_dim ** 2) * mult
    l_data.shape = "DISK"
    l_data.size = max_dim * radius_mult
    l_obj = bpy.data.objects.new(name=name, object_data=l_data)
    l_obj.location = (global_bbox_center.x + offset_x * max_dim, global_bbox_center.y + offset_y * max_dim, global_bbox_center.z + offset_z * max_dim)
    bpy.context.scene.collection.objects.link(l_obj)
    track_target = bpy.data.objects.new("Target", None)
    track_target.location = global_bbox_center
    bpy.context.scene.collection.objects.link(track_target)
    tt = l_obj.constraints.new(type="TRACK_TO")
    tt.target = track_target; tt.track_axis = "TRACK_NEGATIVE_Z"; tt.up_axis = "UP_Y"

light_style = lighting.lower()
if "workbench" in light_style or "soft" in light_style:
    add_light("Front", 36, 0.0, 1.2, 0.0, 2.5, mult=1.0)
    add_light("Top", 18, 0.0, 0.2, 1.2, 2.0, mult=1.0)
    add_light("Back", 18, 0.0, -1.0, 0.0, 2.0, mult=1.0)
elif "bright" in light_style or "flat" in light_style:
    add_light("Front", 45, 0.0, 1.0, 0.2, 2.0, mult=1.2)
    add_light("Back", 25, 0.0, -1.0, 0.2, 2.0, mult=1.2)
elif "dark" in light_style or "cinematic" in light_style:
    add_light("Key", 15, -0.8, 0.8, 0.2, 0.2, mult=1.2)
    add_light("Rim", 250, 0.5, -0.8, 0.8, 0.1, mult=1.2)
else:  # Studio Pro (Default)
    add_light("Key", 42, -0.6, 1.0, 0.5, 0.6, mult=1.2)
    add_light("Fill", 12, 0.6, 1.0, -0.4, 1.0, mult=1.2)
    add_light("Rim", 120, 0.2, -0.8, 0.5, 0.2, mult=1.2)

if blend_path != "SKIP":
    try:
        for s in bpy.data.screens:
            for a in s.areas:
                if a.type == 'VIEW_3D':
                    for sp in a.spaces:
                        if sp.type == 'VIEW_3D':
                            sp.region_3d.view_perspective = 'CAMERA'
                            sp.shading.type = 'MATERIAL'
    except Exception:
        pass
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)

bpy.context.scene.render.image_settings.file_format = fmt
bpy.context.scene.render.filepath = out_path
bpy.ops.render.render(write_still=True)
'''

try:
    with open(blender_script, 'w', encoding='utf-8') as f:
        f.write(blender_code)
except Exception:
    pass

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ---------------- 3D TACTILE HARDWARE STYLES ----------------
STYLE_BTN_PRIMARY_3D = {
    "fg_color": "#dc2626",
    "hover_color": "#b91c1c",
    "border_width": 2,
    "border_color": "#fca5a5",
    "corner_radius": 8,
    "text_color": "#ffffff",
}
STYLE_BTN_SECONDARY_3D = {
    "fg_color": "#27272a",
    "hover_color": "#3f3f46",
    "border_width": 1.5,
    "border_color": "#52525b",
    "corner_radius": 7,
    "text_color": "#f4f4f5",
}
STYLE_BTN_HERO_3D = {
    "fg_color": "#dc2626",
    "hover_color": "#b91c1c",
    "border_width": 2.5,
    "border_color": "#fca5a5",
    "corner_radius": 10,
    "text_color": "#ffffff",
}
STYLE_CARD = {
    "fg_color": "#141417",
    "border_width": 1,
    "border_color": "#27272a",
    "corner_radius": 10,
}
SLIDER_3D_KWARGS = {
    "button_color": "#ef4444",
    "button_hover_color": "#f87171",
    "border_width": 2,
    "border_color": "#ffffff",
}
SLIDER_ACTIVE_STYLE = {
    "button_color": "#ef4444",
    "button_hover_color": "#f87171",
    "progress_color": "#dc2626",
    "border_color": "#fca5a5",
}
SLIDER_INACTIVE_STYLE = {
    "button_color": "#71717a",
    "button_hover_color": "#a1a1aa",
    "progress_color": "#3f3f46",
    "border_color": "#27272a",
}
STYLE_BTN_STEPPER_INACTIVE = {
    "fg_color": "#18181b",
    "hover_color": "#27272a",
    "border_width": 1.5,
    "border_color": "#3f3f46",
    "corner_radius": 6,
    "text_color": "#a1a1aa",
}
STYLE_BTN_STEPPER_ACTIVE = {
    "fg_color": "#27272a",
    "hover_color": "#3f3f46",
    "border_width": 2,
    "border_color": "#ef4444",
    "corner_radius": 6,
    "text_color": "#ffffff",
}
CHECKBOX_3D_KWARGS = {
    "fg_color": "#ef4444",
    "hover_color": "#dc2626",
    "border_width": 2,
    "border_color": "#52525b",
}

class IconBuilder:
    def __init__(self):
        self.scale = 4
        self._cache = {}

    def _canvas(self, w, h):
        W, H = w * self.scale, h * self.scale
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        return img, ImageDraw.Draw(img), W, H, (w, h)

    def _to_ctk(self, key, img, size):
        res = img.resize(size, Image.Resampling.LANCZOS)
        ctk_img = ctk.CTkImage(light_image=res, dark_image=res, size=size)
        self._cache[key] = ctk_img
        return ctk_img

    def eye(self, size=(18, 18), color=(255, 255, 255, 245)):
        key = ("eye", size, color)
        if key in self._cache:
            return self._cache[key]
        img, d, W, H, sz = self._canvas(*size)
        pts_top = [(x, int(H/2 - math.sin(x/W * math.pi) * (H*0.35))) for x in range(int(W*0.1), int(W*0.9))]
        pts_bot = [(x, int(H/2 + math.sin(x/W * math.pi) * (H*0.35))) for x in range(int(W*0.9), int(W*0.1)-1, -1)]
        d.polygon(pts_top + pts_bot, outline=color, width=self.scale)
        r = int(H * 0.16)
        d.ellipse([W/2 - r, H/2 - r, W/2 + r, H/2 + r], fill=color)
        d.ellipse([W/2 + r*0.2, H/2 - r*0.5, W/2 + r*0.6, H/2 - r*0.1], fill=(255, 255, 255, 180))
        return self._to_ctk(key, img, sz)

    def refresh(self, size=(16, 16), color=(255, 255, 255, 245)):
        key = ("refresh", size, color)
        if key in self._cache:
            return self._cache[key]
        img, d, W, H, sz = self._canvas(*size)
        cx, cy, r = W/2, H/2, W*0.36
        bbox = [cx - r, cy - r, cx + r, cy + r]
        d.arc(bbox, start=25, end=155, fill=color, width=self.scale)
        d.arc(bbox, start=205, end=335, fill=color, width=self.scale)
        rad1 = math.radians(155)
        ax1, ay1 = cx + r * math.cos(rad1), cy + r * math.sin(rad1)
        d.polygon([(ax1, ay1), (ax1 - self.scale*3, ay1 - self.scale*2.5), (ax1 - self.scale*0.5, ay1 - self.scale*4)], fill=color)
        rad2 = math.radians(335)
        ax2, ay2 = cx + r * math.cos(rad2), cy + r * math.sin(rad2)
        d.polygon([(ax2, ay2), (ax2 + self.scale*3, ay2 + self.scale*2.5), (ax2 + self.scale*0.5, ay2 + self.scale*4)], fill=color)
        return self._to_ctk(key, img, sz)

    def resize(self, size=(16, 16), color=(255, 255, 255, 245)):
        key = ("resize", size, color)
        if key in self._cache:
            return self._cache[key]
        img, d, W, H, sz = self._canvas(*size)
        sw = self.scale
        pad = int(W * 0.18)
        d.line([(pad, H - pad), (W - pad, pad)], fill=color, width=sw)
        d.line([(W - pad - self.scale*3.5, pad), (W - pad, pad), (W - pad, pad + self.scale*3.5)], fill=color, width=sw)
        d.line([(pad + self.scale*3.5, H - pad), (pad, H - pad), (pad, H - pad - self.scale*3.5)], fill=color, width=sw)
        return self._to_ctk(key, img, sz)

    def cube3d(self, size=(24, 24)):
        key = ("cube3d", size)
        if key in self._cache:
            return self._cache[key]
        img, d, W, H, sz = self._canvas(*size)
        cx, cy = W/2, H/2
        L = W * 0.38
        p_top_mid = (cx, cy - L*0.9)
        p_top_r = (cx + L*0.8, cy - L*0.45)
        p_center = (cx, cy)
        p_top_l = (cx - L*0.8, cy - L*0.45)
        d.polygon([p_top_mid, p_top_r, p_center, p_top_l], fill=(255, 255, 255, 245), outline=(255, 255, 255, 255), width=2)
        p_bot_l = (cx - L*0.8, cy + L*0.45)
        p_bot_mid = (cx, cy + L*0.9)
        d.polygon([p_center, p_top_l, p_bot_l, p_bot_mid], fill=(225, 225, 235, 230), outline=(255, 255, 255, 255), width=2)
        p_bot_r = (cx + L*0.8, cy + L*0.45)
        d.polygon([p_center, p_top_r, p_bot_r, p_bot_mid], fill=(185, 185, 200, 230), outline=(255, 255, 255, 255), width=2)
        return self._to_ctk(key, img, sz)

    def dice(self, size=(16, 16), color=(255, 255, 255, 245)):
        key = ("dice", size, color)
        if key in self._cache:
            return self._cache[key]
        img, d, W, H, sz = self._canvas(*size)
        pad = int(W*0.14)
        cr = int(W*0.16)
        d.rounded_rectangle([pad, pad, W-pad, H-pad], radius=cr, outline=color, width=self.scale)
        dot_r = int(self.scale * 1.1)
        for px, py in [(W*0.32, H*0.32), (W*0.5, H*0.5), (W*0.68, H*0.68)]:
            d.ellipse([px-dot_r, py-dot_r, px+dot_r, py+dot_r], fill=color)
        return self._to_ctk(key, img, sz)

    def check_all(self, size=(16, 16), color=(255, 255, 255, 245)):
        key = ("check_all", size, color)
        if key in self._cache:
            return self._cache[key]
        img, d, W, H, sz = self._canvas(*size)
        pad = int(W*0.14)
        d.rounded_rectangle([pad, pad, W-pad, H-pad], radius=int(W*0.14), outline=color, width=self.scale)
        d.line([(W*0.28, H*0.52), (W*0.45, H*0.70), (W*0.75, H*0.32)], fill=color, width=int(self.scale*1.2))
        return self._to_ctk(key, img, sz)

    def clear_all(self, size=(16, 16), color=(255, 255, 255, 200)):
        key = ("clear_all", size, color)
        if key in self._cache:
            return self._cache[key]
        img, d, W, H, sz = self._canvas(*size)
        pad = int(W*0.14)
        d.rounded_rectangle([pad, pad, W-pad, H-pad], radius=int(W*0.14), outline=color, width=self.scale)
        return self._to_ctk(key, img, sz)

    def reset(self, size=(16, 16), color=(255, 255, 255, 245)):
        key = ("reset", size, color)
        if key in self._cache:
            return self._cache[key]
        img, d, W, H, sz = self._canvas(*size)
        cx, cy, r = W/2, H/2, W*0.35
        bbox = [cx - r, cy - r, cx + r, cy + r]
        d.arc(bbox, start=50, end=330, fill=color, width=self.scale)
        rad = math.radians(50)
        ax, ay = cx + r*math.cos(rad), cy + r*math.sin(rad)
        d.polygon([(ax, ay), (ax + self.scale*3, ay - self.scale*2), (ax + self.scale*3, ay + self.scale*2)], fill=color)
        return self._to_ctk(key, img, sz)

    def scale_1x(self, size=(16, 16), color=(255, 255, 255, 245)):
        key = ("scale_1x", size, color)
        if key in self._cache:
            return self._cache[key]
        img, d, W, H, sz = self._canvas(*size)
        pad = int(W*0.14)
        d.rounded_rectangle([pad, pad, W-pad, H-pad], radius=int(W*0.14), outline=color, width=self.scale)
        d.line([(W*0.32, H*0.30), (W*0.32, H*0.70)], fill=color, width=int(self.scale*1.1))
        d.ellipse([W*0.5-self.scale*0.6, H*0.5-self.scale*0.6, W*0.5+self.scale*0.6, H*0.5+self.scale*0.6], fill=color)
        d.line([(W*0.68, H*0.30), (W*0.68, H*0.70)], fill=color, width=int(self.scale*1.1))
        return self._to_ctk(key, img, sz)

    def folder(self, size=(16, 16), color=(255, 255, 255, 245)):
        key = ("folder", size, color)
        if key in self._cache:
            return self._cache[key]
        img, d, W, H, sz = self._canvas(*size)
        p1 = (int(W*0.15), int(H*0.28))
        p2 = (int(W*0.45), int(H*0.28))
        p3 = (int(W*0.55), int(H*0.40))
        p4 = (int(W*0.85), int(H*0.40))
        p5 = (int(W*0.85), int(H*0.76))
        p6 = (int(W*0.15), int(H*0.76))
        d.polygon([p1, p2, p3, p4, p5, p6], outline=color, width=self.scale)
        return self._to_ctk(key, img, sz)

    def pin(self, size=(16, 16), color=(255, 255, 255, 245)):
        key = ("pin", size, color)
        if key in self._cache:
            return self._cache[key]
        img, d, W, H, sz = self._canvas(*size)
        cx, cy = W/2, H/2
        d.line([(cx, cy - H*0.3), (cx, cy + H*0.15)], fill=color, width=int(self.scale*1.8))
        d.line([(cx - W*0.25, cy - H*0.3), (cx + W*0.25, cy - H*0.3)], fill=color, width=int(self.scale*1.4))
        d.line([(cx - W*0.18, cy + H*0.15), (cx + W*0.18, cy + H*0.15)], fill=color, width=int(self.scale*1.4))
        d.line([(cx, cy + H*0.15), (cx, cy + H*0.4)], fill=color, width=self.scale)
        return self._to_ctk(key, img, sz)

    def sliders(self, size=(16, 16), color=(255, 255, 255, 245)):
        key = ("sliders", size, color)
        if key in self._cache:
            return self._cache[key]
        img, d, W, H, sz = self._canvas(*size)
        for x, y_knob in [(W*0.33, H*0.38), (W*0.67, H*0.62)]:
            d.line([(x, H*0.2), (x, H*0.8)], fill=color, width=self.scale)
            d.ellipse([x - self.scale*2, y_knob - self.scale*2, x + self.scale*2, y_knob + self.scale*2], fill=color)
        return self._to_ctk(key, img, sz)

    def arrow_left(self, size=(10, 10), color=(240, 240, 245, 230)):
        key = ("arrow_left", size, color)
        if key in self._cache:
            return self._cache[key]
        img, d, W, H, sz = self._canvas(*size)
        pad_x = int(W * 0.22)
        pad_y = int(H * 0.18)
        pts = [(pad_x, int(H / 2)), (W - pad_x, pad_y), (W - pad_x, H - pad_y)]
        d.polygon(pts, fill=color)
        return self._to_ctk(key, img, sz)

    def arrow_right(self, size=(10, 10), color=(240, 240, 245, 230)):
        key = ("arrow_right", size, color)
        if key in self._cache:
            return self._cache[key]
        img, d, W, H, sz = self._canvas(*size)
        pad_x = int(W * 0.22)
        pad_y = int(H * 0.18)
        pts = [(W - pad_x, int(H / 2)), (pad_x, pad_y), (pad_x, H - pad_y)]
        d.polygon(pts, fill=color)
        return self._to_ctk(key, img, sz)

class TopBarMenu(ctk.CTkOptionMenu):
    """
    Compact top ribbon dropdown menu with zero excess spacing
    between the text label and the dropdown arrow button.
    """
    def __init__(self, master, name, values, command=None, variable=None, **kwargs):
        self._menu_name = name
        self.arrow_width = 10
        super().__init__(
            master,
            values=values,
            command=command,
            variable=variable,
            dynamic_resizing=False,
            height=26,
            corner_radius=4,
            fg_color="#18181b",
            button_color="#18181b",
            button_hover_color="#27272a",
            text_color="#f4f4f5",
            **kwargs
        )
        self.set(name)
        self.update_idletasks()
        tw = self._text_label.winfo_reqwidth()
        total_width = 5 + tw + 4 + self.arrow_width + 4
        self.configure(width=total_width)

    def _create_grid(self):
        self._canvas.grid(row=0, column=0, sticky="nsew")
        left_section_width = self._current_width - self.arrow_width - 2
        self._text_label.grid(row=0, column=0, sticky="w",
                              padx=(max(self._apply_widget_scaling(self._corner_radius), self._apply_widget_scaling(5)),
                                    max(self._apply_widget_scaling(self.arrow_width + 4), self._apply_widget_scaling(3))))

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)
        left_section_width = self._current_width - self.arrow_width - 2
        self._draw_engine.draw_rounded_rect_with_border_vertical_split(
            self._apply_widget_scaling(self._current_width),
            self._apply_widget_scaling(self._current_height),
            self._apply_widget_scaling(self._corner_radius),
            0,
            self._apply_widget_scaling(left_section_width)
        )
        self._draw_engine.draw_dropdown_arrow(
            self._apply_widget_scaling(self._current_width - (self.arrow_width / 2) - 1),
            self._apply_widget_scaling(self._current_height / 2),
            self._apply_widget_scaling(4)
        )
        self._canvas.update_idletasks()

    def _on_enter(self, event=0):
        super()._on_enter(event)
        if self._hover and self._state == tkinter.NORMAL:
            hover_col = self._apply_appearance_mode(self._button_hover_color)
            self._canvas.itemconfig("inner_parts_left", outline=hover_col, fill=hover_col)
            self._canvas.itemconfig("inner_parts_right", outline=hover_col, fill=hover_col)
            self._text_label.configure(bg=hover_col)

    def _on_leave(self, event=0):
        super()._on_leave(event)
        normal_col = self._apply_appearance_mode(self._fg_color)
        self._canvas.itemconfig("inner_parts_left", outline=normal_col, fill=normal_col)
        self._canvas.itemconfig("inner_parts_right", outline=normal_col, fill=normal_col)
        self._text_label.configure(bg=normal_col)

    def _dropdown_callback(self, value: str):
        if self._command is not None:
            self._command(value)
        self.set(self._menu_name)

class CS2SkinGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Antigravity CS2 Skin Forge v1.2.5")
        
        window_width = 1450
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_height = min(820, max(740, screen_height - 80))
        center_x = max(10, int(screen_width / 2 - window_width / 2))
        center_y = max(10, int(screen_height / 2 - window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.minsize(1100, 600)
        
        try:
            self.iconbitmap(icon_path)
        except Exception:
            pass

        self.icon_builder = IconBuilder()

        self.blender_exe = blender_exe
        self.in_dir = default_input_folder
        self.out_dir = default_out_folder
        self.blend_dir = default_blend_folder

        self.preview_win = None
        self.pw_btn_render = None
        self.preview_raw_render = None
        self.is_preview_running = False
        self.preview_pending = False
        self._debounced_preview_job = None

        # Precision Slider Variables & Definition System
        self.bright_var = ctk.DoubleVar(value=1.0)
        self.cont_var = ctk.DoubleVar(value=1.0)
        self.sat_var = ctk.DoubleVar(value=1.0)
        self.tex_off_x_var = ctk.DoubleVar(value=0.0)
        self.tex_off_y_var = ctk.DoubleVar(value=0.0)
        self.tex_scale_var = ctk.DoubleVar(value=1.0)
        self.flip_x_var = ctk.BooleanVar(value=False)
        self.flip_y_var = ctk.BooleanVar(value=False)
        self.light_var = ctk.StringVar(value="Studio Pro")

        self.slider_defs = {
            "tx": {
                "title": "Texture X:",
                "var": self.tex_off_x_var,
                "from_": -1.0,
                "to": 1.0,
                "step": 0.01,
                "step_large": 0.05,
                "decimals": 2,
                "fmt": lambda v: f"{v:.2f}",
                "category": "offset",
                "main_lbl": None, "main_val": None, "main_slider": None, "main_btn_dec": None, "main_btn_inc": None,
                "pw_lbl": None, "pw_val": None, "pw_slider": None, "pw_btn_dec": None, "pw_btn_inc": None,
            },
            "ty": {
                "title": "Texture Y:",
                "var": self.tex_off_y_var,
                "from_": -1.0,
                "to": 1.0,
                "step": 0.01,
                "step_large": 0.05,
                "decimals": 2,
                "fmt": lambda v: f"{v:.2f}",
                "category": "offset",
                "main_lbl": None, "main_val": None, "main_slider": None, "main_btn_dec": None, "main_btn_inc": None,
                "pw_lbl": None, "pw_val": None, "pw_slider": None, "pw_btn_dec": None, "pw_btn_inc": None,
            },
            "scale": {
                "title": "Texture Scale:",
                "var": self.tex_scale_var,
                "from_": 0.1,
                "to": 5.0,
                "step": 0.05,
                "step_large": 0.20,
                "decimals": 2,
                "fmt": lambda v: f"{v:.2f}x",
                "category": "offset",
                "main_lbl": None, "main_val": None, "main_slider": None, "main_btn_dec": None, "main_btn_inc": None,
                "pw_lbl": None, "pw_val": None, "pw_slider": None, "pw_btn_dec": None, "pw_btn_inc": None,
            },
            "bright": {
                "title": "Brightness:",
                "var": self.bright_var,
                "from_": 0.2,
                "to": 2.0,
                "step": 0.01,
                "step_large": 0.05,
                "decimals": 2,
                "fmt": lambda v: f"{v:.2f}",
                "category": "post",
                "main_lbl": None, "main_val": None, "main_slider": None, "main_btn_dec": None, "main_btn_inc": None,
                "pw_lbl": None, "pw_val": None, "pw_slider": None, "pw_btn_dec": None, "pw_btn_inc": None,
            },
            "cont": {
                "title": "Contrast:",
                "var": self.cont_var,
                "from_": 0.2,
                "to": 2.0,
                "step": 0.01,
                "step_large": 0.05,
                "decimals": 2,
                "fmt": lambda v: f"{v:.2f}",
                "category": "post",
                "main_lbl": None, "main_val": None, "main_slider": None, "main_btn_dec": None, "main_btn_inc": None,
                "pw_lbl": None, "pw_val": None, "pw_slider": None, "pw_btn_dec": None, "pw_btn_inc": None,
            },
            "sat": {
                "title": "Saturation:",
                "var": self.sat_var,
                "from_": 0.0,
                "to": 2.0,
                "step": 0.01,
                "step_large": 0.05,
                "decimals": 2,
                "fmt": lambda v: f"{v:.2f}",
                "category": "post",
                "main_lbl": None, "main_val": None, "main_slider": None, "main_btn_dec": None, "main_btn_inc": None,
                "pw_lbl": None, "pw_val": None, "pw_slider": None, "pw_btn_dec": None, "pw_btn_inc": None,
            },
        }
        self.active_slider_key = "tx"
        self.bind("<Key>", self._on_global_key)

        # ---------------- TOP RIBBON MENU ----------------
        self.top_bar = ctk.CTkFrame(self, height=34, corner_radius=0, fg_color="#18181b", border_width=1, border_color="#27272a")
        self.top_bar.pack(side="top", fill="x")

        self.file_var = ctk.StringVar(value="File")
        self.file_menu = TopBarMenu(self.top_bar, name="File", 
                                    values=["Open Input Directory", "Open Output Directory", "Open Project Directory", "Exit"],
                                    command=self.handle_file_menu,
                                    variable=self.file_var)
        self.file_menu.pack(side="left", padx=(6, 2), pady=3)

        self.edit_var = ctk.StringVar(value="Edit")
        self.edit_menu = TopBarMenu(self.top_bar, name="Edit", 
                                    values=["Select All Models", "Deselect All Models", "Select Random Model (3)", "Resize Texture Image..."],
                                    command=self.handle_edit_menu,
                                    variable=self.edit_var)
        self.edit_menu.pack(side="left", padx=2, pady=3)

        self.config_var = ctk.StringVar(value="Configure")
        self.config_menu = TopBarMenu(self.top_bar, name="Configure", 
                                      values=["Set Input Textures Directory", "Set Output Renders Directory", "Set Output Projects Directory", "Set Blender Executable Path"],
                                      command=self.handle_config_menu,
                                      variable=self.config_var)
        self.config_menu.pack(side="left", padx=2, pady=3)
        
        self.help_var = ctk.StringVar(value="Help")
        self.help_menu = TopBarMenu(self.top_bar, name="Help", 
                                    values=["View Documentation", "About"],
                                    command=self.handle_help_menu,
                                    variable=self.help_var)
        self.help_menu.pack(side="left", padx=2, pady=3)

        self.btn_top_preview = ctk.CTkButton(
            self.top_bar,
            text="Live Preview",
            image=self.icon_builder.eye((16, 16)),
            compound="left",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=26,
            width=0,
            command=self.toggle_preview_window,
            **STYLE_BTN_PRIMARY_3D
        )
        self.btn_top_preview.pack(side="right", padx=10, pady=3)

        # ---------------- DIRECTORY FOOTER ----------------
        self.footer_toggle = ctk.CTkButton(
            self,
            text="Show Active Directories",
            image=self.icon_builder.folder((15, 15)),
            compound="left",
            fg_color="#18181b",
            hover_color="#27272a",
            text_color="#d4d4d8",
            border_width=1,
            border_color="#27272a",
            corner_radius=0,
            height=26,
            command=self.toggle_dirs
        )
        self.footer_toggle.pack(side="bottom", fill="x")

        self.footer_frame = ctk.CTkFrame(self, fg_color="#18181b", corner_radius=0)
        self.footer_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.footer_frame, text="Input Textures:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.lbl_path_in = ctk.CTkEntry(self.footer_frame, fg_color="#27272a", border_width=0, text_color="#a1a1aa")
        self.lbl_path_in.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.footer_frame, text="Output Renders:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.lbl_path_out = ctk.CTkEntry(self.footer_frame, fg_color="#27272a", border_width=0, text_color="#a1a1aa")
        self.lbl_path_out.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.footer_frame, text="Output Projects:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.lbl_path_blend = ctk.CTkEntry(self.footer_frame, fg_color="#27272a", border_width=0, text_color="#a1a1aa")
        self.lbl_path_blend.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        self.update_path_displays()

        # ---------------- MAIN HORIZONTAL CONTAINER ----------------
        self.main_container = ctk.CTkFrame(self, fg_color="#09090b")
        self.main_container.pack(side="top", fill="both", expand=True)
        self.main_container.grid_columnconfigure(0, weight=55)
        self.main_container.grid_columnconfigure(1, weight=45)
        self.main_container.grid_rowconfigure(0, weight=1)

        # ==========================================
        # LEFT COLUMN (60% width): Textures & Weapons
        # ==========================================
        self.left_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(15, 5), pady=15)

        # 1. TEXTURE SELECTION BLOCK
        self.tex_container = ctk.CTkFrame(self.left_frame, **STYLE_CARD)
        self.tex_container.pack(fill="x", pady=(0, 15))
        
        self.tex_top = ctk.CTkFrame(self.tex_container, fg_color="transparent")
        self.tex_top.pack(fill="x", padx=15, pady=(15, 5))
        self.lbl_tex = ctk.CTkLabel(self.tex_top, text="Texture Selection", font=ctk.CTkFont(size=18, weight="bold"), text_color="#f4f4f5")
        self.lbl_tex.pack(side="left")
        
        self.btn_tex_none = ctk.CTkButton(self.tex_top, text="Clear", image=self.icon_builder.clear_all((13, 13)), compound="left", width=0, height=26, command=self.deselect_all_tex, **STYLE_BTN_SECONDARY_3D)
        self.btn_tex_none.pack(side="right", padx=(5,0))
        self.btn_tex_all = ctk.CTkButton(self.tex_top, text="Select All", image=self.icon_builder.check_all((13, 13)), compound="left", width=0, height=26, command=self.select_all_tex, **STYLE_BTN_SECONDARY_3D)
        self.btn_tex_all.pack(side="right")
        self.btn_tex_refresh = ctk.CTkButton(self.tex_top, text="Refresh", image=self.icon_builder.refresh((14, 14)), compound="left", width=0, height=26, command=self.refresh_textures, **STYLE_BTN_SECONDARY_3D)
        self.btn_tex_refresh.pack(side="right", padx=(0, 5))
        self.btn_tex_resize = ctk.CTkButton(self.tex_top, text="Resize Image", image=self.icon_builder.resize((14, 14)), compound="left", width=0, height=26, command=self.open_image_resizer, **STYLE_BTN_PRIMARY_3D)
        self.btn_tex_resize.pack(side="right", padx=(0, 5))

        self.grid_textures = ctk.CTkScrollableFrame(self.tex_container, fg_color="#18181c", border_width=1, border_color="#27272a", corner_radius=8, height=190)
        self.grid_textures.pack(fill="x", padx=15, pady=(5, 15))
        self.grid_textures.grid_columnconfigure(0, weight=1)
        self.texture_vars = {}
        self.refresh_textures()

        # 2. WEAPON MODEL SELECTION BLOCK (5-column grid)
        self.weap_container = ctk.CTkFrame(self.left_frame, **STYLE_CARD)
        self.weap_container.pack(fill="both", expand=True)

        self.weap_top = ctk.CTkFrame(self.weap_container, fg_color="transparent")
        self.weap_top.pack(fill="x", padx=15, pady=(15, 5))
        self.lbl_weapons = ctk.CTkLabel(self.weap_top, text="Weapon Model Selection", font=ctk.CTkFont(size=18, weight="bold"), text_color="#f4f4f5")
        self.lbl_weapons.pack(side="left")

        self.btn_sel_none = ctk.CTkButton(self.weap_top, text="Clear", image=self.icon_builder.clear_all((13, 13)), compound="left", width=0, height=26, command=self.deselect_all, **STYLE_BTN_SECONDARY_3D)
        self.btn_sel_none.pack(side="right", padx=(5,0))
        self.btn_sel_all = ctk.CTkButton(self.weap_top, text="Select All", image=self.icon_builder.check_all((13, 13)), compound="left", width=0, height=26, command=self.select_all, **STYLE_BTN_SECONDARY_3D)
        self.btn_sel_all.pack(side="right", padx=5)
        self.btn_sel_rand = ctk.CTkButton(self.weap_top, text="Random (3)", image=self.icon_builder.dice((14, 14)), compound="left", width=0, height=26, command=self.select_random, **STYLE_BTN_SECONDARY_3D)
        self.btn_sel_rand.pack(side="right", padx=5)

        self.grid_weapons = ctk.CTkScrollableFrame(self.weap_container, fg_color="#18181c", border_width=1, border_color="#27272a", corner_radius=8)
        self.grid_weapons.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        self.weapon_vars = {}
        for i, w in enumerate(all_weapons):
            col = i % 5
            row = i // 5
            var = ctk.BooleanVar(value=False)
            chk = ctk.CTkCheckBox(self.grid_weapons, text=w["name"], variable=var, font=ctk.CTkFont(size=13),
                                  command=self._on_item_toggle, **CHECKBOX_3D_KWARGS)
            chk.grid(row=row, column=col, sticky="w", padx=12, pady=7)
            self.weapon_vars[w["id"]] = var
            self.grid_weapons.grid_columnconfigure(col, weight=1)

        # ==========================================
        # RIGHT COLUMN (40% width): Settings, Post-Process, Console, Generate
        # ==========================================
        self.right_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 15), pady=15)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # 5. BOTTOM EXECUTION BLOCK (Live Status, Progress, Generate Button)
        # CRITICAL: PACKED FIRST with side="bottom" so the Hero Render/Generate button is NEVER squeezed out or hidden!
        self.bottom_container = ctk.CTkFrame(self.right_frame, **STYLE_CARD)
        self.bottom_container.pack(side="bottom", fill="x", pady=(8, 0))

        self.status_row = ctk.CTkFrame(self.bottom_container, fg_color="transparent")
        self.status_row.pack(fill="x", padx=15, pady=(8, 2))

        self.lbl_status = ctk.CTkLabel(
            self.status_row,
            text="● Engine Ready [OptiX GPU Raytracing]",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#10b981",
            anchor="w"
        )
        self.lbl_status.pack(side="left")

        self.progress_bar = ctk.CTkProgressBar(self.bottom_container, progress_color="#ef4444", height=8)
        self.progress_bar.pack(fill="x", padx=15, pady=(4, 8))
        self.progress_bar.set(0)

        self.btn_generate = ctk.CTkButton(
            self.bottom_container,
            text="GENERATE 3D SKINS & RENDERS",
            image=self.icon_builder.cube3d((26, 26)),
            compound="left",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            command=self.start_generation,
            **STYLE_BTN_HERO_3D
        )
        self.btn_generate.pack(fill="x", padx=15, pady=(0, 10))

        # Responsive Scrollable Frame for Settings and Adjustments
        self.right_scroll = ctk.CTkScrollableFrame(self.right_frame, fg_color="transparent")
        self.right_scroll.pack(side="top", fill="both", expand=True)

        # 3. SETTINGS BLOCK
        self.settings_container = ctk.CTkFrame(self.right_scroll, **STYLE_CARD)
        self.settings_container.pack(fill="x", pady=(0, 10))
        self.settings_container.grid_columnconfigure(0, weight=1, uniform="a")
        self.settings_container.grid_columnconfigure(1, weight=1, uniform="a")
        
        self.lbl_settings = ctk.CTkLabel(self.settings_container, text="Rendering Engine Options", font=ctk.CTkFont(size=18, weight="bold"), text_color="#f4f4f5")
        self.lbl_settings.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(12, 4))

        self.lbl_eng = ctk.CTkLabel(self.settings_container, text="Render Engine:")
        self.lbl_eng.grid(row=1, column=0, sticky="w", padx=(14, 6))
        self.engine_var = ctk.StringVar(value="Cycles Raytracing")
        self.opt_engine = ctk.CTkOptionMenu(self.settings_container, variable=self.engine_var, values=["Cycles Raytracing", "BLENDER_EEVEE"],
                                            fg_color="#27272a", button_color="#3f3f46", button_hover_color="#52525b", dynamic_resizing=False)
        self.opt_engine.grid(row=2, column=0, sticky="ew", padx=(14, 6), pady=(0, 6))

        self.lbl_dev = ctk.CTkLabel(self.settings_container, text="Compute Device:")
        self.lbl_dev.grid(row=1, column=1, sticky="w", padx=(6, 14))
        self.compute_var = ctk.StringVar(value="GPU + CPU (Hybrid)")
        self.opt_compute = ctk.CTkOptionMenu(self.settings_container, variable=self.compute_var, 
                                             values=["GPU + CPU (Hybrid)", "GPU Only", "CPU Only"],
                                             fg_color="#27272a", button_color="#3f3f46", button_hover_color="#52525b", dynamic_resizing=False)
        self.opt_compute.grid(row=2, column=1, sticky="ew", padx=(6, 14), pady=(0, 6))

        self.lbl_quality = ctk.CTkLabel(self.settings_container, text="Quality Preset:")
        self.lbl_quality.grid(row=3, column=0, sticky="w", padx=(14, 6))
        self.quality_var = ctk.StringVar(value="Standard (1080p | 32 Samples)")
        self.opt_quality = ctk.CTkOptionMenu(self.settings_container, variable=self.quality_var,
                                            values=[
                                                "Fast Draft (720p | 16 Samples)",
                                                "Standard (1080p | 32 Samples)",
                                                "High Quality (1440p | 48 Samples)",
                                                "Ultra (4K | 64 Samples)",
                                                "Masterpiece (8K | 96 Samples)"
                                            ],
                                            fg_color="#27272a", button_color="#3f3f46", button_hover_color="#52525b", dynamic_resizing=False)
        self.opt_quality.grid(row=4, column=0, sticky="ew", padx=(14, 6), pady=(0, 6))

        self.lbl_lighting = ctk.CTkLabel(self.settings_container, text="Lighting Rig:")
        self.lbl_lighting.grid(row=3, column=1, sticky="w", padx=(6, 14))
        self.opt_lighting = ctk.CTkOptionMenu(
            self.settings_container, variable=self.light_var,
            values=["Studio Pro", "Soft Workbench", "Bright Flat", "Dark Cinematic"],
            fg_color="#27272a", button_color="#3f3f46", button_hover_color="#52525b",
            dynamic_resizing=False, command=self._on_lighting_change
        )
        self.opt_lighting.grid(row=4, column=1, sticky="ew", padx=(6, 14), pady=(0, 8))

        self.lbl_bg = ctk.CTkLabel(self.settings_container, text="Studio Background:")
        self.lbl_bg.grid(row=5, column=0, sticky="w", padx=(14, 6))
        self.bg_var = ctk.StringVar(value="Dark Grey (Default)")
        self.opt_bg = ctk.CTkOptionMenu(self.settings_container, variable=self.bg_var,
                                        values=["Dark Grey (Default)", "Deep Blue", "Pure Black", "Pure White", "Green Screen"],
                                        fg_color="#27272a", button_color="#3f3f46", button_hover_color="#52525b", dynamic_resizing=False, command=self._on_bg_change)
        self.opt_bg.grid(row=6, column=0, sticky="ew", padx=(14, 6), pady=(0, 8))
        
        self.blend_var = ctk.BooleanVar(value=True)
        self.chk_blend = ctk.CTkCheckBox(self.settings_container, text="Save .blend File", variable=self.blend_var, **CHECKBOX_3D_KWARGS)
        self.chk_blend.grid(row=5, column=1, sticky="w", padx=(6, 14))

        self.trans_var = ctk.BooleanVar(value=False)
        self.chk_trans = ctk.CTkCheckBox(self.settings_container, text="Transparent Alpha", variable=self.trans_var,
                                         command=self._on_trans_toggle, **CHECKBOX_3D_KWARGS)
        self.chk_trans.grid(row=6, column=1, sticky="w", padx=(6, 14), pady=(0, 8))

        self.mode_grid = ctk.CTkFrame(self.settings_container, fg_color="transparent")
        self.mode_grid.grid(row=7, column=0, columnspan=2, sticky="w", padx=15, pady=(4, 12))
        self.lbl_mode = ctk.CTkLabel(self.mode_grid, text="Generation Mode:", font=ctk.CTkFont(weight="bold"))
        self.lbl_mode.pack(side="left", padx=(0, 8))
        self.mode_var = ctk.StringVar(value="all")
        self.rb_all = ctk.CTkRadioButton(self.mode_grid, text="All Combinations", variable=self.mode_var, value="all", fg_color="#ef4444", hover_color="#dc2626")
        self.rb_all.pack(side="left", padx=(0, 8))
        self.rb_random = ctk.CTkRadioButton(self.mode_grid, text="Random Match", variable=self.mode_var, value="random", fg_color="#ef4444", hover_color="#dc2626")
        self.rb_random.pack(side="left")

        # 4. ADJUSTMENTS BLOCK (Sliders with precision Stepper Arrows & Visual Highlight)
        self.post_container = ctk.CTkFrame(self.right_scroll, **STYLE_CARD)
        self.post_container.pack(fill="x", pady=(0, 4))
        self.post_container.grid_columnconfigure(1, weight=1)
        
        self.lbl_bc = ctk.CTkLabel(self.post_container, text="Adjustments", font=ctk.CTkFont(size=18, weight="bold"), text_color="#f4f4f5")
        self.lbl_bc.grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(10, 4))
        
        # Main window slider rows: tx, ty, scale, bright, cont, sat
        main_rows = [
            ("tx", 1),
            ("ty", 2),
            ("scale", 3),
            ("bright", 4),
            ("cont", 5),
            ("sat", 6),
        ]

        for key, r in main_rows:
            s = self.slider_defs[key]
            lbl = ctk.CTkLabel(self.post_container, text=f"  {s['title']}", width=110, anchor="w", font=ctk.CTkFont(size=12, weight="normal"), text_color="#e4e4e7")
            lbl.grid(row=r, column=0, sticky="w", padx=15, pady=2)
            s["main_lbl"] = lbl

            slider_box = ctk.CTkFrame(self.post_container, fg_color="transparent")
            slider_box.grid(row=r, column=1, sticky="ew", padx=10, pady=2)

            btn_dec = ctk.CTkButton(
                slider_box,
                text="",
                image=self.icon_builder.arrow_left((10, 10)),
                width=24,
                height=24,
                command=lambda k=key: self.step_slider(k, -1),
                **STYLE_BTN_STEPPER_INACTIVE
            )
            btn_dec.pack(side="left", padx=(0, 4))
            s["main_btn_dec"] = btn_dec

            slider = ctk.CTkSlider(
                slider_box,
                from_=s["from_"],
                to=s["to"],
                variable=s["var"],
                command=lambda v, k=key: self._on_slider_command(k, v, source="main"),
                **SLIDER_INACTIVE_STYLE
            )
            slider.pack(side="left", fill="x", expand=True)
            slider._canvas.bind("<Button-1>", lambda e, k=key: self.set_active_slider(k), add="+")
            slider.bind("<Button-1>", lambda e, k=key: self.set_active_slider(k), add="+")
            slider._canvas.bind("<ButtonRelease-1>", lambda e, k=key: self._on_slider_release(k), add="+")
            slider.bind("<ButtonRelease-1>", lambda e, k=key: self._on_slider_release(k), add="+")
            s["main_slider"] = slider

            btn_inc = ctk.CTkButton(
                slider_box,
                text="",
                image=self.icon_builder.arrow_right((10, 10)),
                width=24,
                height=24,
                command=lambda k=key: self.step_slider(k, 1),
                **STYLE_BTN_STEPPER_INACTIVE
            )
            btn_inc.pack(side="left", padx=(4, 0))
            s["main_btn_inc"] = btn_inc

            val_lbl = ctk.CTkLabel(self.post_container, text=s["fmt"](s["var"].get()), width=46, anchor="e", text_color="#a1a1aa")
            val_lbl.grid(row=r, column=2, padx=15, pady=2)
            s["main_val"] = val_lbl

        # Aliases for backward compatibility
        self.lbl_tex_off_x = self.slider_defs["tx"]["main_lbl"]
        self.tex_off_x_slider = self.slider_defs["tx"]["main_slider"]
        self.lbl_tx_val = self.slider_defs["tx"]["main_val"]

        self.lbl_tex_off_y = self.slider_defs["ty"]["main_lbl"]
        self.tex_off_y_slider = self.slider_defs["ty"]["main_slider"]
        self.lbl_ty_val = self.slider_defs["ty"]["main_val"]

        self.lbl_tex_scale = self.slider_defs["scale"]["main_lbl"]
        self.tex_scale_slider = self.slider_defs["scale"]["main_slider"]
        self.lbl_scale_val = self.slider_defs["scale"]["main_val"]

        self.lbl_bright = self.slider_defs["bright"]["main_lbl"]
        self.bright_slider = self.slider_defs["bright"]["main_slider"]
        self.lbl_b_val = self.slider_defs["bright"]["main_val"]

        self.lbl_cont = self.slider_defs["cont"]["main_lbl"]
        self.cont_slider = self.slider_defs["cont"]["main_slider"]
        self.lbl_c_val = self.slider_defs["cont"]["main_val"]

        self.lbl_sat = self.slider_defs["sat"]["main_lbl"]
        self.sat_slider = self.slider_defs["sat"]["main_slider"]
        self.lbl_sat_val = self.slider_defs["sat"]["main_val"]

        # Texture Mirroring (Flip X & Flip Y)
        flip_frame = ctk.CTkFrame(self.post_container, fg_color="transparent")
        flip_frame.grid(row=7, column=0, columnspan=3, padx=15, pady=(2, 2), sticky="w")
        
        lbl_flip = ctk.CTkLabel(flip_frame, text="Mirror Texture:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#e4e4e7")
        lbl_flip.pack(side="left", padx=(0, 12))

        self.chk_flip_x = ctk.CTkCheckBox(
            flip_frame, text="Flip X (⇄)", variable=self.flip_x_var,
            command=self._on_flip_toggle, **CHECKBOX_3D_KWARGS
        )
        self.chk_flip_x.pack(side="left", padx=(0, 12))

        self.chk_flip_y = ctk.CTkCheckBox(
            flip_frame, text="Flip Y (⇅)", variable=self.flip_y_var,
            command=self._on_flip_toggle, **CHECKBOX_3D_KWARGS
        )
        self.chk_flip_y.pack(side="left")

        # Shortcut hint
        lbl_hint = ctk.CTkLabel(
            self.post_container,
            text="⌨ Arrow Keys / ◀ ▶ to nudge  •  Tab to switch  •  1-6 to select  •  Shift 5x",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#a1a1aa"
        )
        lbl_hint.grid(row=8, column=0, columnspan=3, padx=15, pady=(2, 8), sticky="w")

        self.fmt_var = ctk.StringVar(value="PNG")

    def refresh_textures(self):
        for widget in self.grid_textures.winfo_children():
            widget.destroy()
        self.texture_vars.clear()
        
        if not os.path.exists(self.in_dir):
            return
        valid_ext = ('.jpg', '.jpeg', '.png')
        tex_files = [f for f in os.listdir(self.in_dir) if f.lower().endswith(valid_ext)]
        
        if not tex_files:
            lbl = ctk.CTkLabel(self.grid_textures, text=f"No textures found in:\n{self.in_dir}", text_color="#a1a1aa", font=ctk.CTkFont(slant="italic"))
            lbl.grid(row=0, column=0, padx=15, pady=10)
            return

        for i, tex in enumerate(tex_files):
            var = ctk.BooleanVar(value=False)
            ext = os.path.splitext(tex)[1].upper().replace('.', '')
            if ext == "JPEG":
                ext = "JPG"
            
            row_frame = ctk.CTkFrame(self.grid_textures, fg_color="transparent")
            row_frame.grid(row=i, column=0, sticky="ew", padx=10, pady=3)
            row_frame.grid_columnconfigure(0, weight=1)

            chk = ctk.CTkCheckBox(row_frame, text=tex, variable=var, font=ctk.CTkFont(size=13),
                                  command=self._on_item_toggle, **CHECKBOX_3D_KWARGS)
            chk.grid(row=0, column=0, sticky="w", padx=(5, 10), pady=2)
            
            badge_fg = "#ef4444" if ext == "PNG" else "#38bdf8"
            lbl_ext = ctk.CTkLabel(row_frame, text=ext, font=ctk.CTkFont(size=11, weight="bold"),
                                   fg_color="#3f3f46", text_color=badge_fg, corner_radius=6,
                                   width=40, height=20)
            lbl_ext.grid(row=0, column=1, sticky="e", padx=(0, 5), pady=2)
            self.texture_vars[tex] = var

        if hasattr(self, 'preview_win') and self.preview_win is not None and self.preview_win.winfo_exists():
            self._sync_preview_selectors()

    def select_all_tex(self):
        for var in self.texture_vars.values():
            var.set(True)
        self._on_item_toggle()

    def deselect_all_tex(self):
        for var in self.texture_vars.values():
            var.set(False)

    def select_all(self):
        for var in self.weapon_vars.values():
            var.set(True)
        self._on_item_toggle()

    def deselect_all(self):
        for var in self.weapon_vars.values():
            var.set(False)

    def select_random(self):
        self.deselect_all()
        keys = random.sample(list(self.weapon_vars.keys()), min(3, len(self.weapon_vars)))
        for k in keys:
            self.weapon_vars[k].set(True)
        self._on_item_toggle()

    def _on_item_toggle(self):
        if hasattr(self, 'preview_win') and self.preview_win is not None and self.preview_win.winfo_exists():
            self._sync_preview_selectors()
            self.trigger_live_preview()

    def toggle_dirs(self):
        if self.footer_frame.winfo_ismapped():
            self.footer_frame.pack_forget()
            self.footer_toggle.configure(text="▼ Show Active Directories")
        else:
            self.footer_frame.pack(side="bottom", fill="x", before=self.footer_toggle)
            self.footer_toggle.configure(text="▲ Hide Active Directories")

    def update_path_displays(self):
        self.lbl_path_in.configure(state="normal")
        self.lbl_path_in.delete(0, "end")
        self.lbl_path_in.insert(0, self.in_dir)
        self.lbl_path_in.configure(state="readonly")
        
        self.lbl_path_out.configure(state="normal")
        self.lbl_path_out.delete(0, "end")
        self.lbl_path_out.insert(0, self.out_dir)
        self.lbl_path_out.configure(state="readonly")
        
        self.lbl_path_blend.configure(state="normal")
        self.lbl_path_blend.delete(0, "end")
        self.lbl_path_blend.insert(0, self.blend_dir)
        self.lbl_path_blend.configure(state="readonly")

    def handle_config_menu(self, choice):
        self.config_var.set("Configure")
        if choice == "Set Input Textures Directory":
            path = ctk.filedialog.askdirectory(title="Select Input Directory")
            if path:
                self.in_dir = path
                self.refresh_textures()
                self.update_path_displays()
                self.log(f"Input directory set: {path}")
        elif choice == "Set Output Renders Directory":
            path = ctk.filedialog.askdirectory(title="Select Output Renders Directory")
            if path: 
                self.out_dir = path
                self.update_path_displays()
                self.log(f"Output renders directory set: {path}")
        elif choice == "Set Output Projects Directory":
            path = ctk.filedialog.askdirectory(title="Select Output Projects Directory")
            if path: 
                self.blend_dir = path
                self.update_path_displays()
                self.log(f"Output projects directory set: {path}")
        elif choice == "Set Blender Executable Path":
            path = ctk.filedialog.askopenfilename(title="Select blender.exe", filetypes=[("Blender Executable", "blender.exe"), ("All Files", "*.*")])
            if path:
                self.blender_exe = path
                self.log(f"Blender executable path configured: {path}")

    def handle_file_menu(self, choice):
        self.file_var.set("File")
        if choice == "Open Input Directory":
            if os.path.exists(self.in_dir):
                os.startfile(self.in_dir)
        elif choice == "Open Output Directory":
            if os.path.exists(self.out_dir):
                os.startfile(self.out_dir)
        elif choice == "Open Project Directory":
            if os.path.exists(self.blend_dir):
                os.startfile(self.blend_dir)
        elif choice == "Exit":
            self.quit()

    def handle_edit_menu(self, choice):
        self.edit_var.set("Edit")
        if choice == "Select All Models":
            self.select_all()
        elif choice == "Deselect All Models":
            self.deselect_all()
        elif choice == "Select Random Model (3)":
            self.select_random()
        elif choice == "Resize Texture Image...":
            self.open_image_resizer()

    def handle_help_menu(self, choice):
        self.help_var.set("Help")
        if choice == "View Documentation":
            self.show_docs()
        elif choice == "About":
            self.show_about()
        
    def show_docs(self):
        win = ctk.CTkToplevel(self)
        win.title("Documentation - Antigravity CS2 Skin Forge")
        win.geometry("580x380")
        win.transient(self)
        win.attributes('-topmost', True)
        try:
            win.after(200, lambda: win.iconbitmap(icon_path) if os.path.exists(icon_path) else None)
        except Exception:
            pass
        lbl = ctk.CTkLabel(win, text=(
            "Antigravity CS2 Skin Forge (v1.2.5) Quick Guide:\n\n"
            "1. Texture Selection & Resizing:\n"
            "   - Place flat patterns into Input_Textures/.\n"
            "   - Click 'Resize Image' to resize textures (4K/2K/1K/512/Custom) with Lanczos quality.\n"
            "2. Weapon Selection: Check which of the 35 CS2 weapon models to forge.\n"
            "3. Live Preview & Scaling:\n"
            "   - Click 'Live Preview' on top ribbon to inspect in real time (~0.2s).\n"
            "   - Move 'Texture X' & 'Texture Y' sliders to translate the pattern.\n"
            "   - Adjust 'Texture Scale' (0.1x - 5.0x) to resize the pattern centered on the weapon.\n"
            "   - Toggle 'Flip Horizontal' (⇄) & 'Flip Vertical' (⇅) to mirror textures along weapon axes.\n"
            "   - The preview window stays locked on top of the app and never hides sliders.\n"
            "4. Hardware Acceleration: Hybrid GPU (OptiX / CUDA) + CPU acceleration engages all\n"
            "   RT cores and CPU threads for ultra-fast previews and raytraced production assets.\n"
            "5. Click 'GENERATE 3D SKINS & RENDERS' to batch render photorealistic production assets."
        ), justify="left", font=ctk.CTkFont(size=13))
        lbl.pack(expand=True, padx=25, pady=20)

    def show_about(self):
        win = ctk.CTkToplevel(self)
        win.title("About")
        win.geometry("460x280")
        win.transient(self)
        win.attributes('-topmost', True)
        try:
            win.after(200, lambda: win.iconbitmap(icon_path) if os.path.exists(icon_path) else None)
        except Exception:
            pass
        lbl = ctk.CTkLabel(win, text=(
            "Antigravity CS2 Skin Forge v1.2.5\n\n"
            "Professional CS2 Weapon Texturing & Rendering Studio\n"
            "Powered by Headless Blender OptiX GPU + CPU Raytracing\n\n"
            "Created by Smokianlord\n"
            "All 35 CS2 Weapon Models & Valve PBR Maps Included"
        ), font=ctk.CTkFont(size=13, weight="bold"))
        lbl.pack(expand=True)
        
    def show_completion_popup(self):
        win = ctk.CTkToplevel(self)
        win.title("Done!")
        win.geometry("340x170")
        win.transient(self)
        win.attributes('-topmost', True)
        try:
            win.after(200, lambda: win.iconbitmap(icon_path) if os.path.exists(icon_path) else None)
        except Exception:
            pass
        lbl = ctk.CTkLabel(win, text="Rendering is Complete!", font=ctk.CTkFont(size=18, weight="bold"), text_color="#10b981")
        lbl.pack(pady=(20, 10))
        btn = ctk.CTkButton(
            win,
            text="Open Output Folder",
            image=self.icon_builder.folder((16, 16)),
            compound="left",
            height=38,
            command=lambda: [os.startfile(self.out_dir) if os.path.exists(self.out_dir) else None, win.destroy()],
            **STYLE_BTN_PRIMARY_3D
        )
        btn.pack(pady=10)

    def log(self, message):
        clean_msg = message.replace("> ", "").strip()
        if hasattr(self, 'lbl_status') and self.lbl_status.winfo_exists():
            if "ERROR" in clean_msg or "FAILED" in clean_msg:
                self.lbl_status.configure(text=f"✖ {clean_msg}", text_color="#ef4444")
            elif "SUCCESS" in clean_msg or "complete" in clean_msg.lower():
                self.lbl_status.configure(text=f"✔ {clean_msg}", text_color="#10b981")
            elif "Warming" in clean_msg or "Rendering" in clean_msg or "Queued" in clean_msg:
                self.lbl_status.configure(text=f"⚡ {clean_msg}", text_color="#38bdf8")
            else:
                self.lbl_status.configure(text=clean_msg, text_color="#e4e4e7")
        print(f"[SkinForge] {clean_msg}")
        
    def set_active_slider(self, key):
        if key not in self.slider_defs:
            return
        self.active_slider_key = key
        for k, s in self.slider_defs.items():
            is_active = (k == self.active_slider_key)
            prefix = "► " if is_active else "  "
            lbl_title = f"{prefix}{s['title']}"
            lbl_color = "#ef4444" if is_active else "#f4f4f5"
            lbl_font = ctk.CTkFont(size=12, weight="bold" if is_active else "normal")
            val_color = "#ef4444" if is_active else "#a1a1aa"
            val_font = ctk.CTkFont(size=12, weight="bold" if is_active else "normal")

            # Main window widgets
            if s.get("main_lbl") and s["main_lbl"].winfo_exists():
                s["main_lbl"].configure(text=lbl_title, text_color=lbl_color, font=lbl_font)
            if s.get("main_val") and s["main_val"].winfo_exists():
                s["main_val"].configure(text_color=val_color, font=val_font)
            if s.get("main_slider") and s["main_slider"].winfo_exists():
                sl_style = SLIDER_ACTIVE_STYLE if is_active else SLIDER_INACTIVE_STYLE
                s["main_slider"].configure(**sl_style)
            if s.get("main_btn_dec") and s["main_btn_dec"].winfo_exists():
                btn_style = STYLE_BTN_STEPPER_ACTIVE if is_active else STYLE_BTN_STEPPER_INACTIVE
                s["main_btn_dec"].configure(**btn_style)
            if s.get("main_btn_inc") and s["main_btn_inc"].winfo_exists():
                btn_style = STYLE_BTN_STEPPER_ACTIVE if is_active else STYLE_BTN_STEPPER_INACTIVE
                s["main_btn_inc"].configure(**btn_style)

            # Preview window widgets
            if s.get("pw_lbl") and s["pw_lbl"].winfo_exists():
                s["pw_lbl"].configure(text=lbl_title, text_color=lbl_color, font=lbl_font)
            if s.get("pw_val") and s["pw_val"].winfo_exists():
                s["pw_val"].configure(text_color=val_color, font=val_font)
            if s.get("pw_slider") and s["pw_slider"].winfo_exists():
                sl_style = SLIDER_ACTIVE_STYLE if is_active else SLIDER_INACTIVE_STYLE
                s["pw_slider"].configure(**sl_style)
            if s.get("pw_btn_dec") and s["pw_btn_dec"].winfo_exists():
                btn_style = STYLE_BTN_STEPPER_ACTIVE if is_active else STYLE_BTN_STEPPER_INACTIVE
                s["pw_btn_dec"].configure(**btn_style)
            if s.get("pw_btn_inc") and s["pw_btn_inc"].winfo_exists():
                btn_style = STYLE_BTN_STEPPER_ACTIVE if is_active else STYLE_BTN_STEPPER_INACTIVE
                s["pw_btn_inc"].configure(**btn_style)

    def step_slider(self, key, delta, large=False):
        self.set_active_slider(key)
        s = self.slider_defs.get(key)
        if not s:
            return
        step = s["step_large"] if large else s["step"]
        curr = float(s["var"].get())
        new_val = curr + delta * step
        new_val = max(s["from_"], min(s["to"], new_val))
        new_val = round(new_val, s.get("decimals", 2))

        s["var"].set(new_val)
        self._sync_slider_value(key, new_val, source="program")

        if s["category"] == "post":
            self._refresh_preview_postprocess()
        else:
            self._schedule_debounced_preview()

    def cycle_active_slider(self, direction=1):
        keys = list(self.slider_defs.keys())
        if self.active_slider_key in keys:
            idx = keys.index(self.active_slider_key)
            new_idx = (idx + direction) % len(keys)
        else:
            new_idx = 0
        self.set_active_slider(keys[new_idx])

    def set_slider_boundary(self, key, to_min=True):
        self.set_active_slider(key)
        s = self.slider_defs.get(key)
        if not s:
            return
        val = s["from_"] if to_min else s["to"]
        val = round(val, s.get("decimals", 2))
        s["var"].set(val)
        self._sync_slider_value(key, val, source="program")
        if s["category"] == "post":
            self._refresh_preview_postprocess()
        else:
            self._schedule_debounced_preview()

    def _on_slider_command(self, key, val, source="main"):
        if self.active_slider_key != key:
            self.set_active_slider(key)
        s = self.slider_defs.get(key)
        if not s:
            return
        val_f = round(float(val), s.get("decimals", 2))
        s["var"].set(val_f)
        self._sync_slider_value(key, val_f, source=source)
        if s["category"] == "post":
            self._refresh_preview_postprocess()

    def _on_slider_release(self, key):
        s = self.slider_defs.get(key)
        if not s:
            return
        if s["category"] == "offset":
            if getattr(self, '_debounced_preview_job', None):
                self.after_cancel(self._debounced_preview_job)
                self._debounced_preview_job = None
            if hasattr(self, 'preview_win') and self.preview_win is not None and self.preview_win.winfo_exists():
                self.trigger_live_preview()
        elif s["category"] == "post":
            self._refresh_preview_postprocess()

    def _sync_slider_value(self, key, val_f, source="program"):
        s = self.slider_defs.get(key)
        if not s:
            return
        text_val = s["fmt"](val_f)

        # Update Main Window
        if s.get("main_val") and s["main_val"].winfo_exists():
            s["main_val"].configure(text=text_val)
        if source != "main" and s.get("main_slider") and s["main_slider"].winfo_exists():
            s["main_slider"].set(val_f)

        # Update Preview Window
        if s.get("pw_val") and s["pw_val"].winfo_exists():
            s["pw_val"].configure(text=text_val)
        if source != "pw" and s.get("pw_slider") and s["pw_slider"].winfo_exists():
            s["pw_slider"].set(val_f)

    def _schedule_debounced_preview(self):
        if getattr(self, '_debounced_preview_job', None):
            self.after_cancel(self._debounced_preview_job)
        self._debounced_preview_job = self.after(160, self._fire_debounced_preview)

    def _fire_debounced_preview(self):
        self._debounced_preview_job = None
        if hasattr(self, 'preview_win') and self.preview_win is not None and self.preview_win.winfo_exists():
            self.trigger_live_preview()

    def _on_global_key(self, event):
        focused = getattr(event, 'widget', None)
        if focused is not None:
            try:
                w_class = focused.__class__.__name__.lower()
                if "entry" in w_class or "text" in w_class:
                    return
            except Exception:
                pass

        keysym = event.keysym
        is_shift = bool(event.state & 0x1)

        if keysym in ("Left", "Down"):
            self.step_slider(self.active_slider_key, -1, large=is_shift)
            return "break"
        elif keysym in ("Right", "Up"):
            self.step_slider(self.active_slider_key, 1, large=is_shift)
            return "break"
        elif keysym == "Tab":
            self.cycle_active_slider(-1 if is_shift else 1)
            return "break"
        elif keysym == "Home":
            self.set_slider_boundary(self.active_slider_key, to_min=True)
            return "break"
        elif keysym == "End":
            self.set_slider_boundary(self.active_slider_key, to_min=False)
            return "break"
        elif keysym in ("1", "2", "3", "4", "5", "6"):
            idx = int(keysym) - 1
            keys = list(self.slider_defs.keys())
            if 0 <= idx < len(keys):
                self.set_active_slider(keys[idx])
            return "break"

    # Backward-compatible slider wrappers
    def _on_bright_slider(self, v):
        self._on_slider_command("bright", v, source="main")

    def _on_cont_slider(self, v):
        self._on_slider_command("cont", v, source="main")

    def _on_sat_slider(self, v):
        self._on_slider_command("sat", v, source="main")

    def _on_tx_slider(self, v):
        self._on_slider_command("tx", v, source="main")

    def _on_ty_slider(self, v):
        self._on_slider_command("ty", v, source="main")

    def _on_scale_slider(self, v):
        self._on_slider_command("scale", v, source="main")

    def _sync_slider_x(self, v):
        self._on_slider_command("tx", v, source="pw")

    def _sync_slider_y(self, v):
        self._on_slider_command("ty", v, source="pw")

    def _sync_slider_scale(self, v):
        self._on_slider_command("scale", v, source="pw")

    def _on_bg_change(self, val):
        if hasattr(self, 'pw_opt_bg') and self.pw_opt_bg.winfo_exists():
            self.pw_bg_var.set(val)
        if hasattr(self, 'opt_bg') and self.opt_bg.winfo_exists():
            self.bg_var.set(val)
        self._refresh_preview_postprocess()

    def _on_lighting_change(self, val=None):
        if hasattr(self, 'pw_opt_lighting') and self.pw_opt_lighting.winfo_exists() and val:
            self.light_var.set(val)
        if hasattr(self, 'opt_lighting') and self.opt_lighting.winfo_exists() and val:
            self.opt_lighting.set(val)
        if hasattr(self, 'preview_win') and self.preview_win is not None and self.preview_win.winfo_exists():
            self.trigger_live_preview()

    def _on_trans_toggle(self):
        self._refresh_preview_postprocess()

    def _on_flip_toggle(self):
        self._update_pw_flip_buttons()
        if hasattr(self, 'preview_win') and self.preview_win is not None and self.preview_win.winfo_exists():
            self.trigger_live_preview()

    def _toggle_flip_x(self):
        self.flip_x_var.set(not self.flip_x_var.get())
        self._on_flip_toggle()

    def _toggle_flip_y(self):
        self.flip_y_var.set(not self.flip_y_var.get())
        self._on_flip_toggle()

    def _update_pw_flip_buttons(self):
        if hasattr(self, 'btn_pw_flip_x') and self.btn_pw_flip_x is not None and self.btn_pw_flip_x.winfo_exists():
            if self.flip_x_var.get():
                self.btn_pw_flip_x.configure(fg_color="#3b82f6", text_color="#ffffff", border_color="#60a5fa")
            else:
                self.btn_pw_flip_x.configure(fg_color="#27272a", text_color="#e4e4e7", border_color="#3f3f46")
        if hasattr(self, 'btn_pw_flip_y') and self.btn_pw_flip_y is not None and self.btn_pw_flip_y.winfo_exists():
            if self.flip_y_var.get():
                self.btn_pw_flip_y.configure(fg_color="#3b82f6", text_color="#ffffff", border_color="#60a5fa")
            else:
                self.btn_pw_flip_y.configure(fg_color="#27272a", text_color="#e4e4e7", border_color="#3f3f46")

    def _on_main_slider_release(self):
        self._on_slider_release(self.active_slider_key)

    def _on_preview_close(self):
        for s in self.slider_defs.values():
            s["pw_lbl"] = None
            s["pw_val"] = None
            s["pw_slider"] = None
            s["pw_btn_dec"] = None
            s["pw_btn_inc"] = None
        self.btn_pw_flip_x = None
        self.btn_pw_flip_y = None
        self.pw_btn_render = None
        if self.preview_win is not None:
            self.preview_win.destroy()
            self.preview_win = None

    def _reset_offsets(self):
        self.slider_defs["tx"]["var"].set(0.0)
        self.slider_defs["ty"]["var"].set(0.0)
        self.slider_defs["scale"]["var"].set(1.0)
        self.flip_x_var.set(False)
        self.flip_y_var.set(False)
        self._sync_slider_value("tx", 0.0, source="program")
        self._sync_slider_value("ty", 0.0, source="program")
        self._sync_slider_value("scale", 1.0, source="program")
        self._update_pw_flip_buttons()
        self.trigger_live_preview()

    def _reset_fx(self):
        self.slider_defs["bright"]["var"].set(1.0)
        self.slider_defs["cont"]["var"].set(1.0)
        self.slider_defs["sat"]["var"].set(1.0)
        self._sync_slider_value("bright", 1.0, source="program")
        self._sync_slider_value("cont", 1.0, source="program")
        self._sync_slider_value("sat", 1.0, source="program")
        self._refresh_preview_postprocess()

    def _on_preview_viewport_resize(self, event=None):
        if getattr(self, '_resize_job', None):
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(80, self._refresh_preview_postprocess)

    def toggle_preview_window(self):
        if hasattr(self, 'preview_win') and self.preview_win is not None and self.preview_win.winfo_exists():
            self.preview_win.deiconify()
            self.preview_win.transient(self)
            self.preview_win.attributes("-topmost", True)
            self.preview_win.lift()
            self.preview_win.focus_force()
            self.trigger_live_preview()
            return
        
        self.create_preview_window()

    def _sync_preview_selectors(self):
        if not hasattr(self, 'preview_win') or self.preview_win is None or not self.preview_win.winfo_exists():
            return
        w_names = [w["name"] for w in all_weapons]
        if hasattr(self, 'pw_weapon_opt') and self.pw_weapon_opt.winfo_exists():
            self.pw_weapon_opt.configure(values=w_names)
            selected_w = [w["name"] for w in all_weapons if self.weapon_vars[w["id"]].get()]
            if selected_w:
                self.pw_weapon_var.set(selected_w[0])

        valid_ext = ('.jpg', '.jpeg', '.png')
        tex_files = [f for f in os.listdir(self.in_dir) if f.lower().endswith(valid_ext)] if os.path.exists(self.in_dir) else []
        if hasattr(self, 'pw_tex_opt') and self.pw_tex_opt.winfo_exists() and tex_files:
            self.pw_tex_opt.configure(values=tex_files)
            selected_tex = [tex for tex, var in self.texture_vars.items() if var.get()]
            if selected_tex:
                self.pw_tex_var.set(selected_tex[0])

    def create_preview_window(self):
        self.preview_win = ctk.CTkToplevel(self)
        self.preview_win.title("Live Skin Preview - Antigravity CS2 Skin Forge")
        self.preview_win.transient(self)
        self.preview_win.attributes("-topmost", True)
        
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        pw_w = min(1120, sw - 40)
        pw_h = min(820, sh - 80)
        cx = max(10, int(sw / 2 - pw_w / 2))
        cy = max(10, int(sh / 2 - pw_h / 2))
        self.preview_win.geometry(f"{pw_w}x{pw_h}+{cx}+{cy}")
        self.preview_win.minsize(860, 660)
        
        try:
            self.preview_win.after(200, lambda: self.preview_win.iconbitmap(icon_path) if os.path.exists(icon_path) else None)
        except Exception:
            pass
            
        self.preview_win.protocol("WM_DELETE_WINDOW", self._on_preview_close)

        # Force stay on top of the parent window
        self.preview_win.lift()
        self.preview_win.focus_force()
        self.preview_win.after(60, lambda: [self.preview_win.lift(), self.preview_win.focus_force()] if self.preview_win and self.preview_win.winfo_exists() else None)
        self.preview_win.after(180, lambda: [self.preview_win.lift()] if self.preview_win and self.preview_win.winfo_exists() else None)

        # 1. Header bar
        pw_header = ctk.CTkFrame(self.preview_win, fg_color="#18181b", height=46, corner_radius=0, border_width=1, border_color="#27272a")
        pw_header.pack(side="top", fill="x", padx=0, pady=0)
        
        # Dedicated right button box (packed first with priority to guarantee no button squeezing)
        pw_btn_box = ctk.CTkFrame(pw_header, fg_color="transparent")
        pw_btn_box.pack(side="right", padx=14, pady=6)

        self.pw_btn_refresh = ctk.CTkButton(
            pw_btn_box,
            text="Update Preview",
            image=self.icon_builder.refresh((15, 15)),
            compound="left",
            width=0,
            height=28,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.trigger_live_preview,
            **STYLE_BTN_PRIMARY_3D
        )
        self.pw_btn_refresh.pack(side="left", padx=(0, 8))

        self.pw_btn_render = ctk.CTkButton(
            pw_btn_box,
            text="Render All Skins",
            image=self.icon_builder.cube3d((16, 16)),
            compound="left",
            width=0,
            height=28,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.start_generation,
            **STYLE_BTN_HERO_3D
        )
        self.pw_btn_render.pack(side="left")

        # Left title and status container
        pw_info_box = ctk.CTkFrame(pw_header, fg_color="transparent")
        pw_info_box.pack(side="left", fill="x", expand=True, padx=(14, 8), pady=6)

        self.pw_title_lbl = ctk.CTkLabel(
            pw_info_box,
            text="Preview: Initializing...",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#f4f4f5",
            anchor="w"
        )
        self.pw_title_lbl.pack(side="left")

        self.pw_status_lbl = ctk.CTkLabel(
            pw_info_box,
            text="● Ready",
            text_color="#10b981",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        self.pw_status_lbl.pack(side="left", padx=12)

        # 2. Bottom Controls (PACK THIS FIRST with side="bottom" so controls NEVER get hidden!)
        pw_controls = ctk.CTkFrame(self.preview_win, **STYLE_CARD)
        pw_controls.pack(side="bottom", fill="x", padx=16, pady=(6, 12))
        pw_controls.grid_columnconfigure(1, weight=1)
        pw_controls.grid_columnconfigure(4, weight=1)

        # Helper function to build a preview slider control cell
        def _build_pw_slider_cell(row, col_lbl, col_box, col_val, key, pad_r=(4, 14)):
            s = self.slider_defs[key]
            lbl = ctk.CTkLabel(pw_controls, text=s['title'], width=110 if col_lbl == 0 else 95, anchor="w", font=ctk.CTkFont(size=12, weight="normal"), text_color="#e4e4e7")
            lbl.grid(row=row, column=col_lbl, padx=(14, 4), pady=3, sticky="w")
            s["pw_lbl"] = lbl

            slider_box = ctk.CTkFrame(pw_controls, fg_color="transparent")
            slider_box.grid(row=row, column=col_box, padx=4, pady=3, sticky="ew")

            btn_dec = ctk.CTkButton(
                slider_box,
                text="",
                image=self.icon_builder.arrow_left((10, 10)),
                width=22,
                height=22,
                command=lambda k=key: self.step_slider(k, -1),
                **STYLE_BTN_STEPPER_INACTIVE
            )
            btn_dec.pack(side="left", padx=(0, 2))
            s["pw_btn_dec"] = btn_dec

            slider = ctk.CTkSlider(
                slider_box,
                from_=s["from_"],
                to=s["to"],
                variable=s["var"],
                command=lambda v, k=key: self._on_slider_command(k, v, source="pw"),
                **SLIDER_INACTIVE_STYLE
            )
            slider.pack(side="left", fill="x", expand=True)
            slider._canvas.bind("<Button-1>", lambda e, k=key: self.set_active_slider(k), add="+")
            slider.bind("<Button-1>", lambda e, k=key: self.set_active_slider(k), add="+")
            slider._canvas.bind("<ButtonRelease-1>", lambda e, k=key: self._on_slider_release(k), add="+")
            slider.bind("<ButtonRelease-1>", lambda e, k=key: self._on_slider_release(k), add="+")
            s["pw_slider"] = slider

            btn_inc = ctk.CTkButton(
                slider_box,
                text="",
                image=self.icon_builder.arrow_right((10, 10)),
                width=22,
                height=22,
                command=lambda k=key: self.step_slider(k, 1),
                **STYLE_BTN_STEPPER_INACTIVE
            )
            btn_inc.pack(side="left", padx=(2, 0))
            s["pw_btn_inc"] = btn_inc

            val_lbl = ctk.CTkLabel(pw_controls, text=s["fmt"](s["var"].get()), width=44, anchor="e", text_color="#a1a1aa")
            val_lbl.grid(row=row, column=col_val, padx=pad_r, pady=3)
            s["pw_val"] = val_lbl

            return lbl, slider, val_lbl

        # Row 0: Texture X & Texture Y
        self.pw_lbl_x, self.pw_slider_x, self.pw_val_x = _build_pw_slider_cell(0, 0, 1, 2, "tx", pad_r=(4, 14))
        self.pw_lbl_y, self.pw_slider_y, self.pw_val_y = _build_pw_slider_cell(0, 3, 4, 5, "ty", pad_r=(4, 10))

        btn_reset = ctk.CTkButton(
            pw_controls,
            text="Reset All",
            image=self.icon_builder.reset((14, 14)),
            compound="left",
            width=0,
            height=28,
            command=self._reset_offsets,
            **STYLE_BTN_SECONDARY_3D
        )
        btn_reset.grid(row=0, column=6, padx=(4, 14), pady=3, sticky="ew")

        # Row 1: Texture Scale & Lighting Rig
        self.pw_lbl_scale, self.pw_slider_scale, self.pw_val_scale = _build_pw_slider_cell(1, 0, 1, 2, "scale", pad_r=(4, 14))

        lbl_light_pw = ctk.CTkLabel(pw_controls, text="Lighting:", width=95, anchor="w", font=ctk.CTkFont(weight="bold"))
        lbl_light_pw.grid(row=1, column=3, padx=(14, 4), pady=3, sticky="w")

        self.pw_opt_lighting = ctk.CTkOptionMenu(
            pw_controls, variable=self.light_var,
            values=["Studio Pro", "Soft Workbench", "Bright Flat", "Dark Cinematic"],
            fg_color="#27272a", button_color="#3f3f46", button_hover_color="#52525b", width=140, dynamic_resizing=False,
            command=self._on_lighting_change
        )
        self.pw_opt_lighting.grid(row=1, column=4, padx=4, pady=3, sticky="ew")

        btn_scale_1x = ctk.CTkButton(
            pw_controls,
            text="1.0x Scale",
            image=self.icon_builder.scale_1x((14, 14)),
            compound="left",
            width=0,
            height=28,
            command=lambda: [self.slider_defs["scale"]["var"].set(1.0), self._sync_slider_value("scale", 1.0, source="program"), self.trigger_live_preview()],
            **STYLE_BTN_SECONDARY_3D
        )
        btn_scale_1x.grid(row=1, column=6, padx=(4, 14), pady=3, sticky="ew")

        # Row 2: Brightness & Contrast
        self.pw_lbl_b, self.pw_slider_b, self.pw_val_b = _build_pw_slider_cell(2, 0, 1, 2, "bright", pad_r=(4, 14))
        self.pw_lbl_c, self.pw_slider_c, self.pw_val_c = _build_pw_slider_cell(2, 3, 4, 5, "cont", pad_r=(4, 10))

        btn_reset_fx = ctk.CTkButton(
            pw_controls,
            text="Default FX",
            image=self.icon_builder.sliders((14, 14)),
            compound="left",
            width=0,
            height=28,
            command=self._reset_fx,
            **STYLE_BTN_SECONDARY_3D
        )
        btn_reset_fx.grid(row=2, column=6, padx=(4, 14), pady=3, sticky="ew")

        # Row 3: Saturation & Studio Background
        self.pw_lbl_sat, self.pw_slider_sat, self.pw_val_sat = _build_pw_slider_cell(3, 0, 1, 2, "sat", pad_r=(4, 14))

        lbl_bg_pw = ctk.CTkLabel(pw_controls, text="Background:", width=95, anchor="w", font=ctk.CTkFont(weight="bold"))
        lbl_bg_pw.grid(row=3, column=3, padx=(14, 4), pady=3, sticky="w")

        self.pw_bg_var = self.bg_var
        self.pw_opt_bg = ctk.CTkOptionMenu(
            pw_controls, variable=self.pw_bg_var,
            values=["Dark Grey (Default)", "Deep Blue", "Pure Black", "Pure White", "Green Screen"],
            fg_color="#27272a", button_color="#3f3f46", button_hover_color="#52525b", width=140, dynamic_resizing=False,
            command=self._on_bg_change
        )
        self.pw_opt_bg.grid(row=3, column=4, padx=4, pady=3, sticky="ew")

        # Row 3, Column 6: Texture Mirroring buttons (⇄ Flip X and ⇅ Flip Y)
        flip_btn_frame = ctk.CTkFrame(pw_controls, fg_color="transparent")
        flip_btn_frame.grid(row=3, column=6, padx=(4, 14), pady=3, sticky="ew")

        self.btn_pw_flip_x = ctk.CTkButton(
            flip_btn_frame,
            text="⇄ Flip X",
            width=50,
            height=28,
            command=self._toggle_flip_x,
            **STYLE_BTN_SECONDARY_3D
        )
        self.btn_pw_flip_x.pack(side="left", padx=(0, 4), expand=True, fill="x")

        self.btn_pw_flip_y = ctk.CTkButton(
            flip_btn_frame,
            text="⇅ Flip Y",
            width=50,
            height=28,
            command=self._toggle_flip_y,
            **STYLE_BTN_SECONDARY_3D
        )
        self.btn_pw_flip_y.pack(side="left", expand=True, fill="x")
        self._update_pw_flip_buttons()

        # Row 4: Helpful Tip with Keyboard Navigation Guide
        tip_lbl = ctk.CTkLabel(
            pw_controls,
            text="💡 Tip: Arrow keys / ◀ ▶ to nudge  •  Tab / 1-6 to switch slider  •  Shift for 5x  •  OptiX GPU+CPU (~0.2s)",
            text_color="#a1a1aa",
            font=ctk.CTkFont(size=11, slant="italic")
        )
        tip_lbl.grid(row=4, column=0, columnspan=7, padx=14, pady=(2, 6), sticky="w")

        # 3. Center Display Area (Responsive Viewport)
        self.pw_display_frame = ctk.CTkFrame(self.preview_win, fg_color="#09090b", corner_radius=10, border_width=1, border_color="#27272a")
        self.pw_display_frame.pack(side="top", fill="both", expand=True, padx=16, pady=(8, 4))
        self.pw_display_frame.bind("<Configure>", self._on_preview_viewport_resize)
        
        self.pw_image_lbl = ctk.CTkLabel(self.pw_display_frame, text="⚡ Rendering live preview...", font=ctk.CTkFont(size=16), text_color="#71717a")
        self.pw_image_lbl.pack(expand=True, fill="both", padx=8, pady=8)

        # Bind keyboard events to preview window as well
        self.preview_win.bind("<Key>", self._on_global_key)

        # Apply active highlight to preview sliders immediately
        self.set_active_slider(self.active_slider_key)

        # Automatically start initial preview render
        self.trigger_live_preview()

    def trigger_live_preview(self):
        if self.is_preview_running:
            self.preview_pending = True
            return
        
        selected_weapons = [w for w in all_weapons if self.weapon_vars[w["id"]].get()]
        if not selected_weapons:
            w = all_weapons[0] if all_weapons else None
        else:
            w = selected_weapons[0]

        if not w:
            if hasattr(self, 'pw_status_lbl') and self.pw_status_lbl.winfo_exists():
                self.pw_status_lbl.configure(text="No weapons found!", text_color="#ef4444")
            return

        selected_tex_paths = [os.path.join(self.in_dir, tex) for tex, var in self.texture_vars.items() if var.get()]
        if not selected_tex_paths:
            valid_ext = ('.jpg', '.jpeg', '.png')
            tex_files = [f for f in os.listdir(self.in_dir) if f.lower().endswith(valid_ext)] if os.path.exists(self.in_dir) else []
            tex_path = os.path.join(self.in_dir, tex_files[0]) if tex_files else None
        else:
            tex_path = selected_tex_paths[0]

        if not tex_path or not os.path.exists(tex_path):
            if hasattr(self, 'pw_status_lbl') and self.pw_status_lbl.winfo_exists():
                self.pw_status_lbl.configure(text="Please select a texture from the list!", text_color="#ef4444")
            return

        tex_name = os.path.basename(tex_path)
        disp_tex = tex_name if len(tex_name) <= 24 else tex_name[:21] + "..."
        if hasattr(self, 'pw_title_lbl') and self.pw_title_lbl.winfo_exists():
            self.pw_title_lbl.configure(text=f"{w['name']}  |  {disp_tex}")

        if hasattr(self, 'pw_status_lbl') and self.pw_status_lbl.winfo_exists():
            self.pw_status_lbl.configure(text="⚡ Rendering...", text_color="#ef4444")

        engine = self.engine_var.get()
        light = self.light_var.get()
        compute = self.compute_var.get()
        off_x = str(self.tex_off_x_var.get())
        off_y = str(self.tex_off_y_var.get())
        scale = str(self.tex_scale_var.get())
        flip_x = str(self.flip_x_var.get())
        flip_y = str(self.flip_y_var.get())

        self.is_preview_running = True
        threading.Thread(target=self._run_preview_render, args=(w, tex_path, engine, light, compute, off_x, off_y, scale, flip_x, flip_y), daemon=True).start()

    def _run_preview_render(self, w, tex_path, engine, light, compute, off_x, off_y, scale, flip_x, flip_y):
        preview_out = os.path.join(pipeline_folder, "_preview_temp.png")
        cmd = [
            self.blender_exe, "-b", "--python-exit-code", "1", "-P", blender_script, "--",
            os.path.abspath(w["obj"]), w["normal"], w["rough"], os.path.abspath(tex_path),
            os.path.abspath(preview_out), "SKIP",
            "Preview (540p | 4 Samples)", "True", engine, light, "PNG", compute,
            off_x, off_y, scale,
            flip_x, flip_y
        ]
        try:
            subprocess.run(cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            from PIL import Image
            self.preview_raw_render = Image.open(preview_out).convert("RGBA").copy()
            try:
                os.remove(preview_out)
            except Exception:
                pass
            self.after(0, self._render_preview_success)
        except Exception as e:
            self.after(0, lambda: self._render_preview_error(str(e)))

    def _render_preview_success(self):
        self.is_preview_running = False
        if hasattr(self, 'pw_status_lbl') and self.pw_status_lbl.winfo_exists():
            self.pw_status_lbl.configure(text="● Ready", text_color="#10b981")
        self._refresh_preview_postprocess()
        if getattr(self, 'preview_pending', False):
            self.preview_pending = False
            self.trigger_live_preview()

    def _render_preview_error(self, err):
        self.is_preview_running = False
        if hasattr(self, 'pw_status_lbl') and self.pw_status_lbl.winfo_exists():
            self.pw_status_lbl.configure(text="✖ Error", text_color="#ef4444")
        if getattr(self, 'preview_pending', False):
            self.preview_pending = False
            self.trigger_live_preview()

    def _refresh_preview_postprocess(self):
        if self.preview_raw_render is None:
            return
        if not hasattr(self, 'pw_image_lbl') or not self.pw_image_lbl.winfo_exists():
            return

        from PIL import Image, ImageEnhance
        render = self.preview_raw_render.copy()

        if abs(self.bright_var.get() - 1.0) > 0.001:
            render = ImageEnhance.Brightness(render).enhance(self.bright_var.get())
        if abs(self.cont_var.get() - 1.0) > 0.001:
            render = ImageEnhance.Contrast(render).enhance(self.cont_var.get())
        if abs(self.sat_var.get() - 1.0) > 0.001:
            render = ImageEnhance.Color(render).enhance(self.sat_var.get())

        bg_colors = {
            "Dark Grey (Default)": (20, 20, 24, 255),
            "Deep Blue": (15, 20, 35, 255),
            "Pure Black": (0, 0, 0, 255),
            "Pure White": (255, 255, 255, 255),
            "Green Screen": (0, 255, 0, 255)
        }
        if not self.trans_var.get():
            bg = Image.new("RGBA", render.size, bg_colors.get(self.bg_var.get(), (20, 20, 24, 255)))
            bg.paste(render, (0, 0), render)
            render = bg

        if hasattr(self, 'pw_display_frame') and self.pw_display_frame.winfo_exists():
            fw = self.pw_display_frame.winfo_width()
            fh = self.pw_display_frame.winfo_height()
            if fw > 100 and fh > 100:
                avail_w = max(320, fw - 24)
                avail_h = max(180, fh - 24)
                aspect = 16.0 / 9.0
                if avail_w / avail_h > aspect:
                    disp_h = int(avail_h)
                    disp_w = int(disp_h * aspect)
                else:
                    disp_w = int(avail_w)
                    disp_h = int(disp_w / aspect)
            else:
                disp_w, disp_h = 920, 518
        else:
            disp_w, disp_h = 920, 518

        render_disp = render.copy()
        if render_disp.size != (disp_w, disp_h):
            render_disp = render_disp.resize((disp_w, disp_h), Image.Resampling.BILINEAR)
        ctk_img = ctk.CTkImage(light_image=render_disp, dark_image=render_disp, size=(disp_w, disp_h))
        
        self.pw_image_lbl.configure(image=ctk_img, text="")
        self.pw_image_lbl.image = ctk_img

    def start_generation(self):
        self.btn_generate.configure(state="disabled", text="FORGING SKINS IN PROGRESS...")
        if hasattr(self, 'pw_btn_render') and self.pw_btn_render and self.pw_btn_render.winfo_exists():
            self.pw_btn_render.configure(state="disabled", text="Forging Skins...")
        self.progress_bar.set(0)
        self.lbl_status.configure(text="⚡ Initializing headless Blender engine...", text_color="#eab308")
        threading.Thread(target=self.run_pipeline, daemon=True).start()

    def run_pipeline(self):
        selected_tex_paths = [os.path.join(self.in_dir, tex) for tex, var in self.texture_vars.items() if var.get()]
        if not selected_tex_paths:
            self.log("ERROR: Please select at least one Texture from the checklist!")
            self.btn_generate.configure(state="normal", text="GENERATE 3D SKINS & RENDERS")
            if hasattr(self, 'pw_btn_render') and self.pw_btn_render and self.pw_btn_render.winfo_exists():
                self.pw_btn_render.configure(state="normal", text="Render All Skins")
            return
            
        selected_weapons = [w for w in all_weapons if self.weapon_vars[w["id"]].get()]
        if not selected_weapons:
            self.log("ERROR: Please select at least one weapon model!")
            self.btn_generate.configure(state="normal", text="GENERATE 3D SKINS & RENDERS")
            if hasattr(self, 'pw_btn_render') and self.pw_btn_render and self.pw_btn_render.winfo_exists():
                self.pw_btn_render.configure(state="normal", text="Render All Skins")
            return
            
        jobs = []
        if self.mode_var.get() == "random":
            for w in selected_weapons:
                tex = random.choice(selected_tex_paths)
                jobs.append((w, tex))
        else:
            for w in selected_weapons:
                for tex in selected_tex_paths:
                    jobs.append((w, tex))
                    
        total_jobs = len(jobs)
        q_preset = self.quality_var.get()
        self.log(f"Warming up headless Blender engine... [{q_preset}] [Compute: {self.compute_var.get()}]")
        self.log(f"Queued {total_jobs} unique skins for compilation.")
        
        bg_colors = {
            "Dark Grey (Default)": (20, 20, 24, 255),
            "Deep Blue": (15, 20, 35, 255),
            "Pure Black": (0, 0, 0, 255),
            "Pure White": (255, 255, 255, 255),
            "Green Screen": (0, 255, 0, 255)
        }
        
        for i, (w, tex_path) in enumerate(jobs):
            tex_name = os.path.basename(tex_path)
            self.log(f"[{i+1}/{total_jobs}] Rendering {w['name']} with {tex_name} (Scale: {self.tex_scale_var.get():.2f}x)...")
            ext = ".png" if self.fmt_var.get() == "PNG" else ".jpg"
            clean_base_tex = os.path.splitext(tex_name)[0].split('_')[0]
            out_img = os.path.join(self.out_dir, f"True3D_{w['id']}_{clean_base_tex}_PlaySide{ext}")
            blend_out = "SKIP"
            if self.blend_var.get():
                blend_out = os.path.join(self.blend_dir, f"True3D_{w['id']}_{clean_base_tex}_Project.blend")
                
            cmd = [
                self.blender_exe, "-b", "--python-exit-code", "1", "-P", blender_script, "--",
                os.path.abspath(w["obj"]), w["normal"], w["rough"], os.path.abspath(tex_path),
                os.path.abspath(out_img), os.path.abspath(blend_out) if blend_out != "SKIP" else "SKIP", 
                q_preset, str(self.trans_var.get()), self.engine_var.get(), self.light_var.get(), self.fmt_var.get(), self.compute_var.get(),
                str(self.tex_off_x_var.get()), str(self.tex_off_y_var.get()), str(self.tex_scale_var.get()),
                str(self.flip_x_var.get()), str(self.flip_y_var.get())
            ]
            
            try:
                subprocess.run(cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                
                # Apply post-processing using Python PIL
                from PIL import Image, ImageEnhance
                render = Image.open(out_img).convert("RGBA")
                
                # Apply sliders
                if abs(self.bright_var.get() - 1.0) > 0.001:
                    render = ImageEnhance.Brightness(render).enhance(self.bright_var.get())
                if abs(self.cont_var.get() - 1.0) > 0.001:
                    render = ImageEnhance.Contrast(render).enhance(self.cont_var.get())
                if abs(self.sat_var.get() - 1.0) > 0.001:
                    render = ImageEnhance.Color(render).enhance(self.sat_var.get())
                
                if not self.trans_var.get() and self.fmt_var.get() == "PNG":
                    bg = Image.new("RGBA", render.size, bg_colors.get(self.bg_var.get(), (20, 20, 24, 255)))
                    bg.paste(render, (0, 0), render)
                    render = bg
                elif not self.trans_var.get() and self.fmt_var.get() == "JPEG":
                    bg = Image.new("RGB", render.size, bg_colors.get(self.bg_var.get(), (20, 20, 24, 255))[:3])
                    bg.paste(render, (0, 0), render)
                    render = bg
                    
                render.save(out_img)
                self.log(f"SUCCESS: Exported {os.path.basename(out_img)}")
                
            except Exception as e:
                self.log(f"FAILED: Blender execution error on {w['name']}.")
                
            self.progress_bar.set((i + 1) / total_jobs)
            
        self.log("Pipeline cycle complete! All assets forged.")
        self.btn_generate.configure(state="normal", text="GENERATE 3D SKINS & RENDERS")
        if hasattr(self, 'pw_btn_render') and self.pw_btn_render and self.pw_btn_render.winfo_exists():
            self.pw_btn_render.configure(state="normal", text="Render All Skins")
        self.after(0, self.show_completion_popup)

    def open_image_resizer(self):
        valid_ext = ('.jpg', '.jpeg', '.png')
        tex_files = [f for f in os.listdir(self.in_dir) if f.lower().endswith(valid_ext)] if os.path.exists(self.in_dir) else []
        if not tex_files:
            self.log("ERROR: No image textures found in Input directory to resize.")
            return

        selected_tex = [tex for tex, var in self.texture_vars.items() if var.get()]
        initial_tex = selected_tex[0] if selected_tex else tex_files[0]

        win = ctk.CTkToplevel(self)
        win.title("Resize Texture Image - Antigravity CS2 Skin Forge")
        win.geometry("540x510")
        win.transient(self)
        win.attributes('-topmost', True)
        try:
            win.after(200, lambda: win.iconbitmap(icon_path) if os.path.exists(icon_path) else None)
        except Exception:
            pass

        win.lift()
        win.focus_force()

        frame = ctk.CTkFrame(win, **STYLE_CARD)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        lbl_head = ctk.CTkLabel(frame, text="  Texture Image Resizer", image=self.icon_builder.resize((20, 20)), compound="left", font=ctk.CTkFont(size=18, weight="bold"), text_color="#f4f4f5")
        lbl_head.pack(padx=15, pady=(15, 10), anchor="w")

        row_tex = ctk.CTkFrame(frame, fg_color="transparent")
        row_tex.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(row_tex, text="Select Image:", font=ctk.CTkFont(weight="bold"), width=110, anchor="w").pack(side="left")
        res_tex_var = ctk.StringVar(value=initial_tex)
        opt_tex = ctk.CTkOptionMenu(row_tex, variable=res_tex_var, values=tex_files, fg_color="#27272a", button_color="#3f3f46", button_hover_color="#52525b", dynamic_resizing=False)
        opt_tex.pack(side="left", fill="x", expand=True)

        lbl_info = ctk.CTkLabel(frame, text="", text_color="#a1a1aa", font=ctk.CTkFont(size=12))
        lbl_info.pack(padx=15, pady=2, anchor="w")

        from PIL import Image

        lbl_presets = ctk.CTkLabel(frame, text="Resolution Presets:", font=ctk.CTkFont(weight="bold"))
        lbl_presets.pack(padx=15, pady=(10, 4), anchor="w")

        preset_frame = ctk.CTkFrame(frame, fg_color="transparent")
        preset_frame.pack(fill="x", padx=15, pady=2)

        dim_frame = ctk.CTkFrame(frame, fg_color="transparent")
        dim_frame.pack(fill="x", padx=15, pady=8)
        
        ctk.CTkLabel(dim_frame, text="Width (px):", width=80, anchor="w").pack(side="left")
        entry_w = ctk.CTkEntry(dim_frame, width=90, fg_color="#27272a")
        entry_w.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(dim_frame, text="Height (px):", width=80, anchor="w").pack(side="left")
        entry_h = ctk.CTkEntry(dim_frame, width=90, fg_color="#27272a")
        entry_h.pack(side="left", padx=(0, 15))

        save_mode_var = ctk.StringVar(value="new")
        save_frame = ctk.CTkFrame(frame, fg_color="transparent")
        save_frame.pack(fill="x", padx=15, pady=5)
        rb_new = ctk.CTkRadioButton(save_frame, text="Save as new file", variable=save_mode_var, value="new", fg_color="#ef4444", hover_color="#dc2626")
        rb_new.pack(side="left", padx=(0, 15))
        rb_overwrite = ctk.CTkRadioButton(save_frame, text="Overwrite original", variable=save_mode_var, value="overwrite", fg_color="#ef4444", hover_color="#dc2626")
        rb_overwrite.pack(side="left")

        lbl_status = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=12))
        lbl_status.pack(padx=15, pady=4)

        current_dims = [2048, 2048]

        def update_info(*args):
            p = os.path.join(self.in_dir, res_tex_var.get())
            if os.path.exists(p):
                try:
                    with Image.open(p) as im:
                        w, h = im.size
                        current_dims[0] = w
                        current_dims[1] = h
                        size_mb = os.path.getsize(p) / (1024 * 1024)
                        lbl_info.configure(text=f"Original Resolution: {w} × {h} px  |  File Size: {size_mb:.2f} MB")
                        entry_w.delete(0, "end"); entry_w.insert(0, str(w))
                        entry_h.delete(0, "end"); entry_h.insert(0, str(h))
                except Exception as ex:
                    lbl_info.configure(text=f"Could not read image: {ex}")

        res_tex_var.trace_add("write", update_info)
        update_info()

        def apply_preset(target_w, target_h=None):
            orig_w, orig_h = current_dims
            if target_h is None:
                if orig_w >= orig_h:
                    target_h = max(1, int(target_w * (orig_h / orig_w)))
                else:
                    target_h = target_w
                    target_w = max(1, int(target_h * (orig_w / orig_h)))
            entry_w.delete(0, "end"); entry_w.insert(0, str(target_w))
            entry_h.delete(0, "end"); entry_h.insert(0, str(target_h))

        btn_4k = ctk.CTkButton(preset_frame, text="4K (3840)", width=0, height=28, command=lambda: apply_preset(3840), **STYLE_BTN_SECONDARY_3D)
        btn_4k.pack(side="left", padx=(0, 5))
        btn_2k = ctk.CTkButton(preset_frame, text="2K (2048)", width=0, height=28, command=lambda: apply_preset(2048), **STYLE_BTN_SECONDARY_3D)
        btn_2k.pack(side="left", padx=5)
        btn_1k = ctk.CTkButton(preset_frame, text="1K (1024)", width=0, height=28, command=lambda: apply_preset(1024), **STYLE_BTN_SECONDARY_3D)
        btn_1k.pack(side="left", padx=5)
        btn_512 = ctk.CTkButton(preset_frame, text="512px", width=0, height=28, command=lambda: apply_preset(512), **STYLE_BTN_SECONDARY_3D)
        btn_512.pack(side="left", padx=5)
        btn_half = ctk.CTkButton(preset_frame, text="50%", width=0, height=28, command=lambda: apply_preset(max(1, current_dims[0]//2), max(1, current_dims[1]//2)), **STYLE_BTN_SECONDARY_3D)
        btn_half.pack(side="left", padx=5)

        def do_resize():
            try:
                nw = int(entry_w.get().strip())
                nh = int(entry_h.get().strip())
                if nw <= 0 or nh <= 0:
                    lbl_status.configure(text="Dimensions must be positive integers!", text_color="#ef4444")
                    return
                src_p = os.path.join(self.in_dir, res_tex_var.get())
                if not os.path.exists(src_p):
                    lbl_status.configure(text="Source file not found!", text_color="#ef4444")
                    return

                with Image.open(src_p) as im:
                    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
                    base, ext = os.path.splitext(res_tex_var.get())
                    if save_mode_var.get() == "overwrite":
                        dest_p = src_p
                        dest_name = res_tex_var.get()
                    else:
                        dest_name = f"{base}_{nw}x{nh}{ext}"
                        dest_p = os.path.join(self.in_dir, dest_name)
                    
                    if ext.lower() in ('.jpg', '.jpeg'):
                        resized.convert("RGB").save(dest_p, quality=95, optimize=True)
                    else:
                        resized.save(dest_p)
                
                self.refresh_textures()
                if dest_name in self.texture_vars:
                    self.deselect_all_tex()
                    self.texture_vars[dest_name].set(True)
                    self._on_item_toggle()
                
                self.log(f"Resized image saved: {dest_name} ({nw}x{nh})")
                win.destroy()
            except Exception as e:
                lbl_status.configure(text=f"Error: {e}", text_color="#ef4444")

        btn_run = ctk.CTkButton(
            frame,
            text="Resize & Apply Texture",
            image=self.icon_builder.resize((16, 16)),
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=40,
            command=do_resize,
            **STYLE_BTN_PRIMARY_3D
        )
        btn_run.pack(fill="x", padx=15, pady=(12, 15))

if __name__ == "__main__":
    app = CS2SkinGeneratorApp()
    app.mainloop()
