# -*- coding: utf-8 -*-
"""Quỷ xích DẠNG 1 NON (quy_xich_non): dạng trước của quỷ xích giáp kín (dạng 2, inbox/quy_xich_1), trên CÙNG rig monster_3408.

Người dùng 2026-11-16: "ok làm dạng 1" → chọn "làm thêm dạng 1 non" (dạng vừa làm thành dạng 2, dạng cuối). Tỉ lệ đổi ở rig trước
(quy_xich_rig.py QX_DANG=non: đầu × 1,25, cánh × 0,72, móc × 0,8), hình bố cục dựng bằng da dạng 2 làm ảnh mẫu cho concept.

    quy_xich_non.py khung      bố cục (mau/bo_cuc.png) đặt vào khung 1536 × 1024 nền trắng → mau/bo_cuc_khung.png (+ .json)
    quy_xich_non.py concept    ba file prompt concept → gui_gpt/quy_xich_non/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
"""
import json
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "inbox", "quy_xich_non")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
GUI = os.path.join(HERE, "gui_gpt", "quy_xich_non")
DANG2 = os.path.join(HERE, "inbox", "quy_xich_1", "tai_ve", "L1_duyet.png")
W, H = 1536, 1024
MUC = "#2B2118"


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def khung():
    im = Image.open(os.path.join(MAU, "bo_cuc.png")).convert("RGB")
    k = 940.0 / im.height
    im2 = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    can = Image.new("RGB", (W, H), (255, 255, 255))
    ox, oy = (W - im2.width) // 2, (H - im2.height) // 2
    can.paste(im2, (ox, oy))
    p = os.path.join(MAU, "bo_cuc_khung.png")
    can.save(p)
    json.dump(dict(k=k, ox=ox, oy=oy), open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"k {k:.3f}, lệch {ox},{oy}")


GIU = ("KEEP (they make it the same family line as image 2): the red skin #BE452E, the two narrow slanted yellow eyes #F5BB3B (flat, no "
       "glow) and the small frowning mouth with one tiny ivory fang at its right corner, the bat wings (dark maroon membrane #5E2C2D, "
       "charcoal bones), the thin red devil tail with an iron arrow-head tip, the dark iron colours of the metal, the steel chain links, "
       "and the HOOK ON A CHAIN held upright in the right fist with the chain hanging from the ring at its lower end down to the ground.")

HUONG = {
    "A": ("đội nồi sắt",
          "quỷ con đội cái NỒI sắt méo làm mũ (quai nồi một bên, hai sừng con nhú qua lỗ thủng), không má mũ; bụng đỏ để trần có rốn, thắt "
          "dây thừng; một vạt da nhỏ thay giáp vai; xích chéo ngực + vòng sắt nhỏ thay ổ khoá; móc nhỏ gỉ; vây lưng thành ba u nhỏ",
          ["HELMET: instead of the kettle helmet, a slightly dented iron COOKING POT worn upside down as a helmet, a bit too big and tilted, "
           "with one small loop handle sticking out on its left side and a plain rim just above the eyes; flat dark iron #5C5C64 with a "
           "lighter rim #8E9199. NO cheek plates.",
           "HORNS: two SHORT stubby ivory horns #ECD7AC poking up through two holes in the pot (about one third of the size of the horns "
           "in image 2), slightly curved, rounded tips.",
           "BACK: the three iron fins become three small round iron NUBS (tiny spikes) peeking above the shoulder.",
           "SHOULDER: instead of the big spiked pauldron, one small rounded LEATHER shoulder pad #7A4A32 tied with a thin strap, no spike. "
           "The far shoulder: nothing (bare red skin).",
           "BODY: NO belly plate: the round pot belly is BARE red skin with a small navel; a thick ROPE belt #B08A55 tied round the waist "
           "over dark brown short pants #4A3A33; the two chest chains still cross the chest in an X, and where they cross a small plain "
           "iron RING (no padlock).",
           "ARMS and LEGS: bare red arms, no bracers; short legs with bare red feet with small dark claws (no greaves).",
           "HOOK: a SMALL rusty iron hook: a simple J-shaped hook with a blunt-ish point, iron #8E9199 with two small rust patches "
           "#9A5A3A, on the same short shaft with the ring at its lower end."]),
    "B": ("mũ da tai bèo",
          "quỷ con đội MŨ DA ôm đầu viền sắt (hai sừng con xuyên qua), hai miếng che tai bằng da; bụng trần, thắt lưng da khoá sắt vuông; "
          "giáp vai da tròn một đinh; xích chéo + vòng sắt; móc nhỏ cong đơn giản; vây lưng thành ba gai da",
          ["HELMET: instead of the kettle helmet, a snug brown LEATHER CAP #7A4A32 hugging the top of the head with a thin iron band #8E9199 "
           "along its lower edge just above the eyes, and two small rounded leather EAR FLAPS hanging down both sides of the face. No "
           "rivets, no ridge.",
           "HORNS: two SHORT ivory horns #ECD7AC coming out through the top of the cap, slightly curving outward (about one third of the "
           "size of the horns in image 2).",
           "BACK: the three iron fins become three small brown leather SPIKES.",
           "SHOULDER: instead of the big spiked pauldron, one small round LEATHER pad #7A4A32 with ONE round iron stud in its middle. The "
           "far shoulder: a tiny leather pad.",
           "BODY: NO belly plate: the round pot belly is BARE red skin with a small navel; a brown LEATHER belt #6A4030 with a square iron "
           "buckle round the waist over dark brown short pants #4A3A33; the two chest chains cross in an X with a small plain iron RING "
           "where they cross (no padlock).",
           "ARMS and LEGS: bare red arms with a thin leather wrist band; short legs with small brown leather boots.",
           "HOOK: a SMALL plain iron hook #8E9199: a simple curved hook with a sharp point, thinner than in image 2, on the same short "
           "shaft with the ring at its lower end."]),
    "C": ("giáp vụn nhặt nhạnh",
          "quỷ con mặc GIÁP VỤN quá cỡ: mũ xô sắt to lệch che một bên trán, một nắp nồi làm giáp vai, một miếng giáp ngực nhỏ buộc dây trên "
          "bụng trần; sừng con; móc nhỏ; vây lưng thành ba đinh sắt cong",
          ["HELMET: instead of the kettle helmet, an oversized dented iron BUCKET #5C5C64 worn tilted to the right, its rim resting just "
           "above the eyes, one small dent line; no cheek plates, no rivets.",
           "HORNS: two SHORT stubby ivory horns #ECD7AC sticking out through the bucket (about one third of the size of the horns in image "
           "2).",
           "BACK: the three iron fins become three small bent iron NAILS sticking up.",
           "SHOULDER: instead of the big spiked pauldron, a round iron POT LID #6E6E76 with a small knob in its middle, tied to the shoulder "
           "with a rope. The far shoulder: nothing.",
           "BODY: the round pot belly is BARE red skin with a small navel; on the upper chest a SMALL square iron plate #66666C hanging from "
           "two ropes (much smaller than the belly plate of image 2); a rope belt over dark brown short pants #4A3A33; the two chest chains "
           "cross in an X with a small iron RING where they cross (no padlock).",
           "ARMS and LEGS: bare red arms; short legs with bare red feet with small dark claws.",
           "HOOK: a SMALL iron hook #8E9199 shaped like a big fish hook with a small barb, on the same short shaft with the ring at its "
           "lower end."]),
}

