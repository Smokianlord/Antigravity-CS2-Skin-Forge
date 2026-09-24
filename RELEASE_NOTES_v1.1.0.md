# Antigravity CS2 Skin Forge v1.1.0

[![Release](https://img.shields.io/badge/Release-v1.1.0-red.svg)](https://github.com/Smokianlord/Antigravity-CS2-Skin-Forge/releases/tag/v1.1.0)
[![Blender](https://img.shields.io/badge/Blender-4.0%2B%20%7C%205.x-orange.svg)](https://www.blender.org/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20x64-0078d7.svg)](https://microsoft.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Antigravity CS2 Skin Forge (v1.1.0)** is a standalone desktop application for Counter-Strike 2 skin creators, workshop artists, and 3D weapon designers. Created by **Smokianlord**, it automates mapping 2D pattern textures onto 3D CS2 weapon models, framing them using mathematical bounding-box orthographic cameras, rendering them through headless Blender (Cycles / Eevee) with studio PBR materials, post-processing them in real time, and batch exporting production-ready showcases and `.blend` project files.

---

## 🚀 What's New in v1.1.0

### 👁️ Dedicated Large Live Preview Window (1060×720)
- **Large 16:9 Viewport (960×540)**: Dedicated high-resolution interactive viewport launched via the top ribbon bar (`👁 Live Preview`).
- **Interactive Texture Movement**: Real-time **Texture X** and **Texture Y** sliders allow you to slide patterns seamlessly across weapon geometry.
- **Natural Coordinate Mapping**: Inverted mapping offsets ensure positive slider values slide textures right and up naturally.
- **Auto-Render on Slider Release**: Letting go of the mouse button while dragging texture sliders automatically triggers a fresh preview render in **~1.3–1.8 seconds**.
- **Instant PIL Compositing (<10ms)**: Adjusting `Brightness`, `Contrast`, `Studio Background`, or `Transparent Background` updates the preview canvas instantly without re-rendering in Blender.
- **Active Weapon & Texture Switchers**: Switch weapons or texture maps directly inside the preview header.
- **Reset (0, 0)**: One-click reset to snap texture coordinates back to default alignment.

### 📦 All 35 Official CS2 Weapon Models Bundled
- **Completely Self-Contained**: All 35 official CS2 `.obj` weapon models (~131 MB) are bundled directly inside the standalone Windows executable (`Antigravity CS2 Skin Forge.exe`).
- **Multi-Tiered Asset Resolution (`resolve_asset_dir`)**: Automatically resolves assets from PyInstaller extraction (`sys._MEIPASS`), local workspace directory, or parent directory structures.
- **Valve PBR Textures Pre-Mapped**: Automatic matching and injection of official normal maps and roughness maps for all 35 weapons.

### 🎨 Refined 1450×750 UI / UX & Dark Theme
- **Dynamic Startup Centering**: Automatically calculates primary monitor resolution and centers the window on launch.
- **Sleek Top Ribbon Bar (`#1f1f23`)**:
  - `File`: Open Input, Output, and Project folders; Exit.
  - `Edit`: Select All, Deselect All, Random Pick (3).
  - `Configure`: Set custom folders for Input Textures, Output Renders, Output Projects, and custom Blender path.
  - `Help`: Built-in documentation modal and official About dialog.
- **Checklist with Badges**: Vertical scrollable texture checklist featuring color-coded pill badges (`JPG`, `PNG`) and live folder refresh (`⟳ Refresh`).
- **5-Column Weapon Grid**: Organized layout for all 35 CS2 weapons, unselected by default.
- **Engine Selection**: Toggle between `Cycles Raytracing` (photorealistic raytracing with OptiX/CUDA/CPU) and `BLENDER_EEVEE_NEXT` (high-speed rasterization) with backward/forward compatibility across Blender 4.0 through 5.x.
- **Collapsible Slide-Up Drawer**: Bottom footer drawer displaying copyable absolute folder paths.

---

## 📦 Release Assets & Checksums

| File | Size | Format | Description |
| :--- | :--- | :--- | :--- |
| **`Antigravity CS2 Skin Forge.exe`** | `~58.2 MB` | Windows Executable | Standalone portable executable (v1.1.0.0, 64-bit). No Python installation required. |
| **`Antigravity-CS2-Skin-Forge-v1.1.0-SHA256SUMS.txt`** | `97 B` | Plain Text | SHA-256 integrity checksum file. |
| **Source code (zip)** | - | ZIP Archive | Source files, scripts, models, and assets. |
| **Source code (tar.gz)** | - | TAR.GZ Archive | Source files, scripts, models, and assets. |

### 🔒 SHA-256 Checksums
```text
b645913e9bb1aa4cd9e7b2e1ed2931cda6f37e7cacb7621eef711be4abccd29b *Antigravity CS2 Skin Forge.exe
```

---

## 🛠️ System Requirements

- **Operating System**: Windows 10 or Windows 11 (64-bit).
- **Blender**: Blender 4.0+ / 4.1 / 4.2 / 5.x (Installed via Steam or standard Blender Foundation installer).
- **GPU (Optional but recommended)**: NVIDIA GPU with CUDA/OptiX for accelerated Cycles raytracing. CPU rendering fully supported.

---

## 🚀 Quick Start Guide

### Option A: Portable Standalone Executable (Recommended)
1. Download **`Antigravity CS2 Skin Forge.exe`** from this release.
2. Ensure Blender 4.0+ is installed on your computer.
3. Drop your flat texture files (`.png`, `.jpg`, `.jpeg`) into the `Input_Textures` directory.
4. Launch `Antigravity CS2 Skin Forge.exe`.
5. Select your textures and weapon models, click **`👁 Live Preview`** to adjust **Texture X & Y**, and hit **Generate**!

### Option B: Running from Python Source
```bash
# 1. Clone the repository
git clone https://github.com/Smokianlord/Antigravity-CS2-Skin-Forge.git
cd Antigravity-CS2-Skin-Forge

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch application
python gui_app.py
```

---

## 👨‍💻 Credits & Author
- **Author**: Smokianlord
- **License**: MIT License
- **Framework**: CustomTkinter, Python 3.12, Blender 3D Engine, Pillow (PIL)
