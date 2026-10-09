"""Native, opt-in Qt desktop GUI for the standalone Subterfuge Framework.

The GUI uses Qt Widgets only. It embeds no browser engine or WebView and
does not launch the web dashboard automatically. Network activity occurs
only after an explicit GUI action and confirmation. Analyses use worker
threads so the window remains responsive.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable
from importlib.resources import files
import sys

from PySide6.QtCore import QProcess, QRunnable, QThreadPool, Qt, QObject, Signal, QSize
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPen, QBrush
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QFileDialog, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QListWidget,
    QMainWindow, QMessageBox, QPlainTextEdit, QProgressBar, QPushButton,
    QScrollArea, QSizePolicy, QSpinBox, QStackedWidget, QStatusBar, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget
)

from . import __version__
from .analysis import AnalysisError, analyze_nmap, analyze_pcap, read_input, write_report
from .desktop_reports import read_saved_report, report_preview, report_summary

COLORS = {
    "background": "#0A111B", "side": "#101C2B", "card": "#142334",
    "border": "#24354A", "text": "#EAF3FF", "muted": "#A1B5C9",
    "accent": "#55D6B3", "danger": "#F2A1A1", "blue": "#81B5FF",
}

STYLESHEET = """
* { font-family: "DejaVu Sans", "Adwaita Sans", sans-serif; font-size: 12px; }
QMainWindow, QWidget#root, QWidget#page {background: #0A111B; color: #EAF3FF;}
QFrame#sidebar {background: #101C2B; border-right: 1px solid #24354A;}
QFrame#topbar {background: #0A111B; border-bottom: 1px solid #24354A;}
QFrame#card, QGroupBox#card {
    background: #142334; border: 1px solid #293C51; border-radius: 13px;
}
QGroupBox#card {margin-top: 13px; padding: 18px 14px 15px;}
QGroupBox#card::title {
    subcontrol-origin: margin; subcontrol-position: top left;
    left: 16px; padding: 0 5px; color: #EAF3FF;
    font-weight: 700; font-size: 13px;
}
QLabel {background: transparent; color: #EAF3FF;}
QLabel#brand {font-size: 16px; font-weight: 800; letter-spacing: 0px;}
QLabel#eyebrow {color: #55D6B3; font-size: 10px; font-weight: 800; letter-spacing: 2px;}
QLabel#pageTitle {font-size: 25px; font-weight: 800;}
QLabel#subtitle, QLabel#muted {color: #A1B5C9; font-size: 11px;}
QLabel#metricValue {font-size: 27px; font-weight: 800;}
QLabel#metricLabel {color: #A1B5C9; font-size: 11px;}
QLabel#statusTag {border: 1px solid #2F6A61; border-radius: 11px;
    background: #18352F; padding: 5px 11px; color: #79E7C6; font-size: 10px;}
QPushButton {
    border: 1px solid #365069; background: #1C2D42; color: #EAF3FF;
    padding: 10px 13px; border-radius: 8px; font-weight: 600;
}
QPushButton:hover {background: #294159; border: 1px solid #55D6B3;}
QPushButton:pressed {background: #193B35;}
QPushButton:disabled {color: #6D8097; border-color: #2B3A4B; background: #172232;}
QPushButton#primary {background: #55D6B3; border: 1px solid #55D6B3;
    color: #08231F; font-weight: 800;}
QPushButton#primary:hover {background: #82E8CD;}
QPushButton#danger {background: #553039; border-color: #96565F; color: #FFE8E9;}
QPushButton#navButton {
    border: 0; border-radius: 8px; background: transparent;
    color: #A7BBD0; text-align: left; padding: 13px 15px; font-size: 12px;
}
QPushButton#navButton:hover {background: #1F3045; color: #F5FAFF;}
QPushButton#navButton[active="true"] {
    background: #1F3E40; color: #78E9CB; border-left: 3px solid #55D6B3;
}
QLineEdit, QSpinBox, QComboBox, QPlainTextEdit {
    background: #0E1A29; border: 1px solid #344C64; border-radius: 7px;
    color: #EAF3FF; padding: 8px 9px; selection-background-color: #297B69;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QPlainTextEdit:focus {
    border-color: #55D6B3;
}
QComboBox QAbstractItemView {background: #1A293A; color: #EAF3FF;}
QCheckBox {color: #D9E5F3; spacing: 10px;}
QCheckBox::indicator {width: 16px; height: 16px;}
QTableWidget, QListWidget {
    background: #101C2B; border: 1px solid #2C4155;
    border-radius: 9px; gridline-color: #263B4E; color: #E0EBF7;
    alternate-background-color: #18283A;
}
QTableWidget::item {padding: 7px 8px;}
QHeaderView::section {background: #1C3043; color: #BFD2E7; padding: 10px;
    border: 0; border-bottom: 1px solid #375068; font-weight: 700;}
QTableWidget::item:selected, QListWidget::item:selected {background: #21544D; color: #F6FFFE;}
QScrollArea {border: 0; background: #0A111B;}
QScrollBar:vertical {background: #101C2B; width: 10px; margin: 2px;}
QScrollBar::handle:vertical {background: #34495F; min-height: 24px; border-radius: 5px;}
QStatusBar {background: #0D1927; color: #B0C4D7; border-top: 1px solid #26394D;}
QProgressBar {border: 0; background: #162537; height: 5px; border-radius: 2px;}
QProgressBar::chunk {background: #55D6B3; border-radius: 2px;}
"""

PAGE_LABELS = [
    ("◈", "Vue d'ensemble"),
    ("▤", "Fichiers & rapports"),
    ("⌁", "Réseau"),
    ("◇", "TLS / HTTPS"),
    ("⚙", "Paramètres"),
]


def _text(text: str, style: str = "", wrap: bool = False) -> QLabel:
    label = QLabel(text)
    label.setTextFormat(Qt.TextFormat.PlainText)
    if style:
        label.setObjectName(style)
    label.setWordWrap(wrap)
    return label


def _button(text: str, action: Callable, primary: bool = False, danger: bool = False) -> QPushButton:
    button = QPushButton(text)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    if primary:
        button.setObjectName("primary")
    elif danger:
        button.setObjectName("danger")
    button.clicked.connect(action)
    return button


def _column(parent: QWidget | None = None, gap: int = 14, padding: int = 0) -> QVBoxLayout:
    layout = QVBoxLayout(parent)
    layout.setSpacing(gap)
    layout.setContentsMargins(padding, padding, padding, padding)
    return layout


def _row(parent: QWidget | None = None, gap: int = 10, padding: int = 0) -> QHBoxLayout:
    layout = QHBoxLayout(parent)
    layout.setSpacing(gap)
    layout.setContentsMargins(padding, padding, padding, padding)
    return layout


def _card(layout: QVBoxLayout, heading: str, description: str = "") -> tuple[QGroupBox, QVBoxLayout]:
    card = QGroupBox(heading)
    card.setObjectName("card")
    body = _column(card, gap=12, padding=10)
    if description:
        body.addWidget(_text(description, "muted", wrap=True))
    layout.addWidget(card)
    return card, body


def _table(headers: list[str], minimum: int = 120) -> QTableWidget:
    table = QTableWidget(0, len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.setMinimumHeight(minimum)
    table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
    table.setAlternatingRowColors(True)
    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    table.setWordWrap(False)
    table.verticalHeader().hide()
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    return table


def _fill_table(table: QTableWidget, rows: list[tuple | list]) -> None:
    table.setUpdatesEnabled(False)
    try:
        table.setRowCount(len(rows))
        for i, fields in enumerate(rows):
            for j, field in enumerate(fields[:table.columnCount()]):
                item = QTableWidgetItem(str(field))
                item.setToolTip(str(field)[:850])
                table.setItem(i, j, item)
        table.resizeRowsToContents()
    finally:
        table.setUpdatesEnabled(True)


def _scroll(widget: QWidget) -> QScrollArea:
    area = QScrollArea()
    area.setWidget(widget)
    area.setWidgetResizable(True)
    area.setFrameShape(QFrame.Shape.NoFrame)
    return area


def _frame(height: int = 0) -> QFrame:
    panel = QFrame()
    panel.setObjectName("card")
    if height:
        panel.setMinimumHeight(height)
    return panel


def _perform_job(action: str, settings: dict) -> dict:
    """Explicit allowlist of user-requested tasks, suitable for a background worker."""
    if action == "demo":
        from .demo import demo_report
        return demo_report()
    if action == "import_pcap":
        return analyze_pcap(read_input(settings["file"]), Path(settings["file"]).name)
    if action == "import_nmap":
        return analyze_nmap(read_input(settings["file"]), Path(settings["file"]).name)
    if action == "import_bettercap":
        from .bettercap_events import import_bettercap_events
        return import_bettercap_events(settings["file"])
    if action == "open_report":
        return read_saved_report(settings["file"])
    if action == "doctor":
        from .environment import doctor
        return {"desktop_kind": "doctor", "environment": doctor()}
    if action == "interfaces":
        from .environment import interfaces
        return {"desktop_kind": "interfaces", "interfaces": interfaces()}
    if action == "discover":
        from .environment import discover
        return discover(settings["target"])
    if action == "scan_services":
        from .environment import scan_services
        return scan_services(settings["target"], settings["ports"])
    if action == "capture_arp":
        from .environment import capture
        return capture(settings["interface"], float(settings["duration"]))
    if action == "capture_protocols":
        from .environment import capture_protocols
        return capture_protocols(settings["interface"], float(settings["duration"]))
    if action == "inspect_tls":
        from .tls import inspect_tls
        return inspect_tls(settings["host"], int(settings["port"]))
    if action == "decrypt_tls":
        from .tls_lab import decrypt_https
        return decrypt_https(
            settings["capture"], settings["keylog"],
            include_uris=bool(settings.get("include_uris", False)),
            export_json=settings.get("export_decrypted_json"),
        )
    raise AnalysisError("Unsupported native desktop action.")


class _Signals(QObject):
    success = Signal(object)
    failure = Signal(str)
    finished = Signal()


class _Job(QRunnable):
    def __init__(self, action: str, settings: dict):
        super().__init__()
        self.action = action
        self.settings = dict(settings)
        self.signals = _Signals()

    def run(self) -> None:
        try:
            result = _perform_job(self.action, self.settings)
        except (AnalysisError, OSError, ValueError) as exc:
            self.signals.failure.emit(str(exc)[:900])
        except Exception as exc:
            # Present an error without a traceback or any file contents.
            self.signals.failure.emit(f"Erreur inattendue : {type(exc).__name__}: {str(exc)[:280]}")
        else:
            self.signals.success.emit(result)
        finally:
            self.signals.finished.emit()


class _Mark(QWidget):
    """Simple vector-only brand mark; no image resources needed for the window."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(42, 42)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor("#183D39")))
        painter.setPen(QPen(QColor("#55D6B3"), 1.4))
        painter.drawRoundedRect(2, 2, 38, 38, 10, 10)
        font = QFont("DejaVu Sans", 22, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor("#83F0D1"))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "S")
        painter.end()


class DesktopWindow(QMainWindow):
    """One coherent native workspace for local evidence and explicit network tasks."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Subterfuge Framework · Desktop {__version__}")
        self.setWindowIcon(QIcon(str(files("subterfuge").joinpath("assets/subterfuge.svg"))))
        self.resize(1250, 850)
        self.setMinimumSize(980, 640)
        self.setStyleSheet(STYLESHEET)
        self.setObjectName("subterfugeDesktop")
        self._pool = QThreadPool.globalInstance()
        self._busy = False
        self._jobs: list[_Job] = []
        self._report: dict | None = None
        self._proxy: QProcess | None = None
        self._web: QProcess | None = None
        self._nav_buttons: list[QPushButton] = []

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        shell = _row(root, gap=0)
        self._build_sidebar(shell)
        right = QWidget()
        right.setObjectName("page")
        shell.addWidget(right, stretch=1)
        right_layout = _column(right, gap=0)
        self._build_topbar(right_layout)
        self.pages = QStackedWidget()
        right_layout.addWidget(self.pages, stretch=1)
        self._build_overview()
        self._build_files()
        self._build_network()
        self._build_tls()
        self._build_settings()
        self._navigate(0)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Prêt · Aucun scan ni capture actif")
        self._render_empty()

    def _build_sidebar(self, shell: QHBoxLayout) -> None:
        bar = QFrame()
        bar.setObjectName("sidebar")
        bar.setFixedWidth(248)
        layout = _column(bar, gap=8, padding=18)
        branding = QWidget()
        top = _row(branding, gap=12)
        top.addWidget(_Mark())
        name = QWidget()
        name_layout = _column(name, gap=2)
        name_layout.addWidget(_text("SUBTERFUGE", "brand"))
        name_layout.addWidget(_text("Network security workspace", "muted"))
        top.addWidget(name, stretch=1)
        layout.addWidget(branding)
        layout.addSpacing(30)
        layout.addWidget(_text("ESPACE DE TRAVAIL", "eyebrow"))
        layout.addSpacing(7)
        for index, (glyph, title) in enumerate(PAGE_LABELS):
            button = QPushButton(f"  {glyph}    {title.replace('&', '&&')}")
            button.setObjectName("navButton")
            button.setProperty("active", False)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _, current=index: self._navigate(current))
            layout.addWidget(button)
            self._nav_buttons.append(button)
        layout.addStretch()
        hint = _text("LOCAL  ·  DONNÉES PRIVÉES\nAucune télémétrie intégrée", "muted")
        hint.setWordWrap(True)
        layout.addWidget(hint)
        layout.addWidget(_text(f"ALPHA {__version__}", "eyebrow"))
        shell.addWidget(bar)

    def _build_topbar(self, layout: QVBoxLayout) -> None:
        head = QFrame()
        head.setObjectName("topbar")
        head.setFixedHeight(67)
        row = _row(head, gap=12, padding=16)
        self.top_title = _text("Vue d'ensemble", "pageTitle")
        self.top_title.setStyleSheet("font-size: 16px;")
        row.addWidget(self.top_title)
        row.addStretch()
        row.addWidget(_text("ANALYSE LOCALE", "statusTag"))
        layout.addWidget(head)

    def _page(self, heading: str, subtitle: str) -> tuple[QWidget, QVBoxLayout]:
        container = QWidget()
        container.setObjectName("page")
        layout = _column(container, gap=18, padding=24)
        layout.addWidget(_text(heading, "pageTitle"))
        layout.addWidget(_text(subtitle, "subtitle", wrap=True))
        return container, layout

    def _add_scroll_page(self, container: QWidget) -> None:
        self.pages.addWidget(_scroll(container))

    def _metric(self, parent: QHBoxLayout, name: str) -> QLabel:
        panel = _frame(104)
        row = _column(panel, gap=8, padding=16)
        row.addWidget(_text(name.upper(), "metricLabel"))
        value = _text("—", "metricValue")
        row.addWidget(value)
        parent.addWidget(panel, stretch=1)
        return value

    def _build_overview(self) -> None:
        widget, layout = self._page(
            "Comprendre votre réseau",
            "Inventaire, observations et constats regroupés en un seul endroit. "
            "Aucune connexion réseau n'est lancée automatiquement.",
        )
        controls = QWidget()
        buttons = _row(controls)
        buttons.addWidget(_button("Charger la démonstration", lambda: self._launch("demo", {}), primary=True))
        buttons.addWidget(_button("Importer une capture", self._open_capture))
        buttons.addWidget(_button("Enregistrer JSON", self._save_report))
        buttons.addStretch()
        layout.addWidget(controls)
        metrics = QWidget()
        cards = _row(metrics, gap=15)
        self.metric_hosts = self._metric(cards, "Machines observées")
        self.metric_activity = self._metric(cards, "Activité")
        self.metric_findings = self._metric(cards, "Éléments à examiner")
        layout.addWidget(metrics)
        source = _frame()
        src_row = _row(source, padding=15)
        src_row.addWidget(_text("SOURCE  ", "eyebrow"))
        self.overview_source = _text("Aucun rapport ouvert", "muted")
        src_row.addWidget(self.overview_source, stretch=1)
        layout.addWidget(source)
        group1, section1 = _card(layout, "Inventaire des équipements")
        self.host_table = _table(["Adresse IP", "Adresses MAC", "Observations / services"], 190)
        section1.addWidget(self.host_table)
        group2, section2 = _card(layout, "Éléments à examiner")
        self.findings_table = _table(["Niveau", "Constat", "Interprétation"], 150)
        section2.addWidget(self.findings_table)
        group3, section3 = _card(layout, "DHCP / NetBIOS / événements passifs")
        self.passive_table = _table(["Type", "Observation", "Détail"], 120)
        section3.addWidget(self.passive_table)
        group4, section4 = _card(layout, "Avertissements")
        self.warning_list = QListWidget()
        self.warning_list.setMinimumHeight(94)
        section4.addWidget(self.warning_list)
        layout.addStretch()
        self._add_scroll_page(widget)

    def _build_files(self) -> None:
        widget, layout = self._page(
            "Fichiers et rapports",
            "Travaillez hors ligne sur vos captures et inventaires existants. "
            "Tous les imports restent sur cet ordinateur.",
        )
        _, body = _card(layout, "Importer une source")
        buttons = QWidget()
        row = _row(buttons)
        row.addWidget(_button("PCAP / PCAPNG", self._open_capture, primary=True))
        row.addWidget(_button("Nmap XML", self._open_nmap))
        row.addWidget(_button("Bettercap JSON", self._open_bettercap))
        row.addWidget(_button("Rapport JSON", self._open_json))
        body.addWidget(buttons)
        _, body = _card(layout, "Rapport courant")
        body.addWidget(_text("Prévisualisation en lecture seule. Les champs importés ne sont jamais exécutés.", "muted"))
        buttons = QWidget()
        row = _row(buttons)
        row.addWidget(_button("Enregistrer le rapport", self._save_report, primary=True))
        row.addStretch()
        body.addWidget(buttons)
        self.raw_report = QPlainTextEdit()
        self.raw_report.setObjectName("rawReport")
        self.raw_report.setReadOnly(True)
        self.raw_report.setMinimumHeight(360)
        self.raw_report.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        font = QFont("DejaVu Sans Mono")
        font.setPointSize(10)
        self.raw_report.setFont(font)
        body.addWidget(self.raw_report)
        layout.addStretch()
        self._add_scroll_page(widget)

    def _build_network(self) -> None:
        widget, layout = self._page(
            "Outils réseau",
            "Les observations passives et la découverte active sont séparées. "
            "Toute action réseau exige une sélection explicite.",
        )
        _, body = _card(layout, "Interfaces réseau")
        controls = QWidget()
        row = _row(controls)
        row.addWidget(_button("Actualiser les interfaces", self._refresh_interfaces))
        row.addStretch()
        body.addWidget(controls)
        self.interface_table = _table(["Interface", "État", "Adresse MAC", "Adresses IP"], 125)
        body.addWidget(self.interface_table)
        self.interface_select = QComboBox()
        self.interface_select.setMinimumWidth(160)
        body.addWidget(self.interface_select)
        _, body = _card(layout, "Capture passive", "Sélectionnez une interface, la durée et les protocoles. "
                        "Scapy et des autorisations de capture peuvent être nécessaires.")
        row_widget = QWidget()
        fields = _row(row_widget)
        self.capture_mode = QComboBox()
        self.capture_mode.addItems(["ARP uniquement", "ARP + DHCPv4 + NetBIOS"])
        self.capture_duration = QSpinBox()
        self.capture_duration.setRange(1, 600)
        self.capture_duration.setSuffix(" secondes")
        self.capture_duration.setValue(20)
        fields.addWidget(self.capture_mode, stretch=1)
        fields.addWidget(self.capture_duration)
        fields.addWidget(_button("Démarrer la capture", self._capture, primary=True))
        body.addWidget(row_widget)
        _, body = _card(layout, "Découverte des hôtes", "Découverte Nmap limitée à 256 adresses par opération.")
        row_widget = QWidget()
        fields = _row(row_widget)
        self.discovery_target = QLineEdit()
        self.discovery_target.setPlaceholderText("192.0.2.0/24")
        self.discovery_target.setAccessibleName("Adresse IP ou réseau CIDR à découvrir")
        fields.addWidget(self.discovery_target, stretch=1)
        fields.addWidget(_button("Découvrir", self._discover))
        body.addWidget(row_widget)
        _, body = _card(layout, "Inventaire des services TCP", "Une adresse IP et 32 ports TCP maximum.")
        row_widget = QWidget()
        fields = _row(row_widget)
        self.services_target = QLineEdit()
        self.services_target.setPlaceholderText("192.0.2.10")
        self.services_ports = QLineEdit("22,80,443")
        self.services_ports.setMaximumWidth(190)
        fields.addWidget(self.services_target, stretch=1)
        fields.addWidget(self.services_ports)
        fields.addWidget(_button("Analyser les ports", self._scan_services))
        body.addWidget(row_widget)
        layout.addStretch()
        self._add_scroll_page(widget)

    def _build_tls(self) -> None:
        widget, layout = self._page(
            "Inspection TLS / HTTPS",
            "Vérifiez un certificat ou analysez une capture avec des secrets de session obtenus "
            "depuis un client que vous contrôlez.",
        )
        _, body = _card(layout, "Inspection du certificat", "Une seule connexion TLS vérifiée vers la cible choisie.")
        controls = QWidget()
        row = _row(controls)
        self.tls_host = QLineEdit()
        self.tls_host.setPlaceholderText("exemple.test")
        self.tls_host.setAccessibleName("Nom d'hôte TLS")
        self.tls_port = QSpinBox()
        self.tls_port.setRange(1, 65535)
        self.tls_port.setValue(443)
        self.tls_port.setMinimumWidth(95)
        row.addWidget(self.tls_host, stretch=1)
        row.addWidget(self.tls_port)
        row.addWidget(_button("Inspecter TLS", self._inspect_tls, primary=True))
        body.addWidget(controls)

        _, body = _card(layout, "Déchiffrement hors ligne", "Fichier PCAP/PCAPNG + SSLKEYLOGFILE correspondant. "
                        "TShark est nécessaire. Aucun handshake ne révèle à lui seul les secrets TLS.")
        self.capture_file = QLineEdit()
        self.capture_file.setReadOnly(True)
        self.capture_file.setPlaceholderText("Sélectionner une capture réseau…")
        self.keylog_file = QLineEdit()
        self.keylog_file.setReadOnly(True)
        self.keylog_file.setPlaceholderText("Sélectionner le fichier de clés de session…")
        body.addWidget(self._file_picker_row(self.capture_file, self._pick_tls_capture, "Capture"))
        body.addWidget(self._file_picker_row(self.keylog_file, self._pick_keylog, "Secrets TLS"))
        self.include_uris = QCheckBox("Inclure les chemins d'URL (données potentiellement sensibles)")
        body.addWidget(self.include_uris)
        self.full_decrypt = QCheckBox("Exporter également les détails déchiffrés (fichier privé)")
        body.addWidget(self.full_decrypt)
        self.details_file = QLineEdit()
        self.details_file.setReadOnly(True)
        self.details_file.setPlaceholderText("Sélectionner un fichier de sortie lorsque l'export complet est activé…")
        body.addWidget(self._file_picker_row(self.details_file, self._pick_details, "Exporter vers"))
        controls = QWidget()
        row = _row(controls)
        row.addWidget(_button("Analyser la capture TLS", self._decrypt_tls, primary=True))
        row.addStretch()
        body.addWidget(controls)

        _, body = _card(layout, "Proxy de laboratoire local",
                        "Un proxy HTTP(S) explicite sur 127.0.0.1 uniquement. "
                        "Le navigateur de test doit être configuré manuellement.")
        controls = QWidget()
        row = _row(controls)
        row.addWidget(_text("Port local :"))
        self.proxy_port = QSpinBox()
        self.proxy_port.setRange(1024, 65535)
        self.proxy_port.setValue(8081)
        row.addWidget(self.proxy_port)
        self.proxy_button = _button("Démarrer le proxy", self._toggle_proxy)
        row.addWidget(self.proxy_button)
        row.addStretch()
        body.addWidget(controls)
        self.proxy_state = _text("Proxy arrêté · aucun certificat installé automatiquement", "muted")
        body.addWidget(self.proxy_state)
        layout.addStretch()
        self._add_scroll_page(widget)

    def _file_picker_row(self, target: QLineEdit, action: Callable, label: str) -> QWidget:
        widget = QWidget()
        row = _row(widget)
        row.addWidget(_text(label))
        row.addWidget(target, stretch=1)
        row.addWidget(_button("Parcourir…", action))
        return widget

    def _build_settings(self) -> None:
        widget, layout = self._page(
            "Paramètres",
            "Application indépendante, avec cœur Python partagé entre l'interface native "
            "et l'interface Web optionnelle.",
        )
        _, body = _card(layout, "Environnement local")
        body.addWidget(_button("Diagnostiquer les dépendances", lambda: self._launch("doctor", {})))
        self.environment_info = QPlainTextEdit()
        self.environment_info.setReadOnly(True)
        self.environment_info.setMinimumHeight(210)
        body.addWidget(self.environment_info)

        _, body = _card(layout, "Accès depuis le menu des applications (Linux)",
                        "Crée un raccourci dans le menu de votre utilisateur, sans droits administrateur.")
        body.addWidget(_button("Créer le raccourci bureau", self._install_shortcut))
        _, body = _card(layout, "Interface Web facultative (PC / serveur)",
                        "L'interface Web fonctionne même sur un serveur sans écran. "
                        "Le GUI natif ne nécessite jamais de navigateur.")
        controls = QWidget()
        row = _row(controls)
        row.addWidget(_text("Port local :"))
        self.web_port = QSpinBox()
        self.web_port.setRange(1024, 65535)
        self.web_port.setValue(8080)
        row.addWidget(self.web_port)
        self.web_button = _button("Démarrer Web local", self._toggle_web)
        row.addWidget(self.web_button)
        row.addStretch()
        body.addWidget(controls)
        self.web_state = _text(
            "Serveur Web arrêté · localhost 127.0.0.1 · aucun accès distant activé",
            "muted", wrap=True
        )
        body.addWidget(self.web_state)
        body.addWidget(_text(
            "Serveur sans GUI : subterfuge serve --port 8080. "
            "Accès distant : tunnel SSH vers l'adresse IP et le port SSH du serveur, "
            "ou proxy HTTPS authentifié. Consultez SERVER_ACCESS.md.",
            "muted", wrap=True
        ))
        _, body = _card(layout, "À propos")
        body.addWidget(_text(
            f"Subterfuge Framework {__version__} · Qt Desktop\n"
            "Analyses PCAP / Nmap / Bettercap · TLS · Diagnostics · Rapports JSON\n"
            "Données locales · Pas de télémétrie intégrée · Licence GPLv3+", "muted", wrap=True
        ))
        layout.addStretch()
        self._add_scroll_page(widget)

    def _navigate(self, index: int) -> None:
        self.pages.setCurrentIndex(index)
        self.top_title.setText(PAGE_LABELS[index][1])
        for pos, button in enumerate(self._nav_buttons):
            button.setProperty("active", index == pos)
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()

    def _render_empty(self) -> None:
        self.metric_hosts.setText("0")
        self.metric_activity.setText("0")
        self.metric_findings.setText("0")
        self.overview_source.setText("Aucun rapport ouvert")
        self.raw_report.setPlainText(
            "Aucun rapport chargé.\n\n"
            "Pour commencer : choisissez « Charger la démonstration » "
            "ou importez un fichier PCAP / PCAPNG / Nmap."
        )
        _fill_table(self.host_table, [])
        _fill_table(self.findings_table, [])
        _fill_table(self.passive_table, [])
        self.warning_list.clear()

    def _render_report(self, report: dict) -> None:
        summary = report_summary(report)
        self._report = report
        self.metric_hosts.setText(str(summary["hosts_count"]))
        self.metric_activity.setText(str(summary["activity_count"]))
        self.metric_findings.setText(str(summary["findings_count"]))
        self.overview_source.setText(f'{summary["kind"]} · {summary["source"]}')
        _fill_table(self.host_table, summary["hosts"])
        _fill_table(self.findings_table, summary["findings"])
        _fill_table(self.passive_table, summary["evidence"])
        self.warning_list.clear()
        self.warning_list.addItems(summary["warnings"])
        self.raw_report.setPlainText(report_preview(report))
        self.status.showMessage(f'Rapport prêt · {summary["source"]}')
        self._navigate(0)

    def _ask_file(self, caption: str, filters: str) -> str | None:
        file, _ = QFileDialog.getOpenFileName(self, caption, str(Path.home()), filters)
        return file or None

    def _open_capture(self) -> None:
        file = self._ask_file("Ouvrir une capture", "Captures (*.pcap *.pcapng *.cap);;Tous les fichiers (*)")
        if file:
            self._launch("import_pcap", {"file": file})

    def _open_nmap(self) -> None:
        file = self._ask_file("Ouvrir un inventaire Nmap", "XML Nmap (*.xml);;Tous les fichiers (*)")
        if file:
            self._launch("import_nmap", {"file": file})

    def _open_bettercap(self) -> None:
        file = self._ask_file("Importer les événements Bettercap", "Fichiers JSON (*.json)")
        if file:
            self._launch("import_bettercap", {"file": file})

    def _open_json(self) -> None:
        file = self._ask_file("Ouvrir un rapport Subterfuge", "Rapports JSON (*.json)")
        if file:
            self._launch("open_report", {"file": file})

    def _save_report(self) -> None:
        if self._report is None:
            self._alert("Aucun rapport", "Chargez d'abord une capture ou une démonstration.")
            return
        filename, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le rapport", str(Path.home() / "subterfuge-report.json"),
            "Rapports JSON (*.json)"
        )
        if not filename:
            return
        try:
            write_report(self._report, Path(filename))
        except (OSError, AnalysisError) as exc:
            self._alert("Enregistrement impossible", str(exc))
            return
        self.status.showMessage(f"Rapport enregistré : {filename}")

    def _refresh_interfaces(self) -> None:
        self._launch("interfaces", {})

    def _capture(self) -> None:
        interface = self.interface_select.currentData()
        if not interface:
            self._alert("Interface manquante", "Actualisez et sélectionnez une interface.")
            return
        if not self._confirm("Démarrer la capture passive",
                             f"Capturer sur {interface} pendant {self.capture_duration.value()} secondes ? "
                             "Seules les données du périmètre autorisé doivent être observées."):
            return
        action = "capture_arp" if self.capture_mode.currentIndex() == 0 else "capture_protocols"
        self._launch(action, {"interface": interface, "duration": self.capture_duration.value()})

    def _discover(self) -> None:
        target = self.discovery_target.text().strip()
        if not target:
            self._alert("Cible manquante", "Saisissez une adresse IP ou un réseau CIDR.")
            return
        if not self._confirm("Découverte active",
                             f"Lancer Nmap sur {target} ?\nConfirmez que ce réseau est autorisé."):
            return
        self._launch("discover", {"target": target})

    def _scan_services(self) -> None:
        target = self.services_target.text().strip()
        ports = self.services_ports.text().strip()
        if not target or not ports:
            self._alert("Cible manquante", "Renseignez une adresse IP et les ports TCP.")
            return
        if not self._confirm("Inventaire actif des services",
                             f"Scanner les ports {ports} de {target} ?\n"
                             "Cette opération ouvre de véritables connexions TCP."):
            return
        self._launch("scan_services", {"target": target, "ports": ports})

    def _inspect_tls(self) -> None:
        host = self.tls_host.text().strip()
        if not host:
            self._alert("Hôte manquant", "Indiquez le serveur TLS à inspecter.")
            return
        if not self._confirm("Connexion TLS",
                             f"Ouvrir une connexion de vérification vers {host}:{self.tls_port.value()} ?"):
            return
        self._launch("inspect_tls", {"host": host, "port": self.tls_port.value()})

    def _pick_tls_capture(self) -> None:
        path = self._ask_file("Capture PCAP / PCAPNG", "Captures (*.pcap *.pcapng *.cap)")
        if path:
            self.capture_file.setText(path)

    def _pick_keylog(self) -> None:
        path = self._ask_file("Secrets TLS du client autorisé", "SSLKEYLOGFILE (*.keys *.log *.txt);;Tous les fichiers (*)")
        if path:
            self.keylog_file.setText(path)

    def _pick_details(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Détails TLS déchiffrés", str(Path.home() / "subterfuge-decrypted.json"), "JSON (*.json)"
        )
        if path:
            self.details_file.setText(path)
            self.full_decrypt.setChecked(True)

    def _decrypt_tls(self) -> None:
        capture = self.capture_file.text().strip()
        keylog = self.keylog_file.text().strip()
        if not capture or not keylog:
            self._alert("Fichiers manquants", "Choisissez une capture et ses secrets de session TLS.")
            return
        if self.full_decrypt.isChecked() and not self.details_file.text().strip():
            self._alert("Export manquant", "Choisissez le fichier de destination des détails déchiffrés.")
            return
        message = ("Analyser les sessions HTTPS de cette capture avec les secrets fournis ?\n"
                   "Ces secrets et les données déchiffrées doivent provenir d'un client autorisé.")
        if self.full_decrypt.isChecked() or self.include_uris.isChecked():
            message += "\nAttention : l'export détaillé ou les URL peuvent contenir des informations sensibles."
        if not self._confirm("Déchiffrement TLS hors ligne", message):
            return
        settings = {
            "capture": capture, "keylog": keylog,
            "include_uris": self.include_uris.isChecked(),
        }
        if self.full_decrypt.isChecked():
            settings["export_decrypted_json"] = self.details_file.text().strip()
        self._launch("decrypt_tls", settings)

    def _toggle_proxy(self) -> None:
        if self._proxy is not None:
            self._stop_proxy()
            return
        if not self._confirm("Proxy HTTPS de laboratoire",
                             "Démarrer un proxy explicite sur 127.0.0.1 uniquement ?\n"
                             "Configurez vous-même le navigateur de test et la confiance CA. "
                             "Aucun trafic distant n'est redirigé automatiquement."):
            return
        try:
            from .tls_lab import proxy_command
            command = proxy_command(
                "127.0.0.1", self.proxy_port.value(), authorized_clients=True,
            )
        except (AnalysisError, OSError) as exc:
            self._alert("Proxy indisponible", str(exc))
            return
        process = QProcess(self)
        process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        process.started.connect(lambda: self._proxy_started(process))
        process.errorOccurred.connect(lambda _: self._proxy_error(process))
        process.finished.connect(lambda *_: self._proxy_finished(process))
        self._proxy = process
        self.proxy_button.setEnabled(False)
        self.proxy_state.setText("Démarrage du proxy…")
        process.start(command[0], command[1:])

    def _proxy_started(self, process: QProcess) -> None:
        if self._proxy is not process:
            return
        self.proxy_button.setEnabled(True)
        self.proxy_button.setText("Arrêter le proxy")
        self.proxy_button.setObjectName("danger")
        self.proxy_button.style().unpolish(self.proxy_button)
        self.proxy_button.style().polish(self.proxy_button)
        self.proxy_state.setText(
            f"Proxy local en cours · 127.0.0.1:{self.proxy_port.value()} · clients configurés manuellement"
        )
        self.status.showMessage("Proxy de laboratoire actif · boucle locale seulement")

    def _proxy_error(self, process: QProcess) -> None:
        if self._proxy is process:
            self.proxy_state.setText("Erreur de démarrage du proxy (consultez mitmdump / le port local).")

    def _proxy_finished(self, process: QProcess) -> None:
        if self._proxy is not process:
            return
        self._proxy = None
        self.proxy_button.setText("Démarrer le proxy")
        self.proxy_button.setObjectName("")
        self.proxy_button.setEnabled(True)
        self.proxy_button.style().unpolish(self.proxy_button)
        self.proxy_button.style().polish(self.proxy_button)
        self.proxy_state.setText("Proxy arrêté")
        self.status.showMessage("Proxy de laboratoire arrêté")
        process.deleteLater()

    def _stop_proxy(self) -> None:
        process = self._proxy
        if process is None:
            return
        if process.state() != QProcess.ProcessState.NotRunning:
            process.terminate()
            if not process.waitForFinished(1500):
                process.kill()
                process.waitForFinished(1500)
        if self._proxy is process:
            self._proxy_finished(process)

    def _toggle_web(self) -> None:
        if self._web is not None:
            self._stop_web()
            return
        process = QProcess(self)
        process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        process.started.connect(lambda: self._web_started(process))
        process.errorOccurred.connect(lambda _: self._web_error(process))
        process.finished.connect(lambda *_: self._web_finished(process))
        self._web = process
        self.web_button.setEnabled(False)
        self.web_state.setText("Démarrage du tableau de bord Web local…")
        process.start(
            sys.executable,
            ["-m", "subterfuge", "serve", "--port", str(self.web_port.value())],
        )

    def _web_started(self, process: QProcess) -> None:
        if self._web is not process:
            return
        self.web_button.setEnabled(True)
        self.web_button.setText("Arrêter Web local")
        self.web_state.setText(
            f"Web local lancé : http://127.0.0.1:{self.web_port.value()}/ "
            "· uniquement sur cet ordinateur"
        )
        self.status.showMessage("Tableau de bord Web local démarré à la demande")

    def _web_error(self, process: QProcess) -> None:
        if self._web is process:
            self.web_state.setText(
                "Erreur au démarrage du serveur Web. Vérifiez le port local."
            )

    def _web_finished(self, process: QProcess) -> None:
        if self._web is not process:
            return
        self._web = None
        self.web_button.setText("Démarrer Web local")
        self.web_button.setEnabled(True)
        self.web_state.setText("Serveur Web arrêté · localhost seulement")
        process.deleteLater()

    def _stop_web(self) -> None:
        process = self._web
        if process is None:
            return
        if process.state() != QProcess.ProcessState.NotRunning:
            process.terminate()
            if not process.waitForFinished(1800):
                process.kill()
                process.waitForFinished(1800)
        if self._web is process:
            self._web_finished(process)

    def _install_shortcut(self) -> None:
        try:
            from .desktop_shortcut import install_shortcut
            path = install_shortcut()
        except (AnalysisError, OSError, ValueError) as exc:
            self._alert("Raccourci indisponible", str(exc))
            return
        QMessageBox.information(
            self, "Raccourci créé",
            f"Subterfuge est ajouté au menu des applications :\n{path}",
        )

    def _launch(self, action: str, settings: dict) -> None:
        if self._busy:
            self._alert("Analyse en cours", "Attendez la fin de l'opération actuelle.")
            return
        self._busy = True
        job = _Job(action, settings)
        self._jobs.append(job)
        job.signals.success.connect(self._on_result)
        job.signals.failure.connect(self._on_error)
        job.signals.finished.connect(lambda: self._job_done(job))
        self.status.showMessage(f"Analyse en cours : {action}…")
        self._pool.start(job)

    def _job_done(self, job: _Job) -> None:
        if job in self._jobs:
            self._jobs.remove(job)
        self._busy = False

    def _on_error(self, message: str) -> None:
        self.status.showMessage("Opération interrompue · " + message[:180])
        self._alert("Opération impossible", message)

    def _on_result(self, result: dict) -> None:
        if result.get("desktop_kind") == "doctor":
            from json import dumps
            self.environment_info.setPlainText(dumps(result["environment"], ensure_ascii=False, indent=2))
            self.status.showMessage("Diagnostic de l'environnement terminé")
            return
        if result.get("desktop_kind") == "interfaces":
            interfaces = result["interfaces"]
            data = []
            previous = self.interface_select.currentData()
            self.interface_select.clear()
            for item in interfaces:
                data.append((
                    item.get("name", ""),
                    item.get("state", "—"),
                    item.get("mac_address", "—"),
                    ", ".join(
                        addr.get("address", "") for addr in item.get("addresses", [])[:8]
                    ) or "—",
                ))
                self.interface_select.addItem(item.get("name", "?"), item.get("name"))
            _fill_table(self.interface_table, data)
            if previous:
                found = self.interface_select.findData(previous)
                if found >= 0:
                    self.interface_select.setCurrentIndex(found)
            self.status.showMessage(f"{len(interfaces)} interface(s) trouvée(s)")
            return
        try:
            self._render_report(result)
        except AnalysisError as exc:
            self._on_error(str(exc))

    def _confirm(self, title: str, explanation: str) -> bool:
        return QMessageBox.question(
            self, title, explanation,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        ) == QMessageBox.StandardButton.Yes

    def _alert(self, title: str, explanation: str) -> None:
        QMessageBox.warning(self, title, explanation[:900])

    def closeEvent(self, event) -> None:
        if self._busy:
            self._alert("Opération en cours", "Attendez la fin de l'analyse avant de fermer.")
            event.ignore()
            return
        self._stop_proxy()
        self._stop_web()
        event.accept()


def main() -> int:
    if sys.platform.startswith("linux"):
        import os
        if not (
            os.environ.get("DISPLAY")
            or os.environ.get("WAYLAND_DISPLAY")
            or os.environ.get("QT_QPA_PLATFORM") in {"offscreen", "minimal"}
        ):
            raise AnalysisError(
                "Native desktop GUI requires a graphical session. "
                "On a headless server use: subterfuge serve --port 8080"
            )
    app = QApplication.instance()
    if app is not None and not isinstance(app, QApplication):
        raise AnalysisError("Desktop requires a Qt QApplication.")
    owner = app is None
    if owner:
        app = QApplication([])
    assert isinstance(app, QApplication)
    app.setApplicationName("Subterfuge Framework")
    app.setOrganizationName("Subterfuge")
    window = DesktopWindow()
    window.show()
    return app.exec() if owner else 0
