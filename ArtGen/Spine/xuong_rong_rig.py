# -*- coding: utf-8 -*-
"""Xương rồng tròn (xuong_rong, tướng đầu tiên đảo Mộc), dạng 1: hình của mình chạy trên ĐÚNG rig của con gốc monster_3229.
Ghi chú: inbox/xuong_rong_ghichu.md. Cách làm như rong_vay_rig.py (skill pokiclash-spine-rig mục 00):
- XƯƠNG: đủ mọi xương của họ (trừ xương bóng), đúng cha – con, đúng biến đổi riêng ở dáng gốc; thêm `move` (game đo cú lao), `mieng`
  (chỗ nhả của chiêu), `u_dat` (ụ đất của appear).
- MẢNH: mỗi part một ảnh vẽ đúng khung ảnh vùng của part (xuong_rong.py cat_part), lắp vào NGUYÊN lưới của họ (đỉnh, tam giác, uv,
  trọng số). Vành hoa mang hình bóng của mình nên dùng lưới riêng, mỗi đỉnh biến dạng như điểm tương ứng trên lưới mào của họ. Vành
  môi = da thân nướng vào khung vành môi (xuong_rong.py moi): không thấy môi. Mỗi gai có thêm hai hình "gai vừa", "gai dài": lúc gai
  phóng dài thì ĐỔI HÌNH thay vì kéo giãn ảnh gai ngắn. Tay sau có bản sao ở lớp trước thân (lúc gồng hai nắm tay chụm vào giữa).
- CHUYỂN ĐỘNG: clip dựng ở tầng điều khiển của rig gốc (xuong_rong_clip.py), runtime Spine thật nướng ra scan/sample_moi.json (biến
  đổi riêng đã áp: IK chân đã thành FK) → lệch so với dáng gốc cho mọi xương. Ẩn slot, thứ tự vẽ đọc ở trường n, o của mẫu.
- APPEAR trồi từ đất: mặt nạ cắt ở mặt đất (luôn bật), ụ đất vẽ trước cùng, cả con dời dọc trên xương `move`.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/xuong_rong_rig.py        → inbox/xuong_rong_1/rig/
    py -3 -I ArtGen/Spine/xuong_rong_rig.py soi <clip> <giây,giây,...> [tỉ lệ] [luoi]          → rig/soi_<clip>.png (khung lớn nền xám)
"""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, luoi, trongso, khung, hoat, xuat, soi, tienhoa  # noqa: E402
from quai.khung import Dat  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import xuong_rong as XR  # noqa: E402
import xuong_rong_clip as RC  # noqa: E402

RA = os.environ.get("XR_RA")
# DẠNG 2 (người dùng 2026-11-12: "dạng 2 sẽ to hơn chiến hơn chút nhưng form người vẫn vậy"): CÙNG rig, cùng lưới, cùng clip; đổi tỉ lệ
# dáng gốc của vài xương (xương con thừa hưởng) và vẽ lại da trong cùng khung part. Tỉ lệ (dọc xương, ngang): gai thân dài và to
# hơn, hai nắm tay to hơn (gai nắm tay theo), cánh hoa lớn hơn. To hơn cả con là việc của `size` trong heroes.json.
TI_LE_K = {1: {},
           2: {**{b: (1.45, 1.15) for b in ("bone21", "bone22", "bone23", "bone24", "bone25")},
               "bone15": (1.18, 1.18), "bone18": (1.18, 1.18),
               **{b: (1.22, 1.08) for b in ("bone26", "bone27", "bone28", "bone32", "bone33", "bone34")},
               **{b: (1.28, 1.28) for b in ("bone29", "bone30", "bone31")}}}
KG = 1.0                     # đơn vị rig con gốc → đơn vị rig của mình
D_PX = 2.0                   # pixel ảnh atlas cho mỗi đơn vị rig
BO_TEN = ("shadow",)
S_TAY_SAU = RC.S_TAY_SAU     # slot tay sau: có bản sao "truoc_<tên>" vẽ trước thân
GAI = XR.GAI_THAN + XR.GAI_TAY
# clip game ← clip dựng ở tầng điều khiển (xuong_rong_clip.py), lặp?, giờ trúng / nhả cho game (None: lấy theo sự kiện)
CLIPS = [("appear", "xr_appear", False, None), ("idle", "xr_idle", True, None), ("walk", "xr_walk", True, None),
         ("attack", "xr_attack", False, None), ("cast", "xr_cast", False, None), ("skill", "xr_skill", False, RC.S_BAT),
         ("skill_land", "xr_skill_land", False, RC.L_CHAM), ("hit", "xr_hit", False, None), ("die", "xr_die", False, None)]
