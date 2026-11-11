# -*- coding: utf-8 -*-
"""tm09 cách lai (DAC_TA mục 5 "Cách lai"): các lớp thân chính CẮT THẲNG TỪ CONCEPT đã duyệt (đầu + sừng, thân + cổ/họng + gờ băng,
đuôi + chùy, bốn chân phần thấy) bằng loang vùng từ hạt giống đọc trên concept kẻ lưới, nét mực là tường (như thuy_long_lien);
mảnh GPT chỉ còn hàm dưới, lòng miệng, lưỡi, mí, và làm nguồn vẽ bù thân dưới chân / dưới đầu. Ra inbox/tm09_<k>/manh_lai/:
<lớp>.png (RGBA, cắt sát) + lop.json (gốc crop, hạt giống) + nhan.png (bản đồ vùng để soi).

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm09_lai.py 2
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

import rig as riglib  # noqa: E402
import tm09_place as tp  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm09"

# hạt giống (px concept) từng lớp; "bo" = vùng bỏ (hàm dưới + lòng miệng của concept: thay bằng mảnh GPT)
SEEDS = {
    2: {"dau": [(1200, 350), (1300, 330), (1400, 350), (1100, 330), (1130, 200), (1060, 150), (980, 230), (950, 300), (1220, 420)],
        "than": [(800, 580), (650, 560), (950, 500), (1030, 450), (1060, 560), (900, 400), (720, 455), (560, 480), (900, 450), (1000, 600)],
        "duoi": [(400, 520), (300, 480), (240, 430), (160, 330), (100, 300), (380, 540)],
        "chan_tn": [(930, 720), (960, 800)], "chan_sn": [(520, 720), (470, 800)],
        "chan_tx": [(1130, 740), (1150, 800)], "chan_sx": [(700, 740), (700, 800)],
        "bo": [(1300, 500), (1250, 470), (1380, 520)]},
    1: {"dau": [(1100, 380), (1250, 350), (1380, 380), (1020, 300), (920, 200), (790, 260), (1100, 450), (1250, 470), (1380, 440)],
        "than": [(560, 650), (450, 620), (700, 620), (850, 500), (640, 470), (510, 505), (390, 540), (760, 560)],
        "duoi": [(250, 640), (170, 610), (120, 600)],
        "chan_tn": [(700, 800), (760, 850)], "chan_sn": [(340, 820), (380, 860)],
        "chan_tx": [(1030, 800), (1070, 850)], "chan_sx": [(570, 800), (600, 850)],
        "bo": [(1150, 560), (1250, 590), (1120, 525), (1300, 560)]},
}
ORDER = ["chan_sx", "chan_tx", "duoi", "than", "chan_sn", "chan_tn", "bo", "dau"]   # vẽ sau → trước ("bo" = hàm dưới + lòng miệng concept → lớp ham)
# tường kẻ tay (px concept) ở ranh không có nét mực (chibi: má/hàm nối liền cổ)
# dạng 1: tường đầu–cổ là CUNG bo theo má (lồi về sau), không thẳng đứng, kẻo dải thân mọc thêm lộ thành cạnh thẳng khi đầu ngẩng
_ARC1 = [(1030, 200), (1055, 265), (995, 345), (962, 430), (990, 520), (1050, 595), (1040, 690)]
WALLS = {2: [], 1: list(zip(_ARC1[:-1], _ARC1[1:]))}
GROW_PX = {2: 65, 1: 80}   # dải thân mọc thêm dưới đầu/chân (px concept ≈ 39 / 40 px rig)


def flood(fg, ink, seeds):
    """loang vùng từ hạt giống, 1 px mỗi bước, nét mực là tường; rồi nét mực nhận nhãn vùng gần nhất."""
    H, W = fg.shape
    lab = np.zeros((H, W), np.int32)
    names = list(seeds)
    for i, n in enumerate(names, 1):
        for x, y in seeds[n]:
            cv2.circle(lab, (int(x), int(y)), 6, i, -1)
    lab[~fg] = 0
    free = fg & ~ink
    k = np.ones((3, 3), np.uint8)
    for _ in range(2000):
        changed = False
        for i in range(1, len(names) + 1):
            m = (lab == i).astype(np.uint8)
            d = cv2.dilate(m, k) > 0
            new = d & free & (lab == 0)
            if new.any():
                lab[new] = i
                changed = True
        if not changed:
            break
    # nét mực và chỗ chưa tới: nhãn gần nhất (loang không tường)
    for _ in range(60):
        rest = fg & (lab == 0)
        if not rest.any():
            break
        for i in range(1, len(names) + 1):
            m = (lab == i).astype(np.uint8)
            d = cv2.dilate(m, k) > 0
            lab[d & rest] = i
    return lab, names


def warp_part(k, n, pl, parts):
    """mảnh GPT đặt vào concept theo place.json (như so_ghep): trả RGBA cỡ concept."""
    t = pl[n]
    part = parts[n]
    wp = tp.warp2(part, t["sx"], t["sy"], t["r"], t["lat"])
    cx, cy = t["cx"], t["cy"]
    return wp, int(round(cx - wp.shape[1] / 2)), int(round(cy - wp.shape[0] / 2))


def paste_into(canvas, wp, x0, y0):
    H, W = canvas.shape[:2]
    ax0, ay0, ax1, ay1 = max(0, x0), max(0, y0), min(W, x0 + wp.shape[1]), min(H, y0 + wp.shape[0])
    if ax1 <= ax0 or ay1 <= ay0:
        return
    canvas[ay0:ay1, ax0:ax1] = wp[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0]


def lai(k):
    base = os.path.join(HERE, "inbox", f"{CODE}_{k}")
    out = os.path.join(base, "manh_lai")
    os.makedirs(out, exist_ok=True)
    ref = np.array(Image.open(os.path.join(base, "tai_ve", "L1_duyet.png")).convert("RGB"))
    H, W = ref.shape[:2]
    fg = riglib.fg_mask(ref) > 0
    lum = ref.astype(np.int32).sum(2) / 3
    ink = (lum < 85) & fg
    for p0, p1 in WALLS.get(k, []):
        cv2.line(ink.view(np.uint8), p0, p1, 1, 3)
    ink = ink.astype(bool)
    lab, names = flood(fg, ink, SEEDS[k])
    # mảnh GPT thân, đuôi đặt theo place.json: nguồn vẽ bù
    pj = json.load(open(os.path.join(base, "place.json"), encoding="utf-8"))
    pl = pj["parts"]
    parts = {n: np.array(Image.open(os.path.join(base, "manh", n + ".png")).convert("RGBA")) for n in ("than", "duoi")}
    bu = {}
    for n in ("than", "duoi"):
        canvas = np.zeros((H, W, 4), np.uint8)
        wp, x0, y0 = warp_part(k, n, pl, parts)
        paste_into(canvas, wp, x0, y0)
        bu[n] = canvas
    rgba = np.dstack([ref, np.where(fg, 255, 0).astype(np.uint8)])
    idx = {n: i + 1 for i, n in enumerate(names)}
    info = {"ref_size": [W, H], "ground": pj["ground"], "lop": {}}
    legs = [n for n in names if n.startswith("chan")]
    grow_than = np.zeros((H, W), bool)
    for n in ORDER:
        m = lab == idx[n]
        layer = np.where(m[..., None], rgba, 0).astype(np.uint8)
        if n == "than":
            # lớp thân MỌC THÊM dưới đầu, dưới chân (pokiclash-spine-rig mục 12): dải rộng GROW px concept quanh vùng thân, nằm trong
            # vùng đầu/chân; vẽ bù từ mảnh thân GPT đã đặt, chỗ GPT không phủ thì inpaint từ màu lớp thân + nét mực dọc mép ngoài
            hid = np.zeros((H, W), bool)
            for g in [l for l in legs if l.endswith("n")] + ["dau", "bo"]:   # dưới đầu, hàm và chân GẦN (thân vẽ sau chân xa: mọc dưới chân xa sẽ che chân xa)
                hid |= lab == idx[g]
            GROW = int(GROW_PX[k])
            near = cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=GROW) > 0
            grow = hid & near
            src = bu["than"]
            take = grow & (src[..., 3] > 128)
            layer[take] = src[take]
            layer[..., 3][take] = 255
            rest = grow & ~take
            if rest.any():
                # tô màu chính của lớp thân (trung vị pixel không phải mực, không phải tấm bụng nhạt) + vân nhẹ; inpaint từ biên
                # lấy nhầm màu nét mực nên dải bù ra nâu đen (lỗi đã gặp)
                px = ref[m]
                lum_m = px.astype(np.int32).sum(1) / 3
                body_px = px[(lum_m > 85) & (lum_m < 190)]
                col = np.median(body_px, axis=0) if len(body_px) else np.array([31, 85, 102])
                rng = np.random.default_rng(9)
                noise = rng.integers(-10, 11, (int(rest.sum()), 1))
                layer[..., :3][rest] = np.clip(col[None, :] + noise, 0, 255).astype(np.uint8)
                layer[..., 3][rest] = 255
            grow_than = grow.copy()
            full = m | grow
            edge = full & ~(cv2.erode(full.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=3) > 0) & grow
            layer[..., :3][edge] = (43, 33, 24)
            print(f"  thân: mọc thêm {int(grow.sum())} px dưới đầu/chân (GPT {int(take.sum())}, inpaint {int(rest.sum())}, mực mép {int(edge.sum())})")
        if n == "duoi":
            src = bu["duoi"]
            take = (lab == idx["than"]) & (src[..., 3] > 128)
            # chỉ phần gốc đuôi sát hông (trong 80 px quanh vùng đuôi)
            near = cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=80) > 0
            take &= near
            layer[take] = src[take]
            layer[..., 3][take] = 255
            print(f"  đuôi: vẽ bù gốc {int(take.sum())} px")
        if n in ("bo", "dau") and WALLS.get(k):
            # mép cắt bằng tường kẻ tay (không theo nét mực) làm mờ dần 30 px về phía tường để không lộ cạnh thẳng khi đầu ngẩng
            wall = np.zeros((H, W), np.uint8)
            for p0, p1 in WALLS[k]:
                if min(p0[1], p1[1]) >= 400:   # chỉ đoạn tường dưới mắt (má–họng); đỉnh cung qua sọ giữ mép cứng
                    cv2.line(wall, p0, p1, 1, 1)
            dist = cv2.distanceTransform((wall == 0).astype(np.uint8), cv2.DIST_L2, 5)
            fade = np.clip(dist / 30.0, 0, 1)
            fade = np.where(grow_than, fade, 1.0)   # chỉ mờ ở chỗ có dải thân mọc thêm nằm dưới (không mờ đỉnh sọ)
            layer[..., 3] = (layer[..., 3] * fade).astype(np.uint8)
        # bỏ mẩu rời nhỏ (nét mực nhận nhầm nhãn): giữ cụm ≥ 400 px
        nlab, cc, st, _ = cv2.connectedComponentsWithStats((layer[..., 3] > 128).astype(np.uint8), connectivity=8)
        small = np.isin(cc, [i for i in range(1, nlab) if st[i, cv2.CC_STAT_AREA] < 400])
        if small.any():
            layer[small] = 0
            print(f"  {n}: bỏ {int(small.sum())} px mẩu rời")
        # mép mềm 1 px
        a = layer[..., 3].astype(np.float32) / 255
        a = cv2.GaussianBlur(a, (3, 3), 0.8)
        layer[..., 3] = (np.clip(a, 0, 1) * 255).astype(np.uint8)
        ys, xs = np.nonzero(layer[..., 3] > 8)
        if not len(xs):
            print(f"  {n}: vùng trống!")
            continue
        x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
        crop = layer[y0:y1, x0:x1]
        nn = "ham" if n == "bo" else n
        Image.fromarray(crop, "RGBA").save(os.path.join(out, nn + ".png"))
        info["lop"][nn] = {"x0": x0, "y0": y0, "w": x1 - x0, "h": y1 - y0, "px": int(m.sum())}
        print(f"  {n:8s} ({x0},{y0}) {x1 - x0}x{y1 - y0}, {int(m.sum())} px")
    json.dump(info, open(os.path.join(out, "lop.json"), "w"), indent=1)
    # bản đồ vùng để soi
    pal = np.array([(255, 255, 255), (230, 80, 80), (80, 160, 230), (90, 200, 120), (240, 200, 60), (200, 120, 220), (120, 220, 220),
                    (250, 150, 90), (150, 150, 150), (60, 60, 60)], np.uint8)
    vis = pal[np.clip(lab, 0, len(pal) - 1)]
    vis[ink] = (40, 30, 20)
    for n, pts in SEEDS[k].items():
        for x, y in pts:
            cv2.circle(vis, (int(x), int(y)), 7, (0, 0, 0), 2)
    side = np.concatenate([ref, vis], 1)
    Image.fromarray(side).save(os.path.join(out, "nhan.png"))
    print(f"  nhãn: {', '.join(f'{n}={idx[n]}' for n in names)} → {os.path.join(out, 'nhan.png')}")


if __name__ == "__main__":
    lai(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
