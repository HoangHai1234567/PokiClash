# -*- coding: utf-8 -*-
"""Gói GPT vẽ DẠNG 1 của Voọc Tướng (tho_hoang, mã làm việc kiem_si): voọc non, tướng thứ 8 đảo Mộc. Gói vào gui_gpt/kiem_si_non/.

Dạng 1 dùng CHUNG rig với dạng lớn (monster_3620): kiem_si_non.py đổi tỉ lệ (nửa thân trên co 0,8 quanh hông, đầu + mũ × 1,4 so với
thân, chân ngắn lại, mầm lá mào). Bố cục = hình rig dạng non dựng bằng da dạng lớn (kiem_si_non.py bo_cuc). Các mảnh giáp, kiếm, áo tơi,
chân giữ HÌNH của dạng lớn (sau này đổi màu bằng mã), chỉ đầu, mặt, mũ, mào vẽ mới. Hai hướng màu là ĐỀ XUẤT của Claude, chờ người dùng chọn.
Toạ độ trong prompt đo bằng `kiem_si_non.py vung` (px trên hình bố cục 1536 × 1024).

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/kiem_si_non.py bo_cuc
    py -3 -I ArtGen/Spine/build_kiem_si_non.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/kiem_si_non/luot_1_concept_<hướng>.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.join(HERE, "gui_gpt", "kiem_si_non")
TAI = os.path.join(HERE, "inbox", "kiem_si_non", "tai_ve")
BO_CUC = os.path.join(HERE, "inbox", "kiem_si_non", "mau", "bo_cuc.png")
LON = os.path.join(HERE, "inbox", "kiem_si_1", "tai_ve", "L1_duyet.png")

HUONG = {
    "cam": dict(
        ten="A · voọc con lông cam (như voọc con ngoài đời, lớn lên mới sẫm lại)",
        fur="bright young orange (#E8873A): a langur baby is born with bright orange fur that darkens to charcoal as it grows up",
        fur_hex="#E8873A", ruff="soft cream (#F4E7C8)", skin="pale pink-tan (#EBC3A0)",
        iris="warm dark brown (#7A4A22)",
        helmet="a small round helmet BOWL of fresh young green (#6FA65A) made of a few vertical plates, with a small bamboo knob on top and two "
               "rivet dots; a pale bamboo (#E3CB8A) brow band; at the back a short NECK GUARD of two or three small tiers of light young green "
               "(#8DBF6A) laced with pale yellow cord (#F0D66A), sweeping out and down to the left; at the front a short rounded VISOR that "
               "stops ABOVE the brow (the big eye stays fully visible)",
        crest="TWO small young leaves standing up from the front of the bowl in a V, like a seedling's first pair of leaves (one tip at about "
              "(1110, 150), the other leaning right with its tip at about (1240, 205)); spring green (#8CC85A) and light yellow-green (#C2DE7A), "
              "each a simple pointed leaf with one centre vein. No big blade-like leaf",
        plates="light young green (#8DBF6A)", trim="pale bamboo straw (#E3CB8A)", cord="pale buttery yellow (#F0D66A)",
        cape="fresh young green (#5FA858)", skirt="light brown cloth (#8A6446)",
        swords="WOODEN practice swords: each scabbard is a slim tube of young green bamboo (#B9C46A) with two or three darker bamboo node "
               "rings (#8E9A48); each hilt is wrapped in cream cord (#F4E7C8) in a diamond pattern with light brown (#9A6E48) diamonds and a "
               "pale wood end cap; the guard is a small round disc of light wood (#B98A55)",
        tail="orange like the fur with a cream (#F4E7C8) tuft at the tip",
        colours=[("fur (head, arms, thighs, tail)", "#E8873A"), ("whisker ruff, beard, tail tuft, hilt cord", "#F4E7C8"),
                 ("bare face, hands, feet", "#EBC3A0"), ("armour plates, neck guard tiers", "#8DBF6A"), ("helmet bowl and visor", "#6FA65A"),
                 ("bamboo trim, arm guards, shin guards, emblem disc, brow band", "#E3CB8A"),
                 ("lacing cord, braided belt, tassels", "#F0D66A"), ("crest leaves", "#8CC85A and #C2DE7A"), ("leaf cape", "#5FA858"),
                 ("cloth skirt", "#8A6446"), ("bamboo scabbards", "#B9C46A with node rings #8E9A48"), ("sword guards", "#B98A55"),
                 ("hilt diamonds", "#9A6E48"), ("eye iris", "#7A4A22"), ("every outline, dark-brown ink", "#2B2118")],
        no="NO charcoal or grey fur, NO dark lacquered green, NO blue, NO purple, NO red, NO gold metal, NO grey steel",
    ),
    "xam": dict(
        ten="B · voọc con lông xám tro nhạt, nón lá nhỏ thay mũ giáp",
        fur="light ash grey (#8E8A84), a much paler version of the grown form's charcoal",
        fur_hex="#8E8A84", ruff="white (#F3EEE0), big and fluffy", skin="light tan (#E2C3A0)",
        iris="amber (#F0AA32)",
        helmet="instead of a helmet, a small CONICAL STRAW HAT (a kasa) of pale woven straw (#D9BE7A) with a few thin weave lines, sitting "
               "slightly tilted forward on the head, its wide brim covering the top of the head and the back of the neck (spread over the area of "
               "the helmet and neck guard of image 1, about x = 480 to x = 1140, y = 120 to y = 500) and ending ABOVE the brow so that the big "
               "eye stays fully visible; a moss-green (#4F8F5A) chin cord tied under the jaw",
        crest="ONE small young leaf (#8CC85A, one centre vein) tucked into the hat band at the front, standing up and leaning right (tip at "
              "about (1220, 200))",
        plates="soft moss green (#6E9A55)", trim="pale bamboo straw (#DCC184)", cord="amber (#E0A030)",
        cape="mid green (#4F8F5A)", skirt="dark brown cloth (#5C3E2A)",
        swords="real swords in their scabbards: each scabbard is warm brown lacquered wood (#7A5536) with two pale bamboo (#DCC184) bands; "
               "each hilt is wrapped in amber cord (#E0A030) in a diamond pattern showing dark brown (#463024) diamonds, with a pale bamboo end "
               "cap; the guard is a small four-lobed leaf-shaped disc of pale bamboo (#DCC184)",
        tail="ash grey like the fur with a white (#F3EEE0) tuft at the tip",
        colours=[("fur (head, arms, thighs, tail)", "#8E8A84"), ("whisker ruff, beard, tail tuft", "#F3EEE0"),
                 ("bare face, hands, feet", "#E2C3A0"), ("straw hat", "#D9BE7A"), ("armour plates", "#6E9A55"),
                 ("bamboo trim, arm guards, shin guards, emblem disc, sword guards", "#DCC184"),
                 ("lacing cord, braided belt, tassels, hilt wrapping", "#E0A030"), ("crest leaf", "#8CC85A"),
                 ("leaf cape, chin cord", "#4F8F5A"), ("cloth skirt", "#5C3E2A"), ("scabbards", "#7A5536"), ("hilt diamonds", "#463024"),
                 ("eye iris", "#F0AA32"), ("every outline, dark-brown ink", "#2B2118")],
        no="NO charcoal fur, NO dark lacquered green, NO metal helmet, NO blue, NO purple, NO red, NO gold metal, NO grey steel",
    ),
}


# LƯỢT 2 (người dùng 2026-11-13, không chọn A/B của lượt 1: "làm dạng 1 chibi cute kiểu con khỉ không giáp cầm kiếm cũ cùn hoặc cành cây
# thôi, khi có concept phải mở tôi xem"): khỉ voọc con lông cam, KHÔNG giáp; hai hướng chỉ khác vũ khí. Bố cục mau/bo_cuc_tran.png
# (kiem_si_non.py bo_cuc_tran, đầu × 1,55): vũ khí là lưỡi kiếm dài trần (nằm sẵn dọc chỗ vỏ cũ), không vỏ, không kiếm ngắn.
BO_CUC_TRAN = os.path.join(HERE, "inbox", "kiem_si_non", "mau", "bo_cuc_tran.png")
TRAN = {
    "kiem_cun": dict(
        ten="khỉ voọc con không giáp, cầm thanh kiếm cũ cùn (băng vải sờn), buộc khăn trán",
        dau="a green cloth HEADBAND (#5FA858) tied around the head just above the eye (a little would-be samurai), its knot at the back of "
            "the head with two short cloth tails flying back to the left (about x = 690 to x = 800, y = 230 to y = 320)",
        vu_khi="an OLD, BATTERED, BLUNT sword with NO scabbard: a straight katana blade of dull old iron (#9A958A) with a few rust-brown "
               "patches (#A8643A), three small nicks chipped out of its edge and a rounded, broken-off tip; it runs from the hands up and to "
               "the left, behind the near forearm, to its tip at about (290, 520). Its HILT (about x = 1000 to x = 1225, y = 770 to y = 890) "
               "is wrapped in a frayed, faded cloth strip (#C9B48A) with one loose end, and a small cracked round wooden guard (#8A6446) sits "
               "between hilt and blade. The lower part of the blade just above the guard is wrapped in the same frayed cloth: that is where "
               "the near hand holds it (the sword is so blunt that the little monkey holds it there)",
        mau=[("old iron blade", "#9A958A"), ("rust patches", "#A8643A"), ("frayed cloth wrap", "#C9B48A"), ("wooden guard", "#8A6446"),
             ("headband", "#5FA858")],
    ),
    "canh_cay": dict(
        ten="khỉ voọc con không giáp, cầm cành cây làm kiếm, đội một chiếc lá trên đầu",
        dau="one small round fresh LEAF (#8CC85A, one centre vein) sitting on top of the head like a tiny cap, its short stem sticking up "
            "(about x = 900 to x = 1060, y = 160 to y = 250)",
        vu_khi="a crooked tree BRANCH used as a sword, with NO scabbard: light brown wood (#9A6E48) with a few bark lines and two small knots "
               "(darker brown #6E4A30); it lies exactly where the sword is in image 1: its thick end is the grip in the far hand (about x = "
               "1000 to x = 1225, y = 770 to y = 890), wrapped with a few turns of green vine (#6E9A3E); the near hand holds it a little "
               "further up; it runs up and to the left, behind the near forearm, getting thinner, to a small forked tip at about (290, 520) "
               "with two or three small young leaves (#8CC85A)",
        mau=[("branch wood", "#9A6E48"), ("bark lines and knots", "#6E4A30"), ("vine wrap", "#6E9A3E"), ("leaves on the branch and the head", "#8CC85A")],
    ),
}


def prompt_tran(k, h):
    save = os.path.join(TAI, f"L2_{k}.png")
    mau = [("fur (head, body, arms, legs, tail)", "#E8873A"), ("whisker ruff, belly patch, tail tuft", "#F4E7C8"),
           ("bare face, hands, feet", "#EBC3A0"), ("eye iris", "#7A4A22"), ("vine belt", "#6E9A3E"), ("leaf skirt", "#5FA858")] + h["mau"] + \
          [("every outline, dark-brown ink", "#2B2118")]
    mau = "; ".join(f"{a} {b}" for a, b in mau)
    return f"""IMAGES (attached in this order; open each from its path):
