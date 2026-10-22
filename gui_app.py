"""Antigravity CS2 Skin Forge - Qt front end. Rendering/asset logic lives in skinforge_core.py."""
import os
import random
import shutil
import sys
import threading

from PIL import Image
from PySide6.QtCore import QObject, QPointF, QRectF, QRunnable, QSettings, QSize, Qt, QThreadPool, QTimer, QUrl, Signal
from PySide6.QtGui import QBrush, QColor, QDesktopServices, QIcon, QImage, QPainter, QPixmap
from PySide6.QtWidgets import (
    QAbstractItemView, QApplication, QCheckBox, QComboBox, QDialog, QDoubleSpinBox, QFileDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit, QListView, QListWidget, QListWidgetItem, QMainWindow,
    QMessageBox, QPlainTextEdit, QProgressBar, QPushButton, QRadioButton, QSlider, QSpinBox, QSplitter,
    QTabWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget,
)

import skinforge_core as core

ACCENT = "#ff6a1a"
PREVIEW_QUALITY = "Preview (540p | 4 Samples)"

QSS = """
* { font-family: "Segoe UI"; font-size: 13px; color: #ececf1; }
QMainWindow, QDialog, QWidget#root { background: #0e0e11; }
QWidget { background: transparent; }
QFrame#header, QFrame#bottombar { background: #141418; border: none; }
QFrame#header { border-bottom: 1px solid #25252c; }
QFrame#bottombar { border-top: 1px solid #25252c; }
QFrame#card { background: #16161a; border: 1px solid #25252c; border-radius: 10px; }
QLabel#title { font-size: 16px; font-weight: 700; }
QLabel#badge { background: #26262d; color: #a1a1ab; border-radius: 8px; padding: 2px 8px; font-size: 11px; }
QLabel#muted, QLabel[muted="true"] { color: #8b8b96; font-size: 12px; }
QLabel#section { color: #a1a1ab; font-size: 11px; font-weight: 700; letter-spacing: 1px; }
QLabel#chipok { color: #34d399; } QLabel#chipbad { color: #f87171; }
QTabWidget::pane { border: none; border-top: 1px solid #25252c; background: #121216; }
QTabBar { background: #0e0e11; }
QTabBar::tab { background: transparent; color: #8b8b96; padding: 9px 11px; border-bottom: 2px solid transparent; font-weight: 600; }
QTabBar::tab:hover { color: #ececf1; }
QTabBar::tab:selected { color: #ececf1; border-bottom: 2px solid #ff6a1a; }
QPushButton { background: #202026; border: 1px solid #2e2e36; border-radius: 7px; padding: 6px 12px; }
QPushButton:hover { background: #2a2a32; border-color: #3a3a44; }
QPushButton:pressed { background: #18181d; }
QPushButton:disabled { color: #5a5a64; background: #17171b; border-color: #222228; }
QPushButton:checked { background: #3a2415; border-color: #ff6a1a; color: #ffb27d; }
QPushButton[kind="primary"] { background: #ff6a1a; border: 1px solid #ff8340; color: #1a0d04; font-weight: 700; }
QPushButton[kind="primary"]:hover { background: #ff8340; }
QPushButton[kind="primary"]:disabled { background: #3a2a20; color: #7a6454; border-color: #3a2a20; }
QPushButton[kind="seg"] { border-radius: 0; padding: 6px 14px; }
QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox { background: #1b1b20; border: 1px solid #2e2e36; border-radius: 7px; padding: 5px 8px; selection-background-color: #ff6a1a; }
QComboBox:hover, QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus { border-color: #ff6a1a; }
QComboBox QAbstractItemView { background: #1b1b20; border: 1px solid #2e2e36; selection-background-color: #3a2415; outline: 0; }
QComboBox::drop-down { border: none; width: 22px; }
QSpinBox::up-button, QSpinBox::down-button, QDoubleSpinBox::up-button, QDoubleSpinBox::down-button { width: 0; }
QSlider::groove:horizontal { height: 4px; background: #2a2a32; border-radius: 2px; }
QSlider::sub-page:horizontal { background: #ff6a1a; border-radius: 2px; }
QSlider::handle:horizontal { background: #ececf1; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }
QSlider::handle:horizontal:hover { background: #ffffff; border: 2px solid #ff6a1a; }
QProgressBar { background: #1b1b20; border: none; border-radius: 4px; height: 8px; text-align: center; color: transparent; }
QProgressBar::chunk { background: #ff6a1a; border-radius: 4px; }
QCheckBox, QRadioButton { spacing: 8px; }
QCheckBox::indicator, QTreeView::indicator { width: 16px; height: 16px; border-radius: 4px; border: 1px solid #3a3a44; background: #1b1b20; }
QCheckBox::indicator:checked, QTreeView::indicator:checked { background: #ff6a1a; border-color: #ff6a1a; image: none; }
QTreeView::indicator:indeterminate { background: #7a3a14; border-color: #ff6a1a; }
QRadioButton::indicator { width: 14px; height: 14px; border-radius: 8px; border: 1px solid #3a3a44; background: #1b1b20; }
QRadioButton::indicator:checked { background: #ff6a1a; border-color: #ff6a1a; }
QListWidget, QTreeWidget, QPlainTextEdit { background: #121216; border: 1px solid #25252c; border-radius: 8px; outline: 0; }
QListWidget::item { border: 2px solid transparent; border-radius: 8px; padding: 4px; color: #a1a1ab; }
QListWidget::item:hover { background: #1c1c22; }
QListWidget::item:selected { background: #2b1b10; border: 2px solid #ff6a1a; color: #ececf1; }
QTreeWidget::item { padding: 4px 2px; }
QTreeWidget::item:selected { background: #2b1b10; }
QTreeWidget::item:hover { background: #1c1c22; }
QScrollBar:vertical { background: transparent; width: 10px; margin: 2px; }
QScrollBar::handle:vertical { background: #34343c; border-radius: 4px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #4a4a54; }
QScrollBar::add-line, QScrollBar::sub-line { height: 0; width: 0; }
QScrollBar:horizontal { height: 0; }
QSplitter::handle { background: #0e0e11; width: 6px; }
QToolTip { background: #1b1b20; color: #ececf1; border: 1px solid #3a3a44; padding: 4px; }
"""


def pil_to_qimage(img):
    img = img.convert("RGBA")
    w, h = img.size
    return QImage(img.tobytes("raw", "RGBA"), w, h, w * 4, QImage.Format.Format_RGBA8888).copy()


def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


