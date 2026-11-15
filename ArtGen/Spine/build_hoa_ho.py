# -*- coding: utf-8 -*-
"""Gói GPT vẽ hổ lửa đảo Hỏa (mã làm việc hoa_ho, con gốc của rig: monster_3645). Tướng thứ 9 đảo Hỏa (suất hoa_tinh, ải 60).

Người dùng (2026-11-14): "concept hổ lửa, bạn phải giữ được kiểu style của nó như này (phần mây xung quanh đổi sang kiểu mây đỏ lửa hoặc
làm lại như họ), bỏ sừng đi, bỏ chuông ở dưới đi". Ba hướng màu dưới đây là ĐỀ XUẤT của Claude, chờ người dùng chọn. Chỉ lấy của con gốc
cách dựng (chỗ đặt, cỡ, thứ tự chồng từng part); hình là của mình. Không đính ảnh con gốc; đính sơ đồ bố cục tự dựng bằng mã
(hoa_ho_bo_cuc.py).

    py -3 -I ArtGen/Spine/hoa_ho_bo_cuc.py all
    py -3 -I ArtGen/Spine/build_hoa_ho.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/hoa_ho_1/luot_1_concept_<hướng>.txt [--note "..."]
"""
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "hoa_ho"
K = 1
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
VIEM_DAO = os.path.join(HERE, "inbox", "quy_dao_1", "tai_ve", "L1_duyet.png")
GIAC_MOC = os.path.join(HERE, "inbox", "giac_moc_1", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def pk():
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{K}")


def save_dir():
    return os.path.join(HERE, "inbox", f"{CODE}_{K}", "tai_ve")


def mau_dir():
    return os.path.join(HERE, "inbox", f"{CODE}_{K}", "mau")


def co(p):
    w, h = Image.open(p).size
    return f"{w}x{h}", f"{w} × {h}"


STANCE = ("STANCE (the same in the layout guide, image 1): a huge, heavy, muscular TIGER standing on all FOUR legs in a low, wide, "
          "planted battle stance, seen from the side and slightly from the front, facing the viewer's RIGHT. The chest and "
          "shoulders are massive and raised; the back slopes down to lower hindquarters at the left. The head sits at the upper "
          "right on a thick short neck, chin slightly lifted, turned in a three-quarter view toward the right so that mainly "
          "ONE eye is seen clearly. The FAR foreleg is stretched forward to the right with its big paw flat on the ground; the "
          "NEAR foreleg stands under the chest, its huge paw in the middle foreground; both hind legs are planted at the left. "
          "The long thick tail rises from the rump at the left and curls up in an S above the back. The mouth is CLOSED, with "
          "two long sabre fangs showing. Proud, fierce, ready to pounce; a noble guardian beast, appealing, not horror, not a "
          "smiling cute mascot, not a chibi.")

BODY = (
    "- HEAD (about x = 865 to x = 1120, y = 190 to y = 460; one solid piece): a broad, heavy tiger head with a strong square "
    "muzzle pointing to the right (nose at about x = 1100, y = 345), a thick ruff of jagged cheek fur and a bearded chin "
    "(about x = 880 to x = 1090, y = 380 to y = 460). ONE sharp, narrow, slanted EYE at about x = 1040, y = 282 under a heavy "
    "angry brow; {mat} A small triangular nose, a firm closed mouth line turned down. TWO long curved SABRE FANGS hang from the "
    "upper jaw: the near one from about (1000, 345) down to its tip at about (990, 432), the far one shorter at about "
    "(1080, 385) to (1075, 440); {nanh} On the near cheek, below the eye (about x = 920 to x = 1040, y = 315 to y = 350), one "
    "bold curled SWIRL MARK like a brush stroke ending in a spiral; a second small swirl mark by the nose at about "
    "x = 1105 to x = 1140, y = 350 to y = 385. {mat_hoa}\n"
    "- EARS: two small rounded tiger ears. NEAR ear at the top left of the head (about x = 862 to x = 940, y = 176 to "
    "y = 269), FAR ear at the top right (about x = 1075 to x = 1130, y = 253 to y = 310). {tai}\n"
    "- NO HORN: the top of the head carries NO horn of any kind. Instead, on the forehead and brow (about x = 887 to "
    "x = 1102, y = 144 to y = 251) sit THREE small licking FLAME TUFTS like fiery eyebrows and a forelock, the tallest one "
    "at about x = 900 to x = 940, y = 144 to y = 200. {chom}\n"
    "- FIRE-CLOUD MANE (the key feature of this creature; about x = 315 to x = 972, y = 169 to y = 578): instead of a normal "
    "mane, about TWELVE separate FIRE CLOUDS grow from the back of the head, the neck, the shoulders and the back and stream "
    "backward to the LEFT as if in a strong wind. Each one is a hybrid of a stylised East-Asian auspicious cloud and a "
    "flame: a flat ribbon-like shape with a rounded, curled SPIRAL HEAD and one to three long tapering, curling TONGUES "
    "ending in sharp hooked tips; inside each cloud one thin spiral line follows the curl. They overlap like roof tiles, "
    "big ones over the shoulder (about x = 580 to x = 920, y = 300 to y = 580), long thin streamers at the top (tips at "
    "about (650, 175), (580, 275), (430, 365) and (460, 440)). {may}\n"
    "- CHEST FLAMES (about x = 1040 to x = 1166, y = 428 to y = 712): down the FRONT edge of the chest, from the throat to "
    "the far elbow, a ragged strip of the same fire with three or four sharp spikes pointing forward to the right. {may_nguc}\n"
    "- HAUNCH FIRE CLOUDS (about x = 392 to x = 786, y = 488 to y = 732): on the flank and the near thigh lie three more fire "
    "clouds: one big hooked swirl with two horn-like curled tips in the middle of the flank (about x = 540 to x = 786, "
    "y = 490 to y = 665), and one long cloud with a spiral head trailing to the left across the near thigh (about x = 392 "
    "to x = 665, y = 625 to y = 732).\n"
    "- BODY (about x = 401 to x = 1060, y = 234 to y = 776): a massive barrel chest in front (its lowest point at about "
    "x = 850, y = 775), a strong back and a rounded rump at the left (about x = 340 to x = 560, y = 540 to y = 760). The "
    "chest and belly are plain FUR. NO armour, NO chest plate, NO bell, NO ring, nothing hanging under the body. {long}\n"
    "- TAIL (about x = 274 to x = 612, y = 62 to y = 583): long and thick; it leaves the rump at about (345, 545), sweeps left "
    "and up to about (280, 400), then curves right and up to its tip at about (550, 70). The last part (about x = 490 to "
    "x = 612, y = 62 to y = 230) is a thick brush. {duoi} ONE fire cloud with a big curled spiral head hooks around the bend of "
    "the tail (about x = 198 to x = 406, y = 254 to y = 400), one small one sits on the tail lower down (about x = 240 to "
    "x = 340, y = 460 to y = 502), and one long thin streamer crosses the tail below the brush (about x = 315 to x = 610, "
    "y = 198 to y = 262).\n"
    "- LEGS (FOUR, all visible, very thick and muscular, each ending in a HUGE broad paw with FOUR toes and four big hooked "
    "claws): NEAR FORELEG in front of everything (about x = 479 to x = 843, y = 412 to y = 970; its paw at about x = 535 to "
    "x = 890, y = 820 to y = 970, the biggest paw). NEAR HIND LEG at the far left (about x = 248 to x = 544, y = 546 to "
    "y = 968; paw at about x = 250 to x = 395, y = 895 to y = 965). FAR FORELEG stretched forward at the right (about "
    "x = 840 to x = 1342, y = 415 to y = 952; paw at about x = 1100 to x = 1340, y = 835 to y = 950). FAR HIND LEG between "
    "the near legs, mostly hidden (about x = 600 to x = 892, y = 531 to y = 955; paw at about x = 730 to x = 890, y = 860 "
    "to y = 950). {chan}\n"
    "- ANKLE BANGLES: around each ankle, just above the paw, floats ONE open C-shaped BANGLE (a broken ring, not closed, "
    "about 25 px thick), tilted like a hoop seen from the side: near foreleg (about x = 480 to x = 735, y = 750 to y = 850), "
    "near hind leg (about x = 220 to x = 405, y = 790 to y = 870), far hind leg (about x = 700 to x = 835, y = 820 to "
    "y = 870), far foreleg (about x = 1075 to x = 1225, y = 785 to y = 840). {vong} A small fire cloud with a spiral curls "
    "on the far fore ankle (about x = 975 to x = 1075, y = 760 to y = 830).")

FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the figure is about 1150 px wide (from the fire cloud on the tail at about "
         "x = 198 to the far front paw at about x = 1342) and about 910 px tall (from the tail tip at about y = 62 to the paws "
         "at about y = 970). Do NOT enlarge, shrink or move the figure.")

POSE = ("ANIMATION-READY (very important: the picture will be cut into many separate pieces and animated with a 2D skeleton): "
        "calm, clean resting pose exactly as in the guide. Draw every piece as a clear, simple, closed shape with its own ink "
        "outline, so that the pieces can be separated: head / each ear / each fang / each flame tuft on the brow / EVERY single "
        "fire cloud (each keeps its own complete outline even where another one overlaps it) / body / tail / each leg (upper "
        "leg, lower leg, paw, each toe with its claw) / each bangle. No sparks, no embers in the air, no smoke, no speed lines, "
        "no glow, no ground, no grass, no props, no second character.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram made of rough blobs: take ONLY the placement, the sizes, the overlaps and the "
        "kind of colour of each piece from it, never its line, its edge noise or its exact blob shapes. Design the real shape "
        "of every piece yourself as described: bold, chunky, readable shapes with a clear silhouette and a rich but tidy "
        "amount of detail (fur tufts at the elbows, heels, cheeks and chest drawn as a few big jagged points, not as many tiny "
        "hairs), the way a carefully designed final-stage Pokemon-like legendary beast is drawn. Do not leave any piece as a "
        "plain empty blob. Do NOT copy any existing character.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 5 px thick on this canvas around every big piece, and about 3 px for "
        "small details (toes, claws, the eye, stripes, the spiral lines inside the clouds, fur points); every area coloured "
        "with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the "
        "outline), kept inside the outline. Clean and appealing, neither a crude scribble nor an over-rendered painting.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker underside, no lighter patches, no shadows of any kind (no cast shadow of one "
        "piece on another, no shadow under the figure or on the background), no white highlights or shine spots (not on the "
        "fangs, not on the claws, not on the bangles), no gloss, no reflections, no glow, no halo, no rim light, NO GRADIENTS "
        "(the fire clouds are flat colour bands with a clean edge between two colours, never a soft blend), no 3D look. The "
        "only exception: one tiny light dot in the eye. A different tone appears only where the design itself lists a "
        "different colour.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the character.")

KHONG = ("FORBIDDEN: NO horn, NO antlers, NO bell, NO chest armour, NO metal plate or pot on the chest, NO hanging ring, NO bones or "
         "bandages on the tail, NO wings, NO saddle, NO clothes, NO weapons, NO human features.")

D = {}

D["bach"] = dict(
    ten="bạch hổ mây lửa: lông trắng kem, vằn than hình lưỡi lửa, mây lửa đỏ son lõi cam xoáy vàng, vòng chân vàng đồng",
    intro=("CREATURE: a FIRE TIGER, a legendary fire-element guardian beast of a volcano island in a monster-collecting game: a "
           "huge WHITE TIGER whose mane, tail and flanks are wrapped in drifting FIRE CLOUDS (stylised East-Asian cloud "
           "scrolls made of flame). Cream-white fur with charcoal stripes shaped like small flame tongues, two sabre fangs, "
           "flame eyebrows, four gold bangles floating around its ankles. It is a real four-legged big cat, NOT a human, NOT "
           "a lion dance costume, NOT a dragon, NOT a qilin."),
    parts=dict(
        mat="the iris is bright amber gold (#F8C43C) with a thin vertical slit pupil.",
        nanh="both fangs ivory white (#FAF6E8).",
        mat_hoa="Both swirl marks are vermilion red (#D6402A). The nose is dusty rose (#C8706A).",
        tai="Cream outside, the inside of the ear soft rose (#EEAA96).",
        chom="The tufts are orange (#F49630) with a yellow (#F8C84A) core band.",
        may=("COLOUR OF EVERY FIRE CLOUD: the main body vermilion flame red (#D6402A); a narrower inner band of orange "
             "(#F49630) along the leading rounded edge and in the spiral head; the thin spiral line inside is golden yellow "
             "(#F8C84A); the very tips of the longest tongues are deep crimson (#8E2420). Clean edges between the bands."),
        may_nguc="Vermilion red (#D6402A) with crimson (#8E2420) spike tips.",
        long=("Cream-white fur (#F2ECDE). On the shoulder, flank, rump and the upper legs a few bold TIGER STRIPES, each "
              "stripe a short jagged zigzag shape like a small flame tongue or a lightning mark, charcoal grey (#5A5458); "
              "about four on the chest and shoulder, three on the flank, two or three on each upper leg. The fur edge at the "
              "chest front and under the belly is drawn as a few big jagged points."),
        duoi=("Cream white with six or seven charcoal zigzag stripe bands across it; the brush at the tip is charcoal grey "
              "(#5A5458) shaped like a soft flame with two or three jagged cream stripes."),
        chan=("Legs cream-white with the zigzag stripes on the upper part; the paws a slightly warmer cream (#E2D6C4); the "
              "claws dark charcoal (#3A3438), big and hooked. Jagged fur tufts at the elbows and heels."),
        vong=("The bangles are antique gold (#E2AA3E) with a darker gold (#B47E2A) line engraved along the middle and three "
              "or four small notches; the open ends are cut square.")),
    palette=("COLOURS (use exactly these, each area one flat colour): fur cream white (#F2ECDE); paws warmer cream (#E2D6C4); "
             "stripes and tail brush charcoal grey (#5A5458); claws dark charcoal (#3A3438); fire clouds vermilion (#D6402A) "
             "with orange (#F49630) bands, golden yellow (#F8C84A) spiral lines and crimson (#8E2420) tips; brow flames "
             "orange and yellow; swirl marks on the face vermilion; eye amber gold (#F8C43C); fangs ivory (#FAF6E8); inner "
             "ear rose (#EEAA96); bangles antique gold (#E2AA3E / #B47E2A); every outline dark-brown ink (#2B2118). Only "
             "these colours. NO blue, NO teal, NO green, NO purple, NO black-to-red gradients."),
)

D["cam"] = dict(
    ten="hổ cam vằn đen, bụng và mõm kem, mây lửa đỏ thẫm viền vàng, vòng chân sắt đen",
    intro=("CREATURE: a FIRE TIGER, a legendary fire-element guardian beast of a volcano island in a monster-collecting game: a "
           "huge ORANGE TIGER whose mane, tail and flanks are wrapped in drifting FIRE CLOUDS (stylised East-Asian cloud "
           "scrolls made of flame). Bright tiger-orange fur with near-black stripes shaped like small flame tongues, a cream "
           "muzzle, chest and paws, two sabre fangs, flame eyebrows, four dark iron bangles floating around its ankles. It "
           "is a real four-legged big cat, NOT a human, NOT a lion dance costume, NOT a dragon, NOT a qilin."),
    parts=dict(
        mat="the iris is bright yellow (#FADC5A) with a thin vertical slit pupil.",
        nanh="both fangs ivory white (#FAF6E8).",
        mat_hoa=("Both swirl marks are near-black brown (#3C2C28). The muzzle, the chin beard and the cheek ruff are cream "
                 "(#F6E2C4); the nose is dark rose (#B45A50)."),
        tai="Orange outside with a near-black tip, the inside cream (#F6E2C4).",
        chom="The tufts are golden yellow (#F8C446) with a deep red (#AA2824) base.",
        may=("COLOUR OF EVERY FIRE CLOUD: the main body deep flame red (#AA2824); a narrow band of golden yellow (#F8C446) "
             "along the leading rounded edge and around the spiral head, like a gold lining; the thin spiral line inside is "
             "also golden yellow; the very tips of the longest tongues are dark maroon (#5E1C1C). Clean edges between the bands."),
        may_nguc="Deep red (#AA2824) with a golden yellow (#F8C446) edge.",
        long=("Tiger orange fur (#EE943C); the throat, the lower chest and the belly cream (#F6E2C4) with a jagged border "
              "between orange and cream. On the shoulder, flank, rump and the upper legs bold TIGER STRIPES, each stripe a "
              "short jagged zigzag shape like a small flame tongue, near-black brown (#3C2C28); about four on the chest "
              "and shoulder, three on the flank, two or three on each upper leg."),
        duoi=("Tiger orange with six or seven near-black zigzag stripe bands across it; the brush at the tip is near-black "
              "brown (#3C2C28) shaped like a soft flame."),
        chan=("Legs tiger orange with the zigzag stripes on the upper part; the paws cream (#F6E2C4); the claws near-black "
              "(#2E2628), big and hooked. Jagged fur tufts at the elbows and heels."),
        vong=("The bangles are dark iron (#464046) with one thin line of golden yellow (#F8C446) inlaid along the middle and "
              "three or four small notches; the open ends are cut square.")),
    palette=("COLOURS (use exactly these, each area one flat colour): fur tiger orange (#EE943C); muzzle, chest, belly and "
             "paws cream (#F6E2C4); stripes, tail brush and face marks near-black brown (#3C2C28); claws (#2E2628); fire "
             "clouds deep flame red (#AA2824) with golden yellow (#F8C446) lining and spiral lines and maroon (#5E1C1C) "
             "tips; brow flames yellow on a red base; eye yellow (#FADC5A); fangs ivory (#FAF6E8); bangles dark iron "
             "(#464046) with a gold line; every outline dark-brown ink (#2B2118). Only these colours. NO blue, NO teal, NO "
             "green, NO purple, NO white fur."),
)

D["than"] = dict(
    ten="hổ than: lông xám than, vằn cam than hồng, mây lửa cam lõi vàng, vòng chân đỏ son",
    intro=("CREATURE: an EMBER TIGER, a legendary fire-element guardian beast of a volcano island in a monster-collecting game: "
           "a huge CHARCOAL-GREY TIGER, as if made of cooled volcanic ash, whose stripes are glowing-ember orange (flat "
           "colour, not luminous) and whose mane, tail and flanks are wrapped in drifting FIRE CLOUDS (stylised East-Asian "
           "cloud scrolls made of bright flame). Two sabre fangs, flame eyebrows, four red-lacquer bangles floating around "
           "its ankles. It is a real four-legged big cat, NOT a human, NOT a lion dance costume, NOT a dragon, NOT a demon."),
    parts=dict(
        mat="the iris is bright ember orange-yellow (#FABE3C) with a thin vertical slit pupil.",
        nanh="both fangs warm ivory (#F6EEDC).",
        mat_hoa=("Both swirl marks are ember orange (#F07828). The chin beard and the cheek ruff are a lighter ash grey "
                 "(#8C868C); the nose is dark (#3C3840)."),
        tai="Charcoal outside, the inside lighter ash grey (#8C868C).",
        chom="The tufts are golden yellow (#FACC50) with an orange (#F07828) base.",
        may=("COLOUR OF EVERY FIRE CLOUD: the main body bright flame orange (#F07828); a narrower inner band of golden "
             "yellow (#FACC50) along the leading rounded edge and in the spiral head; the thin spiral line inside is pale "
             "yellow (#FCE9A0); the very tips of the longest tongues are vermilion red (#C43C2C). Clean edges between the bands."),
        may_nguc="Flame orange (#F07828) with vermilion (#C43C2C) spike tips.",
        long=("Charcoal ash-grey fur (#545058). On the shoulder, flank, rump and the upper legs bold TIGER STRIPES, each "
              "stripe a short jagged zigzag shape like a small flame tongue or a crack in cooling lava, ember orange "
              "(#F07828); about four on the chest and shoulder, three on the flank, two or three on each upper leg. The fur "
              "edge at the chest front and under the belly is drawn as a few big jagged points of lighter ash grey (#8C868C)."),
        duoi=("Charcoal grey with six or seven ember-orange zigzag stripe bands across it; the brush at the tip is a flame: "
              "orange (#F07828) with a golden yellow (#FACC50) core band."),
        chan=("Legs charcoal grey with the orange zigzag stripes on the upper part; the paws darker charcoal (#3C3840); the "
              "claws warm ivory (#F6EEDC), big and hooked. Jagged fur tufts of lighter ash grey at the elbows and heels."),
        vong=("The bangles are vermilion red lacquer (#C43C2C) with one thin line of golden yellow (#FACC50) along the "
              "middle and three or four small notches; the open ends are cut square.")),
    palette=("COLOURS (use exactly these, each area one flat colour): fur charcoal ash grey (#545058); lighter ash fur tufts "
             "(#8C868C); paws dark charcoal (#3C3840); stripes and face marks ember orange (#F07828); fire clouds flame "
             "orange (#F07828) with golden yellow (#FACC50) bands, pale yellow (#FCE9A0) spiral lines and vermilion "
             "(#C43C2C) tips; eye orange-yellow (#FABE3C); fangs and claws warm ivory (#F6EEDC); bangles vermilion lacquer "
             "(#C43C2C) with a gold line; every outline dark-brown ink (#2B2118). Only these colours. NO blue, NO teal, NO "
             "green, NO purple, NO white fur."),
)


def refs(kieu):
    c1, v1 = co(os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"))
    c2, v2 = co(VIEM_DAO)
    c3, v3 = co(GIAC_MOC)
    c4, v4 = co(WORLD_STYLE)
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         f"LAYOUT GUIDE, {c1}, white background: a flat computer-made diagram of THIS creature in its resting stance, built "
         "from rough coloured blobs: where every piece goes on the canvas, how big it is and which piece overlaps which (the "
         "head with one eye at the upper right, two ears, small flame tufts on the brow, two fangs; the many ragged fire-cloud "
         "blobs of the mane streaming to the left; the big body; the tail curling up at the left with fire clouds on it; four "
         "thick legs with broad paws; an open bangle around each ankle). Use it for placement, size and overlap only; design "
         "and redraw everything in the hand-drawn style of the approved heroes.",
         f"Sơ đồ bố cục tự dựng bằng mã ({v1}, nền trắng): các khối tô phẳng theo nhóm màu (đầu một mắt ở trên phải, hai tai, chỏm "
         "lửa nhỏ trên trán, hai nanh; các mảng mây lửa của bờm bay sang trái; thân to; đuôi cuộn lên bên trái có mây lửa; bốn chân "
         "bàn to; vòng hở quanh mỗi cổ chân). KHÔNG có sừng, KHÔNG có chuông. Lấy chỗ đặt, cỡ, thứ tự chồng"),
        (VIEM_DAO,
         f"an approved hero of the same game and the same fire island (an ash-skinned fire ogre with a great blade), {c2}, white "
         "background: match EXACTLY its wobbly dark-brown pen line, its visible crayon hatching, its completely flat colouring "
         "(see how its flames are flat colour bands, not gradients), its bold chunky shapes and its fierce battle-ready "
         "attitude. Do NOT copy its species, its design or its colours.",
         f"Viêm Đao đã duyệt ({v2}, nền trắng): quỷ lửa da tro vác đại đao, bờm lửa ba dải màu phẳng. Lấy nét bút rung, vân sáp, tô "
         "phẳng, cách vẽ lửa thành dải màu phẳng, thần thái chiến"),
        (GIAC_MOC,
         f"another approved hero of the same game (a big four-legged horned forest beast), {c3}, white background: the same "
         "line and flat crayon colouring; see how its thick four legs, broad feet and claws are drawn. Do NOT copy its "
         "species, design or colours.",
         f"Giác Mộc đã duyệt ({v3}, nền trắng): thú bốn chân to. Lấy nét, tô phẳng, cách vẽ bốn chân và bàn chân"),
        (WORLD_STYLE,
         f"the game's hand-drawn map, {c4}: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching), nothing of its content.",
         f"Bản đồ vẽ tay đã duyệt ({v4}): chỉ lấy nét bút mực nâu, vân chì sáp"),
    ]


