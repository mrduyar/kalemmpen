# =============================================================================
# Kalemm Pen Pro — Ekran Üzeri Çizim Aracı
# -----------------------------------------------------------------------------
# Geliştirici : Mehmet Ramazan DUYAR
# Konum       : Şarkikaraağaç, Isparta
# Sürüm       : 1.2.0
# Lisans      : Tüm hakları saklıdır © 2025
# Web         : www.mrduyar.com
# -----------------------------------------------------------------------------
# Açıklama    : Bu uygulama, masaüstü ekranı üzerine saydam bir çizim katmanı
#               serer. Kullanıcı kalem, ok, dikdörtgen, elips ve metin araçlarıyla
#               çizim yapabilir; renk & kalınlık seçebilir; çizimi PNG olarak
#               kaydedebilir. Aktif/Pasif mod ile çizim katmanı devre dışı
#               bırakılarak pencere tıklamaları alttaki masaüstüne iletilebilir.
# =============================================================================

import sys        # Uygulama çıkışı (sys.exit) için
import json       # Ayarları dosyaya kaydetmek/yüklemek için (JSON formatı)
import os         # Dosya/klasör işlemleri için
from datetime import datetime   # Kayıt dosyası adına tarih-saat damgası eklemek için

# --- PyQt6 UI Bileşenleri ---
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QColorDialog, QSlider, QLabel, QFrame,
                             QFileDialog, QLineEdit, QGridLayout, QDialog)
# Qt sabitleri, geometri sınıfları ve sinyaller
from PyQt6.QtCore import Qt, QPoint, QRect, QSize, pyqtSignal, QUrl
# Grafik / çizim / ikon araçları
from PyQt6.QtGui import (QPainter, QPen, QColor, QCursor, QIcon, QImage,
                         QPixmap, QAction, QKeySequence, QGuiApplication, QFont, QRegion,
                         QLinearGradient, QBrush, QDesktopServices)


