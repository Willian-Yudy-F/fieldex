"""
FielDex - Daily Knowledge Card Generator
=========================================
Gotta learn 'em all. Generates a Pokedex-style trading card (1080x1350)
for one knowledge entry, ready to post on Instagram / LinkedIn.

Usage:
    python generate_card.py            # generates the latest entry in fieldex.json
    python generate_card.py 2          # generates the card for entry id=2
    python generate_card.py --all      # regenerates every card

Output: cards/fieldex_<id>_<slug>.png
"""

import json
import sys
import re
import textwrap
import unicodedata
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Circle
    import matplotlib.patheffects as pe
    HAS_MPL = True
except ModuleNotFoundError:
    from PIL import Image, ImageDraw, ImageFont
    HAS_MPL = False

ROOT = Path(__file__).parent
DEX = ROOT / "fieldex.json"
OUT = ROOT / "cards"
OUT.mkdir(exist_ok=True)

# Each category is a "type" with its own colour identity (like Pokemon types)
TYPES = {
    "probability": {"color": "#00d4ff", "glow": "#0a2a3a", "icon": "%"},
    "math":        {"color": "#ef476f", "glow": "#3a0a18", "icon": "x"},
    "logic":       {"color": "#06d6a0", "glow": "#0a3a2a", "icon": ">"},
    "history":     {"color": "#ffb703", "glow": "#3a2a0a", "icon": "H"},
    "geography":   {"color": "#8ecae6", "glow": "#1a2a3a", "icon": "G"},
    "data":        {"color": "#c77dff", "glow": "#2a0a3a", "icon": "#"},
    "security":    {"color": "#9ad17b", "glow": "#15301d", "icon": "S"},
    "corinthians": {"color": "#ffffff", "glow": "#1a1a1a", "icon": "C"},
    "worldcup":    {"color": "#2dd4bf", "glow": "#0f2f2d", "icon": "W"},
    "football":    {"color": "#74c69d", "glow": "#102d1c", "icon": "XI"},
}
DEFAULT_TYPE = {"color": "#adb5bd", "glow": "#22252a", "icon": "?"}

RARITY = {
    "common":   ("COMMON",   "#adb5bd", 1),
    "uncommon": ("UNCOMMON", "#06d6a0", 2),
    "rare":     ("RARE",     "#00d4ff", 3),
    "epic":     ("EPIC",     "#c77dff", 4),
    "legendary":("LEGENDARY","#ffb703", 5),
}

BG = "#0b0f14"
PANEL = "#121821"
TEXT = "#e9ecef"
MUTED = "#6c757d"


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:30]


def type_label(category):
    return {"worldcup": "WORLD CUP"}.get(category, category.upper())


def hex_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def blend(a, b, amount):
    ar, ag, ab = hex_rgb(a)
    br, bg, bb = hex_rgb(b)
    return (
        int(ar + (br - ar) * amount),
        int(ag + (bg - ag) * amount),
        int(ab + (bb - ab) * amount),
    )


def pillow_font(size, bold=False, mono=False):
    if mono:
        candidates = ["/System/Library/Fonts/Menlo.ttc"]
    elif bold:
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        ]
    else:
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        ]
    for candidate in candidates:
        if Path(candidate).exists():
            try:
                return ImageFont.truetype(candidate, size=size)
            except OSError:
                pass
    return ImageFont.load_default()


