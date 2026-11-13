# -*- coding: utf-8 -*-
"""Thanh Long DẠNG 1 (rồng con) và DẠNG 2 (rồng thiếu niên), suất 10 đảo Mộc (id thanh_long); dạng 3 = rồng trúc moc_vuong_1.
Người dùng 2026-11-13 duyệt concept inbox/thanh_long_non/tai_ve/L1_d1.png, L1_d2.png ("dạng 1 và 2 ổn đấy").
Dựng THẲNG trên .atomik dạng 3 (Resources/moc_vuong_1/moc_vuong_1.atomik; máy C không có dữ liệu quét monster_3709):
- tỉ lệ xương: inbox/thanh_long_non/mau/ti_le_d<k>.json (như bố cục gửi GPT);
- sọ + hàm trên (`tou_01`, ô cứng trên all8), hàm dưới (`tou_02`, ô cứng trên all13: hàm há tới 57° ở cast / skill), hai sừng
  (`longjiao_01` trên jiao, `longjiao_02` trên jiao2), mắt nhắm (`biyan`, vẽ bằng mã trên mắt mới): cắt từ concept;
- bỏ mảnh lòng hàm cũ `tou_04` (hàm mới to hơn), dạng 1 bỏ lá trán `tou_05` (concept không có); lưỡi `tou_03` giữ;
- mọi mảnh khác: tô màu lại theo nhóm (giữ vân chì sáp; lông than dưới ngưỡng mực giữ nguyên);
- clip `evolve`: dạng 1 gộp dạng 2 (chưa có evolve) bản nhẹ, dạng 2 gộp dạng 3 bản nhẹ.
Ra inbox/thanh_long_non/rig_d<k>/. Xương, lưới, chuyển động gốc là của nhà phát hành game tham khảo; hình là của mình. Dùng nội bộ.

    py -3 -I ArtGen/Spine/thanh_long_non.py
"""
import json
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
import atomik_dang as A  # noqa: E402
from cat_concept import cat  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RES = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources")
BASE = os.path.join(HERE, "inbox", "thanh_long_non")
SRC = os.path.join(RES, "moc_vuong_1", "moc_vuong_1.atomik")
SIZE = {1: 0.95, 2: 1.1, 3: 1.16}
DPX = 1.6                                         # px atlas / đơn vị rig cho mảnh cắt từ concept

GREEN_H = [("#2E895B", "#3D914A"), ("#399564", "#59B459"), ("#79C885", "#90D574"), ("#2E794E", "#367A3F"), ("#6EBE7A", "#8CC753"),
           ("#2E6645", "#2F6A3A"), ("#55A46B", "#79BC52"), ("#2A8858", "#3D914A"), ("#339463", "#59B459"), ("#439767", "#5FB25A"),
           ("#2D784D", "#367A3F"), ("#368C62", "#4FA650"), ("#4BA46E", "#79BC52"), ("#6ABE81", "#8CC753")]
GREEN_H2 = [("#2E895B", "#39834C"), ("#399564", "#489A51"), ("#79C885", "#91CD68"), ("#2E794E", "#2F7241"), ("#6EBE7A", "#61B464"),
            ("#2E6645", "#2A6238"), ("#55A46B", "#53A75A"), ("#2A8858", "#39834C"), ("#339463", "#489A51"), ("#439767", "#53A75A"),
            ("#2D784D", "#2F7241"), ("#368C62", "#489A51"), ("#4BA46E", "#61B464"), ("#6ABE81", "#91CD68")]

