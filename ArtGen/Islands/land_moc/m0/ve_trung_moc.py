# Hình easter egg riêng của đảo Mộc (2026-11-19), dùng lại hàm vẽ của ArtGen/Islands/land_thuy/m0/ve_trung.py:
# - trung_ghi_moc_<k>.png: ghi chú bút chì ở mép vùng k (phông Pangolin của game);
# - trung_buom.png: bướm (cánh trắng viền mực để game nhuộm nhiều màu; cánh trên to, cánh dưới nhỏ, thân, râu);
# - trung_la.png: lá rơi (trắng viền mực, gân giữa, cuống) để game nhuộm cam / đỏ / xanh theo vùng.
# Xuất vào Assets/03 Art/Islands/Co. Chạy: py -3 -I ve_trung_moc.py
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
THUY = os.path.abspath(os.path.join(HERE, "..", "..", "land_thuy", "m0"))
sys.path.insert(0, THUY)
import ve_trung  # noqa: E402
from ve_co import INK, M, OUT, finish, outline, px, shape  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

NOTES = {
    1: ("Thơm quá!", "sao"),
    2: ("Nấm… ăn được?", "?"),
    3: ("Dây leo chặn lối!", "!"),
    4: ("Gió hú…", "mui_ten"),
    5: ("Lá đỏ rơi mãi…", "sao"),
    6: ("Vuốt rồng?!", "!"),
    7: ("Ai múa gậy?", "?"),
    8: ("Pha lê!", "sao"),
    9: ("Cây thần…", "vuong_mien"),
}


def butterfly():
    """bướm: mỗi bên hai cánh elip nghiêng (trên to, dưới nhỏ), thân bầu, hai râu cong; cánh trắng để nhuộm"""
    W, H = 64.0, 52.0
    img = Image.new("RGBA", (px(W + 2 * M), px(H + 2 * M)), (0, 0, 0, 0))
    cx, cy = M + W / 2, M + H / 2 + 3

    def ell(ex, ey, rx, ry, ang):
        a0 = math.radians(ang)
        return [(px(ex + rx * math.cos(t) * math.cos(a0) - ry * math.sin(t) * math.sin(a0)),
                 px(ey + rx * math.cos(t) * math.sin(a0) + ry * math.sin(t) * math.cos(a0))) for t in np.linspace(0, 2 * math.pi, 28, endpoint=False)]

    for side in (-1, 1):
        lay, _ = shape((255, 255, 255, 255), ell(cx + side * 14, cy - 9, 15, 11, -side * 28), img.size, 500 + side, line=2.8,
                       hatch_kw={"alpha": (8, 18)})
        img.alpha_composite(lay)
        lay, _ = shape((255, 255, 255, 255), ell(cx + side * 10, cy + 8, 10, 8, side * 30), img.size, 510 + side, line=2.8,
                       hatch_kw={"alpha": (8, 18)})
        img.alpha_composite(lay)
    body = ell(cx, cy, 3.2, 12, 0)
    ImageDraw.Draw(img).polygon(body, fill=INK)
    d = ImageDraw.Draw(img)
    for side in (-1, 1):
        outline(d, [(px(cx), px(cy - 11)), (px(cx + side * 4), px(cy - 18)), (px(cx + side * 9), px(cy - 22))], 1.6, closed=False)
        r = 1.6
        d.ellipse([px(cx + side * 9 - r), px(cy - 22 - r), px(cx + side * 9 + r), px(cy - 22 + r)], fill=INK)
    return finish(img)


def leaf():
    """lá: đầu trên nhọn, gốc dưới tròn có cuống, gân giữa, hai cặp gân phụ; trắng để nhuộm"""
    W, H = 40.0, 56.0
    img = Image.new("RGBA", (px(W + 2 * M), px(H + 2 * M)), (0, 0, 0, 0))
    cx, top, bot = M + W / 2, M + 2, M + H - 10
    pts = []
    for t in np.linspace(0, math.pi, 22):
        y = top + (bot - top) * (1 - math.cos(t)) / 2
        w = math.sin(t) ** 1.25 * (W / 2 - 3) * (0.82 + 0.3 * (1 - math.cos(t)) / 2)
        pts.append((px(cx + w), px(y)))
    for t in np.linspace(math.pi, 0, 22)[1:-1]:
        y = top + (bot - top) * (1 - math.cos(t)) / 2
        w = math.sin(t) ** 1.25 * (W / 2 - 3) * (0.82 + 0.3 * (1 - math.cos(t)) / 2)
        pts.append((px(cx - w), px(y)))
    lay, _ = shape((255, 255, 255, 255), pts, img.size, 530, line=2.8, hatch_kw={"alpha": (8, 18)})
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    outline(d, [(px(cx), px(top + 6)), (px(cx + 0.6), px(bot)), (px(cx + 2.5), px(bot + 7))], 2.0, closed=False)
    for f in (0.38, 0.62):
        y = top + (bot - top) * f
        for side in (-1, 1):
            outline(d, [(px(cx), px(y + 4)), (px(cx + side * 9), px(y - 3))], 1.4, closed=False)
    return finish(img)


def main():
    os.makedirs(OUT, exist_ok=True)
    ve_trung.NOTES = NOTES
    for k in NOTES:
        im = ve_trung.note(k)
        im.save(os.path.join(OUT, f"trung_ghi_moc_{k}.png"))
        print(f"trung_ghi_moc_{k}", im.size)
    b = butterfly()
    b.save(os.path.join(OUT, "trung_buom.png"))
    print("trung_buom", b.size)
    lf = leaf()
    lf.save(os.path.join(OUT, "trung_la.png"))
    print("trung_la", lf.size)
    sheet = Image.new("RGBA", (1500, 520), (243, 233, 211, 255))
    x, y = 10, 10
    for k in NOTES:
        im = Image.open(os.path.join(OUT, f"trung_ghi_moc_{k}.png"))
        im = im.resize((im.width // 2, im.height // 2))
        if x + im.width > 1490:
            x, y = 10, y + 120
        sheet.alpha_composite(im, (x, y))
        x += im.width + 10
    bb = b.resize((b.width * 2, b.height * 2))
    sheet.alpha_composite(bb, (1300, 360))
    sheet.alpha_composite(lf.resize((lf.width * 2, lf.height * 2)), (1150, 360))
    sheet.convert("RGB").save(os.path.join(HERE, "..", "m1", "soi_trung_moc.png") if os.path.isdir(os.path.join(HERE, "..", "m1")) else os.path.join(HERE, "soi_trung_moc.png"))
    print("ok")


if __name__ == "__main__":
    main()
