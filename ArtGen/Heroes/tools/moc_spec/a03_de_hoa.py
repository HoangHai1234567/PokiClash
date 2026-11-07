# Dê Hoa (ải 10, Khá): dê sừng cành, vương miện cúc. Người dùng chốt concept bằng chữ 2026-11-07.
# Gốc: 866 cừu con lông xanh lá như bụi cây, sừng xoắn nâu nhạt, hoa hồng to; 867 lớn hơn, hoa loa kèn hồng có tua vàng;
#      868 dê thon trắng bờm lá xanh, giáp vàng, sừng xoắn có hoa.
# Mới: lông kem xù, mặt nâu hạt dẻ, sừng là cành gỗ nâu sẫm có chồi lá non, vương miện hoa cúc vàng, móng nâu sẫm.
DH_COL = ("fluffy warm cream wool, a chestnut-brown face with a small pale cream muzzle, dark-brown wooden twig horns with small "
          "fresh light-green leaf buds, yellow daisies with orange-brown centres, dark-brown hooves, big honey-amber eyes")
DH_AV = ("green or bush-like wool, round curled light-tan ram horns, roses, lilies, pink or pastel-pink flowers, curly yellow-green "
         "stamens or antennae, gold armour or gold rings, an all-white or all-cream face")
DH1 = "image 6 (the round goat kid)"

