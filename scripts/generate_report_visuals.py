from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "images" / "report-visuals"
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 1600
HEIGHT = 980
BG = "#f4efe6"
PANEL = "#fffdf9"
TEXT = "#1f1914"
MUTED = "#71665a"
LINE = "#ddd2c4"
ACCENT = "#201914"
ACCENT_2 = "#8a6d54"
ACCENT_3 = "#c8aa8c"


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/SourceHanSansSC-Bold.otf" if bold else "C:/Windows/Fonts/SourceHanSansSC-Medium.otf",
        "C:/Windows/Fonts/SourceHanSansSC-Bold.ttf" if bold else "C:/Windows/Fonts/SourceHanSansSC-Medium.ttf",
        "C:/Windows/Fonts/simhei.ttf" if bold else "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_SMALL = font(24)
FONT_BODY = font(30)
FONT_BODY_BOLD = font(30, True)
FONT_TITLE = font(58, True)
FONT_SUBTITLE = font(38, True)
FONT_LABEL = font(20, True)


def draw_wrapped(draw, text, xy, width, font_obj, fill, line_gap=10):
    chars = list(text)
    lines = []
    current = ""
    for ch in chars:
        test = current + ch
        if draw.textlength(test, font=font_obj) <= width:
            current = test
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)

    x, y = xy
    line_height = font_obj.size + line_gap
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += line_height
    return y


def base_canvas():
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    grid = 44
    for x in range(0, WIDTH, grid):
        draw.line((x, 0, x, HEIGHT), fill="#efe6da", width=1)
    for y in range(0, HEIGHT, grid):
        draw.line((0, y, WIDTH, y), fill="#efe6da", width=1)
    return image, draw


