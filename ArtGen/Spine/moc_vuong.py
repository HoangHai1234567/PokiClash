# -*- coding: utf-8 -*-
"""Boss cuối đảo Mộc (mã làm việc moc_vuong; con gốc của rig: monster_3709 của game tham khảo, do người dùng chỉ 2026-11-13).

Chỉ lấy của con gốc CÁCH DỰNG (bốn chân, bốn cánh xếp từ từng chiếc lông rời, đuôi dải dài vắt trước thân, chỗ đặt, cỡ, thứ tự chồng);
hình là thiết kế của mình: rồng trúc (cánh trên lá trúc, cánh dưới lá trúc ngà, sừng ống trúc vát, giáp tre, ngọc bích).

    py -3 -I ArtGen/Spine/moc_vuong.py bo_cuc [nga|mac]     sơ đồ bố cục cho GPT: khối từng part ở idle giây 0, tô phẳng theo bảng màu mình
                                                            → inbox/moc_vuong_1/mau/bo_cuc_<kiểu>.png + bo_cuc.json (khung từng nhóm)

Dữ liệu quét (mo_xe/chay.py) ở <SXS>/scan/monster_3709/. SXS mặc định D:/RefAnimation/SwordxStaff (máy D), đổi bằng biến môi trường SXS.
"""
import colorsys
import json
import os
import re
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
import to_manh as TM  # noqa: E402
from quai.soi import _tris  # noqa: E402

CODE, GOC = "moc_vuong", "monster_3709"
SXS = os.environ.get("SXS") or next((p for p in ("D:/RefAnimation/SwordxStaff", "D:/Ripper/SwordxStaff", "E:/Ripper/SwordxStaff")
                                      if os.path.isdir(p)), "D:/RefAnimation/SwordxStaff")
RIG = f"{SXS}/web/assets/Monster/{GOC}"
SCAN = f"{SXS}/scan/{GOC}"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
W, H, S2 = 1536, 1024, 2
INK = (43, 33, 24)
TI = 0.632                      # đơn vị rig → pixel khung concept

# bảng màu của MÌNH theo hai kiểu (đề xuất của Claude 2026-11-13, chờ người dùng chọn)
HUONG = {
    "nga": dict(la_dam=(47, 107, 63),        # lá trúc sẫm #2F6B3F
                la=(95, 168, 74),            # lá trúc #5FA84A
                la_nhat=(168, 212, 104),     # lá non #A8D468
                nga=(232, 192, 74),          # trúc ngà vàng #E8C04A
                nga_dam=(201, 154, 46),      # ngà sẫm #C99A2E
                kem=(244, 235, 208),         # lông kem #F4EBD0
                than=(244, 235, 208),        # thân: lông kem
                vay=(62, 143, 106),          # vảy cổ ngọc #3E8F6A
                chan=(42, 90, 74),           # ống chân giáp trúc sẫm #2A5A4A
                giap=(233, 217, 166),        # giáp tre ngà nhạt #E9D9A6
                ngoc=(63, 191, 143),         # ngọc bích #3FBF8F
                nhan=(217, 72, 43),          # đỏ son #D9482B
                mat_dau=(62, 143, 106),      # mặt: vảy ngọc
                bom=(244, 235, 208)),
    "mac": dict(la_dam=(30, 84, 62),         # lục bảo sẫm #1E543E
                la=(52, 140, 92),            # lục bảo #348C5C
                la_nhat=(120, 196, 128),     # #78C480
                nga=(236, 196, 80),          # vàng ngà #ECC450
                nga_dam=(196, 146, 40),      # #C49228
                kem=(240, 232, 206),
                than=(58, 68, 64),           # thân: lông mực than #3A4440
                vay=(196, 146, 40),          # vảy cổ vàng sẫm
                chan=(36, 44, 42),           # ống chân mực #242C2A
                giap=(236, 196, 80),         # giáp vàng ngà
                ngoc=(63, 191, 143),
                nhan=(217, 72, 43),
                mat_dau=(58, 68, 64),
                bom=(240, 232, 206)),
}


def nap():
    atlas, imgs = TM.nap(RIG, GOC)
    D = json.load(open(f"{SCAN}/att_idle0.json", encoding="utf-8"))
    atts = sorted([a for a in D["atts"] if a.get("region") in imgs and a["cur"]], key=lambda a: a["order"])
    return imgs, D, atts


def khung_T(atts):
    P = np.array([v for a in atts for v in np.array(a["xy"]).reshape(-1, 2).tolist()])
    cx, cy = (P[:, 0].min() + P[:, 0].max()) / 2, (P[:, 1].min() + P[:, 1].max()) / 2

    def T(V):
        return np.stack([(V[:, 0] - cx) * TI + W / 2, (cy - V[:, 1]) * TI + H / 2 + 4], 1)
    return T


def bong(a, imgs, T, tron):
    """hình bóng KÍN của một part đặt đúng chỗ trên khung concept (phóng S2), làm trơn: chỉ còn khối."""
    im = imgs[a["region"]]
    V = T(np.array(a["xy"], float).reshape(-1, 2)) * S2
    UV = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
    lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
    _tris(lay, im.convert("RGBa"), V, UV, np.array(a["tris"]).reshape(-1, 3))
    m = (np.asarray(lay)[..., 3] > 90).astype(np.uint8) * 255
    if tron:
        m = cv2.GaussianBlur(m, (0, 0), tron * S2)
    return m > 127


