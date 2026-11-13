# -*- coding: utf-8 -*-
"""Rùa golem lửa (rua_lua, tướng thứ 5 đảo Hỏa): rig trên bộ xương của con gốc monster_3425. Mảnh của mình đặt đúng chỗ concept đã duyệt
(L1_duyet = hướng A đá bazan, hai sừng lành lặn); chuyển động nền lấy mẫu từ clip của họ bằng runtime Spine thật (<scan>/sample.json,
trường `l`: biến đổi riêng ĐÃ áp 8 IK chân), clip riêng dựng bằng mã trên chính rig của mình.

- Đủ xương của họ (bỏ `root` của họ: thay bằng root + move của mình); không ràng buộc (đã nướng vào mẫu khung).
- Mảnh cứng (cột đá, hai sừng, mặt, hàm, bốn đùi, lòng miệng) bám xương của part gốc; mảnh có lưới trọng số ở con gốc (mai, bụng, đuôi,
  bốn ống chân) dựng lưới dày của mình, mỗi đỉnh biến dạng như điểm tương ứng trên lưới thưa của họ (gan_theo_goc).
- Bảy NGỌN LỬA trên lưng là lưới riêng: xương gốc `<lửa>_g` (co / mọc cả ngọn: chiêu cuối hút lửa, die, appear) + chuỗi 3 đốt đung đưa
  nhẹ lệch pha + lò xo (người dùng dặn: "lửa cũng phải có animation đung đưa nhẹ").
- Đổi hình bằng độ đậm: `mat_tat` (mắt tắt), `<ống chân>_nguoi` (pha lê nguội).
- Xương chỗ bám cho VFX: `mieng` (trước mõm: cầu lửa của chiêu mana), `cau` (mũi sừng gần: cầu lửa chiêu cuối), `<lửa>_g` (gốc từng
  ngọn lửa: dải lửa bị hút). Sự kiện: tu, phun, hut (chuỗi = tên ngọn lửa), day, nem, trung, gam, chan, dau, lua, tat, sap.

Người dùng (2026-11-13): appear = cái mai nằm dưới đất rồi chân tay đầu đuôi mọc ra, gầm một phát; idle, walk giống họ; đánh thường bò
nhanh tới mục tiêu và húc như skill_03; chiêu mana như skill_04 (đứng lên nhẹ, há mồm, tụ cầu lửa rồi bắn); chiêu cuối tụ cầu lửa trên
sừng, lửa hút từ lửa trên lưng, hút hết thì phóng cầu vào địch; die lửa tắt, tướng quỵ xuống.

    rua_lua_rig.py                           dựng, xuất inbox/rua_lua_1/rig/ (JSON Spine, atlas, .atomik, tờ khung, xem.html)
    rua_lua_rig.py soi <clip> <giây,..> [tỉ lệ]   khung lớn nền xám → rig/soi_<clip>.png
Xương, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai."""
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
from quai.khung import Sk, Pose, mat, goc_mat  # noqa: E402
from quai.hoat import Clip, LoXo  # noqa: E402
from quai.luoi import luoi_vung  # noqa: E402
import rua_lua as G  # noqa: E402

# RL_NON=<hướng>: DẠNG 1 (rùa non): cùng xương, cùng clip, mảnh xếp lại ở tỉ lệ non (rua_lua_non.py manh) → inbox/rua_lua_non/rig_<hướng>/
NON = os.environ.get("RL_NON") or ""
TEN = "rua_lua_non" if NON else "rua_lua_1"
RA = os.path.join(HERE, "inbox", "rua_lua_non", "rig_" + NON) if NON else os.path.join(G.BASE, "rig")
MANH = os.environ.get("RL_MANH") or (os.path.join(HERE, "inbox", "rua_lua_non", "manh_" + NON) if NON else os.path.join(G.BASE, "manh"))
SCAN = G.scan()
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
A0 = json.load(open(os.path.join(SCAN, "att_idle0.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample.json"), encoding="utf-8"))
NB = [b["name"] for b in I["bones"]]
NA = [b["name"] for b in A0["bones"]]
KG = 0.80                    # đơn vị rig con gốc → đơn vị rig của mình
PXU = 0.92                   # pixel ảnh atlas cho mỗi đơn vị rig con gốc
FPS = 30.0

# ngọn lửa → xương đá nó mọc ra (xương của pha lê tương ứng ở con gốc)
LUA_XUONG = {"lua_sung": "bone31", "lua_duoi": "bone38", "lua_trai": "bone28", "lua_giua_trai": "bone28", "lua_cao": "bone29",
             "lua_phai": "bone29", "lua_nho": "bone30"}
# thứ tự bị hút ở chiêu cuối: xa sừng nhất trước
HUT = ["lua_duoi", "lua_trai", "lua_giua_trai", "lua_cao", "lua_phai", "lua_nho", "lua_sung"]
# khung concept (px, y xuống) ↔ thế giới con gốc dáng idle giây 0: px = ox + s·X, py = oy − s·Y. Khớp bằng MỐC TAY đọc trên concept
# (mũi sừng gần, mũi đuôi, mép ngoài và đáy ba chân): viền part của rig chồng lên concept khít (mau/_rig_tren_concept.png). Khớp tự động
# theo tâm khung các mảnh cho 1,238 và lệch 40–70 px vì mảnh của mình vẽ thêm phần khuất nên tâm khung không còn ứng với part gốc.
KHOP = (1.144, 720.0, 934.0)
MIENG = (1088, 812)          # trước mõm trên concept (chỗ tụ cầu lửa của chiêu mana)
SUNG_MUI = (1100, 316)       # mũi sừng gần trên concept (chỗ tụ cầu lửa của chiêu cuối)
# nhóm mọc ra ở appear: (xương gốc để co, các mảnh)
NHOM = {
    "chan_sau_xa": ("bone20", ["dui_sau_xa", "ong_sau_xa"]),
    "chan_sau_gan": ("bone16", ["dui_sau_gan", "ong_sau_gan"]),
    "chan_truoc_xa": ("bone12", ["dui_truoc_xa", "ong_truoc_xa", "ong_truoc_xa_nguoi"]),
    "chan_truoc_gan": ("bone8", ["dui_truoc_gan", "ong_truoc_gan", "ong_truoc_gan_nguoi"]),
    "duoi": ("bone24", ["duoi"]),
    "dau": ("bone7", ["hong", "ham", "mat_so", "mat_tat", "sung_gan", "sung_xa"]),      # bone6 (cổ) còn giữ một phần lưới bụng: không co
}


