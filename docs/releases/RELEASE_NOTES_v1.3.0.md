# Release Notes - Antigravity CS2 Skin Forge v1.3.0

**Release Date:** October 23, 2026
**Build Target:** Windows 10 / 11 (64-bit)
**Binary Executable:** `Antigravity CS2 Skin Forge.exe`
**Version:** `1.3.0.0`

---

## Highlights

### Complete UI overhaul on Qt (PySide6)
- The window was rebuilt from CustomTkinter to Qt. Resizing and scrolling are now smooth (about 5 ms per resize step, down from about 380 ms), because the old toolkit paid a per-widget cost on every resize.
- New dark theme with an orange accent and a new application icon.

### Designer-first workflow
- **Live 3D preview is always visible** next to the controls. Scroll to zoom, drag to pan, double-click to fit, and switch between the **3D Render** and the **Source texture**.
- **One tab per job:** Textures, Weapons, Placement, Color, Render, Output.
- **Texture thumbnails + large preview:** see every image as a thumbnail, click to include it in the batch, and view the selected one large (with size and dimensions) and rendered live on the weapon.
- **Add images** with a button or by dragging files onto the window. New files are selected and previewed immediately.
- **Sliders** accept dragging, exact typed values and arrow-key nudges, each with its own Reset.
- **Weapon search**, grouped by category, with Select all / Clear / Random 3.
- **Resize...** creates a resized copy of a texture (the original is never overwritten).
- Settings (folders, Blender path, render options) are remembered between sessions.

### Faster previews
- Preview renders use cached 1K copies of the large 4K weapon maps.

## Fixes
- Brightness below 1.0 no longer makes renders partly transparent (color grading now leaves alpha untouched).
- JPEG export with Transparent enabled no longer fails; it composites onto the chosen background.
- Output files are named from the full texture name, so textures that share a first word no longer overwrite each other.
- Preview and export failures now show the real error; a clear message appears when Blender cannot be found.
- Batch renders can be cancelled.
- Menu hover crash and Tk thread-safety problems from the old UI are gone with the rewrite.

## Requirements
- Blender 4.0+ installed (auto-detected, or set in the **Output** tab).
- Running from source: `pip install -r requirements.txt` (now `PySide6-Essentials` and `Pillow`; `customtkinter` and `numpy` are no longer needed).
- The executable is larger (about 41 MB) because it bundles Qt.

## Checksums
See `Antigravity-CS2-Skin-Forge-v1.3.0-SHA256SUMS.txt`.
