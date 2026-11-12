# -*- coding: utf-8 -*-
"""Người cây đầm lầy (mã làm việc nguoi_cay; con gốc của rig: monster_3491, game tham khảo). Tướng thứ 7 đảo Mộc.

Người dùng 2026-11-12: "concept là giống với swampthing của DC, một humanoid bọc trong các lớp thực vật". Hình là thiết kế của mình
(không chép nhân vật đó: không mặt nạ rễ sống mũi, không mắt đỏ, không thân bùn lục một màu); con gốc chỉ cho bộ khung dáng người đấm
bốc (thân, hai tay ba khúc, hai chân ba khúc, vạt váy). Đầu rương của con gốc BỎ HẲN, thay bằng đầu của mình.
Con gốc nhìn sang PHẢI, góc ba phần tư: tay R (bên trái hình, buông thấp) là tay GẦN vẽ trước thân; tay L (bên phải hình, nắm đấm giơ
ngang mặt) là tay XA vẽ sau thân. Không lật.

    nguoi_cay.py part_goc       ảnh từng part của con gốc cắt theo lưới → <SXS>/scan/monster_3491/parts/ (chỉ để xem, nội bộ)
    nguoi_cay.py bo_cuc [kiểu]  sơ đồ bố cục phẳng 1536 × 1024 (dam_lay | mat_go: bản 1 bị trả; chien: bản 2) → inbox/nguoi_cay_1/mau/bo_cuc_<kiểu>.png
    nguoi_cay.py luoi_xem       sơ đồ thân trơn có kẻ lưới toạ độ (để đọc chỗ đặt chi tiết) → mau/_luoi.png
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

CODE = "nguoi_cay"
MON = "monster_3491"
K = int(os.environ.get("NC_DANG", "2"))        # dạng đang làm: NC_DANG=1 (con non) | 2 (dạng lớn, mặc định)
BASE = os.path.join(HERE, "inbox", f"{CODE}_{K}")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
W, H = 1536, 1024
SC = 1.24                                        # đơn vị rig con gốc → pixel khung concept
DY = 34                                          # dời cả con xuống (chừa chỗ cho chồi trên đầu)
INK = (43, 33, 24)
ATT = "att_idle0.json"                           # dáng đứng thủ của idle_01 giây 0
S2 = 2

# bảng màu ĐỀ XUẤT của Claude, chờ người dùng chọn hướng
PALS = {
    "dam_lay": dict(reu=(111, 148, 64),          # rêu ô-liu (mũ trùm, u vai, đùi) #6F9440
                    reu_ru=(160, 186, 110),      # rêu rủ sợi nhạt #A0BA6E
                    la=(47, 117, 88),            # lá to lục lam sẫm (áo ngực, váy) #2F7558
                    la_nhat=(156, 196, 86),      # lá non, dương xỉ #9CC456
                    re=(139, 98, 56),            # rễ bện (bắp tay, bụng, ống chân) #8B6238
                    go=(170, 124, 74),           # gỗ rễ nắm tay, bàn chân #AA7C4A
                    day=(62, 107, 58),           # dây gai #3E6B3A
                    gai=(239, 224, 168),         # gai kem #EFE0A8
                    mat_nen=(59, 47, 39),        # hốc mặt tối #3B2F27
                    mat=(246, 217, 62),          # mắt vàng #F6D93E
                    nam=(224, 96, 58),           # mũ nấm cam đỏ #E0603A
                    kem=(239, 227, 196)),        # chân nấm, chấm nấm #EFE3C4
    "mat_go": dict(reu=(92, 150, 70),            # tán lá đầu, u vai #5C9646
                   reu_ru=(168, 204, 96),        # lá non #A8CC60
                   la=(62, 132, 72),             # lá áo ngực, váy #3E8448
                   la_nhat=(168, 204, 96),
                   re=(150, 110, 70),            # rễ bện #966E46
                   go=(214, 190, 150),           # gỗ nhạt: mặt nạ, nắm tay, bàn chân #D6BE96
                   day=(70, 110, 60),
                   gai=(239, 224, 168),
                   mat_nen=(214, 190, 150),      # mặt gỗ nhạt
                   mat=(240, 170, 50),           # mắt hổ phách #F0AA32
                   nam=(170, 96, 184),           # hoa kế tím #AA60B8
                   kem=(239, 227, 196)),
    # bản 2 (người dùng trả bản 1: "chưa đủ chiến, đầu nhìn xấu quá, làm sát với swampthing hơn 1 chút"): thân rêu lục gần kín
    "chien": dict(than=(78, 122, 62),            # thân, bắp tay, đùi: bó dây leo phủ rêu sẫm #4E7A3E
                  reu=(124, 164, 74),            # u rêu vai, rêu rủ #7CA44A
                  reu_ru=(124, 164, 74),
                  la=(44, 96, 66),               # lá sẫm răng cưa #2C6042
                  la_nhat=(146, 186, 92),        # lá nhạt #92BA5C
                  re=(122, 90, 58),              # cành khô, rễ #7A5A3A
                  go=(152, 114, 72),             # gỗ rễ: cẳng tay, nắm tay, ống chân, bàn chân #987248
                  day=(47, 82, 51),              # dây gai #2F5233
                  gai=(239, 224, 168),
                  mat_nen=(40, 50, 36),          # hốc mắt tối #283224
                  mat=(238, 108, 44),            # mắt cam lửa #EE6C2C
                  nam=(224, 96, 58), kem=(239, 227, 196)),
}
PAL = PALS["dam_lay"]

NHOM = {"P_shenti2": "re", "P_shouR1": "re", "P_shouL1": "re", "P_shouR2": "day", "P_shouL2": "day", "P_shouR3": "go", "P_shouL3": "go",
        "P_tuiR1": "reu", "P_tuiL1": "reu", "P_tuiR2": "re", "P_tuiL2": "re", "P_jiaoR": "go", "P_jiaoL": "go", "P_bu": "la", "P_bu2": "la"}


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
        atts = sorted([a for a in D["atts"] if a.get("region") in imgs and a["cur"]], key=lambda a: a["order"])
        _C.update(atlas=atlas, imgs=imgs, atts=atts, bones=D["bones"])
    return _C["atlas"], _C["imgs"], _C["atts"]


def luoi(a):
    _, imgs, _ = nap()
    im = imgs[a["region"]]
    return np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(a["tris"]).reshape(-1, 3)


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
    """rig → pixel khung concept: thân (không kể đầu rương) nằm giữa khung theo chiều ngang, bàn chân cách đáy ~70 px."""
    _, _, atts = nap()
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, x1 = P[:, 0].min(), P[:, 0].max()
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = H - 70 + P[:, 1].min() * SC
    return lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1)


def bong_khung(a, T, tron=5.0):
    """hình bóng KÍN của một part đặt đúng chỗ trên khung concept (phóng S2), làm trơn mạnh: chỉ còn khối."""
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


# ---------------------------------------------------------------- hình vẽ thêm bằng mã (toạ độ pixel khung concept)
def _pts(ps):
    return (np.array(ps, float) * S2).astype(np.int32)


def to(can, m, mau, net=6):
    can[m] = mau
    if net:
        can[vien(m, net)] = INK


def mask_poly(ps, tron=3.0):
    m = np.zeros((H * S2, W * S2), np.uint8)
    cv2.fillPoly(m, [_pts(ps)], 255, cv2.LINE_AA)
    if tron:
        m = cv2.GaussianBlur(m, (0, 0), tron * S2)
    return m > 127


def mask_el(c, ax, goc=0.0):
    m = np.zeros((H * S2, W * S2), np.uint8)
    cv2.ellipse(m, (int(c[0] * S2), int(c[1] * S2)), (int(ax[0] * S2), int(ax[1] * S2)), goc, 0, 360, 255, -1, cv2.LINE_AA)
    return m > 127


def la(can, goc, mui, rong, mau, gan=None, net=5):
    """một chiếc lá nhọn hai đầu: goc = cuống, mui = mũi lá, rong = bề rộng lớn nhất; một gân giữa."""
    g, t = np.array(goc, float), np.array(mui, float)
    d = t - g
    L = np.hypot(*d)
    u = d / L
    n = np.array([-u[1], u[0]])
    ps = []
    for s in np.linspace(0, 1, 15):
        ps.append(g + u * L * s + n * rong / 2 * np.sin(np.pi * s) ** 0.75)
    for s in np.linspace(1, 0, 15):
        ps.append(g + u * L * s - n * rong / 2 * np.sin(np.pi * s) ** 0.75)
    m = mask_poly(ps, 0.8)
    to(can, m, mau, net)
    if gan is not None:
        cv2.line(can, tuple(_pts([g + u * L * 0.08])[0]), tuple(_pts([g + u * L * 0.86])[0]), gan, 3 * S2 // 2, cv2.LINE_AA)
    return m


def duong(can, ps, day, mau, net=5):
    """một dải cong (dây leo, cuống): đường gấp khúc làm trơn, bề dày day."""
    m = np.zeros((H * S2, W * S2), np.uint8)
    cv2.polylines(m, [_pts(ps)], False, 255, int(day * S2), cv2.LINE_AA)
    m = cv2.GaussianBlur(m, (0, 0), 1.5 * S2) > 127
    to(can, m, mau, net)
    return m


def nam(can, c, r, P):
    """một cây nấm nhỏ: chân kem, mũ vòm có ba chấm."""
    x, y = c
    to(can, mask_poly([(x - r * 0.28, y), (x - r * 0.22, y + r * 0.9), (x + r * 0.22, y + r * 0.9), (x + r * 0.28, y)], 0.6), P["kem"], 4)
    m = mask_el((x, y), (r, r * 0.72)) & (np.arange(H * S2)[:, None] < (y + r * 0.12) * S2)
    to(can, m, P["nam"], 4)
    for dx, dy, rr in [(-0.45, -0.25, 0.15), (0.2, -0.42, 0.17), (0.55, -0.12, 0.12)]:
        cv2.circle(can, (int((x + dx * r) * S2), int((y + dy * r) * S2)), int(rr * r * S2), P["kem"], -1, cv2.LINE_AA)


def than_tron(P, bo=()):
    """khối các part thân của con gốc (không đầu rương), tô theo nhóm màu của mình. Trả (ảnh S2, hộp từng part)."""
    _, _, atts = nap()
    T = khung_T()
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop = {}
    for a in atts:
        ten = a["att"]
        if ten not in NHOM or ten in bo:
            continue
        nho = ten.startswith(("P_jiao", "P_bu2"))
        m = bong_khung(a, T, 3.0 if nho else 6.0)
        if ten.endswith("3") and ten.startswith("P_shou"):               # nắm tay rễ to hơn nắm tay con gốc một chút
            m = cv2.dilate(m.astype(np.uint8), el(9)).astype(bool)
        if not m.any():
            continue
        to(can, m, P[NHOM[ten]], 6)
        ys, xs = np.nonzero(m)
        hop[ten] = [int(xs.min() / S2), int(ys.min() / S2), int(xs.max() / S2), int(ys.max() / S2)]
    return can, hop, T


def luoi_xem():
    can, hop, T = than_tron(PAL)
    im = Image.fromarray(can).resize((W, H), Image.LANCZOS)
    # bóng mờ đầu rương của con gốc để biết chỗ đầu (chỉ trên tờ lưới nội bộ)
    _, _, atts = nap()
    d = ImageDraw.Draw(im)
    for a in atts:
        if a["att"] not in NHOM:
            P = T(np.array(a["xy"], float).reshape(-1, 2))
            d.rectangle([P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()], outline=(255, 150, 150))
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    for x in range(0, W, 50):
        d.line([(x, 0), (x, H)], fill=(0, 120, 255) if x % 100 == 0 else (190, 215, 255), width=1)
        if x % 100 == 0:
            d.text((x + 2, 2), str(x), fill=(0, 60, 200), font=f)
    for y in range(0, H, 50):
        d.line([(0, y), (W, y)], fill=(0, 120, 255) if y % 100 == 0 else (190, 215, 255), width=1)
        if y % 100 == 0:
            d.text((2, y + 2), str(y), fill=(0, 60, 200), font=f)
    os.makedirs(MAU, exist_ok=True)
    im.save(os.path.join(MAU, "_luoi.png"))
    for k, v in hop.items():
        print(f"  {k:12s} x {v[0]}-{v[2]}  y {v[1]}-{v[3]}")
    xs = [T((0, 0)), T((0, 400)), T((0, 630))]
    print("gốc rig (0,0) →", xs[0], " (0,400) →", xs[1], " (0,630) →", xs[2])
    print(os.path.join(MAU, "_luoi.png"))


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
    elif a[:1] == ["luoi_xem"]:
        luoi_xem()
    elif a[:1] == ["bo_cuc"]:
        import nguoi_cay_bo_cuc as B
        for k in (a[1:] or list(PALS)):
            B.bo_cuc(k)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
