# Gió Lốc (ải 30, Hiếm): rồng chuồn chuồn. Người dùng chốt concept bằng chữ 2026-11-07.
# Gốc: 850-852 rồng xanh lá gạc nâu, vòng hào quang xanh lơ trên đầu, cánh vàng xanh, quả cầu lửa cam trong bụng,
# chóp đuôi hình lá.
# Mới: rồng thon xanh ngọc lam bụng kem, cánh chuồn chuồn bạc hà nhạt gân xanh thẫm, hai râu lông vũ thay gạc, vòng gió
# trắng thay hào quang, ngọc gió trắng xanh xoáy thay cầu lửa, chóp đuôi chuồn chuồn. 851 cánh to hơn; 852 thêm gai lưng
# trắng, cánh viền xanh thẫm.
# Cánh mỗi bên: một xương cánh (mảnh tối) + 3-4 tấm cánh; mỗi tấm thành một lá cánh chuồn chuồn dài hẹp.
GL_COL = ("a teal-jade (blue-green) body, head, fins, legs and tail, a warm cream belly, jaw and soles, pale mint dragonfly "
          "wing blades with a fine dark teal vein network, pale mint feathery antennae on teal shafts, a white wind ring, "
          "a white-and-pale-blue wind gem with a blue spiral, deep navy-blue eyes")
GL_AV = ("a banana-green or leaf-green body, brown antlers, a glowing cyan halo, an orange flame or fire ball, a glass "
         "bubble, yellow or olive wings, bat-wing membranes, a leaf-shaped or diamond tail tip, orange petal markings "
         "around the eye, red eyes")

GL_ANT_NEW = ("two feathery antennae like a moth's, rising from the same spots and leaning the same way as the antlers: a "
              "thin teal shaft with soft pale mint feather barbs on both sides, about as long as the old antlers; no brown, "
              "no antlers, no tines")
GL_RING_NEW = ("a ring of white wind floating at the same place and tilt: a thin white swirling band made of two curling "
               "wind streaks with small curled ends, ink outline and a few pale blue-grey swirl lines; flat white, no glow, "
               "no cyan")
GL_GEM_NEW = ("a round wind gem, same size and place: white and pale blue with a darker blue spiral swirl inside, flat "
              "colours; no flame, no orange, no glass shine, no glow")
GL_TAIL_NEW = ("a slim teal-jade tail with a cream underside, same curl; the tip becomes the end of a dragonfly's abdomen: "
               "three short teal segments with dark teal rings ending in two small pointed pale mint claspers, same place "
               "and size as the old tip; no leaf shape, no diamond")
GL_FIN_NEW = ("swept-back fins: the mane becomes a crest of three pointed teal fin spikes with pale mint webbing swept back "
              "to the viewer-left; the ear behind the head becomes a darker teal pointed fin ear; the small back piece a "
              "short dark teal fin; no leaf shapes, no spots")
GL_STREAM_NEW = ("two long thin teal fin streamers with pale mint edges, same place, length and curve, like trailing wind "
                 "ribbons; no leaf-green")
GL_INTRO1 = ("a slim teal dragonfly dragon with a cream belly, pale mint dragonfly wings, feathery antennae, a white wind "
             "ring above its head and a swirling wind gem on its chest")

