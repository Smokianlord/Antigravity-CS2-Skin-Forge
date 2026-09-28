<div align="center">
  
# Antigravity CS2 Skin Forge 🔫🎨

**An automated, headless Python pipeline for generating photorealistic Counter-Strike 2 weapon skins using Blender's CYCLES & EEVEE engines.**

[![Release](https://img.shields.io/badge/Release-v1.2.5-red.svg)](https://github.com/Smokianlord/Antigravity-CS2-Skin-Forge/releases/tag/v1.2.5)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Blender 4.0+](https://img.shields.io/badge/blender-4.0+-orange.svg)](https://www.blender.org/)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blueviolet)](https://github.com/TomSchimansky/CustomTkinter)

<br>

<p align="center">
  <img src="docs/images/app_interface.png" alt="Antigravity CS2 Skin Forge v1.2.5 Main Interface" width="950">
</p>

</div>

## 📖 Description

**Antigravity CS2 Skin Forge** (version **v1.2.5**), created by **Smokianlord**, is a professional-grade UI and rendering pipeline built specifically for Counter-Strike 2 skin creators, workshop designers, and 3D artists. It completely automates the process of mapping 2D pattern textures onto 3D CS2 weapon models, framing them using mathematical bounding-box orthographic cameras, rendering them through headless Blender (Cycles / Eevee) with studio PBR materials, post-processing them in real time, and exporting production-ready showcases and `.blend` project files in batch.

---

## 👁️ Dedicated Large Live Preview Window (Adaptive 16:9 Viewport)

Clicking **`Live Preview`** on the top ribbon bar launches a dedicated high-resolution studio with a large 16:9 responsive viewport that stays permanently pinned on top of the application.

<p align="center">
  <img src="docs/images/live_preview_window.png" alt="Live Skin Preview Studio" width="950">
</p>

- **🔄 Texture Mirroring & Reflection (Flip X & Flip Y)**: Instant horizontal (`⇄ Flip X`) and vertical (`⇅ Flip Y`) texture reflection with center-anchored UV transformation math. Mirrors patterns across weapon axes without drifting out of position.
- **⚡ 2x Faster Debounced Preview (~160ms)**: Instant feedback during slider interaction, powered by an optimized 160ms debounce timer and real-time bilinear viewport scaling.
- **🎯 Permanently Visible Hero Generate Button**: Pinned unconditionally to the bottom edge of the window (`side="bottom"` priority), guaranteeing immediate access on any display size.
- **Calibrated True-Color Fidelity**: Uses `Standard` tone curve colorimetry and physically calibrated lighting multipliers, completely eliminating washed-out or bleached chalk highlights on weapon artwork.
- **Precision Stepper Arrow Buttons (`[ ◀ ]` & `[ ▶ ]`)**: Fine-grained ±0.01 (offsets / brightness / contrast / saturation) and ±0.05 (scale) micro-adjustments with instant click precision.
- **Keyboard Arrow Key Nudge**: Press `Left`/`Right`/`Up`/`Down` to nudge sliders directly from your keyboard. Hold `Shift` for 5x larger increments.
- **Visual Selection Highlight (`►`)**: The currently active slider illuminates in crimson red (`#ef4444`) with an active indicator pointer `►`, glowing stepper button borders, and bold accent badges.
- **Rapid Navigation (`Tab` & `1`–`6`)**: Cycle all 6 sliders sequentially using `Tab` / `Shift+Tab` or immediately jump to any slider with keys `1` through `6` (`tx`, `ty`, `scale`, `bright`, `cont`, `sat`).
- **Dynamic Lighting Rig Selector**: Switch directly between Studio Pro, Soft Workbench, Bright Flat, and Dark Cinematic presets from inside the preview window with instant debounced rendering.
- **Permanent Topmost Pinning**: Native Z-order transient locking ensures the preview window stays permanently on top without cluttering the interface with redundant toggle checkboxes.
- **Real-Time Saturation & Color Vibrance (<1ms)**: Fine-tune texture saturation from monochrome (`0.00`) to vibrant richness (`2.00`) with zero render lag.
- **Unclipped Responsive Sliders**: Intelligent layout hierarchy reserves full space for all positioning, scale, mirroring, and FX controls (`side="bottom"` priority), dynamically scaling the render viewport to prevent clipping on any monitor.
- **High-DPI Vector Icons & 3D Tactile Buttons**: Studio-grade 4x supersampled geometric icons with beveled 3D rim highlights for tactile, customer-grade usability.
- **Real-Time Texture Movement & Resizing**: Slide patterns horizontally (**Texture X**) and vertically (**Texture Y**), and scale textures (**Texture Scale: 0.10x – 5.00x**) with symmetrical center-anchored scaling.
- **Dedicated Image File Resizer**: One-click texture file resizing (`Resize Image`) supporting 4K, 2K, 1K, 512px, 50%, and custom dimensions with Lanczos resampling.
- **OptiX GPU + CPU Hybrid Raytracing**: Hardware-accelerated Ray Tracing & Tensor AI Denoising delivers ultra-fast previews in **~0.17s–0.3s**.
- **Auto-Render on Slider Release & Pending Queue**: Releasing sliders automatically triggers preview renders, while a non-blocking queue guarantees rapid adjustments are never dropped.
- **Instant PIL Compositing (<10ms)**: Adjusting `Brightness`, `Contrast`, `Saturation`, `Studio Background`, or `Transparent Background` updates the preview canvas instantly via PIL without re-rendering in Blender.
- **Direct Switchers & Reset**: Switch active weapon models and textures directly in the preview header, or click **Reset All** to snap back to default center and unmirror, or **Default FX** to reset color grading.

---

## 🖼️ Showcase Gallery (Rendered via Headless Cycles Raytracing)

| AK-47 Showcase | AWP Showcase |
| :---: | :---: |
| <img src="docs/images/showcase_weapon_rif_ak47.png" width="450" alt="AK-47 Skin Showcase"> | <img src="docs/images/showcase_weapon_snip_awp.png" width="450" alt="AWP Skin Showcase"> |
| **Desert Eagle Showcase** | **M4A1-S Showcase** |
| <img src="docs/images/showcase_weapon_pist_deagle.png" width="450" alt="Desert Eagle Skin Showcase"> | <img src="docs/images/showcase_weapon_rif_m4a1_silencer.png" width="450" alt="M4A1-S Skin Showcase"> |

---

## ✨ Key Features

- **All 35 CS2 Weapons Included**: 3D OBJ weapon models are bundled directly inside the standalone executable and organized cleanly in `Assets/Models`.
- **Dedicated Live Preview Window**: Large 16:9 adaptive viewport with permanent topmost locking, 6 precision sliders, vector stepper buttons, and instant debounced rendering.
- **Headless Blender Integration**: Directly interfaces with Blender (CYCLES/EEVEE) in the background with OptiX GPU + CPU Hybrid acceleration.
- **Smart Framing & Alignment**: Uses global bounding-box math and orthographic scales to perfectly frame any weapon size, from a Glock to an AWP, at consistent scales.
- **Auto-Material Generation**: Automatically extracts and injects official Valve CS2 normal and roughness maps into calibrated dielectric PBR shaders (`Metallic = 0.02`, `Specular = 0.25`).
- **Batch Processing**: Render hundreds of weapon-texture permutations automatically ("All Combinations" or "Random Match").
- **Dynamic Lighting Environments**: 4 studio lighting rigs (`Studio Pro`, `Soft Workbench`, `Bright Flat`, `Dark Cinematic`) with live switching in both preview and render pipelines.
- **Full Color Grading Suite**: Built-in Brightness, Contrast, and Saturation slider integration via Python `PIL.ImageEnhance` with instant (<1ms) real-time response.
- **Slide-up Folder Drawer**: Bottom bar with one-click copyable directory paths for easy file management.

---

## 🛠️ Installation

### 1. Prerequisites
You must have the following software installed:
* [Python 3.10+](https://www.python.org/downloads/)
* [Blender](https://www.blender.org/download/) (Installed via Steam at `C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe` or automatically discovered across standard system paths)

### 2. Clone the Repository
```bash
git clone https://github.com/Smokianlord/Antigravity-CS2-Skin-Forge.git
cd Antigravity-CS2-Skin-Forge
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

*(Required packages: `customtkinter`, `Pillow`, `numpy`)*

---

## 🚀 Usage

### Option A: Running the Standalone Executable (.exe)
Download or double-click `Antigravity CS2 Skin Forge.exe`. The 35 official weapon models are bundled directly inside the executable, so it runs completely out of the box!

### Option B: Running from Python Source
```bash
python gui_app.py
```

### Compiling to a Standalone Executable (.exe)
To compile a standalone `.exe` with the weapon models bundled inside:
```bash
pyinstaller --onefile --noconsole --name "Antigravity CS2 Skin Forge" --icon="icon.ico" --add-data "icon.ico;." --add-data "Assets/Models;Assets/Models" --version-file=version.txt gui_app.py
```

### Workflow
1. Place your exported flat `.jpg` or `.png` textures into the `Input_Textures` directory (or click **⟳ Refresh** to reload textures while the app is running).
2. Launch the application.
3. Select the textures you want from the **Texture Selection** checklist.
4. Select the weapons you want to render from the **Weapon Model Selection** grid.
5. Click **`👁 Live Preview`** in the top ribbon bar to open the large preview viewport. Adjust **Texture X** and **Texture Y** to position the skin exactly where you want it.
6. Configure Render Engine (CYCLES GPU recommended), Quality Preset, Background, and Post-Processing.
7. Click **Generate** and monitor progress in the live terminal console.

---

## 📂 Directory Structure

```text
Antigravity-CS2-Skin-Forge/
│
├── "Antigravity CS2 Skin Forge.exe"  # Standalone compiled executable (all models bundled)
├── gui_app.py                       # Main CustomTkinter application and logic
├── blender_headless_render.py       # Headless Blender execution script
├── requirements.txt                 # Python dependencies
├── version.txt                      # Windows Executable metadata for PyInstaller
├── icon.ico                         # Application crosshair icon
├── CHAT_AND_DEVELOPMENT_LOG.md      # Full chronological project history & changelog
│
├── docs/                            # Documentation and media
│   └── images/                      # App screenshots & weapon showcases
│       ├── app_interface.png        # Main GUI preview
│       ├── live_preview_window.png  # Dedicated Live Preview Studio screenshot
│       └── showcase_*.png           # Photorealistic weapon renders
│
├── Input_Textures/                  # Drop your custom weapon textures here
├── Output_Renders/                  # Rendered showcases appear here
├── Output_Project_Files/            # Automatically saved .blend projects
│
└── Assets/                          # Fully self-contained local assets
    ├── Models/                      # All 35 official weapon .obj models
    └── Textures/                    # Valve CS2 normal & roughness maps
```

---

## 🔧 Configuration

Blender is automatically discovered on your system (Steam paths, standard installation directories, and system PATH). You can also configure a custom Blender executable path directly in the application via:
`Top Ribbon` -> `Configure` -> `Set Blender Executable Path`

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to open an issue or pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <i>Created with ❤️ by Smokianlord</i>
</div>
