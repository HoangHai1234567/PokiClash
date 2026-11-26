# Trường đua kiểu sân vận động (người dùng dặn 2026-11-26): cắt 4 tờ gen (goc/*_1k.png) và đóng thành 2 tấm atlas cho Unity.
#   py -3 -I ArtGen/Casino/truong_dua/dong_goi.py
# Ra: Assets/03 Art/Baked/Casino/race_san.png   (dải khán đài, tường trước, hàng rào dây, vân đất; lát cuộn ngang)
#     Assets/03 Art/Baked/Casino/race_hinh.png  (khán giả trước / sau lưng, bảng treo, cột, cờ, vạch đích, biển tròn, trang trí theo hệ)
#     Assets/03 Art/Baked/Casino/race_buc.png   (bục nhận thưởng 3 bậc, cúp, nơ vàng / bạc / đồng)
#     Assets/03 Art/Baked/Casino/race_quay.png  (quầy cược: tấm quầy, 4 chip, dải băng, vé lượt)
#     Assets/03 Art/Baked/Casino/race_art.json  (khung từng hình: x, y từ góc trên trái; pivot theo Unity, gốc dưới trái)
#     xem/*.jpg (tờ soi trên nền xanh)
# Thư mục Baked: ArtImporter không ép về một sprite; menu "Trường đua: dựng scene" tự đặt cách nhập (nhiều sprite, ASTC 6x6).
# Số đo khung (px tờ 1536 x 1024) lấy bằng soi cột / hàng alpha của đúng 4 tờ này; gen lại tờ nào thì đo lại tờ đó.
import json
import os
import random

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(HERE, "goc")
OUT = os.path.join(ROOT, "Assets", "03 Art", "Baked", "Casino")
XEM = os.path.join(HERE, "xem")
ELEMS = ["kim", "moc", "thuy", "hoa", "tho"]  # cột tờ trang trí, trái sang phải


def load(name):
    return Image.open(os.path.join(SRC, name + "_1k.png")).convert("RGBA")


def trim(im, pad=0):
    box = im.split()[3].point(lambda v: 255 if v > 24 else 0).getbbox()
    if not box:
        return im
    x0, y0, x1, y1 = box
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def scale(im, k):
    return im if k == 1 else im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)


def foot_x(im):
    # tâm ngang của phần thân sát đáy (không tính cờ, biển giơ lệch sang bên)
    a = np.array(im.split()[3]) > 40
    h = a.shape[0]
    cols = np.nonzero(a[int(h * 0.8):].sum(0))[0]
    return float((cols.min() + cols.max()) / 2 / im.width) if len(cols) else 0.5


# ---------- tấm sân: dải lát ngang ----------

