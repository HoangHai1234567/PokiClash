# -*- coding: utf-8 -*-
"""tm02 Thạch Giải (cua ẩn sĩ cõng nhà đá), pha 2: rig dựng bằng mã từ các lớp cắt thẳng từ concept (tm02_lai.py), mắt nhắm làm
từ chính mắt concept, lòng miệng từ tờ GPT M01. Thư viện ArtGen/Spine/quai.

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm02_lai.py 2        (cắt lớp; tương tự cho 1)
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm02.py 2     (dạng 2: rig, clip, xuất)
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm02.py 1     (dạng 1 + gộp dạng 2 cho clip evolve)

Ra inbox/tm02_<k>/rig/.
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
from quai.hoat import Clip, DayMem, LoXo, an_hien, bao, chuoi_song, cv, ease, lui, rung, song  # noqa: E402
from quai.khung import Dat  # noqa: E402

CODE = "tm02"


def path(k, *a):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", *a)


# ---------------------------------------------------------------- cấu hình từng dạng (toạ độ concept px)
CFG = {
    2: dict(
        ten="Thạch Thành Giải", S=0.44, G=(625, 990),
        than=(830, 650), nha=(560, 720), dau=(930, 600), dau_vung=[(915, 480), (1080, 480), (1080, 700), (915, 700)],
        ham=((936, 650), (1016, 650)), mom=(1036, 612),
        mat={"mat0": [(866, 548), (878, 512), (874, 470)], "mat1": [(956, 548), (972, 505), (1003, 462)]},
        rau=["rau0", "rau1"], rong=["rong0", "rong1"], san_ho={"sh0": (360, 192), "sh1": (412, 172), "sh2": (470, 228),
                                                              "sh3": (572, 336), "sh4": (650, 390)},
        chan=["chan0", "chan1", "chan2", "chan3"],
        # càng: (lớp tay, lớp lòng càng, lớp ngón động, khớp tay [vai, khuỷu, cổ tay], (gốc lòng, hướng lòng), (khớp ngón, ngọn ngón))
        cang={"c1": ("cang1_tay", "cang1", "cang1_ngon", [(1040, 640), (1095, 548), (1150, 465)], ((1150, 465), (1300, 300)),
                     ((1240, 200), (1385, 218))),
              "c2": ("cang2_tay", "cang2", "cang2_ngon", [(866, 772), (1005, 724), (1140, 672)], ((1140, 672), (1405, 630)),
                     ((1190, 722), (1385, 668)))},
        mieng=("c1", (1150, 300), (1398, 268)),      # chỗ nhả chiêu cast: càng búa (gốc trục, miệng càng)
        mieng_mom=True,
        trong=("M01", (990, 652), 74),               # lòng miệng: tờ, tâm đặt, bề rộng (px concept)
        # mặt nạ (lồi): bên phải mép trong vành cửa; trên cao chéo lên phải để càng búa giơ cao, mắt vẫn trong mặt nạ
        cat=[(4000, -2500), (4000, 3500), (660, 3500), (628, 770), (606, 700), (602, 620), (616, 540), (650, 488), (722, 466),
             (1260, -2500)],
        dong=2,
    ),
    1: dict(
        ten="Thạch Giải", S=0.40, G=(588, 905),
        than=(820, 560), nha=(540, 640), dau=(860, 560), dau_vung=[(760, 420), (1010, 420), (1010, 670), (760, 670)],
        ham=((846, 640), (918, 638)), mom=(928, 618),
        mat={"mat0": [(788, 508), (792, 466), (818, 398)], "mat1": [(938, 518), (940, 466), (964, 398)]},
        rau=["rau0", "rau1"], rong=["rong0", "rong1", "rong2"], san_ho={},
        chan=["chan0", "chan1", "chan2", "chan3"],
        # càng liền một lớp: ngón động bẻ bằng trọng số (phần tử thứ 7: vùng ngón động, toạ độ concept)
        cang={"c1": ("cang1_tay", "cang1", None, [(690, 640), (830, 685), (975, 690)], ((975, 690), (1292, 668)),
                     ((1180, 722), (1272, 724)), [(1168, 706), (1310, 700), (1310, 830), (1168, 830)]),
              "c2": ("cang2_tay", "cang2", None, [(990, 572), (1040, 536), (1095, 490)], ((1095, 490), (1122, 370)),
                     ((1152, 470), (1190, 396)), [(1150, 375), (1205, 375), (1205, 495), (1150, 495)])},
        mieng=("dau", (880, 620), (930, 618)),       # chiêu cast (Bọt Nước) nhả từ miệng
        mieng_cang=("c1", (1150, 690), (1296, 672)), # đòn thường (Búng Càng) nhả từ khe càng búa
        mieng_mom=False,
        trong=("M01", (880, 642), 62),
        cat=[(4000, -2500), (4000, 3500), (690, 3500), (668, 726), (645, 690), (632, 600), (640, 500), (660, 432), (700, 404), (760, 396),
             (740, -2500)],
        dong=1,
    ),
}


# ---------------------------------------------------------------- dựng rig
class Rig:
    def __init__(self, k):
        self.k = k
        c = self.c = CFG[k]
        self.S = c["S"]
        self.GX, self.GY = c["G"]
        self.lai = json.load(open(path(k, "manh_lai", "lai.json"), encoding="utf-8"))
        self.sk = khung.Sk(f"{CODE}_{k}")
        self.img = {}
        self.dat = {}

    def R(self, x, y):
        return ((x - self.GX) * self.S, (self.GY - y) * self.S)

    def RA(self, pts):
        return np.array([self.R(*p) for p in pts], float)

    def nap(self, n, src=None):
        """lớp cắt từ concept: co theo S, loang màu; Dat đặt góc trên trái đúng chỗ trong concept."""
        t = self.lai["lop"][n.replace("_nham", "")]
        im = Image.open(src or path(self.k, "manh_lai", n + ".png")).convert("RGBA")
        aw, ah = max(2, round(t["w"] * self.S)), max(2, round(t["h"] * self.S))
        im = anh.loang_mau(im.resize((aw, ah), Image.LANCZOS))
        self.sk.anh(n, im)
        self.img[n] = im
        self.dat[n] = Dat(*self.R(t["x0"], t["y0"]), ti=(t["w"] * self.S / aw, t["h"] * self.S / ah), neo=(0.0, 0.0))
        return im

    def to_img(self, n, pts):
        t = self.lai["lop"][n.replace("_nham", "")]
        im = self.img[n]
        return [((x - t["x0"]) * im.width / t["w"], (y - t["y0"]) * im.height / t["h"]) for x, y in pts]

    def truc(self, n, ext):
        """trục dải theo đường giữa "cl" (gốc → ngọn), nối dài ext px concept về phía gốc (phần mọc thêm dưới lớp trên)."""
        t = self.lai["lop"][n]
        cl = [tuple(p) for p in t["cl"]]
        p0, p1 = np.array(cl[0], float), np.array(cl[1], float)
        u = (p0 - p1) / (np.linalg.norm(p0 - p1) + 1e-9)
        return [tuple(p0 + u * ext)] + cl

    def H(self):
        return self.c.get("H_rig") or (self.GY - 30) * self.S

    def build(self):
        sk, c, S = self.sk, self.c, self.S
        Hr = self.c["H_rig"] = (self.GY - min(t["y0"] for t in self.lai["lop"].values())) * S
        names = list(self.lai["lop"])
        for n in names:
            self.nap(n)
        for n in c["mat"]:
            self.nap(n + "_nham", path(self.k, "manh_lai", n + "_nham.png"))
        # lòng miệng (tờ GPT M01, ô trên phải)
        tr_src, tr_c, tr_w = c["trong"]
        to = anh.doc_to(anh.to_moi_nhat(path(self.k, "tai_ve"), tr_src))
        cand = [m for m in to.manh if m["x0"] > 1000 and m["y1"] < 520]
        tm = max(cand, key=lambda m: m["dt"])
        im = anh.cat_manh(to, tm)
        k_ = tr_w * S / im.width
        im = anh.loang_mau(im.resize((max(2, round(im.width * k_)), max(2, round(im.height * k_))), Image.LANCZOS))
        sk.anh("mieng_trong", im)
        self.img["mieng_trong"] = im

        # ---- xương
        sk.xuong("root")
        sk.xuong("shadow", "root")
        sk.xuong("move", "root")
        sk.xuong("than", "move", *self.R(*c["than"]), dai=60, the_gioi=True)
        sk.xuong("nha", "move", *self.R(*c["nha"]), dai=80, the_gioi=True)
        sk.xuong("dau", "than", *self.R(*c["dau"]), dai=60, the_gioi=True)
        h0, h1 = self.RA(c["ham"])
        gj = math.degrees(math.atan2(*(h1 - h0)[::-1]))
        sk.xuong("ham", "dau", *h0, goc=gj, dai=float(np.hypot(*(h1 - h0))), the_gioi=True)
        if c.get("mieng_mom"):
            sk.xuong("mieng_mom", "dau", *self.R(*c["mom"]), goc=0, dai=40, the_gioi=True)
        self.chain = {}
        for n, J in c["mat"].items():
            self.chain[n] = sk.chuoi(n, "dau", self.RA(J))
        for n, (bx, by) in c["san_ho"].items():
            sk.xuong(n, "nha", *self.R(bx, by), goc=90, dai=40, the_gioi=True)
        # càng
        for key, (tay, long, ngon, J, (pa, pb), (fa, fb), *_vn) in c["cang"].items():
            self.chain[tay] = sk.chuoi("t" + key[1], "than", self.RA(J))
            A, B = self.RA([pa, pb])
            sk.xuong("k" + key[1], self.chain[tay][-1], *A, goc=math.degrees(math.atan2(*(B - A)[::-1])), dai=float(np.hypot(*(B - A))),
                     the_gioi=True)
            A2, B2 = self.RA([fa, fb])
            sk.xuong("n" + key[1], "k" + key[1], *A2, goc=math.degrees(math.atan2(*(B2 - A2)[::-1])), dai=float(np.hypot(*(B2 - A2))),
                     the_gioi=True)
        for bn in ("mieng", "mieng_cang"):
            if not c.get(bn):
                continue
            mk, ma, mb = c[bn]
            A, B = self.RA([ma, mb])
            par = ("k" + mk[1]) if mk.startswith("c") else mk
            sk.xuong(bn, par, *B, goc=math.degrees(math.atan2(*(B - A)[::-1])), dai=40, the_gioi=True)

        # ---- dải lưới (chân, râu, rong, tay càng): trục theo đường giữa
        self.L, self.W = {}, {}
        dai = {}
        for n in c["chan"]:
            dai[n] = (3, "than", 0.75, 40)
        for n in c["rau"]:
            dai[n] = (6, "dau", 0.6, 30)
        for n in c["rong"]:
            dai[n] = (4, "nha", 0.6, 0)
        for key, (tay, *_r) in c["cang"].items():
            dai[tay] = (2, "than", 0.75, 36)
        for n, (nseg, par, hoa, ext) in dai.items():
            im = self.img[n]
            if n in self.chain:   # tay càng: trục qua khớp đã cho
                J = c["cang"]["c" + n[4]][3]
                p0, p1 = np.array(J[0], float), np.array(J[1], float)
                u = (p0 - p1) / np.linalg.norm(p0 - p1)
                ax = [tuple(p0 + u * ext)] + [tuple(p) for p in J]
            else:
                ax = self.truc(n, ext) if ext else [tuple(p) for p in self.lai["lop"][n]["cl"]]
            Lx = luoi.luoi_dai(im, nseg, truc=self.to_img(n, ax), buoc_theo_cao=Hr, mu=True, ten=n)
            Jw = self.dat[n].ra(Lx.khop(nseg), im.width, im.height)
            if n not in self.chain:
                self.chain[n] = sk.chuoi(n, par, Jw)
            if Lx.ho > 0:
                # dải không phủ hết (mảnh rời, mép lồi xa trục): lưới vùng đều + trọng số B-spline chiếu lên trục
                Lx = luoi.luoi_vung(im, buoc_theo_cao=Hr, ten=n + " (vùng)")
                Q = self.dat[n].ra(Lx.pts, im.width, im.height)
                Wx = trongso.chuoi_chieu(Q, Jw, self.chain[n], cha=par, cha_hoa=hoa)
            else:
                Wx = trongso.chuoi(Lx.s, Lx.truc[1][-1] / nseg, self.chain[n], cha=par, cha_hoa=hoa)
            self.L[n], self.W[n] = Lx, Wx

        # ---- slot (thứ tự vẽ sau → trước) + mặt nạ
        first_masked = names[names.index("rau1") + 1] if "rau1" in names else None
        for n in names:
            if n == first_masked:
                sk.slot("cat", "nha")
            bone = self._bone_of(n)
            if n == "than":
                sk.slot("mieng_trong", "ham", "mieng_trong")
            sk.slot(n, bone, n)
            if n in c["mat"]:
                sk.slot(n + "_nham", self.chain[n][-1], n + "_nham", an=True)
        # mặt nạ phải lồi: bao lồi của vành trong cửa + các điểm phải hiện (mắt, càng búa giơ cao); phần lấn sang đá là mẩu nhỏ
        hull = anh.bao_loi([tuple(p) for p in c["cat"]])
        sk.cat("cat", names[names.index("vanh") - 1], self.RA(hull))

        # ---- lưới + trọng số
        for n in names:
            im = self.img[n]
            dat = self.dat[n]
            if n in self.L:
                sk.luoi_gan(n, n, self.L[n], self.W[n], dat=dat)
                continue
            # đá cứng thật (nhà đá, vành cửa) không uốn: lưới thưa hơn 1,8 lần cho nhẹ file; thân, mặt, chi, càng giữ mật độ đích
            Lv = luoi.luoi_vung(im, buoc_theo_cao=Hr * (1.8 if n in ("thap", "vanh") else 1.0), ten=n)
            Q = dat.ra(Lv.pts, im.width, im.height)
            if n in c["mat"]:
                Wv = trongso.chuoi_chieu(Q, self.RA(c["mat"][n]), self.chain[n], cha="dau", cha_hoa=0.7)
                sk.luoi_gan(n, n, Lv, Wv, dat=dat)
                sk.luoi_gan(n + "_nham", n + "_nham", Lv, Wv, dat=self.dat[n + "_nham"])
            elif n == "than":
                poly = self.to_img(n, c["dau_vung"])
                Wv = trongso.vung(Lv, [("dau", poly), ("than", [(0, 0), (im.width, 0), (im.width, im.height), (0, im.height)])],
                                  dai_hoa=0.09 * Hr)
                Wv = trongso.lam_tron(Lv, Wv, 2)
                sk.luoi_gan(n, n, Lv, Wv, dat=dat)
            elif any(n == v[1] and v[2] is None for v in c["cang"].values()):
                key = next(kk for kk, v in c["cang"].items() if v[1] == n)
                poly = self.to_img(n, c["cang"][key][6])
                Wv = trongso.vung(Lv, [("n" + key[1], poly), ("k" + key[1], [(0, 0), (im.width, 0), (im.width, im.height), (0, im.height)])],
                                  dai_hoa=0.05 * Hr)
                Wv = trongso.lam_tron(Lv, Wv, 2)
                sk.luoi_gan(n, n, Lv, Wv, dat=dat)
            elif n == "ham":
                Wv = mieng.ham_hai_xuong(Q, h0, h1, "dau", "ham", u0=0.05, u1=0.4)
                sk.luoi_gan(n, n, Lv, Wv, dat=dat)
            else:
                b = self._bone_of(n)
                sk.luoi_gan(n, n, Lv, trongso.cung(Lv.n, b), dat=dat)
        # lòng miệng: mảnh cứng trên hàm, tâm ở chỗ khe môi
        im = self.img["mieng_trong"]
        sk.manh("mieng_trong", "mieng_trong", Dat(*self.R(*c["trong"][1]), ti=1.0))
        for e, m_ in (("trung", "khung đòn trúng / nện chạm đất"), ("phun", "bắt đầu nhả (VFX bám xương mieng)"), ("het_phun", "hết nhả"),
                      ("gam", "chiêu cuối bung"), ("het_gam", "hết chiêu cuối"), ("nen", "càng nện đất"), ("xoay", "xoáy nước dưới chân đối thủ"),
                      ("troi", "cột đá trồi")):
            sk.su_kien(e, m_)
        foot = {}
        W0 = sk.the_gioi()
        for n in c["chan"]:
            ch = self.chain[n]
            foot[n] = (W0[ch[2]][:2, 2].copy(), math.degrees(math.atan2(W0[ch[2]][1, 0], W0[ch[2]][0, 0])))
        self.foot = foot
        print(f"rig dạng {self.k}: {sk.tom_tat()}  cao {Hr:.0f} px rig")
        return sk

    def _bone_of(self, n):
        c = self.c
        if n in ("thap", "vanh") or n.startswith("thap"):
            return "nha"
        if n in c["san_ho"]:
            return n
        if n in ("than",):
            return "than"
        if n == "ham":
            return "ham"
        for key, (tay, long, ngon, *_r) in c["cang"].items():
            if n == long:
                return "k" + key[1]
            if ngon and n == ngon:
                return "n" + key[1]
            if n == tay:
                return self.chain[tay][0]
        if n in self.chain:
            return self.chain[n][0]
        return "than"


# ---------------------------------------------------------------- clip
def clips_cho(rig):
    sk, c, k = rig.sk, rig.c, rig.k
    Hr = c["H_rig"]
    u = Hr / 100.0                       # 1 u = 1% chiều cao
    ch = rig.chain
    legs = c["chan"]
    t1, t2 = ch[c["cang"]["c1"][0]], ch[c["cang"]["c2"][0]]
    rau = [ch[n] for n in c["rau"]]
    rong = [ch[n] for n in c["rong"]]
    mats = [ch[n] for n in c["mat"]]
    sh = list(c["san_ho"])
    D_IDLE = 2.4 if k == 2 else 2.0
    soft = []
    for r_ in rau:
        soft.append(LoXo(r_, k=[260, 220, 185, 150, 120, 95], damp=0.6, maxang=12))
    for r_ in rong:
        soft.append(LoXo(r_, k=[200, 160, 130, 100], damp=0.62, maxang=14))
    for m_ in mats:
        soft.append(LoXo(m_, k=[420, 340], damp=0.55, maxang=8))

    def giu_chan(P, dx, dy=0.0):
        """thân dời (dx, dy) mà gốc chân đứng yên (chân nằm dưới nhà đá, không bị kéo theo khi thân thụt vào)."""
        for n in legs:
            P.move(ch[n][0], -dx, -dy)

    def feet(P, lift=None):
        W = sk.the_gioi(P)
        for n in legs:
            names = ch[n]
            pos, ang = rig.foot[n]
            tgt = (W["move"] @ np.array([pos[0], pos[1], 1.0]))[:2]
            if lift and n in lift:
                tgt = tgt + np.array(lift[n])
            hoat.ik_hai_doan(sk, P, names[0], names[1], tgt)
            W2 = sk.the_gioi(P)
            cur = math.degrees(math.atan2(W2[names[2]][1, 0], W2[names[2]][0, 0]))
            P.rot(names[2], ((ang + math.degrees(math.atan2(W2["move"][1, 0], W2["move"][0, 0])) - cur + 180) % 360) - 180)

    def z(t, T, ph=0.0):
        """sin trừ giá trị ở t = 0: mọi dao động idle bằng 0 ở khung 0 (khung 0 idle = dáng concept)."""
        return song(t, T, ph) - math.sin(ph)

    def cs(P, bones, t, T, amps, **kw):
        a_, b_ = khung.Pose(), khung.Pose()
        chuoi_song(a_, bones, t, T, amps, **kw)
        chuoi_song(b_, bones, 0.0, T, amps, **kw)
        for bn in bones:
            P.rot(bn, a_.t[bn][2] - b_.t[bn][2])

    def nen(P, t, amp=1.0, D=None):
        """chuyển động nền idle (giờ t, vòng D_IDLE): nhún hai lần một vòng, nhà đá trễ nửa nhịp, càng thở, phụ kiện lệch pha.
        Clip không lặp (D = độ dài clip): biên độ nhân bao 0 → 1 → 0 nên khung 0 và khung cuối đúng dáng khung 0 idle."""
        T = D_IDLE
        if D:
            amp = amp * bao(t, 0, D, 0.3 * D, 0.3 * D)
        P.move("than", 0, -1.0 * u * z(t, T / 2) * amp)
        P.rot("than", 0.8 * z(t, T, 0.3) * amp)
        P.move("nha", 0, -0.8 * u * z(t, T / 2, -0.9) * amp)
        P.rot("nha", -0.7 * z(t, T, 1.4) * amp)
        P.rot("dau", 1.6 * z(t, T, 1.0) * amp)
        for i, b in enumerate(t1):
            P.rot(b, (2.2 + 1.4 * i) * z(t, T, 0.5 + 0.35 * i) * amp)
        P.rot("k1", -2.5 * z(t, T, 1.2) * amp)
        for i, b in enumerate(t2):
            P.rot(b, (1.6 + 1.0 * i) * z(t, T, 2.0 + 0.35 * i) * amp)
        P.rot("k2", 2.0 * z(t, T, 2.6) * amp)
        for j, m_ in enumerate(mats):
            cs(P, m_, t, T, [3.0 * amp, 4.0 * amp], tre=0.12, pha=1.7 * j)
        for j, r_ in enumerate(rau):
            cs(P, r_, t, T, [v * amp for v in (1.5, 2, 2.6, 3.2, 3.8, 4.4)], tre=0.1, ngon_dan=False, pha=0.9 * j)
        for j, r_ in enumerate(rong):
            cs(P, r_, t, T, [v * amp for v in (3, 5, 7, 9)], tre=0.16, ngon_dan=False, pha=2.1 * j)
        for j, b in enumerate(sh):
            P.rot(b, 1.6 * z(t, T, 0.8 * j) * amp)

    def idle_fn(t, P):
        nen(P, t)
        # điểm phá nhịp: kìm lưỡi cưa bập hai cái (học con gốc), chớp mắt, càng búa hé ngón
        P.rot("n2", -cv(t, [(0, 0), (1.45, 0), (1.52, 14, "out"), (1.6, 1), (1.67, 12, "out"), (1.76, 0, "io"), (D_IDLE, 0)]))
        P.rot("n1", cv(t, [(0, 0), (0.55, 0), (0.7, 9, "out"), (0.95, 0, "io"), (D_IDLE, 0)]))
        for n in c["mat"]:
            an_hien(P, n + "_nham", t, [(1.0, 1.12)] if n == "mat0" else [(1.02, 1.14)])
        feet(P)

    def appear_fn(t, P, D=1.6):
        a = cv(t, [(0, 0), (0.1, 1)])
        for s_ in sk.slots:
            if s_["alpha"] > 0 and s_["name"] != "cat":
                P.alpha[s_["name"]] = a
        drop = cv(t, [(0, 60 * u), (0.32, 0, "in"), (0.42, 3 * u, "out"), (0.52, 0, "in"), (D, 0)])
        sq = cv(t, [(0, 0), (0.32, 0), (0.36, 1, "out"), (0.5, 0, "io"), (D, 0)])
        P.move("move", 0, drop)
        P.scale("move", 1 + 0.06 * sq, 1 - 0.1 * sq)
        out = cv(t, [(0, 1), (0.6, 1), (1.05, 0, "out"), (D, 0)])       # 1 = thụt hẳn trong nhà
        P.move("than", -0.52 * Hr * out, -2 * u * out)
        hid = min(1.0, 1.6 * out)
        for n in [x for x in legs + list(c["cang"]["c2"][:3]) + list(c["cang"]["c1"][:3]) + c["rau"] if x]:
            P.alpha[n] = a * (1 - hid)
        P.rot("t10", -40 * out)
        P.rot("t20", -20 * out)
        P.scale("k1", 1 - 0.4 * out, 1 - 0.4 * out)
        P.scale("k2", 1 - 0.4 * out, 1 - 0.4 * out)
        nen(P, t, D=D, amp=ease((t - 1.0) / 0.5))
        for r_ in rau:
            for i, b in enumerate(r_):
                P.rot(b, -10 * out)
        P.rot("t1" + "0", cv(t, [(0, 0), (1.05, 0), (1.22, 14, "out"), (1.45, 0, "io"), (D, 0)]))
        P.rot("ham", -cv(t, [(0, 0), (1.05, 0), (1.2, 16, "out"), (1.45, 0, "io"), (D, 0)]))
        feet(P)

    def attack_fn(t, P, D=1.1, H=0.55):
        """Búa Càng: giơ găng đá cao, lấy đà dài, nện xuống đất tại chỗ, giữ có trôi, về."""
        up = cv(t, [(0, 0), (0.12, -0.15, "io"), (0.42, 1, "io"), (0.47, 1.05), (H, -1, "in"), (0.6, -0.9, "out"), (0.8, -0.85), (D, 0, "io")])
        nen(P, t, D=D, amp=1 - 0.75 * bao(t, 0.05, D - 0.05, 0.15, 0.25))
        P.rot("t10", (-4 if up > 0 else 55) * up)
        P.rot("t11", (2 if up > 0 else 30) * up)
        P.rot("k1", (36 if up > 0 else 36) * up)
        P.rot("n1", 16 * max(0.0, up))
        P.rot("than", 3.5 * up)
        P.move("than", -2.5 * u * max(0.0, up) + 2.5 * u * max(0.0, -up), -1.2 * u * max(0.0, -up))
        P.rot("nha", 2.0 * up)
        P.rot("dau", 2.5 * up)
        P.rot("ham", -10 * bao(t, 0.3, 0.75, 0.1, 0.15))
        sm = cv(t, [(0, 0), (H - 0.03, 0), (H, 1), (H + 0.06, -0.3), (H + 0.14, 0), (D, 0)])
        P.scale("k1", 1 + 0.1 * sm, 1 - 0.08 * sm)
        P.move("move", 0, -0.6 * u * bao(t, H, H + 0.12, 0.02, 0.08))
        feet(P)

    def cast_fn(t, P, D=1.6, H=0.62, E=1.25):
        """Pháo Áp Suất: chĩa càng búa về đối thủ, ngón bập liên hồi nhả tia nước áp suất (VFX bám xương mieng), giữ rung, về."""
        aim = cv(t, [(0, 0), (0.42, 1, "io"), (E, 1), (D, 0, "io")])
        kick = cv(t, [(0, 0), (0.5, 0), (0.58, -0.4, "io"), (H, 1, "out"), (H + 0.12, 0.35, "io"), (E, 0.3), (D, 0, "io")])
        nen(P, t, D=D, amp=1 - 0.8 * bao(t, 0.05, D - 0.05, 0.2, 0.3))
        r = rung(t, H + 0.05, E)
        P.rot("t10", -30 * aim + 4 * kick + 1.2 * r)
        P.rot("t11", -12 * aim + 3 * kick)
        P.rot("k1", -26 * aim + 5 * kick + 1.0 * r)
        snap = 0.0
        if H <= t < E:
            ph = ((t - H) / 0.13) % 1.0
            snap = 1 - ph if ph > 0.25 else ph / 0.25
        P.rot("n1", 30 * cv(t, [(0, 0), (0.42, 1, "io"), (H, 1), (E, 1), (D, 0, "io")]) * (1 - 0.8 * snap * (H <= t < E)))
        P.move("than", -1.8 * u * kick, 0)
        P.rot("than", 2.0 * kick + 0.4 * r)
        P.rot("nha", 0.8 * r)
        P.rot("dau", -2.0 * aim)
        P.rot("ham", -8 * bao(t, 0.4, E, 0.1, 0.2))
        feet(P)

    def skill_fn(t, P, D=2.0):
        """Xoáy Thạch Thành: cúi tụ lực, giơ găng, nện hai lần, gầm giữ rung hai dáng (xoáy, cột đá ở chỗ đối thủ là VFX), về."""
        cr = cv(t, [(0, 0), (0.45, 1, "io"), (0.55, 1.05), (0.62, -0.2, "out"), (1.6, -0.2), (D, 0, "io")])
        arm = cv(t, [(0, 0), (0.45, 0.3, "io"), (0.6, 1.1, "out"), (0.68, -1, "in"), (0.76, 0.6, "out"), (0.86, 0.75), (0.95, -1, "in"),
                     (1.05, -0.85, "out"), (1.6, -0.8), (D, 0, "io")])
        nen(P, t, D=D, amp=1 - 0.85 * bao(t, 0.05, D - 0.05, 0.2, 0.35))
        r = rung(t, 0.98, 1.6)
        P.move("than", 0, -2.2 * u * max(cr, 0))
        P.move("nha", 0, -1.6 * u * max(cr, 0))
        P.rot("nha", 1.2 * r + 2.0 * max(cr, 0))
        P.rot("than", 1.0 * r - 2.0 * max(cr, 0))
        P.rot("t10", (-4 if arm > 0 else 55) * arm)
        P.rot("t11", (2 if arm > 0 else 30) * arm)
        P.rot("k1", (36 if arm > 0 else 36) * arm + 1.2 * r)
        P.rot("dau", 5 * bao(t, 0.95, 1.6, 0.06, 0.2) + 1.2 * r)
        P.rot("ham", -(20 * bao(t, 0.95, 1.6, 0.05, 0.2) + 3 * r * bao(t, 0.95, 1.6, 0.05, 0.2)))
        for j, b in enumerate(sh):
            P.rot(b, 3.0 * r * (1 if j % 2 else -1))
        for i, b in enumerate(t2):
            P.rot(b, -8 * max(cr, 0) + 6 * bao(t, 0.9, 1.6, 0.1, 0.2))
        P.rot("n2", -18 * bao(t, 0.95, 1.6, 0.06, 0.2))
        sm = cv(t, [(0, 0), (0.66, 0), (0.68, 1), (0.74, 0), (0.93, 0), (0.95, 1), (1.02, 0), (D, 0)])
        P.scale("k1", 1 + 0.1 * sm, 1 - 0.08 * sm)
        P.move("move", 0, -0.7 * u * (bao(t, 0.68, 0.76, 0.02, 0.05) + bao(t, 0.95, 1.05, 0.02, 0.06)))
        feet(P)

    def hit_fn(t, P, D=0.6):
        hd = cv(t, [(0, 0), (0.07, 1, "out"), (0.2, 0.6, "io"), (0.42, -0.1, "io"), (D, 0, "io")])
        bd = cv(t, [(0, 0), (0.07, 0.35, "out"), (0.2, 1, "io"), (0.44, -0.05, "io"), (D, 0, "io")])
        nen(P, t, D=D, amp=ease((t - 0.25) / 0.35))
        P.move("than", -6 * u * bd, -0.8 * u * bd)          # thụt nửa vào nhà
        giu_chan(P, -6 * u * bd, -0.8 * u * bd)
        P.rot("dau", 6 * hd)
        P.rot("nha", 1.5 * bd)
        for m_ in mats:   # cuống mắt cụp (ngọn trước)
            P.rot(m_[1], 16 * hd)
            P.rot(m_[0], 8 * bd)
        P.rot("t10", 10 * bd)
        P.rot("k1", 8 * hd)
        P.rot("t20", -6 * bd)
        P.rot("k2", -8 * hd)
        P.rot("ham", -6 * hd)
        for n in c["mat"]:
            an_hien(P, n + "_nham", t, [(0.03, 0.34)])
        feet(P)

    def die_fn(t, P, D=2.0):
        """giật, nhắm mắt, lả đi giữ một nhịp, thụt hẳn vào nhà, nhà đá lắc rồi đổ nghiêng, tan."""
        P.rot("dau", cv(t, [(0, 0), (0.07, 8, "out"), (0.3, 3), (0.7, -8, "io"), (D, -8)]))
        P.rot("ham", -cv(t, [(0, 0), (0.07, 14, "out"), (0.3, 6), (0.7, 18, "io"), (1.0, 8), (D, 8)]))
        sag = cv(t, [(0, 0), (0.12, 0), (0.6, 1, "io"), (D, 1)])
        P.rot("t10", -40 * sag)
        P.rot("t11", -18 * sag)
        P.rot("k1", -34 * sag)
        P.rot("t20", -12 * sag)
        for m_ in mats:
            P.rot(m_[1], 22 * sag)
        for r_ in rau:
            P.rot(r_[0], 16 * sag)
        P.move("than", 0, -1.5 * u * sag)
        ins = cv(t, [(0, 0), (0.75, 0), (1.15, 1, "in"), (D, 1)])
        P.move("than", -0.52 * Hr * ins, 0)
        tip = cv(t, [(0, 0), (1.1, 0), (1.25, -3), (1.38, 2.5), (1.5, 0, "io"), (1.62, 18, "in"), (1.72, 15, "out"), (D, 16)])
        P.rot("nha", tip)
        P.move("nha", -0.15 * u * tip, -0.2 * u * max(tip, 0))
        for n in c["mat"]:
            an_hien(P, n + "_nham", t, [(0.04, D + 1)])
        a = cv(t, [(0, 1), (1.62, 1), (1.95, 0, "io"), (D, 0)])
        leg_a = cv(t, [(0, 1), (0.8, 1), (1.1, 0, "io"), (D, 0)])
        thu = [x for x in legs + list(c["cang"]["c2"][:3]) + list(c["cang"]["c1"][:3]) + c["rau"] if x]
        than_a = cv(t, [(0, 1), (1.12, 1), (1.22, 0), (D, 0)])     # đã thụt hẳn vào nhà: tắt hẳn (nhà đổ thì mặt nạ xoay theo)
        trong = ["than", "ham", "mieng_trong"] + list(c["mat"]) + [m + "_nham" for m in c["mat"]]
        P.rot("t10", -30 * ins)
        P.scale("k1", 1 - 0.35 * ins, 1 - 0.35 * ins)
        P.scale("k2", 1 - 0.35 * ins, 1 - 0.35 * ins)
        for s_ in sk.slots:
            nm = s_["name"]
            if (s_["alpha"] > 0 or nm.endswith("_nham")) and nm != "cat":
                P.alpha[nm] = (a * (leg_a if nm in thu else 1.0) * (than_a if nm in trong else 1.0)
                               * (P.alpha.get(nm, 1.0) if nm.endswith("_nham") else 1.0))
        feet(P)

    def attack1(t, P, D=0.9, H=0.42):
        """Búng Càng (kiểu tôm gõ mõ): ngả về sau, giơ càng búa hé ngón, bập "tách" một nhát nhả viên đạn bọt áp suất (VFX bám xương
        mieng_cang), giật lùi nhẹ, giữ, về. Đứng tại chỗ."""
        up = cv(t, [(0, 0), (0.08, -0.12, "io"), (0.32, 1, "io"), (0.37, 1.05), (H, -0.5, "in"), (0.5, -0.4, "out"), (0.66, -0.35), (D, 0, "io")])
        nen(P, t, D=D, amp=1 - 0.7 * bao(t, 0.05, D - 0.05, 0.12, 0.2))
        P.rot("t10", 4 * up)
        P.rot("t11", 3 * up)
        P.rot("k1", 8 * up)
        P.rot("n1", -cv(t, [(0, 0), (0.3, 20, "io"), (0.38, 22), (H, -3, "in"), (0.48, 2, "out"), (0.6, 0), (D, 0)]))
        P.rot("than", 2.5 * up)
        P.move("than", -1.2 * u * max(0.0, up) - 1.6 * u * bao(t, H, 0.62, 0.02, 0.18), 0)
        P.rot("dau", 2.0 * up)
        P.rot("nha", 1.2 * up)
        sm = cv(t, [(0, 0), (H - 0.03, 0), (H, 1), (H + 0.05, -0.3), (H + 0.12, 0), (D, 0)])
        P.scale("k1", 1 + 0.08 * sm, 1 - 0.06 * sm)
        feet(P)

    def cast1(t, P, D=1.0, H=0.5, E=0.82):
        """Bọt Nước: ngửa lấy hơi, phồng má, há miệng nhả chuỗi bong bóng (VFX bám xương mieng), giữ rung tới hết dòng, về."""
        rear = cv(t, [(0, 0), (0.36, 1, "io"), (0.44, 1.06), (H, -0.5, "in"), (0.58, -0.6), (E, -0.5), (D, 0, "io")])
        nen(P, t, D=D, amp=1 - 0.8 * bao(t, 0.05, D - 0.05, 0.15, 0.2))
        r = rung(t, H + 0.04, E)
        P.rot("dau", 4.5 * rear + 0.8 * r)
        P.rot("than", 2.0 * rear)
        P.move("than", -1.0 * u * max(rear, 0) + 0.8 * u * max(-rear, 0), 0)
        P.rot("ham", -(cv(t, [(0, 0), (0.36, 6, "io"), (H, 26, "out"), (E, 24), (D, 0, "io")]) + 2.5 * r))
        P.scale("dau", 1 + 0.03 * bao(t, 0.2, 0.46, 0.1, 0.06), 1 + 0.03 * bao(t, 0.2, 0.46, 0.1, 0.06))
        for m_ in mats:
            P.rot(m_[1], -6 * max(rear, 0))
        P.rot("t10", -4 * rear)
        P.rot("t20", 5 * rear)
        feet(P)

    def skill1(t, P, D=1.7):
        """Đá Ngầm Trồi: thụt vào nhà đá tụ lực (đá rung), bật ra, giơ càng búa nện xuống đất: hàng cột đá + mạch nước trồi dọc đất tới
        đối thủ (VFX, sự kiện nen / troi), giữ thế, về."""
        ins = cv(t, [(0, 0), (0.3, 1, "io"), (0.52, 1), (0.6, -0.15, "out"), (0.7, 0, "io"), (D, 0)])
        arm = cv(t, [(0, 0), (0.5, 0), (0.62, 1.1, "out"), (0.72, -1, "in"), (0.78, -0.9, "out"), (1.3, -0.85), (D, 0, "io")])
        nen(P, t, D=D, amp=1 - 0.85 * bao(t, 0.05, D - 0.05, 0.15, 0.3))
        r = rung(t, 0.3, 0.52) + rung(t, 0.76, 1.3)
        dxs = -0.2 * Hr * max(ins, 0) + 1.5 * u * max(-ins, 0)
        P.move("than", dxs, 0)
        giu_chan(P, dxs)
        P.rot("nha", 1.4 * r)
        P.move("nha", 0, -1.0 * u * bao(t, 0.3, 0.55, 0.05, 0.05))
        for m_ in mats:
            P.rot(m_[1], 22 * max(ins, 0))
            P.rot(m_[0], 10 * max(ins, 0))
        for r_ in rau:
            P.rot(r_[0], 12 * max(ins, 0))
        P.rot("t10", (6 if arm > 0 else 30) * arm)
        P.rot("t11", (4 if arm > 0 else 16) * arm)
        P.rot("k1", (26 if arm > 0 else 26) * arm + 1.0 * r)
        P.rot("t20", 10 * max(ins, 0))
        P.rot("ham", -14 * bao(t, 0.72, 1.3, 0.05, 0.2))
        sm = cv(t, [(0, 0), (0.7, 0), (0.72, 1), (0.78, 0), (D, 0)])
        P.scale("k1", 1 + 0.1 * sm, 1 - 0.08 * sm)
        P.move("move", 0, -0.6 * u * bao(t, 0.72, 0.8, 0.02, 0.05))
        feet(P)

    if k == 1:
        attack_fn, cast_fn, skill_fn = attack1, cast1, skill1
        ev_a, ev_c = [(0.42, "trung", "mieng_cang")], [(0.5, "phun", "mieng"), (0.82, "het_phun", "")]
        ev_s = [(0.72, "nen", ""), (0.78, "gam", ""), (0.8, "troi", ""), (1.3, "het_gam", "")]
        dur = {"attack": 0.9, "cast": 1.0, "skill": 1.7}
    else:
        ev_a, ev_c = [(0.55, "trung", "")], [(0.62, "phun", "mieng"), (1.25, "het_phun", "")]
        ev_s = [(0.68, "nen", ""), (0.95, "gam", ""), (1.0, "xoay", ""), (1.5, "troi", ""), (1.75, "het_gam", "")]
        dur = {"attack": 1.1, "cast": 1.6, "skill": 2.0}

    out = [Clip("appear", 1.6, appear_fn, mem=soft),
           Clip("idle", D_IDLE, idle_fn, loop=True, mem=soft),
           Clip("attack", dur["attack"], attack_fn, ev=ev_a, mem=soft),
           Clip("cast", dur["cast"], cast_fn, ev=ev_c, mem=soft),
           Clip("skill", dur["skill"], skill_fn, ev=ev_s, mem=soft),
           Clip("hit", 0.6, hit_fn, mem=soft),
           Clip("die", 2.0, die_fn, mem=soft)]
    return out


def khop_dau(frames, idle0, giay=0.3, fps=30):
    """khung 0 clip không lặp = khung 0 idle thật sự (gồm phần lò xo còn trễ trong idle): cộng phần chênh ở khung 0, tắt dần trong
    `giay` giây đầu (như khop_cuoi của thư viện nhưng ở đầu clip)."""
    P0 = frames[0]
    keys = set(P0.t) | set(idle0.t)
    dlt = {}
    for b in keys:
        a = idle0.t.get(b, [0, 0, 0, 1, 1])
        c = P0.t.get(b, [0, 0, 0, 1, 1])
        d = [a[0] - c[0], a[1] - c[1], a[2] - c[2], a[3] / c[3] if c[3] else 1, a[4] / c[4] if c[4] else 1]
        if max(abs(d[0]), abs(d[1]), abs(d[2]), abs(d[3] - 1), abs(d[4] - 1)) > 1e-6:
            dlt[b] = d
    n = int(round(giay * fps))
    for i in range(min(n + 1, len(frames))):
        w = 1 - ease(i / max(1, n))
        P = frames[i]
        for b, d in dlt.items():
            g = P._g(b)
            g[0] += d[0] * w
            g[1] += d[1] * w
            g[2] += d[2] * w
            g[3] *= 1 + (d[3] - 1) * w
            g[4] *= 1 + (d[4] - 1) * w


def uon_thu(rig, ra):
    sk = rig.sk
    P = khung.Pose()
    for n in rig.c["chan"]:
        P.rot(rig.chain[n][0], 15)
        P.rot(rig.chain[n][1], -25)
    for n in rig.c["rau"] + rig.c["rong"]:
        for b in rig.chain[n]:
            P.rot(b, 10)
    P.rot("t10", 30)
    P.rot("t20", -20)
    P.rot("n1", 25)
    P.rot("n2", -20)
    P.rot("ham", -20)
    P.rot("dau", 8)
    ve = soi.Ve(sk)
    B = soi._union([ve.bao(P)], 0.05)
    a = ve.ve(P, B, 1.3, bg=(150, 150, 150), ss=2, luoi=True, mau_luoi=(10, 10, 10, 90))
    a.convert("RGB").save(ra)


def so_concept(rig, frames, ra):
    """khung 0 idle dựng lại ở tỉ lệ concept, đặt cạnh concept; IoU mặt nạ (đặc tả mục 5: ≥ 0,9 với cách lai)."""
    sk, S = rig.sk, rig.S
    ve = soi.Ve(sk)
    box = ((0 - rig.GX) * S, (rig.GY - 1024) * S, (1536 - rig.GX) * S, rig.GY * S)
    im = ve.ve(frames["idle"][0], box, 1.0 / S, bg=None, ss=1)
    im = im.resize((1536, 1024), Image.LANCZOS)
    a = np.asarray(im)[..., 3] > 100
    ref = np.asarray(Image.open(path(rig.k, "tai_ve", "L1_duyet.png")).convert("RGB"))
    m = ref.min(2) < 236
    iou = float((a & m).sum() / max(1, (a | m).sum()))
    vis = Image.new("RGB", (1536 * 2, 1024), (255, 255, 255))
    vis.paste(Image.fromarray(ref), (0, 0))
    bg = Image.new("RGBA", (1536, 1024), (150, 150, 150, 255))
    bg.alpha_composite(im)
    vis.paste(bg.convert("RGB"), (1536, 0))
    ov = np.full((1024, 1536, 3), 255, np.uint8)
    ov[m & ~a] = (220, 40, 40)
    ov[a & ~m] = (40, 90, 220)
    ov[a & m] = (200, 200, 200)
    vis = vis.resize((1536, 512))
    out = Image.new("RGB", (1536, 512 + 512), (255, 255, 255))
    out.paste(vis, (0, 0))
    out.paste(Image.fromarray(ov).resize((768, 512)), (384, 512))
    from PIL import ImageDraw
    ImageDraw.Draw(out).text((10, 520), f"IoU khung 0 idle / concept = {iou:.3f}  (đỏ: concept có rig thiếu; xanh: rig thừa)",
                             fill=(0, 0, 0), font=anh.font(20))
    out.save(ra)
    print(f"  so_concept: IoU {iou:.3f}")
    return iou


def them_so_sanh(rig, tong, ra):
    """nối thêm vào so_sanh.md: mật độ lưới theo chiều cao, IoU với concept, lệch khung 0 các clip."""
    Hr = rig.c["H_rig"]
    L = [f"", f"## Thêm của tm02 (cách lai: mọi lớp cắt thẳng từ concept; mắt nhắm làm từ mắt concept; lòng miệng tờ GPT M01)", "",
         f"- Chiều cao con {Hr:.0f} px rig; lưới bước viền {0.015 * Hr:.1f} px (1,5 %), bước trong {0.02 * Hr:.1f} px (2 %); "
         f"{tong['dinh']} đỉnh / {Hr:.0f} px = {tong['dinh'] / Hr:.2f} đỉnh mỗi px chiều cao.",
         f"- IoU mặt nạ khung 0 idle với concept: {tong.get('iou_concept', 0):.3f} (`so_concept.png`).",
         "- Khung 0 mỗi clip so khung 0 idle (đỉnh lưới đã vẽ, gồm lò xo): " +
         ", ".join(f"{k} {v[0]:.2f} px" for k, v in tong.get("khung0", {}).items()) + "; khung cuối: xem mục nối clip ở trên."]
    with open(os.path.join(ra, "so_sanh.md"), "a", encoding="utf-8") as f:
        f.write(chr(10).join(L) + chr(10))


def lam(k):
    t0 = time.time()
    rig = Rig(k)
    sk = rig.build()
    cl = clips_cho(rig)
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    for c in cl:
        if not c.loop and c.ten not in ("appear",):
            khop_dau(fr[c.ten], fr["idle"][0])
    print(f"nướng {len(cl)} clip ({time.time() - t0:.1f} s)")
    ra = path(k, "rig")
    tong = xuat.xuat_het(sk, cl, ra, f"{CODE}_{k}", rig.c["ten"], frames=fr, dang=k, so_dang=2, dung_yen=("attack", "cast", "skill"),
                         mieng="mieng", ma_goc=3227,
                         can=[("can_mieng_skill", "skill", 1.2, "ham", 60), ("can_cang_cast", "cast", 0.7, "k1", 110),
                              ("can_nen_attack", "attack", 0.55, "k1", 120), ("can_mat_hit", "hit", 0.1, rig.chain["mat0"][-1], 60),
                              ("can_chan_skill", "skill", 0.5, rig.chain["chan2"][1], 90)])
    uon_thu(rig, os.path.join(ra, "uon_thu.png"))
    tong["iou_concept"] = so_concept(rig, fr, os.path.join(ra, "so_concept.png"))
    # khung 0 mỗi clip so khung 0 idle, đo trên đỉnh lưới đã vẽ (gồm lò xo)
    ve = soi.Ve(sk)
    dau0 = {}
    for c in cl:
        if c.ten in ("idle", "appear", "evolve"):
            continue
        d, w = soi.lech(ve, fr[c.ten][0], fr["idle"][0])
        dau0[c.ten] = (round(d, 2), w)
        print(f"  khung 0 {c.ten} lệch khung 0 idle {d:.2f} px ({w})")
    tong["khung0"] = dau0
    them_so_sanh(rig, tong, ra)
    print(f"xong {time.time() - t0:.1f} s")
    return rig, cl, fr, tong


def lam1():
    """dạng 1 + gộp dạng 2 (clip evolve 2,8 s: cua thụt vào nhà đá, đá rung, lốc; đổi dạng lúc lốc đậm nhất; tháp đá dạng 2 lớn dần,
    cua bật ra giơ găng gầm; khung cuối = khung 0 idle dạng 2)."""
    t0 = time.time()
    rigB = Rig(2)
    skB = rigB.build()
    clB = clips_cho(rigB)
    idleB = hoat.nuong(skB, next(c for c in clB if c.ten == "idle"))
    rigA = Rig(1)
    skA = rigA.build()
    clA = clips_cho(rigA)
    frA = {c.ten: hoat.nuong(skA, c) for c in clA}
    for c in clA:
        if not c.loop and c.ten not in ("appear",):
            khop_dau(frA[c.ten], frA["idle"][0])
    veA, veB = soi.Ve(skA), soi.Ve(skB)
    hA, hB = soi.chieu_cao(veA, frA["idle"][0]), soi.chieu_cao(veB, idleB[0])
    M = tienhoa.gop(skA, skB)
    HrA = rigA.c["H_rig"]

    def gong(t, P):
        """dạng 1: thụt vào nhà đá, càng co, nhà đá rung mạnh dần (tụ lực)."""
        ins = hoat.cv(t, [(0, 0), (0.45, 1, "io"), (1.4, 1)])
        P.move("than", -0.5 * HrA * ins, 0)
        r = hoat.rung(t, 0.45, 1.35)
        P.rot("nha", (1.0 + 2.5 * hoat.ease((t - 0.45) / 0.9)) * r)
        P.move("nha", 0, -0.012 * HrA * hoat.bao(t, 0.4, 1.35, 0.1, 0.1))
        a = 1 - hoat.ease(t / 0.4)
        for n in [x for x in rigA.c["chan"] + list(rigA.c["cang"]["c1"][:2]) + list(rigA.c["cang"]["c2"][:2]) + rigA.c["rau"] if x]:
            P.alpha[n] = a
        P.rot("t10", -40 * ins)
        P.rot("t20", -20 * ins)

    def gam(t, P, fl):
        """dạng 2: giơ găng đá, há miệng gầm."""
        P.rot("n_t10", -4 * fl)
        P.rot("n_k1", 30 * fl)
        P.rot("n_n1", 18 * fl)
        P.rot("n_ham", -20 * fl)
        P.rot("n_dau", 4 * fl)
        P.scale("n_move", 1 + 0.04 * fl, 1 + 0.04 * fl)

    memA = next(c for c in clA if c.ten == "idle").mem
    memB = next(c for c in clB if c.ten == "idle").mem
    memM = list(memA) + tienhoa.doi_ten_mem(memB)
    ev = tienhoa.clip_tien_hoa(M, skA, skB, idleB[0], tiB=hA / hB, fnA=gong, fnB=gam, mem=memM)
    goc_fn = ev.fn
    thu = [x for x in rigA.c["chan"] + list(rigA.c["cang"]["c1"][:2]) + list(rigA.c["cang"]["c2"][:2]) + rigA.c["rau"] if x]

    def fn_thu(t, P):
        """chân, càng, râu dạng cũ mờ đi cùng lúc thân thụt vào nhà (clip_tien_hoa đặt độ đậm sau fnA nên nhân thêm ở đây)."""
        goc_fn(t, P)
        a = 1 - hoat.ease(t / 0.42)
        for nm in thu:
            P.alpha[nm] = P.alpha.get(nm, 1.0) * a
    ev.fn = fn_thu
    clM = list(clA) + [ev]
    frM = dict(frA)
    frM["evolve"] = hoat.nuong(M, ev)
    khop_dau(frM["evolve"], frA["idle"][0])
    px, con, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], skB, idleB[0], hA / hB)
    print(f"nướng {len(clM)} clip ({time.time() - t0:.1f} s); evolve: {s_ev}")
    ra = path(1, "rig")
    tong = xuat.xuat_het(M, clM, ra, f"{CODE}_1", rigA.c["ten"] + " (gộp dạng 2 cho tiến hóa)", frames=frM, dang=1, so_dang=2,
                         dung_yen=("attack", "cast", "skill"), mieng="mieng", ma_goc=3227,
                         noi_them={"evolve": s_ev + f" (dạng sau co {hA / hB:.3f} trong rig gộp)"},
                         can=[("can_mieng_cast", "cast", 0.6, "ham", 50), ("can_cang_attack", "attack", 0.42, "k1", 90),
                              ("can_mat_hit", "hit", 0.1, rigA.chain["mat0"][-1], 55), ("can_chan_skill", "skill", 0.72, rigA.chain["chan2"][1], 80),
                              ("can_tien_hoa", "evolve", 1.25, "nha", 150)])
    uon_thu(rigA, os.path.join(ra, "uon_thu.png"))
    tong["iou_concept"] = so_concept(rigA, frA, os.path.join(ra, "so_concept.png"))
    ve = soi.Ve(skA)
    dau0 = {}
    for c in clA:
        if c.ten in ("idle", "appear"):
            continue
        d, w = soi.lech(ve, frA[c.ten][0], frA["idle"][0])
        dau0[c.ten] = (round(d, 2), w)
        print(f"  khung 0 {c.ten} lệch khung 0 idle {d:.2f} px ({w})")
    d, w = soi.lech(soi.Ve(M), frM["evolve"][0], frA["idle"][0])
    dau0["evolve"] = (round(d, 2), w)
    print(f"  khung 0 evolve lệch khung 0 idle {d:.2f} px ({w})")
    tong["khung0"] = dau0
    tong["dinh"] = skA.tom_tat()["dinh"]
    them_so_sanh(rigA, tong, ra)
    print(f"xong {time.time() - t0:.1f} s")


if __name__ == "__main__":
    if int(sys.argv[1]) == 1:
        lam1()
    else:
        lam(int(sys.argv[1]))
