# -*- coding: utf-8 -*-
"""Thổ Tinh (thach_de, final boss đảo Thổ): rig trên bộ xương của con gốc monster_3802 (khổng lồ đá nổi). Mảnh của mình là MẢNH CỨNG một
xương (hành tinh, hai mặt trăng nắm đấm, vỏ vai, lưỡi trăng, đốt tay...) đặt vào chỗ mảnh tương ứng của họ; chuyển động = mẫu khung
`scan/monster_3802/sample.json` (biến đổi riêng đã áp ràng buộc, lệch so với khung 0 idle).

Thêm ngoài rig gốc:
- `tam` (con của bone5, ở tâm lõi): gốc của hố hành tinh và quỹ đạo vệ tinh; nghiêng theo lõi nên quỹ đạo luôn song song các dải.
- Hố hành tinh `ho_k`: clip `aura` dời ngang x = R·sinθ và co bề ngang cosθ (nửa sau ẩn) → hành tinh TỰ QUAY, không cần mặt nạ.
- Vệ tinh `ve_j`: chuỗi xương quay ngược `quy_j` → `quy2_j` → `dao_j` vẽ elip nghiêng; aura cộng +Δ / −2Δ / +Δ nên clip trận cộng thêm
  được; nửa gần vẽ trước lõi (slot `ve_j_f`), nửa xa vẽ sau lõi (`ve_j_b`).
- Thứ tự vẽ đổi trong clip của họ: slot "di động" nhân bản theo chỗ chèn (`<slot>@<chỗ>`), mỗi khung bật đúng một bản.
- Đầu tách hàm (tờ D): xương `ham` ở bản lề, hàm vẽ sau đầu trên, nanh trước; bàn tay xoè ngửa đi kèm mặt trăng nắm đấm (`xoe`);
  mỗi lưỡi trăng lưng một xương `gai_i` ở đế. Clip 2026-11-18: attack nhảy nện hai tay, cast gầm + gai lưng phóng (sự kiện `ban`),
  skill bay lên / gọi đá / ép / gọi mặt trời / tia / nổ / đáp (VFX: thach_de_fx.py).

    thach_de_rig.py                       dựng, xuất inbox/thach_de_1/rig/
    thach_de_rig.py soi <clip|all> <giây,giây | t0:t1:n | n=10> [tỉ lệ]     khung nền xám → rig/soi_<clip>.png
    thach_de_rig.py kiem                  bước xoay / dời lớn nhất mỗi khung của từng clip
Chạy qua quai/khoa.py nang. Xương, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai."""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import anh, khung, hoat, xuat, soi  # noqa: E402
from quai.khung import Dat, Pose  # noqa: E402
from quai.hoat import Clip  # noqa: E402

CODE, MON = "thach_de", "monster_3802"
NON = os.environ.get("TH_DANG", "") == "non"     # dạng 1 Tiểu Thổ Tinh (thach_de_non.py): cùng xương, nhân mau/ti_le.json, mảnh non_*
TEN = f"{CODE}_non" if NON else f"{CODE}_1"
BASE2 = os.path.join(HERE, "inbox", f"{CODE}_1")              # dạng 2: mảnh, goc_ca_con
BASE = os.path.join(HERE, "inbox", TEN)
MANH = os.path.join(BASE2, "manh")
MANH_NON = os.path.join(HERE, "inbox", f"{CODE}_non", "manh")
RA = os.path.join(BASE, "rig")


def p_anh(a):
    """đường dẫn ảnh mảnh: non_* ở manh của dạng 1, còn lại ở manh dạng 2."""
    return os.path.join(MANH_NON if a.startswith("non_") else MANH, a + ".png")


def scan():
    for p in [os.environ.get("SXS"), r"D:\Ripper\SwordxStaff", r"D:\RefAnimation\SwordxStaff", r"E:\Ripper\SwordxStaff"]:
        if p and os.path.isdir(os.path.join(p, "scan", MON)):
            return os.path.join(p, "scan", MON)
    raise SystemExit("không thấy scan/" + MON)


KG = 0.46                    # đơn vị rig con gốc → đơn vị rig của mình
PXU = 0.44                   # pixel atlas cho mỗi đơn vị rig con gốc
FPS = 30.0
W, HH = 1536, 1024           # khung concept / goc_ca_con
TAM = (763.0, 405.0)         # tâm hành tinh trên khung concept (px)
RHT = 272.0                  # bán kính hành tinh (px khung concept)
T_AURA = 12.0                # chu kỳ clip aura (giây): hành tinh quay 2 vòng, vệ tinh 1–4 vòng

# ---- mảnh của mình đặt theo slot của họ: slot → (ảnh, tâm x, tâm y, cao px khung concept, góc độ)
BANG = {
    "P_L_shitou07": ("vo_nho", 1090, 420, 360, 0),
    "P_shenti01": ("hanh_tinh", TAM[0], TAM[1], 2 * RHT * 653 / 622.0, 0),
    "P_L_xiaobi04": ("cang_nho", 1202, 552, 175, 0),
    "P_L_shouzh05": ("dot_8", 1172, 838, 78, 0),
    "P_L_xiaobi05": ("trang_nho", 1110, 708, 285, 0),
    "P_L_shouzh04": ("dot_6", 968, 842, 92, 0),
    "P_L_shouzh03": ("dot_4", 1046, 866, 104, 0),
    "P_L_shouzh02": ("dot_7", 1122, 858, 90, 0),
    "P_L_shitou05": ("luoi_6", 1128, 300, 175, -22),
    "P_R_xiaobi05": ("cang_to", 350, 530, 255, 0),
    "P_R_xiaobi06": ("trang_to", 458, 700, 355, 0),
    "P_R_shouzhi04": ("dot_3", 428, 838, 112, 0),
    "P_R_shouzhi03": ("dot_1", 500, 850, 132, 0),
    "P_R_shouzhi05": ("dot_4", 640, 812, 104, 0),
    "P_R_shouzhi02": ("dot_2", 574, 836, 126, 0),
    "P_R_shitou09": ("vo_to", 438, 362, 445, 0),
    "P_R_shitou07": ("luoi_4", 402, 196, 225, 14),
    "P_tou1": ("dau", 925, 452, 352, 0),
    "P_kua03": ("hong", 662, 748, 112, 0),
    "P_R_datui06": ("dui_1", 572, 750, 118, 0),
    "P_R_xiaotui02": ("ban_1", 522, 838, 86, 0),
    "P_R_xigai": ("goi_1", 560, 806, 46, 0),
    "P_L_datui05": ("dui_2", 812, 764, 104, 0),
    "P_L_xiaotui02": ("ban_2", 834, 826, 80, 0),
}
# lưỡi trăng trên lưng: mười mảnh lưng của họ (sau → trước) → lưỡi đứng trên vành hành tinh, toả từ 152° tới 30°
LUNG = ["P_R_beiji10", "P_R_beiji09", "P_R_beiji08", "P_R_beiji07", "P_R_beiji06", "P_R_beiji05", "P_R_beiji04", "P_R_beiji03",
        "P_R_beiji02", "P_R_beiji01"]
LUNG_CAO = [128, 158, 190, 224, 252, 268, 244, 208, 170, 134]
LUNG_ANH = ["luoi_7", "luoi_6", "luoi_4", "luoi_3", "luoi_2", "luoi_1", "luoi_2", "luoi_3", "luoi_5", "luoi_7"]
LUNG_GOC = np.linspace(152.0, 30.0, 10)
# hố hành tinh: (ảnh, vĩ độ = phần bán kính lên trên, kinh độ đầu độ, cao px)
HO = [("ho_1", 0.46, 20.0, 78), ("ho_3", 0.10, 150.0, 58), ("ho_2", -0.26, 265.0, 68), ("ho_4", -0.55, 80.0, 48), ("ho_3", 0.30, 220.0, 50)]
QUAY_HT = 2                  # số vòng hành tinh quay trong một chu kỳ aura
# vệ tinh: (ảnh, đường kính px, bán trục lớn px, bán trục nhỏ px, số vòng mỗi chu kỳ aura, pha đầu độ, tâm quỹ đạo cao hơn tâm lõi px).
# Tâm quỹ đạo nâng lên để nửa gần đi ngang phần mặt hành tinh còn lộ (giữa hàng lưỡi trăng và đầu, nắm đấm), nửa xa khuất sau lõi.
VE = [("ve_1", 118, 372, 84, 1, 250.0, 118), ("ve_2", 90, 330, 66, 2, 20.0, 60), ("ve_3", 70, 404, 96, 1, 120.0, 165),
      ("ve_4", 54, 300, 52, 3, 300.0, 20), ("ve_5", 46, 350, 74, 2, 200.0, 95), ("ve_3", 62, 318, 60, 2, 110.0, 140)]
