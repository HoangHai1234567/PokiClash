# -*- coding: utf-8 -*-
"""Tinh linh đuôi máy cưa đảo Kim (mã làm việc cua_xich; con gốc của rig: monster_3374, sinh vật nhỏ mũ sừng sẫm, ba tinh thể trên lưng,
đuôi là cái đĩa bánh răng có gai tinh thể; game tham khảo). Tướng thứ 4 đảo Kim (ải 15 "Tháp Canh Thép", id game hiện là phi_thuong).

Người dùng 2026-11-16: concept tinh linh đuôi máy cưa; appear kéo một sợi dây trên người để khởi động máy cưa ở đuôi; idle / walk giống
con gốc, sửa chút cho khác; đánh thường lao vào húc đối thủ; chiêu mana dùng đuôi cưa quật đối thủ; chiêu cuối kéo dây thêm nhiều lần, cưa
quay nhanh hơn và to ra chút, có hiệu ứng hút quanh..., rồi dùng đuôi cưa cưa liên tục đối thủ (đối thủ bị đánh liên hồi), tia lửa bắn ra;
die giống con gốc.
Con gốc nhìn sang PHẢI. Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

Dùng lại các hàm mổ của hoa_ho.py (cùng định dạng quét), chỉ đổi con và bảng nhóm.

    cua_xich.py mo [att json] [tên ra] [S]   tờ MỔ từng part ở một dáng → <SXS>/scan/monster_3374/mo/<tên>_<k>.jpg + bảng
    cua_xich.py nhom [att json] [tên ra]      cả con tô màu theo NHÓM part + viền từng part → mo/nhom_<tên>.jpg
    cua_xich.py part_goc                      ảnh từng part cắt theo lưới → <SXS>/scan/monster_3374/parts/ + tờ tổng (chỉ để xem)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hoa_ho as H  # noqa: E402

CODE = "cua_xich"
MON = "monster_3374"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")

# nhóm part theo tên slot của họ (cái đầu tiên khớp thì lấy)
NHOM = [
    ("duoi_cua", r"^(weiba_0[1-4]|juzi_0[34])$", (250, 190, 110)),   # đuôi: các khúc đuôi + đĩa cưa (juzi = cưa)
    ("chan", r"(datui|xiaotui)", (120, 140, 250)),                    # chân (đùi, cẳng) hai bên
    ("than", r"^shenti$", (235, 235, 235)),                            # thân
    ("tay", r"(youshou|zuoshou)", (90, 220, 230)),                    # hai tay
    ("dau", r"^(to_0[12]|tofa|youerduo|zuoerduo)$", (200, 120, 220)),  # đầu: mặt, mũ / tóc (tofa), hai tai
    ("mat", r"^yanjing", (250, 90, 90)),                               # mắt
    ("khac", r".", (255, 0, 0)),
]

H.CODE, H.MON, H.BASE, H.MAU, H.TAI, H.NHOM = CODE, MON, BASE, MAU, TAI, NHOM


def _luoi(a):
    """như hoa_ho.luoi nhưng đúng cho hình region có `rotate: 90 / 270` (xem tinh_sat_2._luoi)."""
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
