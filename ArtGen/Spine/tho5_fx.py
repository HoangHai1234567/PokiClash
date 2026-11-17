# -*- coding: utf-8 -*-
"""Bản xem trước chiêu của năm tướng đầu đảo Thổ trên sân có ĐỐI THỦ + VFX hạt phẳng (fxlib), để người dùng hình dung chiêu đánh thế
nào trước khi làm VFX trong Unity (người dùng 2026-11-17: "tôi chưa tưởng tượng 2 chiêu mana và cuối là sẽ đánh như nào").

Tướng mình = khung rig THẬT (nướng từ <mã>_rig.py), lật quay về địch, đặt ở chỗ phe mình (fxlib.ME, dưới phải); địch ở fxlib.FOE (trên
trái). Xương far của rig đặt đúng giữa thân địch nên mảnh bay (sỏi) bay đúng chỗ như game sẽ lái. VFX hệ Thổ (skill-petclash mục 5): khối
đá góc cạnh, rơi nặng nảy một lần, bụi tròn nhạt, sỏi; pha lê hổ phách. Không glow, không gradient, viền mực.

    tho5_fx.py cong_da [cast|skill|attack|all]   → inbox/tho5_fx/cong_da_<clip>.gif + _soi.png, trang inbox/tho5_fx/xem.html
"""
import importlib
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fxlib as fx  # noqa: E402
from quai import hoat, soi  # noqa: E402

RA = os.path.join(HERE, "inbox", "tho5_fx")
K, M = fx.K, fx.M
INK = (43, 33, 24)
DUST = [(122, 98, 72), (176, 148, 110), (214, 192, 152), (236, 222, 194)]      # bụi đất: nâu → be
DA = [(118, 104, 90), (150, 136, 118), (184, 170, 150)]                         # dăm đá xám nâu
AMBER = [(240, 166, 46), (255, 210, 112)]                                       # pha lê hổ phách: mặt chính, mặt sáng
FOE_IMG = "inbox/ti_tach_1/tai_ve/L1_duyet.png"
BG = "battle_moc_c03.png"
FOE_C = fx.FOE + np.array([0.0, -fx.H * 0.45])                                   # giữa thân địch (đơn vị sân)


# ---------------------------------------------------------------- hạt hệ Thổ
def _rot(pts, a):
    c, s = math.cos(a), math.sin(a)
    return [(x * c - y * s, x * s + y * c) for x, y in pts]


def ve_khoi(group, layer, pos, pts, col, ink=2.4, alpha=1.0, mat_sang=None):
    """một khối đa giác có viền mực (lớp mực nở dưới, lớp màu trên), tuỳ chọn một mặt sáng."""
    P = [(pos[0] + x, pos[1] + y) for x, y in pts]
    out = [fx.poly(group, layer, P, INK, alpha, ink), fx.poly(group, layer + 0.1, P, col, alpha)]
    if mat_sang:
        out.append(fx.poly(group, layer + 0.2, [(pos[0] + x, pos[1] + y) for x, y in mat_sang[0]], mat_sang[1], alpha))
    return out


def dam_da(sim, pos, vel, size=5.0, col=None, life=None, group=fx.FRONT, ground=None):
    """dăm đá: tứ giác méo xoay, rơi có trọng lực, chạm đất nảy một lần rồi nằm, mờ dần."""
    rng = sim.rng
    col = col or DA[rng.randint(len(DA))]
    pts = [(rng.uniform(0.7, 1.0) * size * math.cos(a), rng.uniform(0.7, 1.0) * size * math.sin(a))
           for a in np.linspace(0, 2 * math.pi, 5)[:-1] + rng.uniform(0, 1.5)]
    p = fx.P(pos, vel, life or rng.uniform(0.6, 0.9), acc=np.array([0, 900.0]), drag=0.6, spin=rng.uniform(-14, 14), group=group,
             ground=ground, bounce=0.35, pts=pts, col=col)
    p.draw = lambda q, k: ve_khoi(q.group, 45, q.pos, _rot(q.pts, q.ang), q.col, 2.0, 1.0 - max(0.0, k - 0.7) / 0.3)
    return sim.add(p)


def bui(sim, pos, vel=None, r0=7.0, r1=20.0, life=None, group=fx.FRONT, rise=18.0):
    return fx.smoke(sim, pos, vel=vel, life=life or sim.rng.uniform(0.55, 0.9), r0=r0, r1=r1, pal=DUST, group=group, rise=rise,
                    with_ash=0.0)


def vong_dat(sim, pos, R1=60.0, life=0.45):
    return fx.ring(sim, pos, life, R1 * 0.25, R1, col=DUST[2], squash=0.30, group=fx.FLOOR, band=(6.0, 1.2), ink=True)


def soi_bay(sim, a, b, t_bay, size=7.0, vong=40.0):
    """viên sỏi (tròn xám, viền mực) bay vồng từ a tới b trong t_bay giây (dùng cho bản xem trước khi rig không tự bay)."""
    a, b = np.array(a, float), np.array(b, float)
    p = fx.P(a, (0, 0), t_bay, group=fx.FRONT, a0=a, b0=b, vong=vong)
    def upd(q, dt, s):
        f = min(1.0, q.age / q.life)
        n = np.array([-(q.b0 - q.a0)[1], (q.b0 - q.a0)[0]])
        n = n / (np.hypot(*n) or 1.0)
        q.pos = q.a0 + (q.b0 - q.a0) * f + n * q.vong * math.sin(math.pi * f) - q.vel * dt
    p.upd = upd
    pts = [(size * math.cos(t), size * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 10)[:-1]]
    p.draw = lambda q, k: ve_khoi(q.group, 46, q.pos, pts, DA[1], 2.2)
    return sim.add(p)


def manh_pha_le(sim, pos, vel, L=26.0, Wd=10.0, life=1.0, group=fx.FRONT, on_hit=None, y_cham=None):
    """mảnh pha lê hổ phách lăng trụ nhọn, chĩa theo hướng bay; y_cham: chạm mức này thì gọi on_hit rồi tắt."""
    p = fx.P(pos, vel, life, group=group, L=L, Wd=Wd, y_cham=y_cham, on_hit=on_hit)
    base = [(L / 2, 0), (L / 5, Wd / 2), (-L / 2, Wd / 2), (-L / 2, -Wd / 2), (L / 5, -Wd / 2)]
    sang = [(L / 2, 0), (L / 5, Wd / 2), (-L / 2, Wd / 2), (-L / 2, 0)]
    def upd(q, dt, s):
        if q.y_cham is not None and q.pos[1] >= q.y_cham and not q.dead:
            q.dead = True
            if q.on_hit:
                q.on_hit(q, s)
    p.upd = upd
    def draw(q, k):
        a = math.atan2(q.vel[1], q.vel[0])
        return ve_khoi(q.group, 47, q.pos, _rot(base, a), AMBER[0], 2.4, 1.0, (_rot(sang, a), AMBER[1]))
    p.draw = draw
    return sim.add(p)


