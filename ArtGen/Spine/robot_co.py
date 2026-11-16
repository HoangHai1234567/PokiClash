# -*- coding: utf-8 -*-
"""Robot hủy diệt thời cổ đại (mã làm việc robot_co; con gốc của rig: monster_3613, golem giáp vàng cát có mào đỉnh, mắt đỏ giữa trán,
lõi tròn giữa ngực, giáp vai sừng đen, vạt vải đỏ hoa văn mạch, hai tay dài chống nắm đấm xuống đất; game tham khảo). Tướng thứ 7 đảo Kim
(ải 40, id game hiện là thiet_phu).

Người dùng 2026-11-16: concept robot hủy diệt từ thời cổ đại; appear các bộ phận bay bezier vào; idle / walk làm giống họ; đánh thường giơ
một tay phải lên, tụ một quả cầu năng lượng kiểu dragonball rồi bắn, tay bị giật lại như skill_01; chiêu mana đưa hai tay lên trời, xoay lòng
bàn tay liên tục tụ một quả cầu năng lượng to hơn rồi ném xuống đầu đối thủ, impact lớn, nặng; chiêu cuối giống skill_04, mở mặt ra có lõi tên
lửa lục giác, phóng các tên lửa bay random theo đường cong bezier kiểu homing missile vào đối thủ, impact nặng, nổ lớn.
Con gốc nhìn sang PHẢI. Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

Dùng lại các hàm mổ của hoa_ho.py (cùng định dạng quét), chỉ đổi con và bảng nhóm.

    robot_co.py mo [att json] [tên ra] [S]   tờ MỔ từng part ở một dáng → <SXS>/scan/monster_3613/mo/<tên>_<k>.jpg + bảng
    robot_co.py nhom [att json] [tên ra]      cả con tô màu theo NHÓM part + viền từng part → mo/nhom_<tên>.jpg
    robot_co.py part_goc                      ảnh từng part cắt theo lưới → <SXS>/scan/monster_3613/parts/ + tờ tổng (chỉ để xem)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hoa_ho as H  # noqa: E402

CODE = "robot_co"
MON = "monster_3613"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")

# nhóm part theo tên slot của họ (cái đầu tiên khớp thì lấy)
NHOM = [
    ("dau", r"^P_tou", (235, 235, 235)),                        # tou = đầu
    ("vai", r"^P_jianjia", (200, 120, 220)),                    # jianjia = giáp vai
    ("nguc", r"^P_xiongjia", (255, 120, 80)),                   # xiongjia = giáp ngực
    ("vai_do", r"^P_butiao", (230, 60, 60)),                    # butiao = dải vải
    ("vu_khi", r"^P_wuqi", (90, 220, 230)),                     # wuqi = vũ khí (?)
    ("than", r"^P_shenti", (255, 230, 60)),                     # shenti = thân
    ("ngon_R", r"^P_shouR3", (250, 170, 110)),                  # shou?3 = ngón tay
    ("ngon_L", r"^P_shouL3", (120, 190, 250)),
    ("tay_R", r"^P_shouR", (230, 120, 90)),                     # shouR = tay R
    ("tay_L", r"^P_shouL", (90, 140, 230)),                     # shouL = tay L
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
