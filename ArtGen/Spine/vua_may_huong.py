# -*- coding: utf-8 -*-
"""Vua robot (vua_may): mô tả con gốc monster_3637 từng mảnh (theo sơ đồ bố cục đã nâng thân, chân robot, bốn cánh) và ba hướng concept
lượt 1 (Claude đề xuất, chờ người dùng chọn). Dùng trong vua_may_da.py (concept)."""

MO_TA_CON = (
    "PIECE BY PIECE (as in image 1: a big, heavy, wide ROBOT KING seen in three-quarter view, turned to the RIGHT, standing on two short "
    "sturdy legs, four wings floating behind his back):\n"
    "- HEAD (upper right of the middle): a big CROWN with tall battlements sits low over the face; under the crown band a face with TWO eye "
    "windows in the band, a white metal BEARD plate under it, a round NOSE in the middle of the beard and two small curled white moustache "
    "tips at both ends of the beard; a dark collar under the beard.\n"
    "- BODY: a broad barrel CHEST under the head with a horizontal GRILLE (five vents) in a pointed frame, a belly plate below it; a dark "
    "round GEAR (seen in perspective, a flat ellipse with teeth) at the waist on the right side.\n"
    "- NEAR SHOULDER (left of the picture): a huge rounded SHOULDER ARMOUR; a red CAPE hangs over it from the neck and falls down the left "
    "side behind the near arm to the hip.\n"
    "- FAR SHOULDER (right of the picture): a big rounded shoulder armour, a blue SASH runs over it diagonally, with a small gear emblem.\n"
    "- ARMS: both arms have a short upper arm and a HUGE rounded FOREARM armour; a dark perspective GEAR at each elbow; dark-metal HANDS "
    "with three thick fingers. The near arm (left) hangs down along the body and its hand holds the SCEPTER upright; the far arm comes "
    "across the belly, its fist in front of the chest.\n"
    "- SCEPTER (in front, left of the middle): a long straight dark shaft standing upright on the ground, a golden foot cap, a golden "
    "cup-shaped top like a little tower, a BLUE ORB on top, and the SCEPTER HEAD floating above the orb: a big flat GEAR WHEEL with a hole "
    "in the middle seen in perspective, with TWO RINGS floating under it.\n"
    "- HIP: a wide dark hip block under the belly, between the legs.\n"
    "- LEGS (NEW, image 1 only shows flat placeholder blocks): two short, very sturdy walking ROBOT LEGS standing apart, feet flat on the "
    "ground: the NEAR leg (left of the picture, in front of the hip block) and the FAR leg (right, partly behind the hip block). Each leg: "
    "a big round HIP JOINT, a thick armoured THIGH going down and outward, a big round KNEE GUARD, a thick armoured SHIN, a round ANKLE "
    "joint and a wide heavy FOOT with three blunt toes. Keep their places, sizes and directions as the blocks in image 1.\n"
    "- WINGS (NEW, image 1 only shows grey placeholder shapes): FOUR WINGS FLOATING behind the back, NOT attached: a small clear gap "
    "between the back and the root of each wing. Two big UPPER wings rise up and outward like a V behind the crown (the near one up to "
    "the upper left behind the cape, the far one up to the upper right behind the crown), two smaller LOWER wings spread sideways and a "
    "little down (the near one to the left behind the cape, the far one to the right behind the far shoulder). Each wing: a round floating "
    "CORE at its root, a WING ARM going out from it, and SIX separate overlapping FEATHERS hanging along the arm (the outer feather the "
    "longest, pointing along the arm; the inner ones shorter and pointing more and more downward). Keep their places, sizes and directions "
    "as the grey shapes in image 1. All four wings are BEHIND the body.")

STYLE_ANH1 = (
    "Image 1 is a rough PLACEMENT SKETCH: its robot body is painted in a smooth digital cel style with soft light and dark planes and "
    "glossy gold; its legs are flat placeholder blocks and its wings are grey placeholder shapes. Do NOT copy that painting style, that "
    "glossy gold, or the crude placeholder shapes")