image 1 = {BO_CUC_TRAN}: PROPORTION GUIDE, 1536x1024, white background: a computer-assembled puppet of the YOUNG form of this monkey, built from the grown form's own pieces rescaled on the animation skeleton (a big head, a compact body, short legs, a long curled tail) with all the armour removed. It gives the exact pose, the proportions and the place, size and overlap of every piece. Its colours, its face and its stern grown-up look are those of the GROWN form and must be changed as described below; the slatted bamboo arm guards and shin guards still visible on it must be drawn as bare furry forearms and shins.
image 2 = {LON}: the approved GROWN form of the same creature, 1536x1024, white background: a langur warlord in samurai armour (charcoal fur, white whisker ruff, bare tan face). It gives ONLY the drawing style (wobbly dark-brown ink line, crayon hatching, completely flat colour) and the family look of the face. The young form has NO armour at all.

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L2_{k}_2.png, L2_{k}_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: draw the YOUNG FORM (the first evolution stage) of the langur of image 2, as ONE picture, landscape 1536x1024, pure-white background, in the same hand-drawn style. Keep EXACTLY the pose, the proportions and the place and size of every piece of image 1 (the picture will be mapped back onto that skeleton): the same low, hunched stance leaning toward the viewer's RIGHT, the big head in three-quarter profile looking RIGHT with ONLY ONE eye visible, both hands low in front of the belly on the long weapon, short legs planted wide, the long tail curling up behind.

