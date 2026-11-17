# -*- coding: utf-8 -*-
"""Thú giáp pháo (thu_phao): mô tả con gốc monster_3629 từng mảnh và ba hướng concept lượt 1 (Claude đề xuất, chờ người dùng chọn).
Dùng trong thu_phao_da.py (prompt_concept)."""

MO_TA_CON = (
    "PIECE BY PIECE (as in image 1: a heavy, low, wide FOUR-LEGGED BEAST seen from the side in three-quarter view, turned to the RIGHT, "
    "built like a tortoise; its whole body is covered by big blocky armour pieces; its TAIL rises at the rear, curls up over its back "
    "and becomes a huge CANNON lying along the top of the back, with the cannon MUZZLE above the head, pointing to the RIGHT): "
    "HEAD (lower right, low between the front legs): a small blocky head turned to the right, a squarish face plate; two tall narrow "
    "fin-shaped EARS rise from the top of the head, sweeping up and back (to the upper left). "
    "BODY: a big rounded DOME of overlapping armour plates (like a tortoise shell) from the middle to the right, in about three rows "
    "(a top row under the cannon, a middle row, a lower row along the flank); a dark belly shows under the dome, between the legs; a "
    "short thick neck under the front of the dome, behind the head. "
    "LEGS: four short, thick legs, each built of stacked blocks (a big upper block at the shoulder or hip, a smaller knee block, a lower "
    "leg block, and a wide flat foot with three or four flat toes): the NEAR FRONT leg (right of the middle, in front of the body), the "
    "FAR FRONT leg (far right, partly behind the head), the NEAR BACK leg (lower left) and the FAR BACK leg (middle, behind the body). "
    "TAIL: at the rear (left), FOUR big rounded lumps stacked one under another curl down along the back of the body like the thick "
    "segments of a tail, with a dark mass behind them. "
    "CANNON (on top of the back): from the tail a long BOX-SHAPED cannon body lies along the top of the back, from the rear (left, above "
    "the tail) to the front (right); on its rear end, on the left side, a ROUND core (a thick ring with a glowing inside); two flat "
    "hook-shaped HANDLES stick up on top of its rear part; a raised block in its middle; at its front end a big square MUZZLE BLOCK whose "
    "front face, facing right, has an arched glowing opening, right above the head.")

# Mỗi hướng: (tên Việt, mô tả Việt, các dòng CHANGE tiếng Anh)
_KHONG = ("No spiral patterns, no carved meanders, no stone texture anywhere: this beast is made of forged METAL armour plates, not "
          "stone.")

