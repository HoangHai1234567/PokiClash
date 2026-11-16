# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 4 đảo Kim (id `phi_thuong`, ải 15 "Tháp Canh Thép") sang tinh linh đuôi máy cưa (mã làm việc cua_xich; rig monster_3374;
rig inbox/cua_xich_1/rig/cua_xich.atomik; ghi chú ArtGen/Spine/inbox/cua_xich_ghichu.md). Người dùng 2026-11-16: "ok cho vào game".

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, số mảnh, SỐ DẠNG (2: chưa có rig dạng non nên cả hai dạng trỏ cua_xich_1, cỡ 0,92 / 1,1, như
doi_phap_lua lúc đầu) → stages, golden không đổi. Đổi:
    tên     Phi Thương -> Thiết Cưa; danh hiệu "Tinh linh đuôi máy cưa"; dòng "Dòng Thiết Cưa"
    dạng    [Phi Thương Con (phi_thuong_1), Phi Thương (phi_thuong_2)] -> [Thiết Cưa (cua_xich_1, 0,92), Thiết Cưa (cua_xich_1, 1,1)]
    thẻ     Đâm Thương -> Quật Cưa (trident -> wheel); Mưa Thương -> Cưa Liên Hồi (sword -> crack); Giáp Lam -> Mai Quặng (shield)
Tên do Claude tạm đặt (người dùng chưa đặt), người dùng có thể đổi. Không đè, không xoá thư mục Resources/phi_thuong_* cũ.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng". Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_cua_xich.py [--kiem]   heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_cua_xich.py chep        chép rig + chân dung vào Resources/cua_xich_1/
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doi_phap_lua as D  # noqa: E402  (dùng lại khoi_tuong, dat_dang, heroes, cards, chep)

D.ID = "phi_thuong"
TEN = "Thiết Cưa"
D.KHAC = [("name", "Phi Thương", TEN), ("title", "Kỵ sĩ máy song thương", "Tinh linh đuôi máy cưa"),
          ("line", "Dòng Phi Thương", "Dòng Thiết Cưa")]
D.THE = {"phi_thuong_skill": ("Đâm Thương", "Quật Cưa", "trident", "wheel"),
         "phi_thuong_ult": ("Mưa Thương", "Cưa Liên Hồi", "sword", "crack"),
         "phi_thuong_pas": ("Giáp Lam", "Mai Quặng", "shield", "shield")}
RIG = os.path.join(os.path.normpath(D.INBOX), "cua_xich_1", "rig")

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[:1] == ["chep"]:
        D.chep("cua_xich_1", RIG, "cua_xich.atomik")
    else:
        D.heroes([(TEN, "cua_xich_1", 0.92), (TEN, "cua_xich_1", 1.1)])
        D.cards()
