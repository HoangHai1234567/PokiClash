# Dựng ảnh mẫu đính cho GPT từ hình trận aola (người dùng cho đính, 2026-11-02):
#   refs/style/style_sheet.png   1536 x 1024: 8 tướng aola (khung đứng đầu), mẫu nét và cách dựng tay chân
#   refs/style/parts_example.png 1536 x 1024: bộ mảnh tháo rời của 2 tướng aola (hai chân, bốn chân), mẫu cách tách mảnh
# Nguồn: E:/ProjectAtomik/aola/reskin/goc_<id>/export (portrait.png, anim.json). Chạy: py -3 -I ArtGen/Heroes/tools/make_refs.py
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import explode  # noqa: E402

AOLA = "E:/ProjectAtomik/aola/reskin/"
OUT = os.path.join(os.path.dirname(HERE), "refs", "style")
STYLE = ["goc_713", "goc_714", "goc_715", "goc_5", "goc_205", "goc_1176", "goc_1831", "goc_182"]  # 3 con rùa người dùng đưa + 5 con khác
PARTS = [("goc_7", 0.55), ("goc_5", 0.5)]  # hai chân (bắp tay, cẳng tay tách) và bốn chân (chân chia khúc)


def style_sheet():
    W, H, cols = 1536, 1024, 4
    cw, ch = W // cols, H // 2
    sheet = Image.new("RGB", (W, H), (255, 255, 255))
    for i, n in enumerate(STYLE):
        im = Image.open(AOLA + n + "/export/portrait.png").convert("RGBA")
        im.thumbnail((cw - 16, ch - 16), Image.LANCZOS)
        x = (i % cols) * cw + (cw - im.width) // 2
        y = (i // cols) * ch + (ch - im.height) // 2
        sheet.paste(im, (x, y), im)
    p = os.path.join(OUT, "style_sheet.png")
    sheet.save(p)
    return p


def parts_example():
    W, H = 1536, 1024
    sheet = Image.new("RGB", (W, H), (255, 255, 255))
    for i, (n, k) in enumerate(PARTS):
        tmp = os.path.join(OUT, f"_tmp_{n}.png")
        explode.explode(n, k, tmp, W // 2, H)
        im = Image.open(tmp).convert("RGB")
        sheet.paste(im, (i * W // 2, 0))
        os.remove(tmp)
    p = os.path.join(OUT, "parts_example.png")
    sheet.save(p)
    return p


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(style_sheet())
    print(parts_example())
