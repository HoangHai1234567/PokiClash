# -*- coding: utf-8 -*-
"""Thiên thạch thú D2 "lưng rừng tinh thể" (tinh_hach; tướng 9 đảo Thổ, ải 60, mini boss): hình của mình chạy trên ĐÚNG rig của con gốc
monster_3806 (quái thú gù ôm chuỗi quả cầu; game tham khảo). Ghi chú: inbox/tho9_ghichu.md. Cách làm như quy_nui_rig.py, thêm:
- XƯƠNG dựng ở KHUNG 0 IDLE (mảnh của mình đặt theo hình khung 0 idle; dáng gốc của rig lệch tới ~140 đơn vị ở ngón tay). Rig gốc có 20
  xương kế thừa kiểu "noRotationOrReflection" (all5, all6 đầu, all7-9, shenti_03/04 ...): bộ dựng .atomik chỉ có kế thừa thường, nên góc
  riêng của các xương đó = góc thế giới của nó − góc thế giới của cha (trường `m` của mẫu khung); vị trí riêng vẫn lấy `l`.
- BỎ của họ: vòng, mây, sao, mảng tinh vân, thân rồng biến hình `shenti_z*` (skill_03), đuôi chạc `weiba`.
- MẢNH (tinh_hach_manh.py → inbox/tinh_hach_1/manh/): thân, đầu, hàm, lòng miệng, hai tay gắn trên NHÓM lưới gốc (gan_goc); móng cứng
  trên xương ngón nặng nhất; 5 cụm tinh thể bay cứng trên xương quả cầu qiu_* (gán theo chỗ); rừng tinh thể sau thân bám hai xương
  riêng tt_sau (con all4) / tt_truoc (con all5) hoà theo bề ngang; tinh thể lớn vắt vai trên xương riêng tt_nam_g (con all5); đuôi là
  chuỗi ba xương riêng duoi0..2 (con all3) có sóng trễ ở mọi clip.
- CLIP (đề xuất ở trang so, người dùng "làm D2" 2026-11-17):
    appear = rơi từ trời như thiên thạch, đáp nện, 5 cụm tinh thể trồi lên quanh chân, rừng tinh thể dựng lên, gầm;
    idle   = sóng mềm lệch pha (thở, đầu, hàm, tay, đuôi, cụm bay nhấp nhô) + trò: lắc đầu rũ mình, rừng tinh thể rung lách cách;
    walk   = run_01; hit = hit_01; die = die_01 + tan;
    attack = skill_01_1 (vồ tay gần nện xuống);
    cast   = skill_02: giơ tay, 5 cụm tinh thể bay lên xoay quanh rồi lần lượt lao vào đối thủ (code lái đích qua far / fly_*), mọc lại;
    skill  = MƯA THIÊN THẠCH: thu mình, gầm, cả rừng tinh thể trên lưng phóng vọt lên trời (mưa xuống đối thủ là VFX), nện hai tay,
             tinh thể mọc lại.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tinh_hach_rig.py     → inbox/tinh_hach_1/rig/
    py -3 -I ArtGen/Spine/tinh_hach_rig.py soi <clip> <giây,...|n=12|t0:t1:n> [tỉ lệ]       → rig/soi_<clip>.png
    py -3 -I ArtGen/Spine/tinh_hach_rig.py kiem                                              đo góc nhảy / bước dời từng clip
"""
import itertools
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
import tho9  # noqa: E402,F401
import tho5  # noqa: E402
import quy_nui_rig as QR  # noqa: E402
from hoa_ho_rig import ease, tmap, _goc  # noqa: E402

G = tho5.dat("tinh_hach")
TEN_RIG = "tinh_hach_1"
D_PX = float(os.environ.get("TH_DPX", "0.42"))       # pixel ảnh atlas cho mỗi đơn vị rig
MANH = os.path.join(G.BASE, "manh")
QR.G, QR.MANH, QR.D_PX = G, MANH, D_PX               # các hàm dùng chung của quy_nui_rig đọc ba biến này
RA = os.environ.get("TH_RA") or os.path.join(G.BASE, "rig")
TAN = 0.45
FPS = 30.0
IMPACT = {"attack": (0.14, 0.95, 0.16), "cast": (0.14, 0.8, 0.15), "skill": (0.30, 2.4, 0.26, "#fff3d0a0")}
BO_TIEN_TO = ("shadow", "xing", "xiongkong", "yun_", "jinhuan", "jinghuan", "shenti_z", "zs_z", "ys_z", "long")

# mảnh của mình (thứ tự vẽ sau → trước) → slot gốc dùng làm lưới gắn
MANH_GOC = [
    ("duoi", None), ("tay_xa", ["dabi_l", "xiaobi_l", "shouzhang_l", "xiaomuzhi_l", "zhongzhi_l", "shizhi_l", "damuzhi_l"]),
    ("rung", None), ("than", ["shenti_02", "shenti_04", "shenti_03"]), ("tt_nam", None),
    ("long_mieng", ["zuiba_01"]), ("ham", ["zuiba_02"]),
    ("tay_gan", ["dabi_r", "damuzhi_r", "shizhi_r", "xiaobi_r", "zhongzhi_r", "xiaomuzhi_r"]), ("dau", ["tou"]),
]
NGON_GOC = {"gan": ["damuzhi_r", "shizhi_r", "zhongzhi_r", "xiaomuzhi_r"], "xa": ["shouzhang_l", "xiaomuzhi_l", "zhongzhi_l", "shizhi_l",
                                                                               "damuzhi_l"]}
CUM_QIU = ["qiu_01", "qiu_02", "qiu_03", "qiu_04", "qiu_05", "qiu_06", "qiu_07"]
MUOT = {"than": 6, "tay_gan": 5, "tay_xa": 5, "ham": 2, "long_mieng": 3}
TAY_GAN = ("dabi_r", "xiaobi_r", "xiaobi_r2")          # bắp, cẳng, bàn (bên trái tranh)
TAY_XA = ("dabi_l", "xiaobi_l", "shouzhang_l")         # bên phải tranh
DUOI = ("duoi0", "duoi1", "duoi2")

# DẠNG 1 "Thiên Thạch Thú Non" (TH_DANG=non; người dùng 2026-11-18: "làm dạng 1", chọn cùng rig 3806, concept A "mầm tinh thể"; ghi chú
# inbox/tinh_hach_non_ghichu.md). Cùng xương / lưới / clip; xương của họ nhân tỉ lệ inbox/tinh_hach_non/mau/ti_le.json NGAY sau khi dựng.
# Mảnh dạng 2 dùng lại (thân, hai tay, móng, lòng miệng, quả cầu) gắn ở khung dạng 2 (tạm trả tỉ lệ về gốc: co theo xương như bố cục);
# mảnh mới (đầu, hàm, mầm tinh thể, đuôi, ba thiên thạch: inbox/tinh_hach_non/manh, hộp px concept A) và xương riêng (đuôi, tt_*, quỹ đạo,
# quả cầu) đặt thẳng theo concept A qua tinh_hach_non.tf() trên bộ xương đã co. Không có tinh thể vắt vai (concept A không có).
NON = os.environ.get("TH_DANG", "") == "non"
if NON:
    import tinh_hach_non as THN  # noqa: E402
    TEN_RIG = "tinh_hach_non"
    RA = os.environ.get("TH_RA") or os.path.join(HERE, "inbox", "tinh_hach_non", "rig")
    TI_NON = json.load(open(os.path.join(THN.MAU, "ti_le.json"), encoding="utf-8"))
    MANH_MOI = ("dau", "ham", "rung", "duoi")          # + cum1..3
    DUOI_J_NON = [[545.0, 772.0], [430.0, 820.0], [310.0, 842.0], [185.0, 815.0]]   # px concept A: gốc (khuất) → chóp lưỡi
    Y_CHAN_MAM = 330.0                                  # px concept A: chân ba mầm tinh thể trên sống lưng


def la_moi(ten_m):
    return NON and (ten_m in MANH_MOI or ten_m.startswith("cum"))


def ap_ti(sk, bat):
    """dạng non: bat=True đặt tỉ lệ ti_le.json lên các xương của họ (đã có), False trả về dáng gốc dạng 2; tính lại W0."""
    if "ti_goc" not in sk.info:
        sk.info["ti_goc"] = {nm: {k: sk.bones[sk.bi[nm]][k] for k in ("x", "y", "sx", "sy")} for nm in TI_NON if nm in sk.bi}
    for nm, g in sk.info["ti_goc"].items():
        b = sk.bones[sk.bi[nm]]
        b.update(g)
        if bat:
            k = TI_NON[nm]
            if isinstance(k, dict):
                b["x"] += k.get("dx", 0.0)
                b["y"] += k.get("dy", 0.0)
                k = k.get("s", 1.0)
            b["sx"] *= k
            b["sy"] *= k
    sk.W0 = sk.the_gioi(khung.Pose())
    sk.info["ti_bat"] = bat


