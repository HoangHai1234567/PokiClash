# -*- coding: utf-8 -*-
"""Chiến binh đất nung, đá dung nham, có lõi dung nham (mã làm việc dat_nung; con gốc của rig: monster_3625, game tham khảo).
Tướng thứ 8 đảo Hỏa (suất ải 50, id game hiện là huyen_viem).

Con gốc nhìn sang PHẢI. Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

    dat_nung.py mo [att json] [tên ra] [S]   tờ MỔ từng part ở một dáng -> <SXS>/scan/monster_3625/mo/<tên>_<k>.jpg + bảng
    dat_nung.py nhom [att json] [tên ra]      cả con tô màu theo từng part + số thứ tự vẽ -> mo/nhom_<tên>.jpg
    dat_nung.py part_goc                      ảnh từng part cắt theo lưới -> <SXS>/scan/monster_3625/parts/ + tờ tổng
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quy_dao as Q  # noqa: E402  (bộ mổ dùng chung: chỉ đổi con gốc)

CODE = "dat_nung"
MON = "monster_3625"
Q.MON = MON
Q.CODE = CODE
K = int(os.environ.get("DN_DANG", "1"))
BASE = os.path.join(HERE, "inbox", f"{CODE}_{K}")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")

sxs, rig_goc, scan, nap, luoi, part_goc, xuong_bam = Q.sxs, Q.rig_goc, Q.scan, Q.nap, Q.luoi, Q.part_goc, Q.xuong_bam

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "mo":
        Q.mo(*sys.argv[2:5])
    elif cmd == "nhom":
        Q.nhom(*sys.argv[2:6])
    elif cmd == "part_goc":
        Q.part_het()
    else:
        print(__doc__)