VE_NGHI = ("appear", "attack", "cast", "skill_land", "hit")       # clip hết ở dáng nghỉ: hoà 0,2 s cuối về khung 0 idle
MAT_SAU = 3000.0             # mặt nạ đất nằm sâu chừng này ngoài clip appear
TAN = 0.45                   # die: giữ dáng cuối rồi mờ dần chừng này giây
# chiều cao game (game.height, game co mỗi dạng về cùng chiều cao rồi nhân `size`) đo trên THÂN: không tính vành hoa và gai. Tính cả
# hoa thì dạng 2 (hoa cao, gai dài) bị co nhỏ thân lại, hết "to hơn"; cũng nhờ vậy dạng 2 trong rig gộp tiến hóa không phải co.
# cảm giác trúng (khựng giây, rung trauma, bật lùi × chiều cao[, chớp màn]) theo dạng. Người dùng 2026-11-12: chiêu cuối "impact hơi
# nhẹ" → khựng và rung gần mức trần (sân khựng tối đa 0,2 s, trauma tối đa 1), đối thủ bật lùi mạnh; dạng 2 thêm chớp màn nhạt
IMPACT_K = {1: {"attack": (0.05, 0.26, 0.07), "skill": (0.17, 0.92, 0.14)},
            2: {"attack": (0.06, 0.32, 0.08), "skill": (0.20, 1.0, 0.16, "#fff6c966")}}
BO_CAO = ("P_toufa",) + tuple(GAI) + tuple("truoc_" + s_ for s_ in GAI)
TI_GAI = (1.45, 2.8)         # tỉ lệ dài/ngang của xương gai: dưới 1,45 gai ngắn, dưới 2,8 gai vừa, trên nữa gai dài


def nap_goc():
    scan = XR.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    return D, I, scan


def tim_part(ten, k):
    """(đường dẫn ảnh part, tỉ lệ phóng của tờ chứa nó, độ nới khung px trên tờ): tìm ở dạng k trước, thiếu thì lấy của dạng 1 (gai,
    gai dài, ụ đất dùng chung). XR_MANH (thư mục mảnh thử) đè lên tất cả."""
    thu = [(os.environ["XR_MANH"], 1)] if os.environ.get("XR_MANH") else [(XR.manh_dir(kk), kk) for kk in dict.fromkeys((k, 1))]
    for goc, kk in thu:
        for thu_muc in ("part_moi", "part"):
            pth = os.path.join(goc, thu_muc, ten + ".png")
            if os.path.exists(pth):
                z = {t: z_ for to, (z_, ds) in XR.TO_K[kk].items() for t in ds}[ten]
                return pth, z, XR.DEM_K[kk].get(ten, 0)
    raise SystemExit(f"thiếu ảnh part {ten} (dạng {k})")


def anh_part(ten, k, nhe=1.0):
    """ảnh part của mình (cỡ ô trên tờ, × z) → cỡ atlas (D_PX px mỗi đơn vị rig; ảnh vùng của họ là 0,75 px mỗi đơn vị). Trả (ảnh,
    độ nới khung tính bằng px ảnh atlas)."""
    pth, z, dem = tim_part(ten, k)
    g = Image.open(pth).convert("RGBA")
    kq = D_PX * nhe / (0.75 * z)
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g), dem * kq


def gan_cung(sk, slot, anh_ten, att, ten, Wc, dem):
    """part CỨNG vẽ trong ô NỚI khung (hai dải nanh dạng 2: nanh dài hơn hình bóng răng của họ): cả ảnh là một ô chữ nhật bám xương
    của part; chỗ đặt suy từ lưới của họ (ảnh vùng ↔ thế giới dáng gốc), kéo dài ra phần nới."""
    im = sk.images[anh_ten]
    w0, h0 = im.width - 2 * dem, im.height - 2 * dem
    uv = np.array(att["uv"], float).reshape(-1, 2) * np.array([w0, h0]) + dem
    xy = np.array(att["xy"], float).reshape(-1, 2) * KG
    M, *_ = np.linalg.lstsq(np.c_[uv, np.ones(len(uv))], xy, rcond=None)      # px ảnh → thế giới
    xg = ten[att["w"][0][0][0]]
    L = luoi.luoi_o(im.width, im.height, 2, 2, ten=slot)
    V = np.c_[L.pts, np.ones(L.n)] @ M
    sk.luoi_gan(slot, anh_ten, L, [{xg: 1.0}] * L.n, the_gioi=V)
    inv = np.linalg.inv(Wc[xg])
    sk.atts[slot][anh_ten]["verts"] = [[(xg, *[float(v) for v in (inv @ np.r_[q, 1.0])[:2]], 1.0)] for q in V]
    return L, xg


