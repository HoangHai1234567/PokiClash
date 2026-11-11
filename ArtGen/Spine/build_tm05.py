"""Gói GPT dòng tm05 của lô 10 tướng mới đảo Thủy (2026-11-11): Sò Ngọc, sinh vật hai mảnh vỏ có gai.

Con gốc tham khảo là monster_3237 của game khác (sò / cầu gai vỏ xanh, gai kem, miệng hồng). Chỉ giữ chủ đề "hai mảnh vỏ có gai";
hình, màu, chi tiết, diễn xuất là của mình. KHÔNG đính ảnh con gốc hay ảnh chụp trang xem vào prompt, chỉ ảnh của dự án.

  dạng 1  Sò Gai     chibi, vỏ tròn xanh đá đêm, gai san hô, màng ngọc lam, một chân mềm, ngọc trai nhỏ trong miệng
  dạng 2  Bạng Vương dạng cuối: vỏ chàm sẫm đứng dựng trên bốn xúc tu, vành đồng thau, răng vỏ, vương miện gai, ngọc trai lớn

    py -3 -I ArtGen/Spine/build_tm05.py          dựng file prompt (dạng 2 chỉ dựng khi đã chọn concept dạng 1)
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm05_1/luot_1_concept.txt
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm05_2/luot_1_concept.txt

Concept Claude chọn chép thành inbox/tm05_<k>/tai_ve/L1_chon.png (chưa phải người dùng duyệt).
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm05"
INBOX = os.path.join(HERE, "inbox")
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
REF_A = os.path.join(INBOX, "vay_lam_1", "tai_ve", "L1_lien.png")
REF_B = os.path.join(INBOX, "huyen_vu_1", "tai_ve", "L1_lien.png")
REF_A2 = os.path.join(INBOX, "vay_lam_3", "tai_ve", "L1_lien.png")
REF_B2 = os.path.join(INBOX, "huyen_vu_3", "tai_ve", "L1_lien.png")


def W(*p):
    return os.path.normpath(os.path.join(*p))


def pk(k):
    return W(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return W(INBOX, f"{CODE}_{k}", "tai_ve")


def chosen(k):
    return W(save_dir(k), "L1_chon.png")


LINE = ("LINE AND COLOUR: the hand-drawn look of images 1 to 3: drawn by hand on paper with a dark-brown ink pen (#2B2118), an "
        "outline about {n} px thick on this canvas, the same weight on every edge, slightly wobbly like a real pen; every area "
        "coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than "
        "the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, no shadow under the creature, "
        "nothing on the background), no white highlights or shine spots (also none on the pearl and none on the shell), no "
        "gloss, no glow, no rim light, no gradients, no 3D look. The only white allowed is one small catchlight dot in each eye. "
        "A darker tone appears only where the design itself has a darker colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure. No text, no labels, no frame, no ground line, no water, no bubbles, no effects around the "
      "creature.")

STAGE = {
    1: ("FORM 1, the young stage: clearly chibi like a monster-collecting game starter: round, plump and compact, big "
        "expressive eyes, few details. Cute but already brave."),
    2: ("FORM 2, the FINAL stage of this two-stage line: fully grown and NOT chibi at all: a big, heavy, battle-hardened sea "
        "monster, the eyes now small, narrow and sharp, armour and weapons, a powerful stance. The coolest and most beautiful "
        "design of the line: fierce, proud and dangerous-looking, but NOT a horror monster and NOT disgusting. Clearly the "
        "same line as form 1 (image 4): the pearl, the coral spines, the turquoise soft body and the concentric growth rings "
        "of the shell stay, everything else grows up and changes."),
}

DESIGN = {
    1: ("THE CREATURE: a young SPIKY CLAM, a pet-like battle creature of the water element: a bivalve with a round, plump "
        "two-part shell, seen from the side in a three-quarter view. The shell's opening (its mouth) is at the FRONT, facing "
        "the viewer's RIGHT; the hinge of the two shells is at the BACK, on the LEFT. The whole shell is round and plump like "
        "a ball, about as tall as it is wide (spines not counted).\n"
        "- TOP SHELL: a fat rounded dome, slate blue (#3D5C9C: a greyish dark BLUE, clearly blue, NOT violet, NOT purple), "
        "with three thin concentric growth lines that follow its rim and one cyan band (#5EC2E0) running along the rim; the "
        "rim is gently scalloped (wavy). A small round hinge knob at the back-left where the two shells meet.\n"
        "- BOTTOM SHELL: a deep round bowl of the same slate blue with the same cyan rim band and wavy rim, a little smaller "
        "than the top shell.\n"
        "- SPINES: EXACTLY five short, thick cone spines stand out of the top shell like sea-urchin spines, spread over its "
        "upper curve, each pointing straight out from the shell and leaning a little backward; EXACTLY two smaller cone spines "
        "stand under the bottom shell pointing down and back. Each spine is ONE flat coral-orange (#F07F55) with only a small "
        "pale-peach cap at the very tip (#FFD2B4); a spine is never split lengthwise into a light side and a dark side. Every "
        "spine is clearly separate: an ink line where it meets the shell, white space between neighbouring spines.\n"
        "- SOFT BODY inside the shell: turquoise (#36C2B4) with a few small slate-blue dots. Along the edge of each shell a "
        "soft, wavy, frilly turquoise mantle lip shows between the shell rims. The shell is opened at the front like a mouth "
        "in a brave battle shout (the gap about 110 px at the front, closing to nothing at the hinge), so we see inside: the "
        "inside of the mouth is deep raspberry (#B83A5A), and a small round pearl rests on the lower lip: ONE flat cream colour "
        "(#F5F0E6) with one flat lilac patch (#D8CCF0) on its lower part, NO white shine dot, NO highlight.\n"
        "- FACE: two big round eyes peek out from just under the front rim of the top shell, set in the turquoise mantle above "
        "the mouth, side by side at the same height, BOTH pupils looking straight to the right at the enemy (the near eye a "
        "little bigger): white eyeballs, a big golden-amber iris (#F2B33D), a dark navy pupil and one small white catchlight "
        "dot each. The upper eyelids are flat and slant down toward the front (a confident frown), and the top shell rim sits "
        "low over them like a heavy brow, so the face looks brave and determined, a little fighter: cute but NOT goofy, NOT a "
        "happy mascot, NOT scary, NOT googly eyes.\n"
        "- THREE short curly turquoise tentacles, like little whiskers (each a small, fairly thick tapering curl about as long "
        "as one eye is wide), stick out of the front corner of the mouth, pointing forward to the right, not crossing each "
        "other.\n"
        "- FOOT: under the front half of the bottom shell a fat, short, rubbery foot of lighter turquoise (#7ED8CB) comes out, "
        "shaped like a big thumb bending forward to the right with a rounded tip; the creature stands and hops on it. It is "
        "NOT a thin stem and NOT a mushroom stalk. It has NO legs and NO arms.\n"
        "- Do NOT draw: a tongue hanging out, black empty eye holes, a purple or violet shell, a face drawn on the outside of "
        "the shell."),
    2: ("THE CREATURE: the grown, final form of the spiky clam of image 4, now a PEARL-FORTRESS CLAM KING: a huge armoured "
        "bivalve that stands UPRIGHT on four thick tentacle legs, seen from the side in a three-quarter view, the shell's "
        "opening (its jaws) facing the viewer's RIGHT, the hinge at the back-LEFT. It is much taller than form 1: the shell "
        "stands up on its edge like a giant open-jawed head held high on the tentacles, a completely new silhouette.\n"
        "- SHELL: two big heavy shell halves, deep indigo blue (#232A66, a very dark blue, not purple), each with concentric growth ridges and one teal band "
        "(#1F9AA8) along the rim. The top shell is longer and juts forward over the jaws like a helmet visor. A riveted "
        "brass armour band (#C9923C) runs along the rim of each shell, and a brass cap covers the hinge knob at the back.\n"
        "- FANGS: the rims of both shells are serrated into a row of short, thick, bone-white tooth points (#F0E4CA), like the "
        "jaws of a beast, the top row overlapping the bottom row a little at the sides.\n"
        "- CROWN OF SPINES: five LONG, curved crimson-coral spines (#D2493A) with bone-white tips sweep backward from the top of "
        "the top shell like a crown or a war crest (the middle one the longest, about as long as the shell is high); three "
        "shorter crimson spines stand out from the bottom shell pointing down and back. Every spine is clearly separate with "
        "white space between them; each spine meets the shell with a plain ink line (no white ring around its base) and is "
        "one flat crimson with only its tip bone-white, never split lengthwise into a light and a dark side.\n"
        "- SOFT BODY: deep teal (#15827F) with small indigo dots. A wavy, frilly mantle lip shows along both shell rims. The "
        "jaws are open wide (about 30 degrees), so we see inside: the inside of the mouth is deep raspberry (#9E2E4D), a fat "
        "teal tongue lies along the lower jaw, and on it sits a BIG round pearl (#EFEAF7) about as wide as a quarter of the "
        "shell, marked with one flat pale-cyan swirl (#9FD8F0), no shine, no glow. Two short curled teal tentacles hang from "
        "the corners of the jaws.\n"
        "- FACE: two small, narrow, fierce eyes set deep under the brass-edged visor of the top shell, both looking right: "
        "golden iris (#F2B33D), dark slit pupil, one tiny catchlight each, a heavy frowning brow line. Proud and battle-ready.\n"
        "- LEGS: FOUR thick muscular tentacles of deep teal (#15827F) with round cream suckers (#F0E2C4) on their undersides "
        "come out from under the shell: two in front, two behind, each one separate, splayed wide, curling outward at the tip "
        "and planted on the ground like the legs of a strong beast in a fighting stance. They do NOT cross each other or the "
        "shell.\n"
        "- Do NOT draw: a tongue hanging out of the mouth, black empty eye holes, a purple shell, a face drawn on the outside of "
        "the shell, water or effects."),
}

POSE = {
    1: ("POSE (very important: the picture will be cut into parts and animated with a 2D skeleton, so the parts must be "
        "readable and must not overlap):\n"
        "- Side three-quarter view turned toward the viewer's RIGHT; the mouth opening and the eyes are at the right.\n"
        "- The shell is slightly open at the front so the mantle lips, the inside of the mouth and the pearl are clearly seen.\n"
        "- Nothing covers the eyes. The spines, the whisker tentacles and the foot do not cross each other or the eyes."),
    2: ("POSE (very important: the picture will be cut into parts and animated with a 2D skeleton, so the parts must be "
        "readable and must not overlap):\n"
        "- Side three-quarter view turned toward the viewer's RIGHT; the open jaws and the eyes are at the right, facing an "
        "enemy on the right.\n"
        "- The jaws are open wide enough that the fangs, the inside of the mouth, the tongue and the big pearl are clearly seen.\n"
        "- The four tentacle legs are clearly separate from each other; the spines do not cross each other; nothing covers "
        "the eyes."),
}

FRAME = {
    1: ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background. The whole creature is visible (all spines and the "
        "foot included), nothing cut by the edges, at least 80 px of white margin all round. It is centred, about 660 px wide "
        "and about 540 px tall from the tip of the highest spine to the bottom of the foot; its lowest point is about 150 px "
        "above the bottom edge."),
    2: ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background. The whole creature is visible (the whole crown of "
        "spines and the tips of all four tentacles included), nothing cut by the edges, at least 60 px of white margin all "
        "round. It is centred, about 760 px tall from the tip of the highest spine to the lowest tentacle tip and about 820 "
        "px wide; its lowest point is about 90 px above the bottom edge."),
}


def refs(k):
    r = [(WORLD_STYLE, "the game's approved hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen "
                       "outline + coloured pencil / wax crayon hatching), nothing of its content",
          "Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền giấy kem): bản đồ đảo vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. "
          "Chỉ lấy nét"),
         (REF_A, "an approved hero of the same game (a chibi shark), 1536x1024, white background: match EXACTLY its pen line, "
                 "crayon hatching, flat colouring, brave frowning eyes and level of detail. Do NOT copy its species, design, "
                 "colours or pose",
          "Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): cá mập chibi xanh lam bụng trắng, mắt hổ phách cau có; lấy nét bút, "
          "vân sáp, độ chi tiết, ánh mắt"),
         (REF_B, "another approved hero of the same game (a chibi turtle), 1536x1024, white background: see how a hard shell is "
                 "drawn in this style (flat colour areas, thick even outline, crayon texture). Do NOT copy its species, "
                 "shell pattern, colours or pose",
          "Huyền Vũ dạng 1 đã duyệt (1536 × 1024, nền trắng): rùa chibi xanh lá, mai lục sẫm vân lục giác vàng; lấy cách vẽ vỏ "
          "cứng tô phẳng")]
    if k == 2:
        # dạng cuối: mốc nét lấy hai dạng cuối đã duyệt (dữ, giáp), không lấy hai con chibi kẻo GPT vẽ lại chibi
        r[1:3] = [
            (REF_A2, "an approved FINAL-FORM hero of the same game (a fierce adult shark), 1536x1024, white background: match "
                     "EXACTLY its pen line, crayon hatching, flat colouring and level of detail, and its fierce, grown-up, "
                     "battle-ready attitude. Do NOT copy its species, design, colours or pose",
             "Vây Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): cá mập trưởng thành xanh chàm sọc trắng, nhe răng, dữ; lấy nét "
             "bút, vân sáp, thần thái dạng cuối"),
            (REF_B2, "another approved FINAL-FORM hero of the same game (an armoured adult turtle), 1536x1024, white background: "
                     "see how a hard shell with metal ornament is drawn in this style (flat colour areas, thick even outline, "
                     "crayon texture). Do NOT copy its species, shell pattern, colours or pose",
             "Huyền Vũ dạng 3 đã duyệt (1536 × 1024, nền trắng): rùa giáp, mai sẫm viền vàng, rắn trên lưng; lấy cách vẽ vỏ cứng "
             "có giáp kim loại tô phẳng")]
        r.append((chosen(1), "FORM 1 of THIS creature line (the young spiky clam), 1536x1024, white background: the new form "
                             "is its grown-up final form: keep its pearl, its coral spines (now longer and crimson), its "
                             "turquoise soft body (now deep teal) and the growth rings of its shell; do NOT copy its chibi "
                             "proportions, its round shape, its single foot or its colours: the new form is bigger, "
                             "darker, stronger and cooler",
                  "Concept dạng 1 Sò Gai Claude đã chọn (1536 × 1024, nền trắng): sò tròn chibi vỏ xanh đá đêm, gai san hô, "
                  "màng ngọc lam, mắt hổ phách, ngọc trai nhỏ, một chân mềm"))
    return r


def check(r):
    missing = [W(p) for p, _, _ in r if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def prompt(k):
    r = refs(k)
    check(r)
    out = W(save_dir(k), "L1_concept.png")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(p)}: {en}" for i, (p, en, _) in enumerate(r, 1)]
    t += ["", f"SAVE: save it as a PNG to {out}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not "
          "edit, move or delete any other file.", "",
          "TASK: design and draw ONE creature hero as ONE full-body picture, in a clean animation-ready pose, in the "
          "hand-drawn style of images 1 to 3.", "",
          STAGE[k], "", DESIGN[k], "", FRAME[k], "", POSE[k], "",
          LINE.format(n=7), FLAT, BG]
    os.makedirs(pk(k), exist_ok=True)
    os.makedirs(save_dir(k), exist_ok=True)
    p = W(pk(k), "luot_1_concept.txt")
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return p, out, r


CHECK_VN = {
    1: ["Sò chibi tròn mập, nhìn nghiêng 3/4 **quay sang phải**: miệng vỏ (khe mở) và mắt ở bên phải, bản lề ở sau bên trái.",
        "Vỏ trên và vỏ dưới xanh đá (`#3D5C9C`, lam xám, không ngả tím), vân tăng trưởng đồng tâm, một dải xanh lơ ở mép, mép lượn sóng.",
        "Đúng năm gai nón san hô trên vỏ trên, hai gai nhỏ dưới vỏ dưới, mỗi gai một màu phẳng, chỉ chóp hồng đào (không tô hai nửa sáng tối); gai rời nhau, không chạm mắt.",
        "Màng ngọc lam lượn sóng ở mép hai vỏ; khe mở thấy lòng miệng đỏ mâm xôi và một ngọc trai kem nhỏ (không bóng).",
        "Hai mắt to ngang nhau, cùng nhìn sang phải, tròng hổ phách, mí trên phẳng xếch (mặt quả quyết, không mắt lồi ngớ ngẩn); ba xúc tu cong nhỏ ở khoé miệng.",
        "Một chân mềm mập như ngón cái cong ra trước (không phải thân nấm); không tay, không chân khác.",
        "Tô phẳng: không bóng, không điểm sáng trên ngọc/vỏ (chỉ chấm sáng nhỏ trong mắt), nền trắng tinh, không nước, không "
        "bọt."],
    2: ["Hết chibi: sò lớn **đứng dựng** trên bốn xúc tu, hàm vỏ há quay sang phải, bóng dáng khác hẳn dạng 1 (cao, không tròn).",
        "Vỏ chàm sẫm (`#232A66`), vân đồng tâm, dải xanh mòng két, vành đồng thau có đinh tán, nắp đồng ở bản lề.",
        "Mép vỏ răng cưa trắng ngà như hàm thú; vương miện năm gai dài đỏ san hô sẫm cong ra sau, ba gai dưới vỏ dưới.",
        "Trong miệng: lòng đỏ mâm xôi, lưỡi xanh mòng két, ngọc trai lớn có vệt xoáy xanh lơ (không bóng, không phát sáng).",
        "Mắt nhỏ, hẹp, dữ dưới mép vỏ trên; bốn xúc tu tách rời, giác bám kem, thế đứng chiến.",
        "Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh."],
}

FIX_VN = [
    ("Có bóng, mảng sáng tối, ngọc/vỏ bóng loáng",
     "Flat colour only: remove every shadow, highlight, shine spot and gradient (also on the pearl and the shell); keep the "
     "crayon hatching as texture."),
    ("Quay sang trái", "The creature must face the viewer's RIGHT: mouth opening and eyes on the right, hinge on the left."),
    ("Mắt là hốc đen / mặt vẽ ngoài vỏ",
     "The eyes are big round eyes with white eyeballs and amber irises, peeking out of the soft body under the top shell rim, "
     "not black holes and not drawn on the outside of the shell."),
    ("Gai dính nhau, chạm mắt", "Keep every spine clearly separate with white space between them; nothing touches the eyes."),
    ("Vỏ khép kín, không thấy lòng miệng",
     "Open the shell a little more at the front so the inside of the mouth and the pearl are clearly visible."),
    ("Có nước, bọt, hiệu ứng quanh con", "Remove all water, bubbles and effects: only the creature on pure white."),
    ("Mắt lồi ngớ ngẩn, hai mắt nhìn hai hướng",
     "Both eyes level and both looking straight to the right, flat slanted upper lids: a brave, determined frown, not goofy."),
    ("Vỏ ngả tím", "The shell must be a greyish slate BLUE (#3D5C9C), not violet or purple."),
]
FIX_VN2 = [
    ("Vẫn chibi, vẫn tròn",
     "Not chibi at all: make it a huge armoured clam standing UPRIGHT on four thick tentacle legs, the eyes small and narrow, "
     "a tall silhouette completely different from form 1."),
    ("Xúc tu chéo nhau",
     "The four tentacle legs must be clearly separate, splayed wide, none crossing another or the shell."),
]


# ------------------------------------------------------------------ lượt 2: tờ mảnh (pha 2, concept đã duyệt 2026-11-11)
PIECES = ("THIS IS A SHEET OF SEPARATE PARTS for a 2D cut-out animation rig, NOT a scene: every part is drawn COMPLETE and on "
          "its own (also the areas that are hidden behind other parts in the concept), flat on the white page like stickers "
          "laid out on a table, with at least 60 px of pure white between any two parts and between a part and the image edge. "
          "No part touches or overlaps another. Do not draw a whole creature, do not draw extra parts, do not draw labels, "
          "numbers, arrows or guide lines.")
SPINE_BASE = ("The BASE of every spine is a plain, wide, slightly rounded end closed by the ink outline (it will be tucked under "
              "the shell): no white ring, no white gap, no socket, no shell drawn around it.")

STEPS = {
    2: [
        ("M01", "shell halves",
         "Canvas 1536 x 1024. Two parts side by side, each centred in its half of the canvas (left half and right half):\n"
         "- LEFT: the UPPER HALF of the creature of image 2, seen exactly as in image 2 (same three-quarter side view facing "
         "the viewer's RIGHT, same angle and proportions): the deep-indigo domed TOP SHELL with its growth ridges and teal band, "
         "the riveted brass band along its rim, the brass visor jutting forward at the front, the brass hinge cap at the "
         "back-left end; under the visor the deep-teal soft FACE with the two small fierce golden eyes OPEN; along the whole "
         "lower edge the wavy teal mantle lip, and hanging from it the row of upper fangs. The fangs are short, thick and "
         "bone-white with slightly ROUNDED tips (fierce but not creepy, not needle-sharp). Do NOT draw: any spine (the top of "
         "the shell is smooth: the spines are separate parts), the little crown, the lower shell, the tongue, the pearl, the "
         "inside of the mouth, the tentacles. About 680 px wide and 440 px tall.\n"
         "- RIGHT: the LOWER HALF, seen as in image 2: the deep-indigo BOTTOM SHELL bowl with growth ridges and teal band, the "
         "riveted brass band along its rim, the wavy teal mantle lip along its whole upper edge with the row of lower fangs "
         "standing on it (same slightly rounded tips); its back-left end is a rounded stub. Do NOT draw: spines, tentacles, "
         "tongue, pearl, the upper shell. About 660 px wide and 320 px tall.",
         "nửa trên (vỏ trên, vành đồng, lưỡi trai, mặt mòng két hai mắt mở, màng mép, hàng răng trên chóp bo tròn, không gai, "
         "không mũ miện) và nửa dưới (vỏ dưới, vành đồng, màng mép, hàng răng dưới)"),
        ("M02", "mouth and small parts",
         "Canvas 1536 x 1024, a 3 x 2 grid of 512 px cells, the part(s) of each cell centred in it:\n"
         "- top-left: the MOUTH INSIDE: one big rounded shape of flat deep raspberry (#9E2E4D) like a wide rounded fan or a "
         "half disc lying on its flat side, with a darker throat area (#7A2140) toward its LEFT end; it is the inside of the "
         "mouth seen when the shell opens wide, drawn whole. About 440 px wide and 320 px tall. No teeth, no tongue, no pearl.\n"
         "- top-middle: the TONGUE alone: a fat deep-teal tongue (#15827F) with one thin darker line along its middle, drawn "
         "perfectly STRAIGHT and horizontal, the root on the LEFT thick and cut off flat, the tip on the RIGHT rounded. About "
         "400 px long and 90 px thick.\n"
         "- top-right: the big PEARL alone: a circle of flat pale lilac-white (#EFEAF7) with the flat pale-cyan swirl (#9FD8F0), "
         "no shine, no highlight, no glow. About 220 px across.\n"
         "- bottom-left: the LITTLE CROWN alone: the small brass crown (#C9923C) with its blue gem, as on top of the visor in "
         "image 2, its flat base at the bottom. About 210 px wide.\n"
         "- bottom-middle: TWO CLOSED-EYE PATCHES side by side with white between them: each a small almond-shaped patch of the "
         "deep-teal face skin with a curved dark closed-eye line and a short frowning brow line above it, made to cover one of "
         "the open eyes of image 2: the left one about 130 px wide (near eye), the right one about 110 px wide (far eye).\n"
         "- bottom-right: TWO MOUTH-CORNER TENTACLES one above the other: short tapering deep-teal tentacles with small cream "
         "suckers along the bottom edge, drawn almost STRAIGHT and horizontal (thick root on the LEFT cut off flat, thin tip on "
         "the RIGHT with only a small curl): about 260 px and 210 px long.",
         "lòng miệng (quạt tròn đỏ mâm xôi), lưỡi duỗi ngang, ngọc trai lớn, mũ miện đồng, hai mí nhắm, hai xúc tu khoé hàm"),
        ("M03", "tentacle legs and spines",
         "Canvas 1536 x 1024. Parts:\n"
         "- top area: TWO LEG TENTACLES, one above the other, each laid out perfectly STRAIGHT and horizontal like a long "
         "tapering tube seen from the side: thick muscular deep-teal (#15827F) tentacles with small indigo dots, a row of round "
         "cream suckers (#F0E2C4) along the BOTTOM edge, the root on the LEFT thick and cut off flat (it will be hidden under "
         "the shell), tapering to the RIGHT into a tip that curls up only a little. Draw them LONG: the upper one about 760 px "
         "long and 125 px thick at the root, the lower one about 680 px long and 105 px thick.\n"
         "- lower area: EIGHT separate SPINES in a row, each standing upright with its base at the bottom: FIVE long crown "
         "spines curving backward (their tips bending to the LEFT, like the crown in image 2), about 320, 290, 260, 220 and 180 "
         "px tall; then THREE short straight spines about 130, 110 and 95 px tall. Each spine is one flat crimson (#D2493A) with "
         "only its tip bone-white (#F0E4CA), never split lengthwise into a light and a dark side. " + SPINE_BASE,
         "hai xúc tu chân duỗi thẳng ngang (760 và 680 px), tám gai rời đứng (năm gai vương miện cong, ba gai ngắn), chân gai "
         "không có khe trắng"),
    ],
    1: [
        ("M01", "shell halves",
         "Canvas 1536 x 1024. Two parts side by side, each centred in its half of the canvas (left half and right half):\n"
         "- LEFT: the UPPER HALF of the creature of image 2, seen exactly as in image 2 (same three-quarter side view facing "
         "the viewer's RIGHT, same angle and proportions): the slate-blue domed TOP SHELL with its growth lines and the cyan "
         "rim band, the round hinge knob at the back-left end, and under its front rim the turquoise soft body with the few "
         "slate-blue dots and the two big golden-amber eyes OPEN (the same determined frown as image 2), down to the frilly "
         "turquoise mantle lip along its whole lower edge (the upper lip of the open mouth). Do NOT draw: any spine (the shell "
         "is smooth: the spines are separate parts), the whisker tentacles, the lower shell, the inside of the mouth, the "
         "pearl, the foot. About 640 px wide and 360 px tall.\n"
         "- RIGHT: the LOWER HALF, seen as in image 2: the slate-blue BOTTOM SHELL bowl with growth lines and the cyan rim band, "
         "and the frilly turquoise mantle lip along its whole upper edge (the lower lip of the mouth). Its back-left end is a "
         "rounded stub. Do NOT draw: spines, foot, pearl, the upper shell. About 600 px wide and 280 px tall.",
         "nửa trên (vỏ trên, núm bản lề, thân ngọc lam có hai mắt mở, môi trên lượn sóng, không gai) và nửa dưới (vỏ dưới, môi "
         "dưới lượn sóng)"),
        ("M02", "mouth and small parts",
         "Canvas 1536 x 1024, a 3 x 2 grid of 512 px cells, the part(s) of each cell centred in it:\n"
         "- top-left: the MOUTH INSIDE: one big rounded shape of flat deep raspberry (#B83A5A) like a wide rounded fan or a "
         "half disc lying on its flat side, with a darker throat area (#8E2A45) toward its LEFT end, drawn whole. About 380 px "
         "wide and 260 px tall. No teeth, no pearl.\n"
         "- top-middle: the small PEARL alone: a circle of flat cream (#F5F0E6) with one flat lilac patch (#D8CCF0) on its lower "
         "part, no shine, no highlight. About 130 px across.\n"
         "- top-right: the FOOT alone: the fat soft rubbery foot of lighter turquoise (#7ED8CB), drawn as a thick sausage lying "
         "STRAIGHT and horizontal, the root on the LEFT cut off flat (it will be hidden under the shell), the rounded tip on the "
         "RIGHT bending only a little. About 330 px long and 130 px thick.\n"
         "- bottom-left: TWO CLOSED-EYE PATCHES side by side with white between them: each a round patch of the turquoise skin "
         "with a curved dark closed-eye line and a short frowning brow line, made to cover one of the big open eyes of image 2: "
         "the left one about 150 px wide (near eye), the right one about 125 px wide (far eye).\n"
         "- bottom-middle and bottom-right together: THREE WHISKER TENTACLES one above the other: short tapering turquoise "
         "tentacles (#36C2B4), drawn almost STRAIGHT and horizontal (thick root on the LEFT cut off flat, thin tip on the RIGHT "
         "with only a small curl): about 300, 260 and 220 px long and about 34 px thick at the root.",
         "lòng miệng, ngọc trai nhỏ, chân mềm duỗi ngang, hai mí nhắm, ba xúc tu râu duỗi ngang"),
        ("M03", "spines",
         "Canvas 1536 x 1024. SEVEN separate SPINES in one row across the middle of the canvas, each standing upright with its "
         "base at the bottom: FIVE short thick cone spines like sea-urchin spines (about 190, 180, 170, 160 and 150 px tall, "
         "about 85 px wide at the base) and TWO smaller ones (about 120 and 110 px tall). Each spine is one flat coral-orange "
         "(#F07F55) with only a small pale-peach cap at the very tip (#FFD2B4), never split lengthwise into a light and a dark "
         "side. " + SPINE_BASE,
         "bảy gai nón rời đứng (năm to, hai nhỏ), chân gai không có khe trắng"),
    ],
}


def prompt_manh(k):
    r = [refs(k)[0],
         (chosen(k), f"the APPROVED CONCEPT of this creature (form {k}), 1536x1024: every part you draw belongs to THIS creature: "
                     "same design, same colours, same line and crayon texture. Use it only to know what the parts look like; do "
                     "not redraw the whole creature",
          f"Concept dạng {k} đã duyệt (1536 × 1024, nền trắng)")]
    check(r)
    sv = save_dir(k)
    order = [s[0] for s in STEPS[k]]
    t = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image per step "
         "and save each one as its step says. Do not reply with text only.", "",
         "REFERENCE IMAGES (open each file from its full path):"]
    t += [f"image {i} = {W(p)}: {en}" for i, (p, en, _) in enumerate(r, 1)]
    t += ["", "WHAT THIS IS: sheets of separate, complete parts of the creature of image 2, for a 2D cut-out animation rig. The "
          "animation software opens and closes the two shell halves, bends the straight tentacles and the tongue with bones, "
          "and wobbles every spine on its own, so every part must be drawn whole (also the areas hidden in image 2), clean, "
          "and well separated from the others.", "",
          f"SAVE: every step's image goes into {sv} under the step's name (for example {order[0]}.png). If that file already "
          "exists, add _2, _3 ... before .png. Do not change, move or delete any other file.", "",
          f"ORDER: draw step {order[0]} now, save it and stop. Each time I say \"next\", draw the next step, save it and stop, in "
          f"this order: {', '.join(order[1:])}.", ""]
    for sc, title, en, _ in STEPS[k]:
        t += [f"=== STEP {sc} ({title}) ===", PIECES, en, "", LINE.replace("images 1 to 3", "images 1 and 2").format(n=7), FLAT,
              BG.replace(" no water, no bubbles, no effects around the creature.", ""),
              f"SAVE this step: save it as a PNG to {W(sv, sc + '.png')} (if that file already exists, save it as {sc}_2.png, "
              f"{sc}_3.png ... in the same folder instead). Do not change, move or delete any other file.", ""]
    p = W(pk(k), "luot_2_manh.txt")
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return p, r


def build():
    made = []
    for k in (1, 2):
        if k == 2 and not os.path.exists(chosen(1)):
            print("(chưa dựng dạng 2: chưa có", chosen(1) + ")")
            continue
        p, out, r = prompt(k)
        made.append(p)
        name = {1: "Sò Gai (dạng 1, chibi)", 2: "Bạng Vương (dạng 2, dạng cuối)"}[k]
        gd = [f"# Gói gửi GPT: {name}, dòng Sò Ngọc (`{CODE}_{k}`)", "",
              "Lô 10 tướng mới đảo Thủy, dòng 5 (thay suất ải 20, Ma Kết). Một lượt: concept trọn con một ảnh, nền trắng, dáng "
              "dễ tách mảnh. Không có ảnh con gốc nào trong gói (chỉ ảnh của dự án).", "",
              f"**Chỉ gửi GPT đường dẫn:** `{p}`", "",
              f"**GPT lưu ảnh vào:** `{out}` (trùng tên thì `L1_concept_2.png`, `_3`… cùng thư mục).", "",
              f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_1_concept.txt` (chạy nền, "
              "khoá Codex chung). Bản Claude chọn chép thành `L1_chon.png` cùng thư mục.", "",
              "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{W(pp)}` | {vi} |" for i, (pp, _, vi) in enumerate(r, 1)]
        gd += ["", "## Kiểm ảnh", ""] + [f"- {c}" for c in CHECK_VN[k]]
        gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat)", "", "| Sai | Gửi thêm |", "|---|---|"]
        gd += [f"| {a} | `{b}` |" for a, b in FIX_VN + (FIX_VN2 if k == 2 else [])]
        if os.path.exists(chosen(k)):
            p2, r2 = prompt_manh(k)
            made.append(p2)
            order = ",".join(s[0] for s in STEPS[k])
            gd += ["", "## Lượt 2: tờ mảnh (concept đã duyệt 2026-11-11)", "",
                   f"**Chỉ gửi GPT đường dẫn:** `{p2}`. Vẽ lần lượt {order.replace(',', ', ')}, gõ `next` sau mỗi ảnh. GPT lưu "
                   f"vào `{save_dir(k)}` (`M01.png`…; trùng tên thì `_2`, `_3`).", "",
                   f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_2_manh.txt --steps "
                   f"{order}`.", "", "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
            gd += [f"| {i} | `{W(pp)}` | {vi} |" for i, (pp, _, vi) in enumerate(r2, 1)]
            gd += ["", "Kiểm từng tờ (1536 × 1024, nền trắng, mảnh rời nhau ít nhất 60 px, tô phẳng, không bóng):", ""]
            gd += [f"- **{sc}**: {vi}" for sc, _, _, vi in STEPS[k]]
            gd += ["", "| Sai | Gửi thêm |", "|---|---|",
                   "| Vẽ cả con thay vì mảnh rời | `This must be a sheet of separate parts laid flat on white, not a creature. "
                   "Redraw only the parts listed.` |",
                   "| Gai vẽ dính trên vỏ | `The shell halves must be smooth with no spines; the spines are separate parts on "
                   "another sheet.` |",
                   "| Xúc tu, lưỡi vẽ cong | `The tentacles and the tongue must be drawn straight and horizontal, root on the left "
                   "cut off flat.` |",
                   "| Chân gai có vòng trắng | `The base of each spine is a plain ink-closed end, no white ring or gap.` |"]
        open(W(pk(k), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    for p in made:
        print(p)


if __name__ == "__main__":
    build()
