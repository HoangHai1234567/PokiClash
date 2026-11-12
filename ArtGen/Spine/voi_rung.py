# -*- coding: utf-8 -*-
"""Ma mút rừng (mã làm việc voi_rung): tướng thứ 5 đảo Mộc. Cắt mảnh GPT (đúng chỗ, đúng cỡ như concept), tự dựng xương, lưới,
trọng số, clip (thư viện quai/), xuất JSON Spine 4.2 + .atomik. Không có rig gốc.

    py -3 -I ArtGen/Spine/voi_rung.py cat          tách mảnh từ B01, H01, G01, T01 -> inbox/voi_rung_2/manh/ + so_ghep.png
    py -3 -I ArtGen/Spine/voi_rung.py luoi [ảnh] [ra]   ảnh kẻ lưới toạ độ (đọc khớp)
    py -3 -I ArtGen/Spine/voi_rung.py rig          dựng rig, nướng clip, xuất -> inbox/voi_rung_2/rig/
    py -3 -I ArtGen/Spine/voi_rung.py soi <clip> <giây,giây,...> [cx,cy,r]     dựng nhanh vài khung (không xuất)
Dạng: biến môi trường VR_DANG = 2 (trưởng thành, mặc định) | 1 (voi con; `rig` gộp bản nhẹ của dạng 2 và thêm clip evolve).
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
from quai import anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat  # noqa: E402
from quai.hoat import Clip, LoXo, an_hien, cv, ease, lui, rung, song, bao  # noqa: E402
from quai.khung import Dat  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
CODE = "voi_rung"
K = int(os.environ.get("VR_DANG", "2"))        # dạng đang làm: 2 = trưởng thành (mặc định), 1 = voi con
INBOX = TAI = MANH = RIG = None
CFG = None
INK = np.array([43, 33, 24], np.float32)
SC = 0.5                    # px concept -> đơn vị rig (pixel atlas)

# ---------------------------------------------------------------- số đọc trên concept đã duyệt (px khung 1536 x 1024)
CFG2 = dict(
    dat=915, x0=670,                       # mặt đất (đáy bàn chân gần), tâm giữa bốn chân
    # ảnh nguồn -> các mảnh và tâm ước chừng của từng mảnh
    nguon={"B01": {"ao": (600, 500)},                        # khối áo liền (lượt 2): chỉ để dựng lõi nền và so ghép
           "C01": {"la_day": (720, 700)}, "C02": {"la_giua": (700, 590)}, "C03": {"la_tren": (740, 380)},
           "H02": {"so": (1050, 600)}, "F01": {"mai": (985, 440)},
           "G01": {"chan_1": (365, 780), "chan_2": (652, 790), "chan_4": (975, 790), "duoi": (230, 790)},
           "T01": {"nga_g": (945, 665), "nga_x": (1250, 650)}},
    than=(570, 610), hong=(380, 640), nguc=(790, 610),
    co=(890, 500),                          # khớp cổ (đầu gật quanh đây)
    voi=[(1104, 700), (1126, 752), (1152, 810), (1200, 840), (1250, 815), (1290, 785)],     # trục vòi: gốc (giữa đường cắt) -> chóp
    voi_cat=[(1172, 648), (1036, 752)],     # đường cắt gốc vòi: mép phải vòi -> chỗ mép dưới vòi gặp hàm
    mat=(968, 505, 46),                     # mắt: tâm, bán kính dò
    nga_goc={"nga_g": (885, 590), "nga_x": (1150, 590)},           # gốc hai ngà (xương riêng để thò ra / thụt vào)
    mu_goc=(985, 345),                      # xương mái lá của đầu
    # các lọn mái rủ: (x0, y0, x1, y1, y cuống): trong hộp, dưới cuống thì chuyển dần sang xương lọn
    lon=[(760, 430, 885, 620, 455), (885, 410, 1050, 560, 432), (1050, 380, 1215, 520, 400), (1030, 520, 1175, 630, 525)],
    lop={
        "la_day": dict(ten="d", y=650, dai=170, x=[220, 460, 700, 940, 1220], nhanh=1.9),
        "la_giua": dict(ten="g", y=500, dai=260, x=[220, 460, 700, 940, 1220], nhanh=1.5),
        # cụm lá to của lớp trên: (x0, x1, x cuống, y cuống); chỏm lá: gốc và khoảng x
        "la_tren": dict(cum=[(300, 610, 500, 300), (610, 860, 735, 240), (860, 1215, 990, 310)], chom_goc=(720, 262), chom_x=(480, 940)),
    },
    ao_cat=(840, 560, 272, 320),            # mép phải các lớp lá của thân (phần GPT vẽ bù sau đầu) gọt theo cung elip (tâm x, y, bán kính x, y)
                                            # rồi kẻ mực: đầu cúi / ngẩng lộ ra thì thấy một vai áo tròn, không phải mép thẳng
    bung=(315, 500, 1050, 792),             # khối bụng (da) nấp sau tấm áo: hộp bo tròn (lấp khe giữa các mũi lá khi đầu, chân dời đi)
    chan={"chan_1": ("hong", 365), "chan_2": ("than", 652), "chan_3": ("nguc", 835), "chan_4": ("nguc", 975)},
    chan_3=dict(tu="chan_2", ti=0.62, cx=835, day=884),            # chân nhỏ khuất giữa: dùng lại ảnh chân thứ hai
    duoi=[(292, 668), (262, 715), (240, 760), (228, 850)],
)
THU_TU = ["bung", "duoi", "chan_3", "chan_1", "chan_2", "chan_4", "loi", "la_day", "la_giua", "la_tren", "nga_x", "so", "mi", "mai", "nga_g"]
N_VOI = 9
# dạng 1 (voi con, hướng B "nam_la" người dùng chọn 2026-11-12): số đọc trên inbox/voi_rung_1/tai_ve/L1_duyet.png
CFG1 = dict(
    dat=945, x0=680,
    nguon={"B01": {"ao": (600, 540)},
           "C01": {"la_day": (600, 740)}, "C02": {"la_giua": (600, 600)}, "C03": {"la_tren": (680, 350)},
           "H02": {"so": (1020, 640)}, "F01": {"mai": (975, 440)},
           "G01": {"chan_1": (410, 860), "chan_2": (655, 860), "chan_4": (948, 860), "duoi": (255, 820)},
           "T01": {"nga_g": (915, 695), "nga_x": (1185, 685)}},
    than=(620, 650), hong=(430, 690), nguc=(800, 650),
    co=(865, 580),
    voi=[(1032, 711), (1080, 778), (1125, 825), (1165, 845), (1205, 815), (1235, 795)],
    voi_cat=[(1128, 645), (942, 784)],
    mat=(957, 565, 78),
    nga_goc={"nga_g": (880, 680), "nga_x": (1130, 665)},
    mu_goc=(975, 340),
    lon=[(740, 470, 855, 640, 500), (855, 430, 1030, 580, 465), (1030, 430, 1215, 640, 470)],
    lop={
        "la_day": dict(ten="d", y=700, dai=150, x=[240, 440, 630, 820, 1020], nhanh=1.9),
        "la_giua": dict(ten="g", y=520, dai=190, x=[240, 440, 630, 820, 1020], nhanh=1.5),
        "la_tren": dict(cum=[(280, 610, 510, 300), (610, 880, 760, 250), (880, 1120, 990, 300)], chom_goc=(737, 226), chom_x=(680, 860)),
    },
    ao_cat=(780, 650, 270, 330), ao_cat_x=880, ao_cat_y=405,     # phần lá ló trên đỉnh đầu không gọt (mép gọt ngang nấp sau mái lá cả khi đầu cúi, mái úp xuống)
    bung=(340, 560, 1010, 800),
    chan={"chan_1": ("hong", 410), "chan_2": ("than", 655), "chan_3": ("nguc", 800), "chan_4": ("nguc", 948)},
    chan_3=dict(tu="chan_2", ti=0.6, cx=800, day=927),
    duoi=[(300, 745), (280, 790), (262, 830), (250, 885)],
    y_cao=205,                              # chiều cao cho game tính tới đỉnh ụ lá (không tính mầm xoắn chìa lên)
)
CFGS = {2: CFG2, 1: CFG1}


def chon(k):
    """đổi dạng đang làm (thư mục và bảng số)."""
    global K, INBOX, TAI, MANH, RIG, CFG
    K = k
    INBOX = os.path.join(HERE, "inbox", f"{CODE}_{k}")
    TAI, MANH, RIG = os.path.join(INBOX, "tai_ve"), os.path.join(INBOX, "manh"), os.path.join(INBOX, "rig")
    CFG = CFGS.get(k)
    if CFG is None:
        raise SystemExit(f"chưa có bảng số (CFG) cho dạng {k}")




def concept():
    return os.path.join(TAI, "L1_duyet.png")


def doc(p):
    return np.array(Image.open(p).convert("RGB")).astype(np.float32)


def tg(p):
    """px concept -> thế giới rig (x phải, y lên, gốc ở chân)."""
    return ((p[0] - CFG["x0"]) * SC, (CFG["dat"] - p[1]) * SC)


def nen_trang(a, thr=236):
    sang = (a.min(2) >= thr).astype(np.uint8)
    n, lab = cv2.connectedComponents(sang, connectivity=4)
    vien = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    return np.isin(lab, vien[vien != 0])


def rgba(a, m):
    """mảnh RGBA: dải 2 px sát mép lấy màu mực, độ đậm theo độ tối (không viền sáng)."""
    mn = a.min(2)
    band = m & (cv2.dilate((~m).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0)
    al = m.astype(np.float32)
    al[band] = np.clip((246 - mn[band]) / 120.0, 0, 1)
    rgb = a.copy()
    rgb[band] = INK
    return np.dstack([np.clip(rgb, 0, 255), al * 255]).astype(np.uint8)


def co_gian(im, w, h):
    f = im.astype(np.float32)
    f[..., :3] *= f[..., 3:4] / 255.0
    f = cv2.resize(f, (int(w), int(h)), interpolation=cv2.INTER_AREA if w < im.shape[1] else cv2.INTER_CUBIC)
    al = np.clip(f[..., 3:4], 0, 255)
    f[..., :3] = np.where(al > 0.5, f[..., :3] * 255.0 / np.maximum(al, 0.5), 0)
    return np.clip(f, 0, 255).astype(np.uint8)


def moi_nhat(ten):
    """ảnh mới nhất của một bước (B01.png, B01_2.png...)."""
    c = [f for f in os.listdir(TAI) if f == ten + ".png" or (f.startswith(ten + "_") and f.endswith(".png"))]
    if not c:
        return None
    return os.path.join(TAI, max(c, key=lambda f: os.path.getmtime(os.path.join(TAI, f))))


# ---------------------------------------------------------------- cắt
def cat():
    os.makedirs(MANH, exist_ok=True)
    boxes = {}
    for src, parts in CFG["nguon"].items():
        p = moi_nhat(src)
        if not p:
            print(f"  thiếu {src}")
            continue
        a = doc(p)
        bg = nen_trang(a)
        n, lab, st, cen = cv2.connectedComponentsWithStats((~bg).astype(np.uint8), connectivity=8)
        cs = sorted([i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] >= 120], key=lambda i: -st[i, cv2.CC_STAT_AREA])
        names = list(parts)
        chinh = {}
        for i in cs[:len(names)]:                         # cụm lớn nhất -> tên có tâm ước gần nhất
            cx, cy = cen[i]
            ten = min((t for t in names if t not in chinh), key=lambda t: math.hypot(cx - parts[t][0], cy - parts[t][1]))
            chinh[ten] = [i]
        for i in cs[len(names):]:                         # mẩu nhỏ: nhập vào mảnh sát nó (< 26 px), không thì bỏ
            x, y, w, h = st[i, :4]
            best, bd = None, 26
            for ten, ids in chinh.items():
                X, Y, Wd, Hd = st[ids[0], :4]
                d = max(max(X, x) - min(X + Wd, x + w), max(Y, y) - min(Y + Hd, y + h))
                if d < bd:
                    best, bd = ten, d
            if best:
                chinh[best].append(i)
            else:
                print(f"  {src}: bỏ mẩu rời {st[i, cv2.CC_STAT_AREA]} px ở ({cen[i][0]:.0f}, {cen[i][1]:.0f})")
        if len(chinh) != len(names):
            raise SystemExit(f"{src}: tìm được {len(chinh)} mảnh, cần {len(names)}")
        for ten, ids in chinh.items():
            m = np.isin(lab, ids)
            ys, xs = np.nonzero(m)
            x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(a.shape[1], xs.max() + 4), min(a.shape[0], ys.max() + 4)
            Image.fromarray(rgba(a, m)[y0:y1, x0:x1], "RGBA").save(os.path.join(MANH, ten + ".png"))
            boxes[ten] = [int(x0), int(y0), int(x1), int(y1)]
            print(f"  {src} -> {ten}: {x1 - x0} x {y1 - y0} tại ({x0}, {y0}), {int(m.sum())} px")
    cu = {}
    pj = os.path.join(MANH, "manh.json")
    if os.path.exists(pj):
        cu = json.load(open(pj, encoding="utf-8"))
    cu.update(boxes)
    json.dump(cu, open(pj, "w", encoding="utf-8"), indent=1)
    so_ghep()


def got_mep(a, box):
    """gọt mép phải một lớp lá của thân theo cung elip CFG["ao_cat"] (chỉ vùng nấp sau đầu), kẻ mực mép gọt."""
    ex, ey, rx, ry = CFG["ao_cat"]
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    X, Y = xx + box[0], yy + box[1]
    bo = (X > CFG.get("ao_cat_x", 960)) & (Y > CFG.get("ao_cat_y", -1)) & ((((X - ex) / rx) ** 2 + ((Y - ey) / ry) ** 2) > 1.0)
    co_ = a[..., 3] > 120
    mep = co_ & ~bo & (cv2.dilate((bo & co_).astype(np.uint8), np.ones((15, 15), np.uint8)) > 0)
    a = a.copy()
    a[mep] = (43, 33, 24, 255)
    a[bo, 3] = 0
    ys, xs = np.nonzero(a[..., 3] > 0)
    a = a[:, :xs.max() + 4].copy()
    return a, [box[0], box[1], box[0] + a.shape[1], box[3]]


def ve_loi(ao, box):
    """lõi nền của khối lá: hình bóng khối áo co vào 14 px, tô lục sẫm phẳng, không viền. Nằm sau ba lớp lá: lá lay hở khe thì
    thấy màu lá sẫm chứ không thấy bụng hay nền."""
    al = ao[..., 3] > 120
    rgb = ao[..., :3].astype(np.float32)
    sam = al & (rgb[..., 1] > rgb[..., 0] + 30) & (rgb[..., 1] < 170)
    col = np.median(rgb[sam], 0) * 0.86 if sam.sum() > 100 else np.array([30, 110, 60], np.float32)
    m = cv2.erode(al.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (29, 29))) > 0
    m[int(m.shape[0] * 0.8):] = False                      # không phủ tầng lá dưới cùng (lục tươi)
    mm = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 2.0)
    out = np.zeros(ao.shape, np.float32)
    out[..., :3] = col
    out[..., 3] = mm * 255
    return np.clip(out, 0, 255).astype(np.uint8), list(box)


def nap():
    """mảnh cỡ gốc (RGBA numpy) + hộp trên concept; thêm các mảnh dựng bằng mã / dùng lại (lõi áo, chân 3, bụng, mí)."""
    bx = json.load(open(os.path.join(MANH, "manh.json"), encoding="utf-8"))
    pc = {t: np.array(Image.open(os.path.join(MANH, t + ".png")).convert("RGBA")) for t in bx}
    for t in ("ao", "la_day", "la_giua", "la_tren"):
        if t in pc:
            pc[t], bx[t] = got_mep(pc[t], bx[t])
    if "ao" in pc:
        pc["loi"], bx["loi"] = ve_loi(pc["ao"], bx["ao"])
    c3 = CFG["chan_3"]
    if c3["tu"] in pc:
        s = pc[c3["tu"]]
        w, h = int(round(s.shape[1] * c3["ti"])), int(round(s.shape[0] * c3["ti"]))
        pc["chan_3"] = co_gian(s, w, h)
        bx["chan_3"] = [int(c3["cx"] - w / 2), c3["day"] - h, int(c3["cx"] - w / 2) + w, c3["day"]]
    mau = mau_da(pc)
    pc["bung"], bx["bung"] = ve_bung(mau)
    if "so" in pc:
        r = mi_mat(pc["so"], bx["so"], mau)
        if r:
            pc["mi"], bx["mi"] = r
    return pc, bx


def mau_da(pc):
    """màu da (trung vị) + ô vân sáp lấy từ chân."""
    for t in ("chan_2", "chan_1", "chan_4"):
        if t in pc:
            a = pc[t].astype(np.float32)
            h, w = a.shape[:2]
            o = a[int(h * 0.25):int(h * 0.6), int(w * 0.3):int(w * 0.7)]
            ok = (o[..., 3] > 250) & (o[..., :3].min(2) > 60)
            if ok.sum() > 100:
                return np.median(o[ok][:, :3], 0), o[..., :3]
    return np.array([86, 104, 120], np.float32), None


def ve_bung(mau):
    """khối bụng nấp sau tấm áo: hộp bo tròn tô màu da (lát vân sáp của chân), viền mực. Tô phẳng nên vẽ bằng mã được."""
    col, van = mau
    x0, y0, x1, y1 = CFG["bung"]
    w, h = x1 - x0, y1 - y0
    S = 2
    m = Image.new("L", (w * S, h * S), 0)
    ImageDraw.Draw(m).rounded_rectangle([4 * S, 4 * S, (w - 4) * S, (h - 4) * S], radius=int(0.42 * h * S), fill=255)
    m = np.array(m.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255.0
    rgb = np.empty((h, w, 3), np.float32)
    rgb[...] = col
    if van is not None and van.shape[0] > 20 and van.shape[1] > 20:
        t = np.concatenate([van, van[:, ::-1]], 1)
        t = np.concatenate([t, t[::-1]], 0)
        rgb = np.tile(t, (h // t.shape[0] + 1, w // t.shape[1] + 1, 1))[:h, :w].copy()
        rgb += col - np.median(rgb.reshape(-1, 3), 0)
    inner = cv2.erode((m > 0.5).astype(np.uint8), np.ones((13, 13), np.uint8)) > 0
    rgb[(m > 0.05) & ~inner] = INK
    return np.dstack([np.clip(rgb, 0, 255), m * 255]).astype(np.uint8), (x0, y0, x1, y1)


def mi_mat(dau, box, mau):
    """mí mắt nhắm: phủ lòng mắt (hổ phách, con ngươi, chấm trắng) và viền dưới của nó bằng màu da, rồi kẻ một nét mực theo mép
    dưới lòng mắt (mắt nhắm). Không đè lên lá của mái (mái lá và nét mày phía trên giữ nguyên)."""
    ex, ey, er = CFG["mat"]
    cx, cy = ex - box[0], ey - box[1]
    a = dau.astype(np.float32)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    trong = np.hypot(xx - cx, yy - cy) < er
    vang = trong & (R > 190) & (G > 120) & (B < 130)
    if vang.sum() < 60:
        print("  mí mắt: không dò ra lòng mắt")
        return None
    pts_ = np.argwhere(vang)[:, ::-1].astype(np.int32)           # bao lồi của phần hổ phách: lấy luôn con ngươi, chấm trắng
    long_ = np.zeros(vang.shape, np.uint8)
    cv2.fillConvexPoly(long_, cv2.convexHull(pts_), 1)
    long_ = long_ > 0
    la = (G > R + 25) & (G > B + 20)
    phu = long_.copy()
    cols = np.flatnonzero(long_.any(0))
    ylow = {}
    for c in cols:
        rows = np.flatnonzero(long_[:, c])
        ylow[c] = rows.max()
        phu[max(0, rows.min() - 7):rows.max() + 10, max(0, c - 8):c + 9] = True
    phu &= ~la
    phu &= ~(cv2.dilate(la.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0) | long_      # chừa viền mực của lá
    ys, xs = np.nonzero(phu)
    x0, y0, x1, y1 = xs.min() - 3, ys.min() - 3, xs.max() + 4, ys.max() + 4
    al = cv2.GaussianBlur(phu[y0:y1, x0:x1].astype(np.float32), (0, 0), 0.8) * 255
    rr = np.hypot(xx - cx, yy - cy)                               # màu mí = màu da ngay quanh mắt (khỏi lệch tông với mặt)
    quanh = (rr > er * 0.9) & (rr < er * 1.7) & (a[..., 3] > 250) & (B > R + 12) & (a[..., :3].min(2) > 70) & ~la
    da = np.median(a[quanh][:, :3], 0) if quanh.sum() > 80 else mau[0]
    im = np.zeros((y1 - y0, x1 - x0, 4), np.float32)
    im[..., :3] = da
    im[..., 3] = al
    pil = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(pil)
    cs = sorted(ylow)
    yl = np.array([ylow[c] for c in cs], np.float32)
    yl = cv2.GaussianBlur(yl[None, :], (0, 0), 4)[0]
    pts = [(c - x0, float(v) - y0 + 2) for c, v in zip(cs, yl)][2:-2]
    d.line(pts, fill=(43, 33, 24, 255), width=6, joint="curve")
    return np.array(pil), (box[0] + int(x0), box[1] + int(y0), box[0] + int(x1), box[1] + int(y1))


def dan(canvas, im, x, y):
    H, W = canvas.shape[:2]
    h, w = im.shape[:2]
    X0, Y0, X1, Y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if X1 <= X0 or Y1 <= Y0:
        return
    s = im[Y0 - y:Y1 - y, X0 - x:X1 - x].astype(np.float32)
    al = s[..., 3:4] / 255.0
    d = canvas[Y0:Y1, X0:X1]
    d[..., :3] = d[..., :3] * (1 - al) + s[..., :3] * al
    d[..., 3:4] = d[..., 3:4] * (1 - al) + 255.0 * al


def so_ghep():
    """ghép các mảnh theo thứ tự vẽ ngay tại chỗ, so với concept."""
    pc, bx = nap()
    ac = doc(concept())
    cv_ = np.zeros(ac.shape[:2] + (4,), np.float32)
    for t in THU_TU:
        if t in pc and t != "mi":
            dan(cv_, pc[t], bx[t][0], bx[t][1])
    al = cv_[..., 3:4] / 255.0
    gh = cv_[..., :3] * al + 255.0 * (1 - al)
    fg_c, fg_g = ~nen_trang(ac), cv_[..., 3] > 110
    thieu, thua = int((fg_c & ~fg_g).sum()), int((fg_g & ~fg_c).sum())
    lech = np.abs(gh - ac).max(2)
    khac = int(((lech > 70) & fg_c & fg_g).sum())
    print(f"  ghép so concept: thiếu {thieu} px, thừa {thua} px, khác màu rõ {khac} px (concept có {int(fg_c.sum())} px)")
    d = np.zeros_like(ac)
    d[...] = 255
    d[fg_c & fg_g] = (200, 200, 200)
    d[fg_c & ~fg_g] = (255, 0, 0)
    d[fg_g & ~fg_c] = (0, 160, 0)
    d[(lech > 70) & fg_c & fg_g] = (0, 0, 255)
    out = np.concatenate([ac, gh, d], 1).astype(np.uint8)
    Image.fromarray(out).resize((out.shape[1] // 2, out.shape[0] // 2), Image.LANCZOS).save(os.path.join(MANH, "so_ghep.png"))
    Image.fromarray(gh.astype(np.uint8)).save(os.path.join(MANH, "ghep.png"))
    ten = [t for t in THU_TU if t in pc]                 # tờ mảnh rời trên nền xám
    cw, ch = 400, 330
    sh = Image.new("RGB", (cw * 4, ch * ((len(ten) + 3) // 4)), (150, 150, 150))
    dr = ImageDraw.Draw(sh)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
    for i, t in enumerate(ten):
        im = Image.fromarray(pc[t], "RGBA")
        k = min((cw - 20) / im.width, (ch - 40) / im.height, 1.0)
        im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
        x, y = (i % 4) * cw + 10, (i // 4) * ch + 28
        sh.paste(im, (x, y), im)
        dr.text((x, y - 22), f"{t}  {pc[t].shape[1]}x{pc[t].shape[0]}", fill=(255, 255, 255), font=f)
    sh.save(os.path.join(MANH, "to_manh.png"))


def ke_luoi(src=None, ra=None, buoc=50):
    im = Image.open(src or concept()).convert("RGB")
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    for x in range(0, im.width, buoc):
        d.line([(x, 0), (x, im.height)], fill=(255, 0, 0) if x % 100 == 0 else (255, 170, 170), width=1)
        if x % 100 == 0:
            d.text((x + 2, 2), str(x), fill=(200, 0, 0), font=f)
    for y in range(0, im.height, buoc):
        d.line([(0, y), (im.width, y)], fill=(255, 0, 0) if y % 100 == 0 else (255, 170, 170), width=1)
        if y % 100 == 0:
            d.text((2, y + 2), str(y), fill=(200, 0, 0), font=f)
    ra = ra or os.path.join(INBOX, "mau", "concept_luoi.png")
    im.save(ra)
    print(ra)


# ---------------------------------------------------------------- rig
def spline(pts, n):
    """n+1 điểm cách đều dọc đường Catmull-Rom qua pts."""
    P = np.asarray(pts, float)
    dense = []
    m = len(P)
    for i in range(m - 1):
        p0, p1, p2, p3 = P[max(i - 1, 0)], P[i], P[i + 1], P[min(i + 2, m - 1)]
        for k in range(24):
            t = k / 24.0
            dense.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    dense.append(P[-1])
    D = np.array(dense)
    s = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(D, axis=0).T))])
    u = np.linspace(0, s[-1], n + 1)
    return np.stack([np.interp(u, s, D[:, 0]), np.interp(u, s, D[:, 1])], 1)


def dung(nhe=1.0):
    """dựng rig dạng đang chọn: trả (sk, info). nhe < 1: bản nhẹ (ảnh nhỏ lại nên lưới cũng thưa đi) để gộp vào dạng trước cho evolve."""
    pc0, bx = nap()
    H_RIG = (CFG["dat"] - min(bx[t][1] for t in ("la_tren", "mai") if t in bx)) * SC
    pc0.pop("ao", None)
    pc = {}
    for t, im in pc0.items():
        w, h = max(2, int(round(im.shape[1] * SC * nhe))), max(2, int(round(im.shape[0] * SC * nhe)))
        pc[t] = anh.loang_mau(Image.fromarray(co_gian(im, w, h), "RGBA"))
    sk = khung.Sk(f"{CODE}_{K}")
    for t, im in pc.items():
        sk.anh(t, im)

    def dat(t):
        x0, y0, x1, y1 = bx[t]
        X, Y = tg((x0, y0))
        return Dat(X, Y, neo=(0, 0), ti=((x1 - x0) * SC / pc[t].width, (y1 - y0) * SC / pc[t].height))

    def anh_px(t, pts):
        """px concept -> px ảnh mảnh (đã co)."""
        x0, y0, x1, y1 = bx[t]
        P = np.asarray(pts, float).reshape(-1, 2)
        return np.stack([(P[:, 0] - x0) * pc[t].width / (x1 - x0), (P[:, 1] - y0) * pc[t].height / (y1 - y0)], 1)

    def cpx(t, L):
        """đỉnh lưới của mảnh t -> px concept."""
        x0, y0, x1, y1 = bx[t]
        return np.stack([x0 + L.pts[:, 0] * (x1 - x0) / pc[t].width, y0 + L.pts[:, 1] * (y1 - y0) / pc[t].height], 1)

    T = lambda p: np.array(tg(p))  # noqa: E731
    LOP_ = CFG["lop"]
    # ---- xương
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("than", "move", *T(CFG["than"]), the_gioi=True, dai=60)
    sk.xuong("hong", "than", *T(CFG["hong"]), the_gioi=True, dai=40)
    sk.xuong("nguc", "than", *T(CFG["nguc"]), the_gioi=True, dai=40)
    cha3 = lambda x: "hong" if x < 500 else ("nguc" if x > 760 else "than")  # noqa: E731
    vat = {}                                                   # lớp rủ -> danh sách chuỗi (2 đốt chĩa xuống), trái -> phải
    for t in ("la_day", "la_giua"):
        c = LOP_[t]
        ex = c["x"]
        vat[t] = []
        for i in range(len(ex) - 1):
            xm = (ex[i] + ex[i + 1]) / 2
            vat[t].append(sk.chuoi(f"{c['ten']}{i}_", cha3(xm), [T((xm, c["y"])), T((xm, c["y"] + c["dai"] * 0.5)), T((xm, c["y"] + c["dai"]))]))
    cum = []                                                   # lớp trên: mỗi cụm lá to một xương (gốc ở cuống lá, chĩa xuống) + chỏm
    for i, (x0_, x1_, px_, py_) in enumerate(LOP_["la_tren"]["cum"]):
        cum.append(sk.xuong(f"t{i}", cha3(px_), *T((px_, py_)), goc=-90, the_gioi=True, dai=60))
    sk.xuong("chom", "than", *T(LOP_["la_tren"]["chom_goc"]), goc=90, the_gioi=True, dai=50)
    sk.xuong("dau", "nguc", *T(CFG["co"]), the_gioi=True, dai=70)
    sk.xuong("so", "dau", *T(CFG["co"]), the_gioi=True, dai=60)
    sk.xuong("mu", "dau", *T(CFG["mu_goc"]), the_gioi=True, dai=50)
    lon = []                                                   # các lọn mái: mỗi lọn một xương chĩa xuống
    for i, (x0_, y0_, x1_, y1_, py_) in enumerate(CFG["lon"]):
        lon.append(sk.xuong(f"m{i}", "mu", *T(((x0_ + x1_) / 2, py_)), goc=-90, the_gioi=True, dai=40))
    Jv = np.array([T(p) for p in spline(CFG["voi"], N_VOI)])
    voi = sk.chuoi("voi", "so", Jv)
    d_tip = Jv[-1] - Jv[-2]
    sk.xuong("mieng", voi[-1], *Jv[-1], goc=math.degrees(math.atan2(d_tip[1], d_tip[0])), dai=30, the_gioi=True)
    sk.xuong("nga_g", "so", *T(CFG["nga_goc"]["nga_g"]), the_gioi=True, dai=40)
    sk.xuong("nga_x", "so", *T(CFG["nga_goc"]["nga_x"]), the_gioi=True, dai=40)
    Jd = np.array([T(p) for p in CFG["duoi"]])
    duoi = sk.chuoi("duoi", "hong", Jd)
    chan = {}
    for t, (cha, cx) in CFG["chan"].items():
        if t not in bx:
            continue
        y_dat = bx[t][3] - 4
        sk.xuong("ban_" + t[5:], "move", *T((cx, y_dat)), the_gioi=True, dai=30)
        chan[t] = (cha, "ban_" + t[5:], cx, y_dat)
    # ---- slot (sau -> trước)
    sk.slot("bung", "than", "bung")
    sk.slot("duoi", duoi[0], "duoi")
    for t in ("chan_3", "chan_1", "chan_2", "chan_4"):
        if t in chan:
            sk.slot(t, chan[t][1], t)
    for t in ("loi", "la_day", "la_giua", "la_tren"):
        sk.slot(t, "than", t)
    sk.slot("nga_x", "nga_x", "nga_x")
    sk.slot("so", "so", "so")
    if "mi" in pc:
        sk.slot("mi", "so", "mi", an=True)
    sk.slot("mai", "mu", "mai")
    sk.slot("nga_g", "nga_g", "nga_g")
    BT = dict(buoc_theo_cao=H_RIG)
    BL = dict(buoc_vien=8.5, buoc_trong=12.0)                 # các lớp lá to: lưới thưa hơn chút (ba lớp chồng nhau)

    def ba_vung(t):
        """hông / thân / ngực theo x (hoà rộng), toạ độ ảnh mảnh."""
        w, h = pc[t].size
        xa = anh_px(t, [(CFG["hong"][0] + 40, 0)])[0][0]
        xb = anh_px(t, [(CFG["nguc"][0] - 40, 0)])[0][0]
        xm = (xa + xb) / 2
        return [("hong", [(-9, -9), (xa, -9), (xa, h + 9), (-9, h + 9)]), ("nguc", [(xb, -9), (w + 9, -9), (w + 9, h + 9), (xb, h + 9)]),
                ("than", [(xm - 12, -9), (xm + 12, -9), (xm + 12, h + 9), (xm - 12, h + 9)])]

    def nen3(t, L):
        return trongso.vung(L, ba_vung(t), dai_hoa=0.2 * pc[t].width)

    # ---- bụng, lõi áo (nền lục sẫm sau các lớp lá)
    for t in ("bung", "loi"):
        im = pc[t]
        Lb = luoi.luoi_vung(im, ten=t, buoc_vien=12, buoc_trong=18)
        sk.luoi_gan(t, t, Lb, trongso.lam_tron(Lb, nen3(t, Lb), 2), dat=dat(t))
    # ---- hai lớp lá rủ (đáy, giữa): trên mức gốc bám hông / thân / ngực, dưới đó chuyển dần sang các vạt (2 đốt, lò xo)
    for t in ("la_day", "la_giua"):
        c = LOP_[t]
        im = pc[t]
        L = luoi.luoi_vung(im, ten=t, **BL)
        W0_ = nen3(t, L)
        C = cpx(t, L)
        ex = c["x"]
        y_day = bx[t][3]
        out = []
        for i in range(L.n):
            x, y = C[i]
            d = dict(W0_[i])
            if y > c["y"]:
                f = (y - c["y"]) / max(1e-6, y_day - c["y"])
                ws = {}
                for k_ in range(len(ex) - 1):
                    cc, half = (ex[k_] + ex[k_ + 1]) / 2, (ex[k_ + 1] - ex[k_]) / 2
                    dx_ = abs(x - cc)
                    if (k_ == 0 and x < cc) or (k_ == len(ex) - 2 and x > cc):
                        dx_ = 0.0
                    ws[k_] = max(0.0, 1 - dx_ / (half * 1.25)) ** 1.5
                sw = sum(ws.values()) or 1.0
                u = min(1.0, f * c.get("nhanh", 1.6)) ** 1.2
                d = {k: v * (1 - u) for k, v in d.items()}
                g = min(1.0, max(0.0, (f - 0.42) / 0.3))
                for k_, wv in ws.items():
                    if wv > 0:
                        d[vat[t][k_][0]] = d.get(vat[t][k_][0], 0) + u * wv / sw * (1 - g)
                        d[vat[t][k_][1]] = d.get(vat[t][k_][1], 0) + u * wv / sw * g
            out.append(d)
        W = trongso.lam_tron(L, trongso.chuan(out), 2)
        trongso.kiem(W, t)
        sk.luoi_gan(t, t, L, W, dat=dat(t))
    # ---- lớp lá trên: mỗi cụm lá to đung đưa quanh cuống của nó; chỏm lá có xương riêng
    t = "la_tren"
    im = pc[t]
    L = luoi.luoi_vung(im, ten=t, **BL)
    W0_ = nen3(t, L)
    C = cpx(t, L)
    cl_ = LOP_[t]["cum"]
    cgx, cgy = LOP_[t]["chom_goc"]
    out = []
    for i in range(L.n):
        x, y = C[i]
        d = dict(W0_[i])
        if y < cgy and LOP_[t]["chom_x"][0] < x < LOP_[t]["chom_x"][1]:
            u = min(1.0, max(0.0, (cgy - y) / 55.0))
            d = {k: v * (1 - u) for k, v in d.items()}
            d["chom"] = d.get("chom", 0) + u
        else:
            ws = {}
            for k_, (x0_, x1_, px_, py_) in enumerate(cl_):
                cc, half = (x0_ + x1_) / 2, (x1_ - x0_) / 2
                dx_ = abs(x - cc)
                if (k_ == 0 and x < cc) or (k_ == len(cl_) - 1 and x > cc):
                    dx_ = 0.0
                ws[k_] = (max(0.0, 1 - dx_ / (half * 1.2)) ** 1.5, min(1.0, max(0.0, (y - py_ - 15) / 110.0)))
            sw = sum(a for a, _ in ws.values()) or 1.0
            u = sum(a / sw * b for a, b in ws.values())
            d = {k: v * (1 - u) for k, v in d.items()}
            for k_, (a, b) in ws.items():
                if a * b > 0:
                    d[cum[k_]] = d.get(cum[k_], 0) + a / sw * b
        out.append(d)
    W = trongso.lam_tron(L, trongso.chuan(out), 2)
    trongso.kiem(W, t)
    sk.luoi_gan(t, t, L, W, dat=dat(t))
    # ---- đầu trọc liền vòi: phía chóp vòi của đường cắt bám chuỗi, còn lại bám sọ; tam giác vòi vẽ sau
    im = pc["so"]
    Lh = luoi.luoi_vung(im, ten="so", **BT)
    Qh = dat("so").ra(Lh.pts, *im.size)
    A_, B_ = T(CFG["voi_cat"][0]), T(CFG["voi_cat"][1])
    nrm = np.array([-(B_ - A_)[1], (B_ - A_)[0]])
    if (Jv[-1] - A_) @ nrm < 0:
        nrm = -nrm
    s_h, cumv = trongso._chieu_len_gay(Qh, Jv)
    trong_voi = (((Qh - A_) @ nrm) > 0) & (Qh[:, 1] < A_[1] + 6 * SC)
    Wc = trongso.chuoi(s_h, np.diff(cumv), voi, cha="so", cha_hoa=1.0)
    Wh = [Wc[i] if trong_voi[i] else {"so": 1.0} for i in range(Lh.n)]
    Wh = trongso.lam_tron(Lh, Wh, 2)
    trongso.kiem(Wh, "so", cho_cung=("so",))
    sv = np.where(trong_voi, np.maximum(s_h, 0), -1.0)
    Lh.tris = np.asarray(Lh.tris)[np.argsort([sv[list(t_)].max() for t_ in Lh.tris], kind="stable")]
    sk.luoi_gan("so", "so", Lh, Wh, dat=dat("so"))
    if "mi" in pc:
        sk.manh("mi", "mi", dat("mi"))
    # ---- mái lá của đầu: vòm bám `mu`, từng lọn rủ bám xương riêng (chuyển dần từ cuống lọn xuống mũi)
    im = pc["mai"]
    Lm = luoi.luoi_vung(im, ten="mai", **BT)
    C = cpx("mai", Lm)
    out = []
    for i in range(Lm.n):
        x, y = C[i]
        d = {"mu": 1.0}
        best = None
        for k_, (x0_, y0_, x1_, y1_, py_) in enumerate(CFG["lon"]):
            if x0_ <= x <= x1_ and y0_ <= y <= y1_:
                u = min(1.0, max(0.0, (y - py_) / 45.0))
                if best is None or u > best[1]:
                    best = (k_, u)
        if best and best[1] > 0:
            d = {"mu": 1 - best[1], lon[best[0]]: best[1]}
        out.append(d)
    Wm = trongso.lam_tron(Lm, trongso.chuan(out), 2)
    trongso.kiem(Wm, "mai", cho_cung=("mu",))
    sk.luoi_gan("mai", "mai", Lm, Wm, dat=dat("mai"))
    # ---- ngà: mỗi ngà một xương ở gốc ngà (con của sọ) để thò ra, thụt vào được
    sk.manh("nga_g", "nga_g", dat("nga_g"))
    sk.manh("nga_x", "nga_x", dat("nga_x"))
    # ---- đuôi
    im = pc["duoi"]
    Ld = luoi.luoi_vung(im, ten="duoi", **BT)
    Qd = dat("duoi").ra(Ld.pts, *im.size)
    sk.luoi_gan("duoi", "duoi", Ld, trongso.chuan(trongso.chuoi_chieu(Qd, Jd, duoi, cha="hong", cha_hoa=0.8)), dat=dat("duoi"))
    # ---- chân: trên bám hông / thân / ngực, dưới bám bàn chân (ống chân tự giãn, co)
    for t, (cha, ban, cx, y_dat) in chan.items():
        im = pc[t]
        Ll = luoi.luoi_vung(im, ten=t, **BT)
        Ql = dat(t).ra(Ll.pts, *im.size)
        Wl = trongso.theo_truc(Ql, T((cx, bx[t][1])), T((cx, y_dat)), cha, ban, u0=0.3, u1=0.78)
        sk.luoi_gan(t, t, Ll, Wl, dat=dat(t))
    for e, m in (("trung", "đòn thường trúng (ngà hất)"), ("tu", "bắt đầu tụ ở chóp vòi"), ("phun", "vòi bắt đầu phun (VFX bám xương mieng)"),
                 ("het_phun", "hết phun"), ("gam", "chồm lên rống"), ("dam", "hai chân trước dậm xuống (VFX sóng đất, rễ trồi)"),
                 ("dap", "chân sau đạp đất bật tới (bụi)"), ("xao_dong", "đống lá rung (lúc ra sân)"), ("chui_ra", "đầu thò ra khỏi đống lá"), ("cham_dat", "đứng dậy dậm chân (sân lắc cam)"),
                 ("hat_xi", "hắt xì (idle)")):
        sk.su_kien(e, m)
    info = dict(voi=voi, vat=vat, cum=cum, lon=lon, duoi=duoi, chan=chan, H=H_RIG, pc=pc, bx=bx)
    return sk, info


# ---------------------------------------------------------------- clip
def clips(sk, info):
    voi, vat, cum, lon, duoi, chan, H = info["voi"], info["vat"], info["cum"], info["lon"], info["duoi"], info["chan"], info["H"]
    n = len(voi)
    W0 = sk.W0
    goc0 = [khung.goc_mat(W0[b]) for b in voi]              # góc thế giới dáng gốc từng đốt vòi
    truoc = [t for t in ("chan_4", "chan_3") if t in chan]
    sau = [t for t in ("chan_1", "chan_2") if t in chan]
    co_mi = "mi" in sk.si
    DAY, GIUA = vat["la_day"], vat["la_giua"]

    def mi(P, t, kh):
        if co_mi:
            an_hien(P, "mi", t, kh)

    def voi_toi(P, dich, w=1.0):
        """đưa vòi về dáng có góc thế giới `dich` (gốc -> chóp, len tuỳ ý: nội suy), trộn w."""
        d = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(dich)), dich)
        prev = 0.0
        for i, b in enumerate(voi):
            lech = d[i] - goc0[i]
            lech = prev + ((lech - prev + 180) % 360) - 180        # liền dọc chuỗi (không nhảy 360 độ)
            P.rot(b, w * (lech - prev))
            prev = lech

    def voi_cuon(P, a):
        for i, b in enumerate(voi):
            P.rot(b, a * (0.5 + i / n))

    # dáng vòi theo góc thế giới từng đốt (gốc -> chóp). Gốc vòi dày gấp ba bề dài một đốt: bẻ gắt ở gốc là nhăn gập, nên các
    # dáng đều uốn dần từ gốc ra (dáng gốc khoảng [-67, -67, -66, -60, -40, -20, 10, 30, 37])
    V_NGAM = [-55, -42, -28, -14, -4, 2, 4, 2, 0]              # vươn ra trước, chóp chĩa ngang (ngắm bắn)
    V_HIT = [-64, -50, -26, 8, 44, 76, 98, 110, 116]           # hít hơi: cuộn chóp lên
    V_LEN = [-22, 12, 44, 70, 88, 100, 104, 96, 84]            # giơ cao rống
    V_GAI = [-40, -8, 26, 58, 88, 116, 140, 158, 170]          # cuộn lên gãi mái lá (idle)
    V_NAM = [-30, -18, -8, 0, 4, 6, 6, 4, 2]                   # duỗi nằm ra trước trên đất

    def theo(P, ban, cha, k=1.0, xoay=1.0):
        """bàn chân đi theo xương cha (ngực / hông) một phần k: nhấc chân khi thân chồm."""
        W = sk.the_gioi(P)
        M = np.linalg.inv(W["move"]) @ W[cha] @ np.linalg.inv(W0[cha]) @ W0["move"]
        p0 = np.array([sk.bones[sk.bi[ban]]["x"], sk.bones[sk.bi[ban]]["y"], 1.0])
        p1 = M @ p0
        P.move(ban, k * (p1[0] - p0[0]), k * (p1[1] - p0[1]))
        P.rot(ban, k * xoay * khung.goc_mat(M))

    def la(P, a, day=1.0, giua=0.7, tren=0.35, mai=0.8):
        """mọi lớp lá cùng lắc a độ (dương = hất ra trước); lớp trên lắc ít hơn. Các vạt cùng chiều (ngược chiều thì gập lưới)."""
        for ch_, k in ((DAY, day), (GIUA, giua)):
            for i, c in enumerate(ch_):
                for j, b in enumerate(c):
                    P.rot(b, a * k * (0.6 + 0.5 * j) * (1.0 - 0.08 * i))
        for i, b in enumerate(cum):
            P.rot(b, a * tren)
        for i, b in enumerate(lon):
            P.rot(b, a * mai)

    def gio(P, tt, amp=1.0, ck=2.0):
        """gió: sóng chạy từ đuôi lên đầu qua các vạt lá, mỗi lớp trễ một nhịp; chỏm và các lọn mái rung nhanh hơn."""
        w = 2 * math.pi / ck
        for ch_, a0, ph in ((DAY, 2.6, 0.0), (GIUA, 2.0, 0.9)):
            for i, c in enumerate(ch_):
                for j, b in enumerate(c):
                    P.rot(b, amp * a0 * (0.8 + 0.9 * j) * (math.sin(w * tt - 0.6 * i - 0.35 * j - ph) + 0.35 * math.sin(2 * w * tt - 1.1 * i - ph)))
        for i, b in enumerate(cum):
            P.rot(b, amp * 2.0 * (math.sin(w * tt - 0.7 * i - 1.8) + 0.3 * math.sin(2 * w * tt - 1.3 * i)))
        P.rot("chom", amp * 2.6 * math.sin(w * tt - 2.4))
        for i, b in enumerate(lon):
            P.rot(b, amp * (2.6 + 0.5 * i) * (math.sin(w * tt - 0.5 * i - 1.2) + 0.4 * math.sin(2 * w * tt - 0.9 * i)))

    def xu_la(P, t, t0, manh=1.0, dai=0.45):
        """một cú rùng mình xù lá: mọi lớp lá hất ra rồi lắng (so le theo lớp)."""
        if not (t0 <= t <= t0 + dai + 0.12):
            return
        for k, (grp, a0) in enumerate(((DAY, 7.0), (GIUA, 5.5))):
            f = cv(t - 0.03 * k, [(t0, 0), (t0 + 0.22 * dai, 1, "out"), (t0 + 0.5 * dai, -0.6, "io"), (t0 + 0.76 * dai, 0.3, "io"), (t0 + dai, 0, "io")])
            for i, c in enumerate(grp):
                for j, b in enumerate(c):
                    P.rot(b, manh * a0 * (0.7 + 0.6 * j) * f * (1.0 - 0.1 * i))
        f = cv(t - 0.06, [(t0, 0), (t0 + 0.22 * dai, 1, "out"), (t0 + 0.5 * dai, -0.6, "io"), (t0 + 0.76 * dai, 0.3, "io"), (t0 + dai, 0, "io")])
        for i, b in enumerate(cum):
            P.rot(b, manh * 5 * f * (1 if i % 2 == 0 else -1))
        P.rot("chom", -manh * 7 * f)
        for i, b in enumerate(lon):
            P.rot(b, manh * 9 * f)

    def nen(P, tt, amp=1.0, voi_amp=1.0):
        """nhịp nền (chu kỳ 2 s): thở (khối lá phồng), đầu gật, vòi đung đưa, gió lùa lá, đuôi ve vẩy."""
        s = song(tt, 2.0)
        P.move("than", 0, 2.6 * s * amp)
        P.scale("than", 1 + 0.012 * s * amp, 1 + 0.022 * s * amp)
        P.rot("dau", (2.0 * song(tt, 2.0, 0.6) - 0.7 * song(tt, 1.0, 0.3)) * amp)
        P.move("dau", 0, -1.2 * s * amp)
        for i, b in enumerate(voi):
            P.rot(b, voi_amp * amp * (1.5 + 0.6 * i) * math.sin(2 * math.pi * (tt - 0.1 * i) / 2.0 + 0.4))
        gio(P, tt, amp)
        for i, b in enumerate(duoi):
            P.rot(b, amp * (4.0 + 3.0 * i) * math.sin(2 * math.pi * (tt - 0.1 * i) / 1.0 + 1.0))

    mem = [LoXo(c, k=[240, 180], damp=0.45, maxang=14) for c in DAY] + [LoXo(c, k=[280, 210], damp=0.5, maxang=11) for c in GIUA] + \
          [LoXo([b], k=[300], damp=0.5, maxang=7) for b in cum] + [LoXo([b], k=[250], damp=0.45, maxang=15) for b in lon] + \
          [LoXo(["chom"], k=[300], damp=0.5, maxang=8), LoXo(duoi, k=[300, 240, 190], damp=0.5, maxang=16),
           LoXo(voi, k=[520, 460, 400, 350, 300, 260, 230, 200, 180], damp=0.65, maxang=7)]

    def hien(P, a, bo=()):
        for s in sk.slots:
            if s["alpha"] > 0 and s["name"] not in bo:
                P.alpha[s["name"]] = a

    def nhac(P, ban, h, x=0.0, r=0.0):
        P.move(ban, x, h)
        P.rot(ban, r)

    # ---- idle 4 s: nhún nhảy theo nhịp, gió lùa lá, giậm chân, cuộn vòi gãi mái lá rồi hắt xì
    def idle_fn(t, P):
        nen(P, t)
        # nhún nhảy: lắc mông - vai theo nhịp 1 s, hai chân trước thay nhau nhấc nhẹ
        lac = math.sin(2 * math.pi * t / 1.0) * cv(t, [(0, 0), (0.25, 1, "io"), (1.9, 1), (2.15, 0, "io"), (4.0, 0)])
        P.rot("than", 1.3 * lac)
        P.move("than", 2.0 * lac, 0)
        P.rot("dau", -1.6 * lac)
        for tn, sg in (("chan_4", 1.0), ("chan_2", -1.0)):
            if tn in chan:
                nhac(P, chan[tn][1], 4.5 * max(0.0, sg * lac) ** 1.5)
        # gãi mái lá bằng vòi (2,2 – 3,0), hắt xì ở 3,1
        gai = cv(t, [(0, 0), (2.15, 0), (2.55, 1, "io"), (2.95, 1), (3.1, 0.25, "in"), (3.3, 0, "out"), (4.0, 0)])
        voi_toi(P, V_GAI, 0.82 * gai)
        co = math.sin(2 * math.pi * (t - 2.55) / 0.2) if 2.55 <= t <= 2.95 else 0.0
        for i, b in enumerate(voi[-3:]):
            P.rot(b, 7 * co)
        for i, b in enumerate(lon):
            P.rot(b, (5 + 2 * i) * co * (1 if i % 2 else -1))
        P.rot("mu", 1.6 * co)
        P.rot("dau", 5 * gai)
        hx = cv(t, [(0, 0), (2.98, 0), (3.08, -1, "io"), (3.13, 1.3, "in"), (3.3, -0.3, "out"), (3.5, 0, "io"), (4.0, 0)])   # ngửa lấy hơi rồi giật xuống
        P.rot("dau", -9 * hx)
        P.move("than", -2 * hx, -3.5 * max(hx, 0))
        P.scale("than", 1 + 0.02 * max(hx, 0), 1 - 0.03 * max(hx, 0))
        xu_la(P, t, 3.11, 1.5, 0.5)
        mi(P, t, [(1.2, 1.31), (3.02, 3.34)])

    # ---- appear 2,5 s: một đống lá nằm im rung rinh; đuôi thò ra, đầu chui ra dưới mái lá, hai ngà bật ra, bốn chân đẩy đống lá
    #      đứng dậy, rùng mình xù lá
    def appear_fn(t, P, D=2.5):
        hien(P, cv(t, [(0, 0), (0.1, 1)]), bo=("mi",))
        dong = cv(t, [(0, 1), (1.22, 1), (1.42, 0.5, "io"), (1.5, 0.52), (1.72, -0.08, "io"), (1.86, 0.03, "io"), (2.0, 0, "io"), (D, 0)])   # 1 = nằm bẹp
        ha = 0.118 * H                                          # mép lá dưới cùng hạ sát đất
        P.move("than", 0, -ha * max(dong, 0) + 5 * max(-dong, 0))
        P.scale("than", 1 + 0.07 * max(dong, 0), 1 - 0.1 * max(dong, 0))
        P.rot("than", 5 * cv(t, [(0, 0), (1.22, 0), (1.42, 1, "io"), (1.72, -0.2, "io"), (1.9, 0, "io"), (D, 0)]))             # chân trước đẩy lên trước
        # đống lá rung hai lần
        for t0 in (0.14, 0.4):
            xu_la(P, t, t0, 0.8, 0.26)
            P.move("than", 0, 3.5 * cv(t, [(t0, 0), (t0 + 0.06, 1, "out"), (t0 + 0.2, 0, "in")]) if t0 <= t <= t0 + 0.2 else 0)
        # chân: thụt hết vào trong đống lá, rồi đẩy ra (trước rồi sau)
        for tn in truoc + sau:
            ban = chan[tn][1]
            t1 = 1.22 if tn in truoc else 1.5
            len_ = cv(t, [(0, 1), (t1, 1), (t1 + 0.2, 0, "io"), (D, 0)])
            cao = (CFG["dat"] - info["bx"][tn][1]) * SC * 0.62
            nhac(P, ban, cao * len_)
            P.alpha[tn] = cv(t, [(0, 0), (t1 - 0.02, 0), (t1 + 0.06, 1), (D, 1)])
        # đuôi thò ra
        dk = cv(t, [(0, 0.02), (0.56, 0.02), (0.68, 1.25, "out"), (0.78, 0.92, "io"), (0.88, 1, "io"), (D, 1)])
        P.scale(duoi[0], dk, dk)
        P.alpha["duoi"] = cv(t, [(0, 0), (0.55, 0), (0.6, 1), (D, 1)])
        for i, b in enumerate(duoi):
            P.rot(b, (10 + 6 * i) * cv(t, [(0, 0), (0.6, 0), (0.7, 1, "out"), (0.85, -0.6, "io"), (1.0, 0.3, "io"), (1.15, 0, "io"), (D, 0)]))
        # mái lá của đầu: lúc đầu úp xuống nhập vào đống lá, đầu chui ra thì bị đội lên
        up = cv(t, [(0, 1), (0.72, 1), (0.98, -0.12, "out"), (1.1, 0.04, "io"), (1.2, 0, "io"), (D, 0)])
        P.move("mu", -16 * up, -30 * up)
        P.rot("mu", -9 * up)
        # sọ + vòi: thu nhỏ nấp dưới mái lá, rồi chui ra (vòi cuộn, duỗi dần)
        sc = cv(t, [(0, 0.05), (0.72, 0.05), (0.95, 1.1, "out"), (1.06, 0.96, "io"), (1.16, 1, "io"), (D, 1)])
        P.scale("so", sc, sc)
        P.move("so", 20 * (1 - min(sc, 1)), 26 * (1 - min(sc, 1)))
        for sl in ("so",):
            P.alpha[sl] = cv(t, [(0, 0), (0.7, 0), (0.76, 1), (D, 1)])
        voi_toi(P, V_HIT, cv(t, [(0, 0.9), (0.9, 0.9), (1.25, 0, "io"), (D, 0)]))
        P.rot("dau", cv(t, [(0, -8), (0.72, -8), (0.95, 9, "out"), (1.15, 0, "io"), (1.72, 0), (1.8, -7, "out"), (2.0, 0, "io"), (D, 0)]))
        # hai ngà bật ra lần lượt
        for sl, t1 in (("nga_g", 1.0), ("nga_x", 1.1)):
            k = cv(t, [(0, 0.02), (t1, 0.02), (t1 + 0.1, 1.28, "out"), (t1 + 0.18, 0.9, "io"), (t1 + 0.26, 1, "io"), (D, 1)])
            P.scale(sl, k, k)
            P.alpha[sl] = cv(t, [(0, 0), (t1 - 0.01, 0), (t1 + 0.03, 1), (D, 1)])
        # đứng dậy xong: rùng mình xù lá, vòi giơ rống nhẹ
        xu_la(P, t, 1.74, 1.6, 0.5)
        voi_toi(P, V_LEN, 0.55 * cv(t, [(0, 0), (1.74, 0), (1.94, 1, "out"), (2.16, 0.85), (D, 0, "io")]))
        la(P, 10 * cv(t, [(0, 0), (1.22, 0), (1.42, 1, "io"), (1.72, -1.1, "in"), (1.86, 0.5, "io"), (2.0, 0, "io"), (D, 0)]))
        nen(P, lui(t, D), ease((t - 2.0) / 0.5))

    # ---- attack 1,2 s: cào đất lấy đà, chân sau ĐẠP bật cả thân chồm tới, hai chân trước giơ cao rồi NỆN xuống đúng lúc hất ngà,
    #      nhảy lùi về hai nhịp. (Người dùng 2026-11-12: "chân đạp mạnh lên chứ không move không lên thì đơn điệu quá".)
    def attack_fn(t, P, D=1.2, Hh=0.5):
        nen(P, lui(t, D), 1 - 0.9 * bao(t, 0.04, D - 0.04, 0.12, 0.22))
        T0, T1 = 0.36, 0.42                         # T0: chân sau bắt đầu đạp; T1: rời đất
        # cả con: lùi rạp -> phóng tới (bay một cung) -> nện -> nhảy lùi về hai nhịp
        P.move("move",
               cv(t, [(0, 0), (0.28, -0.08 * H, "io"), (T0, -0.09 * H), (Hh, 0.5 * H, "in"), (Hh + 0.07, 0.53 * H, "out"), (0.74, 0.5 * H),
                      (0.9, 0.24 * H, "io"), (0.96, 0.22 * H), (1.12, 0, "io"), (D, 0)]),
               cv(t, [(0, 0), (T0, 0), (0.44, 0.085 * H, "out"), (Hh, 0, "in"), (0.76, 0), (0.83, 0.03 * H, "out"), (0.9, 0, "in"),
                      (0.98, 0), (1.05, 0.025 * H, "out"), (1.12, 0, "in"), (D, 0)]))
        # thân: rạp xuống (mông cao, đầu thấp) -> ngửa vai lên lúc bật -> dộng xuống lúc nện
        ng = cv(t, [(0, 0), (0.28, -1, "io"), (T0, -1.1), (0.44, 2.6, "out"), (Hh - 0.02, 1.6), (Hh + 0.03, -1.5, "in"), (Hh + 0.16, 0.3, "out"),
                    (0.76, 0, "io"), (D, 0)])
        P.rot("than", 3.4 * ng)
        P.move("than", -5 * cv(t, [(0, 0), (0.28, 1, "io"), (T0, 1.1), (0.44, -0.6, "out"), (Hh, 0), (D, 0)]),
               cv(t, [(0, 0), (0.28, -9, "io"), (T0, -11), (0.44, 5, "out"), (Hh - 0.02, 3), (Hh + 0.03, -9, "in"), (Hh + 0.18, 1, "out"), (0.76, 0, "io"), (D, 0)]))
        P.scale("move", cv(t, [(0, 1), (T0, 1.03, "io"), (0.42, 0.97, "out"), (Hh - 0.02, 0.98), (Hh + 0.03, 1.07), (Hh + 0.16, 0.99, "out"), (0.76, 1), (D, 1)]),
                cv(t, [(0, 1), (T0, 0.96, "io"), (0.42, 1.04, "out"), (Hh - 0.02, 1.03), (Hh + 0.03, 0.92), (Hh + 0.16, 1.02, "out"), (0.76, 1), (D, 1)]))
        # đầu: cúi rạp -> hất ngà lên đúng lúc nện
        P.rot("dau", cv(t, [(0, 0), (0.28, -15, "io"), (T0 + 0.04, -18), (Hh, 20, "in"), (Hh + 0.07, 26, "out"), (0.74, 11, "io"), (0.98, 0, "io"), (D, 0)]))
        P.move("dau", cv(t, [(0, 0), (0.28, -3, "io"), (T0, -3), (Hh, 6, "in"), (0.76, 0, "io"), (D, 0)]), 0)
        w = cv(t, [(0, 0), (0.28, 1, "io"), (T0 + 0.06, 1), (Hh + 0.02, 0, "in"), (D, 0)])
        voi_toi(P, V_HIT, 0.55 * w)                 # lấy đà: cuộn vòi lên (duỗi thẳng xuống thì vòi chọc qua mặt đất)
        voi_toi(P, V_LEN, 0.5 * cv(t, [(0, 0), (Hh - 0.04, 0), (Hh + 0.08, 1, "out"), (0.72, 0.6), (0.98, 0, "io"), (D, 0)]))
        # chân trước gần: cào đất một cái lúc lấy đà
        if "chan_4" in chan:
            nhac(P, chan["chan_4"][1], 9 * cv(t, [(0, 0), (0.08, 0), (0.14, 1, "out"), (0.2, 0.15, "in"), (0.26, 0, "io"), (D, 0)]),
                 x=cv(t, [(0, 0), (0.08, 0), (0.14, 9, "out"), (0.24, -9, "in"), (0.3, 0, "io"), (D, 0)]),
                 r=cv(t, [(0, 0), (0.08, 0), (0.14, -14, "out"), (0.24, 8, "in"), (0.3, 0, "io"), (D, 0)]))
        # hai chân trước: nhấc theo vai, vươn ra trước, rồi nện xuống ở khung trúng
        for k, tn in enumerate(truoc):
            ban = chan[tn][1]
            cao = cv(t, [(0, 0), (T0 - 0.02, 0), (0.43, 1, "out"), (Hh - 0.03, 0.95), (Hh, 0, "in"), (D, 0)])
            nhac(P, ban, (30 if k == 0 else 24) * cao, x=cv(t, [(0, 0), (T0 - 0.02, 0), (0.44, 16, "out"), (Hh, 7, "in"), (0.66, 0, "io"), (D, 0)]),
                 r=-22 * cao + cv(t, [(0, 0), (Hh - 0.01, 0), (Hh + 0.02, 5), (Hh + 0.12, 0), (D, 0)]))
        # hai chân sau: ĐẠP (bàn chân miết lùi, gót nhấc) rồi rời đất, co lên, đáp sau chân trước một nhịp
        for k, tn in enumerate(sau):
            ban = chan[tn][1]
            nhac(P, ban, cv(t, [(0, 0), (T1 - 0.02, 0), (0.47, 20 - 4 * k, "out"), (Hh + 0.01, 13), (Hh + 0.05, 0, "in"), (D, 0)]),
                 x=cv(t, [(0, 0), (T0 - 0.04, 0), (T1, -15, "in"), (0.47, -6, "out"), (Hh + 0.05, 0), (D, 0)]),
                 r=cv(t, [(0, 0), (T0 - 0.04, 0), (T1, 16, "in"), (0.47, 24, "out"), (Hh + 0.05, 0, "in"), (D, 0)]))
        # nhảy lùi về: hai nhịp nhún, chân trước rồi chân sau nhấc
        for tn in truoc + sau:
            ban = chan[tn][1]
            ph = 0.0 if tn in truoc else 0.035
            nhac(P, ban, 7 * (cv(t, [(0, 0), (0.76 + ph, 0), (0.82 + ph, 1, "out"), (0.9 + ph, 0, "in"), (D, 0)]) +
                              cv(t, [(0, 0), (0.98 + ph, 0), (1.04 + ph, 1, "out"), (1.12 + ph, 0, "in"), (D, 0)])))
        # lá: bị ép về sau lúc phóng, hất tung lúc nện, nảy lúc nhảy về
        la(P, cv(t, [(0, 0), (0.28, 4, "io"), (T0, 5), (0.44, -13, "out"), (Hh - 0.02, -11), (Hh + 0.05, 13, "in"), (Hh + 0.2, -5, "io"),
                     (0.76, 0, "io"), (0.86, 4, "out"), (0.96, -2, "io"), (1.08, 3, "out"), (D, 0, "io")]))
        P.rot("chom", cv(t, [(0, 0), (T0, -3), (0.44, 7, "out"), (Hh + 0.05, -8, "in"), (Hh + 0.22, 3, "io"), (0.8, 0, "io"), (D, 0)]))
        for i, b in enumerate(duoi):                # đuôi vểnh lên lúc phóng
            P.rot(b, -(8 + 5 * i) * cv(t, [(0, 0), (T0, 0.3), (0.44, 1, "out"), (Hh + 0.1, -0.4, "io"), (0.8, 0, "io"), (D, 0)]))
        mi(P, t, [(Hh - 0.01, Hh + 0.1)])

    # ---- cast 2,0 s: hít hơi cuộn vòi, duỗi vòi ngắm, phun từ chóp vòi, giữ tới hết luồng
    def cast_fn(t, P, D=2.0, F=0.62, E=1.56):
        nen(P, lui(t, D), 1 - 0.9 * bao(t, 0.05, D - 0.05, 0.15, 0.3))
        hit_ = cv(t, [(0, 0), (0.36, 1, "io"), (0.5, 1.05), (F, 0, "in"), (D, 0)])
        ban_ = cv(t, [(0, 0), (F - 0.08, 0), (F, 1, "in"), (E, 1), (D, 0, "io")])
        voi_toi(P, V_HIT, hit_)
        voi_toi(P, V_NGAM, ban_)
        rg = rung(t, F + 0.04, E)
        for i, b in enumerate(voi):
            P.rot(b, 0.7 * rg * (1 if i % 2 else -1))
        P.scale("than", 1 + 0.04 * hit_ - 0.025 * ban_, 1 + 0.06 * hit_ - 0.03 * ban_)
        P.rot("dau", 9 * hit_ - 4 * ban_ + 0.6 * rg)
        P.move("than", -5 * hit_ + cv(t, [(0, 0), (F, 0), (F + 0.07, -9, "out"), (E, -6), (D, 0, "io")]), 3 * hit_)
        P.rot("than", 1.6 * hit_ - 1.2 * ban_)
        la(P, -6 * hit_ + 8 * cv(t, [(0, 0), (F, 0), (F + 0.1, 1, "out"), (E, 0.5), (D, 0, "io")]) + 0.9 * rg)      # hít: lá bị hút về trước mặt; phun: giật ra sau
        P.rot("chom", 4 * hit_ - 5 * ban_)
        mi(P, t, [(F - 0.02, F + 0.12)])

    # ---- skill 2,6 s: chồm hai chân trước, giơ vòi rống, dậm xuống
    def skill_fn(t, P, D=2.6, G=0.55, S=1.42):
        nen(P, lui(t, D), 1 - 0.9 * bao(t, 0.05, D - 0.05, 0.15, 0.35))
        up = cv(t, [(0, 0), (0.18, -0.12, "io"), (G, 1, "out"), (S - 0.2, 1.06, "io"), (S - 0.08, 1.1), (S, 0, "in"), (D, 0)])
        P.rot("than", 19 * up)
        P.move("than", -14 * max(up, 0), 16 * max(up, 0) - 9 * max(-up, 0))
        P.rot("dau", -7 * max(up, 0) + cv(t, [(0, 0), (G, 13, "out"), (S - 0.1, 15), (S, -15, "in"), (S + 0.25, -6, "out"), (D, 0, "io")])
              + 1.2 * rung(t, G + 0.05, S - 0.25))
        voi_toi(P, V_LEN, cv(t, [(0, 0), (0.2, 0), (G, 1, "out"), (S - 0.12, 1), (S + 0.02, 0, "in"), (D, 0)]))
        for i, b in enumerate(voi):
            P.rot(b, 1.0 * rung(t, G + 0.05, S - 0.25) * (1 if i % 2 else -1))
        voi_toi(P, V_HIT, 0.3 * cv(t, [(0, 0), (S - 0.02, 0), (S + 0.06, 1, "out"), (S + 0.4, 0, "io"), (D, 0)]))
        for tn in truoc:      # chân trước nhấc theo ngực, co lại, rồi dậm
            theo(P, chan[tn][1], "nguc", k=max(up, 0) * 0.96, xoay=1.2)
            nhac(P, chan[tn][1], 0, r=-12 * cv(t, [(0, 0), (G, 1, "out"), (S - 0.1, 1.2), (S, 0, "in"), (D, 0)]) * (1.0 if tn == "chan_4" else 0.7))
        sq = cv(t, [(0, 0), (0.18, 0.05, "io"), (0.3, -0.02), (S - 0.01, -0.02), (S + 0.05, 0.13, "out"), (S + 0.24, -0.03, "io"), (S + 0.45, 0, "io"), (D, 0)])
        P.scale("move", 1 + 0.45 * sq, 1 - sq)
        fl = cv(t, [(0, 0), (G, -1, "out"), (S - 0.1, -0.8), (S + 0.05, 1.3, "in"), (S + 0.28, -0.5, "io"), (S + 0.5, 0, "io"), (D, 0)])
        la(P, 11 * fl - 12 * max(up, 0) + 1.2 * rung(t, G + 0.05, S - 0.25))         # áo ngả ra sau lúc chồm, hất tung lúc dậm
        P.rot("chom", -8 * fl)

    # ---- hit 0,6 s
    def hit_fn(t, P, D=0.6):
        hd = cv(t, [(0, 0), (0.07, 1, "out"), (0.22, 0.5, "io"), (0.42, -0.1, "io"), (D, 0, "io")])
        bd = cv(t, [(0, 0), (0.08, 1, "out"), (0.26, 0.4, "io"), (0.45, -0.05, "io"), (D, 0, "io")])
        nen(P, lui(t, D), ease((t - 0.3) / 0.3))
        P.rot("dau", 14 * hd)
        P.rot("than", 3.5 * bd)
        P.move("than", -12 * bd, 3 * bd)
        P.move("move", -0.035 * H * bd, 0)
        voi_toi(P, V_HIT, 0.4 * hd)
        mi(P, t, [(0.03, 0.34)])
        la(P, -13 * cv(t, [(0, 0), (0.08, 1, "out"), (0.3, -0.35, "io"), (D, 0, "io")]))
        P.rot("chom", 7 * hd)
        for tn in truoc:
            theo(P, chan[tn][1], "nguc", k=0.5 * max(bd, 0))

    # ---- die 1,7 s: giật ngửa, khuỵu xuống thành một đống lá, tan
    def die_fn(t, P, D=1.7):
        P.rot("dau", cv(t, [(0, 0), (0.08, 15, "out"), (0.4, 6, "io"), (0.95, -20, "in"), (1.1, -15, "out"), (D, -17)]))
        dn = cv(t, [(0, 0), (0.08, -0.1, "out"), (0.4, 0, "io"), (0.95, 1, "in"), (1.06, 0.88, "out"), (1.2, 1, "io"), (D, 1)])
        P.rot("than", -7 * dn)
        P.move("than", 10 * dn, -44 * dn)
        P.move("dau", 0, -8 * dn)
        voi_toi(P, V_HIT, 0.35 * cv(t, [(0, 0), (0.08, 1, "out"), (0.5, 0, "io"), (D, 0)]))
        voi_toi(P, V_NAM, 0.95 * max(dn, 0))     # thân khuỵu thì vòi duỗi nằm ra trước trên đất (không chọc xuống dưới đất)
        mi(P, t, [(0.04, D + 1)])
        la(P, 12 * cv(t, [(0, 0), (0.08, -0.6, "out"), (0.4, 0, "io"), (0.95, 0), (1.02, 1, "out"), (1.25, 0.2, "io"), (D, 0.3)]))
        P.rot("chom", -8 * dn)
        for i, b in enumerate(duoi):
            P.rot(b, -(5 + 3 * i) * dn)
        a = cv(t, [(0, 1), (1.25, 1), (1.62, 0, "io"), (D, 0)])
        hien(P, a)
        if co_mi:
            P.alpha["mi"] = a

    return [Clip("appear", 2.5, appear_fn, ev=[(0.14, "xao_dong", ""), (0.8, "chui_ra", ""), (1.72, "cham_dat", "")], mem=mem),
            Clip("idle", 4.0, idle_fn, loop=True, ev=[(3.13, "hat_xi", "")], mem=mem),
            Clip("attack", 1.2, attack_fn, ev=[(0.36, "dap", ""), (0.5, "trung", "")], trung=0.5, mem=mem),
            Clip("cast", 2.0, cast_fn, ev=[(0.2, "tu", ""), (0.62, "phun", ""), (1.56, "het_phun", "")], mem=mem),
            Clip("skill", 2.6, skill_fn, ev=[(0.55, "gam", ""), (1.42, "dam", "")], trung=1.42, mem=mem),
            Clip("hit", 0.6, hit_fn, mem=mem),
            Clip("die", 1.7, die_fn, mem=mem)]


def rig():
    """dạng 2: dựng, nướng, xuất. Dạng 1: dựng thêm bản nhẹ của dạng 2, gộp vào và thêm clip evolve."""
    k = K
    noi, frames_them, sk2 = {}, {}, None
    if k == 1 and 2 in CFGS:
        chon(2)
        sk2, info2 = dung(nhe=0.6)
        cl2 = {c.ten: c for c in clips(sk2, info2)}
        idle2 = hoat.nuong(sk2, cl2["idle"])
        h2 = soi.chieu_cao(soi.Ve(sk2), idle2[0])
        chon(1)
    sk, info = dung()
    cl = clips(sk, info)
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    M = sk
    cao = (CFG["dat"] - CFG["y_cao"]) * SC if "y_cao" in CFG else None
    if sk2 is not None:
        h1 = cao or soi.chieu_cao(soi.Ve(sk), fr["idle"][0])
        ti = h1 / h2
        M = tienhoa.gop(sk, sk2)
        vat1 = [b for t in ("la_day", "la_giua") for c in info["vat"][t] for b in c]
        voi2, n2 = info2["voi"], len(info2["voi"])
        goc2 = [khung.goc_mat(sk2.W0[b]) for b in voi2]

        def gong(t, P):                             # voi con: rạp xuống, co mình thành một ụ lá, rung
            g = cv(t, [(0, 0), (0.3, -0.25), (0.62, 1, "out"), (1.35, 1.12)])
            r = rung(t, 0.5, 1.35, moi=1)
            P.move("than", 0, -14 * max(g, 0) + 3 * max(-g, 0))
            P.scale("than", 1 + 0.06 * max(g, 0), 1 - 0.08 * max(g, 0))
            P.rot("dau", -12 * g + 0.8 * r)
            P.move("dau", -6 * max(g, 0), -6 * max(g, 0))
            for i, b in enumerate(info["voi"]):
                P.rot(b, 6 * max(g, 0) + 0.8 * r * (1 if i % 2 else -1))
            for i, b in enumerate(vat1):
                P.rot(b, (5 * max(g, 0) + 2.2 * r) * (1 if i % 4 < 2 else 0.6))
            P.rot("chom", 3 * r)

        def gam(t, P, fl):                          # dạng lớn: lá xù tung, giơ vòi rống
            d = np.interp(np.linspace(0, 1, n2), np.linspace(0, 1, 9), [-22, 12, 44, 70, 88, 100, 104, 96, 84])
            prev = 0.0
            for i, b in enumerate(voi2):
                lech = d[i] - goc2[i]
                lech = prev + ((lech - prev + 180) % 360) - 180
                P.rot("n_" + b, fl * (lech - prev))
                prev = lech
            r = rung(t, 2.0, 2.4, moi=1)
            P.rot("n_dau", 12 * fl + 1.2 * r * fl)
            P.rot("n_than", 5 * fl)
            xu = cv(t, [(0, 0), (1.5, 0), (1.62, 1, "out"), (1.85, -0.5, "io"), (2.1, 0.3, "io"), (2.4, 0, "io"), (2.8, 0)])
            for tt_ in ("la_day", "la_giua"):
                for i, c in enumerate(info2["vat"][tt_]):
                    for j, b in enumerate(c):
                        P.rot("n_" + b, (9 + 7 * j) * xu * (1.0 - 0.1 * i) + 1.2 * r * fl)
            for b in info2["cum"]:
                P.rot("n_" + b, 5 * xu)
            for b in info2["lon"]:
                P.rot("n_" + b, 10 * xu + 1.5 * r * fl)
            P.rot("n_chom", -8 * xu)

        ev = tienhoa.clip_tien_hoa(M, sk, sk2, idle2[0], tiB=ti, fnA=gong, fnB=gam, mem=[])
        cl = cl + [ev]
        fr["evolve"] = hoat.nuong(M, ev)
        _, _, s_ev = tienhoa.lech_cuoi(M, fr["evolve"], sk2, idle2[0], ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
        print("  evolve:", noi["evolve"])
    tk = xuat.xuat_het(M, cl, RIG, f"{CODE}_{k}", f"Ma mút rừng (dạng {k})", frames=fr, dang=k, so_dang=2, dung_yen=("cast", "skill"),
                       lao=(), far=(), mieng="mieng", tran_mb=0.5, noi_them=noi, cao=cao,
                       can=[("can_dau_cast", "cast", 0.9, "dau", 170), ("can_dau_skill", "skill", 1.0, "dau", 190),
                            ("can_dau_idle", "idle", 2.8, "dau", 170), ("can_dau_appear", "appear", 0.9, "dau", 190)])
    return sk, info, cl, fr, tk


def soi_nhanh(clip, giay, tam=None):
    sk, info = dung()
    cl = {c.ten: c for c in clips(sk, info)}[clip]
    fr = hoat.nuong(sk, cl)
    ve = soi.Ve(sk)
    os.makedirs(os.path.join(INBOX, "soi"), exist_ok=True)
    ims = []
    for g in giay:
        P = fr[min(len(fr) - 1, int(round(g * 30)))]
        if tam:
            box = (tam[0] - tam[2], tam[1] - tam[2], tam[0] + tam[2], tam[1] + tam[2])
            sc = 520 / (2 * tam[2])
        else:
            box = (-430, -30, 470, 560)
            sc = 0.8
        ims.append(ve.ve(P, box, sc, bg=(150, 150, 150), ss=2).convert("RGB"))
    W = sum(i.width for i in ims)
    out = Image.new("RGB", (W, ims[0].height), (150, 150, 150))
    x = 0
    for i in ims:
        out.paste(i, (x, 0))
        x += i.width
    p = os.path.join(INBOX, "soi", f"{clip}_{'_'.join(str(g) for g in giay)}{'_can' if tam else ''}.png")
    out.save(p)
    print(p)


if __name__ == "__main__":
    lenh = sys.argv[1] if len(sys.argv) > 1 else ""
    if lenh:
        chon(K)
    if lenh == "cat":
        cat()
    elif lenh == "ghep":
        so_ghep()
    elif lenh == "luoi":
        ke_luoi(*(sys.argv[2:4]))
    elif lenh == "rig":
        rig()
    elif lenh == "soi":
        soi_nhanh(sys.argv[2], [float(x) for x in sys.argv[3].split(",")],
                  [float(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else None)
    else:
        print(__doc__)
