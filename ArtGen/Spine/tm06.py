# -*- coding: utf-8 -*-
"""Dòng tm06 "Giông Bão" (lô 10 tướng mới đảo Thủy): cắt tờ mảnh GPT, dựng rig bằng mã với thư viện quai/, đặt mảnh theo dò tự
động trên concept (tm06_place.py -> place.json), nướng clip, xuất .atomik + game.json, tờ khung, lưới, ảnh cận, so_concept.

  dạng 1 Giông Mưa: kỳ giông con chibi đứng hai chân cõng bầu hồ lô (rig + clip ở file này)
  dạng 2 Giông Bão: kỳ giông núi khổng lồ bò bốn chân cõng bình đồng (tm06_d2.py)

    py -3 -I ArtGen/Spine/tm06.py cat 1|2
    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm06_place.py 1|2
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm06.py rig 2      dạng 2 trước
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm06.py rig 1      dạng 1 + evolve gộp dạng 2
Con gốc tham khảo monster_3241 (chỉ học: chuỗi lá/dây trễ 5 khung mỗi đốt, biên độ tăng ra ngọn; đồ trên lưng là mảnh cứng có
xương riêng; mắt đổi hình khi trúng đòn). Ghi chú: inbox/tm06_ghichu.md. Gói GPT: build_tm06.py.
"""
import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

from quai import anh, hoat, khung, luoi, mieng, soi, tienhoa, trongso, xuat  # noqa: E402
from quai.hoat import Clip, an_hien, chuoi_song, cv, ease, rung, song  # noqa: E402
from quai.khung import Dat  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm06"
TEN = {1: "Giông Mưa", 2: "Giông Bão"}
B_VIEN, B_TRONG = 11.0, 15.0


def inbox(k, *p):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", *p)


# ---------------------------------------------------------------- cắt tờ
def _o(to, cols, rows):
    cells = {}
    for m in to.manh:
        cx, cy = (m["x0"] + m["x1"]) / 2, (m["y0"] + m["y1"]) / 2
        cells.setdefault((min(rows - 1, int(cy / (to.h / rows))), min(cols - 1, int(cx / (to.w / cols)))), []).append(m)
    return cells


def _lon(ms):
    return max(ms, key=lambda m: m["dt"]) if ms else None


def cat(k):
    tv, ra = inbox(k, "tai_ve"), inbox(k, "manh")
    os.makedirs(ra, exist_ok=True)
    ten = {}
    p = anh.to_moi_nhat(tv, "M01")
    if p:
        to = anh.doc_to(p)
        cells = _o(to, 3, 2)
        g = {}
        for key, nm in (((0, 0), "dau"), ((0, 1), "ham"), ((0, 2), "mieng")):
            if _lon(cells.get(key, [])):
                g[nm] = _lon(cells[key])
        lids = sorted(cells.get((1, 0), []), key=lambda m: -m["dt"])[:2]
        for nm, m in zip(("mi_n", "mi_x"), lids):
            g[nm] = m
        gill_cells = [(1, 1)] if k == 1 else [(1, 1), (1, 2)]
        gills = [m for c in gill_cells for m in cells.get(c, [])]
        gills = sorted(gills, key=lambda m: -(m["x1"] - m["x0"]))[:3]
        for nm, m in zip(("mang1", "mang2", "mang3"), gills):
            g[nm] = m
        if k == 1 and _lon(cells.get((1, 2), [])):
            g["nut"] = _lon(cells[(1, 2)])
        ten.update(anh.luu_manh(to, g, ra, duc={"mieng": ("tu_dong", 400)}))
    p = anh.to_moi_nhat(tv, "M02")
    if p:
        to = anh.doc_to(p)
        g = {}
        if k == 1:
            left = [m for m in to.manh if (m["x0"] + m["x1"]) / 2 < to.w / 3]
            right = [m for m in to.manh if (m["x0"] + m["x1"]) / 2 >= to.w / 3]
            if left:
                g["than"] = _lon(left)
            top = [m for m in right if (m["y0"] + m["y1"]) / 2 < to.h / 2]
            bot = sorted([m for m in right if (m["y0"] + m["y1"]) / 2 >= to.h / 2], key=lambda m: -m["dt"])[:2]
            if top:
                g["duoi"] = _lon(top)
            bot = sorted(bot, key=lambda m: m["x0"])
            for nm, m in zip(("tay_n", "tay_x"), bot):
                g[nm] = m
        else:
            ms = sorted(to.manh, key=lambda m: -m["dt"])[:2]
            ms = sorted(ms, key=lambda m: m["y0"])
            for nm, m in zip(("than", "duoi"), ms):
                g[nm] = m
        ten.update(anh.luu_manh(to, g, ra))
    p = anh.to_moi_nhat(tv, "M03")
    if p:
        to = anh.doc_to(p)
        g = {}
        if k == 1:
            ms = sorted(sorted(to.manh, key=lambda m: -m["dt"])[:3], key=lambda m: m["x0"])
            for nm, m in zip(("chan_t", "chan_p", "bau"), ms):
                g[nm] = m
        else:
            top = sorted([m for m in to.manh if (m["y0"] + m["y1"]) / 2 < to.h / 2], key=lambda m: -m["dt"])[:2]
            top = sorted(top, key=lambda m: -m["dt"])
            for nm, m in zip(("binh", "nap"), top):
                g[nm] = m
            bot = sorted([m for m in to.manh if (m["y0"] + m["y1"]) / 2 >= to.h / 2], key=lambda m: -m["dt"])[:4]
            for nm, m in zip(("chan1", "chan2", "chan3", "chan4"), sorted(bot, key=lambda m: m["x0"])):
                g[nm] = m
        ten.update(anh.luu_manh(to, g, ra, duc={"nap": [(0.5, 0.22), (0.5, 0.27)]} if k == 2 else None))
    if k == 1 and os.path.exists(os.path.join(ra, "bau.png")):
        # lòng miệng bầu (giấy trắng trong vành cổ bầu): tô nâu sẫm như lòng bầu, để khi nút bật ra không lộ giấy
        im = np.asarray(Image.open(os.path.join(ra, "bau.png")).convert("RGBA")).copy()
        h, w = im.shape[:2]
        sel = np.zeros((h, w), bool)
        sel[: int(0.1 * h), int(0.28 * w): int(0.75 * w)] = True
        lite = (im[..., :3].min(axis=2) > 205) & (im[..., 3] > 150) & sel
        im[lite, :3] = (74, 48, 28)
        Image.fromarray(im, "RGBA").save(os.path.join(ra, "bau.png"))
        print(f"  bau: tô lòng miệng bầu {int(lite.sum())} px")
    print("  đã cắt:", ", ".join(sorted(ten)))
    print("  soi:", anh.to_soi(ra, sorted(ten)))


