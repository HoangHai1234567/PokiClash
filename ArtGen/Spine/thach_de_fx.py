# -*- coding: utf-8 -*-
"""Thổ Tinh (thach_de, final boss đảo Thổ): bản xem trước ba đòn trên sân có ĐỐI THỦ + VFX hạt phẳng (fxlib), như tho5_fx.py.
Người dùng 2026-11-18 tả đòn:
- đánh thường: "lên cao, dùng 2 tay đập xuống người đối thủ";
- cast: "hét gầm lên, các gai sau lưng bắt đầu tách ra nổi lên sau đó lần lượt từng gai xoay hướng vào mục tiêu rồi lao vào";
- chiêu cuối: "dang 2 tay ngửa lòng bàn tay ra rồi từ từ bay lên trời, sau đó rất nhiều tiểu hành tinh / thiên thạch / đá sẽ lao vào bám
  xung quanh đối thủ, sau đó tướng ép 2 tay gần vào nhau ở phía trước, các hành tinh quanh đối thủ co nhỏ lại (tướng ở trong cũng phải co
  theo để không bị lộ) rồi triệu hồi 1 mặt trời trên đầu đối thủ rồi bắn 1 tia nhiệt cực lớn xuống tạo ra 1 vụ nổ hình nấm, đá văng tứ
  tung (vfx làm thêm cho hoành tráng)".

Tướng mình = khung rig THẬT (thach_de_rig.py, aura ghép cùng giây), lật quay về địch, chân ở fx.ME; địch ở fx.FOE. Đích gai của rig đặt
đúng giữa thân địch (thach_de_rig.DICH_RIG). Thứ bay khỏi thân (gai, thiên thạch, mặt trời, tia, nổ) là VFX: ở đây vẽ bằng Python để
người dùng hình dung, sẽ làm lại trong Unity. Luật: tô phẳng, viền mực, không glow, không gradient.

    thach_de_fx.py [attack|cast|skill|all]   → inbox/thach_de_1/fx/thach_de_<clip>.gif + _soi.png, trang inbox/thach_de_1/fx/xem.html
"""
import math
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("SXS", r"D:\Ripper\SwordxStaff")
import fxlib as fx  # noqa: E402
import tho5_fx as T5  # noqa: E402
import thach_de_rig as R  # noqa: E402
from quai import hoat, soi, khung  # noqa: E402

RA = os.path.join(HERE, "inbox", "thach_de_1", "fx")
K, M = fx.K, fx.M
INK = (43, 33, 24)
DUST = T5.DUST
DA = T5.DA
TRANG = [(207, 200, 214), (157, 149, 171), (179, 171, 192)]          # đá trăng của tướng: mặt, mặt bên, hố
KEM = (255, 246, 214)
LUA = [(234, 96, 40), (248, 158, 52), (252, 214, 92), (255, 244, 206)]   # mặt trời / tia nhiệt: cam đỏ → kem (không glow)
FOE_IMG = T5.FOE_IMG
BG = T5.BG
FOE_C = T5.FOE_C


# ---------------------------------------------------------------- ảnh mảnh của tướng làm hình hạt (đá trăng, gai)
def _manh(ten, lat=False):
    im = Image.open(os.path.join(R.MANH, ten + ".png")).convert("RGBA")
    return im.transpose(Image.FLIP_LEFT_RIGHT) if lat else im


for _i, _a in enumerate(R.LUNG_ANH):
    fx.Art.EXTRA[f"gai_{_i}"] = (lambda a: (lambda seed: _manh(a, True)))(_a)
for _n in ("ve_1", "ve_2", "ve_3", "ve_4", "ve_5", "vun_1", "vun_2", "vun_3", "vun_4", "trang_nho"):
    fx.Art.EXTRA[_n] = (lambda a: (lambda seed: _manh(a, seed % 2 == 1)))(_n)
TI_LE = {n: (lambda im: im.width / im.height)(_manh(n)) for n in ("ve_1", "ve_2", "ve_3", "ve_4", "ve_5", "vun_1", "vun_2", "vun_3",
                                                                    "vun_4", "trang_nho")}
TI_GAI = [(lambda im: im.width / im.height)(_manh(a)) for a in R.LUNG_ANH]


def sprite(group, layer, ten, pos, cao, ang=0.0, alpha=1.0, seed=0, ti=None):
    return fx.item(group, layer, ten, seed, None, pos, cao, ti if ti is not None else TI_LE.get(ten, 1.0), ang, alpha)


# ---------------------------------------------------------------- tướng mình = rig thật
class Thach:
    def __init__(self):
        sk, info, clips, frames = R.dung_het()
        cl = {c.ten: c for c in clips}
        ve = soi.Ve(sk)
        idle0 = hoat.nuong(sk, cl["idle"])[0]
        bx = ve.bao(idle0)
        self.s = fx.H * 1.15 / info["cao"]
        self.cx, self.yg = (bx[0] + bx[2]) / 2.0, bx[1]
        self.rong = bx[2] - bx[0]
        R.DICH_RIG = list(self.rig(FOE_C))                 # gai chĩa đúng giữa thân địch
        sk, info, clips, frames = R.dung_het()
        self.sk, self.info, self.aura = sk, info, frames["aura"]
        self.clips = {c.ten: c for c in clips}
        self.ve = soi.Ve(sk)
        self.idle = hoat.phu_aura(hoat.nuong(sk, self.clips["idle"]), self.aura, sk)
        self.s_hop = R.nap()[3]["s"]

    def rig(self, p):
        return np.array([self.cx - (p[0] - fx.ME[0]) / self.s, self.yg + (fx.ME[1] - p[1]) / self.s])

    def san(self, v):
        return np.array([fx.ME[0] - (v[0] - self.cx) * self.s, fx.ME[1] - (v[1] - self.yg) * self.s])

    def goc_san(self, th):
        """góc thế giới rig (độ, ngược kim, y lên) → góc nhìn trên sân sau khi lật (độ, ngược kim)."""
        return 180.0 - th

    def khung(self, clip, lao=False):
        fr = [P.copy() for P in hoat.nuong(self.sk, self.clips[clip])]
        if clip not in ("idle", "aura"):
            hoat.khop_cuoi(fr, hoat.nuong(self.sk, self.clips["idle"])[0], 0.2)
        if lao:                                          # như sân (AolaSticker.Lunge): đỉnh cú lao rơi vào 72 % quãng tới đối thủ
            xs = [P.t.get("move", [0.0] * 5)[0] for P in fr]
            mx = max(xs) or 1.0
            v = self.rig(fx.ME + 0.72 * (fx.FOE - fx.ME)) - np.array([self.cx, self.yg])
            for P, x in zip(fr, xs):
                g = list(P.t.get("move", [0.0, 0.0, 0.0, 1.0, 1.0]))
                g[0], g[1] = float(v[0] * x / mx), float(v[1] * x / mx + g[1])
                P.t["move"] = g
        return hoat.phu_aura(fr, self.aura, self.sk)

    def diem(self, P, xuong):
        return self.san(self.sk.the_gioi(P)[xuong][:2, 2])

    def anh(self, P):
        X = fx.ME[0] / self.s + 40
        Y = (fx.ME[1] + 40) / self.s
        box = (self.cx - X, self.yg - 12.0, self.cx + X, self.yg + Y)
        im = self.ve.ve(P, box, self.s * K, ss=1).transpose(Image.FLIP_LEFT_RIGHT)
        nang = max(0.0, (self.sk.the_gioi(P)["bone3"][1, 2] - self.sk.W0["bone3"][1, 2]) * self.s)
        return im, 12.0 * self.s * K, nang


