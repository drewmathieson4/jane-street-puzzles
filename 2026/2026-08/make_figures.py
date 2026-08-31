"""Renders the figures used by SOLUTION.md. Palette and geometry match walkthrough.html."""
import math
from PIL import Image, ImageDraw, ImageFont

SS   = 4                      # supersample factor
BG   = (248, 250, 248)
BLK  = (35, 42, 44)
STRK = (174, 185, 179)
FCOL = [(191, 64, 56), (37, 117, 109), (143, 102, 18), (76, 90, 153)]   # red teal gold blue
INK  = (22, 26, 24)
PAPER= (248, 250, 248)

FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def font(px): return ImageFont.truetype(FONT, px)

# ---------------------------------------------------------------- tiling
SQ3 = math.sqrt(3)
def f(a, b): return (a - b) % 3
def is_white(a, b): return f(a, b) != 0
def ctr(a, b, s): return (a * s + b * s / 2, -(b * s * SQ3 / 2))
def hexpts(a, b, s, shrink=0.955):
    cx, cy = ctr(a, b, s); r = s / SQ3 * shrink
    return [(cx + r * math.cos(math.radians(30 + 60 * k)),
             cy + r * math.sin(math.radians(30 + 60 * k))) for k in range(6)]

def tcls(a, b):
    bp = b % 2; s = (b - bp) // 2
    return ((a - 2 * s) % 6, bp)
def okey(a, b):
    p, q = tcls(a, b), tcls(-a, -b)
    return (min(p, q), max(p, q))
FAM = {okey(1, 0): 0, okey(1, -1): 1, okey(2, 0): 2, okey(0, 1): 3}
fam    = lambda a, b: FAM[okey(a, b)]
is_red = lambda a, b: okey(a, b) == okey(1, 0)

ANG = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
def wnbrs(a, b): return [(a + x, b + y) for x, y in ANG if is_white(a + x, b + y)]

# ---------------------------------------------------------------- ball
TV = {'A': (1, 1, 1), 'B': (1, -1, -1), 'C': (-1, 1, -1), 'D': (-1, -1, 1)}
cut = lambda P, Q: tuple(P[i] + (Q[i] - P[i]) / 3 for i in range(3))
TF  = [('A', 'B', 'C'), ('A', 'C', 'D'), ('A', 'D', 'B'), ('B', 'D', 'C')]
BALL = []
for X, Y, Z in TF:
    x, y, z = TV[X], TV[Y], TV[Z]
    BALL.append((True, [cut(x, y), cut(y, x), cut(y, z), cut(z, y), cut(z, x), cut(x, z)]))
for P in TV:
    BALL.append((False, [cut(TV[P], TV[Q]) for Q in TV if Q != P]))

def rot(p, ax, ay):
    x, y, z = p
    c, s = math.cos(ay), math.sin(ay); x, z = x * c + z * s, -x * s + z * c
    c, s = math.cos(ax), math.sin(ax); y, z = y * c - z * s, y * s + z * c
    return (x, y, z)

def draw_ball(size, ax, ay):
    W = size * SS
    im = Image.new("RGB", (W, W), BG); d = ImageDraw.Draw(im)
    K = W * 0.42
    for i, (is_hex, pts) in enumerate(BALL):
        P = [rot(p, ax, ay) for p in pts]
        c = [sum(q[k] for q in P) / len(P) for k in range(3)]
        u = [P[1][k] - P[0][k] for k in range(3)]
        v = [P[2][k] - P[0][k] for k in range(3)]
        n = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
        if sum(n[k] * c[k] for k in range(3)) < 0: n = [-t for t in n]
        nl = math.sqrt(sum(t * t for t in n)); nz = n[2] / nl
        if nz <= 0.02: continue
        base = FCOL[i] if is_hex else BLK
        t = 0.34 * (1 - nz)
        col = tuple(int(ch * (1 - t)) for ch in base)
        xy = [(W/2 + p[0]*K, W/2 - p[1]*K) for p in P]
        d.polygon(xy, fill=col, outline=STRK, width=max(1, int(2*SS)))
    return im.resize((size, size), Image.LANCZOS)

def ball_gif(path, size=360, frames=40):
    # a plain spin about Y looks straight down a hexagon twice a turn and reads flat,
    # so nod the tilt once per revolution (still seamless, sin is periodic over the turn)
    ims = []
    for i in range(frames):
        th = 2 * math.pi * i / frames
        ims.append(draw_ball(size, 2.62 + 0.30 * math.sin(th), 1.86 + th))
    ims = [im.convert("P", palette=Image.ADAPTIVE, colors=128) for im in ims]
    ims[0].save(path, save_all=True, append_images=ims[1:], duration=60, loop=0, optimize=True)
    return path

