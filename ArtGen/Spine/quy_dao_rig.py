# -*- coding: utf-8 -*-
"""Quỷ lửa cầm đao lớn (quy_dao, tướng thứ 7 đảo Hỏa): RESKIN trên rig con gốc monster_3655 (quỷ lửa lưng gù vác kiếm khổng lồ).

- Xương: đủ mọi xương của họ, dáng gốc = khung 0 idle_01 (biến đổi riêng ĐÃ ÁP ràng buộc `l`, lấy mẫu bằng runtime Spine thật: IK hai
  chân, IK tay gần bám điểm trên vũ khí, vũ khí bám bàn tay xa (transform constraint) đều đã nướng thành FK).
- Hình: MỖI hình của họ một hình của mình, NGUYÊN lưới của họ (đỉnh, tam giác, uv, trọng số; điểm gắn theo ma trận dáng gốc att_goc.json).
  Mảnh đổi dáng (đao, sừng, mặt nạ, giáp vai, bờm lửa...) khai trong manh/dat_moi.json: ảnh của mình đặt "đúng chỗ, đúng cỡ", lưới dày của
  mình, mỗi đỉnh biến dạng như điểm tương ứng trên lưới của họ.
- Thứ tự vẽ: của họ. Họ đổi thứ tự vẽ trong clip (vũ khí + bàn tay xa ra trước chân / bờm / mặt / cả thân): slot "di động" được nhân bản ở
  từng chỗ chèn (tên `<slot>@<chỗ>`), mỗi khung bật đúng bản theo thứ tự vẽ của họ.
- Clip (người dùng dặn 2026-11-13):
    idle    KHÁC con gốc: thở chậm nặng (nhịp idle_01 kéo giãn), mỗi vòng một lần xốc đao trên vai rồi thả mũi đao xuống đất, bấu vuốt,
            lửa bờm bùng theo
    walk    KHÁC con gốc: VÁC ĐAO NGANG VAI mà bước (thân trên lấy dáng vác của skill_02, chân + hông của run_01)
    attack  vung đao chém NẶNG NỀ, impact lớn (skill_02: xốc đao lên vai chậm, gồng, bổ xuống nhanh, đao cắm đất, lôi về) + lao
    cast    giống skill_01, đổi nhẹ: giơ đao hai tay quá đầu, GỒNG tụ lửa (bờm bùng) rồi bổ cắm xuống đất
    skill   giống skill_04_1: LAO TỚI rồi liên hoàn chém như animation gốc, nhảy lên bổ xuống, lùi về
    appear  (tự làm) từ trên trời bổ đao xuống đất (đoạn rơi của skill_04), đứng dậy, dang tay gầm (dáng skill_03)
    die     (tự làm) die_01 của họ (bật ngửa, đao cắm đất, đổ sấp) + lửa bờm lụi dần, mờ dần
    hit     hit_01
    aura    lửa bờm + râu uốn lượn liên tục (lặp, phủ lên mọi clip)
- Vệt chém, lửa, bụi, nổ: VFX của game (rig chỉ đặt sự kiện + xương `mui_dao`, `than_dao`, `mieng`).

    quy_dao_rig.py                              dựng, xuất inbox/quy_dao_1/rig/
    quy_dao_rig.py soi <clip> <giây,..> [tỉ lệ]   khung lớn nền xám → rig/soi_<clip>.png
    quy_dao_rig.py kiem                         góc nhảy lớn nhất giữa hai khung của từng clip
  QD_GOC=1: dựng thử bằng DA GỐC (ảnh part của họ) vào rig_goc/ (kiểm rig trùng con gốc, làm clip trước khi có da).
Xương, lưới, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai."""
import json
import math
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import anh, hoat, xuat, soi  # noqa: E402
from quai.khung import Sk, goc_mat  # noqa: E402
from quai.hoat import Clip  # noqa: E402
from quai.luoi import Luoi, luoi_vung  # noqa: E402
import quy_dao as G  # noqa: E402

GOC = os.environ.get("QD_GOC") == "1"
TEN = os.environ.get("QD_TEN") or "quy_dao_1"
MANH = os.environ.get("QD_MANH") or os.path.join(G.BASE, "manh")
RA = os.environ.get("QD_RA") or os.path.join(G.BASE, "rig_goc" if GOC else "rig")
SCAN = G.scan()
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
AG = json.load(open(os.path.join(SCAN, "att_goc.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample.json"), encoding="utf-8"))
NB = [b["name"] for b in I["bones"]]
SL = [s["name"] for s in I["slots"]]
FPS = 30.0
WG = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0, 0, 1.0]]) for b in AG["bones"]}
L0 = S["idle_01"]["frames"][0]["l"]
ZERO5 = np.array([0, 0, 0, 1, 1.0])
USE = ["idle_01", "run_01", "skill_01_1", "skill_02_1", "skill_03", "skill_04_1", "hit_01", "die_01"]
BO_SLOT = {"shadow", "root"} | (set() if GOC else {"jiao_01", "jiao_02", "jiao_03", "jiao_04"})   # mào liền vào mặt nạ của mình
BOM = [["toufa_07", "toufa_08", "toufa_09"], ["toufa_03", "toufa_04", "toufa_05", "toufa_06"], ["toufa_02", "toufa_010", "toufa_011"],
       ["toufa_01", "toufa_012", "toufa_013", "toufa_017"], ["toufa_014", "toufa_015", "toufa_016"], ["huzi", "huzi2"]]
BOM_X = [b for ch in BOM for b in ch]
CAO = 760.0
# VỆT CHÉM dọc lưỡi đao (người dùng 2026-11-13: "thêm trail dọc lưỡi đao, trail cam mờ mờ thôi, kiểu thể hiện nhát chém splash")
VET_K, VET_DT = 10, 1.0 / 120.0          # số cột quá khứ, khoảng cách thời gian giữa hai cột (vệt dài ~0,08 s)
VET_V0, VET_V1 = 4500.0, 9500.0          # tốc độ mũi đao (đơn vị / giây) bắt đầu hiện / hiện đủ (idle, walk không tới ngưỡng)
VET_A = 0.42                             # độ đậm lớn nhất (cam mờ)
VET_HANG = ((0.40, -0.058), (0.60, -0.110), (0.80, -0.148), (0.93, -0.130), (1.0, -0.062))   # điểm dọc LƯỠI SẮC (u từ chuôi, v ngang; theo chiều dài đao)


# ---------------------------------------------------------------- thứ tự vẽ của họ: slot đứng yên + slot di động
def _thu_tu():
    base = list(S["idle_01"]["frames"][0]["o"])
    pos0 = {s: i for i, s in enumerate(base)}
    orders = []
    for c in USE:
        for F in S[c]["frames"]:
            o = tuple(F["o"])
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
    return stat, [s for s in base if s not in static]


