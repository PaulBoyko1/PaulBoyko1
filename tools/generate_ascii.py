from __future__ import annotations
import html
import math
import random
from pathlib import Path

COLS, ROWS = 320, 94
OUT = Path("ascii-profile-v5.svg")
grid = [[" "] * COLS for _ in range(ROWS)]

def put(x: int, y: int, text: str, overwrite: bool = True) -> None:
    if not (0 <= y < ROWS):
        return
    for i, ch in enumerate(text):
        xx = x + i
        if 0 <= xx < COLS and (overwrite or grid[y][xx] == " "):
            grid[y][xx] = ch

def hline(x1: int, x2: int, y: int, ch: str = "-") -> None:
    for x in range(max(0, x1), min(COLS, x2 + 1)):
        grid[y][x] = ch

def vline(x: int, y1: int, y2: int, ch: str = "|") -> None:
    for y in range(max(0, y1), min(ROWS, y2 + 1)):
        grid[y][x] = ch

def box(x1: int, y1: int, x2: int, y2: int, title: str = "") -> None:
    put(x1, y1, "+")
    put(x2, y1, "+")
    put(x1, y2, "+")
    put(x2, y2, "+")
    hline(x1 + 1, x2 - 1, y1)
    hline(x1 + 1, x2 - 1, y2)
    vline(x1, y1 + 1, y2 - 1)
    vline(x2, y1 + 1, y2 - 1)
    if title:
        put(x1 + 3, y1, f"[ {title} ]")

FONT = {
    "P": ["11110","10001","10001","11110","10000","10000","10000"],
    "A": ["01110","10001","10001","11111","10001","10001","10001"],
    "U": ["10001","10001","10001","10001","10001","10001","01110"],
    "L": ["10000","10000","10000","10000","10000","10000","11111"],
    "B": ["11110","10001","10001","11110","10001","10001","11110"],
    "O": ["01110","10001","10001","10001","10001","10001","01110"],
    "Y": ["10001","10001","01010","00100","00100","00100","00100"],
    "K": ["10001","10010","10100","11000","10100","10010","10001"],
}
RAMP = " .`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
DARK = RAMP[40:]

def draw_textured_name(text: str, x: int, y: int, sx: int = 5, sy: int = 3) -> None:
    random.seed(20260808)
    cursor = x
    for letter in text:
        if letter == " ":
            cursor += sx * 2
            continue
        pattern = FONT[letter]
        for gy, row in enumerate(pattern):
            for gx, bit in enumerate(row):
                if bit != "1":
                    continue
                for yy in range(sy):
                    for xx in range(sx):
                        px = cursor + gx * sx + xx
                        py = y + gy * sy + yy
                        tone = 0.5 + 0.25 * math.sin(px * 0.23 + py * 0.47) + 0.25 * random.random()
                        idx = max(0, min(len(DARK)-1, int(tone * (len(DARK)-1))))
                        put(px, py, DARK[idx])
        cursor += 5 * sx + 2

def background_field(x0: int, y0: int, x1: int, y1: int) -> None:
    random.seed(808)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            v = (
                0.46 * math.sin(x * 0.108 + y * 0.49)
                + 0.33 * math.cos(x * 0.043 - y * 0.77)
                + 0.22 * math.sin((x + y) * 0.073)
                + random.uniform(-0.28, 0.28)
            )
            if v > 0.85:
                put(x, y, random.choice(":;,`'~"), overwrite=False)
            elif v > 0.55 and random.random() < 0.55:
                put(x, y, random.choice("..,,"), overwrite=False)

box(0, 0, COLS - 1, ROWS - 1)
put(4, 0, " PAUL BOYKO / COMPUTER SCIENCE @ UC DAVIS / SOFTWARE ENGINEERING + ML + SYSTEMS ")
put(COLS - 44, 0, " ascii.profile / density-320x94 ")
put(4, 2, "stack:// python / c++ / typescript / fastapi / git")
put(4, 3, "method: build -> instrument -> test -> measure -> iterate")
put(205, 2, "field: data / simulation / APIs / research")
put(205, 3, "status: shipping projects / adding more soon")
hline(1, COLS - 2, 5, ".")
put(4, 5, "+ 320 columns / long density ramp / 1.15s scanline reveal +")

