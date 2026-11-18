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
TEN = f"{CODE}_1"
BASE = os.path.join(HERE, "inbox", TEN)
MANH = os.path.join(BASE, "manh")
RA = os.path.join(BASE, "rig")


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
CLIPS = [("appear", "generate_01", False), ("idle", "idle_01", True), ("walk", "run_01", True), ("attack", "skill_01_1", False),
         ("cast", "skill_05", False), ("skill", "skill_03", False), ("hit", "hit_01", False), ("die", "die_01", False)]
TAN = 0.5
SAU = 3000.0                 # mặt nạ đất nằm sâu chừng này (đơn vị rig mình) khi không dùng
# slot của nắm đấm trái (mặt trăng to + đốt tay): chiêu cuối ném đi rồi mọc lại
TAY_NEM = ["P_R_xiaobi06", "P_R_shouzhi04", "P_R_shouzhi03", "P_R_shouzhi05", "P_R_shouzhi02"]

_C = {}


def nap():
    if not _C:
        sc = scan()
        _C["I"] = json.load(open(os.path.join(sc, "info.json"), encoding="utf-8"))
        _C["A0"] = json.load(open(os.path.join(sc, "att_idle0.json"), encoding="utf-8"))
        _C["S"] = json.load(open(os.path.join(sc, "sample.json"), encoding="utf-8"))
        _C["hop"] = json.load(open(os.path.join(BASE, "mau", "goc_ca_con.json")))
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
    tam_tg = tg(*TAM) * KG
    R = RHT / s_ * KG
    for k, sl in enumerate(LUNG):
        g = math.radians(LUNG_GOC[k])
        bang[sl] = (LUNG_ANH[k], None, None, LUNG_CAO[k], LUNG_GOC[k] - 90.0, (TAM[0] + (RHT - 16) * math.cos(g), TAM[1] - (RHT - 16) * math.sin(g)))
    dung_slot = {slots.index(sl) for sl in bang}
    tinh, cac, cho = thu_tu_ve(S, slots, dung_slot, {slots.index("P_shenti01")})

    def them_anh(a, cao_px):
        g = Image.open(os.path.join(MANH, a + ".png"))
        k = cao_px / g.height * PXU / s_
        key = f"{a}_{int(round(cao_px))}"
        if key not in sk.images:
            sk.anh(key, anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * k)), max(2, round(g.height * k))), Image.LANCZOS).convert("RGBA")))
        return key

    TI = KG / PXU

    def dat_manh(slot_ten, xuong, spec, an=False):
        a, px, py, cao_px, goc = spec[:5]
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
    for j, (a, dk, ra_, rb_, vong, pha, cy_) in enumerate(VE):
        A_, B_ = (ra_ + rb_) / 2 / s_ * KG, (ra_ - rb_) / 2 / s_ * KG
        cy_ = cy_ / s_ * KG
        sk.xuong(f"quy_{j}", "tam", 0.0, cy_, goc=NGHIENG + pha)
        sk.xuong(f"quy2_{j}", f"quy_{j}", A_, 0.0, goc=-2 * pha)
        sk.xuong(f"dao_{j}", f"quy2_{j}", B_, 0.0, goc=pha - NGHIENG)
        quy.append(dict(j=j, anh=a, dk=dk, vong=vong, pha=pha, cy=cy_))

    ten_slot = {}                                            # slot của họ → [(chỗ chèn | None, tên slot của mình)]
    idle_cho = cho(S["idle_01"]["frames"][0]["o"])

    def them_dong(k):
        for s in sorted(cac):
            if k in cac[s]:
                nm = f"{slots[s]}@{k}"
                dat_manh(nm, bam[slots[s]], bang[slots[s]], an=(idle_cho.get(s) != k))
                ten_slot.setdefault(s, []).append((k, nm))

    for k, s in enumerate(tinh):
        them_dong(k)
        sl = slots[s]
        if sl == "P_shenti01":
            for q in quy:                                    # nửa xa của quỹ đạo: sau hành tinh
                key = them_anh(q["anh"], q["dk"])
                p = sk.W0[f"dao_{q['j']}"][:2, 2]
                sk.slot(f"ve_{q['j']}_b", f"dao_{q['j']}", key)
                sk.manh(f"ve_{q['j']}_b", key, Dat(p[0], p[1], ti=TI))
        dat_manh(sl, "ht" if sl == "P_shenti01" else bam[sl], bang[sl])
        ten_slot[s] = [(None, sl)]
        if sl == "P_shenti01":
            for i, (a, vi, kd, cao_px) in enumerate(HO):     # hố: xương con của tam, ở vĩ độ vi
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
    for e, m in (("trung", "khung đòn trúng"), ("tu", "bắt đầu tụ lực"), ("nem", "vệ tinh rời quỹ đạo"), ("cham_dat", "nện xuống đất"),
                 ("troi", "bắt đầu trồi lên"), ("xong", "đứng vững")):
        sk.su_kien(e, m)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {len(sk.images)} ảnh")
    return sk, dict(S=S, ten=ten, ix=ix, slots=slots, ten_slot=ten_slot, cho=cho, R=R, tam=tam_tg, IB=IB, L0=L0, dat_y=dat_y)


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
    ten_slot, cho = info["ten_slot"], info["cho"]

    def noi(arr, x):
        n = len(arr)
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        return np.asarray(arr[i0], float) * (1 - w) + np.asarray(arr[i1], float) * w

    def dat_dang(P, goc, tau, lap=False, bo=()):
        dur, Rm, fr = CD[goc]
        x = (tau % dur if lap else min(max(tau, 0.0), dur)) * FPS
        for b, arr in Rm.items():
            if b in bo:
                continue
            v = noi(arr, x)
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        F = fr[min(int(round(x)), len(fr) - 1)]
        vt = cho(F["o"])
        for s, ds in ten_slot.items():
            a = float(F["a"][s]) if F["n"][s] else 0.0
            for k, nm in ds:
                P.alpha[nm] = a if (k is None or vt.get(s) == k) else 0.0

    info["dat_dang"], info["CD"] = dat_dang, CD
    cv = hoat.cv
    quy = sk.info["quy"]
    NQ = len(quy)
    AB = {q["j"]: (sk.bones[sk.bi[f"quy2_{q['j']}"]]["x"], sk.bones[sk.bi[f"dao_{q['j']}"]]["x"]) for q in quy}
    cao = info["cao"]
    R = info["R"]
    VE_SLOT = [f"ve_{q['j']}_{c}" for q in quy for c in "bf"]
    HT_SLOT = ["P_shenti01"] + [f"ho_{h['i']}" for h in sk.info["ho"]]

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

    def tam_tg_luc(fn, t):
        P = Pose()
        fn(t, P)
        return sk.the_gioi(P)

    out = []
    # ---------------- idle (10 s của họ, có cú đấm tay vào lòng bàn tay ở giây 6), walk
    out.append(Clip("idle", CD["idle_01"][0], lambda t, P: dat_dang(P, "idle_01", t, True), loop=True))
    out.append(Clip("walk", CD["run_01"][0], lambda t, P: dat_dang(P, "run_01", t, True), loop=True))

    # ---------------- appear: trồi lên từ đất như trăng mọc (mặt nạ đất), vệ tinh bung ra từ sau hành tinh khi đã đứng vững
    D_AP = CD["generate_01"][0]

    def f_appear(t, P):
        dat_dang(P, "generate_01", t)
        # mặt nạ ở mặt đất tới 1,6 s, rồi hạ dần 260 đơn vị (nắm đấm phía gần nằm thấp hơn chân theo phối cảnh) và rút hẳn ở 2,5 s
        P.move("dat_cat", 0.0, SAU * cv(t, [(0, 1), (2.5, 1), (2.51, 0)]) - 260.0 * cv(t, [(0, 0), (1.6, 0), (2.5, 1, "io")]))
        k = cv(t, [(0, 0.0), (D_AP - 0.95, 0.0), (D_AP - 0.35, 1.12, "out"), (D_AP, 1.0)])
        ve_bk(P, k)
        ve_mo(P, cv(t, [(0, 0), (D_AP - 0.95, 0), (D_AP - 0.8, 1)]))
    out.append(Clip("appear", D_AP, f_appear, ev=[(0.0, "troi", ""), (D_AP - 0.9, "xong", "")]))

    # ---------------- attack: cú đấm của họ (skill_01_1), lao tới bằng xương move; quỹ đạo vệ tinh giật nở lúc trúng
    T_TR = 0.55
    D_AT = CD["skill_01_1"][0]

    def f_attack(t, P):
        dat_dang(P, "skill_01_1", t)
        P.move("move", 0.55 * cao * cv(t, [(0, 0), (0.22, 0), (T_TR - 0.05, 1, "in"), (T_TR + 0.2, 1), (D_AT - 0.1, 0, "io"), (D_AT, 0)]), 0.0)
        ve_bk(P, cv(t, [(0, 1), (0.3, 0.82, "io"), (T_TR, 0.82), (T_TR + 0.08, 1.3, "out"), (T_TR + 0.45, 1.0, "io"), (D_AT, 1)]))
    out.append(Clip("attack", D_AT, f_attack, ev=[(T_TR, "trung", "")], trung=T_TR))

    # ---------------- hit: của họ; quỹ đạo vệ tinh văng lệch rồi bật về
    D_HI = CD["hit_01"][0]

    def f_hit(t, P):
        dat_dang(P, "hit_01", t)
        g = cv(t, [(0, 0), (0.07, 1, "out"), (0.2, 1), (D_HI, 0, "io")])
        ve_bk(P, 1.0 + 0.22 * g)
        ve_tam(P, -0.10 * R * g, 0.06 * R * g)
    out.append(Clip("hit", D_HI, f_hit))

    # ---------------- cast "Nguyệt Xạ": vỗ tay gom vệ tinh thành cụm xoáy trên đầu, dang tay phóng từng viên tới đối thủ, vệ tinh mới
    # mọc ra từ sau hành tinh. Thân: skill_05 của họ (vỗ 0–0,27; dang 0,36–0,55) giãn giờ.
    D_CA = 1.5

    def _tam_anh(sl):
        sp = next(iter(sk.atts[sl].values()))
        return np.array([sp["x"], sp["y"], 1.0])
    C_G, C_X = _tam_anh("P_R_xiaobi06"), _tam_anh([n for n in sk.si if n.startswith("P_L_xiaobi05")][0])

    def giua_tay(P):
        """điểm giữa hai mặt trăng nắm đấm (thế giới) và ma trận `tam` ở tư thế P: chỗ gom vệ tinh (hai tay vỗ vào đó)."""
        Wd = sk.the_gioi(P)
        m = ((Wd["bone96"] @ C_G)[:2] + (Wd["bone102"] @ C_X)[:2]) / 2
        return m, Wd["tam"]
    T_BAN = [0.66 + 0.055 * j for j in range(NQ)]     # giờ từng viên rời cụm
    BAY = 0.20                                        # giây bay tới đối thủ

    def than_cast(t, P):
        tau = cv(t, [(0, 0), (0.26, 0.27, "io"), (0.56, 0.30), (0.74, 0.52, "out"), (1.08, 0.60), (D_CA, 1.0, "io")])
        dat_dang(P, "skill_05", tau)

    def f_cast(t, P):
        than_cast(t, P)
        g = cv(t, [(0, 0), (0.06, 0), (0.40, 1, "io"), (1.02, 1), (1.03, 0)])          # mức gom
        ve_bk(P, 1.0 - 0.90 * g)
        if g > 0:
            m, Wt = giua_tay(P)
            gl = np.linalg.solve(Wt, np.array([m[0], m[1], 1.0]))
            for q in quy:
                ve_tam(P, float(gl[0]) * g, (float(gl[1]) - q["cy"]) * g, q["j"])
        for q in quy:
            j = q["j"]
            d = 360.0 * 2 * cv(t, [(0, 0), (0.06, 0), (0.66, 1, "in"), (D_CA, 1)])       # cụm xoáy thêm hai vòng (khép bội 360°)
            P.rot(f"quy_{j}", d)
            P.rot(f"quy2_{j}", -2 * d)
            P.rot(f"dao_{j}", d)
            tb = T_BAN[j]
            if tb <= t < 1.03:
                ve_mo(P, 0.0, j)                                                      # viên thật ẩn từ lúc bản sao rời cụm
            if t >= 1.03:                                                             # mọc lại từ sau hành tinh
                kk = cv(t, [(1.03, 0.0), (1.38, 1.1, "out"), (D_CA, 1.0)])
                P.move(f"quy2_{j}", (kk - 1.0) * AB[j][0], 0.0)
                P.move(f"dao_{j}", (kk - 1.0) * AB[j][1], 0.0)
                ve_mo(P, cv(t, [(1.03, 0), (1.12, 1)]), j)
            # bản sao bay
            f_ = (t - tb) / BAY
            if 0.0 <= f_ < 1.0 - 1e-6 and f"fly_{j}" in sk.bi:
                x0, y0 = sk.W0[f"fly_{j}"][:2, 2]
                fx, fy = sk.W0["far"][:2, 2]
                e = f_ * f_ * (3 - 2 * f_) * 0.25 + f_ * 0.75
                P.move(f"fly_{j}", e * (fx - x0), e * (fy - y0))
                P.rot(f"bay_{j}", -540.0 * f_)
                P.alpha[f"bay_{j}"] = 1.0
            elif f"bay_{j}" in sk.si:
                P.alpha[f"bay_{j}"] = 0.0
                if f_ >= 1.0 - 1e-6 and f"fly_{j}" in sk.bi:                           # ở lại đích (đã ẩn) kẻo runtime nội suy ngược về
                    x0, y0 = sk.W0[f"fly_{j}"][:2, 2]
                    fx, fy = sk.W0["far"][:2, 2]
                    P.move(f"fly_{j}", fx - x0, fy - y0)
    t_tr_cast = round((T_BAN[0] + BAY) * FPS) / FPS + 0.012
    out.append(Clip("cast", D_CA, f_cast, ev=[(0.12, "tu", ""), (T_BAN[0], "nem", ""), (t_tr_cast, "trung", "")], trung=t_tr_cast))
    info["cast"] = dict(than=than_cast, T_BAN=T_BAN, giua=giua_tay)

    # ---------------- skill "Nguyệt Lạc": nhún, nhảy vọt lên (skill_03 của họ), ở đỉnh ném MẶT TRĂNG NẮM ĐẤM xuống đối thủ, rơi nện đất,
    # mặt trăng mới mọc lại ở cổ tay. Vệ tinh co sát lõi lúc nhún, bung rộng lúc nện.
    D_SK = 2.2
    T_NEM, BAY_S = 0.86, 0.30
    T_DAT = 1.30

    def than_skill(t, P):
        tau = cv(t, [(0, 0), (0.42, 0.26, "io"), (0.70, 0.50, "out"), (T_NEM + 0.12, 0.60), (T_DAT, 0.78, "in"), (D_SK, 1.67, "io")])
        dat_dang(P, "skill_03", tau)

    def f_skill(t, P):
        than_skill(t, P)
        ve_bk(P, cv(t, [(0, 1), (0.40, 0.55, "io"), (0.70, 0.75), (T_DAT - 0.02, 0.7), (T_DAT + 0.10, 1.45, "out"), (T_DAT + 0.6, 1.0, "io"), (D_SK, 1)]))
        d = 360.0 * cv(t, [(0, 0), (0.2, 0), (T_DAT, 1, "in"), (D_SK, 1)])                # thêm một vòng lúc lấy đà (khép 360°)
        for q in quy:
            j = q["j"]
            P.rot(f"quy_{j}", d)
            P.rot(f"quy2_{j}", -2 * d)
            P.rot(f"dao_{j}", d)
        # nắm đấm trái: ẩn từ lúc ném, mọc lại
        if t >= T_NEM:
            a = cv(t, [(T_NEM, 0), (T_DAT + 0.12, 0), (T_DAT + 0.18, 1)])
            for sl in TAY_NEM:
                P.alpha[sl] = a * P.alpha.get(sl, 1.0)
            k = cv(t, [(T_NEM, 0.05), (T_DAT + 0.12, 0.05), (T_DAT + 0.42, 1.14, "out"), (T_DAT + 0.62, 1.0, "io")])
            P.scale("bone10", k, k)
        f_ = (t - T_NEM) / BAY_S
        if "fly_n" in sk.bi:
            x0, y0 = sk.W0["fly_n"][:2, 2]
            fx, fy = sk.W0["far"][:2, 2]
            if 0.0 <= f_ < 1.0 - 1e-6:
                e = f_ * f_
                P.move("fly_n", e * (fx - x0), e * (fy - y0))
                P.rot("nem", -300.0 * f_)
                P.scale("nem", 1.0 + 0.55 * f_)
                P.alpha["nem"] = 1.0
            else:
                P.alpha["nem"] = 0.0
                if f_ >= 1.0 - 1e-6:
                    P.move("fly_n", fx - x0, fy - y0)
    t_tr_sk = round((T_NEM + BAY_S) * FPS) / FPS + 0.012
    out.append(Clip("skill", D_SK, f_skill, ev=[(0.05, "tu", ""), (T_NEM, "nem", ""), (t_tr_sk, "trung", ""), (T_DAT, "cham_dat", "")], trung=t_tr_sk))
    info["skill"] = dict(than=than_skill, T_NEM=T_NEM)

    # ---------------- die: của họ, nhưng hành tinh KHÔNG mờ trước (lõi của họ tắt giữa chừng); vệ tinh rơi khỏi quỹ đạo, tan cùng thân
    D_DI = CD["die_01"][0]

    def f_die(t, P):
        dat_dang(P, "die_01", t)
        a = float(np.clip(1.0 - (t - D_DI) / (TAN - 0.1), 0.0, 1.0))
        for sl in HT_SLOT:
            P.alpha[sl] = 1.0
        # hành tinh rơi xuống nằm trên đất giữa đống đá (lõi của họ tắt nên xương lõi không rơi), lăn nhẹ rồi nằm yên
        Wd = sk.the_gioi(P)
        roi = max(0.0, float(Wd["ht"][1, 2]) - (info["dat_y"] + 0.93 * R))
        k = cv(t, [(0, 0), (1.42, 0), (1.80, 1.0, "in"), (1.88, 0.94, "out"), (1.98, 1.0, "in"), (D_DI + TAN, 1.0)])
        v = np.linalg.solve(Wd["bone5"][:2, :2], np.array([0.10 * R * k, -roi * k]))
        P.move("ht", float(v[0]), float(v[1]))
        P.rot("ht", -22.0 * cv(t, [(0, 0), (1.42, 0), (2.0, 1, "out"), (D_DI + TAN, 1)]))
        ve_bk(P, cv(t, [(0, 1), (0.15, 1.25, "out"), (1.1, 0.25, "in"), (D_DI, 0.15)]))
        ve_mo(P, cv(t, [(0, 1), (0.9, 1), (1.35, 0)]))
        for s_ in sk.slots:
            if s_["name"] != "dat_cat":
                P.alpha[s_["name"]] = a * P.alpha.get(s_["name"], s_["alpha"])
    out.append(Clip("die", D_DI + TAN, f_die))
    thu = {c.ten: c for c in out}
    return [thu[n] for n in ("appear", "idle", "walk", "attack", "cast", "skill", "hit", "die")]