def cham_no(sim, pos, muc=1.0, mau_dam=None):
    """một cú trúng hệ Thổ: chớp sao kem nhỏ, dăm văng đều quanh tâm, bụi tròn; muc = 1 vừa, 2 nặng."""
    rng = sim.rng
    n = int(6 * muc)
    for i in range(n):
        a = -math.pi / 2 + (i / n - 0.5) * 2.6 + rng.uniform(-0.2, 0.2)
        v = np.array([math.cos(a), math.sin(a)]) * rng.uniform(150, 260) * (0.8 + 0.25 * muc)
        dam_da(sim, pos, v, size=rng.uniform(3.5, 6.5) * (0.8 + 0.2 * muc), col=mau_dam(rng) if mau_dam else None,
               ground=fx.FOE[1] + rng.uniform(-4, 6))
    for i in range(int(3 * muc)):
        bui(sim, pos + rng.uniform(-10, 10, 2), vel=np.array([rng.uniform(-60, 60), rng.uniform(-50, -10)]), r0=8 * muc, r1=22 * muc)
    sao = fx.P(pos, (0, 0), 0.12, group=fx.FRONT, r=18.0 * muc)
    sao.draw = lambda q, k: ve_khoi(fx.FRONT, 60, q.pos, [((q.r if j % 2 == 0 else q.r * 0.42) * math.cos(j * math.pi / 5),
                                                             (q.r if j % 2 == 0 else q.r * 0.42) * math.sin(j * math.pi / 5))
                                                            for j in range(10)], (255, 246, 214), 2.2)
    sim.add(sao)
    sim.shake(0.12 * muc)
    sim.hero_fx["foe"] = {"tint": (255, 246, 214), "amt": 0.9, "decay": 7.0, "off": (-5.0 * muc, -2.0 * muc), "sq": (1.0, 1.0)}
    sim.at(sim.t + 0.08, lambda s: s.hero_fx.get("foe", {}).update(off=(0.0, 0.0)))


# ---------------------------------------------------------------- dựng rig của từng con, đặt far tuỳ ý (không sửa file rig)
def _far_tam(sk, far_xy):
    """thay tạm sk.xuong để xương "far" dựng ở far_xy (rig của agent đặt far cố định trong hàm thêm mảnh bay)."""
    goc = sk.xuong

    def xuong2(name, cha=None, x=0.0, y=0.0, *a, **k):
        if name == "far" and far_xy is not None:
            x, y = far_xy
        return goc(name, cha, x, y, *a, **k)
    sk.xuong = xuong2
    return goc


def dung_than_lan_cat(R, far_xy):
    sk, info = R.dung()
    ve0 = soi.Ve(sk)
    clips, than_cast = R.lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0) - info["y_day"]
    goc = _far_tam(sk, far_xy)
    R.them_phien_bay(sk, info, than_cast, cao)
    sk.xuong = goc
    clips, _ = R.lam_clip(sk, info, cao)
    return sk, info, clips, cao


def dung_thu_da(R, far_xy):
    sk, info = R.dung()
    ve0 = soi.Ve(sk)
    clips = R.lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0)
    clips = R.lam_clip(sk, info, cao)
    return sk, info, clips, cao


def dung_rong_cat(R, far_xy):
    sk = R.dung()
    ve0 = soi.Ve(sk)
    P0 = R.Pose()
    R.ap(P0, R.gia_tri("idle_01", 0.0))
    cao = soi.chieu_cao(ve0, P0)
    clips = R.lam_clip(sk, cao)
    return sk, None, clips, cao


DUNG = {"than_lan_cat": dung_than_lan_cat, "thu_da": dung_thu_da, "quy_nui": dung_thu_da, "rong_cat": dung_rong_cat}


GOM = [(184, 98, 58), (214, 140, 90), (232, 206, 160)]                         # đất nung: đỏ nâu, cam đất, kem
CAT = [(196, 160, 104), (222, 192, 138), (240, 222, 182)]                      # cát


def loc_cat(sim, chan, t0, t1, cao=150.0):
    """lốc cát trùm đối thủ (mảng liền): thân phễu màu cát trong mờ viền mực, các dải xoáy chéo cát sẫm chạy lên, bụi tràn ở miệng và chân
    phễu, mảnh đất nung xoay quanh; nở 0,25 s đầu, tan 0,35 s cuối (skill-petclash mục 5: khối lớn là mảng liền, hạt chỉ làm mép)."""
    dur = t1 - t0
    chan = np.array(chan, float)

    def ban_kinh(u, mo):
        return (12 + 28 * u + 30 * u ** 3) * (0.35 + 0.65 * mo)      # miệng phễu loe

    def lac(a, u):
        return 7.0 * math.sin(a * 8 + u * 4.5) * u

    def ve(q, k):
        a = q.age
        mo = min(1.0, a / 0.25) * min(1.0, (dur - a) / 0.35)
        if mo <= 0.01:
            return []
        h = cao * (0.3 + 0.7 * min(1.0, a / 0.25))
        L, Rr = [], []
        for j in range(11):
            u = j / 10.0
            y = chan[1] - u * h
            r = ban_kinh(u, mo)
            L.append((chan[0] - r + lac(a, u), y))
            Rr.append((chan[0] + r + lac(a, u), y))
        P = L + Rr[::-1]
        hinh = [(P, INK, 2.2), (P, (226, 190, 128), 0.0)]          # vẽ đặc cả khối rồi mới làm trong (không lộ lớp mực qua lớp màu)
        for i in range(6):                                       # dải xoáy chéo chạy lên
            v = (a * 1.7 + i / 6.0) % 1.0
            u0, u1 = max(0.02, v - 0.05), min(0.98, v + 0.03)
            ra, rb = ban_kinh(u0, mo), ban_kinh(u1, mo)
            ya, yb = chan[1] - u0 * h, chan[1] - u1 * h
            xa, xb = chan[0] + lac(a, u0), chan[0] + lac(a, u1)
            band = [(xa - ra * 0.92, ya), (xb + rb * 0.92, yb), (xb + rb * 0.92, yb + 5.0), (xa - ra * 0.92, ya + 5.0)]
            if 0.08 < v < 0.94:
                hinh.append((band, (168, 124, 70), 0.0))
                if i % 2 == 0:
                    band2 = [(xa - ra * 0.6, ya - 9), (xb + rb * 0.5, yb - 9), (xb + rb * 0.5, yb - 6.5), (xa - ra * 0.6, ya - 6.5)]
                    hinh.append((band2, (244, 226, 180), 0.0))
        return [fx.polys(fx.FRONT, 30, hinh, alpha=0.9 * mo)]

    def bat_dau(s):
        p = fx.P(chan.copy(), (0, 0), dur, group=fx.FRONT)
        p.draw = ve
        s.add(p)
    sim.at(t0, bat_dau)
    rng = sim.rng

    def xoay(s, x):                                              # mảnh gốm + bụi bay quanh lốc, bụi tràn miệng / chân phễu
        u = rng.uniform(0.15, 0.95)
        q = fx.P(chan + np.array([0.0, -u * cao]), (0, 0), rng.uniform(0.35, 0.6), group=fx.FRONT, u=u, a0=rng.uniform(0, 6.28),
                 col=GOM[rng.randint(2)], sz=rng.uniform(3.5, 6.0), sp=rng.uniform(9, 14))

        def upd(q, dt, s2):
            r = 18 + 50 * q.u ** 1.2
            q.pos = np.array([chan[0] + r * math.cos(q.a0 + q.age * q.sp), chan[1] - q.u * cao - 10 * q.age]) - q.vel * dt
        q.upd = upd
        pts = [(q.sz * math.cos(t), q.sz * 0.7 * math.sin(t)) for t in (0.3, 1.9, 3.4, 4.9)]
        q.draw = lambda q, k: ve_khoi(fx.FRONT, 32 if math.sin(q.a0 + q.age * q.sp) > 0 else 29, q.pos, _rot(pts, q.age * 8), q.col, 1.8)
        s.add(q)
        if rng.uniform() < 0.45:
            d = rng.choice([-1, 1])
            bui(s, chan + np.array([d * 60.0, -cao * 0.95]), vel=np.array([d * 70.0, -10.0]), r0=7, r1=18, life=0.5)
        if rng.uniform() < 0.35:
            d = rng.choice([-1, 1])
            bui(s, chan + np.array([d * 20.0, -2.0]), vel=np.array([d * 80.0, -10.0]), r0=6, r1=16, life=0.45, group=fx.BACK)
    sim.every(t0 + 0.12, t1 - 0.25, 50, xoay)