background_field(4, 7, COLS - 5, 39)
name = "PAUL BOYKO"
name_width = sum((5 * 5 + 2) if ch != " " else 10 for ch in name)
draw_textured_name(name, (COLS - name_width)//2, 12, 5, 3)
put(8, 8, ":: printable ASCII / micro-raster / density shading ::")
put(246, 38, ":: texture > blocks ::")

hline(1, COLS - 2, 42, "-")
put(4, 42, " PROJECT FIELD / THREE LIVE BUILDS ")

gap = 3
usable = COLS - 2
pw = (usable - 2 * gap) // 3
p1 = (1, 44, pw, 85)
p2 = (pw + gap + 1, 44, 2 * pw + gap, 85)
p3 = (2 * pw + 2 * gap + 1, 44, COLS - 2, 85)
for coords, title in [
    (p1, "01 / CRYPTO INTERVAL ANALYZER"),
    (p2, "02 / MANDELBROT EXPLORER"),
    (p3, "03 / PARTICLE ENGINE"),
]:
    box(*coords, title)

# Panel 1: market research
xL, yT, xR, yB = p1
put(xL+3, yT+2, "fixed-window market research / 15m + 1h")
put(xL+3, yT+3, "live API -> signal -> backtest -> OOS validation")
put(xL+3, yT+5, "OPEN       LAST       FAIR       BRIER       STATE")
put(xL+3, yT+6, "67418.2    67461.9    0.533      0.192       TEST")
put(xL+3, yT+8, "price")
cx0, cy0 = xL + 4, yT + 10
cw, ch = xR - xL - 8, 20
for gy in [0,5,10,15,19]:
    hline(cx0, cx0+cw, cy0+gy, ".")
vline(cx0, cy0, cy0+ch)
random.seed(22)
v, vals = 50, []
for _ in range(28):
    v = max(12, min(88, v + random.choice([-4,-3,-2,-1,1,2,3,4,5])))
    vals.append(v)
for i, val in enumerate(vals):
    x = round(cx0 + 2 + i * (cw-4)/(len(vals)-1))
    yy = cy0 + ch - 1 - round(val/100*(ch-2))
    put(x, yy, "*")
    for w in range(1, random.randint(1,3)+1):
        if yy-w >= cy0: put(x, yy-w, "|")
        if yy+w <= cy0+ch: put(x, yy+w, "|")
    if i:
        px = round(cx0 + 2 + (i-1)*(cw-4)/(len(vals)-1))
        py = cy0 + ch - 1 - round(vals[i-1]/100*(ch-2))
        steps = max(1, x-px)
        for s in range(1, steps):
            xx = px+s
            yi = round(py+(yy-py)*s/steps)
            put(xx, yi, "/" if yy < py else "\\" if yy > py else "-")
put(xL+3, yB-7, "walk-forward  [##########------]  62%")
put(xL+3, yB-5, "bootstrap     [############----]  75%")
put(xL+3, yB-3, "python / fastapi / typescript / REST APIs")
put(xL+3, yB-2, "public data / research only / no execution")

# Panel 2: actual Mandelbrot
xL, yT, xR, yB = p2
put(xL+3, yT+2, "complex plane / mouse-centered zoom / iterations")
mcols, mrows = xR-xL-6, 31
mramp = " .,:;irsXA253hMHGS#9B&@"
for iy in range(mrows):
    cy = -1.13 + iy*(2.26/(mrows-1))
    row = []
    for ix in range(mcols):
        cx = -2.20 + ix*(3.12/(mcols-1))
        z, c, n, maxit = 0j, complex(cx,cy), 0, 36
        while z.real*z.real + z.imag*z.imag <= 4 and n < maxit:
            z = z*z + c
            n += 1
        if n == maxit:
            row.append("@")
        else:
            q = (n/maxit)**0.58
            row.append(mramp[min(len(mramp)-1, int(q*(len(mramp)-1)))])
    put(xL+3, yT+5+iy, "".join(row))
put(xL+3, yB-3, "c++ / sfml / complex-coordinate mapping")
put(xL+3, yB-2, "render -> zoom -> remap -> iterate")

# Panel 3: particle field
xL, yT, xR, yB = p3
put(xL+3, yT+2, "interactive simulation / lifecycle / cleanup")
put(xL+3, yT+3, "click -> spawn -> update(dt) -> decay -> erase")
px0, py0, px1, py1 = xL+4, yT+6, xR-4, yB-9
random.seed(3301)
nodes = [(random.randint(px0,px1), random.randint(py0,py1)) for _ in range(52)]
for i, (x,y) in enumerate(nodes):
    nearest = sorted(
        (abs(x-x2)+abs(y-y2), x2, y2)
        for j,(x2,y2) in enumerate(nodes) if j != i
    )[0]
    dist, x2, y2 = nearest
    if dist < 19:
        dx, dy = x2-x, y2-y
        steps = max(abs(dx), abs(dy))
        for s in range(1, steps):
            xx = round(x + dx*s/steps)
            yy = round(y + dy*s/steps)
            if abs(dx) > 2*abs(dy): ch = "-"
            elif abs(dy) > 2*abs(dx): ch = "|"
            else: ch = "/" if dx*dy < 0 else "\\"
            put(xx, yy, ch, overwrite=False)
for i,(x,y) in enumerate(nodes):
    put(x, y, "*" if i % 7 == 0 else "o")
put(xL+3, yB-7, "particles : 0048    active : 0031    dead : 0017")
put(xL+3, yB-5, "lifetime  : [###########-----]  68%")
put(xL+3, yB-3, "c++ / sfml / unit tests")
put(xL+3, yB-2, "time-based updates / automatic cleanup")

hline(1, COLS-2, 87, ".")
put(4, 89, "projects/ 01 interval-analyzer // 02 mandelbrot // 03 particles // + more soon")
put(4, 90, "principle/ clear code :: reproducible experiments :: useful software")
put(4, 92, "github.com/PaulBoyko1")
put(COLS-58, 92, "[ build -> test -> measure -> iterate -> repeat ]")

lines = ["".join(row).rstrip() for row in grid]
accent_rows = {0,5,8,42,44,89}
muted_rows = {2,3,90,92}
frame_rows = {1,4,6,41,43,86,87,88,91,93}

svg = [
    '<svg viewBox="0 0 650 610" width="650" height="610" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="High-density ASCII profile for Paul Boyko" xml:space="preserve">',
    '<style>.a{font-family:SFMono-Regular,Consolas,"Liberation Mono",Menlo,monospace;font-size:5.65px;font-weight:500;white-space:pre;fill:#3d444d}.x{fill:#0969da;font-weight:700}.m{fill:#6e7781}.f{fill:#8c959f}@media(prefers-color-scheme:dark){.a{fill:#c9d1d9}.x{fill:#58a6ff}.m{fill:#8b949e}.f{fill:#484f58}}</style>',
    '<defs><clipPath id="scan"><rect x="0" y="0" width="650" height="0"><animate attributeName="height" from="0" to="610" dur="1.15s" fill="freeze"/></rect></clipPath></defs>',
    '<text class="a" x="8" y="10" clip-path="url(#scan)">',
]
for i, line in enumerate(lines):
    cls = "x" if i in accent_rows else "m" if i in muted_rows else "f" if i in frame_rows else ""
    attr = f' class="{cls}"' if cls else ""
    if i == 0:
        svg.append(f'<tspan{attr} x="8">{html.escape(line, quote=False)}</tspan>')
    else:
        svg.append(f'<tspan{attr} x="8" dy="6.35">{html.escape(line, quote=False)}</tspan>')
svg.append("</text></svg>")
OUT.write_text("\n".join(svg), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
