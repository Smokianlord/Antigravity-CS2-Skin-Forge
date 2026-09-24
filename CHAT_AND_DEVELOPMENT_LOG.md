# Antigravity CS2 Skin Forge — Full Chat & Development History

This document contains a comprehensive record of the entire design, architectural decisions, user requests, problem-solving iterations, and feature implementations for **Antigravity CS2 Skin Forge v1.0.0**.

---

## 📌 Project Overview & Purpose
* **Project Name**: Antigravity CS2 Skin Forge
* **Target Game**: Counter-Strike 2 (CS2)
* **Author / Creator**: Smokianlord
* **Core Technology Stack**: Python 3.12, CustomTkinter, Blender 4.0+ (Headless via Python API), Pillow (PIL), PyInstaller.
* **Goal**: Provide an automated, standalone GUI application that allows CS2 skin creators to apply flat 2D texture patterns onto official 3D weapon models, frame them with mathematically perfect orthographic cameras, render them using Blender's Cycles raytracing engine (or Eevee) with studio lighting and PBR materials, post-process brightness/contrast/backgrounds, and export high-resolution presentation renders and editable `.blend` project files in batches.

---

## 🛠️ Complete Chronological Development Log

### Phase 1: Engine Foundation & Asset Discovery
* **Discovery & Model Parsing**: Located official Valve CS2 3D OBJ weapon models and their corresponding PBR normal and roughness textures across the repository.
* **Mapping Dictionary**: Built a dictionary mapping internal Valve identifiers (`weapon_rif_ak47`, `weapon_snip_awp`, `weapon_pist_glock18`, `weapon_rif_m4a1_silencer`, etc.) to clean, user-friendly display names (AK-47, AWP, Glock-18, M4A1-S, etc.).
* **Headless Blender Pipeline**: Created `blender_headless_render.py` that executes silently without opening the Blender GUI:
  - Loads OBJ model.
  - Automatically calculates 3D bounding box dimensions (`size_x`, `size_y`, `size_z`) and center point.
  - Configures an orthographic camera (`ORTHO`) aligned to the side profile.
  - Implements dynamic ortho-scale formula:
    `cam_data.ortho_scale = max(max(size_x, size_y), size_z * render_ratio) * 1.15`
    ensuring tall weapons (e.g. AWP, P90, M249) never have barrels or stocks cut off.
  - Assembles shader node tree with `Principled BSDF`, `ShaderNodeTexCoord` (Window projection), `ShaderNodeMapping`, and loads official normal and roughness textures.
  - Configures 3-point studio lighting constraints (`TRACK_TO`).
  - Supports Cycles (CUDA/GPU & CPU) and Eevee Next.

---

### Phase 2: User Interface Evolution (V1 to V9)
* Built a modern Dark Mode interface using `CustomTkinter`.
* Created high-resolution CS2-themed application icons (`icon.ico`) and embedded them in the PyInstaller executable bundle.
* Added live terminal logging (`CTkTextbox`) capturing console output from headless Blender subprocess runs.
* Implemented multi-threaded pipeline execution so the GUI never freezes while Blender renders in the background.

---

### Phase 3: UI Modernization & Ribbon System (V10 to V12)
* **User Feedback**: "Remove native Windows menu bar; it doesn't look professional. Follow modern software style like Photoshop/Illustrator."
* **Solution (V10)**: Replaced standard `tk.Menu` with a modern CustomTkinter dark ribbon bar at the top containing clickable dropdown menus:
  - `File`: Open Input Directory, Open Output Directory, Open Project Directory, Exit.
  - `Edit`: Select All Models, Deselect All Models, Select Random Model (3).
  - `Configure`: Set custom input and output folder paths.
  - `Help`: View Documentation, About.
* **Hardware & Studio Backgrounds (V11-V12)**:
  - Added "Compute Device (Cycles)" selector: `GPU` / `CPU`.
  - Added "Studio Background" selector: `Dark Grey (Default)`, `Deep Blue`, `Pure Black`, `Pure White`, `Green Screen`.
  - Background rendering implemented by rendering Blender with transparent alpha (`film_transparent = True`) and compositing using Python PIL.
  - Built custom `CTkToplevel` popup dialogs with correct taskbar icons for Help and About.

---

### Phase 4: Image Post-Processing & Previews (V13 to V14)
* **User Request**: "Add brightness editable meter bar and contrast meter | Small preview side bar | Single window for whole thing | Select texture file | Start app with all options unselected | Rename button to Generate | Completion notification."
* **Implementation (V13-V14)**:
  - Integrated `PIL.ImageEnhance.Brightness` and `Contrast` sliders (range 0.2 to 2.0).
  - Flattened interface from multi-tab layout into a unified, clean layout.
  - Defaulted all weapon checkboxes to unselected on boot.
  - Renamed render trigger button to a prominent red **Generate** button.
  - Added popup modal upon batch completion with a direct "Open Output Folder" button.

---

### Phase 5: Horizontal Aspect Ratio Overhaul (V15)
* **User Feedback**: "The app is vertically long for the monitor, make it horizontal so it fits the monitor."
* **Solution (V15)**: Redesigned window to a wide 1450x750 horizontal layout:
  - **Left Column (60%)**: Weapon selection grid and texture selection.
  - **Right Column (40%)**: Rendering engine settings, sliders, log console, and Generate button.

---

