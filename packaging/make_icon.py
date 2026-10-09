"""Generate self-authored Windows ICO asset using Pillow at build time."""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "subterfuge.ico"


def main() -> None:
    base = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle((7, 7, 249, 249), radius=52,
                           fill="#112433", outline="#67e0bc", width=7)
    # The badge uses vector-like primitive drawing, with no bundled font asset.
    draw.arc((52, 42, 205, 214), start=190, end=355, fill="#67e0bc", width=23)
    draw.arc((52, 42, 205, 214), start=10, end=175, fill="#67e0bc", width=23)
    draw.ellipse((208, 46, 230, 68), fill="#9effde")
    base.save(TARGET, format="ICO", sizes=[
        (16, 16), (24, 24), (32, 32), (48, 48),
        (64, 64), (128, 128), (256, 256),
    ])
    print("ICON_CREATED", TARGET, TARGET.stat().st_size)


if __name__ == "__main__":
    main()
