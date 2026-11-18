# Ghép thử luật nối mép ô lát (giống HomeScene.RenderTiles) trên nền cỏ của ảnh đảo: ra ArtGen/Home/tiles/preview_tiles.png.
import os, sys
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
T = os.path.join(ROOT, "Assets", "03 Art", "Home", "tiles")
PRIO = ["water", "dirt", "sand", "stone", "grass"]
AROUND = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
CORNER_EDGES = [(0, 1, 4), (1, 2, 5), (2, 3, 6), (3, 0, 7)]  # góc k: hai mép kề, ô chéo (chỉ số trong AROUND)

grid = {}
for k in range(6):
    grid[(2 + k, 3)] = "dirt"
for (x, y) in [(3, 5), (4, 5), (5, 5), (3, 6), (4, 6), (5, 6), (4, 7)]:
    grid[(x, y)] = "water"
for (x, y) in [(6, 5), (7, 5), (6, 6), (7, 6), (6, 4)]:
    grid[(x, y)] = "sand"
for (x, y) in [(5, 1), (5, 2), (6, 2)]:
    grid[(x, y)] = "stone"

img_cache = {}


def im(n):
    if n not in img_cache:
        img_cache[n] = Image.open(os.path.join(T, n + ".png")).convert("RGBA")
    return img_cache[n]


Wd, Hd = 1400, 900
base = Image.open(os.path.join(ROOT, "Assets", "03 Art", "Home", "home_base.png")).convert("RGBA")
bg = base.crop((640, 400, 760, 470)).resize((Wd, Hd), Image.LANCZOS)
O = (700, 60)


def top_of(tx, ty):
    return (O[0] + (tx - ty) * 96, O[1] + (tx + ty) * 48)


def put(name, tx, ty):
    t = top_of(tx, ty)
    bg.alpha_composite(im(name), (int(t[0] - 112), int(t[1] - 16)))


def typ(x, y):
    return grid.get((x, y), "grass")


tiles = sorted(grid, key=lambda p: p[0] + p[1])
for (x, y) in tiles:
    put("fill_" + grid[(x, y)], x, y)
for (x, y) in tiles:
    t = grid[(x, y)]
    if t == "water":
        for e in (2, 3):
            dx, dy = AROUND[e]
            if typ(x + dx, y + dy) != "water":
                put(f"bank_{e}", x, y)
    for e in range(4):
        dx, dy = AROUND[e]
        n = typ(x + dx, y + dy)
        if n != t and PRIO.index(n) > PRIO.index(t):
            put(f"lip_{n}_{e}", x, y)
    for k, (e1, e2, dg) in enumerate(CORNER_EDGES):
        n1 = typ(x + AROUND[e1][0], y + AROUND[e1][1])
        n2 = typ(x + AROUND[e2][0], y + AROUND[e2][1])
        dd = typ(x + AROUND[dg][0], y + AROUND[dg][1])
        if n1 == t and n2 == t and dd != t and PRIO.index(dd) > PRIO.index(t):
            put(f"cor_{dd}_{k}", x, y)
bg.save(os.path.join(HERE, "preview_tiles.png"))
print("ok")