R_VI = ("a rough PLACEMENT SKETCH, 1536x1024, white background: a golden robot king with a battlement crown, a white beard plate, a red "
        "cape over the near (left) shoulder, a blue sash, huge rounded forearms, holding upright a scepter with a blue orb and a floating "
        "gear head with two rings; under him two flat placeholder leg blocks; behind him four grey placeholder wing shapes. It shows the "
        "POSE, the PIECES, their PLACES and SIZES only.",
        "Sơ đồ bố cục (1536 × 1024, nền trắng): thân con gốc vua robot vàng (vương miện, râu trắng, áo choàng đỏ, dải xanh, quyền trượng "
        "đầu bánh răng + hai vòng) nâng lên, hai chân khối phẳng thay chân xích, bốn cánh xám giữ chỗ sau lưng. Chỉ để lấy dáng, chỗ, cỡ")
R_ROBOT = ("an approved hero of our game from the same metal island (an ancient war robot), 1536x1024, white background: match EXACTLY "
           "its wobbly dark-brown pen line, its visible crayon hatching and its completely flat colouring of metal (front faces and "
           "darker side faces, flat metal bands, flat round rivets, a flat round eye with one white dot). Do NOT copy its design, its "
           "rust or its colours.",
           "Robot hủy diệt cổ (tướng 7 đảo Kim) đã duyệt: lấy nét bút rung, vân sáp, cách tô kim loại phẳng (mặt trước + mặt bên sẫm, đai, "
           "đinh tán, mắt tròn chấm trắng)")
R_VUA = ("another approved hero of our game from the same island (a cursed ancient war king with a torn cape), 1536x1024, white "
         "background: see how a royal CAPE, a crown and big armour plates are drawn in our style (flat, an ink outline, crayon texture, no "
         "shading). Do NOT copy its design, its rust, its flames or its colours.",
         "Vong Kỵ (tướng 8 đảo Kim) đã duyệt: xem cách vẽ áo choàng, vương miện, tấm giáp lớn theo nét của game")

TASK = ("TASK: REDESIGN ON THE SAME POSE. Redraw the robot king of image 1 as ONE picture of OUR OWN character: THE FINAL BOSS of the metal "
        "island, a majestic ROBOT KING. The SAME pose (three-quarter view turned to the right), with EVERY piece of the body (crown, face, "
        "chest, shoulders, cape, sash, arms, hands, scepter, scepter head, hip) in the same place, at the same size and with the same "
        "overlaps (if the new picture were laid over image 1, every body piece must sit on its old place), and the NEW legs and wings at "
        "the places and sizes of the placeholders; but with NEW shapes, MORE DETAIL, new materials, new colours and our hand-drawn drawing "
        "style described below. Do not add other pieces, do not remove, merge or move pieces.")

DETAIL = (
    "MORE DETAIL THAN IMAGE 1 (very important, this is the final boss): every big armour piece is built of 2 or 3 layered plates with an "
    "engraved trim line along its rim, neat rows of small round rivets, small gear and sun-ray engravings on the shoulders and forearms, "
    "visible joint rings and short pistons at the elbows, knees and ankles, an embroidered border and a gear pattern on the cape, a "
    "rich crown with jewels. All of it still drawn FLAT (lines and flat colour shapes), never shaded.")

MOOD = ("Mood: a proud, commanding, battle-ready ROBOT KING (the strongest boss of the island, a game hero): chest out, a stern "
        "determined face, angry focused eyes; majestic and powerful; not a cute mascot, not horror: no skulls, no bones, no blood. He "
        "stands on his two legs, feet flat on the ground; the scepter stands upright in his near hand.")

