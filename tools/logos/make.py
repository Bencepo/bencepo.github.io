"""Bencepo addon logo family: dark tile, double gold ring (from the avatar),
one clear gold glyph per addon, one accent colour per addon."""
import math
from PIL import Image, ImageDraw, ImageFilter

SS = 4
N = 512
W = N * SS
BG0, BG1 = (11, 10, 9), (31, 26, 20)
GOLD, GOLD2, GOLDD = (224, 180, 90), (245, 214, 138), (156, 122, 50)

ACCENT = {
    "leveltrail": (95, 176, 122), "vendorfloor": (224, 112, 60), "procflare": (240, 190, 90),
    "swingcast": (90, 120, 230), "stattrim": (110, 160, 240), "transmogsweep": (163, 53, 238),
    "trinketdock": (79, 195, 247), "spikespotter": (255, 138, 61), "profcd": (140, 204, 242),
}


def s(v): return v * SS
def P(pts): return [(s(x), s(y)) for x, y in pts]


def base(acc):
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    # tile with radial gradient
    grad = Image.new("RGB", (W, W), BG0)
    gd = ImageDraw.Draw(grad)
    for i in range(60, 0, -1):
        t = i / 60
        c = tuple(int(BG0[k] + (BG1[k] - BG0[k]) * (1 - t)) for k in range(3))
        r = s(330) * t
        gd.ellipse([W / 2 - r, W / 2 - r * 0.95 - s(20), W / 2 + r, W / 2 + r * 0.95 - s(20)], fill=c)
    mask = Image.new("L", (W, W), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, W - 1], radius=s(96), fill=255)
    im.paste(grad, (0, 0), mask)
    # accent glow behind the glyph
    glow = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([s(136), s(136), s(376), s(376)], fill=acc + (70,))
    glow = glow.filter(ImageFilter.GaussianBlur(s(42)))
    im.alpha_composite(glow)
    d = ImageDraw.Draw(im)
    # tile edge and the double ring of the avatar
    d.rounded_rectangle([s(3), s(3), W - s(3), W - s(3)], radius=s(94), outline=(60, 48, 30), width=s(4))
    d.ellipse([s(34), s(34), s(478), s(478)], outline=GOLDD, width=s(10))
    d.ellipse([s(52), s(52), s(460), s(460)], outline=GOLD, width=s(4))
    return im, d


def line(d, pts, col, w):
    d.line(P(pts), fill=col, width=s(w), joint="curve")
    for x, y in (pts[0], pts[-1]):
        d.ellipse([s(x - w / 2), s(y - w / 2), s(x + w / 2), s(y + w / 2)], fill=col)


def dot(d, x, y, r, col): d.ellipse([s(x - r), s(y - r), s(x + r), s(y + r)], fill=col)


def arc(d, cx, cy, r, a0, a1, col, w):
    d.arc([s(cx - r), s(cy - r), s(cx + r), s(cy + r)], a0, a1, fill=col, width=s(w))


# ---------------------------------------------------------------- glyphs
def star(d, cx, cy, r, col, pts=5, inner=0.42):
    p = []
    for i in range(pts * 2):
        rr = r if i % 2 == 0 else r * inner
        ang = -math.pi / 2 + i * math.pi / pts
        p.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(P(p), fill=col)


def leveltrail(d, a):
    # a trail of steps climbing to a star
    pts = [(132, 372), (180, 342), (214, 296), (262, 270), (300, 226)]
    for i, (x, y) in enumerate(pts):
        dot(d, x, y, 13 + i * 3, a)
    star(d, 348, 168, 66, GOLD2)


def vendorfloor(d, a):
    dot(d, 256, 256, 80, GOLD)
    dot(d, 256, 256, 58, (186, 140, 56))
    line(d, [(256, 222), (256, 290)], GOLD2, 14)
    arc(d, 256, 256, 134, 0, 360, a, 16)
    for (x0, y0, x1, y1) in [(256, 92, 256, 150), (256, 362, 256, 420), (92, 256, 150, 256), (362, 256, 420, 256)]:
        line(d, [(x0, y0), (x1, y1)], a, 16)


