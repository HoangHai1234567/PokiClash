# -*- coding: utf-8 -*-
"""Robot hủy diệt cổ đại (robot_co): mô tả con gốc monster_3613 từng mảnh và ba hướng concept lượt 1 (Claude đề xuất, chờ người dùng chọn).
Dùng trong robot_co_da.py (prompt_concept)."""

MO_TA_CON = (
    "PIECE BY PIECE (as in image 1: a big heavy ancient war robot seen straight from the FRONT, nearly symmetric, crouching low; its wide "
    "armoured shoulders sit much higher than its small head; its two huge arms come down so that both big fists rest on the ground in "
    "front of its short legs): "
    "the HEAD in the top middle: a small head between the shoulders on a short thick neck; its top is a wide crest (in image 1 a T-shaped "
    "hammer-head cap with a tall split blade rising from its middle); ONE round EYE in the middle of the head; a FACE PLATE (a separate "
    "frame piece) laid over the front of the head, with a round opening around the eye, its lower tip pointing down to the chest. "
    "NECK: a short neck with a row of small round holes, sitting in a thick collar. "
    "CHEST: TWO big curved CHEST PLATES (a left one and a right one) cover the upper chest like a split collar; their inner ends meet in "
    "the middle of the chest along a thin vertical seam, and where they meet they leave a ROUND OPENING with a dark ring inside and one "
    "small round light in its centre (the same colour as the eye). "
    "LOWER BODY: under the chest plates a dark round lower body, with two short pale tooth-like plates on its sides. "
    "WAIST: from under the chest hang FIVE CLOTH STRIPS (a wide one in the middle, two narrow ones on each side) with torn ragged ends, "
    "reaching down between the two fists. "
    "SHOULDERS: on each shoulder a big rounded PAULDRON (armour plate) curving down over the upper arm; from the top of each shoulder a "
    "big pointed spike rises and curves up and outward (the left one to the upper left, the right one to the upper right); small red "
    "cones stick out under the pauldrons and at the elbows. "
    "ARMS: the upper arms hidden under the pauldrons; each FOREARM is a huge round barrel-shaped shell (the left one curving down and to "
    "the right, the right one down and to the left), ending in a dark round FIST SOCKET with a red ring inside, facing the middle; from "
    "each socket come THREE short thick dark FINGERS (two segments each) resting on the ground. "
    "LEGS: two short thick dark cylinder legs under the body, mostly hidden behind the forearms (the left leg shows on the far left behind "
    "the left forearm, the right leg under the right forearm), each with a pale armour plate on its outer side and a red cone on its top, "
    "and two small round toes at the bottom.")

