# -*- coding: utf-8 -*-
"""Gói GPT vẽ pháp sư lửa (mã làm việc phap_lua, con gốc của rig: monster_3481). Tướng thứ 6 đảo Hỏa.

Người dùng (2026-11-13): "concept pháp sư lửa giống như ref, con mắt trong quyền trượng đổi thành cầu lửa cháy liên tục (làm anima lửa
cháy, thêm fx khói bốc đằng sau lớp cầu lửa)". appear bay vào; idle, walk giống con gốc nhưng sửa khác chút; đánh thường dùng tay không
cầm trượng cào đối thủ; cast giống skill_02 (giơ trượng triệu hồi kim lửa rồi bắn); chiêu cuối giống skill_03 (dang hai tay, trượng lơ
lửng, cầu lửa tách ra bay lên cao, hút lửa thành cầu lửa to rồi bắn); die giống con gốc. Ba hướng màu là ĐỀ XUẤT của Claude, chờ người
dùng chọn. Chỉ lấy của con gốc cách dựng (chỗ, cỡ, hình bóng, thứ tự chồng từng part); hình là của mình. Không đính ảnh con gốc; đính
sơ đồ bố cục tự dựng bằng mã (phap_lua_bo_cuc.py).

    py -3 -I ArtGen/Spine/phap_lua_bo_cuc.py all
    py -3 -I ArtGen/Spine/build_phap_lua.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/phap_lua_1/luot_1_concept_<hướng>.txt [--note "..."]
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "phap_lua"
K = 1
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
KIEM_SI = os.path.join(HERE, "inbox", "kiem_si_1", "tai_ve", "L1_duyet.png")
CUNG_LUA = os.path.join(HERE, "inbox", "cung_lua_1", "mau", "concept_A.png")


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


LUA = ("#E0441F", "#F7902A", "#FFD45A")

STANCE = ("STANCE (the same as in the layout guide, image 1): a FLOATING FIRE-MAGE SPIRIT with NO legs and NO arms. Its body is a "
          "wide ragged robe that hangs in the air and ends at the bottom in several tattered pointed tails; its head is a dark "
          "horned mask seen almost from the front, turned a little toward the VIEWER'S RIGHT (it faces its opponent on the right); "
          "behind the head a HUGE mane of hair sweeps back to the viewer's left. It has two DETACHED floating hands, each one a "
          "short wispy wrist ending in dark clawed fingers: the hand on the viewer's LEFT grips a tall staff whose head holds a "
          "burning FIRE ORB; the hand on the viewer's RIGHT is raised and open, long curved claws spread, ready to slash. Menacing, "
          "determined, ready to fight; appealing like a monster-collecting game creature, NOT a cute smiling mascot, NOT horror, "
          "NOT gory, NOT a realistic human.")

BODY = (
    "- THE ROBE (the biggest piece, about {ao}): one wide ragged cloak body, widest in the middle, its lower edge cut into five or "
    "six big tattered pointed tails of different lengths (like the points of a maple leaf), one tail sticking out to the right at "
    "about x = 1190, y = 700. Its upper part rises behind the mask up to the neck. {ao_ten}\n"
    "- THE SHOULDER CAPES: a big dark cape hangs from the left shoulder (about {choang_trai}): it starts under the mask, runs to the "
    "left behind the staff hand and ends in a wide flat squarish flap with a notched edge at the far lower left; a small short cape "
    "covers the right shoulder (about {choang_phai}). {choang_ten} ONE thin pale trim line runs along the lower edge of each cape.\n"
    "- THE CHEST ORNAMENT: in the middle of the chest, under the mask, a braided cord (about {day}): two flat straps coming down "
    "from the two shoulders cross and twist into a zigzag braid that hangs down and ends in a sharp point. {day_ten} At each side of "
    "it one sharp FOUR-POINTED STAR spike, like a compass needle with a long lower point (left one about {sao_trai}, right one about "
    "{sao_phai}). {sao_ten}\n"
    "- THE HAIR (about {toc}): a huge thick mane, bigger than the head, swept back and up to the viewer's LEFT like a wave, with "
    "four or five big pointed locks at its upper edge and its left end curling into a hook; one smaller pointed lock sticks out to "
    "the right of the head. {toc_ten}\n"
    "- THE MASK (the face): no skin, no mouth. A narrow dark beak-like face plate pointing DOWN (about {mat_na}), built from two "
    "angular plates that meet at a centre ridge, with two small narrow slanted EYE SLITS, one each side of the ridge; through the "
    "slits and between the plates the bright inner colour of the robe shows ({mat_ten}). From the face two HORN pieces rise: on the "
    "viewer's left a tall thin prong going straight up with, at its base, a big curved hook horn sweeping out to the left and down "
    "like a bull horn (about {sung_phai}); on the right a second tall thin prong, a little shorter, with a smaller curved hook at "
    "its base pointing right and down (about {sung_trai}). The two tall prongs stand close together like a tuning fork. Between "
    "them, on the forehead, a small diamond-shaped GEM (about {ngoc}). {giap_ten}\n"
    "- THE STAFF (about {truong}): a tall thin staff held diagonally. Its HEAD is at the upper left: an angular dark claw-like "
    "frame that grips the orb: a pointed hood arching over the top and the right side of the orb, one sharp spike reaching from "
    "the right to the LEFT across the middle of the orb, and a prong under the orb pointing left; two thin icicle-like spikes hang "
    "down under the head. From the head the long thin shaft runs down to the RIGHT, passes through the staff hand at about "
    "x = 650, y = 600, and ends in a ZIGZAG lightning-bolt-shaped tip at about x = 840, y = 965. {truong_ten}\n"
    "- THE FIRE ORB (instead of an eye or a crystal ball): inside the staff head a round BALL OF FIRE, centre about "
    "({cx}, {cy}), radius about {cr}: flat nested zones, red-orange ({l0}) outside, orange ({l1}), yellow ({l2}) heart, the borders "
    "between the zones wavy like flame tongues. The ball BURNS: three flame tongues rise from its top BEHIND the dark frame, up to "
    "about y = {cy0}, leaning a little to the left, each with a thick base, a soft S-curve and a sharp tip; the same three flat "
    "colours. The dark frame is drawn IN FRONT of the ball and of the flames.\n"
    "- THE STAFF HAND (about {tay_truong}): a short wispy wrist with a small curling tail pointing right, and FOUR dark clawed "
    "fingers wrapped around the shaft (the fingers in front of the shaft). {tay_ten}\n"
    "- THE CLAW HAND (about {tay_vuot}): raised at the right, open, palm toward the viewer: a wispy wrist that trails DOWN into a "
    "long wavy tail ending in a small curl at about x = 1080, y = 580, and FIVE long curved dark claws spread like a rake at the "
    "top, each claw two segments (a short knuckle and a long curved pointed nail), the nails curving to the left and down.")

SIMPLE = ("SIMPLE DESIGN, FEW DETAILS (very important): big clean readable shapes, each area ONE flat colour. Inside the hair only "
          "four to six long flowing strand lines; on the robe only the one inner zone described; on each cape only the one trim "
          "line; on the dark armour pieces (mask, horns, stars, staff, claws) at most one thin ridge line each. NO runes, NO "
          "patterns, NO cracks, NO jewellery other than the gem, NO belts, NO extra spikes. The ONLY fire is what is listed: the "
          "fire orb with its three flame tongues{lua_them}. NO sparks, NO embers, NO smoke, NO floating bits.")

FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the figure fills the middle of the canvas: from the left flap of the big cape "
         "at about x = {x0} to the claw hand at about x = {x1}, and from the tip of the tallest flame at about y = {y0} to the "
         "zigzag tip of the staff at about y = {y1}. Do NOT enlarge, shrink, move or mirror the figure.")

POSE = ("ANIMATION-READY (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): calm, "
        "clean resting pose exactly as in the guide. Draw every piece as a clear closed shape with its own complete ink outline so "
        "the pieces can be separated: the robe, each cape, the cord, each star, the hair, each horn piece, the face plates, the "
        "gem, the staff, the fire orb, each wrist, each finger and claw. Pieces touch or overlap but are NOT melted into one blob. "
        "No glow, no speed lines, no ground, no magic circles, no second character, no text.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram: take from it the placement, the size, the SILHOUETTE and the overlaps of every "
        "piece and the kind of colour of each piece; do NOT take its line quality. Keep the silhouettes close to the guide (the "
        "pieces will be fitted onto an existing skeleton), but draw them cleanly and elegantly by hand: sharp where the guide is "
        "sharp (horns, claws, staff, stars), flowing where it is soft (hair, wrists, robe tails). Do NOT copy any existing "
        "character.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 5 px thick on this canvas around every big piece, and about 3 px for small "
        "details (strand lines, trim lines, eye slits, finger joints); every area coloured with coloured pencils and wax crayons, "
        "the strokes visible as loose diagonal hatching (strokes thinner than the outline), kept inside the outline. Clean and "
        "appealing, neither a crude scribble nor an over-rendered painting.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker underside, no shadows of any kind (no cast shadow of one piece on another, no "
        "shadow under the figure), no white highlights or shine spots, no gloss, no reflections, NO GLOW around the fire, the orb, "
        "the gem or the eye slits, no halo, no rim light, no gradients, no 3D look. The fire looks hot only because its flat "
        "colours are bright.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no effects around the "
      "character.")

FLAME_HAIR = (" It is a MANE OF FIRE: the whole hair mass is one big flame shape with the same silhouette, three nested flat "
              f"colour zones (red-orange {LUA[0]} outside, orange {LUA[1]}, yellow {LUA[2]} inside), the zone borders wavy; drawn "
              "like a hand-drawn flame, not like hair strands (two or three flowing lines at most).")

D = {
    "ao_do": dict(
        ten="áo choàng đỏ thẫm hoa văn lưỡi lửa cam, tóc tro trắng kem, giáp + trượng đen than (sát con gốc nhất)",
        ao_ten="Deep crimson red (#A32E22) with ONE big inner zone of orange (#E8782A) in its middle whose border is wavy like "
               "flame tongues reaching down into the tails.",
        choang_ten="Both capes dark charcoal (#3C353B), the trim line pale gold (#E2B24C).",
        day_ten="Pale gold (#E2B24C).", sao_ten="Charcoal black (#2F2A30).",
        toc_ten="Pale ash-cream white (#E9E1D2), the strand lines a slightly darker warm grey (#CFC5B4).",
        mat_ten="orange #E8782A", giap_ten="Face plates and horns charcoal black (#2F2A30); the gem yellow (#FFD45A).",
        truong_ten="The whole staff charcoal black (#2F2A30).",
        tay_ten="Both wrists pale ash-cream (#E9E1D2) like the hair, like wisps of pale smoke; fingers and claws charcoal black "
                "(#2F2A30).",
        lua_them="",
        palette="COLOURS (use exactly these, each area one flat colour): robe deep crimson #A32E22 with the orange #E8782A inner "
                "zone; capes charcoal #3C353B with a pale gold #E2B24C trim line; cord pale gold #E2B24C; hair and wrists pale "
                "ash-cream #E9E1D2; mask, horns, stars, staff, fingers and claws charcoal black #2F2A30; gem yellow #FFD45A; fire "
                f"orb and flames red-orange {LUA[0]} / orange {LUA[1]} / yellow {LUA[2]}; every outline dark-brown ink #2B2118. "
                "Only these colours: NO blue, NO green, NO purple, NO pink.",
        check=["Áo **đỏ thẫm** có một vùng cam giữa (ranh uốn lưỡi lửa); tóc và cổ tay **tro trắng kem**; mặt nạ, sừng, trượng, vuốt "
               "**đen than**; dây ngực vàng nhạt."]),
    "toc_lua": dict(
        ten="tóc là bờm lửa, áo xám than hoa văn than hồng, khăn vai đỏ thẫm, giáp sắt đen",
        ao_ten="Dark ash grey (#5B5357) with ONE big inner zone of ember red-orange (#BE542C) in its middle whose border is wavy "
               "like flame tongues reaching down into the tails.",
        choang_ten="Both capes deep crimson (#8A2A22), the trim line pale bone (#E8DFCC).",
        day_ten="Pale bone (#E8DFCC).", sao_ten="Black iron (#2E2A30).",
        toc_ten=FLAME_HAIR.strip(),
        mat_ten="ember orange #BE542C", giap_ten="Face plates and horns black iron (#2E2A30); the gem orange (#F7902A).",
        truong_ten="The whole staff black iron (#2E2A30).",
        tay_ten=f"Both wrists are small wisps of FLAME (orange {LUA[1]} with a yellow {LUA[2]} centre, red-orange {LUA[0]} edge); "
                "fingers and claws black iron (#2E2A30).",
        lua_them=", the mane of fire and the two flame wrists",
        palette="COLOURS (use exactly these, each area one flat colour): robe dark ash grey #5B5357 with the ember #BE542C inner "
                "zone; capes deep crimson #8A2A22 with a pale bone #E8DFCC trim line; cord pale bone #E8DFCC; mask, horns, stars, "
                "staff, fingers and claws black iron #2E2A30; gem orange #F7902A; hair, wrists, fire orb and flames red-orange "
                f"{LUA[0]} / orange {LUA[1]} / yellow {LUA[2]}; every outline dark-brown ink #2B2118. Only these colours: NO blue, "
                "NO green, NO purple, NO pink.",
        check=["**Tóc là bờm lửa** ba vùng màu (giữ hình bóng bờm tóc); hai cổ tay là **đốm lửa**; áo **xám than** có vùng than hồng; "
               "khăn vai **đỏ thẫm**; mặt nạ, sừng, trượng, vuốt sắt đen."]),
    "khoi": dict(
        ten="tóc khói xám than, áo cam hổ phách hoa văn vàng, khăn vai nâu đỏ, giáp + trượng đồng thau",
        ao_ten="Warm amber orange (#E08A2E) with ONE big inner zone of yellow (#F7C454) in its middle whose border is wavy like "
               "flame tongues reaching down into the tails.",
        choang_ten="Both capes dark maroon (#6E2630), the trim line brass (#B57438).",
        day_ten="Dark charcoal (#3C343A).", sao_ten="Brass (#B57438).",
        toc_ten="Dark charcoal-grey SMOKE colour (#605A66), like a thick cloud of dark smoke, the strand lines a lighter grey "
                "(#8A8490).",
        mat_ten="yellow #F7C454",
        giap_ten="Face plates and horns dull bronze-brass (#B57438); the gem red-orange (#E0441F).",
        truong_ten="The whole staff dull bronze-brass (#B57438).",
        tay_ten="Both wrists grey smoke (#96909A); fingers and claws dark charcoal (#3C343A).",
        lua_them="",
        palette="COLOURS (use exactly these, each area one flat colour): robe amber orange #E08A2E with the yellow #F7C454 inner "
                "zone; capes dark maroon #6E2630 with a brass #B57438 trim line; cord dark charcoal #3C343A; hair smoke grey "
                "#605A66; wrists lighter smoke grey #96909A; mask, horns, stars and staff dull bronze-brass #B57438; fingers and "
                f"claws dark charcoal #3C343A; gem red-orange #E0441F; fire orb and flames red-orange {LUA[0]} / orange {LUA[1]} "
                f"/ yellow {LUA[2]}; every outline dark-brown ink #2B2118. Only these colours: NO blue, NO green, NO purple, NO "
                "pink.",
        check=["**Tóc khói xám than**, cổ tay khói xám nhạt; áo **cam hổ phách** có vùng vàng; khăn vai **nâu đỏ**; mặt nạ, sừng, sao, "
               "trượng **đồng thau**; vuốt than."]),
}

CHECK_CHUNG = [
    "Bố cục y sơ đồ (không lật ngang): trượng bên **trái**, tay vuốt giơ bên **phải**; mặt nạ gần chính diện hơi quay phải; bờm tóc to "
    "hất về trái; không chân, không cánh tay (hai bàn tay rời có cổ tay khói).",
    "**Đầu trượng**: khung vuốt sẫm ôm **cầu lửa** ba vùng màu, ba lưỡi lửa bốc lên SAU khung; không còn con mắt; hai gai nhỏ dưới đầu "
    "trượng; cán dài xuống phải, mũi zíc zắc.",
    "Mặt nạ mỏ nhọn chĩa xuống, hai khe mắt hẹp; hai nhánh sừng cao thẳng đứng sát nhau + hai móc sừng cong hai bên; viên ngọc nhỏ giữa trán.",
    "Tay trượng: bốn ngón ôm cán. Tay vuốt: năm vuốt dài cong hai đốt, cổ tay kéo đuôi lượn xuống.",
    "Ngực: dây bện zíc zắc + hai gai sao bốn cánh; hai khăn vai mỗi cái một nét viền.",
    "Ít chi tiết: không hoa văn, không tia lửa, tàn, khói; tô phẳng, không bóng, **không quầng sáng**; nét bút nâu rung, vân sáp; nền trắng.",
]

FIX = [
    ("Đầu trượng vẫn là con mắt / quả cầu pha lê", "The ball in the staff head is a BALL OF FIRE (red-orange / orange / yellow flat zones) with three flame tongues rising behind the dark frame. No eye, no pupil, no crystal."),
    ("Lật ngang / đổi tay", "Do not mirror: the staff is on the viewer's LEFT, the open claw hand on the viewer's RIGHT, exactly as in the layout guide."),
    ("Vẽ thêm cánh tay / chân", "No arms and no legs: two detached floating hands with short wispy wrists; the robe ends in tattered tails."),
    ("Có quầng sáng / tia lửa / khói", "Remove every glow, halo, spark, ember and smoke. Flat colours only."),
    ("Thêm hoa văn / chi tiết", "Remove all runes, patterns and extra ornaments: each area one flat colour, only the details listed."),
    ("Mặt người / mặt cười", "The face is a dark beak-like MASK pointing down with two narrow slanted eye slits, no skin, no mouth, no smile."),
    ("Có bóng đổ / tô khối", "Flat colour only: no shading, no cast shadow, no highlights."),
]


def refs(kieu):
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature in its resting stance, built "
         "from flat coloured silhouettes: where every piece goes on the canvas, how big it is, its silhouette and which piece "
         "overlaps which (the ragged robe; two shoulder capes; the big hair mane; the horned mask with two tall prongs; the staff "
         "at the left with the ball of fire in its claw-like head; the staff hand; the open claw hand at the right; the braided "
         "cord and two star spikes on the chest). Use it for placement, size, silhouette and overlap; redraw everything in the "
         "hand-drawn style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng) ở dáng nghỉ của rig: hình bóng phẳng từng mảnh tô theo màu của hướng này "
         "(áo rách nhiều đuôi nhọn, hai khăn vai, bờm tóc to, mặt nạ sừng hai nhánh cao, trượng bên trái có cầu lửa trong đầu vuốt, tay "
         "cầm trượng, tay vuốt giơ bên phải, dây bện và hai gai sao ở ngực). Lấy chỗ đặt, cỡ, hình bóng, thứ tự chồng"),
        (KIEM_SI,
         "an approved hero of the same game (an armoured monkey samurai), 1536x1024, white background: match EXACTLY its wobbly "
         "dark-brown pen line, its visible crayon hatching, its completely flat colouring, its bold readable shapes and its fierce "
         "battle-ready attitude. Do NOT copy its species, its design or its colours.",
         "Voọc Tướng đã duyệt (1536 × 1024, nền trắng): khỉ samurai giáp lục. Lấy nét bút rung, vân sáp, tô phẳng, thần thái chiến"),
        (CUNG_LUA,
         "another approved hero of the same game, a fire-element archer in burnt armour with a flame plume, 1536x1024, white "
         "background: see how its FIRE is drawn (three nested flat colour zones, wobbly ink outline, crayon hatching, no glow). Do "
         "NOT copy its design, its armour or its colours.",
         "Quỷ lửa bắn cung (tướng 3 đảo Hỏa, bản concept A; 1536 × 1024, nền trắng): kỵ sĩ giáp cháy nâu đen, chùm lửa ba màu trên mũ. "
         "Lấy cách vẽ lửa"),
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
    cx, cy, cr = B["cau_tam"]
    gd = [f"# Gói gửi GPT: `{CODE}` (pháp sư lửa, tướng thứ 6 đảo Hỏa, tên chưa đặt)", "",
          "Làm 2026-11-13: dựng trên rig của con gốc `monster_3481` (pháp sư bóng ma cầm trượng có con mắt, tay vuốt rời). Ba hướng màu "
          "là đề xuất của Claude, chờ người dùng chọn và duyệt concept. Ghi chú: `ArtGen/Spine/inbox/phap_lua_ghichu.md`.",
          "", "Lượt mảnh chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    ra = []
    for kieu, d in D.items():
        R = refs(kieu)
        missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
        if missing:
            raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
        out = os.path.join(save_dir(), f"L1_{kieu}.png")
        p = os.path.join(pk(), f"luot_1_concept_{kieu}.txt")
        body = BODY.format(
            ao=xy(B["ao"]), ao_ten=d["ao_ten"], choang_trai=xy(B["choang_trai"]), choang_phai=xy(B["choang_phai"]),
            choang_ten=d["choang_ten"], day=xy(B["day"]), day_ten=d["day_ten"], sao_trai=xy(B["sao_trai"]),
            sao_phai=xy(B["sao_phai"]), sao_ten=d["sao_ten"], toc=xy(B["toc"]), toc_ten=d["toc_ten"], mat_na=xy(B["mat_na"]),
            mat_ten=d["mat_ten"], sung_phai=xy(B["sung_phai"]), sung_trai=xy(B["sung_trai"]), ngoc=xy(B["ngoc"]),
            giap_ten=d["giap_ten"], truong=xy(B["truong"]), truong_ten=d["truong_ten"], cx=cx, cy=cy, cr=cr,
            l0=LUA[0], l1=LUA[1], l2=LUA[2], cy0=B["cau_lua"][1], tay_truong=xy(B["tay_truong"]), tay_ten=d["tay_ten"],
            tay_vuot=xy(B["tay_vuot"]))
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "",
              "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
              "approved hero images.", "",
              "CREATURE: a FIRE MAGE SPIRIT, a fire-element hero of the volcano island in a monster-collecting game: a floating "
              "robed wraith-like sorcerer creature with a horned mask, a huge mane, two detached clawed hands and a staff whose "
              "head holds a ball of fire that burns all the time. It is a spirit creature (an elemental monster), NOT a human "
              "wizard, NOT a skeleton, NOT a robot.", "",
              STANCE, "",
              "Follow the LAYOUT GUIDE (image 1) for WHERE every piece is on the canvas, HOW BIG it is, its SILHOUETTE and WHICH "
              "piece overlaps which. Coordinates below are pixels on the 1536x1024 canvas (x from the left, y from the top). LEFT "
              "and RIGHT are always the viewer's left and right.", "",
              body, "", SIMPLE.format(lua_them=d["lua_them"]), "",
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
    gd += ["Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/phap_lua_bo_cuc.py all`).",
           "", "## Kiểm chung", ""]
    gd += [f"- {c}" for c in CHECK_CHUNG]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    ghi(os.path.join(pk(), "HUONG_DAN.md"), gd)
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 2: đổi dáng ÁO CHOÀNG (người dùng 2026-11-13: "nhìn concept đầu, áo
# choàng bị giống con gốc quá"). Giữ nguyên mọi thứ khác của bản nháp, chỉ vẽ lại áo thân + hai khăn vai theo dáng khác hẳn con gốc.
AO = {
    "ao_lua": dict(
        ten="áo cháy thành lửa: nửa trên là áo vải đỏ thẫm mép cháy sém, nửa dưới thân là khối lưỡi lửa; khăn vai thành áo choàng vai ngắn có một đuôi nhọn dài",
        en=("A ROBE THAT BURNS AWAY INTO FIRE.\n"
            "- UPPER BODY (from the neck down to about y = 650): a fitted robe of dark crimson cloth (#A32E22), widest at about "
            "y = 620 (about x = 600 to x = 1090). Its lower edge is NOT cut into tails: it is an irregular, wavy BURNT edge with a "
            "thin charred rim of charcoal (#3C353B).\n"
            "- LOWER BODY (from the burnt edge down to about y = 900): instead of cloth, the body continues as a MASS OF FIRE, as if "
            "the spirit floats on its own flame: five or six big flame tongues growing out from under the burnt edge and streaming "
            "DOWN and a little to the LEFT, each with a thick base, a soft S-curve and a sharp curled tip, of clearly different "
            "lengths (the longest in the middle reaching about y = 900, the outer ones shorter and leaning outward); three nested "
            f"flat colours (red-orange {LUA[0]} outside, orange {LUA[1]}, yellow {LUA[2]} inside), drawn like the flames of the "
            "staff. The fire part spans about x = 560 to x = 1150.\n"
            "- SHOULDERS: the two capes become ONE short MANTLE lying over both shoulders, charcoal (#3C353B) with a pale gold "
            "(#E2B24C) trim line along its lower edge, the lower edge a smooth curve. On the LEFT it continues behind the staff "
            "hand as ONE long narrow tapering TAIL that flies out to the lower left and ends in a single sharp point at about "
            "x = 330, y = 730 (no squarish flap, no notches). On the right it ends short at the shoulder (about x = 1130, y = 590)."),
        check="Nửa trên áo vải đỏ thẫm, mép dưới cháy sém; nửa dưới là **khối lưỡi lửa** chảy xuống (không còn các đuôi nhọn kiểu lá phong); khăn vai thành áo vai ngắn, bên trái kéo một **đuôi nhọn dài**."),
    "ao_chuong": dict(
        ten="áo chuông thầy pháp: áo dài loe hình chuông, gấu lượn sóng tròn có dải lửa bốc từ gấu lên; khăn vai thành khăn quàng dài đuôi én",
        en=("A SORCERER'S BELL ROBE.\n"
            "- THE ROBE: one long closed robe of dark crimson cloth (#A32E22) that widens steadily from the neck down to a WIDE hem "
            "like a bell or a long gown (at the hem about x = 540 to x = 1170, the hem at about y = 860 to y = 890). The hem is ONE "
            "soft wavy line of four or five broad ROUNDED scallops, like the swaying edge of a heavy curtain: NO points, NO tails, "
            "NO rips. One long fold line runs down the front from under the braid to the hem, and two more fold lines fan out from "
            "the chest to the hem.\n"
            "- HEM OF FIRE: along the whole hem a broad band of orange (#E8782A), about 90 px tall, whose UPPER border is a row of "
            "flame tongues licking up into the crimson cloth (as if the hem were burning), with a thin yellow (#FFD45A) core in the "
            "bigger tongues.\n"
            "- SHOULDERS: the two capes become a long SCARF (a stole) of charcoal (#3C353B) with a pale gold (#E2B24C) trim line, "
            "laid over both shoulders. Its LEFT end flies out long to the lower left behind the staff hand and ends in a forked "
            "SWALLOW-TAIL (two points, the lower one at about x = 320, y = 740); its RIGHT end is short and hangs to about "
            "x = 1140, y = 620, also with a small forked end."),
        check="Áo dài **loe hình chuông**, gấu là một đường lượn sóng **tròn** (không nhọn, không rách), có **dải lửa cam** bốc từ gấu lên; khăn vai thành **khăn quàng** than viền vàng, đầu trái dài đuôi én."),
    "ao_tang": dict(
        ten="áo nhiều tầng lông phượng: ba tầng vạt hình lông vũ chồng nhau, đỏ thẫm → đỏ → cam ngọn vàng; khăn vai cắt vạt lông vũ",
        en=("A LAYERED PHOENIX-FEATHER CLOAK.\n"
            "- THE ROBE is built from THREE overlapping TIERS of big feather-shaped lappets (like the layered feathers of a "
            "phoenix, or overlapping petals), each tier hanging over the next one:\n"
            "  * top tier (under the shoulders, down to about y = 650): dark crimson (#8A2A22), a row of four or five lappets;\n"
            "  * middle tier (down to about y = 780): crimson red (#C2382A), a row of five or six lappets, wider than the top tier;\n"
            "  * bottom tier (down to about y = 890): orange (#E8782A) with yellow (#FFD45A) tips, five or six long lappets.\n"
            "  Every lappet is a smooth long leaf / feather shape with a softly POINTED rounded (ogive) tip and ONE centre line (the "
            "feather shaft); in each tier the middle lappets are longer than the outer ones, the outer ones lean outward, so the "
            "whole robe has the silhouette of a closed fan of tail feathers, widest at about y = 760 (about x = 540 to x = 1160). "
            "No ragged straight-edged tails, no rips.\n"
            "- SHOULDERS: the two capes stay where they are and stay charcoal (#3C353B) with the pale gold (#E2B24C) trim line, but "
            "their lower edges are cut into the same feather lappets: the big left cape ends at the lower left in THREE long "
            "feather lappets fanning out (tips at about x = 310 to x = 420, y = 690 to y = 760) instead of the squarish flap; the "
            "small right cape ends in two short lappets."),
        check="Áo là **ba tầng vạt lông vũ** chồng nhau (đỏ thẫm, đỏ, cam ngọn vàng), mỗi vạt đầu nhọn bo tròn có một gân giữa; bóng dáng như chùm lông đuôi xoè; khăn vai trái tận cùng bằng **ba vạt lông**."),
}


def build_ao():
    nhap = os.path.join(save_dir(), "L1_ao_do.png")
    gd = ["", "## Lượt 2: đổi dáng áo choàng (2026-11-13)", "",
          "Người dùng xem lượt 1: \"nhìn concept đầu, áo choàng bị giống con gốc quá\". Giữ nguyên mọi thứ của bản A (`L1_ao_do.png`), chỉ vẽ "
          "lại áo thân + hai khăn vai theo dáng khác hẳn con gốc. Ba kiểu là đề xuất của Claude.", ""]
    ra = []
    for kieu, d in AO.items():
        out = os.path.join(save_dir(), f"L2_{kieu}.png")
        p = os.path.join(pk(), f"luot_2_ao_{kieu}.txt")
        R = [(nhap, "the CURRENT DRAFT of our character, 1536x1024, white background: a floating fire-mage spirit with a horned dark "
                    "mask, a big pale mane, a staff at the left whose claw-like head holds a burning ball of fire, a staff hand, an open "
                    "claw hand at the right, a gold braid and two star spikes on the chest, a crimson ragged robe with an orange inner "
                    "zone and two charcoal shoulder capes with gold trim. Everything EXCEPT the robe and the two capes is final.",
              "Bản nháp A lượt 1 (1536 × 1024, nền trắng): pháp sư lửa lơ lửng, mặt nạ sừng đen, bờm tóc kem, trượng có cầu lửa bên trái, tay "
              "vuốt bên phải, áo đỏ rách nhiều đuôi nhọn, hai khăn vai than viền vàng. Giữ nguyên mọi thứ trừ áo và khăn vai"),
             (CUNG_LUA, "an approved hero of the same game (a fire archer with a flame plume), 1536x1024: ONLY to see how fire is drawn "
                        "in this game (three nested flat colour zones, wobbly ink outline, no glow). Do NOT copy its design.",
              "Quỷ lửa bắn cung bản A (1536 × 1024): chỉ lấy cách vẽ lửa")]
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L2_{kieu}_2.png, L2_{kieu}_3.png ... in the same folder. Do not edit, "
              "move or delete any other file.", "",
              "TASK: redraw image 1 with ONLY its CLOAK changed (the robe body and the two shoulder capes). Same 1536x1024 canvas, same "
              "pure-white background.", "",
              "KEEP IDENTICAL (same place, same size, same shapes, same colours, same hand-drawn line; if the new picture were laid over "
              "image 1, all of these must coincide): the staff with its claw-like head, the ball of fire and its flames; the staff hand "
              "with its wispy wrist; the whole hair mane; the mask, the two horn pieces and the gem; the open claw hand with its wispy "
              "wrist and five claws; the gold braid and the two four-pointed star spikes on the chest. The figure still floats: NO legs, "
              "NO feet, NO arms, no ground.", "",
              "CHANGE ONLY THE CLOAK. In image 1 the robe is a ragged cloth whose lower edge is cut into big straight-edged pointed "
              "tails like a maple leaf, and the big left cape ends in a squarish notched flap: that silhouette must GO. Replace it by "
              "this new design, which must read as a clearly DIFFERENT silhouette at first glance, while filling about the same area "
              "of the canvas (the body still hangs below the mask, between about x = 520 and x = 1190, down to about y = 900; the left "
              "cape still reaches out to the lower left behind the staff hand to about x = 320):", "",
              d["en"], "",
              "The robe still rises behind the mask to the neck, and the orange colour still shows through the two eye slits of the "
              "mask. The staff shaft and the staff hand stay IN FRONT of the cloak; the braid and the stars stay in front of the robe; "
              "the hair and the claw-hand wrist overlap the capes as in image 1.", "",
              "STYLE: exactly as image 1: wobbly dark-brown ink outline (#2B2118, about 5 px; about 3 px for inner lines), flat colours "
              "with visible crayon hatching, NO shading, NO shadows, NO highlights, NO glow, NO gradients, no sparks, no smoke. Few "
              "details: only the lines listed. Only warm colours as listed: no blue, green, purple or pink.", "", BG]
        ghi(p, t)
        ra.append(p)
        gd += [f"### Kiểu `{kieu}`: {d['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += ["", f"Kiểm: {d['check']} Mọi thứ khác trùng bản nháp A.", ""]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2: đổi dáng áo choàng")[0].rstrip("\n")
    ghi(hd, [cu] + gd)
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 3: đổi dáng MẶT (người dùng 2026-11-13: "các dạng D E F mặt vẫn bị
# giống con gốc, bạn đổi dạng mặt nó đi"). Mặt nạ + sừng + ngọc đều là mảnh cứng trên một xương đầu nên đổi dáng tự do. Giữ nguyên mọi thứ
# khác của bản nháp (mặc định bản D áo cháy thành lửa), chỉ vẽ lại cái đầu.
MAT = {
    "mu_trum": dict(
        ten="mũ trùm pháp sư: mũ trùm than viền vàng chóp nhọn ngả về sau, trong mũ tối đen chỉ thấy hai mắt lửa; không sừng",
        en=("A SORCERER'S HOOD WITH BURNING EYES, no horns at all.\n"
            "- THE HOOD: a deep pointed cowl of charcoal cloth (#3C353B) pulled over the head, seen almost from the front and turned "
            "a little to the right. Its outline is a soft rounded hood, about x = 770 to x = 960 and y = 250 to y = 520, whose "
            "pointed TIP rises above the head and droops back to the LEFT (tip at about x = 760, y = 200). Around the face opening "
            "runs a broad hem of pale gold (#E2B24C). Two short pointed lappets of the hood hang down at the sides of the opening "
            "onto the shoulders.\n"
            "- THE FACE: inside the opening there is NO face, only flat darkness (#1F1A1E), and in it two big slanted, angry, "
            "almond-shaped EYES of fire (orange #F7902A with a yellow #FFD45A centre), tilted down toward the middle. No nose, no "
            "mouth, no skin.\n"
            "- ON THE BROW of the hood, in the middle of the gold hem above the eyes, the small diamond-shaped yellow gem (#FFD45A)."),
        check="**Mũ trùm** than viền vàng, chóp nhọn ngả về sau trái; trong mũ tối đen, chỉ có **hai mắt lửa** xếch; không còn sừng và mặt nạ mỏ nhọn."),
    "sung_cuu": dict(
        ten="mặt nạ quỷ sừng cừu: mặt nạ than có mày cau, hai mắt lửa, cằm nhọn, hai sừng cừu to cuộn xoắn màu tro kem hai bên",
        en=("A DEMON MASK WITH TWO BIG CURLED RAM HORNS.\n"
            "- THE MASK: one solid shield-shaped mask of charcoal black (#2F2A30), about x = 790 to x = 940 and y = 300 to y = 520: "
            "a broad flat forehead, a heavy V-shaped frowning brow ridge, two slanted eye openings filled with fire (orange #F7902A "
            "with a yellow #FFD45A centre), flat cheeks and a short pointed chin. One ink line down the middle of the forehead. No "
            "nose, no mouth, no teeth.\n"
            "- THE HORNS: from the two upper corners of the mask grow two BIG thick RAM HORNS of pale ash-cream (#E9E1D2, like the "
            "hair), each curling outward, down and round in ONE full spiral turn beside the cheek (like the horns of a ram), with "
            "four or five ring grooves across it. The left horn curls at about x = 690 to x = 800, y = 290 to y = 460; the right "
            "horn, a little smaller because the head is turned, at about x = 930 to x = 1010, y = 300 to y = 450. The horns do "
            "NOT rise above the head.\n"
            "- Between the horns, on top of the forehead, the small diamond-shaped yellow gem (#FFD45A) in a little gold setting."),
        check="Mặt nạ than hình khiên có **mày cau chữ V**, hai mắt lửa, cằm nhọn; hai **sừng cừu to cuộn xoắn** màu tro kem hai bên má; không còn hai nhánh sừng thẳng đứng."),
    "trang_khuyet": dict(
        ten="mặt nạ sứ + mào trăng khuyết: mặt nạ trái xoan màu tro kem có hai hốc mắt hình ngọn lửa, trên trán một mào hình trăng khuyết lớn than viền vàng",
        en=("A PALE MASK WITH A BIG CRESCENT CREST.\n"
            "- THE MASK: a smooth oval mask of pale ash-cream (#E9E1D2), like porcelain, about x = 800 to x = 930 and y = 330 to "
            "y = 525, narrowing to a small pointed chin. In it two EYE HOLES shaped like small upright flames (teardrops with the "
            "point up and outward), filled with fire (orange #F7902A with a yellow #FFD45A centre), slanted so the mask looks "
            "stern. Under each eye one short dark ink streak like a tear mark. No nose, no mouth.\n"
            "- THE CREST: fixed on the forehead of the mask, a BIG CRESCENT like a moon lying on its back (a wide U), charcoal black "
            "(#2F2A30) with a pale gold (#E2B24C) rim: its two sharp points sweep up and outward to about x = 730, y = 200 (left) "
            "and x = 990, y = 215 (right); its thick middle sits on the brow at about y = 330. In the middle of the crescent, on "
            "the brow, the small diamond-shaped yellow gem (#FFD45A).\n"
            "- A short dark charcoal cowl frames the sides of the mask (two narrow strips beside the cheeks)."),
        check="Mặt nạ **trái xoan tro kem** nhẵn như sứ, hai hốc mắt **hình ngọn lửa**, vệt mực dưới mắt; trên trán **mào trăng khuyết lớn** than viền vàng (hình chữ U rộng); không còn sừng thẳng và mặt nạ mỏ nhọn."),
}


def build_mat(nen="ao_lua"):
    nhap = os.path.join(save_dir(), f"L2_{nen}.png")
    if not os.path.exists(nhap):
        raise SystemExit("thiếu bản nháp: " + nhap)
    gd = ["", "## Lượt 3: đổi dáng mặt (2026-11-13)", "",
          "Người dùng xem lượt 2: \"các dạng D E F mặt vẫn bị giống con gốc, bạn đổi dạng mặt nó đi, animation tôi thấy khá ổn rồi\". Giữ "
          f"nguyên mọi thứ của bản `L2_{nen}.png`, chỉ vẽ lại cái đầu (mặt nạ, sừng, ngọc). Ba kiểu là đề xuất của Claude; mặt là mảnh cứng "
          "trên một xương nên ghép được với dáng áo nào cũng được.", ""]
    ra = []
    for kieu, d in MAT.items():
        out = os.path.join(save_dir(), f"L3_{kieu}.png")
        p = os.path.join(pk(), f"luot_3_mat_{kieu}.txt")
        R = [(nhap, "the CURRENT DRAFT of our character, 1536x1024, white background: a floating fire-mage spirit with a big pale "
                    "mane, a staff at the left whose claw-like head holds a burning ball of fire, a staff hand, an open claw hand at "
                    "the right, a gold braid and two star spikes on the chest, a charcoal mantle with gold trim and a crimson robe "
                    "that burns away into flames below. Its HEAD is a dark beak-like mask with two tall thin horn prongs standing "
                    "side by side, two curved hook horns and a diamond gem. Everything EXCEPT the head is final.",
              "Bản nháp lượt 2 (1536 × 1024, nền trắng): pháp sư lửa, trượng cầu lửa bên trái, tay vuốt bên phải, bờm tóc kem, áo vai than "
              "viền vàng, áo đỏ cháy thành lửa; đầu là mặt nạ mỏ nhọn có hai nhánh sừng cao + hai móc sừng. Giữ nguyên mọi thứ trừ cái đầu")]
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L3_{kieu}_2.png, L3_{kieu}_3.png ... in the same folder. Do not edit, "
              "move or delete any other file.", "",
              "TASK: redraw image 1 with ONLY its HEAD changed (the mask, the horns and the gem). Same 1536x1024 canvas, same "
              "pure-white background.", "",
              "KEEP IDENTICAL (same place, same size, same shapes, same colours, same hand-drawn line; if the new picture were laid over "
              "image 1, all of these must coincide): the staff with its claw-like head, the ball of fire and its flames; the staff hand; "
              "the open claw hand with its wispy wrist and five claws; the gold braid and the two four-pointed star spikes on the chest; "
              "the charcoal mantle with its gold trim and its long pointed tail at the left; the crimson robe with its burnt edge and "
              "the mass of flames below it; the whole pale hair mane (same outline, same strand lines).", "",
              "CHANGE ONLY THE HEAD. In image 1 the head is a narrow dark beak-like mask pointing down, with two tall thin horn prongs "
              "standing close together like a tuning fork, a curved hook horn at each side and a gem between the prongs: that whole "
              "design must GO (no tall prongs, no hook horns, no beak). Replace it by the new head below, which must read as a clearly "
              "DIFFERENT face and silhouette at first glance. The new head sits at the SAME place and is about the same size (centred "
              "at about x = 865, y = 420, in front of the hair, above the braid), is seen almost from the front and turned a little "
              "toward the viewer's RIGHT, and looks stern and battle-ready (angry slanted eyes), not cute, not smiling, not gory:", "",
              d["en"], "",
              "Where the old horns covered the hair, continue the hair mane behind the new head (same pale ash-cream, same flowing "
              "strand lines). The head is ONE compact group of a few clear closed shapes with complete ink outlines (it will be cut "
              "out and animated as rigid pieces). The fire of the eyes is flat colour: NO glow, no halo.", "",
              "STYLE: exactly as image 1: wobbly dark-brown ink outline (#2B2118, about 5 px; about 3 px for inner lines), flat colours "
              "with visible crayon hatching, NO shading, NO shadows, NO highlights, NO glow, NO gradients, no sparks, no smoke. Few "
              "details: only what is listed. Only the colours listed: no blue, green, purple or pink.", "", BG]
        ghi(p, t)
        ra.append(p)
        gd += [f"### Kiểu `{kieu}`: {d['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += ["", f"Kiểm: {d['check']} Mọi thứ khác trùng bản nháp.", ""]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 3: đổi dáng mặt")[0].rstrip("\n")
    ghi(hd, [cu] + gd)
    for p in ra:
        print(p)


if __name__ == "__main__":
    if sys.argv[1:2] == ["mat"]:
        build_mat(*sys.argv[2:3])
    elif sys.argv[1:2] == ["ao"]:
        build_ao()
    else:
        main()
