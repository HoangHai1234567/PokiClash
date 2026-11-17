# -*- coding: utf-8 -*-
"""Đổi HÌNH năm suất đầu đảo Thổ (ải 1 / 5 / 10 / 15 / 20) sang năm tướng vẽ lại trên rig Sword x Staff (ghi chú
ArtGen/Spine/inbox/tho5_ghichu.md). Người dùng 2026-11-17: chọn concept "1C 2D 3D 4D 5C", duyệt rig, "cho vào game đi".

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ (không đổi bản lưu). SỐ DẠNG 3 → 2 (như các suất Hỏa, Kim đã đổi hình): mỗi tướng mới có
một rig, hai dạng cùng trỏ rig đó, cỡ lớn dần theo ải. Tên do Claude đặt, người dùng có thể đổi:
    thach_nhan  Thạch Nhân -> Thạch Giáp  "Tatu mai đá hổ phách"        rig cong_da_1
    lung_vuong  Lửng Vương -> Sa Tích     "Thằn lằn áo choàng đất nung"  rig than_lan_cat_1
    cao_da      Cáo Đá     -> Tê Thiềm    "Cóc tê giác đất nung"         rig thu_da_1
    ho_khoan    Hổ Khoan   -> Sa Long     "Rồng giáp sa thạch"           rig rong_cat_1
    phu_van     Phù Văn    -> Sơn Viên    "Vượn núi đá bốn tay"          rig quy_nui_1
Thẻ đổi tên, biểu tượng theo chiêu mới (hiệu ứng giữ nguyên). Hình cũ (Resources/<id>_1..3) không xoá ở đây.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn), từng khối (các phiên khác cũng sửa hai file này). Rồi trong Unity:
"PokiClash/Nhập dữ liệu", "PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng", các menu golden. Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_tho5.py [--kiem]   heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_tho5.py chep        chép <mã>.atomik + chân dung vào Resources/<mã>/ (thư mục mới)
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doi_phap_lua as D  # noqa: E402  (dùng lại khoi_tuong, dat_dang, heroes, cards, chep)

INBOX = os.path.normpath(D.INBOX)
# id: (tên cũ, tên mới, danh hiệu cũ, danh hiệu mới, mã rig, cỡ dạng 1, cỡ dạng 2, thẻ {id thẻ: (tên cũ, tên mới, icon cũ, icon mới)})
TUONG = {
    "thach_nhan": ("Thạch Nhân", "Thạch Giáp", "Núi đá biết đi", "Tatu mai đá hổ phách", "cong_da_1", 0.88, 1.0,
                   {"thach_nhan_skill": ("Ném Đá", "Văng Sỏi", "rock", "rock"),
                    "thach_nhan_ult": ("Núi Lở", "Mưa Hổ Phách", "crack", "star"),
                    "thach_nhan_pas": ("Da Đá", "Mai Đá", "helmet", "shield")}),
    "lung_vuong": ("Lửng Vương", "Sa Tích", "Vua lửng vuốt vàng", "Thằn lằn áo choàng đất nung", "than_lan_cat_1", 0.9, 1.04,
                   {"lung_vuong_skill": ("Vuốt Vàng", "Phiến Gốm Bay", "claw", "feather"),
                    "lung_vuong_ult": ("Lửng Vương Cào Xé", "Lốc Cát", "fang", "wind"),
                    "lung_vuong_pas": ("Da Dày", "Áo Phiến Gốm", "helmet", "shield")}),
    "cao_da": ("Cáo Đá", "Tê Thiềm", "Vuốt đá lục bảo", "Cóc tê giác đất nung", "thu_da_1", 0.92, 1.08,
               {"cao_da_skill": ("Vuốt Đá Lục", "Phun Đá", "claw", "rock"),
                "cao_da_ult": ("Lở Đá Ngọc", "Lăn Nện", "crack", "wheel"),
                "cao_da_pas": ("Mắt Pha Lê", "Sừng Đá", "eye", "fang")}),
    "ho_khoan": ("Hổ Khoan", "Sa Long", "Sừng khoan pha lê", "Rồng giáp sa thạch", "rong_cat_1", 0.94, 1.1,
                 {"ho_khoan_skill": ("Sừng Khoan", "Lưỡi Cát", "crack", "claw"),
                  "ho_khoan_ult": ("Pháo Hoa Pha Lê", "Cột Sa Thạch", "bolt", "crack"),
                  "ho_khoan_pas": ("Gai Pha Lê", "Giáp Gai", "mirror", "mirror")}),
    "phu_van": ("Phù Văn", "Sơn Viên", "Khổng lồ đá khắc chữ", "Vượn núi đá bốn tay", "quy_nui_1", 0.96, 1.14,
                {"phu_van_skill": ("Ấn Phù Văn", "Chấn Địa", "rock", "fist"),
                 "phu_van_ult": ("Cự Thần Giáng Thế", "Cự Thạch", "hammer", "rock"),
                 "phu_van_pas": ("Thân Đá Khắc", "Da Đá Núi", "helmet", "helmet")}),
}


def kiem_ten():
    """tên mới không trùng tên tướng khác."""
    h = json.load(open(os.path.join(D.DATA, "Json", "heroes.json"), encoding="utf-8"))
    H = h if isinstance(h, list) else h.get("heroes", [])
    ten = {x["name"]: x["id"] for x in H}
    for hid, v in TUONG.items():
        assert ten.get(v[1], hid) == hid, f"tên {v[1]} trùng tướng {ten.get(v[1])}"


def doi():
    kiem_ten()
    for hid, (ten0, ten, dh0, dh, rig, co1, co2, the) in TUONG.items():
        D.ID = hid
        D.KHAC = [("name", ten0, ten), ("title", dh0, dh), ("line", f"Dòng {ten0}", f"Dòng {ten}")]
        D.THE = the
        D.heroes([(ten, rig, co1), (ten, rig, co2)])
        D.cards()


def chep():
    for hid, v in TUONG.items():
        ma = v[4]
        D.chep(ma, os.path.join(INBOX, ma, "rig"), f"{ma}.atomik")


if __name__ == "__main__":
    D.KIEM = "--kiem" in sys.argv
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[:1] == ["chep"]:
        chep()
    else:
        doi()