def mau_goc(im):
    """màu trung vị của ảnh part gốc (chỉ để xếp TẦNG sáng tối / nhóm sắc; không lấy màu đó)."""
    a = np.asarray(im.convert("RGBA")).reshape(-1, 4).astype(float)
    a = a[(a[:, 3] > 200) & (a[:, :3].sum(1) > 150)]
    if not len(a):
        return 0, 0, 1
    r, g, b = np.median(a[:, :3], 0) / 255
    return colorsys.rgb_to_hsv(r, g, b)


def vien(m, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return m & ~cv2.erode(m.astype(np.uint8), k).astype(bool)


def to(can, m, mau, net=6):
    can[m] = mau
    if net:
        can[vien(m, net)] = INK


def truc(m):
    """trục dài của một khối: hai đầu mút (px khung S2)."""
    ys, xs = np.nonzero(m)
    P = np.stack([xs, ys], 1).astype(float)
    c = P.mean(0)
    u = np.linalg.svd(P - c, full_matrices=False)[2][0]
    t = (P - c) @ u
    return c + u * t.min(), c + u * t.max()


def nhom_cua(slot):
    return re.sub(r"_?\d+$", "", slot)


def mau_part(slot, hsv, P):
    """nhóm màu của mình cho một part: theo nhóm slot, và với cánh thì theo tầng sắc của chiếc lông gốc."""
    g = nhom_cua(slot)
    h, s, v = hsv
    hd = h * 360
    if g.startswith("chibang_h"):                         # cánh TRÊN: lá trúc lục ba tầng
        if s > 0.45 and (hd < 45 or hd > 345):
            return "nhan"                                 # móc ở ngọn dây cánh
        if s < 0.16:
            return "la_nhat"                              # lông phủ trong (kem ở con gốc) → lá non
        if 200 <= hd <= 262:
            return "la_dam"
        if hd > 262:
            return "nga"
        return "la"
    if g.startswith("chibang_q"):                         # cánh DƯỚI: lá trúc ngà vàng
        if s < 0.10:
            return "kem"
        if 140 <= hd <= 200:
            return "la_nhat"
        return "nga" if v > 0.86 else "nga_dam"
    if g.startswith("weiba"):
        return "la" if (140 <= hd <= 200) else "la_dam"   # đuôi: dải lá dài hai mặt
    if g in ("houzhi_l", "houzhi_r", "qianzhi_l", "qianzhi_r"):
        n = int(slot.rsplit("_", 1)[1])
        if g.startswith("qianzhi"):
            return {1: "nga", 2: "nga", 3: "nga", 4: "chan", 5: "chan", 6: "chan", 7: "than", 8: "nga_dam", 9: "nga_dam", 10: "nga_dam"}.get(n, "chan")
        return {1: "than", 8: "chan"}.get(n, "nga" if n in (5, 6, 7) else "chan")
    if g == "shenti":
        return "than"
    if g.startswith("xiongjia") or g.startswith("hujian"):
        return "giap"
    if g == "toufa":
        return "bom"
    if g == "longjiao":
        return "nga"
    if g == "tou":
        return "mat_dau"
    return "kem"


def bo_cuc(kieu="nga", luu=True):
    P = HUONG[kieu]
    imgs, D, atts = nap()
    T = khung_T(atts)
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop = {}
    for a in atts:
        ten = a["slot"]
        if ten == "biyan":
            continue
        g = nhom_cua(ten)
        im = imgs[a["region"]]
        nho = max(im.width, im.height) < 70
        m = bong(a, imgs, T, 1.2 if nho else 2.6)
        if not m.any():
            continue
        ys, xs = np.nonzero(m)
        b = hop.setdefault(g, [10 ** 6, 10 ** 6, 0, 0])
        b[0], b[1], b[2], b[3] = min(b[0], int(xs.min() / S2)), min(b[1], int(ys.min() / S2)), max(b[2], int(xs.max() / S2)), max(b[3], int(ys.max() / S2))
        hop[ten] = [int(xs.min() / S2), int(ys.min() / S2), int(xs.max() / S2), int(ys.max() / S2)]
        if g == "longjiao":                                # sừng: KHÔNG dùng hình bóng sừng lửa của con gốc; vẽ ống trúc vát theo trục
            p0, p1 = truc(m)
            if p0[1] < p1[1]:
                p0, p1 = p1, p0                            # p0 = gốc (thấp), p1 = ngọn (cao)
            sung(can, p0, p1, P, a["slot"].endswith("01"))
            continue
        k = mau_part(ten, mau_goc(im), P)
        to(can, m, P[k], 3 if nho else 5)
        if g.startswith("chibang") and not nho and k != "nhan":   # sống lá
            p0, p1 = truc(cv2.erode(m.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool) if m.sum() > 4000 else m)
            q0, q1 = p0 + (p1 - p0) * 0.14, p0 + (p1 - p0) * 0.86
            cv2.line(can, tuple(q0.astype(int)), tuple(q1.astype(int)), INK, S2 + 1, cv2.LINE_AA)
        if ten == "xiongjia_08":                           # ngọc bích giữa ngực
            mm = cv2.erode(m.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (29, 29))).astype(bool)
            if mm.any():
                to(can, mm, P["ngoc"], 4)
    out = Image.fromarray(can).resize((W, H), Image.LANCZOS)
    if luu:
        os.makedirs(MAU, exist_ok=True)
        p = os.path.join(MAU, f"bo_cuc_{kieu}.png")
        out.save(p)
        json.dump(hop, open(os.path.join(MAU, "bo_cuc.json"), "w", encoding="utf-8"), indent=0)
        print(p)
        for k in sorted(k for k in hop if not re.search(r"\d$", k)):
            print(f"  {k:14s} {hop[k]}")
    return out