def them_bay(sk, info):
    """xương far, bản sao vệ tinh bay (cast) và mặt trăng ném (skill): đặt ở đúng chỗ rời thân, tính từ dáng của clip ở giờ rời."""
    cao = info["cao"]
    TI, them_anh = sk.info["TI"], sk.info["them_anh"]
    sk.xuong("far", "root", 1.25 * cao, 0.42 * cao)
    c = info["cast"]
    for q in sk.info["quy"]:
        j = q["j"]
        P = Pose()
        c["than"](c["T_BAN"][j], P)
        g, _ = c["giua"](P)
        sk.xuong(f"fly_{j}", "root", float(g[0]), float(g[1]))
        sk.xuong(f"bay_{j}", f"fly_{j}", 0.0, 0.0)
        key = them_anh(q["anh"], max(96.0, q["dk"] * 1.3))
        sk.slot(f"bay_{j}", f"bay_{j}", key, an=True)
        sk.manh(f"bay_{j}", key, Dat(float(g[0]), float(g[1]), ti=TI))
    s = info["skill"]
    P = Pose()
    s["than"](s["T_NEM"], P)
    Wb = sk.the_gioi(P)["bone96"]
    # tâm mặt trăng to trong hệ bone96 = tâm ảnh ở dáng gốc
    a = sk.atts["P_R_xiaobi06"]
    spec = next(iter(a.values()))
    m = Wb @ np.array([spec["x"], spec["y"], 1.0])
    sk.xuong("fly_n", "root", float(m[0]), float(m[1]))
    sk.xuong("nem", "fly_n", 0.0, 0.0)
    key = [k for k in sk.images if k.startswith("trang_to_")][0]
    sk.slot("nem", "nem", key, an=True)
    sk.manh("nem", key, Dat(float(m[0]), float(m[1]), ti=TI))
    # mặt nạ đất: mọi slot (trừ bản sao bay) chỉ còn phần trên mặt đất khi dat_cat được nâng lên
    cuoi = [x["name"] for x in sk.slots if not x["name"].startswith(("bay_", "nem"))][-1]
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
    xuat.xuat_het(sk, clips, RA, TEN, tieu_de="Thổ Tinh (thach_de_1): final boss đảo Thổ", frames=frames, dang=1, so_dang=1,
                  dung_yen=("cast", "skill"), lao=("attack",), far=("cast", "skill"), ma_goc=None, khop_idle=0.2, cao=info["cao"],
                  tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.5, tran_mb=0.9)


if __name__ == "__main__":
    main(sys.argv[1:])
