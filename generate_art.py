#!/usr/bin/env python3
"""
Génère un pixel art SVG aléatoire (symétrique, façon "invader")
et l'enregistre dans art/today.svg
"""

import random
import datetime
from pathlib import Path

# --- Configuration ---
GRID_WIDTH = 8          # largeur de la moitié gauche (sera reflétée)
GRID_HEIGHT = 8
PIXEL_SIZE = 30
FILL_PROBABILITY = 0.45  # chance qu'un pixel soit "allumé"

PALETTES = [
    ["#0d1117", "#39d353", "#26a641", "#006d32"],   # thème "GitHub green"
    ["#1a1b27", "#ff79c6", "#bd93f9", "#8be9fd"],   # thème "dracula"
    ["#0f1021", "#f72585", "#7209b7", "#3a0ca3"],   # thème "neon"
    ["#101820", "#f2a541", "#e94f37", "#393e46"],   # thème "sunset"
]

QUOTES = [
    "Code today, debug tomorrow.",
    "Ship it.",
    "It works on my machine.",
    "One commit at a time.",
    "Semper fi, semper git push.",
    "404: motivation not found (retrying...)",
    "git commit -m \"fix everything\"",
]


def seeded_random():
    """Seed basé sur la date du jour -> même art toute la journée, différent chaque jour."""
    today = datetime.date.today().isoformat()
    rng = random.Random(today)
    return rng, today


def generate_grid(rng):
    bg, *colors = rng.choice(PALETTES)
    half = [
        [rng.random() < FILL_PROBABILITY for _ in range(GRID_WIDTH)]
        for _ in range(GRID_HEIGHT)
    ]
    return bg, colors, half


def build_svg(bg, colors, half, quote):
    full_width = GRID_WIDTH * 2
    svg_w = full_width * PIXEL_SIZE
    svg_h = GRID_HEIGHT * PIXEL_SIZE + 50  # + espace pour la citation

    rects = []
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if half[y][x]:
                color = random.Random(f"{x}-{y}-{bg}").choice(colors)
                # pixel gauche
                rects.append(
                    f'<rect x="{x*PIXEL_SIZE}" y="{y*PIXEL_SIZE}" '
                    f'width="{PIXEL_SIZE}" height="{PIXEL_SIZE}" fill="{color}"/>'
                )
                # pixel miroir (droite)
                mirror_x = full_width - 1 - x
                rects.append(
                    f'<rect x="{mirror_x*PIXEL_SIZE}" y="{y*PIXEL_SIZE}" '
                    f'width="{PIXEL_SIZE}" height="{PIXEL_SIZE}" fill="{color}"/>'
                )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">
  <rect width="100%" height="100%" fill="{bg}"/>
  {''.join(rects)}
  <text x="{svg_w/2}" y="{GRID_HEIGHT*PIXEL_SIZE + 30}" font-family="monospace"
        font-size="14" fill="#ffffff" text-anchor="middle">{quote}</text>
</svg>'''
    return svg


def main():
    rng, today = seeded_random()
    bg, colors, half = generate_grid(rng)
    quote = rng.choice(QUOTES)
    svg = build_svg(bg, colors, half, quote)

    out_dir = Path("art")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "today.svg"
    out_path.write_text(svg, encoding="utf-8")

    print(f"Pixel art généré pour le {today} -> {out_path}")


if __name__ == "__main__":
    main()
