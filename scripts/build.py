"""Generates README.md and every SVG under assets/gen/ from config.py.

    pip install pillow
    python scripts/build.py
"""
import html, math, os, random, sys, textwrap
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(__file__))
import config as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = "assets/gen"

# palette: deep space panel, one cold accent, one warm signal
VOID, PANEL, LINE = "#04060c", "#080d18", "#16243a"
CYAN, CYAN_DIM, AMBER, LIME = "#38e8ff", "#0e6378", "#ffb547", "#7dffb2"
TEXT, MUTED, WHITE = "#cfe6f0", "#5d7689", "#ffffff"
STATUS = {"LIVE": LIME, "ACTIVE": AMBER, "SHIPPED": CYAN}

MONO = "'JetBrains Mono','SF Mono',ui-monospace,Menlo,Consolas,monospace"
ARABIC = "'Noto Kufi Arabic','Geeza Pro','Segoe UI',Tahoma,sans-serif"
CHAR = 0.6  # monospace advance, as a fraction of font size
esc = lambda s: html.escape(str(s), quote=True)

BASE_CSS = f"""
text{{font-family:{MONO}}}
.ar{{font-family:{ARABIC}}}
.em{{font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif}}
@keyframes fade{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
.in{{opacity:0;animation:fade .6s cubic-bezier(.2,.7,.2,1) forwards}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.2}}}}
.pulse{{animation:pulse 1.8s ease-in-out infinite}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.blink{{animation:blink 1s step-end infinite}}
@keyframes reveal{{to{{clip-path:inset(0 0 0 0)}}}}
.rv{{clip-path:inset(0 100% 0 0);animation:reveal .14s linear forwards}}
@keyframes sweep{{from{{transform:translateY(-40px)}}to{{transform:translateY(var(--h))}}}}
.beam{{animation:sweep 5s linear infinite}}
@keyframes dash{{to{{stroke-dashoffset:0}}}}
"""
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}.in{opacity:1}.rv{clip-path:none}}"


def svg(w, h, body, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
            f'<style>{BASE_CSS}{css}{REDUCED}</style>\n{body}\n</svg>\n')


def delay(t):
    return f'style="animation-delay:{t:.2f}s"'


def brackets(x, y, w, h, s=14, color=CYAN, width=1.5):
    """HUD corner brackets around a box."""
    d = (f"M{x} {y+s}V{y}H{x+s} M{x+w-s} {y}H{x+w}V{y+s} "
         f"M{x+w} {y+h-s}V{y+h}H{x+w-s} M{x+s} {y+h}H{x}V{y+h-s}")
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"/>'


def panel(w, h, c=16):
    """Chamfered panel with a scanline texture and a sweeping beam."""
    shape = f"M{c} .5H{w-.5}V{h-c}L{w-c} {h-.5}H.5V{c}Z"
    return f'''<defs>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="{WHITE}" opacity=".025"/></pattern>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".09"/></linearGradient>
<clipPath id="pc"><path d="{shape}"/></clipPath>
</defs>
<path d="{shape}" fill="{PANEL}" stroke="{LINE}"/>
<g clip-path="url(#pc)"><rect width="{w}" height="{h}" fill="url(#scan)"/>
<rect class="beam" style="--h:{h}px" width="{w}" height="40" fill="url(#beam)"/></g>
<path d="M.5 {c+18}V{c}L{c} .5H{c+18} M{w-.5} {h-c-18}V{h-c}L{w-c} {h-.5}H{w-c-18}" fill="none" stroke="{CYAN}" stroke-width="1.5"/>'''


def header(w, left, right):
    return (f'<text x="22" y="30" font-size="11" letter-spacing="2.5" fill="{MUTED}">'
            f'<tspan fill="{CYAN}">◢ </tspan>{esc(left)}</text>'
            f'<circle class="pulse" cx="{w-28}" cy="26" r="3.5" fill="{LIME}"/>'
            f'<text x="{w-40}" y="30" font-size="11" letter-spacing="2.5" fill="{MUTED}" text-anchor="end">{esc(right)}</text>'
            f'<line x1="22" y1="44" x2="{w-22}" y2="44" stroke="{LINE}"/>')


