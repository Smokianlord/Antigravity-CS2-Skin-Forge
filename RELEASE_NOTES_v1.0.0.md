# Antigravity CS2 Skin Forge v1.0.0

First public release of Antigravity CS2 Skin Forge.

## Highlights

- Batch-preview 2D skin concepts on multiple CS2 weapon models.
- Render through Blender Cycles or EEVEE without manually opening Blender for each job.
- Automatic camera framing, material setup, lighting, and export.
- 1080p through 8K presets, PNG/JPEG output, transparency, and optional `.blend` project saves.
- Windows GUI with progress logging and live preview thumbnails.

## Before you run it

This release does **not** include Counter-Strike/Valve weapon models or texture assets. Add only resources you are legally permitted to use under the top-level `Assets` folder.

The included v1.0.0 Windows executable expects Blender here:

```text
C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe
```

If Blender is installed somewhere else, run from source after changing `blender_exe` in `app/gui_app.py`, or rebuild the executable.

## Windows package layout

Keep the extracted package structure intact:

```text
Antigravity-CS2-Skin-Forge-v1.0.0/
├─ Assets/
└─ App/
   ├─ Antigravity CS2 Skin Forge.exe
   ├─ Input_Textures/
   ├─ Output_Renders/
   └─ Output_Project_Files/
```

## Known limitations

- Windows-focused release.
- Blender path is fixed in v1.0.0.
- External weapon/PBR resources are required before weapon entries can populate.
- GPU rendering support depends on Blender and the local graphics driver/configuration.

## Integrity

A SHA-256 checksum file is published alongside the downloadable release package.