NGHIENG = 12.0               # quỹ đạo nghiêng (độ, ngược kim: bên phải cao hơn)
SPAN = 5.0                   # khung vẽ trên sân (lần chiều cao): chiêu cuối bay lên 0,72 chiều cao, hai tay giơ quá đầu
CLIPS = [("appear", "generate_01", False), ("idle", "idle_01", True), ("walk", "run_01", True), ("attack", "skill_03", False),
         ("cast", "skill_05", False), ("skill", "skill_03", False), ("hit", "hit_01", False), ("die", "die_01", False)]
TAN = 0.5
SAU = 3000.0                 # mặt nạ đất nằm sâu chừng này (đơn vị rig mình) khi không dùng
# slot nắm đấm (mặt trăng + đốt tay): ẩn khi đổi sang bàn tay xoè
TAY_TO = ["P_R_xiaobi06", "P_R_shouzhi04", "P_R_shouzhi03", "P_R_shouzhi05", "P_R_shouzhi02"]
TAY_NHO = ["P_L_xiaobi05", "P_L_shouzh05", "P_L_shouzh04", "P_L_shouzh03", "P_L_shouzh02"]
# ---- đầu tách hàm (tờ D, thach_de_dau.py; người dùng 2026-11-18 "tạo thêm hàm dưới"): đầu trên + hàm dưới (kèm lòng miệng) + hai nanh;
# hàm và nanh gắn xương `ham` (con bone7, ở bản lề sau miệng), hàm vẽ sau đầu trên, nanh vẽ trước
DAU0 = ("dau", 925, 452, 352)          # chỗ mảnh đầu cũ trên khung concept
HA = 19.0                              # độ há khi gầm (độ); quá ~20° thì lòng miệng lòi ra sau má
# bàn tay xoè ngửa (tờ D): slot nắm đấm → (ảnh, tâm lòng bàn tay px ảnh, bề ngang lòng bàn tay px ảnh); lòng bàn tay đặt trùng tâm mặt trăng
XOE = {"P_R_xiaobi06": ("tay_xoe_to", (405, 320), 450.0), "P_L_xiaobi05": ("tay_xoe_nho", (175, 240), 310.0)}

# ---- dạng 1 (TH_DANG=non; người dùng 2026-11-18 chọn concept B "trăng non nứt vỏ"): lõi bọc vỏ nứt thay hành tinh, SÁU mảnh vỏ vỡ thay
# mười lưỡi trăng (ẩn 4 lưỡi xen kẽ), BA vệ tinh, không hố (vỏ che), đầu non tách hàm; mảnh mới vẽ cùng cỡ mảnh dạng 2 tương ứng nên đặt
# đúng chỗ mảnh cũ trong hệ xương dạng 2, rồi co / phóng theo ti_le.json như mảnh dùng lại
GAI_AN = (1, 3, 6, 8) if NON else ()
VO_NON = {5: "non_vo_1", 4: "non_vo_2", 7: "non_vo_3", 2: "non_vo_4", 9: "non_vo_5", 0: "non_vo_6"}   # lưỡi → mảnh vỏ (cao → thấp)
K_VO = 1.3                   # mảnh vỏ cao hơn lưỡi trăng cùng chỗ (đo theo concept B), trước khi co theo xương gai
N_VE = 3 if NON else 6
DICH_RIG = None              # đích của gai (toạ độ rig); None = trước mặt 1,25 / 0,42 chiều cao (thach_de_fx.py đặt chỗ đối thủ)
_C = {}


def dau_spec():
    """chỗ các mảnh đầu mới trên khung concept, tính từ chỗ mảnh đầu cũ + manh/_dau_khop.json."""
    P = "non_" if NON else ""
    K = json.load(open(os.path.join(MANH_NON if NON else MANH, "_dau_khop.json")))
    Wd, Hd = Image.open(p_anh(P + "dau")).size
    _, X0, Y0, H0 = DAU0
    k = H0 / Image.open(p_anh("dau")).height       # px mảnh (cỡ tờ dạng 2) → px concept dạng 2; đầu non vẽ cùng cỡ đầu dạng 2
    out = {}
    for n, a in (("dau_tren", "dau_tren"), ("ham", "ham_cat"), ("nanh_1", "nanh_1"), ("nanh_2", "nanh_2")):
        q = K[n]
        a = P + a
        h = Image.open(p_anh(a)).height
        out[n] = (a, X0 + (q["cx"] - Wd / 2) * k, Y0 + (q["cy"] - Hd / 2) * k, h * q["s"] * k, 0)
    bl = K["ban_le"]
    out["ban_le"] = (X0 + (bl["x"] - Wd / 2) * k, Y0 + (bl["y"] - Hd / 2) * k)
    return out


def xoe_spec(host_spec, host):
    """bàn tay xoè đặt theo mặt trăng nắm đấm: lòng bàn tay trùng tâm, bề ngang lòng = 0,98 đường kính mặt trăng."""
    a, cx, cy, d = host_spec[:4]
    anh_, (px, py), pw = XOE[host]
    w, h = Image.open(p_anh(anh_)).size
    k = 0.98 * d / pw
    return (anh_, cx + (w / 2 - px) * k, cy + (h / 2 - py) * k, h * k, 0)


def nap():
    if not _C:
        sc = scan()
        _C["I"] = json.load(open(os.path.join(sc, "info.json"), encoding="utf-8"))
        _C["A0"] = json.load(open(os.path.join(sc, "att_idle0.json"), encoding="utf-8"))
        _C["S"] = json.load(open(os.path.join(sc, "sample.json"), encoding="utf-8"))
        _C["hop"] = json.load(open(os.path.join(BASE2, "mau", "goc_ca_con.json")))
    return _C["I"], _C["A0"], _C["S"], _C["hop"]


def thu_tu_ve(S, slots, dung_slot, giu):
    """thứ tự vẽ đổi trong clip: tách slot ĐỨNG YÊN (thứ tự tương đối không đổi ở mọi khung) và slot DI ĐỘNG; mỗi slot di động có
    chỗ chèn = số slot đứng yên vẽ trước nó. Trả (đứng yên theo thứ tự idle, {di động: tập chỗ chèn}, hàm cho(order) → {di động: chỗ})."""
    orders = set()
    for _, goc, _ in CLIPS:
        for F in S[goc]["frames"]:
            orders.add(tuple(s for s in F["o"] if s in dung_slot))
    orders = [list(o) for o in orders]
    tinh = sorted(dung_slot)
    while True:
        dem = {s: 0 for s in tinh}
        st = set(tinh)
        for o in orders:
            pos = {s: i for i, s in enumerate(x for x in o if x in st)}
            for i, a in enumerate(tinh):
                for b in tinh[i + 1:]:
                    if pos[a] > pos[b]:
                        dem[a] += 1
                        dem[b] += 1
        xau = max((s for s in tinh if s not in giu), key=lambda s: dem[s])
        if dem[xau] == 0:
            break
        tinh.remove(xau)
    st = set(tinh)
    dong = [s for s in sorted(dung_slot) if s not in st]

    def cho(order):
        out, k = {}, 0
        for s in order:
            if s in st:
                k += 1
            elif s in dung_slot:
                out[s] = k
        return out
    cac = {s: set() for s in dong}
    for o in orders:
        for s, k in cho(o).items():
            cac[s].add(k)
    print(f"thứ tự vẽ: {len(orders)} thứ tự; {len(tinh)} slot đứng yên, {len(dong)} di động: " +
          ", ".join(f"{slots[s]}@{sorted(cac[s])}" for s in dong))
    return tinh, cac, cho