def gan_nguyen(sk, slot, anh_ten, att, ten, Wc, hinh=None):
    """slot dùng NGUYÊN lưới của con gốc (đỉnh, tam giác, uv, trọng số) với ảnh của mình đã nằm đúng khung ảnh vùng của part đó."""
    im = sk.images[anh_ten]
    L = luoi.Luoi(np.array(att["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(att["tris"]).reshape(-1, 3),
                  att["hull"], att["hull"], im.width, im.height, ten=slot)
    V = np.array(att["xy"], float).reshape(-1, 2) * KG
    sk.luoi_gan(slot, anh_ten, L, trongso.cung(L.n, "move"), the_gioi=V, ten=hinh)
    rows = []
    for p, ws in zip(V, att["w"]):
        row = [(ten[k], *[float(v) for v in (np.linalg.inv(Wc[ten[k]]) @ np.array([p[0], p[1], 1.0]))[:2]], float(w)) for k, w in ws if w > 0.002]
        tot = sum(r[3] for r in row) or 1.0
        rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    sk.atts[slot][hinh or anh_ten]["verts"] = rows
    return L


def gan_goc(sk, slot, hinh, V, att, ten, Wc):
    """lưới của mình (đỉnh V, toạ độ rig) biến dạng ĐÚNG như lưới thưa của con gốc (att): mỗi đỉnh là một điểm trong một tam giác của
    họ (toạ độ trọng tâm β) → bám xương b với trọng số W_b = Σ β_k w_b(k) và điểm gắn riêng từng xương q_b = Σ β_k w_b(k) v_k / W_b.
    Đỉnh nằm ngoài lưới của họ: bám như điểm gần nhất c trên lưới, cộng nguyên khoảng lệch (p − c) vào điểm gắn. (rong_vay_rig.py)"""
    Q = np.array(att["xy"], float).reshape(-1, 2) * KG
    tr = np.array(att["tris"]).reshape(-1, 3)
    Wg = [{ten[k]: w for k, w in ws if w > 0.002} for ws in att["w"]]
    A, B_, C = Q[tr[:, 0]], Q[tr[:, 1]], Q[tr[:, 2]]
    v0, v1 = B_ - A, C - A
    den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
    den = np.where(np.abs(den) < 1e-9, 1e-9, den)

    def gan_canh(p, a, b):
        d = b - a
        t = np.clip(((p - a) * d).sum(axis=1) / np.maximum((d * d).sum(axis=1), 1e-12), 0, 1)
        return np.hypot(*(p - (a + t[:, None] * d)).T), t

    inv = {}
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
            for n, w in Wg[vi].items():
                e = acc.setdefault(n, [0.0, np.zeros(2)])
                e[0] += bw * w
                e[1] += bw * w * Q[vi]
        row = []
        for n, (w, q) in acc.items():
            if abs(w) < 1e-5 or n not in sk.bi:
                continue
            if n not in inv:
                inv[n] = np.linalg.inv(Wc[n])
            g = q / w + lech
            lp = inv[n] @ np.array([g[0], g[1], 1.0])
            row.append((n, float(lp[0]), float(lp[1]), float(w)))
        tot = sum(r[3] for r in row) or 1.0
        rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    sk.atts[slot][hinh]["verts"] = rows
    return ngoai, xa


def gan_rieng(sk, slot, anh_ten, att, ten, Wc, dem=0.0):
    """part mang HÌNH BÓNG CỦA MÌNH (vành hoa): ảnh vẫn đúng khung ảnh vùng của part nhưng hình thò ra ngoài lưới của họ. Dựng lưới
    của mình phủ đủ ảnh; mỗi đỉnh đặt vào thế giới qua lưới của họ trong hệ uv (toạ độ trọng tâm; ngoài lưới thì kéo dài mặt phẳng
    tam giác gần nhất), rồi bám xương bằng gan_goc."""
    im = sk.images[anh_ten]
    L = luoi.luoi_vung(im, buoc_vien=14, buoc_trong=22, ten=slot, in_tk=False)
    U = np.array(att["uv"], float).reshape(-1, 2) * np.array([im.width - 2 * dem, im.height - 2 * dem]) + dem     # dem: ô nới khung
    Q = np.array(att["xy"], float).reshape(-1, 2) * KG
    tr = np.array(att["tris"]).reshape(-1, 3)
    A, B_, C = U[tr[:, 0]], U[tr[:, 1]], U[tr[:, 2]]
    v0, v1 = B_ - A, C - A
    den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
    den = np.where(np.abs(den) < 1e-9, 1e-9, den)
    tam = (A + B_ + C) / 3
    V = []
    for p in L.pts:
        v2 = p - A
        b1 = (v2[:, 0] * v1[:, 1] - v2[:, 1] * v1[:, 0]) / den
        b2 = (v0[:, 0] * v2[:, 1] - v0[:, 1] * v2[:, 0]) / den
        b0 = 1 - b1 - b2
        ok = np.flatnonzero((b0 >= -1e-4) & (b1 >= -1e-4) & (b2 >= -1e-4))
        i = int(ok[0]) if len(ok) else int(np.argmin(np.hypot(*(tam - p).T)))
        V.append(b0[i] * Q[tr[i, 0]] + b1[i] * Q[tr[i, 1]] + b2[i] * Q[tr[i, 2]])
    V = np.array(V)
    sk.luoi_gan(slot, anh_ten, L, trongso.cung(L.n, "move"), the_gioi=V)
    ng, xa = gan_goc(sk, slot, anh_ten, V, att, ten, Wc)
    return L, ng, xa


def cat_sat(path, le=3):
    """ảnh ô tự do (gai dài, ụ đất): cắt sát phần có hình."""
    g = Image.open(path).convert("RGBA")
    bb = g.split()[3].point(lambda v: 255 if v > 40 else 0).getbbox()
    return g.crop((max(0, bb[0] - le), max(0, bb[1] - le), min(g.width, bb[2] + le), min(g.height, bb[3] + le)))


def dung(k=1, nhe=1.0):
    """rig của dạng k. nhe < 1: bản nhẹ (ảnh nhỏ lại) để gộp vào rig dạng trước cho clip tiến hóa."""
    D, I, scan = nap_goc()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    assert ten == [b["name"] for b in D["bones"]]
    TI_LE = TI_LE_K[k]
    sk = khung.Sk(f"xuong_rong_{k}")
    sk.xuong("root")
    sk.xuong("move", "root")                     # game đo độ dời thân trên xương này; cung bay của đòn thường, appear đặt ở đây
    for b in IB:
        if b["name"] == "root" or b["name"] in BO_TEN:
            continue
        cha = ten[b["parent"]]
        kx, ky = TI_LE.get(b["name"], (1.0, 1.0))
        sk.xuong(b["name"], "move" if cha == "root" else cha, b["x"] * KG, b["y"] * KG, goc=b["rot"], dai=b["len"] * KG,
                 sx=b["sx"] * kx, sy=b["sy"] * ky)
    Wc = {b["name"]: np.array([[b["a"], b["b"], b["x"] * KG], [b["c"], b["d"], b["y"] * KG], [0.0, 0.0, 1.0]]) for b in D["bones"]}
    by = {a["slot"]: a for a in D["atts"]}
    slots = [s["name"] for s in I["slots"] if s["name"] not in BO_TEN and s["name"] in by]
    # mặt đất: đáy hai bàn chân ở dáng gốc
    dat_y = min(float(np.array(by[t]["xy"], float).reshape(-1, 2)[:, 1].min()) for t in ("P_tuiL2", "P_tuiR2")) * KG
    Pall = np.concatenate([np.array(by[s]["xy"], float).reshape(-1, 2) for s in slots]) * KG
    tam_x = float((Pall[:, 0].min() + Pall[:, 0].max()) / 2)
    # mặt nạ cắt ở mặt đất: .atomik chưa bật tắt được mặt nạ theo clip, nên mặt nạ bám xương `mat_dat` nằm SÂU dưới đất (không cắt
    # gì: gai dài, quả cầu xoay thò xuống dưới mặt đất vẫn nguyên); chỉ clip appear kéo nó lên đúng mặt đất
    sk.xuong("mat_dat", "root", 0.0, -MAT_SAU)
    sk.slot("mat_na", "mat_dat")
    # ảnh gai vừa, gai dài (chĩa sang phải, gốc bên trái)
    for g_ in ("gai_vua", "gai_dai"):
        pth, z_, _ = tim_part(g_, k)
        c = cat_sat(pth)
        kq = D_PX * nhe / (0.75 * z_)
        sk.anh(g_, anh.loang_mau(c.convert("RGBa").resize((max(2, round(c.width * kq)), max(2, round(c.height * kq))), Image.LANCZOS).convert("RGBA")))
    GAI_X = {}
    DEM = {}
    tong = [0, 0]

    def them_slot(slot, nguon, an=False):
        a = by[nguon]
        sk.slot(slot, "move", nguon, an=an)
        if nguon not in sk.images:
            im_, DEM[nguon] = anh_part(nguon, k, nhe)
            sk.anh(nguon, im_)
        if XR.loai(nguon) == "hoa":
            L, ng, xa = gan_rieng(sk, slot, nguon, a, ten, Wc, DEM.get(nguon, 0.0))
            ghi = f"lưới riêng {L.n} đỉnh ({ng} đỉnh ngoài lưới họ, xa nhất {xa:.1f})"
        elif DEM.get(nguon):
            L, xg_ = gan_cung(sk, slot, nguon, a, ten, Wc, DEM[nguon])
            ghi = f"ô cứng nới khung {DEM[nguon]:.0f} px, bám xương {xg_}"
        else:
            L = gan_nguyen(sk, slot, nguon, a, ten, Wc)
            ghi = f"nguyên lưới của họ {L.n} đỉnh"
        tong[0] += L.n
        tong[1] += len(L.tris)
        if nguon in GAI:
            # hai hình gai dài: ô chữ nhật trùng trục, trùng gốc, trùng bề dài và bề ngang với gai ngắn, bám xương gai
            day, mui, hw, xg = XR.gai_tg(nguon)
            GAI_X[slot] = xg
            Wd = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0, 0, 1.0]]) for b in XR._C[XR.ATT]["bones"]}
            inv = np.linalg.inv(Wd[xg])
            ld, lm = (inv @ np.r_[day, 1.0])[:2], (inv @ np.r_[mui, 1.0])[:2]      # trong hệ xương gai (không phụ thuộc dáng)
            doc = lm - ld
            dai_ = float(np.hypot(*doc))
            doc /= dai_
            ngang = np.array([-doc[1], doc[0]])
            for g_ in ("gai_vua", "gai_dai"):
                im = sk.images[g_]
                Lq = luoi.luoi_o(im.width, im.height, 2, 2, ten=slot + "_" + g_)
                loc = np.array([ld + doc * dai_ * (px / im.width) + ngang * hw * 1.08 * (1 - 2 * py / im.height) for px, py in Lq.pts])
                Vq = np.array([(Wc[xg] @ np.r_[q, 1.0])[:2] for q in loc])       # dáng gốc của họ (xương gai dạng 2 đã đổi tỉ lệ)
                sk.luoi_gan(slot, g_, Lq, [{xg: 1.0}] * Lq.n, the_gioi=Vq, ten=g_)
                sk.atts[slot][g_]["verts"] = [[(xg, float(q[0]), float(q[1]), 1.0)] for q in loc]
            ghi += f"; + gai_vua, gai_dai trên xương {xg}"
        print(f"  {slot:16s} ← {nguon:12s} {ghi}")

    for s in slots:
        them_slot(s, s)
    for s in S_TAY_SAU:                           # bản sao tay sau ở lớp trước thân (ẩn sẵn)
        them_slot("truoc_" + s, s, an=True)
    cuoi = sk.slots[-1]["name"]
    sk.cat("mat_na", cuoi, [(tam_x - 2500, dat_y - 5 - MAT_SAU), (tam_x + 2500, dat_y - 5 - MAT_SAU), (tam_x + 2500, dat_y + 6000),
                            (tam_x - 2500, dat_y + 6000)])
    # ụ đất của appear: trước mọi thứ, ẩn sẵn, không bị mặt nạ cắt
    ud = cat_sat(tim_part("u_dat", k)[0])
    if nhe != 1.0:
        ud = ud.convert("RGBa").resize((max(2, round(ud.width * nhe)), max(2, round(ud.height * nhe))), Image.LANCZOS).convert("RGBA")
    sk.anh("u_dat", anh.loang_mau(ud))
    sk.xuong("u_dat", "root", tam_x + 6, dat_y - 4)
    sk.slot("u_dat", "u_dat", "u_dat", an=True)
    rong = 235.0 * KG                            # ụ đất thấp, dẹt (cao ~50): vành hoa nhú lên 96 đơn vị phải lộ trên ụ
    sk.manh("u_dat", "u_dat", Dat(tam_x + 6, dat_y - 14, ti=(rong / ud.width, 0.42 * rong / ud.width), neo=(0.5, 1.0)))
    # xương miệng: giữa lỗ miệng (tâm lòng miệng ở dáng gốc), con của quả cầu
    cm = np.array(by["P_kouqiang"]["xy"], float).reshape(-1, 2).mean(axis=0) * KG
    lp = np.linalg.solve(Wc["bone12"], np.array([cm[0] + 40.0, cm[1], 1.0]))
    sk.xuong("mieng", "bone12", float(lp[0]), float(lp[1]))
    lech = max(float(np.hypot(sk.goc_tg(b["name"])[0] - b["x"] * KG, sk.goc_tg(b["name"])[1] - b["y"] * KG)) for b in D["bones"]
               if b["name"] in sk.bi and not any(b["name"] in (IB[k_["bones"][0]]["name"], IB[k_["bones"][-1]]["name"]) for k_ in I["ik"]))
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác; mặt đất y = {dat_y:.1f}; "
          f"xương không dính IK lệch dáng gốc của họ tối đa {lech:.3f}")
    for e, m in (("trung", "khung cắn"), ("phun", "gai bung"), ("het_phun", "gai rút"), ("phong", "chiêu cuối: phồng, gai dài"),
                 ("bat", "chiêu cuối: rời chỗ (code cho bay)"), ("tong", "chiêu cuối TÔNG THẲNG: AolaSticker.Jump bay gần như ngang (Rams)"), ("cham_dat", "chạm (đối thủ / đất)"), ("dap", "chiêu cuối: về tới chỗ"),
                 ("nut_dat", "appear: đất nứt"), ("troi", "appear: vọt lên khỏi đất")):
        sk.su_kien(e, m)
    return sk, dict(scan=scan, IB=IB, ten=ten, slots=[s["name"] for s in I["slots"]], GAI_X=GAI_X, dat_y=dat_y, k=k)