STAT, DONG = _thu_tu()
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


def ten_ban(m, k):
    return SL[m] if k == NEO0[m] else f"{SL[m]}@{k}"


# ---------------------------------------------------------------- chuyển động của họ (mẫu khung)
def _cd():
    out = {}
    for clip in USE:
        v = S[clip]
        fr = v["frames"]
        res = {}
        for i, b0 in enumerate(I["bones"]):
            if b0["name"] == "root":
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
BAN = {m: sorted({c[m] for clip in USE for c, h in zip(CD[clip][3], CD[clip][2]) if h[m][0] is not None} | {NEO0[m]}) for m in DONG}


def mau(clip, t, lap=False, chi=None, tru=()):
    dur, R = CD[clip][0], CD[clip][1]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    out = {}
    for b, arr in R.items():
        if (chi is not None and b not in chi) or b in tru:
            continue
        n = len(arr)
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        out[b] = arr[i0] * (1 - w) + arr[i1] * w
    return out


def khung_ho(clip, t, lap=False):
    dur = CD[clip][0]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    return min(len(CD[clip][2]) - 1, int(round(x)))


def pha(a, b, w):
    out = {}
    for k in set(a) | set(b):
        out[k] = a.get(k, ZERO5) * (1 - w) + b.get(k, ZERO5) * w
    return out


def pha_gan(a, b, w):
    """như pha, nhưng góc của b quy về cùng vòng với a (góc đã nướng của clip họ cộng dồn nhiều vòng: pha thẳng thì tay quay tít)."""
    out = {}
    for k in set(a) | set(b):
        x, y = a.get(k, ZERO5), np.array(b.get(k, ZERO5), float)
        y[0] += 360.0 * round((x[0] - y[0]) / 360.0)
        out[k] = x * (1 - w) + y * w
    return out


TAY_XA = ("yao", "yao2", "shenti", "dabi_l", "xiaobi_l", "shou_l")      # chuỗi mang bàn tay xa (và đao bám theo nó)


def pha_tay(a, b, w):
    """pha_gan, thêm: nếu TỔNG góc quay của chuỗi tay xa (= góc đao quay trong thế giới) vượt nửa vòng thì cho bắp / cẳng tay quay chiều kia.
    Từng xương đi đường ngắn nhất nhưng cộng lại đao quay gần trọn vòng (288° trong 0,2 s lúc thu đao về): đổi chiều một xương thì đao gần
    như giữ hướng, cánh tay vòng qua phía trước đưa chuôi lên."""
    bb = {}
    for k in set(a) | set(b):
        y = np.array(b.get(k, ZERO5), float)
        y[0] += 360.0 * round((a.get(k, ZERO5)[0] - y[0]) / 360.0)
        bb[k] = y
    tong = sum(bb[k][0] - a.get(k, ZERO5)[0] for k in TAY_XA if k in bb)
    if abs(tong) > 180.0:
        dau = 1.0 if tong > 0 else -1.0
        k = max(("dabi_l", "xiaobi_l"), key=lambda q: dau * (bb.get(q, ZERO5)[0] - a.get(q, ZERO5)[0]))
        bb[k] = bb[k].copy()
        bb[k][0] -= dau * 360.0
    return {k: a.get(k, ZERO5) * (1 - w) + bb[k] * w for k in bb}


def cong(a, b, w=1.0, chi=None):
    """a + w · (b − dáng gốc): cộng thêm độ lệch của b (xoay, dời cộng; tỉ lệ nhân)."""
    out = dict(a)
    for k, v in b.items():
        if chi is not None and k not in chi:
            continue
        z = out.get(k, ZERO5)
        out[k] = np.array([z[0] + w * v[0], z[1] + w * v[1], z[2] + w * v[2], z[3] * (1 + w * (v[3] - 1)), z[4] * (1 + w * (v[4] - 1))])
    return out


def dat(P, d):
    for b, v in d.items():
        if abs(v[0]) > 1e-5:
            P.rot(b, float(v[0]))
        if abs(v[1]) > 1e-5 or abs(v[2]) > 1e-5:
            P.move(b, float(v[1]), float(v[2]))
        if abs(v[3] - 1) > 1e-6 or abs(v[4] - 1) > 1e-6:
            P.scale(b, float(v[3]), float(v[4]))


