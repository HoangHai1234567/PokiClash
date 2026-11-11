# -*- coding: utf-8 -*-
"""Viết animation cho thư viện quai: hàm thời gian f(t, P) đặt dáng mỗi khung (P là khung.Pose: rot, move, scale, alpha, att),
nướng 30 khung/giây, chạy phần mềm (lò xo, dây mềm), khép vòng clip lặp, lọc khoá RDP từng kênh, ra timeline Spine 4.2.

    def f(t, P):
        P.rot("dau", 6 * hoat.song(t, 2.0))
        hoat.chuoi_song(P, ["duoi0", "duoi1", "duoi2", "duoi3"], t, 2.0, [3, 5, 7, 9])
    idle = hoat.Clip("idle", 2.0, f, loop=True, mem=[hoat.LoXo(["rau0", "rau1", "rau2"], k=[300, 220, 160])])
    attack = hoat.Clip("attack", 0.9, g, ev=[(0.45, "trung", "")], trung=0.45)
    frames = hoat.nuong(sk, idle)          # list Pose, khung i ở giây i/30 (khung cuối đúng giây dur)

Luật nhịp (skill-petclash 7.2, mo_xe_quai_nhieu_dau 6b): đầu dẫn thân theo (đốt về gốc trễ ~0,17 s), hai đốt kề ngược dấu, biên
độ lớn nhất giữa chuỗi; idle 2 cực trị mỗi đốt + điểm phá nhịp; ra đòn dáng → dáng, khung gãy, chạm 1 khung, giữ có trôi; gồng
bằng rung hai dáng (đổi mỗi 2 khung); trúng đòn không lấy đà, ngọn đỉnh ở 0,07 s, sóng chạy từ ngọn về gốc.
"""
import math

import numpy as np

from .khung import Pose, ZERO, goc_mat

FPS = 30
TOL = {"rotate": 0.15, "translate": 0.35, "scale": 0.0025, "alpha": 0.01}


# ---------------------------------------------------------------- đường cong
def ease(u, kind="io"):
    """io (êm hai đầu), out (bật nhanh rồi chậm), in (chậm rồi nhanh), back (vượt nhẹ rồi về), sin, hold (bậc), lin."""
    u = min(1.0, max(0.0, u))
    if kind == "io":
        return u * u * (3 - 2 * u)
    if kind == "io5":
        return u * u * u * (u * (6 * u - 15) + 10)
    if kind == "out":
        return 1 - (1 - u) ** 3
    if kind == "in":
        return u ** 3
    if kind == "back":
        c1, c3 = 1.70158, 2.70158
        return 1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2
    if kind == "sin":
        return 0.5 - 0.5 * math.cos(math.pi * u)
    if kind == "hold":
        return 0.0 if u < 1 else 1.0
    return u


class Track:
    """khoá (t, giá trị, kiểu êm của đoạn TỚI khoá đó); giá trị là số hoặc bộ số. Gọi tr(t) ra giá trị (numpy)."""

    def __init__(self, keys):
        self.k = [(float(k[0]), np.atleast_1d(np.array(k[1], float)), k[2] if len(k) > 2 else "io") for k in keys]

    def __call__(self, t):
        k = self.k
        if t <= k[0][0]:
            return k[0][1]
        for (t0, v0, _), (t1, v1, e) in zip(k[:-1], k[1:]):
            if t <= t1:
                return v0 + (v1 - v0) * ease((t - t0) / max(1e-9, t1 - t0), e)
        return k[-1][1]


def K(*keys):
    """K((0, 0), (0.3, -12, "io"), (0.42, 30, "out"), ...) -> Track."""
    return Track(keys)


def cv(t, keys):
    """giá trị số của khoá ở giây t: cv(t, [(0, 0), (0.3, 1, "out"), ...])."""
    return float(Track(keys)(t)[0])


