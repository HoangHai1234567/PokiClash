# Thỏ Hoàng (ải 50, Sử thi): thỏ tướng giáp ngọc bích, 1 dạng. Người dùng chốt concept bằng chữ 2026-11-07.
# Gốc: 2010 thỏ tướng áo đen, vàng, đĩa âm dương ở ngực và tay, nhiều tấm vàng bay quanh, vuốt sắt to bên trái người xem
#      (rig này đã dùng cho tu sĩ đỏ vàng ở aola/reskin/monk_2010: chia nhóm tham khảo từ đó).
# Mới: thỏ tai dài lông trắng ngà, giáp vảy ngọc bích viền đồng, áo choàng xanh rừng thẫm, mắt xanh lục; tấm vàng bay quanh
#      thành thẻ tre xanh khắc lá; đĩa âm dương thành đĩa ngọc bích chạm lá; vuốt sắt thành vuốt gỗ mun gắn ngọc.
TH_COL = ("ivory-white fur, jade-green scale armour with bronze rims, a dark forest-green cloak, big green eyes, flat green "
          "bamboo slips, dark ebony wood, small jade stones")
TH_AV = ("black robes or sleeves, red, orange or yellow-gold colours, a yin-yang symbol, gold plates or bars, a human face "
         "or human hands, silver claws, flame shapes, glowing green flame wisps, glowing specks")

