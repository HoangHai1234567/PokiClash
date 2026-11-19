# Cắt tờ ảnh Magnific (nền trắng đặc, chưa trong suốt) thành từng sprite cho máy bi (2026-11-19, hiệu ứng mở rương).
# Mỗi ô của lưới: xoá nền trắng loang từ mép ô vào (ruột trắng bên trong viền mực giữ nguyên), mép mềm 1–2 px theo độ sáng,
# cắt sát hình, chừa lề, thu về cạnh dài tối đa MAX px, ghi vào Assets/03 Art/Pachinko.
#   py -3 -I ArtGen/Pachinko/cat_magnific.py            (cắt cả hai tờ trong tai_ve/magnific)
#   py -3 -I ArtGen/Pachinko/cat_magnific.py --soi out.png  (thêm tờ soi các sprite đã cắt trên nền tối)
#   py -3 -I ArtGen/Pachinko/cat_magnific.py --ra <thư mục>   (ghi ra chỗ khác, không đụng Assets)
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
SRC = HERE / "tai_ve" / "magnific"
OUT = HERE.parent.parent / "Assets" / "03 Art" / "Pachinko"

# tờ, số cột, số hàng, tên từng ô theo thứ tự (None = bỏ), cạnh dài tối đa
SHEETS = [
    ("fx_mo_ruong.png", 4, 3, [
        "pk_fx_hao_quang", "pk_fx_quat_sang", "pk_fx_bung", "pk_fx_vong_giot",
        "pk_fx_giay_dai", "pk_fx_giay_tron", "pk_fx_lap_lanh_beo", "pk_fx_giay_vuong",
        "pk_fx_giot", "pk_fx_bui", "pk_fx_day_xoan", "pk_fx_tinh_tu",
    ], 256),
    ("ruong_mo_xu.png", 3, 2, [
        "pk_ruong_go_mo_sach", "pk_ruong_bac_mo_sach", "pk_ruong_vang_mo_sach",
        "pk_xu", "pk_xu_nghieng", "pk_ngoc_tim",
    ], 320),
]
WHITE = 236  # sáng hơn mức này ở cả ba kênh và ít màu thì coi là nền


def is_bg(px):
    r, g, b = px[..., 0].astype(int), px[..., 1].astype(int), px[..., 2].astype(int)
    return (np.minimum(np.minimum(r, g), b) >= WHITE) & ((np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)) < 18)


def flood(bgmask):
    """vùng nền nối với mép ô"""
    h, w = bgmask.shape
    seen = np.zeros_like(bgmask, dtype=bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if bgmask[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if bgmask[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and bgmask[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((ny, nx))
    return seen


def dilate(m, r):
    out = m.copy()
    for _ in range(r):
        n = out.copy()
        n[1:, :] |= out[:-1, :]
        n[:-1, :] |= out[1:, :]
        n[:, 1:] |= out[:, :-1]
        n[:, :-1] |= out[:, 1:]
        out = n
    return out


def background(a):
    """nền: vùng trắng nối với mép tờ; viền mực được nong 2 px trước khi loang để khe hở nhỏ của nét không làm rò vào ruột hình"""
    cand = is_bg(a)
    ink = a.min(axis=2) < 170
    seen = flood(cand & ~dilate(ink, 2))
    # trả lại phần nền sát nét bị nong che
    return dilate(seen, 3) & cand


def matte(a, bg):
    alpha = np.where(bg, 0, 255).astype(np.float32)
    # mép mềm: điểm hình sát nền lấy alpha theo độ tối (viền mực đậm giữ đặc, điểm gần trắng mờ dần)
    edge = dilate(bg, 1) & ~bg
    lum = a.min(axis=2).astype(np.float32)
    soft = np.clip((255 - lum) / (255 - 150), 0, 1) * 255
    alpha[edge] = np.minimum(alpha[edge], soft[edge])
    return np.dstack([a, alpha.astype(np.uint8)])


def blobs(fg):
    """các mảng hình liền (4 hướng): danh sách (nhãn, điểm giữa, hộp)"""
    h, w = fg.shape
    lab = np.zeros((h, w), dtype=np.int32)
    out = []
    n = 0
    for y0 in range(h):
        row = fg[y0]
        for x0 in np.nonzero(row & (lab[y0] == 0))[0]:
            if lab[y0, x0]:
                continue
            n += 1
            q = deque([(y0, x0)])
            lab[y0, x0] = n
            ys, xs = [], []
            while q:
                y, x = q.popleft()
                ys.append(y)
                xs.append(x)
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and fg[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = n
                        q.append((ny, nx))
            out.append((n, (sum(xs) / len(xs), sum(ys) / len(ys)), len(xs)))
    return lab, out


def main():
    global OUT
    if "--ra" in sys.argv:
        OUT = Path(sys.argv[sys.argv.index("--ra") + 1])
        OUT.mkdir(parents=True, exist_ok=True)
    made = []
    for name, cols, rows, names, mx in SHEETS:
        sheet = Image.open(SRC / name).convert("RGB")
        a = np.array(sheet)
        bg = background(a)
        rgba = matte(a, bg)
        lab, bl = blobs(~bg)
        cw, ch = sheet.width / cols, sheet.height / rows
        cell_of = np.zeros(lab.max() + 1, dtype=np.int32) - 1
        for n, (cx, cy), area in bl:
            if area < 30:
                continue  # vụn
            cell_of[n] = min(cols - 1, int(cx / cw)) + cols * min(rows - 1, int(cy / ch))
        for i, nm in enumerate(names):
            if not nm:
                continue
            mask = cell_of[lab] == i
            if not mask.any():
                print("trống:", nm)
                continue
            px = rgba.copy()
            px[..., 3] = np.where(mask, px[..., 3], 0)
            ys, xs = np.nonzero(mask)
            pad = 6
            box = (max(0, xs.min() - pad), max(0, ys.min() - pad), min(sheet.width, xs.max() + 1 + pad), min(sheet.height, ys.max() + 1 + pad))
            im = Image.fromarray(px, "RGBA").crop(box)
            s = mx / max(im.size)
            if s < 1:
                im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
            im.save(OUT / (nm + ".png"))
            made.append((nm, im))
            print(nm, im.size)
    if "--soi" in sys.argv:
        out = sys.argv[sys.argv.index("--soi") + 1]
        cell = 280
        cols = 6
        rows = (len(made) + cols - 1) // cols
        soi = Image.new("RGBA", (cols * cell, rows * cell), (60, 52, 80, 255))
        for i, (nm, im) in enumerate(made):
            t = im.copy()
            t.thumbnail((cell - 20, cell - 20))
            soi.alpha_composite(t, ((i % cols) * cell + (cell - t.width) // 2, (i // cols) * cell + (cell - t.height) // 2))
        soi.save(out)


if __name__ == "__main__":
    main()
