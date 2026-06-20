from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "images" / "favicons"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SIZE = 256
BG = "#f4efe6"
INK = "#181411"
MUTED = "#6c6257"
ACCENT = "#d87437"
PANEL = "#fffdf9"
LINE = "#ddd2c4"


def load_font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/SourceHanSansSC-Bold.ttf" if bold else "C:/Windows/Fonts/SourceHanSansSC-Medium.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_BIG = load_font(118, True)
FONT_MED = load_font(84, True)
FONT_UI = load_font(30, True)
FONT_SMALL = load_font(24, False)


def canvas():
    return Image.new("RGBA", (SIZE, SIZE), BG)


def center_text(draw, text, font, fill, x, y):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text((x - w / 2, y - h / 2), text, font=font, fill=fill)


def option_1():
    image = canvas()
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((18, 18, 238, 238), radius=56, fill=PANEL, outline=LINE, width=3)
    center_text(draw, "W", FONT_BIG, INK, 128, 132)
    image.save(OUT_DIR / "favicon-option-1.png")


def option_2():
    image = canvas()
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((20, 20, 236, 236), radius=52, fill=INK)
    draw.rounded_rectangle((48, 48, 208, 208), radius=42, outline=ACCENT, width=6)
    center_text(draw, "W", FONT_MED, PANEL, 128, 134)
    image.save(OUT_DIR / "favicon-option-2.png")


def option_3():
    image = canvas()
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((18, 18, 238, 238), radius=64, fill=PANEL, outline=LINE, width=3)
    draw.rounded_rectangle((62, 62, 194, 194), radius=34, fill=ACCENT)
    center_text(draw, "W", FONT_MED, PANEL, 128, 132)
    image.save(OUT_DIR / "favicon-option-3.png")


def option_4():
    image = canvas()
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((18, 18, 238, 238), radius=48, fill=PANEL, outline=LINE, width=3)
    draw.line((58, 198, 198, 58), fill=ACCENT, width=8)
    center_text(draw, "WW", FONT_UI, INK, 108, 104)
    center_text(draw, "WIKI", FONT_SMALL, MUTED, 136, 154)
    image.save(OUT_DIR / "favicon-option-4.png")


def main():
    option_1()
    option_2()
    option_3()
    option_4()


if __name__ == "__main__":
    main()
