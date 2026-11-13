# -*- coding: utf-8 -*-
"""Gói GPT vẽ rùa golem lửa (mã làm việc rua_lua, con gốc của rig: monster_3425). Tướng thứ 5 đảo Hỏa.

Người dùng (2026-11-13): "concept rùa golem lửa, đổi pha lê đỏ trên lưng thành gai lửa, lửa cũng phải có animation đung đưa nhẹ".
appear: cái mai nằm dưới đất rồi chân tay đầu đuôi mọc ra, gầm một phát; idle, walk giống con gốc; đánh thường bò nhanh tới mục tiêu
và húc như skill_03; chiêu mana như skill_04 (đứng lên nhẹ, há mồm, tụ cầu lửa rồi bắn); chiêu cuối tụ cầu lửa trên sừng, lửa hút từ
lửa trên lưng, hút hết thì phóng cầu vào địch; die lửa tắt, tướng quỵ xuống. Ba hướng màu là ĐỀ XUẤT của Claude, chờ người dùng chọn.
Chỉ lấy của con gốc cách dựng (chỗ, cỡ, thứ tự chồng từng part); hình là của mình. Không đính ảnh con gốc; đính sơ đồ bố cục tự dựng
bằng mã (rua_lua_bo_cuc.py).

    py -3 -I ArtGen/Spine/rua_lua_bo_cuc.py all
    py -3 -I ArtGen/Spine/build_rua_lua.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/rua_lua_1/luot_1_concept_<hướng>.txt [--note "..."]
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "rua_lua"
K = 1
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
KIEM_SI = os.path.join(HERE, "inbox", "kiem_si_1", "tai_ve", "L1_duyet.png")
GOLEM = os.path.join(HERE, "inbox", "golem_lua_1", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def pk():
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{K}")


def save_dir():
    return os.path.join(HERE, "inbox", f"{CODE}_{K}", "tai_ve")


def mau_dir():
    return os.path.join(HERE, "inbox", f"{CODE}_{K}", "mau")


def bc():
    return json.load(open(os.path.join(mau_dir(), "bo_cuc.json"), encoding="utf-8"))


def xy(b):
    return f"x = {b[0]} to x = {b[2]}, y = {b[1]} to y = {b[3]}"


def pt(p):
    return f"({p[0]}, {p[1]})"


STANCE = ("STANCE (the same as in the layout guide, image 1): a heavy FOUR-LEGGED ROCK TORTOISE GOLEM standing on four short thick "
          "pillar legs, seen from its left side in a slight three-quarter view, FACING THE VIEWER'S RIGHT. A big domed SHELL built "
          "from thick stone slabs covers its back; clusters of dark stone columns stick out of the shell, and a row of FLAME SPIKES "
          "burns on top of the shell. Its head sits LOW at the FRONT (right): a skull-like stone face mask with one fierce eye and "
          "a separate lower jaw; a HUGE curved horn rises from the near side of the head, and a shorter blunt horn from the far "
          "side. A short thick tail with small spikes at the back (left). Fierce, determined, ready to charge: head lowered, horn "
          "forward. Chunky and appealing like a monster-collecting game creature, NOT a cute smiling mascot, NOT horror, NOT a "
          "robot, NOT a real animal.")

BODY = (
    "- THE SHELL (the biggest piece, about {mai}): a big domed stone shell like a boulder, built from a few large flat stone "
    "slabs (three or four straight seam lines between the slabs, nothing else). Its lower edge arches up over the near front leg "
    "and comes down again in front, toward the head. Under the shell, a lighter stone BELLY plate and shell rim show between the "
    "legs (about {bung}), colour {bung_ten}.\n"
    "- THE STONE COLUMNS on the shell (colour {cot_ten}): on the near (left) side of the shell a cluster of five or six short "
    "thick faceted stone columns like basalt pillars, leaning a little to the upper left, stepping down toward the tail (about "
    "{cot_gan}); they stand IN FRONT of the bases of the flame spikes. A second small pair of columns at the top right of the "
    "shell, behind the big horn (about {cot_xa}).\n"
    "- THE FLAME SPIKES (the only fire on the back; where a rock monster would have crystal spikes, this one has spikes MADE OF "
    "FIRE growing straight out of the shell): {lua_ds} "
    "Draw every flame spike as a real hand-drawn FLAME with the bold silhouette of a spike: a thick base sitting on the shell, a "
    "body that tapers with only a slight S-curve, and one sharp tip that leans a little BACK (toward the viewer's left); the big "
    "ones may have one small side lick. Three nested flat colour zones: red-orange {lua0} outside, orange {lua1}, yellow {lua2} "
    "inside near the base. NOT crystals, NOT rocks, NOT horns, NOT leaves; no hole, ring or collar at the base.\n"
    "- THE HEAD (about {mat_so}, colour {so_ten}): a SKULL-LIKE STONE FACE MASK turned three-quarters to the right, low at the "
    "front of the body, its muzzle pointing down-right. ONE eye only (centre about {mat}): a dark angular eye socket with a "
    "slanted, fierce, bright yellow-orange FIRE EYE ({lua2}) with a small dark pupil looking right; the other eye is hidden. A "
    "jagged crack-like seam runs down the mask behind the eye. Below the mask a separate LOWER JAW block (about {ham}) with a "
    "stepped, notched edge where it meets the mask, like big blunt stone teeth; mouth closed. No nose, no ears, no smile, no "
    "tongue.\n"
    "- THE BIG NEAR HORN (about {sung_gan}, colour {sung_ten}): it starts as a thick angular faceted block on the near side of the "
    "head (covering the top-left of the face mask) and sweeps up to the right in one long smooth curve, ending in a sharp tip at "
    "about ({sung_x}, {sung_y}); thick at the base, thin at the tip, like a rhino or triceratops horn. One colour, at most one "
    "facet line.\n"
    "- THE FAR HORN (about {sung_xa}, same colour): the SAME kind of horn as the near one, WHOLE and INTACT, only smaller because "
    "it is on the far side: a thick faceted base behind the face mask, sweeping up to the right in a smooth curve to ONE SHARP "
    "POINTED TIP at about (1240, 470). NOT broken, NOT blunt, NOT cut off flat. It is BEHIND the face mask.\n"
    "- THE LEGS (colour {da_ten}): four short thick stone PILLAR legs with flat feet, each made of a rounded thigh block and a "
    "bigger lower-leg block that overlaps it. NEAR FRONT leg in front of the shell (about {ctg}); NEAR HIND leg at the left "
    "(about {csg}); FAR FRONT leg at the right under the far horn (about {ctx}), partly hidden behind the jaw; FAR HIND leg "
    "between the two near legs, behind the belly (about {csx}). Two or three small angular LAVA CRYSTALS (hot orange, {ple}) "
    "stick out of the top of the near front leg (around {ple1}) and of the far front leg (around {ple2}): small simple faceted "
    "shards, each one flat colour.\n"
    "- THE TAIL (about {duoi}): a short thick stone tail pointing to the lower left, tapering to a blunt point, with THREE small "
    "curved spikes ({gai_ten}) along its upper edge.")

SIMPLE = ("VERY SIMPLE DESIGN, FEW DETAILS (very important): big clean chunky shapes, each stone piece ONE flat colour with at most "
          "ONE facet or seam line; NO cracks except the one seam on the face mask, NO lava cracks, NO runes, NO glowing lines on "
          "the stone, NO moss, NO extra spikes, NO extra horns, NO extra flames, NO smoke. The ONLY fire-coloured things on the "
          "creature are: the flame spikes on the shell, the eye, and the small lava crystals on the two front legs.")

FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the figure stands in the middle of the canvas: from the tip of the tail at "
         "about x = {x0} to the far horn at about x = {x1}, and from the tip of the tallest flame spike at about y = {y0} to the "
         "bottom of the feet at about y = {y1}. Do NOT enlarge, shrink or move the figure.")

POSE = ("ANIMATION-READY (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): calm, "
        "clean resting pose exactly as in the guide, all four feet flat on the same ground level. Draw every piece as a clear, "
        "simple, closed shape with its own complete ink outline, so that the pieces can be separated: the shell, each column "
        "cluster, each flame spike, the face mask, the jaw, each horn, each thigh block, each lower leg, the tail, the belly. The "
        "pieces touch or overlap but are NOT melted into one blob. No sparks, no embers, no smoke, no glow, no speed lines, no "
        "ground, no lava puddle, no props, no second character.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram: take ONLY the placement, the sizes, the overlaps and the kind of colour of each "
        "piece from it, never its line, its blob edges or its exact shapes. Design the real shape of every piece yourself as "
        "described: bold, chunky, readable shapes with a clear silhouette and clean bevelled stone blocks, the way a carefully "
        "designed Pokemon-like rock monster is drawn. Do NOT copy any existing character.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 5 px thick on this canvas around every big piece, and about 3 px for small "
        "details (seam lines, the pupil, the small crystals); every area coloured with coloured pencils and wax crayons, the "
        "strokes visible as loose diagonal hatching (strokes thinner than the outline), kept inside the outline. Clean and "
        "appealing, neither a crude scribble nor an over-rendered painting.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker underside, no shadows of any kind (no cast shadow of a piece on another, no shadow "
        "under the figure or on the background), no white highlights or shine spots (only the tiny dot in the eye), no gloss, no "
        "reflections, NO GLOW around the fire, the crystals or the eye, no halo, no rim light, no gradients, no 3D look. The fire "
        "looks hot only because its flat colours are bright.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no effects around the "
      "character.")

LUA = ("#E0441F", "#F7902A", "#FFD45A")
PLE = "#F28A2E"
D = {
    "bazan": dict(
        ten="đá bazan xám lam, cột đá chàm than, sọ và sừng màu ngà",
        da_ten="slate blue-grey stone (#5F6C7D)", cot_ten="dark navy-charcoal stone (#353B48)",
        bung_ten="lighter blue-grey (#8793A1)", so_ten="warm ivory bone-stone (#E6DAC0)", sung_ten="pale ivory (#F0E8D4)",
        gai_ten="pale ivory, #F0E8D4",
        palette=("COLOURS (use exactly these, each area one flat colour): the shell slate blue-grey basalt (#4E5A6C); the legs and "
                 "tail a slightly lighter slate blue-grey (#5F6C7D); the stone columns dark navy-charcoal (#353B48); the belly and "
                 "shell rim lighter blue-grey (#8793A1); the face mask and jaw warm ivory bone-stone (#E6DAC0); the two horns and "
                 "the tail spikes pale ivory (#F0E8D4); the flame spikes red-orange (#E0441F) / orange (#F7902A) / yellow "
                 "(#FFD45A); the eye yellow (#FFD45A) in a dark socket; the small leg crystals hot orange (#F28A2E); every "
                 "outline dark-brown ink (#2B2118). Only these colours: NO green, NO purple, NO pink, NO red stone."),
        check=["Mai và chân **xám lam**, cột đá **chàm than**, mặt sọ + hàm **ngà ấm**, hai sừng và gai đuôi **ngà nhạt**."]),
    "dat_son": dict(
        ten="đá sa thạch vàng son, cột đá và sừng nâu sẫm, sọ kem",
        da_ten="warm ochre sandstone (#C9A05C)", cot_ten="dark umber-brown stone (#5B4334)",
        bung_ten="pale sand (#E0C48C)", so_ten="cream bone-stone (#F0E4C6)", sung_ten="dark umber-brown (#5B4334)",
        gai_ten="cream, #F0E4C6",
        palette=("COLOURS (use exactly these, each area one flat colour): the shell ochre sandstone (#BA8E4A); the legs and tail a "
                 "slightly lighter warm ochre (#C9A05C); the stone columns dark umber-brown (#5B4334); the belly and shell rim pale "
                 "sand (#E0C48C); the face mask and jaw cream bone-stone (#F0E4C6); the two horns dark umber-brown (#5B4334); the "
                 "tail spikes cream (#F0E4C6); the flame spikes red-orange (#E0441F) / orange (#F7902A) / yellow (#FFD45A); the "
                 "eye yellow (#FFD45A) in a dark socket; the small leg crystals hot orange (#F28A2E); every outline dark-brown ink "
                 "(#2B2118). Only these colours: NO blue, NO green, NO purple, NO pink, NO grey."),
        check=["Mai và chân **vàng son**, cột đá và **hai sừng nâu sẫm**, mặt sọ + hàm **kem**."]),
    "ca_phe": dict(
        ten="đá nâu cà phê sẫm, cột đá nâu đen, sọ và sừng màu ngà",
        da_ten="dark coffee-brown stone (#68503F)", cot_ten="brown-black stone (#382C28)",
        bung_ten="tan (#9A7B5E)", so_ten="warm ivory bone-stone (#E8DCC0)", sung_ten="pale ivory (#F0E8D4)",
        gai_ten="pale ivory, #F0E8D4",
        palette=("COLOURS (use exactly these, each area one flat colour): the shell dark coffee-brown stone (#5C4638); the legs "
                 "and tail a slightly lighter coffee brown (#68503F); the stone columns brown-black (#382C28); the belly and shell "
                 "rim tan (#9A7B5E); the face mask and jaw warm ivory bone-stone (#E8DCC0); the two horns and the tail spikes pale "
                 "ivory (#F0E8D4); the flame spikes red-orange (#E0441F) / orange (#F7902A) / yellow (#FFD45A); the eye yellow "
                 "(#FFD45A) in a dark socket; the small leg crystals hot orange (#F28A2E); every outline dark-brown ink (#2B2118). "
                 "Only these colours: NO blue, NO green, NO purple, NO pink, NO grey, NO brick red."),
        check=["Mai và chân **nâu cà phê sẫm**, cột đá **nâu đen**, mặt sọ + hàm + sừng + gai đuôi **ngà**."]),
}

TEN_LUA = [  # (tên trong bo_cuc.json, mô tả tiếng Anh)
    ("lua_cao", "the TALLEST flame spike stands in the middle of the top of the shell: base about {goc}, almost straight up, its "
                "tip at about {ngon} (the highest point of the whole figure)"),
    ("lua_trai", "a LONG flame spike left of it leans to the upper LEFT: base about {goc}, tip about {ngon}"),
    ("lua_giua_trai", "a shorter one between those two, leaning upper left: base about {goc}, tip about {ngon}"),
    ("lua_phai", "a medium one right of the tallest: base about {goc}, up, tip about {ngon}"),
    ("p_kuangshi02", "a small one further right: base about {goc}, tip about {ngon}"),
    ("p_kuangshi07", "one at the right end of the shell, behind the big horn (the horn overlaps it): base about {goc}, leaning "
                     "upper right, tip about {ngon}"),
    ("p_kuangshi06", "a small one low on the back of the shell, above the tail: base about {goc}, leaning upper left, tip about {ngon}"),
]

CHECK_CHUNG = [
    "Bố cục y sơ đồ: rùa golem **bốn chân** nhìn sang **phải**, đầu **thấp phía trước**; mặt sọ đá **một mắt**, hàm dưới là khối riêng.",
    "Pha lê đỏ trên lưng của con gốc thành **gai lửa** (lửa thật dáng gai: gốc dày trên mai, thon dần, ngọn nhọn ngả về sau): một cái cao "
    "nhất giữa mai, hai cái ngả trái, hai ba cái nhỏ bên phải, một cái sau sừng, một cái nhỏ trên đuôi. Không phải pha lê, sừng.",
    "**Hai sừng lành lặn, mũi nhọn** (người dùng dặn 2026-11-13: không làm gãy một bên): sừng gần to cong vút lên phải (chiêu cuối tụ cầu lửa trên sừng này), sừng xa cùng kiểu, nhỏ hơn, nằm sau mặt.",
    "Cụm **cột đá** sẫm trên mai phía gần (che gốc gai lửa) và hai cột nhỏ sau sừng; bốn chân trụ ngắn, đuôi ngắn ba gai.",
    "Pha lê nhỏ ở hai chân trước giữ là pha lê, màu cam dung nham.",
    "Ít chi tiết: mỗi khối một màu, nhiều nhất một nét; không vết nứt dung nham, không hoa văn, không lửa thừa.",
    "Tô phẳng, không bóng, **không quầng sáng** quanh lửa; nét bút nâu rung, vân sáp; nền trắng.",
]

FIX = [
    ("Gai lửa thành pha lê / sừng / đá", "Every spike on the shell must be a real FLAME shaped like a spike: thick base on the shell, tapering body with a slight S-curve, sharp tip leaning back to the left, three nested flat colours. Not crystals, not horns."),
    ("Có quầng sáng / tia lửa bay / khói", "Remove every glow, halo, spark, ember and smoke. Flat colours only."),
    ("Mặt nhìn thẳng / hai mắt", "ONE fierce slanted eye on the skull-like face mask low at the FRONT RIGHT, looking right, exactly as in the layout guide."),
    ("Thêm vết nứt dung nham / hoa văn", "Remove all lava cracks, runes and ornaments: each stone piece one flat colour with at most one seam line."),
    ("Các khối dính liền một cục", "Every stone piece (shell, columns, thighs, lower legs, jaw, horns, tail) is a separate block with its own complete ink outline."),
    ("Có bóng đổ / tô khối", "Flat colour only: no shading, no cast shadow, no highlights."),
    ("Thành rùa thật / dễ thương", "It is a fierce ROCK GOLEM shaped like a tortoise, built from stone blocks, with a skull-like stone face and a huge horn; not a real turtle, not a cute mascot."),
]


def refs(kieu):
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature in its resting stance, built "
         "from rough coloured blobs: where every piece goes on the canvas, how big it is and which piece overlaps which (the big "
         "shell; the dark column clusters on it; flame-coloured spikes on top of the shell; the pale face mask and jaw low at the "
         "front right with one eye; the big curved near horn and the short far horn; four pillar legs with small orange crystals "
         "on the front ones; the tail with small spikes at the left). Use it for placement, size and overlap only; design and "
         "redraw everything in the hand-drawn style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng) ở dáng nghỉ của rig: mai lớn, cụm cột đá sẫm, gai lửa trên đỉnh mai, "
         "mặt sọ + hàm màu sáng thấp phía trước bên phải, sừng gần cong to, sừng xa ngắn, bốn chân trụ, đuôi có gai. Lấy chỗ đặt, cỡ, "
         "thứ tự chồng"),
        (KIEM_SI,
         "an approved hero of the same game (an armoured monkey samurai), 1536x1024, white background: match EXACTLY its wobbly "
         "dark-brown pen line, its visible crayon hatching, its completely flat colouring, its bold chunky shapes and its fierce "
         "battle-ready attitude. Do NOT copy its species, its design or its colours.",
         "Voọc Tướng đã duyệt (1536 × 1024, nền trắng): khỉ samurai giáp lục. Lấy nét bút rung, vân sáp, tô phẳng, thần thái chiến"),
        (GOLEM,
         "another approved hero of the same game and the same volcano island, a stone golem with flames, 1536x1024, white "
         "background: see how its stone blocks and its fire are drawn (flat colour zones, wobbly ink, crayon hatching, no glow). "
         "Do NOT copy its design, its body, its rings and holes, or its colours.",
         "Golem lõi lửa (tướng 4 đảo Hỏa, đã duyệt; 1536 × 1024, nền trắng): lấy cách vẽ khối đá và lửa"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp"),
    ]


SUNG_BAN = {"bazan": "L1_bazan.png", "bazan_gai": "L1_bazan_2.png", "dat_son": "L1_dat_son.png", "ca_phe": "L1_ca_phe.png"}


def build_sung():
    """lượt 1b (người dùng 2026-11-13: "làm 2 sừng lành lặn đi không làm gãy 1 bên"): vẽ lại đúng bản nháp, chỉ đổi sừng xa thành
    sừng nguyên mũi nhọn."""
    ra = []
    for ban, f in SUNG_BAN.items():
        src = os.path.join(save_dir(), f)
        if not os.path.exists(src):
            continue
        out = os.path.join(save_dir(), f"L1b_{ban}.png")
        p = os.path.join(pk(), f"luot_1b_sung_{ban}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(src)}: the current draft of our own game creature (a fire tortoise golem), 1536x1024, white background. "
             "It is the picture to redraw.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as L1b_{ban}_2.png, L1b_{ban}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "",
             "TASK: redraw image 1 as the SAME picture, same canvas 1536x1024, changing ONLY ONE THING: the FAR HORN.", "",
             "KEEP IDENTICAL (if the new picture were laid over image 1, everything except the far horn must coincide): the whole "
             "creature at the same position and size; the shell, the stone columns, every flame on the shell (same shapes, same "
             "positions), the skull-like face mask with its one eye, the jaw, the BIG NEAR HORN, the four legs with their small orange "
             "crystals, the tail with its spikes, the belly; the same colours; the same wobbly dark-brown ink outline and visible "
             "crayon hatching; completely flat colouring; pure-white background.", "",
             "CHANGE ONLY THIS: the far horn is the shorter horn at the right of the head, behind the face mask, pointing up-right "
             "(in image 1 it is a blunt prong whose tip is broken off flat, between about x = 1040 and x = 1230, y = 530 and y = 770). "
             "Redraw it as a WHOLE, INTACT horn of the same kind as the big near horn, only smaller because it is on the far side of "
             "the head: a thick base coming out from BEHIND the face mask (the mask still overlaps its base), then a smooth curve "
             "sweeping up and to the right, tapering evenly to ONE SHARP POINTED TIP at about (1245, 465). Same colour as the near "
             "horn, one flat colour, at most one facet line, complete ink outline. NOT broken, NOT chipped, NOT blunt, NOT cut off "
             "flat. Both horns of the creature are now whole and pointed.", "",
             "Do not add anything else: no new spikes, no cracks, no glow, no sparks, no smoke, no shadow, no ground line, no text. "
             "No white border or sticker outline around the figure."]
        ghi(p, t)
        ra.append(p)
        print(p)
    return ra


def build_chan():
    """lượt 1c (người dùng 2026-11-13, chọn A: "A nhưng chân phải trước đang bị rách rời khỏi thân"): vẽ lại đúng L1b_bazan, chỉ nối
    chân TRƯỚC XA vào thân (bụng chạy tiếp ra sau hàm tới chân, đùi lộ sau mặt)."""
    src = os.path.join(save_dir(), "L1b_bazan.png")
    out = os.path.join(save_dir(), "L1c_bazan.png")
    p = os.path.join(pk(), "luot_1c_chan_bazan.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(src)}: the current draft of our own game creature (a fire tortoise golem facing right), 1536x1024, white "
         "background. It is the picture to redraw.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as L1c_bazan_2.png, L1c_bazan_3.png ... in the same folder. Do not edit, "
         "move or delete any other file.", "",
         "TASK: redraw image 1 as the SAME picture, same canvas 1536x1024, fixing ONLY ONE THING: the FAR FRONT LEG must be clearly "
         "ATTACHED to the body.", "",
         "KEEP IDENTICAL (if the new picture were laid over image 1, everything else must coincide): the whole creature at the same "
         "position and size; the shell, the stone columns, every flame on the shell (same shapes, same positions), the skull-like "
         "face mask with its one eye, the jaw, BOTH horns (both whole and pointed), the near front leg and the two hind legs with "
         "their small orange crystals, the tail with its spikes; the same colours; the same wobbly dark-brown ink outline and "
         "visible crayon hatching; completely flat colouring; pure-white background.", "",
         "THE PROBLEM in image 1: the far front leg is the leg at the far right of the picture, under the small far horn, to the "
         "right of the jaw (about x = 1020 to x = 1240, y = 700 to y = 940). It looks torn off the body: it only touches the jaw, "
         "and white background shows between the belly, the bottom of the jaw and that leg (around x = 950 to x = 1030, y = 840 to "
         "y = 900).", "",
         "FIX IT LIKE THIS (anatomy: the creature is a four-legged tortoise seen from its left side; its far front leg grows out "
         "of the chest, on the other side of the body, BEHIND the head):",
         "1. The lighter blue-grey BELLY / CHEST plate under the shell continues to the RIGHT, passing BEHIND the jaw, until it "
         "reaches the far front leg. Its lower edge runs on as one line from behind the near front leg to the far front leg at about "
         "y = 860 to y = 880. No white background anywhere between the belly, the jaw and the far front leg.",
         "2. The far front leg gets a visible rounded THIGH block at its top (same slate blue-grey as the other legs), rising up "
         "and to the LEFT behind the jaw and the face mask toward the chest, so the leg clearly comes out of the body behind the "
         "head. The face mask and the jaw are IN FRONT and overlap the thigh and the chest; the thigh and the lower leg are in front "
         "of the belly plate. The lower leg keeps its place, its size and its two small orange crystals.",
         "3. The jaw, the face mask and the far horn do not move and do not change shape.", "",
         "Do not add anything else: no new spikes, no cracks, no glow, no sparks, no smoke, no shadow, no ground line, no text. No "
         "white border or sticker outline around the figure."]
    ghi(p, t)
    print(p)
    return p


def ghi(p, lines):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def main():
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    B = bc()
    x0, y0, x1, y1 = B["_khung"]
    gd = [f"# Gói gửi GPT: `{CODE}` (rùa golem lửa, tướng thứ 5 đảo Hỏa, tên chưa đặt)", "",
          "Làm 2026-11-13: dựng trên rig của con gốc `monster_3425` (rùa golem đá bốn chân, pha lê đỏ trên lưng, mặt sọ đá, sừng "
          "to). Ba hướng màu là đề xuất của Claude, chờ người dùng chọn và duyệt concept. Ghi chú: "
          "`ArtGen/Spine/inbox/rua_lua_ghichu.md`.",
          "", "Lượt mảnh chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    lua_ds = " ".join(f"({i}) " + s.format(goc=pt(B["lua"][sl]["goc"]), ngon=pt(B["lua"][sl]["ngon"])) + ";"
                      for i, (sl, s) in enumerate(TEN_LUA, 1) if sl in B["lua"])
    ple = B["ple"]
    ple_truoc_gan = [p for p in ple if p[0] < 900]
    ple_truoc_xa = [p for p in ple if p[0] >= 900]

    def tb(ps):
        return pt([round(sum(p[0] for p in ps) / len(ps)), round(sum(p[1] for p in ps) / len(ps))])
    sg = B["lua"]  # noqa: F841
    sung = B["sung_gan"]
    ra = []
    for kieu, d in D.items():
        R = refs(kieu)
        missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
        if missing:
            raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
        out = os.path.join(save_dir(), f"L1_{kieu}.png")
        p = os.path.join(pk(), f"luot_1_concept_{kieu}.txt")
        body = BODY.format(
            mai=xy(B["mai"]), bung=xy(B["bung"]), bung_ten=d["bung_ten"], cot_ten=d["cot_ten"], cot_gan=xy(B["cot_gan"]),
            cot_xa=xy(B["cot_xa"]), lua_ds=lua_ds, lua0=LUA[0], lua1=LUA[1], lua2=LUA[2], mat_so=xy(B["mat_so"]),
            so_ten=d["so_ten"], mat=pt(B["mat_tam"][:2]), ham=xy(B["ham"]), sung_gan=xy(sung), sung_ten=d["sung_ten"],
            sung_x=sung[2], sung_y=sung[1], sung_xa=xy(B["sung_xa"]), da_ten=d["da_ten"], ctg=xy(B["chan_truoc_gan"]),
            csg=xy(B["chan_sau_gan"]), ctx=xy(B["chan_truoc_xa"]), csx=xy(B["chan_sau_xa"]), ple=PLE,
            ple1=tb(ple_truoc_gan), ple2=tb(ple_truoc_xa), duoi=xy(B["duoi"]), gai_ten=d["gai_ten"])
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "",
              "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
              "approved hero images.", "",
              "CREATURE: a FIRE TORTOISE GOLEM, a fire-element hero of the volcano island in a monster-collecting game: a living "
              "rock golem shaped like a heavy tortoise, built from thick separate stone blocks, with spikes of FIRE burning on its "
              "shell, a skull-like stone face and a huge horn. It is a creature (an elemental monster pet), NOT a robot, NOT a "
              "human, NOT a statue, NOT a real turtle.", "",
              STANCE, "",
              "Follow the LAYOUT GUIDE (image 1) for WHERE every piece is on the canvas, HOW BIG it is and WHICH piece overlaps "
              "which. Coordinates below are pixels on the 1536x1024 canvas (x from the left, y from the top). NEAR = the side of "
              "the body toward the viewer; FAR = the other side, partly hidden. LEFT / RIGHT are the viewer's.", "",
              body, "", SIMPLE, "",
              d["palette"], "", FRAME.format(x0=x0, x1=x1, y0=y0, y1=y1), "", POSE, "", SOFT, LINE, FLAT, BG]
        ghi(p, t)
        ra.append(p)
        gd += [f"## Hướng `{kieu}`: {d['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{K}/luot_1_concept_{kieu}.txt` (thêm "
               "`--note \"...\"` để sửa nhanh).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += ["", "Kiểm riêng hướng này:", ""] + [f"- {c}" for c in d["check"]] + [""]
    gd += ["Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/rua_lua_bo_cuc.py all`).",
           "", "## Kiểm chung", ""]
    gd += [f"- {c}" for c in CHECK_CHUNG]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    ghi(os.path.join(pk(), "HUONG_DAN.md"), gd)
    for p in ra:
        print(p)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sung":
        build_sung()
    elif len(sys.argv) > 1 and sys.argv[1] == "chan":
        build_chan()
    else:
        main()
