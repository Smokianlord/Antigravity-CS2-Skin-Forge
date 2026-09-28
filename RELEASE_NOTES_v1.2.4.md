# Release Notes - Antigravity CS2 Skin Forge v1.2.4

**Release Date:** September 28, 2026  
**Build Target:** Windows 10 / 11 (64-bit)  
**Binary Executable:** `Antigravity CS2 Skin Forge.exe`  
**Version:** `1.2.4.0`

---

## 🚀 Key Highlights & What's New

### 1. 🔄 Texture Mirroring & Axis Reflection (Flip X & Flip Y)
- **Horizontal & Vertical Reflection**: Added dedicated texture mirroring toggles:
  - **Flip Horizontal (⇄ Flip X)**: Inverts the texture along the horizontal axis with center-point preservation.
  - **Flip Vertical (⇅ Flip Y)**: Inverts the texture along the vertical axis with center-point preservation.
- **Center-Anchored Shader Coordinates**:
  - Automatically calculates center-anchored UV transformation offsets:
    $$\text{eff\_sx} = -\text{sx} \quad \text{if flip\_x else} \quad \text{sx}$$
    $$\text{eff\_sy} = -\text{sy} \quad \text{if flip\_y else} \quad \text{sy}$$
    $$\text{loc\_x} = 0.5 \times (1.0 - \text{eff\_sx}) + \text{offset\_x}$$
    $$\text{loc\_y} = 0.5 \times (1.0 - \text{eff\_sy}) + \text{offset\_y}$$
  - Guarantees patterns flip perfectly around the weapon's focal center without shifting out of view.
- **Dual Controls**: Mirroring toggles are accessible directly in the Main Window Post-Processing card and as tactile 3D buttons in Row 3 of the Live Preview Window controls.
- **Auto-Sync & Preview**: Toggling either flip option instantly updates both interfaces and triggers an accelerated live viewport preview.

### 2. ⚡ Ultra-Responsive Live Preview & Performance Optimizations
- **2x Faster Preview Debounce**: Slider debounce timer reduced from 350ms to **160ms**, giving near-instantaneous feedback during slider adjustments.
- **High-Speed Real-Time Viewport Resizing**: Preview viewport scaling upgraded to lightning-fast `BILINEAR` resampling for seamless, lag-free UI resizing.
- **Calibrated Raytracing Samples**:
  - `Preview (540p | 4 Samples)`: Renders in ~170ms on RTX GPU via OptiX hardware raytracing.
  - `Fast Draft (720p | 16 Samples)`: Ultra-fast proofing in ~0.5s.
  - `Standard (1080p | 32 Samples)`: Default preset, crisp 1080p render in ~1.0s.
  - `High (1440p | 48 Samples)`: Clean 2K resolution in ~1.5s.
  - `Ultra (4K | 64 Samples)`: Ultra HD in ~1.9s.
  - `Masterpiece (8K | 96 Samples)`: Uncompromising 8K showcase render in ~7.5s.
- **Hybrid GPU + CPU Architecture**: Full OptiX RT Cores hardware AI denoising + multi-threaded CPU acceleration.

### 3. 🎯 Generate Button Fixed & Clean Status Badge
- **Permanently Pinned Execution Bar**: The `GENERATE 3D SKINS & RENDERS` hero button is packed with `side="bottom", fill="x"`, guaranteeing it is 100% visible at all times regardless of screen resolution or DPI scaling.
- **Removed Bulky Log Window**: Eliminated the redundant green terminal box, reclaiming ~100px of vertical space.
- **Sleek Live Status Badge**: Integrated an elegant, color-coded single-line status indicator (`● Engine Ready`, `⚡ Initializing...`, `✔ Success`, `✖ Error`).
- **Dynamic Button State**: Button displays `FORGING SKINS IN PROGRESS...` with amber progress indicator during batch generation, returning to active state on completion.

---

## 🛠️ Verification & Quality Assurance

- **Blender 5.2.2 LTS Verified**: Tested with Blender headless Cycles / OptiX pipeline.
- **Hardware Validated**: Benchmarked on NVIDIA GeForce RTX 5080 + AMD Ryzen 7 9850X3D.
- **Thread Safety**: All Tkinter state variables read safely on the main thread prior to worker dispatch.
- **Packaging Integrity**: Standalone executable bundle size is ~30 MB, excluding heavy asset folders.

---

## 📦 Distribution Files

| File | Description |
|---|---|
| `Antigravity CS2 Skin Forge.exe` | Standalone Windows 64-bit Application (v1.2.4) |
| `Antigravity-CS2-Skin-Forge-v1.2.4-Windows.zip` | Complete portable release package |
| `Antigravity-CS2-Skin-Forge-v1.2.4-SHA256SUMS.txt` | SHA-256 verification hashes |