def dung():
    I, A0, S, hop = nap()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    ix = {n: i for i, n in enumerate(ten)}
    slots = [s["name"] for s in I["slots"]]
    s_, cx, cy = hop["s"], hop["cx"], hop["cy"]
    tg = lambda px, py: np.array([cx + (px - W / 2) / s_, cy - (py - HH / 2) / s_])     # px khung concept → thế giới con gốc  # noqa: E731
    L0 = S["idle_01"]["frames"][0]["l"]

    sk = khung.Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")
    for i, b in enumerate(IB):
        if b["name"] == "root":
            continue
        cha = ten[b["parent"]]
        l = L0[i]
        sk.xuong(b["name"], "move" if cha == "root" else cha, l[0] * KG, l[1] * KG, goc=l[2], dai=b["len"] * KG, sx=l[3], sy=l[4])
    # kiểm: ma trận dáng gốc của mình trùng thế giới khung 0 idle của họ
    B0 = S["idle_01"]["frames"][0]["b"]
    lech = max(float(np.hypot(sk.W0[n][0, 2] - B0[i][0] * KG, sk.W0[n][1, 2] - B0[i][1] * KG)) for i, n in enumerate(ten) if n != "root")
    print(f"dáng gốc = khung 0 idle: lệch lớn nhất {lech:.2f} đơn vị rig")

    by = {a["slot"]: a for a in A0["atts"] if a.get("cur") and a.get("region")}
    bam = {}
    for sl, a in by.items():
        if a.get("w"):
            w = {}
            wl = a["w"]
            for v in wl:
                for b_, wt in (v if isinstance(v[0], (list, tuple)) else [v]):
                    w[b_] = w.get(b_, 0.0) + wt
            b0 = max(w, key=w.get)
            bam[sl] = ten[b0] if isinstance(b0, int) else b0
        else:
            bam[sl] = a["bone"]

    bang = dict(BANG)
    DS = dau_spec()
    bang["P_tou1"] = DS["dau_tren"]
    if NON:                                                  # lõi bọc vỏ nứt: đĩa đặt trùng đĩa hành tinh dạng 2 (đường kính 2 RHT)
        g_ = Image.open(p_anh("non_hanh_tinh"))
        bb = g_.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox()
        bang["P_shenti01"] = ("non_hanh_tinh", TAM[0], TAM[1], g_.height * 2 * RHT / (bb[2] - bb[0]), 0)
    tam_tg = tg(*TAM) * KG
    R = RHT / s_ * KG
    for k, sl in enumerate(LUNG):
        g = math.radians(LUNG_GOC[k])
        a_, cao_ = (VO_NON.get(k), LUNG_CAO[k] * K_VO) if NON else (LUNG_ANH[k], LUNG_CAO[k])
        bang[sl] = (a_, None, None, cao_, LUNG_GOC[k] - 90.0, (TAM[0] + (RHT - 16) * math.cos(g), TAM[1] - (RHT - 16) * math.sin(g)))
    dung_slot = {slots.index(sl) for sl in bang}
    tinh, cac, cho = thu_tu_ve(S, slots, dung_slot, {slots.index("P_shenti01")})

    def them_anh(a, cao_px):
        g = Image.open(p_anh(a))
        k = cao_px / g.height * PXU / s_
        key = f"{a}_{int(round(cao_px))}"
        if key not in sk.images:
            sk.anh(key, anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * k)), max(2, round(g.height * k))), Image.LANCZOS).convert("RGBA")))
        return key

    TI = KG / PXU

    def dat_manh(slot_ten, xuong, spec, an=False):
        a, px, py, cao_px, goc = spec[:5]
        if a is None:                                        # slot không hình (dạng 1: lưỡi lưng bị bỏ)
            sk.slot(slot_ten, xuong, None, an=True)
            return
        key = them_anh(a, cao_px)
        sk.slot(slot_ten, xuong, key, an=an)
        if len(spec) > 5:                                    # neo ở đế (lưỡi trăng): điểm đế tới điểm vành
            p = tg(*spec[5]) * KG
            sk.manh(slot_ten, key, Dat(p[0], p[1], goc=goc, ti=TI, neo=(0.5, 0.93)))
        else:
            p = tg(px, py) * KG
            sk.manh(slot_ten, key, Dat(p[0], p[1], goc=goc, ti=TI))

    # xương tâm lõi (góc thế giới 0 ở dáng gốc): gốc của hố và quỹ đạo
    sk.xuong("ht", "bone5", tam_tg[0], tam_tg[1], goc=0.0, the_gioi=True)       # hành tinh có xương riêng (die: rơi xuống đất)
    sk.xuong("tam", "ht", 0.0, 0.0)
    quy = []
    for j, (a, dk, ra_, rb_, vong, pha, cy_) in enumerate(VE[:N_VE]):
        A_, B_ = (ra_ + rb_) / 2 / s_ * KG, (ra_ - rb_) / 2 / s_ * KG
        cy_ = cy_ / s_ * KG
        sk.xuong(f"quy_{j}", "tam", 0.0, cy_, goc=NGHIENG + pha)
        sk.xuong(f"quy2_{j}", f"quy_{j}", A_, 0.0, goc=-2 * pha)
        sk.xuong(f"dao_{j}", f"quy2_{j}", B_, 0.0, goc=pha - NGHIENG)
        quy.append(dict(j=j, anh=a, dk=dk, vong=vong, pha=pha, cy=cy_))

    ten_slot = {}                                            # slot của họ → [(chỗ chèn | None, tên slot của mình)]
    idle_cho = cho(S["idle_01"]["frames"][0]["o"])
    # hàm: xương bản lề (con bone7), trục x nằm ngang ở dáng gốc; mở hàm = xoay âm (cằm xuống, mặt nhìn sang phải)
    bl = tg(*DS["ban_le"]) * KG
    sk.xuong("ham", "bone7", bl[0], bl[1], goc=0.0, the_gioi=True)
    KEM = {}                                                 # slot chủ → [(slot đi kèm, kiểu)]: độ đậm theo slot chủ

    def kem_truoc(base, nm, an):
        if base == "P_tou1":
            dat_manh(nm.replace("P_tou1", "ham"), "ham", DS["ham"], an=an)

    def kem_sau(base, nm, an):
        if base == "P_tou1":
            KEM[nm] = [(nm.replace("P_tou1", "ham"), "ham")]
            for n in ("nanh_1", "nanh_2"):
                dat_manh(nm.replace("P_tou1", n), "ham", DS[n], an=an)
                KEM[nm].append((nm.replace("P_tou1", n), "ham"))
        if base in XOE:
            c = nm.replace(base, XOE[base][0])
            dat_manh(c, bam[base], xoe_spec(bang[base], base), an=True)
            KEM[nm] = [(c, "xoe_to" if base == "P_R_xiaobi06" else "xoe_nho")]

    def them_dong(k):
        for s in sorted(cac):
            if k in cac[s]:
                nm = f"{slots[s]}@{k}"
                an = idle_cho.get(s) != k
                kem_truoc(slots[s], nm, an)
                dat_manh(nm, bam[slots[s]], bang[slots[s]], an=an)
                ten_slot.setdefault(s, []).append((k, nm))
                kem_sau(slots[s], nm, an)

    gai = []
    for k, s in enumerate(tinh):
        them_dong(k)
        sl = slots[s]
        if sl in LUNG:                                       # gai lưng: xương riêng ở đế, trục x chĩa ra ngoài theo bán kính (chiêu mana bứt gai)
            i = LUNG.index(sl)
            p = tg(*bang[sl][5]) * KG
            sk.xuong(f"gai_{i}", bam[sl], p[0], p[1], goc=float(LUNG_GOC[i]), the_gioi=True)
            if i not in GAI_AN:
                gai.append(dict(i=i, slot=sl, bone=f"gai_{i}", cha=bam[sl]))
            dat_manh(sl, f"gai_{i}", bang[sl])
            ten_slot[s] = [(None, sl)]
            continue
        if sl == "P_shenti01":
            for q in quy:                                    # nửa xa của quỹ đạo: sau hành tinh
                key = them_anh(q["anh"], q["dk"])
                p = sk.W0[f"dao_{q['j']}"][:2, 2]
                sk.slot(f"ve_{q['j']}_b", f"dao_{q['j']}", key)
                sk.manh(f"ve_{q['j']}_b", key, Dat(p[0], p[1], ti=TI))
        kem_truoc(sl, sl, False)
        dat_manh(sl, "ht" if sl == "P_shenti01" else bam[sl], bang[sl])
        ten_slot[s] = [(None, sl)]
        kem_sau(sl, sl, False)
        if sl == "P_shenti01":
            sk.info.setdefault("ho", [])
            for i, (a, vi, kd, cao_px) in enumerate([] if NON else HO):     # hố: xương con của tam, ở vĩ độ vi (dạng 1: vỏ che, không hố)
                rl = R * math.sqrt(max(0.0, 1 - vi * vi))
                sk.xuong(f"ho_{i}", "tam", 0.0, R * vi)
                key = them_anh(a, cao_px)
                sk.slot(f"ho_{i}", f"ho_{i}", key)
                sk.manh(f"ho_{i}", key, Dat(tam_tg[0], tam_tg[1] + R * vi, ti=TI))
                sk.info.setdefault("ho", []).append(dict(i=i, rl=rl, kd=kd, vi=vi))
            for q in quy:                                    # nửa gần: trước hành tinh, sau đầu và tay
                key = them_anh(q["anh"], q["dk"])
                p = sk.W0[f"dao_{q['j']}"][:2, 2]
                sk.slot(f"ve_{q['j']}_f", f"dao_{q['j']}", key)
                sk.manh(f"ve_{q['j']}_f", key, Dat(p[0], p[1], ti=TI))
    them_dong(len(tinh))
    sk.info["quy"] = quy
    # mặt đất: đáy đốt tay ở khung 0 idle; mặt nạ cắt (mặc định nằm sâu, clip appear nâng lên mặt đất)
    dat_y = float(tg(0, 914)[1] * KG)
    sk.xuong("dat_cat", "root", 0.0, dat_y - SAU)
    sk.slots.insert(0, {"name": "dat_cat", "bone": "dat_cat", "att": None, "alpha": 1.0})
    sk.si = {q["name"]: i for i, q in enumerate(sk.slots)}
    sk.atts.setdefault("dat_cat", {})
    sk.info["TI"], sk.info["them_anh"] = TI, them_anh
    for e, m in (("trung", "khung đòn trúng"), ("tu", "bắt đầu tụ lực"), ("cham_dat", "nện xuống đất / đáp đất"),
                 ("troi", "bắt đầu trồi lên"), ("xong", "đứng vững"), ("gam", "há miệng gầm"),
                 ("tach", "gai lưng bứt khỏi vành hành tinh"), ("ban", "một gai phóng đi (chuỗi = số gai): VFX lái tới đối thủ"),
                 ("bay", "bay lên trời"), ("hut", "gọi thiên thạch bám quanh đối thủ"), ("ep", "ép hai tay: khối đá quanh đối thủ co lại"),
                 ("goi", "gọi mặt trời trên đầu đối thủ"), ("tia", "mặt trời bắn tia nhiệt")):
        sk.su_kien(e, m)
    if NON:                                                  # dạng 1: co / phóng xương theo bố cục (mảnh đã gắn theo hệ xương nên đi theo)
        ti = json.load(open(os.path.join(BASE, "mau", "ti_le.json"), encoding="utf-8"))
        for nm, kk in ti.items():
            if nm not in sk.bi:                              # vệ tinh dạng 2 thừa (dạng 1 chỉ ba)
                continue
            b = sk.bones[sk.bi[nm]]
            if isinstance(kk, dict):
                b["x"] += kk.get("dx", 0.0)
                b["y"] += kk.get("dy", 0.0)
                kk = kk.get("s", 1.0)
            b["sx"] *= kk
            b["sy"] *= kk
        for b in sk.bones:
            L = khung.mat(b["x"], b["y"], b["rot"], b["sx"], b["sy"])
            sk.W0[b["name"]] = sk._world(b, L, sk.W0[b["parent"]] if b["parent"] else None)
        R *= ti["bone5"]
        print(f"dạng 1: nhân {len(ti)} xương theo ti_le.json (lõi {ti['bone5']}, đầu {ti['bone6']})")
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {len(sk.images)} ảnh")
    sk.info["gai"] = gai
    return sk, dict(S=S, ten=ten, ix=ix, slots=slots, ten_slot=ten_slot, cho=cho, R=R, tam=tam_tg, IB=IB, L0=L0, dat_y=dat_y, KEM=KEM,
                    gai=gai)