CFG = {
    1: dict(
        khung=(-260, -30, 370, 390),
        dau_poly=[(700, 330), (720, 290), (760, 275), (800, 285), (845, 270), (880, 265), (905, 262), (930, 290), (965, 300), (985, 330),
                  (995, 380), (1035, 395), (1045, 440), (1032, 482), (990, 503), (930, 503), (880, 497), (850, 482), (800, 472), (760, 462),
                  (735, 440), (710, 400)],
        ham_poly=[(858, 428), (900, 442), (940, 454), (985, 466), (1015, 462), (1040, 448), (1048, 497), (990, 510), (930, 507), (870, 497),
                  (840, 470)],
        sung=[("longjiao_01", "jiao", [(700, 120), (765, 140), (805, 175), (822, 235), (814, 292), (780, 302), (750, 294), (728, 250), (705, 180)]),
              ("longjiao_02", "jiao2", [(905, 240), (928, 180), (960, 165), (985, 230), (994, 302), (962, 314), (930, 302)])],
        mat=((900, 392), 46, 38),
        ha_poly=[(700, 330), (720, 290), (760, 275), (800, 285), (845, 270), (880, 265), (905, 262), (930, 290), (965, 300), (985, 330),
                 (995, 380), (1035, 395), (1045, 440), (1035, 472), (995, 522), (962, 552), (900, 556), (850, 532), (800, 478), (760, 462),
                 (735, 440), (710, 400)],
        an=["tou_02", "tou_03", "tou_04", "tou_05"],
        mau={("chibang_q",): [("#ECC655", "#D6D962"), ("#C5942A", "#A9B040"), ("#D0AC45", "#BFC452"), ("#B28E34", "#9EA43C"),
                              ("#92732B", "#7F8A32"), ("#6E5B2A", "#5E6A2A"), ("#76C482", "#90D574"), ("#58945F", "#5FA55A")],
             ("chibang_h", "weiba"): GREEN_H,
             ("xiongjia", "hujian"): [("#ECC652", "#7CC45A"), ("#CEAD45", "#69B452"), ("#B2913C", "#4F9A48"), ("#8F732E", "#3F8040"),
                                      ("#685E31", "#2F6A3A"), ("#ECE8CE", "#F4E7BD"), ("#44BD8C", "#48BD84")],
             ("qianzhi", "houzhi"): [("#EDC756", "#F1E4B8"), ("#C6952B", "#D8CCA0"), ("#B18B30", "#C6BA90"), ("#E2BB48", "#EADDB0"),
                                     ("#9F7827", "#B5A882"), ("#8B6621", "#A49674"), ("#6D5928", "#857A60"), ("#CCA63D", "#DCD0A6")],
             ("shenti",): [("#C8962C", "#EEDFB2"), ("#BF8A21", "#E6D6A6"), ("#AF892E", "#D9CA9C"), ("#8D6420", "#BBAA82"),
                           ("#D0A536", "#F2E4B8"), ("#A47924", "#CDBD92"), ("#C9A84A", "#EEDFB2"), ("#6C5722", "#8E8166")]},
        ten="Thanh Long dạng 1 (rồng con, suất 10 đảo Mộc)"),
    2: dict(
        khung=(-300, -30, 360, 410),
        dau_poly=[(770, 352), (800, 342), (860, 347), (900, 332), (940, 347), (965, 372), (990, 400), (1006, 440), (998, 472), (962, 488),
                  (920, 484), (880, 474), (840, 458), (800, 422), (775, 382)],
        ham_poly=[(898, 452), (940, 456), (975, 461), (999, 452), (1008, 482), (962, 494), (910, 488), (888, 466)],
        sung=[("longjiao_01", "jiao", [(700, 108), (762, 148), (822, 228), (858, 290), (872, 332), (842, 348), (800, 322), (770, 282), (730, 200)]),
              ("longjiao_02", "jiao2", [(918, 250), (948, 158), (976, 198), (987, 260), (977, 332), (950, 348), (924, 322)])],
        mat=((918, 408), 36, 27),
        ha_poly=[(770, 352), (800, 342), (860, 347), (900, 332), (940, 347), (965, 372), (990, 400), (1006, 440), (1000, 472), (976, 522),
                 (950, 550), (905, 554), (872, 534), (850, 505), (836, 474), (815, 440), (790, 410), (775, 382)],
        an=["tou_02", "tou_03", "tou_04"],
        mau={("chibang_h", "weiba"): GREEN_H2,
             ("xiongjia", "hujian"): [("#ECC652", "#EFE4BE"), ("#CEAD45", "#DBA63B"), ("#B2913C", "#B88A30"), ("#8F732E", "#8F6A28"),
                                      ("#685E31", "#6A5228"), ("#44BD8C", "#48BD84")],
             ("tou_05",): GREEN_H2},
        ten="Thanh Long dạng 2 (rồng thiếu niên, suất 10 đảo Mộc)"),
}


HAM_HA = 0.45                                     # biên độ xoay hàm dưới so với dạng 3 (57° → ~26°)
CHAN = [("all30", "target4"), ("all19", "target2"), ("all44", "all46"), ("all41", "all43")]   # (hông, bàn) bốn chân
MIENG_MAU = (94, 40, 38)                          # lòng miệng (đỏ sẫm)
LONG_MIENG = 0.5                                  # chiều cao lòng miệng ở mũi / dài hàm
CHOM, MUC = 10, 7                                 # hàm chờm lên sau sọ; bề dày nét mực miệng sọ giữ lại


