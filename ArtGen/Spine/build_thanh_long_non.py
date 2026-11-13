# -*- coding: utf-8 -*-
"""Gói gửi GPT cho DẠNG 1 và DẠNG 2 của Thanh Long (suất 10 đảo Mộc, boss, id thanh_long; dạng 3 = rồng trúc bốn cánh moc_vuong_1).
Người dùng 2026-11-13: "tạo thêm dạng 1/2 cho tướng thứ 10", chọn hướng "con non → thiếu niên → boss". Ảnh mẫu bố cục: rig dạng 3
(Resources/moc_vuong_1/moc_vuong_1.atomik) đổi tỉ lệ xương theo inbox/thanh_long_non/mau/ti_le_d<k>.json, chụp khung 0 idle bằng runtime
Spine thật:

    py -3 -I ArtGen/Spine/mo_xe/atomik_bocuc.py "Assets/03 Art/Heroes/Resources/moc_vuong_1/moc_vuong_1.atomik" \
        ArtGen/Spine/inbox/thanh_long_non/mau/ti_le_d1.json ArtGen/Spine/inbox/thanh_long_non/mau/bo_cuc_d1.png idle 0 --w 1536 --h 1024 \
        --khung -260,-30,370,390          (dạng 2: ti_le_d2.json, bo_cuc_d2.png, --khung -300,-30,360,410)

    py -3 -I ArtGen/Spine/build_thanh_long_non.py       → ArtGen/Spine/gui_gpt/thanh_long_non/ (luot_1_concept_d1.txt, luot_1_concept_d2.txt, HUONG_DAN.md)
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "gui_gpt", "thanh_long_non")
BASE = os.path.join(HERE, "inbox", "thanh_long_non")
DUYET = os.path.join(HERE, "inbox", "moc_vuong_1", "tai_ve", "L1_duyet.png")
TAI_VE = os.path.join(BASE, "tai_ve")

CHUNG_IMG2 = (f"image 2 = {DUYET}: the approved FINAL form of the same creature, 1536x1024, white background: a four-winged bamboo "
              "dragon king (ink-charcoal fur, a big cream mane, two huge bamboo-shoot horns built of charcoal sheath scales with ivory-gold "
              "edges, a gold collar armour with a jade stone and gold shoulder guards, upper wings of layered dark-to-light green bamboo "
              "leaves, lower wings of ivory-gold dry bamboo leaves, two thin vine tendrils with red buds, one long green leaf ribbon as a "
              "tail, legs in charcoal greaves with gold bands). It gives the drawing style (wobbly dark-brown ink line, crayon hatching, "
              "completely flat colour) and the family look.")

D = {
    "d1": dict(
        ten="L1_d1.png", tuoi="the YOUNGEST form (the first evolution stage, a hatchling)",
        guide=("a computer-assembled puppet of the HATCHLING form of this dragon, built from the final form's own pieces rescaled on the "
               "animation skeleton (big head and mane, tiny horns, four tiny wings mostly hidden behind the body, a short tail, short legs)"),
        char=("a brave little bamboo dragon hatchling: big-headed, round, compact and endearing, but with a determined, battle-ready little "
              "glare and a firm crouching stance; not a smiling baby mascot, not scary. It has NO gold armour yet: where the grown dragon "
              "wears armour, the hatchling is wrapped in fresh young bamboo sheath leaves."),
        head=("- HEAD AND FACE (about x = 700 to x = 1020, y = 250 to y = 500): a BIG, round young dragon head of ink-charcoal fur (#46504B) "
              "with a SHORT rounded muzzle (tip at about (1015, 465)), one nostril, a small mouth shut in a firm line with only TWO tiny "
              "blunt fangs; ONE eye at about (910, 400): clearly BIGGER and ROUNDER than the final form's (about 60 px wide), ivory-gold "
              "(#ECC450) iris, a big round dark pupil, one tiny white dot, a clean ink rim, a SHORT slanted brow stroke above it tilting "
              "down toward the muzzle (a determined frown). A pointed ear at the back of the head (about (915, 300)). No second eye.\n"
              "- HORNS: two tiny bamboo-shoot BUDS (the grown dragon's horns as just-sprouted shoots): each a short, fat cone of two or "
              "three overlapping sheath scales, charcoal (#3A4440) with ivory-gold (#ECC450) edges and an ivory-gold tip; the near bud "
              "rises from the top of the head at about (760, 255) to its tip at about (715, 150); the far bud from about (950, 270) to "
              "about (962, 200).\n"
              "- MANE (about x = 585 to x = 990, y = 170 to y = 560): a soft, fluffy cream (#F2E6C8) baby mane in the same place and size "
              "as image 1, in big rounded tufts."),
        keep=("the four small wings (green bamboo leaves at the upper left and the small leaves at the right, the yellow leaves at the "
              "lower left), the neck plates, the collar and the two shoulder pieces, the round chest gem and the pale leaf under it, the "
              "body, the four legs with their greaves and paws, the leaf-ribbon tail"),
        rest=("- WINGS: the small leaf wings exactly where image 1 has them (upper wings about x = 440 to x = 680, y = 375 to y = 700 and a "
              "little at x = 860 to x = 1000, y = 500 to y = 560; lower wing leaves about x = 530 to x = 680, y = 580 to y = 760): young "
              "fresh greens (#3E8E58, #5FB066, #9CD67A) for the upper ones and pale young yellow-green (#CFD86A) for the lower ones.\n"
              "- NECK PLATES (about x = 790 to x = 880, y = 420 to y = 830): pale ivory (#E8DDB0) plates like young bamboo nodes.\n"
              "- COLLAR AND SHOULDERS (about x = 640 to x = 980, y = 550 to y = 760): NOT armour: the same shapes as image 1 drawn as "
              "fresh bamboo SHEATH LEAVES (#6FB860 with darker veins #3E8E58) wrapped around the shoulders and the chest; the round gem in "
              "the middle (about (850, 615)) is a small jade-green (#3FB58A) bud; the pale piece under it is a pale young leaf (#E8DDB0).\n"
              "- BODY AND LEGS: ink-charcoal fur (#46504B); the greaves on the legs are young green bamboo (#6FB860) with pale ivory "
              "(#E8DDB0) node rings instead of gold bands; paws charcoal with ivory-gold (#ECC450) claws. Feet at about x = 430 to "
              "x = 560, x = 660 to x = 860 and x = 1000 to x = 1150, all at y = 880 to y = 950.\n"
              "- TAIL: the leaf ribbon (about x = 400 to x = 760, y = 680 to y = 870) is one fresh young bamboo leaf (#5FB066, centre "
              "vein #3E8E58)."),
        colours=("fur #46504B; horn buds #3A4440 with #ECC450; mane #F2E6C8; upper wing leaves #3E8E58, #5FB066, #9CD67A; lower wing "
                 "leaves #CFD86A; bamboo sheath collar and greaves #6FB860; neck plates, node rings, pale leaf #E8DDB0; chest bud #3FB58A; "
                 "claws, eye #ECC450; tail leaf #5FB066; every outline dark-brown ink #2B2118. NO gold armour, NO metal."),
        frame="about 750 px wide (x = 400 to x = 1150) and about 805 px tall (y = 145 to y = 950)"),
    "d2": dict(
        ten="L1_d2.png", tuoi="the MIDDLE form (the second evolution stage, a young dragon)",
        guide=("a computer-assembled puppet of the YOUNG form of this dragon, built from the final form's own pieces rescaled on the "
               "animation skeleton (a slightly bigger head, horns about 60 % of the final length, four wings about two thirds of the final "
               "size, a shorter tail)"),
        char=("a proud young bamboo dragon, half grown: lean and alert, a fierce, determined look, ready to fight; less armour and less "
              "gold than the king it will become; not a cute mascot, not a monster."),
        head=("- HEAD AND FACE (about x = 780 to x = 1000, y = 300 to y = 490): a young dragon head of ink-charcoal fur (#3F4945), a "
              "medium muzzle (shorter than the final form's) with one nostril, two small fangs; ONE eye at about (915, 415), a little bigger "
              "than the final form's, ivory-gold (#ECC450) iris, dark pupil, one tiny white dot, a slanted brow (fierce frown). A pointed "
              "ear at the back of the head. No second eye.\n"
              "- HORNS: two bamboo-SHOOT horns in the approved style of image 2 but only about 60 % as long: each a strong cone of four "
              "overlapping pointed sheath scales, charcoal (#3A4440) with an ivory-gold (#ECC450) edge band on every sheath and an "
              "ivory-gold tip, sweeping up and back; the near horn from about (850, 330) to its tip at about (705, 120); the far horn from "
              "about (960, 320) to about (980, 165).\n"
              "- MANE (about x = 690 to x = 980, y = 290 to y = 560): a cream (#F2E6C8) mane in flame-like locks, in the same place and "
              "size as image 1."),
        keep=("the four wings leaf by leaf, the two vine tendrils with their buds, the neck plates, the collar and the two shoulder "
              "guards, the chest stone and the pale leaf under it, the body, the four legs with their greaves and paws, the leaf-ribbon "
              "tail"),
        rest=("- WINGS: exactly where image 1 has them (upper wings about x = 305 to x = 680, y = 220 to y = 650 and x = 900 to x = 1150, "
              "y = 220 to y = 560; lower wings about x = 500 to x = 700, y = 550 to y = 780 and x = 990 to x = 1115, y = 560 to y = 720): "
              "upper wing leaves in three greens (#2E7A4E, #4FA060, #8CCB6A), lower wing leaves ivory-gold dry bamboo (#E3BE4E).\n"
              "- VINES: two thin vine tendrils (#5A9A48) with a red (#D8452E) bud at about (335, 640) and (1125, 650).\n"
              "- NECK PLATES (about x = 840 to x = 900, y = 440 to y = 760): ivory-gold (#E3BE4E).\n"
              "- COLLAR AND SHOULDERS (about x = 730 to x = 1000, y = 540 to y = 700): LIGHT armour of split bamboo: ivory (#E8DDB0) "
              "bamboo slats with thin gold (#E0B440) edges (much less gold than the final form); the chest stone (about (890, 620)) jade "
              "(#3FB58A); the pale leaf under it ivory (#E8DDB0).\n"
              "- BODY AND LEGS: ink-charcoal fur (#3F4945); greaves charcoal (#3A4440) with ONE gold (#E0B440) band each; claws ivory-gold "
              "(#ECC450). Feet at about x = 500 to x = 610, x = 760 to x = 910 and x = 1005 to x = 1185, all at y = 880 to y = 950.\n"
              "- TAIL: the leaf ribbon (about x = 365 to x = 1160, y = 640 to y = 900) is one long green bamboo leaf (#3E8E58, lighter "
              "underside #4FA060)."),
        colours=("fur #3F4945; horns #3A4440 with #ECC450; mane #F2E6C8; upper wing leaves #2E7A4E, #4FA060, #8CCB6A; lower wing leaves "
                 "and neck plates #E3BE4E; bamboo armour slats, pale leaf #E8DDB0; gold edges and greave bands #E0B440; jade #3FB58A; vines "
                 "#5A9A48; buds #D8452E; claws, eye #ECC450; tail leaf #3E8E58 / #4FA060; every outline dark-brown ink #2B2118."),
        frame="about 880 px wide (x = 305 to x = 1185) and about 830 px tall (y = 120 to y = 950)"),
}


def prompt(k):
    d = D[k]
    bo = os.path.join(BASE, "mau", f"bo_cuc_{k}.png")
    return f"""IMAGES (attached in this order; open each from its path):
