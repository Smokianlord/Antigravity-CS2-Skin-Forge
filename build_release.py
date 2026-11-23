"""Build the Windows executable and a portable ZIP with lossless weapon maps."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

from PIL import Image
import skinforge_core as core

ROOT = Path(__file__).resolve().parent


def sha256(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-build", action="store_true", help="Reuse the current version's compiled executable")
    args = parser.parse_args()
    version = core.APP_VERSION
    output = ROOT / "dist" / ("v" + version)
    work = ROOT / "build" / ("v" + version)
    package = output / "package"
    for folder in (output, work, package):
        folder.mkdir(parents=True, exist_ok=True)
    executable = output / "Antigravity CS2 Skin Forge.exe"
    if not args.skip_build:
        command = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
                   "--onefile", "--noconsole", "--name", "Antigravity CS2 Skin Forge",
                   "--icon", str(ROOT / "icon.ico"), "--version-file", str(ROOT / "version.txt"),
                   "--distpath", str(output), "--workpath", str(work / "pyinstaller"),
                   "--specpath", str(work)]
        for source, destination in [(ROOT / "icon.ico", "."),
                                    (ROOT / "blender_headless_render.py", "."),
                                    (ROOT / "Assets" / "Models", "Assets/Models")]:
            command.extend(["--add-data", str(source) + ";" + destination])
        for module in ["tkinter", "customtkinter", "numpy", "PySide6.QtNetwork",
                       "PySide6.QtQml", "PySide6.QtQuick", "PySide6.QtPdf",
                       "PySide6.QtSvg", "PySide6.QtOpenGL"]:
            command.extend(["--exclude-module", module])
        command.append(str(ROOT / "gui_app.py"))
        # Build tools can inherit unrelated DLL folders from editors or media
        # tools. In particular, another ICU DLL can break frozen Qt at startup.
        # Keep dependency discovery limited to Python, Qt and Windows itself.
        import PySide6
        import shiboken6
        windows = Path(os.environ.get("SystemRoot", r"C:\Windows"))
        environment = os.environ.copy()
        environment["PATH"] = os.pathsep.join(map(str, [
            Path(sys.executable).parent, Path(PySide6.__file__).parent,
            Path(shiboken6.__file__).parent, windows / "System32", windows,
        ]))
        subprocess.run(command, cwd=ROOT, env=environment, check=True)
    if not executable.is_file():
        raise FileNotFoundError(executable)
    for source in [executable, ROOT / "blender_headless_render.py", ROOT / "README.md",
                   ROOT / "docs" / "releases" / ("RELEASE_NOTES_v" + version + ".md")]:
        shutil.copy2(source, package / source.name)
    images = package / "docs" / "images"
    images.mkdir(parents=True, exist_ok=True)
    for source in (ROOT / "docs" / "images").iterdir():
        if source.suffix.lower() in (".png", ".jpg"):
            shutil.copy2(source, images / source.name)

    maps = sorted((ROOT / "Assets" / "Textures").glob("*.png"))
    if not maps:
        raise RuntimeError("Assets/Textures is empty: the release must include normal/roughness maps")
    maps_out = package / "Assets" / "Textures"
    maps_out.mkdir(parents=True, exist_ok=True)
    cache_path = work / "map-cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    for index, source in enumerate(maps, 1):
        destination = maps_out / source.name
        source_hash = sha256(source)
        cached = cache.get(source.name, {})
        if (cached.get("source") != source_hash or not destination.exists()
                or cached.get("packed") != sha256(destination)):
            with Image.open(source) as image:
                original_pixels = hashlib.sha256(image.tobytes()).hexdigest()
                image.save(destination, format="PNG", compress_level=6)
            with Image.open(destination) as image:
                if hashlib.sha256(image.tobytes()).hexdigest() != original_pixels:
                    raise RuntimeError("Pixel data changed: " + source.name)
            cache[source.name] = {"source": source_hash, "packed": sha256(destination)}
            cache_path.write_text(json.dumps(cache, indent=2), encoding="utf-8")
        print(f"Weapon map {index}/{len(maps)}: {source.name}", flush=True)

    manifest = {"version": version, "weapon_models": len(list((ROOT / "Assets/Models").glob("*.obj"))),
                "weapon_maps": len(maps), "files": {}}
    for path in sorted(package.rglob("*")):
        if path.is_file() and path.name != "asset-manifest.json":
            manifest["files"][path.relative_to(package).as_posix()] = sha256(path)
    (package / "asset-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    archive = output / ("Antigravity-CS2-Skin-Forge-v" + version + "-Windows.zip")
    with zipfile.ZipFile(archive, "w", allowZip64=True) as zipped:
        for path in sorted(package.rglob("*")):
            if path.is_file():
                # PNGs and the one-file executable are already compressed.
                mode = zipfile.ZIP_STORED if path.suffix.lower() in (".png", ".exe") else zipfile.ZIP_DEFLATED
                zipped.write(path, path.relative_to(package).as_posix(), compress_type=mode)
    checksums = output / ("Antigravity-CS2-Skin-Forge-v" + version + "-SHA256SUMS.txt")
    checksums.write_text("".join(sha256(path) + "  " + path.name + "\n"
                                 for path in [archive, executable, package / "blender_headless_render.py"]),
                         encoding="utf-8")
    print(f"Release ZIP: {archive} ({archive.stat().st_size / 1024**2:.1f} MiB)", flush=True)
    print(f"Checksums: {checksums}", flush=True)


if __name__ == "__main__":
    main()
