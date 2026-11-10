"""Gói GPT vẽ Hải Long Ngũ Đầu: quái nhiều đầu có sóng nước chuyển động (người dùng dặn 2026-11-10, học cách dựng của một con
rắn bảy đầu trong game khác, xem .claude/skills/skill-petclash/mo_xe_quai_nhieu_dau.md; thiết kế, hình và diễn xuất của con này
là của mình, không lấy gì của con kia).

Con nhiều cổ chồng nhau không rig được từ một ảnh liền (cổ sau bị che). Vì vậy:
  lượt 1: concept trọn con (chốt dáng, màu; chỉ làm mốc, không cắt từ ảnh này);
  lượt 2: bốn tờ mảnh rời vẽ đủ (M01 đầu + hàm, M02 cổ duỗi thẳng + vòng thân, M03 cuộn sóng, M04 mặt nước + nước toé).
Rig và animation: hai_long.py.

    py -3 -I build_hai_long.py            dựng file prompt (lượt 2 chỉ dựng khi đã có ảnh concept đã duyệt)
    py -3 -I gen.py gui_gpt/hai_long/luot_1_concept.txt
    py -3 -I gen.py gui_gpt/hai_long/luot_2_manh.txt --steps M01,M02,M03,M04
    py -3 -I gen.py gui_gpt/hai_long/luot_3_phun_nuoc.txt --steps M05      (tia nước, vụ nổ, loa nước, vệt nước, mí mắt)
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "hai_long"
PK = os.path.join(HERE, "gui_gpt", CODE)
SAVE = os.path.join(HERE, "inbox", CODE, "tai_ve")
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
DRAGON = os.path.join(HERE, "inbox", "thuong_lam_3", "tai_ve", "L1_lien.png")
FX_ART = os.path.normpath(os.path.join(HERE, "..", "..", "Assets", "03 Art", "Fx"))
SPLASH = os.path.join(FX_ART, "no_nuoc.png")
SWIRL = os.path.join(FX_ART, "xoay_nuoc.png")
CONCEPT = os.path.join(SAVE, "L1_duyet.png")  # concept Claude đã chọn (chép từ L1_concept*.png)


def W(p):
    return os.path.normpath(p)


DESIGN = ("THE CREATURE: a FIVE-HEADED SEA DRAGON, an eastern-style water dragon (long serpent necks, no wings, no legs "
          "visible), a boss monster of the water element. Colours, the same on all five heads and necks: scales jade-teal "
          "(#2FA79B) on the back and sides; belly plates warm cream-gold (#F2D9A0) as a row of wide segments along the underside "
          "of each neck; a low coral-red (#E0563C) fin ridge running along the back of each neck and a coral-red fin mane behind "
          "each head; two golden antler-like horns (#E9B84A) per head; two long cream whiskers (#F4EEDC) from the snout; amber "
          "eyes (#F0A030) with a dark slit pupil; inside of the mouth deep rose (#B8405A), teeth cream. Each head is a long "
          "dragon head seen from the side: long snout, strong lower jaw, brow ridge, determined fierce look, NOT cute and NOT "
          "scary-horror. The CENTRE head is the leader: about 30% bigger, with bigger branching antlers and a small cream pearl "
          "set on its forehead.")
LINE = ("LINE AND COLOUR: the hand-drawn look of the style images: drawn by hand on paper with a dark-brown ink pen (#2B2118), "
        "an outline about {n} px thick on this canvas, the same weight on every edge, slightly wobbly like a real pen; every "
        "area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner "
        "than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, nothing on the background), no "
        "white highlights or shine spots, no gloss, no glow, no rim light, no gradients, no 3D look. The only white allowed is "
        "one small catchlight dot in each eye, and the white foam of the water. A darker tone appears only where the design "
        "itself has a darker colour.")
WATER = ("THE WATER, in the style of images 3 and 4: stylised hand-drawn waves, plump curling crests like the waves of an old "
         "woodblock print but simple and chunky: three flat blues (deep #1E68BE, sky #3A96E2, pale #8CD0F6) in broad bands that "
         "follow the flow of each wave, and flat white foam (#F4FCFF) as round bumpy scallops on the crests, all with the same "
         "brown ink outline.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure or its pieces. No text, no labels, no frame, no ground line.")
PIECES = ("THIS IS A SHEET OF SEPARATE PARTS for a 2D cut-out animation rig, NOT a scene: every part is drawn COMPLETE and on "
          "its own, flat on the white page like stickers laid out on a table, with at least 60 px of pure white between any two "
          "parts and between a part and the image edge. No part touches or overlaps another. Do not draw a whole creature, do "
          "not draw extra parts, do not draw labels, numbers, arrows or guide lines.")

# (bước, tên file, tiêu đề, mô tả tiếng Anh, ghi chú tiếng Việt)
STEPS = [
    ("M01", "dau", "heads and jaws",
     "Canvas 1536 x 1024. Lay the parts out in a 3 x 2 grid of 512 px cells, one part group centred in each cell:\n"
     "- top-left cell: the LEADER HEAD, UPPER PART ONLY, side view facing the viewer's RIGHT: skull, brow, eye, long snout and "
     "the upper lip with its upper teeth showing along the bottom edge, the two big golden branching antlers, the forehead "
     "pearl, and the coral-red fin mane sweeping back from the back of the skull. NO lower jaw, NO neck, NO whiskers. The back "
     "end of the head (where the neck will attach) is a smooth rounded stump. About 430 px wide.\n"
     "- top-middle cell: the LEADER LOWER JAW alone, side view facing right: the lower jaw as one long wedge, cream-gold "
     "underside and jade-teal side, the lower teeth standing along its top edge, a strip of the deep-rose inner mouth and the "
     "rose tongue lying inside it visible above the gum line; the back end (the jaw hinge) is a rounded knob. About 330 px "
     "wide.\n"
     "- top-right cell: a MOUTH INTERIOR patch: one simple soft rounded blob of flat deep rose (#B8405A) with a slightly darker "
     "rose throat spot (#8E2F48) in the middle, brown ink outline, about 240 px wide, 170 px tall. No teeth.\n"
     "- bottom-left cell: a NORMAL HEAD, UPPER PART ONLY, same species and same view as the leader but simpler: two shorter "
     "plain golden horns (no branches), no pearl, a smaller fin mane. NO lower jaw, NO neck, NO whiskers; rounded stump at the "
     "back. About 380 px wide.\n"
     "- bottom-middle cell: the NORMAL LOWER JAW alone, like the leader's but a little smaller, about 290 px wide.\n"
     "- bottom-right cell: TWO separate small parts with white between them: (a) ONE long whisker: a single cream tendril "
     "(#F4EEDC), thick at the root and tapering to a fine curled tip, drawn as a gentle S-curve running left to right, about "
     "360 px long and 26 px thick at the root; (b) below it, ONE fin tuft: a coral-red fan of three pointed fin lobes joined "
     "at a rounded root on the left, about 200 px wide.",
     "đầu thủ lĩnh (phần trên, có gạc, ngọc, bờm vây), hàm dưới thủ lĩnh, mảng lòng miệng, đầu thường (phần trên), hàm dưới "
     "thường, một sợi râu + một chùm vây"),
    ("M02", "co", "necks and body coil",
     "Canvas 1536 x 1024. Three rows, parts drawn horizontally:\n"
     "- top row: the THICK NECK of the leader head, laid out perfectly STRAIGHT and horizontal like a long tube seen from the "
     "side, about 1380 px long and 190 px thick, the same thickness for most of its length and a little thinner toward the "
     "RIGHT end (the head end). Along the TOP edge runs the low coral-red fin ridge (small pointed fin lobes, a regular row); "
     "the upper two thirds of the tube are jade-teal with a few simple curved scale marks; the lower third is the row of "
     "cream-gold belly plates (about 16 wide segments separated by thin ink lines). BOTH ends are closed and rounded (round "
     "stumps). No head, no tail.\n"
     "- middle row: a THIN NECK, the same design, perfectly straight and horizontal, about 1380 px long and 140 px thick, a "
     "little thinner toward the right end, both ends rounded.\n"
     "- bottom row, two parts side by side with white between them: (a) on the left, a BODY COIL: one arch of the dragon's "
     "body shaped like an upside-down U (a hump rising out of water), jade-teal with the coral fin ridge along its outer "
     "(upper) curve and the cream-gold belly plates along its inner curve, the two leg ends pointing straight down and cut "
     "off flat at the bottom, about 520 px wide and 300 px tall, tube thickness about 150 px; (b) on the right, the TAIL TIP: "
     "the last tapering part of the tail lying horizontal, about 520 px long, thick rounded stump on the left tapering to the "
     "right into a coral-red fan-shaped tail fin of three lobes.",
     "cổ to duỗi thẳng (1380 × 190), cổ nhỏ duỗi thẳng (1380 × 140), một vòng thân hình chữ U úp, chóp đuôi có vây"),
    ("M03", "song", "wave curls",
     "Canvas 1536 x 1024. Six separate water shapes in a 3 x 2 grid of 512 px cells, one centred in each cell, each with a "
     "flat or gently rounded bottom so they can be stacked in rows:\n"
     "- top-left: a BIG wave crest curling over to the RIGHT (a tall plump hook of water, foam scallops on the curling tip), "
     "about 400 px wide, 400 px tall.\n"
     "- top-middle: a BIG wave crest curling over to the LEFT, a different shape from the first (wider, the curl lower and "
     "rounder), about 430 px wide, 360 px tall.\n"
     "- top-right: a MEDIUM double wave: two crests of different height rising from one base, both curling right, about 400 px "
     "wide, 300 px tall.\n"
     "- bottom-left: a SMALL curl: one little wave hook curling right with one foam scallop, about 260 px wide, 230 px tall.\n"
     "- bottom-middle: a LOW SWELL: a long low hump of water with a small curl at its right end and a line of foam along the "
     "top, about 440 px wide, 170 px tall.\n"
     "- bottom-right: a FOAM PUFF: a cluster of five to seven round white foam bumps of different sizes with a few small pale "
     "blue shadows of form inside drawn as flat shapes, like a little cloud, about 300 px wide, 220 px tall.",
     "sáu hình nước rời: mào sóng to cuộn phải, mào sóng to cuộn trái, sóng đôi vừa, cuộn nhỏ, dải sóng thấp, cụm bọt"),
    ("M04", "mat_nuoc", "water surface, base and splash",
     "Canvas 1536 x 1024. Parts:\n"
     "- top row: a long WATER SURFACE BAND: a horizontal strip of sea surface about 1400 px wide and 230 px tall: the top edge "
     "is a row of seven or eight small wave crests of different sizes with white foam tips, the bottom edge is one smooth "
     "shallow curve (lower in the middle), broad flat bands of the three blues inside.\n"
     "- middle row, two parts: (a) on the left, a WATER MOUND: a wide low dome of deep-blue water (#1E68BE with a few sky-blue "
     "#3A96E2 flow bands), smooth rounded top, flat bottom, NO foam, about 820 px wide and 250 px tall; (b) on the right, a "
     "SPLASH CROWN: water bursting upward from a flat base into seven pointed plump spikes of different heights with round "
     "drops at the tips and a foam ring at the base, about 480 px wide and 300 px tall.\n"
     "- bottom row, four small parts with white between them: three separate water DROPS of different sizes (teardrop shapes, "
     "tail pointing up, about 90, 70 and 50 px tall, sky blue with a pale blue flat patch), and one flat RIPPLE RING: a thin "
     "oval ring of sky-blue water seen in perspective (a squashed ellipse outline, hollow inside), about 520 px wide and "
     "130 px tall, the band about 26 px thick with a few tiny foam bumps on it.",
     "dải mặt nước dài có hàng mào sóng, mô nước nền xanh đậm, vương miện nước toé, ba giọt nước, một vòng sóng dẹt"),
]


# lượt 3 (thêm 2026-11-10): mảnh cho chiêu phun nước và mí mắt (chớp, nhắm lúc trúng đòn)
HEADS_SHEET = os.path.join(SAVE, "M01.png")
STEPS3 = [
    ("M05", "phun_nuoc", "water breath parts and eyelids",
     "Canvas 1536 x 1024. Parts, in three rows:\n"
     "- top row: a THICK WATER JET: one long straight stream of rushing water shooting to the viewer's RIGHT, drawn perfectly "
     "straight and horizontal like a long tube of water seen from the side, about 1380 px long and 170 px thick, the same "
     "thickness for most of its length. The LEFT end (where it leaves the dragon's mouth) narrows over its first 150 px to a "
     "rounded neck about 90 px thick; the RIGHT end is closed and rounded. Inside: long flat lengthwise bands of the three "
     "blues that follow the flow (a pale-blue core band along the middle, sky blue beside it, deep blue along both edges) "
     "with a few thin dark-brown flow lines drawn along the length; small round white foam bumps sit irregularly along the "
     "top edge and the bottom edge, like the foam of the waves. No splash at either end, no drops around it.\n"
     "- second row: a THIN WATER JET: the same design, perfectly straight and horizontal, about 1380 px long and 105 px "
     "thick, left end narrowing to a rounded neck, right end rounded.\n"
     "- third row, four groups from left to right with white between them: (a) an IMPACT BURST: the splash where a jet "
     "hits, seen from the side: a fan of eight or nine plump pointed tongues of water bursting out toward the right, the "
     "upper right and the lower right from one centre at the middle of its LEFT edge (like half of a flower opening to the "
     "right), white foam bumps packed around that centre, round drops at some tips, about 470 px wide and 400 px tall; "
     "(b) a MOUTH FLARE: a short flared collar of water like the bell of a trumpet opening to the RIGHT, narrow (about 90 px) "
     "at its left end and widening to about 250 px at its right rim, with a ruff of small foam bumps and short pointed spray "
     "tongues around the wide rim, about 230 px wide and 260 px tall; (c) THREE SPRAY STREAKS stacked one above the other "
     "with white between them: comet-shaped splashes of water flying to the right (a round plump head on the right, a "
     "tapering tail to the left), sky blue with a pale flat patch, about 170, 130 and 95 px long; (d) TWO CLOSED EYELIDS "
     "stacked one above the other with white between them, for the heads of image 6 (heads facing right): each is a small "
     "leaf-shaped patch of the head's jade-teal skin (#2FA79B, crayon hatching) with the brown ink outline all round and ONE "
     "thick dark-brown curved line across its lower half (the shut eye, curving down toward the snout like a stern frown); "
     "the big one about 120 px wide and 78 px tall, the small one about 100 px wide and 64 px tall.",
     "tia nước to duỗi thẳng (1380 × 170), tia nước nhỏ (1380 × 105), vụ nổ nước chỗ tia chạm (xoè sang phải), loa nước ở "
     "miệng, ba vệt nước bay, hai mí mắt nhắm (to, nhỏ)"),
]


# lượt 4 (thêm 2026-11-10): lưỡi cho clip chết (đầu ngửa, nhắm mắt, lè lưỡi)
STEPS4 = [
    ("M06", "luoi", "tongues",
     "Canvas 1536 x 1024. Only TWO small parts, one above the other in the middle of the page, with at least 200 px of white "
     "between them and nothing else on the page:\n"
     "- upper part: the LEADER'S TONGUE: one long, soft, flat tongue hanging limp, drawn perfectly STRAIGHT and horizontal, "
     "the root on the LEFT and the tip on the RIGHT, about 320 px long; about 64 px thick at the rounded root, narrowing "
     "gently to about 36 px near the tip, the tip ending in two short rounded lobes (a small fork). Colour: flat rose pink "
     "(#E27C92), clearly lighter than the mouth interior of image 6, with ONE thin darker rose line (#B8405A) running along "
     "the middle from the root to just before the fork. Brown ink outline of the same weight as the heads of image 6. No "
     "teeth, no mouth, no drool, no shading.\n"
     "- lower part: a SMALLER TONGUE of the same design, about 260 px long and 52 px thick at the root.",
     "hai cái lưỡi duỗi thẳng nằm ngang (to 320 px, nhỏ 260 px), hồng nhạt, chẻ nhẹ ở đầu, một nét giữa"),
]


# lượt 5 (thêm 2026-11-10): hình nước đợt hai, cho nước quanh thân dày và mềm hơn (vòi nước cuộn cao, cuộn xoắn nhỏ, dải sóng dài)
STEPS5 = [
    ("M07", "nuoc_2", "more water shapes",
     "Canvas 1536 x 1024. Seven separate water shapes in three rows, all in the same water style as the waves of image 5 "
     "(three flat blues in bands that follow the flow, round white foam scallops, brown ink outline):\n"
     "- top row, two parts: (a) on the left, a LONG SWEEPING WAVE: one long low ribbon of water flowing from left to "
     "right, about 1000 px wide and 200 px tall: it starts as a thin pointed tail at the far left, swells into a thick "
     "rounded body, and at the right end its crest curls over forward into a small round hook with foam; the bottom edge "
     "is flat; long lengthwise bands of the three blues; a line of foam scallops along the top of the right half. (b) on "
     "the right, a SMALL SPIRAL CURL: a little wave curling to the right like a fern fiddlehead, the tip rolled into a "
     "tight round spiral, one foam scallop on the tip, flat bottom, about 180 px wide and 190 px tall.\n"
     "- middle row, four parts from left to right: (a) a TALL TENDRIL: a tall slender column of water rising straight up "
     "from a flat base, about 130 px wide at the base and 400 px tall, getting thinner upward, its top bending over to the "
     "RIGHT and rolling into a round spiral hook with a foam scallop on the tip; lengthwise bands of the three blues. "
     "(b) a SHORTER, FATTER TENDRIL: about 170 px wide at the base and 320 px tall, bending over to the RIGHT and ending "
     "in TWO small rolled hooks, one above the other. (c) a MEDIUM SPIRAL CURL like the one in the top row but bigger and "
     "plumper, about 230 px wide and 230 px tall, curling right. (d) a TINY SPIRAL CURL, about 150 px wide and 150 px "
     "tall, curling right.\n"
     "- bottom row: a WAVELET ROW: one long horizontal strip of small ripples, about 1300 px wide and 120 px tall: its "
     "top edge is a row of ten or eleven small pointed wavelets, each leaning to the right with a tiny curl and a thin "
     "white foam line, of slightly different sizes; its bottom edge is one smooth straight line; coloured with the two "
     "lighter blues (sky #3A96E2 and pale #8CD0F6).",
     "dải sóng dài quét ngang (1000 × 200, mào cuộn ở đầu phải), cuộn xoắn nhỏ, vòi nước cao mảnh cuộn sang phải (130 × "
     "400), vòi nước thấp mập hai móc, cuộn xoắn vừa, cuộn xoắn tí hon, dải gợn sóng lăn tăn (1300 × 120)"),
]


def refs_concept():
    return [(WORLD_STYLE, "the game's approved hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen "
                          "outline + coloured pencil / wax crayon hatching), nothing of its content",
             "Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét"),
            (DRAGON, "an approved dragon creature of the same game, 1536x1024, white background: match EXACTLY its pen line, "
                     "crayon texture, flat colouring and level of detail. Do NOT copy its design, colours, wings or pose",
             "Rồng băng Thương Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): lấy nét bút, vân sáp, mức chi tiết; không chép dáng"),
            (SPLASH, "the game's approved water splash: the look of the game's water (plump pointed water shapes, round foam "
                     "bumps, flat blues, brown ink outline)",
             "Vụ nước toé đã duyệt của game (512 × 505, nền trong): mũi nước mập, bọt tròn, ba màu lam phẳng"),
            (SWIRL, "the game's approved swirling water: the look of its curled wave crests",
             "Vòng nước xoáy đã duyệt của game (384 × 362, nền trong): dòng nước có mào sóng cuộn")]


def check(refs):
    missing = [W(p) for p, _, _ in refs if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def build():
    os.makedirs(PK, exist_ok=True)
    os.makedirs(SAVE, exist_ok=True)
    refs = refs_concept()
    check(refs)
    out1 = os.path.join(SAVE, "L1_concept.png")
    p1 = os.path.join(PK, "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(p)}: {en}" for i, (p, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out1)}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not "
          "edit, move or delete any other file.", "",
          "TASK: design and draw ONE boss monster as ONE full picture, in the hand-drawn style of the style images.", "",
          DESIGN, "", WATER, "",
          "CANVAS AND FRAMING: landscape 1536x1024, pure-white background. The whole monster and its water are visible, nothing "
          "cut by the edges, at least 50 px of white margin all round; the group is about 1300 px wide and 880 px tall, centred.",
          "",
          "COMPOSITION (important):",
          "- The five necks rise out of ONE churning mass of water at the bottom centre and fan out upward like the ribs of a "
          "hand fan. ALL five heads are seen from the side and ALL face the viewer's RIGHT, mouths slightly open, as if "
          "watching an enemy on the right.",
          "- The LEADER head is in the centre, the highest, its neck an upright S-curve. Two heads are on the left: one high "
          "(neck leaning back to the left, then curving so the head still faces right), one lower. Two heads are on the right: "
          "one at middle height reaching forward to the right, one low near the water stretching far to the right. Every neck "
          "has its own clear curve; the five heads do NOT overlap each other, and each head is fully visible with white or "
          "water behind it.",
          "- The water: a ring of big curling waves around the place where the necks come out, tallest at the two sides, with "
          "smaller curls and foam in front; one hump of the dragon's coiled body arches out of the water at the far left and "
          "the finned tail tip rises out of the water at the far right. A few drops fly above the waves. The front waves "
          "overlap the bottoms of the necks, so no neck base is seen.",
          "- No ground, no rocks, no sky, no other creature.", "",
          LINE.format(n=6), FLAT, BG]
    open(p1, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    made = [p1]

    p2 = os.path.join(PK, "luot_2_manh.txt")
    if os.path.exists(CONCEPT):
        refs2 = refs + [(CONCEPT, "the APPROVED CONCEPT of this monster, 1536x1024: every part you draw belongs to THIS monster: "
                                  "same species, same colours, same line and crayon texture, same head design, same water. Use "
                                  "it only to know what the parts look like; do not redraw the scene",
                         "Concept Hải Long đã duyệt (1536 × 1024, nền trắng): năm đầu rồng xanh ngọc trồi lên từ sóng")]
        check(refs2)
        order = [s[0] for s in STEPS]
        t = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image per reply "
             "and save each one as its step says. Do not reply with text only.", "",
             "REFERENCE IMAGES (open each file from its full path):"]
        t += [f"image {i} = {W(p)}: {en}" for i, (p, en, _) in enumerate(refs2, 1)]
        t += ["", "WHAT THIS IS: sheets of separate, complete parts of the five-headed sea dragon of image 5 and of its water, "
              "for a 2D cut-out animation rig. The animation software bends the straight necks with bones, opens the jaws, "
              "and slides the wave pieces, so every part must be drawn whole (also the areas that are hidden in image 5), "
              "clean, and well separated from the others.", "",
              f"SAVE: every step's image goes into {W(SAVE)} under the step's name (for example {order[0]}.png). If that file "
              "already exists, add _2, _3 ... before .png. Do not change, move or delete any other file.", "",
              f"ORDER: draw step {order[0]} now, save it and stop. Each time I say \"next\", draw the next step, save it and "
              f"stop, in this order: {', '.join(order[1:])}.", "", DESIGN, "", WATER, ""]
        for sc, _, title, en, _ in STEPS:
            t += [f"=== STEP {sc} ({title}) ===", PIECES, en, "", LINE.format(n=6), FLAT, BG,
                  f"SAVE this step: save it as a PNG to {W(os.path.join(SAVE, sc + '.png'))} (create the folder if it is "
                  f"missing; if that file already exists, save it as {sc}_2.png, {sc}_3.png ... in the same folder instead). Do "
                  "not change, move or delete any other file.", ""]
        open(p2, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        made.append(p2)

    p3 = os.path.join(PK, "luot_3_phun_nuoc.txt")
    p4 = os.path.join(PK, "luot_4_luoi.txt")
    p5 = os.path.join(PK, "luot_5_nuoc.txt")
    if os.path.exists(CONCEPT) and os.path.exists(HEADS_SHEET):
        refs3 = refs + [(CONCEPT, "the APPROVED CONCEPT of this monster, 1536x1024: the parts you draw belong to THIS monster "
                                  "and its water: same colours, same line and crayon texture, same kind of water",
                         "Concept Hải Long đã duyệt (1536 × 1024, nền trắng)"),
                        (HEADS_SHEET, "the APPROVED HEAD PARTS of this monster, 1536x1024: the two head designs whose eyes the "
                                      "eyelids must cover (same teal, same outline weight); the jets and the tongues must "
                                      "look right coming out of these mouths",
                         "Tờ đầu đã duyệt M01 (1536 × 1024, nền trắng): đầu thủ lĩnh, đầu thường, hai hàm, lòng miệng, râu")]
        check(refs3)
        for pth, steps, what in ((p3, STEPS3, "the water it breathes out (the animation software bends and stretches the straight "
                                              "jets with bones and slides the small splashes along them) and closed eyelids for "
                                              "blinking"),
                                 (p4, STEPS4, "its tongues (the animation software bends the straight tongue with bones so it "
                                              "hangs limp out of the mouth)"),
                                 (p5, STEPS5, "more shapes for the water around it (the animation software bends each wave with "
                                              "bones so it rises, curls over and fades, and stacks many of them in rows)")):
            t = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image and "
                 "save it as the step says. Do not reply with text only.", "",
                 "REFERENCE IMAGES (open each file from its full path):"]
            t += [f"image {i} = {W(p)}: {en}" for i, (p, en, _) in enumerate(refs3, 1)]
            t += ["", "WHAT THIS IS: one more sheet of separate, complete parts for the 2D cut-out animation rig of the "
                  f"five-headed sea dragon of image 5: {what}.", "",
                  f"SAVE: the image goes into {W(SAVE)} under the step's name. If that file already exists, add _2, _3 ... "
                  "before .png. Do not change, move or delete any other file.", "", WATER, ""]
            for sc, _, title, en, _ in steps:
                t += [f"=== STEP {sc} ({title}) ===", PIECES, en, "", LINE.format(n=6), FLAT, BG,
                      f"SAVE this step: save it as a PNG to {W(os.path.join(SAVE, sc + '.png'))} (create the folder if it is "
                      f"missing; if that file already exists, save it as {sc}_2.png, {sc}_3.png ... in the same folder "
                      "instead). Do not change, move or delete any other file.", ""]
            open(pth, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
            made.append(pth)

    gd = [f"# Gói gửi GPT: Hải Long Ngũ Đầu (`{CODE}`)", "",
          "Quái năm đầu trồi lên từ sóng, làm theo cách dựng đã mổ xẻ ở `.claude/skills/skill-petclash/mo_xe_quai_nhieu_dau.md`. "
          "Con nhiều cổ chồng nhau không rig được từ một ảnh liền, nên có hai lượt: concept trọn con, rồi bốn tờ mảnh rời.", "",
          f"**Lượt 1, chỉ gửi GPT đường dẫn:** `{W(p1)}`. GPT lưu ảnh vào `{W(out1)}`.", "",
          f"**Lượt 2** (Claude dựng file sau khi chép concept đã chọn thành `{W(CONCEPT)}`): `{W(p2)}`, bốn bước "
          f"{', '.join(s[0] for s in STEPS)}, gõ `next` sau mỗi ảnh. GPT lưu vào `{W(SAVE)}`.", "",
          f"Claude tự gen: `py -3 -I gen.py gui_gpt/{CODE}/luot_1_concept.txt`, rồi "
          f"`py -3 -I gen.py gui_gpt/{CODE}/luot_2_manh.txt --steps {','.join(s[0] for s in STEPS)}`.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(p)}` | {vi} |" for i, (p, _, vi) in enumerate(refs, 1)]
    gd += [f"| 5 (chỉ lượt 2) | `{W(CONCEPT)}` | Concept Hải Long đã duyệt (1536 × 1024, nền trắng) |", "",
           "## Kiểm concept (lượt 1)", "",
           "- Năm đầu rồng nhìn nghiêng, **đều quay sang phải**, không đầu nào che đầu nào; đầu giữa to nhất, có gạc lớn và ngọc trán.",
           "- Vảy xanh ngọc, bụng kem vàng, vây và bờm đỏ san hô, gạc vàng, râu kem.",
           "- Nước ba màu lam phẳng, bọt trắng tròn, viền mực nâu; sóng trước che chỗ cổ mọc ra.",
           "- Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh.", "",
           "## Kiểm tờ mảnh (lượt 2): mỗi tờ 1536 × 1024, nền trắng, các mảnh rời nhau ít nhất 60 px", ""]
    gd += [f"- **{sc}**: {vi}" for sc, _, _, _, vi in STEPS]
    gd += ["", f"## Lượt 3 (chiêu phun nước, mí mắt): `{W(p3)}`", "",
           f"Một bước M05, GPT lưu vào `{W(SAVE)}`. Ảnh mẫu thêm: ảnh 6 = `{W(HEADS_SHEET)}` (tờ đầu đã duyệt, 1536 × 1024, nền "
           f"trắng). Claude tự gen: `py -3 -I gen.py gui_gpt/{CODE}/luot_3_phun_nuoc.txt --steps M05`.", ""]
    gd += [f"- **{sc}**: {vi}" for sc, _, _, _, vi in STEPS3]
    gd += ["", f"## Lượt 4 (lưỡi cho clip chết): `{W(p4)}`", "",
           f"Một bước M06, GPT lưu vào `{W(SAVE)}`, cùng sáu ảnh mẫu như lượt 3. Claude tự gen: "
           f"`py -3 -I gen.py gui_gpt/{CODE}/luot_4_luoi.txt --steps M06`.", ""]
    gd += [f"- **{sc}**: {vi}" for sc, _, _, _, vi in STEPS4]
    gd += ["", f"## Lượt 5 (hình nước đợt hai): `{W(p5)}`", "",
           f"Một bước M07, GPT lưu vào `{W(SAVE)}`, cùng sáu ảnh mẫu như lượt 3. Claude tự gen: "
           f"`py -3 -I gen.py gui_gpt/{CODE}/luot_5_nuoc.txt --steps M07`.", ""]
    gd += [f"- **{sc}**: {vi}" for sc, _, _, _, vi in STEPS5]
    gd += ["- Kiểm: hai tia **thẳng, nằm ngang**, đầu trái thuôn lại, không có nước toé dính vào; vụ nổ xoè sang **phải**; "
           "mí mắt là mảng xanh ngọc nhỏ có một nét cong sẫm."]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat)", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Có bóng, mảng sáng tối | `Flat colour only: remove every shadow, highlight and gradient; keep the crayon hatching as texture.` |",
           "| Vẽ cả con thay vì mảnh rời | `This must be a sheet of separate parts laid flat on white, not a creature or a scene. Redraw only the parts listed.` |",
           "| Cổ vẽ cong | `The necks must be perfectly straight horizontal tubes, like a ruler, both ends rounded.` |",
           "| Đầu dính hàm dưới hoặc dính cổ | `The head part is the UPPER part only: no lower jaw, no neck; the lower jaw is its own separate part.` |",
           "| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |"]
    open(os.path.join(PK, "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    for p in made:
        print(W(p))
    if len(made) == 1:
        print("(chưa dựng lượt 2: chưa có", W(CONCEPT) + ")")


if __name__ == "__main__":
    build()
