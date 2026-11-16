# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 2 đảo Kim (id `doc_giac`, ải 5) sang chiến binh sắt khiên giáo (mã làm việc chien_sat; rig monster_3348; dạng 1 →
`chien_sat_1` (rig inbox/chien_sat_1/rig/chien_sat.atomik, đã gộp dạng 2 + clip evolve), dạng 2 → `chien_sat_2`; ghi chú
ArtGen/Spine/inbox/chien_sat_ghichu.md). Người dùng 2026-11-16: duyệt dạng 1 (concept A), dạng 2 (concept B), "ok cho vào game đi".

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ (không đổi bản lưu). SỐ DẠNG 1 → 2 nên stages (ải tướng có evo), golden roster, sim phải tính lại
trong Unity. Đổi:
    tên     Độc Giác Thép -> Thiết Vệ; danh hiệu "Chiến binh sắt khiên giáo"; dòng "Dòng Thiết Vệ"
    dạng    [Độc Giác Thép] (doc_giac_1) -> [Thiết Vệ Nhi (chien_sat_1, cỡ 0,92), Thiết Vệ (chien_sat_2, cỡ 1,1)]
    thẻ     Sừng Bạc -> Phóng Giáo (crack -> trident); Phi Mã Xung Trận -> Vạn Kim Sắt (wing -> fang); Giáp Kỵ -> Khiên Thép (helmet -> shield)
Tên do Claude đặt (người dùng chưa đặt), người dùng có thể đổi. Không đè, không xoá thư mục Resources/doc_giac_1 cũ.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng", rồi sinh lại ải + các menu golden. Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_chien_sat.py [--kiem]   heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_chien_sat.py chep        chép rig + chân dung vào Resources/chien_sat_1/, Resources/chien_sat_2/
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doi_phap_lua as D  # noqa: E402  (dùng lại khoi_tuong, dat_dang, heroes, cards, chep)

D.ID = "doc_giac"
TEN, TEN_NON = "Thiết Vệ", "Thiết Vệ Nhi"
CO_1, CO_2 = 0.92, 1.1
D.KHAC = [("name", "Độc Giác Thép", TEN), ("title", "Ngựa một sừng giáp bạc", "Chiến binh sắt khiên giáo"),
          ("line", "Dòng Độc Giác Thép", "Dòng Thiết Vệ")]
D.THE = {"doc_giac_skill": ("Sừng Bạc", "Phóng Giáo", "crack", "trident"),
         "doc_giac_ult": ("Phi Mã Xung Trận", "Vạn Kim Sắt", "wing", "fang"),
         "doc_giac_pas": ("Giáp Kỵ", "Khiên Thép", "helmet", "shield")}
INBOX = os.path.normpath(D.INBOX)
RIG1 = os.path.join(INBOX, "chien_sat_1", "rig")
RIG2 = os.path.join(INBOX, "chien_sat_2", "rig")

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[:1] == ["chep"]:
        D.chep("chien_sat_1", RIG1, "chien_sat.atomik")
        D.chep("chien_sat_2", RIG2, "chien_sat_2.atomik")
    else:
        D.heroes([(TEN_NON, "chien_sat_1", CO_1), (TEN, "chien_sat_2", CO_2)])
        D.cards()
