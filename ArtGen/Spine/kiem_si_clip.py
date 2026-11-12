# -*- coding: utf-8 -*-
"""Kiếm sĩ rừng (kiem_si): clip. Nền là chuyển động lấy mẫu của con gốc monster_3620 (thân, tay, kiếm, hai chân dùng lại), phần riêng viết
thêm: gió trên lá / tua / áo tơi / đuôi, trò riêng lúc đứng (bật chuôi kiếm), nhịp hai chân lúc chạy, cú lao của đòn và chiêu, ảo ảnh.

Người dùng 2026-11-12:
  attack  như skill_1 của họ: quật cả thanh kiếm còn trong vỏ (báng kiếm) vào đối thủ
  cast    như skill_2: cúi xuống GIỮ THẾ (trong lúc giữ lướt tới đối thủ), rút kiếm chém, tra kiếm
  skill   skill_4 + skill_4_1..4: rút hai kiếm → biến mất cực nhanh → BỐN ảo ảnh chém đối thủ từ nhiều góc → về chỗ cũ → tra kiếm;
          lúc tra kiếm "cạch" thì đối thủ bị chém liên tục từ các vết trước (sự kiện `vet`, việc của lớp VFX)
  idle, run, appear, die: tự làm
"""
import math
import os

import numpy as np
from PIL import Image

from quai import anh, hoat, khung, soi
from quai.khung import Dat, goc_mat
from quai.hoat import Clip
import kiem_si_rig as R

KG, S, IB, TENX, BO, B0, SLOT_HO = R.KG, R.S, R.IB, R.TENX, R.BO, R.B0, R.SLOT_HO
ZERO5 = (0.0, 0.0, 0.0, 1.0, 1.0)


def chuyen_dong():
    """{clip: (dài, {xương: mảng (số khung, 5) = lệch xoay độ, dời x, y (đơn vị rig mình), tỉ lệ x, y nhân})} so với dáng gốc của mình."""
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        res = {}
        for i, b in enumerate(IB):
            if b["name"] in BO:
                continue
            x0, y0, r0, sx0, sy0 = B0[i]
            Am = np.array([[F["l"][i][2] - r0, (F["l"][i][0] - x0) * KG, (F["l"][i][1] - y0) * KG, F["l"][i][3] / (sx0 or 1.0),
                            F["l"][i][4] / (sy0 or 1.0)] for F in fr])
            Am[:, 0] = np.degrees(np.unwrap(np.radians(Am[:, 0])))
            Am[:, 0] -= 360.0 * round(Am[0, 0] / 360.0)
            if np.abs(Am - np.array([0, 0, 0, 1, 1])).max() > 1e-4:
                res[b["name"]] = Am
        out[clip] = (float(v["dur"]), res)
    return out


