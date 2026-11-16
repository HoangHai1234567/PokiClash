# -*- coding: utf-8 -*-
"""Kỵ sĩ cổ đại bị nguyền (mã làm việc ky_nguyen; con gốc của rig: monster_3642, hiệp sĩ giáp trắng viền vàng rỗng ruột, áo choàng tím
rách, tinh thể tím mọc trên giáp, chùm lông vũ trên mũ, kiếm lưỡi mẻ có ngọc lam; game tham khảo). Tướng thứ 8 đảo Kim (ải 50, id game hiện
là tam_kiem).

Người dùng 2026-11-16: concept kỵ sĩ cổ đại bị nguyền rủa bất tử; giáp sắt đen rỉ sét, bên trong là ngọn lửa aura xanh lá tỏa ra. appear:
bộ giáp rỗng nằm dưới đất, mắt sáng xanh rồi lơ lửng thành hình; idle / walk giống họ; đánh thường lao tới chém kiếm; chiêu mana giơ kiếm
lên trời gọi linh hồn đồng đội xưa (linh hồn xanh) lao tới đánh; chiêu cuối đầu giống skill_03_1, tay kia vuốt lên, kiếm cùn hút khí xanh
quanh người, được phục hồi bằng vật chất linh hồn xanh lá thành kiếm hoàn chỉnh rất dài, tỏa aura, chém một phát thật mạnh xuống đối thủ.
Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

Dùng lại các hàm mổ của hoa_ho.py (cùng định dạng quét), chỉ đổi con và bảng nhóm.

    ky_nguyen.py mo [att json] [tên ra] [S]   tờ MỔ từng part ở một dáng → <SXS>/scan/monster_3642/mo/<tên>_<k>.jpg + bảng
    ky_nguyen.py nhom [att json] [tên ra]      cả con tô màu theo NHÓM part + viền từng part → mo/nhom_<tên>.jpg
    ky_nguyen.py part_goc                      ảnh từng part cắt theo lưới → <SXS>/scan/monster_3642/parts/ + tờ tổng (chỉ để xem)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hoa_ho as H  # noqa: E402

CODE = "ky_nguyen"
MON = "monster_3642"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")

# nhóm part theo tên slot của họ (cái đầu tiên khớp thì lấy)
NHOM = [
    ("dau", r"^P_tou", (235, 235, 235)),                        # tou = đầu (mũ)
    ("long_vu", r"^P_yumao", (120, 200, 250)),                  # yumao = lông vũ
    ("kiem", r"^P_jian$", (90, 220, 230)),                      # jian = kiếm
    ("vai", r"^P_jianjia", (200, 120, 220)),                    # jianjia = giáp vai
    ("nguc", r"^P_xiongjia", (255, 120, 80)),                   # xiongjia = giáp ngực
    ("ao_choang", r"^P_pifeng", (150, 90, 230)),                # pifeng = áo choàng
    ("than", r"^P_shenti", (255, 230, 60)),                     # shenti = thân
    ("tinh_the", r"^P_ci", (230, 60, 160)),                     # ci = gai (tinh thể)
    ("da", r"^P_shitou", (140, 140, 140)),                      # shitou = đá
    ("khoi", r"^P_yanwu|^P_yanse", (60, 220, 120)),             # yanwu = khói
    ("tay_phai", r"^P_y_", (250, 170, 110)),                    # y_ = tay phải (của nhân vật)
    ("tay_trai", r"^P_z_", (90, 140, 230)),                     # z_ = tay trái
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
