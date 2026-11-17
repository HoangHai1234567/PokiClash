# -*- coding: utf-8 -*-
"""Vua robot (mã làm việc vua_may; con gốc của rig: monster_3637, vua robot giáp vàng đội vương miện, áo choàng đỏ, dải xanh, ngồi trên
bệ hai chân xích tam giác, cầm quyền trượng đầu bánh răng + hai vòng; game tham khảo). Tướng thứ 10 / final boss đảo Kim (ải 70, id game
hiện là kim_nghe).

Người dùng 2026-11-17: concept vua robot như con gốc nhưng nhiều chi tiết hơn; đổi chân xích thành CHÂN ROBOT đi lại; thêm 4 CÁNH máy
móc lơ lửng sau lưng (hoặc cánh thiên thần lông vũ, đen hoặc trắng); appear bay lên rồi hạ cánh; đủ chiêu từ skill_01 tới skill_04; walk
= bay bằng cánh. "Con khó, mổ xẻ kĩ con gốc; cánh xem các con trước trong game làm thế nào để tự làm".
Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ, không đăng công khai.

Dùng lại các hàm mổ của hoa_ho.py (cùng định dạng quét), chỉ đổi con và bảng nhóm.

    vua_may.py mo [att json] [tên ra] [S]   tờ MỔ từng part ở một dáng → <SXS>/scan/monster_3637/mo/<tên>_<k>.jpg + bảng
    vua_may.py nhom [att json] [tên ra]      cả con tô màu theo NHÓM part + viền từng part → mo/nhom_<tên>.jpg
    vua_may.py part_goc                      ảnh từng part cắt theo lưới → <SXS>/scan/monster_3637/parts/ + tờ tổng (chỉ để xem)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hoa_ho as H  # noqa: E402

CODE = "vua_may"
MON = "monster_3637"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")

# nhóm part theo tên slot của họ (cái đầu tiên khớp thì lấy). Tên Trung: touguan = vương miện, bizi = mũi, toufa = tóc (râu, ria),
# xiongqiong = ngực, fubu = bụng, beibu = lưng, dabi / xiaobi = bắp / cẳng tay, shouwan = cổ tay, shouzhang = bàn tay,
# damuzhi / shizhi / zhongzhi = ngón cái / trỏ / giữa, jianjia = giáp vai, jian = vai, jiao = chân, fazhang = quyền trượng,
# fatiao = dây cót (bánh răng), pifeng = áo choàng
NHOM = [
    ("ao_choang", r"^pifeng", (230, 80, 80)),
    ("truong", r"^fazhang", (250, 210, 60)),
    ("banh_rang", r"^fatiao", (150, 150, 150)),
    ("dau", r"^(touguan|bizi|toufa|yanjing)", (240, 240, 240)),
    ("chan", r"^(jiao|xiabanshen_02$)", (160, 110, 60)),
    ("tay_l", r"_l(_|$)|_l\d", (90, 200, 120)),
    ("tay_r", r"_r(_|$)|__r|_r\d", (90, 140, 230)),
    ("than", r"^(xiabanshen|beibu|xiongqiong|fubu)", (255, 170, 90)),
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
