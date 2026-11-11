# -*- coding: utf-8 -*-
"""tm04 Hà Bá (hà mã nước): rig dựng bằng mã từ các lớp cắt thẳng từ concept (tm04_cat.py) + mí mắt của tờ GPT M01.

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm04_cat.py 2 ; ... 1          (cắt lớp, cần cv2)
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm04.py      (dựng dạng 2 rồi dạng 1 + tiến hóa, xuất)
    py -3 -I ArtGen/Spine/tm04.py 2                                               (chỉ dạng 2)

Ra inbox/tm04_<k>/rig/: tm04_<k>.json/.atlas/.png/.atomik, tm04_<k>_game.json, xem.html, khung_*.png, luoi.png, ảnh cận,
so_concept.png, uon_thu.png, so_sanh.md, chan_dung.png.
"""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

from quai import anh, hoat, khung, luoi, mieng, soi, tienhoa, trongso, xuat  # noqa: E402
from quai.hoat import Clip, LoXo, an_hien, chuoi_song, cv, ease, lui, rung, song, bao  # noqa: E402
from quai.khung import Dat  # noqa: E402

CODE = "tm04"
TEN = {1: "Hà Mã Con", 2: "Hà Bá"}

# ---------------------------------------------------------------- toạ độ concept (L1_duyet.png 1536x1024) của từng dạng
PT = {
    2: {"than": (640, 640), "hong": (380, 560), "nguc": (880, 600), "co": (1000, 560), "dau": (1120, 520), "mui": (1380, 600),
        "mom": (1300, 600), "ban_le": (1010, 725), "ham_mui": (1400, 810), "mieng": (1345, 705), "vai": (770, 520),
        "mat_n": (1148, 522), "mat_x": (1287, 524), "hop_n": (1104, 486, 1190, 554), "hop_x": (1250, 492, 1320, 552), "mieng_tren": 650, "mieng_duoi": 785,
        "giot": [(240, 52), (146, 118), (86, 250)]},
    1: {"than": (660, 560), "hong": (560, 560), "nguc": (760, 560), "co": (820, 540), "dau": (900, 520), "mui": (1120, 580),
        "mom": (1050, 580), "ban_le": (878, 676), "ham_mui": (1092, 702), "mieng": (1080, 650),
        "mat_n": (885, 500), "mat_x": (1040, 492), "hop_n": (858, 438, 957, 532), "hop_x": (1003, 436, 1067, 517), "mieng_tren": 612, "mieng_duoi": 700, "giot": []},
}
CHAINS = {  # tên: (cha, [khớp concept gốc → ngọn], cha_hoa)
    2: {"tai_n": ("dau", [(1002, 478), (975, 440), (948, 408)], 0.7),
        "tai_x": ("dau", [(1262, 445), (1288, 408), (1312, 378)], 0.7),
        "vay1": ("hong", [(510, 400), (480, 350), (440, 312), (405, 322)], 0.85),
        "vay2": ("than", [(650, 385), (620, 320), (570, 250), (525, 240)], 0.85),
        "vay3": ("nguc", [(820, 355), (790, 260), (740, 180), (695, 180)], 0.85),
        "vay4": ("nguc", [(1000, 345), (960, 230), (900, 120), (850, 85)], 0.85),
        "duoi": ("hong", [(300, 480), (220, 430), (150, 340), (150, 220), (230, 110), (340, 62)], 0.8)},
    1: {"tai_n": ("dau", [(825, 442), (812, 405), (800, 370)], 0.7),
        "tai_x": ("dau", [(1030, 428), (1040, 396), (1050, 365)], 0.7),
        "vay1": ("hong", [(650, 432), (630, 380), (600, 330)], 0.85),
        "vay2": ("than", [(790, 392), (790, 300), (780, 235)], 0.85),
        "vay3": ("nguc", [(930, 388), (935, 348), (945, 315)], 0.85),
        "duoi": ("hong", [(515, 588), (450, 560), (400, 505), (385, 440), (420, 390), (490, 375)], 0.8)},
}
LEGS = {  # lớp: (cha, [hông/vai, gối, gan bàn chân trên đất])
    2: {"chan_sn": ("hong", [(300, 600), (255, 765), (225, 940)]), "chan_sx": ("hong", [(470, 700), (482, 815), (495, 905)]),
        "chan_tn": ("nguc", [(745, 620), (772, 790), (805, 968)]), "chan_tx": ("nguc", [(1180, 760), (1232, 860), (1285, 945)])},
    1: {"chan_sn": ("hong", [(650, 690), (650, 738), (652, 786)]), "chan_sx": ("hong", [(556, 688), (556, 730), (556, 768)]),
        "chan_tn": ("nguc", [(932, 700), (934, 745), (935, 786)]), "chan_tx": ("nguc", [(816, 703), (816, 740), (817, 773)])},
}
REGIONS = {  # vùng thân (concept), ưu tiên trước → sau; phần còn lại là "than"
    2: [("dau", [(1000, 330), (1500, 330), (1500, 730), (1110, 730), (1040, 700), (990, 560)]),
        ("co", [(930, 380), (1010, 380), (1050, 600), (1060, 800), (900, 800), (890, 600)]),
        ("nguc", [(760, 330), (940, 330), (930, 830), (760, 830)]),
        ("hong", [(150, 330), (470, 330), (470, 830), (150, 830)])],
    1: [("dau", [(850, 330), (1200, 330), (1200, 740), (880, 740), (810, 640), (810, 480)]),
        ("co", [(770, 330), (850, 330), (850, 740), (770, 740)]),
        ("nguc", [(690, 330), (770, 330), (770, 740), (690, 740)]),
        ("hong", [(450, 330), (590, 330), (590, 760), (450, 760)])],
}


AN = {"chan_sx", "chan_tx", "mieng"}   # lớp gần như luôn khuất (chân xa, lòng miệng): lưới thưa hơn một chút (1,3 lần bước)


def base(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}")


