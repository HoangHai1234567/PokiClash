# Tiên Lá (ải 1, Thường): đom đóm rêu. Người dùng chốt concept bằng chữ 2026-11-07.
# Gốc: 648 thú trắng tóc lá xanh vàng, cầu sáng xanh lơ trên râu, tai cánh xanh lơ, vòng cỏ ba lá; 649 lớn hơn; 650 tiên cánh lá.
# Mới: lông kem, mũ trùm rêu xanh mép lá ô liu, đèn đom đóm hổ phách trên râu, cánh cứng nâu hạt dẻ chấm vàng, mắt nâu hạt dẻ.
TL_COL = ("warm cream fur on the face and belly, a moss-green hood with olive leaf-shaped tips, chestnut-brown beetle wing "
          "cases with small yellow dots, a flat amber-yellow firefly lantern, big dark chestnut-brown eyes")
TL_AV = ("a white face with a green-and-yellow hair streak, cyan or turquoise ears or wings, clover leaves, a glowing ball, "
         "light rays, a ring or swoosh around the body")

SPEC = [
    F("tien_la_1", 648, "Tiên Lá", 1, 3, "Thú Ánh Lục", "ải 1 đảo Mộc, dạng 1/3",
      "đom đóm con tròn: lông kem, mũ trùm rêu xanh mép lá ô liu, râu mang đèn đom đóm hổ phách, hai cánh cứng nâu hạt dẻ chấm vàng thay tai, mắt nâu hạt dẻ",
      "a round FIREFLY PUP of the forest-light line, the first stage of a three-stage Wood evolution line",
      "sitting low on the ground", "a brave little firefly ready to charge: brows angled down, a small fang showing",
      TL_COL, TL_AV,
      [G("N01", [8, 12, 13, 9, 10], "giu", "round head-body with face", "khối đầu thân có mặt",
         "a big round white creature whose whole back and top are a spiky green-and-yellow hair crest, two big green eyes in "
         "the lower front and two small green dots on the forehead",
         "a round chubby firefly pup: warm cream face and belly in front, a moss-green hood covering the back and top with "
         "olive leaf-shaped tips along its spiky edge, two big dark chestnut-brown eyes (one catchlight dot each) exactly "
         "where the old eyes are, brows angled down, a small confident grin with a tiny fang; no forehead dots",
         hide=[12, 13, 9, 10]),
       G("N02", [11], "doi", "firefly lantern on its antenna", "đèn đom đóm trên râu",
         "a thin dark stalk growing up from the top of the head and ending in a big glowing cyan ball",
         "a thin dark-brown antenna stalk ending in a round firefly lantern bulb of flat amber-yellow with three darker "
         "amber segment lines; no glow, no light rays",
         joint="bottom end of the stalk (where it grows from the head)"),
       G("N03", [15, 14, 4], "doi", "two beetle wing cases", "hai cánh cứng",
         "two big cyan ear-like flaps on both sides of the head: a big one on the viewer-left with a small grey piece under "
         "it, and a small one on the viewer-right mostly hidden behind the head",
         "two hard beetle wing cases (elytra) sticking out on both sides like the old flaps: chestnut brown with small "
         "yellow dots and a thin olive rim, about the same size and place as the old flaps",
         joint="end of each wing case that touches the head"),
       G("N04", [5, 6, 7], "giu", "three small feet", "ba bàn chân",
         "three small stubby feet peeking out under the round body",
         "three small stubby feet in moss green with cream toe pads")],
      keep=[1], drop=[2, 3, 16, 17],
      anim=dict(root=8, head=8, swing=[], wob=[15, 4, 11], fly=[], cast=(11, 0.5, 0.45)),
      note="2, 16 cỏ ba lá (chung hình c5), 3, 17 vòng xoáy: bỏ"),
    F("tien_la_2", 649, "Tiên Lá", 2, 3, "Linh Ánh Lục", "ải 1 đảo Mộc, dạng 2/3",
      "đom đóm lớn bay lơ lửng: mặt, bụng kem; mũ rêu dài thành mào lá nhọn mép ô liu, chóp mào cong thành râu mang đèn đom đóm hổ phách to hơn; lưng mai cánh cứng nâu hạt dẻ chấm vàng; đôi cánh mỏng xanh bạc hà gân ô liu; tay chân xanh rêu đệm kem; mắt nâu hạt dẻ",
      "a FIREFLY SPRITE with a long leafy moss crest and a bigger amber lantern, the SECOND stage of a three-stage Wood "
      "evolution line whose first stage is image 6: a round firefly pup with a moss hood",
      "hovering just above the ground on its thin wings, arms and legs hanging loose",
      "a brave young firefly ready to dart in: brows angled down, a small fang showing in a confident grin",
      TL_COL + ", thin wings of flat mint green (a soft green, not cyan) with fine olive veins",
      TL_AV + ", a spiky green-and-yellow hair crest, a lime-green leaf on the forehead, see-through glassy wings",
      [G("N01", [11, 13, 17, 18, 14, 15, 16], "giu", "head with face and leafy moss crest", "đầu có mặt và mào lá rêu",
         "a big head: a white face in front and a huge spiky green-and-yellow hair crest sweeping back to the viewer-left, "
         "whose long top tip curls up and over to the viewer-right like a stalk; a lime-green leaf lies on the top right of "
         "the head; two big green eyes, a small pink mouth and two small green dots on the forehead",
         "warm cream face in front; the hair crest becomes a long moss-green hood of pointed leaves with olive leaf-shaped "
         "tips, sweeping back to the viewer-left in the same spiky outline; its long top tip is a curling moss-green stalk "
         "with a dark-brown core line that ends where the lantern hangs (do NOT draw the lantern here); the lime leaf "
         "becomes one more olive leaf lying flat on the hood; two big dark chestnut-brown eyes (one small catchlight dot "
         "each) exactly where the old eyes are, brows angled down, a small confident grin with a tiny fang where the old "
         "mouth is; no forehead dots",
         hide=[13, 17, 18, 14, 15, 16]),
       G("N02", [12], "doi", "big firefly lantern", "đèn đom đóm to",
         "a big glowing cyan ball with a white centre at the end of the curling top tip of the head crest",
         "a big round firefly lantern bulb of flat amber-yellow with three darker amber segment lines and a small "
         "dark-brown cap where it meets the stalk, a little bigger than the old ball; no glow, no light rays, no white "
         "centre",
         joint="the viewer-left side of the bulb, where the curling stalk ends"),
       G("N03", [8, 6], "doi", "two thin wings", "đôi cánh mỏng",
         "two see-through cyan butterfly wings behind the body: a bigger one on the viewer-left reaching up-left, a "
         "smaller one on the viewer-right partly hidden behind the body",
         "two thin firefly wings of flat mint green (a soft green, not cyan) with fine olive veins and a thin olive rim, "
         "the same two-lobed shapes and places as the old wings; opaque flat colour, no transparency, no glow",
         joint="end of each wing that touches the back of the body"),
       G("N04", [9], "giu", "body with beetle shell", "thân có mai cánh cứng",
         "a small egg-shaped body under the head: white belly in front, a green-and-yellow band down its viewer-left "
         "side (the back)",
         "warm cream belly in front; the green-and-yellow band becomes a chestnut-brown beetle shell with small yellow "
         "dots and a thin olive rim covering the back on the viewer-left side"),
       G("N05", [10, 7], "giu", "two small arms", "hai tay nhỏ",
         "two thin arms hanging down: the viewer-left one in front of the belly, the viewer-right one at the side; the "
         "TOP end of each is the shoulder, the green BOTTOM end is the hand",
         "two short moss-green arms, shoulder at the TOP end, a small cream paw at the BOTTOM end"),
       G("N06", [4, 5], "giu", "two small legs", "hai chân nhỏ",
         "two short oval legs hanging under the body, the hip at the TOP end and a green foot tip at the BOTTOM end",
         "two short moss-green legs, hip at the TOP end, a cream toe pad at the BOTTOM end")],
      keep=[1], drop=[2, 19, 3, 20], prev="tien_la_1",
      anim=dict(root=9, head=11, swing=[], wob=[8, 6, 12], fly=[], cast=(12, 0.5, 0.5), parent={12: 11}),
      note="2, 19 cỏ ba lá (chung hình c5), 3, 20 vệt xoáy: bỏ; 13 lá trên đầu gộp vào mào (ẩn)"),
    F("tien_la_3", 650, "Tiên Lá", 3, 3, "Tiên Lá", "ải 1 đảo Mộc, dạng 3/3",
      "hiệp sĩ đom đóm bay đứng thẳng: mặt kem, mũ rêu xanh như mũ giáp có ba lá mép ô liu, râu mang đèn đom đóm hổ phách; thân kem bọc giáp vỏ hạt dẻ chấm vàng; tay trái (người xem) cầm kiếm lá ô liu; bốn cánh mỏng bạc hà gân ô liu; chân giáp hạt dẻ, bàn chân xanh rêu; mắt nâu hạt dẻ",
      "a FIREFLY KNIGHT standing upright in chestnut shell armour, the THIRD stage of a three-stage Wood evolution line "
      "whose first stage is image 6: a round firefly pup with a moss hood",
      "hovering upright just above the ground on four thin wings, legs dangling, like a small knight on guard",
      "a proud little knight ready to strike: brows angled down, a confident grin with a small fang",
      "warm cream fur on the face, body and thighs, a moss-green hood with olive leaf-shaped tips, chestnut-brown "
      "beetle-shell armour with small yellow dots, a flat amber-yellow firefly lantern, big dark chestnut-brown eyes, "
      "four thin wings of flat mint green (a soft green, not cyan) with olive veins, an olive-green leaf blade",
      TL_AV + ", a fairy with cyan leaf-shaped wings, a yellow-gold body, a gold forehead gem with a crescent, a spiral "
      "around the antenna ball",
      [G("N01", [18, 20, 23, 21, 22, 27], "giu", "head with face and moss hood", "đầu có mặt và mũ rêu",
         "a big head: a white face in front and a spiky green-and-yellow hair crest over the top and back; two big green "
         "eyes, two small cyan marks beside the viewer-left eye, a small cyan mark and a gold oval gem with a cyan "
         "crescent near the viewer-right eye",
         "warm cream face in front; the hair crest becomes a moss-green hood shaped like a knight's helmet hood, with "
         "olive leaf-shaped tips along its spiky edge; two big dark chestnut-brown eyes (one small catchlight dot each) "
         "exactly where the old eyes are, brows angled down, a small confident grin with a tiny fang below them; no "
         "marks, no gem",
         hide=[20, 23, 21, 22, 27]),
       G("N02", [19, 17, 16], "doi", "three leaves of the hood crest", "ba lá mào mũ",
         "three green leaves on the head: a big one sticking out to the viewer-left over the forehead, a smaller one "
         "lying on the top right of the head, and a pale one behind the head at the top right",
         "three big moss-green leaves with olive tips and a dark-green midrib growing from the hood like a leafy helmet "
         "crest, about the same size, place and direction as the old leaves",
         joint="base of each leaf (where it grows from the hood)"),
       G("N03", [26, 25], "doi", "firefly lantern on its antenna", "đèn đom đóm trên râu",
         "a thin green-and-yellow stalk curving up from the top of the head, ending in a round cyan ball with a white "
         "centre",
         "a thin dark-brown antenna stalk with the same curve, ending in a big round firefly lantern bulb of flat "
         "amber-yellow with three darker amber segment lines; no glow, no spiral, no light rays, no white centre",
         joint="bottom end of the stalk (where it grows from the head)"),
       G("N04", [5, 7, 4, 6], "doi", "four thin wings", "bốn cánh mỏng",
         "four cyan leaf-shaped wings with pale veins behind the body: a big upper one and a small lower one on the "
         "viewer-left, an upper one and a small lower one on the viewer-right",
         "four thin firefly wings of flat mint green (a soft green, not cyan) with olive veins and a thin olive rim, "
         "slim oval dragonfly-like shapes in the same places and directions as the old wings; opaque flat colour, no "
         "transparency, no glow",
         joint="end of each wing nearest the back of the body"),
       G("N05", [12, 15], "giu", "armoured body", "thân giáp vỏ hạt dẻ",
         "a small body under the head: a yellow chest with a white belly patch, and a round yellow-brown neck disc "
         "under the chin",
         "a warm cream body in a breastplate of chestnut-brown beetle shell with a few small yellow dots and a thin olive "
         "rim, the cream belly showing in the middle; the neck disc is a plain cream neck"),
       G("N06", [14, 10], "giu", "two arms, one holding a leaf blade", "hai tay, một tay cầm kiếm lá",
         "two thin yellow arms, the TOP end of each is the shoulder: the viewer-left arm goes down-left with a big "
         "dark-green leaf along its lower side ending in a point at the lower left; the viewer-right arm goes down-right "
         "to a green hand at its BOTTOM end",
         "two cream arms in chestnut-brown shell gauntlets with small moss-green paws; the viewer-left paw holds a long "
         "olive-green leaf blade (a short leaf sword) lying along the forearm in the place of the old dark leaf, its "
         "point at the lower left; the viewer-right arm hangs down-right, paw clenched"),
       G("N07", [13, 8, 11, 9], "giu", "two legs", "hai chân",
         "two short yellow legs dangling under the body, each a thigh at the TOP and a shin below with a cyan foot at "
         "its BOTTOM end; the viewer-left leg is in front and longer, the viewer-right leg is thinner and partly behind",
         "two short legs: cream thighs, chestnut-brown shell greaves on the shins, small moss-green feet at the BOTTOM "
         "ends")],
      keep=[1], drop=[2, 28, 3, 29, 24], prev="tien_la_1",
      anim=dict(root=12, head=18, swing=[14], wob=[5, 7, 4, 6, 26], fly=[], cast=(25, 0.5, 0.5),
                parent={19: 18, 17: 18, 16: 18, 26: 18, 25: 26, 8: 13, 9: 11}),
      note="2, 28 cỏ ba lá (chung hình c5), 3, 29 vệt xoáy, 24 vòng xoáy quanh cầu: bỏ; 27 ngọc trán ẩn"),
]
