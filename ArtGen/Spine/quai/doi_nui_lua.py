# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 10 đảo Hỏa (id `lan_hoa`, boss ải 70 "Miệng Núi Lửa") sang khủng long núi lửa (mã làm việc nui_lua, rig monster_3654;
người dùng 2026-11-14 chốt concept "sừng" cho dạng lớn, concept A cho dạng 1; 2026-11-15: "cho vào game đi", rồi "con này cần có dạng 2 nữa").

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, SỐ DẠNG (ba) nên không đổi bản lưu, golden roster không đổi. Đổi:
    tên     Lân Hỏa -> Hỏa Sơn Long; danh hiệu "Khủng long núi lửa hai sừng"; dòng "Dòng Hỏa Sơn Long"
    dạng    [Lân Con, Lân Ngàn Năm, Thánh Lân] (lan_hoa_1..3) -> [Hỏa Sơn Nhi (nui_lua_non), Hỏa Sơn Thú (TẠM trỏ nui_lua_1 cỡ nhỏ: rig
            dạng 2 đang làm, có thì chạy `dang_2`), Hỏa Sơn Long (nui_lua_1)]
    thẻ     Lân Hống -> Hỏa Cầu Phún Viêm (bell -> flame); Thánh Lân Giáng Phúc -> Vạn Viêm Truy Kích (crown -> sun);
            Phúc Khí Ngàn Năm -> Lõi Dung Nham (incense -> torch); thẻ boss Thánh Lân Hộ Thể -> Giáp Bazan (incense -> shield)
Tên do Claude đặt (người dùng chưa đặt, đã hỏi hai lần), người dùng có thể đổi. Không đè, không xoá thư mục Resources/lan_hoa_* cũ.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng", rồi các menu golden. Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_nui_lua.py [--kiem]
    py -3 -I ArtGen/Spine/quai/doi_nui_lua.py chep             chép rig hai dạng + chân dung vào Resources/nui_lua_1/, Resources/nui_lua_non/
    py -3 -I ArtGen/Spine/quai/doi_nui_lua.py dang_2 [--kiem]  dạng 2 -> nui_lua_2 (sau khi có Resources/nui_lua_2; `chep_2` chép rig đó)
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doi_phap_lua as D  # noqa: E402  (dùng lại khoi_tuong, dat_dang, heroes, cards, chep)

D.ID = "lan_hoa"
TEN, TEN_2, TEN_NON = "Hỏa Sơn Long", "Hỏa Sơn Thú", "Hỏa Sơn Nhi"
CO_NON, CO_2, CO_LON = 0.85, 0.86, 0.92      # 2026-11-15, soi trong trận: 1,05 thì dạng lớn (thân rộng hơn cao, thêm khói) tràn mép phải sân
D.KHAC = [("name", "Lân Hỏa", TEN), ("title", "Thần thú ngàn năm", "Khủng long núi lửa hai sừng"), ("line", "Dòng Lân Hỏa", "Dòng Hỏa Sơn Long")]
D.THE = {"lan_hoa_skill": ("Lân Hống", "Hỏa Cầu Phún Viêm", "bell", "flame"),
         "lan_hoa_ult": ("Thánh Lân Giáng Phúc", "Vạn Viêm Truy Kích", "crown", "sun"),
         "lan_hoa_pas": ("Phúc Khí Ngàn Năm", "Lõi Dung Nham", "incense", "torch"),
         "lan_hoa_boss": ("Thánh Lân Hộ Thể", "Giáp Bazan", "incense", "shield")}
INBOX = D.INBOX

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[:1] == ["chep"]:
        D.chep("nui_lua_1", os.path.join(INBOX, "nui_lua_1", "rig"), "nui_lua_1.atomik")
        D.chep("nui_lua_non", os.path.join(INBOX, "nui_lua_non", "rig"), "nui_lua_non.atomik")
    elif a[:1] == ["chep_2"]:
        D.chep("nui_lua_2", os.path.join(INBOX, "nui_lua_2", "rig"), "nui_lua_2.atomik")
    elif a[:1] == ["dang_2"]:
        D.heroes([(TEN_NON, "nui_lua_non", CO_NON), (TEN_2, "nui_lua_2", CO_2), (TEN, "nui_lua_1", CO_LON)])
    else:
        D.heroes([(TEN_NON, "nui_lua_non", CO_NON), (TEN_2, "nui_lua_1", CO_2), (TEN, "nui_lua_1", CO_LON)])
        D.cards()
