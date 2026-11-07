# Hoa Nhụy (ải 5, Thường): củ cải đỏ nở hoa trà. Người dùng chốt concept bằng chữ 2026-11-07.
# Gốc: 593 củ cải mầm xanh nhạt; 594 thú búp hoa có nụ hồng, cổ vòng hạt vàng; 595 tiên hoa dạng người đội hoa loa kèn hồng,
# chuông tím ở ngực, tóc xanh.
# Mới: củ cải đỏ thẫm bụng kem, lá xanh thẫm; dạng 2 áo lá, nụ hoa trà trắng; dạng 3 tiên củ cải đầu tròn mặt thú, hoa trà
# trắng nhụy đỏ thẫm, váy lá, hai tay cầm quả mọng đỏ.
HN_COL = ("deep crimson-red radish skin, a warm cream face-and-belly patch, dark forest-green leaves with olive midribs, "
          "big dark-brown eyes")
HN_AV = ("pale washed-out green, a pale green or whitish body, pink flowers or petals, purple bells, a human face or human "
         "hair, glowing dots, sparkles")

SPEC = [
    F("hoa_nhuy_1", 593, "Hoa Nhụy", 1, 3, "Thú Ba Lá", "ải 5 đảo Mộc, dạng 1/3",
      "củ cải con tròn: da đỏ thẫm, mảng kem phủ mặt và bụng, trên đầu ba lá xanh thẫm gân ô liu, bốn chân ngắn đỏ thẫm đệm kem, đuôi rễ đỏ thẫm chóp kem, mắt nâu sẫm",
      "a round RADISH PUP, the first stage of a three-stage Wood evolution line",
      "sitting low on four short stubby legs, leaning forward",
      "a tough little radish ready to charge: brows angled down, a confident open grin with a small fang",
      HN_COL, HN_AV + ", a light-green sprout body",
      [G("N01", [7, 9, 10, 8], "giu", "round radish head-body with face", "khối đầu thân củ cải có mặt",
         "a big round pale-green body that is head and body in one, with two big brown eyes in the upper half and a wide "
         "open pink mouth in the middle",
         "a round chubby radish: deep crimson-red skin on the top, back and sides, a big warm cream patch on the front "
         "holding the face and belly; two big dark-brown eyes (one small catchlight dot each) exactly where the old eyes "
         "are, brows angled down, a confident open grin with a small fang where the old mouth is",
         hide=[9, 10, 8]),
       G("N02", [4, 3, 5], "doi", "three leaves on top", "ba lá trên đầu",
         "three light-green leaves growing from the top of the body: a tall one in the middle, a small one on the "
         "viewer-right, a wide one leaning out to the viewer-left",
         "three sturdy radish leaves of dark forest green with an olive midrib and slightly wavy edges, the same sizes "
         "and directions as the old leaves",
         joint="base of each leaf (on top of the body)"),
       G("N03", [11], "giu", "two front legs", "hai chân trước",
         "two short pale-green front legs curling up over the bottom of the belly, joined in the middle at the bottom of "
         "the body",
         "two short stubby front legs in deep crimson red with cream toe tips, the same shape and place"),
       G("N04", [12, 6], "giu", "two hind feet", "hai chân sau",
         "two short round green feet under the body: one on the viewer-left in front, one on the viewer-right partly "
         "behind; the TOP end joins the body, the foot is at the BOTTOM end",
         "two short stubby feet in deep crimson red with cream toe pads"),
       G("N05", [2], "doi", "radish root tail", "đuôi rễ củ cải",
         "a small pointed leaf-shaped tail sticking out of the back of the body on the viewer-left",
         "a thin tapering radish root tail in deep crimson red with a cream tip, curving out like the old tail; not a "
         "leaf",
         joint="base of the tail (where it joins the body)")],
      keep=[1], drop=[13, 14],
      anim=dict(root=7, head=7, swing=[], wob=[4, 3, 5, 2], fly=[], cast=(7, 0.6, 0.56)),
      note="13, 14 chấm sáng (chung hình c21): bỏ"),
    F("hoa_nhuy_2", 594, "Hoa Nhụy", 2, 3, "Thú Búp Hoa", "ải 5 đảo Mộc, dạng 2/3",
      "củ cải lớn khoác áo lá: đầu tròn da đỏ thẫm mặt kem, chóp rễ nhọn bên trái; vương miện lá xanh thẫm, giữa là nụ hoa trà trắng đài xanh thẫm; áo lá xanh thẫm có cổ lá ô liu; mắt nâu sẫm",
      "a RADISH SPROUT in a leaf coat with a white camellia bud on its head, the SECOND stage of a three-stage Wood "
      "evolution line whose first stage is image 6: a round crimson radish pup",
      "standing squat, the hem of its leaf coat touching the ground",
      "a stubborn little radish guarding its bud: brows angled down, a confident grin with a small fang",
      HN_COL + ", a white camellia bud with a dark-green calyx",
      HN_AV + ", a pink lotus bud, a collar of yellow beads",
      [G("N01", [4, 3, 11, 8, 9, 10], "giu", "radish head with face", "đầu củ cải có mặt",
         "a big bulb-shaped head: a pale cream-green face in front, and behind it a darker olive layer of the same bulb "
         "whose pointed tip sticks out on the viewer-left; two big crimson eyes, two pink cheek marks and a small smile",
         "a round radish head: deep crimson-red skin on the top, the back and the pointed tip on the viewer-left (a "
         "short radish root tip), a warm cream face patch in front; two big dark-brown eyes (one small catchlight dot "
         "each) exactly where the old eyes are, brows angled down, a confident grin with a small fang where the old "
         "mouth is; no cheek marks",
         hide=[11, 8, 9, 10]),
       G("N02", [15], "doi", "leaf crown with a camellia bud", "vương miện lá và nụ hoa trà",
         "a big crown of light-green leaves on top of the head, some hanging over the forehead, with a closed pink "
         "lotus-like bud standing up in the middle",
         "a crown of dark forest-green leaves with olive midribs on top of the head, the front ones hanging over the "
         "forehead like the old ones, and in the middle a closed white camellia bud (rounded layered white petals with "
         "thin warm-grey lines, a dark-green calyx at its base); no pink",
         joint="bottom centre of the crown (where it sits on top of the head)"),
       G("N03", [2], "giu", "lower body", "thân dưới",
         "the rounded tan bottom of the body under the head, mostly hidden behind the leaf skirt",
         "the rounded bottom of the radish body: warm cream belly in front, deep crimson red at the sides"),
       G("N04", [14, 13, 12, 19, 18, 17, 16], "giu", "leaf coat", "áo lá",
         "a short coat of leaves: three big green leaves around the bottom of the body (one in front pointing down, one "
         "on each side), and a collar of four small yellow rounded pieces around the neck",
         "a leaf coat: the three bottom leaves are its skirt, dark forest green with olive midribs; the four collar "
         "pieces are small rounded olive-green leaf tips with dark-green edges forming the collar; no yellow beads")],
      keep=[1], drop=[5, 6, 7], prev="hoa_nhuy_1",
      anim=dict(root=2, head=4, swing=[], wob=[15], fly=[], cast=(4, 0.55, 0.79), parent={15: 4}),
      note="5, 6, 7 chấm sáng (chung hình c9): bỏ"),
    F("hoa_nhuy_3", 595, "Hoa Nhụy", 3, 3, "Tiên Hoa Nhụy", "ải 5 đảo Mộc, dạng 3/3",
      "tiên củ cải đứng: đầu tròn mặt thú (không tóc, không mặt người), da đỏ thẫm mặt kem; đội hoa trà trắng nở to nhụy đỏ thẫm; cổ áo lá xanh thẫm; thân đỏ thẫm bụng kem; váy ba lá xanh thẫm; ba chóp rễ đỏ thẫm dưới váy; hai tay đỏ thẫm bàn kem, mỗi tay cầm một quả mọng đỏ; mắt nâu sẫm",
      "a RADISH FAIRY standing upright, with a ROUND ANIMAL HEAD (not a human girl), crowned with a white camellia in full "
      "bloom, the THIRD stage of a three-stage Wood evolution line whose first stage is image 6: a round crimson radish pup",
      "standing upright with both arms held out to the sides",
      "a proud flower fighter: brows angled down, a confident grin with a small fang",
      HN_COL + ", a big white camellia with deep-crimson stamens, plump deep-red berries",
      HN_AV + ", a pink lily, yellow stamens on long stalks, a golden collar, a human girl's face, hair or bangs, pale "
              "green skin",
      [G("N01", [36, 37, 39, 42, 43, 44], "doi", "round animal head with face", "đầu tròn mặt thú",
         "a human-like head: a pale-green round face with a pointed side lock on the viewer-left, two big purple eyes and "
         "a tiny smile, and green hair: a big lock sweeping over the top and down the viewer-right side, a smaller lock "
         "on the viewer-left",
         "a ROUND animal head with NO hair, filling the face and hair area: deep crimson-red radish skin on the top, "
         "back and sides where the old hair was, a big warm cream face patch in front with a small animal muzzle; two "
         "big dark-brown eyes (one small catchlight dot each) exactly where the old eyes are, brows angled down, a "
         "confident grin with a small fang where the old mouth is; not a human face, no hair, no bangs, no nose",
         joint="bottom of the head (the neck, at the collar)",
         hide=[37, 39, 42, 43, 44]),
       G("N02", [33, 31, 34, 35, 38, 40, 41, 28, 29, 30], "doi", "white camellia on the head", "hoa trà trắng trên đầu",
         "a big pink lily sitting on top of the head: seven curling pink petals, and three thin yellow stamens with round "
         "tips standing up from its centre",
         "a big white camellia in full bloom sitting on top of the head: the petals become wide rounded white camellia "
         "petals in the same places (thin warm-grey lines between petals, no pink); the three stalks become short thick "
         "deep-crimson stamens with round crimson tips standing up from the centre",
         joint="base of the flower (where it sits on top of the head)"),
       G("N03", [27, 46, 47], "doi", "leaf collar", "cổ áo lá",
         "a big golden curved collar behind the neck spreading out to both sides, and two golden curling tips at the "
         "front of the shoulders",
         "a collar of dark forest-green leaves with olive midribs: a wide leaf spreading behind the neck to both sides "
         "and two leaf tips curling up at the front of the shoulders, the same shapes and places; no gold",
         joint="middle of the collar (at the neck, under the chin)"),
       G("N04", [18, 14], "giu", "body", "thân",
         "a small pale-green torso narrowing at the waist with a leafy lower edge, and a dark-green oval at the waist "
         "mostly hidden under the skirt",
         "a deep crimson-red radish torso with a warm cream belly patch in front, its leafy lower edge dark forest "
         "green; the waist oval dark forest green"),
       G("N05", [17, 15, 16], "giu", "leaf skirt", "váy lá",
         "a skirt of three big round green leaves: one in front, one on the viewer-left, one on the viewer-right",
         "a skirt of three big dark forest-green leaves with olive midribs and a thin olive rim"),
       G("N06", [11, 12, 13], "giu", "radish root feet", "chân rễ củ cải",
         "three yellow drop-shaped petals under the skirt, their points hanging down, standing in for feet",
         "three deep crimson-red radish-root lobes peeking out under the skirt, each tapering to a thin cream root tip "
         "pointing down"),
       G("N07", [20, 21, 19, 23, 24, 25, 26, 22], "giu", "viewer-left arm holding a berry", "tay bên trái cầm quả mọng",
         "the arm on the viewer-left: an upper arm going down from the shoulder (TOP end = shoulder), a round elbow, a "
         "forearm going down-left, an open leafy hand at the BOTTOM-LEFT end with three small finger tips, and a "
         "dark-green leaf over the shoulder like a sleeve",
         "a deep crimson-red arm ending in a cream paw with three short fingers at the bottom-left end; the paw clutches "
         "one plump round deep-red berry with a tiny dark-green leaf cap, drawn inside the paw outline; the shoulder "
         "leaf is a dark forest-green leaf sleeve"),
       G("N08", [2, 5, 4, 6, 7, 8, 9, 3], "giu", "viewer-right arm holding a berry", "tay bên phải cầm quả mọng",
         "the arm on the viewer-right: an upper arm going down from the shoulder (TOP end = shoulder), a round elbow, a "
         "forearm going down-right, an open leafy hand at the BOTTOM-RIGHT end with three small finger tips, and a "
         "dark-green leaf over the shoulder like a sleeve",
         "a deep crimson-red arm ending in a cream paw with three short fingers at the bottom-right end; the paw "
         "clutches one plump round deep-red berry with a tiny dark-green leaf cap, drawn inside the paw outline; the "
         "shoulder leaf is a dark forest-green leaf sleeve")],
      keep=[1], drop=[48, 49, 10, 32, 45, 50, 51, 52, 53, 54, 55], prev="hoa_nhuy_1",
      anim=dict(root=18, head=36, swing=[2], wob=[28, 29, 30], fly=[], cast=(6, 0.45, 0.5),
                parent={33: 36, 31: 36, 34: 36, 35: 36, 38: 36, 40: 36, 41: 36, 28: 36, 29: 36, 30: 36,
                        22: 20, 21: 20, 19: 20, 23: 19, 24: 23, 25: 23, 26: 23,
                        3: 2, 5: 2, 4: 2, 6: 4, 7: 6, 8: 6, 9: 6}),
      note="48, 49 chùm chuông tím ở ngực: bỏ (quả mọng vẽ trong bàn tay); 37, 39 tóc gộp vào đầu (ẩn); 10, 32, 45, 50 "
           "lấp lánh (32, 45, 50 chung hình c50), 51–55 quả cầu sáng (c7, c8): bỏ"),
]
