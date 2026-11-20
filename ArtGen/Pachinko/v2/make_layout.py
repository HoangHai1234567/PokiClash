# Khung bố cục màn máy bi bản 2 (GD_Claude/23, người dùng dặn 2026-11-20: "UI và máy bắn bóng chưa đủ đẹp, chưa đủ ấn tượng; layout lấy
# theo Clash of Critters; đèn chạy xung quanh, bảng số to đẹp có đèn"). Tỉ lệ các khối đo theo màn máy bi của họ (ảnh người dùng gửi,
# số đo bản đục ở D:\CrittersRipper\analysis_ui), hình là của mình: khung này chỉ là ô chữ nhật có nhãn, gửi Magnific làm khung.
# Ra: refs/khung_man_may.png (1024 x 1536, GPT 2.6 khổ 2:3 1k). Chạy: py -3 -I ArtGen/Pachinko/v2/make_layout.py
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "refs")
os.makedirs(OUT, exist_ok=True)
W, H = 1024, 1536
INK = (70, 50, 40)


def font(sz):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def label(d, xy, text, sz=26, fill=INK):
    d.text(xy, text, fill=fill, font=font(sz), anchor="mm")


def bulbs_on_arc(d, cx, cy, r, a0, a1, n, rb=11, fill=(255, 214, 90)):
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * i / (n - 1))
        x, y = cx + r * math.cos(a), cy - r * math.sin(a)
        d.ellipse([x - rb, y - rb, x + rb, y + rb], fill=fill, outline=INK, width=2)


def bulbs_on_line(d, x0, y0, x1, y1, n, rb=11, fill=(255, 214, 90)):
    for i in range(n):
        u = i / (n - 1)
        x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        d.ellipse([x - rb, y - rb, x + rb, y + rb], fill=fill, outline=INK, width=2)


