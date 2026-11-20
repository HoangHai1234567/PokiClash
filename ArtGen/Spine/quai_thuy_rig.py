# -*- coding: utf-8 -*-
"""Quái đảo Thủy (tôm tít đấm bốc): sinh lệnh AtomSpine dựng rig từ mảnh đã cắt (quai_thuy_cat.py) -> quai_thuy/atom/rig.ops.

    py -3 -I ArtGen/Spine/quai_thuy_rig.py        # rồi: atom do -f rig.ops -p ArtGen/Spine/quai_thuy/atom

Xương cho bằng hai điểm trên ảnh concept (đầu khớp, mút); toạ độ thế giới x = px - OX, y = OY - py (y lên), góc CCW.
"""
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "quai_thuy")
P = json.load(open(os.path.join(D, "parts.json"), encoding="utf-8"))
OX, OY = P["origin"]
CW, CH = P["canvas"]

# (tên, cha, điểm khớp px, điểm mút px)
BONES = [
    ("move", "root", (720, 950), (720, 950)),
    ("hip", "move", (650, 800), (650, 760)),
    ("than", "hip", (650, 790), (800, 480)),
    ("dau", "than", (800, 480), (990, 410)),
    ("mat_s", "dau", (812, 338), (800, 232)),
    ("mat_t", "dau", (948, 330), (990, 226)),
    ("vay_l", "dau", (735, 345), (600, 300)),
    ("vay_r", "dau", (1000, 338), (1072, 330)),
    ("rt1", "dau", (742, 352), (650, 232)),
    ("rt2", "rt1", (650, 232), (520, 170)),
    ("rt3", "rt2", (520, 170), (335, 222)),
    ("rs1", "dau", (790, 182), (690, 95)),
    ("rs2", "rs1", (690, 95), (570, 82)),
    ("rs3", "rs2", (570, 82), (470, 125)),
    ("cx_bap", "than", (975, 598), (1095, 480)),
    ("cx_cang", "cx_bap", (1095, 480), (1195, 385)),
    ("cx_chuy", "cx_cang", (1195, 385), (1240, 320)),
    ("cx_mui", "cx_chuy", (1300, 290), (1340, 270)),   # mũi chùy càng xa: chỗ nhả hiệu ứng
    ("cg_vai", "than", (690, 520), (660, 650)),
    ("cg_co", "cg_vai", (660, 650), (790, 662)),
    ("cg_chuy", "cg_co", (790, 662), (890, 635)),
    ("cg_mui", "cg_chuy", (985, 620), (1025, 615)),     # mũi chùy càng gần: chỗ nhả hiệu ứng
    ("cg_vong", "cg_chuy", (985, 620), (1025, 615)),    # vòng sóng / chớp ở mũi chùy gần (vfx.ring co giãn xương này)
    ("cx_vong", "cx_chuy", (1300, 290), (1340, 270)),   # vòng sóng / chớp ở mũi chùy xa
    ("dat_vong", "root", (720, 950), (760, 950)),        # vòng sóng dưới đất (ra sân)
    ("duoi1", "than", (520, 672), (410, 770)),
    ("duoi2", "duoi1", (410, 770), (330, 850)),
    ("quat", "duoi2", (330, 850), (205, 900)),
    ("chan1", "move", (560, 790), (500, 945)),
    ("chan2", "move", (668, 800), (668, 945)),
    ("chan3", "move", (790, 795), (810, 945)),
    ("chan4", "move", (865, 780), (935, 935)),
]
# mảnh -> xương; lưới (mesh) + chuỗi trọng số cho phần mềm
SLOT_BONE = {
    "rau_sau": ("rs1", ["rs1", "rs2", "rs3"]), "rau_truoc": ("rt1", ["rt1", "rt2", "rt3"]),
    "vay_trai": ("vay_l", None), "vay_phai": ("vay_r", None),
    "cang_xa_bap": ("cx_bap", None), "cang_xa_cang": ("cx_cang", None), "cang_xa_chuy": ("cx_chuy", None),
    "quat": ("quat", None), "duoi2": ("duoi2", None), "duoi1": ("duoi1", None),
    "chan1": ("chan1", None), "chan2": ("chan2", None), "chan3": ("chan3", None), "chan4": ("chan4", None),
    "than": ("than", None), "dau": ("dau", None), "mat_sau": ("mat_s", None), "mat_truoc": ("mat_t", None),
    "cang_gan_vai": ("cg_vai", None), "cang_gan_co": ("cg_co", None), "cang_gan_chuy": ("cg_chuy", None),
}


def w(pt):
    return pt[0] - OX, OY - pt[1]


def main():
    out = ["# rig tôm tít đấm bốc (quái đảo Thủy) — sinh bởi ArtGen/Spine/quai_thuy_rig.py"]
    for name, parent, a, b in BONES:
        x, y = w(a)
        bx, by = w(b)
        ln = math.hypot(bx - x, by - y)
        rot = math.degrees(math.atan2(by - y, bx - x)) if ln > 0.5 else 0
        out.append(f"bone.add {name} parent={parent} x={x:.1f} y={y:.1f} rot={rot:.2f} len={ln:.1f} world=true")
    for p in P["parts"]:
        bone, chain = SLOT_BONE[p["name"]]
        mesh = "true" if chain else "false"
        out.append(f"part.add {p['name']} path=images/{p['name']}.png at={p['at'][0]},{p['at'][1]} canvas={CW},{CH} "
                   f"origin={OX},{OY} bone={bone} mesh={mesh}")
        if chain:
            out.append(f"att.weights {p['name']} {p['name']} bones={','.join(chain)}")
    path = os.path.join(D, "atom", "rig.ops")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print(f"{len(out)} dòng -> {path}")


if __name__ == "__main__":
    main()
