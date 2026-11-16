# -*- coding: utf-8 -*-
"""Kỵ sĩ cổ đại bị nguyền (ky_nguyen): mô tả con gốc monster_3642 từng mảnh và ba hướng concept lượt 1 (Claude đề xuất, chờ người dùng
chọn). Dùng trong ky_nguyen_da.py (prompt_concept)."""

MO_TA_CON = (
    "PIECE BY PIECE (as in image 1: an armoured KNIGHT WITH NO LEGS, FLOATING, seen in three-quarter view turned to the RIGHT, hunched and "
    "leaning forward; the knight is HOLLOW: there is no body inside the armour, only a dark void; its lower body is a long torn cape "
    "hanging down): "
    "HELMET (upper middle-right): a closed helmet turned to the right with a narrow dark eye slit on its front; on top of it a CREST of "
    "five swept-back pieces fanning up and to the right (in image 1 pale feathers on a gold scroll ornament). "
    "VOID BODY: between the armour pieces only the hollow void shows: the torso behind the chest plate, a band under the big shoulder, the "
    "upper arm under the big shoulder on the left, the upper arm reaching to the right; and a few small wisps rising behind the neck, just "
    "left of the helmet. "
    "BIG SHOULDER (left, the near side): a huge pauldron of several overlapping curved plates covering the near shoulder, with flanges "
    "rising behind it. "
    "CHEST PLATE (middle-right): a breastplate turned to the right, its lower edge pointed; a small plate at its lower left. "
    "TABARD: a long narrow cloth strip hanging from the right side of the chest down to the right. "
    "NEAR ARM (left): from under the big shoulder a big armoured forearm (a long vambrace with a mark on it) bends down; its armoured fist "
    "at the lower left holds the SWORD by the grip. "
    "SWORD: the pommel and grip stick out on the left of the fist, a big crossguard with a round gem in its middle sits just right of "
    "the fist, and a wide straight blade goes down to the lower right to the bottom of the picture, its tip broken and notched. "
    "FAR ARM (right): a void upper arm reaching to the right from behind the chest, a banded bracer on the forearm, and an open clawed "
    "hand with five fingers on the far right, reaching forward, palm towards the viewer. "
    "SPIKES: pointed shards stick out of the armour: a TALL one rising from the big shoulder up to the top left (with two tiny ones beside "
    "it), one from the front of the big shoulder pointing down-left, one at the near elbow pointing left, two on the near forearm, a long "
    "one from the right side of the chest pointing right, a small one under the chest, and a few small ones near the far bracer. "
    "CAPE: a big torn cape from behind the shoulders, hanging down to the bottom left, its lower edge torn into ragged strips; it also "
    "shows between the near arm and the chest, down to the bottom. "
    "FLOATING DEBRIS: five small pieces floating under the chest (in image 1 dark stones).")

# Mỗi hướng: (tên Việt, mô tả Việt, các dòng CHANGE tiếng Anh)
_SAT = ("ARMOUR: BLACKENED IRON, very old and RUSTY: flat dark iron #3A3C44 on the faces turned to the viewer, darker iron #26272D on the "
        "faces turned away, and flat RUST patches #A4532B (2 or 3 simple rounded patches on each big plate, a little rust along some "
        "edges). No white, no gold, no purple anywhere on the armour.")
_LUA = ("GREEN SOUL FIRE (the curse that keeps this knight alive): drawn as flat flame shapes with the same ink outline, in TWO flat tones "
        "only: bright soul green #8FEA5E outside and pale green #D6FFA8 for one simple inner tongue; like the flames of image 3 but green. "
        "No glow, no halo, no light rays, no gradient.")
_MAT = ("EYES: two narrow eyes in the eye slit, flat bright green #B6FF7A inside their ink outline with one small white dot each, slanted "
        "and determined (no glow).")