# ---------- hero ----------
def hero():
    w, h, horizon = 1280, 420, 300
    rnd = random.Random(7)
    stars = "".join(
        f'<circle class="tw" cx="{rnd.uniform(0, w):.0f}" cy="{rnd.uniform(0, horizon - 10):.0f}" r="{rnd.uniform(.5, 1.4):.1f}" '
        f'fill="{WHITE}" style="animation-delay:-{rnd.uniform(0, 4):.1f}s"/>' for _ in range(90))

    vanish = w / 2
    verticals = "".join(f'<line x1="{vanish}" y1="{horizon}" x2="{vanish + k * 150}" y2="{h}"/>' for k in range(-14, 15))
    rows = 9
    horizontals = "".join(f'<line class="fl" x1="0" y1="{horizon}" x2="{w}" y2="{horizon}" style="animation-delay:-{i * 4 / rows:.2f}s"/>'
                          for i in range(rows))

    # rotating tagline: each line types in, holds, then hands over to the next
    n, slot, fs = len(C.TYPING_LINES), 4.0, 18
    p = 100 / n
    ty_css = (f"@keyframes ty{{0%{{opacity:1;clip-path:inset(0 100% 0 0);animation-timing-function:steps(28,end)}}"
              f"{p * .35:.2f}%{{clip-path:inset(0 0 0 0)}}{p * .92:.2f}%{{opacity:1}}{p:.2f}%,100%{{opacity:0;clip-path:inset(0 0 0 0)}}}}"
              f".ty{{opacity:0;animation:ty {n * slot}s linear infinite both}}"
              "@media (prefers-reduced-motion:reduce){.ty0{opacity:1;clip-path:none}}")
    typing = []
    for i, line in enumerate(C.TYPING_LINES):
        tl = len(line) * CHAR * fs
        x0 = (w - tl) / 2
        typing.append(
            f'<g class="ty ty{i}" style="animation-delay:{i * slot:.1f}s">'
            f'<text x="{x0 - 22:.1f}" y="250" font-size="{fs}" fill="{CYAN}">›</text>'
            f'<text x="{x0:.1f}" y="250" font-size="{fs}" fill="{TEXT}" textLength="{tl:.1f}" lengthAdjust="spacing">{esc(line)}</text>'
            f'<rect class="blink" x="{x0 + tl + 4:.1f}" y="235" width="9" height="19" fill="{CYAN}"/></g>')

    brand = C.BRAND.upper()
    title = (f'<text x="{w/2}" y="150" font-size="76" font-weight="800" letter-spacing="16" text-anchor="middle" %s>{esc(brand)}</text>')
    now = "  ·  ".join(C.NOW).upper()

    css = f"""
@keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:.9}}}}
.tw{{animation:tw 4s ease-in-out infinite}}
@keyframes fl{{from{{transform:translateY(0);opacity:0}}to{{transform:translateY({h - horizon}px);opacity:1}}}}
.fl{{animation:fl 4s cubic-bezier(.55,0,1,.45) infinite}}
@keyframes ga{{0%,88%,100%{{opacity:0;transform:none}}89%{{opacity:.85;transform:translate(-6px,1px);clip-path:inset(12% 0 58% 0)}}
91%{{opacity:.85;transform:translate(5px,-1px);clip-path:inset(62% 0 10% 0)}}93%{{opacity:.6;transform:translate(-3px,0);clip-path:inset(35% 0 40% 0)}}94%{{opacity:0}}}}
.ga{{animation:ga 7s steps(1,end) infinite}}.gb{{animation:ga 7s steps(1,end) infinite;animation-delay:.08s}}
.orbit{{stroke-dasharray:6 10;stroke-dashoffset:320;animation:dash 12s linear infinite}}
{ty_css}"""

    body = f'''<defs>
<radialGradient id="glow" cx=".5" cy=".72" r=".6"><stop offset="0" stop-color="{CYAN}" stop-opacity=".22"/><stop offset=".55" stop-color="{CYAN}" stop-opacity=".04"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<linearGradient id="nameg" x1="0" y1="0" x2="0" y2="1"><stop offset=".2" stop-color="{WHITE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="floorfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{WHITE}" stop-opacity="0"/><stop offset="1" stop-color="{WHITE}" stop-opacity="1"/></linearGradient>
<mask id="floormask"><rect y="{horizon}" width="{w}" height="{h - horizon}" fill="url(#floorfade)"/></mask>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="{WHITE}" opacity=".03"/></pattern>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".07"/></linearGradient>
<clipPath id="frame"><rect width="{w}" height="{h}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="{w}" height="{h}" fill="{VOID}"/>
<rect width="{w}" height="{h}" fill="url(#glow)"/>
{stars}
<ellipse class="orbit" cx="{vanish}" cy="{horizon - 8}" rx="560" ry="54" fill="none" stroke="{CYAN}" stroke-opacity=".35"/>
<circle r="3" fill="{AMBER}"><animateMotion dur="12s" repeatCount="indefinite" path="M{vanish - 560} {horizon - 8}a560 54 0 1 0 1120 0a560 54 0 1 0 -1120 0"/></circle>
<g mask="url(#floormask)" stroke="{CYAN}" stroke-opacity=".45">{verticals}{horizontals}</g>
<line x1="0" y1="{horizon}" x2="{w}" y2="{horizon}" stroke="{CYAN}" stroke-opacity=".7"/>
<rect width="{w}" height="{h}" fill="url(#scan)"/>
<rect class="beam" style="--h:{h}px" width="{w}" height="40" fill="url(#beam)"/>

<g class="in" {delay(.1)}>{header(w, f"{brand}/OS  ·  SYS.ONLINE", f"EST. {C.SINCE}  ·  RTL / OFFLINE-FIRST")}</g>
<g class="in" {delay(.35)}>
{title % f'fill="url(#nameg)"'}
<g class="ga">{title % f'fill="{CYAN}"'}</g><g class="gb">{title % f'fill="{AMBER}"'}</g>
</g>
<g class="in" {delay(.6)}>
<line x1="{w/2 - 300}" y1="186" x2="{w/2 - 190}" y2="186" stroke="{CYAN}" stroke-opacity=".6"/>
<text x="{w/2 - 12}" y="192" font-size="16" letter-spacing="5" fill="{TEXT}" text-anchor="end">{esc(C.NAME.upper())}</text>
<text x="{w/2}" y="192" font-size="16" fill="{CYAN}" text-anchor="middle">·</text>
<text class="ar" x="{w/2 + 12}" y="193" font-size="19" fill="{TEXT}" text-anchor="end" direction="rtl">{esc(C.NAME_AR)}</text>
<line x1="{w/2 + 190}" y1="186" x2="{w/2 + 300}" y2="186" stroke="{CYAN}" stroke-opacity=".6"/>
</g>
{"".join(typing)}
<g class="in" {delay(.9)}>
<rect x="22" y="{h - 44}" width="{w - 44}" height="26" fill="{VOID}" fill-opacity=".72"/>
<text x="32" y="{h - 26}" font-size="11" letter-spacing="2.5" fill="{MUTED}">NOW BUILDING <tspan fill="{AMBER}">▸</tspan> <tspan fill="{TEXT}">{esc(now)}</tspan></text>
<text x="{w - 32}" y="{h - 26}" font-size="11" letter-spacing="2.5" fill="{MUTED}" text-anchor="end">UPTIME <tspan fill="{TEXT}">SINCE {C.SINCE}</tspan></text>
</g>
{brackets(10, 10, w - 20, h - 20, s=22)}
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="{LINE}"/>'''
    return svg(w, h, body, css)


# ---------- ASCII portrait from a photo ----------
RAMP = " .`'-:;=+*sS%#@"
COLS, ROWS = 72, 42

def to_ascii(img):
    px = img.load()
    return ["".join(RAMP[min(len(RAMP) - 1, int(px[x, y] / 255 * len(RAMP)))] for x in range(COLS)) for y in range(ROWS)]


def ascii_rows(path):
    from PIL import Image, ImageOps, ImageFilter
    img = Image.open(path)
    img = (ImageOps.exif_transpose(img) or img).convert("L")
    # characters are ~2x taller than wide, so the source crop is wider than the grid
    w, h = img.size
    target = COLS / ROWS * 0.55
    cw, ch = (w, int(w / target)) if w / h < target else (int(h * target), h)
    cw, ch = min(cw, w), min(ch, h)
    left, top = (w - cw) // 2, max(0, int((h - ch) * 0.25))
    img = img.crop((left, top, left + cw, top + ch))
    img = ImageOps.autocontrast(img, cutoff=2).filter(ImageFilter.SHARPEN)
    return to_ascii(img.resize((COLS, ROWS)))


