# Hoa văn lát cho ô cột của popup chọn một gói / Hết bi (người dùng 2026-11-27: "cái hình splash đằng sau xấu quá, như bị stretch ra. Làm
# màu trơn rồi trang trí hoa văn nhẹ nhàng thôi (hoa văn có thể làm giống với cột trái trong shop)"): các mảnh hình vẽ tay của cột trái
# (hinh_cot/: sao, lấp lánh, quái nhỏ, bi, trứng, tim...) rải so le trên tấm trong suốt, nét trắng; mảnh sát mép vẽ lặp ở mép đối diện để lát
# liền hai chiều. Game tô màu + độ đục (OfferPopColumn.Plain), ô nền vẫn là o_nen tô màu trơn.
# Chạy: py -3 -I ArtGen/Shop/v3/ve_hoa_van.py [--assets]  → out/ hoặc Assets/03 Art/Shop/v3/hoa_van.png (256×320, lát).
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image  # noqa: E402

import ve_ui as v  # noqa: E402


def pattern(w=256, h=320):
    S = v.SS
    pieces = [(f, Image.open(os.path.join(v.DOODLE, f)).convert("RGBA")) for f in sorted(os.listdir(v.DOODLE)) if f.endswith(".png")]
    rnd = random.Random(301)
    order = pieces[:]
    rnd.shuffle(order)
    im = Image.new("RGBA", (w * S, h * S), (255, 255, 255, 0))
    # lưới so le 3 hàng x 2 cột (hàng lẻ lệch nửa ô), mỗi ô một mảnh, lệch + xoay ngẫu nhiên; thêm lấp lánh nhỏ
    rows, cols = 4, 2
    k = 0
    spots = []
    for r in range(rows):
        for c in range(cols):
            x = (c + 0.5 + (0.5 if r % 2 else 0)) * w / cols + rnd.uniform(-12, 12)
            y = (r + 0.5) * h / rows + rnd.uniform(-10, 10)
            spots.append((x % w, y, False))
    for _ in range(5):
        spots.append((rnd.uniform(0, w), rnd.uniform(0, h), True))
    small = [p for n, p in pieces if "sao_nho" in n or "lap_lanh" in n]
    big = [p for n, p in pieces if not ("sao_nho" in n or "lap_lanh" in n)]
    rnd.shuffle(big)
    for x, y, tiny in spots:
        p = rnd.choice(small) if tiny else big[k % len(big)]
        if not tiny:
            k += 1
        size = rnd.uniform(16, 24) if tiny else rnd.uniform(46, 60)
        sc = size / max(p.width, p.height)
        q = p.resize((max(1, int(p.width * sc * S)), max(1, int(p.height * sc * S))), Image.LANCZOS)
        q = q.rotate(rnd.uniform(-22, 22), resample=Image.BICUBIC, expand=True)
        white = Image.new("RGBA", q.size, (255, 255, 255, 255))
        white.putalpha(q.split()[3])
        layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
        for dx in (-w * S, 0, w * S):
            for dy in (-h * S, 0, h * S):
                layer.paste(white, (int(x * S - q.width / 2 + dx), int(y * S - q.height / 2 + dy)), white)
        im.alpha_composite(layer)
    v.finish(im, w, h, "hoa_van")


if __name__ == "__main__":
    pattern()
