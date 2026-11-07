# Bờm Lá (ải 15, Khá): sư tử con bờm dương xỉ, dòng 2 dạng. Người dùng chốt concept bằng chữ 2026-11-07.
# Gốc: 911 thú tròn xanh lá, tai cánh sọc vàng, búi lá trên đầu, kim cương xanh lơ trên trán;
#      912 sư tử con bờm lá vàng xanh, đuôi và móng pha lê xanh lơ.
# Mới: lông vàng nâu (tawny), bờm lá dương xỉ xanh thẫm, trán đeo huy hiệu gỗ hình lá, chóp đuôi quả thông, móng bọc mũ quả
#      sồi thay pha lê, mắt xanh lục.
BL_COL = ("tawny golden-brown fur with a pale cream muzzle, dark-green fern fronds, a carved light-wood leaf-shaped badge on the "
          "forehead, brown scaly acorn caps over the paws, big leaf-green eyes")
BL_AV = ("a green body, yellow stripes or green-and-yellow stripes, crystals, gems or diamonds, cyan or turquoise, gold armour or "
         "gold frames, thorny vines, feathery wing-shaped ears")

SPEC = [
    # ---- dạng 1: rig #911, thú tròn một khối đầu thân, hai tai cánh, búi lá trên đầu, ba chân nhỏ
    F("bom_la_1", 911, "Bờm Lá", 1, 2, "Bờm Lá Con", "ải 15 đảo Mộc, dạng 1/2",
      "sư tử con tròn: lông vàng nâu mõm kem, hai túm lá dương xỉ xanh thẫm thay tai cánh, chồi dương xỉ cuộn trên đầu thay "
      "búi lá, huy hiệu gỗ hình lá trên trán thay kim cương, ba bàn chân bọc mũ quả sồi, mắt xanh lục",
      "a round LION CUB with the beginnings of a fern mane, the first stage of a two-stage Wood evolution line",
      "crouched low on its little paws, leaning forward",
      "a brave little lion cub ready to pounce: brows angled down, a confident grin with a tiny fang",
      BL_COL, BL_AV,
      [G("N01", [7, 11, 12, 13], "giu", "round head-body with face", "khối đầu thân có mặt",
         "a big round green head-body with yellow and dark-green stripes on both sides, a cyan diamond gem in a small gold "
         "crown shape on the forehead, two big dark eyes and a tiny open mouth",
         "a round chubby lion cub head-body: tawny golden-brown fur, a pale cream muzzle and chin, a small carved light-wood "
         "badge shaped like a leaf on the forehead where the old gem was, two big leaf-green eyes (one catchlight dot each) "
         "exactly where the old eyes are, brows angled down, a confident grin with a tiny fang; no stripes, no gem",
         hide=[11, 12, 13]),
       G("N02", [3, 2, 8], "doi", "curled fern sprout on the head", "chồi dương xỉ cuộn trên đầu",
         "a big leaf-like tuft on top of the head: a large green leaf lying across the top, a darker green back part on the "
         "viewer-left and the leaf tip curling up on the viewer-right",
         "a young fern frond (fiddlehead) growing from the top of the head: a thick dark-green stalk rolling into a tight "
         "spiral, with small fern leaflets along it, about the same size and place as the old tuft",
         joint="bottom edge of the tuft, where it sits on top of the head"),
       G("N03", [9, 6], "doi", "two fern tufts (ears)", "hai túm lá dương xỉ (tai)",
         "two wing-like ears sticking out on both sides of the head, yellow and green striped with orange-brown rims and "
         "jagged feathery edges; the viewer-left one is bigger",
         "two tufts of dark-green fern fronds sticking out sideways like the old ears (each a bunch of three or four fern "
         "leaves with small leaflets along their edges), the same size and place; no stripes, no yellow",
         joint="inner end of each tuft, where it joins the side of the head"),
       G("N04", [10, 4, 5], "giu", "three small paws", "ba bàn chân",
         "three tiny green stubby feet under the body: one at the far viewer-left, one at the bottom left of centre in front, "
         "one at the bottom viewer-right",
         "three tiny stubby tawny paws, each covered over the toes by a brown scaly acorn cap like a little boot")],
      keep=[1],
      anim=dict(root=7, head=7, swing=[], wob=[9, 6, 3], fly=[], cast=(7, 0.67, 0.83), parent={2: 3, 8: 3}),
      note="7 khối đầu thân (kim cương vẽ liền trong mảnh); 11, 12 mắt, 13 miệng: ẩn; không có đuôi"),

    # ---- dạng 2: rig #912, sư tử con đứng thế vồ nghiêng 3/4 quay phải, đuôi dây leo pha lê, hai dây roi pha lê hai bên
    F("bom_la_2", 912, "Bờm Lá", 2, 2, "Chiến Sư Bờm Lá", "ải 15 đảo Mộc, dạng 2/2",
      "sư tử con đứng thế vồ: lông vàng nâu mõm kem, bờm lá dương xỉ xanh thẫm quanh đầu và ngực, huy hiệu gỗ hình lá trên "
      "trán, đuôi dài chóp quả thông, hai roi thân dương xỉ đầu bọc mũ quả sồi thay dây gai pha lê, bốn chân bọc mũ quả sồi "
      "thay vuốt vàng, mắt xanh lục",
      "a young LION warrior with a full mane of fern fronds, the SECOND stage of a two-stage Wood evolution line whose first "
      "stage is image 6 (the round lion cub)",
      "standing in a low pouncing crouch on four short legs, body turned slightly to the viewer-right",
      "a fierce little lion about to pounce: brows angled down, an open confident grin with a small fang",
      BL_COL + ", a brown pine cone at the tail tip", BL_AV,
      [G("N01", [13, 21, 20, 15], "giu", "head with face", "đầu có mặt",
         "a big rounded pale-green head turned slightly to the viewer-right, with a darker green patch at the top "
         "viewer-right; on it sit two big brown-and-amber eyes with angry brows, an open mouth with a fang, and a small cyan "
         "diamond gem on the forehead between the eyes (a separate piece)",
         "a lion cub head: tawny golden-brown fur, a pale cream muzzle and chin, two big leaf-green eyes (one catchlight dot "
         "each) exactly where the old eyes are, brows angled down, an open confident grin with one small fang where the old "
         "mouth is; the forehead gem piece becomes a small carved light-wood badge shaped like a leaf, the same size and place",
         hide=[21, 20]),
       G("N02", [18, 4, 6, 14, 5, 19, 16, 9], "doi", "fern mane", "bờm lá dương xỉ",
         "spiky leaf-shaped mane pieces around the head: a big yellow-and-green striped double leaf over the top viewer-left "
         "of the head, pale-green leaves behind it at the top viewer-left and top viewer-right, a striped leaf at the top "
         "viewer-right and a green leaf by the viewer-right cheek; plus three small curved gold plates on the chest under the "
         "chin",
         "a lion mane of dark-green fern fronds: each old leaf becomes a fern frond (a long leaf with small rounded leaflets "
         "along both edges) in the same place and pointing the same way, and the three gold chest plates become three short "
         "fern fronds hanging over the chest under the chin; no stripes, no yellow, no gold",
         joint="inner end of each frond, where it grows from the head or the neck"),
       G("N03", [10], "giu", "body", "thân",
         "a small oval torso under the head, dark green with orange and yellow stripes",
         "a small tawny golden-brown torso with a pale cream belly, same outline; no stripes"),
       G("N04", [12, 11, 7, 8], "giu", "four legs", "bốn chân",
         "four short legs, pale green with dark-green and yellow stripes, each ending in a yellow-gold claw cuff: two on the "
         "viewer-left (the front one nearest us) and two on the viewer-right; TOP end = shoulder or hip under the body, BOTTOM "
         "end = paw on the ground",
         "four short sturdy tawny lion legs with the same outline; at the BOTTOM end each paw is covered by a brown scaly acorn "
         "cap like a little boot, where the old gold claw cuff was; no stripes"),
       G("N05", [3], "doi", "tail with pine cone tip", "đuôi chóp quả thông",
         "a long thin green thorny vine rising from behind the body and curving up to the top viewer-left, ending in a big "
         "cyan crystal in a gold frame",
         "a long thin tawny lion tail with the same curve, ending in a brown pine cone (overlapping scales, flat colour) where "
         "the old crystal was; no thorns, no crystal",
         joint="bottom (viewer-right) end of the tail, hidden behind the body"),
       G("N06", [17, 2], "doi", "two fern whips with acorn-cap claws", "hai roi dương xỉ đầu mũ quả sồi",
         "two thin green thorny vines growing from behind the head: one curls out to the viewer-left and down, the other runs "
         "out to the viewer-right and down; each ends in a cyan crystal claw in a gold frame",
         "two curling dark-green fern-stem whips with the same curves (small fern leaflets instead of thorns), each ending in a "
         "big brown scaly acorn cap like a claw club where the old crystal was; no crystals, no thorns",
         joint="inner end of each whip, hidden behind the head (where it grows from the neck)")],
      keep=[1], prev="bom_la_1",
      anim=dict(root=10, head=13, swing=[17, 2], wob=[3, 6, 4], fly=[], cast=(13, 0.64, 0.9),
                parent={18: 13, 4: 13, 6: 13, 14: 13, 5: 13, 19: 13, 16: 13, 9: 13}),
      note="17, 2 dây roi đầu pha lê (\"móng pha lê\" của gốc): vung khi đánh; 19, 16, 9 tấm vàng dưới cằm thành lá bờm; "
           "15 kim cương trán giữ thành huy hiệu gỗ"),
]
