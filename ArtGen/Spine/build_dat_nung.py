# -*- coding: utf-8 -*-
"""Gói GPT vẽ chiến binh đất nung (mã làm việc dat_nung, con gốc của rig: monster_3625). Tướng thứ 8 đảo Hỏa.

Người dùng (2026-11-14): "làm tướng thứ 8 đảo hỏa; concept chiến binh đất nung đá dung nham, có lõi dung nham". Không dặn màu, chi
tiết: hai hướng dưới đây là ĐỀ XUẤT của Claude, chờ người dùng chọn. Chỉ lấy của con gốc cách dựng (bộ giáp rỗng lơ lửng, chỗ đặt,
cỡ, thứ tự chồng); hình từng mảnh là của mình. Không đính ảnh con gốc; đính sơ đồ bố cục tự dựng bằng mã (dat_nung_bo_cuc.py).

    py -3 -I ArtGen/Spine/dat_nung_bo_cuc.py
    py -3 -I ArtGen/Spine/build_dat_nung.py            (lượt 1: concept)
    py -3 -I ArtGen/Spine/build_dat_nung.py manh       (lượt 2: sáu tờ mảnh, sau khi có tai_ve/L1_duyet.png)
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/dat_nung_1/luot_1_concept_<hướng>.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "dat_nung"
K = int(os.environ.get("DN_DANG", "1"))
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
GOLEM = os.path.join(HERE, "inbox", "golem_lua_1", "tai_ve", "L1_duyet.png")
QUY = os.path.join(HERE, "inbox", "quy_dao_1", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def pk(k=K):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def mau_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "mau")


INTRO = {
    "tuong_binh": (
        "CREATURE: a TERRACOTTA WARRIOR GOLEM, a fire-element monster for a monster-collecting game: an ancient warrior statue of "
        "FIRED CLAY (terracotta) whose hollow armour pieces FLOAT in the air around a HEART OF MOLTEN LAVA, together with shards of "
        "dark LAVA ROCK. It carries one huge broad sword of black lava rock."),
    "lo_gom": (
        "CREATURE: a KILN-POT WARRIOR GOLEM, a fire-element monster for a monster-collecting game: a warrior built from big pieces "
        "of FIRED POTTERY (dark red brick-clay jars and tiles with cream-glazed rims) that FLOAT in the air around a HEART OF MOLTEN "
        "LAVA, together with shards of dark LAVA ROCK. It carries one huge broad sword of black lava rock."),
}
COMMON = (
    "It has NO legs and NO feet: it hovers. It has NO neck and NO torso of flesh: the chest is hollow and the round lava heart shows "
    "inside it. The pieces are not joined: the head, the shoulder armour, the arm slabs, the hands and the rock shards float near "
    "each other, overlapping like stacked armour, with small white gaps where the guide shows gaps. Character: a stern, heavy, "
    "battle-ready guardian warrior: huge shoulders, a small head sunk between them, a determined glare. Chunky, bold, simple "
    "shapes with few details (the way a rock-and-fire Pokemon is designed): appealing and tough, not scary, not a smiling cute "
    "mascot, not a human.\n"
    "Follow the LAYOUT GUIDE (image 1) for WHERE every piece floats on the canvas, HOW BIG it is and WHICH piece overlaps which. "
    "The outlines in the guide are only rough computer blobs: design the real outline of every piece yourself as described below, "
    "as a chunky block of fired clay or broken rock with its own character (a chipped corner, one crack), but keep every piece in "
    "its place and at its size.\n"
    "- VIEW: three-quarter front view. The warrior FIGHTS TOWARD THE VIEWER'S RIGHT: its head looks to the right. Its far "
    "shoulder is at the viewer's left; its near, bigger shoulder is at the viewer's right; its near arm comes from the right "
    "shoulder, sweeps across the bottom of the picture to the left and grips the sword there; its far arm hangs at the left "
    "behind the sword with an open hand.")

HEAD = {
    "tuong_binh": (
        "- HEAD (small, sunk between the shoulders, in front of the lava heart; the head block from about x = 722 to x = 915, "
        "y = 325 to y = 510, the hair knot above it up to about y = 257): the head of a terracotta soldier statue, simplified into "
        "ONE chunky rounded block of terracotta clay with a flat darker clay HEADBAND across the forehead, and ONE round HAIR KNOT "
        "(a topknot bun, about 90 px across) of dark lava rock sitting on top of the head toward the back (the viewer's left), "
        "tied with a thin clay band. FACE: turned toward the viewer's right: two slanted, angry EYES that are simple slits filled "
        "with bright lava yellow, under a heavy straight brow ridge; one short straight carved line for a firm closed mouth; no "
        "nose detail, no teeth, no beard, no ears. No horns."),
    "lo_gom": (
        "- HEAD (small, sunk between the shoulders, in front of the lava heart; from about x = 700 to x = 940, y = 300 to "
        "y = 513): a HELMET that is one big clay JAR turned upside-down: a tall rounded dome of dark red brick-clay, with a thick "
        "flat cream-glazed RIM band around its bottom edge (about 220 px wide, 40 px tall) and two small ring HANDLES (jar lugs) on "
        "its sides. In the dome, a T-SHAPED VISOR SLIT (a horizontal bar about 105 px wide with a short vertical bar under its "
        "middle), placed a little right of centre because the head looks toward the viewer's right; inside the slit only flat "
        "bright lava yellow shows, like two glaring eyes joined into one fierce visor: make the top edge of the horizontal bar "
        "slant down toward the middle so it reads as an angry frown. No other face, no mouth, no horns."),
}

BODY = {
    "tuong_binh": (
        "- LAVA HEART (centre of the hollow chest, a round disc from about x = 584 to x = 895, y = 365 to y = 685, mostly hidden "
        "behind the head and the collar arcs): a ball of MOLTEN LAVA, flat deep orange, with three or four small darker-orange "
        "crust patches drifting on it. On its lower left, fully visible (centre about x = 712, y = 597, about 78 px across): the "
        "CORE, a perfectly round bright yellow disc with ONE thin orange ring line inside it. The heart is the brightest thing in "
        "the picture but it is flat colour: no glow, no rays, no sparks.\n"
        "- TWO COLLAR ARCS of darker clay curve around the lava heart like the two halves of an open breastplate: one at the left "
        "of the heart (about x = 569-730, y = 332-572), one sweeping under the head from the right to the core (about "
        "x = 750-1040, y = 395-641). Each is a thick curved band with a flat face and one carved groove line along it.\n"
        "- FAR SHOULDER ARMOUR (viewer's left, from about x = 460 to x = 716, y = 292 to y = 541) and NEAR SHOULDER ARMOUR "
        "(viewer's right, bigger and in front, from about x = 946 to x = 1130, y = 360 to y = 635): each ONE big curved plate of "
        "terracotta like a shoulder guard of LAMELLAR armour: its face is divided by thin carved lines into three rows of "
        "rectangular armour tiles, each tile with one small round rivet dot; a plain thick rim along its top edge.\n"
        "- TWO FLAT CLAY PLATES behind the sword at the left (about x = 328-580, y = 339-553 and x = 387-625, y = 405-678): "
        "pointed slabs of terracotta like broken roof tiles, each with one carved groove.\n"
        "- NEAR ARM (bottom of the picture, in front of everything except the sword hand): a round dark lava-rock SHOULDER JOINT "
        "(about x = 824-1085, y = 501-698); two stacked terracotta UPPER-ARM SLABS (about x = 842-1172, y = 603-888) and one long "
        "upright terracotta PLATE in front of them at the right (about x = 1008-1132, y = 553-885); a darker clay FOREARM block "
        "(about x = 709-955, y = 729-878) with a dark lava-rock under-slab below it (about x = 694-914, y = 795-935).\n"
        "- NEAR HAND (about x = 491-714, y = 722-913): one big terracotta FIST like a chunky gauntlet, four thick fingers wrapped "
        "around the sword's grip, the knuckles facing the viewer, one small round rivet on each knuckle.\n"
        "- FAR ARM (viewer's left, behind the sword): a terracotta upper-arm block (about x = 464-621, y = 451-611), a dark "
        "lava-rock forearm block (about x = 423-549, y = 573-725), a terracotta palm block (about x = 395-551, y = 688-801) and an "
        "OPEN HAND of five short fingers, each finger TWO separate little dark lava-rock stones (ten small stones, about "
        "x = 368-579, y = 657-848), slightly spread.\n"
        "- UNDER THE CHEST, instead of legs: three chunky dark lava-rock pieces hang close together (about x = 548-822, "
        "y = 643-824), the middle one the biggest, pointed downward. Nothing below them: the warrior hovers.\n"
        "- NINE LAVA-ROCK SHARDS float BEHIND the body like a fan or a broken stone halo, their points away from the body: one up-"
        "left (about x = 434-731, y = 194-557), one straight up behind the head (x = 756-812, y = 110-454), one up-right "
        "(x = 794-1030, y = 166-500), one long one to the right and up (x = 822-1211, y = 219-568), two shorter ones behind the "
        "near shoulder (x = 923-1191, y = 377-574 and x = 890-1058, y = 333-588), one pointing DOWN at the far right "
        "(x = 1075-1163, y = 411-763), one low at the right (x = 790-960, y = 617-785) and one low at the left (x = 488-745, "
        "y = 486-724). Each is a STRAIGHT, chunky, pointed splinter of dark rock (like a broken piece of cooled lava crust; wide "
        "at the body end, a sharp tip, three or four straight facet edges), with ONE thin zigzag crack of orange lava along its "
        "middle. They are straight, not curved; not horns, not wings, not flames.\n"
        "- SWORD (held upright and slanted at the viewer's left, IN FRONT of the far arm and the left plates; the fist grips it at "
        "about x = 574, y = 807; the tip at about x = 306, y = 67): a huge BROAD SWORD, about 790 px long. BLADE of black lava "
        "rock about 135 px wide, straight, getting slightly wider toward the end, then a short pointed tip; down the middle of the "
        "blade a straight CHANNEL about 45 px wide filled with flat orange lava, with one thin bright-yellow line along its "
        "centre. GUARD: a chunky terracotta block wider than the blade (about 185 px), its two ends turned slightly up toward the "
        "blade. GRIP: a short dark rod, mostly hidden inside the fist. POMMEL (below the fist, at about x = 622, y = 945): a "
        "terracotta RING about 70 px across with a dark centre.\n"
        "- Exactly: one head, one lava heart with one core, two collar arcs, two shoulder armours, two flat plates at the left, "
        "one near arm with one fist, one far arm with one open five-finger hand, three hanging rock pieces, nine rock shards, one "
        "sword."),
}
BODY["lo_gom"] = (
    BODY["tuong_binh"]
    .replace("each ONE big curved plate of terracotta like a shoulder guard of LAMELLAR armour: its face is divided by thin carved "
             "lines into three rows of rectangular armour tiles, each tile with one small round rivet dot; a plain thick rim along "
             "its top edge.",
             "each ONE big curved piece of a huge broken clay JAR (a round belly shard, hollow inside): dark red brick-clay with a "
             "thick cream-glazed RIM band along its top edge and ONE painted cream zigzag band across its belly; one chipped "
             "notch in its lower edge.")
    .replace("TWO COLLAR ARCS of darker clay", "TWO COLLAR ARCS of darker brick-clay")
    .replace("pointed slabs of terracotta like broken roof tiles", "pointed shards of red brick-clay like broken roof tiles")
    .replace("terracotta", "red brick-clay"))

PALETTE = {
    "tuong_binh": (
        "COLOURS, a warm, slightly muted palette (use exactly these, each area one flat colour): TERRACOTTA CLAY (head, shoulder "
        "armours, left plates, upper-arm slabs, the upright plate, palm, fist, sword guard and pommel) warm orange-brown (#C8683C); "
        "DARKER CLAY (collar arcs, forearm block, headband, the carved lines and rivets) deep brick-brown (#96482C); LAVA ROCK "
        "(hair knot, shards, shoulder joint, hanging pieces, far forearm, finger stones, under-slab, sword blade and grip) warm "
        "charcoal brown-black (#4A3E3C); LAVA (heart, cracks in the shards, sword channel) flat orange (#EE7A22); the CORE, the "
        "eyes and the thin line in the sword channel bright lava yellow (#FFD64A); every outline dark-brown ink (#2B2118). Only "
        "these colours. NO grey stone, NO blue, NO green, NO purple, NO gold metal, NO red flames."),
    "lo_gom": (
        "COLOURS, a warm, slightly muted palette (use exactly these, each area one flat colour): RED BRICK-CLAY (helmet dome, "
        "shoulder jar pieces, left plates, upper-arm slabs, the upright plate, palm, fist, sword guard and pommel) deep brick red "
        "(#A8432F); DARKER BRICK-CLAY (collar arcs, forearm block, jar handles, carved lines) dark red-brown (#78302A); CREAM GLAZE "
        "(the helmet rim band, the rim bands and zigzag bands of the shoulder pieces: only these) warm cream (#E8D8B0); LAVA ROCK "
        "(shards, shoulder joint, hanging pieces, far forearm, finger stones, under-slab, sword blade and grip) cool charcoal black "
        "(#3E3A44); LAVA (heart, cracks in the shards, sword channel) flat orange (#F28C28); the CORE, the visor slit and the thin "
        "line in the sword channel bright lava yellow (#FFE066); every outline dark-brown ink (#2B2118). Only these colours. NO grey "
        "stone, NO blue, NO green, NO gold metal, NO red flames."),
}

FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the whole figure with its sword is about 900 px wide (from about x = 285 to "
         "x = 1215) and about 920 px tall (from the sword tip at about y = 65 to the sword pommel at about y = 980).")

POSE = ("POSE (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): hovering still in "
        "a calm, clean, ready stance, exactly as in the guide. EVERY piece is one closed shape with its own closed ink outline; "
        "where one piece overlaps another, the front piece simply covers the back one. No dust, no sparks, no embers, no smoke, "
        "no flames, no glow, no motion lines, no dripping lava, no ground, no props.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram with rough, jagged edges: take only the placement, the sizes, the overlaps and the "
        "colour of each kind of piece from it, never its line, its jagged edge noise or its exact blobs. Draw the clay pieces as "
        "bold chunky blocks with softly rounded corners (hand-shaped clay), the lava-rock pieces as angular broken blocks with "
        "straight facet edges.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 6 px thick on this canvas around every big piece (head, shoulder armours, "
        "plates, arm slabs, fist, shards, sword, heart), and about 4 px for small pieces and details (finger stones, core, eyes, "
        "pommel, hair knot band); the carved grooves, tile lines, rivets and facet lines are thin darker pencil lines about 3-4 "
        "px, not ink; every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching "
        "(strokes thinner than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly "
        "detailed: no small cracks all over, no pebbly texture, no realistic rock or clay rendering.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker side of a block, no lighter patches, no shadows of any kind (no cast shadow of one "
        "piece on another, no shadow under the figure or on the background), no white highlights or shine spots, no gloss, no "
        "glow around the lava, the core, the eyes or the sword channel, no rim light, no gradients, no 3D look. A different tone "
        "appears only where the design itself lists a different colour. One tiny lighter dot in the eyes is allowed.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the creature.")

TEN = {"tuong_binh": "tượng binh đất nung cam: đầu có búi tóc đá, giáp vai xếp vảy ngói, đá dung nham nâu than",
       "lo_gom": "chiến binh lò gốm gạch đỏ sẫm: mũ là chiếc vò úp có khe chữ T, giáp vai là mảnh vò vỡ vành men ngà, đá dung nham đen"}


def refs(kieu):
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature showing where every floating "
         "piece goes on the canvas, how big it is and which piece overlaps which (clay colour: the small head in the middle, the "
         "two big shoulder armours, the plates at the left, the arm slabs and the big fist at the bottom; darker clay: the two "
         "collar arcs and the forearm; dark rock: the nine pointed shards fanned behind the body, the shoulder joint, the hanging "
         "pieces under the chest, the finger stones at the left; orange disc with a yellow ball: the lava heart and its core; the "
         "huge dark sword with an orange channel held at the left). Use it for placement, size and overlap only; redraw everything "
         "in the hand-drawn style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): các khối giáp lơ lửng tô phẳng (màu đất nung: đầu nhỏ ở giữa, hai "
         "giáp vai lớn, hai phiến bên trái, các tấm tay và nắm tay to phía dưới; đất nung sẫm: hai vành cổ, cẳng tay; đá sẫm: chín "
         "mảnh đá nhọn xoè sau lưng, khớp vai, mảnh treo dưới ngực, đốt ngón tay bên trái; đĩa cam có viên vàng: lõi dung nham; "
         "thanh kiếm lớn sẫm có rãnh cam dựng chéo bên trái). Lấy chỗ đặt, cỡ, thứ tự chồng"),
        (GOLEM,
         "an approved hero of the same game and the same island (a rock golem with flames), 1536x1024, white background: match "
         "EXACTLY its wobbly dark-brown pen line, its visible crayon hatching, its completely flat colouring and its bold, simple, "
         "chunky level of detail; see how its rocks are drawn with only two or three lines each. Do NOT copy its species, its "
         "design, its flames or its colours.",
         "Golem lõi lửa đã duyệt (1536 × 1024, nền trắng): golem đá kem xám có các ngọn lửa. Lấy nét bút rung, vân sáp, tô phẳng, mức "
         "chi tiết gọn"),
        (QUY,
         "another approved hero of the same island (an ash-grey fire demon with a huge blade), 1536x1024, white background: the "
         "same line and flat crayon colouring; see how its big weapon and its armour plates are drawn. Do NOT copy its species, "
         "design, weapon shape or colours.",
         "Quỷ lửa vác đao đã duyệt (1536 × 1024, nền trắng): quỷ da tro, giáp sắt đen, đao lớn. Lấy nét, tô phẳng, cách vẽ vũ khí và giáp"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp"),
    ]


CHECK = [
    "**Không chân**, bộ giáp rỗng **lơ lửng**; đầu nhỏ thụt giữa hai vai, **nhìn sang phải**; mỗi mảnh viền mực kín.",
    "**Lõi dung nham** tròn giữa ngực (đĩa cam) có **viên lõi vàng** lộ trọn ở phía dưới bên trái; không phát sáng.",
    "Đủ: hai giáp vai lớn (bên phải to hơn, ở trước), hai vành cổ sẫm, hai phiến bên trái, tay gần vắt ngang phía dưới với **nắm tay to "
    "cầm kiếm**, tay xa bên trái **xoè năm ngón đá**, ba mảnh đá treo dưới ngực, **chín mảnh đá nhọn thẳng** xoè sau lưng có khe dung nham.",
    "**Kiếm bản rộng** đá đen dựng chéo bên trái, rãnh dung nham cam chạy giữa, chắn tay và khâu chuôi màu đất nung.",
    "Hướng `tuong_binh`: đầu tượng binh có **búi tóc** đá + đai trán, mắt khe vàng; giáp vai **xếp vảy ngói** có đinh tán; màu đất nung cam. "
    "Hướng `lo_gom`: mũ là **chiếc vò úp** có khe chữ T vàng + vành men ngà + hai quai; giáp vai là **mảnh vò vỡ** vành men ngà, dải zíc zắc; "
    "màu gạch đỏ sẫm.",
    "Tô phẳng: **không** bóng, không mảng sáng tối, không điểm sáng, dung nham không phát sáng, không lửa, không tàn; nền trắng tinh.",
]

FIX = [
    ("Vẽ thêm chân, thân liền", "It has NO legs and NO solid torso: only floating armour pieces around the round lava heart. Remove the legs."),
    ("Đầu to, nhìn sang trái hoặc nhìn thẳng", "The head is SMALL (about 200 px wide), sunk between the shoulders, and looks toward the viewer's RIGHT."),
    ("Lõi phát sáng, có tia, quầng, tàn lửa", "The lava heart and the core are flat colour: remove the glow, the rays, the sparks and the embers."),
    ("Có bóng, mảng sáng tối, vẽ nổi khối", "Flat colour only: remove every shadow, highlight, darker side and gradient; each piece is one even colour "
                                            "with two or three thin carved lines; keep the crayon hatching as texture only."),
    ("Mảnh đá sau lưng cong như sừng, như cánh", "The nine shards behind the body are STRAIGHT pointed splinters of dark rock, not curved horns, not wings."),
    ("Thêm lửa cháy", "No flames anywhere: the only hot things are the lava heart, the thin lava cracks in the shards and the lava channel of the sword."),
    ("Quá nhiều vết nứt, chi tiết", "Simplify: bold chunky blocks, at most two or three carved lines per piece."),
    ("Kiếm khác kiểu (cong, răng cưa, lưỡi lửa)", "The sword is a straight BROAD sword: black rock blade with a straight orange lava channel down its middle, "
                                                 "a chunky clay guard, a clay ring pommel. Not curved, not jagged, not a flame."),
    ("Bố cục khác sơ đồ", "Follow image 1 exactly for the place and size of every piece: sword upright at the left gripped by the big fist at "
                          "the bottom, far open hand at the left, bigger shoulder at the right, shards fanned behind."),
]


def main():
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    gd = [f"# Gói gửi GPT: `{CODE}` dạng {K} (chiến binh đất nung, lõi dung nham; tướng thứ 8 đảo Hỏa, tên chưa đặt)", "",
          "Làm 2026-11-14: dựng trên rig của con gốc `monster_3625` (mọi mảnh cứng, lơ lửng); hình từng mảnh, màu, chi tiết là đề xuất "
          "của Claude, chờ người dùng chọn hướng và duyệt concept. Ghi chú: `ArtGen/Spine/inbox/dat_nung_ghichu.md`.", "",
          "Lượt 2 (mảnh) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    ra = []
    for kieu in ("tuong_binh", "lo_gom"):
        R = refs(kieu)
        missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
        if missing:
            raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
        out = os.path.join(save_dir(), f"L1_{kieu}.png")
        p = os.path.join(pk(), f"luot_1_concept_{kieu}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "",
              "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
              "approved hero images.", "",
              INTRO[kieu] + " " + COMMON, HEAD[kieu], BODY[kieu], "", PALETTE[kieu], "", FRAME, "", POSE, "", SOFT, LINE, FLAT, BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd += [f"## Hướng `{kieu}`: {TEN[kieu]}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{K}/luot_1_concept_{kieu}.txt` (thêm "
               "`--note \"...\"` để sửa nhanh).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += [""]
    gd += ["Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/dat_nung_bo_cuc.py`).",
           "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    open(os.path.join(pk(), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 2: MẢNH "đúng chỗ, đúng cỡ" (người dùng chọn hướng A tuong_binh, 2026-11-14)
MANH_CHUNG = ("TASK: redraw image 1, but keep ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the "
              "SAME SIZE as in image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). "
              "REMOVE everything else and leave pure white (#FFFFFF) there. Every kept part must be ONE COMPLETE CLOSED SHAPE with "
              "the dark-brown ink outline running all the way around it: where a part is hidden behind another part in image 1, "
              "DRAW the hidden portion as described. The kept parts must NOT touch each other: clear white between them (at least "
              "12 px). Same wobbly ink line, same colours, same crayon hatching, same completely flat colouring as image 1. Do not "
              "add anything: no shadows, no glow, no dust, no labels.")
MO_TA_EN = ("a terracotta warrior golem made of floating armour pieces: a small terracotta head with a dark rock hair knot and a "
            "headband, a round orange lava heart with a yellow core in the hollow chest, two darker clay collar arcs, two big "
            "shoulder armours of riveted armour tiles, two pointed clay fins at the left, dark lava-rock shards with orange zigzag "
            "cracks fanned behind the body, a row of dark rock teeth under the chest, a near arm of big terracotta blocks at the "
            "bottom right ending in a big fist that grips a huge broad sword (black rock blade with an orange lava channel, "
            "terracotta guard and ring pommel) held upright at the left, and a far open hand with dark finger stones at the far "
            "left.")
MO_TA_VI = ("chiến binh đất nung lơ lửng: đầu nhỏ có búi tóc đá và đai trán, lõi dung nham tròn có viên vàng, hai vành cổ sẫm, hai giáp "
            "vai vảy ngói có đinh tán, hai phiến nhọn bên trái, các mảnh đá dung nham có khe cam xoè sau lưng, hàng răng đá dưới ngực, tay "
            "gần gồm các khối đất nung ở dưới bên phải, nắm tay to cầm kiếm bản rộng dựng chéo bên trái, bàn tay xa xoè ngón đá ở mép trái")
MANH = {
    "A": ("đầu (có búi tóc), giáp vai XA vẽ đủ, nắm tay (không kiếm), tấm dựng bên phải, mảnh đá dài phía trên bên phải vẽ đủ",
          ["1. THE HEAD: the terracotta head block with its headband, its two yellow eyes, its mouth line, and the round dark hair "
           "knot with its clay band on top (from about x = 700 to x = 918, y = 238 to y = 515). In image 1 the right collar arc and a "
           "lava crust patch touch its lower edge: remove them and complete the head's rounded lower edge with an ink line.",
           "2. THE LEFT SHOULDER ARMOUR: the big curved armour plate of riveted tiles at the viewer's LEFT (its visible part from "
           "about x = 520 to x = 700, y = 262 to y = 600), with its plain thick rim on top. In image 1 its left part is covered by "
           "the sword and its right part by the darker collar arc: remove the sword and the arc and complete the plate: the tile "
           "rows and rivets continue under them; the whole plate is one rounded shape about 250 px wide (from about x = 462 to "
           "x = 712) and 340 px tall.",
           "3. THE FIST: the big terracotta fist with its four fingers and round rivets (from about x = 520 to x = 742, y = 722 to "
           "y = 922), WITHOUT the sword: remove the sword guard above it and the grip rod and ring pommel below it; where the grip "
           "passed through the fist just close the fingers. Complete the fist's top edge (it was covered by the sword guard) as one "
           "rounded knuckle line.",
           "4. THE UPRIGHT PLATE: the tall terracotta plate with one curved groove at the viewer's right (from about x = 1008 to "
           "x = 1142, y = 598 to y = 872). Complete its left edge and its lower left corner (hidden behind the arm blocks) into one "
           "closed slab with softly rounded corners.",
           "5. THE LONG ROCK SHARD: the long dark lava-rock shard with the orange zigzag crack that points up to the right (its "
           "visible part from about x = 1000 to x = 1215, y = 210 to y = 470). In image 1 its lower end is hidden behind the right "
           "shoulder armour: complete it downward to the left into one closed pointed splinter with a blunt broken base at about "
           "x = 965, y = 525 (the whole shard about 330 px long)."]),
    "B": ("thanh kiếm trọn cây, giáp vai GẦN vẽ đủ, mảnh đá thẳng đứng sau đầu vẽ đủ, viên lõi vàng",
          ["1. THE SWORD, complete, WITHOUT any hand: the black rock blade with its orange lava channel and yellow centre line "
           "(tip at about x = 300, y = 45), the chunky terracotta guard (about x = 425 to x = 648, y = 662 to y = 762), the dark "
           "grip rod and the terracotta ring pommel (centre at about x = 640, y = 963). In image 1 the fist covers the grip and "
           "the lower right corner of the guard: remove the fist and draw the straight dark grip rod (about 34 px thick) running "
           "from the guard down to the pommel along the sword's axis, and complete the guard.",
           "2. THE RIGHT SHOULDER ARMOUR: the big curved armour plate of riveted tiles at the viewer's RIGHT (its visible part "
           "from about x = 893 to x = 1168, y = 362 to y = 642), with its plain thick rim on top. In image 1 its lower left is "
           "covered by the collar arc and its bottom by the arm blocks: complete it into one closed rounded plate (the tile rows "
           "and rivets continue), reaching down to about y = 665 and left to about x = 880.",
           "3. THE UPRIGHT ROCK SHARD behind the head: the dark lava-rock shard with the orange zigzag crack that points straight "
           "up (its visible part from about x = 793 to x = 858, y = 95 to y = 335). In image 1 its lower end is hidden behind the "
           "head: complete it downward into one closed pointed splinter with a blunt broken base at about y = 440 (about 345 px "
           "long, the same width).",
           "4. THE CORE: the round bright-yellow core with its orange ring line (centre at about x = 700, y = 580, about 95 px "
           "across), as a complete circle with its ink outline. No lava around it."]),
    "C": ("quầng dung nham tròn vẽ đủ (không viên lõi), bàn tay xa (lòng + mười đốt ngón rời), mảnh đá hình thoi bên phải, khối cẳng tay sẫm, mảnh đá phía trên bên trái",
          ["1. THE LAVA HEART: the big round ball of flat orange lava with its darker crust patches (centre at about x = 750, "
           "y = 530, about 300 px across). In image 1 most of it is hidden behind the head, the collar arcs and the core: remove "
           "them all (also the yellow core) and draw the WHOLE disc as one complete circle with an ink outline, flat orange, with "
           "six or seven small darker-orange crust patches spread over it.",
           "2. THE LEFT HAND, as separate pieces: (a) the terracotta PALM block (about x = 352 to x = 442, y = 678 to y = 772), "
           "complete, with a closed outline; (b) the TEN small dark finger stones (five fingers of two stones each, about x = 252 "
           "to x = 392, y = 652 to y = 852), each stone complete with its own closed outline and a clear white gap of about 8 px "
           "to its neighbours and to the palm.",
           "3. THE DIAMOND ROCK SHARD at the far right: the dark lava-rock shard with the orange zigzag crack, pointed at both ends "
           "(its visible part from about x = 1118 to x = 1236, y = 405 to y = 738). In image 1 its left side is hidden behind the "
           "right shoulder armour: complete it into one closed diamond-shaped splinter about 150 px wide.",
           "4. THE FOREARM BLOCK: the darker brick-brown clay block of the near forearm (about x = 728 to x = 942, y = 742 to "
           "y = 872). In image 1 its left end is hidden behind the fist and its right end behind the arm blocks: complete it into "
           "one closed chunky block with softly rounded corners, about 240 px wide.",
           "5. THE UPPER LEFT ROCK SHARD: the dark lava-rock shard with the orange zigzag crack that points up to the left (its "
           "visible part from about x = 448 to x = 565, y = 165 to y = 300). In image 1 its lower end is hidden behind the left "
           "shoulder armour: complete it downward to the right into one closed pointed splinter with a blunt broken base at about "
           "x = 600, y = 420 (about 300 px long)."]),
    "D": ("hai vành cổ sẫm vẽ đủ, phiến nhọn TRÊN bên trái vẽ đủ, tấm đá sẫm dưới cẳng tay",
          ["1. THE LEFT COLLAR ARC: the darker brick-brown curved band at the left of the lava heart (about x = 618 to x = 718, "
           "y = 328 to y = 575), like a thick letter C with one carved groove line. Complete both of its ends as rounded ends.",
           "2. THE RIGHT COLLAR ARC: the darker brick-brown curved band that comes down along the right side of the head and "
           "sweeps to the left under it toward the core (about x = 745 to x = 1032, y = 392 to y = 652), with one carved groove "
           "line. In image 1 its upper part is hidden behind the head and the right shoulder armour: complete it into one closed "
           "curved band (like a thick letter J lying on its side) with rounded ends.",
           "3. THE UPPER LEFT FIN: the upper of the two pointed terracotta fins at the far left (its visible part from about "
           "x = 268 to x = 440, y = 415 to y = 530). In image 1 its right part is hidden behind the sword and the lower fin "
           "overlaps its lower edge: complete it into one closed pointed slab (like a broken roof tile, point at the left) "
           "reaching right to about x = 520. Do NOT keep the lower fin.",
           "4. THE DARK UNDER-SLAB of the near forearm: the dark lava-rock slab under the forearm block (its visible part about "
           "x = 728 to x = 938, y = 835 to y = 928). In image 1 its top is hidden behind the forearm block: complete it upward "
           "into one closed chunky slab about 215 px wide and 120 px tall."]),
    "E": ("bốn răng đá dưới ngực vẽ đủ, mảnh đá chếch phải sau đầu vẽ đủ, phiến nhọn DƯỚI bên trái vẽ đủ, khối bắp tay trên",
          ["1. THE FOUR ROCK TEETH under the chest: the four dark lava-rock pieces that hang point-down under the lava heart (at "
           "about x = 615-678, y = 608-692; the big middle one at x = 688-802, y = 618-768; x = 800-842, y = 640-728; and "
           "x = 842-880, y = 628-700). In image 1 their tops are hidden behind the lava heart and the collar arc: complete each "
           "one upward into a closed chunky pointed rock (like a tooth or a spinning top, widest near its top, blunt on top), "
           "each with its own closed outline and a clear white gap of about 12 px between neighbours (shift nothing; make them "
           "slightly slimmer if needed).",
           "2. THE UPPER RIGHT ROCK SHARD: the dark lava-rock shard with the orange zigzag crack that points up to the right "
           "just right of the head (its visible part from about x = 880 to x = 1032, y = 140 to y = 400). In image 1 its lower "
           "end is hidden behind the head and the shoulder armour: complete it downward to the left into one closed pointed "
           "splinter with a blunt broken base at about x = 868, y = 480 (about 370 px long).",
           "3. THE LOWER LEFT FIN: the lower of the two pointed terracotta fins at the far left, with its carved groove (its "
           "visible part from about x = 235 to x = 432, y = 538 to y = 645). In image 1 its right part is hidden behind the sword: "
           "complete it into one closed pointed slab reaching right to about x = 500. Do NOT keep the upper fin.",
           "4. THE UPPER ARM BLOCK: the terracotta block of the near upper arm directly under the right collar arc (about "
           "x = 878 to x = 1012, y = 652 to y = 762). In image 1 its edges are hidden behind the neighbouring blocks: complete it "
           "into one closed chunky block with softly rounded corners, about 150 px wide and 125 px tall; keep it clear of the "
           "rock teeth at its left."]),
    "F": ("khớp vai đá sẫm, khối tay dưới, khối cẳng tay xa sẫm, mảnh đá nhỏ sau giáp vai phải vẽ đủ, và MỘT khối bắp tay xa vẽ thêm ở góc trên trái",
          ["1. THE SHOULDER JOINT: the dark lava-rock piece between the right collar arc and the arm blocks (its visible part "
           "about x = 868 to x = 1012, y = 585 to y = 662). Complete it into one closed rounded boulder about 160 px wide and "
           "115 px tall, with two straight facet lines.",
           "2. THE LOWER ARM BLOCK: the big terracotta block at the bottom right under the upper arm block (about x = 838 to "
           "x = 1092, y = 762 to y = 902). In image 1 its top is hidden behind the upper block and the upright plate, its left "
           "end behind the forearm: complete it into one closed chunky block with softly rounded corners, about 265 px wide and "
           "150 px tall.",
           "3. THE LEFT FOREARM ROCK: the dark lava-rock block between the fins and the left hand (its visible part about "
           "x = 385 to x = 472, y = 622 to y = 702). Complete it into one closed chunky block about 115 px wide and 105 px tall.",
           "4. THE SMALL ROCK SHARD behind the right shoulder armour: the dark lava-rock point that sticks out above the right "
           "shoulder armour (its visible tip at about x = 1078 to x = 1132, y = 392 to y = 445). Complete it downward to the left "
           "into one closed pointed splinter about 190 px long with a blunt base at about x = 1040, y = 560, with one short "
           "orange zigzag crack.",
           "5. ONE EXTRA PIECE that is hidden in image 1: in the EMPTY upper left corner of the canvas (inside x = 60 to x = 250, "
           "y = 60 to y = 250) draw the far UPPER ARM block: one chunky terracotta block with softly rounded corners, about "
           "150 px wide and 160 px tall, with one carved groove line and one round rivet, in exactly the same style and colour "
           "as the other terracotta blocks."]),
}


def build_manh():
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    if not os.path.exists(duyet):
        raise SystemExit("chưa có concept duyệt " + Wp(duyet))
    ra = []
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ (2026-11-14, người dùng chọn hướng A `tuong_binh` → `L1_duyet.png`)", "",
          "Mọi mảnh của rig là mảnh cứng một xương. Mỗi file vẽ lại concept đã duyệt nhưng chỉ giữ vài mảnh không chồng nhau, vẽ đủ phần "
          "khuất, bỏ hết thứ khác (nền trắng). Ảnh mẫu duy nhất của cả sáu file:", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(duyet)}` | Concept đã duyệt (1536 × 1024, nền trắng): " + MO_TA_VI + " |", ""]
    for ma, (vi, giu) in MANH.items():
        out = os.path.join(save_dir(), f"M_{ma}.png")
        p = os.path.join(pk(), f"luot_2_manh_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(duyet)}: the APPROVED picture of the creature, 1536x1024, white background: " + MO_TA_EN,
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "", MANH_CHUNG, "", "KEEP:"] + giu + ["", FLAT, BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd += [f"- **`{ma}`**: {vi}. Chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
    gd += ["", "Kiểm từng ảnh: đúng các mảnh đã kê, nằm trùng chỗ concept (chồng lên concept phải khít), mỗi mảnh viền mực kín, không "
           "chạm nhau, phần khuất đã vẽ đủ, nền trắng tinh, không bóng. Claude cắt bằng `dat_nung_manh.py`."]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in ra:
        print(p)


if __name__ == "__main__":
    if sys.argv[1:2] == ["manh"]:
        build_manh()
    else:
        main()
