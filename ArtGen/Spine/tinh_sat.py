# -*- coding: utf-8 -*-
"""Tinh linh tinh thể sắt đảo Kim (mã làm việc tinh_sat; con gốc của rig: monster_3346, game tham khảo). Tướng thứ 1 đảo Kim (suất 1, ải 1,
id game hiện là bo_cap).

Người dùng 2026-11-15: concept như ảnh con gốc (khối tròn trắng mặt ":3", tinh thể vây quanh); idle / die / walk giống con gốc (sửa chút được);
đánh thường lao vào tông đối thủ; chiêu mana gọi mọi tinh thể sắt quanh người bay lên trên đầu rồi đâm vào đối thủ (đường bay bằng code);
chiêu cuối phình to cơ thể, nhảy dập lên đầu đối thủ, rung rung squash stretch như tướng 1 đảo Thủy (Tí Tách).
Con gốc nhìn sang PHẢI. Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

Dùng lại các hàm mổ của hoa_ho.py (cùng định dạng quét), chỉ đổi con và bảng nhóm.

    tinh_sat.py mo [att json] [tên ra] [S]   tờ MỔ từng part ở một dáng → <SXS>/scan/monster_3346/mo/<tên>_<k>.jpg + bảng
    tinh_sat.py nhom [att json] [tên ra]      cả con tô màu theo NHÓM part + viền từng part → mo/nhom_<tên>.jpg
    tinh_sat.py part_goc                      ảnh từng part cắt theo lưới → <SXS>/scan/monster_3346/parts/ + tờ tổng (chỉ để xem)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hoa_ho as H  # noqa: E402

CODE = "tinh_sat"
MON = "monster_3346"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")

# nhóm part theo tên slot của họ (cái đầu tiên khớp thì lấy)
NHOM = [
    ("tinh_the", r"^bin\d+$", (120, 140, 250)),              # 9 tinh thể (bin = băng) vây quanh thân, mỗi cái một xương con của all2
    ("duoi", r"tail", (200, 120, 220)),                       # chuỗi tinh thể đuôi dưới đáy
    ("tay", r"shou$", (250, 190, 110)),                       # youshou / zuoshou: hai tinh thể hai bên = tay
    ("chan", r"jiao$", (90, 200, 190)),                       # youjiao / zuojiao: hai mẩu dưới đáy = chân
    ("than", r"^body$", (235, 235, 235)),
    ("mat", r"^eyes|^mt", (255, 230, 60)),
]

H.CODE, H.MON, H.BASE, H.MAU, H.TAI, H.NHOM = CODE, MON, BASE, MAU, TAI, NHOM
sxs, scan, rig_goc, nap, luoi, part_goc, nhom_cua = H.sxs, H.scan, H.rig_goc, H.nap, H.luoi, H.part_goc, H.nhom_cua

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
