import bpy
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
# Neutral highlight roll-off preserves paint colors better than a filmic look.
# Blender 4.0/4.1 do not have PBR Neutral; the calibrated rig also works in Standard.
view = bpy.context.scene.view_settings
try:
    view.view_transform = 'Khronos PBR Neutral'
except TypeError:
    view.view_transform = 'Standard'
view.look = 'None'
view.exposure = 0.0
view.gamma = 1.0
bpy.context.scene.display_settings.display_device = 'sRGB'

is_preview = "Preview" in quality
if is_preview:
    res_x, res_y, samples = 960, 540, 8
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
tex_node.image.colorspace_settings.name = "sRGB"
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
    # These weapon roughness images can be packed RGB data, not greyscale.
    # Read R explicitly; converting the entire color to a value mixes in G/B.
    rough_channels = nodes.new("ShaderNodeSeparateColor")
    rough_channels.mode = 'RGB'
    links.new(rough_tex.outputs["Color"], rough_channels.inputs["Color"])
    links.new(rough_channels.outputs["Red"], bsdf.inputs["Roughness"])
else:
    bsdf.inputs['Roughness'].default_value = 0.4
bsdf.inputs['Metallic'].default_value = 0.02
if 'Specular IOR Level' in bsdf.inputs:
    bsdf.inputs['Specular IOR Level'].default_value = 0.5
elif 'Specular' in bsdf.inputs:
    bsdf.inputs['Specular'].default_value = 0.5

# A thin paint topcoat adds restrained edge reflections, not a chrome finish.
# Keep the original normal map in both layers so rivets and recesses stay visible.
if 'Coat Weight' in bsdf.inputs:
    bsdf.inputs['Coat Weight'].default_value = 0.12
    bsdf.inputs['Coat Roughness'].default_value = 0.22
    if normal_path != "NONE" and os.path.exists(normal_path):
        links.new(norm_map.outputs['Normal'], bsdf.inputs['Coat Normal'])

for m in meshes:
    m.data.materials.clear()
    m.data.materials.append(mat)

# Place lights relative to the camera, so weapons along either model axis
# receive the same illumination. Powers and emitter sizes scale with the model.
light_basis = cam_obj.rotation_euler.to_quaternion()

def add_light(name, power, right, up, front, radius, height=None):
    data = bpy.data.lights.new(name=name, type="AREA")
    data.energy = power * max_dim ** 2
    data.color = (1.0, 1.0, 1.0)
    data.shape = "DISK" if height is None else "RECTANGLE"
    data.size = max_dim * radius
    if height is not None:
        data.size_y = max_dim * height
    obj = bpy.data.objects.new(name=name, object_data=data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = global_bbox_center + light_basis @ (
        mathutils.Vector((right, up, front)) * max_dim
    )
    local_direction = mathutils.Vector((-right, -up, -front))
    obj.rotation_euler = (
        light_basis @ local_direction.to_track_quat('-Z', 'Y')
    ).to_euler()

# Broad white softboxes provide fill in both Cycles and Eevee, without relying
# on world illumination (which needs baked probes for diffuse light in Eevee).
# No emission or texture brightening: normal and roughness still shape the paint.
light_style = lighting.lower()
if "workbench" in light_style or "soft" in light_style:
    add_light("Front", 12.0, 0.0, 0.0, 1.1, 2.0)
    add_light("Top", 4.0, -0.3, 0.8, 0.8, 1.8)
    add_light("Fill", 3.0, 0.5, -0.5, 0.8, 1.8)
    add_light("Back", 2.0, 0.0, 0.5, -1.0, 1.2)
elif "bright" in light_style or "flat" in light_style:
    add_light("Front", 14.0, 0.0, 0.0, 1.1, 2.0)
    add_light("Fill", 5.0, 0.5, -0.4, 0.9, 1.8)
    add_light("Top", 3.0, -0.4, 0.7, 0.8, 1.6)
    add_light("Back", 2.0, 0.0, 0.5, -1.0, 1.2)
elif "dark" in light_style or "cinematic" in light_style:
    add_light("Key", 5.0, -0.6, 0.7, 1.0, 1.0)
    add_light("Fill", 3.0, 0.4, -0.2, 1.1, 1.8)
    add_light("Rim", 4.0, 0.2, 0.7, -0.8, 0.8)
else:  # Studio Pro: directional reflections with bright, readable paint.
    # The overhead strip creates shape-dependent highlights and real shadows.
    # Side/front fill keeps the paint visible without a uniform frontal light wash.
    add_light("Key", 24.0, -0.15, 0.9, 0.45, 1.3, height=0.16)
    add_light("FrontSoftbox", 7.0, -0.6, 0.15, 0.9, 1.2, height=1.2)
    add_light("Fill", 3.0, 0.6, -0.5, 0.9, 1.6, height=1.6)
    add_light("Rim", 2.0, 0.2, 0.7, -0.8, 1.2, height=0.12)

# Save the same output settings that are used for the exported render.
bpy.context.scene.render.image_settings.file_format = fmt
bpy.context.scene.render.filepath = out_path

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

bpy.ops.render.render(write_still=True)