HUONG = {
    "A": ("lửa linh hồn trong giáp",
          "giáp sắt đen rỉ sét; KHOẢNG RỖNG bên trong (thân, dải dưới vai, hai bắp tay, mấy sợi sau gáy) thành LỬA LINH HỒN XANH LÁ tô phẳng; "
          "mũ ĐỔI DÁNG: mũ thùng đỉnh phẳng, khe mắt hình chữ thập; chùm lông vũ thành CHÙM LỬA XANH vuốt ra sau; gai tinh thể thành GAI "
          "SẮT rỉ hình nón; giáp vai ba tấm chồng, mép răng cưa; giáp ngực có VẾT NỨT lộ lửa xanh; kiếm GÃY lưỡi, chắn thẳng có ngọc xanh; "
          "áo choàng đen than rách, mép rách cháy thành lưỡi lửa xanh; đá bay thành mảnh giáp vụn rỉ",
          [_SAT, _LUA, _MAT,
           "VOID BODY: everything that was the dark void in image 1 (the torso behind the chest plate, the band under the big shoulder, "
           "both upper arms) is now FILLED WITH GREEN SOUL FIRE, flat bright green with a few pale green flame tongues pointing upward. "
           "The small wisps behind the neck become small GREEN FLAME TONGUES.",
           "HELMET: a NEW SHAPE: a squat BUCKET-shaped great helm with a flat top and a CROSS-shaped eye slit (a horizontal slit crossed by "
           "a short vertical slit); inside the slit only green fire and the two green eyes. No gold scroll ornament: instead one low rusty "
           "iron ridge along the top.",
           "CREST: the five feathers become a CREST OF GREEN SOUL FIRE streaming back from the top of the helm: five flame tongues in the "
           "same places and directions as the five feathers, sweeping up and to the right.",
           "SPIKES: every crystal shard becomes a RUSTY IRON SPIKE: a straight sharp cone of dark iron with a rust-coloured tip, same place, "
           "same length and direction; the few small floating shards near the far bracer become small iron splinters.",
           "BIG SHOULDER: a NEW SHAPE: THREE stacked overlapping iron plates, each with a jagged SAW-TOOTH lower rim (no leaf-shaped "
           "flanges), the tall spike rising from the top plate.",
           "CHEST PLATE: plain blackened iron breastplate (no emblem) with ONE jagged CRACK running down its middle; through the crack "
           "green soul fire shows.",
           "TABARD: torn charcoal-grey cloth #4A4A50 with ONE faded rust-red ring sigil, ragged lower end.",
           "NEAR ARM: black iron vambrace with ONE simple green zigzag rune (flat green) instead of the mark; black iron gauntlet fist and "
           "fingers.",
           "FAR ARM: rusty iron bands on the bracer; the hand a black iron CLAWED GAUNTLET with pointed fingertips.",
           "SWORD: a NEW SHAPE: an ancient heavy black-iron greatsword whose blade is BROKEN OFF about two thirds along (a jagged broken "
           "end at the lower right instead of a tip), a few notches on its edges, rust patches; the crossguard a heavy straight iron bar "
           "with downturned ends and ONE round green soul gem in its middle; grip wrapped in dark leather; round iron pommel.",
           "CAPE: charcoal-black torn cape #2E2E33, its ragged lower strips ending in small green flame tongues (inside the same outline).",
           "FLOATING DEBRIS: the five stones become small broken pieces of rusty armour plate (flat dark iron with a rust edge)."]),
    "B": ("hồn ma bóng tối, lửa rỉ ra khe giáp",
          "giáp sắt đen rỉ, viền đồng xỉn cổ; khoảng rỗng giữ ĐEN XANH THẪM, lưỡi lửa xanh liếm ra ở mép; gai tinh thể thành LƯỠI LỬA XANH phụt "
          "ra từ khe giáp; mũ ĐỔI DÁNG: hai SỪNG cong vuốt ra sau, khe mắt ngang; chùm lông vũ thành bờm lửa ma xanh dài; giáp vai tròn có "
          "ba vây lưỡi cong; giáp ngực có lỗ tròn giữa lộ lõi lửa; kiếm gãy, chắn hai cánh cụp; áo choàng xanh rêu thẫm rách; đá bay đen nứt "
          "vân xanh",
          [_SAT.replace("No white, no gold, no purple anywhere on the armour.",
                        "A thin dull dark-bronze trim #7A6440 only along the rims of the big plates (old tarnished, flat). No white, no "
                        "purple."), _LUA, _MAT,
           "VOID BODY: the void stays a very dark green-black #1D2622 (flat), and along its edges, where it meets the armour, small GREEN "
           "FLAME TONGUES lick outward. The small wisps behind the neck become GREEN FLAME TONGUES.",
           "HELMET: a NEW SHAPE: a rounded close helm with TWO HORNS curving up and back from its top sides (dark iron, rust at the tips), "
           "a single narrow HORIZONTAL eye slit with the two green eyes. No gold scroll ornament.",
           "CREST: the five feathers become a long ragged MANE OF GREEN GHOST FIRE streaming back behind the horns, five flame tongues in the "
           "same places and directions as the feathers.",
           "SPIKES: every crystal shard becomes a pointed TONGUE OF GREEN SOUL FIRE bursting out of a gap in the armour, same place, same "
           "length and direction (straight and pointed like the shards, flame-edged).",
           "BIG SHOULDER: a NEW SHAPE: one big rounded pauldron with THREE long backward-curving blade FINS rising from its top (instead of "
           "leaf-shaped flanges), the tall green flame bursting out beside them.",
           "CHEST PLATE: blackened iron breastplate with a ROUND HOLE in its middle; inside the hole a round core of green soul fire.",
           "TABARD: a torn strip of very dark moss-green cloth #2F4436 with a dull bronze border, ragged lower end.",
           "NEAR ARM: black iron vambrace with a dull bronze band and ONE green rune (a simple downward chevron); black iron fist.",
           "FAR ARM: rusty iron bracer with a bronze band; the hand a black iron clawed gauntlet.",
           "SWORD: a NEW SHAPE: an ancient black-iron greatsword BROKEN OFF about two thirds along (jagged broken end), notched edges, rust; "
           "the crossguard two short WINGS swept downward (flat dark bronze) round ONE green soul gem; dark grip; pommel a small iron ring.",
           "CAPE: very dark moss-green torn cape #26372D with ragged strips.",
           "FLOATING DEBRIS: five small black rocks with one thin green crack line each."]),
    "C": ("vua chiến trận cổ, vết thương trận xưa",
          "giáp sắt đen RỈ NẶNG (mảng rỉ cam nâu nhiều hơn), còn vệt viền vàng xỉn; khoảng rỗng đen, lửa xanh ở mép; mũ ĐỔI DÁNG: VƯƠNG MIỆN "
          "gai năm mũi liền mũ, khe mắt dọc; chùm lông vũ thành ngọn lửa xanh bốc lên từ trong vương miện; gai tinh thể thành MŨI TÊN GÃY + "
          "mũi giáo gãy cắm trên giáp (vết trận xưa); giáp vai tròn vạt gãy; giáp ngực có vết chém lộ lửa; kiếm cổ gãy, chắn vòng; áo choàng "
          "đỏ rượu sẫm phai, viền vàng sờn; đá bay thành đầu tên + mảnh khiên vỡ",
          [_SAT.replace("2 or 3 simple rounded patches", "3 or 4 bigger rounded patches").replace(
              "No white, no gold, no purple anywhere on the armour.",
              "A few remains of a thin worn GOLD trim #B08A3E along the rims (broken in places). No white, no purple."), _LUA, _MAT,
           "VOID BODY: the void stays near-black #1F2321 (flat) with a few small green flame tongues along its upper edges. The small wisps "
           "behind the neck become GREEN FLAME TONGUES.",
           "HELMET: a NEW SHAPE: a tall helm with a jagged iron CROWN of five short points fused round its top rim, and a single VERTICAL "
           "eye slit widening at the eyes (two green eyes in it). No gold scroll ornament.",
           "CREST: the five feathers become GREEN SOUL FIRE rising up out of the open top of the crown, five flame tongues in the same "
           "places and directions as the feathers.",
           "SPIKES: the crystal shards become the WOUNDS OF AN ANCIENT BATTLE stuck in the armour, same places, lengths and directions: the "
           "tall one on the big shoulder is a BROKEN SPEAR shaft with its iron head buried in the plate (the shaft pointing up-left, its "
           "end broken), the long one on the chest a broken spear head, the other ones BROKEN ARROWS (a short wooden shaft with grey "
           "fletching) stuck in; the small floating ones near the far bracer small arrow splinters.",
           "BIG SHOULDER: a NEW SHAPE: a big rounded pauldron of two plates whose upper edge is BROKEN off in a jagged line, no flanges.",
           "CHEST PLATE: blackened rusty breastplate with ONE long diagonal SWORD CUT across it; through the cut green soul fire shows.",
           "TABARD: a torn dark wine-red cloth strip #5E2430 with a worn gold border, ragged lower end.",
           "NEAR ARM: rusty black vambrace with ONE green rune (a simple circle with a line through it); black iron fist.",
           "FAR ARM: rusty bracer; the hand a black iron gauntlet with pointed fingers.",
           "SWORD: a NEW SHAPE: an ancient black-iron longsword BROKEN OFF about two thirds along (jagged broken end), notched, rusty; the "
           "crossguard a straight bar with a RING round the base of the blade, ONE green soul gem in the pommel; dark grip.",
           "CAPE: a faded dark WINE-RED royal cape #4E1F2A with a frayed worn gold border along its edge, torn into ragged strips.",
           "FLOATING DEBRIS: two broken arrow heads and three small pieces of a broken iron shield."]),
}

