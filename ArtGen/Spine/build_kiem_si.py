# -*- coding: utf-8 -*-
"""Gói GPT vẽ kiếm sĩ rừng mặc giáp (mã làm việc kiem_si, con gốc của rig: monster_3620). Tướng thứ 8 đảo Mộc.

Người dùng (2026-11-12): "concept như con gốc tôi gửi, biến tấu đi; con gốc là bọ hung, bạn có thể đổi sang con khỉ hoặc không nhất
thiết phải là 1 sinh vật, chỉ cần nó mặc giáp, có 1 chút thiên hướng rừng rậm, samurai". Ba hướng dưới đây là ĐỀ XUẤT của Claude, chờ
người dùng chọn. Chỉ lấy của con gốc cách dựng (dáng gù thế iai, tấm vai to phía gần, hai kiếm, chỗ đặt, cỡ, thứ tự chồng); hình từng
mảnh là của mình. Không đính ảnh con gốc; đính sơ đồ bố cục tự dựng bằng mã (kiem_si.py bo_cuc).

    py -3 -I ArtGen/Spine/kiem_si.py bo_cuc
    py -3 -I ArtGen/Spine/build_kiem_si.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/kiem_si_1/luot_1_concept_<hướng>.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "kiem_si"
K = int(os.environ.get("KS_DANG", "1"))
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
NGUOI_CAY = os.path.join(HERE, "inbox", "nguoi_cay_2", "tai_ve", "L1_duyet.png")
CHIM_LA = os.path.join(HERE, "inbox", "chim_la_1", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def pk(k=K):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def mau_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "mau")


STANCE = ("STANCE (the same in the layout guide, image 1): a low, hunched QUICK-DRAW stance. The body is a compact, heavy, rounded "
          "mass leaning forward toward the viewer's RIGHT; the head is pushed forward and down, tucked under the headgear, at "
          "about x = 920-1090, y = 380-590, looking to the RIGHT in a three-quarter profile so that ONLY ONE eye is visible (at "
          "about x = 1020, y = 490). The NEAR shoulder (viewer's left) is raised toward us and carries a HUGE shoulder guard that "
          "is the biggest single piece of the picture. Both arms reach forward and down in front of the belly: the near hand "
          "(at about x = 860, y = 790) grips the mouth of the long sheathed sword's scabbard, the far hand (at about x = 1055, "
          "y = 815) closes on its hilt, ready to draw. Short legs, feet planted wide and low. Tense, silent, dangerous: a "
          "swordsman one heartbeat before the strike. Battle-ready and determined; appealing, not scary, not a smiling cute "
          "mascot, not a human.")

SWORDS = ("- LONG SWORD (a katana, still completely inside its scabbard: NO bare blade is visible anywhere): the SCABBARD is one "
          "long, slim, slightly curved shape that runs diagonally from its closed tip far behind the figure at the upper left "
          "(about x = 222, y = 470) down to its mouth in the near hand (about x = 940, y = 800); {vo}. It passes BEHIND the big "
          "shoulder guard and the near forearm and IN FRONT of the cape. Its HILT continues the same line to the right of the "
          "near hand, almost horizontal, from about x = 966 to x = 1230, y = 760-880: {chuoi}; where the hilt meets the scabbard "
          "sits the guard, {tsuba}. The far hand's fingers lie over the hilt.\n"
          "- SHORT SWORD (the second sword, also fully sheathed, worn through the belt): its scabbard runs from the belt at "
          "about x = 875, y = 650 back and down to the lower left, ending at about x = 335, y = 850 (it shows below the near "
          "forearm and crosses under the long scabbard); its hilt sticks out forward across the belly from about x = 860 to "
          "x = 1050, y = 600-695, tilted slightly upward. Same materials as the long sword, shorter.")

POSE = ("ANIMATION-READY (very important: the picture will be cut into separate rigid pieces and animated with a 2D skeleton): "
        "calm, clean resting pose exactly as in the guide. Draw every piece as a clear, simple, closed shape with its own ink "
        "outline, so that the pieces can be separated: headgear / head / each shoulder guard / upper arm / forearm guard / hand / "
        "chest armour / belt rope / each sword scabbard / each hilt / each tassel / each leg / cape{duoi}. The two swords are "
        "straight clean shapes, not bent by perspective. No dust, no leaves flying, no speed lines, no glow, no ground, no grass, "
        "no props, no second character.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram made of rough blobs with jagged edges: take ONLY the placement, the sizes, the "
        "overlaps and the kind of colour of each piece from it, never its line, its jagged edge noise or its exact blob shapes. "
        "Design the real shape of every piece yourself as described: bold, chunky, readable shapes with a clear silhouette, and "
        "a rich but tidy amount of detail on the armour (lacing rows, bands, rivets, one emblem), the way a carefully designed "
        "armoured Pokemon is drawn. Do not leave any piece as a plain empty blob.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 6 px thick on this canvas around every big piece, and about 4 px for "
        "small details (fingers, lacing, tassels, the eye, leaf veins, bands on the scabbards); every area coloured with coloured "
        "pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the outline), kept inside "
        "the outline. Clean and appealing, neither a crude scribble nor an over-rendered painting.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker underside, no lighter patches, no shadows of any kind (no cast shadow of one "
        "piece on another, no shadow under the figure or on the background), no white highlights or shine spots (not on the "
        "armour, not on the scabbards, not on the hat), no gloss, no reflections, no glow, no rim light, no gradients, no 3D "
        "look. The only exception: one tiny light dot in the eye. A different tone appears only where the design itself lists a "
        "different colour.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the character.")

FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the whole figure with its swords is about 1030 px wide (from the tip of the "
         "long scabbard at about x = 220 to the far shoulder guard at about x = 1250) and about 850 px tall (from the top of the "
         "headgear at about y = {top} to the feet at about y = 925).")

D = {}

D["khi_non"] = dict(
    ten="khỉ ronin đội nón lá, giáp nan tre, áo tơi lá",
    top=75,
    duoi=" / tail",
    intro=("CREATURE: a MONKEY RONIN of the rainforest, a plant-element monster for a monster-collecting game: a stocky, "
           "broad-backed wild monkey (macaque-like, NOT a human, NOT a cute pet) who wanders the jungle as a masterless samurai. "
           "He wears armour he made himself from the forest: split BAMBOO slats laced with dark green cord, dark hardwood "
           "guards, a rain cape of big jungle LEAVES, a wide woven straw HAT. Two swords."),
    body=("- HAT (the headgear; from about x = 610 to x = 1245, y = 75 to y = 470): a WIDE, low, conical woven straw hat (a "
          "wandering swordsman's kasa), much wider than the head, tilted forward and down toward the right so that its front "
          "brim hides the forehead and the top of the face and throws the face into its cover; apex at about x = 898, y = 95 "
          "with a small knotted orange cord tuft; the brim is one big tilted oval. Thin straw ribs radiate from the apex to "
          "the brim, two or three rings of weaving run around it, the rim is bound with a darker band, ONE ragged notch is torn "
          "out of the back brim, and TWO fresh green leaves on a short twig are stuck into the weave at the back left (about "
          "x = 640-790, y = 110-250). A dark green chin cord runs from under the brim to the jaw.\n"
          "- HEAD AND FACE (under the hat): a round monkey head with short russet fur on the cheeks and the back of the head "
          "and a bare tan FACE: a heavy brow ridge pressed low (angry, concentrated), ONE visible eye that is narrow and sharp "
          "with an amber iris, a short flat muzzle with two nostril slits, a wide mouth shut in a firm downturned line with "
          "ONE small lower fang showing, and a tuft of longer cheek fur sweeping back. One round ear at the back of the cheek.\n"
          "- NEAR SHOULDER GUARD (viewer's left, in FRONT of everything, from about x = 400 to x = 820, y = 240 to y = 680): a "
          "huge slanted rectangular shoulder shield (a samurai sode) built from five or six horizontal BAMBOO slats, each slat "
          "its own band, laced together by two vertical rows of dark green cord cross-stitches; a dark hardwood frame along its "
          "top and bottom edges; in its upper middle (centre at about x = 585, y = 400, about 165 px across) ONE big round dark "
          "wooden EMBLEM disc carved with a single leaf. Along its lower edge hang THREE orange cord TASSELS (at about x = 445, "
          "x = 525 and x = 620, each about 120 px long, each a separate little shape with a round knot on top).\n"
          "- FAR SHOULDER GUARD (viewer's right, BEHIND the far arm, from about x = 1108 to x = 1245, y = 290 to y = 630): the "
          "same kind of bamboo shield seen almost edge-on, narrow; ONE orange tassel hangs from its lower end (about "
          "x = 1194-1241, y = 541-661).\n"
          "- CHEST AND BELLY: the torso is a big round furry barrel (russet fur shows at the neck, under the arms and at the "
          "flanks). On its front a rounded bamboo CUIRASS of vertical slats laced with green cord (about x = 738-1061, "
          "y = 466-738). Around the waist a thick BRAIDED ROPE BELT of twisted dark green vine (about x = 575-905, "
          "y = 536-788), knotted at the front, with one loop of the same braid hanging over the chest at the right (about "
          "x = 888-1017, y = 397-770). Below the belt a short skirt of dark green cloth.\n"
          "- ARMS: thick upper arms covered in russet fur. Each forearm wears a long dark hardwood ARM GUARD with a bamboo "
          "rim at the wrist and ONE carved leaf-vein curl on it: the near one lies low and almost horizontal from the elbow "
          "at about x = 560, y = 710 to the wrist at about x = 840, y = 800; the far one comes down from the elbow at about "
          "x = 1140, y = 650 to the wrist at about x = 1060, y = 800. The HANDS are bare tan monkey hands with four thick "
          "fingers and a thumb.\n"
          "- LEGS: only TWO short, bent, sturdy legs show under the body, planted wide apart: the REAR foot at the left (about "
          "x = 495-615, y = 750-920) and the FRONT foot at the right (about x = 883-990, y = 765-925). Each: a short furry "
          "thigh, a shin wrapped in dark green cloth bound with cord, and a bare tan monkey FOOT with long gripping toes, "
          "toes pointing outward. No other legs.\n"
          "- TAIL: one long russet monkey tail rises from behind the lower back, up behind the near shoulder guard, and ends "
          "in a tight curl at the top left (about x = 465-645, y = 90-470), about 45 px thick, with a slightly darker tip.\n"
          "- LEAF CAPE: a rain cape made of four or five very large overlapping jungle leaves (banana-leaf shape, each with a "
          "centre vein) hangs down the back BEHIND the body and the swords; it shows at the lower left between the shoulder "
          "guard and the scabbards (about x = 404-560, y = 600-830) and a little behind the belly (about x = 900-975, "
          "y = 700-840)."),
    swords=dict(vo="dark brown lacquered wood with two pale bamboo bands near the tip and a short wrap of green vine cord near the mouth",
                chuoi="wrapped in orange cord in a diamond pattern that shows four or five pale tan diamonds, with a pale bamboo cap at its end",
                tsuba="a small round dark wooden disc shaped like a four-lobed leaf"),
    palette=("COLOURS, a calm, slightly muted palette (use exactly these, each area one flat colour): monkey fur warm russet "
             "brown (#965C38); the bare face, hands and feet tan (#E2B48A); bamboo slats, bamboo bands and the straw hat pale "
             "straw yellow (hat #D8BE7A, bamboo #CFAE6B); hardwood guards, frames and the emblem disc dark brown (#5C3E2A); "
             "lacing cord, the braided belt, the chin cord and the shin wraps dark forest green (#2F5A3A); the cloth skirt "
             "green (#3E6B45); the leaf cape and the leaves on the hat fresh leaf green (#5E9440) with darker veins; the "
             "tassels, the hat tuft and the hilt wrapping orange-vermilion (#D9622B); the scabbards very dark brown (#463024); "
             "the eye amber (#F0AA32); every outline dark-brown ink (#2B2118). Only these colours. NO blue, NO purple, NO "
             "gold metal, NO red armour, NO grey steel."),
    check=["**Khỉ** (mặt da trần, lông nâu hung), không phải người; **nón lá chóp rộng vành** chúc về trước, có hai chiếc lá giắt, vành rách một khấc.",
           "Chỉ **hai chân** khỉ (chân sau bên trái, chân trước bên phải), có **đuôi cuộn** sau lưng phía trên bên trái."],
)

D["khi_mu"] = dict(
    ten="voọc tướng quân lông than, ria trắng, mũ kabuto mào lá",
    top=40,
    duoi=" / tail",
    intro=("CREATURE: a LANGUR WARLORD of the rainforest, a plant-element monster for a monster-collecting game: a stocky, "
           "broad-backed leaf-monkey (a langur with charcoal fur and a white whisker ruff around a bare face; NOT a human, NOT "
           "a cute pet) dressed as a samurai general. His armour is lacquered moss-green plates trimmed with pale bamboo and "
           "laced with amber cord, a helmet whose crest is one great LEAF, a rain cape of big jungle leaves. Two swords."),
    body=("- HELMET (the headgear; a samurai kabuto, from about x = 612 to x = 1130, y = 65 to y = 470, its crest reaching up "
          "to about x = 1330, y = 40): a round dark-green lacquered BOWL (about x = 670-1100, y = 65-372) made of narrow "
          "vertical plates meeting at a small bamboo knob on top, with three or four rivet dots; a pale bamboo BROW BAND around "
          "its lower edge; at the back a flaring NECK GUARD of three overlapping lacquered tiers laced with amber cord, "
          "sweeping out and down to the left (to about x = 612, y = 250-450); at the front a short pointed VISOR that juts "
          "forward and down to the right over the brow (tip at about x = 1130, y = 420), hiding the forehead. The CREST: "
          "instead of horns, ONE huge fresh green LEAF with a centre vein and six side veins, shaped like a broad curved "
          "blade, rises from the front of the bowl and sweeps up and to the right (from about x = 1010, y = 300 to its tip "
          "at about x = 1330, y = 70, about 150 px wide), with ONE smaller leaf beside it (tip at about x = 1150, y = 40).\n"
          "- HEAD AND FACE (under the helmet): a round langur head: charcoal fur at the back, a wide RUFF of long white "
          "whiskers framing the whole face like a mane and a pointed white beard, and a bare tan FACE: a heavy brow pressed "
          "low (stern, commanding), ONE visible eye that is narrow and sharp with an amber iris, a short flat muzzle with two "
          "nostril slits, a wide mouth shut in a firm downturned line with ONE small lower fang showing. A dark green chin "
          "cord ties the helmet under the jaw.\n"
          "- NEAR SHOULDER GUARD (viewer's left, in FRONT of everything, from about x = 400 to x = 820, y = 240 to y = 680): a "
          "huge slanted rectangular shoulder shield (a samurai sode) of five or six horizontal lacquered moss-green plates, "
          "each plate its own band, laced together by two vertical rows of amber cord cross-stitches, with a pale bamboo "
          "frame along its top and bottom edges; in its upper middle (centre at about x = 585, y = 400, about 165 px across) "
          "ONE big round pale bamboo EMBLEM disc bearing a single green leaf. Along its lower edge hang THREE amber cord "
          "TASSELS (at about x = 445, x = 525 and x = 620, each about 120 px long, each a separate little shape with a round "
          "knot on top).\n"
          "- FAR SHOULDER GUARD (viewer's right, BEHIND the far arm, from about x = 1108 to x = 1245, y = 290 to y = 630): the "
          "same kind of shield seen almost edge-on, narrow; ONE amber tassel hangs from its lower end (about x = 1194-1241, "
          "y = 541-661).\n"
          "- CHEST AND BELLY: the torso is a big round furry barrel (charcoal fur shows at the neck, under the arms and at the "
          "flanks). On its front a rounded lacquered moss-green CUIRASS of three horizontal plates with a bamboo rim (about "
          "x = 738-1061, y = 466-738). Around the waist a thick BRAIDED ROPE BELT of twisted amber cord (about x = 575-905, "
          "y = 536-788), knotted at the front, with one loop of the same braid hanging over the chest at the right (about "
          "x = 888-1017, y = 397-770). Below the belt a short skirt of dark brown cloth.\n"
          "- ARMS: thick upper arms covered in charcoal fur. Each forearm wears a long pale BAMBOO ARM GUARD of three or four "
          "lengthwise slats bound by two green bands: the near one lies low and almost horizontal from the elbow at about "
          "x = 560, y = 710 to the wrist at about x = 840, y = 800; the far one comes down from the elbow at about x = 1140, "
          "y = 650 to the wrist at about x = 1060, y = 800. The HANDS are bare dark-tan monkey hands with four thick fingers "
          "and a thumb.\n"
          "- LEGS: only TWO short, bent, sturdy legs show under the body, planted wide apart: the REAR foot at the left (about "
          "x = 495-615, y = 750-920) and the FRONT foot at the right (about x = 883-990, y = 765-925). Each: a short furry "
          "thigh, a pale bamboo shin guard, and a bare tan monkey FOOT with long gripping toes. No other legs.\n"
          "- TAIL: one very long charcoal langur tail rises from behind the lower back, up behind the near shoulder guard, and "
          "ends in a tight curl at the top left (about x = 465-645, y = 90-470), about 45 px thick, with a white tuft at the tip.\n"
          "- LEAF CAPE: a rain cape made of four or five very large overlapping dark jungle leaves (each with a centre vein) "
          "hangs down the back BEHIND the body and the swords; it shows at the lower left between the shoulder guard and the "
          "scabbards (about x = 404-560, y = 600-830) and a little behind the belly (about x = 900-975, y = 700-840)."),
    swords=dict(vo="dark brown lacquered wood with two pale bamboo bands near the tip and a short wrap of amber cord near the mouth",
                chuoi="wrapped in amber cord in a diamond pattern that shows four or five dark diamonds, with a pale bamboo cap at its end",
                tsuba="a small round pale bamboo disc shaped like a four-lobed leaf"),
    palette=("COLOURS, a calm, slightly muted palette (use exactly these, each area one flat colour): langur fur charcoal "
             "(#403E3A); the whisker ruff, the beard and the tail tuft off-white (#EDE6D2); the bare face, hands and feet tan "
             "(#D6B08C); lacquered armour plates moss green (#4C7A3F); the helmet bowl, neck guard and visor darker forest "
             "green (#2F5A3A); bamboo trim, arm guards, shin guards and the emblem disc pale straw (#CFAE6B); lacing cord, the "
             "braided belt, the tassels and the hilt wrapping amber (#E0A030); the crest leaves fresh leaf green (#7CB048) "
             "with darker veins; the leaf cape deep green (#2F6B4A); the cloth skirt dark brown (#5C3E2A); the scabbards very "
             "dark brown (#463024); the eye amber (#F0AA32); every outline dark-brown ink (#2B2118). Only these colours. NO "
             "blue, NO purple, NO red, NO gold metal, NO grey steel."),
    check=["**Voọc** lông than, **ria trắng** quanh mặt da trần, không phải người; **mũ kabuto** sơn lục có tấm che gáy ba tầng, mào là **một chiếc lá to** quét lên phải (không sừng).",
           "Chỉ **hai chân** (chân sau bên trái, chân trước bên phải), có **đuôi dài cuộn** sau lưng phía trên bên trái, chóp trắng."],
)

D["giap_rong"] = dict(
    ten="bộ giáp cũ không người mặc, dây leo và rễ cây điều khiển",
    top=10,
    duoi="",
    intro=("CREATURE: a HAUNTED SUIT OF ARMOUR of the rainforest, a plant-element monster for a monster-collecting game. It is "
           "NOT an animal and NOT a person: the old wooden-and-bamboo armour of a long-dead jungle swordsman, left under the "
           "trees, has been grown through by living VINES and ROOTS that now wear it and fight with its two swords. Where a "
           "body would be there is only a dense bundle of twisted green vines; where a face would be, a carved wooden war "
           "MASK; it walks on FOUR pointed root legs. Moss and a few ferns grow on it."),
    body=("- HELMET (the headgear; a samurai kabuto of old dark wood, from about x = 612 to x = 1130, y = 65 to y = 470): a "
          "round BOWL (about x = 670-1100, y = 65-372) made of narrow vertical wooden plates with one long crack, a cushion of "
          "MOSS with a bumpy edge lying on its top left (about x = 715-885, y = 75-145); a pale bamboo BROW BAND around its "
          "lower edge; at the back a flaring NECK GUARD of three overlapping wooden tiers laced with faded cord, sweeping out "
          "and down to the left (to about x = 612, y = 250-450); at the front a short pointed VISOR that juts forward and down "
          "to the right over the brow (tip at about x = 1130, y = 420). The CREST: instead of horns, ONE living brown BRANCH "
          "like a single stag antler grows out of the front of the bowl and reaches up and to the right (from about "
          "x = 1000, y = 290 to about x = 1390, y = 10-150), forking into three twigs, each twig tipped with one small green "
          "leaf.\n"
          "- MASK (where the face would be, under the visor): a carved pale-wood war mask (a menpo) in three-quarter profile "
          "facing right: a heavy carved brow pressed low, ONE visible eye hole that is a narrow slanted slit with a small "
          "bright yellow leaf-shaped light of the spirit inside, a short carved nose, and a grim carved mouth with a row of "
          "four square wooden teeth and two short tusks. Thin vines curl out from behind the mask and around its edge; no "
          "skin, no fur anywhere.\n"
          "- NEAR SHOULDER GUARD (viewer's left, in FRONT of everything, from about x = 400 to x = 820, y = 240 to y = 680): a "
          "huge slanted rectangular shoulder shield (a samurai sode) of five or six horizontal old wooden slats, each slat its "
          "own band, laced together by two vertical rows of faded cord cross-stitches, with a pale bamboo frame along its top "
          "and bottom edges, one corner chipped; in its upper middle (centre at about x = 585, y = 400, about 165 px across) "
          "ONE big round pale bamboo EMBLEM disc bearing a single green leaf; a patch of moss on its top edge. Along its lower "
          "edge hang THREE faded brick-red cord TASSELS (at about x = 445, x = 525 and x = 620, each about 120 px long, each a "
          "separate little shape with a round knot on top).\n"
          "- FAR SHOULDER GUARD (viewer's right, BEHIND the far arm, from about x = 1108 to x = 1245, y = 290 to y = 630): the "
          "same kind of shield seen almost edge-on, narrow; ONE brick-red tassel hangs from its lower end (about "
          "x = 1194-1241, y = 541-661).\n"
          "- BODY: a thick rounded BUNDLE OF TWISTED GREEN VINES fills the armour (it shows at the neck around the mask, "
          "between the plates and at the flanks, drawn as five or six fat parallel twisting strands). On its front a rounded "
          "wooden CUIRASS of vertical slats with a bamboo rim (about x = 738-1061, y = 466-738). Around the waist a thick "
          "BRAIDED ROPE BELT of twisted dark green vine (about x = 575-905, y = 536-788), knotted at the front, with one loop "
          "of the same braid hanging over the chest at the right (about x = 888-1017, y = 397-770).\n"
          "- ARMS: the upper arms are bundles of green vines. Each forearm wears a long pale BAMBOO ARM GUARD of three or four "
          "lengthwise slats bound by two green bands: the near one lies low and almost horizontal from the elbow at about "
          "x = 560, y = 710 to the wrist at about x = 840, y = 800; the far one comes down from the elbow at about x = 1140, "
          "y = 650 to the wrist at about x = 1060, y = 800. The HANDS are made of brown ROOT: a knot of root for the palm and "
          "four thick pointed root fingers and a thumb.\n"
          "- LEGS: FOUR short pointed ROOT legs carry it like a crab or a beetle, spread under the body at about x = 500-610, "
          "x = 630-710, x = 760-835 and x = 885-990, each reaching the ground at about y = 925: each leg is one small round "
          "root knee and one curved, tapering brown root spike, each with its own outline. No feet, no toes.\n"
          "- FERN PLUME: three big green fern fronds (pointed leaves with a centre vein) fan out up and to the left from "
          "behind the near shoulder guard (about x = 400-640, y = 95-430), like the plume of a helmet.\n"
          "- MOSS CAPE: a ragged cape of hanging moss and three or four large leaves hangs down the back BEHIND the body and "
          "the swords; it shows at the lower left between the shoulder guard and the scabbards (about x = 404-560, "
          "y = 600-830) and a little behind the belly (about x = 900-975, y = 700-840)."),
    swords=dict(vo="very dark brown old wood with two pale bamboo bands near the tip and a thin green vine wound twice around it near the mouth",
                chuoi="wrapped in faded brick-red cord in a diamond pattern that shows four or five pale diamonds, with a pale bamboo cap at its end",
                tsuba="a small round pale bamboo disc shaped like a four-lobed leaf"),
    palette=("COLOURS, a calm, slightly muted palette (use exactly these, each area one flat colour): old armour wood warm "
             "grey-brown (#7A6042); the helmet darker brown (#5C4632); bamboo trim, arm guards and the emblem disc pale straw "
             "(#CFAE6B); the mask pale wood (#D6BE96); the vine body and vine arms leaf green (#46803E); lacing cord and the "
             "braided belt dark green (#2F5A3A); roots (hands, legs, the crest branch) brown (#805836); moss, fern fronds and "
             "leaves lighter green (#7CA44A); tassels and hilt wrapping faded brick red (#C85A32); the scabbards very dark "
             "brown (#463024); the light in the eye slit bright yellow (#F6D93E), flat, not glowing; every outline dark-brown "
             "ink (#2B2118). Only these colours. NO blue, NO purple, NO gold metal, NO grey steel, NO skin, NO fur."),
    check=["**Không phải con vật, không phải người**: bộ giáp gỗ cũ, bên trong là **bó dây leo lục**; mặt là **mặt nạ gỗ** nhạt chỉ một khe mắt vàng; mũ kabuto gỗ có mào là **nhánh cây** có lá, rêu trên đỉnh.",
           "**Bốn chân rễ** nhọn dưới thân; chùm **dương xỉ** ba lá sau vai gần; bàn tay bằng rễ."],
)

CHECK_CHUNG = [
    "Dáng **gù thế rút kiếm**, nhìn sang PHẢI, chỉ lộ **một mắt**; mặt quả quyết, không cười, không đáng sợ.",
    "**Tấm vai gần rất to** ở bên trái, phía trước (nan ngang, hai hàng dây buộc, huy hiệu tròn hình lá, **ba tua** treo mép dưới); tấm vai xa hẹp bên phải, một tua.",
    "**Hai kiếm đều còn trong vỏ**: kiếm dài chéo từ sau lưng (trên trái) xuống tay gần, chuôi nằm ngang sang phải, tay xa đặt lên chuôi; kiếm ngắn giắt đai, chuôi chìa trước bụng.",
    "Giáp ngực, **đai thừng bện**, bao tay, áo tơi lá sau lưng.",
    "Tô phẳng: **không** bóng, không mảng sáng tối, không điểm sáng trên giáp / vỏ kiếm; nền trắng tinh; không lưỡi kiếm trần.",
]

FIX = [
    ("Vẽ thành người / chibi dễ thương", "It is not a human and not a cute mascot: keep the hunched heavy body, the stern face and the armour; no smile."),
    ("Rút kiếm, lộ lưỡi kiếm", "Both swords stay completely inside their scabbards: remove every bare blade."),
    ("Có bóng, mảng sáng tối, giáp bóng loáng", "Flat colour only: remove every shadow, highlight, shine and gradient; keep the crayon hatching as texture only."),
    ("Lộ cả hai mắt / mặt chính diện", "The head is in three-quarter profile facing right, tucked under the headgear: only ONE eye is visible."),
    ("Bố cục khác sơ đồ", "Follow image 1 exactly for the place and size of every piece: the huge shoulder guard at the left in front, the head low at the right under the headgear, the long scabbard running from the upper left down to the near hand."),
    ("Quá sơ sài, mảnh trơn", "Add the armour detail listed: slat bands, lacing rows, the emblem disc, tassels with knots, braided belt, diamond hilt wrapping, bands on the scabbards."),
    ("Thừa chân (hướng khỉ)", "Only TWO legs: remove the extra legs."),
]


def refs(kieu):
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS character in its resting stance, "
         "built from rough coloured blobs: where every piece goes on the canvas, how big it is and which piece overlaps which "
         "(the huge slanted shoulder guard with a round emblem and three hanging tassels at the left in front; the headgear on "
         "top; the small face low at the right with one eye; the far shoulder guard at the right edge; the two arm guards and "
         "hands reaching down to the sword; the long dark scabbard running diagonally from the upper left to the hand and its "
         "hilt going right; the second sword at the belt; the legs underneath). Use it for placement, size and overlap only; "
         "design and redraw everything in the hand-drawn style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): các khối tô phẳng theo nhóm màu (tấm vai to có huy hiệu tròn và ba "
         "tua bên trái; mũ ở trên; mặt nhỏ một mắt bên phải; hai bao tay vươn xuống kiếm; vỏ kiếm dài chéo từ trên trái xuống tay; "
         "kiếm ngắn ở đai; chân bên dưới). Lấy chỗ đặt, cỡ, thứ tự chồng"),
        (NGUOI_CAY,
         "an approved hero of the same game and the same island (a hulking swamp plant brute), 1536x1024, white background: "
         "match EXACTLY its wobbly dark-brown pen line, its visible crayon hatching, its completely flat colouring, its bold "
         "chunky shapes and its fierce battle-ready attitude. Do NOT copy its species, its design or its colours.",
         "Người cây đầm lầy đã duyệt (1536 × 1024, nền trắng): quái rêu lục vai u, nắm tay gỗ. Lấy nét bút rung, vân sáp, tô phẳng, thần "
         "thái chiến"),
        (CHIM_LA,
         "another approved hero of the same island, 1536x1024, white background: the same line and flat crayon colouring; see "
         "how its leaves are drawn. Do NOT copy its species, design or colours.",
         "Chim lá đã duyệt (1536 × 1024, nền trắng). Lấy nét, tô phẳng, cách vẽ lá"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp"),
    ]


def main(chon=None):
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    gd = [f"# Gói gửi GPT: `{CODE}` dạng {K} (kiếm sĩ rừng mặc giáp, tướng thứ 8 đảo Mộc, tên chưa đặt)", "",
          "Làm 2026-11-12: dựng trên rig của con gốc `monster_3620` (bọ hung samurai hai kiếm; gần như mọi mảnh cứng); loài, mũ, màu, chi "
          "tiết là đề xuất của Claude, chờ người dùng chọn hướng và duyệt concept. Ghi chú: `ArtGen/Spine/inbox/kiem_si_ghichu.md`.", "",
          "Lượt 2 (mảnh) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    ra = []
    for kieu, d in D.items():
        R = refs(kieu)
        missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
        if missing:
            raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
        out = os.path.join(save_dir(), f"L1_{kieu}.png")
        p = os.path.join(pk(), f"luot_1_concept_{kieu}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "",
              "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
              "approved hero images.", "",
              d["intro"], "", STANCE, "",
              "Follow the LAYOUT GUIDE (image 1) for WHERE every piece is on the canvas, HOW BIG it is and WHICH piece overlaps "
              "which. Coordinates below are pixels on the 1536x1024 canvas (x from the left, y from the top). The viewer's LEFT "
              "side of the picture is the character's back and NEAR shoulder; the viewer's RIGHT is where it faces.", "",
              d["body"], SWORDS.format(**d["swords"]), "",
              d["palette"], "", FRAME.format(top=d["top"]), "", POSE.format(duoi=d["duoi"]), "", SOFT, LINE, FLAT, BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd += [f"## Hướng `{kieu}`: {d['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{K}/luot_1_concept_{kieu}.txt` (thêm "
               "`--note \"...\"` để sửa nhanh).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += ["", "Kiểm riêng hướng này:", ""] + [f"- {c}" for c in d["check"]] + [""]
    gd += ["Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/kiem_si.py bo_cuc`).",
           "", "## Kiểm chung", ""]
    gd += [f"- {c}" for c in CHECK_CHUNG]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    open(os.path.join(pk(), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 2: mảnh từ concept đã duyệt (người dùng chọn B = khi_mu, 2026-11-12)
# Gần như mọi mảnh của rig là mảnh CỨNG một xương: sáu tờ "đúng chỗ, đúng cỡ" (mỗi tờ giữ vài mảnh KHÔNG chồng nhau, vẽ đủ phần khuất)
# + hai tờ mảnh rời (kiếm; tua, lá mào, bắp tay, đùi).
CON = ("a LANGUR WARLORD in samurai armour, hunched in a quick-draw stance facing right: charcoal fur, a white whisker ruff around a "
       "tan face with one amber eye, a dark-green helmet with a bamboo brow band, a tiered neck guard and two big leaf crests, a huge "
       "moss-green shoulder guard with amber cross lacing, a round leaf emblem and three amber tassels, a narrow far shoulder guard, "
       "a green cuirass, a braided amber rope belt, bamboo arm guards and shin guards, a brown cloth skirt, a cape of dark leaves, a "
       "long curled tail with a white tuft, and two sheathed swords")
KEEP_TASK = ("TASK: redraw image 1, but keep ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME "
             "SIZE as in image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE "
             "everything else and leave pure white (#FFFFFF) there. Every kept part must be ONE COMPLETE CLOSED SHAPE with the "
             "dark-brown ink outline running all the way around it: where a part is hidden behind another part in image 1, DRAW the "
             "hidden portion as described. The kept parts must NOT touch each other: clear white between them. Same wobbly ink line, "
             "same line thickness, same colours, same crayon hatching, same completely flat colouring as image 1. Do not add "
             "anything: no shadows, no glow, no dust, no labels. Coordinates are pixels on the 1536x1024 canvas (x from the left, y "
             "from the top).")
FLAT3 = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do not "
         "model light. No shading, no darker side, no lighter patches, no shadows of any kind, no white highlights or shine spots "
         "(except the one tiny light dot in the eye), no gloss, no glow, no gradients, no 3D look.\n"
         "Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
         "outline around the shapes. No text, no labels, no numbers, no frame, no guide lines.")
TO = {
    "A": ("tấm vai gần, tấm vai xa, bao tay xa, hai giáp ống chân", [
        "THE NEAR SHOULDER GUARD (the huge one at the left; about x = 350 to x = 765, y = 265 to y = 605): the big moss-green "
        "lacquered shield with its bamboo roll along the top, its horizontal green plates, its two rows of amber cross lacing, the "
        "round bamboo emblem disc with the green leaf, and its bamboo rim along the bottom. WITHOUT the three tassels (where their "
        "knots overlap the bottom rim in image 1, draw the plain bamboo rim), WITHOUT the tail, the helmet and the scabbard. It is "
        "already almost completely visible: just close its outline all round.",
        "THE FAR SHOULDER GUARD (the narrow one at the right; about x = 1085 to x = 1235, y = 290 to y = 585): the narrow shield of "
        "green plates with amber lacing, its round bamboo knob on top and its bamboo rim at the bottom, WITHOUT its tassel. Where its "
        "left edge is hidden behind the fur in image 1, complete it: a narrow closed shape whose left edge runs at about x = 1085.",
        "THE FAR FOREARM GUARD (at the right; about x = 1015 to x = 1175, y = 660 to y = 850): the bamboo arm guard of lengthwise "
        "slats with its two green bands, WITHOUT the hand below it and WITHOUT the fur above it. Its upper end (the elbow, at about "
        "(1100, 668)) is closed with the rounded bamboo rim; its lower end (the wrist, at about (1075, 848)) is closed, rounded.",
        "THE REAR SHIN GUARD (the left leg; about x = 428 to x = 548, y = 848 to y = 958): the bamboo shin guard with its green band, "
        "WITHOUT the foot below it and WITHOUT the fur and leaves above it. Its top (hidden in image 1) is a closed, rounded bamboo "
        "rim at about y = 848; its bottom is closed at about y = 958.",
        "THE FRONT SHIN GUARD (the right leg; about x = 860 to x = 968, y = 878 to y = 962): the same for the right leg: bamboo shin "
        "guard with its green band, closed rounded top at about y = 878, closed bottom at about y = 962, WITHOUT the foot.",
    ]),
    "B": ("mũ (không mào lá), bao tay gần, hai bàn chân", [
        "THE HELMET ALONE (about x = 555 to x = 1105, y = 55 to y = 435): the dark-green bowl with its vertical plate lines, amber "
        "rivets and the bamboo knob on top, the bamboo brow band, the pointed visor jutting to the right, and the three-tier neck "
        "guard with amber lacing sweeping down to the left. WITHOUT the two crest leaves (draw the plain bowl and the plain brow "
        "band where they are attached), WITHOUT the head, the face and the white ruff, WITHOUT the shoulder guard and the tail. "
        "Complete it into ONE closed helmet shape: where the near shoulder guard covers the lower left of the neck guard in image 1, "
        "draw the three tiers complete (the lowest tier ends at about x = 555-600, y = 345); the underside of the visor and of the "
        "bowl (where the head was) is closed with one firm ink line running from the back of the neck guard at about (700, 345) to "
        "the visor tip at about (1100, 388).",
        "THE NEAR FOREARM GUARD (low, at the left of the hands; about x = 585 to x = 875, y = 710 to y = 910): the big bamboo arm "
        "guard of lengthwise slats with its two green bands and the frayed straw fringe at its elbow end (left), WITHOUT the hand, "
        "WITHOUT the rope ends and the tassel that hang over it, WITHOUT fur. Complete its upper edge where the rope ends cover it; "
        "its wrist end (right, at about x = 860) is closed, rounded.",
        "THE REAR FOOT (the left one; about x = 392 to x = 572, y = 925 to y = 1012): the tan monkey foot with its toes, WITHOUT the "
        "shin guard. Its top (the ankle, at about (490, 932)) is closed with a rounded tan lump.",
        "THE FRONT FOOT (the right one; about x = 862 to x = 1045, y = 945 to y = 1012): the same for the right foot, toes pointing "
        "right; closed rounded ankle lump on top at about (915, 950).",
    ]),
    "C": ("đầu (không mũ), áo tơi lá, hai bàn tay", [
        "THE HEAD ALONE (about x = 750 to x = 1095, y = 320 to y = 605): the langur head: the tan face with its heavy brow, the one "
        "amber eye, the flat muzzle, the downturned mouth with the small fang, the whole white whisker ruff and beard around the "
        "face, the charcoal fur behind it, and the green chin cord with its bow under the chin. WITHOUT the helmet: where the helmet "
        "covers the top of the head in image 1, draw the rounded skull covered in short charcoal fur (top of the skull at about "
        "y = 322) and the tan forehead above the brow; WITHOUT the cuirass, the rope and the shoulder guards: where they cover the "
        "lower tips of the ruff, draw the white ruff tips complete (down to about y = 605). ONE closed head shape.",
        "THE LEAF CAPE ALONE (about x = 245 to x = 700, y = 560 to y = 985): the rain cape of big dark-green leaves. WITHOUT the two "
        "scabbards, the tassels, the shoulder guard, the fur body and the leg. Complete it into ONE closed fan of five or six big "
        "overlapping pointed leaves (each with its centre vein and side veins) hanging down and to the left from a gathered top at "
        "about (610, 575): where the scabbards, the tassels and the body cover it in image 1, draw the leaves continuing.",
        "THE NEAR HAND (about x = 795 to x = 885, y = 785 to y = 905): the tan fist with its curled fingers and thumb, WITHOUT the "
        "scabbard it holds (draw the fingers closed onto the palm: a closed fist) and WITHOUT the arm guard. Its wrist end (upper "
        "left) is closed, rounded.",
        "THE FAR HAND (about x = 980 to x = 1110, y = 815 to y = 910): the tan fist with four fingers and thumb, WITHOUT the sword "
        "hilt it holds (a closed fist) and WITHOUT the arm guard. Its wrist end (top) is closed, rounded.",
    ]),
    "D": ("thân lông, đuôi", [
        "THE BODY ALONE (about x = 615 to x = 1115, y = 470 to y = 905): the charcoal-furred torso WITHOUT any armour, WITHOUT the "
        "rope, the swords, the arms, the shoulder guards, the head, the skirt, the legs and the cape. Draw it as ONE closed, broad, "
        "rounded barrel of charcoal fur leaning forward to the right, with shaggy fur tufts along its outline and a few short fur "
        "ticks inside: a rounded top (shoulders and neck stump) at about y = 470, a rounded bottom at about y = 905.",
        "THE TAIL ALONE (about x = 365 to x = 625, y = 35 to y = 470): the long charcoal tail with its curled end and the white tuft "
        "exactly as in image 1. Where the shoulder guard hides its lower part, continue the tail at the same thickness (about 50 "
        "px) straight down to a rounded, closed end at about (500, 465).",
    ]),
    "E": ("giáp ngực, váy vải", [
        "THE CUIRASS ALONE (about x = 695 to x = 1025, y = 535 to y = 735): the green lacquered chest armour with its bamboo collar "
        "rim on top, its green plates with the amber rivet dots, and its bamboo rims. WITHOUT the rope belt, the short sword, the "
        "chin cord bow, the ruff and the fur. Complete it into ONE closed rounded breastplate: where the rope, the sword hilt and "
        "the ruff cover it in image 1, draw the green plates continuing; its bottom edge is a closed curve at about y = 735.",
        "THE CLOTH SKIRT ALONE (about x = 585 to x = 855, y = 790 to y = 950): the short skirt of dark-brown cloth strips. WITHOUT "
        "the arm guard, the scabbard, the hand and the fur. Complete it into ONE closed band of five or six hanging rectangular "
        "cloth strips side by side (bottoms at about y = 945, slightly uneven), its top edge one straight closed line at about "
        "y = 792.",
    ]),
    "F": ("đai thừng bện", [
        "THE ROPE BELT ALONE (about x = 660 to x = 1045, y = 555 to y = 800): the thick braided amber rope exactly as in image 1: "
        "the band across the waist from about (665, 640) at the left to about (1040, 655) at the right, the big knot at about "
        "(810, 690) with its two short hanging rope ends (frayed tips at about y = 800), and the loop that rises at the right end up "
        "to about (1030, 560). WITHOUT the cuirass, the short sword, the fur and the arm guard. Complete it into ONE closed rope "
        "shape: where the short sword's guard and hilt cross it in image 1, draw the braided rope continuing.",
    ]),
}


def main_manh():
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    if not os.path.exists(duyet):
        raise SystemExit("chưa có concept duyệt " + Wp(duyet))
    ra = []
    gd = ["", "## Lượt 2: mảnh (hướng B `khi_mu` đã duyệt 2026-11-12)", "",
          f"Ảnh mẫu 1 của mọi tờ: `{Wp(duyet)}` (concept đã duyệt, 1536 × 1024, nền trắng: voọc tướng quân lông than, ria trắng, mũ kabuto "
          "lục có hai lá mào, tấm vai lục to có huy hiệu lá và ba tua hổ phách, đai thừng bện, hai kiếm trong vỏ, áo tơi lá, đuôi cuộn "
          "chóp trắng). Mỗi tờ một file prompt; **chỉ gửi GPT đường dẫn file prompt**. Claude tự gen bằng `py -3 -I ArtGen/Spine/gen.py "
          "<file prompt>` rồi cắt bằng `py -3 -I ArtGen/Spine/kiem_si_manh.py lam`.", "",
          "| Tờ | File prompt | Giữ lại / vẽ gì | Ảnh lưu vào |", "|---|---|---|---|"]

    def dau(out, ten, them=""):
        return ["IMAGES (attached in this order; open each from its path):",
                f"image 1 = {Wp(duyet)}: the APPROVED picture of the creature, 1536x1024, white background: {CON}.{them}",
                "", f"SAVE: save it as a PNG to {Wp(out)}",
                f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                "delete any other file.", ""]

    for ma, (vi, ds) in TO.items():
        out = os.path.join(save_dir(), f"M_{ma}.png")
        p = os.path.join(pk(), f"luot_2_manh_{ma}.txt")
        t = dau(out, f"M_{ma}") + [KEEP_TASK, "", "KEEP:"]
        t += [f"{i}. {d}" for i, d in enumerate(ds, 1)]
        t += ["", FLAT3]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd.append(f"| `{ma}` | `{Wp(p)}` | đúng chỗ, đúng cỡ: {vi} ({len(ds)} mảnh, vẽ đủ phần khuất) | `{Wp(out)}` |")
    SHEET = ("landscape 1536x1024, pure-white background, each part drawn exactly in the style of image 1 (same ink line thickness as "
             "in image 1, about 6 px; same colours; same crayon hatching; flat colour). Every part is ONE COMPLETE CLOSED SHAPE with "
             "its own ink outline all the way round; the parts do NOT touch or overlap: at least 40 px of clear white between them. No "
             "creature, no body, no hands, nothing else on the sheet.")
    # tờ S1: hai thanh kiếm tháo rời
    out = os.path.join(save_dir(), "M_S1.png")
    p = os.path.join(pk(), "luot_2_manh_S1.txt")
    t = dau(out, "M_S1", " It gives the design, the colours, the ink line and the exact look of the two swords: dark-brown lacquered "
            "scabbards with pale bamboo bands, flower-shaped pale bamboo guards, hilts wrapped in amber cord with dark diamonds and a "
            "bamboo end cap.")
    t += ["TASK: draw a PARTS SHEET with the creature's TWO SWORDS taken apart, for a 2D animation rig: " + SHEET + " SIX parts in "
          "five rows. Every part lies HORIZONTAL: tips and closed ends to the LEFT, the hand end to the RIGHT. The swords are "
          "Japanese katana: very slightly curved (the back of the curve up), not straight sticks.", "",
          "ROW 1 (centre line at about y = 120): 1. THE LONG SCABBARD, empty: about 800 px long (from about x = 120 to x = 920) and "
          "about 58 px thick: dark-brown lacquered wood; its LEFT end is the closed, rounded tip with a pale bamboo cap and two pale "
          "bamboo bands near it (as on the scabbard at the upper left of image 1); one pale bamboo band about one third from the "
          "right; its RIGHT end is the open mouth, cut straight, with a pale bamboo ring.",
          "ROW 2 (centre line at about y = 300): 2. THE LONG BLADE, bare: about 740 px long (from about x = 150 to x = 890) and about "
          "40 px wide, with the same gentle curve as the scabbard: a single-edged katana blade, pointed tip at the LEFT; flat pale "
          "steel colour (#D9DED6) with ONE thin darker line running along its length (the ridge) and a thin wavy line near the "
          "cutting edge; at its RIGHT end a short pale bamboo-yellow collar (about 30 px long). No shine, no highlight, no glow.",
          "ROW 3 (centre line at about y = 480): 3. THE LONG HILT WITH ITS GUARD: about 350 px long in all (from about x = 400 to "
          "x = 750): at its LEFT end the guard, a pale bamboo-yellow flower-shaped disc seen at a slight angle (about 66 px wide and "
          "104 px tall, as in image 1); then the grip running to the right, about 58 px thick, wrapped in amber cord with a row of "
          "five dark-brown diamonds; a pale bamboo end cap at the far RIGHT.",
          "ROW 4 (centre line at about y = 660): 4. THE SHORT SCABBARD, empty: about 570 px long (from about x = 200 to x = 770) and "
          "about 54 px thick: the same dark-brown lacquer, closed rounded tip at the LEFT, one pale bamboo band near the tip and one "
          "in the middle, open mouth with a pale bamboo ring at the RIGHT.",
          "ROW 5 (centre line at about y = 860), two parts side by side: 5. THE SHORT BLADE, bare (from about x = 120 to x = 620: "
          "about 500 px long, about 36 px wide): like the long blade, pointed tip at the LEFT, pale steel (#D9DED6), one thin ridge "
          "line, a short bamboo-yellow collar at its RIGHT end. 6. THE SHORT HILT WITH ITS GUARD (from about x = 760 to x = 980: about "
          "220 px long): a smaller flower-shaped pale bamboo guard at its LEFT end (about 56 px wide, 86 px tall), a grip about 50 px "
          "thick wrapped in amber cord with three dark diamonds, a pale bamboo end cap at the RIGHT.", "", FLAT3]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    ra.append(p)
    gd.append(f"| `S1` | `{Wp(p)}` | tờ mảnh rời, năm hàng, mọi thứ nằm ngang mũi bên trái: vỏ kiếm dài (~800 px), lưỡi kiếm dài, chuôi dài + "
              f"kiếm cách hình hoa; vỏ kiếm ngắn (~570 px); lưỡi kiếm ngắn và chuôi ngắn (6 mảnh) | `{Wp(out)}` |")
    # tờ S2: tua, lá mào, bắp tay, đùi
    out = os.path.join(save_dir(), "M_S2.png")
    p = os.path.join(pk(), "luot_2_manh_S2.txt")
    t = dau(out, "M_S2", " It gives the design, the colours, the ink line and the exact look of the amber tassels, the two green "
            "crest leaves of the helmet and the shaggy charcoal fur.")
    t += ["TASK: draw a PARTS SHEET of loose parts of the creature of image 1, for a 2D animation rig: " + SHEET + " EIGHT parts in "
          "two rows.", "",
          "ROW 1 (tops at about y = 50, bottoms at about y = 480), from left to right, FOUR parts:",
          "1. A TASSEL, exactly like the amber tassels hanging from the shoulder guard in image 1 (centre at about x = 110; about "
          "80 px wide and 135 px tall, its top at y = 60): a round amber knot on top, a short neck ring, and a flaring skirt of amber "
          "threads with four or five thin dark lines; hanging straight down.",
          "2. A SECOND TASSEL of the same kind, very slightly different (centre at about x = 260; same size, top at y = 60).",
          "3. THE BIG CREST LEAF (centre at about x = 560): the big fresh-green leaf of the helmet crest of image 1, drawn UPRIGHT: "
          "its base (a short blunt stalk) at the BOTTOM at about (560, 480), its pointed tip at the TOP at about (560, 55); about "
          "190 px wide at its widest; gently curved like a blade; slightly wavy edge; ONE dark-green centre vein and six or seven "
          "side veins, as in image 1.",
          "4. THE SMALL CREST LEAF (centre at about x = 900): the smaller leaf of the crest, UPRIGHT, base at the bottom at about "
          "(900, 480), tip at the top at about (900, 170); about 125 px wide; one centre vein and four or five side veins.",
          "",
          "ROW 2 (tops at about y = 560, bottoms at about y = 990), from left to right, FOUR parts, all of shaggy charcoal fur exactly "
          "like the fur of the creature's arms in image 1 (flat charcoal, a jagged outline of short fur tufts, a few short fur ticks "
          "inside; no hand, no armour):",
          "5. THE NEAR UPPER ARM (centre at about x = 170): a very thick, slightly bent, furry arm segment standing UPRIGHT: about "
          "150 px thick and 380 px long (from y = 580 to y = 960), both ends rounded.",
          "6. THE FAR UPPER ARM (centre at about x = 470): the same kind, about 125 px thick and 270 px long (from y = 580 to "
          "y = 850), both ends rounded.",
          "7. A THIGH (centre at about x = 760): a short, fat furry leg segment, UPRIGHT, about 120 px thick and 170 px long (from "
          "y = 580 to y = 750), both ends rounded.",
          "8. A SECOND THIGH of the same kind (centre at about x = 1000; about 115 px thick and 160 px long, from y = 580 to "
          "y = 740).", "", FLAT3]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    ra.append(p)
    gd.append(f"| `S2` | `{Wp(p)}` | tờ mảnh rời hai hàng: 2 tua, lá mào to, lá mào nhỏ (dựng đứng, cuống ở dưới); bắp tay gần, bắp tay xa, 2 "
              f"đùi lông than (8 mảnh) | `{Wp(out)}` |")
    gd += ["", "Kiểm từng tờ: tờ A..F các mảnh nằm ĐÚNG chỗ, đúng cỡ như concept (Claude chồng lên concept để đo), mỗi mảnh kín viền, không "
           "chạm nhau, nền trắng tinh; tờ S1 đủ 6 mảnh kiếm nằm ngang, lưỡi kiếm tô phẳng không bóng; tờ S2 đủ 8 mảnh rời.", "",
           "Gửi thêm khi GPT vẽ sai: `Keep every kept part exactly where it is and at the size it has in image 1.` · `The kept parts must "
           "not touch: leave clear white between them.` · `Each part needs its own closed ink outline.` · `Flat colour only: remove every "
           "shadow, highlight and gradient.`"]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2: mảnh")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 4: bàn tay HAI MẢNH kẹp thanh kiếm (người dùng 2026-11-12: "phần bàn
# tay không ôm vào kiếm, bạn xem con gốc nó làm thế nào sửa lại đi"). Con gốc: lòng bàn tay nằm SAU kiếm, các ngón dài vắt NGANG QUA cả
# thân kiếm ở phía TRƯỚC, đầu ngón thò sang bên kia. Nắm tay một cục liền (tờ M_C) đặt kiểu gì cũng chỉ như đè lên kiếm.
def main_tay():
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    out = os.path.join(save_dir(), "M_T.png")
    p = os.path.join(pk(), "luot_4_ban_tay.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(duyet)}: the APPROVED picture of the creature, 1536x1024, white background: {CON}. It gives the wobbly "
         "dark-brown ink line and its thickness, the crayon hatching, and the exact tan skin colour and chunky look of its bare monkey "
         "hands.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as M_T_2.png, M_T_3.png ... in the same folder. Do not edit, move or delete any "
         "other file.", "",
         "TASK: draw a PARTS SHEET of the creature's HAND taken apart into TWO LAYERS, for a 2D animation rig in which the hand grips "
         "a sword: the sword will be placed BETWEEN the two layers (the palm behind it, the fingers in front of it, crossing over it). "
         "Landscape 1536x1024, pure-white background, FOUR separate parts in one row, each drawn in exactly the style of image 1 (ink "
         "line about 8 px on this sheet because the parts are drawn big; the same flat tan skin colour as the hands in image 1; crayon "
         "hatching). Every part is ONE COMPLETE CLOSED SHAPE with its own ink outline all the way round; the parts do NOT touch: at "
         "least 60 px of clear white between them. NO sword, NO bar, NO arm, NO armour, nothing else on the sheet.", "",
         "1. FINGERS, version A (centre at about x = 220, y = 512; about 300 px wide and 420 px tall): ONLY the four fingers of a "
         "monkey hand that is clenched around a horizontal bar, seen from the front: FOUR fat fingers side by side, each running "
         "VERTICALLY from its knuckle at the TOP to its rounded fingertip at the BOTTOM, each about 70 px wide and about 400 px long, "
         "slightly curved like a hook, the four fingertips ending at slightly different heights. The four fingers are joined into one "
         "shape: thin ink lines separate neighbouring fingers; along the top the four knuckles make a gently bumpy edge, closed with "
         "ink. One short crease line across each finger about one third from the top. No palm, no thumb, no nails.",
         "2. FINGERS, version B (centre at about x = 600, y = 512; about 280 px wide and 340 px tall): the same kind of part with "
         "shorter, chunkier fingers (about 320 px long), slightly different from version A.",
         "3. PALM, version A (centre at about x = 990, y = 512; about 300 px wide and 300 px tall): the REST of the hand without the "
         "four fingers: the rounded back of the hand as one chunky rounded block, with the THUMB folded along its lower right side "
         "(one fat thumb with a rounded tip, separated by an ink line). Its top edge (the wrist side) is closed and rounded. No "
         "fingers.",
         "4. PALM, version B (centre at about x = 1350, y = 512; about 270 px wide and 280 px tall): the same kind of part, the thumb "
         "folded along its lower LEFT side instead.", "", FLAT3]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 4: bàn tay")[0].rstrip("\n")
    gd = ["", "## Lượt 4: bàn tay hai mảnh kẹp kiếm (2026-11-12)", "",
          f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(duyet)}` | Concept đã duyệt (1536 × 1024, nền trắng): voọc tướng quân; lấy nét, màu da bàn tay |", "",
          "Tờ ra bốn mảnh rời một hàng, vẽ to: hai bản BỐN NGÓN TAY (dọc, khớp ở trên, đầu ngón ở dưới, không lòng bàn tay) và hai bản LÒNG "
          "BÀN TAY có ngón cái (không có bốn ngón). Kiểm: không có kiếm, không có cánh tay; mỗi mảnh kín viền, không chạm nhau."]
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    print(p)


if __name__ == "__main__":
    if sys.argv[1:2] == ["tay"]:
        main_tay()
    elif sys.argv[1:2] == ["manh"]:
        main_manh()
    else:
        main()