def tang_da(sim, a, b, t_bay, r=13.0, vong=70.0, on_hit=None):
    """tảng đá (đa giác xám nâu viền mực, một đốm pha lê) bay vồng từ a tới b, xoay, kéo vệt bụi; tới nơi gọi on_hit."""
    a, b = np.array(a, float), np.array(b, float)
    rng = sim.rng
    pts = [(r * rng.uniform(0.8, 1.05) * math.cos(t), r * rng.uniform(0.8, 1.05) * math.sin(t)) for t in np.linspace(0, 6.28, 8)[:-1]]
    dom = [(r * 0.35 * math.cos(t) + r * 0.2, r * 0.35 * math.sin(t) - r * 0.2) for t in np.linspace(0, 6.28, 6)[:-1]]
    p = fx.P(a.copy(), (0, 0), t_bay, group=fx.FRONT, a0=a, b0=b)

    def upd(q, dt, s):
        f = min(1.0, q.age / q.life)
        n = np.array([-(q.b0 - q.a0)[1], (q.b0 - q.a0)[0]])
        n = n / (np.hypot(*n) or 1.0)
        if n[1] > 0:
            n = -n
        q.pos = q.a0 + (q.b0 - q.a0) * f + n * vong * math.sin(math.pi * f) - q.vel * dt
        q.ang = -q.age * 9.0
        if rng.uniform() < 0.6:
            bui(s, q.pos.copy(), vel=np.array([rng.uniform(-20, 20), rng.uniform(-20, 0)]), r0=4, r1=10, life=0.35)
    p.upd = upd
    p.draw = lambda q, k: ve_khoi(q.group, 46, q.pos, _rot(pts, q.ang), DA[1], 2.4) + [
        fx.poly(q.group, 46.3, [(q.pos[0] + x, q.pos[1] + y) for x, y in _rot(dom, q.ang)], AMBER[0])]
    if on_hit:
        p.on_death = lambda q, s: on_hit(q, s)
    return sim.add(p)


def khoi_tang(r, rng):
    """đa giác tảng đá lớn + một mặt tối + một mạch hổ phách (toạ độ quanh tâm, đơn vị sân)."""
    pts = [(r * rng.uniform(0.85, 1.05) * math.cos(t), r * rng.uniform(0.85, 1.05) * math.sin(t)) for t in np.linspace(0, 6.28, 10)[:-1]]
    toi = [(x * 0.95, y * 0.95) for x, y in pts[5:9]] + [(0.0, 0.0)]
    mach = [(-0.55 * r, -0.10 * r), (0.10 * r, 0.05 * r), (0.55 * r, -0.25 * r), (0.58 * r, -0.15 * r), (0.12 * r, 0.16 * r),
            (-0.52 * r, 0.02 * r)]
    return pts, toi, mach


def ve_tang(group, layer, pos, r, ang, hinh):
    pts, toi, mach = hinh
    k = lambda P: _rot([(x * r, y * r) for x, y in P], ang)
    return (ve_khoi(group, layer, pos, k(pts), DA[1], 2.8) + [fx.poly(group, layer + 0.3, [(pos[0] + x, pos[1] + y) for x, y in k(toi)], DA[0])]
            + [fx.poly(group, layer + 0.4, [(pos[0] + x, pos[1] + y) for x, y in k(mach)], AMBER[0])])


def song_chan(sim, a, b, t0, t_bay, on_toi=None):
    """sóng chấn: dải đá góc cạnh trồi lên nối nhau dọc mặt đất từ a tới b (mỗi cụm trồi rồi lún, bụi), tới nơi gọi on_toi."""
    a, b = np.array(a, float), np.array(b, float)
    rng = sim.rng
    n = 9
    for i in range(n):
        f = (i + 1) / n
        def troi(s, f=f, i=i):
            c = a + (b - a) * f
            for j in range(2):
                h = rng.uniform(18, 30) * (0.7 + 0.5 * f)
                w = rng.uniform(8, 13)
                pts = [(-w, 0), (-w * 0.5, -h * rng.uniform(0.6, 0.9)), (rng.uniform(-3, 3), -h), (w * 0.6, -h * 0.7), (w, 0)]
                q = fx.P(c + np.array([rng.uniform(-14, 14), rng.uniform(-3, 3)]), (0, 0), 0.32, group=fx.FRONT, pts=pts)
                q.draw = lambda q, k: ve_khoi(q.group, 40, q.pos, [(x, y * min(1.0, k / 0.25) * (1 - max(0.0, k - 0.6) / 0.4)) for x, y in q.pts],
                                              DA[rng.randint(3)], 2.2)
                s.add(q)
            bui(s, c, vel=np.array([rng.uniform(-40, 40), -30.0]), r0=8, r1=20, life=0.5)
            if f >= 0.999 and on_toi:
                on_toi(s)
        sim.at(t0 + t_bay * f, troi)


def luoi_cat(sim, a, b, t_bay, R=26.0, on_hit=None):
    """lưỡi cát trăng khuyết liền (mảng, viền mực, dải sáng ở mép trước) bay thẳng từ a tới b, vệt bụi phía sau."""
    a, b = np.array(a, float), np.array(b, float)
    d = b - a
    goc = math.atan2(d[1], d[0])
    ngoai = [(R * math.cos(t), R * math.sin(t)) for t in np.linspace(-1.25, 1.25, 9)]
    trong = [(-0.25 * R + 0.95 * R * math.cos(t), 0.85 * R * math.sin(t)) for t in np.linspace(1.2, -1.2, 9)]   # lưng lưỡi dày ~0,3 R
    sang = [(0.92 * R * math.cos(t), 0.92 * R * math.sin(t)) for t in np.linspace(-1.0, 1.0, 7)] + \
           [(0.78 * R * math.cos(t), 0.78 * R * math.sin(t)) for t in np.linspace(1.0, -1.0, 7)]
    p = fx.P(a.copy(), d / t_bay, t_bay, group=fx.FRONT)
    rng = sim.rng

    def upd(q, dt, s2):
        if rng.uniform() < 0.7:
            bui(s2, q.pos - unit_(d) * R * 0.4 + rng.uniform(-6, 6, 2), vel=np.array([rng.uniform(-20, 20), -10.0]), r0=4, r1=10,
                life=0.3)
    p.upd = upd
    p.draw = lambda q, k: ve_khoi(fx.FRONT, 48, q.pos, _rot(ngoai + trong, goc), CAT[1], 2.4, 1.0, (_rot(sang, goc), CAT[2]))
    if on_hit:
        p.on_death = lambda q, s2: on_hit(q, s2)
    return sim.add(p)


