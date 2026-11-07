"""Tự kiểm ảnh GPT trước khi Claude xem bằng mắt (2026-11-07): nền, điểm sáng trắng, độ dày nét mực, độ trùng hình gốc.

    py -3 -I ArtGen/Heroes/tools/kiem_anh.py <ảnh.png> [--orig refs/<hệ>/<mã>/orig/Nxx.png] [--px 12]

In một dòng mỗi ảnh:
  nen       phần nền trắng nối mép (tỉ lệ ảnh); nền xám, lưới, giấy màu thì thấp bất thường;
  sang      số đốm trắng tinh nằm TRONG hình (điểm sáng, vệt bóng loáng); chấm sáng trong mắt cũng tính, nên vài đốm nhỏ
            là bình thường, nhiều đốm hay đốm to là lỗi "không ánh sáng";
  vien      độ dày nét mực ở mép ngoài (trung vị, px) so với số đã ghi (--px);
  iou       độ trùng bóng hình mới với bóng hình gốc của nhóm (--orig), cùng khung 1024 (nhóm giữ viền cần gần 0,8 trở lên);
  lech      tâm hình mới lệch tâm hình gốc bao nhiêu px (dx, dy).
"""
import sys

import numpy as np
from PIL import Image, ImageDraw


def fg_mask(path, side=1024):
    im = Image.open(path).convert("RGB")
    if im.size != (side, side):
        im = im.resize((side, side), Image.LANCZOS)
    a = np.asarray(im).astype(int)
    white = a.min(axis=2) > 232
    m = Image.fromarray((white * 255).astype(np.uint8), "L").copy()
    px = m.load()
    W, H = m.size
    for xy in [(x, 0) for x in range(0, W, 4)] + [(x, H - 1) for x in range(0, W, 4)] + \
              [(0, y) for y in range(0, H, 4)] + [(W - 1, y) for y in range(0, H, 4)]:
        if px[xy] == 255:
            ImageDraw.floodfill(m, xy, 128)
    bg = np.asarray(m) == 128
    return a, ~bg, bg.mean()


def blobs(mask, min_px):
    """Số cụm điểm (4 hướng) có ít nhất min_px điểm, trên lưới thu nhỏ 4 lần cho nhanh."""
    m = Image.fromarray(mask.astype(np.uint8) * 255).copy()
    px = m.load()
    W, H = m.size
    n, big = 0, 0
    for y in range(H):
        for x in range(W):
            if px[x, y] == 255:
                before = (np.asarray(m) == 255).sum()
                ImageDraw.floodfill(m, (x, y), 60)
                size = before - (np.asarray(m) == 255).sum()
                if size >= min_px:
                    n += 1
                    big = max(big, size)
    return n, big


def line_width(a, fg):
    """Độ dày nét mực sát nền: từ mỗi điểm mép đi vào trong theo 4 hướng tới khi hết màu mực (tối)."""
    # mực nâu sẫm #2B2118: gần màu mực, hoặc rất tối; màu đậm của thiết kế (xanh mòng két đậm) không tính
    ink = np.sqrt(((a - np.array([43, 33, 24])) ** 2).sum(axis=2))
    dark = ((a.max(axis=2) < 125) & (ink < 75)) | (a.max(axis=2) < 55)
    edge = fg & ~np.roll(fg, 1, 0) | fg & ~np.roll(fg, -1, 0) | fg & ~np.roll(fg, 1, 1) | fg & ~np.roll(fg, -1, 1)
    ys, xs = np.nonzero(edge)
    if not len(xs):
        return None
    pick = np.random.default_rng(0).choice(len(xs), min(600, len(xs)), replace=False)
    out = []
    for i in pick:
        y, x = ys[i], xs[i]
        best = None
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            yy, xx = y - dy, x - dx
            if 0 <= yy < fg.shape[0] and 0 <= xx < fg.shape[1] and fg[yy, xx]:
                continue  # hướng này không đi vào trong
            k = 0
            while 0 <= y + dy * k < fg.shape[0] and 0 <= x + dx * k < fg.shape[1] and dark[y + dy * k, x + dx * k]:
                k += 1
            if k:
                best = k if best is None else min(best, k)
        if best:
            out.append(best)
    return float(np.median(out)) if out else None


def main(argv):
    orig = argv[argv.index("--orig") + 1] if "--orig" in argv else None
    px = float(argv[argv.index("--px") + 1]) if "--px" in argv else None
    path = argv[0]
    a, fg, nen = fg_mask(path)
    pure = (a.min(axis=2) > 245) & fg
    small = np.asarray(Image.fromarray(pure.astype(np.uint8) * 255).resize((256, 256), Image.BOX)) > 100
    n_sang, big = blobs(small, 2)
    lw = line_width(a, fg)
    parts = [f"nen {nen:.2f}", f"sang {n_sang} dom (to nhat {big * 16} px)",
             f"vien {lw:.0f} px" + (f" (can {px:.0f})" if px else "") if lw else "vien ?"]
    if orig:
        _, ofg, _ = fg_mask(orig)
        u = (fg | ofg).sum()
        parts.append(f"iou {(fg & ofg).sum() / u:.2f}" if u else "iou ?")
        ys, xs = np.nonzero(fg)
        oys, oxs = np.nonzero(ofg)
        if len(xs) and len(oxs):
            parts.append(f"lech ({xs.mean() - oxs.mean():+.0f}, {ys.mean() - oys.mean():+.0f}) px")
    print(f"{path.replace(chr(92), '/').split('/')[-1]}: " + ", ".join(parts))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
