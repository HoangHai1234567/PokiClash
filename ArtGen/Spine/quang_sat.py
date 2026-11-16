# -*- coding: utf-8 -*-
"""Tinh linh quặng sắt đảo Kim (mã làm việc quang_sat; con gốc của rig: monster_3371, khối vỏ trắng mặt tối hai mắt xanh, tinh thể tím
trên đầu và hai tinh thể làm tay; game tham khảo). Tướng thứ 3 đảo Kim.

Người dùng 2026-11-16: concept tinh linh quặng sắt, CHỦ Ý làm biểu cảm mắt như con gốc; appear nằm đất ngủ, mở mắt rồi bay lên; idle / walk
giống con gốc (sửa chút), để ý animation mắt; đánh thường lao vào húc đối thủ; chiêu mana phóng hai tay vào người đối thủ rồi thu lại
(animation + code lái tay); chiêu cuối chui xuống đất, ụ đất trồi chạy tới chỗ địch (kiểu chuột chũi hoạt hình), rồi trồi lên húc địch từ
dưới lên (động tác húc lên dùng skill_01_2).
Con gốc nhìn sang PHẢI (hơi nghiêng). Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

Dùng lại các hàm mổ của hoa_ho.py (cùng định dạng quét), chỉ đổi con và bảng nhóm.

    quang_sat.py mo [att json] [tên ra] [S]   tờ MỔ từng part ở một dáng → <SXS>/scan/monster_3371/mo/<tên>_<k>.jpg + bảng
    quang_sat.py nhom [att json] [tên ra]      cả con tô màu theo NHÓM part + viền từng part → mo/nhom_<tên>.jpg
    quang_sat.py part_goc                      ảnh từng part cắt theo lưới → <SXS>/scan/monster_3371/parts/ + tờ tổng (chỉ để xem)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hoa_ho as H  # noqa: E402

CODE = "quang_sat"
MON = "monster_3371"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")

# nhóm part theo tên slot của họ (cái đầu tiên khớp thì lấy). Mọi slot tên longdan_<số> nên khớp theo số.
NHOM = [
    ("than", r"^longdan_9$", (235, 235, 235)),                   # thân: vỏ trắng + dải mặt tối + hai hạt tím trên trán (một lưới)
    ("tinh_the_dau", r"^longdan_(2|3|4)$", (250, 190, 110)),     # ba tinh thể trên đầu: 4 giữa to, 3 trái, 2 phải
    ("tay", r"^longdan_(0|1)$", (120, 140, 250)),                # hai tinh thể làm tay: 1 trái dài, 0 phải
    ("mat", r"^longdan_(7|8)$", (90, 220, 230)),                 # hai mắt: 7 trái, 8 phải (hình phụ `>` `<`)
    ("ban_sao", r"^longdan_(5|6|10|11|12)$", (200, 120, 220)),   # bản sao ẩn của tinh thể (skill_02 văng ra)
]

H.CODE, H.MON, H.BASE, H.MAU, H.TAI, H.NHOM = CODE, MON, BASE, MAU, TAI, NHOM


def _luoi(a):
    """như hoa_ho.luoi nhưng đúng cho hình region có `rotate: 90 / 270` (xem tinh_sat_2._luoi). Ở con này mọi hình là lưới có uv nên
    thường không rơi vào nhánh này."""
    import numpy as np
    atlas, imgs, _ = H.nap(H._C.get("att"))
    im = imgs[a["region"]]
    if "uv" in a:
        return np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(a["tris"]).reshape(-1, 3)
    r = atlas[a["region"]]
    ox, oy, ow, oh = r.get("offsets", [0, 0, im.width, im.height])
    w, h = r["bounds"][2], r["bounds"][3]
    return (np.array([[ox, oh - oy], [ox, oh - oy - h], [ox + w, oh - oy - h], [ox + w, oh - oy]], float),
            np.array([[0, 1, 2], [2, 3, 0]]))


H.luoi = _luoi
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