# ---------------------------------------------------------------- tiện ích đặt mảnh
class Dung:
    """đọc place.json (toạ độ concept), quy về thế giới rig: X = (px - xg)·G, Y = (yg - py)·G. Mỗi mảnh nạp ở tỉ lệ atlas
    T = s·G (đúng độ phân giải hiển thị), Dat = (tâm, góc, ti = s·G / T)."""

    def __init__(self, k, G, giu_cho, ti_anh=1.0):
        self.k, self.G = k, G
        pj = json.load(open(inbox(k, "place.json"), encoding="utf-8"))
        self.pl = pj["parts"]
        self.xg, self.yg = pj["ground"]
        self.iou_ghep = pj.get("iou")
        T = {}
        for n, p in self.pl.items():
            img = p.get("img", n)
            T[img] = max(T.get(img, 0.0), max(p["sx"], p["sy"]) * G * ti_anh)
        self.T = T
        gc = {n: v for n, v in giu_cho.items()}
        self.pc = anh.nap_manh(inbox(k, "manh"), gc, ti_le=1.0, ti_le_rieng={n: T.get(n, 0.5 * G) for n in gc})
        _, fg = concept_fg(k)
        ys = np.nonzero(fg.any(axis=1))[0]
        self.cao = float((self.yg - ys.min()) * G)          # chiều cao con (pixel rig) theo concept
        self.bv, self.bt = 0.015 * self.cao, 0.02 * self.cao  # mật độ lưới theo chiều cao (đặc tả mục 5)
        print(f"  dạng {k}: cao {self.cao:.0f} px rig, bước lưới viền {self.bv:.1f} / trong {self.bt:.1f}")

    def w(self, px, py):
        return np.array([(px - self.xg) * self.G, (self.yg - py) * self.G])

    def dat(self, n):
        p = self.pl[n]
        img = p.get("img", n)
        Tn = self.T[img]
        c = self.w(p["cx"], p["cy"])
        return Dat(c[0], c[1], goc=p["r"], ti=(p["sx"] * self.G / Tn, p["sy"] * self.G / Tn), lat=p.get("lat", False))

    def img(self, n):
        return self.pc[self.pl[n].get("img", n)] if n in self.pl else self.pc[n]


def nguoc(dat, Pw, w, h):
    """thế giới rig -> toạ độ ảnh (nghịch Dat.ra)."""
    P = np.asarray(Pw, float).reshape(-1, 2)
    ax, ay = (dat.neo if dat.neo_px else (dat.neo[0] * w, dat.neo[1] * h))
    c, s = math.cos(math.radians(dat.goc)), math.sin(math.radians(dat.goc))
    dx, dy = P[:, 0] - dat.x, P[:, 1] - dat.y
    lx, ly = c * dx + s * dy, -s * dx + c * dy
    return np.stack([ax + lx / (dat.sx * (-1 if dat.lat else 1)), ay - ly / dat.sy], 1)


def mo_mep(im, ben, frac, ra=None, bo=0.0):
    """làm mờ dần (alpha) dải mép ảnh để chỗ nối chui dưới mảnh khác không lộ "miệng ống": ben trai/phai/tren/duoi, frac = bề dày
    dải theo tỉ lệ khung hình (cắt sát); ra = phần còn lại ở mép (0 = trong suốt hẳn); bo = bỏ hẳn dải này trước khi mờ dần (cắt
    nắp ống ở đầu mảnh)."""
    a = np.asarray(im).copy()
    al = a[:, :, 3].astype(np.float32)
    ys, xs = np.nonzero(al > 8)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    H, W_ = al.shape
    if ben in ("trai", "phai"):
        u = (np.arange(W_) - x0) / max(1, x1 - x0)
        u = u if ben == "trai" else 1 - u
        f = np.clip((u - bo) / frac, 0, 1)[None, :]
    else:
        u = (np.arange(H) - y0) / max(1, y1 - y0)
        u = u if ben == "tren" else 1 - u
        f = np.clip((u - bo) / frac, 0, 1)[:, None]
    f = (ra or 0.0) + (1 - (ra or 0.0)) * (f * f * (3 - 2 * f))
    a[:, :, 3] = (al * f).astype(np.uint8)
    return Image.fromarray(a, "RGBA")


def mat_na(im):
    return np.asarray(im)[:, :, 3] > 100


def geo_truc(im, goc, n, buoc=3):
    """n+1 điểm khớp dọc mảnh (toạ độ ảnh): khoảng cách đi trong hình từ điểm goc (ảnh), mỗi khớp là trọng tâm dải khoảng cách."""
    m = mat_na(im)
    h, w = m.shape
    ms = m[::buoc, ::buoc]
    H, Wd = ms.shape
    g = np.array(goc, float) / buoc
    ys, xs = np.nonzero(ms)
    i0 = int(np.argmin((xs - g[0]) ** 2 + (ys - g[1]) ** 2))
    D = np.full(ms.shape, np.inf)
    D[ys[i0], xs[i0]] = 0.0
    INF = np.inf
    for _ in range(4 * (H + Wd)):
        old = D
        P = np.pad(D, 1, constant_values=INF)
        cand = [P[1:-1, :-2] + 1, P[1:-1, 2:] + 1, P[:-2, 1:-1] + 1, P[2:, 1:-1] + 1,
                P[:-2, :-2] + 1.414, P[:-2, 2:] + 1.414, P[2:, :-2] + 1.414, P[2:, 2:] + 1.414]
        D = np.minimum(D, np.minimum.reduce(cand))
        D[~ms] = INF
        if np.array_equal(D, old):
            break
    fin = np.isfinite(D)
    dmax = D[fin].max()
    band = dmax / (2 * n)
    J = []
    for k in range(n + 1):
        d = dmax * k / n
        sel = fin & (np.abs(D - d) <= band)
        if k == 0:
            sel = fin & (D <= band)
        if k == n:
            sel = fin & (D >= dmax - band)
        yy, xx = np.nonzero(sel)
        J.append(((xx.mean() + 0.5) * buoc, (yy.mean() + 0.5) * buoc))
    J = np.array(J)
    J[0] = J[0] * 0.5 + np.array([xs[i0] + 0.5, ys[i0] + 0.5]) * buoc * 0.5
    return J


def dau_mut(im, ben="trai"):
    """tâm đầu mút trái / phải của mảnh (toạ độ ảnh): trọng tâm 6 % bề ngang ở mép đó."""
    m = mat_na(im)
    ys, xs = np.nonzero(m)
    if ben == "trai":
        s = xs <= xs.min() + 0.06 * (xs.max() - xs.min())
    else:
        s = xs >= xs.max() - 0.06 * (xs.max() - xs.min())
    return np.array([xs[s].mean(), ys[s].mean()])