SPEC = [
    F("gio_loc_1", 850, "Gió Lốc", 1, 3, "Gió Con", "ải 30 đảo Mộc, dạng 1/3",
      "rồng chuồn chuồn con: thân thon xanh ngọc lam bụng kem, cánh chuồn chuồn bạc hà nhạt gân xanh thẫm, hai râu lông vũ "
      "thay gạc, vòng gió trắng trên đầu, ngọc gió trắng xanh xoáy trước bụng, chóp đuôi chuồn chuồn, khăn gió bạc hà",
      "a slim young DRAGONFLY DRAGON, the first stage of a three-stage Wood evolution line",
      "hovering just above the ground with its body curled, both short legs tucked up and its tail curling down under it",
      "a bold young dragon eager to fight: brows angled down, a confident grin with a tiny fang",
      GL_COL, GL_AV,
      [G("N01", [21, 17, 23, 26, 27], "giu", "head with face", "đầu có mặt",
         "a big light-green dragon head facing the viewer-right with a long snout, a lower jaw piece under the snout "
         "(cream with a red mouth line), a small green frill under the cheek, one big red-brown eye ringed by orange-"
         "yellow petal markings",
         "a slim teal-jade dragon head with the same outline: cream lower jaw and chin, a small teal cheek frill, one big "
         "deep navy-blue eye exactly where the old eye is (one small catchlight dot), brows angled down, a small "
         "confident grin with a tiny fang; no orange petal markings, no leaf-green",
         hide=[26, 27]),
       G("N02", [19, 16], "doi", "two feathery antennae", "hai râu lông vũ",
         "two brown deer antlers with short tines growing up from the top of the head, one on the viewer-left (behind "
         "the halo) and one on the viewer-right",
         GL_ANT_NEW, joint="base of each antenna, on top of the head"),
       G("N03", [24, 22, 15, 20], "doi", "ear fins and head crest", "vây tai và mào đầu",
         "a dark green leafy mane with light spots on the viewer-left side of the head, a green leaf-shaped ear on top "
         "of the head, a dark green ear behind the head on the viewer-right, and a small dark green piece at the back of "
         "the head",
         GL_FIN_NEW + "; the ear on top becomes a pointed teal fin ear with a pale mint inner web",
         joint="where each fin meets the head"),
       G("N04", [25, 18], "doi", "white wind ring", "vòng gió trắng",
         "a thin glowing cyan halo ring floating tilted above the head, in two pieces (front arc and back arc)",
         GL_RING_NEW, joint="the ring floats tilted above the head, where the old halo is"),
       G("N05", [13, 31], "giu", "body and wind scarf", "thân và khăn gió",
         "a chubby dark green body with a big cream belly patch, and a yellow-green leaf-shaped scarf end with a small "
         "swirl rising from the chest toward the upper viewer-left",
         "a slim teal-jade dragon body with a warm cream belly marked by soft segment lines; the scarf becomes a pale "
         "mint wind streamer with a dark teal swirl, same shape and place; no leaf-green, no yellow"),
       G("N06", [30, 14], "doi", "swirling wind gem", "ngọc gió xoáy",
         "a round glass bubble in front of the belly with an orange-yellow flame inside, and a small teal-and-yellow curl "
         "above it",
         GL_GEM_NEW + "; it hangs from the small curl, which becomes a teal clasp",
         joint="the small clasp at the top of the gem, on the chest"),
       G("N07", [11, 10, 9, 8, 4, 3, 5, 2], "doi", "two dragonfly wings", "hai cánh chuồn chuồn",
         "two bat-like wings behind the body: on the viewer-left, a dark green wing-arm (8) reaching up-left from the "
         "shoulder with three yellow-green feather panels (11 big, 10 and 9 smaller) hanging under it; on the "
         "viewer-right, a dark green wing-arm (2) curving behind the neck to the right with three olive panels (4 big, 3 "
         "and 5 smaller) under it",
         "dragonfly wings: each wing-arm becomes a slim teal leading edge (the wing's front rib), and each panel becomes "
         "one long narrow dragonfly wing blade, flat pale mint with a fine dark teal vein network and a rounded tip, same "
         "place, size and direction as the panel; no yellow, no feathers, no bat-wing membrane",
         joint="root of each wing at the shoulder (the inner end of each dark wing-arm)"),
       G("N08", [29, 28, 7, 6], "giu", "two legs", "hai chân",
         "two short legs: the near leg on the viewer-left (28 a green thigh behind, 29 the leg in front with a big cream "
         "sole) and the far leg on the viewer-right (6 a dark round thigh, 7 a thin lower leg kicked up to the "
         "viewer-right, its foot at the top-right end)",
         "two short teal-jade legs with cream soles and small cream claws, same shapes, places and directions: thigh at "
         "the hip end, foot at the far end; no leaf-green"),
       G("N09", [12, 32], "doi", "tail with dragonfly tip", "đuôi chóp chuồn chuồn",
         "a long dark green tail with a cream underside curling down from the hips and around to the viewer-right, "
         "ending in a green diamond leaf-shaped tip with a yellow centre (32)",
         GL_TAIL_NEW, joint="base of the tail at the hips")],
      keep=[1], drop=[],
      anim=dict(root=13, head=21, swing=[12, 7], wob=[11, 4, 19, 16, 22, 32], fly=[], cast=(30, 0.5, 0.5),
                parent={19: 21, 16: 21, 24: 21, 22: 21, 15: 21, 20: 21, 25: 21, 18: 21, 11: 8, 10: 8, 9: 8, 4: 2, 3: 2,
                        5: 2, 29: 28, 7: 6, 32: 12}),
      note="26 vân cam quanh mắt, 27 mắt: ẩn; 18, 25 hào quang có hình con c34_1.., c71_1..; 30 cầu có hình con c11_1.."),

    F("gio_loc_2", 851, "Gió Lốc", 2, 3, "Gió Cuộn", "ải 30 đảo Mộc, dạng 2/3",
      "như dạng 1 nhưng lớn hơn, cánh chuồn chuồn to hơn: thân xanh ngọc lam bụng kem, hai râu lông vũ, vòng gió trắng, "
      "ngọc gió xoáy, chóp đuôi chuồn chuồn; hai vây gió bạc hà ở cổ, hai dải vây xanh ngọc buông ở hông",
      "a bigger DRAGONFLY DRAGON with larger wings, the SECOND stage of a three-stage Wood evolution line whose first "
      "stage is image 6: " + GL_INTRO1,
      "hovering with its big wings spread wide, both short legs raised in front of its belly and its tail curling down "
      "under it",
      "a fierce, confident dragon ready to dive: brows angled down, a sharp grin with a small fang",
      GL_COL, GL_AV,
      [G("N01", [28, 27, 30, 31, 32], "giu", "head with face", "đầu có mặt",
         "a big light-green dragon head facing the viewer-right with a pointed ear on top and two small cyan marks above "
         "the eye, a cream lower jaw under the snout, a small green cheek frill, one big red-brown eye ringed by "
         "orange-yellow petal markings",
         "a slim teal-jade dragon head with the same outline: a pointed teal ear on top, two small pale mint marks above "
         "the eye, cream lower jaw, a small teal cheek frill, one big deep navy-blue eye exactly where the old eye is "
         "(one small catchlight dot), brows angled down, a confident grin with a small fang; no orange petal markings, "
         "no leaf-green",
         hide=[31, 32]),
       G("N02", [23, 25], "doi", "two feathery antennae", "hai râu lông vũ",
         "two long brown deer antlers with short tines growing up from the top of the head, one on the viewer-left "
         "(behind the halo) and one on the viewer-right",
         GL_ANT_NEW, joint="base of each antenna, on top of the head"),
       G("N03", [29, 24, 26], "doi", "ear fins and head crest", "vây tai và mào đầu",
         "a dark green leafy mane with light spots on the viewer-left side of the head, a dark green ear behind the "
         "head on the viewer-right, and a small dark green piece at the back of the head",
         GL_FIN_NEW, joint="where each fin meets the head"),
       G("N04", [33, 22], "doi", "white wind ring", "vòng gió trắng",
         "a thin glowing cyan halo ring floating tilted above the head, in two pieces (front arc and back arc)",
         GL_RING_NEW, joint="the ring floats tilted above the head, where the old halo is"),
       G("N05", [18, 20, 8], "giu", "body and collar fins", "thân và vây cổ",
         "a dark green body with a big cream belly patch curving down, and two yellow-green leaf-shaped scarf pieces "
         "with small swirls standing up at both sides of the neck",
         "a slim teal-jade dragon body with a warm cream belly marked by soft segment lines; the two scarf pieces become "
         "two pale mint wind-streamer fins with dark teal swirls, same shapes and places; no leaf-green, no yellow"),
       G("N06", [34], "doi", "swirling wind gem", "ngọc gió xoáy",
         "a big round glass bubble in front of the belly with an orange-yellow flame inside",
         GL_GEM_NEW, joint="top of the gem, on the chest"),
       G("N07", [14, 16, 15, 13, 4, 3, 5, 6, 2], "doi", "two big dragonfly wings", "hai cánh chuồn chuồn to",
         "two big bat-like wings behind the body: on the viewer-left, a dark green wing-arm (13) reaching up-left from "
         "the shoulder with three long yellow-green panels (14, 16, 15) hanging under it; on the viewer-right, a dark "
         "green wing-arm (2) going right behind the neck with four olive panels (4 long and thin at the outer edge, 3, 5, "
         "6) under it",
         "bigger dragonfly wings than the first stage's: each wing-arm becomes a slim teal leading edge (the wing's "
         "front rib), and each panel becomes one long narrow dragonfly wing blade, flat pale mint with a fine dark teal "
         "vein network and a rounded tip, same place and direction as the panel and a little longer; no yellow, no "
         "feathers, no bat-wing membrane",
         joint="root of each wing at the shoulder (the inner end of each dark wing-arm)"),
       G("N08", [35, 19, 37, 36, 11, 10, 12], "giu", "two legs", "hai chân",
         "two short legs raised in front of the belly: the near leg on the viewer-left (19 a round green thigh; 35 the "
         "lower leg with a big cream sole running from the knee at its bottom-left end up to the toes at its top-right "
         "end; 37 and 36 two brown-and-yellow claws at the toes) and the far leg on the viewer-right (10 a round dark "
         "thigh; 11 the lower leg going up-right; 12 a small claw at its tip)",
         "two short teal-jade legs with cream soles and small cream claws, same pieces, bends and directions; no "
         "leaf-green, no brown"),
       G("N09", [7, 21], "doi", "tail with dragonfly tip", "đuôi chóp chuồn chuồn",
         "a long dark green tail with a cream underside curling down from the hips and around to the viewer-right, "
         "ending in a big green leaf-shaped tip with a yellow diamond (21)",
         GL_TAIL_NEW, joint="base of the tail at the hips"),
       G("N10", [17, 9], "doi", "two hip streamers", "hai dải vây hông",
         "two long thin green leaf-like streamers hanging down from the hips: one under the viewer-left wing (17), one "
         "under the belly (9)",
         GL_STREAM_NEW, joint="top end of each streamer, at the hips")],
      keep=[1], drop=[], prev="gio_loc_1",
      anim=dict(root=18, head=28, swing=[7, 11], wob=[14, 4, 23, 25, 21, 17, 9], fly=[], cast=(34, 0.5, 0.5),
                parent={23: 28, 25: 28, 29: 28, 24: 28, 26: 28, 33: 28, 22: 28, 14: 13, 16: 13, 15: 13, 4: 2, 3: 2,
                        5: 2, 6: 2, 35: 19, 37: 35, 36: 35, 11: 10, 12: 11, 21: 7}),
      note="31 vân cam quanh mắt, 32 mắt: ẩn; 34 cầu có hình con c226_1..17"),

    F("gio_loc_3", 852, "Gió Lốc", 3, 3, "Gió Lốc", "ải 30 đảo Mộc, dạng 3/3",
      "như dạng 2, thân dựng chữ S trên đuôi cuộn, cánh chuồn chuồn rất to viền xanh thẫm, thêm hàng gai lưng trắng; râu "
      "lông vũ cao, vòng gió trắng, ngọc gió xoáy, chóp đuôi chuồn chuồn, vây gió ở cổ, dải vây ở hông",
      "a grown DRAGONFLY DRAGON with huge dark-rimmed wings and white back spikes, the THIRD stage of a three-stage Wood "
      "evolution line whose first stage is image 6: " + GL_INTRO1,
      "rearing up tall on its coiled tail with huge wings spread wide and both short legs reaching forward to strike",
      "a proud, fierce dragon in full battle stance: brows angled down hard, narrowed eyes, a sharp confident grin "
      "with a fang",
      GL_COL + ", white back spikes, a dark teal rim on every wing blade", GL_AV,
      [G("N01", [25, 24, 27, 28, 29, 31], "giu", "head with face", "đầu có mặt",
         "a light-green dragon head facing the viewer-right with a long pointed snout, a tall pointed crest-ear at the "
         "back and a cyan swirl mark on the forehead, a cream lower jaw with a red mouth, a small green cheek frill, a "
         "narrow angry red eye ringed by orange-yellow petal markings",
         "a slim teal-jade dragon head with the same outline: a pointed teal crest-ear, a pale mint swirl mark on the "
         "forehead, cream lower jaw, a small teal cheek frill, a narrowed deep navy-blue eye exactly where the old eye "
         "is (one small catchlight dot), brows angled down hard, a confident grin with a small fang; no orange petal "
         "markings, no leaf-green",
         hide=[28, 29, 31]),
       G("N02", [20, 23], "doi", "two feathery antennae", "hai râu lông vũ",
         "two tall brown deer antlers with sharp tines growing up from the top of the head, one on the viewer-left "
         "(crossed by the halo) and one on the viewer-right",
         GL_ANT_NEW, joint="base of each antenna, on top of the head"),
       G("N03", [26, 22, 21], "doi", "ear fins and head crest", "vây tai và mào đầu",
         "a dark green leafy mane with light spots on the viewer-left side of the head, a dark green ear behind the "
         "head on the viewer-right, and a small dark green piece at the back of the head",
         GL_FIN_NEW, joint="where each fin meets the head"),
       G("N04", [30, 19], "doi", "white wind ring", "vòng gió trắng",
         "a thin jagged glowing cyan halo streak crossing above the head, in two pieces (front and back)",
         GL_RING_NEW, joint="the ring floats tilted above the head, where the old halo is"),
       G("N05", [18, 38, 13], "giu", "body with back spikes and collar fins", "thân gai lưng và vây cổ",
         "a long S-curved dark green body with a cream belly running down its front, and two yellow-green leaf-shaped "
         "collar pieces with swirls standing up at both sides of the neck",
         "a slim teal-jade S-curved body with a warm cream belly marked by soft segment lines and a row of small white "
         "back spikes along its back edge (the viewer-left edge); the two collar pieces become two pale mint "
         "wind-streamer fins with dark teal swirls, same shapes and places; no leaf-green, no yellow"),
       G("N06", [41], "doi", "swirling wind gem", "ngọc gió xoáy",
         "a round glass bubble in front of the belly with an orange-yellow flame and a green bud inside",
         GL_GEM_NEW, joint="top of the gem, on the chest"),
       G("N07", [39, 40, 15, 16, 14, 12, 9, 10, 11, 8], "doi", "two huge dragonfly wings", "hai cánh chuồn chuồn rất to",
         "two huge bat-like wings: on the viewer-left, a dark green wing-arm (14) reaching up-left from the shoulder "
         "with four panels (39 and 40 huge yellow-green crescents with zig-zag bands, 15 and 16 smaller olive panels); "
         "on the viewer-right, a dark green wing-arm (8) going right behind the neck with four olive panels (12 long and "
         "thin at the outer edge, 9, 10, 11)",
         "the first stage's dragonfly wings grown huge: each wing-arm becomes a slim teal leading edge (the wing's front "
         "rib), and each panel becomes one long dragonfly wing blade, flat pale mint with a fine dark teal vein network "
         "and a bold dark teal rim around the blade, same place, size and direction as the panel; no yellow, no zig-zag "
         "bands, no feathers, no bat-wing membrane",
         joint="root of each wing at the shoulder (the inner end of each dark wing-arm)"),
       G("N08", [33, 34, 37, 36, 35, 3, 4, 6, 5], "giu", "two legs", "hai chân",
         "two short legs reaching forward to the viewer-right: the near leg (33 a green thigh; 34 the lower leg with a "
         "cream sole going right; 37, 36, 35 three brown-and-yellow claws at its right end) and the far leg (3 a round "
         "dark thigh; 4 the lower leg going right; 6 and 5 two claws at its tip)",
         "two short teal-jade legs with cream soles and small cream claws, same pieces, bends and directions: thigh at "
         "the hip end, claws at the far right end; no leaf-green, no brown"),
       G("N09", [7, 32], "doi", "tail with dragonfly tip", "đuôi chóp chuồn chuồn",
         "a long dark green tail with a cream underside curling down from the hips and around to the viewer-right, "
         "ending in a big green leaf-shaped tip with a cyan diamond (32)",
         GL_TAIL_NEW, joint="base of the tail at the hips"),
       G("N10", [17, 2], "doi", "two hip streamers", "hai dải vây hông",
         "two long thin green leaf-like streamers hanging down from the hips: one under the viewer-left wing (17), one "
         "under the belly (2)",
         GL_STREAM_NEW, joint="top end of each streamer, at the hips")],
      keep=[1], drop=[], prev="gio_loc_1",
      anim=dict(root=18, head=25, swing=[7, 4], wob=[39, 12, 20, 23, 32, 17, 2], fly=[], cast=(41, 0.5, 0.5),
                parent={20: 25, 23: 25, 26: 25, 22: 25, 21: 25, 30: 25, 19: 25, 39: 14, 40: 14, 15: 14, 16: 14, 12: 8,
                        9: 8, 10: 8, 11: 8, 34: 33, 37: 34, 36: 34, 35: 34, 4: 3, 6: 4, 5: 4, 32: 7}),
      note="28, 29 vân cam quanh mắt, 31 mắt: ẩn; 41 cầu có hình con c221_1..3"),
]