# ---------------------------------------------------------------- floors
def draw_floor(size, rad_tiles, loops=False, pad=1.0):
    W = size * SS
    s = W / (2.0 * (rad_tiles + pad))
    im = Image.new("RGB", (W, W), BG); d = ImageDraw.Draw(im)
    off = W / 2
    lim = int(rad_tiles) + 3
    tiles = []
    for a in range(-2*lim, 2*lim + 1):
        for b in range(-2*lim, 2*lim + 1):
            x, y = ctr(a, b, s)
            if math.hypot(x, y) <= rad_tiles * s: tiles.append((a, b))
    for a, b in tiles:
        col = BLK if not is_white(a, b) else FCOL[fam(a, b)]
        d.polygon([(x + off, y + off) for x, y in hexpts(a, b, s)],
                  fill=col, outline=STRK, width=max(1, int(0.8*SS)))
    if loops:
        for a, b in tiles:
            if is_white(a, b): continue
            ring = [(a + x, b + y) for x, y in ANG]
            if any(is_red(*q) for q in ring): continue
            if any(math.hypot(*ctr(*q, s)) > rad_tiles * s for q in ring): continue
            pts = [(ctr(*q, s)[0] + off, ctr(*q, s)[1] + off) for q in ring]
            d.line(pts + [pts[0]], fill=PAPER, width=max(2, int(5.0*SS)), joint="curve")
    return im.resize((size, size), Image.LANCZOS)

# ---------------------------------------------------------------- one ring, labelled
RING  = [(0, 1), (0, 2), (-1, 3), (-2, 3), (-2, 2), (-1, 1)]
EXITS = [(1, 0), (1, 2), (-1, 4), (-3, 4), (-3, 2), (-1, 0)]
DIST  = [1, 2, 3, 4, 3, 2]
BLACK_CENTRE = (-1, 2)

def draw_ring(size=820):
    W = size * SS; s = W / 5.75; H = int(s * 5.15)
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    bx, by = ctr(*BLACK_CENTRE, s)
    off = lambda p: (p[0] - bx + W/2, p[1] - by + H/2)
    def poly(t, **kw): d.polygon([off(p) for p in hexpts(*t, s)], **kw)
    for t in EXITS: poly(t, fill=FCOL[0], outline=STRK, width=max(1, int(1.2*SS)))
    poly(BLACK_CENTRE, fill=BLK, outline=STRK, width=max(1, int(1.2*SS)))
    for t in RING:  poly(t, fill=FCOL[fam(*t)], outline=STRK, width=max(1, int(1.2*SS)))
    for seat, ex in zip(RING, EXITS):                       # trapdoor arrows
        p0, p1 = off(ctr(*seat, s)), off(ctr(*ex, s))
        vx, vy = p1[0]-p0[0], p1[1]-p0[1]; L = math.hypot(vx, vy); ux, uy = vx/L, vy/L
        a0 = (p0[0]+ux*0.30*L, p0[1]+uy*0.30*L); a1 = (p0[0]+ux*0.66*L, p0[1]+uy*0.66*L)
        col = INK if ex == (1, 0) else PAPER
        d.line([a0, a1], fill=col, width=max(2, int(2.4*SS)))
        hw = 0.055*L
        d.polygon([(a1[0]+ux*hw*1.6, a1[1]+uy*hw*1.6),
                   (a1[0]-uy*hw, a1[1]+ux*hw), (a1[0]+uy*hw, a1[1]-ux*hw)], fill=col)
    fb, fs = font(int(0.52*s)), font(int(0.20*s))
    for t, n in zip(RING, DIST):
        d.text(off(ctr(*t, s)), str(n), font=fb, fill=PAPER, anchor="mm")
    d.text(off(ctr(1, 0, s)), "HOME", font=fs, fill=PAPER, anchor="mm")
    for t in EXITS[1:]:
        d.text(off(ctr(*t, s)), "not\nhome", font=fs, fill=PAPER, anchor="mm", align="center")
    return im.resize((size, int(H/SS)), Image.LANCZOS)

if __name__ == "__main__":
    print("ring seat families:", [fam(*t) for t in RING], "(0=red 1=teal 2=gold 3=blue)")
    print("exits all red:", all(is_red(*e) for e in EXITS))
    ball_gif("ball-colored.gif");            print("ball-colored.gif")
    draw_floor(900, 6.4, loops=True).save("locked-loops.png"); print("locked-loops.png")
    draw_ring().save("ring-labeled.png");                      print("ring-labeled.png")