def procflare(d, a):
    star(d, 256, 262, 170, a, pts=4, inner=0.2)
    star(d, 256, 262, 128, GOLD2, pts=4, inner=0.22)
    dot(d, 256, 262, 28, (255, 246, 220))
    star(d, 372, 146, 34, GOLD, pts=4, inner=0.3)


def swingcast(d, a):
    arc(d, 256, 316, 150, 196, 334, GOLD, 18)
    ex, ey = 256 + 150 * math.cos(math.radians(334)), 316 + 150 * math.sin(math.radians(334))
    dot(d, ex, ey, 24, GOLD2)
    d.rounded_rectangle([s(108), s(326), s(404), s(374)], radius=s(14), outline=GOLD, width=s(8))
    d.rounded_rectangle([s(120), s(338), s(316), s(362)], radius=s(7), fill=a)


def stattrim(d, a):
    for i, (w, col) in enumerate([(250, GOLD), (180, GOLD), (220, GOLDD), (150, GOLD)]):
        y = 150 + i * 62
        d.rounded_rectangle([s(132), s(y), s(132 + w), s(y + 30)], radius=s(15), fill=col)
    line(d, [(120, 400), (396, 128)], a, 16)


def transmogsweep(d, a):
    shirt = [(178, 128), (218, 116), (256, 146), (294, 116), (334, 128), (408, 196), (366, 250),
             (338, 228), (338, 390), (174, 390), (174, 228), (146, 250), (104, 196)]
    d.line(P(shirt + [shirt[0], shirt[1]]), fill=GOLD, width=s(16), joint="curve")
    star(d, 392, 128, 40, a, pts=4, inner=0.26)


def trinketdock(d, a):
    for x, col in ((106, GOLD), (266, a)):
        d.rounded_rectangle([s(x), s(176), s(x + 140), s(316)], radius=s(22), outline=col, width=s(14))
        gem = [(x + 70, 206), (x + 108, 236), (x + 94, 286), (x + 46, 286), (x + 32, 236)]
        d.polygon(P(gem), fill=GOLD2 if col == GOLD else col)
    line(d, [(126, 362), (386, 362)], GOLDD, 10)


def spikespotter(d, a):
    pts = [(96, 312), (160, 312), (188, 300), (216, 312), (240, 312), (262, 138), (286, 312), (340, 312), (416, 312)]
    line(d, pts, GOLD, 16)
    arc(d, 262, 178, 70, 0, 360, a, 16)
    line(d, [(312, 228), (360, 276)], a, 20)
    line(d, [(96, 370), (416, 370)], GOLDD, 8)


def profcd(d, a):
    arc(d, 256, 256, 150, -90, 196, a, 20)
    arc(d, 256, 256, 150, 206, 260, GOLD, 20)
    fl = [(234, 160), (278, 160), (278, 222), (334, 334), (178, 334), (234, 222)]
    d.line(P(fl + [fl[0], fl[1]]), fill=GOLD, width=s(14), joint="curve")
    line(d, [(218, 160), (294, 160)], GOLD, 16)
    d.polygon(P([(212, 272), (300, 272), (322, 322), (190, 322)]), fill=a)


GLYPH = dict(leveltrail=leveltrail, vendorfloor=vendorfloor, procflare=procflare, swingcast=swingcast,
             stattrim=stattrim, transmogsweep=transmogsweep, trinketdock=trinketdock,
             spikespotter=spikespotter, profcd=profcd)

if __name__ == "__main__":
    import sys, os
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    os.makedirs(out, exist_ok=True)
    for k, fn in GLYPH.items():
        im, d = base(ACCENT[k])
        fn(d, ACCENT[k])
        im.resize((N, N), Image.LANCZOS).save(f"{out}/{k}.png")
    # overview sheet
    keys = list(GLYPH)
    sheet = Image.new("RGB", (len(keys) * 150 + 10, 160), (24, 22, 20))
    for i, k in enumerate(keys):
        t = Image.open(f"{out}/{k}.png").resize((140, 140), Image.LANCZOS)
        sheet.paste(t, (10 + i * 150, 10), t)
    sheet.save(f"{out}/_sheet.png")
    print("ok")
