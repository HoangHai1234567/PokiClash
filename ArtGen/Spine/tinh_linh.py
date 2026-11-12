# -*- coding: utf-8 -*-
"""Tinh linh rừng mập (mã làm việc tinh_linh; con gốc của rig: monster_3407, game tham khảo). Tướng thứ 2 đảo Mộc, DẠNG 1.

Người dùng 2026-11-12: "concept tinh linh rừng chubby cute như hình, hơi trong suốt nhẹ; tạo hình chubby giống với hình, phần tóc trên
đầu có thể thay đổi tuỳ bạn"; chiêu mana cần thêm MỒM (con gốc không có mồm).
Cách làm = "reskin theo khung part" (skill pokiclash-spine-rig mục 00, mẫu xuong_rong.py / rong_vay.py): chỉ lấy của con gốc hình bóng,
chỗ đặt, thứ tự chồng của từng part; hình tô là THIẾT KẾ CỦA MÌNH (bảng màu, mắt có con ngươi, má hồng, mồm, nụ hoa hồng san hô).
Con gốc đã nhìn sang PHẢI nên không lật.

    tinh_linh.py part_goc     ảnh từng part của con gốc cắt theo lưới → <SXS>/scan/monster_3407/parts/ (chỉ để xem, nội bộ)
    tinh_linh.py bo_cuc [kiểu]  sơ đồ bố cục phẳng 1536 × 1024 từng hướng thiết kế (đính vào prompt concept) → inbox/tinh_linh_1/mau/bo_cuc_<kiểu>.png
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

CODE = "tinh_linh"
MON = "monster_3407"
K = int(os.environ.get("TL_DANG", "2"))        # dạng đang làm: đặt biến môi trường TL_DANG=1 | 2 | 3 (mặc định 2 = mầm hai lá)
BASE = os.path.join(HERE, "inbox", f"{CODE}_{K}")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
W, H = 1536, 1024
SC = 1.12                                        # đơn vị rig con gốc → pixel khung concept
INK = (43, 33, 24)
ATT = "att_goc.json"
# bảng màu ĐỀ XUẤT của Claude (người dùng chỉ dặn "tinh linh rừng chubby cute, hơi trong suốt"), chờ duyệt concept
PAL = dict(than=(150, 214, 178),                 # thạch ngọc bạc hà #96D6B2
           nep=(74, 150, 122),                   # nét nếp gấp, nét của thứ nằm TRONG thạch #4A967A
           la_dam=(62, 140, 88),                 # lá to phía sau #3E8C58
           la_tuoi=(156, 204, 92),               # lá non phía trước #9CCC5C
           cuong=(104, 170, 96),                 # cuống, dây leo #68AA60
           nu=(238, 138, 146),                   # nụ hoa hồng san hô #EE8A92
           mat=(255, 248, 232),                  # tròng mắt kem #FFF8E8
           ma=(244, 170, 168))                   # má hồng #F4AAA8


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
    if ten.startswith(("P_shenti", "P_tou2")):
        return "than"
    if ten.startswith("P_shouL"):
        return "tay_xa"
    if ten.startswith("P_shouR"):
        return "tay_gan"
    if ten.startswith("P_SL_bq"):
        return "mat"
    if ten.startswith("T_qiu"):
        return "nu"
    if ten.startswith("T_meimao"):
        return "day"
    if ten.startswith("T_yezi"):
        return "la"
    if ten.startswith("D_qiu"):
        return "trong_nu"
    if ten.startswith("D_shuzhi") or ten == "D_yezi1":
        return "trong_cuong"
    return "trong_la"


LA_TUOI = {"T_yezi1", "T_yezi6", "T_yezi8", "T_yezi9", "T_yezi7"}       # lá non phía trước; còn lại lá đậm phía sau


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


_C = {}


def nap():
    """(atlas, ảnh vùng đã gỡ xoay {tên: RGBA}, danh sách att dáng gốc theo thứ tự vẽ)."""
    if not _C:
        atlas, imgs = to_manh.nap(rig_goc(), MON)
        D = json.load(open(os.path.join(scan(), ATT), encoding="utf-8"))
        atts = sorted([a for a in D["atts"] if a.get("region") in imgs], key=lambda a: a["order"])
        _C.update(atlas=atlas, imgs=imgs, atts=atts, bones=D["bones"])
    return _C["atlas"], _C["imgs"], _C["atts"]


def luoi(a):
    """(uv theo pixel ảnh vùng, tam giác) của một hình; hình chữ nhật (region) thì dựng 2 tam giác từ khung đã cắt."""
    atlas, imgs, _ = nap()
    im = imgs[a["region"]]
    if a["type"].endswith("MeshAttachment"):
        return np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(a["tris"]).reshape(-1, 3)
    r = atlas[a["region"]]
    ox, oy, ow, oh = r.get("offsets", [0, 0, im.width, im.height])
    w, h = r["bounds"][2], r["bounds"][3]            # cỡ đã cắt, CHƯA xoay (to_manh.vung gỡ xoay rồi mới dán vào khung gốc)
    return np.array([[ox, oh - oy], [ox, oh - oy - h], [ox + w, oh - oy - h], [ox + w, oh - oy]], float), np.array([[0, 1, 2], [2, 3, 0]])


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
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts if a["cur"]])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = (H + (y1 - y0) * SC) / 2 + y0 * SC
    return lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1)


S2 = 2


def bong_khung(a, T):
    """hình bóng KÍN của một part đặt đúng chỗ dáng gốc trên khung concept (phóng S2), làm trơn: không mang nét vẽ của con gốc."""
    src = part_goc(a)
    al = np.asarray(src)[..., 3]
    one = Image.fromarray(np.dstack([np.full(al.shape + (3,), 255, np.uint8), np.where(al > 90, 255, 0).astype(np.uint8)]), "RGBA")
    uv, tr = luoi(a)
    V = T(np.array(a["xy"], float).reshape(-1, 2)) * S2
    lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
    _tris(lay, one.convert("RGBa"), V, uv, tr)
    m = (np.asarray(lay)[..., 3] > 110).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(3))
    m = cv2.GaussianBlur(m * 255, (0, 0), 2.2) > 127
    return m


def vien(m, r):
    return m & ~cv2.erode(m.astype(np.uint8), el(r)).astype(bool)


# ba hướng thiết kế lượt 2 (người dùng 2026-11-12: bản đầu "nhìn giống con gốc quá"; mắt chỉ lòng trắng; mồm chỉ hiện khi bắn chiêu):
# sơ đồ chỉ còn THÂN + TAY + MẮT (hình bóng theo part của rig); tóc và thứ nằm trong bụng tả bằng lời, là mảnh riêng của mình
KIEU = {
    "hoa": dict(than=(156, 203, 106), nep=(95, 143, 62), vanh=(58, 112, 44), ma=(240, 160, 140)),          # DẠNG 3: nở hoa, thân lục đậm hơn
    "hat": dict(than=(224, 234, 150), nep=(150, 172, 84), vanh=(104, 140, 62), ma=(242, 172, 150)),        # DẠNG 1: hạt chưa nảy mầm, thân nhạt
    "mam": dict(than=(200, 222, 142), nep=(127, 160, 80), vanh=(98, 140, 62), ma=(240, 170, 150)),         # matcha non + mầm hai lá
    "nam": dict(than=(246, 217, 184), nep=(190, 140, 96), vanh=(176, 122, 78), ma=(240, 150, 140)),        # kem đào + mũ nấm
    "ho_phach": dict(than=(237, 184, 90), nep=(185, 128, 46), vanh=(160, 104, 36), ma=(232, 130, 96)),     # nhựa cây hổ phách + rêu, cành
}


def bo_cuc(kieu="mam", luu=True):
    """sơ đồ bố cục: hình bóng thân, tay, mắt đặt đúng chỗ dáng gốc, tô phẳng theo THIẾT KẾ CỦA MÌNH (không tóc, không mồm)."""
    _, _, atts = nap()
    T = khung_T()
    C = KIEU[kieu]
    can_ve = ("P_shou", "P_shenti", "P_tou2", "P_SL_bq1")
    M = {a["att"]: bong_khung(a, T) for a in atts if a["cur"] and a["att"].startswith(can_ve)}
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    vi = 6

    def to(m, mau, net=INK, r=vi):
        can[m] = mau
        if net is not None:
            can[vien(m, r)] = net

    def gop(*ten):
        m = np.zeros((H * S2, W * S2), bool)
        for n in ten:
            m |= M[n]
        return cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, el(5)).astype(bool)

    tay_xa, tay_gan = gop("P_shouLA", "P_shouLB"), gop("P_shouRA", "P_shouRB")
    bung, dau = gop("P_shentiA", "P_shentiB"), gop("P_tou2A", "P_tou2B")
    khoi = bung | dau
    to(tay_xa, C["than"])
    to(khoi, C["than"])
    nep = vien(dau, 4) & cv2.erode(bung.astype(np.uint8), el(vi + 2)).astype(bool)
    xs = np.nonzero(nep.any(0))[0]
    if len(xs):
        x0, x1 = xs.min(), xs.max()
        cat = np.zeros_like(nep)
        cat[:, :int(x0 + 0.20 * (x1 - x0))] = True
        cat[:, int(x1 - 0.16 * (x1 - x0)):] = True
        can[nep & cat] = C["nep"]
    # mắt: chỉ lòng trắng, vành dày màu thân đậm (không mực, không con ngươi); má hồng; KHÔNG mồm
    mat = M["P_SL_bq1"]
    n, lab, st, _ = cv2.connectedComponentsWithStats(mat.astype(np.uint8), 8)
    hop = []
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] < 400:
            continue
        to(lab == i, (255, 255, 255), C["vanh"], 9)
        hop.append(tuple(st[i, :4]))
    hop.sort()
    pil = Image.fromarray(can)
    d = ImageDraw.Draw(pil)
    if len(hop) >= 2:
        (ax, ay, aw, ah), (bx, by, bw, bh) = hop[0], hop[-1]
        day = max(ay + ah, by + bh)
        d.ellipse([ax - aw * 0.05, day + 10, ax + aw * 0.55, day + 10 + ah * 0.36], fill=C["ma"])
        d.ellipse([bx + bw * 0.25, day + 6, bx + bw * 1.0, day + 6 + ah * 0.30], fill=C["ma"])
    can[:] = np.asarray(pil)
    to(tay_gan, C["than"])
    out = Image.fromarray(can).resize((W, H), Image.LANCZOS)
    if luu:
        os.makedirs(MAU, exist_ok=True)
        out.save(os.path.join(MAU, f"bo_cuc_{kieu}.png"))
        print(os.path.join(MAU, f"bo_cuc_{kieu}.png"))
    return out


def xuat_part_goc():
    ra = os.path.join(scan(), "parts")
    os.makedirs(ra, exist_ok=True)
    _, _, atts = nap()
    for a in atts:
        part_goc(a).save(os.path.join(ra, f"{a['order']:02d}_{a['att'].replace(' ', '')}.png"))
    print(ra, len(atts), "part")


def main(a):
    if a[:1] == ["part_goc"]:
        xuat_part_goc()
    elif a[:1] == ["bo_cuc"]:
        for k in (a[1:] or (["hat"] if K == 1 else ["hoa"] if K == 3 else ["mam", "nam", "ho_phach"])):
            bo_cuc(k)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