def main():
    im = Image.new("RGB", (W, H), (236, 226, 210))  # nền phòng
    d = ImageDraw.Draw(im)
    # 1. thanh cấp
    d.rounded_rectangle([150, 46, 880, 104], 28, fill=(150, 120, 200), outline=INK, width=3)
    d.ellipse([56, 30, 156, 130], fill=(190, 160, 240), outline=INK, width=3)
    d.ellipse([900, 40, 968, 108], fill=(120, 200, 190), outline=INK, width=3)
    label(d, (515, 75), "1 LEVEL / XP BAR", 24, (255, 255, 255))
    # 3. tủ máy: vòm + hai cột, bóng đèn quanh vòm và dọc cột
    cab = (48, 300, 976, 1196)
    cx, top_r = 512, 464
    arch_cy = cab[1] + top_r
    d.pieslice([cx - top_r, cab[1], cx + top_r, cab[1] + 2 * top_r], 180, 360, fill=(232, 96, 70), outline=INK, width=4)
    d.rectangle([cab[0], arch_cy, cab[2], cab[3]], fill=(232, 96, 70), outline=INK, width=4)
    d.line([cab[0] + 2, arch_cy, cab[2] - 2, arch_cy], fill=(232, 96, 70), width=6)
    bulbs_on_arc(d, cx, arch_cy, top_r - 22, 180, 0, 21)
    bulbs_on_line(d, cab[0] + 22, arch_cy + 30, cab[0] + 22, cab[3] - 40, 12)
    bulbs_on_line(d, cab[2] - 22, arch_cy + 30, cab[2] - 22, cab[3] - 40, 12)
    # 4. mặt chơi (vòm trong) + làn phóng mép phải
    pr = 392
    d.pieslice([cx - pr, cab[1] + 72, cx + pr, cab[1] + 72 + 2 * pr], 180, 360, fill=(170, 215, 240), outline=INK, width=3)
    d.rectangle([cx - pr, cab[1] + 72 + pr, cx + pr, 1110], fill=(170, 215, 240), outline=INK, width=3)
    d.line([cx - pr + 2, cab[1] + 72 + pr, cx + pr - 2, cab[1] + 72 + pr], fill=(170, 215, 240), width=6)
    d.rounded_rectangle([cx + pr - 52, 560, cx + pr - 14, 1100], 16, fill=(250, 238, 210), outline=INK, width=2)
    label(d, (cx - 20, 690), "4 PLAYFIELD", 30)
    label(d, (cx - 20, 730), "(pegs, 2 bumpers, roof, cup)", 22)
    label(d, (cx + pr - 33, 830), "^", 26)
    # 5. hàng ô
    sx0, sx1, sy0, sy1 = cx - pr + 14, cx + pr - 60, 960, 1104
    n = 5
    for i in range(n):
        x0 = sx0 + (sx1 - sx0) * i / n + 6
        x1 = sx0 + (sx1 - sx0) * (i + 1) / n - 6
        col = (255, 220, 120) if i == 2 else (215, 190, 245)
        d.rounded_rectangle([x0, sy0, x1, sy1], 14, fill=col, outline=INK, width=3)
        label(d, ((x0 + x1) / 2, sy1 - 34), ["5", "10", "CHEST", "10", "5"][i], 30 if i != 2 else 22)
    label(d, (cx - 20, sy0 - 26), "5 SLOTS with big numbers", 22)
    # 2. bảng số (trên đỉnh vòm, chồng lên vòm)
    sb = (226, 150, 798, 318)
    d.rounded_rectangle(sb, 30, fill=(250, 180, 60), outline=INK, width=4)
    d.rounded_rectangle([sb[0] + 34, sb[1] + 30, sb[2] - 34, sb[3] - 30], 18, fill=(80, 40, 70), outline=INK, width=3)
    bulbs_on_line(d, sb[0] + 30, sb[1] + 15, sb[2] - 30, sb[1] + 15, 14, 9)
    bulbs_on_line(d, sb[0] + 30, sb[3] - 15, sb[2] - 30, sb[3] - 15, 14, 9)
    bulbs_on_line(d, sb[0] + 16, sb[1] + 40, sb[0] + 16, sb[3] - 40, 3, 9)
    bulbs_on_line(d, sb[2] - 16, sb[1] + 40, sb[2] - 16, sb[3] - 40, 3, 9)
    label(d, ((sb[0] + sb[2]) / 2, (sb[1] + sb[3]) / 2 - 8), "2 SCORE BOARD  523", 34, (255, 230, 120))
    label(d, ((sb[0] + sb[2]) / 2, (sb[1] + sb[3]) / 2 + 30), "big glowing digits", 18, (255, 230, 120))
    # đế tủ
    d.rounded_rectangle([90, 1190, 934, 1246], 18, fill=(200, 80, 60), outline=INK, width=3)
    # 6. nút thả tròn lớn
    d.ellipse([352, 1250, 672, 1450], fill=(250, 200, 60), outline=INK, width=5)
    d.ellipse([382, 1262, 642, 1410], fill=(255, 225, 110), outline=INK, width=3)
    label(d, (512, 1336), "6 PUSH", 36)
    # 7. nút cược, 8. khay rương
    d.rounded_rectangle([120, 1290, 296, 1392], 26, fill=(230, 230, 236), outline=INK, width=3)
    label(d, (208, 1341), "7 BET x3", 28)
    d.rounded_rectangle([728, 1270, 904, 1420], 26, fill=(160, 110, 70), outline=INK, width=3)
    label(d, (816, 1345), "8 CHEST", 26, (255, 255, 255))
    # 9. thanh đếm bi
    d.rounded_rectangle([340, 1466, 684, 1508], 20, fill=(120, 200, 230), outline=INK, width=3)
    label(d, (512, 1487), "9 BALLS 569", 22)
    im.save(os.path.join(OUT, "khung_man_may.png"))
    print("ok")


if __name__ == "__main__":
    main()
