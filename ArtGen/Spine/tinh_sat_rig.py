# -*- coding: utf-8 -*-
"""Tinh linh tinh thể sắt (tinh_sat; tướng 1 đảo Kim): hình của mình chạy trên ĐÚNG rig của con gốc monster_3346. Ghi chú:
inbox/tinh_sat_ghichu.md. Cách làm như nui_lua_rig.py (skill pokiclash-spine-rig mục 00):
- XƯƠNG: đủ mọi xương của họ (FK thuần, không IK); thêm `move` (cha của mọi thứ: cú lao, cú nhảy) và `day` (đáy thân: tâm phình / bẹp của
  chiêu cuối; cha của `all`).
- MẢNH: mỗi part của họ một ảnh lắp vào NGUYÊN lưới của họ; mắt có ba hình (`eyes`, `biyan` nhắm `> <`, `yun` choáng) đổi theo khung như họ.
  BỎ slot `shadow`. TS_GOC=1: ảnh part GỐC (chỉ để dựng và soi clip trong máy, KHÔNG đưa vào game); không đặt: ảnh của mình ở
  inbox/tinh_sat_1/manh_part/<vùng>.png.
- CHUYỂN ĐỘNG (người dùng 2026-11-15):
    idle = idle_01, walk = run_01, hit = hit_01, die = die_01 + tan (như họ);
    attack = skill_01_1 (lấy đà ngả ra sau rồi quật tới): LAO VÀO TÔNG đối thủ; cả quãng tới của thân dồn vào `move` để sân kéo tới;
    cast   = GỌI TINH THỂ: co tinh thể sát người (skill_02), 8 tinh thể bay lên xếp vòng cung trên đầu, xoay mũi về đối thủ, lần lượt PHÓNG
             (sự kiện `ban`, chuỗi = tên xương; đường bay do code game lo), rồi tinh thể mới mọc lại đúng chỗ;
    skill  = PHÌNH TO cả thân + tinh thể xù ra, nhún, bật lên (kết thúc ở dáng đang bay, sự kiện `bat`; cung nhảy do code game);
    skill_land = rơi DẬP xuống đầu đối thủ (`cham_dat`), bẹp mạnh, RUNG squash stretch tắt dần, xẹp về cỡ thường (như Tí Tách);
    appear = thân bật ra, các tinh thể bay từ ngoài vào ráp quanh người (Claude tự đặt, người dùng chưa dặn).
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tinh_sat_rig.py        → inbox/tinh_sat_1/rig/ (TS_GOC=1: rig_goc/)
    py -3 -I ArtGen/Spine/tinh_sat_rig.py soi <clip> <giây,giây,...|n=12|t0:t1:n> [tỉ lệ]   → soi_<clip>.png (khung lớn nền xám)
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
import tinh_sat as G  # noqa: E402
from hoa_ho_rig import gan_nguyen, ease, tmap, _goc  # noqa: E402

GOC = os.environ.get("TS_GOC") == "1"
TEN_RIG = "tinh_sat_1"
D_PX = float(os.environ.get("TS_DPX", "1.2"))        # pixel ảnh atlas cho mỗi đơn vị rig (con cao ~380 đơn vị)
BO_SLOT = ("shadow",)
MANH = os.path.join(G.BASE, "manh_part")
TAN = 0.45
FPS = 30.0
IMPACT = {"attack": (0.08, 0.45, 0.12), "cast": (0.10, 0.6, 0.14, "#e8eefc44"), "skill": (0.22, 1.2, 0.3, "#ffffffaa")}   # chiêu cuối: khựng, rung, chớp mạnh

# tinh thể bay ở chiêu mana (trái → phải theo chỗ xếp trên đầu) và thứ tự phóng
BAY = ["all11", "all9", "all13", "all8", "all18", "all14", "all10", "all12"]
PHONG = ["all10", "all9", "all8", "all12", "all11", "all14", "all13", "all18"]
DICH = (760.0, 230.0)                                 # điểm (rig, dáng gốc) các mũi tinh thể chĩa vào lúc chờ phóng: thân đối thủ bên phải
CO_DINH = {"all2", "all7", "all19", "all6", "all3", "all20", "all16", "all21", "all22", "all4", "all5"}   # thân, mặt, tay, chân, tinh thể má
MANH_MOI = os.path.join(G.BASE, "manh")             # mảnh "đúng chỗ, đúng cỡ" cắt từ concept đã duyệt (tinh_sat_manh.py)


# ---------------------------------------------------------------- nạp
def nap_goc():
    scan = G.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    return D, I, scan


def ti_le_atlas(D):
    """px ảnh vùng của họ cho mỗi đơn vị rig (đo trên lưới thân)."""
    _, imgs, _ = G.nap("att_goc.json")
    a = next(x for x in D["atts"] if x["slot"] == "body")
    im = imgs[a["region"]]
    U = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
    V = np.array(a["xy"], float).reshape(-1, 2)
    T = np.array(a["tris"]).reshape(-1, 3)

    def dt(P):
        e1, e2 = P[T[:, 1]] - P[T[:, 0]], P[T[:, 2]] - P[T[:, 0]]
        return np.abs(e1[:, 0] * e2[:, 1] - e1[:, 1] * e2[:, 0]).sum() / 2

    return float(math.sqrt(dt(U) / dt(V)))


def gan(sk, slot, anh_ten, att, ten, Wc):
    """nguyên lưới của họ; hình kiểu region (4 đỉnh, không có uv) đổi thành lưới 4 đỉnh một xương."""
    if "uv" in att:
        return gan_nguyen(sk, slot, anh_ten, att, ten, Wc)
    im = sk.images[anh_ten]
    uv, tr = G.luoi(att)                              # uv theo px ảnh vùng GỐC: đổi sang px ảnh của mình
    _, imgs, _ = G.nap("att_goc.json")
    g0 = imgs[att["region"]]
    uv = uv * np.array([im.width / g0.width, im.height / g0.height])
    V = np.array(att["xy"], float).reshape(-1, 2)
    L = luoi.Luoi(uv, tr, len(uv), len(uv), im.width, im.height, ten=slot)
    sk.luoi_gan(slot, anh_ten, L, trongso.cung(L.n, "move"), the_gioi=V)
    b = ten[att["bone"]] if isinstance(att["bone"], int) else att["bone"]
    sk.atts[slot][anh_ten]["verts"] = [[(b, *[float(v) for v in (np.linalg.inv(Wc[b]) @ np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
    return L


def gan_moi(sk, slot, ten_anh, att, ten, Wi):
    """mảnh của mình (manh/<tên>.png, hộp trên concept trong manh/dat.json) thành lưới 4 đỉnh đúng chỗ trên concept: góc ảnh đổi sang thế giới
    rig ở dáng khung 0 idle (concept vẽ đúng khung đó), bám xương của part cũ; part cũ bám nhiều xương thì mỗi góc lấy trọng số của 3 đỉnh
    gần nhất trên lưới cũ (cũng ở dáng idle 0). Điểm gắn tính bằng ma trận idle 0 nên ở dáng idle 0 mảnh nằm đúng chỗ concept."""
    import tinh_sat_manh as TM
    D = json.load(open(os.path.join(MANH_MOI, "dat.json")))
    x0, y0, x1, y1 = D[ten_anh]["hop"]
    s_px, _, to_rig = TM.tf()
    g = Image.open(os.path.join(MANH_MOI, ten_anh + ".png")).convert("RGBA")
    kq = D_PX / s_px
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    sk.anh(ten_anh, anh.loang_mau(g))
    im = sk.images[ten_anh]
    goc_px = np.array([[x0, y1], [x0, y0], [x1, y0], [x1, y1]], float)      # trái dưới, trái trên, phải trên, phải dưới
    V = to_rig(goc_px)
    uv = np.array([[0, im.height], [0, 0], [im.width, 0], [im.width, im.height]], float)
    L = luoi.Luoi(uv, np.array([[0, 1, 2], [2, 3, 0]]), 4, 4, im.width, im.height, ten=slot)
    if att.get("w"):
        Q = np.array(att["xy"], float).reshape(-1, 2)
        rows_w = []
        for p in V:
            d = np.hypot(*(Q - p).T)
            k = np.argsort(d)[:3]
            ww = 1.0 / np.maximum(d[k], 1.0) ** 2
            acc = {}
            for j, wj in zip(k, ww / ww.sum()):
                for b, w in att["w"][j]:
                    acc[ten[b]] = acc.get(ten[b], 0.0) + wj * w
            tot = sum(acc.values())
            rows_w.append({b: w / tot for b, w in acc.items() if w / tot > 0.01})
    else:
        b = ten[att["bone"]] if isinstance(att["bone"], int) else att["bone"]
        rows_w = [{b: 1.0}] * 4
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
    sk.luoi_gan(slot, ten_anh, L, trongso.cung(L.n, "move"), the_gioi=np.array(Vs))
    sk.atts[slot][ten_anh]["verts"] = rows
    return L


def anh_part(a, a_tl):
    r = a["region"]
    pth = os.path.join(MANH, r + ".png")
    if GOC:
        g = G.part_goc(a)
        kq = (a_tl if GOC else D_PX) / a_tl
    elif os.path.exists(pth):
        import tinh_sat_da as M
        g = Image.open(pth).convert("RGBA")
        kq = D_PX / (a_tl * M.zs()[r])
    else:
        raise SystemExit("thiếu ảnh part " + pth + " (TS_GOC=1: da gốc)")
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g)


def dung():
    D, I, scan = nap_goc()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    assert ten == [b["name"] for b in D["bones"]]
    a_tl = ti_le_atlas(D)
    sk = khung.Sk(TEN_RIG)
    sk.xuong("root")
    sk.xuong("move", "root")
    Wc = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]]) for b in D["bones"]}
    by = {}
    for a in D["atts"]:
        by.setdefault(a["slot"], []).append(a)
    Vb = np.array(next(a for a in by["body"] if a["cur"])["xy"], float).reshape(-1, 2)
    y_day = float(Vb[:, 1].min())                     # đáy thân ở dáng gốc
    tam = Vb.mean(0)
    sk.xuong("day", "move", float(tam[0]), y_day)
    goc0 = {}
    for b in IB:
        if b["name"] == "root":
            continue
        cha = ten[b["parent"]]
        g = [b["x"], b["y"], b["rot"], b["sx"], b["sy"]]
        goc0[b["name"]] = g
        if cha == "root":
            par = "day" if b["name"] == "all" else "move"
            ox, oy = (float(tam[0]), y_day) if par == "day" else (0.0, 0.0)
            sk.xuong(b["name"], par, g[0] - ox, g[1] - oy, goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
        else:
            sk.xuong(b["name"], cha, g[0], g[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
    slots = [s["name"] for s in I["slots"] if s["name"] not in BO_SLOT and s["name"] in by]
    if not GOC:                                       # tay trái của mình là cục u nấp sau thân (như concept), không đè trước thân như họ
        slots.remove("zuoshou")
        slots.insert(slots.index("body"), "zuoshou")
    tong = [0, 0]
    truc = {}                                        # trục chính từng tinh thể (dáng gốc): (tâm, góc của đầu mũi)
    D0 = json.load(open(os.path.join(scan, "att_idle0.json"), encoding="utf-8"))
    Wi = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]]) for b in D0["bones"]}
    by0 = {(a["slot"], a["region"]): a for a in D0["atts"]}
    for s in slots:
        cur = [a for a in by[s] if a["cur"]] or by[s][:1]
        sk.slot(s, "move", cur[0]["region"])
        for a in sorted(by[s], key=lambda q: not q["cur"]):
            r = a["region"]
            if not GOC:                                  # mảnh của mình: đặt theo concept (dáng idle 0), trọng số theo lưới cũ ở idle 0
                a0 = by0.get((s, r))
                if a0 is None:                           # hình không bật ở idle 0 (mắt nhắm, choáng): lấy đúng hình mắt mở ở idle 0
                    a0 = dict(by0[(s, cur[0]["region"])])
                L = gan_moi(sk, s, r, a0, ten, Wi)
                tong[0] += L.n
                tong[1] += len(L.tris)
                continue
            if r not in sk.images:
                sk.anh(r, anh_part(a, a_tl))
            L = gan(sk, s, r, a, ten, Wc)
            tong[0] += L.n
            tong[1] += len(L.tris)
        V = np.array(cur[0]["xy"], float).reshape(-1, 2)
        c = V.mean(0)
        _, _, vt = np.linalg.svd(V - c)
        ax = vt[0]
        pr = (V - c) @ ax
        if abs(pr.max()) < abs(pr.min()):            # đầu mũi = đầu xa tâm hình hơn
            ax = -ax
        if np.dot(ax, c - tam) < 0 and abs(abs(pr.max()) - abs(pr.min())) < 6:
            ax = -ax                                 # hai đầu gần đều: lấy đầu chĩa ra ngoài thân
        xb = cur[0]["bone"]
        truc[ten[xb] if isinstance(xb, int) else xb] = (c, math.degrees(math.atan2(ax[1], ax[0])))
    for e, m in (("trung", "khung trúng"), ("tong", "attack: thân tông vào đối thủ"), ("tu", "cast: gọi tinh thể (co sát người)"),
                 ("ban", "cast: một tinh thể phóng đi (chuỗi = tên xương; ẩn trong rig, code game cho bay)"), ("het_ban", "cast: hết loạt phóng"),
                 ("moc", "cast: tinh thể mới mọc lại"), ("bat", "skill: rời đất (cung nhảy do code)"), ("cham_dat", "skill_land: dập xuống")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác (lưới của họ); atlas của họ {a_tl:.3f} px / đơn vị; "
          f"đáy thân y = {y_day:.1f}, tâm thân ({tam[0]:.1f}, {tam[1]:.1f})")
    return sk, dict(scan=scan, IB=IB, ten=ten, goc0=goc0, slots=[s["name"] for s in I["slots"]], y_day=y_day, tam=tam, truc=truc, Wc=Wc)


# ---------------------------------------------------------------- chuyển động
def chuyen_dong(sk, info):
    S = json.load(open(os.path.join(info["scan"], "sample_goc.json"), encoding="utf-8"))
    IB, ten, goc0 = info["IB"], info["ten"], info["goc0"]
    ids = [i for i, n in enumerate(ten) if n in sk.bi and n != "root"]
    i_mat = info["slots"].index("eyes")
    out = {}
    ref = None
    for clip in ["idle_01"] + [c for c in S if c != "idle_01"]:
        fr = S[clip]["frames"]
        L = np.array([F["l"] for F in fr], float)                     # (khung, xương, 7): x, y, xoay, tỉ lệ x, y, xô
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
        mat = [F["n"][i_mat] or "eyes" for F in fr]
        out[clip] = (float(S[clip]["dur"]), res, len(fr), mat)
    return out


# giờ của mình → giờ clip nguồn
# attack: lấy đà (0 → 13 khung của họ) chậm hơn chút, quật tới (khung 13 → 15) đúng lúc tông, nảy về
T_TONG = 0.52
M_ATTACK = [(0.0, 0.0), (0.42, 13 / 30.0, "io"), (T_TONG, 15.5 / 30.0, "in"), (0.66, 18 / 30.0, "out"), (1.0, 23 / 30.0, "io")]
# cast
T_GOM = 0.30
T_LEN = 0.26                                          # tinh thể đầu bắt đầu bay lên
LEN_CACH, LEN_DAI = 0.035, 0.32
T_BAN0, BAN_CACH = 0.98, 0.075
T_HET = T_BAN0 + (len(PHONG) - 1) * BAN_CACH + 0.06
T_MOC = T_HET + 0.12
MOC_CACH, MOC_DAI = 0.03, 0.26
D_CAST = T_MOC + (len(BAY) - 1) * MOC_CACH + MOC_DAI + 0.22
M_CAST = [(0.0, 0.0), (T_GOM, 10 / 30.0, "io"), (T_HET, 15 / 30.0, "lin"), (D_CAST, 36 / 30.0, "io")]
# chiêu cuối (bản 2, người dùng 2026-11-15: "chưa đủ ấn tượng" → làm đủ ba pha Claude gợi ý):
# skill: GỒNG ba nhịp bơm phồng (đỉnh 0,18 / 0,48 / 0,85; nhịp cuối 1,66 lần, tinh thể khoá chĩa ra thành quả cầu gai, run), nhún sâu
#        (0,98 → 1,21), BẬT (bat 1,24), bay lên duỗi dài, KHỰNG ở đỉnh + LỘN một vòng (1,50 → 1,74; game bay cung từ bat tới cham_dat nên đỉnh
#        cung rơi đúng quãng này), cắm xuống: thân vươn dọc, tinh thể dồn ngược lên như đuôi sao chổi (kết thúc ở dáng đang rơi);
# skill_land: rơi nốt 3 khung → DẬP (cham_dat 0,10) bẹp thành bánh, tinh thể cắm phập xuống quanh người rồi bật về → RUNG squash stretch
#        4 nhịp tắt dần trong lúc xì hơi về cỡ thường.
PHINH = 1.66
T_BOM = (0.18, 0.48, 0.85)
T_NEN0, T_BAT = 0.98, 1.24
T_DINH0, T_DINH1 = 1.50, 1.74
D_SKILL = 1.86
BAY_DANG = (0.74, 1.36)
T_CHAM, D_LAND = 3 / 30.0, 1.15
SPAN = 4.4                                            # khung vẽ sticker (chiều cao): lúc bẹp thành bánh con rộng ~3,6 lần chiều cao


def lam_clip(sk, info, cao=380.0):
    CD = chuyen_dong(sk, info)
    truc, tam, Wc = info["truc"], info["tam"], info["Wc"]

    def dat(P, goc, tau, lap=False, mat=True):
        dur, R, n, M = CD[goc]
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
        if mat:
            P.att["eyes"] = M[min(n - 1, int(round(x)))]

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

    slot_cua = {}
    for s in sk.slots:
        slot_cua.setdefault(s["bone"], s["name"])
    # slot bám xương nào: lưới của họ ghi trọng số theo xương, slot nằm trên `move`; tra theo xương nặng nhất của hình mặc định
    for s in sk.slots:
        att = sk.atts[s["name"]].get(s["att"])
        if att and att.get("verts"):
            nang = {}
            for row in att["verts"]:
                for b, _, _, w in row:
                    nang[b] = nang.get(b, 0.0) + w
            slot_cua[max(nang, key=nang.get)] = s["name"]

    def dat_tg(P, b, xy, goc_tg, k=1.0):
        """đặt xương b (trong tư thế P hiện có) tới chỗ xy, góc goc_tg THẾ GIỚI; k = mức hoà 0..1 với dáng đang có."""
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

    # ---- chỗ xếp trên đầu (cast): vòng cung ôm quanh đầu (elip quanh tâm thân), mũi chĩa về DICH
    CHO = {}
    for i, b in enumerate(BAY):
        a = math.radians(162.0 - 144.0 * i / (len(BAY) - 1))
        x = float(tam[0] + 250.0 * math.cos(a))
        y = float(tam[1] + 45.0 + 205.0 * math.sin(a))
        CHO[b] = (x, y, math.degrees(math.atan2(DICH[1] - y, DICH[0] - x)))

    def pha(Pa, Pb, w):
        """tư thế hoà: (1 − w)·Pa + w·Pb (dời, xoay cộng; tỉ lệ nội suy); hình mắt theo bên nặng hơn."""
        Q = khung.Pose()
        for b in set(Pa.t) | set(Pb.t):
            a_ = Pa.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            b_ = Pb.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            Q.t[b] = [a_[q] + (b_[q] - a_[q]) * w for q in range(5)]
        Q.alpha = dict(Pa.alpha)
        Q.att = dict(Pb.att if w > 0.5 else Pa.att)
        return Q

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

    x0_all2 = CD["skill_01_1"][1]["all2"][0, 1]

    def f_attack(t, P):
        dat(P, "skill_01_1", tmap(t, M_ATTACK))
        # LAO VÀO TÔNG (người dùng): quãng tới của thân (all2) dồn hết sang `move` rồi nới thêm: đỉnh lao 0,62 chiều cao ở đúng khung tông;
        # sân nắn đỉnh lao này tới 72 % quãng tới đối thủ (AolaSticker.Lunge)
        g = P._g("all2")
        dx = g[0] - x0_all2
        g[0] -= dx
        tien = max(0.0, dx)
        lao = 0.0
        t_ve = T_TONG + 0.12
        if t < T_TONG - 0.10:
            lao = -0.05 * ease(t / (T_TONG - 0.10))
        elif t < T_TONG:
            lao = -0.05 + 0.67 * ease((t - (T_TONG - 0.10)) / 0.10, "in")
        elif t < t_ve:
            lao = 0.62
        else:
            lao = 0.62 * (1 - ease((t - t_ve) / max(0.05, M_ATTACK[-1][0] - 0.06 - t_ve)))
        P.move("move", cao * lao + min(tien, 40.0) * 0.0 + rung(t, T_TONG + 0.02, T_TONG + 0.18, 5.0) + (dx if dx < 0 else 0.0), 0.0)
        k = math.exp(-((t - (T_TONG + 0.02)) / 0.05) ** 2)
        P.scale("day", 1 - 0.16 * k, 1 + 0.12 * k)                     # bẹp theo chiều tông đúng khung chạm

    def f_cast(t, P):
        if t <= T_GOM:
            dat(P, "skill_02", tmap(t, M_CAST))
        else:                                         # giữ dáng co của skill_02 (khung 10) rồi hoà dần về idle tới lúc mọc lại xong
            Pa, Pb = khung.Pose(), khung.Pose()
            dat(Pa, "skill_02", 10 / 30.0)
            dat(Pb, "idle_01", t - T_GOM, True)
            w = ease((t - T_GOM) / (D_CAST - 0.15 - T_GOM))
            Q = pha(Pa, Pb, 0.35 * ease((t - T_GOM) / 0.4) + 0.65 * w)
            P.t.update(Q.t)
            P.att.update(Q.att)
        if T_GOM - 0.04 < t < T_HET + 0.25:
            P.att["eyes"] = "eyes"                    # mắt mở quả quyết lúc điều khiển tinh thể
        if t > T_GOM - 0.05:
            nh = hoat.bao(t, T_GOM - 0.05, D_CAST - 0.1, 0.25, 0.35)
            P.move("all2", 0.0, 14.0 * nh + 3.0 * math.sin(t * 9.0) * nh)
        # mỗi lần phóng thân giật nhẹ
        for i in range(len(PHONG)):
            u = t - (T_BAN0 + i * BAN_CACH)
            if 0 <= u < 0.12:
                k = math.sin(math.pi * u / 0.12)
                P.scale("day", 1 + 0.035 * k, 1 - 0.03 * k)
        base = P.copy()
        for i, b in enumerate(BAY):
            j = PHONG.index(b)
            t_ban = T_BAN0 + j * BAN_CACH
            t_moc = T_MOC + i * MOC_CACH
            s = slot_cua.get(b)
            if t < t_ban:
                u = (t - (T_LEN + i * LEN_CACH)) / LEN_DAI
                if u <= 0:
                    continue
                k = ease(u, "io")
                x, y, g = CHO[b]
                # nhấp nhô lúc chờ, lấy đà lùi theo trục ngay trước khi phóng
                bob = 5.0 * math.sin(t * 7.0 + i) * min(1.0, max(0.0, u - 1.0) * 3)
                lui = 22.0 * ease((t - (t_ban - 0.08)) / 0.08, "out") if t > t_ban - 0.08 else 0.0
                gr = math.radians(g)
                c0, a0 = truc[b]
                # chỗ là TÂM hình tinh thể: đổi sang gốc xương (tâm hình lệch gốc xương ở dáng gốc)
                W0 = Wc[b]
                off = np.linalg.solve(W0, np.array([c0[0], c0[1], 1.0]))[:2]
                quay = g - a0
                ca, sa = math.cos(math.radians(quay)), math.sin(math.radians(quay))
                bx = x - lui * math.cos(gr) - (ca * off[0] - sa * off[1])
                by = y - lui * math.sin(gr) + bob - (sa * off[0] + ca * off[1])
                if u < 1:                                 # giữa đường bay: hoà từ chỗ đang có, xoay dần
                    p0, r0 = tg_xuong(base, b)
                    xy = (p0[0] + (bx - p0[0]) * k, p0[1] + (by - p0[1]) * k + 60.0 * math.sin(math.pi * k))
                    dat_tg(P, b, xy, r0 + ((quay + _goc(W0) - r0 + 180) % 360 - 180) * k)
                else:
                    dat_tg(P, b, (bx, by), quay + _goc(W0))
                P.scale(b, 1.0 + 0.12 * math.sin(math.pi * min(1.0, u)), 1.0 + 0.12 * math.sin(math.pi * min(1.0, u)))
            elif t < t_moc:
                if s:
                    P.alpha[s] = 0.0                      # đã phóng: code game cho bay, trong rig ẩn
            else:
                u = (t - t_moc) / MOC_DAI                 # mọc lại đúng chỗ: nở từ nhỏ, vượt nhẹ
                if u < 1 and s:
                    k = hoat.cv(u, [(0, 0.0), (0.6, 1.15, "out"), (1.0, 1.0, "io")])
                    P.scale(b, max(0.02, k), max(0.02, k))
                    P.alpha[s] = min(1.0, u / 0.25)

    def phinh(t):
        """ba nhịp bơm: phồng vọt (ra nhanh) rồi xẹp lại chút, nhịp sau to hơn; nhịp cuối giữ."""
        return hoat.cv(t, [(0, 1.0), (T_BOM[0], 1.22, "out"), (0.30, 1.12, "io"), (T_BOM[1], 1.42, "out"), (0.60, 1.33, "io"),
                           (T_BOM[2], PHINH, "out"), (D_SKILL, PHINH)])

    def nay_bom(t):
        """rung thạch sau mỗi nhịp bơm (dao động tắt nhanh, chu kỳ 0,12 s)."""
        w = 0.0
        for i, p in enumerate(T_BOM):
            if t > p:
                u = t - p
                w += (0.04 + 0.015 * i) * math.exp(-u / 0.09) * math.sin(2 * math.pi * u / 0.12)
        return w

    def run_tt(P, bien):
        """tinh thể run bần bật (mỗi tinh thể một chiều, đổi chiều mỗi 2 khung)."""
        if abs(bien) < 1e-4:
            return
        for i, b in enumerate(sorted(truc)):
            if b not in CO_DINH:
                P.rot(b, bien * (1 if i % 2 else -1))

    def tt_doi(P, dx, dy):
        for b in truc:
            if b not in CO_DINH:
                P.move(b, dx, dy)

    def xu(P, k, lech=0.0):
        """tinh thể xù ra khỏi thân (k > 0) hoặc ép sát (k < 0): dời mỗi tinh thể theo hướng từ tâm thân ra tâm hình nó."""
        for b, (c, _) in truc.items():
            if b in CO_DINH:
                continue
            v = c - tam
            n = float(np.hypot(*v)) or 1.0
            P.move(b, k * 34.0 * v[0] / n, k * 34.0 * v[1] / n)
            if lech:
                P.rot(b, lech * (1 if v[0] > 0 else -1))

    def f_skill(t, P):
        dat(P, "idle_01", min(t, 0.5), True, mat=False)
        g = phinh(t)
        w = nay_bom(t)
        r = rung(t, 0.55, T_NEN0 + 0.15, 1.0, ra=0.2)                  # run vì nén sức (nhịp 2 → lúc nhún)
        sx = hoat.cv(t, [(0, 1), (T_NEN0, 1), (1.16, 1.24, "out"), (1.21, 1.24), (T_BAT, 0.62, "in"), (1.32, 0.68), (1.46, 0.94, "out"),
                         (T_DINH0, 1.05), (1.62, 1.09), (T_DINH1, 1.02), (1.80, 0.80, "in"), (D_SKILL, BAY_DANG[0])])
        sy = hoat.cv(t, [(0, 1), (T_NEN0, 1), (1.16, 0.64, "out"), (1.21, 0.64), (T_BAT, 1.62, "in"), (1.32, 1.48), (1.46, 1.08, "out"),
                         (T_DINH0, 0.95), (1.62, 0.91), (T_DINH1, 0.98), (1.80, 1.28, "in"), (D_SKILL, BAY_DANG[1])])
        P.scale("day", g * sx * (1 + w) * (1 + 0.012 * r), g * sy * (1 - w) * (1 - 0.012 * r))
        P.move("all2", 3.0 * r, hoat.cv(t, [(0, 0), (T_NEN0, 0), (1.16, -18, "out"), (1.21, -18), (T_BAT, 14, "in"), (1.40, 0), (D_SKILL, 0)]))
        # tinh thể: xoè theo từng nhịp bơm, khoá chĩa ra ở nhịp cuối (quả cầu gai), ép lại lúc bật, xoè lúc khựng trên đỉnh
        xu(P, hoat.cv(t, [(0, 0), (T_BOM[0], 0.75, "out"), (0.30, 0.1, "io"), (T_BOM[1], 1.0, "out"), (0.60, 0.3, "io"), (T_BOM[2], 1.3, "out"),
                          (T_NEN0, 1.18), (1.16, 0.6), (T_BAT, -0.3, "in"), (1.40, 0.4), (T_DINH0, 1.0, "out"), (T_DINH1, 1.0), (1.80, 0.25),
                          (D_SKILL, 0.25)]),
           hoat.cv(t, [(0, 0), (T_BOM[2], 10, "out"), (T_NEN0, 8), (T_BAT, -6), (T_DINH0, 8), (T_DINH1, 6), (D_SKILL, 0)]))
        run_tt(P, 4.0 * rung(t, 0.55, T_NEN0 + 0.15, 1.0, ra=0.2))
        # lúc cắm xuống: tinh thể dồn ngược lên phía trên như đuôi sao chổi
        tt_doi(P, 0.0, 46.0 * hoat.cv(t, [(0, 0), (T_DINH1, 0), (D_SKILL, 1.0, "in")]))
        # khựng ở đỉnh cung + lộn một vòng (quay quanh tâm thân, tinh thể quay theo)
        if t > T_DINH0:
            P.rot("all2", -360.0 * ease((t - T_DINH0) / (T_DINH1 - T_DINH0), "io"))
        P.att["eyes"] = "eyes" if t < 0.52 or 1.56 <= t < 1.70 else "biyan"

    def f_land(t, P):
        dat(P, "idle_01", 0.5 + t, True, mat=False)
        g = hoat.cv(t, [(0, PHINH), (0.30, PHINH), (0.80, 1.0, "io"), (D_LAND, 1.0)])               # xì hơi về cỡ thường sau cú dập
        # rơi nốt → DẬP bẹp thành bánh → RUNG squash stretch 4 nhịp tắt dần (chu kỳ ~0,14 s) → về
        sx = hoat.cv(t, [(0, BAY_DANG[0]), (0.07, 0.72), (T_CHAM, 1.2, "in"), (0.14, 1.86, "out"), (0.26, 1.76), (0.33, 0.86, "io"),
                         (0.40, 1.16, "io"), (0.47, 0.92, "io"), (0.54, 1.08, "io"), (0.61, 0.96, "io"), (0.68, 1.03, "io"), (0.78, 0.99, "io"),
                         (D_LAND, 1.0)])
        sy = hoat.cv(t, [(0, BAY_DANG[1]), (0.07, 1.42), (T_CHAM, 0.8, "in"), (0.14, 0.42, "out"), (0.26, 0.48), (0.33, 1.22, "io"),
                         (0.40, 0.86, "io"), (0.47, 1.10, "io"), (0.54, 0.93, "io"), (0.61, 1.05, "io"), (0.68, 0.97, "io"), (0.78, 1.01, "io"),
                         (D_LAND, 1.0)])
        P.scale("day", g * sx, g * sy)
        # dập xuống: cả con hạ thấp cho đáy thân chạm chỗ đáp (con bay lơ lửng cao hơn gốc), rồi nổi lên lại
        P.move("move", 0, -info["y_day"] * hoat.cv(t, [(0, 0.6), (T_CHAM, 1.0, "in"), (0.30, 1.0), (0.60, 0.3, "io"), (0.85, 0.0, "io"),
                                                        (D_LAND, 0.0)]))
        P.move("all2", 0, hoat.cv(t, [(0, 0), (0.07, 8), (0.14, -26, "out"), (0.26, -20), (0.33, 14, "io"), (0.40, -6, "io"), (0.50, 2, "io"),
                                      (0.60, 0), (D_LAND, 0)]))
        # tinh thể cắm phập xuống quanh người rồi bật về, nảy theo nhịp rung
        xu(P, hoat.cv(t, [(0, 0.25), (T_CHAM, -0.2, "in"), (0.14, 1.7, "out"), (0.26, 1.5), (0.36, 0.2, "io"), (0.44, 0.6, "io"),
                          (0.52, 0.15, "io"), (0.60, 0.35, "io"), (0.70, 0.05, "io"), (0.80, 0), (D_LAND, 0)]),
           hoat.cv(t, [(0, 0), (0.14, 16, "out"), (0.26, 12), (0.36, -6, "io"), (0.50, 3, "io"), (0.62, 0), (D_LAND, 0)]))
        tt_doi(P, 0.0, 46.0 * hoat.cv(t, [(0, 1.0), (T_CHAM, 0.3, "in"), (0.14, 0)])
               - 40.0 * hoat.cv(t, [(0, 0), (T_CHAM, 0), (0.14, 1.0, "out"), (0.26, 0.9), (0.36, 0.0, "io"), (D_LAND, 0)]))
        P.att["eyes"] = "biyan" if t < 0.5 else "eyes"

    def f_appear(t, P):
        dat(P, "idle_01", t, True, mat=False)
        sc = hoat.cv(t, [(0, 0.2), (0.22, 1.18, "out"), (0.34, 0.92, "io"), (0.46, 1.05, "io"), (0.58, 1.0, "io")])
        P.scale("day", sc, sc * hoat.cv(t, [(0, 1), (0.22, 0.94), (0.34, 1.06), (0.46, 0.98), (0.58, 1.0)]))
        dam(P, ease(t / 0.12), chi=("body", "eyes", "mt", "youshou", "zuoshou", "youjiao", "zuojiao", "bin4", "bin5"))
        P.att["eyes"] = "biyan" if t < 0.42 else "eyes"
        thu = [b for b in truc if b not in CO_DINH]
        for i, b in enumerate(sorted(thu)):
            c, _ = truc[b]
            v = c - tam
            n = float(np.hypot(*v)) or 1.0
            t0 = 0.10 + 0.035 * i
            u = (t - t0) / 0.30
            k = 1.0 - ease(u, "out") if u < 1 else 0.0
            vuot = -0.08 * math.sin(math.pi * min(1.0, max(0.0, (u - 1.0) / 0.4))) if u > 1 else 0.0
            d = 260.0 * k + 30.0 * vuot
            P.move(b, d * v[0] / n, d * v[1] / n)
            P.rot(b, 160.0 * k * (1 if i % 2 else -1))
            s = slot_cua.get(b)
            if s:
                P.alpha[s] = float(np.clip(u * 3.0, 0.0, 1.0)) if u < 1 else 1.0

    ev_cast = [(T_GOM - 0.25, "tu", "")] + [(round(T_BAN0 + j * BAN_CACH, 3), "ban", b) for j, b in enumerate(PHONG)] + \
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
    ra = os.environ.get("TS_RA") or os.path.join(G.BASE, "rig_goc" if GOC else "rig")
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
    xuat.xuat_het(sk, clips, ra, TEN_RIG, "Tinh linh tinh thể sắt (tinh_sat): tướng 1 đảo Kim" + (" — DA GỐC, chỉ để soi clip" if GOC else ""),
                  dang=1, so_dang=1, dung_yen=("cast", "skill", "skill_land"), ma_goc=None, khop_idle=0.2, khong_khop=("skill",),
                  cao=cao, impact=IMPACT, tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.3, tran_mb=0.5, span=SPAN)


if __name__ == "__main__":
    main(sys.argv[1:])