def chuyen_dong(sk, info):
    """clip đã lấy mẫu → {clip: (dài, {xương: mảng (số khung, 5) = xoay độ, dời x, y, tỉ lệ x, y nhân}, ẩn [khung][slot], tay sau ra
    trước [khung])}: lệch của biến đổi RIÊNG đã áp (runtime Spine) so với dáng gốc."""
    S = json.load(open(os.path.join(info["scan"], "sample_moi.json"), encoding="utf-8"))
    IB, ten, SL = info["IB"], info["ten"], info["slots"]
    ids = [i for i, n in enumerate(ten) if n in sk.bi and n != "root"]
    i_than, i_tay = SL.index("P_shenti"), SL.index("P_shouL1")
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        res = {}
        for i in ids:
            b0 = IB[i]
            A = np.array([[F["l"][i][2] - b0["rot"], (F["l"][i][0] - b0["x"]) * KG, (F["l"][i][1] - b0["y"]) * KG,
                           F["l"][i][3] / (b0["sx"] or 1.0), F["l"][i][4] / (b0["sy"] or 1.0)] for F in fr])
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            # quả cầu xoay nhiều vòng: chuẩn góc theo đầu clip còn ở dáng nghỉ; clip hết ở dáng nghỉ thì chuẩn theo khung cuối
            moc = A[0, 0] if clip == "xr_skill" else A[-1, 0]
            A[:, 0] -= 360.0 * round(moc / 360.0)
            if np.abs(A[:, :3]).max() > 1e-3 or np.abs(A[:, 3:] - 1).max() > 1e-4:
                res[ten[i]] = A
        an = [{SL[j] for j, n in enumerate(F["n"]) if n is None and SL[j] in sk.si} for F in fr]
        truoc = [F["o"].index(i_tay) > F["o"].index(i_than) for F in fr]
        out[clip] = (float(v["dur"]), res, an, truoc)
    return out


