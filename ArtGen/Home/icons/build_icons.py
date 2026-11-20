# -*- coding: utf-8 -*-
"""Icon công trình màn Nhà (người dùng 2026-11-20: "gen thêm icon các building trong đó nữa").

    py -3 -I ArtGen/Home/icons/build_icons.py          dựng ảnh mẫu + file prompt (icons_A.txt, icons_B.txt) + HUONG_DAN.md
    py -3 -I ArtGen/Home/icons/build_icons.py cat      cắt tai_ve/icons_A.png, icons_B.png -> Assets/03 Art/Home/icons/icon_home_<mã>.png

Tờ A (4 x 4, 1:1): 15 công trình đã có hình trên đảo (ảnh mẫu = chính hình đó) + hàng rào gỗ.
Tờ B (4 x 3, 3:2): 12 đồ trang trí chưa có hình (đèn, chum, tượng boss...).
Sau khi cắt: Unity "PokiClash/Dựng lại danh mục ảnh" -> App.Art.Icon("home_<mã>").
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
ART = os.path.join(ROOT, "Assets", "03 Art", "Home")
OUT = os.path.join(ART, "icons")
REFS = os.path.join(HERE, "refs")
TAI = os.path.join(HERE, "tai_ve")
STYLE = os.path.normpath(os.path.join(HERE, "..", "..", "Islands", "refs", "world_style.png"))

A = [
    ("main", "the main house: cozy two-storey wooden cottage, red tiled roof, chimney, flower boxes, small flag"),
    ("field", "fenced vegetable field: dark soil with carrots, cabbages and a pumpkin, low wooden rails, little gate"),
    ("orchard", "apple orchard: small apple trees with red apples inside low wooden rails, a ladder, baskets of apples"),
    ("sawmill", "sawmill: small open timber shed with a slanted blue plank roof, a round saw blade, stacked logs"),
    ("pond", "fishing pond: round pond with a stone rim, blue water, lily pads, reeds, a tiny wooden jetty"),
    ("mine", "mine: grey rock hill with coloured crystals poking out, a timber-framed mine entrance with a minecart, a lantern post"),
    ("forge", "forge: stone forge with a chimney under a small timber roof, an anvil, bellows, orange coals drawn flat"),
    ("kitchen", "kitchen: small thatched-roof cottage with an open stone oven with a fire and a pot, a chimney, barrels"),
    ("storage", "storage barn: small red wooden barn with a big double door, crates and sacks in front"),
    ("well", "stone well with a little wooden roof, a crank and a bucket"),
    ("waterwheel", "water wheel mill: small timber mill house with a big wooden water wheel on its side"),
    ("hotspring", "hot spring: round stone pool with pale blue water and drawn steam curls, bamboo fence behind"),
    ("tree", "ball tree: small round tree whose fruits are white balls with one grey stripe"),
    ("bench", "wooden park bench"),
    ("swing", "rope swing hanging from a wooden A-frame"),
    ("fence_wood", "a short section of wooden picket fence (three or four pickets with two rails)"),
]
B = [
    ("flowerbed", "flower bed: a small wooden planter box full of pink, yellow and red flowers"),
    ("lantern", "paper lantern: a round red paper lantern hanging from a short wooden post"),
    ("shell_lamp", "shell lamp: a big pink-cream seashell on a small stand with a little warm light inside, drawn flat"),
    ("bamboo_fence", "bamboo fence: a short section of green bamboo poles tied with rope"),
    ("bronze_bell", "bronze bell: a bronze temple bell hanging under a small wooden frame"),
    ("stone_jar", "stone jar: a big round grey stone water jar with a wooden lid"),
    ("cup_fish", "fishing trophy: a golden trophy cup with a little blue fish on top"),
    ("statue_thuy", "WATER boss statue: a grey stone statue of a sea dragon with five long necks and heads rising from carved stone waves, on a square plinth with a small blue gem"),
    ("statue_hoa", "FIRE boss statue: a grey stone statue of a stocky volcano dinosaur with a little volcano crater on its back, on a square plinth with a small red-orange gem"),
    ("statue_kim", "METAL boss statue: a grey stone statue of a big robot king with a crown and wide square shoulders, on a square plinth with a small silver gem"),
    ("statue_moc", "WOOD boss statue: a grey stone statue of a long bamboo dragon with four wings and bamboo-shoot horns, coiled, on a square plinth with a small green gem"),
    ("statue_tho", "EARTH boss statue: a grey stone statue of a floating rock giant made of round boulders with one big eye in its chest, on a square plinth with a small golden gem"),
]

NO_SHADOW = ("NO SHADOWS: no drop shadow, no hard offset shadow, no cast shadow, no shadow under the object or on the ground or "
             "background. Shade only with colour-pencil hatching inside the shapes; the game adds shadows itself where needed.")
ICON = ("Each icon: ONE object only, seen from the same 3/4 isometric angle as the reference buildings, centred in its cell, "
        "filling about 80 % of the cell, chunky simple shape that reads clearly at 64 px, a small patch of its own grass or "
        "ground under it is fine, nothing crossing the cell. Drawn like image 1: thick wobbly dark-brown ink outline (#2B2118), "
        "flat coloured-pencil and wax-crayon colour (one flat colour per area, pencil hatching only as texture), cheerful and "
        "cozy. No glossy highlights, no glow, no gradients, no 3D render. No text, no numbers, no letters, no grid lines, no "
        "creatures, no people. Background: plain flat pure white everywhere around and between the icons.")


def font(n):
    for f in ("arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(f, n)
        except OSError:
            pass
    return ImageFont.load_default()


def grid(path, cols, rows, w, h):
    im = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(im)
    cw, ch = w / cols, h / rows
    f = font(int(min(cw, ch) * 0.3))
    for r in range(rows):
        for c in range(cols):
            x0, y0 = c * cw, r * ch
            d.rectangle((x0 + 6, y0 + 6, x0 + cw - 6, y0 + ch - 6), outline=(170, 170, 170), width=3)
            d.text((x0 + cw / 2, y0 + ch / 2), str(r * cols + c + 1), fill=(200, 200, 200), font=f, anchor="mm")
    im.save(path)


def collage(path, ids, cols, rows, cell):
    """các hình công trình đang có trên đảo, mỗi hình một ô có số (đúng thứ tự tờ icon); thiếu hình thì để trống"""
    im = Image.new("RGB", (cols * cell, rows * cell), "white")
    d = ImageDraw.Draw(im)
    f = font(28)
    for i, mid in enumerate(ids):
        c, r = i % cols, i // cols
        p = os.path.join(ART, f"home_b_{mid}.png")
        if os.path.exists(p):
            s = Image.open(p).convert("RGBA")
            s.thumbnail((cell - 30, cell - 40))
            im.paste(s, (c * cell + (cell - s.width) // 2, r * cell + 34 + (cell - 40 - s.height) // 2), s)
        d.text((c * cell + 10, r * cell + 6), str(i + 1), fill=(120, 120, 120), font=f)
        d.rectangle((c * cell, r * cell, (c + 1) * cell - 1, (r + 1) * cell - 1), outline=(220, 220, 220), width=2)
    im.save(path)


def build():
    os.makedirs(REFS, exist_ok=True)
    os.makedirs(TAI, exist_ok=True)
    ga, gb = os.path.join(REFS, "grid_4x4.png"), os.path.join(REFS, "grid_4x3.png")
    ca, cb = os.path.join(REFS, "buildings_A.png"), os.path.join(REFS, "buildings_style.png")
    grid(ga, 4, 4, 1024, 1024)
    grid(gb, 4, 3, 1536, 1024)
    collage(ca, [m for m, _ in A], 4, 4, 300)
    collage(cb, ["bench", "swing", "well", "tree"], 4, 1, 300)
    sa, sb = os.path.join(TAI, "icons_A.png"), os.path.join(TAI, "icons_B.png")
    la = "\n".join(f"{i + 1}. {t}" for i, (_, t) in enumerate(A))
    lb = "\n".join(f"{i + 1}. {t}" for i, (_, t) in enumerate(B))
    pa = f"""image 1 = {STYLE}: drawing style (hand-drawn ink + coloured pencil + crayon)
