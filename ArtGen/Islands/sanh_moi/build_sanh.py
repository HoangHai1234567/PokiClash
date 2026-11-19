# Bản đồ sảnh mới (người dùng 2026-11-19: "cải thiện phần đảo chính ở home ... dễ để sau này thêm đảo mới", "liên kết thành map như
# kingdom rush", "địa hình cao thấp", "bỏ máy pinball", trang trại / tiềm năng ra UI; concept duyệt: concept_I_bo_pha_le_1.png).
# Mây che hết lúc mới chơi; chọn tướng khởi đầu thì mây đảo cùng hệ tan; xong trận hướng dẫn thì tan nốt (HubIslands, HubFog).
# Ra:
#   Assets/03 Art/Islands/world_map.png  : ảnh bản đồ phóng 2 lần (2048 x 3072) có làm nét
#   Assets/03 Art/Islands/hub_map.json   : cỡ hiện trên sảnh (view), từng đảo: điểm bấm (mốc lớn), mây che (u, v, w, lật)
#   khoá "world_map" trong Assets/03 Art/Islands/island_anim.json: khói núi lửa, xoáy nước, bọt thác, lấp lánh mặt trời, đèn đêm
#   sanh_moi/xem_suong.png               : tờ soi vùng, điểm bấm, mây
# Vành mây (người dùng 2026-11-19: "mây xung quanh đảo chính cứ tách riêng ra để khi đi thì nó tách luôn chứ không để liền mảng
# trắng"): vành mây vẽ liền trong tranh được thay bằng biển (open_sea), ảnh nới thêm biển TOP / BOT; mây vành là từng đám rời
# (khoá "ring" trong hub_map.json, CloudRing trong Unity): toả ra quanh tàu, chuyến tàu qua mây mang theo khi chụp màn.
# Toạ độ trong file này vẫn là toạ độ tranh gốc 1024 x 1536; ra JSON thì cộng TOP (khoá "offset").
# Thêm đảo về sau: vẽ nối thêm tranh (mở rộng về phía mây), thêm một mục vào REALMS (đa giác vùng + điểm bấm), chạy lại script
# rồi menu "PokiClash/Prefab/Sảnh bản đồ thế giới (mây, điểm bấm)". Chạy: py -3 -I build_sanh.py
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tach_dao  # noqa: E402
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ART = os.path.join(ROOT, "Assets", "03 Art", "Islands")
SRC = os.path.join(HERE, "concept_I_ben_tau.png")  # concept_I_bo_pha_le_1.png + bến tàu (ben_tau/ghep_ben.py)
VIEW_W = 1728  # bề ngang bản đồ trên sảnh (đơn vị khung 1080 x 1920): rộng hơn màn để kéo được 4 hướng
CLOUD = "land_thuy_may_2"
CLOUD_ASPECT = 348 / 652  # cao / ngang hình mây
TOP, BOT = 90, 170  # biển nới thêm phía trên / dưới tranh (px tranh gốc): bến tàu khỏi sát mép, mây vành có chỗ
SHIP = os.path.join(ROOT, "Assets", "03 Art", "Ship")

# mỗi đảo: hệ, điểm bấm (mốc lớn, toạ độ ảnh gốc 1024 x 1536), đa giác vùng mây che (ảnh gốc)
REALMS = [
    ("thuy", (510, 1150), [(330, 1010), (560, 990), (800, 1050), (800, 1300), (720, 1450), (400, 1455), (225, 1335), (220, 1180)]),
    ("hoa", (380, 285), [(95, 90), (560, 70), (610, 200), (520, 290), (480, 420), (330, 425), (225, 385), (135, 335), (85, 250)]),
    ("kim", (790, 320), [(515, 110), (985, 110), (1005, 250), (965, 435), (780, 462), (600, 452), (420, 442), (500, 330), (515, 255)]),
    ("moc", (245, 760), [(0, 320), (170, 330), (240, 390), (340, 442), (470, 442), (520, 520), (512, 900), (470, 985), (250, 1005),
                         (55, 1005), (0, 945)]),
    ("tho", (770, 690), [(500, 452), (700, 442), (965, 435), (1015, 520), (1005, 905), (870, 995), (700, 975), (560, 905), (500, 800)]),
]

# chừa mây che quanh bến tàu (ben_tau/): tàu cập bến lúc mới chơi (màn tải) phải thấy được; mây được chạm mép vùng
AVOID = [(700, 1305, 915, 1478), (560, -170, 720, 110)]  # bến dưới (đảo Thủy), bến trên (giữa đảo Hỏa và Kim)