def ghi(p, lines):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def main():
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    gd = [f"# Gói gửi GPT: `{CODE}` (hổ lửa, tướng thứ 9 đảo Hỏa, suất `hoa_tinh`, tên chưa đặt)", "",
          "Làm 2026-11-14: dựng trên rig của con gốc `monster_3645` (hổ trắng bờm mây, 197 xương, 74 mảnh). Người dùng dặn: giữ kiểu "
          "style của con gốc, mây đổi sang mây đỏ lửa, BỎ sừng, BỎ chuông. Ba hướng màu là đề xuất của Claude, chờ người dùng chọn. "
          "Ghi chú: `ArtGen/Spine/inbox/hoa_ho_ghichu.md`.", "",
          "Lượt mảnh chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    for kieu, d in D.items():
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
              d["intro"], "", STANCE, "",
              "Follow the LAYOUT GUIDE (image 1) for WHERE every piece is on the canvas, HOW BIG it is and WHICH piece overlaps "
              "which. Coordinates below are pixels on the 1536x1024 canvas (x from the left, y from the top). The viewer's LEFT "
              "side of the picture is the creature's rear; the viewer's RIGHT is where it faces. NEAR = the side of the body "
              "toward the viewer; FAR = the other side.", "",
              "PARTS:", BODY.format(**d["parts"]), "", KHONG, "", d["palette"], "", FRAME, "", POSE, "", SOFT, "", LINE, "", FLAT,
              "", BG]
        ghi(p, t)
        print(p)
        gd += [f"## Hướng `{kieu}`: {d['ten']}", "",
               f"- File prompt: `{Wp(p)}`", f"- Ảnh lưu: `{Wp(out)}` (trùng tên thì `_2`, `_3`…)", "- Ảnh mẫu:"]
        gd += [f"  {i}. `{Wp(r)}`: {vi}." for i, (r, _, vi) in enumerate(R, 1)]
        gd += [""]
    gd += ["## Cách kiểm", "",
           "- Đúng bố cục sơ đồ: hổ bốn chân nhìn sang PHẢI, chân trước xa duỗi về phải, đuôi cuộn lên bên trái, bờm mây lửa bay sang trái.",
           "- KHÔNG sừng, KHÔNG chuông, KHÔNG giáp ngực, không khuyên treo dưới bụng.",
           "- Mây lửa: từng cụm là hình khép kín có đầu xoắn và lưỡi nhọn cong, tô DẢI MÀU PHẲNG (không chuyển màu mềm, không phát sáng).",
           "- Nét bút mực nâu hơi rung, vân chì sáp, không bóng, không điểm sáng trắng; nền trắng tinh, không viền sticker.",
           "- Đủ bốn chân, mỗi bàn bốn móng; hai nanh dài; bốn vòng hở ở cổ chân.", "",
           "## Câu sửa nhanh", "",
           "- Có sừng / chuông: `--note \"Remove the horn and the bell completely: bare forehead with small flame tufts, plain fur chest.\"`",
           "- Mây chuyển màu mềm: `--note \"The fire clouds must be FLAT colour bands with clean edges, no gradient, no glow.\"`",
           "- Lệch bố cục: `--note \"Follow the layout guide exactly: same placement and size of every piece, do not move or enlarge.\"`", ""]
    ghi(os.path.join(pk(), "HUONG_DAN.md"), gd)
    print(os.path.join(pk(), "HUONG_DAN.md"))


