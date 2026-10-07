"""Generates the placeholder artwork in ../assets/art/ as JPEGs.

Each scene is drawn as a layered SVG (fog, light shafts, particles, textures),
then rendered with headless Chrome and saved as JPEG so pages stay fast.

Run: python3 tools/gen_art.py
Replace any output with real artwork of the same name (or update the src in the HTML).
"""
import math
import os
import random
import shutil
import subprocess
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "art")
WORK = os.path.join(HERE, "_render")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
os.makedirs(OUT, exist_ok=True)
os.makedirs(WORK, exist_ok=True)

FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900"
         "&family=IBM+Plex+Mono:wght@400;500&display=swap")


# ---------------------------------------------------------------- helpers
def blur(fid, sd):
    return (f'<filter id="{fid}" x="-50%" y="-50%" width="200%" height="200%">'
            f'<feGaussianBlur stdDeviation="{sd}"/></filter>')


def clouds(fid, rgb, freq, seed, a=3.0, b=-1.35, octaves=5):
    r, g, bl = (int(rgb[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return (f'<filter id="{fid}" x="0" y="0" width="100%" height="100%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="{octaves}" seed="{seed}"/>'
            f'<feColorMatrix values="0 0 0 0 {r:.3f}  0 0 0 0 {g:.3f}  0 0 0 0 {bl:.3f}  0 0 0 {a} {b}"/></filter>')


def vgrad(gid, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">{s}</linearGradient>'


def hgrad(gid, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">{s}</linearGradient>'


def rgrad(gid, stops, cx=.5, cy=.5, r=.5):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'


def band_mask(mid, y0, y1, w):
    """Mask that is white in the middle of [y0, y1] and fades out at both edges."""
    return (f'<linearGradient id="{mid}g" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity="1"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="0" y="{y0}" width="{w}" height="{y1 - y0}">'
            f'<rect x="0" y="{y0}" width="{w}" height="{y1 - y0}" fill="url(#{mid}g)"/></mask>')


def pts(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def glow(x, y, r, color, op=1.0, core=None):
    s = (f'<circle cx="{x}" cy="{y}" r="{r*4}" fill="{color}" opacity="{op*.18}" filter="url(#b40)"/>'
         f'<circle cx="{x}" cy="{y}" r="{r*1.6}" fill="{color}" opacity="{op*.6}" filter="url(#b6)"/>')
    s += f'<circle cx="{x}" cy="{y}" r="{r*.55}" fill="{core or "#fff3e0"}"/>'
    return s


def astronaut(x, feet, h, lamp=True):
    hr, top, c = h * .13, feet - h, "#07090b"
    s = (f'<ellipse cx="{x - h*.9}" cy="{feet + 2}" rx="{h*1.1}" ry="{h*.07}" fill="#000" opacity=".5" filter="url(#b2)"/>'
         f'<circle cx="{x}" cy="{top + hr}" r="{hr}" fill="{c}"/>'
         f'<path d="M{x + hr*.1} {top + hr*.55} a{hr*.7} {hr*.6} 0 0 1 {hr*.75} {hr*.5}" stroke="#9fc4d1" stroke-width="1.2" fill="none" opacity=".8"/>'
         f'<rect x="{x - h*.19}" y="{top + hr*1.8}" width="{h*.38}" height="{h*.42}" rx="{h*.07}" fill="{c}"/>'
         f'<rect x="{x - h*.31}" y="{top + hr*1.9}" width="{h*.16}" height="{h*.32}" rx="{h*.03}" fill="{c}"/>'
         f'<path d="M{x - h*.17} {top + h*.64} L{x - h*.21} {feet} L{x - h*.04} {feet} L{x} {top + h*.7} '
         f'L{x + h*.05} {feet} L{x + h*.21} {feet} L{x + h*.17} {top + h*.64}Z" fill="{c}"/>')
    if lamp:
        s += (f'<path d="M{x + h*.12} {top + h*.42} L{x + h*1.9} {feet + 4} L{x + h*.5} {feet + 8}Z" fill="#cfe9f0" opacity=".12" filter="url(#b6)"/>'
              f'<circle cx="{x + h*.12}" cy="{top + h*.42}" r="1.6" fill="#e8f7fb"/>')
    return s


def hooded(x, feet, h, c="#120f0c", staff=True, cloak_dir=-1):
    """Hooded, cloaked figure; the cape blows in cloak_dir (-1 = left)."""
    k, top = cloak_dir, feet - h
    s = (f'<path d="M{x - h*.1} {top + h*.2} Q{x - h*.11} {top + h*.02} {x + h*.02} {top} Q{x + h*.12} {top + h*.04} {x + h*.11} {top + h*.2}Z" fill="{c}"/>'
         f'<path d="M{x - h*.13} {top + h*.18} L{x + h*.13} {top + h*.18} L{x + h*.2} {feet - h*.3} L{x + h*.16} {feet} '
         f'L{x - h*.16} {feet} L{x - h*.2} {feet - h*.3}Z" fill="{c}"/>'
         f'<path d="M{x - k*-.1*h} {top + h*.2} C{x + k*.35*h} {top + h*.24} {x + k*.62*h} {top + h*.36} {x + k*.8*h} {top + h*.42} '
         f'L{x + k*.62*h} {top + h*.5} C{x + k*.55*h} {top + h*.6} {x + k*.38*h} {top + h*.72} {x + k*.12*h} {feet - h*.08}Z" fill="{c}" opacity=".95"/>')
    if staff:
        s += f'<line x1="{x - k*.3*h}" y1="{feet}" x2="{x - k*.36*h}" y2="{top - h*.15}" stroke="{c}" stroke-width="{max(h*.04, 1.4)}"/>'
    return s


def particles(n, x0, y0, x1, y1, color, rmin, rmax, omin, omax, seed, blurred=False):
    random.seed(seed)
    f = ' filter="url(#b2)"' if blurred else ""
    return "".join(
        f'<circle cx="{random.uniform(x0, x1):.1f}" cy="{random.uniform(y0, y1):.1f}" r="{random.uniform(rmin, rmax):.2f}" '
        f'fill="{color}" opacity="{random.uniform(omin, omax):.2f}"{f}/>' for _ in range(n))


COMMON_DEFS = blur("b2", 2) + blur("b6", 6) + blur("b14", 14) + blur("b40", 40)


# ---------------------------------------------------------------- scene A: Last Signal
def scene_last_signal():
    W, H = 1600, 900
    HZ = 585  # horizon
    d = COMMON_DEFS
    d += vgrad("skyA", [(0, "#05080b", 1), (.42, "#0d141a", 1), (.6, "#1a252d", 1), (.66, "#2b3a44", 1), (1, "#0d1317", 1)])
    d += rgrad("planet", [(0, "#4a6878", 1), (.55, "#22343f", 1), (1, "#0b1217", 1)], cx=.32, cy=.78, r=.85)
    d += rgrad("terminator", [(0, "#04070a", 0), (.55, "#04070a", .2), (1, "#04070a", .95)], cx=.25, cy=.85, r=.95)
    d += vgrad("ground", [(0, "#1d2830", 1), (.25, "#141c22", 1), (1, "#080b0e", 1)])
    d += hgrad("beam", [(0, "#ffb27a", 0), (.75, "#ffb27a", .22), (1, "#ffd9b8", .5)])
    d += vgrad("search", [(0, "#cfe6ee", 0), (1, "#cfe6ee", .22)])
    d += rgrad("vign", [(0, "#000", 0), (.65, "#000", 0), (1, "#000", .55)], r=.75)
    d += clouds("fogA", "#8a9ca6", "0.0022 0.014", 7)
    d += clouds("fogA2", "#a9b8bf", "0.004 0.03", 19, a=2.6, b=-1.25)
    d += clouds("iceA", "#9fb1ba", "0.0015 0.09", 3, a=2.2, b=-1.2, octaves=3)
    d += band_mask("mFar", 430, 660, W) + band_mask("mNear", 600, 820, W)
    d += f'<clipPath id="cPlanet"><circle cx="1180" cy="-70" r="530"/></clipPath>'
    d += f'<clipPath id="cGround"><rect x="0" y="{HZ}" width="{W}" height="{H - HZ}"/></clipPath>'

    b = f'<rect width="{W}" height="{H}" fill="url(#skyA)"/>'
    # stars + a faint galactic band
    b += f'<ellipse cx="420" cy="170" rx="520" ry="70" transform="rotate(-16 420 170)" fill="#6f8792" opacity=".12" filter="url(#b40)"/>'
    b += particles(260, 0, 0, W, 470, "#e9f1f4", .4, 1.1, .15, .7, 11)
    b += particles(40, 120, 60, 760, 300, "#e9f1f4", .5, 1.2, .3, .8, 12)
    # planet with bands, storm, terminator and rim light
    b += '<circle cx="1180" cy="-70" r="530" fill="url(#planet)"/>'
    random.seed(4)
    bands = ""
    for i in range(12):
        y = -70 + random.uniform(-80, 500)
        bands += (f'<ellipse cx="1180" cy="{y:.0f}" rx="600" ry="{random.uniform(6, 26):.0f}" '
                  f'fill="{random.choice(["#6d8c9a", "#1a2a33", "#86a6b3"])}" opacity="{random.uniform(.06, .18):.2f}" filter="url(#b6)"/>')
    b += f'<g clip-path="url(#cPlanet)">{bands}<circle cx="1180" cy="-70" r="530" fill="url(#terminator)"/></g>'
    b += '<circle cx="1180" cy="-70" r="530" fill="none" stroke="#a9cdd9" stroke-width="10" opacity=".14" filter="url(#b14)"/>'
    b += '<circle cx="1180" cy="-70" r="530" fill="none" stroke="#b8dbe6" stroke-width="1.6" opacity=".45"/>'
    # distant mesas (two hazy layers)
    for layer, (col, base, amp, seed) in enumerate([("#2a3740", HZ - 22, 42, 5), ("#1d2830", HZ - 4, 30, 8)]):
        random.seed(seed)
        x, p = 0, [(0, H)]
        while x < W:
            top = base - random.uniform(.2, 1) * amp
            p += [(x, base), (x + random.uniform(4, 14), top), (x + random.uniform(60, 180), top - random.uniform(-4, 4))]
            x = p[-1][0] + random.uniform(10, 30)
            p += [(x, base)]
            x += random.uniform(30, 160)
        p += [(W, base), (W, H)]
        b += f'<polygon points="{pts(p)}" fill="{col}"/>'
    b += f'<rect x="0" y="430" width="{W}" height="230" filter="url(#fogA)" mask="url(#mFar)" opacity=".75"/>'
    # stepped pyramid megastructure in the haze (right)
    for i in range(6):
        w, y = 330 - i * 48, HZ - 40 - i * 34
        b += f'<rect x="{1430 - w/2}" y="{y}" width="{w}" height="36" fill="#18222a" opacity=".85"/>'
    b += f'<rect x="1260" y="380" width="340" height="230" fill="#2b3a44" opacity=".35" filter="url(#b14)"/>'
    # ground and ice texture
    b += f'<rect x="0" y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#ground)"/>'
    b += f'<g clip-path="url(#cGround)"><rect x="0" y="{HZ}" width="{W}" height="{H - HZ}" filter="url(#iceA)" opacity=".16"/></g>'
    # antenna array receding to the horizon
    random.seed(9)
    for row, (by, s0, x0, x1, step) in enumerate([(600, 9, 40, 1060, 34), (622, 15, 0, 1080, 58), (668, 26, -40, 1090, 96)]):
        x = x0 + random.uniform(0, step * .5)
        while x < x1:
            s = s0 * random.uniform(.9, 1.1)
            ang = -32 + random.uniform(-4, 4)
            cy = by - s * 1.25
            b += (f'<line x1="{x - s*.35:.1f}" y1="{by}" x2="{x:.1f}" y2="{cy + s*.2:.1f}" stroke="#0c1115" stroke-width="{s*.08:.1f}"/>'
                  f'<line x1="{x + s*.35:.1f}" y1="{by}" x2="{x:.1f}" y2="{cy + s*.2:.1f}" stroke="#0c1115" stroke-width="{s*.08:.1f}"/>'
                  f'<g transform="rotate({ang:.1f} {x:.1f} {cy:.1f})">'
                  f'<ellipse cx="{x:.1f}" cy="{cy:.1f}" rx="{s:.1f}" ry="{s*.38:.1f}" fill="#141c22" stroke="#4d626d" stroke-width="{max(s*.04, .6):.1f}" stroke-opacity=".55"/>'
                  f'<ellipse cx="{x:.1f}" cy="{cy + s*.04:.1f}" rx="{s*.7:.1f}" ry="{s*.22:.1f}" fill="#0b1014"/>'
                  f'<line x1="{x:.1f}" y1="{cy:.1f}" x2="{x:.1f}" y2="{cy - s*.75:.1f}" stroke="#2b3943" stroke-width="{max(s*.04, .6):.1f}"/></g>')
            if random.random() < .12:
                b += f'<circle cx="{x:.1f}" cy="{cy - s*.6:.1f}" r="{max(s*.07, .9):.1f}" fill="#ff7a3a"/><circle cx="{x:.1f}" cy="{cy - s*.6:.1f}" r="{s*.4:.1f}" fill="#ff7a3a" opacity=".25" filter="url(#b6)"/>'
            x += step * random.uniform(.8, 1.2)
    # searchlights from the station
    b += '<polygon points="1250,560 980,40 1060,30" fill="url(#search)" opacity=".5" filter="url(#b14)"/>'
    b += '<polygon points="1420,550 1560,20 1610,40" fill="url(#search)" opacity=".35" filter="url(#b14)"/>'
    # brutalist station base
    b += '<polygon points="1060,712 1110,566 1600,540 1600,720" fill="#10171c"/>'
    b += '<polygon points="1110,566 1600,540 1600,556 1112,580" fill="#24313a"/>'
    for i, y in enumerate(range(596, 700, 18)):
        b += f'<line x1="{1104 - i*6}" y1="{y}" x2="1600" y2="{y - 20 + i*.5}" stroke="#1b252c" stroke-width="2"/>'
    random.seed(2)
    for row in range(2):
        for i in range(40):
            if random.random() < .45:
                x = 1130 + i * 11.5
                b += f'<rect x="{x}" y="{588 + row*14 - i*.4}" width="6" height="2.2" fill="#a9dbe6" opacity="{random.uniform(.25, .7):.2f}"/>'
    b += '<rect x="1240" y="640" width="150" height="72" fill="#06090b"/>'
    b += '<rect x="1250" y="650" width="130" height="62" fill="#e07a3a" opacity=".12" filter="url(#b14)"/>'
    b += '<polygon points="1240,712 1390,712 1430,760 1200,760" fill="#0d1317"/>'
    # lattice tower
    tx, base_y, top_y = 1330, 548, 140
    lx0, lx1, rx0, rx1 = tx - 44, tx - 13, tx + 44, tx + 13
    b += f'<polygon points="{lx0},{base_y} {lx1},{top_y} {rx1},{top_y} {rx0},{base_y}" fill="#0f161b" opacity=".75"/>'
    b += f'<line x1="{lx0}" y1="{base_y}" x2="{lx1}" y2="{top_y}" stroke="#2c3b45" stroke-width="3"/><line x1="{rx0}" y1="{base_y}" x2="{rx1}" y2="{top_y}" stroke="#1a242b" stroke-width="3"/>'
    n = 16
    for i in range(n):
        y0, y1 = base_y - (base_y - top_y) * i / n, base_y - (base_y - top_y) * (i + 1) / n
        f0, f1 = i / n, (i + 1) / n
        xl0, xr0 = lx0 + (lx1 - lx0) * f0, rx0 + (rx1 - rx0) * f0
        xl1, xr1 = lx0 + (lx1 - lx0) * f1, rx0 + (rx1 - rx0) * f1
        b += (f'<line x1="{xl0:.1f}" y1="{y0:.1f}" x2="{xr1:.1f}" y2="{y1:.1f}" stroke="#25323b" stroke-width="1.2"/>'
              f'<line x1="{xr0:.1f}" y1="{y0:.1f}" x2="{xl1:.1f}" y2="{y1:.1f}" stroke="#25323b" stroke-width="1.2"/>'
              f'<line x1="{xl1:.1f}" y1="{y1:.1f}" x2="{xr1:.1f}" y2="{y1:.1f}" stroke="#2c3b45" stroke-width="1"/>')
        if i % 4 == 2:
            b += f'<rect x="{tx - 2}" y="{y1:.1f}" width="4" height="2" fill="#a9dbe6" opacity=".7"/>'
    # double ring with struts
    for ry, rr, col in ((300, 190, "#1f2a31"), (318, 172, "#18212 7".replace(" ", ""))):
        b += f'<path d="M{tx - rr} {ry} A{rr} {rr*.17} 0 0 1 {tx + rr} {ry}" fill="none" stroke="{col}" stroke-width="8"/>'
    for a in range(0, 360, 30):
        ex, ey = tx + 190 * math.cos(math.radians(a)), 300 + 190 * .17 * math.sin(math.radians(a))
        b += f'<line x1="{tx}" y1="300" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#1a232a" stroke-width="1.5"/>'
    b += f'<path d="M{tx - 190} 300 A190 32 0 0 0 {tx + 190} 300" fill="none" stroke="#2f3e48" stroke-width="8"/>'
    b += f'<path d="M{tx - 190} 296 A190 32 0 0 0 {tx + 190} 296" fill="none" stroke="#7fa3b0" stroke-width="1" opacity=".35"/>'
    b += f'<line x1="{tx}" y1="{top_y}" x2="{tx}" y2="{top_y - 70}" stroke="#2c3b45" stroke-width="2"/>'
    b += f'<line x1="{tx - 6}" y1="{top_y - 40}" x2="{tx + 6}" y2="{top_y - 40}" stroke="#2c3b45" stroke-width="1.5"/>'
    # beacon and its long beam through the fog
    b += f'<polygon points="{tx},{top_y - 4} 120,250 120,330" fill="url(#beam)" filter="url(#b14)" opacity=".55"/>'
    b += glow(tx, top_y - 4, 7, "#ff8a45")
    # tracks and footprints to the hangar
    b += '<polygon points="880,900 1010,900 1290,712 1262,712" fill="#0b1013" opacity=".9"/>'
    b += '<polyline points="880,900 1262,712" stroke="#3a4b55" stroke-width="1.4" opacity=".6" fill="none"/>'
    b += '<polyline points="1010,900 1290,712" stroke="#3a4b55" stroke-width="1.4" opacity=".6" fill="none"/>'
    random.seed(14)
    for i in range(14):
        t = i / 14
        x, y = 1190 - t * 120 + (i % 2) * 6, 768 + t * 120
        b += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{3 + t*3:.1f}" ry="{1.2 + t:.1f}" fill="#06090b" opacity=".7"/>'
    # low fog in front of the array
    b += f'<rect x="0" y="600" width="{W}" height="220" filter="url(#fogA2)" mask="url(#mNear)" opacity=".38"/>'
    # foreground ice boulders
    for poly, lit in (([(0, 900), (0, 780), (70, 752), (150, 770), (230, 820), (270, 900)], [(0, 780), (70, 752), (150, 770)]),
                      ([(1420, 900), (1470, 812), (1540, 790), (1600, 800), (1600, 900)], [(1470, 812), (1540, 790), (1600, 800)])):
        b += f'<polygon points="{pts(poly)}" fill="#070a0c"/>'
        b += f'<polyline points="{pts(lit)}" fill="none" stroke="#5f7884" stroke-width="1.4" opacity=".5"/>'
    b += astronaut(1205, 765, 62)
    # snow: fine flakes + out-of-focus foreground flakes
    b += particles(420, 0, 0, W, H, "#e3edf1", .5, 1.4, .25, .75, 21)
    b += particles(30, 0, 0, W, H, "#e3edf1", 4, 10, .08, .2, 22, blurred=True)
    b += f'<rect width="{W}" height="{H}" fill="url(#vign)"/>'
    return W, H, d, b


# ---------------------------------------------------------------- scene B: Backup
def scene_backup():
    W, H = 900, 1600
    d = COMMON_DEFS
    d += vgrad("skyB", [(0, "#3e4c51", 1), (.22, "#26343b", 1), (.5, "#121a1f", 1), (1, "#05070a", 1)])
    d += rgrad("sodium", [(0, "#d07a3a", .5), (1, "#d07a3a", 0)])
    d += rgrad("holo", [(0, "#9be8f5", .55), (1, "#9be8f5", 0)])
    d += rgrad("warm", [(0, "#ffb070", .9), (1, "#e07a3a", 0)])
    d += rgrad("vign", [(0, "#000", 0), (.6, "#000", 0), (1, "#000", .6)], r=.8)
    d += clouds("fogB", "#93a9b1", "0.006 0.004", 5)
    d += clouds("fogB2", "#b8c7cc", "0.01 0.006", 13, a=2.6, b=-1.3)
    d += band_mask("mB1", 150, 700, W) + band_mask("mB2", 1050, 1600, W)
    d += '<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="#bff3fb"/></pattern>'

    b = f'<rect width="{W}" height="{H}" fill="url(#skyB)"/>'
    b += f'<ellipse cx="450" cy="760" rx="420" ry="320" fill="url(#sodium)"/>'

    def towers(seed, n, x0, x1, ymin, ymax, col, win_op, wmin=50, wmax=120):
        random.seed(seed)
        s = ""
        for _ in range(n):
            w = random.uniform(wmin, wmax)
            x = random.uniform(x0, x1 - w)
            top = random.uniform(ymin, ymax)
            s += f'<rect x="{x:.1f}" y="{top:.1f}" width="{w:.1f}" height="{H - top:.1f}" fill="{col}"/>'
            if random.random() < .5:
                s += f'<line x1="{x + w/2:.1f}" y1="{top:.1f}" x2="{x + w/2:.1f}" y2="{top - random.uniform(20, 70):.1f}" stroke="{col}" stroke-width="2"/>'
                s += f'<circle cx="{x + w/2:.1f}" cy="{top - 40:.1f}" r="1.6" fill="#ff5a3a" opacity=".8"/>'
            for yy in range(int(top) + 8, H, 11):
                for xx in range(int(x) + 4, int(x + w) - 4, 8):
                    if random.random() < win_op:
                        s += f'<rect x="{xx}" y="{yy}" width="4" height="3" fill="{random.choice(["#cfe9ee", "#cfe9ee", "#f0c08a"])}" opacity="{random.uniform(.15, .6):.2f}"/>'
        return s
    b += towers(3, 9, 220, 700, 60, 300, "#33454c", .05)
    b += f'<rect x="0" y="150" width="{W}" height="550" filter="url(#fogB)" mask="url(#mB1)" opacity=".7"/>'
    b += towers(5, 7, 200, 720, 240, 520, "#1f2c33", .08, 70, 150)
    # giant hologram: a figure made of light, and the MIRROR brand
    hx, hy = 470, 520
    holo = (f'<circle cx="{hx}" cy="{hy}" r="62"/>'
            f'<path d="M{hx - 150} {hy + 300} Q{hx - 140} {hy + 110} {hx - 40} {hy + 85} L{hx + 40} {hy + 85} Q{hx + 140} {hy + 110} {hx + 150} {hy + 300}Z"/>'
            f'<rect x="{hx - 26}" y="{hy + 50}" width="52" height="45"/>')
    b += f'<g fill="url(#holo)" opacity=".55" filter="url(#b14)">{holo}</g>'
    b += f'<g fill="url(#scan)" opacity=".22">{holo}</g>'
    b += f'<g fill="#d65a9a" opacity=".07" transform="translate(9 3)">{holo}</g>'
    b += (f'<text x="640" y="380" font-family="Archivo" style="font-stretch:125%" font-weight="200" font-size="58" fill="#bff3fb" '
          f'opacity=".55" writing-mode="tb" letter-spacing="10">MIRROR</text>'
          f'<text x="292" y="900" font-family="IBM Plex Mono" font-size="11" fill="#bff3fb" opacity=".5" letter-spacing="3">REMEMBER EVERYTHING · BACKUP 03:00</text>')
    # spinners with light trails
    random.seed(8)
    for i in range(6):
        x, y, s = random.uniform(260, 650), random.uniform(300, 760), random.uniform(.6, 1.4)
        b += (f'<line x1="{x - 120*s:.1f}" y1="{y + 8*s:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="#ffcaa0" stroke-width="{1.2*s:.1f}" opacity=".3" filter="url(#b2)"/>'
              f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{9*s:.1f}" ry="{3*s:.1f}" fill="#0b0f12"/>'
              f'<circle cx="{x + 8*s:.1f}" cy="{y:.1f}" r="{1.5*s:.1f}" fill="#fff4e0"/><circle cx="{x - 8*s:.1f}" cy="{y:.1f}" r="{1.2*s:.1f}" fill="#ff4a3a"/>')
    # far sky-bridge
    b += '<rect x="230" y="560" width="450" height="9" fill="#172128"/><line x1="230" y1="569" x2="680" y2="569" stroke="#9be8f5" stroke-width="1" opacity=".4"/>'
    # signage
    for x, y, w, h, c in ((268, 640, 16, 120, "#6fd6e8"), (612, 700, 14, 90, "#e09a3a"), (250, 980, 18, 150, "#d65a9a"), (645, 1040, 16, 110, "#6fd6e8")):
        b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" opacity=".5"/><rect x="{x - 10}" y="{y - 10}" width="{w + 20}" height="{h + 20}" fill="{c}" opacity=".25" filter="url(#b14)"/>'

    # near brutalist towers (left/right) with dense window grids and fins
    def near_tower(x0, x1, slant, seed):
        random.seed(seed)
        s = f'<polygon points="{x0},0 {x1},0 {x1 + slant},{H} {x0 - (slant if x0 > 0 else 0)},{H}" fill="#0f151a"/>'
        cols = int(abs(x1 - x0) / 26)
        for r in range(0, 120):
            y = 10 + r * 13.2
            off = slant * y / H
            for c in range(cols):
                x = min(x0, x1) + 8 + c * 26 + (off if x1 > x0 and x0 > 0 else off * (1 if x0 == 0 else 0))
                v = random.random()
                if v < .1:
                    col, op = "#cfe9ee", random.uniform(.25, .6)
                elif v < .13:
                    col, op = "#f0b47a", random.uniform(.4, .8)
                else:
                    col, op = "#05080a", .9
                s += f'<rect x="{x:.1f}" y="{y:.1f}" width="15" height="6" fill="{col}" opacity="{op:.2f}"/>'
        for c in range(0, cols + 1, 3):
            x = min(x0, x1) + 3 + c * 26
            s += f'<rect x="{x}" y="0" width="3" height="{H}" fill="#1a232a"/>'
        return s
    b += near_tower(0, 230, 40, 31)
    b += near_tower(670, W, -40, 37)
    # the warm window with the other self, across from the bridge
    b += f'<ellipse cx="722" cy="822" rx="120" ry="90" fill="url(#warm)" opacity=".45"/>'
    b += '<rect x="690" y="790" width="64" height="64" fill="#f2a46a"/><rect x="690" y="790" width="64" height="64" fill="url(#scan)" opacity=".08"/>'
    b += hooded(722, 854, 50, c="#24150d", staff=False, cloak_dir=1)
    # main sky-bridge and the courier
    b += '<polygon points="230,860 690,860 690,884 230,884" fill="#0a0f12"/>'
    b += '<line x1="230" y1="846" x2="690" y2="846" stroke="#26333b" stroke-width="2"/>'
    for x in range(240, 690, 22):
        b += f'<line x1="{x}" y1="846" x2="{x}" y2="860" stroke="#1b252c" stroke-width="1.5"/>'
    b += '<line x1="230" y1="885" x2="690" y2="885" stroke="#9be8f5" stroke-width="2" opacity=".6" filter="url(#b2)"/>'
    b += ('<circle cx="372" cy="850" r="10" fill="none" stroke="#06090b" stroke-width="3"/>'
          '<circle cx="408" cy="850" r="10" fill="none" stroke="#06090b" stroke-width="3"/>'
          '<path d="M372 850 L388 836 L408 850 M388 836 L396 828" stroke="#06090b" stroke-width="3" fill="none"/>')
    b += hooded(425, 860, 54, c="#06090b", staff=False)
    b += '<rect x="414" y="816" width="16" height="14" fill="#06090b"/><rect x="415" y="820" width="14" height="1.5" fill="#e07a3a" opacity=".9"/>'
    # lower fog, wet abyss and reflections
    b += f'<rect x="0" y="1050" width="{W}" height="550" filter="url(#fogB2)" mask="url(#mB2)" opacity=".45"/>'
    random.seed(17)
    for _ in range(40):
        x = random.uniform(240, 660)
        b += f'<rect x="{x:.1f}" y="{random.uniform(1300, 1500):.1f}" width="{random.uniform(1, 4):.1f}" height="{random.uniform(40, 160):.1f}" fill="{random.choice(["#6fd6e8", "#f0b47a", "#d65a9a", "#cfe9ee"])}" opacity=".18" filter="url(#b6)"/>'
    # rain
    random.seed(23)
    rain = ""
    for _ in range(900):
        x, y, L = random.uniform(-100, W), random.uniform(-50, H), random.uniform(8, 38)
        rain += f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + L*.22:.1f}" y2="{y + L:.1f}" stroke="#cfdde2" stroke-width="{random.uniform(.5, 1.2):.1f}" opacity="{random.uniform(.06, .3):.2f}"/>'
    b += rain
    b += particles(30, 230, 852, 690, 864, "#cfe9ee", .8, 1.8, .2, .5, 29)
    b += f'<rect width="{W}" height="{H}" fill="url(#vign)"/>'
    return W, H, d, b


# ---------------------------------------------------------------- scene C: Ark of Sand
def scene_ark():
    W, H = 1600, 900
    d = COMMON_DEFS
    d += vgrad("skyC", [(0, "#211d1a", 1), (.3, "#3f352d", 1), (.55, "#7c6450", 1), (.66, "#b8936c", 1), (.72, "#caa57c", 1), (1, "#5b4a3b", 1)])
    d += rgrad("sun", [(0, "#fff1d6", 1), (.35, "#f4d3a3", .9), (1, "#f4d3a3", 0)])
    d += rgrad("bloom", [(0, "#f0a060", .55), (1, "#e07a3a", 0)])
    d += vgrad("hullTop", [(0, "#8a7a68", 1), (1, "#4a423a", 1)])
    d += vgrad("hullSide", [(0, "#2e2a27", 1), (1, "#171513", 1)])
    d += vgrad("duneLit", [(0, "#b48d64", 1), (1, "#6e543e", 1)])
    d += vgrad("duneShade", [(0, "#5b4636", 1), (1, "#2f241c", 1)])
    d += vgrad("duneNear", [(0, "#8a6a4c", 1), (1, "#2b2119", 1)])
    d += vgrad("cyanBeam", [(0, "#9be3ee", .45), (1, "#9be3ee", 0)])
    d += rgrad("vign", [(0, "#000", 0), (.62, "#000", 0), (1, "#000", .55)], r=.75)
    d += clouds("storm", "#8f7457", "0.0028 0.006", 9, a=3.2, b=-1.2)
    d += clouds("haze", "#d9b98f", "0.003 0.03", 15, a=2.4, b=-1.2)
    d += clouds("ripple", "#2a1f17", "0.002 0.11", 4, a=2.6, b=-1.4, octaves=3)
    d += band_mask("mStorm", 250, 640, W) + band_mask("mHaze", 540, 700, W)
    d += ('<mask id="cStorm" maskUnits="userSpaceOnUse" x="0" y="0" width="1600" height="900">'
          '<path d="M-60 660 L-60 330 Q180 250 380 300 Q560 240 760 330 Q880 380 960 660Z" fill="#fff" filter="url(#b40)"/></mask>')

    b = f'<rect width="{W}" height="{H}" fill="url(#skyC)"/>'
    b += '<circle cx="1030" cy="470" r="260" fill="url(#bloom)" filter="url(#b40)"/>'
    b += '<ellipse cx="1030" cy="560" rx="760" ry="60" fill="#f2c98e" opacity=".25" filter="url(#b40)"/>'
    b += '<circle cx="1030" cy="470" r="64" fill="url(#sun)"/>'
    # sandstorm wall (haboob) on the left horizon
    b += f'<g mask="url(#cStorm)"><rect x="0" y="200" width="1000" height="460" filter="url(#storm)"/>'
    b += '<rect x="0" y="200" width="1000" height="460" fill="#7d6450" opacity=".4"/></g>'
    # ornithopters (side view, wings a motion blur)
    for x, y, sc in ((540, 175, 1), (700, 235, .55)):
        b += (f'<g transform="translate({x} {y}) scale({sc})">'
              f'<ellipse cx="0" cy="-9" rx="44" ry="5" fill="#2a221c" opacity=".45" filter="url(#b2)"/>'
              f'<ellipse cx="6" cy="-11" rx="30" ry="3" fill="#2a221c" opacity=".35" filter="url(#b2)"/>'
              f'<path d="M-30 0 Q-24 -6 -6 -6 L18 -6 Q30 -6 34 0 Q30 5 18 5 L-6 5 Q-24 5 -30 0Z" fill="#221b16"/>'
              f'<path d="M-30 0 L-58 -2 L-58 2Z" fill="#221b16"/><circle cx="26" cy="-1" r="3.2" fill="#3a3029"/>'
              f'<line x1="-10" y1="5" x2="-14" y2="12" stroke="#221b16" stroke-width="1.5"/><line x1="12" y1="5" x2="16" y2="12" stroke="#221b16" stroke-width="1.5"/></g>')
    # distant rock formations
    b += '<polygon points="1180,600 1210,548 1260,540 1290,560 1350,552 1380,600" fill="#8a6c52" opacity=".7"/>'
    b += '<polygon points="1380,604 1420,520 1500,505 1530,530 1600,522 1600,604" fill="#7a5f49" opacity=".75"/>'
    # far dunes
    b += '<path d="M0 640 C200 600 380 630 560 610 S900 590 1100 612 S1420 590 1600 606 L1600 700 L0 700Z" fill="#a07e5c"/>'
    b += '<path d="M0 640 C200 600 380 630 560 610 S900 590 1100 612 S1420 590 1600 606" fill="none" stroke="#e3c59b" stroke-width="1.4" opacity=".5"/>'
    # old wreck ribs
    for i in range(6):
        x = 150 + i * 46
        b += f'<path d="M{x} 660 Q{x + 22} {585 - i*3} {x + 60} {566 + i*2}" stroke="#3b2f26" stroke-width="{7 - i*.6:.1f}" fill="none"/>'
    # the colony ship: a long faceted hull, bow raised to the right
    top = [(520, 600), (1480, 332)]
    b += f'<polygon points="520,600 1480,332 1530,322 1505,372 560,640" fill="url(#hullTop)"/>'
    b += f'<polygon points="560,640 1505,372 1460,560 620,720" fill="url(#hullSide)"/>'
    b += '<polyline points="520,600 1480,332 1530,322" fill="none" stroke="#f0d5ac" stroke-width="2" opacity=".6"/>'
    for i in range(1, 16):
        t = i / 16
        x0, y0 = 520 + 960 * t, 600 - 268 * t
        x1, y1 = 560 + 945 * t, 640 - 268 * t
        x2, y2 = 620 + 840 * t, 720 - 160 * t
        b += f'<polyline points="{x0:.1f},{y0:.1f} {x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="#14110f" stroke-width="1.6" opacity=".7"/>'
    random.seed(6)
    for row in range(3):
        for i in range(60):
            t = (i + .5) / 60
            x = 580 + 900 * t
            y = 655 - 260 * t + row * 16 - row * 4 * t
            if random.random() < .6:
                b += f'<rect x="{x:.1f}" y="{y:.1f}" width="5" height="2.4" fill="#0a0908" opacity=".9"/>'
    # torn plating showing ribs
    b += '<polygon points="880,560 980,532 1000,600 900,628" fill="#0c0a09"/>'
    for i in range(6):
        b += f'<line x1="{886 + i*18}" y1="{556 - i*5}" x2="{902 + i*18}" y2="{624 - i*5}" stroke="#3a312a" stroke-width="2.4"/>'
    # spines and antennas on the hull
    for x, y, h in ((1100, 440, 60), (1180, 418, 90), (1260, 396, 50), (1360, 368, 70)):
        b += f'<line x1="{x}" y1="{y}" x2="{x + 6}" y2="{y - h}" stroke="#2a241f" stroke-width="2.4"/>'
    # the hatch: cyan light spilling onto the sand
    b += '<polygon points="1152,508 1186,498 1190,532 1156,542" fill="#c9f3f9"/>'
    b += '<polygon points="1156,542 1190,532 1260,700 1060,720" fill="url(#cyanBeam)" filter="url(#b6)"/>'
    b += glow(1171, 520, 10, "#8fe0ec", op=.9, core="#e9fbfd")
    # mid dune burying the hull
    b += '<path d="M0 700 C260 650 480 690 700 668 C900 648 1060 690 1240 676 C1400 664 1520 690 1600 680 L1600 900 L0 900Z" fill="url(#duneLit)"/>'
    b += '<path d="M0 700 C260 650 480 690 700 668 C900 648 1060 690 1240 676 C1400 664 1520 690 1600 680" fill="none" stroke="#efd2a6" stroke-width="1.6" opacity=".55"/>'
    b += f'<rect x="0" y="540" width="{W}" height="160" filter="url(#haze)" mask="url(#mHaze)" opacity=".45"/>'
    # near dune crest with ripples and the scavenger
    crest = "M620 900 C820 840 1040 790 1300 772 C1420 766 1520 790 1600 806 L1600 900Z"
    b += f'<path d="{crest}" fill="url(#duneNear)"/>'
    b += '<path d="M1300 772 C1420 766 1520 790 1600 806 L1600 900 L1340 900Z" fill="#1d1712" opacity=".55"/>'
    b += f'<clipPath id="cCrest"><path d="{crest}"/></clipPath>'
    b += f'<g clip-path="url(#cCrest)"><rect x="600" y="760" width="1000" height="140" filter="url(#ripple)" opacity=".7"/></g>'
    b += '<path d="M620 900 C820 840 1040 790 1300 772 C1420 766 1520 790 1600 806" fill="none" stroke="#f2d4a4" stroke-width="2" opacity=".65"/>'
    b += '<path d="M1300 770 C1200 760 1080 762 980 772" stroke="#e8cfa6" stroke-width="10" opacity=".12" fill="none" filter="url(#b6)"/>'
    b += '<ellipse cx="1250" cy="782" rx="80" ry="5" fill="#120d09" opacity=".5" filter="url(#b2)"/>'
    b += hooded(1300, 772, 66)
    # dust
    b += particles(260, 0, 300, W, H, "#f1d7ae", .5, 1.4, .15, .55, 31)
    b += particles(24, 0, 400, W, H, "#f1d7ae", 4, 9, .06, .16, 32, blurred=True)
    b += f'<rect width="{W}" height="{H}" fill="url(#vign)"/>'
    return W, H, d, b


# ---------------------------------------------------------------- posters and rendering
def poster_overlay(x, y, w, h, title, line):
    return (f'<linearGradient id="pfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B0D10" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#0B0D10" stop-opacity=".92"/></linearGradient>'
            f'<rect x="{x}" y="{y + h*.72}" width="{w}" height="{h*.28}" fill="url(#pfade)"/>'
            f'<text x="{x + w/2}" y="{y + h*.915}" text-anchor="middle" font-family="Archivo" style="font-stretch:125%" '
            f'font-weight="300" font-size="{w*.064:.1f}" letter-spacing="{w*.018:.1f}" fill="#E4E6E3">{title}</text>'
            f'<text x="{x + w/2}" y="{y + h*.955}" text-anchor="middle" font-family="IBM Plex Mono" font-size="{w*.019:.1f}" '
            f'letter-spacing="{w*.006:.1f}" fill="#8FB3C0">{line}</text>')


def render(name, scene, out_w, out_h, view=None, overlay=""):
    W, H, defs, body = scene
    vx, vy, vw, vh = view or (0, 0, W, H)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{out_w}" height="{out_h}" viewBox="{vx} {vy} {vw} {vh}" '
           f'preserveAspectRatio="xMidYMid slice"><defs>{defs}</defs>{body}{overlay}</svg>')
    page = (f'<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}">'
            f'<style>html,body{{margin:0;background:#000;overflow:hidden}}svg{{display:block}}</style></head><body>{svg}</body></html>')
    html_path = os.path.join(WORK, name + ".html")
    png_path = os.path.join(WORK, name + ".png")
    with open(html_path, "w") as f:
        f.write(page)
    if os.path.exists(png_path):
        os.remove(png_path)
    profile = tempfile.mkdtemp(prefix="chq")
    proc = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={profile}",
                             "--no-first-run", "--virtual-time-budget=8000", f"--window-size={out_w},{out_h}",
                             f"--screenshot={png_path}", "file://" + html_path],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(240):
        if os.path.exists(png_path) and os.path.getsize(png_path) > 0:
            time.sleep(.8)
            break
        time.sleep(.5)
    proc.kill()
    shutil.rmtree(profile, ignore_errors=True)
    jpg = os.path.join(OUT, name + ".jpg")
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", png_path, "--out", jpg],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"{name}.jpg  {out_w}x{out_h}  {os.path.getsize(jpg)//1024} KB")


if __name__ == "__main__":
    A, B, C = scene_last_signal(), scene_backup(), scene_ark()
    render("last-signal-key", A, 2400, 1350)
    render("last-signal-mobile", A, 1080, 1568, view=(980, 0, 620, 900))
    render("last-signal-poster", A, 1200, 1800, view=(1000, 0, 600, 900),
           overlay=poster_overlay(1000, 0, 600, 900, "LAST SIGNAL", "A NOVA INTELLIGENCE SERIES · 16:9"))
    render("backup-key", B, 1080, 1920)
    render("backup-poster", B, 1200, 1800, view=(0, 130, 900, 1350),
           overlay=poster_overlay(0, 130, 900, 1350, "BACKUP", "A NOVA INTELLIGENCE SERIES · 9:16"))
    render("ark-of-sand-key", C, 2400, 1350)
    render("ark-of-sand-vertical", C, 1080, 1920, view=(1000, 0, 506, 900))
    render("ark-of-sand-poster", C, 1200, 1800, view=(900, 0, 600, 900),
           overlay=poster_overlay(900, 0, 600, 900, "ARK OF SAND", "A NOVA INTELLIGENCE SERIES · 16:9 + 9:16"))
