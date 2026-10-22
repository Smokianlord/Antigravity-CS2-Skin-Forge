"""Toolkit-independent core for Antigravity CS2 Skin Forge: assets, Blender discovery, render commands."""
import hashlib
import os
import shutil
import subprocess
import sys

from PIL import Image

APP_VERSION = "1.3.0"
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tga")
PREVIEW_MAX_TEXTURE = 1024

if getattr(sys, "frozen", False):
    pipeline_folder = os.path.dirname(sys.executable)
    resource_folder = getattr(sys, "_MEIPASS", pipeline_folder)
else:
    pipeline_folder = os.path.dirname(os.path.abspath(__file__))
    resource_folder = pipeline_folder

icon_path = os.path.join(resource_folder, "icon.ico")
blender_script = os.path.join(pipeline_folder, "blender_headless_render.py")
default_input_folder = os.path.join(pipeline_folder, "Input_Textures")
default_out_folder = os.path.join(pipeline_folder, "Output_Renders")
default_blend_folder = os.path.join(pipeline_folder, "Output_Project_Files")
preview_cache_dir = os.path.join(pipeline_folder, "_preview_cache")

QUALITY_PRESETS = [
    "Fast Draft (720p | 16 Samples)",
    "Standard (1080p | 32 Samples)",
    "High Quality (1440p | 48 Samples)",
    "Ultra (4K | 64 Samples)",
    "Masterpiece (8K | 96 Samples)",
]
ENGINES = ["Cycles Raytracing", "BLENDER_EEVEE"]
COMPUTE_MODES = ["GPU + CPU (Hybrid)", "GPU Only", "CPU Only"]
LIGHTING_RIGS = ["Studio Pro", "Soft Workbench", "Bright Flat", "Dark Cinematic"]
BACKGROUNDS = {
    "Dark Grey": (20, 20, 24, 255),
    "Deep Blue": (15, 20, 35, 255),
    "Pure Black": (0, 0, 0, 255),
    "Pure White": (255, 255, 255, 255),
    "Green Screen": (0, 255, 0, 255),
}

CS2_NAMES = {
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
    "weapon_snip_scar20": "SCAR-20", "weapon_snip_ssg08": "SSG 08",
}
_TEXTURE_ALIASES = {"glock18": "glock", "m4a1_silencer": "m4a1", "usp_silencer": "usp", "elite": "beretta", "hkp2000": "p2000"}
CATEGORY_LABELS = {"rif": "Rifles", "snip": "Snipers", "pist": "Pistols", "smg": "SMGs", "shot": "Shotguns", "mach": "Machine guns"}


def find_blender():
    env = os.environ.get("BLENDER_PATH")
    if env and os.path.exists(env):
        return env
    found = shutil.which("blender") or shutil.which("blender.exe")
    if found and os.path.exists(found):
        return found
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
    if os.path.isdir(bf_dir):
        for s in sorted(os.listdir(bf_dir), reverse=True):
            cand = os.path.join(bf_dir, s, "blender.exe")
            if os.path.exists(cand):
                return cand
    return candidates[0]


def resolve_asset_dir(primary, fallbacks=()):
    candidates = [primary, *fallbacks]
    roots = [getattr(sys, "_MEIPASS", None), pipeline_folder, os.path.dirname(pipeline_folder)]
    for root in roots:
        if not root:
            continue
        for sub in candidates:
            p = os.path.join(root, sub)
            if os.path.exists(p):
                return p
    return os.path.join(pipeline_folder, primary)


def scan_weapons():
    """Return weapon dicts (id, name, category, obj, normal, rough) using a single walk of the texture folder."""
    models_dir = resolve_asset_dir(r"Assets\Models", [r"Assets\Official Resources\CS2 Models", r"Assets\CS2 Models"])
    tex_dir = resolve_asset_dir(r"Assets\Textures", [r"Assets\CS2_Weapon\CS2_Weapon", r"Assets\CS2_Weapon"])
    if not os.path.isdir(models_dir):
        return []
    pngs = []
    for root, _dirs, files in os.walk(tex_dir):
        for f in files:
            if f.lower().endswith(".png"):
                pngs.append((f.lower(), os.path.join(root, f)))

    def find(token, kind):
        for low, full in pngs:
            if token in low and kind in low:
                return full
        return "NONE"

    weapons = []
    for obj_file in sorted(os.listdir(models_dir)):
        if not obj_file.endswith(".obj"):
            continue
        base = obj_file[:-4]
        parts = base.split("_", 2)
        category = parts[1] if len(parts) > 2 else "other"
        short = parts[2] if len(parts) > 2 else base
        token = _TEXTURE_ALIASES.get(short, short)
        weapons.append({
            "id": base,
            "name": CS2_NAMES.get(base, base.replace("weapon_", "").title()),
            "category": CATEGORY_LABELS.get(category, "Other"),
            "obj": os.path.join(models_dir, obj_file),
            "normal": find(token, "normal"),
            "rough": find(token, "rough"),
        })
    return weapons


