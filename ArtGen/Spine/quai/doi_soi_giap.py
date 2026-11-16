# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 6 đảo Kim (id `chien_than`, ải 30) sang sói giáp sắt khiên búa (mã làm việc soi_giap, rig gốc monster_3428 của
Sword x Staff; dạng 1 sói con → `soi_giap_1`, dạng 2 sói giáp kín → `soi_giap_2`; ghi chú ArtGen/Spine/inbox/soi_giap_ghichu.md).
Người dùng 2026-11-16: "ok cho vào game và làm các fx cần thiết".

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, SỐ DẠNG (2 → 2): bản lưu và golden không đổi. Đổi:
    tên     Chiến Thần -> Sói Giáp; danh hiệu "Sói chiến binh khiên búa"; dòng "Dòng Sói Giáp"
    dạng    [Chiến Linh Con, Chiến Thần] (chien_than_1, chien_than_2) -> [Sói Giáp Con (soi_giap_1, cỡ 0,86), Sói Giáp (soi_giap_2, cỡ 1,1)]
    thẻ     Pháo Vàng -> Ném Búa Sắt (bolt -> hammer); Chiến Thần Giáng Pháo -> Khiên Xé Gió (hammer -> shield); Giáp Vàng -> Giáp Sắt
Tên do Claude đặt TẠM (người dùng chưa đặt), người dùng đổi thì sửa TEN / KHAC / THE rồi chạy lại. Không đè, không xoá Resources/chien_than_*.

Cỡ dạng 1 = 0,86: rig sói con cao 504 đơn vị, sói lớn 641 (cùng rig 3428) → 0,86 / 1,1 ≈ 504 / 641, hai dạng cùng tỉ lệ điểm ảnh trên sân.
Clip evolve đã gộp sẵn trong soi_giap_non.atomik (soi_giap_rig.py, SG_DANG=non): dạng 2 trong rig gộp co hA / hB, đúng với ô xem tướng
(HeroViewer dựng hai dạng cùng một chiều cao).

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng". Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_soi_giap.py [--kiem]   heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_soi_giap.py chep        chép rig + chân dung vào Resources/soi_giap_1/, Resources/soi_giap_2/
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SPINE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import doi_phap_lua as D  # noqa: E402  (dùng lại khoi_tuong, dat_dang, heroes, cards, chep)

D.ID = "chien_than"
TEN, TEN_NON = "Sói Giáp", "Sói Giáp Con"
CO_1, CO_2 = 0.86, 1.1
D.KHAC = [("name", "Chiến Thần", TEN), ("title", "Pháo thủ giáp vàng", "Sói chiến binh khiên búa"), ("line", "Dòng Chiến Thần", "Dòng Sói Giáp")]
D.THE = {"chien_than_skill": ("Pháo Vàng", "Ném Búa Sắt", "bolt", "hammer"),
         "chien_than_ult": ("Chiến Thần Giáng Pháo", "Khiên Xé Gió", "hammer", "shield"),
         "chien_than_pas": ("Giáp Vàng", "Giáp Sắt", "helmet", "helmet")}
INBOX = os.path.normpath(D.INBOX)
RIG1 = os.path.join(INBOX, "soi_giap_non", "rig")
RIG2 = os.path.join(INBOX, "soi_giap_1", "rig")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[:1] == ["chep"]:
        D.chep("soi_giap_1", RIG1, "soi_giap_non.atomik")
        D.chep("soi_giap_2", RIG2, "soi_giap.atomik")
    else:
        D.heroes([(TEN_NON, "soi_giap_1", CO_1), (TEN, "soi_giap_2", CO_2)])
        D.cards()