def em(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def u_(t, a, b):
    return em((t - a) / (b - a))


def bump(t, a, b, c, d):
    return em((t - a) / (b - a)) * (1 - em((t - c) / (d - c)))


def tq(t, bang):
    for (a_, x), (b_, y) in zip(bang, bang[1:]):
        if t <= b_:
            return x + (y - x) * (t - a_) / max(1e-9, b_ - a_)
    return bang[-1][1]


def tat_dan(t, t0, bien, tan, giam):
    """rung tắt dần sau t0."""
    if t < t0:
        return 0.0
    s = t - t0
    return bien * math.exp(-s / giam) * math.sin(2 * math.pi * tan * s)


def hien_theo_ho(sk, P, clip, t, lap=False):
    """độ đậm + hình của mọi slot theo khung của họ; slot di động bật đúng bản theo chỗ chèn (thứ tự vẽ) của họ ở khung đó."""
    i = khung_ho(clip, t, lap)
    hinh, cho = CD[clip][2][i], CD[clip][3][i]
    for k, sl in enumerate(SL):
        if sl in BO_SLOT or sl not in sk.si:
            continue
        n, a = hinh[k]
        if k in NEO0:
            for kk in BAN[k]:
                nm = ten_ban(k, kk)
                P.alpha[nm] = a if (n is not None and kk == cho[k]) else 0.0
                if n is not None and len(sk.atts[nm]) > 1:
                    P.att[nm] = n
        else:
            P.alpha[sl] = a if n is not None else 0.0
            if n is not None and len(sk.atts[sl]) > 1:
                P.att[sl] = n


# ---------------------------------------------------------------- dựng
def dung():
    sk = Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("far", "root", 0.9 * CAO + 140.0, 0.45 * CAO)
    for i, b in enumerate(I["bones"]):
        if b["name"] == "root":
            continue
        cha = NB[b["parent"]]
        z = L0[i]
        sk.xuong(b["name"], "move" if cha == "root" else cha, z[0], z[1], goc=z[2], dai=b["len"], sx=z[3], sy=z[4])
    Wi = sk.the_gioi()
    G._C.pop("att", None)
    _, imgs_ho, _ = G.nap("att_goc.json")
    hinh0 = CD["idle_01"][2][0]
    IM = {}

    def anh_cua(a):
        r = a["region"]
        if r not in IM:
            p = os.path.join(MANH, r + ".png")
            if os.path.exists(p) and not GOC:
                g = Image.open(p).convert("RGBA")
                k = float(os.environ.get("QD_PX") or 0.72) / 2.0             # ảnh mảnh = ảnh vùng × 2 (1 px / đơn vị) → 0,72 px / đơn vị
                g = g.convert("RGBa").resize((max(2, round(g.width * k)), max(2, round(g.height * k))), Image.LANCZOS).convert("RGBA")
            elif GOC or os.environ.get("QD_THIEU") == "1":                   # QD_THIEU=1: mảnh chưa có thì tạm lấy da gốc (chỉ để thử)
                g = G.part_goc(a)
            else:
                raise SystemExit(f"thiếu mảnh {p}")
            IM[r] = anh.loang_mau(g)
            sk.anh(r, IM[r])
        return IM[r]

    def hang(a, xy):
        ws = a.get("w")
        rows, V0 = [], []
        for i, p in enumerate(xy):
            lst = [(NB[b], w) for b, w in ws[i] if w > 0] if ws else [(a["bone"], 1.0)]
            tong = sum(w for _, w in lst)
            row, v0 = [], np.zeros(2)
            for bn, w in lst:
                bn2 = "move" if bn == "root" else bn
                lp = np.linalg.solve(WG[bn], np.array([p[0], p[1], 1.0]))
                row.append((bn2, float(lp[0]), float(lp[1]), float(w / tong)))
                v0 += w / tong * (Wi[bn2] @ np.array([lp[0], lp[1], 1.0]))[:2]
            rows.append(row)
            V0.append(v0)
        return rows, np.array(V0)

    def gan(slot_ten, a):
        """NGUYÊN lưới của họ với ảnh cùng khung ảnh vùng."""
        r = a["region"]
        im = anh_cua(a)
        wr, hr = imgs_ho[r].size
        uv_px, tris = G.luoi(a)
        xy = np.array(a["xy"], float).reshape(-1, 2)
        uv = uv_px / np.array([wr, hr], float)
        rows, V0 = hang(a, xy)
        tris = np.asarray(tris, int).reshape(-1, 3)
        sk.atts[slot_ten][a["att"]] = {"type": "mesh", "path": r, "uv": uv, "tris": tris, "hull": len(uv), "V": V0, "verts": rows,
                                       "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, a["att"])] = Luoi(uv * np.array([im.width, im.height], float), tris, len(uv), len(uv), im.width, im.height,
                                             ten=slot_ten)

    pm = os.path.join(MANH, "dat_moi.json")
    MOI = json.load(open(pm, encoding="utf-8")) if (os.path.exists(pm) and not GOC) else {}
    DAY = {}

    def gan_goc(slot_ten, a):
        """mảnh ĐỔI DÁNG: ảnh của mình đặt theo dat_moi.json {slot: {"anh", "goc": [x, y thế giới của góc trên trái ảnh], "ti": đơn vị / px
        ảnh nguồn, "px": px atlas / đơn vị, "buoc": bước lưới}}, lưới dày của mình; mỗi đỉnh bám xương b với W_b = Σ β_k w_b(k) và điểm gắn
        riêng q_b = Σ β_k w_b(k) l_kb / W_b (β: toạ độ trọng tâm trong tam giác của họ chứa đỉnh; nằm ngoài lưới của họ: bám như điểm gần
        nhất trên lưới, cộng nguyên khoảng lệch)."""
        d = MOI[a["slot"]]
        key = d.get("anh", a["slot"])
        if key not in DAY:
            g = Image.open(os.path.join(MANH, key + ".png")).convert("RGBA")
            k_px = float(d.get("px", 0.55))
            if "M" in d:                                          # phép đồng dạng ảnh nguồn (px, y xuống) → thế giới rig
                Mm = np.array(d["M"], float)
            else:
                ti = float(d["ti"])
                Mm = np.array([[ti, 0.0, d["goc"][0]], [0.0, -ti, d["goc"][1]]])
            ti = float(np.sqrt(abs(np.linalg.det(Mm[:, :2]))))    # đơn vị / px ảnh nguồn
            im = anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * ti * k_px)), max(2, round(g.height * ti * k_px))),
                                                         Image.LANCZOS).convert("RGBA"))
            sk.anh(key + "_moi", im)
            b_ = float(d.get("buoc", 26.0))
            L = luoi_vung(im, buoc_vien=b_ * k_px, buoc_trong=b_ * 1.5 * k_px, ten=key, in_tk=False)
            kx, ky = g.width / im.width, g.height / im.height
            V = np.array([Mm @ np.array([q[0] * kx, q[1] * ky, 1.0]) for q in np.asarray(L.pts, float)])
            rows_ho, Q = hang(a, np.array(a["xy"], float).reshape(-1, 2))
            _, tr = G.luoi(a)
            tr = np.asarray(tr, int).reshape(-1, 3)
            A, B_, C = Q[tr[:, 0]], Q[tr[:, 1]], Q[tr[:, 2]]
            v0, v1 = B_ - A, C - A
            den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
            den = np.where(np.abs(den) < 1e-9, 1e-9, den)

            def gan_canh(p, pa, pb):
                dd = pb - pa
                t = np.clip(((p - pa) * dd).sum(axis=1) / np.maximum((dd * dd).sum(axis=1), 1e-12), 0, 1)
                return np.hypot(*(p - (pa + t[:, None] * dd)).T), t

            # trọng số từng đỉnh: trong lưới của họ = nội suy trọng tâm; ngoài lưới (lưỡi lửa thò ra, viền nới) = của điểm gần nhất rồi LÀM TRƠN
            # theo cạnh lưới mình (đỉnh kề nhau rơi vào tam giác khác nhau của họ thì lưỡi lửa bị xé). Điểm gắn = một điểm chung (LBS thường).
            ten_x = sorted({bn for row in rows_ho for bn, _, _, _ in row})
            ix = {bn: i for i, bn in enumerate(ten_x)}
            Wt = np.zeros((len(V), len(ten_x)))
            la_ngoai = np.zeros(len(V), bool)
            ngoai, xa = 0, 0.0
            for vi_, p in enumerate(V):
                v2 = p - A
                b1 = (v2[:, 0] * v1[:, 1] - v2[:, 1] * v1[:, 0]) / den
                b2 = (v0[:, 0] * v2[:, 1] - v0[:, 1] * v2[:, 0]) / den
                b0 = 1 - b1 - b2
                ok = np.flatnonzero((b0 >= -1e-4) & (b1 >= -1e-4) & (b2 >= -1e-4))
                if len(ok):
                    i = int(ok[0])
                    be = (float(b0[i]), float(b1[i]), float(b2[i]))
                else:
                    ngoai += 1
                    la_ngoai[vi_] = True
                    best = None
                    for (pa, pb, ia, ib) in ((A, B_, 0, 1), (B_, C, 1, 2), (C, A, 2, 0)):
                        dist, t = gan_canh(p, pa, pb)
                        j = int(np.argmin(dist))
                        if best is None or dist[j] < best[0]:
                            w3 = [0.0, 0.0, 0.0]
                            w3[ia], w3[ib] = 1 - float(t[j]), float(t[j])
                            best = (float(dist[j]), j, tuple(w3))
                    dmin, i, be = best
                    xa = max(xa, dmin)
                for vk, bw in zip(tr[i], be):
                    for (bn, lx, ly, w) in rows_ho[vk]:
                        Wt[vi_, ix[bn]] += bw * w
            if la_ngoai.any() and len(ten_x) > 1:
                ke = [set() for _ in V]
                for t3 in np.asarray(L.tris, int):
                    for q in range(3):
                        ke[t3[q]].update((int(t3[(q + 1) % 3]), int(t3[(q + 2) % 3])))
                for _ in range(40):
                    Wn = Wt.copy()
                    for vi_ in np.flatnonzero(la_ngoai):
                        if ke[vi_]:
                            Wn[vi_] = 0.5 * Wt[vi_] + 0.5 * Wt[list(ke[vi_])].mean(0)
                    Wt = Wn
            rows = []
            for vi_, p in enumerate(V):
                w = Wt[vi_].copy()
                w[w < 0.02] = 0.0
                keep = np.argsort(-w)[:4]
                tong = w[keep].sum()
                row = []
                for k in keep:
                    if w[k] <= 0:
                        continue
                    lp = np.linalg.solve(Wi[ten_x[k]], np.array([p[0], p[1], 1.0]))
                    row.append((ten_x[k], float(lp[0]), float(lp[1]), float(w[k] / tong)))
                rows.append(row)
            V0 = np.array([sum(w * (Wi[bn] @ np.array([x, y, 1.0]))[:2] for bn, x, y, w in row) for row in rows])
            DAY[key] = (im, L, rows, V0)
            print(f"  {key}: lưới của mình {L.n} đỉnh, {ngoai} đỉnh ngoài lưới gốc (xa nhất {xa:.0f}), lệch dáng gốc {np.abs(V0 - V).max():.2f}")
        im, L, rows, V0 = DAY[key]
        sk.atts[slot_ten][a["att"]] = {"type": "mesh", "path": key + "_moi", "uv": np.asarray(L.pts, float) / np.array([im.width, im.height], float),
                                       "tris": np.asarray(L.tris, int), "hull": L.nh, "V": V0, "verts": rows, "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, a["att"])] = L

    by_slot = {}
    for a in AG["atts"]:
        if a["att"] == "lian_02":                 # bản lưới mặt thứ hai của họ: không clip nào dùng
            continue
        by_slot.setdefault(a["slot"], []).append(a)

    def them(slot_goc, ten, hien):
        ats = by_slot.get(slot_goc)
        if not ats:
            return
        mac = next((a for a in ats if a["cur"]), ats[0])
        sk.slot(ten, "move", mac["att"], an=not hien)
        for a in ats:
            (gan_goc if a["slot"] in MOI else gan)(ten, a)
        sk._slot(ten)["bone"] = sk.atts[ten][mac["att"]]["verts"][0][0][0]

    cho_chen = {}                                    # chỗ chèn -> [(thứ hạng trung bình, slot di động)]
    for m in DONG:
        for kk in BAN[m]:
            hang_ = [list(F["o"]).index(m) for c in USE for F in S[c]["frames"] if neo(F["o"], m) == kk]
            cho_chen.setdefault(kk, []).append((float(np.mean(hang_)) if hang_ else 0.0, m))
    for k in range(len(STAT) + 1):
        for _, m in sorted(cho_chen.get(k, [])):
            if SL[m] in BO_SLOT:
                continue
            them(SL[m], ten_ban(m, k), hien=(hinh0[m][0] is not None and k == NEO0[m]))
        if k < len(STAT):
            s_ = STAT[k]
            if SL[s_] in BO_SLOT:
                continue
            them(SL[s_], SL[s_], hien=hinh0[s_][0] is not None)

    # ---- xương cho VFX: mũi đao, giữa bản đao (con của xương vũ khí wuqi_03: trục x = chuôi → mũi), miệng (chỗ nhả của chiêu mana = mũi đao)
    Vd = np.array(next(a for a in AG["atts"] if a["slot"] == "wuqi_02")["xy"], float).reshape(-1, 2)
    mui = np.linalg.solve(WG["wuqi_03"], np.array([*((Vd[0] + Vd[3]) / 2), 1.0]))[:2]
    sk.xuong("mui_dao", "wuqi_03", float(mui[0]) * 0.97, float(mui[1]))
    sk.xuong("than_dao", "wuqi_03", float(mui[0]) * 0.62, float(mui[1]))
    sk.xuong("mieng", "move", 430.0, 40.0)                       # chỗ đao bổ xuống đất trước mặt (cast): lửa trào từ đây
    chuoi_g, mui_g = (Vd[1] + Vd[2]) / 2, (Vd[0] + Vd[3]) / 2
    Ld = float(np.linalg.norm(mui_g - chuoi_g))
    ax_g = (mui_g - chuoi_g) / Ld
    song_g = np.array([-ax_g[1], ax_g[0]])
    hang_loc = [np.linalg.solve(WG["wuqi_03"], np.array([*(chuoi_g + ax_g * (u * Ld) + song_g * (v * Ld)), 1.0])) for u, v in VET_HANG]
    Ww = Wi["wuqi_03"]
    x0, y0, r0 = float(Ww[0, 2]), float(Ww[1, 2]), goc_mat(Ww)
    sx0, sy0 = float(np.hypot(Ww[0, 0], Ww[1, 0])), float(np.hypot(Ww[0, 1], Ww[1, 1]))
    for k in range(1, VET_K + 1):
        sk.xuong(f"vet_{k}", "root", x0, y0, goc=r0, sx=sx0, sy=sy0)
    if not GOC:
        nr, nc = len(VET_HANG), VET_K + 1
        tw, th = 96, 64                                              # ảnh vệt: ngang = thời gian (trái: sát lưỡi đao → phải: đuôi), dọc = dọc lưỡi (trên: gần chắn tay → dưới: mũi)
        uu, vv = np.meshgrid(np.linspace(0, 1, tw), np.linspace(0, 1, th))
        al = (1.0 - uu) ** 1.25 * np.clip(vv / 0.22, 0, 1) ** 0.8 * np.clip((1.0 - vv) / 0.04, 0, 1)
        rgb = np.zeros((th, tw, 3), np.float32)
        rgb[...] = (247, 144, 42)
        sang = np.exp(-((vv - 0.86) / 0.07) ** 2) * (1.0 - uu) ** 0.6       # một vạch sáng hơn theo cung mũi đao
        rgb = rgb * (1 - sang[..., None]) + np.array([255, 208, 96], np.float32) * sang[..., None]
        al = np.clip(al * (1.0 + 0.5 * sang), 0, 1)
        sk.anh("vet", Image.fromarray(np.dstack([rgb, al * 255]).astype(np.uint8), "RGBA"))
        pts, V, W_ = [], [], []
        for c in range(nc):
            for r_ in range(nr):
                pts.append([1.0 + (tw - 2.0) * c / (nc - 1), 1.0 + (th - 2.0) * r_ / (nr - 1)])
                V.append((Ww @ hang_loc[r_])[:2])
                W_.append({("wuqi_03" if c == 0 else f"vet_{c}"): 1.0})
        tris = []
        for c in range(nc - 1):
            for r_ in range(nr - 1):
                a_, b_, c_, d_ = c * nr + r_, (c + 1) * nr + r_, (c + 1) * nr + r_ + 1, c * nr + r_ + 1
                tris += [[a_, b_, c_], [a_, c_, d_]]
        sk.slot("vet", "root", "vet", an=True)
        sk.luoi_gan("vet", "vet", Luoi(np.array(pts), np.array(tris), len(pts), len(pts), tw, th, ten="vet"), W_, the_gioi=np.array(V), ten="vet")
    for e, m in (("trung", "khung đòn trúng"), ("chem", "một nhát chém (vệt chém theo mui_dao / than_dao)"), ("nen", "đao bổ cắm xuống đất"),
                 ("tu", "gồng tụ lửa, bờm bùng"), ("lao", "bắt đầu lao tới"), ("nhay", "bật nhảy lên cao"), ("gam", "gầm"),
                 ("xoc", "xốc đao"), ("tat", "lửa bờm tắt"), ("nga", "đổ xuống đất"), ("buoc", "chân giậm đất")):
        sk.su_kien(e, m)
    tk = sk.tom_tat()
    off = np.linalg.inv(Wi["shou_l"]) @ Wi["wuqi_02"]
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao game {CAO:.0f}; slot di động: "
          + ", ".join(f"{SL[m]} {BAN[m]}" for m in DONG))
    return sk, dict(cao=CAO, off=off, vet=dict(mui=np.array([hang_loc[-1][0], hang_loc[-1][1], 1.0]), goc=(x0, y0, r0, sx0, sy0)))


