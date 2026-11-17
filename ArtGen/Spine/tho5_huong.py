# -*- coding: utf-8 -*-
"""Năm tướng đầu đảo Thổ: mô tả con gốc từng mảnh và hai hướng concept lượt 1 mỗi con (Claude đề xuất 2026-11-17, chờ người dùng chọn).
Dùng trong tho5.py (concept). Tông chung của đảo: đất, sa thạch, đất son, đất nung, pha lê hổ phách (vàng là màu của Thổ); tránh dung nham
phát sáng (đảo Hỏa), kim loại (đảo Kim), rêu (đảo Mộc). Con sau trông chiến hơn con trước."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_I = os.path.join(HERE, "inbox")
GOLEM = os.path.join(_I, "golem_lua_1", "tai_ve", "L1_duyet.png")
RUA = os.path.join(_I, "rua_lua_1", "tai_ve", "L1_duyet.png")
TINH = os.path.join(_I, "tinh_sat_1", "tai_ve", "L1_duyet.png")
HUOU = os.path.join(_I, "huou_go_2", "tai_ve", "L1_duyet.png")
DAT = os.path.join(_I, "dat_nung_1", "tai_ve", "L1_duyet.png")

# ảnh mẫu phong cách: (đường dẫn, câu tiếng Anh, câu Việt)
REF = {
    "golem": (GOLEM,
              "an approved hero of our game (a stone golem with fires), 1536x1024, white background: match EXACTLY how STONE is drawn in our "
              "style: the wobbly dark-brown pen line, the visible crayon hatching, completely flat stone colours (a front-face tone and a "
              "darker side-face tone, nothing else). Do NOT copy its design, its fire or its colours.",
              "Golem lửa (tướng đảo Hỏa) đã duyệt: lấy cách vẽ ĐÁ theo nét game (bút mực rung, vân sáp, đá tô phẳng hai tông mặt trước / mặt bên)"),
    "rua": (RUA,
            "an approved hero of our game (a rock tortoise beast), 1536x1024, white background: match EXACTLY its wobbly dark-brown pen line, "
            "its crayon hatching and its flat colouring of a heavy rock beast (rock blocks, horns, eye). Do NOT copy its design, its fire or "
            "its colours.",
            "Rùa golem lửa (tướng đảo Hỏa) đã duyệt: lấy nét bút, vân sáp, cách tô phẳng một con thú đá nặng"),
    "tinh": (TINH,
             "an approved small starter hero of our game (a little crystal spirit), 1536x1024, white background: match EXACTLY its wobbly "
             "dark-brown pen line, its crayon hatching, its flat colours and how a small determined face is drawn (eyes with one small white "
             "dot, a short frowning mouth). Do NOT copy its design or its colours.",
             "Thiết Tinh (tướng 1 đảo Kim) đã duyệt: lấy nét bút, vân sáp, cách vẽ một gương mặt nhỏ quả quyết"),
    "huou": (HUOU,
             "an approved hero of our game (a giraffe-like wood beast), 1536x1024, white background: match EXACTLY its wobbly dark-brown pen "
             "line, its crayon hatching and how an animal hide with a few flat patches or bands is coloured (flat, no shading). Do NOT copy "
             "its design or its colours.",
             "Hươu gỗ (tướng đảo Mộc) đã duyệt: lấy nét bút, vân sáp, cách tô da thú có vài mảng / vằn phẳng"),
    "dat": (DAT,
            "an approved hero of our game (a terracotta warrior golem), 1536x1024, white background: match EXACTLY its wobbly dark-brown pen "
            "line, its crayon hatching and its flat colouring of a big blocky earth body. Do NOT copy its design, its sword, its lava or its "
            "colours.",
            "Chiến binh đất nung (tướng đảo Hỏa) đã duyệt: lấy nét bút, vân sáp, cách tô phẳng thân khối to bằng đất"),
}

STYLE_ANH1 = ("Image 1 is painted in a smooth digital cel style with soft light and dark planes and gradients: do NOT copy that painting "
              "style or its colours")


def task(concept, pose):
    return (f"TASK: REDESIGN ON THE SAME POSE. Redraw the creature of image 1 as ONE picture of OUR OWN character, {concept}. The SAME "
            f"pose ({pose}), with EVERY piece in the same place, at the same size and with the same overlaps (if the new picture were "
            "laid over image 1, every piece must sit on its old place), but with the NEW shapes, new materials, new colours and our "
            "hand-drawn drawing style described below. Do not add pieces, do not remove, merge or move pieces. Every limb, the tail and "
            "the head stay joined to the body (no white gaps between a limb and the body).")


CON = {}

# ---------------------------------------------------------------- 1. cong_da (monster_3378), ải 1
CON["cong_da"] = dict(
    ten="thú nhỏ cõng đá", ai=1, refs=["tinh", "golem"],
    goc_vi=("Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): thú nhỏ tròn tím, bốn chân ngắn, đuôi nhọn nhỏ bên trái; hai mắt to mày "
            "cau, miệng răng cưa; hai tấm sẫm dựng trên trán làm mày; trên lưng khối pha lê sáu cạnh to hơn cả thân, quanh chân khối mấy viên "
            "pha lê lập phương. Giữ dáng và từng mảnh, đổi hình"),
    goc_en=("the REFERENCE creature, 1536x1024, white background: a small round purple critter with four stubby legs and a small pointed "
            "tail at the left, two big frowning eyes and a zigzag mouth, two flat dark plates standing on its forehead like stiff brows, "
            "and a huge six-sided crystal block on its back with a few crystal cubes round it. It is painted in a smooth digital cel style. "
            "Keep its POSE, its PIECES and their PLACES; change its LOOK and the shapes listed."),
    task=task("a SMALL, BRAVE EARTH CRITTER that digs in the ground and carries a big rock on its back",
              "seen from the front, turned a little to the right, standing low on four stubby legs, the big rock on its back"),
    mo_ta=("PIECE BY PIECE (as in image 1: a SMALL ROUND critter seen from the front, turned a little to the RIGHT, carrying a huge rock on "
           "its back): BODY: a small, round, soft body like a bun, low on the ground, in the lower middle; four very short stubby legs "
           "under it (two near legs in front, two far legs partly hidden behind); one small pointed tail sticking out at the lower left. "
           "FACE (on the right half of the body): two big oval EYES side by side (the left eye bigger, the right eye smaller and partly "
           "turned away), with small dark pupils looking to the right; a small zigzag frowning MOUTH under and between them. BROWS: two "
           "stiff flat dark PLATES rise from the top of the eyes up past the top of the head, the left one leaning to the upper left, the "
           "right one upright; their lower ends sit ON the top of the eyes and make the angry frown. ON THE BACK: one huge six-sided "
           "CRYSTAL BLOCK, as wide as the whole creature and taller than the body, sits on the back behind the head (top middle of the "
           "picture); round its lower edge smaller crystal CUBES: two on the left side, one big and one small on the right side."),
    mood=("Mood: a small, plucky, grumpy earth critter (a starter game hero): cute and round but brave, frowning, ready to headbutt; not a "
          "happy mascot, not scary."),
    huong={
        "A": ("chũi lông nâu đất cõng tảng đá hoa cương có khe hổ phách",
              "lông ngắn nâu đất, mõm kem; khối pha lê thành TẢNG ĐÁ TRÒN hoa cương be xám có khe nứt lộ ba tinh thể hổ phách; các khối lập "
              "phương thành sỏi tròn; hai tấm mày thành hai SỪNG MÀY đá nâu ngắn mập",
              ["BODY: short soft FUR, flat warm earth brown #B07A4A; a flat lighter cream-tan patch #E3C79A round the mouth and on the lower "
               "face; the legs a little darker brown #8A5A35 with three tiny pale claws #E9DCC3 on each foot; the tail the body colour "
               "with a dark brown tip.",
               "EYES: white with round dark-brown pupils #3A2618 and one small white dot each; same places, sizes and directions.",
               "BROWS: NEW SHAPE: the two flat plates become two short thick wedge-shaped BROW HORNS of dark brown stone #6E5440 with blunt "
               "rounded tips (about two thirds of the old length), on the same bases on top of the eyes, with the same tilts, still making "
               "the angry frown.",
               "BACK ROCK: NEW SHAPE: the six-sided crystal block becomes ONE big ROUND BOULDER of sandy granite: an irregular rounded rock "
               "with a flatter bottom, flat beige-grey #C9BBA2 on the faces turned to the viewer and #A3937A on the faces turned away; one "
               "jagged CRACK across its front through which three small flat AMBER crystals #F2B33D peek out (flat colour, no glow); same "
               "place, about the same width and height.",
               "SMALL CUBES: NEW SHAPE: they become rounded PEBBLES of the same granite, of different sizes, in the same places.",
               "MOUTH: the same small zigzag frown in dark-brown ink."]),
        "B": ("thú đất nung đỏ cõng tháp đá sa thạch xếp lớp",
              "da đất nung đỏ, mặt dưới màu cát; khối pha lê thành THÁP BA PHIẾN SA THẠCH xếp chồng (kem, một vạch son); các khối lập phương "
              "thành mảnh sa thạch dẹt; hai tấm mày thành hai GAI tai nhọn sa thạch sẫm",
              ["BODY: smooth skin like fired CLAY, flat terracotta #C0683F; a flat lighter sand patch #E8C089 on the lower face round the "
               "mouth; the legs darker terracotta #9A4E2E with tiny cream claws; the tail with a sand-coloured tip.",
               "EYES: white with round dark-brown pupils #3A2618 and one small white dot each; same places, sizes and directions.",
               "BROWS: NEW SHAPE: two short pointed ear-like SPIKES of dark sandstone #7A5236 (narrow triangles leaning outward), on the same "
               "bases on top of the eyes, still making the angry frown.",
               "BACK ROCK: NEW SHAPE: the six-sided crystal block becomes a stack of THREE flat rounded SANDSTONE SLABS piled on top of each "
               "other like a small rock tower (the biggest at the bottom, the smallest at the top, each a little tilted); each slab cream "
               "#EBD7A8 with ONE flat ochre band #C9954E across its side; the whole stack in the same place with about the same width and "
               "height as the old block.",
               "SMALL CUBES: NEW SHAPE: they become small flat sandstone CHIPS, cream with one ochre band, tilted, in the same places.",
               "MOUTH: the same small zigzag frown in dark-brown ink."]),
    },
    kiem=("đúng dáng (thân tròn thấp, bốn chân ngắn, đuôi nhọn bên trái, mặt bên phải nhìn phải); hai mắt cau có chấm trắng; hai mảnh mày ngồi "
          "trên mắt; khối đá trên lưng đúng chỗ, to cỡ con gốc; các viên nhỏ quanh chân khối; không còn pha lê tím"),
)

# ---------------------------------------------------------------- 2. than_lan_cat (monster_3257), ải 5
CON["than_lan_cat"] = dict(
    ten="thằn lằn sa mạc", ai=5, refs=["huou", "golem"],
    goc_vi=("Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): thằn lằn ngồi rạp quay phải, đầu nêm to, hai mắt to tròng đỏ mí nặng (mắt "
            "xa lấp ló ở mép phải đầu), gai móc dưới cằm; sau đầu diềm ba tấm nhọn hồng nhạt xoè sang trái; chân trước, chân sau gập, ngón tù "
            "sẫm; đuôi ngắn cong bên trái. Giữ dáng và từng mảnh, đổi hình"),
    goc_en=("the REFERENCE creature, 1536x1024, white background: a squat beige lizard sitting low, turned to the right, with a broad "
            "wedge-shaped head, two big heavy-lidded red eyes (the far one peeking at the right edge of the head), a curved barb under the "
            "chin, a fan of three pointed pinkish "
            "frill plates behind the head, folded legs with blunt dark toes and a short curled tail at the left. It is painted in a smooth "
            "digital cel style. Keep its POSE, its PIECES and their PLACES; change its LOOK and the shapes listed."),
    task=task("a TOUGH DESERT EARTH LIZARD with a collar of rock",
              "seen from the side in three-quarter view, turned to the right, sitting low on its belly, its big head raised at the upper right"),
    mo_ta=("PIECE BY PIECE (as in image 1: a squat LIZARD sitting low on its belly, seen from the side in three-quarter view, turned to the "
           "RIGHT, its big head raised at the upper right): HEAD (upper right): a broad flat wedge-shaped lizard head, its snout pointing "
           "right, with a heavy BROW RIDGE over one long narrow half-lidded EYE in the middle of the head; a wide closed mouth line under "
           "the eye; at the front-right under the chin one pointed curved BARB hanging down; a small pointed bump at the top-right of the "
           "head. FRILL: behind the head a big FAN of three overlapping stiff pointed plates spreading to the upper left and the left (the "
           "top one the narrowest, the bottom one the widest, reaching down past the shoulder), each with two or three small spines on its "
           "edge. BODY: a round sitting body under the frill, a short thick neck. LIMBS: the near FRONT ARM (right of the middle) bent, "
           "its hand with four blunt dark toes on the ground at the lower right; the far front arm behind it; the near BACK LEG (lower "
           "left of the middle) folded, its foot with blunt dark toes on the ground; the far back leg behind. TAIL: a short thick tail "
           "curling up at the left behind the body."),
    mood=("Mood: a stubborn, sulky-tough desert lizard (a game hero) guarding its rock: the eye narrowed and fierce, ready to fight; "
          "chunky and appealing but not a happy mascot, not scary."),
    huong={
        "A": ("thằn lằn cát vàng, diềm ba phiến sa thạch",
              "da vàng cát, vài vằn nâu ở đuôi và gáy, bụng kem; diềm thành BA PHIẾN SA THẠCH dày mép vỡ thẳng (kem, một vạch son); gai đầu, "
              "gai cằm thành gai đá tù; mắt hổ phách đồng tử dọc",
              ["SKIN: flat sand yellow #D9B46A on the head, body, limbs and tail; a few flat darker brown #9A6B3C BANDS across the tail and "
               "two on the back of the head (no spots, no dots); the throat and belly cream #EEDDB0; the toes dark brown #5E4330.",
               "FRILL: NEW SHAPE: the three membrane plates become THREE overlapping flat SANDSTONE SLABS (thick plates of layered rock with "
               "straight broken edges and blunt corners, no thin spines), in the same places, at the same sizes and directions; each slab "
               "cream #E9D2A0 with ONE flat ochre band #C48A45 along its length.",
               "BUMP AND BARB: the small bump on the head and the chin barb become short blunt ROCK SPIKES, dark sandstone #8C6A48.",
               "EYE: a narrow fierce eye under the heavy frowning brow: flat AMBER iris #F0A830 with a black vertical slit pupil and one "
               "small white dot.",
               "MOUTH: a firm closed mouth line with the corner turned down."]),
        "B": ("thằn lằn đỏ đất nung, vương miện gai thạch nhũ",
              "da đỏ đất nung, họng bụng màu cát, vài vằn nâu sẫm ở đuôi; diềm thành VƯƠNG MIỆN NĂM GAI ĐÁ dựng như thạch nhũ (đá be xám); "
              "gai đầu thành chóp đá, gai cằm thành móc đá; mắt vàng đồng tử dọc",
              ["SKIN: flat terracotta red-brown #B5603A on the head, back, limbs and tail; the throat, belly and the underside of the tail "
               "cream sand #E8CC98; a few flat dark brown #6E3A22 bands across the tail; the toes dark brown #5E4330.",
               "FRILL: NEW SHAPE: the fan of three plates becomes a CROWN of FIVE upright pointed ROCK SPIKES like stalagmites (cones with "
               "blunt tips, standing up and leaning back, the middle ones the tallest), filling the same area behind the head; flat "
               "grey-beige stone #C2B49B with a darker tone #9C8D74 on the side turned away.",
               "BUMP AND BARB: the small bump on the head becomes a short stone cone; the chin barb a short curved stone hook; same stone "
               "colours.",
               "EYE: a narrow fierce eye under the heavy frowning brow: flat yellow iris #F2C640 with a black vertical slit pupil and one "
               "small white dot.",
               "MOUTH: a firm closed mouth line with the corner turned down."]),
    },
    kiem=("đúng dáng (ngồi rạp quay phải, đầu to phía trên bên phải, diềm sau đầu xoè sang trái, đuôi cong bên trái); mắt hẹp dữ có chấm trắng; "
          "chân, đuôi dính thân; diềm đã đổi dáng hẳn (không còn màng hồng có gai)"),
)

# ---------------------------------------------------------------- 3. thu_da (monster_3525), ải 10
CON["thu_da"] = dict(
    ten="thú đá hàm lớn", ai=10, refs=["rua", "golem"],
    goc_vi=("Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): thú đá xám bốn chân mập quay phải, đầu tròn liền thân, hàm dưới trắng to "
            "mép răng cưa ôm xuống ngực, mắt đỏ nhỏ có quầng cam; dãy gai pha lê dáng lửa cam trên đầu và lưng; chân phiến đá, ngón tù. Giữ "
            "dáng và từng mảnh, đổi hình"),
    goc_en=("the REFERENCE beast, 1536x1024, white background: a stocky grey rock beast on four thick legs, turned to the right, a big round "
            "head merged into the body, a huge white lower jaw with a jagged edge curving down under the chest, a small red eye with an "
            "orange patch, a row of orange flame-shaped crystal spikes on the head and back. It is painted in a smooth digital cel style. "
            "Keep its POSE, its PIECES and their PLACES; change its LOOK and the shapes listed."),
    task=task("a TOUGH, HEAVY EARTH BEAST of sandstone, a brawler that charges and bites",
              "three-quarter view turned to the right, standing square on four short thick legs"),
    mo_ta=("PIECE BY PIECE (as in image 1: a stocky, heavy FOUR-LEGGED rock beast like a bulldog crossed with a toad, three-quarter view "
           "turned to the RIGHT, standing square on four short thick legs): HEAD (upper right, merged into the body without a neck): a big "
           "rounded head; at its front a huge pale LOWER JAW that curves from under the eye down under the chest like a big shovel, its "
           "upper edge jagged like a row of big blunt teeth; one small slanted EYE under a heavy brow, with a coloured patch round it; on "
           "top of the head blunt rounded rock LUMPS. SPIKES: a row of big angular flame-shaped spikes rising up and back: one big spike at "
           "the top behind the head pointing up-left, one small spike at the top of the head, a cluster of three on the upper left of the "
           "back (one big, two smaller), one more at the left, one small at the hip (lower left). BODY: made of big rock slabs; a pale chest "
           "plate continues under the jaw. LEGS: four thick legs of rock slabs: the near front leg (right, in front of the jaw) with a wide "
           "foot and three blunt toes; the far front leg (right, behind); the near back leg (lower middle) with three blunt toes; the far "
           "back leg (far left, behind) ending in a pointed foot."),
    mood=("Mood: a tough, hot-headed brawler beast (a game hero): heavy and solid, head low, the eye narrowed and angry, ready to charge and "
          "bite; chunky and appealing but not a cute mascot, not horror."),
    huong={
        "A": ("thú sa thạch nâu, gai pha lê hổ phách, hàm kem",
              "thân sa thạch nâu ấm hai tông; gai dáng lửa thành MŨI PHA LÊ HỔ PHÁCH thẳng cạnh; hàm và ngực màu kem xương, mép hàm năm răng "
              "tù to; u đầu thành hai SỪNG ĐÁ kem ngắn chĩa ra sau; mắt vàng hổ phách, vành mày nâu sẫm",
              ["BODY AND HEAD: flat warm brown sandstone #9E7653 on the faces turned to the viewer, darker brown #7A5A3F on the faces "
               "turned away; two or three flat darker brown patches, no cracks.",
               "SPIKES: NEW SHAPE: every flame-shaped spike becomes a straight-edged AMBER CRYSTAL SHARD (a long flat prism with a sharp "
               "point and straight sides, like a quartz point), in the same places, at the same sizes and directions; flat amber #F0AA32 "
               "with one lighter flat facet #FFD27A on its front half; NOT flame-shaped, no wavy edges, no veins, no glow.",
               "JAW AND CHEST PLATE: flat cream bone-sandstone #EADCBD; the jagged upper edge of the jaw drawn as FIVE big blunt TEETH.",
               "EYE: small and fierce, flat amber-yellow iris #F5C04A, a dark pupil, one small white dot; the coloured patch round the eye "
               "becomes a flat dark brown #5E4430 brow band.",
               "HEAD LUMPS: NEW SHAPE: the rounded lumps on top of the head become two short thick blunt STONE HORNS pointing back, cream "
               "#EADCBD.",
               "TOES: short blunt cream toes #EADCBD."]),
        "B": ("thú đất son vàng, sống lưng phiến đá xám",
              "thân đất son vàng hai tông, vài vằn nâu sẫm ngang chân như lớp đất; gai thành PHIẾN ĐÁ PHIẾN XÁM đầu tròn dựng nghiêng ra sau "
              "(như phiến lưng khủng long); hàm và ngực kem, mép hàm năm răng tù; u đầu thành hai núm đá xám; mắt vàng",
              ["BODY AND HEAD: flat ochre earth #C39556 on the faces turned to the viewer, #9C7340 on the faces turned away; two or three "
               "flat dark brown #6A4A2E stripes across each leg (like layers of earth), no cracks.",
               "SPIKES: NEW SHAPE: every spike becomes a thick flat SLATE PLATE (a tall slab of grey stone with a rounded top, like the back "
               "plates of a stegosaurus, a little tilted back), in the same places and directions, at about the same sizes; flat slate grey "
               "#7E8088 with a darker edge band #5E6068.",
               "JAW AND CHEST PLATE: flat cream #EEE0C2; the jagged upper edge of the jaw drawn as FIVE big blunt TEETH.",
               "EYE: small and fierce, flat yellow iris #F6CD4C, a dark pupil, one small white dot; a flat dark brown brow band round the "
               "eye.",
               "HEAD LUMPS: they become two rounded slate-grey rock knobs.",
               "TOES: short blunt slate-grey toes."]),
    },
    kiem=("đúng dáng (bốn chân đứng đất, quay phải, đầu liền thân, hàm to ôm xuống ngực); gai đổi dáng hẳn (không còn dáng lửa cam); mắt dữ có "
          "chấm trắng; bốn chân dính thân, chân xa không rời"),
)

# ---------------------------------------------------------------- 4. rong_cat (monster_3424), ải 15
CON["rong_cat"] = dict(
    ten="rồng cát", ai=15, refs=["rua", "huou"],
    goc_vi=("Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): rồng bốn chân màu be cúi rạp quay phải sắp vồ, đầu nêm thấp bên phải, mắt "
            "hẹp dữ, ba sừng đỏ trên mõm, mào sáu gai lưỡi kiếm sau đầu; trên vai và lưng các mảnh đá sẫm nhọn; tay trước có ba vuốt dài cong "
            "sẫm; đuôi dài bên trái. Giữ dáng và từng mảnh, đổi hình"),
    goc_en=("the REFERENCE drake, 1536x1024, white background: a beige four-legged drake crouching low to pounce, turned to the right, a "
            "wedge-shaped head low at the right, a narrow angry eye, three red horns on the snout, a crest of six blade-like spines behind "
            "the head, dark angular rock shards on the shoulders and back, front legs with three long curved dark talons, a long tail at "
            "the left. It is painted in a smooth digital cel style. Keep its POSE, its PIECES and their PLACES; change its LOOK and the "
            "shapes listed."),
    task=task("a FIERCE DUNE DRAKE of the desert canyons, a predator with rock spines",
              "three-quarter view turned to the right, crouching low on four legs, the head low at the right, about to pounce"),
    mo_ta=("PIECE BY PIECE (as in image 1: a strong four-legged DRAKE crouching low, three-quarter view turned to the RIGHT, its head low at "
           "the right, about to pounce): HEAD (right, low): a long wedge-shaped reptile head pointing to the lower right; a separate heavy "
           "LOWER JAW under it; one narrow angry EYE under a heavy brow; three HORNS on top of the snout and brow pointing up and forward "
           "(the front one big and curved forward, two small ones behind it); behind the head a CREST of six long pointed blade-like spines "
           "fanning up and back (to the upper left). BODY: a hunched muscular body; on the shoulders and back big angular ROCK SHARDS "
           "sticking up and back to the upper left (a group of three over the shoulders at the top middle, three more on the back left of "
           "the middle); small dark scale plates along the top of the tail. NEAR FRONT LEG (middle left, in front of the body): an upper "
           "arm and a huge armoured FOREARM whose upper end rises behind the shoulder, and whose lower end has three long curved dark "
           "TALONS on the ground (middle bottom). FAR FRONT LEG (right, behind the head): three long curved dark talons on the ground at "
           "the far right. BACK LEGS: the near back leg (left of the middle) bent with a clawed foot on the ground; the far back leg "
           "(middle, behind) bent. TAIL: a long tapering tail at the far left."),
    mood=("Mood: a fierce predator drake (a game hero) crouched to pounce: head low, the eye narrowed, talons ready; powerful and "
          "dangerous-looking but appealing, not horror: no blood, no skulls."),
    huong={
        "A": ("rồng cồn cát vàng, cột sa thạch trên lưng, sừng hổ phách",
              "da vàng cát hai tông, vài vằn nâu ở lưng, đuôi, cẳng tay, bụng kem; mảnh đá nhọn thành CỘT SA THẠCH đầu vỡ phẳng (kem, vạch son); "
              "mào sáu gai thành BỐN VÂY ĐÁ rộng đầu khía; ba sừng đỏ thành sừng PHA LÊ HỔ PHÁCH; mắt vàng đồng tử dọc; vuốt nâu sẫm",
              ["HIDE: flat sand yellow #D6B271 on the faces turned to the viewer, darker ochre #B08A4E on the faces turned away; a few flat "
               "brown #7E5A36 stripes across the back, the tail and the forearms (no spots, no scale texture); the belly and throat cream "
               "#EBDDB5.",
               "BACK ROCKS: NEW SHAPE: the angular dark shards become blocky SANDSTONE PILLARS (rectangular columns with flat broken tops, a "
               "little tilted back), in the same places and directions, at about the same sizes; each pillar cream #E6CF9C with one or two "
               "flat ochre bands #BF8443 across it (layers of rock).",
               "HEAD CREST: NEW SHAPE: the six blade spines become FOUR wide flat stone FINS with notched tips, fanning back in the same "
               "area, flat ochre #C4964F.",
               "HORNS: the red horns become flat straight-edged AMBER CRYSTAL horns #F0A62E, in the same places, the front one the biggest.",
               "EYE: narrow and angry under a heavy brow: flat amber-yellow iris #F6C443 with a black vertical slit pupil and one small "
               "white dot.",
               "TALONS AND TOES: dark brown #4E3726, same shapes and sizes; the tail scale plates dark ochre #A07A44."]),
        "B": ("rồng đá đỏ hẻm núi, cột bazan, sừng ngà",
              "da đỏ nâu hẻm núi hai tông, họng bụng mặt trong cẳng tay màu cát, vài vằn sẫm ở đuôi lưng; mảnh đá nhọn thành CỤM CỘT BAZAN sáu "
              "cạnh xám sẫm; mào thành BA LƯỠI ĐÁ cong vuốt ra sau; ba sừng thành sừng NGÀ cong; mắt vàng cam; vuốt bazan sẫm",
              ["HIDE: flat canyon red-brown #A85B3B on the faces turned to the viewer, darker #82432A on the faces turned away; cream sand "
               "#E9CFA2 on the throat, the belly and the inner forearms; a few flat dark #5C2E1C bands across the tail and the back.",
               "BACK ROCKS: NEW SHAPE: the angular shards become clusters of six-sided BASALT COLUMNS (tall columns with flat tops, tilted "
               "back), in the same places and directions, at about the same sizes; flat dark grey #5A5856 on the faces turned to the viewer, "
               "#403E3C on the faces turned away.",
               "HEAD CREST: NEW SHAPE: the six spines become THREE tall curved stone BLADES sweeping back in the same area, dark basalt grey "
               "#5A5856.",
               "HORNS: smooth curved IVORY horns #EFE3C6, in the same places, the front one the biggest.",
               "EYE: narrow and angry under a heavy brow: flat yellow-orange iris #F7B13A with a black vertical slit pupil and one small "
               "white dot.",
               "TALONS AND TOES: dark basalt grey #3E3B39, same shapes and sizes; the tail scale plates dark grey."]),
    },
    kiem=("đúng dáng (cúi rạp quay phải, đầu thấp bên phải, ba vuốt dài chạm đất ở giữa và bên phải, đuôi dài bên trái); đá trên lưng, mào, "
          "sừng đã đổi dáng; mắt dữ có chấm trắng; bốn chân dính thân"),
)

# ---------------------------------------------------------------- 5. quy_nui (monster_3612), ải 20
CON["quy_nui"] = dict(
    ten="titan núi bốn tay", ai=20, refs=["golem", "dat"],
    goc_vi=("Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): golem bốn tay nhìn thẳng, gù, chống hai nắm đấm khối to xuống đất như khỉ "
            "đột; đầu tấm hẹp một mắt đỏ trong hốc hình thoi, hai sừng cong sẫm; giáp ngực đỏ; hai tay phụ máy mọc sau vai xoè bàn tay vuốt; "
            "khố đỏ có bốn dải sẫm. Giữ dáng và từng mảnh, đổi hình"),
    goc_en=("the REFERENCE brute, 1536x1024, white background: a hunched four-armed golem seen from the front, leaning on two huge blocky "
            "fists like a gorilla, a narrow plate-like head with ONE red eye in a diamond socket and two curved dark horns, a red chest "
            "plate, two extra arms rising from behind the shoulders with open clawed hands, a red cloth with four dark straps at the waist. "
            "It is painted in a smooth digital cel style. Keep its POSE, its PIECES and their PLACES; change its LOOK and the shapes listed."),
    task=task("a MIGHTY MOUNTAIN TITAN, a four-armed earth brute made of rock (a living creature of stone, not a robot)",
              "seen from the front, hunched forward and leaning on its two big front fists, the two back arms raised with open hands"),
    mo_ta=("PIECE BY PIECE (as in image 1: a huge hunched FOUR-ARMED brute seen from the FRONT, leaning forward on its two big front arms "
           "like a gorilla): HEAD (top middle, small for the body): a narrow tall plate-like head with a vertical ridge down its middle and "
           "ONE round EYE in a diamond-shaped socket; two big curved dark HORNS rise from behind the sides of the head, curving out and up. "
           "CHEST: a big rounded chest plate behind and under the head, and a paler lower chest plate. SHOULDERS: two huge blocky shoulder "
           "pieces at the left and the right. FRONT ARMS: from the shoulders two massive arms come down to two HUGE blocky FISTS planted on "
           "the ground at the lower left and the lower right, each with two dark claws on its front. BACK ARMS: two extra arms rise from "
           "behind the shoulders: each a big blocky upper arm reaching out sideways (upper left and upper right) and ending in a dark "
           "CLAWED HAND with four fingers open. WAIST: a cloth apron hanging between the legs with four short dark straps in front of it. "
           "LEGS: two short legs behind the apron with small feet."),
    mood=("Mood: the strongest, most intimidating earth titan of the island (a boss-like game hero): heavy, hunched, ready to smash; "
          "powerful and frightening in size but still a game character drawn in our style: no skulls, no blood, no horror, no robot parts."),
    huong={
        "A": ("titan đá hoa cương, lõi ngực pha lê hổ phách, sừng đá kem",
              "mọi khối thành đá hoa cương nâu be hai tông, khớp nâu đất sẫm, bỏ hoa văn khắc; giáp ngực đỏ thành LÕI PHA LÊ HỔ PHÁCH nạm trong "
              "đá; đầu thành ĐẦU ĐÁ NHƯ ĐỈNH NÚI có gờ mày, một mắt hổ phách; sừng thành sừng đá kem cong như sừng bò; khố thành tấm da nâu, "
              "bốn dải thành dây treo hòn đá tròn",
              ["BODY: all the blocky pieces (shoulders, arms, fists, the back arms) become solid ROCK blocks of warm granite: flat beige-brown "
               "#A88E6E on the faces turned to the viewer, darker #7C664E on the faces turned away; the dark joints and inner limbs between "
               "the blocks dark brown earth #4E3B2C (flat); no cracks, no carved signs, no rings, no machine parts.",
               "CHEST: NEW: the chest plate becomes a big AMBER CRYSTAL CORE #EFA330 (flat, made of three or four big flat crystal faces "
               "with straight edges, one lighter face #FFD27A) set into the chest and framed by rock; the paler lower plate becomes plain "
               "cream sandstone #E5D3AE. No glow.",
               "HEAD: NEW SHAPE: a craggy rock head like a small mountain peak (a blunt pointed top, a heavy brow ledge), still narrow and in "
               "the same place, with ONE round amber eye #F6C443 (dark pupil, one small white dot) under the brow ledge; no diamond socket, "
               "no ridge line.",
               "HORNS: NEW SHAPE: two thick curved STONE horns, cream #E9DCC0, in the same places, curving out and up like a bull's.",
               "CLAWS AND FINGERS: dark brown stone #3E2F24; the fingers of the back hands thick and blunt.",
               "APRON AND STRAPS: the cloth becomes a hanging piece of thick brown hide #7B5236; the four straps become four short dark "
               "ropes, each with a small round stone #A88E6E at its end."]),
        "B": ("quỷ núi đất nâu sẫm, vằn vàng son, đầu bò đá, sừng ngà",
              "mọi khối thành đá đất nâu sẫm hai tông, mỗi khối to một vằn vàng son như vằn chiến; giáp ngực thành phiến sa thạch vàng son; "
              "đầu thành MŨ ĐÁ HÌNH ĐẦU BÒ mày rộng, một mắt vàng; sừng ngà dày cong; vuốt ngà; khố da đỏ nâu, bốn dải thành dây tết đầu son",
              ["BODY: all the blocky pieces (shoulders, arms, fists, the back arms) become dark earth-brown ROCK: flat #6B4A33 on the faces "
               "turned to the viewer, #4E3424 on the faces turned away; on each big block ONE flat ochre-yellow #D9A441 war stripe (a simple "
               "band); the joints and inner limbs very dark brown #2F2119 (flat); no cracks, no carved signs, no rings, no machine parts.",
               "CHEST: the chest plate becomes a big rounded slab of ochre-yellow sandstone #D9A441 with one flat darker band #B27F2E; the "
               "paler lower plate dark brown #6B4A33.",
               "HEAD: NEW SHAPE: a heavy rock helm shaped like the head of a BULL (a broad brow, a short blunt muzzle), in the same place, "
               "with ONE fierce round yellow eye #F6C443 (dark pupil, one small white dot) in the middle under the brow; no diamond socket.",
               "HORNS: thick curved IVORY horns #EFE3C6, in the same places, curving out and up.",
               "CLAWS AND FINGERS: ivory #E9DCC0; the fingers of the back hands thick, with short ivory claws.",
               "APRON AND STRAPS: the cloth becomes dark red-brown hide #8A3D2A; the four straps become four short braided ropes with ochre "
               "tips."]),
    },
    kiem=("đúng dáng (nhìn thẳng, gù, hai nắm đấm chống đất hai bên dưới, hai tay phụ giơ hai bên trên); MỘT mắt; đầu, sừng, ngực đổi dáng; "
          "là sinh vật đá, không còn chi tiết máy; mọi tay dính thân"),
)
