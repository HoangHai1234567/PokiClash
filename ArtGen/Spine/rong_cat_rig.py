# -*- coding: utf-8 -*-
"""Rồng giáp sa thạch (rong_cat; tướng 4 đảo Thổ, ải 15): hình của mình chạy trên ĐÚNG rig con gốc monster_3424 (rồng cúi rạp sắp vồ; game
tham khảo). Ghi chú: inbox/rong_cat_ghichu.md. Cách làm như quang_sat_rig.py + quy_dao_rig.py (skill pokiclash-spine-rig mục 00, 28):
- XƯƠNG: đủ mọi xương của họ, dáng gốc = khung 0 idle_01 (biến đổi riêng ĐÃ ÁP ràng buộc `l`: bốn IK chân sau / tay của họ đã nướng thành
  FK), thêm `move` (cha của `bone`: cú lao, game đo quãng) và `cat_x` (mặt nạ cắt mặt đất cho appear).
- MẢNH: ảnh của mình "đúng chỗ, đúng cỡ" trên bố cục (rong_cat_manh.py → inbox/rong_cat_1/manh/), đặt vào thế giới rig ở dáng idle 0; mỗi đỉnh
  lưới của mình biến dạng ĐÚNG như điểm tương ứng trên lưới của họ (trọng số + điểm gắn riêng từng xương). Mắt hai hình (mở, nhắm) đổi theo
  khung như họ. BỎ shadow và bốn gai mào thừa (P_qi01 / qi10 / qi11 / qi12): mào của mình chỉ còn HAI sừng dài (P_qi08, P_qi09).
- THỨ TỰ VẼ: của họ; slot di động (tay xa, tay gần, vuốt, đầu ra trước / sau trong đòn) nhân bản theo chỗ chèn (`<slot>@<chỗ>`).
- CLIP (tho5_anim.py, người dùng duyệt đề xuất 2026-11-17):
    appear  mặt đất nứt, vuốt gần đâm lên bấu đất, rồi vuốt xa, kéo thân trồi lên (vuốt giữ yên chỗ bám: IK hai đoạn), rũ cát, ngẩng gầm
    idle    idle_01 (thân lắc vòng rình mồi) + trò riêng: cào đất hai nhát bằng vuốt gần, rồi khịt hàm
    walk    run_01
    attack  skill_01: đứng lên chân sau, vuốt xa giơ cao CHÉM chéo xuống (lấy đà chậm hơn, chém nhanh hơn, quá đà + nảy)
    cast    skill_02 kéo dài: đứng dậy dang hai tay, gồng ngắn, hai vuốt chém chéo ba nhát vào không khí (sự kiện chem1..3: VFX lưỡi cát)
    skill   skill_03 kéo dài: đứng thẳng giơ hai tay GỒNG (hai dáng lệch 2–3° đổi nhau), NỆN hai vuốt xuống đất, giữ rạp; sự kiện nen,
            cot1..3 (VFX cột sa thạch); tấm giáp lưng nảy lên rồi rơi về chỗ
    hit     hit_01 (mắt nhắm như họ)
    die     die_01 + các tấm giáp rơi khỏi lưng từng tấm, mờ dần
- Lưỡi cát, cột đá, bụi, nứt đất là VFX của game (rig chỉ đặt sự kiện + xương `mieng`).
Xương, lưới, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/rong_cat_rig.py            → inbox/rong_cat_1/rig/
    py -3 -I ArtGen/Spine/rong_cat_rig.py soi <clip> <giây,..|n=12|t0:t1:n> [tỉ lệ]               → rig/soi_<clip>.png
    py -3 -I ArtGen/Spine/rong_cat_rig.py kiem                                                    góc nhảy, bước dời lớn nhất từng clip
  RC_GOC=1: dựng bằng DA GỐC (manh_goc/) vào rig_goc/ (chạy thử clip khi chưa có mảnh của mình).
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import anh, hoat, xuat, soi, luoi, trongso, khung  # noqa: E402
from quai.hoat import Clip  # noqa: E402
from quai.khung import Pose  # noqa: E402
import tho5  # noqa: E402

G = tho5.dat("rong_cat")
GOC = os.environ.get("RC_GOC") == "1"
TEN = "rong_cat_1"
MANH = os.path.join(G.BASE, "manh_goc" if GOC else "manh")
RA = os.environ.get("RC_RA") or os.path.join(G.BASE, "rig_goc" if GOC else "rig")
D_PX = float(os.environ.get("RC_DPX", "0.62"))     # pixel ảnh atlas cho mỗi đơn vị rig (con cao ~740 đơn vị)
FPS = 30.0
SCAN = G.scan()
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
D0 = json.load(open(os.path.join(SCAN, "att_idle0.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample_goc.json"), encoding="utf-8"))
NB = [b["name"] for b in I["bones"]]
SL = [s["name"] for s in I["slots"]]
L0 = S["idle_01"]["frames"][0]["l"]
ZERO5 = np.array([0, 0, 0, 1, 1.0])
USE = ["idle_01", "run_01", "skill_01", "skill_02", "skill_03", "hit_01", "die_01"]
BO_SLOT = {"shadow", "P_qi01", "P_qi10", "P_qi11", "P_qi12", "P_shitou01", "P_shitou02", "P_jian01", "P_jian02"}
GIAP = ["P_shitou0", "P_shitou03", "P_shitou05", "P_shitou06"]
IMPACT = {"attack": (0.10, 0.6, 0.13), "cast": (0.10, 0.6, 0.12), "skill": (0.18, 1.2, 0.26, "#fff3d24d")}
# tay (xương vai → cánh tay → bàn) và vuốt
TAY_GAN = ("bone18", "bone19", "bone20")
TAY_XA = ("bone15", "bone16", "bone17")
VUOT_GAN = ("bone40", "bone29", "bone43")
VUOT_XA = ("bone45", "bone46", "bone44")


def em(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def _goc(M):
    return math.degrees(math.atan2(M[1, 0], M[0, 0]))


def tmap(t, moc):
    """ánh xạ giờ từng đoạn: moc = [(t, tau[, kiểu])...]; kiểu áp cho đoạn KẾT THÚC ở mốc đó."""
    if t <= moc[0][0]:
        return moc[0][1]
    for a, b in zip(moc, moc[1:]):
        if t <= b[0]:
            u = (t - a[0]) / max(1e-9, b[0] - a[0])
            return a[1] + (b[1] - a[1]) * hoat.ease(u, b[2] if len(b) > 2 else "lin")
    return moc[-1][1]


# ---------------------------------------------------------------- thứ tự vẽ của họ: slot đứng yên + slot di động
def _thu_tu():
    base = [s for s in S["idle_01"]["frames"][0]["o"] if SL[s] not in BO_SLOT]
    pos0 = {s: i for i, s in enumerate(base)}
    orders = []
    for c in USE:
        for F in S[c]["frames"]:
            o = tuple(s for s in F["o"] if SL[s] not in BO_SLOT)
            if o not in orders:
                orders.append(o)
    static = set(base)
    while True:
        cnt = {}
        for o in orders:
            seq = [s for s in o if s in static]
            for i in range(len(seq)):
                for j in range(i + 1, len(seq)):
                    if pos0[seq[i]] > pos0[seq[j]]:
                        cnt[seq[i]] = cnt.get(seq[i], 0) + 1
                        cnt[seq[j]] = cnt.get(seq[j], 0) + 1
        if not cnt:
            break
        static.discard(max(cnt, key=lambda k: (cnt[k], -pos0[k])))
    stat = [s for s in base if s in static]
    return base, stat, [s for s in base if s not in static], orders


BASE, STAT, DONG, ORDERS = _thu_tu()
STAT_I = {s: i for i, s in enumerate(STAT)}


def neo(o, m):
    """chỗ chèn của slot di động m trong thứ tự vẽ o: số slot đứng yên được vẽ trước nó."""
    n = 0
    for s in o:
        if s == m:
            return n
        if s in STAT_I:
            n += 1
    return n


NEO0 = {m: neo(S["idle_01"]["frames"][0]["o"], m) for m in DONG}
BAN = {m: sorted({neo(o, m) for o in ORDERS} | {NEO0[m]}) for m in DONG}


def ten_ban(m, k):
    return SL[m] if k == NEO0[m] else f"{SL[m]}@{k}"


def thu_tu_slot():
    """danh sách (tên slot của mình, chỉ số slot của họ) theo thứ tự vẽ: slot đứng yên theo thứ tự idle; mỗi bản của slot di động chèn sau
    slot đứng yên thứ k (cùng chỗ chèn thì theo thứ tự idle của họ)."""
    out = []
    for k in range(len(STAT) + 1):
        for m in DONG:
            for kk in BAN[m]:
                if kk == k:
                    out.append((ten_ban(m, kk), m))
        if k < len(STAT):
            out.append((SL[STAT[k]], STAT[k]))
    # chân sau gần vẽ DƯỚI đuôi và thân (họ: trên thân; người dùng chê "bụng bị lỗi": đùi gốc vẽ đè lên bụng thành vết rách) → đỉnh đùi luôn nấp
    # sau hông, bụng chỉ còn một đường viền ngoài; ba khúc giữ thứ tự bàn → cẳng → đùi
    chan = [x for x in out if x[0] in ("P_jiao01", "P_xiaotui01", "P_datui01")]
    for x in chan:
        out.remove(x)
    i_duoi = next(i for i, x in enumerate(out) if x[0] == "P_weiba")
    out[i_duoi:i_duoi] = chan
    # bố cục của mình: hai tấm giáp lưng P_shitou0, P_shitou06 nằm TRÊN cánh tay gần (họ: đá nằm dưới cánh tay) → dời ra ngay sau P_shoubi01
    for ten in ("P_shitou0", "P_shitou06"):
        if ten in [n for n, _ in out] and "P_shoubi01" in [n for n, _ in out]:
            g = next(x for x in out if x[0] == ten)
            out.remove(g)
            out.insert(next(i for i, x in enumerate(out) if x[0] == "P_shoubi01") + 1, g)
    return out


# ---------------------------------------------------------------- chuyển động của họ
def _cd():
    out = {}
    for clip in USE:
        v = S[clip]
        fr = v["frames"]
        res = {}
        for i, b0 in enumerate(I["bones"]):
            if b0["name"] in ("root", "shadow"):
                continue
            z = L0[i]
            Am = np.array([[F["l"][i][2] - z[2], F["l"][i][0] - z[0], F["l"][i][1] - z[1],
                            F["l"][i][3] / (z[3] or 1.0), F["l"][i][4] / (z[4] or 1.0)] for F in fr])
            Am[:, 0] = np.degrees(np.unwrap(np.radians(Am[:, 0])))
            Am[:, 0] -= 360.0 * round(Am[0, 0] / 360.0)
            if np.abs(Am - ZERO5).max() > 1e-4:
                res[b0["name"]] = Am
        hinh = [[(F["n"][k], float(F["a"][k])) for k in range(len(SL))] for F in fr]
        cho = [{m: neo(F["o"], m) for m in DONG} for F in fr]
        out[clip] = (float(v["dur"]), res, hinh, cho)
    return out


CD = _cd()


def khung_ho(clip, t, lap=False):
    dur, _, hinh, _ = CD[clip]
    n = len(hinh)
    tq = t % dur if lap else min(max(t, 0.0), dur)
    return min(n - 1, int(round(tq * FPS)))


def gia_tri(clip, t, lap=False):
    """{xương: [xoay, dx, dy, sx, sy]} của họ ở giây t (nội suy giữa hai khung mẫu)."""
    dur, R, hinh, _ = CD[clip]
    n = len(hinh)
    tq = t % dur if lap else min(max(t, 0.0), dur)
    x = tq * FPS
    i0 = min(int(x), n - 1)
    i1 = min(i0 + 1, n - 1)
    w = x - i0
    return {b: A[i0] * (1 - w) + A[i1] * w for b, A in R.items()}


def ap(P, d, k=1.0, chi=None, tru=None):
    for b, v in d.items():
        if (chi is not None and b not in chi) or (tru is not None and b in tru):
            continue
        if abs(v[0]) > 1e-5:
            P.rot(b, float(k * v[0]))
        if abs(v[1]) > 1e-5 or abs(v[2]) > 1e-5:
            P.move(b, float(k * v[1]), float(k * v[2]))
        if abs(v[3] - 1) > 1e-6 or abs(v[4] - 1) > 1e-6:
            P.scale(b, float(1 + k * (v[3] - 1)), float(1 + k * (v[4] - 1)))


def pha(a, b, w):
    """pha hai bộ giá trị {xương: [xoay, dx, dy, sx, sy]}: góc của b quy về cùng vòng với a."""
    out = {}
    for k in set(a) | set(b):
        x, y = np.array(a.get(k, ZERO5), float), np.array(b.get(k, ZERO5), float)
        y[0] += 360.0 * round((x[0] - y[0]) / 360.0)
        out[k] = x * (1 - w) + y * w
    return out


def hien_theo_ho(sk, P, clip, t, lap=False):
    """hình + độ đậm của mọi slot theo khung của họ; slot di động bật đúng bản theo chỗ chèn của họ ở khung đó."""
    i = khung_ho(clip, t, lap)
    hinh, cho = CD[clip][2][i], CD[clip][3][i]
    for k, sl in enumerate(SL):
        if sl in BO_SLOT:
            continue
        n, a = hinh[k]
        an = n is None
        ten_hinh = None
        if sl == "P_yanjing01" and not an:
            ten_hinh = "mat_nham" if n == "P_yanjing01" else "P_yanjing01"
        if k in NEO0:
            for kk in BAN[k]:
                nm = ten_ban(k, kk)
                if nm not in sk.si:
                    continue
                P.alpha[nm] = (a if not an else 0.0) if kk == cho[k] else 0.0
                if ten_hinh and ten_hinh in sk.atts[nm]:
                    P.att[nm] = ten_hinh
        elif sl in sk.si:
            P.alpha[sl] = a if not an else 0.0
            if ten_hinh and ten_hinh in sk.atts[sl]:
                P.att[sl] = ten_hinh


# ---------------------------------------------------------------- mảnh
def tf():
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    return s, (lambda P: np.stack([cx + (P[:, 0] - 768) / s, cy - (P[:, 1] - 512) / s], 1))


def anh_manh(ten):
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    s_px, _ = tf()
    g = Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA")
    kq = D_PX / s_px
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g), DATJ[ten]["hop"], kq


def trong_so_goc(V, a0, Wi):
    """mỗi điểm V (thế giới idle 0) biến dạng như điểm tương ứng trên lưới của họ a0 (att_idle0): toạ độ trọng tâm trong tam giác chứa nó
    (ngoài lưới: điểm gần nhất trên cạnh + khoảng lệch), W_b = Σ β_k w_b(k), điểm gắn riêng q_b = Σ β_k w_b(k) v_k / W_b. Trả hàng
    (xương, x, y, w) theo ma trận idle 0 Wi."""
    Q = np.array(a0["xy"], float).reshape(-1, 2)
    tr = np.array(a0["tris"]).reshape(-1, 3)
    Wg = [{NB[k]: w for k, w in ws if w > 0.002} for ws in a0["w"]]
    A, B_, C = Q[tr[:, 0]], Q[tr[:, 1]], Q[tr[:, 2]]
    v0, v1 = B_ - A, C - A
    den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
    den = np.where(np.abs(den) < 1e-9, 1e-9, den)

    def gan_canh(p, a, b):
        d = b - a
        t = np.clip(((p - a) * d).sum(axis=1) / np.maximum((d * d).sum(axis=1), 1e-12), 0, 1)
        return np.hypot(*(p - (a + t[:, None] * d)).T), t

    rows, ngoai = [], []
    for p in V:
        v2 = p - A
        b1 = (v2[:, 0] * v1[:, 1] - v2[:, 1] * v1[:, 0]) / den
        b2 = (v0[:, 0] * v2[:, 1] - v0[:, 1] * v2[:, 0]) / den
        b0 = 1 - b1 - b2
        ok = np.flatnonzero((b0 >= -1e-4) & (b1 >= -1e-4) & (b2 >= -1e-4))
        lech = np.zeros(2)
        if len(ok):
            i = int(ok[0])
            be = (float(b0[i]), float(b1[i]), float(b2[i]))
            ngoai.append(False)
        else:
            best = None
            for (pa, pb, ia, ib) in ((A, B_, 0, 1), (B_, C, 1, 2), (C, A, 2, 0)):
                dist, t = gan_canh(p, pa, pb)
                j = int(np.argmin(dist))
                if best is None or dist[j] < best[0]:
                    w3 = [0.0, 0.0, 0.0]
                    w3[ia], w3[ib] = 1 - float(t[j]), float(t[j])
                    best = (float(dist[j]), j, tuple(w3), pa[j] + t[j] * (pb[j] - pa[j]))
            _, i, be, c = best
            lech = p - c
            ngoai.append(True)
        acc = {}
        for vi, bw in zip(tr[i], be):
            for n, w in Wg[vi].items():
                e = acc.setdefault(n, [0.0, np.zeros(2)])
                e[0] += bw * w
                e[1] += bw * w * Q[vi]
        row = []
        for n, (w, q) in acc.items():
            if abs(w) < 1e-5:
                continue
            g = q / w + lech
            lp = np.linalg.solve(Wi[n], np.array([g[0], g[1], 1.0]))
            row.append((n, float(lp[0]), float(lp[1]), float(w)))
        tot = sum(r[3] for r in row) or 1.0
        rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    return rows, np.array(ngoai)


def lam_tron(L, V, rows, ngoai, Wi, vong=40):
    """đỉnh nằm ngoài lưới của họ: trọng số làm trơn theo cạnh lưới mình (vong vòng), điểm gắn tính lại từ chỗ thế giới idle 0 (một điểm
    chung): hai đỉnh kề nhau rơi vào hai tam giác khác nhau của họ thì mảnh khỏi bị xé (skill mục 28)."""
    if not ngoai.any():
        return rows
    xs = sorted({b for r in rows for b, *_ in r})
    bi = {b: i for i, b in enumerate(xs)}
    Wm = np.zeros((len(rows), len(xs)))
    for i, r in enumerate(rows):
        for b, _, _, w in r:
            Wm[i, bi[b]] = w
    ke = [set() for _ in rows]
    for t in L.tris:
        for a in t:
            for b in t:
                if a != b:
                    ke[a].add(b)
    for _ in range(vong):
        Wn = Wm.copy()
        for i in np.flatnonzero(ngoai):
            if ke[i]:
                Wn[i] = 0.5 * Wm[i] + 0.5 * Wm[list(ke[i])].mean(0)
        Wm = Wn
    out = list(rows)
    for i in np.flatnonzero(ngoai):
        w = Wm[i]
        w[w < 0.01] = 0
        w /= w.sum() or 1.0
        row = []
        for b, wb in zip(xs, w):
            if wb <= 0:
                continue
            lp = np.linalg.solve(Wi[b], np.array([V[i, 0], V[i, 1], 1.0]))
            row.append((b, float(lp[0]), float(lp[1]), float(wb)))
        out[i] = row
    return out


def gan_manh(sk, slot, ten_anh, a0, Wi):
    """mảnh của mình (manh/<ten_anh>.png, hộp trên khung concept) thành lưới đặt đúng chỗ ở dáng idle 0, bám như lưới a0 của họ."""
    im, (x0, y0, x1, y1), kq = anh_manh(ten_anh)
    if ten_anh not in sk.images:
        sk.anh(ten_anh, im)
    im = sk.images[ten_anh]
    _, to_rig = tf()
    nhieu = len({k for ws in a0["w"] for k, w in ws if w > 0.002}) > 1
    if nhieu:
        L = luoi.luoi_vung(im, buoc_vien=10.0, buoc_trong=15.0, vien=2, ten=slot, in_tk=False)
    else:
        L = luoi.luoi_o(im.width, im.height, 2, 2, ten=slot)
    Px = np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1)
    V = to_rig(Px)
    rows, ngoai = trong_so_goc(V, a0, Wi)
    if nhieu:
        rows = lam_tron(L, V, rows, ngoai, Wi)
    Vs = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows])
    sk.luoi_gan(slot, ten_anh, L, trongso.cung(L.n, "move"), the_gioi=Vs)
    sk.atts[slot][ten_anh]["verts"] = rows
    return L


# ---------------------------------------------------------------- dựng
CAT_TI, CAT_SAU = 12.0, 4000.0


def dung():
    sk = khung.Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")
    for i, b in enumerate(I["bones"]):
        if b["name"] in ("root", "shadow"):
            continue
        cha = NB[b["parent"]]
        if cha == "root":
            cha = "move"
        g = L0[i]
        sk.xuong(b["name"], cha, g[0], g[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
    # kiểm dáng gốc trùng ma trận idle 0 của họ
    Wi = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]]) for b in D0["bones"]}
    lech = max(float(np.abs(sk.W0[n] - Wi[n]).max()) for n in sk.W0 if n in Wi and n not in ("root",))
    if lech > 0.05:
        print(f"CẢNH BÁO: dáng gốc lệch ma trận idle 0 của họ {lech:.3f}")
    Wi = {n: sk.W0[n] for n in sk.W0}
    by0 = {a["slot"]: a for a in D0["atts"]}
    sk.xuong("cat_x", "move", 0.0, -CAT_SAU, sx=CAT_TI, sy=CAT_TI)
    sk.slot("cat", "cat_x")
    tong = [0, 0]
    for nm, k in thu_tu_slot():
        sl = SL[k]
        a0 = by0[sl]
        hinh = ["P_yanjing01", "mat_nham"] if sl == "P_yanjing01" else [sl]
        sk.slot(nm, "move", hinh[0])
        for h in hinh:
            L = gan_manh(sk, nm, h, a0, Wi)
            tong[0] += L.n
            tong[1] += len(L.tris)
    last = sk.slots[-1]["name"]
    sk.cat("cat", last, mat_dat())
    # chỗ phát VFX của cast (game đọc `mieng` ở khung nhả): ngọn cẳng tay gần (chỗ vuốt quét ra lưỡi cát)
    W0 = sk.W0
    L20 = sk.bones[sk.bi["bone20"]]["length"]
    sk.xuong("mieng", "bone20", L20, 0.0)
    mieng_tg = W0["mieng"][:2, 2]
    for e, m in (("trung", "khung trúng"), ("chem1", "cast: nhát chém 1 (VFX lưỡi cát)"), ("chem2", "cast: nhát chém 2"),
                 ("chem3", "cast: nhát chém 3"), ("gong", "skill: gồng"), ("nen", "skill: nện đất, nứt lan tới đối thủ (VFX)"),
                 ("cot1", "skill: cột sa thạch nhịp 1"), ("cot2", "skill: cột nhịp 2"), ("cot3", "skill: cột to nhất, hất tung"),
                 ("nut", "appear: đất nứt"), ("vuot1", "appear: vuốt xa (phía trước) đập xuống bấu đất"), ("vuot2", "appear: vuốt gần đập xuống bấu đất"),
                 ("troi", "appear: thân trồi lên, đất nổ"), ("ru", "appear: rũ cát"), ("gam", "appear: gầm"), ("cao_dat", "idle: cào đất (cát văng)"),
                 ("cham_dat", "chạm đất mạnh (bụi)")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác; slot di động {len(DONG)}: "
          f"{[SL[m] for m in DONG]}; mieng {mieng_tg.round(0)}")
    return sk


def mat_dat():
    """đa giác LỒI của mặt nạ cắt (thế giới dáng gốc khi cat_x ở tỉ lệ CAT_TI, sâu CAT_SAU): giữ phần TRÊN mặt đất (y > −2)."""
    R = 3000.0
    pts = [(-R, -2.0), (R, -2.0), (R, 2600.0), (-R, 2600.0)]
    return [(px * CAT_TI, -CAT_SAU + py * CAT_TI) for px, py in pts[::-1]]


# ---------------------------------------------------------------- tiện ích dáng
def tg(sk, P, b):
    W = sk.the_gioi(P)
    return W[b][:2, 2].copy(), _goc(W[b])


def dich_tg(sk, P, b, d):
    """dời xương b thêm véc-tơ d (thế giới)."""
    W = sk.the_gioi(P)
    Wp = W[sk.bones[sk.bi[b]]["parent"]]
    dl = np.linalg.solve(Wp[:2, :2], np.asarray(d, float))
    P.move(b, float(dl[0]), float(dl[1]))


UON = {}


def ik_tay(sk, P, tay, dich, k=1.0):
    """IK hai đoạn cánh tay: xương cánh tay → xương cẳng / bàn (gốc ở khuỷu); đặt NGỌN cẳng (chỗ vuốt chạm đất) tới đích thế giới. Thử cả hai
    chiều gập khuỷu, lấy nghiệm gần dáng đang có nhất (khỏi lật khuỷu giữa hai khung), rồi hoà với dáng đang có theo k (0..1)."""
    _, canh, ban = tay
    if tay not in UON:                                         # chiều gập khuỷu cố định theo dáng đứng (đổi chiều giữa clip là lật khuỷu)
        W = sk.W0
        A, B = W[canh][:2, 2], W[ban][:2, 2]
        C = ngon_tay(sk, W, tay)
        cr = (C - A)[0] * (B - A)[1] - (C - A)[1] * (B - A)[0]
        UON[tay] = 1.0 if cr >= 0 else -1.0
    g0 = {b: list(P._g(b)) for b in (canh, ban)}
    Q = P.copy()
    hoat.ik_hai_doan(sk, Q, canh, ban, dich, ngon=None, uon=UON[tay])
    for b in (canh, ban):
        dd = ((Q._g(b)[2] - g0[b][2] + 180.0) % 360.0) - 180.0
        P._g(b)[2] = g0[b][2] + k * dd


def ngon_tay(sk, W, tay):
    """chỗ ngọn cẳng tay (thế giới) theo ma trận W."""
    ban = tay[2]
    return (W[ban] @ np.array([sk.bones[sk.bi[ban]]["length"], 0.0, 1.0]))[:2]


# ---------------------------------------------------------------- clip
def lam_clip(sk, cao):
    W0 = sk.W0

    def theo_ho(P, clip, tau, lap=False, k=1.0, chi=None, tru=None, hien=True):
        ap(P, gia_tri(clip, tau, lap), k, chi, tru)
        if hien:
            hien_theo_ho(sk, P, clip, tau, lap)

    # ------------------------------------------------ idle: SÓNG MỀM lệch pha trên dáng đứng (không dùng nguyên idle_01 của họ: người dùng chê
    # idle tướng 1 "giật, không mềm mại"). Vòng 4 s = hai nhịp thở 2 s; ngực dẫn, cổ trễ 0,1 s, đầu giữ yên nhìn đối thủ (xoay bù nhẹ), hàm,
    # giáp, sừng trễ 0,15–0,35 s, đuôi sóng chậm 4 s lan gốc → ngọn; trò nhỏ: một lần cào đất chậm bằng vuốt gần 2,30 → 3,70 s.
    D_IDLE = 4.0
    T_CAO0, T_CAO1 = 2.30, 3.70

    def tho(t, tre=0.0, chu=2.0):
        return math.sin(2 * math.pi * (t - tre) / chu)

    def f_idle(t, P):
        theo_ho(P, "idle_01", 0.0)
        b = tho(t)
        P.scale("bone5", 1 + 0.018 * b, 1 + 0.018 * b)          # thở: ngực phồng 1 ± 1,8 %
        P.scale("bone4", 1 + 0.010 * tho(t, 0.08), 1 + 0.010 * tho(t, 0.08))
        P.move("bone3", 0.0, 2.2 * tho(t, 0.05))
        P.rot("bone5", 1.1 * tho(t, 0.0))
        P.rot("bone4", -0.6 * tho(t, 0.05))
        P.rot("bone6", 1.0 * tho(t, 0.10))                      # cổ trễ
        P.rot("bone13", -1.3 * tho(t, 0.18))                    # đầu xoay bù: gần như đứng yên, mắt vẫn nhìn đối thủ
        P.rot("bone14", 0.9 * tho(t, 0.26))                     # hàm
        for bn, tre, a in (("bone30", 0.28, 1.6), ("bone31", 0.34, 1.9),                     # hai sừng dài
                           ("bone27", 0.18, 1.3), ("bone35", 0.22, 1.1), ("bone36", 0.26, 1.2), ("bone37", 0.16, 1.0),
                           ("bone41", 0.30, 1.5), ("bone42", 0.35, 1.8)):                    # giáp lưng, vảy đuôi
            P.rot(bn, a * tho(t, tre))
        for i, bn in enumerate(("bone7", "bone8", "bone9", "bone10")):                    # đuôi: sóng 4 s, gốc dẫn ngọn
            P.rot(bn, (1.6 + 1.1 * i) * tho(t, 0.17 * i, 4.0))
        for bn, tre, a in (("bone16", 0.12, 0.8), ("bone19", 0.14, -0.8)):                  # hai cánh tay theo ngực
            P.rot(bn, a * tho(t, tre))
        # cào đất chậm: nhấc vuốt gần lên, kéo về sau trên mặt đất, đặt lại (mọi đoạn êm, không đổi hướng gắt)
        if T_CAO0 < t < T_CAO1:
            u = (t - T_CAO0) / (T_CAO1 - T_CAO0)
            env = math.sin(math.pi * u) ** 2
            nhac = math.sin(math.pi * min(1.0, u / 0.50)) ** 2 if u < 0.50 else 0.0          # sin²: đầu, cuối mỗi đoạn vận tốc 0
            keo = math.sin(math.pi * max(0.0, (u - 0.25) / 0.65)) ** 2 if 0.25 < u < 0.90 else 0.0
            P.rot("bone19", env * (9.0 * nhac - 7.0 * keo))
            P.rot("bone20", env * (-12.0 * nhac + 6.0 * keo))
            for bn in VUOT_GAN:
                P.rot(bn, env * 8.0 * nhac)
            P.rot("bone13", env * -2.0)                         # liếc xuống chỗ cào
            P.rot("bone5", env * 1.2)

    def f_walk(t, P):
        theo_ho(P, "run_01", t, True)

    def f_hit(t, P):
        theo_ho(P, "hit_01", t)

    # ------------------------------------------------ attack: skill_01 (đứng lên, vuốt xa giơ cao, chém chéo xuống)
    # lấy đà chậm hơn họ (0 → 0,33 trong 0,42 s), cú chém trải ĐỀU ba khung (0,33 → 0,45 trong 0,10 s: mỗi khung dời ~0,3 chiều cao thay
    # vì 0,9), quá đà rồi về
    M_ATK = [(0.0, 0.0), (0.40, 0.33, "io"), (0.555, 0.45, "lin"), (0.68, 0.57, "out"), (1.15, 1.0, "io")]
    T_ATK = 0.54

    def f_attack(t, P):
        tau = tmap(t, M_ATK)
        theo_ho(P, "skill_01", tau)
        k = math.exp(-((t - (T_ATK + 0.02)) / 0.05) ** 2)
        P.scale("bone4", 1 + 0.06 * k, 1 - 0.05 * k)           # nén thân đúng khung chém
        if t > T_ATK:
            P.rot("bone5", hoat_tat(t, T_ATK, 2.2, 9.0, 0.10))  # quá đà + nảy
            P.rot("bone13", hoat_tat(t, T_ATK + 0.02, -1.6, 9.0, 0.10))

    # ------------------------------------------------ cast: skill_02 kéo dài, ba nhát chém vào không khí
    D_CAST = 1.55
    M_CAST = [(0.0, 0.0), (0.36, 0.40, "io"), (0.60, 0.53, "lin"), (0.79, 0.70, "lin"), (0.94, 0.80, "out"), (D_CAST, 1.20, "io")]
    T_CHEM = (0.70, 0.76, 0.84)                                 # vuốt xa quét, vuốt gần quét, cả hai

    def f_cast(t, P):
        tau = tmap(t, M_CAST)
        theo_ho(P, "skill_02", tau)
        # gồng ngắn trước khi chém (hai dáng lệch nhau)
        r = hoat.rung(t, 0.40, 0.62, 2)
        P.rot("bone5", 1.6 * r)
        P.rot("bone4", -1.0 * r)
        # mỗi nhát chém: hai cánh tay giật chéo thêm, thân xoắn theo
        for i, tc in enumerate(T_CHEM):
            k = math.exp(-((t - tc) / 0.045) ** 2)
            dau = 1.0 if i % 2 == 0 else -1.0
            P.rot("bone16", 16.0 * k * dau)
            P.rot("bone19", -16.0 * k * dau)
            P.rot("bone5", 3.0 * k * dau)
        if t > T_CHEM[-1]:
            P.rot("bone5", hoat_tat(t, T_CHEM[-1], 1.8, 8.0, 0.12))

    # ------------------------------------------------ skill: skill_03 kéo dài: gồng giơ tay → nện → giữ rạp (cột đá ba nhịp)
    D_SKILL = 2.25
    T_GONG0, T_GONG1, T_NEN = 0.36, 1.02, 1.16
    # cú nện của họ (0,33 → 0,40: cánh tay xa quay ~210° trong hai khung) trải ra 0,14 s (≈ 4 khung), đều
    M_SKILL = [(0.0, 0.0), (0.36, 0.30, "io"), (T_GONG1, 0.33, "lin"), (T_NEN, 0.44, "lin"), (1.92, 1.04, "lin"), (D_SKILL, 1.333, "io")]
    T_COT = (T_NEN + 0.18, T_NEN + 0.40, T_NEN + 0.66)

    XUONG_GIAP = ("bone27", "bone35", "bone36", "bone37", "bone38", "bone39")

    def f_skill(t, P):
        tau = tmap(t, M_SKILL)
        theo_ho(P, "skill_03", tau, tru=XUONG_GIAP)            # họ cho đá lưng bay đi: mình giữ giáp trên lưng
        # họ ẩn dần đá lưng (đá bay đi): mình giữ giáp trên lưng
        for g in GIAP:
            if g in sk.si:
                P.alpha[g] = 1.0
        if T_GONG0 < t < T_GONG1:
            env = em((t - T_GONG0) / 0.12) * (1 - em((t - (T_GONG1 - 0.06)) / 0.06))
            r = hoat.rung(t, T_GONG0, T_GONG1, 2)
            for b, a in (("bone5", 2.6), ("bone4", -1.4), ("bone13", 2.0), ("bone16", 3.0), ("bone19", -3.0)):
                P.rot(b, env * a * r)
            P.scale("bone5", 1 + 0.03 * env, 1 + 0.03 * env)       # phồng ngực
        k = math.exp(-((t - (T_NEN + 0.02)) / 0.05) ** 2)
        P.scale("bone4", 1 + 0.07 * k, 1 - 0.07 * k)
        if t > T_NEN:
            P.rot("bone5", hoat_tat(t, T_NEN, 2.4, 7.0, 0.12))
            # tấm giáp lưng nảy lên một nhịp rồi rơi về
            for j, g in enumerate(("bone27", "bone37", "bone38", "bone39", "bone35", "bone36")):
                s = t - (T_NEN + 0.02 * j)
                if 0 < s < 0.4:
                    h = 18.0 * math.sin(math.pi * min(1.0, s / 0.22)) if s < 0.22 else 4.0 * math.sin(math.pi * (s - 0.22) / 0.18)
                    dich_tg(sk, P, g, (0.0, h))

    # ------------------------------------------------ die: die_01 + giáp rơi từng tấm + mờ dần
    D_DIE = CD["die_01"][0]
    TAN = 0.55

    def f_die(t, P):
        tau = tmap(t, [(0.0, 0.0), (0.14, 0.10, "io"), (D_DIE, D_DIE, "lin")])
        theo_ho(P, "die_01", tau, tru=XUONG_GIAP)
        for g in GIAP:
            if g in sk.si:
                P.alpha[g] = 1.0
        for j, b in enumerate(("bone38", "bone39", "bone37", "bone27", "bone35", "bone36")):
            s = t - (0.50 + 0.07 * j)
            if s > 0:
                y_cur = tg(sk, P, b)[0][1]
                roi = min(0.5 * 2600.0 * s * s, max(0.0, y_cur - 30.0))        # rơi tới mặt đất (y ≈ 30) rồi nằm
                cham = y_cur - roi <= 30.5
                nay = 10.0 * abs(math.sin(10.0 * s)) * math.exp(-6.0 * s) if cham else 0.0
                dau = -1.0 if j % 2 else 1.0
                dich_tg(sk, P, b, (dau * 70.0 * min(s, 0.3), -roi + nay))
                P.rot(b, dau * 110.0 * min(s, 0.32))
        a = float(np.clip(1.0 - (t - D_DIE) / (TAN - 0.05), 0.0, 1.0))
        if a < 0.999:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])

    # ------------------------------------------------ appear: vuốt bấu đất, kéo thân trồi lên, rũ cát, gầm
    # Trồi khỏi hố như leo ra: (1) đầu và hai tay chồi lên trước, thân chúc mũi lên (xoay quanh hông), vuốt gần rồi vuốt xa đập xuống BÁM
    # mặt đất đúng chỗ cổ tay ở dáng đứng; (2) thân được kéo lên, xoay về ngang, hai vuốt giữ yên chỗ bám (IK hai đoạn); (3) rũ cát, gầm.
    D_APPEAR = 2.10
    T_V1, T_V2, T_TROI0, T_TROI1, T_RU0, T_RU1, T_GAM = 0.30, 0.80, 0.58, 1.16, 1.22, 1.50, 1.60
    SAU = 1.40 * cao                                           # thân nằm sâu dưới đất chừng này lúc đầu (không ló gì)
    SAU_A = 0.62 * cao                                         # pha 1: chồi lên tới đây, chúc mũi lên NGHIENG độ
    NGHIENG = 26.0
    P0 = Pose()
    theo_ho(P0, "idle_01", 0.0, hien=False)
    W_i0 = sk.the_gioi(P0)
    co_gan = ngon_tay(sk, W_i0, TAY_GAN)                       # ngọn cẳng tay ở dáng đứng (chỗ vuốt bám đất)
    co_xa = ngon_tay(sk, W_i0, TAY_XA)
    hong = W_i0["bone3"][:2, 2].copy()                         # tâm xoay chúc mũi (hông)

    def f_appear(t, P):
        theo_ho(P, "idle_01", 0.0)
        if t < 0.16:                                           # còn hẳn dưới đất: khung đầu trống
            for sl in sk.slots:
                P.alpha[sl["name"]] = 0.0
        if t < 0.18:
            h, ng = -SAU, 0.0
        elif t < T_TROI0:                                      # pha 1: chồi lên nửa chừng, chúc mũi lên
            u = hoat.ease((t - 0.18) / (T_V1 + 0.06 - 0.18), "out")
            h, ng = -SAU + (SAU - SAU_A) * u, NGHIENG * u
        elif t < T_TROI1:                                      # pha 2: kéo thân lên, về ngang
            u = hoat.ease((t - T_TROI0) / (T_TROI1 - T_TROI0), "io")
            h, ng = -SAU_A * (1 - u), NGHIENG * (1 - u)
        else:
            h, ng = 0.0, 0.0
        if t > T_TROI1:                                        # vọt hơi quá rồi lún về
            h += 16.0 * math.sin(math.pi * min(1.0, (t - T_TROI1) / 0.16)) if t < T_TROI1 + 0.16 else 0.0
        # xoay "bone" quanh hông: xoay + bù dời cho hông đứng yên
        if abs(ng) > 1e-4:
            W = sk.the_gioi(P)
            o = W["bone"][:2, 2]
            c, s = math.cos(math.radians(ng)), math.sin(math.radians(ng))
            d = hong - o
            hong2 = o + np.array([c * d[0] - s * d[1], s * d[0] + c * d[1]])
            P.rot("bone", ng)
            P.move("bone", float(hong[0] - hong2[0]), float(hong[1] - hong2[1]))
        P.move("bone", 0.0, h)
        P.rot("bone13", -10.0 * math.sin(math.pi * min(1.0, max(0.0, (t - T_TROI0) / (T_TROI1 - T_TROI0 + 0.1)))))
        # rũ cát: lắc cả thân hai dáng
        if T_RU0 < t < T_RU1:
            r = math.sin((t - T_RU0) * 2 * math.pi / 0.09) * em((T_RU1 - t) / 0.1)
            P.rot("bone4", 3.0 * r)
            P.rot("bone5", -4.0 * r)
            P.rot("bone13", 5.0 * r)
        # gầm: ngẩng đầu, há hàm
        if t > T_GAM:
            k = em((t - T_GAM) / 0.12) * (1 - em((t - (D_APPEAR - 0.22)) / 0.22))
            P.rot("bone13", 16.0 * k + 1.2 * math.sin((t - T_GAM) * 50.0) * k)
            P.rot("bone14", -20.0 * k)
            P.rot("bone6", 6.0 * k)
        # mặt nạ đất bật suốt lúc còn dưới đất
        if t < T_TROI1 + 0.05:
            P.move("cat_x", 0.0, CAT_SAU)
            P.scale("cat_x", 1.0 / CAT_TI, 1.0 / CAT_TI)
        # vuốt: từ lúc t_v vươn lên cao rồi ĐẬP xuống bám đúng chỗ cổ tay ở dáng đứng; sau đó giữ yên chỗ bám (IK) tới khi thân lên hẳn
        for tay, co, t_v in ((TAY_XA, co_xa, T_V1),):          # chỉ vuốt XA (phía trước) bám đất bằng IK; vuốt gần IK thì khuỷu lật khi thân
                                                                # còn thấp → để vuốt gần theo thân trồi lên, chạm đất ở 0,90 (sự kiện vuot2)
            if t < t_v - 0.25 or t > T_TROI1 + 0.10:
                continue
            cao_v = co + np.array([60.0, 150.0])                # chỗ giơ vuốt lên trước khi đập xuống
            if t < t_v:                                         # giơ vuốt lên cao, ra trước (hoà dần từ dáng tự nhiên trong 0,25 s)
                dich, k = cao_v, hoat.ease((t - (t_v - 0.25)) / 0.25, "io")
            elif t < t_v + 0.10:                                # đập xuống
                u = hoat.ease((t - t_v) / 0.10, "in")
                dich, k = cao_v * (1 - u) + co * u, 1.0
            else:
                dich, k = co.copy(), 1.0
            if t > T_TROI1:
                k *= 1.0 - hoat.ease((t - T_TROI1) / 0.10)
            ik_tay(sk, P, tay, dich, k)

    ev_appear = [(0.05, "nut", ""), (T_V1 + 0.10, "vuot1", ""), (T_V2 + 0.10, "vuot2", ""), (T_TROI0, "troi", ""), (T_RU0, "ru", ""),
                 (T_GAM, "gam", "")]
    clips = [
        Clip("appear", D_APPEAR, f_appear, ev=ev_appear),
        Clip("idle", D_IDLE, f_idle, loop=True, ev=[(T_CAO0 + 0.90, "cao_dat", "")]),
        Clip("walk", CD["run_01"][0], f_walk, loop=True),
        Clip("attack", 1.15, f_attack, ev=[(T_ATK, "trung", "")], trung=T_ATK),
        Clip("cast", D_CAST, f_cast, ev=[(T_CHEM[0], "chem1", ""), (T_CHEM[1], "chem2", ""), (T_CHEM[2], "chem3", ""),
                                          (T_CHEM[1] + 0.22, "trung", "")], trung=T_CHEM[1]),
        Clip("skill", D_SKILL, f_skill, ev=[(T_GONG0, "gong", ""), (T_NEN, "nen", ""), (T_COT[0], "cot1", ""), (T_COT[1], "cot2", ""),
                                            (T_COT[2], "cot3", ""), (T_COT[2], "trung", "")], trung=T_COT[2]),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", D_DIE + TAN, f_die),
    ]
    return clips


def nuong_lap(sk, clip, m=6):
    """nướng clip lặp như hoat.nuong nhưng khép vòng THEO VÒNG GÓC: góc nướng của họ cộng dồn ±360 qua một chu kỳ (chân chạy), hoà thẳng về
    khung 0 thì chân quay tít; ở đây đích của từng xương là góc khung 0 + 360·k gần góc đang có nhất (cùng tư thế)."""
    n = int(round(clip.dur * FPS)) + 1
    ts = [min(clip.dur, i / FPS) for i in range(n)]
    fr = []
    for t in ts:
        P = Pose()
        clip.fn(t, P)
        fr.append(P)
    a0 = fr[0]
    m = min(m, max(0, n // 3))
    for j in range(m + 1):
        w = (j + 1) / (m + 1) if j < m else 1.0
        P = fr[n - 1 - m + j]
        for b in set(P.t) | set(a0.t):
            pa, pb = P._g(b), list(a0.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0]))
            pb[2] += 360.0 * round((pa[2] - pb[2]) / 360.0)
            for q in range(5):
                pa[q] = pa[q] * (1 - w) + pb[q] * w
        if j == m:
            P.alpha = dict(a0.alpha)
            P.att = dict(a0.att)
    return fr


def nuong(sk, c):
    return nuong_lap(sk, c) if c.loop else hoat.nuong(sk, c)


def hoat_tat(t, t0, bien, tan, giam):
    """rung tắt dần sau t0 (biên độ bien, tần tan Hz, giảm theo giam giây)."""
    if t < t0:
        return 0.0
    s = t - t0
    return bien * math.exp(-s / giam) * math.sin(2 * math.pi * tan * s)


def main(a):
    sk = dung()
    ve0 = soi.Ve(sk)
    P0 = Pose()
    ap(P0, gia_tri("idle_01", 0.0))
    cao = soi.chieu_cao(ve0, P0)
    clips = lam_clip(sk, cao)
    print(f"chiều cao {cao:.0f}")
    if a and a[0] == "kiem":
        for c in clips:
            fr = nuong(sk, c)
            xau = []
            for i in range(1, len(fr)):
                A, B = fr[i - 1], fr[i]
                for b in set(A.t) | set(B.t):
                    da = abs(B.t.get(b, khung.ZERO)[2] - A.t.get(b, khung.ZERO)[2])
                    if da > 35.0:
                        xau.append(f"{i / 30:.2f}s {b} xoay {da:.0f}°")
            Wl = [sk.the_gioi(P) for P in fr]
            for b in ("bone13", "bone17", "bone20", "bone5", "bone10"):
                for i in range(1, len(fr)):
                    d = float(np.hypot(*(Wl[i][b][:2, 2] - Wl[i - 1][b][:2, 2])))
                    if d > 0.22 * cao:
                        xau.append(f"{i / 30:.2f}s {b} dời {d / cao:.2f} cao/khung")
            print(f"{c.ten}: {len(fr)} khung" + ("" if not xau else " | " + "; ".join(xau[:12]) + (" ..." if len(xau) > 12 else "")))
        return
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = nuong(sk, c)
        if ":" in a[2]:
            t0, t1, n = a[2].split(":")
            ts = list(np.linspace(float(t0), float(t1), int(n)))
        elif a[2].startswith("n="):
            ts = list(np.linspace(0, c.dur, int(a[2][2:])))
        else:
            ts = [float(x) for x in a[2].split(",")]
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve0.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 0.4
        cot = min(len(Ps), 6)
        hang = (len(Ps) + cot - 1) // cot
        out = None
        for i, P in enumerate(Ps):
            im = ve0.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB")
            d = ImageDraw.Draw(im)
            d.text((6, 4), f"{ts[i]:.2f}", fill=(255, 255, 255))
            if out is None:
                out = Image.new("RGB", (im.width * cot, im.height * hang), (150, 150, 150))
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    frames = {c.ten: nuong(sk, c) for c in clips if c.loop}
    xuat.xuat_het(sk, clips, RA, TEN, frames=frames, tieu_de="Rồng giáp sa thạch (rong_cat_1): tướng 4 đảo Thổ", dang=1, so_dang=1,
                  dung_yen=("cast", "skill"), lao=(), far=(), ma_goc=None, khop_idle=0.2, cao=cao, impact=IMPACT,
                  tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.3, tran_mb=0.5, span=3.6)


if __name__ == "__main__":
    main(sys.argv[1:])