HUONG = {
    "A": ("thép xám lam + đồng thau, lõi điện lam",
          "giáp THÉP XÁM LAM (mặt trước sáng, mặt bên sẫm), viền ĐỒNG THAU và vài đinh tán tròn; bỏ hết hoa văn xoắn đá; ĐẦU đổi dáng: mũ giáp "
          "kín mõm tròn như heo rừng, khe mắt ngang với HAI MẮT LAM ĐIỆN xếch; hai tai thành HAI SỪNG LƯỠI THÉP vuốt ra sau; PHÁO: thân pháo khối "
          "thép có hai đai đồng, khối giữa thành nắp ổ đạn có bản lề; khối họng thành HỌNG PHÁO TRÒN vành loe đồng thau, lòng họng lam điện "
          "tô phẳng; lõi tròn thành ô cửa đồng lõi lam điện; hai móc thành hai tay cầm đồng hình chữ C vuông; đuôi bốn khối thành bốn ĐỐT "
          "GIÁP ĐUÔI chồng nhau viền đồng; chân khối thép viền đồng, ngón thành vuốt thép sẫm; bụng thép sẫm",
          ["ARMOUR: forged STEEL plates, flat steel blue-grey #8593A3 on the faces turned to the viewer and darker steel #5C6878 on the faces "
           "turned away; a thin flat BRASS trim #C9A24E along the lower rim of the big plates; only a few small round rivets (2 or 3 on a big "
           "plate, none on small pieces). " + _KHONG,
           "GLOW PARTS (the inside of the round core and the inside of the muzzle): flat ELECTRIC BLUE in two flat tones only: bright "
           "#4FD8FF outside and pale #D4F7FF for one simple inner shape, inside their ink outline. No glow, no halo, no light rays, no "
           "gradient, no lightning bolts.",
           "HEAD: a NEW SHAPE: a closed armoured helm like the head of a war BOAR, turned to the right: a rounded snout guard at its front "
           "with two small round nostril holes, a narrow horizontal VISOR slit, and in the slit TWO small slanted angry eyes, flat electric "
           "blue #4FD8FF with one small white dot each (no glow); a short brass rim along the lower edge of the helm.",
           "EARS: the two fin-shaped ears become TWO swept-back STEEL BLADE HORNS (flat, pointed, slightly curved), same places, lengths and "
           "directions, with a brass band at their base.",
           "CANNON BODY: the box-shaped cannon body becomes a heavy steel GUN HOUSING (keep its blocky outline) with TWO brass bands round "
           "it; the raised block in its middle becomes an AMMO HATCH with one brass hinge.",
           "MUZZLE: a NEW SHAPE: the square muzzle block becomes a big ROUND CANNON MOUTH seen in three-quarter view (an upright oval facing "
           "right) with a thick flared BRASS rim; inside it the dark bore with the electric-blue glow in its middle; behind the rim the "
           "short thick steel barrel, same place and size as the old block.",
           "ROUND CORE: a round brass PORTHOLE ring with the electric-blue core inside, same place and size.",
           "HANDLES: the two hook-shaped handles become two simple flat BRASS handles shaped like a squared letter C, same places and size.",
           "TAIL: the four rounded lumps become FOUR overlapping curved steel TAIL PLATES (like the segments of an armadillo tail), each with "
           "a brass rim on its lower edge, same places and sizes; the dark mass behind them dark steel #3F4652.",
           "BODY DOME: the same rows of plates, now plain steel plates, each with the brass rim and 2 or 3 rivets; the belly under the dome "
           "very dark steel #3A404B (flat).",
           "LEGS: the same stacked blocks, now plain steel blocks with a brass rim on the big upper blocks; the flat toes become short thick "
           "dark-steel CLAWS #4A4F58."]),
    "B": ("sắt đen rèn + đồng đỏ, lõi lửa lò",
          "giáp SẮT ĐEN RÈN, viền ĐỒNG ĐỎ, đinh tán to; lòng lõi và họng pháo LỬA LÒ CAM tô phẳng; ĐẦU đổi dáng: mũ giáp TÊ GIÁC có một sừng mũi "
          "ngắn dày, khe mắt hẹp hai mắt cam; hai tai thành hai sừng cong ngắn; PHÁO: thân pháo có ba đai đồng đỏ, khối giữa thành ống khói "
          "ngắn; họng thành họng pháo cối TRÒN có vành răng cưa; lõi tròn thành cửa lò tròn có song sắt; hai móc thành hai vây tản nhiệt; "
          "đuôi bốn khối thành bốn đốt giáp gai tù; chân khối sắt có đinh to, vuốt đồng đỏ",
          ["ARMOUR: blackened FORGED IRON, flat dark iron #4A4D55 on the faces turned to the viewer and darker iron #2F3137 on the faces "
           "turned away; a flat COPPER-RED trim #B0583A along the rims of the big plates; a few big round rivets. " + _KHONG,
           "GLOW PARTS (the inside of the round core and the inside of the muzzle): flat FURNACE ORANGE in two flat tones only: #FF9A3D "
           "outside and pale yellow #FFE39A for one simple inner shape, inside their ink outline. No glow, no halo, no light rays, no "
           "gradient, no flames sticking out.",
           "HEAD: a NEW SHAPE: a heavy armoured helm like the head of a RHINO, turned to the right: a thick face plate with ONE short thick "
           "horn on the snout pointing up and forward, a narrow eye slit with TWO small slanted angry eyes, flat orange #FF9A3D with one "
           "small white dot each (no glow).",
           "EARS: the two fin-shaped ears become TWO short thick curved iron HORNS sweeping back, same places and directions (a little "
           "shorter).",
           "CANNON BODY: the box-shaped cannon body becomes a heavy black-iron gun housing (keep its blocky outline) with THREE copper-red "
           "bands; the raised block in its middle becomes a short square SMOKESTACK.",
           "MUZZLE: a NEW SHAPE: the square muzzle block becomes a big ROUND MORTAR MOUTH seen in three-quarter view (an upright oval facing "
           "right) with a thick iron rim notched into blunt teeth; inside it the dark bore with the orange glow in its middle; same place "
           "and size as the old block.",
           "ROUND CORE: a round FURNACE DOOR with three iron bars across the orange glow, in a thick copper ring, same place and size.",
           "HANDLES: the two hook-shaped handles become two flat iron COOLING FINS (simple rectangles with three slots), same places and size.",
           "TAIL: the four rounded lumps become FOUR overlapping heavy iron tail segments, each with ONE blunt short spike on top, same places "
           "and sizes; the dark mass behind them very dark iron #26282D.",
           "BODY DOME: the same rows of plates, now black-iron plates with the copper-red rim and big rivets; the belly very dark iron "
           "#2A2C31 (flat).",
           "LEGS: the same stacked blocks, black iron with a few big rivets; the flat toes become short thick copper-red CLAWS #9A4A30."]),
    "C": ("thép bạc trắng + vàng kim, lõi vàng",
          "giáp THÉP BẠC TRẮNG kiểu giáp hiệp sĩ, viền VÀNG KIM; lòng lõi và họng pháo VÀNG tô phẳng; ĐẦU đổi dáng: mũ hiệp sĩ đầu SƯ TỬ có khe "
          "mắt chữ T, chỏm vàng; hai tai thành hai tai giáp nhọn dựng đứng viền vàng; PHÁO: thân pháo bạc có gờ vàng dọc sống, khối giữa thành "
          "khiên huy hiệu tròn trơn; họng thành họng pháo TRÒN vành vàng chạm hình cánh; lõi tròn thành mặt trời vàng tám tia ngắn; hai móc thành "
          "hai cánh vàng nhỏ; đuôi bốn khối thành bốn vảy giáp bạc viền vàng; chân khối bạc viền vàng, vuốt vàng sẫm",
          ["ARMOUR: polished-looking but FLAT SILVER-WHITE knight steel, #C9D0D8 on the faces turned to the viewer and #9AA3AE on the faces "
           "turned away; a flat GOLD trim #D3A83F along the rims of the big plates; almost no rivets. " + _KHONG,
           "GLOW PARTS (the inside of the round core and the inside of the muzzle): flat GOLDEN YELLOW in two flat tones only: #FFC93C "
           "outside and pale #FFF1B0 for one simple inner shape, inside their ink outline. No glow, no halo, no light rays, no gradient.",
           "HEAD: a NEW SHAPE: a knight helm shaped like the head of a LION, turned to the right: a short muzzle plate, a T-shaped visor slit "
           "with TWO small slanted angry eyes, flat golden yellow #FFC93C with one small white dot each (no glow), and a small gold crest "
           "ridge on top.",
           "EARS: the two fin-shaped ears become TWO upright pointed armour EAR GUARDS with gold rims, same places, lengths and directions.",
           "CANNON BODY: the box-shaped cannon body becomes a silver gun housing (keep its blocky outline) with ONE gold ridge along its top "
           "edge; the raised block in its middle becomes a plain round gold-rimmed SHIELD BOSS.",
           "MUZZLE: a NEW SHAPE: the square muzzle block becomes a big ROUND CANNON MOUTH seen in three-quarter view (an upright oval facing "
           "right) with a thick gold rim carrying two small gold WING shapes on its sides; inside it the dark bore with the golden glow in "
           "its middle; same place and size as the old block.",
           "ROUND CORE: a gold ring with a simple golden SUN of eight short rays inside, same place and size.",
           "HANDLES: the two hook-shaped handles become two small flat gold WINGS, same places and size.",
           "TAIL: the four rounded lumps become FOUR overlapping silver armour SCALES with gold rims, same places and sizes; the dark mass "
           "behind them steel grey #6C7480.",
           "BODY DOME: the same rows of plates, now silver plates with the gold rim; the belly dark steel #4A505A (flat).",
           "LEGS: the same stacked blocks, silver with gold rims on the big upper blocks; the flat toes become short dark-gold CLAWS "
           "#9C7A2E."]),
}

