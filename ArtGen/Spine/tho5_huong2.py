# -*- coding: utf-8 -*-
"""Năm tướng đầu đảo Thổ, LƯỢT 2 concept (2026-11-17). Người dùng trả cả lượt 1: "ảnh bạn gen ra bị giống con gốc quá, tự lên concept gần
giống thôi" (tướng 2 còn lỗi vì ảnh con gốc dựng sai mắt, đã sửa ở tho5.luoi_sua). Ảnh 1 chỉ còn là mẫu DÁNG và BỐ CỤC CHI; đầu, mặt, mảnh
lưng, sừng, diềm, mào là thiết kế mới của mình. Thân và chân giữ cỡ, bề dày gần như cũ (để lắp lên lưới của rig), phần còn lại tự do.
Dùng trong tho5.py (concept2)."""
from tho5_huong import CON


def task2(concept):
    return (f"TASK: DESIGN A NEW CHARACTER, LOOSELY BASED ON image 1: {concept}. Image 1 is ONLY a guide for the POSE and the BODY PLAN (the "
            "new character will be animated with the same skeleton): keep its pose, its facing, its size and place on the canvas, and "
            "roughly where the head, the body, each limb, the tail and the big pieces on the back are and which way they point. The body "
            "and the legs keep about the same size and thickness. EVERYTHING ELSE IS OUR OWN NEW DESIGN, described below: a different head "
            "and face, different shapes for the pieces on the back, the horns, frills and crests, new materials and colours. The result "
            "must NOT look like a recolour or a trace of image 1: someone who knows image 1 must see a DIFFERENT creature standing in the "
            "same pose. Every limb, the tail and the head stay joined to the body (no white gaps between a limb and the body).")


def goc2(en):
    return (en.split(" It is painted")[0] + ". It is painted in a smooth digital cel style. Use it ONLY for the pose and the body plan; do "
            "NOT copy its shapes, its face, the outlines of its pieces, its details or its colours.")


HUONG2 = {}

HUONG2["cong_da"] = dict(
    concept="a SMALL, BRAVE EARTH CRITTER that digs in the ground and carries a big load of rock on its back",
    plan=("BODY PLAN (from image 1): a small round four-legged critter in three-quarter front view, turned a little to the RIGHT, standing "
          "low on four very short stubby legs, a small tail at the lower left, its face on the right half of the body, and a big load on "
          "its back that is wider than the body and rises well above it (top middle of the picture)."),
    huong={
        "C": ("tatu con mai đá, hốc đá vỡ lộ cụm hổ phách",
              "tatu con: mõm nhọn ngắn mũi tròn sẫm, hai tai tròn nhỏ, mắt quả quyết; lông vàng đất, mặt và bụng kem; trên lưng MAI ĐÁ bốn tấm "
              "cong chồng nhau, trên đỉnh một hốc đá vỡ lộ cụm tinh thể hổ phách; vài viên sỏi bám mép mai; đuôi ngắn có khoanh",
              ["NEW CREATURE: a round ARMADILLO pup. HEAD AND FACE (right half of the body): a short pointed snout pointing to the right with "
               "a round dark-brown nose, two small rounded ears on top of the head, two determined eyes (white, dark-brown pupils, one small "
               "white dot each) under two short thick angry brows drawn as ink strokes, a small frowning mouth.",
               "BODY: sandy ochre #D2A066; the face round the snout and the belly cream #F0DDB4; four stubby legs with three tiny cream claws; "
               "a short tail with two darker rings #9A6B3C.",
               "BACK LOAD: a big rounded STONE SHELL made of FOUR overlapping curved plates (like an armadillo shell turned to rock), about as "
               "wide and tall as the load in image 1, flat grey-beige #BFB29B with darker #998D77 plate rims; on its top a broken-open GEODE "
               "hole with a cluster of four flat AMBER crystals #F2B33D standing up (flat colour, no glow); two small round pebbles stuck to "
               "the lower left edge of the shell and one on the right.",
               "NO crystal block, no hexagon shapes, no flat plates standing on the forehead."]),
        "D": ("chuột chũi vuốt đào, lưng xoè gai đá như nhím",
              "chũi tròn lông nâu sẫm, mũi hồng to, mắt nhỏ dưới mày rậm, hai răng cửa; hai chân trước là bàn đào to ba vuốt kem; trên lưng "
              "VƯƠNG MIỆN GAI ĐÁ bảy mũi xoè lên như nhím (kem, chóp son); vài hòn đá vụn ở chân gai",
              ["NEW CREATURE: a round MOLE. HEAD AND FACE (right half of the body): a big round pink-brown nose #D48A78 pointing to the right, "
               "two small fierce eyes (white, dark pupils, one small white dot) under thick bushy brows, a small mouth showing two square "
               "front teeth, no visible ears.",
               "BODY: short velvety fur, dark earth brown #7A5238; a lighter tan patch #C9A274 on the face round the nose and on the belly; "
               "the two FRONT feet are big flat DIGGING PAWS with three thick cream claws #EFE2C4 each; the back feet small; a short stubby "
               "tail.",
               "BACK LOAD: a fan of SEVEN short thick cone-shaped ROCK QUILLS rising up and back like a hedgehog's spines, filling about the "
               "same area as the load in image 1 (the middle ones the tallest), flat sandstone cream #E7D3A3 with ochre tips #C48A45; two "
               "small loose stones at their base on the left and one on the right.",
               "NO crystal block, no hexagon shapes, no flat plates standing on the forehead."]),
    },
)