image 2 = {ca}: the buildings as they look on the game map, numbered in the same order as the icons (cell 16 is empty: design it)
image 3 = {ga}: numbered 4 x 4 grid, one icon per cell
SAVE: {sa} (if the name exists add _2, _3...; do not edit, move or delete any other file)
Magnific: gpt-2-6, 1k, quality high, 1:1

A 1024 x 1024 sheet of 16 game icons for the buildings of a cozy island base-building mobile game, laid out exactly on the
4 x 4 grid of image 3 (left to right, top to bottom), one icon per cell. Each icon must be the SAME DESIGN as the numbered
building in image 2 (same shapes, colours and details, simplified a little so it reads at small size), not a new design.
{ICON}
{NO_SHADOW}

ICONS in grid order:
{la}
"""
    pb = f"""image 1 = {STYLE}: drawing style (hand-drawn ink + coloured pencil + crayon)
image 2 = {cb}: four existing objects from the same game (style and angle to match)
image 3 = {gb}: numbered 4 x 3 grid, one icon per cell
SAVE: {sb} (if the name exists add _2, _3...; do not edit, move or delete any other file)
Magnific: gpt-2-6, 1k, quality high, 3:2

A 1536 x 1024 sheet of 12 game icons for the decorations of a cozy island base-building mobile game, laid out exactly on
the 4 x 3 grid of image 3 (left to right, top to bottom), one icon per cell. Same drawing style and same 3/4 isometric angle
as the objects in image 2.
{ICON}
{NO_SHADOW}

ICONS in grid order:
{lb}
"""
    open(os.path.join(HERE, "icons_A.txt"), "w", encoding="utf-8").write(pa)
    open(os.path.join(HERE, "icons_B.txt"), "w", encoding="utf-8").write(pb)
    hd = f"""# Icon công trình màn Nhà

Hai lượt, mỗi lượt một file prompt (GPT tự mở ảnh mẫu theo đường dẫn trong file, tự lưu ảnh):