class AboutDialog(QDialog):
    """Modern Kalemm Pen Pro Hakkında Penceresi"""
    VERSION = "1.2.0"
    YEAR = "2025"
    DEVELOPER = "Mehmet Ramazan DUYAR"
    CITY = "Şarkikaraağaç, Isparta"
    WEBSITE = "www.mrduyar.com"
    EMAIL = "info@mrduyar.com"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kalemm Pen Pro — Hakkında")
        self.setFixedSize(700, 420)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self._drag_pos = None
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                border: 2px solid #8B3A3A;
            }
        """)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── SOL KOLON: Kızıldağ görseli (50%) ──
        left_panel = QLabel()
        left_panel.setFixedWidth(350)
        left_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel.setStyleSheet("border: none;")

        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Kalemm_gorsel.png")
        if os.path.exists(img_path):
            pix = QPixmap(img_path).scaled(
                350, 420,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            ).copy(0, 0, 350, 420)
            left_panel.setPixmap(pix)
        else:
            left_panel.setStyleSheet("background-color: #2D5A27;")
            left_panel.setText("🌲\nKızıldağ")
        root.addWidget(left_panel)

        # İnce dikey çizgi
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.VLine)
        divider.setFixedWidth(2)
        divider.setStyleSheet("background-color: #8B3A3A; border: none;")
        root.addWidget(divider)

        # ── SAĞ KOLON: Bilgiler (50%) ──
        right = QWidget()
        right.setStyleSheet("background-color: #1e1e1e; border: none;")
        right_lyt = QVBoxLayout(right)
        right_lyt.setContentsMargins(28, 24, 28, 18)
        right_lyt.setSpacing(0)

        # Kapat (X) butonu — sağ üst köşe
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent; color: #888;
                font-size: 16px; font-weight: bold;
                border: none;
            }
            QPushButton:hover { color: #e74c3c; }
        """)
        close_btn.clicked.connect(self.close)
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(close_btn)
        right_lyt.addLayout(top_bar)

        # Logo + Başlık
        logo_row = QHBoxLayout()
        logo_row.setSpacing(14)
        logo_lbl = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Kalemm_gorsel_logo2.png")
        if os.path.exists(logo_path):
            pix_logo = QPixmap(logo_path).scaled(
                72, 72,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo_lbl.setPixmap(pix_logo)
        else:
            logo_lbl.setText("✒️")
            logo_lbl.setStyleSheet("font-size: 48px;")
        logo_row.addWidget(logo_lbl, 0, Qt.AlignmentFlag.AlignVCenter)

        title_block = QVBoxLayout()
        title_block.setSpacing(2)
        app_name = QLabel("Kalemm Pen Pro")
        app_name.setStyleSheet("""
            color: #F5F5F5;
            font-size: 22px;
            font-weight: bold;
            font-family: 'Segoe UI', sans-serif;
        """)
        platform_lbl = QLabel("64-bit  •  Windows 10 / 11")
        platform_lbl.setStyleSheet("color: #8B3A3A; font-size: 11px; font-family: 'Segoe UI';")
        title_block.addWidget(app_name)
        title_block.addWidget(platform_lbl)
        logo_row.addLayout(title_block)
        logo_row.addStretch()
        right_lyt.addLayout(logo_row)

        right_lyt.addSpacing(16)

        # Yatay ayırıcı çizgi
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #333; border: none; max-height: 1px;")
        right_lyt.addWidget(sep)
        right_lyt.addSpacing(14)

        # Bilgi satırları
        def info_row(label_text, value_text, value_color="#F5F5F5"):
            row = QHBoxLayout()
            lbl = QLabel(label_text)
            lbl.setFixedWidth(100)
            lbl.setStyleSheet("color: #777; font-size: 11px; font-family: 'Segoe UI';")
            val = QLabel(value_text)
            val.setStyleSheet(f"color: {value_color}; font-size: 11px; font-family: 'Segoe UI'; font-weight: bold;")
            val.setWordWrap(True)
            row.addWidget(lbl)
            row.addWidget(val)
            row.addStretch()
            return row

        right_lyt.addLayout(info_row("Sürüm", f"v{self.VERSION}", "#2ecc71"))
        right_lyt.addSpacing(6)
        right_lyt.addLayout(info_row("Geliştirici", self.DEVELOPER))
        right_lyt.addSpacing(6)
        right_lyt.addLayout(info_row("Konum", self.CITY))
        right_lyt.addSpacing(6)
        right_lyt.addLayout(info_row("Telif Hakkı",
            f"© {self.YEAR}  {self.DEVELOPER}", "#ccc"))
        right_lyt.addSpacing(14)

        # Web bağlantısı
        web_row = QHBoxLayout()
        web_icon = QLabel("🌐")
        web_icon.setStyleSheet("font-size: 14px;")
        web_btn = QPushButton(self.WEBSITE)
        web_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        web_btn.setStyleSheet("""
            QPushButton {
                color: #3498db;
                background: transparent;
                border: none;
                font-size: 12px;
                font-family: 'Segoe UI';
                text-decoration: underline;
                text-align: left;
            }
            QPushButton:hover { color: #5dade2; }
        """)
        web_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(f"https://{self.WEBSITE}")))
        web_row.addWidget(web_icon)
        web_row.addWidget(web_btn)
        web_row.addStretch()
        right_lyt.addLayout(web_row)

        right_lyt.addSpacing(8)

        # E-posta
        mail_row = QHBoxLayout()
        mail_icon = QLabel("✉️")
        mail_icon.setStyleSheet("font-size: 14px;")
        mail_btn = QPushButton(self.EMAIL)
        mail_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        mail_btn.setStyleSheet("""
            QPushButton {
                color: #8B3A3A;
                background: transparent;
                border: none;
                font-size: 12px;
                font-family: 'Segoe UI';
                text-decoration: underline;
                text-align: left;
            }
            QPushButton:hover { color: #e74c3c; }
        """)
        mail_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(f"mailto:{self.EMAIL}")))
        mail_row.addWidget(mail_icon)
        mail_row.addWidget(mail_btn)
        mail_row.addStretch()
        right_lyt.addLayout(mail_row)

        right_lyt.addStretch()

        # Alt şerit: Kızıldağ etiketi + Tamam butonu
        bottom_sep = QFrame()
        bottom_sep.setFrameShape(QFrame.Shape.HLine)
        bottom_sep.setStyleSheet("background-color: #333; border: none; max-height: 1px;")
        right_lyt.addWidget(bottom_sep)
        right_lyt.addSpacing(10)

        bottom_row = QHBoxLayout()
        nature_lbl = QLabel("🌲 Kızıldağ Milli Parkı'ndan Esintilerle Geliştirildi")
        nature_lbl.setStyleSheet("color: #2D5A27; font-size: 9px; font-family: 'Segoe UI';")
        bottom_row.addWidget(nature_lbl)
        bottom_row.addStretch()

        ok_btn = QPushButton("  Tamam  ")
        ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D5A27;
                color: #F5F5F5;
                border: none;
                border-radius: 6px;
                padding: 6px 18px;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }
            QPushButton:hover { background-color: #3a7a33; }
            QPushButton:pressed { background-color: #8B3A3A; }
        """)
        ok_btn.clicked.connect(self.close)
        bottom_row.addWidget(ok_btn)
        right_lyt.addLayout(bottom_row)

        root.addWidget(right)

    # Pencereyi sürükle
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None


class DrawingCanvas(QWidget):
    """
    Tam ekran saydam çizim yüzeyi.

    Masaüstünün üstünde, görünmez bir cam gibi durur.
    Aktif modda fare olaylarını yakalar ve çizim yapar;
    Pasif modda tıklamalar alttaki uygulamalara iletilir
    (WindowTransparentForInput bayrağı ile).
    """
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app  # Ana uygulama mantığına referans

        # Çerçevesiz, her zaman üstte, görev çubuuğunda görünmeyen pencere
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        # Arkaplan tamamen saydam olsun (alfa = 0)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.showFullScreen()

        self.draw_objects = []       # Tamamlanmış çizim nesnelerinin listesi
        self.current_object = None   # Fare basılıyken oluşmakta olan nesne
        self.is_drawing = False      # Çizim devam ediyor mu?
        self.is_static_mode = False  # Dondurma modu: ekran görüntüsüne çiz
        self.screenshot_pixmap = None  # Dondurma modunda alınan ekran görüntüsü

    def set_click_through(self, enabled: bool):
        """
        Kanvasa tıklanabilirliği aç/kapat.

        enabled=True  → Pasif mod: Fare olayları kanvasa gelmiyor,
                         altındaki masaüstü/uygulamalar tıklanabilir.
        enabled=False → Aktif mod: Kanvas fare olaylarını yakalar, çizim yapılır.

        NOT: Window flag değişikliklerinin etkili olabilmesi için
        pencereyi gizleyip tekrar göstermek gerekiyor (Qt gerekliliği).
        """
        self.hide()  # Flag değişimi için pencereyi geçici gizle
        if enabled:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowTransparentForInput)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowTransparentForInput)
        self.showFullScreen()
        self.raise_()                       # Kanvası tekrar üste taşı
        self.parent_app.panel.raise_()      # Panel her zaman kanvasın üstünde kalsın

    def paintEvent(self, event):
        """
        Qt’nun çizim döngüsü tarafından her yenileme isteğinde tetiklenir.
        Tüm kaydedilmiş ve devam eden çizim nesneleri burada ekrana yansıtılır.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # Kenar yumuşatma

        if self.is_static_mode and self.screenshot_pixmap:
            # Dondurma modunda: çekilmiş ekran görüntüsünü arkaplan olarak çiz
            painter.drawPixmap(self.rect(), self.screenshot_pixmap)
        elif not (self.windowFlags() & Qt.WindowType.WindowTransparentForInput):
            # Aktif modda: fare olaylarını yakalamak için neredeyse seffaf dolgu
            # (alfa=1 ile tamamen saydam gibi görünür ama tıklama alınır)
            painter.fillRect(self.rect(), QColor(0, 0, 0, 1))

        # Kaydedilmiş nesneleri en alttan üste dogru çiz (FIFO sırası)
        for obj in self.draw_objects:
            if obj['type'] == 'pen':     self.parent_app.draw_path(painter, obj)
            elif obj['type'] == 'rect':  self.parent_app.draw_rectangle(painter, obj)
            elif obj['type'] == 'ellipse': self.parent_app.draw_ellipse(painter, obj)
            elif obj['type'] == 'arrow': self.parent_app.draw_arrow(painter, obj)
            elif obj['type'] == 'image': painter.drawPixmap(obj['rect'], obj['pixmap'])
            elif obj['type'] == 'text':  self.parent_app.draw_text_obj(painter, obj)

        # Devam eden (henüz tamamlanmamış) nesneyi ön izleme olarak çiz
        if self.current_object:
            if self.current_object['type'] == 'pen':
                self.parent_app.draw_path(painter, self.current_object)
            elif self.current_object['type'] in ['rect', 'ellipse', 'arrow']:
                if self.current_object['type'] == 'rect':     self.parent_app.draw_rectangle(painter, self.current_object)
                elif self.current_object['type'] == 'ellipse': self.parent_app.draw_ellipse(painter, self.current_object)
                else:                                          self.parent_app.draw_arrow(painter, self.current_object)

    # Fare olaylarını ana uygulama mantığına devret (tek sorumluluk ilkesi)
    def mousePressEvent(self, event):   self.parent_app.canvas_mousePress(event)
    def mouseMoveEvent(self, event):    self.parent_app.canvas_mouseMove(event)
    def mouseReleaseEvent(self, event): self.parent_app.canvas_mouseRelease(event)
    def keyPressEvent(self, event):     self.parent_app.canvas_keyPress(event)

class ControlPanel(QFrame):
    """Yan tarafta duran kontrol paneli"""
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(90, 800)
        self.move(10, 50)
        self.quick_buttons = {} # Renk butonlarını tutmak için (init_ui'den önce tanımlanmalı)
        self.init_ui()

    def init_ui(self):
        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(0, 0, 90, 800)
        self.main_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(35, 35, 35, 235);
                border-radius: 15px;
                border: 2px solid #555;
            }
            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 8px;
                padding: 8px;
                font-weight: bold;
                font-size: 11px;
                border: 1px solid #666;
            }
            QPushButton:hover { background-color: #666; }
            QPushButton:checked { background-color: #e67e22; border: 1px solid white; }
            QLabel { color: #bbb; border:None; font-size: 9px; font-weight: bold; }
        """)
        
        layout = QVBoxLayout(self.main_frame)
        layout.setContentsMargins(10, 15, 10, 15)
        layout.setSpacing(8)

        # Panel başlığı: KALEMM / PEN PRO
        lbl_kalemm = QLabel("KALEMM")
        lbl_kalemm.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_kalemm.setStyleSheet("""
            color: #2D5A27;
            font-size: 11px;
            font-weight: bold;
            font-family: 'Segoe UI';
            border: none;
        """)
        lbl_penpro = QLabel("PEN PRO")
        lbl_penpro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_penpro.setStyleSheet("""
            color: #8B3A3A;
            font-size: 9px;
            font-weight: bold;
            font-family: 'Segoe UI';
            border: none;
            margin-bottom: 4px;
        """)
        layout.addWidget(lbl_kalemm)
        layout.addWidget(lbl_penpro)

        self.btn_pen = QPushButton("✏️")
        self.btn_pen.setCheckable(True); self.btn_pen.setChecked(True)
        self.btn_pen.clicked.connect(lambda: self.parent_app.set_shape_mode("pen"))
        layout.addWidget(self.btn_pen)

        self.btn_arrow = QPushButton("↗️")
        self.btn_arrow.setCheckable(True)
        self.btn_arrow.clicked.connect(lambda: self.parent_app.set_shape_mode("arrow"))
        layout.addWidget(self.btn_arrow)

        self.btn_rect = QPushButton("⬜")
        self.btn_rect.setCheckable(True)
        self.btn_rect.clicked.connect(lambda: self.parent_app.set_shape_mode("rect"))
        layout.addWidget(self.btn_rect)

        self.btn_ellipse = QPushButton("⭕")
        self.btn_ellipse.setCheckable(True)
        self.btn_ellipse.clicked.connect(lambda: self.parent_app.set_shape_mode("ellipse"))
        layout.addWidget(self.btn_ellipse)

        self.btn_text = QPushButton("T")
        self.btn_text.setStyleSheet("font-family: serif; font-size: 16px;") # Added back text style
        self.btn_text.setCheckable(True)
        self.btn_text.clicked.connect(lambda: self.parent_app.set_shape_mode("text"))
        layout.addWidget(self.btn_text)

        layout.addSpacing(5)
        layout.addWidget(QLabel("MODLAR"))
        self.btn_freeze = QPushButton("❄️")
        self.btn_freeze.setCheckable(True)
        self.btn_freeze.clicked.connect(self.parent_app.toggle_static_mode)
        layout.addWidget(self.btn_freeze)

        self.btn_paste = QPushButton("📋")
        self.btn_paste.clicked.connect(self.parent_app.paste_from_clipboard)
        layout.addWidget(self.btn_paste)

        self.btn_save = QPushButton("📸")
        self.btn_save.setToolTip("Sadece Çizimleri Kaydet") # Added back tooltip
        self.btn_save.clicked.connect(self.parent_app.save_canvas)
        layout.addWidget(self.btn_save)

        layout.addSpacing(5)
        layout.addWidget(QLabel("KALINLIK")) # Changed from BOYUT to KALINLIK
        self.slider_width = QSlider(Qt.Orientation.Horizontal)
        self.slider_width.setRange(5, 100)
        self.slider_width.setValue(self.parent_app.pen_width)
        self.slider_width.valueChanged.connect(self.parent_app.change_width)
        layout.addWidget(self.slider_width)

        layout.addStretch()

        # RENK SEÇİMİ - Kalıcı Çözüm: Konteyner kullanımı
        layout.addWidget(QLabel("RENKLER"))
        
        colors_container = QWidget()
        colors_container.setFixedSize(70, 48)  # Tam kontrol için sabit alan
        colors_grid = QGridLayout(colors_container)
        colors_grid.setSpacing(4)
        colors_grid.setContentsMargins(0, 0, 0, 0)
        
        quick_colors = [
            ("#FF0000", "Kırmızı"), ("#00CC00", "Yeşil"), ("#0055FF", "Mavi"),
            ("#FFFF00", "Sarı"),    ("#FFFFFF", "Beyaz"), ("#000000", "Siyah"),
        ]
        r, c = 0, 0
        for hex_code, tooltip in quick_colors:
            btn = QPushButton()
            btn.setFixedSize(20, 20)  # Buton boyutu biraz makulleştirildi
            btn.setToolTip(tooltip)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda ch, code=hex_code: self.parent_app.set_quick_color(code))
            colors_grid.addWidget(btn, r, c)
            self.quick_buttons[hex_code] = btn
            c += 1
            if c > 2: c = 0; r += 1
            
        layout.addWidget(colors_container, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(10)
        self.btn_color_picker = QPushButton("🎨")
        self.btn_color_picker.setFixedSize(62, 30)
        self.update_color_button()
        self.btn_color_picker.clicked.connect(self.parent_app.choose_color)
        layout.addWidget(self.btn_color_picker, 0, Qt.AlignmentFlag.AlignHCenter)

        self.btn_undo = QPushButton("↩️")
        self.btn_undo.clicked.connect(self.parent_app.undo)
        layout.addWidget(self.btn_undo)

        self.btn_clear = QPushButton("🗑️")
        self.btn_clear.clicked.connect(self.parent_app.clear_all)
        layout.addWidget(self.btn_clear)

        # AKTİF / HAKKINDA / KAPAT (en altta)
        self.btn_toggle_active = QPushButton("AKTİF")
        self.btn_toggle_active.setCheckable(True)
        self.btn_toggle_active.setChecked(True)
        self.btn_toggle_active.setStyleSheet("background-color: #27ae60; color: white;")
        self.btn_toggle_active.clicked.connect(self.parent_app.toggle_active_passive)
        layout.addWidget(self.btn_toggle_active)

        self.btn_about = QPushButton()
        self.btn_about.setToolTip("Hakkında")
        self.btn_about.clicked.connect(self.parent_app.show_about)
        logo1_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Kalemm_gorsel_logo1.png")
        if os.path.exists(logo1_path):
            logo1_pix = QPixmap(logo1_path).scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.btn_about.setIcon(QIcon(logo1_pix))
            self.btn_about.setIconSize(QSize(32, 32))
        else:
            self.btn_about.setText("❔")
        layout.addWidget(self.btn_about)

        self.btn_close = QPushButton("❌")
        self.btn_close.clicked.connect(self.parent_app.close_app)
        self.btn_close.setStyleSheet("background-color: #c0392b; color: white;")
        layout.addWidget(self.btn_close)

    def update_color_button(self):
        current_hex = self.parent_app.pen_color.name().upper()
        # Ana seçiciyi güncelle
        self.btn_color_picker.setStyleSheet(f"background-color: {current_hex}; border: 2px solid white; border-radius: 5px;")
        
        # Hızlı renk butonlarının kenarlıklarını güncelle
        for hex_code, btn in self.quick_buttons.items():
             if hex_code.upper() == current_hex:
                 btn.setStyleSheet(f"background-color: {hex_code}; border: 2px solid #fff; border-radius: 3px;")
             else:
                 btn.setStyleSheet(f"background-color: {hex_code}; border: 1px solid #555; border-radius: 3px;")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'old_pos'):
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()
            self.parent_app.update_canvas_mask() # Hareket ettikçe maskeyi güncelle

    def mouseReleaseEvent(self, event):
        if hasattr(self, 'old_pos'): del self.old_pos

class KalemmPenApp:
    """Uygulama Mantığı ve Pencerelerin Yöneticisi"""
    def __init__(self):
        self.config_file = "kalemm_config.json"
        self.load_settings()
        
        # Değişkenleri önce tanımla (UI bunlara ihtiyaç duyuyor)
        self.shape_mode = "pen"
        self.pen_color = QColor(*self.settings["pen_color"])
        self.pen_width = self.settings["pen_width"]
        
        self.canvas = DrawingCanvas(self)
        self.panel = ControlPanel(self)
        
        # Metin girişi için canvas üzerinde gizli bir widget
        self.text_input = QLineEdit(self.canvas)
        self.text_input.setHidden(True)
        self.text_input.setStyleSheet("background: #222; color: white; border: 1px solid #e67e22; padding: 2px;") # Added padding
        self.text_input.returnPressed.connect(self.commit_text)
        self.text_pos = QPoint()

        self.canvas.show()
        self.panel.show()
        self.update_canvas_mask()
        self.canvas.raise_()
        self.panel.raise_()
        self.panel.update_color_button() 

    def update_canvas_mask(self):
        """
        Kanvas penceresi üzerinde, panalin kapladığı alana karşılık
        gelen bölgeı 'delerek' fare olaylarının panele geçmesini sağlar.

        setMask(QRegion) ile kanvasın 'tıklanabilir' alanı kısıtlanır:
        panel geometrisi bu alandan çıkarılır, borada kanvas 'yok' hissini verir.
        Pasif modda kanvas zaten saydam olduğundan maskeye gerek yoktur.
        """
        if self.canvas.windowFlags() & Qt.WindowType.WindowTransparentForInput:
            self.canvas.clearMask()  # Pasif modda maske gerekmez
            return

        full_region = QRegion(self.canvas.rect())        # Tüm ekran alanı
        panel_rect  = self.panel.geometry()              # Panelin ekrandaki konumu
        # Panel bölgesini kanvasın tıklanabilir alanından çıkar
        mask_region = full_region.subtracted(QRegion(panel_rect))
        self.canvas.setMask(mask_region)

    def load_settings(self):
        """
        kalemm_config.json dosyasından ayarları yükler.
        Dosya yoksa ya da bozuksa güvenli varsayılan değerler kullanılır.
        """
        default_settings = {
            "pen_color"     : [255, 0, 0, 255],  # Varsayılan: Kırmızı
            "pen_width"     : 5,                 # Varsayılan kalem kalınlığı
            "opacity"       : 0.9,               # (Gelecekte kullanılabilir)
            "history_limit" : 1000               # (Gelecekte kullanılabilir)
        }
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    self.settings = json.load(f)
            except:
                self.settings = default_settings  # JSON bozuksa varsayılana dön
        else:
            self.settings = default_settings
        self.pen_width = self.settings.get("pen_width", 5)

    def save_settings(self):
        """Güncel kalem rengi ve kalınlığını JSON dosyasına yazar."""
        self.settings["pen_color"] = [
            self.pen_color.red(), self.pen_color.green(),
            self.pen_color.blue(), self.pen_color.alpha()
        ]
        self.settings["pen_width"] = self.pen_width
        with open(self.config_file, "w") as f:
            json.dump(self.settings, f)

    def set_shape_mode(self, mode: str):
        """
        Çizim modunu değiştirir ve panőldeki ilgili butonu işaretler.
        mod: 'pen' | 'arrow' | 'rect' | 'ellipse' | 'text'
        """
        self.shape_mode = mode
        self.panel.btn_pen.setChecked(mode == "pen")
        self.panel.btn_arrow.setChecked(mode == "arrow")
        self.panel.btn_rect.setChecked(mode == "rect")
        self.panel.btn_ellipse.setChecked(mode == "ellipse")
        self.panel.btn_text.setChecked(mode == "text")
        if mode != "text":
            self.text_input.setHidden(True)  # Metin modu dışında yazı alanı gizle

    def toggle_active_passive(self, checked: bool):
        """
        AKTİF / PASİF modlar arasında geçiş yapar.
        Aktif: Kanvas fare olaylarını yakalar, çizim yapılır.
        Pasif: Fare olayları saydam kanvastan geçer, masaüstü serbestce kullanılır.
        """
        if checked:  # Aktif mod
            self.panel.btn_toggle_active.setText("AKTİF")
            self.panel.btn_toggle_active.setStyleSheet("background-color: #27ae60; color: white;")
            self.canvas.set_click_through(False)
            self.update_canvas_mask()  # Panel deliği yeniden oluştur
        else:        # Pasif mod
            self.panel.btn_toggle_active.setText("PASİF")
            self.panel.btn_toggle_active.setStyleSheet("background-color: #e67e22; color: white;")
            self.canvas.set_click_through(True)
            self.canvas.clearMask()    # Pasif modda maskeye gerek yok
        self.panel.raise_()  # Mod değişiminden sonra paneli uyandır

    def set_quick_color(self, hex_code: str):
        """Hızlı renk butonundan renk seçimini uygular ve kaydeder."""
        self.pen_color = QColor(hex_code)
        self.panel.update_color_button()
        self.save_settings()
        # Metin modu açıksa yazı alanının rengini de güncelle
        if not self.text_input.isHidden():
            self.text_input.setStyleSheet(
                f"background: #222; color: {self.pen_color.name()};"
                f"border: 1px solid #e67e22; font-size: {self.pen_width//2}px;"
            )

    def choose_color(self):
        """
        Tam renk paleti diyaloğunu açar.
        Pencereler renk seçici diyaloğunun arkasında kalabileceğinden
        geçici olarak gizlenip, seçim bittikten sonra yeniden gösterilir.
        """
        self.canvas.hide(); self.panel.hide()
        color = QColorDialog.getColor(self.pen_color, self.canvas, "Renk Seç")
        self.canvas.show(); self.panel.show()
        self.canvas.raise_(); self.panel.raise_()
        if color.isValid():
            self.pen_color = color
            self.panel.update_color_button()
            self.save_settings()

    def change_width(self, val: int):
        """Slider değiştiğinde kalem kalınlığını günceller; metin boyutunu da eşler."""
        self.pen_width = val
        self.save_settings()
        if not self.text_input.isHidden():
            self.text_input.setStyleSheet(
                f"background: #222; color: {self.pen_color.name()};"
                f"border: 1px solid #e67e22; font-size: {self.pen_width//2}px;"
            )

    def undo(self):
        """Son çizim nesnesini geri alır (Ctrl+Z)."""
        if self.canvas.draw_objects:
            self.canvas.draw_objects.pop()
            self.canvas.update()

    def clear_all(self):
        """Tüm çizimleri temizler."""
        self.canvas.draw_objects = []
        self.canvas.update()

    def toggle_static_mode(self, checked: bool):
        """
        Dondurma modunu aç/kapat.
        Açıkken anlık ekran görüntüsü alınır ve arkaplan olarak kullanılır;
        ekran yenilenirse çizimler kaybolmaz.
        """
        self.canvas.is_static_mode = checked
        if checked:
            self.canvas.hide(); self.panel.hide()  # Görüntü almadan önce gizle
            QApplication.processEvents()           # Gizleme ekrana yansısın
            screen = QGuiApplication.primaryScreen()
            self.canvas.screenshot_pixmap = screen.grabWindow(0)  # Tüm ekranı yakala
            self.canvas.show(); self.panel.show()
            self.canvas.raise_(); self.panel.raise_()
        else:
            self.canvas.screenshot_pixmap = None  # Arkaplanı temizle
        self.canvas.update()

    def paste_from_clipboard(self):
        """
        Panodan resim alarak kanvasın ortasına yapıştırır.
        Metin içeren pano verisi desteklenmez, yalnızca resim.
        """
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()
        if mime_data.hasImage():
            image = QImage(clipboard.image())
            if not image.isNull():
                # Resmi kanvasın ortasına hizala
                pos = self.canvas.rect().center() - QPoint(image.width()//2, image.height()//2)
                self.canvas.draw_objects.append({
                    'type'  : 'image',
                    'pixmap': QPixmap.fromImage(image),
                    'rect'  : QRect(pos.x(), pos.y(), image.width(), image.height())
                })
                self.canvas.update()

    def save_canvas(self):
        """
        Tüm çizimleri saydam arkaplanlı PNG olarak diske kaydeder.
        Hedef klasör: ~/Documents/Kalemm_Cizimleri/
        Dosya adı formatı: Cizim_YYYYMMDD_HHMMSS.png
        """
        folder = os.path.join(os.path.expanduser("~"), "Documents", "Kalemm_Cizimleri")
        if not os.path.exists(folder):
            os.makedirs(folder)  # Klasör yoksa oluştur
        path = os.path.join(folder, f"Cizim_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

        img = QPixmap(self.canvas.size())
        img.fill(Qt.GlobalColor.transparent)      # Saydam arka plan
        painter = QPainter(img)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        for obj in self.canvas.draw_objects:       # Her nesneyi off-screen çiz
            if   obj['type'] == 'pen':     self.draw_path(painter, obj)
            elif obj['type'] == 'rect':    self.draw_rectangle(painter, obj)
            elif obj['type'] == 'ellipse': self.draw_ellipse(painter, obj)
            elif obj['type'] == 'arrow':   self.draw_arrow(painter, obj)
            elif obj['type'] == 'image':   painter.drawPixmap(obj['rect'], obj['pixmap'])
            elif obj['type'] == 'text':    self.draw_text_obj(painter, obj)
        painter.end()
        if img.save(path, "PNG"):
            print(f"Kaydedildi: {path}")

    def commit_text(self):
        """
        Metin giriş alanındaki metni bir 'text' nesnesine dönüştürür,
        kanvas nesne listesine ekler ve alanı temizler.
        """
        text = self.text_input.text()
        if text:
            self.canvas.draw_objects.append({
                'type' : 'text',
                'text' : text,
                'pos'  : self.text_pos,
                'color': self.pen_color,
                'size' : self.pen_width   # Kalem kalınlığı = yazı boyutu
            })
            self.text_input.clear()
        self.text_input.setHidden(True)
        self.canvas.update()

    # =========================================================================
    # Çizim Yardımcıları
    # Her metot, içine aktardığınız nesne sözlüğündülerin 'color' ve
    # 'width' anahtarlarını kullanarak verilen QPainter üzerinde çizer.
    # =========================================================================

    def draw_path(self, p, o):
        """Serbest kalem yolu: ardışık noktalar arası çizgi."""
        p.setPen(QPen(o['color'], o['width'],
                      Qt.PenStyle.SolidLine,
                      Qt.PenCapStyle.RoundCap,
                      Qt.PenJoinStyle.RoundJoin))
        pts = o['points']
        for i in range(len(pts)-1):
            p.drawLine(pts[i], pts[i+1])

    def draw_rectangle(self, p, o):
        """Dikdörtgen çizimi."""
        p.setPen(QPen(o['color'], o['width']))
        p.drawRect(o['rect'])

    def draw_ellipse(self, p, o):
        """Elips / çember çizimi."""
        p.setPen(QPen(o['color'], o['width']))
        p.drawEllipse(o['rect'])

    def draw_arrow(self, p, o):
        p1, p2 = o['p1'], o['p2']
        p.setPen(QPen(o['color'], o['width'], Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        
        # Ana çizgiyi çiz
        p.drawLine(p1, p2)
        
        import math
        # Çizginin vektörünü al
        diff = p2 - p1
        if diff.manhattanLength() < 5: 
            return

        # Açıyı hesapla (radyan cinsinden)
        # Not: atan2(y, x) standarttır, ancak Qt'de y aşağı doğrudur.
        angle = math.atan2(diff.y(), diff.x())
        
        sz = o['width'] * 4  # Ok ucu büyüklüğü
        arrow_angle = math.pi / 6  # 30 derecelik kanat açısı

        # Ok ucu noktalarını hesapla (p2'den geriye doğru)
        pa1 = p2 - QPoint(int(math.cos(angle - arrow_angle) * sz), 
                        int(math.sin(angle - arrow_angle) * sz))
        pa2 = p2 - QPoint(int(math.cos(angle + arrow_angle) * sz), 
                        int(math.sin(angle + arrow_angle) * sz))

        # Ok ucunu çiz
        p.drawLine(p2, pa1)
        p.drawLine(p2, pa2)

    def draw_text_obj(self, p, o):
        """Metin nesnesini belirtilen konuma ve renge göre çizer."""
        p.setPen(o['color'])
        p.setFont(QFont("Segoe UI", o['size']))
        p.drawText(o['pos'], o['text'])

    # =========================================================================
    # Kanvas Fare & Klavye Olayları
    # =========================================================================

    def canvas_mousePress(self, event):
        """
        Fare sol tuşu basıldı: yeni nesne yarat veya metin girişini aç.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            if self.shape_mode == "text":
                if not self.text_input.isHidden():
                    self.commit_text()  # Önceki metni kaydet
                self.text_pos = event.pos()
                self.text_input.move(event.pos().x(), event.pos().y() - 20)
                self.text_input.setHidden(False)
                self.text_input.setFocus()
                self.text_input.setStyleSheet(
                    f"background: #222; color: {self.pen_color.name()};"
                    f"border: 1px solid #e67e22; font-size: {self.pen_width//2}px;"
                )
                return

            self.canvas.is_drawing = True
            if self.shape_mode == "pen":
                self.canvas.current_object = {
                    'type'  : 'pen',
                    'points': [event.pos()],
                    'color' : self.pen_color,
                    'width' : self.pen_width
                }
            elif self.shape_mode in ["rect", "ellipse", "arrow"]:
                self.start_pos = event.pos()
                if self.shape_mode == "arrow":
                    self.canvas.current_object = {
                        'type' : 'arrow',
                        'p1'   : self.start_pos,
                        'p2'   : self.start_pos,
                        'color': self.pen_color,
                        'width': self.pen_width
                    }
                else:
                    self.canvas.current_object = {
                        'type' : self.shape_mode,
                        'rect' : QRect(self.start_pos, QSize()),
                        'color': self.pen_color,
                        'width': self.pen_width
                    }
            self.canvas.update()

    def canvas_mouseMove(self, event):
        """Fare hareket ettikçe mevcut nesneyi güncelle (canlı önizleme)."""
        if self.canvas.is_drawing and self.canvas.current_object:
            if self.canvas.current_object['type'] == 'pen':
                self.canvas.current_object['points'].append(event.pos())
            elif self.canvas.current_object['type'] == 'arrow':
                self.canvas.current_object['p2'] = event.pos()
            elif self.canvas.current_object['type'] in ["rect", "ellipse"]:
                # normalized() → negatif boyutu düzeltir (ters yönde çizim)
                self.canvas.current_object['rect'] = QRect(
                    self.start_pos, event.pos()
                ).normalized()
            self.canvas.update()

    def canvas_mouseRelease(self, event):
        """Fare bırakıldı: nesneyi tamamla ve kalıcı listeye ekle."""
        if event.button() == Qt.MouseButton.LeftButton and self.canvas.is_drawing:
            self.canvas.is_drawing = False
            if self.canvas.current_object:
                self.canvas.draw_objects.append(self.canvas.current_object)
            self.canvas.current_object = None
            self.canvas.update()

    def canvas_keyPress(self, event):
        """
        Klavye kısayolları:
          Ctrl+Z → Geri al    | Ctrl+V → Panodan yapıştır
          Ctrl+1 → Kırmızı   | Ctrl+2 → Yeşil  | Ctrl+3 → Mavi
          ESC    → Yazı alanını kapat / uygulamayı kapat
        """
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if   event.key() == Qt.Key.Key_Z: self.undo()
            elif event.key() == Qt.Key.Key_V: self.paste_from_clipboard()
            elif event.key() == Qt.Key.Key_1: self.pen_color = QColor(255, 0, 0);   self.panel.update_color_button()
            elif event.key() == Qt.Key.Key_2: self.pen_color = QColor(0, 255, 0);   self.panel.update_color_button()
            elif event.key() == Qt.Key.Key_3: self.pen_color = QColor(0, 0, 255);  self.panel.update_color_button()
        elif event.key() == Qt.Key.Key_Escape:
            if not self.text_input.isHidden():
                self.text_input.setHidden(True)  # Yazı alanını kapat
            else:
                self.close_app()  # Kapat
        self.canvas.update()

    def show_about(self):
        """Hakkında penceresini açar; kapandıktan sonra paneli ön plana getirir."""
        dlg = AboutDialog(self.panel)  # Paneli ebeveyn olarak ata
        dlg.exec()
        
        # Dialog kapandıktan sonra paneli ön plana ve odağa al
        self.panel.show()
        self.panel.raise_()
        self.panel.activateWindow()
        self.panel.setFocus()

    def close_app(self):
        """Ayarları kaydeder ve uygulaması kapatır."""
        self.save_settings()
        QApplication.quit()


# =============================================================================
# Giriş Noktası
# =============================================================================
if __name__ == "__main__":
    app     = QApplication(sys.argv)
    kalemm  = KalemmPenApp()   # Tek koordinatör özne
    sys.exit(app.exec())        # Qt olay döngüsünü başlat