HUONG2["than_lan_cat"] = dict(
    concept="a TOUGH DESERT EARTH LIZARD",
    plan=("BODY PLAN (from image 1): a squat lizard sitting low on its belly, three-quarter view turned to the RIGHT, its big head raised at "
          "the upper right, something big behind its head spreading to the upper left, the near front arm planted at the lower right, the "
          "near back leg folded at the lower left, the far limbs behind, a short thick tail curling up at the left."),
    huong={
        "C": ("thằn lằn sừng sa mạc, vương miện sừng đá, cổ áo ngắn",
              "đầu rõ mõm tù, miệng rộng hàm dưới nhô, hai mắt hổ phách đồng tử dọc; quanh gáy VƯƠNG MIỆN SÁU SỪNG ĐÁ ngắn dày (hai sừng đỉnh dài "
              "cong ra sau); sau đầu CỔ ÁO NGẮN ba phiến sa thạch tròn mép; da vàng cát, họng bụng kem, ba vằn nâu ở đuôi; vuốt nâu",
              ["NEW HEAD: a clear lizard head with a short blunt SNOUT pointing right, a wide mouth line with the lower jaw jutting out a "
               "little, TWO eyes: the near eye big under a heavy frowning brow (amber iris #F0A830, black slit pupil, one small white dot), "
               "the far eye just peeking at the right edge of the head.",
               "HORN CROWN: round the back of the head a crown of SIX short thick ROCK HORNS (the two at the top the longest, curving back), "
               "flat dark sandstone #8C6A48.",
               "COLLAR: behind the head a SHORT stiff collar of three rounded overlapping sandstone plates, smaller than the frill of image 1 "
               "(it reaches only the shoulder), cream #E9D2A0 each with one flat ochre band #C48A45.",
               "SKIN: sand yellow #D9B46A; throat and belly cream #EEDDB0; three flat brown #9A6B3C bands across the tail; blunt dark-brown "
               "claws #5E4330.",
               "NO membrane frill with spines, no pink."]),
        "D": ("thằn lằn giáp áo choàng phiến đất nung",
              "đầu nêm ngắn mày giáp đá nặng, hai mắt vàng, hai răng nanh nhỏ ở khoé hàm; lưng và chỗ diềm thành ÁO CHOÀNG PHIẾN ĐẤT NUNG chồng "
              "nhau dựng sau đầu như mũ trùm, mép trên răng cưa; da vàng xám đất, bụng kem; đuôi khoanh phiến đất nung",
              ["NEW HEAD: a short blunt wedge-shaped head with a heavy ROCK-PLATED BROW, TWO eyes (the near one fierce, yellow iris #F2C640, "
               "black slit pupil, one small white dot; the far one just peeking), a jaw with two small fangs at the corner.",
               "CAPE: the area of the frill and the top of the back covered by a big MANTLE of overlapping flat terracotta CLAY PLATES "
               "#B5603A with cream rims #EAD3A6, rising behind the head like a raised hood with a jagged top edge (about the size of the "
               "frill of image 1 but a different outline).",
               "SKIN: dusty khaki-ochre #B9A06A; throat and belly cream #EEDDB0; the tail ringed with three small terracotta plates; blunt "
               "dark-brown claws.",
               "NO membrane frill with spines, no pink."]),
    },
)

