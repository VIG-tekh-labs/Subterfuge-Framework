"""Optional classic visual palette for the Qt desktop.

Inspired by the archived Subterfuge black/blue interface. The original
2015 JavaScript, Django runtime, attack controls and assets are deliberately
not executed or reintroduced. This only transforms trusted, bundled QSS.
"""

THEMES = ("modern", "classic")

CLASSIC_COLORS = {
    "#0A111B": "#050812",
    "#101C2B": "#0C1526",
    "#142334": "#17283C",
    "#24354A": "#354C6A",
    "#293C51": "#375272",
    "#55D6B3": "#579DF6",
    "#78E9CB": "#B8D9FF",
    "#79E7C6": "#B8D9FF",
    "#83F0D1": "#B8D9FF",
    "#A7BBD0": "#B0C8E8",
    "#1F3E40": "#203E6B",
    "#18352F": "#183453",
    "#2F6A61": "#376B9B",
    "#1C2D42": "#1D3455",
    "#294159": "#274E7B",
    "#193B35": "#224C7A",
    "#08231F": "#061629",
    "#82E8CD": "#A2C9FA",
    "#21544D": "#2A568C",
    "#297B69": "#346EA8",
}


def normalize_theme(value: object) -> str:
    """Unrecognized saved settings fall back to the established theme."""
    return value if isinstance(value, str) and value in THEMES else "modern"


def desktop_stylesheet(base: str, theme: str) -> str:
    """Keep all controls and operations identical while changing appearance."""
    if normalize_theme(theme) != "classic":
        return base
    sheet = base
    for old, new in CLASSIC_COLORS.items():
        sheet = sheet.replace(old, new)
    return sheet + """
/* Historical visual nod: black/blue panels, angular module buttons. */
QFrame#topbar { border-bottom: 2px solid #376BA5; }
QFrame#sidebar { border-right: 2px solid #294C7A; }
QFrame#card, QGroupBox#card { border-radius: 5px; }
QPushButton { border-radius: 5px; }
QPushButton#navButton[active="true"] {
    background: #213D66; border-left: 3px solid #77B8FF;
}
"""