# ---------------------------------------------------------------- tiện ích dáng
def dao_theo_tay(sk, info, P):
    """vũ khí bám CỨNG bàn tay xa (ràng buộc `wuq` của họ, mix 1): sau khi sửa thân / pha dáng thì tính lại biến đổi riêng của wuqi_02."""
    W = sk.the_gioi(P)
    Lm = np.linalg.inv(W["bone"]) @ (W["shou_l"] @ info["off"])
    b = sk.bones[sk.bi["wuqi_02"]]
    cu = P.t.get("wuqi_02", [0, 0, 0, 1, 1])[2]
    d = goc_mat(Lm) - b["rot"]
    d += 360.0 * round((cu - d) / 360.0)
    P.t["wuqi_02"] = [float(Lm[0, 2] - b["x"]), float(Lm[1, 2] - b["y"]), float(d), 1.0, 1.0]


def lua_bung(P, k, rung=0.0, t=0.0):
    """bờm lửa to lên k lần (đốt gốc mỗi búi), rung nhanh."""
    for i, ch in enumerate(BOM):
        s = 1.0 + (k - 1.0) * (0.6 if ch[0] == "huzi" else 1.0)
        P.scale(ch[0], s, s)
        if rung:
            for j, b in enumerate(ch):
                P.rot(b, rung * math.sin(2 * math.pi * 11.0 * t + 1.7 * i + 0.9 * j))