def text_wh(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def wrap_px(draw, text, font, max_width):
    lines = []
    for paragraph in str(text).splitlines() or [""]:
        words = paragraph.split()
        current = ""
        for word in words:
            trial = f"{current} {word}".strip()
            if current and text_wh(draw, trial, font)[0] > max_width:
                lines.append(current)
                current = word
            else:
                current = trial
        if current:
            lines.append(current)
    return lines or [""]


def draw_center(draw, box, text, font, fill):
    w, h = text_wh(draw, text, font)
    x = box[0] + (box[2] - box[0] - w) / 2
    y = box[1] + (box[3] - box[1] - h) / 2
    draw.text((x, y), text, font=font, fill=fill)


def draw_lines(draw, x, y, lines, font, fill, line_gap):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y


def draw_card_pillow(entry):
    t = TYPES.get(entry["category"], DEFAULT_TYPE)
    color, glow, icon = t["color"], t["glow"], t["icon"]
    rar_label, rar_color, rar_stars = RARITY.get(entry.get("rarity", "common"))

    W, H = 1080, 1350
    img = Image.new("RGB", (W, H), hex_rgb(BG))
    draw = ImageDraw.Draw(img)

    card = [42, 42, 1038, 1308]
    draw.rounded_rectangle(card, radius=36, fill=hex_rgb(PANEL), outline=hex_rgb(color), width=5)

    title_font = pillow_font(46, bold=True)
    title_lines = wrap_px(draw, entry["title"], title_font, 720)
    band_bottom = 410 + max(0, len(title_lines) - 1) * 58
    draw.rounded_rectangle([62, 62, 1018, band_bottom], radius=24, fill=blend(PANEL, glow, 0.76))

    mono_46 = pillow_font(46, bold=True, mono=True)
    badge_font = pillow_font(24, bold=True)
    icon_font = pillow_font(34, bold=True)
    draw.text((90, 105), f"#{entry['id']:03d}", font=mono_46, fill=hex_rgb(color))
    badge = [720, 96, 970, 164]
    draw.rounded_rectangle(badge, radius=28, fill=hex_rgb(color))
    draw_center(draw, badge, type_label(entry["category"]), badge_font, hex_rgb(BG))
    draw.ellipse([105, 214, 195, 304], fill=hex_rgb(color))
    draw_center(draw, [105, 214, 195, 304], icon, icon_font, hex_rgb(BG))

    title_y = 205
    draw_lines(draw, 240, title_y, title_lines, title_font, hex_rgb(TEXT), 12)

    rarity_y = max(342, title_y + len(title_lines) * 58 + 24)
    star_font = pillow_font(30, bold=True, mono=True)
    label_font = pillow_font(22, bold=True)
    star_str = "*" * rar_stars + "-" * (5 - rar_stars)
    draw.text((90, rarity_y), star_str, font=star_font, fill=hex_rgb(rar_color))
    draw.text((310, rarity_y + 6), rar_label, font=label_font, fill=hex_rgb(rar_color))

    label_font = pillow_font(23, bold=True)
    fact_font = pillow_font(30)
    why_font = pillow_font(27)
    fact_top = rarity_y + 72
    fact_lines = wrap_px(draw, entry["fact"], fact_font, 830)
    fact_h = 86 + len(fact_lines) * 42
    draw.rounded_rectangle([90, fact_top, 990, fact_top + fact_h], radius=20,
                           fill=hex_rgb(BG), outline=hex_rgb(MUTED), width=2)
    draw.text((132, fact_top + 30), "FACT", font=label_font, fill=hex_rgb(color))
    draw_lines(draw, 132, fact_top + 72, fact_lines, fact_font, hex_rgb(TEXT), 12)

    why_top = fact_top + fact_h + 42
    why_lines = wrap_px(draw, entry["why"], why_font, 840)
    why_h = 82 + len(why_lines) * 38
    draw.rounded_rectangle([90, why_top, 990, why_top + why_h], radius=20,
                           fill=blend(PANEL, glow, 0.72))
    draw.text((132, why_top + 28), "WHY IT MATTERS", font=pillow_font(22, bold=True),
              fill=hex_rgb(color))
    draw_lines(draw, 132, why_top + 68, why_lines, why_font, hex_rgb("#ced4da"), 11)

    tag_y = min(why_top + why_h + 48, 1138)
    tag_font = pillow_font(21, mono=True)
    x = 132
    for tag in entry.get("tags", [])[:4]:
        label = f"#{tag}"
        tw, _ = text_wh(draw, label, tag_font)
        width = tw + 34
        if x + width > 950:
            break
        draw.rounded_rectangle([x, tag_y, x + width, tag_y + 46], radius=16,
                               outline=hex_rgb(MUTED), width=2)
        draw_center(draw, [x, tag_y, x + width, tag_y + 46], label, tag_font, hex_rgb(MUTED))
        x += width + 18

    draw.text((90, 1230), "FielDex", font=pillow_font(38, bold=True), fill=hex_rgb(color))
    draw.text((90, 1276), "gotta learn 'em all", font=pillow_font(20), fill=hex_rgb(MUTED))
    date_font = pillow_font(22, mono=True)
    date_w, _ = text_wh(draw, entry["date"], date_font)
    draw.text((990 - date_w, 1260), entry["date"], font=date_font, fill=hex_rgb(MUTED))

    fname = OUT / f"fieldex_{entry['id']:03d}_{slug(entry['title'])}.png"
    img.save(fname)
    print(f"  captured -> {fname.name}")
    return fname


def draw_card(entry):
    if not HAS_MPL:
        return draw_card_pillow(entry)

    t = TYPES.get(entry["category"], DEFAULT_TYPE)
    color, glow, icon = t["color"], t["glow"], t["icon"]
    rar_label, rar_color, rar_stars = RARITY.get(entry.get("rarity", "common"))

    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 125)
    ax.axis("off")

    # Outer card frame with type-coloured border
    ax.add_patch(FancyBboxPatch((4, 4), 92, 117,
                 boxstyle="round,pad=1.5,rounding_size=3",
                 fc=PANEL, ec=color, lw=4, zorder=1))
    # subtle inner glow band (height adapts to title length below)
    title_n = len(textwrap.wrap(entry["title"], width=24))
    band_bot = 86 - (title_n - 1) * 5.5
    ax.add_patch(FancyBboxPatch((6, band_bot), 88, 116 - band_bot,
                 boxstyle="round,pad=1,rounding_size=2",
                 fc=glow, ec="none", zorder=2))

    # --- HEADER: dex number + type badge ---
    ax.text(9, 113, f"#{entry['id']:03d}", color=color, fontsize=26,
            fontweight="bold", va="center", family="monospace", zorder=5)

    # type badge (pill)
    ax.add_patch(FancyBboxPatch((68, 110), 24, 6,
                 boxstyle="round,pad=0.6,rounding_size=3",
                 fc=color, ec="none", zorder=5))
    ax.text(80, 113, type_label(entry["category"]), color=BG, fontsize=12.5,
            fontweight="bold", ha="center", va="center", zorder=6)

    # type icon coin
    ax.add_patch(Circle((15, 103), 4.5, fc=color, ec="none", zorder=5))
    ax.text(15, 103, icon, color=BG, fontsize=18, fontweight="bold",
            ha="center", va="center", zorder=6)

    # --- TITLE ---
    title_lines = textwrap.wrap(entry["title"], width=24)
    ty = 99
    for line in title_lines:
        ax.text(24, ty, line, color=TEXT, fontsize=23, fontweight="bold",
                va="center", zorder=6)
        ty -= 5.5

    # rarity stars (placed below whichever is lower: icon coin or title)
    rar_y = min(92, ty - 1)
    star_str = "*" * rar_stars + "-" * (5 - rar_stars)
    ax.text(9, rar_y, star_str, color=rar_color, fontsize=16,
            family="monospace", va="center", zorder=6)
    ax.text(30, rar_y, rar_label, color=rar_color, fontsize=11,
            fontweight="bold", va="center", zorder=6)

    # --- FACT BOX (height scales with wrapped text) ---
    fact_w = textwrap.wrap(entry["fact"], width=44)
    fact_h = 9 + len(fact_w) * 3.4          # header + lines
    fact_top = min(84, rar_y - 6)
    fact_bot = fact_top - fact_h
    ax.add_patch(FancyBboxPatch((9, fact_bot), 82, fact_h,
                 boxstyle="round,pad=1,rounding_size=2",
                 fc=BG, ec=MUTED, lw=1, zorder=3))
    ax.text(13, fact_top - 3, "FACT", color=color, fontsize=11.5,
            fontweight="bold", va="top", zorder=5)
    ax.text(13, fact_top - 7, "\n".join(fact_w), color=TEXT, fontsize=13.5,
            va="top", linespacing=1.5, zorder=5)

    # --- WHY BOX (sits just below the fact box) ---
    why_w = textwrap.wrap(entry["why"], width=46)
    why_h = 8.5 + len(why_w) * 3.1
    why_top = fact_bot - 4
    why_bot = why_top - why_h
    ax.add_patch(FancyBboxPatch((9, why_bot), 82, why_h,
                 boxstyle="round,pad=1,rounding_size=2",
                 fc=glow, ec="none", zorder=3))
    ax.text(13, why_top - 3, "WHY IT MATTERS", color=color, fontsize=11,
            fontweight="bold", va="top", zorder=5)
    ax.text(13, why_top - 6.8, "\n".join(why_w), color="#ced4da",
            fontsize=12, va="top", linespacing=1.45, zorder=5)

    # --- TAGS (below why box) ---
    tx = 13
    tag_y = why_bot - 6
    for tag in entry.get("tags", [])[:4]:
        w = 3 + len(tag) * 1.7
        ax.add_patch(FancyBboxPatch((tx, tag_y), w, 4.5,
                     boxstyle="round,pad=0.4,rounding_size=2",
                     fc="none", ec=MUTED, lw=1, zorder=4))
        ax.text(tx + w / 2, tag_y + 2.2, f"#{tag}", color=MUTED, fontsize=9,
                ha="center", va="center", zorder=5)
        tx += w + 2.5

    # --- FOOTER ---
    ax.text(9, 9, "FielDex", color=color, fontsize=18, fontweight="bold",
            va="center", zorder=5,
            path_effects=[pe.withStroke(linewidth=0.5, foreground=color)])
    ax.text(9, 6, "gotta learn 'em all", color=MUTED, fontsize=10,
            style="italic", va="center", zorder=5)
    ax.text(91, 7.5, entry["date"], color=MUTED, fontsize=10,
            ha="right", va="center", family="monospace", zorder=5)

    fname = OUT / f"fieldex_{entry['id']:03d}_{slug(entry['title'])}.png"
    plt.savefig(fname, facecolor=BG, dpi=100)
    plt.close(fig)
    print(f"  captured -> {fname.name}")
    return fname


def main():
    data = json.loads(DEX.read_text(encoding="utf-8"))
    entries = data["entries"]

    if "--all" in sys.argv:
        targets = entries
    elif len(sys.argv) > 1 and sys.argv[1].isdigit():
        wanted = int(sys.argv[1])
        targets = [e for e in entries if e["id"] == wanted]
        if not targets:
            print(f"No entry with id={wanted}")
            return
    else:
        targets = [max(entries, key=lambda e: e["id"])]

    print(f"FielDex - generating {len(targets)} card(s):")
    for e in targets:
        draw_card(e)


if __name__ == "__main__":
    main()