def chuyen_dong(info):
    """{clip gốc: (dài, {xương: mảng (số khung, 5) = lệch xoay độ, dời x, y (đơn vị rig mình), tỉ lệ x, y nhân}, khung)} so với khung 0 idle."""
    out = {}
    L0 = info["L0"]
    for clip, v in info["S"].items():
        fr = v["frames"]
        res = {}
        for i, n in enumerate(info["ten"]):
            if n == "root":
                continue
            l0 = L0[i]
            Am = np.array([[F["l"][i][2] - l0[2], (F["l"][i][0] - l0[0]) * KG, (F["l"][i][1] - l0[1]) * KG,
                            F["l"][i][3] / (l0[3] or 1.0), F["l"][i][4] / (l0[4] or 1.0)] for F in fr])
            Am[:, 0] = np.degrees(np.unwrap(np.radians(Am[:, 0])))
            Am[:, 0] -= 360.0 * round(Am[0, 0] / 360.0)
            if np.abs(Am - np.array([0, 0, 0, 1, 1])).max() > 1e-4:
                res[n] = Am
        out[clip] = (float(v["dur"]), res, fr)
    return out


def lam_clip(sk, info):
    CD = chuyen_dong(info)
    ten_slot, cho, KEM = info["ten_slot"], info["cho"], info["KEM"]
    ten_cua = {}
    for s, ds in ten_slot.items():
        ten_cua[info["slots"][s]] = [nm for _, nm in ds]
    AN_TO = [nm for b in TAY_TO for nm in ten_cua.get(b, [])]
    AN_NHO = [nm for b in TAY_NHO for nm in ten_cua.get(b, [])]

    def noi(arr, x):
        n = len(arr)
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        return np.asarray(arr[i0], float) * (1 - w) + np.asarray(arr[i1], float) * w

    def dat_dang(P, goc, tau, lap=False, bo=(), xoe=(0.0, 0.0), khong_dich=()):
        """dáng của clip gốc `goc` ở giây tau (lệch so với khung 0 idle) + độ đậm, thứ tự vẽ; xoe = (tay to, tay nhỏ) 0..1: đổi nắm
        đấm sang bàn tay xoè ngửa; khong_dich: xương bỏ phần dời (giữ xoay) — vd. bone3 để bỏ cú nhảy của họ."""
        dur, Rm, fr = CD[goc]
        x = (tau % dur if lap else min(max(tau, 0.0), dur)) * FPS
        for b, arr in Rm.items():
            if b in bo:
                continue
            v = noi(arr, x)
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if (abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4) and b not in khong_dich:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        F = fr[min(int(round(x)), len(fr) - 1)]
        vt = cho(F["o"])
        for s, ds in ten_slot.items():
            a = float(F["a"][s]) if F["n"][s] else 0.0
            for k, nm in ds:
                P.alpha[nm] = a if (k is None or vt.get(s) == k) else 0.0
        for host, ds in KEM.items():
            a = P.alpha.get(host, 0.0)
            for c, kieu in ds:
                P.alpha[c] = a if kieu == "ham" else a * (xoe[0] if kieu == "xoe_to" else xoe[1])
        if xoe[0] > 0:
            for nm in AN_TO:
                P.alpha[nm] = P.alpha.get(nm, 0.0) * (1 - xoe[0])
        if xoe[1] > 0:
            for nm in AN_NHO:
                P.alpha[nm] = P.alpha.get(nm, 0.0) * (1 - xoe[1])

    def tron(P, ds, xoe=(0.0, 0.0)):
        """trộn dáng nhiều clip gốc: ds = [(clip, giây, trọng số[, xương bỏ dời])]; độ đậm / thứ tự vẽ theo dáng nặng nhất."""
        Ps = []
        for d in ds:
            if d[2] <= 1e-4:
                continue
            Q = Pose()
            dat_dang(Q, d[0], d[1], xoe=xoe, khong_dich=d[3] if len(d) > 3 else ())
            Ps.append((Q, d[2]))
        tw = sum(w for _, w in Ps)
        for b in set().union(*[set(Q.t) for Q, _ in Ps]):
            acc = [0.0] * 5
            for Q, w in Ps:
                v = Q.t.get(b, khung.ZERO)
                for i in range(5):
                    acc[i] += v[i] * w / tw
            g = P._g(b)
            g[0] += acc[0]
            g[1] += acc[1]
            g[2] += acc[2]
            g[3] *= acc[3]
            g[4] *= acc[4]
        P.alpha.update(max(Ps, key=lambda x: x[1])[0].alpha)

    def dich_tg(P, b, dx, dy, W=None):
        """dời xương b một quãng (dx, dy) theo trục THẾ GIỚI."""
        W = W if W is not None else sk.the_gioi(P)
        v = np.linalg.solve(W[sk.bones[sk.bi[b]]["parent"]][:2, :2], np.array([dx, dy]))
        P.move(b, float(v[0]), float(v[1]))

    def dat_tg(P, b, pos=None, ang=None, W=None):
        """đặt xương b tới vị trí / góc THẾ GIỚI (ghi đè phần lệch đã có của xương đó)."""
        W = W if W is not None else sk.the_gioi(P)
        bb = sk.bones[sk.bi[b]]
        Wp = W[bb["parent"]]
        g = P._g(b)
        if pos is not None:
            lp = np.linalg.solve(Wp, np.array([pos[0], pos[1], 1.0]))
            g[0], g[1] = float(lp[0] - bb["x"]), float(lp[1] - bb["y"])
        if ang is not None:
            d = ang - khung.goc_mat(Wp) - bb["rot"]
            g[2] = float((d + 180.0) % 360.0 - 180.0)

    def ha(P, u):
        """há hàm: u = 1 là há gầm (HA độ)."""
        if abs(u) > 1e-4:
            P.rot("ham", -HA * u)

    info["dat_dang"], info["CD"], info["tron"] = dat_dang, CD, tron
    cv = hoat.cv
    rung = hoat.rung
    quy = sk.info["quy"]
    AB = {q["j"]: (sk.bones[sk.bi[f"quy2_{q['j']}"]]["x"], sk.bones[sk.bi[f"dao_{q['j']}"]]["x"]) for q in quy}
    cao = info["cao"]
    R = info["R"]
    HT_SLOT = ["P_shenti01"] + [f"ho_{h['i']}" for h in sk.info["ho"]]
    G0_TO = khung.goc_mat(sk.W0["bone96"])
    G0_NHO = khung.goc_mat(sk.W0["bone102"])

    def ve_bk(P, k, j=None):
        """bán kính quỹ đạo vệ tinh × k (1 = như aura; 0 = gom về tâm quỹ đạo)."""
        for q in quy:
            if j is None or q["j"] == j:
                a_, b_ = AB[q["j"]]
                P.move(f"quy2_{q['j']}", (k - 1.0) * a_, 0.0)
                P.move(f"dao_{q['j']}", (k - 1.0) * b_, 0.0)

    def ve_tam(P, x, y, j=None):
        """dời tâm quỹ đạo (trong hệ `tam`: x tới trước, y lên, theo độ nghiêng của lõi)."""
        for q in quy:
            if j is None or q["j"] == j:
                P.move(f"quy_{q['j']}", x, y)

    def ve_mo(P, a, j=None):
        for q in quy:
            if j is None or q["j"] == j:
                P.alpha[f"ve_{q['j']}_b"] = a
                P.alpha[f"ve_{q['j']}_f"] = a

    def ve_quay(P, d):
        """vệ tinh bay thêm d độ trên quỹ đạo (cộng lên aura)."""
        for q in quy:
            j = q["j"]
            P.rot(f"quy_{j}", d)
            P.rot(f"quy2_{j}", -2 * d)
            P.rot(f"dao_{j}", d)

    out = []
    # ---------------- idle (10 s của họ, có cú đấm tay vào lòng bàn tay ở giây 6) + gầm gừ khẽ ở giây 2,3; walk
    def f_idle(t, P):
        dat_dang(P, "idle_01", t, True)
        ha(P, cv(t, [(0, 0), (2.25, 0), (2.45, 0.42, "out"), (2.75, 0.36), (2.95, 0.48, "io"), (3.25, 0, "io")]))
    out.append(Clip("idle", CD["idle_01"][0], f_idle, loop=True))
    out.append(Clip("walk", CD["run_01"][0], lambda t, P: dat_dang(P, "run_01", t, True), loop=True))

    # ---------------- appear: trồi lên từ đất như trăng mọc (mặt nạ đất), vệ tinh bung ra khi đã đứng vững, rồi há miệng gầm
    D_AP = CD["generate_01"][0]

    def f_appear(t, P):
        dat_dang(P, "generate_01", t)
        P.move("dat_cat", 0.0, SAU * cv(t, [(0, 1), (2.5, 1), (2.51, 0)]) - 260.0 * cv(t, [(0, 0), (1.6, 0), (2.5, 1, "io")]))
        k = cv(t, [(0, 0.0), (D_AP - 0.95, 0.0), (D_AP - 0.35, 1.12, "out"), (D_AP, 1.0)])
        ve_bk(P, k)
        ve_mo(P, cv(t, [(0, 0), (D_AP - 0.95, 0), (D_AP - 0.8, 1)]))
        ha(P, cv(t, [(0, 0), (D_AP - 0.95, 0), (D_AP - 0.8, 1, "out"), (D_AP - 0.35, 0.9), (D_AP - 0.05, 0, "io"), (D_AP, 0)])
           + 0.05 * rung(t, D_AP - 0.8, D_AP - 0.35))
    out.append(Clip("appear", D_AP, f_appear, ev=[(0.0, "troi", ""), (D_AP - 0.9, "xong", ""), (D_AP - 0.8, "gam", "")]))

    # ---------------- attack "Thiên Chuỳ" (người dùng: "lên cao, dùng 2 tay đập xuống người đối thủ"): nhún, nhảy vọt lên, ôm hai nắm đấm giơ
    # quá đầu (skill_03 của họ), lao tới đối thủ (move, sân nắn quãng), nện cả hai nắm đấm xuống người nó; há miệng quát ở đỉnh, nghiến
    # răng lúc nện; thân nén, quỹ đạo vệ tinh bung
    D_AT, T_AT = 1.40, 0.68
    D3 = CD["skill_03"][0]

    def f_attack(t, P):
        tau = cv(t, [(0, 0), (0.22, 0.20, "io"), (0.50, 0.60, "io"), (0.54, 0.61), (0.585, 0.645, "lin"), (T_AT, 0.70, "lin"), (0.98, 1.05, "out"), (D_AT, D3, "io")])
        dat_dang(P, "skill_03", tau)
        P.move("move", 0.95 * cao * cv(t, [(0, 0), (0.22, 0), (T_AT, 1, "io"), (0.98, 1), (D_AT - 0.06, 0, "io"), (D_AT, 0)]), 0.0)
        W = sk.the_gioi(P)
        dich_tg(P, "all", 0.0, 0.16 * cao * cv(t, [(0, 0), (0.25, 0), (0.56, 1, "out"), (0.62, 1), (T_AT, 0, "in"), (D_AT, 0)]), W)
        f = cv(t, [(0, 0), (0.50, 0), (T_AT, 1, "in"), (0.96, 1), (1.24, 0, "io"), (D_AT, 0)])
        if f > 0:
            dich_tg(P, "bone10", f * 0.36 * cao, f * 0.06 * cao, W)
            dich_tg(P, "bone18", f * 0.22 * cao, f * 0.06 * cao, W)
        ha(P, cv(t, [(0, 0), (0.30, 0), (0.45, 0.8, "out"), (0.60, 0.75), (T_AT - 0.03, 0.0, "in"), (0.92, 0.0), (1.06, 0.25, "io"), (D_AT, 0, "io")]))
        k = cv(t, [(0, 0), (T_AT - 0.01, 0), (T_AT + 0.03, 1, "out"), (T_AT + 0.24, 0, "io")])
        P.scale("bone5", 1 + 0.07 * k, 1 - 0.07 * k)
        ve_bk(P, cv(t, [(0, 1), (0.30, 0.75, "io"), (T_AT - 0.02, 0.75), (T_AT + 0.08, 1.45, "out"), (T_AT + 0.5, 1.0, "io"), (D_AT, 1)]))
    out.append(Clip("attack", D_AT, f_attack, ev=[(0.22, "tu", ""), (T_AT, "trung", "")], trung=T_AT))

    # ---------------- hit: của họ; quỹ đạo vệ tinh văng lệch rồi bật về; hàm bật há
    D_HI = CD["hit_01"][0]

    def f_hit(t, P):
        dat_dang(P, "hit_01", t)
        g = cv(t, [(0, 0), (0.07, 1, "out"), (0.2, 1), (D_HI, 0, "io")])
        ve_bk(P, 1.0 + 0.22 * g)
        ve_tam(P, -0.10 * R * g, 0.06 * R * g)
        ha(P, cv(t, [(0, 0), (0.07, 0.55, "out"), (0.22, 0.45), (0.5, 0, "io")]))
    out.append(Clip("hit", D_HI, f_hit))

    # ---------------- cast "Nguyệt Nhận" (người dùng: "tướng hét gầm lên, các gai sau lưng bắt đầu tách ra nổi lên sau đó lần lượt từng gai xoay
    # hướng vào mục tiêu rồi lao vào"): ngửa gầm, dang tay (skill_05 của họ); mười lưỡi trăng bứt khỏi vành hành tinh, nổi lên thành vòng
    # quạt quanh lưng; lần lượt từng lưỡi xoay mũi về đối thủ, giật lùi lấy đà rồi PHÓNG (rig ẩn lưỡi đúng sự kiện `ban`, VFX lái đường bay
    # tới đối thủ); thân chồm tới theo nhịp phóng; lưỡi mới mọc lại từ vành.
    D_CA = 2.10
    T_GAM = 0.32
    THU = [i for i in range(9, -1, -1) if i not in GAI_AN]   # thứ tự phóng: lưỡi phía trước (gần đối thủ) trước (dạng 1: sáu mảnh vỏ)
    T_BAN = {g: 0.98 + (0.08 if NON else 0.062) * j for j, g in enumerate(THU)}
    BAY_G = 0.20                                        # giây bay (VFX) tới đối thủ: giờ trúng của gai đầu
    DICH = np.array(DICH_RIG if DICH_RIG is not None else [1.25 * cao, 0.42 * cao])   # đích (= xương far; bản xem trước đặt đúng chỗ đối thủ)
    GAI = {g["i"]: g for g in sk.info["gai"]}

    def than_cast(t, P):
        r = cv(t, [(0, 0), (0.12, 0), (0.40, 1, "io"), (0.92, 1), (1.30, 0.45, "io"), (1.75, 0.0, "io"), (D_CA, 0)])
        tron(P, [("idle_01", t, 1.0 - r), ("skill_05", 0.62 + 0.05 * math.sin(2.2 * t), r)])
        rr = rung(t, T_GAM, 0.92)
        P.rot("bone5", cv(t, [(0, 0), (0.15, -3, "io"), (T_GAM + 0.05, 8, "out"), (0.92, 7), (1.10, -6, "io"), (1.6, -5), (1.95, 0, "io")]) + 1.2 * rr)
        P.rot("bone6", cv(t, [(0, 0), (0.15, -6, "io"), (T_GAM + 0.05, 28, "out"), (0.92, 25), (1.10, -6, "io"), (1.6, -4), (1.95, 0, "io")]) + 2.0 * rr)
        k = cv(t, [(0, 0), (0.18, 0), (T_GAM + 0.04, 1, "out"), (0.92, 1), (1.10, 0, "io")])          # đầu phồng nhẹ khi gầm
        P.scale("bone7", 1 + 0.07 * k, 1 + 0.07 * k)
        ha(P, cv(t, [(0, 0), (0.18, 0), (T_GAM, 1, "out"), (0.92, 0.95), (1.08, 0.3, "io"), (1.6, 0.2), (1.85, 0, "io")]) + 0.04 * rr)
        ve_bk(P, cv(t, [(0, 1), (T_GAM, 1.2, "out"), (0.92, 1.15), (1.3, 1.0, "io"), (D_CA, 1)]))

    def gai_dang(i, t, W):
        """vị trí, góc thế giới, tỉ lệ, độ đậm của lưỡi i ở giây t (None = để nguyên trên vành)."""
        t_tach = 0.30 + 0.024 * i
        tf = T_BAN[i]
        t_mo = 1.52 + 0.022 * (9 - i)
        g = GAI[i]
        goc0 = float(LUNG_GOC[i])
        if t < t_tach:
            return None
        if t >= t_mo:                                    # mọc lại từ vành
            k = cv(t, [(t_mo, 0.04), (t_mo + 0.18, 1.12, "out"), (t_mo + 0.32, 1.0, "io")])
            return None if k >= 0.999 and t > t_mo + 0.33 else ("mo", k)
        if t >= t_mo - 1.0 / FPS:                        # một khung ẩn ở đế, tí hon: runtime không nội suy hình mờ từ chỗ phóng về đế
            return ("mo0",)
        if t >= tf:                                      # đã phóng (VFX lái): ẩn, đứng yên ở chỗ phóng
            st = gai_dang(i, tf - 1e-3, W)
            return ("an", st[1], st[2])
        c = W["tam"][:2, 2]
        p0 = W[g["bone"]][:2, 2]                       # đế lưỡi khi còn trên vành (theo dáng thân)
        rad = np.array([math.cos(math.radians(goc0)), math.sin(math.radians(goc0))])
        u1 = hoat.ease((t - t_tach) / 0.14, "out")
        pos = p0 + rad * 0.14 * R * u1
        goc = goc0
        u2 = hoat.ease((t - t_tach - 0.08) / 0.42, "io")
        phi = 90.0 + (goc0 - 90.0) * 1.18
        rh = (1.48 + 0.16 * (i % 2)) * R
        H = c + rh * np.array([math.cos(math.radians(phi)), math.sin(math.radians(phi))])
        H = H + np.array([0.0, 0.025 * R * math.sin(2 * math.pi * t / 0.9 + i)])
        pos = pos * (1 - u2) + H * u2
        goc = goc0 * (1 - u2) + phi * u2
        u3 = hoat.ease((t - (tf - 0.20)) / 0.14, "out")
        if u3 > 0:
            d = DICH - pos
            ga = math.degrees(math.atan2(d[1], d[0]))
            ga = goc + ((ga - goc + 180.0) % 360.0 - 180.0)
            goc = goc * (1 - u3) + ga * u3
            pos = pos - d / (np.hypot(*d) or 1.0) * 0.07 * R * u3 * (1 - hoat.ease((t - (tf - 0.04)) / 0.04, "in"))
        return ("bay", pos, goc)

    def f_cast(t, P):
        than_cast(t, P)
        W = sk.the_gioi(P)
        for i in GAI:
            st = gai_dang(i, t, W)
            if st is None:
                continue
            g = GAI[i]
            if st[0] == "an":
                P.alpha[g["slot"]] = 0.0
                dat_tg(P, g["bone"], st[1], st[2], W)
            elif st[0] == "mo0":
                P.alpha[g["slot"]] = 0.0
                P.scale(g["bone"], 0.04, 0.04)
            elif st[0] == "mo":
                P.scale(g["bone"], st[1], st[1])
            else:
                dat_tg(P, g["bone"], st[1], st[2], W)
    t_tr_cast = round((T_BAN[THU[0]] + BAY_G) * FPS) / FPS + 0.012
    ev = [(0.12, "tu", ""), (T_GAM, "gam", ""), (0.30, "tach", "")] + [(T_BAN[g], "ban", str(g)) for g in THU] + [(t_tr_cast, "trung", "")]
    out.append(Clip("cast", D_CA, f_cast, ev=ev, trung=t_tr_cast))
    info["cast"] = dict(T_BAN=T_BAN, BAY=BAY_G, DICH=DICH, gai_dang=gai_dang, than=than_cast)

    # ---------------- skill "Hằng Tinh Diệt" (người dùng: dang 2 tay ngửa lòng bàn tay, từ từ bay lên trời; thiên thạch lao tới bám quanh
    # đối thủ; ép 2 tay vào nhau phía trước, khối đá co lại (đối thủ co theo); gọi mặt trời trên đầu đối thủ, bắn tia nhiệt lớn, nổ hình nấm).
    # Rig diễn thân: dang tay (dáng dang của skill_05), đổi nắm đấm sang bàn tay xoè ngửa, bay lên (xương all), gọi (hai tay nâng nhịp),
    # ép (dáng vỗ tay của skill_05, hai lòng bàn tay quay vào nhau, run), giơ hai tay quá đầu gọi mặt trời (skill_03 0,56, bỏ cú nhảy của
    # họ), vung hai tay bổ xuống ra lệnh tia nhiệt (skill_03 0,70), hạ xuống đáp đất nặng. Thiên thạch, mặt trời, tia, nổ: lớp VFX.
    D_SK = 4.70
    T_XOE, T_BAY0, T_BAY1, T_HUT = 0.16, 0.36, 1.45, 1.00
    T_EP0, T_EP1, T_GOI, T_TIA, T_NO, T_DAT = 2.15, 2.50, 3.05, 3.40, 3.48, 4.15

    def than_skill(t, P):
        w_dang = cv(t, [(0, 0), (0.06, 0), (0.36, 1, "io"), (T_EP0, 1), (T_EP1, 0, "io")])
        w_ep = cv(t, [(0, 0), (T_EP0, 0), (T_EP1, 1, "io"), (T_GOI - 0.22, 1), (T_GOI, 0, "io")])
        w_gio = cv(t, [(0, 0), (T_GOI - 0.22, 0), (T_GOI, 1, "io"), (T_TIA - 0.13, 1), (T_TIA + 0.05, 0, "io")])
        w_nen = cv(t, [(0, 0), (T_TIA - 0.13, 0), (T_TIA + 0.05, 1, "io"), (T_DAT - 0.25, 0.75, "io"), (T_DAT + 0.05, 1.0, "in"),
                       (D_SK - 0.05, 0.0, "io"), (D_SK, 0)])
        w_idle = max(0.0, 1.0 - w_dang - w_ep - w_gio - w_nen)
        tau_nen = cv(t, [(0, 0.70), (T_TIA + 0.05, 0.70), (T_DAT - 0.02, 0.72), (T_DAT + 0.30, 0.98, "out"), (D_SK, 1.2)])   # thế đã nện (không lấy cú vung của họ)
        xoe = 1.0 if T_XOE <= t < T_TIA - 0.03 else 0.0
        # ép = 60 % dáng vỗ tay + 40 % dáng dang (vai không cụp hẳn che hành tinh); gọi = dáng dang, hai tay nâng cao thành chữ V
        tron(P, [("idle_01", t, w_idle), ("skill_05", 0.62 + 0.04 * math.sin(2 * math.pi * t / 1.6), w_dang + 0.4 * w_ep + w_gio),
                 ("skill_05", 0.235 + 0.01 * math.sin(2 * math.pi * t / 0.5), 0.6 * w_ep),
                 ("skill_03", tau_nen, w_nen, ("bone3",))], xoe=(xoe, xoe))
        bao_ = hoat.bao(t, T_BAY0, T_DAT - 0.1, 0.5, 0.4)
        nang = 0.72 * cao * cv(t, [(0, 0), (T_BAY0, 0), (T_BAY1, 1, "io"), (T_TIA + 0.08, 1.0), (T_DAT, 0, "in")])
        nang += 0.018 * cao * math.sin(2 * math.pi * (t - T_BAY0) / 1.3) * bao_
        nang -= 0.05 * cao * cv(t, [(0, 0), (T_DAT - 0.01, 0), (T_DAT + 0.06, 1, "out"), (T_DAT + 0.35, 0, "io")])
        rr = rung(t, T_EP1 - 0.05, T_GOI - 0.25)
        lean = cv(t, [(0, 0), (0.3, 3, "io"), (T_EP0, 3), (T_EP1, -7, "io"), (T_GOI - 0.2, -8), (T_GOI, 8, "out"), (T_TIA - 0.07, 8),
                      (T_TIA + 0.05, -9, "in"), (T_DAT - 0.1, -4), (T_DAT + 0.1, -7), (D_SK, 0, "io")]) + 1.0 * rr
        P.rot("bone5", lean)
        P.rot("bone6", cv(t, [(0, 0), (0.4, 9, "io"), (T_EP0, 8), (T_EP1, -4, "io"), (T_GOI - 0.2, -4), (T_GOI, 18, "out"), (T_TIA - 0.07, 16),
                              (T_TIA + 0.05, -6, "in"), (T_DAT + 0.2, -2), (D_SK, 0, "io")]) + 1.2 * rr)
        ha(P, cv(t, [(0, 0), (0.25, 0), (0.45, 0.32, "io"), (T_EP0, 0.3), (T_EP0 + 0.15, 0.0, "io"), (T_GOI - 0.22, 0.0), (T_GOI, 1.0, "out"),
                     (T_TIA - 0.05, 0.9), (T_TIA + 0.05, 0.55, "io"), (T_NO + 0.3, 0.4), (T_DAT, 0.0, "io"), (T_DAT + 0.1, 0.3, "out"),
                     (T_DAT + 0.4, 0.0, "io")]) + 0.05 * rr)
        W = sk.the_gioi(P)
        dich_tg(P, "all", 0.0, nang, W)
        if xoe:                                          # lòng bàn tay: ngửa (dang, giơ), quay vào nhau (ép)
            nhip = 0.10 * cao * math.sin(2 * math.pi * (t - T_HUT) / 0.7) * hoat.bao(t, T_HUT, T_EP0, 0.2, 0.2)   # hai tay nâng nhịp gọi đá
            dich_tg(P, "bone10", 0.0, nhip, W)
            dich_tg(P, "bone18", 0.0, nhip, W)
            if w_ep > 0:                                 # ép: hai bàn tay xuống thấp trước bụng (về phía đối thủ, dưới mặt), lòng quay vào nhau, run
                c = W["tam"][:2, 2]
                M = c + np.array([1.0 * R, -1.05 * R])
                hep = 0.50 * R * (1.0 - 0.10 * cv(t, [(0, 0), (T_EP1, 0), (T_GOI - 0.25, 1, "io")])) + 0.012 * cao * rr
                for xb, xh, s_ in (("bone10", "bone96", -1.0), ("bone18", "bone102", 1.0)):
                    d = (M + np.array([s_ * hep, 0.0])) - W[xh][:2, 2]
                    dich_tg(P, xb, w_ep * d[0], w_ep * d[1], W)
            if w_gio > 0:                                # gọi mặt trời: hai tay nâng cao, chếch ra ngoài
                dich_tg(P, "bone10", -0.06 * cao * w_gio, 0.50 * cao * w_gio, W)
                dich_tg(P, "bone18", 0.08 * cao * w_gio, 0.50 * cao * w_gio, W)
            W = sk.the_gioi(P)
            dat_tg(P, "bone96", ang=G0_TO + 14.0 * w_dang - 84.0 * w_ep + 22.0 * w_gio, W=W)
            dat_tg(P, "bone102", ang=G0_NHO - 14.0 * w_dang + 84.0 * w_ep - 22.0 * w_gio, W=W)
        # vệ tinh: bung rộng, bay nhanh khi bay lên; co sát lõi khi ép (như khối đá quanh đối thủ); bung mạnh lúc nổ
        ve_bk(P, cv(t, [(0, 1), (T_BAY1, 1.32, "io"), (T_EP0, 1.3), (T_EP1, 0.62, "io"), (T_GOI - 0.2, 0.55), (T_TIA, 1.0, "io"),
                        (T_NO + 0.08, 1.5, "out"), (T_DAT + 0.4, 1.0, "io"), (D_SK, 1)]))
        ve_quay(P, 360.0 * 2 * cv(t, [(0, 0), (0.3, 0), (T_EP0, 1, "io"), (D_SK, 1)]))

    out.append(Clip("skill", D_SK, than_skill,
                    ev=[(0.05, "tu", ""), (T_BAY0, "bay", ""), (T_HUT, "hut", ""), (T_EP0, "ep", ""), (T_GOI - 0.05, "gam", ""), (T_GOI, "goi", ""),
                        (T_TIA, "tia", ""), (T_NO, "trung", ""), (T_DAT, "cham_dat", "")], trung=T_NO))
    info["skill"] = dict(T_XOE=T_XOE, T_BAY0=T_BAY0, T_BAY1=T_BAY1, T_HUT=T_HUT, T_EP0=T_EP0, T_EP1=T_EP1, T_GOI=T_GOI, T_TIA=T_TIA,
                         T_NO=T_NO, T_DAT=T_DAT, D=D_SK)

    # ---------------- die: của họ, nhưng hành tinh KHÔNG mờ trước (lõi của họ tắt giữa chừng); vệ tinh rơi khỏi quỹ đạo, tan cùng thân;
    # hàm trễ há ra lúc lả đi
    D_DI = CD["die_01"][0]

    def f_die(t, P):
        dat_dang(P, "die_01", t)
        a = float(np.clip(1.0 - (t - D_DI) / (TAN - 0.1), 0.0, 1.0))
        for sl in HT_SLOT:
            P.alpha[sl] = 1.0
        Wd = sk.the_gioi(P)
        roi = max(0.0, float(Wd["ht"][1, 2]) - (info["dat_y"] + 0.93 * R))
        k = cv(t, [(0, 0), (1.42, 0), (1.80, 1.0, "in"), (1.88, 0.94, "out"), (1.98, 1.0, "in"), (D_DI + TAN, 1.0)])
        v = np.linalg.solve(Wd["bone5"][:2, :2], np.array([0.10 * R * k, -roi * k]))
        P.move("ht", float(v[0]), float(v[1]))
        P.rot("ht", -22.0 * cv(t, [(0, 0), (1.42, 0), (2.0, 1, "out"), (D_DI + TAN, 1)]))
        ve_bk(P, cv(t, [(0, 1), (0.15, 1.25, "out"), (1.1, 0.25, "in"), (D_DI, 0.15)]))
        ve_mo(P, cv(t, [(0, 1), (0.9, 1), (1.35, 0)]))
        ha(P, cv(t, [(0, 0), (0.07, 0.6, "out"), (0.35, 0.5), (0.9, 0.85, "io"), (D_DI + TAN, 0.85)]))
        for s_ in sk.slots:
            if s_["name"] != "dat_cat":
                P.alpha[s_["name"]] = a * P.alpha.get(s_["name"], s_["alpha"])
    out.append(Clip("die", D_DI + TAN, f_die))
    thu = {c.ten: c for c in out}
    return [thu[n] for n in ("appear", "idle", "walk", "attack", "cast", "skill", "hit", "die")]


