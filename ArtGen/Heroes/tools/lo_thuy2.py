"""Đảo Thủy lô 2 (5 dòng boss, 15 dạng), 2026-11-07 đêm: người dùng ủy quyền làm một mạch, Claude tự chốt concept.

Mỗi dạng khai gọn: nhóm mảnh (mảnh, kiểu, tên, cũ là gì, mới thành gì) và vài câu thiết kế. Script ghi cho từng dạng:
  <aola>/reskin/thuy_<id>/regions.json, groups.json, ghep.json (vùng concept = nhóm), chạy dung_rig.py (ảnh rig, chép sang
  refs/thuy/<mã>/), tính độ dày viền mỗi nhóm (0,85% chiều cao con × k), rồi ghi ArtGen/Heroes/forms_thuy_lo2.json mà
  build.py nạp thêm vào FORMS.

    py -3 -I ArtGen/Heroes/tools/lo_thuy2.py [mã ...]
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HEROES = os.path.normpath(os.path.join(HERE, ".."))
AOLA = None
for cand in ("D:/Aola-20261029T161238Z-1-001/Aola/AolaRipper/AolaRipper", "E:/ProjectAtomik/aola"):
    if os.path.isdir(cand):
        AOLA = cand
        break
sys.stdout.reconfigure(encoding="utf-8")

# nhóm: (mã, mảnh, kiểu "giu"/"doi", tên en, tên vi, cũ en, mới en, khớp (đổi dáng) hoặc None)
L = []


def form(code, aola, hero, n, forms, name, role, design_vi, intro, stance, attitude, colours, avoid, groups, keep=(1,),
         drop=(), prev=None, ghep=None):
    L.append(dict(code=code, aola=aola, hero=hero, form=n, forms=forms, form_name=name, role=role, design_vi=design_vi,
                  intro=intro, stance=stance, attitude=attitude, colours=colours, avoid=avoid, groups=groups,
                  keep=list(keep), drop=list(drop), prev=prev, ghep=ghep or {}))


# ---------------- Vây Lam: cá mập rẽ sóng (mini boss ải 30) ----------------
VL = ("a cobalt-blue back, a snow-white belly with round white spots on the blue, fins edged in saffron yellow, big "
      "saffron-amber eyes")
form("vay_lam_1", 546, "Vây Lam", 1, 3, "Cá Đốm", "mini boss ải 30 đảo Thủy, dạng 1/3",
     "cá mập con tròn vo cuộn trong quả trứng bong bóng nước (chỉ viền), lưng xanh coban đốm trắng, bụng trắng, vây viền vàng nghệ, mắt hổ phách",
     "a round baby SHARK PUP of the wave-splitter line, curled up inside a water-bubble egg, the first stage of a three-stage Water evolution line",
     "floating a little above the ground", "a brave round shark pup ready to burst out and bite: brows angled down, a small fang showing",
     VL + "; a very pale aqua tint in the bubble", "a green or teal fish, a yellow belly band, a glass sphere with shine",
     [("N01", [3, 2, 12], "giu", "water bubble egg", "quả trứng bong bóng", "a big round green bubble sphere with shine spots around the fish",
       "a big round water bubble drawn with only a thin dark-brown ink outline and a very light, even aqua tint, see-through; no shine", None),
      ("N02", [5, 6, 7, 8, 9, 10, 11, 4], "giu", "round shark pup with face", "cá mập con có mặt",
       "a round blue and yellow fish with a fin on top, two big black eyes and a small mouth",
       "a round chubby shark pup: cobalt-blue back with round white spots, snow-white belly, a small dorsal fin edged in saffron yellow on top, two big saffron-amber eyes (one catchlight dot each) where the old eyes are, brows angled down, a small fang", None),
      ("N03", [13, 14], "giu", "two small bubbles", "hai bong bóng nhỏ", "two small green bubbles with shine",
       "two simple bubbles with a thin ink outline and a very light aqua tint, no shine", None)])
form("vay_lam_2", 547, "Vây Lam", 2, 3, "Cá Song Tiễn", "mini boss ải 30 đảo Thủy, dạng 2/3",
     "cá mập thon xanh coban bụng trắng đốm trắng, mũ giáp vỏ ốc vàng nghệ có sừng, hai mũi tên nước (song tiễn) bay hai bên, vây viền vàng",
     "the SECOND stage of a three-stage Water evolution line whose first stage is image 6: the round shark pup has grown into a sleek TWIN-ARROW SHARK guarded by two floating water arrowheads",
     "leaping up from the ground", "a fierce young shark leaping to strike: brows angled down, a confident fanged grin",
     VL + "; a saffron-yellow shell helmet; two floating arrowheads of clear blue water with white foam edges",
     "a green or teal body, a dark green helmet, leaf-shaped shields, a gold neck band",
     [("N01", [5, 16, 14, 15], "giu", "head with helmet and face", "đầu có mũ và mặt",
       "a teal shark head with a dark green horned helmet, a blue face band and a red eye",
       "the shark head: cobalt-blue top with white spots, snow-white jaw with a fanged grin, a saffron-amber eye (one catchlight dot) where the old eye is, brow angled down, wearing a saffron-yellow spiral-shell helmet with two short horns", None),
      ("N02", [8, 11], "giu", "body", "thân", "a teal body with a gold band at the neck",
       "a sleek cobalt-blue body with white spots and a snow-white belly; a saffron-yellow shell band at the neck", None),
      ("N03", [3], "doi", "dorsal fin", "vây lưng", "a tall teal dorsal fin", "a tall cobalt-blue dorsal fin edged in saffron yellow", "base of the fin"),
      ("N04", [10, 4], "giu", "two side fins", "hai vây bên", "two teal side fins", "two cobalt-blue side fins edged in saffron yellow", None),
      ("N05", [7, 6], "giu", "tail", "đuôi", "a teal tail bending down with a small tip", "a cobalt-blue tail with white spots ending in a saffron-edged tail fin", None),
      ("N06", [12, 13, 2, 9], "doi", "two floating water arrowheads", "hai mũi tên nước",
       "two floating teal leaf-shaped shields with gold centres and two tiny bubbles",
       "two floating arrowheads made of clear blue water with white foam edges, pointing forward, each where an old shield is; the two tiny bubbles stay as small plain bubbles", "centre of each arrowhead")],
     prev="vay_lam_1")
form("vay_lam_3", 548, "Vây Lam", 3, 3, "Cá Mập Vây Lam", "mini boss ải 30 đảo Thủy, dạng 3/3",
     "cá mập lớn rẽ sóng: lưng xanh coban đốm trắng, bụng trắng, mũ vỏ ốc vàng nghệ, quanh mình bay nhiều vây lưỡi sóng xanh bọt trắng",
     "the THIRD and final stage of a three-stage Water evolution line whose first stage is image 6: the WAVE-SPLITTER SHARK, a big proud shark surrounded by many floating blade-fins made of rushing water",
     "surging forward above the ground", "a proud shark lord cutting through the waves: brows angled down, a fanged grin",
     VL + "; blade-fins of clear blue water with white foam edges", "an ice or crystal body, glassy shards, dark navy, metal",
     [("N01", [16, 18, 17, 22, 19, 20, 21, 15, 13, 14], "giu", "head and body", "đầu và thân",
       "a big shark body made of pale blue crystal with a darker head, a green eye and white teeth",
       "a big shark: cobalt-blue back with white spots, snow-white belly and jaw with a fanged grin, a saffron-amber eye where the old eye is, a saffron-yellow spiral-shell helmet on the head", None),
      ("N02", [9, 10, 11, 12, 24, 25, 26, 27], "doi", "upper blade-fins", "vây lưỡi sóng trên",
       "pale blue crystal shards floating above the shark, with dark inner panels",
       "blade-fins made of rushing blue water with white foam edges, each where an old shard is, pointing the same way", "centre of each blade"),
      ("N03", [28, 29, 30, 31, 32, 33, 23], "doi", "side blade-fins", "vây lưỡi sóng bên",
       "pale blue crystal shards floating at the left side", "blade-fins of rushing blue water with white foam edges, each where an old shard is", "centre of each blade"),
      ("N04", [2, 3, 4, 5, 6, 7, 8], "doi", "lower blade-fins", "vây lưỡi sóng dưới",
       "pale blue crystal shards under the shark", "blade-fins of rushing blue water with white foam edges, each where an old shard is", "centre of each blade")],
     prev="vay_lam_1")

# ---------------- Kuba: mai cứng kim cương (mini boss ải 40) ----------------
KB = ("coral-salmon skin, violet seaweed hair, a sand-gold spiral conch shell with cream bands, big teal eyes, small "
      "white-and-aqua diamond crystals")
KB_AV = "green hair, a blue striped shell, blue-grey skin, a fluffy bubble scarf, a human face"
form("kuba_1", 94, "Kuba", 1, 3, "Kuba", "mini boss ải 40 đảo Thủy, dạng 1/3",
     "ốc mượn hồn con: da cam san hô, tóc tảo tím, mang vỏ ốc xoắn vàng cát to sau lưng, khăn cổ bọt biển, mắt xanh ngọc",
     "a little HERMIT-CRAB SPRITE with a big spiral conch shell on its back, the first stage of a three-stage Water evolution line",
     "standing on the ground", "a stubborn little hermit sprite ready to headbutt: brows angled down, cheeks puffed, a small grin",
     KB + "; a pale foam-white sea-sponge scarf", KB_AV,
     [("N01", [19, 17], "doi", "big shell", "vỏ ốc to", "a big round blue striped shell behind the creature",
       "a big sand-gold spiral conch shell with cream bands and a pointed spiral tip, as big as the old shell and in the same place", "bottom of the shell (where it sits on the back)"),
      ("N02", [18, 20, 22, 23, 24, 25, 10, 11], "giu", "head with face", "đầu có mặt",
       "a blue-grey head with two yellow eyes and a red open mouth",
       "a round coral-salmon head with two big teal eyes (one catchlight dot each) where the old eyes are, brows angled down, a small grin where the old mouth is", None),
      ("N03", [51, 52, 53, 54, 55, 56, 48, 49, 50], "doi", "hair", "tóc", "spiky green hair on top of the head",
       "short spiky violet seaweed hair, the same spikes and places", "root of the hair (on the head)"),
      ("N04", [27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 43, 47], "giu", "scarf", "khăn cổ",
       "a fluffy pale blue bubble scarf around the neck", "a puffy foam-white sea-sponge scarf with small holes, the same outline", None),
      ("N05", [14, 15, 12, 13, 16, 21, 26, 44, 7, 9], "giu", "body and arms", "thân và tay",
       "a small dark body with a cream belly and short arms", "a small coral-salmon body with a cream belly and short coral-salmon arms with tiny pincer hands", None),
      ("N06", [39, 40, 41, 42, 45, 46, 2, 3, 4, 5, 6, 8], "giu", "feet", "bàn chân", "two small feet with blue bits",
       "two small coral-salmon feet with cream toes", None),
      ("N07", [57, 58, 59, 60, 61, 62], "giu", "water drops", "giọt nước", "small blue water drops around the creature",
       "small water drops of light blue with a thin deeper-blue rim, flat, no shine", None)])
form("kuba_2", 95, "Kuba", 2, 3, "Kuba Vỏ Cứng", "mini boss ải 40 đảo Thủy, dạng 2/3",
     "ốc mượn hồn chiến binh: vỏ ốc xoắn vàng cát gai cứng trên lưng, càng phải to cam đỏ, tóc tảo tím, đuôi gai",
     "the SECOND stage of a three-stage Water evolution line whose first stage is image 6: the hermit sprite has grown into a HARD-SHELL BRAWLER with a spiked conch on its back and one big pincer",
     "crouching in a fighting stance", "a tough brawler ready to smash with its big pincer: brows angled down, a fierce grin",
     KB + "; a big orange-red pincer", KB_AV + ", a dark horn",
     [("N01", [13], "doi", "spiked shell on the back", "vỏ ốc gai", "a big pale shell with an orange pattern on the back",
       "a big sand-gold spiral conch with cream bands and short blunt spikes, in the same place", "bottom of the shell"),
      ("N02", [17, 18, 19, 20, 21, 22, 23, 24, 25, 34, 15, 16, 14], "giu", "head with face", "đầu có mặt",
       "a blue-grey head with two yellow eyes, a dark horn at the right", "a coral-salmon head with two big teal eyes where the old eyes are, brows angled down, a fierce grin; the horn becomes a small violet seaweed lock", None),
      ("N03", [26, 27, 28, 30], "doi", "hair", "tóc", "big spiky green hair", "big spiky violet seaweed hair", "root of the hair"),
      ("N04", [29, 31, 12, 2], "giu", "scarf", "khăn", "a blue scarf at the neck", "a foam-white sea-sponge scarf", None),
      ("N05", [3, 4, 5, 6, 7, 9], "doi", "big pincer arm", "càng to", "a right arm with a pale claw-like hand",
       "a coral-salmon arm ending in one big orange-red pincer with saw-toothed jaws, the pincer where the old hand is", "shoulder end"),
      ("N06", [10, 11, 35, 32, 33, 36], "giu", "body and legs", "thân và chân", "a small body and two short legs",
       "a coral-salmon body with a cream belly, two short legs with cream toes", None),
      ("N07", [8], "giu", "spiked tail", "đuôi gai", "a long grey tail with a spike at its tip", "a coral-salmon tail with small sand-gold shell plates and a spiral shell tip", None),
      ("N08", [37], "giu", "water splash", "bụi nước", "a faint water splash effect", "small flat water drops of light blue with a thin deeper-blue rim", None)],
     prev="kuba_1")
form("kuba_3", 96, "Kuba", 3, 3, "Kuba Kim Cương", "mini boss ải 40 đảo Thủy, dạng 3/3",
     "ốc mượn hồn vua kim cương: vỏ ốc vàng cát mọc tinh thể kim cương trắng xanh, tóc tảo tím dài, khăn bọt biển, khăn sọc tảo, đuôi gai",
     "the THIRD and final stage of a three-stage Water evolution line whose first stage is image 6: the DIAMOND-SHELL KING, a big hermit giant whose conch is crowned with white-and-aqua diamond crystals",
     "standing tall", "a proud diamond-shell king: brows angled down, a confident grin, chest out",
     KB + "; big flat diamond crystals of white and aqua", KB_AV + ", orange crystals",
     [("N01", [8, 10, 11, 12], "doi", "diamond-crowned shell", "vỏ ốc kim cương",
       "a huge green shell with an orange-red pattern and orange crystal spikes on top and at the left",
       "a huge sand-gold spiral conch with cream bands, crowned with big flat white-and-aqua diamond crystals where the old orange crystals are", "bottom of the shell"),
      ("N02", [15, 16, 17, 19, 20, 21, 25], "giu", "face", "mặt", "a blue-grey face with two eyes and a cream mouth",
       "a coral-salmon face with two big teal eyes where the old eyes are, brows angled down, a confident grin", None),
      ("N03", [18, 14, 9], "doi", "hair", "tóc", "big spiky green hair with brown locks at the right", "long spiky violet seaweed hair", "root of the hair"),
      ("N04", [22, 24, 6], "giu", "scarf", "khăn", "a fluffy pale blue feather collar", "a puffy foam-white sea-sponge collar", None),
      ("N05", [26, 27, 4, 5, 3, 2, 13, 23], "giu", "body, sash and legs", "thân, khăn sọc và chân",
       "a big grey-blue body with a long green striped sash and two thick legs",
       "a coral-salmon body with a cream belly, a long violet-and-seaweed-green striped sash, two thick coral-salmon legs with cream toes", None),
      ("N06", [7], "giu", "spiked tail", "đuôi gai", "a grey tail with a spike", "a coral-salmon tail with sand-gold shell plates and a spiral shell tip", None),
      ("N07", [28, 29], "giu", "water drops", "giọt nước", "two small water drops", "two small flat light-blue water drops", None)],
     prev="kuba_1")

# ---------------- Thương Lam: rồng lam cánh băng (mini boss ải 50, boss cuối 3) ----------------
TL = ("snow-white and pale ice-blue scales, deep teal markings, frost-white wing fins with ice-blue veins, silver horns, "
      "a pale cyan snowflake gem")
TL_AV = "royal-blue scales, a red gem, gold armour, a human face"
form("thuong_lam_1", 805, "Thương Lam", 1, 3, "Thương", "mini boss ải 50 đảo Thủy, dạng 1/3",
     "rồng biển băng con dáng hải cẩu: vảy trắng tuyết xanh băng, vân xanh mòng két, vây cánh băng trắng gân xanh, ngọc hoa tuyết trên ngực",
     "a little ICE SEA-DRAGON PUP shaped like a baby seal with frost wing fins, the first stage of a three-stage Water evolution line",
     "sitting up on the ground", "a proud little ice dragon puffing its chest: brows angled down, a small confident smile",
     TL, TL_AV,
     [("N01", [13, 15, 16, 12, 14], "giu", "head with crest and face", "đầu có mào và mặt",
       "a blue head with a big pale fin crest at the left, a yellow eye and two small ears",
       "a snow-white and pale ice-blue head with a frost-white fin crest with ice-blue veins at the left, a big icy-teal eye (one catchlight dot) where the old eye is, brow angled down, two small silver horn-ears", None),
      ("N02", [5, 3, 6, 4, 11, 18], "giu", "body with gem", "thân và ngọc",
       "a blue seal-like body with a white chest, a red gem and a small gold piece",
       "a snow-white body with pale ice-blue back and deep teal markings, a pale cyan snowflake gem on the chest set in silver", None),
      ("N03", [17], "doi", "frost wing fin", "vây cánh băng", "a big pale wing fin", "a big frost-white wing fin with ice-blue veins and pointed icicle tips", "root of the wing"),
      ("N04", [9, 7, 8], "giu", "tail", "đuôi", "a blue tail with a pale tail fin", "a pale ice-blue tail with a frost-white tail fin", None),
      ("N05", [10, 2], "giu", "flippers", "chân chèo", "two blue flippers", "two pale ice-blue flippers with deep teal tips", None)])
form("thuong_lam_2", 806, "Thương Lam", 2, 3, "Thương Nhiễm", "mini boss ải 50 đảo Thủy, dạng 2/3",
     "rồng biển băng bay: vảy trắng tuyết, bờm vây băng, sừng bạc, cánh băng lớn, giáp ngực bạc ngọc hoa tuyết",
     "the SECOND stage of a three-stage Water evolution line whose first stage is image 6: the ice pup has grown into a FLYING ICE SEA-DRAGON with frost wings",
     "flying low above the ground", "a fierce young ice dragon gliding in to strike: brows angled down, a fanged grin",
     TL, TL_AV,
     [("N01", [9, 7, 2, 3], "giu", "head with mane and face", "đầu có bờm và mặt",
       "a blue dragon head with swept-back fin mane, a yellow eye, a long snout",
       "a snow-white dragon head with a swept-back mane of frost fins, short silver horns, an icy-teal eye where the old eye is, brow angled down, a fanged grin", None),
      ("N02", [6, 8, 4], "giu", "body and front flipper", "thân và chân chèo", "a blue body with a pale belly and a front flipper",
       "a snow-white body with pale ice-blue back and deep teal markings, a pale ice-blue front flipper", None),
      ("N03", [10], "doi", "frost wing", "cánh băng", "a big pale wing", "a big frost-white wing with ice-blue veins and icicle tips", "root of the wing"),
      ("N04", [11], "doi", "chest guard with gem", "giáp ngực ngọc", "a gold and red gem armour", "a silver chest guard with a pale cyan snowflake gem", "centre of the guard"),
      ("N05", [5], "giu", "tail with fins", "đuôi có vây", "a long blue tail ending in leaf fins", "a long pale ice-blue tail with deep teal markings ending in frost-white leaf fins", None)],
     prev="thuong_lam_1")
form("thuong_lam_3", 807, "Thương Lam", 3, 3, "Thương Lam", "mini boss ải 50 đảo Thủy, dạng 3/3",
     "rồng băng lam trưởng thành: vảy trắng tuyết, đôi cánh băng pha lê lớn, sừng bạc dài, râu băng, đuôi gai băng có lưỡi hoa tuyết, giáp ngực bạc ngọc hoa tuyết",
     "the THIRD and final stage of a three-stage Water evolution line whose first stage is image 6: the ICE-WINGED BLUE DRAGON, a majestic sea dragon with two great frost-crystal wings",
     "rearing up above the ground", "a majestic ice dragon about to unleash a frost torrent: brows angled down, jaws a little open",
     TL, TL_AV + ", gold star-shaped blades",
     [("N01", [26, 27, 28, 29, 30, 32, 33, 34, 2], "giu", "head with horns and whiskers", "đầu có sừng và râu",
       "a blue dragon head at the upper right with dark crests, long whiskers and a tall pale mane",
       "a snow-white dragon head with long silver horns, frost-white whisker fins, an icy-teal eye where the old eye is, brow angled down", None),
      ("N02", [15, 20], "doi", "two frost-crystal wings", "đôi cánh băng", "two big wings, one blue and one pale green",
       "two great frost-crystal wings, frost-white with ice-blue veins and pointed icicle edges", "root of each wing"),
      ("N03", [16, 17, 18, 19, 31], "giu", "neck and body", "cổ và thân", "a long blue neck and body",
       "a long snow-white neck and body with pale ice-blue back and deep teal markings", None),
      ("N04", [9, 10, 11, 25, 14], "giu", "tail", "đuôi", "a dark segmented tail running to the left",
       "a pale ice-blue segmented tail with deep teal bands", None),
      ("N05", [3, 12, 8, 4, 5, 6, 7], "doi", "tail blade and fins", "lưỡi đuôi và vây",
       "a gold star-shaped blade at the tail end and pale leaf fins", "a snowflake-shaped ice blade at the tail end and frost-white leaf fins", "base of the blade"),
      ("N06", [22, 23, 24], "doi", "chest guard with gem", "giáp ngực ngọc", "a gold armour with a red gem",
       "a silver chest guard with a pale cyan snowflake gem", "centre of the guard"),
      ("N07", [13, 21], "giu", "legs", "chân", "two pale blue legs with fin tips", "two pale ice-blue legs with frost-white fin tips", None)],
     prev="thuong_lam_1")

# ---------------- Huyền Vũ: thần thú phương Bắc (mini boss ải 60, boss cuối 2) ----------------
HV = ("pale jade-green skin, a charcoal-black shell with bronze-gold hexagon lines, bronze trim, deep teal eyes, a "
      "black pearl")
HV_AV = "a cream or tan turtle, a blue shell, green or orange crystals, a gold crown, a human face"
form("huyen_vu_1", 713, "Huyền Vũ", 1, 3, "Rùa Ngọc", "mini boss ải 60 đảo Thủy, dạng 1/3",
     "rùa con thần: da ngọc bích nhạt, mai đen than viền đồng vàng hoa văn lục giác, mào vây xanh rêu, ngọc trai đen bay trên đầu",
     "a little SPIRIT TURTLE of the north sea, the first stage of a three-stage Water evolution line", "crawling forward on the ground",
     "a brave little spirit turtle with a serious face: brows angled down, a determined small mouth",
     HV + "; a small moss-green fin crest", HV_AV,
     [("N01", [7, 3, 8, 9, 6, 21], "giu", "shell", "mai", "a blue shell with green crystals on it",
       "a charcoal-black shell with bronze-gold hexagon lines and a bronze rim; where the crystals are, small bronze-capped shell knobs", None),
      ("N02", [12, 13, 14, 15, 16, 17, 18, 19, 20, 11], "giu", "head with face", "đầu có mặt",
       "a cream turtle head with big blue eyes and orange brows",
       "a pale jade-green turtle head with big deep teal eyes (one catchlight dot) where the old eyes are, dark brows angled down", None),
      ("N03", [10], "doi", "crest", "mào", "a gold crown on the head", "a small moss-green fin crest with three rounded points", "base of the crest"),
      ("N04", [5, 4, 2], "giu", "legs", "chân", "three cream legs", "three pale jade-green legs with bronze claws", None),
      ("N05", [22], "doi", "black pearl", "ngọc trai đen", "a green jade orb floating above", "a round black pearl with a thin bronze ring around it", "centre of the pearl")])
form("huyen_vu_2", 714, "Huyền Vũ", 2, 3, "Rùa Biển Ngọc", "mini boss ải 60 đảo Thủy, dạng 2/3",
     "rùa biển lớn: mai đen than hoa văn đồng vàng mọc gai đá đen viền đồng, da ngọc bích, chân chèo",
     "the SECOND stage of a three-stage Water evolution line whose first stage is image 6: the spirit turtle has grown into a great SEA TURTLE whose shell bristles with black stone spikes",
     "swimming low above the ground", "a calm but dangerous sea turtle: brows angled down, a stern mouth",
     HV, HV_AV + ", a pink starfish",
     [("N01", [13, 3, 9], "giu", "shell", "mai", "a big green shell with a pink starfish on top",
       "a big charcoal-black shell with bronze-gold hexagon lines and a bronze rim", None),
      ("N02", [11, 14, 15, 22, 25, 4, 7, 12, 5], "doi", "shell spikes", "gai mai", "orange and blue crystals on the shell",
       "black stone spikes with bronze tips, each where an old crystal is", "base of each spike"),
      ("N03", [16, 17, 18, 19, 20, 21, 23, 24], "giu", "head with face", "đầu có mặt", "a pale green turtle head with orange eyes and a green fin",
       "a pale jade-green turtle head with deep teal eyes where the old eyes are, brows angled down, a moss-green fin", None),
      ("N04", [2, 10, 6, 8], "giu", "flippers and belly", "chân chèo và bụng", "pale flippers and a pale belly",
       "pale jade-green flippers with darker jade spots and a pale jade belly", None)],
     prev="huyen_vu_1")
form("huyen_vu_3", 715, "Huyền Vũ", 3, 3, "Huyền Vũ", "mini boss ải 60 đảo Thủy, dạng 3/3",
     "thần rùa Huyền Vũ đứng: mai đen than gai đá viền đồng, râu dài trắng, sừng đồng, đai thừng, cầm mái chèo gỗ lũa to",
     "the THIRD and final stage of a three-stage Water evolution line whose first stage is image 6: HUYEN VU, the ancient guardian turtle of the north sea, standing upright and holding a huge driftwood oar",
     "standing upright", "an ancient guardian, calm and mighty: brows angled down, a stern mouth under a long beard",
     HV + "; a long white beard; a driftwood-brown oar", HV_AV + ", a wooden club",
     [("N01", [14], "doi", "driftwood oar", "mái chèo gỗ lũa", "a big brown wooden paddle held up at the left",
       "a huge driftwood oar, weathered brown wood with a bronze band, the blade at the top", "grip near the bottom"),
      ("N02", [3, 13, 31, 4, 6, 7], "giu", "shell and back plates", "mai và giáp lưng", "a big blue shell with plates and spikes",
       "a charcoal-black shell with bronze-gold hexagon lines, black stone spikes with bronze tips", None),
      ("N03", [12, 33, 34, 35, 36, 37, 38, 39, 32], "giu", "head with beard and horn", "đầu có râu và sừng",
       "a blue turtle head with a white beard, a horn and swept hair", "a pale jade-green turtle head with a long white beard, a bronze horn, deep teal eyes, brows angled down", None),
      ("N04", [5, 19, 24, 25, 26, 27, 28, 29], "giu", "belly and rope belt", "bụng và đai thừng", "a pale belly plate with a red and white rope belt",
       "a pale jade belly plate with a bronze-and-black rope belt", None),
      ("N05", [8, 30, 9, 10, 11, 2], "giu", "arms", "tay", "two arms with blue plates", "two pale jade-green arms with charcoal shell plates trimmed in bronze", None),
      ("N06", [15, 16, 17, 18, 20, 21, 22, 23], "giu", "legs", "chân", "two thick legs with blue plates", "two thick pale jade-green legs with charcoal shell plates and bronze claws", None)],
     prev="huyen_vu_1")

# ---------------- Lam Quân: tiểu tướng chuông đồng (boss ải 70, boss cuối 1) ----------------
LQ = ("warm brown otter fur, a cream face and belly, bronze-gold armour, a deep teal cape lining, coral-red accents")
LQ_AV = "blue fox ears, a black crescent helmet, a human face, a human body"
form("lam_quan_1", 1831, "Lam Quân", 1, 3, "Lam Quân", "boss ải 70 đảo Thủy, dạng 1/3",
     "rái cá biển tiểu tướng: lông nâu ấm, mặt bụng kem, mũ hình chuông đồng có tua san hô, cầm đinh ba san hô, chuông đồng lớn bên cạnh",
     "a little SEA-OTTER GENERAL who rings a great bronze bell to command the tides, the first stage of a three-stage Water evolution line",
     "standing in a ready stance", "a cocky little general shouting a war cry: brows angled down, mouth open in a shout",
     LQ + "; a coral-red trident", LQ_AV,
     [("N01", [14], "doi", "head with bell helmet", "đầu có mũ chuông",
       "a big blue head with a black and gold crescent helmet with feathers, big eyes, an open mouth",
       "a round otter head (warm brown fur, cream face, big deep teal eyes, brows angled down, mouth open in a war cry) under a bronze helmet shaped like a small bell with a coral-red tassel on top", "bottom of the head (the neck)"),
      ("N02", [7], "doi", "great bronze bell", "chuông đồng lớn", "a big gold and blue bell standing at the left",
       "a great bronze bell with a deep teal wave band and a coral-red rope, in the same place and size", "centre of the bell"),
      ("N03", [17, 2, 3, 4, 16, 18, 19], "giu", "trident and hands", "đinh ba và tay",
       "a long silver trident held across the body with black-gloved hands", "a coral-red trident held across the body by small brown otter paws", None),
      ("N04", [5, 6, 8, 9, 15, 11], "giu", "body with armour", "thân có giáp", "a small dark armoured body",
       "a small otter body with a cream belly, a bronze chest plate and a deep teal sash", None),
      ("N05", [10, 12, 13], "giu", "legs", "chân", "two short dark legs", "two short brown otter legs with bronze greaves", None)])
form("lam_quan_2", 1832, "Lam Quân", 2, 3, "Vạn Quân", "boss ải 70 đảo Thủy, dạng 2/3",
     "rái cá đại tướng: giáp đồng, mũ chuông có cánh tua, áo choàng xanh mòng két, đinh ba dài, chuông đồng khổng lồ, quả cầu nước",
     "the SECOND stage of a three-stage Water evolution line whose first stage is image 6: the otter has grown into a TIDE GENERAL in bronze armour with a giant bell and a long trident",
     "in a wide battle stance", "a fierce general commanding the tide: brows angled down, a battle shout",
     LQ + "; a long coral-red trident; swirls of clear blue water", LQ_AV + ", black wings on the helmet",
     [("N01", [24, 3, 25], "doi", "head with helmet", "đầu có mũ", "a blue head with a black winged helmet",
       "an otter head (brown fur, cream face, deep teal eyes, brows angled down) in a bronze bell-shaped helmet with two swept bronze fins", "bottom of the head"),
      ("N02", [2], "giu", "water swirl", "xoáy nước", "a big water swirl behind at the left", "a big curling swirl of clear blue water with white foam", None),
      ("N03", [28, 29, 36, 38, 35], "doi", "giant bell", "chuông khổng lồ", "a giant gold and blue bell at the right",
       "a giant bronze bell with a deep teal wave band, in the same place and size", "top of the bell"),
      ("N04", [27, 23, 26], "doi", "long trident", "đinh ba dài", "a long spear with gold blades",
       "a long coral-red trident with bronze prongs along the same line", "middle of the shaft"),
      ("N05", [37], "giu", "water orb", "quả cầu nước", "a blue water orb with splashes", "a ball of churning blue water with white foam curls", None),
      ("N06", [4, 5, 6, 7, 8, 9, 10, 14, 15, 16, 17, 18, 19, 20, 30, 21, 22, 31], "giu", "body and arms in armour", "thân và tay có giáp",
       "a dark armoured body and arms", "a brown otter body and arms in bronze-gold armour with a deep teal sash and cape lining", None),
      ("N07", [11, 12, 13, 32, 33, 34], "giu", "legs", "chân", "two armoured legs", "two brown otter legs in bronze greaves", None)],
     prev="lam_quan_1")
form("lam_quan_3", 2955, "Lam Quân", 3, 3, "Hắc Dực Vạn Quân", "boss ải 70 đảo Thủy, dạng 3/3",
     "rái cá thống soái cánh đen: giáp đồng đen, đôi cánh cá đuối đen tím, áo choàng tím than, chuông đồng đen khổng lồ, quầng nước tím than",
     "the THIRD and final stage of a three-stage Water evolution line whose first stage is image 6: the BLACK-WINGED TIDE MARSHAL, an otter warlord with manta-ray wings and a giant dark bronze bell, wrapped in swirling midnight water",
     "floating in a commanding pose", "a dark majestic warlord: brows angled down, a cold confident smile",
     "warm brown otter fur, a cream face, dark bronze armour with gold trim, midnight-navy and violet manta wings, midnight-violet water swirls",
     LQ_AV + ", purple flames, glowing aura",
     [("N01", [28], "doi", "giant dark bell", "chuông đen khổng lồ", "a giant bell with gold trim at the left, with a purple aura",
       "a giant dark-bronze bell with gold trim and a midnight wave band, in the same place and size", "top of the bell"),
      ("N02", [2, 1], "giu", "water swirls", "xoáy nước", "purple flame-like water swirls at the top right and on the ground",
       "swirls of midnight-violet water with white foam curls, flat colours, no glow", None),
      ("N03", [4], "giu", "cape", "áo choàng", "a long purple cape", "a long midnight-navy cape with a violet lining", None),
      ("N04", [9, 10, 29, 3, 6, 11, 14, 22], "giu", "head, wings and shoulders", "đầu, cánh và vai",
       "a dark armoured head with spiky crests and shoulder plates", "an otter head (brown fur, cream face, deep teal eyes, brows angled down) in a dark-bronze helmet, two midnight-navy manta-ray wings and dark-bronze shoulder plates", None),
      ("N05", [5, 7, 8, 12, 13, 15, 16, 17, 18, 19, 25, 27], "giu", "body and arms", "thân và tay", "a dark armoured body and arms",
       "an otter body and arms in dark-bronze armour with gold trim", None),
      ("N06", [20, 21, 23, 24, 26], "giu", "legs", "chân", "two armoured legs", "two brown otter legs in dark-bronze greaves", None)],
     keep=(), prev="lam_quan_1")


# ---------------- sinh file ----------------
def concept_text(f):
    gs = f["groups"]
    keep = "; ".join(f"{i} {g[3]}" for i, g in enumerate(gs, 1))
    change = "\n".join(f"{i} {g[3]}: {g[6]}." for i, g in enumerate(gs, 1))
    prev = (" Image 6 is the approved first stage of this creature: keep its colours, face and drawing style; this stage is "
            "the same creature grown up.") if f["prev"] else ""
    return (f"Character concept for a 2D cut-out animation game. Draw ONE original creature: {f['intro']}, in the same view "
            f"and pose as image 1, {f['stance']}, on a plain white background. A cute, chunky creature, but an original design "
            "that must look clearly DIFFERENT from the figure the silhouette came from; not any existing character.\n\n"
            "Image 1 (grey silhouette) and image 2 (the same figure split into numbered regions) show the PUPPET RIG the new "
            "creature will be animated on. They tell you where each part and joint is, NOT what the creature looks like: do "
            "not trace their outline. Viewer-left and viewer-right mean as seen in the picture.\n\n"
            "KEEP FROM THE RIG (the animation moves these parts around these joints):\n"
            f"- the same parts, no more, no fewer, each where its numbered region is: {keep};\n"
            "- every joint where it is and every part pointing the same way as in image 1; eyes where the old eyes are;\n"
            "- each part about the size and shape of its region; the whole figure about the same size.\n\n"
            f"CHANGE (the new look, region by region):\n{change}\n\n"
            f"ATTITUDE: {f['attitude']}; cute, never scary, never a cheerful mascot.\n\n"
            "{RENDER}\n{DESIGN}\n"
            "The style sheet is image 3; the hand-drawn map is image 4. Image 5 is an approved character of this game: copy "
            "its ink line weight and its pencil and crayon texture, not its design; it has a few white shine spots and some "
            f"darker shading: do NOT copy those.{prev}\n\n"
            f"COLOURS: {f['colours']}. Few colours.\n\n"
            f"AVOID: {f['avoid']}, text, labels, numbers, the region colours, frames, background scenery, a second view, "
            "shading, shadows, white highlights, glossy shine, glow, gradients.")


def group_tuple(g, px):
    code, parts, kind, en, vi, old, new, joint = g
    n = len(parts)
    pieces = "one piece" if n == 1 else f"{n} pieces"
    keep = ", with the same outline" if kind == "giu" else ""
    prompt = (f"Image 1 is {pieces} of a 2D cut-out animation puppet (the old design): {old}. Redraw THESE pieces as the "
              f"{en} of image 2 (the approved concept): {new}. Keep every piece where it is in image 1{keep}.\n"
              "Do NOT draw: any other part of the creature, the old colours, extra pieces.")
    check = f"- đúng chỗ, cỡ như mảnh cũ{'' if kind == 'doi' else ', giữ viền'};\n- như concept: {vi};\n- không vẽ phần khác."
    return [code, vi, en, kind, px, old, f"{vi} cũ (1024 × 1024, nền trắng)", check, prompt, joint]


def main(only):
    out_path = os.path.join(HEROES, "forms_thuy_lo2.json")
    old = {f["code"]: f for f in json.load(open(out_path, encoding="utf-8"))} if os.path.exists(out_path) else {}
    sys.path.insert(0, os.path.join(AOLA, "tools"))
    import ghep_nhom as gn
    import portrait_png as pp
    for f in L:
        if only and f["code"] not in only:
            continue
        pid = f["aola"]
        rdir = os.path.join(AOLA, "reskin", f"thuy_{pid}")
        os.makedirs(rdir, exist_ok=True)
        regions = {"note": f"{f['code']} (lo_thuy2.py): vùng concept = nhóm mảnh", "exclude": f["keep"] + f["drop"],
                   "regions": [{"n": i, "name": g[3], "parts": g[1]} for i, g in enumerate(f["groups"], 1)]}
        groups = {"note": f"{f['code']} (lo_thuy2.py)", "clip": "1_1", "keep": f["keep"], "drop": f["drop"],
                  "groups": [{"code": g[0], "name": g[3], "anchor": g[1][0], "draw": g[1]} for g in f["groups"]]}
        ghep = {"code": f["code"], "elem": "thuy", "parts": f"pet{pid}_parts", **f["ghep"]}
        for name, data in (("regions.json", regions), ("groups.json", groups), ("ghep.json", ghep)):
            json.dump(data, open(os.path.join(rdir, name), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        subprocess.run([sys.executable, "-I", os.path.join(AOLA, "tools", "dung_rig.py"), rdir], check=True,
                       stdout=subprocess.DEVNULL)
        r = gn.Rig(os.path.join(AOLA, "reskin", f"pet{pid}_parts"), "1_1")
        bs = [r.box(p) for p in r.first if r.box(p) and not pp.is_shadow(r.char_img(str(p["c"])))]
        H = max(b[3] for b in bs) - min(b[1] for b in bs)
        meta = json.load(open(os.path.join(rdir, "refs", "orig", "orig_groups.json"), encoding="utf-8"))
        px = {k: max(6, round(0.0085 * H * v["k"])) for k, v in meta.items()}
        entry = {"code": f["code"], "elem": "thuy", "aola": pid, "hero": f["hero"], "form": f["form"], "forms": f["forms"],
                 "form_name": f["form_name"], "role_vi": f"tướng boss hệ Thủy ({f['role']}), rig aola #{pid}",
                 "design_vi": f["design_vi"], "rig_vi": f"con gốc #{pid} (xem Rig_Numbered.png)",
                 "regions_vi": ", ".join(f"{i} {g[4]}" for i, g in enumerate(f["groups"], 1)), "anchor": True,
                 "concept": concept_text(f), "groups": [group_tuple(g, px[g[0]]) for g in f["groups"]], "extra": [],
                 "first": [f["groups"][0][0], f["groups"][1][0]]}
        if f["prev"]:
            entry["prev"] = [[f["prev"], "the approved FIRST stage of this evolution line: keep its colours, face and drawing "
                                         "style; this stage is the same creature grown up",
                              "dạng 1 đã duyệt của dòng này"]]
        old[f["code"]] = entry
        print(f["code"], f"cao {H:.0f}", px)
    json.dump(list(old.values()), open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(set(sys.argv[1:]))