def lam_clip(sk, info):
    CD = chuyen_dong(sk, info)
    GAI_X = info["GAI_X"]
    nhe_hoa = 0.55 if info["k"] == 2 else 1.0
    U_T, U_C = RC.P_TROI, RC.P_CHAM

    def dat_dang(P, goc, tau, lap, tt="", dam=True):
        """đặt dáng của clip nguồn `goc` ở giây tau. tt: tiền tố xương / slot / hình (rig gộp tiến hóa: "n_"); dam=False: không đụng
        độ đậm slot (clip tiến hóa tự lo hiện / tan)."""
        dur, R, an, truoc = CD[goc]
        n = len(an)
        x = (tau % dur if lap else min(max(tau, 0.0), dur)) * 30.0
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        tl = {}
        for b, A in R.items():
            v = A[i0] * (1 - w) + A[i1] * w
            if nhe_hoa != 1.0 and b in RC.HOA:        # dạng 2: cánh hoa dài, to (xương hoa × 1,28) nên lắc nhẹ hơn kẻo cánh bị ép mảnh
                v = np.array([v[0] * nhe_hoa, v[1] * nhe_hoa, v[2] * nhe_hoa, v[3], v[4]])
            tl[b] = v
            if abs(v[0]) > 1e-4:
                P.rot(tt + b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(tt + b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(tt + b, float(v[3]), float(v[4]))
        if dam:
            for s in an[i0]:
                P.alpha[tt + s] = 0.0
            tr = truoc[i0]
            for s in S_TAY_SAU:                   # tay sau: bản gốc (sau thân) hoặc bản sao (trước thân)
                hien = s not in an[i0]
                P.alpha[tt + s] = 1.0 if hien and not tr else 0.0
                P.alpha[tt + "truoc_" + s] = 1.0 if hien and tr else 0.0
        for slot, xg in GAI_X.items():            # gai phóng dài: đổi hình theo tỉ lệ dài/ngang của xương gai
            v = tl.get(xg)
            ti = float(v[3] / max(1e-3, v[4])) if v is not None else 1.0
            P.att[tt + slot] = tt + ("gai_dai" if ti >= TI_GAI[1] else "gai_vua" if ti >= TI_GAI[0] else slot.replace("truoc_", ""))
        bay = RC.BAY.get(goc)
        if bay:
            dx, dy = bay(min(max(tau, 0.0), dur))
            if abs(dx) > 1e-4 or abs(dy) > 1e-4:
                P.move(tt + "move", dx * KG, dy * KG)

    def u_dat(t, P):
        """ụ đất của appear: đùn lên cùng lúc hoa nhú, rung khi con thụt lấy đà, bung to lúc con vọt ra rồi xẹp, tan."""
        e = RC.em
        lon = e(t / 0.22) * (1.0 + 0.05 * np.sin(2 * np.pi * 2.1 * t)) if t < U_T else 1.0
        if t >= U_T:
            lon = 1.0 + 0.28 * RC.cung(t, U_T - 0.01, U_T + 0.06, U_T + 0.08, U_T + 0.30)
        xep = 1.0 - 0.72 * e((t - U_T - 0.10) / (U_C + 0.30 - U_T - 0.10)) if t > U_T + 0.10 else 1.0
        P.scale("u_dat", lon * (1.0 + 0.25 * (1 - xep)), lon * xep * (0.25 + 0.75 * e(t / 0.22)))
        P.alpha["u_dat"] = float(np.clip(t / 0.06, 0, 1) * (1.0 - e((t - U_C - 0.05) / 0.40)))

    out = []
    for ten_, goc, lap, trung in CLIPS:
        dur = CD[goc][0]
        ev = RC.SU_KIEN.get(goc, [])
        if ten_ == "die":
            def fn(t, P, goc=goc, dur=dur):
                dat_dang(P, goc, t, False)
                a = float(np.clip(1.0 - (t - dur) / (TAN - 0.1), 0.0, 1.0))
                for sl in sk.slots:
                    if sl["name"] not in ("mat_na", "u_dat"):
                        P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])
            out.append(Clip(ten_, dur + TAN, fn, ev=ev))
        elif ten_ == "appear":
            def fn(t, P, goc=goc, dur=dur):
                dat_dang(P, goc, t, False)
                u_dat(t, P)
                # mặt nạ lên đúng mặt đất suốt lúc trồi; con đã đứng hẳn trên đất (sau khi chạm đất) thì hạ mặt nạ xuống lại
                P.move("mat_dat", 0.0, MAT_SAU * (1.0 - RC.em((t - U_C - 0.10) / 0.12)))
                if t < 0.02:                    # khung đầu trống hẳn (cả con còn dưới đất)
                    for sl in sk.slots:
                        if sl["name"] != "mat_na":
                            P.alpha[sl["name"]] = 0.0
            out.append(Clip(ten_, dur, fn, ev=ev, trung=trung))
        else:
            out.append(Clip(ten_, dur, (lambda t, P, goc=goc, lap=lap: dat_dang(P, goc, t, lap)), loop=lap, ev=ev, trung=trung))
    return out, dat_dang


