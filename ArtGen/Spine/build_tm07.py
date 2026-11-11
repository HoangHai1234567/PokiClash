# -*- coding: utf-8 -*-
"""Gói GPT dòng tm07 (lô 10 tướng mới đảo Thủy, 2026-11-11): LIÊN KÌNH, cá kỳ lân biển mang hoa sen, thay suất ải 40 (Kuba, epic).

Con gốc tham khảo là dạng 2 (dạng cuối). Thiết kế của mình khác hẳn, chỉ giữ chủ đề "cá voi kỳ lân biển cõng hoa sen":
  dạng 2 (tm07_2) LIÊN KÌNH: trưởng thành, uy nghi, chiến; thân chàm, bụng ngà, sen đỏ thắm nở to, ngà vàng xoắn, vòng vàng.
  dạng 1 (tm07_1) KÌNH NỤ: bé con chibi, thân lam phấn, nụ sen hồng nhạt chưa nở, ngà cụt, mắt to.
Dạng 2 duyệt xong mới dựng prompt dạng 1 (đính concept dạng 2 làm ảnh mẫu).

    py -3 -I build_tm07.py                 dựng file prompt (dạng 1 chỉ dựng khi đã có inbox/tm07_2/tai_ve/L1_duyet.png)
    py -3 -I gen.py gui_gpt/tm07_2/luot_1_concept.txt
    py -3 -I gen.py gui_gpt/tm07_1/luot_1_concept.txt
Rig và animation (pha 2): tm07.py (chưa viết).
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm07"
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
HAI_LONG = os.path.join(HERE, "inbox", "hai_long", "tai_ve", "L1_duyet.png")
MA_KET = os.path.join(HERE, "inbox", "ma_ket_3", "tai_ve", "L1_lien.png")


def W(p):
    return os.path.normpath(p)


def pk(k):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


CONCEPT2 = os.path.join(save_dir(2), "L1_duyet.png")  # concept dạng 2 Claude đã chọn (chép từ L1_concept*.png)

LINE = ("LINE AND COLOUR: the hand-drawn look of the style images: drawn by hand on paper with a dark-brown ink pen (#2B2118), "
        "an outline about {n} px thick on this canvas, the same weight on every edge, slightly wobbly like a real pen; every "
        "area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner "
        "than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, nothing on the background), no "
        "white highlights or shine spots, no gloss, no glow, no rim light, no gradients, no 3D look. The only white allowed is "
        "one small catchlight dot in each eye, the ivory parts of the design, and the white foam of the water. A darker tone "
        "appears only where the design itself has a darker colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure. No text, no labels, no frame, no ground line, no sky, no rocks, no other creature.")
WATER = ("THE WATER, in the style of image 2: stylised hand-drawn waves, plump curling crests, simple and chunky: three flat "
         "blues (deep #1E68BE, sky #3A96E2, pale #8CD0F6) in broad bands that follow the flow, and flat white foam (#F4FCFF) "
         "as round bumpy scallops on the crests, all with the same brown ink outline.")

# ---------------------------------------------------------------- dạng 2: LIÊN KÌNH
DESIGN2 = (
    "THE CREATURE: an adult SEA-UNICORN WHALE, a narwhal-like whale of the water element that carries a big blooming LOTUS on its "
    "back: a sacred guardian beast, majestic and battle-ready, drawn as a stylised game monster (plump streamlined whale body, "
    "big expressive head, simple shapes), NOT realistic, NOT cute-chibi, NOT scary-horror. It is seen from the SIDE and faces the "
    "viewer's RIGHT.\n"
    "- BODY: a long, muscular whale body, deep indigo-blue (#3A4A9C) on the back and sides, a wide ivory (#F4ECD8) belly and "
    "throat with four or five simple ink grooves along the throat (whale pleats). The dividing line between indigo and ivory is one "
    "clean wavy ink line; NO swirl patterns, NO spots, NO scales. Three thin GOLD (#E8B64A) ring bands around the body at the "
    "root of the tail, like armour rings.\n"
    "- HEAD: a big rounded whale head with a strong brow ridge; the mouth is a long line slightly OPEN, showing a strip of deep "
    "wine-red (#8B2F45) inside the mouth and a row of small pointed ivory teeth on the upper and lower jaw (the lower jaw must be "
    "clearly its own shape below the mouth line); one eye on the visible side: a narrow, sharp, determined eye with a round cyan "
    "iris (#45CFE0), a dark pupil and one small white catchlight; a flat GOLD brow crest shaped like a single lotus petal lies on "
    "the forehead at the root of the tusk.\n"
    "- TUSK: ONE long straight spiral tusk like a narwhal's, GOLD (#E8B64A) with a thin ink spiral groove winding along it, "
    "growing from the top of the snout and pointing forward and slightly upward to the right, about as long as the head is wide; "
    "it must stand alone against white with nothing crossing it.\n"
    "- LOTUS: one large fully OPEN lotus flower standing on the middle of the back, as tall as the head: two rings of plump "
    "pointed petals, the outer petals crimson (#D9443A), the inner petals a lighter rose (#EE8A80), and a round GOLD seed-pod in "
    "the centre with a few dark ink dots; the flower is fully visible against white, it does not overlap the head or the tail.\n"
    "- FINS: two broad paddle-shaped pectoral flippers, indigo with a crimson (#D9443A) edge band: the NEAR flipper points "
    "down-forward away from the body (clearly separated from the belly by white), the FAR flipper peeks out behind the body "
    "above the back, in front of the lotus; one tall dorsal fin behind the lotus, indigo with a crimson edge, swept back; the "
    "TAIL ends in a wide two-lobed fluke seen flat (like a fan), indigo on top with crimson tips and an ivory underside stripe.\n"
    "- The whole creature looks powerful and noble: chest raised, head up, eye fixed on an enemy to the right.")
COMPOSE2 = (
    "CANVAS AND FRAMING: landscape 1536x1024, pure-white background. The whole creature and its water are visible, nothing cut by "
    "the edges, at least 60 px of white margin all round; the group is about 1300 px wide and 820 px tall, centred.\n"
    "POSE (important, the drawing will be cut into parts for a 2D cut-out animation): side view, head at the RIGHT, tail at the "
    "LEFT. The body makes one gentle S: the chest and head rise toward the upper right (head tilted up about 20 degrees), the "
    "back arches, the tail curves down and then its fluke sweeps up at the far left so the whole fluke is visible against white. "
    "The near flipper, the far flipper, the dorsal fin, the lotus, the tusk and the fluke each stand clear with white around them; "
    "no part crosses another part. The mouth is slightly open so the inside of the mouth and the teeth are visible.\n"
    "- It rides on a LOW CUSHION OF WATER: a long low swell of curling water under the belly, about one fifth of the picture's "
    "height, with two small curls and foam at its two ends and a few drops in the air; the water covers only the bottom edge of "
    "the belly and the base of the near flipper, nothing else.")

# ---------------------------------------------------------------- dạng 1: KÌNH NỤ (bé con)
DESIGN1 = (
    "THE CREATURE: the BABY FORM of the sea-unicorn whale of image 4: the same species and the same family (whale body, one tusk, "
    "a lotus on the back, pectoral flippers, a two-lobed fluke, cyan eyes), but a CHIBI baby: a short tubby body like a bean, "
    "the head about 45% of the whole body length, a very big round head, big round cyan eyes (#45CFE0) with a dark pupil and one "
    "white catchlight, tiny flippers, a short tail with a small fluke. Brave, stubborn, ready to fight: brows drawn down in a "
    "determined frown, mouth a small open line with two tiny pointed teeth and a strip of wine-red (#8B2F45) inside. NOT a "
    "mascot smile, NOT sleepy.\n"
    "- COLOURS, lighter than the adult: back and sides soft periwinkle blue (#8FA7E6); belly and throat cream (#F7F0DF) with two "
    "or three short ink grooves; flipper edges and fluke tips crimson (#D9443A) as thin bands; NO swirls, NO spots, NO scales.\n"
    "- TUSK: only a short stubby cone of pale gold (#F1D27A) on top of the snout, about one third of the head's length, pointing "
    "forward-up to the right, with one ink spiral line; a tiny flat gold (#E8B64A) dot on the forehead at its root.\n"
    "- LOTUS BUD: on the middle of the back stands one CLOSED lotus bud, as tall as half the head: a plump teardrop of overlapping "
    "pointed petals, pale rose (#F3B5AE) with crimson (#D9443A) tips, sitting on a tiny indigo (#3A4A9C) cup; the bud is NOT open "
    "(no petals spread, no seed-pod visible).\n"
    "- One small dorsal fin behind the bud, periwinkle with a crimson edge. One near flipper pointing down-forward away from the "
    "body, one far flipper peeking out behind the back.")
COMPOSE1 = (
    "CANVAS AND FRAMING: landscape 1536x1024, pure-white background. The whole creature and its water are visible, nothing cut by "
    "the edges, at least 60 px of white margin all round; the group is about 1000 px wide and 820 px tall, centred.\n"
    "POSE (important, the drawing will be cut into parts for a 2D cut-out animation): side view, head at the RIGHT, tail at the "
    "LEFT, facing the viewer's RIGHT. Body almost horizontal with the head tilted up a little; the short tail curves down and the "
    "small fluke sweeps up at the left so it is fully visible against white. The near flipper, the far flipper, the dorsal fin, "
    "the bud, the stubby tusk and the fluke each stand clear with white around them; no part crosses another part. Mouth slightly "
    "open so the inside is visible.\n"
    "- It floats on a SMALL RING OF WATER: a low round puddle of curling water under the belly, about one sixth of the picture's "
    "height, with a little curl at each end, a few foam bumps and two drops in the air; the water covers only the bottom edge of "
    "the belly.")


def refs_common():
    return [(WORLD_STYLE, "the game's approved hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen "
                          "outline + coloured pencil / wax crayon hatching), nothing of its content",
             "Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét"),
            (HAI_LONG, "an approved sea-dragon boss of the same game, 1536x1024, white background: match EXACTLY its pen line, "
                       "crayon texture, flat colouring, level of detail, the look of its WATER, and the fierce determined faces. "
                       "Do NOT copy its species, design, colours or pose",
             "Hải Long Ngũ Đầu đã duyệt (1536 × 1024, nền trắng): lấy nét bút, vân sáp, mức chi tiết, kiểu nước, thần thái; "
             "không chép loài, màu, dáng"),
            (MA_KET, "an approved armoured sea-goat creature of the same game, 1536x1024, white background: match its flat "
                     "crayon colouring and the way its gold trims and armour plates are drawn as simple flat shapes. Do NOT copy "
                     "its species, colours or pose",
             "Ma Kết dạng 3 đã duyệt (1536 × 1024, nền trắng): lấy cách tô phẳng, cách vẽ viền vàng và giáp thành mảng phẳng; "
             "không chép loài, màu, dáng")]


def check(refs):
    missing = [W(p) for p, _, _ in refs if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def write_prompt(k, refs, design, compose, extra_water):
    os.makedirs(pk(k), exist_ok=True)
    os.makedirs(save_dir(k), exist_ok=True)
    out = os.path.join(save_dir(k), "L1_concept.png")
    p = os.path.join(pk(k), "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(pth)}: {en}" for i, (pth, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not "
          "edit, move or delete any other file.", "",
          "TASK: design and draw ONE creature as ONE full picture, in the hand-drawn style of the style images.", "",
          design, "", WATER if extra_water else "", "", compose, "", LINE.format(n=6), FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(x for x in t if x is not None) + "\n")
    return p, out


CONCEPT1 = os.path.join(save_dir(1), "L1_duyet.png")
PIECES = ("THIS IS A SHEET OF SEPARATE PARTS for a 2D cut-out animation rig, NOT a scene: every part is drawn COMPLETE and on "
          "its own, flat on the white page like stickers laid out on a table, with at least 60 px of pure white between any two "
          "parts and between a part and the image edge. No part touches or overlaps another. Do not draw a whole creature, do "
          "not draw extra parts, do not draw labels, numbers, arrows or guide lines. Same colours, same ink line, same crayon "
          "texture as the approved concept image.")

# tờ mảnh dạng 2 (bước, tên, tiêu đề, mô tả tiếng Anh, ghi chú tiếng Việt); nước dùng lại mảnh sóng đã cắt của Hải Long
STEPS2 = [
    ("M01", "dau", "head group",
     "Canvas 1536 x 1024. Lay the parts out in a 3 x 2 grid of 512 px cells, one part centred in each cell:\n"
     "- top-left cell: the HEAD, UPPER PART ONLY, side view facing the viewer's RIGHT: the big rounded indigo (#3A4A9C) whale "
     "skull with its strong brow ridge, the one narrow fierce eye (round cyan #45CFE0 iris, dark pupil, one small white catchlight), "
     "the flat gold (#E8B64A) lotus-petal brow crest on the forehead, and the upper jaw with its row of small pointed ivory teeth "
     "along the bottom edge; a strip of ivory (#F4ECD8) along the lower edge where the throat begins. NO tusk, NO lower jaw, NO "
     "neck. The back end of the head (where the body attaches, on the left) is a smooth rounded stump. About 440 px wide.\n"
     "- top-middle cell: the LOWER JAW alone, side view facing right: one long wedge, ivory (#F4ECD8) with three ink throat "
     "grooves along its underside, the lower teeth (small pointed ivory) standing along its top edge, a strip of the wine-red "
     "(#8B2F45) inner mouth visible above the gum line; the back end (the jaw hinge, on the left) is a rounded knob. About 340 px "
     "wide, 120 px tall.\n"
     "- top-right cell: a MOUTH INTERIOR patch: one simple soft rounded blob of flat wine-red (#8B2F45) with a slightly darker "
     "throat spot (#6A1F33) in the middle, brown ink outline, about 240 px wide and 170 px tall. No teeth.\n"
     "- bottom-left cell: the TUSK alone, drawn perfectly STRAIGHT and HORIZONTAL like a ruler: the thick rounded root at the "
     "LEFT (with one gold ring band around it), tapering to a sharp point at the RIGHT; flat gold (#E8B64A) with one thin ink "
     "spiral groove winding along its whole length. About 470 px long and 72 px thick at the root.\n"
     "- bottom-middle cell: ONE CLOSED EYELID for the head above: a leaf-shaped patch of the head's indigo skin (#3A4A9C, crayon "
     "hatching) with the brown ink outline all round and ONE thick dark-brown curved line across its lower half (the shut eye, "
     "curving down toward the snout like a stern frown). About 150 px wide and 95 px tall.\n"
     "- bottom-right cell: the DORSAL FIN alone: a tall fin swept back to the LEFT (like a shark fin leaning back), indigo with a "
     "crimson (#D9443A) edge band along its back edge, the root at the bottom cut flat and slightly widened. About 300 px wide "
     "and 330 px tall.",
     "đầu (phần trên, có mào vàng, mắt, răng trên; không ngà, không hàm dưới), hàm dưới rời, mảng lòng miệng, ngà thẳng nằm "
     "ngang (gốc trái), mí mắt nhắm, vây lưng"),
    ("M02", "than", "body group",
     "Canvas 1536 x 1024. Three rows, parts drawn horizontally:\n"
     "- top row: the BODY TRUNK of the whale, laid out perfectly STRAIGHT and horizontal like a long thick tube seen from the "
     "side. PROPORTIONS ARE CRITICAL: the tube is SHORT AND FAT, only about 2.5 times longer than it is thick: about 1000 px "
     "long, 420 px thick at the RIGHT end (the neck end, where the head attaches) and about 250 px thick at the LEFT end (the "
     "tail end), tapering smoothly. It must look like a plump whale torso, NOT a long thin tube; leave white space on the "
     "right of the row if needed. The upper two thirds are flat indigo (#3A4A9C); the lower third is the "
     "ivory (#F4ECD8) belly with five long lengthwise ink grooves on the right half (whale pleats); the border between indigo and "
     "ivory is one clean gently wavy ink line. Three thin GOLD (#E8B64A) ring bands go around the tube near the left end. BOTH "
     "ends are closed and rounded (round stumps). No head, no fins, no lotus, no tail fluke.\n"
     "- middle row, two parts side by side with white between them: (a) on the left, the TAIL STEM: a straight horizontal tube, "
     "thick rounded end at the RIGHT (about 190 px, joins the body) tapering to about 110 px at the LEFT end, indigo on top and "
     "ivory below, both ends rounded, about 380 px long; (b) on the right, the TAIL FLUKE alone: a wide two-lobed whale fluke "
     "seen flat like an open fan, the two lobes spreading up-left and up-right from one short rounded root at the bottom "
     "centre, indigo with crimson (#D9443A) tips and one ivory stripe along the lower edge of each lobe, about 400 px wide and "
     "300 px tall.\n"
     "- bottom row, two parts side by side with white between them: (a) on the left, ONE PECTORAL FLIPPER alone: a broad paddle, "
     "drawn horizontal with its rounded root stump at the LEFT and its rounded tip at the RIGHT, indigo with a crimson "
     "(#D9443A) edge band along the lower edge and the tip, about 430 px long and 190 px wide; (b) on the right, THREE separate "
     "loose LOTUS PETALS of three sizes (about 150, 115 and 85 px tall), plump pointed petals standing upright, crimson "
     "(#D9443A) with a lighter rose (#EE8A80) inner half, white between them.",
     "thân duỗi thẳng (1380 × 330→190, bụng ngà có rãnh, ba vòng vàng bên trái), cuống đuôi thẳng, vây đuôi xoè rời, một vây "
     "chèo nằm ngang (gốc trái), ba cánh sen rời"),
    ("M03", "sen", "lotus group",
     "Canvas 1536 x 1024. Parts:\n"
     "- top row, centred: the BACK PETAL ROW of the open lotus: FIVE plump pointed petals, crimson (#D9443A) with a narrow "
     "lighter rose (#EE8A80) band along the centre of each, all growing from ONE common short base at the bottom centre and "
     "spreading upward like an open fan (the middle petal tallest and upright, the outer petals leaning outward about 35 "
     "degrees); the petals touch each other only at the base; the base is cut flat. About 640 px wide and 430 px tall.\n"
     "- bottom row, three parts from left to right with white between them: (a) the FRONT PETAL ROW: FOUR shorter petals of the "
     "lighter rose (#EE8A80) with crimson (#D9443A) tips, from one common flat base, leaning outward a little more than the back "
     "row, about 560 px wide and 300 px tall; (b) the SEED POD: a round flat-bottomed gold (#E8B64A) cup with seven dark ink "
     "dots on its top face, about 210 px wide and 160 px tall; (c) a BLOWHOLE SPRAY: a small plume of water shooting straight "
     "UP from a flat base, three plump pointed tongues of pale blue (#8CD0F6 and #3A96E2) with round white foam bumps and two "
     "drops, about 170 px wide and 200 px tall.",
     "hàng cánh sau (5 cánh đỏ thắm xoè quạt, đế phẳng), hàng cánh trước (4 cánh hồng), đài sen vàng, tia nước lỗ thở"),
]

STEPS1 = [
    ("M01", "dau", "baby head group",
     "Canvas 1536 x 1024. Lay the parts out in a 3 x 2 grid of 512 px cells, one part centred in each cell:\n"
     "- top-left cell: the BABY HEAD, UPPER PART ONLY, side view facing the viewer's RIGHT: a very big round periwinkle "
     "(#8FA7E6) skull with one big round cyan (#45CFE0) eye (dark pupil, one small white catchlight) under a frowning brow, a tiny "
     "flat gold (#E8B64A) dot on the forehead, the upper jaw with TWO tiny pointed ivory teeth along the bottom edge, a strip of "
     "cream (#F7F0DF) along the lower edge. NO tusk, NO lower jaw, NO body. The back end (left) is a smooth rounded stump. About "
     "440 px wide.\n"
     "- top-middle cell: the baby's LOWER JAW alone: a short plump wedge, cream (#F7F0DF) with two short ink grooves underneath, "
     "one tiny pointed ivory tooth on its top edge, a strip of wine-red (#8B2F45) inner mouth above the gum line, rounded knob at "
     "the left (hinge). About 260 px wide and 110 px tall.\n"
     "- top-right cell: a MOUTH INTERIOR patch: a soft rounded blob of flat wine-red (#8B2F45) with a slightly darker throat spot, "
     "about 200 px wide and 150 px tall. No teeth.\n"
     "- bottom-left cell: the STUBBY TUSK alone: a short fat cone, perfectly horizontal, rounded root at the LEFT, blunt point at "
     "the RIGHT, flat pale gold (#F1D27A) with one ink spiral line, about 200 px long and 90 px thick at the root.\n"
     "- bottom-middle cell: ONE CLOSED EYELID for the baby head: a big round-ish patch of periwinkle (#8FA7E6) skin with the "
     "brown ink outline and ONE thick curved shut-eye line across its lower half (a stubborn frown), about 190 px wide and 150 "
     "px tall.\n"
     "- bottom-right cell: the baby's small DORSAL FIN alone: a little fin swept back to the LEFT, periwinkle with a crimson "
     "(#D9443A) edge band, flat root at the bottom, about 180 px wide and 200 px tall.",
     "đầu bé (phần trên, mắt to, chấm vàng trán, hai răng; không ngà, không hàm dưới), hàm dưới rời, lòng miệng, ngà cụt nằm "
     "ngang, mí mắt nhắm to, vây lưng nhỏ"),
    ("M02", "than", "baby body group",
     "Canvas 1536 x 1024. Three rows:\n"
     "- top row: the BABY BODY alone, a short tubby bean laid horizontal, about 820 px long and 520 px tall, the RIGHT end (neck, "
     "where the head attaches) thicker and the LEFT end (tail end) narrower, both ends closed and rounded; the upper two thirds "
     "flat periwinkle (#8FA7E6), the lower third cream (#F7F0DF) belly with three short lengthwise ink grooves; the border one "
     "clean gently wavy ink line. No head, no fins, no bud, no tail.\n"
     "- middle row, three parts from left to right with white between them: (a) the TAIL STEM: a short straight horizontal tube, "
     "rounded thick end at the RIGHT (about 120 px) tapering to 60 px at the LEFT, periwinkle on top and cream below, about 300 "
     "px long; (b) the small TAIL FLUKE: a two-lobed fan with the lobes spreading up-left and up-right from a short rounded root "
     "at the bottom centre, periwinkle with crimson (#D9443A) tips, about 240 px wide and 190 px tall; (c) ONE small PECTORAL "
     "FLIPPER: a plump paddle, horizontal, rounded root at the LEFT and tip at the RIGHT, periwinkle with a thin crimson edge "
     "band, about 260 px long and 120 px wide.\n"
     "- bottom row, four parts from left to right with white between them: (a) the BUD CUP: a small indigo (#3A4A9C) cup, wide "
     "and shallow, flat bottom, about 170 px wide and 80 px tall; (b) the BUD BACK LAYER: three tall closed petals standing "
     "together as one teardrop shape, pale rose (#F3B5AE) with crimson (#D9443A) tips, flat base, about 230 px wide and 330 px "
     "tall; (c) the BUD FRONT LAYER: two shorter closed petals side by side as one piece, pale rose with crimson tips, flat base, "
     "about 190 px wide and 260 px tall; (d) THREE separate loose pale-rose petals of three sizes (about 120, 95 and 70 px tall) "
     "standing upright, white between them.",
     "thân hạt đậu nằm ngang (900 × 480), cuống đuôi, vây đuôi nhỏ, một vây chèo, đế nụ chàm, lớp cánh sau của nụ, lớp cánh "
     "trước, ba cánh rời"),
]


def write_manh(k, refs, steps, loai):
    """file luot_2_manh.txt của dạng k: mỗi bước một ảnh, SAVE riêng từng bước (như build_hai_long.py)."""
    sd = save_dir(k)
    p = os.path.join(pk(k), "luot_2_manh.txt")
    order = [s[0] for s in steps]
    t = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image per reply "
         "and save each one as its step says. Do not reply with text only.", "",
         "REFERENCE IMAGES (open each file from its full path):"]
    t += [f"image {i} = {W(pth)}: {en}" for i, (pth, en, _) in enumerate(refs, 1)]
    t += ["", f"WHAT THIS IS: sheets of separate, complete parts of the {loai} of the LAST reference image (the approved concept), "
          "for a 2D cut-out animation rig. The animation software bends the straight body and tail with bones, opens the jaw, "
          "swings the flippers and the petals, so every part must be drawn whole (also the areas that are hidden in the concept), "
          "clean, and well separated from the others. Keep EXACTLY the concept's colours, ink line and crayon texture.", "",
          f"SAVE: every step's image goes into {W(sd)} under the step's name (for example {order[0]}.png). If that file already "
          "exists, add _2, _3 ... before .png. Do not change, move or delete any other file.", "",
          f"ORDER: draw step {order[0]} now, save it and stop. Each time I say \"next\", draw the next step, save it and stop, in "
          f"this order: {', '.join(order[1:])}.", ""]
    for sc, _, title, en, _ in steps:
        t += [f"=== STEP {sc} ({title}) ===", PIECES, en, "", LINE.format(n=6), FLAT, BG,
              f"SAVE this step: save it as a PNG to {W(os.path.join(sd, sc + '.png'))} (create the folder if it is missing; if "
              f"that file already exists, save it as {sc}_2.png, {sc}_3.png ... in the same folder instead). Do not change, move "
              "or delete any other file.", ""]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return p


def build():
    refs = refs_common()
    check(refs)
    p2, out2 = write_prompt(2, refs, DESIGN2, COMPOSE2, True)
    made = [(2, p2, out2)]
    p1 = out1 = None
    if os.path.exists(CONCEPT2):
        r = refs + [(CONCEPT2, "the APPROVED CONCEPT of the adult sea-unicorn whale, 1536x1024: every part you draw belongs to "
                               "THIS creature: same colours, same line and crayon texture, same head, tusk, lotus, fins. Use it "
                               "only to know what the parts look like; do not redraw the scene", "Concept dạng 2 đã chọn")]
        print(write_manh(2, r, STEPS2, "adult sea-unicorn whale"))
    if os.path.exists(CONCEPT1):
        r = refs + [(CONCEPT1, "the APPROVED CONCEPT of the BABY sea-unicorn whale, 1536x1024: every part you draw belongs to "
                               "THIS baby: same colours, same line and crayon texture, same head, stubby tusk, closed bud, fins. "
                               "Use it only to know what the parts look like; do not redraw the scene", "Concept dạng 1 đã chọn")]
        print(write_manh(1, r, STEPS1, "baby sea-unicorn whale"))
    if os.path.exists(CONCEPT2):
        refs1 = refs + [(CONCEPT2, "the APPROVED ADULT FORM of this creature, 1536x1024, white background: the baby you draw is "
                                   "the same species and the same family as THIS adult (same whale shape language, same tusk, "
                                   "same lotus theme, same line and crayon texture) but a baby: much simpler, rounder, lighter "
                                   "colours, lotus still a closed bud, tusk only a stub. Do not redraw the adult",
                         "Concept dạng 2 Liên Kình đã chọn (1536 × 1024, nền trắng): cùng dòng, bé con phải nhận ra là con của nó")]
        check(refs1)
        p1, out1 = write_prompt(1, refs1, DESIGN1, COMPOSE1, True)
        made.append((1, p1, out1))

    gd = [f"# Gói gửi GPT: Liên Kình (`{CODE}`), dòng 7 lô tướng mới đảo Thủy", "",
          "Cá kỳ lân biển (cá voi một ngà) cõng hoa sen, hai dạng. Dạng 2 là dạng cuối (trưởng thành, chiến), dạng 1 là bé con chibi. "
          "Thiết kế khác hẳn con tham khảo, chỉ giữ chủ đề; không đính ảnh con tham khảo.", "",
          f"**Dạng 2, chỉ gửi GPT đường dẫn:** `{W(p2)}`. GPT lưu ảnh vào `{W(out2)}`.", ""]
    if p1:
        gd += [f"**Dạng 1** (dựng sau khi chép concept dạng 2 đã chọn thành `{W(CONCEPT2)}`): `{W(p1)}`. GPT lưu vào `{W(out1)}`.", ""]
    else:
        gd += [f"**Dạng 1**: chưa dựng, chờ chép concept dạng 2 đã chọn thành `{W(CONCEPT2)}` rồi chạy lại `build_tm07.py`.", ""]
    gd += [f"Claude tự gen: `py -3 -I gen.py gui_gpt/{CODE}_2/luot_1_concept.txt`, rồi `py -3 -I gen.py gui_gpt/{CODE}_1/luot_1_concept.txt`.", "",
           "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(p)}` | {vi} |" for i, (p, _, vi) in enumerate(refs, 1)]
    gd += [f"| 4 (chỉ dạng 1) | `{W(CONCEPT2)}` | Concept dạng 2 đã chọn (1536 × 1024, nền trắng) |", "",
           "## Bảng màu", "",
           "| Vùng | Dạng 2 Liên Kình | Dạng 1 Kình Nụ |", "|---|---|---|",
           "| Lưng, sườn | chàm `#3A4A9C` | lam phấn `#8FA7E6` |",
           "| Bụng, cổ họng | ngà `#F4ECD8` | kem `#F7F0DF` |",
           "| Sen | cánh ngoài đỏ thắm `#D9443A`, cánh trong hồng `#EE8A80`, đài vàng `#E8B64A` | nụ hồng nhạt `#F3B5AE`, chóp đỏ `#D9443A` |",
           "| Ngà, mào trán, vòng đuôi | vàng `#E8B64A` | ngà cụt vàng nhạt `#F1D27A` |",
           "| Viền vây, chóp đuôi | đỏ thắm `#D9443A` | đỏ thắm `#D9443A` (dải mỏng) |",
           "| Mắt | mống cyan `#45CFE0`, hẹp, sắc | mống cyan `#45CFE0`, to tròn |",
           "| Lòng miệng | đỏ rượu `#8B2F45` | đỏ rượu `#8B2F45` |",
           "| Nước | lam `#1E68BE` `#3A96E2` `#8CD0F6`, bọt `#F4FCFF` | như dạng 2 |", "",
           "## Kiểm concept dạng 2", "",
           "- Nhìn nghiêng, **quay sang phải**, đầu ở phải, đuôi ở trái, đầu ngẩng ~20°; thân chữ S nhẹ; vây đuôi xoè thấy trọn.",
           "- Một ngà vàng xoắn thẳng, không bị gì che; sen nở to đứng giữa lưng, không đè đầu, không đè đuôi; vây gần tách khỏi bụng.",
           "- Miệng hé thấy lòng miệng đỏ rượu và răng nhọn nhỏ; hàm dưới là hình riêng; mắt hẹp quả quyết, một chấm sáng.",
           "- Thân chàm + bụng ngà, không vân xoắn, không đốm, không vảy; ba vòng vàng ở gốc đuôi.",
           "- Nước: đệm sóng thấp dưới bụng, chỉ che mép dưới bụng; ba màu lam phẳng, bọt trắng tròn.",
           "- Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh, không chữ.", "",
           "## Kiểm concept dạng 1", "",
           "- Chibi: đầu ~45% thân, mắt to tròn, thân bầu; vẫn cau mày, hai răng nhọn, miệng hé.",
           "- Nụ sen **khép**, ngà **cụt**, màu nhạt hơn dạng 2; vẫn nhận ra cùng dòng với ảnh 4.", "",
           "## GPT vẽ sai thì gửi thêm (`gen.py ... --note \"...\"`)", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Có bóng, mảng sáng tối | `Flat colour only: remove every shadow, highlight and gradient; keep the crayon hatching as texture.` |",
           "| Quay sang trái | `The creature must face the viewer's RIGHT: head on the right, tail on the left.` |",
           "| Dạng 2 vẫn chibi, dễ thương | `Not chibi at all: adult proportions, head about one quarter of the body length, narrow fierce eye, powerful body.` |",
           "| Vẽ vân xoắn, đốm trên thân | `No swirl patterns, spots or scales on the body: plain indigo back, plain ivory belly with a few throat grooves.` |",
           "| Sen che đầu hoặc đuôi, ngà bị che | `The lotus, the tusk, each flipper and the fluke must each stand clear with white around them; nothing overlaps.` |",
           "| Nước quá to | `The water is only a low cushion under the belly, about one fifth of the picture height.` |",
           "| Dạng 1 sen nở, ngà dài | `Baby form: the lotus is a CLOSED bud, the tusk only a short stub, colours lighter.` |"]
    open(os.path.join(pk(2), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    if p1:
        open(os.path.join(pk(1), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    for k, p, _ in made:
        print(W(p))
    if not p1:
        print("(chưa dựng dạng 1: chưa có", W(CONCEPT2) + ")")


if __name__ == "__main__":
    build()