# ---------------------------------------------------------------- chuyển động nền của họ (mẫu khung, đã áp IK)
def _cd():
    """lệch so với dáng gốc của từng xương, từng khung. Góc mỗi clip liền mạch theo thời gian (unwrap) và KHUNG ĐẦU của mọi clip quy về
    cùng vòng với khung đầu idle_01: pha hai clip ở bất kỳ giây nào cũng không lệch nhau bội 360° (xương chân nướng IK có góc gần ±180°
    so với dáng gốc; quy từng clip về gần 0 hoặc quy từng khung thì hai clip lệch nhau một vòng, pha ra xương quay ngược)."""
    out, ref = {}, {}
    for clip in ["idle_01"] + [c for c in S if c != "idle_01"]:
        v = S[clip]
        fr = v["frames"]
        res = {}
        for i, b0 in enumerate(I["bones"]):
            if b0["name"] == "root":
                continue
            Am = np.array([[F["l"][i][2] - b0["rot"], (F["l"][i][0] - b0["x"]) * KG, (F["l"][i][1] - b0["y"]) * KG,
                            F["l"][i][3] / (b0["sx"] or 1.0), F["l"][i][4] / (b0["sy"] or 1.0)] for F in fr])
            Am[:, 0] = np.degrees(np.unwrap(np.radians(Am[:, 0])))
            if clip == "idle_01":
                Am[:, 0] -= 360.0 * round(Am[0, 0] / 360.0)
                ref[b0["name"]] = Am[0, 0]
            else:
                Am[:, 0] -= 360.0 * round((Am[0, 0] - ref[b0["name"]]) / 360.0)
            res[b0["name"]] = Am          # giữ mọi xương (kể cả xương đứng yên) để pha không thiếu
        out[clip] = (float(v["dur"]), res)
    return out


CD = _cd()
MOT = np.array([0, 0, 0, 1, 1.0])


def mau(clip, t, lap=False):
    dur, R = CD[clip]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    out = {}
    for b, arr in R.items():
        n = len(arr)
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        out[b] = arr[i0] * (1 - w) + arr[i1] * w
    return out


def mau_tr(clip, t, r=1):
    """mẫu làm trơn theo thời gian (trung bình tam giác ± r khung của clip nguồn): clip của họ bật cả thân trong 1–2 khung (thụp, chồm,
    xoạc chân); hình họ nhỏ không lộ, hình mình to thì thấy giật."""
    if r <= 0:
        return mau(clip, t)
    acc, tot = None, 0.0
    for k in range(-r, r + 1):
        w = r + 1 - abs(k)
        d = mau(clip, t + k / FPS)
        tot += w
        if acc is None:
            acc = {b: v * w for b, v in d.items()}
        else:
            for b, v in d.items():
                acc[b] = acc[b] + v * w
    return {b: v / tot for b, v in acc.items()}


def pha(a, b, w):
    out = {}
    for k in set(a) | set(b):
        out[k] = a.get(k, MOT) * (1 - w) + b.get(k, MOT) * w
    return out


def dat(P, d, chi=None, tru=()):
    for b, v in d.items():
        if (chi is not None and b not in chi) or b in tru:
            continue
        if abs(v[0]) > 1e-5:
            P.rot(b, float(v[0]))
        if abs(v[1]) > 1e-5 or abs(v[2]) > 1e-5:
            P.move(b, float(v[1]), float(v[2]))
        if abs(v[3] - 1) > 1e-6 or abs(v[4] - 1) > 1e-6:
            P.scale(b, float(v[3]), float(v[4]))