| Lượt | File prompt | Lưu vào | Cỡ |
|---|---|---|---|
| 1 | `{os.path.join(HERE, 'icons_A.txt')}` | `{sa}` | 1024 x 1024, lưới 4 x 4 |
| 2 | `{os.path.join(HERE, 'icons_B.txt')}` | `{sb}` | 1536 x 1024, lưới 4 x 3 |

Ảnh mẫu:
- `world_style.png`: mốc nét vẽ (bút mực nâu sẫm, chì màu, sáp màu), cảnh đảo.
- `refs/buildings_A.png`: 15 công trình đang có trên đảo (ảnh trong `Assets/03 Art/Home/home_b_*.png`), mỗi ô một số, nền trắng, 1200 x 1200; ô 16 trống (hàng rào gỗ, GPT tự vẽ).
- `refs/buildings_style.png`: ghế, xích đu, giếng, cây bi (mẫu nét và góc cho đồ trang trí), 1200 x 300.
- `refs/grid_4x4.png`, `refs/grid_4x3.png`: lưới ô đánh số xám nhạt trên nền trắng.

Kiểm: mỗi ô đúng một món, đúng thứ tự, không chữ số, không bóng đổ, không món nào tràn sang ô bên.
Câu sửa nhanh: `Same icons, same order; each icon fully inside its own cell, simpler shapes, thicker outlines, no shadows.`

Cắt: `py -3 -I ArtGen/Home/icons/build_icons.py cat` rồi Unity "PokiClash/Dựng lại danh mục ảnh".
"""
    open(os.path.join(HERE, "HUONG_DAN.md"), "w", encoding="utf-8").write(hd)
    print("xong:", os.path.join(HERE, "icons_A.txt"), os.path.join(HERE, "icons_B.txt"))


def knock_white(im):
    """điểm gần trắng nối với mép -> trong suốt (như ArtImporter.KnockOutWhite)"""
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    seen = bytearray(w * h)
    st = [(x, y) for x in range(w) for y in (0, h - 1)] + [(x, y) for y in range(h) for x in (0, w - 1)]
    while st:
        x, y = st.pop()
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        r, g, b, a = px[x, y]
        if min(r, g, b) < 232:
            continue
        px[x, y] = (255, 255, 255, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                st.append((nx, ny))
    # mép mềm: điểm sáng sát vùng đã xoá mờ dần theo độ trắng
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            near = any(0 <= x + dx < w and 0 <= y + dy < h and px[x + dx, y + dy][3] == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if near:
                m = min(r, g, b)
                if m > 200:
                    px[x, y] = (r, g, b, int(255 * (255 - m) / 55))
    return im


HOLES = {"bamboo_fence"}  # ô trắng kín giữa các thân tre: cũng là nền


def knock_holes(im, min_px=30):
    """vùng gần trắng kín (không nối mép) rộng hơn min_px điểm -> trong suốt"""
    w, h = im.size
    px = im.load()
    seen = bytearray(w * h)
    for sy in range(h):
        for sx in range(w):
            if seen[sy * w + sx]:
                continue
            r, g, b, a = px[sx, sy]
            if a < 200 or min(r, g, b) < 236:
                continue
            reg, st = [], [(sx, sy)]
            seen[sy * w + sx] = 1
            while st:
                x, y = st.pop()
                reg.append((x, y))
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                        q = px[nx, ny]
                        if q[3] >= 200 and min(q[:3]) >= 236:
                            seen[ny * w + nx] = 1
                            st.append((nx, ny))
            if len(reg) >= min_px:
                for x, y in reg:
                    px[x, y] = (255, 255, 255, 0)
    return im


def cat():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    # tờ B vẽ cả đường viền ô xám (GPT chép lưới mẫu): cắt chừa mép ô `inset` điểm rồi mới tách nền trắng từng ô
    for name, items, cols, rows, inset in (("icons_A", A, 4, 4, 0), ("icons_B", B, 4, 3, 16)):
        p = os.path.join(TAI, name + ".png")
        if not os.path.exists(p):
            print("chưa có", p)
            continue
        src = Image.open(p)
        has_a = src.mode == "RGBA" and src.getchannel("A").getextrema()[0] < 250
        src = src.convert("RGBA")
        cw, ch = src.width // cols, src.height // rows
        for i, (mid, _) in enumerate(items):
            c, r = i % cols, i // cols
            cell = src.crop((c * cw + inset, r * ch + inset, (c + 1) * cw - inset, (r + 1) * ch - inset))
            if not has_a:
                cell = knock_white(cell)
            if mid in HOLES:
                cell = knock_holes(cell)
            bb = cell.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox()
            if not bb:
                print("ô trống", name, i + 1, mid)
                continue
            x0, y0, x1, y1 = bb
            cell = cell.crop((max(0, x0 - 4), max(0, y0 - 4), min(cell.width, x1 + 4), min(cell.height, y1 + 4)))
            cell.thumbnail((256, 256), Image.LANCZOS)
            cell.save(os.path.join(OUT, f"icon_home_{mid}.png"))
            n += 1
    print(f"cắt {n} icon -> {OUT}")


if __name__ == "__main__":
    cat() if sys.argv[1:] == ["cat"] else build()