STYLE_ANH1 = (
    "Image 1 is painted in a smooth digital cel style with soft light and dark planes, glossy gems and white-gold-purple colours: do NOT "
    "copy that painting style or its colours")

R_VI = ("the REFERENCE character, 1536x1024, white background: a floating hollow armoured knight with no legs, turned to the right: a "
        "white helmet with a pale feather crest, a dark void body, a big white-and-gold shoulder plate with purple crystal shards, a white "
        "chest plate, a purple torn cape, a big gauntlet holding a broad sword with a round blue gem pointing down-right, an open dark "
        "clawed hand on the right, small dark stones floating below. It is painted in a smooth digital cel style. Keep its POSE, its PIECES "
        "and their PLACES; change its LOOK and the shapes listed.",
        "Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): hiệp sĩ giáp rỗng không chân lơ lửng, quay phải; mũ trắng chùm lông vũ, "
        "thân là khoảng rỗng đen, giáp vai trắng vàng to có tinh thể tím, giáp ngực trắng, áo choàng tím rách, găng to cầm kiếm bản rộng "
        "ngọc lam chĩa xuống phải, bàn tay vuốt tối bên phải, đá nhỏ lơ lửng dưới thân. Giữ dáng và từng mảnh, đổi hình")
R_SOI = ("an approved hero of our game from the same metal island (an armoured wolf with a big iron shield), 1536x1024, white background: "
         "match EXACTLY its wobbly dark-brown pen line, its visible crayon hatching and its completely flat colouring of dark iron plates "
         "(front faces and darker side faces). Do NOT copy its design or colours.",
         "Sói giáp sắt (tướng 6 đảo Kim) đã duyệt: lấy nét bút rung, vân sáp, cách tô giáp sắt sẫm phẳng (mặt trước + mặt bên sẫm hơn)")
