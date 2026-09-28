# Antigravity CS2 Skin Forge — Release Notes v1.2.1

**Release Date:** September 28, 2026  
**Author:** Smokianlord  
**Binary:** `Antigravity CS2 Skin Forge.exe` (Standalone Windows x64)

---

## 🌟 What's New in v1.2.1

### 1. 📌 Preview Window Always On Top of App (Fixed Z-Ordering)
- **Root Window Ownership (`transient`)**: Configured the Live Preview studio as a transient window of the root application. Under Windows Desktop Window Manager (DWM), transient windows are strictly pinned above their owner, preventing the preview window from ever sinking behind the main interface when clicking controls or interacting with settings.
- **Topmost Priority**: Embedded `-topmost` attribute flag and forced focus on launch with micro-delayed focus preservation callbacks.
- **"Always on Top" Header Switch**: Added a dedicated, tactile `Always on Top` checkbox directly in the preview window header (enabled by default) giving users instant visual confirmation and full control.

### 2. 🎛️ Permanent Fix for Hidden Preview Sliders
- **Protected Packing Order**: Repositioned the bottom adjustment panel (`pw_controls`) to bind to `side="bottom"` before viewport allocation. Tkinter's layout engine now reserves 100% of the required vertical space for sliders prior to viewport sizing, guaranteeing that `Brightness`, `Contrast`, and tip rows are never clipped or pushed off-screen.
- **Dynamic 16:9 Viewport Scaling**: Replaced fixed 540p canvas sizing with an adaptive 16:9 bounding calculator that monitors window resize events (`<Configure>`). The preview image automatically expands or contracts smoothly to fill the exact available screen real estate without overflowing.
- **Expanded Default Window Dimensions**: Increased default window footprint to `1120x820` (capped at 88% screen height) with minimum constraints (`860x620`).
- **Added "Default FX" Reset**: One-click tactile reset button to restore Brightness (1.00) and Contrast (1.00).

### 3. 🎨 High-DPI Vector Icons (Replaced Blurry Emojis)
- Replaced fuzzy system emoji fonts (`⟳`, `📐`, `👁`, `⚡`, `▼`) with a dedicated `IconBuilder` vector engine.
- Uses **4x supersampled geometric rendering** in Pillow downscaled with `LANCZOS` anti-aliasing to generate razor-sharp, pixel-perfect alpha-transparent `CTkImage` icons across all display DPI scalings (100%, 125%, 150%, 200%).
- Crisp iconography added for:
  - **Live Preview** (Almond aperture eye)
  - **Refresh & Update** (Symmetrical circular cycle arrows)
  - **Resize Image** (Expanding diagonal transform arrows)
  - **GENERATE 3D SKINS** (Illuminated isometric 3D cube)
  - **Random Pick** (Crisp 3D dice)
  - **Select All & Clear** (Crisp checkmarks and square clear boxes)
  - **Directories** (Crisp folder glyph)
  - **Reset All & Default FX** (Circular rewind arrow and dual-slider rails)

### 4. 🕹️ 3D Tactile Hardware Aesthetics
- **Primary 3D Action Buttons**: Formatted with high-contrast bevel highlights (`border_width=2`, `border_color="#fca5a5"` on `#dc2626` base), providing a physical raised push-button appearance.
- **Secondary 3D Slate Buttons**: Formatted with an etched metallic bezel (`border_width=1.5`, `border_color="#52525b"` on `#27272a` base).
- **Tactile Thumb Sliders**: Upgraded slider handles with crisp white perimeter rings (`border_width=2`, `border_color="#ffffff"`), turning flat circles into 3D metallic potentiometer knobs.
- **Modular Studio Cards**: Wrapped containers with subtle obsidian borders (`border_width=1`, `border_color="#27272a"`, `fg_color="#141417"`), giving the interface the look and feel of high-end creative software suites.

---

## 📂 Verification & Hashes
Upon completion of the build, standalone executable and distribution archives are validated with SHA-256 signatures.
