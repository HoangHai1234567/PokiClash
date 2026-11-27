# Cắt 4 tờ hình gói cửa hàng bản 2 (2026-11-27, gen Magnific GPT 2.6 nền trong, lưới 2 x 3) vào Assets/03 Art/Shop/v2/<tên>.png.
# Tờ nguồn nằm cạnh script: goi_bi_v2b.png, trung_v2.png, goi_lon_v2.png, dac_quyen_v2.png; icon riêng từng loại ưu đãi (cùng ngày,
# uu_dai_v2.png lưới 2 x 3, uu_dai_v2b.png lưới 2 x 2) → uu2_<mã mẫu ưu đãi>.png (ShopUi.TplArt).
# - Nền GPT 2.6 rải điểm mờ (độ đục 1–63): kéo giãn độ đục (a - 70) * 255 / 185 rồi chỉ giữ quanh các vùng liền của hình;
# - mỗi vùng liền (hình, lấp lánh rời) gán vào ô theo tâm, ô cắt sát + lề 8; điểm trong suốt tô trắng (mép sticker trắng, khỏi viền đen khi lọc);
# - trứng: đo đường nối vòm / thân (vệt nâu ngang dài nhất trong 35–75% chiều cao, như cat_trung.py) ghi vào trung2.json
#   (EggHatchView.Seam lấy số ở đây).
# Chạy: py -3 -I ArtGen/Shop/v2/cat_v2.py [tên tờ ...] (không ghi tên tờ: cắt hết)
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "Assets", "03 Art", "Shop", "v2")
PAD = 8

SHEETS = [
    ("goi_bi_v2b.png", ["goi2_bi_1", "goi2_bi_2", "goi2_bi_3", "goi2_bi_4", "goi2_bi_5", "goi2_bi_6"]),
    ("trung_v2.png", ["trung2_0", "trung2_1", "trung2_2", "trung2_3", "trung2_4", "goi2_ve"]),
    ("goi_lon_v2.png", ["goi2_nhap_mon", "goi2_khoi_hanh_1", "goi2_khoi_hanh_2", "goi2_khoi_hanh_3", "goi2_lo_bi", "goi2_tuong_tuan"]),
    ("dac_quyen_v2.png", ["goi2_the_tuan", "goi2_the_phieu_luu", "goi2_quy", "goi2_bo_qc", "goi2_da_nho", "goi2_da_lon"]),
    ("uu_dai_v2.png", ["uu2_flash", "uu2_hot", "uu2_relief", "uu2_companion", "uu2_nearstar", "uu2_jump"]),
    ("uu_dai_v2b.png", ["uu2_newisle", "uu2_comeback", "uu2_chain", "uu2_offer"], 2, 2),
]


def seam_of(rgba):
    h, w = rgba.shape[:2]
    best, best_y = -1, h // 2
    for y in range(int(h * 0.35), int(h * 0.75)):
        r, g, b, a = rgba[y, :, 0], rgba[y, :, 1], rgba[y, :, 2], rgba[y, :, 3]
        dark = (a > 0) & (r < 110) & (g < 90) & (b < 80)
        run = cur = 0
        for d in dark:
            cur = cur + 1 if d else 0
            run = max(run, cur)
        if run > best:
            best, best_y = run, y
    return round(best_y / h, 4)


