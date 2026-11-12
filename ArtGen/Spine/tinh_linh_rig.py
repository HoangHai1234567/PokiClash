# -*- coding: utf-8 -*-
"""Tinh linh rừng mập dạng 1 (tinh_linh_1, hướng "mầm hai lá"): hình của mình chạy trên rig của con gốc monster_3407.
Ghi chú: inbox/tinh_linh_ghichu.md.

- XƯƠNG của họ (giữ): bone > bone2 > bone3 (thân) > hai tay bone5-7 / bone8-10, hai góc đáy bụng bone11 / bone12 (IK đã nướng), bone15
  (gốc thứ trong bụng); bone2 > bone43 > bone44 > bone4 (đầu) > bone13 (mắt), bone14 (gốc tóc). bone4 của họ "chỉ thừa hưởng độ dời":
  rig mình thừa hưởng thường, nên góc riêng của bone4 trừ đi tổng góc các xương cha (cha không co giãn nên tương đương).
  BỎ: mọi chuỗi lá / dây leo / mầm cây / lá trôi của họ (hình đó không dùng).
- LƯỚI của họ (nguyên đỉnh, tam giác, uv, trọng số): bụng P_shentiB, đầu P_tou2B, tay trước P_shouRB, tay sau P_shouLB; sáu bộ mắt là
  sáu ô chữ nhật đúng khung part trên bone13 (bật bằng độ đậm).
- MẢNH RIÊNG của mình: tóc (mầm hai lá: một lưới, cuống + vòng lá bám toc_goc, mỗi lá một chuỗi 3 đốt có lò xo, lắc theo góc chuỗi
  lá bone39.. / dây leo bone49.. của họ); cụm hạt giống (xương hat, con của bone15, lắc theo bone16); ba bong bóng (con của bone3,
  trôi nhẹ); MỒM tròn (xương mieng, con của bone4; ẩn, chỉ hiện lúc bắn chiêu, cũng là chỗ nhả lá cho VFX).
- CHUYỂN ĐỘNG: mẫu 30 khung/giây của runtime Spine (biến đổi riêng ĐÃ áp IK) từ clip dựng ở tầng điều khiển (tinh_linh_clip.py →
  scan/sample_moi.json); cung lao / rơi (kenh_rieng.json) đặt lên xương move.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tinh_linh_rig.py          → inbox/tinh_linh_1/rig/ (xem.html, khung_*.png)
    py -3 -I ArtGen/Spine/tinh_linh_rig.py soi <clip> <giây,giây,...> [tỉ lệ]                   → rig/soi_<clip>.png (khung lớn nền xám)
"""
import json
import math
import os
import pickle
import subprocess
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, luoi, trongso, khung, hoat, xuat, soi, tienhoa  # noqa: E402
from quai.khung import Dat  # noqa: E402
from quai.hoat import Clip, LoXo  # noqa: E402
import tinh_linh as TL  # noqa: E402
import tinh_linh_manh as TM  # noqa: E402

TEN = f"tinh_linh_{TL.K}"
RA = os.path.join(TL.BASE, "rig")
KG = 0.46                    # đơn vị rig con gốc → đơn vị rig của mình
PXU = 0.62                   # pixel ảnh atlas cho mỗi đơn vị rig con gốc (atlas của họ: 0,5)
GIU = ["bone", "bone2", "bone3", "bone43", "bone44", "bone4", "bone5", "bone6", "bone7", "bone8", "bone9", "bone10", "bone11", "bone12",
       "bone13", "bone14", "bone15"]
MAT = {f"P_SL_bq{i}": f"mat{i}" for i in range(1, 7)}
CLIPS = [("appear", "tl_appear", False), ("idle", "tl_idle", True), ("walk", "tl_walk", True), ("attack", "tl_attack", False),
         ("cast", "tl_cast", False), ("skill", "tl_skill", False), ("hit", "tl_hit", False), ("die", "tl_die", False)]
TAN = 0.45                   # die: giữ dáng cuối rồi mờ dần chừng này giây
# khớp của tóc, đọc trên concept (px khung concept): gốc cuống (giữa vòng lá), rồi dọc gân từng lá từ đỉnh cuống ra ngọn
J_GOC = (792.0, 300.0)
CHUOI = {"la_trai": [(786.0, 212.0), (680.0, 160.0), (560.0, 166.0), (440.0, 236.0)],
         "la_phai": [(806.0, 214.0), (856.0, 136.0), (936.0, 100.0), (1042.0, 88.0)]}
Y_VONG, R_VONG = 250.0, 128.0   # dưới mức Y_VONG (px concept) và cách gốc cuống dưới R_VONG theo x là cuống + vòng lá: bám cứng toc_goc
LO_XO = {"la_trai": ((300, 240, 190), 7.0), "la_phai": ((320, 260, 200), 7.0)}      # chuỗi: (độ cứng từng đốt, góc lệch tối đa)
CAO_TOC = 790.0              # đỉnh tóc ở dáng gốc (đơn vị con gốc), để tính chiều cao game
TIEU_DE = "Tinh linh rừng mập (tinh_linh) dạng 2: mầm hai lá"
DAU_TI = 1.0                 # phóng cả ĐẦU (xương bone4: đầu, mắt, mồm, tóc) quanh tâm đầu ở dáng gốc
MAT_TI, MAT_HA, MAT_TRAI = 1.0, 0.0, 0.0    # phóng thêm MẮT (xương bone13), hạ mắt xuống, dời mắt sang trái (đơn vị con gốc)
# nguồn lắc của mảnh riêng: xương mình ← (xương của họ, hệ số góc)
NGUON = {"la_trai0": ("bone39", 0.32), "la_trai1": ("bone39b", 0.36), "la_trai2": ("bone39c", 0.4),
         "la_phai0": ("bone49", 0.3), "la_phai1": ("bone49b", 0.32), "la_phai2": ("bone49c", 0.36), "hat": ("bone16", 0.6)}
