# Cắt rãnh thanh kinh nghiệm (viên thuốc viền nâu, lòng tím) ra khỏi thân máy vẽ tay, để thanh EXP nhún được cả viền:
# - đọc Assets/03 Art/Pachinko/pk_than_may.png và số đo refs/than_may_da_duyet.json (rãnh "groove", khung thân máy "cabinet");
# - tìm đúng mép viên thuốc theo nét viền tối quanh rãnh, cắt theo hình viên thuốc (ngoài hình thì trong suốt, mép mềm 1 px);
# - ghi Assets/03 Art/Pachinko/pk_ranh_exp.png và refs/ranh_exp.json (khung ảnh cắt theo px khối máy, y xuống).
# Menu Unity "PokiClash/Prefab/Máy bi: thân máy vẽ tay" đặt ảnh này trùng khít lên rãnh của thân máy, gom cùng thanh thành
# nhóm "khung_thanh" để nhún cùng nhau. Duyệt lại thân máy (build.py --duyet) thì chạy lại script này rồi chạy lại menu.
# Chạy: py -3 -I ArtGen/Pachinko/cat_ranh.py
import json
import os
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(ROOT, "Assets", "03 Art", "Pachinko", "pk_than_may.png")
OUT = os.path.join(ROOT, "Assets", "03 Art", "Pachinko", "pk_ranh_exp.png")
MEASURE = os.path.join(HERE, "refs", "than_may_da_duyet.json")
OUT_JSON = os.path.join(HERE, "refs", "ranh_exp.json")
SS = 4  # siêu lấy mẫu cho mép mặt nạ


def dark(px):
    r, g, b, a = px
    return a > 128 and r + g + b < 200


def main():
    m = json.load(open(MEASURE, encoding="utf-8"))
    im = Image.open(SRC).convert("RGBA")
    W, H = im.size
    cab = m["cabinet"]
    # ảnh thân máy đặt ở khung cabinet (px khối máy); đổi px khối máy -> px ảnh
    sx = W / (cab[2] - cab[0])
    sy = H / (cab[3] - cab[1])
    gx0, gy0, gx1, gy1 = m["groove"]
    ix0, iy0 = (gx0 - cab[0]) * sx, (gy0 - cab[1]) * sy
    ix1, iy1 = (gx1 - cab[0]) * sx, (gy1 - cab[1]) * sy
    cy = int((iy0 + iy1) / 2)
    cx = int((ix0 + ix1) / 2)
    px = im.load()
    pad = 20

    # mép ngoài nét viền: từ trong lòng rãnh đi ra tới hết nét tối
    def out_edge(x, y, dx, dy, limit):
        # đi tới nét tối đầu tiên
        n = 0
        while n < limit and not dark(px[x, y]):
            x += dx
            y += dy
            n += 1
        # đi qua hết nét tối
        while n < limit and dark(px[x, y]):
            x += dx
            y += dy
            n += 1
        return x - dx, y - dy

    _, top = out_edge(cx, cy, 0, -1, int((iy1 - iy0) / 2) + pad)
    _, bot = out_edge(cx, cy, 0, 1, int((iy1 - iy0) / 2) + pad)
    left, _ = out_edge(int(ix0 + (iy1 - iy0) / 2), cy, -1, 0, int((iy1 - iy0)) + pad)
    right, _ = out_edge(int(ix1 - (iy1 - iy0) / 2), cy, 1, 0, int((iy1 - iy0)) + pad)
    # thêm 1 px cho mép mềm của nét vẽ tay
    x0, y0, x1, y1 = left - 1, top - 1, right + 2, bot + 2
    w, h = x1 - x0, y1 - y0
    crop = im.crop((x0, y0, x1, y1))
    mask = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w * SS - 1, h * SS - 1), radius=h * SS / 2, fill=255)
    mask = mask.resize((w, h), Image.LANCZOS)
    a = crop.getchannel("A")
    a = Image.composite(a, Image.new("L", (w, h), 0), mask)
    crop.putalpha(a)
    crop.save(OUT, optimize=True)

    # khung ảnh cắt theo px khối máy
    bx0, by0 = cab[0] + x0 / sx, cab[1] + y0 / sy
    bx1, by1 = cab[0] + x1 / sx, cab[1] + y1 / sy
    info = {"source": os.path.relpath(SRC, ROOT).replace("\\", "/"), "image_px": [x0, y0, x1, y1],
            "block": [round(bx0, 2), round(by0, 2), round(bx1, 2), round(by1, 2)]}
    json.dump(info, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Rãnh: ảnh px {x0},{y0} → {x1},{y1} ({w} × {h}); px khối máy {info['block']}")
    print("Ghi", OUT)
    print("Ghi", OUT_JSON)


if __name__ == "__main__":
    main()
