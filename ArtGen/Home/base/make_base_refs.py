# Bản phác bố cục cho ảnh ĐẢO NỀN của Nhà (GD_Claude/21_Nha_Home.md): chỉ phần cố định, không rừng, không công trình.
# Toạ độ lấy từ khối "home" của Assets/02 Data/Json/balance.json (lưới 48 x 48, ô rừng 8 x 8, features, lots "hill").
# Ra: refs/base_layout.png (1792 x 1008, 16:9). Hình thoi đảo: ô (0,0) ở góc trên, gx đi xuống phải, gy đi xuống trái, ô rộng 32 px.
# Chạy: py -3 -I make_base_refs.py
import os, json, math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "refs")
os.makedirs(OUT, exist_ok=True)
cfg = json.load(open(os.path.join(ROOT, "Assets", "02 Data", "Json", "balance.json"), encoding="utf-8"))["home"]

W, H = 1792, 1008
CW = 32  # px mỗi ô theo bề ngang
OX, OY = 896, 150  # góc trên của hình thoi (ô 0,0)
GRID, LOT = cfg["grid"], cfg["lot"]
INK = (60, 40, 30)


def font(sz):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def P(gx, gy, z=0):
    return (OX + (gx - gy) * CW / 2, OY + (gx + gy) * CW / 4 - z)


def quad(gx, gy, w, d, z=0):
    return [P(gx, gy, z), P(gx + w, gy, z), P(gx + w, gy + d, z), P(gx, gy + d, z)]


def label(d, q, text, sz=22):
    c = ((q[0][0] + q[2][0]) / 2, (q[0][1] + q[2][1]) / 2)
    d.text(c, text, fill=(255, 255, 255), font=font(sz), anchor="mm", stroke_width=2, stroke_fill=INK)


def build():
    im = Image.new("RGB", (W, H), (120, 180, 222))
    d = ImageDraw.Draw(im)
    top, right, bottom, left = P(0, 0), P(GRID, 0), P(GRID, GRID), P(0, GRID)
    # dải phong cảnh xa trên cùng, dải đồi cao ngoài hai cạnh trên
    d.rectangle([0, 0, W, 70], fill=(170, 205, 160))
    d.text((W / 2, 35), "far landscape strip: distant hills, sea, small islands", fill=INK, font=font(20), anchor="mm")
    d.polygon([(top[0], top[1] - 70), (right[0] + 90, right[1] - 10), right, top, left, (left[0] - 90, left[1] - 10)], fill=(120, 165, 95), outline=INK)
    # bãi cát ngoài hai cạnh dưới, rồi biển
    d.polygon([(left[0] - 90, left[1] - 10), left, bottom, right, (right[0] + 90, right[1] - 10), (bottom[0], bottom[1] + 75)], fill=(238, 222, 168), outline=INK)
    # đồng cỏ
    d.polygon([top, right, bottom, left], fill=(178, 214, 128), outline=INK)
    # ô cao nguyên (lots kind hill): khối nâng có vách nâu
    for l in cfg["lots"]:
        if l["kind"] != "hill":
            continue
        gx, gy = l["i"] * LOT, l["j"] * LOT
        a = quad(gx, gy, LOT, LOT)
        t = quad(gx, gy, LOT, LOT, 46)
        d.polygon([a[3], a[2], t[2], t[3]], fill=(150, 100, 70), outline=INK)
        d.polygon([a[2], a[1], t[1], t[2]], fill=(130, 85, 60), outline=INK)
        d.polygon(t, fill=(130, 180, 90), outline=INK)
        label(d, t, "H", 26)
    # điểm cố định
    col = {"lake": (90, 160, 220), "stream": (90, 160, 220), "ore": (128, 118, 112)}
    for f in cfg["features"]:
        if f["kind"] not in col:
            continue
        q = quad(f["gx"], f["gy"], f["w"], f["d"])
        d.polygon(q, fill=col[f["kind"]], outline=INK)
        if f["kind"] == "lake":
            label(d, q, "lake", 18)
        elif f["kind"] == "ore":
            label(d, q, "ore", 18)
    # thác: từ vách cao nguyên (0,1)/(1,0) xuống hồ ở ô rừng (1,1)
    w0 = P(8, 9, 46)
    w1 = P(10.5, 10.5)
    d.line([w0, w1], fill=(90, 160, 220), width=10)
    d.text((w0[0] + 40, w0[1] + 10), "waterfall", fill=INK, font=font(16), anchor="lm")
    # bến thuyền ở mũi nam
    d.polygon([(bottom[0] - 6, bottom[1] - 3), (bottom[0] + 6, bottom[1] - 3), (bottom[0] + 46, bottom[1] + 60), (bottom[0] + 34, bottom[1] + 64)], fill=(150, 100, 60), outline=INK)
    d.text((bottom[0] + 70, bottom[1] + 40), "dock", fill=INK, font=font(18), anchor="lm")
    im.save(os.path.join(OUT, "base_layout.png"))
    # toạ độ góc hình thoi trong ảnh phác (tỉ lệ 0..1) để khớp ảnh gen ra
    meta = {"size": [W, H], "top": P(0, 0), "right": P(GRID, 0), "bottom": P(GRID, GRID), "left": P(0, GRID)}
    json.dump(meta, open(os.path.join(OUT, "base_layout.json"), "w"), indent=1)


if __name__ == "__main__":
    build()
    print("ok", OUT)