CHA_BONE4 = ("bone", "bone2", "bone43", "bone44")
if TL.K == 1:
    # DẠNG 1 (hạt mầm): cùng rig, nhỏ hơn; tóc chỉ là MỘT mầm cong tí hon (một chuỗi 4 đốt: cuống lên, vòng qua đỉnh, lá rủ xuống)
    # người dùng 2026-11-12 (xem bản đầu KG 0,38, tỉ lệ y như dạng 2): "dạng 1 cho nhỏ hơn chút, chibi hơn, mặt cũng chibi hơn"
    KG = 0.34                # dạng 2: 0,46 → dạng 1 nhỏ bằng ~74%
    DAU_TI = 1.17            # đầu to hơn so với thân (chibi)
    MAT_TI, MAT_HA, MAT_TRAI = 1.24, 7.0, 14.0   # mắt to và thấp hơn trên mặt; dời trái cho mắt phải (to ra) không thò khỏi mép đầu
    J_GOC = (770.0, 298.0)
    CHUOI = {"mam": [(770.0, 292.0), (742.0, 200.0), (788.0, 128.0), (850.0, 150.0), (884.0, 238.0)]}
    Y_VONG, R_VONG = 284.0, 60.0
    LO_XO = {"mam": ((300, 250, 200, 160), 8.0)}
    NGUON = {"mam0": ("bone39", 0.3), "mam1": ("bone39b", 0.34), "mam2": ("bone39c", 0.4), "mam3": ("bone49c", 0.4), "hat": ("bone16", 0.6)}
    CAO_TOC = 717.0
    TIEU_DE = "Tinh linh rừng mập (tinh_linh) dạng 1: hạt mầm"
if TL.K == 3:
    # DẠNG 3 (nở hoa): cùng rig, to hơn; tóc = hai lá lớn + một bông hoa trên cuống (chuỗi `hoa`: cuống, nửa dưới hoa, nửa trên hoa)
    KG = 0.54                # người dùng 2026-11-12 (bản đầu 0,50, to hơn dạng 2 có 9%): "dạng 3 ổn, cho to hơn dạng 2 một chút" → to hơn ~18%
    J_GOC = (790.0, 308.0)
    CHUOI = {"la_trai": [(770.0, 262.0), (660.0, 200.0), (540.0, 215.0), (425.0, 300.0)],
             "la_phai": [(810.0, 262.0), (900.0, 195.0), (1000.0, 180.0), (1085.0, 215.0)],
             "hoa": [(790.0, 290.0), (790.0, 236.0), (786.0, 150.0), (786.0, 60.0)]}
    Y_VONG, R_VONG = 286.0, 128.0
    LO_XO = {"la_trai": ((300, 240, 190), 7.0), "la_phai": ((320, 260, 200), 7.0), "hoa": ((360, 300, 240), 5.0)}
    NGUON = dict(NGUON, hoa0=("bone49", 0.22), hoa1=("bone49b", 0.26), hoa2=("bone49c", 0.3))
    CAO_TOC = 793.0
    TIEU_DE = "Tinh linh rừng mập (tinh_linh) dạng 3: nở hoa"
SO_DANG = 3 if os.path.exists(os.path.join(HERE, "inbox", "tinh_linh_3", "manh", "dat.json")) else 2      # dạng 3 có mảnh rồi thì dòng có 3 dạng
E_NHUN, E_BAT, E_ROI, E_DUR = 0.42, 0.50, 1.02, 2.86      # tiến hóa: nhún tới E_NHUN, bật E_BAT, dạng sau bắt đầu rơi E_ROI (clip appear 1,8 s)
CAO_GAME = {1: 1.19, 3: 0.94}.get(TL.K, 1.0)    # game quy mỗi dạng về cùng chiều cao theo game.height rồi nhân `size` của heroes.json (0,9 / 1,02):
#                                          khai chiều cao dạng 1 lớn hơn thật 1,19 lần để trong game thân dạng 1 = 74% thân dạng 2 như ở rig;
#                                          dạng 3 khai nhỏ hơn thật (0,94) để trong game thân dạng 3 to hơn dạng 2 ~19% (để nguyên chỉ ~12%)
NHE = os.environ.get("TL_NHE") == "1"    # bản NHẸ (ảnh nhỏ, lưới thưa) của dạng 2, chỉ để gộp vào dạng 1 cho clip tiến hóa
if NHE:
    PXU *= 0.72
# LƯỚI DÀY (người dùng 2026-11-12: "chia mesh / đỉnh thêm nữa cho mềm mại hơn và bụng rung mượt hơn"): bước viền / bước trong (px atlas)
BUOC = {"bung": (7.0, 9.5), "dau": (7.0, 9.5), "tay_gan": (6.0, 8.0), "tay_xa": (6.0, 8.0)}
if os.environ.get("TL_NHE") == "1":           # bản nhẹ: lưới thưa
    BUOC = {k_: (v_[0] * 1.8, v_[1] * 1.8) for k_, v_ in BUOC.items()}
