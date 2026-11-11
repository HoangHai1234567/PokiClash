# -*- coding: utf-8 -*-
"""tm03 (dòng Nòng Xoáy, lô 10 tướng đảo Thủy): rig dựng bằng mã theo cách lai (DAC_TA mục 5) trên thư viện quai/.

Thân chính cắt từ concept (tm03_lai.py, tm03_ghep.py: inbox/tm03_<k>/lai/), mảnh GPT cho phần tách / bị che (inbox/tm03_<k>/manh/).
Dạng 1: quả bóng thân (đầu liền thân, hàm dưới là vùng lưới), đuôi GPT vẽ duỗi cuộn xoắn bằng chuỗi xương (khớp đường xoắn của
concept), bốn chân GPT ngắn mập (IK bám đất), lòng miệng + lưỡi GPT thuộc hàm dưới, mí nhắm.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm03.py rig 1      dạng 1 đứng riêng (chưa tiến hóa)
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm03.py rig 2
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm03.py all        dạng 2 rồi dạng 1 + tiến hóa
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

from quai import anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat  # noqa: E402
from quai.hoat import Clip, LoXo, DayMem, an_hien, bao, chuoi_song, cv, ease, lui, rung, song  # noqa: E402
from quai.khung import Dat, Pose  # noqa: E402

CODE = "tm03"
S = 0.72                      # px concept -> px rig (atlas)


def base(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}")


class Conv:
    """đổi toạ độ concept (px, y xuống) -> rig (y lên, gốc ở chân)."""

    def __init__(self, gx, gy, s=S):
        self.gx, self.gy, self.s = gx, gy, s

    def __call__(self, x, y=None):
        if y is None:
            P = np.asarray(x, float).reshape(-1, 2)
            return np.stack([(P[:, 0] - self.gx) * self.s, (self.gy - P[:, 1]) * self.s], 1)
        return ((x - self.gx) * self.s, (self.gy - y) * self.s)


def img_scaled(path, f):
    im = Image.open(path).convert("RGBA")
    if abs(f - 1) > 1e-6:
        im = im.resize((max(2, int(round(im.width * f))), max(2, int(round(im.height * f)))), Image.LANCZOS)
    return anh.loang_mau(im)


def ellipse(x0, y0, x1, y1, n=40):
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    return np.stack([cx + rx * np.cos(a), cy + ry * np.sin(a)], 1)


def to_img(poly, x0, y0, f=S):
    """đa giác toạ độ concept -> toạ độ ảnh lớp (ảnh cắt tại x0, y0 rồi co f)."""
    P = np.asarray(poly, float)
    return [((p[0] - x0) * f, (p[1] - y0) * f) for p in P]


def leg_joints(part):
    """hông, gối, cổ chân (px ảnh) của ảnh chân đứng: trọng tâm các dải ngang 0–30 %, 45–60 %, 72–82 % chiều cao hình."""
    a = np.asarray(part)[..., 3] > 128
    ys, xs = np.nonzero(a)
    y0, y1 = ys.min(), ys.max()
    out = []
    for lo, hi in ((0.05, 0.30), (0.45, 0.60), (0.72, 0.82)):
        m = (ys >= y0 + lo * (y1 - y0)) & (ys <= y0 + hi * (y1 - y0))
        out.append((float(xs[m].mean()), float(ys[m].mean())))
    out[0] = (out[0][0], float(y0 + 0.22 * (y1 - y0)))
    return np.array(out), float(y1)


def tron_ke(W, ke, cap=0.9):
    """không đỉnh mềm nào bám cứng 100 % một xương: phần trọng số vượt cap của xương có trong ke chuyển sang xương kề ke[xương]."""
    for d in W:
        for b, w in list(d.items()):
            if w > cap and b in ke:
                d[b] = cap
                d[ke[b]] = d.get(ke[b], 0.0) + (w - cap)
    return trongso.chuan(W, 4)


# ---------------------------------------------------------------- đuôi cuộn
def centerline(p, Lp, n=600):
    x0, y0, h0, s_lead, r0, q = p
    s = np.linspace(0, Lp, n)
    ds = s[1] - s[0]
    u = s / Lp
    w = np.clip(u / max(1e-3, s_lead), 0, 1)
    w = w * w * (3 - 2 * w)
    r = r0 * (1 - q * u)
    kap = w / np.maximum(r, 4.0)
    th = math.radians(h0) + np.concatenate([[0], np.cumsum((kap[1:] + kap[:-1]) / 2 * ds)])
    pts = np.zeros((n, 2))
    pts[0] = (x0, y0)
    for i in range(1, n):
        a = (th[i] + th[i - 1]) / 2
        pts[i] = pts[i - 1] + ds * np.array([math.cos(a), math.sin(a)])
    return pts, th, s


def tail_rig(sk, conv, img_path, fit, parent, n_dot=20, ten="duoi", buoc=None):
    """đuôi: ảnh GPT duỗi thẳng -> dải lưới -> cuộn theo đường xoắn đã khớp (dáng gốc là dáng cuộn, đỉnh đặt đúng chỗ trên đường
    xoắn), chuỗi n_dot xương đặt trên đường xoắn, khoảng cách khớp đều theo góc quay + độ dài. Trả (tên đốt, Luoi, ảnh)."""
    x0, y0, h0, sl, r0, q, lam_t, rho = fit["p"]
    lam_len = lam_t * rho
    Limg = len(fit["prof"]["up"])
    Lp = Limg * lam_len
    pts, th, s = centerline((x0, y0, h0, sl, r0, q), Lp)
    f_img = lam_t * S                                         # ảnh atlas: co theo bề dày
    im = img_scaled(img_path, f_img)
    bb = im.getbbox()
    im = im.crop(bb)
    sk.anh(ten, im)
    L = luoi.luoi_dai(im, n_dot, cot_moi_dot=3, buoc=buoc or 8.0, ten=ten)
    # đỉnh: độ dài dọc trục (px ảnh atlas) -> độ dài trên đường xoắn (px concept); lệch khỏi trục -> lệch theo pháp tuyến
    s_img = L.s
    ax = L.diem_truc(s_img)
    d_img = L.pts[:, 1] - ax[:, 1]
    s_c = s_img / f_img * lam_len
    d_c = d_img / f_img * lam_t
    px = np.interp(s_c, s, pts[:, 0])
    py = np.interp(s_c, s, pts[:, 1])
    tt = np.interp(s_c, s, th)
    nx, ny = -np.sin(tt), np.cos(tt)
    V = conv(np.stack([px + nx * d_c, py + ny * d_c], 1))
    # khớp: chia đều theo f = 0,65 góc quay + 0,35 độ dài
    Th = th - th[0]
    f = 0.8 * Th / max(1e-6, Th[-1]) + 0.2 * s / Lp
    s_lim = min(Lp, s_c.max())
    sj = np.interp(np.linspace(0, f[np.searchsorted(s, s_lim) - 1], n_dot + 1), f, s)
    J = conv(np.stack([np.interp(sj, s, pts[:, 0]), np.interp(sj, s, pts[:, 1])], 1))
    names = sk.chuoi(ten, parent, J)
    W = trongso.chuoi(s_c, list(np.diff(sj)), names, cha=parent, cha_hoa=0.55)
    W = trongso.chuan(W)
    W = tron_ke(W, {names[-1]: names[-2], names[0]: names[1]}, cap=0.88)
    trongso.kiem(W, ten)
    # thứ tự vẽ: ngọn đè lên gốc (vòng trong đè vòng ngoài)
    order = np.argsort(s_c[L.tris].mean(1), kind="stable")
    L.tris = L.tris[order]
    return names, L, sj, W, V


# ---------------------------------------------------------------- dạng 1
def rig1():
    B = base(1)
    lop = json.load(open(os.path.join(B, "lai", "lop.json"), encoding="utf-8"))
    dat = json.load(open(os.path.join(B, "lai", "dat.json"), encoding="utf-8"))
    P = dat["parts"]
    GX, GY = 770.0, float(dat["ground"])
    conv = Conv(GX, GY)
    sk = khung.Sk("tm03_1")
    H_rig = (GY - 282) * S
    info = {"conv": conv, "H": H_rig}
    # --- ảnh
    L0 = lop["lop"]["than"]
    than = img_scaled(os.path.join(B, "lai", "than.png"), S)
    sk.anh("than", than)
    md = os.path.join(B, "manh")
    lm = P["long_mieng"]
    sk.anh("long_mieng", img_scaled(os.path.join(md, "long_mieng.png"), 1.0))
    for mi in ("mi_n", "mi_x"):
        sk.anh(mi, img_scaled(os.path.join(B, "lai", mi + ".png"), S))
    leg_img = {}
    for nm in ("chan_sn", "chan_tn", "chan_tx"):
        t = P[nm]
        if t["img"] not in leg_img:
            f = t["sx"] * S
            im = img_scaled(os.path.join(md, t["img"] + ".png"), f)
            sk.anh(t["img"], im)
            leg_img[t["img"]] = (im, f)
    luoi_im = img_scaled(os.path.join(md, "luoi.png"), lm["sx"] * S * 0.85)
    sk.anh("luoi", luoi_im)
    # --- xương
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("than", "move", *conv(860, 822), goc=90, dai=60, the_gioi=True)
    sk.xuong("bung", "than", *conv(865, 748), goc=90, dai=40, the_gioi=True)
    sk.xuong("hong", "than", *conv(688, 640), goc=150, dai=40, the_gioi=True)
    sk.xuong("dau", "than", *conv(845, 600), goc=40, dai=80, the_gioi=True)
    hinge, snout = np.array(conv(908, 596)), np.array(conv(1085, 612))
    gj = math.degrees(math.atan2(*(snout - hinge)[::-1]))
    sk.xuong("ham", "dau", *hinge, goc=gj, dai=float(np.hypot(*(snout - hinge))), the_gioi=True)
    sk.xuong("mieng_mom", "dau", *conv(1068, 590), goc=0, dai=30, the_gioi=True)
    sk.xuong("mat_n", "dau", *conv(857, 515), goc=90, dai=60, the_gioi=True)
    sk.xuong("mat_x", "dau", *conv(1033, 510), goc=90, dai=50, the_gioi=True)
    # --- đuôi (sau thân)
    duoi, Ld, sj, Wd, Vd = tail_rig(sk, conv, os.path.join(md, "duoi.png"), dat["duoi"], "hong", n_dot=24, buoc=0.02 * H_rig)
    tip = sk.W0[duoi[-1]]
    tipL = sk.bones[sk.bi[duoi[-1]]]["length"]
    ptip = (tip @ np.array([tipL, 0, 1.0]))[:2]
    sk.xuong("mieng", duoi[-1], *ptip, goc=0, dai=30, the_gioi=True)      # chỗ nhả chiêu cast (ngọn đuôi), trục x chĩa phải
    # --- chân: hông, gối, cổ chân đọc trên ảnh; đặt theo dat.json
    legs = {}
    for nm, par in (("chan_sx", "hong"), ("chan_tx", "than"), ("chan_sn", "hong"), ("chan_tn", "than")):
        t = P[nm]
        im, f = leg_img[t["img"]]
        kf = t["sx"] / (f / S)                       # chân xa dùng chung ảnh, co thêm
        orig = Image.open(os.path.join(md, t["img"] + ".png"))
        Jimg, yb = leg_joints(orig)
        c_img = np.array([orig.width / 2, orig.height / 2])
        Jc = np.array([t["cx"], t["cy"]]) + (Jimg - c_img) * t["sx"]
        J = conv(Jc)
        names = sk.chuoi(nm, par, J, khong_ti_le=True)
        dat_leg = Dat(*conv(t["cx"], t["cy"]), ti=kf)
        legs[nm] = {"names": names, "J": J, "dat": dat_leg, "img": t["img"], "foot": J[-1].copy()}
    # --- slot (sau -> trước)
    sk.slot("chan_sx", legs["chan_sx"]["names"][0], legs["chan_sx"]["img"])
    sk.slot("chan_tx", legs["chan_tx"]["names"][0], legs["chan_tx"]["img"])
    sk.slot("duoi", duoi[0], "duoi")
    sk.slot("long_mieng", "ham", "long_mieng")
    sk.slot("than", "than", "than")
    sk.slot("luoi", "ham", "luoi", an=True)
    sk.slot("chan_sn", legs["chan_sn"]["names"][0], legs["chan_sn"]["img"])
    sk.slot("chan_tn", legs["chan_tn"]["names"][0], legs["chan_tn"]["img"])
    sk.slot("mi_x", "mat_x", "mi_x", an=True)
    sk.slot("mi_n", "mat_n", "mi_n", an=True)
    sk.luoi_gan("duoi", "duoi", Ld, Wd, the_gioi=Vd)
    # --- lưới thân: vùng mắt, hàm, đầu, hông, bụng
    x0, y0 = L0["x0"], L0["y0"]
    Lt = luoi.luoi_vung(than, buoc_theo_cao=H_rig, ten="than")
    w, h = than.size
    full = [(0, 0), (w, 0), (w, h), (0, h)]
    vm = lop["lop"]
    reg = [("mat_n", to_img(ellipse(*vm["vung_mat_n"]), x0, y0)),
           ("mat_x", to_img(ellipse(*vm["vung_mat_x"]), x0, y0)),
           ("ham", to_img([(905, 603), (1110, 603), (1110, 700), (975, 712), (912, 650)], x0, y0)),
           ("dau", to_img([(700, 300), (1120, 300), (1120, 596), (905, 596), (760, 575), (700, 540)], x0, y0)),
           ("hong", to_img([(590, 300), (700, 300), (700, 880), (590, 880)], x0, y0)),
           ("bung", to_img([(735, 700), (1010, 700), (1010, 840), (735, 840)], x0, y0)),
           ("than", full)]
    Wt = trongso.vung(Lt, reg, dai_hoa=0.07 * H_rig)
    Wt = trongso.lam_tron(Lt, Wt, 2)
    Wt = tron_ke(Wt, {"bung": "than", "dau": "than", "hong": "than", "than": "dau", "ham": "dau", "mat_n": "dau", "mat_x": "dau"})
    trongso.kiem(Wt, "than")
    sk.luoi_gan("than", "than", Lt, Wt, dat=Dat(*conv(x0, y0), neo=(0, 0)))
    # --- lòng miệng: thuộc hàm dưới (hàng dưới 100 % hàm, góc sau-trên chỉ hơi bám đầu)
    im = sk.images["long_mieng"]
    Lm = luoi.luoi_vung(im, 0.015 * H_rig / (lm["sx"] * S), 0.02 * H_rig / (lm["sx"] * S), ten="long_mieng")
    u = Lm.pts[:, 0] / im.width
    v = Lm.pts[:, 1] / im.height
    wh = np.clip(0.3 + 0.95 * v + 0.25 * u, 0, 1)
    Wm = [{"ham": float(a), "dau": float(1 - a)} if a < 0.999 else {"ham": 1.0} for a in wh]
    sk.luoi_gan("long_mieng", "long_mieng", Lm, Wm, dat=Dat(*conv(lm["cx"], lm["cy"]), goc=lm["r"], ti=(lm["sx"] * S, lm["sy"] * S)))
    # --- lưỡi (chỉ hiện khi chết, trúng đòn): dải 3 đốt, con của hàm, thè ra phía trước-dưới
    p_root = np.array(conv(lm["cx"] - 8, lm["cy"] + 12))
    dat_l = Dat(*p_root, goc=-32, neo=(0.05, 0.5))
    Ll = luoi.luoi_dai(luoi_im, 3, buoc=0.02 * H_rig, ten="luoi")
    lu = sk.chuoi("luoi", "ham", dat_l.ra(Ll.khop(3), *luoi_im.size))
    sk.luoi_gan("luoi", "luoi", Ll, trongso.chuoi(Ll.s, Ll.truc[1][-1] / 3, lu, cha="ham", cha_hoa=0.5), dat=dat_l)
    # --- mí nhắm: mảnh cứng trên xương mắt
    for mi in ("mi_n", "mi_x"):
        g = lop["lop"][mi]
        sk.manh(mi, mi, Dat(*conv(g["x0"], g["y0"]), neo=(0, 0)))
    # --- chân: lưới vùng, trọng số chiếu lên chuỗi hông-gối-cổ chân, gốc hoà vào thân
    for nm, d in legs.items():
        im = sk.images[d["img"]]
        Lc = luoi.luoi_vung(im, buoc_theo_cao=H_rig / max(0.5, d["dat"].sx), ten=nm)
        V = d["dat"].ra(Lc.pts, im.width, im.height)
        par = sk.bones[sk.bi[d["names"][0]]]["parent"]
        Wc = trongso.chuoi_chieu(V, d["J"], d["names"], cha=par, cha_hoa=0.6)
        Wc = trongso.lam_tron(Lc, trongso.chuan(Wc), 1)
        Wc = tron_ke(Wc, {d["names"][1]: d["names"][0], d["names"][0]: par})
        sk.luoi_gan(nm, d["img"], Lc, Wc, dat=d["dat"])
    for e, m in (("trung", "bong bóng rời miệng (đòn thường)"), ("phun", "đuôi quất nhả vòng nước (VFX bám xương mieng ở ngọn đuôi)"),
                 ("het_phun", "hết nhả"), ("gam", "đáp xuống, xoáy mở dưới chân đối thủ"), ("het_gam", "hết chiêu cuối")):
        sk.su_kien(e, m)
    info.update({"duoi": duoi, "lu": lu, "legs": legs, "sj": sj})
    return sk, info


def clips1(sk, info):
    duoi, lu, legs = info["duoi"], info["lu"], info["legs"]
    n = len(duoi)
    k = 1.0
    tail_mem = [LoXo(duoi[8:], k=list(np.linspace(520, 260, n - 8)), damp=0.6, maxang=10)]
    mem = tail_mem + [DayMem(lu, k0=0.24, k1=0.08, zeta=0.5, lim=(18, 28), luc=lambda t, i: np.array([0.0, -1100.0 * (1 + i)]))]

    def curl(P, a, start=0, ramp=6):
        """cuộn thêm (a < 0: chặt lại, a > 0: lỏng ra) đều trên các đốt, tăng dần qua ramp đốt đầu."""
        for i, b in enumerate(duoi[start:], start):
            P.rot(b, a * min(1.0, (i - start + 1) / ramp))

    def feet(P):
        W = sk.the_gioi(P)
        for nm, d in legs.items():
            tgt = (W["move"] @ np.array([d["foot"][0], d["foot"][1], 1.0]))[:2]
            hoat.ik_hai_doan(sk, P, d["names"][0], d["names"][1], tgt)

    def mieng_post(t, P):
        """xương mieng (ngọn đuôi) luôn chĩa trục x sang phải (hướng đối thủ) để VFX bắn đúng hướng."""
        W = sk.the_gioi(P)
        par = W[duoi[-1]]
        ang = math.degrees(math.atan2(par[1, 0], par[0, 0]))
        b0 = sk.bones[sk.bi["mieng"]]["rot"]
        P.rot("mieng", -(ang + b0))

    def nen(P, tt, amp=1.0):
        """idle: nhún hai lần mỗi 2 s, mắt nảy trễ, đuôi thở (cuộn lỏng / chặt) và sóng nhẹ từ gốc ra ngọn."""
        b = 0.5 - 0.5 * math.cos(2 * math.pi * tt / 1.0)            # 0..1, hai lần mỗi vòng 2 s
        b2 = 0.5 - 0.5 * math.cos(2 * math.pi * (tt - 0.1) / 1.0)
        P.scale("than", 1 + 0.025 * b * amp, 1 - 0.035 * b * amp)
        P.move("than", 0, -2.0 * b * amp)
        P.rot("dau", 1.6 * song(tt, 2.0, 0.6) * amp)
        P.scale("mat_n", 1.0, 1 + 0.05 * b2 * amp)
        P.scale("mat_x", 1.0, 1 + 0.05 * (0.5 - 0.5 * math.cos(2 * math.pi * (tt - 0.16) / 1.0)) * amp)
        P.rot("mat_n", 1.5 * song(tt, 2.0, 1.2) * amp)
        P.rot("mat_x", 2.0 * song(tt, 2.0, 1.6) * amp)
        P.rot("hong", 1.2 * song(tt, 2.0, 0.3) * amp)
        curl(P, 0.9 * song(tt, 2.0, 0.9) * amp)
        chuoi_song(P, duoi, tt, 2.0, list(np.linspace(1.0, 2.6, n) * amp), tre=0.05, ngon_dan=False)

    def idle_fn(t, P):
        nen(P, t)
        pf = cv(t, [(0, 0), (1.18, 0), (1.32, 1, "out"), (1.5, 0.85), (1.66, 0, "io"), (2.0, 0)])     # phồng họng
        P.scale("bung", 1 + 0.07 * pf, 1 + 0.10 * pf)
        P.rot("ham", -3 * pf)
        an_hien(P, "mi_n", t, [(0.62, 0.74)])
        an_hien(P, "mi_x", t, [(0.63, 0.75)])
        feet(P)

    def appear_fn(t, P, D=1.2):
        g = cv(t, [(0, 0.02), (0.42, 1.12, "out"), (0.6, 0.95, "io"), (0.8, 1.0, "io"), (D, 1.0)])
        P.scale("move", g, g)
        a = cv(t, [(0, 0), (0.12, 1)])
        for s in sk.slots:
            if s["alpha"] > 0:
                P.alpha[s["name"]] = a
        nen(P, lui(t, D), ease((t - 0.5) / 0.6))
        curl(P, 14 * cv(t, [(0, 1), (0.35, 1), (0.95, 0, "out"), (D, 0)]))          # đuôi bung ra rồi cuộn lại
        P.rot("dau", 8 * cv(t, [(0, 0), (0.7, 0), (0.85, 1, "out"), (1.05, 0, "io"), (D, 0)]))
        P.rot("ham", -20 * cv(t, [(0, 0), (0.7, 0), (0.85, 1, "out"), (1.05, 0, "io"), (D, 0)]))
        feet(P)

    def attack_fn(t, P, D=0.9, H=0.42):
        lean = cv(t, [(0, 0), (0.3, 1, "io"), (0.36, 1.08), (H, -1.0, "in"), (0.47, -1.1), (0.64, -0.9, "io"), (D, 0, "io")])
        nen(P, lui(t, D), 1 - 0.7 * bao(t, 0.1, 0.8, 0.2, 0.25))
        P.rot("than", 6 * lean)
        P.rot("dau", 5 * lean)
        pf = cv(t, [(0, 0), (0.3, 1, "io"), (H - 0.02, 1.05), (H + 0.04, 0, "out"), (D, 0)])
        P.scale("bung", 1 + 0.08 * pf, 1 + 0.12 * pf)
        P.rot("ham", -cv(t, [(0, 0), (0.3, 4, "io"), (H - 0.03, 6), (H, 30, "out"), (0.6, 24), (D, 0, "io")]))
        P.scale("than", cv(t, [(0, 1), (0.3, 0.96), (H, 1.08, "out"), (0.55, 1.0), (D, 1)]),
                cv(t, [(0, 1), (0.3, 1.05), (H, 0.93, "out"), (0.55, 1.0), (D, 1)]))
        curl(P, 6 * cv(t, [(0, 0), (0.3, -1, "io"), (H, 1.2, "out"), (0.65, 0.3), (D, 0, "io")]))
        feet(P)

    per = sum(abs(sk.bones[sk.bi[b]]["rot"]) for b in duoi[1:]) / (n - 1)      # góc cuộn TB mỗi đốt ở dáng gốc

    def uncurl(P, u):
        """duỗi cuộn đuôi một phần u (0 = cuộn như gốc, 1 = thẳng; âm = cuộn chặt hơn)."""
        for i, b in enumerate(duoi[1:], 1):
            P.rot(b, u * per * min(1.0, i / 4))

    def cast_fn(t, P, D=1.1, H=0.55, E=0.85):
        """Đuôi Xoáy: cuộn chặt lấy đà, vung đuôi thành vòm qua lưng, quất ngọn ra trước trên đầu (nhả vòng nước ở ngọn đuôi)."""
        nen(P, lui(t, D), 1 - 0.85 * bao(t, 0.08, 1.0, 0.15, 0.2))
        u = cv(t, [(0, 0), (0.36, -0.07, "io"), (0.47, 0.5, "out"), (H, 0.38, "in"), (0.62, 0.34), (E, 0.4, "io"), (D, 0, "io")])
        uncurl(P, u)
        sw = cv(t, [(0, 0), (0.36, 8, "io"), (0.47, -46, "out"), (H, -64, "in"), (0.6, -67), (E, -58, "io"), (D, 0, "io")])
        P.rot(duoi[0], sw)
        P.rot("than", cv(t, [(0, 0), (0.36, 4, "io"), (H, -6, "in"), (E, -3), (D, 0, "io")]))
        P.scale("than", cv(t, [(0, 1), (0.36, 1.04), (H, 0.97), (D, 1)]), cv(t, [(0, 1), (0.36, 0.95), (H, 1.05), (D, 1)]))
        P.rot("ham", -cv(t, [(0, 0), (0.36, 4, "io"), (H, 14, "out"), (E, 10), (D, 0, "io")]) - 2 * rung(t, H + 0.04, E))
        P.rot("dau", cv(t, [(0, 0), (0.36, 3, "io"), (H, -2), (D, 0, "io")]) + 2 * rung(t, H + 0.04, E))
        feet(P)

    def skill_fn(t, P, D=1.8, H=0.95, E=1.45):
        nen(P, lui(t, D), 1 - 0.9 * bao(t, 0.1, 1.7, 0.2, 0.3))
        up = cv(t, [(0, 0), (0.55, 0), (0.75, 1, "out"), (0.88, 0.9), (H, 0, "in"), (D, 0)])
        P.move("move", 0, 46 * up)
        sq = cv(t, [(0, 0), (0.5, 1, "io"), (0.62, -0.6, "out"), (0.88, -0.3), (H, 1.2, "in"), (1.05, 0.5, "out"), (E, 0.3), (D, 0, "io")])
        P.scale("than", 1 + 0.07 * max(sq, 0) - 0.04 * min(sq, 0), 1 - 0.1 * max(sq, 0) + 0.07 * min(sq, 0))
        # đuôi quay như chân vịt: sóng cuộn chạy nhanh dọc đuôi (chu kỳ 0,24 s) trong lúc giữ chiêu
        wv = bao(t, 0.5, E + 0.1, 0.15, 0.3)
        for i, b in enumerate(duoi):
            P.rot(b, wv * 9 * math.sin(2 * math.pi * (t / 0.24 - i * 0.11)))
        curl(P, -5 * cv(t, [(0, 0), (0.5, 1, "io"), (H, 1), (E, 0.6), (D, 0, "io")]))
        P.rot("ham", -cv(t, [(0, 0), (0.5, 5), (H, 26, "out"), (E, 22), (D, 0, "io")]) - 3 * rung(t, H + 0.04, E))
        P.rot("than", 2.0 * rung(t, H + 0.04, E))
        P.rot("dau", cv(t, [(0, 0), (0.5, -4), (H, 6, "out"), (E, 5), (D, 0, "io")]))
        feet(P)

    def hit_fn(t, P, D=0.6):
        hd = cv(t, [(0, 0), (0.07, 1, "out"), (0.2, 0.55, "io"), (0.42, -0.12, "io"), (D, 0, "io")])
        nen(P, lui(t, D), ease((t - 0.25) / 0.35))
        P.rot("than", 11 * hd)
        P.move("move", -12 * hd, 0)
        P.scale("than", 1 - 0.05 * hd, 1 + 0.06 * hd)
        P.rot("ham", -12 * hd)
        P.rot("dau", 6 * hd)
        an_hien(P, "mi_n", t, [(0.03, 0.32)])
        an_hien(P, "mi_x", t, [(0.03, 0.32)])
        for i, b in enumerate(duoi):          # sóng chạy từ ngọn về gốc
            j = n - 1 - i
            P.rot(b, 5 * cv(t, [(0, 0), (0.07 + 0.012 * j, 1, "out"), (0.32 + 0.01 * j, -0.3, "io"), (D, 0, "io")]))
        feet(P)

    def die_fn(t, P, D=1.6):
        P.rot("than", cv(t, [(0, 0), (0.07, 10, "out"), (0.3, 4), (0.75, 10, "io"), (1.1, 78, "in"), (1.2, 72, "out"), (D, 74)]))
        P.move("move", cv(t, [(0, 0), (0.85, 0), (1.15, -26, "in"), (D, -26)]), 0)
        P.rot("ham", -cv(t, [(0, 0), (0.07, 18, "out"), (0.3, 12), (0.6, 26, "io"), (D, 26)]))
        P.rot("dau", cv(t, [(0, 0), (0.07, 8, "out"), (0.5, -4, "io"), (0.75, 4, "io"), (D, 4)]))
        an_hien(P, "mi_n", t, [(0.04, D + 1)])
        an_hien(P, "mi_x", t, [(0.04, D + 1)])
        P.alpha["luoi"] = cv(t, [(0, 0), (0.25, 0), (0.32, 1)])
        for i, b in enumerate(lu):
            P.rot(b, cv(t, [(0, 0), (0.3, 0), (0.6, -14 - 6 * i, "out"), (D, -18 - 6 * i)]))
        curl(P, cv(t, [(0, 0), (0.07, -4, "out"), (0.8, 6, "io"), (D, 8)]))
        a = cv(t, [(0, 1), (1.22, 1), (1.56, 0, "io"), (D, 0)])
        for s in sk.slots:
            if s["alpha"] > 0 or s["name"] in ("mi_n", "mi_x", "luoi"):
                P.alpha[s["name"]] = min(P.alpha.get(s["name"], s["alpha"]), a)
        if t < 0.85:
            feet(P)

    def hit_tongue(t, P):
        pass

    out = [Clip("appear", 1.2, appear_fn, mem=mem, post=mieng_post),
           Clip("idle", 2.0, idle_fn, loop=True, mem=mem, post=mieng_post),
           Clip("attack", 0.9, attack_fn, ev=[(0.42, "trung", "")], mem=mem, post=mieng_post),
           Clip("cast", 1.1, cast_fn, ev=[(0.55, "phun", ""), (0.85, "het_phun", "")], mem=mem, post=mieng_post),
           Clip("skill", 1.8, skill_fn, ev=[(0.95, "gam", ""), (1.45, "het_gam", "")], mem=mem, post=mieng_post),
           Clip("hit", 0.6, hit_fn, mem=mem, post=mieng_post),
           Clip("die", 1.6, die_fn, mem=mem, post=mieng_post)]
    return out


# ---------------------------------------------------------------- so concept
def so_concept(sk, frame0, k, conv, ra, y_chan=None):
    """khung 0 idle vẽ đúng tỉ lệ concept, đặt cạnh concept; IoU mặt nạ."""
    B = base(k)
    cfile = {1: "L1_duyet.png", 2: "L1_concept_3.png"}[k]
    ref = Image.open(os.path.join(B, "tai_ve", cfile)).convert("RGB")
    Wc, Hc = ref.size
    box = (-conv.gx * conv.s, (conv.gy - Hc) * conv.s, (Wc - conv.gx) * conv.s, conv.gy * conv.s)
    ve = soi.Ve(sk)
    im = ve.ve(frame0, box, 1.0 / conv.s, ss=1)
    im = im.resize((Wc, Hc))
    a = np.asarray(im)[..., 3] > 100
    rr = np.asarray(ref).astype(int)
    fg = ~((rr.min(2) > 235) & (rr.max(2) - rr.min(2) < 20))
    iou = float((a & fg).sum() / max(1, (a | fg).sum()))
    iou2 = None
    if y_chan:                      # bỏ dải chân (chân cố ý đổi ngắn, mập hơn concept theo điều phối)
        a2, f2 = a[:int(y_chan)], fg[:int(y_chan)]
        iou2 = float((a2 & f2).sum() / max(1, (a2 | f2).sum()))
    rgb = Image.new("RGB", (Wc, Hc), (255, 255, 255))
    rgb.paste(im, (0, 0), im)
    diff = np.full((Hc, Wc, 3), 255, np.uint8)
    diff[fg & ~a] = (230, 60, 60)
    diff[~fg & a] = (60, 110, 230)
    diff[fg & a] = (205, 205, 205)
    side = np.concatenate([np.asarray(ref), np.asarray(rgb), diff], 1)
    out = Image.fromarray(side)
    d = __import__("PIL.ImageDraw", fromlist=["ImageDraw"]).Draw(out)
    txt = f"khung 0 idle (rig)   IoU mat na voi concept = {iou:.3f}" + (f"   (tru dai chan y>{y_chan}: {iou2:.3f})" if iou2 else "")
    d.text((Wc + 20, 20), txt, fill=(0, 0, 0), font=anh.font(28))
    out.save(ra)
    print(f"  so_concept: IoU khung 0 idle / concept = {iou:.3f}" + (f", trừ dải chân (y > {y_chan}): {iou2:.3f}" if iou2 else "") + f" -> {ra}")
    return iou


def uon_thu(sk, info, ra):
    P = Pose()
    for i, b in enumerate(info["duoi"]):
        P.rot(b, 10)
    P.rot("ham", -28)
    P.rot("dau", 10)
    P.scale("bung", 1.1, 1.14)
    for nm, d in info["legs"].items():
        P.rot(d["names"][0], 20)
        P.rot(d["names"][1], -35)
    ve = soi.Ve(sk)
    B = soi._union([ve.bao(P)], 0.05)
    ve.ve(P, B, 1.4, bg=(150, 150, 150), ss=2, luoi=True, mau_luoi=(10, 10, 10, 110)).convert("RGB").save(ra)


def main_rig1(sk2=None, cl2=None, fr2=None):
    """dạng 1; có sk2 (dạng 2 đã dựng) thì gộp rig và thêm clip evolve (tiến hóa nối liền) trước khi xuất."""
    t0 = time.time()
    sk, info = rig1()
    cl = clips1(sk, info)
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    print(f"dạng 1: dựng + nướng {time.time() - t0:.1f} s")
    ra = os.path.join(base(1), "rig")
    os.makedirs(ra, exist_ok=True)
    iou = so_concept(sk, fr["idle"][0], 1, info["conv"], os.path.join(ra, "so_concept.png"), y_chan=715)
    can = [("can_mieng_attack", "attack", 0.47, "ham", 70), ("can_duoi_cast", "cast", 0.6, duoi_mid(info), 150),
           ("can_mi_hit", "hit", 0.1, "dau", 90), ("can_chan_skill", "skill", 0.96, "than", 120)]
    if sk2 is None:
        tong = xuat.xuat_het(sk, cl, ra, "tm03_1", "Nòng Xoáy (dạng 1, chưa gộp tiến hóa)", frames=fr, dang=1, so_dang=2,
                             dung_yen=("attack", "cast", "skill"), ma_goc=3230, can=can)
    else:
        ve1, ve2 = soi.Ve(sk), soi.Ve(sk2)
        hA, hB = soi.chieu_cao(ve1, fr["idle"][0]), soi.chieu_cao(ve2, fr2["idle"][0])
        M = tienhoa.gop(sk, sk2)
        duoi = info["duoi"]

        def gong(t, P):   # Nòng Xoáy gồng: đuôi quay tít, cuộn chặt, thân nén, ngửa đầu há miệng
            sq = cv(t, [(0, 0), (0.3, -0.06), (0.5, 0.07, "out"), (1.0, 0.05), (1.3, 0.0)])
            P.scale("than", 1 - 0.5 * sq, 1 + sq)
            wv = bao(t, 0.15, 1.3, 0.2, 0.15)
            for i, b in enumerate(duoi):
                P.rot(b, wv * 10 * math.sin(2 * math.pi * (t / 0.2 - i * 0.12)) - 4 * wv)
            P.rot("dau", cv(t, [(0, 0), (0.3, -4), (0.7, 9, "out"), (1.3, 11)]) + 1.5 * rung(t, 0.55, 1.3))
            P.rot("ham", -cv(t, [(0, 0), (0.5, 6), (1.0, 16, "out"), (1.3, 18)]))
            P.scale("bung", 1 + 0.08 * bao(t, 0.4, 1.3, 0.3, 0.1), 1 + 0.1 * bao(t, 0.4, 1.3, 0.3, 0.1))

        def gam(t, P, fl):  # Ếch Lốc ộp gầm: túi kêu phồng, há miệng, chồm nhẹ
            P.scale("n_tui", 1 + 0.45 * fl, 1 + 0.5 * fl)
            P.rot("n_ham", -26 * fl)
            P.rot("n_dau", 7 * fl)
            P.rot("n_nguc", 3 * fl)

        memM = cl[1].mem + tienhoa.doi_ten_mem(cl2[1].mem)
        ev = tienhoa.clip_tien_hoa(M, sk, sk2, fr2["idle"][0], tiB=hA / hB, fnA=gong, fnB=gam, mem=memM)
        clM = cl + [ev]
        frM = dict(fr)
        frM["evolve"] = hoat.nuong(M, ev)
        _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, fr2["idle"][0], hA / hB)
        tong = xuat.xuat_het(M, clM, ra, "tm03_1", "Nòng Xoáy (dạng 1, gộp tiến hóa sang Ếch Lốc)", frames=frM, dang=1, so_dang=2,
                             dung_yen=("attack", "cast", "skill"), ma_goc=3230, tran_mb=0.5,
                             noi_them={"evolve": s_ev + f" (dạng sau co {hA / hB:.3f} trong rig gộp)"},
                             can=can + [("can_tien_hoa", "evolve", 1.3, "than", 260)])
    uon_thu(sk, info, os.path.join(ra, "uon_thu.png"))
    return sk, info, cl, fr, iou


def duoi_mid(info):
    return info["duoi"][len(info["duoi"]) // 2]


# ---------------------------------------------------------------- dạng 2: Ếch Lốc
S2 = 0.62


def rig2(s2=None, thua=1.0):
    """dạng 2. s2: tỉ lệ px concept -> rig (mặc định S2); thua: hệ số thưa lưới (bản gộp trong rig tiến hóa của dạng 1 dùng
    s2 nhỏ, lưới thưa hơn cho nhẹ: hình bản gộp chỉ hiện trong clip evolve)."""
    S2 = s2 or globals()["S2"]
    B = base(2)
    lop = json.load(open(os.path.join(B, "lai", "lop.json"), encoding="utf-8"))
    dat = json.load(open(os.path.join(B, "lai", "dat.json"), encoding="utf-8"))
    P = dat["parts"]
    GX, GY = 760.0, float(dat["ground"])
    conv = Conv(GX, GY, S2)
    sk = khung.Sk("tm03_2")
    H_rig = (GY - 214) * S2
    info = {"conv": conv, "H": H_rig}
    lv = lop["lop"]
    md = os.path.join(B, "manh")
    # ảnh
    for nm in ("than", "chan_sn", "chan_tn", "mi_n", "mi_x"):
        sk.anh(nm, img_scaled(os.path.join(B, "lai", nm + ".png"), S2))
    lm = P["long_mieng"]
    sk.anh("long_mieng", img_scaled(os.path.join(md, "long_mieng.png"), 1.0))
    for nm in ("chan_sx", "chan_tx"):
        t = P[nm]
        sk.anh(t["img"], img_scaled(os.path.join(md, t["img"] + ".png"), t["sx"] * S2))
    luoi_im = img_scaled(os.path.join(md, "luoi.png"), lm["sx"] * S2 * 0.8)
    sk.anh("luoi", luoi_im)
    # xương
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("hong", "move", *conv(450, 560), goc=10, dai=80, the_gioi=True)
    sk.xuong("lung", "hong", *conv(640, 480), goc=0, dai=80, the_gioi=True)
    sk.xuong("nguc", "lung", *conv(820, 470), goc=10, dai=70, the_gioi=True)
    sk.xuong("dau", "nguc", *conv(905, 400), goc=8, dai=200, the_gioi=True)
    hinge, snout = np.array(conv(898, 422)), np.array(conv(1196, 434))
    gj = math.degrees(math.atan2(*(snout - hinge)[::-1]))
    sk.xuong("ham", "dau", *hinge, goc=gj, dai=float(np.hypot(*(snout - hinge))), the_gioi=True)
    sk.xuong("mieng", "dau", *conv(1196, 404), goc=0, dai=40, the_gioi=True)      # chỗ ộp nhả sóng âm (cast), trục x chĩa phải
    sk.xuong("tui", "nguc", *conv(905, 505), goc=-90, dai=120, the_gioi=True)
    sk.xuong("la", "lung", *conv(620, 335), goc=0, dai=150, the_gioi=True)
    sk.xuong("la2", "la", *conv(780, 325), goc=0, dai=110, the_gioi=True)
    sk.xuong("sung_n", "dau", *conv(925, 268), goc=125, dai=70, the_gioi=True)
    sk.xuong("sung_x", "dau", *conv(1100, 268), goc=110, dai=60, the_gioi=True)
    legs = {}
    # chân gần cắt từ concept: hông / vai, gối / khuỷu, cổ chân / cổ tay đọc trên concept
    JC = {"chan_sn": [(430, 470), (385, 622), (410, 712)], "chan_tn": [(652, 505), (664, 616), (690, 712)]}
    for nm, par in (("chan_sn", "hong"), ("chan_tn", "nguc")):
        J = conv(np.array(JC[nm], float))
        names = sk.chuoi(nm, par, J)
        g = lv[nm]
        legs[nm] = {"names": names, "J": J, "dat": Dat(*conv(g["x0"], g["y0"]), neo=(0, 0)), "img": nm, "foot": J[-1].copy()}
    for nm, par in (("chan_sx", "hong"), ("chan_tx", "nguc")):
        t = P[nm]
        orig = Image.open(os.path.join(md, t["img"] + ".png"))
        Jimg, _ = leg_joints(orig)
        c_img = np.array([orig.width / 2, orig.height / 2])
        Jc = np.array([t["cx"], t["cy"]]) + (Jimg - c_img) * t["sx"]
        J = conv(Jc)
        names = sk.chuoi(nm, par, J)
        legs[nm] = {"names": names, "J": J, "dat": Dat(*conv(t["cx"], t["cy"])), "img": t["img"], "foot": J[-1].copy()}
    # slot sau -> trước
    sk.slot("chan_sx", legs["chan_sx"]["names"][0], legs["chan_sx"]["img"])
    sk.slot("chan_tx", legs["chan_tx"]["names"][0], legs["chan_tx"]["img"])
    sk.slot("long_mieng", "ham", "long_mieng")
    sk.slot("than", "lung", "than")
    sk.slot("luoi", "ham", "luoi", an=True)
    sk.slot("chan_sn", legs["chan_sn"]["names"][0], "chan_sn")
    sk.slot("chan_tn", legs["chan_tn"]["names"][0], "chan_tn")
    sk.slot("mi_x", "dau", "mi_x", an=True)
    sk.slot("mi_n", "dau", "mi_n", an=True)
    # lưới thân: vùng sừng, hàm, đầu, túi kêu, lá súng (hai nửa), ngực, lưng, hông
    than = sk.images["than"]
    g = lv["than"]
    x0, y0 = g["x0"], g["y0"]
    Lt = luoi.luoi_vung(than, buoc_theo_cao=H_rig * thua, ten="than")
    w, h = than.size
    full = [(0, 0), (w, 0), (w, h), (0, h)]

    def bb(nm, pad=4):
        a = lv["vung_" + nm]
        return to_img([(a[0] - pad, a[1] - pad), (a[2] + pad, a[1] - pad), (a[2] + pad, a[3] + pad), (a[0] - pad, a[3] + pad)], x0, y0, S2)
    pad_poly = np.array(lv["da_giac_la"], float)
    la1 = [p for p in pad_poly if p[0] < 700] + [(700, 200), (700, 420)]
    la2 = [p for p in pad_poly if p[0] >= 700] + [(700, 420), (700, 200)]
    from quai.anh import bao_loi
    reg = [("sung_n", bb("sung_n")), ("sung_x", bb("sung_x")),
           ("ham", to_img([(893, 428), (1210, 428), (1210, 475), (1100, 492), (950, 488), (898, 460)], x0, y0, S2)),
           ("dau", to_img([(858, 205), (1220, 205), (1220, 427), (893, 427), (862, 445), (845, 330)], x0, y0, S2)),
           ("tui", to_img(lv["da_giac_tui"], x0, y0, S2)),
           ("la", to_img(bao_loi(np.array(la1, float)), x0, y0, S2)),
           ("la2", to_img(bao_loi(np.array(la2, float)), x0, y0, S2)),
           ("nguc", to_img([(735, 200), (900, 200), (900, 700), (735, 700)], x0, y0, S2)),
           ("hong", to_img([(300, 200), (540, 200), (540, 700), (300, 700)], x0, y0, S2)),
           ("lung", full)]
    Wt = trongso.vung(Lt, reg, dai_hoa=0.06 * H_rig)
    Wt = trongso.lam_tron(Lt, Wt, 2)
    Wt = tron_ke(Wt, {"hong": "lung", "lung": "nguc", "nguc": "lung", "dau": "nguc", "tui": "nguc", "la": "lung",
                      "la2": "la", "sung_n": "dau", "sung_x": "dau", "ham": "dau"})
    trongso.kiem(Wt, "than")
    sk.luoi_gan("than", "than", Lt, Wt, dat=Dat(*conv(x0, y0), neo=(0, 0)))
    # lòng miệng thuộc hàm dưới
    im = sk.images["long_mieng"]
    Lm = luoi.luoi_vung(im, 0.015 * H_rig / (lm["sx"] * S2), 0.02 * H_rig / (lm["sx"] * S2), ten="long_mieng")
    u = Lm.pts[:, 0] / im.width
    v = Lm.pts[:, 1] / im.height
    wh = np.clip(0.3 + 0.95 * v + 0.2 * u, 0, 1)
    Wm = [{"ham": float(a), "dau": float(1 - a)} if a < 0.999 else {"ham": 1.0} for a in wh]
    sk.luoi_gan("long_mieng", "long_mieng", Lm, Wm, dat=Dat(*conv(lm["cx"], lm["cy"]), goc=lm["r"], ti=(lm["sx"] * S2, lm["sy"] * S2)))
    # lưỡi (chết): dải 3 đốt con của hàm
    p_root = np.array(conv(lm["cx"] - 40, lm["cy"] + 8))
    dat_l = Dat(*p_root, goc=-18, neo=(0.05, 0.5))
    Ll = luoi.luoi_dai(luoi_im, 3, buoc=0.02 * H_rig, ten="luoi")
    lu = sk.chuoi("luoi", "ham", dat_l.ra(Ll.khop(3), *luoi_im.size))
    sk.luoi_gan("luoi", "luoi", Ll, trongso.chuoi(Ll.s, Ll.truc[1][-1] / 3, lu, cha="ham", cha_hoa=0.5), dat=dat_l)
    for mi in ("mi_n", "mi_x"):
        gm = lv[mi]
        sk.manh(mi, mi, Dat(*conv(gm["x0"], gm["y0"]), neo=(0, 0)))
    # chân: lưới vùng, trọng số chiếu lên chuỗi, gốc hoà vào thân
    for nm, d in legs.items():
        im = sk.images[d["img"]]
        Lc = luoi.luoi_vung(im, buoc_theo_cao=H_rig * thua / max(0.5, d["dat"].sx), ten=nm)
        V = d["dat"].ra(Lc.pts, im.width, im.height)
        par = sk.bones[sk.bi[d["names"][0]]]["parent"]
        Wc = trongso.chuoi_chieu(V, d["J"], d["names"], cha=par, cha_hoa=0.75)
        Wc = trongso.lam_tron(Lc, trongso.chuan(Wc), 1)
        Wc = tron_ke(Wc, {d["names"][1]: d["names"][0], d["names"][0]: par})
        sk.luoi_gan(nm, d["img"], Lc, Wc, dat=d["dat"])
    for e, m in (("trung", "chưởng chạm (đạn nước xoắn rời lòng bàn tay)"), ("phun", "ộp: sóng âm nước rời miệng (xương mieng)"),
                 ("het_phun", "hết sóng âm"), ("gam", "hai tay đập đất, xoáy lớn mở dưới chân đối thủ"), ("het_gam", "hết chiêu cuối")):
        sk.su_kien(e, m)
    info.update({"legs": legs, "lu": lu})
    return sk, info


def clips2(sk, info):
    legs, lu = info["legs"], info["lu"]
    H = info["H"]
    mem = [LoXo(["la", "la2"], k=[420, 300], damp=0.6, maxang=8),
           LoXo(["sung_n"], k=[520], damp=0.6, maxang=6), LoXo(["sung_x"], k=[520], damp=0.6, maxang=6),
           DayMem(lu, k0=0.24, k1=0.08, zeta=0.5, lim=(18, 28), luc=lambda t, i: np.array([0.0, -1100.0 * (1 + i)]))]

    def feet(P, off=None):
        """bốn chân bám đất (IK); off = {tên chân: (dx, dy)} dời đích (nhấc tay, chưởng)."""
        W = sk.the_gioi(P)
        for nm, d in legs.items():
            f = d["foot"] + (np.array(off[nm]) if off and nm in off else 0)
            tgt = (W["move"] @ np.array([f[0], f[1], 1.0]))[:2]
            hoat.ik_hai_doan(sk, P, d["names"][0], d["names"][1], tgt)

    def nen(P, tt, amp=1.0):
        """idle 2,4 s: thở nặng, túi kêu phập phồng hai nhịp, đầu gật nhẹ trễ, lá súng, sừng đung đưa lệch pha."""
        b = 0.5 - 0.5 * math.cos(2 * math.pi * tt / 2.4)
        b2 = 0.5 - 0.5 * math.cos(2 * math.pi * (tt - 0.15) / 1.2)
        P.scale("lung", 1 + 0.012 * b * amp, 1 + 0.022 * b * amp)
        P.move("hong", 0, -2.5 * b * amp)
        P.rot("nguc", 1.2 * song(tt, 2.4, 0.5) * amp)
        P.rot("dau", -1.4 * song(tt, 2.4, 1.1) * amp)
        P.scale("tui", 1 + 0.04 * b2 * amp, 1 + 0.05 * b2 * amp)
        P.rot("la", 1.5 * song(tt, 2.4, 1.6) * amp)
        P.rot("la2", 2.5 * song(tt, 2.4, 2.2) * amp)
        P.rot("sung_n", 2.0 * song(tt, 2.4, 1.9) * amp)
        P.rot("sung_x", 2.0 * song(tt, 2.4, 2.4) * amp)

    def idle_fn(t, P):
        nen(P, t)
        cr = cv(t, [(0, 0), (1.75, 0), (1.9, 1, "out"), (2.05, 0.9), (2.25, 0, "io"), (2.4, 0)])        # ộp nhẹ (phá nhịp)
        P.scale("tui", 1 + 0.16 * cr, 1 + 0.2 * cr)
        P.rot("ham", -5 * cr)
        an_hien(P, "mi_n", t, [(1.3, 1.42)])
        an_hien(P, "mi_x", t, [(1.31, 1.43)])
        feet(P)

    def appear_fn(t, P, D=1.4):
        fall = cv(t, [(0, 1), (0.42, 0, "in"), (D, 0)])
        P.move("move", 0, 0.75 * H * fall)
        a = cv(t, [(0, 0), (0.1, 1)])
        for s in sk.slots:
            if s["alpha"] > 0:
                P.alpha[s["name"]] = a
        land = cv(t, [(0, 0), (0.42, 0), (0.5, 1, "out"), (0.7, -0.2, "io"), (0.85, 0, "io"), (D, 0)])
        P.scale("lung", 1 + 0.06 * land, 1 - 0.1 * land)
        P.move("hong", 0, -10 * land)
        nen(P, lui(t, D), ease((t - 0.7) / 0.5))
        cr = cv(t, [(0, 0), (0.75, 0), (0.92, 1, "out"), (1.12, 0.8), (1.3, 0, "io"), (D, 0)])
        P.scale("tui", 1 + 0.35 * cr, 1 + 0.42 * cr)
        P.rot("ham", -16 * cr)
        P.rot("dau", 5 * cr)
        P.rot("la", -6 * fall)
        P.rot("la2", -10 * fall)
        feet(P, {nm: (0, 0) for nm in legs})

    def attack_fn(t, P, D=1.0, Hh=0.46):
        """Thủy Chưởng: nhổm lùi lấy đà, nhấc tay gần, đẩy chưởng ra trước ngang ngực (đứng tại chỗ, thân vươn ≤ 0,15 H)."""
        nen(P, lui(t, D), 1 - 0.8 * bao(t, 0.08, 0.92, 0.15, 0.2))
        back = cv(t, [(0, 0), (0.32, 1, "io"), (0.4, 1.05), (Hh, -1, "in"), (0.52, -1.1), (0.72, -0.9, "io"), (D, 0, "io")])
        P.move("move", -0.07 * H * max(back, 0) + 0.11 * H * max(-back, 0), 0)
        P.rot("nguc", 5 * back)
        P.rot("lung", 2 * back)
        P.rot("dau", 4 * back)
        P.rot("ham", -cv(t, [(0, 0), (0.32, 6, "io"), (Hh, 18, "out"), (0.7, 12), (D, 0, "io")]))
        lift = cv(t, [(0, 0), (0.22, 0.25, "io"), (0.36, 0.7, "io"), (Hh, 1, "out"), (0.7, 0.92), (0.88, 0.1, "io"), (D, 0, "io")])
        fx = cv(t, [(0, 0), (0.36, -0.25, "io"), (Hh, 1.0, "out"), (0.7, 0.9), (D, 0, "io")])
        # cổ tay tới trước ngực (trong tầm với: tay duỗi, không gập), lúc lấy đà rút về sau
        feet(P, {"chan_tn": (0.25 * H * fx, 0.19 * H * lift)})

    def cast_fn(t, P, D=1.3, Hh=0.62, E=1.02):
        """Ộp Âm Ba: túi kêu phồng to, ngửa đầu, há miệng ộp, giữ rung hai dáng."""
        nen(P, lui(t, D), 1 - 0.9 * bao(t, 0.08, 1.22, 0.15, 0.2))
        inf = cv(t, [(0, 0), (0.55, 1, "io"), (Hh, 1.05), (E, 0.5, "io"), (D, 0, "io")])
        P.scale("tui", 1 + 0.5 * inf, 1 + 0.58 * inf)
        P.rot("dau", cv(t, [(0, 0), (0.5, 8, "io"), (Hh, -4, "out"), (E, -2), (D, 0, "io")]) + 2.0 * rung(t, Hh + 0.03, E))
        P.rot("nguc", cv(t, [(0, 0), (0.5, 4, "io"), (Hh, -2, "out"), (D, 0, "io")]))
        P.rot("ham", -cv(t, [(0, 0), (0.5, 4, "io"), (Hh, 32, "out"), (E, 28), (D, 0, "io")]) - 3 * rung(t, Hh + 0.03, E))
        P.move("move", cv(t, [(0, 0), (Hh, 0), (Hh + 0.06, -0.03 * H, "out"), (E, -0.02 * H), (D, 0, "io")]), 0)
        feet(P)

    def skill_fn(t, P, D=2.0, Hh=0.98, E=1.5):
        """Đại Hải Lốc: chồm hai tay lên (túi phồng, há miệng), đập hai tay xuống đất; giữ rung, gầm."""
        nen(P, lui(t, D), 1 - 0.95 * bao(t, 0.08, 1.9, 0.2, 0.3))
        rear = cv(t, [(0, 0), (0.6, 1, "io"), (0.86, 1.08), (Hh, -0.25, "in"), (1.08, -0.1, "out"), (E, 0), (D, 0)])
        P.rot("hong", 13 * rear)
        P.rot("nguc", -4 * rear + 1.5 * rung(t, Hh + 0.03, E))
        up = max(rear, 0)
        feet(P, {"chan_tn": (0.08 * H * up, 0.2 * H * up), "chan_tx": (0.06 * H * up, 0.2 * H * up)})
        P.scale("tui", 1 + 0.35 * up, 1 + 0.4 * up)
        P.rot("ham", -cv(t, [(0, 0), (0.6, 18, "io"), (Hh, 30, "out"), (E, 26), (D, 0, "io")]) - 3 * rung(t, Hh + 0.03, E))
        P.rot("dau", cv(t, [(0, 0), (0.6, 6, "io"), (Hh, -5, "in"), (E, -3), (D, 0, "io")]) + 2 * rung(t, Hh + 0.03, E))
        sl = cv(t, [(0, 0), (Hh - 0.02, 0), (Hh, 1, "out"), (Hh + 0.18, 0, "io"), (D, 0)])
        P.scale("lung", 1 + 0.05 * sl, 1 - 0.08 * sl)
        P.move("hong", 0, -0.02 * H * sl)
        P.rot("la", -8 * sl + 3 * up)
        P.rot("la2", -12 * sl + 5 * up)

    def hit_fn(t, P, D=0.7):
        hd = cv(t, [(0, 0), (0.07, 1, "out"), (0.22, 0.55, "io"), (0.45, -0.12, "io"), (D, 0, "io")])
        nen(P, lui(t, D), ease((t - 0.3) / 0.35))
        P.rot("nguc", 6 * hd)
        P.rot("dau", 9 * hd)
        P.rot("lung", 2 * hd)
        P.move("move", -0.04 * H * hd, 0)
        P.scale("tui", 1 - 0.08 * hd, 1 - 0.1 * hd)
        P.rot("ham", -10 * hd)
        an_hien(P, "mi_n", t, [(0.03, 0.34)])
        an_hien(P, "mi_x", t, [(0.03, 0.34)])
        P.rot("la2", 9 * cv(t, [(0, 0), (0.07, 1, "out"), (0.3, -0.4, "io"), (D, 0, "io")]))
        P.rot("la", 5 * cv(t, [(0, 0), (0.12, 1, "out"), (0.36, -0.3, "io"), (D, 0, "io")]))
        feet(P)

    def die_fn(t, P, D=1.8):
        P.rot("dau", cv(t, [(0, 0), (0.07, 10, "out"), (0.3, 4), (0.85, -12, "io"), (D, -12)]))
        P.rot("ham", -cv(t, [(0, 0), (0.07, 16, "out"), (0.3, 10), (0.7, 22, "io"), (D, 22)]))
        P.rot("nguc", cv(t, [(0, 0), (0.07, 5, "out"), (0.9, -6, "io"), (D, -6)]))
        P.scale("tui", cv(t, [(0, 1), (0.6, 0.86, "io"), (D, 0.86)]), cv(t, [(0, 1), (0.6, 0.8, "io"), (D, 0.8)]))
        P.move("move", 0, cv(t, [(0, 0), (0.9, 0), (1.25, -0.06 * H, "in"), (D, -0.06 * H)]))
        P.rot("move", cv(t, [(0, 0), (0.9, 0), (1.25, 16, "in"), (1.35, 13, "out"), (D, 14)]))
        an_hien(P, "mi_n", t, [(0.04, D + 1)])
        an_hien(P, "mi_x", t, [(0.04, D + 1)])
        P.alpha["luoi"] = cv(t, [(0, 0), (0.28, 0), (0.34, 1)])
        for i, b in enumerate(lu):
            P.rot(b, cv(t, [(0, 0), (0.32, 0), (0.7, -12 - 5 * i, "out"), (D, -16 - 5 * i)]))
        a = cv(t, [(0, 1), (1.32, 1), (1.72, 0, "io"), (D, 0)])
        for s in sk.slots:
            if s["alpha"] > 0 or s["name"] in ("mi_n", "mi_x", "luoi"):
                P.alpha[s["name"]] = min(P.alpha.get(s["name"], s["alpha"]), a)
        if t < 0.9:
            feet(P)

    return [Clip("appear", 1.4, appear_fn, mem=mem),
            Clip("idle", 2.4, idle_fn, loop=True, mem=mem),
            Clip("attack", 1.0, attack_fn, ev=[(0.46, "trung", "")], mem=mem),
            Clip("cast", 1.3, cast_fn, ev=[(0.62, "phun", ""), (1.02, "het_phun", "")], mem=mem),
            Clip("skill", 2.0, skill_fn, ev=[(0.98, "gam", ""), (1.5, "het_gam", "")], mem=mem),
            Clip("hit", 0.7, hit_fn, mem=mem),
            Clip("die", 1.8, die_fn, mem=mem)]


def uon_thu2(sk, info, ra):
    P = Pose()
    P.rot("ham", -30)
    P.rot("dau", 8)
    P.scale("tui", 1.4, 1.5)
    P.rot("la2", 10)
    for nm, d in info["legs"].items():
        P.rot(d["names"][0], 15)
        P.rot(d["names"][1], -30)
    ve = soi.Ve(sk)
    B = soi._union([ve.bao(P)], 0.05)
    ve.ve(P, B, 1.0, bg=(150, 150, 150), ss=2, luoi=True, mau_luoi=(10, 10, 10, 110)).convert("RGB").save(ra)


def main_rig2():
    t0 = time.time()
    sk, info = rig2()
    cl = clips2(sk, info)
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    print(f"dạng 2: dựng + nướng {time.time() - t0:.1f} s")
    ra = os.path.join(base(2), "rig")
    os.makedirs(ra, exist_ok=True)
    so_concept(sk, fr["idle"][0], 2, info["conv"], os.path.join(ra, "so_concept.png"))
    xuat.xuat_het(sk, cl, ra, "tm03_2", "Ếch Lốc (dạng 2, dạng cuối)", frames=fr, dang=2, so_dang=2,
                  dung_yen=("attack", "cast", "skill"), ma_goc=3230,
                  can=[("can_mieng_cast", "cast", 0.7, "ham", 110), ("can_tay_attack", "attack", 0.46, "chan_tn1", 130),
                       ("can_mi_hit", "hit", 0.1, "dau", 110), ("can_tui_cast", "cast", 0.6, "tui", 120)])
    uon_thu2(sk, info, os.path.join(ra, "uon_thu.png"))
    return sk, info, cl, fr


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "rig" and sys.argv[2] == "1":
        main_rig1()
    elif cmd == "rig" and sys.argv[2] == "2":
        main_rig2()
    elif cmd == "all":
        main_rig2()
        # bản gộp dạng 2 trong rig tiến hóa của dạng 1: atlas 0,7, lưới thưa 1,5 lần (chỉ hiện trong clip evolve)
        sk2, info2 = rig2(s2=S2 * 0.7, thua=1.5)
        cl2 = clips2(sk2, info2)
        fr2 = {"idle": hoat.nuong(sk2, cl2[1])}
        main_rig1(sk2, cl2, fr2)
