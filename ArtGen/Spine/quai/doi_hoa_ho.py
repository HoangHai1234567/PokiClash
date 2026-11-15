# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 9 đảo Hỏa (id `hoa_tinh`, ải 60 của đảo, "Hang Hồng Ngọc") sang hổ lửa (mã làm việc hoa_ho, rig monster_3645;
người dùng 2026-11-14 chốt concept A, rồi "Ok cho vào game rồi làm dạng 1").

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, số dạng (2) nên không đổi bản lưu. Đổi:
    tên     Hỏa Tinh -> Bạch Viêm Hổ; danh hiệu "Bạch hổ cưỡi mây lửa"; dòng "Dòng Bạch Viêm Hổ"
    dạng    [Tiểu Hỏa Tinh, Hỏa Tinh] (hoa_tinh_1, hoa_tinh_2) -> hai dạng. Chưa có rig dạng 1: cả hai trỏ hoa_ho_1 (cỡ 0,8 / 0,95).
            Có rig dạng 1 thì chạy `dang_1`: dạng 1 "Viêm Hổ Nhi" -> hoa_ho_non (cỡ CO_NON)
    thẻ     Gai Hồng Ngọc -> Hổ Gầm Chấn Viêm (rock -> fang); Sao Hỏa Rơi -> Ảnh Trảo Liên Hoàn (sun -> claw);
            Giáp Hồng Ngọc -> Mây Lửa Hộ Thân (shield giữ)
Tên do Claude đặt (người dùng chưa đặt), người dùng có thể đổi. Không đè, không xoá thư mục Resources/hoa_tinh_* cũ.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng", rồi các menu golden. Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_hoa_ho.py [--kiem]
    py -3 -I ArtGen/Spine/quai/doi_hoa_ho.py chep              chép rig/hoa_ho_1.atomik + chân dung vào Resources/hoa_ho_1/ (thư mục mới)
    py -3 -I ArtGen/Spine/quai/doi_hoa_ho.py dang_1 [--kiem]   dạng 1 -> hoa_ho_non (sau khi có Resources/hoa_ho_non)
    py -3 -I ArtGen/Spine/quai/doi_hoa_ho.py chep_non [thư mục rig dạng 1]   chép hoa_ho_non.atomik + chan_dung.png vào Resources/hoa_ho_non/
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doi_phap_lua as D  # noqa: E402  (dùng lại khoi_tuong, dat_dang, heroes, cards, chep)

D.ID = "hoa_tinh"
TEN, TEN_NON = "Bạch Viêm Hổ", "Viêm Hổ Nhi"
CO_NON, CO_LON = 0.9, 0.95      # 2026-11-14: 1,1 thì hổ lớn (thân dài) tràn mép phải sân; soi trong trận rồi hạ; bản chibi (đầu to, chiều cao khai 1110) ở 0,8 thì bé quá nên 0,9
D.KHAC = [("name", "Hỏa Tinh", TEN), ("title", "Thú giáp lửa hồng", "Bạch hổ cưỡi mây lửa"), ("line", "Dòng Hỏa Tinh", "Dòng Bạch Viêm Hổ")]
D.THE = {"hoa_tinh_skill": ("Gai Hồng Ngọc", "Hổ Gầm Chấn Viêm", "rock", "fang"),
         "hoa_tinh_ult": ("Sao Hỏa Rơi", "Ảnh Trảo Liên Hoàn", "sun", "claw"),
         "hoa_tinh_pas": ("Giáp Hồng Ngọc", "Mây Lửa Hộ Thân", "shield", "shield")}
INBOX = D.INBOX

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[:1] == ["chep"]:
        D.chep("hoa_ho_1", os.path.join(INBOX, "hoa_ho_1", "rig"), "hoa_ho_1.atomik")
    elif a[:1] == ["chep_non"]:
        D.chep("hoa_ho_non", os.path.abspath(a[1]) if len(a) > 1 else os.path.join(INBOX, "hoa_ho_non", "rig"), "hoa_ho_non.atomik")
    elif a[:1] == ["dang_1"]:
        D.heroes([(TEN_NON, "hoa_ho_non", CO_NON), (TEN, "hoa_ho_1", CO_LON)])
    else:
        D.heroes([(TEN, "hoa_ho_1", 0.8), (TEN, "hoa_ho_1", CO_LON)])
        D.cards()