# xương "mỡ bụng" (con của bone3, có lò xo điểm): tên: (x, y tâm trong thế giới con gốc, bán kính ảnh hưởng, trọng số đỉnh, lệch tối đa)
MO = {"mo_g": (12.0, 150.0, 165.0, 0.62, 15.0), "mo_t": (-190.0, 118.0, 120.0, 0.55, 11.0), "mo_p": (188.0, 112.0, 120.0, 0.55, 11.0)}


class Nay:
    """xương NẢY (mỡ bụng): mỗi xương là một điểm khối lượng nối lò xo tới chỗ động học của nó trong thế giới; độ lệch (trễ, vọt quá,
    rung tắt dần) ghi thành độ dời của xương. hz: tần số riêng, zeta: giảm chấn, toi_da: {xương: lệch tối đa} (chặn mềm bằng tanh)."""

    def __init__(self, toi_da, hz=3.3, zeta=0.2, sub=4):
        self.bones, self.td, self.k, self.zeta, self.sub = list(toi_da), dict(toi_da), (2 * math.pi * hz) ** 2, zeta, sub

    def chay(self, sk, frames, ts, loop, fps):
        dt = 1.0 / fps / self.sub
        st = {}

        def step(P, record):
            W = sk.the_gioi(P)
            for b in self.bones:
                tg = W[b][:2, 2].copy()
                if b not in st:
                    st[b] = [tg.copy(), np.zeros(2), tg.copy()]
                p_, v_, tg0 = st[b]
                for q in range(self.sub):
                    tq = tg0 + (tg - tg0) * (q + 1) / self.sub
                    v_ = v_ + (self.k * (tq - p_) - 2 * self.zeta * math.sqrt(self.k) * v_) * dt
                    p_ = p_ + v_ * dt
                off = p_ - tg
                n_ = float(np.hypot(*off))
                m_ = self.td[b]
                if n_ > 1e-9:
                    off = off * (m_ * math.tanh(n_ / m_) / n_)
                    if n_ > 2.5 * m_:                        # lao / rơi quá nhanh: không để điểm tụt lại quá xa rồi quất về
                        p_ = tg + off * 2.5
                st[b] = [p_, v_, tg]
                if record:
                    cha = sk.bones[sk.bi[b]]["parent"]
                    d = np.linalg.solve(W[cha][:2, :2], off)
                    P.move(b, float(d[0]), float(d[1]))

        if loop:
            for _ in range(2):
                for P in frames[:-1]:
                    step(P.copy(), False)
        else:
            for _ in range(fps):
                step(frames[0].copy(), False)
        for P in frames:
            step(P, True)


