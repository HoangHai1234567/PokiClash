# -*- coding: utf-8 -*-
"""Sâu đất khổng lồ (sau_dat; tướng 7 đảo Thổ, ải 40): hình của mình chạy trên ĐÚNG rig của con gốc monster_3643 (như hoa_ho_rig.py,
skill pokiclash-spine-rig mục 00). Ghi chú: inbox/sau_dat_ghichu.md.
- XƯƠNG: đủ mọi xương của họ, đúng cha – con, đúng biến đổi riêng ở dáng gốc; thêm `move`; `fly_sau` (con của root, trùng chỗ xương
  `bone` tĩnh của họ) làm CHA MỚI của chuỗi thân `bone6..` để cả con sâu (thân, đầu, râu, tua gáy) lặn xuống đất và trồi lên ở chỗ đối
  thủ (game co quãng bằng xương `fly*`, `AolaActor.FarAtomik`); `far` (đích hiệu ứng ở xa); `mieng` (giữa miệng, con của sọ bone12).
- MẢNH: part khung của mình (manh/part/<vùng>.png, sau_dat_part.py) lắp vào NGUYÊN lưới của họ; mảnh cứng của đầu (manh/cung/*.png,
  sau_dat_cung.py) đặt theo chỗ trên concept, lưới dày, mỗi đỉnh bám như điểm tương ứng trên lưới của part gốc nguồn (NGUON). Gai mõm
  `P_jiao_06` tạm ẩn. Mặt nạ cắt `cat_dat` (mọi slot, hình chữ nhật trên mặt đất): phần dưới đất bị giấu (chui lên, lặn xuống).
- CHUYỂN ĐỘNG: mẫu khung của họ (scan/sample.json, `l`, 30 khung/giây) → lệch so với dáng gốc; clip = co giãn giờ clip nguồn + kênh riêng.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/sau_dat_rig.py       → inbox/sau_dat_1/rig/ (SD_GOC=1: da gốc → rig_goc/)
    py -3 -I ArtGen/Spine/sau_dat_rig.py soi <clip> <giây,...|n=12|t0:t1:n> [tỉ lệ]      → soi_<clip>.png
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
import sau_dat  # noqa: E402,F401
import tho5  # noqa: E402

G = tho5.dat("sau_dat")
GOC = os.environ.get("SD_GOC") == "1"
D_PX = float(os.environ.get("SD_DPX", "0.5" if GOC else "0.55"))     # px atlas mỗi đơn vị rig (con cao ~1150 đơn vị)
FPS = 30.0
TAN = 0.45
MANH = os.path.join(G.BASE, "manh", "part")
CUNG = os.path.join(G.BASE, "manh", "cung")
# P_jiao_06 (gai mõm của họ): concept không có. P_jiao_04 / 08 / 05 (vòng giáp thứ hai, gờ mày, mắt): đã GỘP vào mảnh đầu cắt thẳng từ
# concept (sau_dat_dau.py, 2026-11-17).
BO_SLOT = ("shadow",) + (() if GOC else ("P_jiao_06", "P_jiao_04", "P_jiao_08", "P_jiao_05"))
# DẠNG 1 "Sa Trùng Nhi" (SD_DANG=non; người dùng 2026-11-17: "tự nghĩ 1 mini version, cùng rig"): cùng xương, lưới, clip; đổi TỈ LỆ ở rig
# (skill pokiclash-spine-rig "DẠNG KHÁC trên CÙNG rig gốc"): thân ngắn, đầu to tương đối (chibi chỉ ở dạng 1), râu ngắn và ít, ba phiến nhỏ.
# bone16 (đầu) thừa hưởng KHÔNG tỉ lệ (inherit 3) nên tỉ lệ đầu là tuyệt đối, không nhân với thân.
NON = os.environ.get("SD_DANG") == "non" and not GOC
TEN_RIG = "sau_dat_non" if NON else "sau_dat_1"
TI_NON = {"bone6": 0.82, "bone16": 1.12, "bone23": 0.6, "bone30": 0.6, "bone63": 0.7, "bone69": 0.7, "bone76": 0.7,
          "bone153": 0.8, "bone154": 0.8, "bone3": 0.8, "bone4": 0.8, "bone5": 0.8}
for _b in ("bone155", "bone156", "bone157", "bone158", "bone159", "bone160", "bone161", "bone162", "bone163", "bone164"):
    TI_NON[_b] = 0.7                                                # râu ngắn
for _b in ("bone148", "bone144", "bone136", "bone140", "bone132"):
    TI_NON[_b] = 0.75                                               # phiến nhỏ
for _b in ("bone128", "bone125", "bone122", "bone119"):
    TI_NON[_b] = 0.72                                               # tảng trước
for _b in ("bone38", "bone44", "bone51", "bone57", "bone93", "bone101", "bone110"):
    TI_NON[_b] = 0.62                                               # tua quanh chân
for _b in ("bone18", "bone19", "bone20", "bone21"):
    TI_NON[_b] = 0.7                                                # mào ba tấm nhỏ lại (không át đầu)
# concept B đã duyệt (2026-11-17) chỉ ba râu: bỏ thêm A_chuxu_01 / 06 (hai roi sát mõm)
BO_NON = ("A_chuxu_07", "A_chuxu_08", "A_chuxu_09", "A_chuxu_010", "A_chuxu_01", "A_chuxu_06", "P_shitou_06", "P_shitou_07")
if NON:
    BO_SLOT = BO_SLOT + BO_NON
# DA dạng 1 (sau_dat_non_da.py): mảnh đầu cắt từ concept B, thân / râu đổi màu; ảnh nào dạng 1 không có thì dùng của dạng 2.
# SD_DA2=1: dạng 1 mặc da dạng 2 (bố cục, khớp mảnh đầu).
NON_DA = NON and os.environ.get("SD_DA2") != "1"
BASE_NON = os.path.join(HERE, "inbox", "sau_dat_non")
if NON_DA:
    CUNG = os.path.join(BASE_NON, "manh", "cung")
RAU = tuple(f"A_chuxu_{k}" for k in ("01", "010", "02", "03", "04", "05", "06", "07", "08", "09"))
# mảnh cứng: tên mảnh → part gốc làm nguồn trọng số (ngà bám HÀM)
CUNG_SLOT = {"P_shange": "dau", "P_xiae_01": "ham", "P_xiae_02": "mieng", "P_jiao_05": "mat", "P_jiao_08": "may", "P_jiao_07": "nanh1",
             "P_jiao_09": "nanh2", "P_jiao_03": "maoA", "P_jiao_02": "maoB", "P_jiao_01": "maoC", "P_jiao_04": "vong"}
NGUON = {"P_jiao_07": "P_xiae_01", "P_jiao_09": "P_xiae_01", "P_jiao_04": "P_shange"}
# thứ tự vẽ của cụm đầu (sau → trước), chèn ngay sau khúc thân cuối của họ: mào sau vòng giáp, lòng miệng sau hai hàm, ngà (có hốc ngà
# màu vàng đất như concept) TRƯỚC cả đầu và hàm. Người dùng 2026-11-17 "2 nanh dưới nhìn như lỗi layer": do mảnh ngà trái tách hỏng
# (xén mũi, dính mẩu vòng giáp) và đầu vẽ đè lên hốc ngà; để ngà sau hàm thì hàm che mất cả ngà.
DAU_THU_TU = ["P_jiao_01", "P_jiao_02", "P_jiao_03", "P_jiao_04", "P_xiae_02", "P_xiae_01", "P_shange", "P_jiao_07", "P_jiao_09",
              "P_jiao_08", "P_jiao_05"]
SAU_SAU = 1350.0                          # độ sâu lặn (đơn vị rig): cả con sâu xuống dưới mặt đất
DAT_Y = -16.0                             # mép trên mặt nạ đất (dưới đế đá thấp nhất y = -14)
PHIEN = ("bone148", "bone144", "bone136", "bone140", "bone132")                     # gốc năm phiến sau lưng (trái → phải)
TANG = ("bone128", "bone125", "bone122", "bone119")                                 # gốc bốn tảng trước
TUA = ("bone38", "bone44", "bone51", "bone57", "bone93", "bone101", "bone110")      # gốc các chuỗi tua quanh chân
DE = ("bone3", "bone4", "bone5", "bone153", "bone154")                              # đế đá, hai phiến dẹt sát đất
IMPACT = {"attack": (0.13, 0.85, 0.16), "cast": (0.16, 1.0, 0.2, "#ffd9a055"), "skill": (0.30, 1.6, 0.30, "#fff0c088")}


# ---------------------------------------------------------------- nạp
def nap_goc():
    scan = G.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    D0 = json.load(open(os.path.join(scan, "att_idle0.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    return D, D0, I, scan


def _goc(M):
    return math.degrees(math.atan2(M[1, 0], M[0, 0]))


def concept_tg():
    """px concept (khung goc_ca_con) → thế giới rig dáng gốc."""
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    return s, (lambda P: np.stack([(np.asarray(P, float)[..., 0] - 768) / s + cx, -(np.asarray(P, float)[..., 1] - 512) / s + cy], -1))


def anh_part(a):
    r = a["region"]
    if GOC:
        g = G.part_goc(a)
        kq = D_PX / 0.5
    else:
        import sau_dat_part as M
        pth = os.path.join(MANH, r + ".png")
        p1 = os.path.join(BASE_NON, "manh", "part", r + ".png")
        if NON_DA and os.path.exists(p1):
            pth = p1
        if not os.path.exists(pth):
            raise SystemExit("thiếu ảnh part " + pth)
        g = Image.open(pth).convert("RGBA")
        kq = D_PX / (0.5 * M.zs()[r])
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g)


def gan_nguyen(sk, slot, anh_ten, att, ten, Wc):
    im = sk.images[anh_ten]
    L = luoi.Luoi(np.array(att["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(att["tris"]).reshape(-1, 3),
                  att["hull"], att["hull"], im.width, im.height, ten=slot)
    V = np.array(att["xy"], float).reshape(-1, 2)
    sk.luoi_gan(slot, anh_ten, L, trongso.cung(L.n, "move"), the_gioi=V)
    rows = []
    for p, ws in zip(V, att["w"]):
        row = [(ten[k], *[float(v) for v in (np.linalg.inv(Wc[ten[k]]) @ np.array([p[0], p[1], 1.0]))[:2]], float(w)) for k, w in ws if w > 0.002]
        tot = sum(r[3] for r in row) or 1.0
        rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    sk.atts[slot][anh_ten]["verts"] = rows
    return L


def gan_theo_goc(sk, slot, anh_ten, L, V, att, ten, Wc, att_tu=None):
    """lưới của mình (đỉnh V) biến dạng như lưới của part gốc att: đỉnh trong một tam giác của họ (trọng tâm β) bám xương b với
    W_b = Σ β_k w_b(k), điểm gắn q_b = Σ β_k w_b(k) v_k / W_b; ngoài lưới: như điểm gần nhất + khoảng lệch. Trả đỉnh ở dáng gốc.
    att_tu: lưới gốc ở DÁNG mà V được đo (khung 0 idle: concept vẽ trên dáng đó). β tính trên att_tu, điểm gắn bằng đỉnh của att ở dáng
    gốc (cùng dáng với Wc); khoảng lệch ngoài lưới đổi qua phép afin của tam giác gần nhất. Không có att_tu: V ở dáng gốc.
    (2026-11-17: gắn thẳng toạ độ concept như dáng gốc làm mảnh đầu trượt 30–90 đơn vị mỗi mảnh một kiểu: đầu hở, hàm lệch.)"""
    Qg = np.array(att["xy"], float).reshape(-1, 2)
    Q = np.array((att_tu or att)["xy"], float).reshape(-1, 2)
    tr = np.array(att["tris"]).reshape(-1, 3)
    Wg = [{ten[k]: w for k, w in ws if w > 0.002} for ws in att["w"]]
    A, B_, C = Q[tr[:, 0]], Q[tr[:, 1]], Q[tr[:, 2]]
    v0, v1 = B_ - A, C - A
    den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
    den = np.where(np.abs(den) < 1e-9, 1e-9, den)
    rows, dat_g = [], []
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
            best = None
            for (pa, pb, ia, ib) in ((A, B_, 0, 1), (B_, C, 1, 2), (C, A, 2, 0)):
                d = pb - pa
                t = np.clip(((p - pa) * d).sum(1) / np.maximum((d * d).sum(1), 1e-12), 0, 1)
                dist = np.hypot(*(p - (pa + t[:, None] * d)).T)
                j = int(np.argmin(dist))
                if best is None or dist[j] < best[0]:
                    w3 = [0.0, 0.0, 0.0]
                    w3[ia], w3[ib] = 1 - float(t[j]), float(t[j])
                    best = (float(dist[j]), j, tuple(w3), pa[j] + t[j] * (pb[j] - pa[j]))
            _, i, be, c = best
            lech = p - c
            if att_tu is not None:                                    # khoảng lệch: dáng từ → dáng gốc qua afin của tam giác
                a_, b_, c_ = tr[i]
                Mi = np.c_[Q[b_] - Q[a_], Q[c_] - Q[a_]]
                Mg = np.c_[Qg[b_] - Qg[a_], Qg[c_] - Qg[a_]]
                if abs(np.linalg.det(Mi)) > 1e-6:
                    lech = Mg @ np.linalg.solve(Mi, lech)
        dat_g.append(sum(bw * Qg[vi] for vi, bw in zip(tr[i], be)) + lech)
        acc = {}
        for vi, bw in zip(tr[i], be):
            for n, w in Wg[vi].items():
                e = acc.setdefault(n, [0.0, np.zeros(2)])
                e[0] += bw * w
                e[1] += bw * w * Qg[vi]
        row = []
        for n, (w, q) in acc.items():
            if abs(w) < 1e-5:
                continue
            g = q / w + lech
            lp = np.linalg.inv(Wc[n]) @ np.array([g[0], g[1], 1.0])
            row.append((n, float(lp[0]), float(lp[1]), float(w)))
        tot = sum(r[3] for r in row) or 1.0
        rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    Vg = np.array(dat_g)
    sk.luoi_gan(slot, anh_ten, L, trongso.cung(L.n, "move"), the_gioi=Vg)
    sk.atts[slot][anh_ten]["verts"] = rows
    return Vg


def ve_dang_goc(P, att, att_tu):
    """điểm ở dáng của att_tu → dáng gốc qua phép afin của tam giác gần nhất trên lưới part."""
    Qg = np.array(att["xy"], float).reshape(-1, 2)
    Q = np.array(att_tu["xy"], float).reshape(-1, 2)
    tr = np.array(att["tris"]).reshape(-1, 3)
    out = []
    for p in np.atleast_2d(P):
        i = int(np.argmin(np.hypot(*(Q[tr].mean(1) - p).T)))
        a_, b_, c_ = tr[i]
        Mi = np.c_[Q[b_] - Q[a_], Q[c_] - Q[a_]]
        Mg = np.c_[Qg[b_] - Qg[a_], Qg[c_] - Qg[a_]]
        out.append(Qg[a_] + Mg @ np.linalg.solve(Mi, p - Q[a_]))
    return np.array(out)


def mieng_gian(sk, slot, anh_ten, Vg, Wc, tam, mat):
    """lòng miệng CO GIÃN theo hàm (người dùng 2026-11-17): nửa trên bám sọ (bone12), nửa dưới bám hàm (bone13), giữa hoà dần theo
    khoảng cách có dấu tới đường môi (qua khớp hàm và tâm miệng); há miệng thì lòng miệng giãn ra, không trượt nguyên khối theo hàm.
    Vg (đỉnh), tam (tâm miệng), mat (mắt: chỉ phía sọ): đều ở dáng gốc."""
    khop = Wc["bone13"][:2, 2]
    d = (tam - khop) / np.hypot(*(tam - khop))
    n = np.array([-d[1], d[0]])
    if n @ (mat - tam) < 0:
        n = -n
    R = max(1.0, float(np.abs((Vg - tam) @ n).max()))
    rows = []
    for p in Vg:
        s = float((p - tam) @ n) / R
        u = min(1.0, max(0.0, (0.40 - s) / 0.80))
        wj = u * u * (3 - 2 * u)
        row = []
        for b, w in (("bone12", 1 - wj), ("bone13", wj)):
            if w > 1e-4:
                lp = np.linalg.inv(Wc[b]) @ np.array([p[0], p[1], 1.0])
                row.append((b, float(lp[0]), float(lp[1]), float(w)))
        tot = sum(r[3] for r in row)
        rows.append([(b, x, y, w / tot) for b, x, y, w in row])
    sk.atts[slot][anh_ten]["verts"] = rows


def _ss(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def vanh_mem(sk, Wc, VG, C, mat, R0):
    """VÀNH MIỆNG CO GIÃN (người dùng 2026-11-17: "đoạn há to mồm này lỗi, rig thêm xương phần hàm trên để nó nối với hàm dưới"): quanh nửa
    TRƯỚC miệng, đầu (sọ bone12), hàm (bone13) và lòng miệng dùng CHUNG một trường trọng số: phía trên đường môi bám sọ, phía dưới bám hàm,
    góc miệng nửa nọ nửa kia, mờ dần ra ngoài bán kính 1,15–1,9 R0 và về phía khớp hàm. Há miệng thì vành tròn kéo giãn, góc miệng vẫn liền,
    lòng miệng không lòi ra ngoài đầu. VG: đỉnh dáng gốc từng slot; C tâm miệng, mat mắt (chỉ phía sọ), R0 bán kính miệng (dáng gốc)."""
    khop = Wc["bone13"][:2, 2]
    d = (C - khop) / np.hypot(*(C - khop))
    n = np.array([-d[1], d[0]])
    if n @ (mat - C) < 0:
        n = -n
    inv = {b: np.linalg.inv(Wc[b]) for b in ("bone12", "bone13")}

    def tron(row, p, b, w):
        """trộn thêm xương b với tỉ phần w vào hàng trọng số (điểm gắn mọi xương tính lại từ p: dáng gốc trùng tuyệt đối)."""
        acc = {}
        for (n_, _, _, ww) in row:
            acc[n_] = acc.get(n_, 0.0) + ww * (1 - w)
        acc[b] = acc.get(b, 0.0) + w
        out = []
        for n_, ww in acc.items():
            if ww < 1e-4:
                continue
            Mi = inv[n_] if n_ in inv else np.linalg.inv(Wc[n_])
            lp = Mi @ np.array([p[0], p[1], 1.0])
            out.append((n_, float(lp[0]), float(lp[1]), float(ww)))
        tot = sum(r[3] for r in out)
        return [(n_, x, y, ww / tot) for n_, x, y, ww in out]

    for slot, Vg in VG.items():
        att = next(iter(sk.atts[slot].values()))
        rows = att["verts"]
        for i, p in enumerate(Vg):
            q = p - C
            v, u, r = float(q @ n), float(q @ d), float(np.hypot(*q))
            sv = _ss((0.55 * R0 - v) / (1.1 * R0))                    # 1 dưới đường môi (phần hàm), 0 trên
            if slot == "P_xiae_02":
                rows[i] = tron([("bone12", 0, 0, 1.0)], p, "bone13", sv)
                continue
            # cả góc miệng PHÍA SAU (má, gần khớp hàm) cũng co giãn: bản đầu chỉ phủ nửa trước (gf từ −0,7 R0) → khe hình nêm ở góc sau
            # khi hàm xoay (người dùng 2026-11-17: "đoạn này vẫn bị hở")
            fr = 1 - _ss((r - 1.45 * R0) / (0.95 * R0))
            gf = _ss((u + 2.0 * R0) / (0.8 * R0))
            if slot == "P_shange":
                rows[i] = tron(rows[i], p, "bone13", sv * fr * gf)
            else:
                rows[i] = tron(rows[i], p, "bone12", (1 - sv) * fr * gf)


def them_lot(sk, by, than_slots, ten, Wc):
    """LÓT THÂN: cả ảnh thân liền (tai_ve/N_L, sau_dat_part.to_lien) thành MỘT lưới nằm SAU mọi khúc cổ của họ; mỗi đỉnh bám như điểm tương
    ứng trên lưới hợp của các part thân gốc. Lúc vươn cao các khúc trượt lên nhau, khe hé ra chỉ lộ thân, không lộ nền (soi 2026-11-17:
    khe chữ V dưới hàm, chỗ con gốc được hàm và lưỡi mào của họ che)."""
    from quai import anh as A_
    import sau_dat_part as M
    Lj = json.load(open(os.path.join(G.MAU, "lien_L.json"), encoding="utf-8"))
    ti, (ox, oy) = Lj["ti"], Lj["goc"]
    nl = os.path.join(BASE_NON, "tai_ve", "N_L.png")
    tt = A_.doc_to(nl if (NON_DA and os.path.exists(nl)) else A_.to_moi_nhat(G.TAI, "N_L"), dien_tich_min=600, gop_px=10)
    a = tt.rgba
    ys, xs = np.nonzero(a[..., 3] > 10)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    g = Image.fromarray(a[y0:y1, x0:x1], "RGBA")
    kq = D_PX / ti
    g2 = anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA"))
    sk.anh("than_lot", g2)
    sk.slot("than_lot", "move", "than_lot", truoc=than_slots[0])
    L = luoi.luoi_vung(g2, buoc_vien=10.0, buoc_trong=14.0, ten="than_lot", in_tk=False)
    Ppx = np.array(L.pts, float) / kq + np.array([x0, y0])
    V = np.stack([(Ppx[:, 0] - ox) / ti, (oy - Ppx[:, 1]) / ti], 1)
    # lưới hợp của các part thân gốc (đỉnh, tam giác, trọng số nối liền)
    xy, tris, ws, n0 = [], [], [], 0
    for s in than_slots:
        q = by[s]
        P_ = np.array(q["xy"], float).reshape(-1, 2)
        xy.append(P_)
        tris.append(np.array(q["tris"]).reshape(-1, 3) + n0)
        ws += q["w"]
        n0 += len(P_)
    hop = {"xy": np.concatenate(xy).ravel().tolist(), "tris": np.concatenate(tris).ravel().tolist(), "w": ws}
    gan_theo_goc(sk, "than_lot", "than_lot", L, V, hop, ten, Wc)
    return L


def dung():
    D, D0, I, scan = nap_goc()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    assert ten == [b["name"] for b in D["bones"]]
    sk = khung.Sk(TEN_RIG)
    sk.xuong("root")
    sk.xuong("move", "root")
    Wc = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]]) for b in D["bones"]}
    Wb = Wc["bone"]
    goc0 = {}
    for b in IB:
        if b["name"] == "root":
            continue
        cha = ten[b["parent"]]
        g = [b["x"], b["y"], b["rot"], b["sx"], b["sy"]]
        if b["inherit"]:
            g[2] = _goc(Wc[b["name"]]) - _goc(Wc[cha])
        goc0[b["name"]] = g
        if b["name"] == "bone6":                     # chuỗi thân sang cha mới fly_sau (trùng chỗ `bone`, xương tĩnh của họ)
            sk.xuong("fly_sau", "root", float(Wb[0, 2]), float(Wb[1, 2]), goc=_goc(Wb))
            cha = "fly_sau"
        kd = TI_NON.get(b["name"], 1.0) if NON else 1.0
        sk.xuong(b["name"], "move" if cha == "root" else cha, g[0], g[1], goc=g[2], dai=b["len"], sx=g[3] * kd, sy=g[4] * kd,
                 khong_ti_le=b["inherit"] in (3, 4))
    by = {a["slot"]: a for a in D["atts"]}
    by0 = {a["slot"]: a for a in D0["atts"]}
    goc_slots = [s["name"] for s in I["slots"] if s["name"] not in BO_SLOT and s["name"] in by and by[s["name"]].get("region")]
    # thứ tự vẽ: cụm đầu xếp lại, chèn ngay sau slot thân cuối cùng của họ
    thu_tu = [s for s in goc_slots if s not in DAU_THU_TU]
    i_than = max(i for i, s in enumerate(thu_tu) if s.startswith("P_bozi"))
    thu_tu = thu_tu[:i_than + 1] + [s for s in DAU_THU_TU if s in goc_slots] + thu_tu[i_than + 1:]
    # các slot của CON SÂU (mọi trọng số trên chuỗi thân bone6..) xếp LIỀN nhau: mặt nạ đất chỉ phủ con sâu (đi theo nó tới chỗ đối thủ ở
    # chiêu cuối), tổ phiến đá ở nhà không bao giờ bị cắt. Slot tổ nằm lọt giữa (P_chuxu_10, P_shitou_04) dời ra trước con sâu.
    con = {}
    for b in IB:
        if b["parent"] >= 0:
            con.setdefault(ten[b["parent"]], []).append(b["name"])
    sau_bones, st = set(), ["bone6"]
    while st:
        x = st.pop()
        sau_bones.add(x)
        st += con.get(x, [])
    la_sau = lambda s_: all(ten[k] in sau_bones for ws in by[NGUON.get(s_, s_)]["w"] for k, _ in ws)
    iw = [i for i, s_ in enumerate(thu_tu) if la_sau(s_)]
    giua = [s_ for s_ in thu_tu[iw[0]:iw[-1] + 1] if not la_sau(s_)]
    thu_tu = thu_tu[:iw[0]] + giua + [s_ for s_ in thu_tu[iw[0]:iw[-1] + 1] if la_sau(s_)] + thu_tu[iw[-1] + 1:]
    sau_dau, sau_cuoi = next(s_ for s_ in thu_tu if la_sau(s_)), [s_ for s_ in thu_tu if la_sau(s_)][-1]
    sk.xuong("fly_dat", "root")
    s_px, c2w = concept_tg()
    DAT = {} if GOC else json.load(open(os.path.join(CUNG, "dat.json"), encoding="utf-8"))
    tong = [0, 0]
    VG = {}
    for s in thu_tu:
        a = by[s]
        r = a["region"]
        if s == sau_dau:
            sk.slot("cat_dat", "fly_dat")
        sk.slot(s, "move", r if (GOC or s not in CUNG_SLOT) else CUNG_SLOT[s])
        if GOC or s not in CUNG_SLOT:
            if r not in sk.images:
                sk.anh(r, anh_part(a))
            L = gan_nguyen(sk, s, r, a, ten, Wc)
        else:
            k = CUNG_SLOT[s]
            g = Image.open(os.path.join(CUNG, k + ".png")).convert("RGBA")
            kq = D_PX / s_px
            g2 = anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA"))
            sk.anh(k, g2)
            L = luoi.luoi_vung(g2, buoc_vien=10.0, buoc_trong=14.0, ten=k, in_tk=False)
            x0, y0, _, _ = DAT[k]["hop"]
            Ppx = np.array(L.pts, float) / kq + np.array([x0, y0])          # px ảnh mảnh → px concept
            ng = NGUON.get(s, s)
            VG[s] = gan_theo_goc(sk, s, k, L, c2w(Ppx), by[ng], ten, Wc, att_tu=by0[ng])
        tong[0] += L.n
        tong[1] += len(L.tris)
    if not GOC:
        # vành miệng co giãn: đầu + hàm + lòng miệng chung một trường trọng số sọ / hàm quanh nửa trước miệng
        hm, he = DAT["mieng"]["hop"], DAT["mat"]["hop"]
        tam = ve_dang_goc(c2w(np.array([[(hm[0] + hm[2]) / 2, (hm[1] + hm[3]) / 2]])), by["P_xiae_02"], by0["P_xiae_02"])[0]
        mat = ve_dang_goc(c2w(np.array([[(he[0] + he[2]) / 2, (he[1] + he[3]) / 2]])), by["P_shange"], by0["P_shange"])[0]
        vanh_mem(sk, Wc, {q: VG[q] for q in ("P_shange", "P_xiae_01", "P_xiae_02") if q in VG}, tam, mat, 0.42 * (hm[2] - hm[0]) / s_px)
        lot = them_lot(sk, by, [s for s in thu_tu if s.startswith("P_bozi")], ten, Wc)
        tong[0] += lot.n
        tong[1] += len(lot.tris)
    # mặt nạ đất: chỉ các slot của con sâu, bám `fly_dat` (game dời cùng quãng với fly_sau → ở chỗ đối thủ cắt theo mặt đất của nó)
    sk.cat("cat_dat", sau_cuoi, [(-6000, DAT_Y), (9000, DAT_Y), (9000, 6000), (-6000, 6000)])
    # điểm phụ
    Vm = np.array(by["P_xiae_02"]["xy"], float).reshape(-1, 2)
    m0 = Vm.mean(0) if GOC else c2w(np.array([[983.0, 556.0]]))[0]
    lp = np.linalg.solve(Wc["bone12"], np.array([m0[0], m0[1], 1.0]))
    sk.xuong("mieng", "bone12", float(lp[0]), float(lp[1]), goc=-_goc(Wc["bone12"]))
    # far ở 45 % chiều cao dáng đứng (1 126): game nhắm GIỮA THÂN đối thủ (StageView.Body = chân − 0,45 chiều cao), nên đối thủ cùng cỡ thì
    # độ dời dọc của fly_sau / fly_dat = 0 → sâu trồi đúng ở mặt đất dưới chân nó
    sk.xuong("far", "root", 1850.0, 0.45 * 1126.0)
    for e, m in (("nut", "appear: đất nứt dưới chân"), ("troi", "sâu phá đất trồi lên (appear / skill)"), ("gam", "gầm: bụi, rung"),
                 ("lao", "attack: lao đầu"), ("trung", "khung trúng"), ("vuon", "cast: vươn cao"), ("nen", "cast: giáng đầu xuống đất"),
                 ("gai", "cast: gai đá trồi dưới chân đối thủ"), ("lan", "skill: lặn xuống đất"), ("ngam", "skill: gò đất chạy ngầm tới đối thủ"),
                 ("can", "skill: đớp khép hàm"), ("ve", "skill: trồi lại ở chỗ cũ")):
        sk.su_kien(e, m)
    info = dict(scan=scan, IB=IB, ten=ten, goc0=goc0, slots=[s["name"] for s in I["slots"]])
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác")
    return sk, info


# ---------------------------------------------------------------- chuyển động
def chuyen_dong(sk, info):
    S = json.load(open(os.path.join(info["scan"], "sample.json"), encoding="utf-8"))
    IB, ten, goc0 = info["IB"], info["ten"], info["goc0"]
    ids = [i for i, n in enumerate(ten) if n in sk.bi and n != "root"]
    out, ref = {}, None
    for clip in ["idle_01"] + [c for c in S if c != "idle_01"]:
        fr = S[clip]["frames"]
        L = np.array([F["l"] for F in fr], float)
        Wm = np.array([F["m"] for F in fr], float)
        res = {}
        for i in ids:
            g = goc0[ten[i]]
            rot = L[:, i, 2]
            if IB[i]["inherit"]:
                p = IB[i]["parent"]
                rot = np.degrees(np.arctan2(Wm[:, i, 2], Wm[:, i, 0]) - np.arctan2(Wm[:, p, 2], Wm[:, p, 0]))
            A = np.stack([rot - g[2], L[:, i, 0] - g[0], L[:, i, 1] - g[1], L[:, i, 3] / (g[3] or 1.0), L[:, i, 4] / (g[4] or 1.0)], 1)
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            moc = ref[ten[i]][0, 0] if ref is not None and ten[i] in ref else 0.0
            A[:, 0] -= 360.0 * round((A[0, 0] - moc) / 360.0)
            res[ten[i]] = A
        for (c_, k0, k1) in LAM_MUOT:                                 # khoá giật của chính clip gốc: nội suy đều qua đoạn đó
            if c_ == clip:
                for A in res.values():
                    for k in range(k0 + 1, k1):
                        w = (k - k0) / (k1 - k0)
                        A[k] = A[k0] * (1 - w) + A[k1] * w
        if ref is None:
            ref = res
        out[clip] = (float(S[clip]["dur"]), res)
    return out


# skill_03 của họ: khung 17 → 20 (0,57–0,67 s) đầu quay NGƯỢC chiều rồi bật 121° trong MỘT khung (soi 2026-11-17: góc thế giới bone16
# −56, −71, −87, +34). Họ chắc che bằng hiệu ứng; mình trồi đầu lên đúng lúc đó (appear, skill) → thay bằng nội suy đều khung 17 → 20.
# (skill_01, skill_02 có cổ quay ~50°/khung trong 2–3 khung liền: cú đánh nhanh thật, giữ.)
LAM_MUOT = [("skill_03", 17, 20)]


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
    if t <= moc[0][0]:
        return moc[0][1]
    for a, b in zip(moc, moc[1:]):
        if t <= b[0]:
            u = (t - a[0]) / max(1e-9, b[0] - a[0])
            return a[1] + (b[1] - a[1]) * ease(u, b[2] if len(b) > 2 else "lin")
    return moc[-1][1]


def bat(t, t0, t1, vuot=0.12):
    """0 → 1 trong [t0, t1] có vượt nhẹ (bật lên rồi nảy về)."""
    if t <= t0:
        return 0.0
    if t >= t1 + 0.18:
        return 1.0
    if t <= t1:
        u = (t - t0) / (t1 - t0)
        return (1 + vuot) * (1 - (1 - u) ** 3)
    u = (t - t1) / 0.18
    return 1 + vuot * (1 - ease(u))


# giờ của mình → giờ clip nguồn
# đánh thường bản epic (người dùng 2026-11-17 "làm epic hơn"): lấy đà dài, phóng nhanh, đớp + khựng, lắc nghiến, bật về
M_ATTACK = [(0.0, 0.0), (0.42, 0.30, "io"), (0.54, 0.34, "lin"), (0.65, 0.56, "in"), (1.00, 0.62, "lin"), (1.52, 1.233, "io")]
A_LAO, A_TRUNG, A_NGHIEN, A_HET = 0.54, 0.65, 0.75, 1.00   # cú phóng 0,11 s (0,08 s nén cú đánh nhanh của họ gần 3 lần: cổ quay 118°/khung)
RAU_GOC = ("bone155", "bone156", "bone157", "bone158", "bone159", "bone160", "bone161", "bone162", "bone163", "bone164")
# chiêu cuối bản epic: gầm → lặn cắm đầu → chạy ngầm → phá đất há ngửa nuốt, treo → giáng ngoạm, lắc nghiến → lặn về → trồi ở nhà, gầm
S_GAM, S_LAN_A, S_LAN_B, S_DI = 0.32, 0.50, 0.80, 1.25
S_TROI, S_TREO, S_CAN, S_NGHIEN = 1.42, 1.55, 1.62, 1.72
S_LAN2A, S_LAN2B, S_VE0, S_VE1, S_GAM2 = 1.98, 2.25, 2.35, 2.70, 2.72
D_SKILL2 = 3.45
CHON_XA = 240.0                          # chiêu cuối: độ lún thêm khi trồi ở chỗ đối thủ
LECH_XA = 340.0                          # chiêu cuối: chỗ trồi lùi về phía mình so với đích far
M_CAST = [(0.0, 0.0), (0.70, 0.74, "io"), (0.92, 0.93, "lin"), (1.06, 1.11, "in"), (1.40, 1.30, "out"), (1.85, 1.667, "io")]
M_APPEAR = [(0.0, 0.44), (0.50, 0.44), (1.05, 0.95, "out"), (1.55, 1.40, "lin"), (2.10, 2.0, "io")]
T_LAN0, T_LAN1 = 0.30, 0.62               # skill: lặn xuống
T_DI1 = 1.02                              # tới dưới chân đối thủ
T_TROI1 = 1.22                            # trồi hết
T_CAN = 1.34                              # đớp
T_LAN2A, T_LAN2B = 1.62, 1.90             # lặn lại
T_VE0, T_VE1 = 1.96, 2.30                 # trồi lại chỗ cũ
D_SKILL = 2.75


def lam_clip(sk, info, cao=1150.0):
    CD = chuyen_dong(sk, info)
    far_x = sk.bones[sk.bi["far"]]["x"]
    xa_x = far_x - LECH_XA                # chiêu cuối: trồi lùi về phía mình 0,3 chiều cao (đầu gập tới ~0,48 chiều cao khi ngoạm → rơi trúng đối thủ)

    def dat(P, goc, tau, lap=False):
        dur, R = CD[goc]
        n = len(next(iter(R.values())))
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

    def dam(P, a, chi=None):
        for sl in sk.slots:
            if sl["name"] == "cat_dat" or (chi is not None and sl["name"] not in chi):
                continue
            P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])

    def rung(t, t0, t1, bien):
        if t0 <= t <= t1:
            k = int((t - t0) * FPS) // 2
            return bien * (1 if k % 2 == 0 else -1) * min(1.0, (t1 - t) / 0.12)
        return 0.0

    def mo_ham(P, goc):                                               # cộng thêm vào độ há của clip gốc (họ đã mở tới 38°)
        P.rot("bone13", goc)

    def f_idle(t, P):
        dat(P, "idle_01", t, True)
        if 1.05 < t < 1.75:                                           # trò riêng: há miệng "nếm" không khí hai nhịp ngắn
            u = (t - 1.05) / 0.70
            mo_ham(P, -9.0 * math.sin(math.pi * u) * (0.6 + 0.4 * math.cos(4 * math.pi * u)))

    def f_walk(t, P):
        dat(P, "run_01", t, True)

    def f_hit(t, P):
        dat(P, "hit_01", t)

    def f_die(t, P):
        d = CD["die_01"][0]
        dat(P, "die_01", min(t, d))
        u = ease((t - (d - 0.35)) / (TAN + 0.35), "in")             # thân chìm xuống đất, phiến và đế mờ đi
        P.move("fly_sau", 0.0, -0.75 * SAU_SAU * u)
        a = float(np.clip(1.0 - (t - d) / TAN, 0.0, 1.0))
        dam(P, a)

    def pha(P, a, b, w):
        """dáng = trộn hai dáng clip nguồn a = (clip, giờ), b = (clip, giờ) theo w (0 → a, 1 → b), cộng vào P."""
        Pa, Pb = khung.Pose(), khung.Pose()
        dat(Pa, *a)
        dat(Pb, *b)
        for bn in set(Pa.t) | set(Pb.t):
            ga = Pa.t.get(bn, [0.0, 0.0, 0.0, 1.0, 1.0])
            gb = Pb.t.get(bn, [0.0, 0.0, 0.0, 1.0, 1.0])
            g = [ga[q] * (1 - w) + gb[q] * w for q in range(5)]
            P.rot(bn, g[2])
            P.move(bn, g[0], g[1])
            P.scale(bn, g[3], g[4])

    def rau_vut(P, goc):
        for k, bn in enumerate(RAU_GOC):
            P.rot(bn, goc * (0.8 + 0.4 * ((k * 37) % 10) / 10.0))

    def lac(t, t0, t1, bien, chu_ky=0.16):
        """lắc nghiến: dao động tắt dần trong [t0, t1]."""
        if not t0 <= t <= t1:
            return 0.0
        u = (t - t0) / (t1 - t0)
        return bien * math.sin(2 * math.pi * (t - t0) / chu_ky) * (1 - u) ** 1.5

    def f_attack(t, P):
        dat(P, "skill_01", tmap(t, M_ATTACK))
        # thân: ngả ra sau lấy đà (giữ căng), phóng chúi tới, giữ lúc nghiến, bật về có vượt
        if t < A_LAO:
            c = ease(t / 0.42)
            xoay, dx = 7.0 * c, -35.0 * c
        elif t < A_TRUNG:
            u = ease((t - A_LAO) / (A_TRUNG - A_LAO), "in")
            xoay, dx = 7.0 - 16.0 * u, -35.0 + 85.0 * u
        elif t < A_HET:
            xoay, dx = -9.0, 50.0
        else:
            u = (t - A_HET) / (M_ATTACK[-1][0] - A_HET)
            xoay = -9.0 * (1 - ease(u)) + 3.0 * math.sin(math.pi * min(1.0, u * 1.6)) * (1 - u)
            dx = 50.0 * (1 - ease(u))
        P.rot("fly_sau", xoay)
        P.move("fly_sau", dx, 0.0)
        if 0.42 < t < A_LAO:                                          # gồng căng trước khi phóng
            P.rot("bone16", 1.5 * math.sin((t - 0.42) * 2 * math.pi / 0.04))
        # hàm: há dần thật rộng khi lấy đà, ĐỚP sập lúc trúng, ngậm chặt khi nghiến
        if t < A_LAO:
            ham = -16.0 * ease((t - 0.18) / 0.34)
        elif t < A_TRUNG:
            ham = -16.0 + 21.0 * ease((t - A_LAO) / (A_TRUNG - A_LAO), "in")
        else:
            ham = 5.0 * (1 - ease((t - A_HET) / 0.2)) if t > A_HET else 5.0
        mo_ham(P, ham)
        # râu xoè ra sau khi lấy đà, quất tới khi phóng (trễ 0,04 s)
        rau_vut(P, -18.0 * ease(t / 0.45) * (1 - ease((t - 0.58) / 0.08)) + 22.0 * math.exp(-((t - 0.68) / 0.10) ** 2))
        # lắc nghiến hai nhịp + rung
        P.rot("bone16", lac(t, A_TRUNG + 0.02, A_HET, 11.0))
        P.rot("bone11", lac(t, A_TRUNG + 0.02, A_HET, -5.0))
        P.move("move", rung(t, A_TRUNG, A_TRUNG + 0.32, 9.0), 0.0)
        k = math.exp(-((t - A_TRUNG) / 0.035) ** 2)
        P.scale("move", 1 + 0.03 * k, 1 - 0.035 * k)

    def f_cast(t, P):
        dat(P, "skill_02", tmap(t, M_CAST))
        mo_ham(P, -6.0 * math.exp(-((t - 0.80) / 0.16) ** 2))
        P.move("move", rung(t, 1.06, 1.30, 7.0), 0.0)
        g = math.exp(-((t - 1.08) / 0.05) ** 2)
        P.scale("move", 1 + 0.02 * g, 1 - 0.03 * g)

    def f_skill(t, P):
        """bản epic: gầm → lặn cắm đầu chéo xuống → chạy ngầm → phá đất dưới chân đối thủ, vươn dài há ngửa như nuốt, treo một nhịp →
        giáng đầu ngoạm, rung, lắc nghiến → lặn về → trồi ở nhà, gầm lần nữa."""
        # 1) ngửa cổ gầm
        if t < S_LAN_A:
            dat(P, "skill_03", tmap(t, [(0.0, 0.0), (0.30, 0.67, "io"), (S_LAN_A, 0.75, "lin")]))
            mo_ham(P, -10.0 * math.sin(math.pi * min(1.0, max(0.0, (t - 0.16) / 0.32))))
            P.move("move", rung(t, S_GAM, S_LAN_A - 0.02, 6.0), 0.0)
            rau_vut(P, -15.0 * ease(t / 0.3))
            return
        # 2) lặn CẮM ĐẦU chéo xuống (như cá heo lao): đầu chúi xuống, cả con trượt tới và chìm
        if t < S_LAN_B:
            u = (t - S_LAN_A) / (S_LAN_B - S_LAN_A)
            pha(P, ("skill_03", 0.75), ("skill_02", 1.11), ease(min(1.0, u * 2.0)))
            e = ease(u, "in")
            P.move("fly_sau", 140.0 * e, -SAU_SAU * e)
            P.rot("fly_sau", -35.0 * e)
            rau_vut(P, -15.0 + 25.0 * ease(u))
            return
        # 3) chạy ngầm tới dưới chân đối thủ (ẩn dưới đất)
        if t < S_DI:
            u = ease((t - S_LAN_B) / (S_DI - S_LAN_B), "io")
            pha(P, ("skill_02", 1.11), ("skill_03", 0.75), u)          # đổi dáng dần trong lúc ẩn, tới thế ĐÃ NGÓC ĐẦU (skill_03 0,62–0,68 đầu quay rất nhanh: 116°/khung khi vừa ló)
            P.move("fly_sau", 140.0 + (xa_x - 140.0) * u, -SAU_SAU)
            P.rot("fly_sau", -35.0 * (1 - u))
            return
        # 4) PHÁ ĐẤT dưới chân đối thủ: vươn dài, ngửa đầu há rộng (nuốt), treo một nhịp, giáng ngoạm, lắc nghiến
        if t < S_LAN2B:
            if t < S_TREO:
                dat(P, "skill_03", tmap(t, [(S_DI, 0.75), (S_TROI, 0.95, "io")]))
            elif t < S_CAN:
                pha(P, ("skill_03", 0.95), ("skill_02", 1.11), ease((t - S_TREO) / (S_CAN - S_TREO), "in"))
            elif t < S_LAN2A:
                dat(P, "skill_02", tmap(t, [(S_CAN, 1.11), (S_LAN2A, 1.22, "lin")]))
            else:                                                     # đang chìm: hoà dần sang dáng thụt của phần sau (không nhảy dáng ở S_LAN2B)
                pha(P, ("skill_02", 1.22), ("skill_03", 0.44), ease((t - S_LAN2A) / (S_LAN2B - S_LAN2A)))
            # ở chỗ đối thủ không có tổ đá che chân: lún thêm CHON_XA để ĐÁY THÂN luôn dưới mặt nạ đất (đáy thân có lúc cao hơn đất 207 đơn vị)
            y = -CHON_XA - (SAU_SAU - CHON_XA) * (1 - bat(t, S_DI, S_TROI, 0.05))
            if t > S_LAN2A:
                y = -CHON_XA - (SAU_SAU - CHON_XA) * ease((t - S_LAN2A) / (S_LAN2B - S_LAN2A), "in")
            P.move("fly_sau", xa_x, y)
            if t > S_LAN2A:
                P.rot("fly_sau", -25.0 * ease((t - S_LAN2A) / (S_LAN2B - S_LAN2A), "in"))
            g = math.sin(math.pi * min(1.0, max(0.0, (t - S_DI) / (S_TREO + 0.05 - S_DI))))       # vươn dài khi phóng lên
            P.scale("fly_sau", 1 - 0.07 * g, 1 + 0.12 * g)
            if t < S_TREO:
                ham = -16.0 * ease((t - S_DI) / 0.15)
            elif t < S_CAN:
                ham = -16.0 + 21.0 * ease((t - S_TREO) / (S_CAN - S_TREO), "in")
            else:
                ham = 5.0
            mo_ham(P, ham)
            if S_TROI < t < S_TREO + 0.03:                             # treo: run run trước khi giáng
                P.rot("bone16", 1.2 * math.sin((t - S_TROI) * 2 * math.pi / 0.045))
            P.rot("bone16", lac(t, S_CAN + 0.03, S_LAN2A, 12.0, 0.17))
            P.rot("bone11", lac(t, S_CAN + 0.03, S_LAN2A, -6.0, 0.17))
            P.move("move", rung(t, S_CAN - 0.01, S_LAN2A, 12.0), 0.0)
            k = math.exp(-((t - S_CAN) / 0.04) ** 2)
            P.scale("move", 1 + 0.035 * k, 1 - 0.04 * k)
            rau_vut(P, -18.0 * g + 24.0 * math.exp(-((t - S_CAN - 0.05) / 0.1) ** 2))
            return
        # 5) về dưới đất (ẩn), trồi ở nhà và gầm
        if t < S_VE0:
            dat(P, "skill_03", 0.44)
            P.move("fly_sau", 0.0, -SAU_SAU)
            return
        dat(P, "skill_03", tmap(t, [(S_VE0, 0.44), (S_VE1, 0.95, "io"), (3.0, 1.10, "lin"), (D_SKILL2, 2.0, "io")]))
        P.move("fly_sau", 0.0, -SAU_SAU * (1 - bat(t, S_VE0, S_VE1, 0.06)))
        if S_GAM2 < t < 2.98:
            mo_ham(P, -10.0 * math.sin(math.pi * (t - S_GAM2) / (2.98 - S_GAM2)))
            P.move("move", rung(t, S_GAM2, 2.96, 6.0), 0.0)

    def f_skill_cu(t, P):
        # bản đầu (giữ để so): thụt vào kén rồi LẶN thẳng, trồi, đớp, lặn lại, trồi về
        if t < T_LAN1:
            dat(P, "skill_03", tmap(t, [(0.0, 0.0), (T_LAN0, 0.40, "io"), (T_LAN1, 0.44, "lin")]))
            u = ease((t - T_LAN0) / (T_LAN1 - T_LAN0), "in") if t > T_LAN0 else 0.0
            P.move("fly_sau", 0.0, -SAU_SAU * u)
            P.rot("fly_sau", -10.0 * u)
            return
        # 2) chạy ngầm tới dưới chân đối thủ (ẩn dưới đất)
        if t < T_DI1:
            dat(P, "skill_03", 0.44)
            u = ease((t - T_LAN1) / (T_DI1 - T_LAN1), "io")
            P.move("fly_sau", far_x * u, -SAU_SAU)
            return
        # 3) trồi lên dưới chân đối thủ, há to, ĐỚP, lặn lại
        if t < T_LAN2B:
            tau = tmap(t, [(T_DI1, 0.30), (T_TROI1, 0.62, "out"), (T_CAN, 0.74, "lin"), (T_LAN2A, 0.93, "lin"), (T_LAN2B, 1.00, "in")])
            dat(P, "skill_02", tau)
            y = -SAU_SAU * (1 - bat(t, T_DI1, T_TROI1, 0.06))
            if t > T_LAN2A:
                y = -SAU_SAU * ease((t - T_LAN2A) / (T_LAN2B - T_LAN2A), "in")
            P.move("fly_sau", far_x, y)
            mo_ham(P, -12.0 * (1 - ease((t - (T_CAN - 0.06)) / 0.06)) if t < T_CAN else 4.0 * math.exp(-((t - T_CAN - 0.03) / 0.05) ** 2))
            P.move("move", rung(t, T_CAN - 0.02, T_CAN + 0.22, 8.0), 0.0)
            return
        # 4) trở về dưới đất, trồi lại ở chỗ cũ (như appear, nhanh)
        if t < T_VE0:
            dat(P, "skill_03", 0.44)
            P.move("fly_sau", 0.0, -SAU_SAU)
            return
        dat(P, "skill_03", tmap(t, [(T_VE0, 0.44), (T_VE1, 0.95, "out"), (D_SKILL, 2.0, "io")]))
        P.move("fly_sau", 0.0, -SAU_SAU * (1 - bat(t, T_VE0, T_VE1, 0.05)))

    def f_appear(t, P):
        dat(P, "skill_03", tmap(t, M_APPEAR))
        for k, b in enumerate(DE):                                    # đế đá trồi trước
            s = max(0.02, bat(t, 0.02 + 0.03 * k, 0.20 + 0.03 * k))
            P.scale(b, s, s)
        for k, b in enumerate(PHIEN):                                 # năm phiến đâm lên lệch nhịp
            s = max(0.02, bat(t, 0.12 + 0.07 * k, 0.34 + 0.07 * k, 0.14))
            P.scale(b, s, s)
        for k, b in enumerate(TANG):
            s = max(0.02, bat(t, 0.30 + 0.05 * k, 0.48 + 0.05 * k, 0.12))
            P.scale(b, s, s)
        for k, b in enumerate(TUA):                                   # tua mọc ra
            s = max(0.02, bat(t, 0.55 + 0.035 * k, 0.78 + 0.035 * k, 0.1))
            P.scale(b, s, s)
        P.move("fly_sau", 0.0, -SAU_SAU * (1 - bat(t, 0.50, 0.88, 0.07)))   # sâu phá đất vọt lên
        if 1.05 < t < 1.60:
            mo_ham(P, -8.0 * math.sin(math.pi * (t - 1.05) / 0.55))
            P.move("move", rung(t, 1.08, 1.55, 6.0), 0.0)
        dam(P, min(1.0, t * FPS / 2.0))

    ev_skill = [(S_GAM, "gam", ""), (S_LAN_A, "lan", ""), (S_LAN_B, "ngam", ""), (S_DI, "troi", ""), (S_CAN, "can", ""),
                (S_CAN, "trung", ""), (S_NGHIEN, "nghien", ""), (S_LAN2A, "lan", ""), (S_VE0, "ve", ""), (S_GAM2, "gam", "")]

    def theo_dat(fn):
        """mặt nạ đất (fly_dat) dời ngang ĐÚNG như fly_sau: game co quãng hai xương fly* bằng nhau → mặt đất của mặt nạ luôn dưới con sâu."""
        def g(t, P):
            fn(t, P)
            dx = P.t.get("fly_sau", [0.0])[0]
            if abs(dx) > 1e-6:
                P.move("fly_dat", dx, 0.0)
        return g

    f_attack, f_skill, f_die, f_appear = theo_dat(f_attack), theo_dat(f_skill), theo_dat(f_die), theo_dat(f_appear)
    return [
        Clip("appear", M_APPEAR[-1][0], f_appear, ev=[(0.02, "nut", ""), (0.50, "troi", ""), (1.08, "gam", "")]),
        Clip("idle", CD["idle_01"][0], f_idle, loop=True),
        Clip("walk", CD["run_01"][0], f_walk, loop=True),
        Clip("attack", M_ATTACK[-1][0], f_attack, ev=[(A_LAO, "lao", ""), (A_TRUNG, "trung", ""), (A_NGHIEN, "nghien", "")],
             trung=A_TRUNG),
        Clip("cast", M_CAST[-1][0], f_cast, ev=[(0.20, "vuon", ""), (1.06, "nen", ""), (1.14, "gai", ""), (1.20, "trung", "")]),
        Clip("skill", D_SKILL2, f_skill, ev=ev_skill, trung=S_CAN),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", CD["die_01"][0] + TAN, f_die),
    ]


def main(a):
    sk, info = dung()
    ve0 = soi.Ve(sk)
    clips = lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0, RAU)
    clips = lam_clip(sk, info, cao)
    print(f"chiều cao (không tính râu) {cao:.0f}")
    ra = os.environ.get("SD_RA") or (os.path.join(HERE, "inbox", "sau_dat_non", "rig") if NON else os.path.join(G.BASE, "rig_goc" if GOC else "rig"))
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
        sc = float(a[3]) if len(a) > 3 else 0.25
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
    xuat.xuat_het(sk, clips, ra, TEN_RIG, "Sâu đất khổng lồ (sau_dat): tướng 7 đảo Thổ" + (" — DA GỐC, chỉ để soi clip" if GOC else
                  " — dạng 1 Sa Trùng Nhi" if NON else ""),
                  dang=1 if NON else 2, so_dang=2, dung_yen=("cast", "skill"), lao=(), far=("cast", "skill"), ma_goc=None, khop_idle=0.2,
                  cao=cao, impact=IMPACT, tol={"rotate": 0.08, "translate": 0.2, "scale": 0.0015}, dich_mb=0.6, tran_mb=1.0, span=7.0)


if __name__ == "__main__":
    main(sys.argv[1:])
