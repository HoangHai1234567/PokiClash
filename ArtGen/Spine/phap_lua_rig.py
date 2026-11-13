# -*- coding: utf-8 -*-
"""Pháp sư lửa (phap_lua, tướng thứ 6 đảo Hỏa): RESKIN trên rig con gốc monster_3481 (pháp sư bóng ma cầm trượng mắt).

- Xương: đủ mọi xương của họ, dáng gốc = khung 0 idle_01 (biến đổi riêng `l`, lấy mẫu bằng runtime Spine thật; rig FK thuần).
- Hình: MỖI hình của họ một hình của mình, NGUYÊN lưới của họ (đỉnh, tam giác, uv, trọng số; điểm gắn theo ma trận dáng gốc trong att_goc.json).
- Thứ tự vẽ: của họ. Họ đưa trượng + bốn ngón tay trượng ra TRƯỚC tay vuốt (skill_02 từ 0,80 s; skill_03, die: bản trượng thả rời `wuqi2`)
  → các slot đó có thêm bản `_t` ở trên cùng, bật theo thứ tự vẽ từng khung của họ.
- TRƯỢNG tách lớp (con gốc: một ảnh liền con mắt): khói → lưỡi lửa (lưới + chuỗi 3 xương, uốn lượn liên tục) → cầu lửa → tim lửa → khung
  trượng. Nhóm cầu lửa nằm trên `cau_goc` (con của `fly_cau`, con của root): mỗi khung đặt vào đúng đầu trượng nhưng KHÔNG xoay theo
  trượng (lửa luôn bốc lên trời, ngả ngược chiều bay). Lửa uốn + khói bốc chạy trong clip lặp `aura` (liền qua mọi clip).
- Bàn tay thứ 2 của họ (hiện ra chỗ đối thủ, clip skill_01_1) bám xương `far`: game dời `far` tới đối thủ.
- Clip: idle, walk = của họ + sửa khác chút; hit = của họ; attack = skill_01 + skill_01_1; cast = skill_02; skill = skill_03 kéo dài (cầu lửa
  tách khỏi trượng bay lên, hút lửa lớn dần; mốc `ban_cau` thì biến mất: đoạn bay tới đối thủ do CODE làm, người dùng dặn 2026-11-13);
  appear = bay vào; die = die_01 + cầu lửa tắt.
- Kim lửa, lửa bị hút về, vệt cầu lửa, nổ: VFX của game (rig chỉ đặt sự kiện).

    phap_lua_rig.py                          dựng, xuất inbox/phap_lua_1/rig/
    phap_lua_rig.py soi <clip> <giây,..> [tỉ lệ]   khung lớn nền xám → rig/soi_<clip>.png
    phap_lua_rig.py kiem                     góc nhảy lớn nhất giữa hai khung của từng clip
  PL_MANH=<thư mục mảnh> (mặc định manh/; thử bằng da gốc: manh_goc/), PL_RA=<thư mục ra>.
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
from quai.khung import Sk, mat, goc_mat, Pose, Dat  # noqa: E402
from quai.hoat import Clip, LoXo  # noqa: E402
from quai.luoi import Luoi, luoi_vung  # noqa: E402
import phap_lua as G  # noqa: E402
import phap_lua_da as DA  # noqa: E402

TEN = os.environ.get("PL_TEN") or "phap_lua_1"
MANH = os.environ.get("PL_MANH") or os.path.join(G.BASE, "manh")
RA = os.environ.get("PL_RA") or os.path.join(G.BASE, "rig")
SCAN = G.scan()
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
AG = json.load(open(os.path.join(SCAN, "att_goc.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample.json"), encoding="utf-8"))
NB = [b["name"] for b in I["bones"]]
SL = [s["name"] for s in I["slots"]]
FPS = 30.0
WG = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0, 0, 1.0]]) for b in AG["bones"]}
L0 = S["idle_01"]["frames"][0]["l"]
B0 = S["idle_01"]["frames"][0]["b"]
ZERO5 = np.array([0, 0, 0, 1, 1.0])

TAY_R = ("shouzhiR_04", "shouzhiR_03", "shouzhiR_02", "shouzhiR_01")       # bốn ngón tay trượng (theo thứ tự vẽ)
DOI = ("wuqi",) + TAY_R                                                     # slot có bản _t (trượng ra trước tay vuốt)
TAY2 = ["bone103", "bone104"] + [f"bone{i}" for i in range(72, 87)]         # chuỗi bàn tay thứ 2 (hiện ra chỗ đối thủ)
N_LUA, N_KHOI = 4, 5
PX_CAU = 1.35                  # px atlas cho mỗi đơn vị của nhóm cầu lửa (chiêu cuối phóng to 2,4 lần)
# lưỡi lửa: (gốc x, y theo bán kính cầu tính từ tâm; cao theo bán kính; ngả độ, dương = sang trái)
LUA = [(0.15, 0.10, 3.3, 6.0), (-0.55, 0.0, 2.5, 16.0), (0.50, -0.05, 1.9, -9.0), (0.20, 0.25, 1.4, -2.0)]
KEM, BO = {}, set()            # dung() điền: slot mới → slot của họ mà nó theo độ đậm; slot của họ không dựng (đã thay bằng mảnh của mình)
LOP = {"pifeng_03": [("lua_ao", "lua_ao"), ("pifeng_03", "ao")], "pifeng_02": [("pifeng_02", "vai_trai")], "pifeng_01": [("pifeng_01", "vai_phai")],
       "maofa_01": [("maofa_01", "toc")]}
# áo của mình hình chuông, không có cái đuôi nhọn chìa sang phải của áo gốc: phần lưới rơi vào tam giác của đuôi đó không theo hai đốt đuôi
GOP = {"pifeng_03": {"bone49": "bone36", "bone41": "bone36"}, "lua_ao": {"bone49": "bone36", "bone41": "bone36"}}
XUONG_AO = ("bone25", "bone26", "bone27", "bone28", "bone31", "bone36", "bone32", "bone33", "bone34", "bone35", "bone37", "bone38", "bone39", "bone40")
DAU = ("tou_05", "tou_04", "tou_03", "tou_02", "tou_01")       # năm mảnh đầu của họ (cùng xương bone6) → một mảnh đầu mũ trùm của mình
NHOM = [f"khoi_{i}" for i in range(N_KHOI)] + [f"lua_{k}" for k in (1, 2, 0, 3)] + ["cau", "tim"]     # sau → trước


# ---------------------------------------------------------------- chuyển động của họ (mẫu khung)
def _cd():
    out = {}
    i_w, i_w2, i_tay = SL.index("wuqi"), SL.index("wuqi2"), SL.index("shouzhangL_01")
    for clip, v in S.items():
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
        tren, truong = [], []
        for F in fr:
            k = i_w2 if F["n"][i_w2] else i_w
            tren.append(F["o"].index(k) > F["o"].index(i_tay))
            truong.append("bone102" if F["n"][i_w2] else "bone56")
        hien = [[(F["n"][k] is not None) * float(F["a"][k]) for k in range(len(SL))] for F in fr]
        out[clip] = (float(v["dur"]), res, tren, hien, truong)
    return out


CD = _cd()


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
    """0 → 1 (a..b) giữ → 0 (c..d)."""
    return em((t - a) / (b - a)) * (1 - em((t - c) / (d - c)))


def tq(t, bang):
    for (a_, x), (b_, y) in zip(bang, bang[1:]):
        if t <= b_:
            return x + (y - x) * (t - a_) / (b_ - a_)
    return bang[-1][1]


def hien_theo_ho(P, clip, t, lap=False, chi=None, tru=(), ep_goc=False):
    """độ đậm mọi slot theo khung của họ; trượng + bốn ngón tay trượng bật bản gốc hay bản _t theo thứ tự vẽ của họ ở khung đó. Trả
    (xương trượng đang hiện, trượng ở trên cùng?)."""
    i = khung_ho(clip, t, lap)
    _, _, tren, hien, truong = CD[clip]
    tr = tren[i] and not ep_goc          # ep_goc: 0,2 s cuối clip (đoạn hoà về idle) dùng sẵn bản gốc, kẻo hai bản cùng mờ nửa chừng
    for k, sl in enumerate(SL):
        if sl == "shadow" or (chi is not None and sl not in chi) or sl in tru:
            continue
        a = hien[i][k]
        if sl in DOI:
            P.alpha[sl] = 0.0 if tr else a
            P.alpha[sl + "_t"] = a if tr else 0.0
        else:
            P.alpha[sl] = a
    for moi_, nguon in KEM.items():                  # slot của mình đi kèm một slot của họ (khối lửa dưới áo, đầu mũ trùm)
        if nguon in P.alpha:
            P.alpha[moi_] = P.alpha[nguon]
    for sl in BO:
        P.alpha.pop(sl, None)
    return truong[i], tr


# ---------------------------------------------------------------- dựng
def truc_lua(im):
    """trục một lưỡi lửa trên ảnh (px): gốc (giữa đáy), hai điểm giữa, ngọn (điểm cao nhất, lùi vào 8%)."""
    a = np.asarray(im)[..., 3] > 100
    ys, xs = np.nonzero(a)
    Pp = np.stack([xs, ys], 1).astype(float)
    y1 = ys.max()
    day = Pp[ys > y1 - 0.12 * (y1 - ys.min())]
    g = np.array([day[:, 0].mean(), y1 - 0.06 * (y1 - ys.min())])
    tip = Pp[np.argmin(ys)]
    ax = tip - g
    L = np.hypot(*ax)
    u = (Pp - g) @ ax / (L * L)
    pts = [g]
    for f in (1 / 3, 2 / 3):
        sel = np.abs(u - f) < 0.06
        pts.append(Pp[sel].mean(0) if sel.sum() > 5 else g + ax * f)
    pts.append(g + (tip - g) * 0.92)
    return np.array(pts)


def trong_so_lua(Vpx, J, goc, chuoi):
    """trọng số đỉnh lưới lửa theo vị trí dọc đường gấp khúc J (gốc → ngọn): sát gốc bám xương gốc, còn lại chia mượt cho 3 đốt."""
    seg = [(J[k], J[k + 1]) for k in range(len(J) - 1)]
    lens = [np.hypot(*(q - p)) for p, q in seg]
    Ltot = sum(lens)
    out = []
    for v in Vpx:
        best, sbest, acc = 1e18, 0.0, 0.0
        for (p, q), Lk in zip(seg, lens):
            d = q - p
            u = float(np.clip(np.dot(v - p, d) / np.dot(d, d), 0, 1))
            dd = float(np.hypot(*(p + d * u - v)))
            if dd < best:
                best, sbest = dd, (acc + u * Lk) / Ltot
            acc += Lk
        s = sbest
        w = {goc: 1 - em(s / 0.14)}
        rest = 1 - w[goc]
        c = [(k + 0.5) / 3 for k in range(3)]
        h = [max(0.0, 1 - abs(s - ck) * 2.4) for ck in c]
        if s < c[0]:
            h[0] = 1.0
        if s > c[2]:
            h[2] = 1.0
        hs = sum(h) or 1.0
        for k, nm in enumerate(chuoi):
            if h[k] > 0:
                w[nm] = rest * h[k] / hs
        w = {k: x for k, x in w.items() if x > 1e-3}
        s_ = sum(w.values())
        out.append({k: x / s_ for k, x in w.items()})
    return out


def dung():
    sk = Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")
    by = {a["slot"]: a for a in AG["atts"]}
    cao = float(np.array(by["tou_01"]["xy"]).reshape(-1, 2)[:, 1].max()) - 20.0          # đỉnh nhánh sừng (bỏ chóp nhọn)
    pm = os.path.join(MANH, "dat_moi.json")
    MOI = json.load(open(pm, encoding="utf-8")) if os.path.exists(pm) else {}
    if "dau" in MOI:
        cao = float(MOI["dau"]["goc"][1]) - 12.0                                         # đỉnh mũ trùm (bỏ chóp nhọn)
    sk.xuong("far", "root", 0.9 * cao + 140.0, 0.45 * cao)
    for i, b in enumerate(I["bones"]):
        if b["name"] == "root":
            continue
        cha = NB[b["parent"]]
        z = L0[i]
        if b["name"] == "bone103":          # gốc bàn tay thứ 2: toạ độ của họ tính từ chỗ ĐỐI THỦ (gốc toạ độ của skill_01_1) → con của far
            w0 = B0[i]
            sk.xuong("bone103", "far", w0[0], w0[1], goc=w0[2], dai=b["len"])
            continue
        sk.xuong(b["name"], "move" if cha == "root" else cha, z[0], z[1], goc=z[2], dai=b["len"], sx=z[3], sy=z[4])
    Wi = sk.the_gioi()                        # dáng gốc của mình = khung 0 idle của họ
    G._C.pop("att", None)
    _, imgs_ho, _ = G.nap("att_goc.json")
    hien0 = {SL[k]: v > 0.5 for k, v in enumerate(CD["idle_01"][3][0])}
    IM = {}

    def anh_cua(r, ti=None):
        if r not in IM:
            g = Image.open(os.path.join(MANH, r + ".png")).convert("RGBA")
            if ti:
                g = g.convert("RGBa").resize((max(2, round(g.width * ti)), max(2, round(g.height * ti))), Image.LANCZOS).convert("RGBA")
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

    def gan(slot_ten, a, an):
        r = a["region"]
        im = anh_cua(r)
        wr, hr = imgs_ho[r].size
        uv_px, tris = G.luoi(a)
        xy = np.array(a["xy"], float).reshape(-1, 2)
        uv = uv_px / np.array([wr, hr], float)
        rows, V0 = hang(a, xy)
        sk.slot(slot_ten, rows[0][0][0], r, an=an)
        sk.atts[slot_ten][r] = {"type": "mesh", "path": r, "uv": uv, "tris": np.asarray(tris, int).reshape(-1, 3), "hull": len(uv),
                                "V": V0, "verts": rows, "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, r)] = Luoi(uv * np.array([im.width, im.height], float), np.asarray(tris, int).reshape(-1, 3), len(uv), len(uv),
                                      im.width, im.height, ten=slot_ten)
        return V0

    # ---- mảnh ĐỔI HÌNH BÓNG so với con gốc (áo, khăn vai của mình): ảnh gen "đúng chỗ, đúng cỡ" từ concept, lưới dày của mình, mỗi đỉnh
    # biến dạng ĐÚNG như điểm tương ứng trên lưới thưa của họ. dat_moi.json: {slot: {"goc": [x, y thế giới của góc trên trái ảnh], "ti": đơn vị / px}}
    def gan_goc(slot_ten, a, an, d):
        """vị trí = Σ_k β_k Σ_b w_b(k) M_b l_kb = Σ_b M_b [Σ_k β_k w_b(k) l_kb]: mỗi đỉnh của mình bám xương b với W_b = Σ β_k w_b(k) và
        điểm gắn riêng q_b = Σ β_k w_b(k) l_kb / W_b (l_kb: điểm gắn của đỉnh k của họ trong hệ xương b). Đỉnh nằm ngoài lưới của họ: bám như
        điểm gần nhất trên lưới, cộng nguyên khoảng lệch (ở dáng gốc của mình) vào điểm gắn từng xương."""
        g = Image.open(os.path.join(MANH, d.get("anh", slot_ten) + ".png")).convert("RGBA")
        ti = float(d["ti"])
        k_px = min(1.0, float(d.get("px", 1.0)))          # px atlas cho mỗi đơn vị (1,0 là đủ: dung lượng .atomik có trần 0,5 MB)
        im = anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * ti * k_px)), max(2, round(g.height * ti * k_px))), Image.LANCZOS).convert("RGBA"))
        ten_anh = slot_ten + "_moi"
        sk.anh(ten_anh, im)
        L = luoi_vung(im, buoc_vien=17.0 * k_px, buoc_trong=25.0 * k_px, ten=slot_ten, in_tk=False)
        V = np.array([[d["goc"][0] + q[0] / k_px, d["goc"][1] - q[1] / k_px] for q in np.asarray(L.pts, float)])
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

        rows, ngoai, xa = [], 0, 0.0
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
            else:
                ngoai += 1
                best = None
                for (pa, pb, ia, ib) in ((A, B_, 0, 1), (B_, C, 1, 2), (C, A, 2, 0)):
                    dist, t = gan_canh(p, pa, pb)
                    j = int(np.argmin(dist))
                    if best is None or dist[j] < best[0]:
                        w3 = [0.0, 0.0, 0.0]
                        w3[ia], w3[ib] = 1 - float(t[j]), float(t[j])
                        best = (float(dist[j]), j, tuple(w3), pa[j] + t[j] * (pb[j] - pa[j]))
                dmin, i, be, c = best
                lech = p - c
                xa = max(xa, dmin)
            acc = {}
            for vi, bw in zip(tr[i], be):
                for (bn, lx, ly, w) in rows_ho[vi]:
                    e = acc.setdefault(bn, [0.0, np.zeros(2)])
                    e[0] += bw * w
                    e[1] += bw * w * np.array([lx, ly])
            row = []
            gop = d.get("gop") or GOP.get(slot_ten, {})
            for bn, (w, q) in acc.items():
                if w < 1e-4:
                    continue
                q = q / w + np.linalg.solve(Wi[bn][:2, :2], lech)
                if bn in gop:                       # xương đuôi quật quá mạnh so với hình của mình: dồn trọng số về xương gốc chuỗi (giữ chỗ ở dáng gốc)
                    q = np.linalg.solve(Wi[gop[bn]], Wi[bn] @ np.array([q[0], q[1], 1.0]))[:2]
                    bn = gop[bn]
                row.append((bn, float(q[0]), float(q[1]), float(w)))
            tong = sum(r_[3] for r_ in row)
            rows.append([(bn, x, y, w / tong) for bn, x, y, w in row])
        V0 = np.array([sum(w * (Wi[bn] @ np.array([x, y, 1.0]))[:2] for bn, x, y, w in row) for row in rows])
        sk.slot(slot_ten, rows[0][0][0], ten_anh, an=an)
        sk.atts[slot_ten][ten_anh] = {"type": "mesh", "path": ten_anh, "uv": np.asarray(L.pts, float) / np.array([im.width, im.height], float),
                                      "tris": np.asarray(L.tris, int), "hull": L.nh, "V": V0, "verts": rows, "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, ten_anh)] = L
        print(f"  {slot_ten}: lưới của mình {L.n} đỉnh, {ngoai} đỉnh ngoài lưới gốc (xa nhất {xa:.0f}), lệch dáng gốc {np.abs(V0 - V).max():.2f}")

    def gan_xuong(slot_ten, d, xuongs, sigma, an):
        """áo vải / khối lửa của mình (hình chuông, khác hẳn áo rách nhiều đuôi của họ): KHÔNG nội suy theo tam giác lưới của họ (chỗ đuôi
        áo phải của họ lưới gập, hình mình bị xé, lòi vệt); tự chia trọng số trơn theo khoảng cách tới các đốt xương đuôi áo của họ
        (w = exp(−(d / sigma)²), giữ 4 xương nặng nhất). Xương vẫn chạy bằng clip của họ nên áo, lửa vẫn bay theo đúng nhịp."""
        g = Image.open(os.path.join(MANH, d.get("anh", slot_ten) + ".png")).convert("RGBA")
        ti = float(d["ti"])
        im = anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * ti)), max(2, round(g.height * ti))), Image.LANCZOS).convert("RGBA"))
        ten_anh = slot_ten + "_moi"
        sk.anh(ten_anh, im)
        L = luoi_vung(im, buoc_vien=17.0, buoc_trong=25.0, ten=slot_ten, in_tk=False)
        V = np.array([[d["goc"][0] + q[0], d["goc"][1] - q[1]] for q in np.asarray(L.pts, float)])
        segs = [(b_, Wi[b_][:2, 2], (Wi[b_] @ np.array([sk.bones[sk.bi[b_]]["length"], 0.0, 1.0]))[:2], np.linalg.inv(Wi[b_])) for b_ in xuongs]
        rows = []
        for p in V:
            ws = []
            for b_, p0, p1, inv in segs:
                dd = p1 - p0
                t = float(np.clip(np.dot(p - p0, dd) / max(1e-9, np.dot(dd, dd)), 0, 1))
                ws.append(math.exp(-(float(np.hypot(*(p - (p0 + t * dd)))) / sigma) ** 2))
            idx = np.argsort(ws)[::-1][:4]
            tong = sum(ws[i] for i in idx) or 1.0
            row = []
            for i in idx:
                if ws[i] / tong < 0.01:
                    continue
                lp = segs[i][3] @ np.array([p[0], p[1], 1.0])
                row.append((segs[i][0], float(lp[0]), float(lp[1]), ws[i] / tong))
            t2 = sum(r_[3] for r_ in row)
            rows.append([(b_, x, y, w / t2) for b_, x, y, w in row])
        sk.slot(slot_ten, rows[0][0][0], ten_anh, an=an)
        sk.atts[slot_ten][ten_anh] = {"type": "mesh", "path": ten_anh, "uv": np.asarray(L.pts, float) / np.array([im.width, im.height], float),
                                      "tris": np.asarray(L.tris, int), "hull": L.nh, "V": V, "verts": rows, "width": im.width, "height": im.height}
        sk.luoi[(slot_ten, ten_anh)] = L
        print(f"  {slot_ten}: lưới của mình {L.n} đỉnh, trọng số theo {len(xuongs)} đốt xương đuôi áo")

    # ---- tâm, bán kính quả cầu trong đầu trượng (trong hệ xương trượng bone56 và xương trượng thả rời bone102)
    cx, cy, Rpx, _ = DA.cau_trong_truong(DA.vung()["wuqi"][1])
    G._C.pop("att", None)
    G.nap("att_goc.json")
    c_loc = {}
    for sl, bn in (("wuqi", "bone56"), ("wuqi2", "bone102")):
        a = by[sl]
        uv_px, _ = G.luoi(a)
        M, *_ = np.linalg.lstsq(np.c_[uv_px, np.ones(len(uv_px))], np.array(a["xy"], float).reshape(-1, 2), rcond=None)
        c_loc[bn] = np.linalg.solve(WG[bn], np.array([*(np.array([cx, cy, 1.0]) @ M), 1.0]))
        Rw = float(Rpx * math.sqrt(abs(np.linalg.det(M[:2]))))
    C0 = (Wi["bone56"] @ c_loc["bone56"])[:2]

    # ---- xương nhóm cầu lửa
    sk.xuong("fly_cau", "root", 0.0, 0.0)
    sk.xuong("cau_goc", "fly_cau", float(C0[0]), float(C0[1]))
    sk.xuong("cau", "cau_goc", 0.0, 0.0)
    sk.xuong("tim", "cau", 0.0, 0.0)
    sk.xuong("mieng", "cau_goc", 0.0, 0.0)
    lua_x = {}
    for k, (gx, gy, cao_l, nga) in enumerate(LUA):
        g = Image.open(os.path.join(MANH, f"lua_{k}.png")).convert("RGBA")
        s_ = cao_l * Rw / g.height                                   # đơn vị cho mỗi px ảnh nguồn
        im = anh_cua(f"lua_{k}", ti=s_ * PX_CAU)
        Jpx = truc_lua(g)
        goc_tg = C0 + np.array([gx, gy]) * Rw
        c_, sn = math.cos(math.radians(nga)), math.sin(math.radians(nga))
        Rm = np.array([[c_, -sn], [sn, c_]])
        tg = lambda p, goc_tg=goc_tg, Rm=Rm, s_=s_, g0=Jpx[0]: goc_tg + Rm @ (np.array([p[0] - g0[0], -(p[1] - g0[1])]) * s_)   # noqa: E731
        sk.xuong(f"lua_{k}_g", "cau_goc", float(goc_tg[0] - C0[0]), float(goc_tg[1] - C0[1]))
        names = [f"lua_{k}_{j}" for j in range(3)]
        sk.chuoi(f"lua_{k}_", f"lua_{k}_g", [tg(p) for p in Jpx], ten_rieng=names)
        L = luoi_vung(im, buoc_vien=11.0, buoc_trong=15.0, ten=f"lua_{k}", in_tk=False)
        kk = g.width / im.width
        Vpx = np.asarray(L.pts, float) * kk
        lua_x[k] = dict(names=names, L=L, V=np.array([tg(p) for p in Vpx]), W=trong_so_lua(Vpx, Jpx, f"lua_{k}_g", names))
    for i in range(N_KHOI):
        sk.xuong(f"khoi_{i}", "cau_goc", 0.0, 0.9 * Rw)
    im_cau = anh_cua("cau", ti=2.06 * Rw * PX_CAU / Image.open(os.path.join(MANH, "cau.png")).width)
    im_tim = anh_cua("tim", ti=1.12 * Rw * PX_CAU / Image.open(os.path.join(MANH, "tim.png")).width)
    tat = np.asarray(im_cau).astype(np.float32).copy()               # cầu tắt (die): than nguội, đổi màu bằng mã
    xam = tat[..., :3].mean(-1, keepdims=True)
    tat[..., :3] = np.clip(xam * 0.34 + np.array([34, 28, 30]), 0, 255)
    sk.anh("cau_tat", Image.fromarray(tat.astype(np.uint8), "RGBA"))
    khoi_im = []
    for j in range(3):
        g = Image.open(os.path.join(MANH, f"khoi_{j}.png"))
        khoi_im.append(anh_cua(f"khoi_{j}", ti=1.25 * Rw * 1.0 / g.width))

    def nhom_cau(hau=""):
        for nm in NHOM:
            sl = nm + hau
            if nm.startswith("khoi"):
                sk.slot(sl, nm, "khoi_0")
                for j in range(3):
                    sk.manh(sl, f"khoi_{j}", Dat(C0[0], C0[1] + 0.9 * Rw, ti=1.25 * Rw / khoi_im[j].width), ten=f"khoi_{j}")
            elif nm.startswith("lua"):
                k = int(nm[-1])
                sk.slot(sl, f"lua_{k}_g", f"lua_{k}")
                sk.luoi_gan(sl, f"lua_{k}", lua_x[k]["L"], lua_x[k]["W"], the_gioi=lua_x[k]["V"], ten=f"lua_{k}")
            elif nm == "cau":
                sk.slot(sl, "cau", "cau")
                sk.manh(sl, "cau", Dat(C0[0], C0[1], ti=2.06 * Rw / im_cau.width), ten="cau")
                sk.manh(sl, "cau_tat", Dat(C0[0], C0[1], ti=2.06 * Rw / im_cau.width), ten="cau_tat")
            else:
                sk.slot(sl, "tim", "tim")
                sk.manh(sl, "tim", Dat(C0[0], C0[1], ti=1.12 * Rw / im_tim.width), ten="tim")
            if hau:
                sk._slot(sl)["alpha"] = 0.0

    # ---- slot theo thứ tự vẽ của họ (sau → trước)
    for a in sorted(AG["atts"], key=lambda q: q["order"]):
        s_ = a["slot"]
        if s_ == "wuqi2":
            continue
        if s_ == "wuqi":
            nhom_cau()
        if s_ in LOP and all(k in MOI for _, k in LOP[s_]):
            for sl_moi, khoa in LOP[s_]:
                if s_ == "pifeng_03":
                    gan_xuong(sl_moi, MOI[khoa], XUONG_AO, 62.0 if khoa == "ao" else 54.0, not hien0[s_])
                else:
                    gan_goc(sl_moi, a, not hien0[s_], MOI[khoa])
                if sl_moi != s_:
                    KEM[sl_moi] = s_
        elif s_ in DAU and "dau" in MOI:
            BO.add(s_)
            if s_ == "tou_01":                    # đầu mũ trùm: một mảnh cứng trên xương đầu, ở chỗ mảnh đầu trên cùng của họ
                d = MOI["dau"]
                g = Image.open(os.path.join(MANH, "dau.png")).convert("RGBA")
                kp = 1.2
                im = anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * d["ti"] * kp)), max(2, round(g.height * d["ti"] * kp))), Image.LANCZOS).convert("RGBA"))
                sk.anh("dau", im)
                sk.slot("dau", "bone6", "dau")
                sk.manh("dau", "dau", Dat(d["goc"][0], d["goc"][1], ti=1.0 / kp, neo=(0.0, 0.0)), ten="dau")
                KEM["dau"] = "tou_02"
        else:
            gan(s_, a, an=not hien0[s_])
    # ---- trên cùng: nhóm cầu lửa bản _t, trượng bản _t, trượng thả rời, bốn ngón tay trượng bản _t
    nhom_cau("_t")
    gan("wuqi_t", by["wuqi"], an=True)
    gan("wuqi2", by["wuqi2"], an=True)
    for s_ in TAY_R:
        gan(s_ + "_t", by[s_], an=True)

    for e, m in (("trung", "khung đòn trúng"), ("tay_tan", "bàn tay vuốt tan đi"), ("tay_hien", "bàn tay vuốt hiện ra chỗ đối thủ"),
                 ("goi_kim", "giơ trượng: kim lửa hiện ra quanh đầu trượng"), ("ban_kim", "vụt trượng: kim lửa phóng đi"),
                 ("tha_truong", "buông trượng, trượng lơ lửng"), ("tach_cau", "cầu lửa rời đầu trượng"), ("hut", "bắt đầu hút lửa, cầu lớn dần"),
                 ("ban_cau", "bắn cầu lửa lớn: cầu của rig biến mất, code sinh cầu lửa bay từ xương mieng (cỡ = 2,4 bán kính cầu thường)"), ("nhen", "cầu lửa mới nhen trong đầu trượng"), ("tat", "cầu lửa tắt"), ("nga", "ngã xuống")):
        sk.su_kien(e, m)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao game {cao:.0f}; cầu lửa tâm {C0.round(1)} bán kính {Rw:.1f}")
    return sk, dict(cao=cao, C0=C0, Rw=Rw, c_loc=c_loc, lua={k: v["names"] for k, v in lua_x.items()})


# ---------------------------------------------------------------- tiện ích dáng
def dich_tg(sk, P, b, d, W=None):
    """dời xương b một véc-tơ THẾ GIỚI d (đổi về hệ xương cha)."""
    W = W if W is not None else sk.the_gioi(P)
    cha = sk.bones[sk.bi[b]]["parent"]
    lp = np.linalg.solve(W[cha][:2, :2], np.asarray(d, float))
    P.move(b, float(lp[0]), float(lp[1]))


def cho_cau(sk, info, P, xuong, W=None):
    """tâm quả cầu trong đầu trượng (thế giới) ở tư thế P."""
    W = W if W is not None else sk.the_gioi(P)
    return (W[xuong] @ info["c_loc"][xuong])[:2]


def dat_cau(info, P, pos, fly=(0.0, 0.0), tren=False, co=1.0, hien=1.0):
    """đặt nhóm cầu lửa: tâm ở pos (thế giới), fly = độ dời của fly_cau; tren: vẽ bản trên cùng; co: cỡ; hien: độ đậm."""
    C0 = info["C0"]
    P.t.pop("cau_goc", None)
    P.t.pop("fly_cau", None)
    if abs(fly[0]) > 1e-6 or abs(fly[1]) > 1e-6:
        P.move("fly_cau", float(fly[0]), float(fly[1]))
    P.move("cau_goc", float(pos[0] - fly[0] - C0[0]), float(pos[1] - fly[1] - C0[1]))
    if abs(co - 1) > 1e-6:
        P.scale("cau_goc", co)
    for nm in NHOM:
        P.alpha[nm] = 0.0 if tren else hien
        P.alpha[nm + "_t"] = hien if tren else 0.0
    P.att.setdefault("cau", "cau")
    P.att.setdefault("cau_t", "cau")


def lua_co(P, k_dai=1.0, k_rong=None, nga=0.0, chi=None):
    """lưỡi lửa dài / ngắn, ngả (độ, dương = ngọn sang trái)."""
    for k in range(N_LUA):
        if chi is not None and k not in chi:
            continue
        if abs(k_dai - 1) > 1e-6 or k_rong is not None:
            P.scale(f"lua_{k}_g", k_rong if k_rong is not None else 1.0 + (k_dai - 1) * 0.3, k_dai)
        if abs(nga) > 1e-6:
            P.rot(f"lua_{k}_g", nga * 0.7)
            for j in range(3):
                P.rot(f"lua_{k}_{j}", nga * 0.14)


class LuaNga:
    """hậu kỳ (chạy như phần mềm của clip): lưỡi lửa ngả NGƯỢC chiều bay của quả cầu, đo vận tốc trên khung đã nướng, làm mượt theo thời
    gian (không lật gắt khi vận tốc đổi dấu); cầu nhảy chỗ (nhen lại trong đầu trượng) thì coi như đứng yên."""

    def __init__(self, info, tinh=0.0):
        self.C0, self.tinh = info["C0"], tinh

    def chay(self, sk, frames, ts, loop, fps):
        n = len(frames)

        def vt(P):
            a, b = P.t.get("cau_goc", (0, 0)), P.t.get("fly_cau", (0, 0))
            return np.array([a[0] + b[0], a[1] + b[1]])
        pos = [vt(P) for P in frames]
        ang, dai = [0.0] * n, [1.0] * n
        for i in range(n):
            j = i - 1 if i > 0 else (n - 2 if loop else 0)
            v = (pos[i] - pos[j]) * fps
            sp = float(np.hypot(*v))
            if sp > 7000.0 or sp < 1e-6:
                continue
            d = np.array([-v[0], max(300.0, 700.0 - 0.3 * v[1])])
            a = math.degrees(math.atan2(d[1], d[0])) - 90.0
            ang[i] = max(-55.0, min(55.0, a)) * min(1.0, sp / 300.0)
            dai[i] = 1.0 + min(0.4, abs(v[0]) / 2600.0) - max(-0.28, min(0.28, v[1] / 3600.0))
        for vong in range(2 if loop else 1):
            a_, d_ = (ang[-1], dai[-1]) if (loop and vong) else (0.0, 1.0)
            for i in range(n):
                a_ += (ang[i] - a_) * 0.3
                d_ += (dai[i] - d_) * 0.3
                if vong or not loop:
                    ang[i], dai[i] = a_, d_
            if loop and not vong:
                continue
        for i, P in enumerate(frames):
            if loop and i == n - 1:
                ang[i], dai[i] = ang[0], dai[0]
            if abs(ang[i]) > 0.05 or abs(dai[i] - 1) > 0.002:
                lua_co(P, k_dai=dai[i], nga=ang[i])


def boc(sk, info, fn):
    return fn


# ---------------------------------------------------------------- clip
def lam_clip(sk, info):
    out = []
    cao, Rw = info["cao"], info["Rw"]
    far = sk.W0["far"][:2, 2].copy()
    lua = info["lua"]
    NGON_L = [f"bone{i}" for i in range(11, 21)]        # mười đốt vuốt của tay vuốt

    def ho(P, clip, u, lap=False, d=None, tru_x=(), cau=True, ep_goc=False):
        """dáng + độ đậm theo clip của họ ở giây u; đặt nhóm cầu lửa vào đầu trượng. d: dáng đã pha sẵn (thay mau)."""
        dat(P, d if d is not None else mau(clip, u, lap, tru=tru_x))
        xg, tr = hien_theo_ho(P, clip, u, lap, ep_goc=ep_goc)
        return xg, tr

    def cau_o_truong(P, xg, tr, co=1.0, hien=1.0):
        dat_cau(info, P, cho_cau(sk, info, P, xg), tren=tr, co=co, hien=hien)

    # ---- AURA: lửa uốn lượn + tim lửa đập + khói bốc sau cầu lửa (lặp, phủ lên mọi clip)
    D_AU, DOI_KHOI = 4.0, 2.0

    def aura(t, P):
        om = 2 * math.pi / 1.0
        for k, names in lua.items():
            ph = k * 1.9
            for j, nm in enumerate(names):
                a = (2.8 + 2.6 * j) * math.sin(om * t + ph - 0.95 * j) + 1.3 * math.sin(2 * om * t + ph * 1.3 - 0.7 * j)
                P.rot(nm, a)
            sc = 1.0 + 0.07 * math.sin(2 * om * t + ph * 0.7) + 0.04 * math.sin(3 * om * t + ph)
            P.scale(f"lua_{k}_g", 1.0 + (sc - 1) * 0.35, sc)
        if "lua_ao" in sk.si:                      # khối lửa dưới áo: sóng chạy xuống các đốt cuối của ba chuỗi đuôi áo (xương chỉ áo dùng)
            for nm, ph, bd in (("bone34", 0.0, 3.2), ("bone35", 0.9, 5.5), ("bone39", 2.1, 3.2), ("bone40", 3.0, 5.5)):
                P.rot(nm, bd * math.sin(om * t * 0.75 + ph) + 0.35 * bd * math.sin(2 * om * t * 0.75 + 1.7 * ph))
        P.scale("tim", 1.0 + 0.07 * math.sin(2 * om * t), 1.0 + 0.07 * math.sin(2 * om * t + 1.3))
        P.rot("tim", 9.0 * math.sin(om * t * 0.5))
        P.scale("cau", 1.0 + 0.015 * math.sin(2 * om * t + 0.6))
        for i in range(N_KHOI):
            q = ((t + i * DOI_KHOI / N_KHOI) % DOI_KHOI) / DOI_KHOI            # tuổi 0..1
            lech = (-1) ** i * (0.18 + 0.07 * (i % 3))
            x = Rw * (lech * 0.6 + (-0.55 + lech) * q ** 1.3 + 0.16 * math.sin(2 * math.pi * (q * 1.5 + i * 0.37)))
            y = Rw * (0.2 + 3.6 * q ** 1.25)                                    # càng về cuối bay lên càng nhanh
            P.move(f"khoi_{i}", x, y)
            P.rot(f"khoi_{i}", (-1) ** i * (70.0 * q + 25.0 * i))
            s = (0.42 + 0.68 * em(q / 0.42)) * (1.0 - 0.72 * em((q - 0.55) / 0.45))
            P.scale(f"khoi_{i}", s)
            a = em(q / 0.10) * (1.0 - em((q - 0.70) / 0.30))
            hinh = "khoi_0" if q < 0.36 else ("khoi_1" if q < 0.66 else "khoi_2")
            for hau in ("", "_t"):
                P.alpha[f"khoi_{i}{hau}"] = a
                P.att[f"khoi_{i}{hau}"] = hinh
    out.append(Clip("aura", D_AU, aura, loop=True))

    # ---- IDLE: của họ + sửa: nhấp nhô chậm thêm, một lần mỗi vòng nâng trượng ngắm cầu lửa (lửa bùng), vuốt gõ nhịp
    def idle(t, P):
        xg, tr = ho(P, "idle_01", t, True)
        P.move("bone", 0.0, 7.0 * math.sin(2 * math.pi * t / 2.0))
        w = bump(t, 2.15, 2.6, 3.05, 3.55)
        if w > 0:
            dich_tg(sk, P, "bone45", (10.0 * w, 26.0 * w))
            P.rot("bone6", 6.0 * w)
            lua_co(P, k_dai=1.0 + 0.38 * w)
            P.scale("tim", 1.0 + 0.22 * w)
        g = bump(t, 0.55, 0.8, 1.5, 1.8)
        if g > 0:
            for i, b in enumerate(NGON_L):
                P.rot(b, 9.0 * g * math.sin(2 * math.pi * (t - 0.55) / 0.42 - 0.55 * (i // 2)))
        cau_o_truong(P, xg, tr)
    out.append(Clip("idle", CD["idle_01"][0], boc(sk, info, idle), loop=True))

    # ---- WALK: của họ + nhún mạnh hơn, lửa ngả về sau
    D_W = CD["run_01"][0]

    def walk(t, P):
        xg, tr = ho(P, "run_01", t, True)
        P.move("bone", 0.0, 8.0 * (math.sin(2 * math.pi * 2 * t / D_W) - 0.0) * 0.5)
        P.rot("bone6", 3.0 * math.sin(2 * math.pi * t / D_W + 0.8) - 3.0 * math.sin(0.8))
        lua_co(P, k_dai=1.15, nga=24.0)
        cau_o_truong(P, xg, tr)
    out.append(Clip("walk", D_W, walk, loop=True))

    def hit(t, P):
        xg, tr = ho(P, "hit_01", t)
        cau_o_truong(P, xg, tr)
    out.append(Clip("hit", CD["hit_01"][0], boc(sk, info, hit)))

    # ---- ATTACK: skill_01 của họ (giơ tay vuốt, tay tan) + bàn tay thứ 2 hiện ra chỗ đối thủ cào (skill_01_1, trên xương far)
    K_AT = 1.2 / CD["skill_01"][0]
    D_AT = 1.2
    SL2 = [s for s in SL if any(F[SL.index(s)] > 0 for F in CD["skill_01_1"][3])]

    def attack(t, P):
        u = t / K_AT
        xg, tr = ho(P, "skill_01", u, tru_x=TAY2)
        dat(P, mau("skill_01_1", u, chi=TAY2))
        hien_theo_ho(P, "skill_01_1", u, chi=SL2)
        cau_o_truong(P, xg, tr)
    out.append(Clip("attack", D_AT, boc(sk, info, attack),
                    ev=[(0.33 * K_AT, "tay_tan", ""), (0.47 * K_AT, "tay_hien", ""), (0.56 * K_AT, "trung", "")], trung=0.56 * K_AT))

    # ---- CAST: skill_02 của họ: giơ trượng (kim lửa hiện ra), giữ, vụt trượng (kim phóng đi)
    TC = [(0.0, 0.0), (0.16, 0.14), (0.95, 0.70), (1.05, 0.80), (1.75, 1.5)]
    T_GOI, T_BAN = 0.16, 1.05

    def cast(t, P):
        u = tq(t, TC)
        xg, tr = ho(P, "skill_02", u, ep_goc=t > 1.75 - 0.23)
        g = bump(t, 0.16, 0.4, 0.9, 1.0)
        P.rot("bone4", 1.3 * g * math.sin(2 * math.pi * 10 * t))            # gồng run lúc giữ trượng trên cao
        lua_co(P, k_dai=1.0 + 0.55 * g)
        P.scale("tim", 1.0 + 0.25 * g)
        cau_o_truong(P, xg, tr)
    out.append(Clip("cast", 1.75, boc(sk, info, cast), ev=[(T_GOI, "goi_kim", ""), (T_BAN, "ban_kim", ""), (T_BAN + 0.14, "trung", "")],
                    trung=T_BAN + 0.14))

    # ---- SKILL: skill_03 của họ kéo dài. Tung trượng, dang hai tay, trượng lơ lửng trước ngực → cầu lửa RỜI đầu trượng bay lên cao →
    # hút lửa, lớn dần → hai tay vung tới, cầu lửa bắn sang đối thủ → chụp lại trượng, cầu lửa mới nhen trong đầu trượng
    T_TACH, T_LEN, T_HUT, T_DAY, T_NEM, BAY, T_VE, D_SK = 0.66, 1.05, 1.05, 2.05, 2.25, 0.2, 2.75, 3.4
    U_GIU0, U_GIU1, U_VE = 0.62, 1.36, 1.36
    TOP = np.array([64.0, 1000.0])                  # khung sticker của game: 2,72 chiều cao trên chân (≈ 1570): cầu to + lửa phải nằm dưới đó
    CO_TO = 2.2

    def u_sk(t):
        if t < 0.62:
            return t
        if t < T_VE:
            return U_GIU0 + (U_GIU1 - U_GIU0) * ((t - 0.62) / (T_VE - 0.62))
        return U_VE + (t - T_VE) * (CD["skill_03"][0] - U_VE) / (D_SK - T_VE)

    def cau_sk(t, c_tr):
        """(tâm, fly, cỡ, độ đậm) của cầu lửa trong chiêu cuối; c_tr = tâm đầu trượng ở khung này."""
        if t < T_TACH:
            return c_tr, (0, 0), 1.0, 1.0
        if t < T_NEM:
            q = em((t - T_TACH) / (T_LEN - T_TACH))
            p = c_tr + (TOP - c_tr) * q
            lon = em((t - T_HUT) / (T_DAY - T_HUT))
            co = 1.0 + (CO_TO - 1.0) * lon
            co *= 1.0 + 0.05 * lon * math.sin(2 * math.pi * 6.5 * t)                    # phập phồng lúc hút lửa
            p = p + np.array([0.0, 10.0 * lon * math.sin(2 * math.pi * 1.4 * t)])
            lui = em((t - T_DAY) / (T_NEM - T_DAY))                                      # lấy đà: lùi về sau, lên chút
            p = p + np.array([-70.0, 34.0]) * lui
            co *= 1.0 + 0.10 * lui
            return p, (0, 0), co, 1.0
        if t < T_VE + 0.1:
            # người dùng 2026-11-13: "bạn chỉ cần làm cầu lửa bay lên phình to, còn bay đi đâu do code làm" → đúng mốc ban_cau cầu lửa của
            # rig biến mất tại chỗ (giữ nguyên chỗ, cỡ cuối để code hiệu ứng sinh cầu lửa bay từ xương `mieng`), KHÔNG nướng đường bay
            return TOP + np.array([-70.0, 34.0]), (0, 0), CO_TO * 1.1, 0.0
        # sau khi nổ: cầu lửa mới nhen dần trong đầu trượng
        nh = em((t - (T_VE + 0.12)) / 0.42)
        return c_tr, (0, 0), max(0.02, nh), 1.0 if nh > 0.001 else 0.0

    def skill(t, P):
        u = u_sk(t)
        xg, tr = ho(P, "skill_03", u)
        hut = bump(t, T_HUT, T_HUT + 0.3, T_DAY, T_NEM)
        nem = bump(t, T_NEM - 0.04, T_NEM + 0.08, T_NEM + 0.35, T_VE)
        lay_da = bump(t, T_DAY, T_NEM - 0.02, T_NEM, T_NEM + 0.06)
        # thân: ngửa nhìn lên quả cầu lúc hút, run; lấy đà ngả sau; ném thì chúi tới
        P.rot("bone6", 9.0 * hut + 6.0 * lay_da - 12.0 * nem)
        P.rot("bone4", 2.0 * hut * math.sin(2 * math.pi * 9 * t) * (0.4 + 0.8 * u_(t, T_HUT, T_DAY)) + 5.0 * lay_da - 9.0 * nem)
        P.move("bone", -14.0 * lay_da + 30.0 * nem, 10.0 * hut + 8.0 * lay_da - 16.0 * nem)
        W = sk.the_gioi(P)
        # hai tay: lúc hút nâng dần lên và dang rộng; lấy đà giơ cao ra sau; ném thì vung tới trước - xuống
        for b, ben in (("bone10", 1.0), ("bone87", -1.0)):
            d = np.array([ben * 26.0, 150.0]) * hut * (0.55 + 0.45 * u_(t, T_HUT, T_DAY))
            d += np.array([-60.0 + ben * 20.0, 120.0]) * lay_da
            d += np.array([230.0 - ben * 90.0, 40.0 + ben * 30.0]) * nem
            if b == "bone87" and P.alpha.get("shouzhangL_03", 0) < 0.5:
                continue
            dich_tg(sk, P, b, d, W)
        c_tr = cho_cau(sk, info, P, xg)
        p, fly, co, a = cau_sk(t, c_tr)
        roi = T_TACH <= t < T_VE + 0.1
        dat_cau(info, P, p, fly=fly, tren=True if roi else tr, co=co, hien=a)
        lon = em((t - T_HUT) / (T_DAY - T_HUT)) if t < T_NEM else 0.0
        lua_co(P, k_dai=(1.0 + 0.45 * hut) * (1.0 - 0.5 * lon))          # cầu càng to lưỡi lửa càng ngắn so với cầu (khỏi vọt khỏi khung)
        P.scale("tim", 1.0 + 0.2 * hut)
    out.append(Clip("skill", D_SK, boc(sk, info, skill),
                    ev=[(0.17, "tha_truong", ""), (T_TACH, "tach_cau", ""), (T_HUT, "hut", ""), (T_NEM, "ban_cau", ""),
                        (T_NEM + BAY, "trung", ""), (T_VE + 0.12, "nhen", "")], trung=T_NEM + BAY))

    # ---- APPEAR: bay từ ngoài - trên bên trái vào (dáng lướt của run_01, áo tóc kéo ngược), hãm lại quá đà chút rồi về thế
    T_TOI, D_AP = 0.62, 1.3
    BD = np.array([-0.95 * cao, 0.40 * cao])

    def appear(t, P):
        w = 1.0 - em((t - 0.42) / 0.5)
        d = pha(mau("idle_01", 0.0), mau("run_01", t * 1.1, True), w)
        dat(P, d)
        xg, tr = hien_theo_ho(P, "idle_01", 0.0)
        q = min(1.0, t / T_TOI)
        e = 1.0 - (1.0 - q) ** 2.4
        x = BD[0] * (1.0 - e)
        y = BD[1] * (1.0 - e) - 0.16 * cao * math.sin(math.pi * q) * (1.0 - q * 0.5)
        if t > T_TOI:
            s = t - T_TOI
            x += 36.0 * math.exp(-s / 0.16) * math.sin(math.pi * min(1.0, s / 0.22))
            y += 14.0 * math.exp(-s / 0.2) * math.sin(2 * math.pi * s / 0.5)
        P.move("move", x, y)
        P.rot("bone2", -9.0 * (1.0 - e) + 5.0 * bump(t, T_TOI - 0.05, T_TOI + 0.08, T_TOI + 0.15, T_TOI + 0.5))
        cau_o_truong(P, xg, tr)
        a_ = min(1.0, t / 0.09)
        if a_ < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a_ * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("appear", D_AP, boc(sk, info, appear)))

    # ---- DIE: die_01 của họ + cầu lửa tắt dần (lửa lụi, cầu thành than), khói lịm, mờ dần
    D_DIE = CD["die_01"][0] + 0.45

    def die(t, P):
        u = min(t, CD["die_01"][0])
        xg, tr = ho(P, "die_01", u)
        cau_o_truong(P, xg, tr)
        lui = em((t - 0.25) / 0.6)
        lua_co(P, k_dai=max(0.03, 1.0 - lui), k_rong=max(0.03, 1.0 - 0.8 * lui))
        P.scale("tim", max(0.02, 1.0 - em((t - 0.45) / 0.45)))
        if t > 0.8:
            P.att["cau"] = P.att["cau_t"] = "cau_tat"
            P.alpha["tim"] = P.alpha["tim_t"] = 0.0
            for k in range(N_LUA):
                P.alpha[f"lua_{k}"] = P.alpha[f"lua_{k}_t"] = 0.0
        if "lua_ao" in sk.si:                              # lửa dưới áo cũng lụi dần lúc nằm xuống
            P.alpha["lua_ao"] = P.alpha.get("lua_ao", 1.0) * (1.0 - em((t - 0.75) / 0.5))
        kh = 1.0 - em((t - 0.9) / 0.4)
        for i in range(N_KHOI):
            for hau in ("", "_t"):
                P.alpha[f"khoi_{i}{hau}"] = P.alpha.get(f"khoi_{i}{hau}", 1.0) * kh
        fa = 1.0 - em((t - (D_DIE - 0.3)) / 0.3)
        if fa < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = fa * P.alpha.get(sl["name"], sl["alpha"])
    out.append(Clip("die", D_DIE, die, ev=[(0.8, "tat", ""), (0.75, "nga", "")]))
    for c in out:
        if c.ten in ("idle", "hit", "attack", "cast", "skill", "appear"):
            c.mem = [LuaNga(info)] + [LoXo(n, k=(170, 120, 85), damp=0.5, maxang=16.0) for n in lua.values()]
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
    if a and a[0] == "so":           # khung 0 idle (không khói) đặt cạnh concept đã duyệt, cùng khung nhìn → rig/so_concept.png + IoU hình bóng
        tg, ti = DA.tg_concept()
        x0, y1 = tg(0, 0)
        x1, y0 = tg(DA.W, DA.H)
        c = [x for x in clips if x.ten == "idle"][0]
        P = hoat.nuong(sk, c)[0]
        for i in range(N_KHOI):
            P.alpha[f"khoi_{i}"] = P.alpha[f"khoi_{i}_t"] = 0.0
        im = soi.Ve(sk).ve(P, (x0, y0, x1, y1), 1.0 / ti, bg=(255, 255, 255), ss=2).convert("RGB").resize((DA.W, DA.H), Image.LANCZOS)
        cc = Image.open(DA.CONCEPT).convert("RGB").resize((DA.W, DA.H), Image.LANCZOS)
        ma, mb = np.asarray(im).min(2) < 225, np.asarray(cc).min(2) < 225
        vis = np.full((DA.H, DA.W, 3), 255, np.uint8)
        vis[ma & mb] = (170, 170, 170)
        vis[mb & ~ma] = (230, 60, 60)
        vis[ma & ~mb] = (60, 190, 60)
        out = Image.new("RGB", (DA.W * 3, DA.H), (255, 255, 255))
        out.paste(cc, (0, 0))
        out.paste(im, (DA.W, 0))
        out.paste(Image.fromarray(vis), (DA.W * 2, 0))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, "so_concept.png")
        out.save(pth)
        print(pth, f"IoU hình bóng {float((ma & mb).sum()) / max(1, (ma | mb).sum()):.3f} (đỏ: concept có mà rig thiếu; xanh: rig thừa)")
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
        sc = float(a[3]) if len(a) > 3 else 0.5
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB") for P in Ps]
        cot = min(len(ims), 6)
        hang_ = (len(ims) + cot - 1) // cot
        out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang_), (150, 150, 150))
        for i, im in enumerate(ims):
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    xuat.xuat_het(sk, clips, RA, TEN, "Pháp sư lửa (phap_lua_1)", dang=1, so_dang=1, dung_yen=("attack", "cast", "skill"), lao=(),
                  far=("attack",), cao=info["cao"], ma_goc=None, tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001},
                  khop_idle=0.2, impact={"attack": (0.05, 0.25, 0.07), "skill": (0.22, 1.0, 0.18, "#ffb04066")})


if __name__ == "__main__":
    main(sys.argv[1:])