def tach_ham(rgb, m_dau, ham_poly, rang):
    """tách đầu thành sọ (giữ nét mực miệng) và hàm dưới (từ mép trên nét mực miệng, chờm lên CHOM px sau sọ). Đường miệng: mỗi cột trong
    đa giác hàm, dải mực gần mép trên đa giác nhất (±10 px), trung vị trượt 7 cột cho khỏi nhảy."""
    H, W = m_dau.shape
    hp = np.zeros((H, W), np.uint8)
    cv2.fillPoly(hp, [np.array(ham_poly, np.int32)], 1)
    hp = hp.astype(bool)
    ink = rgb.min(2) < 90
    cols = np.flatnonzero(hp.any(0))
    top, bot, low = {}, {}, {}
    for x in cols:
        ys = np.flatnonzero(hp[:, x])
        y0 = int(ys.min())
        low[x] = int(ys.max())
        runs, y = [], max(0, y0 - 10)
        while y <= min(H - 1, y0 + 10):
            if ink[y, x]:
                s = y
                while y + 1 < H and ink[y + 1, x]:
                    y += 1
                runs.append((s, y))
            y += 1
        if runs:
            s, e = min(runs, key=lambda r: abs((r[0] + r[1]) / 2 - y0))
        else:
            s, e = y0, y0
        top[x], bot[x] = s, e
    xs = list(cols)
    med = lambda d, i: int(np.median([d[xs[j]] for j in range(max(0, i - 3), min(len(xs), i + 4))]))  # noqa: E731
    m_ham = np.zeros((H, W), bool)
    m_cat = np.zeros((H, W), bool)
    for i, x in enumerate(xs):
        tp, bt = med(top, i), med(bot, i)
        m_ham[max(0, tp - CHOM):low[x] + 1, x] = True
        m_cat[bt + 1:low[x] + 1, x] = True
    m_ham &= m_dau & ~rang
    m_tren = m_dau & ~(m_cat & ~rang)
    # lòng miệng: dải phía TRÊN đường miệng, nấp sau sọ lúc ngậm; cao dần từ khoé (0) tới mũi (LONG_MIENG × dài hàm), cắt trong hình sọ
    x0, x1 = xs[0], xs[-1]
    m_long = np.zeros((H, W), bool)
    for i, x in enumerate(xs):
        tp = med(top, i)
        h = int(round(LONG_MIENG * (x1 - x0) * (x - x0) / max(1, x1 - x0)))
        m_long[max(0, tp - CHOM - h):max(0, tp - CHOM + 1), x] = True
    m_long &= m_tren
    return m_tren, m_ham, m_long