### Phase 6: Texture Checklist & Configure Menu (V16 to V17)
* **User Request**: "Random pick should choose 3 | In texture feature, select multiple or single from options vertically with file type column and scrollbar | Add Configure dropdown for I/O folders | Keep grey background frames consistent."
* **Implementation (V16-V17)**:
  - Replaced pop-up file dialog with an integrated vertical scrollable checklist showing all `.jpg`/`.png` textures from the input folder, with filename and uppercase filetype badge (`JPG`, `PNG`).
  - Added "Select All" and "Deselect All" for textures.
  - Updated "Random Pick" button in weapons section to randomly pick exactly 3 models.
  - Added `Configure` menu in top toolbar to dynamically set Input Textures, Output Renders, and Output Projects folders.
  - Unified all panel cards with consistent `#18181b` dark grey backgrounds and matching corner radiuses.

---

### Phase 7: UI Stability & Default Logic (V18)
* **User Feedback**: "Why does it jump around when I click quality presets or background? | I chose 3 textures but it rendered only one."
* **Root Cause & Fix (V18)**:
  - Dropdown jumping: CTkOptionMenu was dynamically resizing itself based on text length. Fixed by adding `dynamic_resizing=False` to all dropdowns and locking grid columns to `uniform="a"`.
  - Single render vs multi render: Generation Mode was defaulting to "Random Match" (which picks 1 random texture per weapon). Renamed options to "Random Match" and "All Combinations" and changed default to **"All Combinations"**.

---

### Phase 8: Official Release v1.0.0 Packaging (V19)
* **User Request**: "Start the app centered | Give me a github ready one with all fields | Version is v1.0.0 | Show version in app title and in windows exe | In about show created by Smokianlord."
* **Implementation**:
  - Dynamically calculates screen resolution on launch and centers the 1450x750 window on the primary monitor.
  - Generated full GitHub open-source repository files: `README.md`, `requirements.txt`, and `.gitignore`.
  - Created PyInstaller Windows resource manifest `version.txt` embedding Product Version `1.0.0.0` and Company/Copyright `Smokianlord` into the compiled `.exe` properties.
  - Updated app title to `Antigravity CS2 Skin Forge v1.0.0` and About popup credits.

---

### Phase 9: Texture Refresh & Texture Movement Sliders
* **User Request**: "1. Add a refresh button for textures if new textures are added while app is open. 2. Live preview window before going full rendering. 3. Give me ability to move around the texture."
* **Implementation**:
  - Added `⟳ Refresh` button in Texture Selection header.
  - Added `Texture X` and `Texture Y` sliders (range -1.0 to 1.0) under Adjustments.
  - Modified Blender script to accept `tex_offset_x` and `tex_offset_y` and apply them to the mapping node's Location.

---

### Phase 10: Dedicated Large Live Preview Window & Layout Cleanup
* **User Feedback & Screenshot**: "I can't check it live where I am placing the texture, keep the preview window in the hidden and in the top toolbar add a button for it, remove the one above the generate button, make preview window bigger."
* **Problem Identified**: The 140x140 thumbnail and quick preview button in the right column pushed the Generate button off-screen on standard displays.
* **Solution**:
  - **Removed the box above Generate**: Deleted the 140x140 thumbnail and bottom preview button. The log console now spans full width and the big red "Generate" button is 100% visible and accessible.
  - **Top Toolbar Button**: Added a dedicated `👁 Live Preview` button on the right side of the top ribbon bar.
  - **Big Dedicated Preview Window**: Launches a spacious `1060x720` window with a large `960x540` 16:9 viewport.
  - **Live Texture Positioning**: Built Texture X and Texture Y sliders directly into the preview window. Moving the sliders and releasing mouse (`<ButtonRelease-1>`) auto-renders the preview in ~1.8 seconds.
  - **Instant PIL Post-Processing**: Brightness, Contrast, and Studio Background changes reflect on the preview image in 10ms without re-running Blender.

---

### Phase 11: Offset Axis Inversion & Executable Naming
* **User Feedback**: "the X and Y meter is working inversely | keep the exe name as the app title 'Antigravity CS2 Skin Forge'."
* **Root Cause & Fix**:
  - In Blender Mapping nodes (Point mode), adding positive location coordinates translates the sampled texture in the negative direction.
  - Negated `tex_offset_x = -float(tex_offset_x)` and `tex_offset_y = -float(tex_offset_y)` in the Blender render script so moving the slider right moves texture right, and moving up moves texture up.
  - Renamed compiled executable from `Antigravity_Skin_Forge.exe` to `Antigravity CS2 Skin Forge.exe`.
  - Updated `version.txt` and `README.md` to reflect the official name.

---

## 📂 Key Project Files Summary

| File | Purpose |
|---|---|
| `gui_app.py` | Main CustomTkinter UI application, state management, and orchestration |
| `blender_headless_render.py` | Standalone Python script executed headlessly by Blender for 3D rendering |
| `Antigravity CS2 Skin Forge.exe` | Compiled standalone Windows executable (standalone distribution) |
| `version.txt` | PyInstaller Windows file version resource manifest (v1.0.0.0, Smokianlord) |
| `README.md` | Complete GitHub open-source repository documentation and badges |
| `requirements.txt` | Python package dependencies (`customtkinter`, `Pillow`, `numpy`) |
| `.gitignore` | Configured to exclude virtual environments, cache, and heavy output folders |
| `icon.ico` | Embedded multi-resolution application icon |

---

## 🚀 How to Run & Build in the Future

### Running from Python:
```bash
python gui_app.py
```

### Rebuilding the Standalone Executable (.exe):
```bash
pyinstaller --onefile --noconsole --name "Antigravity CS2 Skin Forge" --icon="icon.ico" --add-data "icon.ico;." --version-file=version.txt gui_app.py
```
After building, move the resulting `.exe` from the `dist/` directory into the main folder and clean up the `build/` and `dist/` folders.
