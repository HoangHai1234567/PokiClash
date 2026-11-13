# -*- coding: utf-8 -*-
"""Tiểu quỷ lava (quy_lava): cắt mảnh từ năm tờ "đúng chỗ, đúng cỡ" (M_A..M_E: Codex vẽ lại concept đã duyệt, mỗi tờ giữ vài bộ phận không
chạm nhau, vẽ đủ phần khuất) → inbox/quy_lava_1/manh/<mảnh>.png + dat.json + _so_ghep.png (ghép lại cạnh concept) + _to.png.

    quy_lava_manh.py lam

dat.json: {"_thu_tu": [mảnh sau → trước], mảnh: {anh, A: [[1, 0, x0], [0, 1, y0]] (px ảnh → px concept), co: [w, h]}}.
Con nhìn sang phải; "g" = gần (bên trái người xem), "x" = xa."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kiem_si_manh as KMS  # noqa: E402  (dùng lại các hàm cắt: nen, cum, manh_rgba, dan)

BASE = os.path.join(HERE, "inbox", "quy_lava_1")
TAI = os.path.join(BASE, "tai_ve")
MANH = os.path.join(BASE, "manh")
DUYET = os.path.join(TAI, "L1_duyet.png")
# tờ → {mảnh: tâm ước chừng trên khung concept (px)}
TO = {"A": {"than": (792, 590)},
      "B": {"lua": (735, 250), "giot1": (637, 45), "giot2": (518, 197), "giao": (660, 690)},
      "C": {"khien": (1093, 650), "sung_g": (746, 335), "mat_g": (797, 530), "mat_x": (945, 523), "mieng": (880, 598)},
      "D": {"sung_x": (976, 343), "tay_x": (998, 632), "chan_g": (623, 834), "chan_x": (912, 788)},
      "E": {"nam_x": (1021, 615), "dot_g": (632, 771), "mat_g_nham": (797, 538), "mat_x_nham": (945, 534)},
      "F": {"gang": (622, 670)},
      "G": {"dui_g": (661, 788)}}           # đùi chân gần nối đáy thân với cụm đá chân (giơ găng là lộ chỗ hở)           # găng liền núm vai (tờ C vẽ găng lệch, núm lơ lửng)
NHO = {"E": 60, "C": 120, "B": 200}            # cụm nhỏ nhất được giữ (px²) theo tờ: mắt nhắm là nét mảnh
# thứ tự vẽ sau → trước (theo thứ tự slot của rig gốc)
THU_TU = ["tay_x", "nam_x", "khien", "lua", "giot1", "giot2", "dui_g", "chan_x", "than", "chan_g", "mat_g", "mat_x", "mat_g_nham", "mat_x_nham", "mieng",
          "sung_g", "sung_x", "giao", "giao_mui", "gang", "dot_g"]   # nắm tay xa SAU khiên (người dùng: không thấy ngón tay cầm khiên)
AN = {"mat_g_nham", "mat_x_nham"}              # ẩn ở dáng nghỉ
# giáo cắt hai mảnh ở khâu nối (px concept)
GIAO_DUOI, GIAO_MUI, KHAU = (355.0, 470.0), (1000.0, 913.0), (685.0, 685.0)

GOP = {}                                        # mảnh → khung (x0, y0, x1, y1): gộp mọi cụm có tâm trong khung
DANG = int(os.environ.get("QL_DANG", "1"))
if DANG == 2:                                   # dạng 2 (hiệp sĩ dung nham, concept quy_lava_2/L1_duyet.png = L1_hiep_si.png)
    BASE = os.path.join(HERE, "inbox", "quy_lava_2")
    TAI = os.path.join(BASE, "tai_ve")
    MANH = os.path.join(BASE, "manh")
    DUYET = os.path.join(TAI, "L1_duyet.png")
    TO = {"A": {"than": (818, 600)},
          "B": {"lua": (680, 240), "giot1": (350, 123), "giot2": (300, 238), "giao": (612, 672)},
          "C": {"khien": (1125, 656), "sung_g": (697, 280), "mat_g": (816, 480), "mat_x": (960, 480), "mieng": (880, 551), "dui_g": (630, 852)},
          "D": {"sung_x": (1053, 295), "nam_x": (1037, 605), "chan_g": (541, 902), "chan_x": (950, 871)},
          "E": {"gang": (558, 690), "mat_g_nham": (816, 488), "mat_x_nham": (960, 488)},
          "F": {"vai_g": (577, 517), "dot_g": (541, 796), "tay_x": (1005, 620)},
          "cam": {"cam": (880, 600)}}   # khối hai tay + giáo dựng của chiêu cuối (đổi ảnh; tờ M_cam tách từ L2_cam_giao.png)
    NHO = {"E": 60, "C": 120, "B": 200}
    # vai_g (giáp vai gai) bám bắp tay, vẽ TRƯỚC găng tay
    THU_TU = ["tay_x", "nam_x", "khien", "lua", "giot1", "giot2", "dui_g", "chan_x", "than", "chan_g", "mat_g", "mat_x", "mat_g_nham",
              "mat_x_nham", "mieng", "sung_g", "sung_x", "giao", "giao_mui", "gang", "dot_g", "vai_g", "cam"]
    AN = AN | {"cam"}
    GIAO_DUOI, GIAO_MUI, KHAU = (225.0, 420.0), (998.0, 935.0), (657.0, 730.0)
    GOP = {"mieng": (790.0, 512.0, 968.0, 590.0)}


def moi_nhat(ma):
    ds = [f for f in os.listdir(TAI) if f == f"M_{ma}.png" or (f.startswith(f"M_{ma}_") and f.endswith(".png"))]
    if not ds:
        raise SystemExit(f"chưa có tờ M_{ma}")
    ds.sort(key=lambda f: (int(f[len(f"M_{ma}_"):-4]) if f != f"M_{ma}.png" else 1))
    return os.path.join(TAI, ds[-1])


def cat_to(ma):
    A = KMS.doc(moi_nhat(ma))
    ds = KMS.cum(A, NHO.get(ma, 300), lo_min=10 ** 9 if ma in ("A", "C") else 2500)   # thân, răng nanh: không đục lỗ trắng kín
    ra, da = {}, set()
    for ten, (cx, cy) in TO[ma].items():
        best, bi = 1e18, -1
        for i, (m, st, cen) in enumerate(ds):
            if i in da:
                continue
            x, y, w, h, _ = st
            dx, dy = max(x - cx, 0, cx - (x + w)), max(y - cy, 0, cy - (y + h))
            d = dx * dx + dy * dy + 0.02 * ((cen[0] - cx) ** 2 + (cen[1] - cy) ** 2)
            if d < best:
                best, bi = d, i
        if bi < 0:
            raise SystemExit(f"tờ {ma}: không thấy mảnh {ten}")
        da.add(bi)
        m_ = ds[bi][0]
        if ten in GOP:                                     # gộp mọi cụm có tâm trong khung (răng nanh rời của miệng dạng 2)
            gx0, gy0, gx1, gy1 = GOP[ten]
            for i, (m2, st2, c2) in enumerate(ds):
                if i not in da and gx0 <= c2[0] <= gx1 and gy0 <= c2[1] <= gy1:
                    m_ = m_ | m2
                    da.add(i)
        ra[ten] = (A, m_)
        x, y, w, h, a = ds[bi][1]
        print(f"    {ten:11s} x {x}-{x + w}  y {y}-{y + h}  ({a} px²)")
    thua = [tuple(int(v) for v in st[:5]) for i, (m, st, c) in enumerate(ds) if i not in da and st[4] >= 150]
    print(f"  tờ {ma}: {len(ra)} mảnh" + (f"; cụm THỪA không dùng: {thua}" if thua else ""))
    return ra


# giáo cắt hai mảnh ở khâu nối (px concept): phiến đá đuôi (giao) và mũi tinh thể (giao_mui). Chiêu cuối vẽ phiến đá SAU thân (không che
# mặt, sừng) mà mũi tinh thể vẫn TRƯỚC thân; khâu nối luôn nằm dưới găng tay nên chỗ cắt không lộ.
KHAU_NUA = 34.0                                # nửa bề dài khâu dọc trục giáo (px concept)


def noi_mieng(anh_):
    """dạng 2: tờ C chỉ có bốn răng nanh rời → kẻ nét miệng zíc zắc mực nối gốc các răng (chân răng là mép trên mỗi cụm), thò ra hai đầu."""
    im = anh_["mieng"]
    A = np.asarray(im).copy()
    al = A[..., 3] > 120
    n, lab, st, cen = cv2.connectedComponentsWithStats(al.astype(np.uint8), 8)
    rang = sorted([(st[i, 0], st[i, 1], st[i, 2], st[i, 3]) for i in range(1, n) if st[i, 4] > 40], key=lambda r: r[0])
    if len(rang) < 2:
        return
    pts = []
    for x, y, w, h in rang:
        pts += [(x + 2, y + 2), (x + w // 2, y + 6), (x + w - 2, y + 2)]
    pts = [(max(0, pts[0][0] - 14), pts[0][1] - 4)] + pts + [(min(A.shape[1] - 1, pts[-1][0] + 14), pts[-1][1] - 4)]
    cv2.polylines(A, [np.array(pts, np.int32)], False, (43, 33, 24, 255), 6, cv2.LINE_AA)
    g = Image.fromarray(A, "RGBA")
    g.save(os.path.join(MANH, "mieng.png"))
    anh_["mieng"] = g


def tach_giao(anh_, dat):
    im = anh_["giao"]
    x0, y0 = dat["giao"]["A"][0][2], dat["giao"]["A"][1][2]
    A = np.asarray(im).copy()
    h, w = A.shape[:2]
    u = np.array(GIAO_MUI) - np.array(GIAO_DUOI)
    u = u / np.hypot(*u)
    yy, xx = np.mgrid[0:h, 0:w]
    t = (xx + x0 - KHAU[0]) * u[0] + (yy + y0 - KHAU[1]) * u[1]          # vị trí dọc trục so với tâm khâu
    duoi = A.copy()
    duoi[..., 3] = np.where(t <= KHAU_NUA, A[..., 3], 0)                  # phiến đá + cả khâu
    mui = A.copy()
    mui[..., 3] = np.where(t >= 0.0, A[..., 3], 0)                        # mũi tinh thể + nửa trước khâu (chồng lên nhau dưới găng)
    for ten, arr in (("giao", duoi), ("giao_mui", mui)):
        g = Image.fromarray(arr, "RGBA")
        g.save(os.path.join(MANH, ten + ".png"))
        anh_[ten] = g
        dat[ten] = dict(anh=ten, A=[[1.0, 0.0, x0], [0.0, 1.0, y0]], co=[w, h])


def lam():
    os.makedirs(MANH, exist_ok=True)
    C = KMS.doc(DUYET)
    anh_, dat = {}, {}
    for ma in TO:
        for ten, (A, m) in cat_to(ma).items():
            im, goc = KMS.manh_rgba(A, m)
            im.save(os.path.join(MANH, ten + ".png"))
            anh_[ten] = im
            dat[ten] = dict(anh=ten, A=[[1.0, 0.0, float(goc[0])], [0.0, 1.0, float(goc[1])]], co=[im.width, im.height])
    tach_giao(anh_, dat)
    if DANG == 2:
        noi_mieng(anh_)
    dat["_thu_tu"] = THU_TU
    json.dump(dat, open(os.path.join(MANH, "dat.json"), "w", encoding="utf-8"), indent=1)
    Wc, Hc = C.shape[1], C.shape[0]
    ghep = Image.new("RGBA", (Wc, Hc), (255, 255, 255, 255))
    for t in THU_TU:
        if t not in AN:
            KMS.dan(ghep, anh_[t], dat[t]["A"])
    so = Image.new("RGB", (Wc * 2 + 10, Hc), (255, 255, 255))
    so.paste(Image.fromarray(C.astype(np.uint8)), (0, 0))
    so.paste(ghep.convert("RGB"), (Wc + 10, 0))
    so.save(os.path.join(MANH, "_so_ghep.png"))
    # chỗ concept có hình mà bản ghép trống (lỗ), đo trên vùng hình của concept
    cm = C.min(2) < 230
    gm = np.asarray(ghep.convert("RGB")).min(2) < 230
    lo = cm & ~gm
    lo = cv2.morphologyEx(lo.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)).astype(bool)
    print(f"điểm concept có hình mà bản ghép trống: {int(lo.sum())} px")
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
    x = y = 12
    hh = 0
    cho = []
    for t, im in anh_.items():
        if x + im.width + 12 > 2400:
            x, y, hh = 12, y + hh + 34, 0
        cho.append((t, x, y))
        x += max(im.width, 90) + 16
        hh = max(hh, im.height)
    to = Image.new("RGB", (2400, y + hh + 40), (150, 150, 150))
    dr = ImageDraw.Draw(to)
    for t, x, y in cho:
        to.paste(anh_[t], (x, y + 20), anh_[t])
        dr.text((x, y), t, fill=(255, 255, 255), font=f)
    to.save(os.path.join(MANH, "_to.png"))
    print(os.path.join(MANH, "_so_ghep.png"))
    print(os.path.join(MANH, "_to.png"), len(anh_), "mảnh")


if __name__ == "__main__":
    if sys.argv[1:2] == ["lam"]:
        lam()
    else:
        print(__doc__)
