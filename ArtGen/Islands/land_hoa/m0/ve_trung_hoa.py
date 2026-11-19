# Ghi chú bút chì easter egg riêng của đảo Hỏa (2026-11-19): trung_ghi_hoa_<k>.png ở mép vùng k (phông Pangolin của game), dùng lại
# hàm vẽ của ArtGen/Islands/land_thuy/m0/ve_trung.py. Hình rơi, bay (lá, tàn lửa, tro) dùng lại trung_la, anim_glow, trung_tuyet
# nhuộm màu theo vùng (vung.py TEASE_COLOR). Xuất vào Assets/03 Art/Islands/Co. Chạy: py -3 -I ve_trung_hoa.py
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
    1: ("Nóng bỏng chân!", "!"),
    2: ("Cây cháy mãi…", "?"),
    3: ("Khói mù mịt…", "mui_ten"),
    4: ("Ai giữ lửa?", "?"),
    5: ("Sen nở trong lửa?!", "sao"),
    6: ("Tiếng búa đêm…", "!"),
    7: ("Lửa tím… ảo ảnh?", "?"),
    8: ("Hồng ngọc!", "sao"),
    9: ("Núi sắp phun!", "vuong_mien"),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    ve_trung.NOTES = NOTES
    for k in NOTES:
        im = ve_trung.note(k)
        im.save(os.path.join(OUT, f"trung_ghi_hoa_{k}.png"))
        print(f"trung_ghi_hoa_{k}", im.size)
    sheet = Image.new("RGBA", (1500, 380), (243, 233, 211, 255))
    x, y = 10, 10
    for k in NOTES:
        im = Image.open(os.path.join(OUT, f"trung_ghi_hoa_{k}.png"))
        im = im.resize((im.width // 2, im.height // 2))
        if x + im.width > 1490:
            x, y = 10, y + 120
        sheet.alpha_composite(im, (x, y))
        x += im.width + 10
    sheet.convert("RGB").save(os.path.join(HERE, "soi_trung_hoa.png"))
    print("ok")


if __name__ == "__main__":
    main()