# ---------------------------------------------------------------- đường cong
def em(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ra_(x, k=2.0):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** k


def vao(x, k=2.0):
    x = min(1.0, max(0.0, x))
    return x ** k


def vot(x, s=1.70158):
    x = min(1.0, max(0.0, x)) - 1.0
    return x * x * ((s + 1) * x + s) + 1.0


def cong(moc, t, kieu=None):
    if t <= moc[0][0]:
        return moc[0][1]
    for i in range(len(moc) - 1):
        (a, x), (b, y) = moc[i], moc[i + 1]
        if t <= b:
            w = (t - a) / (b - a)
            w = (kieu[i] if kieu and kieu[i] else em)(w)
            return x + (y - x) * w
    return moc[-1][1]


def rung(t, t0, bien, tan=0.2, hz=9.0):
    if t < t0:
        return 0.0
    x = t - t0
    return bien * math.exp(-x / tan) * math.sin(2 * math.pi * hz * x)


def bat(t, t0, dai=0.22, qua=1.18):
    """mọc ra: 0 → vọt quá → 1."""
    u = (t - t0) / dai
    if u <= 0:
        return 0.0
    if u >= 1:
        return 1.0
    return cong([(0, 0.0), (0.55, qua), (0.8, 0.94), (1.0, 1.0)], u, [ra_, em, em])


# ---------------------------------------------------------------- dựng rig
def att_cua(slot):
    return next(a for a in A0["atts"] if a["slot"] == slot and a["cur"])


def xuong_chinh(att):
    acc = {}
    for ws in att["w"]:
        for b, w in ws:
            acc[NA[b]] = acc.get(NA[b], 0.0) + w
    return max(acc, key=acc.get)


def hop_slot(slot):
    P = np.array(att_cua(slot)["xy"], float).reshape(-1, 2)
    return P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()


def khop_khung(dat_):
    """khung concept (px, y xuống) ↔ thế giới con gốc dáng idle giây 0 (y lên): px = ox + s·X, py = oy − s·Y (bình phương tối thiểu
    trên tâm các mảnh kiểu "c": trùng chỗ concept và cùng dáng với part gốc)."""
    R, b, cap = [], [], []
    for m, d in dat_.items():
        if d.get("kieu") != "c" or not d.get("slot"):
            continue
        x0, y0, x1, y1 = hop_slot(d["slot"])
        gx, gy = d["goc"]
        w, hh = d["co"]
        R += [[(x0 + x1) / 2, 1, 0], [-(y0 + y1) / 2, 0, 1]]
        b += [gx + w / 2, gy + hh / 2]
        cap.append(m)
    (s, ox, oy), *_ = np.linalg.lstsq(np.array(R, float), np.array(b, float), rcond=None)
    lech = np.array(R) @ np.array([s, ox, oy]) - np.array(b)
    print(f"khớp khung concept: {s:.3f} px / đơn vị con gốc; lệch từng mốc (px): " +
          ", ".join(f"{m} {math.hypot(lech[2 * i], lech[2 * i + 1]):.0f}" for i, m in enumerate(cap)))
    return float(s), float(ox), float(oy)


def gan_cung(sk, slot, ten_anh, b, goc_tg, ex, ey, Wi):
    im = sk.images[ten_anh]
    w, h = im.width, im.height
    c = np.asarray(goc_tg) + ex * w / 2 + ey * h / 2
    Wb = Wi[b]
    lp = np.linalg.solve(Wb, np.array([c[0], c[1], 1.0]))
    n0, n1 = math.hypot(Wb[0, 0], Wb[1, 0]), math.hypot(Wb[0, 1], Wb[1, 1])
    rot = math.degrees(math.atan2(ex[1], ex[0])) - goc_mat(Wb)
    sk.atts[slot][ten_anh] = {"type": "region", "path": ten_anh, "x": float(lp[0]), "y": float(lp[1]), "rotation": rot,
                              "scaleX": float(np.hypot(*ex)) / n0, "scaleY": float(np.hypot(*ey)) / n1, "width": w, "height": h, "bone": b}


def _ghi_luoi(sk, slot, ten_anh, L, rows):
    im = sk.images[ten_anh]
    V0 = np.zeros((len(rows), 2))
    for i, row in enumerate(rows):
        for b, x, y, w in row:
            V0[i] += w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2]
    uv = np.asarray(L.pts, float) / np.array([im.width, im.height], float)
    sk.atts[slot][ten_anh] = {"type": "mesh", "path": ten_anh, "uv": uv, "tris": np.asarray(L.tris, int), "hull": L.nh, "V": V0,
                              "verts": rows, "width": im.width, "height": im.height}
    sk.luoi[(slot, ten_anh)] = L


def gan_luoi(sk, slot, ten_anh, L, V, trongso, Wi):
    """lưới của mình: đỉnh V (thế giới dáng idle 0), trọng số {xương: w} từng đỉnh."""
    inv, rows = {}, []
    for i, d in enumerate(trongso):
        row = []
        for b, w in d.items():
            if b not in inv:
                inv[b] = np.linalg.inv(Wi[b])
            lp = inv[b] @ np.array([V[i][0], V[i][1], 1.0])
            row.append((b, float(lp[0]), float(lp[1]), float(w)))
        rows.append(row)
    _ghi_luoi(sk, slot, ten_anh, L, rows)


def gan_theo_goc(sk, slot, ten_anh, L, V, att, Wi):
    """lưới dày của mình (đỉnh V, thế giới dáng idle 0) biến dạng ĐÚNG như lưới thưa của con gốc (att, cũng ở dáng idle 0): mỗi đỉnh là
    một điểm trong một tam giác của họ (toạ độ trọng tâm β) → bám xương b với trọng số W_b = Σ β_k w_b(k) và điểm gắn riêng từng xương
    q_b = Σ β_k w_b(k) v_k / W_b. Đỉnh nằm ngoài lưới của họ: bám như điểm gần nhất trên lưới, cộng nguyên khoảng lệch vào điểm gắn."""
    Q = np.array(att["xy"], float).reshape(-1, 2) * KG
    tr = np.array(att["tris"]).reshape(-1, 3)
    Wg = [{NA[k]: w for k, w in ws if w > 0.002} for ws in att["w"]]
    A, B_, C = Q[tr[:, 0]], Q[tr[:, 1]], Q[tr[:, 2]]
    v0, v1 = B_ - A, C - A
    den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
    den = np.where(np.abs(den) < 1e-9, 1e-9, den)

    def gan_canh(p, a, b):
        d = b - a
        t = np.clip(((p - a) * d).sum(axis=1) / np.maximum((d * d).sum(axis=1), 1e-12), 0, 1)
        return np.hypot(*(p - (a + t[:, None] * d)).T), t

    inv, rows, ngoai, xa = {}, [], 0, 0.0
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
            for n, w in Wg[vi].items():
                e = acc.setdefault(n, [0.0, np.zeros(2)])
                e[0] += bw * w
                e[1] += bw * w * Q[vi]
        row = []
        for n, (w, q) in acc.items():
            if abs(w) < 1e-5 or n not in sk.bi:
                continue
            if n not in inv:
                inv[n] = np.linalg.inv(Wi[n])
            g = q / w + lech
            lp = inv[n] @ np.array([g[0], g[1], 1.0])
            row.append((n, float(lp[0]), float(lp[1]), float(w)))
        tot = sum(r[3] for r in row) or 1.0
        rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    _ghi_luoi(sk, slot, ten_anh, L, rows)
    return ngoai, xa


