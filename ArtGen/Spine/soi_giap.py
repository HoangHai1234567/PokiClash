# -*- coding: utf-8 -*-
"""Sói giáp sắt đảo Kim (mã làm việc soi_giap; con gốc của rig: monster_3428, sói to cơ bắp đội mũ giáp gỗ sừng cong, khiên gỗ lớn, búa
gỗ đai sắt, game tham khảo; DO NGƯỜI DÙNG CHỈ 2026-11-16). Tướng thứ 6 đảo Kim (suất ải 30, id game hiện là chien_than).

Người dùng 2026-11-16: concept sói humanoid mặc giáp sắt, cầm khiên sắt và búa sắt; appear nhặt khiên lên và gầm; idle / walk giống con
gốc; đánh thường lao lên dùng búa gõ đối thủ; chiêu mana ném búa vào đối thủ; chiêu cuối vào tư thế che khiên rồi charge nhanh xé gió tới
đối thủ húc mạnh, thêm FX; die giống con gốc.
(Lượt đầu Claude tự chọn monster_3263 khi người dùng chưa chỉ; người dùng chỉ lại 3428. Bản cũ cất ở inbox/soi_giap_bo3263/.)
Con gốc nhìn sang PHẢI. Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

Dùng lại các hàm mổ của hoa_ho.py (cùng định dạng quét), chỉ đổi con và bảng nhóm.

    soi_giap.py mo [att json] [tên ra] [S]   tờ MỔ từng part ở một dáng → <SXS>/scan/monster_3428/mo/<tên>_<k>.jpg + bảng
    soi_giap.py nhom [att json] [tên ra]      cả con tô màu theo NHÓM part + viền từng part → mo/nhom_<tên>.jpg
    soi_giap.py part_goc                      ảnh từng part cắt theo lưới → <SXS>/scan/monster_3428/parts/ + tờ tổng (chỉ để xem)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hoa_ho as H  # noqa: E402

CODE = "soi_giap"
MON = "monster_3428"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")

# nhóm part theo tên slot của họ (cái đầu tiên khớp thì lấy)
NHOM = [
    ("dau", r"^P_tou|^P_yanjin|^P_erduo", (235, 235, 235)),       # tou = đầu, yanjin = mắt, erduo = tai
    ("mu_sung", r"^P_toushi", (160, 110, 70)),                    # toushi = đồ trên đầu (mũ, sừng, tinh thể)
    ("khien", r"^W_dunpai", (120, 140, 250)),                     # khiên
    ("bua", r"^W_futou", (90, 220, 230)),                         # vũ khí: búa (futou)
    ("giap", r"^P_jianjia|^P_diaozhui", (200, 120, 220)),         # giáp vai, mảnh treo (diaozhui)
    ("tay", r"^P_shou", (250, 190, 110)),                         # shouL / shouR = tay
    ("chan", r"^P_tui", (90, 200, 190)),                          # tuiL / tuiR = chân
    ("than", r"^P_shenti|^P_yaodai|^P_xianglian", (255, 230, 60)),  # thân, đai / vạt, vòng cổ (xianglian)
    ("duoi", r"^P_weiba", (250, 120, 120)),                       # đuôi
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