def tim_mat(im, toi_thieu=60):
    """các cụm tròng mắt (vàng / hổ phách) trên ảnh đầu, lớn → nhỏ: [(x, y, diện tích)]."""
    a = np.asarray(im.convert("RGBA")).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    m = (al > 128) & (r > 200) & (g > 120) & (b < 120) & (r - b > 100)
    lab, cs = anh.thanh_phan(m)
    out = []
    for c in sorted(cs, key=lambda q: -q["dt"]):
        if c["dt"] < toi_thieu:
            continue
        yy, xx = np.nonzero(lab == c["i"])
        out.append((float(xx.mean()), float(yy.mean()), int(c["dt"])))
    return out


def mat_mat(dau, seed, noi=4):
    """mặt nạ con mắt cho fit_lid: cụm tròng vàng/hổ phách gần điểm seed nhất, lấy bao lồi (gồm đồng tử, chấm sáng), nới noi px."""
    a = np.asarray(dau.convert("RGBA")).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    m = (al > 128) & (r > 200) & (g > 120) & (b < 120) & (r - b > 100)
    lab, cs = anh.thanh_phan(m)
    cs = [c for c in cs if c["dt"] >= 12]
    best, bd = None, 1e18
    for c in cs:
        yy, xx = np.nonzero(lab == c["i"])
        d = (xx.mean() - seed[0]) ** 2 + (yy.mean() - seed[1]) ** 2
        if d < bd:
            best, bd = (xx, yy), d
    xx, yy = best
    hull = anh.bao_loi(np.stack([xx + 0.5, yy + 0.5], 1))
    eye = anh.to_da_giac(m.shape, hull)
    return anh.gian(eye, noi, tron=True)


def songz(t, T, pha=0.0):
    """sin lệch về 0 ở t = 0 (khung 0 idle đúng dáng gốc = dáng concept)."""
    return math.sin(2 * math.pi * t / T + pha) - math.sin(pha)


def chuoi_songz(P, ten, t, T, bien_do, tre=0.12, ngon_dan=False, pha=0.0):
    """như hoat.chuoi_song nhưng mỗi đốt trừ giá trị ở t = 0 (khung 0 = dáng gốc)."""
    n = len(ten)
    amp = np.broadcast_to(np.asarray(bien_do, float), (n,))
    for i, b in enumerate(ten):
        k = (n - 1 - i) if ngon_dan else i
        ph = pha - 2 * math.pi * k * tre / T
        P.rot(b, amp[i] * (math.sin(2 * math.pi * t / T + ph) - math.sin(ph)))


def concept_fg(k):
    rgb = np.asarray(Image.open(inbox(k, "tai_ve", "L1_duyet.png")).convert("RGB"))
    bg = anh.nen_tu_mep((rgb.min(axis=2) > 222) & ((rgb.max(axis=2).astype(int) - rgb.min(axis=2)) < 32))
    return rgb, ~bg