def truc_lua(im, goc_px):
    """trục một ngọn lửa trên ảnh mảnh (px trong ảnh): gốc (điểm mảnh gần chỗ gốc nấp sau đá nhất), hai điểm giữa (trung bình các điểm
    có hình chiếu ở 1/3, 2/3 trục gốc → ngọn), ngọn (điểm xa gốc nhất, lùi vào trong 8%)."""
    a = np.asarray(im)[..., 3] > 100
    ys, xs = np.nonzero(a)
    Pp = np.stack([xs, ys], 1).astype(float)
    g = Pp[np.argmin(np.hypot(*(Pp - goc_px).T))]
    d = np.hypot(*(Pp - g).T)
    tip = Pp[np.argmax(d)]
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
    """trọng số mỗi đỉnh lưới lửa (px của ảnh) theo vị trí dọc đường gấp khúc J (gốc → ngọn): s < ~0,16 bám xương gốc lửa (đứng yên
    trên mai), còn lại chia mượt cho 3 đốt."""
    seg = [(J[k], J[k + 1]) for k in range(len(J) - 1)]
    lens = [np.hypot(*(q - p)) for p, q in seg]
    Ltot = sum(lens)
    out = []
    for v in Vpx:
        best, sbest = 1e18, 0.0
        acc = 0.0
        for (p, q), Lk in zip(seg, lens):
            d = q - p
            u = float(np.clip(np.dot(v - p, d) / np.dot(d, d), 0, 1))
            dd = float(np.hypot(*(p + d * u - v)))
            if dd < best:
                best, sbest = dd, (acc + u * Lk) / Ltot
            acc += Lk
        s = sbest
        w = {goc: 1 - em(s / 0.16)}
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


def pose_mau(clip, t, lap=False):
    P = Pose()
    dat(P, mau(clip, t, lap))
    return P


def dung():
    sk = Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")
    for b in I["bones"]:
        if b["name"] == "root":
            continue
        cha = NB[b["parent"]]
        sk.xuong(b["name"], "move" if cha == "root" else cha, b["x"] * KG, b["y"] * KG, goc=b["rot"], dai=b["len"] * KG,
                 sx=b["sx"], sy=b["sy"])
    P0 = pose_mau("idle_01", 0.0)
    Wi = sk.the_gioi(P0)

    dat_ = json.load(open(os.path.join(MANH, "dat.json"), encoding="utf-8"))
    thu_tu = dat_.pop("_thu_tu")
    mieng_px = dat_.pop("_mieng", MIENG)                  # dạng non: đầu phóng to nên mõm, mũi sừng dời chỗ (rua_lua_non.py ghi vào dat.json)
    sung_px = dat_.pop("_sung_mui", SUNG_MUI)
    khop_khung(dat_)                                  # chỉ in độ lệch để tham khảo
    s, ox, oy = KHOP
    tg = lambda px, py: np.array([(px - ox) / s * KG, (oy - py) / s * KG])      # noqa: E731
    k = PXU / s

    # xương lửa: <lửa>_g ở gốc ngọn (con của xương đá) → chuỗi 3 đốt; đặt theo thế giới DÁNG IDLE, đổi về dáng gốc qua xương đá
    lua_xuong = {}
    for t, bg in LUA_XUONG.items():
        if t not in dat_:
            continue
        g = Image.open(os.path.join(MANH, t + ".png"))
        gx, gy = dat_[t]["goc"]
        gp = dat_[t]["goc_lua"]
        Jpx = truc_lua(g, np.array([gp[0] - gx, gp[1] - gy], float))
        Jtg = [tg(gx + p[0], gy + p[1]) for p in Jpx]
        Mi = sk.W0[bg] @ np.linalg.inv(Wi[bg])
        pts = [(Mi @ np.array([*q, 1.0]))[:2] for q in Jtg]
        d0 = pts[1] - pts[0]
        sk.xuong(t + "_g", bg, pts[0][0], pts[0][1], math.degrees(math.atan2(d0[1], d0[0])), 0.0, the_gioi=True)
        names = [f"{t}_{j}" for j in range(3)]
        sk.chuoi(t, t + "_g", pts, ten_rieng=names)
        lua_xuong[t] = (bg, names, Jpx)
    Wi = sk.the_gioi(P0)

    for t in thu_tu:
        g = Image.open(os.path.join(MANH, t + ".png"))
        d = dat_[t]
        kieu = d.get("kieu", "c")
        if kieu == "r" and not d.get("slot"):
            continue                                      # lòng miệng chưa được đặt (thiếu mặt / hàm)
        if kieu == "r":                                   # mảnh khuất: đặt theo khung part của con gốc (tâm + chiều cao)
            x0, y0, x1, y1 = hop_slot(d["slot"])
            th = (y1 - y0) * 1.10
            tw = th * g.width / g.height
            kk = PXU * th / g.height
            im = anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * kk)), max(2, round(g.height * kk))), Image.LANCZOS).convert("RGBA"))
            ex = np.array([tw * KG / im.width, 0.0])
            ey = np.array([0.0, -th * KG / im.height])
            goc_ = np.array([((x0 + x1) / 2 - tw / 2) * KG, ((y0 + y1) / 2 + th / 2) * KG])
        else:
            im = anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * k)), max(2, round(g.height * k))), Image.LANCZOS).convert("RGBA"))
            gx, gy = d["goc"]
            ex = np.array([g.width / s * KG / im.width, 0.0])
            ey = np.array([0.0, -g.height / s * KG / im.height])
            goc_ = tg(gx, gy)
        sk.anh(t, im)
        an = t == "mat_tat" or t.endswith("_nguoi")
        if t in lua_xuong:
            bg, names, Jpx = lua_xuong[t]
            sk.slot(t, bg, t)
            L = luoi_vung(im, buoc_vien=8.0, buoc_trong=10.0, ten=t, in_tk=False)
            V = np.array([goc_ + ex * p[0] + ey * p[1] for p in L.pts])
            Vpx = np.asarray(L.pts, float) * (g.width / im.width)
            gan_luoi(sk, t, t, L, V, trong_so_lua(Vpx, Jpx, t + "_g", names), Wi)
            continue
        slot_goc = d.get("slot") or dat_.get(d.get("tren", ""), {}).get("slot")
        if t == "hong" or t == "mat_tat":
            slot_goc = "p_lian"
        att = att_cua(slot_goc)
        nx = {NA[b] for ws in att["w"] for b, w in ws if w > 0.01}
        if len(nx) == 1:
            b = next(iter(nx))
            sk.slot(t, b, t, an=an)
            gan_cung(sk, t, t, b, goc_, ex, ey, Wi)
        else:
            sk.slot(t, "move", t, an=an)
            L = luoi_vung(im, buoc_vien=10.0, buoc_trong=14.0, ten=t, in_tk=False)
            V = np.array([goc_ + ex * p[0] + ey * p[1] for p in L.pts])
            ng, xa = gan_theo_goc(sk, t, t, L, V, att, Wi)
            print(f"  {t}: lưới {L.n} đỉnh theo {slot_goc} ({len(nx)} xương); {ng} đỉnh ngoài lưới gốc, xa nhất {xa:.0f}")
    # chỗ tụ cầu lửa: trước mõm (con của mặt), mũi sừng gần (con của sừng)
    pm = tg(*mieng_px)
    sk.xuong("mieng", "bone34", *(np.linalg.solve(Wi["bone34"], np.array([*pm, 1.0]))[:2]))
    pc = tg(*sung_px)
    sk.xuong("cau", "bone36", *(np.linalg.solve(Wi["bone36"], np.array([*pc, 1.0]))[:2]))
    # chiều cao game: con dài hơn cao, lấy bề ngang thân / 1,16, không thấp hơn đỉnh mai. Đã thử / 1,42 (luật max_w): trong trận ở dạng 3
    # (size 1,14) con rộng ~60 % bề ngang màn hình, đuôi bị mép phải màn cắt (tour HoaFxTour "riêng Hỏa Quy", 2026-11-13)
    dm = dat_["mai"]
    dinh_mai = float(tg(0, dm["goc"][1] + 8)[1])
    x_trai = min(tg(v["goc"][0], 0)[0] for kk_, v in dat_.items() if v.get("kieu") != "r")
    x_phai = max(tg(v["goc"][0] + v["co"][0], 0)[0] for kk_, v in dat_.items() if v.get("kieu") != "r")
    cao = max(dinh_mai, (x_phai - x_trai) / 1.16)
    sk.xuong("far", "root", 0.9 * cao + 140.0, 0.45 * cao)
    for e, m in (("trung", "khung đòn trúng (húc)"), ("tu", "bắt đầu tụ cầu lửa"), ("phun", "bắn cầu lửa từ mõm"),
                 ("hut", "một ngọn lửa trên lưng bị hút về mũi sừng (chuỗi = tên ngọn lửa)"), ("day", "cầu trên sừng đầy"),
                 ("nem", "hất sừng phóng cầu"), ("gam", "gầm"), ("chan", "chân mọc ra"), ("dau", "đầu mọc ra"),
                 ("lua", "lửa bùng trên lưng"), ("tat", "lửa tắt"), ("sap", "thân sập xuống đất")):
        sk.su_kien(e, m)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; đỉnh mai {dinh_mai:.0f}, bề ngang {x_phai - x_trai:.0f}, "
          f"chiều cao game {cao:.0f}")
    return sk, dict(cao=cao, lua={t: v[1] for t, v in lua_xuong.items()}, P0=P0, khop=(s, ox, oy), dat=dat_)


