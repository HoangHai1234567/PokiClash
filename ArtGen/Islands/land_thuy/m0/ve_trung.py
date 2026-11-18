# Hình cho easter egg vùng boss chưa mở của đảo vùng đất (người dùng 2026-11-18: "làm 1 vài easter egg cho các zone khi bị khóa để kích
# thích tò mò người chơi", rồi "làm cả 6"). Cùng nét với cờ (ve_co.py): viền mực nâu hơi rung, tô phẳng, không bóng.
# - (mắt boss trong mây đã bỏ 2026-11-18, thay bằng boss tung tuyệt kỹ; hàm eyes() giữ lại để tham khảo)
# - trung_set.png: tia sét (đền Giông Mưa: sét chớp trong mây); trung_bong.png: bong bóng; trung_tuyet.png: bông tuyết;
#   trung_nuoc.png: cột nước cá voi phun;
# - trung_ghi_<k>.png: ghi chú bút chì người vẽ bản đồ để lại ở mép vùng k (chữ phông Pangolin của game, màu chì, kèm hình nguệch ngoạc).
# Xuất vào Assets/03 Art/Islands/Co; tờ soi m1/soi_trung.png. Chạy: py -3 -I ve_trung.py
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # chạy py -I: tự thêm thư mục script
from ve_co import INK, M, OUT, R, SS, finish, outline, px, shape  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
FONT = os.path.join(ROOT, "Assets", "03 Art", "Fonts", "Pangolin-Regular.ttf")
SOI = os.path.join(HERE, "..", "m1", "soi_trung.png")
GRAPHITE = (66, 56, 48)

# ghi chú từng vùng (đảo Thủy): chữ, hình nguệch ngoạc kèm theo
NOTES = {
    1: ("ộp ộp…?", "?"),
    2: ("Ai thắp đèn?", "mui_ten"),
    3: ("Ngọc trai!?", "sao"),
    4: ("Xác tàu cũ", "mui_ten"),
    5: ("Đừng vào khi mưa!", "set"),
    6: ("Xương… to quá!", "!"),
    7: ("Nấm phát sáng?!", "sao"),
    8: ("Lạnh buốt…", "tuyet"),
    9: ("Hang rồng?", "vuong_mien"),
}


def canvas(w, h):
    return Image.new("RGBA", (px(w + 2 * M), px(h + 2 * M)), (0, 0, 0, 0))


def eyes():
    W, H = 132.0, 58.0
    img = canvas(W, H)
    for side in (-1, 1):
        cx, cy = M + W / 2 + side * 33, M + H / 2 + 6
        ew, eh = 21.0, 11.5
        # mắt hình hạnh nhân, đuôi mắt xếch lên phía ngoài (vẻ dữ)
        pts = []
        for a in np.linspace(0, 2 * math.pi, 36, endpoint=False):
            x = math.cos(a) * ew
            y = math.sin(a) * eh * (0.55 + 0.45 * abs(math.sin(a)))
            y -= side * x * 0.18
            pts.append((px(cx + x), px(cy + y)))
        lay, _ = shape((255, 236, 140, 255), pts, img.size, 400 + side, line=3.4, hatch_kw={"alpha": (10, 22)})
        img.alpha_composite(lay)
        pup = [(px(cx + math.cos(a) * 3.6), px(cy + math.sin(a) * 9.5)) for a in np.linspace(0, 2 * math.pi, 20, endpoint=False)]
        d = ImageDraw.Draw(img)
        d.polygon(pup, fill=INK)
        # mày chau
        outline(d, [(px(cx - side * 22), px(cy - 19)), (px(cx + side * 16), px(cy - 12))], 3.4, closed=False)
    return finish(img)


def bolt():
    W, H = 70.0, 150.0
    img = canvas(W, H)
    pts = [(28, 0), (60, 0), (40, 58), (66, 58), (12, 150), (26, 84), (2, 84)]
    poly = [(px(M + x), px(M + y)) for x, y in pts]
    lay, _ = shape((255, 240, 120, 255), poly, img.size, 410, line=3.6, hatch_kw={"alpha": (10, 24)})
    img.alpha_composite(lay)
    return finish(img)


