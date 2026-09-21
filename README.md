<div align="center">
  
# Antigravity CS2 Skin Forge ????

**An automated, headless Python pipeline for generating photorealistic Counter-Strike 2 weapon skins using Blender's CYCLES & EEVEE engines.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Blender 4.0+](https://img.shields.io/badge/blender-4.0+-orange.svg)](https://www.blender.org/)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blueviolet)](https://github.com/TomSchimansky/CustomTkinter)

</div>

## ?? Description

Antigravity CS2 Skin Forge is a professional-grade UI and rendering pipeline built specifically for Counter-Strike 2 skin creators. It completely automates the grueling process of rendering 3D skin showcases. 

Simply drop your 2D design textures into the Input folder, select your target weapons (e.g. AK-47, AWP, M4A1-S) via the CustomTkinter UI, and click **Generate**. The application will silently boot Blender in headless mode, automatically align cameras to perfectly fit each weapon's bounds, configure CYCLES raytracing materials with auto-extracted normal/roughness maps, light the scene, apply post-processing filters, and output production-ready transparent PNGs.

### ? Key Features
- **Headless Blender Integration**: Directly interfaces with Blender (CYCLES/EEVEE) in the background without needing to open the software.
- **Smart Framing & Alignment**: Uses global bounding-box math and orthographic scales to perfectly frame any weapon size, from a Glock to an AWP, at consistent scales.
- **Auto-Material Generation**: Automatically extracts and injects official Valve CS2 normal and roughness maps into the node tree.
- **Batch Processing**: Render hundreds of weapon-texture permutations automatically ("All Combinations" or "Random Match").
- **Dynamic Environments**: 3 unique lighting presets (Studio Pro, Bright Flat, Dark Cinematic) and 5 dynamic background compositions (Pure White, Deep Blue, Green Screen, etc).
- **Post-Processing**: Built-in Brightness and Contrast slider integration via Python PIL.ImageEnhance.

---

## ??? Installation

### 1. Prerequisites
You must have the following software installed:
* [Python 3.10+](https://www.python.org/downloads/)
* [Blender](https://www.blender.org/download/) (Installed via Steam at C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe or update the path in gui_app.py)

### 2. Clone the Repository
\\\ash
git clone https://github.com/YOUR_USERNAME/Antigravity-CS2-Skin-Forge.git
cd Antigravity-CS2-Skin-Forge
\\\

### 3. Install Dependencies
\\\ash
pip install -r requirements.txt
\\\

*(Required packages: customtkinter, Pillow, 
umpy)*

### 4. Provide the Assets
Due to copyright, official Valve CS2 Models are not included in this repository. 
You must place the official extracted .obj weapon models in:
\Assets/Official Resources/CS2 Models/\

---

## ?? Usage

### Running the Python Source
\\\ash
python gui_app.py
\\\

### Compiling to a Standalone Executable (.exe)
If you want to distribute this to users who don't have Python installed, you can compile it using PyInstaller:
\\\ash
pyinstaller --onefile --noconsole --name "Antigravity_Skin_Forge" --icon="icon.ico" --add-data "icon.ico;." gui_app.py
\\\

### Workflow
1. Place your exported flat .jpg or .png textures into the Input_Textures directory.
2. Launch the application.
3. Select the textures you want to use from the **Texture Selection** checklist.
4. Select the weapons you want to render from the **Weapon Model Selection** grid.
5. Configure your Render Engine (CYCLES GPU is highly recommended), Quality Preset, Background, and Lighting.
6. Click **Generate** and monitor the live terminal and thumbnail preview.

---

## ?? Directory Structure

\\\	ext
Antigravity-CS2-Skin-Forge/
¦
+-- gui_app.py                  # Main CustomTkinter application and logic
+-- blender_headless_render.py  # Generated on-the-fly to execute headless blender commands
+-- requirements.txt            # Python dependencies
+-- icon.ico                    # Application icon
¦
+-- Input_Textures/             # Drop your custom weapon textures here
+-- Output_Renders/             # Fully rendered PNG/JPG showcases appear here
+-- Output_Project_Files/       # Automatically saved .blend projects for manual tweaking
¦
+-- Assets/                     # Official Valve resources (Not included)
    +-- Official Resources/CS2 Models/
    +-- CS2_Weapon/             # Contains the extracted Normal/Roughness maps
\\\

---

## ?? Configuration

If your Blender is installed in a custom location (e.g. Epic Games, standalone installer), edit line 23 in \gui_app.py\:
\\\python
blender_exe = r"C:\Path\To\Your\Blender\blender.exe"
\\\

---

## ?? Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to check the [issues page](https://github.com/YOUR_USERNAME/Antigravity-CS2-Skin-Forge/issues).

1. Fork the Project
2. Create your Feature Branch (\git checkout -b feature/AmazingFeature\)
3. Commit your Changes (\git commit -m 'Add some AmazingFeature'\)
4. Push to the Branch (\git push origin feature/AmazingFeature\)
5. Open a Pull Request

---

## ?? License

Distributed under the MIT License. See \LICENSE\ for more information.

---

<div align="center">
  <i>Developed with ?? by [YOUR_NAME / YOUR_STUDIO]</i>
</div>
