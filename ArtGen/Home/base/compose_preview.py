# Ghép thử: đảo nền (base_dao_nen_3.png) + khối rừng 8 x 8 (forest_lot_A/B/C.png) đặt lên mọi ô rừng chưa mở lúc mới chơi.
# - Tách nền trắng của khối rừng (tô loang từ mép), lưu *_cut.png để đưa vào Unity.
# - Hình thoi đồng cỏ đo trên base_dao_nen_1.png (bản 3 là bản sửa của bản 1, giữ nguyên hình thoi): mũi trái (2,336), mũi phải
#   (1338,334), góc dưới (678,700) → góc trên suy ra (662,-30). Tỉ lệ thoi khoảng 1,85:1 (không đúng 2:1); trong Unity kéo ngang nền
#   cho đúng 2:1.
# Ra: preview_rung.png. Chạy: py -3 -I compose_preview.py [lots khoảnh đầu thêm, dạng i,j i,j ...]
import os, sys, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
cfg = json.load(open(os.path.join(ROOT, "Assets", "02 Data", "Json", "balance.json"), encoding="utf-8"))["home"]
GRID, LOT = cfg["grid"], cfg["lot"]
N = GRID // LOT

LEFT, RIGHT, BOTTOM = (2, 336), (1338, 334), (678, 700)
TOP = (LEFT[0] + RIGHT[0] - BOTTOM[0], LEFT[1] + RIGHT[1] - BOTTOM[1])
U = ((RIGHT[0] - TOP[0]) / GRID, (RIGHT[1] - TOP[1]) / GRID)  # một ô theo gx
V = ((LEFT[0] - TOP[0]) / GRID, (LEFT[1] - TOP[1]) / GRID)  # một ô theo gy


def P(gx, gy):
    return (TOP[0] + gx * U[0] + gy * V[0], TOP[1] + gx * U[1] + gy * V[1])


def cut(fn):
    """Tách nền trắng bằng tô loang từ mép; trả ảnh RGBA đã cắt sát và toạ độ góc dưới, bề ngang chân thoi."""
    im = Image.open(os.path.join(HERE, fn)).convert("RGB")
    w, h = im.size
    key = (255, 0, 255)
    work = im.copy()
    for xy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (0, h // 2), (w - 1, h // 2)]:
        if sum(work.getpixel(xy)) > 690:
            ImageDraw.floodfill(work, xy, key, thresh=45)
    px = work.load()
    out = Image.new("RGBA", (w, h))
    op = out.load()
    src = im.load()
    for y in range(h):
        for x in range(w):
            if px[x, y] != key:
                op[x, y] = src[x, y] + (255,)
    bbox = out.getbbox()
    out = out.crop(bbox)
    a = out.split()[3]
    ow, oh = out.size
    # góc dưới: điểm đặc thấp nhất; bề ngang chân thoi: điểm trái nhất, phải nhất ở 40% dưới cùng
    al = a.load()
    bottom = max((y for y in range(oh) for x in range(0, ow, 3) if al[x, y] > 0), default=oh - 1)
    xs = [x for x in range(ow) if al[x, bottom] > 0]
    bx = sum(xs) / len(xs)
    lo = [x for y in range(int(oh * 0.6), oh) for x in range(ow) if al[x, y] > 0]
    width = max(lo) - min(lo)
    out.save(os.path.join(HERE, fn.replace(".png", "_cut.png")))
    return out, (bx, bottom), width


def main():
    base = Image.open(os.path.join(HERE, "base_dao_nen_3.png")).convert("RGBA")
    forests = [cut(f) for f in ["forest_lot_A.png", "forest_lot_B.png", "forest_lot_C.png"]]
    open_lots = {(l[0], l[1]) for l in cfg["startLots"]}
    for a in sys.argv[1:]:
        i, j = a.split(",")
        open_lots.add((int(i), int(j)))
    hills = {(l["i"], l["j"]) for l in cfg["lots"] if l["kind"] == "hill"}
    lot_w = LOT * (U[0] - V[0])
    lots = [(i, j) for i in range(N) for j in range(N) if (i, j) not in open_lots and (i, j) not in hills]
    for i, j in sorted(lots, key=lambda t: (t[0] + t[1], t[0])):
        k = int(hashlib.md5(f"{i},{j}".encode()).hexdigest(), 16)
        spr, (bx, by), w = forests[k % 3]
        flip = (k >> 3) & 1
        s = lot_w / w * 1.13  # chồng lên nhau để cây khối trước che viền cỏ khối sau
        img = spr.resize((max(1, int(spr.width * s)), max(1, int(spr.height * s))), Image.LANCZOS)
        if flip:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            bx = spr.width - bx
        gb = P((i + 1) * LOT, (j + 1) * LOT)  # góc dưới của ô rừng
        base.alpha_composite(img, (int(gb[0] - bx * s), int(gb[1] - by * s + 2)))
    base.save(os.path.join(HERE, "preview_rung.png"))
    print("ok", len(lots), "ô rừng, ô lưới", U, V)


if __name__ == "__main__":
    main()