# Mỗi hướng: (tên Việt, mô tả Việt, các dòng CHANGE tiếng Anh)
HUONG = {
    "A": ("vàng hoàng kim + men trắng, 4 cánh MÁY lơ lửng (Claude đề xuất)",
          "giáp VÀNG HOÀNG KIM xen các tấm MEN TRẮNG NGÀ, viền vàng đậm, đinh tán; áo choàng ĐỎ THẪM thêu viền vàng và hoa văn bánh răng; dải "
          "XANH HOÀNG GIA; MẶT: mũ trụ có tấm che mặt vàng, hai mắt LAM sáng xếch trong khe vương miện, RÂU kim loại trắng ba lớp xoăn, mũi "
          "giáp nhọn vàng có viên hồng ngọc; VƯƠNG MIỆN: tia mặt trời nhọn xen răng thành, đính ngọc lam; QUYỀN TRƯỢNG: đầu bánh răng mặt "
          "trời + hai vòng khắc vạch, ngọc lam; CHÂN: giáp vàng – trắng, gối bánh răng, pít-tông sau ống chân, bàn chân ba ngón; CÁNH: 4 cánh "
          "MÁY lơ lửng, khung vàng, lông THÉP TRẮNG viền vàng tách rời từng chiếc, lõi gốc cánh ngọc lam",
          ["ARMOUR: royal GOLD #E3B54A on the faces turned to the viewer, darker gold #B8862F on the faces turned away, with inset panels of "
           "flat IVORY-WHITE enamel #F2ECDC (on the chest, the shoulders, the forearms, the thighs) edged with the gold; dark joints and gears "
           "flat bronze-brown #5E4A33.",
           "FACE: a gold face plate under the crown band; in the band TWO narrow slanted angry EYES, flat bright blue #4FC3FF with one small "
           "white dot each (no glow); the beard becomes a majestic WHITE METAL BEARD #ECEFF2 of three stacked curled plates; the round nose "
           "becomes a short pointed gold NOSE GUARD with a small round RUBY #D8343A; the two moustache tips become two curled white metal "
           "moustache plates.",
           "CROWN: a NEW SHAPE: a tall gold crown whose battlements alternate with sharp SUN-RAY spikes, a band of round BLUE jewels #3E8EE8 "
           "and one big blue jewel in the front.",
           "CAPE: deep CRIMSON #B5283A with a wide embroidered gold border and a pattern of small gold gears; its inside darker #7E1C2C. "
           "SASH: royal blue #2F5FC4 with a gold edge and a gold gear emblem.",
           "SCEPTER: a gold shaft with three dark rings, a long enough shaft that its gold foot rests on the ground; the tower top stays, the "
           "orb becomes a BLUE crystal ball #4FA8FF; the floating head: a big gold SUN GEAR (gear teeth plus short rays) with a blue jewel in "
           "its hole, and the two floating rings engraved with notches.",
           "LEGS: gold and ivory armour plates, a gold KNEE GUARD with a gear at the joint, a short piston behind the shin, a heavy gold FOOT "
           "with three blunt toes and a dark sole.",
           "WINGS: four floating MECHANICAL wings: a gold WING ARM with rivets; SIX separate long FEATHER PLATES of white steel #E4E8EE with a "
           "thin gold rim and one engraved line each, with small gaps between them like floating metal feathers; a round BLUE gem core "
           "#4FA8FF in a gold ring at the root of each wing (flat, no glow)."]),
    "B": ("vàng hoàng kim + bạc, 4 cánh LÔNG VŨ TRẮNG thiên thần",
          "giáp VÀNG xen BẠC, áo choàng ĐỎ SON viền trắng lông, dải XANH TRỜI; MẶT: hai mắt VÀNG SÁNG, râu bạc dài chẻ đôi, mũi giáp; VƯƠNG "
          "MIỆN: vòng nguyệt quế vàng + răng thành; QUYỀN TRƯỢNG: bánh răng có hai cánh nhỏ + hai vòng; CHÂN: giáp vàng bạc; CÁNH: 4 cánh LÔNG "
          "VŨ TRẮNG thiên thần lơ lửng (lông thật, mềm, ngọn ánh vàng nhạt), gốc cánh là vòng vàng nhỏ",
          ["ARMOUR: GOLD #DDB04C on the faces turned to the viewer, darker gold #AE8231 on the faces turned away, with inset SILVER panels "
           "#C9CED6 (darker #9AA1AC) on the chest, the shoulders and the forearms; dark joints and gears flat dark steel #4E525A.",
           "FACE: in the crown band TWO narrow slanted angry EYES, flat bright golden yellow #FFD24A with one small white dot each (no glow); "
           "the beard becomes a long SILVER beard plate split into two points; the round nose becomes a short silver nose guard; the two "
           "moustache tips become two long swept silver moustache plates.",
           "CROWN: a NEW SHAPE: a gold crown whose battlements are wrapped by a gold LAUREL wreath, with a row of small white pearls.",
           "CAPE: VERMILION red #D2412F with a thick white FUR trim #F4F0E6 (simple flat tufts) along its edge and gold stitches. SASH: sky "
           "blue #4C8FD8 with a gold edge.",
           "SCEPTER: a silver shaft long enough that its foot rests on the ground; gold tower top; a white pearl orb; the floating head: a "
           "gold GEAR with two small gold wings on its sides, and the two floating gold rings.",
           "LEGS: gold armour with silver knee guards, a gear at each knee, heavy gold FEET with three blunt toes.",
           "WINGS: four floating ANGEL WINGS of real soft WHITE FEATHERS #F7F7F4: each wing a white feathered wing arm and SIX big separate "
           "flight feathers, each feather with one simple quill line and a pale gold tip #EBD9A0; a small gold RING floating at the root of "
           "each wing; flat white, no glow, no shine."]),
    "C": ("thép đen + vàng, 4 cánh LÔNG VŨ ĐEN, mắt đỏ (bản tối)",
          "giáp THÉP ĐEN xanh than viền VÀNG, áo choàng ĐỎ RƯỢU viền vàng, dải TÍM; MẶT: mặt nạ đen, hai mắt ĐỎ, râu kim loại vàng vuông vức "
          "nhiều tầng; VƯƠNG MIỆN: vàng đen răng nhọn cao, ngọc đỏ; QUYỀN TRƯỢNG: bánh răng răng nhọn + hai vòng vàng, ngọc đỏ; CHÂN: thép "
          "đen viền vàng; CÁNH: 4 cánh LÔNG VŨ ĐEN lơ lửng (lông đen ánh tím than, ngọn vàng), gốc cánh là ngọc đỏ",
          ["ARMOUR: blackened STEEL #3D4250 on the faces turned to the viewer, darker #282C36 on the faces turned away, with flat GOLD trims "
           "#D7A848 along every rim and gold rivets; joints and gears flat dark bronze #6B5434.",
           "FACE: a black face mask; in the crown band TWO narrow slanted angry EYES, flat RED #FF4A3D with one small white dot each (no "
           "glow); the beard becomes a squared GOLD beard of stacked plates; the round nose becomes a sharp black nose guard; the two "
           "moustache tips become two hooked gold moustache plates.",
           "CROWN: a NEW SHAPE: a black-and-gold crown with tall sharp pointed battlements and a band of round RED jewels #D8343A.",
           "CAPE: wine red #8E1F33 with a gold border and black gear pattern; its inside very dark #4A1420. SASH: royal purple #5B3A8E with "
           "a gold edge.",
           "SCEPTER: a black shaft with gold rings, long enough that its foot rests on the ground; gold tower top; a RED crystal orb; the "
           "floating head: a black GEAR with sharp gold teeth and a red jewel in its hole, and the two floating gold rings.",
           "LEGS: black steel with gold trims, gold knee guards with a gear, heavy black FEET with three gold-capped toes.",
           "WINGS: four floating BLACK FEATHERED wings: soft black feathers #2A2B33 with a dark plum tint on the inner faces #3B2E44, SIX big "
           "separate flight feathers per wing with one simple quill line and a thin gold tip #D7A848; a round RED gem core #D8343A in a gold "
           "ring at the root of each wing (flat, no glow)."]),
}