# Mỗi hướng: (tên Việt, mô tả Việt, các dòng CHANGE tiếng Anh)
HUONG = {
    "A": ("đồng thau cổ phủ gỉ xanh",
          "giáp đồng thau vàng nâu, vài mảng gỉ xanh ngọc thay vết ố; thân, cổ, chân, ngón sắt sẫm; mắt đỏ cam; chỏm đầu ĐỔI DÁNG: miệng "
          "vạc đồng cổ có hai quai vuông dựng đứng (bỏ chỏm chữ T + lưỡi chẻ); mặt nạ đồng hình khiên đáy nhọn, gờ mày ngang; gai vai ĐỔI "
          "DÁNG: lưỡi rìu đồng cổ dựng đứng thay sừng đen cong; giáp ngực hoa văn xoắn vuông; vải xanh mòng két sọc đồng; nón đỏ thành đinh "
          "đồng tròn",
          ["ARMOUR colours: warm BRONZE #B9853F on the main faces, darker bronze #8C5E2C on the faces turned away, and a few flat VERDIGRIS "
           "patches #5FA89B (old green-blue patina, 2 or 3 simple rounded patches on each big plate) instead of the stains of image 1. The "
           "dark inner body, the neck, the legs, the fingers and the inside of the fist sockets: dark iron #3A3940.",
           "EYE: one round eye, flat red-orange #E0482F inside its ink outline, with one small white dot (no glow, no shine streak). The "
           "light in the chest opening the same red-orange.",
           "HEAD CREST: a NEW SHAPE instead of the T-shaped cap and the split blade: the top of the head is a wide rectangular RIM like the "
           "mouth of an ancient bronze cauldron, with TWO upright square LOOP HANDLES standing on its two top corners (each a thick "
           "square-cornered ring with an open hole in the middle). Nothing in the middle of the crest.",
           "FACE PLATE: a NEW SHAPE: a bronze mask shaped like a SHIELD with a pointed bottom, a thick horizontal brow ridge across its top "
           "over the eye, a round opening for the eye; it covers the front of the head and its pointed bottom reaches the collar.",
           "SHOULDER SPIKES: a NEW SHAPE instead of the dark curved horns: on each shoulder an upright ancient bronze AXE BLADE: a flat broad "
           "blade with a straight inner edge and a wide rounded cutting edge facing outward, two small round holes near its base; bronze "
           "with one verdigris patch.",
           "PAULDRONS: smooth rounded bronze plates with one raised rim along their lower edge.",
           "CHEST PLATES: keep the two curved plates meeting in the middle round the round opening, but their pattern becomes ONE simple "
           "square-spiral line motif on each plate (thin dark lines) and a raised rim along their inner curved edge.",
           "FOREARMS: the same huge round barrel shells, bronze with TWO raised bands round them; the fist socket a dark iron ring with a "
           "red-orange ring inside.",
           "The small RED CONES become round dome-shaped BRONZE STUDS in the same places.",
           "CLOTH STRIPS: the same five strips in dark teal cloth #2D5C60 with a few straight bronze-coloured lines and a bronze band at "
           "the top; torn ends.",
           "LEGS: dark iron with a bronze plate on their outer side and a bronze stud on top."]),
    "B": ("thép đen + vàng kim + xanh lam kiểu Ai Cập cổ",
          "giáp thép đen ánh lam, viền vàng kim, sọc xanh lam; mắt đỏ; chỏm đầu ĐỔI DÁNG: mũ trùm kiểu pharaoh hai vạt loe rủ xuống hai bên "
          "cổ, sọc vàng – lam (bỏ chỏm chữ T); mặt nạ vàng hẹp có chòm cằm dài; gai vai ĐỔI DÁNG: cánh chim ưng xếp ba bậc vểnh lên thay "
          "sừng; giáp ngực thành vòng cổ rộng sọc vàng – lam; vải xanh lam viền vàng; nón đỏ thành nón vàng",
          ["ARMOUR colours: blackened iron #3B3F4E on the main faces, darker #2B2E3A on the faces turned away, GOLD #D7A63E on the rims "
           "and the parts listed as gold, LAPIS BLUE #2E5AA6 for the stripes listed. No stains; instead a few small flat chipped spots of "
           "lighter iron #5A5F70 on the big plates.",
           "EYE: one round eye, flat red #D83A2E inside its ink outline, with one small white dot (no glow, no shine streak). The light in "
           "the chest opening the same red.",
           "HEAD CREST: a NEW SHAPE: a PHARAOH-STYLE HEADDRESS: the top of the head is a rounded hood whose two sides flare out and fall "
           "down in two wide flat flaps beside the neck down to the top of the shoulders, striped in alternating gold and lapis blue bands "
           "(5 bands on each side). No T-shaped cap, no blade.",
           "FACE PLATE: a NEW SHAPE: a narrow GOLD mask with a round opening for the eye, a straight flat top under the hood, and a long "
           "narrow CHIN piece hanging down from its bottom to the collar (like a long ceremonial beard).",
           "SHOULDER SPIKES: a NEW SHAPE instead of the curved horns: on each shoulder a folded FALCON WING standing up and outward: three "
           "stepped feather plates (blackened iron with gold edges), the longest one at the back, their tips pointing up and out.",
           "PAULDRONS: rounded blackened iron plates with a gold rim.",
           "CHEST PLATES: keep the two curved plates meeting in the middle round the round opening; they become a broad COLLAR: three "
           "curved stripes following their curve, gold, lapis, gold.",
           "FOREARMS: the same huge round barrel shells in blackened iron with one gold band and one lapis band; the fist socket rim gold "
           "with a red ring inside.",
           "The small RED CONES become small GOLD cones in the same places.",
           "CLOTH STRIPS: the same five strips in lapis blue cloth with a gold band at the top and two gold stripes near the torn ends.",
           "LEGS: blackened iron with a gold plate on their outer side and a gold cone on top."]),
    "C": ("sắt cổ gỉ sét, cỗ máy chiến tranh có ống xả",
          "giáp sắt xám thép, vài mảng gỉ cam thay vết ố, thân sẫm; mắt vàng hổ phách; chỏm đầu ĐỔI DÁNG: mũ vòm có một vây sống chạy dọc "
          "đỉnh (bỏ chỏm chữ T); mặt nạ vuông có hàm lưới bốn khe; gai vai ĐỔI DÁNG: mỗi vai hai ống xả tròn chĩa lên thay sừng; giáp vai "
          "và giáp ngực tán đinh to; vải thành dải da nâu sẫm; nón đỏ thành gai sắt ngắn",
          ["ARMOUR colours: gunmetal iron #646A74 on the main faces, darker iron #454A53 on the faces turned away, and a few flat RUST "
           "patches #B4602E (2 or 3 simple patches on each big plate) instead of the stains of image 1. The dark inner body, the neck, the "
           "legs, the fingers and the inside of the fist sockets: very dark iron #2F2F35.",
           "EYE: one round eye, flat amber yellow #F2B33D inside its ink outline, with one small white dot (no glow, no shine streak). The "
           "light in the chest opening the same amber.",
           "HEAD CREST: a NEW SHAPE instead of the T-shaped cap and the split blade: a rounded DOME helmet top with ONE tall flat FIN "
           "running from front to back over it (a crest ridge, its front edge sloping back). No T-shaped cap, no blade.",
           "FACE PLATE: a NEW SHAPE: a squarish iron VISOR with a round opening for the eye and, under the eye, a JAW GRILLE of four "
           "vertical slots; its lower edge straight, reaching the collar.",
           "SHOULDER SPIKES: a NEW SHAPE instead of the curved horns: on each shoulder TWO short thick round EXHAUST PIPES rising up and a "
           "little outward (a taller one behind, a shorter one in front), each with a thick ring round its open top (the inside of the "
           "opening dark). No horns.",
           "PAULDRONS: thick rounded iron plates with a row of three big round rivets along their lower rim.",
           "CHEST PLATES: keep the two curved plates meeting in the middle round the round opening; they become thick plates with one "
           "raised rim along the inner curved edge and three big rivets each.",
           "FOREARMS: the same huge round barrel shells, gunmetal with rust patches and two riveted bands; the fist socket a dark ring with "
           "an amber ring inside.",
           "The small RED CONES become short dark IRON SPIKES in the same places.",
           "CLOTH STRIPS: the same five strips as dark brown leather straps #5A3B2A with a row of iron studs at the top; torn ends.",
           "LEGS: very dark iron with a gunmetal plate on their outer side and a short iron spike on top."]),
}