STYLE_ANH1 = (
    "Image 1 is painted in a smooth digital cel style with soft light and dark planes, jade-green stone with carved spirals and glowing "
    "gradient light: do NOT copy that painting style, its stone material or its colours")

R_VI = ("the REFERENCE beast, 1536x1024, white background: a heavy four-legged jade-green stone beast turned to the right, low like a "
        "tortoise, covered in blocky armour pieces with carved spirals; a small blocky head with two tall fin ears at the lower right; four "
        "short thick block legs; at the rear four big rounded lumps curling down like a tail; on its back a long box-shaped cannon with a "
        "round glowing core at the rear, two brown hook handles on top and a square muzzle block with a glowing arch above the head. It "
        "is painted in a smooth digital cel style. Keep its POSE, its PIECES and their PLACES; change its LOOK and the shapes listed.",
        "Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): thú đá lục bốn chân quay phải, thấp như rùa, giáp khối hoa văn xoắn; đầu "
        "khối nhỏ hai tai vây cao ở dưới bên phải; bốn chân khối ngắn; bốn khối đá tròn cuộn xuống làm đuôi; trên lưng khẩu pháo khối dài "
        "có lõi tròn sáng ở đuôi, hai móc nâu, khối họng vuông có ô cửa vòm sáng ở trên đầu. Giữ dáng và từng mảnh, đổi hình")