def dung():
    scan = TL.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    assert ten == [b["name"] for b in D["bones"]]
    dat = json.load(open(os.path.join(TM.MANH, "dat.json"), encoding="utf-8"))

    sk = khung.Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")                     # game đo độ dời thân trên xương này (lao, rơi)
    for b in IB:
        if b["name"] not in GIU:
            continue
        cha = ten[b["parent"]]
        k_ = DAU_TI if b["name"] == "bone4" else MAT_TI if b["name"] == "bone13" else 1.0     # chibi: phóng đầu, phóng thêm mắt
        la_mat = b["name"] == "bone13"
        sk.xuong(b["name"], "move" if cha == "root" else cha, (b["x"] - (MAT_TRAI if la_mat else 0.0)) * KG, (b["y"] - (MAT_HA if la_mat else 0.0)) * KG,
                 goc=b["rot"], dai=b["len"] * KG, sx=b["sx"] * k_, sy=b["sy"] * k_)
    # ma trận thế giới dáng gốc ĐÃ ÁP RÀNG BUỘC của họ: điểm gắn lưới tính theo đây
    Wc = {b["name"]: np.array([[b["a"], b["b"], b["x"] * KG], [b["c"], b["d"], b["y"] * KG], [0.0, 0.0, 1.0]]) for b in D["bones"]}
    by = {a["att"]: a for a in D["atts"]}
    c4 = Wc["bone4"][:2, 2]
    dau_tg = lambda P_: c4 + DAU_TI * (np.asarray(P_, float) - c4)       # điểm thế giới thuộc đầu, sau khi đầu phóng DAU_TI lần   # noqa: E731
    tong = [0, 0]
    than = []

    def nho(g, k):
        g = g.convert("RGBa")
        return anh.loang_mau(g.resize((max(2, round(g.width * k)), max(2, round(g.height * k))), Image.LANCZOS).convert("RGBA"))

    def gan(slot, hinh, file, an=False, doi=None):
        """slot dùng nguyên lưới của họ (att `hinh`: lưới hoặc ô chữ nhật) với ảnh của mình (manh/<file>.png, cỡ ảnh vùng × Z)."""
        a = by[hinh]
        g = Image.open(os.path.join(TM.MANH, file + ".png"))
        sk.anh(slot, nho(g, 2.0 * PXU / TM.Z))
        im = sk.images[slot]
        uv, tris = TL.luoi(a)
        fw, fh = g.width / TM.Z, g.height / TM.Z            # khung ảnh vùng của họ (px)
        nh = a.get("hull", len(uv))
        L = luoi.Luoi(uv * np.array([im.width / fw, im.height / fh]), tris, nh, nh, im.width, im.height, ten=slot)
        V = np.array(a["xy"], float).reshape(-1, 2) * KG
        ws_ = a.get("w") or [[(ten.index(a["bone"]), 1.0)]] * len(V)
        if doi:                                              # đổi xương bám (tay: phần bám thân chuyển sang khúc tay đầu, xem dưới)
            ws_ = [[(ten.index(doi.get(ten[k], ten[k])), w) for k, w in ws] for ws in ws_]
        sk.slot(slot, "move", slot, an=an)
        sk.luoi_gan(slot, slot, L, trongso.cung(L.n, "move"), the_gioi=V)
        rows = []
        for p, ws in zip(V, ws_):
            row = [(ten[k], *[float(v) for v in (np.linalg.inv(Wc[ten[k]]) @ np.array([p[0], p[1], 1.0]))[:2]], float(w)) for k, w in ws if w > 0.002]
            assert all(r[0] in sk.bi for r in row), (slot, [r[0] for r in row])
            tot = sum(r[3] for r in row) or 1.0
            rows.append([(n, x, y, w / tot) for n, x, y, w in row])
        sk.atts[slot][slot]["verts"] = rows
        tong[0] += L.n
        tong[1] += len(L.tris)
        than.append(slot)

    def gan_day(slot, hinh, file, doi=None, mo=False):
        """như gan nhưng LƯỚI DÀY của mình trên cùng hình: mỗi đỉnh lấy trọng số nội suy (toạ độ trọng tâm) từ lưới thưa của họ rồi
        làm trơn trên lưới dày, nên chỗ lưới họ gập thành mặt phẳng thì của mình uốn cong đều. mo=True: pha thêm ba xương mỡ bụng."""
        a = by[hinh]
        g = Image.open(os.path.join(TM.MANH, file + ".png"))
        sk.anh(slot, nho(g, 2.0 * PXU / TM.Z))
        im = sk.images[slot]
        bv, bt = BUOC[slot]
        L = luoi.luoi_vung(im, buoc_vien=bv, buoc_trong=bt, ten=slot)
        fw, fh = g.width / TM.Z, g.height / TM.Z
        uvf = L.pts * np.array([fw / im.width, fh / im.height])              # px khung ảnh vùng của họ
        Vg = np.c_[uvf, np.ones(L.n)] @ TM.aff(hinh, 1)                      # thế giới con gốc (lưới dáng gốc của họ là affine của ảnh)
        V = Vg * KG
        uv0, tris0 = TL.luoi(a)
        w0 = [{ten[k]: w for k, w in ws} for ws in a["w"]]
        # toạ độ trọng tâm của từng đỉnh dày trong từng tam giác của họ; lấy tam giác chứa nó (ngoài lưới: tam giác gần nhất, kẹp ≥ 0)
        best = np.full(L.n, -np.inf)
        bta = np.zeros((L.n, 3))
        btr = np.zeros(L.n, int)
        for ti, t in enumerate(tris0):
            A_, B_, C_ = uv0[t]
            T_ = np.array([B_ - A_, C_ - A_]).T
            if abs(np.linalg.det(T_)) < 1e-9:
                continue
            bc = np.linalg.solve(T_, (uvf - A_).T).T
            be = np.c_[1 - bc.sum(1), bc]
            mn = be.min(1)
            hon = mn > best
            best[hon], bta[hon], btr[hon] = mn[hon], be[hon], ti
        bta = np.clip(bta, 0, None)
        bta /= bta.sum(1, keepdims=True)
        W = []
        for i in range(L.n):
            d_ = {}
            for vi, be in zip(tris0[btr[i]], bta[i]):
                for b_, w in w0[vi].items():
                    b_ = (doi or {}).get(b_, b_)
                    d_[b_] = d_.get(b_, 0.0) + be * w
            W.append(d_)
        W = trongso.lam_tron(L, W, lan=6)
        if mo:
            # mỡ bụng: mỗi xương một vùng ảnh hưởng hình chuông; đáy bụng (tì đất) và đỉnh bụng (dưới đầu) không rung
            cao = np.clip((Vg[:, 1] - 12.0) / 95.0, 0, 1) * np.clip((392.0 - Vg[:, 1]) / 120.0, 0, 1)
            for i in range(L.n):
                them = {n_: A_ * math.exp(-(((Vg[i, 0] - x_) ** 2 + (Vg[i, 1] - y_) ** 2) / r_ ** 2)) * cao[i] for n_, (x_, y_, r_, A_, _) in MO.items()}
                tong_ = sum(them.values())
                if tong_ > 0.75:
                    them = {k_: v_ * 0.75 / tong_ for k_, v_ in them.items()}
                    tong_ = 0.75
                d_ = {k_: v_ * (1 - tong_) for k_, v_ in W[i].items()}
                d_.update({k_: v_ for k_, v_ in them.items() if v_ > 0.004})
                W[i] = d_
        W = trongso.chuan(W, toi_da=4)
        sk.slot(slot, "move", slot)
        sk.luoi_gan(slot, slot, L, W, the_gioi=V)
        # điểm gắn theo ma trận dáng gốc ĐÃ ÁP RÀNG BUỘC của họ (xương của mình: dáng gốc của rig mình)
        inv = {}
        rows = []
        for p_, d_ in zip(V, W):
            row = []
            for n_, w in d_.items():
                if n_ not in inv:
                    inv[n_] = np.linalg.inv(Wc[n_] if n_ in Wc and n_ in GIU else sk.W0[n_])
                lp_ = inv[n_] @ np.array([p_[0], p_[1], 1.0])
                row.append((n_, float(lp_[0]), float(lp_[1]), float(w)))
            rows.append(row)
        sk.atts[slot][slot]["verts"] = rows
        tong[0] += L.n
        tong[1] += len(L.tris)
        than.append(slot)

    def rieng(ten_):
        """ảnh một mảnh riêng (PX px mỗi đơn vị con gốc) vào atlas + Dat đặt góc trên trái của nó vào thế giới rig."""
        g = Image.open(os.path.join(TM.MANH, ten_ + ".png"))
        sk.anh(ten_, nho(g, PXU / TM.PX))
        im = sk.images[ten_]
        gx, gy = dat[ten_]["goc"]
        ti = (g.width / TM.PX * KG / im.width, g.height / TM.PX * KG / im.height)
        return im, Dat(gx * KG, gy * KG, neo=(0.0, 0.0), ti=ti)

    kh = lambda p: TM.khung_ra_tg(np.array(p, float)) * KG       # px concept → thế giới rig của mình   # noqa: E731

    # tay của họ có gốc bám nửa thân nửa khúc tay đầu: tay vung quá 90 độ thì gốc tay co rúm thành răng cưa trên mép bụng (hình của
    # họ trong mờ nên không lộ; hình mình viền mực nên lộ). Cho cả tay bám khúc tay đầu: gốc tay xoay cứng quanh vai, nằm trong thân
    gan_day("tay_xa", "P_shouLB", "tay_xa")          # tay sau nấp sau thân: giữ trọng số của họ (gốc tay dính thân, không hở)
    for n_, (x_, y_, _, _, _) in MO.items():         # ba xương mỡ bụng
        sk.xuong(n_, "bone3", x_ * KG, y_ * KG, the_gioi=True)
    gan_day("bung", "P_shentiB", "bung", mo=True)
    # thứ trong bụng: cụm hạt giống (xương hat) và ba bong bóng (trôi nhẹ), vẽ trên bụng, dưới đầu
    im, d = rieng("hat")
    c = d.mot((im.width * 0.5, im.height * 0.62), im.width, im.height)          # tâm hạt (mầm ở trên, rễ ở dưới)
    sk.xuong("hat", "mo_g", float(c[0]), float(c[1]), the_gioi=True)        # hạt giống trôi theo mỡ bụng giữa
    sk.slot("hat", "hat", "hat")
    sk.manh("hat", "hat", d)
    than.append("hat")
    bong_ = [k for k in dat if k.startswith("bong")]
    for k in bong_:
        im, d = rieng(k)
        c = d.mot((im.width * 0.5, im.height * 0.5), im.width, im.height)
        sk.xuong(k, "mo_t" if c[0] < 0 else "mo_p", float(c[0]), float(c[1]), the_gioi=True)   # bong bóng theo mỡ bụng hai bên
        sk.slot(k, k, k)
        sk.manh(k, k, d)
        than.append(k)
    gan_day("dau", "P_tou2B", "dau")
    for i, (h, sl) in enumerate(MAT.items()):
        gan(sl, h, sl, an=i > 0)
    # mồm tròn: ẩn, chỉ hiện lúc bắn chiêu; xương mieng cũng là chỗ nhả lá (trục x chĩa sang phải)
    g = Image.open(os.path.join(TM.MANH, "mieng.png"))
    sk.anh("mieng", nho(g, PXU / TM.PX))
    mc = np.array(dat["mieng"]["tam"]) * KG
    lp = np.linalg.solve(Wc["bone4"], np.array([mc[0], mc[1], 1.0]))
    sk.xuong("mieng", "bone4", float(lp[0]), float(lp[1]))
    sk.slot("mieng", "mieng", "mieng", an=True)
    mc2 = dau_tg(mc)
    sk.manh("mieng", "mieng", Dat(mc2[0], mc2[1], neo=(0.5, 0.5), ti=g.width / TM.PX * KG / sk.images["mieng"].width * DAU_TI))
    gan_day("tay_gan", "P_shouRB", "tay_gan", doi={"bone3": "bone5"})
    # tóc (dạng 2: mầm hai lá; dạng 1: một mầm cong): một lưới, mỗi chuỗi trong CHUOI là một dãy xương dọc gân lá / thân mầm
    im, d = rieng("toc")
    g0 = kh(J_GOC)
    lp = np.linalg.solve(Wc["bone14"], np.array([g0[0], g0[1], 1.0]))
    sk.xuong("toc_goc", "bone14", float(lp[0]), float(lp[1]))
    JS = {n_: dau_tg(kh(J_)) for n_, J_ in CHUOI.items()}
    chuoi_ = {n_: sk.chuoi(n_, "toc_goc", J_) for n_, J_ in JS.items()}
    Lh = luoi.luoi_vung(im, buoc_vien=7.0 * (1.5 if NHE else 1.0), buoc_trong=9.5 * (1.5 if NHE else 1.0), ten="toc")
    Q0 = d.ra(Lh.pts, im.width, im.height)
    Q = dau_tg(Q0)

    def cach(Qp, J):
        J = np.asarray(J, float)
        best = np.full(len(Qp), np.inf)
        for k_ in range(len(J) - 1):
            v = J[k_ + 1] - J[k_]
            t = np.clip(((Qp - J[k_]) @ v) / (v @ v), 0, 1)
            best = np.minimum(best, np.hypot(*(Qp - (J[k_] + t[:, None] * v)).T))
        return best

    # phần bám cứng toc_goc: chỉ vùng quanh gốc cuống (lá trái của dạng 2 rủ thấp hơn mức Y_VONG ở phía xa nên phải chặn theo cả x)
    Qc = TL.khung_T()(Q0 / KG)                               # px concept
    goc_ = (Qc[:, 1] > Y_VONG) & (np.abs(Qc[:, 0] - J_GOC[0]) < R_VONG)
    ten_c = list(CHUOI)
    gan_nhat = np.argmin(np.stack([cach(Q, JS[n_]) for n_ in ten_c]), axis=0)
    W = [{"toc_goc": 1.0} for _ in range(Lh.n)]
    for ci, n_ in enumerate(ten_c):
        ids = np.nonzero(~goc_ & (gan_nhat == ci))[0]
        ws_ = trongso.chuoi_chieu(Q[ids], JS[n_], chuoi_[n_], cha="toc_goc", cha_hoa=0.55)
        for i, w in zip(ids, ws_):
            W[i] = w
    W = trongso.chuan(trongso.lam_tron(Lh, W, lan=4))
    sk.slot("toc", "toc_goc", "toc")
    sk.luoi_gan("toc", "toc", Lh, W, the_gioi=Q)
    than.append("toc")
    tong[0] += Lh.n
    tong[1] += len(Lh.tris)
    print(f"{len(sk.bones)} xương, {len(than)} slot, {tong[0]} đỉnh, {tong[1]} tam giác")
    for e, m in (("trung", "khung đòn trúng (tát / húc)"), ("phun", "há mồm, bắt đầu phun lá (VFX)"), ("het_phun", "hết phun"),
                 ("phinh", "phình to xong"), ("dap", "đáp đất"), ("cham_dat", "rơi chạm đất"), ("vo_bung", "tay vỗ vào bụng")):
        sk.su_kien(e, m)
    return sk, dict(scan=scan, IB=IB, ten=ten, slots=[s["name"] for s in I["slots"]], than=than, chuoi=chuoi_, bong=bong_)