def bubble():
    W = H = 34.0
    img = canvas(W, H)
    cx, cy, r = M + 17, M + 17, 16
    circ = [(px(cx + r * math.cos(a)), px(cy + r * math.sin(a))) for a in np.linspace(0, 2 * math.pi, 32, endpoint=False)]
    lay, _ = shape((214, 240, 252, 150), circ, img.size, 420, line=2.4, hatch_kw={"alpha": (6, 14)})
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    arc = [(px(cx + 10 * math.cos(a)), px(cy + 10 * math.sin(a))) for a in np.linspace(math.radians(200), math.radians(260), 6)]
    outline(d, arc, 1.6, closed=False, col=(58, 40, 26, 160))
    return finish(img)


def snowflake():
    W = H = 44.0
    img = canvas(W, H)
    d = ImageDraw.Draw(img)
    cx, cy = M + 22, M + 22
    segs = []
    for i in range(6):
        a = i * math.pi / 3
        ux, uy = math.cos(a), math.sin(a)
        segs.append([(cx, cy), (cx + ux * 19, cy + uy * 19)])
        for t, ln in ((10, 6), (15, 4)):
            bx, by = cx + ux * t, cy + uy * t
            for s in (-1, 1):
                b = a + s * math.pi / 4
                segs.append([(bx, by), (bx + math.cos(b) * ln, by + math.sin(b) * ln)])
    for sg in segs:
        outline(d, [(px(x), px(y)) for x, y in sg], 4.6, closed=False)
    for sg in segs:
        outline(d, [(px(x), px(y)) for x, y in sg], 2.0, closed=False, col=(255, 255, 255, 255))
    return finish(img)


def spout():
    W, H = 96.0, 190.0
    img = canvas(W, H)
    cx = M + W / 2
    top = M + 26
    pts = [(cx - 12, M + H), (cx - 16, top + 60), (cx - 30, top + 18)]
    for i, a in enumerate(np.linspace(math.pi, 0, 9)):  # tán nước gợn
        rr = 40 + (6 if i % 2 else 0)
        pts.append((cx + rr * math.cos(a), top + 10 - 22 * math.sin(a)))
    pts += [(cx + 30, top + 18), (cx + 16, top + 60), (cx + 12, M + H)]
    lay, _ = shape((170, 225, 245, 255), [(px(x), px(y)) for x, y in pts], img.size, 430, line=3.6, hatch_kw={"alpha": (10, 22)})
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    for dx in (-5, 5):
        outline(d, [(px(cx + dx), px(top + 40)), (px(cx + dx * 0.6), px(M + H - 14))], 1.6, closed=False, col=(58, 40, 26, 140))
    for (x, y, r) in ((cx - 44, top + 40, 5), (cx + 46, top + 30, 4.5), (cx - 36, top + 70, 3.6), (cx + 38, top + 64, 3.6)):
        circ = [(px(x + r * math.cos(a)), px(y + r * math.sin(a))) for a in np.linspace(0, 2 * math.pi, 14, endpoint=False)]
        l2, _ = shape((170, 225, 245, 255), circ, img.size, int(x + y), line=2.2, hatch_kw={"alpha": (0, 1)})
        img.alpha_composite(l2)
    return finish(img)


