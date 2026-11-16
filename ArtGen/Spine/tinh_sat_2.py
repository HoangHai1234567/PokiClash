# -*- coding: utf-8 -*-
"""Tinh linh tinh thể sắt DẠNG 2 (dạng cuối; mã làm việc tinh_sat_2; con gốc của rig: monster_3347, game tham khảo: dạng tiến hoá của
monster_3346 mà dạng 1 `tinh_sat_1` bám). Tướng thứ 1 đảo Kim.

Người dùng 2026-11-16: "quét tướng 1 đảo kim mới làm và làm dạng 2 của nó"; chọn rig 3347; dòng có 2 dạng (dạng 2 là dạng cuối, ngầu nhất);
đòn, chiêu như dạng 1 nhưng mạnh hơn (lao tông; tinh thể bay lên trên đầu rồi code lái đâm vào đối thủ; phình to nhảy dập, rung squash stretch).
Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

Dùng lại các hàm mổ của hoa_ho.py (cùng định dạng quét), chỉ đổi con và bảng nhóm.

    tinh_sat_2.py mo [att json] [tên ra] [S]   tờ MỔ từng part ở một dáng → <SXS>/scan/monster_3347/mo/<tên>_<k>.jpg + bảng
    tinh_sat_2.py nhom [att json] [tên ra]      cả con tô màu theo NHÓM part + viền từng part → mo/nhom_<tên>.jpg
    tinh_sat_2.py part_goc                      ảnh từng part cắt theo lưới → <SXS>/scan/monster_3347/parts/ + tờ tổng (chỉ để xem)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hoa_ho as H  # noqa: E402

CODE = "tinh_sat"
MON = "monster_3347"
BASE = os.path.join(HERE, "inbox", f"{CODE}_2")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")

# nhóm part theo tên slot của họ (cái đầu tiên khớp thì lấy)
NHOM = [
    ("tinh_the_bay", r"^P_bc_\d+$", (120, 140, 250)),     # 5 tinh thể bay quanh (bc_01 trái, bc_02 trên trái, bc_03 trên phải, bc_04/05 sau phải)
    ("chan", r"^P_tui", (90, 200, 190)),                   # hai chân (mỗi chân hai khúc, IK)
    ("mu", r"^P_maozi$", (250, 190, 110)),                 # chỏm tinh thể trên đỉnh (mũ)
    ("vo", r"^P_lian_1$", (235, 235, 235)),                # vỏ tinh thể bọc quanh mặt
    ("mat", r"^P_lian$", (60, 60, 90)),                    # mặt tối
    ("mieng", r"^P_zui$", (200, 120, 220)),                # cụm tinh thể dưới mặt (hàm)
    ("mat_mat", r"^P_yanjing$", (255, 230, 60)),           # mắt
]

H.CODE, H.MON, H.BASE, H.MAU, H.TAI, H.NHOM = CODE, MON, BASE, MAU, TAI, NHOM


def _luoi(a):
    """như hoa_ho.luoi nhưng đúng cho hình region có `rotate: 90` (atlas Spine 4: bounds ghi rộng / cao CHƯA xoay; hoa_ho.luoi đảo hai số
    nên mắt P_yanjing của 3347 ra một vạch mảnh). Con 3346 không có region xoay nên dạng 1 không bị."""
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