def _dan(art, im, it):
    g, l, name, seed, col, pos, w, h, ang, alpha = it
    if name == "polys":
        art.polys(im, seed, alpha)
        return
    if name == "poly":
        art.poly(im, seed, col, alpha, w)
        return
    t = art.render(name, seed, col, w * K, h * K, ang, alpha)
    x, y = int(pos[0] * K + M - t.width / 2), int(pos[1] * K + M - t.height / 2)
    if x > im.width or y > im.height or x + t.width < 0 or y + t.height < 0:
        return
    im.alpha_composite(t, (x, y))


def ve_khung(sim, art, stage, hero, foe_img):
    """như tho5_fx.ve_khung + đối thủ co quanh giữa thân (sim.foe_k), bẹp theo chân (hero_fx sq), bóng tướng mình nhỏ lại khi bay."""
    im = stage.bg.copy()
    items = []
    for p in sim.ps:
        if p.draw:
            items += p.draw(p, min(0.999, p.age / p.life))
    items.append((fx.HERO, 0, "@foe", 0, None, (fx.FOE[0], fx.FOE[1]), 0, 0, 0, 1))
    items.append((fx.HERO, 1, "@me", 0, None, (fx.ME[0], fx.ME[1]), 0, 0, 0, 1))
    items.sort(key=lambda it: (it[0], it[1]))
    for g, l, name, seed, col, pos, w, h, ang, alpha in items:
        if name == "@foe":
            k = getattr(sim, "foe_k", 1.0)
            hien = getattr(sim, "foe_a", 1.0)                     # độ hiện (chiêu cuối: ẩn lúc nổ, hiện mờ dần sau khói đen)
            fxh = sim.hero_fx.get("foe", {})
            img = stage.hero_img("foe", fxh) if fxh else foe_img
            sq = fxh.get("sq", (1.0, 1.0))
            off = fxh.get("off", (0, 0))
            sh = art.render("ell", 0, (40, 24, 20), img.width * 0.62 * max(0.3, k), 18 * K * max(0.3, k), 0, 0.35 * min(1.0, k * 1.4) * hien)
            im.alpha_composite(sh, (int(pos[0] * K + M - sh.width / 2), int(pos[1] * K + M - sh.height / 2)))
            if k < 0.03 or hien < 0.02:
                continue
            if hien < 0.999:
                img = img.copy()
                img.putalpha(img.getchannel("A").point(lambda v: int(v * hien)))
            w2, h2 = max(2, int(img.width * k * sq[0])), max(2, int(img.height * k * sq[1]))
            if (w2, h2) != img.size:
                img = img.resize((w2, h2), Image.BILINEAR)
            x = FOE_C[0] * K + M - w2 / 2 + off[0] * K
            y = (pos[1] * K + M - h2) if k > 0.999 else (FOE_C[1] * K + M - 0.55 * h2)
            im.alpha_composite(img, (int(x), int(y + off[1] * K)))
            continue
        if name == "@me":
            img, lech, nang = hero[0], hero[1], hero[3]
            ks = 1.0 / (1.0 + nang / 70.0)
            sh = art.render("ell", 0, (40, 24, 20), hero[2] * K * 0.7 * ks, 18 * K * ks, 0, 0.35 * ks)
            im.alpha_composite(sh, (int(pos[0] * K + M - sh.width / 2), int(pos[1] * K + M - sh.height / 2)))
            im.alpha_composite(img, (int(pos[0] * K + M - img.width / 2), int(pos[1] * K + M - img.height + lech)))
            continue
        if name == "@lop":                               # nhiều nét vẽ đặc lên một lớp rồi làm trong một lần
            tmp = Image.new("RGBA", im.size, (0, 0, 0, 0))
            for it in seed:
                _dan(art, tmp, it)
            if alpha < 0.999:
                tmp.putalpha(tmp.getchannel("A").point(lambda v: int(v * alpha)))
            im.alpha_composite(tmp)
            continue
        _dan(art, im, (g, l, name, seed, col, pos, w, h, ang, alpha))
    if sim.flash > 0.01:
        im = Image.blend(im, Image.new("RGBA", im.size, (255, 246, 214, 255)), min(0.55, sim.flash))
    tr = sim.trauma ** 2
    dx = 12 * K * tr * math.sin(sim.t * 2 * math.pi * 11.7)
    dy = 8 * K * tr * math.sin(sim.t * 2 * math.pi * 14.3 + 1)
    return im.crop((int(M + dx), int(M + dy), int(M + dx) + fx.W * K, int(M + dy) + fx.Hs * K))


def chay(T, clip, build, ten, duoi=0.8, nhan="", lao=False):
    os.makedirs(RA, exist_ok=True)
    fr = T.khung(clip, lao)
    seq = fr + [T.idle[i % len(T.idle)] for i in range(int(duoi * fx.FPS))]
    sim, art = fx.Sim(3), fx.Art()
    sim.foe_k = 1.0
    stage = fx.Stage(bg=BG, heroes=False)
    foe = fx.load_hero(FOE_IMG, fx.H * K)
    stage.heroes["foe"] = (foe, fx.FOE)
    build(sim, T, fr)
    frames = []
    for i, P in enumerate(seq):
        im, lech, nang = T.anh(P)
        frames.append(ve_khung(sim, art, stage, (im, lech, T.rong * T.s, nang), foe))
        for _ in range(4):
            sim.step(1 / fx.FPS / 4)
    fx.save(frames, RA, ten, label=nhan, hold=10)
    print(os.path.join(RA, ten + ".gif"), len(frames), "khung")


def tai(fr, t):
    return fr[min(len(fr) - 1, max(0, int(round(t * fx.FPS))))]


def ev(T, clip, ten):
    return [t for t, n, _ in T.clips[clip].ev if n == ten]


def trung_nhe(sim, muc=1.0, off=(-4.0, -2.0)):
    """đối thủ nháy kem + giật lùi (không đè foe_k)."""
    sim.hero_fx["foe"] = {"tint": KEM, "amt": 0.6, "decay": 7.0, "off": (off[0] * muc, off[1] * muc), "sq": (1.0, 1.0)}
    sim.at(sim.t + 0.08, lambda s: s.hero_fx.get("foe", {}).update(off=(0.0, 0.0)))