image 1 = {bo}: PROPORTION GUIDE, 1536x1024, white background: {d['guide']}. It gives the exact pose, the proportions and the place, size and overlap of every piece. Its colours, its face, its horns and its armour are those of the FINAL form and must be changed as described below.
{CHUNG_IMG2} The new form must clearly be the same species at a younger age.

SAVE: save it as a PNG to {os.path.join(TAI_VE, d['ten'])}
If a file with that name already exists, save as {d['ten'][:-4]}_2.png, {d['ten'][:-4]}_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: draw {d['tuoi']} of the dragon of image 2, as ONE picture, landscape 1536x1024, pure-white background, in the same hand-drawn style. Keep EXACTLY the pose, the proportions and the place and size of every piece of image 1 (the picture will be mapped back onto that skeleton): the same low crouching stance, the body seen from the front-left, the head in three-quarter view looking RIGHT with ONLY ONE eye visible.

CHARACTER: {d['char']}

WHAT CHANGES, WHAT STAYS:
- REDESIGN the HEAD, the FACE, the HORNS and the MANE as described below (these are new drawings).
- KEEP the SHAPE, the place and the size of every other piece exactly as in image 1 and only change its colours and surface as listed: {d['keep']}. (Those pieces will be repainted on the same outlines, so their outlines must stay the same.)

