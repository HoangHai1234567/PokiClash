# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 7 đảo Thổ (id `rua_nui`, ải 40 "Ruộng Bậc Thang") sang SÂU CÁT KHỔNG LỒ (mã làm việc sau_dat, rig monster_3643; ghi chú
ArtGen/Spine/inbox/sau_dat_ghichu.md). Người dùng 2026-11-17: "cho vào game, tạo thêm fx nếu cần rồi làm dạng 1 của tướng này".

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ (không đổi bản lưu). Hai dạng; CHƯA có rig dạng 1 nên cả hai trỏ sau_dat_1 (cỡ 0,92 / 1,1 như
cũ); có rig dạng 1 thì `dang_1` đổi dạng 1 sang sau_dat_non (rồi gộp clip tiến hoá như doi_tho5_dang2.py). Tên do Claude đặt, người dùng đổi
được:
    Rùa Núi -> Sa Trùng  "Sâu cát khổng lồ"  dòng "Dòng Sa Trùng"; dạng 1 "Sa Trùng Nhi"
    thẻ  Núi Đè -> Gai Ngầm (rock -> crack); Sơn Lâm Hộ Thể -> Miệng Sa Mạc (crack -> fang); Rừng Trên Mai -> Giáp Vòng Đốt (leaf -> shield)
Hiệu ứng: HatTho.cs (n_trung_dop / n_trung_gai / n_trung_mieng), StageView.ThoFx / ThoAtk.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (từng khối). Rồi trong Unity: "PokiClash/Nhập dữ liệu", "PokiClash/Tướng/Gắn dạng
.atomik vào prefab tướng", golden. Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_sau_dat.py [--kiem]      heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_sau_dat.py chep           chép sau_dat_1.atomik + chân dung vào Resources/sau_dat_1/
    py -3 -I ArtGen/Spine/quai/doi_sau_dat.py dang_1 [--kiem] gộp clip tiến hoá vào rig dạng 1 (sau_dat_non_th), chép sau_dat_non +
                                                            sau_dat_1 vào Resources, dạng 1 -> sau_dat_non
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doi_phap_lua as D  # noqa: E402

INBOX = os.path.normpath(D.INBOX)
ID = "rua_nui"
TEN, TEN_NON = "Sa Trùng", "Sa Trùng Nhi"
CO1, CO2, CO_NON = 0.92, 1.1, 0.85
KHAC = [("name", "Rùa Núi", TEN), ("title", "Mai núi rừng xanh", "Sâu cát khổng lồ"), ("line", "Dòng Rùa Núi", "Dòng Sa Trùng")]
THE = {"rua_nui_skill": ("Núi Đè", "Gai Ngầm", "rock", "crack"),
       "rua_nui_ult": ("Sơn Lâm Hộ Thể", "Miệng Sa Mạc", "crack", "fang"),
       "rua_nui_pas": ("Rừng Trên Mai", "Giáp Vòng Đốt", "leaf", "shield")}


def kiem_ten():
    h = json.load(open(os.path.join(D.DATA, "Json", "heroes.json"), encoding="utf-8"))
    H = h if isinstance(h, list) else h.get("heroes", [])
    ten = {x["name"]: x["id"] for x in H}
    for t in (TEN,):
        assert ten.get(t, ID) == ID, f"tên {t} trùng tướng {ten.get(t)}"


def dat():
    D.ID, D.KHAC, D.THE = ID, KHAC, THE


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    dat()
    if a[:1] == ["chep"]:
        D.chep("sau_dat_1", os.path.join(INBOX, "sau_dat_1", "rig"), "sau_dat_1.atomik")
    elif a[:1] == ["dang_1"]:
        # rig dạng 1 (sau_dat_non, concept B 2026-11-17) + clip tiến hoá như doi_tho5_dang2.th → Resources/sau_dat_non (bản _th)
        import doi_tho5_dang2 as T2
        T2.TUONG2[ID] = ("sau_dat_non", "sau_dat_1", TEN, CO_NON, CO2)
        T2.th(ID)
        T2.chep(ID)
        D.heroes([(TEN_NON, "sau_dat_non", CO_NON), (TEN, "sau_dat_1", CO2)])
    else:
        kiem_ten()
        D.heroes([(TEN_NON, "sau_dat_1", CO1), (TEN, "sau_dat_1", CO2)])
        D.cards()
