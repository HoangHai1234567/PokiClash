# -*- coding: utf-8 -*-
"""Dòng pháp sư nước bí ẩn (mã tạm `phap_su`, tướng thứ 6 đảo Thủy, 2026-11-11): cắt lớp từ concept đã duyệt, dựng rig, clip.

    py -3 -I ArtGen/Spine/phap_su.py cat 1|2      cắt concept dạng k -> inbox/phap_su_<k>/manh/ (+ manh.json, _soi.png, _nhan.png)
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/phap_su.py rig 1|2    dựng rig một dạng -> inbox/phap_su_<k>/rig/
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/phap_su.py all        dạng 2, rồi dạng 1 gộp bản nhẹ của dạng 2 (clip evolve)

Rig thẳng từ concept, không tờ mảnh (skill pokiclash-spine-rig mục 22): mỗi món đồ là một lớp cắt từ concept theo vùng khép kín
bởi nét mực; phần bị che tô lại bằng vân sáp lát cùng màu. Lớp (sau -> trước): áo choàng (cả tấm), tay áo cầm gậy (tay xa), gậy +
bàn tay, giày, áo dài, vạt trước, tay áo buông (tay gần), khoảng tối dưới mũ, khăn vai, mũ, dải đai mũ.
Toạ độ trong CFG là pixel concept (1536 x 1024, y xuống). Ghi chú thiết kế, mổ xẻ con gốc: inbox/phap_su_ghichu.md.
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "phap_su"
GRAY = (150, 150, 150)
FONT = "C:/Windows/Fonts/arial.ttf"
MUC_RGB = (48, 26, 10)
DAY = 12                       # nét mực (px concept) + dư: mực cách vùng màu của lớp trong khoảng này thì thuộc lớp đó

# màu chuẩn để phân lớp pixel (đo trên concept)
MAU_K = {
    1: {"trang": (254, 254, 254), "muc": (38, 17, 3), "cham": (59, 66, 155), "bang": (199, 237, 246), "ngoc": (63, 169, 183),
        "toi": (17, 21, 62), "cam": (246, 134, 92), "go": (176, 130, 100), "nuoc": (143, 215, 235)},
    2: {"trang": (254, 254, 254), "muc": (38, 16, 5), "cham": (52, 54, 165), "bang": (197, 239, 249), "ngoc": (36, 155, 169),
        "toi": (28, 32, 83), "cam": (253, 129, 91), "go": (184, 137, 111), "nuoc": (154, 225, 245)},
}
TEN = list(MAU_K[1])
LOP0 = ["choang", "tay_p", "gay", "ban", "giay", "ao", "vat", "tay_t", "toi", "khan", "mu", "dai"]       # lớp cắt theo hạt giống vùng
LOP = ["choang", "tay_p", "gay", "day1", "day2", "ban", "giay", "ao", "vat", "tay_t", "toi", "khan", "mu", "dai"]   # thứ tự vẽ sau -> trước
MAU_LOP = {"choang": (90, 60, 200), "tay_p": (0, 170, 170), "gay": (170, 110, 60), "ban": (255, 0, 0), "giay": (60, 60, 60), "ao": (40, 200, 120),
           "vat": (240, 240, 120), "tay_t": (0, 110, 230), "toi": (20, 20, 90), "khan": (250, 170, 210), "mu": (150, 40, 160),
           "dai": (255, 120, 40)}

# ---------------------------------------------------------------- số đọc trên ảnh kẻ lưới (pixel concept)
CFG = {
    1: {
        "dat": 978,                                   # mặt đất (đáy mũi giày, chân gậy)
        # hạt giống vùng: điểm nằm trong vùng màu của lớp (vùng = mảng liền không mực chứa điểm đó)
        "hat": {
            "choang": [(400, 760), (330, 860), (290, 880), (470, 700), (492, 650), (360, 830), (440, 880)],
            "tay_p": [(940, 690), (1010, 670), (1040, 690)],
            "giay": [(731, 954), (871, 947)],
            "ao": [(700, 780), (560, 890), (900, 850), (680, 700)],
            "vat": [(830, 690), (805, 760)],
            "tay_t": [(560, 720), (520, 780), (510, 830)],
            "toi": [(790, 500)],
            "khan": [(700, 600)],
            "mu": [(600, 200), (700, 330), (800, 430), (420, 255), (862, 325), (420, 560), (640, 480), (990, 470),
                   (560, 520), (904, 334)],
            "dai": [(400, 365), (380, 460)],
            "gay": [(1160, 180), (1160, 470), (1225, 400), (1080, 300)], "ban": [(1075, 610)],
        },
        "x_gay": 1052,                                # mọi thứ bên phải cột này (trừ tay áo) là gậy
        # mũ: khớp đầu (cổ), gốc mũ, chuỗi chóp (gốc -> hạt cam), vành trái / phải (gốc -> mép), dải đai (nút -> đuôi)
        "co": (740, 585), "mu_goc": (700, 440),
        "chop": [(625, 235), (592, 135), (522, 96), (462, 140), (428, 212)], "hat_cam": (412, 256),
        "vanh_t": [(560, 520), (460, 560), (365, 585)], "vanh_p": [(900, 445), (975, 455), (1040, 468)],
        "dai_tren": [(515, 378), (445, 384), (375, 370), (305, 368)], "dai_duoi": [(505, 422), (425, 443), (345, 463), (288, 505)],
        # thân: hông (gốc áo), ngực (dưới khăn vai)
        "hong": (735, 860), "nguc": (735, 640),
        "gau_t": [(610, 740), (575, 800), (540, 850), (510, 900)], "gau_p": [(905, 740), (935, 800), (960, 850), (985, 900)],   # gấu áo: mép trái, phải
        "vat_goc": (808, 632),
        "vat_t": [(748, 625), (745, 685), (743, 745), (746, 805), (790, 872)], "vat_p": [(868, 625), (870, 685), (872, 745), (868, 805), (816, 872)],
        "khan_t": [(600, 612), (505, 628)], "khan_p": [(880, 600), (952, 612)],
        "choang_goc": (545, 625),
        "choang_t": [(500, 635), (455, 685), (410, 735), (365, 785), (320, 835), (275, 885)],             # mép ngoài (trái)
        "choang_p": [(592, 640), (588, 690), (578, 740), (565, 790), (548, 840), (525, 895)],             # ranh với áo (từ đây sang phải là phần khuất)
        "choang_them": [(470, 600), (600, 598), (680, 640), (700, 760), (690, 835), (600, 885), (500, 902), (430, 870), (430, 740)],   # phần khuất của tấm áo choàng
        "choang_khuat": [(600, 598), (680, 640), (700, 760), (690, 835), (600, 885), (500, 900)],         # mép khuất (phải, gấu): kẻ nét mực
        # tay gần (buông): vai, khuỷu, cổ tay; gấu ống tay
        "tay_t": [(592, 645), (566, 715), (540, 780), (512, 845)],
        "ao_duoi_tay": [(545, 640), (530, 720), (512, 800), (505, 880), (640, 880), (650, 640)],          # phần áo khuất sau tay gần
        # tay xa (cầm gậy): vai, khuỷu, cổ tay; bàn tay; gấu ống tay
        "tay_p": [(915, 615), (965, 650), (1077, 610)], "ong_p": [(1010, 665), (1014, 710), (1016, 755)],
        "nach": [(940, 606), (898, 694)], "nach_hoa": 85,          # đường nách (mép khăn vai -> mép áo) và bề rộng dải chuyển sang xương tay
        "tay_p_them": [(958, 612), (925, 592), (892, 588), (872, 612), (874, 652), (900, 694), (945, 650)],   # viền phần khuất ở vai (kẻ mực) + một điểm trong ống tay
        # gậy: chân gậy, đầu gậy (trên cùng), tâm cầu nước; hai dây treo (nút -> hạt)
        "gay_duoi_tay": [(1066, 556), (1104, 556), (1091, 668), (1055, 668)],
        "gay_chan": (1058, 969), "gay_dinh": (1150, 75), "cau": (1162, 180), "cau_r": 52,
        "day_x": 1128, "day_y": 297,
        "day1": [(1182, 292), (1178, 360), (1172, 430), (1170, 478)], "day2": [(1190, 292), (1212, 340), (1232, 385), (1240, 420)],
        "giay": [(731, 954), (871, 947)],
    },
    2: {
        "dat": 995,
        "hat": {
            "choang": [(480, 700), (400, 820), (330, 868), (420, 893), (500, 900)],
            "tay_p": [(880, 500), (942, 470), (962, 520)],
            "giay": [(680, 975), (835, 972)],
            "ao": [(700, 600), (600, 800), (640, 915), (700, 950), (880, 800), (850, 600)],
            "vat": [(770, 560), (776, 668)],
            "tay_t": [(625, 560), (600, 640), (610, 685)],
            "toi": [(780, 300)],
            "khan": [(700, 420), (722, 345), (812, 345)],
            "mu": [(600, 120), (700, 250), (797, 182), (475, 218), (640, 200), (620, 330)],
            "dai": [(420, 310), (420, 440)],
            "gay": [(1050, 150), (995, 700), (1100, 42)], "ban": [(1000, 440)],
        },
        "x_gay": 985,
        "co": (775, 385), "mu_goc": (700, 255),
        "chop": [(660, 140), (640, 52), (580, 45), (522, 100), (490, 182)], "hat_cam": (475, 218),
        "vanh_t": [(650, 300), (592, 335), (545, 350)], "vanh_p": [(840, 240), (892, 256), (932, 272)],
        "dai_tren": [(580, 255), (500, 290), (420, 312), (350, 348)], "dai_duoi": [(575, 272), (500, 340), (440, 410), (395, 480)],
        "hong": (770, 800), "nguc": (775, 450),
        "gau_t": [(585, 760), (565, 830), (548, 890), (530, 945)], "gau_p": [(880, 760), (905, 830), (925, 890), (940, 945)],
        "vat_goc": (790, 445),
        "vat_t": [(725, 440), (722, 540), (722, 640), (726, 740), (775, 850)], "vat_p": [(815, 440), (830, 540), (840, 640), (835, 740), (790, 850)],
        "khan_t": [(690, 425), (590, 440)], "khan_p": [(860, 415), (900, 425)],
        "choang_goc": (610, 450),
        "choang_t": [(600, 455), (540, 535), (480, 615), (420, 695), (360, 770), (305, 845)],
        "choang_p": [(640, 465), (620, 550), (600, 635), (580, 720), (562, 805), (545, 895)],
        "choang_them": [(560, 440), (700, 440), (760, 500), (770, 700), (740, 850), (640, 900), (545, 905), (540, 700)],
        "choang_khuat": [(700, 440), (760, 500), (770, 700), (740, 850), (640, 900), (545, 905)],
        "choang_vien": 9,                                                     # nửa bề rộng dải viền cam ở gấu áo choàng (px)
        "tay_t": [(650, 455), (635, 540), (620, 620), (605, 690)],
        "ao_duoi_tay": [(625, 455), (608, 540), (590, 640), (573, 722), (562, 760), (700, 760), (700, 455)],
        "tay_p": [(900, 430), (925, 470), (1000, 440)], "ong_p": [(950, 490), (955, 535), (955, 575)],
        "nach": [(905, 428), (850, 500)], "nach_hoa": 70,
        "tay_p_them": [(903, 430), (880, 418), (858, 422), (846, 445), (846, 475), (852, 498), (900, 480)],
        "gay_duoi_tay": [(985, 398), (1018, 398), (1016, 484), (982, 484)],
        "gay_chan": (1000, 986), "gay_dinh": (1090, 30), "cau": (1050, 150), "cau_r": 60,
        "day_x": 1025, "day_y": 246,
        "day1": [(1072, 240), (1066, 300), (1068, 345), (1082, 395)], "day2": [(1086, 240), (1096, 270), (1106, 300), (1112, 325)],
        "giay": [(680, 975), (835, 972)],
    },
}


def d_inbox(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}")


def concept(k):
    return os.path.join(d_inbox(k), "tai_ve", "L1_duyet.png")


# ---------------------------------------------------------------- công cụ mặt nạ
def moi_nhat(thu_muc, goc):
    """ảnh mới nhất của một bước: V01.png, V01_2.png, V01_3.png... (None nếu chưa có)."""
    best, bn = None, -1
    if not os.path.isdir(thu_muc):
        return None
    for f in os.listdir(thu_muc):
        n, e = os.path.splitext(f)
        if e.lower() != ".png" or not (n == goc or n.startswith(goc + "_")):
            continue
        sx = n[len(goc) + 1:]
        i = int(sx) if sx.isdigit() else (1 if n == goc else -1)
        if i > bn:
            best, bn = os.path.join(thu_muc, f), i
    return best


def nen_trang(a, nguong=236):
    w = (a.min(2) >= nguong).astype(np.uint8)
    n, lab = cv2.connectedComponents(w, connectivity=4)
    mep = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    mep = mep[mep != 0]
    return np.isin(lab, mep) & (w > 0)


def cum(mask, min_dt=300):
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8)
    out = []
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] >= min_dt:
            x, y, w, h, dt = st[i]
            out.append({"m": lab == i, "x0": int(x), "y0": int(y), "x1": int(x + w), "y1": int(y + h), "dt": int(dt)})
    return out


def lap_lo(m):
    pad = np.pad((~m).astype(np.uint8), 1, constant_values=1)
    n, lab = cv2.connectedComponents(pad, connectivity=4)
    return m | ((pad[1:-1, 1:-1] > 0) & (lab[1:-1, 1:-1] != lab[0, 0]))


def _k(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def gian(m, r):
    return cv2.dilate(m.astype(np.uint8), _k(r)) > 0 if r > 0 else m.copy()


def co(m, r):
    return cv2.erode(m.astype(np.uint8), _k(r)) > 0 if r > 0 else m.copy()


def da_giac(shape, pts):
    m = np.zeros(shape[:2], np.uint8)
    cv2.fillPoly(m, [np.round(np.array(pts, float)).astype(np.int32)], 1)
    return m > 0


def hop(m, le=3):
    ys, xs = np.nonzero(m)
    return [max(0, int(xs.min()) - le), max(0, int(ys.min()) - le), min(m.shape[1], int(xs.max()) + 1 + le),
            min(m.shape[0], int(ys.max()) + 1 + le)]


def kc(m):
    """khoảng cách (px) từ mọi pixel tới mặt nạ m."""
    if not m.any():
        return np.full(m.shape, 1e6, np.float32)
    return cv2.distanceTransform((~m).astype(np.uint8), cv2.DIST_L2, 5)


def mem_alpha(m, trong=2, sigma=0.7):
    return np.where(co(m, trong), 1.0, cv2.GaussianBlur(m.astype(np.float32), (0, 0), sigma))


def luu(a, alpha, box, path):
    x0, y0, x1, y1 = box
    rgba = np.dstack([np.clip(a[y0:y1, x0:x1], 0, 255).astype(np.uint8), (np.clip(alpha[y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8)])
    Image.fromarray(rgba, "RGBA").save(path)


def phan_lop(a, mau):
    """nhãn màu từng pixel (chỉ số trong TEN): gần màu chuẩn nào nhất trên ảnh làm mờ nhẹ, rồi lọc đa số 5x5."""
    b = cv2.GaussianBlur(a.astype(np.float32), (0, 0), 1.3)
    C = np.array([mau[t] for t in TEN], np.float32)
    d = ((b[:, :, None, :] - C[None, None]) ** 2).sum(3)
    # mép mực pha với màu sáng ra nâu xám: chỉ nhận màu lam (chàm, tối) khi thật sự ngả lam; gỗ chỉ khi ngả đỏ rõ và đủ sáng
    khong_lam = (b[..., 2] - b[..., 0]) < 30
    for t in ("cham", "toi", "ngoc"):
        d[..., TEN.index(t)][khong_lam] = 1e12
    khong_go = ((b[..., 0] - b[..., 2]) < 40) | (b.sum(2) < 250)
    d[..., TEN.index("go")][khong_go] = 1e12
    lab = d.argmin(2).astype(np.uint8)
    return cv2.medianBlur(lab, 5)


def o_van(a, sach, co_o=96, chong=20):
    """ô vân sáp lát liền được: lấy ô vuông sạch lớn nhất trong mặt nạ `sach`, hoà chéo hai mép để lát không lộ đường nối."""
    dt = cv2.distanceTransform(sach.astype(np.uint8), cv2.DIST_C, 3)
    y, x = np.unravel_index(int(dt.argmax()), dt.shape)
    r = int(dt[y, x]) - 1
    p = min(co_o + chong, 2 * r)
    if p < 24:
        raise SystemExit("không tìm được ô vân sạch đủ lớn")
    t = a[y - p // 2:y - p // 2 + p, x - p // 2:x - p // 2 + p].astype(np.float32).copy()
    o = min(chong, p // 4)
    n = p - o
    w = np.linspace(0, 1, o, dtype=np.float32)
    out = t[:n, :n].copy()
    out[:, :o] = t[:n, :o] * w[None, :, None] + t[:n, n:n + o] * (1 - w[None, :, None])
    top = t[:o, :n].copy()
    top[:, :o] = t[:o, :o] * w[None, :, None] + t[:o, n:n + o] * (1 - w[None, :, None])
    bot = t[n:n + o, :n].copy()
    bot[:, :o] = t[n:n + o, :o] * w[None, :, None] + t[n:n + o, n:n + o] * (1 - w[None, :, None])
    out[:o] = top * w[:, None, None] + bot * (1 - w[:, None, None])
    return out


def lat(shape, o):
    h, w = shape[:2]
    n = o.shape[0]
    return np.tile(o, (h // n + 1, w // n + 1, 1))[:h, :w]


def to_lai(a, vung, van, mem=0.0):
    """tô lại vùng bằng tấm vân đã lát, mép hoà `mem` px."""
    m = cv2.GaussianBlur(vung.astype(np.float32), (0, 0), mem)[..., None] if mem > 0 else vung.astype(np.float32)[..., None]
    m = np.maximum(m, vung[..., None].astype(np.float32))
    return a * (1 - m) + van * m


def net_muc(a, pts, day=9.0, kin=False):
    """kẻ nét mực qua các điểm (đường cong trơn Catmull-Rom), dày `day` px, hơi rung như bút: trả ảnh mới và mặt nạ nét."""
    P = np.array(pts, float)
    if len(P) > 2:
        Q = []
        ext = np.vstack([P[-2] if kin else 2 * P[0] - P[1], P, P[1] if kin else 2 * P[-1] - P[-2]])
        for i in range(1, len(ext) - 2):
            p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
            for u in np.linspace(0, 1, 12, endpoint=False):
                Q.append(0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3))
        Q.append(P[-1])
        P = np.array(Q)
    m = np.zeros(a.shape[:2], np.uint8)
    cv2.polylines(m, [np.round(P * 8).astype(np.int32)], False, 255, int(round(day)), cv2.LINE_AA, shift=3)
    mf = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 0.8)[..., None]
    rng = np.random.default_rng(7)
    nhieu = cv2.GaussianBlur(rng.normal(0, 1, a.shape[:2]).astype(np.float32), (0, 0), 1.5)[..., None] * 14
    col = np.array(MUC_RGB, np.float32)[None, None] + nhieu
    return a * (1 - mf) + col * mf, m > 100


def vien_cua(m):
    """đường viền ngoài của mặt nạ (danh sách điểm, pixel)."""
    cnts, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return max(cnts, key=len)[:, 0, :].astype(float)


# ---------------------------------------------------------------- cắt lớp
def cat(k):
    c = CFG[k]
    src = concept(k)
    if not os.path.exists(src):
        raise SystemExit("chưa có " + src)
    a = np.array(Image.open(src).convert("RGB")).astype(np.float32)
    H, Wd = a.shape[:2]
    xs = np.arange(Wd)[None, :].repeat(H, 0)
    ys = np.arange(H)[:, None].repeat(Wd, 1)
    bg = nen_trang(a)
    # giấy trắng khép kín bên trong hình (lòng móc gậy quanh cầu nước, khe hẹp): cũng là nền
    for q in cum((a.min(2) >= 240) & ~bg, 150):
        bg |= q["m"]
    fg = ~bg
    L = phan_lop(a, MAU_K[k])
    L[bg] = TEN.index("trang")
    ix = {t: i for i, t in enumerate(TEN)}
    muc = (L == ix["muc"]) & fg
    ra = os.path.join(d_inbox(k), "manh")
    os.makedirs(ra, exist_ok=True)

    # ---- vùng: mảng liền không mực (nét mực là tường)
    n, lab = cv2.connectedComponents((fg & ~muc).astype(np.uint8), connectivity=4)
    dt = np.bincount(lab.ravel(), minlength=n)
    lop_cua = np.full(n, -1, int)                                             # vùng -> chỉ số lớp
    for li, ten in enumerate(LOP0):
        for (x, y) in c["hat"][ten]:
            v = lab[y, x]
            if v == 0:
                print(f"  ! hạt giống {ten} ({x}, {y}) rơi vào mực / nền")
                continue
            if lop_cua[v] not in (-1, li):
                print(f"  ! vùng chứa ({x}, {y}) đã thuộc {LOP0[lop_cua[v]]}, hạt giống {ten} trùng vùng (nét mực hở?)")
            lop_cua[v] = li
    # vùng bên phải cột x_gay (đầu gậy, hạt treo...) là gậy
    cx = np.zeros(n)
    np.add.at(cx, lab.ravel(), xs.ravel())
    cy = np.zeros(n)
    np.add.at(cy, lab.ravel(), ys.ravel())
    cx, cy = cx / np.maximum(dt, 1), cy / np.maximum(dt, 1)
    for v in range(1, n):
        if lop_cua[v] == -1 and cx[v] > c["x_gay"]:
            lop_cua[v] = LOP0.index("gay")
    # vùng chưa gán: nhỏ thì theo lớp của vùng lớn gần nhất; lớn thì báo
    da_gan = lop_cua[lab] >= 0
    _, gan_nhat = cv2.distanceTransformWithLabels((~da_gan).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    # ánh xạ nhãn pixel gần nhất -> lớp
    yy0, xx0 = np.nonzero(da_gan)
    lop_px = np.zeros(gan_nhat.max() + 1, int)
    lop_px[gan_nhat[yy0, xx0]] = lop_cua[lab[yy0, xx0]]
    lop_gan = lop_px[gan_nhat]                                                # lớp của vùng đã gán gần nhất, cho mọi pixel
    for v in range(1, n):
        if lop_cua[v] == -1:
            m = lab == v
            cand = np.bincount(lop_gan[m], minlength=len(LOP0))
            lop_cua[v] = int(cand.argmax())
            if dt[v] > 250:
                print(f"  ? vùng chưa có hạt giống: tâm ({cx[v]:.0f}, {cy[v]:.0f}), {dt[v]} px, màu {TEN[np.bincount(L[m]).argmax()]} -> tạm cho "
                      f"{LOP0[lop_cua[v]]}")
    R = {ten: (lop_cua[lab] == li) & fg & ~muc for li, ten in enumerate(LOP0)}  # vùng màu của từng lớp (không mực)
    D = {ten: kc(R[ten]) for ten in LOP0}
    gan = np.argmin(np.stack([D[t] for t in LOP0]), 0)
    # mặt nạ lớp = vùng màu + mực trong khoảng DAY (nét chung thuộc cả hai lớp) + mực xa mọi vùng thì theo vùng gần nhất (dây treo)
    M = {ten: R[ten] | (muc & ((D[ten] <= 9.5) | (gan == li))) for li, ten in enumerate(LOP0)}
    for ten in LOP0:
        lo = lap_lo(M[ten]) & ~M[ten] & fg                                    # vệt sáng nhỏ lọt trong lớp
        for q in cum(lo, 1):
            if q["dt"] < 400:
                M[ten] |= q["m"]

    # ảnh nhãn để soi
    vis = np.full((H, Wd, 3), 255, np.uint8)
    for ten in LOP0:
        vis[R[ten]] = MAU_LOP[ten]
    vis[muc] = (30, 20, 10)
    Image.fromarray(vis).save(os.path.join(ra, "_nhan.png"))
    palc = np.array([(255, 255, 255), (40, 20, 5), (70, 70, 190), (200, 235, 245), (60, 170, 185), (10, 10, 60), (250, 130, 90),
                     (175, 130, 100), (140, 215, 235)], np.uint8)
    Image.fromarray(palc[L]).save(os.path.join(ra, "_mau.png"))

    # ---- vân sáp từng màu
    def van(ten_mau, r=5):
        return lat(a.shape, o_van(a, co((L == ix[ten_mau]) & fg, r)))

    van_cham, van_ngoc, van_bang, van_toi = van("cham"), van("ngoc"), van("bang"), van("toi", 3)

    info = {"concept": os.path.basename(src), "cỡ": [Wd, H], "manh": {}}
    anh_lop, mat_na = {}, {}

    def them_lop(ten, them, van_, net=(), day=9):
        """lớp `ten` = phần thấy trong concept + phần khuất `them` (lát vân); nét mực chung với lớp phía trước nằm giữa phần thấy
        và phần khuất thì tô lại (lớp phía trước vẫn giữ nét đó); `net`: các đường kẻ thêm nét mực, chỉ vẽ trong phần khuất."""
        them = them & ~M[ten]
        truoc = [t_ for t_ in LOP0[LOP0.index(ten) + 1:]]                      # chỉ nét chung với lớp vẽ SAU (nằm trước) mới bỏ
        d_truoc = np.min(np.stack([D[t_] for t_ in truoc]), 0) if truoc else np.full(bg.shape, 1e6, np.float32)
        chung = muc & M[ten] & gian(them, DAY + 2) & (d_truoc <= DAY) & (kc(bg) > DAY + 1)
        t = to_lai(a.copy(), gian(them | chung, 2) & fg, van_)                # nới 2 px: mép mờ của nét mực cũ không để lại vệt nối
        m = M[ten] | them
        cho = gian(them, 2) & ~R[ten] | chung
        for pts in net:
            t2, nm = net_muc(t, pts, day=day)
            t = np.where((nm & cho)[..., None], t2, t)
        anh_lop[ten], mat_na[ten] = t, m

    # ================= ÁO CHOÀNG: cả tấm, phần khuất sau áo và tay áo lát vân chàm =================
    g_, p_, q_ = c["choang_goc"], c["choang_p"], c["choang_khuat"]
    them = da_giac(a.shape, c["choang_them"]) & fg
    them = co(gian(them | M["choang"], 3), 3) & fg
    them_lop("choang", them, van_cham, net=[q_])
    if c.get("choang_vien"):
        # gấu phần khuất: kéo dài đường viền cam của gấu (dải rộng `choang_vien` px dọc mép gấu khuất) + nét mực mép trong
        cam_c = (L == ix["cam"]) & fg & M["choang"]
        mau_cam = np.median(a[co(cam_c, 2)], 0) if co(cam_c, 2).any() else np.array(MAU_K[k]["cam"], np.float32)
        day_g = [pt for pt in q_ if pt[1] > c["hong"][1]]                     # đoạn gấu (dưới hông) của mép khuất
        if len(day_g) >= 2:
            rv = float(c["choang_vien"])
            dai = np.zeros(a.shape[:2], np.uint8)
            cv2.polylines(dai, [np.array(day_g, np.int32)], False, 1, int(2 * rv))
            dai = (dai > 0) & (mat_na["choang"] & ~M["choang"])               # chỉ trong phần khuất vừa thêm
            rng = np.random.default_rng(5)
            tam = np.ones_like(a) * mau_cam[None, None] + cv2.GaussianBlur(rng.normal(0, 1, a.shape[:2]).astype(np.float32), (0, 0), 1.2)[..., None] * 10
            t = np.where(dai[..., None], tam, anh_lop["choang"])
            mep = vien_cua(co(mat_na["choang"], int(rv)))                     # mép trong của dải: viền của tấm co vào rv px
            gan_dai = gian(dai, 3)
            mep = np.array([q for q in mep[::5] if gan_dai[int(q[1]), int(q[0])]])
            if len(mep) >= 3:
                mep = mep[np.argsort(mep[:, 0])]
                t2, nm = net_muc(t, mep.tolist(), day=8)
                t = np.where((nm & gian(dai, 4) & mat_na["choang"] & ~M["choang"])[..., None], t2, t)
            t2, nm = net_muc(t, day_g, day=9)
            t = np.where((nm & gian(dai, 3) & ~M["choang"])[..., None], t2, t)
            anh_lop["choang"] = t

    # ================= TAY ÁO XA (cầm gậy): mọc thêm dưới khăn vai =================
    dg_ = da_giac(a.shape, c["tay_p_them"])
    them = dg_ & (M["khan"] | M["mu"] | M["ao"] | M["tay_p"])
    them = co(gian(them, 6), 6) & dg_ & fg                                    # làm mượt mép phần khuất (không lởm chởm theo mép các lớp che)
    them_lop("tay_p", them, van_ngoc, net=[c["tay_p_them"][:-1]])
    # cổ tay áo: khép kín phần bị gậy, bàn tay che (bao lồi của vành lam băng + lòng tối), tô lam băng, kẻ viền mực
    co_tay = R["tay_p"] & ((L == ix["bang"]) | (L == ix["toi"]))
    co_tay = lap_lo(co_tay | (muc & (kc(co_tay) <= 9.5) & M["tay_p"]))
    pts = cv2.convexHull(np.argwhere(co_tay)[:, ::-1].astype(np.int32))
    bao = np.zeros(a.shape[:2], np.uint8)
    cv2.fillConvexPoly(bao, pts, 1)
    bao = bao > 0
    moi = bao & ~mat_na["tay_p"] & (M["gay"] | M["ban"])                      # chỉ phần đang khuất sau gậy, bàn tay
    if moi.any():
        t = to_lai(anh_lop["tay_p"], gian(moi, 2) & bao & ~R["tay_p"], van_bang)
        vien = vien_cua(co(bao, 4))
        t2, nm = net_muc(t, vien[::6].tolist() + [vien[0].tolist()], day=9)
        cho = gian(moi, 1) & bao                                              # viền chỉ kẻ trên phần vừa tô (không thò ra nền)
        anh_lop["tay_p"] = np.where((nm & cho)[..., None], t2, t)
        mat_na["tay_p"] = mat_na["tay_p"] | moi | (nm & cho)

    # ================= GẬY: thân gậy chạy suốt dưới bàn tay (bàn tay là lớp riêng phía trước; lúc chết gậy rời tay) =================
    van_go = lat(a.shape, o_van(a, co((L == ix["go"]) & fg, 3), co_o=40, chong=8))
    gp = c["gay_duoi_tay"]                                                    # [trái trên, phải trên, phải dưới, trái dưới] theo tim nét mực
    than_gay = da_giac(a.shape, gp)
    t = to_lai(a.copy(), than_gay & ~R["gay"], van_go)
    for pts in ([gp[0], gp[3]], [gp[1], gp[2]]):
        t, nm = net_muc(t, pts, day=9)
        than_gay |= nm
    m = (M["gay"] & ~gian(M["ban"], 2)) | than_gay                            # trong vùng bàn tay chỉ còn thân gậy kẻ lại
    m &= ~(muc & (D["tay_p"] < D["gay"]) & ~than_gay)                         # mẩu nét của ống tay áo dính sang
    # hai dây treo hạt: hai lớp riêng (dây mềm có trọng lực), cắt khỏi lớp gậy theo ô (x > day_x, y > day_y), chia theo dây gần hơn
    go_ = (L == ix["go"]) & fg
    than_go = cv2.morphologyEx(go_.astype(np.uint8), cv2.MORPH_CLOSE, _k(4)) > 0
    tg = np.zeros_like(fg)                                                    # thân gậy = mọi cụm gỗ, trừ hạt cườm nhỏ màu gỗ nằm trên dây (dưới nút buộc)
    for q in cum(than_go, 1):
        if q["dt"] >= 320 or q["y0"] < c["day_y"] + 25 or q["x1"] < c["day_x"]:
            tg |= q["m"]
    than_go = tg
    than_go = than_go | (muc & (kc(than_go) <= 9.5))
    vung_day = m & (xs > c["day_x"]) & (ys > c["day_y"]) & ~than_go
    cam_ = (L == ix["cam"]) & fg
    giu = np.zeros_like(fg)
    for q in cum(vung_day, 1):                                                # chỉ giữ cụm có hạt cam (dây + hạt); mẩu mực rời trả về lớp gậy
        if (q["m"] & cam_).any() or q["dt"] >= 12:                          # hạt cườm nhỏ trên dây cũng thuộc dây; chỉ bỏ vụn vài pixel
            giu |= q["m"]
    vung_day = giu
    duong = []
    for key in ("day1", "day2"):
        mm = np.zeros(a.shape[:2], np.uint8)
        cv2.polylines(mm, [np.array(c[key], np.int32)], False, 1, 3)
        duong.append(kc(mm > 0))
    anh_lop["day1"], mat_na["day1"] = a.copy(), vung_day & (duong[0] <= duong[1])
    anh_lop["day2"], mat_na["day2"] = a.copy(), vung_day & (duong[0] > duong[1])
    anh_lop["gay"], mat_na["gay"] = t, m & ~vung_day

    # ================= BÀN TAY =================
    anh_lop["ban"], mat_na["ban"] = a.copy(), M["ban"]

    # ================= GIÀY: mọc thêm lên dưới gấu áo =================
    them = np.zeros_like(fg)
    for q in cum(R["giay"], 100):
        them |= (xs >= q["x0"] + 6) & (xs <= q["x1"] - 6) & (ys >= q["y0"] - 34) & (ys <= q["y0"] + 8)
    them_lop("giay", them & (M["ao"] | M["giay"]), van_toi)

    # ================= ÁO DÀI: phần khuất sau tay gần, vạt trước, khăn vai lát vân lam ngọc =================
    duoi_tay = da_giac(a.shape, c["ao_duoi_tay"]) & (M["tay_t"] | M["khan"])
    duoi_vat = lap_lo(M["vat"])
    y_nguc = c["nguc"][1] - 45
    duoi_khan = (M["khan"] | M["toi"]) & (ys > y_nguc) & (xs > c["ao_duoi_tay"][0][0]) & (xs < c["tay_p"][0][0] + 20)
    them = co(gian(duoi_tay | duoi_vat | duoi_khan, 2), 2) & fg
    # mẩu nét viền giày dính dưới gấu áo (gai nhỏ): mở hình học quanh giày
    gan_giay = gian(R["giay"], 18)
    M["ao"] = np.where(gan_giay, (cv2.morphologyEx(M["ao"].astype(np.uint8), cv2.MORPH_OPEN, _k(6)) > 0) | R["ao"], M["ao"])
    them_lop("ao", them, van_ngoc, net=[c["ao_duoi_tay"][:-2]])
    kin = (cv2.morphologyEx(mat_na["ao"].astype(np.uint8), cv2.MORPH_CLOSE, _k(9)) > 0) & fg & ~mat_na["ao"]
    kin &= gian(da_giac(a.shape, c["ao_duoi_tay"]), 12)                       # chỉ quanh mép khuất sau tay áo buông
    if kin.any():
        anh_lop["ao"] = to_lai(anh_lop["ao"], kin, van_ngoc)
        mat_na["ao"] = mat_na["ao"] | kin

    # ================= VẠT TRƯỚC: mọc thêm lên dưới khăn vai =================
    bx = hop(R["vat"], 0)
    xl, xr = c["vat_t"][0][0], c["vat_p"][0][0]
    them = (xs >= xl - 8) & (xs <= xr + 8) & (ys >= bx[1] - 50) & (ys <= bx[1] + 30) & (M["khan"] | M["vat"])
    them_lop("vat", them, van_bang, net=[[(xl - 4, bx[1] - 50), (xl - 4, bx[1] + 14)], [(xr + 4, bx[1] - 50), (xr + 4, bx[1] + 14)]])

    # ================= TAY ÁO GẦN (buông): mọc thêm lên dưới khăn vai =================
    j0 = c["tay_t"][0]
    them = da_giac(a.shape, [(j0[0] - 70, j0[1] - 50), (j0[0] + 75, j0[1] - 50), (j0[0] + 70, j0[1] + 30), (j0[0] - 90, j0[1] + 30)]) & M["khan"]
    them_lop("tay_t", them, van_ngoc)

    # ================= KHOẢNG TỐI dưới mũ: nới rộng dưới vành mũ và khăn vai =================
    them = gian(R["toi"], 42) & (M["mu"] | M["khan"]) & ~R["toi"]
    anh_lop["toi"] = to_lai(a.copy(), them | (M["toi"] & muc), van_toi)
    mat_na["toi"] = R["toi"] | them | (M["toi"] & muc & gian(R["toi"], 6))

    # ================= KHĂN VAI: mọc thêm lên dưới vành mũ =================
    them = gian(R["khan"], 30) & M["mu"] & (ys < c["co"][1] + 10) & ~gian(R["toi"], 2)
    them_lop("khan", them, van_bang)

    # ================= MŨ, DẢI ĐAI =================
    anh_lop["mu"], mat_na["mu"] = a.copy(), M["mu"]
    anh_lop["dai"], mat_na["dai"] = a.copy(), M["dai"]

    # ================= lưu =================
    for ten in LOP:
        m = mat_na[ten] & (fg | (ten in ()))
        box = hop(m)
        luu(anh_lop[ten], mem_alpha(m), box, os.path.join(ra, ten + ".png"))
        info["manh"][ten] = box
    # vòng tròn triệu hồi (lượt 2): nền trắng và mọi khoảng giấy trắng giữa các hình thành trong suốt
    fv = moi_nhat(os.path.join(d_inbox(1), "tai_ve"), "V01")
    if fv:
        v = np.array(Image.open(fv).convert("RGB")).astype(np.float32)
        trang = v.min(2) >= 232
        bgv = np.zeros_like(trang)
        for q in cum(trang, 120):
            bgv |= q["m"]
        al = mem_alpha(~bgv, trong=1, sigma=0.8)
        ysv, xsv = np.nonzero(~bgv)
        info["vong"] = {"anh": os.path.basename(fv), "tam": [float((xsv.min() + xsv.max()) / 2), float((ysv.min() + ysv.max()) / 2)],
                        "duong_kinh": float(xsv.max() - xsv.min())}
        luu(v, al, hop(~bgv), os.path.join(ra, "vong.png"))
    json.dump(info, open(os.path.join(ra, "manh.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    np.savez_compressed(os.path.join(ra, "mat_na.npz"), **{t_: mat_na[t_] for t_ in LOP}, **{"R_" + t_: R[t_] for t_ in LOP0}, muc=muc,
                        m_cam=(L == ix["cam"]) & fg, m_bang=(L == ix["bang"]) & fg, m_nuoc=(L == ix["nuoc"]) & fg, m_toi=(L == ix["toi"]) & fg, nen=bg)

    # ================= tờ soi =================
    def ghep(lech=None, chi=None):
        im = Image.new("RGBA", (Wd, H), GRAY + (255,))
        for ten in LOP:
            if chi and ten not in chi:
                continue
            p = Image.open(os.path.join(ra, ten + ".png"))
            x0, y0 = info["manh"][ten][:2]
            dx, dy = (lech or {}).get(ten, (0, 0))
            im.alpha_composite(p, (max(0, x0 + dx), max(0, y0 + dy)))
        return im

    t_ghep = ghep()
    t_goc = Image.new("RGBA", (Wd, H), GRAY + (255,))
    t_goc.alpha_composite(Image.fromarray(np.dstack([a.astype(np.uint8), np.where(bg, 0, 255).astype(np.uint8)]), "RGBA"))
    d = np.abs(np.array(t_ghep.convert("RGB")).astype(int) - np.array(t_goc.convert("RGB")).astype(int)).max(2)
    t_khac = Image.fromarray(np.dstack([np.clip(d * 4, 0, 255)] * 3).astype(np.uint8)).convert("RGBA")
    t_tach = ghep({"choang": (-70, 10), "tay_p": (40, -30), "gay": (110, 0), "day1": (130, 20), "day2": (150, 0), "ban": (50, 30), "giay": (0, 50), "vat": (20, 40), "tay_t": (-50, 40),
                   "toi": (0, 0), "khan": (0, -6), "mu": (0, -70), "dai": (-60, -80)})
    o = [(t_ghep, "1. ghép lại"), (t_goc, "2. concept"), (t_khac, "3. khác nhau giữa 1 và 2 (x4)"), (t_tach, "4. tách lệch các lớp"),
         (ghep(chi=("choang", "giay", "ao")), "5. áo choàng + giày + áo"), (ghep(chi=("tay_p", "toi", "khan", "vat", "tay_t")), "6. tay, khăn, vạt, khoảng tối")]
    to = Image.new("RGBA", (Wd // 2 * 3, H // 2 * 2), (60, 60, 60, 255))
    for i, (im, chu) in enumerate(o):
        sm = im.resize((Wd // 2, H // 2), Image.LANCZOS)
        ImageDraw.Draw(sm).text((12, 8), chu, fill=(255, 255, 255, 255), font=ImageFont.truetype(FONT, 20))
        to.alpha_composite(sm, ((i % 3) * (Wd // 2), (i // 3) * (H // 2)))
    to.convert("RGB").save(os.path.join(ra, "_soi.png"))
    # từng lớp riêng trên nền xám (soi phần tô lại)
    cols = 4
    rows = (len(LOP) + cols - 1) // cols
    tl = Image.new("RGBA", (Wd // 2 * cols, H // 2 * rows), (60, 60, 60, 255))
    for i, ten in enumerate(LOP):
        sm = ghep(chi=(ten,)).resize((Wd // 2, H // 2), Image.LANCZOS)
        ImageDraw.Draw(sm).text((12, 8), ten, fill=(255, 255, 255, 255), font=ImageFont.truetype(FONT, 22))
        tl.alpha_composite(sm, ((i % cols) * (Wd // 2), (i // cols) * (H // 2)))
    tl.convert("RGB").save(os.path.join(ra, "_soi_lop.png"))
    thieu = int(((np.array(t_ghep.convert("RGB")).astype(int) - np.array(GRAY)).__abs__().max(2) < 8)[~bg & ~gian(bg, 3)].sum())
    print(f"dạng {k}: " + ", ".join(f"{t_} {b[2] - b[0]}x{b[3] - b[1]}" for t_, b in info["manh"].items()))
    print(f"  pixel có hình trong concept mà ghép lại bị trống: {thieu}; khác concept tối đa {int(d.max())}, {int((d > 24).sum())} px lệch > 24"
          f" -> {os.path.join(ra, '_soi.png')}")


def Dmin_khac(D, ten):
    """khoảng cách tới vùng màu gần nhất của các lớp khác."""
    return np.min(np.stack([D[t] for t in D if t != ten]), 0)


# ================================================================ RIG (thư viện quai) ================================================================
# Cấu trúc học từ con gốc monster_3313 (ghi chú inbox/phap_su_ghichu.md mục 2), đổi cho hợp thiết kế của mình (áo chuông không chân):
#   root -> move (game dời) -> nhun (cả con: trồi lên lúc ra sân, bị hất)
#     -> hong (gốc áo: dời, nghiêng, nhún) -> gt0..2, gp0..2 (gấu áo: mép trái, mép phải)
#          -> nguc (dưới khăn vai) -> dau (cổ) -> mu -> chop0..3 (chóp mũ), vt0..1, vp0..1 (vành trái, phải), dt0..2, dd0..2 (hai dải đai)
#                -> ch0 -> ca0..4, cb0..4 (áo choàng: HAI chuỗi dọc mép ngoài và ranh với áo, như con gốc)
#                -> v0 -> va0..3, vb0..3 (vạt trước: hai chuỗi dọc hai mép)
#                -> kt0, kp0 (hai thuỳ khăn vai), tt0..2 (tay áo gần, buông)
#                -> tp0 (tay xa: một xương vai -> bàn tay, xoay và co giãn tới chỗ nắm gậy) -> op0..1 (gấu ống tay rủ)
#     -> ban (bàn tay) -> gay (gậy) -> cau (cầu nước), mieng (chỗ và hướng nhả cho VFX), da0..2, db0..2 (hai dây treo hạt)
#     -> giay_t, giay_p (hai mũi giày)
#   root -> goc_cat (mặt nạ cắt ở mặt đất: trồi lên lúc ra sân), vong -> vong_x (vòng tròn triệu hồi: elip nằm, xoay)
SC = 0.5                      # pixel concept -> pixel rig
OX = {1: 735.0, 2: 770.0}     # trục giữa con (pixel concept): gốc rig ở mặt đất dưới điểm này
CHAM = {1: 1.0, 2: 1.12}      # dạng 2 cao lớn, nặng hơn: mọi clip chậm lại chừng này
VONG_RONG = 1.0               # bề ngang vòng triệu hồi so với bề ngang cả con
VONG_DEP = 0.30               # elip: tỉ lệ dẹt của vòng tròn nằm trên đất


def _quai():
    sys.path.insert(0, HERE)
    from quai import anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat
    return anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat


def ss(x, a, b):
    """smoothstep 0..1 khi x đi từ a tới b (a > b thì ngược lại)."""
    u = np.clip((np.asarray(x, float) - a) / (b - a), 0.0, 1.0)
    return u * u * (3 - 2 * u)


def ln(f, keys):
    return float(np.interp(f, [q[0] for q in keys], [q[1] for q in keys]))


def _tron(*nguon):
    """trộn trọng số: _tron((k1, d1), (k2, d2)...) với d là dict {xương: w}."""
    out = {}
    for h, d in nguon:
        if h <= 1e-6:
            continue
        for b, w in d.items():
            out[b] = out.get(b, 0.0) + float(h) * float(w)
    return out


def kc_gay(P, J):
    """khoảng cách từ các điểm P (N, 2) tới đường gấp khúc J (K, 2)."""
    P, J = np.asarray(P, float), np.asarray(J, float)
    best = np.full(len(P), 1e9)
    for a, b in zip(J[:-1], J[1:]):
        d = b - a
        t = np.clip(((P - a) @ d) / max(1e-9, float(d @ d)), 0, 1)
        best = np.minimum(best, np.hypot(*(P - (a + t[:, None] * d)).T))
    return best


def x_tai_y(J, y):
    """hoành độ của đường gấp khúc J (đi từ trên xuống) tại tung độ y (ngoài hai đầu thì kéo dài theo đoạn đầu / cuối)."""
    J = np.asarray(J, float)
    yy, xx = J[:, 1], J[:, 0]
    out = np.interp(y, yy, xx)
    d0 = (xx[1] - xx[0]) / (yy[1] - yy[0])
    d1 = (xx[-1] - xx[-2]) / (yy[-1] - yy[-2])
    out = np.where(y < yy[0], xx[0] + (y - yy[0]) * d0, out)
    return np.where(y > yy[-1], xx[-1] + (y - yy[-1]) * d1, out)


def dung(k, ti=1.0, thua=1.0):
    """dựng rig dạng k: trả (sk, info). ti < 1, thua > 1: bản nhẹ (ảnh nhỏ, lưới thưa) để gộp vào dạng trước cho clip evolve."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    Dat = khung.Dat
    c = CFG[k]
    dm = os.path.join(d_inbox(k), "manh")
    mj = json.load(open(os.path.join(dm, "manh.json"), encoding="utf-8"))
    mn = np.load(os.path.join(dm, "mat_na.npz"))
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
    for t in LOP:
        sk.anh(t, nap(t))
    top_y = min(mj["manh"][t][1] for t in LOP if t != "gay")
    H = (dat_y - top_y) * sc                                                  # chiều cao con không tính gậy (px rig)

    # ---------------- xương
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("nhun", "move")
    sk.xuong("hong", "nhun", *R(c["hong"]), the_gioi=True)
    sk.xuong("nguc", "hong", *R(c["nguc"]), the_gioi=True)
    sk.xuong("dau", "nguc", *R(c["co"]), the_gioi=True)
    sk.xuong("mu", "dau", *R(c["mu_goc"]), the_gioi=True)
    chop = sk.chuoi("chop", "mu", Rs(c["chop"]))
    vt = sk.chuoi("vt", "mu", Rs(c["vanh_t"]))
    vp = sk.chuoi("vp", "mu", Rs(c["vanh_p"]))
    dtr = sk.chuoi("dt", "mu", Rs(c["dai_tren"]))
    ddu = sk.chuoi("dd", "mu", Rs(c["dai_duoi"]))
    sk.xuong("ch0", "nguc", *R(c["choang_goc"]), the_gioi=True)
    ca = sk.chuoi("ca", "ch0", Rs(c["choang_t"]))
    cb = sk.chuoi("cb", "ch0", Rs(c["choang_p"]))
    sk.xuong("v0", "nguc", *R(c["vat_goc"]), the_gioi=True)
    va = sk.chuoi("va", "v0", Rs(c["vat_t"]))
    vb = sk.chuoi("vb", "v0", Rs(c["vat_p"]))
    gt = sk.chuoi("gt", "hong", Rs(c["gau_t"]))
    gp = sk.chuoi("gp", "hong", Rs(c["gau_p"]))
    kt = sk.chuoi("kt", "nguc", Rs(c["khan_t"]))[0]
    kp = sk.chuoi("kp", "nguc", Rs(c["khan_p"]))[0]
    tt = sk.chuoi("tt", "nguc", Rs(c["tay_t"]))
    # tay xa (cầm gậy): MỘT xương từ vai tới bàn tay, co giãn dọc trục để với tới bàn tay (ống tay áo vẽ thẳng, không có khuỷu:
    # hai đốt gập ở khuỷu làm ống tay gấp chồng lên nhau, rách ở nách: người dùng chê 2026-11-11)
    tp = sk.chuoi("tp", "nguc", Rs([c["tay_p"][0], c["tay_p"][2]]))
    op = sk.chuoi("op", tp[0], Rs(c["ong_p"]))
    G, Fc = np.array(R(c["tay_p"][2])), np.array(R(c["gay_chan"]))            # chỗ nắm, chân gậy (thế giới rig)
    g_goc = math.degrees(math.atan2(G[1] - Fc[1], G[0] - Fc[0]))               # góc trục gậy (chân -> chỗ nắm)
    sk.xuong("ban", "nhun", G[0], G[1], goc=g_goc, the_gioi=True)             # bàn tay + gậy: con của nhun (không nhận co giãn của tay áo, thân)
    dinh = np.array(R(c["gay_dinh"]))
    sk.xuong("gay", "ban", G[0], G[1], goc=g_goc, dai=float(np.hypot(*(dinh - G))), the_gioi=True)
    xc, yc = R(c["cau"])
    sk.xuong("cau", "gay", xc, yc, goc=g_goc, the_gioi=True)
    sk.xuong("mieng", "gay", xc, yc, goc=g_goc, dai=40 * ti, the_gioi=True)
    da = sk.chuoi("da", "gay", Rs(c["day1"]))
    db = sk.chuoi("db", "gay", Rs(c["day2"]))
    sk.xuong("giay_t", "nhun", *R(c["giay"][0]), the_gioi=True)
    sk.xuong("giay_p", "nhun", *R(c["giay"][1]), the_gioi=True)
    sk.xuong("goc_cat", "root")
    sk.xuong("vong", "root", 0.0, 5.0 * sc)                                # clip appear co dẹt xương này theo y: vòng tròn thành elip nằm
    sk.xuong("vong_x", "vong")

    # ---------------- slot (sau -> trước)
    sk.slot("vong", "vong_x", "vong", an=True)
    sk.slot("cat", "goc_cat")
    XUONG_SLOT = {"choang": "ch0", "tay_p": tp[0], "gay": "gay", "day1": da[0], "day2": db[0], "ban": "ban", "giay": "nhun", "ao": "hong", "vat": "v0", "tay_t": tt[0],
                  "toi": "dau", "khan": "nguc", "mu": "mu", "dai": "mu"}
    for t in LOP:
        sk.slot(t, XUONG_SLOT[t], t)
    # mặt nạ cắt: dáng gốc để thấp dưới đất 0,6 H (không cắt gì: áo choàng, gấu áo lúc vung có thể chạm xuống dưới mức chân);
    # clip appear nâng xương goc_cat lên cho mép cắt nằm đúng mặt đất
    sk.cat("cat", "dai", [(-2.6 * H, -0.6 * H), (2.6 * H, -0.6 * H), (2.6 * H, 3.2 * H), (-2.6 * H, 3.2 * H)])

    def luoi_cua(ten, **kw):
        L = luoi.luoi_vung(sk.images[ten], buoc_theo_cao=H * thua, ten=f"{ten} {k}", **kw)
        d = dat_cua(ten)
        V = d.ra(L.pts, *sk.images[ten].size)
        return L, d, V, C_(V)

    tong = {"dinh": 0}

    def gan(ten, L, d, W):
        sk.luoi_gan(ten, ten, L, trongso.chuan(W), dat=d)
        tong["dinh"] += L.n

    # ================= ÁO CHOÀNG: hai chuỗi dọc mép ngoài (ca) và ranh với áo (cb); giữa tấm trộn theo vị trí ngang =================
    L, d, V, Cc = luoi_cua("choang")
    JA, JB = np.array(c["choang_t"], float), np.array(c["choang_p"], float)
    WA = trongso.chuoi_chieu(V, Rs(JA), ca, cha="ch0")
    WB = trongso.chuoi_chieu(V, Rs(JB), cb, cha="ch0")
    dA, dB = kc_gay(Cc, JA), kc_gay(Cc, JB)
    tau = np.clip(dA / (dA + dB + 1e-6), 0, 1)
    tau = np.maximum(ss(tau, 0.08, 0.92), ss(Cc[:, 0] - x_tai_y(JB, Cc[:, 1]), -25, 25))     # qua ranh sang phải (phần khuất): theo cb
    gan("choang", L, d, [_tron((1 - tau[i], WA[i]), (tau[i], WB[i])) for i in range(L.n)])

    # ================= TAY ÁO XA (cầm gậy): chuỗi bắp, cẳng; phần ống rủ dưới trục tay theo chuỗi op =================
    L, d, V, Cc = luoi_cua("tay_p")
    Jt = np.array([c["tay_p"][0], c["tay_p"][2]], float)
    Wa = trongso.chuoi_chieu(V, Rs(Jt), tp, cha="nguc", cha_hoa=0.5)
    Wo = trongso.chuoi_chieu(V, Rs(c["ong_p"]), op, cha=tp[0])
    e0, e1 = Jt[0], Jt[1]
    ax = (e1 - e0) / np.hypot(*(e1 - e0))
    duoi = (Cc - e0) @ np.array([-ax[1], ax[0]])                               # dương = phía dưới trục cẳng tay (y ảnh xuống)
    doc = ((Cc - e0) @ ax) / np.hypot(*(e1 - e0))
    h_ = ss(duoi, 30, 95) * ss(doc, 0.45, 0.8)
    # đường nách: bên trong (phía thân) bám ngực; ra phía cổ tay chuyển dần sang xương tay
    n0, n1 = np.array(c["nach"][0], float), np.array(c["nach"][1], float)
    nd = (n1 - n0) / np.hypot(*(n1 - n0))
    nn = np.array([nd[1], -nd[0]])
    if (e1 - n0) @ nn < 0:
        nn = -nn                                                              # pháp tuyến chĩa về phía bàn tay
    xa = (Cc - n0) @ nn
    w_tay = ss(xa, 0.0, c["nach_hoa"])
    gan("tay_p", L, d, [_tron((1 - w_tay[i], {"nguc": 1.0}), (w_tay[i] * (1 - h_[i]), {tp[0]: 1.0}), (w_tay[i] * h_[i], Wo[i]))
                        for i in range(L.n)])

    # ================= GẬY: cứng theo xương gay; cầu nước theo cau. HẠT TREO: hai lớp riêng, mỗi lớp một chuỗi dây =================
    L, d, V, Cc = luoi_cua("gay")
    r_cau = np.hypot(*(Cc - np.array(c["cau"], float)).T)
    w_cau = 1 - ss(r_cau, c["cau_r"] + 4, c["cau_r"] + 12)
    gan("gay", L, d, [_tron((w_cau[i], {"cau": 1.0}), (1 - w_cau[i], {"gay": 1.0})) for i in range(L.n)])
    for ten, key, ds in (("day1", "day1", da), ("day2", "day2", db)):
        L, d, V, Cc = luoi_cua(ten)
        gan(ten, L, d, trongso.chuoi_chieu(V, Rs(c[key]), ds))            # cả dây theo chuỗi (gốc dây xoay bù góc gậy): không hoà vào gậy

    # ================= BÀN TAY, GIÀY =================
    L, d, V, Cc = luoi_cua("ban")
    gan("ban", L, d, [{"ban": 1.0}] * L.n)
    L, d, V, Cc = luoi_cua("giay")
    xg = 0.5 * (c["giay"][0][0] + c["giay"][1][0])
    gan("giay", L, d, [{"giay_t": 1.0} if Cc[i, 0] < xg else {"giay_p": 1.0} for i in range(L.n)])

    # ================= ÁO DÀI: trên theo ngực, giữa theo hông, gấu theo hai chuỗi mép (trộn theo vị trí ngang) =================
    L, d, V, Cc = luoi_cua("ao")
    JL, JR = np.array(c["gau_t"], float), np.array(c["gau_p"], float)
    WL = trongso.chuoi_chieu(V, Rs(JL), gt)
    WR = trongso.chuoi_chieu(V, Rs(JR), gp)
    xl, xr = x_tai_y(JL, Cc[:, 1]), x_tai_y(JR, Cc[:, 1])
    tau = ss((Cc[:, 0] - xl) / np.maximum(40.0, xr - xl), 0.0, 1.0)
    a_ng = 1 - ss(Cc[:, 1], c["nguc"][1] - 10, 0.5 * (c["nguc"][1] + c["hong"][1]) + 30)
    y0 = 0.5 * (JL[0][1] + JR[0][1])
    h_ = ss(Cc[:, 1], y0 - 25, y0 + 55)
    Wao = []
    for i in range(L.n):
        Wao.append(_tron((a_ng[i], {"nguc": 1.0}), ((1 - a_ng[i]) * (1 - h_[i]), {"hong": 1.0}),
                         ((1 - a_ng[i]) * h_[i] * (1 - tau[i]), WL[i]), ((1 - a_ng[i]) * h_[i] * tau[i], WR[i])))
    gan("ao", L, d, Wao)

    # ================= VẠT TRƯỚC: hai chuỗi dọc hai mép =================
    L, d, V, Cc = luoi_cua("vat")
    JA, JB = np.array(c["vat_t"], float), np.array(c["vat_p"], float)
    WA = trongso.chuoi_chieu(V, Rs(JA), va, cha="v0")
    WB = trongso.chuoi_chieu(V, Rs(JB), vb, cha="v0")
    xl, xr = x_tai_y(JA[:4], Cc[:, 1]), x_tai_y(JB[:4], Cc[:, 1])
    tau = ss((Cc[:, 0] - xl) / np.maximum(30.0, xr - xl), 0.0, 1.0)
    gan("vat", L, d, [_tron((1 - tau[i], WA[i]), (tau[i], WB[i])) for i in range(L.n)])

    # ================= TAY ÁO GẦN (buông): một chuỗi vai -> gấu =================
    L, d, V, Cc = luoi_cua("tay_t")
    gan("tay_t", L, d, trongso.chuoi_chieu(V, Rs(c["tay_t"]), tt, cha="nguc", cha_hoa=0.7))

    # ================= KHOẢNG TỐI dưới mũ: theo đầu =================
    L, d, V, Cc = luoi_cua("toi")
    gan("toi", L, d, [{"dau": 1.0}] * L.n)

    # ================= KHĂN VAI: giữa theo ngực, hai thuỳ theo kt / kp =================
    L, d, V, Cc = luoi_cua("khan")
    xt, xp = c["khan_t"][0][0], c["khan_p"][0][0]
    wl = 0.85 * ss(Cc[:, 0], xt + 40, xt - 80)
    wr = 0.85 * ss(Cc[:, 0], xp - 40, xp + 60)
    gan("khan", L, d, [{kt: float(wl[i]), kp: float(wr[i]), "nguc": float(1 - wl[i] - wr[i])} for i in range(L.n)])

    # ================= MŨ: gốc theo mu; chóp theo chuỗi chop; hai đầu vành theo vt / vp =================
    L, d, V, Cc = luoi_cua("mu")
    Jc, Jl, Jr = np.array(c["chop"], float), np.array(c["vanh_t"], float), np.array(c["vanh_p"], float)
    Wc = trongso.chuoi_chieu(V, Rs(Jc), chop, cha="mu")
    Wl = trongso.chuoi_chieu(V, Rs(Jl), vt, cha="mu")
    Wr = trongso.chuoi_chieu(V, Rs(Jr), vp, cha="mu")

    def doc_dau(J, P):
        u = (J[1] - J[0]) / np.hypot(*(J[1] - J[0]))
        return (P - J[0]) @ u

    m_c = ss(doc_dau(Jc, Cc), -35, 45) * (1 - ss(kc_gay(Cc, Jc), 150, 230))
    m_l = ss(doc_dau(Jl, Cc), -25, 55) * (1 - ss(kc_gay(Cc, Jl), 45, 100)) * (1 - m_c)
    m_r = ss(doc_dau(Jr, Cc), -25, 45) * (1 - ss(kc_gay(Cc, Jr), 45, 100)) * (1 - m_c)
    Wm = []
    for i in range(L.n):
        Wm.append(_tron((m_c[i], Wc[i]), (m_l[i], Wl[i]), (m_r[i], Wr[i]), (max(0.0, 1 - m_c[i] - m_l[i] - m_r[i]), {"mu": 1.0})))
    gan("mu", L, d, Wm)

    # ================= DẢI ĐAI: hai dải, mỗi dải một chuỗi =================
    L, d, V, Cc = luoi_cua("dai")
    J1, J2 = np.array(c["dai_tren"], float), np.array(c["dai_duoi"], float)
    W1 = trongso.chuoi_chieu(V, Rs(J1), dtr, cha="mu", cha_hoa=0.5)
    W2 = trongso.chuoi_chieu(V, Rs(J2), ddu, cha="mu", cha_hoa=0.5)
    gan1 = kc_gay(Cc, J1) <= kc_gay(Cc, J2)
    gan("dai", L, d, [W1[i] if gan1[i] else W2[i] for i in range(L.n)])

    # ================= VÒNG TRIỆU HỒI: ảnh tròn trên xương vong_x (cha vong dẹt theo y: thành elip nằm, xoay được) =================
    rong = (max(mj["manh"]["ao"][2], mj["manh"]["gay"][2]) - mj["manh"]["choang"][0]) * sc * VONG_RONG
    fv = os.path.join(d_inbox(1), "manh", "vong.png")
    if os.path.exists(fv):
        iv = Image.open(fv).convert("RGBA")
        px = max(64, int(round(250 * ti)))
        iv = anh.loang_mau(iv.resize((px, px), Image.LANCZOS))
        sk.anh("vong", iv)
        sk.manh("vong", "vong", Dat(0.0, 5.0 * sc, ti=rong / px), xuong="vong_x")
    sk.su_kien("phun", "bắt đầu nhả tia nước ở cầu nước đầu gậy (xương mieng)")
    sk.su_kien("het_phun", "hết nhả, bắt đầu thu gậy")
    sk.su_kien("trieu_hoi", "giơ gậy: kim nước hiện ra quanh đầu gậy")
    sk.su_kien("dam", "dậm gậy xuống đất: kim nước phóng đi")
    sk.su_kien("het_dam", "hết giữ dáng dậm, bắt đầu về")
    sk.su_kien("vong", "vòng tròn triệu hồi hiện trên đất")
    sk.su_kien("cham_dat", "trồi lên hết")
    info = {"H": H, "ti": ti, "chop": chop, "vt": vt, "vp": vp, "dt": dtr, "dd": ddu, "ca": ca, "cb": cb, "va": va, "vb": vb, "gt": gt,
            "gp": gp, "kt": kt, "kp": kp, "tt": tt, "tp": tp, "op": op, "da": da, "db": db, "G": G, "F": Fc, "g_goc": g_goc,
            "dinh": tong["dinh"], "rong_vong": rong, "sc": sc}
    return sk, info


