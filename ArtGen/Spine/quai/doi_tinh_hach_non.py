# -*- coding: utf-8 -*-
"""DẠNG 1 của suất 9 đảo Thổ (id `cu_phu`, ải 60, mini boss) = THIÊN THẠCH THÚ NON (rig tinh_hach_non, ghi chú
ArtGen/Spine/inbox/tinh_hach_non_ghichu.md). Người dùng 2026-11-18 xem rig + tiến hoá: "cho vào game đi".

    dạng 1  Thiên Thạch Thú Non  (tinh_hach_non, 0,92) = bản gộp tiến hoá rig/tinh_hach_non_th.atomik (mang dạng 2 bản nhẹ, clip evolve)
    dạng 2  Thiên Thạch Thú      (tinh_hach_1, 1,1)    = như cũ

Trước đây hai dạng cùng trỏ tinh_hach_1. Tên "Thiên Thạch Thú Non" do Claude đặt tạm, người dùng đổi được. Ải 60 đã có "evo": true (tướng
vốn hai dạng) nên không sửa stages.json. Hiệu ứng theo dạng: StageView.ThoFx cu_phu (n_thach_xoay1 / n_thach_cau1, HatThach.cs ThtD1).

Sửa `Assets/02 Data/Json/heroes.json` (forms, aola / size chung = dạng 1), chép `.atomik` + chân dung vào
`Assets/03 Art/Heroes/Resources/tinh_hach_non/`. Rồi trong Unity: "PokiClash/Nhập dữ liệu", "PokiClash/Tướng/Gắn dạng .atomik vào prefab
tướng", golden (không đổi: chỉ đổi hình). Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_tinh_hach_non.py [--kiem]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doi_phap_lua as D  # noqa: E402

ID = "cu_phu"
TEN, TEN_NON = "Thiên Thạch Thú", "Thiên Thạch Thú Non"
CO1, CO2 = 0.92, 1.1
RIG = os.path.join(os.path.normpath(D.INBOX), "tinh_hach_non", "rig")

if __name__ == "__main__":
    D.ID, D.KHAC, D.THE = ID, [], {}
    D.heroes([(TEN_NON, "tinh_hach_non", CO1), (TEN, "tinh_hach_1", CO2)])
    if not D.KIEM:
        D.chep("tinh_hach_non", RIG, "tinh_hach_non_th.atomik")