Coordinates are pixels on the 1536x1024 canvas (x from the left, y from the top); they are the places of the pieces in image 1.
{d['head']}
{d['rest']}

COLOURS (use exactly these, each area one flat colour): {d['colours']} Only these colours. NO purple, NO blue, NO grey stone, NO pink.

CANVAS AND FRAMING: as in image 1 the whole figure is {d['frame']}; nothing cut by the edges; no ground, no cast shadow.

POSE (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): calm, clean resting pose exactly as in the guide. Every piece is a clear shape with its own ink outline: head, each horn, mane, every wing leaf, collar, each shoulder piece, chest gem, neck plates, body, each leg, each paw, tail. No falling leaves, no sparkles, no glow, no motion lines, no ground, no grass, no props.

HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly like a real pen; loose crayon hatching inside every area. Image 1 is a rough machine-assembled puppet: take its pose, proportions, placement, sizes and piece outlines, but redraw every part cleanly (do not copy its seams, its thin light lines between pieces, its blurred edges or the final form's face, horns and armour).
LINE AND COLOUR: the hand-drawn look of image 2: drawn by hand on paper with a dark-brown ink pen (#2B2118), an outline about 6 px thick on this canvas around every big piece (head, mane, horns, wings, collar, body, legs, tail), and about 4 px for small details (claws, the eye, leaf veins, sheath edges); every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor an over-rendered painting.
FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do not model light. No shading, no darker underside, no lighter patches, no shadows of any kind (no cast shadow of one piece on another, no shadow under the figure or on the background), no white highlights or shine spots (not on the horns, not on the gem, not on the claws), no gloss, no glow, no rim light, no gradients, no 3D look. The only exception: one tiny light dot in the eye. A different tone appears only where the design itself lists a different colour.
Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects around the character.
"""


HD = """# Gói gen concept dạng 1 và dạng 2 của Thanh Long (suất 10 đảo Mộc, boss)

Dạng 3 là rồng trúc bốn cánh đang có (`moc_vuong_1`). Hai file prompt, mỗi file một lượt gen:
- `luot_1_concept_d1.txt`: **rồng con** (đầu to, sừng là hai mầm măng nhú, bốn cánh lá nhỏ xíu, CHƯA có giáp vàng: cổ áo và vai là bẹ măng
  non xanh, giữa ngực một nụ ngọc) → `tai_ve/L1_d1.png`.
- `luot_1_concept_d2.txt`: **rồng thiếu niên** (sừng măng dài chừng 60 % dạng 3, cánh cỡ 2/3, giáp tre chẻ ngà viền vàng mảnh) → `tai_ve/L1_d2.png`.

Ảnh mẫu (GPT tự mở theo đường dẫn):
1. `inbox/thanh_long_non/mau/bo_cuc_d1.png` / `bo_cuc_d2.png` (1536×1024, nền trắng): rig dạng 3 đổi tỉ lệ (dạng 1: đầu ×1,6, sừng 0,3, cánh
   0,35, đuôi 0,5; dạng 2: đầu ×1,2, sừng 0,6, cánh 0,65, đuôi 0,8), chụp khung 0 idle. Cho dáng, chỗ, cỡ từng mảnh; màu, mặt, sừng, giáp còn là
   của dạng 3.
2. `inbox/moc_vuong_1/tai_ve/L1_duyet.png` (1536×1024): concept dạng 3 đã duyệt (bản tối, sừng măng). Cho nét vẽ, dáng dấp họ hàng.

Cách kiểm: chồng lên bố cục phải trùng dáng và chỗ từng mảnh; một mắt; dạng 1 không có giáp vàng; tô phẳng, không bóng; nền trắng.
Câu sửa nhanh: "keep the exact pose and piece positions of image 1"; "flat colour only, no shading, no highlights";
"no gold armour on the hatchling, only green bamboo sheath leaves".
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(TAI_VE, exist_ok=True)
    for k in D:
        p = os.path.join(OUT, f"luot_1_concept_{k}.txt")
        open(p, "w", encoding="utf-8").write(prompt(k))
        print(p)
    open(os.path.join(OUT, "HUONG_DAN.md"), "w", encoding="utf-8").write(HD)


if __name__ == "__main__":
    main()