def song(t, chu_ky, pha=0.0):
    """sin(2π t / chu_ky + pha). Clip lặp: chu_ky phải chia hết độ dài clip."""
    return math.sin(2 * math.pi * t / chu_ky + pha)


def lui(t, D):
    """giờ lùi cho dao động tuần hoàn trong clip KHÔNG lặp: dùng song(lui(t, D), ...) thì ở khung cuối (t = D) dao động trùng
    khung 0 của idle (cùng chu kỳ) nên nối về idle không giật (Hải Long)."""
    return t - D


def rung(t, t0, t1, moi=2, fps=FPS):
    """rung hai dáng: trong [t0, t1) trả +1 / -1 đổi nhau mỗi `moi` khung (2 khung ở 30 khung/giây = 15 lần/giây), ngoài trả 0."""
    if t < t0 or t >= t1:
        return 0.0
    return 1.0 if int(round((t - t0) * fps)) // moi % 2 == 0 else -1.0


def bao(t, t0, t1, vao=0.15, ra=0.15):
    """hệ số 0 → 1 → 0 cho đoạn [t0, t1] (vào, ra êm)."""
    return ease((t - t0) / max(1e-6, vao)) * (1 - ease((t - (t1 - ra)) / max(1e-6, ra)))


def chuoi_song(P, ten, t, chu_ky, bien_do, tre=0.17, nguoc_dau=False, ngon_dan=True, pha=0.0, bao_giua=False):
    """sóng lan dọc chuỗi (ten: gốc → ngọn). Mỗi đốt xoay bien_do[i]·sin(...) với trễ pha: ngon_dan=True thì đốt gần ngọn đạt cực
    trị trước, về gốc trễ thêm `tre` giây mỗi đốt (cổ: đầu dẫn thân theo; đuôi quẫy thì để ngon_dan=False: gốc dẫn ngọn theo).
    nguoc_dau: hai đốt kề ngược dấu (cổ uốn mạnh mà đầu gần như đứng yên). bao_giua: biên độ nhân sin(π (i+0.5)/n) (lớn nhất ở
    giữa chuỗi, nhỏ ở gốc và ngọn)."""
    n = len(ten)
    amp = np.broadcast_to(np.asarray(bien_do, float), (n,))
    for i, b in enumerate(ten):
        k = (n - 1 - i) if ngon_dan else i
        a = amp[i] * (math.sin(math.pi * (i + 0.5) / n) if bao_giua else 1.0)
        sg = (-1 if (nguoc_dau and i % 2) else 1)
        P.rot(b, sg * a * math.sin(2 * math.pi * (t - k * tre) / chu_ky + pha))


def ik_hai_doan(sk, P, dui, cang, dich, ngon=None, uon=None):
    """IK hai đoạn: xoay đùi, cẳng (cang là con trực tiếp của dui) cho ngọn cẳng chạm đích (thế giới rig), gối gập về phía
    đang gập (uon=+1/-1 để ép). ngon: điểm ngọn theo xương cẳng (mặc định (dài, 0)). Gọi CUỐI hàm đặt dáng (sau khi thân đã dời):
    bàn chân bám đất khi thân nhún, lao. Đích thường là chỗ bàn chân dáng gốc theo xương "move"."""
    W = sk.the_gioi(P)
    A, B = W[dui][:2, 2], W[cang][:2, 2]
    tip = ngon or (sk.bones[sk.bi[cang]]["length"] or 10.0, 0.0)
    C = (W[cang] @ np.array([tip[0], tip[1], 1.0]))[:2]
    L1, L2 = float(np.hypot(*(B - A))), float(np.hypot(*(C - B)))
    T = np.asarray(dich, float)
    D = T - A
    d = min(L1 + L2 - 1e-3, max(abs(L1 - L2) + 1e-3, float(np.hypot(*D))))
    a = math.atan2(D[1], D[0])
    al = math.acos(max(-1.0, min(1.0, (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d))))
    if uon is None:
        cr = (C - A)[0] * (B - A)[1] - (C - A)[1] * (B - A)[0]
        uon = 1.0 if cr >= 0 else -1.0
    phi1 = a + uon * al
    th1 = math.atan2(*(B - A)[::-1])
    par = sk.bones[sk.bi[dui]]["parent"]
    s1 = 1.0 if par is None or np.linalg.det(W[par][:2, :2]) > 0 else -1.0
    P.rot(dui, s1 * (((math.degrees(phi1 - th1)) + 180) % 360 - 180))
    sk.cap_nhat(W, [dui, cang], P)
    B2 = W[cang][:2, 2]
    C2 = (W[cang] @ np.array([tip[0], tip[1], 1.0]))[:2]
    Tc = A + d * np.array([math.cos(a), math.sin(a)])
    th2, phi2 = math.atan2(*(C2 - B2)[::-1]), math.atan2(*(Tc - B2)[::-1])
    s2 = 1.0 if np.linalg.det(W[dui][:2, :2]) > 0 else -1.0
    P.rot(cang, s2 * (((math.degrees(phi2 - th2)) + 180) % 360 - 180))


