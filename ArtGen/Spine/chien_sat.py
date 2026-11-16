# -*- coding: utf-8 -*-
"""Chiến binh sắt đảo Kim (mã làm việc chien_sat; con gốc của rig: monster_3348, hiệp sĩ băng khiên + giáo, game tham khảo). Tướng thứ 2 đảo Kim.

Người dùng 2026-11-16: concept chiến binh sắt, BỎ icon bông tuyết; idle / walk giống con gốc (sửa chút); appear nhảy vào sàn đấu; đánh thường
dùng giáo đâm đối thủ; chiêu mana ném giáo vào người đối thủ; chiêu cuối giơ giáo lên triệu hồi các mũi kim sắt rồi dậm mạnh giáo xuống đất,
các mũi kim lao vào đối thủ (rig chỉ làm động tác người, mũi kim do code); die gục xuống.
Con gốc nhìn sang PHẢI. Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

Dùng lại các hàm mổ của hoa_ho.py (cùng định dạng quét), chỉ đổi con và bảng nhóm.

    chien_sat.py mo [att json] [tên ra] [S]   tờ MỔ từng part ở một dáng → <SXS>/scan/monster_3348/mo/<tên>_<k>.jpg + bảng
    chien_sat.py nhom [att json] [tên ra]      cả con tô màu theo NHÓM part + viền từng part → mo/nhom_<tên>.jpg
    chien_sat.py part_goc                      ảnh từng part cắt theo lưới → <SXS>/scan/monster_3348/parts/ + tờ tổng (chỉ để xem)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hoa_ho as H  # noqa: E402

CODE = "chien_sat"
MON = "monster_3348"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")

# nhóm part theo tên slot của họ (cái đầu tiên khớp thì lấy)
NHOM = [
    ("mu_dau", r"^tou|^guan|^hujing", (235, 235, 235)),       # tou = đầu / mũ, guan = mào (chùm lông), hujing = mặt nạ
    ("khien", r"^dun", (120, 140, 250)),                       # khiên
    ("giao", r"^wuqi", (90, 220, 230)),                        # vũ khí: giáo
    ("co_vai", r"^qizi|^hujian", (200, 120, 220)),             # qizi = cờ / vạt, hujian = giáp vai
    ("tay", r"bi_|^sizhi|^damz", (250, 190, 110)),             # dabi / xiaobi = bắp / cẳng tay, sizhi / damz = ngón, nắm tay
    ("chan", r"tui_", (90, 200, 190)),                         # datui / xiaotui = đùi / ống chân
    ("than", r"^st_|^bozi|^dang|^qunbai", (255, 230, 60)),     # thân, cổ, đũng, vạt váy
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