SPEC = [
    # ---- dạng 1: rig #866, cừu con nằm bẹp, mặt trước, ba chân thò dưới bụng
    F("de_hoa_1", 866, "Dê Hoa", 1, 3, "Dê Hoa Con", "ải 10 đảo Mộc, dạng 1/3",
      "dê con tròn nằm bẹp: lông kem xù, mặt nâu hạt dẻ mõm kem, hai sừng cành gỗ nâu sẫm ngắn có chồi lá non, vương miện "
      "nhỏ ba bốn bông cúc vàng thay hoa hồng, ba bàn chân móng nâu sẫm, mắt hổ phách",
      "a round woolly GOAT KID with twig horns and a daisy crown, the first stage of a three-stage Wood evolution line",
      "crouched low on its belly with its little hooves tucked under, head facing forward",
      "a stubborn little goat kid ready to head-butt: brows angled down, a small determined grin with a tiny fang",
      DH_COL, DH_AV,
      [G("N01", [8, 18, 17], "giu", "face", "mặt",
         "a wide rounded cream face patch at the front of the woolly body, with two big pink-red eyes, a small tan nose and a "
         "tiny mouth",
         "a wide rounded goat-kid face: chestnut brown with a small pale cream muzzle patch around the nose and mouth, two big "
         "honey-amber eyes (one catchlight dot each) exactly where the old eyes are, brows angled down, a small determined "
         "grin with a tiny fang",
         hide=[18, 17]),
       G("N02", [3, 2, 5, 9, 11, 13], "giu", "woolly fleece body", "khối lông xù (thân)",
         "the bush-like green wool that makes the whole body: a big rounded fleece over the back and top, a curly tuft behind "
         "on the viewer-left, two side tufts on the viewer-left and one on the viewer-right next to the face, and a curly "
         "wool fringe across the top of the face",
         "fluffy warm cream wool with soft scalloped curls and the same outline: the back fleece, the side tufts and the "
         "fringe on top of the face all cream wool; no green, no leaves"),
       G("N03", [15, 10, 14, 12], "doi", "two twig horns", "hai sừng cành",
         "two curled light-tan ram horns on both sides of the head: a big one on the viewer-left and a smaller one on the "
         "viewer-right, each with a dark-brown root piece hidden under the wool fringe",
         "two short dark-brown wooden twig horns growing from the same places, one on each side: each a stubby crooked branch "
         "with one small fork and one or two tiny fresh light-green leaf buds, pointing outward like the old horns; no curls, "
         "no tan",
         joint="root of each horn (the end hidden under the wool fringe, next to the head)"),
       G("N04", [16], "doi", "daisy crown", "vương miện cúc",
         "a big pink four-petal flower with a dark pink centre sitting on top of the head",
         "a small crown of three or four yellow daisies with orange-brown centres and a couple of small olive leaves, sitting "
         "on top of the head in the same place, about the same size; no pink, no rose",
         joint="bottom centre of the crown, where it sits on the wool on top of the head"),
       G("N05", [7, 4, 6], "giu", "three small feet", "ba bàn chân",
         "three small cream oval feet peeking out under the wool: two on the viewer-left (front and back) and one on the "
         "viewer-right",
         "three small stubby feet: cream fur with dark-brown hoof tips (a small split-hoof line)")],
      keep=[1],
      anim=dict(root=3, head=8, swing=[], wob=[9, 11, 2], fly=[], cast=(8, 0.62, 0.8),
                parent={13: 8, 9: 8, 11: 8, 15: 8, 10: 8, 14: 8, 12: 8, 16: 8}),
      note="2, 5, 9, 11 túm lông; 13 mái lông trên mặt (nối vào đầu); 10, 12 gốc sừng nằm dưới mái lông"),

    # ---- dạng 2: rig #867, cừu đứng bốn chân, mặt trước, đuôi ló sau lưng
    F("de_hoa_2", 867, "Dê Hoa", 2, 3, "Dê Gỗ", "ải 10 đảo Mộc, dạng 2/3",
      "dê đứng bốn chân: lông kem dày hơn, mặt nâu hạt dẻ mõm kem, sừng cành gỗ nâu sẫm dài hơn có nhánh và chồi lá non, "
      "vương miện cúc vàng to có vòng lá ô liu, đuôi lông kem chóp nâu, móng nâu sẫm, mắt hổ phách",
      "a sturdy woolly WOOD GOAT with a thicker cream fleece, longer twig horns and a big daisy crown with leaves, the SECOND "
      "stage of a three-stage Wood evolution line whose first stage is " + DH1,
      "standing square on four sturdy legs, head facing forward, ready to charge",
      "a tough young goat ready to ram: brows angled down, a determined grin with a tiny fang",
      DH_COL + ", olive-green leaves in the crown", DH_AV,
      [G("N01", [11], "giu", "face", "mặt",
         "a round cream face at the front under the wool fringe, with two big dark-red eyes and a tiny peach nose",
         "a round goat face: chestnut brown with a small pale cream muzzle, two big honey-amber eyes (one catchlight dot each) "
         "exactly where the old eyes are, brows angled down, a determined small grin with a tiny fang"),
       G("N02", [7, 5, 10, 16, 14, 12], "giu", "thick woolly fleece", "lông xù dày",
         "the bush-like green wool: a large rounded fleece covering the back and top behind the head, a side tuft behind it on "
         "each side (viewer-left and viewer-right), a scalloped wool fringe across the top of the face and two small locks "
         "hanging beside the face",
         "thick fluffy warm cream wool with soft scalloped curls and the same outline: the back fleece, side tufts, fringe and "
         "the two locks beside the face all cream wool; no green, no leaves"),
       G("N03", [4], "giu", "chest", "ngực (thân)",
         "a cream oval chest mostly hidden behind the face; only a band shows under the face",
         "a warm cream furry chest, same outline"),
       G("N04", [8, 9, 2, 3], "giu", "four legs", "bốn chân",
         "four straight cream legs: two front legs in front (viewer-left and viewer-right) and two back legs behind them; TOP "
         "end = shoulder or hip under the body, BOTTOM end = foot on the ground",
         "four sturdy goat legs with the same outline: cream fur, each ending at the BOTTOM in a dark-brown split hoof"),
       G("N05", [15, 13], "doi", "two twig horns", "hai sừng cành",
         "two big curled tan ram horns on both sides of the head, curling outward and down (the viewer-left one bigger)",
         "two dark-brown wooden twig horns growing from the same places, longer than the first stage: each a crooked branch "
         "sweeping outward and up with one or two short side twigs and small fresh light-green leaf buds; no curls, no tan",
         joint="base of each horn, where it meets the side of the head (the inner end, next to the wool fringe)"),
       G("N06", [17], "doi", "big daisy crown", "vương miện cúc to",
         "a big pink lily flower on top of the head with two long curly yellow-green stamens rising from it",
         "a big crown of five or six yellow daisies with orange-brown centres set in a ring of olive-green leaves, sitting on "
         "top of the head in the same place; no stamens, no antennae, no pink",
         joint="bottom centre of the crown, where it sits on top of the head"),
       G("N07", [6], "doi", "short tail", "đuôi ngắn",
         "a short cream tail sticking up behind the back, its green base hidden behind the wool, the tip curling to the "
         "viewer-right",
         "a short perky goat tail of cream wool with a chestnut-brown tip, sticking up behind the back in the same place",
         joint="bottom end of the tail (where it joins the back, hidden behind the fleece)")],
      keep=[1], prev="de_hoa_1",
      anim=dict(root=4, head=11, swing=[], wob=[6, 14, 12], fly=[], cast=(11, 0.6, 0.88),
                parent={16: 11, 14: 11, 12: 11, 15: 11, 13: 11, 17: 11}),
      note="11 mặt đã vẽ sẵn mắt mũi (không có mảnh mắt riêng); 6 đuôi ló sau lưng; 14, 12 lọn lông cạnh mặt"),

    # ---- dạng 3: rig #868, dê núi thon đứng nghiêng 3/4 quay phải
    F("de_hoa_3", 868, "Dê Hoa", 3, 3, "Dê Sừng Chiến", "ải 10 đảo Mộc, dạng 3/3",
      "dê núi thon đứng nghiêng: lông kem, mặt nâu hạt dẻ mõm kem, bờm lá ô liu và vàng chanh dọc cổ và lưng, sừng cành gỗ "
      "nâu sẫm phân nhánh như gạc có chồi lá non, vòng cúc vàng trên đầu, giáp ngực vỏ cây chạm lá thay giáp vàng, móng nâu "
      "sẫm, mắt hổ phách",
      "a slim MOUNTAIN GOAT warrior with branching twig antlers, a leaf mane and a bark chest guard, the THIRD stage of a "
      "three-stage Wood evolution line whose first stage is " + DH1,
      "standing tall on four slim legs, body turned to the viewer-right, head raised",
      "a proud goat warrior ready to charge: brow angled down, a calm confident half-smile",
      "warm cream fur, a chestnut-brown face with a pale cream muzzle, a mane of olive-green and lime-yellow leaves, "
      "dark-brown wooden twig antlers with small fresh light-green leaf buds, a ring of yellow daisies with orange-brown "
      "centres, a grey-brown tree-bark chest guard with a carved olive leaf, dark-brown hooves, honey-amber eyes",
      DH_AV + ", peach-tinted leaves",
      [G("N01", [13, 31], "giu", "head with face", "đầu có mặt",
         "a slim goat head turned to the viewer-right: green hair over the top and forehead running down the nose bridge, a "
         "cream cheek and jaw, the muzzle pointing down-right, one pink-red eye",
         "a slim goat head: chestnut-brown face with a pale cream muzzle tip and chin, a small olive leaf forelock on top "
         "where the old green hair starts, one honey-amber eye (one catchlight dot) exactly where the old eye is, brow angled "
         "down, mouth in a confident half-smile",
         hide=[31]),
       G("N02", [10, 11, 18], "giu", "slim body and neck", "thân và cổ",
         "the slim goat body: a cream torso with a green leafy top, a long neck rising to the head (green on its back edge, "
         "white at the front) and a round haunch at the back with a green top",
         "a slim mountain-goat body with the same outline: warm cream fur; the green tops of the torso, neck and haunch become "
         "olive-green and lime-yellow leaves (part of the leaf mane); the front of the neck and the chest cream"),
       G("N03", [30, 3, 26, 27, 28, 24], "doi", "leaf mane on the neck and back", "bờm lá cổ và lưng",
         "green leaf tufts tipped with peach and yellow: a big leaf crest along the top of the neck behind the head, one leaf "
         "hanging at the front of the neck on the viewer-right, and four leafy pieces lying on the back and the haunch",
         "a mane of olive-green and lime-yellow leaves (each leaf one flat colour) in the same places and pointing the same "
         "way; no peach, no gradients",
         joint="inner edge of each leaf tuft, where it lies on the neck or the back"),
       G("N04", [29, 25, 2], "doi", "bark chest guard", "giáp ngực vỏ cây",
         "a big gold chest armour plate with a swirl emblem hanging in front of the chest, and two thin gold straps: one "
         "behind the neck on the viewer-left, one at the viewer-right edge of the neck",
         "a chest guard of grey-brown tree bark with a leaf carved on it (the carved leaf olive green), hung by two bark straps "
         "in the same places, about the same size; no gold, no metal",
         joint="top of the chest guard and of each strap, where they hang around the neck"),
       G("N05", [35, 34, 14, 12, 16, 15], "doi", "branching twig antlers", "sừng cành phân nhánh",
         "two big curled ram horns: the near horn in three pieces (a back piece over the top of the head, a big coil with a "
         "gold ring on the viewer-left, a hooked tip under the coil) and the far horn coiled behind the head on the "
         "viewer-right; plus two thin curly light-green sprouts rising from the top of the head",
         "branching wooden twig antlers like a deer's: each horn becomes a dark-brown branch sweeping back and up with forked "
         "tines and small fresh light-green leaf buds, and the two sprouts become two extra thin dark-brown twig tines with a "
         "leaf bud at the tip, rising from the top of the head; no curls, no gold ring",
         joint="base of each horn and each twig, where it grows from the top of the head"),
       G("N06", [33], "doi", "daisy ring", "vòng cúc",
         "a pink lily flower with a yellow-green bud in the middle, on top of the head in front of the horns",
         "a ring of yellow daisies with orange-brown centres and a few olive leaves, sitting on top of the head between the "
         "antlers in the same place; no pink",
         joint="centre of the ring, where it sits on the head"),
       G("N07", [17], "doi", "tail", "đuôi",
         "a long cream tail with a green leafy base, pointing back to the viewer-left, the tip sweeping up",
         "a short tufted goat tail of cream wool with an olive leaf at the tip, pointing back to the viewer-left the same way",
         joint="viewer-right end of the tail, where it joins the haunch"),
       G("N08", [22, 21, 20, 19, 8, 7, 4, 5], "giu", "four slim legs", "bốn chân thon",
         "four slim cream legs, each in two pieces (upper and lower): two near legs in front of the body (the front leg at "
         "the centre, the back leg at the far viewer-left) and two far legs behind the body; TOP end = shoulder or hip under "
         "the body, BOTTOM end = ankle where the hoof starts",
         "four slim goat legs with the same outline, warm cream fur; no leaves"),
       G("N09", [23, 32, 9, 6], "doi", "four hooves", "bốn móng",
         "four green leaf-shaped hoof covers at the bottom of the legs, each sticking out sideways like a leaf",
         "four small dark-brown split goat hooves at the bottom of the legs, in the same places; no leaves",
         joint="top of each hoof, where it meets the bottom of the leg")],
      keep=[1], prev="de_hoa_1",
      anim=dict(root=10, head=13, swing=[], wob=[17, 16, 15], fly=[], cast=(13, 0.9, 0.88),
                parent={30: 11, 3: 11, 35: 13, 34: 13, 14: 13, 12: 13, 16: 13, 15: 13, 33: 13,
                        21: 22, 23: 21, 19: 20, 32: 19, 7: 8, 9: 7, 5: 4, 6: 5}),
      note="sừng gần = 14 (sau đỉnh đầu) + 34 (cuộn có vòng vàng) + 35 (móc dưới); 12 sừng xa; 15, 16 tua chồi thành nhánh gạc; "
           "chân gần 22/21 (trước), 20/19 (sau); chân xa 8/7 (trước), 4/5 (sau); 18 mông"),
]