# ---------------------------------------------------------------- tiện ích dáng
def hien(P, slot, a):
    P.alpha[slot] = float(min(1.0, max(0.0, a)))


def lua_lay(P, t, lua, chu_ky=1.333, bien=0.7, nga=0.0, chi=None, w=1.0):
    """lửa đung đưa nhẹ: mỗi ngọn sóng chạy từ gốc ra ngọn (đốt sau trễ pha, biên độ tăng dần) + họa âm bậc 2; nga = ngả cả ngọn (độ,
    dương = ngược kim = về phía đuôi)."""
    if w <= 0:
        return
    om = 2 * math.pi / chu_ky
    for i, (t_, names) in enumerate(lua.items()):
        if chi is not None and t_ not in chi:
            continue
        ph = i * 1.9
        for j, nm in enumerate(names):
            a = bien * (2.6 + 2.4 * j) * math.sin(om * t + ph - 0.95 * j) + bien * 1.2 * math.sin(2 * om * t + ph * 1.3 - 0.7 * j)
            P.rot(nm, w * (a + nga * (0.5 + 0.25 * j)))


def lua_co(P, lua, co, t=0.0, chu_ky=1.333):
    """cỡ từng ngọn: co = số hoặc {tên: số} (1 = đủ, 0 = tắt); thêm phập phồng 4%; ngọn nào cỡ < 0,06 thì ẩn hẳn."""
    om = 2 * math.pi / chu_ky
    for i, t_ in enumerate(lua):
        c = co if not isinstance(co, dict) else co.get(t_, 1.0)
        sc = c * (1.0 + 0.04 * math.sin(om * t * 2 + i * 1.3))
        sc = max(0.02, sc)
        P.scale(t_ + "_g", sc, max(0.02, 0.35 + 0.65 * sc) if sc < 1 else 1.0 + (sc - 1) * 0.4)
        if c < 0.999:
            hien(P, t_, em((c - 0.03) / 0.10))


def lo_xo(lua):
    return [LoXo(n, k=(150, 110, 80), damp=0.5, maxang=12.0) for n in lua.values()]


def mat_sang(P, v):
    hien(P, "mat_tat", 1 - v)


def nguoi(sk, P, v):
    for sl in sk.slots:
        if sl["name"].endswith("_nguoi"):
            hien(P, sl["name"], v)


def ham_mo(P, do):
    """há hàm thêm (độ): hàm dưới xoay quanh bản lề phía sau, đầu hàm hạ xuống."""
    P.rot("bone33", -do)


