<div align="center">

# Antigravity CS2 Skin Forge

**A Windows desktop pipeline for batch-generating Counter-Strike 2 weapon-skin showcase renders through Blender.**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6)
![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)
![Blender](https://img.shields.io/badge/Blender-4.x-F5792A)
![License](https://img.shields.io/badge/license-MIT-yellow)

</div>

## Overview

Antigravity CS2 Skin Forge is a CustomTkinter front end for a headless Blender rendering pipeline. It is designed for skin artists who want to preview flat texture concepts across multiple CS2 weapon models without manually setting up each render.

The application can queue weapon/texture combinations, launch Blender in the background, build materials, apply available normal and roughness maps, frame the weapon automatically, render with Cycles or EEVEE, and save final images and optional `.blend` project files.

## Features

- Batch rendering of selected textures across selected weapon models.
- "All combinations" and random-match workflows.
- Blender Cycles and EEVEE rendering modes.
- Automatic orthographic camera framing based on weapon bounds.
- Optional normal and roughness map hookup when matching assets are available.
- Studio Pro, Bright Flat, and Dark Cinematic lighting presets.
- 1080p, 1440p, 4K, and 8K quality presets.
- PNG/JPEG output, transparent backgrounds, brightness/contrast adjustment.
- Optional `.blend` project export for manual refinement.
- Live progress log and render thumbnail preview.

## Requirements

### Windows release

- Windows 10 or Windows 11.
- Blender installed at the current default path used by v1.0.0:

```text
C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe
```

The v1.0.0 binary uses that Blender path directly. If your Blender installation is elsewhere, run from source after changing `blender_exe` in `app/gui_app.py`, or rebuild the executable after making that change.

### Running from source

- Python 3.10+
- Blender 4.x
- Packages listed in `app/requirements.txt`

## Asset layout

Valve/Counter-Strike assets are **not included** in this repository or release. Provide only assets you are legally permitted to use.

The app expects this layout:

```text
Antigravity-CS2-Skin-Forge/
├─ Assets/
│  ├─ Official Resources/
│  │  └─ CS2 Models/
│  │     ├─ weapon_rif_ak47.obj
│  │     └─ ...
│  └─ CS2_Weapon/
│     └─ CS2_Weapon/
│        └─ ... normal/roughness texture files ...
└─ app/
   ├─ gui_app.py
   ├─ Input_Textures/
   ├─ Output_Renders/
   └─ Output_Project_Files/
```

Weapon `.obj` filenames should use the internal CS2-style names recognized by the application, such as `weapon_rif_ak47.obj`, `weapon_snip_awp.obj`, and `weapon_pist_glock18.obj`.

## Quick start: Windows release

1. Download and extract the Windows release ZIP.
2. Add your legally obtained weapon model and PBR resources under the top-level `Assets` folder using the layout above.
3. Put your `.png`, `.jpg`, or `.jpeg` concept textures in `App/Input_Textures`.
4. Run `App/Antigravity CS2 Skin Forge.exe`.
5. Select textures and weapon models, choose render settings, then click **Generate**.
6. Find finished images in `App/Output_Renders` and optional Blender projects in `App/Output_Project_Files`.

## Run from source

From the repository root:

```powershell
cd app
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python gui_app.py
```

## Build the Windows executable

Install the development dependency and run the provided build script:

```powershell
.\build_windows.bat
```

The PyInstaller output will be placed under `app/dist/`.

## Repository structure

```text
.
├─ .github/                 # Issue templates and Windows build/release workflow
├─ Assets/                  # User-supplied external assets; content is gitignored
├─ app/
│  ├─ gui_app.py            # Main application
│  ├─ Antigravity_Skin_Forge.spec
│  ├─ version.txt
│  ├─ icon.ico
│  ├─ requirements.txt
│  ├─ requirements-dev.txt
│  ├─ Input_Textures/
│  ├─ Output_Renders/
│  └─ Output_Project_Files/
├─ CHANGELOG.md
├─ CONTRIBUTING.md
├─ LICENSE
└─ RELEASE_NOTES_v1.0.0.md
```

## Known limitations in v1.0.0

- Blender's executable path is hard-coded to the Steam installation path shown above.
- The release does not include Valve models, textures, or other game assets.
- GPU rendering availability depends on Blender, the installed GPU driver, and the selected compute device.
- The GUI is currently Windows-oriented (`os.startfile` and Windows subprocess flags are used).

## Contributing

Bug reports and pull requests are welcome. Please see `CONTRIBUTING.md` before submitting changes.

## License

The application source code is licensed under the MIT License. See `LICENSE`.

This license applies to this project's code only. It does not grant rights to Counter-Strike, Valve assets, third-party textures, user artwork, or other external content.

## Disclaimer

Antigravity CS2 Skin Forge is an independent community tool and is not affiliated with, endorsed by, or sponsored by Valve Corporation. Counter-Strike, Counter-Strike 2, CS2, and related game assets and trademarks belong to their respective owners.
