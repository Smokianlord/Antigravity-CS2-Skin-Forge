# Antigravity CS2 Skin Forge v1.2.0

[![Release](https://img.shields.io/badge/Release-v1.2.0-red.svg)](https://github.com/Smokianlord/Antigravity-CS2-Skin-Forge/releases/tag/v1.2.0)
[![Blender](https://img.shields.io/badge/Blender-4.0%2B%20%7C%205.x-orange.svg)](https://www.blender.org/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20x64-0078d7.svg)](https://microsoft.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Antigravity CS2 Skin Forge (v1.2.0)**, created by **Smokianlord**, is a professional-grade UI and automated rendering studio for Counter-Strike 2 skin designers and 3D weapon artists. Version 1.2.0 brings full **Image Resizing & Scaling capabilities** across the entire pipeline, alongside blazing-fast **GPU (OptiX) + CPU Hybrid Hardware Acceleration** that accelerates preview and production renders up to 4x faster.

---

## 🚀 What's New in v1.2.0

### 📐 Comprehensive Image Resizing & Scaling
- **Interactive Texture Scale Slider (0.10x – 5.00x)**:
  - Added a dedicated `Texture Scale` slider in the **Adjustments** panel and the **Live Preview** window.
  - Scale texture patterns seamlessly up and down across weapon geometry.
- **Center-Anchored Mathematical Scaling**:
  - Zooming in or out scales symmetrically from the visual center of the weapon rather than shifting toward screen corners.
  - Combines seamlessly with `Texture X` and `Texture Y` translation sliders.
- **Dedicated Image File Resizer Tool**:
  - Accessible via `📐 Resize Image` button in the Texture Selection header or `Edit -> Resize Texture Image...` in the top ribbon.
  - One-click presets: **4K (3840px)**, **2K (2048px)**, **1K (1024px)**, **512px**, **50% half-scale**, or custom width/height.
  - Aspect ratio preservation toggle with high-quality **Lanczos** interpolation.
  - Save as a new texture file (non-destructive) or overwrite original, automatically reloading into the active checklist and preview.
- **Quick Reset Controls**:
  - "Reset All" resets position (0.00, 0.00) and scale (1.00x).
  - Dedicated "1.0x Scale" button in the preview studio.

### ⚡ Ultra-Fast GPU + CPU Hybrid Hardware Acceleration
- **OptiX Hardware Acceleration for RTX GPUs**:
  - Auto-detects and activates NVIDIA OptiX hardware ray-tracing acceleration on RTX series GPUs (with automatic fallback to CUDA, AMD HIP, and Intel oneAPI).
- **True GPU + CPU Hybrid Rendering**:
  - Compute Device selector upgraded to `GPU + CPU (Hybrid)`, `GPU Only`, and `CPU Only`.
  - In Hybrid mode, Cycles distributes raytracing work concurrently across both the GPU and multi-threaded CPU cores for maximum performance.
- **Real-Time Hardware AI Denoising**:
  - Automatically engages OptiX Tensor core AI denoising (or OpenImageDenoise fallback) to produce noise-free renders instantly.
- **Blazing-Fast Live Preview (~0.5s)**:
  - Preview render speed accelerated by nearly 4x (from ~2.0s down to ~0.5s–0.7s).
  - Preview-optimized light path bounces (diffuse: 1, glossy: 1, transmission: 0, max bounces: 2) and adaptive sampling.
  - Eliminated redundant texture packaging overhead (`pack_all`) during preview renders.
- **Non-Blocking Preview Event Queue**:
  - Moving sliders rapidly no longer drops updates. A smart pending queue immediately renders the latest slider state as soon as the in-flight frame completes.

---

## 📂 Key Files Updated
* `gui_app.py`: Integrated Texture Scale slider, GPU+CPU hybrid options, event queue, Image Resizer dialog, and updated UI menus.
* `blender_headless_render.py`: Implemented OptiX/CUDA/CPU hybrid device detection, AI denoiser, preview bounce optimization, and center-anchored UV scaling.
* `version.txt`: Incremented product and file version to `1.2.0.0`.
* `Antigravity CS2 Skin Forge.exe`: Recompiled standalone Windows x64 executable.

---

## 📦 Release Assets & Checksums

| File | Size | Format | Description |
| :--- | :--- | :--- | :--- |
| **`Antigravity-CS2-Skin-Forge-v1.2.0-Windows.zip`** | `~55.5 MB` | ZIP Archive | Recommended standalone bundle containing `Antigravity CS2 Skin Forge.exe`. |
| **`Antigravity CS2 Skin Forge.exe`** | `~58.2 MB` | Windows Executable | Standalone portable executable (v1.2.0.0, 64-bit). |
| **`Antigravity-CS2-Skin-Forge-v1.2.0-SHA256SUMS.txt`** | `194 B` | Plain Text | SHA-256 integrity checksum file. |

### 🔒 SHA-256 Checksums
```text
6b6ac959601cd59d1c36dd2cca5998c836779b38a16d99674fad1aab9033f00c *Antigravity CS2 Skin Forge.exe
dd415189577cf501a48fb04d1f0570f5e42be361b6112d9c62a11b1b38a83e77 *Antigravity-CS2-Skin-Forge-v1.2.0-Windows.zip
```

