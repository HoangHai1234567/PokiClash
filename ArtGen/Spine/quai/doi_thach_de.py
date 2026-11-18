# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 10 đảo Thổ (id `giap_nham`, ải 70 "Kim Tự Viện", final boss) sang THỔ TINH (mã làm việc thach_de, rig monster_3802;
ghi chú ArtGen/Spine/inbox/thach_de_ghichu.md). Người dùng 2026-11-18 xem ba đòn mới: "ok cho vào game đi rồi gen dạng 1 của nó".

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ (không đổi bản lưu, không đổi golden số). Hai dạng như cũ; CHƯA có rig dạng 1 nên cả hai trỏ
thach_de_1 (cỡ 0,92 / 1,1 như cũ). Tên do Claude đặt, người dùng đổi được:
    Giáp Nham -> Thổ Tinh  "Hành tinh đá gọi mặt trời"  dòng "Dòng Thổ Tinh"
    thẻ  Nham Quyền -> Nguyệt Nhận (fist -> moon); Nham Giáp Thiên Băng -> Hằng Tinh Diệt (crack -> sun);
         Bờm Đỏ Chiến Ý -> Vệ Tinh Hộ Thể (rage -> shield); thẻ boss Nham Giáp Chấn Địa -> Lõi Hành Tinh (helmet -> rock)
Bỏ hình cũ giap_nham_1 / giap_nham_2 (Resources) sau khi Unity gắn dạng mới vào prefab giap_nham.

    py -3 -I ArtGen/Spine/quai/doi_thach_de.py [--kiem]      heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_thach_de.py chep           chép thach_de_1.atomik + chân dung vào Resources/thach_de_1/
    py -3 -I ArtGen/Spine/quai/doi_thach_de.py chep_non       chép inbox/thach_de_non/rig/thach_de_non_th.atomik (có clip evolve) + chân dung vào Resources/thach_de_non/
    py -3 -I ArtGen/Spine/quai/doi_thach_de.py dang_1         dạng 1 -> thach_de_non (sau khi có Resources/thach_de_non)
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doi_phap_lua as D  # noqa: E402

INBOX = os.path.normpath(D.INBOX)
ID = "giap_nham"
TEN, TEN_NON = "Thổ Tinh", "Tiểu Thổ Tinh"
CO1, CO2 = 0.92, 1.1
KHAC = [("name", "Giáp Nham", TEN), ("title", "Chiến thần giáp vàng", "Hành tinh đá gọi mặt trời"),
        ("line", "Dòng Giáp Nham", "Dòng Thổ Tinh")]
THE = {"giap_nham_skill": ("Nham Quyền", "Nguyệt Nhận", "fist", "moon"),
       "giap_nham_ult": ("Nham Giáp Thiên Băng", "Hằng Tinh Diệt", "crack", "sun"),
       "giap_nham_pas": ("Bờm Đỏ Chiến Ý", "Vệ Tinh Hộ Thể", "rage", "shield"),
       "giap_nham_boss": ("Nham Giáp Chấn Địa", "Lõi Hành Tinh", "helmet", "rock")}


def kiem_ten():
    h = json.load(open(os.path.join(D.DATA, "Json", "heroes.json"), encoding="utf-8"))
    H = h if isinstance(h, list) else h.get("heroes", [])
    ten = {x["name"]: x["id"] for x in H}
    for t in (TEN, TEN_NON):
        assert ten.get(t, ID) == ID, f"tên {t} trùng tướng {ten.get(t)}"


def dat():
    D.ID, D.KHAC, D.THE = ID, KHAC, THE


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    dat()
    if a[:1] == ["chep"]:
        D.chep("thach_de_1", os.path.join(INBOX, "thach_de_1", "rig"), "thach_de_1.atomik")
    elif a[:1] == ["chep_non"]:
        D.chep("thach_de_non", os.path.abspath(a[1]) if len(a) > 1 else os.path.join(INBOX, "thach_de_non", "rig"), "thach_de_non_th.atomik")
    elif a[:1] == ["dang_1"]:
        D.heroes([(TEN_NON, "thach_de_non", CO1), (TEN, "thach_de_1", CO2)])
    else:
        kiem_ten()
        D.heroes([(TEN, "thach_de_1", CO1), (TEN, "thach_de_1", CO2)])
        D.cards()