# ---------------------------------------------------------------- ĐÁNH THƯỜNG: nhảy, nện hai nắm đấm xuống người đối thủ
def attack(sim, T, fr):
    t_tu, t_tr = ev(T, "attack", "tu")[0], ev(T, "attack", "trung")[0]

    def bat(s):
        T5.vong_dat(s, fx.ME + np.array([0.0, 2.0]), 80, 0.45)
        for d in (-1, 1):
            T5.bui(s, fx.ME + np.array([d * 28.0, -2.0]), vel=np.array([d * 80.0, -25.0]), r0=9, r1=22)
    sim.at(t_tu + 0.04, bat)

    def nen(s):
        P = tai(fr, t_tr)
        a, b = T.diem(P, "bone96"), T.diem(P, "bone102")
        m = (a + b) / 2
        dat = np.array([m[0], fx.FOE[1] + 4.0])
        T5.cham_no(s, FOE_C + np.array([4.0, 10.0]), 1.6)
        T5.vong_dat(s, dat, 120, 0.55)
        for d in (-1, 1):
            T5.vet_nut(s, dat, dat + np.array([d * 70.0, s.rng.uniform(-8, 10)]), s.t, 0.16)
            for j in range(3):
                T5.bui(s, dat + np.array([d * (20.0 + 16 * j), -4.0]), vel=np.array([d * (90.0 + 40 * j), -30.0]), r0=10, r1=26)
        for p in (a, b):
            for j in range(4):
                v = np.array([s.rng.uniform(-220, 220), s.rng.uniform(-300, -120)])
                T5.dam_da(s, p, v, size=s.rng.uniform(4, 7), ground=fx.FOE[1] + s.rng.uniform(-4, 10))
        s.shake(0.55)
        s.flash = 0.25
        s.hero_fx["foe"] = {"tint": KEM, "amt": 1.0, "decay": 5.0, "off": (-3.0, 3.0), "sq": (1.14, 0.80)}
        s.at(s.t + 0.10, lambda s2: s2.hero_fx.get("foe", {}).update(sq=(0.94, 1.06), off=(-2.0, 0.0)))
        s.at(s.t + 0.20, lambda s2: s2.hero_fx.get("foe", {}).update(sq=(1.0, 1.0), off=(0.0, 0.0)))
    sim.at(t_tr, nen)


# ---------------------------------------------------------------- CAST: gầm, gai lưng bứt ra nổi lên, lần lượt phóng vào đối thủ
def cast(sim, T, fr):
    c = T.info["cast"]
    rng = sim.rng
    t_gam = ev(T, "cast", "gam")[0]

    def song_gam(s, x):                                  # sóng gầm: cung kem phình ra từ miệng về phía đối thủ
        m = T.diem(tai(fr, s.t), "ham") + np.array([-14.0, 4.0])
        q = fx.P(m, (0, 0), 0.42, group=fx.FRONT)

        def ve(q, k):
            r = 22 + 135 * fx.ease_out(k)
            return [fx.item(fx.FRONT, 58, "arcpx", 128 * 1000 + 104, (255, 246, 214, 9), q.pos + np.array([-r * 0.2, 0.0]), 2 * r * 1.0,
                            0.62, 0, (1 - k) ** 1.2)]
        q.draw = ve
        s.add(q)
    sim.every(t_gam, 0.92, 9.0, song_gam)

    def run_dat(s, x):                                   # đất rung: sỏi nảy, bụi dưới chân
        p = fx.ME + np.array([rng.uniform(-90, 70), rng.uniform(-4, 6)])
        T5.dam_da(s, p, np.array([rng.uniform(-30, 30), rng.uniform(-150, -80)]), size=rng.uniform(2.5, 4.5), ground=p[1])
        if rng.uniform() < 0.35:
            T5.bui(s, p, vel=np.array([rng.uniform(-30, 30), -20.0]), r0=6, r1=14, life=0.5, group=fx.BACK)
    sim.every(t_gam, 0.95, 26.0, run_dat)
    sim.at(t_gam, lambda s: s.shake(0.25))

    # gai bứt khỏi vành: vụn + bụi ở đế
    for i in range(10):
        t0 = 0.30 + 0.024 * i

        def tach(s, i=i):
            P = tai(fr, s.t)
            p = T.diem(P, f"gai_{i}")
            for _ in range(2):
                T5.dam_da(s, p, np.array([rng.uniform(-90, 90), rng.uniform(-140, -40)]), size=rng.uniform(2.5, 4), col=TRANG[1],
                          ground=fx.ME[1] + rng.uniform(-2, 8))
            T5.bui(s, p, vel=np.array([rng.uniform(-20, 20), -30.0]), r0=5, r1=12, life=0.45, group=fx.BACK)
        sim.at(t0 + 0.02, tach)

    # gai phóng: VFX bay từ chỗ rig ẩn gai tới giữa thân đối thủ, cắm vào, vỡ
    hs = T.s * R.KG / T.s_hop
    thu = sorted(range(10), key=lambda i: c["T_BAN"][i])
    for n, i in enumerate(thu):
        tb = c["T_BAN"][i]

        def phong(s, i=i, n=n, tb=tb):
            P = tai(fr, tb - 1.0 / fx.FPS)
            Wd = T.sk.the_gioi(P)
            a = T.san(Wd[f"gai_{i}"][:2, 2])
            h = R.LUNG_CAO[i] * hs
            b = FOE_C + np.array([rng.uniform(-12, 12), rng.uniform(-16, 14)])
            d = b - a
            nn = np.array([-d[1], d[0]]) / (np.hypot(*d) or 1.0)
            vong = rng.uniform(-14, 14)
            bay = c["BAY"]
            q = fx.P(a.copy(), (0, 0), bay + 0.12, group=fx.FRONT, a0=a, b0=b, nn=nn, vong=vong, h=h, i=i)

            def vi(q, f):
                e = f ** 1.5
                return q.a0 + (q.b0 - q.a0) * e + q.nn * q.vong * math.sin(math.pi * f)

            def ve(q, k):
                f = min(1.0, q.age / bay)
                p = vi(q, f)
                p2 = vi(q, max(0.0, f - 0.04)) if f > 0.04 else q.a0 - (q.b0 - q.a0) * 0.01
                dv = p - p2 if f < 1.0 else (q.b0 - q.a0)
                goc = math.degrees(math.atan2(-dv[1], dv[0])) - 90.0
                out = []
                if f < 1.0:
                    for j, al in ((1, 0.42), (2, 0.24), (3, 0.12)):          # bóng mờ phía sau (vệt tốc độ)
                        fj = f - 0.11 * j
                        if fj > 0:
                            out.append(fx.item(fx.FRONT, 46, f"gai_{q.i}", 0, None, vi(q, fj), q.h, TI_GAI[q.i], goc, al))
                    out.append(fx.item(fx.FRONT, 48, f"gai_{q.i}", 0, None, p, q.h, TI_GAI[q.i], goc, 1.0))
                else:                                                         # cắm vào thân: mũi lún vào giữa
                    u = fx.unit(dv)
                    out.append(fx.item(fx.FRONT, 48, f"gai_{q.i}", 0, None, q.b0 - u * q.h * 0.18, q.h, TI_GAI[q.i], goc,
                                       1.0 - max(0.0, (q.age - bay - 0.08) / 0.04)))
                return out
            q.draw = ve

            def bui_vet(q2, dt, s2):
                if q2.age < bay and s2.rng.uniform() < 0.5:
                    T5.bui(s2, vi(q2, q2.age / bay), vel=np.array([0.0, -10.0]), r0=3, r1=8, life=0.3, group=fx.FRONT)
            q.upd = bui_vet
            s.add(q)

            def cham(s2, b=b, n=n, h=h):
                cuoi = n == 9
                trung_nhe(s2, 1.6 if cuoi else 0.8)
                s2.shake(0.10 if not cuoi else 0.35)
                sao = fx.P(b, (0, 0), 0.12, group=fx.FRONT, r=14.0 * (1.6 if cuoi else 1.0))
                sao.draw = lambda q, k: T5.ve_khoi(fx.FRONT, 60, q.pos, [((q.r if j % 2 == 0 else q.r * 0.42) * math.cos(j * math.pi / 5),
                                                                          (q.r if j % 2 == 0 else q.r * 0.42) * math.sin(j * math.pi / 5))
                                                                         for j in range(10)], KEM, 2.2)
                s2.add(sao)

                def vo(s3):
                    for j in range(3):
                        v = np.array([s3.rng.uniform(-160, 160), s3.rng.uniform(-220, -60)])
                        ten = f"vun_{1 + j % 4}"
                        p = fx.P(b.copy(), v, 0.7, acc=np.array([0, 900.0]), ground=fx.FOE[1] + s3.rng.uniform(-4, 8), bounce=0.3,
                                 spin=s3.rng.uniform(-10, 10), group=fx.FRONT, ten=ten, sz=h * s3.rng.uniform(0.18, 0.28))
                        p.draw = lambda q, k: [sprite(fx.FRONT, 47, q.ten, q.pos, q.sz, math.degrees(q.ang), 1 - max(0.0, k - 0.7) / 0.3)]
                        s3.add(p)
                    for j in range(3):
                        T5.dam_da(s3, b, np.array([s3.rng.uniform(-180, 180), s3.rng.uniform(-200, -60)]), size=s3.rng.uniform(3, 5),
                                  col=TRANG[s3.rng.randint(2)], ground=fx.FOE[1] + s3.rng.uniform(-4, 8))
                    T5.bui(s3, b, vel=np.array([s3.rng.uniform(-30, 30), -30.0]), r0=8, r1=18 * (1.5 if cuoi else 1.0))
                s2.at(s2.t + 0.10, vo)
            s.at(tb + bay, cham)
        sim.at(tb, phong)