R_SOI = ("an approved hero of our game from the same metal island (an armoured wolf with a big iron shield), 1536x1024, white background: "
         "match EXACTLY its wobbly dark-brown pen line, its visible crayon hatching and its completely flat colouring of metal plates "
         "(front faces and darker side faces, a flat metal trim). Do NOT copy its design or its colours.",
         "Sói giáp sắt (tướng 6 đảo Kim) đã duyệt: lấy nét bút rung, vân sáp, cách tô giáp kim loại phẳng (mặt trước + mặt bên sẫm hơn, viền "
         "kim loại phẳng)")
R_PHAP = ("another approved hero of our game from the same island (an ancient war robot), 1536x1024, white background: see how round "
          "rivets, metal bands, round ports and a glowing eye are drawn in our style (flat, an ink outline, no glow, one small white dot "
          "in the eye). Do NOT copy its design, its rust or its colours.",
          "Robot hủy diệt cổ (tướng 7 đảo Kim) đã duyệt: xem cách vẽ đinh tán, đai kim loại, ô tròn, mắt sáng theo nét của game (phẳng, viền "
          "mực, không quầng sáng)")

TASK = ("TASK: REDESIGN ON THE SAME POSE. Redraw the beast of image 1 as ONE picture of OUR OWN character, an ARMOURED SIEGE BEAST: a "
        "sturdy four-legged beast fully clad in forged metal armour, whose TAIL is a big CANNON curling up over its back and aiming forward "
        "over its head. The SAME pose (three-quarter view turned to the right, standing on four short legs), with EVERY piece in the same "
        "place, at the same size and with the same overlaps (if the new picture were laid over image 1, every piece must sit on its old "
        "place), but with the NEW shapes, new materials, new colours and our hand-drawn drawing style described below. Do not add pieces, "
        "do not remove, merge or move pieces.")
MOOD = ("Mood: a stubborn, determined armoured war beast ready to fight (a game hero), a walking siege cannon, heavy and powerful; the "
        "small head low and aggressive, the eyes angry and focused; not a cute mascot, not horror: no skulls, no bones, no blood. The "
        "cannon muzzle stays above the head pointing right; all four feet stand on the ground.")