# ================================================================ CLIP ================================================================
# Nhịp học từ con gốc (ghi chú mục 3), viết theo khung 30 fps của bản thiết kế (dạng 2 chậm lại CHAM lần):
#   idle    2 vòng 40 khung; vòng hai có điểm phá nhịp (nghiêng mũ, cầu nước nẩy). Gậy cắm đất, tay bám gậy (IK giải trong mã).
#   attack  skill_01: giật gậy lên vai 2 khung, giữ 8 khung có trôi, khung gãy 11, chĩa ngang ở khung 12 (trung), giữ tới 23, về 35.
#   cast    cùng động tác, thêm một vòng xoay đầu gậy lúc lấy đà, chĩa ở khung 16 (phun), giữ tới phun + 0,94 s thật, về.
#   skill   skill_02: giơ gậy cao 4 khung (trieu_hoi), gồng 18 khung, dậm ở khung 25 (dam), giữ dáng dậm, về.
#   hit     hit_01. die: bị hất, gậy văng, áo mũ xẹp thành đống (bên trong không có gì). appear: vòng tròn triệu hồi, trồi lên.
def clips(sk, info, k):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    Clip, LoXo, rung = hoat.Clip, hoat.LoXo, hoat.rung
    H = info["H"]
    S = H / 456.0                                                             # mọi độ dời viết cho con cao 456 px rig
    F = 30.0 / CHAM[k]                                                        # khung (của bản thiết kế) mỗi giây
    T0 = 40.0
    slots = [s["name"] for s in sk.slots if s["name"] not in ("vong", "cat")]
    W0 = sk.the_gioi()
    tp0 = info["tp"][0]
    F0, G0, a0 = np.array(info["F"], float), np.array(info["G"], float), float(info["g_goc"])
    Lg = float(np.hypot(*(G0 - F0)))
    TAY0 = G0 - W0["nguc"][:2, 2]                                             # bàn tay dáng gốc trong hệ ngực
    L_TAY = float(np.hypot(*(G0 - W0[tp0][:2, 2])))                           # dài tay dáng gốc (vai -> bàn tay)
    B_BAN = sk.bones[sk.bi["ban"]]
    CH = {"chop": (info["chop"], [1.5, 2.5, 3.5, 4.5], 0, 1), "vt": (info["vt"], [1.2, 2.2], 3, 1), "vp": (info["vp"], [1.2, 2.2], 9, -1),
          "dt": (info["dt"], [3.0, 5.0, 7.0], 2, 1), "dd": (info["dd"], [3.0, 5.5, 8.0], 6, 1),
          "ca": (info["ca"], [2.2, 2.8, 3.6, 5.0, 6.5], 0, 1), "cb": (info["cb"], [1.4, 1.8, 2.6, 3.6, 4.6], 7, 1),
          "va": (info["va"], [0.7, 1.1, 1.8, 2.8], 2, 1), "vb": (info["vb"], [0.7, 1.1, 1.8, 2.8], 6, 1),
          "gt": (info["gt"], [0.9, 1.5, 2.2], 4, -1), "gp": (info["gp"], [0.9, 1.5, 2.2], 8, 1),
          "tt": (info["tt"], [0.9, 1.6, 2.4], 5, 1), "op": (info["op"], [1.8, 3.0], 7, 1),
          "da": (info["da"], [2.5, 4.5, 6.5], 3, 1), "db": (info["db"], [2.5, 4.5, 6.5], 8, 1)}

    def sg(f, chu_ky, tre=0.0):
        """sóng sin theo khung, bằng 0 ở khung 0 (khung 0 của idle là dáng gốc), trễ `tre` khung."""
        return math.sin(2 * math.pi * (f - tre) / chu_ky) + math.sin(2 * math.pi * tre / chu_ky)

    def tung(P, ten, f, keys, he=1.0, tre=1.0, amp=None):
        """vung một chuỗi vải theo khoá (đơn vị: lần biên độ gốc của chuỗi), đốt xa gốc trễ `tre` khung mỗi đốt và vung rộng hơn."""
        ds, am, _, dau = CH[ten]
        am = amp or am
        if ten in ("ca", "cb"):
            he = he * (1.0, 0.7)[k - 1]
        for i, b in enumerate(ds):
            P.rot(b, dau * he * am[i] * ln(f - tre * i, keys))

    def tay_gay(P, bl=0.0, tay=(0.0, 0.0), goc=None, lac=0.0, nhac=0.0, truot=0.0):
        """đặt tay xa và gậy; gọi CUỐI hàm dáng. bl = 0: gậy cắm đất (chân gậy đứng yên so với `nhun`, nhấc lên `nhac`), nghiêng
        thêm `lac` độ, tay bám đúng chỗ nắm trên gậy. bl = 1: bàn tay ở chỗ dáng gốc + `tay` (trong hệ ngực, đơn vị con cao 456),
        trục gậy chĩa góc thế giới `goc`. Ở giữa thì hoà. Ống tay áo là một xương: xoay quanh vai và co giãn dọc trục tới bàn tay."""
        W = sk.the_gioi(P)
        ng = khung.goc_mat(W["nguc"])
        P.rot("ch0", -0.75 * ng)
        P.rot(info["tt"][0], -0.5 * ng)
        P.rot("v0", -0.45 * ng)
        Fw = (W["nhun"] @ np.array([F0[0], F0[1] + nhac, 1.0]))[:2]
        A1 = a0 + lac
        T = Fw + Lg * np.array([math.cos(math.radians(A1)), math.sin(math.radians(A1))])
        A = A1
        if bl > 0:
            T2 = (W["nguc"] @ np.array([TAY0[0] + tay[0] * S, TAY0[1] + tay[1] * S, 1.0]))[:2]
            T = T * (1 - bl) + T2 * bl
            A = A1 * (1 - bl) + (a0 if goc is None else goc) * bl
        # tay áo: xoay quanh vai cho chĩa tới bàn tay, co giãn dọc trục cho vừa tới (0,5 .. 1,6 lần)
        vai_w = W[tp0][:2, 2]
        D = float(np.hypot(*(T - vai_w)))
        P.rot(tp0, ((math.degrees(math.atan2(T[1] - vai_w[1], T[0] - vai_w[0])) - khung.goc_mat(W[tp0])) + 180) % 360 - 180)
        P.scale(tp0, min(1.6, max(0.5, D / L_TAY)), 1.0)
        # bàn tay (con của nhun): đặt đúng chỗ T, trục gậy góc A
        loc = np.linalg.solve(W["nhun"], np.array([T[0], T[1], 1.0]))
        P.move("ban", float(loc[0] - B_BAN["x"]), float(loc[1] - B_BAN["y"]))
        P.rot("ban", A - khung.goc_mat(sk.the_gioi(P)["ban"]))
        if truot:
            P.move("gay", truot, 0.0)                                         # gậy trượt trong bàn tay về phía đầu gậy (nắm thấp xuống)
        return hat_ru(P)

    def hat_ru(P, truoc=0.0):
        """hai dây treo hạt rũ theo trọng lực: gốc dây xoay ngược lại đúng góc gậy đã nghiêng so với dáng gốc. Trả góc đã bù."""
        dg = ((khung.goc_mat(sk.the_gioi(P)["gay"]) - a0) + 180) % 360 - 180
        P.rot(info["da"][0], -(dg - truoc))
        P.rot(info["db"][0], -(dg - truoc))
        return dg

    def gay_tu_do(P, x, y, goc):
        """gậy rời tay (lúc chết): đặt chỗ nắm của gậy ở (x, y) thế giới rig (so với `move`), trục gậy góc `goc`."""
        W = sk.the_gioi(P)
        b = sk.bones[sk.bi["gay"]]
        loc = np.linalg.solve(W["ban"], np.array([x, y, 1.0]))
        P.move("gay", float(loc[0] - b["x"]), float(loc[1] - b["y"]))
        W = sk.the_gioi(P)
        P.rot("gay", goc - khung.goc_mat(W["gay"]))

    def nen(P, f, a=1.0):
        """chuyển động nền (idle) ở khung f, biên độ a; mọi thành phần bằng 0 ở f = 0. Trả độ lắc của gậy (độ)."""
        if a <= 0:
            return 0.0
        tho = 0.5 * (1 - math.cos(2 * math.pi * f / T0))
        P.move("hong", a * 0.8 * S * sg(f, T0, 5), -a * 2.6 * S * tho)
        P.rot("hong", a * 1.0 * sg(f, T0, 3))
        P.scale("hong", 1 + 0.012 * a * tho, 1 - 0.006 * a * tho)
        P.move("nguc", 0, a * 1.6 * S * tho)
        P.rot("nguc", -a * 1.3 * sg(f, T0, 8))
        P.rot("dau", a * 1.1 * sg(f, T0, 13))
        P.rot("mu", a * 0.9 * sg(f, T0, 17))
        P.rot(info["kt"], a * 1.6 * sg(f, T0, 6))
        P.rot(info["kp"], -a * 1.6 * sg(f, T0, 9))
        for ten, (ds, am, pha, dau) in CH.items():
            for i, b in enumerate(ds):
                P.rot(b, a * dau * am[i] * 0.5 * sg(f, T0, pha + 5 * i))
        cs = 1 + 0.02 * a * sg(f, T0, 11)
        P.scale("cau", cs, cs)
        return a * 1.3 * sg(f, T0, 9)

    def an_het(P, a):
        for s in slots:
            P.alpha[s] = a

    def mem():
        return [LoXo(info["ca"], k=[420, 360, 300, 250, 210], damp=0.5, maxang=16), LoXo(info["cb"], k=[520, 440, 370, 310, 260], damp=0.5, maxang=13),
                LoXo(info["va"], k=[560, 470, 390, 320], damp=0.5, maxang=12), LoXo(info["vb"], k=[620, 520, 430, 350], damp=0.5, maxang=12),
                LoXo(info["gt"], k=[560, 460, 380], damp=0.5, maxang=10), LoXo(info["gp"], k=[600, 500, 410], damp=0.5, maxang=10),
                LoXo(info["chop"], k=[620, 500, 400, 320], damp=0.5, maxang=12),
                LoXo(info["dt"], k=[380, 300, 240], damp=0.5, maxang=16), LoXo(info["dd"], k=[340, 270, 210], damp=0.5, maxang=16),
                LoXo(info["tt"], k=[560, 440, 340], damp=0.5, maxang=12), LoXo(info["op"], k=[620, 480], damp=0.55, maxang=6),
                # hai dây treo hạt: gốc dây xoay bù góc gậy (hat_ru: gậy chĩa ngang thì hạt vẫn rũ xuống đất), lò xo thêm độ trễ
                LoXo(info["da"], k=[300, 230, 180], damp=0.45, maxang=24), LoXo(info["db"], k=[270, 210, 160], damp=0.45, maxang=24),
                LoXo(info["vt"], k=[700, 520], damp=0.5, maxang=7), LoXo(info["vp"], k=[700, 520], damp=0.5, maxang=7)]

    # ---------------- idle: 2 vòng; vòng hai nghiêng mũ nhìn đầu gậy, cầu nước nẩy
    def idle_fn(t, P):
        f = t * F
        lac = nen(P, f)
        g = f % 80
        P.rot("dau", ln(g, [(0, 0), (44, 0), (48, -5.5), (57, -5.5), (61, 2.5), (65, 0), (80, 0)]))
        P.rot("mu", ln(g, [(0, 0), (45, 0), (49, -3), (58, -3), (62, 2), (67, 0), (80, 0)]))
        tung(P, "chop", g, [(0, 0), (45, 0), (49, 1.6), (56, 0.8), (62, -1.2), (68, 0.4), (74, 0), (80, 0)], tre=1.5)
        cs = ln(g, [(0, 1), (49, 1), (51, 1.16), (54, 0.94), (57, 1.05), (60, 1), (80, 1)])
        P.scale("cau", cs, cs)
        tay_gay(P, lac=lac + ln(g, [(0, 0), (46, 0), (50, 1.6), (58, 1.6), (64, 0), (80, 0)]))

    # ---------------- attack / cast: giật gậy lên vai, chĩa ngang ra trước nhả tia, giữ, thu về
    def ban(P, f, f_ra, f_giu, f_ve, xoay=0.0, run=0.0):
        """động tác bắn tia dùng chung. f_ra: khung chĩa gậy; f_giu: hết giữ; f_ve: khung cuối. xoay: biên độ vòng xoay đầu gậy lúc lấy
        đà (cast). run: độ rung lúc giữ (±1)."""
        a, b, c_ = f_ra, f_giu, f_ve
        bl = ln(f, [(0, 0), (2, 1), (b + 3, 1), (c_ - 1, 0), (c_, 0)])
        tx = ln(f, [(0, 0), (2, -66), (a - 2, -76), (a - 1, -28), (a, 14), (a + 2, 20), (a + 5, 15), (b, 17), (b + 3, 4), (c_ - 3, 0), (c_, 0)])
        ty = ln(f, [(0, 0), (2, 44), (a - 2, 54), (a - 1, 50), (a, 19), (a + 2, 17), (a + 5, 19), (b, 17), (b + 3, 30), (c_ - 3, 4), (c_, 0)])
        go = ln(f, [(0, a0), (2, 128), (a - 2, 141), (a - 1, 72), (a, 8), (a + 2, 4), (a + 5, 8), (b, 6), (b + 3, 36), (c_ - 3, 83), (c_, a0)])
        if xoay:                                                              # vẽ một vòng nhỏ bằng đầu gậy trong lúc lấy đà
            ph = 2 * math.pi * (f - 2) / max(1.0, (a - 4))
            w = xoay * ln(f, [(0, 0), (2, 0), (4, 1), (a - 3, 1), (a - 2, 0)])
            go += 13 * w * math.sin(ph)
            tx += 9 * w * math.cos(ph)
            ty += 7 * w * math.sin(ph)
        go += 1.2 * run
        ty += 1.5 * run
        # thân: ngả sau lấy đà, chồm tới lúc chĩa, giật lùi ngược chiều bắn, giữ có trôi
        P.rot("hong", ln(f, [(0, 0), (2, 5.5), (a - 2, 6.5), (a - 1, -2), (a, -7.5), (a + 2, 1.5), (a + 5, -3.5), (b, -6), (b + 3, -3), (c_, 0)]))
        P.move("hong", ln(f, [(0, 0), (2, -3), (a - 2, -6), (a, -15), (a + 2, -12), (a + 5, -13), (b, -14), (b + 3, -7), (c_, 0)]) * S,
               ln(f, [(0, 0), (2, 3), (a - 2, 4), (a, -5), (a + 2, -2), (a + 5, -4), (b, -5), (b + 3, -2), (c_, 0)]) * S + 0.8 * run * S)
        P.scale("hong", ln(f, [(0, 1), (a - 1, 1), (a, 1.04), (a + 3, 1), (c_, 1)]), ln(f, [(0, 1), (a - 1, 1), (a, 0.96), (a + 3, 1), (c_, 1)]))
        P.rot("nguc", ln(f, [(0, 0), (2, 4.5), (a - 2, 9), (a - 1, 2), (a, -2), (a + 2, -10), (a + 5, -2), (b, 3.5), (b + 3, 5), (c_, 0)]))
        P.rot("dau", ln(f, [(0, 0), (2, -4.5), (a - 2, -7), (a - 1, 0), (a, -3), (a + 2, -11), (a + 5, -1), (a + 8, 2.5), (b, 2), (b + 3, -6), (c_, 0)]))
        P.rot("mu", ln(f, [(0, 0), (2, -3), (a - 2, -2), (a, 4), (a + 2, -5), (a + 5, 2), (b, 0), (c_, 0)]))
        tung(P, "chop", f, [(0, 0), (2, -2.6), (5, -4.5), (a - 2, 0.8), (a, 1.6), (a + 2, 5), (a + 5, -2), (b, -1.6), (b + 6, 2.6), (c_, 0)])
        tung(P, "vt", f, [(0, 0), (2, -2), (a - 2, 0), (a, 3), (a + 3, -2.5), (b, 0), (c_, 0)])
        tung(P, "vp", f, [(0, 0), (2, -2), (a - 2, 0), (a, 3), (a + 3, -2.5), (b, 0), (c_, 0)])
        # áo choàng: gốc văng ngay lúc giật gậy, ngọn trễ; lúc chĩa thì tung ra sau rồi lắng
        tung(P, "ca", f, [(0, 0), (2, 2.2), (5, 2.4), (a - 2, 1.0), (a, -1.5), (a + 2, -6.5), (a + 5, -3.5), (b, -3.0), (b + 5, 1.2), (c_, 0)], tre=1.4)
        tung(P, "cb", f, [(0, 0), (2, 1.5), (a - 2, 0.6), (a, -2.5), (a + 2, -5.5), (a + 5, -4.2), (b, -2.5), (b + 5, 1.0), (c_, 0)], tre=1.8)
        tung(P, "va", f, [(0, 0), (2, -3), (5, 1.5), (a - 2, -1), (a, 3), (a + 2, -5), (a + 5, 2), (b, 4), (b + 4, -3), (c_, 0)])
        tung(P, "vb", f, [(0, 0), (2, -3), (5, 1.5), (a - 2, -1), (a, 3), (a + 2, -5), (a + 5, 2), (b, 4), (b + 4, -3), (c_, 0)], tre=1.6)
        tung(P, "gt", f, [(0, 0), (2, 2), (a - 2, 1), (a, -4), (a + 3, 2), (b, 1), (c_, 0)])
        tung(P, "gp", f, [(0, 0), (2, 1), (a - 2, 1), (a, 5), (a + 3, 2), (b, 2), (c_, 0)])
        tung(P, "tt", f, [(0, 0), (2, 5), (a - 2, 6), (a, -8), (a + 3, -3), (b, -4), (b + 4, 3), (c_, 0)])
        tung(P, "dt", f, [(0, 0), (2, -2), (a - 2, 0), (a, 2.5), (a + 3, -3.5), (b, -1), (c_, 0)])
        tung(P, "dd", f, [(0, 0), (2, -2), (a - 2, 0), (a, 2.5), (a + 3, -3.5), (b, -1), (c_, 0)], tre=1.5)
        P.rot(info["kp"], ln(f, [(0, 0), (2, 16), (a - 2, 20), (a, 6), (b, 5), (c_, 0)]))
        P.rot(info["kt"], ln(f, [(0, 0), (2, -3), (a, 6), (a + 3, -3), (c_, 0)]))
        cs = ln(f, [(0, 1), (2, 1), (a - 2, 1.14), (a, 0.84), (a + 2, 1.1), (a + 4, 1), (c_, 1)]) * (1 + 0.035 * run)
        P.scale("cau", cs, cs)
        # chĩa ngang thì nắm thấp xuống: phần đuôi gậy sau bàn tay ngắn lại, nấp hết sau thân (dạng 2 gậy dài, đuôi gậy xuyên qua
        # người lòi ra bên kia)
        tr = max(0.0, Lg - 150.0 * S) * ln(f, [(0, 0), (2, 0.35), (a - 1, 0.6), (a, 1), (b, 1), (b + 3, 0.6), (c_ - 2, 0), (c_, 0)])
        tay_gay(P, bl, (tx, ty), go, truot=tr)

    A_RA, A_GIU, A_VE = 12.0, 23.0, 36.0
    DAN_BAY = 0.13                                                            # = HatNuoc.DanTravel (giây thật)

    def attack_fn(t, P):
        f = t * F
        nen(P, f, 0.5 * hoat.bao(t, 0, A_VE / F, 4 / F, 6 / F))
        ban(P, f, A_RA, A_GIU, A_VE, run=rung(t, (A_RA + 2) / F, A_GIU / F))

    GIU_TIA = 0.94                                                            # dòng tia của game chảy 0,88 s thật kể từ sự kiện phun
    C_RA = 16.0
    C_GIU = C_RA + math.ceil(GIU_TIA * F + 1)
    C_VE = C_GIU + 13.0

    def cast_fn(t, P):
        f = t * F
        nen(P, f, 0.4 * hoat.bao(t, 0, C_VE / F, 4 / F, 6 / F))
        ban(P, f, C_RA, C_GIU, C_VE, xoay=1.0, run=rung(t, (C_RA + 2) / F, C_GIU / F))

    # ---------------- skill: giơ gậy cao, gồng (kim nước hiện quanh gậy: VFX), dậm gậy xuống đất (kim phóng đi), giữ dáng dậm, về
    K_GIO, K_DAM = 4.0, 31.0
    K_GIU = K_DAM + math.ceil(0.86 * F)                                       # giữ dáng dậm tới khi loạt kim bay hết (n_thuong: 8 mũi x 0,1 s)
    K_VE = K_GIU + 11.0
    KHUA = 8.0                                                                # một nhịp khua gậy (khung): qua lại ba lần lúc gồng

    def skill_fn(t, P):
        f = t * F
        a, b, c_ = K_DAM, K_GIU, K_VE
        g1, g2 = a - 3, a - 1                                                 # hết gồng, khung gãy
        r1 = rung(t, 6 / F, g1 / F, moi=1)
        go_ = ln(f, [(0, 0), (4, 1), (g1, 1), (a, 0), (c_, 0)])                  # đang giơ gậy
        bl = ln(f, [(0, 0), (4, 1), (g1, 1), (g2, 0.75), (a, 0), (c_, 0)])
        # khua gậy: đầu gậy vẽ vòng số 8 nằm phía trên mũ (gậy nghiêng qua lại ±19°, bàn tay đưa theo), biên độ lớn dần rồi thu lại
        ph = 2 * math.pi * (f - 4) / KHUA
        kh = ln(f, [(0, 0), (4, 0), (7, 1), (g1 - 3, 1.15), (g1, 0.3), (g2, 0), (c_, 0)])
        sw, cw = math.sin(ph) * kh, math.sin(2 * ph) * kh
        tx = ln(f, [(0, 0), (4, -14), (g1, -18), (g2, -6), (a, 0)]) - 13 * sw
        ty = ln(f, [(0, 0), (4, 58), (g1, 66), (g2, 46), (a, 0)]) + 5 * cw
        go = ln(f, [(0, a0), (4, 94), (g1, 96), (g2, 90), (a, a0)]) + 19 * sw + 0.8 * r1 * go_
        P.rot("hong", ln(f, [(0, 0), (4, 5), (g1, 4.5), (g2, 1), (a, -5), (a + 2, 4), (a + 5, -3), (b, -4.5), (b + 5, 0), (c_, 0)]) + 1.6 * sw)
        P.move("hong", ln(f, [(0, 0), (4, -4), (g1, -4), (a, 3), (b, 3), (c_, 0)]) * S - 3.0 * sw * S,
               (ln(f, [(0, 0), (4, 6), (g1, 12), (g2, 2), (a, -15), (a + 2, -4), (a + 5, -8), (b, -11), (b + 5, -1), (c_, 0)]) + 1.6 * abs(cw)) * S)
        P.scale("hong", ln(f, [(0, 1), (4, 0.98), (g1, 0.97), (a, 1.07), (a + 3, 1.0), (b, 1.02), (c_, 1)]),
                ln(f, [(0, 1), (4, 1.03), (g1, 1.05), (a, 0.9), (a + 3, 1.0), (b, 0.97), (c_, 1)]))
        P.rot("nguc", ln(f, [(0, 0), (4, 3.5), (g1, 2), (g2, 0), (a, -11), (a + 2, -16), (a + 5, -6), (b, -6), (b + 5, -7), (c_, 0)]) + 2.2 * sw)
        P.rot("dau", ln(f, [(0, 0), (4, 5), (g1, 6.5), (a, 0), (a + 2, -8), (a + 5, -9), (b, -2), (b + 5, -9), (c_, 0)]) + 2.6 * math.sin(ph - 0.9) * kh)
        P.rot("mu", ln(f, [(0, 0), (4, 2), (g1, 3), (a, -6), (a + 2, 5), (a + 5, -3), (b, 0), (c_, 0)]) + 2.0 * math.sin(ph - 1.5) * kh)
        tung(P, "chop", f, [(0, 0), (4, -3.5), (10, -1), (g1, 2.2), (a, 1), (a + 2, 6.5), (a + 5, 1), (b, -3), (b + 5, 3), (c_, 0)])
        for i, bn in enumerate(info["chop"]):
            P.rot(bn, (2.0, 3.0, 4.0, 5.0)[i] * math.sin(ph - 1.6 - 0.5 * i) * kh)
        tung(P, "vt", f, [(0, 0), (4, 3), (g1, 4), (a, -6), (a + 3, 4), (a + 7, -1.5), (b, 0), (c_, 0)])
        tung(P, "vp", f, [(0, 0), (4, 3), (g1, 4), (a, -6), (a + 3, 4), (a + 7, -1.5), (b, 0), (c_, 0)])
        # áo choàng: phồng lên lúc gồng, đung đưa theo nhịp khua (trễ), dậm thì tung lên rồi rơi
        tung(P, "ca", f, [(0, 0), (4, -2.5), (10, -4.2), (g1, -3.8), (a, -3), (a + 2, -6), (a + 5, -3.4), (b, -0.8), (b + 5, 1.0), (c_, 0)], tre=1.4)
        tung(P, "cb", f, [(0, 0), (4, -1.6), (10, -2.6), (g1, -4), (g2, -2.6), (a, -4.6), (a + 2, -6.5), (a + 5, -3.6), (b, -1), (b + 5, 1.2), (c_, 0)], tre=1.8)
        for ten, he, tre_ in (("ca", 1.5, 0.45), ("cb", 1.3, 0.55), ("va", 2.2, 0.4), ("vb", 2.2, 0.5), ("dt", 1.2, 0.5), ("dd", 1.2, 0.6),
                              ("tt", 2.0, 0.4), ("gt", 1.2, 0.4), ("gp", 1.2, 0.4)):
            ds, am, _, dau = CH[ten]
            for i, bn in enumerate(ds):
                P.rot(bn, he * am[i] * math.sin(ph - 1.2 - tre_ * i) * kh * (0.7 if (ten in ("ca", "cb") and k == 2) else 1.0))
        tung(P, "va", f, [(0, 0), (4, -4), (10, 3), (g1, -2), (a, 5), (a + 2, -7), (a + 5, 4), (b, 3), (b + 5, -3), (c_, 0)])
        tung(P, "vb", f, [(0, 0), (4, -4), (10, 3), (g1, -2), (a, 5), (a + 2, -7), (a + 5, 4), (b, 3), (b + 5, -3), (c_, 0)], tre=1.6)
        tung(P, "gt", f, [(0, 0), (4, 2), (g1, 3), (a, -7), (a + 3, -3), (b, -3.5), (c_, 0)])
        tung(P, "gp", f, [(0, 0), (4, 2), (g1, 3), (a, -7), (a + 3, -3), (b, -3.5), (c_, 0)])
        tung(P, "tt", f, [(0, 0), (4, -5), (g1, -7), (a, 6), (a + 3, -4), (b, -2), (c_, 0)])
        tung(P, "dt", f, [(0, 0), (4, 3), (g1, 4), (a, -4), (a + 3, 4), (b, 0), (c_, 0)])
        tung(P, "dd", f, [(0, 0), (4, 3), (g1, 4), (a, -4), (a + 3, 4), (b, 0), (c_, 0)], tre=1.5)
        P.rot(info["kp"], ln(f, [(0, 0), (4, 22), (g1, 26), (a, 0), (c_, 0)]) + 5 * sw)
        P.rot(info["kt"], ln(f, [(0, 0), (4, -4), (g1, -5), (a, 7), (a + 3, -2), (c_, 0)]))
        cs = ln(f, [(0, 1), (4, 1), (g1, 1.3), (a, 0.82), (a + 2, 1.18), (a + 5, 1), (c_, 1)]) * (1 + 0.04 * r1 * go_)
        P.scale("cau", cs, cs)
        tay_gay(P, bl, (tx, ty), go, lac=ln(f, [(0, 0), (a, -5.5), (a + 1, -4), (a + 2, -5.5), (b, -3.5), (b + 5, -1.5), (c_, 0)]),
                nhac=ln(f, [(0, 0), (a, 0), (a + 1, 4 * S), (a + 2, 0)]))

    # ---------------- hit: gập người, lùi, gậy trượt theo rồi cắm lại
    def hit_fn(t, P):
        f = t * F
        P.move("hong", ln(f, [(0, 0), (1, -12), (2, -17), (6, -12), (10, -6), (15, 0)]) * S, ln(f, [(0, 0), (2, -8), (6, -5), (10, -1), (15, 0)]) * S)
        P.rot("hong", ln(f, [(0, 0), (2, 6), (6, 4), (10, 1.5), (15, 0)]))
        P.scale("hong", ln(f, [(0, 1), (1, 0.95), (3, 1.03), (10, 1.01), (15, 1)]), ln(f, [(0, 1), (1, 1.06), (3, 0.97), (10, 0.99), (15, 1)]))
        P.rot("nguc", ln(f, [(0, 0), (2, -16), (6, -10), (10, -9), (15, 0)]))
        P.rot("dau", ln(f, [(0, 0), (2, 10), (6, -9), (10, -13), (15, 0)]))
        P.rot("mu", ln(f, [(0, 0), (2, 7), (6, -5), (10, 2), (15, 0)]))
        tung(P, "chop", f, [(0, 0), (2, 3), (10, -3), (13, 5), (15, 0)])
        tung(P, "ca", f, [(0, 0), (1, 7), (2, 6), (6, 2), (10, -1.5), (13, 1), (15, 0)], tre=1.2)
        tung(P, "cb", f, [(0, 0), (1, 6), (2, 5), (6, 1.5), (10, -1.5), (15, 0)], tre=1.5)
        tung(P, "va", f, [(0, 0), (2, 8), (6, -4), (10, 5), (15, 0)])
        tung(P, "vb", f, [(0, 0), (2, 8), (6, -4), (10, 5), (15, 0)], tre=1.4)
        tung(P, "gt", f, [(0, 0), (2, -5), (8, 2), (15, 0)])
        tung(P, "gp", f, [(0, 0), (2, 6), (8, -2), (15, 0)])
        tung(P, "tt", f, [(0, 0), (2, 8), (8, -5), (15, 0)])
        tung(P, "dt", f, [(0, 0), (2, 5), (8, -3), (15, 0)])
        tung(P, "dd", f, [(0, 0), (2, 5), (8, -3), (15, 0)], tre=1.4)
        tay_gay(P, lac=ln(f, [(0, 0), (2, 9), (6, 7), (10, 3), (15, 0)]), nhac=ln(f, [(0, 0), (10, 0), (12, 5 * S), (13, 0)]))

    # ---------------- die: bị hất, gậy văng khỏi tay, rồi áo mũ XẸP xuống thành đống, mũ úp lên trên (bên trong không có gì); mờ dần
    D_ROI, D_XEP, D_NAM, D_HET = 4.0, 12.0, 26.0, 46.0

    def die_fn(t, P):
        f = t * F
        xep = ln(f, [(0, 0), (D_XEP, 0), (D_XEP + 5, 0.72), (D_XEP + 8, 0.94), (D_XEP + 10, 0.86), (D_NAM, 1), (D_HET, 1)])   # áo xẹp
        hat_ = ln(f, [(0, 0), (2, 1), (6, 0.8), (D_XEP, 0), (D_HET, 0)])                                                      # bị hất
        P.move("nhun", -16 * S * ln(f, [(0, 0), (3, 1), (D_XEP, 1.3), (D_HET, 1.3)]), 20 * S * ln(f, [(0, 0), (3, 1), (7, 0.9), (D_XEP, 0), (D_HET, 0)]))
        P.rot("hong", 9 * hat_ - 3 * xep)
        P.move("hong", 0, -30 * S * xep)
        P.scale("hong", 1 + 0.2 * xep, 1 - 0.12 * xep)
        P.rot("nguc", -14 * hat_ + 5 * xep)
        P.move("nguc", 8 * S * xep, -112 * S * xep)
        P.rot("dau", 10 * hat_ + ln(f, [(0, 0), (D_XEP, 0), (D_XEP + 5, -10), (D_XEP + 8, -24), (D_XEP + 11, -16), (D_NAM, -20), (D_HET, -20)]))
        P.move("dau", -6 * S * xep, ln(f, [(0, 0), (D_XEP + 8, 0), (D_XEP + 10, 6), (D_NAM - 2, 0), (D_HET, 0)]) * S - 30 * S * xep)
        P.alpha["toi"] = ln(f, [(0, 1), (D_XEP + 4, 1), (D_XEP + 9, 0), (D_HET, 0)])
        P.rot("mu", ln(f, [(0, 0), (2, 6), (D_XEP, -2), (D_XEP + 8, 6), (D_NAM, 3), (D_HET, 3)]))
        tung(P, "chop", f, [(0, 0), (2, 3), (8, -3), (D_XEP + 5, -6), (D_XEP + 9, 7), (D_XEP + 13, 3), (D_NAM + 3, 5), (D_HET, 5)])
        tung(P, "vt", f, [(0, 0), (D_XEP, 0), (D_XEP + 5, 6), (D_XEP + 9, -8), (D_NAM, -5), (D_HET, -5)])
        tung(P, "vp", f, [(0, 0), (D_XEP, 0), (D_XEP + 5, 6), (D_XEP + 9, -8), (D_NAM, -5), (D_HET, -5)])
        # gấu áo xoè ra hai bên, áo choàng và tay áo rũ sang bên rồi nằm
        for ten, goc in (("gt", -17.0), ("gp", 17.0)):
            for i, bn in enumerate(info[ten]):
                P.rot(bn, goc * 1.5 * xep * (1.0, 0.8, 0.6)[i])
        for i, bn in enumerate(info["ca"]):
            P.rot(bn, 5 * hat_ * (i + 1) * 0.5 - (9, 8, 7, 7, 6)[i] * xep)
        for i, bn in enumerate(info["cb"]):
            P.rot(bn, 4 * hat_ * (i + 1) * 0.5 - (4, 4, 4, 5, 5)[i] * xep)
        for i, bn in enumerate(info["tt"]):
            P.rot(bn, 6 * hat_ - (22, 16, 12)[i] * xep)
        for i, bn in enumerate(info["va"]):
            P.rot(bn, (3, 5, 7, 9)[i] * xep)
        for i, bn in enumerate(info["vb"]):
            P.rot(bn, (3, 5, 7, 9)[i] * xep)
        tung(P, "dt", f, [(0, 0), (2, 5), (8, -4), (D_XEP + 6, -5), (D_XEP + 10, 4), (D_NAM, 6), (D_HET, 6)])
        tung(P, "dd", f, [(0, 0), (2, 5), (8, -4), (D_XEP + 6, -5), (D_XEP + 10, 4), (D_NAM, 6), (D_HET, 6)], tre=1.4)
        P.rot(info["kt"], -20 * xep)
        P.rot(info["kp"], 20 * xep)
        # tay xa buông gậy rồi rũ xuống theo áo; bàn tay biến mất
        bl = ln(f, [(0, 0), (2, 1), (D_HET, 1)])
        da_bu = tay_gay(P, bl, (ln(f, [(0, 0), (2, 6), (D_ROI, -6), (D_XEP, -28), (D_NAM, -36), (D_HET, -36)]),
                        ln(f, [(0, 0), (2, 14), (D_ROI, 20), (D_XEP, -24), (D_NAM, -30), (D_HET, -30)])),
                ln(f, [(0, a0), (2, a0 + 12), (D_HET, a0 + 12)]))
        P.alpha["ban"] = ln(f, [(0, 1), (D_XEP - 2, 1), (D_XEP + 3, 0), (D_HET, 0)])
        P.alpha["giay"] = ln(f, [(0, 1), (D_XEP, 1), (D_XEP + 4, 0), (D_HET, 0)])
        # gậy văng ra trước, xoay nửa vòng, rơi xuống đất nảy rồi nằm
        if f >= 2:
            g0 = (W0["move"] @ np.array([G0[0], G0[1], 1.0]))[:2]
            u = f - 2
            x = g0[0] + ln(u, [(0, 0), (3, 12), (9, 40), (14, 58), (18, 64), (24, 66), (44, 66)]) * S
            y = ln(u, [(0, g0[1] + 14 * S), (3, g0[1] + 46 * S), (6, g0[1] + 54 * S), (10, g0[1] + 10 * S), (14, 13 * S), (16, 30 * S), (19, 13 * S),
                       (21, 19 * S), (23, 13 * S), (44, 13 * S)])
            gy = ln(u, [(0, a0 + 12), (4, 62), (9, 24), (14, -4), (16, 5), (19, -3), (21, 1), (23, -2), (44, -2)])
            gay_tu_do(P, x, y, gy)
            hat_ru(P, da_bu)
        tung(P, "da", f, [(0, 0), (3, 5), (10, -5), (18, 6), (22, -3), (28, 0), (D_HET, 0)])
        tung(P, "db", f, [(0, 0), (3, 5), (10, -5), (18, 6), (22, -3), (28, 0), (D_HET, 0)], tre=1.4)
        if f > D_HET - 12:
            an_het(P, ln(f, [(D_HET - 12, 1), (D_HET - 1, 0), (D_HET, 0)]))
            P.alpha["ban"] = 0.0
            P.alpha["giay"] = 0.0
            P.alpha["toi"] = 0.0

    # ---------------- appear: vòng tròn triệu hồi hiện trên đất, xoay; tướng trồi lên qua mặt đất (mặt nạ cắt); vòng tan
    AP_VONG, AP_LEN, AP_DAT, AP_HET = 6.0, 7.0, 23.0, 38.0
    CAO_TROI = 1.08 * H / SC * info["sc"]                                      # chìm sâu chừng này lúc đầu (cả mũ lẫn đầu gậy)

    def appear_fn(t, P):
        f = t * F
        P.alpha["vong"] = ln(f, [(0, 0), (1, 0), (AP_VONG, 1), (AP_DAT + 5, 1), (AP_HET - 1, 0), (AP_HET, 0)])
        vs = ln(f, [(0, 0.35), (AP_VONG, 1.06), (AP_VONG + 3, 1.0), (AP_DAT + 5, 1.0), (AP_HET, 1.12)])
        P.scale("vong", vs, vs * VONG_DEP)
        P.rot("vong_x", -7.5 * f)
        u = ss(f, AP_LEN, AP_DAT)
        u = 1 - (1 - u) ** 1.6
        y = -CAO_TROI * (1 - u) + ln(f, [(0, 0), (AP_DAT, 0), (AP_DAT + 3, 7 * S), (AP_DAT + 7, 0), (AP_HET, 0)])
        P.move("nhun", 0, y)
        P.move("goc_cat", 0, (0.6 * H - 2.0 * info["sc"]) * ln(f, [(0, 1), (AP_DAT + 1, 1), (AP_DAT + 5, 0), (AP_HET, 0)]))
        v = ln(f, [(0, 0), (AP_LEN, 0), (AP_LEN + 5, 1), (AP_DAT - 2, 1), (AP_DAT + 2, -0.7), (AP_DAT + 7, 0.3), (AP_DAT + 11, 0), (AP_HET, 0)])
        P.scale("hong", 1 - 0.04 * v, 1 + 0.05 * v)
        P.rot("dau", 4 * v)
        tung(P, "ca", f, [(0, 0), (AP_LEN, 0), (AP_LEN + 5, 2.5), (AP_DAT - 2, 2.5), (AP_DAT + 3, -4), (AP_DAT + 8, 1), (AP_HET, 0)], tre=1.4)
        tung(P, "cb", f, [(0, 0), (AP_LEN, 0), (AP_LEN + 5, 2), (AP_DAT - 2, 2), (AP_DAT + 3, -4), (AP_DAT + 8, 1), (AP_HET, 0)], tre=1.8)
        tung(P, "gt", f, [(0, 0), (AP_LEN + 5, 4), (AP_DAT - 2, 4), (AP_DAT + 3, -5), (AP_DAT + 8, 1), (AP_HET, 0)])
        tung(P, "gp", f, [(0, 0), (AP_LEN + 5, 4), (AP_DAT - 2, 4), (AP_DAT + 3, -5), (AP_DAT + 8, 1), (AP_HET, 0)])
        tung(P, "chop", f, [(0, 0), (AP_LEN + 5, 3), (AP_DAT - 2, 3), (AP_DAT + 3, -5), (AP_DAT + 8, 2), (AP_HET, 0)])
        tung(P, "dt", f, [(0, 0), (AP_LEN + 5, -4), (AP_DAT - 2, -4), (AP_DAT + 3, 4), (AP_DAT + 8, -1), (AP_HET, 0)])
        tung(P, "dd", f, [(0, 0), (AP_LEN + 5, -4), (AP_DAT - 2, -4), (AP_DAT + 3, 4), (AP_DAT + 8, -1), (AP_HET, 0)], tre=1.4)
        tung(P, "vt", f, [(0, 0), (AP_LEN + 5, -3), (AP_DAT - 2, -3), (AP_DAT + 3, 5), (AP_DAT + 8, -1), (AP_HET, 0)])
        tung(P, "vp", f, [(0, 0), (AP_LEN + 5, -3), (AP_DAT - 2, -3), (AP_DAT + 3, 5), (AP_DAT + 8, -1), (AP_HET, 0)])
        cs = ln(f, [(0, 1), (AP_DAT, 1), (AP_DAT + 2, 1.2), (AP_DAT + 5, 0.94), (AP_DAT + 8, 1), (AP_HET, 1)])
        P.scale("cau", cs, cs)
        tay_gay(P)

    info["tay_gay"] = tay_gay
    return [Clip("appear", AP_HET / F, appear_fn, ev=[(1 / F, "vong", ""), (AP_DAT / F, "cham_dat", "")], mem=mem()),
            Clip("idle", 80 / F, idle_fn, loop=True, mem=mem()),
            # đòn thường: đạn nước của game (HatNuoc.NDan) rời đầu gậy ở khung chĩa (phun) và bay DAN_BAY giây thật: khung trúng của clip
            # (game.hitTimes) đặt đúng lúc đạn chạm đối thủ
            Clip("attack", A_VE / F, attack_fn, ev=[(A_RA / F, "phun", ""), (A_RA / F + DAN_BAY, "trung", ""), (A_GIU / F, "het_phun", "")],
                 trung=A_RA / F + DAN_BAY, mem=mem()),
            Clip("cast", C_VE / F, cast_fn, ev=[(C_RA / F, "phun", ""), (C_GIU / F, "het_phun", "")], mem=mem()),
            Clip("skill", K_VE / F, skill_fn, ev=[(K_GIO / F, "trieu_hoi", ""), (K_DAM / F, "dam", ""), (K_GIU / F, "het_dam", "")], trung=K_DAM / F,
                 mem=mem()),   # có het_*: sân để clip tự diễn đoạn giữ (AolaActor.SelfHold), không ghìm ở khung dậm
            Clip("hit", 15 / F, hit_fn, mem=mem()),
            Clip("die", D_HET / F, die_fn, mem=mem())]