# phần động (IslandAnim, toạ độ ảnh gốc, cỡ px ảnh gốc)
ANIM = [
    ("plume", (387, 98), 46, {"c": "#8f8580", "v": 1, "n": 8, "l": 4.4}),  # miệng núi lửa
    ("swirl", (700, 1098), 170, None),  # xoáy nước
    ("foam", (192, 972), 30, None), ("foam", (232, 980), 26, None), ("foam", (690, 1300), 30, None), ("foam", (498, 965), 24, None),
    ("ripple", (150, 1380), 30, None), ("ripple", (912, 1402), 30, None), ("ripple", (150, 1135), 28, None), ("ripple", (885, 1240), 28, None),
    ("sparkle", (790, 190), 30, None), ("sparkle", (772, 535), 30, None), ("sparkle", (505, 1110), 22, None),
    ("wave", (130, 1060), 70, None), ("wave", (900, 1110), 70, None), ("wave", (620, 1490), 70, None), ("wave", (120, 1470), 60, None),
    ("leaf", (150, 560), 24, None), ("leaf", (320, 520), 22, None),
]
LIGHTS = [("glow", (387, 150), 150), ("glow", (305, 1185), 60), ("glow", (790, 190), 110), ("glow", (772, 535), 120),
          ("glow", (505, 1110), 60)]


def inside(poly, x, y):
    c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def clouds_for(poly, seed):
    rng = np.random.default_rng(seed)
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    out = []
    step_x, step_y = 92, 58
    row = 0
    for y in range(int(min(ys)) - 20, int(max(ys)) + 40, step_y):
        off = (row % 2) * step_x / 2
        row += 1
        for x in range(int(min(xs)) - 30, int(max(xs)) + 40, step_x):
            jx, jy = x + off + rng.uniform(-18, 18), y + rng.uniform(-12, 12)
            if not inside(poly, jx, jy):
                continue
            w = rng.uniform(210, 290)
            h = w * CLOUD_ASPECT
            if any(x0 - w * 0.3 < jx < x1 + w * 0.3 and y0 - h * 0.3 < jy < y1 + h * 0.3 for x0, y0, x1, y1 in AVOID):
                continue
            out.append((jx, jy, w, int(rng.random() < 0.5)))
    out.sort(key=lambda c: c[1])
    return out


def ring_mask(src):
    """Vành mây vẽ liền: điểm kem ấm (và trắng ở dải trên cùng) nối từ mép tranh, khép kín, lấp lỗ."""
    a = np.asarray(src, dtype=np.int16)
    r, b = a[..., 0], a[..., 2]
    mn, mx = a.min(2), a.max(2)
    h, w = mn.shape
    cream = (mn > 195) & ((r - b) > 8) & (mx - mn < 70)
    top = np.zeros_like(cream)
    top[:70] = (mn[:70] > 205) & (mx[:70] - mn[:70] < 45)
    cand = cream | top
    lab, n = ndimage.label(cand)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    ring = np.isin(lab, list(edge))
    # cụm mây kem lớn ở dải mép (trên 170 px, hai bên 130 px) dù không chạm mép
    sizes = ndimage.sum(cand, lab, range(1, n + 1))
    objs = ndimage.find_objects(lab)
    for i, sl in enumerate(objs, 1):
        if sizes[i - 1] < 150:
            continue
        y0, x0 = sl[0].start, sl[1].start
        y1, x1 = sl[0].stop, sl[1].stop
        if y0 < 170 or x0 < 130 or x1 > w - 130 or y1 > h - 60:
            if cream[sl][lab[sl] == i].mean() > 0.6:
                ring |= lab == i
    ring = ndimage.binary_closing(ring, iterations=6)
    ring = ndimage.binary_fill_holes(ring)
    # nuốt nét mực viền mây và rìa nhạt sát vành (không lấn vào màu khác)
    for _ in range(3):
        grow = ndimage.binary_dilation(ring, iterations=2) & ~ring
        ink = (mn < 130) | ((mn > 175) & (mx - mn < 80))
        ring |= grow & ink
    ring[:4] = ring[-4:] = True
    ring[:, :4] = ring[:, -4:] = True
    return ring


