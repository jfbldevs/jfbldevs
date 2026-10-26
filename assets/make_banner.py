"""Draws the profile banner in a dot-matrix style, in a dark and a light variant.

Usage (from this folder): python3 make_banner.py
Writes banner-dark.svg and banner-light.svg; no fonts or external services.
"""

from pathlib import Path

GLYPHS = {  # 5x7 dot-matrix letters
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    ".": ["0", "0", "0", "0", "0", "0", "1"],
    " ": ["00", "00", "00", "00", "00", "00", "00"],
}
NAME = "JORGE F. BELTRAN"
ACCENT_ON = 14  # index of the A that carries the accent in BELTRÁN
WIDTH, HEIGHT, PITCH, RADIUS = 880, 240, 9.6, 3.4
RED = "#d71921"
THEMES = {
    "dark": {"card": "#000000", "grid": "#1c1c1c", "dot": "#ffffff", "text": "#9a9a9a"},
    "light": {"card": "#f4f4f2", "grid": "#e2e2df", "dot": "#111111", "text": "#6b6b6b"},
}


def dots():
    """Returns the (column, row) of every lit dot, accent included."""
    lit, column = [], 0
    for index, char in enumerate(NAME):
        glyph = GLYPHS[char]
        for row, line in enumerate(glyph):
            lit += [(column + x, row) for x, bit in enumerate(line) if bit == "1"]
        if index == ACCENT_ON:
            lit += [(column + 3, -2), (column + 2, -1.1)]
        column += len(glyph[0]) + 1
    return lit, column - 1


def svg(theme: dict) -> str:
    lit, columns = dots()
    x0 = (WIDTH - (columns - 1) * PITCH) / 2
    y0 = 92
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
             f'<rect width="{WIDTH}" height="{HEIGHT}" rx="22" fill="{theme["card"]}"/>']
    for gx in range(int(WIDTH / 16) + 1):  # faint background dot grid
        for gy in range(int(HEIGHT / 16) + 1):
            x, y = 12 + gx * 16, 12 + gy * 16
            if 6 < x < WIDTH - 6 and 6 < y < HEIGHT - 6:
                parts.append(f'<circle cx="{x}" cy="{y}" r="1.1" fill="{theme["grid"]}"/>')
    for col, row in lit:
        parts.append(f'<circle cx="{x0 + col * PITCH:.1f}" cy="{y0 + row * PITCH:.1f}" r="{RADIUS}" fill="{theme["dot"]}"/>')
    mono = "font-family=\"'JetBrains Mono','SF Mono',Menlo,Consolas,monospace\""
    parts += [f'<circle cx="{x0 + 4}" cy="186" r="5" fill="{RED}"/>',
              f'<text x="{x0 + 20}" y="191" {mono} font-size="14" letter-spacing="3" fill="{theme["text"]}">'
              'SENIOR SCIENTIST · BIOINFORMATICS · SOFTWARE · AI</text>',
              f'<text x="{WIDTH - x0}" y="44" {mono} font-size="12" letter-spacing="3" text-anchor="end" '
              f'fill="{theme["text"]}">[ JFB—01 ]</text>',
              "</svg>"]
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    for name, theme in THEMES.items():
        (here / f"banner-{name}.svg").write_text(svg(theme))
    print("banners written")