HUONG2["thu_da"] = dict(
    concept="a TOUGH, HEAVY EARTH BEAST, a brawler that charges and bites",
    plan=("BODY PLAN (from image 1): a stocky heavy four-legged beast standing square, three-quarter view turned to the RIGHT, a big head "
          "merged into the body without a neck at the upper right, a big lower jaw, a row of big pieces along the top of the head and the "
          "back pointing up and back, four short thick legs."),
    huong={
        "C": ("chó lửng đất răng nanh, sống lưng tảng sa thạch",
              "đầu rộng mõm ngắn, hàm dưới chìa hai NANH to vểnh lên và ba răng tù, mắt nhỏ dữ, vằn nâu sẫm như mặt nạ qua mắt; lông nâu son, hàm "
              "và ngực kem; dọc lưng NĂM TẢNG SA THẠCH tròn như giáp đá; chân mập ba vuốt kem to",
              ["NEW CREATURE: a heavy BADGER-BULLDOG of the earth. HEAD: a broad flat head with a short snout and a dark nose; a huge underbite "
               "JAW with TWO big tusks rising from the lower jaw and three blunt lower teeth between them; small fierce eyes under a heavy "
               "brow (yellow iris #F5C04A, dark pupil, one small white dot); a flat dark brown #5A3E2B stripe like a mask across the eyes; two "
               "small round ears.",
               "FUR: brown-ochre #A8784D; the jaw, the chest and the belly cream #EADCBD.",
               "BACK: instead of spikes, a row of FIVE big rounded SANDSTONE BOULDERS along the top of the head and the back (the biggest over "
               "the shoulders), like a ridge of stone armour, cream #E3CFA0 with one flat ochre band #BF8443 each.",
               "LEGS: thick short legs with three big pale claws #EFE2C4.",
               "NO flame shapes, no crystal spikes."]),
        "D": ("cóc tê giác đất nung, cụm pha lê hổ phách trên lưng",
              "cóc tê giác: một SỪNG ĐÁ dày trên mõm, miệng rộng năm răng tù, mắt nhỏ giận; da đất nung đỏ, hàm ngực kem; dọc lưng BA CỤM PHA LÊ "
              "HỔ PHÁCH (mỗi cụm hai, ba lăng trụ thẳng); chân mập vuốt kem",
              ["NEW CREATURE: a stocky TOAD-RHINO. HEAD: a wide toad-like head with ONE thick blunt STONE HORN on the snout, cream #EADCBD, "
               "pointing up and forward; a wide mouth with five blunt teeth along the jaw; small angry eyes under a heavy brow (amber iris "
               "#F5C04A, dark pupil, one small white dot).",
               "HIDE: warm terracotta #B8663E; the jaw, the chest and the belly cream #EADCBD; two or three flat darker #8A4A2C patches on the "
               "back.",
               "BACK: instead of the row of spikes, THREE CLUSTERS of AMBER CRYSTALS #F0AA32 along the back (each cluster two or three straight "
               "prisms with sharp points, one lighter flat facet #FFD27A), the biggest cluster over the shoulders.",
               "LEGS: thick short legs with short cream claws.",
               "NO flame shapes."]),
    },
)

HUONG2["rong_cat"] = dict(
    concept="a FIERCE DESERT DRAKE that hunts in the canyons and digs through sand",
    plan=("BODY PLAN (from image 1): a strong four-legged drake crouching low, three-quarter view turned to the RIGHT, ready to pounce: the "
          "head low at the right pointing down-right, a crest behind the head, big pieces on the shoulders and the back, the near front leg "
          "in the middle with long talons on the ground, the far front leg at the right with long talons on the ground, the back legs bent "
          "at the left, a long tail at the far left."),
    huong={
        "C": ("rồng đào cát, sừng xẻng trên mõm, lưng phiến sa thạch như núi bàn",
              "mõm có SỪNG XẺNG ĐÁ dẹt to chĩa tới (để đào), hai sừng ngắn cong sau mắt, sau đầu ba vây sa thạch tròn mép; lưng là CÁC PHIẾN SA "
              "THẠCH XẾP CHỒNG đầu phẳng như núi bàn; da vàng cát vằn nâu; mắt hổ phách; vuốt nâu sẫm to",
              ["NEW HEAD: a long head with a big flat SHOVEL-SHAPED STONE HORN on the snout pointing forward-down (for digging), cream #E6CF9C; "
               "two short curved horns behind the eyes, dark sandstone #8C6A48; a narrow angry eye (amber iris #F6C443, black slit pupil, one "
               "small white dot); a jaw with a few small teeth showing.",
               "CREST: behind the head THREE wide rounded sandstone FINS fanning back (instead of six blades), ochre #C4964F.",
               "BACK: instead of pointed shards, ridges of flat STACKED SANDSTONE SLABS with flat tops (like small mesas) on the shoulders and "
               "on the back, cream #E6CF9C with flat ochre bands #BF8443.",
               "HIDE: sand yellow #D6B271, darker ochre #B08A4E on the faces turned away, a few flat brown #7E5A36 stripes across the back and "
               "the tail; belly and throat cream #EBDDB5.",
               "TALONS: big curved dark brown #4E3726."]),
        "D": ("rồng giáp đá, giáp sa thạch vai và sống lưng, hai sừng dài vuốt ra sau, sừng mũi hổ phách",
              "đầu có HAI SỪNG ĐÁ DÀI vuốt ra sau thay mào gai, một sừng mũi pha lê hổ phách; GIÁP SA THẠCH dày trên vai, cẳng tay gần và dọc sống "
              "lưng; da nâu bụi, vằn son; mắt vàng; vuốt sẫm",
              ["NEW HEAD: a heavy head with a blunt snout carrying ONE thick AMBER CRYSTAL nose horn #F0A62E (flat, straight-edged), a narrow "
               "angry eye (yellow iris #F7C43A, black slit pupil, one small white dot), a strong jaw.",
               "CREST: instead of the fan of spines, TWO long thick backswept STONE HORNS from the back of the head, cream #E3CC98.",
               "ARMOUR: thick SANDSTONE ARMOUR PLATES (rounded slabs) on the shoulders, on the near forearm and along the spine down to the "
               "tail, cream #E3CC98 with one flat ochre band #BF8443 each (instead of the pointed shards).",
               "HIDE: dusty brown #8E6E52, darker #6E533D on the faces turned away, a few flat ochre #C4964F stripes on the tail; belly "
               "cream #E8D7B0.",
               "TALONS: big curved dark brown #3E2F24."]),
    },
)

