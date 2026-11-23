#!/usr/bin/env python3
"""Draw the 22 Nov 2026 world-news front page: six region panels.

Layout (1024x1024): masthead, number strip, 3 heroes, small pinned map,
six region panels (3x2), NOT YET strip, date-check footer.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (164, 18, 32)
NAVY = (31, 51, 80)
GOLD = (212, 165, 60)
GREEN = (34, 120, 60)
AMBER = (176, 120, 10)
BLUE = (40, 90, 160)
GRAY = (110, 105, 95)
PANEL_BG = (255, 252, 244)

FD = "/usr/share/fonts/truetype/dejavu/"


def f(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF_B = lambda s: f("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: f("DejaVuSans.ttf", s)
SANS_B = lambda s: f("DejaVuSans-Bold.ttf", s)


def fit(text, font, max_w, draw):
    """Truncate text with an ellipsis so it fits max_w pixels."""
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "\u2026", font=font) > max_w:
        text = text[:-1]
    return text + "\u2026"


def wrap(text, font, max_w, draw, max_lines=2):
    """Greedy wrap; if text still overflows the last line, ellipsis-truncate it."""
    words = text.split()
    lines, cur, idx = [], "", 0
    while idx < len(words):
        w = words[idx]
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
            idx += 1
        else:
            if cur:
                lines.append(cur)
                cur = ""
                if len(lines) == max_lines:
                    remaining = " ".join(words[idx:])
                    lines[-1] = fit(lines[-1] + " " + remaining, font, max_w, draw)
                    return lines
            else:
                lines.append(fit(w, font, max_w, draw))
                idx += 1
                if len(lines) == max_lines:
                    return lines
    if cur and len(lines) < max_lines:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- top red rule ----
d.rectangle([0, 0, W, 6], fill=RED)

# ---- masthead ----
d.text((16, 12), "THE WORLD TODAY", font=SERIF_B(46), fill=INK)
d.text((1024 - 16, 26), "SUNDAY 22 NOVEMBER 2026", font=SANS_B(20),
       fill=RED, anchor="ra")
d.rectangle([16, 66, W - 16, 68], fill=RED)
d.text((16, 74), "33 STORIES  \u00b7  6 REGIONS  \u00b7  EVERY ITEM FIRST REPORTED 22 NOV",
       font=SANS_B(13), fill=INK)
# legend badges, top right
lx = W - 16
for label, col in (("ONGOING", BLUE), ("CLAIM", AMBER), ("REPORTED", GREEN)):
    wdt = d.textlength(label, font=SANS_B(10)) + 12
    lx -= wdt
    d.rounded_rectangle([lx, 74, lx + wdt, 90], radius=3, fill=col)
    d.text((lx + 6, 76), label, font=SANS_B(10), fill=(255, 255, 255))
    lx -= 6
d.text((lx - 6, 76), "HOW WE KNOW EACH STORY \u2014", font=SANS(10),
       fill=GRAY, anchor="ra")

# ---- big-number strip ----
d.rectangle([16, 96, W - 16, 128], fill=NAVY)
nums = [("258", "House seats"), ("2", "tankers hit"), ("194", "COP31 parties"),
        ("330", "votes in NC"), ("36", "missing in Banten"), ("1,661", "Gaza toll")]
seg = (W - 32) / 6
for i, (n, lab) in enumerate(nums):
    x = 16 + i * seg
    d.text((x + 14, 99), n, font=SANS_B(22), fill=GOLD)
    d.text((x + 14 + d.textlength(n, font=SANS_B(22)) + 7, 106), lab,
           font=SANS(12), fill=(255, 255, 255))

# ---- heroes ----
heroes = [
    dict(kick="CONFLICT \u00b7 STRAIT OF HORMUZ", time="17:13 UTC",
         head="2 TANKERS HIT",
         body="Two supertankers hit mines east of Hormuz; both on fire.",
         src="Iran navy \u00b7 AP", badge="REPORTED", bg=NAVY, art="tanker"),
    dict(kick="CLIMATE \u00b7 ANTALYA", time="12:00 UTC",
         head="NO DEAL",
         body="COP31 collapses; EU + ~130 parties reject a text with no fossil fuels. Longest COP ever.",
         src="CNN \u00b7 Reuters", badge="REPORTED", bg=RED, art="globe"),
    dict(kick="POLITICS \u00b7 WASHINGTON", time="EVENING",
         head="258",
         body="Dems win House, largest majority since 1992; Hubbard beats Foxx by 330 in NC recount.",
         src="AP \u00b7 Reuters", badge="REPORTED", bg=NAVY, art="capitol"),
]
hx, hy, hw, hh = 16, 136, 322, 176
for i, hro in enumerate(heroes):
    x = hx + i * (hw + 8)
    # art band
    d.rectangle([x, hy, x + hw, hy + 76], fill=hro["bg"])
    if hro["art"] == "tanker":
        d.rectangle([x + 30, hy + 44, x + 240, hy + 62], fill=(230, 90, 20))
        d.rectangle([x + 190, hy + 22, x + 228, hy + 44], fill=(255, 255, 255))
        d.rectangle([x + 60, hy + 62, x + 250, hy + 76], fill=(60, 120, 180))
        for k in range(5):
            d.arc([x + 70 + k * 36, hy + 64, x + 94 + k * 36, hy + 76],
                  180, 360, fill=(255, 255, 255), width=2)
        cx, cy = x + 60, hy + 26
        for a in range(8):
            import math
            ang = a * math.pi / 4
            d.line([cx + 10 * math.cos(ang), cy + 10 * math.sin(ang),
                    cx + 18 * math.cos(ang), cy + 18 * math.sin(ang)],
                   fill=(255, 210, 40), width=3)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 210, 40))
        d.ellipse([x + 268, hy + 52, x + 284, hy + 68], fill=(20, 20, 20))
        for a in range(8):
            import math
            ang = a * math.pi / 4
            d.line([x + 276 + 9 * math.cos(ang), hy + 60 + 9 * math.sin(ang),
                    x + 276 + 14 * math.cos(ang), hy + 60 + 14 * math.sin(ang)],
                   fill=(20, 20, 20), width=2)
    elif hro["art"] == "globe":
        d.ellipse([x + 118, hy + 6, x + 204, hy + 72], fill=(235, 230, 210))
        d.ellipse([x + 132, hy + 18, x + 158, hy + 38], fill=(90, 160, 90))
        d.ellipse([x + 168, hy + 42, x + 194, hy + 62], fill=(90, 160, 90))
        d.ellipse([x + 150, hy + 12, x + 166, hy + 26], fill=(90, 160, 90))
        d.line([x + 161, hy + 6, x + 150, hy + 30, x + 172, hy + 48, x + 158, hy + 72],
               fill=(20, 20, 20), width=3)
    else:
        d.ellipse([x + 128, hy + 14, x + 194, hy + 44], fill=(255, 255, 255))
        d.rectangle([x + 128, hy + 40, x + 194, hy + 46], fill=(255, 255, 255))
        for k in range(5):
            d.rectangle([x + 132 + k * 13, hy + 46, x + 140 + k * 13, hy + 72],
                        fill=(255, 255, 255))
        d.rectangle([x + 126, hy + 72, x + 196, hy + 76], fill=(255, 255, 255))
        for sx, sy in ((x + 40, hy + 20), (x + 280, hy + 16), (x + 250, hy + 52)):
            d.text((sx, sy), "\u2605", font=SANS_B(12), fill=GOLD)
    # text below art
    ty = hy + 82
    d.text((x, ty), hro["kick"], font=SANS_B(11), fill=RED)
    d.text((x + hw, ty), hro["time"], font=SANS_B(11), fill=GRAY, anchor="ra")
    d.text((x, ty + 15), hro["head"], font=SERIF_B(26), fill=INK)
    lines = wrap(hro["body"], SANS(12), hw, d, max_lines=2)
    yy = ty + 46
    for ln in lines:
        d.text((x, yy), ln, font=SANS(12), fill=INK)
        yy += 15
    d.rounded_rectangle([x, hy + hh - 16, x + 74, hy + hh], radius=3, fill=GREEN)
    d.text((x + 6, hy + hh - 14), "REPORTED", font=SANS_B(9), fill=(255, 255, 255))
    d.text((x + 80, hy + hh - 14), hro["src"], font=SANS(11), fill=GRAY)

# ---- map strip ----
my = 320
d.text((16, my), "WHERE IT HAPPENED \u2014 EVERY HERO PINNED", font=SANS_B(12), fill=INK)
d.text((W - 16, my), "ALL TIMES UTC", font=SANS_B(10), fill=GRAY, anchor="ra")
mapx, mapy, mapw, maph = 16, my + 18, 620, 82
d.rectangle([mapx, mapy, mapx + mapw, mapy + maph], fill=(214, 232, 240),
            outline=(160, 180, 195))
land = (222, 205, 160)
continents = [
    [(30, 16), (120, 8), (150, 20), (140, 40), (100, 56), (60, 48), (32, 36)],
    [(132, 56), (166, 52), (176, 70), (152, 82), (136, 72)],
    [(300, 14), (340, 6), (360, 16), (350, 30), (320, 28), (305, 20)],
    [(300, 40), (345, 38), (360, 54), (340, 80), (315, 78), (300, 58)],
    [(370, 8), (480, 4), (520, 18), (500, 44), (450, 54), (420, 38), (390, 28), (375, 18)],
    [(480, 60), (520, 56), (530, 70), (500, 80), (485, 70)],
]
for poly in continents:
    d.polygon([(mapx + px, mapy + py) for px, py in poly], fill=land,
              outline=(150, 135, 100))
pins = [(445, 42, "1"), (372, 30, "2"), (75, 30, "3"), (325, 40, "4"),
        (335, 58, "5"), (345, 20, "6"), (490, 55, "7"), (365, 48, "8")]
for px, py, n in pins:
    cx, cy = mapx + px, mapy + py
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255))
    d.text((cx, cy - 6), n, font=SANS_B(8), fill=(255, 255, 255), anchor="ma")
# pin key, right of map, two columns of four
kx = mapx + mapw + 14
d.text((kx, my + 18), "PIN KEY", font=SANS_B(11), fill=INK)
key_items = ["1 Hormuz \u2014 2 tankers hit, 17:13", "2 Antalya \u2014 COP31 ends, no deal",
             "3 Washington \u2014 Dems reach 258", "4 Benghazi \u2014 Russian ship hit",
             "5 Khartoum \u2014 drones kill 4, UN hit", "6 Kyiv \u2014 Dymer strike, 3 killed",
             "7 Banten \u2014 factory fire, 36 missing", "8 Gaza \u2014 toll 1,661 since Oct 2025"]
for i, ki in enumerate(key_items):
    colx = kx + (i // 4) * 190
    yy = my + 36 + (i % 4) * 16
    d.text((colx, yy), ki, font=SANS(10), fill=INK)

# ---- region panels ----
REGIONS = [
    ("MIDDLE EAST", RED, [
        ("01", "Saudi intercepts Houthi drone + missile", "Reuters", "CLAIM"),
        ("02", "Bahrain blames Iran for strike", "France 24", ""),
        ("03", "UAE condemns Bahrain attack", "WAM", ""),
        ("04", "Pezeshkian: \u201csilent economic war\u201d", "IRNA", ""),
        ("05", "Iran unveils missile city", "IRGC media", ""),
        ("06", "Aoun: Israel must leave \u201cevery inch\u201d", "Al Jazeera", ""),
        ("07", "WCK: 3 killed in Gaza strike not its team", "WCK", ""),
        ("08", "Gaza: 350,000 families homeless", "Al Jazeera", ""),
        ("09", "Gaza toll 1,661 since Oct 2025", "Gaza health min.", ""),
        ("10", "Settlers burn West Bank cars", "Guardian", ""),
        ("11", "Settlers attack homes in Hebron", "WAFA", ""),
        ("12", "Unity talks stall", "Israeli media", "ONGOING"),
    ]),
    ("EUROPE", (40, 90, 160), [
        ("13", "Europe protests, day 3, costs + housing", "AP", ""),
        ("14", "Finland: war spills over, Baltic ship hit", "Finland", ""),
        ("15", "Zelenskyy pleads for Patriots", "BBC", ""),
        ("16", "Dymer drone strike kills 3", "BBC", ""),
        ("17", "Ex-Italian police chief found dead", "ANSA", ""),
        ("18", "Germany urged to arrest soldier", "HRF", ""),
        ("19", "de Soto: Iran war \u201cperfectly avoidable\u201d", "MED", ""),
    ]),
    ("ASIA", (150, 90, 20), [
        ("20", "Banten factory fire: 3 dead, 36 missing", "BBC", ""),
        ("21", "Korea minister quits over AI exam cheat", "BBC", ""),
        ("22", "Fidan: war fallout hits markets", "Anadolu", ""),
        ("23", "Turkey: Israel blocks Gaza homes", "Anadolu", "CLAIM"),
        ("24", "Fidan: Israel may use Druze in Syria", "Anadolu", "CLAIM"),
    ]),
    ("AFRICA", (120, 70, 20), [
        ("25", "Merkury hit at Benghazi", "France 24", "CLAIM"),
        ("26", "Khartoum drones kill 4, UN hit", "AP", "CLAIM"),
        ("27", "Benghazi depot blast", "Local auth.", ""),
        ("28", "S. Kordofan gold-mine drone kills 10", "R. Dabanga", ""),
    ]),
    ("AMERICAS", (20, 90, 110), [
        ("29", "Teen gamer + mother help FBI rescue girl", "FBI", ""),
    ]),
    ("OCEANIA", (180, 90, 20), [
        ("30", "Fred Nile dies, 92", "Guardian", ""),
    ]),
]
px0, py0, pw, ph, gap = 16, 428, 322, 216, 8
for idx, (name, col, stories) in enumerate(REGIONS):
    col_i, row_i = idx % 3, idx // 3
    x = px0 + col_i * (pw + gap)
    y = py0 + row_i * (ph + gap)
    d.rectangle([x, y, x + pw, y + ph], fill=PANEL_BG, outline=(200, 192, 175))
    d.rectangle([x, y, x + pw, y + 24], fill=col)
    d.text((x + 8, y + 4), name, font=SANS_B(13), fill=(255, 255, 255))
    d.text((x + pw - 8, y + 5), f"{len(stories)} STORIES", font=SANS_B(10),
           fill=(255, 255, 255), anchor="ra")
    yy = y + 30
    for num, head, src, flag in stories:
        # number colour codes verification: amber = CLAIM, blue = ONGOING
        num_col = AMBER if flag == "CLAIM" else (BLUE if flag == "ONGOING" else RED)
        rest = fit(f"{head} \u2014 {src}", SANS(11), pw - 16 - 24, d)
        d.text((x + 8, yy), num, font=SANS_B(11), fill=num_col)
        d.text((x + 8 + d.textlength(num + "  ", font=SANS_B(11)), yy),
               rest, font=SANS(11), fill=INK)
        yy += 15
    # filler illustration for short panels
    if len(stories) <= 5:
        fy = y + ph - 58
        if name == "ASIA":
            d.rectangle([x + 24, fy + 30, x + pw - 24, fy + 52], fill=(200, 60, 40))
            d.polygon([(x + 60, fy + 30), (x + 90, fy + 4), (x + 120, fy + 30)],
                      fill=(240, 160, 40))
            d.text((x + pw // 2, fy + 34), "BANTEN BLAZE", font=SANS_B(10),
                   fill=(255, 255, 255), anchor="ma")
        elif name == "AFRICA":
            d.rectangle([x + 40, fy + 34, x + pw - 40, fy + 50], fill=(230, 90, 20))
            d.rectangle([x + 190, fy + 20, x + 238, fy + 34], fill=(255, 255, 255))
            d.text((x + pw // 2, fy + 36), "BENGHAZI HARBOUR", font=SANS_B(10),
                   fill=(255, 255, 255), anchor="ma")
        elif name == "AMERICAS":
            d.text((x + 8, yy + 4), "Also in the US: Dems take the House \u2014",
                   font=SANS(11), fill=GRAY)
            d.text((x + 8, yy + 20), "see hero 258 above.", font=SANS(11), fill=GRAY)
            d.ellipse([x + pw // 2 - 26, fy + 2, x + pw // 2 + 26, fy + 54],
                      outline=NAVY, width=3)
            d.text((x + pw // 2, fy + 18), "FBI", font=SANS_B(16), fill=NAVY,
                   anchor="ma")
        elif name == "OCEANIA":
            d.text((x + 8, yy + 4), "Died 21 Nov, announced 22 Nov.",
                   font=SANS(11), fill=GRAY)
            d.text((x + 8, yy + 20), "NSW\u2019s longest-serving MP, 40+ years",
                   font=SANS(11), fill=GRAY)
            d.text((x + 8, yy + 36), "in parliament.", font=SANS(11), fill=GRAY)
            d.polygon([(x + 60, fy + 26), (x + 120, fy + 10), (x + 200, fy + 14),
                       (x + 260, fy + 30), (x + 220, fy + 50), (x + 120, fy + 48),
                       (x + 70, fy + 40)], fill=(222, 205, 160),
                      outline=(150, 135, 100))
            d.text((x + 150, fy + 24), "AUSTRALIA", font=SANS_B(10), fill=INK,
                   anchor="ma")
        elif name == "EUROPE":
            d.text((x + pw // 2, fy + 8), "\u2605 \u2605 \u2605 \u2605 \u2605 \u2605",
                   font=SANS_B(14), fill=GOLD, anchor="ma")
            d.text((x + pw // 2, fy + 30), "DAY 3 ON THE STREETS",
                   font=SANS_B(10), fill=NAVY, anchor="ma")

# ---- NOT YET strip ----
ny = py0 + 2 * ph + gap + 8
d.rectangle([16, ny, W - 16, ny + 26], fill=(255, 236, 170),
            outline=(200, 170, 60))
d.text((24, ny + 5),
       "NOT YET \u2014 DO NOT READ AS DONE:  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  Gaza ceasefire talks: no deal announced",
       font=SANS_B(11), fill=(90, 60, 0))

# ---- footer ----
fy = ny + 34
d.text((16, fy), "DATE CHECK \u2014 Every story above was first reported on 22 Nov, unless its kicker says otherwise.",
       font=SANS_B(11), fill=INK)
excl = wrap("EXCLUDED: El Chapo Isidro captured 20 Nov \u00b7 BepiColombo Mercury orbit 21 Nov \u00b7 ICJ Myanmar ruling 19 Nov \u00b7 Wall St rout 20 Nov \u00b7 FBI NCIC hack first reported 21 Nov \u00b7 Trump\u2013Xi AI guardrails announced 20 Nov.",
            SANS(10), W - 32, d, max_lines=2)
eyy = fy + 16
for ln in excl:
    d.text((16, eyy), ln, font=SANS(10), fill=INK)
    eyy += 14
d.text((16, eyy + 2),
       "LEGEND: REPORTED = confirmed by 2+ sources  \u00b7  number in amber = CLAIM (one side alleges, unverified)  \u00b7  number in blue = ONGOING (still developing).",
       font=SANS(10), fill=INK)
d.text((16, eyy + 18),
       "SOURCES: AP \u00b7 Reuters \u00b7 BBC \u00b7 CNN \u00b7 France 24 \u00b7 Al Jazeera \u00b7 Guardian \u00b7 SCMP \u00b7 IRNA \u00b7 Anadolu \u00b7 WAFA \u00b7 HRF \u00b7 WCK \u00b7 FBI \u00b7 Euronews \u00b7 dailysummaryof, 22 Nov 2026.",
       font=SANS(10), fill=GRAY)
d.text((16, eyy + 34), "THE WORLD TODAY \u00b7 22 NOV 2026",
       font=SANS_B(10), fill=GRAY)
d.text((W - 16, eyy + 34), "ALL TIMES UTC", font=SANS_B(10), fill=GRAY, anchor="ra")

img.save("entry.png", optimize=True)
print("saved entry.png")
