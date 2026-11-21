# Ghi chú bút chì bản tiếng Anh (2026-11-21, đa ngôn ngữ GD_Claude/24): vẽ trung_ghi_<k>_en.png (đảo Thủy) và
# trung_ghi_<đảo>_<k>_en.png (Mộc, Kim, Hỏa, Thổ) bằng đúng hàm vẽ của land_thuy/m0/ve_trung.py (phông Pangolin, màu chì, hình
# nguệch ngoạc, gạch chân, hạt chì, cùng hạt ngẫu nhiên theo k). Xuất vào Assets/03 Art/Islands/Co cạnh bản tiếng Việt.
# ZoneSceneEggs chọn bản _en khi Loc.IsEn; gắn ảnh vào màn đảo: menu PokiClash/Ngôn ngữ/Gắn ghi chú tiếng Anh vào màn đảo
# (hoặc PokiClash/Đảo vùng đất/Dựng cờ ải, vùng boss — gom mọi trung_*). Chạy: py -3 -I ve_trung_en.py
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
THUY = os.path.join(HERE, "land_thuy", "m0")
sys.path.insert(0, THUY)
import ve_trung  # noqa: E402
from ve_co import OUT  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

# (tiền tố tên ảnh, ghi chú theo vùng k: (chữ, hình nguệch ngoạc) — hình giữ như bản tiếng Việt)
NOTES = {
    "trung_ghi_": {
        1: ("Ribbit…?", "?"),
        2: ("Who lit the lamp?", "mui_ten"),
        3: ("A pearl!?", "sao"),
        4: ("Old shipwreck", "mui_ten"),
        5: ("Keep out in rain!", "set"),
        6: ("Bones… huge!", "!"),
        7: ("Glowing shrooms?!", "sao"),
        8: ("Freezing…", "tuyet"),
        9: ("Dragon's den?", "vuong_mien"),
    },
    "trung_ghi_moc_": {
        1: ("Smells so good!", "sao"),
        2: ("Shrooms… edible?", "?"),
        3: ("Vines block the way!", "!"),
        4: ("Howling wind…", "mui_ten"),
        5: ("Red leaves forever…", "sao"),
        6: ("Dragon claw?!", "!"),
        7: ("Who twirls a staff?", "?"),
        8: ("Crystals!", "sao"),
        9: ("Sacred tree…", "vuong_mien"),
    },
    "trung_ghi_kim_": {
        1: ("Gears creaking…", "mui_ten"),
        2: ("Leaves sharp as knives!", "!"),
        3: ("Who stands guard?", "?"),
        4: ("Bells ring alone?", "?"),
        5: ("Bronze is boiling!", "!"),
        6: ("Silver in the mine!", "sao"),
        7: ("Cursed sword…", "!"),
        8: ("Whose nest?", "?"),
        9: ("Sky Bell…", "vuong_mien"),
    },
    "trung_ghi_hoa_": {
        1: ("Hot hot feet!", "!"),
        2: ("Trees burn forever…", "?"),
        3: ("Thick smoke…", "mui_ten"),
        4: ("Who keeps the fire?", "?"),
        5: ("Lotus in flames?!", "sao"),
        6: ("Hammering at night…", "!"),
        7: ("Purple fire… mirage?", "?"),
        8: ("Rubies!", "sao"),
        9: ("Volcano's gonna blow!", "vuong_mien"),
    },
    "trung_ghi_tho_": {
        1: ("Whose cave?", "?"),
        2: ("Emeralds!", "sao"),
        3: ("Pink crystals…", "sao"),
        4: ("Glowing runes?", "?"),
        5: ("Thousand-year oak…", "mui_ten"),
        6: ("Golden rice", "!"),
        7: ("Real diamonds!", "sao"),
        8: ("Kiln's still warm…", "?"),
        9: ("The Earth King rules here", "vuong_mien"),
    },
}


def main():
    os.makedirs(OUT, exist_ok=True)
    made = []
    for prefix, notes in NOTES.items():
        ve_trung.NOTES = notes
        for k in notes:
            name = f"{prefix}{k}_en"
            im = ve_trung.note(k)
            im.save(os.path.join(OUT, name + ".png"))
            made.append((name, im))
    # tờ soi: bản Việt (nếu có) cạnh bản Anh
    rows = []
    for name, im in made:
        vi = os.path.join(OUT, name[:-3] + ".png")
        a = Image.open(vi).convert("RGBA") if os.path.exists(vi) else Image.new("RGBA", (10, 10))
        rows.append((a, im))
    W = 1400
    H = sum(max(a.height, b.height) // 2 + 8 for a, b in rows) + 10
    sheet = Image.new("RGBA", (W, H), (243, 233, 211, 255))
    y = 5
    for a, b in rows:
        a2 = a.resize((max(1, a.width // 2), max(1, a.height // 2)))
        b2 = b.resize((max(1, b.width // 2), max(1, b.height // 2)))
        sheet.alpha_composite(a2, (10, y))
        sheet.alpha_composite(b2, (710, y))
        y += max(a2.height, b2.height) + 8
    sheet.convert("RGB").save(os.path.join(HERE, "soi_trung_en.png"))
    print(len(made), "ghi chú tiếng Anh ->", OUT)


if __name__ == "__main__":
    main()