def tien_hoa(sk1, dd1, cao1):
    """rig dạng 1 gộp bản nhẹ của dạng 2 + clip evolve 2,8 s (quai/tienhoa.py): dạng 1 giơ hai tay lên trời gồng, rung; tan lúc đổi
    dạng (sự kiện doi_dang, VFX là lớp riêng của game); dạng 2 hiện lớn dần, há miệng gầm xù gai, hoà về đúng khung 0 idle dạng 2."""
    sk2, info2 = dung(2, nhe=0.6)
    cl2, dd2 = lam_clip(sk2, info2)
    idle2 = hoat.nuong(sk2, [c for c in cl2 if c.ten == "idle"][0])[0]
    cao2 = soi.chieu_cao(soi.Ve(sk2), idle2, BO_CAO)
    ti = cao1 / cao2
    M = tienhoa.gop(sk1, sk2)

    def gong(t, P):                               # dạng cũ: hai tay giơ lên trời (dáng 0,22 s của cast), thân rung dần
        g = hoat.cv(t, [(0, 0), (0.55, 1, "out"), (1.4, 1)])
        dd1(P, "xr_cast", 0.22 * g, False)
        r = hoat.rung(t, 0.5, 1.35, moi=1)
        P.move("bone3", 1.6 * r, 0.0)
        P.scale("bone4", 1 + 0.04 * g + 0.012 * r, 1 + 0.04 * g - 0.012 * r)

    def gam(t, P, fl):                            # dạng sau: há miệng gầm, xù gai (đoạn gầm của appear: 1,50 → 1,72 s)
        dd2(P, "xr_appear", 1.50 + 0.22 * max(0.0, min(1.0, fl)), False, tt="n_", dam=False)
        r = hoat.rung(t, 2.0, 2.4, moi=1)
        P.scale("n_bone4", 1 + 0.03 * fl + 0.01 * r * fl, 1 + 0.03 * fl - 0.01 * r * fl)

    ev = tienhoa.clip_tien_hoa(M, sk1, sk2, idle2, tiB=ti, fnA=gong, fnB=gam)
    return M, ev, sk2, idle2, ti