class Bridge(QObject):
    """Signals emitted from worker threads and delivered on the UI thread."""
    image_loaded = Signal(str, str, QImage, int, int)   # tag, path, image, orig_w, orig_h
    preview_done = Signal(object)
    preview_error = Signal(str)
    job_progress = Signal(int, int, str)
    job_log = Signal(str)
    job_done = Signal(int, int, bool)


class _ImageLoad(QRunnable):
    def __init__(self, bridge, tag, path, max_side):
        super().__init__()
        self.bridge, self.tag, self.path, self.max_side = bridge, tag, path, max_side

    def run(self):
        try:
            Image.MAX_IMAGE_PIXELS = None
            with Image.open(self.path) as im:
                ow, oh = im.size
                im.draft("RGB", (self.max_side * 2, self.max_side * 2))
                im = im.convert("RGBA")
                im.thumbnail((self.max_side, self.max_side), Image.Resampling.LANCZOS)
            self.bridge.image_loaded.emit(self.tag, self.path, pil_to_qimage(im), ow, oh)
        except Exception:
            pass


class Viewport(QWidget):
    """Zoom/pan image viewer with checkerboard or solid background behind the image."""

    zoom_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.setMinimumSize(420, 300)
        self.setMouseTracking(True)
        self._img = None
        self._bg = None
        self._message = ""
        self._fit = True
        self._zoom = 1.0
        self._off = QPointF(0, 0)
        self._drag = None
        tile = QPixmap(24, 24)
        tile.fill(QColor("#2a2a30"))
        p = QPainter(tile)
        p.fillRect(0, 0, 12, 12, QColor("#34343c"))
        p.fillRect(12, 12, 12, 12, QColor("#34343c"))
        p.end()
        self._checker = QBrush(tile)

    def set_image(self, img):
        self._img = img
        self.update()
        self._emit_zoom()

    def set_background(self, color):
        self._bg = color
        self.update()

    def set_message(self, text):
        self._message = text
        self.update()

    def fit(self):
        self._fit = True
        self._off = QPointF(0, 0)
        self.update()
        self._emit_zoom()

    def zoom_100(self):
        self._fit, self._zoom, self._off = False, 1.0, QPointF(0, 0)
        self.update()
        self._emit_zoom()

    def _fit_scale(self):
        if self._img is None:
            return 1.0
        return max(0.01, min((self.width() - 24) / self._img.width(), (self.height() - 24) / self._img.height()))

    def _scale(self):
        return self._fit_scale() if self._fit else self._zoom

    def _rect(self):
        s = self._scale()
        w, h = self._img.width() * s, self._img.height() * s
        c = QPointF(self.width() / 2, self.height() / 2) + self._off
        return QRectF(c.x() - w / 2, c.y() - h / 2, w, h)

    def _emit_zoom(self):
        self.zoom_changed.emit("Fit" if self._fit else f"{self._zoom * 100:.0f}%")

    def paintEvent(self, _e):
        p = QPainter(self)
        p.fillRect(self.rect(), QColor("#0b0b0e"))
        if self._img is None:
            p.setPen(QColor("#6b6b76"))
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, self._message)
            return
        r = self._rect()
        if self._bg is None:
            p.fillRect(r, self._checker)
        else:
            p.fillRect(r, self._bg)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        p.drawImage(r, self._img)
        if self._message:
            p.setPen(QColor("#ffb27d"))
            p.drawText(self.rect().adjusted(12, 8, -12, -8), Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight, self._message)

    def wheelEvent(self, e):
        if self._img is None:
            return
        old = self._scale()
        new = max(0.05, min(16.0, old * (1.15 if e.angleDelta().y() > 0 else 1 / 1.15)))
        center = QPointF(self.width() / 2, self.height() / 2)
        cursor = e.position() - center - self._off      # cursor in image-space pixels * old scale
        self._off = self._off - cursor * (new / old - 1.0)
        self._fit, self._zoom = False, new
        self.update()
        self._emit_zoom()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag = e.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseMoveEvent(self, e):
        if self._drag is not None and self._img is not None:
            self._off += e.position() - self._drag
            self._drag = e.position()
            self.update()

    def mouseReleaseEvent(self, _e):
        self._drag = None
        self.unsetCursor()

    def mouseDoubleClickEvent(self, _e):
        self.fit()


class SliderField(QWidget):
    """Label + slider + exact numeric entry + reset, so designers can drag or type values."""
    changed = Signal(float)
    released = Signal()

    def __init__(self, title, lo, hi, step, default, suffix=""):
        super().__init__()
        self._step, self._default = step, default
        lay = QGridLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setHorizontalSpacing(8)
        self.label = QLabel(title)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(round(lo / step), round(hi / step))
        self.spin = QDoubleSpinBox()
        self.spin.setRange(lo, hi)
        self.spin.setSingleStep(step)
        self.spin.setDecimals(2)
        self.spin.setSuffix(suffix)
        self.spin.setFixedWidth(78)
        self.reset = QPushButton("Reset")
        self.reset.setFixedWidth(56)
        self.reset.setToolTip("Reset to default")
        lay.addWidget(self.label, 0, 0, 1, 3)
        lay.addWidget(self.slider, 1, 0)
        lay.addWidget(self.spin, 1, 1)
        lay.addWidget(self.reset, 1, 2)
        lay.setColumnStretch(0, 1)
        self.slider.valueChanged.connect(self._from_slider)
        self.spin.valueChanged.connect(self._from_spin)
        self.slider.sliderReleased.connect(self.released)
        self.reset.clicked.connect(lambda: self.setValue(default))
        self.setValue(default, emit=False)

    def value(self):
        return self.spin.value()

    def setValue(self, v, emit=True):
        self.spin.setValue(v)  # triggers _from_spin
        if not emit:
            return

    def _from_slider(self, i):
        v = round(i * self._step, 4)
        if abs(self.spin.value() - v) > 1e-9:
            self.spin.setValue(v)

    def _from_spin(self, v):
        self.slider.blockSignals(True)
        self.slider.setValue(round(v / self._step))
        self.slider.blockSignals(False)
        self.changed.emit(v)


