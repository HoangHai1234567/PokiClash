# Long Vuốt (ải 40, Sử thi): rồng gai sồi. Người dùng chốt concept bằng chữ 2026-11-07.
# Gốc: 1219 rồng con xanh lá sừng vàng, kính pha lê xanh dương, vòng tay vàng gắn đá, vệt cam quanh mình;
#      1220 rồng xanh lá cánh xanh thẫm, sừng vàng, pha lê xanh, vuốt vàng.
# Mới: da xanh ô liu, giáp vỏ cây nâu ở lưng và vai, sừng gai gỗ, kính thành mảnh nhựa cây hổ phách, vuốt gai đỏ thẫm;
#      vòng tay và vệt cam thành hạt nhựa hổ phách kéo vệt lá sồi; dạng 2 cánh lá sồi màng ô liu gân nâu, vuốt gai to.
LV_COL = ("olive-green skin, a pale khaki belly, bark-brown armour plates and wooden thorn horns, flat honey-amber resin, "
          "deep crimson thorn claws, olive oak-leaf wing membranes with brown veins, dark brown eyes")
LV_AV = ("bright fresh green skin, gold or yellow-gold horns, metal or claws, blue crystal or glass, gold bracelets set with "
         "blue gems, orange swoosh trails, gem shine")

TRAIL_OLD = ("two thin swoosh pieces circling the body: each is a long orange motion streak on one side and a small gold "
             "ring set with a blue gem on the other side (one streak on the viewer-left with its ring at the viewer-right "
             "hand, one streak on the viewer-right with its ring at the viewer-left hand)")
TRAIL_NEW = ("each orange streak becomes a thin trail of small olive-green and brown oak leaves following the same curve, "
             "and each gold ring becomes a small flat amber resin bead; no orange streak, no gold, no blue gem")
TRAIL_JOINT = "each bead and leaf trail stays where the old ring and streak are"

