# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 9 đảo Thổ (id `cu_phu`, ải 60 "Lò Gốm Đất Nung", mini boss) sang THIÊN THẠCH THÚ (mã làm việc tinh_hach, rig
monster_3806; ghi chú ArtGen/Spine/inbox/tho9_ghichu.md). Người dùng 2026-11-17 xem lượt 3: "ok cho vào game".

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ (không đổi bản lưu). Hai dạng như cũ; CHƯA có rig dạng 1 nên cả hai trỏ tinh_hach_1 (cỡ
0,92 / 1,1 như cũ). Tên do Claude đặt, người dùng đổi được:
    Cự Phủ -> Thiên Thạch Thú  "Quái thú lưng rừng tinh thể"  dòng "Dòng Thiên Thạch Thú"
    thẻ  Rìu Lửa -> Thiên Thạch Xoáy (hammer -> rock); Cự Phủ Khai Thiên -> Quả Cầu Thiên Thạch (crack, giữ);
         Lửa Chiến -> Rừng Tinh Thể (flame -> star)
Bỏ hẳn hình cũ cu_phu_1 / cu_phu_2 (Resources) sau khi Unity gắn dạng mới vào prefab cu_phu.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (từng khối). Rồi trong Unity: "PokiClash/Nhập dữ liệu", "PokiClash/Tướng/Gắn dạng
.atomik vào prefab tướng", golden. Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_tinh_hach.py [--kiem]      heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_tinh_hach.py chep           chép tinh_hach_1.atomik + chân dung vào Resources/tinh_hach_1/
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doi_phap_lua as D  # noqa: E402

INBOX = os.path.normpath(D.INBOX)
ID = "cu_phu"
TEN = "Thiên Thạch Thú"
CO1, CO2 = 0.92, 1.1
KHAC = [("name", "Cự Phủ", TEN), ("title", "Chiến binh rìu tím", "Quái thú lưng rừng tinh thể"),
        ("line", "Dòng Cự Phủ", "Dòng Thiên Thạch Thú")]
THE = {"cu_phu_skill": ("Rìu Lửa", "Thiên Thạch Xoáy", "hammer", "rock"),
       "cu_phu_ult": ("Cự Phủ Khai Thiên", "Quả Cầu Thiên Thạch", "crack", "crack"),
       "cu_phu_pas": ("Lửa Chiến", "Rừng Tinh Thể", "flame", "star")}


def kiem_ten():
    h = json.load(open(os.path.join(D.DATA, "Json", "heroes.json"), encoding="utf-8"))
    H = h if isinstance(h, list) else h.get("heroes", [])
    ten = {x["name"]: x["id"] for x in H}
    assert ten.get(TEN, ID) == ID, f"tên {TEN} trùng tướng {ten.get(TEN)}"


def dat():
    D.ID, D.KHAC, D.THE = ID, KHAC, THE


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    dat()
    if a[:1] == ["chep"]:
        D.chep("tinh_hach_1", os.path.join(INBOX, "tinh_hach_1", "rig"), "tinh_hach_1.atomik")
    else:
        kiem_ten()
        D.heroes([(TEN, "tinh_hach_1", CO1), (TEN, "tinh_hach_1", CO2)])
        D.cards()
