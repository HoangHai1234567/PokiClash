# -*- coding: utf-8 -*-
"""Sửa nhầm suất (người dùng 2026-11-19): Cổ Vương (tượng vua cổ rễ quấn cầm cột, ghi chú ArtGen/Spine/inbox/tuong_cot_ghichu.md) là
tướng thứ 6 đảo THỔ, không phải đảo Mộc. Ngày 2026-11-17 nó bị ghép đè lên suất 6 đảo Mộc (`gio_loc`, Linh Điểu). Script này làm hai việc:

    gio_loc (đảo Mộc, ải 30 "Thung Lũng Lá")  Cổ Vương -> Linh Điểu như trước 2026-11-17 (doi_linh_dieu.py): tên, danh hiệu, dòng, cỡ,
                                              hai dạng Điểu Nhi / Linh Điểu, tên + biểu tượng 4 thẻ (gồm bị động boss Gió Cuốn).
    hat_de  (đảo Thổ, ải 30)                  Hạt Dẻ -> Cổ Vương: dạng Cổ Vương Nhi (hat_de_1 = tuong_cot_non_th.atomik) / Cổ Vương
                                              (hat_de_2 = tuong_cot_1.atomik). Giữ id tướng, id thẻ, chỉ số, HIỆU ỨNG thẻ của suất (độ khó ải
                                              30 đảo Thổ và golden không đổi); đổi tên thẻ (Claude đặt, người dùng: "tên bạn tự quyết").

Không đụng thẻ chung `hat_de` (thẻ hồi máu trong kho thẻ, không thuộc tướng). Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_suat6_tho.py [--kiem]     heroes.json, cards.json
    py -3 -I ArtGen/Spine/quai/doi_suat6_tho.py chep         chép .atomik + chân dung vào Resources/hat_de_1, hat_de_2, gio_loc_1, gio_loc_2
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doi_phap_lua as D  # noqa: E402

INBOX = os.path.normpath(D.INBOX)

LINH_DIEU = dict(
    ID="gio_loc",
    KHAC=[("name", "Cổ Vương", "Linh Điểu"), ("title", "Tượng vua cổ cầm trụ", "Chim thần giữ rừng"), ("line", "Dòng Cổ Vương", "Dòng Linh Điểu")],
    THE={"gio_loc_skill": ("Rễ Trói Đất", "Lông Lá Găm", "seed", "leaf"),
         "gio_loc_ult": ("Thần Trụ Giáng Thế", "Thiên Thạch Giáng", "rock", "rock"),
         "gio_loc_pas": ("Thân Đá Rời", "Cánh Lá Nhẹ", "shield", "wing"),
         "gio_loc_boss": ("Rễ Hút Linh Lực", "Gió Cuốn", "leaf", "wind")},
    DANG=[("Điểu Nhi", "gio_loc_1", 0.92), ("Linh Điểu", "gio_loc_2", 1.1)],
)

CO_VUONG = dict(
    ID="hat_de",
    KHAC=[("name", "Hạt Dẻ", "Cổ Vương"), ("title", "Dũng sĩ khiên hạt dẻ", "Tượng vua cổ cầm trụ"), ("line", "Dòng Hạt Dẻ", "Dòng Cổ Vương")],
    # hiệu ứng giữ của suất: chiêu mana 2 nhát, chiêu cuối 3 nhát, bị động và bị động boss là khiên khi trúng đòn
    THE={"hat_de_skill": ("Ném Hạt Dẻ", "Rễ Trói Đất", "seed", "seed"),
         "hat_de_ult": ("Mưa Hạt Dẻ", "Thần Trụ Giáng Thế", "rock", "rock"),
         "hat_de_pas": ("Khiên Vỏ Cứng", "Giáp Đá Cổ", "shield", "shield"),
         "hat_de_boss": ("Vỏ Dẻ Hộ Thân", "Rễ Đá Hộ Thân", "shield", "rock")},
    DANG=[("Cổ Vương Nhi", "hat_de_1", 0.88), ("Cổ Vương", "hat_de_2", 1.1)],
)

# Resources/<dạng> <- (thư mục rig trong inbox, tên .atomik)
CHEP = {"hat_de_1": ("tuong_cot_non_1", "tuong_cot_non_th.atomik"), "hat_de_2": ("tuong_cot_1", "tuong_cot_1.atomik"),
        "gio_loc_1": ("chim_la_non", "chim_la_non.atomik"), "gio_loc_2": ("chim_la_1", "chim_la_1.atomik")}


def du_lieu():
    for s in (LINH_DIEU, CO_VUONG):
        D.ID, D.KHAC, D.THE = s["ID"], s["KHAC"], s["THE"]
        D.heroes(s["DANG"])
        D.cards()


def chep():
    for dich, (thu_muc, ten) in CHEP.items():
        D.chep(dich, os.path.join(INBOX, thu_muc, "rig"), ten)


if __name__ == "__main__":
    D.KIEM = "--kiem" in sys.argv
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[:1] == ["chep"]:
        chep()
    else:
        du_lieu()
