import math
from PIL import Image, ImageDraw
from make import base, ACCENT, GOLD, GOLD2, GOLDD, P, s, line, dot, arc, star, N

WHITE = (255, 246, 220)


# ---------------- LevelTrail: records your leveling run, split by split
def lt_a(d, a):
    # rising graph over an XP bar, level-up arrow at the end
    pts = [(120, 320), (176, 300), (222, 268), (270, 252), (318, 204), (370, 168)]
    line(d, pts, a, 14)
    for x, y in pts[:-1]:
        dot(d, x, y, 12, GOLD2)
    d.polygon(P([(370, 128), (408, 176), (332, 176)]), fill=GOLD2)
    d.rounded_rectangle([s(116), s(352), s(396), s(380)], radius=s(12), outline=GOLD, width=s(6))
    d.rounded_rectangle([s(124), s(360), s(318), s(372)], radius=s(5), fill=a)


def lt_b(d, a):
    # level badge with upward chevrons and split ticks
    for i in range(3):
        y = 196 - i * 44
        d.line(P([(196, y + 40), (256, y), (316, y + 40)]), fill=a if i else GOLD2, width=s(18), joint="curve")
    d.rounded_rectangle([s(150), s(262), s(362), s(346)], radius=s(18), outline=GOLD, width=s(10))
    for i, x in enumerate(range(176, 340, 34)):
        h = [18, 30, 22, 40, 34][i]
        d.rounded_rectangle([s(x), s(330 - h), s(x + 18), s(330)], radius=s(4), fill=GOLD2 if i == 3 else GOLD)


def lt_c(d, a):
    # stopwatch with a rising trail inside (speedrun splits)
    dot(d, 256, 272, 128, (0, 0, 0, 0))
    arc(d, 256, 272, 124, 0, 360, GOLD, 14)
    d.rounded_rectangle([s(234), s(110), s(278), s(138)], radius=s(6), fill=GOLD)
    line(d, [(256, 138), (256, 150)], GOLD, 12)
    pts = [(176, 320), (220, 300), (248, 262), (292, 244), (330, 200)]
    line(d, pts, a, 14)
    d.polygon(P([(342, 176), (348, 222), (308, 204)]), fill=a)


# ---------------- ProcFlare: big pulsing alert when Clearcasting or a proc fires
def pf_a(d, a):
    # spell icon with glowing border and pulse rings
    for r, w, c in ((150, 6, GOLDD), (124, 8, a)):
        arc(d, 256, 256, r, 0, 360, c, w)
    d.rounded_rectangle([s(176), s(176), s(336), s(336)], radius=s(18), outline=GOLD2, width=s(14))
    star(d, 256, 256, 54, a, pts=4, inner=0.25)
    dot(d, 256, 256, 12, WHITE)


def pf_b(d, a):
    # alert: spell icon plus sound waves
    d.rounded_rectangle([s(118), s(184), s(262), s(328)], radius=s(18), outline=GOLD2, width=s(14))
    star(d, 190, 256, 48, a, pts=4, inner=0.25)
    for r in (52, 92, 132):
        arc(d, 262, 256, r, -40, 40, a if r != 92 else GOLD, 14)


def pf_c(d, a):
    # exclamation in a burst: "proc!"
    star(d, 256, 256, 170, a, pts=8, inner=0.62)
    dot(d, 256, 256, 104, (20, 16, 12))
    d.rounded_rectangle([s(240), s(178), s(272), s(282)], radius=s(14), fill=GOLD2)
    dot(d, 256, 316, 18, GOLD2)


# ---------------- TrinketDock: two trinket buttons, flyout to swap, queued in combat
def td_a(d, a):
    # flyout column above the right slot, swap arrow
    for x, col in ((118, GOLD), (266, a)):
        d.rounded_rectangle([s(x), s(286), s(x + 128), s(414)], radius=s(18), outline=col, width=s(12))
        gem = [(x + 64, 314), (x + 98, 340), (x + 86, 386), (x + 42, 386), (x + 30, 340)]
        d.polygon(P(gem), fill=GOLD2 if col == GOLD else col)
    for i, y in enumerate((112, 192)):
        d.rounded_rectangle([s(290), s(y), s(370), s(y + 70)], radius=s(12), outline=GOLDD, width=s(8))
        dot(d, 330, y + 35, 16, GOLDD if i == 0 else GOLD)
    line(d, [(330, 262), (330, 280)], GOLDD, 8)


def td_b(d, a):
    # two slots with circular swap arrows
    for x, col in ((122, GOLD), (262, a)):
        d.rounded_rectangle([s(x), s(196), s(x + 128), s(324)], radius=s(18), outline=col, width=s(12))
        gem = [(x + 64, 224), (x + 98, 250), (x + 86, 296), (x + 42, 296), (x + 30, 250)]
        d.polygon(P(gem), fill=GOLD2 if col == GOLD else col)
    arc(d, 256, 190, 100, 210, 330, GOLD2, 12)
    d.polygon(P([(354, 156), (352, 196), (318, 176)]), fill=GOLD2)
    arc(d, 256, 330, 100, 30, 150, GOLD2, 12)
    d.polygon(P([(158, 364), (160, 324), (194, 344)]), fill=GOLD2)


def td_c(d, a):
    # slot with fanned trinkets and a queue clock
    for i, ang in enumerate((-24, 0, 24)):
        cx = 256 + 120 * math.sin(math.radians(ang)); cy = 290 - 120 * math.cos(math.radians(ang))
        dot(d, cx, cy, 30, GOLDD if i != 1 else GOLD)
    d.rounded_rectangle([s(186), s(250), s(326), s(390)], radius=s(20), outline=a, width=s(14))
    gem = [(256, 282), (296, 312), (282, 362), (230, 362), (216, 312)]
    d.polygon(P(gem), fill=a)
    arc(d, 344, 360, 36, 0, 360, GOLD2, 8)
    line(d, [(344, 360), (344, 338)], GOLD2, 6)
    line(d, [(344, 360), (360, 368)], GOLD2, 6)


SETS = [("leveltrail", [lt_a, lt_b, lt_c]), ("procflare", [pf_a, pf_b, pf_c]), ("trinketdock", [td_a, td_b, td_c])]

if __name__ == "__main__":
    T = 170
    sheet = Image.new("RGB", (40 + 3 * (T + 14) + 110, 3 * (T + 30) + 20), (24, 22, 20))
    sd = ImageDraw.Draw(sheet)
    for r, (k, fns) in enumerate(SETS):
        sd.text((10, 20 + r * (T + 30) + T // 2), k, fill=(224, 180, 90))
        for c, fn in enumerate(fns):
            im, d = base(ACCENT[k]); fn(d, ACCENT[k])
            im = im.resize((N, N), Image.LANCZOS)
            im.save(f"out/{k}_{'abc'[c]}.png")
            t = im.resize((T, T), Image.LANCZOS)
            x = 110 + c * (T + 14); y = 20 + r * (T + 30)
            sheet.paste(t, (x, y), t)
            sd.text((x + T // 2 - 4, y + T + 4), "ABC"[c], fill=(236, 227, 208))
    sheet.save("out/_variants.png")
    print("ok")