def cut(src, names, rows=2, cols=3):
    im = np.array(Image.open(os.path.join(HERE, src)).convert("RGBA"))
    h, w = im.shape[:2]
    a = im[:, :, 3].astype(np.float32)
    a = np.clip((a - 70) * 255 / 185, 0, 255).astype(np.uint8)
    solid = (a >= 128).astype(np.uint8)
    cw, ch = w / cols, h / rows
    # co vùng hình 6 px để cắt chỗ hai viền sticker chạm nhau, lấy các khối chính (hình) gán ô theo tâm
    core = cv2.erode(solid, np.ones((3, 3), np.uint8), iterations=6)
    n, lab, stats, cent = cv2.connectedComponentsWithStats(core, connectivity=8)
    seeds = [np.zeros((h, w), np.uint8) for _ in names]
    yy, xx = np.mgrid[0:h, 0:w]
    cell_of = np.minimum(rows - 1, (yy / ch).astype(int)) * cols + np.minimum(cols - 1, (xx / cw).astype(int))
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] < 0.04 * cw * ch:
            continue
        # lõi vẫn dính hai hình (tràn quá 1,2 ô): chia theo lưới thành hạt giống của từng ô
        tall, wide = stats[i, cv2.CC_STAT_HEIGHT] > 1.2 * ch, stats[i, cv2.CC_STAT_WIDTH] > 1.2 * cw
        if tall or wide:
            # chỉ chia theo chiều bị tràn; chiều kia lấy hàng / cột của tâm lõi
            sel = lab == i
            cx, cy = cent[i]
            row = np.minimum(rows - 1, (yy / ch).astype(int)) if tall else min(rows - 1, int(cy / ch))
            col = np.minimum(cols - 1, (xx / cw).astype(int)) if wide else min(cols - 1, int(cx / cw))
            cell = row * cols + col
            for k in range(len(names)):
                seeds[k][sel & (cell == k)] = 1
            continue
        cx, cy = cent[i]
        k = min(rows - 1, int(cy * rows / h)) * cols + min(cols - 1, int(cx * cols / w))
        seeds[k][lab == i] = 1
    # gán từng vùng liền của hình: vùng chứa một lõi → ô đó; vùng không lõi (lấp lánh rời) → ô có lõi gần nhất (xa quá 80 px thì bỏ,
    # bụi nền); vùng chứa nhiều lõi (hình dính nhau qua viền) → loang từ lõi theo độ dày (watershed): chỗ nối mỏng thành ranh giới
    dist = np.stack([cv2.distanceTransform((1 - s).astype(np.uint8), cv2.DIST_L2, 5) for s in seeds])
    thick = cv2.distanceTransform(solid, cv2.DIST_L2, 5)
    n2, lab2, stats2, _ = cv2.connectedComponentsWithStats(solid, connectivity=8)
    masks = [np.zeros((h, w), np.uint8) for _ in names]
    loose = []
    for i in range(1, n2):
        if stats2[i, cv2.CC_STAT_AREA] < 40:
            continue
        sel = lab2 == i
        has = [k for k in range(len(names)) if (seeds[k] & sel).any()]
        if len(has) == 0:
            loose.append(sel)
        elif len(has) == 1:
            masks[has[0]][sel] = 1
        else:
            mk = np.where(sel, 0, 255).astype(np.int32)
            for k in has:
                mk[(seeds[k] == 1) & sel] = k + 1
            t = thick * sel
            img = (255 - np.clip(t * 255 / max(1, t.max()), 0, 255)).astype(np.uint8)
            cv2.watershed(cv2.merge([img, img, img]), mk)
            for k in has:
                part = ((mk == k + 1) & sel).astype(np.uint8)
                masks[k][part == 1] = 1
                # mảnh không chứa lõi (mẩu của hình bên cạnh, nối qua cầu mảnh: co 4 px để cắt cầu) trả về hình có lõi gần nhất khác
                pe = cv2.erode(part, np.ones((3, 3), np.uint8), iterations=4)
                pn, plab = cv2.connectedComponents(pe, connectivity=8)
                for j in range(1, pn):
                    piece = (plab == j).astype(np.uint8)
                    if (seeds[k][piece == 1] == 1).any():
                        continue
                    region = (cv2.dilate(piece, np.ones((3, 3), np.uint8), iterations=6) & part) == 1
                    other = min((o for o in has if o != k), key=lambda o: dist[o][region].min())
                    masks[k][region] = 0
                    masks[other][region] = 1
    # vùng rời không lõi (lấp lánh, mẩu viền): thuộc hình đầy đủ gần nhất, xa quá 80 px thì bỏ (bụi nền)
    full = [cv2.distanceTransform((1 - m).astype(np.uint8), cv2.DIST_L2, 5) for m in masks]
    for sel in loose:
        dmin = [d[sel].min() for d in full]
        k = int(np.argmin(dmin))
        if dmin[k] < 80:
            masks[k][sel] = 1
    # điểm mép mềm (độ đục dưới 128) thuộc hình gần nhất
    near = np.stack([cv2.distanceTransform((1 - m).astype(np.uint8), cv2.DIST_L2, 5) for m in masks]).argmin(axis=0)
    meta = {}
    kernel = np.ones((7, 7), np.uint8)
    for k, name in enumerate(names):
        m = cv2.dilate(masks[k], kernel) & (near == k).astype(np.uint8)
        ys, xs = np.nonzero(masks[k])
        if len(xs) == 0:
            print(f"{name}: trống")
            continue
        x0, x1 = max(0, xs.min() - PAD), min(w, xs.max() + 1 + PAD)
        y0, y1 = max(0, ys.min() - PAD), min(h, ys.max() + 1 + PAD)
        out = im[y0:y1, x0:x1].copy()
        oa = (a[y0:y1, x0:x1] * m[y0:y1, x0:x1]).astype(np.uint8)
        if name.startswith("trung2_"):
            # trứng: dưới hàng rộng nhất, mép chỉ được thu vào (mẩu viền hình bên dưới dính đáy thì bỏ)
            hh = oa.shape[0]
            cover = [(np.nonzero(oa[y] > 60)[0]) for y in range(hh)]
            widths = [c[-1] - c[0] if len(c) else 0 for c in cover]
            y0w = int(np.argmax(widths[hh // 2:])) + hh // 2
            for y in range(max(y0w + 2, int(hh * 0.92)), hh):
                if widths[y] > widths[y - 1] + 1 and widths[y - 1] > 0:
                    oa[y - 1:, :] = 0
                    cover = [(np.nonzero(oa[yy] > 60)[0]) for yy in range(hh)]
                    break
            lo, hi = cover[y0w][0], cover[y0w][-1]
            for y in range(y0w + 1, hh):
                c = cover[y]
                if len(c) == 0:
                    continue
                lo, hi = max(lo, c[0] - 1), min(hi, c[-1] + 1)
                oa[y, :max(0, lo - 2)] = 0
                oa[y, hi + 3:] = 0
        out[:, :, 3] = oa
        out[oa == 0, :3] = 255
        ys2, xs2 = np.nonzero(oa)
        out = out[max(0, ys2.min() - PAD):ys2.max() + 1 + PAD, max(0, xs2.min() - PAD):xs2.max() + 1 + PAD]
        path = os.path.join(OUT, name + ".png")
        Image.fromarray(out, "RGBA").save(path)
        info = f"{name}: {out.shape[1]}x{out.shape[0]}"
        if name.startswith("trung2_"):
            s = seam_of(out)
            meta[name[-1]] = {"w": int(out.shape[1]), "h": int(out.shape[0]), "seam": s}
            info += f", đường nối {s}"
        print(info)
    return meta


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(OUT, exist_ok=True)
    only = set(sys.argv[1:])
    seams = {}
    for src, names, *grid in SHEETS:
        if only and src not in only:
            continue
        seams.update(cut(src, names, *grid))
    if seams:  # chỉ ghi khi đã cắt tờ trứng
        with open(os.path.join(HERE, "trung2.json"), "w", encoding="utf-8") as f:
            json.dump(seams, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
