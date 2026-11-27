# Sprite giao diện màn cửa hàng bản 3 (người dùng 2026-11-27: "thiết kế shop như clash of critters, nền tối, gói IAP màu tươi nổi").
# Vẽ bằng PIL (khối phẳng, viền đậm, vân sáp mờ), không lấy hình của game khác. Các tấm xám (the_*, o_nen, nut_gia) để code tô màu theo gói:
# trắng nhân màu thành màu đó, đen giữ đen (viền, dải tên). Chạy: py -3 -I ve_ui.py [--assets]  → out/ (xem trước) hoặc Assets/03 Art/Shop/v3/.
# Cỡ khớp bộ dựng Editor/ShopPageMenu.cs (BuildPage): thẻ 858 x 400, ô lưới 276 x 420, băng mục 858 x 100.
import math
import os
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
import sys

# mặc định ghi ra out/ cạnh script để xem trước; --assets ghi thẳng vào Assets (lúc giữ lượt Unity)
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Assets", "03 Art", "Shop", "v3")) if "--assets" in sys.argv else os.path.join(HERE, "out")
SS = 3  # vẽ to gấp 3 rồi thu cho mép mịn
INK = (22, 20, 42, 255)  # viền: xanh mực gần đen như thẻ mẫu


def hexc(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def canvas(w, h, fill=(0, 0, 0, 0)):
    return Image.new("RGBA", (w * SS, h * SS), fill)


def finish(im, w, h, name):
    im = im.resize((w, h), Image.LANCZOS)
    os.makedirs(OUT, exist_ok=True)
    im.save(os.path.join(OUT, name + ".png"))
    print(name, w, h)


def rr_mask(w, h, r, inset=0):
    m = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(m).rounded_rectangle([inset * SS, inset * SS, (w - inset) * SS - 1, (h - inset) * SS - 1], r * SS - inset * SS, fill=255)
    return m


def grain(w, h, amp, seed):
    # vân sáp: nhiễu mịn kéo chéo, độ lệch ±amp quanh 128
    rnd = random.Random(seed)
    small = Image.new("L", (w // 2 + 1, h // 2 + 1))
    small.putdata([128 + int(rnd.uniform(-amp, amp)) for _ in range(small.width * small.height)])
    g = small.resize((w * SS, h * SS), Image.BILINEAR).filter(ImageFilter.GaussianBlur(SS * 0.6))
    return g


def apply_grain(lum, g):
    # lum: ảnh L độ sáng; cộng nhiễu quanh 128
    return ImageChops.add(lum, g, 1, -128)


def vgrad(w, h, stops):
    # stops: [(t 0..1 từ trên xuống, độ sáng 0..255)]
    col = Image.new("L", (1, h * SS))
    px = []
    for y in range(h * SS):
        t = y / (h * SS - 1)
        for i in range(len(stops) - 1):
            t0, v0 = stops[i]
            t1, v1 = stops[i + 1]
            if t0 <= t <= t1:
                k = 0 if t1 == t0 else (t - t0) / (t1 - t0)
                px.append(int(v0 + (v1 - v0) * k))
                break
        else:
            px.append(stops[-1][1])
    col.putdata(px)
    return col.resize((w * SS, h * SS))


def diamonds(w, h, size, lo, hi):
    # caro thoi (xoay 45 độ) hai tông độ sáng
    m = Image.new("L", (w * SS, h * SS), hi)
    d = ImageDraw.Draw(m)
    s = size * SS
    for cy in range(-s, h * SS + s, s):
        for cx in range(-s, w * SS + s, s):
            if ((cx // s) + (cy // s)) % 2 == 0:
                d.polygon([(cx, cy - s // 2), (cx + s // 2, cy), (cx, cy + s // 2), (cx - s // 2, cy)], fill=lo)
    return m


def gray_rgba(lum, alpha):
    return Image.merge("RGBA", (lum, lum, lum, alpha))


def outline_layer(w, h, r, width):
    outer = rr_mask(w, h, r)
    inner = rr_mask(w, h, r, width)
    ring = ImageChops.subtract(outer, inner)
    layer = Image.new("RGBA", (w * SS, h * SS), INK)
    layer.putalpha(ring)
    return layer


def bottom_dark(w, h, start, full):
    # hệ số tối dần ở đáy: 255 (không tối) tới 0 (đen) — dải tên của thẻ
    return vgrad(w, h, [(0, 255), (start, 255), (full, 18), (1, 10)])


def burst_poly(cx, cy, r_in, r_out, n, rot=0.0, jitter=0.0, seed=1):
    rnd = random.Random(seed)
    pts = []
    for i in range(n * 2):
        a = rot + math.pi * i / n
        r = (r_out if i % 2 == 0 else r_in) * (1 + rnd.uniform(-jitter, jitter))
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


# ---------- thẻ ngang (ShopCard) ----------

def card(w=858, h=400, r=28, line=7):
    inner = rr_mask(w, h, r, line)
    dark = bottom_dark(w, h, 0.62, 0.9)
    g = grain(w, h, 9, 11)
    # nền màu chính: sáng trên, hơi trầm dưới, tối hẳn ở dải tên
    lum = vgrad(w, h, [(0, 255), (0.55, 236), (1, 220)])
    lum = ImageChops.multiply(apply_grain(lum, g), dark)
    base = gray_rgba(lum, rr_mask(w, h, r))
    base.alpha_composite(outline_layer(w, h, r, line))
    finish(base, w, h, "the_nen")

    # mảng phải màu phụ: cắt chéo, caro thoi, cùng độ tối đáy
    m = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(m).polygon([(w * 0.56 * SS, 0), (w * SS, 0), (w * SS, h * SS), (w * 0.44 * SS, h * SS)], fill=255)
    m = ImageChops.multiply(m, inner)
    lum = ImageChops.multiply(apply_grain(diamonds(w, h, 70, 222, 255), g), dark)
    finish(gray_rgba(lum, m), w, h, "the_phai")

    # sao nổ sau hình (trái): khối sao kem + tia mờ, mờ dần xuống dải tên
    cx, cy = 0.27 * w * SS, 0.43 * h * SS
    a = Image.new("L", (w * SS, h * SS), 0)
    d = ImageDraw.Draw(a)
    for i in range(18):
        if i % 2:
            continue
        a0 = math.pi * 2 * i / 18 + 0.1
        a1 = math.pi * 2 * (i + 1) / 18 + 0.1
        R = w * SS
        d.polygon([(cx, cy), (cx + math.cos(a0) * R, cy + math.sin(a0) * R), (cx + math.cos(a1) * R, cy + math.sin(a1) * R)], fill=70)
    d.polygon(burst_poly(cx, cy, 120 * SS, 190 * SS, 13, 0.2, 0.12, 5), fill=235)
    fade = vgrad(w, h, [(0, 255), (0.55, 255), (0.85, 0), (1, 0)])
    a = ImageChops.multiply(ImageChops.multiply(a, inner), fade)
    lum = Image.new("L", (w * SS, h * SS), 255)
    finish(gray_rgba(lum, a), w, h, "the_tia")


# ---------- ô lưới (ShopTile) ----------

def tile(w=276, h=420, r=24, line=6, strip=100):
    g = grain(w, h, 9, 23)
    lum = vgrad(w, h, [(0, 255), (1, 214)])
    lum = ImageChops.multiply(apply_grain(lum, g), diamonds(w, h, 56, 238, 255))
    base = gray_rgba(lum, rr_mask(w, h, r))
    # dải nút đáy: đen mực, nối thẳng vào viền
    s = Image.new("RGBA", (w * SS, h * SS), INK)
    sm = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(sm).rectangle([0, (h - strip) * SS, w * SS, h * SS], fill=255)
    s.putalpha(ImageChops.multiply(sm, rr_mask(w, h, r)))
    base.alpha_composite(s)
    base.alpha_composite(outline_layer(w, h, r, line))
    finish(base, w, h, "o_nen")

    inner = rr_mask(w, h, r, line)
    cx, cy = 0.5 * w * SS, 0.42 * h * SS
    a = Image.new("L", (w * SS, h * SS), 0)
    d = ImageDraw.Draw(a)
    for i in range(0, 16, 2):
        a0 = math.pi * 2 * i / 16
        a1 = math.pi * 2 * (i + 1) / 16
        R = h * SS
        d.polygon([(cx, cy), (cx + math.cos(a0) * R, cy + math.sin(a0) * R), (cx + math.cos(a1) * R, cy + math.sin(a1) * R)], fill=60)
    d.polygon(burst_poly(cx, cy, 82 * SS, 124 * SS, 11, 0.3, 0.12, 9), fill=225)
    cut = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(cut).rectangle([0, 0, w * SS, (h - strip) * SS], fill=255)
    a = ImageChops.multiply(ImageChops.multiply(a, inner), cut)
    finish(gray_rgba(Image.new("L", (w * SS, h * SS), 255), a), w, h, "o_tia")


# ---------- băng tiêu đề mục, ô chọn cột trái ----------

def band(w=858, h=100, r=20, line=6):
    lo, hi = hexc("#7a2be8"), hexc("#8a38f6")
    m = diamonds(w, h, 44, 0, 255)
    im = Image.composite(Image.new("RGBA", (w * SS, h * SS), hi), Image.new("RGBA", (w * SS, h * SS), lo), m)
    # vệt sáng mép trên trong viền
    hl = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(hl).rounded_rectangle([line * SS, line * SS, (w - line) * SS, (line + 7) * SS], 4 * SS, fill=90)
    im.alpha_composite(Image.merge("RGBA", (Image.new("L", hl.size, 200), Image.new("L", hl.size, 150), Image.new("L", hl.size, 255), hl)))
    im.putalpha(rr_mask(w, h, r))
    im.alpha_composite(outline_layer(w, h, r, line))
    finish(im, w, h, "muc_bang")


def nav_pick(w=176, h=220, r=24, line=5):
    top, bot = hexc("#a04cff"), hexc("#38d8ff")
    t = vgrad(w, h, [(0, 0), (0.3, 0), (1, 255)])
    im = Image.composite(Image.new("RGBA", (w * SS, h * SS), bot), Image.new("RGBA", (w * SS, h * SS), top), t)
    im.putalpha(rr_mask(w, h, r))
    im.alpha_composite(outline_layer(w, h, r, line))
    finish(im, w, h, "muc_chon")


# ---------- nhãn giá trị, nút giá, ô món ----------

def ribbon(w=320, h=74, line=5):
    notch = 26
    poly = [(0, 0), (w, 0), (w, h), (0, h), (notch, h / 2)]
    S = [(x * SS, y * SS) for x, y in poly]
    m = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(m).polygon(S, fill=255)
    fill = Image.composite(Image.new("RGBA", m.size, hexc("#e8285a")), Image.new("RGBA", m.size, hexc("#ff3d6e")),
                           vgrad(w, h, [(0, 0), (0.5, 0), (1, 255)]))
    fill.putalpha(m)
    # viền: nét đa giác dày
    o = Image.new("L", m.size, 0)
    ImageDraw.Draw(o).line(S + [S[0]], fill=255, width=line * 2 * SS, joint="curve")
    o = ImageChops.multiply(o, m)
    ink = Image.new("RGBA", m.size, INK)
    ink.putalpha(o)
    fill.alpha_composite(ink)
    finish(fill, w, h, "nhan_gia_tri")


def button(name, w=300, h=110, r=30, line=6, body=224, lip=176):
    outer = rr_mask(w, h, r)
    lum = Image.new("L", (w * SS, h * SS), body)
    # môi tối dưới, viền sáng trong
    ImageDraw.Draw(lum).rectangle([0, (h - line - 14) * SS, w * SS, h * SS], fill=lip)
    rim = ImageChops.subtract(rr_mask(w, h, r, line), rr_mask(w, h, r, line + 5))
    lum = Image.composite(Image.new("L", lum.size, 255), lum, rim)
    im = gray_rgba(apply_grain(lum, grain(w, h, 6, 31)), outer)
    im.alpha_composite(outline_layer(w, h, r, line))
    finish(im, w, h, name)


def item_cell(w=128, h=128, r=20, line=5, strip=42):
    im = Image.new("RGBA", (w * SS, h * SS), (255, 255, 255, 255))
    ImageDraw.Draw(im).rectangle([0, (h - strip) * SS, w * SS, h * SS], fill=INK)
    im.putalpha(rr_mask(w, h, r))
    im.alpha_composite(outline_layer(w, h, r, line))
    finish(im, w, h, "o_mon")


def dot(w=48, h=48, line=5):
    # chấm đỏ báo quà chờ: tròn đỏ viền mực
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, w * SS - 1, h * SS - 1], fill=INK)
    d.ellipse([line * SS, line * SS, (w - line) * SS - 1, (h - line) * SS - 1], fill=hexc("#ff3b4f"))
    finish(im, w, h, "cham_do")


def sheet_panel(w=300, h=300, r=34, line=7):
    # nền tờ popup / trang con: chàm thẫm caro thoi mờ, viền mực (Sliced 44)
    lo, hi = hexc("#272247"), hexc("#2d2852")
    m = diamonds(w, h, 52, 0, 255)
    im = Image.composite(Image.new("RGBA", (w * SS, h * SS), hi), Image.new("RGBA", (w * SS, h * SS), lo), m)
    im.putalpha(rr_mask(w, h, r))
    im.alpha_composite(outline_layer(w, h, r, line))
    finish(im, w, h, "to_toi")


def spin_rays(w=256, h=256, n=12):
    # vầng tia sau icon ưu đãi ở sảnh: tia kem, mờ dần ra mép (xoay bằng Spin)
    cx, cy = w * SS / 2, h * SS / 2
    a = Image.new("L", (w * SS, h * SS), 0)
    d = ImageDraw.Draw(a)
    R = w * SS
    for i in range(n):
        a0 = math.pi * 2 * i / n
        a1 = a0 + math.pi / n * 0.9
        d.polygon([(cx, cy), (cx + math.cos(a0) * R, cy + math.sin(a0) * R), (cx + math.cos(a1) * R, cy + math.sin(a1) * R)], fill=255)
    fall = Image.new("L", (w * SS, h * SS), 0)
    fd = ImageDraw.Draw(fall)
    steps = 40
    for k in range(steps):
        rr = (w * SS / 2) * (1 - k / steps)
        fd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=int(230 * (k + 1) / steps))
    a = ImageChops.multiply(a, fall)
    col = Image.new("RGBA", (w * SS, h * SS), hexc("#fff4c8"))
    col.putalpha(a)
    finish(col, w, h, "tia_xoay")


def pill(w=96, h=48):
    # viên thuốc trơn trắng (tô màu lúc chạy: đồng hồ, số bi, nhãn góc, thanh Lọ Bi); Sliced 24
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w * SS - 1, h * SS - 1], h * SS // 2, fill=(255, 255, 255, 255))
    finish(im, w, h, "vien")


def bg_tile(w=96, h=96):
    base, line = hexc("#3b3558"), hexc("#443e64")
    im = Image.new("RGBA", (w * SS, h * SS), base)
    d = ImageDraw.Draw(im)
    for k in (-1, 0, 1):
        d.line([(k * w * SS, 0), ((k + 1) * w * SS, h * SS)], fill=line, width=3 * SS)
        d.line([((k + 1) * w * SS, 0), (k * w * SS, h * SS)], fill=line, width=3 * SS)
    finish(im, w, h, "nen_trang")


if __name__ == "__main__":
    card()
    tile()
    band()
    nav_pick()
    ribbon()
    button("nut_gia")
    button("nut_gia_an", body=196, lip=160)
    item_cell()
    dot()
    sheet_panel()
    spin_rays()
    pill()
    bg_tile()
