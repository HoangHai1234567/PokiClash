# -*- coding: utf-8 -*-
"""Dòng cá voi biến dị (mã làm việc `ca_voi`, tướng thứ 7 đảo Thủy, 2026-11-11): cắt mảnh từ concept đã duyệt, dựng rig, clip.

    py -3 -I ArtGen/Spine/ca_voi.py cat 1|2      cắt concept dạng k -> inbox/ca_voi_<k>/manh/ (+ manh.json, _soi.png, _nhan.png, _ghep.png)
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/ca_voi.py rig 1|2
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/ca_voi.py all        dạng 2, rồi dạng 1 gộp bản nhẹ của dạng 2 (evolve)

Mảnh chia MỘT – MỘT theo file Spine của con gốc `monster_3281` (ghi chú inbox/ca_voi_ghichu.md), sau -> trước:
  vay_x      vây ngực bên xa + ba móng (con gốc: chân trước bên xa P_tuiL01..05)
  vay_duoi   vây đuôi đá đen hai thuỳ (con gốc: ba tinh thể P_ci01..03)
  duoi       mông + cuống đuôi + mẩu đá trên lưng đuôi, lưới chuỗi xương (P_weiba)
  hong       vách họng tím sẫm, tô bằng mã: lúc nghỉ nấp sau hai hàm, há to thì căng giữa hai hàm (con gốc: lòng miệng nằm trên P_mouth02)
  ham_duoi   hàm dưới + bụng + dải sóng + sàn miệng (P_mouth02)
  ham_tren   vòm hàm trên + dải môi + vòm họng + lỗ phun + ba con hà (P_mouth01)
  d1..d5     năm nanh dưới, t1..t5 năm nanh trên: mỗi nanh một mảnh cứng, một xương (P_ya01..10)
  vay_g      vây ngực bên gần + ba móng (con gốc: chân sau bên gần P_tuiR01..05)
Mọi mảnh cắt thẳng từ concept (khớp concept 100 %); chỗ bị che tô lại bằng vân sáp chép từ chỗ sạch cùng màu.
Toạ độ trong CFG là pixel concept (1536 x 1024, y xuống).
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ca_den as CD  # noqa: E402  (nen_trang, cum, cum_chua, lap_lo, gian, co, da_giac, hop, mem_alpha, luu, o_van, lat, to_lai)

sys.stdout.reconfigure(encoding="utf-8")
CODE = "ca_voi"
GRAY = (150, 150, 150)
FONT = "C:/Windows/Fonts/arial.ttf"
MUC_RGB = (58, 32, 12)

# màu chuẩn để phân lớp pixel (đo trên concept từng dạng)
TEN = ["trang", "muc", "lam", "nhat", "bang", "man", "sanho", "kem", "da", "xam"]
MAU = {
    2: {"trang": (254, 254, 254), "muc": (58, 32, 12), "lam": (31, 76, 138), "nhat": (66, 150, 198), "bang": (226, 245, 250),
        "man": (162, 34, 91), "sanho": (236, 74, 107), "kem": (254, 242, 190), "da": (48, 44, 50), "xam": (100, 94, 106)},
    1: {"trang": (254, 254, 254), "muc": (58, 32, 12), "lam": (50, 122, 180), "nhat": (113, 175, 210), "bang": (236, 246, 248),
        "man": (205, 62, 111), "sanho": (252, 124, 142), "kem": (254, 241, 194), "da": (48, 44, 48), "xam": (116, 112, 120)},
}
I = {t: i for i, t in enumerate(TEN)}

CFG = {
    1: {                                 # cá voi con (số đọc trên inbox/ca_voi_1/mau/luoi_480_390.png)
        "dat": 866,
        "ngam": 0.80,                    # môi khép chừng này quãng lúc ngậm
        "truot_nanh_d": -56,             # ba nanh dưới nằm đúng dưới ba nanh trên: lúc ngậm trượt dọc môi về phía bản lề nửa khoảng
        #                                  cách (px concept) để hai hàng so le, cài răng lược như dạng 2 (không chồng lên nhau)
        "ban_le": (764, 647),
        "mui_tren": (1165, 584),
        "mui_duoi": (1168, 743),
        "tam_mieng": (974, 625),
        "than": (790, 690),
        "cat_lung": ((725, 570), (790, 665)),
        "hat": {"vay_g": (756, 743), "vay_x": (1162, 825), "duoi": (656, 725), "song": (856, 772)},
        "mong_g": (665, 818, 850, 880),
        "mong_x": (1030, 818, 1205, 880),
        "vay_duoi_x": 596,
        "day_than": [(680, 778), (740, 812), (800, 834), (842, 845)],
        "vay_x_them": [(1120, 760), (1150, 760), (1150, 800), (1120, 800)],
        "mep_tren": [(774, 647), (815, 619), (862, 566), (892, 537), (939, 516), (980, 505), (1045, 502), (1092, 516), (1133, 537),
                     (1145, 566), (1148, 602), (1139, 625)],
        "mep_duoi": [(774, 649), (809, 672), (845, 702), (880, 731), (927, 743), (980, 749), (1039, 749), (1086, 734), (1121, 702),
                     (1136, 666), (1139, 628)],
        "moi_ngoai": [(768, 643), (798, 608), (833, 566), (892, 516), (951, 487), (1009, 469), (1068, 466), (1127, 478), (1162, 511),
                      (1174, 566), (1165, 614), (1142, 628)],
        "ranh_tong": [(774, 647), (833, 646), (892, 637), (951, 622), (1009, 611), (1068, 608), (1115, 614), (1139, 628)],
        "bang_khuat": [(774, 649), (827, 719), (842, 845), (740, 812), (715, 770), (735, 690)],
        "noi_khuat": [(774, 649), (735, 690), (715, 770), (740, 812)],
        "duoi_khop": [(715, 722), (680, 728), (645, 728), (612, 720), (586, 712)],
        "vay_duoi_khop": {"goc": (580, 708), "tren": (512, 616), "duoi": (509, 781)},
        "ban_g": (756, 860), "vai_g": (756, 649),
        "ban_x": (1118, 860), "vai_x": (1118, 760),
    },
    2: {
        "dat": 914,                      # mặt đất (đáy móng)
        "ngam": 0.74,                    # nanh rất to: môi chỉ khép chừng này quãng, hai hàng nanh đan cài vừa đủ
        "ban_le": (782, 600),            # bản lề hai hàm: ngay sau khoé nhọn của miệng, trên đỉnh vây gần
        "mui_tren": (1330, 470),         # đầu trước của hàm trên (má phải)
        "mui_duoi": (1335, 720),         # đầu trước của hàm dưới (cằm)
        "tam_mieng": (1110, 585),        # tâm miệng (xương mieng cho VFX)
        "than": (800, 650),              # tâm thân
        "cat_lung": ((700, 530), (790, 640)),     # đường chia mảng lam: bên phải là vòm hàm trên, bên trái là mông + đuôi
        "hat": {"vay_g": (700, 720), "vay_x": (1385, 825), "duoi": (500, 720), "song": (880, 790)},
        "mong_g": (575, 838, 880, 930),  # hộp chứa ba móng vây gần
        "mong_x": (1180, 838, 1450, 930),
        "vay_duoi_x": 300,               # đá bên trái cột này là vây đuôi
        "day_than": [(628, 792), (700, 822), (780, 848), (862, 864)],     # đáy thân khuất sau vây gần (nối đáy đuôi với đáy bụng)
        "vay_x_them": [(1296, 640), (1306, 612), (1326, 604), (1344, 618), (1350, 680), (1356, 740), (1372, 800), (1300, 860),
                       (1268, 790), (1280, 700)],  # phần vây xa khuất sau hàm dưới
        # mép miệng (phần khuất sau gốc nanh khai tay, đọc trên ảnh kẻ lưới), từ khoé nhọn phía sau tới khoé trước
        "mep_tren": [(797, 598), (868, 558), (936, 499), (985, 450), (1040, 400), (1100, 372), (1180, 360), (1260, 385), (1310, 440),
                     (1335, 520), (1325, 585)],
        "mep_duoi": [(797, 602), (905, 658), (960, 690), (1030, 728), (1120, 752), (1220, 738), (1280, 690), (1312, 620), (1325, 585)],
        "moi_ngoai": [(797, 585), (868, 522), (936, 467), (1005, 390), (1073, 347), (1164, 329), (1255, 354), (1309, 404), (1338, 458),
                      (1346, 540), (1335, 590)],                         # mép ngoài của dải môi trên (ranh với mảng lam)
        "ranh_tong": [(797, 600), (936, 590), (1030, 572), (1118, 554), (1200, 556), (1280, 580), (1325, 585)],   # vòm họng | sàn miệng
        # phần hàm dưới (trắng băng) khuất sau vây gần, và nét ranh với mảng lam
        "bang_khuat": [(797, 600), (862, 640), (866, 866), (700, 824), (672, 740), (720, 640)],
        "noi_khuat": [(797, 600), (720, 640), (672, 740), (700, 824)],
        "duoi_khop": [(700, 690), (610, 715), (520, 722), (440, 712), (360, 696), (290, 684)],        # chuỗi xương đuôi, gốc -> chót
        "vay_duoi_khop": {"goc": (270, 684), "tren": (150, 520), "duoi": (130, 850)},
        "ban_g": (720, 900), "vai_g": (745, 610),
        "ban_x": (1320, 900), "vai_x": (1320, 700),
    },
}


def d_inbox(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}")


def concept(k):
    return os.path.join(d_inbox(k), "tai_ve", "L1_duyet.png")


# ================================================================ phân lớp màu
def phan_lop(a, mau):
    """nhãn màu từng pixel (chỉ số trong TEN). Mực nâu và đá đen đều tối: mực ngả nâu (R − B lớn), đá trung tính."""
    b = cv2.GaussianBlur(a.astype(np.float32), (0, 0), 1.4)
    C = np.array([mau[t] for t in TEN], np.float32)
    d = ((b[:, :, None, :] - C[None, None]) ** 2).sum(3)
    nau = (b[..., 0] - b[..., 2]) > 18
    toi = b.max(2) < 120
    d[..., I["da"]][toi & nau] = 1e12
    d[..., I["xam"]][toi & nau] = 1e12
    d[..., I["muc"]][toi & ~nau] = 1e12
    lam_that = (b[..., 2] - b[..., 0]) > 40           # mép mực pha với màu khác ra xám nâu: chỉ nhận lam khi thật ngả lam
    for t in ("lam", "nhat"):
        d[..., I[t]][~lam_that] = 1e12
    return cv2.medianBlur(d.argmin(2).astype(np.uint8), 5)


def gan_nhat(L, lo, cho_phep):
    """nhãn gần nhất (chỉ trong các nhãn cho_phep, lấy từ ngoài vùng lo) cho mọi pixel."""
    src = np.isin(L, cho_phep) & ~lo
    _, lab = cv2.distanceTransformWithLabels((~src).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    lut = np.zeros(int(lab.max()) + 1, np.uint8)
    lut[lab[src]] = L[src]
    return lut[lab]


def ke_muc(img, m, day=3):
    """tô mực lên mặt nạ nét m (nới `day` px), mép mềm, hơi rung màu như bút."""
    mm = CD.gian(m, day).astype(np.float32)
    mf = cv2.GaussianBlur(mm, (0, 0), 0.9)[..., None]
    rng = np.random.default_rng(11)
    nhieu = cv2.GaussianBlur(rng.normal(0, 1, img.shape[:2]).astype(np.float32), (0, 0), 1.5)[..., None] * 12
    col = np.array(MUC_RGB, np.float32)[None, None] + nhieu
    return img * (1 - mf) + col * mf, mm > 0


def ranh(G, a_, b_):
    """pixel nằm trên ranh giữa hai nhóm nhãn a_, b_ của bản đồ nhãn G."""
    A = np.isin(G, a_)
    B = np.isin(G, b_)
    return (CD.gian(A, 1) & B) | (CD.gian(B, 1) & A)


def truc_chinh(m):
    """hai đầu mút theo trục chính của một mặt nạ: trả (p0, p1) toạ độ (x, y)."""
    ys, xs = np.nonzero(m)
    P = np.stack([xs, ys], 1).astype(np.float64)
    c = P.mean(0)
    _, _, vt = np.linalg.svd(P - c, full_matrices=False)
    t = (P - c) @ vt[0]
    return c + vt[0] * t.min(), c + vt[0] * t.max()


# ================================================================ cắt mảnh
def cat(k):
    c = CFG[k]
    a = np.array(Image.open(concept(k)).convert("RGB")).astype(np.float32)
    Hh, Wd = a.shape[:2]
    bg = CD.nen_trang(a, 238)
    fig = ~bg
    L = phan_lop(a, MAU[k])
    L[bg] = I["trang"]
    ra = os.path.join(d_inbox(k), "manh")
    os.makedirs(ra, exist_ok=True)
    yy, xx = np.mgrid[0:Hh, 0:Wd]
    is_ = lambda *ts: np.isin(L, [I[t] for t in ts])
    muc = is_("muc") & fig
    Hb = np.array(c["ban_le"], float)
    Mc = np.array(c["tam_mieng"], float)

    def them_muc(m, r=9):
        """thêm nét mực sát mảng màu m (nét chung của hai mảnh kề nhau thuộc cả hai)."""
        return CD.lap_lo(m | (CD.gian(m, r) & muc))

    # ---------- nanh và hà (kem)
    kem = [q for q in CD.cum(is_("kem") & fig, 300)]
    nanh = [q for q in kem if (q["x0"] + q["x1"]) / 2 > Hb[0] + 100]
    ha = [q for q in kem if (q["x0"] + q["x1"]) / 2 <= Hb[0] + 100]
    for q in nanh:
        ys, xs = np.nonzero(q["m"])
        q["c"] = (float(xs.mean()), float(ys.mean()))
    # hàng trên / dưới: nanh trên có gốc ở phía trên tâm miệng
    tren = sorted([q for q in nanh if q["c"][1] < Mc[1] - 5], key=lambda q: q["c"][0])
    duoi = sorted([q for q in nanh if q["c"][1] >= Mc[1] - 5], key=lambda q: q["c"][0])
    print(f"dạng {k}: {len(tren)} nanh trên, {len(duoi)} nanh dưới, {len(ha)} con hà")
    ten_nanh = [(f"t{i + 1}", q) for i, q in enumerate(tren)] + [(f"d{i + 1}", q) for i, q in enumerate(duoi)]
    m_nanh_all = np.zeros((Hh, Wd), bool)
    for _, q in ten_nanh:
        q["mk"] = them_muc(q["m"], 8)
        m_nanh_all |= q["mk"]
    m_nanh_mau = np.zeros((Hh, Wd), bool)
    for _, q in ten_nanh:
        m_nanh_mau |= q["m"]

    # ---------- vây gần, vây xa (lam + móng đá + mực)
    lam = is_("lam") & fig
    da = is_("da", "xam") & fig

    def vay(hat, hop_mong):
        v = CD.cum_chua(lam, hat)
        x0, y0, x1, y1 = hop_mong
        mong = da & (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)
        return v, mong
    vg, mong_g = vay(c["hat"]["vay_g"], c["mong_g"])
    vx, mong_x = vay(c["hat"]["vay_x"], c["mong_x"])
    lung0 = CD.cum_chua(lam, c["hat"]["duoi"])
    if (vg & lung0).any() or (vx & lung0).any():
        raise SystemExit("vây dính liền với lưng (viền vây hở): cần cắt tay")
    m_vg = CD.lap_lo(CD.co(CD.gian(them_muc(vg | mong_g, 9), 3), 3)) & fig
    m_vx = CD.lap_lo(CD.co(CD.gian(them_muc(vx | mong_x, 9), 3), 3)) & fig
    print(f"  vây gần {int(vg.sum())} px + móng {int(mong_g.sum())}; vây xa {int(vx.sum())} px + móng {int(mong_x.sum())}")

    # ---------- đá: vây đuôi (bên trái), mẩu đá trên lưng đuôi (thuộc mảnh đuôi)
    da_khac = da & ~mong_g & ~mong_x
    vd_mau = da_khac & (xx < c["vay_duoi_x"])
    cum_vd = CD.cum(vd_mau, 100)
    lon_nhat = max([q["dt"] for q in cum_vd] or [1])
    for q in cum_vd:                         # chỉ giữ hai thuỳ lớn; mẩu nhỏ (dưới 1/4 thuỳ lớn nhất) trả về đuôi
        if q["dt"] < 0.25 * lon_nhat:
            vd_mau &= ~q["m"]
    da_duoi = da_khac & ~vd_mau
    m_vd = them_muc(vd_mau, 9)

    # ---------- bản đồ nhãn "phía sau": chỗ nhìn thấy giữ nhãn của chính nó; chỗ bị nanh / vây gần che thì gán theo hình học khai
    #   trong CFG (mép miệng trên, mép miệng dưới, ranh hai tông, phần hàm dưới khuất sau vây)
    NEN = [I[t] for t in ("lam", "nhat", "bang", "man", "sanho")]
    dx = [p[0] for p in c["day_than"]]
    dy = [p[1] for p in c["day_than"]]
    duoi_day = yy > np.interp(xx, dx, dy, left=dy[0], right=dy[-1])
    vg_no = CD.gian(m_vg, 3) & fig                              # nới 3 px cho hết viền răng cưa của nét vây
    khuat_g = vg_no & ~duoi_day                                 # bóng thân khuất sau vây gần (trên đường đáy thân nội suy)
    than_nhin = fig & ~vg_no & ~m_vx & ~m_vd                    # phần thân nhìn thấy (kể cả mực, nanh, hà)
    than_day = CD.lap_lo(than_nhin | khuat_g) & ~(m_vx & ~CD.gian(than_nhin, 2)) & ~(m_vd & ~CD.gian(than_nhin, 2))
    than_day &= ~(vg_no & duoi_day)
    nanh_no = CD.gian(m_nanh_all, 5)                              # nới 3 px cho hết viền răng cưa của nét nanh
    che = (nanh_no | khuat_g) & than_day

    def duong(pts, day=1):
        m = np.zeros((Hh, Wd), np.uint8)
        cv2.polylines(m, [np.round(np.array(pts, float)).astype(np.int32)], False, 1, day, cv2.LINE_8)
        return m > 0
    MO = CD.da_giac(a.shape, list(c["mep_tren"]) + list(c["mep_duoi"])[::-1])          # lòng miệng đầy đủ
    rx = [p[0] for p in c["ranh_tong"]]
    ry = [p[1] for p in c["ranh_tong"]]
    tren_ranh = yy < np.interp(xx, rx, ry, left=ry[0], right=ry[-1])
    mx = [p[0] for p in c["mep_tren"]]
    tren_mieng = yy < Mc[1]                                                               # ngoài lòng miệng: phía trên hay phía dưới
    G_lam = gan_nhat(L, m_nanh_all | m_vg | m_vx | muc | bg, [I["lam"], I["nhat"]])       # dải môi nối dài sau gốc nanh
    G_bang = gan_nhat(L, m_nanh_all | m_vg | m_vx | muc | bg, [I["bang"], I["nhat"]])     # dải sóng nối dài sau vây gần
    G = L.copy()
    muc_ngoai = muc & CD.gian(bg, 10)                             # nét viền ngoài của thân: nanh và thân dùng chung, không tô đè
    z = nanh_no & than_day & ~muc_ngoai
    dai_moi = CD.da_giac(a.shape, list(c["moi_ngoai"]) + list(c["mep_tren"])[::-1])
    che = z | khuat_g
    G[z & MO & tren_ranh] = I["man"]
    G[z & MO & ~tren_ranh] = I["sanho"]
    G[z & ~MO & tren_mieng & dai_moi] = I["nhat"]
    G[z & ~MO & tren_mieng & ~dai_moi] = I["lam"]
    G[z & ~MO & ~tren_mieng] = I["bang"]
    bk = CD.da_giac(a.shape, c["bang_khuat"])
    G[khuat_g & bk] = G_bang[khuat_g & bk]
    G[khuat_g & ~bk] = I["lam"]

    # ---------- tấm vân từng màu
    def van(ten, mk=None):
        sach = CD.co((is_(ten) & fig) if mk is None else mk, 7)
        return CD.lat(a.shape, CD.o_van(a, sach, co_o=64, chong=16))
    VAN = {}
    for t in ("lam", "nhat", "bang", "man", "sanho"):
        try:
            VAN[I[t]] = van(t)
        except SystemExit:
            VAN[I[t]] = np.zeros_like(a) + np.array(MAU[k][t], np.float32)
    try:
        van_da = van("da", vd_mau & is_("da"))
    except SystemExit:                       # thuỳ đá hẹp, không đủ ô vân sạch: tô màu đá đều, thêm hạt nhẹ
        rng = np.random.default_rng(5)
        van_da = np.zeros_like(a) + np.array(MAU[k]["da"], np.float32) + cv2.GaussianBlur(
            rng.normal(0, 1, a.shape[:2]).astype(np.float32), (0, 0), 1.2)[..., None] * 10

    # ---------- ảnh "phía sau" đầy đủ: concept, những chỗ bị nanh / vây che tô lại theo nhãn G, kẻ lại nét mực
    sau = a.copy()
    for i_ in NEN:
        sau = CD.to_lai(sau, che & (G == i_), VAN[i_], mem=1.0)
    net = (duong(c["mep_tren"]) | duong(c["mep_duoi"])) & CD.gian(nanh_no, 2)          # mép miệng khuất sau nanh
    net |= duong(c["noi_khuat"]) & CD.gian(khuat_g, 2)                                    # ranh hàm dưới | mảng lam sau vây gần
    net |= duong(c["day_than"]) & CD.gian(vg_no, 1)                                        # đáy thân sau vây gần
    net |= ranh(G, [I["nhat"]], [I["bang"]]) & khuat_g                                    # mép dải sóng sau vây gần
    sau, m_net = ke_muc(sau, net, 3)
    muc_sau = (muc & ~che) | m_net

    def lap_nho(m, dt=700):
        """lấp các lỗ nhỏ (dưới dt px) của mặt nạ; lỗ lớn giữ nguyên."""
        lo_ = CD.lap_lo(m) & ~m
        for q in CD.cum(lo_, 1):
            if q["dt"] < dt:
                m = m | q["m"]
        return m

    def them_muc_sau(m, r=9):
        return lap_nho(m | (CD.gian(m, r) & muc_sau & than_day))

    # ---------- chia thân thành ba mảng theo nhãn G
    (ax, ay), (bx, by) = c["cat_lung"]
    xa_cat = ((xx - ax) * (by - ay) - (yy - ay) * (bx - ax)) / math.hypot(bx - ax, by - ay)   # > 0: bên phải đường cắt (phía đầu)
    phai = xa_cat > 0
    than_mau = than_day & ~muc_sau & np.isin(G, NEN)
    lam_G = than_mau & (G == I["lam"])
    nhat_G = than_mau & (G == I["nhat"])
    man_G = than_mau & (G == I["man"])
    # dải môi = phần "nhat" phía trên mép miệng; dải sóng + rãnh họng = phần "nhat" nằm trong hàm dưới
    moi = nhat_G & (yy < np.interp(xx, [p[0] for p in c["mep_duoi"]], [p[1] for p in c["mep_duoi"]]) - 4) & (xx > Hb[0] - 10)
    song = nhat_G & ~moi
    # ĐÁY BỤNG TÔ TRƠN (người dùng 2026-11-11: "những đoạn đáy để màu trơn thôi cho đỡ lộ khuyết điểm"): bỏ dải sóng và rãnh họng trên
    # hàm dưới, tô lại trắng băng. Hoa văn nằm trên vùng lưới bị kéo nén nhiều (bụng, chỗ khuất sau vây) nên méo là thấy ngay.
    xoa_day = np.zeros((Hh, Wd), bool)
    if c.get("day_tron", True):
        giu = CD.gian(muc_ngoai, 1) | CD.gian(duong(c["day_than"]) | duong(c["noi_khuat"]), 5) | CD.gian(MO, 12)
        lam_that = CD.gian(CD.co(lam_G, 3), 6)                    # mảng lam thật (bỏ các chấm lam lẫn trong nét mực)
        xoa_day = CD.gian(song, 17) & than_day & ~giu & ~lam_that
        sau = CD.to_lai(sau, xoa_day, VAN[I["bang"]], mem=1.0)
        muc_sau = muc_sau & ~xoa_day
        # màu của dải sóng còn sót sát các nét được giữ (đáy thân khuất sau vây...): tô nốt, chỉ đụng pixel màu, không đụng mực
        sot = CD.gian(song, 2) & than_day & ~muc_sau & ~xoa_day & ~lam_that & ~CD.gian(MO, 4)
        sau = CD.to_lai(sau, sot, VAN[I["bang"]], mem=0.8)
        xoa_day = xoa_day | sot
        # mực còn sót nằm sâu trong lòng mảng trắng băng (cách viền mảng từ 14 px, không sát miệng) cũng là nét hoa văn: xoá nốt
        trong = CD.co(CD.lap_lo(CD.gian((than_mau & (G == I["bang"])) | song | xoa_day, 6)), 14)
        xoa2 = CD.gian(muc_sau & trong & ~giu, 4) & trong & ~giu
        sau = CD.to_lai(sau, xoa2, VAN[I["bang"]], mem=1.0)
        muc_sau = muc_sau & ~xoa2
        xoa_day = xoa_day | xoa2
        print(f"  đáy trơn: dải sóng + rãnh họng {int(song.sum())} px, tô lại {int(xoa_day.sum())} px, trong đó mực {int((xoa_day & muc).sum())} px; "
              f"mực sát dải sóng bị giữ lại {int((CD.gian(song, 17) & muc & than_day & giu).sum())} px")
    ha_m = np.zeros((Hh, Wd), bool)                              # hà thuộc vòm hàm trên
    ha_d = np.zeros((Hh, Wd), bool)                              # hà thuộc mông + đuôi (tâm nằm bên trái đường cắt)
    for q in ha:
        ys_, xs_ = np.nonzero(q["m"])
        if xa_cat[int(ys_.mean()), int(xs_.mean())] > 0:
            ha_m |= q["m"]
        else:
            ha_d |= q["m"]
    def mo(m, r=3):
        """bỏ sợi mảnh (pixel răng cưa ở mép nét mực bị xếp nhầm màu): co rồi nới lại."""
        return CD.gian(CD.co(m, r), r) & m
    tren_mau = mo((lam_G & phai) | moi | ha_m)
    duoi_mau = mo((than_mau & np.isin(G, [I["bang"], I["sanho"]])) | song | xoa_day)
    duoi_d_mau = mo((lam_G & (xa_cat < 70)) | (da_duoi & than_day) | ha_d)   # mông + đuôi: lấn 70 px sang phải (nấp dưới vòm)
    m_tren = them_muc_sau(tren_mau)
    m_duoi = them_muc_sau(duoi_mau)
    m_dd = them_muc_sau(duoi_d_mau)
    # mực ở lưng bên trái đường cắt quá 10 px thuộc mông, không thuộc vòm
    m_tren &= ~(muc_sau & (xa_cat < -10))
    m_tren = lap_nho(m_tren)
    # bỏ sợi mực mảnh (dưới 9 px) chìa ra khỏi mảnh: nét viền chung với mảnh khác, há miệng thì thành sợi râu
    m_tren = CD.gian(CD.co(m_tren, 4), 4) & m_tren
    m_duoi = CD.gian(CD.co(m_duoi, 4), 4) & m_duoi

    # ---------- vòm họng: mảnh riêng nằm SAU hàm dưới (đi theo hàm trên). Để chung mảnh hàm trên thì lúc ngậm miệng nó đè lên hàm dưới,
    #   lộ nguyên mảng tím (người dùng báo 2026-11-11). Nới 14 px ra mọi phía (tô tím) để hai hàm xê dịch không hở.
    man_s = mo(man_G)
    m_vom = CD.gian(man_s, 14) & than_day
    img_vom = CD.to_lai(sau.copy(), m_vom & ~CD.co(man_s, 2), VAN[I["man"]], mem=1.0)

    # ---------- vách họng (tô bằng mã): toàn bộ bóng hai hàm co vào 10 px, phía trước bản lề; mép phải có vành môi + nét mực
    hai_ham = CD.lap_lo(m_tren | m_duoi | m_vom)
    hong = CD.co(hai_ham, 10) & (xx > Hb[0] + 24)
    hong = CD.cum_chua(hong, (int(Mc[0]), int(Mc[1])))
    img_hong = np.zeros_like(a) + VAN[I["man"]]
    vanh = hong & ~CD.co(hong, 9) & (xx > Mc[0])                         # vành môi "mép bên kia" ở mép phải vách họng
    img_hong = CD.to_lai(img_hong, vanh, VAN[I["nhat"]], mem=0.8)
    img_hong, _ = ke_muc(img_hong, hong & ~CD.co(hong, 3), 1)

    # ---------- vây xa: thêm phần khuất sau hàm dưới (lam + nét mực hai bên)
    them = CD.da_giac(a.shape, c["vay_x_them"]) & ~m_vx
    img_vx = a.copy()
    img_vx = CD.to_lai(img_vx, them, VAN[I["lam"]], mem=1.0)
    m_vx_day = CD.lap_lo(m_vx | them)
    img_vx, _ = ke_muc(img_vx, m_vx_day & ~CD.co(m_vx_day, 3) & CD.gian(them, 3), 2)

    # ---------- vây đuôi: lấp chỗ chót đuôi che (giữa hai thuỳ) bằng vân đá
    gy = c["vay_duoi_khop"]["goc"]
    noi = CD.da_giac(a.shape, [(gy[0] - 40, gy[1] - 34), (gy[0] + 14, gy[1] - 26), (gy[0] + 18, gy[1] + 30), (gy[0] - 40, gy[1] + 40)])
    noi &= ~m_vd
    img_vd = CD.to_lai(a.copy(), noi, van_da, mem=1.0)
    m_vd_day = CD.lap_lo(m_vd | noi)

    # ---------- mông + đuôi: phần lấn dưới vòm và phần khuất sau vây gần đã có trong ảnh `sau`
    # ---------- lưu
    manh, info = {}, {"nanh": {}, "kich_thuoc": [Wd, Hh]}

    def luu(ten, img, m, mem=True):
        al = CD.mem_alpha(m) if mem else m.astype(np.float32)
        box = CD.hop(m, 3)
        CD.luu(img, al, box, os.path.join(ra, ten + ".png"))
        manh[ten] = box
    # vây xa = MỘT CÁNH VÂY ĐỦ nằm lớp dưới cùng (người dùng 2026-11-11: "chân con gốc đâu bị móp một bên... để nó làm layer dưới là
    # được"): phần lộ ra trên concept bị viền hàm khoét lõm mép trái, vá thêm thì vẫn móp. Dùng lại hình vây gần (lật ngang, thu
    # 0,86), đặt cho ba móng trùng chỗ ba móng vây xa của concept; lúc nghỉ nửa trái của nó nấp sau cằm.
    bxg = CD.hop(m_vg, 3)
    al_g = CD.mem_alpha(m_vg)
    rg = np.dstack([np.clip(a[bxg[1]:bxg[3], bxg[0]:bxg[2]], 0, 255).astype(np.uint8),
                    (np.clip(al_g[bxg[1]:bxg[3], bxg[0]:bxg[2]], 0, 1) * 255).astype(np.uint8)])
    imx = Image.fromarray(rg, "RGBA").transpose(Image.FLIP_LEFT_RIGHT)
    tlx = c.get("vay_x_ti", 0.86)
    imx = imx.resize((round(imx.width * tlx), round(imx.height * tlx * c.get("vay_x_dep", 0.72))), Image.LANCZOS)
    x0x = int(round(c["ban_x"][0] - imx.width / 2))
    y0x = bxg[3] - imx.height
    imx.save(os.path.join(ra, "vay_x.png"))
    manh["vay_x"] = [x0x, y0x, x0x + imx.width, y0x + imx.height]
    luu("vay_duoi", img_vd, m_vd_day)
    luu("duoi", sau, m_dd)
    luu("hong", img_hong, hong)
    luu("vom", img_vom, m_vom)
    luu("ham_duoi", sau, m_duoi)
    luu("ham_tren", sau, m_tren)
    for ten, q in ten_nanh:
        luu(ten, a, q["mk"])
        p0, p1 = truc_chinh(q["m"])
        mui, goc = (p0, p1) if np.hypot(*(p0 - Mc)) < np.hypot(*(p1 - Mc)) else (p1, p0)
        info["nanh"][ten] = {"goc": [float(v) for v in goc], "mui": [float(v) for v in mui], "tam": list(q["c"])}
    luu("vay_g", a, m_vg)

    # mép miệng theo từng cột (để chia trọng số vách họng): đỉnh và đáy của vùng miệng (vòm họng + sàn miệng) trong bản đồ G
    mieng = than_day & np.isin(G, [I["man"], I["sanho"]]) & ~muc_sau
    mieng = CD.lap_lo(CD.gian(mieng, 3))
    cot = np.nonzero(mieng.any(0))[0]
    y_top = np.array([np.argmax(mieng[:, x]) for x in cot], float)
    y_bot = np.array([Hh - 1 - np.argmax(mieng[::-1, x]) for x in cot], float)
    info["mieng"] = {"x": [int(v) for v in cot[::4]], "tren": [float(v) for v in y_top[::4]], "duoi": [float(v) for v in y_bot[::4]]}
    info["manh"] = manh
    json.dump(info, open(os.path.join(ra, "manh.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    np.savez_compressed(os.path.join(ra, "mat_na.npz"), G=G, than_day=than_day, mieng=mieng, m_tren=m_tren, m_duoi=m_duoi, m_dd=m_dd,
                        m_vg=m_vg, m_vx=m_vx_day, hong=hong, m_vd=m_vd_day)

    # ---------- soi: bản đồ nhãn, tờ mảnh, ghép lại so concept
    PAL = {"trang": (255, 255, 255), "muc": (0, 0, 0), "lam": (40, 80, 160), "nhat": (80, 190, 230), "bang": (210, 240, 250),
           "man": (150, 30, 90), "sanho": (240, 90, 120), "kem": (250, 235, 170), "da": (60, 60, 60), "xam": (140, 140, 150)}
    vis = np.zeros((Hh, Wd, 3), np.uint8)
    for t in TEN:
        vis[L == I[t]] = PAL[t]
    Image.fromarray(vis).save(os.path.join(ra, "_nhan.png"))
    visG = np.zeros((Hh, Wd, 3), np.uint8) + 150
    for t in ("lam", "nhat", "bang", "man", "sanho"):
        visG[than_day & (G == I[t])] = PAL[t]
    visG[muc_sau & than_day] = (0, 0, 0)
    Image.fromarray(visG).save(os.path.join(ra, "_nhan_sau.png"))

    thu_tu = ["vay_x", "vay_duoi", "duoi", "hong", "vom", "ham_duoi", "ham_tren"] + [t for t, _ in ten_nanh if t[0] == "d"][::-1] \
        + [t for t, _ in ten_nanh if t[0] == "t"][::-1] + ["vay_g"]
    info["thu_tu"] = thu_tu
    json.dump(info, open(os.path.join(ra, "manh.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ghep = Image.new("RGBA", (Wd, Hh), (0, 0, 0, 0))
    for t in thu_tu:
        im = Image.open(os.path.join(ra, t + ".png"))
        ghep.alpha_composite(im, (manh[t][0], manh[t][1]))
    g = np.array(ghep)
    thieu = int((fig & (g[..., 3] < 110)).sum())
    thua = int((bg & (g[..., 3] > 110) & ~CD.gian(fig, 2)).sum())
    lech = np.abs(g[..., :3].astype(int) - a.astype(int)).max(2)
    khac = int(((lech > 40) & fig & (g[..., 3] > 200)).sum())
    out = Image.new("RGB", (Wd, Hh), GRAY)
    out.paste(ghep, (0, 0), ghep)
    out.save(os.path.join(ra, "_ghep.png"))
    print(f"  ghép lại so concept: concept có mà ghép trống {thieu} px, ghép thừa ra ngoài {thua} px, lệch màu > 40: {khac} px")

    # tờ mảnh trên nền xám
    f = ImageFont.truetype(FONT, 15)
    ims = [(t, Image.open(os.path.join(ra, t + ".png"))) for t in thu_tu]
    cw = max(im.width for _, im in ims) + 20
    hang, x, y, hh, cells = [], 10, 10, 0, []
    Wt = 2200
    for t, im in ims:
        if x + im.width + 20 > Wt:
            x, y, hh = 10, y + hh + 34, 0
        cells.append((t, im, x, y))
        x += im.width + 24
        hh = max(hh, im.height)
    tot = Image.new("RGB", (Wt, y + hh + 40), GRAY)
    d = ImageDraw.Draw(tot)
    for t, im, x, y in cells:
        tot.paste(im, (x, y + 18), im)
        d.text((x, y), f"{t} {im.width}x{im.height}", fill=(255, 255, 255), font=f)
    tot.save(os.path.join(ra, "_soi.png"))
    print("  ->", ra)


# ================================================================ rig
SC = 0.5                      # pixel concept -> pixel rig
OX = {1: 800.0, 2: 800.0}     # trục giữa con (pixel concept): gốc rig ở mặt đất dưới điểm này
CHAM = {1: 1.0, 2: 1.1}       # dạng 2 nặng hơn: mọi clip chậm lại chừng này


def _quai():
    from quai import anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat
    return anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat


def ss(x, a, b):
    u = np.clip((np.asarray(x, float) - a) / (b - a), 0.0, 1.0)
    return u * u * (3 - 2 * u)


def dung(k, ti=1.0, thua=1.0):
    """dựng rig dạng k: trả (sk, info). ti < 1, thua > 1: bản nhẹ (ảnh nhỏ, lưới thưa) để gộp vào dạng trước cho clip evolve."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    Dat = khung.Dat
    c = CFG[k]
    dm = os.path.join(d_inbox(k), "manh")
    mj = json.load(open(os.path.join(dm, "manh.json"), encoding="utf-8"))
    ox, dat_y = OX[k], float(c["dat"])
    sc = SC * ti

    def R(x, y=None):
        if y is None:
            x, y = x
        return ((x - ox) * sc, (dat_y - y) * sc)

    def Rs(pts):
        return np.array([R(p) for p in pts], float)

    def C_(V):
        V = np.asarray(V, float)
        return np.stack([ox + V[:, 0] / sc, dat_y - V[:, 1] / sc], 1)

    def nap(ten):
        im = Image.open(os.path.join(dm, ten + ".png")).convert("RGBA")
        im = im.resize((max(2, round(im.width * sc)), max(2, round(im.height * sc))), Image.LANCZOS)
        return anh.loang_mau(im)

    def dat_cua(ten):
        b = mj["manh"][ten]
        return Dat(*R((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))

    sk = khung.Sk(f"{CODE}_{k}")
    thu_tu = mj["thu_tu"]
    for t in thu_tu:
        sk.anh(t, nap(t))
    Hb = np.array(c["ban_le"], float)
    Ft, Fd, Mc = np.array(c["mui_tren"], float), np.array(c["mui_duoi"], float), np.array(c["tam_mieng"], float)
    top_y = min(mj["manh"][t][1] for t in ("ham_tren", "duoi"))
    H = (dat_y - top_y) * sc

    def goc_dai(p0, p1):
        a, b = np.array(R(p0)), np.array(R(p1))
        return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])), float(np.hypot(*(b - a)))

    # ---------------- xương
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("than", "move", *R(c["than"]), the_gioi=True)
    g, d = goc_dai(Hb, Ft)
    sk.xuong("ham_tren", "than", *R(Hb), goc=g, dai=d, the_gioi=True)
    g, d = goc_dai(Hb, Fd)
    sk.xuong("ham_duoi", "than", *R(Hb), goc=g, dai=d, the_gioi=True)
    sk.xuong("mieng", "than", *R(Mc), goc=0, dai=40, the_gioi=True)
    # trục miệng: từ khoé sau (sát bản lề) tới khoé trước. Hai mép môi là hai cung ở hai bên trục; NGẬM = hai cung khép về trục.
    ax0, ax1 = np.array(c["mep_tren"][0], float), np.array(c["mep_tren"][-1], float)
    axl = float(np.hypot(*(ax1 - ax0)))
    axn = (ax1 - ax0) / axl
    nor = np.array([axn[1], -axn[0]])                                         # pháp tuyến chĩa LÊN (pixel concept, y xuống)

    def ud(Pc):
        r = np.asarray(Pc, float) - ax0
        return (r @ axn) / axl, r @ nor                                       # u dọc trục 0..1, d > 0: phía trên trục

    def cung(pts, dau):
        u, d = ud(pts)
        o = np.argsort(u)
        return u[o], np.maximum(dau * d[o], 0.0)
    cu_t, cd_t = cung(c["mep_tren"], 1.0)
    cu_d, cd_d = cung(c["mep_duoi"], -1.0)
    D_t, D_d = float(cd_t.max()), float(cd_d.max())                           # mép môi cách trục xa nhất bao nhiêu (px concept)

    def dang(u):
        return np.sin(np.pi * np.clip((np.asarray(u, float) - 0.03) / 0.94, 0.0, 1.0)) ** 0.8    # 0 ở hai khoé, 1 ở giữa miệng

    NGOAI = {}                                                                # viền ngoài của từng hàm theo u (đo trên lưới hàm)

    def do_ngoai(Pc, tren):
        u, d = ud(Pc)
        d = d if tren else -d
        o = np.linspace(-0.1, 1.15, 26)
        mx = np.zeros(len(o) - 1)
        for i in range(len(o) - 1):
            m = (u >= o[i]) & (u < o[i + 1])
            mx[i] = d[m].max() if m.any() else 0.0
        for i in range(1, len(mx)):                                           # ô trống lấy ô kề
            if mx[i] <= 0:
                mx[i] = mx[i - 1]
        mx = np.convolve(np.pad(mx, 1, mode="edge"), [0.25, 0.5, 0.25], mode="valid")
        NGOAI[tren] = ((o[:-1] + o[1:]) / 2, mx)

    def w_moi(Pc, tren):
        """phần đi theo xương môi của một điểm: 1 ở mép môi giữa miệng; giảm dần về 0 ở trục miệng (lòng miệng co lại), ở hai khoé
        và ở VIỀN NGOÀI của hàm (viền ngoài đứng yên, da hàm giãn ra: đầu giữ nguyên khối, vách họng phía sau không lòi ra)."""
        u, d = ud(Pc)
        d = d if tren else -d
        dl = np.maximum(np.interp(u, cu_t if tren else cu_d, cd_t if tren else cd_d), 1.0)
        dn = np.interp(u, *NGOAI[tren])
        g = np.where(d <= dl, np.clip(d / dl, 0.0, 1.0), np.clip((dn - d) / np.maximum(dn - dl, 6.0), 0.0, 1.0))
        return dang(u) * g
    it, id_ = int(np.argmax(cd_t)), int(np.argmax(cd_d))
    pt_t = ax0 + axn * cu_t[it] * axl + nor * cd_t[it]
    pt_d = ax0 + axn * cu_d[id_] * axl - nor * cd_d[id_]
    sk.xuong("moi_t", "ham_tren", *R(pt_t), the_gioi=True)                    # môi trên (chỉ dời: khép xuống trục miệng)
    sk.xuong("moi_d", "ham_duoi", *R(pt_d), the_gioi=True)                    # môi dưới
    nanh = []
    for ten, q in mj["nanh"].items():
        goc, mui = np.array(q["goc"]), np.array(q["mui"])
        truc = goc + 0.22 * (mui - goc)                                       # khớp xoay ở gần gốc nanh
        g, d = goc_dai(truc, mui)
        cha = "ham_tren" if ten[0] == "t" else "ham_duoi"
        sk.xuong("x_" + ten, cha, *R(truc), goc=g, dai=d, the_gioi=True)
        ra_ngoai = math.degrees(math.atan2(-(truc[1] - Mc[1]), truc[0] - Mc[0]))    # hướng từ tâm miệng ra gốc nanh (rig: y lên)
        xoe = (ra_ngoai - g + 180) % 360 - 180
        nanh.append({"ten": ten, "xuong": "x_" + ten, "tren": ten[0] == "t", "xoe": xoe, "dai": d,
                     "moi": float(dang(ud(truc[None])[0][0]))})                # nanh đi theo môi bao nhiêu (theo chỗ gốc nanh dọc miệng)
    Jt0 = Rs(c["duoi_khop"])
    # chia lại đường khớp thành nhiều đốt đều nhau (người dùng 2026-11-11: chia phần vây / đuôi thật kĩ): đuôi uốn tròn, không gãy khúc
    n_dot = int(c.get("so_dot_duoi", 2 * (len(Jt0) - 1)))
    cum0 = np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(Jt0, axis=0).T))])
    sj = np.linspace(0.0, cum0[-1], n_dot + 1)
    Jt = np.stack([np.interp(sj, cum0, Jt0[:, 0]), np.interp(sj, cum0, Jt0[:, 1])], 1)
    duoi = sk.chuoi("duoi", "than", Jt)
    vk = c["vay_duoi_khop"]
    g, d = goc_dai(vk["goc"], vk["tren"])
    sk.xuong("vd_t", duoi[-1], *R(vk["goc"]), goc=g, dai=d, the_gioi=True)
    g, d = goc_dai(vk["goc"], vk["duoi"])
    sk.xuong("vd_d", duoi[-1], *R(vk["goc"]), goc=g, dai=d, the_gioi=True)
    sk.xuong("ban_g", "move", *R(c["ban_g"]), the_gioi=True)
    sk.xuong("ban_x", "move", *R(c["ban_x"]), the_gioi=True)
    bvx = mj["manh"]["vay_x"]
    sk.xuong("vai_x", "move", *R(c["ban_x"][0], bvx[1] + 0.22 * (bvx[3] - bvx[1])), the_gioi=True)   # khớp vai của vây xa (clip đặt)

    # ---------------- slot (sau -> trước), đúng thứ tự cắt
    bone_of = {"vay_x": "than", "vay_duoi": duoi[-1], "duoi": "than", "hong": "than", "vom": "than", "ham_duoi": "than",
               "ham_tren": "than", "vay_g": "than"}
    for t in thu_tu:
        sk.slot(t, bone_of.get(t, "x_" + t), t)

    MAU = {"duoi": 0.55, "vay_duoi": 0.55, "vay_g": 0.55, "vay_x": 0.55}       # vây, đuôi: bước lưới còn 55 % (dày gấp ~3 lần số đỉnh)

    def luoi_cua(ten, **kw):
        return luoi.luoi_vung(sk.images[ten], buoc_theo_cao=H * thua * MAU.get(ten, 1.0), ten=f"{ten} {k}", **kw)

    def dinh(ten, L):
        dt = dat_cua(ten)
        return dt, C_(dt.ra(L.pts, *sk.images[ten].size))

    # trường trọng số của hai hàm: 0 ở bản lề, 1 từ khoảng một phần tư hàm trở ra (bản lề mềm, không hở)
    def doc(P, F):
        v = F - Hb
        return ((P - Hb) @ v) / float(v @ v)

    def f_ham(P, F, tren=None):
        """phần đi theo xương hàm: 0 ở bản lề, lên 1 dọc theo hàm. Sát mép môi thì lên nhanh (hết một phần tư hàm: nanh và môi bám
        chắc); càng ra viền ngoài (lưng, bụng) vùng chuyển càng rộng (tới 70 % hàm) để lưng UỐN ĐỀU khi há to, không gãy khúc ở
        giữa thân (người dùng báo trên dạng 1, 2026-11-11)."""
        u_ = doc(P, F)
        if tren is None or tren not in NGOAI:
            return ss(u_, 0.03, 0.27)
        uu, d = ud(P)
        d = d if tren else -d
        dl = np.maximum(np.interp(uu, cu_t if tren else cu_d, cd_t if tren else cd_d), 1.0)
        dn = np.interp(uu, *NGOAI[tren])
        t_ = np.clip((d - dl) / np.maximum(dn - dl, 6.0), 0.0, 1.0)
        a0, a1 = 0.03 - 0.12 * t_, 0.27 + 0.43 * t_
        x = np.clip((u_ - a0) / (a1 - a0), 0.0, 1.0)
        return x * x * (3 - 2 * x)

    ho = {}
    # ================= HÀM TRÊN, HÀM DƯỚI =================
    for ten, F, xg, xm, tr in (("ham_tren", Ft, "ham_tren", "moi_t", True), ("ham_duoi", Fd, "ham_duoi", "moi_d", False),
                               ("vom", Ft, "ham_tren", "moi_t", True)):
        L = luoi_cua(ten)
        dt, P = dinh(ten, L)
        if ten != "vom":
            do_ngoai(P, tr)
        w = f_ham(P, F, tr)
        wl = w_moi(P, tr)
        sk.luoi_gan(ten, ten, L, trongso.chuan([{xm: float(l_), xg: float((1 - l_) * v), "than": float((1 - l_) * (1 - v))}
                                                for v, l_ in zip(w, wl)]), dat=dt)
        ho[ten] = L.ho

    # ================= VÁCH HỌNG: căng giữa hai hàm (mép trên theo hàm trên, mép dưới theo hàm dưới) =================
    L = luoi_cua("hong")
    dt, P = dinh("hong", L)
    mx = np.array(mj["mieng"]["x"], float)
    yt = np.interp(P[:, 0], mx, np.array(mj["mieng"]["tren"], float))
    yb = np.interp(P[:, 0], mx, np.array(mj["mieng"]["duoi"], float))
    s_ = np.clip((yb - P[:, 1]) / np.maximum(yb - yt, 1.0), 0.0, 1.0)
    wt, wd = s_ * f_ham(P, Ft, True), (1 - s_) * f_ham(P, Fd, False)
    sk.luoi_gan("hong", "hong", L, trongso.chuan([{"ham_tren": float(a_), "ham_duoi": float(b_), "than": float(max(0.0, 1 - a_ - b_))}
                                                  for a_, b_ in zip(wt, wd)]), dat=dt)
    ho["hong"] = L.ho

    # ================= MÔNG + ĐUÔI: chuỗi B-spline, phía trước khớp gốc bám thân =================
    L = luoi_cua("duoi")
    dt = dat_cua("duoi")
    V = dt.ra(L.pts, *sk.images["duoi"].size)
    s_d, cum_d = trongso._chieu_len_gay(V, Jt)
    W_ch = trongso.chuoi(s_d, np.diff(cum_d), duoi, cha="than", cha_hoa=1.0)
    truoc = ss(V[:, 0], Jt[0][0] - 10 * sc, Jt[0][0] + 70 * sc)              # càng về phía đầu càng bám thân
    # đoạn lưng mà mảnh này nằm dưới vòm hàm trên: phải uốn Y HỆT vòm (cùng trường bản lề f_ham), không thì há miệng là hai mảnh
    # lệch nhau, lưng nhìn như hai lớp chồng lên nhau (người dùng báo 2026-11-11)
    w_vom = f_ham(C_(V), Ft, True)
    W = []
    for i in range(L.n):
        d_ = {b: (1 - truoc[i]) * w for b, w in W_ch[i].items()}
        d_["than"] = d_.get("than", 0.0) + float(truoc[i])
        d_ = {b: (1 - float(w_vom[i])) * w for b, w in d_.items()}
        d_["ham_tren"] = float(w_vom[i])
        W.append(d_)
    sk.luoi_gan("duoi", "duoi", L, trongso.chuan(W), dat=dt)
    ho["duoi"] = L.ho

    # ================= VÂY ĐUÔI ĐÁ: hai thuỳ, mỗi thuỳ một xương, chỗ nối hoà =================
    L = luoi_cua("vay_duoi")
    dt, P = dinh("vay_duoi", L)
    gy = np.array(vk["goc"], float)
    wt_ = ss(gy[1] - P[:, 1], -16, 16)                                        # trên khe chữ V: thuỳ trên
    gan = 1 - ss(np.hypot(P[:, 0] - gy[0], P[:, 1] - gy[1]), 14, 60)          # sát chỗ nối: theo đốt đuôi cuối
    sk.luoi_gan("vay_duoi", "vay_duoi", L, trongso.chuan([{"vd_t": float((1 - g_) * a_), "vd_d": float((1 - g_) * (1 - a_)),
                                                          duoi[-1]: float(g_)} for a_, g_ in zip(wt_, gan)]), dat=dt)
    ho["vay_duoi"] = L.ho

    # ================= HAI VÂY NGỰC: trên theo thân, đầu vây + móng bám đất =================
    #   vây gần: phần trên theo thân (gốc vây sát tâm thân nên thân nhổm lên nó không bị kéo dài).
    #   vây xa: phần trên theo khớp vai riêng `vai_x`, đầu vây theo `ban_x`; clip đặt hai xương này mỗi khung (hàm `theo`): cả vây trượt
    #   ngang theo cằm, vai đi lên theo hàm dưới khi hàm nhấc (vây nối liền với thân), hàm hạ xuống thì vai chỉ hạ tối đa 35 % chiều
    #   cao vây (không ép bẹp thành tấm dẹt), phần còn lại nấp sau hàm.
    for ten, ban, tren, u0, u1 in (("vay_g", "ban_g", "than", 0.20, 0.78), ("vay_x", "ban_x", "vai_x", 0.25, 0.72)):
        L = luoi_cua(ten)
        dt, P = dinh(ten, L)
        y_t, y_b = mj["manh"][ten][1], mj["manh"][ten][3]
        f = ss(P[:, 1], y_t + u0 * (y_b - y_t), y_t + u1 * (y_b - y_t))
        sk.luoi_gan(ten, ten, L, trongso.chuan([{ban: float(v), tren: float(1 - v)} for v in f]), dat=dt)
        ho[ten] = L.ho

    # ================= NANH: mảnh cứng, mỗi nanh một xương =================
    for q in nanh:
        sk.manh(q["ten"], q["ten"], dat_cua(q["ten"]), xuong=q["xuong"])

    tong = sum(len(a_["uvs"]) // 2 if "uvs" in a_ else 4 for s_ in sk.skin.values() for a_ in s_.values()) if hasattr(sk, "skin") else 0
    info = {"k": k, "ti": ti, "H": H, "duoi": duoi, "nanh": nanh, "ho": ho, "dinh": tong, "sc": sc,
            "do_cao_bung": (dat_y - max(p[1] for p in c["day_than"])) * sc, "cao_vay_x": (bvx[3] - bvx[1]) * sc,
            "moi_t": D_t * sc, "moi_d": D_d * sc, "ngam": c.get("ngam", 0.93), "truot": c.get("truot_nanh_d", 0.0) * sc}
    return sk, info


# ================================================================ clip
def clips(sk, info, k):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    Clip, cv = hoat.Clip, hoat.cv
    H, duoi, nanh = info["H"], info["duoi"], info["nanh"]
    F = 30.0 / CHAM[k]                                                        # khung thiết kế mỗi giây
    W0 = sk.the_gioi()
    slots = [s["name"] for s in sk.slots]
    ND = len(duoi)
    UD = np.linspace(0.0, 1.0, ND)                                            # vị trí từng đốt dọc đuôi 0..1
    KD = 5.0 / ND                                                             # bản gốc viết cho 5 đốt: chia lại cho ND đốt
    A_DUOI = (3.0 + 11.0 * UD) * KD
    BUNG = info["do_cao_bung"]                                                # bụng cách đất bao nhiêu (px rig)

    def sg(f, chu_ky, tre=0.0):
        """sóng sin theo khung, bằng 0 ở khung 0 (khung 0 idle là dáng gốc), trễ `tre` khung."""
        return math.sin(2 * math.pi * (f - tre) / chu_ky) + math.sin(2 * math.pi * tre / chu_ky)

    def ham(P, tren, duoi_):
        """hai hàm. tren > 0: hàm trên ngửa lên (há thêm, độ); duoi_ > 0: hàm dưới hạ xuống (há thêm, độ).
        Số ÂM là NGẬM: -26 (hàm trên) và -13 (hàm dưới) là ngậm hết. Miệng khép sẵn ở cả hai khoé nên không ngậm bằng xoay quanh
        bản lề được (mỏm hàm trên chọc xuyên hàm dưới), ép dẹt cả hàm thì miệng vẫn mở một nửa: ngậm = HAI MÉP MÔI KHÉP VỀ TRỤC MIỆNG
        như mí mắt (xương moi_t, moi_d; lòng miệng co lại, da hàm giãn theo), nanh đi theo môi nên hai hàng đan cài; hàm chỉ ép nhẹ
        và xoay nhẹ cho có lực."""
        for tr, v, xh, xm, D, r_, e_ in ((True, tren, "ham_tren", "moi_t", info["moi_t"], -5.0, 0.16),
                                         (False, duoi_, "ham_duoi", "moi_d", info["moi_d"], 3.0, 0.13)):
            if v >= 0:
                P.rot(xh, v if tr else -v)
                continue
            a_ = min(-v / (26.0 if tr else 13.0), 1.0)
            P.rot(xh, r_ * a_)
            P.scale(xh, 1, 1 - e_ * a_)
            dy = (-1 if tr else 1) * info["ngam"] * D * a_ / (1 - e_ * a_)    # trong hệ của xương hàm (đã ép): bù lại cho đủ quãng
            P.move(xm, 0, dy)
            for q in nanh:
                if q["tren"] == tr:
                    P.move(q["xuong"], 0.0 if tr else info["truot"] * a_, dy * q["moi"])

    def tho_(P, a):
        """thở: hai hàm phồng nhẹ ra (a = 0..1), không xoay, hai khoé miệng không tách (người dùng: idle hở mép miệng)."""
        P.scale("ham_tren", 1, 1 + 0.055 * a)
        P.scale("ham_duoi", 1, 1 + 0.045 * a)

    def xoe(P, a, rung=0.0):
        """nanh xoè ra ngoài như cánh hoa (a = 0..1), rung thêm vài độ."""
        for i, q in enumerate(nanh):
            P.rot(q["xuong"], 0.5 * q["xoe"] * a + rung * (1 if i % 2 else -1))

    def nanh_lac(P, a):
        """nanh nẩy nhẹ theo quán tính (độ): hàng trên và hàng dưới ngược chiều."""
        for q in nanh:
            P.rot(q["xuong"], a if q["tren"] else -a)

    def duoi_(P, cong, f=None, bien=1.0, vay=0.0):
        """đuôi: cong = góc cộng thêm mỗi đốt (dương: vểnh lên phía lưng); f: khung, thêm sóng quẫy trễ dần ra ngọn; vay: hai thuỳ xoè."""
        for i, b in enumerate(duoi):
            w = 0.0 if f is None else A_DUOI[i] * bien * sg(f, 60.0, 14.0 * UD[i])
            P.rot(b, -cong * (0.6 + 0.8 * UD[i]) * KD + w)                            # xương đuôi chĩa sang trái: xoay âm là vểnh lên
        P.rot("vd_t", -vay)
        P.rot("vd_d", vay)

    bv_ = sk.bones[sk.bi["vai_x"]]
    VAI_X = (bv_["x"], bv_["y"])                                              # khớp vai vây xa ở dáng gốc (hệ của move)
    CAO_VX = info["cao_vay_x"]

    def theo(P, ten, w=1.0, dx=0.0, dy=0.0, goc=0.0):
        """đầu vây (xương bám đất) đi theo thân với tỉ lệ w (1: dính cứng vào thân; 0: bám đất), cộng thêm dời / xoay.
        Vây xa (ban_x) còn có khớp vai vai_x: phần (1 − w) trượt ngang theo cằm (gốc vây trên hàm dưới) để vây luôn nằm ngay dưới
        cằm; vai lên theo hàm dưới khi hàm nhấc, hàm hạ thì vai chỉ hạ tối đa 35 % chiều cao vây (không ép bẹp)."""
        xa = ten == "ban_x"
        vdx, vdy, vg = dx, 0.0, 0.0
        W = sk.the_gioi(P) if (w > 0 or xa) else None
        if w > 0:
            T = np.linalg.inv(W["move"]) @ W["than"] @ np.linalg.inv(W0["than"]) @ W0["move"]
            b = sk.bones[sk.bi[ten]]
            p = T @ np.array([b["x"], b["y"], 1.0])
            ang = math.degrees(math.atan2(T[1, 0], T[0, 0]))
            dx += w * (p[0] - b["x"])
            dy += w * (p[1] - b["y"])
            goc += w * ang
            if xa:
                pv = T @ np.array([VAI_X[0], VAI_X[1], 1.0])
                vdx += w * (pv[0] - VAI_X[0])
                vdy += w * (pv[1] - VAI_X[1])
                vg += w * ang
        if xa and w < 1:
            q = np.linalg.inv(W["move"]) @ W["ham_duoi"] @ np.linalg.inv(W0["ham_duoi"]) @ W0["move"] @ np.array([VAI_X[0], VAI_X[1], 1.0])
            truot = (1 - w) * (q[0] - VAI_X[0])
            dx += truot
            vdx += truot
            vdy += (1 - w) * max(q[1] - VAI_X[1], -0.35 * CAO_VX)
        if dx or dy:
            P.move(ten, dx, dy)
        if goc:
            P.rot(ten, goc)
        if xa:
            if vdx or vdy:
                P.move("vai_x", vdx, vdy)
            if vg:
                P.rot("vai_x", vg)

    def an_het(P, a):
        for s_ in slots:
            P.alpha[s_] = a

    U = H / 322.0                                                             # mọi độ dời viết cho con cao 322 px rig

    # ---------------- idle: thân lắc + dời vòng, miệng mở thở nhẹ (người dùng dặn: không táp miệng nhanh), đuôi quẫy trễ dần
    def idle_fn(t, P):
        f = t * F
        P.move("than", 5 * U * sg(f, 60, 0), -4 * U * (1 - math.cos(2 * math.pi * f / 30)) / 2)
        P.rot("than", 2.2 * sg(f, 60, 6))
        tho = (1 - math.cos(2 * math.pi * f / 60)) / 2                                    # thở: miệng mở, hé thêm rồi về, một nhịp mỗi vòng
        tho_(P, tho)
        nanh_lac(P, 1.2 * sg(f, 60, 5))
        duoi_(P, 2.0 + 2.5 * sg(f, 60, 10) - 2.0 * math.cos(2 * math.pi * f / 60), f, 0.6, 5 * sg(f, 60, 20))
        theo(P, "ban_x", 0.0)

    # ---------------- attack: nhổm lùi há to -> lao tới sập hàm trong 2 khung -> nảy -> giữ ngậm -> về (theo skill_01 của con gốc)
    A_TRUNG = 17

    def attack_fn(t, P):
        f = t * F
        lao = cv(f, [(0, 0), (13, -0.10, "io"), (15, 0.2, "in"), (17, 0.55, "out"), (26, 0.5), (36, 0, "io")])
        P.move("move", lao * H, 0)
        mo_ = cv(f, [(0, 0), (3, 0.1), (13, 1, "out"), (15, 0.8), (17, -1, "in"), (19, -0.8), (26, -0.85), (36, 0, "io")])   # 1 há to, -1 sập
        tr = 30 * mo_ if mo_ > 0 else 26 * mo_
        du = 28 * mo_ if mo_ > 0 else 13 * mo_
        ham(P, tr, du)
        P.rot("than", cv(f, [(0, 0), (3, -3), (13, 17, "out"), (15, 6), (17, -15, "in"), (19, -8), (22, -10), (26, -5), (36, 0, "io")]))
        P.move("than", cv(f, [(0, 0), (13, -34, "out"), (16, 6), (17, 18), (19, 2), (26, 0), (36, 0)]) * U,
               cv(f, [(0, 0), (3, -8), (13, 20, "out"), (16, 2), (17, -16, "in"), (19, -8), (22, -12), (26, -4), (36, 0, "io")]) * U)
        nen = cv(f, [(0, 0), (16, 0), (17, 1), (20, -0.3), (24, 0)])                    # nén bẹp đúng khung cắn
        P.scale("than", 1 + 0.07 * nen, 1 - 0.07 * nen)
        nanh_lac(P, cv(f, [(0, 0), (13, -4), (17, 9), (19, -5), (22, 3), (26, 0)]))
        duoi_(P, cv(f, [(0, 0), (13, 5, "out"), (17, -16, "in"), (20, 14), (25, -5), (36, 0, "io")]), None, 0, cv(f, [(0, 0), (13, 8), (18, -10), (24, 5), (36, 0)]))
        nhac = cv(f, [(0, 0), (4, 1), (11, 0), (14, 0), (16, 1), (18, 0)])              # hai vây bước theo
        theo(P, "ban_x", 0.0, 0, 16 * U * nhac)
        theo(P, "ban_g", 0.0, 0, 10 * U * cv(f, [(0, 0), (2, 0), (6, 1), (12, 0), (15, 1), (17, 0)]))

    # ---------------- cast (chiêu mana; người dùng dặn 2026-11-11: XOAY NGƯỜI quật đuôi mạnh, không lộn ngược): lao tới, xoay người
    #   quay lưng lại (lật ngang cả con qua xương move, 5 khung), đuôi đang vểnh cao quật mạnh xuống đối thủ, giữ, xoay người lại, về
    C_TRUNG = 20

    def cast_fn(t, P):
        f = t * F
        lao = cv(f, [(0, 0), (6, -0.06, "io"), (13, 0.36, "io"), (27, 0.36), (40, 0, "io"), (46, 0)])
        P.move("move", lao * H, 0)
        sx = cv(f, [(0, 1), (11, 1), (16, -1, "io"), (27, -1), (32, 1, "io"), (46, 1)])                 # xoay người: 1 -> -1 -> 1
        if abs(sx) < 0.14:
            sx = 0.14 if sx >= 0 else -0.14
        P.scale("move", sx, 1)
        # các số dưới đây tính trong hệ của chính con vật (đuôi ở bên trái); lúc đã xoay người thì đuôi chĩa về phía đối thủ
        cong = cv(f, [(0, 0), (7, 8, "io"), (13, 24, "io"), (17, 36), (20, -11, "in"), (22, -6, "out"), (27, -8), (33, 7, "io"), (40, -2), (46, 0)])
        for i, b in enumerate(duoi):                                                                    # > 0 vểnh cao lấy đà; < 0 quật xuống
            P.rot(b, -cong * (0.7 + 0.6 * UD[i]) * KD)
        vay = cv(f, [(0, 0), (13, 10), (17, 14), (20, -14, "in"), (23, 8), (30, 0), (46, 0)])
        P.rot("vd_t", -vay)
        P.rot("vd_d", vay)
        P.rot("than", cv(f, [(0, 0), (7, -5), (13, -8), (17, -13), (20, 15, "in"), (22, 10, "out"), (27, 9), (33, 0, "io"), (46, 0)]))
        P.move("than", cv(f, [(0, 0), (13, 6), (17, 12), (20, -34, "in"), (22, -28), (27, -26), (33, 0, "io"), (46, 0)]) * U,
               cv(f, [(0, 0), (7, -8), (14, 10, "out"), (17, 8), (20, -8, "in"), (27, -3), (30, 8), (33, 0), (46, 0)]) * U)
        ngam = cv(f, [(0, 0), (7, 0.4), (13, 1, "io"), (27, 1), (36, 0, "io"), (46, 0)])                # mím miệng lúc xoay và quật
        ham(P, -15 * ngam, -7.5 * ngam)
        nen = cv(f, [(0, 0), (19, 0), (20, 1), (23, -0.3), (27, 0), (46, 0)])
        P.scale("than", 1 + 0.06 * nen, 1 - 0.06 * nen)
        nanh_lac(P, cv(f, [(0, 0), (20, 0), (21, 7), (24, -4), (28, 0), (46, 0)]))
        nhay = cv(f, [(0, 0), (11, 0), (14, 1, "out"), (17, 0, "in"), (27, 0), (30, 1, "out"), (33, 0, "in"), (46, 0)])   # nhún chân lúc xoay
        theo(P, "ban_g", 0.0, 0, 12 * U * nhay)
        theo(P, "ban_x", 0.0, 0, 9 * U * nhay)

    # ---------------- skill (chiêu cuối): rạp xuống ngậm miệng -> bật há cực đại, nanh xoè -> giữ rung tới hết luồng nước -> sập -> về
    K_PHUN = 12
    GIU = int(round(1.25 * F))                                                          # giữ há 1,25 giây thật
    K_HET = K_PHUN + GIU

    def skill_fn(t, P):
        f = t * F
        g = f - K_PHUN
        rung = hoat.rung(t, K_PHUN / F + 0.05, K_HET / F, moi=2) if K_PHUN < f < K_HET else 0.0
        mo_ = cv(f, [(0, 0), (3, -0.5), (10, -1, "out"), (K_PHUN, 1, "in"), (K_HET, 1), (K_HET + 4, -0.6, "in"), (K_HET + 12, 0, "io")])
        tr = (24 if mo_ > 0 else 26) * mo_ + 1.6 * rung
        du = (23 if mo_ > 0 else 12) * mo_ - 1.6 * rung
        ham(P, tr, du)
        xoe(P, max(0.0, cv(f, [(0, 0), (10, 0), (K_PHUN, 1, "in"), (K_HET, 1), (K_HET + 4, 0, "in")])), 2.0 * rung)
        P.rot("than", cv(f, [(0, 0), (3, -4), (10, -13, "out"), (K_PHUN, 9, "in"), (K_HET, 7), (K_HET + 4, -6), (K_HET + 12, 0, "io")]))
        P.move("than", cv(f, [(0, 0), (10, -26, "out"), (K_PHUN, 14, "in"), (K_HET, 8), (K_HET + 12, 0, "io")]) * U - 2.5 * U * rung,
               cv(f, [(0, 0), (3, -6), (10, -16, "out"), (K_PHUN, 26, "in"), (K_HET, 22), (K_HET + 4, -6), (K_HET + 12, 0, "io")]) * U + 3.5 * U * rung)
        phinh = cv(f, [(0, 0), (10, 1, "out"), (K_PHUN, -0.4), (K_PHUN + 4, 0)])       # nén phồng trước khi phun
        P.scale("than", 1 + 0.05 * phinh, 1 + 0.04 * phinh)
        duoi_(P, cv(f, [(0, 0), (10, -8, "out"), (K_PHUN, 18, "in"), (K_HET, 14), (K_HET + 12, 0, "io")]) + 2.5 * rung, None, 0,
              cv(f, [(0, 0), (K_PHUN, 12), (K_HET, 9), (K_HET + 10, 0)]) + 3 * rung)
        theo(P, "ban_g", 0.0, -8 * U * cv(f, [(0, 0), (10, 1), (K_PHUN, 0)]), 0)
        theo(P, "ban_x", 0.0)

    # ---------------- hit: bật ngửa, há miệng, vây xa nhấc khỏi đất
    def hit_fn(t, P):
        f = t * F
        a = cv(f, [(0, 0), (2, 1, "out"), (6, 0.85), (11, 0.25, "io"), (16, 0, "io")])
        P.rot("than", 17 * a)
        P.move("than", -22 * U * a, 12 * U * a)
        ham(P, 6 * a, 20 * a)
        nanh_lac(P, cv(f, [(0, 0), (2, -8), (5, 5), (9, -2), (16, 0)]))
        duoi_(P, cv(f, [(0, 0), (3, -14), (8, 9), (12, -3), (16, 0)]), None, 0, cv(f, [(0, 0), (3, 10), (9, -5), (16, 0)]))
        theo(P, "ban_x", 0.0, -6 * U * a, 34 * U * cv(f, [(0, 0), (3, 1, "out"), (8, 0.8), (13, 0, "in"), (16, 0)]))

    # ---------------- die: hất tung, lộn ngửa, rơi lưng xuống, nảy, giãy vây rồi nằm; tan ở cuối
    def die_fn(t, P):
        f = t * F
        P.rot("than", cv(f, [(0, 0), (3, 22, "out"), (8, 95), (13, 150), (15, 168, "in"), (17, 160), (20, 166), (44, 164)]))
        P.move("than", cv(f, [(0, 0), (8, -40), (15, -60), (44, -60)]) * U,
               cv(f, [(0, 0), (3, 90, "out"), (8, 150), (11, 130), (15, -6, "in"), (17, 12, "out"), (20, -2, "in"), (22, 2), (44, 0)]) * U + 0.10 * H * cv(f, [(0, 0), (15, 1), (44, 1)]))
        ham(P, cv(f, [(0, 0), (3, 4), (13, 10), (15, -18, "in"), (18, 14), (24, 4), (44, 8, "io")]), cv(f, [(0, 0), (3, 14), (13, 20), (15, -8, "in"), (18, 22), (26, 12), (44, 16, "io")]))
        nanh_lac(P, cv(f, [(0, 0), (15, 0), (16, 9), (19, -6), (23, 3), (28, 0)]))
        duoi_(P, cv(f, [(0, 0), (8, -18), (15, 12), (17, -22), (22, -8), (30, -14), (44, -12)]), None, 0, cv(f, [(0, 0), (15, 0), (17, 14), (24, 4), (44, 8)]))
        giay = cv(f, [(0, 0), (17, 0), (20, 1), (23, -0.7), (26, 0.5), (30, -0.3), (36, 0)])
        theo(P, "ban_g", 1.0, 0, 0, 16 * giay)
        theo(P, "ban_x", 1.0, 0, 0, -14 * giay)
        an_het(P, 1 - cv(f, [(0, 0), (38, 0), (44, 1)]))

    # ---------------- appear: rơi từ trên trời xuống, nện bụng xuống đất (sự kiện cham_dat: sân lắc cam), nằm bẹp, chống vây đứng dậy, lắc mình
    A_DAT = 8

    def appear_fn(t, P):
        f = t * F
        cao = cv(f, [(0, 1.0), (A_DAT, 0, "in"), (48, 0)])                                # rơi nhanh dần
        nam = cv(f, [(0, 1), (A_DAT, 1), (18, 1), (28, 0, "io"), (48, 0)])                 # 1: nằm bẹp bụng sát đất; 0: đứng trên vây
        nay = cv(f, [(0, 0), (A_DAT, 0), (A_DAT + 3, 1, "out"), (A_DAT + 6, 0, "in"), (48, 0)])
        day = cv(f, [(0, 0), (18, 0), (28, 1, "io"), (32, 0, "io"), (48, 0)])              # đẩy người lên quá đà rồi về
        P.move("than", cv(f, [(0, -14), (A_DAT, 0), (48, 0)]) * U, 1.25 * H * cao - (BUNG - 2) * nam + 14 * U * nay + 10 * U * day)
        lac = cv(f, [(0, 0), (30, 0), (33, 1), (36, -1), (39, 0.6), (42, -0.3), (45, 0)])  # lắc mình
        P.rot("than", cv(f, [(0, -24), (A_DAT - 1, -12), (A_DAT, 3, "in"), (A_DAT + 3, -4), (18, -5), (28, 5, "io"), (33, 0), (48, 0)]) + 4 * lac)
        bep = cv(f, [(0, -0.4), (A_DAT - 1, -0.6), (A_DAT, 1, "in"), (A_DAT + 4, 0.5), (18, 0.45), (27, -0.2, "io"), (33, 0)])
        P.scale("than", 1 + 0.11 * bep, 1 - 0.15 * bep)
        ham(P, cv(f, [(0, -10), (A_DAT - 1, -6), (A_DAT, -24, "in"), (A_DAT + 4, 6), (18, -4), (28, 0), (33, -10), (38, 0), (48, 0)]),
            cv(f, [(0, -6), (A_DAT, -12, "in"), (A_DAT + 4, 10), (18, 2), (28, 0), (33, -6), (38, 0), (48, 0)]))
        nanh_lac(P, cv(f, [(0, 0), (A_DAT, 0), (A_DAT + 1, 10), (A_DAT + 4, -6), (A_DAT + 8, 3), (20, 0), (33, 3), (37, -3), (42, 0)]))
        duoi_(P, cv(f, [(0, 26), (A_DAT, 20), (A_DAT + 3, -20, "in"), (A_DAT + 7, 6), (18, -6), (28, 4), (34, -3), (48, 0)]), None, 0,
              cv(f, [(0, 12), (A_DAT + 3, -12), (18, 0), (48, 0)]))
        # hai vây: lúc rơi dang ra theo thân; chạm đất thì xoạc ra hai bên; rồi thu về chống xuống đẩy người lên
        bam = cv(f, [(0, 1), (A_DAT - 1, 1), (A_DAT + 1, 0.0), (48, 0)])                   # 1: theo thân (đang rơi)
        xoac = cv(f, [(0, 1), (A_DAT, 1), (18, 1), (26, 0, "io"), (48, 0)])
        theo(P, "ban_g", bam, -16 * U * xoac, 0, 10 * xoac * (1 - bam))
        theo(P, "ban_x", bam, 8 * U * xoac, 0, -5 * xoac * (1 - bam))
        an_het(P, cv(f, [(0, 0), (2, 1), (48, 1)]))

    T_A, T_C, T_K = 36, 46, K_HET + 12
    return [Clip("appear", 48 / F, appear_fn, ev=[(A_DAT / F, "cham_dat", "")]),
            Clip("idle", 60 / F, idle_fn, loop=True),
            Clip("attack", T_A / F, attack_fn, ev=[(A_TRUNG / F, "trung", "")]),
            Clip("cast", T_C / F, cast_fn, ev=[(C_TRUNG / F, "trung", "")]),
            Clip("skill", T_K / F, skill_fn, ev=[(K_PHUN / F, "phun", ""), (K_HET / F, "het_phun", "")], trung=K_PHUN / F),
            Clip("hit", 16 / F, hit_fn),
            Clip("die", 44 / F, die_fn)]


def nuong_het(sk, cl):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    ve = soi.Ve(sk)
    for c in cl:
        if not c.loop and c.ten not in ("appear", "die", "evolve"):
            print(f"  vào {c.ten}: khung 0 lệch khung 0 idle {soi.lech(ve, fr['idle'][0], fr[c.ten][0])}; "
                  f"khung cuối lệch {soi.lech(ve, fr['idle'][0], fr[c.ten][-1])}")
    return fr


def so_concept(sk, fr, k, ra):
    """chồng khung 0 idle lên concept: ảnh so và IoU hình bóng."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    a = np.array(Image.open(concept(k)).convert("RGB")).astype(np.float32)
    bg = CD.nen_trang(a, 238)
    Hh, Wd = a.shape[:2]
    ox, dat_y = OX[k], float(CFG[k]["dat"])
    box = ((0 - ox) * SC, (dat_y - Hh) * SC, (Wd - ox) * SC, dat_y * SC)
    ve = soi.Ve(sk)
    im = ve.ve(fr["idle"][0], box, 1 / SC, bg=None, ss=1)
    r = np.array(im.resize((Wd, Hh), Image.LANCZOS))
    m_rig, m_con = r[..., 3] > 110, ~bg
    iou = float((m_rig & m_con).sum()) / max(1, int((m_rig | m_con).sum()))
    vis = np.zeros((Hh, Wd, 3), np.uint8) + 150
    vis[m_con & ~m_rig] = (230, 60, 60)
    vis[m_rig & ~m_con] = (60, 90, 230)
    ca = m_rig & m_con
    vis[ca] = (r[..., :3] * 0.5 + a * 0.5)[ca].astype(np.uint8)
    Image.fromarray(vis).save(ra)
    print(f"  so concept dạng {k}: IoU hình bóng {iou:.4f}; concept có mà rig thiếu {int((m_con & ~m_rig).sum())} px, rig thừa "
          f"{int((m_rig & ~m_con).sum())} px -> {ra}")
    return iou


def clK(cl):
    return next(c_ for c_ in cl if c_.ten == "skill")


def rig(k, tien_hoa=None):
    """dựng, nướng, xuất dạng k vào inbox/ca_voi_<k>/rig/. tien_hoa = (sk2, info2, fr2, cl2): gộp dạng sau cho clip evolve."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    sk, info = dung(k)
    cl = clips(sk, info, k)
    fr = nuong_het(sk, cl)
    ra = os.path.join(d_inbox(k), "rig")
    os.makedirs(ra, exist_ok=True)
    # điểm bắn tia cho game (game.muzzle): bộ xuất lấy xương miệng ở khung trúng của CAST, mà cast của con này là xoay người quật đuôi
    # (cả con đang lật ngang). Tia là của chiêu cuối: đặt xương `nha` (con của root, đứng yên) ở tâm miệng lúc đang há giữ chiêu cuối.
    i_giu = min(len(fr["skill"]) - 1, int(round(30 * (clK(cl).gio_trung() + 0.3))))
    pm_ = sk.the_gioi(fr["skill"][i_giu])["mieng"][:2, 2]
    sk.xuong("nha", "root", float(pm_[0]), float(pm_[1]), goc=0, dai=40, the_gioi=True)
    so_concept(sk, fr, k, os.path.join(ra, "so_concept.png"))
    ve = soi.Ve(sk)
    cao = soi.chieu_cao(ve, fr["idle"][0])
    ten = f"{CODE}_{k}"
    ch = CHAM[k]
    noi = {}
    M, clM, frM = sk, cl, fr
    if tien_hoa:
        sk2, info2, fr2, cl2 = tien_hoa
        h2 = soi.chieu_cao(soi.Ve(sk2), fr2["idle"][0])
        ti = cao / h2
        M = tienhoa.gop(sk, sk2)

        def gong(t, P):                                                       # dạng cũ: rạp xuống, ngậm miệng, rung, đuôi vểnh
            g = hoat.cv(t, [(0, 0), (0.3, -0.3), (0.6, 1, "out"), (1.3, 1.15)])
            r = hoat.rung(t, 0.45, 1.35, moi=1)
            P.rot("than", -8 * g + 0.8 * r)
            P.move("than", -6 * g, -5 * max(g, 0))
            a_ = 0.75 * max(g, 0)
            P.rot("ham_tren", -9 * a_ + 0.6 * r)
            P.scale("ham_tren", 1, 1 - 0.5 * a_)
            P.rot("ham_duoi", 5 * a_ - 0.6 * r)
            P.scale("ham_duoi", 1, 1 - 0.45 * a_)
            kd_ = 5.0 / len(info["duoi"])
            for i, b in enumerate(info["duoi"]):
                P.rot(b, (-6 * max(g, 0) + 1.5 * r * (1 if i % 2 else -1)) * kd_)

        def gam(t, P, fl):                                                    # dạng sau: chồm tới há to gầm, nanh xoè
            r = hoat.rung(t, 2.0, 2.4, moi=1)
            P.rot("n_ham_tren", 22 * fl + 1.5 * r * fl)
            P.rot("n_ham_duoi", -26 * fl - 1.5 * r * fl)
            for i, q in enumerate(info2["nanh"]):
                P.rot("n_" + q["xuong"], 0.4 * q["xoe"] * fl)
            P.rot("n_than", 7 * fl)
            n2_ = len(info2["duoi"])
            for i, b in enumerate(info2["duoi"]):
                P.rot("n_" + b, -(4 + 8 * i / max(1, n2_ - 1)) * (5.0 / n2_) * fl * (0.6 + 0.4 * r * (1 if i % 2 else -1)))

        ev = tienhoa.clip_tien_hoa(M, sk, sk2, fr2["idle"][0], tiB=ti, fnA=gong, fnB=gam, mem=[])
        clM = cl + [ev]
        frM = dict(fr)
        frM["evolve"] = hoat.nuong(M, ev)
        _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, fr2["idle"][0], ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
        print("  evolve:", noi["evolve"])
    Hh = info["H"]
    tk = xuat.xuat_het(M, clM, ra, ten, f"Cá voi biến dị dạng {k}", frames=frM, dang=k, so_dang=2, dung_yen=("skill",), lao=("cast",), mieng="nha",
                       cao=cao, khop_idle=0, ma_goc=3281, noi_them=noi,
                       can=[("can_can", "attack", 17 / 30.0 * ch, "mieng", 0.6 * Hh),
                            ("can_ha_to", "skill", 20 / 30.0 * ch, "mieng", 0.75 * Hh),
                            ("can_quat_duoi", "cast", 20 / 30.0 * ch, "than", 1.0 * Hh),
                            ("can_nam_bep", "appear", 14 / 30.0 * ch, "than", 0.9 * Hh),
                            ("can_chet", "die", 30 / 30.0 * ch, "than", 0.9 * Hh)])
    print(f"dạng {k}: hở {info['ho']}; cao {cao:.0f} px rig; .atomik {tk['atomik_kb']:.0f} KB -> {ra}")
    return sk, info, fr, cl


if __name__ == "__main__":
    arg = sys.argv[1:]
    if arg[:1] == ["cat"]:
        for kk in ([int(arg[1])] if len(arg) > 1 else [1, 2]):
            cat(kk)
    elif arg[:1] == ["rig"]:
        rig(int(arg[1]))
    elif arg[:1] == ["xem"]:                                                  # xem <k> <clip> <khung,khung> <x> <y> <bán kính> (toạ độ rig)
        anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
        kk = int(arg[1])
        sk_, info_ = dung(kk)
        cl_ = {c_.ten: c_ for c_ in clips(sk_, info_, kk)}
        fr_ = hoat.nuong(sk_, cl_[arg[2]])
        ve_ = soi.Ve(sk_)
        for i_ in [int(v) for v in arg[3].split(",")]:
            ra_ = os.path.join(d_inbox(kk), "rig", f"xem_{arg[2]}_{i_}.png")
            soi.anh_can(ve_, fr_[min(i_, len(fr_) - 1)], (float(arg[4]), float(arg[5])), float(arg[6]), ra_, phong=int(arg[7]) if len(arg) > 7 else 2, luoi=False)
            print(ra_)
    elif arg[:1] == ["all"]:
        rig(2)
        sk2, info2 = dung(2, ti=0.6, thua=1.8)                                # bản nhẹ của dạng 2 gộp vào dạng 1
        cl2 = clips(sk2, info2, 2)
        rig(1, tien_hoa=(sk2, info2, nuong_het(sk2, cl2), cl2))
    else:
        print(__doc__)