def them_bay(sk, info):
    """xương far (đích mặc định trước mặt; game KHÔNG khai far cho clip nào: gai và mặt trời do VFX lái) và mặt nạ đất của appear."""
    cao = info["cao"]
    sk.xuong("far", "root", 1.25 * cao, 0.42 * cao)
    cuoi = [x["name"] for x in sk.slots][-1]
    y0 = sk.W0["dat_cat"][1, 2]
    sk.cat("dat_cat", cuoi, [(-9000.0, y0), (9000.0, y0), (9000.0, y0 + 9000.0), (-9000.0, y0 + 9000.0)])


def aura_frames(sk, info):
    """clip nền lặp T_AURA giây (runtime phủ lên mọi clip): hố hành tinh trôi (hành tinh tự quay), vệ tinh bay vòng (nửa gần trước lõi,
    nửa xa sau lõi, to nhỏ theo xa gần). Tự nướng (không hoà khung cuối: góc quay đều nhiều vòng)."""
    n = int(round(T_AURA * FPS))
    out = []
    for i in range(n + 1):
        t = i / FPS
        P = Pose()
        for h in sk.info["ho"]:
            th = math.radians(h["kd"]) + 2 * math.pi * QUAY_HT * t / T_AURA
            c = math.cos(th)
            P.move(f"ho_{h['i']}", h["rl"] * math.sin(th), 0.0)
            P.scale(f"ho_{h['i']}", max(0.03, c) if c > 0 else 0.03, 1.0)
            P.alpha[f"ho_{h['i']}"] = 1.0 if c > 0.06 else 0.0
        for q in sk.info["quy"]:
            j = q["j"]
            d = 360.0 * q["vong"] * t / T_AURA
            P.rot(f"quy_{j}", d)
            P.rot(f"quy2_{j}", -2 * d)
            P.rot(f"dao_{j}", d)
            psi = math.radians(q["pha"] + d)
            gan = math.sin(psi) < 0                          # nửa dưới elip = phía người xem
            k = 1.0 - 0.16 * math.sin(psi)
            P.scale(f"dao_{j}", k, k)
            P.alpha[f"ve_{j}_f"] = 1.0 if gan else 0.0
            P.alpha[f"ve_{j}_b"] = 0.0 if gan else 1.0
        out.append(P)
    return out


