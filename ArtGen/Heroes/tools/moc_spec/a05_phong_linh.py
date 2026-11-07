# Phong Linh (ải 20, Hiếm): cú gió lá. Người dùng chốt concept bằng chữ 2026-11-07.
# Gốc: 943 tiên xanh ngọc đội mũ lá to viền vàng có ngọc hồng, hai tay cầm hoa cam; 944 linh tướng dạng người áo lá,
# vòng dây leo gỗ sau lưng, hoa cam hai bên.
# Mới: con CÚ (bỏ dạng người): lông xanh xô thơm pha kem, mặt nạ lông trắng kem, túm tai lá, mắt hổ phách; 943 cầm hai
# chong chóng hạt phong thay hoa cam; 944 cú tướng áo choàng lá xếp lớp, vòng tre quấn dải gió trắng sau lưng.
# 943: tóc mái hai bên (16, 20) ẩn, mặt nạ cú vẽ phủ chỗ đó để có đủ hai mắt (rig chỉ có một mắt, mắt kia bị tóc che).
# 944: đầu là một mảnh (22: mũ, mào lá, tóc dài buông trước ngực); hoa (4, 20) và tay (9, 21) mỗi cặp chung hình.
PL_COL = ("sage-green feathers (soft grey-green) with darker sage leaf-shaped feathers, a warm cream face mask, chest and "
          "feather tips, big amber eyes, a small olive-brown beak, pale tan-green maple seed spinners with olive-brown knots")
PL_AV = ("a human face or body, human hair, a big leaf hat or helmet with a gold rim, a pink gem, orange flowers, turquoise, "
         "mint or light-blue colours, light-blue skin, sleeves or hands")

