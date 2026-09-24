import os
import sys
import subprocess
import random
import threading
import glob
import shutil
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
obj_path, normal_path, rough_path, tex_path, out_path, blend_path, quality, transparent, engine, lighting, fmt, compute_device, tex_offset_x, tex_offset_y = argv
tex_offset_x = -float(tex_offset_x)
tex_offset_y = -float(tex_offset_y)

bpy.ops.wm.read_factory_settings(use_empty=True)
if "Cycles" in engine:
    try:
        import addon_utils
        addon_utils.enable('cycles')
    except:
        pass
    bpy.context.scene.render.engine = 'CYCLES'
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'CUDA'
        prefs.get_devices()
        for d in prefs.devices:
            d.use = True
    except:
        pass
    bpy.context.scene.cycles.device = compute_device
    bpy.context.scene.cycles.use_denoising = True
else:
    for eng_candidate in ['BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE']:
        try:
            bpy.context.scene.render.engine = eng_candidate
            break
        except Exception:
            pass

bpy.context.scene.render.film_transparent = True if transparent == "True" else False

if quality in ("Preview (480p | 8 Samples)", "Preview (540p | 8 Samples)"): res_x, res_y, samples = 960, 540, 8
elif quality == "Standard (1080p | 32 Samples)": res_x, res_y, samples = 1920, 1080, 32
elif quality == "High (1440p | 64 Samples)": res_x, res_y, samples = 2560, 1440, 64
elif quality == "Ultra (4K | 256 Samples)": res_x, res_y, samples = 3840, 2160, 256
elif quality == "Masterpiece (8K | 512 Samples)": res_x, res_y, samples = 7680, 4320, 512
else: res_x, res_y, samples = 2560, 1440, 64

bpy.context.scene.render.resolution_x = res_x
bpy.context.scene.render.resolution_y = res_y
if bpy.context.scene.render.engine == 'CYCLES':
    bpy.context.scene.cycles.samples = samples
else:
    try:
        bpy.context.scene.eevee.taa_render_samples = samples
    except:
        pass

try: bpy.ops.wm.obj_import(filepath=obj_path)
except:
    try: bpy.ops.import_scene.obj(filepath=obj_path)
    except: pass

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
map_node = nodes.new("ShaderNodeMapping")
tex_ratio = tex_node.image.size[0] / tex_node.image.size[1]
map_node.inputs['Scale'].default_value = (render_ratio / tex_ratio, 1.0, 1.0)
map_node.inputs['Location'].default_value = (tex_offset_x, tex_offset_y, 0.0)
links.new(tc_node.outputs["Window"], map_node.inputs["Vector"])
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
    bsdf.inputs['Roughness'].default_value = 0.5
bsdf.inputs['Metallic'].default_value = 0.5

for m in meshes:
    m.data.materials.clear()
    m.data.materials.append(mat)

def add_light(name, base_energy, offset_x, offset_y, offset_z, radius_mult):
    l_data = bpy.data.lights.new(name=name, type="AREA")
    l_data.energy = base_energy * (max_dim ** 2) * 5.0
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

if lighting == "Studio Pro":
    add_light("Key", 50, -0.5, 1.0, 0.5, 0.5)
    add_light("Fill", 10, 0.5, 1.0, -0.5, 1.0)
    add_light("Rim", 250, 0.2, -0.8, 0.5, 0.2)
elif lighting == "Bright Flat":
    add_light("Front", 80, 0.0, 1.0, 0.2, 2.0)
    add_light("Back", 40, 0.0, -1.0, 0.2, 2.0)
elif lighting == "Dark Cinematic":
    add_light("Key", 15, -0.8, 0.8, 0.2, 0.2)
    add_light("Rim", 500, 0.5, -0.8, 0.8, 0.1)

bpy.ops.file.pack_all()
if blend_path != "SKIP":
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