def unit_(v):
    n = float(np.hypot(*v))
    return v / n if n > 1e-6 else np.array([1.0, 0.0])


def cot_da(sim, chan, w, h, t_len=0.12, giu=0.35, t_lun=0.25):
    """cột sa thạch trồi lên từ đất (kem, hai vạch son, đỉnh vỡ xiên), giữ rồi lún; bụi, dăm ở chân."""
    chan = np.array(chan, float)
    rng = sim.rng
    nghieng = rng.uniform(-0.25, 0.25) * w
    dur = t_len + giu + t_lun
    p = fx.P(chan.copy(), (0, 0), dur, group=fx.BACK)

    def ve(q, k):
        a = q.age
        hh = h * (min(1.0, a / t_len) ** 0.5 if a < t_len else (1.0 if a < t_len + giu else max(0.0, 1 - (a - t_len - giu) / t_lun)))
        if hh < 1:
            return []
        than = [(-w / 2, 0), (-w / 2, -hh + nghieng * 0.5), (0, -hh - abs(nghieng) * 0.4), (w / 2, -hh - nghieng * 0.5), (w / 2, 0)]
        out = ve_khoi(fx.BACK, 42, q.pos, than, (230, 206, 156), 2.6)
        for f in (0.35, 0.68):
            if hh > h * f + 6:
                y = -h * f
                out.append(fx.poly(fx.BACK, 42.3, [(q.pos[0] - w / 2 + 2, q.pos[1] + y), (q.pos[0] + w / 2 - 2, q.pos[1] + y - 3),
                                                    (q.pos[0] + w / 2 - 2, q.pos[1] + y + 4), (q.pos[0] - w / 2 + 2, q.pos[1] + y + 7)],
                                   (196, 134, 70)))
        return out
    p.draw = ve
    sim.add(p)
    for i in range(4):
        bui(sim, chan + np.array([rng.uniform(-w, w) * 0.6, -2.0]), vel=np.array([rng.uniform(-70, 70), rng.uniform(-50, -10)]), r0=8,
            r1=20, life=0.6)
    for i in range(5):
        dam_da(sim, chan + np.array([rng.uniform(-w, w) * 0.4, -4.0]), np.array([rng.uniform(-160, 160), rng.uniform(-300, -150)]),
               size=rng.uniform(3, 6), col=CAT[rng.randint(3)], ground=chan[1] + 2)


def vet_nut(sim, a, b, t0, t_lan=0.18):
    """vết nứt đất (dải nâu sẫm gấp khúc trên mặt đất) lan từ a tới b."""
    a, b = np.array(a, float), np.array(b, float)
    rng = sim.rng
    n = 12
    pts = [a + (b - a) * (i / n) + (np.array([0.0, rng.uniform(-5, 5)]) if 0 < i < n else 0) for i in range(n + 1)]
    p = fx.P(a.copy(), (0, 0), t_lan + 0.9, group=fx.FLOOR)

    def ve(q, k):
        m = min(n, int(n * min(1.0, q.age / t_lan)) + 1)
        al = 1.0 - max(0.0, (q.age - t_lan - 0.5) / 0.4)
        out = []
        for i in range(m):
            p0, p1 = pts[i], pts[i + 1]
            nn = np.array([-(p1 - p0)[1], (p1 - p0)[0]])
            nn = nn / (np.hypot(*nn) or 1.0) * 2.4
            out.append(fx.poly(fx.FLOOR, 5, [tuple(p0 + nn), tuple(p1 + nn), tuple(p1 - nn), tuple(p0 - nn)], (70, 50, 34), al))
        return out
    p.draw = ve
    sim.at(t0, lambda s2: s2.add(p))


def vet_can(sim, pos):
    """vết cắn: hai cung kem viền mực (hàm trên, hàm dưới) khép vào nhau 0,14 s."""
    for dau in (-1, 1):
        q = fx.P(np.array(pos, float) + np.array([0.0, dau * 10.0]), (0, 0), 0.16, group=fx.FRONT, dau=dau)
        q.draw = lambda q, k: [fx.item(fx.FRONT, 61, "arcpx", (200 if q.dau < 0 else 20) * 1000 + 140, (255, 246, 214, 6),
                                       q.pos + np.array([0, -q.dau * 8 * k]), 22, 1.6, 0, 1 - k * k)]
        sim.add(q)


# ---------------------------------------------------------------- tướng mình = khung rig thật
class Tuong:
    def __init__(self, code):
        R = importlib.import_module(f"{code}_rig")
        self.R = R
        dh = (lambda far_xy: R.dung_het(far_xy=far_xy)) if hasattr(R, "dung_het") else (lambda far_xy: DUNG[code](R, far_xy))
        s_stage = fx.H * 1.15                                     # chiều cao phe mình trên sân (như fxlib.Stage)
        sk, info, clips, cao = dh((0.0, 0.0))                     # dựng thử để đo cỡ, rồi đặt far đúng chỗ địch
        ve = soi.Ve(sk)
        idle0 = hoat.nuong(sk, clips[1])[0]
        bx = ve.bao(idle0)
        self.s = s_stage / cao                                    # đơn vị sân / đơn vị rig
        self.cx, self.yg = (bx[0] + bx[2]) / 2.0, bx[1]
        far = self.rig(FOE_C)
        sk, info, clips, cao = dh(tuple(far))
        self.sk, self.clips, self.cao = sk, {c.ten: c for c in clips}, cao
        self.ve = soi.Ve(sk)
        self.rong = (bx[2] - bx[0])

    def rig(self, p):
        """toạ độ sân → toạ độ rig (tướng lật, chân ở fx.ME)."""
        return np.array([self.cx - (p[0] - fx.ME[0]) / self.s, self.yg + (fx.ME[1] - p[1]) / self.s])

    def san(self, v):
        return np.array([fx.ME[0] - (v[0] - self.cx) * self.s, fx.ME[1] - (v[1] - self.yg) * self.s])

    def khung(self, clip, lao=False):
        fr = hoat.nuong(self.sk, self.clips[clip])
        if not lao:
            return fr
        xs = [P.t.get("move", [0.0] * 5)[0] for P in fr]
        mx = max(xs) or 1.0
        v = self.rig(fx.FOE + np.array([22.0, 6.0])) - np.array([self.cx, self.yg])   # dừng trước giữa đối thủ một chút
        out = []
        for P, x in zip(fr, xs):
            Q = P.copy()
            g = list(Q.t.get("move", [0.0, 0.0, 0.0, 1.0, 1.0]))
            k = x / mx
            g[0], g[1] = float(v[0] * k), float(v[1] * k + g[1])
            Q.t["move"] = g
            out.append(Q)
        return out

    def diem(self, P, xuong):
        return self.san(self.sk.the_gioi(P)[xuong][:2, 2])

    def anh(self, P):
        X = (fx.ME[0] - 0) / self.s + 40                         # khung đủ rộng tới mép trái sân (mảnh bay tới địch)
        Y = (fx.ME[1] + 40) / self.s
        box = (self.cx - X, self.yg - 12.0, self.cx + X, self.yg + Y)
        im = self.ve.ve(P, box, self.s * K, ss=1)
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        return im, 12.0 * self.s * K