# ---------------------------------------------------------------- lượt 2: MẢNH (sau khi concept được duyệt: tai_ve/L1_duyet.png)
# Theo đúng cách tách của rig gốc (skill mục 00): năm tờ KHUNG PART + hai tờ LIỀN (thân, đuôi, từng chân: gen liền rồi nướng bằng mã).
# Tờ hướng dẫn do hoa_ho_manh.py dựng.
CON = ("a FIRE TIGER: a huge cream-white tiger facing right, with bold charcoal zigzag stripes shaped like small flame tongues, a "
       "mane of drifting FIRE CLOUDS (flat vermilion flame-red cloud scrolls with orange bands and golden-yellow spiral curls), "
       "small flame tufts on its brow, a vermilion spiral mark on its cheek, two long sabre fangs, big cream paws with hooked "
       "charcoal claws and an open antique-gold bangle around each ankle")
LOAI = {
    "may": ("a FIRE CLOUD of the mane (a stylised East-Asian cloud scroll made of flame, exactly like the ones on image 1): "
            "vermilion flame red (#D6402A) body; inside it a narrower ORANGE (#F49630) band where the guide shows orange, with a "
            "clean edge between red and orange; in the thick rounded end ONE bold SPIRAL CURL (a golden-yellow (#F8C84A) centre "
            "with an ink line spiralling around it, as on image 1); the very tips of the long tapering tongues deep crimson "
            "(#8E2420). Keep every hooked tip and tongue of the silhouette"),
    "chom": ("a small licking FLAME tuft of the brow: orange (#F49630) with a golden-yellow (#F8C84A) core where the guide "
             "shows yellow, a clean edge between them"),
    "may_mat": "a small flame-red BROW MARK (#D6402A), plain flat red with one short darker curl line",
    "vong": ("an open ANKLE BANGLE (a piece of a hoop seen at an angle): antique gold (#E2AA3E) with ONE thin darker-gold (#B47E2A) "
             "line engraved along its middle and three or four short notches across it; ends cut square"),
    "ngon": ("ONE TOE of a paw: warm cream fur (#E2D6C4) ending in one big hooked charcoal CLAW (#3A3438) exactly where the guide "
             "shows the dark area, with an ink line between fur and claw"),
    "nanh": "a SABRE FANG, ivory white (#FAF6E8), plain, with one thin line along its curve",
    "rang": "a small row of TEETH, ivory white (#FAF6E8), plain",
    "tai": ("an EAR: cream-white (#F2ECDE) rim, soft rose (#EEAA96) inside exactly where the guide shows rose, an ink line between "
            "them, two or three short fur strokes"),
    "mat": ("the EYE (a narrow, slanted, fierce eye): a dark charcoal-brown (#463430) lid-and-lash shape that contains a bright "
            "amber-gold (#F8C43C) iris exactly where the guide shows yellow, a thin vertical slit pupil and one tiny light dot"),
    "P_tou": ("the UPPER HEAD of the tiger in three-quarter view facing RIGHT: skull, forehead, cheek, nose bridge, nose and upper "
              "lip, WITHOUT the lower jaw, WITHOUT ears, WITHOUT fangs, WITHOUT flames. The muzzle is the lower right end, the "
              "back of the skull with jagged cheek-fur points is the left side. Cream-white fur (#F2ECDE). Draw on it: a small "
              "dusty-rose (#C8706A) nose with a dark nostril at the tip of the muzzle, the curved line of the upper lip, a heavy "
              "angry brow line just above the red patch, ONE bold vermilion (#D6402A) SPIRAL SWIRL painted on the cheek below "
              "and behind the red patch (as on image 1), and two or three small charcoal (#5A5458) zigzag stripe marks on the "
              "forehead and the back of the skull. THE FLAT RED PATCH in the middle is the EYE SOCKET: keep it a flat vermilion "
              "patch of the same shape at the same place; do NOT draw an eye, iris or pupil anywhere on this piece (the eye is "
              "a separate piece on this sheet)"),
    "P_zui": ("the LOWER JAW with the chin beard and cheek ruff: cream-white fur (#F2ECDE) whose lower edge is a row of big "
              "jagged fur points exactly as the guide; the dark crimson (#8E2420) area at the upper right is the INSIDE OF THE "
              "MOUTH: keep it flat dark crimson at the same place with an ink line between it and the fur; a few fur strokes "
              "and one or two small charcoal zigzag marks on the fur"),
    "P_zui_01": "a strip of FAR-CHEEK FUR: cream-white (#F2ECDE), ending in jagged fur points at the bottom, a few fur strokes",
}
TEN_TO = {"M1": "sáu cụm mây lửa lớn", "M2": "bảy cụm mây lửa vừa", "M3": "chín cụm mây lửa nhỏ",
          "D": "mảnh đầu: đầu trên, hàm dưới, lông má xa, mắt, hai nanh, hai hàm răng, hai tai, hai chỏm lửa trán, ba mảnh mày",
          "E": "sáu vòng cổ chân, tám ngón chân gần có móng"}


