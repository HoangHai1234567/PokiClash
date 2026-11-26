# -*- coding: utf-8 -*-
"""Dựng mặt thẻ mẫu (PIL, cỡ thật 320 x 464 như prefab The) để duyệt tranh thẻ chung trước khi đưa vào Unity.

    py -3 -I ArtGen/Cards/xem_the.py 1     # ArtGen/Cards/xem/luot_01.png

Hàng trên: 3 thẻ đầu kiểu CŨ (icon trong ô tròn). Dưới: các thẻ của lượt theo bố cục MỚI (ô tranh 280 x 175, viền mực, băng keo).
Chỉ là mô phỏng gần đúng (màu, phông của game) để xem tranh đọc được ở cỡ thẻ; bố cục thật làm trong prefab.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
ASSETS = os.path.join(ROOT, "Assets")
FONT_B = os.path.join(ASSETS, "03 Art", "Fonts", "Baloo2-ExtraBold.ttf")
FONT_M = os.path.join(ASSETS, "03 Art", "Fonts", "Baloo2-Bold.ttf")
ICONS = os.path.join(ASSETS, "03 Art", "Fallback", "Icons")
PER = 9
CW, CH = 320, 464
INK, INK2, FILL = (43, 33, 24), (90, 70, 54), (255, 250, 240)
RAR = {"common": ((185, 177, 163), "THƯỜNG"), "uncommon": ((108, 191, 79), "KHÁ"), "rare": ((74, 144, 217), "HIẾM"),
       "epic": ((154, 106, 214), "SỬ THI"), "legend": ((243, 154, 45), "HUYỀN THOẠI")}
TAPE = (255, 236, 170, 200)


def font(p, s):
    return ImageFont.truetype(p, s)


def wrap(d, text, f, wmax):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= wmax:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def the(card, desc, art=None, icon=None):
    im = Image.new("RGBA", (CW + 20, CH + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ox, oy = 10, 20
    rc, rname = RAR[card["rarity"]]
    d.rounded_rectangle((ox, oy, ox + CW, oy + CH), 18, fill=FILL, outline=INK, width=4)
    # dải độ hiếm + tên
    d.rounded_rectangle((ox + 4, oy + 4, ox + CW - 4, oy + 74), 14, fill=rc)
    d.rectangle((ox + 4, oy + 40, ox + CW - 4, oy + 74), fill=rc)
    d.line((ox + 4, oy + 74, ox + CW - 4, oy + 74), fill=INK, width=3)
    fb = font(FONT_B, 32)
    d.text((ox + CW / 2, oy + 42), card["name"], font=fb, fill="white", anchor="mm", stroke_width=4, stroke_fill=INK)
    if art is not None:
        ax0, ay0 = ox + 20, oy + 90
        a = art.resize((280, 175), Image.LANCZOS)
        im.paste(a, (ax0, ay0))
        d.rectangle((ax0 - 2, ay0 - 2, ax0 + 281, ay0 + 176), outline=INK, width=4)
        desc_top = oy + 278
    else:
        cx, cy, r = ox + CW / 2, oy + 92 + 78, 78
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=tuple(int(c * 0.35 + 255 * 0.65) for c in rc))
        if icon is not None:
            ic = icon.resize((128, 128), Image.LANCZOS)
            im.alpha_composite(ic, (int(cx - 64), int(cy - 64)))
        desc_top = oy + 268
    # băng keo
    tape = Image.new("RGBA", (92, 28), TAPE)
    tape = tape.rotate(-4, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(tape, (int(ox + CW / 2 - tape.width / 2), oy - 14))
    fm = font(FONT_M, 24)
    lines = wrap(d, desc, fm, CW - 44)
    y = desc_top + (110 - len(lines) * 30) / 2
    for ln in lines:
        d.text((ox + CW / 2, y + 15), ln, font=fm, fill=INK, anchor="mm")
        y += 30
    fr = font(FONT_M, 18)
    d.text((ox + CW / 2, oy + CH - 26), "•  " + rname, font=fr, fill=INK2, anchor="mm")
    d.ellipse((ox + CW / 2 - d.textlength("•  " + rname, font=fr) / 2 - 2, oy + CH - 31,
               ox + CW / 2 - d.textlength("•  " + rname, font=fr) / 2 + 8, oy + CH - 21), fill=rc)
    return im


def main(argv):
    n = int(argv[0])
    data = json.load(open(os.path.join(HERE, "canh_the_chung.json"), encoding="utf-8"))["cards"]
    pool = {c["id"]: c for c in json.load(open(os.path.join(ASSETS, "02 Data", "Json", "cards.json"), encoding="utf-8"))["pool"]}
    txt = {c["id"]: c["lv1"] for c in json.load(open(os.path.join(ASSETS, "02 Data", "Golden", "cardtext.json"), encoding="utf-8"))["cards"]}
    cards = [pool[c["id"]] for c in data[(n - 1) * PER: n * PER]]
    cols = 3
    gap = 24
    tw, th = CW + 20, CH + 30
    rows_new = (len(cards) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * gap, (rows_new + 1) * th + (rows_new + 3) * gap + 40), (243, 235, 214))
    d = ImageDraw.Draw(sheet)
    fl = font(FONT_B, 26)
    d.text((gap, gap), "Cũ: icon trong ô tròn", font=fl, fill=INK)
    for i, c in enumerate(cards[:3]):
        p = os.path.join(ICONS, c["icon"] + ".png")
        ic = Image.open(p).convert("RGBA") if os.path.exists(p) else None
        sheet.paste(t := the(c, txt[c["id"]], icon=ic), (gap + i * (tw + gap), gap + 30), t)
    y0 = gap * 2 + 30 + th
    d.text((gap, y0), f"Mới: tranh GPT lượt {n}", font=fl, fill=INK)
    for i, c in enumerate(cards):
        r, k = divmod(i, cols)
        art = Image.open(os.path.join(HERE, "cat", c["id"] + ".png")).convert("RGB")
        t = the(c, txt[c["id"]], art=art)
        sheet.paste(t, (gap + k * (tw + gap), y0 + 30 + r * (th + gap)), t)
    os.makedirs(os.path.join(HERE, "xem"), exist_ok=True)
    out = os.path.join(HERE, "xem", f"luot_{n:02d}.png")
    sheet.save(out, optimize=True)
    print(out, sheet.size)


if __name__ == "__main__":
    main(sys.argv[1:])
