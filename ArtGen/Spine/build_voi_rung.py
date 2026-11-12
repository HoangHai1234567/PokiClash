# -*- coding: utf-8 -*-
"""Gói GPT vẽ ma mút rừng cổ (mã làm việc voi_rung): tướng thứ 5 đảo Mộc (suất ải 20, id game phong_linh), dạng 2 (trưởng thành).

Người dùng (2026-11-12) đưa ý "voi ma mút hệ cây" kèm ảnh một con ma mút phủ cỏ của game khác. Không có rig gốc: tự dựng xương,
lưới (voi_rung.py). Không đính ảnh của game nào vào prompt; hình là thiết kế của mình.

Bản đầu (voi xám lam nhìn ngang, tai lá, mũ vỏ cây, cây nhỏ trên lưng; bám sơ đồ hình khối voi_rung_bo_cuc.py) bị người dùng trả:
"concept này xấu quá" (tai_ve/L1.png). Bản này giữ cái làm con gợi ý đẹp (khối to lù lù, lưng gù cao hơn đầu, góc ba phần tư, lớp
áo rậm xếp tầng rủ che trán, mắt nhỏ dữ, chân cột ngắn, vòi to dài); chi tiết nhận diện là của mình (chất liệu và màu áo, màu da,
ngà mọc từ khoé miệng, thứ mọc trên u vai, không vòng đá, không sừng đá). Hai hướng để người dùng chọn. GPT tự dựng hình theo lời.

    py -3 -I ArtGen/Spine/build_voi_rung.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/voi_rung_2/luot_1_concept_<hướng>.txt [--note "..."]
Lượt 2 (mảnh) viết sau khi người dùng duyệt một hướng (tai_ve/L1_duyet.png).
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "voi_rung"
K = 2
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
CACTUS = os.path.join(HERE, "inbox", "xuong_rong_1", "tai_ve", "L1_duyet.png")
SPIRIT = os.path.join(HERE, "inbox", "tinh_linh_3", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def pk(k=K):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def chosen(k=K):
    return os.path.join(save_dir(k), "L1_duyet.png")


HUONG = {
    "duong_xi": dict(
        ten="áo dương xỉ lục sẫm, da đá lam, ngà rễ gỗ màu mật, cụm nấm cam trên u vai, mắt hổ phách",
        hide="dark slate blue (#566878)",
        coat="a heavy mantle of FERN FRONDS and long drooping jungle leaves",
        coat_d="each piece is a long pointed frond or leaf with a centre vein (some with a few side notches like a fern), "
               "hanging straight down and overlapping the tier below like roof tiles",
        c1="deep forest green (#2F7A45)", c2="fresh leaf green (#63B04A)", vein="darker green (#235C36)",
        tusk="two big curved TUSKS that grow from the corners of the mouth, under the cheeks: thick twisted ROOT WOOD of pale "
             "honey colour (#E3C98A) with two or three darker grain lines (#B8975A) spiralling along each, sweeping forward and "
             "curving up to blunt points; a small tuft of moss where each tusk leaves the cheek",
        back="a cluster of THREE big shelf MUSHROOMS with flat round caps of warm orange (#E8862E) and cream undersides "
             "(#F2E6C0), the biggest about 150 px wide, growing out of the mantle on top of the hump",
        eye="amber yellow (#F2B43A)", nail="pale honey wood (#E3C98A)",
        extra="A few tiny cream dots (spores) may sit on the mantle, at most six.",
        cam="NO brown or orange body, NO grey stone, NO red eye"),
    "lieu_hoa": dict(
        ten="áo liễu rủ lục vàng điểm hoa hồng, da bạch dương kem, ngà cành gỗ sẫm có nụ, bụi hoa trên u vai, mắt lục lam",
        hide="pale birch cream (#E6DCC2)",
        coat="a heavy mantle of WEEPING-WILLOW strands",
        coat_d="each piece is a long, gently wavy hanging willow branch with a row of small narrow leaves, the strands "
               "grouped into thick pointed locks that overlap the tier below like roof tiles",
        c1="willow green (#7FA83E)", c2="light yellow-green (#B9CF5A)", vein="olive (#5E7F2E)",
        tusk="two big curved TUSKS that grow from the corners of the mouth, under the cheeks: thick dark BRANCH WOOD "
             "(#6E4A32) with two or three lighter grain lines, sweeping forward and curving up to blunt points, each carrying "
             "two small pink buds near its tip",
        back="a round flowering BUSH: a dome of darker green leaves (#4F8A3C) with five or six simple five-petal blossoms of "
             "soft pink (#F08FA8) with yellow centres, about 260 px wide, growing on top of the hump",
        eye="teal green (#2FA38C)", nail="dark branch wood (#6E4A32)",
        extra="Six to eight of the same small pink blossoms are scattered on the willow mantle.",
        cam="NO brown or orange body, NO grey stone, NO red eye"),
}


def body(kieu):
    M = HUONG[kieu]
    return "\n".join([
        "CREATURE: an ANCIENT FOREST MAMMOTH, a plant-element monster for a monster-collecting game. A colossal, heavy, "
        "slow, immovable beast that looks like a walking hill of vegetation. Character: an old, grim, unshakable guardian of "
        "the forest, calm but dangerous, ready to charge. Powerful and appealing, not a smiling cute mascot, not a children's "
        "book elephant, not horrific. Bold, chunky, simple shapes (the way a Pokemon is designed), but with a rich, layered "
        "silhouette.",
        "- VIEW AND BUILD: three-quarter front view. The creature faces the viewer's RIGHT and is turned partly toward the "
        "viewer: its huge head and trunk are at the right front of the picture, its body recedes behind it to the left. The "
        "body is enormously wide and LOW, like a boulder: a high rounded SHOULDER HUMP that is clearly higher than the head, "
        "a back that slopes down to the rump at the left, a heavy belly close to the ground. The head is big, broad and "
        "carried LOW in front of the chest (the top of the head is below the top of the hump). The legs are very short, very "
        "thick pillars. The overall silhouette is a massive hunched mound, much wider than tall.",
        f"- MANTLE (the most important feature): {M['coat']} covers the creature like a thick shaggy cloak. It covers the top "
        "and the back of the head, the whole hump and back, and hangs down over the shoulders and flanks to about the height "
        f"of the knees, in THREE or FOUR clearly separate overlapping TIERS: {M['coat_d']}. Every tier ends in a jagged row of "
        "big pointed tips (each tip about 40-90 px long), so the outline of the mantle is a bold zigzag of hanging points, "
        "big and readable, not fine hair. On the head the mantle forms a heavy FRINGE that hangs over the brow and partly "
        "over the cheek, like a helmet of foliage, so that the eye peeks out from under it. The mantle is thick and has "
        f"volume: it makes the creature look even bigger. Upper tiers {M['c1']}, the lowest tier and the fringe tips "
        f"{M['c2']}; centre veins {M['vein']}. {M['extra']}",
        f"- HIDE: below the mantle the bare hide shows: the lower half of the face, the whole trunk, the chest, the belly and "
        f"the four legs. Smooth thick hide of {M['hide']}, no fur.",
        "- FACE: ONE eye visible (the near one), fairly small, set deep under the fringe: a fierce slanted eye of "
        f"{M['eye']} with a black pupil and one tiny white dot, the upper lid cut straight and slanting down toward the trunk "
        "(a stern glare). No second eye. Under the root of the trunk a wide, closed, down-turned mouth line with a heavy lower "
        "lip.",
        "- TRUNK: a very thick, long, heavy trunk (about 130 px thick where it leaves the face, tapering only a little, to "
        "about 85 px). It hangs down in front of the chest at the right, bends forward near the ground without touching it, "
        "and its blunt round tip curls slightly up and to the right, with two small dark nostril dots. Five or six curved "
        "wrinkle lines across it. A narrow strip of the mantle (short hanging tips) runs a little way down the top of the "
        "trunk from the forehead and stops after the first third.",
        f"- TUSKS: {M['tusk']}. The near tusk is in front of the trunk root; the far tusk shows on the other side of the trunk, "
        "partly hidden by it.",
        f"- ON THE HUMP: {M['back']}.",
        f"- LEGS: four very short, very thick pillar legs of bare hide, each with THREE big rounded toenails of {M['nail']} at "
        "the front of a wide flat foot. All four feet are visible and stand apart on the same ground: the two near legs in "
        "front, the two far legs showing behind and between them. The mantle hangs over the tops of the legs. No rings, no "
        "bands, no bracelets on the legs.",
        "- TAIL: short and thin, hanging at the far left from the rump, ending in a small tuft of the same foliage as the "
        "mantle.",
        "- No ears are visible (they are buried under the mantle). No saddle, no ropes, no armour, no stone spikes, no horns "
        "on the forehead or the back.",
        "",
        f"COLOURS (use exactly these, each area ONE flat colour): hide {M['hide']} (wrinkle lines a little darker); mantle "
        f"{M['c1']} and {M['c2']} with veins {M['vein']}; the things on the hump, the tusks, the toenails and the eye as "
        f"listed above; mouth line and every outline dark-brown ink (#2B2118). Only these colours. {M['cam']}.",
    ])


FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. The whole creature is "
         "visible, nothing cut by the edges, with at least 50 px of white on every side. It fills the canvas: about 1150-1250 px "
         "wide and about 800-860 px tall, its feet standing at about y = 940.")

POSE = ("POSE (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): standing still, "
        "planted on all four legs, in a clean resting pose: legs straight and apart, not crossing, not walking; the trunk "
        "hanging free in front (it does not touch the ground, the legs or the tusk tips); the mouth closed; the head low. No "
        "falling leaves, no dust, no sparkles, no glow, no motion lines, no ground, no grass, no props.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. Give the "
        "creature WEIGHT and MASS: big overlapping forms, the mantle draped over the body in thick layers, the head pushing "
        "forward. Avoid a flat side-on clip-art look: this is a three-quarter view with real volume, told only by the shapes "
        "and overlaps (not by shading).")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 1 and 2): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 6 px thick on this canvas around every big part (body, head and trunk, "
        "legs, tusks, each tier of the mantle, the things on the hump), and about 4 px for small details (the tips inside a "
        "tier, toenails, the eye, the mouth line, small flowers or dots); leaf veins, trunk wrinkles and wood grain are thin "
        "darker pencil lines about 3-4 px, not ink; every area coloured with coloured pencils and wax crayons, the strokes "
        "visible as loose diagonal hatching (strokes thinner than the outline), kept inside the outline. Clean and appealing, "
        "neither a crude scribble nor overly detailed: no single hairs, no tiny leaves everywhere.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker underside, no lighter patches or blotches, no shadows of any kind (no cast "
        "shadow of one tier on the next, no shadow under the figure or on the background), no white highlights or shine "
        "spots, no gloss, no glow, no rim light, no gradients, no 3D render look. A different tone appears only where the "
        "design itself lists a different colour (the two greens of the mantle).")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the creature.")


def refs():
    return [
        (CACTUS,
         "an approved hero of the same game and the same island (a round cactus monster), 1536x1024, white background: match "
         "EXACTLY its wobbly dark-brown pen line, its visible crayon hatching and its completely flat colouring. Do NOT copy "
         "its species, its design or its colours.",
         "Xương rồng tròn đã duyệt (1536 × 1024, nền trắng): quả cầu lục miệng to nanh kem. Lấy nét bút rung, vân sáp, tô phẳng"),
        (SPIRIT,
         "another approved hero of the same island (a plump green forest spirit with two big leaves and a flower on its head), "
         "1536x1024, white background: the same line and flat crayon colouring; see how its big leaves and its flower are "
         "drawn. Do NOT copy its design or its colours.",
         "Tinh linh rừng mập đã duyệt (1536 × 1024, nền trắng): thân lục tròn, hai lá to và một bông hoa đỏ trên đầu. Lấy nét, tô "
         "phẳng, cách vẽ lá to, hoa"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching) and the way its trees and leaves are simplified, nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp, cách giản lược cây, lá"),
    ]


CHECK = [
    "Ma mút **to lù lù, thấp, lưng gù cao hơn đầu**, góc **ba phần tư** nhìn sang phải (đầu và vòi ở phía trước bên phải, thân lùi về "
    "bên trái); không phải voi nhìn ngang kiểu minh hoạ.",
    "**Lớp áo rậm xếp 3–4 tầng** phủ đỉnh đầu, u vai, lưng, rủ xuống sườn tới ngang gối, mép là hàng mũi nhọn to; mái áo rủ che "
    "trán, **một mắt nhỏ dữ** ló ra dưới mái; nửa dưới mặt, vòi, bụng, bốn chân là da trần.",
    "Vòi rất to, buông trước ngực, chóp cong ra trước, không chạm đất; **hai ngà mọc từ khoé miệng** (hướng dương xỉ: rễ gỗ màu "
    "mật; hướng liễu hoa: cành gỗ sẫm có nụ); trên u vai: cụm nấm cam / bụi hoa hồng.",
    "Bốn chân cột ngắn, đủ bốn bàn chân, mỗi bàn ba móng; không vòng, không đai ở chân; không sừng đá, không gai đá.",
    "Tô phẳng: **không** bóng, không mảng sáng tối; nền trắng tinh; không lá rơi; cả con không bị cắt mép.",
]

FIX = [
    ("Ra voi nhìn ngang kiểu minh hoạ thiếu nhi", "Three-quarter front view with real mass: the huge head and trunk at the right "
                                                  "front, the body receding to the left, a shoulder hump higher than the head, "
                                                  "a thick layered mantle; not a flat side-view elephant."),
    ("Áo thành lông mảnh / cỏ sợi nhỏ", "The mantle is made of BIG pieces in three or four overlapping tiers, each tier ending in "
                                        "big pointed tips 40-90 px long; no fine hair, no single grass blades."),
    ("Có bóng, mảng sáng tối", "Flat colour only: remove every shadow, highlight, gradient and glow; each area one even colour; "
                               "keep the crayon hatching as texture only."),
    ("Vòi chạm đất / vắt qua chân", "The trunk hangs free in front of the chest and ends above the ground; it does not touch the "
                                    "legs."),
    ("Hai mắt, mặt quay chính diện", "Only ONE eye is visible: the creature faces the viewer's right."),
    ("Chân chéo, đang bước, thiếu chân", "Standing still: all four legs visible, straight and apart."),
]


def _dau(R, out, ten):
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
    t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
          f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move "
          "or delete any other file.", ""]
    return t


def _viet(p, t):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")


def check(R):
    missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def build_concept(kieu):
    R = refs()
    check(R)
    out = os.path.join(save_dir(), f"L2_{kieu}.png")
    p = os.path.join(pk(), f"luot_1_concept_{kieu}.txt")
    t = _dau(R, out, f"L2_{kieu}")
    t += ["TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
          "approved hero images.", "", body(kieu), "", FRAME, "", POSE, "", SOFT, LINE, FLAT, BG]
    _viet(p, t)
    return p, R, out


INTRO = ("a forest mammoth in three-quarter view facing the viewer's right, 1536x1024, white background: a huge hunched body "
         "covered by a mantle of big dark-green leaves in overlapping tiers (the lowest tier lighter green), a leaf fringe over "
         "the brow with one fierce amber eye under it, dark slate-blue hide on the face, trunk and legs, a thick trunk hanging "
         "at the right with its tip curled forward, two big curled honey-coloured root-wood tusks with a moss tuft at each "
         "root, four short pillar legs with three honey toenails each, a thin tail with a leaf tuft at the far left")


def build_sua():
    """lượt 1b: người dùng chọn hướng duong_xi (2026-11-12): "lấy con này nhưng bỏ nấm đi"."""
    nhap = os.path.join(save_dir(), "L2_duong_xi.png")
    if not os.path.exists(nhap):
        raise SystemExit("thiếu bản nháp " + Wp(nhap))
    out = os.path.join(save_dir(), "L3.png")
    p = os.path.join(pk(), "luot_1b_bo_nam.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(nhap)}: the DRAFT of this creature: {INTRO}, and THREE orange mushrooms on top of its hump. This is the "
         "design, the pose, the line and the colours to keep.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as L3_2.png, L3_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: redraw image 1 as ONE picture, changing ONLY the two things listed under CHANGE.", "",
         "KEEP IDENTICAL to image 1, in the same place and at the same size (if the new picture were laid over image 1, "
         "everything except the changed things must coincide): the whole creature, its pose and its view; every leaf of the "
         "mantle and of the fringe with its shape and its vein lines; the small cream dots on the leaves; the eye and brow; the "
         "mouth line; the trunk with its wrinkle lines and nostril dots; both tusks with their grain lines and moss tufts; all "
         "four legs and toenails; the tail and its leaf tuft; every colour; the bold dark-brown ink outline; the white "
         "background.", "",
         "CHANGE:",
         "1. REMOVE THE THREE MUSHROOMS completely (caps, gills and stems). Where they stood, close the top of the hump with the "
         "same big dark-green leaves as the rest of the mantle: the leaves that were partly hidden behind the mushroom stems "
         "are drawn complete, and one or two more leaves of the same kind and size cover the very top, so the hump ends in a "
         "round crown of overlapping leaf tips. Nothing else grows on the back: no mushrooms, no flowers, no tree, no rocks.",
         "2. FLAT COLOUR in the lowest tier of the mantle: in image 1 the lowest leaves fade softly from dark green into light "
         "green. Replace every such soft fade by a clean split: each leaf is entirely ONE flat colour, either the dark forest "
         "green (#2F7A45) or the fresh leaf green (#63B04A); the leaves of the lowest tier (the row hanging over the legs and "
         "the belly) are fresh leaf green, all the tiers above are dark forest green. No gradient anywhere.", "",
         "Colouring as in the game's other heroes: every area filled with coloured pencil / wax crayon, the strokes visible as "
         "loose diagonal hatching, texture only.", "", FLAT, BG]
    _viet(p, t)
    return p, nhap, out


# ---------------------------------------------------------------- lượt 2: mảnh, mỗi ảnh "đúng chỗ, đúng cỡ" như concept đã duyệt
PAGE = ("CANVAS: 1536x1024, pure-white background (#FFFFFF) everywhere outside the drawing: no paper grain, no ground line, no "
        "shadow, no text, no labels, no frame, no white sticker border. Nothing else on the page.")
SAME = ("Same hand-drawn look as image 1: bold dark-brown ink outline (#2B2118) of the same thickness as in image 1, the same "
        "flat colours, the same crayon hatching.")
FLAT2 = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area one even colour, the crayon strokes are texture only; no shading, no "
         "darker side, no highlights, no shine spots, no gloss, no glow, no gradients, no shadows of any kind, no 3D look.")

PARTS = {
    "ao": dict(
        out="B01", vi="tấm áo lá của thân (cả khối lá phủ lưng, u vai, sườn; bỏ đầu, vòi, ngà, bốn chân, đuôi)",
        what="THE LEAF MANTLE OF ITS BODY",
        role="In the animation this big mound of leaves is the body; the head, the tusks, the legs and the tail are separate "
             "parts laid over it or behind it.",
        keep="the whole mound of leaves that covers the hump, the back and the flanks: every dark-green leaf tier and the "
             "light-green lowest tier with its hanging pointed tips, with every leaf, vein line and cream dot exactly as drawn",
        remove="the whole head (its own leaf fringe, the face, the eye, the trunk), both tusks with their moss tufts, all four "
               "legs with their toenails, and the tail with its leaf tuft",
        complete=["where the head, its leaf fringe and the big near tusk covered the mantle (the right part of the mound): "
                  "continue the mantle as the same overlapping tiers of big leaves, down to the same light-green lowest tier "
                  "with hanging pointed tips at the same height as on the flank, so the mound is a complete round hill of "
                  "leaves whose right edge is about where the middle of the head was;",
                  "between the hanging tips of the lowest tier, where the legs and the belly showed: pure white page (do not "
                  "draw legs, hide or belly);",
                  "where the tail was attached at the left: the plain leaf outline of the mound."]),
    "dau": dict(
        out="H01", vi="đầu: mái lá + mặt + mắt + vòi (bỏ hai ngà và túm rêu gốc ngà, thân, chân)",
        what="ITS HEAD TOGETHER WITH ITS TRUNK",
        role="In the animation the head nods and the trunk swings and curls; the two tusks are separate parts laid over or "
             "behind this part.",
        keep="the leaf fringe of the head (the cap of dark-green leaves over the skull and brow, with its cream dots, and the "
             "light-green leaf tufts hanging at the right side of the face), the slate-blue face with the eye, the brow and the "
             "mouth line, and the whole trunk hanging from the face down to its curled tip with the nostril dots and the "
             "wrinkle lines. Face and trunk are ONE continuous slate-blue shape",
        remove="both tusks completely (the big curled near tusk with its moss tuft, and the far tusk at the right), the whole "
               "leaf mantle of the body, all four legs and the tail",
        complete=["where the big near tusk and its moss tuft covered the face and the trunk: plain slate-blue hide; draw the "
                  "cheek as a round jaw whose outline runs from under the leaf fringe at the left down and around to the "
                  "underside of the trunk root; the left edge of the trunk runs through unbroken as one smooth line from the "
                  "jaw down to the bend, with the wrinkle lines continued across; the mouth line continues to its natural "
                  "end;",
                  "where the far tusk passed behind the trunk at the right: nothing (pure white outside the trunk outline);",
                  "the head with its fringe and trunk is ONE CLOSED SHAPE; outside it pure white page."]),
    "nga": dict(
        out="T01", vi="hai ngà rễ gỗ: ngà gần (cuộn to, có túm rêu ở gốc) và ngà xa vẽ đủ phần bị vòi che",
        what="ITS TWO TUSKS",
        role="In the animation the tusks are rigid parts fixed to the head: the near one lies in front of the face, the far one "
             "behind the trunk.",
        keep="(1) the big curled near tusk with its grain lines, together with the moss tuft at its root; (2) the visible part "
             "of the far tusk at the right with its grain lines. Two separate shapes, each exactly where it is in image 1",
        remove="everything else: the head with its leaf fringe, the face, the eye, the trunk, the leaf mantle of the body, the "
               "legs and the tail",
        complete=["the near tusk is ONE closed shape exactly as visible (nothing covers it);",
                  "the far tusk is drawn COMPLETE as ONE closed crescent: continue it to the left, where the trunk and the leaf "
                  "tufts hid its root, as the same thick honey-coloured tusk, about 120 px further left and slightly up, and "
                  "close it there with a rounded root end carrying a small moss tuft like the near one;",
                  "everything else: pure white page."]),
    "chan": dict(
        out="G01", vi="ba chân (chân ngoài cùng bên trái, chân thứ hai từ trái, chân trước to bên phải) vẽ đủ phần bị áo che + đuôi",
        what="THREE OF ITS LEGS AND ITS TAIL",
        role="In the animation the legs stand behind the hanging leaf mantle and the tail swings from the rump; each is a "
             "separate part.",
        keep="(1) the leftmost leg; (2) the second leg from the left; (3) the big front leg at the right, the one below the big "
             "curled tusk; each with its flat foot and three honey toenails; and (4) the thin tail with its leaf tuft at the "
             "far left. Four separate shapes, each exactly where it is in image 1",
        remove="the leaf mantle, the head, the trunk, both tusks, and the small fourth leg that is partly hidden between the "
               "second leg and the big front leg",
        complete=["each leg is drawn COMPLETE as ONE CLOSED thick pillar: continue it upward, where the hanging leaves, the "
                  "tusk or the trunk hid it, with the same width, up to about y = 600, and close it there with a round top; "
                  "plain slate-blue hide, ink outline all the way around;",
                  "the tail is ONE closed shape: continue its thin stem up and to the right for about 60 px, where the leaves "
                  "hid it, and close it with a small round end;",
                  "between and around the four shapes: pure white page."]),
}


# ---------------------------------------------------------------- lượt 3: tách LỚP LÁ (người dùng 2026-11-12: "tách thêm lớp lá và rig
# xương vào để gió đung đưa"). Ảnh mẫu là ảnh mảnh lượt 2 (B01 khối áo, H01 đầu): mỗi lớp nằm đúng chỗ, đúng cỡ, vẽ đủ phần khuất.
MANTLE = ("the leaf mantle of a forest mammoth, alone on a white 1536x1024 page: a big round mound of overlapping dark-green "
          "leaves in tiers (some of the upper leaves carry a small cream dot), with one lowest tier of LIGHT-green leaves "
          "hanging along the bottom")
HEAD = ("the head of a forest mammoth, alone on a white 1536x1024 page: a slate-blue face with one fierce amber eye and a mouth "
        "line, a thick trunk hanging down to the right with a curled tip and two nostril dots, and on top a cap of dark-green "
        "leaves whose fringe hangs over the brow, with light-green leaf tufts at the right side of the face")
LOP = {
    "la_day": dict(
        src="B01", out="C01", vi="tầng lá dưới cùng (lục tươi) vẽ đủ phần bị lá sẫm che",
        intro=MANTLE,
        what="ITS LOWEST TIER, THE LIGHT-GREEN LEAVES",
        keep="every light-green leaf of the lowest tier, with its hanging pointed tip, its outline and its vein, exactly where "
             "it is",
        remove="all the dark-green leaves (every tier above) and the cream dots",
        complete=["each light-green leaf continues UPWARD, where the dark leaves hid it, as a full leaf of the same light green "
                  "with its centre vein, up to about y = 560; the leaves overlap each other like roof tiles and together form "
                  "ONE connected band across the whole width of the mound (from about x = 240 to x = 1210);",
                  "the top edge of the band is a row of rounded leaf tops at about y = 540-570, with an ink outline;",
                  "above the band and below the tips: pure white page."]),
    "la_giua": dict(
        src="B01", out="C02", vi="các tầng lá sẫm phía dưới (mũi lá rủ thấp hơn y ≈ 580) vẽ đủ phần bị tầng trên che",
        intro=MANTLE,
        what="THE LOWER DARK-GREEN LEAVES",
        keep="the dark-green leaves of the lower half of the mound: every dark-green leaf whose pointed TIP hangs below about "
             "y = 580 (the lowest dark rows, all the way from the left edge of the mound to its right edge), each with its "
             "outline and veins exactly where it is",
        remove="the light-green lowest tier (pure white where it showed below and between the dark tips), and all the UPPER "
               "leaves: the crown at the very top and the big leaves that carry the cream dots, every leaf whose tip ends above "
               "about y = 580",
        complete=["each kept leaf continues UPWARD, where the upper leaves hid it, as a full dark-green leaf with its centre "
                  "vein, up to about y = 400; together the kept leaves form ONE connected mass across the whole width of the "
                  "mound;",
                  "the top edge of that mass is a row of rounded leaf tops at about y = 380-420, with an ink outline;",
                  "above it and below the tips: pure white page."]),
    "la_tren": dict(
        src="B01", out="C03", vi="các lá phía trên (chỏm lá và các lá to có chấm kem, mũi lá cao hơn y ≈ 580)",
        intro=MANTLE,
        what="THE UPPER LEAVES",
        keep="the upper part of the mound exactly as drawn: the crown of leaves at the very top and the big dark-green leaves "
             "that carry the cream dots, every leaf whose pointed TIP ends above about y = 580, with all outlines, veins and "
             "dots",
        remove="everything below them: the lower dark-green leaves (every leaf whose tip hangs below about y = 580) and the "
               "light-green lowest tier",
        complete=["nothing was hidden: the kept leaves stay exactly as they are and form ONE connected mass with an ink outline "
                  "all the way around; its lower edge is the jagged row of its own hanging leaf tips;",
                  "below and between those tips, where the removed leaves were: pure white page."]),
    "so": dict(
        src="H01", out="H02", vi="đầu TRỌC (không lá) liền vòi: sọ tròn, mắt vẽ đủ",
        intro=HEAD,
        what="ITS HEAD AND TRUNK WITHOUT ANY LEAVES",
        keep="the slate-blue face with the mouth line, the eye, and the whole trunk with its wrinkle lines, curled tip and "
             "nostril dots, exactly where they are",
        remove="the whole cap of dark-green leaves with its fringe, and the light-green leaf tufts at the right side of the "
               "face",
        complete=["where the leaf cap was: a BALD rounded skull of the same slate-blue hide: a smooth dome whose top is at about "
                  "y = 340 and whose sides run down into the cheeks and into the trunk root; plain hide, no hair, no leaves;",
                  "the EYE is drawn complete: an amber eye of the same size and place as in image 1, with its black pupil and "
                  "tiny white dot, its upper edge a thick straight ink lid line slanting down toward the trunk (the same stern "
                  "glare), and one short thick brow stroke just above it;",
                  "where the light-green tufts covered the right edge of the face: the plain face outline running down into the "
                  "trunk;",
                  "head and trunk are ONE closed slate-blue shape; outside it pure white page."]),
    "mai": dict(
        src="H01", out="F01", vi="mái lá của đầu (cả vòm lá sẫm, các lọn mái rủ trước trán, túm lá lục tươi bên phải)",
        intro=HEAD,
        what="THE LEAF CAP OF ITS HEAD",
        keep="the whole cap of dark-green leaves on the head with its cream dots, the fringe of leaf tips hanging over the brow "
             "and down the left side of the face, and the light-green leaf tufts at the right side, every leaf exactly where "
             "it is",
        remove="the slate-blue face, the eye, the mouth line and the whole trunk",
        complete=["nothing was hidden: the leaves stay exactly as they are and form ONE connected shape with an ink outline all "
                  "the way around; the lower edge is the jagged row of hanging leaf tips;",
                  "where the face and the eye showed between and below the leaf tips: pure white page (no blue, no eye)."]),
}


def nguon_lop(d):
    return os.path.join(save_dir(), d["src"] + ".png")


def build_lop(ten):
    d = LOP[ten]
    R = [(nguon_lop(d), d["intro"] + f". You will redraw this picture keeping ONLY {d['what']}, in exactly the same place.",
          ("Ảnh mảnh khối áo lá của thân (B01, 1536 × 1024, nền trắng): ụ lá lục sẫm xếp tầng, tầng dưới cùng lục tươi"
           if d["src"] == "B01" else
           "Ảnh mảnh đầu (H01, 1536 × 1024, nền trắng): mặt da đá lam một mắt hổ phách, vòi buông bên phải, mái lá lục sẫm phủ trên")
          + ". Lấy đúng " + d["vi"] + ", giữ nguyên chỗ, cỡ")]
    check(R)
    out = os.path.join(save_dir(), d["out"] + ".png")
    p = os.path.join(pk(), f"luot_3_{ten}.txt")
    t = _dau(R, out, d["out"])
    t += [f"TASK: redraw image 1 with ONLY {d['what']}: one separate, complete layer for a 2D cut-out animation in which the "
          "leaf layers sway in the wind independently, so every layer must be complete even where another layer lies over it.", "",
          f"KEEP EXACTLY AS DRAWN in image 1, in the SAME POSITION on the canvas and at the SAME SIZE (if the new picture were "
          f"laid over image 1, every kept line must coincide): {d['keep']}. Same outline, same colours, same crayon hatching.", "",
          f"REMOVE completely: {d['remove']}. No trace of them may remain.", "",
          "COMPLETE the layer so that it is ONE CLOSED SHAPE with an ink outline all the way around:"]
    t += ["- " + c for c in d["complete"]]
    t += ["", PAGE, "", SAME, "", FLAT2]
    _viet(p, t)
    return p, R, out


def build_part(ten):
    d = PARTS[ten]
    R = [(chosen(), "the approved creature: " + INTRO + f". You will redraw this picture keeping ONLY {d['what']}, in exactly "
                    "the same place.",
          "Ma mút rừng đã duyệt (1536 × 1024, nền trắng): áo lá lục sẫm xếp tầng, da đá lam, hai ngà rễ gỗ màu mật, không nấm. "
          "Lấy đúng " + d["vi"] + ", giữ nguyên chỗ, cỡ")]
    check(R)
    out = os.path.join(save_dir(), d["out"] + ".png")
    p = os.path.join(pk(), f"luot_2_{ten}.txt")
    t = _dau(R, out, d["out"])
    t += [f"TASK: redraw image 1 with ONLY {d['what']}: separate, complete part(s) for a 2D cut-out animation. {d['role']}", "",
          f"KEEP EXACTLY AS DRAWN in image 1, in the SAME POSITION on the canvas and at the SAME SIZE (if the new picture were "
          f"laid over image 1, every kept line must coincide): {d['keep']}. Same outline, same colours, same crayon hatching.", "",
          f"REMOVE completely: {d['remove']}. No trace of them may remain.", "",
          "COMPLETE what was hidden, so that every kept part is ONE CLOSED SHAPE with an ink outline all the way around:"]
    t += ["- " + c for c in d["complete"]]
    t += ["", PAGE, "", SAME, "", FLAT2]
    _viet(p, t)
    return p, R, out


def main():
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    for f in os.listdir(pk()):               # prompt của bản đầu (bị trả)
        if f == "luot_1_concept.txt" or f.startswith("luot_2_"):
            os.remove(os.path.join(pk(), f))
    gd = [f"# Gói gửi GPT: `{CODE}` dạng {K} (ma mút rừng cổ, tướng thứ 5 đảo Mộc, tên chưa đặt)", "",
          "Làm 2026-11-12. Bản concept đầu (voi xám lam nhìn ngang, `tai_ve/L1.png`) bị người dùng trả: \"xấu quá\". Bản này: ma mút "
          "to gù, góc ba phần tư, áo rậm xếp tầng; **hai hướng** để người dùng chọn. Không đính ảnh của game nào, không đính sơ đồ "
          "hình khối. Ghi chú: `ArtGen/Spine/inbox/voi_rung_ghichu.md`.", "",
          "Lượt 2 (mảnh) chỉ dựng sau khi người dùng duyệt một hướng (`tai_ve/L1_duyet.png`).", ""]
    ra = []
    for kieu, M in HUONG.items():
        p, R, out = build_concept(kieu)
        ra.append(p)
        gd += [f"## Hướng `{kieu}`: {M['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{K}/luot_1_concept_{kieu}.txt` (thêm "
               "`--note \"...\"` để sửa nhanh).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += [""]
    if os.path.exists(os.path.join(save_dir(), "L2_duong_xi.png")):
        p, nhap, out = build_sua()
        ra.append(p)
        gd += ["## Lượt 1b: người dùng chọn hướng `duong_xi`, dặn \"bỏ nấm đi\" (2026-11-12)", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Ảnh mẫu duy nhất: `{Wp(nhap)}` (bản nháp hướng dương xỉ, 1536 × 1024, nền trắng: ma mút áo lá lục sẫm xếp tầng, da "
               "đá lam, hai ngà rễ gỗ màu mật cuộn to, ba cây nấm cam trên u vai). Vẽ lại y hệt, chỉ bỏ ba cây nấm (đỉnh u vai khép "
               "bằng lá) và đổi chỗ chuyển màu ở tầng áo dưới cùng thành tô phẳng hai màu lục.", "",
               "Kiểm: đặt chồng lên bản nháp phải khít mọi thứ trừ chỗ nấm; không còn nấm; tầng lá dưới cùng một màu lục tươi phẳng, "
               "không chuyển màu. Bản đạt chép thành `tai_ve/L1_duyet.png`.", ""]
    if os.path.exists(chosen()):
        gd += ["## Lượt 2: mảnh (mỗi file một ảnh; mảnh nằm ĐÚNG CHỖ, ĐÚNG CỠ như concept đã duyệt)", "",
               f"Ảnh mẫu duy nhất của mọi file lượt 2: `{Wp(chosen())}` (concept đã duyệt, 1536 × 1024, nền trắng: ma mút góc ba phần "
               "tư nhìn sang phải, áo lá lục sẫm xếp tầng, da đá lam, hai ngà rễ gỗ màu mật cuộn to, không nấm).", "",
               "| File prompt (chỉ gửi GPT đường dẫn này) | Ảnh ra | Là gì |", "|---|---|---|"]
        for ten, d in PARTS.items():
            p, _, out = build_part(ten)
            ra.append(p)
            gd += [f"| `{Wp(p)}` | `{Wp(out)}` | {d['vi']} |"]
        gd += ["", "Kiểm từng ảnh: chỉ còn đúng bộ phận được nêu, nằm trùng chỗ concept (đặt chồng lên concept phải khít), mỗi mảnh "
               "viền mực kín, nền trắng tinh, không bóng. Sai thì gen lại file đó với `--note`: "
               "`Keep ONLY the listed part(s), in the same position and at the same size as in image 1; pure white elsewhere.`",
               "", "Chân thứ tư (chân nhỏ khuất giữa) dùng lại ảnh chân thứ hai thu nhỏ; bụng (khối da sau tấm áo) và mí mắt nhắm "
               "vẽ bằng mã (tô phẳng).", ""]
    if all(os.path.exists(os.path.join(save_dir(), n + ".png")) for n in ("B01", "H01")):
        gd += ["## Lượt 3: tách lớp lá (người dùng 2026-11-12: \"tách thêm lớp lá và rig xương vào để gió đung đưa\")", "",
               "Mỗi file một ảnh, một ảnh mẫu (ảnh mảnh lượt 2), lớp nằm ĐÚNG CHỖ, ĐÚNG CỠ và vẽ đủ phần bị lớp khác che.", "",
               "| File prompt (chỉ gửi GPT đường dẫn này) | Ảnh mẫu | Ảnh ra | Là gì |", "|---|---|---|---|"]
        for ten, d in LOP.items():
            p, _, out = build_lop(ten)
            ra.append(p)
            gd += [f"| `{Wp(p)}` | `{Wp(nguon_lop(d))}` | `{Wp(out)}` | {d['vi']} |"]
        gd += ["", "Ảnh mẫu `B01.png`: khối áo lá của thân (ụ lá lục sẫm xếp tầng, tầng dưới cùng lục tươi, nền trắng). Ảnh mẫu "
               "`H01.png`: đầu (mặt da đá lam, một mắt hổ phách, vòi, mái lá lục sẫm, nền trắng).",
               "Kiểm: đặt chồng lên ảnh mẫu thì phần giữ lại phải khít; mỗi lớp một hình kín viền mực; nền trắng tinh; không bóng.", ""]
    gd += ["## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    _viet(os.path.join(pk(), "HUONG_DAN.md"), gd)
    for p in ra:
        print(p)


if __name__ == "__main__":
    main()