def ve_khung(sim, art, stage, hero_img, foe_img):
    """như fxlib.render nhưng tướng mình là ảnh khung rig (neo chân giữa đáy khung, có lề 12 đơn vị dưới chân)."""
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
            fxh = sim.hero_fx.get("foe", {})
            img = stage.hero_img("foe", fxh) if fxh else foe_img
            off = fxh.get("off", (0, 0))
            sh = art.render("ell", 0, (40, 24, 20), img.width * 0.62, 18 * K, 0, 0.35)
            im.alpha_composite(sh, (int(pos[0] * K + M - sh.width / 2), int(pos[1] * K + M - sh.height / 2)))
            im.alpha_composite(img, (int(pos[0] * K + M - img.width / 2 + off[0] * K), int(pos[1] * K + M - img.height + off[1] * K)))
            continue
        if name == "@me":
            img, lech = hero_img[0], hero_img[1]
            sh = art.render("ell", 0, (40, 24, 20), hero_img[2] * K * 0.7, 18 * K, 0, 0.35)
            im.alpha_composite(sh, (int(pos[0] * K + M - sh.width / 2), int(pos[1] * K + M - sh.height / 2)))
            im.alpha_composite(img, (int(pos[0] * K + M - img.width / 2), int(pos[1] * K + M - img.height + lech)))
            continue
        if name == "polys":
            art.polys(im, seed, alpha)
            continue
        if name == "poly":
            art.poly(im, seed, col, alpha, w)
            continue
        t = art.render(name, seed, col, w * K, h * K, ang, alpha)
        x, y = int(pos[0] * K + M - t.width / 2), int(pos[1] * K + M - t.height / 2)
        if x > im.width or y > im.height or x + t.width < 0 or y + t.height < 0:
            continue
        im.alpha_composite(t, (x, y))
    if sim.flash > 0.01:
        im = Image.blend(im, Image.new("RGBA", im.size, (255, 246, 214, 255)), min(0.55, sim.flash))
    tr = sim.trauma ** 2
    dx = 12 * K * tr * math.sin(sim.t * 2 * math.pi * 11.7)
    dy = 8 * K * tr * math.sin(sim.t * 2 * math.pi * 14.3 + 1)
    return im.crop((int(M + dx), int(M + dy), int(M + dx) + fx.W * K, int(M + dy) + fx.Hs * K))


def chay(tuong, clip, build, ten, duoi=0.7, nhan="", lao=False):
    """phát clip của tướng + lịch VFX build(sim, tuong, khung) → GIF + tờ soi. lao: clip khai lunge (sân nắn quãng tới đối thủ)."""
    os.makedirs(RA, exist_ok=True)
    fr = tuong.khung(clip, lao)
    idle = tuong.khung("idle")
    n_duoi = int(duoi * fx.FPS)
    seq = fr + [idle[i % len(idle)] for i in range(n_duoi)]
    sim, art = fx.Sim(3), fx.Art()
    stage = fx.Stage(bg=BG, heroes=False)
    foe = fx.load_hero(FOE_IMG, fx.H * K)
    stage.heroes["foe"] = (foe, fx.FOE)
    build(sim, tuong, fr)
    frames = []
    for i, P in enumerate(seq):
        im, lech = tuong.anh(P)
        frames.append(ve_khung(sim, art, stage, (im, lech, tuong.rong * tuong.s), foe))
        for _ in range(4):
            sim.step(1 / fx.FPS / 4)
    fx.save(frames, RA, ten, label=nhan, hold=10)
    print(os.path.join(RA, ten + ".gif"), len(frames), "khung")


# ---------------------------------------------------------------- công thức từng tướng
def cong_da_cast(sim, T, fr):
    R = T.R
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]
    # lắc mai: bụi, dăm nhỏ rơi khỏi mai
    def rung(s, x):
        p = T.diem(tt(s.t), "hair") + s.rng.uniform(-30, 30, 2) * np.array([1.0, 0.5])
        bui(s, p, vel=np.array([s.rng.uniform(-30, 30), s.rng.uniform(-20, 20)]), r0=4, r1=11, life=0.5)
        if s.rng.uniform() < 0.5:
            dam_da(s, p, np.array([s.rng.uniform(-90, 90), s.rng.uniform(-160, -60)]), size=3.0, ground=fx.ME[1] + 4)
    sim.every(R.T_LAC0, R.T_LAC1 + 0.04, 40, rung)
    # sỏi rời mai: bụi nhỏ ở chỗ rời; tới đích: trúng
    for k in R.BAY_MANH:
        t0, t1 = R.T_PHONG[k], R.T_PHONG[k] + R.BAY
        sim.at(t0, lambda s, k=k: bui(s, T.diem(tt(R.T_PHONG[k]), f"fly_{k}"), r0=5, r1=13, life=0.45))
        sim.at(t1, lambda s, k=k: cham_no(s, FOE_C + s.rng.uniform(-14, 14, 2), 1.0))
    # đáp phịch
    sim.at(R.T_DAP_C, lambda s: (vong_dat(s, fx.ME + np.array([0, 2.0]), 70), [bui(s, fx.ME + np.array([d * 40.0, -4.0]),
                                 vel=np.array([d * 70.0, -20.0]), r0=8, r1=20) for d in (-1, 1)], s.shake(0.08)))


def cong_da_skill(sim, T, fr):
    R = T.R
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]
    # gồng: mai rung, bụi dưới chân, sỏi nảy bụi
    def gong(s, x):
        p = fx.ME + np.array([s.rng.uniform(-60, 60), -2.0])
        bui(s, p, vel=np.array([s.rng.uniform(-40, 40), -15.0]), r0=5, r1=12, life=0.5, group=fx.BACK)
    sim.every(R.T_GONG0, R.T_GONG1, 22, gong)
    sim.at(R.T_GONG0, lambda s: s.shake(0.05))
    # pha lê vọt lên: vệt mảnh pha lê bay thẳng lên, bụi bung ở hốc mai
    def ban(s):
        goc = T.diem(tt(R.T_BAN_TROI), "pha_le")
        for i in range(6):
            manh_pha_le(s, goc + np.array([s.rng.uniform(-18, 18), 0.0]), np.array([s.rng.uniform(-60, 60), -1100.0 - 120 * i]),
                        L=22, Wd=8, life=0.5)
        for i in range(4):
            bui(s, goc + s.rng.uniform(-20, 20, 2), vel=np.array([s.rng.uniform(-80, 80), s.rng.uniform(-60, -20)]), r0=7, r1=18)
        vong_dat(s, fx.ME + np.array([0, 2.0]), 80)
        s.shake(0.15)
    sim.at(R.T_BAN_TROI, ban)
    # mưa pha lê xuống địch: 7 mảnh nhỏ so le rồi một mảnh to cắm xuống
    xs = [-34, 22, -10, 36, -26, 8, 30]
    for i, dx in enumerate(xs):
        t = R.T_MUA + 0.045 * i
        def roi(s, dx=dx, i=i):
            p0 = FOE_C + np.array([dx + 70.0, -300.0])
            manh_pha_le(s, p0, np.array([-230.0, 1050.0]), L=24, Wd=9, life=0.6, y_cham=FOE_C[1] + s.rng.uniform(-30, 25),
                        on_hit=lambda q, s2: cham_no(s2, q.pos.copy(), 0.8, mau_dam=lambda r: AMBER[r.randint(2)] if r.uniform() < 0.6 else DA[1]))
        sim.at(t, roi)
    def to(s):
        p0 = FOE_C + np.array([90.0, -340.0])
        def trung(q, s2):
            cham_no(s2, q.pos.copy(), 2.0, mau_dam=lambda r: AMBER[r.randint(2)] if r.uniform() < 0.6 else DA[0])
            vong_dat(s2, fx.FOE + np.array([0, 2.0]), 95, 0.55)
            s2.flash = 0.35
            s2.shake(0.35)
            cam = fx.P(np.array([q.pos[0] + 12, fx.FOE[1] - 4.0]), (0, 0), 0.45, group=fx.FRONT)   # mảnh to cắm đất, rung rồi vỡ
            base = [(0, -46), (12, -20), (12, 8), (-12, 8), (-12, -20)]
            sang = [(0, -46), (12, -20), (12, 8), (0, 8)]
            cam.draw = lambda c, k: ve_khoi(fx.FRONT, 47, c.pos + np.array([1.5 * math.sin(c.age * 70), 0]), base, AMBER[0], 2.6, 1.0,
                                            (sang, AMBER[1]))
            cam.on_death = lambda c, s3: cham_no(s3, c.pos + np.array([0, -20.0]), 1.2,
                                                 mau_dam=lambda r: AMBER[r.randint(2)])
            s2.add(cam)
        manh_pha_le(s, p0, np.array([-260.0, 1150.0]), L=48, Wd=18, life=0.6, y_cham=FOE_C[1] + 10, on_hit=trung)
    sim.at(R.T_SKILL_TRUNG - 0.04, to)


