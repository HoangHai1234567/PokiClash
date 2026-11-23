# Tách 5 quả trứng capsule từ tờ gen (nền trắng, một hàng, trái → phải: Thường, Khá, Hiếm, Sử thi, Huyền thoại) thành
# Assets/03 Art/Shop/trung_<bậc>.png (nền trong, cắt sát + lề), kèm trung.json: tỉ lệ đường nối vòm / thân tính từ trên xuống
# (hoạt ảnh nở tách vòm bay lên theo đường này).
# Chạy: py -3 -I ArtGen/Shop/cat_trung.py [tờ nguồn] (mặc định ArtGen/Shop/trung/trung_b.png)
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "trung", "trung_b.png")
OUT = os.path.join(ROOT, "Assets", "03 Art", "Shop")
PAD = 6


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    im = Image.open(SRC).convert("RGBA")
    w, h = im.size
    px = im.load()

    # nền: loang từ mép qua các điểm gần trắng (giữ lòng vòm nhạt vì có viền nâu bao kín)
    def whiteish(c):
        return c[0] > 228 and c[1] > 228 and c[2] > 228

    bg = bytearray(w * h)
    if px[0, 0][3] < 100:
        # tờ đã có nền trong (GPT 2.6 hay trả vậy): nền là điểm gần trong suốt
        for y in range(h):
            for x in range(w):
                if px[x, y][3] < 100:
                    bg[y * w + x] = 1
    stack = [] if px[0, 0][3] < 100 else [(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] + [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)]
    while stack:
        x, y = stack.pop()
        i = y * w + x
        if bg[i] or not whiteish(px[x, y]):
            continue
        bg[i] = 1
        if x > 0: stack.append((x - 1, y))
        if x < w - 1: stack.append((x + 1, y))
        if y > 0: stack.append((x, y - 1))
        if y < h - 1: stack.append((x, y + 1))

    # cột có nét (không phải nền) để chia 5 quả theo khoảng trống dọc
    cols = [any(not bg[y * w + x] for y in range(h)) for x in range(w)]
    spans, x = [], 0
    while x < w:
        if cols[x]:
            s = x
            while x < w and cols[x]:
                x += 1
            if x - s > 40:
                spans.append((s, x))
        x += 1
    if len(spans) != 5:
        raise SystemExit(f"tách được {len(spans)} cụm, cần 5: {spans}")

    os.makedirs(OUT, exist_ok=True)
    meta = {}
    for tier, (x0, x1) in enumerate(spans):
        ys = [y for y in range(h) if any(not bg[y * w + x] for x in range(x0, x1))]
        y0, y1 = min(ys), max(ys) + 1
        cx0, cy0, cx1, cy1 = max(0, x0 - PAD), max(0, y0 - PAD), min(w, x1 + PAD), min(h, y1 + PAD)
        out = Image.new("RGBA", (cx1 - cx0, cy1 - cy0), (0, 0, 0, 0))
        op = out.load()
        for y in range(cy0, cy1):
            for x in range(cx0, cx1):
                if not bg[y * w + x]:
                    op[x - cx0, y - cy0] = px[x, y]
        # mép nền còn sót điểm trắng xám sát viền: làm mờ dần những điểm sáng tiếp giáp nền
        for y in range(1, out.size[1] - 1):
            for x in range(1, out.size[0] - 1):
                c = op[x, y]
                if 0 < c[3] and min(c[:3]) > 205:
                    near = any(op[x + dx, y + dy][3] == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                    if near:
                        op[x, y] = (c[0], c[1], c[2], 90)
        # đường nối: hàng có vệt nâu sẫm ngang dài nhất trong khoảng 35–75% chiều cao (viền trên của dải nối)
        ow, oh = out.size
        best, best_y = -1, oh // 2
        for y in range(int(oh * 0.35), int(oh * 0.75)):
            run = cur = 0
            for x in range(ow):
                c = op[x, y]
                dark = c[3] > 0 and c[0] < 110 and c[1] < 90 and c[2] < 80
                cur = cur + 1 if dark else 0
                run = max(run, cur)
            if run > best:
                best, best_y = run, y
        path = os.path.join(OUT, f"trung_{tier}.png")
        out.save(path)
        meta[str(tier)] = {"w": ow, "h": oh, "seam": round(best_y / oh, 4)}
        print(f"bậc {tier}: {ow}x{oh}, đường nối {best_y}/{oh} = {best_y / oh:.3f} → {path}")
    with open(os.path.join(HERE, "trung", "trung.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