def doodle(d, kind, x, y, s, col):
    """hình nguệch ngoạc bút chì cạnh chữ (toạ độ đã phóng)"""
    w = max(1, int(s * 0.11))
    if kind == "mui_ten":
        d.line([(x, y), (x + s, y - s * 0.12)], fill=col, width=w)
        d.line([(x + s * 0.78, y - s * 0.32), (x + s, y - s * 0.12), (x + s * 0.74, y + s * 0.1)], fill=col, width=w, joint="curve")
    elif kind == "sao":
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = s * (0.5 if i % 2 == 0 else 0.22)
            pts.append((x + s * 0.5 + rr * math.cos(a), y + rr * math.sin(a)))
        d.line(pts + [pts[0]], fill=col, width=w, joint="curve")
    elif kind == "set":
        d.line([(x + s * 0.5, y - s * 0.5), (x + s * 0.2, y), (x + s * 0.55, y), (x + s * 0.25, y + s * 0.55)], fill=col, width=w, joint="curve")
    elif kind == "tuyet":
        for i in range(3):
            a = i * math.pi / 3
            d.line([(x + s * 0.5 - math.cos(a) * s * 0.4, y - math.sin(a) * s * 0.4),
                    (x + s * 0.5 + math.cos(a) * s * 0.4, y + math.sin(a) * s * 0.4)], fill=col, width=w)
    elif kind == "vuong_mien":
        pts = [(x, y + s * 0.3), (x + s * 0.05, y - s * 0.3), (x + s * 0.3, y), (x + s * 0.5, y - s * 0.4), (x + s * 0.7, y),
               (x + s * 0.95, y - s * 0.3), (x + s, y + s * 0.3)]
        d.line(pts + [pts[0]], fill=col, width=w, joint="curve")
    elif kind in ("?", "!"):
        f = ImageFont.truetype(FONT, int(s * 1.1))
        d.text((x, y), kind * (3 if kind == "?" else 2), fill=col, font=f, anchor="lm")


def note(k):
    text, dood = NOTES[k]
    fs = 40 * R * SS  # chữ cao ~40 đơn vị bản đồ
    f = ImageFont.truetype(FONT, fs)
    tmp = ImageDraw.Draw(Image.new("L", (10, 10)))
    tb = tmp.textbbox((0, 0), text, font=f)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    dw = int(fs * 1.2) if dood else 0
    pad = int(fs * 0.35)
    W, H = tw + dw + pad * 3, th + pad * 2 + int(fs * 0.5)
    lay = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(lay)
    d.text((pad - tb[0], pad + int(fs * 0.25) - tb[1]), text, fill=255, font=f)
    if dood:
        doodle(d, dood, pad * 2 + tw, pad + int(fs * 0.25) + th * 0.55, fs * 0.9, 255)
    # gạch chân nguệch ngoạc
    yl = pad + int(fs * 0.25) + th + int(fs * 0.12)
    rng = random.Random(k)
    pts = [(pad + i * tw / 8, yl + rng.uniform(-fs * 0.04, fs * 0.04)) for i in range(9)]
    d.line(pts, fill=200, width=max(1, int(fs * 0.06)), joint="curve")
    # hạt chì: alpha lốm đốm như nét chì trên giấy
    a = np.asarray(lay).astype(np.float32) / 255
    grain = np.random.default_rng(k).random(a.shape).astype(np.float32)
    a = a * (0.82 + 0.18 * grain)
    out = np.zeros(a.shape + (4,), np.uint8)
    out[..., :3] = GRAPHITE
    out[..., 3] = (a * 255).astype(np.uint8)
    img = Image.fromarray(out).rotate(rng.uniform(-7, 7), resample=Image.BICUBIC, expand=True)
    return finish(img)


def main():
    os.makedirs(OUT, exist_ok=True)
    arts = {"trung_set": bolt(), "trung_bong": bubble(), "trung_tuyet": snowflake(), "trung_nuoc": spout()}
    for k in NOTES:
        arts[f"trung_ghi_{k}"] = note(k)
    for name, im in arts.items():
        im.save(os.path.join(OUT, name + ".png"))
        print(name, im.size)
    # tờ soi trên giấy phác chì và trên mây
    items = list(arts.items())
    cols = 5
    cw, ch = 300, 230
    sheet = Image.new("RGBA", (cw * cols, ch * ((len(items) + cols - 1) // cols)), (243, 233, 211, 255))
    for i, (name, im) in enumerate(items):
        x, y = (i % cols) * cw, (i // cols) * ch
        k = min((cw - 20) / im.width, (ch - 40) / im.height, 1.0)
        im2 = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
        sheet.alpha_composite(im2, (x + (cw - im2.width) // 2, y + 10))
        ImageDraw.Draw(sheet).text((x + 6, y + ch - 24), name, fill=(0, 0, 0, 255))
    sheet.convert("RGB").save(SOI)
    print("tờ soi:", os.path.abspath(SOI))


if __name__ == "__main__":
    main()