def chuyen_dong(info):
    """{clip: (dài, {xương của họ: mảng (số khung, 5) = xoay độ, dời x, y (đơn vị rig mình), tỉ lệ x, y nhân}, hình mắt từng khung)}:
    lệch của biến đổi RIÊNG đã áp (runtime Spine) so với dáng gốc, cho MỌI xương của họ (xương mình mượn góc của xương đã bỏ)."""
    S = json.load(open(os.path.join(info["scan"], "sample_moi.json"), encoding="utf-8"))
    IB, ten = info["IB"], info["ten"]
    im = info["slots"].index("P_SL_bq1")
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        res = {}
        for i, b0 in enumerate(IB):
            if b0["name"] == "root":
                continue
            A = np.array([[F["l"][i][2] - b0["rot"], (F["l"][i][0] - b0["x"]) * KG, (F["l"][i][1] - b0["y"]) * KG,
                           F["l"][i][3] / (b0["sx"] or 1.0), F["l"][i][4] / (b0["sy"] or 1.0)] for F in fr])
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            A[:, 0] -= 360.0 * round(A[0, 0] / 360.0)
            res[ten[i]] = A
        # bone4 của họ chỉ thừa hưởng độ dời: đổi về thừa hưởng thường bằng cách trừ tổng góc các xương cha
        res["bone4"] = res["bone4"].copy()
        for c in CHA_BONE4:
            res["bone4"][:, 0] -= res[c][:, 0]
        out[clip] = (float(v["dur"]), res, [F["n"][im] or "P_SL_bq1" for F in fr])
    return out


