# Thanh Long (ải 70, boss cuối đảo Mộc, Huyền thoại): rồng xanh lam phương Đông. Người dùng chốt concept bằng chữ 2026-11-07.
# Gốc: 214 rắn rồng xanh lá đội mũ đồng chạm hoa văn, ngồi trên mây xanh lơ, chóp đuôi pha lê lửa vàng; 215 rồng uốn khúc
# xanh lá, giáp đồng, mây xanh lơ, đuôi cầm khung pha lê vàng, phun lửa sét; 1749 rồng sấm nhiều khúc xanh lá vàng kim, giáp
# bạc vàng chạm chữ đỏ, mây xanh lơ, đuôi cầm vòng vàng.
# Mới: vảy xanh lam ngọc, bụng kem vàng, bờm trắng bay, sừng vàng san hô, râu dài trắng, vương miện ngọc nhỏ, mắt vàng hổ phách;
# mây lành trắng viền xanh ngọc (dạng 1, 2); dạng 2 ôm ngọc rồng trắng ngà; dạng 3 vảy thẫm, gai lưng vàng, sét vàng chanh,
# mây giông xám tím viền trắng.
TL_COL = ("azure-teal blue scales (a clear blue leaning to teal, NOT green), a cream-yellow belly, a flowing white mane, "
          "coral-gold antler horns, long white whiskers, a small pale turquoise-jade crown with a coral-gold rim, big "
          "golden-amber eyes")
TL_CLOUD = "white auspicious clouds with turquoise-jade edges"
TL_AV = ("a green body or green scales, sky-blue or cyan clouds, a bronze helmet or crest with carved spiral patterns, heavy "
         "bronze armor plates")