HUONG2["quy_nui"] = dict(
    concept="a MIGHTY FOUR-ARMED EARTH TITAN (a living creature of rock and earth, not a robot)",
    plan=("BODY PLAN (from image 1): a huge hunched four-armed brute seen from the FRONT, leaning forward on two big front fists planted "
          "on the ground at the lower left and the lower right, two extra arms raised at the upper left and the upper right with open "
          "clawed hands, a small head at the top middle, a broad chest, something hanging at the waist between short legs."),
    huong={
        "C": ("vượn núi đá bốn tay, mặt khỉ đột, vương miện gai đá",
              "mặt vượn rộng: gờ mày nặng, hai mắt hổ phách nhỏ dữ, mũi bè, hai nanh ngắn vểnh; không sừng mà ba gai đá lởm chởm trên đỉnh đầu; "
              "thân tảng đá tròn hoa cương; ngực đá có mạch pha lê hổ phách chạy chéo; nắm đấm to có đốt; tay phụ ba ngón vuốt đá; khố da",
              ["NEW CREATURE: a four-armed MOUNTAIN APE made of rock. HEAD: a broad APE face with a heavy brow ledge, TWO small fierce amber "
               "eyes #F6C443 (dark pupils, one small white dot each), a wide flat nose, a jaw with two short tusks pointing up; no horns but a "
               "crown of THREE jagged rock spikes on top of the head.",
               "BODY: big ROUNDED BOULDERS for the shoulders, arms and fists (not square blocks), granite beige-brown #A88E6E on the faces "
               "turned to the viewer, #7C664E on the faces turned away; the joints and inner limbs dark earth #4E3B2C; the fists with big "
               "knuckles.",
               "CHEST: a rough stone chest with ONE vein of flat AMBER crystals #EFA330 running across it diagonally (no glow).",
               "BACK ARMS: a little thinner, each ending in a three-fingered stone claw, dark earth #4E3B2C.",
               "WAIST: a plain hide loincloth #7B5236.",
               "NO single eye, no diamond socket, no curved bull horns, no machine parts, no rings."]),
        "D": ("quỷ đất bốn tay sừng cừu xoắn, giáp sa thạch vai và nắm đấm",
              "đầu rộng hai SỪNG CỪU XOẮN dày cuộn tới trước, hai mắt vàng sâu, miệng rộng nhe nanh; thân là da đất nâu đỏ cơ bắp (không phải khối "
              "đá), giáp sa thạch kem trên vai và nắm đấm; một dây đeo chéo ngực; tay phụ quấn dây thừng; khố da sẫm",
              ["NEW CREATURE: a four-armed EARTH OGRE-DEMON. HEAD: wide, with TWO thick RAM HORNS curling forward round its sides, cream "
               "#E9DCC0; TWO deep-set yellow eyes #F6C443 (dark pupils, one small white dot each) under a heavy brow; a wide mouth showing a "
               "row of teeth and two lower fangs.",
               "BODY: muscular EARTH SKIN (not rock blocks), dark terracotta-brown #7A4A33 on the faces turned to the viewer, #5A3424 on the "
               "faces turned away; SANDSTONE ARMOUR pieces (rounded cream slabs #E3CC98 with one ochre band #BF8443) on the shoulders and "
               "over the two big fists.",
               "CHEST: one plain leather strap #4E3424 across the chest.",
               "BACK ARMS: the forearms wrapped with a few turns of rope #C9A86A, hands with four thick fingers and short cream claws.",
               "WAIST: a dark hide loincloth #4E3424.",
               "NO single eye, no diamond socket, no bull head, no machine parts, no rings."]),
    },
)

for _k, _v in HUONG2.items():
    _v["mood"] = CON[_k]["mood"]
    _v["refs"] = CON[_k]["refs"]