R_PHAP = ("another approved hero of our game (a hooded fire mage), 1536x1024, white background: see how a DARK VOID face with two bright "
          "eyes and how FLAMES are drawn in our style (flat flame shapes with an ink outline, two flat tones, no glow). Do NOT copy its "
          "design, its hood or its orange colours.",
          "Pháp sư lửa (tướng đảo Hỏa) đã duyệt: xem cách vẽ khoảng tối trong mũ trùm với hai mắt sáng, và cách vẽ lửa phẳng có viền mực")

TASK = ("TASK: REDESIGN ON THE SAME POSE. Redraw the knight of image 1 as ONE picture of OUR OWN character, an ANCIENT CURSED KNIGHT who "
        "cannot die: an empty suit of very old black rusty iron armour kept alive by green soul fire inside. The SAME pose (floating, no "
        "legs, three-quarter view turned to the right), with EVERY piece in the same place, at the same size and with the same overlaps "
        "(if the new picture were laid over image 1, every piece must sit on its old place), but with the NEW shapes, new materials, new "
        "colours and our hand-drawn drawing style described below. Do not add pieces, do not remove, merge or move pieces.")
MOOD = ("Mood: a grim, determined, unstoppable undead knight ready to fight (a game hero), heavy and powerful; not a cute mascot, not "
        "horror: no skulls, no bones, no blood. Both arms stay attached to the body exactly as in image 1; the near fist holds the sword "
        "grip; the far hand is open, reaching forward; no legs, the cape hangs down.")
