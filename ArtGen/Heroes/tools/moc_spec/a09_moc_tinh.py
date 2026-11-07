# Mộc Tinh (ải 60, Sử thi): cáo, sói pha lê lục. Người dùng chốt concept bằng chữ 2026-11-07.
# Gốc: 1480 mèo cáo xanh lá tai cam, mắt đỏ, đuôi lá, quả mọng đỏ ở cổ;
#      1481 sư sói lông trắng xù, cánh lá xanh, sừng nâu, hoa văn nâu.
# Mới: lông xám đá phiến, bụng kem, pha lê ngọc lục bảo (tô phẳng, không lấp lánh) mọc ở tai, đuôi, lưng, mắt vàng chanh;
#      dạng 1 cáo con tai to có cụm pha lê, đuôi mang lá pha lê; dạng 2 sói pha lê: cánh thành dải pha lê, sừng pha lê,
#      bờm xám bạc.
MT_COL1 = ("slate-grey fur, a cream belly, face mask and ear insides, flat emerald-green crystals with a few darker emerald "
           "facet lines (no sparkle), a dark-brown root cord, lemon-yellow eyes")
MT_COL2 = ("slate-grey fur, a cream belly and muzzle, a silver-grey mane, flat emerald-green crystal horns, wing blades and "
           "shards with a few darker emerald facet lines (no sparkle), lemon-yellow eyes")
MT_AV = ("a green body, orange ears, red eyes, white fur, brown horns, leaves on a stem, a red berry, a glowing magic circle "
         "on the ground, a gold crown, glowing green flame wisps, sparkles, crystal shine")

