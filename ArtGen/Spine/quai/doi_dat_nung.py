# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 8 đảo Hỏa (id `huyen_viem`, ải 50 của đảo, "Rừng Lửa Ảo") sang chiến binh đất nung lõi dung nham (mã làm việc dat_nung, rig
monster_3625; người dùng 2026-11-14 chốt bản mặt + giáp mới: "Ổn, cho vào game đi rồi làm dạng 1 của tướng này").

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ (không đổi bản lưu). SỐ DẠNG 3 → 2 (như các suất Hỏa khác đã đổi hình) nên golden roster, sim phải
tính lại trong Unity. Đổi:
    tên     Huyễn Viêm -> Viêm Dũng ("dũng" = tượng binh, như binh mã dũng); danh hiệu "Tượng binh đất nung lõi dung nham"; dòng "Dòng Viêm Dũng"
    dạng    [Linh Viêm, Huyễn Viêm, Thánh Huyễn Viêm] (huyen_viem_1..3) -> hai dạng. Chưa có rig dạng 1: cả hai trỏ dat_nung_1 (cỡ 0,92 / 1,1).
            Có rig dạng 1 thì chạy `dang_1`: dạng 1 "Viêm Dũng Nhi" -> dat_nung_non (cỡ CO_NON)
    thẻ     Ảo Hỏa -> Xuyên Tâm Liên Trảm (flame -> crack); Huyễn Viêm Thiên Hỏa -> Ngũ Kiếm Tề Phi (phoenix -> sword);
            Hồ Ảnh -> Lõi Nham Bùng Cháy (mirror -> flame); thẻ boss Ảo Ảnh Hồ Ly -> Giáp Nung Tự Liền (mirror -> shield)
Tên do Claude đặt (người dùng chưa đặt), người dùng có thể đổi. Không đè, không xoá thư mục Resources/huyen_viem_* cũ.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng", rồi các menu golden. Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_dat_nung.py [--kiem]
    py -3 -I ArtGen/Spine/quai/doi_dat_nung.py chep              chép rig_moi/dat_nung_1.atomik + chân dung vào Resources/dat_nung_1/ (thư mục mới)
    py -3 -I ArtGen/Spine/quai/doi_dat_nung.py dang_1 [--kiem]   dạng 1 -> dat_nung_non (sau khi có Resources/dat_nung_non)
    py -3 -I ArtGen/Spine/quai/doi_dat_nung.py chep_non [thư mục rig dạng 1]   chép dat_nung_non_th.atomik (đã gộp clip evolve) + chan_dung.png vào Resources/dat_nung_non/
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doi_phap_lua as D  # noqa: E402  (dùng lại khoi_tuong, dat_dang, heroes, cards, chep)

D.ID = "huyen_viem"
TEN, TEN_NON = "Viêm Dũng", "Viêm Dũng Nhi"
CO_NON, CO_LON = 0.85, 0.95     # 2026-11-14: 1,1 thì thân bè ngang + kiếm chạm mép phải sân (soi ảnh tour trong trận) nên hạ còn 0,95
D.KHAC = [("name", "Huyễn Viêm", TEN), ("title", "Hồ lửa ảo ảnh", "Tượng binh đất nung lõi dung nham"), ("line", "Dòng Huyễn Viêm", "Dòng Viêm Dũng")]
D.THE = {"huyen_viem_skill": ("Ảo Hỏa", "Xuyên Tâm Liên Trảm", "flame", "crack"),
         "huyen_viem_ult": ("Huyễn Viêm Thiên Hỏa", "Ngũ Kiếm Tề Phi", "phoenix", "sword"),
         "huyen_viem_pas": ("Hồ Ảnh", "Lõi Nham Bùng Cháy", "mirror", "flame"),
         "huyen_viem_boss": ("Ảo Ảnh Hồ Ly", "Giáp Nung Tự Liền", "mirror", "shield")}
INBOX = D.INBOX

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[:1] == ["chep"]:
        D.chep("dat_nung_1", os.path.join(INBOX, "dat_nung_1", "rig_moi"), "dat_nung_1.atomik")
    elif a[:1] == ["chep_non"]:
        D.chep("dat_nung_non", os.path.abspath(a[1]) if len(a) > 1 else os.path.join(INBOX, "dat_nung_non", "rig"), "dat_nung_non_th.atomik")
    elif a[:1] == ["dang_1"]:
        D.heroes([(TEN_NON, "dat_nung_non", CO_NON), (TEN, "dat_nung_1", CO_LON)])
    else:
        D.heroes([(TEN, "dat_nung_1", 0.8), (TEN, "dat_nung_1", CO_LON)])
        D.cards()
