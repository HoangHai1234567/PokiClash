# Easter egg bản đồ sảnh (người dùng 2026-11-23: "bố cục scene các đảo này vẫn hơi tĩnh ... thêm các easter egg vào để người chơi khám
# phá"). Ghi các món e_* (và hải âu lượn) vào khoá world_map của Assets/03 Art/Islands/island_anim.json; Unity: IslandAnimTrung.cs.
# Hình sinh vật: to_sinh_vat_1.png (Magnific GPT 2.6, ảnh mẫu mau_style_thuy.jpg cắt từ bản đồ) → cat_to.py --chep.
# Toạ độ: ảnh nới 1024 x 1796 (= world_map.png / 2), như nuoc_dong.py. Chạy: py -3 -I trung_sanh.py
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Assets", "03 Art", "Islands"))
W1, H1 = 1024, 1796

# k, x, y, s (bề ngang hình), thêm: r (bán kính điểm chạm), tx/ty (đích bò / chỗ chai trôi), lx/ly (đèn), pts, rx/ry
EGGS = [
    {"k": "e_nui", "x": 375, "y": 195, "s": 95, "r": 48},                       # miệng núi lửa
    {"k": "e_den", "x": 302, "y": 1308, "s": 150, "r": 34, "lx": 302, "ly": 1276},  # hải đăng (điểm chạm thân, đèn dưới mái đỏ)
    {"k": "e_tau", "x": 365, "y": 1428, "s": 34, "r": 40, "tx": 452, "ty": 1446},   # xác tàu → bãi cát
    {"k": "e_xoay", "x": 695, "y": 1180, "s": 30, "r": 62, "tx": 800, "ty": 1310},  # xoáy nước → chai trôi ra biển (cạnh thác Thủy)
    {"k": "e_sanho", "x": 135, "y": 1350, "s": 15, "r": 26, "pts": [[135, 1350], [155, 1470], [300, 1452], [355, 1484]]},
    # sinh vật đặt trong dải biển gần bờ: mây vành phủ biển cách đất từ ~100 px (tach_dao.ring_clouds; mây trong game to hơn ước lượng,
    # soát với elip mây phóng 1,35 lần), cách bờ 18–70 px
    {"k": "e_voi", "x": 780, "y": 1528, "s": 72},                                # cá voi dưới cầu tàu (lưng không đè cột cầu, mép mây dưới ~1547)
    {"k": "e_ca", "x": 180, "y": 1290, "s": 30,
     "pts": [[200, 1312], [250, 1515], [560, 1540], [760, 1545], [860, 1530], [620, 1085], [420, 1095], [195, 1200]]},
    {"k": "e_rua", "x": 860, "y": 1225, "s": 30, "rx": 45, "ry": 12},            # rùa bên phải xoáy nước
    # hải âu lượn (hình cắt từ đảo Thủy vùng đất, chung atlas với mây sảnh)
    {"k": "glide", "x": 170, "y": 1110, "s": 36, "a": "land_thuy_chim_1", "v": 2.2},
    {"k": "glide", "x": 870, "y": 1060, "s": 30, "a": "land_thuy_chim_2", "v": 2.8},
    {"k": "glide", "x": 610, "y": 760, "s": 28, "a": "land_thuy_chim_3", "v": 3.0},
]
OWN_KEYS = ("e_",)


def apply(entry):
    """Thay các món của file này trong khoá world_map (nuoc_dong.py và build_sanh.py gọi lại)."""
    keep = [it for it in entry.get("items", []) if not str(it.get("k", "")).startswith(OWN_KEYS)
            and not (it.get("k") == "glide" and str(it.get("a", "")).startswith("land_thuy_chim_"))]
    for e in EGGS:
        it = {"k": e["k"], "x": round(e["x"] / W1, 4), "y": round(e["y"] / H1, 4), "s": round(e["s"] / W1, 4)}
        for key in ("r", "rx", "ry"):
            if key in e:
                it[key] = round(e[key] / W1, 4)
        for kx, ky in (("tx", "ty"), ("lx", "ly")):
            if kx in e:
                it[kx], it[ky] = round(e[kx] / W1, 4), round(e[ky] / H1, 4)
        if "pts" in e:
            it["pts"] = [[round(x / W1, 4), round(y / H1, 4)] for x, y in e["pts"]]
        for key in ("a", "v"):
            if key in e:
                it[key] = e[key]
        keep.append(it)
    entry["items"] = keep


def main():
    path = os.path.join(ART, "island_anim.json")
    raw = open(path, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    anim = json.loads(raw.decode("utf-8"))
    entry = anim.setdefault("world_map", {"items": [], "rivers": [], "lights": []})
    apply(entry)
    open(path, "w", encoding="utf-8", newline=nl).write(json.dumps(anim, ensure_ascii=False, indent=1))
    print("đã ghi", len(EGGS), "món easter egg vào khoá world_map,", len(entry["items"]), "món")


if __name__ == "__main__":
    main()
