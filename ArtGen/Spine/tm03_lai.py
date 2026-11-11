# -*- coding: utf-8 -*-
"""tm03, cách lai (DAC_TA mục 5): thân chính CẮT THẲNG TỪ CONCEPT đã duyệt (loang vùng từ hạt giống, nét mực là tường, nhãn gần
nhất); mảnh GPT (tờ M0x) chỉ cho phần phải tách / bị che và làm nguồn vẽ bù. Cần cv2:

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm03_lai.py nhan 1      bản đồ vùng trên concept (soi hạt giống)
    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm03_lai.py lai 1       dò mảnh GPT trên concept + cắt lớp + vẽ bù

Ra inbox/tm03_<k>/lai/: nhan.png (concept | bản đồ vùng), <lớp>.png (RGBA cỡ concept, cắt sát), lop.json (gốc crop, đất, mảnh
GPT đặt ở đâu), so_ghep.png (mảnh GPT đặt lên concept, IoU).
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

import cv2  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm03"
INK = 62          # độ sáng TB dưới ngưỡng này là nét mực (mực #2B2118 ~ 34; lam đậm #24407F ~ 76 không tính là tường)

# ---------------------------------------------------------------- cấu hình từng dạng (toạ độ px concept 1536 x 1024)
CFG = {
    1: {
        "concept": "L1_duyet.png",
        "seeds": {
            "duoi": [(450, 500), (420, 600), (540, 330), (650, 400), (600, 330), (540, 470), (500, 560), (530, 655), (600, 670),
                     (470, 680), (410, 450), (680, 470), (640, 540)],
            "than": [(850, 650), (720, 560), (800, 470), (950, 600), (1000, 700), (880, 760), (700, 650), (860, 380), (870, 450),
                     (1040, 420), (1040, 470), (1070, 520), (760, 700), (1060, 600), (680, 560), (660, 620), (650, 680), (700, 500),
                     (690, 470), (740, 530), (720, 610), (668, 520), (775, 760), (790, 778), (960, 750), (1050, 752), (948, 772)],
            "mieng": [(980, 560), (950, 612), (1020, 605), (1040, 570), (935, 590), (960, 626), (990, 626), (930, 575), (1010, 560)],
            "chan_sn": [(650, 740), (630, 790), (640, 845), (690, 850)],
            "chan_sx": [(500, 770), (480, 820), (470, 850), (520, 850)],
            "chan_tn": [(830, 760), (840, 810), (850, 850)],
            "chan_tx": [(1000, 760), (1010, 810), (1010, 850)],
            "mat_n": [(850, 350), (830, 430), (920, 450), (880, 485), (800, 400)],
            "mat_x": [(1030, 395), (1050, 452), (1085, 452), (1060, 480)],
        },
        # chân trước mọc ra từ bụng không có nét mực ngăn: phần nhãn chân cao hơn y này trả về thân
        "clamp_y": {"chan_tn": 740, "chan_tx": 738},
    },
    2: {
        "concept": "L1_concept_3.png",
        "seeds": {
            "than": [(500, 420), (600, 450), (750, 450), (850, 470), (800, 520), (560, 520), (480, 340), (420, 330), (950, 280),
                     (1050, 300), (1150, 350), (900, 330), (870, 380), (900, 455), (1000, 462), (1100, 452), (760, 500),
                     (600, 560), (700, 560), (840, 470), (930, 515), (1180, 380), (1060, 350), (980, 360), (380, 390),
                     (560, 380), (730, 420), (650, 520), (1150, 450), (1200, 430)],
            "mieng": [(960, 402), (1050, 396), (1100, 400), (1050, 422), (1000, 420), (1130, 410), (930, 410), (1160, 405)],
            "tui": [(900, 590), (950, 610), (870, 560), (960, 560), (900, 630)],
            "la": [(700, 300), (600, 320), (800, 300), (560, 360), (650, 360), (760, 350), (850, 330), (700, 250), (820, 360),
                   (860, 380), (780, 380), (870, 350), (840, 300)],
            "sung_n": [(905, 248), (875, 232), (930, 262)],
            "sung_x": [(1090, 245), (1112, 260), (1080, 232)],
            "mat_n": [(985, 320), (960, 330), (1005, 342), (950, 315)],
            "mat_x": [(1180, 322), (1172, 335)],
            "chan_sn": [(420, 450), (360, 500), (480, 520), (400, 560), (390, 640), (400, 690), (330, 750), (410, 760), (490, 740),
                        (360, 722), (450, 722), (340, 450), (450, 400), (500, 450), (520, 500), (470, 580), (430, 590),
                        (500, 560), (480, 400), (440, 380), (530, 470), (510, 420)],
            "chan_sx": [(290, 615), (265, 652), (330, 642), (310, 600)],
            "chan_tn": [(640, 520), (650, 570), (660, 640), (680, 680), (640, 752), (730, 772), (800, 742), (650, 615), (700, 720),
                        (640, 540), (670, 580), (680, 520), (668, 505), (672, 530), (660, 515), (625, 548), (622, 565)],
            "chan_tx": [(1080, 520), (1100, 600), (1120, 660), (1180, 722), (1250, 712), (1110, 600), (1070, 735), (1150, 690)],
        },
        "clamp_y": {"chan_tn": 492, "chan_tx": 476},
    },
}


# ---------------------------------------------------------------- tiện ích ảnh
def fg_mask(rgb, light=222, sat=32):
    """nền = vùng sáng ít màu nối mép ảnh; trắng khép kín bên trong hình (chấm mắt) giữ."""
    mn = rgb.min(2).astype(np.int16)
    mx = rgb.max(2).astype(np.int16)
    lite = ((mn > light) & (mx - mn < sat)).astype(np.uint8)
    n, lab = cv2.connectedComponents(lite, connectivity=4)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    bg = np.isin(lab, border[border > 0]) & (lite > 0)
    fg = (~bg).astype(np.uint8)
    return cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0


def lab_f(rgb):
    return cv2.cvtColor(np.ascontiguousarray(rgb), cv2.COLOR_RGB2LAB).astype(np.float32)


def warp(rgba, sx, sy, r, lat=False):
    """phóng (sx, sy), lật ngang, xoay r độ (ngược kim như mắt nhìn) quanh tâm; trả ảnh vừa khít."""
    im = rgba[:, ::-1] if lat else rgba
    h, w = im.shape[:2]
    nw, nh = max(2, int(round(w * sx))), max(2, int(round(h * sy)))
    im = cv2.resize(im, (nw, nh), interpolation=cv2.INTER_AREA if sx < 1 else cv2.INTER_LINEAR)
    h, w = im.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), r, 1.0)
    c, si = abs(M[0, 0]), abs(M[0, 1])
    W2, H2 = int(h * si + w * c) + 2, int(h * c + w * si) + 2
    M[0, 2] += W2 / 2 - w / 2
    M[1, 2] += H2 / 2 - h / 2
    return cv2.warpAffine(im, M, (W2, H2), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))


def match(ref_lab, part, sxs, sys_, rots, f, around, win, lat=False, allow=None):
    """dò (sai, sx, sy, r, cx, cy) cực tiểu SQDIFF có mặt nạ / diện tích, ở độ phân giải f, tâm trong ô ±win quanh around."""
    best = None
    R = cv2.resize(ref_lab, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
    for sx in sxs:
        for sy0 in sys_:
            sy = sx if sy0 is None else sy0
            for r in rots:
                wp = warp(part, sx * f, sy * f, r, lat)
                if wp.shape[0] >= R.shape[0] or wp.shape[1] >= R.shape[1] or min(wp.shape[:2]) < 6:
                    continue
                m = (wp[:, :, 3] > 200).astype(np.float32)
                area = m.sum()
                if area < 20:
                    continue
                t = lab_f(wp[:, :, :3])
                res = cv2.matchTemplate(R, t, cv2.TM_SQDIFF, mask=np.dstack([m, m, m])) / area
                th, tw = wp.shape[:2]
                ys, xs = np.mgrid[0:res.shape[0], 0:res.shape[1]]
                cx, cy = (xs + tw / 2) / f, (ys + th / 2) / f
                bad = (np.abs(cx - around[0]) > win) | (np.abs(cy - around[1]) > win)
                res = np.where(bad, np.inf, res)
                mn, _, loc, _ = cv2.minMaxLoc(res)
                if not np.isfinite(mn):
                    continue
                if best is None or mn < best[0]:
                    best = (mn, sx, sy, r, (loc[0] + tw / 2) / f, (loc[1] + th / 2) / f)
    return best


def paste(canvas, wp, cx, cy):
    """dán RGBA wp tâm (cx, cy) vào canvas RGBA cỡ concept (ghi đè theo alpha)."""
    H, W = canvas.shape[:2]
    x0, y0 = int(round(cx - wp.shape[1] / 2)), int(round(cy - wp.shape[0] / 2))
    ax0, ay0, ax1, ay1 = max(0, x0), max(0, y0), min(W, x0 + wp.shape[1]), min(H, y0 + wp.shape[0])
    if ax1 <= ax0 or ay1 <= ay0:
        return canvas
    src = wp[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0].astype(np.float32)
    a = src[:, :, 3:4] / 255.0
    dst = canvas[ay0:ay1, ax0:ax1].astype(np.float32)
    dst[:, :, :3] = src[:, :, :3] * a + dst[:, :, :3] * (1 - a)
    dst[:, :, 3] = np.maximum(dst[:, :, 3], src[:, :, 3])
    canvas[ay0:ay1, ax0:ax1] = dst.astype(np.uint8)
    return canvas


def flood(fg, ink, seeds):
    """loang vùng từ hạt giống, 1 px mỗi bước, nét mực là tường; nét mực và chỗ chưa tới nhận nhãn gần nhất."""
    H, W = fg.shape
    lab = np.zeros((H, W), np.int32)
    names = list(seeds)
    for i, n in enumerate(names, 1):
        for x, y in seeds[n]:
            cv2.circle(lab, (int(x), int(y)), 5, i, -1)
    lab[~fg] = 0
    free = fg & ~ink
    k = np.ones((3, 3), np.uint8)
    for _ in range(3000):
        changed = False
        for i in range(1, len(names) + 1):
            d = cv2.dilate((lab == i).astype(np.uint8), k) > 0
            new = d & free & (lab == 0)
            if new.any():
                lab[new] = i
                changed = True
        if not changed:
            break
    for _ in range(80):
        rest = fg & (lab == 0)
        if not rest.any():
            break
        for i in range(1, len(names) + 1):
            d = cv2.dilate((lab == i).astype(np.uint8), k) > 0
            lab[d & rest] = i
    return lab, names


def doc_concept(k):
    base = os.path.join(HERE, "inbox", f"{CODE}_{k}")
    ref = np.array(Image.open(os.path.join(base, "tai_ve", CFG[k]["concept"])).convert("RGB"))
    fg = fg_mask(ref)
    ink = (ref.astype(np.int32).sum(2) / 3 < INK) & fg
    return base, ref, fg, ink


PAL = np.array([(255, 255, 255), (230, 80, 80), (80, 160, 230), (90, 200, 120), (240, 200, 60), (200, 120, 220), (120, 220, 220),
                (250, 150, 90), (150, 150, 150), (60, 60, 60), (170, 90, 40), (40, 120, 90)], np.uint8)


def nhan(k):
    base, ref, fg, ink = doc_concept(k)
    lab, names = flood(fg, ink, CFG[k]["seeds"])
    yy = np.mgrid[0:lab.shape[0], 0:lab.shape[1]][0]
    for n, y0 in CFG[k].get("clamp_y", {}).items():
        lab[(lab == names.index(n) + 1) & (yy < y0)] = names.index("than") + 1
    out = os.path.join(base, "lai")
    os.makedirs(out, exist_ok=True)
    vis = PAL[np.clip(lab, 0, len(PAL) - 1)].copy()
    vis[ink] = (40, 30, 20)
    for i, (n, pts) in enumerate(CFG[k]["seeds"].items(), 1):
        for x, y in pts:
            cv2.circle(vis, (int(x), int(y)), 6, (0, 0, 0), 2)
        ys, xs = np.nonzero(lab == i)
        if len(xs):
            cv2.putText(vis, n, (int(xs.mean()) - 30, int(ys.mean())), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    Image.fromarray(np.concatenate([ref, vis], 1)).save(os.path.join(out, "nhan.png"))
    for i, n in enumerate(names, 1):
        m = lab == i
        ys, xs = np.nonzero(m)
        print(f"  {n:8s} {int(m.sum()):7d} px  x {xs.min()}-{xs.max()}  y {ys.min()}-{ys.max()}")
    np.save(os.path.join(out, "nhan.npy"), lab.astype(np.int8))
    json.dump({"names": names}, open(os.path.join(out, "nhan.json"), "w"))
    return lab, names


if __name__ == "__main__":
    cmd, k = sys.argv[1], int(sys.argv[2])
    if cmd == "nhan":
        nhan(k)
    elif cmd in ("cat", "dat", "lai"):
        import tm03_ghep as G  # noqa: E402
        getattr(G, cmd)(k)
