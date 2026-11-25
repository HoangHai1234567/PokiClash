# Cắt mảnh Lão Mực (GD_Claude/31_LaoMuc_Dealer.md, mốc D1) từ ba ảnh gen không viền:
#   L1_goc_rig.png   thân toàn thân, mặt trống, nền xanh lơ #3AD0FF  -> manh/than.png
#   L2_mat_mieng.png 10 cặp mắt (2 hàng trên) + 10 miệng (2 hàng dưới), nền xanh lơ -> manh/mat_01..10.png, mieng_01..10.png
#   L3_ban_tay.png   10 bàn tay, nền trong suốt -> manh/tay_01..10.png
# rồi ghép thử vài biểu cảm lên mặt trống -> soi/D1_ghep_thu.png
# Chạy: py -3 -I cat_manh.py   (thư mục làm việc tuỳ ý; đường dẫn tính từ chỗ đặt script)
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "manh")
SOI = os.path.join(HERE, "soi")
os.makedirs(OUT, exist_ok=True)
os.makedirs(SOI, exist_ok=True)
CYAN = np.array([58, 208, 255], float)


def key_cyan(path, tol=70, soft=40):
    """Nền xanh lơ -> alpha (mềm ở mép), khử viền xanh còn sót (despill)."""
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    d = np.sqrt(((a - CYAN) ** 2).sum(2))
    al = np.clip((d - tol) / soft, 0, 1)
    # điểm mép còn ánh xanh: kéo kênh lam về không vượt kênh đỏ / lục nhiều
    rgb = a.copy()
    spill = (rgb[..., 2] > np.maximum(rgb[..., 0], rgb[..., 1]) + 30) & (al < 1)
    rgb[spill, 2] = np.maximum(rgb[spill, 0], rgb[spill, 1])
    # bỏ cụm nhỏ lạc
    n, lab, st, _ = cv2.connectedComponentsWithStats((al > 0.5).astype(np.uint8), 8)
    keep = np.isin(lab, [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] >= 60]).astype(np.uint8)
    al = al * (cv2.dilate(keep, np.ones((5, 5), np.uint8)) > 0)
    out = np.dstack([rgb, al * 255]).clip(0, 255).astype(np.uint8)
    return out


def crop(rgba, pad=4):
    al = rgba[..., 3]
    ys, xs = np.where(al > 8)
    y0, y1, x0, x1 = max(0, ys.min() - pad), min(al.shape[0], ys.max() + pad + 1), max(0, xs.min() - pad), min(al.shape[1], xs.max() + pad + 1)
    return rgba[y0:y1, x0:x1], (x0, y0)