def sung(can, p0, p1, P, to_hon):
    """một chiếc sừng ống trúc: ba đốt hơi cong, ngọn vát chéo, vòng mắt trúc ở khớp; kèm một nhánh con mang hai lá."""
    d = p1 - p0
    L = np.hypot(*d)
    u = d / L
    n = np.array([-u[1], u[0]])
    day = L * (0.15 if to_hon else 0.17)
    cong = L * 0.10 * (1 if u[0] < 0 else -1)
    pts = [p0 + u * L * s + n * cong * np.sin(np.pi * s) for s in np.linspace(0, 1, 13)]
    m = np.zeros(can.shape[:2], np.uint8)
    cv2.polylines(m, [np.array(pts).astype(np.int32)], False, 255, int(day), cv2.LINE_8)
    tip = pts[-1]
    cat = np.array([tip + n * day, tip - n * day + u * day * 0.2, tip + u * day * 1.6 + n * day, tip + u * day * 1.6 - n * day])
    cv2.fillPoly(m, [np.array([tip - n * day * 0.6 + u * day * 0.9, tip + u * day * 2, tip + n * day * 2 + u * day * 2,
                               tip + n * day * 0.62 - u * day * 0.2]).astype(np.int32)], 0)       # vát chéo ngọn
    m = cv2.GaussianBlur(m, (0, 0), 1.2 * S2) > 127
    to(can, m, P["nga"], 5)
    for s in (0.3, 0.62):                                  # mắt trúc
        c = p0 + u * L * s + n * cong * np.sin(np.pi * s)
        cv2.line(can, tuple((c - n * day * 0.5).astype(int)), tuple((c + n * day * 0.5).astype(int)), P["la_dam"], 3 * S2, cv2.LINE_AA)
    c = p0 + u * L * 0.62 + n * cong * np.sin(np.pi * 0.62)  # nhánh con + hai lá
    side = -n if u[0] < 0 else n
    for goc, dai in ((0.5, 0.42), (1.0, 0.36)):
        t = c + (u * np.cos(goc) + side * np.sin(goc)) * L * dai
        la(can, c, t, L * 0.11, P["la"])
    del cat


def la(can, goc, mui, rong, mau):
    g, t = np.array(goc, float), np.array(mui, float)
    d = t - g
    L = np.hypot(*d)
    u = d / L
    n = np.array([-u[1], u[0]])
    tr, du = [], []
    for s in np.linspace(0, 1, 15):
        c = g + u * L * s
        w = rong / 2 * np.sin(np.pi * min(1, s * 1.25)) ** 0.8 if s < 0.8 else rong / 2 * (1 - s) / 0.2 * np.sin(np.pi * 1.0 * 0.8 * 1.25 / 1.25) ** 0.8
        tr.append(c + n * w)
        du.append(c - n * w)
    m = np.zeros(can.shape[:2], np.uint8)
    cv2.fillPoly(m, [np.array(tr + du[::-1]).astype(np.int32)], 255, cv2.LINE_AA)
    to(can, m > 127, mau, 4)


# ================================================================ MẢNH THEO KHUNG PART (sau khi người dùng chốt concept 2026-11-13:
# bản tối `mac` + sừng măng → tai_ve/L1_duyet.png). Mỗi part của rig một ô đúng khung ảnh vùng (× z), trong ô là hình bóng KÍN của part
# tô phẳng theo thiết kế của mình; Codex vẽ lại sạch, giữ hình bóng. Đầu và sừng KHÔNG đi đường này (mảnh riêng cắt từ concept).
MANH = os.path.join(BASE, "manh")
TAI = os.path.join(BASE, "tai_ve")
Z = 2                           # ảnh vùng atlas phóng 2 lần = đúng cỡ thế giới của họ (atlas của họ 0,5 px / đơn vị)
PAL = HUONG["mac"]
BO_NHOM = ("longjiao", "biyan")          # sừng (ô riêng vẽ mới: sừng măng), mắt nhắm (dựng bằng mã từ ảnh sọ)
MAU_DAU = dict(ham=(89, 100, 95), luoi=(200, 80, 60), mat=(240, 170, 50))      # hàm dưới xám nhạt hơn, lưỡi đỏ, mắt hổ phách
# hai sừng măng: (tên ô, dài, bề ngang gốc, độ cong sang trái) theo đơn vị rig con gốc; sừng gần to hơn
SUNG = [("sung_1", 455.0, 118.0, 70.0), ("sung_2", 380.0, 96.0, 26.0)]
_C = {}


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def nap_goc():
    """(ảnh vùng {tên: RGBA}, {tên hình: att dáng gốc}, danh sách att theo thứ tự vẽ, xương dáng gốc)."""
    if not _C:
        _, imgs = TM.nap(RIG, GOC)
        D = json.load(open(f"{SCAN}/att_goc.json", encoding="utf-8"))
        atts = sorted([a for a in D["atts"] if a.get("region") in imgs], key=lambda a: a["order"])
        _C.update(imgs=imgs, by={a["att"]: a for a in atts}, atts=atts, bones=D["bones"])
    return _C["imgs"], _C["by"], _C["atts"]