def open_sea(src):
    """Thay vành mây bằng biển, nới TOP / BOT. Trả (ảnh nới, mặt nạ vùng biển mới theo toạ độ ảnh nới)."""
    W, H = src.size
    ring = ring_mask(src)
    H2 = H + TOP + BOT
    fill = np.ones((H2, W), bool)
    fill[TOP:TOP + H] = ring
    # biển: mặt biển lát của chuyến tàu thu về cỡ tranh, rải nét sóng trắng
    k = 1024 / 1728
    tile = Image.open(os.path.join(SHIP, "tau_bien.png")).convert("RGB")
    tile = tile.resize((round(tile.width * k), round(tile.height * k)), Image.LANCZOS)
    sea = Image.new("RGB", (W, H2))
    for x in range(0, W, tile.width):
        for y in range(0, H2, tile.height):
            sea.paste(tile, (x, y))
    waves = []
    for i in range(1, 5):
        f = os.path.join(SHIP, f"tau_song_{i}.png")
        if os.path.exists(f):
            wv = Image.open(f).convert("RGBA")
            waves.append(wv.resize((max(6, round(wv.width * k * 0.75)), max(4, round(wv.height * k * 0.75))), Image.LANCZOS))
    rng = np.random.default_rng(23)
    seaA = sea.convert("RGBA")
    for _ in range(int(fill.sum() / 5200)):
        ys, xs = np.nonzero(fill)
        j = rng.integers(len(xs))
        wv = waves[rng.integers(len(waves))]
        seaA.alpha_composite(wv, (int(xs[j]) - wv.width // 2, int(ys[j]) - wv.height // 2))
    sea = seaA.convert("RGB")
    out = sea.copy()
    keep = Image.fromarray(((~fill) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.6))
    big = Image.new("RGB", (W, H2))
    big.paste(src, (0, TOP))
    out = Image.composite(big, sea, keep)
    return out, fill


def ring_clouds(fill):
    """Mây vành rời: lưới so le phủ vùng biển mới (vành cũ + phần nới) và dải sát mép ảnh."""
    H2, W = fill.shape
    zone = ndimage.binary_dilation(fill, iterations=18)
    band = np.zeros_like(zone)
    band[:, :70] = band[:, -70:] = True
    band[:TOP + 40] = band[-(BOT + 40):] = True
    zone |= band
    rng = np.random.default_rng(57)
    out = []
    step_x, step_y = 92, 56
    row = 0
    for y in range(-10, H2 + 30, step_y):
        off = (row % 2) * step_x / 2
        row += 1
        for x in range(-30, W + 40, step_x):
            jx, jy = x + off + rng.uniform(-16, 16), y + rng.uniform(-10, 10)
            ix, iy = int(np.clip(jx, 0, W - 1)), int(np.clip(jy, 0, H2 - 1))
            if not zone[iy, ix]:
                continue
            out.append((jx, jy, rng.uniform(200, 270), int(rng.random() < 0.5)))
    out.sort(key=lambda c: c[1])
    return out


def main():
    global AVOID
    src0 = Image.open(SRC).convert("RGB")
    src, fill = open_sea(src0)
    src.save(os.path.join(HERE, "concept_I_mo_bien.png"))
    # bờ các đảo bị vành mây cũ che (mép trái / phải / trên) đã được GPT khép thành vách đá + bọt (bo_dao/sua_bo_dao.txt): dán đè vùng tranh
    fix = os.path.join(HERE, "bo_dao", "sua_bo_dao_1.png")
    fixsrc = src0
    if os.path.exists(fix):
        fixsrc = Image.open(fix).convert("RGB").resize((src0.width, src0.height), Image.LANCZOS)
        src.paste(fixsrc, (0, TOP))
    # toạ độ tranh gốc → ảnh nới
    sh = lambda p: (p[0], p[1] + TOP)
    realms_s = [(z, sh(at), [sh(q) for q in poly]) for z, at, poly in REALMS]
    anim_s = [(k_, sh(p), sz, ex) for k_, p, sz, ex in ANIM]
    lights_s = [(k_, sh(p), sz) for k_, p, sz in LIGHTS]
    AVOID = [(x0, y0 + TOP, x1, y1 + TOP) for x0, y0, x1, y1 in AVOID]
    W, H = src.size
    # tách từng đảo (người dùng: "tách từng đảo 1 ra rồi xếp chúng lại"), biển lát riêng, mây chỉ trên biển xa bờ
    land = tach_dao.land_mask(src)
    isl = tach_dao.cut_islands(src, land, realms_s)
    islands = []
    for zone, im, (x0, y0, x1, y1), glow, (gx0, gy0, gx1, gy1) in isl:
        name = "sanh_dao_" + zone
        im.save(os.path.join(ART, name + ".png"), optimize=True)
        entry = {"zone": zone, "sprite": name, "rect": [round(x0 / W, 5), round(y0 / H, 5), round(x1 / W, 5), round(y1 / H, 5)]}
        # quầng sáng quanh chi tiết chính của đảo (cây thần, mặt trời, miệng núi lửa, đền mặt trời, cổng rồng)
        lg, lb = tach_dao.landmark_glow(fixsrc, zone, TOP)
        if lg is not None:
            lg.save(os.path.join(ART, "sanh_sang_" + zone + ".png"), optimize=True)
            entry["glow"] = "sanh_sang_" + zone
            entry["glowRect"] = [round(lb[0] / W, 5), round(lb[1] / H, 5), round(lb[2] / W, 5), round(lb[3] / H, 5)]
        islands.append(entry)
        print("đảo", zone, im.size)
    tach_dao.sea_tile(SHIP).save(os.path.join(ART, "sanh_bien.png"), optimize=True)
    ring = tach_dao.ring_clouds(land, AVOID)
    view_h = round(VIEW_W * H / W)
    up = src.resize((W * 2, H * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.6, percent=70, threshold=2))
    up.save(os.path.join(ART, "world_map.png"))
    realms = []
    prev = src.copy().convert("RGBA")
    ov = Image.new("RGBA", prev.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for i, (zone, at, poly) in enumerate(realms_s):
        cl = clouds_for(poly, 31 + i)
        realms.append({"zone": zone, "at": [round(at[0] / W, 4), round(at[1] / H, 4)],
                       "clouds": [[round(x / W, 4), round(y / H, 4), round(w / W, 4), f] for x, y, w, f in cl]})
        d.polygon(poly, outline=(255, 0, 255, 255))
        for x, y, w, f in cl:
            h = w * CLOUD_ASPECT
            d.ellipse([x - w / 2, y - h / 2, x + w / 2, y + h / 2], fill=(255, 255, 255, 70), outline=(120, 120, 120, 160))
        d.ellipse([at[0] - 10, at[1] - 10, at[0] + 10, at[1] + 10], fill=(255, 0, 0, 255))
        print(zone, len(cl), "đám mây")
    for x0, y0, x1, y1 in AVOID:
        d.rectangle([x0, y0, x1, y1], outline=(0, 160, 255, 255), width=2)
    for x, y, w, f in ring:
        h = w * CLOUD_ASPECT
        d.ellipse([x - w / 2, y - h / 2, x + w / 2, y + h / 2], fill=(255, 250, 235, 150), outline=(90, 70, 50, 200))
    print("mây vành", len(ring), "đám")
    prev.alpha_composite(ov)
    prev.convert("RGB").save(os.path.join(HERE, "xem_suong.png"))
    data = {"art": "world_map", "img": [W, H], "view": [VIEW_W, view_h], "offset": [0, TOP], "cloud": CLOUD, "realms": realms,
            "islands": islands, "sea": "sanh_bien",
            "ring": [[round(x / W, 4), round(y / H, 4), round(w / W, 4), f] for x, y, w, f in ring]}
    json.dump(data, open(os.path.join(ART, "hub_map.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def P(x, y):
        return round(x / W, 4), round(y / H, 4)
    items = []
    for k, (x, y), s, ex in anim_s:
        u, v = P(x, y)
        it = {"k": k, "x": u, "y": v, "s": round(s / W, 4)}
        if ex:
            it.update(ex)
        items.append(it)
    lights = [{"k": k, "x": P(x, y)[0], "y": P(x, y)[1], "s": round(s / W, 4)} for k, (x, y), s in lights_s]
    anim_path = os.path.join(ART, "island_anim.json")
    raw = open(anim_path, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    anim = json.loads(raw.decode("utf-8"))
    anim["world_map"] = {"items": items, "rivers": [], "lights": lights}
    open(anim_path, "w", encoding="utf-8", newline=nl).write(json.dumps(anim, ensure_ascii=False, indent=1))
    print("đã ghi world_map.png", up.size, "hub_map.json view", VIEW_W, view_h, ", khoá world_map")


if __name__ == "__main__":
    main()
