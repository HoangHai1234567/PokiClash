# -*- coding: utf-8 -*-
"""Mắt lửa bọc giáp (mat_lua, tướng thứ 2 đảo Hỏa): rig trên bộ xương của con gốc monster_3342. Mảnh của mình là MẢNH CỨNG đặt đúng chỗ
concept đã duyệt (quả cầu và hai khúc tay dùng trọng số lưới của họ); chuyển động nền lấy mẫu từ clip của họ bằng runtime Spine thật
(<scan>/sample.json, trường `l`: biến đổi riêng ĐÃ áp 12 transform constraint), clip riêng dựng bằng mã trên chính rig của mình.

- Đủ xương của họ (bỏ `root` của họ: thay bằng root + move của mình); không có ràng buộc (đã nướng vào mẫu khung).
- Lớp lửa sau lưng (mảnh thêm): xương `lua` (con của quả cầu `bone`) + mỗi lưỡi lửa một chuỗi hai đốt, lưới có trọng số, lay lệch pha +
  lò xo; hai giọt lửa trên xương `giot*`.
- Đổi hình: `mat` / `mat_tat` (mắt sáng / tắt), `cau` / `cau_tat` (cầu lửa / cầu nguội) bằng độ đậm.
- Xương `mieng` ở con ngươi: chỗ bắn tia lửa (cast). Sự kiện: phun, het_phun, trung, xoay, roi, cham_dat, sang, tat.

Người dùng (2026-11-13): appear = bộ giáp nằm đất, mắt sáng lên, phồng lên, tay trồi ra rồi bay lên; idle, walk như họ; đánh thường
bay tới đấm một phát nặng, nhanh; cast giống skill_02 + tia lửa từ giữa mắt; chiêu cuối dang hai tay xoay chong chóng quanh thân rồi
lao vào đập liên tục; die rơi xuống, mắt tắt, giáp rơi ra.

    mat_lua_rig.py                       dựng, xuất inbox/mat_lua_1/rig/ (JSON Spine, atlas, .atomik, tờ khung, xem.html)
    mat_lua_rig.py soi <clip> <giây,..> [tỉ lệ]    khung lớn nền xám → rig/soi_<clip>.png
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
import pickle  # noqa: E402
import subprocess  # noqa: E402
from quai import anh, hoat, xuat, soi, tienhoa  # noqa: E402
from quai.khung import Sk, mat, goc_mat  # noqa: E402
from quai.hoat import Clip, LoXo  # noqa: E402
from quai.luoi import luoi_o, luoi_vung  # noqa: E402
import mat_lua as G  # noqa: E402

K = G.K
TEN = f"mat_lua_{K}"
RA = os.path.join(G.BASE, "rig")
MANH = os.environ.get("ML_MANH") or os.path.join(G.BASE, "manh")
BO_CUC = not os.path.exists(os.path.join(MANH, "dat.json"))          # dạng chưa có mảnh: dựng bằng da dạng 1 (hình bố cục)
if BO_CUC:
    MANH = os.path.join(HERE, "inbox", "mat_lua_1", "manh")
KHOP = os.path.join(HERE, "inbox", "mat_lua_1", "manh", "khop.json")    # khung concept ↔ thế giới con gốc, đo ở dạng 1 (dạng 2 dùng lại)
# DẠNG 2 "to hơn, chiến hơn" (người dùng 2026-11-13): tỉ lệ mảnh dạng 2 so với dạng 1, áp vào tư thế lúc dựng HÌNH BỐ CỤC bằng da dạng 1
# (bo_cuc); rig dạng 2 lấy mảnh to sẵn từ concept dạng 2 nên không đổi tỉ lệ xương
TI = {2: {"bone14": 1.30, "bone17": 1.30, "bone10": 1.22, "bone11": 1.22, "bone5": 1.15, "bone4": 1.10, "bone7": 1.15,
          "bone6": 1.12, "bone8": 1.12, "bone9": 1.12, "lua": 1.22}}.get(K, {})
BO_CUC_THU = 0.86                    # hình bố cục dạng 2: thu cả con cho vừa khung concept (trong game dạng 2 to hơn nhờ cỡ tướng)
SCAN = G.scan()
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
A0 = json.load(open(os.path.join(SCAN, "att_idle0.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample.json"), encoding="utf-8"))
NB = [b["name"] for b in I["bones"]]
KG = 0.85                    # đơn vị rig con gốc → đơn vị rig của mình
NHE = os.environ.get("ML_NHE") == "1"   # bản NHẸ (ảnh nhỏ) của dạng 2, chỉ để gộp vào dạng 1 cho clip tiến hóa
PXU = 0.70 if NHE else 1.30  # pixel ảnh atlas cho mỗi đơn vị rig con gốc
FPS = 30.0
MAX_W = 1.30                 # tỉ lệ rộng / chiều cao game tối đa (dạng 1: 1,28)
NHIEU_XUONG = ("cau", "cau_tat", "tay_gan", "tay_xa")     # mảnh dùng trọng số lưới của họ (slot của họ bám nhiều xương)
XUONG_MANH = {"mat": "bone18", "mat_tat": "bone18", "mu": "bone5", "nho_mat": "bone4", "nho_phai": "bone7", "vai_gan": "bone10",
              "vai_xa": "bone11", "duoi_trai": "bone6", "duoi_giua": "bone8", "duoi_phai": "bone9", "nam_gan": "bone14", "nam_xa": "bone17"}
GIAP = ["mu", "nho_mat", "nho_phai", "vai_gan", "vai_xa", "duoi_trai", "duoi_giua", "duoi_phai"]
# lưỡi lửa: (gốc, giữa, ngọn) trên khung concept (px), đọc trên mảnh lửa đã cắt
LUOI = [((560, 470), (440, 300), (350, 180)), ((640, 420), (590, 230), (500, 55)), ((700, 400), (690, 230), (650, 120)),
        ((780, 380), (800, 210), (760, 70)), ((860, 380), (900, 260), (905, 170)), ((520, 540), (380, 440), (290, 400)),
        ((500, 590), (350, 520), (262, 470))]
GIOT = {"giot1": (452, 50), "giot2": (318, 250)}
CON_NGUOI = (947, 650)
MANH_DANG = 1.0 if K == 1 else 1.5   # độ mạnh rung / khựng theo dạng           # tâm con ngươi trên concept (chỗ bắn tia)
CAO_Y = None                     # y concept của đỉnh tính chiều cao game (None: đỉnh tấm giáp đầu)
if K == 2:                       # số đo trên concept dạng 2
    LUOI = [((560, 480), (420, 280), (290, 200)), ((640, 440), (600, 220), (560, 40)), ((760, 420), (800, 220), (830, 60)),
            ((880, 400), (960, 260), (995, 160)), ((520, 560), (330, 420), (240, 330)), ((500, 620), (300, 580), (215, 520)),
            ((700, 420), (690, 260), (680, 150))]
    GIOT = {"giot1": (445, 65), "giot2": (258, 275)}
    CON_NGUOI = (935, 655)
    CAO_Y = 255                  # thân tấm đầu (không tính gai giữa)


# ---------------------------------------------------------------- chuyển động nền của họ (mẫu khung, đã áp ràng buộc)
def _cd():
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        res = {}
        for i, b0 in enumerate(I["bones"]):
            if b0["name"] == "root":
                continue
            Am = np.array([[F["l"][i][2] - b0["rot"], (F["l"][i][0] - b0["x"]) * KG, (F["l"][i][1] - b0["y"]) * KG,
                            F["l"][i][3] / (b0["sx"] or 1.0), F["l"][i][4] / (b0["sy"] or 1.0)] for F in fr])
            Am[:, 0] = np.degrees(np.unwrap(np.radians(Am[:, 0])))
            Am[:, 0] -= 360.0 * round(Am[0, 0] / 360.0)
            if np.abs(Am - np.array([0, 0, 0, 1, 1])).max() > 1e-4:
                res[b0["name"]] = Am
        mat_x = [F["n"][NB.index("bone18") and [s["name"] for s in I["slots"]].index("yanjing_01")] == "yanjing_02" for F in fr]
        out[clip] = (float(v["dur"]), res, mat_x)
    return out


CD = _cd()


def mau(clip, t, lap=False):
    """{xương: (lệch xoay, dời x, y, tỉ lệ x, y)} của clip họ ở giây t (nội suy giữa hai khung mẫu)."""
    dur, R, _ = CD[clip]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    out = {}
    for b, arr in R.items():
        n = len(arr)
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        out[b] = arr[i0] * (1 - w) + arr[i1] * w
    return out


def mat_x(clip, t):
    dur, _, mx = CD[clip]
    return mx[min(len(mx) - 1, int(round(min(max(t, 0.0), dur) * FPS)))]


def pha(a, b, w):
    """pha hai dáng mẫu."""
    out = {}
    for k in set(a) | set(b):
        va = a.get(k, np.array([0, 0, 0, 1, 1.0]))
        vb = b.get(k, np.array([0, 0, 0, 1, 1.0]))
        out[k] = va * (1 - w) + vb * w
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


# ---------------------------------------------------------------- dựng rig
def khop_khung(dat_):
    """khung concept (px, y xuống) ↔ thế giới con gốc dáng idle giây 0 (y lên): px = ox + s·X, py = oy − s·Y."""
    by = {a["slot"]: a for a in A0["atts"] if a["cur"]}
    R, b = [], []
    cap = []
    for m, d in dat_.items():
        sl = d.get("slot")
        if not sl or m.endswith("_tat") or sl not in by:
            continue
        P = np.array(by[sl]["xy"], float).reshape(-1, 2)
        X, Y = (P[:, 0].min() + P[:, 0].max()) / 2, (P[:, 1].min() + P[:, 1].max()) / 2
        gx, gy = d["goc"]
        w, hh = d["co"]
        R += [[X, 1, 0], [-Y, 0, 1]]
        b += [gx + w / 2, gy + hh / 2]
        cap.append(m)
    (s, ox, oy), *_ = np.linalg.lstsq(np.array(R, float), np.array(b, float), rcond=None)
    lech = np.array(R) @ np.array([s, ox, oy]) - np.array(b)
    print(f"khớp khung concept: {s:.3f} px / đơn vị con gốc; lệch từng mốc (px): " +
          ", ".join(f"{m} {math.hypot(lech[2 * i], lech[2 * i + 1]):.0f}" for i, m in enumerate(cap)))
    return float(s), float(ox), float(oy)


def gan_cung(sk, slot, ten_anh, b, goc_tg, ex, ey, Wi):
    """mảnh cứng: ảnh w×h đặt ở thế giới DÁNG IDLE GIÂY 0 (góc trên-trái goc_tg, véc-tơ một px ảnh theo x: ex, theo y (xuống): ey),
    bám xương b; toạ độ gắn tính theo ma trận của b ở dáng đó (clip luôn đi qua dáng này)."""
    im = sk.images[ten_anh]
    w, h = im.width, im.height
    c = np.asarray(goc_tg) + ex * w / 2 + ey * h / 2
    Wb = Wi[b]
    lp = np.linalg.solve(Wb, np.array([c[0], c[1], 1.0]))
    n0, n1 = math.hypot(Wb[0, 0], Wb[1, 0]), math.hypot(Wb[0, 1], Wb[1, 1])
    rot = math.degrees(math.atan2(ex[1], ex[0])) - goc_mat(Wb)
    sk.atts[slot][ten_anh] = {"type": "region", "path": ten_anh, "x": float(lp[0]), "y": float(lp[1]), "rotation": rot,
                              "scaleX": float(np.hypot(*ex)) / n0, "scaleY": float(np.hypot(*ey)) / n1, "width": w, "height": h, "bone": b}


def gan_luoi(sk, slot, ten_anh, L, V, trongso, Wi):
    """lưới có trọng số: V = toạ độ thế giới DÁNG IDLE GIÂY 0 từng đỉnh; toạ độ gắn theo ma trận từng xương ở dáng đó."""
    im = sk.images[ten_anh]
    inv = {}
    verts = []
    V0 = np.zeros((len(V), 2))
    for i, d in enumerate(trongso):
        row = []
        for b, w in d.items():
            if b not in inv:
                inv[b] = np.linalg.inv(Wi[b])
            lp = inv[b] @ np.array([V[i][0], V[i][1], 1.0])
            row.append((b, float(lp[0]), float(lp[1]), float(w)))
            V0[i] += w * (sk.W0[b] @ lp)[:2]
        verts.append(row)
    uv = np.asarray(L.pts, float) / np.array([im.width, im.height], float)
    sk.atts[slot][ten_anh] = {"type": "mesh", "path": ten_anh, "uv": uv, "tris": np.asarray(L.tris, int), "hull": L.nh, "V": V0,
                              "verts": verts, "width": im.width, "height": im.height}
    sk.luoi[(slot, ten_anh)] = L


def trong_so_ho(slot_ho, V):
    """trọng số từng đỉnh V (thế giới rig mình, dáng idle giây 0) nội suy từ lưới của họ (toạ độ trọng tâm trên tam giác chứa đỉnh;
    nằm ngoài thì tam giác gần nhất, toạ độ trọng tâm kẹp dương)."""
    a = [x for x in A0["atts"] if x["slot"] == slot_ho and x["cur"]][0]
    P = np.array(a["xy"], float).reshape(-1, 2) * KG
    T = np.array(a["tris"], int).reshape(-1, 3)
    Wv = a["w"]
    out = []
    for v in V:
        best, bb = 1e18, None
        for t in T:
            p0, p1, p2 = P[t]
            M = np.array([[p1[0] - p0[0], p2[0] - p0[0]], [p1[1] - p0[1], p2[1] - p0[1]]])
            if abs(np.linalg.det(M)) < 1e-9:
                continue
            l1, l2 = np.linalg.solve(M, v - p0)
            be = np.array([1 - l1 - l2, l1, l2])
            d = -min(0.0, be.min())
            if d < best:
                best, bb = d, (t, be)
            if d == 0:
                break
        t, be = bb
        be = np.clip(be, 0, None)
        be /= be.sum()
        w = {}
        for k in range(3):
            for bi, ww in Wv[t[k]]:
                w[NB[bi]] = w.get(NB[bi], 0.0) + be[k] * ww
        w = {k: x for k, x in w.items() if x > 0.02}
        s_ = sum(w.values())
        out.append({k: x / s_ for k, x in w.items()})
    return out


def pose_mau(sk, clip, t, lap=False):
    from quai.khung import Pose
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
    P0 = pose_mau(sk, "idle_01", 0.0)
    Wi = sk.the_gioi(P0)

    dat_ = json.load(open(os.path.join(MANH, "dat.json"), encoding="utf-8"))
    thu_tu = dat_.pop("_thu_tu")
    if K == 1:
        s, ox, oy = khop_khung(dat_)
        json.dump(dict(s=s, ox=ox, oy=oy), open(KHOP, "w"))
    else:
        q = json.load(open(KHOP))
        s, ox, oy = q["s"], q["ox"], q["oy"]
        if not BO_CUC:
            s *= BO_CUC_THU          # concept dạng 2 vẽ trên hình bố cục đã thu quanh gốc thế giới: trả lại cỡ thật để mảnh khớp xương
    tg = lambda px, py: np.array([(px - ox) / s * KG, (oy - py) / s * KG])      # noqa: E731

    # lửa: xương gốc ở tâm đáy lửa, mỗi lưỡi một chuỗi hai đốt
    goc_lua = tg(700, 470)
    sk.xuong("lua", "bone", *(np.linalg.solve(Wi["bone"], np.array([*goc_lua, 1.0]))[:2]))
    lua_xuong = []
    for i, (a, m, n) in enumerate(LUOI):
        A_, M_, N_ = tg(*a), tg(*m), tg(*n)
        names = [f"lua{i}a", f"lua{i}b"]
        # đặt theo toạ độ thế giới DÁNG IDLE: đổi về dáng gốc qua xương cha `lua` (dáng gốc và idle chỉ lệch phép dời / xoay của cha)
        Mi = sk.W0["lua"] @ np.linalg.inv(_W_idle_lua(sk, Wi))
        pts = [(Mi @ np.array([*q, 1.0]))[:2] for q in (A_, M_, N_)]
        sk.chuoi(f"lua{i}", "lua", pts, ten_rieng=names)
        lua_xuong.append(names)
    for g, (gx, gy) in GIOT.items():
        q = (sk.W0["lua"] @ np.linalg.inv(_W_idle_lua(sk, Wi)) @ np.array([*tg(gx, gy), 1.0]))[:2]
        sk.xuong(g, "lua", *(np.linalg.solve(sk.W0["lua"], np.array([*q, 1.0]))[:2]))
    Wi = sk.the_gioi(P0)

    # mảnh
    k = PXU / s
    for t in thu_tu:
        g = Image.open(os.path.join(MANH, t + ".png"))
        im = anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * k)), max(2, round(g.height * k))), Image.LANCZOS).convert("RGBA"))
        sk.anh(t, im)
        gx, gy = dat_[t]["goc"]
        ex = np.array([g.width / s * KG / im.width, 0.0])
        ey = np.array([0.0, -g.height / s * KG / im.height])
        goc_ = tg(gx, gy)
        an = t in ("mat_tat", "cau_tat")
        if t in ("lua",):
            sk.slot(t, "lua", t)
            L = luoi_vung(im, buoc_vien=14.0, buoc_trong=18.0, ten=t, in_tk=False)
            V = np.array([goc_ + ex * p[0] + ey * p[1] for p in L.pts])
            sk.anh(t, im)
            gan_luoi(sk, t, t, L, V, trong_so_lua(V, lua_xuong, Wi, tg), Wi)
        elif t in GIOT:
            sk.slot(t, t, t)
            gan_cung(sk, t, t, t, goc_, ex, ey, Wi)
        elif t in NHIEU_XUONG:
            sl = t.replace("_tat", "")
            sk.slot(t, "bone", t, an=an)
            L = luoi_o(im.width, im.height, 7, 7)
            V = np.array([goc_ + ex * p[0] + ey * p[1] for p in L.pts])
            gan_luoi(sk, t, t, L, V, trong_so_ho(dat_[t]["slot"], V), Wi)
        else:
            b = XUONG_MANH[t]
            sk.slot(t, b, t, an=an)
            gan_cung(sk, t, t, b, goc_, ex, ey, Wi)
    # chỗ bắn tia: tâm con ngươi (khung concept ~ (947, 650))
    pm = tg(*CON_NGUOI)
    sk.xuong("mieng", "bone18", *(np.linalg.solve(Wi["bone18"], np.array([*pm, 1.0]))[:2]))
    cao = float(tg(0, CAO_Y if CAO_Y is not None else dat_["mu"]["goc"][1] + 12)[1])           # chiều cao game: đỉnh tấm giáp đầu (không tính lửa)
    sk.xuong("far", "root", 0.9 * cao + 140.0, 0.45 * cao)
    for e, m in (("trung", "khung đòn trúng"), ("phun", "tia lửa bắn ra từ con ngươi"), ("het_phun", "tia lửa tắt"),
                 ("xoay", "bắt đầu xoay chong chóng"), ("sang", "mắt sáng lên"), ("tat", "mắt tắt"), ("roi", "giáp bắt đầu rơi"),
                 ("cham_dat", "mảnh chạm đất")):
        sk.su_kien(e, m)
    # tâm HÌNH quả cầu (gốc xương `bone` thấp hơn tâm cầu) và tâm hình hai nắm tay, trong hệ xương của chúng
    sa = sk.atts["cau"]["cau"]
    Vc = np.array([sum(w * (Wi[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in row) for row in sa["verts"]])
    c_cau = np.linalg.solve(Wi["bone"], np.array([*((Vc.min(0) + Vc.max(0)) / 2), 1.0]))[:2]
    tam_nam = {b: np.array([sk.atts[t][t]["x"], sk.atts[t][t]["y"]]) for t, b in (("nam_gan", "bone14"), ("nam_xa", "bone17"))}
    r_cau = float((Vc.max(0) - Vc.min(0)).mean() / 2)
    a_n = sk.atts["nam_gan"]["nam_gan"]
    r_nam = 0.5 * max(a_n["width"] * a_n["scaleX"], a_n["height"] * a_n["scaleY"])
    r_quay = r_cau + 0.72 * r_nam                     # nắm tay quay sát mép cầu (dạng 1: 120)
    # con bè ngang (dạng 2 rộng 1,54 lần chiều cao): game co tướng theo chiều cao nên khai chiều cao hiệu dụng ≥ bề rộng / MAX_W để không
    # tràn mép sân (cách "max_w" của beast.py; tiến hóa dùng chiều cao hiệu dụng nên không giật cỡ)
    x0_, _, x1_, _ = soi.Ve(sk).bao(P0)
    if (x1_ - x0_) / cao > MAX_W:
        print(f"bề rộng {x1_ - x0_:.0f} = {(x1_ - x0_) / cao:.2f} × chiều cao {cao:.0f}: khai chiều cao {(x1_ - x0_) / MAX_W:.0f}")
        cao = (x1_ - x0_) / MAX_W
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao game {cao:.0f}")
    return sk, dict(cao=cao, lua=lua_xuong, P0=P0, c_cau=c_cau, tam_nam=tam_nam, r_quay=r_quay, khop=(s, ox, oy))


def _W_idle_lua(sk, Wi):
    """ma trận thế giới DÁNG IDLE của xương lua (con của bone, không khoá riêng): Wi[bone] · L_lua."""
    b = sk.bones[sk.bi["lua"]]
    return Wi["bone"] @ mat(b["x"], b["y"], b["rot"], b["sx"], b["sy"])


def trong_so_lua(V, lua_xuong, Wi, tg):
    """mỗi đỉnh của mảnh lửa: gần lưỡi nào thì theo chuỗi lưỡi đó (đốt dưới / đốt trên theo vị trí dọc lưỡi); phần đáy theo `lua`."""
    out = []
    for v in V:
        ws = {"lua": 0.08}
        for (a, m, n), names in zip(LUOI, lua_xuong):
            A_, M_, N_ = tg(*a), tg(*m), tg(*n)
            best, tt = 1e18, 0.0
            for k, (p, q) in enumerate(((A_, M_), (M_, N_))):
                d = q - p
                u = float(np.clip(np.dot(v - p, d) / np.dot(d, d), 0, 1))
                dd = float(np.hypot(*(p + d * u - v)))
                if dd < best:
                    best, tt = dd, k + u
            L = float(np.hypot(*(N_ - A_)))
            aff = math.exp(-(best / (0.22 * L)) ** 2)
            f = em(tt / 0.6)
            ws["lua"] += aff * (1 - f)
            ws[names[0]] = ws.get(names[0], 0.0) + aff * f * (1 - em((tt - 0.7) / 0.8))
            ws[names[1]] = ws.get(names[1], 0.0) + aff * f * em((tt - 0.7) / 0.8)
        ws = {k: x for k, x in ws.items() if x > 1e-3}
        top = sorted(ws.items(), key=lambda kv: -kv[1])[:4]
        s_ = sum(x for _, x in top)
        out.append({k: x / s_ for k, x in top})
    return out


# ---------------------------------------------------------------- tiện ích dáng
def dat_tg(sk, P, b, Wd, W=None, them=0.0):
    """đặt xương b sao cho ma trận thế giới = Wd (cha đã đặt xong). Góc riêng chọn cùng vòng với góc đang có + `them` (độ đã quay
    thêm so với dáng nền): xương quay nhiều vòng phải giữ góc LIÊN TỤC, không quy về một vòng (runtime nội suy sẽ quay ngược)."""
    W = W if W is not None else sk.the_gioi(P)
    bb = sk.bones[sk.bi[b]]
    L = np.linalg.solve(W[bb["parent"]], Wd)
    sx = math.hypot(L[0, 0], L[1, 0])
    sy = math.hypot(L[0, 1], L[1, 1])
    rot = math.degrees(math.atan2(L[1, 0], L[0, 0]))
    g = P._g(b)
    cur = bb["rot"] + g[2] + them
    rot = rot - 360.0 * round((rot - cur) / 360.0)
    g[0], g[1], g[2] = L[0, 2] - bb["x"], L[1, 2] - bb["y"], rot - bb["rot"]
    g[3], g[4] = sx / (bb["sx"] or 1.0), sy / (bb["sy"] or 1.0)


def quay_quanh(Wm, c, goc):
    R = mat(c[0], c[1], goc) @ mat(-c[0], -c[1], 0.0)
    return R @ Wm


def lua_lay(P, t, lua, chu_ky=0.8, bien=1.0, nga=0.0, co=1.0):
    """lửa lay: mỗi lưỡi sóng lệch pha (đốt trên trễ, mạnh hơn), phập phồng dài ngắn; nga = ngả cả đám lửa (độ, dương = về sau)."""
    for i, (a, b) in enumerate(lua):
        ph = i * 1.7
        w = 2 * math.pi / chu_ky
        P.rot(a, bien * (5.0 * math.sin(w * t + ph)) + nga * 0.6)
        P.rot(b, bien * (9.0 * math.sin(w * t + ph - 1.1)) + nga * 0.4)
        sc = 1.0 + bien * 0.07 * math.sin(w * t * 2 + ph * 0.7)
        P.scale(a, sc, 1.0)
    if co != 1.0:
        P.scale("lua", max(0.2, co))          # co đều ở gốc (co lệch trục làm xương lưỡi lật khi gần 0); lúc nhỏ hơn đã ẩn bằng độ đậm
    P.rot("lua", nga * 0.3)
    for j, g in enumerate(GIOT):
        P.move(g, 0.0, bien * 7.0 * math.sin(2 * math.pi * t / chu_ky + j * 2.1))
        P.rot(g, bien * 8.0 * math.sin(2 * math.pi * t / chu_ky * 0.5 + j))


def chu_ky_lap(dur, muon=0.8):
    return dur / max(1, round(dur / muon))


def lo_xo(lua):
    return [LoXo(n, k=(170, 120), damp=0.5, maxang=16.0) for n in lua]


def hien(P, slot, a):
    P.alpha[slot] = float(min(1.0, max(0.0, a)))


def mat_sang(P, v):
    """v = 1 mắt sáng, 0 tắt (đổi hình bằng độ đậm hai slot)."""
    hien(P, "mat", v)
    hien(P, "mat_tat", 1 - v)


def cau_sang(P, v):
    hien(P, "cau", v)
    hien(P, "cau_tat", 1 - v)


def _goc_manh(sk_, b, Wm):
    pts = []
    for sl in sk_.slots:
        if sl["bone"] != b:
            continue
        for spec in sk_.atts[sl["name"]].values():
            if spec["type"] != "region":
                continue
            w, h = spec["width"], spec["height"]
            M = Wm @ mat(spec["x"], spec["y"], spec["rotation"], spec["scaleX"], spec["scaleY"])
            pts += [(M @ np.array([cx_, cy_, 1.0]))[:2] for cx_, cy_ in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]
    return np.array(pts) if pts else np.array([Wm[:2, 2]])


def tam_manh(sk_, b, Wm):
    """tâm khung bao (thế giới) của các mảnh cứng trên xương b khi xương có ma trận Wm."""
    Q = _goc_manh(sk_, b, Wm)
    return (Q.min(0) + Q.max(0)) / 2


def day_thap_ngoai(sk_, b, Wm):
    """y thấp nhất của các mảnh cứng trên xương b khi xương có ma trận Wm."""
    return float(_goc_manh(sk_, b, Wm)[:, 1].min())


# ---------------------------------------------------------------- clip
def lam_clip(sk, info):
    lua = info["lua"]
    W_idle = sk.the_gioi(info["P0"])
    out = []

    # idle: nguyên idle_01 của họ + lửa lay
    d_i = CD["idle_01"][0]
    ck_i = chu_ky_lap(d_i, 0.8)

    def idle(t, P):
        dat(P, mau("idle_01", t, True))
        lua_lay(P, t, lua, ck_i)
    out.append(Clip("idle", d_i, idle, loop=True, mem=lo_xo(lua)))

    # walk: run_01 + lửa ngả về sau
    d_w = CD["run_01"][0]

    def walk(t, P):
        dat(P, mau("run_01", t, True))
        lua_lay(P, t, lua, chu_ky_lap(d_w, 0.3), 1.2, nga=10.0)
    out.append(Clip("walk", d_w, walk, loop=True, mem=lo_xo(lua)))

    # hit: hit_01; lúc họ đổi mắt chữ X thì mắt mình nheo (ép dọc)
    d_h = CD["hit_01"][0]

    def hit(t, P):
        dat(P, mau("hit_01", t))
        if mat_x("hit_01", t):
            P.scale("bone18", 1.0, 0.35)
        lua_lay(P, t, lua, 0.5, 1.4, nga=14.0 * math.sin(math.pi * min(1, t / d_h)))
    out.append(Clip("hit", d_h, hit, mem=lo_xo(lua)))

    # attack: lấy đà (kéo nắm tay gần ra sau như skill_01_1 0,2–0,47), BAY tới, ĐẤM một phát (cú vung 0,47→0,53 của họ trải 3 khung),
    # khựng, bay lùi về. Xương move: lao (game kéo tới đối thủ).
    A_DUR, A_TRUNG = 1.30, 0.62
    # quãng dời trong clip nhỏ (game tự nắn quãng lao tới đối thủ, AolaSticker.Lunge): dời lớn quá khung sticker (rộng 3,4 lần chiều cao)
    # thì thân phía trước bị cắt dọc (đã gặp ở chiêu cuối khi còn dời 360)
    A_XA = 0.6 * info["cao"]

    def att_t(t):          # giờ của mình → giờ clip họ
        return cong([(0, 0.0), (0.36, 0.47), (0.56, 0.47), (A_TRUNG, 0.535), (0.86, 0.80), (1.30, 1.133)], t,
                    [em, None, ra_, None, em])

    def attack(t, P):
        dat(P, mau("skill_01_1", att_t(t)))
        x = cong([(0, 0.0), (0.36, -40.0), (0.56, A_XA * 0.9), (A_TRUNG, A_XA), (0.90, A_XA - 10), (1.18, 0.0), (A_DUR, 0.0)], t,
                 [em, vao, ra_, None, em, None])
        y = 46.0 * math.sin(math.pi * min(1, max(0, (t - 0.36) / 0.2))) if 0.36 < t < 0.56 else 0.0
        y += 30.0 * math.sin(math.pi * min(1, max(0, (t - 0.9) / 0.28))) if 0.9 < t < 1.18 else 0.0
        P.move("move", x, y)
        r = rung(t, A_TRUNG, 5.0 * MANH_DANG, 0.12 * MANH_DANG, 14.0)
        P.move("bone", r, 0.0)
        lua_lay(P, t, lua, 0.45, 1.3, nga=cong([(0, 0.0), (0.4, -6.0), (0.56, 22.0), (0.9, 10.0), (1.3, 0.0)], t))
    out.append(Clip("attack", A_DUR, attack, ev=[(A_TRUNG, "trung", "")], trung=A_TRUNG, mem=lo_xo(lua)))

    # cast: skill_02 (thu mình, cuộn bay lên, BUNG dang tay) + GIỮ dáng bung cho tia lửa từ con ngươi; mắt phồng lúc bắn
    C_PHUN = 0.82
    C_HET = C_PHUN + 0.96
    C_DUR = 2.10

    def cast_t(t):
        # cú bung của họ bật trong một khung (0,63 → 0,67): giãn ra 0,60 → 0,74 cho mượt
        return cong([(0, 0.0), (0.60, 0.60), (0.74, 0.67), (0.80, 0.74), (C_HET, 1.30), (C_DUR, 1.633)], t, [None, em, None, None, em])

    def cast(t, P):
        tt = cast_t(t)
        dat(P, mau("skill_02", tt))
        ph = em((t - 0.70) / 0.12) * (1 - em((t - C_HET) / 0.15))
        P.scale("bone18", 1 + (0.14 if K == 1 else 0.20) * ph)
        P.move("bone", rung(t, C_PHUN, 3.0, 0.5, 18.0) * ph, 0.0)
        lua_lay(P, t, lua, 0.5, 1.0 + 0.6 * ph, nga=-6.0 * ph, co=1 + 0.12 * ph)
    out.append(Clip("cast", C_DUR, cast, ev=[(0.70, "tu", ""), (C_PHUN, "phun", ""), (C_HET, "het_phun", "")], trung=C_PHUN,
                    mem=lo_xo(lua)))

    # skill: dang hai tay (dáng bung của skill_02) → hai cánh tay QUAY CHONG CHÓNG quanh tâm quả cầu (nhanh dần) → lao tới đập liên
    # tục → chậm lại, lùi về. Tấm vai giữ nguyên chỗ (quay ngược bù), nắm tay quay theo tay.
    # dạng 2 mạnh hơn: quay 8 vòng, đứng đập lâu hơn, 7 nhát (dạng 1: 6 vòng, 5 nhát)
    KEO = 0.0 if K == 1 else 0.40                 # giây kéo dài thêm ở đoạn đập
    S_DUR = 2.90 + KEO
    S_LAO0, S_LAO1, S_VE0, S_VE1 = 1.05, 1.25, 2.15 + KEO, 2.45 + KEO
    S_XA = 0.5 * info["cao"]
    VONG = 6 if K == 1 else 8                     # số vòng quay cả chiêu (nguyên, để tay về đúng chỗ)
    s0, s1 = 0.30, 2.40 + KEO                     # quãng quay
    SO_NHAT = 5 if K == 1 else 7
    R_QUAY = info["r_quay"]                          # bán kính quỹ đạo nắm tay quanh tâm quả cầu (sát mép cầu)

    def goc_quay(t):
        if t <= s0:
            return 0.0
        if t >= s1:
            return -360.0 * VONG
        u = (t - s0) / (s1 - s0)
        # nhanh dần 25% đầu, đều, chậm dần 15% cuối: tích phân của hình thang vận tốc
        a, b = 0.25, 0.15
        vmax = 1.0 / (1 - a / 2 - b / 2)
        if u < a:
            x = vmax * u * u / (2 * a)
        elif u < 1 - b:
            x = vmax * (a / 2 + (u - a))
        else:
            r = 1 - u
            x = 1 - vmax * r * r / (2 * b)
        return -360.0 * VONG * x

    def skill(t, P):
        mo = em(t / 0.30) * (1 - em((t - s1) / 0.40))
        dat(P, pha(mau("idle_01", 0.0), mau("skill_02", 1.0), mo))
        W = sk.the_gioi(P)
        c = W["bone"] @ np.array([*info["c_cau"], 1.0])
        g = goc_quay(t)
        if abs(g) > 1e-6:
            thu = em((t - s0) / 0.35) * (1 - em((t - (s1 - 0.25)) / 0.25))      # kéo nắm tay sát quả cầu lúc quay
            for tay, vai, nam in (("bone20", "bone10", "bone14"), ("bone21", "bone11", "bone17")):
                Wv = W[vai].copy()
                Wq = quay_quanh(W[tay], c[:2], g)
                Fp = (Wq @ np.linalg.inv(W[tay]) @ W[nam] @ np.array([*info["tam_nam"][nam], 1.0]))[:2]
                d = float(np.hypot(*(Fp - c[:2])))
                if d > 1e-6:
                    Wq[:2, 2] += (c[:2] - Fp) / d * max(0.0, d - R_QUAY) * thu
                dat_tg(sk, P, tay, Wq, W, them=g)
                W = sk.the_gioi(P)
                dat_tg(sk, P, vai, Wv, W, them=-g)
                W = sk.the_gioi(P)
        x = cong([(0, 0.0), (S_LAO0, -20.0), (S_LAO1, S_XA), (S_VE0, S_XA), (S_VE1, 0.0), (S_DUR, 0.0)], t, [em, ra_, None, em, None])
        nay = 18.0 * math.sin(2 * math.pi * (t - S_LAO1) / 0.2) if S_LAO1 < t < S_VE0 else 0.0
        y = 40.0 * math.sin(math.pi * (t - S_VE0) / (S_VE1 - S_VE0)) if S_VE0 < t < S_VE1 else 0.0
        P.move("move", x + nay * 0.4, y + abs(nay) * 0.5)
        P.rot("bone", 8.0 * em((t - 0.3) / 0.5) * (1 - em((t - (s1 - 0.2)) / 0.3)))
        lua_lay(P, t, lua, 0.4, 1.5, nga=24.0 * em((t - 0.4) / 0.4) * (1 - em((t - (s1 - 0.1)) / 0.4)))
    trung_s = [S_LAO1 + 0.05 + 0.18 * k for k in range(SO_NHAT)]
    out.append(Clip("skill", S_DUR, skill, ev=[(s0, "xoay", "")] + [(x, "trung", "") for x in trung_s], trung=trung_s[0],
                    mem=lo_xo(lua)))

    # appear: bộ giáp nằm bẹp dưới đất (mắt tắt, cầu nguội, không lửa, không tay) → mắt SÁNG lên → cầu PHỒNG lên, giáp bung ra → hai
    # tay TRỒI ra → cả con BAY lên vào dáng nghỉ
    P_DUR = 2.20
    cx_tg = W_idle["bone"][:2, 2].copy()
    pile = {}
    for k_, b in enumerate([XUONG_MANH[t] for t in GIAP] + ["bone14", "bone17"]):
        Wb = W_idle[b]
        x, y = Wb[0, 2], Wb[1, 2]
        nx = cx_tg[0] + (x - cx_tg[0]) * 0.80
        ny = 12.0 + max(0.0, y) * 0.24
        lech = (12.0 if x < cx_tg[0] else -12.0) * (1 + 0.3 * (k_ % 3))
        if b in ("bone5", "bone7", "bone11"):            # tấm đầu và mảnh bên phải ngả về sau: chừa con mắt lộ ra cho thấy mắt sáng lên
            nx -= 75.0
            lech += 26.0
        if b == "bone9":                                 # tấm dưới phải dạt sang phải
            nx += 50.0
            lech -= 14.0
        pile[b] = mat(nx, ny, lech) @ np.array([[Wb[0, 0], Wb[0, 1], 0], [Wb[1, 0], Wb[1, 1], 0], [0, 0, 1.0]])
        if K == 2:
            # dạng 2: mảnh nằm xa gốc xương hơn (hàm thấp, tấm vai to): tính theo TÂM MẢNH và kê cho đáy mảnh không lún dưới đất
            pc = tam_manh(sk, b, Wb)
            px_ = cx_tg[0] + (pc[0] - cx_tg[0]) * 0.80 + (nx - (cx_tg[0] + (x - cx_tg[0]) * 0.80))
            if b in ("bone5", "bone7", "bone11"):
                px_ -= 45.0                                  # tấm đầu dạng 2 to hơn: ngả ra sau xa hơn cho mắt lộ
            if b in ("bone8", "bone9"):
                px_ += 30.0
            py_ = 12.0 + max(0.0, pc[1]) * 0.24
            Wp_ = mat(px_, py_, lech) @ mat(-pc[0], -pc[1], 0.0) @ Wb
            dy_ = day_thap_ngoai(sk, b, Wp_)
            if dy_ < 2.0:
                Wp_ = mat(0.0, 2.0 - dy_, 0.0) @ Wp_
            pile[b] = Wp_

    def nhap(Wa, Wb, w):
        ga, gb = goc_mat(Wa), goc_mat(Wb)
        gb = gb - 360.0 * round((gb - ga) / 360.0)
        sa, sb = math.hypot(Wa[0, 0], Wa[1, 0]), math.hypot(Wb[0, 0], Wb[1, 0])
        return mat(Wa[0, 2] + (Wb[0, 2] - Wa[0, 2]) * w, Wa[1, 2] + (Wb[1, 2] - Wa[1, 2]) * w, ga + (gb - ga) * w, sa + (sb - sa) * w)

    def appear(t, P):
        dat(P, mau("idle_01", 0.0))
        sang = em((t - 0.40) / 0.25)
        bung = vot((t - 0.62) / 0.42, 2.2)                   # cầu phồng, giáp bung về chỗ
        bay = em((t - 1.30) / 0.45)                          # cả con bay lên dáng nghỉ
        tay = vot((t - 0.95) / 0.35, 1.8)                    # tay trồi ra
        # quả cầu: nằm thấp, nhỏ → phồng → bay lên
        r0 = W_idle["bone"][1, 2]
        y_cau = (0.60 if K == 1 else 0.74) * r0 * (1 - bay) + r0 * bay
        sc = 0.55 + (1.08 - 0.55) * min(1.0, bung) - 0.08 * em((t - 1.05) / 0.3) if t < 1.6 else 1.0
        rr = rung(t, 0.45, 4.0, 0.25, 16.0)
        P.move("bone", rr, y_cau - r0)
        P.scale("bone", sc)
        W = sk.the_gioi(P)
        for b in [XUONG_MANH[x] for x in GIAP]:
            w = min(1.0, max(0.0, bung)) * 0.55 + 0.45 * bay
            Wt = W_idle[b].copy()
            Wt[1, 2] += (y_cau - r0) * (1 - bay)
            dat_tg(sk, P, b, nhap(pile[b], Wt, w), W)
        W = sk.the_gioi(P)
        for b in ("bone14", "bone17"):
            Wa = mat(cx_tg[0], y_cau, 0.0) @ np.array([[W_idle[b][0, 0] * 0.4, W_idle[b][0, 1] * 0.4, 0], [W_idle[b][1, 0] * 0.4, W_idle[b][1, 1] * 0.4, 0], [0, 0, 1.0]])
            dat_tg(sk, P, b, nhap(Wa, W_idle[b], max(0.0, tay)) if tay < 1.0 else nhap(W_idle[b], W_idle[b], 0.0), W)
            W = sk.the_gioi(P)
        for s_ in ("nam_gan", "nam_xa"):
            hien(P, s_, em((t - 0.95) / 0.12))
        for s_ in ("tay_gan", "tay_xa"):                  # khúc tay lửa hiện khi nắm tay đã ra gần chỗ (khỏi lơ lửng)
            hien(P, s_, em((t - 1.12) / 0.12))
        mat_sang(P, sang)
        cau_sang(P, em((t - 0.45) / 0.35))
        lua_co = em((t - 0.75) / 0.35)
        lua_lay(P, t, lua, 0.6, 0.4 + 0.8 * lua_co, co=max(0.05, lua_co))
        for s_ in ("lua", "giot1", "giot2"):
            hien(P, s_, lua_co)
        a0 = em(t / 0.15)                                    # khung đầu trống
        for s_ in [s["name"] for s in sk.slots]:
            P.alpha[s_] = P.alpha.get(s_, next(q["alpha"] for q in sk.slots if q["name"] == s_)) * a0
    out.insert(0, Clip("appear", P_DUR, appear, ev=[(0.40, "sang", ""), (0.95, "xong", ""), (1.30, "bay", "")], mem=lo_xo(lua)))

    # die: giật ngửa, RƠI xuống đất, mắt TẮT, lửa lụi, cầu nguội; các tấm giáp RƠI ra từng tấm, nảy nhẹ, nằm yên; tan
    X_DUR, TAN = 1.80, 0.45
    G_ = 2600.0
    rnd = np.random.default_rng(7)
    roi = {}
    for k_, b in enumerate([XUONG_MANH[x] for x in GIAP] + ["bone14", "bone17"]):
        Wb = W_idle[b]
        roi[b] = dict(t0=0.42 + 0.06 * k_ + 0.03 * rnd.random(), vx=(1 if Wb[0, 2] > cx_tg[0] else -1) * (40 + 60 * rnd.random()),
                      vy=60 + 80 * rnd.random(), quay=(1 if Wb[0, 2] > cx_tg[0] else -1) * (-120 - 160 * rnd.random()))

    def day_thap(sk_, b, Wm):
        """y thấp nhất của mảnh trên xương b khi xương có ma trận Wm."""
        ys = []
        for sl in sk_.slots:
            if sl["bone"] != b:
                continue
            for spec in sk_.atts[sl["name"]].values():
                if spec["type"] != "region":
                    continue
                w, h = spec["width"], spec["height"]
                M = Wm @ mat(spec["x"], spec["y"], spec["rotation"], spec["scaleX"], spec["scaleY"])
                for cx_, cy_ in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
                    ys.append((M @ np.array([cx_, cy_, 1.0]))[1])
        return min(ys) if ys else Wm[1, 2]

    def die(t, P):
        dat(P, mau("idle_01", 0.0))
        tat = em((t - 0.12) / 0.30)
        # quả cầu: giật ngửa rồi rơi
        giat = math.sin(math.pi * min(1.0, t / 0.22)) if t < 0.22 else 0.0
        r0 = W_idle["bone"][1, 2]
        tr = max(0.0, t - 0.20)
        y_roi = max(-(r0 - 0.62 * r0 * 1.0), -0.5 * G_ * tr * tr)
        nay = -abs(rung(t, 0.20 + math.sqrt(2 * (0.38 * r0) / G_), 14.0, 0.12, 5.0)) if y_roi <= -(0.38 * r0) + 1 else 0.0
        P.move("bone", -18.0 * giat - 22.0 * em((t - 0.2) / 0.4), 26.0 * giat + max(y_roi, -0.38 * r0) + nay)
        P.rot("bone", 14.0 * giat + 10.0 * em((t - 0.2) / 0.5))
        W = sk.the_gioi(P)
        for b, r in roi.items():
            if t < r["t0"]:
                continue
            Wst = _W_tai(sk, P, b, r, W_idle, t)
            dat_tg(sk, P, b, Wst, W)
            W = sk.the_gioi(P)
        mat_sang(P, 1 - tat)
        cau_sang(P, 1 - em((t - 0.25) / 0.45))
        lua_co = 1 - em((t - 0.12) / 0.40)
        lua_lay(P, t, lua, 0.4, 1.0, nga=10.0, co=max(0.05, lua_co))
        for s_ in ("lua", "giot1", "giot2", "tay_gan", "tay_xa"):
            hien(P, s_, lua_co)
        a = 1.0 - em((t - X_DUR) / (TAN - 0.05))
        if a < 1.0:
            for s_ in [s["name"] for s in sk.slots]:
                P.alpha[s_] = P.alpha.get(s_, next(q["alpha"] for q in sk.slots if q["name"] == s_)) * a

    def _W_tai(sk_, P, b, r, Wid, t):
        """ma trận thế giới của mảnh đang rơi: rời chỗ ở khung bắt đầu rơi (dáng nghỉ, cầu đã tụt), bay chéo, quay, chạm đất, nảy."""
        W0b = Wid[b].copy()
        tau = t - r["t0"]
        x = W0b[0, 2] + r["vx"] * tau
        y = W0b[1, 2] + r["vy"] * tau - 0.5 * G_ * tau * tau
        g = goc_mat(W0b) + r["quay"] * min(tau, 0.45)
        sc0 = math.hypot(W0b[0, 0], W0b[1, 0])
        Wm = mat(x, y, g, sc0, sc0)
        dy = day_thap(sk_, b, Wm)
        if dy < 0.0:
            # chạm đất: nằm trên đất, nảy nhỏ một lần
            t_cham = (r["vy"] + math.sqrt(r["vy"] ** 2 + 2 * G_ * max(1.0, W0b[1, 2]))) / G_
            sau = max(0.0, tau - t_cham)
            nay = 22.0 * abs(math.sin(math.pi * min(1.0, sau / 0.18))) * (1 if sau < 0.18 else 0)
            Wm = mat(x - r["vx"] * sau * 0.85, (Wm[1, 2] - dy) + nay, g, sc0, sc0)
        return Wm
    out.append(Clip("die", X_DUR + TAN, die, ev=[(0.12, "tat", ""), (0.42, "roi", ""), (0.75, "cham_dat", "")], mem=lo_xo(lua)))
    return out


def bo_cuc(sk, info):
    """HÌNH BỐ CỤC của dạng K: da dạng 1 ở khung 0 idle, mảnh phóng theo TI quanh xương của nó, vẽ đúng khung concept dạng 1
    (1536 × 1024, nền trắng) → inbox/mat_lua_<K>/mau/bo_cuc.png (+ _luoi.png kẻ lưới toạ độ)."""
    from PIL import ImageDraw, ImageFont
    s, ox, oy = info["khop"]
    P = info["P0"].copy()
    P.scale("move", BO_CUC_THU)
    W = sk.the_gioi(P)
    for b, k in TI.items():
        # tâm phóng: nắm tay = điểm chạm đất (giữa đáy mảnh), tấm giáp = tâm mảnh, lửa = gốc xương lửa
        pts = []
        for sl in sk.slots:
            if sl["bone"] != b:
                continue
            for spec in sk.atts[sl["name"]].values():
                if spec["type"] == "region":
                    w, h = spec["width"], spec["height"]
                    M = W[b] @ mat(spec["x"], spec["y"], spec["rotation"], spec["scaleX"], spec["scaleY"])
                    pts += [(M @ np.array([cx, cy, 1.0]))[:2] for cx, cy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]
        if not pts:
            c = W[b][:2, 2]
        else:
            Q = np.array(pts)
            c = np.array([(Q[:, 0].min() + Q[:, 0].max()) / 2, Q[:, 1].min() if b in ("bone14", "bone17") else (Q[:, 1].min() + Q[:, 1].max()) / 2])
        Wd = mat(c[0], c[1], 0.0) @ mat(0, 0, 0.0, k, k) @ mat(-c[0], -c[1], 0.0) @ W[b]
        dat_tg(sk, P, b, Wd, W)
        W = sk.the_gioi(P)
    x0, y1 = (0 - ox) / s * KG, (oy - 0) / s * KG
    x1, y0 = (1536 - ox) / s * KG, (oy - 1024) / s * KG
    im = soi.Ve(sk).ve(P, (x0, y0, x1, y1), s / KG, bg=(255, 255, 255), ss=2).convert("RGB").resize((1536, 1024), Image.LANCZOS)
    os.makedirs(G.MAU, exist_ok=True)
    pth = os.path.join(G.MAU, "bo_cuc.png")
    im.save(pth)
    g = im.copy()
    d = ImageDraw.Draw(g)
    F = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 16)
    for x in range(0, 1536, 50):
        d.line([(x, 0), (x, 1024)], fill=(0, 160, 255) if x % 100 == 0 else (170, 210, 255), width=1)
        if x % 100 == 0:
            d.text((x + 2, 2), str(x), fill=(0, 0, 255), font=F)
    for y in range(0, 1024, 50):
        d.line([(0, y), (1536, y)], fill=(0, 160, 255) if y % 100 == 0 else (170, 210, 255), width=1)
        if y % 100 == 0:
            d.text((2, y + 2), str(y), fill=(0, 0, 255), font=F)
    g.save(os.path.join(G.MAU, "_luoi.png"))
    print(pth)


def main(a):
    sk, info = dung()
    if a and a[0] == "bo_cuc":
        bo_cuc(sk, info)
        return
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
    if a and a[0] == "nhe":                    # ML_DANG=2 ML_NHE=1: ghi bản nhẹ (rig + khung 0 idle + chiều cao) cho dạng 1 gộp tiến hóa
        idle = [c for c in clips if c.ten == "idle"][0]
        os.makedirs(RA, exist_ok=True)
        pickle.dump((sk, hoat.nuong(sk, idle)[0], info["cao"]), open(os.path.join(RA, "_nhe.pkl"), "wb"))
        print("bản nhẹ:", os.path.join(RA, "_nhe.pkl"))
        return
    M, noi = sk, {}
    if K == 1:
        # TIẾN HÓA nối liền: gộp bản nhẹ của dạng 2 (dựng ở tiến trình riêng vì cấu hình theo dạng đọc lúc nạp mô-đun)
        subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "nhe"], env=dict(os.environ, ML_DANG="2", ML_NHE="1"), check=True)
        sk2, idle2, cao2 = pickle.load(open(os.path.join(HERE, "inbox", "mat_lua_2", "rig", "_nhe.pkl"), "rb"))
        ti = info["cao"] / cao2
        M = tienhoa.gop(sk, sk2)
        lua = info["lua"]

        def gong(t, P):                        # Nhãn Than: dáng nghỉ, thụp xuống lấy hơi rồi GỒNG: mắt và cầu phồng, rung, lửa bùng
            dat(P, mau("idle_01", 0.0))
            g = hoat.cv(t, [(0, 0), (0.3, -0.5), (0.6, 1, "out"), (1.3, 1.2)])
            r = hoat.rung(t, 0.5, 1.35, moi=1)
            P.move("bone", 2.0 * r, 14.0 * g)
            P.scale("bone", 1 + 0.10 * max(g, 0))
            P.scale("bone18", 1 + 0.18 * max(g, 0))
            P.rot("bone20", 10.0 * max(g, 0))
            P.rot("bone21", -10.0 * max(g, 0))
            lua_lay(P, t, lua, 0.35, 1.6, co=1 + 0.35 * max(g, 0))

        def bung(t, P, fl):                    # Hỏa Nhãn: hiện ở dáng nghỉ của nó, bùng lửa, mắt phồng, hai tay dang ra rồi về
            for b_, v in tienhoa.doi_ten_pose(idle2, "n_").t.items():
                P.t[b_] = list(v)
            P.move("n_bone", 0.0, 12.0 * fl)
            P.scale("n_bone18", 1 + 0.15 * fl)
            P.scale("n_lua", 1 + 0.25 * fl)
            P.rot("n_bone20", 14.0 * fl)
            P.rot("n_bone21", -14.0 * fl)

        ev = tienhoa.clip_tien_hoa(M, sk, sk2, idle2, tiB=ti, fnA=gong, fnB=bung, mem=[])
        clips = clips + [ev]
        _, _, s_ev = tienhoa.lech_cuoi(M, hoat.nuong(M, ev), sk2, idle2, ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
        print("  evolve:", noi["evolve"])
    xuat.xuat_het(M, clips, RA, TEN, f"Mắt lửa bọc giáp dạng {K} (mat_lua_{K})", dang=K, so_dang=2, dung_yen=("cast",), lao=("skill",), far=(),
                  cao=info["cao"], ma_goc=None, tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2, noi_them=noi)


if __name__ == "__main__":
    main(sys.argv[1:])