def main(a):
    k = XR.K
    sk, info = dung(k)
    clips, dat_dang = lam_clip(sk, info)
    ra = RA or os.path.join(XR.HERE, "inbox", f"{XR.CODE}_{k}", "rig")
    if a and a[0] == "bo_cuc":                 # hình bố cục 1536x1024 nền trắng ở dáng concept (xr_dang) → a[1] (cho prompt concept của dạng)
        P = khung.Pose()
        dat_dang(P, "xr_dang", 0.0, False)
        ve = soi.Ve(sk)
        Bx = soi._union([ve.bao(P)], 0.10)
        sc = min(1536 * 0.80 / (Bx[2] - Bx[0]), 1024 * 0.84 / (Bx[3] - Bx[1]))
        im = ve.ve(P, Bx, sc, bg=(255, 255, 255), ss=2).convert("RGB")
        o_ = Image.new("RGB", (1536, 1024), (255, 255, 255))
        o_.paste(im, ((1536 - im.width) // 2, (1024 - im.height) // 2))
        os.makedirs(os.path.dirname(a[1]), exist_ok=True)
        o_.save(a[1])
        print(a[1], im.size)
        return
    if a and a[0] == "soi":                    # soi <clip> <giây,giây,...> [tỉ lệ] [luoi]: khung lớn nền xám → rig/soi_<clip>.png
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 1.0
        kw = dict(luoi=True, mau_luoi=(10, 10, 10, 90)) if len(a) > 4 else {}
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2, **kw).convert("RGB") for P in Ps]
        cot = min(len(ims), 4)
        hang = (len(ims) + cot - 1) // cot
        out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang), (150, 150, 150))
        for i, im in enumerate(ims):
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(ra, exist_ok=True)
        pth = os.path.join(ra, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    M, noi_ = sk, {}
    frames = {c.ten: hoat.nuong(sk, c) for c in clips}
    for c in clips:
        if c.ten in VE_NGHI:
            frames[c.ten] = [P.copy() for P in frames[c.ten]]
            hoat.khop_cuoi(frames[c.ten], frames["idle"][0], 0.2)
    cao = soi.chieu_cao(soi.Ve(sk), frames["idle"][0], BO_CAO)
    co_dang_2 = os.path.exists(os.path.join(XR.manh_dir(2), "part", "P_shenti.png")) and not os.environ.get("XR_MANH")
    if k == 1 and co_dang_2:                   # dạng 1: gộp bản nhẹ của dạng 2 + clip tiến hóa
        M, ev, sk2, idle2, ti = tien_hoa(sk, dat_dang, cao)
        clips = clips + [ev]
        frames["evolve"] = hoat.nuong(M, ev)
        _, _, s_ev = tienhoa.lech_cuoi(M, frames["evolve"], sk2, idle2, ti)
        noi_["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
        print("  evolve:", noi_["evolve"])
    xuat.xuat_het(M, clips, ra, f"xuong_rong_{k}", f"Xương rồng tròn (xuong_rong) dạng {k}", frames=frames, dang=k, so_dang=2,
                  dung_yen=("cast", "skill", "skill_land"), ma_goc=None, khop_idle=0, cao=cao, noi_them=noi_, impact=IMPACT_K[k],
                  tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, dich_mb=0.6, tran_mb=1.0)


if __name__ == "__main__":
    main(sys.argv[1:])