def placeholder_rows():
    """Brand monogram used until a photo is added."""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("L", (COLS * 8, ROWS * 16), 0)
    d = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype("DejaVuSans-Bold.ttf", 380)
    except OSError:
        try:
            f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 380)
        except OSError:
            f = ImageFont.load_default()
    d.text((img.width / 2, img.height / 2), "ZC", fill=255, font=f, anchor="mm")
    return to_ascii(img.resize((COLS, ROWS)))


LH, CW = 14, 7.6           # portrait line height / char width
CARD_H = 74 + ROWS * LH + 52  # portrait and spec sheet share this size
PORTRAIT_W = round(22 * 2 + COLS * CW)


def portrait():
    photo = os.path.join(ROOT, C.PHOTO)
    lines = ascii_rows(photo) if os.path.exists(photo) else placeholder_rows()
    x0, y0 = 22, 74
    w = PORTRAIT_W
    h = CARD_H
    parts = [panel(w, h), header(w, "VISUAL.ID  //  ./portrait.sh", "REC"),
             f'<defs><linearGradient id="ag" gradientUnits="userSpaceOnUse" x1="0" y1="{y0}" x2="0" y2="{y0 + ROWS * LH}">'
             f'<stop offset="0" stop-color="{CYAN}"/><stop offset=".45" stop-color="{WHITE}"/><stop offset="1" stop-color="{CYAN_DIM}"/></linearGradient></defs>']
    step = 0.05
    for i, line in enumerate(lines):
        parts.append(f'<text class="rv" {delay(.4 + i * step)} xml:space="preserve" x="{x0}" y="{y0 + i * LH}" fill="url(#ag)" '
                     f'font-size="12.6" textLength="{COLS * CW:.0f}" lengthAdjust="spacing">{esc(line)}</text>')
    end = .4 + ROWS * step + .2
    yb = y0 + ROWS * LH + 18
    parts.append(f'<g class="in" {delay(end)}><text x="{x0}" y="{yb}" font-size="12.5"><tspan fill="{CYAN}">$ </tspan>'
                 f'<tspan fill="{WHITE}" font-weight="700">{esc(C.BRAND)}</tspan>'
                 f'<tspan fill="{MUTED}"> · {esc(C.TAGLINE)}</tspan></text></g>')
    parts.append(f'<g class="in" {delay(end + .3)}><rect class="blink" x="{x0}" y="{yb + 9}" width="8" height="14" fill="{CYAN}"/></g>')
    return svg(w, h, "\n".join(parts))


# ---------- spec sheet ----------
def spec_card():
    w, h = PORTRAIT_W, CARD_H
    top, bottom = 84, h - 74
    row = (bottom - top) / len(C.INFO)
    parts = [panel(w, h), header(w, f"SYS.PROFILE  //  {C.GITHUB_USER.lower()}", "OK")]
    for i, (label, value) in enumerate(C.INFO):
        y = top + i * row + row / 2 + 4
        parts.append(
            f'<g class="in" {delay(.4 + i * .09)}>'
            f'<text x="22" y="{y:.1f}" font-size="10.5" letter-spacing="2" fill="{CYAN}">{i + 1:02d}  {esc(label.upper())}</text>'
            f'<text x="{w - 22}" y="{y:.1f}" font-size="12.5" fill="{TEXT}" text-anchor="end">{esc(value)}</text>'
            f'<line x1="22" y1="{top + (i + 1) * row:.1f}" x2="{w - 22}" y2="{top + (i + 1) * row:.1f}" stroke="{LINE}" stroke-dasharray="2 4"/></g>')
    # signal meter: segments light up in a loop
    segs = 24
    sw = (w - 44 - (segs - 1) * 4) / segs
    meter = "".join(
        f'<rect class="seg" x="{22 + i * (sw + 4):.1f}" y="{h - 44}" width="{sw:.1f}" height="12" '
        f'fill="{AMBER if i >= segs - 4 else CYAN}" style="animation-delay:{i * .08:.2f}s"/>' for i in range(segs))
    parts.append(f'<text x="22" y="{h - 54}" font-size="10" letter-spacing="2" fill="{MUTED}">SIGNAL</text>{meter}')
    css = "@keyframes seg{0%,100%{opacity:.15}40%,60%{opacity:1}}.seg{animation:seg 2.4s ease-in-out infinite}"
    return svg(w, h, "\n".join(parts), css)


# ---------- section headers ----------
def section(index, title, file_hint):
    w, h = 1280, 64
    tw = len(title) * CHAR * 22 + len(title) * 6
    x = 96 + tw + 24
    css = (".run{stroke-dasharray:80 2000;stroke-dashoffset:2080;animation:dash 4s linear infinite}")
    body = f'''<text x="10" y="40" font-size="14" letter-spacing="2" fill="{CYAN}">[{index:02d}]</text>
<text x="96" y="41" font-size="22" font-weight="700" letter-spacing="6" fill="{WHITE}">{esc(title.upper())}</text>
<line x1="{x:.0f}" y1="34" x2="{w - 190}" y2="34" stroke="{LINE}"/>
<line class="run" x1="{x:.0f}" y1="34" x2="{w - 190}" y2="34" stroke="{CYAN}" stroke-width="2"/>
<text x="{w - 10}" y="39" font-size="12" letter-spacing="1.5" fill="{MUTED}" text-anchor="end">// {esc(file_hint)}</text>'''
    return svg(w, h, body, css)


