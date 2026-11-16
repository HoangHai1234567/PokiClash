# -*- coding: utf-8 -*-
"""Tinh linh tinh thể sắt DẠNG 2 (tinh_sat_2; tướng 1 đảo Kim, dạng cuối): hình của mình chạy trên ĐÚNG rig của con gốc monster_3347 (dạng tiến
hoá của monster_3346 mà dạng 1 bám). Ghi chú: inbox/tinh_sat_ghichu.md mục 6. Cách làm như tinh_sat_rig.py (dạng 1):
- XƯƠNG: đủ mọi xương của họ; hai IK chân và transform `rotate_01` KHÔNG chép: dùng biến đổi riêng ĐÃ ÁP lấy mẫu bằng runtime thật
  (sample_goc.json, trường `l`). Thêm `move` (cú lao, cú nhảy), `day` (ở MẶT ĐẤT dưới thân: tâm phình / bẹp; cha của `bone2`), `xoay` (TÂM THÂN,
  con của `bone`, cha của `bone3`, `bone15`, `rotate_01`: lộn vòng cả thân lẫn vòng tinh thể).
- MẢNH: mảnh "đúng chỗ, đúng cỡ" cắt từ concept A (tinh_sat_2_manh.py → inbox/tinh_sat_2/manh/), mỗi mảnh lưới 4 đỉnh đặt đúng chỗ concept ở
  dáng idle 0, bám xương (trọng số) của part cũ. Mắt ba hình: `P_yanjing` (mở + mày), `P_biyan` (nhắm `> <`), `P_biyan2` (chớp). Bàn chân rời
  ở clip chết (`P_tui_R1_2`, `P_tui_L1_1`) dùng lại ảnh bàn chân của mình, đặt bằng phép dời cứng khớp lưới bàn chân của họ. BỎ `shadow`.
  Thêm 5 tinh thể NHÂN BẢN (`tt1..tt5`, slot `P_bc_0k_b`, ẩn) cho chiêu mana.
- CHUYỂN ĐỘNG (người dùng 2026-11-16: như dạng 1 nhưng mạnh hơn):
    idle = idle_01, walk = run_01, hit = hit_01, die = die_01 + tan (như họ);
    attack = skill_01 (ngả ra sau, tinh thể cuộn ra trước mặt thành khiên mũi nhọn) rồi LAO TÔNG: quãng tới dồn vào `move`, đỉnh lao 0,68 chiều
             cao đúng khung tông, bẹp mạnh hơn dạng 1;
    cast   = GỌI TINH THỂ: vòng tinh thể xoay một vòng quanh người (skill_02), mỗi tinh thể TÁCH ĐÔI (nhân bản), 10 tinh thể bay lên xếp vòng cung
             trên đầu, mũi chĩa về đối thủ, lần lượt PHÓNG (sự kiện `ban`, chuỗi = tên xương; đường bay do code game), rồi mọc lại;
    skill  = PHÌNH TO ba nhịp (tới 1,8 lần) + vòng tinh thể quay tít quanh người, nhún, BẬT (`bat`), khựng + lộn một vòng ở đỉnh, cắm xuống;
    skill_land = DẬP (`cham_dat`) bẹp mạnh, tinh thể cắm phập xuống quanh người, RUNG squash stretch 5 nhịp tắt dần;
    appear = thân bật ra, tinh thể bay từ ngoài vào xoay rồi ráp quanh người.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tinh_sat_2_rig.py        → inbox/tinh_sat_2/rig/
    py -3 -I ArtGen/Spine/tinh_sat_2_rig.py soi <clip> <giây,giây,...|n=12|t0:t1:n> [tỉ lệ]   → rig/soi_<clip>.png
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
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, khung, hoat, xuat, soi, luoi, trongso  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import tinh_sat_2 as G  # noqa: E402
from hoa_ho_rig import ease, tmap, _goc  # noqa: E402

TEN_RIG = "tinh_sat_2"
D_PX = float(os.environ.get("TS_DPX", "1.2"))        # pixel ảnh atlas cho mỗi đơn vị rig
BO_SLOT = ("shadow",)
MANH_MOI = os.path.join(G.BASE, "manh")
TAN = 0.45
FPS = 30.0
IMPACT = {"attack": (0.10, 0.55, 0.14), "cast": (0.10, 0.6, 0.14, "#e8eefc44"), "skill": (0.26, 1.4, 0.34, "#ffffffaa")}

# tinh thể bay: xương mảnh → (xương quỹ đạo cha, slot)
TT = {"bone17": ("bone6", "P_bc_01"), "bone16": ("bone5", "P_bc_02"), "bone18": ("bone4", "P_bc_03"), "bone19": ("bone7", "P_bc_04"),
      "bone20": ("bone8", "P_bc_05")}
NHAN = {"tt1": "bone17", "tt2": "bone16", "tt3": "bone18", "tt4": "bone19", "tt5": "bone20"}   # bản sao → bản gốc
BAY = ["bone17", "tt1", "bone16", "tt2", "tt3", "bone18", "tt4", "bone19", "tt5", "bone20"]   # chỗ xếp trên đầu, trái → phải
PHONG = ["bone18", "tt3", "tt2", "tt4", "bone16", "bone19", "tt1", "tt5", "bone17", "bone20"]  # thứ tự phóng (giữa ra ngoài)
QUY_DAO = ("bone4", "bone5", "bone6", "bone7", "bone8")     # cha của 5 xương tinh thể (noScale)
DICH = (760.0, 230.0)                                # điểm (rig) các mũi tinh thể chĩa vào lúc chờ phóng: thân đối thủ bên phải
TAM_THAN = (15.1, 160.0)                             # tâm thân (xương `xoay`)


# ---------------------------------------------------------------- nạp
def nap_goc():
    scan = G.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    D0 = json.load(open(os.path.join(scan, "att_idle0.json"), encoding="utf-8"))
    return D, I, D0, scan


def tf():
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    W, H = 1536, 1024
    to_rig = lambda P: np.stack([cx + (P[:, 0] - W / 2) / s, cy - (P[:, 1] - H / 2) / s], 1)  # noqa: E731
    return s, to_rig


def mat3(b):
    return np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]])


def anh_moi(sk, ten_anh):
    if ten_anh in sk.images:
        return sk.images[ten_anh]
    D = json.load(open(os.path.join(MANH_MOI, "dat.json")))
    if ten_anh not in D:
        raise SystemExit(f"thiếu mảnh {ten_anh} (tinh_sat_2_manh.py cat)")
    s_px, _ = tf()
    g = Image.open(os.path.join(MANH_MOI, ten_anh + ".png")).convert("RGBA")
    kq = D_PX / s_px
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    sk.anh(ten_anh, anh.loang_mau(g))
    return sk.images[ten_anh]


def goc_the_gioi(ten_anh):
    """bốn góc (trái dưới, trái trên, phải trên, phải dưới) của mảnh trên concept → thế giới rig ở dáng idle 0."""
    D = json.load(open(os.path.join(MANH_MOI, "dat.json")))
    x0, y0, x1, y1 = D[ten_anh]["hop"]
    _, to_rig = tf()
    return to_rig(np.array([[x0, y1], [x0, y0], [x1, y0], [x1, y1]], float))


def gan_4(sk, slot, ten_att, ten_anh, V, rows_w, Wi):
    """lưới 4 đỉnh: góc V (thế giới ở dáng mà ma trận Wi mô tả), trọng số rows_w; điểm gắn tính bằng Wi."""
    im = anh_moi(sk, ten_anh)
    uv = np.array([[0, im.height], [0, 0], [im.width, 0], [im.width, im.height]], float)
    L = luoi.Luoi(uv, np.array([[0, 1, 2], [2, 3, 0]]), 4, 4, im.width, im.height, ten=slot)
    rows, Vs = [], []
    for p, ws in zip(V, rows_w):
        tot = sum(ws.values())
        row, q = [], np.zeros(2)
        for b, w in ws.items():
            lp = np.linalg.solve(Wi[b], np.array([p[0], p[1], 1.0]))
            row.append((b, float(lp[0]), float(lp[1]), w / tot))
            q += (w / tot) * (sk.W0[b] @ lp)[:2]
        rows.append(row)
        Vs.append(q)
    sk.luoi_gan(slot, ten_anh, L, trongso.cung(L.n, "move"), the_gioi=np.array(Vs), ten=ten_att)
    sk.atts[slot][ten_att]["verts"] = rows
    return L


def trong_so(att, V, ten):
    """trọng số cho các góc V theo lưới cũ (3 đỉnh gần nhất) hoặc một xương."""
    if att.get("w"):
        Q = np.array(att["xy"], float).reshape(-1, 2)
        out = []
        for p in V:
            d = np.hypot(*(Q - p).T)
            k = np.argsort(d)[:3]
            ww = 1.0 / np.maximum(d[k], 1.0) ** 2
            acc = {}
            for j, wj in zip(k, ww / ww.sum()):
                for b, w in att["w"][j]:
                    acc[ten[b]] = acc.get(ten[b], 0.0) + wj * w
            tot = sum(acc.values())
            out.append({b: w / tot for b, w in acc.items() if w / tot > 0.01})
        return out
    b = ten[att["bone"]] if isinstance(att["bone"], int) else att["bone"]
    return [{b: 1.0}] * 4


def khop_cung(A, B):
    """phép dời cứng (xoay + tịnh tiến) đưa tập điểm A về B (bình phương nhỏ nhất)."""
    ca, cb = A.mean(0), B.mean(0)
    U, _, Vt = np.linalg.svd((A - ca).T @ (B - cb))
    R = (U @ Vt).T
    if np.linalg.det(R) < 0:
        Vt[-1] *= -1
        R = (U @ Vt).T
    return lambda P: (P - ca) @ R.T + cb, float(np.abs((A - ca) @ R.T + cb - B).max())


def dung():
    D, I, D0, scan = nap_goc()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    sk = khung.Sk(TEN_RIG)
    sk.xuong("root")
    sk.xuong("move", "root")
    Wc = {b["name"]: mat3(b) for b in D["bones"]}
    Wi = {b["name"]: mat3(b) for b in D0["bones"]}
    x_day = float(Wc["bone3"][0, 2])
    sk.xuong("day", "move", x_day, 0.0)
    goc0 = {}
    the_gioi_goc = {b["name"]: (Wc[b["name"]][0, 2], Wc[b["name"]][1, 2]) for b in D["bones"]}
    con_xoay = ("bone3", "bone15", "rotate_01")
    for b in IB:
        n = b["name"]
        if n == "root":
            continue
        cha = ten[b["parent"]]
        g = [b["x"], b["y"], b["rot"], b["sx"], b["sy"]]
        goc0[n] = g
        if cha == "root":
            sk.xuong(n, "day", g[0] - x_day, g[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
        elif n in con_xoay:
            if "xoay" not in sk.bi:                     # tâm thân: con của `bone`, chỉ tịnh tiến
                bx, by = the_gioi_goc["bone"]
                sk.xuong("xoay", "bone", TAM_THAN[0] - bx, TAM_THAN[1] - by)
            wx, wy = the_gioi_goc[n]
            sk.xuong(n, "xoay", wx - TAM_THAN[0], wy - TAM_THAN[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
        else:                                           # xương quỹ đạo tinh thể: không nhận tỉ lệ của cha (bẹp không kéo dẹt tinh thể), giu_hinh bù
            sk.xuong(n, cha, g[0], g[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4], khong_ti_le=n in QUY_DAO)
    for nb, goc in NHAN.items():                        # tinh thể nhân bản: xương con của `move`, dáng gốc trùng xương tinh thể gốc
        M = sk.W0[goc]
        sk.xuong(nb, "move", float(M[0, 2]), float(M[1, 2]), goc=_goc(M))
    by = {}
    for a in D["atts"]:
        by.setdefault(a["slot"], []).append(a)
    by0 = {(a["slot"], a["region"]): a for a in D0["atts"]}
    slots = [s["name"] for s in I["slots"] if s["name"] not in BO_SLOT and s["name"] in by]
    tong = [0, 0]
    for s in slots:
        cur = [a for a in by[s] if a["cur"]]
        sk.slot(s, "move", cur[0]["region"] if cur else None)
        if s in ("P_tui_R1_2", "P_tui_L1_1"):            # bàn chân rời (clip chết): ảnh bàn chân của mình, dời cứng theo lưới của họ
            nguon = "P_tui_R1" if s == "P_tui_R1_2" else "P_tui_L1"
            a_src = by0[(nguon, nguon)]
            a_dst = by[s][0]
            A = np.array(a_src["xy"], float).reshape(-1, 2)
            B = np.array(a_dst["xy"], float).reshape(-1, 2)
            f, sai = khop_cung(A, B)
            V = f(goc_the_gioi(nguon))
            b = ten[a_dst["bone"]] if isinstance(a_dst["bone"], int) else a_dst["bone"]
            L = gan_4(sk, s, a_dst["region"], nguon, V, [{b: 1.0}] * 4, Wc)
            print(f"  {s}: ảnh {nguon}, khớp cứng lưới của họ lệch {sai:.2f} đơn vị")
            tong[0] += L.n
            tong[1] += len(L.tris)
            continue
        for a in sorted(by[s], key=lambda q: not q["cur"]):
            r = a["region"]
            a0 = by0.get((s, r))
            if a0 is None:                               # hình không bật ở idle 0 (mắt nhắm, chớp): khung của mắt mở ở idle 0
                a0 = by0[(s, cur[0]["region"])]
            V = goc_the_gioi(r)
            L = gan_4(sk, s, r, r, V, trong_so(a0, V, ten), Wi)
            tong[0] += L.n
            tong[1] += len(L.tris)
        if s in [TT[b][1] for b in TT]:                  # bản sao chèn ngay sau tinh thể gốc
            goc = next(b for b in TT if TT[b][1] == s)
            nb = next(k for k, v in NHAN.items() if v == goc)
            s2 = s + "_b"
            sk.slot(s2, "move", s, an=True)
            att = sk.atts[s][s]
            rows = [[(nb if b == goc else b, x, y, w) for b, x, y, w in row] for row in att["verts"]]
            sk.luoi_gan(s2, s, sk.luoi[(s, s)], trongso.cung(4, "move"), the_gioi=np.array(att["V"]), ten=s)
            sk.atts[s2][s]["verts"] = rows
    # trục chính từng tinh thể (dáng gốc): (tâm hình, góc của đầu mũi)
    truc = {}
    tam = np.array(TAM_THAN)
    for b, (_, s) in TT.items():
        V = np.array(sk.atts[s][s]["V"], float)
        c = V.mean(0)
        a0 = by0[(s, s)]
        Q = np.array(a0["xy"], float).reshape(-1, 2)
        _, _, vt = np.linalg.svd(Q - Q.mean(0))
        ax = vt[0]
        pr = (Q - Q.mean(0)) @ ax
        if np.dot(ax, Q.mean(0) - tam) < 0:
            ax = -ax                                     # mũi = đầu chĩa ra ngoài thân
        truc[b] = (c, math.degrees(math.atan2(ax[1], ax[0])))
    for nb, goc in NHAN.items():
        truc[nb] = truc[goc]
    for e, m in (("trung", "khung trúng"), ("tong", "attack: thân tông vào đối thủ"), ("tu", "cast: gọi tinh thể"),
                 ("ban", "cast: một tinh thể phóng đi (chuỗi = tên xương; ẩn trong rig, code game cho bay)"), ("het_ban", "cast: hết loạt phóng"),
                 ("moc", "cast: tinh thể mới mọc lại"), ("bat", "skill: rời đất (cung nhảy do code)"), ("cham_dat", "skill_land: dập xuống")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác")
    return sk, dict(scan=scan, IB=IB, ten=ten, goc0=goc0, slots=[s["name"] for s in I["slots"]], truc=truc, Wc=Wc, tam=tam)


# ---------------------------------------------------------------- chuyển động
def chuyen_dong(sk, info):
    S = json.load(open(os.path.join(info["scan"], "sample_goc.json"), encoding="utf-8"))
    ten, goc0 = info["ten"], info["goc0"]
    ids = [i for i, n in enumerate(ten) if n in sk.bi and n != "root"]
    co_slot = [(i, n) for i, n in enumerate(info["slots"]) if n in sk.si]
    out = {}
    ref = None
    for clip in ["idle_01"] + [c for c in S if c != "idle_01"]:
        fr = S[clip]["frames"]
        L = np.array([F["l"] for F in fr], float)
        res = {}
        for i in ids:
            g = goc0[ten[i]]
            A = np.stack([L[:, i, 2] - g[2], L[:, i, 0] - g[0], L[:, i, 1] - g[1], L[:, i, 3] / (g[3] or 1.0), L[:, i, 4] / (g[4] or 1.0)], 1)
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            moc = ref[ten[i]][0, 0] if ref is not None and ten[i] in ref else 0.0
            A[:, 0] -= 360.0 * round((A[0, 0] - moc) / 360.0)
            res[ten[i]] = A
        if ref is None:
            ref = res
        hinh = {n: [F["n"][i] for F in fr] for i, n in co_slot}
        out[clip] = (float(S[clip]["dur"]), res, len(fr), hinh)
    return out


T_TONG = 0.50
M_ATTACK = [(0.0, 0.0), (0.42, 14 / 30.0, "io"), (T_TONG, 17.5 / 30.0, "in"), (0.64, 20 / 30.0, "out"), (1.0, 30 / 30.0, "io")]
LAO = 0.68
# cast
CO_TREO = 0.72                                        # cỡ tinh thể lúc treo trên đầu
T_GOM = 0.55                                          # vòng tinh thể xoay xong một vòng (skill_02 khung 20)
T_TACH0, T_TACH1 = 0.30, 0.55                         # bản sao tách ra khỏi tinh thể gốc
T_LEN, LEN_CACH, LEN_DAI = 0.52, 0.03, 0.34
T_BAN0, BAN_CACH = 1.05, 0.06
T_HET = T_BAN0 + (len(PHONG) - 1) * BAN_CACH + 0.06
T_MOC = T_HET + 0.12
MOC_CACH, MOC_DAI = 0.03, 0.26
D_CAST = T_MOC + (len(TT) - 1) * MOC_CACH + MOC_DAI + 0.22
# chiêu cuối
PHINH = 1.80
T_BOM = (0.18, 0.48, 0.85)
T_NEN0, T_BAT = 0.98, 1.24
T_DINH0, T_DINH1 = 1.50, 1.74
D_SKILL = 1.86
BAY_DANG = (0.74, 1.36)
T_CHAM, D_LAND = 3 / 30.0, 1.25
SPAN = 4.6


def lam_clip(sk, info, cao=400.0):
    CD = chuyen_dong(sk, info)
    truc, tam, Wc = info["truc"], info["tam"], info["Wc"]
    slot_cua = {b: TT[b][1] for b in TT}
    slot_cua.update({nb: TT[g][1] + "_b" for nb, g in NHAN.items()})

    def dat(P, goc, tau, lap=False, mat=True):
        dur, R, n, Hh = CD[goc]
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
        k = min(n - 1, int(round(x)))
        for s, seq in Hh.items():
            if s == "P_yanjing" and not mat:
                continue
            P.att[s] = seq[k]

    def dam(P, a, chi=None):
        if a < 0.999:
            for sl in sk.slots:
                if chi is None or sl["name"] in chi:
                    P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])

    def rung(t, t0, t1, bien, ra=0.12):
        if t0 <= t <= t1:
            k = int((t - t0) * FPS) // 2
            return bien * (1 if k % 2 == 0 else -1) * min(1.0, (t1 - t) / ra)
        return 0.0

    def dat_tg(P, b, xy, goc_tg, k=1.0):
        if k <= 1e-4:
            return
        W = sk.the_gioi(P)
        cha = sk.bones[sk.bi[b]]["parent"]
        Wp = W[cha]
        lp = np.linalg.solve(Wp, np.array([xy[0], xy[1], 1.0]))
        b0 = sk.bones[sk.bi[b]]
        g = P._g(b)
        dx, dy = float(lp[0]) - b0["x"], float(lp[1]) - b0["y"]
        dr = goc_tg - _goc(Wp) - b0["rot"]
        cur = _goc(W[b]) - _goc(Wp) - b0["rot"]
        dr = cur + ((dr - cur + 180.0) % 360.0 - 180.0)
        g[0] += k * (dx - g[0])
        g[1] += k * (dy - g[1])
        g[2] += k * (dr - g[2])

    def tg_xuong(P, b):
        W = sk.the_gioi(P)
        return W[b][:2, 2].copy(), _goc(W[b])

    def giu_hinh(P):
        """tinh thể nhận tỉ lệ ĐỀU = trung bình nhân tỉ lệ của day × xoay: phình thì to theo, bẹp thì không bị kéo dẹt."""
        a = P.t.get("day", [0, 0, 0, 1.0, 1.0])
        b = P.t.get("xoay", [0, 0, 0, 1.0, 1.0])
        m = math.sqrt(abs(a[3] * b[3] * a[4] * b[4]))
        if abs(m - 1.0) > 1e-4:
            for qd in QUY_DAO:
                P.scale(qd, m, m)

    def pha(Pa, Pb, w):
        Q = khung.Pose()
        for b in set(Pa.t) | set(Pb.t):
            a_ = Pa.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            b_ = Pb.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            Q.t[b] = [a_[q] + (b_[q] - a_[q]) * w for q in range(5)]
        Q.alpha = dict(Pa.alpha)
        Q.att = dict(Pb.att if w > 0.5 else Pa.att)
        return Q

    # chỗ xếp trên đầu (cast): vòng cung ôm quanh đầu, mũi chĩa về DICH
    CHO = {}
    for i, b in enumerate(BAY):
        a = math.radians(172.0 - 164.0 * i / (len(BAY) - 1))
        x = float(tam[0] + 305.0 * math.cos(a))
        y = float(tam[1] + 70.0 + 230.0 * math.sin(a))
        CHO[b] = (x, y, math.degrees(math.atan2(DICH[1] - y, DICH[0] - x)))

    def f_idle(t, P):
        dat(P, "idle_01", t, True)

    def f_walk(t, P):
        dat(P, "run_01", t, True)

    def f_hit(t, P):
        dat(P, "hit_01", t)

    def f_die(t, P):
        d = CD["die_01"][0]
        dat(P, "die_01", t)
        dam(P, float(np.clip(1.0 - (t - d) / (TAN - 0.1), 0.0, 1.0)))

    def f_attack(t, P):
        tq = tmap(t, M_ATTACK)
        dat(P, "skill_01", tq)
        # họ ném tinh thể vầng (bone4 / P_bc_03) đi ở khung 17: mình giữ nó bên người, kéo dần về chỗ idle từ khung 14
        w = float(np.clip((tq * FPS - 14) / 4.0, 0.0, 1.0))
        if w > 0:
            Pi = khung.Pose()
            dat(Pi, "idle_01", t, True, mat=False)
            for b in ("bone4", "bone18"):
                a_ = P.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
                b_ = Pi.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
                P.t[b] = [a_[q] + (b_[q] - a_[q]) * ease(w) for q in range(5)]
        P.att["P_bc_03"] = "P_bc_03"
        # LAO VÀO TÔNG: đỉnh lao LAO × chiều cao đúng khung tông; sân nắn tới 72 % quãng tới đối thủ
        t_ve = T_TONG + 0.12
        if t < T_TONG - 0.10:
            lao = -0.06 * ease(t / (T_TONG - 0.10))
        elif t < T_TONG:
            lao = -0.06 + (LAO + 0.06) * ease((t - (T_TONG - 0.10)) / 0.10, "in")
        elif t < t_ve:
            lao = LAO
        else:
            lao = LAO * (1 - ease((t - t_ve) / max(0.05, M_ATTACK[-1][0] - 0.06 - t_ve)))
        P.move("move", cao * lao + rung(t, T_TONG + 0.02, T_TONG + 0.20, 6.0), 0.0)
        k = math.exp(-((t - (T_TONG + 0.02)) / 0.05) ** 2)
        P.scale("xoay", 1 - 0.20 * k, 1 + 0.15 * k)                     # bẹp theo chiều tông đúng khung chạm
        giu_hinh(P)

    def f_cast(t, P):
        if t <= T_GOM:
            dat(P, "skill_02", tmap(t, [(0.0, 0.0), (T_GOM, 20 / 30.0, "io")]))
        else:                                         # giữ dáng cuối vòng xoay rồi hoà dần về idle tới lúc mọc lại xong
            Pa, Pb = khung.Pose(), khung.Pose()
            dat(Pa, "skill_02", 20 / 30.0)
            dat(Pb, "idle_01", t - T_GOM, True)
            w = ease((t - T_GOM) / (D_CAST - 0.15 - T_GOM))
            Q = pha(Pa, Pb, 0.35 * ease((t - T_GOM) / 0.4) + 0.65 * w)
            P.t.update(Q.t)
            P.att.update(Q.att)
        P.att["P_yanjing"] = "P_yanjing" if T_GOM - 0.30 < t < T_HET + 0.25 else P.att.get("P_yanjing", "P_yanjing")
        if t > T_GOM - 0.05:
            nh = hoat.bao(t, T_GOM - 0.05, D_CAST - 0.1, 0.25, 0.35)
            P.move("xoay", 0.0, 12.0 * nh + 3.0 * math.sin(t * 9.0) * nh)
        for i in range(len(PHONG)):                   # mỗi lần phóng thân giật nhẹ
            u = t - (T_BAN0 + i * BAN_CACH)
            if 0 <= u < 0.12:
                k = math.sin(math.pi * u / 0.12)
                P.scale("xoay", 1 + 0.04 * k, 1 - 0.035 * k)
        base = P.copy()
        for i, b in enumerate(BAY):
            j = PHONG.index(b)
            t_ban = T_BAN0 + j * BAN_CACH
            goc = NHAN.get(b, b)
            t_moc = T_MOC + list(TT).index(goc) * MOC_CACH
            s = slot_cua[b]
            nhan = b in NHAN
            # đã phóng thì ẩn nhưng GIỮ dáng treo cuối cùng (đổi dáng cùng khung ẩn thì ở 60 khung/giây lọt nửa khung tinh thể quay dở);
            # tinh thể gốc về chỗ cũ trước lúc mọc lại 0,04 s (vẫn ẩn)
            an_sau = t >= t_ban and (nhan or t < t_moc - 0.04)
            tt = min(t, t_ban - 1.0 / 60.0) if an_sau else t
            if nhan:                                  # bản sao: trùng tinh thể gốc rồi tách ra (chạy cả lúc đã ẩn để chọn cùng nhánh góc)
                if t < T_TACH0:
                    P.alpha[s] = 0.0
                    continue
                P.alpha[s] = 0.0 if an_sau else 1.0
                pg, rg = tg_xuong(base, goc)
                dat_tg(P, b, pg, rg)
                u_t = ease((t - T_TACH0) / (T_TACH1 - T_TACH0), "out")
                c0, _ = truc[goc]
                v = c0 - tam
                v = v / (np.hypot(*v) or 1.0)
                g = P._g(b)                           # tách: dời ra ngoài + lệch 25° so với bản gốc
                g[0] += 28.0 * u_t * v[0]
                g[1] += 28.0 * u_t * v[1]
                g[2] += 25.0 * u_t
            if t < t_ban or an_sau:
                u = (tt - (T_LEN + i * LEN_CACH)) / LEN_DAI
                if an_sau:
                    P.alpha[s] = 0.0
                if u <= 0:
                    continue
                k = ease(u, "io")
                x, y, gg = CHO[b]
                bob = 5.0 * math.sin(tt * 7.0 + i) * min(1.0, max(0.0, u - 1.0) * 3)
                lui = 24.0 * ease((tt - (t_ban - 0.08)) / 0.08, "out") if tt > t_ban - 0.08 else 0.0
                gr = math.radians(gg)
                c0, a0 = truc[b]
                W0 = Wc[goc]
                off = np.linalg.solve(W0, np.array([c0[0], c0[1], 1.0]))[:2]
                quay = gg - a0
                ca, sa = math.cos(math.radians(quay)), math.sin(math.radians(quay))
                bx = x - lui * math.cos(gr) - (ca * off[0] - sa * off[1])
                by = y - lui * math.sin(gr) + bob - (sa * off[0] + ca * off[1])
                if u < 1:
                    p0, r0 = tg_xuong(P if nhan else base, b)
                    xy = (p0[0] + (bx - p0[0]) * k, p0[1] + (by - p0[1]) * k + 60.0 * math.sin(math.pi * k))
                    dat_tg(P, b, xy, r0 + ((quay + _goc(W0) - r0 + 180) % 360 - 180) * k)
                else:
                    dat_tg(P, b, (bx, by), quay + _goc(W0))
                sc = (1.0 + 0.12 * math.sin(math.pi * min(1.0, u))) * (1.0 - (1.0 - CO_TREO) * k)   # treo trên đầu: thu nhỏ cho đỡ chồng
                P.scale(b, sc, sc)
            elif t < t_moc:
                P.alpha[s] = 0.0                      # về chỗ cũ, chờ mọc lại
            else:
                u = (t - t_moc) / MOC_DAI             # mọc lại đúng chỗ: nở từ nhỏ, vượt nhẹ
                if u < 1:
                    kk = hoat.cv(u, [(0, 0.0), (0.6, 1.15, "out"), (1.0, 1.0, "io")])
                    P.scale(b, max(0.02, kk), max(0.02, kk))
                    P.alpha[s] = min(1.0, u / 0.25)
        giu_hinh(P)

    def phinh(t):
        return hoat.cv(t, [(0, 1.0), (T_BOM[0], 1.25, "out"), (0.30, 1.14, "io"), (T_BOM[1], 1.50, "out"), (0.60, 1.40, "io"),
                           (T_BOM[2], PHINH, "out"), (D_SKILL, PHINH)])

    def nay_bom(t):
        w = 0.0
        for i, p in enumerate(T_BOM):
            if t > p:
                u = t - p
                w += (0.045 + 0.018 * i) * math.exp(-u / 0.09) * math.sin(2 * math.pi * u / 0.12)
        return w

    def xu(P, k, lech=0.0):
        """tinh thể xù ra (k > 0) / ép sát (k < 0): dời xương quỹ đạo (khung của bone15 = thế giới) theo hướng từ tâm thân ra tâm hình."""
        for b, (qd, _) in TT.items():
            c, _ = truc[b]
            v = c - tam
            n = float(np.hypot(*v)) or 1.0
            P.move(qd, k * 36.0 * v[0] / n, k * 36.0 * v[1] / n)
            if lech:
                P.rot(b, lech * (1 if v[0] > 0 else -1))

    def run_tt(P, bien):
        if abs(bien) < 1e-4:
            return
        for i, b in enumerate(sorted(TT)):
            P.rot(b, bien * (1 if i % 2 else -1))

    def tt_doi(P, dx, dy):
        for b, (qd, _) in TT.items():
            P.move(qd, dx, dy)

    def f_skill(t, P):
        dat(P, "idle_01", min(t, 0.5), True, mat=False)
        g = phinh(t)
        w = nay_bom(t)
        r = rung(t, 0.55, T_NEN0 + 0.15, 1.0, ra=0.2)
        sx = hoat.cv(t, [(0, 1), (T_NEN0, 1), (1.16, 1.26, "out"), (1.21, 1.26), (T_BAT, 0.62, "in"), (1.32, 0.68), (1.46, 0.94, "out"),
                         (T_DINH0, 1.05), (1.62, 1.09), (T_DINH1, 1.02), (1.80, 0.80, "in"), (D_SKILL, BAY_DANG[0])])
        sy = hoat.cv(t, [(0, 1), (T_NEN0, 1), (1.16, 0.62, "out"), (1.21, 0.62), (T_BAT, 1.62, "in"), (1.32, 1.48), (1.46, 1.08, "out"),
                         (T_DINH0, 0.95), (1.62, 0.91), (T_DINH1, 0.98), (1.80, 1.28, "in"), (D_SKILL, BAY_DANG[1])])
        P.scale("day", g * sx * (1 + w) * (1 + 0.012 * r), g * sy * (1 - w) * (1 - 0.012 * r))
        P.move("xoay", 3.0 * r, hoat.cv(t, [(0, 0), (T_NEN0, 0), (1.16, -16, "out"), (1.21, -16), (T_BAT, 12, "in"), (1.40, 0), (D_SKILL, 0)]))
        # vòng tinh thể quay tít quanh người theo các nhịp bơm (nhanh dần), khoá lúc bật
        P.rot("bone15", -360.0 * hoat.cv(t, [(0, 0), (T_BOM[0], 0.15, "in"), (T_BOM[1], 0.62), (T_BOM[2], 1.52), (T_NEN0, 1.8),
                                             (T_BAT, 2.0, "out"), (D_SKILL, 2.0)]))
        xu(P, hoat.cv(t, [(0, 0), (T_BOM[0], 0.8, "out"), (0.30, 0.15, "io"), (T_BOM[1], 1.1, "out"), (0.60, 0.35, "io"), (T_BOM[2], 1.45, "out"),
                          (T_NEN0, 1.3), (1.16, 0.6), (T_BAT, -0.3, "in"), (1.40, 0.4), (T_DINH0, 1.1, "out"), (T_DINH1, 1.1), (1.80, 0.25),
                          (D_SKILL, 0.25)]),
           hoat.cv(t, [(0, 0), (T_BOM[2], 12, "out"), (T_NEN0, 9), (T_BAT, -6), (T_DINH0, 9), (T_DINH1, 6), (D_SKILL, 0)]))
        run_tt(P, 4.5 * rung(t, 0.55, T_NEN0 + 0.15, 1.0, ra=0.2))
        P.rot("bone9", hoat.cv(t, [(0, 0), (T_BOM[2], -8, "out"), (T_BAT, 4), (D_SKILL, 0)]))   # vương miện ngửa lên lúc gồng
        tt_doi(P, 0.0, 48.0 * hoat.cv(t, [(0, 0), (T_DINH1, 0), (D_SKILL, 1.0, "in")]))
        if t > T_DINH0:
            P.rot("xoay", -360.0 * ease((t - T_DINH0) / (T_DINH1 - T_DINH0), "io"))
        P.att["P_yanjing"] = "P_yanjing" if t < 0.52 or 1.56 <= t < 1.70 else "P_biyan"
        giu_hinh(P)

    def f_land(t, P):
        dat(P, "idle_01", 0.5 + t, True, mat=False)
        g = hoat.cv(t, [(0, PHINH), (0.34, PHINH), (0.90, 1.0, "io"), (D_LAND, 1.0)])
        sx = hoat.cv(t, [(0, BAY_DANG[0]), (0.07, 0.72), (T_CHAM, 1.2, "in"), (0.14, 2.00, "out"), (0.27, 1.88), (0.34, 0.84, "io"),
                         (0.41, 1.20, "io"), (0.48, 0.90, "io"), (0.55, 1.10, "io"), (0.62, 0.95, "io"), (0.69, 1.05, "io"), (0.76, 0.98, "io"),
                         (0.86, 1.01, "io"), (D_LAND, 1.0)])
        sy = hoat.cv(t, [(0, BAY_DANG[1]), (0.07, 1.42), (T_CHAM, 0.8, "in"), (0.14, 0.38, "out"), (0.27, 0.44), (0.34, 1.26, "io"),
                         (0.41, 0.84, "io"), (0.48, 1.12, "io"), (0.55, 0.92, "io"), (0.62, 1.06, "io"), (0.69, 0.96, "io"), (0.76, 1.02, "io"),
                         (0.86, 0.99, "io"), (D_LAND, 1.0)])
        P.scale("day", g * sx, g * sy)
        P.move("xoay", 0, hoat.cv(t, [(0, 0), (0.07, 8), (0.14, -24, "out"), (0.27, -18), (0.34, 14, "io"), (0.41, -6, "io"), (0.52, 2, "io"),
                                      (0.62, 0), (D_LAND, 0)]))
        # tinh thể cắm phập xuống quanh người rồi bật về, nảy theo nhịp rung
        xu(P, hoat.cv(t, [(0, 0.25), (T_CHAM, -0.2, "in"), (0.14, 1.9, "out"), (0.27, 1.7), (0.38, 0.2, "io"), (0.46, 0.65, "io"),
                          (0.54, 0.15, "io"), (0.62, 0.38, "io"), (0.72, 0.05, "io"), (0.82, 0), (D_LAND, 0)]),
           hoat.cv(t, [(0, 0), (0.14, 18, "out"), (0.27, 13), (0.38, -6, "io"), (0.52, 3, "io"), (0.64, 0), (D_LAND, 0)]))
        tt_doi(P, 0.0, 48.0 * hoat.cv(t, [(0, 1.0), (T_CHAM, 0.3, "in"), (0.14, 0)])
               - 46.0 * hoat.cv(t, [(0, 0), (T_CHAM, 0), (0.14, 1.0, "out"), (0.27, 0.9), (0.38, 0.0, "io"), (D_LAND, 0)]))
        P.att["P_yanjing"] = "P_biyan" if t < 0.5 else "P_yanjing"
        giu_hinh(P)

    def f_appear(t, P):
        dat(P, "idle_01", t, True, mat=False)
        sc = hoat.cv(t, [(0, 0.2), (0.22, 1.2, "out"), (0.34, 0.92, "io"), (0.46, 1.05, "io"), (0.58, 1.0, "io")])
        P.scale("day", sc, sc * hoat.cv(t, [(0, 1), (0.22, 0.94), (0.34, 1.06), (0.46, 0.98), (0.58, 1.0)]))
        dam(P, ease(t / 0.12), chi=[s["name"] for s in sk.slots if not s["name"].startswith("P_bc_")])
        P.att["P_yanjing"] = "P_biyan" if t < 0.42 else "P_yanjing"
        for i, (b, (qd, s)) in enumerate(sorted(TT.items())):
            c, _ = truc[b]
            v = c - tam
            n = float(np.hypot(*v)) or 1.0
            t0 = 0.10 + 0.04 * i
            u = (t - t0) / 0.30
            k = 1.0 - ease(u, "out") if u < 1 else 0.0
            vuot = -0.08 * math.sin(math.pi * min(1.0, max(0.0, (u - 1.0) / 0.4))) if u > 1 else 0.0
            d = 270.0 * k + 30.0 * vuot
            P.move(qd, d * v[0] / n, d * v[1] / n)
            P.rot(b, 170.0 * k * (1 if i % 2 else -1))
            P.alpha[s] = float(np.clip(u * 3.0, 0.0, 1.0)) if u < 1 else 1.0
        giu_hinh(P)

    ev_cast = [(T_GOM - 0.30, "tu", "")] + [(round(T_BAN0 + j * BAN_CACH, 3), "ban", b) for j, b in enumerate(PHONG)] + \
              [(round(T_HET, 3), "het_ban", ""), (round(T_MOC, 3), "moc", "")]
    clips = [
        Clip("appear", 0.8, f_appear),
        Clip("idle", CD["idle_01"][0], f_idle, loop=True),
        Clip("walk", CD["run_01"][0], f_walk, loop=True),
        Clip("attack", M_ATTACK[-1][0], f_attack, ev=[(T_TONG, "tong", ""), (T_TONG, "trung", "")]),
        Clip("cast", D_CAST, f_cast, ev=ev_cast, trung=T_BAN0),
        Clip("skill", D_SKILL, f_skill, ev=[(T_BAT, "bat", "")], trung=T_BAT),
        Clip("skill_land", D_LAND, f_land, ev=[(T_CHAM, "cham_dat", "")], trung=T_CHAM),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", CD["die_01"][0] + TAN, f_die),
    ]
    return clips


def main(a):
    sk, info = dung()
    ve0 = soi.Ve(sk)
    clips = lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0)
    clips = lam_clip(sk, info, cao)
    print(f"chiều cao {cao:.0f}; cast dài {D_CAST:.2f} s, phóng {T_BAN0:.2f} → {T_HET:.2f}, mọc lại {T_MOC:.2f}")
    ra = os.environ.get("TS_RA") or os.path.join(G.BASE, "rig")
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
        sc = float(a[3]) if len(a) > 3 else 0.6
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
        os.makedirs(ra, exist_ok=True)
        pth = os.path.join(ra, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    xuat.xuat_het(sk, clips, ra, TEN_RIG, "Tinh linh tinh thể sắt dạng 2 (tinh_sat_2): tướng 1 đảo Kim",
                  dang=2, so_dang=2, dung_yen=("cast", "skill", "skill_land"), ma_goc=None, khop_idle=0.2, khong_khop=("skill",),
                  cao=cao, impact=IMPACT, tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.3, tran_mb=0.5, span=SPAN)


if __name__ == "__main__":
    main(sys.argv[1:])
