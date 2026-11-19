# Ghi chú bút chì easter egg riêng của đảo Kim (2026-11-19): trung_ghi_kim_<k>.png ở mép vùng k (phông Pangolin của game), dùng lại
# hàm vẽ của ArtGen/Islands/land_thuy/m0/ve_trung.py. Hình rơi, bay (lá thép, tia đồng, bong bóng) dùng lại trung_la, anim_glow, trung_bong
# nhuộm màu theo vùng (vung.py TEASE_COLOR). Xuất vào Assets/03 Art/Islands/Co. Chạy: py -3 -I ve_trung_kim.py
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
THUY = os.path.abspath(os.path.join(HERE, "..", "..", "land_thuy", "m0"))
sys.path.insert(0, THUY)
import ve_trung  # noqa: E402
from ve_co import OUT  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

NOTES = {
    1: ("Bánh răng kẽo kẹt…", "mui_ten"),
    2: ("Lá sắc như dao!", "!"),
    3: ("Ai canh gác?", "?"),
    4: ("Chuông tự ngân?", "?"),
    5: ("Đồng đang sôi!", "!"),
    6: ("Có bạc trong mỏ!", "sao"),
    7: ("Kiếm bị nguyền…", "!"),
    8: ("Tổ của ai?", "?"),
    9: ("Thiên Chung…", "vuong_mien"),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    ve_trung.NOTES = NOTES
    for k in NOTES:
        im = ve_trung.note(k)
        im.save(os.path.join(OUT, f"trung_ghi_kim_{k}.png"))
        print(f"trung_ghi_kim_{k}", im.size)
    sheet = Image.new("RGBA", (1500, 380), (243, 233, 211, 255))
    x, y = 10, 10
    for k in NOTES:
        im = Image.open(os.path.join(OUT, f"trung_ghi_kim_{k}.png"))
        im = im.resize((im.width // 2, im.height // 2))
        if x + im.width > 1490:
            x, y = 10, y + 120
        sheet.alpha_composite(im, (x, y))
        x += im.width + 10
    sheet.convert("RGB").save(os.path.join(HERE, "soi_trung_kim.png"))
    print("ok")


if __name__ == "__main__":
    main()
