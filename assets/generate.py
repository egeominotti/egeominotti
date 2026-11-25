#!/usr/bin/env python3
"""Generate the profile README's header: what I do, and one isometric block per
project, as tall as its GitHub stars.

Run `python3 assets/generate.py` from the repository root after changing STARS.
The SVG is static and self-contained (no fonts, scripts or filters), and has
its own dark background, so it reads the same on GitHub's light and dark themes.
"""

from math import cos, radians, sin, sqrt
from pathlib import Path

OUT = Path(__file__).resolve().parent / "header.svg"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"

NIGHT, WALL, TEXT, PINK = "#0b0920", "#15123a", "#f3f1ff", "#ff3d9a"
ROLES = ["Software engineer", "Blockchain developer", "AI agent builder"]

# Most starred first: (stars, colour of the block).
STARS = {
    "bunqueue": (597, PINK),
    "binja": (27, "#2de2ff"),
    "flashq": (25, "#ff7847"),
    "bunqueue-dashboard": (18, "#5c9dff"),
    "bunpilot": (5, "#3dffa8"),
    "agentvm": (3, "#a08cff"),
}

def mix(a: str, b: str, t: float) -> str:
    pa, pb = (int(a[i:i + 2], 16) for i in (1, 3, 5)), (int(b[i:i + 2], 16) for i in (1, 3, 5))
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(pa, pb))


def block(ox: float, oy: float, s: float, x: float, size: float, height: float, color: str) -> str:
    """An isometric block standing at `x` along the row: three faces and a lit outline."""
    c, k = cos(radians(30)), sin(radians(30))

    def p(px, py, pz=0.0):
        return f"{ox + (px - py) * c * s:.1f} {oy + (px + py) * k * s - pz * s:.1f}"

    x1, y1, z = x + size, size, height
    left = f"M{p(x, y1, z)}L{p(x1, y1, z)}L{p(x1, y1)}L{p(x, y1)}Z"
    right = f"M{p(x1, y1, z)}L{p(x1, 0, z)}L{p(x1, 0)}L{p(x1, y1)}Z"
    top = f"M{p(x, 0, z)}L{p(x1, 0, z)}L{p(x1, y1, z)}L{p(x, y1, z)}Z"
    return (
        f'<path d="{left}" fill="{mix(WALL, color, 0.2)}"/><path d="{right}" fill="{mix(NIGHT, color, 0.1)}"/>'
        f'<path d="{top}" fill="{mix(WALL, color, 0.45)}"/>'
        f'<path d="{left}{right}{top}" fill="none" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>'
    )


def main() -> None:
    w, h = 1200, 240
    most = max(count for count, _ in STARS.values())
    blocks, x = "", 0.0
    for count, color in sorted(STARS.values(), key=lambda item: -item[0]):
        blocks += block(930, 102, 16, x, 1.6, 0.7 + 4.2 * sqrt(count / most), color)
        x += 2.3
    title = ", ".join(ROLES)
    roles = "".join(
        f'<text x="64" y="{88 + i * 46}" font-family="{SANS}" font-size="34" font-weight="600" fill="{TEXT}">{role}</text>'
        for i, role in enumerate(ROLES)
    )
    OUT.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">\n'
        f"<title>{title}</title>\n"
        f'<rect width="{w}" height="{h}" rx="14" fill="{NIGHT}"/>\n'
        f'<rect x="40" y="58" width="4" height="128" rx="2" fill="{PINK}"/>\n'
        f"{roles}\n{blocks}\n</svg>\n"
    )


if __name__ == "__main__":
    main()