class Khung2:
    """with Khung2(sk): gắn mảnh dạng 2 ở dáng gốc dạng 2 (điểm gắn lưu theo hệ xương nên ra khỏi khối là co theo xương)."""

    def __init__(self, sk):
        self.sk = sk

    def __enter__(self):
        if NON:
            ap_ti(self.sk, False)

    def __exit__(self, *a):
        if NON:
            ap_ti(self.sk, True)


# ---------------------------------------------------------------- nạp, chuyển động của họ đã đổi về kế thừa thường
def nap():
    scan = G.scan()
    D0 = json.load(open(os.path.join(scan, "att_idle0.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    S = json.load(open(os.path.join(scan, "sample_goc.json"), encoding="utf-8"))
    return D0, I, S


def bo_xuong(I):
    ten = [b["name"] for b in I["bones"]]
    bo = set()
    for b in I["bones"]:
        nm = b["name"]
        if nm == "root":
            continue
        if nm.startswith(BO_TIEN_TO) or nm == "weiba" or (b["parent"] >= 0 and ten[b["parent"]] in bo):
            bo.add(nm)
    return bo


def rieng(I, F):
    """biến đổi riêng (x, y, góc, sx, sy) mọi xương ở một khung mẫu, theo kế thừa THƯỜNG."""
    L = np.array(F["l"], float)[:, :5].copy()
    M = np.array(F["m"], float)
    gw = np.degrees(np.arctan2(M[:, 2], M[:, 0]))
    for i, b in enumerate(I["bones"]):
        if b["inherit"] == 2 and b["parent"] >= 0:
            L[i, 2] = gw[i] - gw[b["parent"]]
    return L


def chuyen_dong(I, S, goc0):
    ten = [b["name"] for b in I["bones"]]
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        L = np.array([rieng(I, F) for F in fr], float)
        res = {}
        for i, n in enumerate(ten):
            if n not in goc0:
                continue
            g = goc0[n]
            A = np.stack([L[:, i, 2] - g[2], L[:, i, 0] - g[0], L[:, i, 1] - g[1], L[:, i, 3] / (g[3] or 1.0), L[:, i, 4] / (g[4] or 1.0)], 1)
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            A[:, 0] -= 360.0 * round(A[0, 0] / 360.0)
            if np.abs(A - np.array([0, 0, 0, 1, 1])).max() > 1e-4:
                res[n] = A
        out[clip] = (float(v["dur"]), res, len(fr))
    return out


# ---------------------------------------------------------------- dựng
def anh_manh(ten):
    QR.G, QR.MANH, QR.D_PX = G, MANH, D_PX
    return QR.anh_manh(ten)


def anh_manh_moi(ten):
    """dạng non: mảnh mới (inbox/tinh_hach_non/manh, hộp px concept A), thu về D_PX pixel mỗi đơn vị rig."""
    DATJ = json.load(open(os.path.join(THN.MANH, "dat.json")))
    s_px, _, _ = THN.tf()
    g = Image.open(os.path.join(THN.MANH, ten + ".png")).convert("RGBA")
    kq = D_PX / s_px
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g), DATJ[ten]["hop"], kq


def att_co(a, ten, Wi, W0):
    """dạng non: lưới (gộp) của họ ở khung 0 idle → cùng lưới trên bộ xương đã nhân tỉ lệ (mỗi đỉnh da hoá lại bằng W0 mới)."""
    Q = np.array(a["xy"], float).reshape(-1, 2)
    out = []
    for v, ws in zip(Q, a["w"]):
        acc, tot = np.zeros(2), 0.0
        for k, w in ws:
            n = ten[k]
            if n in W0 and n in Wi and w > 0:
                acc += w * (W0[n] @ np.linalg.solve(Wi[n], np.array([v[0], v[1], 1.0])))[:2]
                tot += w
        out.append(acc / tot if tot > 0 else v)
    return dict(a, xy=np.asarray(out).ravel().tolist())


def luoi_manh(sk, ten_m):
    if la_moi(ten_m):
        im, (x0, y0, x1, y1), kq = anh_manh_moi(ten_m)
        to_rig = THN.tf()[1]
    else:
        im, (x0, y0, x1, y1), kq = anh_manh(ten_m)
        _, to_rig, _ = QR.tf()
    if ten_m not in sk.images:
        sk.anh(ten_m, im)
    im = sk.images[ten_m]
    bv = max(6.0, min(12.0, 0.06 * min(im.width, im.height)))
    L = luoi.luoi_vung(im, buoc_vien=bv, buoc_trong=bv * 1.5, vien=2, ten=ten_m, in_tk=False)
    V = to_rig(np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1))
    return L, V


def gan_tu_do(sk, ten_m, Wd):
    """mảnh tự do (không theo lưới gốc): trọng số Wd (list dict) cho từng đỉnh, điểm gắn = nghịch ma trận dáng gốc (= khung 0 idle)."""
    L, V = luoi_manh(sk, ten_m)
    W = Wd(V) if callable(Wd) else Wd
    sk.luoi_gan(ten_m, ten_m, L, W, the_gioi=V)
    return L, V


def gan_moi(sk, ten_m, a0, ten, Wi):
    """dạng non: mảnh mới gắn trên nhóm lưới của họ ĐÃ CO (att_co), điểm gắn theo W0 đã nhân tỉ lệ (như QR.gan_manh)."""
    L, V = luoi_manh(sk, ten_m)
    Wi_s = dict(Wi)
    Wi_s.update(sk.W0)
    rows = QR.trong_so_goc(V, att_co(a0, ten, Wi, sk.W0), ten, Wi_s)
    vong = MUOT.get(ten_m, 0)
    if vong:
        sk.luoi_gan(ten_m, ten_m, L, QR.lam_tron_ts(L, rows, vong), the_gioi=V)
    else:
        sk.luoi_gan(ten_m, ten_m, L, trongso.cung(L.n, "move"), the_gioi=V)
        sk.atts[ten_m][ten_m]["verts"] = rows
    return L


def att_luoi(a, ten):
    """hình region của họ (4 góc, một xương) hay lưới không trọng số → dạng lưới (xy, tris, w) để gop_att / trong_so_goc dùng chung."""
    n = len(a.get("xy", [])) // 2
    if "tris" in a and "w" in a:
        return a
    tris = a.get("tris", [0, 1, 2, 2, 3, 0])
    return dict(a, tris=tris, w=[[[ten.index(a["bone"]), 1.0]]] * n)


def dung():
    D0, I, S = nap()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    bo = bo_xuong(I)
    L0 = rieng(I, S["idle_01"]["frames"][0])
    Wi = QR.mats(D0)
    by0 = {a["slot"]: att_luoi(a, ten) for a in D0["atts"] if a.get("cur")}
    sk = khung.Sk(TEN_RIG)
    sk.xuong("root")
    sk.xuong("move", "root")
    goc0 = {}
    for i, b in enumerate(IB):
        nm = b["name"]
        if nm == "root" or nm in bo:
            continue
        cha = ten[b["parent"]]
        g = [float(v) for v in L0[i]]
        goc0[nm] = g
        sk.xuong(nm, "move" if cha == "root" else cha, g[0], g[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
    # kiểm: ma trận dáng gốc của mình = khung 0 idle của họ
    lech = max(float(np.hypot(*(sk.W0[n][:2, 2] - Wi[n][:2, 2]))) for n in goc0)
    print(f"lệch vị trí xương so với khung 0 idle: {lech:.2f} đv")
    if NON:
        ap_ti(sk, True)                                                  # từ đây W0 = dáng gốc dạng 1
        print("dạng non: tỉ lệ", {k: v for k, v in TI_NON.items() if k in sk.bi})
    sk.xuong("mieng", "move", 0.0, 0.0)
    sk.info.update(by0=by0, ten=ten, Wi=Wi)
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    _, to_rig, _ = QR.tf()

    def hop_rig(tm):
        x0, y0, x1, y1 = DATJ[tm]["hop"]
        return to_rig(np.array([[x0, y0], [x1, y1]], float))

    if NON:
        DATN = json.load(open(os.path.join(THN.MANH, "dat.json")))
        _, to_rig_n, _ = THN.tf()
        hb = json.load(open(os.path.join(THN.MAU, "bo_cuc_khung.json"), encoding="utf-8"))
        b_rig = THN.A.canvas_map(tuple(hb["khung_rig"]), THN.W, THN.H, pad=THN.PAD)[0]

        def hop_n(tm):
            x0, y0, x1, y1 = DATN[tm]["hop"]
            return to_rig_n(np.array([[x0, y0], [x1, y1]], float))

        def hop_bc(s):                                                   # hộp slot trên bố cục (da dạng 2 đã co) → rig dạng 1
            x0, y0, x1, y1 = hb["slot"][s]
            return b_rig(np.array([[x0, y0], [x1, y1]], float))

    tong = [0, 0]
    # --- 5 thiên thạch (cụm tinh thể) bay kiểu NGUYÊN TỬ: mỗi cái một quỹ đạo elip nghiêng riêng quanh thân. Elip dựng bằng hai xương quay
    # ngược chiều (vòng a quay +u, vòng b quay −u → elip bán trục a + b, a − b, nghiêng α): aura cộng góc vào hai xương (+Δ, −2Δ) nên cast /
    # skill cộng THÊM tốc độ quay mà không cần biết thiên thạch đang ở đâu trên quỹ đạo. Mỗi thiên thạch: xương quy_j (con all2, tâm quỹ
    # đạo) → quy2_j (đầu vòng a) → dao_j (đầu vòng b, mang hình); hai bóng mờ vệt bay (cùng chuỗi, góc trễ); slot sau lưng + slot trước ngực.
    cums = sorted(k for k in (DATN if NON else DATJ) if k.startswith("cum"))
    hb_t, hb_d = (hop_bc("than"), hop_bc("dau")) if NON else (hop_rig("than"), hop_rig("dau"))
    x0_, x1_ = float(min(hb_t[0, 0], hb_d[0, 0])), float(max(hb_t[1, 0], hb_d[1, 0]))
    y0_, y1_ = float(min(hb_t[0, 1], hb_t[1, 1])), float(max(hb_t[0, 1], hb_t[1, 1]))
    C_Q = np.array([(x0_ + x1_) / 2, (y0_ + y1_) / 2])
    A_Q = 0.5 * (x1_ - x0_) + 0.10 * (y1_ - y0_)
    B_Q = 0.26 * A_Q
    ALPHA = [0.0, 45.0, 158.0, 22.0, 135.0]                            # góc nghiêng từng quỹ đạo (độ)
    V_MAX = 0.65 * float(C_Q[1])                                       # nửa bề cao quỹ đạo: thấp nhất ngang gối, không chui xuống đất
    QUY = []
    for j, c in enumerate(cums):
        al, psi = ALPHA[j % len(ALPHA)], 360.0 * j / len(cums)
        A_, B_ = A_Q * (1.0 - 0.06 * (j % 2)), B_Q
        s2, c2 = math.sin(math.radians(al)) ** 2, math.cos(math.radians(al)) ** 2
        if A_ * A_ * s2 + B_ * B_ * c2 > V_MAX * V_MAX:
            A_ = math.sqrt((V_MAX * V_MAX - B_ * B_ * c2) / s2)
        a_, b_ = (A_ + B_) / 2, (A_ - B_) / 2
        for hau in ("", "_g1", "_g2"):
            sk.xuong(f"quy{hau}_{j}", "all2", float(C_Q[0]), float(C_Q[1]), goc=al + psi, dai=a_, the_gioi=True)
            sk.xuong(f"quy2{hau}_{j}", f"quy{hau}_{j}", a_, 0.0, goc=-2.0 * psi, dai=b_)
            sk.xuong(f"dao{hau}_{j}", f"quy2{hau}_{j}", b_, 0.0, goc=0.0)
        QUY.append(dict(c=c, j=j, al=al, psi=psi, a=a_, b=b_))
        L, V = luoi_manh(sk, c)
        V = V - V.mean(0) + sk.W0[f"dao_{j}"][:2, 2]                    # hình đặt giữa xương mang hình (dáng gốc: đầu quỹ đạo)
        sk.slot(c, "move", c)
        sk.luoi_gan(c, c, L, [{f"dao_{j}": 1.0}] * L.n, the_gioi=V)
        QUY[-1]["L"], QUY[-1]["V"] = L, V
    sk.info["quy"] = QUY
    sk.info["quy_tam"] = (C_Q, A_Q, B_Q)
    print(f"quỹ đạo: tâm {np.round(C_Q)}, bán trục {A_Q:.0f} × {B_Q:.0f}")
    # --- đuôi: chuỗi ba xương riêng (con all3), khớp đọc trên concept (gốc khuất sau thân → chóp quạt tinh thể)
    if NON:                                                              # khớp đọc trên concept A (gốc khuất sau tay gần → chóp lưỡi)
        J = to_rig_n(np.array(DUOI_J_NON))
    else:
        J = to_rig(np.array([[600.0, 738.0], [480.0, 765.0], [390.0, 762.0], [215.0, 735.0]]))
    sk.chuoi("duoi", "all3", J, ten_rieng=list(DUOI))
    sk.info["duoi_J"] = J
    # --- rừng tinh thể: hai xương riêng (con all4 / all5) ở chân rừng; tinh thể vắt vai: xương riêng con all5
    # (dạng non: ba mầm tinh thể + hai nụ; xương ở chân mầm trên sống lưng; tinh thể vắt vai không có, xương tt_nam_g giữ cho clip)
    rr = hop_n("rung") if NON else hop_rig("rung")
    xa, xb = float(rr[0, 0]), float(rr[1, 0])
    yb = float((to_rig_n if NON else to_rig)(np.array([[0.0, Y_CHAN_MAM if NON else 430.0]]))[0, 1])
    sk.xuong("tt_sau", "all4", xa + 0.28 * (xb - xa), yb, goc=90.0, dai=200.0, the_gioi=True)
    sk.xuong("tt_truoc", "all5", xa + 0.72 * (xb - xa), yb, goc=90.0, dai=200.0, the_gioi=True)
    cn = (to_rig_n if NON else to_rig)(np.array([[870.0, 440.0]]))[0]
    sk.xuong("tt_nam_g", "all5", float(cn[0]), float(cn[1]), goc=90.0, dai=150.0, the_gioi=True)
    for ten_m, goc in MANH_GOC:
        if NON and ten_m == "tt_nam":
            continue
        sk.slot(ten_m, "move", ten_m)
        if ten_m == "duoi":
            L, V = luoi_manh(sk, "duoi")
            Wd = trongso.chuoi_chieu(V, J, list(DUOI), cha="all3", cha_hoa=0.35)
            sk.luoi_gan("duoi", "duoi", L, Wd, the_gioi=V)
        elif ten_m == "rung":
            def w_rung(V):
                u = np.clip((V[:, 0] - (xa + 0.2 * (xb - xa))) / (0.6 * (xb - xa)), 0.0, 1.0)
                u = u * u * (3 - 2 * u)
                return [{"tt_sau": float(1 - a), "tt_truoc": float(a)} if 0 < a < 1 else ({"tt_truoc": 1.0} if a >= 1 else {"tt_sau": 1.0})
                        for a in u]
            L, V = gan_tu_do(sk, "rung", w_rung)
        elif ten_m == "tt_nam":
            L, V = gan_tu_do(sk, "tt_nam", lambda V: [{"tt_nam_g": 1.0}] * len(V))
        else:
            QR.MUOT = MUOT
            a0 = QR.gop_att([by0[s] for s in goc])
            if la_moi(ten_m):
                L = gan_moi(sk, ten_m, a0, ten, Wi)
            else:
                with Khung2(sk):
                    L = QR.gan_manh(sk, ten_m, ten_m, a0, ten, Wi)
        tong[0] += L.n
        tong[1] += len(L.tris)
    # --- móng: cứng trên xương ngón nặng nhất ở tâm móng; móng tay xa vẽ ngay sau tay xa, móng tay gần ngay sau tay gần
    # (dạng non: móng dạng 2 dùng lại, gắn ở khung dạng 2)
    for ben, truoc in (("xa", "rung"), ("gan", "dau")):
        a_tay = QR.gop_att([by0[s] for s in NGON_GOC[ben]])
        for tm in sorted(k for k in DATJ if k.startswith(f"ngon_{ben}")):
            with Khung2(sk):
                c = hop_rig(tm).mean(0)
                w0 = QR.trong_so_goc(np.array([c]), a_tay, ten, Wi)[0]
                xb_ = max(w0, key=lambda r: r[3])[0] if w0 else ("xiaobi_r2" if ben == "gan" else "shouzhang_l")
                sk.slot(tm, "move", tm, truoc=truoc)
                gan_tu_do(sk, tm, lambda V, b=xb_: [{b: 1.0}] * len(V))
            print(f"  {tm} → {xb_}")
    # --- quả cầu thiên thạch (chiêu cuối): xương bong (con all2) ở tâm thân, ẩn mặc định
    C_Q, A_Q, B_Q = sk.info["quy_tam"]
    sk.xuong("bong", "all2", float(C_Q[0]), float(C_Q[1] - 0.04 * (B_Q / 0.26)), goc=0.0)
    sk.xuong("bong_q", "bong", 0.0, 0.0)                                 # bong: kéo / bẹp (không xoay); bong_q: quả cầu lăn
    im_b = Image.open(os.path.join(MANH, "bong.png")).convert("RGBA")
    D_BONG = 1.35 * A_Q                                                  # đường kính quả cầu (cả gai) ≈ chiều cao thân
    if NON:
        # dạng non: quả cầu vẽ lại (mặt con non, gai ngắn); thân quả cầu cùng tỉ lệ như dạng 2 (0,9: đường kính / chiều cao như dạng 2) →
        # giữ phép thu của ảnh dạng 2 cho ảnh mới (gai ngắn hơn thì ảnh nhỏ hơn, thân cầu không phình)
        p_n = os.path.join(THN.MANH, "bong.png")
        D_BONG *= 0.9
        if os.path.exists(p_n):
            im_n = Image.open(p_n).convert("RGBA")
            D_BONG *= max(im_n.size) / max(im_b.size)
            im_b = im_n
    kq_b = min(1.0, D_BONG * D_PX / max(im_b.size))
    im_s = im_b.convert("RGBa").resize((max(2, round(im_b.width * kq_b)), max(2, round(im_b.height * kq_b))), Image.LANCZOS).convert("RGBA")
    sk.anh("bong", anh.loang_mau(im_s))
    imb = sk.images["bong"]
    Lb = luoi.luoi_vung(imb, buoc_vien=10.0, buoc_trong=16.0, vien=2, ten="bong", in_tk=False)
    sc_b = D_BONG / max(imb.size)
    Vb = sk.W0["bong_q"][:2, 2] + np.stack([(Lb.pts[:, 0] - imb.width / 2) * sc_b, -(Lb.pts[:, 1] - imb.height / 2) * sc_b], 1)
    sk.slot("bong", "move", "bong", an=True)
    sk.luoi_gan("bong", "bong", Lb, [{"bong_q": 1.0}] * Lb.n, the_gioi=Vb)
    sk.info["D_BONG"] = D_BONG
    # --- thiên thạch: slot trước ngực (aura đổi hình sau / trước ở hai đầu quỹ đạo) + hai bóng mờ vệt bay (ẩn, cast / skill bật)
    for q in sk.info["quy"]:
        c, j = q["c"], q["j"]
        sl = c + "~t"
        sk.slot(sl, "move", None)
        sk.atts[sl][c] = sk.atts[c][c]
        sk.luoi[(sl, c)] = sk.luoi[(c, c)]
        for g in (1, 2):
            sg = f"{c}~g{g}"
            sk.slot(sg, "move", c, an=True)
            sk.luoi_gan(sg, c, q["L"], [{f"dao_g{g}_{j}": 1.0}] * q["L"].n, the_gioi=q["V"])
    for e, m in (("trung", "khung trúng"), ("vo", "attack: móng nện đất (VFX dăm đá, bụi)"), ("xe", "attack: lắc đầu xé (VFX dăm, bụi)"),
                 ("xoa", "cast: hai tay bắt đầu xoa vào nhau (VFX tia lửa đá giữa hai bàn tay)"),
                 ("quay_nhanh", "cast / skill: thiên thạch quay nhanh dần (VFX vệt bay)"),
                 ("tu", "cast: thiên thạch xoáy về một điểm trước mặt"),
                 ("phong", "cast: một thiên thạch lao vào đối thủ (chuỗi theo thứ tự; tham số = số thứ tự)"),
                 ("no", "cast: thiên thạch đâm trúng, nứt tung (VFX)"), ("moc", "cast: thiên thạch mới trở lại quỹ đạo"),
                 ("cuon", "skill: cuộn người thành quả cầu thiên thạch đầy gai"),
                 ("bay_len", "skill: quả cầu bay vọt lên cao (VFX vệt bay, bụi đất)"),
                 ("lua", "skill: quả cầu lao xuống, lửa xé gió bùng quanh (VFX lửa đuôi sao chổi)"),
                 ("no_lon", "skill: quả cầu nện trúng đối thủ, NỔ RẤT LỚN (VFX nổ, sóng xung kích, rung màn hình)"),
                 ("bung", "skill: bung người ra giữa không trung"), ("cham_dat", "appear / skill: chạm đất"),
                 ("nen", "appear: nện đất (VFX vết nứt, bụi, rung)"), ("gam", "appear: gầm"),
                 ("tro_lai", "appear: thiên thạch nở ra quỹ đạo")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác")
    return sk, dict(I=I, ten=ten, goc0=goc0, S=S, Wi=Wi)


# ---------------------------------------------------------------- clip
# lượt 3 (người dùng xem lượt 2: "chiêu mana vẫn dùng 2 tay xoa nhau, các thiên thạch xung quanh bay nhanh hơn rồi lao vào người đối thủ";
# "làm các thiên thạch bay xung quanh kiểu atom"; "chiêu cuối tướng cuộn người lại thành 1 quả bóng thiên thạch đầy gai, các thiên thạch xung
# quanh quay cực nhanh để lại trail rồi bay lên cao, lao xuống người đối thủ như 1 viên thiên thạch, có hiệu ứng xé gió tạo lửa rồi nổ rất lớn")
D_ATK = 1.15
T_ATK = 0.46                         # attack: vồ lao trúng (cú lao trên xương move, game kéo tới đối thủ)
D_CAST = 2.40
T_XOA0, T_XOA1 = 0.30, 1.05          # cast: hai tay xoa vào nhau trước ngực (dáng skill_04 của họ)
T_QUAY0, T_QUAY1 = 0.25, 2.05        # thiên thạch quay nhanh dần (cộng thêm N_QUAY_C vòng)
N_QUAY_C = 3
T_TU0, T_TU1 = 0.80, 1.05            # thiên thạch xoáy về một điểm trước mặt
T_PHONG = [1.05, 1.13, 1.21, 1.29, 1.37]
BAY = 0.22
T_MOC_C = 1.85                       # thiên thạch trở lại quỹ đạo
D_SKILL = 3.30
T_CUON0, T_CUON1 = 0.05, 0.36        # cuộn người → quả cầu
T_QS0, T_QS1 = 0.30, 2.75            # thiên thạch quay cực nhanh (cộng thêm N_QUAY_S vòng)
N_QUAY_S = 7
T_LEN0, T_LEN1 = 1.00, 1.36          # bay vọt lên cao
T_NO = 1.70                          # lao xuống nện ngay đối thủ: NỔ LỚN
T_NAY1 = 2.05                        # nảy ngược về phía nhà
T_BUNG0, T_BUNG1 = 2.02, 2.22        # bung người ra giữa không trung
T_VE = 2.50                          # đáp về chỗ cũ
D_APPEAR = 2.50
T_DAP = 0.42
T_TRO = [0.62, 0.70, 0.78, 0.86, 0.94]
T_GAM0, T_GAM1 = 1.15, 1.75
D_AURA = 8.0                          # thiên thạch bay quỹ đạo nguyên tử (clip lặp chồng lên mọi clip)
TRE_G = (0.025, 0.05)                 # độ trễ hai bóng mờ vệt bay (giây)
THAN_SLOT = ("duoi", "tay_xa", "rung", "than", "tt_nam", "long_mieng", "ham", "tay_gan", "dau")
# chiều HÁ của xương hàm all10. Đo 2026-11-18 (cả dạng 2): góc DƯƠNG làm hàm xoay lên chui vào trong đầu (attack 0,40: hộp hàm chồng hộp
# đầu 240 đv, hàm khuất sau đầu) = KHÉP; ghi chú cũ "dương = há" sai, mọi pha "há to / gầm" đang khép miệng còn cú đớp thì hé ra.
HA = -1.0


def lam_clip(sk, info, cao=1300.0):
    CD = chuyen_dong(info["I"], info["S"], info["goc0"])
    QUY = sk.info["quy"]
    C_Q, A_Q, B_Q = sk.info["quy_tam"]
    A2 = sk.W0["all2"][:2, :2]
    cv = hoat.cv

    def dat(P, goc, tau, lap=False, chi=None, bo=None, k=1.0):
        dur, R, n = CD[goc]
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * FPS
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        for b, A in R.items():
            if (chi is not None and b not in chi) or (bo is not None and b in bo):
                continue
            v = A[i0] * (1 - w) + A[i1] * w
            for q in (3, 4):
                if A[i0][q] * A[i1][q] < 0:
                    v[q] = A[i0][q] if w < 0.5 else A[i1][q]
            if abs(v[0]) > 1e-4:
                P.rot(b, k * float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, k * float(v[1]), k * float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, 1 + k * (float(v[3]) - 1), 1 + k * (float(v[4]) - 1))

    def pha(Pa, Pb, w, chi=None):
        Q = Pa.copy()
        for b in (set(Pa.t) | set(Pb.t)) if chi is None else chi:
            a_ = Pa.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            b_ = Pb.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            dr = (b_[2] - a_[2] + 180.0) % 360.0 - 180.0
            Q.t[b] = [a_[0] + (b_[0] - a_[0]) * w, a_[1] + (b_[1] - a_[1]) * w, a_[2] + dr * w,
                      a_[3] + (b_[3] - a_[3]) * w, a_[4] + (b_[4] - a_[4]) * w]
        for s, v in Pb.alpha.items():
            Q.alpha[s] = Pa.alpha.get(s, 1.0) * (1 - w) + v * w
        return Q

    def chep(P, Q):
        P.t.clear()
        P.t.update({k: list(v) for k, v in Q.t.items()})
        P.alpha.update(Q.alpha)
        P.att.update(Q.att)

    def song(t, tre, chu=2.0):
        return math.sin(2 * math.pi * (t - tre) / chu)

    def em(u):
        u = min(1.0, max(0.0, u))
        return u * u * u * (u * (6 * u - 15) + 10)

    BO_QIU = set(CUM_QIU)

    def len_troi(b, d):
        cha = sk.bones[sk.bi[b]]["parent"]
        return np.linalg.solve(sk.W0[cha][:2, :2], np.array([0.0, d]))

    def duoi(P, t, k=1.0, lech=0.0):
        for j, b in enumerate(DUOI):
            P.rot(b, k * (3.0 + 3.0 * j) * song(t, 0.18 * j + lech, 2.0))

    def nen_idle(P):
        dat(P, "idle_01", 0.0, bo=BO_QIU)

    def rung_tt(P, k):
        P.rot("tt_sau", 6.0 * k)
        P.rot("tt_truoc", -6.0 * k)
        P.rot("tt_nam_g", 8.0 * k)

    # ---- thiên thạch: các phép CỘNG lên chuỗi quỹ đạo (đúng với mọi pha aura)
    def chuoi(j, g):
        h = "" if g == 0 else f"_g{g}"
        return f"quy{h}_{j}", f"quy2{h}_{j}", f"dao{h}_{j}"

    def quay_them(P, j, g, deg):
        """quay thêm deg độ trên quỹ đạo elip của thiên thạch j (g = 0: chính, 1/2: bóng mờ)."""
        q1, q2, d = chuoi(j, g)
        P.rot(q1, deg)
        P.rot(q2, -2.0 * deg)
        P.rot(d, deg)

    def co_quy(P, j, g, s, dich=None):
        """co quỹ đạo về tâm (s = 1: thiên thạch nằm ĐÚNG tâm) và dời tâm tới dich (thế giới) theo s; s < 0: nới quỹ đạo ra."""
        q1, q2, d = chuoi(j, g)
        q = QUY[j]
        P.move(q2, -q["a"] * s, 0.0)
        P.move(d, -q["b"] * s, 0.0)
        if dich is not None:
            dd = np.linalg.solve(A2, (np.asarray(dich) - C_Q) * s)            # thế giới → hệ của all2 (cha của quy)
            P.move(q1, float(dd[0]), float(dd[1]))

    def an_dao(P, a, chi_bong=None):
        for q in QUY:
            P.alpha[q["c"]] = a
            P.alpha[q["c"] + "~t"] = a

    def bong_mo(P, a):
        for q in QUY:
            for g, k in ((1, 0.55), (2, 0.3)):
                P.alpha[f"{q['c']}~g{g}"] = a * k

    def quay_nhanh(P, t, t0, t1, n_vong, ac=0.6):
        """mọi thiên thạch (và bóng mờ, trễ TRE_G) quay thêm n_vong vòng từ t0 → t1: tăng tốc rồi giảm tốc, khép đúng bội 360° (về idle
        không quay ngược)."""
        for q in QUY:
            for g in (0, 1, 2):
                tt = t - (0.0 if g == 0 else TRE_G[g - 1])
                u = min(1.0, max(0.0, (tt - t0) / (t1 - t0)))
                f = em(u)
                quay_them(P, q["j"], g, 360.0 * n_vong * f)

    # ------------------------------------------------ aura: quỹ đạo nguyên tử (mỗi thiên thạch một elip nghiêng; đổi lớp sau / trước ở hai
    # đầu trục lớn, nơi nó không chồng lên thân); xa nhỏ gần to, nhấp nhô, tự xoay; bóng mờ đi trễ TRE_G
    def f_aura(t, P):
        for q in QUY:
            j, c = q["j"], q["c"]
            for g in (0, 1, 2):
                tt = t - (0.0 if g == 0 else TRE_G[g - 1])
                dth = 360.0 * tt / D_AURA
                quay_them(P, j, g, dth)
                u = math.radians(dth + q["psi"])
                s = math.sin(u)
                k = 1.0 - 0.14 * s
                q1, q2, d = chuoi(j, g)
                P.scale(d, k, k)
                P.rot(d, 12.0 * math.sin(2 * math.pi * 2 * tt / D_AURA + j))
                if g == 0:
                    truoc = s < 0
                    P.att[c] = None if truoc else c
                    P.att[c + "~t"] = c if truoc else None

    # ------------------------------------------------ idle, walk, hit, die
    D_IDLE = 4.0
    L0, L1, LV = 2.05, 3.25, 0.30

    def f_idle(t, P):
        nen_idle(P)
        b = song(t, 0.0)
        P.scale("all3", 1 + 0.008 * b, 1 + 0.014 * b)
        P.move("all3", 0.0, 6.0 * b)
        P.rot("all4", 0.8 * song(t, 0.06))
        P.rot("all5", 1.0 * song(t, 0.10))
        P.rot("all6", 1.6 * song(t, 0.16))
        P.rot("all10", HA * (2.0 + 2.0 * song(t, 0.30, 2.0)))
        for j, bn in enumerate(TAY_GAN):
            P.rot(bn, (1.2 + 0.6 * j) * song(t, 0.20 + 0.08 * j))
        for j, bn in enumerate(TAY_XA):
            P.rot(bn, -(1.0 + 0.6 * j) * song(t, 0.45 + 0.08 * j))
        P.rot("tt_sau", 1.2 * song(t, 0.25, 4.0))
        P.rot("tt_truoc", -1.0 * song(t, 0.55, 4.0))
        P.rot("tt_nam_g", 1.5 * song(t, 0.35, 2.0))
        duoi(P, t)
        if L0 < t < L1:
            e = em((t - L0) / LV) * em((L1 - t) / LV)
            lac = math.sin(2 * math.pi * (t - L0) / 0.30) * e
            P.rot("all6", 9.0 * lac)
            P.rot("all5", -3.5 * lac)
            P.rot("all10", HA * 6.0 * e)
            P.rot("tt_sau", 4.0 * math.sin(2 * math.pi * (t - L0) / 0.11) * e)
            P.rot("tt_truoc", -4.5 * math.sin(2 * math.pi * (t - L0 - 0.03) / 0.12) * e)
            P.rot("tt_nam_g", 5.0 * math.sin(2 * math.pi * (t - L0 - 0.05) / 0.10) * e)
            P.scale("tt_sau", 1.0, 1 + 0.04 * e)
            P.scale("tt_truoc", 1.0, 1 + 0.05 * e)

    def f_walk(t, P):
        d = CD["run_01"][0]
        dat(P, "run_01", t, True, bo=BO_QIU)
        duoi(P, 2.0 * t / d, 1.3)

    def f_hit(t, P):
        dat(P, "hit_01", t, bo=BO_QIU)
        k = math.exp(-((t - 0.08) / 0.12) ** 2)
        for j, b in enumerate(DUOI):
            P.rot(b, 10.0 * (1 + j) * k)
        P.rot("tt_sau", 5.0 * k)
        P.rot("tt_truoc", -5.0 * k)

    def f_die(t, P):
        d = CD["die_01"][0]
        dat(P, "die_01", min(d, t + 1.0 / FPS), bo=BO_QIU)
        if t < 0.12:
            Q = khung.Pose()
            nen_idle(Q)
            chep(P, pha(Q, P, ease(t / 0.12, "io")))
        duoi(P, t, max(0.0, 1.0 - t / d))
        Wd = sk.the_gioi(P)
        for q in QUY:                                                   # thiên thạch mất lực, rơi thẳng xuống, vỡ tan
            j = q["j"]
            u = ease(min(1.0, max(0.0, (t - 0.12 - 0.05 * j) / 0.40)), "in")
            dd = np.linalg.solve(Wd["all2"][:2, :2], np.array([0.0, -0.45 * cao * u]))
            P.move(f"quy_{j}", float(dd[0]), float(dd[1]))
            a_ = 1.0 - ease(min(1.0, max(0.0, (t - 0.40 - 0.05 * j) / 0.20)))
            P.alpha[q["c"]] = a_
            P.alpha[q["c"] + "~t"] = a_
        a = float(np.clip(1.0 - (t - d) / (TAN - 0.1), 0.0, 1.0))
        if a < 0.999:
            for sl in sk.slots:
                if not sl["name"].startswith("bay_") and "~g" not in sl["name"] and sl["name"] != "bong":
                    P.alpha[sl["name"]] = a

    # ------------------------------------------------ attack: VỒ LAO + ĐỚP XÉ
    LAO = 0.55

    def f_attack(t, P):
        nen_idle(P)
        lao = cv(t, [(0.0, 0.0), (0.28, -0.08, "io"), (T_ATK, LAO, "in"), (0.70, LAO), (0.95, 0.0, "io"), (D_ATK, 0.0)])
        bay = cv(t, [(0.0, 0.0), (0.28, 0.0), (0.37, 0.12, "out"), (T_ATK, 0.0, "in"), (0.70, 0.0), (0.82, 0.07, "out"),
                     (0.95, 0.0, "in"), (D_ATK, 0.0)])
        P.move("move", cao * lao, cao * bay)
        thu = cv(t, [(0.0, 0.0), (0.28, 1.0, "io"), (0.40, -0.6, "out"), (T_ATK, 0.4, "in"), (0.58, 0.2), (0.95, 0.0, "io")])
        P.move("all3", 0.0, -0.05 * cao * max(thu, 0.0))
        P.scale("all3", 1 - 0.04 * thu, 1 + 0.03 * thu)
        P.rot("all4", -5.0 * thu)
        dau = cv(t, [(0.0, 0.0), (0.28, -0.7, "io"), (0.40, 0.6, "out"), (T_ATK, -0.5, "in"), (0.70, -0.3), (D_ATK, 0.0, "io")])
        P.rot("all5", 5.0 * dau)
        P.rot("all6", 12.0 * dau)
        ha = cv(t, [(0.0, 0.0), (0.28, 0.2), (0.40, 1.0, "out"), (T_ATK - 0.02, 1.0), (T_ATK + 0.02, -0.25, "in"), (0.70, -0.2),
                    (D_ATK, 0.0, "io")])
        P.rot("all10", HA * (2.0 + 17.0 * ha))
        if T_ATK < t < 0.72:
            e = math.sin(math.pi * (t - T_ATK) / (0.72 - T_ATK))
            x = math.sin(2 * math.pi * (t - T_ATK) / 0.13) * e
            P.rot("all6", 11.0 * x)
            P.rot("all5", -4.0 * x)
            P.rot("all4", 2.0 * x)
        vo = cv(t, [(0.0, 0.0), (0.28, 0.6, "io"), (0.40, 0.2), (T_ATK, -1.0, "in"), (0.70, -0.8), (D_ATK, 0.0, "io")])
        P.rot("dabi_l", (14.0 if vo > 0 else 30.0) * vo)
        P.rot("xiaobi_l", (8.0 if vo > 0 else 24.0) * vo)
        P.rot("shouzhang_l", 14.0 * vo)
        P.rot("dabi_r", -8.0 * thu)
        P.rot("xiaobi_r", 6.0 * thu)
        quat = cv(t, [(0.0, 0.0), (0.28, -0.5, "io"), (0.42, 1.0, "out"), (0.62, -0.6, "io"), (D_ATK, 0.0, "io")])
        for j, b in enumerate(DUOI):
            P.rot(b, (8.0 + 6.0 * j) * quat)
        duoi(P, t, 0.6)
        k = math.exp(-((t - (T_ATK + 0.02)) / 0.05) ** 2)
        P.scale("all3", 1 + 0.07 * k, 1 - 0.09 * k)
        rung_tt(P, 1.2 * k - 0.4 * thu)

    # ------------------------------------------------ cast: HAI TAY XOA VÀO NHAU trước ngực; thiên thạch quay nhanh dần, xoáy về một điểm
    # trước mặt rồi lần lượt lao vào đối thủ (bản sao trên far / fly_j); thiên thạch thật trở lại quỹ đạo
    far = sk.W0["far"][:2, 2] if "far" in sk.bi else np.array([0.9 * cao + 140.0, 0.45 * cao])
    T_SK4 = (1.00, 2.20)                     # đoạn hai tay xoa trong skill_04 của họ (tay gần cuộn qua ngực, hai bàn tay vờn quanh nhau hai vòng; đầu, cuối tay xa gần chỗ idle)

    def tau_xoa(t):
        if t < T_XOA0:                                                  # đoạn mở đầu của họ (tay xa buông xuống đất) bỏ: hoà thẳng từ idle
            return T_SK4[0]
        return T_SK4[0] + (T_SK4[1] - T_SK4[0]) * min(1.0, (t - T_XOA0) / (T_XOA1 - T_XOA0))

    def than_cast(t, P):
        nen_idle(P)
        w = em(t / T_XOA0) * (1 - em((t - T_XOA1) / 0.32))             # hoà dáng xoa tay của họ, nhả ra khi phóng
        if w > 1e-4:
            Q = khung.Pose()
            dat(Q, "skill_04", tau_xoa(t), bo=BO_QIU)
            chep(P, pha(P, Q, w))
        e = em((t - T_XOA0) / 0.12) * (1 - em((t - (T_XOA1 - 0.08)) / 0.12))
        if e > 1e-4:                                                    # xoa gấp hơn: cẳng, bàn hai tay miết ngược chiều nhau
            ph = 2 * math.pi * 3.0 * (t - T_XOA0)
            P.rot("xiaobi_r", 5.0 * e * math.sin(ph))
            P.rot("xiaobi_r2", 9.0 * e * math.sin(ph + 0.6))
            P.rot("xiaobi_l", -5.0 * e * math.sin(ph))
            P.rot("shouzhang_l", -9.0 * e * math.sin(ph + 0.6))
            r = hoat.rung(t, T_XOA0, T_XOA1, 2)
            P.rot("all4", 0.6 * r)
            P.rot("tt_sau", 2.0 * r)
            P.rot("tt_truoc", -2.0 * r)
        gam = em((t - (T_XOA1 - 0.10)) / 0.15) * (1 - em((t - 1.85) / 0.40))   # ngóc lên gầm khi phóng
        P.rot("all5", 5.0 * gam)
        P.rot("all6", 12.0 * gam)
        P.rot("all10", HA * 15.0 * gam)
        for tk in T_PHONG:                                              # mỗi thiên thạch phóng đi: hất người tới
            k = math.exp(-((t - tk - 0.03) / 0.045) ** 2)
            P.rot("all4", -2.5 * k)
            P.rot("all6", -3.0 * k)
        duoi(P, t, 1.2)

    Qf = khung.Pose()
    than_cast(T_XOA1 - 0.05, Qf)
    Wf = sk.the_gioi(Qf)
    TAY_F = 0.5 * ((Wf["xiaobi_r2"] @ np.array([120.0, 0.0, 1.0]))[:2] + (Wf["shouzhang_l"] @ np.array([90.0, 0.0, 1.0]))[:2])
    F_TU = TAY_F + np.array([0.20 * cao, 0.04 * cao])                  # thiên thạch xoáy về một điểm ngay trước đôi tay đang xoa

    def cho_phong(t, j):
        """chỗ thiên thạch j (bản sao) trước khi phóng: xoáy vòng nhỏ quanh điểm F_TU."""
        ps = 2 * math.pi * (j / len(QUY) + 3.0 * (t - T_TU1))
        r = 0.06 * cao
        return F_TU + np.array([r * math.cos(ps), 0.6 * r * math.sin(ps)])

    def f_cast(t, P):
        than_cast(t, P)
        quay_nhanh(P, t, T_QUAY0, T_QUAY1, N_QUAY_C)
        bong_mo(P, em((t - 0.40) / 0.25) * (1 - em((t - T_TU1 + 0.05) / 0.1)))
        for q in QUY:
            j = q["j"]
            s_tu = em((t - T_TU0) / (T_TU1 - T_TU0)) * (1 - em((t - T_MOC_C) / 0.35))   # xoáy về F_TU rồi nở lại quỹ đạo
            for g in (0, 1, 2):
                co_quy(P, j, g, s_tu, F_TU)
        if T_TU1 <= t < T_MOC_C:                                       # thiên thạch thật tắt khi đã xoáy về một điểm
            an_dao(P, 0.0)
        elif t >= T_MOC_C:
            u = ease((t - T_MOC_C) / 0.30, "out")
            for q in QUY:
                s_ = max(0.02, u * (1 + 0.15 * math.sin(math.pi * u)))
                P.scale(f"dao_{q['j']}", s_, s_)
        for q in QUY:
            j = q["j"]
            fb, bb = f"fly_{j}", f"bay_{j}"
            if fb not in sk.bi:
                continue
            A = sk.W0[fb][:2, 2]
            t0 = T_PHONG[j]
            sgn = 1 if j % 2 else -1
            if t < T_TU1:
                P.alpha[bb] = 0.0
                pos = cho_phong(T_TU1, j)
            elif t < t0:
                pos = cho_phong(t, j)
                P.alpha[bb] = 1.0
                P.rot(bb, 300.0 * (t - T_TU1) * sgn)
            elif t < t0 + BAY:
                S0 = cho_phong(t0, j)
                v = far - S0
                n = np.array([-v[1], v[0]]) / (float(np.hypot(*v)) or 1.0)
                f = ease((t - t0) / BAY, "in")
                pos = S0 + f * v + n * 0.05 * cao * math.sin(math.pi * f) * sgn
                P.alpha[bb] = 1.0
                P.rot(bb, 300.0 * (t0 - T_TU1) * sgn - 420.0 * f * sgn)
            else:
                pos = far
                P.alpha[bb] = 0.0
                P.rot(bb, 300.0 * (t0 - T_TU1) * sgn - 420.0 * sgn)
            P.move(fb, float(pos[0] - A[0]), float(pos[1] - A[1]))

    # ------------------------------------------------ skill: QUẢ CẦU THIÊN THẠCH: cuộn người thành quả cầu đầy gai, thiên thạch quay cực nhanh
    # để vệt, bay vọt lên cao, lao xuống người đối thủ (lửa xé gió, NỔ LỚN: VFX), nảy về, bung người, đáp
    LAO_SK = 0.62

    def f_skill(t, P):
        nen_idle(P)
        x = cv(t, [(0.0, 0.0), (T_LEN0, 0.0), (T_LEN1, -0.08, "out"), (T_NO, LAO_SK, "in"), (T_NO + 0.04, LAO_SK),
                   (T_NAY1, 0.30, "out"), (T_VE, 0.0, "io"), (D_SKILL, 0.0)])
        y = cv(t, [(0.0, 0.0), (T_CUON1, 0.0), (0.70, 0.06, "io"), (T_LEN0, 0.0, "io"), (T_LEN1, 1.35, "out"), (T_NO, 0.0, "in"),
                   (T_NO + 0.04, 0.0), (T_NAY1, 0.55, "out"), (T_VE, 0.0, "in"), (D_SKILL, 0.0)])
        # move chỉ mang cú lao NGANG (xa nhất đúng lúc nện): game xoay, giãn cả quỹ đạo của move cho điểm xa nhất trỏ vào 72 % quãng tới đối
        # thủ (AolaSticker.Lunge); độ cao bay đặt trên xương con `all` (bóng dưới chân của game vẫn nằm trên đất)
        P.move("move", cao * x, 0.0)
        P.move("all", 0.0, cao * y)
        # cuộn người: thân rụt, đầu tuck, tay co → đổi sang quả cầu (thân ẩn) → bung ra lại
        cuon = cv(t, [(0.0, 0.0), (T_CUON1, 1.0, "in"), (T_BUNG0, 1.0), (T_BUNG1, 0.0, "out"), (D_SKILL, 0.0)])
        P.scale("all3", 1 - 0.25 * cuon, 1 - 0.25 * cuon)
        P.rot("all3", -25.0 * cuon)
        P.rot("all6", -20.0 * cuon)
        P.rot("all5", -10.0 * cuon)
        P.rot("dabi_l", 25.0 * cuon)
        P.rot("xiaobi_l", 30.0 * cuon)
        P.rot("dabi_r", 18.0 * cuon)
        for j, b in enumerate(DUOI):
            P.rot(b, 22.0 * cuon)
        hien_bong = T_CUON1 - 0.04 <= t < T_BUNG1 - 0.06
        for sl in tuple(s for s in THAN_SLOT if s in sk.si) + tuple(s for s in sk.si if s.startswith("ngon_")):
            P.alpha[sl] = 0.0 if hien_bong else 1.0
        P.alpha["bong"] = 1.0 if hien_bong else 0.0
        if hien_bong:
            u_hien = (t - (T_CUON1 - 0.04)) / 0.12
            pop = 0.85 + 0.25 * math.sin(math.pi * min(1.0, u_hien)) if u_hien < 1 else 1.0
            quay = cv(t, [(T_CUON1, 0.0), (T_LEN0, -540.0, "in"), (T_NO, -1980.0, "lin"), (T_BUNG1, -2520.0, "out")])
            P.rot("bong_q", quay)
            # kéo dài theo hướng lao xuống, bẹp dí khi nện (trên xương bong không xoay; bong_q lăn bên trong)
            ep = cv(t, [(0.0, 0.0), (T_LEN1, 0.0), (T_NO - 0.03, 0.20, "in"), (T_NO + 0.03, -0.32, "out"), (T_NO + 0.12, 0.08, "io"),
                        (T_NO + 0.24, 0.0, "io")])
            nghieng = cv(t, [(0.0, 0.0), (T_LEN1, 0.0), (T_LEN1 + 0.10, 27.0, "io"), (T_NO - 0.01, 27.0), (T_NO + 0.03, 0.0, "out")])
            P.rot("bong", nghieng)
            P.scale("bong", pop * (1 - 0.6 * ep), pop * (1 + ep))
        # thiên thạch: quay cực nhanh để vệt, nở tung ra khi nổ rồi về quỹ đạo
        quay_nhanh(P, t, T_QS0, T_QS1, N_QUAY_S)
        bong_mo(P, em((t - 0.40) / 0.20) * (1 - em((t - 2.20) / 0.30)))
        no = cv(t, [(0.0, 0.0), (T_CUON1, 0.25, "io"), (T_NO - 0.02, 0.25), (T_NO + 0.10, -0.9, "out"), (T_NO + 0.40, 0.0, "io")])
        for q in QUY:
            for g in (0, 1, 2):
                co_quy(P, q["j"], g, no)                                 # quấn sát quả cầu, nổ tung ra
        # bung người: gầm khi đáp
        gam = em((t - T_BUNG1) / 0.15) * (1 - em((t - (D_SKILL - 0.45)) / 0.35))
        P.rot("all6", 14.0 * gam)
        P.rot("all10", HA * 15.0 * gam)
        if t > T_VE:
            b = math.exp(-(t - T_VE) / 0.09) * math.cos((t - T_VE) * 2 * math.pi / 0.22)
            P.scale("all3", 1 + 0.08 * b, 1 - 0.10 * b)
            u = ease((t - T_VE) / 0.30, "out")
            for b_ in ("tt_sau", "tt_truoc", "tt_nam_g"):
                P.scale(b_, 1.0, max(0.05, 0.6 + 0.4 * u + 0.12 * math.sin(math.pi * u)))
        duoi(P, t, 1.0 - cuon)

    # ------------------------------------------------ appear: rơi như thiên thạch, nện, thiên thạch nở ra quỹ đạo, rừng dựng, gầm
    def f_appear(t, P):
        nen_idle(P)
        if t < T_DAP:
            u = t / T_DAP
            P.move("move", -0.25 * cao * (1 - u), 1.25 * cao * (1 - u * u))
            P.rot("all3", -10.0 * (1 - u))
            for sl in sk.slots:
                if not sl["name"].startswith("bay_") and "~g" not in sl["name"] and sl["name"] != "bong":
                    P.alpha[sl["name"]] = min(1.0, t / 0.10)
            for q in QUY:
                P.scale(f"dao_{q['j']}", 0.02, 0.02)
            for b_ in ("tt_sau", "tt_truoc", "tt_nam_g"):
                P.scale(b_, 1.0, 0.55)
            return
        b = math.exp(-(t - T_DAP) / 0.09) * math.cos((t - T_DAP) * 2 * math.pi / 0.22)
        P.scale("all3", 1 + 0.10 * b, 1 - 0.12 * b)
        duoi(P, t - T_DAP, min(1.0, (t - T_DAP) / 0.4) * 1.4)
        for q in QUY:                                                   # thiên thạch nở từ thân ra quỹ đạo
            j = q["j"]
            u = ease((t - T_TRO[j]) / 0.30, "out") if t > T_TRO[j] else 0.0
            s_ = max(0.02, u * (1 + 0.18 * math.sin(math.pi * u)))
            P.scale(f"dao_{j}", s_, s_)
            co_quy(P, j, 0, 1.0 - u)
        dung_ = ease((t - 0.85) / 0.35, "out") if t > 0.85 else 0.0
        s_ = 0.55 + 0.45 * dung_ + 0.10 * math.sin(math.pi * dung_)
        for b_ in ("tt_sau", "tt_truoc", "tt_nam_g"):
            P.scale(b_, 1.0, s_)
        if t > T_GAM0 - 0.15:
            w = ease((t - (T_GAM0 - 0.15)) / 0.15) * (1 - ease((t - T_GAM1) / (D_APPEAR - 0.1 - T_GAM1)))
            P.rot("all6", 14.0 * w)
            P.rot("all5", 4.0 * w)
            P.rot("all10", HA * 16.0 * w)
            if T_GAM0 < t < T_GAM1:
                r = hoat.rung(t, T_GAM0, T_GAM1, 2)
                P.rot("all4", 1.5 * r)
                P.rot("tt_sau", 3.0 * r)
                P.rot("tt_truoc", -3.0 * r)

    T_PHONG_ = T_PHONG[:len(QUY)]                                      # dạng non: ba thiên thạch
    clips = [
        Clip("appear", D_APPEAR, f_appear, ev=[(T_DAP, "cham_dat", ""), (T_DAP, "nen", ""),
                                               *[(tk, "tro_lai", "") for tk in T_TRO[:len(QUY)]], (T_GAM0, "gam", "")]),
        Clip("idle", D_IDLE, f_idle, loop=True),
        Clip("walk", CD["run_01"][0], f_walk, loop=True),
        Clip("attack", D_ATK, f_attack, ev=[(0.30, "vo", ""), (T_ATK, "trung", ""), (T_ATK + 0.13, "xe", ""), (T_ATK + 0.26, "xe", "")],
             trung=T_ATK),
        Clip("cast", D_CAST, f_cast, ev=[(T_XOA0, "xoa", ""), (0.40, "quay_nhanh", ""), (T_TU0, "tu", ""),
                                         *[(tk, "phong", str(j)) for j, tk in enumerate(T_PHONG_)],
                                         *[(tk + BAY, "no", str(j)) for j, tk in enumerate(T_PHONG_)], (T_PHONG[0] + BAY, "trung", ""),
                                         (T_MOC_C, "moc", "")], trung=T_PHONG[0] + BAY),
        Clip("skill", D_SKILL, f_skill, ev=[(T_CUON1, "cuon", ""), (0.40, "quay_nhanh", ""), (T_LEN0, "bay_len", ""),
                                             (T_LEN1 + 0.02, "lua", ""), (T_NO, "no_lon", ""), (T_NO, "trung", ""), (T_BUNG1, "bung", ""),
                                             (T_VE, "cham_dat", "")], trung=T_NO),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", CD["die_01"][0] + TAN, f_die),
        Clip("aura", D_AURA, f_aura, loop=True),
    ]
    if os.environ.get("TH_GOC"):
        clips += [Clip("g_" + n, CD[n][0], (lambda t, P, n=n: dat(P, n, t, bo=BO_QIU))) for n in CD]
    return clips, than_cast, cho_phong


def them_cum_bay(sk, than_cast, cho_phong, cao, far_xy=None):
    """xương far + fly_<j> + bay_<j> và slot bản sao (ẩn, vẽ trên cùng) cho từng thiên thạch phóng ở cast: xương đặt ở chỗ phóng."""
    fx, fy = far_xy if far_xy is not None else (0.9 * cao + 140.0, 0.45 * cao)
    sk.xuong("far", "root", float(fx), float(fy))
    for q in sk.info["quy"]:
        j, c = q["j"], q["c"]
        V = np.asarray(q["V"])
        m = cho_phong(T_PHONG[j], j)
        V2 = V - V.mean(0) + m
        sk.xuong(f"fly_{j}", "root", float(m[0]), float(m[1]))
        sk.xuong(f"bay_{j}", f"fly_{j}", float(m[0]), float(m[1]), goc=0.0, the_gioi=True)
        sk.slot(f"bay_{j}", "move", c, an=True)
        sk.luoi_gan(f"bay_{j}", c, q["L"], [{f"bay_{j}": 1.0}] * q["L"].n, the_gioi=V2)


def dung_het(far_xy=None):
    sk, info = dung()
    ve0 = soi.Ve(sk)
    clips, than_cast, cho_phong = lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    bo = ("rung", "tt_nam", "bong") + tuple(s["name"] for s in sk.slots if s["name"].startswith("cum"))
    cao = soi.chieu_cao(ve0, idle0, bo=bo)
    clips, than_cast, cho_phong = lam_clip(sk, info, cao)
    them_cum_bay(sk, than_cast, cho_phong, cao, far_xy)
    clips, _, _ = lam_clip(sk, info, cao)
    return sk, info, clips, cao


AURA = {}


def main_soi(sk, ve0, c, spec, sc, clips=None):
    fr = hoat.nuong(sk, c)
    if clips is not None and c.ten != "aura":
        if "fr" not in AURA:
            ca = [x for x in clips if x.ten == "aura"]
            AURA["fr"] = hoat.nuong(sk, ca[0]) if ca else None
        if AURA["fr"]:
            fr = hoat.phu_aura(fr, AURA["fr"], sk)
    if ":" in spec:
        t0, t1, n = spec.split(":")
        ts = list(np.linspace(float(t0), float(t1), int(n)))
    elif spec.startswith("n="):
        ts = list(np.linspace(0, c.dur, int(spec[2:])))
    else:
        ts = [float(x) for x in spec.split(",")]
    Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
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
    sk, info, clips, cao = dung_het()
    ve0 = soi.Ve(sk)
    print(f"chiều cao {cao:.0f}")
    if a and a[0] == "kiem":
        for c in clips:
            fr = hoat.nuong(sk, c)
            xau = []
            for i in range(1, len(fr)):
                A, B = fr[i - 1], fr[i]
                for b in set(A.t) | set(B.t):
                    da = abs(B.t.get(b, khung.ZERO)[2] - A.t.get(b, khung.ZERO)[2])
                    if da > 35.0 and not b.startswith(("bay_", "fly_", "qiu_", "quy", "dao", "bong")):
                        xau.append(f"{i / 30:.2f}s {b} xoay {da:.0f}°")
            Wl = [sk.the_gioi(P) for P in fr]
            for b in ("all6", "all10", "xiaobi_r2", "shouzhang_l", "duoi2", "tt_sau", "tt_truoc"):
                for i in range(1, len(fr)):
                    d = float(np.hypot(*(Wl[i][b][:2, 2] - Wl[i - 1][b][:2, 2])))
                    if d > 0.22 * cao and c.ten not in ("appear", "skill") and not (c.ten == "attack" and False):
                        xau.append(f"{i / 30:.2f}s {b} dời {d / cao:.2f} cao/khung")
            print(f"{c.ten}: {len(fr)} khung" + ("" if not xau else " | " + "; ".join(xau[:14]) + (" ..." if len(xau) > 14 else "")))
        return
    if a and a[0] == "soi":
        if a[1] == "all":
            for c in clips:
                main_soi(sk, ve0, c, a[2] if len(a) > 2 else "n=10", float(a[3]) if len(a) > 3 else 0.16, clips)
            return
        c = [x for x in clips if x.ten == a[1]][0]
        main_soi(sk, ve0, c, a[2], float(a[3]) if len(a) > 3 else 0.22, clips)
        return
    if False:
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
        sc = float(a[3]) if len(a) > 3 else 0.22
        cot = min(len(Ps), 6)
        hang = (len(Ps) + cot - 1) // cot
        out = None
        for i, P in enumerate(Ps):
            im = ve0.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB")
            ImageDraw.Draw(im).text((6, 4), f"{ts[i]:.2f}", fill=(255, 255, 255))
            if out is None:
                out = Image.new("RGB", (im.width * cot, im.height * hang), (150, 150, 150))
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    tieu = ("Thiên Thạch Thú Non (tinh_hach_non): tướng 9 đảo Thổ, dạng 1" if NON else "Thiên thạch thú (tinh_hach_1): tướng 9 đảo Thổ")
    xuat.xuat_het(sk, clips, RA, TEN_RIG, tieu_de=tieu, dang=1, so_dang=1,
                  dung_yen=("cast",), lao=("attack", "skill"), far=("cast",), ma_goc=None, khop_idle=0.2, cao=cao, impact=IMPACT,
                  tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.4, tran_mb=0.7, span=3.4)


if __name__ == "__main__":
    main(sys.argv[1:])