SPEC = [
    F("moc_tinh_1", 1480, "Mộc Tinh", 1, 2, "Tiểu Mộc Tinh", "ải 60 đảo Mộc, dạng 1/2",
      "cáo con lông xám đá phiến, mặt nạ và bụng kem, tai to xám lòng kem, sau mỗi tai một cụm pha lê lục bảo, chỏm lông "
      "xoăn trên đầu, vòng rễ cây nâu sẫm đeo mặt pha lê ở cổ, đuôi xù mang lá pha lê lục, mắt vàng chanh",
      "an EMERALD-CRYSTAL FOX CUB, the first stage of a two-stage Wood evolution line",
      "standing on four short legs",
      "a bold little fox ready to pounce: brows angled down, a small fang in a confident grin",
      MT_COL1, MT_AV,
      [G("N01", [15, 25, 13, 29, 30, 21, 32, 31, 20, 28], "giu", "round head with face", "đầu tròn có mặt",
         "a big round green head with a white face mask in front, a yellow leaf symbol on the forehead and small yellow "
         "marks, two big red eyes (a wide one on the viewer-left and a narrow one on the viewer-right), a tiny nose, a "
         "wide open laughing mouth with a pink tongue, and small green cheek tufts on both sides at the bottom (the "
         "viewer-left one longer)",
         "a round fox-cub head: slate-grey fur on top and sides, a cream face mask around the eyes and muzzle, two big "
         "lemon-yellow eyes (one catchlight dot each) exactly where the old eyes are, brows angled down, a small dark "
         "nose, a confident grin with one tiny fang (smaller than the old open mouth); slate-grey cheek fluff with cream "
         "tips where the old green tufts are; no forehead symbol, no red",
         hide=[29, 30, 21, 32, 31, 20, 28]),
       G("N02", [27, 17, 18, 4, 16], "doi", "big fox ears with emerald crystal clusters", "tai cáo to và cụm pha lê",
         "on the viewer-left a big orange pointed ear in front of a huge green-and-orange leaf crest sweeping up-left; on "
         "the viewer-right a small orange ear in front of a tall green leaf standing up; a curled green leaf sprout on "
         "top of the head",
         "two big pointed fox ears, slate grey outside and cream inside, where the orange ears are; behind each ear a "
         "cluster of flat emerald-green crystal shards growing from the head, sweeping up-left on the viewer-left and "
         "standing up on the viewer-right, about the size of the old leaves, with a few darker emerald facet lines; a "
         "small curled slate-grey fur tuft on top of the head; no leaves, no orange",
         joint="base of each ear, crystal cluster and the tuft (where it grows from the head)"),
       G("N03", [9], "giu", "small body", "thân nhỏ",
         "the small green body under the head with tan patches on the belly, mostly hidden behind the head and the scarf",
         "a small slate-grey body with a cream belly and a few small flat emerald crystal shards along its back"),
       G("N04", [26, 12, 14, 22, 23], "doi", "root collar with crystal pendant", "vòng rễ cây và mặt pha lê",
         "a dark-green vine wrapped across the neck like a scarf with a yellow-orange band in the middle, its "
         "viewer-left end looping up behind the cheek, its viewer-right end curling into a spiral, and a red berry "
         "hanging at the front with three small green leaves on top",
         "a thin twisted dark-brown root cord following the same path across the neck, with the same loop on the "
         "viewer-left and curl on the viewer-right; instead of the berry a flat emerald crystal pendant with three tiny "
         "emerald chips on top; no red berry, no leaves, no yellow band",
         joint="the cord stays on the neck along the same path"),
       G("N05", [10, 11, 19, 24, 6, 7, 8], "giu", "four short legs", "bốn chân ngắn",
         "four short stubby green legs under the body, each with a tan paw at its BOTTOM end: one on the viewer-left, "
         "two in the middle (one behind the other) and one on the viewer-right",
         "four short slate-grey legs with cream paws at the bottom and small dark toe lines; no green, no tan"),
       G("N06", [5], "doi", "bushy tail with a crystal leaf", "đuôi xù mang lá pha lê",
         "a long tail: a dark-brown stem growing from the rump at its lower-right end, curling into small teal tendrils, "
         "ending at the upper-left in a big teal leaf",
         "a bushy slate-grey fox tail curving up from the rump to the upper-left, carrying a big flat emerald crystal "
         "leaf at its tip with a few darker emerald facet lines; no stem, no tendrils, no teal leaf",
         joint="the lower-right end where the tail joins the rump")],
      keep=[1], drop=[2, 3],
      anim=dict(root=9, head=15, swing=[], wob=[27, 18, 5], fly=[], cast=(15, 0.65, 0.9),
                parent={27: 15, 17: 15, 18: 15, 4: 15, 16: 15, 11: 10, 24: 19, 8: 7}),
      note="2, 3 vòng phép dưới chân (chung c123): bỏ; 6 là chân sau có sẵn bàn chân; 25, 13 túm má"),
    F("moc_tinh_2", 1481, "Mộc Tinh", 2, 2, "Mộc Tinh", "ải 60 đảo Mộc, dạng 2/2",
      "sói pha lê: lông xám đá phiến, mõm và bụng kem, bờm xù xám bạc, hai sừng pha lê lục bảo, cánh thành dải pha lê lục, "
      "pha lê dọc lưng và ở đùi sau, đuôi xù mang chùm lá pha lê, mắt vàng chanh",
      "an EMERALD-CRYSTAL WOLF, the SECOND stage of a two-stage Wood evolution line whose first stage is image 6: the "
      "emerald-crystal fox cub",
      "crouched low on four legs ready to pounce",
      "a fierce but cute crystal wolf about to pounce: brow angled down, a confident snarl-grin with small fangs",
      MT_COL2, MT_AV,
      [G("N01", [16], "doi", "head with face and crystal horns", "đầu có mặt, sừng pha lê",
         "a lion-wolf head turned to the viewer-right: a white snout with small fangs at the lower-right, one red eye, a "
         "gold crown on the forehead with a glowing green flame wisp in front of it, a green pointed ear with an orange "
         "inside at the lower-left, and two huge curved brown horns with gold flame marks sweeping up and back over the "
         "head",
         "the grown-up crystal wolf head: slate-grey head, a cream muzzle with small fangs, one lemon-yellow eye (one "
         "catchlight dot) exactly where the old eye is, a brow angled down, a confident snarl-grin; a slate-grey pointed "
         "ear with a cream inside where the green ear is; the two horns become two big curved horns of flat "
         "emerald-green crystal with a few darker emerald facet lines, the same places and sweep; no crown, no glow, no "
         "flame wisp, no brown",
         joint="the lower end of the head where it meets the mane"),
       G("N02", [15], "doi", "silver-grey mane", "bờm xám bạc",
         "a big fluffy pale-teal and white mane around the neck and chest with spiky fur tufts, under the head",
         "a big fluffy silver-grey mane with the same spiky tufts, the tuft tips a lighter silver grey (flat colours, no "
         "white, no teal)",
         joint="where the mane wraps the neck under the head"),
       G("N03", [8], "giu", "body with crystal back", "thân, pha lê dọc lưng",
         "the long horizontal green body, the back hump at the viewer-left and the chest at the viewer-right under the "
         "mane, pale teal belly",
         "a slate-grey body with a cream belly and a row of small flat emerald crystal shards along the back"),
       G("N04", [12, 7, 10, 9, 4, 3, 13, 14], "giu", "four legs", "bốn chân",
         "four legs in a crouching pose, each with orange claws at the paw: at the rear (viewer-left) a round green "
         "haunch with two orange leaves and a yellow spot, and under it a hind leg going down with its paw at the BOTTOM; "
         "in the middle a green shoulder with a yellow spot and under it a straight leg with a big paw at the BOTTOM; "
         "behind it a darker far leg partly hidden, its paw at the BOTTOM; at the front a green shoulder under the mane "
         "and a front leg stretched forward to the viewer-right with its paw at the RIGHT end",
         "slate-grey legs in the same places with cream lower legs and paws and short dark-grey claws; the two orange "
         "leaves on the haunch become two flat emerald crystal shards; no orange, no yellow spots, no brown stripes"),
       G("N05", [11, 5], "doi", "two wings of emerald crystal blades", "hai cánh dải pha lê lục",
         "two leaf wings growing from the back: a big near wing of long green leaves fanning up and to the upper-left, "
         "and a dark-green far wing of pointed leaves standing up behind the head",
         "the wings become fans of long flat emerald-green crystal blades like ribbons, each blade with a darker emerald "
         "facet line down the middle, fanned out the same way; no leaf veins, no glow, no sparkle",
         joint="the bottom end of each wing (wing root on the back)"),
       G("N06", [6], "doi", "bushy tail with crystal leaves", "đuôi xù mang lá pha lê",
         "a big fluffy pale-teal and white tail curling up at the viewer-left, behind the body",
         "a big bushy slate-grey tail with a cream tip, carrying a cluster of flat emerald crystal leaves near the tip; "
         "no white, no teal",
         joint="the lower-right end where the tail joins the rump")],
      keep=[1], drop=[2, 17], prev="moc_tinh_1",
      anim=dict(root=8, head=16, swing=[14], wob=[11, 5, 6], fly=[], cast=(16, 0.72, 0.92),
                parent={9: 10, 7: 12, 3: 4, 14: 13}),
      note="2, 17 vòng phép (chung c5): bỏ; đầu 16 là một mảnh (mắt, tai, sừng, vương miện, lửa xanh) nên không có mảnh ẩn; "
           "3, 4 là chân xa (tô sẫm)"),
]