def dung_het():
    sk, info = dung()
    fr_aura = aura_frames(sk, info)
    ve0 = soi.Ve(sk)
    bo = tuple(s["name"] for s in sk.slots if s["name"].startswith(("ve_", "ho_")))
    info["cao"] = float(soi.chieu_cao(ve0, hoat.phu_aura([Pose()], fr_aura, sk)[0], bo=bo))
    lam_clip(sk, info)                       # lượt 1: lấy dáng thân ở giờ rời để đặt bản sao bay
    them_bay(sk, info)
    clips = lam_clip(sk, info)
    aura = Clip("aura", T_AURA, lambda t, P: None, loop=True)
    print(f"chiều cao {info['cao']:.0f}")
    return sk, info, clips + [aura], {"aura": fr_aura}


def main_soi(sk, ve0, c, fr, aura, spec, sc):
    if c.ten != "aura":
        fr = hoat.phu_aura(fr, aura, sk)
    if ":" in spec:
        t0, t1, n = spec.split(":")
        ts = list(np.linspace(float(t0), float(t1), int(n)))
    elif spec.startswith("n="):
        ts = list(np.linspace(0, c.dur, int(spec[2:])))
    else:
        ts = [float(x) for x in spec.split(",")]
    Ps = [fr[min(len(fr) - 1, int(round(t * FPS)))] for t in ts]
    Bx = soi._union([ve0.bao(P) for P in Ps], 0.04)
    cot = min(len(Ps), 6)
    hang = (len(Ps) + cot - 1) // cot
    out = None
    for i, P in enumerate(Ps):
        im = ve0.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB")
        ImageDraw.Draw(im).text((6, 4), f"{c.ten} {ts[i]:.2f}", fill=(255, 255, 255))
        if out is None:
            out = Image.new("RGB", (im.width * cot, im.height * hang), (150, 150, 150))
        out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
    os.makedirs(RA, exist_ok=True)
    pth = os.path.join(RA, f"soi_{c.ten}.png")
    out.save(pth)
    print(pth, out.size)


