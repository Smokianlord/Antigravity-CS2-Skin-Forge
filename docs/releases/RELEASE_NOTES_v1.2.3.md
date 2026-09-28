# Antigravity CS2 Skin Forge — Release Notes v1.2.3

**Release Date:** September 28, 2026  
**Author:** Smokianlord  
**Binary:** `Antigravity CS2 Skin Forge.exe` (Standalone Windows x64)

---

## 🌟 What's New in v1.2.3

### 1. 🎨 True Color Fidelity & Artwork Brightness Calibration
- **Tone Curve Overhaul**: Replaced Blender's default `AgX` view transform (which aggressively desaturated and bleached high-luminance colors into chalky whites) with calibrated **`Standard`** colorimetry. Artwork renders true to original texture color values, depth, and contrast.
- **Calibrated Studio Lighting Multipliers**: Rebalanced key, fill, and rim light energy formulas from overpowering `5.0x` multipliers down to physically balanced `1.2x` and `1.0x` levels, eliminating specular burn-in and highlight blow-outs.
- **Dielectric Weapon Material Formulation**: Calibrated default weapon shader properties (`Metallic = 0.02`, `Specular = 0.25`) to match authentic CS2 factory finish without artificial metallic glare washing out pattern artwork.
- **New "Soft Workbench" Lighting Preset**: Added a dedicated diffuse workbench illumination preset designed specifically for inspecting fine texture details without harsh directional highlights.

---

### 2. 🎛️ Dedicated Saturation & Color Vibrance Adjustment
- **Real-Time Saturation Slider (`0.00` to `2.00`)**: Added a 6th precision adjustment slider across both the **Live Preview Window** and the **Main Window Adjustments Block**.
- **Instant Response (<1ms)**: Leverages real-time PIL color enhancement so creators can fine-tune color vibrance, desaturate to monochrome (`0.00`), or boost punchy vibrant tones (`1.50+`) with zero render lag.
- **Precision Steppers & Shortcuts**:
  - Stepper arrows `[ ◀ ]` and `[ ▶ ]` for `±0.01` micro-adjustments.
  - Keyboard arrow key nudging and `Shift` 5x acceleration (`±0.05`).
  - Hotkey `6` or `Tab` cycling for instantaneous focus.
- **Default FX Reset**: Clicking **Default FX** resets Brightness, Contrast, and Saturation back to `1.00` in a single click.

---

### 3. 💡 Dynamic Lighting Rig Selector in Preview & Main Windows
- **Live Preview Window Controls**: Added an accessible **Lighting:** selector menu directly into row 1 of the Live Preview Window bottom controls bar.
- **Instant Rig Switching**: Switch between `"Studio Pro"`, `"Soft Workbench"`, `"Bright Flat"`, and `"Dark Cinematic"` on the fly with automatic debounced live re-rendering.
- **Main Window Symmetry**: Integrated the Lighting Rig selector into the Main Window Render Settings container with clean 2-column symmetry.

---

### 4. 📌 Permanent Topmost Pinning (Cleaner Header UI)
- **Always on Top by Default**: The Live Preview Window is now permanently and unconditionally pinned on top of the main application using native Windows Z-order transient locking (`attributes("-topmost", True)` + `transient(self)`).
- **De-cluttered Header Bar**: Removed the redundant "Always on Top" checkbox from the preview window header, freeing up valuable screen real estate and preventing horizontal crowding on compact displays.

---

### 5. 🔀 Enhanced 6-Slider Cycling & Number Hotkeys (`1`–`6`)
- **Full Hotkey Support**:
  - `1`: Texture X Offset (`-1.00` to `1.00`)
  - `2`: Texture Y Offset (`-1.00` to `1.00`)
  - `3`: Texture Scale (`0.10x` to `5.00x`)
  - `4`: Brightness (`0.20` to `2.00`)
  - `5`: Contrast (`0.20` to `2.00`)
  - `6`: Saturation (`0.00` to `2.00`)
- **Seamless Tab Flow**: Press `Tab` or `Shift+Tab` to effortlessly cycle across all 6 sliders in order with illuminated crimson `►` indicators and glowing stepper borders.

---

## 📂 Verification & Distribution
The standalone executable has been built with PyInstaller and packaged into a clean, lightweight Windows zip distribution:
- **Zip Archive**: `Antigravity-CS2-Skin-Forge-v1.2.3-Windows.zip` (~30 MB)
- **Integrity**: Checksums provided in `Antigravity-CS2-Skin-Forge-v1.2.3-SHA256SUMS.txt`
