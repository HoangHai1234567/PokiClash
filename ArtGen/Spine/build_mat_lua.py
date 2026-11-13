# -*- coding: utf-8 -*-
"""Gói GPT vẽ mắt lửa bọc giáp (mã làm việc mat_lua, con gốc của rig: monster_3342). Tướng thứ 2 đảo Hỏa.

Người dùng (2026-11-13): "tướng thứ 2 đảo hỏa, concept flaming fire eyeball có tay chân và bọc giáp". appear: bộ giáp đá nằm đất, mắt
sáng lên, phồng lên, tay trồi ra rồi bay lên; idle, walk gần như con gốc; đánh thường bay tới đấm một phát nặng; cast giống skill_02 thêm
tia lửa bắn từ giữa mắt; chiêu cuối dang hai tay xoay chong chóng quanh thân rồi lao vào đập liên tục; die rơi xuống, mắt tắt, giáp rơi.
Ba hướng giáp dưới đây là ĐỀ XUẤT của Claude, chờ người dùng chọn. Chỉ lấy của con gốc cách dựng (chỗ đặt, cỡ, thứ tự chồng từng part);
hình là của mình. Không đính ảnh con gốc; đính sơ đồ bố cục tự dựng bằng mã (mat_lua_bo_cuc.py).

    py -3 -I ArtGen/Spine/mat_lua_bo_cuc.py all
    py -3 -I ArtGen/Spine/build_mat_lua.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/mat_lua_1/luot_1_concept_<hướng>.txt [--note "..."]
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "mat_lua"
K = 1
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
KIEM_SI = os.path.join(HERE, "inbox", "kiem_si_1", "tai_ve", "L1_duyet.png")
QUY_LAVA = os.path.join(HERE, "inbox", "quy_lava_1", "tai_ve", "L1_da_nung.png")


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


STANCE = ("STANCE (the same as in the layout guide, image 1): a heavy, compact armoured creature resting low on the ground, "
          "seen slightly from its left side, FACING THE VIEWER'S RIGHT. Its body is ONE big round ball of living fire with ONE huge "
          "eye on the RIGHT part of the ball (the eye looks to the right, toward the enemy). Thick separate armour plates hug the "
          "ball on top, on the shoulders and underneath; two short stubby arms end in two huge armoured fists that rest on the "
          "ground at the left and at the right like heavy feet. Fierce, determined, ready to punch: the big top plate comes down "
          "diagonally over the top of the eye like a frowning brow. Appealing and chunky like a first-stage monster-collecting game "
          "creature, NOT a cute smiling mascot, NOT horror (no veins, no blood, no gore).")

BODY = (
    "- THE FIRE EYEBALL (the heart of the creature, about {cau}, centre about ({cx}, {cy}), radius about {r}): a perfect round ball "
    "made of LIVING FIRE, drawn as flat colour zones like a hand-drawn fire, NOT a glossy sphere: the outer part red-orange "
    "({lua0}), a wide band of orange ({lua1}) inside it, and a yellow zone ({lua2}) around the eye; the borders between the zones "
    "are wavy flame-shaped lines (like flame tongues curling around the ball), not perfect circles.\n"
    "- THE EYE (about {mat}): one HUGE eye that fills the right part of the ball: a round iris of hot pale yellow ({trong}) with a "
    "thick ink outline, and in it a tall vertical SLIT pupil ({nguoi}) like a dragon's eye, a little shorter than the iris. Its "
    "top is covered by the edge of the big top armour plate, so the eye looks narrowed and angry. A tiny round white dot of light "
    "may sit at the top of the pupil. No eyelashes, no eyelids, no mouth, no nose, no ears, no second eye.\n"
    "- FLAMES LICKING OUT (about {lua}, behind everything): the fire of the ball escapes through the gaps between the armour plates "
    "as FIVE to SEVEN big FLAME TONGUES: the biggest ones rise from the top and the back-top of the ball (the tallest tip reaching "
    "about y = {lua_top}), smaller ones lick out at the back (left) and between the plates at the sides. Draw them like a real "
    "campfire flame drawn by hand, NOT like spikes, horns or hair: every tongue is thick and round at its base, bends in a soft "
    "S-curve and tapers to a sharp tip that HOOKS backward to the viewer's LEFT and upward; the tongues have different heights, "
    "their edges have a few C-shaped bites and small side licks near the tips; the same three nested flat colour zones as the "
    "ball (red-orange outside, orange, yellow core near the base). The flames sit BEHIND the armour plates and merge into the ball.\n"
    "- TOP PLATE (the helmet, about {mu}): the biggest armour plate, a long thick slab {giap_ten} lying across the top of the ball "
    "from the back-left to the front-right and bending DOWN over the top of the eye at the right end like a heavy frowning brow; "
    "{chi_tiet}.\n"
    "- SMALL PLATES: one small chunky plate stuck on the ball just left of the eye (about {nho_mat}), and one small plate tucked "
    "under the right end of the top plate (about {nho_phai}); the same material.\n"
    "- SHOULDER PLATES: the NEAR shoulder plate (about {vai_gan}) is a tall thick slab leaning back at the left of the ball, its "
    "pointed top up at the upper left; the FAR shoulder plate (about {vai_xa}) is a tall narrow slab standing at the upper right, "
    "behind the right end of the top plate. Both are the same material, with {chi_tiet2}.\n"
    "- LOWER PLATES: three curved thick plates cradle the bottom of the ball like a broken shell: one at the lower left (about "
    "{duoi_trai}), one long one across the bottom middle (about {duoi_giua}), one at the lower right under the eye (about "
    "{duoi_phai}); the yellow-orange fire of the ball shows in the gaps between them.\n"
    "- ARMS: two short stubby arms made of the same fire, each only a small rounded flame-coloured stub ({tay_mau}) joining the "
    "ball to a fist: the near arm at the left (about {tay_gan}), the far arm at the right (about {tay_xa}).\n"
    "- FISTS (they are also the creature's feet): two HUGE heavy armoured fists standing on the ground, each one chunky rounded "
    "block like an armoured boxing glove made of {nam_ten}, with three or four big knuckle bumps on top: the NEAR fist at the lower "
    "left (about {nam_gan}), the FAR fist at the lower right (about {nam_xa}), a little smaller.")

FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the figure stands in the middle of the canvas: from the near fist at about "
         "x = {x0} to the far fist at about x = {x1}, and from the tip of the tallest flame at about y = {y0} to the bottom of the "
         "fists at about y = {y1}. Do NOT enlarge, shrink or move the figure.")

POSE = ("ANIMATION-READY (very important: the picture will be cut into separate pieces and animated with a 2D skeleton; the armour "
        "plates will fly apart and come back): calm, clean resting pose exactly as in the guide. Draw every piece as a clear, "
        "simple, closed shape with its own complete ink outline, so that the pieces can be separated: flames / fire ball / eye / "
        "top plate / each small plate / each shoulder plate / each lower plate / each arm stub / each fist. The plates touch or "
        "overlap the ball but are NOT melted into it. No sparks, no embers, no smoke, no glow, no speed lines, no ground, no lava "
        "puddle, no props, no weapon, no second character.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram: take ONLY the placement, the sizes, the overlaps and the kind of colour of each "
        "piece from it, never its line, its jagged edge noise or its exact blob shapes. Design the real shape of every piece "
        "yourself as described: bold, chunky, readable shapes with a clear silhouette, clean bevelled plates, the way a carefully "
        "designed first-stage Pokemon-like monster is drawn (compact, chunky, one big expressive eye, few but clear details). Do "
        "NOT copy any existing character.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 5 px thick on this canvas around every big piece, and about 3 px for small "
        "details (cracks, bevel lines, rivets, the pupil); every area coloured with coloured pencils and wax crayons, the strokes "
        "visible as loose diagonal hatching (strokes thinner than the outline), kept inside the outline. Clean and appealing, "
        "neither a crude scribble nor an over-rendered painting.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker underside, no shadows of any kind (no cast shadow of a plate on the ball, no shadow "
        "under the figure or on the background), no white highlights or shine spots on the plates or the fists (only the tiny dot "
        "in the eye), no gloss, no reflections, NO GLOW around the fire or the eye, no halo, no rim light, no gradients, no 3D "
        "look. The fire looks hot only because its flat colours are bright.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no effects around the "
      "character.")

D = {
    "da_den": dict(
        ten="giáp đá vỏ chai (obsidian) đen tím, vết nứt dung nham đỏ cam mảnh; cầu lửa đỏ cam, con ngươi đỏ sẫm",
        giap_ten="of black volcanic glass (obsidian, a very dark violet-black #343040)",
        chi_tiet="its flat faces separated by one or two clean bevel lines, and one thin branching lava crack (#EC5A2E) on its top face",
        chi_tiet2="a bevel line along their length and one thin lava crack (#EC5A2E)",
        nam_ten="the same black volcanic glass with a Y-shaped thin lava crack (#EC5A2E) on its face",
        lua=("#DC3A22", "#F48022", "#FFCE50"), trong="#FFECA0", nguoi="deep red, #96181E", tay_mau="red-orange #E8542C",
        palette=("COLOURS (use exactly these, each area one flat colour): every armour plate and both fists very dark violet-black "
                 "obsidian (#343040), bevel lines in ink; every lava crack red-orange (#EC5A2E); the fire ball and the flames "
                 "red-orange (#DC3A22) / orange (#F48022) / yellow (#FFCE50); the iris pale hot yellow (#FFECA0); the slit pupil deep "
                 "red (#96181E); arm stubs red-orange (#E8542C); every outline dark-brown ink (#2B2118). Only these colours: NO "
                 "blue, NO green, NO pink, NO white areas."),
        check=["Giáp và nắm tay **đen tím** như đá vỏ chai, vết nứt dung nham mảnh đỏ cam; cầu lửa đỏ cam, con ngươi khe **đỏ sẫm**."]),
    "sat_ren": dict(
        ten="giáp sắt rèn xám than có đinh tán, mép trong nung cam; cầu lửa cam vàng, con ngươi khe đen nâu",
        giap_ten="of thick hand-forged IRON armour (a dark gunmetal grey #545660)",
        chi_tiet=("a row of three or four round rivets (#3E4046 with ink outline) along its edge, and a thin flat band of red-hot "
                  "metal (#FA8C2E) running along its lower inner edge where it touches the fire"),
        chi_tiet2="two or three round rivets and a thin red-hot band (#FA8C2E) along the edge facing the ball",
        nam_ten="the same forged iron, like a riveted iron gauntlet, the knuckle plates separated by ink lines, two rivets on the back",
        lua=("#EC5C1E", "#FCA028", "#FFDE6E"), trong="#FFF4BE", nguoi="very dark brown-black, #2E1E1E", tay_mau="orange #F6802A",
        palette=("COLOURS (use exactly these, each area one flat colour): every armour plate and both fists dark gunmetal iron "
                 "(#545660), rivets darker iron (#3E4046); the red-hot edge bands orange (#FA8C2E); the fire ball and the flames "
                 "orange-red (#EC5C1E) / orange (#FCA028) / yellow (#FFDE6E); the iris very pale hot yellow (#FFF4BE); the slit pupil "
                 "very dark brown-black (#2E1E1E); arm stubs orange (#F6802A); every outline dark-brown ink (#2B2118). Only these "
                 "colours: NO blue, NO green, NO purple, NO pink."),
        check=["Giáp và nắm tay **sắt rèn xám than**, có **đinh tán**, mép trong là dải kim loại nung cam phẳng (không phát sáng); "
               "cầu lửa cam vàng, con ngươi khe **đen nâu**."]),
    "tro_nui": dict(
        ten="giáp đá bọt xám tro sáng, vết nứt cam; cầu lửa đỏ cam, con ngươi đỏ sẫm",
        giap_ten="of light volcanic PUMICE stone (a warm pale ash grey #96908C)",
        chi_tiet="its flat faces separated by one or two clean bevel lines, three or four tiny round pores, and one branching orange lava crack (#F66826)",
        chi_tiet2="a bevel line along their length, a few tiny pores and one orange lava crack (#F66826)",
        nam_ten="the same pale ash-grey pumice with a Y-shaped orange lava crack (#F66826) on its face",
        lua=("#DC3A22", "#F48022", "#FFCE50"), trong="#FFEA96", nguoi="deep red, #8C161C", tay_mau="red-orange #E8542C",
        palette=("COLOURS (use exactly these, each area one flat colour): every armour plate and both fists warm pale ash grey "
                 "(#96908C), pores slightly darker grey (#7E7874); every lava crack orange (#F66826); the fire ball and the flames "
                 "red-orange (#DC3A22) / orange (#F48022) / yellow (#FFCE50); the iris pale hot yellow (#FFEA96); the slit pupil deep "
                 "red (#8C161C); arm stubs red-orange (#E8542C); every outline dark-brown ink (#2B2118). Only these colours: NO "
                 "blue, NO green, NO purple, NO pink."),
        check=["Giáp và nắm tay **xám tro sáng** như đá bọt, lỗ rỗ nhỏ, vết nứt cam; tương phản mạnh nhất với cầu lửa."]),
}

CHECK_CHUNG = [
    "Bố cục y sơ đồ: nhìn sang **phải**, **một con mắt to** ở phần bên phải quả cầu; tấm giáp đầu đè chéo lên mép trên con mắt như "
    "cặp mày cau (mặt \"chiến\").",
    "Thân là **một quả cầu lửa tròn** ba vùng màu phẳng (đỏ cam ngoài, cam, vàng quanh mắt), ranh giữa các vùng uốn như lưỡi lửa.",
    "Mắt: tròng vàng nhạt viền mực, **con ngươi khe dọc** như mắt rồng; không mi, không miệng, không mắt thứ hai.",
    "**Lưỡi lửa thật** liếm ra ở các khe giáp (to nhất ở đỉnh và sau đỉnh), gốc dày uốn chữ S, ngọn móc ngả về sau (sang trái); nằm SAU "
    "giáp; không phải gai, không phải sừng.",
    "Đủ mảnh, mỗi mảnh viền kín: tấm đầu, 2 tấm nhỏ, 2 tấm vai, 3 tấm dưới, 2 khúc tay lửa ngắn, **2 nắm tay giáp to chạm đất** (làm "
    "chân luôn).",
    "Tô phẳng, không bóng, **không quầng sáng** quanh lửa và mắt; nét bút nâu rung, vân sáp; nền trắng.",
]

FIX = [
    ("Lửa thành gai / sừng", "The flames must look like real flames: thick round bases, S-curved tongues, tips hooking back to the left, three nested colours, merged into the fire ball. Not spikes or horns."),
    ("Có quầng sáng / tia lửa bay", "Remove every glow, halo, spark and ember. Flat colours only."),
    ("Mắt ở giữa / nhìn thẳng / có hai mắt", "ONE huge eye on the RIGHT part of the fire ball, looking to the right, exactly as in the layout guide; the big top plate covers the top of the eye like a frowning brow."),
    ("Giáp dính liền vào quả cầu", "Every armour plate is a separate thick piece with its own complete ink outline, sitting on the fire ball, not melted into it."),
    ("Quả cầu bóng loáng 3D", "The fire ball is flat colour zones with wavy flame-shaped borders, no shading, no highlight, no gloss."),
    ("Có bóng đổ / tô khối", "Flat colour only: no shading, no cast shadow, no highlights."),
]


def refs(kieu):
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature in its resting stance, built "
         "from rough coloured blobs: where every piece goes on the canvas, how big it is and which piece overlaps which (big flame "
         "shapes rising behind everything; the round fire ball with concentric colour zones and one big pale eye with a slit pupil "
         "on its right part; the armour plates around the ball: one big top plate, two small plates, two tall shoulder plates, three "
         "lower plates; two short orange arm stubs; two big fists on the ground at the left and right). Use it for placement, size "
         "and overlap only; design and redraw everything in the hand-drawn style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng) ở dáng nghỉ của rig: khối lửa sau lưng, quả cầu lửa vòng màu đồng tâm, mắt "
         "to tròng nhạt con ngươi khe ở phần phải, các tấm giáp (đầu, 2 tấm nhỏ, 2 vai, 3 tấm dưới), 2 khúc tay cam, 2 nắm tay chạm đất. "
         "Lấy chỗ đặt, cỡ, thứ tự chồng"),
        (KIEM_SI,
         "an approved hero of the same game (an armoured monkey samurai), 1536x1024, white background: match EXACTLY its wobbly "
         "dark-brown pen line, its visible crayon hatching, its completely flat colouring, its bold chunky shapes and its fierce "
         "battle-ready attitude. Do NOT copy its species, its design or its colours.",
         "Voọc Tướng đã duyệt (1536 × 1024, nền trắng): khỉ samurai giáp lục. Lấy nét bút rung, vân sáp, tô phẳng, thần thái chiến"),
        (QUY_LAVA,
         "another approved hero of the same game, a fire-element first-stage hero, 1536x1024, white background: see how its fire, "
         "its dark stone pieces and its lava cracks are drawn (flat colour zones, wobbly ink, crayon hatching, no glow). Do NOT copy "
         "its design.",
         "Tiểu quỷ lava (tướng 1 đảo Hỏa, hướng người dùng đã chọn; 1536 × 1024, nền trắng): lấy cách vẽ lửa, đá, vết nứt"),
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
    allx = [B[k] for k in ("lua", "cau", "vai_gan", "vai_xa", "nam_gan", "nam_xa")]
    x0, y0 = min(b[0] for b in allx), min(b[1] for b in allx)
    x1, y1 = max(b[2] for b in allx), max(b[3] for b in allx)
    gd = [f"# Gói gửi GPT: `{CODE}` (mắt lửa bọc giáp, tướng thứ 2 đảo Hỏa, tên chưa đặt)", "",
          "Làm 2026-11-13: dựng trên rig của con gốc `monster_3342` (quả cầu dung nham một mắt trong bộ giáp đá lơ lửng, hai nắm tay "
          "đá). Ba hướng giáp là đề xuất của Claude, chờ người dùng chọn và duyệt concept. Ghi chú: `ArtGen/Spine/inbox/mat_lua_ghichu.md`.",
          "", "Lượt mảnh chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    ra = []
    for kieu, d in D.items():
        R = refs(kieu)
        missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
        if missing:
            raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
        out = os.path.join(save_dir(), f"L1_{kieu}.png")
        p = os.path.join(pk(), f"luot_1_concept_{kieu}.txt")
        ct = B["cau_tam"]
        body = BODY.format(
            cau=xy(B["cau"]), cx=ct[0], cy=ct[1], r=ct[2], lua0=d["lua"][0], lua1=d["lua"][1], lua2=d["lua"][2],
            mat=xy(B["mat"]), trong=d["trong"], nguoi=d["nguoi"], lua=xy(B["lua"]), lua_top=B["lua"][1],
            mu=xy(B["mu"]), giap_ten=d["giap_ten"], chi_tiet=d["chi_tiet"], chi_tiet2=d["chi_tiet2"],
            nho_mat=xy(B["giap_nho_mat"]), nho_phai=xy(B["giap_nho_phai"]), vai_gan=xy(B["vai_gan"]), vai_xa=xy(B["vai_xa"]),
            duoi_trai=xy(B["giap_duoi_trai"]), duoi_giua=xy(B["giap_duoi_giua"]), duoi_phai=xy(B["giap_duoi_phai"]),
            tay_mau=d["tay_mau"], tay_gan=xy(B["tay_gan"]), tay_xa=xy(B["tay_xa"]), nam_ten=d["nam_ten"],
            nam_gan=xy(B["nam_gan"]), nam_xa=xy(B["nam_xa"]))
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "",
              "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
              "approved hero images.", "",
              "CREATURE: an ARMOURED FIRE EYE, a fire-element hero of the volcano island in a monster-collecting game: a living ball "
              "of fire with one huge fierce eye, wearing a suit of thick separate armour plates, with two short fiery arms ending in "
              "two huge armoured fists that it also stands on. It is a creature (an elemental monster pet), NOT a human, NOT a "
              "robot, NOT a planet, NOT a scary horror eyeball.", "",
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
    gd += ["Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/mat_lua_bo_cuc.py all`).",
           "", "## Kiểm chung", ""]
    gd += [f"- {c}" for c in CHECK_CHUNG]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    ghi(os.path.join(pk(), "HUONG_DAN.md"), gd)
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 2: mảnh "đúng chỗ, đúng cỡ" từ concept đã duyệt (người dùng chọn A,
# 2026-11-13 → L1_duyet.png = L1_da_den.png). Mọi mảnh của rig là mảnh CỨNG lơ lửng: mỗi lượt giữ vài mảnh KHÔNG chồng nhau, vẽ đủ phần khuất.
MANH_CHUNG = ("TASK: redraw image 1, but keep ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the "
              "SAME SIZE as in image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). "
              "REMOVE everything else and leave pure white (#FFFFFF) there. Every kept part must be ONE COMPLETE CLOSED SHAPE with "
              "the dark-brown ink outline running all the way around it: where a part is hidden behind another part in image 1, "
              "DRAW the hidden portion as described. The kept parts must NOT touch each other: clear white between them. Same "
              "wobbly ink line, same colours, same crayon hatching, same completely flat colouring as image 1. Do not add "
              "anything: no shadows, no glow, no sparks, no labels.")
PLATE = "the same dark violet-black stone with its thin red-orange lava crack(s), bevel lines and thick ink outline as in image 1"
MANH = {
    "A": ("quả cầu lửa vẽ đủ hình tròn (không mắt, chỗ mắt là vùng vàng), nắm tay GẦN vẽ đủ",
          ["1. THE FIRE BALL: the round ball of fire that forms the body (a full circle, centre at about x = 805, y = 560, radius "
           "about 270: from about x = 535 to x = 1075, y = 290 to y = 830). In image 1 it is almost completely covered by the "
           "armour plates, the eye and the flames: REMOVE all of them and draw the WHOLE ball as one closed circle with an ink "
           "outline: flat colour zones of fire, red-orange (#DC3A22) in the outer ring, a wide orange (#F48022) band inside, and a "
           "yellow (#FFCE50) zone in the right part where the eye sits (the eye itself is NOT drawn: just the yellow fire there, "
           "about x = 790 to x = 1070, y = 520 to y = 785); the borders between the zones are wavy, curling like flame tongues "
           "around the ball, as in image 1. No eye, no pupil, no plates, no flame tongues sticking out.",
           "2. THE NEAR FIST: the huge armoured fist at the lower LEFT (about x = 210 to x = 555, y = 610 to y = 990) with its "
           "Y-shaped lava crack and its knuckle bumps at the bottom, complete. In image 1 its top right is touched by the orange "
           "arm stub: complete its rounded top there. Do NOT keep the orange arm stub."]),
    "B": ("tấm giáp đầu vẽ đủ, tấm dưới TRÁI vẽ đủ, nắm tay XA vẽ đủ",
          ["1. THE TOP PLATE (the helmet): the biggest armour plate lying across the top (about x = 545 to x = 1080, y = 205 to "
           "y = 610), bending down over the eye at its right end, with its Y-shaped lava crack: " + PLATE + ". In image 1 its "
           "right end is partly covered by the tall far shoulder plate and by the small plate under it: complete it as one "
           "thick slab whose right end comes down to a blunt corner at about x = 1040, y = 605.",
           "2. THE LOWER-LEFT PLATE: the curved armour plate under the near shoulder plate, just right of the orange near arm "
           "stub (its visible part about x = 495 to x = 765, y = 615 to y = 720): " + PLATE + ". In image 1 its left end is "
           "hidden behind the near shoulder plate and the arm stub, and its lower edge behind the long bottom plate: complete it "
           "into one curved crescent-like slab about 290 px long and 95 px thick, from about x = 480 to x = 770.",
           "3. THE FAR FIST: the huge armoured fist at the lower RIGHT (about x = 1030 to x = 1330, y = 600 to y = 960) with its "
           "Y-shaped lava crack and its knuckle bumps at the bottom, complete. In image 1 its upper left is touched by the "
           "orange far arm stub and its left side by the lower-right plate: complete its rounded outline there. Do NOT keep the "
           "arm stub or the lower plates."]),
    "C": ("tấm vai GẦN, tấm vai XA, tấm dưới PHẢI, tấm nhỏ cạnh mắt, mỗi tấm vẽ đủ",
          ["1. THE NEAR SHOULDER PLATE: the tall thick slab leaning back at the LEFT (about x = 318 to x = 655, y = 288 to "
           "y = 695), its pointed blunt top at the upper left, with its lava crack: " + PLATE + ". In image 1 its upper right "
           "edge is touched by the top plate and its lower end by the orange arm stub and the lower-left plate: complete it as "
           "one closed slab, its lower end a blunt bevelled corner at about x = 640, y = 690.",
           "2. THE FAR SHOULDER PLATE: the tall slab standing at the upper RIGHT (about x = 930 to x = 1170, y = 210 to y = 595), "
           "with its lava crack: " + PLATE + ". In image 1 its left part is hidden behind the right end of the top plate: complete "
           "it into one tall chunky slab about 220 px wide, leaning slightly to the right, its left edge reaching about x = 935.",
           "3. THE LOWER-RIGHT PLATE: the thick curved plate under the eye at the lower RIGHT (about x = 840 to x = 1140, y = 690 "
           "to y = 920), with its bevel lines: " + PLATE + ". In image 1 its left end is hidden behind the long bottom plate and "
           "its right end behind the far fist: complete it into one curved slab from about x = 820 to x = 1150.",
           "4. THE SMALL PLATE BESIDE THE EYE: the small chunky plate stuck on the ball just left of the eye (about x = 678 to "
           "x = 835, y = 478 to y = 622), complete, " + PLATE + "."]),
    "D": ("con mắt vẽ đủ (tròng + con ngươi khe + chấm sáng), hai khúc tay lửa vẽ đủ",
          ["1. THE EYE: the big round iris of pale hot yellow (#FFECA0) with a thick ink outline (a full circle, centre at about "
           "x = 932, y = 652, about 285 px across: from about x = 790 to x = 1075, y = 510 to y = 795) and its tall vertical slit "
           "pupil (deep red #96181E, from about y = 555 to y = 748) with the small round pale dot at its top. In image 1 the top "
           "of the iris is covered by the top plate and its bottom by the lower plates: draw the WHOLE circle. Nothing around it.",
           "2. THE NEAR ARM STUB: the short thick orange-red fiery arm at the left between the near shoulder plate and the near "
           "fist (its visible part about x = 350 to x = 505, y = 565 to y = 690): one short rounded sausage of fire, red-orange "
           "(#E8542C) with an orange (#F48022) inner stripe, about 160 px long and 80 px thick, lying diagonally from the upper "
           "right (where it goes into the ball) to the lower left (where it goes into the fist); both ends rounded and closed.",
           "3. THE FAR ARM STUB: the same short fiery arm at the right between the far shoulder plate and the far fist (its "
           "visible part about x = 1090 to x = 1185, y = 565 to y = 670): one short rounded sausage of fire about 120 px long "
           "and 75 px thick, lying diagonally from the upper left to the lower right; both ends rounded and closed."]),
    "E": ("ngọn lửa sau lưng vẽ đủ (đáy tròn nấp sau quả cầu) + hai giọt lửa, tấm dưới GIỮA vẽ đủ, tấm nhỏ dưới mép phải tấm đầu",
          ["1. THE FLAMES: the whole mass of flames rising behind the creature (from about x = 250 to x = 955, y = 20 to y = 610), "
           "all its tongues with their three nested flat colours exactly as in image 1, PLUS the two small separate flame drops "
           "floating at the upper left (at about x = 410-495, y = 20-80 and x = 275-365, y = 215-285), each with its own closed "
           "outline. In image 1 the lower part of the flames is hidden behind the plates and the ball: there, close the flame "
           "mass with one smooth rounded bottom edge running from about x = 255, y = 600 through about x = 560, y = 520 to about "
           "x = 950, y = 330 (the inside of the closed shape is the yellow and orange of the flame base). One single closed "
           "flame shape (plus the two drops).",
           "2. THE LONG BOTTOM PLATE: the long thick plate across the bottom middle (about x = 490 to x = 905, y = 690 to y = 925) "
           "with its lava crack: " + PLATE + ". In image 1 its ends are hidden behind the near fist and the lower-right plate: "
           "complete it into one long curved slab with blunt bevelled ends.",
           "3. THE SMALL PLATE UNDER THE RIGHT END OF THE TOP PLATE: the small chunky block at about x = 1050 to x = 1150, "
           "y = 465 to y = 600, complete, " + PLATE + "."]),
}
MO_TA_EN = ("an armoured fire eye: a round ball of fire with one huge yellow eye with a red slit pupil, wrapped in thick separate dark "
            "violet-black stone armour plates with thin lava cracks (one big top plate over the eye, two small plates, two tall "
            "shoulder plates, three lower plates), big flames rising behind, two short orange fiery arm stubs and two huge "
            "armoured stone fists on the ground.")
MO_TA_VI = ("mắt lửa bọc giáp đá đen tím: quả cầu lửa, mắt vàng con ngươi khe đỏ, tấm giáp đầu, 2 tấm nhỏ, 2 tấm vai, 3 tấm dưới, lửa "
            "sau lưng, 2 khúc tay lửa, 2 nắm tay đá chạm đất")


def build_manh(k=1):
    global K
    K = k
    MANH_, MO_TA_EN_, MO_TA_VI_ = (MANH, MO_TA_EN, MO_TA_VI) if k == 1 else (MANH2, MO_TA_EN2, MO_TA_VI2)
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    if not os.path.exists(duyet):
        raise SystemExit("chưa có concept duyệt " + Wp(duyet))
    ra = []
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ (2026-11-13, sau khi người dùng chọn A = `L1_da_den.png` → `L1_duyet.png`)", "",
          "Mọi mảnh của rig là mảnh cứng lơ lửng. Mỗi file vẽ lại concept đã duyệt nhưng chỉ giữ vài mảnh không chồng nhau, vẽ đủ phần "
          "khuất, bỏ hết thứ khác (nền trắng). Ảnh mẫu duy nhất của cả năm file:", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(duyet)}` | Concept đã duyệt (1536 × 1024, nền trắng): " + MO_TA_VI_ + " |", ""]
    for ma, (vi, giu) in MANH_.items():
        out = os.path.join(save_dir(), f"M_{ma}.png")
        p = os.path.join(pk(), f"luot_2_manh_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(duyet)}: the APPROVED picture of the creature, 1536x1024, white background: " + MO_TA_EN_,
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "", MANH_CHUNG, "", "KEEP:"] + giu + ["", FLAT, BG]
        ghi(p, t)
        ra.append(p)
        gd += [f"- **`{ma}`**: {vi}. Chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
    gd += ["", "Kiểm từng ảnh: đúng các mảnh đã kê, nằm trùng chỗ concept (chồng lên concept phải khít), mỗi mảnh viền mực kín, không "
           "chạm nhau, phần khuất đã vẽ đủ, nền trắng tinh, không bóng. Claude cắt bằng `mat_lua_manh.py`."]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    ghi(hd, [cu] + gd)
    for p in ra:
        print(p)


# ---------------------------------------------------------------- DẠNG 2 (người dùng 2026-11-13: "con này là dạng 1, làm tiếp dạng 2 to hơn,
# chiến hơn"). Cùng rig, cùng clip. Tỉ lệ đổi trên rig trước (mat_lua_rig.py bo_cuc, ML_DANG=2: nắm tay ×1,3, tấm vai ×1,22, tấm đầu ×1,15,
# tấm dưới ×1,12): hình bố cục là da dạng 1 ở tỉ lệ dạng 2. Ba hướng thiết kế là ĐỀ XUẤT của Claude, chờ người dùng chọn.
D2_CHUNG = (
    "EVOLVED FORM: this is the SECOND, final evolution of the creature in image 2 (the approved first form): the same species and the "
    "same build (one round ball of living fire with ONE huge eye on its right part, wrapped in thick separate armour plates, two short "
    "fiery arm stubs, two huge armoured fists standing on the ground, big flames rising behind), but grown up, HEAVIER, MORE ARMOURED "
    "and much FIERCER: an adult battle monster, not a cute baby any more.\n"
    "- LAYOUT: follow image 1 exactly for where every piece is and how big it is (it is the first form's art already re-arranged in "
    "the new proportions: bigger fists, bigger shoulder plates, bigger top plate). Same canvas framing: from about x = 245 to "
    "x = 1305, from the top of the flames at about y = 85 to the bottom of the fists at about y = 1000. Facing the viewer's RIGHT.\n"
    "- KEEP THE SAME PIECES (the picture will be cut into the same pieces and animated with the same skeleton): flames / fire ball / "
    "eye / top plate / two small plates (one beside the eye, one under the right end of the top plate) / near and far shoulder "
    "plates / three lower plates (left, long bottom middle, right) / two arm stubs / two fists. Every piece one closed shape with "
    "its own ink outline. Anything new (horns, spikes, fangs, talons) is drawn AS PART OF the plate or fist it grows from, never as "
    "a separate floating piece.\n"
    "- THE EYE must stay clearly readable: about four fifths of its round iris visible, only its top covered by the edge of the top "
    "plate like a heavy angry brow. Iris hot amber-orange (#FFB43C) with a pale yellow (#FFE89A) inner ring around the pupil; the "
    "pupil a narrow black-red (#3A0E10) vertical slit, narrower and sharper than in image 2; one tiny pale dot of light.\n"
    "- ARMOUR: thicker, more angular, chunkier slabs of black volcanic glass, darker than in image 2 (#2A2430), with THICKER glowing "
    "magma cracks: each crack orange-red (#FF6A1E) with a yellow (#FFC83A) line in its middle, flat colour, no glow.\n"
    "- FLAMES: taller and wilder than in image 2, more tongues, sharper hooked tips, three nested flat colours with a pale yellow "
    "core (#FFF0A0) near the base. The fire ball: the same three wavy flame zones.\n")
D2 = {
    "sung": dict(
        ten="A · mũ sừng chiến: tấm đầu thành mũ trận có hai sừng cong lớn vút ra sau; tấm vai có gai tù; nắm tay có ba gai đá trên đốt",
        thay=("- DESIGN A, HORNED WAR HELM: the top plate becomes a heavy war helmet slab with TWO big curved HORNS of the same black "
              "glass growing from its top (one from its back part, one from its middle), sweeping up and backward to the viewer's "
              "LEFT, each horn with one magma crack. Each shoulder plate gets two short blunt spikes on its outer edge. Each fist "
              "gets three short thick cone spikes along its top knuckles, like a spiked gauntlet. The lower plates stay smooth "
              "curved slabs.")),
    "ham": dict(
        ten="B · hàm dung nham: ba tấm dưới thành bộ hàm đá lởm chởm có nanh lớn dưới con mắt; tấm đầu có gờ mày và một gai giữa; nắm tay có vuốt đá",
        thay=("- DESIGN B, MAGMA JAW: the three lower plates become a jagged stone JAW under the eye: their upper edges carry four or "
              "five big pointed stone FANGS pointing up toward the eye (the long bottom-middle plate carries the biggest two), so "
              "the creature reads as a monster face with a fanged lower jaw; still three separate plates. The top plate gets a "
              "sharp brow ridge along its lower edge and one tall pointed spike rising from its middle. Each fist gets three short "
              "curved stone TALONS sticking out from its front knuckles like a claw gauntlet.")),
    "ca_hai": dict(
        ten="C · bạo chúa: gộp A và B (mũ hai sừng, hàm nanh, nắm tay gai), lửa cao nhất",
        thay=("- DESIGN C, TYRANT: everything at once: the top plate is a horned war helmet with TWO big curved horns sweeping up "
              "and back to the viewer's LEFT; the three lower plates form a jagged jaw with four big stone fangs pointing up toward "
              "the eye; each shoulder plate has two blunt spikes; each fist has three thick cone spikes on its knuckles. The "
              "flames are the tallest and wildest of all.")),
}


def build_dang2():
    k2 = 2
    pk2 = os.path.join(HERE, "gui_gpt", f"{CODE}_{k2}")
    tai2 = os.path.join(HERE, "inbox", f"{CODE}_{k2}", "tai_ve")
    bc2 = os.path.join(HERE, "inbox", f"{CODE}_{k2}", "mau", "bo_cuc.png")
    duyet1 = os.path.join(save_dir(), "L1_duyet.png")
    os.makedirs(pk2, exist_ok=True)
    os.makedirs(tai2, exist_ok=True)
    R = [(bc2, "LAYOUT GUIDE, 1536x1024, white background: the first form's art re-arranged in the NEW proportions of the evolved form "
               "(bigger fists, bigger shoulder plates and top plate). Use it for where every piece is and how big it is.",
          "Hình bố cục dạng 2 (1536 × 1024, nền trắng): da dạng 1 ở tỉ lệ dạng 2 dựng trên rig (nắm tay to ×1,3, tấm vai ×1,22, tấm đầu ×1,15). "
          "Lấy chỗ đặt, cỡ từng mảnh"),
         (duyet1, "the APPROVED FIRST FORM of this creature, 1536x1024, white background: the design to evolve from, and the exact "
                  "line and colouring style to keep.",
          "Concept dạng 1 đã duyệt (1536 × 1024, nền trắng): mắt lửa bọc giáp đá đen tím. Thiết kế gốc để tiến hóa, nét và cách tô"),
         (KIEM_SI, "an approved hero of the same game (an armoured monkey samurai), 1536x1024: match its wobbly dark-brown pen line, "
                   "visible crayon hatching, completely flat colouring and fierce battle-ready attitude. Do NOT copy its design.",
          "Voọc Tướng đã duyệt: lấy nét bút, vân sáp, tô phẳng, thần thái chiến"),
         (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style.",
          "Bản đồ vẽ tay: chỉ lấy nét bút mực nâu, vân chì sáp")]
    missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
    gd = [f"# Gói gửi GPT: `{CODE}` dạng 2 (mắt lửa bọc giáp tiến hóa: to hơn, chiến hơn)", "",
          "Làm 2026-11-13 sau khi người dùng duyệt rig dạng 1 (\"ok nhìn ổn, con này là dạng 1, bạn làm tiếp dạng 2 to hơn, chiến hơn\"). Cùng "
          "rig, cùng clip với dạng 1. Ba hướng thiết kế là đề xuất của Claude, chờ người dùng chọn. Ghi chú: `ArtGen/Spine/inbox/mat_lua_ghichu.md`.", ""]
    for kieu, d in D2.items():
        out = os.path.join(tai2, f"L1_{kieu}.png")
        p = os.path.join(pk2, f"luot_1_concept_{kieu}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "",
              "TASK: draw the EVOLVED FORM of the creature of image 2 as ONE picture, in a clean animation-ready resting pose, in the "
              "hand-drawn style of image 2.", "", D2_CHUNG, d["thay"], "",
              "Fierce and powerful, battle-ready, heavy; still a hand-drawn monster-collecting game creature, NOT horror (no veins, no "
              "blood), NOT a robot.", "",
              "ANIMATION-READY: calm resting pose exactly as in image 1; no sparks, no embers, no smoke, no glow, no speed lines, no "
              "ground, no props, no second character.", "", SOFT, LINE, FLAT, BG]
        ghi(p, t)
        gd += [f"## Hướng `{kieu}`: {d['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += [""]
        print(p)
    gd += ["## Kiểm chung", "",
           "- Bố cục và cỡ từng mảnh theo hình bố cục; nhìn sang phải; đủ các mảnh như dạng 1 (sừng, gai, nanh, vuốt mọc liền trên mảnh của nó).",
           "- Mắt lộ khoảng 4/5, tròng hổ phách, con ngươi khe đen đỏ hẹp; tấm đầu đè mép trên như mày cau.",
           "- Giáp đen hơn dạng 1, vết nứt dung nham dày có lõi vàng; lửa cao, nhiều lưỡi hơn; tô phẳng, không quầng sáng, nền trắng."]
    ghi(os.path.join(pk2, "HUONG_DAN.md"), gd)


# dạng 2: mảnh "đúng chỗ, đúng cỡ" từ concept dạng 2 đã chốt (L1_duyet.png = L1b_ham_tay_tron.png); 6 tờ, mảnh trong một tờ không chạm nhau
PLATE2 = ("the same black volcanic glass with its thick glowing magma cracks (orange-red with a yellow middle line), bevel lines and "
          "thick ink outline as in image 1")
MANH2 = {
    "A": ("quả cầu lửa vẽ đủ hình tròn (không mắt, chỗ mắt là vùng vàng)",
          ["1. THE FIRE BALL: the round ball of fire that forms the body (a full circle, centre at about x = 815, y = 625, radius about "
           "255: from about x = 560 to x = 1070, y = 370 to y = 880). In image 1 it is almost completely covered by the armour plates, "
           "the eye, the jaw and the flames: REMOVE all of them and draw the WHOLE ball as one closed circle with an ink outline: flat "
           "colour zones of fire, red-orange in the outer ring, a wide orange band inside, and a yellow zone in the right part where "
           "the eye sits (the eye itself is NOT drawn: just yellow fire there, about x = 790 to x = 1060, y = 545 to y = 790); the "
           "borders between the zones are wavy, curling like flame tongues, as in image 1. No eye, no plates, no fangs, no flame "
           "tongues sticking out."]),
    "B": ("tấm giáp đầu (có gai giữa) vẽ đủ, hai nắm tay vẽ đủ",
          ["1. THE TOP PLATE (the helmet): the big armour plate across the top with its brow ridge and its tall pointed middle spike "
           "(about x = 515 to x = 1145, y = 160 to y = 615), bending down over the eye at its right end: " + PLATE2 + ". In image 1 its "
           "left end is hidden behind the near shoulder plate and its right end behind the far shoulder plate: complete both ends as "
           "blunt bevelled corners (left end at about x = 500, right end at about x = 1160).",
           "2. THE NEAR FIST: the huge armoured fist at the lower LEFT (about x = 125 to x = 555, y = 570 to y = 985) with its Y-shaped "
           "magma crack and its rounded knuckle bumps along the bottom, complete (its top right is touched by the near shoulder plate "
           "in image 1: complete its rounded top there).",
           "3. THE FAR FIST: the huge armoured fist at the lower RIGHT (about x = 1020 to x = 1415, y = 565 to y = 980), complete, the "
           "same design."]),
    "C": ("tấm vai GẦN, tấm vai XA, tấm hàm PHẢI (có nanh), mỗi tấm vẽ đủ",
          ["1. THE NEAR SHOULDER PLATE: the big thick slab at the LEFT (about x = 270 to x = 695, y = 295 to y = 695) with its long "
           "magma crack: " + PLATE2 + ". In image 1 its lower end is hidden behind the near fist and its upper right edge touches the "
           "top plate: complete it as one closed slab with a blunt bevelled lower end at about x = 640, y = 690.",
           "2. THE FAR SHOULDER PLATE: the tall slab at the upper RIGHT (about x = 1000 to x = 1250, y = 240 to y = 595): " + PLATE2 +
           ". In image 1 its left part is hidden behind the top plate and its bottom behind the far fist: complete it into one tall "
           "chunky slab, its left edge at about x = 990, its lower end a blunt corner at about y = 600.",
           "3. THE RIGHT JAW PLATE: the small lower plate at the right end of the jaw, under the eye (about x = 945 to x = 1080, "
           "y = 700 to y = 925), with its one pointed stone fang on its upper edge (pointing up toward the eye): " + PLATE2 + ". In "
           "image 1 its left end is hidden behind the middle jaw plate and its right end behind the far fist: complete it into one "
           "closed curved plate from about x = 930 to x = 1095."]),
    "D": ("con mắt vẽ đủ (tròng hổ phách + vòng vàng + con ngươi khe + chấm sáng), hai khúc tay lửa vẽ đủ",
          ["1. THE EYE: the big round iris (a full circle, centre at about x = 925, y = 668, about 275 px across: from about x = 788 "
           "to x = 1063, y = 530 to y = 805): hot amber-orange outer iris, pale yellow inner ring, the narrow black-red vertical slit "
           "pupil and the tiny pale dot, thick ink outline. In image 1 its top is covered by the top plate and the small plate, its "
           "bottom by the fangs of the jaw: draw the WHOLE circle. Nothing around it.",
           "2. THE NEAR ARM STUB: a short thick fiery arm hidden in image 1 between the near shoulder plate and the near fist: one "
           "short rounded sausage of fire, red-orange (#E8542C) with an orange (#F48022) inner stripe, about 170 px long and 90 px "
           "thick, lying diagonally from about x = 590, y = 560 (upper right, where it goes into the ball) to about x = 455, y = 655 "
           "(lower left, where it goes into the fist); both ends rounded and closed.",
           "3. THE FAR ARM STUB: the same at the right, hidden between the far shoulder plate and the far fist: about 130 px long and "
           "85 px thick, lying diagonally from about x = 1065, y = 555 (upper left) to about x = 1170, y = 625 (lower right)."]),
    "E": ("ngọn lửa sau lưng vẽ đủ (đáy tròn nấp sau quả cầu) + hai giọt lửa, tấm hàm GIỮA (hai nanh lớn) vẽ đủ, tấm nhỏ dưới mép phải tấm đầu",
          ["1. THE FLAMES: the whole mass of flames rising behind the creature (from about x = 175 to x = 1075, y = 25 to y = 645), all "
           "its tongues with their three nested flat colours exactly as in image 1, PLUS the small separate flame drops floating at "
           "the upper left (at about x = 375-515, y = 25-105 and x = 200-315, y = 225-325), each with its own closed outline. In image "
           "1 the lower part of the flames is hidden behind the plates and the ball: there, close the flame mass with one smooth "
           "rounded bottom edge running from about x = 185, y = 640 through about x = 560, y = 560 to about x = 1065, y = 330 (the "
           "inside is the yellow and orange of the flame base). One single closed flame shape (plus the drops).",
           "2. THE MIDDLE JAW PLATE: the long thick plate across the bottom middle (about x = 595 to x = 960, y = 685 to y = 945) with "
           "its TWO big pointed stone fangs on its upper edge (pointing up toward the eye) and its magma cracks: " + PLATE2 + ". In "
           "image 1 its ends are hidden behind the left and right jaw plates: complete it into one long curved plate with blunt ends.",
           "3. THE SMALL PLATE UNDER THE RIGHT END OF THE TOP PLATE: a small chunky block of the same black glass at about x = 1065 to "
           "x = 1160, y = 470 to y = 600 (mostly hidden in image 1), complete, " + PLATE2 + "."]),
    "F": ("tấm nhỏ cạnh mắt vẽ đủ, tấm hàm TRÁI (có nanh) vẽ đủ",
          ["1. THE SMALL PLATE BESIDE THE EYE: the small chunky plate stuck on the ball just left of the eye (about x = 685 to x = 840, "
           "y = 515 to y = 630), complete, " + PLATE2 + ".",
           "2. THE LEFT JAW PLATE: the small lower plate at the left end of the jaw (about x = 500 to x = 655, y = 690 to y = 930), "
           "with its pointed stone fang on its upper edge (pointing up and to the right): " + PLATE2 + ". In image 1 its left end is "
           "hidden behind the near fist and its right end behind the middle jaw plate: complete it into one closed curved plate from "
           "about x = 480 to x = 670."]),
}
MO_TA_EN2 = ("the evolved armoured fire eye: a round ball of fire with one huge amber eye with a black-red slit pupil, wrapped in thick "
             "black volcanic-glass armour plates with thick glowing magma cracks (a top plate with a brow ridge and a tall middle "
             "spike, two big shoulder plates, a small plate beside the eye, three lower plates forming a jaw with big stone fangs "
             "under the eye), big flames rising behind, and two huge smooth armoured fists on the ground.")
MO_TA_VI2 = ("mắt lửa bọc giáp dạng 2: quả cầu lửa, mắt hổ phách con ngươi khe, tấm đầu có gờ mày và gai giữa, 2 tấm vai to, tấm nhỏ cạnh "
             "mắt, 3 tấm dưới thành hàm nanh, lửa sau lưng, 2 nắm tay giáp trơn chạm đất")

# dạng 2 lượt 1b (người dùng 2026-11-13: "lấy dạng b nhưng bỏ gai ở tay đi"): vẽ lại y hệt L1_ham.png, chỉ bỏ vuốt / gai ở hai nắm tay
def build_dang2_1b():
    tai2 = os.path.join(HERE, "inbox", f"{CODE}_2", "tai_ve")
    src = os.path.join(tai2, "L1_ham.png")
    out = os.path.join(tai2, "L1b_ham_tay_tron.png")
    p = os.path.join(HERE, "gui_gpt", f"{CODE}_2", "luot_1b_tay_tron.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(src)}: THE CHARACTER, already drawn and approved (1536x1024, white background): an armoured fire-eye monster: "
         "a ball of fire with one amber eye, black volcanic-glass armour plates with thick magma cracks (a top plate with a brow "
         "ridge and a tall middle spike, two shoulder plates, a small plate beside the eye, three lower plates forming a fanged "
         "jaw), big flames behind, two huge armoured fists on the ground with curved stone talons at their bottom.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as L1b_ham_tay_tron_2.png, L1b_ham_tay_tron_3.png ... in the same folder. Do "
         "not edit, move or delete any other file.", "",
         "TASK: redraw image 1 EXACTLY, changing ONLY the two fists.", "",
         "KEEP IDENTICAL (if the new picture is laid over image 1, everything except the talons must match: same place, same size, "
         "same shapes, same colours, same line): the flames, the fire ball, the eye, the top plate with its spike, both shoulder "
         "plates, the small plate, the three fanged lower plates and all their fangs, the orange arm stubs, and the main block of "
         "both fists with their Y-shaped magma cracks. Same canvas, same framing, same wobbly ink line, same crayon hatching, same "
         "flat colours.", "",
         "CHANGE ONLY THE FISTS: REMOVE every stone talon / claw / spike from both fists (the curved grey talons along their bottom "
         "and front). Each fist becomes one smooth chunky armoured boxing-glove block of the same black volcanic glass, with three "
         "or four big rounded knuckle bumps along its bottom edge (like the first form's fists, but this bigger size), its Y-shaped "
         "magma crack kept. The fists keep exactly the same position, outline height and width as the fist blocks in image 1 and "
         "still stand on the ground at the same level. No spikes anywhere on the fists.", "",
         "Flat colours only: no shading, no highlights, no glow, no cast shadow. Plain pure-white background, no ground, no text."]
    ghi(p, t)
    print(p)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dang2_1b":
        build_dang2_1b()
    elif len(sys.argv) > 1 and sys.argv[1] == "manh":
        build_manh(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == "dang2":
        build_dang2()
    else:
        main()