def khop_dau(frames, dich, giay=0.15, fps=30):
    """hoà `giay` đầu clip từ tư thế dich (khung 0 idle, có độ trễ lò xo của vòng lặp) sang clip: vào clip không giật. Sửa tại chỗ."""
    m = max(1, min(len(frames) - 1, int(round(giay * fps))))
    p0 = frames[0]
    lech = {}
    for b in set(dich.t) | set(p0.t):
        a, c = dich.t.get(b, [0, 0, 0, 1, 1]), p0.t.get(b, [0, 0, 0, 1, 1])
        lech[b] = [a[0] - c[0], a[1] - c[1], a[2] - c[2], a[3] / (c[3] or 1), a[4] / (c[4] or 1)]
    for i in range(m):
        u = i / float(m)
        w = 1 - u * u * (3 - 2 * u)
        for b, d in lech.items():
            if abs(d[0]) + abs(d[1]) > 1e-6:
                frames[i].move(b, w * d[0], w * d[1])
            if abs(d[2]) > 1e-6:
                frames[i].rot(b, w * d[2])
            if abs(d[3] - 1) + abs(d[4] - 1) > 1e-6:
                frames[i].scale(b, d[3] ** w, d[4] ** w)


def nuong_het(sk, cl):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    ve = soi.Ve(sk)
    for c in cl:
        if not c.loop and c.ten not in ("die", "evolve"):
            hoat.khop_cuoi(fr[c.ten], fr["idle"][0], 0.2)
        if not c.loop and c.ten not in ("appear", "evolve"):
            truoc = soi.lech(ve, fr["idle"][0], fr[c.ten][0])
            khop_dau(fr[c.ten], fr["idle"][0])
            print(f"  vào {c.ten}: khung 0 lệch khung 0 idle {truoc} -> {soi.lech(ve, fr['idle'][0], fr[c.ten][0])}")
    return fr