class ResizeDialog(QDialog):
    """Create a resized copy of a texture (never overwrites the original)."""

    def __init__(self, parent, path):
        super().__init__(parent)
        self.setWindowTitle("Resize texture")
        self.path, self.result_path = path, None
        with Image.open(path) as im:
            self.ow, self.oh = im.size
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel(f"{os.path.basename(path)}  ·  {self.ow}×{self.oh}"))
        row = QHBoxLayout()
        self.w = QSpinBox(); self.w.setRange(16, 16384); self.w.setValue(self.ow)
        self.h = QSpinBox(); self.h.setRange(16, 16384); self.h.setValue(self.oh)
        self.lock = QCheckBox("Keep aspect"); self.lock.setChecked(True)
        row.addWidget(self.w); row.addWidget(QLabel("×")); row.addWidget(self.h); row.addWidget(self.lock)
        lay.addLayout(row)
        presets = QHBoxLayout()
        for px in (4096, 2048, 1024, 512):
            b = QPushButton(f"{px}px wide")
            b.clicked.connect(lambda _=False, px=px: self.w.setValue(px))
            presets.addWidget(b)
        lay.addLayout(presets)
        lay.addWidget(QLabel("Saved as a new file next to the original; the original is not changed."))
        ok = QPushButton("Create resized copy"); ok.setProperty("kind", "primary")
        ok.clicked.connect(self._save)
        lay.addWidget(ok)
        self._busy = False
        self.w.valueChanged.connect(lambda v: self._sync(True, v))
        self.h.valueChanged.connect(lambda v: self._sync(False, v))

    def _sync(self, from_w, v):
        if self._busy or not self.lock.isChecked():
            return
        self._busy = True
        if from_w:
            self.h.setValue(max(16, round(v * self.oh / self.ow)))
        else:
            self.w.setValue(max(16, round(v * self.ow / self.oh)))
        self._busy = False

    def _save(self):
        base, ext = os.path.splitext(self.path)
        out = f"{base}_{self.w.value()}x{self.h.value()}{ext}"
        with Image.open(self.path) as im:
            im = im.resize((self.w.value(), self.h.value()), Image.Resampling.LANCZOS)
            if ext.lower() in (".jpg", ".jpeg"):
                im = im.convert("RGB")
                im.save(out, quality=95)
            else:
                im.save(out)
        self.result_path = out
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Antigravity CS2 Skin Forge v{core.APP_VERSION}")
        self.setWindowIcon(QIcon(core.icon_path))
        self.resize(1480, 880)
        self.setMinimumSize(1100, 680)
        self.setAcceptDrops(True)

        self.bridge = Bridge()
        self.pool = QThreadPool.globalInstance()
        self.bridge.image_loaded.connect(self._on_image_loaded)
        self.bridge.preview_done.connect(self._on_preview_done)
        self.bridge.preview_error.connect(self._on_preview_error)
        self.bridge.job_progress.connect(self._on_job_progress)
        self.bridge.job_log.connect(self._log)
        self.bridge.job_done.connect(self._on_job_done)

        self.cfg = QSettings("Smokianlord", "CS2SkinForge")
        self.in_dir = self.cfg.value("in_dir", core.default_input_folder)
        self.out_dir = self.cfg.value("out_dir", core.default_out_folder)
        self.blend_dir = self.cfg.value("blend_dir", core.default_blend_folder)
        saved_blender = self.cfg.value("blender", "")
        self.blender_exe = saved_blender if saved_blender and os.path.exists(saved_blender) else core.find_blender()
        for d in (self.in_dir, self.out_dir, self.blend_dir):
            os.makedirs(d, exist_ok=True)

        self.weapons = core.scan_weapons()
        self.raw_render = None
        self._texture_image = None
        self._preview_running = False
        self._preview_pending = False
        self._running_jobs = False
        self._cancel = threading.Event()
        self._tex_paths = {}

        self._preview_timer = QTimer(self, singleShot=True)
        self._preview_timer.timeout.connect(self._start_preview)
        self._view_timer = QTimer(self, singleShot=True)
        self._view_timer.timeout.connect(self._refresh_view)

        root = QWidget(); root.setObjectName("root")
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(self._build_header())

        split = QSplitter(Qt.Orientation.Horizontal)
        split.setChildrenCollapsible(False)
        self.tabs = QTabWidget()
        self.tabs.setMinimumWidth(400)
        self.tabs.setDocumentMode(True)
        self.tabs.addTab(self._build_textures_tab(), "Textures")
        self.tabs.addTab(self._build_weapons_tab(), "Weapons")
        self.tabs.addTab(self._build_placement_tab(), "Placement")
        self.tabs.addTab(self._build_color_tab(), "Color")
        self.tabs.addTab(self._build_render_tab(), "Render")
        self.tabs.addTab(self._build_output_tab(), "Output")
        split.addWidget(self.tabs)
        split.addWidget(self._build_viewer())
        split.setStretchFactor(0, 0)
        split.setStretchFactor(1, 1)
        split.setSizes([440, 1040])
        outer.addWidget(split, 1)
        outer.addWidget(self._build_bottom())

        self._load_settings()
        self._wire_triggers()
        self.refresh_textures()
        self._update_blender_chip()
        self._update_summary()
        self.viewport.set_message("Pick a texture and a weapon to see a live 3D preview")
        QTimer.singleShot(150, self.request_preview)

    # ------------------------------------------------------------------ UI builders
    def _build_header(self):
        f = QFrame(); f.setObjectName("header"); f.setFixedHeight(54)
        lay = QHBoxLayout(f); lay.setContentsMargins(16, 6, 16, 6); lay.setSpacing(10)
        logo = QLabel(); logo.setPixmap(QIcon(core.icon_path).pixmap(34, 34))
        title = QLabel("CS2 Skin Forge"); title.setObjectName("title")
        badge = QLabel(f"v{core.APP_VERSION}"); badge.setObjectName("badge")
        lay.addWidget(logo); lay.addWidget(title); lay.addWidget(badge); lay.addStretch(1)
        self.blender_chip = QLabel()
        lay.addWidget(self.blender_chip)
        return f

    def _card(self):
        c = QFrame(); c.setObjectName("card")
        lay = QVBoxLayout(c); lay.setContentsMargins(14, 12, 14, 14); lay.setSpacing(10)
        return c, lay

    def _page(self):
        w = QWidget()
        lay = QVBoxLayout(w); lay.setContentsMargins(14, 14, 14, 14); lay.setSpacing(12)
        return w, lay

    @staticmethod
    def _section(text):
        l = QLabel(text.upper()); l.setObjectName("section")
        return l

    def _build_textures_tab(self):
        page, lay = self._page()
        row = QHBoxLayout(); row.setSpacing(6)
        self.btn_add = QPushButton("＋ Add images…"); self.btn_add.setProperty("kind", "primary")
        self.btn_add.clicked.connect(self.add_textures_dialog)
        btn_all = QPushButton("All"); btn_all.clicked.connect(lambda: self.tex_list.selectAll())
        btn_none = QPushButton("None"); btn_none.clicked.connect(lambda: self.tex_list.clearSelection())
        btn_resize = QPushButton("Resize…"); btn_resize.clicked.connect(self.open_resizer)
        btn_folder = QPushButton("Folder"); btn_folder.clicked.connect(lambda: self._open(self.in_dir))
        for b in (self.btn_add, btn_all, btn_none, btn_resize, btn_folder):
            row.addWidget(b)
        lay.addLayout(row)
        hint = QLabel("Click thumbnails to include them in the batch. The last one you click is previewed live. "
                      "You can also drag image files onto this window.")
        hint.setProperty("muted", True); hint.setWordWrap(True)
        lay.addWidget(hint)

        self.tex_list = QListWidget()
        self.tex_list.setViewMode(QListView.ViewMode.IconMode)
        self.tex_list.setResizeMode(QListView.ResizeMode.Adjust)
        self.tex_list.setMovement(QListView.Movement.Static)
        self.tex_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.tex_list.setIconSize(QSize(160, 90))
        self.tex_list.setGridSize(QSize(176, 128))
        self.tex_list.setUniformItemSizes(True)
        self.tex_list.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        self.tex_list.setSpacing(2)
        lay.addWidget(self.tex_list, 1)

        card, cl = self._card()
        self.tex_detail = QLabel("No texture selected")
        self.tex_detail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tex_detail.setMinimumHeight(170)
        self.tex_detail.setStyleSheet("background:#0b0b0e; border-radius:8px;")
        self.tex_info = QLabel(""); self.tex_info.setProperty("muted", True)
        cl.addWidget(self.tex_detail); cl.addWidget(self.tex_info)
        lay.addWidget(card)
        return page

    def _build_weapons_tab(self):
        page, lay = self._page()
        self.weapon_search = QLineEdit(); self.weapon_search.setPlaceholderText("Search weapons…")
        self.weapon_search.setClearButtonEnabled(True)
        lay.addWidget(self.weapon_search)
        row = QHBoxLayout(); row.setSpacing(6)
        for text, fn in (("Select all", self.weapons_all), ("Clear", self.weapons_none), ("Random 3", self.weapons_random)):
            b = QPushButton(text); b.clicked.connect(fn); row.addWidget(b)
        lay.addLayout(row)
        self.weapon_tree = QTreeWidget(); self.weapon_tree.setHeaderHidden(True)
        self.weapon_tree.setIndentation(14)
        self._weapon_items = {}
        cats = {}
        for w in self.weapons:
            top = cats.get(w["category"])
            if top is None:
                top = QTreeWidgetItem(self.weapon_tree, [w["category"]])
                top.setFlags(top.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsAutoTristate)
                top.setExpanded(True)
                cats[w["category"]] = top
            it = QTreeWidgetItem(top, [w["name"]])
            it.setFlags(it.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            it.setCheckState(0, Qt.CheckState.Unchecked)
            it.setData(0, Qt.ItemDataRole.UserRole, w["id"])
            self._weapon_items[w["id"]] = it
        lay.addWidget(self.weapon_tree, 1)
        self.weapon_note = QLabel("Check weapons to render. The highlighted one is shown in the live preview.")
        self.weapon_note.setProperty("muted", True); self.weapon_note.setWordWrap(True)
        lay.addWidget(self.weapon_note)
        self.weapon_search.textChanged.connect(self._filter_weapons)
        return page

    def _build_placement_tab(self):
        page, lay = self._page()
        card, cl = self._card()
        cl.addWidget(self._section("Texture placement"))
        self.f_x = SliderField("Horizontal offset", -1.0, 1.0, 0.01, 0.0)
        self.f_y = SliderField("Vertical offset", -1.0, 1.0, 0.01, 0.0)
        self.f_scale = SliderField("Scale", 0.1, 5.0, 0.05, 1.0, "×")
        for f in (self.f_x, self.f_y, self.f_scale):
            cl.addWidget(f)
        flips = QHBoxLayout()
        self.btn_flip_x = QPushButton("⇄  Flip X"); self.btn_flip_x.setCheckable(True)
        self.btn_flip_y = QPushButton("⇅  Flip Y"); self.btn_flip_y.setCheckable(True)
        flips.addWidget(self.btn_flip_x); flips.addWidget(self.btn_flip_y)
        cl.addLayout(flips)
        reset = QPushButton("Reset placement"); reset.clicked.connect(self.reset_placement)
        cl.addWidget(reset)
        lay.addWidget(card)
        tip = QLabel("Tip: click a slider and use the arrow keys for fine nudges; the preview updates as you go. "
                     "Double-click the preview to fit it, scroll to zoom, drag to pan.")
        tip.setProperty("muted", True); tip.setWordWrap(True)
        lay.addWidget(tip); lay.addStretch(1)
        return page

    def _build_color_tab(self):
        page, lay = self._page()
        card, cl = self._card()
        cl.addWidget(self._section("Color grading (applied instantly)"))
        self.f_bright = SliderField("Brightness", 0.2, 2.0, 0.01, 1.0)
        self.f_cont = SliderField("Contrast", 0.2, 2.0, 0.01, 1.0)
        self.f_sat = SliderField("Saturation", 0.0, 2.0, 0.01, 1.0)
        for f in (self.f_bright, self.f_cont, self.f_sat):
            cl.addWidget(f)
        reset = QPushButton("Reset color"); reset.clicked.connect(self.reset_color)
        cl.addWidget(reset)
        lay.addWidget(card)
        note = QLabel("Color grading is applied to the final exports exactly as shown in the preview.")
        note.setProperty("muted", True); note.setWordWrap(True)
        lay.addWidget(note); lay.addStretch(1)
        return page

    def _build_render_tab(self):
        page, lay = self._page()
        card, cl = self._card()
        cl.addWidget(self._section("Look"))
        self.cb_lighting = self._combo(cl, "Lighting rig", core.LIGHTING_RIGS)
        cl.addWidget(self._section("Quality"))
        self.cb_quality = self._combo(cl, "Export quality", core.QUALITY_PRESETS)
        self.cb_engine = self._combo(cl, "Engine", core.ENGINES)
        self.cb_compute = self._combo(cl, "Compute device", core.COMPUTE_MODES)
        self.cb_fmt = self._combo(cl, "Format", ["PNG", "JPEG"])
        self.chk_blend = QCheckBox("Also save a .blend project for each render"); self.chk_blend.setChecked(True)
        cl.addWidget(self.chk_blend)
        cl.addWidget(self._section("Batch mode"))
        self.rb_all = QRadioButton("All combinations (every weapon × every texture)"); self.rb_all.setChecked(True)
        self.rb_random = QRadioButton("Random match (one random texture per weapon)")
        cl.addWidget(self.rb_all); cl.addWidget(self.rb_random)
        lay.addWidget(card); lay.addStretch(1)
        return page

    def _combo(self, layout, title, items):
        lab = QLabel(title); lab.setProperty("muted", True)
        cb = QComboBox(); cb.addItems(items)
        layout.addWidget(lab); layout.addWidget(cb)
        return cb

    def _build_output_tab(self):
        page, lay = self._page()
        card, cl = self._card()
        cl.addWidget(self._section("Folders & tools"))
        self.ed_in = self._path_row(cl, "Input textures", lambda: self.in_dir, self._set_in_dir)
        self.ed_out = self._path_row(cl, "Renders", lambda: self.out_dir, lambda p: self._set_dir("out_dir", p))
        self.ed_blend = self._path_row(cl, "Blender projects", lambda: self.blend_dir, lambda p: self._set_dir("blend_dir", p))
        lab = QLabel("Blender executable"); lab.setProperty("muted", True)
        cl.addWidget(lab)
        row = QHBoxLayout()
        self.ed_blender = QLineEdit(self.blender_exe); self.ed_blender.setReadOnly(True)
        bb = QPushButton("Browse…"); bb.clicked.connect(self.browse_blender)
        row.addWidget(self.ed_blender, 1); row.addWidget(bb)
        cl.addLayout(row)
        lay.addWidget(card)
        lay.addWidget(self._section("Activity"))
        self.log_view = QPlainTextEdit(); self.log_view.setReadOnly(True); self.log_view.setMaximumBlockCount(500)
        lay.addWidget(self.log_view, 1)
        return page

    def _path_row(self, layout, title, getter, setter):
        lab = QLabel(title); lab.setProperty("muted", True)
        layout.addWidget(lab)
        row = QHBoxLayout()
        ed = QLineEdit(getter()); ed.setReadOnly(True)
        browse = QPushButton("Browse…")
        opn = QPushButton("Open")

        def pick():
            p = QFileDialog.getExistingDirectory(self, title, getter())
            if p:
                setter(p)
                ed.setText(p)
        browse.clicked.connect(pick)
        opn.clicked.connect(lambda: self._open(getter()))
        row.addWidget(ed, 1); row.addWidget(browse); row.addWidget(opn)
        layout.addLayout(row)
        return ed

    def _build_viewer(self):
        w = QWidget()
        lay = QVBoxLayout(w); lay.setContentsMargins(0, 10, 14, 10); lay.setSpacing(8)
        bar = QHBoxLayout(); bar.setSpacing(0)
        self.btn_mode_render = QPushButton("3D Render"); self.btn_mode_tex = QPushButton("Source texture")
        for b in (self.btn_mode_render, self.btn_mode_tex):
            b.setCheckable(True); b.setProperty("kind", "seg"); bar.addWidget(b)
        self.btn_mode_render.setChecked(True)
        self.btn_mode_render.clicked.connect(lambda: self._set_mode("render"))
        self.btn_mode_tex.clicked.connect(lambda: self._set_mode("texture"))
        bar.addSpacing(14)
        self.cb_bg = QComboBox(); self.cb_bg.addItems(list(core.BACKGROUNDS))
        self.chk_transparent = QCheckBox("Transparent")
        bar.addWidget(QLabel("Background")); bar.addSpacing(6); bar.addWidget(self.cb_bg)
        bar.addSpacing(10); bar.addWidget(self.chk_transparent)
        bar.addStretch(1)
        self.lbl_state = QLabel("● Idle"); self.lbl_state.setProperty("muted", True)
        self.lbl_zoom = QLabel("Fit"); self.lbl_zoom.setProperty("muted", True)
        btn_fit = QPushButton("Fit"); btn_fit.clicked.connect(lambda: self.viewport.fit())
        btn_100 = QPushButton("100%"); btn_100.clicked.connect(lambda: self.viewport.zoom_100())
        btn_refresh = QPushButton("↻ Update"); btn_refresh.clicked.connect(lambda: self.request_preview(0))
        for x in (self.lbl_state, self.lbl_zoom, btn_fit, btn_100, btn_refresh):
            bar.addSpacing(6); bar.addWidget(x)
        lay.addLayout(bar)
        self.viewport = Viewport()
        self.viewport.zoom_changed.connect(self.lbl_zoom.setText)
        lay.addWidget(self.viewport, 1)
        self.view_info = QLabel(""); self.view_info.setProperty("muted", True)
        lay.addWidget(self.view_info)
        return w

    def _build_bottom(self):
        f = QFrame(); f.setObjectName("bottombar"); f.setFixedHeight(66)
        lay = QHBoxLayout(f); lay.setContentsMargins(16, 10, 16, 10); lay.setSpacing(14)
        col = QVBoxLayout(); col.setSpacing(4)
        self.lbl_summary = QLabel(""); self.lbl_status = QLabel("Ready"); self.lbl_status.setProperty("muted", True)
        col.addWidget(self.lbl_summary); col.addWidget(self.lbl_status)
        lay.addLayout(col, 1)
        self.progress = QProgressBar(); self.progress.setFixedWidth(260); self.progress.setTextVisible(False)
        lay.addWidget(self.progress)
        self.btn_cancel = QPushButton("Cancel"); self.btn_cancel.setVisible(False)
        self.btn_cancel.clicked.connect(self._cancel.set)
        self.btn_generate = QPushButton("Generate skins && renders"); self.btn_generate.setProperty("kind", "primary")
        self.btn_generate.setMinimumHeight(42); self.btn_generate.setMinimumWidth(230)
        self.btn_generate.clicked.connect(self.start_generation)
        lay.addWidget(self.btn_cancel); lay.addWidget(self.btn_generate)
        return f

    # ------------------------------------------------------------------ wiring / settings
    def _wire_triggers(self):
        for f in (self.f_x, self.f_y, self.f_scale):
            f.changed.connect(lambda _v: self.request_preview(260))
            f.released.connect(lambda: self.request_preview(0))
        for f in (self.f_bright, self.f_cont, self.f_sat):
            f.changed.connect(lambda _v: self._schedule_view())
        for b in (self.btn_flip_x, self.btn_flip_y):
            b.toggled.connect(lambda _c: self.request_preview(0))
        for cb in (self.cb_lighting, self.cb_engine, self.cb_compute):
            cb.currentIndexChanged.connect(lambda _i: self.request_preview(0))
        self.cb_bg.currentIndexChanged.connect(lambda _i: self._schedule_view())
        self.chk_transparent.toggled.connect(lambda _c: self._schedule_view())
        self.tex_list.itemSelectionChanged.connect(self._update_summary)
        self.tex_list.currentItemChanged.connect(self._on_texture_current)
        self.weapon_tree.currentItemChanged.connect(lambda *_: self._on_weapon_current())
        self.weapon_tree.itemChanged.connect(lambda *_: self._update_summary())
        self.rb_all.toggled.connect(lambda _c: self._update_summary())

    def _load_settings(self):
        def combo(cb, key):
            i = cb.findText(self.cfg.value(key, ""))
            if i >= 0:
                cb.setCurrentIndex(i)
        for cb, key in ((self.cb_lighting, "lighting"), (self.cb_quality, "quality"), (self.cb_engine, "engine"),
                        (self.cb_compute, "compute"), (self.cb_fmt, "fmt"), (self.cb_bg, "bg")):
            combo(cb, key)
        if not self.cfg.value("quality", ""):
            self.cb_quality.setCurrentIndex(core.QUALITY_PRESETS.index("Standard (1080p | 32 Samples)"))
        self.chk_blend.setChecked(self.cfg.value("save_blend", True, type=bool))
        self.chk_transparent.setChecked(self.cfg.value("transparent", False, type=bool))
        self.rb_random.setChecked(self.cfg.value("mode", "all") == "random")

    def closeEvent(self, e):
        self._cancel.set()
        for key, val in (("in_dir", self.in_dir), ("out_dir", self.out_dir), ("blend_dir", self.blend_dir),
                         ("blender", self.blender_exe), ("lighting", self.cb_lighting.currentText()),
                         ("quality", self.cb_quality.currentText()), ("engine", self.cb_engine.currentText()),
                         ("compute", self.cb_compute.currentText()), ("fmt", self.cb_fmt.currentText()),
                         ("bg", self.cb_bg.currentText()), ("save_blend", self.chk_blend.isChecked()),
                         ("transparent", self.chk_transparent.isChecked()),
                         ("mode", "random" if self.rb_random.isChecked() else "all")):
            self.cfg.setValue(key, val)
        super().closeEvent(e)

    def showEvent(self, e):
        super().showEvent(e)
        if sys.platform == "win32" and not getattr(self, "_titlebar_done", False):
            self._titlebar_done = True
            try:
                import ctypes
                v = ctypes.c_int(1)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(int(self.winId()), 20, ctypes.byref(v), 4)
            except Exception:
                pass

    # ------------------------------------------------------------------ helpers
    def _open(self, path):
        if os.path.isdir(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def _log(self, msg):
        self.log_view.appendPlainText(msg)
        self.lbl_status.setText(msg)

    def _update_blender_chip(self):
        ok = os.path.exists(self.blender_exe)
        self.blender_chip.setText("● Blender ready" if ok else "● Blender not found - set it in Output")
        self.blender_chip.setObjectName("chipok" if ok else "chipbad")
        self.blender_chip.style().unpolish(self.blender_chip); self.blender_chip.style().polish(self.blender_chip)
        self.ed_blender.setText(self.blender_exe)

    def browse_blender(self):
        p, _ = QFileDialog.getOpenFileName(self, "Select blender.exe", os.path.dirname(self.blender_exe), "Blender (blender.exe);;All files (*.*)")
        if p:
            self.blender_exe = p
            self._update_blender_chip()
            self.request_preview(0)

    def _set_dir(self, attr, path):
        setattr(self, attr, path)
        os.makedirs(path, exist_ok=True)

    def _set_in_dir(self, path):
        self._set_dir("in_dir", path)
        self.refresh_textures()

    # ------------------------------------------------------------------ textures
    def refresh_textures(self, select=()):
        keep = {i.text() for i in self.tex_list.selectedItems()} | set(select)
        cur = self.tex_list.currentItem().text() if self.tex_list.currentItem() else None
        self.tex_list.blockSignals(True)
        self.tex_list.clear()
        self._tex_paths = {}
        placeholder = QPixmap(160, 90); placeholder.fill(QColor("#1b1b20"))
        for name in core.list_textures(self.in_dir):
            path = os.path.join(self.in_dir, name)
            self._tex_paths[name] = path
            it = QListWidgetItem(QIcon(placeholder), name)
            it.setToolTip(path)
            it.setData(Qt.ItemDataRole.UserRole, path)
            self.tex_list.addItem(it)
            it.setSelected(name in keep)
            self.pool.start(_ImageLoad(self.bridge, "grid", path, 320))
        self.tex_list.blockSignals(False)
        target = cur if cur in self._tex_paths else (next(iter(select), None) if select else None)
        if target is None and self.tex_list.count():
            target = self.tex_list.item(0).text()
        if target:
            for i in range(self.tex_list.count()):
                if self.tex_list.item(i).text() == target:
                    self.tex_list.setCurrentRow(i)
        else:
            self.tex_detail.setText(f"No images in\n{self.in_dir}\nUse “Add images…” or drop files here")
            self.tex_info.setText("")
        self._update_summary()

    def add_textures_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Add texture images", "", "Images (*.png *.jpg *.jpeg *.webp *.bmp *.tga)")
        if files:
            self.add_textures(files)

    def add_textures(self, files):
        added = []
        for src in files:
            if not src.lower().endswith(core.IMAGE_EXTS) or not os.path.isfile(src):
                continue
            name = os.path.basename(src)
            dest = os.path.join(self.in_dir, name)
            if os.path.abspath(src) != os.path.abspath(dest):
                stem, ext = os.path.splitext(name)
                n = 1
                while os.path.exists(dest):
                    dest = os.path.join(self.in_dir, f"{stem}_{n}{ext}")
                    n += 1
                shutil.copy2(src, dest)
            added.append(os.path.basename(dest))
        if added:
            self.tabs.setCurrentIndex(0)
            self.refresh_textures(select=added)
            for i in range(self.tex_list.count()):
                if self.tex_list.item(i).text() == added[-1]:
                    self.tex_list.setCurrentRow(i)
            self._log(f"Added {len(added)} texture(s): {', '.join(added)}")

    def open_resizer(self):
        it = self.tex_list.currentItem()
        if not it:
            self._log("ERROR: Select a texture to resize first.")
            return
        dlg = ResizeDialog(self, it.data(Qt.ItemDataRole.UserRole))
        if dlg.exec() and dlg.result_path:
            self.add_textures([dlg.result_path])

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        self.add_textures([u.toLocalFile() for u in e.mimeData().urls() if u.isLocalFile()])

    def _on_texture_current(self, cur, _prev):
        if cur is None:
            return
        path = cur.data(Qt.ItemDataRole.UserRole)
        self.tex_info.setText(os.path.basename(path))
        self.pool.start(_ImageLoad(self.bridge, "detail", path, 720))
        if self.btn_mode_tex.isChecked():
            self.pool.start(_ImageLoad(self.bridge, "viewport", path, 2048))
        self.request_preview(120)

    def _on_image_loaded(self, tag, path, img, ow, oh):
        if tag == "grid":
            for i in range(self.tex_list.count()):
                it = self.tex_list.item(i)
                if it.data(Qt.ItemDataRole.UserRole) == path:
                    it.setIcon(QIcon(QPixmap.fromImage(img)))
                    break
            return
        cur = self.current_texture_path()
        if path != cur:
            return
        if tag == "detail":
            pm = QPixmap.fromImage(img).scaled(self.tex_detail.width() - 4, 168, Qt.AspectRatioMode.KeepAspectRatio,
                                               Qt.TransformationMode.SmoothTransformation)
            self.tex_detail.setPixmap(pm)
            size = os.path.getsize(path) if os.path.exists(path) else 0
            self.tex_info.setText(f"{os.path.basename(path)}  ·  {ow}×{oh}  ·  {human_size(size)}")
            self.view_info.setText(self._view_info_text(ow, oh))
        elif tag == "viewport":
            self._texture_image = img
            if self.btn_mode_tex.isChecked():
                self.viewport.set_image(img)

    def current_texture_path(self):
        it = self.tex_list.currentItem()
        return it.data(Qt.ItemDataRole.UserRole) if it else None

    # ------------------------------------------------------------------ weapons
    def _weapon_by_id(self, wid):
        return next((w for w in self.weapons if w["id"] == wid), None)

    def checked_weapons(self):
        return [w for w in self.weapons if self._weapon_items[w["id"]].checkState(0) == Qt.CheckState.Checked]

    def current_weapon(self):
        it = self.weapon_tree.currentItem()
        if it is not None and it.data(0, Qt.ItemDataRole.UserRole):
            return self._weapon_by_id(it.data(0, Qt.ItemDataRole.UserRole))
        checked = self.checked_weapons()
        if checked:
            return checked[0]
        return self.weapons[0] if self.weapons else None

    def _on_weapon_current(self):
        self.request_preview(120)

    def _filter_weapons(self, text):
        text = text.strip().lower()
        for i in range(self.weapon_tree.topLevelItemCount()):
            top = self.weapon_tree.topLevelItem(i)
            visible = 0
            for j in range(top.childCount()):
                c = top.child(j)
                hide = bool(text) and text not in c.text(0).lower()
                c.setHidden(hide)
                visible += not hide
            top.setHidden(visible == 0)

    def _set_all_weapons(self, state):
        self.weapon_tree.blockSignals(True)
        for it in self._weapon_items.values():
            it.setCheckState(0, state)
        self.weapon_tree.blockSignals(False)
        for i in range(self.weapon_tree.topLevelItemCount()):
            self.weapon_tree.topLevelItem(i).setCheckState(0, state)
        self._update_summary()

    def weapons_all(self):
        self._set_all_weapons(Qt.CheckState.Checked)

    def weapons_none(self):
        self._set_all_weapons(Qt.CheckState.Unchecked)

    def weapons_random(self):
        self._set_all_weapons(Qt.CheckState.Unchecked)
        for w in random.sample(self.weapons, min(3, len(self.weapons))):
            self._weapon_items[w["id"]].setCheckState(0, Qt.CheckState.Checked)

    # ------------------------------------------------------------------ placement / color
    def reset_placement(self):
        for f in (self.f_x, self.f_y, self.f_scale):
            f.setValue(f._default)
        self.btn_flip_x.setChecked(False); self.btn_flip_y.setChecked(False)
        self.request_preview(0)

    def reset_color(self):
        for f in (self.f_bright, self.f_cont, self.f_sat):
            f.setValue(f._default)

    def collect_settings(self):
        s = core.RenderSettings()
        s.engine, s.compute = self.cb_engine.currentText(), self.cb_compute.currentText()
        s.quality, s.lighting = self.cb_quality.currentText(), self.cb_lighting.currentText()
        s.fmt = self.cb_fmt.currentText()
        s.transparent = self.chk_transparent.isChecked()
        s.save_blend = self.chk_blend.isChecked()
        s.offset_x, s.offset_y, s.scale = self.f_x.value(), self.f_y.value(), self.f_scale.value()
        s.flip_x, s.flip_y = self.btn_flip_x.isChecked(), self.btn_flip_y.isChecked()
        return s

    def _color(self):
        return self.f_bright.value(), self.f_cont.value(), self.f_sat.value()

    # ------------------------------------------------------------------ live preview
    def request_preview(self, delay=200):
        self._preview_timer.start(delay)

    def _start_preview(self):
        if self._preview_running:
            self._preview_pending = True
            return
        weapon, tex = self.current_weapon(), self.current_texture_path()
        if not weapon:
            self.viewport.set_message("No weapon models found in Assets/Models")
            return
        if not tex or not os.path.exists(tex):
            self.viewport.set_message("Add or select a texture to see the preview")
            return
        if not os.path.exists(self.blender_exe):
            self.viewport.set_message("Blender not found.\nSet blender.exe in the Output tab.")
            self.lbl_state.setText("● Blender missing")
            return
        s = self.collect_settings()
        self._preview_running = True
        self.lbl_state.setText("● Rendering…")
        threading.Thread(target=self._preview_worker, args=(weapon, tex, s, self.blender_exe), daemon=True).start()

    def _preview_worker(self, weapon, tex, s, blender):
        out = os.path.join(core.preview_cache_dir, "preview.png")
        try:
            os.makedirs(core.preview_cache_dir, exist_ok=True)
            cmd = core.build_command(blender, weapon, tex, out, "SKIP", PREVIEW_QUALITY, s, transparent=True, proxy=True)
            core.run_blender(cmd)
            with Image.open(out) as im:
                img = im.convert("RGBA")
            self.bridge.preview_done.emit((img, weapon["name"], os.path.basename(tex)))
        except Exception as e:
            self.bridge.preview_error.emit(str(e))

    def _finish_preview(self):
        self._preview_running = False
        if self._preview_pending:
            self._preview_pending = False
            self.request_preview(0)

    def _on_preview_done(self, payload):
        self.raw_render, self._render_label = payload[0], f"{payload[1]}  ·  {payload[2]}"
        self.lbl_state.setText("● Ready")
        self.viewport.set_message("")
        self._refresh_view()
        self._finish_preview()

    def _on_preview_error(self, err):
        self.lbl_state.setText("● Preview failed")
        self._log(f"ERROR: Preview failed - {err}")
        self._finish_preview()

    def _schedule_view(self):
        self._view_timer.start(16)

    def _refresh_view(self):
        if self.raw_render is None:
            return
        img = core.apply_color(self.raw_render, *self._color())
        bg = None if self.chk_transparent.isChecked() else QColor(*core.BACKGROUNDS[self.cb_bg.currentText()][:3])
        self.viewport.set_background(bg)
        if not self.btn_mode_tex.isChecked():
            self.viewport.set_image(pil_to_qimage(img))
            self.view_info.setText(getattr(self, "_render_label", ""))

    def _view_info_text(self, ow, oh):
        return f"Source texture {ow}×{oh}"

    def _set_mode(self, mode):
        self.btn_mode_render.setChecked(mode == "render")
        self.btn_mode_tex.setChecked(mode == "texture")
        if mode == "texture":
            path = self.current_texture_path()
            if self._texture_image is not None:
                self.viewport.set_image(self._texture_image)
            if path:
                self.pool.start(_ImageLoad(self.bridge, "viewport", path, 2048))
            self.viewport.set_background(QColor("#0b0b0e") if not self.chk_transparent.isChecked() else None)
        else:
            self._refresh_view()
            if self.raw_render is None:
                self.viewport.set_image(None)
        self.viewport.fit()

    # ------------------------------------------------------------------ batch generation
    def _jobs(self):
        weapons = self.checked_weapons()
        texs = [i.data(Qt.ItemDataRole.UserRole) for i in self.tex_list.selectedItems()]
        if self.rb_random.isChecked():
            return [(w, random.choice(texs)) for w in weapons] if texs else []
        return [(w, t) for w in weapons for t in texs]

    def _update_summary(self):
        nw, nt = len(self.checked_weapons()), len(self.tex_list.selectedItems())
        n = len(self._jobs())
        self.lbl_summary.setText(f"<b>{n}</b> render{'s' if n != 1 else ''} queued  ·  {nw} weapon{'s' if nw != 1 else ''} × {nt} texture{'s' if nt != 1 else ''}")

    def start_generation(self):
        if self._running_jobs:
            return
        if not os.path.exists(self.blender_exe):
            self._log("ERROR: Blender not found. Set blender.exe in the Output tab.")
            self.tabs.setCurrentIndex(5)
            return
        if not self.tex_list.selectedItems():
            self._log("ERROR: Select at least one texture (Textures tab).")
            self.tabs.setCurrentIndex(0)
            return
        if not self.checked_weapons():
            self._log("ERROR: Check at least one weapon (Weapons tab).")
            self.tabs.setCurrentIndex(1)
            return
        jobs = self._jobs()
        self._running_jobs = True
        self._cancel.clear()
        self.btn_generate.setEnabled(False); self.btn_cancel.setVisible(True)
        self.progress.setRange(0, len(jobs)); self.progress.setValue(0)
        s = self.collect_settings()
        bg = core.BACKGROUNDS[self.cb_bg.currentText()]
        args = (jobs, s, self._color(), bg, self.out_dir, self.blend_dir, self.blender_exe)
        self._log(f"Starting {len(jobs)} render(s) [{s.quality}] [{s.compute}]")
        threading.Thread(target=self._run_jobs, args=args, daemon=True).start()

    def _run_jobs(self, jobs, s, color, bg, out_dir, blend_dir, blender):
        ok = bad = 0
        ext = ".png" if s.fmt == "PNG" else ".jpg"
        for i, (w, tex) in enumerate(jobs):
            if self._cancel.is_set():
                break
            stem = "".join(c if c.isalnum() or c in "-_." else "_" for c in os.path.splitext(os.path.basename(tex))[0])
            self.bridge.job_progress.emit(i, len(jobs), f"[{i + 1}/{len(jobs)}] Rendering {w['name']} with {os.path.basename(tex)}…")
            out_img = os.path.join(out_dir, f"True3D_{w['id']}_{stem}_PlaySide{ext}")
            blend_out = os.path.join(blend_dir, f"True3D_{w['id']}_{stem}_Project.blend") if s.save_blend else "SKIP"
            try:
                core.run_blender(core.build_command(blender, w, tex, out_img, blend_out, s.quality, s, transparent=s.transparent and s.fmt == "PNG"))
                with Image.open(out_img) as im:
                    render = core.apply_color(im.convert("RGBA"), *color)
                if not s.transparent or s.fmt == "JPEG":
                    render = core.composite_on(render, bg)
                if s.fmt == "JPEG":
                    render.convert("RGB").save(out_img, quality=95)
                else:
                    render.save(out_img)
                ok += 1
                self.bridge.job_log.emit(f"SUCCESS: Exported {os.path.basename(out_img)}")
            except Exception as e:
                bad += 1
                self.bridge.job_log.emit(f"FAILED: {w['name']} - {e}")
            self.bridge.job_progress.emit(i + 1, len(jobs), "")
        self.bridge.job_done.emit(ok, bad, self._cancel.is_set())

    def _on_job_progress(self, done, total, msg):
        self.progress.setValue(done)
        if msg:
            self._log(msg)

    def _on_job_done(self, ok, bad, cancelled):
        self._running_jobs = False
        self.btn_generate.setEnabled(True); self.btn_cancel.setVisible(False)
        self._log(f"{'Cancelled' if cancelled else 'Finished'}: {ok} exported, {bad} failed.")
        if ok:
            box = QMessageBox(self)
            box.setWindowTitle("Renders complete")
            box.setText(f"{ok} render(s) exported" + (f", {bad} failed" if bad else "") + ".")
            open_btn = box.addButton("Open renders folder", QMessageBox.ButtonRole.AcceptRole)
            box.addButton("Close", QMessageBox.ButtonRole.RejectRole)
            box.exec()
            if box.clickedButton() is open_btn:
                self._open(self.out_dir)


def main():
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Smokianlord.CS2SkinForge")
        except Exception:
            pass
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(QSS)
    app.setWindowIcon(QIcon(core.icon_path))
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