def em(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ra(x, k=2.2):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** k


def vao(x, k=2.2):
    x = min(1.0, max(0.0, x))
    return x ** k


def moc(t, ks):
    """đường khoá: ks = [(t, v[, kiểu])]; kiểu của khoá áp cho đoạn KẾT THÚC ở khoá đó: em (mặc định), ra, vao, thang."""
    if t <= ks[0][0]:
        return float(ks[0][1])
    for a, b in zip(ks, ks[1:]):
        if t <= b[0]:
            u = (t - a[0]) / max(1e-9, b[0] - a[0])
            kieu = b[2] if len(b) > 2 else "em"
            u = {"em": em, "ra": ra, "vao": vao, "thang": lambda q: q}[kieu](u)
            return float(a[1] + (b[1] - a[1]) * u)
    return float(ks[-1][1])


def rung(t, t0, t1, hz=11.0):
    if t < t0 or t > t1:
        return 0.0
    return math.sin(2 * math.pi * hz * (t - t0)) * min(1.0, (t - t0) / 0.12) * min(1.0, (t1 - t) / 0.12)


def lam_clip(sk, info):
    CD = chuyen_dong()
    cao = info["cao"]
    kiem = info["kiem"]                                                   # [(slot của mình, slot của họ)]
    duoi, ao, vay = info["duoi"], info["ao"], info["vay"]
    mem = info["mem"]
    ds_than = list(info["thu_tu"])                                        # mọi slot thân (cả kiếm)
    CHAN = R.CHAN
    FRONT = (CHAN["t"],)
    la_mem = list(R.MEM)

    def nen(P, goc, tau, lap=False, w=1.0, bo=(), chi_lay=None):
        """dáng nền lấy từ clip của họ ở giây tau, trọng số w. bo: xương không lấy; chi_lay: chỉ lấy các xương này."""
        dur, Rr = CD[goc]
        x = (tau % dur if lap else min(max(tau, 0.0), dur)) * 30.0
        for b, arr in Rr.items():
            if b in bo or (chi_lay is not None and b not in chi_lay):
                continue
            n = len(arr)
            i0 = min(int(x), n - 1)
            i1 = min(i0 + 1, n - 1)
            f = x - i0
            v = arr[i0] * (1 - f) + arr[i1] * f
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]) * w)
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]) * w, float(v[2]) * w)
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, 1 + (float(v[3]) - 1) * w, 1 + (float(v[4]) - 1) * w)

    def kiem_hien(P, goc=None, tau=0.0):
        """bật tắt các slot kiếm theo đúng mẫu khung của họ (goc None: trạng thái nghỉ: cả hai kiếm trong vỏ)."""
        if goc is None:
            F = None
        else:
            fr = S[goc]["frames"]
            F = fr[min(len(fr) - 1, max(0, int(round(tau * 30.0))))]
        for t, sl in kiem:
            i = SLOT_HO.index(sl)
            if F is None:
                P.alpha[t] = 1.0 if R.I["slots"][i]["att"] else 0.0
            else:
                P.alpha[t] = 1.0 if F["n"][i] else 0.0

    def chan(P):
        """bàn chân bám cứng xương đích của họ (đã nằm trong dáng nền); đùi là lưới giãn nên không phải giải gì thêm."""
        return

    def gio(P, t, manh=1.0, chu_ky=2.4):
        """gió: lá mào, tua, áo tơi, đuôi, váy đung đưa lệch pha (lò xo chạy sau làm trễ thêm)."""
        for k, tn in enumerate(la_mem):
            n = R.MEM[tn][1]
            bien = (6.0 if tn.startswith("tua") else 3.5) * manh
            ph = k * 1.7
            for q in range(n):
                P.rot(f"x_{tn}_{q}", bien * (0.6 + 0.5 * q) * math.sin(2 * math.pi * t / chu_ky + ph - 0.7 * q))
        for q, b in enumerate(duoi):                                      # đuôi: sóng chậm lan từ gốc ra ngọn
            P.rot(b, manh * (1.2 + 0.9 * q) * math.sin(2 * math.pi * t / (chu_ky * 1.25) - 0.75 * q))
        for q, b in enumerate(ao):
            P.rot(b, manh * (1.6 + 1.2 * q) * math.sin(2 * math.pi * t / chu_ky + 0.9 - 0.8 * q))
        for q, b in enumerate(vay):
            P.rot(b, manh * (1.5 + 1.5 * q) * math.sin(2 * math.pi * t / chu_ky + 2.1 - 0.8 * q))

    TREO = [(f"x_{tn}_0", 1.0) for tn in la_mem if tn.startswith("tua")]
    REF = {b: goc_mat(sk.W0[b]) for b, _ in TREO}

    def sau(P, giu=1.0):
        """sau khi đặt dáng: áo tơi lá và bốn tua TREO theo trọng lực: gốc của chúng giữ hướng thế giới của dáng gốc (cộng phần đung đưa
        gio() đã đặt), không quay cứng theo ngực / tấm vai (không thì lúc thân ngửa ra áo tơi lật ra trước bụng, tua chĩa ngang)."""
        if giu <= 0:
            return
        for b, k in TREO:
            lac = P.t[b][2] if b in P.t else 0.0
            if b in P.t:
                P.t[b][2] = 0.0
            cur = goc_mat(sk.the_gioi(P)[b])
            d = ((REF[b] - cur + 180.0) % 360.0) - 180.0
            P.rot(b, d * k * giu + lac)

    def mo_het(P, a, bo=()):
        for sl in ds_than:
            if sl not in bo:
                P.alpha[sl] = a * P.alpha.get(sl, 1.0)

    # trục kiếm dài trong hệ xương bone47 (vỏ): hướng rút = từ mũi vỏ về miệng vỏ
    q0, q1, _, _ = R.truc_kiem("W_daoA_1")
    v_tg = (q1 - q0) / np.hypot(*(q1 - q0))
    Wv = sk.W0["bone47"][:2, :2]
    v_loc = np.linalg.solve(Wv, v_tg)
    v_loc = v_loc / np.hypot(*v_loc)                                       # hướng rút trong hệ bone47 (cha của bone51)

    def he_kiem(P, d):
        """bật chuôi: lưỡi + chuôi kiếm dài trượt ra khỏi vỏ một đoạn d (đơn vị rig mình), tay xa (đang nắm chuôi) đi theo."""
        if abs(d) < 1e-3:
            return
        W = sk.the_gioi(P)
        co = W["bone20"][:2, 2].copy()
        huong = W["bone47"][:2, :2] @ v_loc
        huong = huong / np.hypot(*huong)
        P.move("bone51", float(v_loc[0] * d), float(v_loc[1] * d))
        hoat.ik_hai_doan(sk, P, "bone18", "bone19", co + huong * d,
                         ngon=tuple(float(v) for v in np.linalg.solve(sk.W0["bone19"], np.r_[sk.W0["bone20"][:2, 2], 1.0])[:2]))

    # ---------------------------------------------------------------- idle: thế thủ của họ + gió + trò riêng: bật chuôi kiếm "cạch"
    I_DUR = CD["idle_01"][0]

    def idle(t, P):
        nen(P, "idle_01", t, True)
        gio(P, t, 1.0, 2.0)
        # 2,2–3,3 s: liếc sang đối thủ, ngón cái bật chuôi (lưỡi ló ra), giữ, rồi ấn vào "cạch"; đuôi quất một nhịp
        g = moc(t, [(2.15, 0), (2.4, 1, "ra"), (3.0, 1), (3.12, 0, "vao")])
        P.rot("bone7", 5.0 * g)
        P.rot("bone6", 2.0 * g)
        P.rot("bone5", -1.5 * g)
        he_kiem(P, 0.085 * cao * g)
        q_ = moc(t, [(3.08, 0), (3.2, 1, "ra"), (3.5, 0)])
        for i_, b in enumerate(duoi):
            P.rot(b, (2.0 + 1.5 * i_) * q_)
        sau(P)
        kiem_hien(P)

    # ---------------------------------------------------------------- walk: run_01 của họ, hai chân so le nửa nhịp
    W_GOC = CD["run_01"][0]
    W_DUR = 0.60

    def walk(t, P):
        tau = t / W_DUR * W_GOC
        nen(P, "run_01", tau, True, bo=FRONT)
        nen(P, "run_01", tau - W_GOC * 7.0 / 20.0, True, chi_lay=FRONT)   # chân trước trễ thêm cho so le nửa nhịp với chân sau
        gio(P, t, 0.8, W_DUR)
        P.rot("bone5", -3.0)
        sau(P)
        kiem_hien(P)

    def hit(t, P):
        nen(P, "hit_01", t)
        sau(P)
        kiem_hien(P)

    # ---------------------------------------------------------------- attack: skill_1 của họ (quật cả kiếm còn trong vỏ) + lao tới
    A_MOC = [(0.0, 0.0), (0.40, 0.60, "thang"), (0.50, 0.72, "thang"), (0.74, 1.05, "thang"), (1.20, CD["skill_1"][0], "thang")]
    A_DUR = A_MOC[-1][0]
    A_TRUNG = 0.50
    A_XA = 0.55 * cao

    def attack(t, P):
        nen(P, "skill_1", moc(t, A_MOC))
        x = moc(t, [(0.0, 0), (0.30, -0.06 * cao), (A_TRUNG, A_XA, "vao"), (A_TRUNG + 0.24, A_XA), (A_DUR - 0.06, 0)])
        P.move("move", x, 0.0)
        gio(P, t, 0.6, 1.2)
        sau(P)
        kiem_hien(P, "skill_1", moc(t, A_MOC))

    # ---------------------------------------------------------------- cast: skill_2 của họ: cúi GIỮ THẾ (lướt tới), rút chém, bổ xuống, tra kiếm
    C_CUI, C_GIU, C_GOC_GIU = 0.30, 0.86, 0.63                            # cúi xong; hết giữ thế (giờ của mình); giờ hết giữ trong clip của họ
    C_MOC = [(0.0, 0.0), (C_CUI, 0.42, "thang"), (C_GIU, C_GOC_GIU, "thang"), (C_GIU + CD["skill_2"][0] - C_GOC_GIU, CD["skill_2"][0], "thang")]
    C_DUR = C_MOC[-1][0]
    C_TRUNG = C_GIU + (0.80 - C_GOC_GIU)                                   # nhát rút kiếm chém vọt lên
    C_CHEM2 = C_GIU + (1.53 - C_GOC_GIU)                                   # nhát bổ xuống
    C_XA = 0.62 * cao

    def cast(t, P):
        tau = moc(t, C_MOC)
        nen(P, "skill_2", tau)
        x = moc(t, [(C_CUI - 0.06, 0), (C_GIU, C_XA, "vao"), (C_CHEM2 + 0.22, C_XA), (C_DUR - 0.10, 0)])
        P.move("move", x, 0.0)
        r = rung(t, C_CUI, C_GIU, 14.0) * moc(t, [(C_CUI, 0.3), (C_GIU, 1.0, "thang")])     # gồng lúc giữ thế
        P.rot("bone5", 0.7 * r)
        P.rot("bone7", -0.9 * r)
        gio(P, t, 0.6 + 1.2 * moc(t, [(C_CUI, 0), (C_GIU, 1), (C_TRUNG + 0.1, 1.6), (C_DUR - 0.3, 0.3)]), 0.9)
        sau(P)
        if t >= C_DUR - 0.04:
            kiem_hien(P)
        else:
            kiem_hien(P, "skill_2", tau)

    # ---------------------------------------------------------------- skill: rút hai kiếm → biến mất → bốn ảo ảnh chém → về chỗ → tra kiếm
    K_RUT, K_BIEN, K_HIEN = 0.90, 1.04, 2.14                              # rút xong hai kiếm; biến mất hẳn; hiện lại
    G_RUT, G_HIEN = 1.06, 2.20                                            # giờ tương ứng trong skill_4 của họ
    K_MOC = [(0.0, 0.0), (K_RUT, G_RUT, "thang"), (K_BIEN, 1.30, "thang"), (K_HIEN - 0.001, 1.30, "thang"), (K_HIEN, G_HIEN, "thang"),
             (K_HIEN + CD["skill_4"][0] - G_HIEN, CD["skill_4"][0], "thang")]
    K_DUR = K_MOC[-1][0]
    K_DONG = K_HIEN + (2.70 - G_HIEN)                                      # "cạch": chuôi chạm miệng vỏ (thân họ nhún ở 2,70 s)
    AO = [dict(ten="a", goc="skill_4_1", khung=9, t0=1.10, dau=(-1.25, 0.0), cuoi=(1.25, 0.0)),            # lướt ngang từ trái sang phải
          dict(ten="b", goc="skill_4_3", khung=14, t0=1.34, dau=(-0.85, 1.05), cuoi=(0.85, -0.55)),        # chéo từ trên trái xuống
          dict(ten="c", goc="skill_4_2", khung=9, t0=1.58, dau=(0.05, 1.35), cuoi=(0.05, -0.45)),          # bổ thẳng từ trên xuống
          dict(ten="d", goc="skill_4_4", khung=14, t0=1.80, dau=(-0.95, -0.55), cuoi=(0.95, 1.05))]        # chéo từ dưới trái lên
    AO_DAI = 0.26                                                          # mỗi ảo ảnh hiện chừng này giây

    def dang_ao(g):
        """dáng của mình ở khung chém của clip ảo ảnh (thân đứng tại chỗ)."""
        P = khung.Pose()
        nen(P, g["goc"], g["khung"] / 30.0, bo=("bone3",))
        dur, Rr = CD[g["goc"]]
        if "bone3" in Rr:
            P.rot("bone3", float(Rr["bone3"][g["khung"]][0]))
        sau(P)
        kiem_hien(P, g["goc"], g["khung"] / 30.0)
        return P

    # ảnh ảo ảnh: chụp chính rig ở dáng chém, nhuộm lục, thu nhỏ; đặt trên xương ao_<k> (con của far)
    ve = soi.Ve(sk)
    far = sk.W0["far"][:2, 2].copy()
    TI_AO = 0.50                                                           # px ảnh ảo ảnh cho mỗi đơn vị rig
    for g in AO:
        P = dang_ao(g)
        Bx = ve.bao(P)
        im = ve.ve(P, Bx, TI_AO, bg=None, ss=2).convert("RGBA")
        a_ = np.asarray(im).astype(np.float32)
        L = a_[..., :3] @ np.array([0.30, 0.59, 0.11], np.float32)
        nhuom = np.stack([L * 0.30 + 20.0, L * 0.62 + 96.0, L * 0.46 + 62.0], -1)          # lục ngọc, giữ nét đậm nhạt
        out = np.dstack([np.clip(nhuom, 0, 255), a_[..., 3]]).astype(np.uint8)
        im = anh.loang_mau(Image.fromarray(out, "RGBA"))
        ten = "ao_" + g["ten"]
        sk.anh(ten, im)
        sk.xuong(ten, "far", far[0], far[1], the_gioi=True)
        sk.slot(ten, ten, ten, an=True)
        tam = np.array([(Bx[0] + Bx[2]) / 2, (Bx[1] + Bx[3]) / 2])        # tâm khung bao dáng chém
        g["lech"] = tam - np.array([0.0, 0.42 * cao])                      # so với tâm thân lúc đứng
        sk.manh(ten, ten, Dat(far[0], far[1], neo=(0.5, 0.5), ti=1.0 / TI_AO))
        g["huong"] = math.degrees(math.atan2(g["cuoi"][1] - g["dau"][1], g["cuoi"][0] - g["dau"][0]))
        sk.xuong("vet_" + g["ten"], "far", far[0], far[1], g["huong"], the_gioi=True)      # chỗ và hướng vết chém (VFX bám)
    AO_SLOT = tuple("ao_" + g["ten"] for g in AO)

    def an_ao(P):
        for sl in AO_SLOT:
            P.alpha[sl] = 0.0

    def skill(t, P):
        tau = moc(t, K_MOC)
        nen(P, "skill_4", tau)
        gio(P, t, 0.7, 1.0)
        sau(P)
        if t >= K_DUR - 0.04:
            kiem_hien(P)
        elif t < K_BIEN or t >= K_HIEN:
            kiem_hien(P, "skill_4", tau)
        else:
            kiem_hien(P, "skill_4", 1.30)
        # biến mất: kéo vệt về phía trước rồi tan; hiện lại: từ phía trước rút về, đậm dần
        a = moc(t, [(K_RUT + 0.04, 1), (K_BIEN, 0, "vao"), (K_HIEN, 0), (K_HIEN + 0.10, 1, "ra")])
        keo = moc(t, [(K_RUT, 0), (K_BIEN, 1, "vao")]) if t < K_BIEN + 0.01 else moc(t, [(K_HIEN, 1), (K_HIEN + 0.12, 0, "ra")])
        if K_RUT <= t <= K_HIEN + 0.13:
            P.move("move", 0.55 * cao * keo, 0.0)
            P.scale("move", 1 + 0.55 * keo, 1 - 0.16 * keo)
        mo_het(P, a)
        # bốn ảo ảnh: mỗi cái lướt xuyên qua đối thủ theo một hướng, nhanh dần, nhạt dần
        for g in AO:
            u = (t - g["t0"]) / AO_DAI
            sl = "ao_" + g["ten"]
            if u < 0 or u > 1:
                P.alpha[sl] = 0.0
                continue
            s_ = vao(u, 1.7)
            d0, d1 = np.array(g["dau"]) * cao, np.array(g["cuoi"]) * cao
            p = d0 + (d1 - d0) * s_ + g["lech"] * 0.0
            P.move(sl, float(p[0]), float(p[1]))
            P.alpha[sl] = 0.78 * moc(u, [(0, 0), (0.12, 1), (0.55, 1), (1.0, 0, "thang")])
            c, s2 = math.cos(math.radians(g["huong"])), math.sin(math.radians(g["huong"]))
            k = 1 + 0.35 * s_                                              # kéo dài theo hướng lướt
            P.scale(sl, 1 + (k - 1) * abs(c), 1 + (k - 1) * abs(s2))

    K_EV = ([(0.42, "rut", ""), (K_RUT + 0.04, "bien", "")] + [(g["t0"] + 0.10, "chem", g["ten"]) for g in AO] + [(K_HIEN, "hien", ""),
            (K_DONG, "trung", "dong_kiem")] + [(K_DONG + 0.05 + 0.07 * i, "vet", g["ten"]) for i, g in enumerate(AO + AO[:2])])

    # ---------------------------------------------------------------- appear: rơi từ tán cây xuống, đáp thụp, đứng dậy vào thế, bật chuôi "cạch"
    P_DUR = 1.75
    P_DAP = 0.34                                                           # chạm đất

    def appear(t, P):
        nen(P, "idle_01", 0.0, True)
        y = moc(t, [(0, 0.85 * cao), (P_DAP, 0.0, "vao")])
        P.move("move", -0.10 * cao * (1 - vao(min(1.0, t / P_DAP), 1.3)), y)
        thup = moc(t, [(P_DAP - 0.02, 0), (P_DAP + 0.07, 1, "ra"), (0.78, 0.86), (1.12, 0)])      # thụp sâu khi chạm đất, giữ thấp, rồi đứng dậy
        co = moc(t, [(0, 0.55), (P_DAP - 0.04, 0.35), (P_DAP + 0.05, 0)])                          # lúc rơi: co người
        P.move("bone3", 0.0, -(0.16 * thup + 0.05 * co) * cao)
        P.rot("bone3", -6.0 * thup + 5.0 * co)
        P.rot("bone5", -9.0 * thup - 4.0 * co)
        P.rot("bone7", 9.0 * thup + 8.0 * co)
        P.rot("bone6", 3.0 * thup)
        for q, b in enumerate(duoi):                                       # đuôi và áo tơi bị hất lên lúc rơi, quật xuống lúc đáp
            P.rot(b, (5.0 + 3.0 * q) * co - (3.0 + 2.5 * q) * moc(t, [(P_DAP, 0), (P_DAP + 0.12, 1, "ra"), (0.9, 0)]))
        for q, b in enumerate(ao):
            P.rot(b, -(10.0 + 8.0 * q) * co + (4.0 + 3.0 * q) * moc(t, [(P_DAP, 0), (P_DAP + 0.14, 1, "ra"), (0.95, 0)]))
        g = moc(t, [(1.14, 0), (1.3, 1, "ra"), (1.46, 1), (1.56, 0, "vao")])                       # vào thế: bật chuôi rồi ấn "cạch"
        he_kiem(P, 0.085 * cao * g)
        P.rot("bone7", 4.0 * g)
        gio(P, t, 1.0 + 1.5 * moc(t, [(0, 1), (P_DAP + 0.1, 1), (1.0, 0)]), 0.7)
        sau(P)
        kiem_hien(P)
        mo_het(P, moc(t, [(0, 0), (0.07, 1)]))
        an_ao(P)

    # ---------------------------------------------------------------- die: ngã của họ rồi mờ dần
    D_DUR = CD["die_01"][0]
    TAN = 0.55

    def die(t, P):
        nen(P, "die_01", t)
        sau(P, 1.0 - moc(t, [(0.0, 0), (0.25, 1)]))
        kiem_hien(P, "die_01", min(t, D_DUR))
        mo_het(P, float(np.clip(1.0 - (t - D_DUR - 0.15) / (TAN - 0.2), 0.0, 1.0)))
        an_ao(P)

    def boc(fn):
        def f(t, P):
            fn(t, P)
            an_ao(P)
        return f

    for e, m in (("trung", "khung đòn trúng (kiếm quật tới / nhát rút kiếm / chuôi chạm miệng vỏ ở chiêu cuối)"),
                 ("chem2", "nhát bổ xuống thứ hai của chiêu mana"), ("rut", "rút hai kiếm"), ("bien", "biến mất (VFX vệt lá, bụi)"),
                 ("chem", "một ảo ảnh lướt qua chém (chuỗi kèm: a / b / c / d; chỗ và hướng: xương vet_<k>)"),
                 ("hien", "hiện lại ở chỗ cũ"), ("vet", "một vết chém cũ nổ lại trên đối thủ sau khi tra kiếm (chuỗi kèm: vết nào)"),
                 ("cham_dat", "chạm đất lúc ra sân (VFX bụi, lá; sân đấu rung màn ở sự kiện tên này)"), ("cach", "bật / ấn chuôi kiếm"), ("nga", "đổ sụp")):
        sk.su_kien(e, m)
    clips = [Clip("appear", P_DUR, appear, ev=[(P_DAP, "cham_dat", ""), (1.56, "cach", "")], mem=mem),
             Clip("idle", I_DUR, boc(idle), loop=True, ev=[(3.12, "cach", "")], mem=mem),
             Clip("walk", W_DUR, boc(walk), loop=True, mem=mem),
             Clip("attack", A_DUR, boc(attack), ev=[(A_TRUNG, "trung", "")], trung=A_TRUNG, mem=mem),
             Clip("cast", C_DUR, boc(cast), ev=[(C_TRUNG, "trung", ""), (C_CHEM2, "chem2", "")], trung=C_TRUNG, mem=mem),
             Clip("skill", K_DUR, skill, ev=K_EV, trung=K_DONG, mem=mem),
             Clip("hit", CD["hit_01"][0], boc(hit), mem=mem),
             Clip("die", D_DUR + TAN, die, ev=[(0.55, "nga", "")], mem=mem)]
    return clips, {}