# ---------- project modules ----------
def project_card(i, p):
    w, h = 620, 236
    color = STATUS.get(p["status"], CYAN)
    lines = textwrap.wrap(p["desc"], 64)
    desc = "".join(f'<text x="24" y="{124 + k * 21}" font-size="13" fill="{TEXT}">{esc(l)}</text>' for k, l in enumerate(lines))
    chips, x = [], 24
    for t in p["tags"]:
        cw = len(t) * CHAR * 11 + 20
        chips.append(f'<rect x="{x:.1f}" y="{h - 48}" width="{cw:.1f}" height="24" fill="{CYAN}" fill-opacity=".06" stroke="{CYAN}" stroke-opacity=".4"/>'
                     f'<text x="{x + 10:.1f}" y="{h - 32}" font-size="11" fill="{CYAN}">{esc(t)}</text>')
        x += cw + 8
    chip_w = len(p["status"]) * (CHAR * 10.5 + 2) + 34
    ar = (f'<text class="ar" x="{w - 24}" y="94" font-size="20" fill="{MUTED}" text-anchor="start" direction="rtl">{esc(p["ar"])}</text>'
          if p["ar"] else "")
    link = (f'<text x="{w - 24}" y="{h - 32}" font-size="11" letter-spacing="1.5" fill="{MUTED}" text-anchor="end">'
            f'{esc(p["link"].split("//")[-1])} <tspan fill="{CYAN}">↗</tspan></text>') if p["link"] else ""
    body = f'''{panel(w, h)}
<text x="24" y="40" font-size="11" letter-spacing="2.5" fill="{MUTED}">MODULE <tspan fill="{CYAN}">{i + 1:02d}</tspan></text>
<g transform="translate({w - 24 - chip_w:.1f} 24)"><rect width="{chip_w:.1f}" height="22" fill="{color}" fill-opacity=".1" stroke="{color}" stroke-opacity=".6"/>
<circle class="pulse" cx="12" cy="11" r="3" fill="{color}"/><text x="22" y="15" font-size="10.5" letter-spacing="2" fill="{color}">{esc(p["status"])}</text></g>
<text class="em" x="24" y="95" font-size="26">{p.get("icon", "")}</text>
<text x="{66 if p.get("icon") else 24}" y="94" font-size="24" font-weight="700" fill="{WHITE}">{esc(p["name"])}</text>
{ar}
{desc}
{"".join(chips)}
{link}'''
    return svg(w, h, body)


# ---------- career timeline ----------
def timeline():
    w, h, y = 1280, 236, 128
    n = len(C.TIMELINE)
    gap = (w - 160) / (n - 1)
    css = (".trace{stroke-dasharray:1200;stroke-dashoffset:1200;animation:dash 2.4s cubic-bezier(.4,0,.2,1) .2s forwards}"
           "@keyframes ping{0%{r:6;opacity:.9}100%{r:22;opacity:0}}.ping{animation:ping 2s ease-out infinite}"
           "@media (prefers-reduced-motion:reduce){.trace{stroke-dashoffset:0}}")
    parts = [f'<line x1="80" y1="{y}" x2="{w - 80}" y2="{y}" stroke="{LINE}" stroke-width="2"/>',
             f'<line class="trace" x1="80" y1="{y}" x2="{w - 80}" y2="{y}" stroke="{CYAN}" stroke-width="2"/>']
    for i, (year, icon, title, detail) in enumerate(C.TIMELINE):
        x, last = 80 + i * gap, i == n - 1
        color = AMBER if last else CYAN
        ping = f'<circle class="ping" cx="{x:.0f}" cy="{y}" r="6" fill="none" stroke="{color}"/>' if last else ""
        parts.append(
            f'<g class="in" {delay(.3 + i * .35)}>{ping}'
            f'<circle cx="{x:.0f}" cy="{y}" r="6" fill="{VOID}" stroke="{color}" stroke-width="2"/>'
            f'<circle cx="{x:.0f}" cy="{y}" r="2.5" fill="{color}"/>'
            f'<text class="em" x="{x:.0f}" y="{y - 58}" font-size="24" text-anchor="middle">{icon}</text>'
            f'<text x="{x:.0f}" y="{y - 26}" font-size="20" font-weight="700" fill="{WHITE}" text-anchor="middle">{esc(year)}</text>'
            f'<text x="{x:.0f}" y="{y + 36}" font-size="12" letter-spacing="2" fill="{color}" text-anchor="middle">{esc(title.upper())}</text>'
            + "".join(f'<text x="{x:.0f}" y="{y + 58 + k * 17}" font-size="11.5" fill="{MUTED}" text-anchor="middle">{esc(l)}</text>'
                      for k, l in enumerate(textwrap.wrap(detail, 24)))
            + '</g>')
    return svg(w, h, "\n".join(parts), css)


# ---------- AI delivery flow ----------
def hexagon(cx, cy, r):
    import math
    return " ".join(f"{cx + r * math.cos(math.radians(a)):.1f},{cy + r * math.sin(math.radians(a)):.1f}" for a in range(30, 390, 60))


def ai_flow():
    w, h, y = 1280, 352, 160
    n = len(C.AI_FLOW)
    gap = (w - 220) / (n - 1)
    css = ("@keyframes pkt{from{transform:translateX(0);opacity:0}15%,85%{opacity:1}to{transform:translateX(var(--d));opacity:0}}"
           ".pkt{animation:pkt 1.6s linear infinite}"
           "@keyframes ping{0%{r:52;opacity:.8}100%{r:84;opacity:0}}.ping{animation:ping 2.2s ease-out infinite}"
           ".loop{stroke-dasharray:6 8;animation:flow 1.2s linear infinite}@keyframes flow{to{stroke-dashoffset:-28}}"
           )
    parts = [panel(w, h), header(w, f"AI.CORE  //  integrated since {C.AI_SINCE}", "ONLINE")]
    xs = [110 + i * gap for i in range(n)]
    for i in range(n - 1):
        x1, x2 = xs[i] + 50, xs[i + 1] - 50
        parts.append(f'<line x1="{x1:.0f}" y1="{y}" x2="{x2:.0f}" y2="{y}" stroke="{LINE}" stroke-width="2"/>'
                     + "".join(f'<circle class="pkt" cx="{x1:.0f}" cy="{y}" r="3" fill="{CYAN}" style="--d:{x2 - x1:.0f}px;animation-delay:{i * .25 + k * .8:.2f}s"/>'
                               for k in range(2)))
    # feedback loop: production signals flow back into the next idea
    parts.append(f'<path class="loop" d="M{xs[-1]:.0f} {y + 86}C{xs[-1]:.0f} {y + 150} {xs[0]:.0f} {y + 150} {xs[0]:.0f} {y + 86}" '
                 f'fill="none" stroke="{AMBER}" stroke-opacity=".55" stroke-width="1.5"/>'
                 f'<text x="{w / 2}" y="{y + 160}" font-size="10.5" letter-spacing="3" fill="{AMBER}" text-anchor="middle">◂ LEARN · MEASURE · ITERATE ◂</text>')
    for i, (icon, step, detail) in enumerate(C.AI_FLOW):
        x, hub = xs[i], i == C.AI_HUB
        color = AMBER if hub else CYAN
        ping = f'<circle class="ping" cx="{x:.0f}" cy="{y}" r="52" fill="none" stroke="{AMBER}"/>' if hub else ""
        parts.append(
            f'<g class="in" {delay(.3 + i * .18)}>{ping}'
            f'<polygon points="{hexagon(x, y, 46)}" fill="{color}" fill-opacity="{.14 if hub else .05}" stroke="{color}" stroke-opacity=".8" stroke-width="1.5"/>'
            f'<text class="em" x="{x:.0f}" y="{y + 11}" font-size="30" text-anchor="middle">{icon}</text>'
            f'<text x="{x:.0f}" y="{y - 62}" font-size="12" letter-spacing="2.5" font-weight="700" fill="{color}" text-anchor="middle">{i + 1:02d} {esc(step.upper())}</text>'
            f'<text x="{x:.0f}" y="{y + 72}" font-size="11.5" fill="{TEXT}" text-anchor="middle">{esc(detail)}</text></g>')
    return svg(w, h, "\n".join(parts), css)


