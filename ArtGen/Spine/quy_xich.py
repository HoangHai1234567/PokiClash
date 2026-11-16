# -*- coding: utf-8 -*-
"""Quỷ béo mặc giáp, vũ khí móc nối xích sắt (mã làm việc quy_xich; con gốc của rig: monster_3408, quỷ béo tím có cánh dơi, mũ giáp sẫm,
sừng, đuôi mũi tên, xích quấn ngực có ổ khoá đồng, tay cầm móc neo nối xích; game tham khảo). Tướng thứ 5 đảo Kim (ải 20 "Gác Chuông Đồng",
id game hiện là khien_bac).

Người dùng 2026-11-16: concept quỷ béo mặc giáp, vũ khí là móc liền gắn với xích sắt; idle / walk làm giống con gốc; appear bay vào rồi rơi
xuống; đánh thường bay tới dùng móc gõ vào đầu đối thủ; chiêu mana giống skill_01 (quay xích ném đối thủ); chiêu cuối xích bốc lửa, xoay xích
tạo vệt lửa và khói, ném trói đối thủ rồi thiêu đốt, thêm FX / animation một cột lửa rất to thiêu cháy đối thủ.
Con gốc nhìn sang PHẢI. Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

Dùng lại các hàm mổ của hoa_ho.py (cùng định dạng quét), chỉ đổi con và bảng nhóm.

    quy_xich.py mo [att json] [tên ra] [S]   tờ MỔ từng part ở một dáng → <SXS>/scan/monster_3408/mo/<tên>_<k>.jpg + bảng
    quy_xich.py nhom [att json] [tên ra]      cả con tô màu theo NHÓM part + viền từng part → mo/nhom_<tên>.jpg
    quy_xich.py part_goc                      ảnh từng part cắt theo lưới → <SXS>/scan/monster_3408/parts/ + tờ tổng (chỉ để xem)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hoa_ho as H  # noqa: E402

CODE = "quy_xich"
MON = "monster_3408"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")

# nhóm part theo tên slot của họ (cái đầu tiên khớp thì lấy)
NHOM = [
    ("mu_dau", r"^P_tou|^P_jiao", (235, 235, 235)),            # tou = đầu, toukui = mũ giáp, jiao = sừng
    ("canh", r"^P_chibang", (200, 120, 220)),                  # chibang = cánh
    ("vu_khi", r"^W_wuqi", (90, 220, 230)),                    # wuqi = vũ khí: móc
    ("xich", r"suolian|^W_s[AB]|^xian", (160, 160, 175)),      # suolian = xích (tay + quấn ngực), xian = đường cong dẫn xích
    ("khoa", r"^P_suo$", (250, 210, 90)),                      # suo = ổ khoá đồng trên ngực
    ("giap", r"^P_jianjia|^P_xiongjia|^P_jiejing", (255, 120, 80)),  # giáp vai, giáp ngực, tinh thể / gai giáp
    ("tay", r"^P_shou", (250, 190, 110)),                      # shou = tay
    ("chan", r"^P_tui", (90, 200, 190)),                       # tui = chân
    ("than", r"^P_duzi|^P_xionqiang|^P_bozi|^P_weiba", (255, 230, 60)),  # bụng, ngực, cổ, đuôi
]

H.CODE, H.MON, H.BASE, H.MAU, H.TAI, H.NHOM = CODE, MON, BASE, MAU, TAI, NHOM
sxs, scan, rig_goc, nap, luoi, part_goc, nhom_cua, _C = H.sxs, H.scan, H.rig_goc, H.nap, H.luoi, H.part_goc, H.nhom_cua, H._C

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "mo":
        H.mo(*sys.argv[2:5])
    elif cmd == "nhom":
        H.nhom(*sys.argv[2:6])
    elif cmd == "part_goc":
        H.part_het()
    else:
        print(__doc__)