def mo_dan(sk, P, a):
    if a < 1.0:
        for sl in sk.slots:
            P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])


class VetDao:
    """hậu kỳ: VỆT CHÉM. Cột k của dải lưới bám xương vet_k = biến đổi thế giới của xương vũ khí ở k · VET_DT giây TRƯỚC (tính lại dáng bằng
    hàm của clip, kể cả phần lao của xương move: vệt nằm lại chỗ đao vừa đi qua). Đao đứng yên thì các cột trùng nhau (dải không có diện tích).
    Độ đậm theo tốc độ mũi đao lớn nhất trong cửa sổ vệt: chỉ hiện ở nhát chém nhanh, tự tan khi các cột dồn về lưỡi đao đã dừng."""

    def __init__(self, clip, info, khoang=None):
        self.clip, self.v, self.khoang = clip, info["vet"], khoang      # khoang (t0, t1): chỉ hiện vệt trong đoạn này (nhát chém), ngoài ra tắt

    def chay(self, sk, frames, ts, loop, fps):
        from quai.khung import Pose as _P
        if "vet" not in sk.si:
            return
        c, dur = self.clip, self.clip.dur
        nho = {}

        def W(t):
            t = (t % dur) if loop else min(max(t, 0.0), dur)
            k = int(round(t * 240))
            if k not in nho:
                P = _P()
                c.fn(k / 240.0, P)
                nho[k] = sk.the_gioi(P)["wuqi_03"]
            return nho[k]

        x0, y0, r0, sx0, sy0 = self.v["goc"]
        mui = self.v["mui"]
        am = []
        for t in ts:
            tips = [(W(t - k * VET_DT) @ mui)[:2] for k in range(VET_K + 2)]
            vmax = max(float(np.hypot(*(tips[k] - tips[k + 1]))) / VET_DT for k in range(VET_K + 1))
            a_ = VET_A * em((vmax - VET_V0) / (VET_V1 - VET_V0))
            if self.khoang:
                a_ *= bump(t, self.khoang[0] - 0.05, self.khoang[0], self.khoang[1], self.khoang[1] + 0.08)
            am.append(a_)
        n = len(frames)
        for i, (t, P) in enumerate(zip(ts, frames)):
            gan_ = max(am[max(0, i - 1):min(n, i + 2)])               # đặt xương sớm / muộn một khung quanh lúc vệt hiện (khỏi vệt bay từ dáng gốc tới)
            P.alpha["vet"] = am[i]
            if gan_ <= 0.0:
                continue
            for k in range(1, VET_K + 1):
                M = W(t - k * VET_DT)
                P.t[f"vet_{k}"] = [float(M[0, 2] - x0), float(M[1, 2] - y0), goc_mat(M) - r0,
                                   float(np.hypot(M[0, 0], M[1, 0]) / sx0), float(np.hypot(M[0, 1], M[1, 1]) / sy0)]