# ---------------------------------------------------------------- CHIÊU CUỐI: bay lên, thiên thạch bọc đối thủ, ép, mặt trời, tia nhiệt, nổ nấm
def skill(sim, T, fr):
    S = T.info["skill"]
    rng = sim.rng
    RS0 = 0.62 * fx.H                                     # bán kính vỏ đá quanh đối thủ lúc mới bọc
    T_HUT, T_EP0, T_EP1, T_GOI, T_TIA, T_NO, T_DAT = S["T_HUT"], S["T_EP0"], S["T_EP1"], S["T_GOI"], S["T_TIA"], S["T_NO"], S["T_DAT"]
    T_EP2 = T_GOI - 0.22                                  # ép xong

    def rs(t):
        """bán kính vỏ đá: co lại khi ép (run nhẹ), vỡ lúc nổ."""
        u = hoat.ease((t - T_EP0) / (T_EP2 - T_EP0), "io")
        rr = 0.012 * math.sin(t * 2 * math.pi * 15) * (T_EP0 < t < T_NO)
        return RS0 * (1.0 - 0.56 * u + rr)

    def foe_k(t):
        return 1.0 if t >= T_NO or t < T_EP0 else rs(t) / RS0 * 0.92 * 0.87

    def foe_a(t):                                         # ẩn trong cầu lửa từ lúc nổ, hiện MỜ DẦN sau khói đen (+0,45 → +1,25 s)
        if t < T_NO:
            return 1.0
        return hoat.ease((t - T_NO - 0.45) / 0.8, "io")

    # đối thủ co theo vỏ đá: cập nhật mỗi bước
    q0 = fx.P(np.zeros(2), (0, 0), 99.0, group=fx.FLOOR)
    q0.upd = lambda q, dt, s: (setattr(s, "foe_k", foe_k(s.t)), setattr(s, "foe_a", foe_a(s.t)))
    sim.add(q0)

    # 1. bay lên: bụi xoáy dưới chân, sỏi nổi lên theo
    sim.at(S["T_BAY0"], lambda s: (T5.vong_dat(s, fx.ME + np.array([0.0, 2.0]), 90, 0.6),
                                   [T5.bui(s, fx.ME + np.array([d * 26.0, -2.0]), vel=np.array([d * 70.0, -30.0]), r0=10, r1=24) for d in (-1, 1)]))

    def soi_noi(s, x):
        p = fx.ME + np.array([rng.uniform(-80, 60), rng.uniform(-2, 6)])
        q = fx.P(p, np.array([rng.uniform(-10, 10), rng.uniform(-90, -50)]), rng.uniform(0.9, 1.4), drag=0.8, spin=rng.uniform(-3, 3),
                 group=fx.BACK if rng.uniform() < 0.5 else fx.FRONT, ten=f"vun_{rng.randint(1, 5)}", sz=rng.uniform(6, 11), seed=rng.randint(2))
        q.draw = lambda q, k: [sprite(q.group, 44, q.ten, q.pos, q.sz, math.degrees(q.ang), min(1.0, k * 6, (1 - k) * 3), q.seed)]
        s.add(q)
    sim.every(S["T_BAY0"], T_EP0, 9.0, soi_noi)

    # 2. thiên thạch lao tới, bám thành vỏ quanh đối thủ: chỗ bám trên đĩa đơn vị (vành trước, rồi lấp mặt trước); z < 0 = nửa sau
    da = []
    n_vanh, n_mat, n_sau = 14, 22, 9
    for j in range(n_vanh):
        a = 2 * math.pi * j / n_vanh + rng.uniform(-0.12, 0.12)
        da.append(dict(u=np.array([math.cos(a), math.sin(a)]) * rng.uniform(0.86, 1.0), z=rng.uniform(-0.1, 0.25)))
    for j in range(n_sau):
        a = 2 * math.pi * (j + 0.5) / n_sau
        da.append(dict(u=np.array([math.cos(a), math.sin(a)]) * rng.uniform(0.55, 0.8), z=-0.8))
    for j in range(n_mat):
        r_ = math.sqrt((j + 0.5) / n_mat) * 0.82
        a = j * 2.39996 + rng.uniform(-0.2, 0.2)
        da.append(dict(u=np.array([math.cos(a), math.sin(a)]) * r_, z=math.sqrt(max(0.0, 1 - r_ * r_))))
    n_da = len(da)
    gio = np.linspace(T_HUT, T_EP0 - 0.05, n_da)
    ten_da = ["ve_1", "ve_2", "ve_3", "ve_4", "ve_5", "vun_1", "vun_2", "vun_3", "trang_nho"]
    for j, d in enumerate(da):
        d["ten"] = ten_da[rng.randint(len(ten_da))] if j % 7 else "trang_nho"
        d["sz"] = (rng.uniform(26, 38) if d["ten"].startswith("ve") or d["ten"] == "trang_nho" else rng.uniform(22, 32)) * (1.15 if d["z"] > 0.5 else 1.0)
        d["ang"] = rng.uniform(0, 360)
        d["seed"] = rng.randint(2)
        d["lua"] = rng.uniform() < 0.45
        d["bay"] = rng.uniform(0.34, 0.5)
        goc = rng.uniform(-165, -35) if rng.uniform() < 0.8 else rng.uniform(160, 195)   # từ trên trời (trái → phải trên) và bên trái,
        d["tu"] = FOE_C + np.array([math.cos(math.radians(goc)), math.sin(math.radians(goc))]) * rng.uniform(300, 380)  # không cắt qua tướng mình
        d["den"] = gio[j] + d["bay"]
    quay = lambda t: 0.25 * (t - T_HUT)                      # vỏ xoay chậm

    def cho_bam(d, t):
        a = quay(t)
        c_, s_ = math.cos(a), math.sin(a)
        u = d["u"]
        v = np.array([u[0] * c_ - u[1] * s_, u[0] * s_ + u[1] * c_]) * np.array([1.0, 0.96])
        return FOE_C + v * rs(t)

    def ve_da(d, t, k_no=None):
        g = fx.FRONT if d["z"] >= 0 else fx.BACK
        lop = 44 + int(4 * (d["z"] + 1))
        ksz = (rs(t) / RS0) ** 0.55
        return sprite(g, lop, d["ten"], cho_bam(d, t), d["sz"] * ksz, d["ang"] + 40 * quay(t), 1.0, d["seed"])

    for j, d in enumerate(da):
        def bay(s, d=d):
            q = fx.P(d["tu"].copy(), (0, 0), d["bay"], group=fx.FRONT, d=d)

            def ve(q, k):
                f = min(1.0, q.age / q.d["bay"])
                b = cho_bam(q.d, s.t)
                vi = lambda ff: q.d["tu"] + (b - q.d["tu"]) * max(0.0, ff) ** 1.6
                p = vi(f)
                out = []
                # đuôi: dải liền thon dần theo đường bay (thiên thạch: lửa cam / vàng; đá: bụi be), viền mực, ngắn lại khi sắp bám
                dai = (0.22 if q.d["lua"] else 0.32) * (1.0 - 0.6 * max(0.0, f - 0.8) / 0.2)
                cs = [vi(f - dai * i / 6) for i in range(7)]
                if np.hypot(*(cs[0] - cs[-1])) > 6:
                    w0 = q.d["sz"] * (0.36 if q.d["lua"] else 0.24)
                    lops = ((1.0, LUA[0]), (0.66, LUA[2]), (0.32, LUA[3])) if q.d["lua"] else ((1.0, DUST[2]), (0.55, DUST[3]))
                    for lop, (kw, col) in enumerate(lops):
                        L_, R_ = [], []
                        for i, c in enumerate(cs):
                            dv = cs[max(0, i - 1)] - cs[min(6, i + 1)]
                            nn = np.array([-dv[1], dv[0]]) / (np.hypot(*dv) or 1.0)
                            gon = 1.0 + (0.28 * math.sin(i * 1.9 + s.t * 38 + lop) if q.d["lua"] else 0.0)     # mép lửa gợn
                            hw = w0 * kw * (1 - i / 6) ** 0.8 * gon
                            L_.append(tuple(c + nn * hw))
                            R_.append(tuple(c - nn * hw))
                        pts = L_ + R_[::-1]
                        if lop == 0 and q.d["lua"]:
                            out.append(fx.poly(fx.FRONT, 48, pts, INK, 1.0, 2.2))
                        out.append(fx.poly(fx.FRONT, 49 + lop * 0.1, pts, col, 1.0 if q.d["lua"] else 0.8))
                out.append(sprite(fx.FRONT, 50, q.d["ten"], p, q.d["sz"] * 1.1, q.d["ang"] + 200 * f, 1.0, q.d["seed"]))
                return out
            q.draw = ve
            s.add(q)

            def bam(s2, d=d):
                b = cho_bam(d, s2.t)
                T5.bui(s2, b, vel=np.array([s2.rng.uniform(-20, 20), -15.0]), r0=5, r1=12, life=0.4)
                for _ in range(2):
                    T5.dam_da(s2, b, np.array([s2.rng.uniform(-120, 120), s2.rng.uniform(-150, -40)]), size=s2.rng.uniform(2.5, 4),
                              col=TRANG[1], ground=fx.FOE[1] + s2.rng.uniform(-4, 8))
                s2.shake(0.03)
                v = fx.P(b, (0, 0), 99.0, group=fx.FRONT, d=d)
                v.draw = lambda q, k: [] if s2.t >= T_NO else [ve_da(q.d, s2.t)]
                s2.add(v)
            s.at(d["den"], bam)
        sim.at(d["den"] - d["bay"], bay)

    # 3. ép: bụi và dăm phì ra ở mép vỏ khi vỏ co lại
    def phi(s, x):
        a = rng.uniform(0, 2 * math.pi)
        u = np.array([math.cos(a), math.sin(a)])
        p = FOE_C + u * rs(s.t) * 0.95
        T5.bui(s, p, vel=u * rng.uniform(40, 90), r0=5, r1=13, life=0.45)
        if rng.uniform() < 0.5:
            T5.dam_da(s, p, u * rng.uniform(80, 160) + np.array([0, -60.0]), size=rng.uniform(2, 3.5), col=TRANG[1],
                      ground=fx.FOE[1] + rng.uniform(-4, 8))
    sim.every(T_EP0 + 0.05, T_EP2 + 0.15, 30.0, phi)
    sim.at(T_EP0 + 0.05, lambda s: s.shake(0.2))

    # 4. mặt trời trên đầu đối thủ: đĩa phẳng nhiều lớp + vành lưỡi lửa quay, no_ bật ra; co lại lấy đà rồi phình khi bắn
    SUN = np.array([FOE_C[0] + 6.0, 62.0])                # dưới mép sân (đỉnh vành lửa ~ y 20), trên quả cầu đá đã ép
    RSUN = 25.0

    def r_sun(t):
        a = fx.ease_out((t - T_GOI) / 0.28) * (1.0 + 0.12 * math.sin(math.pi * min(1.0, (t - T_GOI) / 0.28)))
        a *= 1.0 - 0.10 * hoat.bao(t, T_TIA - 0.2, T_TIA, 0.15, 0.02) + 0.18 * hoat.bao(t, T_TIA, T_TIA + 0.32, 0.04, 0.2)
        a *= 1.0 - hoat.ease((t - (T_NO + 0.35)) / 0.35, "in")
        return RSUN * max(0.0, a)

    def ve_sun(q, k):
        t = sim.t
        r = r_sun(t)
        if r < 1.0:
            return []
        out = []
        n = 12
        rot = t * 1.4
        for j in range(n):                                # lưỡi lửa vành: tam giác cong, dài ngắn xen kẽ, phập phồng lệch pha
            a = rot + 2 * math.pi * j / n
            L = r * (0.55 + 0.18 * (j % 2) + 0.08 * math.sin(t * 9 + j * 1.7))
            w = 0.22
            pts = [(SUN[0] + r * 0.85 * math.cos(a - w), SUN[1] + r * 0.85 * math.sin(a - w)),
                   (SUN[0] + (r + L) * math.cos(a + 0.10), SUN[1] + (r + L) * math.sin(a + 0.10)),
                   (SUN[0] + r * 0.85 * math.cos(a + w), SUN[1] + r * 0.85 * math.sin(a + w))]
            out.append(fx.poly(fx.BACK, 20, pts, INK, 1.0, 2.2))
            out.append(fx.poly(fx.BACK, 21, pts, LUA[1 if j % 2 else 0], 1.0))
        for lop, (rr, col) in enumerate(((1.0, LUA[0]), (0.80, LUA[1]), (0.58, LUA[2]), (0.34, LUA[3]))):
            pts = [(SUN[0] + r * rr * math.cos(a), SUN[1] + r * rr * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 28)[:-1]]
            if lop == 0:
                out.append(fx.poly(fx.BACK, 22, pts, INK, 1.0, 2.6))
            out.append(fx.poly(fx.BACK, 23 + lop, pts, col, 1.0))
        return out
    sun = fx.P(SUN.copy(), (0, 0), 99.0, group=fx.BACK)
    sun.draw = ve_sun
    sim.at(T_GOI, lambda s: (s.add(sun), s.shake(0.15)))

    def hoi_nong(s, x):
        fx.heat(s, SUN + np.array([rng.uniform(-30, 30), 20.0]), h=30, n=2, group=fx.BACK)
    sim.every(T_GOI + 0.1, T_NO + 0.4, 5.0, hoi_nong)

    # 5. tia nhiệt: mảng liền dọc từ đáy mặt trời xuống quả cầu đá, mép gợn, bốn lớp (mực, cam, vàng, kem)
    def w_tia(t):
        return 46.0 * fx.ease_out((t - T_TIA) / 0.06) * (1.0 - hoat.ease((t - (T_TIA + 0.32)) / 0.16, "in")) * (t >= T_TIA)

    def ve_tia(q, k):
        t = sim.t
        w = w_tia(t)
        if w < 1.0:
            return []
        y0 = SUN[1] + r_sun(t) * 0.6
        y1 = FOE_C[1] + 6.0
        ys = np.linspace(y0, y1, 14)
        out = []
        for lop, (kw, col) in enumerate(((1.0, LUA[0]), (0.72, LUA[1]), (0.46, LUA[2]), (0.22, LUA[3]))):
            L, Rr = [], []
            for yy in ys:
                g = 1.0 + 0.09 * math.sin(yy * 0.13 + t * 40 + lop) + 0.05 * math.sin(yy * 0.31 - t * 27)
                hw = w * kw / 2 * g * (1.0 + 0.25 * ((yy - y0) / (y1 - y0)))     # loe dần xuống dưới
                L.append((SUN[0] - hw + (FOE_C[0] - SUN[0]) * (yy - y0) / (y1 - y0), yy))
                Rr.append((SUN[0] + hw + (FOE_C[0] - SUN[0]) * (yy - y0) / (y1 - y0), yy))
            pts = L + Rr[::-1]
            if lop == 0:
                out.append(fx.poly(fx.FRONT, 70, pts, INK, 1.0, 3.0))
            out.append(fx.poly(fx.FRONT, 71 + lop, pts, col, 1.0))
        return out
    tia = fx.P(SUN.copy(), (0, 0), 99.0, group=fx.FRONT)
    tia.draw = ve_tia
    sim.at(T_TIA, lambda s: (s.add(tia), s.shake(0.35)))

    def toe_tia(s, x):                                   # chỗ tia đập vào vỏ đá: lửa toé hai bên
        a = rng.uniform(-math.pi * 0.95, -math.pi * 0.05)
        fx.flame(s, FOE_C + np.array([rng.uniform(-14, 14), -rs(s.t) * 0.7]), np.array([math.cos(a), math.sin(a)]) * rng.uniform(120, 220),
                 rng.uniform(0.25, 0.4), 6, 16, style="tron", pal="lua", group=fx.FRONT, acc=(0, -120), smoke_p=0.3, ember_p=0.2)
    sim.every(T_TIA + 0.02, T_NO, 60.0, toe_tia)

    # mây nấm: hình dựng sẵn (cột 5 cụm + mũ 9 cụm vòm + 4 cụm cuộn dưới mép), mỗi cụm là khói phẳng viền mực (sblob / ssolid như
    # fxlib.mat_smoke), cả khối chung một viền; màu theo tuổi: lửa → khói lửa → than → xám; bốc lên, no_ rồi co dần, nhạt dần (không vụt tắt)
    TAM_NAM = [(-1.0, 0.0), (-0.62, -0.42), (-0.2, -0.62), (0.22, -0.6), (0.64, -0.4), (1.0, 0.02), (-0.4, -0.15), (0.0, -0.25), (0.42, -0.12)]
    CUON = [(-1.12, 0.38), (-0.6, 0.42), (0.6, 0.42), (1.14, 0.36)]

    def ve_nam(q, k):
        t = sim.t - q.t0
        out = []
        len_ = fx.ease_out(min(1.0, t / 0.55))
        y_mu = FOE_C[1] - 14.0 - 64.0 * len_ - 5.0 * t
        no_ = fx.ease_out(min(1.0, t / 0.6)) * (1.0 + 0.10 * t)
        tan = 1.0 - 0.55 * fx.smoothstep(1.1, 2.1, t)
        a_fill = 1.0 - fx.smoothstep(1.5, 2.15, t)
        a_ink = 1.0 - fx.smoothstep(1.3, 1.9, t)
        if a_fill < 0.03:
            return []
        Wm, Hm = 70.0 * no_, 34.0 * no_
        cum = []
        for i in range(5):                                # cột: từ chỗ nổ lên tới mũ, hẹp, lắc nhẹ
            f = (i + 0.5) / 5
            y = FOE_C[1] + (y_mu + Hm * 0.3 - FOE_C[1]) * f
            cum.append((np.array([FOE_C[0] + 4.0 * math.sin(t * 5 + i), y]), (19.0 + 5.0 * (1 - f)) * no_, 0.15 + 0.1 * i, i))
        for j, (dx, dy) in enumerate(CUON):               # cụm cuộn dưới mép mũ
            cum.append((np.array([FOE_C[0] + dx * Wm, y_mu + dy * Hm]), 13.0 * no_, 0.25, 10 + j))
        for j, (dx, dy) in enumerate(TAM_NAM):            # vòm mũ
            cum.append((np.array([FOE_C[0] + dx * Wm, y_mu + dy * Hm]), (19.0 + 4.0 * ((j * 7) % 3)) * no_, 0.0, 20 + j))
        con = []
        for pos, r, tre, sd in cum:
            kk = max(0.0, t - 0.25 - tre * 0.3) / 1.7
            col = fx.ramp([LUA[2], LUA[1]] + fx.SMOKE_FIRE[1:] + [fx.SMOKE_DARK[2]], min(1.0, kk) ** 0.8)
            rr = r * tan
            ang = (sd * 47 + t * (40 if sd % 2 else -40)) % 360
            con.append(fx.item(fx.FRONT, 10, "ssolid", sd % 4, INK, pos, 2 * rr + 4.0, 1.0, ang, a_ink))
            con.append(fx.item(fx.FRONT, 11, "sblob", sd % 4, col, pos, 2 * rr, 1.0, ang, 1.0))
        # cả khối vẽ đặc rồi làm trong 0,82 một lần (che đối thủ thì phải trong: vfx-petclash mục 1)
        return [(fx.FRONT, 40, "@lop", tuple(sorted(con, key=lambda it: it[1])), None, (0.0, 0.0), 0, 0, 0, 0.82 * a_fill)]

    # 6. nổ hình nấm: chớp, rung, vỏ đá văng tứ tung, cầu lửa, cột khói bốc lên, mũ nấm toả ngang, vành bụi trên đất
    CAU_LUA = [(230, 82, 36), (246, 140, 44), (252, 204, 78), (255, 244, 210)]

    def cau_lua(s):
        """cầu lửa bốn lớp: vòng 9 cụm + cụm giữa mỗi lớp, phình 0,16 s, bốc lên; lõi co trước, lớp ngoài nguội thành than (như HatThoTinh.TtCauLua)."""
        q = fx.P(FOE_C.copy(), (0, 0), 1.05, group=fx.FRONT, t0=s.t, ph=rng.uniform(0, 6.28))
        R1 = 0.6 * fx.H

        def ve(q, k):
            t = sim.t - q.t0
            R = R1 * fx.ease_out(min(1.0, t / 0.16)) * (1 + 0.12 * t)
            c = q.pos + np.array([0.0, -45.0 * t ** 1.3])
            a_ink = 1 - fx.smoothstep(0.55, 0.9, t)
            a_fill = 1 - fx.smoothstep(0.75, 1.05, t)
            if a_fill < 0.03 or R < 1:
                return []
            out = []
            for lop in range(4):
                co = [1.0, 0.8 * (1 - 0.6 * fx.smoothstep(0.35, 0.85, t)), 0.58 * (1 - fx.smoothstep(0.25, 0.7, t)),
                      0.36 * (1 - fx.smoothstep(0.18, 0.55, t))][lop]
                r = R * co
                if r < 1.5:
                    continue
                cs = []
                for i in range(12):                       # 12 múi to nhỏ không đều (như HatThoTinh.TtCauLua)
                    h1 = (math.sin(i * 12.9898 + q.ph) * 43758.55) % 1.0
                    h2 = (math.sin(i * 78.233 + q.ph) * 12543.1) % 1.0
                    a = q.ph + i * 0.5236 + 0.18 * math.sin(t * 6 + i)
                    ro = r * (0.42 + 0.22 * h1)
                    rc = r * (0.3 + 0.26 * h2) * (1 + 0.14 * math.sin(i * 1.7 + t * 10 + lop))
                    cs.append((c[0] + ro * math.cos(a), c[1] + ro * 0.9 * math.sin(a), rc))
                cs.append((c[0], c[1], 0.62 * r))
                col = fx.lerp(CAU_LUA[0], (58, 48, 46), fx.smoothstep(0.4, 0.9, t)) if lop == 0 else CAU_LUA[lop]
                for x, y, rr in cs:
                    pts = [(x + rr * math.cos(a), y + rr * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 18)[:-1]]
                    if lop == 0 and a_ink > 0.03:
                        out.append(fx.poly(fx.FRONT, 36, pts, INK, a_fill * a_ink, 2.4))
                    out.append(fx.poly(fx.FRONT, 36.1 + 0.1 * lop, pts, col, a_fill))
            return out
        q.draw = ve
        s.add(q)

    def sao_chop(s, pos, r, n, life):
        q = fx.P(np.array(pos, float), (0, 0), life, group=fx.FRONT, r=r, n=n)
        q.draw = lambda q, k: T5.ve_khoi(fx.FRONT, 60, q.pos, [((q.r if j % 2 == 0 else q.r * 0.42) * math.cos(j * math.pi / (q.n / 2)),
                                                                (q.r if j % 2 == 0 else q.r * 0.42) * math.sin(j * math.pi / (q.n / 2)))
                                                               for j in range(q.n)], KEM, 2.6)
        s.add(q)

    def no_epic(s):
        """phần thêm của vụ nổ (người dùng 2026-11-18: "phải nổ thật epic, sau đó nổ xong có khói đen tỏa ra thì hiện tướng đằng sau khói đen
        mờ mờ"): sao chớp lớn, cầu lửa bốn lớp, cột lửa, vòng sóng, tia lửa, nứt đất, ba tiếng nổ phụ, khói đen dày."""
        t0 = s.t
        sao_chop(s, FOE_C, 0.95 * fx.H * 0.5, 12, 0.16)
        cau_lua(s)
        for _ in range(26):
            a = -math.pi * rng.uniform(0.02, 0.98)
            fx.spark(s, FOE_C, np.array([math.cos(a), math.sin(a)]), rng.uniform(380, 720), life=rng.uniform(0.35, 0.6), size=11)
        fx.ring(s, FOE_C, 0.32, 24, 170, col=KEM, squash=1.0, group=fx.FRONT, layer=62, band=(8.0, 1.5))
        fx.ring(s, np.array([FOE_C[0], fx.FOE[1] + 2.0]), 0.65, 40, 300, col=KEM, squash=0.28, group=fx.FLOOR, band=(8.0, 1.6))
        s.at(t0 + 0.08, lambda s2: fx.ring(s2, FOE_C, 0.42, 30, 240, col=CAU_LUA[1], squash=1.0, group=fx.FRONT, layer=61.5, band=(9.0, 1.6)))
        s.at(t0 + 0.12, lambda s2: setattr(s2, "flash", max(s2.flash, 0.2)))
        s.at(t0 + 0.22, lambda s2: s2.shake(0.4))
        for j in range(5):
            a = (j - 2) * 0.55 + rng.uniform(-0.15, 0.15) + (0 if j % 2 == 0 else math.pi)
            dn = np.array([math.cos(a), 0.32 * math.sin(a)])
            T5.vet_nut(s, fx.FOE + dn * 10, fx.FOE + dn * rng.uniform(70, 130), t0, 0.18)

        def cot(s2, x):
            fx.flame(s2, FOE_C + np.array([rng.uniform(-12, 12), -rng.uniform(0, 24)]), np.array([rng.uniform(-40, 40), -rng.uniform(380, 640)]),
                     rng.uniform(0.3, 0.5), 10, 26, style="tron", pal="lua", group=fx.FRONT, acc=(0, -200), smoke_p=0.3, ember_p=0.2)
        s.every(t0, t0 + 0.32, 50, cot)

        def phu(s2):
            a = rng.uniform(0, 6.28)
            pp = FOE_C + np.array([math.cos(a), 0.7 * math.sin(a)]) * rng.uniform(0.35, 0.6) * fx.H
            sao_chop(s2, pp, 0.17 * fx.H, 10, 0.12)
            for _ in range(4):
                fx.flame(s2, pp, rng.uniform(-120, 120, 2) + np.array([0, -80.0]), rng.uniform(0.25, 0.4), 8, 20, group=fx.FRONT, smoke_p=0.5)
            s2.shake(0.12)
        for j in range(3):
            s.at(t0 + 0.12 + 0.11 * j, phu)

        def khoi(s2, x):                                  # khói đen dày toả ra, phần lớn lớp trước (phủ chỗ đối thủ)
            a = -math.pi * rng.uniform(-0.15, 1.15)
            u = np.array([math.cos(a), math.sin(a)])
            fx.smoke(s2, FOE_C + u * rng.uniform(0, 0.3) * fx.H, vel=u * rng.uniform(50, 160) + np.array([0, -rng.uniform(10, 50)]),
                     life=rng.uniform(1.7, 2.4), r0=18, r1=rng.uniform(44, 68), pal=fx.SMOKE_DARK,
                     group=fx.FRONT if rng.uniform() < 0.75 else fx.BACK, rise=20, with_ash=0.45)
        s.every(t0 + 0.1, t0 + 0.62, 72, khoi)

        def khoi_thap(s2, x):
            d = -1 if rng.uniform() < 0.5 else 1
            fx.smoke(s2, np.array([FOE_C[0] + d * rng.uniform(0, 40), fx.FOE[1] - rng.uniform(10, 30)]),
                     vel=np.array([d * rng.uniform(120, 230), -rng.uniform(10, 40)]), life=rng.uniform(1.4, 2.0), r0=14, r1=rng.uniform(34, 50),
                     pal=fx.SMOKE_DARK, group=fx.FRONT, rise=12, with_ash=0.3)
        s.every(t0 + 0.15, t0 + 0.5, 30, khoi_thap)

    def no(s):
        s.flash = 0.45
        s.shake(1.0)
        s.foe_k = 1.0
        no_epic(s)
        s.hero_fx["foe"] = {"tint": KEM, "amt": 1.0, "decay": 2.2, "off": (-10.0, -4.0), "sq": (1.0, 1.0)}
        s.at(s.t + 0.25, lambda s2: s2.hero_fx.get("foe", {}).update(off=(-4.0, 0.0)))
        s.at(s.t + 0.5, lambda s2: s2.hero_fx.get("foe", {}).update(off=(0.0, 0.0)))
        for d in da:                                     # vỏ đá văng
            b = cho_bam(d, s.t)
            u = fx.unit(b - FOE_C + np.array([0.0, -6.0]))
            v = u * s.rng.uniform(200, 460) + np.array([0.0, -s.rng.uniform(120, 260)])
            p = fx.P(b, v, s.rng.uniform(1.4, 1.8), acc=np.array([0, 900.0]), ground=fx.FOE[1] + s.rng.uniform(-6, 60), bounce=0.35,
                     spin=s.rng.uniform(-9, 9), group=fx.FRONT if d["z"] >= 0 else fx.BACK, d=d, drag=0.3)
            p.draw = lambda q, k: [sprite(q.group, 46, q.d["ten"], q.pos, q.d["sz"] * 0.62, math.degrees(q.ang), 1 - max(0.0, k - 0.72) / 0.28,
                                          q.d["seed"])]
            s.add(p)
        for _ in range(26):
            T5.dam_da(s, FOE_C + s.rng.uniform(-14, 14, 2), np.array([s.rng.uniform(-420, 420), s.rng.uniform(-460, -100)]),
                      size=s.rng.uniform(3, 7), col=(TRANG + DA)[s.rng.randint(6)], ground=fx.FOE[1] + s.rng.uniform(-6, 60))
        for _ in range(14):                              # cầu lửa (ngắn, phía trước, rồi nhường chỗ cho mây nấm sau đối thủ)
            a = s.rng.uniform(0, 2 * math.pi)
            fx.flame(s, FOE_C + s.rng.uniform(-10, 10, 2), np.array([math.cos(a), math.sin(a) - 0.3]) * s.rng.uniform(60, 170),
                     s.rng.uniform(0.25, 0.4), 12, 28, style="tron", pal="lua", group=fx.FRONT, acc=(0, -160), smoke_p=0.25,
                     smoke_pal=fx.SMOKE_FIRE, smoke_big=1.0, ember_p=0.3)
        nam = fx.P(FOE_C.copy(), (0, 0), 2.2, group=fx.FRONT, t0=s.t)
        nam.draw = ve_nam
        s.add(nam)
        fx.ring(s, np.array([FOE_C[0], fx.FOE[1] + 2.0]), 0.7, 30, 190, col=DUST[2], squash=0.28, group=fx.FLOOR, band=(9.0, 2.0))
        fx.ring(s, FOE_C, 0.35, 20, 120, col=KEM, squash=1.0, group=fx.FRONT, layer=62, band=(8.0, 1.5))
        for j in range(14):                              # bụi lan sát đất
            d_ = -1 if j % 2 else 1
            T5.bui(s, np.array([FOE_C[0] + d_ * s.rng.uniform(10, 40), fx.FOE[1] - 4.0]), vel=np.array([d_ * s.rng.uniform(120, 260), -18.0]),
                   r0=12, r1=30, life=s.rng.uniform(0.8, 1.2), group=fx.FRONT if j % 3 else fx.BACK)
    sim.at(T_NO, no)

    # 7. đáp đất
    def dap(s):
        T5.vong_dat(s, fx.ME + np.array([0.0, 2.0]), 110, 0.55)
        for d in (-1, 1):
            for j in range(2):
                T5.bui(s, fx.ME + np.array([d * (30.0 + 18 * j), -2.0]), vel=np.array([d * (100.0 + 40 * j), -25.0]), r0=10, r1=26)
        s.shake(0.45)
    sim.at(T_DAT, dap)