SPEC = [
    F("long_vuot_1", 1219, "Long Vuốt", 1, 2, "Long Vuốt Con", "ải 40 đảo Mộc, dạng 1/2",
      "rồng con gai sồi: da xanh ô liu, bụng kaki nhạt, sừng gai gỗ nâu, kính thành tấm nhựa cây hổ phách che mắt phải, "
      "cổ áo giáp vỏ cây, vai và đuôi có tấm vỏ cây, vuốt gai đỏ thẫm, cánh lá sồi non, vòng tay và vệt cam thành hạt nhựa "
      "hổ phách kéo vệt lá sồi, mắt nâu sẫm",
      "an OAK-THORN DRAGON CUB, the first stage of a two-stage Wood evolution line",
      "crouched low in mid-hop with both arms out to the sides",
      "a plucky little dragon ready to pounce: brow angled down, a small fang in a confident grin",
      LV_COL, LV_AV,
      [G("N01", [14, 26], "giu", "round head with face", "đầu tròn có mặt",
         "a big round bright-green dragon head turned slightly to the viewer-right, a pointed lobe sticking out at the "
         "back of the head on the viewer-left, darker green markings on top, one big blue eye on the viewer-left of the "
         "face (the other eye is hidden under a crystal lens on the viewer-right), the muzzle at the lower right",
         "a round olive-green dragon-cub head of the same shape, the pointed lobe at the back kept; a pale khaki muzzle "
         "at the lower right; one big dark brown eye (one catchlight dot) exactly where the old eye is, a brow angled "
         "down above it, a small confident grin with a tiny fang on the muzzle; a few bark-brown scale plates on top of "
         "the head instead of the dark markings",
         hide=[26]),
       G("N02", [29, 27, 15], "doi", "three wooden thorn horns", "ba sừng gai gỗ",
         "three gold horn-like spikes on the head: a big long blade lying diagonally across the top of the head with its "
         "point at the upper-left, a smaller horn standing up on the viewer-right behind the lens, and a tiny spike on the "
         "viewer-left cheek next to the eye pointing up-left",
         "three thorns of bark-brown oak wood with a few darker grain lines, in the same places and directions: a big "
         "curved thorn horn across the top of the head pointing up-left, a smaller thorn horn standing up on the "
         "viewer-right, and a tiny thorn on the viewer-left cheek; no gold",
         joint="base of each thorn on the head (lower-right end of the big one and of the cheek thorn, bottom end of the "
               "viewer-right one)"),
       G("N03", [28], "doi", "amber resin visor", "tấm nhựa hổ phách che mắt",
         "a big blue crystal lens shaped like a pointed oval, with a thick blue rim and white shine, covering the "
         "viewer-right eye",
         "a flat honey-amber resin plate of the same pointed-oval shape with a thin dark-brown wooden rim, covering the "
         "viewer-right eye like a visor; flat colour, no shine, no blue, no eye drawn on it",
         joint="its viewer-left edge where it touches the head"),
       G("N04", [6, 12, 13], "giu", "body with bark collar", "thân và cổ áo vỏ cây",
         "the small round green body under the head with a cream belly, a blue crystal V-shaped collar on the chest just "
         "under the chin, and a gold-and-orange gem pendant in the middle of the collar",
         "a small round olive-green body with a pale khaki belly; the collar becomes a V-shaped gorget of overlapping "
         "bark-brown armour plates; the pendant becomes a small flat amber resin bead in a wooden setting; no blue "
         "crystal, no gold"),
       G("N05", [16, 8, 17, 18, 19, 9, 10, 11], "giu", "two arms with thorn claws", "hai tay và vuốt gai",
         "two short chubby arms stretched out to both sides: the near arm on the viewer-left (bright green, shoulder at "
         "its RIGHT end next to the body, hand at its LEFT end) with three small gold claws at the hand, and the far arm "
         "on the viewer-right (dark green, behind the body, shoulder at its LEFT end, hand at its RIGHT end) with three "
         "small gold claws at the hand",
         "two short chubby olive-green arms in the same places, each with a small bark-brown armour plate at the "
         "shoulder end; the claws become short curved deep-crimson thorns, three at each hand; no gold"),
       G("N06", [20, 3, 21, 22, 23, 24, 25], "giu", "two feet with thorn claws", "hai bàn chân và vuốt gai",
         "two short stubby feet: the viewer-left foot faces the viewer showing a round cream sole pad, with three small "
         "gold claws along its TOP edge; the viewer-right foot is a small green paw stretched to the right with two small "
         "gold claws at its upper-right tip",
         "two short stubby olive-green feet in the same places, a pale khaki sole pad on the viewer-left foot; the claws "
         "become small curved deep-crimson thorns; no gold"),
       G("N07", [5, 7], "doi", "two young oak-leaf wings", "hai cánh lá sồi non",
         "two dark-green bat-like wings: a big near wing spreading up-left from the back behind the viewer-left arm (root "
         "at its lower-right end), and a small far wing peeking out on the viewer-right behind the neck (root at its "
         "narrow bottom end)",
         "small wings shaped like young oak leaves: olive-green membrane with brown veins and a wavy lobed edge, a bark-brown "
         "wing bone along the top edge, the same sizes and directions",
         joint="the wing root at the back (lower-right end of the big wing, narrow bottom end of the small wing)"),
       G("N08", [4], "doi", "armoured tail", "đuôi giáp vỏ cây",
         "a dark-green curved tail behind the viewer-left arm, its wide base at the bottom behind the body and its "
         "pointed tip curling up to the upper-left",
         "an olive-green tail of the same curve with a row of small bark-brown armour plates along its outer edge and a "
         "tip shaped like a wooden thorn",
         joint="the wide bottom end where the tail joins the body"),
       G("N09", [1, 30], "doi", "two amber beads with oak-leaf trails", "hai hạt nhựa kéo vệt lá sồi",
         TRAIL_OLD, TRAIL_NEW, joint=TRAIL_JOINT)],
      keep=[2], drop=[],
      anim=dict(root=6, head=14, swing=[16, 8], wob=[5, 7, 4], fly=[], cast=(14, 0.9, 0.78),
                parent={29: 14, 27: 14, 15: 14, 28: 14, 17: 16, 18: 16, 19: 16, 9: 8, 10: 8, 11: 8,
                        21: 20, 22: 20, 23: 20, 24: 3, 25: 3}),
      note="bóng là mảnh 2 (không phải 1); 1, 30 = vòng tay gắn đá + vệt cam (mỗi mảnh một vòng một vệt) vẽ lại thành "
           "hạt nhựa kéo vệt lá; 4 là đuôi (sau tay trái), 7 cánh xa, 8 tay xa"),
    F("long_vuot_2", 1220, "Long Vuốt", 2, 2, "Long Vuốt", "ải 40 đảo Mộc, dạng 2/2",
      "rồng gai sồi lớn: như dạng 1 (da ô liu, bụng kaki, mắt nâu sẫm), sừng gai gỗ nâu, tấm nhựa hổ phách che mắt phải, "
      "giáp vỏ cây ở vai và cẳng tay, cánh lá sồi màng ô liu gân nâu, vuốt gai đỏ thẫm to, đuôi giáp vỏ cây, hai hạt nhựa "
      "kéo vệt lá sồi",
      "an OAK-THORN DRAGON, the SECOND stage of a two-stage Wood evolution line whose first stage is image 6: the "
      "oak-thorn dragon cub",
      "standing on two legs with arms spread wide and claws out",
      "a proud dragon ready to slash: brow angled down, a confident grin with a fang, claws spread",
      LV_COL, LV_AV,
      [G("N01", [26], "doi", "head with face and thorn horns", "đầu có mặt, sừng gai",
         "a dragon head turned to the viewer-right with a long green snout pointing down at the bottom, one big blue eye "
         "on the viewer-left, a gold helmet with blade-like gold crests sweeping up-left across the top, a blue crystal "
         "goggle over the viewer-right eye, a gold horn sticking up on the viewer-right and a gold-and-orange fin on the "
         "viewer-left cheek, a tall green crest in the middle of the head",
         "the grown-up oak-thorn dragon head: olive-green head and snout with a pale khaki chin, one big dark brown eye "
         "(one catchlight dot) exactly where the old eye is, a brow angled down, a confident grin with a small fang; the "
         "gold crests become big curved thorn horns of bark-brown oak wood in the same places and directions, the cheek "
         "fin a smaller wooden thorn, the goggle a flat honey-amber resin plate with a thin wooden rim over the "
         "viewer-right eye, the tall middle crest olive green with a bark-brown edge; no gold, no blue",
         joint="the bottom of the head where it sits on the neck"),
       G("N02", [13, 11, 22, 23], "giu", "torso and neck with bark shoulder armour", "thân, cổ và giáp vai vỏ cây",
         "the torso and neck: a green torso with a pale belly and a thin red stripe across it, a green neck rising from "
         "the torso up to the head with a pale front, a spiky blue crystal collar across both shoulders at the base of "
         "the neck, and a gold-and-orange gem pendant at the front of the collar",
         "an olive-green torso and neck with pale khaki belly scales; the collar becomes overlapping bark-brown armour "
         "plates across both shoulders; the pendant becomes a flat amber resin bead in a wooden setting; no red stripe, "
         "no blue crystal, no gold"),
       G("N03", [16, 15, 19, 20, 21, 7, 10, 6, 17, 18], "giu", "two arms with big thorn claws", "hai tay và vuốt gai to",
         "two arms held out to both sides: on the viewer-left an upper arm (shoulder at its RIGHT end, elbow at its LEFT "
         "end) and a big forearm gauntlet with a blue-and-white bracer and a gold blade fin pointing up, the hand at its "
         "BOTTOM-LEFT end with three long gold claws hanging down; on the viewer-right a dark-green upper arm (shoulder "
         "at its TOP-LEFT end, elbow at its BOTTOM-RIGHT end) and a forearm gauntlet with a blue bracer and a gold fin "
         "pointing up, the hand at its BOTTOM end with three gold claws hanging down",
         "olive-green arms in the same places; each forearm wears a bark-brown armour bracer with a bark-plate fin "
         "pointing up instead of the gold blade; the claws become big curved deep-crimson thorn claws hanging down, the "
         "same number and places; no gold, no blue"),
       G("N04", [14, 12, 24, 9, 8, 25], "giu", "two legs with thorn claws", "hai chân và vuốt gai",
         "two legs standing apart: on the viewer-left a round green thigh, a shin going down to the foot and three big "
         "gold claws at the BOTTOM pointing down; on the viewer-right a round green thigh, a shin going down-right and "
         "two gold claws at the BOTTOM",
         "olive-green legs in the same places with pale khaki inner sides and a small bark-brown knee plate on each "
         "shin; the foot claws become curved deep-crimson thorn claws; no gold"),
       G("N05", [5, 3], "doi", "two oak-leaf wings", "hai cánh lá sồi",
         "two big bat-like wings: the near wing (green) spreading up-left from behind the viewer-left shoulder, root at "
         "its lower-right end, and the far wing (dark teal) spreading up-right behind the head, root at its lower-left "
         "end",
         "big wings shaped like oak leaves: olive-green membrane with brown veins and a wavy lobed edge, a bark-brown "
         "wing bone along the top edge, the same sizes and directions; no teal",
         joint="the wing root at the shoulder (lower-right end of the near wing, lower-left end of the far wing)"),
       G("N06", [4], "doi", "armoured tail", "đuôi giáp vỏ cây",
         "a green tail behind the legs curving out to the viewer-left, its pointed tip at the left end",
         "an olive-green tail of the same curve with a row of bark-brown armour plates along its top edge and a wooden "
         "thorn tip",
         joint="the right end where the tail joins the body behind the legs"),
       G("N07", [2, 27], "doi", "two amber beads with oak-leaf trails", "hai hạt nhựa kéo vệt lá sồi",
         TRAIL_OLD, TRAIL_NEW, joint=TRAIL_JOINT)],
      keep=[1], drop=[], prev="long_vuot_1",
      anim=dict(root=13, head=26, swing=[16, 7], wob=[5, 3, 4], fly=[], cast=(26, 0.7, 0.92),
                parent={16: 15, 19: 16, 20: 16, 21: 16, 7: 10, 6: 7, 17: 7, 18: 7, 12: 14, 24: 12, 8: 9, 25: 8}),
      note="đầu 26 là một mảnh (mắt, mũ, kính, sừng) nên không có mảnh ẩn; 2, 27 = vòng tay gắn đá + vệt cam như dạng 1"),
]
