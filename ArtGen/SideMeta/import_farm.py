"""Đưa ảnh Trang trại (gói build_farm.py) vào Unity:
- farm/tai_ve/farm_bg*.png (mới nhất) → Assets/03 Art/Farm/farm_bg.png (giữ 1024 x 1536);
- farm/tai_ve/farm_props*.png (mới nhất) → cắt lưới 4 x 3, khử nền trắng thành trong suốt, xén sát hình (chừa lề 6 px), lưu
  Assets/03 Art/Farm/props/farm_<tên>.png.
Sau đó chạy menu Unity "PokiClash/Prefab/Trang trại: cảnh thật".

    python -I ArtGen/SideMeta/import_farm.py
"""
import glob
import os
import sys

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.normpath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(HERE, "farm", "tai_ve")
DST = os.path.join(PROJECT, "Assets", "03 Art", "Farm")
NAMES = ["hoe", "can", "basket", "bread", "hammer", "sack", "apple", "carrot", "dust", "spark", "smoke", "heart"]


def newest(pattern):
    files = glob.glob(os.path.join(SRC, pattern))
    return max(files, key=os.path.getmtime) if files else None


def key_white(cell):
    """Nền trắng → trong suốt: độ trong theo khoảng cách tới trắng, rồi bỏ mảng trắng nối với mép (giữ trắng bên trong hình)."""
    rgb = cell.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    # vùng nền: loang từ mép qua các điểm gần trắng
    bg = Image.new("L", (w, h), 0)
    bp = bg.load()
    stack = [(x, y) for x in range(w) for y in (0, h - 1)] + [(x, y) for y in range(h) for x in (0, w - 1)]
    def near_white(c):
        return min(c) >= 232
    while stack:
        x, y = stack.pop()
        if bp[x, y] or not near_white(px[x, y]):
            continue
        bp[x, y] = 255
        if x > 0: stack.append((x - 1, y))
        if x < w - 1: stack.append((x + 1, y))
        if y > 0: stack.append((x, y - 1))
        if y < h - 1: stack.append((x, y + 1))
    # mảng gần trắng khép kín đủ lớn (lòng quai giỏ...) cũng là nền; chấm sáng nhỏ trong hình giữ lại
    seen = Image.new("L", (w, h), 0)
    sp = seen.load()
    for y0 in range(h):
        for x0 in range(w):
            if bp[x0, y0] or sp[x0, y0] or not near_white(px[x0, y0]):
                continue
            comp, st = [], [(x0, y0)]
            sp[x0, y0] = 1
            while st:
                x, y = st.pop()
                comp.append((x, y))
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if 0 <= nx < w and 0 <= ny < h and not sp[nx, ny] and not bp[nx, ny] and near_white(px[nx, ny]):
                        sp[nx, ny] = 1
                        st.append((nx, ny))
            if len(comp) > 400:
                for x, y in comp:
                    bp[x, y] = 255
    # mép mềm: làm mờ mặt nạ nền một chút rồi đảo thành alpha
    soft = bg.filter(ImageFilter.GaussianBlur(1.2))
    alpha = Image.eval(soft, lambda v: 255 - v)
    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    return out


def main():
    os.makedirs(os.path.join(DST, "props"), exist_ok=True)
    bg = newest("farm_bg*.png")
    if bg:
        im = Image.open(bg).convert("RGB")
        if im.size != (1024, 1536):
            im = im.resize((1024, 1536), Image.LANCZOS)
        im.save(os.path.join(DST, "farm_bg.png"))
        print("Nền:", bg)
    props = newest("farm_props*.png")
    if props:
        sheet = Image.open(props).convert("RGB")
        sw, sh = sheet.size
        cw, ch = sw / 4, sh / 3
        for i, name in enumerate(NAMES):
            c, r = i % 4, i // 4
            cell = sheet.crop((int(c * cw), int(r * ch), int((c + 1) * cw), int((r + 1) * ch)))
            cut = key_white(cell)
            box = cut.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
            if box:
                m = 6
                box = (max(0, box[0] - m), max(0, box[1] - m), min(cut.width, box[2] + m), min(cut.height, box[3] + m))
                cut = cut.crop(box)
            # vuông, hình ở giữa (Image giữ tỉ lệ dễ canh)
            side = max(cut.size)
            sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
            sq.paste(cut, ((side - cut.width) // 2, (side - cut.height) // 2))
            if side > 256:
                sq = sq.resize((256, 256), Image.LANCZOS)
            sq.save(os.path.join(DST, "props", f"farm_{name}.png"))
        print("Đồ nghề:", props, "→", len(NAMES), "hình")
    if not bg and not props:
        sys.exit("Chưa có ảnh trong " + SRC)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