class GoVong:
    """hậu kỳ: góc đã nướng của clip họ cộng dồn nhiều vòng (tay quay tròn trong liên hoàn chém); chỗ mình nối sang dáng khác thì lệch đúng
    bội 360° trong MỘT khung (runtime sẽ quay tít một vòng) → dời cả phần sau về cùng vòng."""

    def chay(self, sk, frames, ts, loop, fps):
        lech = {}
        for p, q in zip(frames, frames[1:]):
            for b in set(q.t) | set(lech):
                v = q._g(b)
                v[2] += lech.get(b, 0.0)
                d = v[2] - p.t.get(b, [0, 0, 0, 1, 1])[2]
                if abs(d) > 180.0:
                    k = -360.0 * round(d / 360.0)
                    v[2] += k
                    lech[b] = lech.get(b, 0.0) + k


# ---------------------------------------------------------------- clip
def lam_clip(sk, info):
    out = []
    cao = info["cao"]
    i_yao, i_b2 = NB.index("yao"), NB.index("bone2")

    def ho(P, clip, u, lap=False, d=None):
        dat(P, d if d is not None else mau(clip, u, lap))
        hien_theo_ho(sk, P, clip, u, lap)

    def nang_ho(clip, u):
        """độ nhấc thân (hông) của họ so với dáng đứng ở giây u, và độ trôi ngang của bone2."""
        fr = S[clip]["frames"]
        x = min(max(u, 0.0), CD[clip][0]) * FPS
        i0 = min(int(x), len(fr) - 1)
        i1 = min(i0 + 1, len(fr) - 1)
        w = x - i0
        y = fr[i0]["b"][i_yao][1] * (1 - w) + fr[i1]["b"][i_yao][1] * w
        bx = fr[i0]["b"][i_b2][0] * (1 - w) + fr[i1]["b"][i_b2][0] * w
        return y - S["idle_01"]["frames"][0]["b"][i_yao][1], bx

    # ---- AURA: lửa bờm + râu uốn lượn liên tục (sóng chạy gốc → ngọn, lệch pha giữa các búi, phập phồng nhẹ)
    D_AU = 4.0

    def aura(t, P):
        om = 2 * math.pi / 1.0
        for i, ch in enumerate(BOM):
            ph = i * 1.37
            rau = ch[0] == "huzi"
            for j, b in enumerate(ch):
                a = (1.6 + 1.5 * j) * math.sin(om * t + ph - 0.9 * j) + (0.7 + 0.5 * j) * math.sin(2 * om * t + 1.3 * ph - 0.7 * j)
                P.rot(b, a * (0.7 if rau else 1.0))
            s = 1.0 + 0.035 * math.sin(2 * om * t + 0.7 * ph) + 0.02 * math.sin(3 * om * t + ph)
            P.scale(ch[-1], s, 1.0 + (s - 1.0) * 0.4)
    out.append(Clip("aura", D_AU, aura, loop=True))

    # ---- IDLE (khác con gốc): thở chậm nặng: nhịp idle_01 kéo giãn 1,5 lần, biên độ × 1,25; mỗi vòng một lần XỐC ĐAO trên vai (mũi đao nhấc
    # khỏi đất rồi thả xuống), bấu vuốt tay gần, đầu gườm; lửa bờm bùng theo cú xốc
    D_ID = 4.0
    X0, X1, X2, X3 = 1.95, 2.30, 2.62, 2.80
    xoc_dang = mau("skill_02_1", 0.15)
    NGON = ["shouzhi_02", "shouzhi_03", "shouzhi_04", "shouzhi_05", "shouzhi_06", "shouzhi_07", "shouzhi_08", "shouzhi_09", "shouzhi_010"]

    def idle(t, P):
        d = pha({}, mau("idle_01", t * (2 * CD["idle_01"][0] / D_ID), True), 1.25)
        w = 0.62 * (em((t - X0) / (X1 - X0)) - em((t - X2) / (X3 - X2))) if t < X3 else 0.0
        w += tat_dan(t, X3, -0.10, 3.2, 0.16)                    # thả đao: nảy tắt dần
        d = pha(d, xoc_dang, w)
        dat(P, d)
        hien_theo_ho(sk, P, "idle_01", 0.0)
        g = bump(t, 0.45, 0.75, 1.25, 1.6)                        # bấu vuốt
        for i, b in enumerate(NGON):
            P.rot(b, -13.0 * g * (0.6 + 0.4 * math.sin(2 * math.pi * (t - 0.45) / 0.5 - 0.5 * (i // 2))))
        P.rot("lian_01", 5.0 * bump(t, 2.9, 3.2, 3.5, 3.85) - 3.0 * w)
        lua_bung(P, 1.0 + 0.16 * bump(t, X0 + 0.1, X1, X2, X3 + 0.3))
        dao_theo_tay(sk, info, P)
    out.append(Clip("idle", D_ID, idle, loop=True, ev=[(X0, "xoc", "")]))

    # ---- WALK (khác con gốc): XỐC ĐAO LÊN VAI mà bước nặng. Chân, hông, thân: run_01 của họ; tay xa nâng cao cho bản đao rời đất, nằm
    # gần ngang sau đầu (họ kéo đao thấp sau lưng), đao nảy theo từng bước giậm; tay gần đánh mạnh, ngực ưỡn hơn; đao tính lại theo bàn tay xa
    D_W = CD["run_01"][0]
    BUOC = (0.02, 0.76)                                           # hai lần bàn chân giậm đất trong một vòng run_01

    def walk(t, P):
        dat(P, mau("run_01", t, True))
        hien_theo_ho(sk, P, "run_01", t, True)
        ph = 2 * math.pi * t / D_W
        nay = sum(math.exp(-((t - b0) % D_W) / 0.10) for b0 in BUOC)          # nảy sau mỗi bước giậm
        P.rot("dabi_l", 27.0 + 4.0 * math.sin(2 * ph + 0.4) - 3.5 * nay)       # xốc đao lên vai, nảy theo bước
        P.rot("xiaobi_l", 6.0)
        P.rot("shenti", -4.0 + 1.6 * math.sin(2 * ph + 1.2))
        P.rot("lian_01", 3.0 - 2.0 * nay)
        P.rot("dabi_r", 9.0 * math.sin(ph + 0.6))                 # tay gần đánh theo bước
        P.rot("xiaobi_r", 7.0 * math.sin(ph + 0.1))
        P.move("move", 0.0, -5.0 * nay)
        lua_bung(P, 1.0 + 0.05 * nay)
        dao_theo_tay(sk, info, P)
    out.append(Clip("walk", D_W, walk, loop=True, ev=[(b0, "buoc", "") for b0 in BUOC]))

    def hit(t, P):
        ho(P, "hit_01", t)
    out.append(Clip("hit", CD["hit_01"][0], hit))

    # ---- ATTACK: chém NẶNG NỀ, impact lớn. Bản đầu dựng trên skill_02 (xốc đao lên vai rồi bổ): bản đao nằm khuất sau thân suốt cú bổ, không
    # thấy "vung". Đổi sang nhát bổ CỐI XAY của skill_04 (u 0,58 → 1,0): giơ đao dựng đứng lên cao → quay một vòng nặng nề ra sau lưng → bổ qua
    # đầu xuống trước mặt (bản đao lộ trọn, quét từ sau ra trước) → đao ghì sát đất, khựng → lôi về. Vào / ra dáng bằng pha từ / về idle.
    UA0, UA1, UA2, UA3, UA4 = 0.585, 0.67, 25 / 30, 26 / 30, 1.0      # cú bổ của họ là MỘT khung nhảy bậc (25 → 26): giãn đúng đoạn đó ra 0,08 s
    TA0, TA1, TA2, A_TR, TA4, TA5, D_AT = 0.34, 0.52, 0.84, 0.92, 1.22, 1.50, 1.90
    UV0 = 0.90                                                    # thu về: pha sang dáng đao ghì trước mặt của skill_02 rồi chạy đoạn thu về của nó
    X_AT = 0.50 * cao

    def attack(t, P):
        clip, lap_u = "skill_04_1", None
        if t < TA0:
            u, w = UA0, em(t / TA0)
            d = pha_gan({}, mau("skill_04_1", UA0), w)
        elif t < TA4:
            u, w = tq(t, [(TA0, UA0), (TA1, UA1), (TA2, UA2), (A_TR, UA3), (TA4, UA4)]), 1.0
            d = mau("skill_04_1", u)
        elif t < TA5:
            w2 = em((t - TA4) / (TA5 - TA4))
            u, w = UA4, 1.0
            d = pha_tay(mau("skill_04_1", UA4), mau("skill_02_1", UV0), w2)
            if w2 > 0.5:
                clip, u = "skill_02_1", UV0
        else:
            clip, w = "skill_02_1", 1.0
            u = tq(t, [(TA5, UV0), (D_AT, CD["skill_02_1"][0])])
            d = mau("skill_02_1", u)
        if "bone2" in d:                                          # họ trôi tới 194–237 đơn vị trong đoạn này: bỏ (xương move lo phần lao)
            d["bone2"] = np.array([d["bone2"][0], 0.0, d["bone2"][2], d["bone2"][3], d["bone2"][4]])
        dat(P, d)
        hien_theo_ho(sk, P, clip if w > 0.5 else "idle_01", u if w > 0.5 else 0.0)
        dao_theo_tay(sk, info, P)
        gong = bump(t, TA0 - 0.06, TA0 + 0.08, TA2 - 0.04, TA2 + 0.04)
        x = X_AT * (0.25 * u_(t, TA0, TA2) + 0.75 * u_(t, TA2 - 0.06, A_TR)) * (1.0 - u_(t, TA5, D_AT - 0.06))
        P.move("move", x + 2.2 * gong * math.sin(2 * math.pi * 13 * t) + tat_dan(t, A_TR, 11.0, 15.0, 0.11), tat_dan(t, A_TR, -9.0, 13.0, 0.10))
        nen = math.exp(-max(0.0, t - A_TR) / 0.08) if t >= A_TR else 0.0
        P.scale("move", 1.0 + 0.06 * nen, 1.0 - 0.08 * nen)
        lua_bung(P, 1.0 + 0.16 * gong + 0.26 * nen, rung=2.2 * gong, t=t)
    out.append(Clip("attack", D_AT, attack, ev=[(TA0, "xoc", ""), (TA2, "chem", ""), (A_TR, "nen", ""), (A_TR, "trung", "")], trung=A_TR))

    # ---- CAST (giống skill_01, đổi nhẹ): xốc đao, nắm hai tay, giơ quá đầu → GỒNG tụ lửa 0,4 s (run, bờm bùng) → bổ cắm xuống đất → giữ
    # (lửa trào theo đất: VFX) → rút đao về
    TCa = [(0.0, 0.0), (0.50, 0.62), (0.64, 0.79), (1.04, 0.81), (1.14, 0.93), (1.60, 1.26), (2.15, CD["skill_01_1"][0])]
    C_TU, C_TR, D_CA = 0.60, 1.14, 2.15

    def cast(t, P):
        u = tq(t, TCa)
        ho(P, "skill_01_1", u)
        tu = bump(t, C_TU, 0.76, 1.00, 1.08)
        nen = math.exp(-max(0.0, t - C_TR) / 0.08) if t >= C_TR else 0.0
        P.move("move", 2.6 * tu * math.sin(2 * math.pi * 14 * t) + tat_dan(t, C_TR, 10.0, 14.0, 0.12), tat_dan(t, C_TR, -9.0, 12.0, 0.10))
        P.scale("move", 1.0 + 0.06 * nen - 0.012 * tu, 1.0 - 0.08 * nen + 0.02 * tu)
        lua_bung(P, 1.0 + 0.30 * tu * (0.5 + 0.5 * u_(t, C_TU, 1.0)) + 0.25 * nen, rung=3.0 * tu, t=t)
    out.append(Clip("cast", D_CA, cast, ev=[(C_TU, "tu", ""), (1.04, "chem", ""), (C_TR, "nen", ""), (C_TR, "trung", "")], trung=C_TR))

    # ---- SKILL (giống skill_04_1): thu người → LAO TỚI → liên hoàn chém của họ → đâm → bật nhảy cao → bổ xuống (đòn kết) → lùi về
    U_NEN = 1.87
    U_VE0 = 2.12
    D_SK = U_VE0 + 0.55
    X_SK = 0.62 * cao
    CHEM = (0.30, 0.42, 0.60, 0.74, 0.86, 0.98, 1.24)
    NEN_CAO = 0.50                                                # giữ lại chừng này độ cao cú nhảy của họ (họ nhảy vọt khỏi khung)

    def u_sk(t):
        return t if t < U_VE0 else U_VE0 + (t - U_VE0) * (CD["skill_04_1"][0] - U_VE0) / (D_SK - U_VE0)

    def skill(t, P):
        u = u_sk(t)
        ho(P, "skill_04_1", u)
        nang, bx = nang_ho("skill_04_1", u)
        x = X_SK * u_(t, 0.10, 0.28) * (1.0 - u_(t, U_VE0 + 0.05, D_SK - 0.08))
        nen = math.exp(-max(0.0, t - U_NEN) / 0.09) if t >= U_NEN else 0.0
        P.move("move", x + tat_dan(t, U_NEN, 13.0, 13.0, 0.13), tat_dan(t, U_NEN, -11.0, 11.0, 0.11))
        P.scale("move", 1.0 + 0.07 * nen, 1.0 - 0.09 * nen)
        P.move("bone", -0.6 * bx, -(1.0 - NEN_CAO) * max(0.0, nang - 120.0))
        lua_bung(P, 1.0 + 0.16 * bump(t, 0.0, 0.12, 1.3, 1.5) + 0.30 * nen)
    out.append(Clip("skill", D_SK, skill, ev=[(0.10, "lao", "")] + [(c, "chem", "") for c in CHEM] + [(1.38, "nhay", ""), (U_NEN, "nen", ""),
                                                                                                  (U_NEN, "trung", "")], trung=U_NEN))

    # ---- APPEAR (tự làm): từ trên trời BỔ ĐAO xuống đất (đoạn rơi + cắm đao của skill_04), đứng dậy, dang tay GẦM (dáng skill_03), về thế
    U_A0 = 1.755
    T_NEN = 0.27                                                  # rơi 0,27 s (họ rơi 0,115 s: nhanh quá, chưa kịp thấy), nhanh dần
    T_DAY0, T_DAY1 = 0.62, 1.04                                   # rút đao đứng dậy (u 2,12 → 2,43)
    T_G0, T_G1, T_G2, D_AP = 1.24, 1.74, 1.84, 2.32               # dang tay gầm; về thế (skill_03 u 2,02 → 2,47)
    gam_dang = mau("skill_03", 1.0)

    def appear(t, P):
        if t < T_DAY1:
            if t < T_NEN:
                u = U_A0 + (U_NEN - U_A0) * (t / T_NEN) ** 1.7
            else:
                u = tq(t, [(T_NEN, U_NEN), (T_NEN + 0.05, U_NEN + 0.05), (T_DAY0, U_VE0), (T_DAY1, CD["skill_04_1"][0])])
            ho(P, "skill_04_1", u)
            nang, _ = nang_ho("skill_04_1", u)
            P.move("bone", 0.0, -0.42 * max(0.0, nang - 120.0))
        elif t < T_G2:
            w = u_(t, T_DAY1, T_G0)
            d = pha({}, gam_dang, w)
            dat(P, d)
            hien_theo_ho(sk, P, "skill_03" if w > 0.5 else "idle_01", 1.0 if w > 0.5 else 0.0)
            dao_theo_tay(sk, info, P)
        else:
            ho(P, "skill_03", tq(t, [(T_G2, 2.02), (D_AP, CD["skill_03"][0])]))
        nen = math.exp(-max(0.0, t - T_NEN) / 0.09) if t >= T_NEN else 0.0
        gam = bump(t, T_G0 - 0.05, T_G0 + 0.08, T_G1, T_G2)
        P.move("move", tat_dan(t, T_NEN, 14.0, 13.0, 0.13) + 2.4 * gam * math.sin(2 * math.pi * 15 * t), tat_dan(t, T_NEN, -12.0, 11.0, 0.11))
        P.scale("move", 1.0 + 0.07 * nen, 1.0 - 0.09 * nen)
        lua_bung(P, 1.0 + 0.3 * nen + 0.32 * gam, rung=3.0 * gam, t=t)
        P.rot("lian_01", 7.0 * gam)
        mo_dan(sk, P, min(1.0, t / 0.08))
    out.append(Clip("appear", D_AP, appear, ev=[(T_NEN, "nen", ""), (T_G0, "gam", "")]))

    # ---- DIE (tự làm): die_01 của họ (bật ngửa, đao cắm đất, đổ sấp) + lửa bờm lụi dần, tắt; mờ dần
    T_BAT = 0.10                                                  # khung đầu của họ bật ngửa tức thì (300 đơn vị trong một khung): giãn ra 0,10 s
    D_DIE = CD["die_01"][0] + 0.75 + (T_BAT - 1 / FPS)

    def die(t, P):
        u = (1 / FPS) * em(t / T_BAT) ** 0.8 if t < T_BAT else t - (T_BAT - 1 / FPS)
        ho(P, "die_01", min(u, CD["die_01"][0]))
        lui = em((t - 0.50) / 0.75)
        lua_bung(P, 1.0 - 0.72 * lui)
        for ch in BOM:
            P.scale(ch[-1], 1.0 - 0.5 * lui, 1.0 - 0.5 * lui)
        mo_dan(sk, P, 1.0 - em((t - (D_DIE - 0.35)) / 0.35))
    out.append(Clip("die", D_DIE, die, ev=[(0.69, "nga", ""), (1.20, "tat", "")]))
    for c in out:
        kh = {"attack": (0.60, 1.15), "cast": (0.95, 1.45), "skill": None, "appear": (0.0, 0.50)}      # vệt chỉ ở nhát chém, không ở lúc xốc / thu đao
        c.mem = list(c.mem) + ([VetDao(c, info, kh[c.ten])] if c.ten in kh else []) + [GoVong()]
    return out


def main(a):
    sk, info = dung()
    clips = lam_clip(sk, info)
    if a and a[0] == "kiem":
        for c in clips:
            fr = hoat.nuong(sk, c)
            xau = {}
            for p, q in zip(fr, fr[1:]):
                for bn in set(p.t) | set(q.t):
                    d = abs(q.t.get(bn, [0, 0, 0, 1, 1])[2] - p.t.get(bn, [0, 0, 0, 1, 1])[2])
                    xau[bn] = max(xau.get(bn, 0), d)
            lon = sorted(((v, k) for k, v in xau.items() if v > 40), reverse=True)[:6]
            print(f"{c.ten:7s} bước xoay lớn nhất mỗi khung: " + (", ".join(f"{k} {v:.0f}°" for v, k in lon) or "không xương nào quá 40°"))
        return
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        au = hoat.nuong(sk, [x for x in clips if x.ten == "aura"][0])
        if c.ten != "aura":
            fr = hoat.phu_aura(fr, au, sk)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 0.3
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB") for P in Ps]
        cot = min(len(ims), 6)
        hang_ = (len(ims) + cot - 1) // cot
        o = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang_), (150, 150, 150))
        for i, im in enumerate(ims):
            o.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        o.save(pth)
        print(pth, o.size)
        return
    xuat.xuat_het(sk, clips, RA, TEN, "Quỷ lửa cầm đao (quy_dao_1)" + (" · DA GỐC (thử rig)" if GOC else ""), dang=1, so_dang=1,
                  dung_yen=("cast",), lao=("attack", "skill"), far=(), cao=info["cao"], ma_goc=None,
                  tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2,
                  impact={"attack": (0.10, 0.55, 0.14), "skill": (0.22, 1.0, 0.20, "#ffb04066")},
                  plain=["vet"] if "vet" in sk.si else None)


if __name__ == "__main__":
    main(sys.argv[1:])