def cong_da_attack(sim, T, fr):
    R = T.R
    sim.at(R.T_HUC, lambda s: cham_no(s, T.diem(fr[int(R.T_HUC * fx.FPS)], "mieng") + np.array([-14.0, 0.0]), 0.9))


def than_lan_cat_cast(sim, T, fr):
    R = T.R
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]
    def xoe(s, x):                                               # cát bốc quanh áo choàng lúc xoè
        p = T.diem(tt(s.t), "bone8") + s.rng.uniform(-40, 40, 2)
        bui(s, p, vel=np.array([s.rng.uniform(-40, 40), s.rng.uniform(-60, -20)]), r0=5, r1=12, life=0.5)
    sim.every(0.12, 0.45, 26, xoe)
    for k in R.PHIEN:
        t0, t1 = R.T_PHONG[k], R.T_PHONG[k] + R.BAY
        sim.at(t1, lambda s: cham_no(s, FOE_C + s.rng.uniform(-14, 14, 2), 1.0, mau_dam=lambda r: GOM[r.randint(3)]))


def than_lan_cat_skill(sim, T, fr):
    R = T.R
    def xoay_chan(s, x):                                         # cát bắt đầu xoáy quanh chân đối thủ
        a = s.rng.uniform(0, 6.28)
        bui(s, fx.FOE + np.array([50 * math.cos(a), -4 + 8 * math.sin(a)]), vel=np.array([-60 * math.sin(a), -20.0]), r0=5, r1=12,
            life=0.5, group=fx.BACK)
    sim.every(0.08, R.T_TRUNG_SKILL, 18, xoay_chan)
    def dam(s):
        vong_dat(s, fx.ME + np.array([0, 2.0]), 80)
        for d in (-1, 1):
            bui(s, fx.ME + np.array([d * 40.0, -4.0]), vel=np.array([d * 90.0, -20.0]), r0=9, r1=22)
        s.shake(0.25)
    sim.at(R.T_DAM, dam)
    loc_cat(sim, fx.FOE + np.array([0.0, 4.0]), R.T_TRUNG_SKILL - 0.06, R.T_HET + 0.2, cao=fx.H * 1.25)
    sim.at(R.T_TRUNG_SKILL, lambda s: (s.shake(0.3), s.hero_fx.update(foe={"tint": CAT[2], "amt": 0.7, "decay": 1.2, "off": (0, 0),
                                                                           "sq": (1.0, 1.0)})))


def than_lan_cat_attack(sim, T, fr):
    R = T.R
    sim.at(R.T_DOP, lambda s: (vet_can(s, FOE_C + np.array([12.0, 6.0])), cham_no(s, FOE_C + np.array([12.0, 6.0]), 0.7,
                                                                                    mau_dam=lambda r: CAT[r.randint(3)])))


def thu_da_cast(sim, T, fr):
    R = T.R
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]
    rng = sim.rng

    def hut(s, x):                                               # bụi + sỏi xoáy hút vào miệng
        m = T.diem(tt(s.t), "mieng")
        a = rng.uniform(0, 6.28)
        p0 = m + np.array([math.cos(a), math.sin(a)]) * rng.uniform(45, 70)
        q = fx.P(p0, (0, 0), 0.32, group=fx.FRONT, p0=p0, a=a)

        def upd(q, dt, s2):
            f = q.age / q.life
            mm = T.diem(tt(s2.t), "mieng")
            q.pos = q.p0 + (mm - q.p0) * f ** 1.6 - q.vel * dt
        q.upd = upd
        if rng.uniform() < 0.5:
            pts = [(3.5 * math.cos(t), 3.5 * math.sin(t)) for t in (0.2, 1.8, 3.3, 4.8)]
            q.draw = lambda q, k: ve_khoi(fx.FRONT, 45, q.pos, pts, DA[rng.randint(3)], 1.6)
        else:
            q.draw = lambda q, k: fx.mat_smoke(DUST)(q, k) if False else [fx.item(fx.FRONT, 44, "ringpx0", 3, DUST[2], q.pos, 6 * (1 - k),
                                                                                  1.0, 0, 0.9)]
        s.add(q)
    sim.every(R.T_TU, R.T_PHUN - 0.04, 40, hut)

    def phun(s):
        m = T.diem(tt(R.T_PHUN), "mieng")

        def trung(q, s2):
            cham_no(s2, q.pos.copy(), 1.6, mau_dam=lambda r: AMBER[r.randint(2)] if r.uniform() < 0.3 else DA[r.randint(3)])
            vong_dat(s2, fx.FOE + np.array([0, 2.0]), 80)
        tang_da(s, m, FOE_C + np.array([8.0, 0.0]), 0.42, r=15.0, vong=60.0, on_hit=trung)
        for i in range(3):
            bui(s, m + rng.uniform(-8, 8, 2), vel=np.array([rng.uniform(-80, -30), rng.uniform(-40, 10)]), r0=6, r1=14, life=0.4)
    sim.at(R.T_PHUN, phun)


def thu_da_skill(sim, T, fr):
    R = T.R
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]
    rng = sim.rng

    def xoay(s, x):                                              # quả cầu xoay tại chỗ: bụi tóe ra sau
        p = T.diem(tt(s.t), "day") + np.array([rng.uniform(-10, 10), -4.0])
        bui(s, p, vel=np.array([rng.uniform(40, 120), rng.uniform(-50, -10)]), r0=7, r1=18, life=0.5)
        if rng.uniform() < 0.4:
            dam_da(s, p, np.array([rng.uniform(80, 200), rng.uniform(-220, -100)]), size=3.5, ground=fx.ME[1] + 4)
    sim.every(R.T_CUON + 0.04, R.T_LAO, 34, xoay)

    def vet(s, x):                                               # lao: vệt bụi theo đường lăn
        p = T.diem(tt(s.t), "day") + np.array([0.0, -2.0])
        bui(s, p, vel=np.array([rng.uniform(-20, 20), rng.uniform(-30, -5)]), r0=8, r1=20, life=0.55, group=fx.BACK)
    sim.every(R.T_LAO, R.T_NEN, 45, vet)

    def nen(s):
        cham_no(s, FOE_C + np.array([10.0, 10.0]), 2.2, mau_dam=lambda r: AMBER[r.randint(2)] if r.uniform() < 0.5 else DA[r.randint(3)])
        vong_dat(s, fx.FOE + np.array([0, 2.0]), 110, 0.6)
        s.flash = 0.35
        s.shake(0.45)
    sim.at(R.T_NEN, nen)
    sim.at(R.T_VE, lambda s: (vong_dat(s, fx.ME + np.array([0, 2.0]), 70), s.shake(0.1)))


