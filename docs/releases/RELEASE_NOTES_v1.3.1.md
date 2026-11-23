# Antigravity CS2 Skin Forge v1.3.1

Released November 24, 2026. Windows 10/11, 64-bit.

## Rendering improvements

- Brighter painted surfaces with controlled highlights instead of the old burned-out colors.
- Directional overhead reflections and softer fill give the weapon more depth, with clearer rivets, edges and recessed details.
- Roughness is read from the map's red channel rather than mixed with unrelated channels.
- Restored neutral specular response and added a restrained paint topcoat that follows the normal map.
- Camera-relative lights keep illumination consistent across differently oriented models.
- Khronos PBR Neutral controls bright highlights on Blender 4.2+. Blender 4.0/4.1 uses Standard as a fallback.
- Preview samples increased from 4 to 8 to better resolve surface highlights.
- Saved Blender projects retain the actual export path and image format.

## Complete portable package

The ZIP now includes all 68 bundled weapon normal/roughness maps, compressed losslessly with pixel equality checked. These were missing from the previous portable ZIP. The new archive is larger because it includes the surface data needed for the updated rendering.

The executable bundles the 35 weapon models and a fallback copy of the renderer. An external renderer is also supplied for updates. The package includes an asset manifest and SHA-256 checksums.

## Install or upgrade

1. Download `Antigravity-CS2-Skin-Forge-v1.3.1-Windows.zip` and extract the entire ZIP into a new folder.
2. Keep `Assets/Textures` and `blender_headless_render.py` beside the executable. Do not run the app from inside the ZIP.
3. Run `Antigravity CS2 Skin Forge.exe`. Blender 4.0+ must be installed separately.
4. Select **Studio Pro** and reset the Color sliders to **1.0** for the intended appearance.
5. When upgrading, check the remembered input/output folders in the Output tab. Your previous texture and render folders can still be used.

## Validation and limits

The corrected renderer was checked in Cycles and Eevee on Blender 5.3.0, across all four lighting rigs, including missing-map fallback. A same-camera neutral-grey comparison confirmed greater highlight/shadow separation while the colored test retained its brightness without clipped channels. Older Blender versions have not been tested.

This is a Blender paint preview. An exact Source 2 result still requires the CS2 Workshop Item Editor and the matching finish materials.

## Downloads

- Windows portable ZIP: includes the executable, renderer and weapon surface maps.
- SHA-256 checksum file: verify the ZIP before extracting.