def list_textures(folder):
    if not os.path.isdir(folder):
        return []
    return sorted(f for f in os.listdir(folder) if f.lower().endswith(IMAGE_EXTS))


def preview_proxy(path):
    """Cached <=PREVIEW_MAX_TEXTURE copy of a texture so preview renders skip decoding 4K images."""
    if not path or path == "NONE" or not os.path.exists(path):
        return path
    try:
        st = os.stat(path)
        key = hashlib.md5(f"{os.path.abspath(path)}|{st.st_mtime_ns}|{st.st_size}|{PREVIEW_MAX_TEXTURE}".encode()).hexdigest()[:16]
        os.makedirs(preview_cache_dir, exist_ok=True)
        proxy = os.path.join(preview_cache_dir, f"{key}.png")
        if os.path.exists(proxy):
            return proxy
        Image.MAX_IMAGE_PIXELS = None
        with Image.open(path) as im:
            if max(im.size) <= PREVIEW_MAX_TEXTURE:
                return path
            im.draft("RGB", (PREVIEW_MAX_TEXTURE, PREVIEW_MAX_TEXTURE))
            im = im.copy()
        im.thumbnail((PREVIEW_MAX_TEXTURE, PREVIEW_MAX_TEXTURE), Image.Resampling.BILINEAR)
        tmp = proxy + ".tmp"
        im.save(tmp, format="PNG", compress_level=1)
        os.replace(tmp, proxy)
        return proxy
    except Exception:
        return path


def apply_color(img, brightness=1.0, contrast=1.0, saturation=1.0):
    """Brightness/contrast/saturation on RGB only; alpha is preserved (PIL's RGBA enhance would scale alpha)."""
    from PIL import ImageEnhance
    if abs(brightness - 1.0) < 0.001 and abs(contrast - 1.0) < 0.001 and abs(saturation - 1.0) < 0.001:
        return img
    img = img.convert("RGBA")
    alpha = img.getchannel("A")
    rgb = img.convert("RGB")
    if abs(brightness - 1.0) > 0.001:
        rgb = ImageEnhance.Brightness(rgb).enhance(brightness)
    if abs(contrast - 1.0) > 0.001:
        rgb = ImageEnhance.Contrast(rgb).enhance(contrast)
    if abs(saturation - 1.0) > 0.001:
        rgb = ImageEnhance.Color(rgb).enhance(saturation)
    rgb.putalpha(alpha)
    return rgb


def composite_on(img, color):
    bg = Image.new("RGBA", img.size, color)
    bg.alpha_composite(img.convert("RGBA"))
    return bg


class RenderSettings:
    """Plain container for everything the Blender script needs besides weapon/texture."""

    def __init__(self):
        self.engine = ENGINES[0]
        self.compute = COMPUTE_MODES[0]
        self.quality = QUALITY_PRESETS[1]
        self.lighting = LIGHTING_RIGS[0]
        self.fmt = "PNG"
        self.transparent = False
        self.save_blend = True
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.scale = 1.0
        self.flip_x = False
        self.flip_y = False


def build_command(blender_exe, weapon, tex_path, out_path, blend_path, quality, s, *, transparent, proxy=False):
    normal, rough, tex = weapon["normal"], weapon["rough"], tex_path
    if proxy:
        normal, rough, tex = preview_proxy(normal), preview_proxy(rough), preview_proxy(tex_path)
    return [
        blender_exe, "-b", "--python-exit-code", "1", "-P", blender_script, "--",
        os.path.abspath(weapon["obj"]), normal, rough, os.path.abspath(tex),
        os.path.abspath(out_path), os.path.abspath(blend_path) if blend_path != "SKIP" else "SKIP",
        quality, str(transparent), s.engine, s.lighting, s.fmt, s.compute,
        str(s.offset_x), str(s.offset_y), str(s.scale), str(s.flip_x), str(s.flip_y),
    ]


def run_blender(cmd):
    flags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
    proc = subprocess.run(cmd, capture_output=True, text=True, creationflags=flags)
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-3:]
        raise RuntimeError("Blender exited with code %d: %s" % (proc.returncode, " | ".join(tail)))