SPEC = [
    # ---------------- dạng 1: rig #214 (22 mảnh) ----------------
    F("thanh_long_1", 214, "Thanh Long", 1, 3, "Thanh Long Con", "ải 70 đảo Mộc, dạng 1/3",
      "rồng con phương Đông thân rắn ngồi trên mây lành: vảy xanh lam ngọc, bụng kem vàng, bờm trắng bay, sừng vàng san hô, "
      "râu dài trắng, vương miện ngọc nhỏ viền vàng, mắt vàng hổ phách, chóp đuôi túm lông trắng; mây trắng viền xanh ngọc",
      "a young azure EASTERN DRAGON hatchling with a long serpent body sitting on auspicious clouds, the first stage of a "
      "three-stage Wood evolution line",
      "sitting upright on its clouds with the neck raised and the head held high",
      "a proud little dragon ready to fight: brows angled down, a confident smirk with one small fang",
      f"{TL_COL}, {TL_CLOUD}", TL_AV + ", a yellow flame-shaped crystal on the tail",
      [G("N01", [15, 22, 21, 19], "giu", "head with face", "đầu có mặt",
         "a wide green dragon head turned a little to the viewer-right, with two big orange eyes with yellow brow marks (the "
         "viewer-right eye smaller), a small frowning mouth with one fang below them, and a small bronze plate over the "
         "viewer-right eye",
         "a cute chunky eastern-dragon head of azure-teal scales with a small rounded muzzle and cream-yellow lips and chin, "
         "two big golden-amber eyes (one small catchlight dot each) exactly where the old eyes are, brows angled down, a "
         "confident smirk with one small fang where the old mouth is; no bronze plate, no helmet",
         hide=[22, 21, 19]),
       G("N02", [20, 14], "doi", "small jade crown and white mane", "vương miện ngọc nhỏ và bờm trắng",
         "a tall leaf-shaped bronze-and-green helmet crest with spiral patterns rising from the forehead and leaning to the "
         "viewer-right, and a grey dome behind the top of the head",
         "a small pale turquoise-jade crown with a thin coral-gold rim sitting on the forehead where the bottom of the old "
         "crest is, and above and behind it a tall flowing white mane plume streaming up and back like the old crest; the "
         "grey dome becomes the back of the white mane fluffing out behind the top of the head; no helmet, no bronze, no "
         "spirals",
         joint="bottom end of the crest (on the forehead); the dome stays behind the top of the head"),
       G("N03", [16, 18, 17], "doi", "two horns and a whisker", "hai sừng và râu",
         "a big green pointed ear on the viewer-left side of the head, a small green pointed ear on the viewer-right side, "
         "and a small green cheek spike under the viewer-left ear pointing to the viewer-left",
         "two short coral-gold antler horns (deer-antler shape with two or three rounded tines), one where each old ear is "
         "and pointing the same way; the cheek spike becomes one long thin white whisker curling out to the viewer-left",
         joint="base of each horn and of the whisker (where they touch the head)"),
       G("N04", [9, 8, 5], "giu", "coiled serpent body", "thân rắn cuộn",
         "a curved green neck rising from the bottom coil up to the head with a cyan stripe down its viewer-left edge, a "
         "darker green body coil behind it on the viewer-left, and a round green body coil at the bottom front wrapped by a "
         "bronze patterned band",
         "the long serpent body: azure-teal scales (a few simple scale arcs) with a cream-yellow belly stripe along the neck "
         "where the cyan stripe is; the back coil the same azure-teal; the bottom coil azure-teal with a cream-yellow belly "
         "band instead of the bronze band; no bronze, no patterns"),
       G("N05", [10, 11, 13, 3, 4], "giu", "two short legs", "hai chân ngắn",
         "two short dark-green legs under the body: on the viewer-left a small oval haunch over a short leg whose BOTTOM end "
         "is a foot with three yellow claws; on the viewer-right a short thin leg behind the body whose BOTTOM end is a foot "
         "with yellow claws",
         "two short stubby azure-teal dragon legs, the TOP ends joining the body, the feet at the BOTTOM ends with three "
         "short ivory claws each"),
       G("N06", [6, 7], "doi", "tail with a white tuft", "đuôi chóp túm lông trắng",
         "a green U-shaped tail end behind the viewer-left cloud: its viewer-right end goes behind the body, its viewer-left "
         "end points up and holds a yellow flame-shaped crystal",
         "an azure-teal dragon tail with a cream-yellow underside in the same U shape, its upturned viewer-left tip ending "
         "in a flowing white hair tuft like the mane, where the old crystal is; no crystal, no flame",
         joint="viewer-right end of the tail (where it goes behind the body)"),
       G("N07", [12, 2], "doi", "auspicious clouds", "mây lành",
         "two big puffy cyan-blue clouds: a big one on the viewer-left in front of the body, a smaller one on the "
         "viewer-right behind the body",
         "two auspicious clouds in the same places and about the same size: flat white cloud puffs made of rounded swirl "
         "curls (ruyi curls) with a turquoise-jade band along the edges and a few turquoise swirl lines; no cyan-blue fill",
         joint="the clouds stay where they are, under and beside the body")],
      keep=[1],
      anim=dict(root=5, head=15, swing=[], wob=[17, 14, 6], fly=[], cast=(15, 0.65, 0.88),
                parent={9: 5, 8: 5, 15: 9, 20: 15, 14: 15, 16: 15, 18: 15, 17: 15, 6: 8, 7: 6, 13: 10, 4: 3}),
      note="1 bóng; 19 tấm đồng trên mắt phải, 21 miệng, 22 mắt: ẩn vào đầu; mây 2, 12 theo gốc"),

    # ---------------- dạng 2: rig #215 (50 mảnh) ----------------
    F("thanh_long_2", 215, "Thanh Long", 2, 3, "Thanh Long", "ải 70 đảo Mộc, dạng 2/3",
      "rồng xanh lam phương Đông uốn khúc vòng lớn trên mây lành, vuốt phải giơ dưới cằm ôm viên ngọc rồng trắng ngà: vảy "
      "xanh lam ngọc, bụng kem vàng, bờm trắng bay (chùm trên đầu và ba túm sau lưng), sừng vàng san hô, râu dài trắng, "
      "vương miện ngọc nhỏ, chóp đuôi túm lông trắng; mây trắng viền xanh ngọc",
      "a coiling azure EASTERN DRAGON holding a round dragon pearl, the SECOND stage of a three-stage Wood evolution line "
      "whose first stage is image 6: the same little azure dragon grown into a long coiling dragon",
      "coiled in a big loop above its clouds, one claw raised under its chin holding the pearl",
      "a proud young dragon king ready to strike: brow angled down, a confident open-mouthed grin showing small fangs",
      f"{TL_COL}, a flat ivory-white dragon pearl, {TL_CLOUD}",
      TL_AV + ", a yellow flame or a gold crystal frame on the tail, fire or lightning breath, bronze shoulder plates, a "
              "bronze chest plate",
      [G("N01", [30, 25, 34, 35, 36, 37, 26, 28], "giu", "head with face", "đầu có mặt",
         "a green dragon head in side view facing the viewer-right with spiky fins on the back of the skull, a small yellow "
         "eye under a glowing yellow brow, a dark bronze-trimmed band under the eye, a thin far eye near the snout, and an "
         "open lower jaw (red mouth inside, two white fangs) hanging below",
         "an eastern-dragon head of azure-teal scales facing the viewer-right with cream-yellow lips and chin, the "
         "back-of-skull spikes as small azure fins, one big golden-amber eye (one catchlight dot) exactly where the old near "
         "eye is, brow angled down, the far eye a thin golden sliver where the old one is; the lower jaw stays an open jaw "
         "with a cream-yellow lip, a dark red mouth and two small white fangs, a confident grin; no dark band under the "
         "eye, no bronze, no fire",
         hide=[34, 35, 36, 37, 26, 28]),
       G("N02", [31], "doi", "small jade crown and white mane", "vương miện ngọc nhỏ và bờm trắng",
         "a tall dark-green-and-bronze blade-shaped helmet crest with spiral patterns rising from the top of the head",
         "a small pale turquoise-jade crown with a thin coral-gold rim on top of the head where the bottom of the old crest "
         "is, and a tall flowing white mane plume streaming up and back behind it, about the size of the old crest; no "
         "helmet, no bronze, no spirals",
         joint="bottom end of the crest (on top of the head)"),
       G("N03", [33, 24, 29], "doi", "two horns and a whisker", "hai sừng và râu",
         "a long bronze-and-dark-green helmet band sweeping back from the head to the viewer-left over the top of the body "
         "loop, a short curled bronze horn on the viewer-right behind the crest, and a small dark-green-and-bronze curl at "
         "the tip of the snout",
         "two coral-gold antler horns (deer-antler shape with rounded tines): a long one sweeping back to the viewer-left "
         "where the old band is, a short one curling up on the viewer-right where the old curled horn is; the snout curl "
         "becomes one long thin white whisker curling forward from the tip of the snout",
         joint="base of each horn (on the head) and root of the whisker (at the tip of the snout)"),
       G("N04", [19, 8, 7], "doi", "white mane tufts on the back", "túm bờm trắng sau lưng",
         "three small dark-green-and-bronze blade-shaped fins sticking out from the outer (viewer-left) edge of the big "
         "body loop: two near the top of the loop, one lower down",
         "three flowing white mane tufts sticking out from the back of the body loop in the same places and pointing the "
         "same way, like the white mane of image 6; no bronze, no blades",
         joint="base of each tuft (on the outer edge of the body loop)"),
       G("N05", [22, 21, 17, 16, 18, 39, 40, 41], "giu", "coiled serpent body", "thân rắn uốn khúc",
         "the long green serpent body in segments: a dark armored chest in the middle (bronze patterned chest plate with a "
         "dark round top); from it the body rises in a big loop up the viewer-left (two segments), over the top (one "
         "segment) and into the back of the head; below the chest it curls to the viewer-right in a thick coil and down "
         "into two lower segments at the bottom; cyan stripes run along the belly side",
         "the same long serpent body in azure-teal scales (a few simple scale arcs) with a cream-yellow belly stripe where "
         "the cyan stripes are; the chest is plain azure-teal with a cream-yellow belly front; no armor plate, no bronze, "
         "no patterns"),
       G("N06", [43, 45, 44, 42, 46, 47, 23, 10, 11, 20], "giu", "two arms", "hai tay",
         "two thin dark arms with gold shoulder plates: the viewer-left arm goes down from a big gold shoulder plate, bends "
         "to the viewer-left and ends in a dark hand with three big blocky gold claws; the viewer-right arm goes from a "
         "smaller gold shoulder plate to the viewer-right and bends up toward the chin (its hand is not in this picture)",
         "two slim azure-teal dragon arms with cream-yellow scales on the inner side; the TOP ends are the shoulders "
         "joining the body, the gold shoulder plates become round azure-teal shoulders; the viewer-left hand at the far end "
         "has three curved coral-gold claws; no armor, no bronze"),
       G("N07", [13, 12, 14, 15], "doi", "hand holding the dragon pearl", "vuốt ôm ngọc rồng",
         "a dark round fist under the chin at the top end of the viewer-right arm, with three blocky gold claws curled "
         "over it",
         "a round flat ivory-white dragon pearl where the old fist is (about the same size, a thin pale cream rim line, no "
         "glow, no shine), held by the dragon's hand: three curved coral-gold claws gripping its front",
         joint="lower viewer-left end of the hand (where it meets the forearm)"),
       G("N08", [3], "doi", "tail with a white tuft", "đuôi chóp túm lông trắng",
         "a thin green tail rising from behind the lower body coil on the viewer-right, its tip holding a big hollow gold "
         "crystal frame with yellow sparks, and a small loose gold diamond beside it",
         "an azure-teal dragon tail with a cream-yellow underside rising the same way, its tip ending in a big flowing "
         "white hair tuft like the mane, where the old gold frame is; no gold frame, no crystal, no sparks, no loose "
         "diamond",
         joint="lower end of the tail (behind the lower body coil)"),
       G("N09", [4, 48, 5, 6, 38, 49], "doi", "auspicious clouds", "mây lành",
         "six puffy cyan-blue clouds with long thin trailing streaks: two piled under the body in the middle, one under the "
         "viewer-right side, one long flat one at the bottom, and two small floating ones on the viewer-left behind the body "
         "loop",
         "white auspicious clouds in the same places and sizes: flat white puffs of rounded swirl curls (ruyi curls) with a "
         "turquoise-jade band along the edges, a few turquoise swirl lines and thin turquoise trailing streaks; no cyan-blue "
         "fill",
         joint="the clouds stay where they are")],
      keep=[], drop=[1, 2, 50, 9, 27, 32], prev="thanh_long_1",
      anim=dict(root=22, head=30, swing=[43], wob=[19, 8, 7, 29, 3], fly=[], cast=(13, 0.5, 0.5),
                parent={17: 22, 16: 17, 18: 16, 30: 18, 31: 30, 33: 30, 24: 30, 29: 30, 19: 16, 8: 16, 7: 17,
                        39: 22, 40: 39, 41: 40, 3: 41, 43: 23, 45: 43, 44: 45, 42: 44, 46: 44, 47: 44,
                        10: 20, 11: 10, 13: 11, 12: 13, 14: 13, 15: 13}),
      note="1 quầng sét dưới đất (không có bóng xám), 2, 50 vệt gió trong mờ, 27, 32 lửa sét phun (chung c47), 9 chấm mờ: bỏ; "
           "34 dải dưới mắt, 35, 37 mắt, 36 mày, 26, 28 nanh: ẩn vào đầu; mây 4, 48 chung c38, 5, 6 chung c28"),

    # ---------------- dạng 3: rig #1749 (36 mảnh) ----------------
    F("thanh_long_3", 1749, "Thanh Long", 3, 3, "Lôi Thanh Long", "ải 70 đảo Mộc, dạng 3/3",
      "rồng sấm phương Đông cuộn nhiều khúc giữa mây giông: vảy xanh lam ngọc thẫm, bụng kem vàng, gai lưng vàng, bờm trắng "
      "bay, sừng vàng san hô, râu dài trắng, vương miện ngọc nhỏ, chóp đuôi túm lông trắng kèm tia sét; tia sét vàng chanh "
      "dẹt; mây giông xám tím viền trắng",
      "a mighty azure THUNDER DRAGON coiled in many loops among storm clouds, the THIRD stage of a three-stage Wood "
      "evolution line whose first stage is image 6: the same azure dragon fully grown, with deeper scales, golden back "
      "spikes and flat lemon-yellow lightning",
      "coiled in many loops in mid-air with the head raised high, claws out",
      "a fierce but cute storm dragon: brow angled down, jaws a little open in a confident grin showing small fangs",
      "DEEP azure-teal blue scales (darker than image 6, still blue-teal, NOT green), a cream-yellow belly, warm golden "
      "back spikes, a flowing white mane, coral-gold antler horns, long white whiskers, a small pale turquoise-jade crown "
      "with a coral-gold rim, big golden-amber eyes, flat lemon-yellow lightning bolts, grey-purple storm clouds with "
      "white rims",
      TL_AV + ", silver-and-gold armor blades, red rune marks, a glowing red chest orb, a gold ring ornament on the tail, "
              "cyan water splashes, a lavender wind swoosh",
      [G("N01", [32], "doi", "head with face, crown, mane and horns", "đầu có mặt, vương miện, bờm, sừng",
         "a green dragon head in side view facing the viewer-right, with a jagged gold jaw plate under the eye, a small cyan "
         "eye, a tall "
         "silver-and-gold crescent crest with a red gem on top, a big dark-green-and-gold blade sweeping back to the upper "
         "viewer-left, and silver-and-gold horn blades sweeping back to the viewer-left",
         "an eastern-dragon head of deep azure-teal scales facing the viewer-right with cream-yellow lips and chin, one big "
         "golden-amber eye (one catchlight dot) exactly where the old eye is, brow angled down, jaws a little open in a "
         "confident grin with small fangs; two coral-gold antler horns sweeping back to the viewer-left where the silver "
         "blades are, a flowing white mane streaming back to the upper viewer-left where the dark blade is, and a small "
         "pale turquoise-jade crown with a coral-gold rim on top of the head where the bottom of the old crescent crest is "
         "(much smaller than the old crest); no silver, no armor, no red gem",
         joint="back of the head (where it joins the top of the neck)"),
       G("N02", [20], "doi", "long whiskers", "râu dài",
         "a long thin silver-and-gold V-shaped jaw guard hanging under the head: it starts under the cheek and its two "
         "prongs meet in a hooked point past the snout on the viewer-right",
         "two long thin white whiskers growing from under the cheek and streaming forward and down past the snout to the "
         "viewer-right, gently wavy; no silver, no gold",
         joint="viewer-left end (under the cheek, where they hang from the head)"),
       G("N03", [19, 11, 13, 14], "giu", "coiled serpent body", "thân rắn nhiều khúc",
         "the long dark-green serpent body in four big coils with a gold-and-cream belly and small silver fin blades along "
         "the back: an S-shaped neck in the middle rising to the head (cream belly with a red rune), a figure-eight loop on "
         "the viewer-left, a big arch across the top, and a C-shaped coil on the viewer-right",
         "the same serpent body in DEEP azure-teal scales (a few simple scale arcs) with a cream-yellow belly along the "
         "inner edge where the gold-and-cream belly is; the small silver blades along the back become short warm golden "
         "spikes; no red rune, no silver"),
       G("N04", [21, 26, 29, 17, 23, 25], "giu", "two arms with claws", "hai tay có vuốt",
         "two short green arms in front of the body, each a round green shoulder, a green leaf-shaped hand and a crown of "
         "big gold claws pointing down: the viewer-left arm in front of the lower belly, the viewer-right arm in front of "
         "the C-shaped coil",
         "two short deep azure-teal dragon arms: round shoulders (the TOP ends, joining the body), hands with cream-yellow "
         "palms, and big curved coral-gold claws in the same places and shapes as the old gold claws"),
       G("N05", [33, 15, 12, 16, 22, 27], "doi", "golden back spikes", "gai lưng vàng",
         "silver-and-gold armor pieces with red rune marks: a big winged plate with backward spikes over the body on the "
         "viewer-left of the neck, a spiky plate on the viewer-right shoulder, a long thin blade and a curved band on the "
         "top coil, and two small blades on the viewer-left coil",
         "golden dorsal spikes and fins of the dragon in the same places: the big winged plate becomes a fan of sharp "
         "golden spikes (a dorsal fin) pointing back the same way, the shoulder plate a smaller fan of golden spikes, the "
         "blade and the band two golden spike ridges on the top coil, the two small blades two short golden spikes; flat "
         "warm gold with a few darker gold lines; no silver, no red marks, no armor",
         joint="base of each spike fan or ridge (where it touches the body)"),
       G("N06", [8], "doi", "tail with a white tuft", "đuôi chóp túm lông trắng",
         "a thin dark-green tail rising on the viewer-right from behind the coils, its tip holding a gold ring ornament "
         "around a glowing white orb",
         "a deep azure-teal dragon tail with a cream-yellow underside rising the same way, its tip ending in a flowing white "
         "hair tuft with a small flat lemon-yellow zigzag lightning bolt, where the old ring is; no ring, no orb, no glow",
         joint="lower end of the tail (behind the coils)"),
       G("N07", [30, 6, 28, 18, 10, 9, 24, 31], "doi", "storm clouds", "mây giông",
         "puffy cyan-blue clouds with long thin trailing streaks around the dragon (a long one at the bottom, small ones at "
         "the upper viewer-left, viewer-left, viewer-right and upper viewer-right) and two big mint-green-and-yellow wind "
         "swirl clouds in front of the lower coils",
         "storm clouds in the same places and sizes: flat grey-purple cloud puffs with rounded curls and a white band along "
         "their edges, thin white trailing streaks; the two wind swirls become long flat grey-purple storm clouds with "
         "white rims; no cyan, no mint, no yellow",
         joint="the clouds stay where they are"),
       G("N08", [35, 34], "doi", "lightning bolts", "tia sét",
         "cyan water splashes: a bigger splash on the viewer-right of the body and a few small cyan splatter bits inside "
         "the big loop on the viewer-left",
         "flat lemon-yellow zigzag lightning bolts in the same places: one bigger bolt on the viewer-right, two or three "
         "small bolts on the viewer-left; flat colour with the dark ink outline, no glow, no white core, no sparks",
         joint="the bolts stay where they are")],
      keep=[1, 2, 3, 4], drop=[5, 7, 36], prev="thanh_long_1",
      anim=dict(root=19, head=32, swing=[21, 17], wob=[8, 20], fly=[], cast=(32, 0.8, 0.92),
                parent={32: 19, 20: 32, 11: 19, 13: 11, 14: 13, 8: 14, 26: 21, 29: 26, 23: 17, 25: 23,
                        12: 13, 16: 13, 22: 11, 27: 11, 15: 17}),
      note="1 bóng, 2-4 vòng gợn trắng (cùng c2): giữ; 5 gợn nước, 7 vệt gió tím, 36 quầng đỏ trên ngực: bỏ; "
           "đầu là một mảnh (mặt, mào, sừng liền) nên đổi dáng; mây 10, 18 chung c116"),
]
