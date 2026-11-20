# -*- coding: utf-8 -*-
"""Quái đảo Thổ (dê đá húc, thay Chuột Khoan): sinh lệnh AtomSpine dựng rig từ mảnh đã cắt (quai_tho_cat.py) -> quai_tho/atom/rig.ops.

    py -3 -I ArtGen/Spine/quai_tho_rig.py        # rồi: atom do -f rig.ops -p ArtGen/Spine/quai_tho/atom

Xương cho bằng hai điểm trên ảnh concept (đầu khớp, mút); toạ độ thế giới x = px - OX, y = OY - py (y lên), góc CCW.
Bốn chân: mỗi chân hai đoạn (đùi bám hông / ngực, cẳng) + IK tới đích dưới `move` -> móng bám đất khi thân nhún, lao.
Thân lông một lưới trọng số hông + ngực (hai khối nảy lệch pha). Đầu mang hai sừng, tai xa; ba tấm đá lưng xương riêng.
"""
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "quai_tho")
P = json.load(open(os.path.join(D, "parts.json"), encoding="utf-8"))
OX, OY = P["origin"]
CW, CH = P["canvas"]

# (tên, cha, điểm khớp px, điểm mút px)
BONES = [
    ("move", "root", (625, 930), (625, 930)),
    ("hip", "move", (440, 620), (760, 600)),
    ("nguc", "hip", (760, 600), (880, 600)),
    ("dau", "nguc", (835, 615), (1190, 690)),
    ("mui", "dau", (1195, 615), (1235, 615)),         # trán / mõm: điểm va chạm húc
    ("vong_dau", "dau", (1195, 615), (1235, 615)),    # vòng va chạm (vfx.ring co giãn xương này)
    ("sung_g", "dau", (800, 480), (700, 560)),
    ("sung_x", "dau", (1010, 440), (1180, 300)),
    ("tai_x", "dau", (1150, 505), (1205, 440)),
    ("duoi", "hip", (275, 505), (170, 470)),
    ("da1", "hip", (385, 378), (310, 300)),
    ("da2", "hip", (505, 300), (440, 215)),
    ("da3", "nguc", (655, 240), (650, 150)),
    # chân: đùi (cha hông / ngực) -> cẳng (tới móng)
    ("gs_tren", "hip", (335, 735), (318, 815)),
    ("gs_duoi", "gs_tren", (318, 815), (305, 890)),
    ("xs_tren", "hip", (492, 785), (484, 840)),
    ("xs_duoi", "xs_tren", (484, 840), (472, 888)),
    ("gt_tren", "nguc", (640, 760), (640, 840)),
    ("gt_duoi", "gt_tren", (640, 840), (650, 912)),
    ("xt_tren", "nguc", (885, 780), (905, 832)),
    ("xt_duoi", "xt_tren", (905, 832), (928, 888)),
    # đích IK dưới move (ở móng)
    ("ik_gs", "move", (305, 890), (305, 890)),
    ("ik_xs", "move", (472, 888), (472, 888)),
    ("ik_gt", "move", (650, 912), (650, 912)),
    ("ik_xt", "move", (928, 888), (928, 888)),
    ("dat_truoc", "move", (790, 925), (830, 925)),    # chỗ hai móng trước dậm: hạt đá, vòng sóng đất (cast)
    ("dat_vong", "root", (625, 930), (665, 930)),     # vòng bụi dưới đất (ra sân)
]
IK = [("chan_gs", "gs_tren", "gs_duoi", "ik_gs", "-"), ("chan_xs", "xs_tren", "xs_duoi", "ik_xs", "-"),
      ("chan_gt", "gt_tren", "gt_duoi", "ik_gt", "+"), ("chan_xt", "xt_tren", "xt_duoi", "ik_xt", "+")]
# mảnh -> xương; lưới (mesh) + chuỗi trọng số cho phần mềm
SLOT_BONE = {
    "bom": ("nguc", None), "sung_xa": ("sung_x", None),
    "chan_xa_sau": ("xs_tren", ["xs_tren", "xs_duoi"]), "chan_xa_truoc": ("xt_tren", ["xt_tren", "xt_duoi"]),
    "da1": ("da1", None), "da2": ("da2", None), "da3": ("da3", None),
    "duoi": ("duoi", None),
    "chan_gan_sau": ("gs_tren", ["gs_tren", "gs_duoi"]), "chan_gan_truoc": ("gt_tren", ["gt_tren", "gt_duoi"]),
    "than": ("hip", ["hip", "nguc"]),
    "tai_xa": ("tai_x", None), "dau": ("dau", None), "sung_gan": ("sung_g", None),
}


def w(pt):
    return pt[0] - OX, OY - pt[1]


def main():
    out = ["# rig dê đá húc (quái đảo Thổ) — sinh bởi ArtGen/Spine/quai_tho_rig.py"]
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
    for name, a, b, t, bend in IK:
        out.append(f"ik.add {name} bones={a},{b} target={t} bend={bend}")
    path = os.path.join(D, "atom", "rig.ops")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print(f"{len(out)} dòng -> {path}")


if __name__ == "__main__":
    main()
