# -*- coding: utf-8 -*-
"""Thú giáp pháo (mã làm việc thu_phao; con gốc của rig: monster_3629, thú đá lục xám bốn chân mặc giáp khối hoa văn xoắn, khẩu pháo
khối vuông có miệng sáng vàng trên lưng; game tham khảo). Tướng thứ 9 đảo Kim (ải 60, id game hiện là ung_thep).

Người dùng 2026-11-16: concept quái thú mặc kín giáp, đuôi là một khẩu pháo to; appear Claude tự sáng tạo; idle / walk giống họ; đánh
thường giống skill_01 (bắn một quả đạn sắt gây nổ); chiêu mana giống skill_03 (bắn nhiều quả đạn pháo lên trời, tách thành tên lửa nhỏ
homing lao vào mục tiêu); chiêu cuối gồng người, tụ một quả cầu năng lượng rất lớn ở họng súng rồi bắn, gây giật (giống skill_04_1 nhưng
epic, impact hơn); die tuỳ Claude.
Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

Dùng lại các hàm mổ của hoa_ho.py (cùng định dạng quét), chỉ đổi con và bảng nhóm.

    thu_phao.py mo [att json] [tên ra] [S]   tờ MỔ từng part ở một dáng → <SXS>/scan/monster_3629/mo/<tên>_<k>.jpg + bảng
    thu_phao.py nhom [att json] [tên ra]      cả con tô màu theo NHÓM part + viền từng part → mo/nhom_<tên>.jpg
    thu_phao.py part_goc                      ảnh từng part cắt theo lưới → <SXS>/scan/monster_3629/parts/ + tờ tổng (chỉ để xem)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hoa_ho as H  # noqa: E402

CODE = "thu_phao"
MON = "monster_3629"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")

# nhóm part theo tên slot của họ (cái đầu tiên khớp thì lấy)
NHOM = [
    ("phao", r"^P_pao", (255, 120, 80)),                        # pao = pháo
    ("dau", r"^P_tou", (235, 235, 235)),                        # tou = đầu
    ("tai", r"^P_erduo", (120, 200, 250)),                      # erduo = tai
    ("co", r"^P_bozi", (200, 120, 220)),                        # bozi = cổ
    ("than", r"^P_shenti", (255, 230, 60)),                     # shenti = thân (các tấm giáp lưng)
    ("chan_truoc_gan", r"^P_y_qiantui", (250, 170, 110)),       # y_ = phía gần, qiantui = chân trước
    ("chan_sau_gan", r"^P_y_houtui", (90, 220, 120)),           # houtui = chân sau
    ("chan_truoc_xa", r"^P_z_qiantui", (90, 140, 230)),         # z_ = phía xa
    ("chan_sau_xa", r"^P_z_houtui", (150, 90, 230)),
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
