# Antigravity CS2 Skin Forge — Release Notes v1.2.2

**Release Date:** September 28, 2026  
**Author:** Smokianlord  
**Binary:** `Antigravity CS2 Skin Forge.exe` (Standalone Windows x64)

---

## 🌟 What's New in v1.2.2

### 1. 🎯 Precision Stepper Arrow Buttons (`[ ◀ ]` & `[ ▶ ]`)
- **Micro 3D Stepper Controls**: Added dedicated left and right stepper buttons flanking each slider across both the **Live Preview Window** and the **Main Window Adjustments Block**.
- **Vector High-DPI Icons**: Stepper buttons feature razor-sharp geometric vector arrow glyphs generated via `IconBuilder` with Lanczos anti-aliasing.
- **Accurate Granular Stepping**:
  - **Texture X & Y Offsets**: Step by `±0.01` per click.
  - **Texture Scale**: Step by `±0.05` per click.
  - **Brightness & Contrast**: Step by `±0.01` per click.
- **Automatic Focus & Activation**: Clicking any stepper arrow instantly marks that slider as the active selection and applies all visual highlights.

---

### 2. ⌨️ Comprehensive Keyboard Arrow Key Navigation
- **Universal Arrow Controls**: Press `Left` / `Down` to decrement, or `Right` / `Up` to increment the currently selected slider with zero mouse dragging required.
- **Shift Acceleration (5x Step)**: Hold `Shift` while pressing arrow keys or clicking steppers for 5x faster adjustment:
  - Offsets / Brightness / Contrast: `±0.05`
  - Scale: `±0.20`
- **Boundary Snapping**: Press `Home` to snap the active slider to its minimum value, or `End` to snap to its maximum value.
- **Smart Input Isolation**: Keyboard bindings are safely isolated — when typing into text boxes or directory paths, arrow keys retain standard text caret navigation without interfering with sliders.

---

### 3. 💡 High-Contrast Visual Selection Highlight
- **Illuminated Pointer Glyph (`►`)**: The currently active slider's title dynamically changes to bright crimson (`#ef4444`) with a leading `►` indicator, making your current position unmistakable at a glance.
- **Glowing Stepper Borders**: Active stepper buttons illuminate with a 2px crimson outline (`#ef4444`) on dark obsidian (`#27272a`), contrasting against neutral inactive buttons (`#3f3f46`).
- **Active Potentiometer Knob**: The selected slider knob transforms into vibrant brand red (`#ef4444`, hover `#f87171`) with a crimson progress bar (`#dc2626`) and halo bezel (`#fca5a5`). Inactive sliders rest in clean, distraction-free graphite (`#71717a`).
- **Accent Value Badge**: The numeric readout badge highlights in bold crimson for the active slider.

---

### 4. 🔀 Rapid Slider Switching & Cycling
- **Tab & Shift+Tab**: Seamlessly cycle through all adjustment sliders in order:
  `Texture X` ➔ `Texture Y` ➔ `Texture Scale` ➔ `Brightness` ➔ `Contrast`
- **Number Hotkeys (`1` - `5`)**: Instantly jump selection directly:
  - `1`: Texture X
  - `2`: Texture Y
  - `3`: Texture Scale
  - `4`: Brightness
  - `5`: Contrast
- **Direct Canvas Touch**: Clicking anywhere along a slider's track or dragging its knob automatically activates that slider.

---

### 5. ⚡ Debounced Hybrid Rendering & Zero-Lag Sync
- **Sub-Millisecond Color Adjustments**: Brightness and Contrast post-processing adjustments update the preview canvas in real-time (<1ms CPU/PIL processing).
- **Intelligent Render Debounce**: Rapid keyboard arrow taps or stepper button clicking debounce the headless Blender 3D render pipeline (~350ms settle window). This eliminates process thrashing while providing instantaneous UI feedback.
- **Dual-Window State Synchronization**: Offsets, scale, and FX values stay synchronized across the Main Window and Live Preview Window at all times.

---

## 📂 Verification & Hashes
The standalone distribution executable is packaged with SHA-256 integrity verification.