CONG_THUC = {"attack": (attack, "Đánh thường: nhảy nện", True),
             "cast": (cast, "Chiêu mana: gầm, gai lưng phóng", False),
             "skill": (skill, "Chiêu cuối: thiên thạch bọc, mặt trời, nổ nấm", False)}


def trang():
    gifs = [f"thach_de_{c}.gif" for c in ("attack", "cast", "skill") if os.path.exists(os.path.join(RA, f"thach_de_{c}.gif"))]
    the = "".join(f'<figure><img src="{g}"><figcaption>{CONG_THUC[g[9:-4]][1]}</figcaption></figure>' for g in gifs)
    open(os.path.join(RA, "xem.html"), "w", encoding="utf-8").write(
        "<!doctype html><meta charset=utf-8><title>Thổ Tinh: xem trước chiêu</title><style>body{font:15px sans-serif;margin:16px;"
        "background:#f4f1ea}figure{display:inline-block;margin:8px;background:#fff;padding:6px;border:1px solid #ddd}img{width:540px;"
        "display:block}</style><h1>Thổ Tinh (final boss đảo Thổ): xem trước chiêu</h1><p>Rig thật + VFX tạm bằng Python (sẽ làm lại "
        "trong Unity). Tướng mình dưới phải, đối thủ trên trái. Rig riêng từng clip: <a href=\"../rig/xem.html\">rig/xem.html</a>.</p>" + the)
    print(os.path.join(RA, "xem.html"))


if __name__ == "__main__":
    chon = sys.argv[1] if len(sys.argv) > 1 else "all"
    T = Thach()
    for clip, (fn, nhan, lao) in CONG_THUC.items():
        if chon in ("all", clip):
            chay(T, clip, fn, f"thach_de_{clip}", nhan=nhan, lao=lao)
    trang()