def strips():
    im = load("khan_dai")
    items = []
    # A khán đài: bỏ hàng cờ trên mái (cờ thành hình rời, game cho phất); cắt ở tâm hai cột biên để lát lật gương thành một cột liền
    a = im.crop((52, 150, 1485, 581))
    # chân cán cờ ăn vào mép mái ~20 px: vá bằng cách lật gương mái hai bên vào giữa cán (cán đứng ngay ranh hai sọc; cột cờ đo ở tờ gốc)
    arr = np.array(a)
    for x0, x1 in [(51, 73), (344, 367), (615, 638), (887, 910), (1161, 1184), (1434, 1456)]:
        l0, l1 = max(0, x0 - 52 - 3), x1 - 52 + 4
        w = l1 - l0
        if l0 == 0:
            for i in range(w):
                arr[:26, l1 - 1 - i] = arr[:26, l1 + i]
            continue
        for i in range((w + 1) // 2):
            arr[:26, l0 + i] = arr[:26, l0 - 1 - i]
            arr[:26, l1 - 1 - i] = arr[:26, l1 + i]
    a = Image.fromarray(arr)
    items.append(("khan_dai", a, "mirror"))
    items.append(("tuong", im.crop((8, 659, 1529, 832)), "mirror"))
    items.append(("rao", im.crop((40, 894, 1496, 1007)), "mirror"))  # tâm cọc đầu tới tâm cọc cuối
    flag = trim(im.crop((336, 44, 450, 151)))
    return items, flag


def ground(w=500, h=480, seed=7):
    # vân đất: giấy gần trắng + nét chì sáp chéo (như ảnh mốc bản đồ), lặp liền theo chiều ngang; game nhân màu chặng lên
    rnd = random.Random(seed)
    s = 2
    W, H = w * s, h * s
    im = Image.new("L", (W, H), 236)
    d = ImageDraw.Draw(im, "L")
    import math
    for _ in range(2100):
        x, y = rnd.uniform(0, W), rnd.uniform(-20, H + 20)
        L = rnd.uniform(40, 120) * s / 2
        th = math.radians(rnd.uniform(32, 42))
        dx, dy = L * math.cos(th), -L * math.sin(th)
        light = rnd.random() < 0.6
        v = rnd.randint(246, 255) if light else rnd.randint(208, 224)
        wd = rnd.choice([2, 3, 3, 4]) * s // 2
        for ox in (-W, 0, W):
            d.line((x + ox, y, x + ox + dx, y + dy), fill=v, width=max(1, wd))
    for _ in range(34):  # sỏi, vệt đất thưa
        x, y = rnd.uniform(0, W), rnd.uniform(10, H - 10)
        r = rnd.uniform(3, 6) * s / 2
        for ox in (-W, 0, W):
            d.ellipse((x + ox - r * 1.4, y - r, x + ox + r * 1.4, y + r), fill=rnd.randint(178, 198))
    im = im.resize((w, h), Image.LANCZOS)
    return Image.merge("RGBA", (im, im, im, Image.new("L", (w, h), 255)))


def pack_field():
    items, flag = strips()
    items.append(("dat", ground(), "wrap"))
    E = 2  # nới mép 2 px chống rỉ màu khi lát
    W = 2048
    y = E
    atlas = Image.new("RGBA", (W, 1024), (0, 0, 0, 0))
    out = []
    for name, im, mode in items:
        x = E
        y0 = y
        if name == "dat":  # ô vân đất nằm ở khoảng trống bên phải các dải
            x, y = 1536, E
        atlas.paste(im, (x, y))
        w, h = im.size
        for k in range(1, E + 1):
            if mode == "mirror":
                atlas.paste(im.crop((0, 0, 1, h)), (x - k, y))
                atlas.paste(im.crop((w - 1, 0, w, h)), (x + w - 1 + k, y))
            else:
                atlas.paste(im.crop((w - k, 0, w - k + 1, h)), (x - k, y))
                atlas.paste(im.crop((k - 1, 0, k, h)), (x + w - 1 + k, y))
        if mode == "wrap":
            for k in range(1, E + 1):
                atlas.paste(atlas.crop((x - E, y, x + w + E, y + 1)), (x - E, y - k))
                atlas.paste(atlas.crop((x - E, y + h - 1, x + w + E, y + h)), (x - E, y + h - 1 + k))
        out.append({"name": name, "x": x, "y": y, "w": w, "h": h, "pivot": [0.5, 0.5]})
        y = y0 if name == "dat" else y + h + 2 * E + 4
    assert y <= 1024, y
    return atlas, out, flag


# ---------- tấm hình rời ----------

def fans():
    im = load("khan_gia")
    a = np.array(im)[:, :, 3] > 40
    lab, n = ndimage.label(a)
    objs = ndimage.find_objects(lab)
    area = ndimage.sum(a, lab, range(1, n + 1))
    big = [i for i in range(n) if area[i] > 6000]
    cen = ndimage.center_of_mass(a, lab, range(1, n + 1))
    owner = {i: i for i in big}
    for i in range(n):
        if i in owner or area[i] < 12:
            continue
        owner[i] = min(big, key=lambda b: (cen[b][0] - cen[i][0]) ** 2 + (cen[b][1] - cen[i][1]) ** 2)
    res = []
    for b in big:
        ids = [i + 1 for i, o in owner.items() if o == b]
        m = np.isin(lab, ids)
        ys, xs = np.nonzero(m)
        x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
        arr = np.array(im)[y0:y1, x0:x1].copy()
        arr[~m[y0:y1, x0:x1]] = 0
        res.append((cen[b][0], cen[b][1], Image.fromarray(arr)))
    front = sorted([r for r in res if r[0] < 480], key=lambda r: r[1])
    back = sorted([r for r in res if r[0] >= 480], key=lambda r: r[1])
    assert len(front) == 8 and len(back) == 6, (len(front), len(back))
    out = [("fan_f%d" % i, scale(r[2], 0.85)) for i, r in enumerate(front)]
    out += [("fan_b%d" % i, scale(r[2], 0.9)) for i, r in enumerate(back)]
    return out


def props():
    im = load("do_dung")
    out = [
        ("bang", scale(trim(im.crop((340, 0, 1195, 360))), 0.9)),
        ("cot", scale(trim(im.crop((130, 370, 240, 1010))), 0.6)),
        ("vach_dich", scale(trim(im.crop((375, 370, 520, 1010))), 0.7)),
        ("co_caro", scale(trim(im.crop((630, 440, 1005, 710))), 0.6)),
        ("co_trang", scale(trim(im.crop((630, 725, 1005, 940))), 0.6)),
        ("bien_tron", scale(trim(im.crop((1100, 370, 1450, 1010))), 0.5)),
    ]
    return out


def decals():
    im = load("trang_tri_he")
    a = np.array(im)[:, :, 3] > 40
    rows = [(110, 323), (418, 607), (700, 922)]
    out = []
    for r, (y0, y1) in enumerate(rows):
        band = a[y0 - 20:y1 + 21].sum(0) > 0
        cols, s = [], None
        for x, v in enumerate(band):
            if v and s is None:
                s = x
            if not v and s is not None:
                if cols and s - cols[-1][1] < 30:
                    cols[-1] = (cols[-1][0], x)
                else:
                    cols.append((s, x))
                s = None
        assert len(cols) == 5, (r, cols)
        for c, (x0, x1) in enumerate(cols):
            out.append(("decal_%s_%d" % (ELEMS[c], r), scale(trim(im.crop((x0 - 4, y0 - 24, x1 + 4, y1 + 24))), 0.7)))
    return out


def podium():
    # bục nhận thưởng (người dùng dặn 2026-11-26: "đua xong có 1 màn nhận thưởng đứng podium"): bục 3 bậc, cúp, 3 nơ hạng
    im = load("buc")
    k = 0.78
    box = (125, 38, 1409, 576)
    out = [
        ("buc", scale(im.crop(box), k)),
        ("cup", scale(trim(im.crop((40, 620, 445, 1005))), 0.6)),
        ("no_vang", scale(trim(im.crop((485, 620, 780, 1005))), 0.55)),
        ("no_bac", scale(trim(im.crop((822, 620, 1118, 1005))), 0.55)),
        ("no_dong", scale(trim(im.crop((1172, 620, 1472, 1005))), 0.55)),
    ]
    # chỗ đứng (giữa mặt bậc) và tâm biển tròn của hạng 1, 2, 3 trong hình "buc" (px, gốc trên trái); đo ở tờ gốc
    stand = [[639, 82], [235, 176], [1049, 236]]
    plaque = [[639, 266], [235, 310], [1049, 346]]
    return out, [[round(x * k), round(y * k)] for x, y in stand], [[round(x * k), round(y * k)] for x, y in plaque]


def booth():
    # quầy cược ở đáy màn (người dùng dặn 2026-11-26: "thiết kế lại phần dưới chỗ các button nhìn xấu quá"): tấm quầy gỗ có mái sọc
    # (cắt 9 mảnh: mái và khung giữ nguyên, ván giữa giãn), 4 đồng chip mức cược, dải băng, vé lượt (còn / đã dùng)
    im = load("quay_cuoc")
    out = [("quay", im.crop((63, 23, 1473, 575)))]
    for i, (x0, x1) in enumerate([(164, 375), (491, 704), (822, 1037), (1155, 1368)]):
        out.append(("chip_%d" % i, scale(trim(im.crop((x0 - 8, 595, x1 + 8, 828))), 0.72)))
    out.append(("bang_ron", trim(im.crop((80, 850, 826, 996)))))
    out.append(("ve", scale(trim(im.crop((882, 850, 1136, 996))), 0.6)))
    out.append(("ve_het", scale(trim(im.crop((1186, 850, 1441, 996))), 0.6)))
    # viền cắt 9 mảnh (px hình: trái, dưới, phải, trên)
    border = {"quay": [62, 56, 62, 168], "bang_ron": [96, 0, 96, 0]}
    return out, border


def pack_sprites(sprites, W=2048, H=1024, pad=4):
    atlas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    order = sorted(sprites, key=lambda s: -s[1].height)
    x = y = pad
    row_h = 0
    out = {}
    for name, im in order:
        if x + im.width + pad > W:
            x = pad
            y += row_h + pad
            row_h = 0
        assert y + im.height + pad <= H, ("tràn atlas", name, y, im.height)
        atlas.paste(im, (x, y))
        out[name] = {"name": name, "x": x, "y": y, "w": im.width, "h": im.height, "pivot": [round(foot_x(im), 3) if name.startswith("fan_") else 0.5, 0.0]}
        x += im.width + pad
        row_h = max(row_h, im.height)
    return atlas, [out[n] for n, _ in sprites]


def board_inner(im):
    # ô bảng đen trong khung bảng treo (để đặt chữ): vùng xanh rêu sẫm
    a = np.array(im).astype(int)
    m = (a[:, :, 3] > 200) & (a[:, :, 1] > a[:, :, 0] + 8) & (a[:, :, 1] < 110)
    ys, xs = np.nonzero(m)
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def preview(atlas, name):
    bg = Image.new("RGB", atlas.size, (120, 170, 130))
    bg.paste(atlas, mask=atlas.split()[3])
    bg.thumbnail((1600, 1600))
    bg.save(os.path.join(XEM, name + ".jpg"), quality=86)


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(XEM, exist_ok=True)
    field, field_items, flag = pack_field()
    sprites = fans() + props() + [("co_mai", scale(flag, 0.85))] + decals()
    art, art_items = pack_sprites(sprites)
    pod_sprites, pod_stand, pod_plaque = podium()
    pod, pod_items = pack_sprites(pod_sprites, W=1024, H=672)
    booth_sprites, booth_border = booth()
    quay, quay_items = pack_sprites(booth_sprites, W=2048, H=736)
    for it in quay_items:
        if it["name"] in booth_border:
            it["border"] = booth_border[it["name"]]
    board = dict(sprites)["bang"]
    meta = {
        "atlases": [
            {"png": "race_san.png", "w": field.width, "h": field.height, "items": field_items},
            {"png": "race_hinh.png", "w": art.width, "h": art.height, "items": art_items},
            {"png": "race_buc.png", "w": pod.width, "h": pod.height, "items": pod_items},
            {"png": "race_quay.png", "w": quay.width, "h": quay.height, "items": quay_items},
        ],
        "buc_cho": pod_stand,  # chỗ đứng hạng 1, 2, 3 trong hình "buc" (px, gốc trên trái)
        "buc_bien": pod_plaque,  # tâm biển tròn hạng 1, 2, 3
        "bang_trong": board_inner(board),  # x0, y0, x1, y1 trong hình "bang", gốc trên trái
    }
    field.save(os.path.join(OUT, "race_san.png"))
    art.save(os.path.join(OUT, "race_hinh.png"))
    pod.save(os.path.join(OUT, "race_buc.png"))
    quay.save(os.path.join(OUT, "race_quay.png"))
    preview(quay, "race_quay")
    preview(pod, "race_buc")
    with open(os.path.join(OUT, "race_art.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    preview(field, "race_san")
    preview(art, "race_hinh")
    for it in field_items + art_items + pod_items + quay_items:
        print(it["name"], it["w"], it["h"], it["pivot"])
    print("bang_trong", meta["bang_trong"], "bang", board.size)


if __name__ == "__main__":
    main()
