# -*- coding: utf-8 -*-
"""Dòng cá đèn lồng (mã tạm `ca_den`, tướng thứ 3 đảo Thủy, 2026-11-11): cắt lớp từ concept đã duyệt, dựng rig, clip.

    py -3 -I ArtGen/Spine/ca_den.py cat 1|2      cắt concept dạng k -> inbox/ca_den_<k>/manh/ (+ manh.json, _soi.png, _nhan.png)
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/ca_den.py rig 1|2    dựng rig một dạng -> inbox/ca_den_<k>/rig/
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/ca_den.py all        dạng 2, rồi dạng 1 gộp bản nhẹ của dạng 2 (clip evolve)

Cách lai, không nhờ GPT vẽ mảnh: mọi lớp cắt thẳng từ concept (khớp concept 100 %), phần bị che tô lại bằng vân sáp chép từ chỗ
sạch cùng màu. Lớp (sau -> trước): chân xa, lòng miệng (tô bằng mã), THÂN (một lưới liền: đầu, lưng, vây lưng, vây bên, chân gần,
đuôi), con ngươi + vành mắt (con ngươi trượt dưới vành), HÀM DƯỚI + bụng kem + răng, CẦN ĐÈN.
Toạ độ trong CFG là pixel concept (1536 x 1024, y xuống). Ghi chú thiết kế, mổ xẻ con gốc: inbox/ca_den_ghichu.md.
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
CODE = "ca_den"
GRAY = (150, 150, 150)
FONT = "C:/Windows/Fonts/arial.ttf"

# màu chuẩn để phân lớp pixel (đo trên concept)
MAU = {"trang": (254, 254, 254), "muc": (45, 25, 6), "cham": (73, 95, 202), "dom": (48, 62, 150), "kem": (251, 238, 203),
       "nga": (254, 250, 236), "tim": (123, 143, 241), "vang": (253, 216, 68)}
MAU_K = {1: MAU, 2: dict(MAU, cham=(61, 75, 176), dom=(40, 50, 128), vang=(253, 195, 43), kem=(251, 237, 198))}   # dạng 2 chàm đậm hơn
TEN = list(MAU)
MUC_RGB = (52, 30, 10)
MIENG_RGB = (176, 64, 98)        # lòng miệng: hồng mận, tô phẳng
HONG_RGB = (112, 34, 66)         # họng: mận sẫm ở giữa lòng miệng
LUOI_RGB = (226, 112, 128)       # lưỡi

# ---------------------------------------------------------------- số đọc trên ảnh kẻ lưới (pixel concept)
CFG = {
    1: {
        "dat": 952,                                   # mặt đất (đáy bàn chân)
        "ban_le": (655, 650), "mui": (1142, 652),     # bản lề miệng (khoé trái) và đầu mút miệng (mép phải)
        # cần đèn: đa giác bao cần + bóng (đáy ở chỗ hai nét mực của cần tắt vào đầu), các khớp dọc cần (gốc -> chụp), tâm bóng
        "den_poly": [(840, 318), (838, 250), (858, 170), (940, 88), (1060, 42), (1180, 44), (1300, 110), (1410, 200), (1410, 425),
                     (1160, 425), (1160, 172), (1100, 150), (1020, 170), (955, 215), (901, 290), (894, 318)],
        "den_khop": [(866, 318), (870, 270), (882, 217), (923, 158), (982, 112), (1048, 83), (1107, 79), (1173, 96), (1223, 133), (1259, 180)],
        "bong": (1273, 296), "chup": (1262, 192),
        "den_goc": [(822, 310), (912, 335)],          # hai điểm trong đầu, hai bên gốc cần: dò lên gặp nét đỉnh đầu
        # đuôi: đa giác bao (ranh phải chạy trong khe trắng rồi theo đường gốc đuôi), khớp gốc -> chóp
        "duoi_poly": [(352, 686), (322, 640), (322, 560), (300, 470), (250, 455), (150, 560), (150, 760), (300, 900), (470, 880), (480, 848)],
        "duoi_goc": [(352, 686), (480, 848)],
        "duoi_khop": [(455, 775), (385, 790), (318, 772), (262, 728), (228, 668), (222, 600), (240, 540), (272, 490)],
        # chân gần (trong lưới thân): đa giác vùng chân, cao độ bắt đầu / hết hoà sang bàn chân
        "chan_g_poly": [(468, 846), (600, 800), (660, 880), (670, 965), (430, 965)],
        "chan_g_y": (858, 905), "ban_g": (555, 905),
        # chân xa (lớp riêng sau bụng)
        "chan_x_hat": (930, 915), "chan_x_y": (868, 905), "ban_x": (935, 905), "chan_x_moc": 80,
        # vây lưng: gốc (giữa chân vây), ngọn; vây bên: gốc (chỗ bám), ngọn
        "vay_lung": [(630, 335), (560, 272), (482, 226)], "vay_lung_chan": [(500, 400), (755, 290)],   # xương gốc -> ngọn; đường chân vây
        "vay_lung_poly": [(395, 440), (395, 160), (790, 160), (790, 285), (700, 295), (600, 330), (520, 380), (470, 440)],
        "vay_ben": [(610, 690), (520, 715), (450, 735)], "vay_ben_poly": [(425, 590), (670, 590), (670, 660), (600, 790), (560, 815), (425, 760)],
        "bung": (880, 760), "hong": (560, 850), "chan_g_x": 700,
        "mat_g": (780, 427), "mat_x": (1065, 420),    # hạt giống: một điểm trong lòng kem từng mắt (gần, xa)
        "mat_g_hat": (720, 450), "mat_x_hat": (1050, 455),
    },
    2: {
        "dat": 985,
        "ban_le": (600, 612), "mui": (1228, 552),
        "den_poly": [(864, 300), (868, 262), (878, 236), (880, 215), (900, 170), (940, 125), (1000, 80), (1095, 36), (1200, 22),
                     (1300, 40), (1380, 95), (1470, 130), (1505, 330), (1440, 455), (1280, 455), (1195, 340), (1200, 250), (1225, 150),
                     (1200, 132), (1121, 140), (1050, 170), (1000, 205), (966, 255), (948, 300)],
        "den_khop": [(905, 300), (912, 255), (926, 210), (974, 147), (1042, 95), (1121, 66), (1200, 58), (1274, 74), (1326, 110), (1350, 158)],
        "bong": (1355, 332), "chup": (1350, 172),
        "den_goc": [(850, 320), (962, 330)],
        "duoi_poly": [(274, 602), (242, 507), (253, 402), (283, 335), (283, 292), (150, 280), (60, 320), (8, 420), (8, 700), (140, 860),
                      (330, 885), (337, 852)],
        "duoi_goc": [(274, 602), (337, 852)],
        "duoi_khop": [(295, 718), (200, 734), (121, 681), (68, 597), (53, 507), (79, 428), (147, 365), (253, 320)],
        "chan_g_poly": [(330, 850), (560, 800), (640, 900), (640, 995), (300, 995)],
        "chan_g_y": (862, 925), "ban_g": (470, 930),
        "chan_x_hat": (1000, 925), "chan_x_y": (890, 930), "ban_x": (1030, 935), "chan_x_moc": 80,
        "vay_lung": [(630, 317), (572, 205), (522, 112)], "vay_lung_chan": [(389, 386), (874, 247)],
        "vay_lung_poly": [(290, 400), (290, 40), (900, 40), (900, 240), (760, 270), (600, 320), (450, 370), (390, 400)],
        "vay_ben": [(575, 620), (480, 650), (395, 690)], "vay_ben_poly": [(360, 530), (610, 530), (610, 600), (545, 720), (480, 790), (360, 740)],
        "bung": (900, 740), "hong": (470, 860), "chan_g_x": 640,
        "mat_g": (858, 434), "mat_x": (1125, 405),
        "mat_g_hat": (763, 410), "mat_x_hat": (1088, 424),
    },
}


def d_inbox(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}")


def concept(k):
    return os.path.join(d_inbox(k), "tai_ve", "L1_duyet.png")


# ---------------------------------------------------------------- công cụ mặt nạ
def moi_nhat(thu_muc, goc):
    """ảnh mới nhất của một bước: M01.png, M01_2.png, M01_3.png... (None nếu chưa có)."""
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


def cum_chua(mask, p):
    """cụm liền của mask chứa điểm p (x, y); không có thì cụm gần nhất."""
    n, lab = cv2.connectedComponents(mask.astype(np.uint8), connectivity=8)
    x, y = int(round(p[0])), int(round(p[1]))
    if lab[y, x] == 0:
        ys, xs = np.nonzero(mask)
        i = int(np.argmin((xs - x) ** 2 + (ys - y) ** 2))
        x, y = int(xs[i]), int(ys[i])
    return lab == lab[y, x]


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


def mem_alpha(m, trong=2, sigma=0.7):
    """độ đậm mép mềm: trong hình (co `trong` px) = 1, mép làm mờ nhẹ."""
    return np.where(co(m, trong), 1.0, cv2.GaussianBlur(m.astype(np.float32), (0, 0), sigma))


def luu(a, alpha, box, path):
    x0, y0, x1, y1 = box
    rgba = np.dstack([np.clip(a[y0:y1, x0:x1], 0, 255).astype(np.uint8), (np.clip(alpha[y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8)])
    Image.fromarray(rgba, "RGBA").save(path)


def phan_lop(a, mau=None):
    """nhãn màu từng pixel (chỉ số trong TEN): gần màu chuẩn nào nhất trên ảnh làm mờ nhẹ, rồi lọc đa số 5x5."""
    b = cv2.GaussianBlur(a.astype(np.float32), (0, 0), 1.6)
    mau = mau or MAU
    C = np.array([mau[t] for t in TEN], np.float32)
    d = ((b[:, :, None, :] - C[None, None]) ** 2).sum(3)
    # mép mực / kem pha ra màu nâu xám, gần "chàm" hơn mọi màu chuẩn: chỉ cho nhận màu lam khi thật sự ngả lam
    khong_lam = (b[..., 2] - b[..., 0]) < 45
    for t in ("cham", "dom", "tim"):
        d[..., TEN.index(t)][khong_lam] = 1e12
    lab = d.argmin(2).astype(np.uint8)
    return cv2.medianBlur(lab, 5)


def o_van(a, sach, co_o=96, chong=20):
    """ô vân sáp lát liền được: lấy ô vuông sạch lớn nhất trong mặt nạ `sach`, hoà chéo hai mép để lát không lộ đường nối."""
    dt = cv2.distanceTransform(sach.astype(np.uint8), cv2.DIST_C, 3)
    y, x = np.unravel_index(int(dt.argmax()), dt.shape)
    r = int(dt[y, x]) - 1
    p = min(co_o + chong, 2 * r)
    if p < 40:
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
    """lát ô vân kín cả khung."""
    h, w = shape[:2]
    n = o.shape[0]
    return np.tile(o, (h // n + 1, w // n + 1, 1))[:h, :w]


def to_lai(a, vung, van, mem=2.0):
    """tô lại vùng bằng tấm vân đã lát, mép hoà `mem` px."""
    m = cv2.GaussianBlur(vung.astype(np.float32), (0, 0), mem)[..., None] if mem > 0 else vung.astype(np.float32)[..., None]
    m = np.maximum(m, vung[..., None].astype(np.float32))
    return a * (1 - m) + van * m


def net_muc(a, pts, day=13.0, kin=False):
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


# ---------------------------------------------------------------- cắt lớp
def cat(k):
    c = CFG[k]
    src = concept(k)
    if not os.path.exists(src):
        raise SystemExit("chưa có " + src)
    a = np.array(Image.open(src).convert("RGB")).astype(np.float32)
    H, Wd = a.shape[:2]
    bg = nen_trang(a)
    fg = lap_lo(~bg & ~co(gian(bg, 1), 0) | ~bg)
    fg = ~bg
    L = phan_lop(a, MAU_K[k])
    L[bg] = TEN.index("trang")
    ix = {t: i for i, t in enumerate(TEN)}
    muc = (L == ix["muc"]) & fg
    kem = ((L == ix["kem"]) | (L == ix["nga"])) & fg
    cham = ((L == ix["cham"]) | (L == ix["dom"])) & fg
    ra = os.path.join(d_inbox(k), "manh")
    os.makedirs(ra, exist_ok=True)

    # ảnh nhãn để soi
    pal = np.array([(255, 255, 255), (40, 20, 5), (70, 95, 205), (20, 30, 120), (250, 225, 150), (255, 120, 120), (150, 230, 160), (255, 200, 0)], np.uint8)
    Image.fromarray(pal[L]).save(os.path.join(ra, "_nhan.png"))

    def kc(m):
        """khoảng cách (px) từ mọi pixel tới mặt nạ m."""
        return cv2.distanceTransform((~m).astype(np.uint8), cv2.DIST_L2, 5)

    info = {"concept": os.path.basename(src), "cỡ": [Wd, H], "manh": {}}
    DAY = 15                                                                  # bề dày nét mực (px) + dư

    # ---- các vùng màu chính
    bung = cum_chua(kem, c["bung"])                                           # bụng + hàm dưới kem
    rang = np.zeros_like(fg)
    for q in cum((L == ix["nga"]) & fg, 400):                                 # răng: cụm ngà nằm sát mép trên bụng
        if kc(bung)[q["m"]].min() < 2 * DAY and q["y1"] < max(c["ban_le"][1], c["mui"][1]) + 30:
            rang |= q["m"]
    mat_kem = {s: cum_chua(kem & ~bung, c[f"mat_{s}_hat"]) for s in "gx"}
    xs = np.arange(Wd)[None, :].repeat(H, 0)
    ys = np.arange(H)[:, None].repeat(Wd, 1)
    o_chan = (np.abs(xs - c["ban_x"][0]) < 175) & (ys > c["chan_x_y"][0] - 16)
    chan_x = (cham | ((L == ix["nga"]) & fg & ~rang & ~gian(bg, 3))) & ~bung & o_chan
    chan_x = lap_lo(chan_x | (muc & o_chan & (kc(chan_x) <= DAY) & (kc(bung) > DAY))) & ~(muc & (kc(bung) <= DAY))
    den = fg & da_giac(a.shape, c["den_poly"])
    vang = (L == ix["vang"]) & fg

    # ---- con ngươi: khối mực dày (nét mực co 9 px là mất, con ngươi còn)
    loi = co(muc, 9)
    nguoi, nguoi_fit = {}, {}
    for s in "gx":
        q = cum_chua(loi, c[f"mat_{s}"]) if loi.any() else None
        d_gan = kc(mat_kem[s])
        best, bd = None, 1e9
        for cc in cum(loi, 60):
            dd = float(d_gan[cc["m"]].min())
            if dd < bd:
                best, bd = cc["m"], dd
        pm = gian(best, 10) & muc                                             # phía mí / viền mắt lấn 1 px vào nét mực: không sao
        cham_sang = np.zeros_like(fg)                                         # chấm sáng: cụm sáng nhỏ nằm trong mực, sát con ngươi
        for cc in cum(fg & ~muc & ~kem & ~cham & gian(pm, 14), 20):
            if cc["dt"] < 1500:
                cham_sang |= cc["m"]
        for cc in cum(kem & ~bung & ~mat_kem[s] & gian(pm, 14), 20):
            if cc["dt"] < 1500:
                cham_sang |= cc["m"]
        pm = pm | cham_sang | (gian(cham_sang, 16) & muc)
        cau_truc = muc & (kc(cham | bg | ((L == ix["tim"]) & fg)) <= DAY - 1)   # nét viền, mí (sát chàm / nền): không thuộc con ngươi
        nguoi[s] = lap_lo(cum_chua(pm & ~cau_truc, np.argwhere(best)[0][::-1]))   # lấp chấm sáng trong con ngươi
        nguoi_fit[s] = gian(best, 10) & muc & ~cau_truc
    cua = {s: lap_lo(cv2.morphologyEx((mat_kem[s] | nguoi[s]).astype(np.uint8), cv2.MORPH_CLOSE, _k(2)) > 0) for s in "gx"}

    # ---- vân sáp từng màu
    sach_cham = co((L == ix["cham"]) & fg, 6)
    sach_kem = co(bung, 8)
    van_cham = lat(a.shape, o_van(a, sach_cham))
    van_kem = lat(a.shape, o_van(a, sach_kem))
    tb_kem = van_kem.reshape(-1, 3).mean(0)

    # ================= THÂN (một lưới liền) =================
    tm = a.copy()
    M0 = (cham | ((L == ix["tim"]) & fg) | mat_kem["g"] | mat_kem["x"] | nguoi["g"] | nguoi["x"]
          | (fg & ~muc & ~gian(bg, 6))) & ~bung & ~rang & ~chan_x & ~den
    than = (M0 | (muc & (kc(M0) <= DAY))) & fg & ~den
    # răng: lòng răng và hai nét cạnh răng thuộc hàm; ở lớp thân tô lại thành môi trên màu chàm (nét miệng giữ)
    net_mieng = muc & (kc(bung) <= DAY)
    canh_rang = muc & (kc(rang) <= DAY + 1) & ~net_mieng & (kc(rang) < kc(mat_kem["g"] | nguoi["g"] | mat_kem["x"] | nguoi["x"]))
    dau_kin = cv2.morphologyEx((cham | ((L == ix["tim"]) & fg) | (muc & (kc(cham) <= DAY))).astype(np.uint8), cv2.MORPH_CLOSE,
                               cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (231, 91))) > 0
    lo_rang = gian(lap_lo(canh_rang | net_mieng | rang) & ~net_mieng, 3) & ~co(net_mieng, 1) & ~bung & dau_kin
    tm = to_lai(tm, lo_rang, van_cham, mem=1.0)
    than |= lo_rang
    than &= ~(gian(rang | canh_rang, 2) & ~lo_rang & ~net_mieng)              # răng chìa ra ngoài viền đầu: lớp thân không giữ nét răng
    # gốc cần đèn: dưới đường đỉnh đầu tô chàm, kẻ lại nét đỉnh đầu; trên đường đó bỏ trống
    pts = []
    for (x, y0) in c["den_goc"]:
        y = y0
        while y > 0 and not muc[y, x]:
            y -= 1
        y1 = y
        while y1 > 0 and muc[y1, x]:
            y1 -= 1
        pts.append((x, (y + y1 + 1) / 2.0))
    (xa, ya), (xb, yb) = pts
    duoi_dg = np.zeros_like(fg)                                              # phần của vùng cần đèn nằm dưới đường đỉnh đầu
    y_dg = ya + (yb - ya) * (xs - xa) / (xb - xa)
    trong_goc = da_giac(a.shape, [(xa - 2, ya - 30), (xb + 2, yb - 30), (xb + 2, yb + 60), (xa - 2, ya + 60)])
    duoi_dg = trong_goc & (ys > y_dg - 2) & (gian(den, 3) | lap_lo(than | den))
    tm = to_lai(tm, duoi_dg & gian(den, 4), van_cham)
    than = (than | (duoi_dg & gian(den, 4))) & ~(trong_goc & (ys < y_dg - DAY / 2 - 1) & gian(den, 4))
    tm, nm = net_muc(tm, [(xa - 6, ya - 0.5), ((xa + xb) / 2, (ya + yb) / 2 - 2.5), (xb + 6, yb + 0.5)], day=13)
    than |= nm
    # tròng mắt sạch (con ngươi là lớp riêng trượt bên dưới vành mắt); vành mắt lấy từ bản chưa xoá con ngươi
    tm_truoc = tm.copy()
    for s in "gx":
        tm = to_lai(tm, gian(nguoi[s], 2) & cua[s], van_kem, mem=0.8)
    # dải mọc thêm dưới hàm dọc sườn trái (bụng phình co không lộ nền)
    moc = gian(than, 34) & bung & da_giac(a.shape, [(0, c["ban_le"][1] + 14), (c["ban_le"][0] + 70, c["ban_le"][1] + 14),
                                                    (c["ban_le"][0] + 70, c["chan_g_y"][0] - 4), (0, c["chan_g_y"][0] - 4)])
    tm = to_lai(tm, moc & ~gian(than, 1), van_cham, mem=0)
    than |= moc
    soi_ = than & ~(cv2.morphologyEx(than.astype(np.uint8), cv2.MORPH_OPEN, _k(2)) > 0) & ~muc & (kc(bung) <= DAY + 4)
    than &= ~soi_                                                             # sợi mảnh (mép sáng) dọc viền bụng
    sot = fg & (muc | cham | ((L == ix["tim"]) & fg)) & ~than & ~den & ~chan_x & ~(muc & (kc(bung | rang | chan_x) <= DAY)) & (kc(than) <= 25)
    than |= sot                                                               # chóp vây, gai đuôi: mực cách màu nền hơi xa
    lo = lap_lo(than) & ~than                                                 # chỉ lấp lỗ nhỏ (vệt sáng của nét sáp), không lấp bụng
    for cc in cum(lo, 1):
        if cc["dt"] < 2500:
            than |= cc["m"]

    # ================= HÀM DƯỚI + bụng + răng =================
    ham = (bung | rang | (muc & (kc(bung | rang) <= DAY) & (kc(bung | rang) < kc(mat_kem["g"] | nguoi["g"] | mat_kem["x"] | nguoi["x"])))) & fg
    ham = (cv2.morphologyEx(ham.astype(np.uint8), cv2.MORPH_CLOSE, _k(3)) > 0) & fg     # khe mép ngà / kem sát nét mực
    for cc in cum(lap_lo(ham) & ~ham, 1):
        if cc["dt"] < 600:
            ham |= cc["m"]

    # ================= CHÂN XA (sau bụng), mọc thêm lên trên =================
    cx = (chan_x | (muc & (kc(chan_x) <= DAY) & (kc(chan_x) <= kc(M0)))) & fg
    tc = a.copy()
    yb0, yb1 = c["chan_x_y"]
    them = np.zeros_like(fg)                                                  # mọc thêm: đùn từng cột chỗ chân chạm đáy bụng lên trên
    ham_tam = bung | (muc & (kc(bung) <= DAY))
    for x in np.nonzero(cx.any(0))[0]:
        yt = int(np.nonzero(cx[:, x])[0].min())
        if yt > 3 and ham_tam[yt - 2, x] and yt < yb1:
            them[max(0, yt - c["chan_x_moc"]):yt + 10, x] = True
    them = co(gian(them, 3), 3) & lap_lo(than | ham_tam | gian(bung, DAY))
    tc = to_lai(tc, them, van_cham, mem=0)
    cx2 = cx | them

    # ================= CẦN ĐÈN =================
    al_den = mem_alpha(den)
    yy0 = max(pts[0][1], pts[1][1])
    al_den = np.where(xs < xb + 12, al_den * np.clip((c["den_poly"][0][1] - ys) / 10.0, 0, 1), al_den)   # đáy cần mờ dần vào đầu

    # ================= LÒNG MIỆNG (tô bằng mã) =================
    bl, mui = np.array(c["ban_le"], float), np.array(c["mui"], float)
    dinh_bung = np.where(bung.any(0), bung.argmax(0), H + 99)                 # mép trên bụng kem theo từng cột = đường miệng
    net_tren = net_mieng & (ys <= dinh_bung[None, :] + 3) & (xs > bl[0] - 5)   # nét miệng (ranh chàm / kem), không lẫn nét đáy bụng
    sau = kc(net_tren)
    long_m = ((gian(net_tren, 34) & lap_lo(than | ham)) | ((bung | (muc & (kc(bung) <= DAY))) & (sau <= 170))) & (xs > bl[0] + 6) & fg
    long_m = cum_chua(co(long_m, 2), ((bl + mui) / 2 + (0, 30)))
    chi_tiet = (van_kem - tb_kem[None, None]) / 255.0
    tl = np.array(MIENG_RGB, np.float32)[None, None] * (1 + 1.6 * chi_tiet)
    vien_ngoai = muc & (kc(bg) <= DAY) & long_m                               # nét viền mép phải giữ nguyên
    tl = np.where(vien_ngoai[..., None], a, tl)
    long_m &= than | (ys > dinh_bung[None, :] - 9)                            # trên đường miệng chỉ giữ phần nấp sau môi (lớp thân)
    Lmc = float(np.hypot(*(mui - bl)))
    hx = float(bl[0] + 0.56 * (mui[0] - bl[0]))                               # họng: bầu dục sẫm giữa lòng miệng (há ra thì giãn thành hốc tối)
    hong_m = np.zeros(a.shape[:2], np.uint8)
    cv2.ellipse(hong_m, (int(hx), int(dinh_bung[int(hx)] + 30)), (int(0.27 * Lmc), 34), -3, 0, 360, 1, -1)
    hong_m = cv2.GaussianBlur(hong_m.astype(np.float32), (0, 0), 2.0)[..., None]
    tl = tl * (1 - hong_m) + np.array(HONG_RGB, np.float32)[None, None] * (1 + 1.6 * chi_tiet) * hong_m
    long_m &= ~((kc(bg) < 18) & (sau > 95))                                  # phần sâu (luôn khuất sau hàm) lùi vào trong viền
    tl = np.where((long_m & ~vien_ngoai)[..., None], tl, np.where(vien_ngoai[..., None], a, tl))
    # lưỡi: u hồng nằm ngay trên vành hàm, sau môi trên (khép miệng thì khuất), đi theo hàm
    lx = float(bl[0] + 0.58 * (mui[0] - bl[0]))
    ly = float(dinh_bung[int(lx)] - 6)
    luoi_m = np.zeros(a.shape[:2], np.uint8)
    cv2.ellipse(luoi_m, (int(lx), int(ly + 26)), (int(0.30 * Lmc), 86), -2, 0, 360, 1, -1)
    luoi_m = (luoi_m > 0) & (ys < y_dg * 0 + ly + 40)
    tluoi = np.array(LUOI_RGB, np.float32)[None, None] * (1 + 1.6 * chi_tiet)
    cnts, _ = cv2.findContours(luoi_m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cc = max(cnts, key=len)[:, 0, :].astype(float)
    cc = cc[cc[:, 1] < ly + 36]
    cc = cc[np.argsort(cc[:, 0])][::16]
    tluoi, nm_l = net_muc(tluoi, cc.tolist(), day=11)
    luoi_m |= nm_l
    tluoi, nm_l = net_muc(tluoi, [(lx + 4, ly - 52), (lx + 1, ly - 24), (lx + 3, ly + 8)], day=6)
    # hàng răng trên: răng ngà nhọn chĩa xuống, chân răng nấp sau môi trên, thân răng nấp sau hàm lúc khép; xen kẽ với răng dưới
    rd = sorted([[q["x0"], q["x1"]] for q in cum(rang, 300)])
    tam_r = [0.5 * (rd[i][1] + rd[i + 1][0]) for i in range(len(rd) - 1) if rd[i + 1][0] - rd[i][1] > 0.05 * Lmc]
    if rd and rd[0][0] - bl[0] > 0.16 * Lmc:
        tam_r.insert(0, rd[0][0] - 0.07 * Lmc)
    if rd and mui[0] - rd[-1][1] > 0.13 * Lmc:
        tam_r.append(rd[-1][1] + 0.06 * Lmc)
    rt_m = np.zeros(a.shape[:2], bool)
    trt = np.array(MAU["nga"], np.float32)[None, None] * (1 + 1.2 * chi_tiet)
    hb, hh = 0.043 * Lmc, 0.115 * Lmc
    for cx_ in tam_r:
        ym = float(dinh_bung[int(cx_)] - 6)
        poly = [(cx_ - hb, ym - 14), (cx_ - 0.55 * hb, ym + 0.45 * hh), (cx_ + 2, ym + hh), (cx_ + 0.6 * hb, ym + 0.45 * hh), (cx_ + hb, ym - 14)]
        rt_m |= da_giac(a.shape, poly)
        trt, nm_r = net_muc(trt, poly, day=10)
        rt_m |= nm_r

    # má bên kia: dải da ở đầu mút miệng (mép phải), nằm trước lòng miệng, sau lớp thân và lớp hàm. Lúc khép nấp hết sau môi và
    # hàm; lúc há thì giãn ra giữa đầu môi trên và đầu vành hàm, bịt mép phải của hốc miệng: nhìn thấy MÁ (chàm ở trên, kem ở
    # dưới, có nét mực mép trong) chứ không phải thịt đỏ chạy ra tới viền (người dùng dặn 2026-11-11, theo con gốc)
    W_ma = 0.29 * Lmc
    cot_ok = np.nonzero(dinh_bung < H)[0]
    ym_cot = np.interp(np.arange(Wd), cot_ok, dinh_bung[cot_ok] - 6.0)        # đường miệng theo cột, kéo dài ra ngoài mép bụng
    sau_ma = ys - ym_cot[None, :]
    than_ham = fg & ~den
    xr_hang = np.where(than_ham.any(1), Wd - 1 - than_ham[:, ::-1].argmax(1), 0)          # mép phải của con theo từng hàng
    tau = np.clip((sau_ma + 5) / 90.0, 0, 1)
    rong = W_ma * (0.62 + 0.38 * (2 * tau - 1) ** 2)                            # dải rộng ở hai đầu, hẹp ở giữa: mép trong cong
    ma_m = than_ham & (xs > xr_hang[:, None] - rong) & (sau_ma > -30) & (sau_ma < 112) & (xs > mui[0] - 1.6 * W_ma)
    ma_m = cum_chua(ma_m, (mui[0] - 12, mui[1] + 8))
    RANH = 56.0                                                               # trên ranh này là má chàm, dưới là môi dưới kem
    tma = np.where((sau_ma < RANH)[..., None], van_cham, van_kem).astype(np.float32)
    vien_ma = muc & (kc(bg) <= DAY) & ma_m
    tma = np.where(vien_ma[..., None], a, tma)
    xs_r = np.arange(int(mui[0] - 1.6 * W_ma), Wd)
    ranh = [(float(x), float(ym_cot[x] + RANH)) for x in xs_r[::14] if ma_m[int(min(H - 1, ym_cot[x] + RANH)), x]]
    if len(ranh) > 1:
        tma, _ = net_muc(tma, ranh, day=5)
    trong_ = []
    for y in range(H):
        r_ = np.nonzero(ma_m[y])[0]
        if len(r_) and -10 < sau_ma[y, r_[0]] < 98:
            trong_.append((float(r_[0]), float(y)))
    if len(trong_) > 6:
        tma, nm_m = net_muc(tma, trong_[::10] + [trong_[-1]], day=10)
        ma_m |= nm_m & than_ham

    # ================= CON NGƯƠI =================
    nguoi_info = {}
    tn = {}
    for s in "gx":
        vien = (nguoi_fit[s] & gian(mat_kem[s], 2)).astype(np.uint8)
        p = np.argwhere(vien)[:, ::-1].astype(np.float32)
        (ex, ey), (ea, eb), eg = cv2.fitEllipse(p)
        E = np.zeros(a.shape[:2], np.uint8)
        cv2.ellipse(E, ((ex, ey), (ea + 2, eb + 2), eg), 255, -1, cv2.LINE_AA)
        mau = np.median(a[co(nguoi[s], 4) & (L == ix["muc"])], 0)
        rng = np.random.default_rng(3)
        im = np.ones_like(a) * mau[None, None] + rng.normal(0, 1.2, a.shape[:2])[..., None]
        giu = co(nguoi[s], 1)
        im = np.where(giu[..., None], a, im)
        tn[s] = (im, E.astype(np.float32) / 255 * mem_alpha(co(lap_lo(than), 3)))   # mắt xa: con ngươi không thò ra ngoài viền đầu
        phu = float((nguoi[s] & (E > 127)).sum()) / max(1, int(nguoi[s].sum()))
        nguoi_info[s] = {"tam": [float(ex), float(ey)], "truc": [float(ea), float(eb)], "goc": float(eg), "phu": round(phu, 3)}
    # ---- vành mắt: mọi thứ quanh cửa mắt (viền, mí) lấy từ thân chưa xoá con ngươi; rộng đủ che con ngươi khi nó trượt
    vanh = {}
    for s in "gx":
        E = tn[s][1] > 0.02
        ngoai = gian(cua[s], 17) | gian(E, 16)
        v = ngoai & ~cua[s] & than
        al = np.clip(kc(~ngoai) / 5.0, 0, 1) * v * np.clip(kc(cua[s]) / 1.0, 0, 1) * mem_alpha(than)
        vanh[s] = (v, al)

    # ================= lưu =================
    def ghi(ten, img, alpha, m):
        box = hop(m if m.dtype == bool else m > 0.02)
        luu(img, alpha, box, os.path.join(ra, ten + ".png"))
        info["manh"][ten] = box

    ghi("chan_xa", tc, mem_alpha(cx2), cx2)
    ghi("mieng", tl, mem_alpha(long_m), long_m)
    ghi("luoi", tluoi, mem_alpha(luoi_m), luoi_m)
    ghi("rang_tren", trt, mem_alpha(rt_m), rt_m)
    ghi("ma_xa", tma, mem_alpha(ma_m), ma_m)
    ghi("than", tm, mem_alpha(than), than)
    for s in "gx":
        ghi(f"nguoi_{s}", tn[s][0], tn[s][1], tn[s][1] > 0.02)
        ghi(f"vanh_{s}", tm_truoc, vanh[s][1], vanh[s][0])
    ghi("ham", a, mem_alpha(ham), ham)
    ghi("den", a, al_den, den)
    info["nguoi"] = nguoi_info
    info["cua"] = {s: hop(cua[s], 0) for s in "gx"}
    info["dinh_dau"] = [[float(xa), float(ya)], [float(xb), float(yb)]]
    info["bung"] = hop(bung, 0)
    info["rang"] = [[q["x0"], q["y0"], q["x1"], q["y1"]] for q in sorted(cum(rang, 300), key=lambda q: q["x0"])]
    # đường miệng (mép trên bụng kem) lấy mẫu theo x: để tính độ sâu dưới miệng khi chia trọng số
    dm = []
    for x in range(int(bl[0]), int(mui[0]) + 1, 6):
        if dinh_bung[x] < H:
            dm.append([x, float(dinh_bung[x] - 6)])
    info["duong_mieng"] = dm
    them_npz = {}
    f_ha = moi_nhat(os.path.join(d_inbox(k), "tai_ve"), "M01")
    if f_ha:
        # ---- HÌNH HÁ MIỆNG (GPT vẽ lại đúng concept, chỉ đổi miệng; đã đo: lệch concept dưới 0,4 px nên không cần khớp lại).
        # Mảnh `ha` = hốc miệng + răng + hàm dưới và bụng kem (đặc) + vành môi, má quanh hốc (mờ dần vào da chàm của lớp thân).
        # Lúc há thì hiện mảnh này (trên lớp thân, dưới mắt), tắt lớp hàm và các lớp lòng miệng của bản khép: đổi ảnh như con gốc.
        b = np.array(Image.open(f_ha).convert("RGB")).astype(np.float32)
        bgb = nen_trang(b)
        fgb = ~bgb
        bb = cv2.GaussianBlur(b, (0, 0), 1.6)
        hong = ((bb[..., 0] - bb[..., 1]) > 55) & (bb[..., 2] > 45) & fgb     # thịt hồng: lòng miệng, họng, lưỡi
        hong = cum_chua(cv2.morphologyEx(hong.astype(np.uint8), cv2.MORPH_CLOSE, _k(4)) > 0, (c["bung"][0], c["bung"][1] - 60))
        Lb = phan_lop(b, MAU_K[k])
        Lb[bgb] = TEN.index("trang")
        mucb = (Lb == ix["muc"]) & fgb & ~hong
        kemb = ((Lb == ix["kem"]) | (Lb == ix["nga"])) & fgb & ~hong
        chamb = ((Lb == ix["cham"]) | (Lb == ix["dom"])) & fgb & ~hong
        bung_b = cum_chua(kemb, (c["bung"][0], c["bung"][1] + 70))
        rang_b = np.zeros_like(fgb)
        for q in cum(kemb & ~bung_b, 150):                                    # răng: cụm ngà sát hốc miệng
            if kc(hong)[q["m"]].min() < DAY + 3 and q["dt"] < 30000:
                rang_b |= q["m"]
        hoc = lap_lo(cv2.morphologyEx((hong | rang_b | (mucb & (kc(hong | rang_b) <= DAY) & (kc(bung_b) > 3))).astype(np.uint8),
                                      cv2.MORPH_CLOSE, _k(5)) > 0)
        loi_ha = lap_lo(hoc | bung_b | (mucb & (kc(hoc | bung_b) <= DAY)))    # phần đặc: hốc miệng, răng, hàm + bụng kem, nét mực của chúng
        d_hoc = kc(hoc)
        vanh_ha = fgb & ~loi_ha & (d_hoc <= 50) & ~gian(den, 2)               # vành môi, má quanh hốc
        al_vanh = np.clip((50 - d_hoc) / 24.0, 0, 1)
        phai = xs > (np.nonzero(hoc.any(0))[0].max() - 24)                    # má bên kia: giữ đặc ra tới viền
        rong_h = float(np.nonzero(hoc.any(0))[0].max() - np.nonzero(hoc.any(0))[0].min())
        al_vanh = np.where(phai & (d_hoc <= 0.27 * rong_h) & fgb & ~loi_ha & ~gian(den, 2), 1.0, al_vanh * vanh_ha)
        y_day_hoc = int(np.nonzero(hoc.any(1))[0].max())
        thieu = fgb & ~than & ~loi_ha & (d_hoc <= 0.35 * rong_h) & ~gian(den, 2) & (ys < y_day_hoc)   # chỗ lớp thân khép bị khuyết (răng nanh chìa ra)
        al_vanh = np.where(gian(thieu, 9) & fgb & ~loi_ha & ~gian(den, 2), 1.0, al_vanh)
        al_ha = np.maximum(mem_alpha(loi_ha), al_vanh * mem_alpha(fgb))
        m_ha = al_ha > 0.02
        box = hop(m_ha)
        luu(b, al_ha, box, os.path.join(ra, "ha.png"))
        info["manh"]["ha"] = box
        cot_h = np.nonzero(hoc.any(0))[0]
        y_moi = hoc.argmax(0).astype(float)
        y_vanh = (H - 1 - hoc[::-1].argmax(0)).astype(float)
        info["ha"] = {"anh": os.path.basename(f_ha), "x0": int(cot_h.min()), "x1": int(cot_h.max()),
                      "moi": [float(v) for v in y_moi[cot_h.min():cot_h.max() + 1]],
                      "vanh": [float(v) for v in y_vanh[cot_h.min():cot_h.max() + 1]],
                      "tam": [float(cot_h.mean()), float(np.nonzero(hoc.any(1))[0].mean())]}
        giua_h = 0.5 * (y_moi + y_vanh)
        rd_ = np.zeros_like(fgb)
        rt_ = np.zeros_like(fgb)
        for q in cum(rang_b, 100):
            yy, xx = np.nonzero(q["m"])
            (rd_ if yy.mean() > giua_h[int(xx.mean())] else rt_)[q["m"]] = True
        luoi_b = hong & ((bb[..., 0] > 205) & (bb[..., 1] > 85))              # lưỡi (hồng sáng): theo hàm
        them_npz = {"ha_hoc": hoc, "ha_rang_duoi": gian(rd_, 9) & hoc, "ha_rang_tren": gian(rt_, 9) & hoc, "ha_luoi": gian(luoi_b, 6) & hoc,
                    "ha_bung": bung_b}
        # tờ soi: bản khép và bản há (đổi ảnh) cạnh nhau
        im_ha = Image.new("RGBA", (Wd, H), GRAY + (255,))
        for ten in ("chan_xa", "than", "ha", "nguoi_g", "nguoi_x", "vanh_g", "vanh_x", "den"):
            if ten == "ha":
                im_ha.alpha_composite(Image.open(os.path.join(ra, "ha.png")), (box[0], box[1]))
            else:
                x0_, y0_ = info["manh"][ten][:2]
                im_ha.alpha_composite(Image.open(os.path.join(ra, ten + ".png")), (x0_, y0_))
        im_ha.convert("RGB").save(os.path.join(ra, "_soi_ha.png"))
        dd_ = np.abs(np.array(im_ha.convert("RGB")).astype(int) - np.where(bgb[..., None], np.array(GRAY), b).astype(int)).max(2)
        print(f"  há miệng ({os.path.basename(f_ha)}): mảnh ha {box[2] - box[0]}x{box[3] - box[1]}, răng trên {len(cum(rt_, 100))}, răng dưới "
              f"{len(cum(rd_, 100))}; ghép (thân khép + mảnh há) khác ảnh GPT > 60: {int((dd_ > 60).sum())} px")
    json.dump(info, open(os.path.join(ra, "manh.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    np.savez_compressed(os.path.join(ra, "mat_na.npz"), than=than, ham=ham, den=den, chan_xa=cx2, mieng=long_m, bung=bung, rang=rang,
                        vay_tim=(L == ix["tim"]) & fg, cua_g=cua["g"], cua_x=cua["x"], **them_npz)

    # ================= tờ soi =================
    THU_TU = ["chan_xa", "mieng", "luoi", "rang_tren", "ma_xa", "than", "nguoi_g", "nguoi_x", "vanh_g", "vanh_x", "ham", "den"]

    def ghep(lech=None, bo=()):
        im = Image.new("RGBA", (Wd, H), GRAY + (255,))
        for ten in THU_TU:
            if ten in bo:
                continue
            p = Image.open(os.path.join(ra, ten + ".png"))
            x0, y0 = info["manh"][ten][:2]
            dx, dy = (lech or {}).get(ten, (0, 0))
            im.alpha_composite(p, (x0 + dx, max(0, y0 + dy)))
        return im

    t_ghep = ghep()
    t_goc = Image.new("RGBA", (Wd, H), GRAY + (255,))
    t_goc.alpha_composite(Image.fromarray(np.dstack([a.astype(np.uint8), np.where(bg, 0, 255).astype(np.uint8)]), "RGBA"))
    d = np.abs(np.array(t_ghep.convert("RGB")).astype(int) - np.array(t_goc.convert("RGB")).astype(int)).max(2)
    t_khac = Image.fromarray(np.dstack([np.clip(d * 4, 0, 255)] * 3).astype(np.uint8)).convert("RGBA")
    t_bung = ghep({"ham": (40, 60), "den": (0, -30), "nguoi_g": (-22, 14), "nguoi_x": (-14, 10), "chan_xa": (0, 40)})
    t_than = ghep(bo=("ham", "den", "nguoi_g", "nguoi_x", "vanh_g", "vanh_x", "mieng", "chan_xa"))
    t_mieng = ghep(bo=("ham", "than", "nguoi_g", "nguoi_x", "vanh_g", "vanh_x", "den"))
    t_mieng.convert("RGB").save(os.path.join(ra, "_soi_mieng.png"))
    o = [(t_ghep, "1. ghép lại"), (t_goc, "2. concept"), (t_khac, "3. khác nhau giữa 1 và 2 (x4)"),
         (t_bung, "4. tách: hàm lệch (40, 60), đèn lên 30, con ngươi lệch, chân xa xuống 40"), (t_than, "5. riêng lớp thân"),
         (t_mieng, "6. lòng miệng + chân xa")]
    to = Image.new("RGBA", (Wd // 2 * 3, H // 2 * 2), (60, 60, 60, 255))
    for i, (im, chu) in enumerate(o):
        sm = im.resize((Wd // 2, H // 2), Image.LANCZOS)
        ImageDraw.Draw(sm).text((12, 8), chu, fill=(255, 255, 255, 255), font=ImageFont.truetype(FONT, 20))
        to.alpha_composite(sm, ((i % 3) * (Wd // 2), (i // 3) * (H // 2)))
    to.convert("RGB").save(os.path.join(ra, "_soi.png"))
    t_bung.convert("RGB").save(os.path.join(ra, "_soi_tach.png"))
    for ten, (x0, y0, x1, y1) in (("mat", (640, 250, 1200, 700)), ("goc_den", (760, 200, 1000, 400))):
        pair = Image.new("RGB", ((x1 - x0) * 4, (y1 - y0) * 2))
        pair.paste(t_ghep.convert("RGB").crop((x0, y0, x1, y1)).resize(((x1 - x0) * 2, (y1 - y0) * 2), Image.LANCZOS), (0, 0))
        pair.paste(t_than.convert("RGB").crop((x0, y0, x1, y1)).resize(((x1 - x0) * 2, (y1 - y0) * 2), Image.LANCZOS), ((x1 - x0) * 2, 0))
        pair.save(os.path.join(ra, f"_can_{ten}.png"))
    thieu = int(((np.array(t_ghep.convert("RGB")).astype(int) - np.array(GRAY)).__abs__().max(2) < 8)[~bg & ~gian(bg, 3)].sum())
    print(f"  pixel có hình trong concept mà ghép lại bị trống: {thieu}")
    t_than.convert("RGB").save(os.path.join(ra, "_soi_than.png"))
    print(f"dạng {k}: " + ", ".join(f"{t} {b[2] - b[0]}x{b[3] - b[1]}" for t, b in info["manh"].items()))
    print(f"  con ngươi: {nguoi_info}; răng {len(info['rang'])}; khác concept tối đa {int(d.max())}, {int((d > 24).sum())} px lệch > 24"
          f" -> {os.path.join(ra, '_soi.png')}")


# ================================================================ RIG (thư viện quai) ================================================================
# Cấu trúc học từ con gốc monster_3233 (ghi chú inbox/ca_den_ghichu.md mục 2), đổi cho hợp cách cắt của mình:
#   root -> move (game dời: lao) -> nhun (trôi lên xuống, cung nhảy lúc xuất hiện / bị hất)
#     -> than (khớp ở hông chân gần: nghiêng, dời, nén giãn cả con)
#          -> dau (khớp ở khoé miệng: ngửa = nhấc môi trên) -> mat_g, mat_x (con ngươi), den0..8 -> bong (cần đèn, bóng đèn)
#          -> lung (đi theo 55 % góc của dau) -> vl0, vl1 (vây lưng)
#          -> ham (khớp ở khoé miệng: hạ = há), bung (phình), mieng (chỗ và hướng nhả cho VFX)
#          -> vb0, vb1 (chóp vây bên), duoi0..6 (đuôi)
#     -> ban_g, ban_x (bàn chân gần, xa: bám đất; chân là phần lưới giãn giữa thân và bàn chân)
# Miệng há bằng uốn lưới (không đổi ảnh như con gốc): lớp thân nhấc môi, lớp hàm hạ xuống, lòng miệng nằm sau giãn theo cả hai.
SC = 0.5                      # pixel concept -> pixel rig
OX = {1: 750.0, 2: 770.0}               # trục giữa con (pixel concept): gốc rig ở mặt đất dưới điểm này
CHAM = {1: 1.0, 2: 1.1}       # dạng 2 nặng hơn: mọi clip chậm lại chừng này
NG_HA = 0.55                  # há quá mức này thì đổi sang HÌNH HÁ MIỆNG vẽ riêng (như con gốc đổi ảnh); dưới mức này uốn lưới bản khép
O_DAU, O_HAM = 8.0, 10.0      # trên hình há: há chưa hết cỡ (m < 1) thì đầu cúi, hàm nâng chừng này độ mỗi đơn vị m (khép bớt hốc)
SLOT_KHEP = ("ham", "mieng", "luoi", "rang_tren", "ma_xa")   # các lớp miệng của bản khép: tắt khi hiện hình há
HA_DAU, HA_HAM = 11.0, 4.0    # há hết cỡ: đầu ngửa, hàm hạ (độ); phần còn lại là môi vồng lên, hàm võng xuống ở GIỮA miệng
VOM_MOI, VONG_HAM = 0.09, 0.28    # môi trên vồng lên (ít: ngay trên môi là mắt), vành hàm võng xuống nhiều nhất chừng này lần bề dài miệng: miệng há TRÒN, nhìn
#                                   như quay mặt ra phía người xem (con gốc đổi sang ảnh miệng tròn; mình uốn lưới)
LUNG = 0.55


def _quai():
    sys.path.insert(0, HERE)
    from quai import anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat
    return anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat


def ss(x, a, b):
    """smoothstep 0..1 khi x đi từ a tới b."""
    u = np.clip((np.asarray(x, float) - a) / (b - a), 0.0, 1.0)
    return u * u * (3 - 2 * u)


def ln(f, keys):
    return float(np.interp(f, [k[0] for k in keys], [k[1] for k in keys]))


def _tron(*nguon):
    """trộn trọng số: _tron((k1, d1), (k2, d2)...) với d là dict {xương: w}."""
    out = {}
    for k, d in nguon:
        if k <= 1e-6:
            continue
        for b, w in d.items():
            out[b] = out.get(b, 0.0) + float(k) * float(w)
    return out


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
        """thế giới rig (N, 2) -> pixel concept (N, 2)."""
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
    TEN_ANH = ["chan_xa", "mieng", "luoi", "rang_tren", "ma_xa", "than", "nguoi_g", "nguoi_x", "vanh_g", "vanh_x", "ham", "den"]
    co_ha = "ha" in mj["manh"]
    if co_ha:
        TEN_ANH.insert(TEN_ANH.index("than") + 1, "ha")
    for t in TEN_ANH:
        sk.anh(t, nap(t))
    Hb, Fm = np.array(c["ban_le"], float), np.array(c["mui"], float)
    hong = np.array(c["hong"], float)
    top_y = min(mj["manh"][t][1] for t in TEN_ANH)
    H = (dat_y - top_y) * sc                                                  # chiều cao cả con (px rig)

    # ---------------- xương
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("nhun", "move")
    sk.xuong("than", "nhun", *R(hong), the_gioi=True)
    sk.xuong("lung", "than", *R(Hb), the_gioi=True)
    sk.xuong("dau", "than", *R(Hb), the_gioi=True)
    for s_ in "gx":
        sk.xuong(f"mat_{s_}", "dau", *R(mj["nguoi"][s_]["tam"]), the_gioi=True)
    Jd = Rs(c["den_khop"])
    den = sk.chuoi("den", "dau", Jd)
    pc, pb = np.array(R(c["chup"])), np.array(R(c["bong"]))
    sk.xuong("bong", den[-1], *pc, goc=math.degrees(math.atan2(pb[1] - pc[1], pb[0] - pc[0])), dai=float(np.hypot(*(pb - pc))), the_gioi=True)
    vl = sk.chuoi("vl", "lung", Rs(c["vay_lung"]))
    vb = sk.chuoi("vb", "than", Rs(c["vay_ben"]))
    Jt = Rs(c["duoi_khop"])
    duoi = sk.chuoi("duoi", "than", Jt)
    hr, fr_ = np.array(R(Hb)), np.array(R(Fm))
    sk.xuong("ham", "than", *hr, goc=math.degrees(math.atan2(fr_[1] - hr[1], fr_[0] - hr[0])), dai=float(np.hypot(*(fr_ - hr))), the_gioi=True)
    giua = Hb + 0.55 * (Fm - Hb)
    sk.xuong("moi_g", "dau", *R(giua), the_gioi=True)                         # môi trên vồng lên (chỉ dời)
    sk.xuong("ham_g", "ham", *R(giua), the_gioi=True)                         # vành hàm võng xuống (chỉ dời)
    sk.xuong("bung", "than", *R(c["bung"]), the_gioi=True)
    pm = np.array(R(Fm[0] - 70, Fm[1] - 2))
    sk.xuong("mieng", "than", *pm, goc=0, dai=40, the_gioi=True)
    sk.xuong("ban_g", "move", *R(c["ban_g"]), the_gioi=True)
    sk.xuong("ban_x", "move", *R(c["ban_x"]), the_gioi=True)

    # ---------------- slot (sau -> trước)
    sk.slot("chan_xa", "than", "chan_xa")
    sk.slot("mieng", "than", "mieng")
    sk.slot("luoi", "ham_g", "luoi")
    sk.slot("rang_tren", "dau", "rang_tren")
    sk.slot("ma_xa", "than", "ma_xa")
    sk.slot("than", "than", "than")
    if co_ha:
        sk.slot("ha", "than", None)                                           # hình há miệng: mặc định trống, clip bật khi há
    sk.slot("nguoi_g", "mat_g", "nguoi_g")
    sk.slot("nguoi_x", "mat_x", "nguoi_x")
    sk.slot("vanh_g", "dau", "vanh_g")
    sk.slot("vanh_x", "dau", "vanh_x")
    sk.slot("ham", "ham", "ham")
    sk.slot("den", den[0], "den")

    # ---------------- trường trọng số (toạ độ pixel concept)
    dmx = np.array([p[0] for p in mj["duong_mieng"]], float)
    dmy = np.array([p[1] for p in mj["duong_mieng"]], float)
    Lm = float(np.hypot(*(Fm - Hb)))

    def y_mieng(x):
        return np.interp(x, dmx, dmy)

    def f_dau(P):
        """phần đi theo xương dau của một điểm thuộc nửa trên: 0 ở bản lề và phía sau-dưới, 1 ở mặt và đỉnh đầu."""
        dx, dy = P[:, 0] - Hb[0], Hb[1] - P[:, 1]
        r = np.hypot(dx, dy)
        th = np.degrees(np.arctan2(dy, dx))                                   # 0 = sang phải, 90 = lên, ±180 = sang trái
        dth = np.where(th >= 0, 1 - ss(th, 100, 190), 1 - ss(-th, 4, 40))
        return ss(r, 30, 200) * dth

    def f_ham(P, vanh=False):
        """phần đi theo xương ham của một điểm thuộc lớp hàm: 0 ở bản lề, 1 ở vành miệng phía trước; càng sâu xuống bụng càng ít."""
        u = ((P - Hb) @ (Fm - Hb)) / (Lm * Lm)
        sau = P[:, 1] - y_mieng(P[:, 0])
        return ss(u, 0.06, 0.5) * (1.0 if vanh else (1 - 0.8 * ss(sau, 30, 230)))

    mn = np.load(os.path.join(dm, "mat_na.npz"))
    A_c, B_c = VOM_MOI * Lm, VONG_HAM * Lm                                    # px concept
    # khoảng trống phía trên đường miệng tới mắt theo từng cột: môi chỉ vồng trong khoảng đó (vành mắt là mảnh cứng, không ép)
    mat_ = gian(mn["cua_g"] | mn["cua_x"], 22)
    cot = np.arange(mat_.shape[1])
    day_mat = np.where(mat_.any(0), mat_.shape[0] - 1 - mat_[::-1].argmax(0), -999)       # đáy mắt theo cột
    phong = np.clip(y_mieng(cot) - day_mat - 6, 8, 190).astype(np.float32)
    phong = cv2.erode(phong.reshape(1, -1), np.ones((1, 161), np.uint8)).ravel()            # lấy chỗ hẹp nhất quanh đó: môi vồng đều, không nhọn
    phong = cv2.GaussianBlur(phong.reshape(1, -1), (0, 0), 20).ravel()
    u_cot = (cot - Hb[0]) / (Fm[0] - Hb[0])
    vom = np.minimum(A_c * np.sin(np.pi * np.clip((u_cot - 0.06) / 0.9, 0, 1)) ** 1.1, 0.8 * phong)
    vom = cv2.GaussianBlur(vom.reshape(1, -1).astype(np.float32), (0, 0), 16).ravel() / A_c    # phần vồng của môi theo cột (0..1)

    def f_vom(P):
        """phần đi theo xương moi_g của một điểm phía trên đường miệng: mép môi theo trọn, lên tới đáy mắt thì hết."""
        xi = np.clip(np.round(P[:, 0]).astype(int), 0, len(vom) - 1)
        h = y_mieng(P[:, 0]) - P[:, 1]
        return vom[xi] * (1 - ss(h, 0, np.maximum(12, phong[xi])))

    def f_vong(P):
        """phần võng xuống (xương ham_g) trong phần đi theo hàm: nhiều nhất ở giữa vành miệng, ít dần xuống đáy bụng."""
        u = ((P - Hb) @ (Fm - Hb)) / (Lm * Lm)
        sau = P[:, 1] - y_mieng(P[:, 0])
        return np.sin(np.pi * np.clip((u - 0.05) / 0.95, 0, 1)) * (1 - 0.85 * ss(sau, 20, 220))

    def luoi_cua(ten, **kw):
        return luoi.luoi_vung(sk.images[ten], buoc_theo_cao=H * thua, ten=f"{ten} {k}", **kw)

    def trong_poly(poly, P, do=False):
        pl = np.array(poly, np.float32)
        return np.array([cv2.pointPolygonTest(pl, (float(x), float(y)), do) for x, y in P])

    # ================= THÂN: một lưới liền =================
    Lt = luoi_cua("than")
    dat_t = dat_cua("than")
    Vt = dat_t.ra(Lt.pts, *sk.images["than"].size)
    Ct = C_(Vt)
    d_dau = f_dau(Ct)
    # chân gần
    f_chan = ss(Ct[:, 1], c["chan_g_y"][0], c["chan_g_y"][1]) * (Ct[:, 0] < c["chan_g_x"])
    trong_bung = co(mn["bung"], 3)
    ci = np.clip(np.round(Ct).astype(int), 0, [trong_bung.shape[1] - 1, trong_bung.shape[0] - 1])
    f_chan = f_chan * (~trong_bung[ci[:, 1], ci[:, 0]])                        # dải mọc thêm dưới bụng thuộc thân, không theo bàn chân
    # đuôi
    g0, g1 = np.array(c["duoi_goc"][0], float), np.array(c["duoi_goc"][1], float)
    gd = (g1 - g0) / np.hypot(*(g1 - g0))
    gn = np.array([-gd[1], gd[0]])
    if (np.array(c["duoi_khop"][3], float) - g0) @ gn < 0:
        gn = -gn
    rel = Ct - g0
    tt_ = np.clip(rel @ gd, 0, np.hypot(*(g1 - g0)))
    kc_goc = np.hypot(*(rel - tt_[:, None] * gd[None]).T)
    trong = trong_poly(c["duoi_poly"], Ct) >= 0
    tau = np.where(kc_goc < 45, ss(rel @ gn, -45, 45), trong.astype(float))
    tau = tau * (1 - ss(Ct[:, 1], c["chan_g_y"][0] - 12, c["chan_g_y"][0] + 8) * (Ct[:, 0] > g1[0] - 20))
    W_duoi = trongso.chuoi_chieu(Vt, Jt, duoi)
    # vây lưng
    v0, v1 = np.array(c["vay_lung_chan"][0], float), np.array(c["vay_lung_chan"][1], float)
    vd = (v1 - v0) / np.hypot(*(v1 - v0))
    vn = np.array([vd[1], -vd[0]])                                            # pháp tuyến chĩa lên (y ảnh xuống)
    if vn[1] > 0:
        vn = -vn
    u_vl = (Ct - v0) @ vn
    phi = ss(u_vl, 22, 80) * (trong_poly(c["vay_lung_poly"], Ct) >= 0)
    s_vl = ss(u_vl, 70, 150)
    # vây bên (chỉ chóp vây phất)
    b0, b2 = np.array(c["vay_ben"][0], float), np.array(c["vay_ben"][2], float)
    t_vb = ((Ct - b0) @ (b2 - b0)) / float((b2 - b0) @ (b2 - b0))
    beta = ss(t_vb, 0.2, 0.85) * ss(trong_poly(c["vay_ben_poly"], Ct, True), -14, 6)
    s_vb = ss(t_vb, 0.55, 1.0)
    w_vom = f_vom(Ct) * (Ct[:, 0] > Hb[0]) * (Ct[:, 1] < y_mieng(Ct[:, 0]) + 12)
    Wt = []
    for i in range(Lt.n):
        w = {"dau": float(d_dau[i]), "than": float(1 - d_dau[i])}
        if w_vom[i] > 0:
            w = _tron((1 - w_vom[i], w), (w_vom[i], {"moi_g": 1.0}))
        if f_chan[i] > 0:
            w = _tron((1 - f_chan[i], w), (f_chan[i], {"ban_g": 1.0}))
        if tau[i] > 0:
            w = _tron((1 - tau[i], w), (tau[i], W_duoi[i]))
        if phi[i] > 0:
            w = _tron((1 - phi[i], w), (phi[i], {vl[0]: float(1 - s_vl[i]), vl[1]: float(s_vl[i])}))
        if beta[i] > 0:
            w = _tron((1 - beta[i], w), (beta[i], {vb[0]: float(1 - s_vb[i]), vb[1]: float(s_vb[i])}))
        Wt.append(w)
    sk.luoi_gan("than", "than", Lt, trongso.chuan(Wt), dat=dat_t)

    # ================= HÀM DƯỚI + bụng + răng =================
    Lh = luoi_cua("ham")
    dat_h = dat_cua("ham")
    Ch = C_(dat_h.ra(Lh.pts, *sk.images["ham"].size))
    h_ = f_ham(Ch)
    q_ = f_vong(Ch)
    bc = np.array(c["bung"], float)
    sau_h = Ch[:, 1] - y_mieng(Ch[:, 0])
    b_ = 0.9 * np.exp(-((Ch[:, 0] - bc[0]) / 200.0) ** 2 - ((Ch[:, 1] - bc[1]) / 125.0) ** 2) * ss(sau_h, 18, 70)
    Wh = []
    for i in range(Lh.n):
        wb = float(b_[i] * (1 - 0.5 * h_[i]))
        wh = float(h_[i] * (1 - wb))
        Wh.append({"ham": wh * (1 - q_[i]), "ham_g": wh * q_[i], "bung": wb, "than": max(0.0, 1 - wh - wb)})
    sk.luoi_gan("ham", "ham", Lh, trongso.chuan(Wh), dat=dat_h)

    # ================= LÒNG MIỆNG, MÁ BÊN KIA: mép trên theo môi, phần dưới theo vành hàm, giữa giãn =================
    def w_khe(Cp):
        """trọng số của lớp nằm trong khe miệng: trên đường miệng đi theo môi (đầu + vòm môi), sâu quá 85 px đi theo hàm đúng như
        lớp hàm ở chỗ đó (nên luôn khuất), ở giữa hoà: há ra thì dải này giãn lấp khe."""
        sau = Cp[:, 1] - y_mieng(Cp[:, 0])
        g = 1 - ss(sau, -5, 85)
        dmo = ss(np.hypot(Cp[:, 0] - Hb[0], Cp[:, 1] - Hb[1]), 30, 200)
        hv, qv = f_ham(Cp), f_vong(Cp)
        xi = np.clip(np.round(Cp[:, 0]).astype(int), 0, len(vom) - 1)
        av = vom[xi] * (Cp[:, 0] > Hb[0])
        out = []
        for i in range(len(Cp)):
            tren = {"moi_g": float(av[i]), "dau": float(dmo[i] * (1 - av[i])), "than": float((1 - dmo[i]) * (1 - av[i]))}
            duoi = {"ham_g": float(hv[i] * qv[i]), "ham": float(hv[i] * (1 - qv[i])), "than": float(1 - hv[i])}
            out.append(_tron((g[i], tren), (1 - g[i], duoi)))
        return trongso.chuan(out)

    Lg = luoi_cua("mieng")
    dat_g = dat_cua("mieng")
    sk.luoi_gan("mieng", "mieng", Lg, w_khe(C_(dat_g.ra(Lg.pts, *sk.images["mieng"].size))), dat=dat_g)
    Lma = luoi_cua("ma_xa")
    dat_ma = dat_cua("ma_xa")
    sk.luoi_gan("ma_xa", "ma_xa", Lma, w_khe(C_(dat_ma.ra(Lma.pts, *sk.images["ma_xa"].size))), dat=dat_ma)

    # ================= HÌNH HÁ MIỆNG (đổi ảnh): trên vòm môi theo đầu, dưới vành hàm theo hàm, trong hốc hoà =================
    info_o = None
    if co_ha:
        ho = mj["ha"]
        Lo = luoi_cua("ha")
        dat_o = dat_cua("ha")
        Vo = dat_o.ra(Lo.pts, *sk.images["ha"].size)
        Co = C_(Vo)
        cx_ = np.arange(ho["x0"], ho["x1"] + 1)
        yl = np.interp(Co[:, 0], cx_, np.array(ho["moi"]))
        yr = np.interp(Co[:, 0], cx_, np.array(ho["vanh"]))
        ngoai = (Co[:, 0] < ho["x0"]) | (Co[:, 0] > ho["x1"])
        y_mep = np.where(Co[:, 0] < ho["x0"], 0.5 * (ho["moi"][0] + ho["vanh"][0]), 0.5 * (ho["moi"][-1] + ho["vanh"][-1]))
        yl = np.where(ngoai, y_mep - 4, yl)
        yr = np.where(ngoai, y_mep + 4, yr)
        t_ = ss(Co[:, 1], yl, np.maximum(yl + 8, yr))
        ci_o = np.clip(np.round(Co).astype(int), 0, [mn["ha_hoc"].shape[1] - 1, mn["ha_hoc"].shape[0] - 1])
        t_ = np.where(mn["ha_rang_duoi"][ci_o[:, 1], ci_o[:, 0]] | mn["ha_luoi"][ci_o[:, 1], ci_o[:, 0]], 1.0, t_)
        t_ = np.where(mn["ha_rang_tren"][ci_o[:, 1], ci_o[:, 0]], 0.0, t_)
        d_o = f_dau(Co)
        u_o = ((Co - Hb) @ (Fm - Hb)) / (Lm * Lm)
        h_o = ss(u_o, 0.06, 0.5) * (1 - 0.8 * ss(Co[:, 1] - yr, 30, 230))
        bo_ = 0.9 * np.exp(-((Co[:, 0] - bc[0]) / 200.0) ** 2 - ((Co[:, 1] - bc[1] - 30) / 125.0) ** 2) * ss(Co[:, 1] - yr, 18, 70)
        Wo = []
        for i in range(Lo.n):
            wb = float(bo_[i] * (1 - 0.5 * h_o[i]))
            wh = float(h_o[i] * (1 - wb))
            Wo.append(_tron((1 - t_[i], {"dau": float(d_o[i]), "than": float(1 - d_o[i])}),
                            (t_[i], {"ham": wh, "bung": wb, "than": max(0.0, 1 - wh - wb)})))
        sk.luoi_gan("ha", "ha", Lo, trongso.chuan(Wo), dat=dat_o, ten="ha")
        tam_o = np.array(R(ho["tam"][0] + 0.28 * (ho["x1"] - ho["x0"]), ho["tam"][1]))
        info_o = {"dx": float(tam_o[0] - pm[0]), "dy": float(tam_o[1] - pm[1]), "dinh": Lo.n}

    # ================= CHÂN XA: trên theo thân, bàn chân bám đất =================
    Lx = luoi_cua("chan_xa")
    dat_x = dat_cua("chan_xa")
    Cx = C_(dat_x.ra(Lx.pts, *sk.images["chan_xa"].size))
    fx = ss(Cx[:, 1], c["chan_x_y"][0], c["chan_x_y"][1])
    sk.luoi_gan("chan_xa", "chan_xa", Lx, trongso.chuan([{"ban_x": float(v), "than": float(1 - v)} for v in fx]), dat=dat_x)

    # ================= CẦN ĐÈN: chuỗi B-spline, bóng đèn cứng theo xương bong =================
    Ld = luoi_cua("den")
    dat_d = dat_cua("den")
    Vd = dat_d.ra(Ld.pts, *sk.images["den"].size)
    s_d, cum_d = trongso._chieu_len_gay(Vd, Jd)
    W_den = trongso.chuoi(s_d, np.diff(cum_d), den, cha="dau", cha_hoa=1.0)
    m_b = ss(s_d, cum_d[-1] - 16, cum_d[-1] - 2)
    Wd_ = [_tron((1 - m_b[i], W_den[i]), (m_b[i], {"bong": 1.0})) for i in range(Ld.n)]
    sk.luoi_gan("den", "den", Ld, trongso.chuan(Wd_), dat=dat_d)

    # ================= mảnh cứng: con ngươi, vành mắt =================
    sk.manh("luoi", "luoi", dat_cua("luoi"))
    # hàng răng trên: bám mép môi (theo đầu + vòm môi tại cột của từng răng)
    Lr = luoi_cua("rang_tren")
    dat_r = dat_cua("rang_tren")
    Cr = C_(dat_r.ra(Lr.pts, *sk.images["rang_tren"].size))
    xi_r = np.clip(np.round(Cr[:, 0]).astype(int), 0, len(vom) - 1)
    d_r = ss(np.hypot(Cr[:, 0] - Hb[0], y_mieng(Cr[:, 0]) - Hb[1]), 30, 200)
    sk.luoi_gan("rang_tren", "rang_tren", Lr, trongso.chuan(
        [{"moi_g": float(vom[x]), "dau": float(d * (1 - vom[x])), "than": float((1 - d) * (1 - vom[x]))} for x, d in zip(xi_r, d_r)]), dat=dat_r)
    for s_ in "gx":
        sk.manh(f"nguoi_{s_}", f"nguoi_{s_}", dat_cua(f"nguoi_{s_}"))
        sk.manh(f"vanh_{s_}", f"vanh_{s_}", dat_cua(f"vanh_{s_}"))
    for ev, mo_ta in (("trung", "bóng đèn đập trúng đối thủ"), ("phun", "bắt đầu nhả nước (VFX bám xương mieng)"), ("het_phun", "hết nhả"),
                      ("dam", "chiêu cuối: chân dậm xuống đất"), ("cham_dat", "xuất hiện: chạm đất")):
        sk.su_kien(ev, mo_ta)
    xm = int(round(Fm[0] - 70))
    um = (xm - Hb[0]) / (Fm[0] - Hb[0])
    info_ha = {"A": A_c * sc, "B": B_c * sc, "a_m": float(vom[xm]), "q_m": float(math.sin(math.pi * min(1, max(0, (um - 0.05) / 0.95))))}
    info = {"k": k, "ti": ti, "H": H, "ha": info_ha, "o": info_o, "den": den, "duoi": duoi, "vl": vl, "vb": vb, "Lm": float(np.hypot(*(pm - hr))),
            "dinh": {"than": Lt.n, "ham": Lh.n, "mieng": Lg.n, "chan_xa": Lx.n, "den": Ld.n},
            "ho": {"than": Lt.ho, "ham": Lh.ho, "mieng": Lg.ho, "chan_xa": Lx.ho, "den": Ld.ho}}
    return sk, info


def clips(sk, info, k):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    Clip, LoXo, rung = hoat.Clip, hoat.LoXo, hoat.rung
    H, den, duoi, vl, vb, Lm = info["H"], info["den"], info["duoi"], info["vl"], info["vb"], info["Lm"]
    HA = info["ha"]
    OH = info.get("o")
    S = H / 455.0                                                             # mọi độ dời viết cho con cao 455 px rig
    F = 30.0 / CHAM[k]                                                        # khung (của bản thiết kế) mỗi giây
    slots = [s["name"] for s in sk.slots]
    W0 = sk.the_gioi()
    T0 = 32.0                                                                 # một vòng idle của con gốc (khung)
    A_DUOI = np.array([2.5, 4.0, 5.5, 7.5, 10.0, 13.0, 16.0])[:len(duoi)]
    W_DEN = np.array([0.2, 0.17, 0.14, 0.12, 0.1, 0.09, 0.07, 0.06, 0.05])[:len(den)]
    W_DEN = W_DEN / W_DEN.sum()

    def sg(f, chu_ky, tre=0.0):
        """sóng sin theo khung, bằng 0 ở khung 0 (để khung 0 của idle là dáng gốc), trễ `tre` khung."""
        return math.sin(2 * math.pi * (f - tre) / chu_ky) + math.sin(2 * math.pi * tre / chu_ky)

    def dau_(P, a):
        P.rot("dau", a)
        P.rot("lung", LUNG * a)

    def mo(P, m):
        """há miệng m (0 khép .. 1 há hết cỡ). m < NG_HA: uốn lưới bản khép (môi nhấc, hàm hạ). m >= NG_HA: đổi sang hình há miệng
        vẽ riêng (hai hàm khít ở mép bên kia), tắt lớp hàm và các lớp lòng miệng của bản khép; xương mieng (VFX) về giữa hốc."""
        if OH is not None and m >= NG_HA:
            P.att["ha"] = "ha"
            for sl in SLOT_KHEP:
                P.att[sl] = None
            dau_(P, O_DAU * (m - 1))
            P.rot("ham", -O_HAM * (m - 1))
            P.move("mieng", OH["dx"], OH["dy"])
            return
        dau_(P, HA_DAU * m)
        P.rot("ham", -HA_HAM * m)
        mm = max(m, 0.0)
        P.move("moi_g", 0, HA["A"] * mm)
        P.move("ham_g", 0, -HA["B"] * mm)
        P.move("mieng", 0, 0.5 * (Lm * (math.sin(math.radians(HA_DAU * m)) - math.sin(math.radians(HA_HAM * m)))
                                  + (HA["A"] * HA["a_m"] - HA["B"] * HA["q_m"]) * mm))

    def theo_than(P, ten, w=1.0, them=(0.0, 0.0, 0.0)):
        """bàn chân đi theo thân (w = 1: như dính cứng vào thân; 0: bám đất), cộng thêm (dx, dy, góc)."""
        if w > 0:
            W = sk.the_gioi(P)
            T = np.linalg.inv(W["move"]) @ W["than"] @ np.linalg.inv(W0["than"]) @ W0["move"]
            b = sk.bones[sk.bi[ten]]
            p = T @ np.array([b["x"], b["y"], 1.0])
            P.move(ten, w * (p[0] - b["x"]), w * (p[1] - b["y"]))
            P.rot(ten, w * math.degrees(math.atan2(T[1, 0], T[0, 0])))
        P.move(ten, them[0], them[1])
        P.rot(ten, them[2])

    W_RU = np.array([-70, -50, 10, 10, 10, 10, 10, 10, 10])[:len(den)] / 100.0   # đổ ra trước: gập ở gốc, ngọn duỗi bớt (độ mỗi đốt khi khoá = 100)

    def den_xoay(P, f, keys, tre=0.55, w=None):
        """xoay cả cần đèn một góc tổng theo khoá (dương = ngả ra sau), chia cho các đốt, đốt gần ngọn trễ hơn (quất roi)."""
        w = W_DEN if w is None else w
        for i, b in enumerate(den):
            P.rot(b, float(w[i]) * ln(f - tre * i, keys))

    def nen(P, f, a=1.0):
        """chuyển động nền (idle) ở khung f, biên độ a; mọi thành phần bằng 0 ở f = 0."""
        if a <= 0:
            return
        P.move("nhun", 0, a * 3.2 * S * 0.5 * (1 - math.cos(2 * math.pi * f / T0)))
        nh = 0.5 * (1 - math.cos(2 * math.pi * f / (T0 / 2)))                 # nhún hai lần mỗi vòng
        P.move("than", 0, a * 5.5 * S * nh)
        P.scale("than", 1 - 0.012 * a * nh, 1 + 0.02 * a * nh)
        P.rot("than", a * (1.3 * sg(f, T0, 2) - 0.5 * sg(f, T0 / 2, 5)))
        dau_(P, -a * 0.45 * ((1 - math.cos(2 * math.pi * (f - 4) / T0)) - (1 - math.cos(2 * math.pi * 4 / T0))))
        bg_ = 1 + 0.03 * a * sg(f, T0, 6)
        P.scale("bung", bg_, bg_)
        for i, b in enumerate(duoi):
            P.rot(b, a * float(A_DUOI[i]) * 0.5 * sg(f, T0 / 2, 4 * i))
        for i, b in enumerate(vl):
            P.rot(b, a * (4.0, 7.0)[i] * 0.5 * sg(f, T0 / 2, 3 + 4 * i))
        for i, b in enumerate(vb):
            P.rot(b, a * (3.5, 6.0)[i] * 0.5 * sg(f, T0 / 2, 7 + 3 * i))
        for i, b in enumerate(den):
            P.rot(b, a * 0.9 * sg(f, T0, 5 + 1.5 * i))
        P.rot("bong", a * 7.0 * sg(f, T0, 12))

    def mat(P, dx=0.0, dy=0.0, co_=1.0):
        P.move("mat_g", dx * S, dy * S)
        P.move("mat_x", 0.7 * dx * S, 0.8 * dy * S)
        if co_ != 1.0:
            P.scale("mat_g", co_, co_)
            P.scale("mat_x", co_, co_)

    def an_het(P, a):
        for s in slots:
            P.alpha[s] = a

    def mem():
        return [LoXo(duoi, k=[520, 440, 370, 300, 250, 210, 180][:len(duoi)], damp=0.55, maxang=11),
                LoXo(den + ["bong"], k=[620, 560, 500, 450, 400, 360, 320, 290, 260][:len(den)] + [150], damp=0.5, maxang=9),
                LoXo(vl, k=[380, 260], damp=0.5, maxang=9), LoXo(vb, k=[380, 260], damp=0.5, maxang=8)]

    # ---------------- idle: 2 vòng của con gốc (32 khung mỗi vòng): vòng một liếc mắt, vòng hai táp miệng
    def idle_fn(t, P):
        f = t * F
        nen(P, f)
        g = ln(f % 64, [(0, 0), (4, 0), (7, 1), (17, 1), (20, 0), (64, 0)])
        mat(P, -7 * g, -2.5 * g)
        mo(P, ln(f % 64, [(0, 0), (38, 0), (41, 0.2), (43, 0.0), (45, 0.13), (47, 0), (64, 0)]))

    # ---------------- attack: quật bóng đèn. Lấy đà: người ngả sau, cần ngả sau; quật qua đầu xuống trước trong 3 khung; khựng; nảy; về
    def attack_fn(t, P):
        f = t * F
        nen(P, f, 0.5 * hoat.bao(t, 0, 30 / F, 6 / F, 8 / F))
        lean = ln(f, [(0, 0), (8, 1), (10, 1.08), (13, -1.25), (16, -1.1), (21, 0.25), (26, 0), (30, 0)])
        P.rot("than", 7 * lean)
        P.move("than", (-7 * max(lean, 0) - 6 * min(lean, 0)) * S, -4 * S * abs(lean))
        P.scale("than", 1 + 0.03 * max(-lean, 0), 1 - 0.035 * max(-lean, 0))
        P.move("move", 0.30 * H * ln(f, [(0, 0), (9, 0), (10, 0.12), (12, 0.8), (13, 1), (16, 1), (19, 0.6), (24, 0)]), 0)
        den_xoay(P, f, [(0, 0), (8, 96), (10, 108), (12, -20), (13, -90), (14, -112), (16, -104), (20, -30), (23, 14), (26, -4), (30, 0)])
        sc = ln(f, [(0, 1), (10, 1), (12, 1.14), (13, 1.05), (15, 1), (30, 1)])
        for b in den:
            P.scale(b, sc, 1)
        P.rot("bong", ln(f, [(0, 0), (6, -22), (10, -12), (12, 38), (13, -18), (15, 6), (19, 24), (24, -8), (30, 0)]))
        P.scale("bong", ln(f, [(0, 1), (12.5, 1), (13, 1.22), (15, 0.94), (17, 1)]), ln(f, [(0, 1), (12.5, 1), (13, 0.82), (15, 1.05), (17, 1)]))
        mo(P, ln(f, [(0, 0), (9, 0), (12, 0.32), (16, 0.28), (20, 0), (30, 0)]))
        g = ln(f, [(0, 0), (6, 1), (10, 1), (13, -1), (17, -1), (22, 0)])
        mat(P, -3 * max(g, 0), 2 * max(g, 0) - 3 * max(-g, 0))
        for i, b in enumerate(duoi):
            P.rot(b, -float(A_DUOI[i]) * 0.9 * ln(f - 0.8 * i, [(0, 0), (8, 1), (12, -1.2), (17, 0.5), (24, 0)]))

    # ---------------- cast: hít vào (bụng phình), chồm tới há miệng nhả nước, giữ há rung nhẹ, NGẬM LẠI rồi mới về
    C_PHUN, C_HET = 15.0, 27.0
    # Dòng tia nước của game (HatNuoc n_tia) chảy 0,88 s THẬT kể từ sự kiện phun: miệng phải há tới phun + 0,94 s rồi mới ngậm
    # (người dùng chê Tí Tách ngậm miệng khi nước còn phun, 2026-11-11). Khoá viết trên trục cũ (giữ há 12 khung); chèn thêm XC
    # khung đứng ở cuối đoạn giữ, mọi khoá sau đó lùi theo.
    GIU_TIA = 0.94
    XC = max(0.0, math.ceil(GIU_TIA * F + 1 - (C_HET - C_PHUN)))

    def chen(fm, moc, them):
        """trục mới -> trục cũ: sau khung `moc` chèn `them` khung đứng yên."""
        return fm if fm <= moc else (moc if fm <= moc + them else fm - them)

    def cast_fn(t, P):
        f = chen(t * F, C_HET - 0.01, XC)
        nen(P, f, 0.4 * hoat.bao(t, 0, (36 + XC) / F, 5 / F, 6 / F))
        r = rung(t, 16 / F, (C_HET + XC) / F)
        lean = ln(f, [(0, 0), (9, 1), (12, 0.8), (15, -1), (C_HET, -0.85), (31, 0.15), (36, 0)])
        P.rot("than", 5.5 * lean if lean > 0 else 6.0 * lean)
        P.move("than", (ln(f, [(0, 0), (9, -5), (13, -2), (15, 9), (17, -5), (C_HET, -3), (31, 1), (36, 0)]) + 1.2 * r) * S, 0)
        P.scale("than", ln(f, [(0, 1), (9, 0.985), (12, 1.02), (15, 1.03), (17, 0.99), (36, 1)]),
                ln(f, [(0, 1), (9, 1.03), (12, 0.96), (15, 0.97), (17, 1.01), (36, 1)]))
        bg_ = ln(f, [(0, 1), (9, 1.2), (12, 1.24), (15, 0.93), (C_HET, 0.97), (31, 1.03), (36, 1)])
        P.scale("bung", bg_, bg_)
        mo(P, ln(f, [(0, 0), (12, 0.04), (13, 0.2), (15, 1.06), (16.5, 1), (C_HET, 1), (29, 0.4), (31, -0.05), (33, 0), (36, 0)]) + 0.045 * r)
        den_xoay(P, f, [(0, 0), (9, 16), (13, 12), (15, -12), (18, 12), (C_HET, 8), (31, -3), (36, 0)])
        mat(P, 0, ln(f, [(0, 0), (9, 2.5), (15, -1), (C_HET, -1), (32, 0)]), ln(f, [(0, 1), (14, 1), (15, 0.86), (C_HET, 0.86), (30, 1)]))
        for i, b in enumerate(duoi):
            P.rot(b, float(A_DUOI[i]) * (0.8 * ln(f - 0.8 * i, [(0, 0), (9, -1), (15, 1.1), (C_HET, 0.8), (33, 0)]) + 0.25 * r * (1 if i % 2 else -1)))

    # ---------------- skill (học skill_02 của con gốc): bước trụ, ngả người đứng một chân, bụng phình rung; dậm; há miệng gầm; ngậm; lắng
    K_DAM, K_PHUN, K_HET = 16.0, 17.0, 33.0
    XK = max(0.0, math.ceil(GIU_TIA * F + 1 - (K_HET - K_PHUN)))               # chiêu cuối cũng bắn tia: giữ há đủ lâu như trên

    def skill_fn(t, P):
        f = chen(t * F, K_HET - 0.01, XK)
        r1 = rung(t, 5 / F, 15 / F, moi=1)
        r2 = rung(t, K_PHUN / F, (K_HET + XK) / F, moi=1)
        r4 = rung(t, K_PHUN / F, (K_HET + XK) / F, moi=2)
        ng = ln(f, [(0, 0), (2, -4), (4, 6), (6, 25), (15, 28), (16, 8), (17, -9), (K_HET, -7.5), (36, 3), (40, -1), (48, 0)])
        P.rot("than", ng)
        P.move("than", ln(f, [(0, 0), (2, -8), (4, -26), (15, -30), (16, -8), (17, 8), (K_HET, 6), (36, 2), (40, 0)]) * S,
               (ln(f, [(0, 0), (4, 5), (6, 13), (15, 16), (16, 2), (17, -5), (19, 3), (K_HET, 0), (36, 7), (40, 0)]) + 2.5 * r4) * S)
        P.scale("than", ln(f, [(0, 1), (16, 1), (17, 1.05), (19, 0.99), (48, 1)]), ln(f, [(0, 1), (16, 1), (17, 0.93), (19, 1.01), (48, 1)]))
        bg_ = ln(f, [(0, 1), (4, 1.34), (15, 1.42), (K_PHUN, 0.95), (K_HET, 0.98), (37, 1.04), (42, 1)]) * (1 + 0.035 * r1)
        P.scale("bung", bg_, bg_)
        mo(P, ln(f, [(0, 0), (4, -0.05), (15, -0.05), (16, 0.25), (K_PHUN, 1.1), (18.5, 1), (K_HET, 1), (35, 0.3), (36.5, -0.06), (39, 0), (48, 0)])
           + 0.07 * r2)
        # chân trụ (gần) bước lùi rồi về; chân kia theo thân nhấc cao rồi dậm
        P.move("ban_g", ln(f, [(0, 0), (1, -10), (2, -24), (K_HET, -24), (35, -8), (36, 0)]) * S,
               ln(f, [(0, 0), (1, 7), (2, 0), (K_HET, 0), (34.5, 6), (36, 0)]) * S)
        wx = ln(f, [(0, 0), (4, 0), (6, 1), (15, 1), (16, 0), (48, 0)])
        theo_than(P, "ban_x", wx, (ln(f, [(0, 0), (4, 0), (8, 6), (15, 10), (16, 6), (17, 0)]) * S,
                                   ln(f, [(0, 0), (4, 0), (8, 6), (15, 14), (16, 0)]) * S, ln(f, [(0, 0), (4, 0), (6, 14), (15, 22), (16, 0)])))
        P.scale("ban_x", ln(f, [(0, 1), (15.9, 1), (16, 1.18), (18, 1)]), ln(f, [(0, 1), (15.9, 1), (16, 0.8), (18, 1)]))
        # đuôi: ngả người thì cuộn lên khỏi đất; lúc gầm quất mỗi 2 khung
        cuon = ln(f, [(0, 0), (6, 1), (15, 1.05), (17, 0), (48, 0)])
        for i, b in enumerate(duoi):
            P.rot(b, -(3, 3, 3, 2, 2, 1, 1)[i] * cuon + float(A_DUOI[i]) * 0.55 * r4 * (1 if i % 2 else -1)
                  + float(A_DUOI[i]) * ln(f - 0.8 * i, [(0, 0), (16, 0), (18, 1.3), (22, 0), (K_HET, 0), (37, -0.8), (43, 0)]))
        for i, b in enumerate(vl):
            P.rot(b, (5, 8)[i] * r4 * (1 if i else -1) - 6 * cuon)
        den_xoay(P, f, [(0, 0), (4, -8), (7, 30), (15, 22), (17, -34), (20, 6), (K_HET, 0), (37, -10), (42, 0)])
        P.rot("bong", ln(f, [(0, 0), (6, -20), (12, 10), (15, 6), (17, 30), (20, -16), (24, 0)]) + 5 * r4)
        mat(P, ln(f, [(0, 0), (6, -4), (15, -4), (17, 2), (K_HET, 2), (38, 0)]), ln(f, [(0, 0), (6, 3), (15, 3), (17, -2), (K_HET, -2), (38, 0)]),
            ln(f, [(0, 1), (16, 1), (17, 0.8), (K_HET, 0.8), (36, 1)]))

    # ---------------- appear: nhảy bằng chân từ sau lưng (ngoài khung) vào, chân co lúc bay, duỗi đón đất, bẹp, nảy
    A_DAT = 13.0

    def appear_fn(t, P):
        f = t * F
        an_het(P, ln(f, [(0, 0), (2, 1)]))
        u = min(1.0, f / A_DAT)
        x = -0.82 * H * (1 - u)
        y = 0.75 * H * 4 * u * (1 - u) + 0.1 * H * (1 - u)
        y += ln(f, [(0, 0), (A_DAT, 0), (16, 0.07 * H), (19, 0), (21.5, 0.02 * H), (24, 0)])
        P.move("nhun", x, y)
        P.rot("than", ln(f, [(0, 16), (6, 6), (11, -12), (A_DAT, -6), (15, 5), (19, -2), (24, 0), (30, 0)]))
        P.scale("than", ln(f, [(0, 0.94), (10, 0.95), (A_DAT, 0.97), (14.5, 1.16), (17, 0.95), (20, 1.03), (24, 1)]),
                ln(f, [(0, 1.08), (10, 1.07), (A_DAT, 1.04), (14.5, 0.8), (17, 1.07), (20, 0.97), (24, 1)]))
        wbay = ln(f, [(0, 1), (A_DAT - 1, 1), (A_DAT, 0), (15.5, 0), (16, 0.6), (19, 0), (30, 0)])
        co_chan = ln(f, [(0, 1), (8, 1), (A_DAT - 0.5, -0.4), (A_DAT, 0)])
        for ten, g_ in (("ban_g", -24.0), ("ban_x", -20.0)):
            theo_than(P, ten, wbay, (6 * S * co_chan * wbay, (9 * max(co_chan, 0) - 7 * max(-co_chan, 0)) * S * wbay, g_ * co_chan * wbay))
        mo(P, ln(f, [(0, 0.35), (10, 0.4), (A_DAT, 0.15), (15, -0.05), (18, 0), (30, 0)]))
        den_xoay(P, f, [(0, 34), (8, 30), (A_DAT, 10), (15, -42), (18, 14), (22, -5), (26, 0)])
        P.rot("bong", ln(f, [(0, 20), (A_DAT, 10), (15, 26), (18, -14), (22, 4), (26, 0)]))
        for i, b in enumerate(duoi):
            P.rot(b, float(A_DUOI[i]) * ln(f - 0.7 * i, [(0, 1.3), (10, 1.0), (A_DAT, 0.4), (15.5, -1.2), (19, 0.5), (24, 0), (30, 0)]))
        mat(P, 0, ln(f, [(0, -3), (A_DAT, -3), (16, 1.5), (22, 0)]))

    # ---------------- hit: bị hất ngửa ra sau, miệng bật há, chân xa hẫng lên, về
    def hit_fn(t, P):
        f = t * F
        ng = ln(f, [(0, 0), (1, 12), (2, 16), (5, 10), (9, -3.5), (12, 1), (15, 0)])
        P.rot("than", ng)
        P.move("than", ln(f, [(0, 0), (1, -12), (2, -18), (5, -12), (9, 2), (12, 0)]) * S, ln(f, [(0, 0), (2, 9), (5, 6), (9, -3), (12, 0)]) * S)
        P.scale("than", ln(f, [(0, 1), (1, 0.92), (3, 1.03), (9, 1.02), (12, 1)]), ln(f, [(0, 1), (1, 1.1), (3, 0.97), (9, 0.97), (12, 1)]))
        mo(P, ln(f, [(0, 0), (1, 0.5), (2, 0.62), (6, 0.5), (9, 0.1), (10.5, -0.05), (13, 0)]))
        theo_than(P, "ban_x", ln(f, [(0, 0), (1, 0.9), (5, 0.8), (9, 0), (15, 0)]), (0, 0, ln(f, [(0, 0), (2, 16), (9, 0)])))
        mat(P, ln(f, [(0, 0), (1, 4), (6, 3), (11, 0)]), ln(f, [(0, 0), (1, 3), (6, 2), (11, 0)]), ln(f, [(0, 1), (1, 0.62), (6, 0.66), (10, 1)]))
        den_xoay(P, f, [(0, 0), (1, -26), (3, 24), (6, 12), (9, -8), (12, 2), (15, 0)], tre=0.4)
        n = len(duoi)
        for i, b in enumerate(duoi):                                          # sóng chạy từ chóp đuôi về gốc
            P.rot(b, float(A_DUOI[i]) * 1.2 * ln(f, [(0, 0), (2 + 0.8 * (n - 1 - i), 1), (8 + 0.6 * i, -0.4), (15, 0)]))
        for i, b in enumerate(vl):
            P.rot(b, (9, 14)[i] * ln(f - i, [(0, 0), (2, 1), (7, -0.5), (12, 0)]))

    # ---------------- die: bị hất nảy lên, rơi SẤP xuống đất (bụng chạm đất, chân bẹp), nảy một nhịp, miệng trễ, mắt quay vòng,
    # cần đèn đổ ra trước, bóng đèn rơi xuống đất nảy rồi nằm im, đuôi duỗi rũ; mờ dần
    def die_fn(t, P):
        f = t * F
        P.move("nhun", ln(f, [(0, 0), (2, -14), (8, -20), (12, -16), (40, -16)]) * S,
               ln(f, [(0, 0), (2, 30), (5, 62), (7, 66), (9, 54), (11, 16), (12, -12), (15, -2), (18, -14), (21, -11), (24, -14), (40, -14)]) * S)
        P.rot("than", ln(f, [(0, 0), (1, 12), (2, 16), (7, 10), (11, -8), (12, -14), (15, -9), (18, -16), (21, -14), (24, -15.5), (40, -15.5)]))
        P.scale("than", ln(f, [(0, 1), (11, 1), (12, 1.14), (15, 0.97), (18, 1.07), (21, 1.03), (24, 1.05), (40, 1.05)]),
                ln(f, [(0, 1), (11, 1), (12, 0.84), (15, 1.03), (18, 0.92), (21, 0.96), (24, 0.94), (40, 0.94)]))
        mo(P, ln(f, [(0, 0), (1, 0.5), (7, 0.65), (11, 0.5), (12, 0.2), (15, 0.6), (18, 0.34), (22, 0.46), (40, 0.42)]))
        wbay = ln(f, [(0, 0), (1, 1), (10, 1), (12, 0), (40, 0)])
        gi = ln(f, [(0, 0), (12, 0), (13, 1), (24, 1), (30, 0.3), (40, 0)])
        theo_than(P, "ban_g", wbay, (-8 * S * (1 - wbay) * ln(f, [(0, 0), (12, 0), (13, 1), (40, 1)]), 0,
                                     ln(f, [(0, 0), (5, -18), (11, -8), (12, 4), (40, 5)]) + 4 * gi * math.sin(f * 2.1)))
        theo_than(P, "ban_x", wbay, (10 * S * (1 - wbay) * ln(f, [(0, 0), (12, 0), (13, 1), (40, 1)]), 0,
                                     ln(f, [(0, 0), (5, 20), (11, 10), (12, -8), (40, -10)]) + 6 * gi * math.sin(f * 2.1 + 2)))
        # cần đèn: văng ra sau lúc bị hất, rồi đổ ra trước; bóng đèn chạm đất ở khung 14, nảy, nằm im
        den_xoay(P, f, [(0, 0), (2, -24), (6, 34), (10, 20), (12, 0), (40, 0)], tre=0.5)
        den_xoay(P, f, [(0, 0), (10, 0), (12, 34), (14, 105), (16, 86), (19, 103), (22, 96), (25, 100), (40, 100)], tre=0.4, w=W_RU)
        P.rot("bong", ln(f, [(0, 0), (3, 22), (10, -10), (13, 34), (14, -22), (17, 12), (20, -8), (24, 0), (40, 0)]))
        P.scale("bong", ln(f, [(0, 1), (13.5, 1), (14, 1.2), (16, 0.95), (19, 1.08), (22, 1)]), ln(f, [(0, 1), (13.5, 1), (14, 0.84), (16, 1.04), (19, 0.94), (22, 1)]))
        # đuôi: quất lên lúc bị hất, rồi duỗi thẳng rũ xuống đất
        duoi_ru = ln(f, [(0, 0), (11, 0), (13, 1.25), (17, 0.85), (22, 1.05), (40, 1)])
        for i, b in enumerate(duoi):
            P.rot(b, float(A_DUOI[i]) * 1.1 * ln(f - 0.7 * i, [(0, 0), (2, 1), (8, -0.5), (12, 0)]) + (-9, 4, 9, 12, 13, 12, 10)[i] * duoi_ru)
        for i, b in enumerate(vl):
            P.rot(b, (10, 16)[i] * ln(f - i, [(0, 0), (2, 1), (10, -0.4), (12, -1.1), (16, 0.5), (22, 0.9), (40, 0.9)]))
        for i, b in enumerate(vb):
            P.rot(b, (8, 14)[i] * ln(f - i, [(0, 0), (12, 0), (13, -1), (17, 0.4), (22, -0.6), (40, -0.6)]))
        a = 2 * math.pi * f / 11.0                                            # mắt quay vòng
        rr = ln(f, [(0, 0), (2, 1), (40, 1)])
        P.move("mat_g", (-5 + 6 * math.cos(a)) * S * rr, (1 + 5 * math.sin(a)) * S * rr)
        P.move("mat_x", (-3 + 3.5 * math.cos(a + 1)) * S * rr, (1 + 4 * math.sin(a + 1)) * S * rr)
        P.scale("mat_g", 1 - 0.3 * rr, 1 - 0.3 * rr)
        P.scale("mat_x", 1 - 0.3 * rr, 1 - 0.3 * rr)
        if f > 30:
            an_het(P, ln(f, [(30, 1), (39, 0), (40, 0)]))

    return [Clip("appear", 30 / F, appear_fn, ev=[(A_DAT / F, "cham_dat", "")], mem=mem()),
            Clip("idle", 64 / F, idle_fn, loop=True, mem=mem()),
            Clip("attack", 30 / F, attack_fn, ev=[(13 / F, "trung", "")], mem=mem()),
            Clip("cast", (36 + XC) / F, cast_fn, ev=[(C_PHUN / F, "phun", ""), ((C_HET + XC) / F, "het_phun", "")], mem=mem()),
            Clip("skill", (48 + XK) / F, skill_fn, ev=[(K_DAM / F, "dam", ""), (K_PHUN / F, "phun", ""), ((K_HET + XK) / F, "het_phun", "")],
                 trung=K_PHUN / F, mem=mem()),
            Clip("hit", 15 / F, hit_fn, mem=mem()),
            Clip("die", 40 / F, die_fn, mem=mem())]


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
    bg = nen_trang(a)
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


def rig(k, tien_hoa=None):
    """dựng, nướng, xuất dạng k vào inbox/ca_den_<k>/rig/. tien_hoa = (sk2, info2, fr2, cl2): gộp dạng sau cho clip evolve."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    sk, info = dung(k)
    cl = clips(sk, info, k)
    fr = nuong_het(sk, cl)
    ra = os.path.join(d_inbox(k), "rig")
    os.makedirs(ra, exist_ok=True)
    if info["ti"] == 1.0:
        so_concept(sk, fr, k, os.path.join(ra, "so_concept.png"))
    ve = soi.Ve(sk)
    cao = soi.chieu_cao(ve, fr["idle"][0], bo=("den",))                       # chiều cao game: đỉnh vây lưng, không tính cần đèn
    ten = f"{CODE}_{k}"
    ch = CHAM[k]
    noi = {}
    M, clM, frM = sk, cl, fr
    if tien_hoa:
        sk2, info2, fr2, cl2 = tien_hoa
        h2 = soi.chieu_cao(soi.Ve(sk2), fr2["idle"][0], bo=("den",))
        ti = cao / h2
        M = tienhoa.gop(sk, sk2)
        Lm2 = info2["Lm"]

        def gong(t, P):                                                       # dạng cũ: ngả người, bụng phình rung, cần đèn dựng lên
            g = hoat.cv(t, [(0, 0), (0.3, -0.3), (0.6, 1, "out"), (1.3, 1.15)])
            r = hoat.rung(t, 0.45, 1.35, moi=1)
            P.rot("than", 9 * g)
            P.move("than", -6 * g, 5 * g)
            bg_ = (1 + 0.36 * max(g, 0)) * (1 + 0.03 * r)
            P.scale("bung", bg_, bg_)
            for i, b in enumerate(info["den"]):
                P.rot(b, 7 * max(g, 0) + 0.6 * r)
            for i, b in enumerate(info["duoi"]):
                P.rot(b, -2.5 * g + 1.5 * r * (1 if i % 2 else -1))
            P.scale("mat_g", 1 - 0.2 * max(g, 0), 1 - 0.2 * max(g, 0))
            P.scale("mat_x", 1 - 0.2 * max(g, 0), 1 - 0.2 * max(g, 0))

        def gam(t, P, fl):                                                    # dạng sau: chồm tới há miệng gầm
            r = hoat.rung(t, 2.0, 2.4, moi=1)
            m = fl * (1 + 0.06 * r)
            if info2.get("o") is not None and m >= NG_HA:
                P.att["n_ha"] = "n_ha"
                for sl in SLOT_KHEP:
                    P.att["n_" + sl] = None
                P.rot("n_dau", O_DAU * (m - 1))
                P.rot("n_lung", LUNG * O_DAU * (m - 1))
                P.rot("n_ham", -O_HAM * (m - 1))
            else:
                P.rot("n_dau", HA_DAU * m)
                P.rot("n_lung", LUNG * HA_DAU * m)
                P.rot("n_ham", -HA_HAM * m)
                P.move("n_moi_g", 0, info2["ha"]["A"] * max(m, 0))
                P.move("n_ham_g", 0, -info2["ha"]["B"] * max(m, 0))
            P.rot("n_than", -7 * fl)
            P.scale("n_than", 1 + 0.04 * fl, 1 - 0.03 * fl)
            for i, b in enumerate(info2["den"]):
                P.rot("n_" + b, 5 * fl)
            for i, b in enumerate(info2["duoi"]):
                P.rot("n_" + b, (3 + i) * fl * (0.6 + 0.4 * r * (1 if i % 2 else -1)))

        memM = cl[1].mem + tienhoa.doi_ten_mem(cl2[1].mem)
        ev = tienhoa.clip_tien_hoa(M, sk, sk2, fr2["idle"][0], tiB=ti, fnA=gong, fnB=gam, mem=memM)
        clM = cl + [ev]
        frM = dict(fr)
        frM["evolve"] = hoat.nuong(M, ev)
        khop_dau(frM["evolve"], fr["idle"][0])
        _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, fr2["idle"][0], ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
        print("  evolve:", noi["evolve"])
    tk = xuat.xuat_het(M, clM, ra, ten, f"Cá đèn lồng dạng {k}", frames=frM, dang=k, so_dang=2, dung_yen=("cast", "skill"), cao=cao,
                       khop_idle=0, ma_goc=3233, noi_them=noi,
                       can=[("can_mieng_cast", "cast", 20 / 30.0 * ch, "mieng", 0.42 * info["H"]),
                            ("can_quat", "attack", 13 / 30.0 * ch, "dau", 0.7 * info["H"]),
                            ("can_gam", "skill", 22 / 30.0 * ch, "mieng", 0.5 * info["H"]),
                            ("can_dung_1_chan", "skill", 12 / 30.0 * ch, "than", 0.75 * info["H"]),
                            ("can_chet", "die", 26 / 30.0 * ch, "than", 0.8 * info["H"])])
    print(f"dạng {k}: đỉnh {info['dinh']}, hở {info['ho']}; cao {cao:.0f} px rig; .atomik {tk['atomik_kb']:.0f} KB -> {ra}")
    return sk, info, fr, cl


if __name__ == "__main__":
    arg = sys.argv[1:]
    if arg[:1] == ["cat"]:
        for kk in ([int(arg[1])] if len(arg) > 1 else [1, 2]):
            cat(kk)
    elif arg[:1] == ["rig"]:
        rig(int(arg[1]))
    elif arg[:1] == ["all"]:
        rig(2)
        sk2, info2 = dung(2, ti=0.6, thua=1.8)                                # bản nhẹ của dạng 2 gộp vào dạng 1
        cl2 = clips(sk2, info2, 2)
        rig(1, tien_hoa=(sk2, info2, nuong_het(sk2, cl2), cl2))
    else:
        print(__doc__)
