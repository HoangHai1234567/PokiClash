# -*- coding: utf-8 -*-
"""Cổ Vương Nhi (tuong_cot_non): DẠNG 1 của Cổ Vương (tuong_cot, tướng 6 đảo Mộc). Người dùng 2026-11-17: "có cần dạng 1", chọn rig
monster_3273 (cổ vật đá chạm tròn: thân hũ có hốc bụng + lõi tối, quai trên đỉnh, một mắt nhìn phải, hai tay hình cuộn, hai chân ngắn;
game tham khảo, kho SwordxStaff). Xương, lưới, chuyển động gốc là của nhà phát hành game đó: chỉ dùng nội bộ.

Concept: thiết kế mới đặt lên dáng và bố cục chi của 3273 (ảnh 1 chỉ là mẫu dáng), GIỮ NHẬN DIỆN dạng 2 (ảnh 2 = concept Cổ Vương đã
duyệt): đá xám ngả lục, rễ nâu lá xanh, tim pha lê lá trong vòng rễ, nét mực rung, tô phẳng. Dạng 1 được chibi (luật 0a).

    tuong_cot_non.py ca_con        hình cả con gốc khung 0 idle → inbox/tuong_cot_non_1/mau/goc_ca_con.png
    tuong_cot_non.py concept       file prompt từng hướng → gui_gpt/tuong_cot_non_1/luot_1_concept_<k>.txt
    tuong_cot_non.py so_goc        chồng viền con gốc lên từng concept, in IoU
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5  # noqa: E402
from tho5_huong import REF  # noqa: E402

CODE = "tuong_cot_non"
tho5.CON[CODE] = ("monster_3273", 6, 30)
_I = os.path.join(HERE, "inbox")
D2 = os.path.join(_I, "tuong_cot_1", "tai_ve", "L1_duyet.png")

GOC_EN = ("the creature whose skeleton we reuse, idle pose, 1536x1024, white background: a small round ancient relic creature (a round "
          "jar-like body with a round hole in its belly showing a dark disc inside, a wide handle on top, ONE half-round eye at the upper "
          "right of the body looking to the right, two scroll-shaped flat 'hands' at the left and right sides, two tiny stubby legs). It is "
          "painted in a smooth digital cel style. Use it ONLY for the pose and the body plan; do NOT copy its shapes, its jar look, its "
          "handle, its scroll hands, its details or its colours")
D2_EN = ("the APPROVED adult form of the SAME character (an ancient stone king statue with roots, holding a big square stone pillar), "
         "1536x1024, white background: copy its IDENTITY: the weathered grey-green stone (#9DA593 front faces, #77806E side faces), the "
         "thick brown tree roots #7A5534 with small bright-green leaves #6DBE45, the heart made of flat leaf-green crystals #7CCB4E held "
         "in a ring of roots, the narrow fierce leaf-green eyes #8BD448 under a heavy stone brow, the stepped carved stone crown, and its "
         "exact drawing style (wobbly dark-brown pen line, crayon hatching, completely flat colours). Do NOT copy its pose, its body plan "
         "or its pillar.")

CONCEPT = "the BABY form of an ancient stone king statue that has come to life (a small, round, determined little stone statue spirit)"

PLAN = ("BODY PLAN (from image 1, keep it): a small ROUND body seen in three-quarter view, turned to the RIGHT, standing on TWO tiny stubby "
        "legs at the bottom; ONE eye at the upper right of the body (the face is on the upper right of the round body, looking right); a "
        "ROUND SOCKET in the middle of the belly (lower middle); two small flat side pieces sticking out at the left and the right of the "
        "body (they become its little hands); a wide piece on top of the body (it becomes its headpiece). Same size and place on the "
        "canvas as image 1; every piece stays joined to the body or right next to it like in image 1.")

MOOD = ("MOOD: a small, brave, determined little stone guardian (a firm little frown, the eye narrowed and focused), cute but serious; "
        "chibi proportions are fine for this baby form; not a smiling mascot, not scary.")

DETAIL = ("FEW DETAILS (the user asked: not too many details): big simple shapes, each a flat colour; at most one or two inner lines "
          "per piece; only the details listed under DESIGN.")

HUONG = {
    "A": ("vương miện tầng nhỏ + hai rễ lá hai bên đầu, mắt xanh hẹp mày đá, tim pha lê trong vòng rễ, tay đá tròn quấn rễ",
          "đầu là thân tròn đá xám lục có một đai khắc quanh eo; trên đỉnh một vương miện đá nhọn hai tầng nhỏ (giống vương miện dạng 2), "
          "hai rễ nâu cong vươn lên hai bên như hai tai, đầu rễ có lá; một mắt xanh lá hẹp dưới gờ mày đá dày, miệng một nét quả quyết; "
          "hốc bụng chứa cụm hai ba pha lê lá trong vòng rễ; hai tay là hai nắm đá tròn nhỏ, cổ tay quấn một vòng rễ; hai chân đá ngắn",
          ["BODY: a round stone body (NOT a jar, no neck, no rim, no handle), weathered grey-green stone #9DA593 on the faces turned to the "
           "viewer, #77806E on the faces turned away, ONE simple carved band round its waist.",
           "FACE (upper right of the body, looking right): ONE narrow fierce leaf-green eye #8BD448 (dark pupil, one small white dot) under "
           "a thick carved stone brow, a short firm mouth line below it. No second eye visible.",
           "HEADPIECE (on top, same width as the top piece of image 1): a small pointed stone CROWN of TWO stacked tiers in the middle "
           "(like a tiny version of the adult's crown) with TWO curved brown roots #7A5534 rising at its left and right like little horns, "
           "each root ending in one or two small green leaves #6DBE45.",
           "BELLY SOCKET: a cluster of two or three flat leaf-green crystals #7CCB4E sitting in the round socket, held by a brown root ring "
           "round the socket rim.",
           "HANDS (the left and right side pieces): two small ROUND STONE FISTS (mitten-like, a few knuckle lines), each wrist wrapped by "
           "one turn of brown root.",
           "LEGS: two tiny stubby stone feet, darker #6B7363.",
           "NO jar handle, no scrolls, no spirals, no sprout on top, no pillar, no moss beard, no blue."]),
    "B": ("đầu khối đá vuông có mặt nạ đá (mắt xanh), mảnh cột vỡ đội đầu như mũ, rễ quấn chéo thân, tim pha lê trong vòng rễ, tay phiến đá",
          "thân tròn đá xám lục, trên đỉnh đội một khúc đầu cột đá vỡ có đai bậc (mũ, gợi cây cột của dạng 2), một rễ nâu bò chéo qua mũ "
          "và vai có hai lá; một mắt xanh hẹp dưới gờ mày, miệng mím; hốc bụng chứa cụm pha lê lá trong vòng rễ; hai tay là hai phiến đá "
          "dẹt bo tròn như mái chèo; hai chân đá ngắn",
          ["BODY: a round stone body (NOT a jar, no neck, no rim, no handle), weathered grey-green stone #9DA593 on the faces turned to the "
           "viewer, #77806E on the faces turned away.",
           "FACE (upper right of the body, looking right): ONE narrow fierce leaf-green eye #8BD448 (dark pupil, one small white dot) under "
           "a thick carved stone brow, a short firm mouth line below it. No second eye visible.",
           "HEADPIECE (on top, about the width of the top piece of image 1): a BROKEN TOP of a square stone PILLAR worn like a helmet: a "
           "stepped carved band and a broken jagged top edge (a small echo of the adult's pillar), tilted a little; ONE brown root "
           "#7A5534 crawls diagonally over the helmet and down the back of the body, with two small green leaves #6DBE45.",
           "BELLY SOCKET: a cluster of two or three flat leaf-green crystals #7CCB4E sitting in the round socket, held by a brown root ring "
           "round the socket rim.",
           "HANDS (the left and right side pieces): two flat rounded STONE SLABS like small paddles, each with one carved line.",
           "LEGS: two tiny stubby stone feet, darker #6B7363.",
           "NO jar handle, no scrolls, no spirals, no sprout on top, no full pillar, no moss beard, no blue."]),
}


def task():
    from tho5_huong2 import task2
    return task2(CONCEPT)


def concept():
    G = tho5.dat(CODE)
    gui = os.path.join(HERE, "gui_gpt", f"{CODE}_1")
    R = [(os.path.join(G.MAU, "goc_ca_con.png"), GOC_EN, "Con gốc monster_3273, khung 0 idle: chỉ lấy dáng và bố cục chi"),
         (D2, D2_EN, "Concept Cổ Vương (dạng 2) đã duyệt: lấy nhận diện (đá, rễ, lá, tim pha lê, mắt, vương miện) và nét vẽ"),
         REF["tinh"]]
    hd = ["# Gói gen: Cổ Vương Nhi (`tuong_cot_non`), DẠNG 1 của Cổ Vương, tướng 6 đảo Mộc (ải 30)", "",
          "Con gốc của rig: `monster_3273` (game tham khảo; người dùng chọn 2026-11-17). Ảnh mẫu 1 là hình con gốc: chỉ dùng trong máy.", "",
          "## Lượt 1: concept, hai hướng (Magnific GPT 2.6)", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{tho5.Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out = os.path.join(G.TAI, f"L1_{k}.png")
        p = os.path.join(gui, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {tho5.Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {tho5.Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.",
              "", task(), "", PLAN, "", "DESIGN:"] + [f"- {d}" for d in doi] + ["", DETAIL, "", tho5.style().replace("images 2 and 3",
              "images 2 and 3"), "", MOOD, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at about the "
              "same place and size as in image 1. No sparkles, no glints, no dust, no glow, no aura round the character, no smoke, no "
              "speed lines, no labels, no frame."]
        tho5.ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): file prompt `{tho5.Wp(p)}`; ảnh lưu vào `{tho5.Wp(out)}`."]
        print(p)
    tho5.ghi(os.path.join(gui, "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "ca_con":
        tho5.ca_con(CODE)
    elif cmd == "concept":
        concept()
    elif cmd == "so_goc":
        tho5.so_goc(CODE, "AB")
    else:
        print(__doc__)