def an_hien(P, slot, t, khoang, mac_dinh=0.0):
    """slot hiện (độ đậm 1) trong các khoảng [(t0, t1), ...], ngoài là mac_dinh (mí mắt chớp, nhắm)."""
    P.alpha[slot] = 1.0 if any(t0 <= t < t1 for t0, t1 in khoang) else mac_dinh


# ---------------------------------------------------------------- clip
class Clip:
    """một clip: ten (tên game đọc: appear, idle, attack, cast, skill, hit, die, evolve, aura), dur (giây), fn(t, P) đặt dáng,
    loop (lặp liền), ev [(t, tên, chuỗi)] sự kiện, trung (giây khung trúng/nhả cho game.hitTimes; mặc định lấy sự kiện
    trung/can/phun/gam đầu tiên), mem [LoXo | DayMem] phần mềm chạy sau fn, post(t, P) hậu kỳ sau lò xo (tiến hóa khớp idle dạng
    sau)."""

    def __init__(self, ten, dur, fn, loop=False, ev=None, trung=None, mem=None, post=None, mo_ta=""):
        self.ten, self.dur, self.fn, self.loop = ten, float(dur), fn, loop
        self.ev = list(ev or [])
        self.trung, self.mem, self.post, self.mo_ta = trung, list(mem or []), post, mo_ta

    def gio_trung(self):
        if self.trung is not None:
            return float(self.trung)
        for t, n, _ in sorted(self.ev):
            if n in ("trung", "can", "phun", "nha", "gam", "ban"):
                return float(t)
        return None


def nuong(sk, clip, fps=FPS):
    """nướng clip: list Pose, khung i ở giây min(i/fps, dur), khung cuối đúng giây dur. Clip lặp: khung cuối = khung 0."""
    n = int(round(clip.dur * fps)) + 1
    ts = [min(clip.dur, i / fps) for i in range(n)]
    frames = []
    for t in ts:
        P = Pose()
        clip.fn(t, P)
        frames.append(P)
    for m in clip.mem:
        m.chay(sk, frames, ts, clip.loop, fps)
    if clip.post:
        for t, P in zip(ts, frames):
            clip.post(t, P)
    if clip.loop:
        dong_vong(frames)
    return frames


