# -*- coding: utf-8 -*-
"""Quái lính đảo Hỏa (gà chọi lửa): sinh lệnh AtomSpine dựng rig từ mảnh đã cắt (quai_hoa_cat.py) -> quai_hoa/atom/rig.ops.

    py -3 -I ArtGen/Spine/quai_hoa_rig.py        # rồi: atom do -f rig.ops -p ArtGen/Spine/quai_hoa/atom

Xương cho bằng hai điểm trên ảnh concept (đầu khớp, mút); toạ độ thế giới x = px - OX, y = OY - py (y lên), góc CCW.
Chân gắn `move` (thân nhún trên `hip` không kéo bàn chân trượt; đầu cẳng nấp dưới thân 30–40 px). Mào 3 lưỡi lửa, đuôi 4 lông
lửa: mỗi lưỡi / lông một chuỗi 2 xương, cả mảnh là một lưới có trọng số tự động trên mọi xương của chuỗi.
"""
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "quai_hoa")
P = json.load(open(os.path.join(D, "parts.json"), encoding="utf-8"))
OX, OY = P["origin"]
CW, CH = P["canvas"]

# (tên, cha, điểm khớp px, điểm mút px)
BONES = [
    ("move", "root", (775, 960), (775, 960)),
    ("hip", "move", (790, 760), (790, 720)),
    ("than", "hip", (790, 740), (900, 470)),
    ("dau", "than", (880, 500), (1150, 430)),
    ("mieng", "dau", (1150, 452), (1200, 452)),          # chỗ nhả lửa (trục x chĩa ra trước mỏ)
    ("m_vong", "mieng", (1165, 452), (1205, 452)),       # vòng chớp ở mỏ (vfx.ring co giãn xương này)
    ("phun_e", "mieng", (1170, 452), (1170, 492)),       # nơi phát lửa phun: chĩa xuống nên trục +y cục bộ = +x (nón vfx.burst)
    ("mo_duoi", "dau", (1040, 455), (1150, 462)),        # mỏ dưới: há khi phun
    ("m1a", "dau", (820, 290), (735, 225)), ("m1b", "m1a", (735, 225), (665, 180)),
    ("m2a", "dau", (890, 275), (805, 170)), ("m2b", "m2a", (805, 170), (750, 92)),
    ("m3a", "dau", (1000, 270), (965, 140)), ("m3b", "m3a", (965, 140), (905, 40)),
    ("canh_xa", "than", (730, 450), (580, 310)),
    ("canh_gan", "than", (765, 500), (620, 600)), ("canh_gan2", "canh_gan", (620, 600), (490, 640)),
    ("duoi", "than", (530, 600), (480, 590)),
    ("d1a", "duoi", (505, 545), (455, 330)), ("d1b", "d1a", (455, 330), (355, 205)),
    ("d2a", "duoi", (490, 575), (360, 415)), ("d2b", "d2a", (360, 415), (245, 322)),
    ("d3a", "duoi", (485, 610), (330, 525)), ("d3b", "d3a", (330, 525), (200, 495)),
    ("d4a", "duoi", (490, 655), (385, 680)), ("d4b", "d4a", (385, 680), (280, 628)),
    ("chan_t", "move", (603, 785), (560, 885)), ("ban_t", "chan_t", (560, 885), (520, 935)),
    ("chan_p", "move", (950, 790), (975, 885)), ("ban_p", "chan_p", (975, 885), (1040, 935)),
    # điểm nổ cú đá: gắn move, đặt tĩnh đúng chỗ mũi vuốt ở khung trúng (quai_hoa_anim.py tính FK rồi dời bằng khoá setup);
    # *_v riêng cho vfx.ring (ring co giãn xương nó ngồi, hạt không được là con của xương đó)
    ("fx_da1", "move", (1135, 690), (1165, 690)), ("fx_da1v", "move", (1135, 690), (1165, 690)),
    ("fx_da2", "move", (1135, 690), (1165, 690)), ("fx_da2v", "move", (1135, 690), (1165, 690)),
    ("dat_vong", "root", (775, 960), (815, 960)),        # vòng bụi dưới đất (ra sân, đáp)
]
# mảnh -> (xương chính, chuỗi trọng số lưới hoặc None)
SLOT_BONE = {
    "canh_xa": ("canh_xa", None),
    "duoi": ("duoi", ["duoi", "d1a", "d1b", "d2a", "d2b", "d3a", "d3b", "d4a", "d4b"]),
    "chan_trai": ("chan_t", ["chan_t", "ban_t"]),
    "chan_phai": ("chan_p", ["chan_p", "ban_p"]),
    "than": ("than", None),
    "mao": ("m2a", ["m1a", "m1b", "m2a", "m2b", "m3a", "m3b"]),
    "dau": ("dau", None),
    "mo_duoi": ("mo_duoi", None),
    "canh_gan": ("canh_gan", ["canh_gan", "canh_gan2"]),
}


def w(pt):
    return pt[0] - OX, OY - pt[1]


def main():
    out = ["# rig gà chọi lửa (quái lính đảo Hỏa) — sinh bởi ArtGen/Spine/quai_hoa_rig.py"]
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
    # bản sao chân trước vẽ TRƯỚC thân (sau mào, đầu, cánh gần), mặc định ẩn: attack / skill bật bản sao, tắt bản gốc lúc chân
    # vươn ra trước (runtime .atomik của game không đọc khoá thứ tự vẽ). Chung ảnh, cùng lưới tự động + trọng số chan_p / ban_p.
    p = next(x for x in P["parts"] if x["name"] == "chan_phai")
    n = "chan_phai_truoc"
    out.append(f"part.add {n} path=images/chan_phai.png at={p['at'][0]},{p['at'][1]} canvas={CW},{CH} "
               f"origin={OX},{OY} bone=chan_p mesh=true")
    out.append(f"att.weights {n} {n} bones=chan_p,ban_p")
    out.append(f"slot.order {n} to=after:than")
    out.append(f"att.set {n} {n} image=chan_phai")          # dùng chung ảnh chân gốc (atlas không nhân đôi)
    out.append(f"image.del {n}")
    out.append(f"slot.set {n} att=-")
    path = os.path.join(D, "atom", "rig.ops")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print(f"{len(out)} dòng -> {path}")


if __name__ == "__main__":
    main()