# ---------------------------------------------------------------- clip
def lam_clip(sk, info):
    lua = info["lua"]
    out = []
    d_i = CD["idle_01"][0]
    IDLE0 = mau("idle_01", 0.0)

    # idle: idle_01 của họ lặp 3 vòng (4 s) + lửa đung đưa nhẹ; vòng cuối "phì lửa": đầu hất nhẹ, hàm hé, lửa trên lưng bùng cao một nhịp
    I_DUR = 3 * d_i

    def idle(t, P):
        dat(P, mau("idle_01", t, True))
        bung = math.sin(math.pi * min(1.0, max(0.0, (t - 2.65) / 0.8)))
        P.rot("bone7", 5.0 * bung)
        ham_mo(P, 7.0 * bung)
        lua_lay(P, t, lua, I_DUR / 3, 0.7, nga=-3.0 * bung)
        lua_co(P, lua, 1.0 + 0.16 * bung, t, I_DUR / 3)
    out.append(Clip("idle", I_DUR, idle, loop=True, mem=lo_xo(lua)))

    d_w = CD["run_01"][0]

    def walk(t, P):
        dat(P, mau("run_01", t, True))
        lua_lay(P, t, lua, d_w, 0.8, nga=9.0)
        lua_co(P, lua, 1.0, t, d_w)
    out.append(Clip("walk", d_w, walk, loop=True, mem=lo_xo(lua)))

    d_h = CD["hit_01"][0]

    def hit(t, P):
        dat(P, mau("hit_01", t))
        b = math.sin(math.pi * min(1, t / d_h))
        lua_lay(P, t, lua, 0.4, 1.3, nga=14.0 * b)
        lua_co(P, lua, 1 - 0.18 * b, t, 0.4)
    out.append(Clip("hit", d_h, hit, mem=lo_xo(lua)))

    # attack: BÒ NHANH tới (hai bước run_01 tăng tốc, thân lao tới) → rạp người lấy đà → HÚC bằng sừng theo skill_03 (đỉnh lao = lúc
    # húc) → khựng → lùi về
    A_DUR, A_TRUNG, A_XA = 1.56, 0.86, 300.0
    BO = 1.9                                           # hệ số tăng tốc bước bò
    X3 = float(CD["skill_03"][1]["bone3"][:, 1].max())  # độ lao tới lớn nhất của thân trong skill_03 (đơn vị mình)

    def att_t(t):
        return cong([(0, 0.30), (0.40, 0.40), (0.56, 0.54), (0.74, 0.86), (A_TRUNG, 1.07), (1.00, 1.12), (A_DUR, 1.5)], t,
                    [None, em, None, vao, None, em])

    def attack(t, P):
        w_bo = 1 - em((t - 0.36) / 0.20)
        w_lui = em((t - 1.05) / 0.10) * (1 - em((t - 1.34) / 0.14))
        d = mau_tr("skill_03", att_t(t), 2)
        d["bone3"] = d["bone3"].copy()
        d["bone3"][1] = min(d["bone3"][1], 0.0) + max(d["bone3"][1], 0.0) * 0.45      # giữ cú rạp lùi, bớt cú trườn tới (move lo phần lao)
        run = mau("run_01", t * BO, True)
        d = pha(d, run, max(w_bo, 0.75 * w_lui))
        d = pha(IDLE0, d, em(t / 0.18))                # vào từ dáng đứng
        dat(P, d)
        x = cong([(0, 0.0), (0.06, 0.0), (0.44, A_XA * 0.72), (0.72, A_XA * 0.66), (A_TRUNG, A_XA - 0.45 * X3),
                  (1.03, A_XA - 0.45 * X3 - 6), (1.44, 0.0), (A_DUR, 0.0)], t, [None, em, em, vao, None, em, None])
        P.move("move", x, 0.0)
        P.move("bone3", rung(t, A_TRUNG, 9.0, 0.10, 15.0), rung(t, A_TRUNG, -5.0, 0.10, 15.0))
        lua_lay(P, t, lua, 0.5, 1.2, nga=cong([(0, 0.0), (0.25, 16.0), (0.65, 6.0), (A_TRUNG, 24.0), (1.05, -6.0), (1.35, -8.0), (A_DUR, 0.0)], t))
        lua_co(P, lua, 1.0, t, 0.5)
    out.append(Clip("attack", A_DUR, attack, ev=[(A_TRUNG, "trung", "")], trung=A_TRUNG, mem=lo_xo(lua)))

    # cast: thụp nhẹ → ĐỨNG LÊN NHẸ (skill_04, biên độ 0,6), HÁ MỒM → tụ cầu lửa trước mõm (VFX, xương `mieng`) → bắn: đầu giật tới, thân
    # giật lùi, lửa lưng bùng → ngậm mồm, về
    C_DUR, C_TU, C_PHUN = 1.60, 0.36, 0.90
    HA = 27.0

    def cast_t(t):
        return cong([(0, 0.0), (0.16, 0.09), (0.22, 0.20), (0.44, 0.34), (C_PHUN, 0.62), (1.10, 0.86), (C_DUR, 1.1667)], t,
                    [em, None, em, None, None, em])

    def cast(t, P):
        d = mau_tr("skill_04", cast_t(t), 1)
        nhe = 0.62 + 0.38 * (1 - em((t - 0.16) / 0.2)) + 0.38 * em((t - 1.15) / 0.3)       # chỉ đứng lên NHẸ
        d = pha(IDLE0, d, min(1.0, nhe))
        dat(P, d)
        mo = em((t - 0.26) / 0.14) * (1 - em((t - 1.05) / 0.18))
        ban = max(0.0, 1 - abs(t - (C_PHUN + 0.04)) / 0.10) if t >= C_PHUN - 0.02 else 0.0
        ham_mo(P, HA * mo + 6.0 * ban)
        tu = em((t - C_TU) / 0.15) * (1 - em((t - C_PHUN) / 0.05))
        P.rot("bone7", 4.0 * tu - 9.0 * ban)
        P.move("bone3", -10.0 * tu + 2.0 * math.sin(2 * math.pi * 21 * t) * tu - 16.0 * math.exp(-max(0.0, t - C_PHUN) / 0.12) *
               (1 if t >= C_PHUN else 0), rung(t, C_PHUN, 4.0, 0.12, 13.0))
        lua_lay(P, t, lua, 0.5, 0.9 + 0.5 * tu, nga=-6.0 * tu + 14.0 * math.exp(-max(0.0, t - C_PHUN) / 0.18) * (1 if t >= C_PHUN else 0))
        lua_co(P, lua, 1.0 + 0.10 * tu + 0.22 * math.exp(-max(0.0, t - C_PHUN) / 0.2) * (1 if t >= C_PHUN else 0), t, 0.5)
    out.append(Clip("cast", C_DUR, cast, ev=[(C_TU, "tu", ""), (C_PHUN, "phun", "")], trung=C_PHUN, mem=lo_xo(lua)))

    # skill (chiêu cuối): thụp người ghìm chân → từng ngọn lửa trên lưng (xa sừng trước) vươn về phía sừng rồi CO LẠI TẮT, cầu lửa lớn dần ở
    # mũi sừng (VFX; xương `cau` phóng to dần, sự kiện `hut` mỗi ngọn) → hết lửa: ngửa đầu lấy đà → HẤT SỪNG tới trước phóng cầu (`nem`) →
    # thân giật lùi → lửa mọc lại từng ngọn, về idle
    S_DUR = 2.70
    H0, H_CACH, H_DAI = 0.32, 0.125, 0.30
    T_DAY = H0 + H_CACH * (len(HUT) - 1) + H_DAI          # hút xong ngọn cuối
    T_NEM = T_DAY + 0.26
    MOC0, MOC_CACH = T_NEM + 0.42, 0.07
    # dạng có ít ngọn lửa hơn (rùa non): các ngọn CÓ MẶT chia đều quãng hút; chỉ một ngọn thì nó co chậm suốt quãng (cầu vẫn đầy đúng T_DAY)
    HUT_CO = [x for x in HUT if x in lua]
    HC_DAI = H_DAI if len(HUT_CO) > 1 else T_DAY - H0 - 0.08
    HC_CACH = (T_DAY - H_DAI - H0) / (len(HUT_CO) - 1) if len(HUT_CO) > 1 else 0.0
    NGAM = mau("skill_04", 0.16)                         # dáng thụp
    CHIA = mau("skill_02", 0.40)                         # dáng cúi đầu chĩa sừng tới trước

    def skill(t, P):
        thup = em(t / 0.26) * (1 - em((t - (T_NEM - 0.10)) / 0.10))
        hat = em((t - (T_NEM - 0.07)) / 0.07) * (1 - em((t - (T_NEM + 0.30)) / 0.34))
        d = pha(IDLE0, NGAM, 0.75 * thup)
        d = pha(d, CHIA, hat)
        dat(P, d)
        nap = min(1.0, max(0.0, (t - H0) / (T_DAY - H0))) if t < T_NEM else 0.0
        da = em((t - T_DAY) / 0.18) * (1 - em((t - (T_NEM - 0.07)) / 0.06))        # ngửa đầu lấy đà
        P.rot("bone7", 7.0 * nap * (1 - hat) + 12.0 * da)
        P.rot("bone3", 2.5 * da)
        gong = nap * (1 - hat) * (1 if t < T_NEM else 0)
        P.move("bone3", 2.2 * gong * math.sin(2 * math.pi * 19 * t) - 22.0 * math.exp(-max(0.0, t - T_NEM) / 0.14) * (1 if t >= T_NEM else 0)
               + 26.0 * hat, -8.0 * gong + rung(t, T_NEM, 5.0, 0.12, 13.0))
        P.scale("cau", 0.12 + 0.88 * nap if t < T_NEM else 1.0)
        co = {}
        Wc = None
        for i, ten in enumerate(HUT_CO):
            u = (t - (H0 + HC_CACH * i)) / HC_DAI
            moc = bat(t, MOC0 + MOC_CACH * i, 0.26, 1.25)
            if t >= MOC0 + MOC_CACH * i:
                co[ten] = max(0.02, moc)
            elif u <= 0:
                co[ten] = 1.0
            else:
                uu = min(1.0, u)
                co[ten] = max(0.0, (1 + 0.28 * math.sin(math.pi * min(1.0, uu / 0.45))) * (1 - em((uu - 0.30) / 0.70)))
                # vươn về phía mũi sừng
                if Wc is None:
                    Wc = sk.the_gioi(P)
                g = Wc[ten + "_g"]
                v = Wc["cau"][:2, 2] - g[:2, 2]
                lech = math.degrees(math.atan2(v[1], v[0])) - goc_mat(g)
                lech -= 360.0 * round(lech / 360.0)
                P.rot(ten + "_g", max(-38.0, min(38.0, lech)) * em(uu / 0.35) * 0.8)
        lua_lay(P, t, lua, 0.5, 0.9 + 0.6 * gong)
        lua_co(P, lua, co, t, 0.5)
    ev = [(0.26, "tu", "")] + [(round(H0 + HC_CACH * i, 3), "hut", ten) for i, ten in enumerate(HUT_CO)]
    ev += [(round(T_DAY, 3), "day", ""), (round(T_NEM, 3), "nem", ""), (round(MOC0, 3), "lua", "")]
    out.append(Clip("skill", S_DUR, skill, ev=ev, trung=T_NEM, mem=lo_xo(lua)))

    # appear: chỉ có CÁI MAI nằm sát đất (đầu, bốn chân, đuôi rụt trong mai; chưa có lửa) → mai lắc hai nhịp → hai chân sau, hai chân
    # trước thò ra đội mai lên → đuôi → đầu → lửa bùng trên lưng → GẦM (đứng cao, ngẩng đầu há hàm, rung) → về idle
    P_DUR = 2.70
    HA_THAN = 78.0 * KG / 0.8
    LICH = {"chan_sau_xa": 0.62, "chan_sau_gan": 0.56, "chan_truoc_xa": 0.80, "chan_truoc_gan": 0.74, "duoi": 0.98, "dau": 1.12}
    T_LUA, T_GAM = 1.42, 1.72

    def appear(t, P):
        gam = em((t - (T_GAM - 0.10)) / 0.16) * (1 - em((t - (T_GAM + 0.50)) / 0.30))
        d = pha(IDLE0, mau("skill_04", 0.55), 0.85 * gam)
        dat(P, d)
        co = {k_: bat(t, t0, 0.24, 1.16) for k_, t0 in LICH.items()}
        sau = (co["chan_sau_xa"] + co["chan_sau_gan"]) / 2
        truoc = (co["chan_truoc_xa"] + co["chan_truoc_gan"]) / 2
        nang = min(1.0, (sau + truoc) / 2)
        lac = (math.sin(2 * math.pi * (t - 0.22) / 0.16) * math.exp(-(t - 0.22) / 0.25) if 0.22 < t < 0.6 else 0.0)
        P.move("bone3", 3.0 * lac, -HA_THAN * (1 - nang))
        P.rot("bone3", 2.2 * lac + 5.0 * (min(1.0, sau) - min(1.0, truoc)))
        P.scale("bone3", cong([(0, 0.92), (0.14, 1.03), (0.22, 1.0)], t))
        for k_, (xg, manh) in NHOM.items():
            sc = max(0.03, co[k_])
            P.scale(xg, sc)
            for m in manh:
                if m in sk.si and not m.endswith("_nguoi") and m != "mat_tat":
                    hien(P, m, em((co[k_] - 0.04) / 0.12))
        vao_ = em(t / 0.14)
        for m in ("mai", "bung", "cot_gan", "cot_xa"):
            if m in sk.si:
                hien(P, m, vao_)
        ham_mo(P, 24.0 * gam)
        P.rot("bone7", 6.0 * gam)
        P.move("bone3", 2.5 * math.sin(2 * math.pi * 20 * t) * gam, 0.0)
        mat_sang(P, em((t - (LICH["dau"] + 0.20)) / 0.10) if co["dau"] > 0.05 else 1.0)
        if co["dau"] <= 0.05:
            hien(P, "mat_tat", 0.0)
        chay = {}
        for i, ten in enumerate(lua):
            chay[ten] = bat(t, T_LUA + 0.045 * i, 0.26, 1.35) * (1 + 0.20 * gam)
        lua_lay(P, t, lua, 0.5, 0.8 + 0.8 * gam, nga=-5.0 * gam)
        lua_co(P, lua, chay, t, 0.5)
    out.insert(0, Clip("appear", P_DUR, appear, ev=[(0.56, "chan", ""), (0.74, "chan", ""), (1.12, "dau", ""), (T_LUA, "lua", ""),
                                                    (T_GAM, "gam", "")], mem=lo_xo(lua)))

    # die: giật lùi (hit_01) → LỬA TẮT từng ngọn, mắt tắt, pha lê nguội → bốn chân khuỵu, thân QUỴ sập xuống (dáng nằm cuối die_01), đầu
    # gục → tan
    D_DUR, TAN = 1.75, 0.45
    NAM = mau("die_01", 1.0)

    def die(t, P):
        w = cong([(0.0, 0.0), (0.50, 0.0), (0.70, 0.20), (1.04, 1.0)], t, [None, vao, em])
        giat = mau_tr("hit_01", min(t, 0.44) * 0.5, 1)                 # cú giật lùi của hit_01, chậm bằng nửa
        d = pha(IDLE0, giat, em(t / 0.06)) if t < 0.5 else pha(pha(giat, IDLE0, 0.5 * em((t - 0.5) / 0.2)), NAM, w)
        dat(P, d)
        P.move("bone3", rung(t, 1.00, 3.0, 0.10, 12.0), rung(t, 1.00, -7.0, 0.12, 9.0))
        tat = {}
        for i, ten in enumerate(lua):
            u = (t - (0.14 + 0.07 * ((i * 3) % 7))) / 0.34
            chap = 0.75 + 0.25 * math.sin(2 * math.pi * 11 * t + i) if 0 < u < 1 else 1.0
            tat[ten] = max(0.0, (1 - em(u)) * chap)
        lua_lay(P, t, lua, 0.4, 1.2, nga=10.0)
        lua_co(P, lua, tat, t, 0.4)
        mat_sang(P, 1 - em((t - 0.62) / 0.14))
        nguoi(sk, P, em((t - 0.50) / 0.30))
        a = 1.0 - em((t - D_DUR) / (TAN - 0.05))
        if a < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = P.alpha.get(sl["name"], sl["alpha"]) * a
            hien(P, "hong", 0.0)                       # lúc tan các lớp trong dần: đừng để lòng miệng cam lộ qua mặt
    out.append(Clip("die", D_DUR + TAN, die, ev=[(0.14, "tat", ""), (1.00, "sap", "")], mem=lo_xo(lua)))
    return out


def main(a):
    sk, info = dung()
    clips = lam_clip(sk, info)
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 1.0
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB") for P in Ps]
        cot = min(len(ims), 6)
        hang = (len(ims) + cot - 1) // cot
        out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang), (150, 150, 150))
        for i, im in enumerate(ims):
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    xuat.xuat_het(sk, clips, RA, TEN, "Rùa golem lửa dạng 1, rùa non (rua_lua_non)" if NON else "Rùa golem lửa dạng 2 (rua_lua_1)",
                  dang=1 if NON else 2, so_dang=2, dung_yen=("cast", "skill"),
                  lao=("attack",), far=(), cao=info["cao"], ma_goc=None, tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001},
                  khop_idle=0.2)


if __name__ == "__main__":
    main(sys.argv[1:])
