# -*- coding: utf-8 -*-
"""Tinh linh tượng đá cổ giữ rừng (mã làm việc tuong_da; con gốc của rig: monster_3423, game tham khảo). Tướng thứ 3 đảo Mộc.

Người dùng 2026-11-12: "concept tinh linh tượng đá cổ bảo vệ rừng, bị quấn rêu xanh; gen lại các bộ phận khác đi chút, theo thiên hướng
rừng cây, đá rừng hơn; ở giữa có thể là 1 lõi pha lê xanh hoặc lõi gì đó thể hiện trái tim khu rừng".
Rig gốc: 39 mảnh, MỌI mảnh cứng bám một xương (trừ ba dây leo hai xương) → hình bóng từng mảnh của mình tự do, chỉ giữ chỗ đặt, cỡ, thứ
tự chồng. Con gốc nhìn sang PHẢI (tay R = tay gần, bên trái người xem, vẽ trước thân): không lật.

    tuong_da.py part_goc     ảnh từng part của con gốc cắt theo lưới → <SXS>/scan/monster_3423/parts/ (chỉ để xem, nội bộ)
    tuong_da.py bo_cuc [kiểu] sơ đồ bố cục phẳng 1536 × 1024 từng hướng thiết kế (pha_le | gac) → inbox/tuong_da_1/mau/bo_cuc_<kiểu>.png
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
sys.path.insert(0, HERE)
from quai.soi import _tris  # noqa: E402
import to_manh  # noqa: E402

CODE = "tuong_da"
MON = "monster_3423"
K = int(os.environ.get("TD_DANG", "2"))        # dạng đang làm: TD_DANG=1 | 2 (mặc định 2 = Gạc Đá; 1 = Mầm Đá)
BASE = os.path.join(HERE, "inbox", f"{CODE}_{K}")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
W, H = 1536, 1024
SC = 1.22                                        # đơn vị rig con gốc → pixel khung concept
INK = (43, 33, 24)
ATT = "att_goc.json"
# bảng màu ĐỀ XUẤT của Claude (người dùng dặn: tượng đá cổ, rêu xanh, lõi pha lê xanh), chờ duyệt concept
PAL = dict(da=(196, 190, 166),                   # đá tượng (đá vôi cũ ngả kem xám) #C4BEA6
           da_trong=(140, 136, 120),             # mặt trong / mặt khuất của mảnh đá tượng #8C8878
           tang=(110, 104, 92),                  # đá tảng rừng (cẳng tay, bàn tay, ngón, chóp dưới) #6E685C
           reu=(98, 156, 72),                    # rêu #629C48
           re=(128, 88, 54),                     # rễ cây quấn #805836
           day=(70, 128, 62),                    # dây leo, lá #46803E
           loi=(64, 206, 140),                   # pha lê lõi (trái tim rừng) #40CE8C
           loi_dam=(30, 150, 104))               # mặt cắt đậm của pha lê #1E9668


def sxs():
    for p in [os.environ.get("SXS"), r"D:\Ripper\SwordxStaff", r"D:\RefAnimation\SwordxStaff", r"E:\Ripper\SwordxStaff"]:
        if p and os.path.isdir(p):
            return p
    raise SystemExit("không thấy thư mục SwordxStaff (đặt biến môi trường SXS)")


def rig_goc():
    return os.path.join(sxs(), "web", "assets", "Monster", MON)


def scan():
    return os.path.join(sxs(), "scan", MON)


def loai(ten):
    """nhóm thiết kế của một part (tên hình của con gốc)."""
    if ten.startswith("P_shuijing"):
        return "loi"
    if ten.startswith(("P_tengwan", "P_yezi")):
        return "day"
    if ten in ("P_shoubiL02", "P_shoubiR02"):
        return "re"
    if ten in ("P_jianjiaL02", "P_jianjiaR02", "P_shenti03"):
        return "da_trong"
    if ten.startswith(("P_shoubi", "P_shou", "P_shitou", "P_qiu")):
        return "tang"
    return "da"                                  # P_tou, P_jianjia*01, P_shenti01/02, P_zhuangshi


REU = {"P_tou": 0.20, "P_jianjiaR01": 0.26, "P_jianjiaL01": 0.24, "P_shenti01": 0.16, "P_shoubiR01": 0.20, "P_shoubiL01": 0.18}


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


_C = {}


def nap():
    """(atlas, ảnh vùng đã gỡ xoay {tên: RGBA}, danh sách att dáng gốc theo thứ tự vẽ; chỉ hình đang bật)."""
    if not _C:
        atlas, imgs = to_manh.nap(rig_goc(), MON)
        D = json.load(open(os.path.join(scan(), ATT), encoding="utf-8"))
        atts = sorted([a for a in D["atts"] if a.get("region") in imgs and a["cur"]], key=lambda a: a["order"])
        _C.update(atlas=atlas, imgs=imgs, atts=atts, bones=D["bones"])
    return _C["atlas"], _C["imgs"], _C["atts"]


def luoi(a):
    _, imgs, _ = nap()
    im = imgs[a["region"]]
    return np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(a["tris"]).reshape(-1, 3)


def part_goc(a):
    """ảnh một part của con gốc cắt đúng theo lưới của nó (ảnh vùng atlas là chữ nhật nên dính mảnh bên cạnh)."""
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
    _, _, atts = nap()
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = (H + (y1 - y0) * SC) / 2 + y0 * SC
    return lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1)


S2 = 2


def bong_khung(a, T, tron=5.0):
    """hình bóng KÍN của một part đặt đúng chỗ dáng gốc trên khung concept (phóng S2), làm trơn mạnh: chỉ còn khối, không mang nét vẽ,
    góc cạnh riêng của con gốc."""
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


def mang_reu(m, ti, seed):
    """mảng rêu phủ từ mép TRÊN của một mảnh xuống: bề dày ti × chiều cao mảnh, mép dưới lượn sóng."""
    ys, xs = np.nonzero(m)
    if not len(ys):
        return np.zeros_like(m)
    hh = ys.max() - ys.min()
    rng = np.random.default_rng(seed)
    top = np.where(m.any(0), m.argmax(0), 10 ** 6)
    x = np.arange(m.shape[1])
    day = hh * ti * (1 + 0.45 * np.sin(x / 23.0 + rng.uniform(0, 6)) + 0.3 * np.sin(x / 9.0 + rng.uniform(0, 6)))
    Y = np.arange(m.shape[0])[:, None]
    return m & (Y < (top + day)[None, :])


def gac(can, goc, huong):
    """một nhánh gạc cây (hướng "gac"): thân nhánh nâu từ đầu mút mào đá vươn lên, hai chạc, ba lá. goc = (x, y) px khung concept."""
    g = np.array(goc, float) * S2
    s = huong
    k = 1.45

    def P(*ds):
        return [g + np.array(d, float) * (s * k, k) for d in ds]

    than = P((0, 0), (30, -62), (78, -112), (98, -176))
    chac = [P((30, -62), (-18, -110), (-26, -158)), P((78, -112), (132, -128), (168, -170))]
    for mau, them in [(INK, 12), (PAL["re"], 0)]:
        for ds, day in [(than, 40), (chac[0], 30), (chac[1], 30)]:
            cv2.polylines(can, [np.array(ds, np.int32)], False, mau, day + them, cv2.LINE_AA)
    for c, goc_la in [(than[-1], 80 - 14 * s), (chac[0][-1], 90 + 24 * s), (chac[1][-1], 90 - 40 * s)]:
        c2 = (int(c[0]), int(c[1]) - 30)
        cv2.ellipse(can, c2, (62, 30), goc_la, 0, 360, INK, -1, cv2.LINE_AA)
        cv2.ellipse(can, c2, (55, 23), goc_la, 0, 360, PAL["reu"], -1, cv2.LINE_AA)


def bo_cuc(kieu="pha_le", luu=True):
    """sơ đồ bố cục: khối từng mảnh đặt đúng chỗ dáng gốc, tô phẳng theo nhóm màu của THIẾT KẾ MÌNH (đá tượng, mặt trong, đá tảng, rêu,
    rễ, dây leo, lõi lục). kieu: "pha_le" (mào đá phủ rêu, lõi pha lê, mảnh pha lê nhỏ) | "gac" (hai nhánh gạc cây trên mào, lõi là
    hạt mầm to, mảnh nhỏ là lá)."""
    _, _, atts = nap()
    T = khung_T()
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop = {}
    if kieu == "gac":                                                # gạc mọc từ hai đầu mút mào đá, vẽ trước (nấp sau mào)
        gac(can, (640, 190), -1)
        gac(can, (1010, 190), 1)
    for i, a in enumerate(atts):
        ten = a["att"]
        nh = loai(ten)
        nho = nh in ("loi", "day") or ten.startswith("P_shouzhi")
        m = bong_khung(a, T, 2.2 if nho else 5.0)
        if not m.any():
            continue
        if kieu == "gac" and ten == "P_shuijing":                    # lõi là hạt mầm bầu dục thay viên pha lê thoi
            ys, xs = np.nonzero(m)
            m8 = np.zeros(m.shape, np.uint8)
            cv2.ellipse(m8, (int((xs.min() + xs.max()) / 2), int((ys.min() + ys.max()) / 2 + 24)),
                        (int((xs.max() - xs.min()) * 0.60), int((ys.max() - ys.min()) * 0.40)), 0, 0, 360, 1, -1)
            m = m8.astype(bool)
        can[m] = PAL[nh]
        if ten in REU:
            r = mang_reu(m, REU[ten], i)
            can[r] = PAL["reu"]
        if nh == "loi":
            ys, xs = np.nonzero(m)
            cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
            X = np.arange(m.shape[1])[None, :]
            if kieu == "gac":                                        # hạt mầm / lá: một gân giữa
                can[m & (np.abs(X - cx) < 3)] = PAL["loi_dam"]
            else:                                                    # pha lê: nửa phải mặt cắt đậm
                can[m & (X > cx)] = PAL["loi_dam"]
        can[vien(m, 4 if nho else 6)] = INK
        ys, xs = np.nonzero(m)
        hop[ten] = [int(xs.min() / S2), int(ys.min() / S2), int(xs.max() / S2), int(ys.max() / S2)]
    out = Image.fromarray(can).resize((W, H), Image.LANCZOS)
    if luu:
        os.makedirs(MAU, exist_ok=True)
        out.save(os.path.join(MAU, f"bo_cuc_{kieu}.png"))
        json.dump(hop, open(os.path.join(MAU, "bo_cuc_hop.json"), "w"), indent=0)
        print(os.path.join(MAU, f"bo_cuc_{kieu}.png"))
        for k, v in hop.items():
            print(f"  {k:14s} x {v[0]}-{v[2]}  y {v[1]}-{v[3]}")
    return out


def xuat_part_goc():
    ra = os.path.join(scan(), "parts")
    os.makedirs(ra, exist_ok=True)
    _, _, atts = nap()
    for a in atts:
        part_goc(a).save(os.path.join(ra, f"{a['order']:02d}_{a['att']}.png"))
    print(ra, len(atts), "part")


def main(a):
    if a[:1] == ["part_goc"]:
        xuat_part_goc()
    elif a[:1] == ["bo_cuc"]:
        for k in (a[1:] or ["pha_le", "gac"]):
            bo_cuc(k)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