class CS2SkinGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Antigravity CS2 Skin Forge v1.1.0")
        
        window_width = 1450
        window_height = 750
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = max(10, int(screen_width / 2 - window_width / 2))
        center_y = max(10, int(screen_height / 2 - window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        try:
            self.iconbitmap(icon_path)
        except Exception:
            pass

        self.blender_exe = blender_exe
        self.in_dir = default_input_folder
        self.out_dir = default_out_folder
        self.blend_dir = default_blend_folder

        self.preview_win = None
        self.preview_raw_render = None
        self.is_preview_running = False

        # ---------------- TOP RIBBON MENU ----------------
        self.top_bar = ctk.CTkFrame(self, height=34, corner_radius=0, fg_color="#1f1f23")
        self.top_bar.pack(side="top", fill="x")

        self.file_var = ctk.StringVar(value="File")
        self.file_menu = ctk.CTkOptionMenu(self.top_bar, variable=self.file_var, 
                                           values=["Open Input Directory", "Open Output Directory", "Open Project Directory", "Exit"],
                                           command=self.handle_file_menu,
                                           width=70, fg_color="#1f1f23", button_color="#1f1f23", button_hover_color="#3f3f46", text_color="#f4f4f5",
                                           dynamic_resizing=False)
        self.file_menu.pack(side="left", padx=5, pady=3)

        self.edit_var = ctk.StringVar(value="Edit")
        self.edit_menu = ctk.CTkOptionMenu(self.top_bar, variable=self.edit_var, 
                                           values=["Select All Models", "Deselect All Models", "Select Random Model (3)"],
                                           command=self.handle_edit_menu,
                                           width=70, fg_color="#1f1f23", button_color="#1f1f23", button_hover_color="#3f3f46", text_color="#f4f4f5",
                                           dynamic_resizing=False)
        self.edit_menu.pack(side="left", padx=5, pady=3)

        self.config_var = ctk.StringVar(value="Configure")
        self.config_menu = ctk.CTkOptionMenu(self.top_bar, variable=self.config_var, 
                                             values=["Set Input Textures Directory", "Set Output Renders Directory", "Set Output Projects Directory", "Set Blender Executable Path"],
                                             command=self.handle_config_menu,
                                             width=90, fg_color="#1f1f23", button_color="#1f1f23", button_hover_color="#3f3f46", text_color="#f4f4f5",
                                             dynamic_resizing=False)
        self.config_menu.pack(side="left", padx=5, pady=3)
        
        self.help_var = ctk.StringVar(value="Help")
        self.help_menu = ctk.CTkOptionMenu(self.top_bar, variable=self.help_var, 
                                           values=["View Documentation", "About"],
                                           command=self.handle_help_menu,
                                           width=70, fg_color="#1f1f23", button_color="#1f1f23", button_hover_color="#3f3f46", text_color="#f4f4f5",
                                           dynamic_resizing=False)
        self.help_menu.pack(side="left", padx=5, pady=3)

        self.btn_top_preview = ctk.CTkButton(self.top_bar, text="👁 Live Preview", font=ctk.CTkFont(size=12, weight="bold"),
                                             fg_color="#ef4444", hover_color="#dc2626", text_color="#ffffff",
                                             height=26, width=130, command=self.toggle_preview_window)
        self.btn_top_preview.pack(side="right", padx=10, pady=3)

        # ---------------- DIRECTORY FOOTER ----------------
        self.footer_toggle = ctk.CTkButton(self, text="▼ Show Active Directories", fg_color="#1f1f23", hover_color="#27272a", text_color="#a1a1aa", corner_radius=0, height=24, command=self.toggle_dirs)
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
        self.main_container.grid_columnconfigure(0, weight=6)
        self.main_container.grid_columnconfigure(1, weight=4)
        self.main_container.grid_rowconfigure(0, weight=1)

        # ==========================================
        # LEFT COLUMN (60% width): Textures & Weapons
        # ==========================================
        self.left_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(15, 5), pady=15)

        # 1. TEXTURE SELECTION BLOCK
        self.tex_container = ctk.CTkFrame(self.left_frame, fg_color="#18181b", corner_radius=10)
        self.tex_container.pack(fill="x", pady=(0, 15))
        
        self.tex_top = ctk.CTkFrame(self.tex_container, fg_color="transparent")
        self.tex_top.pack(fill="x", padx=15, pady=(15, 5))
        self.lbl_tex = ctk.CTkLabel(self.tex_top, text="Texture Selection", font=ctk.CTkFont(size=18, weight="bold"), text_color="#f4f4f5")
        self.lbl_tex.pack(side="left")
        
        self.btn_tex_none = ctk.CTkButton(self.tex_top, text="Deselect All", width=80, height=24, fg_color="#3f3f46", hover_color="#52525b", command=self.deselect_all_tex)
        self.btn_tex_none.pack(side="right", padx=(5,0))
        self.btn_tex_all = ctk.CTkButton(self.tex_top, text="Select All", width=80, height=24, fg_color="#3f3f46", hover_color="#52525b", command=self.select_all_tex)
        self.btn_tex_all.pack(side="right")
        self.btn_tex_refresh = ctk.CTkButton(self.tex_top, text="⟳ Refresh", width=80, height=24, fg_color="#3f3f46", hover_color="#52525b", command=self.refresh_textures)
        self.btn_tex_refresh.pack(side="right", padx=(0, 5))

        self.grid_textures = ctk.CTkScrollableFrame(self.tex_container, fg_color="#27272a", corner_radius=10, height=190)
        self.grid_textures.pack(fill="x", padx=15, pady=(5, 15))
        self.grid_textures.grid_columnconfigure(0, weight=1)
        self.texture_vars = {}
        self.refresh_textures()

        # 2. WEAPON MODEL SELECTION BLOCK (5-column grid)
        self.weap_container = ctk.CTkFrame(self.left_frame, fg_color="#18181b", corner_radius=10)
        self.weap_container.pack(fill="both", expand=True)

        self.weap_top = ctk.CTkFrame(self.weap_container, fg_color="transparent")
        self.weap_top.pack(fill="x", padx=15, pady=(15, 5))
        self.lbl_weapons = ctk.CTkLabel(self.weap_top, text="Weapon Model Selection", font=ctk.CTkFont(size=18, weight="bold"), text_color="#f4f4f5")
        self.lbl_weapons.pack(side="left")

        self.btn_sel_none = ctk.CTkButton(self.weap_top, text="Deselect All", width=80, height=24, fg_color="#3f3f46", hover_color="#52525b", command=self.deselect_all)
        self.btn_sel_none.pack(side="right", padx=(5,0))
        self.btn_sel_all = ctk.CTkButton(self.weap_top, text="Select All", width=80, height=24, fg_color="#3f3f46", hover_color="#52525b", command=self.select_all)
        self.btn_sel_all.pack(side="right", padx=5)
        self.btn_sel_rand = ctk.CTkButton(self.weap_top, text="Random Pick (3)", width=105, height=24, fg_color="#3f3f46", hover_color="#52525b", command=self.select_random)
        self.btn_sel_rand.pack(side="right", padx=5)

        self.grid_weapons = ctk.CTkScrollableFrame(self.weap_container, fg_color="#27272a", corner_radius=10)
        self.grid_weapons.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        self.weapon_vars = {}
        for i, w in enumerate(all_weapons):
            col = i % 5
            row = i // 5
            var = ctk.BooleanVar(value=False)
            chk = ctk.CTkCheckBox(self.grid_weapons, text=w["name"], variable=var, font=ctk.CTkFont(size=13),
                                  fg_color="#ef4444", hover_color="#dc2626", command=self._on_item_toggle)
            chk.grid(row=row, column=col, sticky="w", padx=12, pady=7)
            self.weapon_vars[w["id"]] = var
            self.grid_weapons.grid_columnconfigure(col, weight=1)

        # ==========================================
        # RIGHT COLUMN (40% width): Settings, Post-Process, Console, Generate
        # ==========================================
        self.right_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 15), pady=15)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # 3. SETTINGS BLOCK
        self.settings_container = ctk.CTkFrame(self.right_frame, fg_color="#18181b", corner_radius=10)
        self.settings_container.pack(fill="x", pady=(0, 12))
        self.settings_container.grid_columnconfigure(0, weight=1, uniform="a")
        self.settings_container.grid_columnconfigure(1, weight=1, uniform="a")
        
        self.lbl_settings = ctk.CTkLabel(self.settings_container, text="Rendering Engine Options", font=ctk.CTkFont(size=18, weight="bold"), text_color="#f4f4f5")
        self.lbl_settings.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(12, 4))

        self.lbl_eng = ctk.CTkLabel(self.settings_container, text="Render Engine:")
        self.lbl_eng.grid(row=1, column=0, sticky="w", padx=15)
        self.engine_var = ctk.StringVar(value="Cycles Raytracing")
        self.opt_engine = ctk.CTkOptionMenu(self.settings_container, variable=self.engine_var, values=["Cycles Raytracing", "BLENDER_EEVEE_NEXT"],
                                            fg_color="#27272a", button_color="#3f3f46", dynamic_resizing=False)
        self.opt_engine.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 8))

        self.lbl_dev = ctk.CTkLabel(self.settings_container, text="Compute Device:")
        self.lbl_dev.grid(row=1, column=1, sticky="w", padx=15)
        self.compute_var = ctk.StringVar(value="GPU")
        self.opt_compute = ctk.CTkOptionMenu(self.settings_container, variable=self.compute_var, values=["GPU", "CPU"],
                                             fg_color="#27272a", button_color="#3f3f46", dynamic_resizing=False)
        self.opt_compute.grid(row=2, column=1, sticky="ew", padx=15, pady=(0, 8))

        self.lbl_quality = ctk.CTkLabel(self.settings_container, text="Quality Preset:")
        self.lbl_quality.grid(row=3, column=0, sticky="w", padx=15)
        self.quality_var = ctk.StringVar(value="High (1440p | 64 Samples)")
        self.opt_quality = ctk.CTkOptionMenu(self.settings_container, variable=self.quality_var,
                                            values=["Standard (1080p | 32 Samples)", "High (1440p | 64 Samples)", "Ultra (4K | 256 Samples)", "Masterpiece (8K | 512 Samples)"],
                                            fg_color="#27272a", button_color="#3f3f46", dynamic_resizing=False)
        self.opt_quality.grid(row=4, column=0, sticky="ew", padx=15, pady=(0, 8))

        self.lbl_bg = ctk.CTkLabel(self.settings_container, text="Studio Background:")
        self.lbl_bg.grid(row=3, column=1, sticky="w", padx=15)
        self.bg_var = ctk.StringVar(value="Dark Grey (Default)")
        self.opt_bg = ctk.CTkOptionMenu(self.settings_container, variable=self.bg_var,
                                        values=["Dark Grey (Default)", "Deep Blue", "Pure Black", "Pure White", "Green Screen"],
                                        fg_color="#27272a", button_color="#3f3f46", dynamic_resizing=False, command=self._on_bg_change)
        self.opt_bg.grid(row=4, column=1, sticky="ew", padx=15, pady=(0, 8))
        
        self.chk_grid = ctk.CTkFrame(self.settings_container, fg_color="transparent")
        self.chk_grid.grid(row=5, column=0, columnspan=2, sticky="w", padx=15, pady=4)
        self.blend_var = ctk.BooleanVar(value=True)
        self.chk_blend = ctk.CTkCheckBox(self.chk_grid, text="Export .blend Project", variable=self.blend_var, fg_color="#ef4444", hover_color="#dc2626")
        self.chk_blend.pack(side="left", padx=(0, 20))
        self.trans_var = ctk.BooleanVar(value=False)
        self.chk_trans = ctk.CTkCheckBox(self.chk_grid, text="Transparent Background", variable=self.trans_var,
                                         fg_color="#ef4444", hover_color="#dc2626", command=self._on_trans_toggle)
        self.chk_trans.pack(side="left")

        self.mode_grid = ctk.CTkFrame(self.settings_container, fg_color="transparent")
        self.mode_grid.grid(row=6, column=0, columnspan=2, sticky="w", padx=15, pady=(4, 12))
        self.lbl_mode = ctk.CTkLabel(self.mode_grid, text="Generation Mode:", font=ctk.CTkFont(weight="bold"))
        self.lbl_mode.pack(side="left", padx=(0, 10))
        self.mode_var = ctk.StringVar(value="all")
        self.rb_all = ctk.CTkRadioButton(self.mode_grid, text="All Combinations", variable=self.mode_var, value="all", fg_color="#ef4444", hover_color="#dc2626")
        self.rb_all.pack(side="left", padx=10)
        self.rb_random = ctk.CTkRadioButton(self.mode_grid, text="Random Match", variable=self.mode_var, value="random", fg_color="#ef4444", hover_color="#dc2626")
        self.rb_random.pack(side="left", padx=10)

        # 4. ADJUSTMENTS BLOCK (Post-Processing + Texture Movement)
        self.post_container = ctk.CTkFrame(self.right_frame, fg_color="#18181b", corner_radius=10)
        self.post_container.pack(fill="x", pady=(0, 10))
        self.post_container.grid_columnconfigure(1, weight=1)
        
        self.lbl_bc = ctk.CTkLabel(self.post_container, text="Adjustments", font=ctk.CTkFont(size=18, weight="bold"), text_color="#f4f4f5")
        self.lbl_bc.grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(10, 4))
        
        self.lbl_bright = ctk.CTkLabel(self.post_container, text="Brightness:")
        self.lbl_bright.grid(row=1, column=0, sticky="w", padx=15, pady=2)
        self.bright_var = ctk.DoubleVar(value=1.0)
        self.bright_slider = ctk.CTkSlider(self.post_container, from_=0.2, to=2.0, variable=self.bright_var, button_color="#ef4444", button_hover_color="#dc2626", command=self._on_bright_slider)
        self.bright_slider.grid(row=1, column=1, sticky="ew", padx=15, pady=2)
        self.lbl_b_val = ctk.CTkLabel(self.post_container, text="1.00", width=40)
        self.lbl_b_val.grid(row=1, column=2, padx=15, pady=2)
        
        self.lbl_cont = ctk.CTkLabel(self.post_container, text="Contrast:")
        self.lbl_cont.grid(row=2, column=0, sticky="w", padx=15, pady=2)
        self.cont_var = ctk.DoubleVar(value=1.0)
        self.cont_slider = ctk.CTkSlider(self.post_container, from_=0.2, to=2.0, variable=self.cont_var, button_color="#ef4444", button_hover_color="#dc2626", command=self._on_cont_slider)
        self.cont_slider.grid(row=2, column=1, sticky="ew", padx=15, pady=2)
        self.lbl_c_val = ctk.CTkLabel(self.post_container, text="1.00", width=40)
        self.lbl_c_val.grid(row=2, column=2, padx=15, pady=2)

        self.lbl_tex_off_x = ctk.CTkLabel(self.post_container, text="Texture X:")
        self.lbl_tex_off_x.grid(row=3, column=0, sticky="w", padx=15, pady=2)
        self.tex_off_x_var = ctk.DoubleVar(value=0.0)
        self.tex_off_x_slider = ctk.CTkSlider(self.post_container, from_=-1.0, to=1.0, variable=self.tex_off_x_var, button_color="#ef4444", button_hover_color="#dc2626", command=self._on_tx_slider)
        self.tex_off_x_slider.grid(row=3, column=1, sticky="ew", padx=15, pady=2)
        self.tex_off_x_slider.bind("<ButtonRelease-1>", lambda e: self._on_main_slider_release())
        self.lbl_tx_val = ctk.CTkLabel(self.post_container, text="0.00", width=40)
        self.lbl_tx_val.grid(row=3, column=2, padx=15, pady=2)

        self.lbl_tex_off_y = ctk.CTkLabel(self.post_container, text="Texture Y:")
        self.lbl_tex_off_y.grid(row=4, column=0, sticky="w", padx=15, pady=(2, 8))
        self.tex_off_y_var = ctk.DoubleVar(value=0.0)
        self.tex_off_y_slider = ctk.CTkSlider(self.post_container, from_=-1.0, to=1.0, variable=self.tex_off_y_var, button_color="#ef4444", button_hover_color="#dc2626", command=self._on_ty_slider)
        self.tex_off_y_slider.grid(row=4, column=1, sticky="ew", padx=15, pady=(2, 8))
        self.tex_off_y_slider.bind("<ButtonRelease-1>", lambda e: self._on_main_slider_release())
        self.lbl_ty_val = ctk.CTkLabel(self.post_container, text="0.00", width=40)
        self.lbl_ty_val.grid(row=4, column=2, padx=15, pady=(2, 8))

        # 5. BOTTOM EXECUTION BLOCK (Terminal Log, Progress, Generate)
        self.bottom_container = ctk.CTkFrame(self.right_frame, fg_color="#18181b", corner_radius=10)
        self.bottom_container.pack(fill="x")

        self.log_box = ctk.CTkTextbox(self.bottom_container, height=75, fg_color="#000000", text_color="#10b981", font=ctk.CTkFont(family="Consolas", size=12))
        self.log_box.pack(fill="x", padx=15, pady=(10, 5))
        self.log_box.insert("0.0", "> System Boot Successful [v1.1.0].\n> Headless Blender backend verified.\n> Awaiting directive...\n")
        self.log_box.configure(state="disabled")

        self.progress_bar = ctk.CTkProgressBar(self.bottom_container, progress_color="#ef4444")
        self.progress_bar.pack(fill="x", padx=15, pady=(4, 10))
        self.progress_bar.set(0)

        self.btn_generate = ctk.CTkButton(self.bottom_container, text="Generate", font=ctk.CTkFont(size=20, weight="bold"), height=50, fg_color="#ef4444", hover_color="#dc2626", command=self.start_generation)
        self.btn_generate.pack(fill="x", padx=15, pady=(0, 12))

        self.fmt_var = ctk.StringVar(value="PNG")
        self.light_var = ctk.StringVar(value="Studio Pro")

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
                                  fg_color="#ef4444", hover_color="#dc2626",
                                  command=self._on_item_toggle)
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

    def handle_help_menu(self, choice):
        self.help_var.set("Help")
        if choice == "View Documentation":
            self.show_docs()
        elif choice == "About":
            self.show_about()
        
    def show_docs(self):
        win = ctk.CTkToplevel(self)
        win.title("Documentation - Antigravity CS2 Skin Forge")
        win.geometry("560x360")
        win.attributes('-topmost', True)
        try:
            win.after(200, lambda: win.iconbitmap(icon_path) if os.path.exists(icon_path) else None)
        except Exception:
            pass
        lbl = ctk.CTkLabel(win, text=(
            "Antigravity CS2 Skin Forge (v1.1.0) Quick Guide:\n\n"
            "1. Texture Selection: Place flat pattern textures into Input_Textures/\n"
            "   and select them using the checklist badges (JPG, PNG).\n"
            "2. Weapon Selection: Check which of the 35 CS2 weapon models to forge.\n"
            "3. Live Preview: Click '👁 Live Preview' on top ribbon to inspect in real time.\n"
            "   Drag Texture X & Texture Y to slide texture across geometry.\n"
            "4. Render Configuration: Choose Cycles Raytracing (photorealistic) or\n"
            "   BLENDER_EEVEE_NEXT (fast), background, and quality preset.\n"
            "5. Click 'Generate' to batch render photorealistic production assets."
        ), justify="left", font=ctk.CTkFont(size=13))
        lbl.pack(expand=True, padx=25, pady=20)

    def show_about(self):
        win = ctk.CTkToplevel(self)
        win.title("About")
        win.geometry("440x260")
        win.attributes('-topmost', True)
        try:
            win.after(200, lambda: win.iconbitmap(icon_path) if os.path.exists(icon_path) else None)
        except Exception:
            pass
        lbl = ctk.CTkLabel(win, text=(
            "Antigravity CS2 Skin Forge v1.1.0\n\n"
            "Professional CS2 Weapon Texturing & Rendering Studio\n"
            "Powered by Headless Blender CYCLES & EEVEE\n\n"
            "Created by Smokianlord\n"
            "All 35 CS2 Weapon Models & Valve PBR Maps Included"
        ), font=ctk.CTkFont(size=13, weight="bold"))
        lbl.pack(expand=True)
        
    def show_completion_popup(self):
        win = ctk.CTkToplevel(self)
        win.title("Done!")
        win.geometry("320x160")
        win.attributes('-topmost', True)
        try:
            win.after(200, lambda: win.iconbitmap(icon_path) if os.path.exists(icon_path) else None)
        except Exception:
            pass
        lbl = ctk.CTkLabel(win, text="Rendering is Complete!", font=ctk.CTkFont(size=18, weight="bold"), text_color="#10b981")
        lbl.pack(pady=20)
        btn = ctk.CTkButton(win, text="Open Output Folder", fg_color="#ef4444", hover_color="#dc2626",
                            command=lambda: [os.startfile(self.out_dir) if os.path.exists(self.out_dir) else None, win.destroy()])
        btn.pack(pady=10)

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", "> " + message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        
    def _on_bright_slider(self, v):
        self.lbl_b_val.configure(text=f"{float(v):.2f}")
        if hasattr(self, 'pw_val_b') and self.pw_val_b.winfo_exists():
            self.pw_val_b.configure(text=f"{float(v):.2f}")
        if hasattr(self, 'pw_slider_b') and self.pw_slider_b.winfo_exists():
            self.pw_slider_b.set(float(v))
        self._refresh_preview_postprocess()

    def _on_cont_slider(self, v):
        self.lbl_c_val.configure(text=f"{float(v):.2f}")
        if hasattr(self, 'pw_val_c') and self.pw_val_c.winfo_exists():
            self.pw_val_c.configure(text=f"{float(v):.2f}")
        if hasattr(self, 'pw_slider_c') and self.pw_slider_c.winfo_exists():
            self.pw_slider_c.set(float(v))
        self._refresh_preview_postprocess()

    def _on_tx_slider(self, v):
        self._sync_slider_x(v)

    def _on_ty_slider(self, v):
        self._sync_slider_y(v)

    def _on_bg_change(self, val):
        if hasattr(self, 'pw_opt_bg') and self.pw_opt_bg.winfo_exists():
            self.pw_bg_var.set(val)
        self._refresh_preview_postprocess()

    def _on_trans_toggle(self):
        self._refresh_preview_postprocess()

    def _sync_slider_x(self, v):
        val_f = float(v)
        self.lbl_tx_val.configure(text=f"{val_f:.2f}")
        if hasattr(self, 'pw_val_x') and self.pw_val_x.winfo_exists():
            self.pw_val_x.configure(text=f"{val_f:.2f}")
        if hasattr(self, 'pw_slider_x') and self.pw_slider_x.winfo_exists():
            self.pw_slider_x.set(val_f)

    def _sync_slider_y(self, v):
        val_f = float(v)
        self.lbl_ty_val.configure(text=f"{val_f:.2f}")
        if hasattr(self, 'pw_val_y') and self.pw_val_y.winfo_exists():
            self.pw_val_y.configure(text=f"{val_f:.2f}")
        if hasattr(self, 'pw_slider_y') and self.pw_slider_y.winfo_exists():
            self.pw_slider_y.set(val_f)

    def _on_main_slider_release(self):
        if hasattr(self, 'preview_win') and self.preview_win is not None and self.preview_win.winfo_exists():
            self.trigger_live_preview()

    def _on_preview_close(self):
        if self.preview_win is not None:
            self.preview_win.destroy()
            self.preview_win = None

    def _reset_offsets(self):
        self.tex_off_x_var.set(0.0)
        self.tex_off_y_var.set(0.0)
        self._sync_slider_x(0.0)
        self._sync_slider_y(0.0)
        self.trigger_live_preview()

    def toggle_preview_window(self):
        if hasattr(self, 'preview_win') and self.preview_win is not None and self.preview_win.winfo_exists():
            self.preview_win.deiconify()
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
        
        pw_w, pw_h = 1060, 720
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        cx = max(10, int(sw / 2 - pw_w / 2))
        cy = max(10, int(sh / 2 - pw_h / 2))
        self.preview_win.geometry(f"{pw_w}x{pw_h}+{cx}+{cy}")
        
        try:
            self.preview_win.after(200, lambda: self.preview_win.iconbitmap(icon_path) if os.path.exists(icon_path) else None)
        except Exception:
            pass
            
        self.preview_win.protocol("WM_DELETE_WINDOW", self._on_preview_close)

        # Header bar
        pw_header = ctk.CTkFrame(self.preview_win, fg_color="#18181b", height=44, corner_radius=0)
        pw_header.pack(fill="x", padx=0, pady=(0, 4))
        
        self.pw_title_lbl = ctk.CTkLabel(pw_header, text="Preview: Initializing...", font=ctk.CTkFont(size=13, weight="bold"), text_color="#f4f4f5")
        self.pw_title_lbl.pack(side="left", padx=15, pady=8)
        
        self.pw_status_lbl = ctk.CTkLabel(pw_header, text="● Ready", text_color="#10b981", font=ctk.CTkFont(size=12, weight="bold"))
        self.pw_status_lbl.pack(side="left", padx=10, pady=8)

        self.pw_btn_refresh = ctk.CTkButton(pw_header, text="⟳ Update Preview", width=120, height=28, fg_color="#ef4444", hover_color="#dc2626", font=ctk.CTkFont(size=12, weight="bold"), command=self.trigger_live_preview)
        self.pw_btn_refresh.pack(side="right", padx=15, pady=6)

        # Center Display Area (Large 960x540 16:9 Viewport)
        self.pw_display_frame = ctk.CTkFrame(self.preview_win, fg_color="#09090b", corner_radius=10, width=960, height=540)
        self.pw_display_frame.pack(fill="both", expand=True, padx=15, pady=4)
        
        self.pw_image_lbl = ctk.CTkLabel(self.pw_display_frame, text="⚡ Rendering live preview...", font=ctk.CTkFont(size=16), text_color="#71717a")
        self.pw_image_lbl.pack(expand=True, fill="both", padx=10, pady=10)

        # Bottom Controls
        pw_controls = ctk.CTkFrame(self.preview_win, fg_color="#18181b", corner_radius=10)
        pw_controls.pack(fill="x", padx=15, pady=(4, 12))
        pw_controls.grid_columnconfigure(1, weight=1)
        pw_controls.grid_columnconfigure(4, weight=1)

        # Row 0: Texture X & Y Sliders + Reset button
        lbl_x = ctk.CTkLabel(pw_controls, text="Texture X:", font=ctk.CTkFont(weight="bold"))
        lbl_x.grid(row=0, column=0, padx=(15, 5), pady=5, sticky="w")
        
        self.pw_slider_x = ctk.CTkSlider(pw_controls, from_=-1.0, to=1.0, variable=self.tex_off_x_var,
                                         button_color="#ef4444", button_hover_color="#dc2626",
                                         command=lambda v: self._sync_slider_x(v))
        self.pw_slider_x.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.pw_slider_x.bind("<ButtonRelease-1>", lambda e: self.trigger_live_preview())
        
        self.pw_val_x = ctk.CTkLabel(pw_controls, text=f"{self.tex_off_x_var.get():.2f}", width=40)
        self.pw_val_x.grid(row=0, column=2, padx=(5, 15), pady=5)

        lbl_y = ctk.CTkLabel(pw_controls, text="Texture Y:", font=ctk.CTkFont(weight="bold"))
        lbl_y.grid(row=0, column=3, padx=(15, 5), pady=5, sticky="w")
        
        self.pw_slider_y = ctk.CTkSlider(pw_controls, from_=-1.0, to=1.0, variable=self.tex_off_y_var,
                                         button_color="#ef4444", button_hover_color="#dc2626",
                                         command=lambda v: self._sync_slider_y(v))
        self.pw_slider_y.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        self.pw_slider_y.bind("<ButtonRelease-1>", lambda e: self.trigger_live_preview())
        
        self.pw_val_y = ctk.CTkLabel(pw_controls, text=f"{self.tex_off_y_var.get():.2f}", width=40)
        self.pw_val_y.grid(row=0, column=5, padx=(5, 10), pady=5)

        btn_reset = ctk.CTkButton(pw_controls, text="Reset (0, 0)", width=95, height=26, fg_color="#3f3f46", hover_color="#52525b", command=self._reset_offsets)
        btn_reset.grid(row=0, column=6, padx=(5, 15), pady=5)

        # Row 1: Real-time Post-Processing controls (Brightness, Contrast, Studio Background)
        lbl_b = ctk.CTkLabel(pw_controls, text="Brightness:", font=ctk.CTkFont(weight="bold"))
        lbl_b.grid(row=1, column=0, padx=(15, 5), pady=5, sticky="w")
        self.pw_slider_b = ctk.CTkSlider(pw_controls, from_=0.2, to=2.0, variable=self.bright_var,
                                         button_color="#ef4444", button_hover_color="#dc2626",
                                         command=lambda v: self._on_bright_slider(v))
        self.pw_slider_b.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.pw_val_b = ctk.CTkLabel(pw_controls, text=f"{self.bright_var.get():.2f}", width=40)
        self.pw_val_b.grid(row=1, column=2, padx=(5, 15), pady=5)

        lbl_c = ctk.CTkLabel(pw_controls, text="Contrast:", font=ctk.CTkFont(weight="bold"))
        lbl_c.grid(row=1, column=3, padx=(15, 5), pady=5, sticky="w")
        self.pw_slider_c = ctk.CTkSlider(pw_controls, from_=0.2, to=2.0, variable=self.cont_var,
                                         button_color="#ef4444", button_hover_color="#dc2626",
                                         command=lambda v: self._on_cont_slider(v))
        self.pw_slider_c.grid(row=1, column=4, padx=5, pady=5, sticky="ew")
        self.pw_val_c = ctk.CTkLabel(pw_controls, text=f"{self.cont_var.get():.2f}", width=40)
        self.pw_val_c.grid(row=1, column=5, padx=(5, 10), pady=5)

        self.pw_bg_var = self.bg_var
        self.pw_opt_bg = ctk.CTkOptionMenu(pw_controls, variable=self.pw_bg_var,
                                          values=["Dark Grey (Default)", "Deep Blue", "Pure Black", "Pure White", "Green Screen"],
                                          fg_color="#27272a", button_color="#3f3f46", width=140, dynamic_resizing=False,
                                          command=self._on_bg_change)
        self.pw_opt_bg.grid(row=1, column=6, padx=(5, 15), pady=5)

        # Row 2: Helpful Tip
        tip_lbl = ctk.CTkLabel(pw_controls, text="💡 Tip: Drag sliders to reposition texture. Release slider to re-render (~1.8s). Brightness, contrast & background update instantly (10ms).", text_color="#71717a", font=ctk.CTkFont(size=11, slant="italic"))
        tip_lbl.grid(row=2, column=0, columnspan=7, padx=15, pady=(2, 6), sticky="w")

        # Automatically start initial preview render
        self.trigger_live_preview()

    def trigger_live_preview(self):
        if self.is_preview_running:
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
        if hasattr(self, 'pw_title_lbl') and self.pw_title_lbl.winfo_exists():
            self.pw_title_lbl.configure(text=f"Active Weapon: {w['name']}  |  Texture: {tex_name}")

        if hasattr(self, 'pw_status_lbl') and self.pw_status_lbl.winfo_exists():
            self.pw_status_lbl.configure(text="⚡ Rendering preview...", text_color="#ef4444")

        engine = self.engine_var.get()
        light = self.light_var.get()
        compute = self.compute_var.get()
        off_x = str(self.tex_off_x_var.get())
        off_y = str(self.tex_off_y_var.get())

        self.is_preview_running = True
        threading.Thread(target=self._run_preview_render, args=(w, tex_path, engine, light, compute, off_x, off_y), daemon=True).start()

    def _run_preview_render(self, w, tex_path, engine, light, compute, off_x, off_y):
        preview_out = os.path.join(pipeline_folder, "_preview_temp.png")
        cmd = [
            self.blender_exe, "-b", "--python-exit-code", "1", "-P", blender_script, "--",
            os.path.abspath(w["obj"]), w["normal"], w["rough"], os.path.abspath(tex_path),
            os.path.abspath(preview_out), "SKIP",
            "Preview (540p | 8 Samples)", "True", engine, light, "PNG", compute,
            off_x, off_y
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

    def _render_preview_error(self, err):
        self.is_preview_running = False
        if hasattr(self, 'pw_status_lbl') and self.pw_status_lbl.winfo_exists():
            self.pw_status_lbl.configure(text="Error rendering preview", text_color="#ef4444")

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

        disp_w, disp_h = 960, 540
        render_disp = render.copy()
        if render_disp.size != (disp_w, disp_h):
            render_disp = render_disp.resize((disp_w, disp_h), Image.Resampling.LANCZOS)
        ctk_img = ctk.CTkImage(light_image=render_disp, dark_image=render_disp, size=(disp_w, disp_h))
        
        self.pw_image_lbl.configure(image=ctk_img, text="")
        self.pw_image_lbl.image = ctk_img

    def start_generation(self):
        self.btn_generate.configure(state="disabled")
        self.progress_bar.set(0)
        self.log_box.configure(state="normal")
        self.log_box.delete("0.0", "end")
        self.log_box.configure(state="disabled")
        threading.Thread(target=self.run_pipeline, daemon=True).start()

    def run_pipeline(self):
        selected_tex_paths = [os.path.join(self.in_dir, tex) for tex, var in self.texture_vars.items() if var.get()]
        if not selected_tex_paths:
            self.log("ERROR: Please select at least one Texture from the checklist!")
            self.btn_generate.configure(state="normal")
            return
            
        selected_weapons = [w for w in all_weapons if self.weapon_vars[w["id"]].get()]
        if not selected_weapons:
            self.log("ERROR: Please select at least one weapon model!")
            self.btn_generate.configure(state="normal")
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
        self.log(f"Warming up headless Blender engine... [{q_preset}]")
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
            self.log(f"[{i+1}/{total_jobs}] Rendering {w['name']} with {tex_name}...")
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
                str(self.tex_off_x_var.get()), str(self.tex_off_y_var.get())
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
        self.btn_generate.configure(state="normal")
        self.after(0, self.show_completion_popup)

if __name__ == "__main__":
    app = CS2SkinGeneratorApp()
    app.mainloop()
