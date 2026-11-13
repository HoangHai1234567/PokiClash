# -*- coding: utf-8 -*-
"""Golem lõi lửa (golem_lua, tướng thứ 4 đảo Hỏa): rig trên bộ xương của con gốc monster_3422. Mảnh của mình là MẢNH CỨNG đặt đúng chỗ
concept đã duyệt (L1_duyet = hướng A đá tro); chuyển động nền lấy mẫu từ clip của họ bằng runtime Spine thật (<scan>/sample.json, trường
`l`: biến đổi riêng ĐÃ áp 2 IK chân), clip riêng dựng bằng mã trên chính rig của mình.

- Đủ xương của họ (bỏ `root` của họ: thay bằng root + move của mình); không ràng buộc (đã nướng vào mẫu khung).
- Bảy LƯỠI LỬA là lưới riêng, mỗi lưỡi một chuỗi 3 đốt con của xương mảnh nó mọc ra; gốc lưỡi bám xương mảnh (đứng yên trong lỗ), thân
  và ngọn uốn lượn nhẹ lệch pha + lò xo (người dùng dặn: "phần lửa bốc ra cũng phải có animation uốn lượn nhẹ nhàng").
- Đổi hình: `loi` / `loi_tat` (lõi cháy / nguội), `mat` / `mat_tat` (mắt sáng / tắt) bằng độ đậm.
- Xương `mieng` ở họng (chỗ phun lửa, cast). Sự kiện: tu, phun, het_phun, trung, nhay, cuon, xoay, ráp, sang, tat, roi, cham_dat.

Người dùng (2026-11-13): appear = lõi lửa hiện trước rồi các part bay vòng cung vào ráp thành con; idle, run giống họ; đánh thường như
skill_01 (lao tới vả tay từ trên xuống đầu đối thủ); cast hơi cúi, há to mồm phun lửa, rung người, impact mạnh; chiêu cuối như skill_03
(nhảy lên co người thành quả cầu, gai lửa dài hơn, xoay nhanh tại chỗ; bay vào nảy ra làm bằng code) → hai clip theo cơ chế tông thẳng
sẵn có của trận (AolaSticker.Rams): `skill` (nhảy + cuộn) và `skill_land` (cầu xoay trong lúc code cho bay vào, chạm, bật về; rồi bung ra, đáp);
die lõi tắt, các bộ phận rơi xuống.

    golem_lua_rig.py                         dựng, xuất inbox/golem_lua_1/rig/ (JSON Spine, atlas, .atomik, tờ khung, xem.html)
    golem_lua_rig.py soi <clip> <giây,..> [tỉ lệ]   khung lớn nền xám → rig/soi_<clip>.png
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
import golem_lua as G  # noqa: E402

# GL_NON=1 (GL_DANG là số dạng của golem_lua.py, để nguyên): DẠNG 1 "Nham Con" (golem_lua_non.py manh): cùng xương, cùng clip; mảnh ở inbox/golem_lua_non/manh (tấm đá của dạng 2, lửa /
# vuốt / lõi vẽ mới, bốn lỗ tắt không có lưỡi lửa); khung concept ↔ rig lấy của dạng 2 (bàn tay, mắt dạng 1 đã đổi cỡ).
DANG_NON = os.environ.get("GL_NON") == "1"
BASE = os.path.join(os.path.dirname(G.BASE), "golem_lua_non") if DANG_NON else G.BASE
TEN = "golem_lua_non" if DANG_NON else "golem_lua_1"
RA = os.path.join(BASE, "rig")
MANH = os.environ.get("GL_MANH") or os.path.join(BASE, "manh")
MANH_KHOP = os.path.join(G.BASE, "manh") if DANG_NON else MANH
SCAN = G.scan()
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
A0 = json.load(open(os.path.join(SCAN, "att_idle0.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample.json"), encoding="utf-8"))
NB = [b["name"] for b in I["bones"]]
KG = 0.85                    # đơn vị rig con gốc → đơn vị rig của mình
PXU = 1.0                    # pixel ảnh atlas cho mỗi đơn vị rig con gốc
FPS = 30.0

XUONG = {  # mảnh → xương (theo slot gốc của mảnh, bảng mổ mục 2 ghi chú)
    "chan_xa_dui": "P_tuiiL1", "chan_xa_ban": "P_tuiiL2", "chan_xa_goi": "P_tuiiL2",
    "hong": "bone2", "chan_gan_dui": "P_tuiiR1", "chan_gan_ban": "P_tuiiR2", "chan_gan_goi": "P_tuiiR2",
    "co_tay_xa": "P_shouL1", "tay_xa": "P_shouL2", "vuot_xa1": "P_shouzhiL3", "vuot_xa2": "P_shouzhiL1", "vuot_xa3": "P_shouzhiL2",
    "loi": "P_xiongjia1", "loi_tat": "P_xiongjia1", "vo_nguc": "P_xiongqiang", "nguc_trai": "P_xiongjia2",
    "hong_lua": "P_kouqiang", "ham": "P_kouqiang", "lung": "P_jianci4", "vong_dinh": "P_jianci4", "dinh": "P_toujia2",
    "ma": "P_toujia2", "dau": "P_tou", "mat": "P_tou", "mat_tat": "P_tou", "vong_tran": "P_tou",
    "vai": "P_toujia7", "vong_vai": "P_toujia7", "co_tay_gan": "P_shouR1", "tay_gan": "P_shouR2",
    "vuot_gan1": "P_shouzhiR1", "vuot_gan2": "P_shouzhiR2", "vuot_gan3": "P_shouzhiR3",
}
# lưỡi lửa: xương gốc (mảnh nó mọc ra), điểm gốc trên concept (chỗ lửa chui vào lỗ)
LUA = {"lua_vai": ("P_jianci7", (522, 405)), "lua_dinh": ("P_jianci5", (695, 272)), "lua_tran": ("P_tou", (1045, 492)),
       "lua_dinh_nho": ("P_jianci6", (898, 214)), "lua_sau_dau": ("P_tou", (1047, 330)), "lua_co_tay": ("P_shouR1", (413, 610)),
       "lua_hong": ("bone2", (680, 800))}
HONG = (1000, 545)           # tâm họng trên concept (chỗ phun lửa)
# mảnh gộp nhiều part / vẽ khác hình part gốc: không dùng làm mốc khớp khung concept ↔ rig
KHOP_BO = {"dau", "hong", "hong_lua", "loi", "dinh"}
# cụm bay vào (appear) / rơi ra (die): xương mang mảnh, thứ tự theo cây xương (cha trước)
CUM = ["bone2", "P_tuiiL1", "P_tuiiL2", "P_tuiiR1", "P_tuiiR2", "P_xiongjia1", "P_tou", "P_toujia2", "P_xiongqiang", "P_jianci4",
       "P_shouR1", "P_xiongjia2", "P_shouL1", "P_toujia7"]


# ---------------------------------------------------------------- chuyển động nền của họ (mẫu khung, đã áp IK)
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
        out[clip] = (float(v["dur"]), res)
    return out


CD = _cd()


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


def pha(a, b, w):
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
def goc_ten(t):
    """tên mảnh gốc của mảnh phụ (<tên>_nguoi, <vòng>_sau / _truoc, <tấm>_vanh) để lấy xương."""
    for hau in ("_nguoi", "_sau", "_truoc", "_vanh"):
        if t.endswith(hau) and t[:-len(hau)] in XUONG:
            return t[:-len(hau)]
    return t


def khop_khung(dat_):
    """khung concept (px, y xuống) ↔ thế giới con gốc dáng idle giây 0 (y lên): px = ox + s·X, py = oy − s·Y (bình phương tối thiểu
    trên tâm các mảnh có slot gốc)."""
    by = {a["slot"]: a for a in A0["atts"] if a["cur"]}
    R, b, cap = [], [], []
    for m, d in dat_.items():
        sl = d.get("slot")
        if not sl or sl not in by or m in KHOP_BO:
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


def truc_lua(im, goc_px):
    """trục một lưỡi lửa trên ảnh mảnh (px trong ảnh): gốc (điểm mảnh gần chỗ chui vào lỗ nhất), hai điểm giữa (trung bình các điểm có
    hình chiếu ở 1/3, 2/3 trục gốc → ngọn), ngọn (điểm xa gốc nhất, lùi vào trong 8%)."""
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
    """trọng số mỗi đỉnh lưới lửa (toạ độ px của ảnh) theo vị trí dọc đường gấp khúc J (gốc → ngọn): s < ~0,15 bám xương gốc (lỗ),
    còn lại chia mượt cho 3 đốt."""
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
    dat_k = dat_
    if MANH_KHOP != MANH:
        dat_k = json.load(open(os.path.join(MANH_KHOP, "dat.json"), encoding="utf-8"))
        dat_k.pop("_thu_tu")
    s, ox, oy = khop_khung(dat_k)
    tg = lambda px, py: np.array([(px - ox) / s * KG, (oy - py) / s * KG])      # noqa: E731
    k = PXU / s

    # chuỗi xương lửa: đặt theo toạ độ thế giới DÁNG IDLE, đổi về dáng gốc qua xương gốc (dáng gốc và idle lệch phép biến đổi của cha)
    lua_xuong = {}
    for t, (bg, gp) in LUA.items():
        if t not in dat_:
            continue
        g = Image.open(os.path.join(MANH, t + ".png"))
        gx, gy = dat_[t]["goc"]
        gp = dat_[t].get("goc_lua", gp)           # điểm gốc thực (golem_lua_manh.tach_vanh: sau khi dời lửa vào lòng lỗ)
        Jpx = truc_lua(g, np.array([gp[0] - gx, gp[1] - gy], float))
        Jtg = [tg(gx + p[0], gy + p[1]) for p in Jpx]
        Mi = sk.W0[bg] @ np.linalg.inv(Wi[bg])
        pts = [(Mi @ np.array([*q, 1.0]))[:2] for q in Jtg]
        names = [f"{t}_{j}" for j in range(3)]
        sk.chuoi(t, bg, pts, ten_rieng=names)
        lua_xuong[t] = (bg, names, Jpx)
    Wi = sk.the_gioi(P0)

    for t in thu_tu:
        g = Image.open(os.path.join(MANH, t + ".png"))
        im = anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * k)), max(2, round(g.height * k))), Image.LANCZOS).convert("RGBA"))
        sk.anh(t, im)
        gx, gy = dat_[t]["goc"]
        ex = np.array([g.width / s * KG / im.width, 0.0])
        ey = np.array([0.0, -g.height / s * KG / im.height])
        goc_ = tg(gx, gy)
        an = t in ("mat_tat", "loi_tat") or t.endswith("_nguoi")
        if t in lua_xuong:
            bg, names, Jpx = lua_xuong[t]
            sk.slot(t, bg, t)
            L = luoi_vung(im, buoc_vien=8.0, buoc_trong=10.0, ten=t, in_tk=False)
            V = np.array([goc_ + ex * p[0] + ey * p[1] for p in L.pts])
            Vpx = np.asarray(L.pts, float) * (g.width / im.width)
            gan_luoi(sk, t, t, L, V, trong_so_lua(Vpx, Jpx, bg, names), Wi)
        else:
            b = XUONG[goc_ten(t)]
            sk.slot(t, b, t, an=an)
            gan_cung(sk, t, t, b, goc_, ex, ey, Wi)
    # chỗ phun lửa: tâm họng, con của hàm (hướng ra trước, chúc xuống nhẹ)
    pm = tg(*HONG)
    sk.xuong("mieng", "P_kouqiang", *(np.linalg.solve(Wi["P_kouqiang"], np.array([*pm, 1.0]))[:2]))
    # chiều cao game: đỉnh tấm đá cao nhất (lưng / tấm đỉnh), không tính lửa
    cao = float(tg(0, min(dat_[x]["goc"][1] for x in ("lung", "dinh") if x in dat_) + 10)[1])
    sk.xuong("far", "root", 0.9 * cao + 140.0, 0.45 * cao)
    for e, m in (("trung", "khung đòn trúng"), ("tu", "bắt đầu tụ lửa"), ("phun", "lửa phun ra từ họng"), ("het_phun", "lửa tắt"),
                 ("nhay", "bật lên"), ("cuon", "co thành quả cầu"), ("xoay", "bắt đầu xoay"), ("rap", "mảnh ráp vào"),
                 ("sang", "lõi / mắt sáng lên"), ("tat", "lõi tắt"), ("roi", "mảnh bắt đầu rơi"), ("cham_dat", "chạm đất")):
        sk.su_kien(e, m)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao game {cao:.0f}")
    return sk, dict(cao=cao, lua={t: v[1] for t, v in lua_xuong.items()}, P0=P0, khop=(s, ox, oy))


# ---------------------------------------------------------------- tiện ích dáng
def dat_tg(sk, P, b, Wd, W=None, them=0.0):
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


def hien(P, slot, a):
    P.alpha[slot] = float(min(1.0, max(0.0, a)))


def lua_lay(P, t, lua, chu_ky=1.333, bien=1.0, nga=0.0, dai=1.0, chi=None, w=1.0):
    """lửa uốn lượn nhẹ: mỗi lưỡi sóng chạy từ gốc ra ngọn (đốt sau trễ pha, biên độ tăng dần), phập phồng dài ngắn chậm; nga = ngả cả
    lưỡi (độ, dương = ngược kim); dai = độ dài lưỡi (chiêu cuối dài ra). chi: chỉ các lưỡi này. w: trọng số (góc nhân w, tỉ lệ mũ w):
    gọi hai lần với w và 1 − w để pha hai kiểu lửa ở chỗ nối clip."""
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
        sc = dai * (1.0 + bien * 0.05 * math.sin(om * t * 2 + ph * 0.7))
        if abs(sc - 1) > 1e-6:
            P.scale(names[0], sc ** w, (1.0 + (sc - 1) * 0.35) ** w)


def lo_xo(lua):
    return [LoXo(n, k=(150, 110, 80), damp=0.5, maxang=14.0) for n in lua.values()]


def mat_sang(P, v):
    hien(P, "mat", v)
    hien(P, "mat_tat", 1 - v)


def loi_sang(P, v):
    hien(P, "loi", v)
    hien(P, "loi_tat", 1 - v)


def nguoi(sk, P, v):
    """v = 1: lòng lỗ lửa, gối nguội (than tro); 0: cháy."""
    for sl in sk.slots:
        if sl["name"].endswith("_nguoi"):
            hien(P, sl["name"], v)


def lua_hien(P, info, a):
    for t in info["lua"]:
        hien(P, t, a)


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
    Q = _goc_manh(sk_, b, Wm)
    return (Q.min(0) + Q.max(0)) / 2


def day_thap(sk_, b, Wm):
    return float(_goc_manh(sk_, b, Wm)[:, 1].min())


def to_tien(sk, b):
    """xương cụm gần nhất (chính nó hoặc tổ tiên) trong CUM."""
    while b is not None:
        if b in CUM:
            return b
        b = sk.bones[sk.bi[b]]["parent"]
    return None


def nhap(Wa, Wb, w):
    ga, gb = goc_mat(Wa), goc_mat(Wb)
    gb = gb - 360.0 * round((gb - ga) / 360.0)
    sa, sb = math.hypot(Wa[0, 0], Wa[1, 0]), math.hypot(Wb[0, 0], Wb[1, 0])
    return mat(Wa[0, 2] + (Wb[0, 2] - Wa[0, 2]) * w, Wa[1, 2] + (Wb[1, 2] - Wa[1, 2]) * w, ga + (gb - ga) * w, sa + (sb - sa) * w)


# ---------------------------------------------------------------- clip
def lam_clip(sk, info):
    lua = info["lua"]
    W_idle = sk.the_gioi(info["P0"])
    out = []
    d_i = CD["idle_01"][0]

    # idle: idle_01 của họ lặp 3 vòng (4 s) + lửa uốn lượn chậm; lõi phập phồng mỗi vòng; vòng cuối "hắt lửa": lửa vươn dài, lõi bùng,
    # đầu gật nhẹ (trò riêng của con, khỏi đơn điệu)
    I_DUR = 3 * d_i

    def idle(t, P):
        dat(P, mau("idle_01", t, True))
        ph = (t % d_i) / d_i
        bung = math.sin(math.pi * min(1.0, max(0.0, (t - 2.55) / 0.9)))
        P.scale("P_xiongjia1", 1.0, 1.0)
        P.scale("P_qiu", 1 + 0.04 * math.sin(2 * math.pi * ph) + 0.06 * bung)
        P.rot("P_tou", -5.0 * bung)
        lua_lay(P, t, lua, I_DUR / 3, 1.0, dai=1.0 + 0.22 * bung, nga=-4.0 * bung)
    out.append(Clip("idle", I_DUR, idle, loop=True, mem=lo_xo(lua)))

    d_w = CD["run_01"][0]

    def walk(t, P):
        dat(P, mau("run_01", t, True))
        lua_lay(P, t, lua, d_w, 1.0, nga=12.0)
    out.append(Clip("walk", d_w, walk, loop=True, mem=lo_xo(lua)))

    d_h = CD["hit_01"][0]

    def hit(t, P):
        dat(P, mau("hit_01", t))
        lua_lay(P, t, lua, 0.4, 1.5, nga=16.0 * math.sin(math.pi * min(1, t / d_h)), dai=1 - 0.15 * math.sin(math.pi * min(1, t / d_h)))
    out.append(Clip("hit", d_h, hit, mem=lo_xo(lua)))

    # attack: skill_01 (giơ tay gần qua đầu, vả xuống phía trước) + LAO tới để bàn tay đập trúng đầu đối thủ; khựng, lùi về
    A_DUR, A_TRUNG = 1.30, 0.55
    A_XA = 300.0

    def att_t(t):
        return cong([(0, 0.0), (0.42, 0.27), (A_TRUNG, 0.37), (0.68, 0.47), (1.30, 1.0)], t, [em, vao, None, em])

    def attack(t, P):
        dat(P, mau("skill_01", att_t(t)))
        x = cong([(0, 0.0), (0.30, -30.0), (A_TRUNG, A_XA), (0.80, A_XA - 10), (1.15, 0.0), (A_DUR, 0.0)], t, [em, vao, None, em, None])
        y = 70.0 * math.sin(math.pi * (t - 0.30) / (A_TRUNG - 0.30)) if 0.30 < t < A_TRUNG else 0.0
        y += 30.0 * math.sin(math.pi * (t - 0.80) / 0.35) if 0.80 < t < 1.15 else 0.0
        P.move("move", x, y)
        P.move("bone2", rung(t, A_TRUNG, 7.0, 0.12, 14.0), rung(t, A_TRUNG, -6.0, 0.12, 14.0))
        lua_lay(P, t, lua, 0.5, 1.3, nga=cong([(0, 0.0), (0.4, -8.0), (A_TRUNG, 22.0), (0.9, 8.0), (1.3, 0.0)], t))
    out.append(Clip("attack", A_DUR, attack, ev=[(A_TRUNG, "trung", "")], trung=A_TRUNG, mem=lo_xo(lua)))

    # cast: gồng lấy hơi (skill_04 0–0,40) → HƠI CÚI tới, HÁ TO mồm, phun lửa (giữ ~1 s), rung người → về. Thân không ngửa như họ:
    # bỏ phần ngửa của bone2 / ngực, thay bằng cúi tới; hàm há rộng hơn họ (×1,3)
    C_PHUN, C_HET, C_DUR = 0.50, 1.50, 2.05
    HAM_MO = 0.6

    def cast_t(t):
        return cong([(0, 0.0), (0.42, 0.40), (C_PHUN, 0.45), (C_HET, 0.83), (C_DUR, 1.1667)], t, [em, None, None, em])

    def cast(t, P):
        tt = cast_t(t)
        d = mau("skill_04", tt)
        ph = em((t - 0.40) / 0.12) * (1 - em((t - C_HET) / 0.25))
        idl = mau("idle_01", 0.0)
        for b, cui in (("bone2", -4.0), ("P_xiongjia1", -12.0), ("P_tou", -5.0)):
            v = d.get(b, np.array([0, 0, 0, 1, 1.0])).copy()
            v0 = idl.get(b, np.array([0, 0, 0, 1, 1.0]))
            v[0] = v[0] * (1 - ph) + (v0[0] + cui) * ph
            d[b] = v
        if "P_kouqiang" in d:
            v = d["P_kouqiang"].copy()
            v0 = idl.get("P_kouqiang", np.array([0, 0, 0, 1, 1.0]))
            v[0] = v0[0] + (v[0] - v0[0]) * HAM_MO      # mảnh hàm của mình to hơn hàm gốc: mở ít hơn họ cho hàm còn dính mặt
            d["P_kouqiang"] = v
        dat(P, d)
        P.move("bone2", rung(t, C_PHUN, 4.0, 0.6, 16.0) * ph + 2.0 * math.sin(2 * math.pi * 23 * t) * ph, 0.0)
        P.scale("P_kouqiang", 1 + 0.06 * ph)
        P.scale("P_qiu", 1 + 0.12 * ph)
        lua_lay(P, t, lua, 0.45, 1.0 + 0.6 * ph, nga=-10.0 * ph, dai=1 + 0.25 * ph)
    out.append(Clip("cast", C_DUR, cast, ev=[(0.20, "tu", ""), (C_PHUN, "phun", ""), (C_HET, "het_phun", "")], trung=C_PHUN,
                    mem=lo_xo(lua)))

    # chiêu cuối, HAI clip theo cơ chế "tông thẳng" sẵn có của trận (AolaSticker.Jumps / Rams, như Cầu Gai): code lái phần bay vào / bật ra
    #   skill      : thụp lấy đà → BẬT lên (skill_03 0,03–0,13) → co người thành QUẢ CẦU rơi về đất (skill_03 0,13–0,30); lửa dài ra 1,4 lần.
    #                Khung trúng (game: JumpOff = lúc rời đất) đặt ở cuối clip: cầu bắt đầu lăn tới khi skill_land bắt đầu
    #   skill_land : sự kiện "tong" (→ Rams). Cầu XOAY đúng 6 vòng (~2000°/s như họ) trong lúc code cho bay gần ngang, nhanh dần tới THÂN
    #                đối thủ (chạm ở L_HIT: bẹp nhẹ, lửa bùng), đứng 0,16 s rồi bị bật ngược về chỗ cũ theo vòng cung (0,42 s); về tới
    #                chỗ thì bung người, đáp đất, về idle (skill_03 0,63–1,33)
    G_DAI = 1.4
    B0 = mau("skill_03", 0.30)["bone3"][0]           # góc bone3 cuối clip skill (lệch so với dáng gốc)
    S_DUR = 1.0                                       # độ dài clip là bội 1/30 s: khung cuối nướng đúng dáng cuối

    def sk_t(t):
        return cong([(0, 0.0), (0.18, 0.0), (0.30, 0.03), (0.64, 0.13), (S_DUR, 0.30)], t, [None, em, ra_, vao])

    X_DUR = 11 / 30.0
    BALL = mau("skill_03", 0.30)                     # đúng dáng khung cuối clip skill (nối liền)

    def lua_cau(P, tau, w=1.0):
        """lửa dáng cầu: dài G_DAI, ngả về sau chiều quay, lay nhanh (chu kỳ X_DUR/2)."""
        lua_lay(P, tau, lua, X_DUR / 2, 1.5, nga=-22.0, dai=G_DAI, w=w)

    def skill(t, P):
        tt = sk_t(t)
        dat(P, mau("skill_03", tt))
        thup = math.sin(math.pi * min(1.0, t / 0.30)) if t < 0.30 else 0.0
        P.move("bone2", 0.0, -26.0 * thup)
        P.scale("bone2", 1 + 0.06 * thup, 1 - 0.06 * thup)
        cuon = em((t - 0.40) / 0.45)
        lua_lay(P, t, lua, 0.5, 1.2, w=1 - cuon)
        lua_cau(P, t - S_DUR, w=cuon)
    out.append(Clip("skill", S_DUR, skill, ev=[(0.30, "nhay", ""), (0.64, "cuon", "")], trung=S_DUR - 1 / 30.0))

    L_HIT = 0.50                                      # giây chạm thân đối thủ (code bay từ đầu clip tới đây)
    SP = 32 / 30.0                                    # quãng xoay: bay vào + đứng 0,16 + bật về 0,42 ≈ 1,07 s, đúng 6 vòng
    V_DUR = 29 / 30.0                                 # bung ra, đáp, về idle

    def ve_dang(tv, P, t):
        tt = cong([(0, 0.63), (V_DUR, 1.3333)], tv, [None])
        d = mau("skill_03", tt)
        if "bone3" in d:                      # nối từ góc cuối vòng xoay (≡ B0); quay thêm theo chiều xoay cho khung cuối đứng thẳng
            d["bone3"] = d["bone3"].copy()
            goc0 = mau("skill_03", 0.63)["bone3"][0]
            b_end = B0 - 2160.0               # góc cuối đoạn xoay (6 vòng): giữ góc LIÊN TỤC, không quy về B0
            cuoi = b_end + (mau("skill_03", 1.3333)["bone3"][0] - goc0)
            bu = 360.0 * math.floor(cuoi / 360.0) - cuoi
            d["bone3"][0] = b_end + (d["bone3"][0] - goc0) + bu * em(tv / 0.55)
        hb = em(tv / 0.2)                     # các xương khác: từ dáng cầu hoà sang dáng của họ trong 0,2 s đầu
        for b, v in BALL.items():
            if b == "bone3":
                d[b][1:] = v[1:] * (1 - hb) + d[b][1:] * hb
                continue
            d[b] = v * (1 - hb) + d.get(b, np.array([0, 0, 0, 1, 1.0])) * hb
        dat(P, d)
        wv = em((tv - 0.15) / 0.5)
        lua_cau(P, t, w=1 - wv)               # giờ chung t: lửa liền pha với đoạn xoay
        lua_lay(P, t, lua, 0.6, 1.0, w=wv)

    # Lúc bung người (skill_03 0,63–1,0) tay, lưng, lửa văng ra SAU tới 295 đơn vị (0,54 lần chiều cao) so với dáng đứng: trong trận con đứng
    # sát mép màn nên gần nửa thân ra ngoài màn hình (soi tour 2026-11-13). Sửa: dời `move` TỚI TRƯỚC V_LUI: cầu bị bật về chỉ tới cách
    # chỗ cũ V_LUI (cùng nhịp cú bật của code: AolaSticker.JumpStay 0,16 + JumpBack 0,42, smoothstep → quãng về một chiều, không giật
    # ngược), bung người ở đó, rơi và trượt lùi nốt về chỗ cũ.
    V_LUI = 300.0

    def lui(t):
        return V_LUI * em((t - L_HIT - 0.16) / 0.42) * (1 - em((t - 1.30) / 0.65))

    def skill_land(t, P):
        P.move("move", lui(t), 0.0)
        if t < SP:
            d = {k: v.copy() for k, v in BALL.items()}
            u = t / SP
            d["bone3"][0] = B0 - 2160.0 * u
            d["bone3"][2] = BALL["bone3"][2] + 8.0 * abs(math.sin(2 * math.pi * 6 * u))
            dat(P, d)
            bep = math.sin(math.pi * min(1.0, max(0.0, (t - L_HIT) / 0.16))) if L_HIT <= t < L_HIT + 0.16 else 0.0
            P.scale("bone3", 1 + 0.10 * bep, 1 - 0.10 * bep)
            lua_lay(P, t, lua, X_DUR / 2, 1.5 + 0.6 * bep, nga=-22.0, dai=G_DAI * (1 + 0.15 * bep))
        else:
            ve_dang(t - SP, P, t)
    out.append(Clip("skill_land", SP + V_DUR, skill_land, ev=[(0.0, "tong", ""), (0.0, "xoay", ""), (L_HIT, "trung", ""),
                                                            (SP + 0.62, "cham_dat", "")], trung=L_HIT))

    # appear: LÕI lửa hiện giữa không trung (nhỏ → bùng → về cỡ), rồi từng cụm mảnh BAY VÒNG CUNG từ ngoài vào đúng chỗ (hông, chân, ngực,
    # tay, lưng, vai, tấm đỉnh, đầu), khựng nhẹ khi ráp; ráp xong mắt sáng, lửa bùng ở các lỗ
    P_DUR = 2.30
    c_loi = W_idle["P_xiongjia1"][:2, 2].copy()
    lich = {"bone2": 0.42, "P_tuiiL1": 0.50, "P_tuiiR1": 0.55, "P_tuiiL2": 0.50, "P_tuiiR2": 0.55, "P_xiongqiang": 0.62,
            "P_xiongjia2": 0.68, "P_shouL1": 0.76, "P_shouR1": 0.82, "P_jianci4": 0.90, "P_toujia7": 0.98, "P_toujia2": 1.05,
            "P_tou": 1.14}
    BAY = 0.40
    rnd = np.random.default_rng(3)
    duong = {}
    for k_, b in enumerate(CUM):
        if b not in lich:
            continue
        Wt = W_idle[b]
        pc = tam_manh(sk, b, Wt)
        v = pc - c_loi
        n_ = np.hypot(*v)
        v = v / n_ if n_ > 1e-6 else np.array([0.0, 1.0])
        goc_ra = math.atan2(v[1], v[0]) + rnd.uniform(-0.5, 0.5)
        D = 620.0 + rnd.uniform(0, 160)
        st = pc + np.array([math.cos(goc_ra), math.sin(goc_ra) * 0.7 + 0.45]) * D
        perp = np.array([-(pc - st)[1], (pc - st)[0]])
        perp /= np.hypot(*perp) + 1e-9
        ctrl = (st + pc) / 2 + perp * (220.0 * (1 if k_ % 2 else -1)) + np.array([0.0, 160.0])
        duong[b] = dict(st=st, ctrl=ctrl, pc=pc, quay=(1 if k_ % 2 else -1) * rnd.uniform(200, 320))

    def appear(t, P):
        dat(P, mau("idle_01", 0.0))
        W = sk.the_gioi(P)
        for b in CUM:
            if b == "P_xiongjia1":
                sc = cong([(0, 0.05), (0.22, 1.25), (0.38, 0.92), (0.5, 1.0)], t, [ra_, em, em])
                Wt = W_idle[b]
                dat_tg(sk, P, b, mat(Wt[0, 2], Wt[1, 2], goc_mat(Wt), sc * math.hypot(Wt[0, 0], Wt[1, 0])), W)
                W = sk.the_gioi(P)
                continue
            r = duong.get(b)
            if r is None:
                continue
            t0 = lich[b]
            u = min(1.0, max(0.0, (t - t0) / BAY))
            e = ra_(u, 2.2)
            q = (1 - e) ** 2 * r["st"] + 2 * (1 - e) * e * r["ctrl"] + e * e * r["pc"]
            g = r["quay"] * (1 - e)
            Wt = W_idle[b]
            Wd = mat(q[0], q[1], g) @ mat(-r["pc"][0], -r["pc"][1], 0.0) @ Wt
            if u >= 1.0:   # khựng khi ráp: nảy nhỏ vào trong
                k = rung(t, t0 + BAY, 8.0, 0.08, 12.0)
                Wd = mat(0.0, -abs(k), 0.0) @ Wt
            dat_tg(sk, P, b, Wd, W)
            W = sk.the_gioi(P)
        # rung cả con khi mảnh cuối ráp xong
        P.move("move", rung(t, 1.56, 5.0, 0.15, 14.0), 0.0)
        for sl in sk.slots:
            nm = sl["name"]
            c = to_tien(sk, sl["bone"])
            if nm in lua:
                a = em((t - 1.58) / 0.18)
            elif nm in ("loi", "loi_tat"):
                a = em(t / 0.10) * (1.0 if nm == "loi" else 0.0)
            elif c in lich:
                a = em((t - lich[c]) / 0.08)
            else:
                a = em((t - 0.9) / 0.2)
            P.alpha[nm] = a * sl["alpha"] if nm not in ("mat", "mat_tat", "loi", "loi_tat") and not nm.endswith("_nguoi") else a
        for sl in sk.slots:
            if sl["name"].endswith("_nguoi"):
                P.alpha[sl["name"]] = P.alpha.get(sl["name"], 0.0) * (1 - em((t - 1.52) / 0.12))
        sang = em((t - 1.50) / 0.15)
        P.alpha["mat"] = P.alpha.get("mat", 1.0) * sang
        P.alpha["mat_tat"] = P.alpha.get("mat_tat", 1.0) * (1 - sang)
        bung = cong([(1.58, 0.0), (1.75, 1.35), (2.0, 1.0)], t, [ra_, em]) if t >= 1.58 else 0.0
        lua_lay(P, t, lua, 0.5, 1.2, dai=max(0.05, bung))
    out.insert(0, Clip("appear", P_DUR, appear, ev=[(0.0, "sang", ""), (0.42, "rap", ""), (1.56, "rap", ""), (1.58, "phun", "")],
                       mem=lo_xo(lua)))

    # die: lõi chập chờn rồi TẮT, mắt tắt, lửa lụi; thân sụm, từng cụm RƠI xuống đất, nảy nhẹ, nằm yên; tan
    D_DUR, TAN = 1.85, 0.45
    G_ = 2600.0
    rnd2 = np.random.default_rng(11)
    roi = {}
    cx_tg = c_loi[0]
    for k_, b in enumerate(CUM):
        Wb = W_idle[b]
        pc = tam_manh(sk, b, Wb)
        roi[b] = dict(t0=0.40 + 0.035 * k_ + 0.03 * rnd2.random(), vx=(1 if pc[0] > cx_tg else -1) * (40 + 70 * rnd2.random()),
                      vy=40 + 90 * rnd2.random(), quay=(1 if pc[0] > cx_tg else -1) * (-90 - 160 * rnd2.random()), pc=pc)

    def _W_tai(b, r, t):
        Wb = W_idle[b]
        tau = t - r["t0"]
        pc = r["pc"]
        x = pc[0] + r["vx"] * tau
        y = pc[1] + r["vy"] * tau - 0.5 * G_ * tau * tau
        g = r["quay"] * min(tau, 0.5)
        Wm = mat(x, y, g) @ mat(-pc[0], -pc[1], 0.0) @ Wb
        dy = day_thap(sk, b, Wm)
        if dy < 0.0:
            t_cham = (r["vy"] + math.sqrt(r["vy"] ** 2 + 2 * G_ * max(1.0, pc[1] - day_thap(sk, b, Wb) + 1.0))) / G_
            sau = max(0.0, tau - t_cham)
            nay = 18.0 * abs(math.sin(math.pi * min(1.0, sau / 0.16))) * (1 if sau < 0.16 else 0)
            Wm = mat(-r["vx"] * sau * 0.85, -dy + nay, 0.0) @ Wm
        return Wm

    def die(t, P):
        dat(P, mau("idle_01", 0.0))
        giat = math.sin(math.pi * min(1.0, t / 0.25)) if t < 0.25 else 0.0
        P.move("bone2", -14.0 * giat, -10.0 * giat)
        W = sk.the_gioi(P)
        for b in CUM:
            r = roi[b]
            if t < r["t0"]:
                continue
            dat_tg(sk, P, b, _W_tai(b, r, t), W)
            W = sk.the_gioi(P)
        chap = 1.0 if t < 0.10 else (0.35 if int(t * 22) % 2 else 1.0) if t < 0.38 else 0.0
        loi_sang(P, chap * (1 - em((t - 0.30) / 0.12)))
        mat_sang(P, 1 - em((t - 0.32) / 0.10))
        nguoi(sk, P, em((t - 0.25) / 0.25))
        co = 1 - em((t - 0.12) / 0.35)
        lua_lay(P, t, lua, 0.35, 1.2, nga=12.0, dai=max(0.05, co))
        lua_hien(P, info, co)
        a = 1.0 - em((t - D_DUR) / (TAN - 0.05))
        if a < 1.0:
            for sl in sk.slots:
                P.alpha[sl["name"]] = P.alpha.get(sl["name"], sl["alpha"]) * a
    out.append(Clip("die", D_DUR + TAN, die, ev=[(0.30, "tat", ""), (0.40, "roi", ""), (0.75, "cham_dat", "")], mem=lo_xo(lua)))
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
    xuat.xuat_het(sk, clips, RA, TEN, "Nham Con: golem lõi lửa dạng non (golem_lua_non)" if DANG_NON else "Golem lõi lửa dạng 1 (golem_lua_1)", dang=1, so_dang=1, dung_yen=("cast",),
                  lao=("attack",), far=(), cao=info["cao"], ma_goc=None, tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001},
                  khop_idle=0.2, khong_khop=("skill",))


if __name__ == "__main__":
    main(sys.argv[1:])