SPEC = [
    F("tho_hoang_1", 2010, "Thỏ Hoàng", 1, 1, "Thỏ Hoàng", "ải 50 đảo Mộc, dạng 1/1",
      "thỏ tướng tai dài lông trắng ngà, mắt xanh lục, mũ và giáp vảy ngọc bích viền đồng, áo choàng xanh rừng thẫm, hai "
      "chùm lông thỏ trắng ngà sau eo; thẻ tre xanh khắc lá bay quanh; đĩa ngọc bích chạm lá ở thắt lưng; vuốt gỗ mun gắn "
      "ngọc bay cạnh tay trái",
      "a long-eared RABBIT GENERAL in jade scale armour, a single-stage Wood creature",
      "leaping in mid-air, one arm raised high and the other stretched out",
      "a proud rabbit general about to strike: brow angled down, a confident closed-mouth smirk",
      TH_COL, TH_AV,
      [G("N01", [10, 9, 12, 15, 14], "doi", "rabbit head with face and jade helmet", "đầu thỏ có mặt, mũ ngọc",
         "a small white-and-grey rabbit face turned to the viewer-right with a black nose at its right end and one blue "
         "eye, grey cheek and throat fur under it, a big spiky orange-and-yellow flame-shaped mane behind the head, and a "
         "long green spike sweeping from the upper-left down to just above the eye",
         "a cute rabbit face turned to the viewer-right with a short animal muzzle and a small dark nose at its right "
         "end, ivory-white fur, one big green eye (one catchlight dot) exactly where the old eye is, a brow angled down, "
         "a confident closed-mouth smirk, ivory cheek and throat fur below it; behind the head a jade-green scale helmet "
         "with a bronze rim whose back edge is layered like leaves, and a long dark forest-green leaf-shaped helmet crest "
         "sweeping from the upper-left down to above the eye; an animal face, not a human face; no orange, no flames",
         joint="the bottom of the face and throat where the head sits on the collar", hide=[14]),
       G("N02", [13, 11], "doi", "two long rabbit ears", "hai tai thỏ dài",
         "two long pointed rabbit ears: a tall one standing straight up behind the head and one leaning to the "
         "upper-right, each white at the tip with green and red stripes",
         "ivory-white fur outside, a pale jade-green inner lining and a thin bronze ring near the base of each ear, the "
         "same lengths and directions; no red",
         joint="the bottom end of each ear where it grows from the head"),
       G("N03", [18, 8, 7, 32, 42, 43, 21, 38, 41], "giu", "chest and waist armour with jade disc",
         "ngực, eo, giáp và đĩa ngọc",
         "the chest and waist: a white chest with a black diamond mark, a high black-and-gold collar on the viewer-right "
         "side of the neck with a small gold ornament, black hips, a big gold belt buckle with a green gem across the "
         "waist holding a round black-and-white yin-yang disc, a green sash end on the viewer-right of the waist and two "
         "small gold tassels hanging from the belt",
         "ivory fur chest covered by jade-green scale armour with bronze rims; the high collar becomes a jade scale "
         "collar with a bronze rim; the hips covered by jade scale armour; a bronze belt buckle holding a round flat "
         "jade-green disc carved with a leaf pattern instead of the yin-yang disc; a dark forest-green sash end; two "
         "small bronze-and-green cord tassels; no black, no gold, no yin-yang"),
       G("N04", [23, 22, 25], "giu", "raised viewer-left arm", "tay trái giơ cao",
         "the viewer-left arm raised to the upper-left inside a wide black sleeve whose pointed green tip at the "
         "upper-left is the sleeve end (NO hand), a black-and-gold pointed shoulder guard at its shoulder (lower-right) "
         "end, and a gold band with black swirls across the upper arm",
         "the same raised arm in a dark forest-green cloak sleeve covered with jade scale plates, its pointed upper-left "
         "tip a jade-green leaf-shaped cuff (no hand drawn); a jade scale shoulder guard with a bronze rim; a bronze arm "
         "band carved with small leaves; no black, no gold"),
       G("N05", [5, 6, 3, 4], "giu", "outstretched viewer-right arm with paw", "tay phải duỗi và bàn tay thỏ",
         "the viewer-right arm stretched to the right: a black shoulder pad with a green spiral at its LEFT end, a black "
         "sleeve with a green cuff, a grey pointed sleeve flap rising above the elbow, and an open pink clawed hand at "
         "its RIGHT end",
         "a jade scale shoulder pad with a bronze rim at the LEFT end, a dark forest-green sleeve with a jade-green cuff, "
         "the flap a jade-green leaf-shaped armour fin, and an open ivory-white furry rabbit paw with small dark claws at "
         "the RIGHT end; no pink human hand, no black"),
       G("N06", [20, 19], "doi", "two fluffy rabbit-fur plumes", "hai chùm lông thỏ",
         "two white furry tails edged with green streaming out to the viewer-left from behind the waist, the lower one "
         "bigger",
         "fluffy ivory-white fur in the same two plumes streaming to the viewer-left, with pale jade-green tips, like a "
         "big rabbit tail",
         joint="the right end of each plume (behind the waist)"),
       G("N07", [27, 37, 36, 39, 40], "doi", "dark forest-green cloak panels", "vạt áo choàng xanh rừng",
         "a grey skirt fluttering out to the viewer-right behind the legs, and four long black robe tails with gold "
         "borders and gold swirl patterns: two streaming down to the lower-left and two streaming out to the lower-right",
         "the skirt and the four tails become long cloak panels in the same places and directions, dark forest green "
         "with a bronze hem and a small carved leaf motif near the tips; no black, no grey, "
         "no gold swirls",
         joint="the waist end of each panel"),
       G("N08", [33, 34, 35, 29, 30, 31], "giu", "two rabbit legs with jade greaves", "hai chân thỏ, giáp ống ngọc",
         "two legs hanging down: on the viewer-left a black thigh, a black shin with a gold knee ornament and a green "
         "foot with silver claws pointing down at the BOTTOM; on the viewer-right a black thigh, a red-and-gold knee "
         "ornament and a green shin with silver claws pointing down at the BOTTOM",
         "ivory-white furry rabbit legs with jade-green scale greaves and bronze-rimmed jade knee guards, big ivory "
         "rabbit feet with small dark claws pointing down at the bottom; no black, no red, no silver"),
       G("N09", [2], "doi", "floating bamboo slips", "thẻ tre bay",
         "four floating clusters of gold-and-dark-green bars around the figure: a big one at the upper-left, a small one "
         "at the upper-right, one at the lower-left and one at the lower-right",
         "the same four floating clusters, but each bar is a flat green bamboo slip carved with a small leaf, tied with "
         "a thin bronze cord; no gold, no glow",
         joint="each cluster stays where it is (floating, not attached)"),
       G("N10", [24], "doi", "big ebony claw with jade disc", "vuốt gỗ mun gắn đĩa ngọc",
         "a big round weapon floating beside the viewer-left arm: a black-and-white yin-yang disc in a gold ring at its "
         "upper-left, red-and-orange flame-shaped fins around it, a few small green bars, and big silver claws hanging "
         "from its bottom",
         "a big ebony-wood claw: a round flat jade-green disc carved with leaves in the same place as the old disc, a "
         "frame of dark ebony wood with leaf-shaped fins instead of the flames, small jade chips instead of the green "
         "bars, and three big curved ebony claws hanging from the bottom, each set with a small jade stone; no yin-yang, "
         "no flames, no red, no gold, no silver",
         joint="the disc centre stays where it is")],
      keep=[1], drop=[16, 17, 26, 28, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55],
      anim=dict(root=18, head=10, swing=[23, 5], wob=[13, 11, 19, 20], fly=[2], cast=(24, 0.4, 0.4),
                parent={13: 10, 11: 10, 23: 22, 25: 23, 24: 23, 5: 6, 3: 5, 4: 5, 34: 33, 35: 34, 30: 29, 31: 29}),
      note="16, 17, 26, 28 lửa linh hồn xanh, 44-55 đốm sáng (chung c7, 53 rỗng): bỏ. Mắt 14 ẩn; ảnh nháy mắt c146 (khung "
           "nghỉ 6-10, trúng đòn 2-9) phải bỏ lúc ghép (monk_2010 dùng drop_chars [28, 36, 146]). Mảnh tự chạy: 2 thanh "
           "(4 ảnh), 24 vũ khí (12), 27 váy (8), 36 37 39 40 vạt áo (7): xem monk_2010/groups.json."),
]