def part_goc(ten, z=1):
    """ảnh một part của con gốc cắt đúng theo lưới của nó (ảnh vùng atlas là chữ nhật nên dính mảnh bên cạnh)."""
    imgs, by, _ = nap_goc()
    a = by[ten]
    im = imgs[a["region"]].convert("RGBA")
    uv = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
    m = np.zeros((im.height * 4, im.width * 4), np.uint8)
    for t in np.array(a["tris"]).reshape(-1, 3):
        cv2.fillPoly(m, [np.round(uv[t] * 4).astype(np.int32)], 255)
    m = cv2.dilate(m, el(3))
    A = np.asarray(im).copy()
    A[..., 3] = (A[..., 3].astype(np.float32) * cv2.resize(m, im.size, interpolation=cv2.INTER_AREA) / 255.0).astype(np.uint8)
    out = Image.fromarray(A, "RGBA")
    return out if z == 1 else out.resize((im.width * z, im.height * z), Image.LANCZOS)


def z_cua(ten):
    imgs, by, _ = nap_goc()
    im = imgs[by[ten]["region"]]
    d = max(im.size)
    return 2 if d * 2 >= 250 else (3 if d * 3 >= 250 else 4)


def bong_part(ten, z=Z):
    """hình bóng KÍN của part (làm trơn nhẹ, không mang nét vẽ của họ), cỡ ảnh vùng × z; kèm ảnh gốc RGBA cùng cỡ."""
    a = np.asarray(part_goc(ten, z))
    m = (a[..., 3] > 100).astype(np.uint8)
    le = 16 * z
    m = cv2.copyMakeBorder(m, le, le, le, le, cv2.BORDER_CONSTANT, value=0)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(2 * z))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, el(0.8 * z))
    nho = max(a.shape[:2]) / z < 70
    m = (cv2.GaussianBlur(m * 255, (0, 0), (0.9 if nho else 1.7) * z) > 127)[le:-le, le:-le]
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n > 2:                                              # bỏ mẩu vụn (dưới 4 % mảng lớn nhất)
        lon = st[1:, cv2.CC_STAT_AREA].max()
        for i in range(1, n):
            if st[i, cv2.CC_STAT_AREA] < 0.04 * lon:
                m[lab == i] = False
    return m, a


def hsv_goc(a):
    """(h độ, s, v) từng điểm của ảnh part gốc: chỉ để TÁCH VÙNG (móng / ngón, vảy / lông), không lấy màu."""
    x = a[..., :3].astype(np.float32) / 255.0
    hsv = cv2.cvtColor(x, cv2.COLOR_RGB2HSV)
    return hsv[..., 0], hsv[..., 1], hsv[..., 2]


def tach(a, m, dk, z, tron=2.0):
    """vùng con của part theo điều kiện trên (h, s, v) của ảnh gốc, làm trơn, nằm trong hình bóng m."""
    h, s, v = hsv_goc(a)
    r = (dk(h, s, v) & (a[..., 3] > 100)).astype(np.uint8)
    r = cv2.morphologyEx(r, cv2.MORPH_OPEN, el(1.2 * z))
    r = cv2.morphologyEx(r, cv2.MORPH_CLOSE, el(2.5 * z))
    r = cv2.GaussianBlur(r * 255, (0, 0), tron * z) > 127
    return r & m


def truc_dai(m):
    ys, xs = np.nonzero(m)
    Pp = np.stack([xs, ys], 1).astype(float)
    c = Pp.mean(0)
    u = np.linalg.svd(Pp - c, full_matrices=False)[2][0]
    t = (Pp - c) @ u
    n = np.array([-u[1], u[0]])
    w = (Pp - c) @ n
    return c, u, t.min(), t.max(), n, w.min(), w.max()


def vai_cua(ten):
    """vai trò của part trong thiết kế của mình: (kiểu, khoá màu chính, khoá màu phụ)."""
    imgs, by, _ = nap_goc()
    g = nhom_cua(ten)
    so = int(ten.rsplit("_", 1)[1]) if re.search(r"_\d+$", ten) else 0
    im = imgs[by[ten]["region"]]
    if g.startswith("chibang"):
        k = mau_part(ten, mau_goc(part_goc(ten)), PAL)
        if g.startswith("chibang_h") and so in (22, 23):
            return "day", "la", "nhan"                       # dải dây dài rủ xuống, nụ đỏ ở móc
        if (g.startswith("chibang_h") and so in (2, 3)) or (g.startswith("chibang_q") and so in (1, 2, 14, 15)):
            return "hang_la", k if k != "nhan" else "la", None
        return "la", (k if k != "nhan" else "la"), None
    if g.startswith("weiba"):
        return "dai", mau_part(ten, mau_goc(part_goc(ten)), PAL), None
    if g.startswith("qianzhi"):
        if so == 7:
            return "long", "than", None                      # bắp chân trước: lông mực
        if so == 6:
            return "giap_chan", "chan", "nga"                # ống chân: giáp trúc đen, vòng vàng
        if so == 4:
            return "long", "than", None                      # mu bàn chân
        if so in (8, 9, 10):
            return "la", "nga_dam", None                     # chùm lá khuỷu
        return "ngon", "than", "nga"                         # ngón + móng vàng
    if g.startswith("houzhi"):
        if so == 1:
            return "long", "than", None                      # đùi
        lon = max(im.size)
        if (g.endswith("_r") and so == 6) or (g.endswith("_l") and so == 7):
            return "giap_chan", "chan", "nga"
        if (g.endswith("_r") and so in (5, 8)) or (g.endswith("_l") and so == 6):
            return "long", "than", None
        del lon
        return "ngon", "than", "nga"
    if g == "shenti":
        return "than", "than", "vay"
    if g.startswith("xiongjia"):
        if g == "xiongjia" and so == 6:
            return "ngoc", "ngoc", "giap"
        if g == "xiongjia" and so == 7:
            return "o_ngoc", "giap", "la_dam"
        if g == "xiongjia" and so == 5:
            return "la", "kem", None
        return "giap", "giap", None
    if g.startswith("hujian"):
        return "giap_vai", "giap", "ngoc"
    if g == "toufa":
        return "bom", "bom", None
    if g == "tou":
        return {1: ("so", "than", "nga"), 2: ("ham", "ham", None), 3: ("luoi", "luoi", None), 4: ("ham_trong", "chan", None),
                5: ("tai", "la", None), 6: ("long", "than", None)}[so]
    return "tron", "kem", None


