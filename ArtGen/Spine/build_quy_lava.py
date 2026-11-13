# -*- coding: utf-8 -*-
"""Gói GPT vẽ tiểu quỷ lava (mã làm việc quy_lava, con gốc của rig: monster_3336). Tướng đầu tiên đảo Hỏa (suất 1 hiện là su_tu_lua, ải 71).

Người dùng (2026-11-13): "làm tướng đầu tiên của đảo hỏa, concept tiểu quỷ lava, con gốc lấy ref làm dạng 1; idle và run có thể làm gần
giống con gốc, thay đổi đi 1 chút nhưng phần tóc lửa tôi muốn bạn cải thiện thêm cho giống ngọn lửa thật hơn". Đánh thường đập khiên,
chiêu mana chĩa kiếm / giáo bắn tia lửa, chiêu cuối cầm giáo hai tay nhảy lên đâm thẳng xuống. Ba hướng màu dưới đây là ĐỀ XUẤT của
Claude, chờ người dùng chọn. Chỉ lấy của con gốc cách dựng (chỗ đặt, cỡ, thứ tự chồng từng part); hình là của mình. Không đính ảnh con
gốc; đính sơ đồ bố cục tự dựng bằng mã (quy_lava_bo_cuc.py).

    py -3 -I ArtGen/Spine/quy_lava_bo_cuc.py all
    py -3 -I ArtGen/Spine/build_quy_lava.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/quy_lava_1/luot_1_concept_<hướng>.txt [--note "..."]
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "quy_lava"
K = 1
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
KIEM_SI = os.path.join(HERE, "inbox", "kiem_si_1", "tai_ve", "L1_duyet.png")
CHIM_NON = os.path.join(HERE, "inbox", "chim_la_non", "tai_ve", "L1_duyet.png")


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


STANCE = ("STANCE (the same as in the layout guide, image 1): a small, chubby, battle-ready imp standing on the ground, seen from "
          "the front and slightly from its left side (a light three-quarter view), facing the viewer's RIGHT, so that BOTH eyes are "
          "visible, the near eye (on the viewer's left) a little bigger than the far eye (close to the right outline of the face). "
          "Its near arm, a huge stone gauntlet, holds a long spear-blade diagonally across the front of the body, the point down at "
          "the lower right; its far fist, raised at the right side, grips a tall narrow stone shield standing upright. Fierce, "
          "determined, ready to fight: a scowling little fire demon, appealing and chibi, NOT a smiling mascot, NOT scary horror.")

BODY = (
    "- FIRE ON THE HEAD (the most important feature; about {lua}): instead of hair the imp has a LIVING FLAME. It grows out of "
    "the whole top of the head, from just behind the near horn to the far horn (its root along about ({g0}, {g1}) to ({g2}, {g3}) "
    "is hidden behind the head's outline), and rises into FOUR or FIVE big FLAME TONGUES merged into one fire at the base. Draw "
    "it like a real campfire flame drawn by hand, NOT like spiky hair and NOT like thorns or leaves: every tongue is thick and "
    "round at its base, bends in a soft S-curve and tapers to a sharp tip that HOOKS backward to the viewer's LEFT, as if the "
    "fire were blown back while the imp charges forward; the tongues have different heights (the tallest one at the back-middle "
    "reaches about y = {lua_top}), some lean more than others, and their edges have a few C-shaped bites and small side licks "
    "that split off near the tips. One or two tiny separate flame drops may float just above two of the tips, still outlined. "
    "Three nested flat colour zones like a hand-drawn fire: {lua_mau}. The flame sits BEHIND the head and BEHIND both horns.\n"
    "- HEAD AND BODY (one single round bean-shaped mass, about {than}; there is NO neck, the head and the body are the same "
    "blob, a little taller than wide, the widest part at the eyes): {than_mau} A slightly lighter belly patch ({bung_mau}) "
    "spreads across the lower front below the mouth (about x = 720 to x = 945, y = 615 to y = 700), with a soft wavy upper "
    "edge. Two or three small round darker spots sit on the upper-left of the head, and one short branching lava crack runs "
    "on the lower-left side of the body near the gauntlet.\n"
    "- FACE: the near eye at about {mat_gan}, the far eye at about {mat_xa}. Each eye is a solid {mat_mau} HALF-MOON shape "
    "without a pupil: the bottom is round, the top is one straight edge slanting DOWN toward the middle of the face (an angry "
    "frown built into the eye shape), with a thick ink outline. The mouth (about {mieng}) is a small wide zigzag 'w' line with "
    "TWO tiny pointed white fangs pointing down from it, a determined scowl. No nose, no eyebrows, no ears.\n"
    "- TWO HORNS of dark volcanic glass ({da_ten}), each with one or two thin branching lava cracks ({nut_ten}): the NEAR horn "
    "(about {sung_gan}) grows from the upper left of the head and points straight UP with a slight backward curve; the FAR horn "
    "(about {sung_xa}) grows from the upper right of the head and curves OUTWARD to the right and then up, like a bull's horn. "
    "Both horns are in FRONT of the flame.\n"
    "- NEAR ARM (in front of the body at the left): one HUGE chunky stone GAUNTLET, the forearm and the fist one single rough "
    "block like a rock boxing glove (about {tay_gan}), {da_ten}, with a Y-shaped lava crack ({nut_ten}) across its face; a "
    "separate rounded stone knob caps its top like a shoulder pad (about {vai_gan}). It grips the spear-blade.\n"
    "- SPEAR-BLADE (the weapon, about {kiem}): a long two-part weapon lying diagonally from the upper left to the lower right. "
    "The BACK HALF (from its back end at about ({kg0}, {kg1}) to the gauntlet) is a broad flat slab of the same dark stone, "
    "shaped like a wide paddle blade, with two or three branching lava cracks; it passes BEHIND the gauntlet. The FRONT HALF is "
    "one long sharp spike of solid MAGMA CRYSTAL ({luoi_mau}) with a thin lighter line ({luoi_vien}) along its middle and two "
    "or three facet lines; it passes IN FRONT of the lower body and ends in a sharp point at about ({km0}, {km1}).\n"
    "- FAR ARM AND SHIELD (at the right): the far arm is short and chubby, the body colour (about {tay_xa}), bent up in front "
    "of the right side of the body; its fist is made of three chunky dark stone KNUCKLES stacked vertically (about {nam_xa}) "
    "that wrap around the handle of a tall narrow SHIELD: a slab of dark volcanic stone standing upright just behind the fist "
    "(about {khien}), seen almost edge-on, with a thick bevelled rim and one long vertical lava crack; its top sticks out above "
    "the fist and its pointed bottom below it.\n"
    "- LEGS AND FEET: short stubby legs hidden under the belly; under the body a row of chunky angular dark stone lumps make "
    "the feet like heavy rock boots (about {chan}).")

FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the figure stands in the middle of the canvas: from the back end of the "
         "spear-blade at about x = {x0} to the shield at about x = {x1}, and from the top of the flame at about y = {y0} to the "
         "point of the blade at about y = {y1}. Do NOT enlarge, shrink or move the figure.")

POSE = ("ANIMATION-READY (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): calm, "
        "clean resting pose exactly as in the guide. Draw every piece as a clear, simple, closed shape with its own ink outline, "
        "so that the pieces can be separated: flame / head-body / each horn / each eye / mouth / near gauntlet / its shoulder knob "
        "/ spear-blade / far arm / each of the three knuckles / shield / each foot lump. No sparks, no embers, no smoke, no glow, "
        "no speed lines, no ground, no lava puddle, no props, no second character.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram: take ONLY the placement, the sizes, the overlaps and the kind of colour of each "
        "piece from it, never its line, its edge noise or its exact blob shapes. Design the real shape of every piece yourself as "
        "described: bold, chunky, readable shapes with a clear silhouette, the way a carefully designed first-stage Pokemon-like "
        "monster is drawn (compact, chubby, big eyes, few but clear details). Do NOT copy any existing character.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 5 px thick on this canvas around every big piece, and about 3 px for small "
        "details (lava cracks, facet lines, the mouth, the fangs); every area coloured with coloured pencils and wax crayons, the "
        "strokes visible as loose diagonal hatching (strokes thinner than the outline), kept inside the outline. Clean and "
        "appealing, neither a crude scribble nor an over-rendered painting.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker underside, no lighter patches except the designed belly patch, no shadows of any "
        "kind (no cast shadow of one piece on another, no shadow under the figure or on the background), no white highlights or "
        "shine spots (not on the horns, not on the stone, not on the crystal), no gloss, no reflections, NO GLOW around the fire "
        "or the lava cracks, no halo, no rim light, no gradients, no 3D look. The fire and the lava look hot only because their "
        "flat colours are bright.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no effects around the "
      "character.")

LUA = "outside a red-orange (#E03E24), inside it an orange (#F48824), and a yellow core (#FFD652) only in the lower part of each tongue near the scalp"

D = {
    "than_tim": dict(
        ten="đá than tím (sát con gốc): thân tím than, đá sẫm gần đen, vết nứt dung nham đỏ cam, lưỡi giáo dung nham đỏ cam",
        than_mau="The skin is cooled volcanic stone, a muted charcoal VIOLET (#5C5070).",
        bung_mau="a soft dusty mauve, #7E6E86",
        da_ten="very dark charcoal stone (#383240)", nut_ten="glowing red-orange lava, #EC5630",
        luoi_mau="red-orange #EE5C38", luoi_vien="#FFC45C", mat_mau="bright yellow (#FFD660)",
        palette=("COLOURS (use exactly these, each area one flat colour): head-body and far arm charcoal violet (#5C5070); belly "
                 "patch dusty mauve (#7E6E86) and darker spots (#4C4260); horns, gauntlet, shoulder knob, knuckles, shield, the "
                 "back half of the weapon and the foot lumps very dark charcoal stone (#383240); every lava crack red-orange "
                 "(#EC5630); the magma crystal red-orange (#EE5C38) with a yellow-orange line (#FFC45C); eyes bright yellow "
                 "(#FFD660); fangs white; the fire red-orange / orange / yellow as described; every outline dark-brown ink "
                 "(#2B2118). Only these colours: NO blue, NO green, NO pink."),
        check=["Thân **tím than**, mảng bụng tím hồng nhạt; đá (sừng, găng tay, khiên, chân, nửa sau giáo) **gần đen**; vết nứt đỏ cam."]),
    "da_nung": dict(
        ten="đá đỏ nung: thân nâu đỏ bazan, đá đen nâu, vết nứt cam vàng, lưỡi giáo cam",
        than_mau="The skin is hot-baked volcanic rock, a deep brick RED-BROWN (#7C4238).",
        bung_mau="a lighter terracotta, #A0604C",
        da_ten="very dark brown-black stone (#3A2828)", nut_ten="glowing orange-yellow lava, #FFA034",
        luoi_mau="bright orange #FA842C", luoi_vien="#FFD660", mat_mau="bright yellow (#FFE070)",
        palette=("COLOURS (use exactly these, each area one flat colour): head-body and far arm brick red-brown (#7C4238); belly "
                 "patch terracotta (#A0604C) and darker spots (#6A362E); horns, gauntlet, shoulder knob, knuckles, shield, the "
                 "back half of the weapon and the foot lumps very dark brown-black stone (#3A2828); every lava crack "
                 "orange-yellow (#FFA034); the magma crystal bright orange (#FA842C) with a yellow line (#FFD660); eyes bright "
                 "yellow (#FFE070); fangs white; the fire red-orange / orange / yellow as described; every outline dark-brown "
                 "ink (#2B2118). Only these colours: NO purple, NO blue, NO green, NO pink."),
        check=["Thân **nâu đỏ gạch**, mảng bụng đất nung; đá **đen nâu**; vết nứt **cam vàng** (sáng hơn hướng 1)."]),
    "tro_nui": dict(
        ten="tro núi lửa: thân xám tro sáng, đá than, vết nứt cam, lưỡi giáo cam",
        than_mau="The skin is light volcanic ASH stone, a warm pale GREY (#96908C), like pumice.",
        bung_mau="a lighter warm grey, #B8B0A8",
        da_ten="dark charcoal stone (#403C40)", nut_ten="glowing orange lava, #F67028",
        luoi_mau="orange #F67028", luoi_vien="#FFC85A", mat_mau="bright yellow (#FFD25A)",
        palette=("COLOURS (use exactly these, each area one flat colour): head-body and far arm warm ash grey (#96908C); belly "
                 "patch light warm grey (#B8B0A8) and darker spots (#7E7874); horns, gauntlet, shoulder knob, knuckles, shield, "
                 "the back half of the weapon and the foot lumps dark charcoal stone (#403C40); every lava crack orange "
                 "(#F67028); the magma crystal orange (#F67028) with a yellow-orange line (#FFC85A); eyes bright yellow "
                 "(#FFD25A); fangs white; the fire red-orange / orange / yellow as described; every outline dark-brown ink "
                 "(#2B2118). Only these colours: NO purple, NO blue, NO green, NO pink."),
        check=["Thân **xám tro sáng** như đá bọt, mảng bụng xám ấm nhạt; đá **than sẫm**; vết nứt cam (tương phản mạnh nhất)."]),
}

CHECK_CHUNG = [
    "Bố cục y sơ đồ: nhìn ba phần tư sang **phải**, **lộ cả hai mắt** (mắt gần to hơn), thân hạt đậu liền đầu, không cổ.",
    "**Tóc là NGỌN LỬA thật**: 4–5 lưỡi lửa gốc dày uốn chữ S, ngọn nhọn móc ngả về sau (sang trái), liền một khối ở gốc, ba lớp đỏ cam "
    "/ cam / lõi vàng ở gốc; không phải gai tóc, không phải lá; nằm SAU đầu và sau hai sừng.",
    "Mắt vàng hình **nửa trăng** cạnh trên xếch xuống về giữa mặt (cau có), không con ngươi; miệng chữ \"w\" có **hai răng nanh** nhỏ.",
    "Tay gần là **găng tay đá to** liền khối có núm vai, vết nứt chữ Y; nắm **giáo hai phần**: nửa sau phiến đá sẫm (sau găng), nửa trước "
    "mũi tinh thể dung nham nhọn (trước bụng), mũi ở dưới phải.",
    "Tay xa ngắn màu thân, nắm tay là **ba khối đá** xếp dọc, nắm **khiên đá dựng đứng** hẹp sau nắm tay, có vết nứt dọc.",
    "Tô phẳng, không bóng, **không quầng sáng** quanh lửa và vết nứt; nét bút nâu rung, vân sáp; nền trắng; mỗi mảnh viền kín.",
]

FIX = [
    ("Tóc thành gai tóc / gai nhọn", "The fire on the head must look like real flames: thick round bases, S-curved tongues, tips hooking back to the left, merged at the base, three nested colours. Not spiky hair."),
    ("Có quầng sáng / tia lửa bay", "Remove every glow, halo, spark and ember. Flat colours only."),
    ("Chỉ thấy một mắt / nhìn thẳng", "Light three-quarter view facing right: BOTH eyes visible, the near eye bigger, the far eye close to the right outline, exactly as in the layout guide."),
    ("Mắt có con ngươi / mắt tròn", "Each eye is a solid yellow half-moon without a pupil, its straight top edge slanting down toward the middle of the face."),
    ("Giáo một khúc / sai chiều", "The weapon has two halves: a broad dark stone paddle at the upper left behind the gauntlet and a long magma-crystal spike in front of the belly pointing to the lower right."),
    ("Có bóng đổ / tô khối", "Flat colour only: no shading, no cast shadow, no highlights."),
]


def refs(kieu):
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature in its resting stance, built "
         "from rough coloured blobs: where every piece goes on the canvas, how big it is and which piece overlaps which (the fire "
         "on the head with three colour zones, behind two dark horns; the round head-body with two yellow eyes and a zigzag mouth; "
         "the big dark stone gauntlet at the left holding the two-part spear-blade diagonally, its dark back half at the upper left "
         "and its bright crystal front half pointing to the lower right; the far fist of three dark knuckles at the right holding "
         "a tall narrow dark shield; dark stone lumps under the body). Use it for placement, size and overlap only; design and "
         "redraw everything in the hand-drawn style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng) ở dáng nghỉ của rig: ngọn lửa ba lớp sau hai sừng sẫm, thân tròn hai mắt "
         "vàng, găng tay đá bên trái nắm giáo chéo (nửa sau sẫm, nửa trước tinh thể sáng mũi xuống dưới phải), nắm tay ba khối đá bên "
         "phải cầm khiên hẹp dựng đứng, khối đá dưới chân. Lấy chỗ đặt, cỡ, thứ tự chồng"),
        (KIEM_SI,
         "an approved hero of the same game (an armoured monkey samurai), 1536x1024, white background: match EXACTLY its wobbly "
         "dark-brown pen line, its visible crayon hatching, its completely flat colouring, its bold chunky shapes and its fierce "
         "battle-ready attitude. Do NOT copy its species, its design or its colours.",
         "Voọc Tướng đã duyệt (1536 × 1024, nền trắng): khỉ samurai giáp lục. Lấy nét bút rung, vân sáp, tô phẳng, thần thái chiến"),
        (CHIM_NON,
         "another approved hero of the same game, a FIRST-STAGE (young) form, 1536x1024, white background: the same line and flat "
         "crayon colouring; see how a small first-stage hero is drawn simple and compact. Do NOT copy its species, design or colours.",
         "Chim lá non đã duyệt (1536 × 1024, nền trắng): dạng 1 nhỏ gọn. Lấy nét, tô phẳng, độ gọn của dạng 1"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp"),
    ]


def ghi(p, lines):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def main():
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    B = bc()
    allx = [B[k] for k in ("lua", "dau", "than", "kiem", "khien", "tay_xa", "chan")]
    x0, y0 = min(b[0] for b in allx), min(b[1] for b in allx)
    x1, y1 = max(b[2] for b in allx), max(b[3] for b in allx)
    gd = [f"# Gói gửi GPT: `{CODE}` (tiểu quỷ lava, tướng đầu tiên đảo Hỏa, tên chưa đặt)", "",
          "Làm 2026-11-13: dựng trên rig của con gốc `monster_3336` (quỷ đá lửa tóc vàng, găng tay đá cầm giáo dung nham, tay kia cầm "
          "khiên đá). Ba hướng màu là đề xuất của Claude, chờ người dùng chọn và duyệt concept. Ghi chú: "
          "`ArtGen/Spine/inbox/quy_lava_ghichu.md`.", "",
          "Lượt mảnh chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    ra = []
    for kieu, d in D.items():
        R = refs(kieu)
        missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
        if missing:
            raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
        out = os.path.join(save_dir(), f"L1_{kieu}.png")
        p = os.path.join(pk(), f"luot_1_concept_{kieu}.txt")
        g = B["lua_goc"]
        body = BODY.format(
            lua=xy(B["lua"]), g0=g[0], g1=g[1], g2=g[2], g3=g[3], lua_top=B["lua"][1], lua_mau=LUA,
            than=xy([B["dau"][0], B["dau"][1], B["dau"][2], B["than"][3]]), than_mau=d["than_mau"], bung_mau=d["bung_mau"],
            mat_gan=xy(B["mat_gan"]), mat_xa=xy(B["mat_xa"]), mat_mau=d["mat_mau"], mieng=xy(B["mieng"]),
            da_ten=d["da_ten"], nut_ten=d["nut_ten"], sung_gan=xy(B["sung_gan"]), sung_xa=xy(B["sung_xa"]),
            tay_gan=xy(B["tay_gan"]), vai_gan=xy(B["vai_gan"]), kiem=xy(B["kiem"]), kg0=B["kiem_goc"][0], kg1=B["kiem_goc"][1],
            km0=B["kiem_mui"][0], km1=B["kiem_mui"][1], luoi_mau=d["luoi_mau"], luoi_vien=d["luoi_vien"],
            tay_xa=xy(B["tay_xa"]), nam_xa=xy(B["nam_xa"]), khien=xy(B["khien"]), chan=xy(B["chan"]))
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "",
              "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
              "approved hero images.", "",
              "CREATURE: a LAVA IMP, the first-stage fire-element hero of the volcano island in a monster-collecting game: a small, "
              "chubby little fire demon whose round body is cooled volcanic stone crossed by glowing lava cracks; a blazing living "
              "FIRE burns on top of its head instead of hair; two dark volcanic-glass horns; a huge stone gauntlet on its near arm "
              "grips a long magma-crystal spear-blade, and its far fist holds a tall stone shield. It is a creature (a little "
              "demon pet), NOT a human, NOT a robot, NOT a golem made of separate floating rocks.", "",
              STANCE, "",
              "Follow the LAYOUT GUIDE (image 1) for WHERE every piece is on the canvas, HOW BIG it is and WHICH piece overlaps "
              "which. Coordinates below are pixels on the 1536x1024 canvas (x from the left, y from the top). NEAR = the side of "
              "the body toward the viewer (the viewer's left); FAR = the other side (the viewer's right).", "",
              body, "",
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
    gd += ["Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/quy_lava_bo_cuc.py all`).",
           "", "## Kiểm chung", ""]
    gd += [f"- {c}" for c in CHECK_CHUNG]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    ghi(os.path.join(pk(), "HUONG_DAN.md"), gd)
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 1b: khiên dày hơn (người dùng 2026-11-13: "làm B, khiên tôi thấy hơi mỏng")
def build_1b():
    src = os.path.join(save_dir(), "L1_da_nung.png")
    out = os.path.join(save_dir(), "L1b_khien_day.png")
    p = os.path.join(pk(), "luot_1b_khien_day.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(src)}: THE CHARACTER, already drawn and approved (1536x1024, white background): a chubby lava imp with a "
         "fire on its head, a stone gauntlet holding a spear-blade, and a narrow stone shield in its far fist at the right.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as L1b_khien_day_2.png, L1b_khien_day_3.png ... in the same folder. Do not "
         "edit, move or delete any other file.", "",
         "TASK: redraw image 1 EXACTLY, changing ONLY the shield.", "",
         "KEEP IDENTICAL (if the new picture is laid over image 1, everything except the shield must match: same place, same size, "
         "same shapes, same colours, same line): the fire on the head with its two small floating drops, both horns, the round "
         "red-brown head-body with its spots and belly patch, the eyes, the mouth and fangs, the big stone gauntlet and its shoulder "
         "knob, the whole spear-blade (dark stone back half and orange crystal front half), the far arm, the three-plus stacked "
         "dark stone knuckles of the far fist, the stone feet. Same canvas, same framing, same wobbly dark-brown ink line, same "
         "crayon hatching, same flat colours.", "",
         "CHANGE ONLY THE SHIELD: it is too thin now (about 95 px wide, x = 995 to x = 1092). Make it a proper sturdy SHIELD, about "
         "TWICE as wide and clearly THICK:",
         "- It stays in the same place behind the far arm and the far fist, upright, the same height as now (top at about y = 430, "
         "bottom point at about y = 860), but now spans about x = 985 to x = 1170 (about 185 px wide).",
         "- Shape: a heavy slab of dark brown-black volcanic stone (#3A2828) shaped like a tall heater / kite shield: a slightly "
         "rounded top with two blunt corners, straight sides, tapering in the lower third to a blunt point at the bottom.",
         "- It is seen at a three-quarter angle: its FACE turns toward the viewer and slightly to the right, and along its LEFT side "
         "a clearly visible THICKNESS band (the stone edge, about 22 px wide, a slightly darker flat brown #2E2020) shows how thick "
         "and heavy it is. A thick bevelled rim runs around the face (one inner outline about 14 px inside the edge).",
         "- On its face: one bold branching lava crack in orange-yellow (#FFA034) running from the top down to the point, with two "
         "short side branches, flat colour, no glow.",
         "- The far arm and the knuckles of the far fist stay IN FRONT of the shield exactly as now, gripping it near its left "
         "side; the shield shows above, to the right of and below the fist.", "",
         "Flat colours only: no shading, no highlights, no glow, no cast shadow. Plain pure-white background, no ground, no text."]
    ghi(p, t)
    print(p)


# ---------------------------------------------------------------- lượt 2: mảnh "đúng chỗ, đúng cỡ" từ concept đã duyệt
# Mỗi tờ giữ vài bộ phận KHÔNG chạm nhau trên concept, vẽ đủ phần khuất, bỏ hết thứ khác (skill pokiclash-spine-rig mục 00, 25).
# Toạ độ (px concept 1536 × 1024) đọc trên tai_ve/L1_duyet.png kẻ lưới; sửa ở MANH_XY nếu concept đổi.
TO_MANH = {
    "A": [
        "THE HEAD-BODY (about x = 595 to x = 990, y = 380 to y = 800): the one round bean-shaped mass of brick red-brown stone, with "
        "its three dark round spots on the upper left and its lighter terracotta belly patch with the wavy upper edge. WITHOUT the "
        "eyes and WITHOUT the mouth: where they are in image 1, draw plain red-brown skin (the belly patch stays where it is). WITHOUT "
        "the fire, the horns, the gauntlet, the spear-blade, the far fist, the shield and the feet. Complete everything they hide: "
        "the top of the head is one smooth round dome (its top at about y = 375, under where the fire and the horns were); the left "
        "side continues as a smooth round curve behind where the gauntlet was (leftmost at about x = 595); the right side is a smooth "
        "round curve at about x = 990 behind where the fist was; the bottom is a broad rounded base at about y = 800 (the belly patch "
        "continues down to it). No legs, no feet. A single closed outline all the way around.",
    ],
    "B": [
        "THE FIRE (about x = 488 to x = 985, y = 55 to y = 470): the whole living flame with all its tongues and its three nested "
        "colours (red-orange outside, orange inside, yellow core), WITHOUT the two small separate flame drops, WITHOUT the horns and "
        "the head. Complete its base: where the head and the horns cover it in image 1, the flame continues down (yellow core and "
        "orange) and is closed by a broad, gently rounded bottom edge that follows the top of the head at about y = 470, from about "
        "x = 600 to x = 960. One closed shape.",
        "THE TWO SMALL FLAME DROPS (one at about x = 605 to x = 670, y = 32 to y = 58; one at about x = 488 to x = 548, y = 183 to "
        "y = 212): exactly as in image 1, each its own small closed shape.",
        "THE SPEAR-BLADE (about x = 355 to x = 1002, y = 455 to y = 915): the whole two-part weapon as ONE closed shape, WITHOUT the "
        "gauntlet and its knuckles in front of it: the broad dark stone slab with its orange cracks at the upper left (from its back "
        "end at about x = 355, y = 470), continuing straight down-right behind where the gauntlet was, then a short dark stone collar "
        "(about x = 650 to x = 720, y = 650 to y = 720) where the slab joins the orange magma-crystal spike with its yellow middle line, "
        "the spike reaching its sharp point at about x = 1000, y = 913. Keep the slab and the spike exactly as in image 1 where they "
        "are visible.",
    ],
    "C": [
        "THE GAUNTLET (about x = 505 to x = 752, y = 590 to y = 795): the big dark stone block of the near forearm and fist with its "
        "Y-shaped orange lava crack, WITHOUT the rounded knob on its top (where the knob covers it, draw the flat top edge of the "
        "block at about y = 600) and WITHOUT the round knuckle lumps under it (close its bottom with a straight rounded edge at about "
        "y = 790). One closed shape.",
        "THE SHIELD (about x = 995 to x = 1192, y = 420 to y = 882): the thick dark stone heater shield with its darker thickness band "
        "on the left, its bevelled rim and its branching orange lava crack, WITHOUT the knuckles of the fist in front of it: draw its "
        "face complete where the fist covered it (the rim and the crack continue).",
        "THE NEAR HORN (about x = 700 to x = 792, y = 238 to y = 432): the dark horn with its orange crack, complete, its base closed "
        "with a rounded edge (no head).",
        "THE NEAR EYE (about x = 748 to x = 847, y = 488 to y = 572) and THE FAR EYE (about x = 918 to x = 972, y = 484 to y = 562): "
        "the two yellow half-moon eyes with their ink outlines, exactly as in image 1, each its own closed shape.",
        "THE MOUTH (about x = 813 to x = 948, y = 573 to y = 622): the zigzag ink line with its two white fangs, exactly as in image 1.",
    ],
    "D": [
        "THE FAR HORN (about x = 905 to x = 1047, y = 238 to y = 448): the dark horn that curves out to the right and up, with its "
        "orange crack, complete, its base closed with a rounded edge (no head).",
        "THE FAR ARM (about x = 935 to x = 1060, y = 560 to y = 705): the short chubby red-brown arm (same skin colour as the body) "
        "that is hidden behind the shield and the fist in image 1: draw it complete as a short thick rounded sausage, from its "
        "shoulder end at about x = 945, y = 590 (round end) bending to its wrist end at about x = 1040, y = 650 (round end). No hand.",
        "THE SHOULDER KNOB (about x = 593 to x = 718, y = 543 to y = 618): the rounded dark stone block on top of the gauntlet, "
        "complete (its lower edge closed and rounded).",
        "THE NEAR FOOT (about x = 543 to x = 703, y = 800 to y = 868): the lowest row of chunky dark stone lumps at the bottom left, "
        "under the gauntlet's knuckles, as ONE closed cluster of three lumps joined together, its top closed with a rounded edge "
        "where the knuckles covered it.",
        "THE FAR FOOT (about x = 850 to x = 975, y = 715 to y = 862): the dark stone lump at the lower middle right, behind the "
        "spear-blade, complete as one chunky rounded stone boot (draw its part hidden by the blade).",
    ],
    "E": [
        "THE FAR FIST (about x = 980 to x = 1062, y = 528 to y = 702): the stack of chunky dark stone knuckles that grips the shield, "
        "as ONE closed shape (the knuckles joined, their separating ink lines kept inside), WITHOUT the shield behind it.",
        "THE NEAR KNUCKLES (about x = 553 to x = 712, y = 735 to y = 808): the row of round dark stone knuckle lumps under the "
        "gauntlet, as ONE closed cluster (the lumps joined, separating lines kept inside), complete where the gauntlet covers their "
        "tops (rounded top edge at about y = 735).",
        "THE CLOSED EYES, NEAR (at about x = 748 to x = 847, y = 515 to y = 560) and FAR (at about x = 918 to x = 972, y = 512 to "
        "y = 555): in place of each open eye, a closed eye drawn as one thick dark-brown ink stroke bent like an upside-down U (a "
        "squeezed-shut eye), about as wide as the open eye. Two separate strokes, nothing else around them.",
    ],
    # lượt sửa: tờ C vẽ găng tay thấp hơn concept ~30 px và vuông góc cạnh, núm vai lơ lửng như hạt đậu rời → găng + núm MỘT mảnh
    "F": [
        "THE GAUNTLET WITH ITS SHOULDER KNOB, as ONE piece (about x = 498 to x = 745, y = 540 to y = 802). Copy the EXACT outline of "
        "image 1, do not straighten it, do not make it boxy or octagonal: the big dark stone block of the near forearm and fist is a "
        "rounded, slightly leaning lump (its left side at about x = 500 around y = 700, its rounded top-right corner at about "
        "(738, 625), its right side at about x = 742 down to y = 760) with its Y-shaped orange lava crack exactly where it is in "
        "image 1; the rounded dark stone KNOB (about x = 582 to x = 715, y = 542 to y = 628) sits ON TOP of the block's upper edge, "
        "overlapping it, with its own ink outline exactly as in image 1. WITHOUT the round knuckle lumps under the block: close the "
        "block's bottom with a rounded edge at about y = 800, continuing its left and right sides. WITHOUT the spear-blade behind it "
        "and the body. The knob and the block together form one closed shape.",
    ],
    # lượt sửa (người dùng 2026-11-13: "chân ở animation này cũng bị hở không nối với cơ thể"): chân gần lệch ra ngoài đáy thân, giơ găng là lộ
    "G": [
        "THE NEAR LEG (hidden in image 1 behind the gauntlet and the spear-blade): draw ONE short, thick, stubby leg of the SAME "
        "brick red-brown stone skin as the body (#7C4238), like the chubby leg of a toddler monster, going from the underside of the "
        "body down-left to the near foot: its upper end is a rounded end centred at about x = 700, y = 745 (this end will be hidden "
        "under the body), its lower end a rounded end centred at about x = 622, y = 830 (hidden inside the dark stone foot); about "
        "78 px thick all along, slightly curved, one closed ink outline all the way around, crayon hatching like the body. Nothing "
        "else on the canvas: no body, no foot, no gauntlet, no spear.",
    ],
}


def build_manh():
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    if not os.path.exists(duyet):
        raise SystemExit("chưa có concept duyệt: " + Wp(duyet))
    head = (f"image 1 = {Wp(duyet)}: the APPROVED picture of the creature, 1536x1024, white background: a chubby LAVA IMP facing "
            "right: a living fire on its head, two dark cracked horns, a round brick red-brown stone body with a lighter belly patch "
            "and three dark spots, yellow half-moon eyes, a zigzag mouth with two fangs, a huge dark stone gauntlet with orange lava "
            "cracks gripping a two-part spear-blade (a dark cracked stone slab at the upper left and an orange magma-crystal spike "
            "pointing to the lower right), a short far arm whose fist of stacked dark knuckles holds a thick dark stone shield, and "
            "dark stone lumps for feet.")
    rule = ("TASK: redraw image 1, but keep ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the "
            "SAME SIZE as in image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE "
            "everything else and leave pure white (#FFFFFF) there. Every kept part must be ONE COMPLETE CLOSED SHAPE with the "
            "dark-brown ink outline running all the way around it: where a part is hidden behind another part in image 1, DRAW the "
            "hidden portion as described. The kept parts must NOT touch each other: clear white between them. Same wobbly ink line, "
            "same line thickness, same colours, same crayon hatching, same completely flat colouring as image 1. Do not add anything: "
            "no shadows, no glow, no sparks, no labels. Coordinates are pixels on the 1536x1024 canvas (x from the left, y from the top).")
    tail = ["", FLAT, BG]
    ra = []
    chi = sys.argv[2:] if len(sys.argv) > 2 else None
    for ten, ds in TO_MANH.items():
        if chi and ten not in chi:
            continue
        out = os.path.join(save_dir(), f"M_{ten}.png")
        p = os.path.join(pk(), f"luot_2_manh_{ten}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", head, "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ten}_2.png, M_{ten}_3.png ... in the same folder. Do not edit, move "
             "or delete any other file.", "", rule, "", "KEEP:"]
        t += [f"{i}. {d}" for i, d in enumerate(ds, 1)]
        ghi(p, t + tail)
        ra.append(p)
        print(p)
    return ra


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "1b":
        build_1b()
    elif len(sys.argv) > 1 and sys.argv[1] == "manh":
        build_manh()
    else:
        main()
