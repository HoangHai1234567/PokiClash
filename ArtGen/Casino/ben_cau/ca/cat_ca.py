# Cắt hình 35 con cá (30 loài + 5 Cá Vua) từ 5 tờ Magnific GPT 2.6 (mỗi hệ một tờ 7 con, nền hồng #FF3AD0, xếp 4 trên + 3 dưới theo thứ tự
# độ hiếm: Thường, Thường, Ít gặp, Hiếm, Sử thi, Huyền thoại, Cá Vua). GD_Claude/32 (hình cá thật thay chấm màu).
# - Tách nền: độ khác màu với nền → alpha mềm; khử hồng ở mép (bỏ phần nền trộn vào màu).
# - Gán loài theo vị trí: thành phần lớn sắp theo hàng (y tâm) rồi theo x; thứ tự id lấy từ balance.json (casino.fishing.fish theo hệ,
#   rồi kings).
# - Tối ưu dung lượng: cạnh dài 256 px (Cá Vua 320), PNG tối ưu; Unity nén ASTC (CasinoFishingMenu đặt maxTextureSize 256 / 512).
# Ra: Assets/03 Art/Casino/BenCau/Ca/<id>.png, xem_ca.png (soát). Chạy: py -3 -I cat_ca.py
import os, sys, json
import numpy as np
import cv2
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.join(ROOT, "Assets", "03 Art", "Casino", "BenCau", "Ca")
os.makedirs(OUT, exist_ok=True)
SHEETS = {"thuy": "to_thuy.png", "kim": "to_kim.png", "moc": "to_moc.png", "hoa": "to_hoa.png", "tho": "to_tho.png"}
MAXS, MAXS_KING = 256, 320


def species():
    d = json.load(open(os.path.join(ROOT, "Assets", "02 Data", "Json", "balance.json"), encoding="utf-8"))["casino"]["fishing"]
    out = {}
    for e in SHEETS:
        ids = [f["id"] for f in d["fish"] if f["elem"] == e]
        kings = [f["id"] for f in d["kings"] if f["elem"] == e]
        out[e] = ids + kings
    return out


def cut(sheet, ids):
    src = Image.open(os.path.join(HERE, sheet))
    a = np.asarray(src.convert("RGB")).astype(np.float32)
    h, w, _ = a.shape
    transparent = src.mode == "RGBA" and np.asarray(src)[..., 3][:8, :8].mean() < 20
    if transparent:   # Magnific có lúc trả nền trong suốt dù prompt xin nền hồng: dùng thẳng alpha
        alpha = np.asarray(src)[..., 3].astype(np.float32) / 255.0
        alpha = np.where(alpha > 0.9, 1.0, np.clip((alpha - 0.15) / 0.75, 0, 1))
        bg = None
    else:
        bg = np.median(np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)]), axis=0)
        dist = np.abs(a - bg).sum(-1)
        alpha = np.clip((dist - 40) / 90, 0, 1)
    solid = alpha > 0.5
    solid = cv2.morphologyEx(solid.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
    n, lab, st, cen = cv2.connectedComponentsWithStats(solid.astype(np.uint8), connectivity=8)
    big = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 2500]
    # ghép mảnh rời gần một con lớn (râu, vây tách) vào con gần nhất
    small = [i for i in range(1, n) if 60 < st[i, cv2.CC_STAT_AREA] <= 2500]
    owner = {i: i for i in big}
    for i in small:
        cx, cy = cen[i]
        j = min(big, key=lambda b: (cen[b][0] - cx) ** 2 + (cen[b][1] - cy) ** 2)
        owner[i] = j
    rows = sorted(big, key=lambda i: cen[i][1])
    top = sorted([i for i in rows if cen[i][1] < h / 2], key=lambda i: cen[i][0])
    bot = sorted([i for i in rows if cen[i][1] >= h / 2], key=lambda i: cen[i][0])
    order = top + bot
    if len(order) != len(ids):
        print(f"  {sheet}: {len(order)} con, cần {len(ids)}: kiểm tờ")
    res = []
    for k, i in enumerate(order[:len(ids)]):
        m = np.isin(lab, [j for j, o in owner.items() if o == i])
        m = cv2.dilate(m.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
        ys, xs = np.nonzero(m)
        y0, y1, x0, x1 = max(0, ys.min() - 2), min(h, ys.max() + 3), max(0, xs.min() - 2), min(w, xs.max() + 3)
        al = (alpha * m)[y0:y1, x0:x1]
        rgb = a[y0:y1, x0:x1]
        # khử hồng: màu = (màu - (1 - a) * nền) / a
        if bg is not None:
            aa = np.maximum(al, 1e-3)[..., None]
            rgb = np.clip((rgb - (1 - aa) * bg) / aa, 0, 255)
        rgba = np.dstack([rgb, al * 255]).astype(np.uint8)
        im = Image.fromarray(rgba, "RGBA")
        lim = MAXS_KING if ids[k].startswith("vua_") else MAXS
        s = min(1.0, lim / max(im.size))
        im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
        # nhẹ file: ảnh 8 bit 160 màu (kèm alpha), nét chì màu vẫn giữ; Unity nén ASTC khi build
        im.quantize(colors=160, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(os.path.join(OUT, ids[k] + ".png"), optimize=True)
        res.append((ids[k], im))
    return res


def main():
    sp = species()
    allims = []
    for e, sheet in SHEETS.items():
        if not os.path.exists(os.path.join(HERE, sheet)):
            print("chưa có", sheet)
            continue
        r = cut(sheet, sp[e])
        allims += r
        print(e, ", ".join(f"{i} {im.size[0]}x{im.size[1]}" for i, im in r))
    # tờ soát
    cell = 200
    cols = 7
    rows = (len(allims) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell, rows * cell), (90, 170, 220, 255))
    for k, (i, im) in enumerate(allims):
        t = im.copy()
        t.thumbnail((cell - 10, cell - 10))
        sheet.alpha_composite(t, ((k % cols) * cell + (cell - t.width) // 2, (k // cols) * cell + (cell - t.height) // 2))
    sheet.save(os.path.join(HERE, "xem_ca.png"))
    tot = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT) if f.endswith(".png"))
    print(f"{len(allims)} con, tổng {tot / 1024:.0f} KB")


if __name__ == "__main__":
    main()