def lam_clip(sk, info):
    CD = chuyen_dong(info)
    KR = json.load(open(os.path.join(info["scan"], "kenh_rieng.json"), encoding="utf-8"))
    than = info["than"]

    def noi(arr, x):
        n = len(arr)
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        return np.asarray(arr[i0], float) * (1 - w) + np.asarray(arr[i1], float) * w, i0

    def dat_dang(P, goc, tau, lap):
        dur, R, mat = CD[goc]
        x = (tau % dur if lap else min(max(tau, 0.0), dur)) * 30.0
        for b in GIU:
            v, _ = noi(R[b], x)
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        for minh, (ho, k) in NGUON.items():
            v, _ = noi(R[ho], x)
            P.rot(minh, float(v[0]) * k)
        _, i0 = noi(R["bone3"], x)
        for h, sl in MAT.items():
            P.alpha[sl] = 1.0 if mat[i0] == h else 0.0
        kr = KR[goc]
        bay, _ = noi(kr["bay"], x)
        if abs(bay[0]) > 1e-4 or abs(bay[1]) > 1e-4:
            P.move("move", float(bay[0]) * KG, float(bay[1]) * KG)
        m, _ = noi(kr["mieng"], x)
        m = float(m)
        P.alpha["mieng"] = min(1.0, m * 4.0)
        if m > 0:
            s = 0.3 + 0.7 * m
            P.scale("mieng", s * (1.0 + 0.05 * math.sin(tau * 48.0)), s * (1.0 - 0.05 * math.sin(tau * 48.0)))     # mồm rung nhẹ lúc phun
        # bong bóng trôi nhẹ: chu kỳ chia hết độ dài clip lặp; clip không lặp thì bằng 0 ở hai đầu
        cua = 1.0 if lap else math.sin(math.pi * min(1.0, max(0.0, tau / dur))) ** 2
        ck = dur / max(1, round(dur / 2.7))
        for i, k in enumerate(info["bong"]):
            P.move(k, 3.0 * cua * math.sin(2 * math.pi * tau / ck + 2.1 * i) * (1 if lap else 0.6),
                   (5.0 * cua * (math.cos(2 * math.pi * tau / ck + 1.3 * i) - math.cos(1.3 * i))) if lap else 4.0 * cua * math.sin(2 * math.pi * tau / ck + 1.3 * i))

    mem = lambda: [Nay({n_: v_[4] for n_, v_ in MO.items()})] + [LoXo(info["chuoi"][n_], k=k_, damp=0.6, maxang=m_) for n_, (k_, m_) in LO_XO.items()]   # noqa: E731
    out = []
    for ten_, goc, lap in CLIPS:
        dur = CD[goc][0]
        ev = [tuple(e) for e in KR[goc]["su_kien"]]
        if ten_ == "die":
            def fn(t, P, goc=goc, dur=dur):
                dat_dang(P, goc, t, False)
                a = float(np.clip(1.0 - (t - dur) / (TAN - 0.1), 0.0, 1.0))
                for sl in than:
                    P.alpha[sl] = a * P.alpha.get(sl, 1.0)
            out.append(Clip(ten_, dur + TAN, fn, mem=mem()))
        elif ten_ == "appear":
            def fn(t, P, goc=goc):
                dat_dang(P, goc, t, False)
                a = min(1.0, t / 0.12)                       # khung đầu trống, hiện dần lúc đang rơi
                for sl in than:
                    P.alpha[sl] = a * P.alpha.get(sl, 1.0)
            out.append(Clip(ten_, dur, fn, ev=ev, mem=mem()))
        else:
            out.append(Clip(ten_, dur, (lambda t, P, goc=goc, lap=lap: dat_dang(P, goc, t, lap)), loop=lap, ev=ev, mem=mem()))
    return out, dat_dang, CD, KR, noi