def so_concept(sk, fr, k, ra):
    """chồng khung 0 idle lên concept: ảnh so và IoU hình bóng."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    a = np.array(Image.open(concept(k)).convert("RGB")).astype(np.float32)
    mn = np.load(os.path.join(d_inbox(k), "manh", "mat_na.npz"))
    bg = mn["nen"]
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
    d = np.abs(r[..., :3].astype(int) - a.astype(int)).max(2)
    khac = int(((d > 40) & ca).sum())
    Image.fromarray(vis).save(ra)
    print(f"  so concept dạng {k}: IoU hình bóng {iou:.4f}; concept có mà rig thiếu {int((m_con & ~m_rig).sum())} px, rig thừa "
          f"{int((m_rig & ~m_con).sum())} px; pixel trong hình lệch màu > 40: {khac} -> {ra}")
    return iou


def rig(k, tien_hoa=None, so_dang=2):
    """dựng, nướng, xuất dạng k vào inbox/phap_su_<k>/rig/. tien_hoa = (sk2, info2, fr2, cl2): gộp dạng sau cho clip evolve."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    sk, info = dung(k)
    cl = clips(sk, info, k)
    fr = nuong_het(sk, cl)
    ra = os.path.join(d_inbox(k), "rig")
    os.makedirs(ra, exist_ok=True)
    so_concept(sk, fr, k, os.path.join(ra, "so_concept.png"))
    ve = soi.Ve(sk)
    cao = soi.chieu_cao(ve, fr["idle"][0], bo=("gay", "vong"))                # chiều cao game: đỉnh mũ, không tính đầu gậy
    ten = f"{CODE}_{k}"
    ch = CHAM[k]
    noi = {}
    M, clM, frM = sk, cl, fr
    if tien_hoa:
        sk2, info2, fr2, cl2 = tien_hoa
        h2 = soi.chieu_cao(soi.Ve(sk2), fr2["idle"][0], bo=("gay", "vong"))
        ti = cao / h2
        M = tienhoa.gop(sk, sk2)
        a0 = float(info["g_goc"])
        S = info["H"] / 456.0

        def gong(t, P):                                                       # dạng cũ: giơ gậy lên cao, gồng, áo choàng phồng
            g = hoat.cv(t, [(0, 0), (0.25, 1, "out"), (1.35, 1)])
            r = hoat.rung(t, 0.3, 1.35, moi=1)
            r3 = hoat.rung(t, 0.3, 1.35, moi=3)
            P.rot("hong", 4 * g)
            P.move("hong", -3 * S * g, (8 * g + 1.0 * r) * S)
            P.rot("nguc", 2 * g)
            P.rot("dau", 5 * g)
            for nm, he in (("ca", -3.5), ("cb", -4.0)):
                for i, bn in enumerate(info[nm]):
                    P.rot(bn, he * g * (0.6 + 0.2 * i) + 0.9 * (r if i % 2 else -r))
            for nm in ("va", "vb", "dt", "dd", "tt"):
                for i, bn in enumerate(info[nm]):
                    P.rot(bn, 1.2 * (r if i % 2 else -r) * (1 + 0.5 * i))
            cs = (1 + 0.3 * g) * (1 + 0.04 * r)
            P.scale("cau", cs, cs)
            info["tay_gay"](P, g, (-16 * g, 62 * g + 3 * r3), a0 + (95 - a0) * g + 1.2 * r)   # tay và gậy như chiêu cuối

        def gam(t, P, fl):                                                    # dạng sau: ưỡn người, cầu nước bừng lên, áo choàng tung
            r = hoat.rung(t, 2.0, 2.4, moi=1)
            P.rot("n_hong", 5 * fl)
            P.scale("n_hong", 1 - 0.02 * fl, 1 + 0.03 * fl)
            P.rot("n_nguc", 3 * fl)
            P.rot("n_dau", 8 * fl)
            for nm, he in (("ca", -3.5), ("cb", -4.0)):
                for i, bn in enumerate(info2[nm]):
                    P.rot("n_" + bn, he * fl * (0.6 + 0.2 * i) + 0.8 * fl * (r if i % 2 else -r))
            for nm in ("va", "vb", "dt", "dd"):
                for i, bn in enumerate(info2[nm]):
                    P.rot("n_" + bn, 1.4 * fl * (r if i % 2 else -r) * (1 + 0.5 * i))
            cs = (1 + 0.28 * fl) * (1 + 0.04 * r * fl)
            P.scale("n_cau", cs, cs)

        memM = cl[1].mem + tienhoa.doi_ten_mem(cl2[1].mem)
        ev = tienhoa.clip_tien_hoa(M, sk, sk2, fr2["idle"][0], tiB=ti, fnA=gong, fnB=gam, mem=memM)
        clM = cl + [ev]
        frM = dict(fr)
        frM["evolve"] = hoat.nuong(M, ev)
        khop_dau(frM["evolve"], fr["idle"][0])
        _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, fr2["idle"][0], ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
        print("  evolve:", noi["evolve"])
    Hh = info["H"]
    tk = xuat.xuat_het(M, clM, ra, ten, f"Pháp sư nước dạng {k}", frames=frM, dang=k, so_dang=so_dang, dung_yen=("attack", "cast", "skill"),
                       cao=cao, khop_idle=0, ma_goc=3313, noi_them=noi,
                       can=[("can_ban", "cast", 20 / 30.0 * ch, "nguc", 0.75 * Hh),
                            ("can_gio_gay", "skill", 14 / 30.0 * ch, "nguc", 0.8 * Hh),
                            ("can_dam", "skill", 32 / 30.0 * ch, "hong", 0.75 * Hh),
                            ("can_xep", "die", 30 / 30.0 * ch, "hong", 0.75 * Hh),
                            ("can_troi", "appear", 15 / 30.0 * ch, "vong", 0.75 * Hh)])
    print(f"dạng {k}: đỉnh {info['dinh']}; cao {cao:.0f} px rig; .atomik {tk['atomik_kb']:.0f} KB -> {ra}")
    return sk, info, fr, cl


