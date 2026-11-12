# -*- coding: utf-8 -*-
"""Gói GPT vẽ người cây đầm lầy (mã làm việc nguoi_cay, con gốc của rig: monster_3491). Tướng thứ 7 đảo Mộc.

Người dùng (2026-11-12): "concept là giống với swampthing của DC, một humanoid bọc trong các lớp thực vật"; "trước khi bắt đầu tách
lớp rig xương cho tôi xem concept đã". Không dặn màu, kiểu đầu: hai hướng dưới đây là ĐỀ XUẤT của Claude, chờ người dùng chọn.
Hình là của mình (không chép nhân vật truyện tranh đó, không đính ảnh của nó, không đính ảnh con gốc): dáng người đấm bốc của rig,
đầu vẽ mới, thân bọc bởi các LỚP thực vật tách rời (rêu, lá to, rễ bện, dây gai). Bố cục đưa bằng sơ đồ tự dựng (nguoi_cay.py bo_cuc).

    py -3 -I ArtGen/Spine/nguoi_cay.py bo_cuc
    py -3 -I ArtGen/Spine/build_nguoi_cay.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/nguoi_cay_1/luot_1_concept_<hướng>.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "nguoi_cay"
K = 2                        # gói concept và mảnh của DẠNG LỚN (thư mục nguoi_cay_2); dạng non: main_non, main_manh_non
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
DEER = os.path.join(HERE, "inbox", "huou_go_2", "tai_ve", "L1_duyet.png")
STONE = os.path.join(HERE, "inbox", "tuong_da_1", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def pk(k=K):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def mau_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "mau")


MAU = {
    "dam_lay": dict(
        ten="A · người rêu đầm lầy: mũ trùm rêu, hốc mặt tối hai mắt vàng, chồi dương xỉ cuộn, nấm trên vai",
        reu="olive moss green (#6F9440)", reu_ru="pale grey-green (#A0BA6E)", la="deep teal green (#2F7558)",
        la_nhat="fresh yellow-green (#9CC456)", gan="dark green (#1C4A34)", re="root brown (#8B6238)", re_dam="dark brown (#5E4226)",
        go="light root-wood brown (#AA7C4A)", day="dark vine green (#3E6B3A)", gai="cream (#EFE0A8)",
        cam="NO blue, NO purple, NO pink, NO red eyes"),
    "mat_go": dict(
        ten="B · người rễ mặt gỗ: mặt nạ gỗ nhạt có gờ mày, mũ ba chiếc lá to, hoa kế tím trên vai",
        reu="leaf green (#5C9646)", reu_ru="light yellow-green (#A8CC60)", la="forest green (#3E8448)",
        la_nhat="light yellow-green (#A8CC60)", gan="dark green (#1C4A34)", re="root brown (#966E46)", re_dam="dark brown (#644628)",
        go="pale wood (#D6BE96)", day="dark vine green (#466E3C)", gai="cream (#EFE0A8)",
        cam="NO blue, NO pink, NO red; purple ONLY on the two thistle flowers"),
}


def head(kieu, M):
    if kieu == "dam_lay":
        return [
            "- HEAD (about x = 610 to x = 915, y = 245 to y = 505; big and round, sitting directly on the shoulders, no neck): a "
            f"rounded HOOD OF MOSS of {M['reu']}, like a soft thick helmet, its surface slightly bumpy at the outline, its lower "
            "edge a row of soft scallops that hangs over the collar. In its front, turned three-quarters to the right, is the "
            "FACE OPENING (about x = 714 to x = 898, y = 326 to y = 470): a smooth oval of flat dark brown (#3B2F27), as if looking "
            "into the dark inside of the hood. In that dark there are ONLY TWO EYES and nothing else: two big, slanted, angular "
            "eyes of flat warm yellow (#F6D93E) with no pupils, the near one at about (772, 398), about 48 px wide, the far one at "
            "about (852, 400), about 40 px wide; their inner corners are lower than their outer corners (a stern, determined "
            "glare). Each eye has one tiny white dot. No nose, no mouth, no teeth, no eyebrows, no skull, no human features.",
            f"- HANGING MOSS: from under the BACK of the hood (the left side), three thick ropes of hanging moss of {M['reu_ru']} "
            "droop down behind the near shoulder like short dreadlocks (from about y = 420 down to about y = 610, each about "
            "28 px thick, slightly wavy, with a rounded tip and two or three short pencil lines along it).",
            "- SPROUT (this is the creature's signature silhouette): from the top of the hood, at about (742, 262), grows ONE "
            f"young FERN FIDDLEHEAD of {M['la_nhat']}: a smooth stem about 20 px thick that rises to about y = 190 and curls "
            "over to the LEFT into a tight spiral (the spiral about 95 px across, its top at about y = 122), with two small "
            "pointed leaves at its base (each about 70 px long, one centre vein).",
        ]
    return [
        "- HEAD (about x = 566 to x = 906, y = 190 to y = 505; big, sitting directly on the shoulders, no neck): the face is a "
        f"smooth carved WOODEN MASK of {M['go']}, an upright oval turned three-quarters to the right (about x = 696 to x = 904, "
        "y = 306 to y = 502), with two or three thin wood-grain pencil lines. On it: a heavy V-shaped BROW of bark of "
        f"{M['re']} (a thick band about 22 px, its point low between the eyes, at about (814, 398)); under it TWO big slanted "
        "angular eyes of flat amber (#F0AA32) with a small round dark pupil and one tiny white dot each, the near one at about "
        "(778, 410), the far one at about (858, 410) (a stern, determined glare); and a short, firm, closed MOUTH LINE at about "
        "(820, 460), about 60 px long, slightly frowning. No nose, no teeth, no ears, no human skin.",
        "- LEAF HOOD (this is the creature's signature silhouette): THREE VERY BIG LEAVES cover the top and the back of the head "
        "like swept-back hair. All three are rooted close together above the forehead (at about (850, 310)) and sweep BACK to "
        "the left, overlapping like roof tiles: the top one points up and back, its tip at about (600, 232); the middle one "
        "points straight back, its tip at about (566, 372); the lowest one hangs down behind the near shoulder, its tip at "
        f"about (590, 498). Each is a broad pointed leaf about 290 px long and 150 px wide with ONE centre vein of {M['gan']}; "
        f"the top and the lowest are {M['la']}, the middle one is {M['reu']}. One small young leaf of {M['la_nhat']} (about "
        "75 px) sticks up and forward from the same root, its tip at about (905, 236).",
    ]


def shoulder_extra(kieu, M):
    if kieu == "dam_lay":
        return ("On top of the NEAR mound stand THREE small MUSHROOMS in a little group (about x = 448 to x = 582, y = 406 to "
                "y = 492): short cream stems (#EFE3C4) and rounded caps of flat orange-red (#E0603A) with three cream dots each; "
                "the middle one is the biggest (cap about 68 px wide), the other two about 50 px. On the FAR mound lies one "
                f"single pointed leaf of {M['la']} (about 115 px long), its tip pointing up and to the right.")
    return ("On top of the NEAR mound grow TWO THISTLE FLOWERS (about x = 462 to x = 572, y = 412 to y = 505): short thick green "
            "stems and round, slightly spiky pom-pom heads of flat purple (#AA60B8) on a small green cup; the right one is the "
            "bigger (head about 60 px), the left one about 48 px. On the FAR mound lies one single pointed leaf of "
            f"{M['la_nhat']} (about 115 px long), its tip pointing up and to the right.")


def body(kieu):
    M = MAU[kieu]
    return "\n".join([
        "CREATURE: a SWAMP-FOREST PLANT BRAWLER, a plant-element monster for a monster-collecting game: a stocky, broad-"
        "shouldered humanoid figure whose whole body is WRAPPED IN LAYERS OF PLANTS: moss, big leaves, woven roots and thorny "
        "vines. It is a plant creature through and through: no skin, no hair, no cloth, no armour, no metal. It stands in a "
        "boxer's guard, one big fist raised, the other hanging low and ready. Character: the silent, tough bruiser of the "
        "forest, battle-ready, glaring at an enemy to the right; chunky and appealing with a big head and big fists, not "
        "scary, not horror, not a smiling cute mascot. Bold, clear, readable shapes; few details.",
        "Follow the LAYOUT GUIDE (image 1) for WHERE every part is on the canvas, HOW BIG it is and WHICH part overlaps which. "
        "The shapes in the guide are only rough computer blobs: design the real outline of every part yourself as described "
        "below, but keep every part in its place and at its size, and keep the pose exactly.",
        "- VIEW AND POSE: the figure faces the viewer's RIGHT, seen in three-quarter view, standing in a wide, low fighting "
        "stance with both knees bent and both feet flat on the ground (no ground line drawn). Its NEAR arm is at the viewer's "
        "LEFT: the elbow sticks out to the left and the forearm hangs straight down, the big fist low at hip height. Its FAR "
        "arm is at the viewer's RIGHT, behind the body: the upper arm goes out to the right, the forearm is bent UP, the fist "
        "raised to chin height. The torso leans slightly forward.",
        *head(kieu, M),
        f"- SHOULDER MOUNDS: each shoulder is covered by a big, soft, rounded MOUND OF MOSS of {M['reu']} like a shoulder pad "
        "(the NEAR one about x = 410 to x = 646, y = 460 to y = 585, in front of the body; the FAR one about x = 822 to "
        "x = 1028, y = 462 to y = 578, behind the head), each with a softly scalloped lower edge and a few short pencil tufts. "
        + shoulder_extra(kieu, M),
        "- ARMS: thick and strong, built of WOVEN ROOTS. Each UPPER ARM (near: about x = 434 to x = 640, y = 489 to y = 646; "
        f"far: about x = 814 to x = 1043, y = 497 to y = 665) is a bundle of three or four fat twisted roots of {M['re']}, "
        f"drawn as one chunky shape with two or three thin dark pencil lines ({M['re_dam']}) running along it. Each FOREARM "
        "(near: about x = 394 to x = 532, y = 527 to y = 715; far: about x = 959 to x = 1106, y = 478 to y = 660) is the same "
        f"root bundle wound round and round by ONE THORNY VINE of {M['day']}: four or five diagonal turns of a vine about "
        f"16 px thick, with six to eight short, chunky, cone-shaped THORNS of {M['gai']} (each about 18 px) sticking out along "
        "the outline of the forearm.",
        f"- FISTS: two very BIG FISTS of knotted root-wood of {M['go']} (near fist about x = 351 to x = 521, y = 670 to y = 849; "
        "far fist about x = 1006 to x = 1178, y = 363 to y = 533; each clearly bigger than the forearm it sits on): a clenched "
        "fist with four chunky knuckles and a thumb folded across, drawn with a few simple ink lines, like a gnarled wooden "
        "knot. No claws, no fingers spread.",
        f"- TORSO (about x = 601 to x = 880, y = 443 to y = 738): a broad barrel chest. Its BELLY (the lower part, below about "
        f"y = 630) is woven roots of {M['re']} with two horizontal root bands drawn as thin dark pencil lines. Its CHEST is "
        f"covered by a COLLAR OF FOUR BIG LEAVES of {M['la']} hanging from under the head and pointing DOWN, overlapping like "
        "roof tiles (the two middle ones about 165 px long and 95 px wide, reaching down to about y = 635; the two outer ones "
        f"about 135 px long); each is a simple broad pointed leaf with ONE centre vein of {M['gan']}.",
        f"- BELT AND LEAF SKIRT: around the waist (about y = 694) a thick VINE BELT of {M['day']} (about 24 px). From it hangs a "
        "SKIRT OF FIVE LONG LEAVES (about x = 560 to x = 922, y = 698 to y = 902), overlapping, their pointed tips down, the "
        f"middle ones the longest (about 190 px long, 88 px wide): they alternate {M['la']} and {M['reu']}, each with one "
        f"centre vein of {M['gan']}. Between the two legs the skirt hangs free.",
        "- LEGS: short, thick, bent. Each THIGH (near: about x = 584 to x = 766, y = 704 to y = 894; far: about x = 716 to "
        f"x = 950, y = 701 to y = 893) is covered in moss of {M['reu']} and mostly hidden under the leaf skirt. Each SHIN (near: "
        "about x = 543 to x = 695, y = 795 to y = 935; far: about x = 854 to x = 954, y = 813 to y = 937) is a root bundle of "
        f"{M['re']} with ONE ring of vine of {M['day']} around the ankle. Each FOOT (near: about x = 527 to x = 621; far: about "
        f"x = 889 to x = 985; both at y = 899 to y = 955) is a short stump of root-wood of {M['go']} with three blunt root "
        "toes pointing right.",
        "- Exactly: one head, two eyes, two shoulder mounds, two arms each with one thorny vine and one big fist, one leaf "
        "collar of four leaves, one vine belt, one leaf skirt of five leaves, two legs, two feet.",
        "",
        "COLOURS, a calm, slightly muted palette (use exactly the colours named above, each area one flat colour); every "
        f"outline dark-brown ink (#2B2118). Only these colours. {M['cam']}.",
    ])


FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the whole figure is about 820 px wide (from the near fist at about x = 351 "
         "to the far fist at about x = 1178) and stands with its feet at about y = 955; the top of its head decoration is at "
         "about y = 120 to y = 190.")

POSE = ("ANIMATION-READY (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): keep "
        "the clean readable pose of the guide. The plant layers are SEPARATE, clearly outlined shapes lying on top of one "
        "another: the head, each shoulder mound, each collar leaf, each skirt leaf, each upper arm, each forearm, each fist, "
        "each thigh, each shin, each foot. The raised far fist does not touch or cover the head; the near arm does not cover "
        "the chest; the two legs do not cross. No falling leaves, no dust, no sparkles, no glow, no motion lines, no ground, "
        "no props, no weapon.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram with rough edges: take only the pose, the placement, the sizes, the overlaps "
        "and the colour of each kind of part from it, never its line, its edge noise or its exact blobs. Draw the leaves as "
        "simple bold leaf shapes, the moss as soft rounded cushions, the roots as smooth chunky twisted wood.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 6 px thick on this canvas around every big part (head, shoulder "
        "mounds, torso, arms, fists, collar leaves, skirt leaves, legs), and about 4 px for small parts (eyes, thorns, vine "
        "turns, toes, the small head and shoulder decorations); leaf veins, root lines and moss tufts are thin darker pencil "
        "lines about 3 px, not ink; every area coloured with coloured pencils and wax crayons, the strokes visible as loose "
        "diagonal hatching (strokes thinner than the outline), kept inside the outline. Clean and appealing, neither a crude "
        "scribble nor overly detailed: no realistic bark cracks, no tangled thin vines all over, no tiny leaves everywhere, "
        "no dripping slime.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker underside, no lighter patches or blotches, no shadows of any kind (no cast "
        "shadow of one part on another, no shadow under the figure or on the background), no white highlights or shine spots "
        "(except the one tiny dot in each eye), no gloss, no glow, no rim light, no gradients, no 3D look. The eyes do NOT "
        "glow. A different tone appears only where the design itself lists a different colour.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the creature.")


def refs(kieu):
    dau = ("the round green dome with a dark oval and two yellow eyes = the moss hood and the face; the pale hanging strips = the "
           "hanging moss; the green curl on top = the fern sprout; the small red caps = the mushrooms" if kieu == "dam_lay" else
           "the pale oval with a brown V and two orange eyes = the wooden mask face; the three big green leaf shapes = the leaf "
           "hood; the two purple balls = the thistle flowers")
    dau_vi = ("vòm lục có bầu dục tối và hai mắt vàng: mũ trùm rêu + hốc mặt; các dải nhạt rủ: rêu rủ; vòng xoắn trên đỉnh: chồi dương "
              "xỉ; ba mũ đỏ nhỏ trên vai trái: nấm" if kieu == "dam_lay" else
              "bầu dục nhạt có chữ V nâu và hai mắt cam: mặt nạ gỗ; ba hình lá to: mũ lá; hai quả cầu tím trên vai trái: hoa kế")
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature showing the pose and where "
         "every part goes on the canvas, how big it is and which part overlaps which (a stocky figure in a boxer's stance "
         f"facing right; {dau}; the two green cushions = the moss shoulder mounds; brown limbs with green stripes = the root "
         "arms and the thorny vine wound round the forearms; the two big light-brown blobs = the fists; the pointed leaf shapes "
         "on the chest = the leaf collar; the green band = the vine belt; the pointed leaf shapes below it = the leaf skirt; "
         "brown and green shapes at the bottom = the legs and feet). Use it for pose, placement, size and overlap only; redraw "
         "everything in the hand-drawn style of the approved heroes.",
         f"Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): hình người lùn mập thế thủ đấm bốc nhìn sang phải, tô phẳng theo "
         f"nhóm màu ({dau_vi}; hai gối lục trên vai: u rêu; tay nâu sọc lục: tay rễ quấn dây gai; hai khối nâu nhạt to: nắm tay; lá "
         "trên ngực: cổ áo lá; dải lục ngang hông: đai dây leo; lá rủ bên dưới: váy lá; nâu và lục phía dưới: chân, bàn chân). Chỉ lấy "
         "dáng, chỗ đặt, cỡ, thứ tự chồng"),
        (DEER,
         "an approved hero of the same game and the same island (a wooden stag-giraffe with a leaf mane), 1536x1024, white "
         "background: match EXACTLY its wobbly dark-brown pen line, its visible crayon hatching, its completely flat colouring "
         "and its bold level of detail; see how its LEAVES (shape, one centre vein), its wood and its moss are drawn. Do NOT "
         "copy its species, its design or its colours.",
         "Hươu gỗ cổ dài đã duyệt (1536 × 1024, nền trắng): thân gỗ bạch dương đốm nâu, bờm lá phong đỏ cam, pha lê lục trên lưng. "
         "Lấy nét bút rung, vân sáp, tô phẳng, cách vẽ lá, gỗ, rêu"),
        (STONE,
         "another approved hero of the same island (a floating stone guardian with moss and wooden antlers), 1536x1024, white "
         "background: the same line and flat crayon colouring; see how its MOSS cushions, its roots and its big chunky fists "
         "are drawn. Do NOT copy its design or its colours.",
         "Tượng đá giữ rừng đã duyệt (1536 × 1024, nền trắng): các khối đá lơ lửng phủ rêu, hai nắm tay đá to quấn rễ. Lấy nét, tô "
         "phẳng, cách vẽ rêu, rễ, nắm tay to"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching) and the way its trees, leaves and moss are simplified, nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp, cách giản lược cây, lá"),
    ]


CHECK = [
    "Hình người lùn mập **thế thủ đấm bốc nhìn sang phải**: tay gần (bên trái hình) buông thấp, tay xa (bên phải) nắm đấm giơ ngang cằm; "
    "hai chân choãi, không bắt chéo.",
    "**Cả thân bọc bằng các lớp thực vật tách rời**: u rêu hai vai, cổ áo bốn lá to, đai dây leo, váy năm lá dài, tay rễ bện, cẳng tay "
    "quấn dây gai có gai kem, hai nắm tay gỗ rễ rất to. Không da người, không vải, không giáp.",
    "Hướng A: mũ trùm rêu tròn, **hốc mặt tối chỉ có hai mắt vàng xếch** (không mũi, không miệng), ba dải rêu rủ sau gáy, **một chồi dương "
    "xỉ cuộn** trên đỉnh đầu, ba cây nấm cam đỏ trên vai gần.",
    "Hướng B: **mặt nạ gỗ nhạt** có gờ mày chữ V, hai mắt hổ phách, khe miệng mím; **ba chiếc lá rất to** quét ra sau làm mũ; hai bông hoa "
    "kế tím trên vai gần.",
    "Mặt quả quyết, không cười, không kinh dị; nét bút mực nâu rung, vân sáp, hình khối to rõ ít chi tiết.",
    "Tô phẳng: **không** bóng, không mảng sáng tối, mắt không phát sáng, không điểm sáng trắng (trừ một chấm trong mỗi mắt); nền trắng "
    "tinh; không lá rơi; cả con không bị cắt mép.",
]

FIX = [
    ("Ra kiểu quái vật kinh dị, quá nhiều chi tiết", "Simplify: chunky, appealing monster-collecting-game creature with a big head and "
                                                    "big fists; bold simple leaves and moss cushions; remove tangled thin vines, "
                                                    "bark cracks, slime and tiny leaves."),
    ("Có mũi, miệng, răng trong hốc mặt (hướng A)", "The face opening is a flat dark oval with ONLY the two yellow eyes; remove the "
                                                   "nose, mouth and teeth."),
    ("Mắt đỏ / mắt phát sáng", "The eyes are flat warm yellow with no glow; no red."),
    ("Có bóng, mảng sáng tối, phát sáng", "Flat colour only: remove every shadow, highlight, gradient and glow; each area one even "
                                          "colour; keep the crayon hatching as texture only."),
    ("Dáng khác sơ đồ / quay mặt sang trái", "Follow image 1 exactly for the pose and the place and size of every part; the figure "
                                            "faces the viewer's right."),
    ("Tay che ngực, nắm tay che đầu", "Keep the limbs apart as in image 1: the raised far fist stays clear of the head, the near arm "
                                      "hangs clear of the chest."),
    ("Các lớp lá dính thành một mảng", "Each collar leaf and each skirt leaf is its own clearly outlined leaf shape, overlapping like "
                                       "roof tiles."),
]


def main():
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    gd = [f"# Gói gửi GPT: `{CODE}` (người cây đầm lầy, tướng thứ 7 đảo Mộc, tên chưa đặt)", "",
          "Làm 2026-11-12: dựng trên rig của con gốc `monster_3491` (dáng người đấm bốc); màu, kiểu đầu và chi tiết là đề xuất của "
          "Claude, chờ người dùng chọn hướng và duyệt concept. Ghi chú: `ArtGen/Spine/inbox/nguoi_cay_ghichu.md`.", "",
          "Lượt 2 (mảnh) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    ra = []
    for kieu, M in MAU.items():
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
              "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready pose, in the hand-drawn style of the "
              "approved hero images.", "", body(kieu), "", FRAME, "", POSE, "", SOFT, LINE, FLAT, BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd += [f"## Hướng `{kieu}`: {M['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{K}/luot_1_concept_{kieu}.txt` (thêm "
               "`--note \"...\"` để sửa nhanh).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += [""]
    gd += ["Không đính ảnh con gốc của game tham khảo, không đính ảnh nhân vật truyện tranh người dùng gửi làm gợi ý; bố cục đưa bằng sơ "
           "đồ tự dựng (`py -3 -I ArtGen/Spine/nguoi_cay.py bo_cuc`).", "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    open(os.path.join(pk(), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ================================================================ BẢN 2 (2026-11-12): người dùng trả bản 1
# "tôi thấy chưa đủ chiến, đầu nhìn xấu quá, làm sát với swampthing hơn 1 chút" → dáng quái đầm lầy nặng đô: vai u khổng lồ, đầu nhỏ
# thụt giữa hai vai, thân rêu lục gần kín, mặt có gờ mày + hàm bạnh, cành khô trên vai, rêu rủ dưới tay. Vẫn là hình của mình: không
# sống mũi rễ, không mắt đỏ, không đính ảnh nhân vật đó. Hai kiểu đầu: gam (mím miệng), nanh (nhe răng gỗ, râu rêu).
C2 = dict(than="dark moss green (#4E7A3E)", reu="lighter moss green (#7CA44A)", la="very dark leaf green (#2C6042)",
          la_nhat="light leaf green (#92BA5C)", gan="near-black green (#173D2B)", canh="dead-wood brown (#7A5A3A)",
          go="root-wood brown (#987248)", go_dam="dark brown (#5E4226)", day="dark vine green (#2F5233)", gai="cream (#EFE0A8)",
          hoc="very dark green-black (#283224)", mat="fiery orange (#EE6C2C)", rang="cream (#EFE3C4)")
MAU2 = {
    "gam": "C · quái rêu mím miệng: gờ mày nặng, hốc mắt tối, mắt cam, hàm rễ bạnh mím chặt, mào lá răng cưa",
    "nanh": "D · quái rêu nhe nanh: như C nhưng há miệng gầm lộ hàm răng gỗ + hai nanh dưới, có chòm râu rêu rủ dưới cằm",
}


def head2(kieu):
    M = C2
    chung = [
        "- HEAD (about x = 700 to x = 900, y = 330 to y = 520: SMALL, only about 200 px wide, sunk LOW between the two huge "
        "shoulder humps and pushed forward; no neck; the tops of the shoulder humps are almost as high as the top of the "
        f"head): a craggy, blunt head of bark overgrown with moss of {M['than']}, shaped like a rough helmet with a flat, "
        "sloping top and hard angular planes (not a round ball). Turned three-quarters to the right.",
        f"- BROW AND EYES: a HEAVY OVERHANGING BROW RIDGE of {M['la']} runs right across the face: one thick, angular, "
        "V-shaped band about 26 px thick, from about (700, 396) down to its point at about (808, 420) and up again to about "
        f"(898, 390). Directly under it lies a band of {M['hoc']}, the deep eye sockets, and in that dark band sit TWO small, "
        f"narrow, slanted eyes of flat {M['mat']}, with NO pupils: the near one at about (765, 427), about 46 px wide, the far "
        "one at about (851, 425), about 42 px wide; their inner corners are much lower than their outer corners (a furious "
        "glare). One tiny white dot in each eye. The eyes are flat colour, they do not glow.",
    ]
    if kieu == "gam":
        mieng = ("- JAW AND MOUTH: below the eyes the face is a broad, HEAVY, SQUARE JAW built of five or six thick vertical root "
                 f"cords of {M['than']} running down over the cheeks and the chin (drawn with thin dark pencil lines between "
                 "them), jutting forward like an underbite. Across it a wide, grim, tightly CLOSED mouth: one firm downturned "
                 "ink line about 90 px long at about y = 480, its corners pulled down. No nose, no nostrils, no ears, no teeth "
                 "showing.")
    else:
        mieng = ("- JAW AND MOUTH: below the eyes the face is a broad, HEAVY, SQUARE JAW built of thick vertical root cords of "
                 f"{M['than']}, jutting forward. The mouth is OPEN IN A SNARL (about x = 762 to x = 862, y = 462 to y = 502): a "
                 f"flat opening of {M['hoc']} with its corners pulled down, showing a row of five chunky, blunt, slightly uneven "
                 f"WOODEN TEETH of {M['rang']} along the lower jaw, the two at the corners bigger and pointed like short tusks "
                 "sticking up. Under the chin hangs a short ragged BEARD of three or four ropes of hanging moss of "
                 f"{M['reu']} (down to about y = 585, each about 20 px thick, uneven lengths). No nose, no nostrils, no ears, no "
                 "tongue.")
    mao = ("- CREST: from the top and the back of the head three or four ragged, saw-toothed LEAVES of "
           f"{M['la']} sweep back and up to the left like a short rough mane (tips at about (640, 330), (668, 268) and "
           f"(752, 246); each about 120 px long and 50 px wide, with one centre vein of {M['gan']} and a serrated edge).")
    return chung + [mieng, mao]


def body2(kieu):
    M = C2
    return "\n".join([
        "CREATURE: a hulking SWAMP PLANT BRUTE, a plant-element monster for a monster-collecting game: a massive, hunched, "
        "humanoid creature made ENTIRELY OF SWAMP PLANTS. Its body is a mass of tightly bundled vines and roots overgrown with "
        "dark moss, and over that lie LAYERS of ragged leaves, cushions of moss, ropes of hanging moss and thorny vines. No "
        "skin, no hair, no cloth, no armour, no metal, no bones. Character: a silent, furious force of the swamp, battle-"
        "ready and intimidating, glaring at an enemy to the right. It must look STRONG AND FIERCE, a boss-like heavyweight: "
        "NOT cute, NOT chibi, NOT a round-headed mascot, no smile. Still drawn with bold, clear, readable shapes in the "
        "game's simple hand-drawn style (not realistic, not horror gore, no slime).",
        "PROPORTIONS (very important): top-heavy like a gorilla or a heavyweight wrestler. ENORMOUS rounded shoulders and very "
        "thick arms with huge fists; a broad barrel chest; a SMALL head sunk low between the shoulders; short, thick, bent "
        "legs. The two shoulder humps together are about four times as wide as the head.",
        "Follow the LAYOUT GUIDE (image 1) for the pose and for WHERE every part is on the canvas, HOW BIG it is and WHICH part "
        "overlaps which. The shapes in the guide are only rough computer blobs: design the real outline of every part "
        "yourself as described below (ragged, organic, plant-like), but keep every part in its place and at its size.",
        "- VIEW AND POSE: the figure faces the viewer's RIGHT, seen in three-quarter view, hunched forward in a wide, low "
        "fighting stance, both knees bent, both feet flat (no ground line drawn). Its NEAR arm is at the viewer's LEFT: the "
        "elbow sticks out to the left and the forearm hangs straight down, the huge fist low at hip height. Its FAR arm is at "
        "the viewer's RIGHT, behind the body: the upper arm goes out to the right, the forearm is bent UP, the fist raised "
        "to head height, ready to punch.",
        *head2(kieu),
        f"- SHOULDER HUMPS: each shoulder is a HUGE rounded hump of thick moss of {M['reu']} (the NEAR one about x = 380 to "
        "x = 664, y = 406 to y = 578, in front of the body; the FAR one about x = 828 to x = 1068, y = 420 to y = 570, behind "
        "the head), with a bumpy, tufted outline and a ragged lower edge, a few short pencil tufts on it. From the near hump "
        f"stick up TWO bare, broken, forked DEAD TWIGS of {M['canh']} (the bigger one from about (470, 430) up to about "
        "(432, 322) with one side fork; the smaller one from about (566, 425) up to about (584, 348)); from the far hump ONE "
        "forked dead twig (from about (938, 436) up to about (920, 338)). Each twig about 15 px thick, blunt broken ends, no "
        f"leaves on them. On each hump lies one ragged saw-toothed leaf of {M['la']} (about 95 px).",
        "- UPPER ARMS (near: about x = 434 to x = 640, y = 489 to y = 646; far: about x = 814 to x = 1043, y = 497 to y = 665): "
        f"very thick, bulging bundles of twisted vines of {M['than']}, each drawn as one chunky muscle shape with two or three "
        "thin dark pencil lines running along it. Under each upper arm hang THREE ROPES OF HANGING MOSS of "
        f"{M['reu']} (near: about x = 530 to x = 615, y = 624 to y = 712; far: about x = 870 to x = 955, y = 640 to y = 724; "
        "each about 22 px thick, uneven lengths, rounded tips).",
        "- FOREARMS (near: about x = 394 to x = 532, y = 527 to y = 715; far: about x = 959 to x = 1106, y = 478 to y = 660): "
        f"thick gnarled root-wood of {M['go']} with two or three grain lines of {M['go_dam']}, wound round and round by ONE "
        f"THORNY VINE of {M['day']} (four or five diagonal turns, about 16 px thick) with six to eight short, chunky, cone-"
        f"shaped THORNS of {M['gai']} (each about 20 px) sticking out along the outline of the forearm.",
        f"- FISTS: two HUGE clenched FISTS of knotted root-wood of {M['go']} (near fist about x = 349 to x = 523, y = 668 to "
        "y = 851; far fist about x = 1004 to x = 1180, y = 361 to y = 535; each clearly bigger than the head's face): four "
        "chunky knuckles and a thumb folded across, drawn with a few simple ink lines, like a gnarled wooden knot; two small "
        f"thorns of {M['gai']} on the knuckles of each fist. No claws, no open fingers.",
        "- TORSO (about x = 601 to x = 880, y = 443 to y = 738): a broad barrel chest and belly of bundled vines of "
        f"{M['than']}, with a few thin dark pencil lines following the vine bundles (chest muscles and belly bands suggested "
        f"simply). ONE thick vine of {M['day']} (about 20 px) crosses the belly diagonally, from under the near arm at about "
        "(600, 560) down to the far hip at about (880, 690). Over the upper chest hangs a ragged COLLAR OF FIVE SAW-TOOTHED "
        "LEAVES pointing down, overlapping like roof tiles (about x = 600 to x = 900, y = 480 to y = 640; the middle one the "
        f"longest, about 155 px; widths about 60-75 px): they alternate {M['la']} and {M['la_nhat']}, each with ONE centre "
        f"vein of {M['gan']} and a serrated edge.",
        f"- BELT AND LEAF SKIRT: around the waist (about y = 694) a thick VINE BELT of {M['day']} (about 24 px). From it hangs a "
        "ragged SKIRT OF SIX NARROW LEAVES of uneven lengths (about x = 560 to x = 925, y = 698 to y = 906; about 60-66 px "
        "wide; the longest about 200 px, the shortest about 135 px), overlapping, pointed tips down: they alternate "
        f"{M['la']} and {M['la_nhat']}, each with one centre vein of {M['gan']} and a serrated edge.",
        "- LEGS: short, thick, bent. Each THIGH (near: about x = 584 to x = 766, y = 704 to y = 894; far: about x = 716 to "
        f"x = 950, y = 701 to y = 893) is bundled vines of {M['than']}, mostly hidden under the leaf skirt. Each SHIN (near: "
        "about x = 543 to x = 695, y = 795 to y = 935; far: about x = 854 to x = 954, y = 813 to y = 937) is gnarled root-wood "
        f"of {M['go']} with ONE ring of vine of {M['day']} around the ankle. Each FOOT (near: about x = 525 to x = 623; far: "
        f"about x = 887 to x = 987; both at y = 897 to y = 955) is a broad stump of root-wood of {M['go']} with three blunt "
        "root toes pointing right.",
        "- Exactly: one small head with two eyes, two huge shoulder humps with three dead twigs in all, two arms each with "
        "three ropes of hanging moss, one thorny vine and one huge fist, one leaf collar of five leaves, one diagonal vine, one "
        "vine belt, one leaf skirt of six leaves, two legs, two feet.",
        "",
        "COLOURS, a dark, earthy swamp palette, almost everything green (use exactly the colours named above, each area one "
        "flat colour); every outline dark-brown ink (#2B2118). Only these colours. NO blue, NO purple, NO pink, NO red, NO "
        "flowers, NO mushrooms.",
    ])


FRAME2 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
          "nothing cut by the edges. As in the guide, the whole figure is about 830 px wide (from the near fist at about x = 349 "
          "to the far fist at about x = 1180) and stands with its feet at about y = 955; the top of the head crest is at about "
          "y = 246 and the highest twig tip at about y = 322.")

POSE2 = ("ANIMATION-READY (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): keep "
         "the clean readable pose of the guide. The plant layers are SEPARATE, clearly outlined shapes lying on top of one "
         "another: the head, each crest leaf, each shoulder hump, each twig, each rope of hanging moss, each collar leaf, each "
         "skirt leaf, each upper arm, each forearm, each fist, each thigh, each shin, each foot. The raised far fist does not "
         "touch or cover the head; the near arm does not cover the chest; the two legs do not cross. No falling leaves, no "
         "dust, no drips, no sparkles, no glow, no motion lines, no ground, no props, no weapon.")

LINE2 = LINE.replace("(head, shoulder mounds, torso, arms, fists, collar leaves, skirt leaves, legs)",
                     "(head, shoulder humps, torso, arms, fists, collar leaves, skirt leaves, legs)").replace(
    "(eyes, thorns, vine turns, toes, the small head and shoulder decorations)",
    "(eyes, teeth, thorns, vine turns, toes, twigs, ropes of hanging moss, crest leaves)")

CHECK2 = [
    "**Dáng quái nặng đô, không chibi**: hai u vai khổng lồ, tay rất to, **đầu nhỏ thụt giữa hai vai**, ngực thùng, chân ngắn choãi; thế "
    "thủ đấm bốc nhìn sang phải (tay gần buông thấp, tay xa nắm đấm giơ ngang đầu).",
    "Mặt dữ: **gờ mày chữ V nặng**, dải hốc mắt tối, hai mắt cam hẹp xếch không con ngươi, hàm rễ bạnh; không mũi. Kiểu C mím miệng trễ "
    "xuống; kiểu D há miệng nhe hàm răng gỗ + hai nanh dưới, có chòm râu rêu.",
    "Thân **gần như toàn lục**: bó dây leo phủ rêu sẫm; u rêu vai nhạt hơn có **ba cành khô gãy**; **rêu rủ** ba dải dưới mỗi bắp tay; "
    "cổ áo năm lá răng cưa; một dây leo vắt chéo bụng; đai + váy sáu lá hẹp so le.",
    "Cẳng tay, ống chân, bàn chân là gỗ rễ nâu; cẳng tay quấn dây gai có gai kem; hai nắm tay gỗ rất to.",
    "Nét bút mực nâu rung, vân sáp, hình khối to rõ; không tả thực, không kinh dị, không nhớt.",
    "Tô phẳng: **không** bóng, không mảng sáng tối, mắt không phát sáng; nền trắng tinh; cả con không bị cắt mép.",
]
FIX2 = [
    ("Vẫn ra kiểu dễ thương, đầu to tròn", "NOT cute and NOT chibi: make the head small and angular, sunk low between two enormous "
                                         "shoulder humps; heavier brow, narrower furious eyes; much bigger shoulders and arms."),
    ("Ra kiểu tả thực / kinh dị", "Keep the simple hand-drawn game style of images 2 and 3: bold flat shapes, no realistic "
                                  "anatomy, no slime, no gore, no tangled thin vines."),
    ("Có mũi / sống mũi rễ", "No nose at all: under the brow there is only the dark eye band, then the jaw."),
    ("Mắt đỏ / phát sáng", "The eyes are flat fiery orange (#EE6C2C), no glow, no red."),
    ("Có bóng, mảng sáng tối", "Flat colour only: remove every shadow, highlight, gradient and glow."),
    ("Dáng khác sơ đồ", "Follow image 1 exactly for the pose and the place and size of every part; the figure faces the viewer's right."),
]


def refs2():
    R = refs("dam_lay")
    R[0] = (os.path.join(mau_dir(), "bo_cuc_chien.png"),
            "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature showing the pose and where "
            "every part goes on the canvas, how big it is and which part overlaps which (a hulking figure in a boxer's stance "
            "facing right; the small angular green head with a dark brow band and two orange eyes, three dark leaves behind it = "
            "the head and its leaf crest; the two big light-green ovals = the moss shoulder humps, the thin brown forked sticks on "
            "them = the dead twigs; dark-green limbs = the vine-bundle upper arms and thighs; the light-green strips hanging under "
            "the arms = ropes of hanging moss; brown limbs with dark stripes = the root-wood forearms wound with the thorny vine; "
            "the two big brown blobs = the fists; pointed leaf shapes on the chest = the leaf collar; the dark diagonal band and "
            "the dark horizontal band = the vine across the belly and the vine belt; pointed leaf shapes below = the leaf skirt; "
            "brown shapes at the bottom = shins and feet). Use it for pose, placement, size and overlap only; redraw everything "
            "in the hand-drawn style of the approved heroes.",
            "Sơ đồ bố cục bản 2 tự dựng bằng mã (1536 × 1024, nền trắng): hình người to vai thế thủ nhìn sang phải; đầu lục nhỏ góc cạnh "
            "có dải mày tối và hai mắt cam, ba lá sẫm sau đầu; hai bầu dục lục nhạt rất to: u rêu vai, que nâu có chạc: cành khô; tay "
            "chân lục sẫm: bắp tay, đùi; các dải lục nhạt rủ dưới tay: rêu rủ; tay nâu sọc sẫm: cẳng tay gỗ quấn dây gai; hai khối nâu "
            "to: nắm tay; lá trên ngực: cổ áo lá; dải sẫm chéo + ngang: dây leo vắt bụng, đai; lá rủ dưới: váy lá. Chỉ lấy dáng, chỗ, cỡ")
    return R


def main2():
    os.makedirs(pk(), exist_ok=True)
    R = refs2()
    missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
    gd = ["", "## Bản 2 (2026-11-12): quái đầm lầy nặng đô", "",
          "Người dùng trả bản 1 (hướng A, B ở trên): \"chưa đủ chiến, đầu nhìn xấu quá, làm sát với swampthing hơn 1 chút\". Bản 2: vai u "
          "khổng lồ, đầu nhỏ thụt giữa hai vai, thân rêu lục gần kín, gờ mày + hàm bạnh, cành khô trên vai, rêu rủ dưới tay. Hai kiểu đầu.",
          "", "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    gd += [""]
    ra = []
    for kieu, ten in MAU2.items():
        out = os.path.join(save_dir(), f"L1b_{kieu}.png")
        p = os.path.join(pk(), f"luot_1b_concept_{kieu}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1b_{kieu}_2.png, L1b_{kieu}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "",
              "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready pose, in the hand-drawn style of the "
              "approved hero images.", "", body2(kieu), "", FRAME2, "", POSE2, "", SOFT, LINE2, FLAT, BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd += [f"- **Kiểu `{kieu}`** ({ten}). **Chỉ gửi GPT đường dẫn:** `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…). "
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{K}/luot_1b_concept_{kieu}.txt`."]
    gd += ["", "### Kiểm bản 2", ""] + [f"- {c}" for c in CHECK2]
    gd += ["", "### GPT vẽ sai thì gửi thêm (bản 2)", "", "| Sai | Gửi thêm |", "|---|---|"] + [f"| {a} | `{b}` |" for a, b in FIX2]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Bản 2 (")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ================================================================ LƯỢT 2: MẢNH (bản D "nhe nanh" đã duyệt 2026-11-12)
# Rig gốc monster_3491 là kiểu cắt giấy (thân, tay ba khúc, chân ba khúc): mảnh của mình là MẢNH CỨNG, chỗ nối khác chất liệu (bắp tay
# dây leo lục ↔ cẳng tay gỗ nâu) hoặc nấp sau lớp phủ (u rêu vai, cổ áo lá, đai, váy lá). Bốn tờ "đúng chỗ, đúng cỡ" (A..D: mỗi tờ giữ
# vài mảnh KHÔNG chồng nhau trên concept, vẽ đủ phần khuất) + hai tờ mảnh rời (S1: lá, râu, cành khô, rêu rủ; S2: quả cầu dây leo và dây
# gai của hai chiêu). Cắt và đặt: nguoi_cay_manh.py.
CON3 = ("a hulking swamp plant brute, a humanoid monster made entirely of plants, in a boxer's stance facing right: a small angular "
        "moss-green head with a heavy dark brow band, two orange eyes, an open snarling mouth with cream wooden teeth and a beard of "
        "light-green leaves, and a crest of dark serrated leaves; two huge light-green moss humps on the shoulders with bare forked "
        "brown twigs and one dark leaf each; thick upper arms and a barrel torso of bundled dark-green vines with a dark vine across "
        "the belly; a collar of serrated leaves on the chest; brown root-wood forearms wound with a dark thorny vine with cream "
        "thorns; two huge brown wooden fists with thorns; ropes of light-green hanging moss under the arms; a dark vine belt and a "
        "skirt of dark and light serrated leaves; brown root-wood shins with a vine ring and broad three-toed root feet")
C3 = dict(than="#4E7A3E", reu="#7CA44A", la="#2C6042", la_nhat="#92BA5C", gan="#173D2B", canh="#7A5A3A", go="#987248", day="#2F5233",
          gai="#EFE0A8")
KEEP_TASK = ("TASK: redraw image 1, but keep ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME "
             "SIZE as in image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE "
             "everything else and leave pure white (#FFFFFF) there. Every kept part must be ONE COMPLETE CLOSED SHAPE with the "
             "dark-brown ink outline running all the way around it: where a part is hidden behind another part in image 1, DRAW the "
             "hidden portion as described. The kept parts must NOT touch each other: clear white between them. Same wobbly ink line, "
             "same line thickness, same colours, same crayon hatching, same completely flat colouring as image 1. Do not add "
             "anything: no shadows, no glow, no dust, no labels.")
FLAT3 = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do not "
         "model light. No shading, no darker side, no lighter patches, no shadows of any kind, no white highlights or shine spots "
         "(except the one tiny white dot in each eye), no gloss, no glow, no gradients, no 3D look.\n"
         "Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
         "outline around the shapes. No text, no labels, no numbers, no frame, no guide lines.")
TO3 = {
    "A": ("đầu, hai cẳng tay, hai ống chân, đai", [
        "THE HEAD ALONE (about x = 700 to x = 950, y = 190 to y = 400): the angular moss-green head with its dark brow band, the dark "
        "eye band with the two orange eyes, the open snarling mouth with its cream teeth and two tusks, and its heavy jaw. WITHOUT "
        "the crest leaves on top, WITHOUT the leaf beard under the chin, WITHOUT the collar leaves, WITHOUT the shoulder humps. "
        "Complete it into ONE closed head shape: where the crest leaves cover its top and its back (upper left) in image 1, draw the "
        "plain rounded moss-green skull there; where the beard and the collar cover its chin and lower jaw, draw the square chin "
        "closed with one firm ink line (the chin ends at about y = 402).",
        "THE NEAR FOREARM (the left one; about x = 235 to x = 430, y = 478 to y = 672): the brown root-wood forearm with its dark "
        "thorny vine wound round it and its cream thorns, WITHOUT the fist below it and WITHOUT the upper arm. Complete it into one "
        "chunky closed club shape: its upper end (the elbow, at about (345, 492), hidden under the upper arm in image 1) is a "
        "rounded knob of the same brown wood; its lower end (the wrist, at about (345, 672)) is closed, rounded brown wood.",
        "THE FAR FOREARM (the right one, raised; about x = 1068 to x = 1252, y = 388 to y = 622): the same: brown root-wood wound with "
        "the thorny vine and thorns, WITHOUT the fist above it and WITHOUT the upper arm. Its lower end (the elbow, at about "
        "(1120, 600)) is a rounded knob; its upper end (the wrist, at about (1195, 400), hidden behind the fist in image 1) is "
        "closed, rounded brown wood.",
        "THE NEAR SHIN (about x = 445 to x = 600, y = 795 to y = 918): the brown root-wood lower leg with its dark vine ring around "
        "the ankle, WITHOUT the foot below it. Its top (the knee, at about (530, 805), hidden under the leaf skirt in image 1) is a "
        "rounded knob of brown wood; its bottom (just under the vine ring, at about y = 918) is closed, rounded brown wood.",
        "THE FAR SHIN (about x = 893 to x = 1038, y = 785 to y = 908): the same for the right leg: brown root-wood with its vine ring, "
        "WITHOUT the foot; rounded knob at the knee (at about (955, 795)), closed rounded bottom under the vine ring.",
        "THE VINE BELT (about x = 573 to x = 937, y = 630 to y = 684): the thick dark-green vine belt alone, as one closed, slightly "
        "sagging band about 44 px thick with rounded ends, with its small knot / overlap at the right end as in image 1. No leaves "
        "hanging from it.",
    ]),
    "B": ("thân, hai nắm tay, hai bàn chân", [
        "THE TORSO ALONE (about x = 585 to x = 945, y = 395 to y = 690): the barrel-shaped chest and belly of bundled dark-green vines "
        f"({C3['than']}) with the dark vine ({C3['day']}) that crosses the belly diagonally, WITHOUT the head, WITHOUT the collar "
        "leaves and the beard, WITHOUT the shoulder humps and arms, WITHOUT the belt and the leaf skirt, WITHOUT the hanging moss. "
        "Complete it into ONE closed, broad, rounded barrel shape: where the collar leaves, the beard and the head cover its upper "
        "chest in image 1, draw the same dark-green vine bundles continuing up to a broad rounded top (two rounded shoulders and a "
        "low neck stump, the top at about y = 395); where the belt and skirt cover its bottom, close it with a rounded bottom edge at "
        "about y = 690. Thin dark pencil lines follow the vine bundles as in image 1.",
        "THE NEAR FIST (the left one, hanging low; about x = 213 to x = 472, y = 688 to y = 852): the huge clenched fist of brown "
        "root-wood with its knuckles, folded thumb and its small cream thorns, WITHOUT the forearm and WITHOUT the vine. Its top "
        "(the wrist side, at about y = 690) is closed, rounded brown wood.",
        "THE FAR FIST (the right one, raised; about x = 1093 to x = 1322, y = 188 to y = 408): the same: the huge clenched wooden fist "
        "with its thorns, WITHOUT the forearm and WITHOUT the vine. Its bottom (the wrist side, at about y = 405) is closed, "
        "rounded brown wood.",
        "THE NEAR FOOT (about x = 403 to x = 592, y = 898 to y = 982): the broad three-toed root-wood foot alone, WITHOUT the shin and "
        "WITHOUT the vine ring. Its top (the ankle, at about (520, 900)) is closed with a rounded lump of brown wood.",
        "THE FAR FOOT (about x = 898 to x = 1102, y = 898 to y = 982): the same for the right foot: three blunt toes pointing right, "
        "closed rounded ankle lump on top (at about (965, 900)).",
    ]),
    "C": ("hai u rêu vai, hai đùi", [
        "THE NEAR SHOULDER HUMP (the left one; about x = 278 to x = 678, y = 250 to y = 472): the huge cushion of light-green moss "
        f"({C3['reu']}) with its bumpy, tufted outline and its little grass tufts, WITHOUT the two brown twigs and WITHOUT the dark "
        "leaf lying on it (draw plain moss where they were), WITHOUT the arm under it. Complete it into ONE closed cushion: where the "
        "head and the collar leaves cover its right end in image 1, draw the moss continuing to a rounded, bumpy right end at about "
        "x = 678.",
        "THE FAR SHOULDER HUMP (the right one; about x = 905 to x = 1142, y = 268 to y = 462): the same kind of moss cushion, WITHOUT "
        "its twig and WITHOUT its leaf. Complete it: where the head, the beard and the collar cover its left part in image 1, draw the "
        "moss continuing to a rounded, bumpy left end at about x = 905; where the raised fist covers its right edge, draw the bumpy "
        "moss outline (right end at about x = 1142).",
        f"THE NEAR THIGH: a thick, short thigh of bundled dark-green vines ({C3['than']}), drawn like the upper arms of image 1 (one "
        "chunky muscle shape with two or three thin dark pencil lines along it): a fat sausage about 135 px thick running from the hip "
        "at about (645, 690) down and to the LEFT to the knee at about (525, 815), both ends rounded. In image 1 it is almost "
        "completely hidden under the leaf skirt: draw it completely (about x = 455 to x = 715, y = 630 to y = 880).",
        "THE FAR THIGH: the same for the right leg: a fat sausage of bundled dark-green vines about 130 px thick running from the hip "
        "at about (850, 690) down and to the RIGHT to the knee at about (960, 805), both ends rounded (about x = 785 to x = 1030, "
        "y = 630 to y = 870).",
    ]),
    "D": ("hai bắp tay", [
        f"THE NEAR UPPER ARM (the left one; about x = 300 to x = 668, y = 428 to y = 590): the very thick, bulging upper arm of bundled "
        f"dark-green vines ({C3['than']}) with its thin dark pencil lines, WITHOUT the moss hump above it, WITHOUT the forearm, "
        "WITHOUT the hanging moss. Complete it into ONE closed, fat, slightly bent sausage running from the shoulder at about "
        "(610, 490) to the LEFT to the elbow at about (345, 520): where the moss hump covers its top in image 1, draw the vine bundles "
        "continuing up to a rounded top edge at about y = 430; both ends rounded; its lower outline as in image 1.",
        "THE FAR UPPER ARM (the right one; about x = 905 to x = 1128, y = 425 to y = 602): the same: a fat sausage of bundled "
        "dark-green vines running from the shoulder at about (945, 485) to the RIGHT and slightly down to the elbow at about "
        "(1090, 555), WITHOUT the hump, the forearm and the hanging moss; where the hump, the collar and the forearm cover it in "
        "image 1, draw it completely; both ends rounded.",
    ]),
}


def main_manh():
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    if not os.path.exists(duyet):
        raise SystemExit("chưa có concept duyệt " + Wp(duyet))
    ra = []
    gd = ["", "## Lượt 2: mảnh (bản D đã duyệt 2026-11-12)", "",
          f"Ảnh mẫu 1 của mọi tờ: `{Wp(duyet)}` (concept đã duyệt, 1536 × 1024, nền trắng: quái rêu dáng người thế thủ nhìn sang phải, hai u "
          "rêu vai có cành khô, đầu nhỏ nhe nanh có râu lá, tay gỗ quấn dây gai, váy lá). Mỗi tờ một file prompt; **chỉ gửi GPT đường dẫn "
          "file prompt**. Claude tự gen bằng `py -3 -I ArtGen/Spine/gen.py <file prompt>` rồi cắt bằng `py -3 -I "
          "ArtGen/Spine/nguoi_cay_manh.py lam`.", "",
          "| Tờ | File prompt | Giữ lại / vẽ gì | Ảnh lưu vào |", "|---|---|---|---|"]
    for ma, (vi, ds) in TO3.items():
        out = os.path.join(save_dir(), f"M_{ma}.png")
        p = os.path.join(pk(), f"luot_2_manh_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(duyet)}: the APPROVED picture of the creature, 1536x1024, white background: {CON3}.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "", KEEP_TASK, "", "KEEP:"]
        t += [f"{i}. {d}" for i, d in enumerate(ds, 1)]
        t += ["", FLAT3]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd.append(f"| `{ma}` | `{Wp(p)}` | đúng chỗ, đúng cỡ: {vi} ({len(ds)} mảnh, vẽ đủ phần khuất) | `{Wp(out)}` |")
    # tờ mảnh rời S1: lá, râu, cành khô, rêu rủ
    out = os.path.join(save_dir(), "M_S1.png")
    p = os.path.join(pk(), "luot_2_manh_S1.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(duyet)}: the APPROVED picture of the creature, 1536x1024, white background: {CON3}. It gives the design, the "
         "colours, the wobbly dark-brown ink line and its thickness, the crayon hatching and the exact look of the leaves, twigs and "
         "hanging moss.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as M_S1_2.png, M_S1_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: draw a PARTS SHEET for a 2D animation rig of the creature of image 1: landscape 1536x1024, pure-white background, "
         "SIXTEEN separate loose parts laid out in three rows, each drawn exactly in the style of image 1 (same ink line thickness as "
         "in image 1, about 6 px; same colours; same crayon hatching; flat colour). Every part is ONE COMPLETE CLOSED SHAPE with its "
         "own ink outline all the way round; the parts do NOT touch or overlap: at least 40 px of clear white between them. No "
         "creature, no body, nothing else on the sheet.", "",
         "ROW 1 (tops at about y = 40, bottoms at about y = 320), from left to right, SIX parts:",
         f"1-5. FIVE DARK LEAVES ({C3['la']}), the big saw-toothed leaves of the creature's skirt and crest: each drawn UPRIGHT with "
         "its STEM END AT THE TOP (a short blunt stalk) and its pointed TIP AT THE BOTTOM, about 115 px wide and 270 px tall, a "
         f"serrated edge, ONE centre vein ({C3['gan']}) and a few faint side veins. Centres at about x = 130, 360, 590, 820, 1050. "
         "Make them slightly different from one another (one a little curved to the left, one to the right, one broader, one "
         "narrower).",
         f"6. THE BEARD (centre at about x = 1330, about 150 px wide and 230 px tall): the creature's chin beard exactly as in image 1: "
         f"a hanging tuft of three or four overlapping LIGHT-GREEN serrated leaves ({C3['la_nhat']}), tips down, the middle one the "
         "longest; its top edge (where it hangs from the chin) is closed with a gently curved line.", "",
         "ROW 2 (tops at about y = 370, bottoms at about y = 650), from left to right, FOUR parts:",
         f"7-10. FOUR LIGHT LEAVES ({C3['la_nhat']}): the same kind of saw-toothed leaf, upright, STEM END AT THE TOP, TIP AT THE "
         "BOTTOM, about 115 px wide and 270 px tall, one centre vein of a darker green, a few faint side veins. Centres at about "
         "x = 130, 360, 590, 820; slightly different from one another.", "",
         "ROW 3 (tops at about y = 720, bottoms at about y = 990), from left to right, SIX parts:",
         f"11. A BIG FORKED DEAD TWIG ({C3['canh']}), like the big twig on the left shoulder hump of image 1: upright, about 120 px wide "
         "and 190 px tall, a bare stick about 26 px thick that forks into two blunt broken ends like a letter Y; its bottom end is "
         "cut flat. Centre at about x = 130.",
         "12. A SMALL FORKED DEAD TWIG, the same kind, about 85 px wide and 115 px tall, about 20 px thick. Centre at about x = 340.",
         "13. A MEDIUM FORKED DEAD TWIG, the same kind but its side branch points to the RIGHT (like the twig on the right shoulder "
         "hump of image 1), about 115 px wide and 170 px tall. Centre at about x = 540.",
         f"14-16. THREE ROPES OF HANGING MOSS ({C3['reu']}), like the moss ropes hanging under the arms in image 1: each one a soft, "
         "fuzzy-edged, slightly wavy hanging rope about 44 px thick with a rounded bottom tip and a flat, closed top end, two or three "
         "short pencil dashes on it. Lengths: about 210 px, 170 px and 135 px. Centres at about x = 800, 960, 1120; all three hang "
         "from the same height (tops at about y = 730).", "", FLAT3]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    ra.append(p)
    gd.append(f"| `S1` | `{Wp(p)}` | tờ mảnh rời, ba hàng: 5 lá sẫm + chòm râu; 4 lá nhạt; 3 cành khô + 3 dải rêu rủ (16 mảnh) | `{Wp(out)}` |")
    # tờ S2: quả cầu dây leo (chiêu cuối) + dây gai (chiêu mana)
    out = os.path.join(save_dir(), "M_S2.png")
    p = os.path.join(pk(), "luot_2_manh_S2.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(duyet)}: the APPROVED picture of a creature, 1536x1024, white background: {CON3}. It gives the colours, the "
         "wobbly dark-brown ink line and its thickness, the crayon hatching and the exact look of the thorny vine wound round the "
         "forearms (dark-green vine, cream cone-shaped thorns) and of the leaves.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as M_S2_2.png, M_S2_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: draw TWO separate objects that this creature conjures in battle, on ONE sheet, landscape 1536x1024, pure-white "
         "background, in exactly the style of image 1 (ink line about 6 px, same colours, crayon hatching, flat colour). Each object "
         "is ONE COMPLETE CLOSED SHAPE with its own ink outline; they do not touch. No creature, nothing else.", "",
         "1. A BALL OF VINES (upper half of the sheet, centre at about (768, 300), about 420 px across): a big round ball tightly "
         f"wound from thick dark-green vines ({C3['day']}) criss-crossing in all directions like a ball of yarn (five or six visible "
         f"vine bands, each about 34 px thick), the gaps between the bands filled with dark moss green ({C3['than']}); eight to ten "
         f"chunky cream cone-shaped THORNS ({C3['gai']}, each about 34 px) stick out all round its outline, and three small serrated "
         f"leaves ({C3['la_nhat']}) poke out between the bands. A solid, heavy, dangerous-looking ball. Perfectly readable round "
         "silhouette.",
         "2. A LONG THORNY VINE (lower part of the sheet), lying perfectly STRAIGHT and HORIZONTAL from its thick root end at the LEFT "
         "(at about x = 70) to its tip at the RIGHT (at about x = 1470), its centre line at about y = 800: one thick dark-green vine "
         f"({C3['day']}) about 64 px thick at the root, tapering evenly to about 26 px near the tip, the tip ending in a small "
         "pointed curl. Its root end is cut flat. Along its whole length about sixteen chunky cream cone-shaped THORNS "
         f"({C3['gai']}, each about 36 px long) stick out, alternating up and down, evenly spaced; near the tip two small serrated "
         f"leaves ({C3['la_nhat']}). Two or three thin dark pencil lines run along the stem. It will be bent by the animation rig, so "
         "draw it straight: no bends, no coils, no knots.", "", FLAT3]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    ra.append(p)
    gd.append(f"| `S2` | `{Wp(p)}` | quả cầu dây leo có gai (chiêu cuối, ~420 px) ở nửa trên; một dây gai dài duỗi thẳng nằm ngang (chiêu "
              f"mana, gốc bên trái, ~1400 × 130) ở nửa dưới | `{Wp(out)}` |")
    gd += ["", "Kiểm từng tờ: tờ A..D các mảnh nằm ĐÚNG chỗ, đúng cỡ như concept (Claude chồng lên concept để đo), mỗi mảnh kín viền, không "
           "chạm nhau, nền trắng tinh; tờ S1 đủ 16 mảnh rời theo ba hàng; tờ S2 đủ hai vật, dây gai thẳng.", "",
           "Gửi thêm khi GPT vẽ sai: `Keep every kept part exactly where it is and at the size it has in image 1.` · `The kept parts must "
           "not touch: leave clear white between them.` · `Each part needs its own closed ink outline.` · `Flat colour only: remove every "
           "shadow, highlight and gradient.`"]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2: mảnh")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ================================================================ DẠNG 1 (con non), người dùng 2026-11-12: "ok gen dạng 1 đi"
# Bản D đã duyệt và đã rig (inbox/nguoi_cay_2) là dạng LỚN. Dạng 1 làm trên CÙNG rig, cùng dáng thủ: vẽ lại bản D, GIỮ NGUYÊN dáng và chỗ đặt
# thân, tay, chân (các khớp đọc trên bản D dùng lại được), ĐỔI: đầu to tròn hơn (chibi chỉ ở dạng 1), u rêu vai nhỏ, không cành khô, không
# gai, nắm tay nhỏ trơn, ít lớp lá, màu lục non. Thư mục: inbox/nguoi_cay_1, gói gui_gpt/nguoi_cay_1. Thiết kế là ĐỀ XUẤT của Claude.
NON = "nguoi_cay_1"
CN = dict(than="#6FA24A", reu="#A9D15C", la="#5E9E4C", la_nhat="#B4D968", gan="#2F6B3A", go="#B98C58", go_dam="#7A5632", day="#3F7A45",
          may="#3F7A45", hoc="#2C3A28", mat="#F08A2E", nanh="#EFE3C4")


def main_non():
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    if not os.path.exists(duyet):
        raise SystemExit("chưa có concept dạng lớn " + Wp(duyet))
    pkn = os.path.join(HERE, "gui_gpt", NON)
    tai = os.path.join(HERE, "inbox", NON, "tai_ve")
    os.makedirs(pkn, exist_ok=True)
    os.makedirs(tai, exist_ok=True)
    out = os.path.join(tai, "L1.png")
    p = os.path.join(pkn, "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(duyet)}: the APPROVED picture of the ADULT form of the creature, 1536x1024, white background: {CON3}. It gives "
         "the exact pose, the exact place of every limb on the canvas, the family look, the wobbly dark-brown ink line and its "
         "thickness, the crayon hatching and the completely flat colouring.",
         f"image 2 = {Wp(WORLD_STYLE)}: the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen "
         "outline + coloured pencil / wax crayon hatching), nothing of its content.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as L1_2.png, L1_3.png ... in the same folder. Do not edit, move or delete any "
         "other file.", "",
         "TASK: draw the YOUNG FORM of the creature of image 1: the same plant brawler when it is still a sapling, its FIRST "
         "evolution stage, as ONE picture, landscape 1536x1024, pure-white background. It must be recognisably the same family "
         "(a humanoid made of green vines with brown wooden fists, a dark brow band and orange eyes) but clearly YOUNGER, SMALLER-"
         "LOOKING, SIMPLER and LIGHTER in colour: fewer plant layers, nothing spiky. Character: a small, stubborn, determined young "
         "fighter with its guard up: appealing and a little cute with a big head, but frowning and battle-ready, not a smiling "
         "mascot, not scary.", "",
         "KEEP IDENTICAL to image 1 (very important: the same animation skeleton will be used, so if your picture were laid over "
         "image 1, these must coincide):",
         "- the canvas, the view (facing the viewer's right, three-quarter view) and the whole boxer's stance;",
         "- the POSITION of the torso (about x = 590 to x = 940, y = 420 to y = 690) and its barrel shape;",
         "- the POSITION, LENGTH and DIRECTION of both arms: the near arm at the viewer's left with its shoulder at about (606, 492), "
         "its elbow at about (345, 502) and its wrist at about (345, 680), the fist hanging below the wrist; the far arm at the "
         "viewer's right with its shoulder at about (946, 488), its elbow at about (1106, 584) and its wrist at about (1196, 406), "
         "the fist raised above the wrist;",
         "- the POSITION of both legs and feet: knees at about (528, 812) and (958, 800), ankles at about (520, 905) and (965, 905), "
         "the two broad three-toed feet exactly where they are (about x = 405 to x = 590 and x = 900 to x = 1100, y = 898 to "
         "y = 982);",
         "- the neck / chin level: the head sits on the shoulders at the same place (its chin at about y = 400, its centre at about "
         "x = 825).", "",
         "CHANGE (the young design):",
         f"1. COLOUR: the vine body (torso, upper arms, thighs) is a FRESH YOUNG GREEN ({CN['than']}) instead of dark moss green, with "
         "fewer pencil lines (smooth young vines).",
         "2. HEAD: BIGGER and ROUNDER than in image 1 (about 300 px wide and 250 px tall: about x = 675 to x = 975, y = 150 to "
         f"y = 400), a smooth rounded head of the same fresh green, like a big bud. The dark brow band ({CN['may']}) is still there "
         "but thinner (about 16 px) and gently V-shaped; under it a narrow dark eye band "
         f"({CN['hoc']}) with TWO eyes of flat orange ({CN['mat']}) that are BIGGER and rounder than in image 1 (each about 60 px "
         "wide), still slanted in a determined frown, with a small round dark pupil and one tiny white dot each. The mouth is "
         "CLOSED: one short, firm, slightly frowning ink line about 70 px long, with TWO small cream lower tusks "
         f"({CN['nanh']}, each about 22 px) peeking up at its corners. NO open mouth, NO row of teeth, NO beard.",
         f"3. CREST: instead of the three big dark leaves, ONE small SPROUT on top of the head: a short stem with TWO young leaves "
         f"of light green ({CN['la_nhat']}), each about 85 px long with one centre vein, spreading left and right like a seedling "
         "(top at about y = 85).",
         f"4. SHOULDERS: instead of the two huge moss humps, two SMALL round TUFTS OF MOSS of light green ({CN['reu']}), each less "
         "than half as big (the near one about x = 455 to x = 640, y = 395 to y = 490; the far one about x = 930 to x = 1075, "
         "y = 400 to y = 485), sitting on top of the shoulders, with a bumpy outline and one or two tiny grass tufts. NO dead twigs, "
         "NO leaf lying on them.",
         f"5. COLLAR: instead of the collar of big saw-toothed leaves and the beard, a small collar of THREE short, smooth-edged "
         f"pointed leaves of light green ({CN['la_nhat']}) hanging under the chin (each about 95 px long and 55 px wide, one centre "
         "vein), about x = 730 to x = 920, y = 400 to y = 500.",
         f"6. BELLY: the vine across the belly is thinner (about 12 px, {CN['day']}).",
         f"7. FOREARMS: slimmer (about 80 % of the thickness in image 1), of lighter root-wood ({CN['go']}) with two or three grain "
         f"lines ({CN['go_dam']}); wound by ONE thin SMOOTH vine ({CN['day']}, about 10 px, only two turns) with NO thorns. There "
         "are NO thorns anywhere on the creature.",
         f"8. FISTS: clearly SMALLER and smooth (about 75 % of the size in image 1: the near fist about 190 px wide, hanging at about "
         f"x = 250 to x = 440, y = 690 to y = 835; the far fist about 175 px wide, at about x = 1110 to x = 1285, y = 235 to "
         f"y = 400), rounded wooden fists of {CN['go']} with simple knuckle lines, NO thorns on them.",
         f"9. HANGING MOSS: only ONE short rope of light-green moss ({CN['reu']}) under each upper arm (about 70 px long) instead of "
         "three.",
         f"10. BELT AND SKIRT: a thin vine belt ({CN['day']}, about 22 px thick) in the same place; from it a SHORT skirt of FIVE "
         f"small smooth-edged pointed leaves (each about 120 px long and 62 px wide), alternating {CN['la']} and {CN['la_nhat']}, "
         "each with one centre vein; the skirt ends at about y = 800, so more of the legs shows than in image 1.",
         f"11. LEGS: thighs of the fresh body green ({CN['than']}); shins and feet of the lighter root-wood ({CN['go']}), the shins a "
         f"little slimmer, each still with ONE thin vine ring ({CN['day']}) at the ankle.",
         "12. Nothing else: no twigs, no thorns, no flowers, no mushrooms, no extra leaves.", "",
         f"COLOURS (use exactly these, each area one flat colour): body vines {CN['than']}; moss tufts and moss ropes {CN['reu']}; "
         f"mid-green leaves {CN['la']}; light leaves {CN['la_nhat']}; leaf veins {CN['gan']}; root-wood {CN['go']}; vines, belt and "
         f"brow band {CN['day']}; eye band {CN['hoc']}; eyes {CN['mat']}; tusks {CN['nanh']}; every outline dark-brown ink (#2B2118). "
         "NO blue, NO purple, NO pink, NO red.", "",
         "ANIMATION-READY: as in image 1, every part is a clear shape with its own ink outline lying on top of the others: the head, "
         "the sprout leaves, each moss tuft, each collar leaf, each skirt leaf, each upper arm, forearm and fist, each thigh, shin "
         "and foot. The raised fist does not touch the head; the legs do not cross. No falling leaves, no dust, no glow, no motion "
         "lines, no ground line, no props.", "",
         "LINE AND COLOUR: exactly the hand-drawn look of image 1: dark-brown ink pen outline (#2B2118) about 6 px thick around the big "
         "parts and about 4 px around the small ones (eyes, tusks, vine turns, toes), slightly wobbly; coloured pencil and wax "
         "crayon hatching visible inside every area; clean and simple.", FLAT3]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = [f"# Gói gửi GPT: `{NON}` (người cây DẠNG 1, con non; dạng lớn là `nguoi_cay_2`)", "",
          "Làm 2026-11-12 theo lời người dùng \"ok gen dạng 1 đi\". Thiết kế con non là đề xuất của Claude, chờ người dùng duyệt concept. "
          "Ghi chú: `ArtGen/Spine/inbox/nguoi_cay_ghichu.md` mục 8.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{NON}/luot_1_concept.txt` (thêm `--note \"...\"` để sửa nhanh).",
          "", "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(duyet)}` | Concept DẠNG LỚN đã duyệt (1536 × 1024, nền trắng): quái rêu dáng người thế thủ nhìn sang phải, hai u rêu vai "
          "to có cành khô, đầu nhỏ nhe nanh có râu lá, tay gỗ quấn dây gai, váy lá. Lấy dáng, chỗ đặt tay chân, nét, vân sáp |",
          f"| 2 | `{Wp(WORLD_STYLE)}` | Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp |", "",
          "## Kiểm", "",
          "- **Cùng dáng thủ, cùng chỗ đặt thân, tay, chân** như dạng lớn (chồng lên bản dạng lớn thì khuỷu, cổ tay, gối, bàn chân trùng).",
          "- **Đầu to tròn hơn** như cái nụ, mày mảnh, hai mắt cam to hơn có con ngươi, **miệng mím có hai nanh nhỏ**; không râu, không hàm răng.",
          "- Trên đầu **một mầm hai lá non**; vai là **hai túm rêu nhỏ**, không cành khô.",
          "- Cổ áo ba lá nhỏ trơn mép; váy năm lá ngắn; mỗi tay một dải rêu rủ ngắn.",
          "- Cẳng tay gỗ nhạt quấn **dây leo trơn không gai**; hai nắm tay **nhỏ hơn, trơn**; cả con không có gai.",
          "- Màu lục non sáng hơn dạng lớn; tô phẳng, không bóng, nền trắng tinh, không bị cắt mép.", "",
          "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|",
          "| Dáng, chỗ tay chân lệch dạng lớn | `Keep the pose and the place of every limb exactly as in image 1: same shoulders, elbows, wrists, knees and feet.` |",
          "| Vẫn còn gai, cành khô, râu | `Remove every thorn, the dead twigs and the beard: the young form has none.` |",
          "| Mặt hiền, cười | `Keep the determined frown: slanted eyes under the brow band, closed frowning mouth with two small tusks.` |",
          "| Có bóng, mảng sáng tối | `Flat colour only: remove every shadow, highlight and gradient.` |"]
    open(os.path.join(pkn, "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    print(p)


# ---------------------------------------------------------------- dạng 1: mảnh (concept dạng 1 duyệt 2026-11-12: "nhìn ổn")
CON_NON = ("the young form of a plant brawler, a humanoid creature made of fresh-green vines, in a boxer's stance facing right: a big "
           "round green head like a bud with a dark-green brow band, two orange eyes, a closed frowning mouth with two small cream "
           "tusks, and a two-leaf sprout on top; two small light-green moss tufts on the shoulders; thick green upper arms and a "
           "barrel torso with a thin dark vine across the belly; a small collar of three light-green leaves under the chin; brown "
           "root-wood forearms wound with a thin smooth vine; two big smooth brown wooden fists; one short rope of light-green moss "
           "under each arm; a thin vine belt and a short skirt of five smooth leaves; brown root-wood shins with a vine ring and "
           "broad three-toed root feet")
TO_NON = {
    "A": ("đầu, hai cẳng tay, hai ống chân, đai", [
        "THE HEAD ALONE (about x = 612 to x = 985, y = 155 to y = 430): the big round green head with its dark-green brow band, the "
        "dark eye band with the two orange eyes, and the closed frowning mouth with its two small cream tusks. WITHOUT the two-leaf "
        "sprout on top (draw the plain rounded top of the head where its stalk was), WITHOUT the collar leaves, WITHOUT the moss "
        "tufts. Complete it into ONE closed round head shape: where the collar leaves and the moss tufts cover its lower part in "
        "image 1, draw the rounded chin and cheeks closed with one firm ink line (the chin ends at about y = 432).",
        "THE NEAR FOREARM (the left one; about x = 270 to x = 422, y = 495 to y = 700): the brown root-wood forearm with its thin "
        "dark-green vine wound round it, WITHOUT the fist below it and WITHOUT the upper arm. Complete it into one chunky closed club "
        "shape: its upper end (the elbow, at about (345, 506), hidden under the upper arm in image 1) is a rounded knob of the same "
        "brown wood; its lower end (the wrist, at about (338, 696)) is closed, rounded brown wood.",
        "THE FAR FOREARM (the right one, raised; about x = 1062 to x = 1238, y = 392 to y = 602): the same: brown root-wood wound "
        "with the thin vine, WITHOUT the fist above it and WITHOUT the upper arm. Its lower end (the elbow, at about (1106, 588)) is "
        "a rounded knob; its upper end (the wrist, at about (1165, 402), hidden behind the fist in image 1) is closed, rounded brown "
        "wood.",
        "THE NEAR SHIN (about x = 463 to x = 602, y = 795 to y = 915): the brown root-wood lower leg with its dark vine ring around "
        "the ankle, WITHOUT the foot below it. Its top (the knee, at about (535, 806), hidden under the leaf skirt in image 1) is a "
        "rounded knob of brown wood; its bottom (just under the vine ring) is closed, rounded brown wood.",
        "THE FAR SHIN (about x = 888 to x = 1022, y = 790 to y = 912): the same for the right leg: brown root-wood with its vine ring, "
        "WITHOUT the foot; rounded knob at the knee (at about (955, 800)), closed rounded bottom under the vine ring.",
        "THE VINE BELT (about x = 563 to x = 920, y = 634 to y = 694): the dark-green vine belt alone, as one closed, slightly sagging "
        "band with rounded ends, with its small knot / overlap at the right end as in image 1. No leaves hanging from it.",
    ]),
    "B": ("thân, hai nắm tay, hai bàn chân", [
        "THE TORSO ALONE (about x = 558 to x = 947, y = 400 to y = 705): the barrel-shaped chest and belly of fresh-green vines with "
        "the thin dark vine that crosses the belly diagonally, WITHOUT the head, WITHOUT the collar leaves, WITHOUT the moss tufts "
        "and arms, WITHOUT the belt and the leaf skirt, WITHOUT the hanging moss. Complete it into ONE closed, broad, rounded barrel "
        "shape: where the collar leaves and the head cover its upper chest in image 1, draw the same green vine body continuing up to "
        "a broad rounded top (two rounded shoulders and a low neck stump, the top at about y = 400); where the belt and skirt cover "
        "its bottom, close it with a rounded bottom edge at about y = 705. Thin dark pencil lines follow the vines as in image 1.",
        "THE NEAR FIST (the left one, hanging low; about x = 233 to x = 447, y = 693 to y = 830): the big smooth clenched fist of brown "
        "root-wood with its knuckle lines, WITHOUT the forearm and WITHOUT the vine. Its top (the wrist side, at about y = 695) is "
        "closed, rounded brown wood.",
        "THE FAR FIST (the right one, raised; about x = 1088 to x = 1312, y = 203 to y = 398): the same: the big smooth clenched wooden "
        "fist, WITHOUT the forearm and WITHOUT the vine. Its bottom (the wrist side, at about y = 396) is closed, rounded brown wood.",
        "THE NEAR FOOT (about x = 398 to x = 592, y = 898 to y = 982): the broad three-toed root-wood foot alone, WITHOUT the shin and "
        "WITHOUT the vine ring. Its top (the ankle, at about (528, 902)) is closed with a rounded lump of brown wood.",
        "THE FAR FOOT (about x = 898 to x = 1102, y = 898 to y = 982): the same for the right foot: three blunt toes pointing right, "
        "closed rounded ankle lump on top (at about (962, 902)).",
    ]),
    "C": ("hai túm rêu vai, hai đùi", [
        "THE NEAR MOSS TUFT (the left one; about x = 450 to x = 650, y = 320 to y = 470): the small cushion of light-green moss with "
        "its bumpy outline and its little grass tufts, WITHOUT the arm under it. Complete it into ONE closed round cushion: where the "
        "head covers its right end in image 1, draw the moss continuing to a rounded, bumpy right end at about x = 650.",
        "THE FAR MOSS TUFT (the right one; about x = 925 to x = 1088, y = 350 to y = 470): the same kind of small moss cushion. "
        "Complete it: where the head covers its left part in image 1, draw the moss continuing to a rounded, bumpy left end at about "
        "x = 925.",
        "THE NEAR THIGH: a thick, short thigh of fresh-green vines, drawn like the upper arms of image 1 (one chunky muscle shape "
        "with one or two thin dark pencil lines along it): a fat sausage about 125 px thick running from the hip at about (640, 700) "
        "down and to the LEFT to the knee at about (535, 806), both ends rounded. In image 1 it is partly hidden under the leaf "
        "skirt: draw it completely (about x = 460 to x = 705, y = 640 to y = 870).",
        "THE FAR THIGH: the same for the right leg: a fat sausage of fresh-green vines about 120 px thick running from the hip at "
        "about (850, 700) down and to the RIGHT to the knee at about (955, 800), both ends rounded (about x = 790 to x = 1025, "
        "y = 640 to y = 865).",
    ]),
    "D": ("hai bắp tay", [
        "THE NEAR UPPER ARM (the left one; about x = 320 to x = 665, y = 425 to y = 590): the thick, bulging upper arm of fresh-green "
        "vines with its thin dark pencil lines, WITHOUT the moss tuft above it, WITHOUT the forearm, WITHOUT the hanging moss. "
        "Complete it into ONE closed, fat, slightly bent sausage running from the shoulder at about (604, 492) to the LEFT to the "
        "elbow at about (345, 506): where the moss tuft and the torso cover it in image 1, draw the green vines continuing; both ends "
        "rounded; its lower outline as in image 1.",
        "THE FAR UPPER ARM (the right one; about x = 905 to x = 1128, y = 428 to y = 605): the same: a fat sausage of fresh-green vines "
        "running from the shoulder at about (946, 490) to the RIGHT and slightly down to the elbow at about (1106, 588), WITHOUT the "
        "moss tuft, the forearm and the hanging moss; where the tuft, the collar and the forearm cover it in image 1, draw it "
        "completely; both ends rounded.",
    ]),
}


def main_manh_non():
    pkn = os.path.join(HERE, "gui_gpt", NON)
    tai = os.path.join(HERE, "inbox", NON, "tai_ve")
    duyet = os.path.join(tai, "L1_duyet.png")
    if not os.path.exists(duyet):
        raise SystemExit("chưa có concept dạng 1 duyệt " + Wp(duyet))
    ra = []
    gd = ["", "## Lượt 2: mảnh dạng 1 (concept duyệt 2026-11-12)", "",
          f"Ảnh mẫu 1 của mọi tờ: `{Wp(duyet)}` (concept dạng 1 đã duyệt, 1536 × 1024, nền trắng: con non đầu to tròn có mầm hai lá, hai túm "
          "rêu vai nhỏ, tay gỗ quấn dây leo trơn, váy lá ngắn). Mỗi tờ một file prompt; **chỉ gửi GPT đường dẫn file prompt**. Claude tự "
          "gen bằng `py -3 -I ArtGen/Spine/gen.py <file prompt>` rồi cắt bằng `NC_DANG=1 py -3 -I ArtGen/Spine/nguoi_cay_manh.py lam`.", "",
          "| Tờ | File prompt | Giữ lại / vẽ gì | Ảnh lưu vào |", "|---|---|---|---|"]
    for ma, (vi, ds) in TO_NON.items():
        out = os.path.join(tai, f"M_{ma}.png")
        p = os.path.join(pkn, f"luot_2_manh_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(duyet)}: the APPROVED picture of the creature, 1536x1024, white background: {CON_NON}.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "", KEEP_TASK, "", "KEEP:"]
        t += [f"{i}. {d}" for i, d in enumerate(ds, 1)]
        t += ["", FLAT3]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd.append(f"| `{ma}` | `{Wp(p)}` | đúng chỗ, đúng cỡ: {vi} ({len(ds)} mảnh, vẽ đủ phần khuất) | `{Wp(out)}` |")
    out = os.path.join(tai, "M_S1.png")
    p = os.path.join(pkn, "luot_2_manh_S1.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(duyet)}: the APPROVED picture of the creature, 1536x1024, white background: {CON_NON}. It gives the design, "
         "the colours, the wobbly dark-brown ink line and its thickness, the crayon hatching and the exact look of the leaves and the "
         "hanging moss.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as M_S1_2.png, M_S1_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: draw a PARTS SHEET for a 2D animation rig of the creature of image 1: landscape 1536x1024, pure-white background, "
         "TWELVE separate loose parts laid out in three rows, each drawn exactly in the style of image 1 (same ink line thickness as "
         "in image 1, about 6 px; same colours; same crayon hatching; flat colour). Every part is ONE COMPLETE CLOSED SHAPE with its "
         "own ink outline all the way round; the parts do NOT touch or overlap: at least 40 px of clear white between them. No "
         "creature, no body, nothing else on the sheet.", "",
         "ROW 1 (tops at about y = 40, bottoms at about y = 320), from left to right, FIVE parts:",
         f"1-2. THE TWO LEAVES OF THE HEAD SPROUT ({CN['la_nhat']}): each is one smooth-edged, rounded young seedling leaf like those on "
         "top of the head in image 1, drawn UPRIGHT with its STALK END AT THE TOP (a short curved green stalk about 40 px long and "
         "16 px thick) and its rounded-pointed TIP AT THE BOTTOM, about 105 px wide and 250 px tall in all, with ONE centre vein of "
         f"a darker green ({CN['gan']}). Centres at about x = 150 and x = 400; the second one a little smaller and mirrored.",
         f"3-5. THREE COLLAR LEAVES ({CN['la_nhat']}): the smooth-edged pointed leaves that hang under the chin in image 1, each "
         "upright, STEM END AT THE TOP (blunt), pointed TIP AT THE BOTTOM, about 100 px wide and 230 px tall, one centre vein. Centres "
         "at about x = 680, 930, 1180; slightly different from one another.", "",
         "ROW 2 (tops at about y = 370, bottoms at about y = 650), from left to right, FIVE parts:",
         "6-10. FIVE SKIRT LEAVES: the smooth-edged pointed leaves of the creature's short skirt, each upright, STEM END AT THE TOP "
         "(blunt), pointed TIP AT THE BOTTOM, about 110 px wide and 250 px tall, one centre vein. From left to right their colours "
         f"are: mid green ({CN['la']}), light green ({CN['la_nhat']}), mid green ({CN['la']}), light green ({CN['la_nhat']}), mid "
         f"green ({CN['la']}). Centres at about x = 150, 420, 690, 960, 1230.", "",
         "ROW 3 (tops at about y = 720), from left to right, TWO parts:",
         f"11-12. TWO SHORT ROPES OF HANGING MOSS ({CN['reu']}), like the moss rope hanging under each arm in image 1: each a soft, "
         "bumpy-edged hanging rope about 46 px thick with a rounded bottom tip and a flat, closed top end. Lengths: about 190 px and "
         "about 160 px. Centres at about x = 300 and x = 700; both hang from the same height (tops at about y = 730).", "", FLAT3]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    ra.append(p)
    gd.append(f"| `S1` | `{Wp(p)}` | tờ mảnh rời, ba hàng: 2 lá mầm + 3 lá cổ áo; 5 lá váy; 2 dải rêu rủ (12 mảnh) | `{Wp(out)}` |")
    gd += ["", "Dây gai và quả cầu của hai chiêu dùng lại ảnh của dạng lớn (`inbox/nguoi_cay_2/manh/gai.png`, `cau.png`), thu nhỏ khi dựng rig.",
           "", "Kiểm từng tờ: tờ A..D các mảnh nằm ĐÚNG chỗ, đúng cỡ như concept, mỗi mảnh kín viền, không chạm nhau, nền trắng tinh; tờ S1 đủ "
           "12 mảnh rời theo ba hàng."]
    hd = os.path.join(pkn, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2: mảnh dạng 1")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in ra:
        print(p)


if __name__ == "__main__":
    if sys.argv[1:2] == ["non"]:
        main_non()
    elif sys.argv[1:2] == ["manh_non"]:
        main_manh_non()
    elif sys.argv[1:2] == ["manh"]:
        main_manh()
    elif sys.argv[1:2] == ["ban2"]:
        main2()
    else:
        main()