def mat_nham(rgb, tam, rx, ry):
    """mảnh mắt nhắm vẽ bằng mã trên concept: lấp mắt bằng màu lông quanh nó, kẻ mí cong (nét mực)."""
    H, W = rgb.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    e = ((xx - tam[0]) / rx) ** 2 + ((yy - tam[1]) / ry) ** 2
    vanh = (e > 1.25) & (e < 2.2)
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    fur = vanh & (lab[..., 0] > 27 * 2.55) & (lab[..., 0] < 55 * 2.55)
    col = np.median(rgb[fur], axis=0) if fur.any() else np.array([70, 76, 72])
    pad = 8
    x0, y0, x1, y1 = int(tam[0] - rx - pad), int(tam[1] - ry - pad), int(tam[0] + rx + pad), int(tam[1] + ry + pad)
    w, h = x1 - x0, y1 - y0
    im = Image.new("RGBA", (w * 4, h * 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = (tam[0] - x0) * 4, (tam[1] - y0) * 4
    d.ellipse([cx - rx * 4 * 1.08, cy - ry * 4 * 1.08, cx + rx * 4 * 1.08, cy + ry * 4 * 1.08], fill=(255, 255, 255, 255))
    # vân lông: mảng lông thật ngay bên trái mắt (dời ngang 2,4 rx), phóng 4 lần, chỉ trong elip
    sx = int(round(rx * 2.4))
    src = rgb[y0:y1, max(0, x0 - sx):max(0, x0 - sx) + w]
    if src.shape[:2] == (h, w):
        L = cv2.cvtColor(src, cv2.COLOR_RGB2LAB)[..., 0]
        tex = src.copy()
        bad = (L < 27 * 2.55) | (L > 60 * 2.55)
        tex[bad] = col.astype(np.uint8)
        tex4 = np.asarray(Image.fromarray(tex).resize((w * 4, h * 4), Image.BICUBIC))
    else:
        tex4 = np.broadcast_to(col.astype(np.uint8), (h * 4, w * 4, 3))
    arr = np.asarray(im).copy()
    sel = arr[..., 3] > 0
    arr[..., :3][sel] = tex4[sel]
    im = Image.fromarray(arr, "RGBA")
    d = ImageDraw.Draw(im)
    pts = [(cx - rx * 4 * 0.95 + i * rx * 4 * 1.9 / 20, cy + ry * 4 * 0.15 + (1 - ((i - 10) / 10) ** 2) * ry * 4 * 0.42) for i in range(21)]
    d.line(pts, fill=(43, 33, 24, 255), width=24, joint="curve")
    im = im.resize((w, h), Image.LANCZOS)
    full = np.zeros((H, W, 4), np.uint8)
    full[y0:y1, x0:x1] = np.asarray(im)
    return full


HA_DO = 12.0                                      # hàm của rig gốc há quá chừng này độ (so với idle) thì đổi sang đầu há


def doi_dau_ha(J, fps=30):
    """mọi clip: slot sọ (tou_01 và bản sinh đôi) dùng đầu há `tou_01_ha` khi xương hàm all13 há quá HA_DO so với sọ all8; giữ nguyên
    lúc nào slot nào hiện (thứ tự vẽ đổi giữa clip)."""
    import math
    B = A.bi(J)
    S = J["slots"]
    sl = [i for i, s in enumerate(S) if s["name"].split("~")[0] == "tou_01"]
    att_ng = {s: next(i for i, a in enumerate(J["atts"]) if a["slot"] == s and a["name"] == "tou_01") for s in sl}
    att_ha = {s: next(i for i, a in enumerate(J["atts"]) if a["slot"] == s and a["name"] == "tou_01_ha") for s in sl}
    P = A.Pose(J)

    def goc():
        a8, a13 = P.w[B["all8"]], P.w[B["all13"]]
        return math.degrees(math.atan2(a13[2], a13[0]) - math.atan2(a8[2], a8[0]))

    P.at(A.clip(J, "idle"), 0)
    g0 = goc()
    tong = {}
    for ci, an in enumerate(J["anims"]):
        ts = list(np.arange(0, an["dur"] + 1e-6, 1 / fps))
        rows = {s: [] for s in sl}
        n_ha = 0
        for t in ts:
            P.at(ci, t)
            d = (goc() - g0 + 180) % 360 - 180
            mo = d < -HA_DO
            n_ha += mo
            for s in sl:
                cur = P.att[s]
                rows[s].append(-1 if cur < 0 else (att_ha[s] if mo else att_ng[s]))
        an["sk"] = [k for k in an.get("sk") or [] if k["slot"] not in sl]
        for s in sl:
            times, atts = [], []
            for t, a in zip(ts, rows[s]):
                if not atts or a != atts[-1]:
                    times.append(round(float(t), 4))
                    atts.append(int(a))
            if len(atts) > 1 or atts[0] != J["slots"][s].get("att", -1):
                an["sk"].append({"slot": s, "times": times, "atts": atts})
        if n_ha:
            tong[an["name"]] = n_ha
    print("  đầu há (số khung):", tong)


def dung_base(k):
    c = CFG[k]
    J, img, ver = A.load(SRC)
    A.scale_bones(J, json.load(open(os.path.join(BASE, "mau", f"ti_le_d{k}.json"), encoding="utf-8")))
    S = J["slots"]
    B = A.bi(J)
    # hàm há ít lại (đầu chibi to: há 57° như dạng 3 thành một khe đen lớn); lòng miệng ở mảnh hàm che khe
    # bàn chân là con của `all` (tách thân): clip bay / xuất hiện kéo bàn ra xa, lưới chân giãn. Giới hạn độ dài chân như lúc đứng
    keo = A.clamp_legs(J, CHAN, clips=("fly",))
    print(f"  dạng {k}: kéo bàn chân về (số khung × chân): {keo}")
    for pre, pairs in c["mau"].items():
        ais = [i for i, a in enumerate(J["atts"]) if S[a["slot"]]["name"].startswith(pre)]
        img = A.recolor(img, A.att_masks(J, img, ais), pairs)
    rgb = np.asarray(Image.open(os.path.join(BASE, "tai_ve", f"L1_d{k}.png")).convert("RGB"))
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    green = (hsv[..., 0] > 30) & (hsv[..., 0] < 95) & (hsv[..., 1] > 50) & (rgb.min(2) < 238)
    cream = (rgb.min(2) > 150) & (rgb.max(2) - rgb.min(2) < 90) & (rgb.min(2) < 245)
    n, lab, st, _ = cv2.connectedComponentsWithStats(cream.astype(np.uint8), connectivity=4)
    big = np.zeros(n, bool)
    big[1:] = st[1:, cv2.CC_STAT_AREA] > 700          # bờm, đốt cổ; răng nanh (nhỏ) vẫn được lấy
    loai = green | big[lab]
    dau, m_dau = cat(rgb, np.array(c["dau_poly"], float), ti=0.7, loai=loai)
    nh, lb2, st2, _ = cv2.connectedComponentsWithStats((cream & ~big[lab]).astype(np.uint8), connectivity=4)
    rang = np.zeros(m_dau.shape, bool)
    for i in range(1, nh):
        if st2[i, cv2.CC_STAT_AREA] < 700:
            rang |= lb2 == i
    rang = cv2.dilate(rang.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool)
    m_tren, m_ham, m_long = tach_ham(rgb, m_dau, c["ham_poly"], rang)

    def rgba_of(m):
        a = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.9)
        return np.dstack([rgb, (np.clip((a - 0.2) / 0.6, 0, 1) * 255).astype(np.uint8)])

    to_rig, to_px, z = A.canvas_map(c["khung"], rgb.shape[1], rgb.shape[0])
    P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
    ims, quads = [], []

    def o_cung(rgba, bone, names):
        im = Image.fromarray(rgba, "RGBA")
        bb = im.getbbox()
        crop = im.crop(bb)
        ims.append(crop.resize((max(2, round((bb[2] - bb[0]) * z * DPX)), max(2, round((bb[3] - bb[1]) * z * DPX))), Image.LANCZOS))
        corners = to_rig([(bb[0], bb[1]), (bb[2], bb[1]), (bb[2], bb[3]), (bb[0], bb[3])])
        quads.append((names, B[bone] if isinstance(bone, str) else bone, A.bone_local(P, B[bone] if isinstance(bone, str) else bone, corners)))

    o_cung(rgba_of(m_dau), "all8", ["tou_01"])
    # đầu HÁ MIỆNG (GPT vẽ lại đúng đầu đang gầm: L2_ha_d<k>.png), khớp vào đầu ngậm bằng tương quan pha quanh mắt
    rgb_h = np.asarray(Image.open(os.path.join(BASE, "tai_ve", f"L2_ha_d{k}.png")).convert("RGB"))
    (ex, ey), rx, ry = c["mat"]
    win = (int(ex - 3 * rx), int(ey - 3 * ry), int(ex + 3 * rx), int(ey + 2 * ry))
    g0 = cv2.cvtColor(rgb[win[1]:win[3], win[0]:win[2]], cv2.COLOR_RGB2GRAY).astype(np.float32)
    g1 = cv2.cvtColor(rgb_h[win[1]:win[3], win[0]:win[2]], cv2.COLOR_RGB2GRAY).astype(np.float32)
    (sx_, sy_), _ = cv2.phaseCorrelate(g0, g1)
    print(f"  dạng {k}: đầu há lệch đầu ngậm ({sx_:+.1f}, {sy_:+.1f}) px, đã bù")
    hsv_h = cv2.cvtColor(rgb_h, cv2.COLOR_RGB2HSV)
    green_h = (hsv_h[..., 0] > 30) & (hsv_h[..., 0] < 95) & (hsv_h[..., 1] > 50) & (rgb_h.min(2) < 238)
    cream_h = (rgb_h.min(2) > 150) & (rgb_h.max(2) - rgb_h.min(2) < 90) & (rgb_h.min(2) < 245)
    nh_, lab_h, st_h, _ = cv2.connectedComponentsWithStats(cream_h.astype(np.uint8), connectivity=4)
    big_h = np.zeros(nh_, bool)
    big_h[1:] = st_h[1:, cv2.CC_STAT_AREA] > 700
    maroon = (hsv_h[..., 0] < 12) | (hsv_h[..., 0] > 168)
    maroon &= (hsv_h[..., 1] > 70) & (rgb_h[..., 0].astype(int) - rgb_h[..., 2].astype(int) > 25)      # lòng miệng, lưỡi: đỏ, không phải mực
    ha, _ = cat(rgb_h, np.array(c["ha_poly"], float), ti=0.6, loai=green_h | big_h[lab_h], mot_khoi=False, them=maroon, gioi_han=True)
    M = np.float32([[1, 0, -sx_], [0, 1, -sy_]])
    ha = cv2.warpAffine(ha, M, (ha.shape[1], ha.shape[0]), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
    sl01 = [i for i, s in enumerate(S) if s["name"].split("~")[0] == "tou_01"]
    base01 = next(a for a in J["atts"] if a["name"] == "tou_01")
    for s in sl01:
        J["atts"].append({"slot": s, "name": "tou_01_ha", "uvs": list(base01["uvs"]), "tris": list(base01["tris"]),
                          "wInfo": list(base01["wInfo"])})
    o_cung(ha, "all8", ["tou_01_ha"])
    for att, bone, poly in c["sung"]:
        s_rgba, _ = cat(rgb, np.array(poly, float), ti=0.6, loai=big[lab] | green)
        o_cung(s_rgba, bone, [att])
    o_cung(mat_nham(rgb, *c["mat"]), "all8", ["biyan"])
    trong = Image.new("RGBA", (4, 4), (0, 0, 0, 0))
    for nm in c["an"]:
        ims.append(trong)
        quads.append(([nm], B["all8"], np.array([[0, 0], [0.01, 0], [0.01, -0.01], [0, -0.01]])))
    img, boxes = A.add_regions(J, img, ims)
    H2, W2 = img.shape[:2]
    for (names, bone, loc), box in zip(quads, boxes):
        for ai, a in enumerate(J["atts"]):
            if a["name"] in names:
                A.set_quad(J, H2, W2, ai, box, bone, loc)
    doi_dau_ha(J)
    # khối game
    g = dict(J["game"])
    P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
    g["height"] = round(float(A.bounds(P)[3]), 2)
    if "mieng" in B and "cast" in g.get("hitClips", []):
        P.at(A.clip(J, "cast"), g["hitTimes"][g["hitClips"].index("cast")])
        g["muzzle"] = [round(float(v), 2) for v in P.bone_pt(B["mieng"])]
    J["game"] = g
    J["rigName"] = f"thanh_long_d{k}"
    return J, img, ver


def xuat(k, J, img, ver):
    ra = os.path.join(BASE, f"rig_d{k}")
    os.makedirs(ra, exist_ok=True)
    p = os.path.join(ra, f"thanh_long_d{k}.atomik")
    n, nj, npng = A.save(p, J, img, ver)
    print(f"{p}: {n // 1024} KB (JSON {nj // 1024} KB, PNG {npng // 1024} KB), {len(J['bones'])} xương, {len(J['slots'])} slot, "
          f"atlas {img.shape[1]}x{img.shape[0]}, cao {J['game']['height']}, clip {[a['name'] for a in J['anims']]}")
    P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
    b = A.bounds(P)
    side = max(b[2] - b[0], b[3] - b[1]) * 1.12
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    A.render(J, img, P, (cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2), 1024 / side, ss=1).resize((512, 512), Image.LANCZOS).save(
        os.path.join(ra, "chan_dung.png"))
    subprocess.run([sys.executable, "-I", os.path.join(HERE, "mo_xe", "atomik_xem.py"), ROOT, ra, p, CFG[k]["ten"]], capture_output=True)
    return p


def main():
    J1, i1, v = dung_base(1)
    J2, i2, _ = dung_base(2)
    J3, i3, _ = A.load(SRC)
    J2b, i2b = json.loads(json.dumps(J2)), i2.copy()       # dạng 2 chưa gộp, để gộp vào dạng 1
    B2 = A.bi(J2)
    k3 = SIZE[3] / SIZE[2] * J2["game"]["height"] / J3["game"]["height"]
    i2 = A.gop_tien_hoa(J2, i2, J3, i3, k3, than_A=B2["all"])
    B1 = A.bi(J1)
    k2 = SIZE[2] / SIZE[1] * J1["game"]["height"] / J2b["game"]["height"]
    i1 = A.gop_tien_hoa(J1, i1, J2b, i2b, k2, than_A=B1["all"])
    print(f"dạng 2 trong rig dạng 1 × {k2:.3f}; dạng 3 trong rig dạng 2 × {k3:.3f}")
    xuat(1, J1, i1, v)
    xuat(2, J2, i2, v)


if __name__ == "__main__":
    main()
