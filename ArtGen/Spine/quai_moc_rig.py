# -*- coding: utf-8 -*-
"""Quái đảo Mộc (sóc dẻ gai): sinh lệnh AtomSpine dựng rig từ mảnh đã cắt (quai_moc_cat.py) -> quai_moc/atom/rig.ops.

    py -3 -I ArtGen/Spine/quai_moc_rig.py        # rồi: atom do -f rig.ops -p ArtGen/Spine/quai_moc/atom

Xương cho bằng hai điểm trên ảnh concept (đầu khớp, mút); toạ độ thế giới x = px - OX, y = OY - py (y lên), góc CCW.
"""
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "quai_moc")
P = json.load(open(os.path.join(D, "parts.json"), encoding="utf-8"))
OX, OY = P["origin"]
CW, CH = P["canvas"]

# (tên, cha, điểm khớp px, điểm mút px)
BONES = [
    ("move", "root", (790, 945), (790, 945)),
    ("hip", "move", (785, 830), (785, 790)),
    ("than_duoi", "hip", (785, 905), (785, 790)),     # nửa dưới thân: đứng yên theo hông, đáy thân bám chân
    ("than", "than_duoi", (785, 790), (820, 600)),
    ("dau", "than", (850, 615), (880, 420)),
    ("mu", "dau", (860, 330), (880, 130)),
    ("tai_l", "dau", (765, 322), (750, 232)),
    ("tai_r", "dau", (1040, 326), (1052, 262)),
    ("tay_gan", "than", (668, 625), (770, 645)),
    ("tay_xa", "than", (1005, 630), (1090, 700)),
    ("nam_xa", "tay_xa", (1135, 615), (1165, 545)),
    ("duoi1", "hip", (612, 770), (550, 600)),
    ("duoi2", "duoi1", (550, 600), (548, 410)),
    ("duoi3", "duoi2", (548, 410), (420, 240)),
    ("chan_gan", "move", (612, 866), (560, 940)),
    ("chan_xa", "move", (945, 820), (1000, 935)),
    # chỗ nhả hiệu ứng (vfx.ring co giãn xương nó đứng nên mỗi vòng một xương riêng)
    ("mu_mui", "mu", (1110, 330), (1150, 330)),        # mũi mũ gai: mảnh gai, lá văng khi húc
    ("mu_vong", "mu", (1110, 330), (1150, 330)),       # vòng chớp khi húc
    ("mu_vong2", "mu", (1110, 330), (1150, 330)),      # vòng sóng khi húc
    ("tg_vong", "tay_gan", (805, 640), (845, 640)),    # nắm đấm gần
    ("tx_vong", "nam_xa", (1160, 565), (1200, 565)),   # nắm đấm xa
    ("tx_mui", "nam_xa", (1160, 565), (1200, 565)),
    ("phong", "move", (1185, 500), (1185, 550)),       # chỗ phóng lá (cast): rot -90 nên hạt bay về +x
    ("phong_vong", "move", (1185, 500), (1225, 500)),
    ("phong_vong2", "move", (1185, 500), (1225, 500)),
    ("dat_truoc", "move", (1180, 940), (1220, 940)),   # vòng đất trước mặt (đuôi nện)
    ("dat_truoc2", "move", (1180, 940), (1220, 940)),
    ("dat_truoc_mui", "move", (1180, 930), (1180, 890)),
    ("dat_vong", "root", (790, 945), (830, 945)),      # vòng đất ra sân
]
# mảnh -> xương; lưới (mesh) + chuỗi trọng số cho phần mềm (sóc: toàn mảnh cứng)
SLOT_BONE = {
    "duoi3": ("duoi3", None), "duoi2": ("duoi2", None), "duoi1": ("duoi1", None),
    "tay_xa": ("tay_xa", None), "nam_xa": ("nam_xa", None), "chan_xa": ("chan_xa", None),
    "than": ("than_duoi", ["than_duoi", "than"]), "chan_gan": ("chan_gan", None), "dau": ("dau", None), "tay_gan": ("tay_gan", None),
    "mu": ("mu", None), "tai_trai": ("tai_l", None), "tai_phai": ("tai_r", None),
}


def w(pt):
    return pt[0] - OX, OY - pt[1]


def main():
    out = ["# rig sóc dẻ gai (quái đảo Mộc) — sinh bởi ArtGen/Spine/quai_moc_rig.py"]
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
    # bản sao lá đuôi vẽ TRƯỚC thân (sau đầu và tay gần), mặc định ẩn: clip quật đuôi ra trước bật bản sao, tắt bản gốc
    # (runtime .atomik của game không có khoá thứ tự vẽ)
    for p in P["parts"]:
        if p["name"] in ("duoi3", "duoi2", "duoi1"):
            n = p["name"] + "_tr"
            out.append(f"part.add {n} path=images/{p['name']}.png at={p['at'][0]},{p['at'][1]} canvas={CW},{CH} "
                       f"origin={OX},{OY} bone={SLOT_BONE[p['name']][0]} mesh=false")
            out.append(f"slot.order {n} to=before:dau")
            out.append(f"att.set {n} {n} image={p['name']}")   # dùng chung ảnh lá gốc (atlas không nhân đôi)
            out.append(f"image.del {n}")
            out.append(f"slot.set {n} att=-")
    path = os.path.join(D, "atom", "rig.ops")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print(f"{len(out)} dòng -> {path}")


if __name__ == "__main__":
    main()