def dong_vong(frames, m=6):
    """khép vòng clip lặp: m khung trước khung cuối hoà dần về khung 0 (phần mềm sau lò xo lệch vài độ), khung cuối = khung 0."""
    n = len(frames)
    m = min(m, max(0, n // 3))
    a0 = frames[0]
    for j in range(m):
        w = (j + 1) / (m + 1)
        P = frames[n - 1 - m + j]
        for b in set(P.t) | set(a0.t):
            pa, pb = P._g(b), a0.t.get(b, list(ZERO))
            for q in range(5):
                pa[q] = pa[q] * (1 - w) + pb[q] * w
    frames[-1] = a0.copy()


def khop_cuoi(frames, dich, giay=0.25, fps=FPS):
    """hoà dần `giay` cuối clip về tư thế dich (thường là khung 0 idle): phần động học đã trùng idle nhờ giờ lùi, cái còn lệch là
    phần mềm (lò xo, dây) chưa lắng; hoà đi để nối về idle không giật. Sửa tại chỗ."""
    n = len(frames)
    m = max(1, min(n - 1, int(round(giay * fps))))
    for j in range(1, m + 1):
        P = frames[n - 1 - m + j]
        w = ease(j / m)
        for b in set(P.t) | set(dich.t):
            pa, pb = P._g(b), dich.t.get(b, list(ZERO))
            for q in range(5):
                pa[q] = pa[q] * (1 - w) + pb[q] * w
        for s in set(dich.alpha):
            P.alpha[s] = P.alpha.get(s, dich.alpha[s]) * (1 - w) + dich.alpha[s] * w
        if j == m:
            P.att.update(dich.att)


def phu_aura(frames, aura, sk=None):
    """ghép clip lặp aura lên clip chính cùng giây như runtime (AtomikPose.Overlay): xoay, dời cộng; tỉ lệ nhân; độ đậm nhân với độ
    đậm của clip chính (slot không khoá thì lấy độ đậm mặc định của slot: truyền sk); hình theo aura. aura: list Pose (lặp theo
    chỉ số khung)."""
    if not aura:
        return frames
    a0 = {s["name"]: s["alpha"] for s in sk.slots} if sk is not None else {}
    n = len(aura) - 1 if len(aura) > 1 else 1
    out = []
    for i, P in enumerate(frames):
        Q = P.copy()
        A = aura[i % n]
        for b, v in A.t.items():
            g = Q._g(b)
            g[0] += v[0]
            g[1] += v[1]
            g[2] += v[2]
            g[3] *= v[3]
            g[4] *= v[4]
        for s, a in A.alpha.items():
            Q.alpha[s] = Q.alpha.get(s, a0.get(s, 1.0)) * a
        for s, a in A.att.items():
            Q.att[s] = a
        out.append(Q)
    return out


# ---------------------------------------------------------------- phần mềm
class LoXo:
    """chuỗi mềm đuổi theo dáng động học (như longrig.Springs, Thủy Long / Thanh Long): mỗi khớp là điểm nối lò xo tới vị trí
    động học, giảm chấn damp, giữ độ dài đốt; góc lệch mỗi đốt chặn trong maxang độ. k: độ cứng từng đốt (380 → 180 là bờm vừa;
    nhỏ hơn mềm hơn), ngon: điểm ngọn theo xương cuối (mặc định dài xương cuối trên trục x)."""

    def __init__(self, xuong, k=(300, 240, 190, 150), damp=0.55, maxang=12.0, ngon=None, sub=4):
        self.bones, self.k, self.damp, self.maxang, self.tip, self.sub = list(xuong), list(k), damp, maxang, ngon, sub

    def _targets(self, sk, W):
        pts = [W[b][:2, 2].copy() for b in self.bones]
        last = self.bones[-1]
        tip = self.tip or (sk.bones[sk.bi[last]]["length"] or 20.0, 0.0)
        pts.append((W[last] @ np.array([tip[0], tip[1], 1.0]))[:2])
        return pts

    def chay(self, sk, frames, ts, loop, fps):
        dt = 1.0 / fps
        bones = [b for b in self.bones if b in sk.bi]
        if len(bones) != len(self.bones):
            return
        st = {}

        def step(P, record):
            W = sk.the_gioi(P)
            tg = self._targets(sk, W)
            if "p" not in st:
                st["p"] = [p.copy() for p in tg]
                st["v"] = [np.zeros(2) for _ in tg]
            p, v = st["p"], st["v"]
            p[0] = tg[0]
            for _ in range(self.sub):
                h = dt / self.sub
                for i in range(1, len(p)):
                    k = self.k[min(i - 1, len(self.k) - 1)]
                    acc = k * (tg[i] - p[i]) - self.damp * 2 * math.sqrt(k) * v[i]
                    v[i] = v[i] + acc * h
                    p[i] = p[i] + v[i] * h
                for i in range(1, len(p)):
                    L = np.linalg.norm(tg[i] - tg[i - 1])
                    dv = p[i] - p[i - 1]
                    nn = np.linalg.norm(dv)
                    if nn > 1e-9:
                        p[i] = p[i - 1] + dv / nn * L
            if not record:
                return
            for i, b in enumerate(bones):
                at = math.degrees(math.atan2(*(tg[i + 1] - tg[i])[::-1]))
                asim = math.degrees(math.atan2(*(p[i + 1] - p[i])[::-1]))
                d = (asim - at + 180) % 360 - 180
                if self.maxang:
                    d = max(-self.maxang, min(self.maxang, d))
                sgn = 1.0 if np.linalg.det(W[b][:2, :2]) > 0 else -1.0
                P.rot(b, d * sgn)
                sk.cap_nhat(W, bones[i:], P)
                tg = self._targets(sk, W)

        if loop:
            for _ in range(2):
                for P in frames[:-1]:
                    step(P.copy(), False)
        else:
            for _ in range(fps):
                step(frames[0].copy(), False)
        for P in frames:
            step(P, True)


class DayMem:
    """dây mềm (rope của Hải Long, râu, lưỡi, dây buộc): Verlet 'đốt sau đi theo đốt trước', mỗi đốt có lò xo về góc động học so
    với đốt trước (cứng k0 ở gốc → k1 ở ngọn; tần số riêng ≈ √k·fps·sub rad/s), giảm chấn zeta, khớp chặn góc mềm bằng tanh (lim
    độ, gốc → ngọn), lực ngoài luc(giây, đốt) -> gia tốc thế giới (gió hình sin cho râu, trọng lực cho lưỡi: độ võng mỗi đốt ≈
    g·dt²/k). Cú giật của đầu chạy dọc sợi thành sóng. Ghi góc lệch so với dáng động học vào từng đốt."""

    def __init__(self, xuong, k0=0.20, k1=0.035, zeta=0.5, luc=None, lim=(20.0, 32.0), sub=4):
        self.bones, self.k0, self.k1, self.zeta, self.luc, self.lim, self.sub = list(xuong), k0, k1, zeta, luc, lim, sub

    def chay(self, sk, frames, ts, loop, fps):
        bones = self.bones
        if any(b not in sk.bi for b in bones):
            return
        N = len(bones)
        par = sk.bones[sk.bi[bones[0]]]["parent"]
        ks = np.linspace(self.k0, self.k1, N)
        keep = 1 - 2 * self.zeta * np.sqrt(ks)
        lims = np.linspace(self.lim[0], self.lim[1], N)
        dt = 1.0 / fps / self.sub
        # dáng động học từng khung: gốc, góc cha, góc nghỉ từng đốt so với đốt trước, dài đốt
        anc, ang0, rest, segs, sgn = [], [], [], [], []
        for P in frames:
            W = sk.the_gioi(P)
            Wp = W[par] if par else np.eye(3)
            th = [goc_mat(W[b]) for b in bones]
            a0 = goc_mat(Wp)
            anc.append(W[bones[0]][:2, 2].copy())
            ang0.append(a0)
            rest.append([((th[0] - a0) + 180) % 360 - 180] + [((th[i] - th[i - 1]) + 180) % 360 - 180 for i in range(1, N)])
            sg = []
            for i, b in enumerate(bones):
                if i + 1 < N:
                    sg.append(float(np.hypot(*(W[bones[i + 1]][:2, 2] - W[b][:2, 2]))))
                else:
                    ln = sk.bones[sk.bi[b]]["length"]
                    sg.append(float(np.hypot(*W[b][:2, 0])) * ln if ln else (sg[-1] if sg else 20.0))
            segs.append(sg)
            sgn.append(1.0 if np.linalg.det(Wp[:2, :2]) > 0 else -1.0)
        anc, ang0, rest, segs = np.array(anc), np.array(ang0), np.array(rest), np.array(segs)
        n = len(frames)

        def pts_of(a, ang, rs, sg):
            pts, th = [np.array(a, float)], ang
            for i in range(N):
                th += rs[i]
                pts.append(pts[-1] + sg[i] * np.array([math.cos(math.radians(th)), math.sin(math.radians(th))]))
            return np.array(pts)

        st = {"p": pts_of(anc[0], ang0[0], rest[0], segs[0])}
        st["prev"] = st["p"].copy()

        def step(a, ang, rs, sg, tsec):
            pp, prev = st["p"], st["prev"]
            new = pp.copy()
            new[0] = a
            thp = ang
            for i in range(1, N + 1):
                q = pp[i] + (pp[i] - prev[i]) * keep[i - 1]
                if self.luc is not None:
                    q = q + np.asarray(self.luc(tsec, i - 1), float) * dt * dt
                base = thp + rs[i - 1]
                r = math.radians(base)
                tgt = new[i - 1] + sg[i - 1] * np.array([math.cos(r), math.sin(r)])
                q = q + (tgt - q) * ks[i - 1]
                d = q - new[i - 1]
                o = ((math.degrees(math.atan2(d[1], d[0])) - base) + 180) % 360 - 180
                thp = base + lims[i - 1] * math.tanh(o / lims[i - 1])
                new[i] = new[i - 1] + sg[i - 1] * np.array([math.cos(math.radians(thp)), math.sin(math.radians(thp))])
            st["prev"], st["p"] = pp, new

        def frame(f, f0):
            for k in range(1, self.sub + 1):
                u = k / self.sub
                step(anc[f0] + (anc[f] - anc[f0]) * u, ang0[f0] + (((ang0[f] - ang0[f0]) + 180) % 360 - 180) * u,
                     rest[f0] + (rest[f] - rest[f0]) * u, segs[f0] + (segs[f] - segs[f0]) * u, ts[f0] + (ts[f] - ts[f0]) * u)

        if loop:
            for _ in range(2):
                for f in range(1, n):
                    frame(f, f - 1)
        else:
            for _ in range(12):
                frame(0, 0)
        for f in range(n):
            if f:
                frame(f, f - 1)
            pts = st["p"]
            thp = ang0[f]
            for i in range(N):
                d = pts[i + 1] - pts[i]
                a = math.degrees(math.atan2(d[1], d[0]))
                off = ((a - thp - rest[f][i]) + 180) % 360 - 180
                frames[f].rot(bones[i], off * sgn[f])
                thp = a


# ---------------------------------------------------------------- khoá
def rdp(ts, vs, tol):
    """lược khoá Ramer-Douglas-Peucker trên chuỗi (t, vector): trả chỉ số khoá giữ lại (luôn giữ hai đầu)."""
    vs = np.asarray(vs, float)
    if vs.ndim == 1:
        vs = vs[:, None]
    ts = np.asarray(ts, float)
    keep = np.zeros(len(ts), bool)
    keep[0] = keep[-1] = True
    st = [(0, len(ts) - 1)]
    while st:
        a, b = st.pop()
        if b <= a + 1:
            continue
        t = (ts[a + 1:b] - ts[a]) / max(1e-9, ts[b] - ts[a])
        lin = vs[a] + (vs[b] - vs[a]) * t[:, None]
        err = np.abs(vs[a + 1:b] - lin).max(axis=1)
        i = int(err.argmax())
        if err[i] > tol:
            keep[a + 1 + i] = True
            st += [(a, a + 1 + i), (a + 1 + i, b)]
    return np.flatnonzero(keep)


_MISS = object()


def thanh_khoa(sk, clip, frames, fps=FPS, tol=None):
    """khung đã nướng -> animation JSON Spine 4.2 (khoá thẳng giữa các khoá giữ lại) và số khoá. Kênh nào không đổi thì bỏ.
    Luôn có khoá dời root ở 0 và dur để độ dài clip đúng (atomik lấy dur = giờ khoá cuối)."""
    tol = dict(TOL, **(tol or {}))
    n = len(frames)
    ts = np.array([min(clip.dur, i / fps) for i in range(n)])
    r2 = lambda v: round(float(v), 2)  # noqa: E731
    A = {"bones": {}, "slots": {}}
    nk = 0
    used = set()
    for P in frames:
        used |= set(P.t)
    for b in [q["name"] for q in sk.bones if q["name"] in used]:
        arr = np.array([P.t.get(b, ZERO) for P in frames], float)
        o = {}
        rot = arr[:, 2]
        if np.abs(rot).max() > 0.02:
            idx = rdp(ts, rot, tol["rotate"])
            o["rotate"] = [{"time": round(float(ts[i]), 4), "value": r2(rot[i])} for i in idx]
        tr = arr[:, 0:2]
        if np.abs(tr).max() > 0.02:
            idx = rdp(ts, tr, tol["translate"])
            o["translate"] = [{"time": round(float(ts[i]), 4), "x": r2(tr[i, 0]), "y": r2(tr[i, 1])} for i in idx]
        sc = arr[:, 3:5]
        if np.abs(sc - 1).max() > 0.001:
            idx = rdp(ts, sc, tol["scale"])
            o["scale"] = [{"time": round(float(ts[i]), 4), "x": round(float(sc[i, 0]), 4), "y": round(float(sc[i, 1]), 4)} for i in idx]
        for kind in o.values():
            nk += len(kind)
            for k in kind:
                if k["time"] == 0:
                    del k["time"]
        if o:
            A["bones"][b] = o
    for s in sk.slots:
        sn = s["name"]
        a0 = s["alpha"]
        vals = np.array([P.alpha.get(sn, a0) for P in frames], float)
        so = {}
        if np.abs(vals - a0).max() > 0.002:
            idx = rdp(ts, vals, tol["alpha"])
            so["alpha"] = [{"time": round(float(ts[i]), 4), "value": round(float(vals[i]), 3)} for i in idx]
        atts = [P.att.get(sn, _MISS) for P in frames]
        if any(x is not _MISS for x in atts):
            seq = [s["att"] if x is _MISS else x for x in atts]
            ks = [{"time": 0.0, "name": seq[0]}]
            for i in range(1, n):
                if seq[i] != seq[i - 1]:
                    ks.append({"time": round(float(ts[i]), 4), "name": seq[i]})
            if len(ks) > 1 or seq[0] != s["att"]:
                so["attachment"] = ks
        for kind in so.values():
            nk += len(kind)
            for k in kind:
                if k.get("time") == 0:
                    del k["time"]
        if so:
            A["slots"][sn] = so
    root = sk.bones[0]["name"]
    rt = A["bones"].setdefault(root, {})
    if "translate" not in rt:
        rt["translate"] = [{"x": 0, "y": 0}, {"time": round(clip.dur, 4), "x": 0, "y": 0}]
        nk += 2
    if clip.ev:
        A["events"] = [{"time": round(float(t), 4), "name": nm, "string": str(st)} for t, nm, st in sorted(clip.ev, key=lambda e: e[0])]
        for _, nm, _ in clip.ev:
            sk.events.setdefault(nm, "")
    return A, nk