def loai_o(M, ten):
    if ten in LOAI:
        return ten
    if ten.startswith("P_ya"):
        return "rang"
    return M.vai(ten)


def build_manh():
    import json
    sys.path.insert(0, HERE)
    import hoa_ho_manh as M
    M._chia_may()
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    if not os.path.exists(duyet):
        raise SystemExit("chưa có " + duyet)
    cd, vd = co(duyet)
    ra = []
    gd = ["", "## Lượt 2: MẢNH theo khung part của rig (sau khi duyệt concept A)", "",
          "Mỗi tờ: ảnh 1 = concept đã duyệt (lấy nét, màu, vân sáp), ảnh 2 = tờ hướng dẫn tự dựng. GPT vẽ lại sạch, GIỮ NGUYÊN hình bóng. "
          "Claude cắt bằng `hoa_ho_manh.py cat_part <tờ>` (đo IoU) và `cat_lien`.", ""]
    for to in M.TO:
        pj = os.path.join(mau_dir(), f"part_{to}.json")
        if not os.path.exists(pj):
            raise SystemExit("chưa có tờ hướng dẫn " + pj)
        Kh = json.load(open(pj, encoding="utf-8"))
        z = next(iter(Kh.values()))["z"]
        net_px = max(4, int(round(M.NET * z)))
        g_im = os.path.join(mau_dir(), f"part_{to}.png")
        out = os.path.join(save_dir(), f"N_{to}.png")
        p = os.path.join(pk(), f"luot_2_manh_{to}.txt")
        nh = {}
        for ten, v in sorted(Kh.items(), key=lambda q: (q[1]["y"] // 120, q[1]["x"])):
            nh.setdefault(loai_o(M, ten), []).append(f"({v['x'] + v['w'] // 2}, {v['y'] + v['h'] // 2})")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(duyet)}: the APPROVED creature, {cd}, white background: {CON}. It gives the design, the colours, "
             "the wobbly dark-brown ink line, the crayon hatching and the look of every material.",
             f"image 2 = {Wp(g_im)}: PARTS GUIDE, 1536x1024, white background, drawn by computer: {len(Kh)} separate flat shapes, each "
             "one a PART of the creature's 2D animation rig, enlarged, lying at the angle the rig needs. Each shape is the EXACT "
             "silhouette of its part, filled with the flat colours of its material and outlined in dark brown.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as N_{to}_2.png, N_{to}_3.png ... in the same folder. Do not edit, move "
             "or delete any other file.", "",
             "TASK: redraw image 2 cleanly in the hand-drawn style of image 1, landscape 1536x1024, pure-white background. Keep "
             "EXACTLY every silhouette of image 2: the same outline, the same size, the same angle, the same position on the sheet "
             "(if your picture were laid over image 2, every shape must coincide with its shape there). Do not move, rotate, "
             "straighten, merge or rearrange the shapes; do not add or drop any; keep clear white between them. A program will cut "
             "this sheet by position.", "",
             "WHAT THE SHAPES ARE (centre of each shape in pixels on the sheet, x from the left, y from the top):"]
        for loai, cho in nh.items():
            t.append(f"- {LOAI[loai]}: {len(cho)} shape{'s' if len(cho) > 1 else ''}, centred at about " + ", ".join(cho) + ".")
        t += ["",
              f"OUTLINE: every shape gets ONE closed dark-brown ink outline (#2B2118), about {net_px} px thick on this sheet, wobbly like "
              "a real pen, lying just INSIDE the edge of the silhouette (never outside it). Inner detail lines are thinner (about "
              f"{max(2, net_px // 2)} px).",
              "COLOUR: keep the colour each shape has in image 2 (and keep every second colour exactly where image 2 shows it). Fill "
              "with visible loose diagonal crayon / coloured-pencil hatching as in image 1, kept inside the outline.",
              "Each shape is a complete, closed object on its own: do not draw neighbouring parts, do not draw the creature.", "",
              "FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no "
              "darker side, no highlights or shine spots (not on the fangs, not on the claws, not on the gold), no glow, NO "
              "GRADIENTS (two colours always meet at a clean edge), no cast shadows, no 3D look. Pure white (#FFFFFF) background; "
              "no text, no labels, no numbers, no frames, no guide lines."]
        ghi(p, t)
        ra.append(p)
        gd += [f"- Tờ `{to}` ({TEN_TO[to]}; phóng {z} lần, nét ~{net_px} px): **chỉ gửi GPT đường dẫn** `{Wp(p)}` → `{Wp(out)}`; ảnh 2 = "
               f"`{Wp(g_im)}` (1536 × 1024, nền trắng, {len(Kh)} ô tô phẳng viền nâu sẫm)."]
    LIEN = {
        "LA": ("THREE separate flat silhouettes side by side. LEFT: the FAR HIND LEG, complete from its rounded top down to its paw "
               "(the paw, a slightly darker cream, points to the right). MIDDLE (the big one): the tiger's BODY WITHOUT head, "
               "legs, tail or flames: the massive chest at the right (its right edge is the jagged fur of the chest front), the "
               "back along the top, the belly along the bottom, the rounded rump at the left, all fused into one shape. RIGHT: "
               "the TAIL: a long S-curved tube; its lower end (pointing down-right) is the base that joins the rump, its upper "
               "end is the tip with a fluffy pointed brush",
               ["- BODY (middle): about ELEVEN bold tiger stripes: each one a jagged zigzag wedge like a small flame tongue or "
                "lightning mark, as on image 1, starting at the top edge (the back) and pointing down toward the belly, spread "
                "from the rump to the chest; two or three more short ones rising from the belly edge. Leave calm plain fur "
                "between them.",
                "- FAR HIND LEG (left): three or four zigzag stripes across the upper leg. THE PAW (darker cream area, #E2D6C4): "
                "ONE ink line between leg and paw; on the paw draw FOUR toes, each ending in a big hooked charcoal CLAW "
                "(#3A3438) at the right end, all inside the silhouette.",
                "- TAIL (right): seven or eight zigzag stripe bands across the tube along its whole length; the fluffy brush at "
                "the upper end (the last sixth of the tail) is charcoal grey (#5A5458) with two or three jagged cream stripes "
                "and a pointed, flame-like tip, as on image 1."]),
        "LB": ("THREE separate legs side by side, each complete from its rounded top (which will be hidden under the body) down "
               "to its paw (the slightly darker cream block at the bottom). LEFT: the NEAR HIND LEG. MIDDLE: the NEAR FORELEG "
               "(the thickest). RIGHT: the FAR FORELEG, stretched forward, its long paw pointing to the right",
               ["- Each leg: three or four bold zigzag tiger stripes across the UPPER half, as on image 1; the lower leg plain; "
                "the jagged fur tufts at the elbow / heel exactly as the silhouette.",
                "- LEFT and MIDDLE paws (#E2D6C4): each a PLAIN rounded paw back with ONE ink line between leg and paw. Do NOT "
                "draw toes or claws on these two paws (the toes are separate parts).",
                "- RIGHT paw (#E2D6C4): ONE ink line between leg and paw; draw FOUR toes, each ending in a big hooked charcoal "
                "CLAW (#3A3438) at the right end, all inside the silhouette."]),
    }
    for to, (mo_ta, rieng) in LIEN.items():
        g_im = os.path.join(mau_dir(), f"lien_{to}.png")
        if not os.path.exists(g_im):
            raise SystemExit("chưa có " + g_im)
        out = os.path.join(save_dir(), f"N_{to}.png")
        p = os.path.join(pk(), f"luot_2_lien_{to}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(duyet)}: the APPROVED creature, {cd}, white background: {CON}. It gives the design, the colours, the ink "
             "line, the crayon hatching and the look of its fur, stripes and paws.",
             f"image 2 = {Wp(g_im)}: BODY GUIDE, 1536x1024, white background, drawn by computer: {mo_ta}. Cream = fur. It gives the "
             "exact silhouettes, sizes and positions.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as N_{to}_2.png, N_{to}_3.png ... in the same folder. Do not edit, move "
             "or delete any other file.", "",
             "TASK: redraw image 2 cleanly in the hand-drawn style of image 1, landscape 1536x1024, pure-white background. Keep EXACTLY "
             "every silhouette of image 2: the same outline, the same size, the same position (if your picture were laid over image 2, "
             "the shapes must coincide). This sheet will be cut by a program into the body parts of a 2D animation rig.", "",
             "VERY IMPORTANT, EACH SILHOUETTE IS ONE CONTINUOUS SURFACE OF FUR: draw the dark-brown ink outline ONLY around the "
             "OUTSIDE of each silhouette. INSIDE a silhouette draw NO outline lines that divide it: no line between upper and lower "
             "leg, no knee or ankle rings, no line between chest and rump, no folds, no muscle lines. Only the stripes, the one "
             "line above each paw and a few short fur strokes.", "",
             "- FUR: cream white (#F2ECDE) with loose diagonal crayon hatching, as on image 1.",
             "- STRIPES: charcoal grey (#5A5458), flat, each with a thin ink outline or none, shaped exactly like the stripes of "
             "image 1."] + rieng + [
             "- OUTLINE: dark-brown ink (#2B2118), about 6 px thick on this canvas, wobbly like a real pen, closed around each "
             "silhouette and lying just INSIDE its edge; keep every jagged fur point of the silhouette.",
             "Draw nothing else: no head, no flames, no fire clouds, no bangles, no ground.", "",
             "FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no "
             "darker underside, no highlights, no gradients, no cast shadows. Pure white (#FFFFFF) background; no text, no labels, no "
             "frames, no guide lines."]
        ghi(p, t)
        ra.append(p)
        gd += [f"- Tờ **liền `{to}`**: `{Wp(p)}` → `{Wp(out)}`; ảnh 2 = `{Wp(g_im)}` (1536 × 1024, nền trắng, ba hình bóng kem viền nâu: "
               + ("chân sau xa, thân, đuôi" if to == "LA" else "chân sau gần, chân trước gần, chân trước xa") + ")."]
    gd += ["", "Kiểm: hình bóng trùng tờ hướng dẫn (IoU ≥ 0,9 mới lắp); tờ liền KHÔNG có nét mực chia khúc bên trong; mây tô dải phẳng; "
           "đầu trên KHÔNG có mắt (chỉ mảng đỏ); nền trắng.", ""]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2:")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in ra:
        print(p)


if __name__ == "__main__":
    if sys.argv[1:2] == ["manh"]:
        build_manh()
    else:
        main()