def grid_items(rgba, rows, cols, gap=18):
    """Gom cụm theo ô lưới: mỗi ô (hàng, cột) một món (cặp mắt có thể là 2 cụm)."""
    al = rgba[..., 3] > 40
    k = 2 * gap + 1
    big = cv2.dilate(al.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(big, 8)
    cents = []
    for i in range(1, n):
        m = (lab == i) & al
        if m.sum() < 300:
            continue
        x, y, w, h = st[i, :4]
        cents.append((y + h / 2, x + w / 2, i, None))
    cents.sort(key=lambda c: c[0])
    # chia hàng theo khoảng y
    out = []
    per = len(cents) // rows if len(cents) % rows == 0 else None
    if per is None or per != cols:
        raise SystemExit(f"đếm sai: {len(cents)} cụm, cần {rows * cols}")
    for r in range(rows):
        row = sorted(cents[r * cols:(r + 1) * cols], key=lambda c: c[1])
        for cy, cx, idx, sl in row:
            m = (lab == idx)
            item = rgba.copy()
            item[..., 3] = (item[..., 3] * m).astype(np.uint8)
            out.append(crop(item))
    return out


def main():
    # thân
    than = key_cyan(os.path.join(HERE, "L1_goc_rig.png"))
    t, off = crop(than)
    Image.fromarray(t).save(os.path.join(OUT, "than.png"))
    print("than.png", t.shape[1], "x", t.shape[0], "lệch", off)
    # mắt, miệng
    fm = key_cyan(os.path.join(HERE, "L2_mat_mieng.png"))
    items = grid_items(fm, 4, 5)
    for i, (img, o) in enumerate(items):
        name = f"mat_{i + 1:02d}.png" if i < 10 else f"mieng_{i - 9:02d}.png"
        Image.fromarray(img).save(os.path.join(OUT, name))
    print("mắt, miệng:", len(items))
    # bàn tay (nền trong suốt sẵn)
    hs = np.asarray(Image.open(os.path.join(HERE, "L3_ban_tay.png")).convert("RGBA")).copy()
    hands = grid_items(hs, 2, 5, gap=10)
    for i, (img, o) in enumerate(hands):
        Image.fromarray(img).save(os.path.join(OUT, f"tay_{i + 1:02d}.png"))
    print("bàn tay:", len(hands))
    ghep_thu(t)


def ghep_thu(than):
    """Ghép thử 6 biểu cảm lên mặt trống (chỗ mặt đo trên thân: tâm đầu, bề ngang đầu)."""
    al = than[..., 3] > 128
    H, W = al.shape
    # đầu: phần thân màu đen phía trên nơ; đo bề ngang lớn nhất trong 15–35 % chiều cao
    dark = al & (than[..., :3].mean(2) < 90)
    band = range(int(H * 0.15), int(H * 0.36))
    best = max(band, key=lambda y: dark[y].sum())
    xs = np.where(dark[best])[0]
    cx, hw = (xs.min() + xs.max()) / 2, xs.max() - xs.min()
    print("đầu: tâm x", round(cx), "rộng", hw, "ở y", best)
    combos = [("nhếch mép", 2, 1), ("cười đắc thắng", 6, 2), ("sốc", 5, 4), ("cáu", 9, 5), ("nháy mắt", 8, 7), ("xị mặt", 7, 6)]
    tiles = []
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 30)
    for label, e, m in combos:
        base = Image.fromarray(than).copy()
        eye = Image.open(os.path.join(OUT, f"mat_{e:02d}.png"))
        mo = Image.open(os.path.join(OUT, f"mieng_{m:02d}.png"))
        s_eye = (hw * 0.62) / eye.width if e not in (8,) else (hw * 0.62) / max(eye.width, 1)
        eye = eye.resize((int(eye.width * s_eye), int(eye.height * s_eye)), Image.LANCZOS)
        s_mo = (hw * 0.55) / max(mo.width, 1) if m not in (3,) else (hw * 0.22) / mo.width
        if m == 4:
            s_mo = (hw * 0.32) / mo.width
        mo = mo.resize((int(mo.width * s_mo), int(mo.height * s_mo)), Image.LANCZOS)
        ey = int(best - hw * 0.06)
        base.alpha_composite(eye, (int(cx - eye.width / 2 + hw * 0.04), int(ey - eye.height / 2)))
        my = int(best + hw * 0.21)
        base.alpha_composite(mo, (int(cx - mo.width / 2 + hw * 0.04), int(my - mo.height / 2)))
        crop_box = (0, 0, W, int(H * 0.62))
        tile = Image.new("RGBA", (W, int(H * 0.62) + 50), (246, 239, 225, 255))
        tile.alpha_composite(base.crop(crop_box), (0, 0))
        ImageDraw.Draw(tile).text((20, tile.height - 44), label, fill=(43, 32, 24), font=font)
        tiles.append(tile)
    tw, th = tiles[0].size
    sheet = Image.new("RGB", (tw * 3, th * 2), (246, 239, 225))
    for i, t in enumerate(tiles):
        sheet.paste(t.convert("RGB"), ((i % 3) * tw, (i // 3) * th))
    sheet = sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS)
    sheet.save(os.path.join(SOI, "D1_ghep_thu.png"))
    print("soi/D1_ghep_thu.png")


if __name__ == "__main__":
    main()
