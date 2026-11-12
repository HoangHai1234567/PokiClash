# -*- coding: utf-8 -*-
"""Chim bảo hộ rừng cánh lá (mã làm việc chim_la; con gốc của rig: monster_3630, game tham khảo). Tướng thứ 6 đảo Mộc.

Người dùng 2026-11-12: "concept Chim bảo hộ rừng, reskin lại phần cánh thành lá cây, đuôi vẫn có thể để là đá, làm khác con gốc đi".
Con gốc nhìn sang PHẢI (đầu nghiêng, lộ một mắt): không lật. Rig gốc: 239 xương, 169 slot (138 hình bật), FK thuần, 11 clip.

    chim_la.py part_goc          ảnh từng part của con gốc cắt theo lưới → <SXS>/scan/monster_3630/parts/ + tờ tổng theo nhóm (nội bộ)
    chim_la.py bo_cuc [hướng]    sơ đồ bố cục phẳng 1536 × 1024 → inbox/chim_la_1/mau/bo_cuc_<hướng>.png
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

CODE = "chim_la"
MON = "monster_3630"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
W, H = 1536, 1024
INK = (43, 33, 24)
ATT = os.environ.get("CL_ATT", "att_goc.json")      # bố cục concept dùng dáng xoè cánh: CL_ATT=att_idle0.json
S2 = 2
FONT = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)


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
        het = sorted([a for a in D["atts"] if a.get("region") in imgs], key=lambda a: a["order"])
        _C.update(atlas=atlas, imgs=imgs, atts=atts, het=het, bones=D["bones"])
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


def nhom(slot):
    """nhóm bộ phận của một slot con gốc (tên slot)."""
    s = slot.replace("P_", "")
    for k, v in (("chibangR1", "canh_gan_ngoai"), ("chibangR2", "canh_gan_trong"), ("chibangR3", "canh_gan_lat"),
                 ("chiabangL", "canh_xa"), ("weiba5", "duoi_long"), ("weiba", "duoi_da"), ("toushi", "mao"),
                 ("xiongjia", "giap_nguc"), ("jiaozh", "ban_chan"), ("xiaotui", "ong_chan"), ("datui", "dui"),
                 ("tou", "dau"), ("yanjing", "mat"), ("zui", "mo"), ("shetou", "luoi"), ("mao", "long"),
                 ("xiong", "than"), ("xiashen", "than")):
        if s.startswith(k):
            return v
    return "khac"


def xuat_part_goc():
    """từng part ra file riêng + tờ tổng theo nhóm (phóng 3, ghi thứ tự vẽ, slot, cỡ, số xương)."""
    _, imgs, _ = nap()
    ra = os.path.join(scan(), "parts")
    os.makedirs(ra, exist_ok=True)
    info = json.load(open(os.path.join(scan(), "info.json"), encoding="utf-8"))
    nb = {a["name"] + "@" + info["slots"][a["slot"]]["name"]: (a["verts"], a["nbones"]) for a in info["skins"][0]["atts"]}
    G = {}
    for a in _C["het"]:
        im = part_goc(a)
        im.save(os.path.join(ra, f"{a['order']:03d}_{a['slot']}.png"))
        G.setdefault(nhom(a["slot"]), []).append((a, im))
    z = 3
    for g, L in G.items():
        Wt = 2200
        x = y = 16
        hh = 0
        cho = []
        for a, im in L:
            w, h = im.width * z, im.height * z
            if x + max(w, 170) + 16 > Wt:
                x, y, hh = 16, y + hh + 44, 0
            cho.append((a, im, x, y))
            x += max(w, 170) + 22
            hh = max(hh, h)
        out = Image.new("RGB", (Wt, y + hh + 50), (120, 125, 140))
        d = ImageDraw.Draw(out)
        for a, im, x, y in cho:
            big = im.resize((im.width * z, im.height * z), Image.LANCZOS)
            out.paste(big, (x, y + 34), big)
            v = nb.get(a["att"] + "@" + a["slot"], ("?", "?"))
            d.text((x, y), f"{a['order']} {a['slot'].replace('P_', '')}{'' if a['cur'] else ' (tắt)'}", fill=(255, 255, 255), font=FONT)
            d.text((x, y + 16), f"{im.width}x{im.height} {v[0]}đ {v[1]}x", fill=(230, 230, 160), font=FONT)
        p = os.path.join(scan(), f"parts_{g}.png")
        out.save(p)
        print(p, out.size, len(L), "part")
# ================================================================ SƠ ĐỒ BỐ CỤC (thiết kế của mình, tô phẳng theo nhóm)
def loai(ten):
    """nhóm thiết kế của một part (tên hình con gốc, bỏ 'P_')."""
    s = ten.replace("P_", "")
    if s.startswith(("chibangR1_", "chibangR2_", "chiabangL_", "chibangR3_")):
        k, so = s.split("_")
        so = int(so)
        if (k, so) in (("chibangR1", 15), ("chibangR1", 16), ("chibangR2", 14), ("chibangR2", 9), ("chiabangL", 21), ("chiabangL", 23),
                       ("chibangR3", 14), ("chibangR3", 15)):
            return "tan"                         # mảng lông phủ → tán lá nhỏ xếp lớp
        if (k, so) in (("chibangR1", 14), ("chiabangL", 22)):
            return "choi"                        # túm lửa ở cổ tay cánh → chồi lá non
        if (k in ("chibangR1", "chibangR2", "chibangR3") and so <= 2) or (k == "chiabangL" and so <= 5 and s != "chiabangL_010"
                                                                          and s != "chiabangL_011"):
            return "canh"                        # dải đá hoa văn → cành cây (xương cánh)
        return "la"                              # từng lông pha lê → từng chiếc lá
    if s.startswith("toushi"):
        return "mao"
    if s.startswith("xiongjia"):
        return "la_co" if s[-2:] in ("05", "06", "07") else "bua"
    if s.startswith("jiaozhi") and (s.endswith("_03") or s == "jiaozhiR4_02"):
        return "vuot"
    if s.startswith(("jiaozh", "xiaotui")):
        return "chan"
    if s.startswith("datui"):
        return "dui"
    if s.startswith("weiba5"):
        return "duoi"
    if s.startswith("weiba"):
        return "da_to" if s in ("weiba1_06", "weiba2_04", "weiba3_04", "weiba4_05") else ("da_ngon" if s.endswith("_01") else "da")
    if s.startswith("tou"):
        return "dau"
    if s.startswith("zui"):
        return "mo"
    if s.startswith("yanjing"):
        return "mat"
    if s.startswith("shetou"):
        return "luoi"
    return "long"                                # xiong, xiashen, mao_01, mao_02


def khung_T():
    """(hàm đổi toạ độ rig → pixel khung concept, tỉ lệ)."""
    _, _, atts = nap()
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    sc = min(1240 / (x1 - x0), 950 / (y1 - y0))
    ox = W / 2 - (x0 + x1) / 2 * sc
    oy = (H + (y1 - y0) * sc) / 2 + y0 * sc
    return (lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * sc, oy - np.asarray(p, float)[..., 1] * sc], -1)), sc


def bong_khung(a, T, tron=5.0):
    """hình bóng KÍN của một part đặt đúng chỗ dáng gốc trên khung concept (phóng S2), làm trơn: chỉ còn khối."""
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


THO = dict(la=(110, 180, 80), tan=(60, 130, 70), choi=(170, 210, 100), canh=(120, 80, 50), mao=(255, 60, 200), la_co=(150, 200, 90),
           bua=(120, 120, 110), vuot=(60, 50, 45), chan=(220, 165, 65), dui=(120, 85, 55), duoi=(140, 95, 60), da_to=(150, 150, 140),
           da=(110, 108, 100), da_ngon=(170, 168, 150), dau=(100, 70, 45), mo=(235, 170, 60), mat=(255, 255, 255), luoi=(200, 80, 80),
           long=(180, 140, 90))


def tho():
    """bản thô để ĐỌC TOẠ ĐỘ: mọi part tô theo nhóm, mào tô hồng; kèm lưới 100 px."""
    _, _, atts = nap()
    T, sc = khung_T()
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop = {}
    for a in atts:
        nh = loai(a["att"])
        m = bong_khung(a, T, 2.5)
        if not m.any():
            continue
        can[m] = THO[nh]
        can[vien(m, 3)] = INK
        ys, xs = np.nonzero(m)
        hop[a["slot"]] = [int(xs.min() / S2), int(ys.min() / S2), int(xs.max() / S2), int(ys.max() / S2)]
    out = Image.fromarray(can).resize((W, H), Image.LANCZOS)
    os.makedirs(MAU, exist_ok=True)
    json.dump(dict(hop=hop, sc=sc), open(os.path.join(MAU, "tho_hop.json"), "w"), indent=0)
    g = out.copy()
    d = ImageDraw.Draw(g)
    for x in range(0, W, 50):
        d.line([(x, 0), (x, H)], fill=(255, 0, 0) if x % 100 == 0 else (255, 190, 190), width=1)
        if x % 100 == 0:
            d.text((x + 2, 2), str(x), fill=(200, 0, 0), font=FONT)
    for y in range(0, H, 50):
        d.line([(0, y), (W, y)], fill=(255, 0, 0) if y % 100 == 0 else (255, 190, 190), width=1)
        if y % 100 == 0:
            d.text((2, y + 2), str(y), fill=(200, 0, 0), font=FONT)
    out.save(os.path.join(MAU, "_tho.png"))
    g.save(os.path.join(MAU, "_tho_luoi.png"))
    print(os.path.join(MAU, "_tho_luoi.png"), "tỉ lệ", round(sc, 4))
    B = {b["name"]: b for b in _C["bones"]}
    for n in ("bone8", "bone115", "bone41", "bone42", "bone5", "bone3", "bone123", "bone178", "bone92", "bone104", "bone99", "bone96", "bone110"):
        if n in B:
            print(n, {k: (round(v, 1) if isinstance(v, float) else v) for k, v in B[n].items() if k in ("x", "y", "wx", "wy", "a", "b", "c", "d")})


# ---------------------------------------------------------------- bảng màu ĐỀ XUẤT của Claude (người dùng chưa dặn màu), chờ duyệt
def _h(x):
    return tuple(int(x[i:i + 2], 16) for i in (1, 3, 5))


PALS = {
    # A: đại bàng rừng nâu vỏ cây, ngực kem, cánh lá lục; mào QUẠT LÁ
    "nau": dict(long=_h("#9A6B42"), long_dam=_h("#5E4028"), bung=_h("#F1E3BC"), dau=_h("#5E4028"), ma=_h("#F1E3BC"),
                la=_h("#5FA646"), la_nhat=_h("#9CCB58"), gan=_h("#2F6B34"), tan=_h("#3B7F43"), choi=_h("#C4DE6E"), canh=_h("#7A5232"),
                la_co=_h("#9CCB58"), da=_h("#8C8A7E"), da_dam=_h("#5C5A52"), reu=_h("#6FAE4B"), mo=_h("#EDAE3C"), chan=_h("#D9A23E"),
                vuot=_h("#3A322C"), mat=_h("#F4C23C"), ngoc=_h("#F2B43E"), hoa=None, mao="quat"),
    # B: chim ngọc lam ngực đỏ (kiểu chim quetzal, linh điểu rừng mưa), lá vàng chanh; mào hai TÀU DƯƠNG XỈ dài
    "ngoc": dict(long=_h("#1F8C7C"), long_dam=_h("#135E58"), bung=_h("#C9463A"), dau=_h("#135E58"), ma=_h("#1F8C7C"),
                 la=_h("#6DBB4A"), la_nhat=_h("#C2E062"), gan=_h("#2C7A3C"), tan=_h("#3E9A4E"), choi=_h("#E2EC84"), canh=_h("#5A3F2C"),
                 la_co=_h("#C2E062"), da=_h("#6A6C72"), da_dam=_h("#44464C"), reu=_h("#7DBB52"), mo=_h("#F2C83E"), chan=_h("#55504C"),
                 vuot=_h("#F1E3BC"), mat=_h("#F4D03C"), ngoc=_h("#C9463A"), hoa=None, mao="duong_xi"),
    # C: linh điểu trắng, mũ lông lục xám, cành cánh nở hoa hồng; mào QUẠT LÁ
    "bach": dict(long=_h("#F4EFDC"), long_dam=_h("#7E9E7A"), bung=_h("#F4EFDC"), dau=_h("#7E9E7A"), ma=_h("#F4EFDC"),
                 la=_h("#4C9A52"), la_nhat=_h("#93C663"), gan=_h("#2A6A3A"), tan=_h("#2F7646"), choi=_h("#93C663"), canh=_h("#7A5638"),
                 la_co=_h("#93C663"), da=_h("#9A968A"), da_dam=_h("#66625A"), reu=_h("#6FAE4B"), mo=_h("#EE8A3E"), chan=_h("#EE8A3E"),
                 vuot=_h("#4A3A30"), mat=_h("#EE8A3E"), ngoc=_h("#EE86A6"), hoa=_h("#F2A6BC"), mao="quat"),
}

# ĐẦU của mình trên khung concept (px, dáng xoè cánh idle 0 s): đầu nhìn sang phải, lộ một mắt như con gốc
MAT = (826, 333)
MA = [(803, 302), (848, 306), (866, 330), (860, 352), (838, 354), (822, 368), (792, 386), (762, 372), (772, 346), (792, 330)]   # mảng mặt sáng
# mào QUẠT LÁ: (gốc, ngọn, nửa bề rộng, độ cong); lá xếp như quạt ngả về sau (trái)
QUAT = [((752, 300), (596, 262), 26, -0.10), ((770, 298), (618, 176), 30, -0.08), ((790, 296), (690, 92), 34, -0.10),
        ((812, 296), (790, 118), 28, 0.06), ((832, 300), (862, 206), 18, 0.10)]
# mào DƯƠNG XỈ: hai tàu dài (gốc, điểm uốn, ngọn) + ba lá ngắn sau gáy
XI = [((792, 296), (668, 236), (668, 98)), ((832, 298), (792, 222), (756, 132))]
XI_LA = [((752, 300), (640, 250), 20, -0.1), ((770, 298), (690, 214), 18, -0.1), ((738, 304), (628, 292), 16, -0.05)]
VONG = [(728, 300), (760, 292), (800, 290), (840, 296), (852, 304), (842, 312), (800, 304), (760, 306), (732, 312)]     # vòng gỗ gốc mào


def _bez(p0, p1, p2, n=40):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0, float) + 2 * (1 - t) * t * np.array(p1, float) + t ** 2 * np.array(p2, float)


def la_hinh(goc, ngon, w, cong, n=36):
    """đa giác một chiếc lá nhọn hai đầu cong nhẹ; trả (đa giác, gân giữa)."""
    g, t_ = np.array(goc, float), np.array(ngon, float)
    d = t_ - g
    nrm = np.array([-d[1], d[0]])
    mid = (g + t_) / 2 + nrm * cong
    c = _bez(g, mid, t_, n)
    tt = np.linspace(0, 1, n)
    hw = w * np.sin(np.pi * np.clip(tt * 0.93 + 0.07, 0, 1)) ** 0.75
    tg = np.gradient(c, axis=0)
    tg /= np.linalg.norm(tg, axis=1, keepdims=True) + 1e-9
    nn = np.stack([-tg[:, 1], tg[:, 0]], 1)
    return np.concatenate([c + nn * hw[:, None], (c - nn * hw[:, None])[::-1]]), c


def ve_la(can, goc, ngon, w, cong, mau, gan, net=6):
    P, c = la_hinh(goc, ngon, w, cong)
    cv2.fillPoly(can, [np.int32(P * S2)], mau, cv2.LINE_AA)
    cv2.polylines(can, [np.int32(P * S2)], True, INK, net * S2 // 2 + 3, cv2.LINE_AA)
    cv2.polylines(can, [np.int32(c[3:-4] * S2)], False, gan, 5, cv2.LINE_AA)


def ve_mao(can, PAL):
    if PAL["mao"] == "quat":
        for i in (0, 4, 1, 3, 2):                                    # lá giữa to nhất vẽ sau cùng
            ve_la(can, *QUAT[i], PAL["la"] if i % 2 == 0 else PAL["la_nhat"], PAL["gan"])
        return
    for la in XI_LA:
        ve_la(can, *la, PAL["la"], PAL["gan"])
    for (p0, p1, p2) in XI:
        c = _bez(p0, p1, p2, 60)
        L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(c, axis=0), axis=1))])
        tg = np.gradient(c, axis=0)
        tg /= np.linalg.norm(tg, axis=1, keepdims=True) + 1e-9
        k = 0
        for s_ in np.arange(34, L[-1] - 6, 24):
            j = int(np.searchsorted(L, s_))
            f = 1 - s_ / L[-1]
            dai = 16 + 36 * f ** 0.8
            for sg in (1, -1):
                a = np.deg2rad(52 * sg)
                v = np.array([tg[j, 0] * np.cos(a) - tg[j, 1] * np.sin(a), tg[j, 0] * np.sin(a) + tg[j, 1] * np.cos(a)])
                ve_la(can, tuple(c[j]), tuple(c[j] + v * dai), 4 + 6 * f, 0.08 * sg, PAL["la_nhat"] if k % 2 else PAL["la"], PAL["gan"], net=4)
            k += 1
        cv2.polylines(can, [np.int32(c * S2)], False, INK, 16, cv2.LINE_AA)
        cv2.polylines(can, [np.int32(c * S2)], False, PAL["canh"], 8, cv2.LINE_AA)


def truc(m):
    """hai đầu trục dài của một mặt nạ (PCA)."""
    ys, xs = np.nonzero(m)
    P = np.stack([xs, ys], 1).astype(float)
    c = P.mean(0)
    u = np.linalg.svd(P - c, full_matrices=False)[2][0]
    t = (P - c) @ u
    return c + u * np.percentile(t, 4), c + u * np.percentile(t, 96)


def bo_cuc(kieu="nau", luu=True):
    """sơ đồ bố cục: khối từng mảnh của rig đặt đúng chỗ (dáng xoè cánh idle 0 s), tô phẳng theo THIẾT KẾ MÌNH; mào vẽ mới."""
    global ATT
    ATT = "att_idle0.json"
    _C.clear()
    PAL = PALS[kieu]
    _, _, atts = nap()
    T, sc = khung_T()
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    Y, X = np.mgrid[0:H * S2, 0:W * S2]
    hop = {}
    da_mao = False

    def hopn(ten, m):
        ys, xs = np.nonzero(m)
        b = [int(xs.min() / S2), int(ys.min() / S2), int(xs.max() / S2), int(ys.max() / S2)]
        if ten in hop:
            o = hop[ten]
            b = [min(o[0], b[0]), min(o[1], b[1]), max(o[2], b[2]), max(o[3], b[3])]
        hop[ten] = b

    for i, a in enumerate(atts):
        ten = a["att"].replace("P_", "")
        nh = loai(ten)
        if nh == "luoi":
            continue
        if nh == "mao":
            if not da_mao:                                           # mào của MÌNH, vẽ ở lượt của mảnh mào đầu tiên (sau đầu)
                ve_mao(can, PAL)
                da_mao = True
            if ten == "toushi_01":                                   # vòng gỗ ở gốc mào, trước đầu
                cv2.fillPoly(can, [np.int32(np.array(VONG) * S2)], PAL["canh"], cv2.LINE_AA)
                cv2.polylines(can, [np.int32(np.array(VONG) * S2)], True, INK, 9, cv2.LINE_AA)
            continue
        nho = nh in ("vuot", "chan", "da", "bua", "mo", "mat")
        m = bong_khung(a, T, 2.2 if nho else 3.6)
        if not m.any():
            continue
        ys, xs = np.nonzero(m)
        dai = max(xs.max() - xs.min(), ys.max() - ys.min()) / S2
        if nh == "la":
            can[m] = PAL["la"] if dai > 95 else PAL["la_nhat"]
        elif nh == "long":
            can[m] = PAL["long"]
            if ten == "xiong":                                       # yếm ngực: nửa phải của cổ – ngực
                can[m & (X > (706 + 0.10 * (Y / S2 - 350)) * S2)] = PAL["bung"]
            if ten == "xiashen":                                     # mảng rêu trên bụng (chỗ con gốc có mảng vảy)
                e = ((X / S2 - 655) / 40.0) ** 2 + ((Y / S2 - 506) / 28.0) ** 2 < 1
                can[m & e] = PAL["reu"]
        elif nh == "dau":
            can[m] = PAL["dau"]
            mk = np.zeros(m.shape, np.uint8)
            cv2.fillPoly(mk, [np.int32(np.array(MA) * S2)], 1)
            can[m & mk.astype(bool)] = PAL["ma"]
        elif nh == "duoi":
            can[m] = PAL["long_dam"] if ten in ("weiba5_01", "weiba5_04", "weiba5_06") else PAL["long"]
        elif nh == "dui":
            can[m] = PAL["long_dam"]
        elif nh == "da_to":                                          # tảng đá đầu chuỗi: chỏm rêu
            can[m] = PAL["da"]
            can[m & (Y < ys.min() + (ys.max() - ys.min()) * 0.42)] = PAL["reu"]
        elif nh == "da_ngon":                                        # viên cuối chuỗi: đá + chỏm rêu ở nửa ngoài
            can[m] = PAL["da"]
            can[m & (X > xs.min() + (xs.max() - xs.min()) * 0.55)] = PAL["reu"]
        elif nh == "da":
            can[m] = PAL["da_dam"]
        elif nh == "bua":
            can[m] = PAL["da"]
            if ten == "xiongjia_02":
                cx, cy = int((xs.min() + xs.max()) / 2), int((ys.min() + ys.max()) / 2)
                r = int((xs.max() - xs.min()) * 0.22)
                cv2.fillPoly(can, [np.array([(cx, cy - int(r * 1.5)), (cx + r, cy), (cx, cy + int(r * 1.5)), (cx - r, cy)], np.int32)],
                             PAL["ngoc"], cv2.LINE_AA)
        elif nh == "mat":
            pass
        else:
            can[m] = PAL[nh]
        if nh != "mat":
            can[vien(m, 3 if nho else 5)] = INK
        if nh == "la" and dai > 34:                                  # gân giữa của lá
            p0, p1 = truc(cv2.erode(m.astype(np.uint8), el(5)).astype(bool) if dai > 60 else m)
            q0, q1 = p0 + (p1 - p0) * 0.10, p0 + (p1 - p0) * 0.92
            cv2.line(can, (int(q0[0]), int(q0[1])), (int(q1[0]), int(q1[1])), PAL["gan"], 5, cv2.LINE_AA)
        if nh == "canh" and PAL["hoa"] is not None:                  # hướng C: vài bông hoa nhỏ trên cành cánh
            rng = np.random.default_rng(5 + i)
            tr = cv2.erode(m.astype(np.uint8), el(7)).astype(bool)
            yy, xx = np.nonzero(tr)
            for _ in range(2 if len(yy) else 0):
                j = int(rng.integers(len(yy)))
                for q in range(5):
                    g = q * 2 * np.pi / 5
                    cv2.circle(can, (int(xx[j] + 11 * np.cos(g)), int(yy[j] + 11 * np.sin(g))), 9, PAL["hoa"], -1, cv2.LINE_AA)
                cv2.circle(can, (int(xx[j]), int(yy[j])), 6, PAL["mat"], -1, cv2.LINE_AA)
        if nh == "mat":                                              # mắt: hạnh nhân xếch, con ngươi sẫm, nét mày
            cx, cy = MAT[0] * S2, MAT[1] * S2
            cv2.ellipse(can, (cx, cy), (24, 13), 18, 0, 360, PAL["mat"], -1, cv2.LINE_AA)
            cv2.ellipse(can, (cx, cy), (24, 13), 18, 0, 360, INK, 5, cv2.LINE_AA)
            cv2.circle(can, (cx + 3, cy + 1), 8, INK, -1, cv2.LINE_AA)
            cv2.line(can, (cx - 34, cy - 30), (cx + 30, cy - 4), INK, 9, cv2.LINE_AA)
            continue
        nhom_hop = nh
        if nh in ("la", "tan", "choi", "canh"):
            nhom_hop = "canh_xa" if "chiabangL" in ten else "canh_gan"
        if nh in ("da", "da_to", "da_ngon"):
            nhom_hop = "chuoi_" + ten.split("_")[0]
        if nh in ("chan", "vuot"):
            nhom_hop = "chan_xa" if "L" in ten.split("_")[0] else "chan_gan"
        hopn(nhom_hop, m)
        hopn(ten, m)
    out = Image.fromarray(can).resize((W, H), Image.LANCZOS)
    if luu:
        os.makedirs(MAU, exist_ok=True)
        out.save(os.path.join(MAU, f"bo_cuc_{kieu}.png"))
        json.dump(dict(hop=hop, sc=sc), open(os.path.join(MAU, "bo_cuc_hop.json"), "w"), indent=0)
        print(os.path.join(MAU, f"bo_cuc_{kieu}.png"), "tỉ lệ", round(sc, 4))
        for k, v in hop.items():
            if not any(ch.isdigit() for ch in k) or k.startswith("chuoi_"):
                print(f"  {k:14s} x {v[0]}-{v[2]}  y {v[1]}-{v[3]}")
    return out


def main(a):
    if a and a[0] == "part_goc":
        xuat_part_goc()
    elif a and a[0] == "tho":
        tho()
    elif a and a[0] == "bo_cuc":
        for k in (a[1:] or list(PALS)):
            bo_cuc(k)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
