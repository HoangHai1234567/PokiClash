# -*- coding: utf-8 -*-
"""Khủng long núi lửa đảo Hỏa (mã làm việc nui_lua; con gốc của rig: monster_3654, game tham khảo). Tướng thứ 10 (cuối) đảo Hỏa, FINAL BOSS
(suất lan_hoa, ải 70 "Miệng Núi Lửa").

Người dùng 2026-11-14: concept khủng long núi lửa như con gốc; idle và walk như con gốc (sửa chút cũng được); đánh thường lao vào húc; chiêu mana
há mồm tụ một quả cầu lửa rồi bắn; chiêu cuối giống skill_04: bẻ các đỉnh núi lửa trên lưng theo các hướng khác nhau, bắn đạn lửa bay vòng cung
ngẫu nhiên nhưng vẫn lao vào đối thủ kiểu tên lửa tầm nhiệt (đường bay làm bằng code); die giống họ; làm thật đẹp, hoành tráng, impact; thêm
fx khói ở đỉnh các núi lửa trên lưng. Con gốc nhìn sang PHẢI. Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ.

Dùng lại các hàm mổ của hoa_ho.py (cùng định dạng quét), chỉ đổi con và bảng nhóm.

    nui_lua.py mo [att json] [tên ra] [S]   tờ MỔ từng part ở một dáng → <SXS>/scan/monster_3654/mo/<tên>_<k>.jpg + bảng
    nui_lua.py nhom [att json] [tên ra]      cả con tô màu theo NHÓM part + viền từng part → mo/nhom_<tên>.jpg
    nui_lua.py part_goc                      ảnh từng part cắt theo lưới → <SXS>/scan/monster_3654/parts/ + tờ tổng (chỉ để xem)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hoa_ho as H  # noqa: E402

CODE = "nui_lua"
MON = "monster_3654"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")

# nhóm part theo tên slot của họ (cái đầu tiên khớp thì lấy)
NHOM = [
    ("ong_nui_lua", r"^P_jiao_\d+$", (230, 70, 60)),          # 16 ống núi lửa (jiao = sừng) trên lưng, mỗi ống một xương
    ("khoi", r"^P_yan_\d+$", (200, 200, 210)),                # 6 cụm khói (yan = khói), tắt ở dáng gốc
    ("giap_lung", r"^P_beijia", (90, 90, 100)),               # các tảng đá lưng
    ("bung", r"^P_duzi", (150, 120, 200)),                    # bụng + 6 tảng đá sườn
    ("dau", r"^P_shagne|^P_xiae|^P_houlong|^P_yanjing", (255, 230, 60)),  # hàm trên, hai mảnh hàm dưới, họng, mắt
    ("chan_sau_xa", r"^P_houtuiL", (90, 140, 230)),
    ("chan_truoc_xa", r"^P_qiantuiL|^P_jiaozhi_02", (120, 190, 250)),
    ("chan_sau_gan", r"^P_houtuiR", (230, 150, 90)),
    ("chan_truoc_gan", r"^P_qiantuiR|^P_jiaozhi_01", (250, 190, 110)),
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
