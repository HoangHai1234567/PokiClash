# -*- coding: utf-8 -*-
"""Quái đảo Kim (nhím thép, thay Giáp Vệ): sinh lệnh AtomSpine dựng rig từ mảnh đã cắt (quai_kim_cat.py) -> quai_kim/atom/rig.ops.

    py -3 -I ArtGen/Spine/quai_kim_rig.py        # rồi: atom do -f rig.ops -p ArtGen/Spine/quai_kim/atom

Xương cho bằng hai điểm trên ảnh concept (đầu khớp, mút); toạ độ thế giới x = px - OX, y = OY - py (y lên), góc CCW.
Thân + đầu là MỘT lưới (đầu và thân dính liền một khối lông), trọng số than/dau: đầu gật mà cổ không lộ đường cắt.
Bờm lưỡi thép: ba nhóm (dưới / giữa / trên), mỗi nhóm một xương để xoè, dựng, run lệch pha.
"""
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "quai_kim")
P = json.load(open(os.path.join(D, "parts.json"), encoding="utf-8"))
OX, OY = P["origin"]
CW, CH = P["canvas"]

# (tên, cha, điểm khớp px, điểm mút px) — mút None: xương dài 0, góc = rot (độ, thế giới)
BONES = [
    ("move", "root", (760, 962), (760, 962)),
    ("hip", "move", (775, 835), (775, 795)),
    ("xoay", "hip", (790, 640), (830, 640)),            # tâm khối thân: cuộn tròn xoay quanh đây
    ("than", "xoay", (775, 840), (795, 575)),
    ("dau", "than", (795, 585), (870, 300)),
    ("tai_x", "dau", (995, 325), (1030, 255)),
    ("bom_d", "than", (590, 760), (330, 790)),
    ("bom_g", "than", (600, 560), (270, 500)),
    ("bom_t", "than", (720, 390), (520, 170)),
    ("tx", "than", (640, 612), (495, 445)),              # tay xa (cả nắm đấm, vuốt)
    ("tg", "than", (985, 617), (1100, 652)),             # tay gần
    ("tg_vuot", "tg", (1100, 648), (1235, 650)),         # vuốt gần
    ("tg_mui", "tg_vuot", (1235, 665), (1275, 665)),     # mũi vuốt: chỗ nhả tia lửa
    ("tg_vong", "tg_vuot", (1215, 660), (1255, 660)),    # vết chém / chớp ở vuốt (vfx.ring co giãn xương này)
    ("ban", "hip", (840, 215), None, -90),               # chỗ phóng loạt lông (trục +y cục bộ chĩa +x thế giới; gắn hông để hướng phun không xoay theo bờm)
    ("ban_vong", "hip", (840, 215), (880, 215)),         # vòng nhả ở chỗ phóng
    ("than_tam", "hip", (790, 610), None, -90),          # tâm khối thân: lông toả tròn lúc cuộn (gắn hông: không xoáy theo cú lăn)
    ("than_vong", "hip", (790, 610), (830, 610)),
    ("dat_vong", "root", (760, 962), (800, 962)),        # vòng dưới đất (ra sân)
    ("chan_x", "move", (585, 805), (575, 950)),
    ("chan_g", "move", (945, 808), (960, 950)),
]
# mảnh -> xương; lưới (mesh) + chuỗi trọng số cho phần mềm
SLOT_BONE = {
    "bom_duoi": ("bom_d", None), "bom_giua": ("bom_g", None), "bom_tren": ("bom_t", None),
    "chan_xa": ("chan_x", None), "tay_xa": ("tx", None), "tai_xa": ("tai_x", None),
    "tay_gan": ("tg", None), "vuot_gan": ("tg_vuot", None), "chan_gan": ("chan_g", None),
    "than": ("than", ["than", "dau"]), "mat": ("dau", None),
}


def w(pt):
    return pt[0] - OX, OY - pt[1]


def main():
    out = ["# rig nhím thép (quái đảo Kim) — sinh bởi ArtGen/Spine/quai_kim_rig.py"]
    for b in BONES:
        name, parent, a, tip = b[:4]
        x, y = w(a)
        if tip is None:
            rot, ln = b[4], 0.0
        else:
            bx, by = w(tip)
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