STYLE_ANH1 = (
    "Image 1 is painted in a smooth digital cel style with soft light and dark planes, weathering stains and glossy red gems: do NOT copy "
    "that painting style or its sand-gold and purple colours")

R_VI = ("the REFERENCE character, 1536x1024, white background: a big heavy ancient golem robot seen from the front, sand-gold armour with "
        "stains, a T-shaped head crest with a split blade and a gold frame round one red eye, two curved chest plates round a small red "
        "light, dark curved horns on the shoulders, red cloth strips at the waist, huge round forearms with both fists resting on the "
        "ground, short dark legs. It is painted in a smooth digital cel style. Keep its POSE, its PIECES and their PLACES; change its LOOK "
        "and the shapes listed.",
        "Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): golem robot cổ giáp vàng cát nhìn thẳng, chỏm đầu chữ T có lưỡi chẻ, khung "
        "vàng quanh một mắt đỏ, hai tấm giáp ngực cong ôm một chấm đỏ, sừng đen cong trên vai, vải đỏ ở eo, cẳng tay tròn to, hai nắm đấm "
        "chống đất, chân ngắn sẫm. Giữ dáng và từng mảnh, đổi hình")
R_SOI = ("an approved hero of our game from the same metal island (an armoured wolf with a big iron shield), 1536x1024, white background: "
         "match EXACTLY its wobbly dark-brown pen line, its visible crayon hatching and its completely flat colouring of metal plates "
         "(front faces and darker side faces, flat gold trims). Do NOT copy its design or colours.",
         "Sói giáp sắt (tướng 6 đảo Kim) đã duyệt: lấy nét bút rung, vân sáp, cách tô giáp kim loại phẳng (mặt trước + mặt bên sẫm, viền vàng phẳng)")
R_GOLEM = ("another approved hero of our game (a heavy stone golem with huge fists), 1536x1024, white background: see how a big heavy golem "
           "body with huge forearms and fists is drawn flat and solid. Do NOT copy its design, its flames or its colours.",
           "Golem lõi lửa (tướng đảo Hỏa) đã duyệt: xem cách vẽ thân golem to nặng, cẳng tay và nắm đấm to, tô phẳng")

TASK = ("TASK: REDESIGN ON THE SAME POSE. Redraw the robot of image 1 as ONE picture of OUR OWN character, an ANCIENT DESTRUCTION ROBOT (a "
        "war machine built in ancient times): the SAME pose, seen straight from the front, with EVERY piece in the same place, at the same "
        "size and with the same overlaps (if the new picture were laid over image 1, every piece must sit on its old place), but with the "
        "NEW shapes, new materials, new colours and our hand-drawn drawing style described below. Do not add pieces, do not remove, merge "
        "or move pieces.")
MOOD = ("Mood: a heavy, menacing, determined ancient war robot ready to fight (a game hero), solid and powerful; not a cute mascot, not "
        "horror. Both arms and both legs stay attached to the body exactly as in image 1; both fists rest on the ground; the two chest "
        "plates meet in the middle round the round opening.")