def smooth(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- mí mắt từ tờ GPT M01
def lids(k):
    """(mí gần, mí xa) PIL; tờ M01 chưa có thì hình giữ chỗ."""
    d = os.path.join(base(k), "tai_ve")
    out = os.path.join(base(k), "manh")
    p = anh.to_moi_nhat(d, "M01")
    col = (64, 76, 134) if k == 2 else (122, 147, 190)
    if p:
        try:
            to = anh.doc_to(p)
            g = anh.gan_theo_o(to, [["mieng_gpt", "mi_n", "mi_x"], ["chan_tx_gpt", "chan_sx_gpt", None]])
            anh.luu_manh(to, g, out)
            anh.to_soi(out, list(g))
            return Image.open(os.path.join(out, "mi_n.png")).convert("RGBA"), Image.open(os.path.join(out, "mi_x.png")).convert("RGBA"), True
        except Exception as e:  # noqa: BLE001
            print("  cắt M01 lỗi:", e)
    sz = {2: ((110, 80), (80, 65)), 1: ((110, 105), (70, 85))}[k]
    return anh.gia("mi", *sz[0], col), anh.gia("mi", *sz[1], col), False


# ---------------------------------------------------------------- dựng một dạng
def dung(k, thua=1.0):
    cat = json.load(open(os.path.join(base(k), "manh", "cat.json"), encoding="utf-8"))
    ks, (xg, yg) = cat["ks"], cat["ground"]
    names = cat["parts"]

    def S(p):
        return np.array([(p[0] - xg) * ks, (yg - p[1]) * ks])

    lays = {l["name"]: l for l in cat["layers"]}
    top = min(l["box"][1] for l in cat["layers"] if not l["name"].startswith("giot"))
    H = (yg - top) * ks
    sk = khung.Sk(f"{CODE}_{k}")
    pt = PT[k]
    imgs, labs = {}, {}
    for n in lays:
        imgs[n] = Image.open(os.path.join(base(k), "manh", n + ".png")).convert("RGBA")
        labs[n] = np.array(Image.open(os.path.join(base(k), "manh", n + "_lab.png")))
        sk.anh(n, imgs[n])
    # ------------------------------------------------ xương
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("shadow", "move")
    sk.xuong("than", "move", *S(pt["than"]), dai=0.12 * H, the_gioi=True)
    sk.xuong("hong", "than", *S(pt["hong"]), dai=0.08 * H, the_gioi=True)
    sk.xuong("nguc", "than", *S(pt["nguc"]), dai=0.08 * H, the_gioi=True)
    a = S(pt["dau"]) - S(pt["co"])
    sk.xuong("co", "nguc", *S(pt["co"]), goc=math.degrees(math.atan2(a[1], a[0])), dai=float(np.hypot(*a)), the_gioi=True)
    a = S(pt["mui"]) - S(pt["dau"])
    sk.xuong("dau", "co", *S(pt["dau"]), goc=math.degrees(math.atan2(a[1], a[0])), dai=float(np.hypot(*a)), the_gioi=True)
    sk.xuong("mom", "dau", *S(pt["mom"]), dai=0.05 * H, the_gioi=True)
    hinge, snout = S(pt["ban_le"]), S(pt["ham_mui"])
    a = snout - hinge
    gj = math.degrees(math.atan2(a[1], a[0]))
    sk.xuong("ham", "dau", *hinge, goc=gj, dai=float(np.hypot(*a)), the_gioi=True)
    sk.xuong("mieng", "dau", *S(pt["mieng"]), goc=0.0, dai=0.08 * H, the_gioi=True)   # chỗ nhả cho VFX, trục x chĩa phải
    if "giap" in lays:
        sk.xuong("vai", "nguc", *S(pt["vai"]), dai=0.05 * H, the_gioi=True)
    ch = {}
    for n, (par, J, _) in CHAINS[k].items():
        ch[n] = sk.chuoi(n, par, [S(p) for p in J])
    legs, foot = {}, {}
    for n, (par, J) in LEGS[k].items():
        legs[n] = sk.chuoi("c" + n[4:], par, [S(p) for p in J])
        foot[n] = S(J[-1])
    for i, p in enumerate(pt["giot"]):
        sk.xuong(f"giot{i + 1}", "move", *S(p), the_gioi=True)
    # ------------------------------------------------ slot (sau → trước, theo lớp cắt)
    order = [l["name"] for l in cat["layers"]]
    bone_of = {"than": "than", "mieng": "dau", "ham": "ham", "giap": "vai", "vay": "than", "duoi": ch["duoi"][0]}
    for n in order:
        if n.startswith("giot"):
            continue
        b = bone_of.get(n) or (legs[n][0] if n in legs else "than")
        sk.slot(n, b, n)
    mi_n, mi_x, gpt_mi = lids(k)
    # mí GPT tô lam sáng hơn da đầu: nhuộm phần da của mí về đúng màu da quanh mắt trên ảnh lớp thân (nét mực giữ nguyên)
    lt0 = lays["than"]
    th = np.asarray(imgs["than"]).astype(np.float32)
    ring = []
    for key in ("mat_n", "mat_x"):
        cx, cy = pt[key]
        u, v = (cx - lt0["box"][0]) / lt0["sx"], (cy - lt0["box"][1]) / lt0["sy"]
        yy, xx = np.mgrid[0:th.shape[0], 0:th.shape[1]]
        d = np.hypot(xx - u, yy - v)
        m = (d > 0.05 * H) & (d < 0.09 * H) & (th[..., 3] > 200) & (th[..., :3].mean(2) > 70) & (th[..., 2] > th[..., 0] + 25)
        ring.append(th[m][:, :3])
    skin = np.median(np.concatenate(ring), 0)

    def tint(im):
        a = np.asarray(im).astype(np.float32)
        body = (a[..., 3] > 0) & (a[..., :3].mean(2) > 70) & (a[..., 2] > a[..., 0] + 15)
        med = np.median(a[body][:, :3], 0)
        a[..., :3] = np.where(body[..., None], np.clip(a[..., :3] * (skin / np.maximum(med, 1)), 0, 255), a[..., :3])
        return Image.fromarray(a.astype(np.uint8), "RGBA")
    mi_n, mi_x = tint(mi_n), tint(mi_x)
    sk.anh("mi_n", mi_n)
    sk.anh("mi_x", mi_x)
    sk.slot("mi_n", "dau", "mi_n", an=True)
    sk.slot("mi_x", "dau", "mi_x", an=True)
    for n in order:
        if n.startswith("giot"):
            sk.slot(n, n, n)
    # ------------------------------------------------ lưới, trọng số
    def dat_of(n):
        return Dat(*lays[n]["rig_tl"], neo=(0.0, 0.0))

    def concept_xy(n, P):
        l = lays[n]
        return np.stack([l["box"][0] + P[:, 0] * l["sx"], l["box"][1] + P[:, 1] * l["sy"]], 1)

    def lab_at(n, P):
        lm = labs[n]
        x = np.clip(P[:, 0].astype(int), 0, lm.shape[1] - 1)
        y = np.clip(P[:, 1].astype(int), 0, lm.shape[0] - 1)
        v = lm[y, x].astype(int)
        bad = v == 255
        if bad.any():   # đỉnh trên viền nới ra ngoài: lấy nhãn pixel gần nhất
            yy, xx = np.nonzero(lm != 255)
            for i in np.flatnonzero(bad):
                j = int(np.argmin((xx - P[i, 0]) ** 2 + (yy - P[i, 1]) ** 2))
                v[i] = lm[yy[j], xx[j]]
        return v

    def to_img(n, poly):
        l = lays[n]
        return [((x - l["box"][0]) / l["sx"], (y - l["box"][1]) / l["sy"]) for x, y in poly]

    stats = {}
    lays_dat = {n: dat_of(n) for n in lays}

    def chain_w(Q, n):
        par, J, hoa = CHAINS[k][n]
        return trongso.chuoi_chieu(Q, [S(p) for p in J], ch[n], cha=par, cha_hoa=hoa)

    def chain_geo(L, lay, n):
        """chuỗi theo khoảng cách đi trong lưới (đuôi sóng, vây cuộn mào: chiếu lên đường khớp làm móc cuộn rách)."""
        par, J, hoa = CHAINS[k][n]
        Ji = np.array(to_img(lay, J))
        near = lambda p: int(np.argmin(((L.pts - p) ** 2).sum(1)))  # noqa: E731
        d = trongso.dijkstra(L, [near(Ji[0])])
        dj = np.array([d[near(p)] for p in Ji])
        dj[0] = 0.0
        for q in range(1, len(dj)):
            dj[q] = max(dj[q] if np.isfinite(dj[q]) else dj[q - 1] + 1.0, dj[q - 1] + 1e-3)
        f = np.interp(np.where(np.isfinite(d), d, 0.0), dj, np.arange(len(dj), dtype=float), left=0.0, right=float(len(dj) - 1))
        over = np.isfinite(d) & (d > dj[-1])
        f[over] = len(dj) - 1 + (d[over] - dj[-1]) / max(1e-6, dj[-1] - dj[-2])
        W = trongso.chuoi_f(f, ch[n], par, hoa)
        bad = np.flatnonzero(~np.isfinite(d))   # mẩu lưới không nối với gốc chuỗi: chiếu lên đường khớp
        if len(bad):
            Wb = trongso.chuoi_chieu(lays_dat[lay].ra(L.pts[bad], imgs[lay].width, imgs[lay].height), [S(p) for p in J], ch[n], par, hoa)
            for j, i in enumerate(bad):
                W[i] = Wb[j]
        return W

    for n in order:
        im = imgs[n]
        L = luoi.luoi_vung(im, buoc_theo_cao=H * thua * (1.3 if n in AN else 1.0), ten=n, in_tk=False)
        stats[n] = L.thong_ke()
        dat = dat_of(n)
        Q = dat.ra(L.pts, im.width, im.height)
        C = concept_xy(n, L.pts)
        lb = lab_at(n, L.pts)
        if n == "than":
            reg = [(b, to_img(n, pg)) for b, pg in REGIONS[k]] + [("than", [(0, 0), (im.width, 0), (im.width, im.height), (0, im.height)])]
            W = trongso.vung(L, reg, dai_hoa=0.10 * H)
            xa = pt["dau"][0] + 0.3 * (pt["mui"][0] - pt["dau"][0])
            m = smooth((C[:, 0] - xa) / max(1.0, pt["mui"][0] - xa)) * 0.5   # nửa trước mõm hoà xương mom (mõm mềm)
            W = [({**{b: w for b, w in d.items() if b != "dau"}, "dau": d.get("dau", 0) * (1 - mm), "mom": d.get("dau", 0) * mm}
                  if d.get("dau", 0) > 0 else d) for d, mm in zip(W, m)]
            for e in ("tai_n", "tai_x"):
                ids = np.flatnonzero(lb == names.index(e))
                if len(ids):
                    We = chain_w(Q[ids], e)
                    for j, i in enumerate(ids):
                        W[i] = We[j]
            W = trongso.lam_tron(L, W, 2)
        elif n == "vay":
            W = [None] * L.n
            for f in [x for x in CHAINS[k] if x.startswith("vay")]:
                ids = np.flatnonzero(lb == names.index(f))
                if len(ids):
                    Wf = chain_geo(L, n, f)
                    for i in ids:
                        W[i] = Wf[i]
            W = [w or {"than": 1.0} for w in W]
            W = trongso.chuan(W)
        elif n == "duoi":
            W = trongso.lam_tron(L, chain_geo(L, n, "duoi"), 1)
        elif n in legs:
            par, J = LEGS[k][n]
            W = trongso.chuoi_chieu(Q, [S(p) for p in J], legs[n], cha=par, cha_hoa=0.85)
            W = trongso.lam_tron(L, W, 1)
        elif n == "mieng":   # thịt trong miệng thuộc hàm dưới: phần dưới theo hàm, mép trên nấp sau đầu
            u = smooth((C[:, 1] - pt["mieng_tren"]) / (pt["mieng_duoi"] - pt["mieng_tren"]) * 1.3)
            W = [{"ham": float(v), "dau": float(1 - v)} if 0 < v < 1 else ({"ham": 1.0} if v >= 1 else {"dau": 1.0}) for v in u]
        elif n == "ham" and k == 1:   # hàm Hà Mã Con: phần sau bản lề hoà vào đầu (má không lộ đường cắt khi há)
            W = mieng.ham_hai_xuong(Q, hinge, snout, "dau", "ham", u0=-0.06, u1=0.12)
        elif n == "ham":
            W = trongso.cung(L.n, "ham")
        elif n == "giap":
            W = trongso.cung(L.n, "vai")
        elif n.startswith("giot"):
            W = trongso.cung(L.n, n)
        else:
            W = trongso.cung(L.n, "than")
        trongso.kiem(W, n, cho_cung=("ham", "vai", "giot1", "giot2", "giot3"), in_ra=False)
        sk.luoi_gan(n, n, L, W, dat=dat)
    # mí: dò cho phủ kín mắt trên ảnh lớp thân
    lt = lays["than"]
    dat_t = dat_of("than")
    kq = {}
    for slot, key, hk in (("mi_n", "mat_n", "hop_n"), ("mi_x", "mat_x", "hop_x")):
        cx, cy = pt[key]
        hat = ((cx - lt["box"][0]) / lt["sx"], (cy - lt["box"][1]) / lt["sy"])
        b = pt[hk]
        hop = ((b[0] - lt["box"][0]) / lt["sx"], (b[1] - lt["box"][1]) / lt["sy"], (b[2] - lt["box"][0]) / lt["sx"], (b[3] - lt["box"][1]) / lt["sy"])
        # hạt mắt phải nằm trên tròng vàng/hổ phách (hạt rơi vào con ngươi đen thì vùng mắt lan theo nét mực, mí phóng quá to)
        arr = np.asarray(imgs["than"]).astype(int)
        x0_, y0_, x1_, y1_ = (int(round(v)) for v in hop)
        sub = arr[y0_:y1_, x0_:x1_]
        iris = (sub[..., 0] > 180) & (sub[..., 1] > 100) & (sub[..., 2] < 120) & (sub[..., 3] > 200)
        if iris.any():
            yy, xx = np.nonzero(iris)
            c = np.array([xx.mean(), yy.mean()])
            j = int(np.argmin((xx - c[0]) ** 2 + (yy - c[1]) ** 2))
            hat = (x0_ + xx[j], y0_ + yy[j])
        for noi in (3, 2, 1, 0):   # mí phải phủ kín (còn hở 0 px): nới vùng mắt ít dần nếu chưa kín
            r = mieng.fit_lid(imgs["than"], sk.images[slot], hat=hat, hop=hop, noi=noi, ten=f"dạng {k} {slot} (nới {noi})",
                              goc=(-36, 36, 4), ti=(0.8, 2.6, 0.1), doi=16)
            if r[4] == 0:
                break
        kq[slot] = r
        sk.manh(slot, slot, mieng.dat_mi(dat_t, imgs["than"], r))
    for e, mo in (("trung", "khung đòn thường trúng"), ("phun", "bắt đầu nhả (VFX bám xương mieng)"), ("het_phun", "hết nhả"),
                  ("gam", "chiêu cuối bung"), ("het_gam", "hết chiêu cuối"), ("troi", "nước trồi dưới chân đối thủ"),
                  ("dam", "chân nện đất")):
        sk.su_kien(e, mo)
    info = {"H": H, "ks": ks, "ground": (xg, yg), "chains": ch, "legs": legs, "foot": foot, "lid": kq, "gpt_mi": gpt_mi,
            "mesh": stats, "S": S, "names": names, "lays": lays}
    tk = sk.tom_tat()
    print(f"dạng {k}: H {H:.0f} px, {tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh, {tk['tam_giac']} tam giác; "
          f"mí {'GPT' if gpt_mi else 'GIỮ CHỖ'}; hở lưới " + ", ".join(f"{n} {s.get('ho', '?')}" for n, s in stats.items()))
    return sk, info


# ---------------------------------------------------------------- clip
def clips(sk, info, k):
    H = info["H"]
    ch, legs, foot = info["chains"], info["legs"], info["foot"]
    tai = ch["tai_n"] + ch["tai_x"]
    vays = [ch[n] for n in ch if n.startswith("vay")]
    duoi = ch["duoi"]
    giots = [b for b in sk.bi if b.startswith("giot")]
    big = k == 2
    mem = [LoXo(v, k=[300, 230, 180][:len(v)] + [150] * max(0, len(v) - 3), damp=0.6, maxang=12) for v in vays] + \
          [LoXo(ch["tai_n"], k=[340, 260], damp=0.6, maxang=14), LoXo(ch["tai_x"], k=[340, 260], damp=0.6, maxang=14)]
    D_IDLE = 2.4 if big else 2.0

    def nen(P, tt, amp=1.0):
        """chuyển động nền của idle (giờ tt): thở, đầu gật lệch pha, vây lượn sóng; amp nhỏ khi đang ra đòn."""
        s, c = song(tt, D_IDLE), song(tt, D_IDLE, 1.1)
        P.move("than", 0, (0.008 if big else 0.012) * H * s * amp)
        P.scale("than", 1 + 0.012 * s * amp, 1 - 0.012 * s * amp)
        P.rot("nguc", 0.8 * c * amp)
        P.rot("hong", -0.6 * c * amp)
        P.rot("dau", (-1.2 * c + 0.9 * song(tt, D_IDLE, 2.0)) * amp)
        P.rot("ham", (2.0 if big else 1.4) * song(tt, D_IDLE / 2, 0.6) * amp)
        for i, v in enumerate(vays):
            chuoi_song(P, v, tt, D_IDLE, [2.5, 3.5, 4.5, 5.0][:len(v)], tre=0.12, ngon_dan=False, pha=0.9 * i)
        for e in (ch["tai_n"], ch["tai_x"]):
            chuoi_song(P, e, tt, D_IDLE, [2.0, 3.0], tre=0.06, ngon_dan=False, pha=1.7)

    def feet(P, lift=None):
        """bàn chân bám đất (IK). lift: {chân: (w, góc vung)}: w = 1 thì chân theo thân như cột cứng (thân chồm lên là chân nhấc
        theo, không gập gối), vung thêm góc quanh vai; w = 0 bám đất. Chân trụ hà mã không gập gối khi nhấc."""
        W = sk.the_gioi(P)
        lift = lift or {}
        for n, names in legs.items():
            f = foot[n]
            ground = (W["move"] @ np.array([f[0], f[1], 1.0]))[:2]
            w, sw = lift.get(n, (0.0, 0.0))
            tgt = ground
            if w > 1e-4:
                par = sk.bones[sk.bi[names[0]]]["parent"]
                Mp = W[par] @ np.linalg.inv(sk.W0[par])
                fk = (Mp @ np.array([f[0], f[1], 1.0]))[:2]
                sh = W[names[0]][:2, 2]
                r = math.radians(sw)
                v = fk - sh
                fk = sh + np.array([v[0] * math.cos(r) - v[1] * math.sin(r), v[0] * math.sin(r) + v[1] * math.cos(r)])
                tgt = (1 - w) * ground + w * fk
            hoat.ik_hai_doan(sk, P, names[0], names[1], tgt)

    def idle_fn(t, P):
        nen(P, t)
        if big:   # phá nhịp: phì mũi, hất đầu, táp hàm ở 62–72%
            P.rot("dau", 4.0 * cv(t, [(0, 0), (1.5, 0), (1.6, 1, "out"), (1.72, -0.4), (1.9, 0, "io"), (D_IDLE, 0)]))
            P.rot("ham", 6.0 * cv(t, [(0, 0), (1.52, 0), (1.62, 1, "out"), (1.74, -0.6), (1.92, 0, "io"), (D_IDLE, 0)]))
            P.rot(ch["tai_n"][0], -10 * cv(t, [(0, 0), (1.55, 0), (1.62, 1, "out"), (1.8, 0, "io"), (D_IDLE, 0)]))
            an_hien(P, "mi_n", t, [(0.9, 1.02)])
            an_hien(P, "mi_x", t, [(0.9, 1.02)])
        else:     # nhai táp ở 62–72%, chớp mắt
            P.rot("ham", 5.0 * cv(t, [(0, 0), (1.24, 0), (1.3, 1, "out"), (1.36, 0), (1.42, 1, "out"), (1.52, 0, "io"), (D_IDLE, 0)]))
            P.rot(ch["tai_x"][0], -12 * cv(t, [(0, 0), (0.6, 0), (0.66, 1, "out"), (0.8, 0, "io"), (D_IDLE, 0)]))
            an_hien(P, "mi_n", t, [(1.62, 1.74)])
            an_hien(P, "mi_x", t, [(1.62, 1.74)])
        feet(P)

    def fade_all(P, a):
        for s in sk.slots:
            if s["alpha"] > 0:
                P.alpha[s["name"]] = a

    # ---------------- appear: rơi bịch xuống, dẹt nảy, lắc đầu rũ nước
    def appear_fn(t, P, D=1.6 if big else 1.2):
        T1 = 0.45 if big else 0.36
        fade_all(P, cv(t, [(0, 0), (0.08, 1)]))
        P.move("move", 0, cv(t, [(0, 0.9 * H), (T1, 0, "in"), (D, 0)]))
        sq = cv(t, [(0, 0.06), (T1, 0), (T1 + 0.08, -0.16 if big else -0.2, "out"), (T1 + 0.24, 0.06, "io"), (T1 + 0.4, -0.02, "io"),
                    (T1 + 0.55, 0, "io"), (D, 0)])
        P.scale("move", 1 - 0.6 * sq, 1 + sq)
        P.rot("dau", 7 * math.sin(2 * math.pi * 3.2 * max(0, t - T1 - 0.35)) * cv(t, [(0, 0), (T1 + 0.35, 0), (T1 + 0.45, 1), (D - 0.25, 0, "io"), (D, 0)]))
        P.rot("ham", -10 * cv(t, [(0, 0), (T1 + 0.05, 0), (T1 + 0.15, 1, "out"), (T1 + 0.5, 0, "io"), (D, 0)]))
        nen(P, lui(t, D), ease((t - T1) / (D - T1)))
        feet(P)

    # ---------------- attack
    if big:   # Dậm Triều: chồm hai chân trước lên, dậm xuống (sóng xung kích chạy dọc đất do VFX)
        DA, HA = 1.3, 0.58

        def attack_fn(t, P):
            up = cv(t, [(0, 0), (0.12, -0.15, "io"), (0.46, 1, "io"), (0.52, 1.06), (HA, -0.35, "in"), (HA + 0.06, -0.42), (0.95, -0.25, "io"),
                        (DA, 0, "io")])
            nen(P, lui(t, DA), 1 - 0.8 * bao(t, 0.05, DA - 0.1, 0.15, 0.3))
            P.rot("than", 9 * up)
            P.move("than", -0.01 * H * max(up, 0), 0.03 * H * max(up, 0))
            P.rot("nguc", 3 * up)
            P.rot("dau", 5 * up + 1.5 * rung(t, HA, HA + 0.2))
            P.rot("ham", -8 * max(up, 0) + 4 * cv(t, [(0, 0), (HA - 0.02, 0), (HA, 1, "out"), (0.9, 0.3), (DA, 0)]))
            sq = cv(t, [(0, 0), (HA - 0.02, 0), (HA, -0.07, "out"), (HA + 0.1, 0.02, "io"), (0.9, 0, "io"), (DA, 0)])
            P.scale("move", 1 - 0.5 * sq, 1 + sq)
            w = cv(t, [(0, 0), (0.12, 0), (0.4, 1, "io"), (0.52, 1), (HA, 0, "in"), (DA, 0)])
            feet(P, {"chan_tn": (w, 16 * w), "chan_tx": (w, 12 * w)})
    else:     # Ngoạm Nước: ngửa há rộng, đớp mạnh tại chỗ (hàm nước VFX đớp vào đối thủ)
        DA, HA = 0.9, 0.42

        def attack_fn(t, P):
            lean = cv(t, [(0, 0), (0.3, 1, "io"), (0.36, 1.08), (HA, -1.0, "in"), (0.48, -1.12), (0.64, -0.9, "io"), (DA, 0, "io")])
            nen(P, lui(t, DA), 1 - 0.7 * bao(t, 0.08, 0.8, 0.2, 0.25))
            P.rot("than", 3 * lean)
            P.rot("dau", 9 * lean)
            P.rot("ham", -cv(t, [(0, 0), (0.28, 26, "io"), (HA - 0.03, 30), (HA, -6, "in"), (0.5, -4), (0.62, 0, "io"), (DA, 0)]))
            P.scale("dau", cv(t, [(0, 1), (HA - 0.03, 1), (HA, 1.1), (HA + 0.05, 0.97), (0.62, 1), (DA, 1)]),
                    cv(t, [(0, 1), (HA - 0.03, 1), (HA, 0.93), (HA + 0.05, 1.03), (0.62, 1), (DA, 1)]))
            sq = cv(t, [(0, 0), (0.3, 0.05, "io"), (HA, -0.08, "in"), (HA + 0.1, 0.02, "io"), (0.7, 0, "io"), (DA, 0)])
            P.scale("move", 1 - 0.5 * sq, 1 + sq)
            feet(P)

    # ---------------- cast
    if big:   # Vòi Rồng Nước: ngửa nén, há to phun giữ 0,55 s rung hai dáng
        DC, HC, EC = 1.5, 0.6, 1.12

        def cast_fn(t, P):
            rear = cv(t, [(0, 0), (0.48, 1, "io"), (0.55, 1.06), (HC, -0.7, "in"), (0.7, -0.8), (EC, -0.7), (DC, 0, "io")])
            nen(P, lui(t, DC), 1 - 0.85 * bao(t, 0.05, DC - 0.1, 0.2, 0.3))
            P.rot("than", 2.5 * rear)
            P.rot("nguc", 2 * rear)
            P.rot("co", 3 * rear)
            P.rot("dau", 6 * rear + 1.2 * rung(t, HC + 0.04, EC))
            P.rot("ham", 6 * max(rear, 0) - cv(t, [(0, 0), (0.48, 0), (HC, 22, "out"), (EC, 19), (DC, 0, "io")]) - 2.5 * rung(t, HC + 0.04, EC))
            P.move("move", cv(t, [(0, 0), (HC, 0), (HC + 0.1, -0.025 * H, "out"), (EC, -0.018 * H), (DC, 0, "io")]), 0)
            feet(P)
    else:     # Súng Nước: phồng hít, há nhả ba nhịp
        DC, HC, EC = 1.0, 0.5, 0.82

        def cast_fn(t, P):
            puff = cv(t, [(0, 0), (0.42, 1, "io"), (HC, -0.3, "out"), (EC, -0.2), (DC, 0, "io")])
            nen(P, lui(t, DC), 1 - 0.8 * bao(t, 0.05, 0.92, 0.2, 0.2))
            P.scale("than", 1 + 0.05 * max(puff, 0), 1 + 0.04 * max(puff, 0))
            P.rot("dau", 6 * max(puff, 0) - 3 * max(-puff, 0) + 1.0 * rung(t, HC, EC))
            pul = sum(cv(t, [(0, 0), (HC + 0.1 * j, 0), (HC + 0.1 * j + 0.04, 1, "out"), (HC + 0.1 * j + 0.1, 0.4)]) for j in range(3))
            P.rot("ham", -cv(t, [(0, 0), (0.42, 0), (HC, 18, "out"), (EC, 16), (DC, 0, "io")]) - 3 * min(pul, 1.2))
            P.move("move", cv(t, [(0, 0), (HC, 0), (HC + 0.08, -0.03 * H, "out"), (EC, -0.02 * H), (DC, 0, "io")]), 0)
            feet(P)

    # ---------------- skill
    if big:   # Hà Bá Nuốt Sông: ngửa gầm há rộng, giữ rung, dậm hai chân trước gọi xoáy (VFX ở chỗ đối thủ)
        DS, HS, ES = 2.3, 0.95, 1.7

        def skill_fn(t, P):
            cr = cv(t, [(0, 0), (0.25, -0.2, "io"), (0.8, 1, "io"), (0.88, 1.05), (HS, 0.85, "out"), (1.15, 0.9), (1.25, -0.25, "in"),
                        (ES, -0.15), (DS, 0, "io")])
            nen(P, lui(t, DS), 1 - 0.85 * bao(t, 0.05, DS - 0.1, 0.25, 0.4))
            P.rot("than", 10 * cr)
            P.move("than", 0, 0.03 * H * max(cr, 0))
            P.rot("co", 4 * cr)
            P.rot("dau", 10 * cr + 2.0 * rung(t, HS, ES))
            P.rot("ham", -cv(t, [(0, 0), (0.25, 0), (HS, 26, "out"), (ES, 22), (DS, 0, "io")]) - 3 * rung(t, HS, ES))
            sq = cv(t, [(0, 0), (1.23, 0), (1.27, -0.08, "out"), (1.4, 0.02, "io"), (1.6, 0, "io"), (DS, 0)])
            P.scale("move", 1 - 0.5 * sq, 1 + sq)
            w = cv(t, [(0, 0), (0.25, 0), (0.8, 1, "io"), (1.15, 1), (1.27, 0, "in"), (DS, 0)])
            feet(P, {"chan_tn": (w, 20 * w), "chan_tx": (w, 15 * w)})
        EVS = [(HS, "gam", ""), (1.27, "dam", ""), (1.32, "troi", ""), (ES, "het_gam", "")]
    else:     # Ngáp Sóng: vươn mình ngáp thật to, sóng lăn từ miệng (VFX)
        DS, HS, ES = 1.8, 0.78, 1.3

        def skill_fn(t, P):
            cr = cv(t, [(0, 0), (0.3, -0.3, "io"), (0.7, 1, "io"), (HS, 1.04), (ES, 0.9), (1.5, -0.1, "io"), (DS, 0, "io")])
            nen(P, lui(t, DS), 1 - 0.85 * bao(t, 0.05, 1.7, 0.25, 0.3))
            P.scale("move", 1 - 0.04 * max(cr, 0) + 0.04 * max(-cr, 0), 1 + 0.08 * max(cr, 0) - 0.06 * max(-cr, 0))
            P.rot("dau", 12 * cr + 1.5 * rung(t, HS, ES))
            P.rot("ham", -cv(t, [(0, 0), (0.3, 0), (HS, 34, "out"), (ES, 30), (1.55, 0, "io"), (DS, 0)]) - 3 * rung(t, HS, ES))
            an_hien(P, "mi_n", t, [(0.62, 1.28)])
            an_hien(P, "mi_x", t, [(0.62, 1.28)])
            feet(P)
        EVS = [(HS, "gam", ""), (ES, "het_gam", "")]

    # ---------------- hit: không lấy đà, đỉnh 0,07 s, sóng từ ngọn về gốc, nhắm mắt
    def hit_fn(t, P, D=0.6):
        hd = cv(t, [(0, 0), (0.07, 1, "out"), (0.2, 0.55, "io"), (0.42, -0.12, "io"), (D, 0, "io")])
        bd = cv(t, [(0, 0), (0.07, 0.3, "out"), (0.2, 1, "io"), (0.44, -0.05, "io"), (D, 0, "io")])
        nen(P, lui(t, D), ease((t - 0.25) / 0.35))
        P.rot("dau", 12 * hd)
        P.rot("than", 3 * bd)
        P.move("move", -0.03 * H * bd, 0)
        P.rot("ham", -8 * hd)
        an_hien(P, "mi_n", t, [(0.03, 0.34)])
        an_hien(P, "mi_x", t, [(0.03, 0.34)])
        for v in vays + [ch["tai_n"], ch["tai_x"]]:
            n = len(v)
            for i, b in enumerate(v):
                P.rot(b, (5 + 3 * i) * cv(t, [(0, 0), (0.07 + 0.04 * (n - 1 - i), 1, "out"), (0.32 + 0.04 * i, -0.3, "io"), (D, 0, "io")]))
        feet(P)

    # ---------------- die: giật, nhắm mắt, lả gục đầu giữ nhịp, khuỵu đổ nghiêng, tan
    def die_fn(t, P, D=2.0 if big else 1.6):
        f = 1.0 if big else 0.8
        P.rot("dau", cv(t, [(0, 0), (0.07, 12, "out"), (0.3, 4), (0.75 * f, -14, "io"), (1.0 * f, -12), (1.3 * f, -22, "in"), (D, -22)]))
        P.rot("ham", -cv(t, [(0, 0), (0.07, 14, "out"), (0.3, 6), (0.8 * f, 20, "io"), (D, 20)]))
        P.rot("than", cv(t, [(0, 0), (0.07, 3, "out"), (0.8 * f, -3, "io"), (1.3 * f, -6, "in"), (D, -6)]))
        P.move("move", cv(t, [(0, 0), (1.0 * f, 0), (1.3 * f, -0.03 * H, "in"), (D, -0.03 * H)]),
               cv(t, [(0, 0), (0.07, 0.02 * H, "out"), (0.3, 0), (1.0 * f, 0), (1.3 * f, -0.09 * H, "in"), (1.4 * f, -0.08 * H, "out"), (D, -0.085 * H)]))
        P.scale("move", 1, cv(t, [(0, 1), (1.0 * f, 1), (1.3 * f, 0.9, "in"), (1.4 * f, 0.93), (D, 0.92)]))
        an_hien(P, "mi_n", t, [(0.04, D + 1)])
        an_hien(P, "mi_x", t, [(0.04, D + 1)])
        a = cv(t, [(0, 1), (D - 0.45, 1), (D - 0.05, 0, "io"), (D, 0)])
        fade_all(P, a)
        P.alpha["mi_n"] = a
        P.alpha["mi_x"] = a
        for b in giots:
            P.alpha[b] = 0.0

    # ---------------- aura: hồn nước ở đuôi tự cuộn (sóng dâng tại chỗ, mào cuộn chặt dần rồi duỗi), giọt nước nhấp nhô quanh đuôi
    DAU = 2.4 if big else 2.0

    def aura_fn(t, P):
        u = 2 * math.pi * t / DAU
        n = len(duoi)
        for i, b in enumerate(duoi):
            fr = (i + 0.5) / n
            P.rot(b, (2.0 + 7.0 * fr) * math.sin(u - 0.7 * i) + 3.0 * fr * math.sin(2 * u - 1.1 * i))
        for j, b in enumerate(giots):
            ph = u + 2.1 * j
            P.move(b, 0.03 * H * math.sin(ph) * (1 if j % 2 else -1), 0.035 * H * math.sin(ph * 1.0 + 0.6))
            sc = 1 + 0.1 * math.sin(2 * ph)
            P.scale(b, sc, sc)

    clips_ = [Clip("appear", 1.6 if big else 1.2, appear_fn, mem=mem),
              Clip("idle", D_IDLE, idle_fn, loop=True, mem=mem),
              Clip("attack", DA, attack_fn, ev=[(HA, "trung", "")] + ([(HA, "dam", "")] if big else []), mem=mem),
              Clip("cast", DC, cast_fn, ev=[(HC, "phun", ""), (EC, "het_phun", "")], mem=mem),
              Clip("skill", DS, skill_fn, ev=EVS, mem=mem),
              Clip("hit", 0.6, hit_fn, mem=mem),
              Clip("die", 2.0 if big else 1.6, die_fn, mem=mem),
              Clip("aura", DAU, aura_fn, loop=True)]
    return clips_


# ---------------------------------------------------------------- soi
def so_concept(sk, frames, k, info, ra):
    """khung 0 idle (bỏ aura) đặt cạnh concept cùng tỉ lệ, IoU mặt nạ."""
    ve = soi.Ve(sk)
    P = frames["idle"][0].copy()
    ks, (xg, yg) = info["ks"], info["ground"]
    cpt = Image.open(os.path.join(base(k), "tai_ve", "L1_duyet.png")).convert("RGB")
    Wc, Hc = cpt.size
    box = (-xg * ks, -(Hc - yg) * ks, (Wc - xg) * ks, yg * ks)   # thế giới rig phủ đúng khung concept
    im = ve.ve(P, box, 1.0 / ks, bg=None, ss=1)
    im = im.resize((Wc, Hc))
    a = np.asarray(im)[..., 3] > 100
    fgp = os.path.join(base(k), "manh", "fg.png")
    ref = np.asarray(Image.open(fgp)) > 127 if os.path.exists(fgp) else np.asarray(cpt).min(2) < 235
    iou = float((a & ref).sum() / max(1, (a | ref).sum()))
    best = (iou, 0, 0)
    for dx in range(-6, 7, 2):
        for dy in range(-6, 7, 2):
            b = np.roll(np.roll(a, dy, 0), dx, 1)
            v = float((b & ref).sum() / max(1, (b | ref).sum()))
            if v > best[0]:
                best = (v, dx, dy)
    print(f"  so_concept dạng {k}: IoU {iou:.3f}; tốt nhất nếu dời ({best[1]}, {best[2]}) px concept: {best[0]:.3f}")
    comp = Image.new("RGB", (Wc, Hc), (150, 150, 150))
    comp.paste(im.convert("RGB"), (0, 0), im)
    diff = np.full((Hc, Wc, 3), 255, np.uint8)
    diff[ref & ~a] = (230, 60, 60)
    diff[~ref & a] = (60, 110, 230)
    diff[ref & a] = (205, 205, 205)
    out = Image.new("RGB", (Wc * 3, Hc), "white")
    out.paste(cpt, (0, 0))
    out.paste(comp, (Wc, 0))
    out.paste(Image.fromarray(diff), (2 * Wc, 0))
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(out)
    d.text((20, 20), f"IoU khung 0 idle / concept = {iou:.3f}", fill=(0, 0, 0), font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 40))
    out.resize((Wc * 3 // 2, Hc // 2)).save(ra)
    return iou


def uon_thu(sk, info, ra, k):
    P = khung.Pose()
    for n, v in info["chains"].items():
        for b in v:
            P.rot(b, 16 if n == "duoi" else 12)
    for n, v in info["legs"].items():
        P.rot(v[0], 18)
        P.rot(v[1], -28)
    P.rot("dau", 14)
    P.rot("ham", -24)
    P.rot("than", 6)
    ve = soi.Ve(sk)
    B = soi._union([ve.bao(P)], 0.05)
    ve.ve(P, B, 1.4, bg=(150, 150, 150), ss=2, luoi=True, mau_luoi=(10, 10, 10, 110)).convert("RGB").save(ra)


def ghi_them(ra, ten, k, info, iou, t, ghi=""):
    """nối vào so_sanh.md: mật độ lưới theo chiều cao, số đỉnh từng lớp, IoU khung 0 với concept, mí."""
    H = info["H"]
    rows = [f"| {n} | {st['dinh']} | {st['tam_giac']} | {st['goc_tb']:.0f}° | {100 * st['duoi25']:.1f}% | {st['ho']} |"
            for n, st in info["mesh"].items()]
    lid = "; ".join(f"{s}: còn hở {r[4]} px" for s, r in info["lid"].items())
    txt = ["", f"## Lưới, khớp concept (dạng {k}, {TEN[k]})", "",
           f"- Chiều cao con H = {H:.0f} px atlas; bước viền {0.015 * H:.1f} px (1,5% H), bước trong {0.02 * H:.1f} px (2% H); "
           f"lớp gần như luôn khuất (chân xa, lòng miệng) thưa hơn 1,3 lần.",
           f"- Đỉnh / chiều cao: {sum(st['dinh'] for st in info['mesh'].values())} đỉnh / {H:.0f} px"
           + (f" (riêng dạng 1; tổng {t['dinh']} đỉnh gồm dạng 2 gộp cho tiến hóa, dạng 2 trong rig gộp lưới thưa 1,6 lần)" if k == 1 else ""),
           f"- IoU khung 0 idle với concept: {iou:.3f} (đích ≥ 0,9; cách lai: thân, đầu, vây, đuôi, chân gần, giáp, hàm cắt thẳng từ concept).",
           f"- Mí mắt (tờ GPT M01, nhuộm về màu da): {lid}.",
           "", "| Lớp | Đỉnh | Tam giác | TB góc nhỏ | % góc < 25° | Hở px |", "|---|---|---|---|---|---|"] + rows
    if ghi:
        txt += ["", ghi]
    with open(os.path.join(ra, "so_sanh.md"), "a", encoding="utf-8") as f:
        f.write("\n".join(txt) + "\n")


def cao_game(sk, frames, max_w=1.42):
    ve = soi.Ve(sk)
    P = frames["idle"][0].copy()
    for s in sk.slots:   # chiều cao dáng đứng tính cả đuôi sóng (aura chỉ cuộn nó tại chỗ), chỉ bỏ giọt nước bay
        if s["name"].startswith("giot") or s["name"].startswith("n_giot"):
            P.alpha[s["name"]] = 0.0
    x0, y0, x1, y1 = ve.bao(P)
    h = max(1.0, y1)
    return round(max(h, (x1 - x0) / max_w), 2), (x1 - x0) / h


# ---------------------------------------------------------------- chạy
def xuat_dang2():
    t0 = time.time()
    sk2, info2 = dung(2)
    cl2 = clips(sk2, info2, 2)
    fr2 = {c.ten: hoat.nuong(sk2, c) for c in cl2}
    print(f"dạng 2: nướng {len(cl2)} clip ({time.time() - t0:.1f} s)")
    cao2, ty2 = cao_game(sk2, fr2)
    ra = os.path.join(base(2), "rig")
    t2 = xuat.xuat_het(sk2, cl2, ra, f"{CODE}_2", f"Hà Bá (dạng 2, {TEN[2]})", frames=fr2, dang=2, so_dang=2,
                       dung_yen=("attack", "cast", "skill"), ma_goc=3233, cao=cao2, tol={"rotate": 0.2},
                       can=[("can_mieng_cast", "cast", 0.75, "ham", 0.22 * info2["H"]),
                            ("can_mieng_skill", "skill", 1.2, "ham", 0.22 * info2["H"]),
                            ("can_chan_attack", "attack", 0.5, "c_tn0", 0.25 * info2["H"]),
                            ("can_mi_hit", "hit", 0.15, "dau", 0.16 * info2["H"]),
                            ("can_vay_hit", "hit", 0.12, "vay41", 0.25 * info2["H"])])
    iou = so_concept(sk2, fr2, 2, info2, os.path.join(ra, "so_concept.png"))
    ghi_them(ra, f"{CODE}_2", 2, info2, iou, t2, f"Dạng 2 rộng/cao {ty2:.2f}: game.height khai {cao2} (max_w 1,42) để không lòi mép sân.")
    uon_thu(sk2, info2, os.path.join(ra, "uon_thu.png"), 2)
    print(f"dạng 2: IoU khung 0 / concept {iou:.3f}; rộng/cao {ty2:.2f}, height game {cao2}")
    return sk2, info2, cl2, fr2, t2, iou


def xuat_dang1(sk2, info2, cl2, fr2):
    t0 = time.time()
    sk1, info1 = dung(1)
    cl1 = clips(sk1, info1, 1)
    fr1 = {c.ten: hoat.nuong(sk1, c) for c in cl1}
    ve1, ve2 = soi.Ve(sk1), soi.Ve(sk2)
    bo1 = xuat.slot_aura(sk1, fr1.get("aura"))
    bo2 = xuat.slot_aura(sk2, fr2.get("aura"))
    hA, hB = soi.chieu_cao(ve1, fr1["idle"][0], bo1), soi.chieu_cao(ve2, fr2["idle"][0], bo2)
    # dạng sau trong rig gộp chỉ hiện ở cuối clip tiến hóa (cỡ 0,7, game đổi sang rig dạng 2 ngay sau): lưới thưa hơn cho nhẹ file,
    # khung 0 idle vẫn trùng khít (cùng ảnh, cùng xương, chỉ khác cách chia tam giác)
    sk2, info2c = dung(2, thua=1.6)
    cl2 = clips(sk2, info2c, 2)
    fr2 = {c.ten: hoat.nuong(sk2, c) for c in cl2 if c.ten in ("idle", "aura")}
    ve2 = soi.Ve(sk2)
    # tỉ lệ dạng sau trong rig gộp theo đúng chiều cao game.height hai dạng (game co mỗi dạng theo height của nó): khung cuối
    # evolve trùng khít dạng 2 khi đổi rig
    hA, hB = cao_game(sk1, fr1)[0], cao_game(sk2, fr2)[0]
    M = tienhoa.gop(sk1, sk2)

    def gong(t, P):   # Hà Mã Con gồng, phồng mình, ngửa đầu
        sq = cv(t, [(0, 0), (0.3, -0.08), (0.45, 0.06, "out"), (1.0, 0.05), (1.3, 0.0)])
        P.scale("move", 1 - 0.5 * sq, 1 + sq)
        P.rot("dau", cv(t, [(0, 0), (0.3, -5), (0.6, 12, "out"), (1.3, 14)]) + 1.5 * rung(t, 0.5, 1.3))
        P.rot("ham", -cv(t, [(0, 0), (0.5, 0), (0.7, 20, "out"), (1.3, 24)]))

    def gam(t, P, fl):  # Hà Bá gầm
        P.rot("n_dau", 9 * fl)
        P.rot("n_ham", -24 * fl)
        P.rot("n_than", 4 * fl)
        P.scale("n_move", 1 + 0.04 * fl, 1 + 0.04 * fl)

    memM = cl1[1].mem + tienhoa.doi_ten_mem(cl2[1].mem)
    ev = tienhoa.clip_tien_hoa(M, sk1, sk2, fr2["idle"][0], tiB=hA / hB, fnA=gong, fnB=gam, mem=memM)
    aura = tienhoa.gop_aura(cl1[-1], cl2[-1])
    clM = [c for c in cl1 if c.ten != "aura"] + [ev, aura]
    frM = {c.ten: fr1[c.ten] for c in cl1 if c.ten != "aura"}
    frM["evolve"] = hoat.nuong(M, ev)
    frM["aura"] = hoat.nuong(M, aura)
    px, con, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, fr2["idle"][0], hA / hB)
    cao1, ty1 = cao_game(sk1, fr1)
    ra = os.path.join(base(1), "rig")
    t1 = xuat.xuat_het(M, clM, ra, f"{CODE}_1", f"Hà Bá (dạng 1, {TEN[1]}, gộp tiến hóa)", frames=frM, dang=1, so_dang=2,
                       dung_yen=("attack", "cast", "skill"), ma_goc=3233, cao=cao1, tol={"rotate": 0.2},
                       noi_them={"evolve": s_ev + f" (dạng sau co {hA / hB:.3f} trong rig gộp)"},
                       can=[("can_mieng_attack", "attack", 0.3, "ham", 0.25 * info1["H"]),
                            ("can_mieng_skill", "skill", 0.9, "ham", 0.25 * info1["H"]),
                            ("can_mi_hit", "hit", 0.15, "dau", 0.2 * info1["H"]),
                            ("can_tien_hoa", "evolve", 1.3, "move", 0.6 * info1["H"])])
    iou = so_concept(sk1, fr1, 1, info1, os.path.join(ra, "so_concept.png"))
    ghi_them(ra, f"{CODE}_1", 1, info1, iou, t1)
    uon_thu(sk1, info1, os.path.join(ra, "uon_thu.png"), 1)
    print(f"dạng 1: IoU khung 0 / concept {iou:.3f}; rộng/cao {ty1:.2f}, height game {cao1}; {time.time() - t0:.1f} s")
    return t1, iou


def show(k, clip, times, scale=1.6):
    """khung lớn để soi: tm04.py show <k> <clip> t1,t2,... -> rig/show_<clip>.png (nền xám, aura ghép)."""
    sk, info = dung(k)
    cl = {c.ten: c for c in clips(sk, info, k)}
    fr = hoat.nuong(sk, cl[clip])
    au = hoat.nuong(sk, cl["aura"])
    fr = hoat.phu_aura(fr, au, sk)
    ve = soi.Ve(sk)
    Ps = [fr[min(len(fr) - 1, int(round(float(t) * 30)))] for t in times]
    B = soi._union([ve.bao(P) for P in Ps], 0.04)
    ims = [ve.ve(P, B, scale, bg=(150, 150, 150), ss=2) for P in Ps]
    out = Image.new("RGB", (sum(i.width for i in ims), max(i.height for i in ims)), (120, 120, 120))
    x = 0
    for i in ims:
        out.paste(i.convert("RGB"), (x, 0))
        x += i.width
    p = os.path.join(base(k), "rig", f"show_{clip}.png")
    out.save(p)
    print(p)


def main(argv):
    if argv and argv[0] == "show":
        return show(int(argv[1]), argv[2], argv[3].split(","), float(argv[4]) if len(argv) > 4 else 1.6)
    only = int(argv[0]) if argv else 0
    sk2, info2, cl2, fr2, t2, iou2 = xuat_dang2()
    if only == 2:
        return
    xuat_dang1(sk2, info2, cl2, fr2)


if __name__ == "__main__":
    main(sys.argv[1:])