CHARACTER: a CUTE CHIBI BABY LANGUR (a little leaf monkey) who plays at being a swordsman: a big round head, a small plump body, short arms and legs, soft fluffy bright orange baby fur (#E8873A: langur babies are born bright orange). Endearing and very cute, but with a determined, brave little glare and a firm stance, ready to fight; not a smiling or laughing mascot, not scary, not a human. NO ARMOUR AT ALL: no helmet, no shoulder guards, no cuirass, no arm guards, no shin guards, no tassels, no scabbard, no second sword.

Coordinates are pixels on the 1536x1024 canvas (x from the left, y from the top); they are the places of the pieces in image 1.
- HEAD AND FACE (about x = 760 to x = 1250, y = 195 to y = 690): a BIG round baby langur head of fluffy orange fur with a little tuft of hair sticking up on top; a round, fluffy RUFF of soft cream (#F4E7C8) whiskers framing the face, with a short tufted chin; a bare FACE of pale pink-tan (#EBC3A0): a short rounded muzzle with two nostril dots, round cheeks, a small mouth shut in a firm little pout (NO fang, no teeth). ONE eye at about (1085, 400): BIG and ROUND (about 70 px wide): warm dark brown (#7A4A22) iris, a big round dark pupil, one tiny white dot, a clean ink rim, and a SHORT slanted brow above it tilting down toward the nose (determined, not angry, not sad). No second eye. No chin cord.
- ON THE HEAD: {h['dau']}.
- BODY: a small round furry orange body (about x = 610 to x = 1140, y = 230 to y = 870) with a soft cream (#F4E7C8) belly patch; around the waist (where image 1 has the braided rope, about x = 700 to x = 1095, y = 500 to y = 780) a simple belt of one twisted green VINE (#6E9A3E) with a little knot; hanging from it a short SKIRT of four big pointed leaves (#5FA858, each with a darker centre vein) (about x = 630 to x = 1010, y = 615 to y = 900).
- ARMS: short furry orange arms. The near arm (viewer's left, in front of the body): upper arm about x = 505 to x = 790, y = 380 to y = 740; forearm where image 1 shows the near arm guard (about x = 480 to x = 865, y = 630 to y = 845), drawn as a plain furry forearm of about the same size. The far arm (viewer's right): upper arm about x = 985 to x = 1215, y = 355 to y = 680, forearm about x = 1010 to x = 1245, y = 585 to y = 840. Small bare monkey hands of pale pink-tan (#EBC3A0) with short thick fingers: the near hand at about (880, 760), the far hand at about (1085, 800), both closed around the weapon.
- WEAPON (exactly one, held in both hands): {h['vu_khi']}.
- LEGS: two short bent furry orange legs planted wide: the REAR foot at the left (about x = 370 to x = 575, y = 870 to y = 960) and the FRONT foot at the right (about x = 950 to x = 1150, y = 875 to y = 960); where image 1 shows shin guards, plain furry shins; bare monkey FEET of pale pink-tan with gripping toes.
- TAIL: one long orange langur tail rising from behind the lower back, up behind the back to a curl at the top left (about x = 435 to x = 655, y = 60 to y = 445), about 40 px thick, with a cream (#F4E7C8) fluffy tuft at the curled tip, as in image 1.
- Exactly: one head with one eye, two arms, two hands, one weapon, one vine belt with a leaf skirt, two legs, one tail. Nothing else.

COLOURS (use exactly these, each area one flat colour): {mau}. Only these colours. NO armour colours, NO blue, NO purple, NO red, NO gold, NO shiny steel.

CANVAS AND FRAMING: as in image 1 the whole figure with its weapon and tail is about 1000 px wide (x = 265 to x = 1270) and about 900 px tall (y = 60 to y = 962); nothing cut by the edges; no ground, no cast shadow.

POSE (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): calm, clean resting pose exactly as in the guide. Every piece is a clear shape with its own ink outline: head, ruff, body, each upper arm, each forearm, each hand, the weapon, the belt, each leaf of the skirt, each leg, each foot, the tail. The weapon is one straight clean shape (the branch may bend gently). No dust, no leaves flying, no sparkles, no glow, no motion lines, no ground, no grass, no props.

HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly like a real pen; loose crayon hatching inside every area. Image 1 is a rough machine-assembled puppet: take its pose, proportions, placement and sizes, but redraw every part cleanly and cutely (do not copy its seams, its blurred edges, its arm guards or the grown form's stern face).
LINE AND COLOUR: the game's hand-drawn look of the approved hero image (image 2): drawn by hand on paper with a dark-brown ink pen (#2B2118), an outline about 6 px thick on this canvas around every big piece (head, body, arms, legs, tail, weapon, skirt), and about 4 px for small details (fingers, toes, the eye, leaf veins, the vine, nicks, knots); every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor an over-rendered painting.
FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do not model light. No shading, no darker underside, no lighter patches, no shadows of any kind (no cast shadow of one piece on another, no shadow under the figure or on the background), no white highlights or shine spots (not on the blade), no gloss, no glow, no rim light, no gradients, no 3D look. The only exception: one tiny light dot in the eye. A different tone appears only where the design itself lists a different colour.
Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects around the character.
"""


# LƯỢT 3 (người dùng 2026-11-13): chọn L2_kiem_cun, "con này nhưng đổi màu lông sang gần giống dạng [lớn] nhưng nhạt hơn" (kiem_si_non_long.py
# → L2_kiem_cun_6f6a63.png, lông xám #6F6A63), rồi "kiếm cùn ở trong, bao kiếm ở ngoài bằng gỗ, xem kĩ lại nhé": kiếm nằm trong vỏ gỗ, cầm như
# dạng lớn (tay gần nắm vỏ sát miệng, kiếm cách ở miệng vỏ, tay xa nắm chuôi). Bố cục mau/bo_cuc_bao.png (cùng hệ toạ độ với bo_cuc_tran).
BO_CUC_BAO = os.path.join(HERE, "inbox", "kiem_si_non", "mau", "bo_cuc_bao.png")
CHON_XAM = os.path.join(TAI, "L2_kiem_cun_6f6a63.png")


def prompt_bao():
    save = os.path.join(TAI, "L3_bao_go.png")
    return f"""IMAGES (attached in this order; open each from its path):
image 1 = {BO_CUC_BAO}: PROPORTION GUIDE, 1536x1024, white background: a computer-assembled puppet of this young monkey on the animation skeleton. It gives the exact place and size of every piece and, most importantly here, of the SWORD IN ITS SCABBARD: the long scabbard running diagonally from its closed tip at the upper left down to its mouth at the near hand, the guard at the scabbard's mouth, the hilt continuing to the right through the far hand. Its colours, its face, its arm guards and shin guards are NOT to be copied.
image 2 = {CHON_XAM}: the APPROVED DESIGN of this character, 1536x1024, white background: a cute chibi baby langur with soft grey fur, a cream whisker ruff and belly patch, a peach-tan face, hands and feet, one big round brown eye with a determined little brow, a green cloth headband with two flying tails, a green vine belt and a skirt of big green leaves, holding an old blunt sword low with both hands. Keep this character EXACTLY: same drawing, same proportions, same pose, same colours, same face, same headband, same skirt, same tail.
image 3 = {LON}: the grown form of the same creature (armoured langur samurai): look ONLY at HOW it holds its sheathed long sword (the near hand grips the scabbard just below its mouth, the round guard sits at the mouth of the scabbard, the far hand closes on the hilt, NO bare blade visible). Copy nothing else from it.

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L3_bao_go_2.png, L3_bao_go_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: redraw the character of image 2 EXACTLY as it is (one picture, landscape 1536x1024, pure-white background, same hand-drawn style), with ONE change only: the old blunt sword is now SHEATHED. The blunt blade is completely hidden INSIDE a plain WOODEN SCABBARD; NO bare blade, no rust and no chipped edge are visible anywhere.

THE SWORD IN ITS SCABBARD (place it as in image 1; coordinates are pixels on the 1536x1024 canvas, x from the left, y from the top):
- SCABBARD: one long, slim, straight shape of plain, old, light-brown WOOD (#A27B54) with a few thin wood-grain lines (#7A5A3C, pencil, not ink), a small crack near its middle bound with two turns of frayed cloth (#C9B48A), and a slightly worn, rounded, closed tip. It runs diagonally from its closed tip at the upper left (about (225, 490)) down and to the right to its open MOUTH at about (965, 775), about 42 px thick. It passes BEHIND the near arm (viewer's left) and in FRONT of the body and the leaf skirt, exactly where image 1 shows the scabbard. No lacquer, no metal fittings, no bands of bamboo: just worn plain wood.
- NEAR HAND (peach-tan, at about (880, 760)): closed around the scabbard just below its mouth (where image 2 had the hand on the cloth-wrapped blade).
- GUARD: the small cracked round wooden guard (#8A6446) of image 2 sits right at the scabbard's mouth (about (1010, 790)), between the near hand and the far hand.
- HILT: the hilt of image 2, wrapped in frayed, faded cloth (#C9B48A) with one loose end hanging down, continues the same straight line to the right through the FAR HAND (peach-tan, at about (1090, 800)) to its end at about (1225, 880).
- The scabbard, the guard and the hilt are ONE straight line, like a sword resting in its sheath held low and ready to draw.

EVERYTHING ELSE stays exactly as in image 2: the grey fur (#6F6A63) on the head, body, arms, legs and tail; the cream (#F4E7C8) ruff, belly patch and tail tuft; the peach-tan face, hands and feet; the one big round brown eye with its tiny white dot and short determined brow; the green headband (#5FA858) with its two flying tails; the green vine belt (#6E9A3E) and the skirt of big leaves (#5FA858); the hunched stance facing the viewer's RIGHT; the tail curling up at the upper left. No armour, no helmet, no second sword.

COLOURS (each area one flat colour): as in image 2, plus the scabbard light-brown wood (#A27B54) with grain lines #7A5A3C and cloth bindings #C9B48A. Every outline dark-brown ink (#2B2118). Only these colours.

LINE AND COLOUR: exactly the hand-drawn look of image 2: wobbly dark-brown ink pen outline about 6 px thick around big pieces (the scabbard included) and about 4 px for small details; coloured-pencil and wax-crayon hatching visible inside every area. FLAT COLOUR, NO LIGHT, NO SHADOW: every area one even colour; no shading, no shadows of any kind, no highlights or shine spots (not on the scabbard), no gloss, no glow, no gradients; only one tiny light dot in the eye. Plain pure-white background (#FFFFFF), no ground, no cast shadow, no white border or sticker outline, no text, no frame, no effects. Nothing cut by the edges.
"""


def prompt(k, h):
    save = os.path.join(TAI, f"L1_{k}.png")
    mau = "; ".join(f"{a} {b}" for a, b in h["colours"])
    return f"""IMAGES (attached in this order; open each from its path):
image 1 = {BO_CUC}: PROPORTION GUIDE, 1536x1024, white background: a computer-assembled puppet of the YOUNG form of this langur samurai, built from the grown form's own pieces rescaled on the animation skeleton (big head and helmet, a smaller compact body, shorter legs, small crest leaves). It gives the exact pose, the proportions and the place, size and overlap of every piece. Its colours, its face and its headgear are those of the GROWN form and must be changed as described below.
image 2 = {LON}: the approved GROWN form of the same creature, 1536x1024, white background: a langur warlord dressed as a samurai general (charcoal fur, a white whisker ruff around a bare tan face, lacquered moss-green armour trimmed with pale bamboo and laced with amber cord, a huge near shoulder guard with a round leaf emblem and three tassels, a dark green kabuto helmet with a leaf crest, a rain cape of big jungle leaves, two sheathed swords held low, ready to draw). It gives the drawing style (wobbly dark-brown ink line, crayon hatching, completely flat colour) and the family look. The young form must clearly be the same species at a much younger age.

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: draw the YOUNG FORM (the first evolution stage) of the langur samurai of image 2, as ONE picture, landscape 1536x1024, pure-white background, in the same hand-drawn style. Keep EXACTLY the pose, the proportions and the place and size of every piece of image 1 (the picture will be mapped back onto that skeleton): the same low, hunched quick-draw stance leaning toward the viewer's RIGHT, the head in three-quarter profile looking RIGHT with ONLY ONE eye visible, both hands low in front of the belly on the long sheathed sword, short legs planted wide.

CHARACTER: a brave little langur trainee who already wants to be a great swordsman: big-headed, compact and endearing, but with a determined, battle-ready little glare and a firm stance; not a smiling baby mascot, not scary, not a human. The young one wears smaller, lighter armour of the same cut as the grown form. Its fur is {h['fur']}.

WHAT CHANGES, WHAT STAYS:
- REDESIGN the HEAD, the FACE, the HEADGEAR and the CREST as described below (these are new drawings).
- KEEP the SHAPE, the place and the size of every other piece exactly as in image 1 and only change its colours as listed: the near shoulder guard with its emblem and three tassels, the far shoulder guard with one tassel, the chest cuirass, the braided rope belt and its hanging loop, the skirt, the upper arms, both arm guards, both hands, both swords, the leaf cape, the thighs, the shin guards and the feet. (Those pieces will be recoloured from the grown form, so their outlines must stay the same.)

Coordinates are pixels on the 1536x1024 canvas (x from the left, y from the top); they are the places of the pieces in image 1.
- HEAD AND FACE (about x = 690 to x = 1120, y = 350 to y = 740): a BIG round young langur head: fur {h['fur_hex']} at the back of the head; a round, fluffy RUFF of soft whiskers of {h['ruff']} framing the whole face like a soft mane, with a short tufted beard (shorter and rounder than the grown form's); a bare FACE of {h['skin']}: a short muzzle with two nostril slits, small round cheeks, a small mouth shut in a firm, slightly pouting line (NO fang). ONE eye at about (1035, 550): clearly BIGGER and ROUNDER than the grown form's eye (about 60 px wide): {h['iris']} iris, a big round dark pupil, one tiny white dot, a clean ink rim, and a SHORT slanted brow stroke above it tilting down toward the nose (a determined frown, not angry, not sad). No second eye. A small chin cord under the jaw.
- HEADGEAR (about x = 480 to x = 1140, y = 60 to y = 500): {h['helmet']}.
- CREST: {h['crest']}.
- NEAR SHOULDER GUARD (viewer's left, in FRONT of the body, about x = 435 to x = 775, y = 350 to y = 650): the same slanted shield of horizontal plates as image 1, plates {h['plates']}, frame {h['trim']}, cross-stitch lacing {h['cord']}; the round emblem disc (centre at about (630, 465)) {h['trim']} with one green leaf; THREE tassels {h['cord']} hanging from its lower edge (about x = 460 to x = 680, y = 580 to y = 730).
- FAR SHOULDER GUARD (viewer's right, about x = 1030 to x = 1160, y = 385 to y = 625), seen almost edge-on, same colours, ONE tassel below it (about x = 1095 to x = 1160, y = 605 to y = 705).
- BODY: the chest cuirass (about x = 710 to x = 965, y = 570 to y = 775) in {h['plates']} with a {h['trim']} rim; the thick braided rope belt (about x = 685 to x = 1010, y = 580 to y = 815) and its hanging loop in {h['cord']}; the skirt below it in {h['skirt']}; fur {h['fur_hex']} at the neck, under the arms and at the flanks.
- ARMS: furry upper arms ({h['fur_hex']}); the near arm guard (about x = 510 to x = 820, y = 690 to y = 865) and the far arm guard (about x = 940 to x = 1130, y = 655 to y = 865) are slatted bamboo guards in {h['trim']} with two green bands; bare monkey hands in {h['skin']}: the near hand at about (853, 780) grips the mouth of the long scabbard, the far hand at about (1010, 800) closes on its hilt.
- SWORDS (both completely sheathed, NO bare blade anywhere): {h['swords']}. The LONG scabbard runs diagonally from its closed tip at the upper left (about x = 290, y = 580) down to the near hand, passing BEHIND the near shoulder guard and the near forearm; its hilt continues to the right of the near hand (about x = 890 to x = 1135, y = 775 to y = 950). The SHORT sword goes through the belt: its scabbard runs from the belt back and down to the lower left (about x = 375 to x = 865, y = 670 to y = 885), its hilt sticks out forward across the belly (about x = 800 to x = 995, y = 610 to y = 760).
- LEAF CAPE: a cape of big overlapping jungle leaves in {h['cape']} with darker centre veins hangs BEHIND the body; it shows at the lower left between the shoulder guard and the scabbards (about x = 440 to x = 560, y = 600 to y = 800).
- LEGS: two short bent legs: the REAR foot at the left (about x = 415 to x = 585, y = 825 to y = 960) and the FRONT foot at the right (about x = 885 to x = 1050, y = 850 to y = 960); each a short furry thigh, a slatted bamboo shin guard ({h['trim']}) and a bare monkey FOOT with gripping toes ({h['skin']}).
- TAIL: a langur tail, {h['tail']}, rises from behind the back and shows only a little behind the headgear at the upper left (as in image 1, about x = 470 to x = 650, y = 230 to y = 540).
- Exactly: one head with one eye, one headgear, the crest described above, two shoulder guards (four tassels in all), one cuirass, one rope belt, two arm guards, two hands, two sheathed swords, one leaf cape, two legs, one tail.

COLOURS (use exactly these, each area one flat colour): {mau}. The young form is LIGHTER and softer in colour than the grown form of image 2. Only these colours. {h['no']}.

CANVAS AND FRAMING: as in image 1 the whole figure with its swords is about 890 px wide (x = 270 to x = 1160) and about 900 px tall (y = 60 to y = 962); nothing cut by the edges; no ground, no cast shadow.

POSE (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): calm, clean resting pose exactly as in the guide. Every piece is a clear shape with its own ink outline: headgear, head, each shoulder guard, each tassel, each upper arm, each arm guard, each hand, cuirass, rope belt, each scabbard, each hilt, cape, each leg, tail. The swords are straight clean shapes. No dust, no leaves flying, no sparkles, no glow, no motion lines, no ground, no grass, no props.

HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly like a real pen; loose crayon hatching inside every area. Image 1 is a rough machine-assembled puppet: take its pose, proportions, placement, sizes and piece outlines, but redraw every part cleanly (do not copy its seams, its blurred edges or the grown form's face and helmet).
LINE AND COLOUR: the game's hand-drawn look of the approved hero image (image 2): drawn by hand on paper with a dark-brown ink pen (#2B2118), an outline about 6 px thick on this canvas around every big piece (head, headgear, shoulder guards, cuirass, belt, arm guards, scabbards, cape, legs, tail), and about 4 px for small details (fingers, toes, lacing, tassels, the eye, leaf veins, bands on the scabbards); every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor an over-rendered painting.
FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do not model light. No shading, no darker underside, no lighter patches, no shadows of any kind (no cast shadow of one piece on another, no shadow under the figure or on the background), no white highlights or shine spots (not on the armour, not on the scabbards, not on the headgear), no gloss, no glow, no rim light, no gradients, no 3D look. The only exception: one tiny light dot in the eye. A different tone appears only where the design itself lists a different colour.
Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects around the character.
"""


def huong_dan():
    out = [f"""# Gói gửi GPT: `kiem_si_non` (DẠNG 1 của Voọc Tướng: voọc non; tướng thứ 8 đảo Mộc, id game `tho_hoang`)

Làm 2026-11-13 ở máy ổ D. Dạng 1 dùng CHUNG rig với dạng lớn (`monster_3620`), đổi tỉ lệ ở rig (`ArtGen/Spine/kiem_si_non.py`): nửa thân
trên co 0,8 quanh hông (hai tay vẫn cùng nắm một thanh kiếm), đầu + mũ to 1,4 lần so với thân, chân ngắn lại, lá mào còn mầm nhỏ. Bố cục =
hình rig dạng non ghép bằng da dạng lớn (`py -3 -I ArtGen/Spine/kiem_si_non.py bo_cuc`). Mảnh giáp, kiếm, áo tơi, chân giữ HÌNH dạng lớn
(sau đổi màu bằng mã); chỉ đầu, mặt, mũ, mào vẽ mới. Màu và mũ là đề xuất của Claude, chờ người dùng chọn. Ghi chú: `ArtGen/Spine/inbox/kiem_si_ghichu.md`.
"""]
    for k, h in HUONG.items():
        p = os.path.join(PK, f"luot_1_concept_{k}.txt")
        out.append(f"""## Hướng `{k}`: {h['ten']}

**Chỉ gửi GPT đường dẫn:** `{p}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{os.path.join(TAI, f'L1_{k}.png')}` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/kiem_si_non/luot_1_concept_{k}.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `{BO_CUC}` | Bố cục voọc non (1536 × 1024, nền trắng): hình rig dạng non ghép bằng da dạng lớn: mũ giáp + đầu rất to, thân gọn, tấm vai to có huy hiệu lá và ba tua ở trái, hai tay cầm kiếm còn trong vỏ thấp trước bụng, chân ngắn. Lấy dáng, tỉ lệ, chỗ đặt, hình từng mảnh; màu, mặt, mũ phải đổi |
| 2 | `{LON}` | Concept dạng lớn đã duyệt (1536 × 1024, nền trắng): voọc tướng quân lông than, ria trắng, giáp sơn lục rêu, mũ kabuto mào lá. Lấy nét vẽ, tô phẳng, vẻ cùng loài |
""")
    out.append(f"""## Lượt 2: khỉ voọc con KHÔNG GIÁP (người dùng 2026-11-13, thay hai hướng trên)

"làm dạng 1 chibi cute kiểu con khỉ không giáp cầm kiếm cũ cùn hoặc cành cây thôi". Lông cam như hướng A; hai hướng chỉ khác vũ khí.
Bố cục mới: `py -3 -I ArtGen/Spine/kiem_si_non.py bo_cuc_tran` (đầu × 1,55; ẩn mọi mảnh giáp, mũ, áo tơi, vỏ kiếm, kiếm ngắn; lưỡi kiếm dài trần
hiện ở dáng nghỉ, hai tay cùng nắm).
""")
    for k, h in TRAN.items():
        p = os.path.join(PK, f"luot_2_concept_{k}.txt")
        out.append(f"""### `{k}`: {h['ten']}

**Chỉ gửi GPT đường dẫn:** `{p}`. Ảnh lưu vào `{os.path.join(TAI, f'L2_{k}.png')}` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/kiem_si_non/luot_2_concept_{k}.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `{BO_CUC_TRAN}` | Bố cục khỉ con không giáp (1536 × 1024, nền trắng): rig dạng non ghép bằng da dạng lớn đã bỏ giáp: đầu to bờm trắng, thân lông than, đuôi cong vút lên ở trên trái, hai tay cầm thanh kiếm trần chĩa lên trái, còn bao tay và giáp ống chân bằng tre (phải vẽ thành cẳng tay, ống chân lông). Lấy dáng, tỉ lệ, chỗ đặt |
| 2 | `{LON}` | Concept dạng lớn đã duyệt (1536 × 1024, nền trắng): voọc tướng quân mặc giáp. Chỉ lấy nét vẽ, tô phẳng, nét mặt cùng loài |
""")
    out.append(f"""## Lượt 3: kiếm cũ cùn TRONG VỎ GỖ, lông xám (người dùng 2026-11-13)

Chọn `kiem_cun`; lông đổi sang xám nhạt hơn dạng lớn bằng mã (`py -3 -I ArtGen/Spine/kiem_si_non_long.py` → `L2_kiem_cun_6f6a63.png`);
"kiếm cùn ở trong, bao kiếm ở ngoài bằng gỗ". Bố cục `py -3 -I ArtGen/Spine/kiem_si_non.py bo_cuc_bao` (cùng hệ toạ độ với `bo_cuc_tran`).

**Chỉ gửi GPT đường dẫn:** `{os.path.join(PK, 'luot_3_concept_bao_go.txt')}`. Ảnh lưu vào `{os.path.join(TAI, 'L3_bao_go.png')}` (trùng tên thì `_2`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/kiem_si_non/luot_3_concept_bao_go.txt`.

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `{BO_CUC_BAO}` | Bố cục (1536 × 1024, nền trắng): rig dạng 1 không giáp, có VỎ kiếm dài chéo từ trên trái xuống tay gần, kiếm cách ở miệng vỏ, chuôi qua tay xa. Lấy chỗ đặt vỏ, kiếm cách, chuôi |
| 2 | `{CHON_XAM}` | Concept đã chọn, lông đã đổi xám (1536 × 1024, nền trắng): khỉ con chibi, khăn trán xanh, váy lá, cầm kiếm cũ trần. Giữ y con này |
| 3 | `{LON}` | Dạng lớn: chỉ xem cách cầm kiếm trong vỏ (tay gần nắm vỏ sát miệng, tay xa nắm chuôi) |
""")
    m4 = {"N1": ("tờ thân 1: đầu chibi có khăn trán, hai đuôi khăn, đai dây leo", "bốn ô: đầu cũ mờ trong viền xám (chỗ mắt, mõm, bờm) + vùng chấm phía trên, hai dải vải lục, đai dây thừng lục"),
          "N2": ("tờ thân 2: hai cẳng tay lông, hai ống chân lông, váy lá", "năm hình bóng phẳng viền nâu: hai cẳng tay xám, váy lục, hai ống chân xám"),
          "S": ("tờ kiếm: vỏ gỗ, lưỡi cùn, chuôi quấn vải + kiếm cách gỗ", "ba hình bóng nằm ngang, mũi bên trái: vỏ nâu, lưỡi xám, chuôi be có kiếm cách to ở đầu trái")}
    out.append("## Lượt 4: mảnh của dạng 1 (concept duyệt 2026-11-13, người dùng: \"duyệt, làm hết 1 lượt đi\")\n\n"
               "Sinh bằng `py -3 -I ArtGen/Spine/kiem_si_non_manh.py to` (tờ hướng dẫn `inbox/kiem_si_non/mau/to_<tờ>.png`); cắt bằng `... cat`. "
               "Mảnh lông / da khác là mảnh dạng lớn đổi màu bằng mã (`... doi_mau`).\n")
    for k, (ten, ta) in m4.items():
        out.append(f"""### `{k}`: {ten}

**Chỉ gửi GPT đường dẫn:** `{os.path.join(PK, f'luot_4_manh_{k}.txt')}`. Ảnh lưu vào `{os.path.join(TAI, f'{k}.png')}` (trùng tên thì `_2`, `_3`…).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `{os.path.join(HERE, 'inbox', 'kiem_si_non', 'mau', f'to_{k}.png')}` | Tờ hướng dẫn 1536 × 1024 nền trắng: {ta}. Giữ đúng hình bóng, chỗ, cỡ |
| 2 | `{os.path.join(TAI, 'L3_bao_go.png')}` | Concept dạng 1 đã duyệt: lấy kiểu, màu, nét |
""" + (f"| 3 | `{os.path.join(TAI, 'L2_kiem_cun_6f6a63.png')}` | Concept lông xám có lưỡi kiếm cùn lộ ra: chỉ lấy kiểu lưỡi (mẻ, gỉ, mũi gãy tròn) |\n" if k == "S" else ""))
    out.append("""## Kiểm

- Lượt 4: mỗi mảnh trùng hình bóng của ô (cẳng tay, ống chân, váy IoU ≥ 0,95 là đạt); đầu có khăn, một mắt, không nanh, không đuôi khăn
  (đuôi khăn là mảnh riêng); kiếm: ba mảnh nằm ngang kín hết bề dài ô, mũi bên trái, mũi vỏ tròn kín. Script `cat` tự canh trục kiếm về giữa ảnh.
- Lượt 3: y con ở ảnh 2 (lông xám, khăn, váy lá, mặt), kiếm nằm TRONG vỏ gỗ trơn (không lộ lưỡi), tay gần nắm vỏ sát miệng, kiếm cách ở miệng vỏ,
  tay xa nắm chuôi quấn vải; vỏ chạy chéo lên trái sau tay gần như ảnh 1.
- Lượt 2: khỉ con lông cam, chibi dễ thương nhưng ánh mắt quả quyết; **không giáp, không mũ, không vỏ kiếm, không kiếm thứ hai**; đúng một
  vũ khí hai tay cùng nắm, chĩa lên trái như ảnh 1; cẳng tay, ống chân là lông (không bao tay, giáp ống); đai dây leo + váy lá; đuôi cong ở trên trái.
- Voọc non **nhìn sang phải**, đầu to, **một mắt** to tròn có nét mày quả quyết (không cười, không buồn), không nanh.
- Dáng, chỗ đặt, cỡ từng mảnh trùng ảnh 1; tấm vai, giáp ngực, đai thừng, bao tay, kiếm, áo tơi, chân **giữ hình**, chỉ đổi màu.
- Cả hai kiếm còn trong vỏ, không lộ lưỡi; đủ bốn tua; một đuôi.
- Màu đúng bảng của hướng, nhạt hơn dạng lớn; tô phẳng, không bóng; nền trắng.

Gửi thêm khi sai: `Keep the pose, proportions and piece outlines of image 1 exactly.` · `Flat colour only, remove shadows and highlights.` ·
`Only one eye, head in three-quarter profile facing right.` · `Keep the swords fully sheathed, no bare blade.`
""")
    return "\n".join(out)


def main():
    os.makedirs(PK, exist_ok=True)
    os.makedirs(TAI, exist_ok=True)
    for k, h in HUONG.items():
        p = os.path.join(PK, f"luot_1_concept_{k}.txt")
        open(p, "w", encoding="utf-8").write(prompt(k, h))
        print(p)
    for k, h in TRAN.items():
        p = os.path.join(PK, f"luot_2_concept_{k}.txt")
        open(p, "w", encoding="utf-8").write(prompt_tran(k, h))
        print(p)
    p = os.path.join(PK, "luot_3_concept_bao_go.txt")
    open(p, "w", encoding="utf-8").write(prompt_bao())
    print(p)
    p = os.path.join(PK, "HUONG_DAN.md")
    open(p, "w", encoding="utf-8").write(huong_dan())
    print(p)


if __name__ == "__main__":
    main()