# ---------- headline metrics ----------
def metrics():
    w, h = 1280, 132
    n = len(C.METRICS)
    cw = (w - 40) / n
    parts = [panel(w, h)]
    for i, (value, label) in enumerate(C.METRICS):
        x = 20 + i * cw + cw / 2
        sep = f'<line x1="{20 + i * cw:.0f}" y1="30" x2="{20 + i * cw:.0f}" y2="{h - 30}" stroke="{LINE}"/>' if i else ""
        parts.append(f'{sep}<g class="in" {delay(.2 + i * .15)}>'
                     f'<text x="{x:.0f}" y="66" font-size="30" font-weight="800" fill="{AMBER if i == 0 else WHITE}" text-anchor="middle">{esc(value)}</text>'
                     f'<text x="{x:.0f}" y="96" font-size="11" letter-spacing="2" fill="{CYAN}" text-anchor="middle">{esc(label.upper())}</text></g>')
    return svg(w, h, "\n".join(parts))


# ---------- services ----------
def services():
    cols, cw, ch, g = 3, 412, 176, 22
    rows = -(-len(C.SERVICES) // cols)
    w, h = cols * cw + (cols - 1) * g, rows * ch + (rows - 1) * g
    parts = []
    for i, (icon, title, pitch) in enumerate(C.SERVICES):
        x, y = (i % cols) * (cw + g), (i // cols) * (ch + g)
        c = 14
        shape = f"M{x + c} {y + .5}H{x + cw - .5}V{y + ch - c}L{x + cw - c} {y + ch - .5}H{x + .5}V{y + c}Z"
        lines = "".join(f'<text x="{x + 24}" y="{y + 112 + k * 19}" font-size="12.5" fill="{TEXT}">{esc(l)}</text>'
                        for k, l in enumerate(textwrap.wrap(pitch, 50)))
        parts.append(
            f'<g class="in" {delay(.15 + i * .12)}><path d="{shape}" fill="{PANEL}" stroke="{LINE}"/>'
            f'<path d="M{x + .5} {y + c + 16}V{y + c}L{x + c} {y + .5}H{x + c + 16}" fill="none" stroke="{CYAN}" stroke-width="1.5"/>'
            f'<text class="em" x="{x + 24}" y="{y + 58}" font-size="30">{icon}</text>'
            f'<text x="{x + cw - 24}" y="{y + 36}" font-size="11" letter-spacing="2" fill="{MUTED}" text-anchor="end">SVC.{i + 1:02d}</text>'
            f'<text x="{x + 24}" y="{y + 86}" font-size="17" font-weight="700" fill="{WHITE}">{esc(title)}</text>{lines}</g>')
    return svg(w, h, "\n".join(parts))


# ---------- toolbox ----------
def arsenal():
    w, lx, x0, fs = 1280, 24, 150, 11.5
    parts, y = [], 70
    for gi, (group, items) in enumerate(C.ARSENAL.items()):
        x, row = x0, [f'<text x="{lx}" y="{y + 16}" font-size="11" letter-spacing="2.5" fill="{CYAN}">{esc(group.upper())}</text>']
        for t in items:
            cw = len(t) * CHAR * fs + 22
            if x + cw > w - 24:
                x, y = x0, y + 34
            row.append(f'<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="24" fill="{CYAN}" fill-opacity=".05" stroke="{LINE}"/>'
                       f'<text x="{x + 11:.1f}" y="{y + 16}" font-size="{fs}" fill="{TEXT}">{esc(t)}</text>')
            x += cw + 8
        parts.append(f'<g class="in" {delay(.2 + gi * .1)}>{"".join(row)}</g>')
        y += 44
    h = y + 20
    return svg(w, h, panel(w, h) + header(w, "TOOLBOX  //  in daily use", f"{sum(map(len, C.ARSENAL.values()))} TOOLS") + "\n".join(parts))


# ---------- call to action ----------
def cta():
    w, h = 1280, 150
    css = ("@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}.nudge{animation:nudge 1.4s ease-in-out infinite}")
    site = C.PORTFOLIO.split("//")[-1]
    body = f"""{panel(w, h)}
<defs><linearGradient id="ctag" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".16"/><stop offset="1" stop-color="{AMBER}" stop-opacity=".1"/></linearGradient></defs>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="url(#ctag)"/>
<text x="48" y="64" font-size="12" letter-spacing="3" fill="{AMBER}">◢ OPEN FOR PROJECTS</text>
<text x="48" y="100" font-size="24" font-weight="700" fill="{WHITE}">{esc(C.CTA)}</text>
<g class="nudge"><rect x="{w - 330}" y="52" width="282" height="52" fill="{CYAN}"/>
<text x="{w - 189}" y="84" font-size="16" font-weight="800" letter-spacing="1.5" fill="{VOID}" text-anchor="middle">{esc(site.upper())} →</text></g>"""
    return svg(w, h, body, css)


# ---------- studio: animated emblem + morning desk scene ----------
def studio():
    w, h = 1280, 420
    ex, ey, er = 170, 240, 78
    hexpts = " ".join(f"{ex + er * math.cos(math.radians(30 + 60 * k)):.1f},{ey + er * math.sin(math.radians(30 + 60 * k)):.1f}" for k in range(6))
    css = f"""
.spin{{transform-box:view-box;transform-origin:{ex}px {ey}px;animation:spin 22s linear infinite}}
.spin.rev{{animation-duration:9s;animation-direction:reverse}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.draw{{stroke-dasharray:{6 * er};stroke-dashoffset:{6 * er};animation:dash 1.8s .2s cubic-bezier(.6,0,.2,1) forwards}}
@keyframes jit{{0%,90%,100%{{transform:none}}92%{{transform:translate(-4px,1px)}}94%{{transform:translate(4px,-1px)}}96%{{transform:translate(-2px,0)}}}}
.jit{{animation:jit 4s steps(1) infinite}}.jit.b{{animation-delay:.05s}}
.type{{clip-path:inset(0 100% 0 0);animation:reveal 2.4s steps(26) 1.6s forwards}}
@keyframes rise{{from{{transform:translateY(70px)}}to{{transform:none}}}}
.sun{{animation:rise 4s cubic-bezier(.2,.7,.2,1) forwards}}
@keyframes fly{{from{{transform:translateX(-40px)}}to{{transform:translateX(260px)}}}}
.fly{{animation:fly 11s linear infinite}}
@keyframes steam{{0%{{opacity:0;transform:translateY(8px)}}35%{{opacity:.7}}100%{{opacity:0;transform:translateY(-18px)}}}}
.steam{{opacity:0;animation:steam 3s ease-out infinite}}
@keyframes code{{0%{{transform:scaleX(0)}}12%,82%{{transform:scaleX(1);opacity:1}}100%{{transform:scaleX(1);opacity:0}}}}
.code{{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:code 9s ease-out infinite}}
@keyframes bob{{0%,100%{{transform:none}}50%{{transform:translateY(2px)}}}}
.bob{{animation:bob 2.6s ease-in-out infinite}}
@keyframes glow{{0%,100%{{opacity:.55}}50%{{opacity:.85}}}}
.glow{{animation:glow 3s ease-in-out infinite}}"""

    letters = "".join(
        f'<text class="in" {delay(.5 + i * .08)} x="{300 + i * 28.8:.1f}" y="222" font-size="48" font-weight="800" fill="url(#sheen)">{c}</text>'
        for i, c in enumerate(C.BRAND.upper()))
    emblem = f"""
<circle class="spin" cx="{ex}" cy="{ey}" r="{er + 22}" fill="none" stroke="{CYAN_DIM}" stroke-width="1.5" stroke-dasharray="3 9"/>
<g class="spin rev"><circle cx="{ex}" cy="{ey}" r="{er + 34}" fill="none" stroke="{LINE}"/><circle cx="{ex + er + 34}" cy="{ey}" r="4" fill="{AMBER}"/></g>
<polygon points="{hexpts}" fill="{CYAN}" fill-opacity=".05"/>
<polygon class="draw" points="{hexpts}" fill="none" stroke="url(#zcg)" stroke-width="3"/>
<g font-size="58" font-weight="800" text-anchor="middle">
<text class="jit" x="{ex}" y="{ey + 20}" fill="{CYAN}" opacity=".55">ZC</text>
<text class="jit b" x="{ex}" y="{ey + 20}" fill="{AMBER}" opacity=".45">ZC</text>
<text class="in" {delay(.9)} x="{ex}" y="{ey + 20}" fill="url(#zcg)">ZC</text></g>"""

    titles = f"""{letters}
<text class="in" {delay(1.3)} x="302" y="258" font-size="13" letter-spacing="4.5" fill="{AMBER}">GOOD MORNING, WORLD</text>
<text class="type" x="302" y="296" font-size="15" fill="{TEXT}"><tspan class="em">☕</tspan> coffee → compile → ship</text>
<text class="in" {delay(3.6)} x="302" y="330" font-size="11" letter-spacing="2" fill="{MUTED}">SINCE {C.SINCE} · AI-NATIVE SINCE {C.AI_SINCE}</text>"""

    # window with sunrise
    wx, wy, ww, wh = 660, 78, 200, 176
    birds = "".join(f'<path class="fly" style="animation-delay:{d}s" d="M{wx + bx} {wy + by}q5 -5 9 0q4 -5 9 0" fill="none" stroke="{VOID}" stroke-width="1.6"/>'
                    for bx, by, d in [(0, 70, 0), (14, 58, -4), (-10, 88, -7)])
    skyline = (f"M{wx} {wy + wh}V{wy + 150}h22v-24h18v30h14v-44h26v38h16v-18h20v28h22v-36h18v22h20v-12h24V{wy + wh}Z")
    window = f"""
<polygon points="{wx},{wy} {wx + ww},{wy} 1000,420 760,420" fill="{AMBER}" opacity=".04"/>
<clipPath id="win"><rect x="{wx}" y="{wy}" width="{ww}" height="{wh}"/></clipPath>
<g clip-path="url(#win)"><rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="url(#sky)"/>
<g class="sun"><circle cx="{wx + 110}" cy="{wy + 132}" r="60" fill="url(#sunglow)"/><circle cx="{wx + 110}" cy="{wy + 132}" r="24" fill="#ffd98a"/></g>
{birds}<path d="{skyline}" fill="#0a1222"/></g>
<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="none" stroke="#22324d" stroke-width="6"/>
<path d="M{wx + ww / 2} {wy}V{wy + wh}M{wx} {wy + wh / 2}H{wx + ww}" stroke="#22324d" stroke-width="4"/>
<rect x="{wx - 10}" y="{wy + wh}" width="{ww + 20}" height="8" fill="#22324d"/>"""

    # monitor with code being written
    mx, my, mw, mh = 890, 104, 270, 160
    rows = [(0, 120, CYAN), (1, 170, TEXT), (2, 140, TEXT), (1, 90, AMBER), (2, 190, TEXT), (2, 110, LIME), (1, 150, TEXT), (0, 60, CYAN)]
    code = "".join(f'<rect class="code" style="animation-delay:{.4 + i * .55:.2f}s" x="{mx + 18 + ind * 16}" y="{my + 20 + i * 16}" width="{cw}" height="6" rx="3" fill="{c}" opacity=".85"/>'
                   for i, (ind, cw, c) in enumerate(rows))
    monitor = f"""
<rect x="{mx - 7}" y="{my - 7}" width="{mw + 14}" height="{mh + 14}" rx="6" fill="#111a2b" stroke="#22324d"/>
<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" fill="#06101d"/>
<rect class="glow" x="{mx}" y="{my}" width="{mw}" height="{mh}" fill="url(#screen)"/>{code}
<rect class="blink" x="{mx + 210}" y="{my + 132}" width="8" height="10" fill="{CYAN}"/>
<rect x="{mx + mw / 2 - 10}" y="{my + mh + 7}" width="20" height="34" fill="#1a2639"/>
<ellipse cx="{mx + mw / 2}" cy="{my + mh + 42}" rx="44" ry="5" fill="#1a2639"/>"""

    # desk, plant, mug with steam
    dy = 310
    mugx = 1178
    steam = "".join(f'<path class="steam" style="animation-delay:{d}s" d="M{mugx + dx} 272c-6 -8 6 -12 0 -20c-6 -8 6 -12 0 -20" fill="none" stroke="{WHITE}" stroke-width="2.4" stroke-linecap="round"/>'
                    for dx, d in [(9, 0), (19, 1), (29, 2)])
    desk = f"""
<rect x="630" y="{dy}" width="610" height="10" fill="#1d2b42"/><rect x="640" y="{dy + 10}" width="590" height="100" fill="#0c1424"/>
<path d="M676 {dy - 22}c-14 -10 -22 -30 -12 -44c6 14 12 26 12 44zM680 {dy - 22}c6 -18 22 -30 34 -30c-6 16 -18 26 -34 30zM678 {dy - 22}c0 -20 4 -38 14 -50c4 18 0 36 -14 50z" fill="{LIME}" opacity=".6"/>
<path d="M664 {dy - 24}h30l-4 24h-22z" fill="#2a3b55"/>
{steam}
<path d="M{mugx + 38} 284c14 0 14 18 0 18" fill="none" stroke="#e8eef5" stroke-width="4"/>
<path d="M{mugx} 276h38v26a8 8 0 0 1 -8 8h-22a8 8 0 0 1 -8 -8z" fill="#e8eef5"/>
<rect x="{mugx}" y="276" width="38" height="4" fill="#5a3b26"/>
<text x="{mugx + 19}" y="298" font-size="10" font-weight="800" fill="{CYAN_DIM}" text-anchor="middle">ZC</text>"""

    # developer, seen from behind, lit by the screen
    px, py = 1010, 262
    dev = f"""
<g class="bob">
<rect x="{px - 11}" y="{py + 22}" width="22" height="22" fill="#1b2a40"/>
<path d="M{px - 92} 420C{px - 92} {py + 64} {px - 64} {py + 38} {px} {py + 36}C{px + 64} {py + 38} {px + 92} {py + 64} {px + 92} 420Z" fill="#14233a"/>
<path d="M{px - 92} 420C{px - 92} {py + 64} {px - 64} {py + 38} {px} {py + 36}C{px + 64} {py + 38} {px + 92} {py + 64} {px + 92} 420" fill="none" stroke="{CYAN}" stroke-opacity=".35" stroke-width="2"/>
<path d="M{px - 34} {py + 46}q34 26 68 0" fill="none" stroke="#0e1a2c" stroke-width="5"/>
<circle cx="{px}" cy="{py}" r="31" fill="#0b111d"/>
<path d="M{px - 31} {py}a31 31 0 0 1 62 0" fill="none" stroke="{CYAN}" stroke-opacity=".45" stroke-width="2"/>
<path d="M{px - 36} {py + 4}a36 38 0 0 1 72 0" fill="none" stroke="#2a3b55" stroke-width="6"/>
<rect x="{px - 42}" y="{py - 4}" width="12" height="22" rx="5" fill="#2a3b55"/><rect x="{px + 30}" y="{py - 4}" width="12" height="22" rx="5" fill="#2a3b55"/>
<circle class="pulse" cx="{px + 36}" cy="{py + 7}" r="2" fill="{LIME}"/></g>"""

    clock = f"""<text x="1235" y="80" font-size="11" letter-spacing="2" fill="{MUTED}" text-anchor="end">LOCAL</text>
<text x="1235" y="100" font-size="18" font-weight="700" fill="{AMBER}" text-anchor="end">06<tspan class="blink">:</tspan>00</text>"""

    defs = f"""<defs>
<linearGradient id="zcg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{AMBER}"/></linearGradient>
<linearGradient id="sheen" gradientUnits="userSpaceOnUse" x1="200" y1="0" x2="420" y2="0">
<stop offset="0" stop-color="{WHITE}"/><stop offset=".45" stop-color="{WHITE}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset=".55" stop-color="{WHITE}"/><stop offset="1" stop-color="{WHITE}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-260 0;460 0" dur="4.5s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#132a57"/><stop offset=".55" stop-color="#c8577a"/><stop offset="1" stop-color="#ffb547"/></linearGradient>
<radialGradient id="sunglow"><stop offset="0" stop-color="#ffd98a" stop-opacity=".8"/><stop offset="1" stop-color="#ffd98a" stop-opacity="0"/></radialGradient>
<linearGradient id="screen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".12"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".02"/></linearGradient>
<radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{CYAN}" stop-opacity=".18"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
</defs>"""
    body = (panel(w, h) + header(w, "STUDIO  //  morning shift", "COFFEE ONLINE") + defs
            + f'<g clip-path="url(#pc)"><ellipse class="glow" cx="1025" cy="220" rx="220" ry="170" fill="url(#halo)"/>'
            + window + monitor + desk + dev + "</g>" + clock + emblem + titles)
    return svg(w, h, body, css)


# ---------- footer ----------
def footer():
    w, h = 1280, 110
    rnd = random.Random(3)
    pts = " ".join(f"{x},{55 + rnd.uniform(-1, 1) * (22 if 520 < x < 760 else 6):.1f}" for x in range(0, w + 1, 8))
    css = ".wave{stroke-dasharray:1800;stroke-dashoffset:1800;animation:dash 3.5s ease-out infinite alternate}"
    body = f'''<polyline points="{pts}" fill="none" stroke="{LINE}"/>
<polyline class="wave" points="{pts}" fill="none" stroke="{CYAN}" stroke-opacity=".8"/>
<rect x="{w/2 - 220}" y="40" width="440" height="30" fill="{VOID}"/>
<text x="{w/2}" y="60" font-size="12" letter-spacing="5" fill="{TEXT}" text-anchor="middle"><tspan fill="{CYAN}">◢ </tspan>END OF TRANSMISSION<tspan fill="{CYAN}"> ◣</tspan></text>
<text x="{w/2}" y="100" font-size="10.5" letter-spacing="3" fill="{MUTED}" text-anchor="middle">{esc(C.BRAND.upper())}  ·  CODING SINCE {C.SINCE}</text>'''
    return svg(w, h, body, css)


# ---------- README ----------
def badge(label, logo, url):
    return (f'<a href="{url}"><img src="https://img.shields.io/badge/{quote(label)}-080d18?style=for-the-badge'
            f'&logo={logo}&logoColor=38e8ff&labelColor=04060c" alt="{esc(label)}"/></a>')


SECTIONS = [("About", "about.md"), ("Services", "hire.md"), ("Track record", "timeline.log"), ("AI core", "ai-flow.yml"),
            ("Modules", "projects/"), ("Stack", "stack.yml"), ("Telemetry", "activity.log")]


def section_img(title):
    i = [t for t, _ in SECTIONS].index(title) + 1
    return f'<img src="./{GEN}/section-{i:02d}.svg" width="100%" alt="{esc(title)}"/>'


def gen_img(name, alt, link=""):
    img = f'<img src="./{GEN}/{name}" width="100%" alt="{esc(alt)}"/>'
    return f'<a href="{link}">{img}</a>' if link else img


def readme():
    u = C.GITHUB_USER
    badges = []
    if C.PORTFOLIO: badges.append(badge("Hire ZoolCoder", "googlechrome", C.PORTFOLIO))
    badges.append(badge("GitHub", "github", f"https://github.com/{u}"))

    cards = []
    for i, p in enumerate(C.PROJECTS):
        img = f'<img src="./{GEN}/project-{i + 1:02d}.svg" width="49%" alt="{esc(p["name"])}: {esc(p["desc"])}"/>'
        cards.append(f'<a href="{p["link"]}">{img}</a>' if p["link"] else img)
    grid = "\n".join(" ".join(cards[i:i + 2]) for i in range(0, len(cards), 2))

    skills = "\n".join(
        f'<tr><td><code>{esc(k.upper())}</code></td><td><img src="https://skillicons.dev/icons?i={v}&theme=dark" alt="{esc(k)}"/></td></tr>'
        for k, v in C.SKILLS.items())

    theme = "bg_color=080d18&title_color=38e8ff&text_color=cfe6f0&icon_color=38e8ff&hide_border=true"
    stats = f"https://github-readme-stats.vercel.app/api?username={u}&show_icons=true&{theme}"
    langs = f"https://github-readme-stats.vercel.app/api/top-langs/?username={u}&layout=compact&{theme}"
    streak = (f"https://streak-stats.demolab.com?user={u}&hide_border=true&background=080d18"
              "&ring=38e8ff&fire=ffb547&currStreakNum=ffffff&currStreakLabel=38e8ff&sideNums=ffffff"
              "&sideLabels=cfe6f0&dates=5d7689&stroke=16243a")
    snake = f"https://raw.githubusercontent.com/{u}/{u}/output"
    metrics_alt = " · ".join(f"{v} {l}" for v, l in C.METRICS)
    services_alt = " · ".join(t for _, t, _ in C.SERVICES)

    return f"""<div align="center">

{gen_img("hero.svg", f"{C.BRAND} by {C.NAME} ({C.NAME_AR}): {C.TAGLINE}")}

{" ".join(badges)}

<img src="https://komarev.com/ghpvc/?username={u}&color=38e8ff&style=flat-square&label=SIGNALS+RECEIVED" alt="Profile views"/>

{gen_img("metrics.svg", metrics_alt)}

{gen_img("studio.svg", "ZoolCoder studio: a developer at the desk at sunrise, code on the screen, coffee steaming")}

<img src="./{GEN}/portrait.svg" width="49.5%" alt="ASCII portrait"/>&nbsp;<img src="./{GEN}/spec.svg" width="49.5%" alt="{esc(C.BRAND)} profile"/>

</div>

{section_img("About")}

""" + "\n".join(f"- {a}" for a in C.ABOUT) + f"""

{section_img("Services")}

{gen_img("services.svg", f"What ZoolCoder builds: {services_alt}", C.PORTFOLIO)}

{section_img("Track record")}

{gen_img("timeline.svg", "Track record: " + " · ".join(f"{y} {t}" for y, _, t, _ in C.TIMELINE))}

{section_img("AI core")}

{gen_img("ai-flow.svg", f"AI in the delivery flow since {C.AI_SINCE}: " + " → ".join(s for _, s, _ in C.AI_FLOW))}

{section_img("Modules")}

<div align="center">

{grid}

</div>

{section_img("Stack")}

<div align="center">
<table>
{skills}
</table>
</div>

{gen_img("arsenal.svg", "Toolbox: " + "; ".join(f"{k}: {', '.join(v)}" for k, v in C.ARSENAL.items()))}

{section_img("Telemetry")}

<div align="center">
<img src="{stats}" height="165" alt="GitHub stats"/>
<img src="{langs}" height="165" alt="Top languages"/>

<img src="{streak}" alt="Contribution streak"/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{snake}/snake-dark.svg"/>
  <img src="{snake}/snake.svg" alt="Snake eating the contribution graph"/>
</picture>

{gen_img("cta.svg", f"{C.CTA} {C.PORTFOLIO}", C.PORTFOLIO)}

{gen_img("footer.svg", "End of transmission")}
</div>
"""


def main():
    files = [("hero.svg", hero()), ("metrics.svg", metrics()), ("studio.svg", studio()), ("portrait.svg", portrait()), ("spec.svg", spec_card()),
             ("services.svg", services()), ("timeline.svg", timeline()), ("ai-flow.svg", ai_flow()),
             ("arsenal.svg", arsenal()), ("cta.svg", cta()), ("footer.svg", footer())]
    files += [(f"section-{i + 1:02d}.svg", section(i + 1, t, hint)) for i, (t, hint) in enumerate(SECTIONS)]
    files += [(f"project-{i + 1:02d}.svg", project_card(i, p)) for i, p in enumerate(C.PROJECTS)]
    os.makedirs(os.path.join(ROOT, GEN), exist_ok=True)
    for name, content in files:
        with open(os.path.join(ROOT, GEN, name), "w", encoding="utf-8") as f:
            f.write(content)
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme())
    print(f"wrote README.md and {len(files)} SVGs in {GEN}/")
    if not os.path.exists(os.path.join(ROOT, C.PHOTO)):
        print(f"note: {C.PHOTO} not found, portrait uses the ZC monogram for now")


if __name__ == "__main__":
    main()
