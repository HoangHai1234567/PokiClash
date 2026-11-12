# -*- coding: utf-8 -*-
"""Kiếm sĩ rừng mặc giáp (mã làm việc kiem_si; con gốc của rig: monster_3620, game tham khảo). Tướng thứ 8 đảo Mộc.

Người dùng 2026-11-12: "concept như con gốc tôi gửi, biến tấu đi; con gốc là bọ hung, bạn có thể đổi sang con khỉ hoặc không nhất thiết
phải là 1 sinh vật, chỉ cần nó mặc giáp, có 1 chút thiên hướng rừng rậm, samurai".
Rig gốc: 65 slot, gần như MỌI mảnh cứng bám một xương (trừ hai chùm lông sau lưng, bốn tua vai, áo trùm cổ, ngực: 2–3 xương) → hình bóng
từng mảnh của mình tự do, chỉ giữ chỗ đặt, cỡ, thứ tự chồng. Con gốc nhìn sang PHẢI, gù lưng thế iai: tay R (bên trái hình, vai có tấm
giáp to) là tay GẦN vẽ trước thân, cầm kiếm dài còn trong vỏ; tay L (bên phải hình) là tay XA. Không lật.

    kiem_si.py part_goc         ảnh từng part của con gốc cắt theo lưới → <SXS>/scan/monster_3620/parts/ (chỉ để xem, nội bộ)
    kiem_si.py luoi_xem         khối từng part ở dáng idle giây 0, kẻ lưới toạ độ khung concept → inbox/kiem_si_1/mau/_luoi.png
    kiem_si.py bo_cuc [hướng]   sơ đồ bố cục phẳng 1536 × 1024 (khi_non | khi_mu | giap_rong) → inbox/kiem_si_1/mau/bo_cuc_<hướng>.png
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
sys.path.insert(0, HERE)
from quai.soi import _tris  # noqa: E402
import to_manh  # noqa: E402

CODE = "kiem_si"
MON = "monster_3620"
K = int(os.environ.get("KS_DANG", "1"))
BASE = os.path.join(HERE, "inbox", f"{CODE}_{K}")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
W, H = 1536, 1024
SC = 0.86                                        # đơn vị rig con gốc → pixel khung concept
INK = (43, 33, 24)
ATT = "att_idle0.json"                           # dáng thủ của idle_01 giây 0
S2 = 2


def sxs():
    for p in [os.environ.get("SXS"), r"D:\Ripper\SwordxStaff", r"D:\RefAnimation\SwordxStaff", r"E:\Ripper\SwordxStaff"]:
        if p and os.path.isdir(p):
            return p
    raise SystemExit("không thấy thư mục SwordxStaff (đặt biến môi trường SXS)")


def rig_goc():
    return os.path.join(sxs(), "web", "assets", "Monster", MON)


def scan():
    return os.path.join(sxs(), "scan", MON)


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


_C = {}


def nap():
    if not _C:
        atlas, imgs = to_manh.nap(rig_goc(), MON)
        D = json.load(open(os.path.join(scan(), ATT), encoding="utf-8"))
        atts = sorted([a for a in D["atts"] if a.get("region") in imgs and a["cur"] and a["slot"] != "shadow"], key=lambda a: a["order"])
        _C.update(atlas=atlas, imgs=imgs, atts=atts, bones=D["bones"])
    return _C["atlas"], _C["imgs"], _C["atts"]


def luoi(a):
    atlas, imgs, _ = nap()
    im = imgs[a["region"]]
    if "uv" in a:
        return np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(a["tris"]).reshape(-1, 3)
    r = atlas[a["region"]]                       # region (kiếm): 4 góc BL, UL, UR, BR của vùng đã cắt
    ox, oy, ow, oh = r.get("offsets", [0, 0, im.width, im.height])
    w, h = (r["bounds"][3], r["bounds"][2]) if r["rotate"] in (90, 270) else (r["bounds"][2], r["bounds"][3])
    return (np.array([[ox, oh - oy], [ox, oh - oy - h], [ox + w, oh - oy - h], [ox + w, oh - oy]], float),
            np.array([[0, 1, 2], [2, 3, 0]]))


def part_goc(a):
    """ảnh một part của con gốc cắt đúng theo lưới của nó."""
    _, imgs, _ = nap()
    im = imgs[a["region"]].convert("RGBA")
    uv, tr = luoi(a)
    m = Image.new("L", (im.width * 4, im.height * 4), 0)
    d = ImageDraw.Draw(m)
    for t in tr:
        d.polygon([tuple(uv[i] * 4) for i in t], fill=255, outline=255)
    A = np.asarray(im).copy()
    A[..., 3] = (A[..., 3].astype(np.float32) * np.asarray(m.resize(im.size, Image.LANCZOS)) / 255.0).astype(np.uint8)
    return Image.fromarray(A, "RGBA")


def khung_T():
    """rig → pixel khung concept: cả con (kể cả vỏ kiếm chìa ra sau) nằm giữa khung, chân cách đáy ~60 px."""
    _, _, atts = nap()
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, x1 = P[:, 0].min(), P[:, 0].max()
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = H - 60 + P[:, 1].min() * SC
    return lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1)


def bong_khung(a, T, tron=5.0):
    """hình bóng KÍN của một part đặt đúng chỗ trên khung concept (phóng S2), làm trơn: chỉ còn khối."""
    src = part_goc(a)
    al = np.asarray(src)[..., 3]
    one = Image.fromarray(np.dstack([np.full(al.shape + (3,), 255, np.uint8), np.where(al > 90, 255, 0).astype(np.uint8)]), "RGBA")
    uv, tr = luoi(a)
    V = T(np.array(a["xy"], float).reshape(-1, 2)) * S2
    lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
    _tris(lay, one.convert("RGBa"), V, uv, tr)
    m = (np.asarray(lay)[..., 3] > 110).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(4))
    m = cv2.GaussianBlur(m * 255, (0, 0), tron) > 127
    return m


def vien(m, r):
    return m & ~cv2.erode(m.astype(np.uint8), el(r)).astype(bool)


MAU_XEM = [(230, 90, 90), (240, 190, 70), (110, 200, 110), (90, 180, 240), (190, 130, 240), (240, 150, 200), (150, 150, 150), (240, 150, 70),
           (120, 220, 200), (200, 200, 90)]


def luoi_xem():
    """mọi part ở dáng idle giây 0, mỗi part một màu + tên, kẻ lưới toạ độ khung concept (tờ nội bộ để đọc chỗ đặt)."""
    _, _, atts = nap()
    T = khung_T()
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop = {}
    for i, a in enumerate(atts):
        m = bong_khung(a, T, 2.5)
        if not m.any():
            continue
        can[m] = MAU_XEM[i % len(MAU_XEM)]
        can[vien(m, 4)] = INK
        ys, xs = np.nonzero(m)
        hop[a["slot"]] = [int(xs.min() / S2), int(ys.min() / S2), int(xs.max() / S2), int(ys.max() / S2)]
    im = Image.fromarray(can).resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)
    for x in range(0, W, 50):
        d.line([(x, 0), (x, H)], fill=(0, 120, 255) if x % 100 == 0 else (190, 215, 255), width=1)
        if x % 100 == 0:
            d.text((x + 2, 2), str(x), fill=(0, 60, 200), font=f)
    for y in range(0, H, 50):
        d.line([(0, y), (W, y)], fill=(0, 120, 255) if y % 100 == 0 else (190, 215, 255), width=1)
        if y % 100 == 0:
            d.text((2, y + 2), str(y), fill=(0, 60, 200), font=f)
    for k, v in hop.items():
        d.text(((v[0] + v[2]) / 2 - 20, (v[1] + v[3]) / 2 - 6), k.replace("P_", "").replace("W_", ""), fill=(0, 0, 0), font=f)
    os.makedirs(MAU, exist_ok=True)
    im.save(os.path.join(MAU, "_luoi.png"))
    json.dump(hop, open(os.path.join(MAU, "_hop.json"), "w"), indent=0)
    for k, v in hop.items():
        print(f"  {k:18s} x {v[0]}-{v[2]}  y {v[1]}-{v[3]}")
    print("gốc rig (0,0) →", T((0, 0)), " (0,500) →", T((0, 500)))
    print(os.path.join(MAU, "_luoi.png"))


def xuat_part_goc():
    ra = os.path.join(scan(), "parts")
    os.makedirs(ra, exist_ok=True)
    _, _, atts = nap()
    for a in atts:
        part_goc(a).save(os.path.join(ra, f"{a['order']:02d}_{a['slot']}.png"))
    print(ra, len(atts), "part")


def main(a):
    if a[:1] == ["part_goc"]:
        xuat_part_goc()
    elif a[:1] == ["luoi_xem"]:
        luoi_xem()
    elif a[:1] == ["bo_cuc"]:
        import kiem_si_bo_cuc as B
        for k in (a[1:] or list(B.HUONG)):
            B.bo_cuc(k)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