def rounded(draw, box, radius=30, fill=PANEL, outline=LINE, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def report_header(draw, title, subtitle):
    rounded(draw, (72, 56, WIDTH - 72, 210), radius=34, fill=PANEL)
    draw.text((110, 92), title, font=FONT_TITLE, fill=TEXT)
    draw.text((112, 160), subtitle, font=FONT_SMALL, fill=MUTED)


def badge(draw, x, y, text, fill="#f7efe5"):
    w = int(draw.textlength(text, font=FONT_LABEL)) + 34
    draw.rounded_rectangle((x, y, x + w, y + 42), radius=20, fill=fill, outline=LINE, width=1)
    draw.text((x + 16, y + 10), text, font=FONT_LABEL, fill=MUTED)
    return x + w + 12


def card_title(draw, x, y, kicker, title):
    draw.text((x, y), kicker, font=FONT_LABEL, fill=MUTED)
    draw.text((x, y + 34), title, font=FONT_SUBTITLE, fill=TEXT)


def bar(draw, x, y, label, value, pct, color):
    draw.text((x, y), label, font=FONT_BODY, fill=TEXT)
    draw.text((x + 500, y), value, font=FONT_BODY_BOLD, fill=TEXT)
    draw.rounded_rectangle((x, y + 46, x + 610, y + 66), radius=10, fill="#efe6da")
    draw.rounded_rectangle((x, y + 46, x + int(610 * pct), y + 66), radius=10, fill=color)


def bubble(draw, x, y, r, color, label, caption):
    draw.ellipse((x - r, y - r, x + r, y + r), fill=color, outline=PANEL, width=4)
    tw = draw.textlength(label, font=FONT_BODY_BOLD)
    draw.text((x - tw / 2, y - 18), label, font=FONT_BODY_BOLD, fill="#fffdf9")
    cw = draw.textlength(caption, font=FONT_LABEL)
    draw.text((x - cw / 2, y + r + 14), caption, font=FONT_LABEL, fill=MUTED)


def create_voc():
    image, draw = base_canvas()
    report_header(draw, "VOC Priority Summary", "把用户原声转成产品优先级的研究摘要页")
    x = badge(draw, 112, 232, "Consumer Voice")
    x = badge(draw, x, 232, "Product Prioritization")
    badge(draw, x, 232, "Mobility Research")

    rounded(draw, (86, 302, 842, 892))
    card_title(draw, 122, 338, "TOP ISSUES", "用户最在意的四个变量")
    bar(draw, 122, 430, "电池续航与寿命", "91", 0.91, ACCENT)
    bar(draw, 122, 545, "组装难易度", "83", 0.83, ACCENT_2)
    bar(draw, 122, 660, "价格与性价比", "79", 0.79, ACCENT_3)
    bar(draw, 122, 775, "舒适度与骑行体验", "74", 0.74, "#d2baa3")

    rounded(draw, (876, 302, 1512, 892))
    card_title(draw, 912, 338, "INSIGHT", "行业用户与平台用户的差异")
    draw.line((1194, 392, 1194, 836), fill=LINE, width=2)
    draw.text((932, 430), "行业消费者", font=FONT_SUBTITLE, fill=TEXT)
    draw_wrapped(draw, "性能、速率、减震、制动与助力体验是更核心的决策变量。", (932, 488), 220, FONT_BODY, MUTED)
    draw.text((1228, 430), "平台消费者", font=FONT_SUBTITLE, fill=TEXT)
    draw_wrapped(draw, "更重视性价比、续航、组装难度与到手使用效率。", (1228, 488), 220, FONT_BODY, MUTED)
    draw_wrapped(draw, "同一个品类，行业平均打法不能直接照搬到 Amazon 平台。研究真正要解决的是：哪些变量应该先被产品、客服与运营共同处理。", (932, 668), 520, FONT_BODY, MUTED)
    image.save(OUT_DIR / "voc-report-board.png")


def create_eu():
    image, draw = base_canvas()
    report_header(draw, "EU Bathroom Market Dashboard", "五国站点、品类优先级与新品结构的一页式看板")
    x = badge(draw, 112, 232, "Germany First")
    x = badge(draw, x, 232, "Category Lens")
    badge(draw, x, 232, "EU Marketplace")

    rounded(draw, (86, 302, 812, 892))
    card_title(draw, 122, 338, "COUNTRY MAP", "国家规模与价格带关系")
    draw.line((170, 796, 710, 796), fill=LINE, width=2)
    draw.line((170, 430, 170, 796), fill=LINE, width=2)
    draw.line((170, 610, 710, 610), fill="#eadfce", width=2)
    draw.line((440, 430, 440, 796), fill="#eadfce", width=2)
    bubble(draw, 594, 490, 78, ACCENT, "DE", "€7.3M / 高价高量")
    bubble(draw, 510, 602, 58, ACCENT_2, "UK", "€6.4M / 次主站点")
    bubble(draw, 350, 668, 42, ACCENT_3, "FR", "延展市场")
    bubble(draw, 286, 726, 34, "#d3b89d", "ES", "后置进入")
    bubble(draw, 392, 758, 30, "#e2d2c3", "IT", "复制站点")
    draw.text((250, 818), "平均价格水平", font=FONT_LABEL, fill=MUTED)

    rounded(draw, (846, 302, 1512, 892))
    card_title(draw, 882, 338, "CATEGORY PRIORITY", "应该先看的德国核心品类")
    bar(draw, 882, 430, "厨房龙头", "€6.1M", 1.0, ACCENT)
    bar(draw, 882, 545, "手持花洒", "€0.8M", 0.67, ACCENT_2)
    bar(draw, 882, 660, "淋浴系统", "€0.7M", 0.66, ACCENT_3)
    bar(draw, 882, 775, "面盆龙头", "€0.3M", 0.58, "#d2baa3")
    image.save(OUT_DIR / "eu-bathroom-report-board.png")


def create_country():
    image, draw = base_canvas()
    report_header(draw, "Market Entry Decision Map", "泰国、墨西哥、英国的进入优先级比较")
    x = badge(draw, 112, 232, "Entry Strategy")
    x = badge(draw, x, 232, "Country Comparison")
    badge(draw, x, 232, "Cross-border E-commerce")

    rounded(draw, (86, 302, 1512, 892))
    card_title(draw, 122, 338, "COUNTRY ENTRY MAP", "看规模、成熟度、增速与执行难度的综合位置")
    draw.line((210, 796, 1390, 796), fill=LINE, width=2)
    draw.line((210, 430, 210, 796), fill=LINE, width=2)
    draw.line((210, 610, 1390, 610), fill="#eadfce", width=2)
    draw.line((800, 430, 800, 796), fill="#eadfce", width=2)
    bubble(draw, 690, 540, 60, ACCENT, "TH", "内容驱动试水")
    bubble(draw, 590, 480, 74, "#8a5a3c", "MX", "高增长高难度")
    bubble(draw, 1080, 602, 92, "#bea287", "UK", "成熟稳健大市场")
    draw_wrapped(draw, "TH：社媒与直播电商增长快，适合验证高传播型品类。", (250, 822), 350, FONT_SMALL, MUTED)
    draw_wrapped(draw, "MX：需求扩张强，但物流与尾程决定是否真正适合进入。", (646, 822), 350, FONT_SMALL, MUTED)
    draw_wrapped(draw, "UK：规模最大、成熟度高，更适合有纪律的站点进入。", (1046, 822), 350, FONT_SMALL, MUTED)
    image.save(OUT_DIR / "country-entry-report-board.png")


def create_mobility():
    image, draw = base_canvas()
    report_header(draw, "Senior Mobility Segment Scan", "三轮车、四轮代步车与电动轮椅的进入判断页")
    x = badge(draw, 112, 232, "Segment Comparison")
    x = badge(draw, x, 232, "Opportunity Filter")
    badge(draw, x, 232, "Amazon US")

    rounded(draw, (86, 302, 812, 892))
    card_title(draw, 122, 338, "SEGMENT MAP", "谁值得优先进入")
    draw.line((170, 796, 710, 796), fill=LINE, width=2)
    draw.line((170, 430, 170, 796), fill=LINE, width=2)
    draw.line((170, 610, 710, 610), fill="#eadfce", width=2)
    draw.line((440, 430, 440, 796), fill="#eadfce", width=2)
    bubble(draw, 356, 706, 46, "#7d6550", "TRIKE", "$1105 / 小众")
    bubble(draw, 556, 596, 58, ACCENT, "SCOOTER", "优先进入")
    bubble(draw, 386, 476, 68, "#be9e84", "WHEELCHAIR", "容量大但高门槛")

    rounded(draw, (846, 302, 1512, 892))
    card_title(draw, 882, 338, "WHY IT MATTERS", "三个赛道的判断逻辑完全不同")
    draw_wrapped(draw, "电动三轮车：客单价高，但市场容量小，更适合差异化和内容打法。", (882, 440), 560, FONT_BODY, MUTED)
    draw_wrapped(draw, "四轮代步车：容量足够、价格带适中、集中度低，是最均衡的优先观察点。", (882, 570), 560, FONT_BODY, MUTED)
    draw_wrapped(draw, "电动轮椅：销量与客单价都高，但监管、售后和产品复杂度显著更高，不适合轻装试错。", (882, 700), 560, FONT_BODY, MUTED)
    image.save(OUT_DIR / "senior-mobility-report-board.png")


def main():
    create_voc()
    create_eu()
    create_country()
    create_mobility()


if __name__ == "__main__":
    main()