def chieu_cao():
    """chiều cao game: đỉnh đầu + gần nửa tóc (tính cả lá thì thân bị thu nhỏ so với tướng khác), nhân CAO_GAME."""
    return (411.0 + DAU_TI * (156.0 + 0.45 * (CAO_TOC - 567.0))) * KG * CAO_GAME


def main(a):
    sk, info = dung()
    clips, dat_dang, CD, KR, noi_ = lam_clip(sk, info)
    if a and a[0] == "nhe":                    # TL_DANG=2 TL_NHE=1: ghi bản nhẹ (rig + khung 0 idle + chiều cao) cho dạng 1 gộp tiến hóa
        idle = [c for c in clips if c.ten == "idle"][0]
        os.makedirs(RA, exist_ok=True)
        pickle.dump(dict(sk=sk, idle0=hoat.nuong(sk, idle)[0], cao=chieu_cao(), kg=KG, chuoi=info["chuoi"], lo_xo=LO_XO, nguon=NGUON),
                    open(os.path.join(RA, "_nhe.pkl"), "wb"))
        print("bản nhẹ:", os.path.join(RA, "_nhe.pkl"))
        return
    if a and a[0] == "soi":                    # soi <clip> <giây,giây,...> [tỉ lệ]: khung lớn nền xám → rig/soi_<clip>.png
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
    cao = chieu_cao()
    M, noi = sk, {}
    if TL.K < SO_DANG:
        # TIẾN HÓA (người dùng 2026-11-12, chê bản "gồng rồi tan": "dạng 1 nhảy lên cao hẳn, sau đó dạng tiếp theo rơi xuống"):
        # gộp bản nhẹ của dạng sau (dựng ở tiến trình riêng vì cấu hình theo dạng đọc lúc nạp mô-đun). Dạng cũ: nhún sâu rồi bật vọt
        # lên, vừa bay vừa mờ (khung sticker chỉ cao thêm ~0,8 chiều cao nên mờ hẳn trước khi chạm mép); nghỉ một nhịp trống; dạng
        # sau RƠI từ trên xuống bằng đúng clip appear của nó (bẹp, nảy, rung, mở mắt), khung cuối = khung 0 idle dạng sau.
        subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "nhe"], env=dict(os.environ, TL_DANG=str(TL.K + 1), TL_NHE="1"), check=True)
        N2 = pickle.load(open(os.path.join(HERE, "inbox", f"tinh_linh_{TL.K + 1}", "rig", "_nhe.pkl"), "rb"))
        sk2, idle2, kg2 = N2["sk"], N2["idle0"], N2["kg"]
        ti = cao / N2["cao"]
        M = tienhoa.gop(sk, sk2)
        end2 = tienhoa.doi_ten_pose(idle2, "n_")
        alphaB = M.info.get("alpha_B", {})
        slotA = {s_["name"]: s_["alpha"] for s_ in sk.slots}
        LEN = 0.80 * cao                        # dạng cũ bay lên chừng này rồi mất (≈ mép trên khung sticker)

        def tron_pose(Pa, Pb, w):
            out = {}
            for b_ in set(Pa.t) | set(Pb.t):
                va, vb = Pa.t.get(b_, [0, 0, 0, 1, 1]), Pb.t.get(b_, [0, 0, 0, 1, 1])
                out[b_] = [va[q] * (1 - w) + vb[q] * w for q in range(5)]
            return out

        def dang_sau(P, goc, tau):
            """dáng của DẠNG SAU (xương n_*) theo clip `goc` ở giây tau: cùng mẫu chuyển động, độ dời theo cỡ của nó."""
            dur, R, mat = CD[goc]
            x = min(max(tau, 0.0), dur) * 30.0
            kq = kg2 / KG
            for b_ in GIU:
                v, _ = noi_(R[b_], x)
                P.rot("n_" + b_, float(v[0]))
                P.move("n_" + b_, float(v[1]) * kq, float(v[2]) * kq)
                P.scale("n_" + b_, float(v[3]), float(v[4]))
            for minh, (ho, k) in N2["nguon"].items():
                P.rot("n_" + minh, float(noi_(R[ho], x)[0][0]) * k)
            _, i0 = noi_(R["bone3"], x)
            for h, sl in MAT.items():
                P.alpha["n_" + sl] = 1.0 if mat[i0] == h else 0.0
            bay, _ = noi_(KR[goc]["bay"], x)
            P.move("n_move", float(bay[0]) * kg2, float(bay[1]) * kg2)
            P.alpha["n_mieng"] = 0.0

        def tien_hoa(t, P):
            # dạng cũ: từ dáng nghỉ sang cú nhún – bật của clip walk (nhún 0,24; rời đất 0,32), nhún chậm và sâu hơn rồi vọt thẳng lên
            Pa, Pb = khung.Pose(), khung.Pose()
            dat_dang(Pa, "tl_idle", 0.0, True)
            tau = hoat.cv(t, [(0, 0.02), (0.16, 0.12), (E_NHUN, 0.245), (E_BAT, 0.33, "in"), (E_BAT + 0.4, 0.44)])
            dat_dang(Pb, "tl_walk", tau, True)
            P.t.update(tron_pose(Pa, Pb, hoat.ease(t / 0.16)))
            sau = hoat.cv(t, [(0, 0), (0.16, 0), (E_NHUN, 1, "out"), (E_BAT, 0)])              # nhún sâu thêm
            P.scale("bone3", 1 + 0.07 * sau, 1 - 0.10 * sau)
            P.move("bone3", 0.0, -0.10 * sau * 205.0 * KG)
            P.move("bone43", 0.0, -0.10 * sau * 417.0 * KG)
            len_ = hoat.cv(t, [(0, 0), (E_BAT - 0.02, 0), (E_BAT + 0.30, 1, "out")])
            P.move("move", 0.0, LEN * len_)
            P.scale("move", 1 - 0.10 * math.sin(math.pi * min(1.0, len_)) , 1 + 0.22 * math.sin(math.pi * min(1.0, len_)))   # vệt vọt lên: giãn dọc
            aA = 1.0 - hoat.ease((t - (E_BAT + 0.10)) / 0.16)
            for sl, a0 in slotA.items():
                P.alpha[sl] = aA * Pb.alpha.get(sl, a0)
            # dạng sau: rơi xuống bằng clip appear của nó
            tb = t - E_ROI
            dang_sau(P, "tl_appear", tb)
            aB = hoat.ease(tb / 0.10) if tb > 0 else 0.0
            for sl, a0 in alphaB.items():
                P.alpha[sl] = aB * P.alpha.get(sl, a0)
            P.scale("evo", ti)

        def ve_dich(t, P):                      # 0,3 s cuối hoà về đúng khung 0 idle của dạng sau (lò xo còn dư)
            w = hoat.ease((t - (E_DUR - 0.3)) / 0.3)
            if w <= 0:
                return
            for b_ in set(end2.t) | {x_ for x_ in P.t if x_.startswith("n_")}:
                tb_, ta_ = end2.t.get(b_, [0, 0, 0, 1, 1]), P._g(b_)
                for q in range(5):
                    ta_[q] = ta_[q] * (1 - w) + tb_[q] * w
            for sl, a0 in alphaB.items():
                P.alpha[sl] = P.alpha.get(sl, a0) * (1 - w) + end2.alpha.get(sl, a0) * w

        mem_ = [Nay({n_: v_[4] for n_, v_ in MO.items()})] + [LoXo(info["chuoi"][n_], k=k_, damp=0.6, maxang=m_) for n_, (k_, m_) in LO_XO.items()]
        mem_ += [Nay({"n_" + n_: v_[4] for n_, v_ in MO.items()})]
        mem_ += [LoXo(["n_" + x_ for x_ in N2["chuoi"][n_]], k=k_, damp=0.6, maxang=m_) for n_, (k_, m_) in N2["lo_xo"].items()]
        ev = Clip("evolve", E_DUR, tien_hoa, ev=[(0.2, "tu_luc", ""), (E_BAT, "nhay", ""), (E_ROI, "doi_dang", ""), (E_ROI + 0.40, "cham_dat", "")],
                  post=ve_dich, mem=mem_)
        clips = clips + [ev]
        _, _, s_ev = tienhoa.lech_cuoi(M, hoat.nuong(M, ev), sk2, idle2, ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
        print("  evolve:", noi["evolve"])
    xuat.xuat_het(M, clips, RA, TEN, TIEU_DE, dang=TL.K, so_dang=SO_DANG, dung_yen=("cast",), lao=("skill",),
                  cao=cao, ma_goc=None, tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2, noi_them=noi)


if __name__ == "__main__":
    main(sys.argv[1:])
