# Antigravity CS2 Skin Forge

A Windows app that puts your own 2D pattern images onto CS2 weapon models and renders them with Blender, so you can see what a skin looks like on the gun.

<img src="docs/images/app_interface.png" alt="Antigravity CS2 Skin Forge main window" width="950">

## What it does

- Takes your texture images and maps them onto any of the 35 bundled CS2 weapon models.
- Shows a live 3D preview next to the controls while you adjust placement, scale, flip and colour.
- Renders the final images in the background with Blender (Cycles or Eevee) and saves `.blend` project files.
- Can render many weapon/texture combinations in one batch.

<img src="docs/images/placement_tab.png" alt="Placement tab with the live preview" width="950">

## Example renders

| AK-47 | AWP |
| :---: | :---: |
| <img src="docs/images/showcase_weapon_rif_ak47.png" width="450" alt="AK-47 render"> | <img src="docs/images/showcase_weapon_snip_awp.png" width="450" alt="AWP render"> |
| **Desert Eagle** | **M4A1-S** |
| <img src="docs/images/showcase_weapon_pist_deagle.png" width="450" alt="Desert Eagle render"> | <img src="docs/images/showcase_weapon_rif_m4a1_silencer.png" width="450" alt="M4A1-S render"> |

## Features

- Tabs for each step: Textures, Weapons, Placement, Color, Render, Output.
- Add textures with the button or by dragging files onto the window.
- Sliders you can drag, type into or nudge with the arrow keys, each with a reset.
- Brightness, contrast and saturation, applied the same way to the preview and the final render.
- Transparent background or a solid colour (dark grey, deep blue, black, white, green screen).
- Weapon search by category, plus Select all, Clear and Random 3.
- 4 lighting setups: Studio Pro, Soft Workbench, Bright Flat, Dark Cinematic.
- Make a resized copy of a texture (4096 / 2048 / 1024 / 512 or custom). The original is never changed.
- Cancel a running batch at any time.

## Requirements

- Windows
- [Blender](https://www.blender.org/download/) 4.0 or newer. The app finds it automatically (including the Steam version); otherwise set `blender.exe` in the **Output** tab.

## How to use

1. Run `Antigravity CS2 Skin Forge.exe`. The weapon models are built into it.
2. **Textures:** add your images and click the ones to include.
3. **Weapons:** tick the weapons to render.
4. **Placement:** position the pattern while watching the preview.
5. **Color:** adjust brightness, contrast, saturation and background.
6. **Render:** choose lighting, quality, engine (Cycles GPU is best) and batch mode.
7. Click **Generate skins & renders**.

## Run from source

Python 3.12+:

```bash
pip install -r requirements.txt
python gui_app.py
```

Build the exe:

```bash
pyinstaller --onefile --noconsole --name "Antigravity CS2 Skin Forge" --icon="icon.ico" --add-data "icon.ico;." --add-data "Assets/Models;Assets/Models" --version-file=version.txt gui_app.py
```

## License

MIT, see [LICENSE](LICENSE).
