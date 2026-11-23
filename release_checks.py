"""Opt-in frozen-app checks used when validating a Windows release."""
import json
import os
from pathlib import Path
import traceback


def run(args):
    if not args:
        return 2
    report_path = Path(args[0]).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = {"success": False}
    window = None
    try:
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
        from PIL import Image, ImageDraw
        from PySide6.QtCore import QSettings, QThreadPool
        from PySide6.QtWidgets import QApplication
        import skinforge_core as core
        import gui_app

        scratch = report_path.parent / (report_path.stem + "-files")
        scratch.mkdir(exist_ok=True)
        # Do not read or write the user's normal application settings or folders.
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        for scope in (QSettings.Scope.UserScope, QSettings.Scope.SystemScope):
            QSettings.setPath(QSettings.Format.IniFormat, scope, str(scratch / "settings"))
        core.default_input_folder = str(scratch / "Input_Textures")
        core.default_out_folder = str(scratch / "Output_Renders")
        core.default_blend_folder = str(scratch / "Output_Project_Files")
        core.preview_cache_dir = str(scratch / "preview")
        app = QApplication.instance() or QApplication([])
        app.setStyle("Fusion")
        app.setStyleSheet(gui_app.QSS)
        window = gui_app.MainWindow()
        window.show()
        app.processEvents()
        assert core.APP_VERSION in window.windowTitle(), "Wrong application version"
        weapons = core.scan_weapons()
        assert len(weapons) == 35, "Weapon models are missing"
        weapon = next(w for w in weapons if w["name"] == "AK-47")
        assert Path(core.blender_script).is_file(), "Renderer is missing"
        assert Path(weapon["normal"]).is_file(), "AK-47 normal map is missing"
        assert Path(weapon["rough"]).is_file(), "AK-47 roughness map is missing"
        settings = window.collect_settings()
        assert settings.lighting == "Studio Pro", "Unexpected fresh-install lighting"
        report.update(version=core.APP_VERSION, weapons=len(weapons),
                      normal_maps=sum(w["normal"] != "NONE" for w in weapons),
                      roughness_maps=sum(w["rough"] != "NONE" for w in weapons),
                      renderer=core.blender_script, qt_window=True)
        window.close()
        window = None
        QThreadPool.globalInstance().waitForDone()

        if "--render" in args:
            texture = scratch / "palette.png"
            image = Image.new("RGB", (512, 512))
            draw = ImageDraw.Draw(image)
            colors = [(128, 128, 128), (220, 220, 220), (230, 110, 20),
                      (190, 30, 130), (30, 160, 170), (30, 30, 30)]
            for i, color in enumerate(colors):
                draw.rectangle((0, i * 512 // 6, 511, (i + 1) * 512 // 6), fill=color)
            image.save(texture)
            report["renders"] = []
            for engine in core.ENGINES:
                settings.engine = engine
                settings.compute = "GPU Only"
                settings.quality = "Fast Draft"
                out = scratch / ("render-" + engine.split()[0] + ".png")
                command = core.build_command(core.find_blender(), weapon, str(texture),
                                             str(out), "SKIP", settings.quality,
                                             settings, transparent=True)
                core.run_blender(command)
                with Image.open(out) as rendered:
                    assert rendered.size == (1280, 720), "Wrong render resolution"
                    assert rendered.getchannel("A").getextrema() == (0, 255), "Invalid silhouette"
                report["renders"].append({"engine": engine, "image": str(out)})
        report["success"] = True
    except Exception:
        report["error"] = traceback.format_exc()
    finally:
        if window is not None:
            window.close()
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0 if report["success"] else 1