SPEC = [
    F("phong_linh_1", 943, "Phong Linh", 1, 2, "Tiểu Phong Linh", "ải 20 đảo Mộc, dạng 1/2",
      "cú mèo nhỏ lông xanh xô thơm pha kem: mặt nạ lông trắng kem có hai mắt hổ phách to, mỏ nâu ô liu, hai túm tai là lá; "
      "hai cánh như tay, đầu cánh xòe như ngón nắm, cạnh mỗi đầu cánh lơ lửng một chong chóng hạt phong (thay hoa cam); "
      "thân phủ lông như áo lá",
      "a small chubby LEAF-WIND OWL (a horned owl chick), the first stage of a two-stage Wood evolution line",
      "floating upright just above the ground, its two wings held out at its sides like small arms, a spinner hovering "
      "just beyond each wing tip",
      "a fierce little owl ready to strike: brows angled down, big amber eyes narrowed with determination, a small "
      "confident smirk under its beak",
      PL_COL, PL_AV + ", pink blush stickers",
      [G("N01", [17, 22, 15, 13, 20, 16, 21, 23, 24, 25], "doi", "round owl head with face", "đầu cú có mặt",
         "a fairy's head turned a little to the viewer-right: a pale blue face with one big brown eye and pink blush, "
         "covered on top by a big green helmet-like leaf hat with a gold rim (plus a small gold piece behind it on the "
         "viewer-right), a pink gem in a gold setting at the hat's viewer-left end, dark teal hair arching behind the head "
         "and two teal hair locks hanging down both sides of the face",
         "a round owl head about the size of the whole old head with its hat and hair: soft sage-green feathers on the "
         "crown and back of the head, a big heart-shaped warm cream facial mask filling the face area (the face and the "
         "place of the viewer-left hair lock), two big amber eyes in the mask (the viewer-right eye exactly where the old "
         "eye is, the viewer-left eye beside it to the left), each with one small catchlight dot, brows angled down, a "
         "small hooked olive-brown beak below and between the eyes, a confident little smirk; no hat, no gold, no gem, no "
         "hair, no blush",
         joint="bottom of the head, where the chin sits on the body",
         hide=[20, 16, 21, 23, 24, 25]),
       G("N02", [18, 19, 14], "doi", "two leaf ear tufts", "hai túm tai lá",
         "three big mint-green leaves with dark teal veins growing from the head: a very big one rising to the top-left, "
         "a smaller one under it pointing left, and one on the top-right half behind the hat",
         "the owl's two leaf-shaped ear tufts: the viewer-left tuft is the big leaf with the smaller leaf growing from "
         "the same spot under it, the viewer-right tuft is the single leaf; each leaf sage green with a darker sage "
         "midrib and a few vein lines, tips pointing up and outward like owl ear tufts; no mint, no turquoise",
         joint="base of each leaf, where it grows from the top of the head"),
       G("N03", [10, 3, 5, 6, 2, 4], "giu", "feathered body with leaf-feather coat", "thân lông áo lá",
         "a small green shirt-like torso with a pink collar, and below it a skirt of five overlapping green leaves with "
         "yellow spots (two on the viewer-left, two at the bottom, a thin one on the viewer-right)",
         "the owl's body: a cream feathered chest with small scalloped feather marks where the torso is, and below it a "
         "coat of overlapping leaf-shaped feathers in sage green and darker sage, each with a thin midrib line, layered "
         "like a leaf cape; no shirt, no pink collar, no yellow spots"),
       G("N04", [11, 8, 12, 9], "giu", "two wings held like arms", "hai cánh như tay",
         "two light-blue sleeve-like arms: the viewer-left one points left from the shoulder (inner end at the body, tip "
         "at the far left) with a small narrow piece under its tip; the viewer-right one points down-right from the "
         "shoulder (inner end at the top-left, tip at the bottom-right) with a small narrow piece under it",
         "two sage-green owl wings held out like small arms, same shape and direction as the old sleeves: the inner end "
         "of each is the shoulder, the outer end is the wing tip, ending in three finger-like primary feathers with "
         "cream tips as if gripping; the two small pieces are a second row of short feathers in darker sage; no light "
         "blue, no sleeves, no hands"),
       G("N05", [26, 7], "doi", "two maple-seed spinners", "hai chong chóng hạt phong",
         "two orange flowers with four round petals (turquoise patches) and a brown centre, floating beside the two "
         "wing tips: a bigger one on the viewer-left, a smaller one on the viewer-right",
         "two maple-seed spinners, each a pair of winged maple seeds joined at a round olive-brown seed knot in the "
         "middle like a two-blade propeller: papery pale tan-green seed wings with fine darker vein lines, the knot "
         "where the old flower centre is, about the size of the old flower; no petals, no orange, no turquoise",
         joint="centre of each spinner (where the old flower centre is)")],
      keep=[1], drop=[],
      anim=dict(root=10, head=17, swing=[11, 8], wob=[18, 19, 14, 2, 3], fly=[26, 7], cast=(7, 0.5, 0.5),
                parent={12: 11, 9: 8, 18: 17, 19: 17, 14: 17}),
      note="16, 20 tóc mái: ẩn (mặt nạ cú phủ, để có hai mắt); 21 mắt, 23 má, 24-25 ngọc: ẩn; hoa 7, 26 bay rời"),

    F("phong_linh_2", 944, "Phong Linh", 2, 2, "Phong Linh Tướng", "ải 20 đảo Mộc, dạng 2/2",
      "cú tướng đứng: đầu cú mặt nạ lông kem, mắt hổ phách, túm tai lá, hai vạt lông lá dài buông trước ngực; áo choàng lá "
      "xếp lớp xanh xô thơm; hai cánh dang như tay, chùm lông đầu cánh ở chỗ bàn tay cũ; vòng tre quấn dải gió trắng sau "
      "lưng (thay vòng dây leo); hai chong chóng hạt phong to hai bên (thay hoa cam); chân cú móng ô liu",
      "a tall LEAF-WIND OWL GENERAL, the SECOND stage of a two-stage Wood evolution line whose first stage is image 6: a "
      "chubby sage-green owl with a cream face mask, leaf ear tufts and amber eyes",
      "standing tall in a long leaf cloak, its two wings spread wide to both sides like open arms, a bamboo ring behind "
      "its back and a big spinner hovering on each side of the cloak's hem",
      "a calm, commanding owl general: brows angled down, a steady amber stare, a confident smirk under its beak",
      PL_COL + ", a pale bamboo ring with olive node rings, white wind ribbons, dark-olive talons",
      PL_AV + ", pink bows or bangles, a wooden ring with vines",
      [G("N01", [22], "doi", "owl general head with face", "đầu cú tướng có mặt",
         "one big piece: a head whose face is hidden under a green visor helmet with a gold rim and a pink leaf-shaped "
         "ornament on the viewer-left, a tall yellow-green leaf crest with a blue tip and a small curled tendril growing "
         "up from the top, dark teal hair, and two long pale-green ribbons of hair hanging from both sides of the face "
         "down over the chest",
         "an owl general's head, same place and about the same size: a round head of sage-green feathers; a big "
         "heart-shaped warm cream facial mask where the green visor is, with two big amber eyes (one small catchlight "
         "dot each), brows angled down, a small hooked olive-brown beak and a confident smirk; two sage-green leaf ear "
         "tufts rising from the top of the head where the tall leaf crest and the curled tendril are; the two long "
         "hanging ribbons become two long sage-green leaf-feather lappets of the owl's hood hanging down both sides of "
         "the chest, same place and length, with darker sage leaf tips; no helmet, no visor, no gold, no pink ornament, "
         "no human face, no hair",
         joint="the neck under the chin, where the head sits on the collar"),
       G("N02", [12, 14, 10], "giu", "feathered chest", "ngực lông",
         "a green tunic torso with a turquoise collar and a dark red leaf on the viewer-left shoulder, a pink "
         "leaf-shaped bow on the chest, and a dark teal cape piece with two mint leaves behind the shoulders",
         "the owl general's chest: a cream feathered chest with small scalloped feather marks where the torso is; the "
         "pink bow becomes a fluffy cream feather ruff of leaf-shaped tufts at the throat; the dark cape piece behind the "
         "shoulders becomes the inside of the leaf cloak in darker sage with two sage leaf tips; no pink, no red leaf, "
         "no turquoise collar"),
       G("N03", [6, 7, 5, 19, 18, 11], "giu", "layered leaf cloak", "áo choàng lá xếp lớp",
         "a long skirt of three big green leaves (viewer-left, middle, viewer-right) with yellow patches, two "
         "green-and-pink leaf peplum pieces at the hips and a small green leaf at the viewer-right hip",
         "a long cloak of overlapping big leaf-shaped feathers in sage green and darker sage, each with a thin midrib "
         "and a few vein lines, layered like a leaf cape down to the ground; the hip pieces are a shorter upper layer of "
         "the same leaves with cream feather edges; no pink, no yellow patches"),
       G("N04", [15, 13, 8, 16, 17], "giu", "two wing-arms", "hai cánh tay",
         "two light-blue arms spread to both sides: the viewer-left arm is an upper arm (13) going down-left from the "
         "shoulder and a forearm (15) going left to the wrist, with two pink bangles (16, 17) at the wrist; the "
         "viewer-right arm (8) bends at the elbow, going down from the shoulder and then right to the wrist",
         "two sage-green feathered owl wings spread like open arms, same pieces, bends and directions: shoulder at the "
         "inner end, wrist at the outer end, rows of layered feathers in sage and darker sage along each wing; the two "
         "bangles become two narrow pale bamboo cuffs with olive node lines; no light-blue skin, no pink"),
       G("N05", [9, 21], "doi", "two wing-tip feather fans", "hai chùm lông đầu cánh",
         "two light-blue open hands, palms up and fingers spread, at the outer ends of the arms (viewer-left and "
         "viewer-right)",
         "the owl's wing tips: a fan of four long primary feathers spread like fingers, sage green with cream tips and "
         "a darker sage midrib, where the old hands are and about the same size; no hands, no fingers, no light blue",
         joint="wrist end of each fan, where it joins the arm"),
       G("N06", [3], "giu", "two owl feet", "hai chân cú",
         "two small pink bud-shaped feet peeking out under the skirt, one in the middle and one on the viewer-right",
         "two small owl feet peeking out under the cloak, sage-feathered with three short dark-olive talons each; no "
         "pink, no buds"),
       G("N07", [20, 4], "doi", "two maple-seed spinners", "hai chong chóng hạt phong",
         "two big orange-yellow star flowers with five pointed petals (turquoise tips) and a brown-orange centre, "
         "hovering at both sides of the skirt hem",
         "two big maple-seed spinners (the first stage's spinners grown bigger): three winged maple seeds joined at a "
         "round olive-brown seed knot like a three-blade propeller, papery pale tan-green seed wings with fine vein "
         "lines, the knot where the old flower centre is, about the size of the old flower; no petals, no orange",
         joint="the round seed knot at the centre of each spinner"),
       G("N08", [2], "doi", "bamboo ring with wind ribbons", "vòng tre quấn dải gió",
         "a big round wooden ring with light-green vines and small leaves twisting around it, standing behind the whole "
         "body from the hips to above the head, with big green leaf fronds along its lower part at both sides of the "
         "waist",
         "a big round ring of pale bamboo (pale straw-green with darker olive node rings every few segments), same size "
         "and place, with two white wind ribbons spiralling around it (ink outline, a few pale blue-grey swirl lines, "
         "flowing curled ends) and a few small sage leaves along its lower part; no wood grain, no vines, no glow",
         joint="bottom middle of the ring, behind the waist")],
      keep=[1], drop=[], prev="phong_linh_1",
      anim=dict(root=12, head=22, swing=[13, 8], wob=[7, 5, 11], fly=[20, 4], cast=(4, 0.5, 0.5),
                parent={15: 13, 16: 15, 17: 15, 21: 15, 9: 8}),
      note="22 đầu một mảnh (có hình con c264_1..11); hoa 4, 20 chung c216, tay 9, 21 chung c238; vòng 2 có hình con c202_1..4"),
]