STYLE = (f"DRAWING STYLE: exactly the hand-drawn style of image 2: a wobbly dark-brown ink outline ({MUC}, about 7 px) round every piece, "
         "thin ink lines for the few inner lines, every area ONE flat colour with visible coloured-pencil / wax-crayon hatching. No shading, "
         "no highlights, no white shine streaks, no gradients, no glow, no shadows. VERY SIMPLE DESIGN, FEW DETAILS: nothing beyond what is "
         "listed.")


def concept():
    bc = os.path.join(MAU, "bo_cuc_khung.png")
    R = [(bc, "the POSE AND PROPORTION GUIDE, 1536x1024, white background: OUR demon redrawn by computer at the proportions of its YOUNG "
              "first form (a bigger head, smaller wings, a smaller hook), still wearing the armour of its final form. It gives the exact "
              "POSE, the PROPORTIONS and the PLACE and SIZE of every body part: head, face, wings, arms, fists, belly, legs, tail, hook, "
              "chain. Keep them. Change the outfit as described.",
          "Hình bố cục dạng non (1536 × 1024, nền trắng): rig dạng 2 đổi tỉ lệ (đầu × 1,25, cánh × 0,72, móc × 0,8), da tạm dạng 2. Giữ dáng, tỉ "
          "lệ, chỗ và cỡ từng bộ phận"),
         (DANG2, "the APPROVED FINAL FORM of the same character (a fat red armoured demon with an iron kettle helmet, ivory bull horns, a big "
                 "spiked shoulder pad, a round iron belly plate, a padlock on crossed chains and a big meat hook on a chain), 1536x1024, "
                 "white background. The young form must look clearly YOUNGER and LESS ARMOURED, but of the same family line.",
          "Concept dạng 2 đã duyệt (quỷ giáp kín): lấy nét vẽ, màu da, mắt, cánh, đuôi; dạng 1 phải non hơn, ít giáp hơn")]
    hd = ["# Gói GPT: quỷ xích dạng 1 non (quy_xich_non), tướng 5 đảo Kim", "",
          "## Lượt 1: concept dạng 1 non, ba hướng (2026-11-16)", "",
          "Người dùng chọn: dạng vừa làm (quỷ giáp kín) là dạng 2; làm thêm dạng 1 non trên cùng rig. Tỉ lệ đã đổi ở rig (đầu × 1,25, cánh × 0,72, "
          "móc × 0,8). Ba hướng: giữ da đỏ, mắt vàng, nanh, cánh dơi, đuôi, móc nối xích; bỏ giáp nặng, mũ đổi dáng, sừng nhỏ, bụng để trần.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out = os.path.join(TAI, f"L1_{k}.png")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "",
              "TASK: draw the YOUNG FIRST FORM of our demon as ONE picture: the SAME pose and proportions as image 1, every body part in the "
              "same place and at the same size (if the new picture were laid over image 1, the head, face, eyes, wings, arms, fists, belly, "
              "legs, tail, hook and chain must coincide), but a new, lighter outfit described below, in the drawing style of image 2.", "",
              GIU, "",
              "CHANGE:"] + [f"- {d}" for d in doi] + ["",
              STYLE, "",
              "Mood: a scrappy, determined little demon kid ready to fight (a game hero's first form), cute but not a mascot, not scary. "
              "Both arms, both legs, both wings and the tail stay attached to the body exactly as in image 1; the fist really grips the "
              "hook shaft.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same place "
              "and size as in image 1. No sparkles, no dust, no glow, no fire, no speed lines, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, tỉ lệ, chỗ và cỡ từng bộ phận như ảnh 1; vẫn nhận ra cùng dòng với ảnh 2 (da đỏ, mắt vàng xếch, nanh, cánh, đuôi, "
           "móc xích); ít giáp hơn hẳn; tô phẳng, không bóng; tay nắm cán móc; nền trắng tinh."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "khung":
        khung()
    elif cmd == "concept":
        concept()
    else:
        print(__doc__)
