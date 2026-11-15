# -*- coding: utf-8 -*-
"""Hổ lửa đảo Hỏa (hoa_ho; tướng thứ 9 đảo Hỏa, suất hoa_tinh): hình của mình chạy trên ĐÚNG rig của con gốc monster_3645.
Ghi chú: inbox/hoa_ho_ghichu.md. Cách làm như giac_moc_rig.py (skill pokiclash-spine-rig mục 00):
- XƯƠNG: đủ mọi xương của họ, đúng cha – con, đúng biến đổi riêng ở dáng gốc; thêm `move` (cha của mọi thứ), `mieng` (miệng: chỗ
  phát sóng gầm của chiêu mana), `vuot` (bàn chân trước XA, cái chân duỗi về phía đối thủ: chỗ vả của đòn thường).
- MẢNH: mỗi part của họ một ảnh lắp vào NGUYÊN lưới của họ (đỉnh, tam giác, uv, trọng số). BỎ: sừng `P_jiao`, khuyên `P_tiehuan`,
  chuông `P_lingdang` (người dùng dặn bỏ sừng, bỏ chuông). HH_GOC=1: dùng ảnh part GỐC (chỉ để dựng và soi clip trong máy, không
  đưa vào game); không đặt: ảnh của mình ở inbox/hoa_ho_1/manh/part/<vùng>.png.
- CHUYỂN ĐỘNG: mẫu khung của họ (scan/sample.json, trường `l` = biến đổi riêng đã áp IK, 30 khung/giây) → lệch so với dáng gốc; clip
  của mình = co giãn giờ một clip nguồn + kênh riêng (dời `move`, lật, độ đậm):
    idle = idle_01, walk = run_01, hit = hit_01, die = die_01 (như họ);
    attack = skill_01_1 (vả): giơ chân trước, GHÌM một nhịp, vả xuống, khựng, về;
    cast   = skill_03 (gồng, ngửa đầu hét): gồng thấp, ngửa đầu GẦM và giữ rung, về;
    skill  = skill_04: thu người, bật tới và biến mất; 12 lượt lướt qua đối thủ (dáng vồ duỗi dài, đổi chiều mỗi lượt); hiện lại ở chỗ cũ
             bằng đoạn đáp của họ; vụ nổ ở đối thủ lúc đáp xong;
    appear = đoạn đáp của skill_04: nhảy từ sau vào sàn.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/hoa_ho_rig.py        → inbox/hoa_ho_1/rig/ (HH_GOC=1: rig_goc/)
    py -3 -I ArtGen/Spine/hoa_ho_rig.py soi <clip> <giây,giây,...|n=12|t0:t1:n> [tỉ lệ]   → soi_<clip>.png (khung lớn nền xám)
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, luoi, trongso, khung, hoat, xuat, soi  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import hoa_ho as G  # noqa: E402

GOC = os.environ.get("HH_GOC") == "1"
# HH_DANG=non: DẠNG 1 (hổ con, "Viêm Hổ Nhi"): cùng xương, cùng lưới, cùng clip, cùng da với dạng 2; khác: đầu to (xương đầu bone5 phóng
# K_DAU), mắt tròn to (MAT_NON), không dải mày đè mắt, không nanh dài, không vòng vàng cổ chân, ít cụm mây lửa (BO_NON), lửa non màu cam lõi vàng (doi_lua).
# HH_DANG=chibi: dạng 1 VẼ RIÊNG (hoa_ho_chibi.py; người dùng chê bản `non` ghép từ da dạng 2): xương và clip như `non`, tỉ lệ đầu 2, chân 0,68,
# đuôi 0,6; mảnh là hình cắt từ concept chibi, lắp bằng hoa_ho_chibi.lap.
CHIBI = os.environ.get("HH_DANG") == "chibi" and not GOC
NON = (os.environ.get("HH_DANG") == "non" or CHIBI) and not GOC
TEN_RIG = "hoa_ho_non" if NON else "hoa_ho_1"
K_DAU = float(os.environ.get("HH_KDAU", "2.0" if CHIBI else "1.4"))
# tỉ lệ chibi (thử 2026-11-14 tối, người dùng: "hổ con xấu quá, gen lại chibi hơn"): HH_CHAN = tỉ lệ chân SAU (vd 0,7; chân trước tính theo
# để bốn bàn chân cùng chạm đất, cả con hạ xuống bằng xương `all`), HH_DUOI = tỉ lệ đuôi (xương gốc đuôi bone8). Không đặt: như cũ.
K_CHAN = float(os.environ.get("HH_CHAN", "0.68" if CHIBI else "1"))
K_DUOI = float(os.environ.get("HH_DUOI", "0.6" if CHIBI else "1"))
CHAN_GOC = {"bone33": 388.0, "bone18": 385.0, "bone43": 459.0, "bone26": 527.0}   # xương đùi: độ cao khớp háng / vai trên mặt đất (dáng gốc)
MAT_NON = [float(x) for x in os.environ.get("HH_MAT", "298,765,45").split(",")]   # mắt tròn dạng 1: tâm x, y và bán kính (đơn vị rig, dáng gốc)
MANH_NON = os.path.join(HERE, "inbox", "hoa_ho_non", "manh", "part")
BO_NON = tuple(f"jiaphuan_0{i}" for i in range(1, 7)) + ("liaoya_01", "liaoya_02", "P_meimao_01") + tuple(
    x for x in os.environ.get("HH_BO", "").split(",") if x)
D_PX = float(os.environ.get("HH_DPX", "0.5" if GOC else "0.6"))        # pixel ảnh atlas cho mỗi đơn vị rig (con cao ~1000 đơn vị)
BO_SLOT = ("shadow", "wangge", "P_jiao", "P_tiehuan", "P_lingdang") + (() if GOC else ("P_L_huxu", "P_R_huxu")) + (BO_NON if NON else ())
THIEU = os.environ.get("HH_THIEU") == "1"           # part chưa có ảnh thì dùng hình tô phẳng của tờ hướng dẫn (giữ chỗ)
MAT = ("P_yanjing", "P_biyan")
MANH = os.path.join(G.BASE, "manh", "part")
TAN = 0.45
FPS = 30.0
N_LUOT = 6 if NON else 12                            # số lượt lướt qua đối thủ của chiêu cuối (dạng 1: 6 lượt)
LUOT = 0.1                                           # giây mỗi lượt = 3 khung mẫu: ẩn (đầu quãng) → HIỆN (giữa quãng) → ẩn (cuối quãng)
IMPACT = {"attack": (0.09, 0.5, 0.12), "cast": (0.14, 0.9, 0.2, "#ffd9a055"), "skill": (0.22, 1.0, 0.2, "#fff3c066")}
if NON:                                              # dạng 1: con nhỏ, cú trúng nhẹ hơn dạng 2
    IMPACT = {"attack": (0.07, 0.4, 0.1), "cast": (0.11, 0.7, 0.16, "#ffe2b044"), "skill": (0.18, 0.85, 0.18, "#fff3c055")}
SPAN = 6.0


# ---------------------------------------------------------------- nạp
def nap_goc():
    scan = G.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    D0 = json.load(open(os.path.join(scan, "att_idle0.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    return D, D0, I, scan


def ti_le_atlas(D):
    """px ảnh vùng của họ cho mỗi đơn vị rig (đo trên lưới thân)."""
    _, imgs, _ = G.nap("att_goc.json")
    a = next(x for x in D["atts"] if x["slot"] == "P_shenti_01")
    im = imgs[a["region"]]
    U = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
    V = np.array(a["xy"], float).reshape(-1, 2)
    T = np.array(a["tris"]).reshape(-1, 3)

    def dt(P):
        e1, e2 = P[T[:, 1]] - P[T[:, 0]], P[T[:, 2]] - P[T[:, 0]]
        return np.abs(e1[:, 0] * e2[:, 1] - e1[:, 1] * e2[:, 0]).sum() / 2

    return float(math.sqrt(dt(U) / dt(V)))


def doi_lua(g):
    """lửa non: mọi điểm màu lửa (đỏ, cam; đủ đậm màu, không phải mực) xoay sắc +20° (đỏ → cam, cam → vàng), sáng hơn chút."""
    A = np.asarray(g.convert("RGBA")).astype(np.float32)
    hsv = np.asarray(Image.fromarray(A[..., :3].astype(np.uint8), "RGB").convert("HSV")).astype(np.float32)
    h, s, v = hsv[..., 0] * 360 / 255, hsv[..., 1] / 255, hsv[..., 2] / 255
    lua = ((h >= 345) | (h <= 40)) & (s > 0.45) & (v > 0.42)
    h2 = np.where(lua, (h + 20) % 360, h)
    v2 = np.where(lua, np.minimum(1.0, v * 1.06), v)
    out = np.dstack([h2 * 255 / 360, s * 255, v2 * 255]).clip(0, 255).astype(np.uint8)
    rgb = np.asarray(Image.fromarray(out, "HSV").convert("RGB"))
    return Image.fromarray(np.dstack([rgb, A[..., 3].astype(np.uint8)]), "RGBA")


def anh_part(a, a_tl):
    r = a["region"]
    pth = os.path.join(MANH, r + ".png")
    if NON and r in MAT:                              # mắt dạng 1: ảnh vuông vẽ bằng mã (hoa_ho_non.py mat), lưới là ô vuông MAT_NON
        g = Image.open(os.path.join(MANH_NON, r + ".png")).convert("RGBA")
        c = max(8, round(2 * MAT_NON[2] * D_PX * 1.5))
        return anh.loang_mau(g.convert("RGBa").resize((c, c), Image.LANCZOS).convert("RGBA"))
    rieng = NON and os.path.exists(os.path.join(MANH_NON, r + ".png"))     # mảnh vẽ riêng cho dạng 1 (đã đúng màu, không đổi sắc)
    if rieng:
        pth = os.path.join(MANH_NON, r + ".png")
    if GOC:
        g = G.part_goc(a)
        kq = D_PX / a_tl
    elif os.path.exists(pth):
        import hoa_ho_manh as M
        g = Image.open(pth).convert("RGBA")
        kq = D_PX / (a_tl * M.zs()[r])
    elif THIEU:
        import hoa_ho_manh as M
        im_, m = M.thiet_ke(r, 2.0)
        g = Image.fromarray(np.dstack([im_, np.where(m, 255, 0).astype(np.uint8)]), "RGBA")
        kq = D_PX / (a_tl * 2.0)
    else:
        raise SystemExit("thiếu ảnh part " + pth + " (HH_GOC=1: da gốc; HH_THIEU=1: giữ chỗ bằng hình tô phẳng)")
    if NON and not rieng and not r.startswith(("P_zui", "P_ya", "P_yanjing", "P_biyan")):
        g = doi_lua(g)
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g)


def gan_nguyen(sk, slot, anh_ten, att, ten, Wc):
    im = sk.images[anh_ten]
    L = luoi.Luoi(np.array(att["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(att["tris"]).reshape(-1, 3),
                  att["hull"], att["hull"], im.width, im.height, ten=slot)
    V = np.array(att["xy"], float).reshape(-1, 2)
    sk.luoi_gan(slot, anh_ten, L, trongso.cung(L.n, "move"), the_gioi=V)
    if att.get("w"):
        rows = []
        for p, ws in zip(V, att["w"]):
            row = [(ten[k], *[float(v) for v in (np.linalg.inv(Wc[ten[k]]) @ np.array([p[0], p[1], 1.0]))[:2]], float(w)) for k, w in ws if w > 0.002]
            tot = sum(r[3] for r in row) or 1.0
            rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    else:
        b = ten[att["bone"]] if isinstance(att["bone"], int) else att["bone"]
        rows = [[(b, *[float(v) for v in (np.linalg.inv(Wc[b]) @ np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
    sk.atts[slot][anh_ten]["verts"] = rows
    return L


def _goc(M):
    return math.degrees(math.atan2(M[1, 0], M[0, 0]))


def dung():
    D, D0, I, scan = nap_goc()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    assert ten == [b["name"] for b in D["bones"]]
    a_tl = ti_le_atlas(D)
    sk = khung.Sk(TEN_RIG)
    sk.xuong("root")
    sk.xuong("move", "root")
    Wc = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]]) for b in D["bones"]}
    goc0 = {}
    for b in IB:
        if b["name"] == "root":
            continue
        cha = ten[b["parent"]]
        g = [b["x"], b["y"], b["rot"], b["sx"], b["sy"]]
        if b["inherit"]:                              # không thừa hưởng xoay của cha: góc riêng tính từ ma trận thế giới
            g[2] = _goc(Wc[b["name"]]) - _goc(Wc[cha])
        goc0[b["name"]] = g
        kd = K_DAU if NON and b["name"] == "bone5" else 1.0
        if NON and K_CHAN < 1 and b["name"] in CHAN_GOC:
            kd = 1 - (1 - K_CHAN) * CHAN_GOC["bone33"] / CHAN_GOC[b["name"]]
        if NON and K_CHAN < 1 and b["name"] == "all":
            g[1] -= (1 - K_CHAN) * CHAN_GOC["bone33"]
        if NON and b["name"] == "bone8":
            kd = K_DUOI
        sk.xuong(b["name"], "move" if cha == "root" else cha, g[0], g[1], goc=g[2], dai=b["len"], sx=g[3] * kd, sy=g[4] * kd)
    by = {a["slot"]: a for a in D["atts"]}
    slots = [s["name"] for s in I["slots"] if s["name"] not in BO_SLOT and s["name"] in by and by[s["name"]].get("region")]
    tong = [0, 0]
    for s in ([] if CHIBI else slots):
        a = by[s]
        r = a["region"]
        if NON and s in MAT:                          # mắt tròn to: lưới là một ô vuông bám xương đầu (mắt mở và mắt nhắm cùng ô)
            cx, cy, rr = MAT_NON
            a = dict(a, uv=[0, 0, 1, 0, 1, 1, 0, 1], xy=[cx - rr, cy + rr, cx + rr, cy + rr, cx + rr, cy - rr, cx - rr, cy - rr],
                     tris=[0, 1, 2, 0, 2, 3], hull=4, w=[[[ten.index("bone5"), 1]]] * 4)
        sk.slot(s, "move", r, an=(s == "P_biyan"))
        if r not in sk.images:
            sk.anh(r, anh_part(a, a_tl))
        L = gan_nguyen(sk, s, r, a, ten, Wc)
        tong[0] += L.n
        tong[1] += len(L.tris)

    def xuong_nang(slot):
        nang = {}
        for ws in by[slot].get("w") or []:
            for k, w in ws:
                nang[ten[k]] = nang.get(ten[k], 0.0) + w
        return max(nang, key=nang.get) if nang else ten[by[slot]["bone"]]

    def them(ten_x, slot, cho):
        xg = xuong_nang(slot)
        lp = np.linalg.solve(Wc[xg], np.array([cho[0], cho[1], 1.0]))
        sk.xuong(ten_x, xg, float(lp[0]), float(lp[1]), goc=-_goc(Wc[xg]))
        return xg

    Vz = np.array(by["P_zui"]["xy"], float).reshape(-1, 2)
    xg_m = them("mieng", "P_tou", (Vz[:, 0].max(), Vz[:, 1].mean()))
    Vj = np.array(by["P_L_jiao"]["xy"], float).reshape(-1, 2)
    xg_v = them("vuot", "P_L_jiao", (Vj[:, 0].max(), Vj[:, 1].min()))
    dat_y = min(np.array(by[s]["xy"], float).reshape(-1, 2)[:, 1].min() for s in slots if "jiao" in s)
    for e, m in (("trung", "khung trúng"), ("va", "attack: bàn chân vả xuống"), ("tu", "cast: bắt đầu gồng"), ("gam", "cast: há miệng gầm"),
                 ("het_gam", "cast: hết gầm"), ("bien_mat", "skill: bật tới và biến mất"), ("chem", "skill: một lượt lướt qua đối thủ"),
                 ("hien", "skill: hiện lại ở chỗ cũ"), ("no", "skill: vụ nổ ở đối thủ"), ("dap_dat", "appear: đáp xuống sàn")):
        sk.su_kien(e, m)
    info = dict(scan=scan, IB=IB, ten=ten, goc0=goc0, slots=[s["name"] for s in I["slots"]], dat_y=dat_y)
    if CHIBI:
        import hoa_ho_chibi as C
        P0 = hoat.nuong(sk, lam_clip(sk, info)[1])[0]
        tong = C.lap(sk, by, ten, Wc, P0, D_PX, luoi, anh)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác" + ("" if CHIBI else " (lưới của họ)") +
          f"; atlas của họ {a_tl:.3f} px / đơn vị; mặt đất y = {dat_y:.1f}; miệng trên {xg_m}, vuốt trên {xg_v}")
    return sk, info


# ---------------------------------------------------------------- chuyển động
def chuyen_dong(sk, info):
    S = json.load(open(os.path.join(info["scan"], "sample.json"), encoding="utf-8"))
    IB, ten, goc0 = info["IB"], info["ten"], info["goc0"]
    ids = [i for i, n in enumerate(ten) if n in sk.bi and n != "root"]
    si = {n: i for i, n in enumerate(info["slots"])}
    out = {}
    ref = None
    for clip in ["idle_01"] + [c for c in S if c != "idle_01"]:
        fr = S[clip]["frames"]
        L = np.array([F["l"] for F in fr], float)                     # (khung, xương, 7): x, y, xoay, tỉ lệ x, y, xô
        Wm = np.array([F["m"] for F in fr], float)                    # (khung, xương, 4): a, b, c, d thế giới
        res = {}
        for i in ids:
            g = goc0[ten[i]]
            rot = L[:, i, 2]
            if IB[i]["inherit"]:
                p = IB[i]["parent"]
                rot = np.degrees(np.arctan2(Wm[:, i, 2], Wm[:, i, 0]) - np.arctan2(Wm[:, p, 2], Wm[:, p, 0]))
            A = np.stack([rot - g[2], L[:, i, 0] - g[0], L[:, i, 1] - g[1], L[:, i, 3] / (g[3] or 1.0), L[:, i, 4] / (g[4] or 1.0)], 1)
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            # khung ĐẦU của mọi clip về cùng vòng với khung đầu idle (pha hai clip không quay thừa một vòng)
            moc = ref[ten[i]][0, 0] if ref is not None and ten[i] in ref else 0.0
            A[:, 0] -= 360.0 * round((A[0, 0] - moc) / 360.0)
            res[ten[i]] = A
        if ref is None:
            ref = res
        hien = np.array([F["a"][si["P_shenti_01"]] for F in fr], float)
        nham = np.array([1.0 if F["n"][si["P_biyan"]] else 0.0 for F in fr])
        out[clip] = (float(S[clip]["dur"]), res, hien, nham)
    return out


def ease(u, k="io"):
    u = min(1.0, max(0.0, u))
    if k == "io":
        return u * u * (3 - 2 * u)
    if k == "out":
        return 1 - (1 - u) ** 2
    if k == "in":
        return u * u
    return u


def tmap(t, moc):
    """ánh xạ giờ từng đoạn: moc = [(t, tau[, kiểu])...]; kiểu áp cho đoạn KẾT THÚC ở mốc đó."""
    if t <= moc[0][0]:
        return moc[0][1]
    for a, b in zip(moc, moc[1:]):
        if t <= b[0]:
            u = (t - a[0]) / max(1e-9, b[0] - a[0])
            return a[1] + (b[1] - a[1]) * ease(u, b[2] if len(b) > 2 else "lin")
    return moc[-1][1]


# giờ của mình → giờ clip nguồn
M_ATTACK = [(0.0, 0.0), (0.30, 0.31, "io"), (0.44, 0.335, "lin"), (0.52, 0.45, "in"), (0.74, 0.62, "out"), (1.20, 1.133, "io")]
M_CAST = [(0.0, 0.0), (0.42, 0.36, "io"), (0.70, 0.73, "in"), (1.45, 1.27, "lin"), (2.10, 2.0, "io")]
T_BIEN = 16 / 30.0                                        # skill: giờ (của mình) biến mất hẳn
T_LUOT0 = 19 / 30.0                                       # lượt lướt đầu
T_HIEN = T_LUOT0 + N_LUOT * LUOT + 5 / 30.0              # hiện lại ở chỗ cũ
M_SKILL_A = [(0.0, 0.0), (0.36, 0.35, "io"), (T_BIEN, 0.53, "in")]
M_SKILL_B = [(T_HIEN, 0.97), (T_HIEN + 0.93, 1.9, "lin")]
D_SKILL = T_HIEN + 0.93
TAU_VO = 1.04                                        # dáng vồ duỗi dài của skill_04 (dùng cho các lượt lướt)
M_APPEAR = [(0.0, 0.97), (0.93, 1.9, "lin")]


def lam_clip(sk, info, cao=1000.0):
    CD = chuyen_dong(sk, info)

    def dat(P, goc, tau, lap=False):
        dur, R, hien, nham = CD[goc]
        n = len(hien)
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * FPS
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        for b, A in R.items():
            v = A[i0] * (1 - w) + A[i1] * w
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        k = i0 if w < 0.5 else i1
        P.alpha["P_biyan"] = float(nham[k])
        P.alpha["P_yanjing"] = 1.0 - float(nham[k])
        return float(hien[i0] * (1 - w) + hien[i1] * w)

    def dam(P, a):
        if a < 0.999:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])

    def rung(t, t0, t1, bien):
        if t0 <= t <= t1:
            k = int((t - t0) * FPS) // 2
            return bien * (1 if k % 2 == 0 else -1) * min(1.0, (t1 - t) / 0.12)
        return 0.0

    def f_idle(t, P):
        dat(P, "idle_01", t, True)

    # xương của bốn chân (đùi và mọi xương con): bản chibi cho chân bước NGẮN hơn ở clip chạy
    cha = {b["name"]: info["ten"][b["parent"]] for b in info["IB"] if b["name"] != "root"}
    chan_x = set()
    for b in cha:
        x = b
        while x in cha:
            if x in CHAN_GOC:
                chan_x.add(b)
                break
            x = cha[x]
    K_BUOC = float(os.environ.get("HH_BUOC", "0.5"))

    nho_walk = {}

    def f_walk(t, P):
        dat(P, "run_01", t, True)
        if CHIBI:
            # bản chibi: thân nhún quanh DÁNG ĐỨNG idle (khung 0) với K_BUOC lần dao động của run_01 (lệch so với dáng trung bình của vòng
            # chạy); chân do IK lo (hoa_ho_chibi.ik: bước tự viết, bàn chân bám đất). Dịu về dáng gốc của rig (bản trước) thì cả thân hạ
            # thấp hơn dáng đứng, chân có độ dài cố định phải gập gục xuống.
            if not nho_walk:
                dur = CD["run_01"][0]
                n = int(round(dur * FPS))
                tong = {}
                for k in range(n):
                    Q = khung.Pose()
                    dat(Q, "run_01", k / FPS, True)
                    for b, g in Q.t.items():
                        s = tong.setdefault(b, [0.0] * 5)
                        for q in range(5):
                            s[q] += g[q] / n
                    for b in tong:
                        if b not in Q.t:
                            tong[b][3] += 1.0 / n
                            tong[b][4] += 1.0 / n
                Q0 = khung.Pose()
                dat(Q0, "idle_01", 0.0, True)
                nho_walk["tb"], nho_walk["idle"] = tong, Q0.t
            tb, i0 = nho_walk["tb"], nho_walk["idle"]
            moi = {}
            for b in set(P.t) | set(tb) | set(i0):
                if b == "move":
                    continue
                g = P.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
                m = tb.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
                z = i0.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
                moi[b] = [z[0] + K_BUOC * (g[0] - m[0]), z[1] + K_BUOC * (g[1] - m[1]), z[2] + K_BUOC * (g[2] - m[2]),
                          z[3] * (1 + K_BUOC * (g[3] / (m[3] or 1.0) - 1)), z[4] * (1 + K_BUOC * (g[4] / (m[4] or 1.0) - 1))]
            mv = P.t.get("move")
            P.t.clear()
            P.t.update(moi)
            if mv:
                P.t["move"] = mv

    def f_hit(t, P):
        dat(P, "hit_01", t)

    def f_die(t, P):
        d = CD["die_01"][0]
        dat(P, "die_01", t)
        dam(P, float(np.clip(1.0 - (t - d) / (TAN - 0.1), 0.0, 1.0)))

    def f_attack(t, P):
        dat(P, "skill_01_1", tmap(t, M_ATTACK))
        # dộng nhẹ cả thân lúc bàn chân vả xuống
        k = math.exp(-((t - 0.54) / 0.05) ** 2)
        P.scale("move", 1 + 0.03 * k, 1 - 0.035 * k)
        P.move("move", rung(t, 0.52, 0.70, 5.0), 0.0)

    def f_cast(t, P):
        dat(P, "skill_03", tmap(t, M_CAST))
        g = hoat.bao(t, 0.70, 1.45, 0.06, 0.15) if hasattr(hoat, "bao") else 0.0
        P.move("move", rung(t, 0.70, 1.45, 6.0), 0.0)
        P.scale("move", 1 + 0.025 * g, 1 + 0.035 * g)

    def f_skill(t, P):
        # Mọi lần ẩn / hiện rơi đúng khung mẫu (30 khung/giây): runtime nội suy thẳng giữa hai khoá nên lật ngang (tỉ lệ x đổi dấu) chỉ được
        # xảy ra giữa HAI khung ẩn, không thì lộ một vạch mỏng lúc tỉ lệ đi qua 0 (soi runtime thật 2026-11-14).
        i = int(round(t * FPS))
        i_b, i_l, i_h = int(round(T_BIEN * FPS)), int(round(T_LUOT0 * FPS)), int(round(T_HIEN * FPS))
        if i < i_h and i >= i_b - 0:
            j = i - i_l
            if 0 <= j < 3 * N_LUOT:
                k, ph = divmod(j, 3)
                dat(P, "skill_04", TAU_VO)
                # lượt chẵn lướt sang phải (xuyên qua đối thủ), lượt lẻ lật lại lướt ngược về; lệch cao thấp, nghiêng mỗi lượt
                sg = 1.0 if k % 2 == 0 else -1.0
                x = (1.55 + sg * (ph / 2.0 - 0.5) * 1.7) * cao
                y = (0.10 + 0.16 * math.sin(k * 2.1)) * cao
                P.move("move", x, y)
                P.rot("move", sg * 9.0 * math.sin(k * 1.3 + 0.5))
                P.scale("move", sg * 1.12, 0.92)
                dam(P, 1.0 if ph == 1 else 0.0)
            elif j < 0:                                               # vừa tan: giữ dáng và chỗ cuối cú bật
                dat(P, "skill_04", 0.53)
                P.move("move", 0.55 * cao, 0.0)
                dam(P, 0.0)
            else:                                                     # hết lượt: chờ ở chỗ cũ, ẩn
                dat(P, "skill_04", M_SKILL_B[0][1])
                dam(P, 0.0)
        elif i < i_b:
            dat(P, "skill_04", tmap(t, M_SKILL_A))
            u = ease((t - 0.36) / (T_BIEN - 0.36), "in") if t > 0.36 else 0.0
            P.move("move", 0.55 * cao * u, 0.0)                       # bật tới trước khi tan
            dam(P, 1.0 if i < i_b - 1 else 0.5)
        else:
            dat(P, "skill_04", tmap(t, M_SKILL_B))
            dam(P, min(1.0, (i - i_h + 1) / 2.0))

    def f_appear(t, P):
        i = int(round(t * FPS))
        dat(P, "skill_04", tmap(t, M_APPEAR))
        u = ease(t / 0.30, "out")
        P.move("move", -0.85 * cao * (1 - u), 0.30 * cao * math.sin(math.pi * min(1.0, t / 0.30)) * (1 - u * 0.5))
        dam(P, min(1.0, i / 2.0))

    ev_skill = [(0.36, "bien_mat", "")] + [(round(T_LUOT0 + k * LUOT + 1 / 30.0, 3), "chem", str(k)) for k in range(N_LUOT)] + \
               [(round(T_HIEN, 3), "hien", ""), (round(T_HIEN + 0.30, 3), "no", ""), (round(T_HIEN + 0.30, 3), "trung", "")]
    clips = [
        Clip("appear", 0.93, f_appear, ev=[(0.27, "dap_dat", "")]),
        Clip("idle", CD["idle_01"][0], f_idle, loop=True),
        Clip("walk", CD["run_01"][0], f_walk, loop=True),
        Clip("attack", M_ATTACK[-1][0], f_attack, ev=[(0.50, "va", ""), (0.50, "trung", "")]),
        Clip("cast", M_CAST[-1][0], f_cast, ev=[(0.20, "tu", ""), (0.70, "gam", ""), (0.74, "trung", ""), (1.45, "het_gam", "")]),
        Clip("skill", D_SKILL, f_skill, ev=ev_skill, trung=T_HIEN + 0.30),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", CD["die_01"][0] + TAN, f_die),
    ]
    if CHIBI and getattr(sk, "chan_chibi", None):     # bản chibi có xương chân riêng: đặt chân bằng IK sau khi hàm clip đã đặt thân
        import hoa_ho_chibi as C

        def boc(f, ten, dur):
            def g(t, P):
                f(t, P)
                C.ik(sk, P, t, ten, dur)
            return g

        for c in clips:
            c.fn = boc(c.fn, c.ten, c.dur)
    return clips


BO_CAO = ("c_duoi", "c_bom", "P_weiba_01", "P_weiba_02", "P_maofa_23", "P_maofa_23_01", "P_maofa_24", "P_maofa_03", "P_maofa_04")


def main(a):
    sk, info = dung()
    ve0 = soi.Ve(sk)
    P0 = khung.Pose() if hasattr(khung, "Pose") else None
    clips = lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0, BO_CAO) - info["dat_y"]
    clips = lam_clip(sk, info, cao)
    print(f"chiều cao thân (không tính đuôi, chỏm lửa) {cao:.0f}; skill dài {D_SKILL:.2f} s, hiện lại {T_HIEN:.2f}")
    ra = os.environ.get("HH_RA") or (os.path.join(HERE, "inbox", "hoa_ho_non", "rig_chibi" if CHIBI else "rig") if NON else os.path.join(G.BASE, "rig_goc" if GOC else "rig"))
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        if ":" in a[2]:
            t0, t1, n = a[2].split(":")
            ts = list(np.linspace(float(t0), float(t1), int(n)))
        elif a[2].startswith("n="):
            ts = list(np.linspace(0, c.dur, int(a[2][2:])))
        else:
            ts = [float(x) for x in a[2].split(",")]
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve0.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 0.3
        ims = [ve0.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB") for P in Ps]
        from PIL import ImageDraw
        cot = min(len(ims), 6)
        hang = (len(ims) + cot - 1) // cot
        out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang), (150, 150, 150))
        for i, im in enumerate(ims):
            ImageDraw.Draw(im).text((6, 4), f"{ts[i]:.2f}", fill=(255, 255, 255))
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(ra, exist_ok=True)
        pth = os.path.join(ra, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    frames = {c.ten: hoat.nuong(sk, c) for c in clips}
    for c in clips:
        if c.ten in ("appear", "attack", "cast", "skill", "hit"):
            frames[c.ten] = [P.copy() for P in frames[c.ten]]
            hoat.khop_cuoi(frames[c.ten], frames["idle"][0], 0.2)
    xuat.xuat_het(sk, clips, ra, TEN_RIG, "Hổ lửa (hoa_ho): tướng thứ 9 đảo Hỏa" + (" — DA GỐC, chỉ để soi clip" if GOC else " — dạng 1 (hổ con)" if NON else ""),
                  frames=frames, dang=1 if NON else 2, so_dang=2, dung_yen=("cast",), lao=("skill",), ma_goc=None, khop_idle=0, cao=cao + info["dat_y"],
                  noi_them={}, impact=IMPACT, tol={"rotate": 0.08, "translate": 0.2, "scale": 0.0015}, dich_mb=0.6, tran_mb=1.0, span=SPAN)


if __name__ == "__main__":
    main(sys.argv[1:])
