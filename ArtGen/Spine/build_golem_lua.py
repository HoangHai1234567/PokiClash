# -*- coding: utf-8 -*-
"""Gói GPT vẽ golem lõi lửa (mã làm việc golem_lua, con gốc của rig: monster_3422). Tướng thứ 4 đảo Hỏa.

Người dùng (2026-11-13): "concept như trong hình, kiểu golem đi bằng 2 chân có lõi lửa, lửa thoát ra từ các lỗ trên người (gai đỏ đổi
thành lửa)". appear: lõi lửa hiện trước, các part còn lại bay vào theo đường vòng cung ráp thành con; idle, run giống con gốc; đánh thường
giống skill_01 (lao tới vả tay từ trên xuống đầu đối thủ); cast hơi cúi người há to mồm phun lửa, rung người, impact mạnh; chiêu cuối giống
skill_03 (nhảy lên co người thành quả cầu, gai lửa dài hơn, xoay nhanh tại chỗ, phần lao vào nảy ra làm bằng code); die lõi tắt, các bộ
phận rơi xuống. Ba hướng chất liệu là ĐỀ XUẤT của Claude, chờ người dùng chọn. Chỉ lấy của con gốc cách dựng (chỗ, cỡ, thứ tự chồng
từng part); hình là của mình. Không đính ảnh con gốc; đính sơ đồ bố cục tự dựng bằng mã (golem_lua_bo_cuc.py).

    py -3 -I ArtGen/Spine/golem_lua_bo_cuc.py all
    py -3 -I ArtGen/Spine/build_golem_lua.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/golem_lua_1/luot_1_concept_<hướng>.txt [--note "..."]
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "golem_lua"
K = 1
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
KIEM_SI = os.path.join(HERE, "inbox", "kiem_si_1", "tai_ve", "L1_duyet.png")
MAT_LUA = os.path.join(HERE, "inbox", "mat_lua_1", "tai_ve", "L1_duyet.png")


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


STANCE = ("STANCE (the same as in the layout guide, image 1): a heavy, hunched STONE GOLEM standing on two short stubby legs, seen "
          "slightly from its left side, FACING THE VIEWER'S RIGHT. A huge rounded mass of thick stone plates forms its back and "
          "shoulders; its small skull-like stone face sits LOW at the FRONT (right), tucked under a heavy brow plate; two long heavy "
          "arms hang down to the ground and end in huge rounded clawed stone hands (the near hand at the lower left, the far hand at "
          "the lower right). Inside its chest burns a round FIRE CORE, and FLAMES burst out of round holes on its body (where a "
          "golem would have spikes). Fierce, determined, ready to fight: the brow plate comes down low over the eye. Chunky and "
          "appealing like a first-stage monster-collecting game creature, NOT a cute smiling mascot, NOT horror, NOT a robot, NOT "
          "a human.")

BODY = (
    "- THE BACK (the biggest piece, about {lung}): one huge rounded thick stone slab forming the hunched back, like a big boulder; "
    "on top of it, near the front, a smaller rounded top plate (about {dinh_dau}).\n"
    "- THE NEAR SHOULDER (about {vai_gan}, at the upper left): a big round boulder-like shoulder plate, with a second plate peeking "
    "out behind it at its left (about {vai_gan_sau}). On its face sits a thick round RING of {phu_ten} (about {vong_vai}) around a "
    "dark round hole.\n"
    "- FLAME JETS (instead of spikes; each one bursts OUT of a dark round hole or socket on the body, the hole edged by a thick "
    "ring or collar of {phu_ten}): {lua_ds} "
    "Draw every flame like a real hand-drawn fire jet, NOT like a spike, horn, crystal or leaf: a thick rounded base coming out of "
    "the hole, a body that bends in a soft S-curve along the direction given, and a sharp tip that curls a little upward and BACK "
    "(toward the viewer's left); one or two small side licks; three nested flat colour zones (red-orange {lua0} outside, orange "
    "{lua1}, yellow {lua2} inside near the base).\n"
    "- THE HEAD (about {dau}): a small skull-like stone FACE MASK turned three-quarters to the right, low at the front of the body; "
    "the face is at its lower right. ONE small round EYE socket (centre about {mat}, radius about {mat_r}) rimmed in {phu_ten}, "
    "with a glowing round yellow eye ({lua2}) and a small dark pupil looking right; no second eye (the other eye is hidden). Below "
    "the face a separate LOWER JAW block of {phu_ten} (about {ham}) with a stepped, notched lower edge; between the face and the "
    "jaw a glimpse of the glowing orange throat ({lua1}, about {mieng}). No nose, no ears, no teeth showing, no smile.\n"
    "- THE BROW (about {may}): a heavy angular stone brow plate like a helmet visor, coming down over the face to just above the "
    "eye (a frowning look), with one carved groove line; behind it a long blade-shaped cheek plate sweeping down to the left "
    "(about {may2}), also with one groove line.\n"
    "- THE CHEST AND THE FIRE CORE: the front of the body is a thick curved stone SHELL shaped like a big letter C (about "
    "{vo_nguc}) that wraps around a hollow round chest; through the opening of the C, on the right, between the shell and the jaw, "
    "the FIRE CORE shows (the core is a round ball of fire about {loi}, centre about {loi_tam}): flat concentric zones of fire, "
    "red-orange ({lua0}) outside, orange ({lua1}) and a bright yellow ({lua2}) round heart ball at the centre; the borders between "
    "the zones are wavy like flame tongues. Left of the shell a big stone chest block (about {nguc_trai}); right of the core, under "
    "the jaw, a narrow stone plate (about {nguc_phai}).\n"
    "- THE ARMS: the NEAR arm (about {tay_gan}) is a dark wrist block of {phu_ten} with a small flame jet on top, then a HUGE "
    "rounded stone hand like a big paw with one carved groove line and THREE big curved claws ({vuot_ten}) at its bottom touching "
    "the ground. The FAR arm (about {tay_xa}) is the same, a little smaller, behind the body at the lower right, its claws pointing "
    "down-right. A small dark band of {phu_ten} at each shoulder joint.\n"
    "- THE LEGS: two short stubby legs under the body (near leg about {chan_gan}, far leg about {chan_xa}): each is a stone thigh "
    "block, a round glowing LAVA KNEE ball (orange {lua1} with a yellow centre) and a small square stone foot. Several chunky stone "
    "hip blocks under the belly (about {hong}), with a small flame jet pointing down-forward between the legs.")

SIMPLE = ("VERY SIMPLE DESIGN, FEW DETAILS (very important): big clean chunky shapes, each stone plate ONE flat colour with at most "
          "ONE carved groove line; NO cracks, NO lava cracks, NO runes, NO glowing lines on the stone, NO rivets unless listed, NO "
          "moss, NO extra spikes, NO extra flames. The ONLY fire on the creature is: the flame jets listed above, the fire core in "
          "the chest, the two knee joints, the eye and the glimpse of the throat.")

FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the figure stands in the middle of the canvas: from the near hand at about "
         "x = {x0} to the tip of the forehead flame at about x = {x1}, and from the tip of the tallest flame at about y = {y0} to "
         "the bottom of the feet and claws at about y = {y1}. Do NOT enlarge, shrink or move the figure.")

POSE = ("ANIMATION-READY (very important: the picture will be cut into separate pieces and animated with a 2D skeleton; the stone "
        "pieces will fly apart and come back together): calm, clean resting pose exactly as in the guide. Draw every piece as a "
        "clear, simple, closed shape with its own complete ink outline, so that the pieces can be separated: each stone plate, "
        "each ring, each flame jet, the core, the face, the jaw, each hand, each claw, each leg part. The pieces touch or overlap "
        "but are NOT melted into one blob. No sparks, no embers, no smoke, no glow, no speed lines, no ground, no lava puddle, no "
        "props, no weapon, no second character.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram: take ONLY the placement, the sizes, the overlaps and the kind of colour of each "
        "piece from it, never its line, its blob edges or its exact shapes. Design the real shape of every piece yourself as "
        "described: bold, chunky, readable shapes with a clear silhouette and clean bevelled stone blocks, the way a carefully "
        "designed Pokemon-like rock monster is drawn. Do NOT copy any existing character.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 5 px thick on this canvas around every big piece, and about 3 px for small "
        "details (groove lines, the pupil); every area coloured with coloured pencils and wax crayons, the strokes visible as loose "
        "diagonal hatching (strokes thinner than the outline), kept inside the outline. Clean and appealing, neither a crude "
        "scribble nor an over-rendered painting.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker underside, no shadows of any kind (no cast shadow of a plate on another, no shadow "
        "under the figure or on the background), no white highlights or shine spots (only the tiny dot in the eye), no gloss, no "
        "reflections, NO GLOW around the fire, the core or the eye, no halo, no rim light, no gradients, no 3D look. The fire looks "
        "hot only because its flat colours are bright.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no effects around the "
      "character.")

LUA = ("#E0441F", "#F7902A", "#FFD45A")
D = {
    "da_tro": dict(
        ten="đá tro núi lửa xám kem, mảng phụ (vòng lỗ lửa, cổ tay, hàm) than chì, vuốt đen than",
        phu_ten="dark charcoal stone (#3F3B46)", vuot_ten="charcoal black, #2E2A30",
        palette=("COLOURS (use exactly these, each area one flat colour): every stone plate, the face, the hands, the legs warm "
                 "pale ash-grey volcanic stone (#B2A79A), groove lines a slightly darker grey (#928678) with ink; the rings, hole "
                 "collars, wrist blocks, jaw and small bands dark charcoal (#3F3B46); the claws charcoal black (#2E2A30); the flames, "
                 "the core, the knees, the throat red-orange (#E0441F) / orange (#F7902A) / yellow (#FFD45A); the eye yellow "
                 "(#FFD45A) with a dark pupil; every outline dark-brown ink (#2B2118). Only these colours: NO blue, NO green, NO "
                 "purple, NO pink."),
        check=["Đá **xám tro sáng** ấm, mảng phụ (vòng quanh lỗ lửa, cổ tay, hàm) **than chì**, vuốt đen than."]),
    "sat_lo": dict(
        ten="sắt lò rèn xám xanh có ít đinh tán, mảng phụ đồng thau, vuốt sắt đen",
        phu_ten="dull bronze-brass metal (#B57438)", vuot_ten="black iron, #2C2D33",
        palette=("COLOURS (use exactly these, each area one flat colour): every plate, the face mask, the hands, the legs dark "
                 "blue-grey cast iron (#5C616C), groove lines darker iron (#454A54) with ink, and on the three biggest plates (the "
                 "back, the near shoulder, the near hand) two or three round rivets (#454A54 with an ink outline); the rings, hole "
                 "collars, wrist blocks, jaw and small bands dull bronze-brass (#B57438); the claws black iron (#2C2D33); the flames, "
                 "the core, the knees, the throat red-orange (#E0441F) / orange (#F7902A) / yellow (#FFD45A); the eye yellow "
                 "(#FFD45A) with a dark pupil; every outline dark-brown ink (#2B2118). It is a living furnace golem: the plates are "
                 "thick forged iron blocks, NOT a robot (no screws, no pipes, no gears, no machinery). Only these colours: NO green, "
                 "NO purple, NO pink."),
        check=["**Sắt lò rèn xám xanh**, vài đinh tán trên ba tấm lớn nhất; mảng phụ **đồng thau**; không ra người máy (không ống, bánh răng, ốc vít)."]),
    "da_cat": dict(
        ten="đá sa thạch vàng cát, mảng phụ nâu than, vuốt nâu đen",
        phu_ten="dark brown-charcoal stone (#4A3A36)", vuot_ten="dark brown-black, #2E2622",
        palette=("COLOURS (use exactly these, each area one flat colour): every stone plate, the face, the hands, the legs warm "
                 "sandstone yellow-beige (#C9AE84), groove lines a darker sand (#A88E66) with ink; the rings, hole collars, wrist "
                 "blocks, jaw and small bands dark brown-charcoal (#4A3A36); the claws dark brown-black (#2E2622); the flames, the "
                 "core, the knees, the throat red-orange (#E0441F) / orange (#F7902A) / yellow (#FFD45A); the eye yellow (#FFD45A) "
                 "with a dark pupil; every outline dark-brown ink (#2B2118). Only these colours: NO blue, NO green, NO purple, NO "
                 "pink."),
        check=["Đá **sa thạch vàng cát**, mảng phụ **nâu than**, vuốt nâu đen."]),
}

TEN_LUA = [  # (slot, mô tả tiếng Anh)
    ("P_jianci9", "the BIGGEST flame bursts out of the ring on the near shoulder: base about {goc}, it shoots up and back to the "
                  "upper LEFT, its tip at about {ngon}"),
    ("P_jianci16", "a TALL flame bursts out of a ring on the top of the back: base about {goc}, straight up, its tip at about {ngon}"),
    ("P_jianci14", "a small flame out of a small hole on the top plate: base about {goc}, up, tip about {ngon}"),
    ("P_jianci13", "a small flame out of a hole on the back of the head: base about {goc}, up and to the right, tip about {ngon}"),
    ("P_jiao3", "a flame out of a socket on the FOREHEAD (where a horn would be): base about {goc}, it shoots forward to the RIGHT "
                "and a little up, its tip at about {ngon}"),
    ("P_yuanzhui1", "a small flame out of a hole on the near elbow: base about {goc}, down-left, tip about {ngon}"),
    ("P_shouR1", "a small flame out of the top of the near wrist block: base about {goc}, up-left, tip about {ngon}"),
    ("P_kua3", "a small flame out of a hole on the round hip block between the legs: base about {goc}, toward {ngon}"),
]

CHECK_CHUNG = [
    "Bố cục y sơ đồ: golem gù nhìn sang **phải**, mặt nạ đầu lâu nhỏ nằm **thấp phía trước** dưới tấm mày; **một mắt**; hàm dưới là khối riêng.",
    "Mọi gai đỏ của con gốc thành **lưỡi lửa thật** phụt ra từ lỗ có vòng viền (to nhất ở vai gần, cao nhất trên lưng, một lưỡi ở trán chĩa ra trước), "
    "gốc dày, uốn chữ S, ngọn móc về sau; không phải gai, sừng, pha lê.",
    "**Lõi lửa** tròn ba vùng màu lộ qua khe vỏ ngực hình chữ C; hai **gối dung nham**; họng lửa lộ chút giữa mặt và hàm.",
    "Đi bằng **hai chân ngắn** (đùi, gối dung nham, bàn chân vuông); hai tay dài, bàn tay đá to tròn **ba vuốt** chạm đất.",
    "Ít chi tiết: mỗi tấm một màu, nhiều nhất một rãnh; không vết nứt, không hoa văn, không lửa thừa.",
    "Tô phẳng, không bóng, **không quầng sáng** quanh lửa và lõi; nét bút nâu rung, vân sáp; nền trắng.",
]

FIX = [
    ("Lửa thành gai / sừng / pha lê", "Every flame must look like a real flame jet: thick round base out of a hole, S-curved body, tip curling back to the left, three nested flat colours. Not spikes, horns or crystals."),
    ("Có quầng sáng / tia lửa bay", "Remove every glow, halo, spark and ember. Flat colours only."),
    ("Mặt ở giữa / nhìn thẳng / hai mắt", "ONE small round eye on the skull-like face low at the FRONT RIGHT, looking right, exactly as in the layout guide; the brow plate comes down just above it."),
    ("Thêm vết nứt / hoa văn", "Remove all cracks, runes and ornaments: each stone plate one flat colour with at most one groove line."),
    ("Các tấm dính liền một khối", "Every stone plate is a separate thick block with its own complete ink outline."),
    ("Có bóng đổ / tô khối", "Flat colour only: no shading, no cast shadow, no highlights."),
]


def refs(kieu):
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature in its resting stance, built "
         "from rough coloured blobs: where every piece goes on the canvas, how big it is and which piece overlaps which (stone "
         "plates; flame shapes coming out of dark rings and holes; the round fire core showing in the chest opening; the small "
         "face with one eye low at the front right; two clawed hands on the ground; two short legs with orange knees). Use it for "
         "placement, size and overlap only; design and redraw everything in the hand-drawn style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng) ở dáng nghỉ của rig: các tấm đá, lưỡi lửa phụt từ vòng lỗ, lõi lửa lộ "
         "ở khe ngực, mặt nhỏ một mắt thấp phía trước bên phải, hai bàn tay vuốt chạm đất, hai chân ngắn gối cam. Lấy chỗ đặt, cỡ, thứ "
         "tự chồng"),
        (KIEM_SI,
         "an approved hero of the same game (an armoured monkey samurai), 1536x1024, white background: match EXACTLY its wobbly "
         "dark-brown pen line, its visible crayon hatching, its completely flat colouring, its bold chunky shapes and its fierce "
         "battle-ready attitude. Do NOT copy its species, its design or its colours.",
         "Voọc Tướng đã duyệt (1536 × 1024, nền trắng): khỉ samurai giáp lục. Lấy nét bút rung, vân sáp, tô phẳng, thần thái chiến"),
        (MAT_LUA,
         "another approved hero of the same game, a fire-element hero made of stone plates around a ball of fire, 1536x1024, white "
         "background: see how its fire and its stone plates are drawn (flat colour zones, wobbly ink, crayon hatching, no glow). "
         "Do NOT copy its design, its eye, its cracks or its colours.",
         "Mắt lửa bọc giáp (tướng 2 đảo Hỏa, đã duyệt; 1536 × 1024, nền trắng): lấy cách vẽ lửa, tấm đá"),
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
    x0, y0, x1, y1 = B["_khung"]
    gd = [f"# Gói gửi GPT: `{CODE}` (golem lõi lửa, tướng thứ 4 đảo Hỏa, tên chưa đặt)", "",
          "Làm 2026-11-13: dựng trên rig của con gốc `monster_3422` (golem đá gù đi hai chân, gai đỏ, lõi đỏ giữa ngực). Ba hướng chất "
          "liệu là đề xuất của Claude, chờ người dùng chọn và duyệt concept. Ghi chú: `ArtGen/Spine/inbox/golem_lua_ghichu.md`.",
          "", "Lượt mảnh chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    lua_ds = " ".join(f"({i}) " + s.format(goc=pt(B["lua"][sl]["goc"]), ngon=pt(B["lua"][sl]["ngon"])) + ";"
                      for i, (sl, s) in enumerate(TEN_LUA, 1) if sl in B["lua"])
    ra = []
    for kieu, d in D.items():
        R = refs(kieu)
        missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
        if missing:
            raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
        out = os.path.join(save_dir(), f"L1_{kieu}.png")
        p = os.path.join(pk(), f"luot_1_concept_{kieu}.txt")
        body = BODY.format(
            lung=xy(B["lung"]), dinh_dau=xy(B["dinh_dau"]), vai_gan=xy(B["vai_gan"]), vai_gan_sau=xy(B["vai_gan_sau"]),
            vong_vai=xy(B["vong_vai"]), phu_ten=d["phu_ten"], lua_ds=lua_ds, lua0=LUA[0], lua1=LUA[1], lua2=LUA[2],
            dau=xy(B["dau"]), mat=pt(B["mat_tam"]), mat_r=B["mat_tam"][2], ham=xy(B["ham"]), mieng=xy(B["mieng"]),
            may=xy(B["may"]), may2=xy(B["may2"]), vo_nguc=xy(B["vo_nguc"]), loi=xy(B["loi"]), loi_tam=pt(B["loi_tam"]),
            nguc_trai=xy(B["nguc_trai"]), nguc_phai=xy(B["nguc_phai"]), tay_gan=xy(B["tay_gan"]), tay_xa=xy(B["tay_xa"]),
            vuot_ten=d["vuot_ten"], chan_gan=xy(B["chan_gan"]), chan_xa=xy(B["chan_xa"]), hong=xy(B["hong"]))
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "",
              "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
              "approved hero images.", "",
              "CREATURE: a FIRE-CORE GOLEM, a fire-element hero of the volcano island in a monster-collecting game: a hunched "
              "living stone golem built from thick separate stone blocks, walking on two short legs, with a burning fire core in "
              "its chest and flames bursting out of holes in its body. It is a creature (an elemental monster pet), NOT a robot, "
              "NOT a human, NOT a statue.", "",
              STANCE, "",
              "Follow the LAYOUT GUIDE (image 1) for WHERE every piece is on the canvas, HOW BIG it is and WHICH piece overlaps "
              "which. Coordinates below are pixels on the 1536x1024 canvas (x from the left, y from the top). NEAR = the side of "
              "the body toward the viewer (the viewer's left); FAR = the other side (the viewer's right).", "",
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
    gd += ["Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/golem_lua_bo_cuc.py all`).",
           "", "## Kiểm chung", ""]
    gd += [f"- {c}" for c in CHECK_CHUNG]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    ghi(os.path.join(pk(), "HUONG_DAN.md"), gd)
    for p in ra:
        print(p)


if __name__ == "__main__":
    main()