def so_concept(sk, P0, k, D, ra):
    """khung 0 idle vẽ cùng tỉ lệ concept, đặt cạnh concept + chồng; IoU mặt nạ (đích ≥ 0,85)."""
    rgb, fg = concept_fg(k)
    H, W = fg.shape
    G = D.G
    box = ((0 - D.xg) * G, (D.yg - H) * G, (W - D.xg) * G, D.yg * G)
    ve = soi.Ve(sk)
    im = ve.ve(P0, box, 1.0 / G, ss=1)
    im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im)[:, :, 3] > 128
    iou = float((a & fg).sum() / max(1, (a | fg).sum()))
    rig_rgb = Image.new("RGB", (W, H), (255, 255, 255))
    rig_rgb.paste(im, (0, 0), im)
    ov = Image.blend(Image.fromarray(rgb), rig_rgb, 0.55)
    diff = np.full((H, W, 3), 255, np.uint8)
    diff[fg & ~a] = (230, 60, 60)
    diff[a & ~fg] = (60, 110, 230)
    diff[a & fg] = (205, 205, 205)
    out = Image.new("RGB", (W * 4, H + 40), (255, 255, 255))
    for i, x in enumerate([Image.fromarray(rgb), rig_rgb, ov, Image.fromarray(diff)]):
        out.paste(x, (i * W, 40))
    d = ImageDraw.Draw(out)
    f = anh.font(26)
    for i, s in enumerate([f"concept dạng {k} (L1_duyet)", f"rig khung 0 idle (IoU {iou:.3f})", "chồng 55 %",
                           "đỏ: concept có, rig thiếu; xanh: rig thừa"]):
        d.text((i * W + 12, 6), s, fill=(0, 0, 0), font=f)
    out = out.resize((out.width // 2, out.height // 2), Image.LANCZOS)
    out.save(ra)
    print(f"  so_concept: IoU khung 0 idle / concept = {iou:.3f} -> {ra}")
    return iou


def lech_dau(sk, frames, clips):
    """lệch khung 0 mỗi clip so với khung 0 idle, đo trên đỉnh lưới đã vẽ của mọi slot."""
    ve = soi.Ve(sk)
    i0 = frames["idle"][0]
    out = {}
    for c in clips:
        if c.ten in ("idle", "aura", "appear", "evolve"):
            continue
        d, w = soi.lech(ve, frames[c.ten][0], i0)
        out[c.ten] = (d, w)
    return out


def uon_thu(sk, chains, ra, extra=None):
    """ảnh uốn thử: mỗi đốt chuỗi xoay 18°: soi lưới cong trơn, không gập ở khớp."""
    P = khung.Pose()
    for names in chains:
        for b in names:
            P.rot(b, 18)
    if extra:
        extra(P)
    ve = soi.Ve(sk)
    B = soi._union([ve.bao(P)], 0.05)
    a = ve.ve(P, B, 1.4, bg=(150, 150, 150), ss=2, luoi=True, mau_luoi=(10, 10, 10, 110))
    a.convert("RGB").save(ra)
    return ra


def fade_all(sk, P, a, an=()):
    for s in sk.slots:
        if s["alpha"] > 0:
            P.alpha[s["name"]] = a
    for s in an:
        if s in P.alpha:
            P.alpha[s] = min(P.alpha[s], a)


def xfade(fn, P, t, D, amp, w0, w1):
    """nền idle trong clip không lặp: khung 0 đúng idle(0), khung cuối đúng idle(0); giữa hoà từ nen(t) sang nen(t - D)."""
    w = ease((t - w0) / max(1e-6, w1 - w0))
    if 1 - w > 1e-6:
        fn(P, t, amp * (1 - w))
    if w > 1e-6:
        fn(P, t - D, amp * w)


# ---------------------------------------------------------------- dạng 1: Giông Mưa
G1 = 0.5
GC1 = {"dau": ("bo", 460, 260, (110, 136, 188)), "ham": ("ham", 300, 110, (244, 166, 90)), "mieng": ("mieng", 220, 140, (194, 71, 94)),
       "mi_n": ("mi", 120, 105, (110, 136, 188)), "mi_x": ("mi", 70, 100, (110, 136, 188)), "mang1": ("luoi", 330, 80, (229, 96, 63)),
       "mang2": ("luoi", 280, 70, (229, 96, 63)), "mang3": ("luoi", 230, 60, (229, 96, 63)), "nut": ("tron", 110, 100, (138, 90, 51)),
       "than": ("tron", 380, 500, (110, 136, 188)), "duoi": ("dai", 760, 420, (110, 136, 188)), "tay_n": ("chan", 260, 220, (110, 136, 188)),
       "tay_x": ("chan", 230, 300, (110, 136, 188)), "chan_t": ("chan", 300, 380, (110, 136, 188)),
       "chan_p": ("chan", 330, 380, (110, 136, 188)), "bau": ("giot", 330, 520, (232, 198, 106))}
# điểm đọc trên concept dạng 1 (px concept, inbox/tm06_1/rig/z_*.png): chỉ để chọn đầu gốc của chuỗi; khớp tính theo hình mảnh
A1 = dict(hong=(855, 745), nguc=(875, 585), co=(905, 478), dau=(925, 440), vai_n=(960, 585), vai_x=(800, 590), hong_t=(735, 720),
          hong_p=(915, 735), goc_duoi=(705, 665), bau=(640, 540), mat_n=(965, 372), mat_x=(1112, 382))


def dung1():
    D = Dung(1, G1, GC1)
    pc = D.pc
    sk = khung.Sk(f"{CODE}_1")
    for n, im in pc.items():
        sk.anh(n, im)
    W = D.w
    sk.xuong("root")
    sk.xuong("move", "root")
    # thân: chuỗi đứng than (hông) -> nguc -> co (đỉnh cổ); khớp tính trên ảnh thân theo trục giữa
    dt = D.dat("than")
    im = pc["than"]
    w, h = im.size
    Jt_img = np.array([(0.47 * w, 0.97 * h), (0.47 * w, 0.62 * h), (0.52 * w, 0.30 * h), (0.58 * w, 0.02 * h)])
    Jt = dt.ra(Jt_img, w, h)
    sk.xuong("than", "move", *Jt[0], the_gioi=True, goc=math.degrees(math.atan2(*(Jt[1] - Jt[0])[::-1])),
             dai=float(np.hypot(*(Jt[1] - Jt[0]))))
    sk.xuong("nguc", "than", *Jt[1], the_gioi=True, goc=math.degrees(math.atan2(*(Jt[2] - Jt[1])[::-1])),
             dai=float(np.hypot(*(Jt[2] - Jt[1]))))
    sk.xuong("co", "nguc", *Jt[2], the_gioi=True, goc=math.degrees(math.atan2(*(Jt[3] - Jt[2])[::-1])),
             dai=float(np.hypot(*(Jt[3] - Jt[2]))))
    neck = W(*A1["dau"])
    # đầu, hàm
    dd = D.dat("dau")
    dau = pc["dau"]
    hw, hh = dau.size
    head_c = dd.mot((0.55 * hw, 0.45 * hh), hw, hh)
    sk.xuong("dau", "co", *neck, the_gioi=True, goc=math.degrees(math.atan2(*(head_c - neck)[::-1])),
             dai=float(np.hypot(*(head_c - neck))))
    dj = D.dat("ham")
    ham = pc["ham"]
    hinge = dj.mot(dau_mut(ham, "trai") + np.array([0.06 * ham.width, -0.05 * ham.height]), *ham.size)
    snout = dj.mot(dau_mut(ham, "phai"), *ham.size)
    gj = math.degrees(math.atan2(*(snout - hinge)[::-1]))
    sk.xuong("ham", "dau", *hinge, goc=gj, dai=float(np.hypot(*(snout - hinge))), the_gioi=True)
    sk.xuong("mieng", "dau", snout[0] + 4, snout[1] + 6, goc=-6, dai=30, the_gioi=True)
    # lá mang: dải lưới 3 đốt, gốc bám đầu
    gills = {}
    for g in ("mang_x1", "mang_x2", "mang_n1", "mang_n2", "mang_n3"):
        if g not in D.pl:
            continue
        im = D.img(g)
        Lg = luoi.luoi_dai(im, 3, ten=g, buoc=D.bv)
        dg = D.dat(g)
        Jg = dg.ra(Lg.khop(3), *im.size)
        names = sk.chuoi(g, "dau", Jg)
        gills[g] = (Lg, dg, names)
    # tay: chuỗi 3 đốt từ vai (điểm mảnh gần vai nhất)
    arms = {}
    for t, anc in (("tay_x", "vai_x"), ("tay_n", "vai_n")):
        im = pc[t]
        da = D.dat(t)
        g0 = nguoc(da, W(*A1[anc]), *im.size)[0]
        Ji = geo_truc(im, g0, 3)
        Ja = da.ra(Ji, *im.size)
        names = sk.chuoi(t, "nguc", Ja)
        arms[t] = (im, da, Ja, names)
    # chân: chuỗi 3 đốt (đùi, cẳng, bàn) từ hông
    legs = {}
    for c, anc in (("chan_t", "hong_t"), ("chan_p", "hong_p")):
        im = pc[c]
        dc = D.dat(c)
        g0 = nguoc(dc, W(*A1[anc]), *im.size)[0]
        g0[1] = min(g0[1], 0.15 * im.height)
        Ji = geo_truc(im, g0, 3)
        Jc = dc.ra(Ji, *im.size)
        names = sk.chuoi(c, "than", Jc)
        legs[c] = (im, dc, Jc, names)
    # đuôi: 6 đốt theo khoảng cách đi trong hình từ gốc
    im = pc["duoi"]
    dq = D.dat("duoi")
    g0 = nguoc(dq, W(*A1["goc_duoi"]), *im.size)[0]
    Jq_img = geo_truc(im, g0, 6)
    Jq = dq.ra(Jq_img, *im.size)
    duoi = sk.chuoi("duoi", "than", Jq)
    # bầu (cứng) + nút
    db = D.dat("bau")
    sk.xuong("bau", "nguc", *W(*A1["bau"]), the_gioi=True, dai=40)
    dn = D.dat("nut") if "nut" in D.pl else None
    if dn is not None:
        sk.xuong("nut", "bau", dn.x, dn.y, the_gioi=True, dai=20)
    # ---- slot (sau -> trước)
    sk.slot("duoi", duoi[0], "duoi")
    sk.slot("bau", "bau", "bau")
    if dn is not None:
        sk.slot("nut", "nut", "nut")
    sk.slot("tay_x", arms["tay_x"][3][0], "tay_x")
    sk.slot("than", "than", "than")
    sk.slot("chan_t", legs["chan_t"][3][0], "chan_t")
    sk.slot("chan_p", legs["chan_p"][3][0], "chan_p")
    for g in ("mang_x1", "mang_x2", "mang_n1", "mang_n2", "mang_n3"):
        if g in gills:
            sk.slot(g, gills[g][2][0], D.pl[g].get("img", g))
    sk.slot("mieng", "ham", "mieng")
    sk.slot("ham", "ham", "ham")
    sk.slot("dau", "dau", "dau")
    sk.slot("mi_x", "dau", "mi_x", an=True)
    sk.slot("mi_n", "dau", "mi_n", an=True)
    sk.slot("tay_n", arms["tay_n"][3][0], "tay_n")
    # ---- lưới, trọng số
    Lt = luoi.luoi_vung(pc["than"], D.bv, D.bt, ten="than")
    Wt = trongso.chuoi_chieu(dt.ra(Lt.pts, *pc["than"].size), Jt, ["than", "nguc", "co"])
    Wt = trongso.lam_tron(Lt, Wt, 2)
    trongso.kiem(Wt, "than")
    sk.luoi_gan("than", "than", Lt, Wt, dat=dt)
    Lh = luoi.luoi_vung(dau, D.bv, D.bt, ten="dau")
    Qh = dd.ra(Lh.pts, hw, hh)
    Wh = trongso.theo_truc(Qh, neck, head_c, "co", "dau", u0=-0.25, u1=0.25)
    Wh = trongso.lam_tron(Lh, Wh, 1)
    trongso.kiem(Wh, "dau", cho_cung=("dau",))
    sk.luoi_gan("dau", "dau", Lh, Wh, dat=dd)
    Lj = luoi.luoi_vung(ham, D.bv, D.bt, ten="ham")
    Wj = mieng.ham_hai_xuong(dj.ra(Lj.pts, *ham.size), hinge, snout, "dau", "ham")
    sk.luoi_gan("ham", "ham", Lj, Wj, dat=dj)
    # lòng miệng: miệng kỳ giông rộng, nhìn 3/4 thấy cả khoang miệng: hàng trên bám đầu (môi trên), hàng dưới bám hàm (giấu sau hàm
    # khi khép); há ra thì khoang miệng giãn lấp kín khe giữa hai môi. Lưỡi vẽ liền trong ảnh hàm nên không có "lưỡi thứ hai".
    mieng.long_mieng(sk, "mieng", "mieng", "dau", "ham", hinge, snout, duoi=-0.16, tren=(0.04, 0.08, 0.13, 0.18, 0.2),
                     q_tren=(0.0, 0.0, 0.0, 0.0, 0.0), doc=(0.04, 0.98))
    for g, (Lg, dg, names) in gills.items():
        Wg = trongso.chuoi(Lg.s, Lg.truc[1][-1] / 3, names, cha="dau", cha_hoa=0.5)
        sk.luoi_gan(g, D.pl[g].get("img", g), Lg, Wg, dat=dg)
    for t, (im, da, Ja, names) in arms.items():
        La = luoi.luoi_vung(im, D.bv, D.bt, ten=t)
        Wa = trongso.chuoi_chieu(da.ra(La.pts, *im.size), Ja, names, cha="nguc", cha_hoa=0.7)
        Wa = trongso.lam_tron(La, Wa, 1)
        sk.luoi_gan(t, t, La, Wa, dat=da)
    for c, (im, dc, Jc, names) in legs.items():
        Lc = luoi.luoi_vung(im, D.bv, D.bt, ten=c)
        Wc = trongso.chuoi_chieu(dc.ra(Lc.pts, *im.size), Jc, names, cha="than", cha_hoa=0.8)
        Wc = trongso.lam_tron(Lc, Wc, 1)
        sk.luoi_gan(c, c, Lc, Wc, dat=dc)
    Lq = luoi.luoi_vung(pc["duoi"], D.bv, D.bt, ten="duoi")
    Wq = trongso.chuoi_geo(Lq, Jq_img, duoi, cha="than", cha_hoa=0.7)
    Wq = trongso.lam_tron(Lq, Wq, 1)
    trongso.kiem(Wq, "duoi")
    sk.luoi_gan("duoi", "duoi", Lq, Wq, dat=dq)
    sk.manh("bau", "bau", db)
    if dn is not None:
        sk.manh("nut", "nut", dn)
    # mí mắt: dò phủ kín
    eyes = tim_mat(dau)
    seeds = {"mi_n": nguoc(dd, W(*A1["mat_n"]), hw, hh)[0], "mi_x": nguoc(dd, W(*A1["mat_x"]), hw, hh)[0]}
    for lid in ("mi_n", "mi_x"):
        s0 = seeds[lid]
        if eyes:
            e = min(eyes, key=lambda q: (q[0] - s0[0]) ** 2 + (q[1] - s0[1]) ** 2)
            if (e[0] - s0[0]) ** 2 + (e[1] - s0[1]) ** 2 < (0.15 * hw) ** 2:
                s0 = np.array(e[:2])
        kq = mieng.fit_lid(dau, pc[lid], mat=mat_mat(dau, s0), ten=f"dạng 1 {lid}")
        sk.manh(lid, lid, mieng.dat_mi(dd, dau, kq))
    for e, m in (("trung", "đuôi đập đất (VFX sóng nước lan tới đối thủ)"), ("phun", "bắt đầu phun tia nước (VFX bám xương mieng)"),
                 ("het_phun", "hết phun"), ("gam", "bầu phụt cột nước lên trời (VFX mưa rơi quanh đối thủ)"),
                 ("het_gam", "hết chiêu cuối"), ("bat_nut", "nút bầu bật ra")):
        sk.su_kien(e, m)
    foot = {c: (np.array(v[2][2]), np.array(v[2][3])) for c, v in legs.items()}
    info = dict(D=D, duoi=duoi, gills={g: v[2] for g, v in gills.items()}, arms={t: v[3] for t, v in arms.items()},
                legs={c: v[3] for c, v in legs.items()}, foot=foot, k=1, H=float(Jt[3][1]), nut=dn is not None)
    print(f"  dạng 1: {sk.tom_tat()}")
    return sk, info


def chan_bam(sk, P, legs, foot):
    """IK hai đoạn đùi-cẳng để cổ chân về chỗ cũ (theo move), rồi xoay bàn chân giữ góc thế giới dáng gốc (bàn phẳng trên đất)."""
    W0 = sk.W0
    for c, names in legs.items():
        W = sk.the_gioi(P)
        ank = foot[c][0]
        tgt = (W["move"] @ np.array([ank[0], ank[1], 1.0]))[:2]
        hoat.ik_hai_doan(sk, P, names[0], names[1], tgt)
        W = sk.the_gioi(P)
        b = names[2]
        a_now = math.degrees(math.atan2(W[b][1, 0], W[b][0, 0]))
        a0 = math.degrees(math.atan2(W0[b][1, 0], W0[b][0, 0])) + math.degrees(math.atan2(W["move"][1, 0], W["move"][0, 0]))
        P.rot(b, ((a0 - a_now + 180) % 360) - 180)


def clips1(sk, info):
    duoi, gills, arms, legs, foot = info["duoi"], info["gills"], info["arms"], info["legs"], info["foot"]
    H = info["H"]
    nd = len(duoi)
    DI = 2.0
    g_amp = {"mang_n1": [4, 6, 8], "mang_n2": [3.5, 5.5, 7.5], "mang_n3": [3, 5, 7], "mang_x1": [3, 5, 7], "mang_x2": [3, 4.5, 6]}
    g_ph = {"mang_n1": 0.0, "mang_n2": 0.7, "mang_n3": 1.4, "mang_x1": 0.35, "mang_x2": 1.05}
    tail_amp = np.linspace(1.5, 6.0, nd)

    def nen(P, t, a=1.0):
        """chuyển động nền idle (tuyến tính theo a): thở, đầu lệch pha, mang và đuôi sóng trễ (gốc dẫn), bầu lắc trễ."""
        s1 = songz(t, DI)
        s2 = songz(t, DI, -0.6)
        P.move("than", 0, -2.2 * a * (0.5 + 0.5 * math.cos(2 * math.pi * t / DI)) + 2.2 * a)
        P.rot("than", 0.8 * a * s1)
        P.rot("nguc", 1.4 * a * s2)
        P.rot("co", -1.0 * a * s2)
        P.rot("dau", -1.6 * a * songz(t, DI, -1.2))
        for g, names in gills.items():
            chuoi_songz(P, names, t, DI, np.array(g_amp.get(g, [3, 5, 7])) * a, tre=0.12, pha=g_ph.get(g, 0))
        chuoi_songz(P, duoi, t, DI, tail_amp * a, tre=0.1, pha=0.5)
        for tn, names in arms.items():
            sg = 1 if tn == "tay_n" else -1
            P.rot(names[0], 2.5 * a * sg * songz(t, DI, -0.9))
            P.rot(names[1], 3.0 * a * sg * songz(t, DI, -1.3))
        P.rot("bau", 2.2 * a * songz(t, DI, -1.0))

    def feet(P):
        chan_bam(sk, P, legs, foot)

    def blink(P, t, khoang):
        an_hien(P, "mi_n", t, khoang)
        an_hien(P, "mi_x", t, khoang)

    def idle_fn(t, P):
        nen(P, t)
        blink(P, t, [(1.30, 1.42)])
        P.rot("ham", -cv(t, [(0, 0), (0.55, 0), (0.62, 8, "out"), (0.72, 2), (0.8, 6, "out"), (0.95, 0, "io"), (DI, 0)]))
        feet(P)

    def appear_fn(t, P, D=1.2):
        g = cv(t, [(0, 0.02), (0.42, 1.1, "out"), (0.6, 0.96, "io"), (0.8, 1.0, "io"), (D, 1.0)])
        P.scale("move", g, g)
        fade_all(sk, P, cv(t, [(0, 0), (0.12, 1)]))
        xfade(nen, P, t, D, ease((t - 0.45) / 0.5), 0.0, 0.01)
        fl = cv(t, [(0, 0), (0.62, 0), (0.78, 1, "out"), (1.0, 0, "io"), (D, 0)])
        P.rot("dau", 8 * fl)
        P.rot("ham", -20 * fl)
        for g, names in gills.items():
            P.rot(names[0], -10 * fl)
        feet(P)

    def attack_fn(t, P, D=1.0, T=0.48):
        """Đuôi Hắt Nước: vặn người lấy đà, đuôi nhấc cao (0,1–0,36), quật xuống đập đất đúng 0,48 (trung), giữ trôi, về."""
        xfade(nen, P, t, D, 1 - 0.75 * hoat.bao(t, 0.05, 0.85, 0.15, 0.2), 0.3, 0.75)
        lift = cv(t, [(0, 0), (0.1, 0.2, "io"), (0.36, 1.0, "io"), (0.40, 1.05), (T, -0.55, "in"), (0.56, -0.62), (0.72, -0.45, "io"),
                      (D, 0, "io")])
        tw = cv(t, [(0, 0), (0.36, 1, "io"), (T, -0.7, "in"), (0.7, -0.5), (D, 0, "io")])
        P.rot("than", -3 * tw)
        P.rot("nguc", -5 * tw)
        P.rot("dau", 4 * tw)
        P.move("than", -6 * tw, -4 * abs(tw) + 4 * max(0.0, -tw))
        for i, b in enumerate(duoi):
            lag = 0.025 * i
            li = cv(t - lag, [(0, 0), (0.1, 0.2, "io"), (0.36, 1.0, "io"), (0.40, 1.05), (T, -0.55, "in"), (0.56, -0.62),
                              (0.72, -0.45, "io"), (D, 0, "io")]) if t - lag > 0 else 0.0
            P.rot(b, -(10 + 4 * i) * li if i < 3 else -(6 + 3 * i) * li)
        P.rot("ham", -cv(t, [(0, 0), (0.36, 4), (T, 16, "out"), (0.66, 10), (D, 0, "io")]))
        for g, names in gills.items():
            P.rot(names[1], 6 * tw)
        _ = lift
        feet(P)

    def cast_fn(t, P, D=1.2, T=0.5, E=0.95):
        """Súng Nước: ngửa ra hít (0–0,42), chúi tới há miệng phun đúng 0,5, giữ phun rung tới 0,95, về."""
        xfade(nen, P, t, D, 1 - 0.85 * hoat.bao(t, 0.05, 1.1, 0.2, 0.2), 0.3, 1.0)
        rear = cv(t, [(0, 0), (0.42, 1, "io"), (0.46, 1.05), (T, -0.65, "in"), (0.6, -0.75), (E, -0.65), (D, 0, "io")])
        P.rot("nguc", 6 * rear)
        P.rot("co", 3 * rear)
        P.rot("dau", 8 * rear + 1.2 * rung(t, T + 0.03, E))
        P.rot("ham", -(cv(t, [(0, 0), (0.42, 3, "io"), (T, 38, "out"), (E, 33), (D, 0, "io")]) + 3 * rung(t, T + 0.03, E)))
        P.move("move", cv(t, [(0, 0), (T, 0), (T + 0.08, -5, "out"), (E, -3), (D, 0, "io")]), 0)
        for g, names in gills.items():
            fl = cv(t, [(0, 0), (0.42, -6), (T + 0.05, 14, "out"), (E, 10), (D, 0, "io")])
            for i, b in enumerate(names):
                P.rot(b, fl * (0.6 + 0.4 * i) + 2 * rung(t, T + 0.03, E) * (i == 2))
        for tn, names in arms.items():
            P.rot(names[0], (8 if tn == "tay_n" else -6) * rear)
        feet(P)

    def skill_fn(t, P, D=1.8, T=0.95, E=1.45):
        """Cầu Mưa: dậm chân trái 0,28, phải 0,55, ngồi thụp 0,8, bật người, bầu dựng đứng, nút bật, cột nước phụt lên trời 0,95
        (gam), giữ rung ngửa đầu há miệng tới 1,45, về."""
        xfade(nen, P, t, D, 1 - 0.85 * hoat.bao(t, 0.05, 1.7, 0.2, 0.3), 0.6, 1.5)
        cr = cv(t, [(0, 0), (0.2, 0.25, "io"), (0.3, 0.05, "out"), (0.47, 0.25, "io"), (0.57, 0.05, "out"), (0.82, 1.0, "io"),
                    (T, -0.6, "out"), (E, -0.45), (D, 0, "io")])
        P.move("than", 0, -14 * max(cr, 0) + 10 * max(-cr, 0))
        P.rot("nguc", 5 * max(cr, 0) - 7 * max(-cr, 0) + 1.2 * rung(t, T + 0.03, E))
        P.rot("dau", -6 * max(cr, 0) + 12 * max(-cr, 0) + 1.5 * rung(t, T + 0.03, E))
        P.rot("ham", -cv(t, [(0, 0), (0.82, 0), (T, 30, "out"), (E, 26), (D, 0, "io")]) - 3 * rung(t, T + 0.03, E))
        up = cv(t, [(0, 0), (0.75, 0), (T, 1, "out"), (E, 1), (D, 0, "io")])
        P.rot("bau", -16 * up + 2 * rung(t, T + 0.03, E))
        P.move("bau", 0, 10 * up)
        if info["nut"]:
            pop = cv(t, [(0, 0), (0.9, 0), (1.05, 1, "out"), (1.25, 0.6, "in"), (1.45, 0.0, "in"), (D, 0)])
            P.move("nut", -30 * pop, 90 * pop)
            P.rot("nut", 160 * pop)
        for tn, names in arms.items():
            sg = 1 if tn == "tay_n" else -1
            P.rot(names[0], sg * (30 * up - 6 * max(cr, 0)))
            P.rot(names[1], sg * 18 * up)
        for g, names in gills.items():
            for i, b in enumerate(names):
                P.rot(b, (-8 + 3 * i) * up + 2.0 * rung(t, T + 0.03, E))
        for i, b in enumerate(duoi):
            P.rot(b, (2 + 1.5 * i) * up * (1 if i % 2 else -1))

        def stomp(c, t0):
            return cv(t, [(0, 0), (t0 - 0.12, 0), (t0 - 0.05, 1, "out"), (t0, 0, "in"), (D, 0)])
        W0 = sk.W0
        feet(P)
        for c, t0 in (("chan_t", 0.28), ("chan_p", 0.55)):
            s = stomp(c, t0)
            if s > 0:
                names = legs[c]
                Wc = sk.the_gioi(P)
                ank = foot[c][0]
                tgt = (Wc["move"] @ np.array([ank[0], ank[1] + 26 * s, 1.0]))[:2]
                hoat.ik_hai_doan(sk, P, names[0], names[1], tgt)
        _ = W0

    def hit_fn(t, P, D=0.6):
        xfade(nen, P, t, D, 1 - 0.75 * hoat.bao(t, 0.0, 0.5, 0.05, 0.15), 0.2, 0.5)
        hd = cv(t, [(0, 0), (0.07, 1, "out"), (0.2, 0.55, "io"), (0.42, -0.12, "io"), (D, 0, "io")])
        bd = cv(t, [(0, 0), (0.07, 0.3, "out"), (0.2, 1, "io"), (0.44, -0.05, "io"), (D, 0, "io")])
        P.rot("dau", 12 * hd)
        P.rot("nguc", 6 * bd)
        P.move("move", -8 * bd, 0)
        P.rot("ham", -10 * hd)
        blink(P, t, [(0.03, 0.32)])
        P.rot("bau", -8 * bd)
        for g, names in gills.items():
            for i, b in enumerate(names):
                P.rot(b, (5 + 3 * (2 - i)) * cv(t, [(0, 0), (0.07 + 0.03 * (2 - i), 1, "out"), (0.32, -0.3, "io"), (D, 0, "io")]))
        for i, b in enumerate(duoi):
            P.rot(b, (4 + 1.5 * i) * cv(t, [(0, 0), (0.07 + 0.025 * (nd - 1 - i), 1, "out"), (0.35 + 0.02 * i, -0.3, "io"), (D, 0, "io")]))
        for tn, names in arms.items():
            P.rot(names[0], (-10 if tn == "tay_n" else 8) * hd)
        feet(P)

    def die_fn(t, P, D=1.6):
        nen(P, t, max(0.0, 1 - t / 0.3))
        P.rot("dau", cv(t, [(0, 0), (0.07, 14, "out"), (0.3, 6), (0.75, -22, "io"), (D, -24)]))
        P.rot("ham", -cv(t, [(0, 0), (0.07, 16, "out"), (0.3, 6), (0.75, 18, "io"), (D, 18)]))
        P.rot("nguc", cv(t, [(0, 0), (0.07, 6, "out"), (0.7, -14, "io"), (D, -14)]))
        P.move("than", 0, cv(t, [(0, 0), (0.3, 0), (0.7, -26, "io"), (D, -26)]))
        P.rot("bau", cv(t, [(0, 0), (0.4, 0), (0.9, 38, "in"), (1.0, 32, "out"), (D, 34)]))
        P.move("bau", cv(t, [(0, 0), (0.4, 0), (0.9, -40, "in"), (D, -44)]), cv(t, [(0, 0), (0.4, 0), (0.9, -70, "in"), (1.0, -62), (D, -64)]))
        # đổ ngửa ra sau quanh điểm chạm đất phía sau (gốc đuôi), đuôi xoay bù để nằm dọc mặt đất
        fall = cv(t, [(0, 0), (0.85, 0), (1.18, 78, "in"), (1.27, 70, "out"), (1.36, 74, "io"), (D, 73)])
        piv = sk.W0[duoi[1]][:2, 2].copy()
        piv[1] = 6.0
        c_, s_ = math.cos(math.radians(fall)), math.sin(math.radians(fall))
        P.rot("move", fall)
        P.move("move", piv[0] - (c_ * piv[0] - s_ * piv[1]), piv[1] - (s_ * piv[0] + c_ * piv[1]))
        P.rot(duoi[0], -0.9 * fall)
        blink(P, t, [(0.04, D + 1)])
        for tn, names in arms.items():
            P.rot(names[0], cv(t, [(0, 0), (0.7, (-25 if tn == "tay_n" else 20), "io"), (D, (-25 if tn == "tay_n" else 20))]))
        for g, names in gills.items():
            for i, b in enumerate(names):
                P.rot(b, cv(t, [(0, 0), (0.7, -8 - 3 * i, "io"), (D, -8 - 3 * i)]))
        if t < 0.85:
            feet(P)
        else:   # chân hổng đất: co lên dần
            k_ = ease((t - 0.85) / 0.3)
            for c, names in legs.items():
                P.rot(names[0], 25 * k_)
                P.rot(names[1], -30 * k_)
        a = cv(t, [(0, 1), (1.25, 1), (1.56, 0, "io"), (D, 0)])
        fade_all(sk, P, a, an=("mi_n", "mi_x"))

    return [Clip("appear", 1.2, appear_fn),
            Clip("idle", DI, idle_fn, loop=True),
            Clip("attack", 1.0, attack_fn, ev=[(0.48, "trung", "")]),
            Clip("cast", 1.2, cast_fn, ev=[(0.5, "phun", ""), (0.95, "het_phun", "")]),
            Clip("skill", 1.8, skill_fn, ev=[(0.95, "gam", ""), (0.97, "bat_nut", ""), (1.45, "het_gam", "")]),
            Clip("hit", 0.6, hit_fn),
            Clip("die", 1.6, die_fn)]


# ---------------------------------------------------------------- dựng + xuất
def rig(k):
    t0 = time.time()
    if k == 2:
        import tm06_d2
        sk2, info2, cl2, fr2, tong = tm06_d2.rig2()
        return sk2, info2, cl2, fr2
    import tm06_d2
    sk2, info2 = tm06_d2.dung2(mat_do=2.2, ti_anh=0.62)   # bản lưới thưa, ảnh nhỏ hơn chỉ để gộp vào evolve (dạng 2 đủ dày ở tm06_2)
    cl2 = tm06_d2.clips2(sk2, info2)
    fr2 = {c.ten: hoat.nuong(sk2, c) for c in cl2}
    sk1, info1 = dung1()
    cl1 = clips1(sk1, info1)
    fr1 = {c.ten: hoat.nuong(sk1, c) for c in cl1}
    ra = inbox(1, "rig")
    os.makedirs(ra, exist_ok=True)
    iou = so_concept(sk1, fr1["idle"][0], 1, info1["D"], os.path.join(ra, "so_concept.png"))
    ld = lech_dau(sk1, fr1, cl1)
    for n, (d, w) in ld.items():
        print(f"  khung 0 {n} lệch khung 0 idle {d:.2f} px ({w})")
    ve1, ve2 = soi.Ve(sk1), soi.Ve(sk2)
    hA, hB = soi.chieu_cao(ve1, fr1["idle"][0]), soi.chieu_cao(ve2, fr2["idle"][0], tm06_d2.BO_CAO)
    hB_game = tm06_d2.cao_game(sk2, fr2)
    tiB = hA / hB_game
    M = tienhoa.gop(sk1, sk2)

    def gong(t, P):
        sq = cv(t, [(0, 0), (0.3, -0.07), (0.45, 0.06, "out"), (1.0, 0.04), (1.3, 0.0)])
        P.scale("move", 1 - 0.5 * sq, 1 + sq)
        P.rot("dau", cv(t, [(0, 0), (0.3, -5), (0.6, 12, "out"), (1.3, 14)]) + 1.5 * rung(t, 0.5, 1.3))
        P.rot("ham", -cv(t, [(0, 0), (0.5, 0), (0.7, 18, "out"), (1.3, 20)]))
        P.rot("bau", -10 * cv(t, [(0, 0), (0.5, 1, "io"), (1.3, 1)]))

    def gam(t, P, fl):
        tm06_d2.gam_evolve(P, fl, "n_")

    ev = tienhoa.clip_tien_hoa(M, sk1, sk2, fr2["idle"][0], tiB=tiB, fnA=gong, fnB=gam)
    clM = cl1 + [ev]
    frM = dict(fr1)
    frM["evolve"] = hoat.nuong(M, ev)
    _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, fr2["idle"][0], tiB)
    noi = {"evolve": s_ev + f" (dạng sau co {tiB:.3f} trong rig gộp)"}
    for n, (d, w) in ld.items():
        noi[n + " (khung 0)"] = f"khung 0 lệch khung 0 idle {d:.2f} px" + (f" ({w})" if w else "")
    noi["so_concept"] = f"IoU khung 0 idle / concept {iou:.3f}; IoU ghép mảnh (place) {info1['D'].iou_ghep}"
    tk1 = sk1.tom_tat()
    noi["mat_do"] = (f"{tk1['dinh']} đỉnh / cao {info1['D'].cao:.0f} px rig (bước viền {info1['D'].bv:.1f}, trong "
                     f"{info1['D'].bt:.1f}; riêng dạng 1, chưa gộp)")
    tong = xuat.xuat_het(M, clM, ra, f"{CODE}_1", f"{TEN[1]} (dạng 1, gộp tiến hóa)", frames=frM, dang=1, so_dang=2,
                         dung_yen=("attack", "cast", "skill"), ma_goc=3241, noi_them=noi,
                         can=[("can_mieng_cast", "cast", 0.62, "ham", 70), ("can_duoi_attack", "attack", 0.48, "duoi2", 120),
                              ("can_mi_hit", "hit", 0.1, "dau", 80), ("can_bau_skill", "skill", 1.05, "bau", 110),
                              ("can_chan_skill", "skill", 0.28, "chan_t1", 80)])
    uon_thu(sk1, [info1["duoi"]] + list(info1["gills"].values()), os.path.join(ra, "uon_thu.png"))
    print(f"xong dạng 1 {time.time() - t0:.1f} s; .atomik {tong['atomik_kb']:.0f} KB")
    return sk1, info1, cl1, fr1


def main(argv):
    if not argv:
        print(__doc__)
        return
    cmd = argv[0]
    if cmd == "cat":
        cat(int(argv[1]))
    elif cmd == "rig":
        rig(int(argv[1]))
    elif cmd == "all":
        rig(2)
        rig(1)


if __name__ == "__main__":
    main(sys.argv[1:])
