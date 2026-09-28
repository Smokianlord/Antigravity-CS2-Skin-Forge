# Release Notes - Antigravity CS2 Skin Forge v1.2.5

**Release Date:** September 28, 2026  
**Build Target:** Windows 10 / 11 (64-bit)  
**Binary Executable:** `Antigravity CS2 Skin Forge.exe`  
**Version:** `1.2.5.0`

---

## 🚀 Key Highlights & What's New

### 1. 🛡️ Render Button Visibility & Layout Pinning Fix
- **Root Cause Addressed**:
  - In previous builds, Tkinter's packing queue allocated vertical cavity space sequentially from top to bottom (`settings_container` -> `post_container` -> `bottom_container`).
  - When running at the default window height (760px) or on displays with Windows DPI scaling (125%/150%), the combined height of settings and post-processing controls starved the bottom container, squeezing `btn_generate` down to 1 pixel (`winfo_ismapped() == False`), rendering it completely invisible.
- **Architectural Solution**:
  - **Bottom Dock Priority**: Inverted the pack order so `self.bottom_container` is packed with `side="bottom", fill="x"` **FIRST**. This guarantees the hero `GENERATE 3D SKINS & RENDERS` button is permanently mapped, elevated, and 100% visible on any resolution or display scaling.
  - **Responsive Scrollable Frame**: Encapsulated `settings_container` and `post_container` inside a clean `CTkScrollableFrame` (`self.right_scroll`). If screen height is constrained or directories footer is expanded, the upper options scroll smoothly without ever pushing or clipping the execution bar.
  - **Dynamic Adaptive Window Geometry**: Increased default window height dynamically up to 820px (`min(820, max(740, screen_height - 80))`) with a minimum window clamp (`minsize(1100, 600)`), ensuring plenty of vertical space on standard 1080p monitors.

### 2. ⚡ Live Preview Render Shortcut Button
- **Direct Header Trigger**: Added a prominent 3D tactile **`Render All Skins`** hero button directly into the **Live Preview Window** header next to `Update Preview`.
- **Bidirectional State Sync**:
  - Clicking `Render All Skins` from either the Main Studio or the Live Preview Studio automatically triggers full batch rendering.
  - Button state and label (`FORGING SKINS IN PROGRESS...` / `Forging Skins...`) stay perfectly synchronized across both windows in real-time.

### 3. 🔍 Comprehensive UI Button Overlap & Squeezing Audit
- **Deep Recursive Layout Audit**: Developed an automated bounding-box and dimension inspection engine analyzing sibling widget geometries and requested vs. actual dimensions across all resolutions down to minimum size boundaries (`1100x600` main window, `860x660` preview window).
- **Preview Window Header Squeezing Fix**:
  - **Issue**: Left-packed title and status labels expanded dynamically, crowding right-packed buttons and compressing `Update Preview` (`pw_btn_refresh`) from 135px down to 24px (text severely clipped).
  - **Resolution**: Encapsulated header buttons inside a dedicated `pw_btn_box = ctk.CTkFrame(pw_header, fg_color="transparent")` with guaranteed right alignment, compacted status indicator to `"● Ready"` / `"⚡ Rendering..."`, and truncated texture names to guarantee 230px+ clearance.
- **Settings Checkbox Squeezing Fix**:
  - **Issue**: In `chk_grid`, `.blend File` and `Transparent Alpha` were co-packed into a single cell in Column 1, compressing the `Transparent Alpha` label to 58px.
  - **Resolution**: Separated into distinct rows (Row 5 Col 1 for `.blend File`, Row 6 Col 1 for `Transparent Alpha`) and balanced column gutters (`padx=(14, 6)` Col 0, `padx=(6, 14)` Col 1).
- **Responsive Label & Hint Optimization**:
  - Compacted mirror checkboxes to `Flip X (⇄)` and `Flip Y (⇅)`.
  - Streamlined helper hint labels in both main studio and live preview to eliminate text overflow clipping at minimum width constraints.

### 4. 🎯 Snug Button Padding & Top Ribbon Menu Optimization
- **Dynamic `TopBarMenu` Component**:
  - Subclassed `ctk.CTkOptionMenu` to create `TopBarMenu`, reducing dropdown chevron reservation from 28px down to 10px and dynamically computing button width (`left_pad + text_width + 4px + arrow_width + 4px`).
  - Standardized snug ~8px gap between label and chevron across all top ribbon menus (`File` 45px, `Edit` 46px, `Configure` 80px, `Help` 51px).
  - Added unified `#27272a` hover state across label and chevron.
- **Excess Space Elimination Across UI**:
  - Removed artificial leading spaces and hardcoded fixed widths from buttons across the app.
  - Buttons (`Live Preview`, `Clear`, `Select All`, `Refresh`, `Resize Image`, `Random (3)`, `Reset All`, `1.0x Scale`, `Default FX`, resizer presets `4K`, `2K`, `1K`, `512px`, `50%`) now hug their text and icons snugly with clean, professional padding.

### 5. 🎨 `.blend` Project Output Texture Alignment & Viewport Defaults
- **Object-Space Camera Projection**:
  - Replaced screen-space `Window` texture coordinates with camera `Object` coordinates (`tc_node.object = cam_obj`, `tc_node.outputs["Object"]`).
  - Anchors the texture projection directly to the orthographic camera's local coordinate system in 3D world units, guaranteeing identical texture placement in both headless batch rendering and interactive Blender GUI navigation.
  - Mathematical parity verification confirmed **0.000 mean difference and 0 max difference (`[0, 0, 0, 0]`)** across all channels.
- **Automatic Camera View & Material Shading on Open**:
  - Automatically configures all 3D Viewport spaces before saving the `.blend` file (`view_perspective = 'CAMERA'`, `shading.type = 'MATERIAL'`). Opening the project in Blender immediately displays the camera view and real-time rendered textures.
- **Standardized 16:9 Preview Resolution**:
  - Upgraded Live Preview resolution from 854x480 to **960x540** (true 16:9 540p), matching the aspect ratio of 720p, 1080p, 1440p, 4K, and 8K renders.

---

## 🛠️ Verification & Quality Assurance

- **Tkinter Mapping Verification**: Tested via automated geometry inspection (`app.update()`); `btn_generate.winfo_ismapped()` confirmed `1` (visible, 520x50px).
- **Full App Overlap Audit**: Automated collision detection across all windows, frames, scrollable containers, and dialogs confirmed **0 overlaps** and **0 squeezed buttons**.
- **Blender Parity Test**: Headless Cycles/EEVEE render vs. `.blend` file render confirmed 100% pixel parity.
- **PyInstaller Packaging**: Standalone executable recompiled and verified (`Antigravity CS2 Skin Forge.exe`).
- **Updated Media**: Captured authentic high-resolution screenshots for `app_interface.png` and `live_preview_window.png`.

---

## 📦 Distribution Files

| File | Description |
|---|---|
| `Antigravity CS2 Skin Forge.exe` | Standalone Windows 64-bit Application (v1.2.5) |
| `Antigravity-CS2-Skin-Forge-v1.2.5-Windows.zip` | Complete portable release package |
| `Antigravity-CS2-Skin-Forge-v1.2.5-SHA256SUMS.txt` | SHA-256 verification checksums |