def main(a):
    sk, info, clips, frames = dung_het()
    ve0 = soi.Ve(sk)
    if a and a[0] == "soi":
        for c in clips:
            if a[1] in ("all", c.ten):
                fr = frames.get(c.ten) or hoat.nuong(sk, c)
                main_soi(sk, ve0, c, fr, frames["aura"], a[2] if len(a) > 2 else "n=12", float(a[3]) if len(a) > 3 else 0.3)
        return
    if a and a[0] == "kiem":
        for c in clips:
            fr = frames.get(c.ten) or hoat.nuong(sk, c)
            mx, ai = 0.0, ""
            for i in range(1, len(fr)):
                for b in set(fr[i].t) | set(fr[i - 1].t):
                    d = abs(fr[i].t.get(b, khung.ZERO)[2] - fr[i - 1].t.get(b, khung.ZERO)[2])
                    if d > mx and not b.startswith(("quy", "dao")):
                        mx, ai = d, f"{b} {i / FPS:.2f}s"
            print(f"{c.ten}: {len(fr)} khung, bước xoay lớn nhất {mx:.0f}° ({ai})")
        return
    xuat.xuat_het(sk, clips, RA, TEN, tieu_de=("Tiểu Thổ Tinh (thach_de_non): dạng 1" if NON else "Thổ Tinh (thach_de_1)") + ", final boss đảo Thổ",
                  frames=frames, dang=1, so_dang=2 if NON else 1,
                  dung_yen=("cast", "skill"), lao=("attack",), far=(), ma_goc=None, khop_idle=0.2, cao=info["cao"],
                  tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.5, tran_mb=0.9, span=SPAN)


if __name__ == "__main__":
    main(sys.argv[1:])