def thu(k):
    """dựng rig rồi vẽ dáng gốc có xương, có lưới (chưa có clip): kiểm cắt lớp, khớp xương."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    sk, info = dung(k)
    ra = os.path.join(d_inbox(k), "rig")
    os.makedirs(ra, exist_ok=True)
    ve = soi.Ve(sk)
    P = khung.Pose()
    a = np.array(Image.open(concept(k)).convert("RGB"))
    Hh, Wd = a.shape[:2]
    ox, dat_y = OX[k], float(CFG[k]["dat"])
    box = ((0 - ox) * SC, (dat_y - Hh) * SC, (Wd - ox) * SC, dat_y * SC)
    ve.ve(P, box, 2.0, bg=GRAY, ss=1, xuong=True).save(os.path.join(ra, "thu_xuong.png"))
    ve.ve(P, box, 2.0, bg=GRAY, ss=1, luoi=True).save(os.path.join(ra, "thu_luoi.png"))
    print(f"đỉnh {info['dinh']}; H {info['H']:.0f}; xương {len(sk.bones)}; slot {len(sk.slots)}")


if __name__ == "__main__":
    arg = sys.argv[1:]
    if arg[:1] == ["cat"]:
        for kk in ([int(arg[1])] if len(arg) > 1 else [1]):
            cat(kk)
    elif arg[:1] == ["thu"]:
        thu(int(arg[1]) if len(arg) > 1 else 1)
    elif arg[:1] == ["xem"]:                                               # xem <k> <clip> <khung,khung...> [phóng] [luoi]
        anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
        kk = int(arg[1])
        sk, info = dung(kk)
        cl = {c_.ten: c_ for c_ in clips(sk, info, kk)}[arg[2]]
        fr = hoat.nuong(sk, cl)
        ve = soi.Ve(sk)
        z = float(arg[4]) if len(arg) > 4 else 1.4
        Hh = info["H"]
        box = (-0.95 * Hh, -0.12 * Hh, 1.25 * Hh, 1.25 * Hh)
        ims = [ve.ve(fr[min(len(fr) - 1, int(i))], box, z, bg=GRAY, ss=2, luoi=len(arg) > 5) for i in arg[3].split(",")]
        to = Image.new("RGB", (sum(i.width for i in ims), ims[0].height), GRAY)
        x = 0
        for im in ims:
            to.paste(im.convert("RGB"), (x, 0))
            x += im.width
        out = os.path.join(d_inbox(kk), "rig", f"xem_{arg[2]}.png")
        to.save(out)
        print(out, to.size, len(fr), "khung")
    elif arg[:1] == ["rig"]:
        rig(int(arg[1]), so_dang=int(arg[2]) if len(arg) > 2 else 2)
    elif arg[:1] == ["all"]:
        rig(2)
        sk2, info2 = dung(2, ti=0.6, thua=1.8)                                # bản nhẹ của dạng 2 gộp vào dạng 1
        cl2 = clips(sk2, info2, 2)
        rig(1, tien_hoa=(sk2, info2, nuong_het(sk2, cl2), cl2))
    else:
        print(__doc__)