def thu_da_attack(sim, T, fr):
    R = T.R
    sim.at(R.T_GIANG, lambda s: (vong_dat(s, fx.ME + np.array([-40.0, 2.0]), 60), cham_no(s, FOE_C + np.array([6.0, 8.0]), 1.0),
                                 [bui(s, fx.ME + np.array([-60.0 + d * 20, -4.0]), vel=np.array([d * 60.0, -30.0]), r0=8, r1=18)
                                  for d in (-1, 1)]))


def quy_nui_cast(sim, T, fr):
    R = T.R
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]

    def nen(s):
        m = T.diem(tt(R.T_NEN), "mieng")
        vong_dat(s, np.array([m[0], fx.ME[1] + 2.0]), 95, 0.5)
        for d in (-1, 1):
            bui(s, np.array([m[0] + d * 30.0, fx.ME[1] - 4.0]), vel=np.array([d * 90.0, -30.0]), r0=10, r1=26)
        s.shake(0.3)

        def toi(s2):
            cham_no(s2, FOE_C + np.array([0.0, 14.0]), 1.8)
            s2.hero_fx["foe"] = {"tint": (255, 246, 214), "amt": 0.9, "decay": 6.0, "off": (-4.0, -16.0), "sq": (1.0, 1.0)}
            s2.at(s2.t + 0.16, lambda s3: s3.hero_fx.get("foe", {}).update(off=(0.0, 0.0)))
        song_chan(s, np.array([m[0], fx.ME[1] - 2.0]), fx.FOE + np.array([10.0, 2.0]), R.T_NEN, 0.36, toi)
    sim.at(R.T_NEN, nen)


def quy_nui_skill(sim, T, fr):
    R = T.R
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]
    rng = sim.rng
    hinh = khoi_tang(1.0, rng)
    TO = 1.8                                                     # tảng "khổng lồ": phóng to so với bán kính 100 × tỉ lệ mieng của rig
    r_max = 220.0 * T.s * TO                                     # bán kính tảng (đơn vị sân) lúc đầy

    def r_luc(t):
        return (70.0 + 150.0 * min(1.0, max(0.0, (t - R.T_TU0) / (R.T_TU1 - R.T_TU0))) ** 1.3) * T.s * TO

    tang = fx.P(np.zeros(2), (0, 0), R.T_NEM - R.T_TU0, group=fx.FRONT)

    def ve(q, k):
        t = R.T_TU0 + q.age
        m = T.diem(tt(t), "mieng")
        return ve_tang(fx.FRONT, 44, m, r_luc(t), 0.15 * math.sin(t * 3), hinh)
    tang.draw = ve
    sim.at(R.T_TU0, lambda s: s.add(tang))

    def hut(s, x):                                               # đá từ mặt đất bay lên nhập vào tảng
        t = s.t
        p0 = fx.ME + np.array([rng.uniform(-110, 70), rng.uniform(-6, 4)])
        q = fx.P(p0.copy(), (0, 0), 0.38, group=fx.FRONT, p0=p0)

        def upd(q, dt, s2):
            f = q.age / q.life
            m = T.diem(tt(s2.t), "mieng")
            q.pos = q.p0 + (m - q.p0) * f ** 1.5 + np.array([0.0, -40.0 * math.sin(math.pi * f)]) - q.vel * dt
        q.upd = upd
        sz = rng.uniform(4, 8)
        pts = [(sz * math.cos(a), sz * math.sin(a)) for a in (0.2, 1.7, 3.0, 4.4, 5.6)]
        q.draw = lambda q, k: ve_khoi(fx.FRONT, 45, q.pos, _rot(pts, q.age * 6), DA[rng.randint(3)], 1.8)
        s.add(q)
        if rng.uniform() < 0.4:
            bui(s, p0, vel=np.array([rng.uniform(-30, 30), -40.0]), r0=6, r1=14, life=0.45, group=fx.BACK)
    sim.every(R.T_TU0 + 0.05, R.T_TU1, 30, hut)
    for tn in (R.T_NEN1, R.T_NEN2):                              # hai nhịp nện gồng
        sim.at(tn, lambda s: (vong_dat(s, fx.ME + np.array([-20.0, 2.0]), 90), s.shake(0.18),
                              [dam_da(s, T.diem(tt(s.t), "mieng") + rng.uniform(-30, 30, 2), np.array([rng.uniform(-80, 80), 40.0]), 4.0,
                                      ground=fx.ME[1] + 2) for _ in range(4)]))

    def nem(s):
        m = T.diem(tt(R.T_NEM), "mieng")

        def trung(q, s2):
            cham_no(s2, q.pos.copy(), 2.8)
            vong_dat(s2, fx.FOE + np.array([0, 2.0]), 130, 0.7)
            s2.flash = 0.45
            s2.shake(0.7)
            for i in range(7):                                   # mưa đá nhỏ
                s2.at(s2.t + 0.08 + 0.05 * i, lambda s3: tang_da(s3, FOE_C + np.array([rng.uniform(-60, 60), -260.0]),
                                                                FOE_C + np.array([rng.uniform(-50, 50), rng.uniform(0, 30)]), 0.28, r=6.0,
                                                                vong=10.0, on_hit=lambda q3, s4: cham_no(s4, q3.pos.copy(), 0.5)))
        p = fx.P(m.copy(), (0, 0), 0.42, group=fx.FRONT, a0=m.copy(), b0=FOE_C + np.array([0.0, 10.0]))

        def upd(q, dt, s2):
            f = q.age / q.life
            q.pos = q.a0 + (q.b0 - q.a0) * f + np.array([0.0, -90.0 * math.sin(math.pi * f)]) - q.vel * dt
            if rng.uniform() < 0.8:
                bui(s2, q.pos + rng.uniform(-r_max * 0.5, r_max * 0.5, 2), vel=np.array([rng.uniform(-30, 30), 10.0]), r0=8, r1=18, life=0.4)
        p.upd = upd
        p.draw = lambda q, k: ve_tang(fx.FRONT, 44, q.pos, r_max * (1 - 0.15 * k), -q.age * 4, hinh)
        p.on_death = trung
        s.add(p)
    sim.at(R.T_NEM, nem)


def quy_nui_attack(sim, T, fr):
    R = T.R
    for t, m in ((R.T_DAM1, 0.6), (R.T_DAM2, 0.6), (R.T_DAM3, 1.4)):
        sim.at(t, lambda s, m=m: cham_no(s, FOE_C + s.rng.uniform(-10, 10, 2), m))
    sim.at(R.T_DAM3, lambda s: vong_dat(s, fx.FOE + np.array([0, 2.0]), 80))


def _ev(T, clip, ten):
    """giờ các sự kiện tên ten của clip (rig có mốc giờ cục bộ trong lam_clip)."""
    return [float(e[0]) for e in T.clips[clip].ev if e[1] == ten]