def thiet_ke(ten, z=None):
    """thiết kế phẳng của mình cho một part, vẽ ngay trong khung ảnh vùng của nó (× z): (RGB nền trắng, mặt nạ hình bóng)."""
    z = z or z_cua(ten)
    m, a = bong_part(ten, z)
    kieu, k1, k2 = vai_cua(ten)
    H_, W_ = m.shape
    im = np.full((H_, W_, 3), 255, np.uint8)
    nho = max(H_, W_) / z < 70
    net = max(2, int(round((2.0 if nho else 3.0) * z)))
    C = dict(PAL, **MAU_DAU)
    im[m] = C[k1]
    if kieu == "so":                                         # sọ: gờ mày vàng (chỗ con gốc là tấm lục quanh mắt + mấu sừng nhỏ), mắt hổ phách
        mm = tach(a, m, lambda h, s, v: (((h > 55) & (h < 130) & (s > 0.18)) | ((h > 20) & (h < 48) & (s > 0.25) & (v < 0.9))), z, 1.2)
        im[mm] = C[k2]
        im[vien(mm, max(1, net // 2)) & m] = INK
        me = tach(a, m, lambda h, s, v: (h > 165) & (h < 205) & (s > 0.35), z, 0.6)
        im[me] = C["mat"]
        im[vien(me, max(1, net // 3)) & m] = INK
    if kieu in ("ngon",):                                    # móng: phần lam tươi của ảnh gốc
        mg = tach(a, m, lambda h, s, v: (h > 185) & (h < 235) & (s > 0.42) & (v > 0.62), z, 1.0)
        im[mg] = PAL[k2]
        im[vien(mg, max(1, net // 2)) & m] = INK
    if kieu == "than":                                       # vảy cổ + vảy bụng: chỗ ảnh gốc là ô liu hoặc chàm
        mv = tach(a, m, lambda h, s, v: ((h > 45) & (h < 100) & (s > 0.22)) | ((h > 225) & (h < 265) & (s > 0.3) & (v > 0.55)), z, 2.5)
        im[mv] = PAL[k2]
        im[vien(mv, max(1, net // 2)) & m] = INK
        c, u, t0, t1, n, w0, w1 = truc_dai(mv) if mv.any() else (None,) * 7
        if c is not None:                                    # vạch ngang chia đốt
            for s_ in np.linspace(0.12, 0.88, 7):
                p = c + u * (t0 + (t1 - t0) * s_)
                q0, q1 = p + n * w0, p + n * w1
                tmp = np.zeros(m.shape, np.uint8)
                cv2.line(tmp, tuple(q0.astype(int)), tuple(q1.astype(int)), 1, max(1, net // 2))
                im[(tmp > 0) & mv] = INK
    if kieu in ("giap_vai",):
        mg = tach(a, m, lambda h, s, v: (h > 150) & (h < 250) & (s > 0.3), z, 1.2)
        mg = cv2.erode(mg.astype(np.uint8), el(1.0 * z)).astype(bool)
        im[mg] = PAL[k2]
        im[vien(mg, max(1, net // 2)) & m] = INK
    if kieu == "o_ngoc":
        mi = cv2.erode(m.astype(np.uint8), el(7 * z)).astype(bool)
        im[mi] = PAL[k2]
        im[vien(mi, max(1, net // 2))] = INK
    if kieu == "ngoc":
        mi = cv2.erode(m.astype(np.uint8), el(5 * z)).astype(bool)
        im[m] = PAL[k2]
        im[mi] = PAL[k1]
        im[vien(mi, max(1, net // 2))] = INK
    if kieu == "giap_chan":                                  # ba vòng mắt trúc vàng ngang ống chân
        c, u, t0, t1, n, w0, w1 = truc_dai(m)
        L = t1 - t0
        for s_ in (0.2, 0.5, 0.8):
            p = c + u * (t0 + L * s_)
            tmp = np.zeros(m.shape, np.uint8)
            cv2.line(tmp, tuple((p + n * (w0 - 9)).astype(int)), tuple((p + n * (w1 + 9)).astype(int)), 1, max(3, int(L * 0.075)))
            b = (tmp > 0) & m
            im[b] = PAL[k2]
            im[vien(b, max(1, net // 2)) & m] = INK
    if kieu == "day":                                        # nụ đỏ: chỗ ảnh gốc là cam
        mg = tach(a, m, lambda h, s, v: ((h < 40) | (h > 340)) & (s > 0.4), z, 1.5)
        im[mg] = PAL[k2]
        im[vien(mg, max(1, net // 2)) & m] = INK
    if kieu in ("la", "dai", "tai") and not nho:             # sống lá
        c, u, t0, t1, n, w0, w1 = truc_dai(cv2.erode(m.astype(np.uint8), el(2 * z)).astype(bool) if m.sum() > 900 * z * z else m)
        L = t1 - t0
        if L > 3.0 * (w1 - w0) * 0.5 or kieu == "la":
            q0, q1 = c + u * (t0 + L * 0.1), c + u * (t0 + L * 0.9)
            tmp = np.zeros(m.shape, np.uint8)
            cv2.line(tmp, tuple(q0.astype(int)), tuple(q1.astype(int)), 1, max(1, int(round(1.2 * z))), cv2.LINE_AA)
            im[(tmp > 0) & cv2.erode(m.astype(np.uint8), el(net)).astype(bool)] = INK
    im[vien(m, net)] = INK
    return im, m


def o_sung(ten, z=Z):
    """ô của một sừng măng (thiết kế của mình, không theo hình bóng sừng lửa của con gốc): sừng dựng đứng, gốc ở đáy ô, cong sang
    trái; thân xếp năm bẹ măng mực than viền vàng, phần ba ngọn vàng. Trả (RGB, mặt nạ, gốc (px), ngọn (px)) theo ô × z."""
    _, dai, rong, cong = next(g for g in SUNG if g[0] == ten)
    le = 14
    Wc_, Hc_ = int((rong + cong + 2 * le) * z), int((dai + 2 * le) * z)
    goc = np.array([(le + cong + rong / 2) * z, (le + dai) * z])
    S_ = np.linspace(0, 1, 41)
    tam = np.stack([goc[0] - cong * z * S_ ** 1.7, goc[1] - dai * z * S_], 1)
    d = np.gradient(tam, axis=0)
    n = np.stack([-d[:, 1], d[:, 0]], 1) / np.hypot(*d.T)[:, None]
    w = rong * z / 2 * (1 - S_) ** 0.8
    tr, ph = tam + n * w[:, None], tam - n * w[:, None]
    m = np.zeros((Hc_, Wc_), np.uint8)
    cv2.fillPoly(m, [np.round(np.r_[tr, ph[::-1]]).astype(np.int32)], 255, cv2.LINE_AA)
    m = cv2.GaussianBlur(m, (0, 0), 1.2 * z) > 127
    im = np.full((Hc_, Wc_, 3), 255, np.uint8)
    im[m] = PAL["than"]
    net = int(3 * z)
    for s0 in (0.0, 0.16, 0.32, 0.47, 0.6):                   # viền vàng hình chữ V ngược của từng bẹ (mũi bẹ chĩa lên ngọn)
        i0 = int(s0 * 40) + 5
        i1 = min(40, i0 + 5)
        v_ = np.zeros((Hc_, Wc_), np.uint8)
        cv2.polylines(v_, [np.round(np.array([tr[i0 - 5], tam[i1], ph[i0 - 5]])).astype(np.int32)], False, 255, int(9 * z), cv2.LINE_AA)
        b = (v_ > 127) & m
        im[b] = PAL["nga"]
        im[vien(b, max(1, net // 2)) & m] = INK
    ngon = np.zeros((Hc_, Wc_), np.uint8)
    i0 = int(0.7 * 40)
    cv2.fillPoly(ngon, [np.round(np.r_[tr[i0:], ph[i0:][::-1]]).astype(np.int32)], 255)
    ngon = (ngon > 127) & m
    im[ngon] = PAL["nga"]
    im[vien(ngon, max(1, net // 2)) & m] = INK
    im[vien(m, net)] = INK
    # ô nằm NGANG (sừng dài hơn chiều cao tờ): quay 90 độ theo chiều kim, gốc sừng bên trái, ngọn bên phải
    quay = lambda p: np.array([Hc_ - 1 - p[1], p[0]])  # noqa: E731
    return np.ascontiguousarray(np.rot90(im, -1)), np.ascontiguousarray(np.rot90(m, -1)), quay(goc), quay(tam[-1])


def ds_o():
    """các ô của tờ mảnh, theo NHÓM để mỗi tờ một loại: [(tên nhóm tờ, [(tên part, RGB, mặt nạ, z)])]."""
    _, _, atts = nap_goc()
    nhom = [("canh_tren_gan", "chibang_h_r"), ("canh_tren_xa", "chibang_h_l"), ("canh_duoi_gan", "chibang_q_r"), ("canh_duoi_xa", "chibang_q_l"),
            ("duoi", "weiba"), ("dau", "tou"), ("than_chan", None)]
    out = []
    da = set()
    for ten_to, tien_to in nhom:
        cells = []
        for a in atts:
            t = a["att"]
            g = nhom_cua(t)
            if t in da or g in BO_NHOM or not a["cur"]:
                continue
            if tien_to is None or g.startswith(tien_to):
                im, m = thiet_ke(t)
                cells.append((t, im, m, z_cua(t)))
                da.add(t)
        if ten_to == "dau":
            for g_ in SUNG:
                im, m, _, _ = o_sung(g_[0])
                cells.append((g_[0], im, m, Z))
        out.append((ten_to, cells))
    return out


def nhom_part():
    """tờ hướng dẫn theo khung part → mau/part_Q<k>.png + part_Q<k>.json (ô của từng part) + part_Q.json (tờ nào thuộc nhóm nào)."""
    os.makedirs(MAU, exist_ok=True)
    for f in os.listdir(MAU):
        if f.startswith("part_Q"):
            os.remove(os.path.join(MAU, f))
    k = 0
    muc = {}
    for ten_to, cells in ds_o():
        cells = sorted(cells, key=lambda c: -c[2].shape[0])
        sheets, cur, x, y, hh = [], [], 36, 36, 0
        for c in cells:
            h, w = c[2].shape
            if x + w + 36 > W:
                x, y, hh = 36, y + hh + 44, 0
            if y + h + 36 > H:
                sheets.append(cur)
                cur, x, y, hh = [], 36, 36, 0
            cur.append((c, x, y))
            x += w + 44
            hh = max(hh, h)
        if cur:
            sheets.append(cur)
        for sh in sheets:
            k += 1
            im = np.full((H, W, 3), 255, np.uint8)
            khung = {}
            for (ten, cim, m, z), x, y in sh:
                h, w = m.shape
                im[y:y + h, x:x + w] = cim
                khung[ten] = {"x": x, "y": y, "w": w, "h": h, "z": z, "goc": ten, "kieu": "sung" if ten.startswith("sung_") else vai_cua(ten)[0]}
            Image.fromarray(im).save(os.path.join(MAU, f"part_Q{k}.png"))
            json.dump(khung, open(os.path.join(MAU, f"part_Q{k}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            muc[f"Q{k}"] = {"nhom": ten_to, "so": len(khung)}
            print(f"Q{k} ({ten_to}): {len(khung)} part")
    json.dump(muc, open(os.path.join(MAU, "part_Q.json"), "w", encoding="utf-8"), indent=1)
    print(k, "tờ")


def cat_part(to):
    """cắt tờ N_<tờ> Codex vẽ: mỗi part lấy đúng Ô của nó, tách nền trắng, cắt sát hình bóng, chỗ vẽ hụt lấy màu tờ hướng dẫn, kẻ nét
    mực dọc phía trong mép lưới → manh/part/<tên>.png cỡ ảnh vùng × Z. Đo IoU, ghi manh/part/_iou.json; chỉ ghi đè khi bản mới khít hơn."""
    from quai import anh
    path = anh.to_moi_nhat(TAI, f"N_{to}")
    if not path:
        print(to, "chưa có ảnh")
        return
    khung = json.load(open(os.path.join(MAU, f"part_{to}.json"), encoding="utf-8"))
    im = Image.open(path).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
        path = os.path.join(MAU, f"_N_{to}_doi_co.png")
        im.save(path)
    tt = anh.doc_to(path, dien_tich_min=120, gop_px=8)
    gd = np.asarray(Image.open(os.path.join(MAU, f"part_{to}.png")).convert("RGB"))
    ra = os.path.join(MANH, "part")
    os.makedirs(ra, exist_ok=True)
    _, by, _ = nap_goc()
    pso = os.path.join(ra, "_iou.json")
    SO = json.load(open(pso, encoding="utf-8")) if os.path.exists(pso) else {}
    kem = []
    for ten, kv in khung.items():
        x, y, w, h, z = kv["x"], kv["y"], kv["w"], kv["h"], kv["z"]
        g = gd[y:y + h, x:x + w].min(axis=2) < 236                       # hình bóng trên tờ hướng dẫn
        cell = tt.rgba[y:y + h, x:x + w].copy()
        lab = tt.lab[y:y + h, x:x + w]
        ids = [i for m_ in tt.manh for i in m_["ids"]]
        giu = np.zeros(lab.shape, bool)
        for i in set(lab[g].ravel().tolist()) - {0}:
            if i in ids:
                giu |= lab == i
        cell[..., 3] = (cell[..., 3] * anh.gian(giu, 2)).astype(np.uint8)
        a = cell[..., 3] > 127
        iou = (a & g).sum() / max(1, (a | g).sum())
        sat = cv2.dilate(g.astype(np.uint8), el(1.5 * z)).astype(bool)
        cell[..., 3][~sat] = 0
        a &= sat
        cu = SO.get(ten, [0, ""])
        if cu[1] != to and cu[0] >= iou:
            continue
        ho = g & ~a
        if ho.any():                                                     # chỗ vẽ hụt lấy màu tô gần nhất của tờ hướng dẫn
            gc = gd[y:y + h, x:x + w]
            to_ = cv2.erode(g.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & (gc.max(axis=2) > 105) & (gc.min(axis=2) < 236)
            if to_.any():
                _, lb = cv2.distanceTransformWithLabels((~to_).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
                tra = np.zeros((int(lb.max()) + 1, 3), np.uint8)
                tra[lb[to_]] = gc[to_]
                cell[ho, :3] = tra[lb][ho]
                cell[ho, 3] = 255
        if kv["goc"] in by:                                              # nét mực dọc phía trong mép lưới (lưới ôm sát hình bóng)
            at = by[kv["goc"]]
            hull = np.array(at["uv"], float).reshape(-1, 2)[:at["hull"]] * np.array([w, h])
            hm = np.zeros(a.shape, np.uint8)
            cv2.fillPoly(hm, [np.round(hull).astype(np.int32)], 1)
            dai = hm.astype(bool) & ~cv2.erode(hm, el(2.2 * z), borderValue=0).astype(bool)
            cell[dai & (cell[..., 3] > 127), :3] = INK
        SO[ten] = [round(float(iou), 3), to]
        if iou < 0.9:
            kem.append((ten, round(float(iou), 2)))
        out = Image.fromarray(cell, "RGBA")
        if z != Z:
            out = out.convert("RGBa").resize((max(2, w * Z // z), max(2, h * Z // z)), Image.LANCZOS).convert("RGBA")
        out.save(os.path.join(ra, ten + ".png"))
    json.dump(SO, open(pso, "w", encoding="utf-8"), indent=1)
    ious = [SO[t][0] for t in khung if t in SO]
    print(f"{to}: {len(khung)} part, IoU thấp nhất {min(ious):.2f}, trung vị {float(np.median(ious)):.2f}; dưới 0,9: {kem}")


def so_part(chi=None):
    """tờ so từng part đã cắt với hình bóng hướng dẫn: ĐỎ = hình bóng mà mảnh không phủ, XANH = vẽ thừa → mau/so_part_<tờ>.jpg."""
    for f in sorted(os.listdir(MAU)):
        if not (f.startswith("part_Q") and f.endswith(".json")) or f == "part_Q.json":
            continue
        to = f[5:-5]
        if chi and to not in chi:
            continue
        K_ = json.load(open(os.path.join(MAU, f), encoding="utf-8"))
        gd = np.asarray(Image.open(os.path.join(MAU, f"part_{to}.png")).convert("RGB"))
        S = np.full((H, W, 3), 150, np.uint8)
        co = False
        for ten, v in K_.items():
            pm = os.path.join(MANH, "part", ten + ".png")
            if not os.path.exists(pm):
                continue
            co = True
            x, y, w, h = v["x"], v["y"], v["w"], v["h"]
            g = gd[y:y + h, x:x + w].min(axis=2) < 236
            c = np.asarray(Image.open(pm).convert("RGBA").resize((w, h)))
            a_ = c[..., 3] > 127
            im = np.full((h, w, 3), 150, np.uint8)
            im[a_] = c[..., :3][a_]
            im[g & ~a_] = (255, 0, 0)
            S[y:y + h, x:x + w] = im
        if co:
            Image.fromarray(S).save(os.path.join(MAU, f"so_part_{to}.jpg"), quality=88)
            print(os.path.join(MAU, f"so_part_{to}.jpg"))


def can_mau(chi=None):
    """cân màu các mảnh Codex vẽ về đúng bảng màu của mình (mỗi tờ gen ra một sắc hơi khác, lá cùng tầng lệch nhau): với mỗi mảnh, từng
    vùng màu của thiết kế (màu chính, màu phụ) lấy trung vị màu tô (bỏ nét mực) rồi cộng độ lệch tới màu chuẩn; vân sáp giữ nguyên.
    manh/part/<tên>.png → manh/part_cb/<tên>.png (rig ưu tiên dùng)."""
    ra = os.path.join(MANH, "part_cb")
    os.makedirs(ra, exist_ok=True)
    src = os.path.join(MANH, "part")
    C = dict(PAL, **MAU_DAU)
    n = 0
    lech = []
    for f in sorted(os.listdir(src)):
        if not f.endswith(".png"):
            continue
        ten = f[:-4]
        if chi and ten not in chi:
            continue
        im = np.asarray(Image.open(os.path.join(src, f)).convert("RGBA")).copy()
        if ten.startswith("sung_"):
            gd, m, _, _ = o_sung(ten)
        else:
            gd, m = thiet_ke(ten, Z)
        if gd.shape[:2] != im.shape[:2]:
            gd = cv2.resize(gd, (im.shape[1], im.shape[0]), interpolation=cv2.INTER_NEAREST)
        rgb = im[..., :3].astype(np.float32)
        co = im[..., 3] > 200
        muc = rgb.max(axis=2) < 96                                       # nét mực (nâu sẫm): không đụng
        for k, mau in C.items():
            vung = (np.abs(gd.astype(np.int32) - np.array(mau)).sum(axis=2) < 12) & co & ~muc
            if vung.sum() < 60:
                continue
            loi = cv2.erode(vung.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
            if loi.sum() < 40:
                loi = vung
            tv = np.median(rgb[loi], axis=0)
            d = np.array(mau, np.float32) - tv
            if np.abs(tv - np.array(mau)).sum() > 190:                   # Codex vẽ thứ khác hẳn ở vùng này (chi tiết thêm): không kéo
                continue
            # vùng áp: mọi điểm gần màu trung vị đo được (kể cả chỗ viền vùng thiết kế lệch vài px)
            gan = (np.abs(rgb - tv).sum(axis=2) < 110) & co & ~muc & cv2.dilate(vung.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool)
            rgb[gan] = np.clip(rgb[gan] + d, 0, 255)
            lech.append(float(np.abs(d).max()))
        im[..., :3] = rgb.astype(np.uint8)
        Image.fromarray(im, "RGBA").save(os.path.join(ra, f))
        n += 1
    print(f"cân màu {n} mảnh → {ra}; độ lệch kênh lớn nhất: trung vị {np.median(lech) if lech else 0:.0f}, tối đa {max(lech) if lech else 0:.0f}")


def anh_part(ten):
    """ảnh của một part cho rig, cỡ ảnh vùng × Z: bản đã cân màu (manh/part_cb) hoặc bản Codex vẽ (manh/part) nếu đã có, không thì DA
    TẠM = thiết kế phẳng."""
    for thu_muc in ("part_cb", "part"):
        p = os.path.join(MANH, thu_muc, ten + ".png")
        if os.path.exists(p):
            return Image.open(p).convert("RGBA"), False
    p = os.path.join(MANH, "part", ten + ".png")
    if os.path.exists(p):
        return Image.open(p).convert("RGBA"), False
    if ten.startswith("sung_"):
        im, m, _, _ = o_sung(ten)
        return Image.fromarray(np.dstack([im, m.astype(np.uint8) * 255]), "RGBA"), True
    im, m = thiet_ke(ten, Z)
    return Image.fromarray(np.dstack([im, m.astype(np.uint8) * 255]), "RGBA"), True


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["bo_cuc"]:
        for k in (a[1:] or list(HUONG)):
            bo_cuc(k)
    elif a[:1] == ["nhom_part"]:
        nhom_part()
    elif a[:1] == ["cat_part"]:
        for t in a[1:]:
            cat_part(t)
    elif a[:1] == ["so_part"]:
        so_part(a[1:] or None)
    elif a[:1] == ["can_mau"]:
        can_mau(a[1:] or None)
    else:
        print(__doc__)