def rong_cat_cast(sim, T, fr):
    R = T.R
    R.T_CHEM = tuple(_ev(T, "cast", k)[0] for k in ("chem1", "chem2", "chem3"))
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]
    for i, tc in enumerate(R.T_CHEM):
        def chem(s, tc=tc, i=i):
            m = T.diem(tt(tc), "mieng")
            luoi_cat(s, m, FOE_C + np.array([0.0, (i - 1) * 16.0]), 0.22, R=40 + 5 * i,
                     on_hit=lambda q, s2: cham_no(s2, q.pos.copy(), 0.9, mau_dam=lambda r: CAT[r.randint(3)]))
        sim.at(tc, chem)


def rong_cat_skill(sim, T, fr):
    R = T.R
    R.T_GONG0, R.T_NEN = _ev(T, "skill", "gong")[0], _ev(T, "skill", "nen")[0]
    R.T_COT = tuple(_ev(T, "skill", k)[0] for k in ("cot1", "cot2", "cot3"))
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]
    rng = sim.rng

    def hut(s, x):                                               # cát, đá vụn hút về vuốt
        m = T.diem(tt(s.t), "mieng")
        a = rng.uniform(0, 6.28)
        p0 = m + np.array([math.cos(a), math.sin(a) * 0.6]) * rng.uniform(50, 80)
        q = fx.P(p0, (0, 0), 0.3, group=fx.FRONT, p0=p0)

        def upd(q, dt, s2):
            q.pos = q.p0 + (T.diem(tt(s2.t), "mieng") - q.p0) * (q.age / q.life) ** 1.5 - q.vel * dt
        q.upd = upd
        sz = rng.uniform(2.5, 4.5)
        q.draw = lambda q, k: ve_khoi(fx.FRONT, 45, q.pos, [(sz * math.cos(t), sz * math.sin(t)) for t in (0.3, 1.9, 3.5, 5.0)],
                                      CAT[rng.randint(3)], 1.6)
        s.add(q)
    sim.every(R.T_GONG0, R.T_NEN - 0.1, 36, hut)

    def nen(s):
        vong_dat(s, fx.ME + np.array([-30.0, 2.0]), 100, 0.55)
        for d in (-1, 1):
            bui(s, fx.ME + np.array([-30.0 + d * 30, -4.0]), vel=np.array([d * 90.0, -30.0]), r0=10, r1=24)
        s.shake(0.3)
    sim.at(R.T_NEN, nen)
    vet_nut(sim, fx.ME + np.array([-60.0, 0.0]), fx.FOE + np.array([20.0, 2.0]), R.T_NEN, 0.18)
    dx = (-48.0, 46.0, 0.0)
    for i, tc in enumerate(R.T_COT):
        def cot(s, i=i):
            to = i == 2
            cot_da(s, fx.FOE + np.array([dx[i], 4.0 if not to else 2.0]), 30 if not to else 58, 70 if not to else 150,
                   giu=0.35 if not to else 0.55)
            s.shake(0.18 if not to else 0.55)
            if to:
                s.flash = 0.35
                cham_no(s, FOE_C + np.array([0.0, 10.0]), 2.2, mau_dam=lambda r: CAT[r.randint(3)])
                s.hero_fx["foe"] = {"tint": (255, 246, 214), "amt": 0.9, "decay": 5.0, "off": (0.0, -34.0), "sq": (1.0, 1.0)}
                s.at(s.t + 0.35, lambda s2: s2.hero_fx.get("foe", {}).update(off=(0.0, 0.0)))
        sim.at(tc, cot)


def rong_cat_attack(sim, T, fr):
    R = T.R
    R.T_ATK = _ev(T, "attack", "trung")[0]

    def chem(s):
        for i in range(3):
            q = fx.P(FOE_C + np.array([-8.0 + 9 * i, -6.0 + 7 * i]), (0, 0), 0.18, group=fx.FRONT)
            q.draw = lambda q, k: [fx.item(fx.FRONT, 61, "arcpx", 200 * 1000 + 70, (255, 246, 214, 5), q.pos, 30, 1.4, 0, 1 - k * k)]
            s.add(q)
        cham_no(s, FOE_C, 1.0, mau_dam=lambda r: CAT[r.randint(3)])
    sim.at(R.T_ATK, chem)


CONG_THUC = {"cong_da": {"cast": (cong_da_cast, "Chiêu mana: lắc mai, ba viên sỏi bay găm"),
                         "skill": (cong_da_skill, "Chiêu cuối: pha lê vọt lên, mưa pha lê"),
                         "attack": (cong_da_attack, "Đánh thường: lao húc")},
             "than_lan_cat": {"cast": (than_lan_cat_cast, "Chiêu mana: ba phiến đất nung bay găm rồi về"),
                              "skill": (than_lan_cat_skill, "Chiêu cuối: dậm chân, lốc cát trùm đối thủ"),
                              "attack": (than_lan_cat_attack, "Đánh thường: chồm đớp")},
             "thu_da": {"cast": (thu_da_cast, "Chiêu mana: há hàm tụ đá, phun tảng đá"),
                        "skill": (thu_da_skill, "Chiêu cuối: cuộn tròn lăn nện", True),
                        "attack": (thu_da_attack, "Đánh thường: giáng sừng")},
             "quy_nui": {"cast": (quy_nui_cast, "Chiêu mana: nện đất, sóng chấn"),
                         "skill": (quy_nui_skill, "Chiêu cuối: tụ tảng đá khổng lồ, bốn tay ném"),
                         "attack": (quy_nui_attack, "Đánh thường: liên hoàn ba đấm")},
             "rong_cat": {"cast": (rong_cat_cast, "Chiêu mana: ba lưỡi cát trăng khuyết"),
                          "skill": (rong_cat_skill, "Chiêu cuối: nện đất, cột sa thạch trồi ba nhịp"),
                          "attack": (rong_cat_attack, "Đánh thường: chém vuốt")}}


def trang():
    """trang xem mọi GIF đã có trong inbox/tho5_fx."""
    gifs = sorted(f for f in os.listdir(RA) if f.endswith(".gif"))
    the = "".join(f'<figure><img src="{g}"><figcaption>{g[:-4]}</figcaption></figure>' for g in gifs)
    open(os.path.join(RA, "xem.html"), "w", encoding="utf-8").write(
        "<!doctype html><meta charset=utf-8><title>Thổ: xem trước chiêu</title><style>body{font:15px sans-serif;margin:16px;background:#f4f1ea}"
        "figure{display:inline-block;margin:8px;background:#fff;padding:6px;border:1px solid #ddd}img{width:540px;display:block}</style>"
        "<h1>Đảo Thổ: xem trước chiêu (rig thật + VFX tạm bằng Python)</h1><p>Tướng mình dưới phải, đối thủ trên trái (như trong trận). "
        "VFX là bản xem trước, sẽ làm lại trong Unity.</p>" + the)
    print(os.path.join(RA, "xem.html"))


if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else "cong_da"
    chon = sys.argv[2] if len(sys.argv) > 2 else "all"
    T = Tuong(code)
    for clip, ct in CONG_THUC[code].items():
        if chon in ("all", clip):
            chay(T, clip, ct[0], f"{code}_{clip}", nhan=ct[1], lao=len(ct) > 2 and ct[2])
    trang()
