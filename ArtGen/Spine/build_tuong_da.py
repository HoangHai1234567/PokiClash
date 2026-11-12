# -*- coding: utf-8 -*-
"""Gói GPT vẽ tinh linh tượng đá cổ giữ rừng (mã làm việc tuong_da, con gốc của rig: monster_3423). Tướng thứ 3 đảo Mộc.

Người dùng (2026-11-12): "concept tinh linh tượng đá cổ bảo vệ rừng, bị quấn rêu xanh; gen lại các bộ phận khác đi chút, theo thiên
hướng rừng cây, đá rừng hơn; ở giữa có thể là 1 lõi pha lê xanh hoặc lõi gì đó thể hiện trái tim khu rừng". Không dặn màu, chi tiết:
hai hướng dưới đây là ĐỀ XUẤT của Claude, chờ người dùng chọn. Chỉ lấy của con gốc cách dựng (các mảnh đá lơ lửng, chỗ đặt, cỡ, thứ
tự chồng); hình từng mảnh là của mình. Không đính ảnh con gốc; đính sơ đồ bố cục tự dựng bằng mã (tuong_da.py bo_cuc).

    py -3 -I ArtGen/Spine/tuong_da.py bo_cuc
    py -3 -I ArtGen/Spine/build_tuong_da.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tuong_da_1/luot_1_concept_<hướng>.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tuong_da"
K = int(os.environ.get("TD_DANG", "2"))
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
CACTUS = os.path.join(HERE, "inbox", "xuong_rong_1", "tai_ve", "L1_duyet.png")
SPIRIT = os.path.join(HERE, "inbox", "tinh_linh_2", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def pk(k=K):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def mau_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "mau")


INTRO = ("CREATURE: an ANCIENT STONE GUARDIAN SPIRIT of the forest, a plant-element monster for a monster-collecting game: the "
         "broken pieces of a very old carved temple statue, overgrown with green MOSS and wrapped by vines and tree roots, that "
         "FLOAT in the air and are held together by the HEART OF THE FOREST in the middle of its chest. It has NO legs and NO "
         "feet: it hovers. It has NO face: NO eyes, NO eyebrows, NO nose, NO mouth. Its arms are not connected to the body: the "
         "shoulder plates, the forearm boulders, the hands and the finger stones float near each other with white gaps between "
         "them. Character: a calm, heavy, powerful protector in a battle-ready stance: broad shoulders, two big boulder fists "
         "hanging at the ready. Chunky, bold, simple shapes with few details (the way a stone Pokemon is designed): appealing, "
         "not scary, not a smiling cute mascot.\n"
         "Follow the LAYOUT GUIDE (image 1) for WHERE every piece floats on the canvas, HOW BIG it is and WHICH piece overlaps "
         "which. The outlines in the guide are only rough computer blobs: design the real outline of every piece yourself as "
         "described below, as a chunky hand-carved or naturally broken block with its own character (a chipped corner, a "
         "broken edge), but keep every piece in its place and at its size.\n"
         "- VIEW: three-quarter front view; the creature is turned slightly toward the viewer's RIGHT. Its near arm is at the "
         "viewer's LEFT, in front; its far arm is at the viewer's RIGHT, partly behind the body.")

HEAD = {
    "pha_le": ("- HEAD CREST (top, from about x = 550 to x = 1094, y = 131 to y = 385): one wide slab of carved statue stone "
               "like a broad stone crown or lintel: its two ends sweep outward and up like blunt horns, its lower middle narrows "
               "to a short stem that rests on the orb. A thick cap of MOSS lies along its whole top edge, with a bumpy lower "
               "edge, and ONE tiny fern sprout with two little leaves grows from the moss near its left end. On the front of "
               "the slab, carved as thin groove lines: ONE big simple LEAF emblem with a centre vein and four side veins. No "
               "face on it."),
    "gac": ("- HEAD CREST (from about x = 550 to x = 1094, y = 131 to y = 385): one wide slab of carved statue stone like a "
            "broad stone brow: its two ends sweep outward and up, its lower middle narrows to a short stem that rests on the "
            "orb. A thick cap of MOSS lies along its whole top edge, with a bumpy lower edge. From each upper end of the slab "
            "grows ONE living wooden BRANCH like a stag's ANTLER (brown bark): the left one rising up-left to about x = 480-680, "
            "y = 35-150, the right one rising up-right to about x = 970-1170, y = 35-150; each antler forks into three short "
            "twigs and carries three or four small green leaves at the tips. On the front of the slab, carved as thin groove "
            "lines: ONE simple spiral. No face on it."),
}

CORE = {
    "pha_le": ("- HEART OF THE FOREST (the centre of the chest, from about x = 732 to x = 866, y = 432 to y = 696): ONE big "
               "EMERALD-GREEN CRYSTAL, tall and pointed at both ends like a leaf bud, with three or four flat facets (the "
               "facets on its right half the darker green). It floats INSIDE the chest rings: the rings cross in front of it, "
               "so it shows through the openings between them, about half of it visible. It is the brightest, most saturated "
               "thing in the picture, but it is flat colour: no glow, no rays, no sparkle.\n"
               "- SMALL CRYSTALS: seven small shards of the same green crystal, each a slim pointed splinter about 60-120 px "
               "long standing upright, float in the gaps between each shoulder plate and its forearm boulder: three at the "
               "viewer's left (at about x = 498, y = 508; x = 418, y = 576; x = 488, y = 636) and four at the right (at about "
               "x = 1039, y = 509; x = 1032, y = 633; x = 1052, y = 660; x = 1126, y = 601). One more small crystal tip "
               "peeks out under the chest at about x = 805, y = 665."),
    "gac": ("- HEART OF THE FOREST (the centre of the chest, from about x = 720 to x = 880, y = 470 to y = 690): ONE big "
            "living SEED, egg-shaped and smooth, bright jade green, with one spiral line carved on it and a tiny sprout of two "
            "leaves at its top; two or three thin brown roots grow from it and hold on to the chest rings. It sits INSIDE the "
            "chest rings: the rings cross in front of it, so it shows through the openings between them, about half of it "
            "visible. It is the brightest, most saturated thing in the picture, but it is flat colour: no glow, no rays, no "
            "sparkle.\n"
            "- FLOATING LEAVES: seven small pointed LEAVES of the same bright jade green, each a slim leaf about 60-120 px "
            "long standing upright with one centre vein, float in the gaps between each shoulder plate and its forearm "
            "boulder: three at the viewer's left (at about x = 498, y = 508; x = 418, y = 576; x = 488, y = 636) and four at "
            "the right (at about x = 1039, y = 509; x = 1032, y = 633; x = 1052, y = 660; x = 1126, y = 601)."),
}

BODY = ("- ORB (centre at about x = 855, y = 407, about 75 px across): a smooth round ball of dark forest rock sitting between "
        "the head crest and the chest like a neck joint, in front of both; one thin spiral groove carved on it.\n"
        "- CHEST (from about x = 632 to x = 953, y = 358 to y = 690): a hollow cage made of two or three thick curved RINGS "
        "and arcs of statue stone, like fragments of a round stone window, one behind the other, open in the middle so the "
        "heart shows through. The upper ring carries a patch of moss on its top; the inner faces of the rings (seen through "
        "the openings) are the darker inner-stone colour. A small carved stone BUCKLE piece (about 120 px wide) sits at the "
        "lower front of the chest at about x = 791-913, y = 578-690.\n"
        "- UNDER THE CHEST: instead of legs, one big pointed shard of dark forest rock hangs point-down under the chest "
        "(about x = 689-822, y = 593-801, partly hidden behind the chest), with two small pointed rock splinters floating "
        "beside it (one at about x = 700, y = 778, one at about x = 853, y = 692). Nothing else below: the creature hovers.\n"
        "- NEAR SHOULDER PLATE (viewer's left, in FRONT of the chest, from about x = 410 to x = 695, y = 210 to y = 536): one "
        "big curved plate of statue stone like a broken piece of a stone dome or a huge roof tile, rounded on top, hollow "
        "underneath (the darker inner-stone colour shows at its lower left opening). A thick cap of moss on its top, a vine "
        "with two small leaves creeping over its upper left edge. Two carved groove lines follow its curve.\n"
        "- FAR SHOULDER PLATE (viewer's right, BEHIND the chest and the head crest, from about x = 873 to x = 1141, y = 206 to "
        "y = 537; its darker inner side shows between it and the chest at about x = 800-1000, y = 300-460): the same kind of "
        "plate, mirrored, with moss on top and one vine hanging down across it.\n"
        "- NEAR FOREARM (viewer's left, floating below the near shoulder plate with a clear white gap, from about x = 372 to "
        "x = 588, y = 609 to y = 831): one big angular BOULDER of dark forest rock, wider at the top, with moss on its top "
        "face and two or three straight facet lines. Around its lower end (the wrist, about x = 464-601, y = 728-863) a "
        "thick brown tree ROOT is wound twice like a bracelet.\n"
        "- NEAR HAND (below the root bracelet, about x = 477-660, y = 749-892): one small chunky block of the same dark rock "
        "(the palm) with FOUR separate little rounded stones as fingers, loosely curled into a fist, each with its own "
        "closed outline, floating right next to the palm.\n"
        "- FAR FOREARM (viewer's right, from about x = 947 to x = 1164, y = 569 to y = 809), FAR ROOT BRACELET (about "
        "x = 952-1095, y = 730-813) and FAR HAND with four finger stones (about x = 886-1077, y = 775-886): the same as the "
        "near ones, mirrored, a little smaller.\n"
        "- Exactly: one head crest, one orb, one chest cage, one heart, one buckle, three hanging rock shards, two shoulder "
        "plates, two forearm boulders, two root bracelets, two hands with four finger stones each, three vines.")

PALETTE = {
    "pha_le": ("COLOURS, a calm, slightly muted palette (use exactly these, each area one flat colour): the carved STATUE "
               "STONE (head crest, shoulder plates, chest rings, buckle) pale weathered limestone (#C4BEA6); the inner / "
               "hidden faces of the statue stone and every carved groove line darker stone (#8C8878); the FOREST ROCK "
               "(forearm boulders, palms, finger stones, the hanging shards, the orb) dark earthy grey-brown (#6E685C); MOSS "
               "moss green (#629C48); vines and leaves deeper green (#46803E); the tree roots warm brown (#805836); the "
               "crystals bright emerald (#40CE8C) with the darker facets (#1E9668); every outline dark-brown ink (#2B2118). "
               "Only these colours. NO blue, NO purple, NO white stone, NO gold."),
    "gac": ("COLOURS, a calm, slightly muted palette (use exactly these, each area one flat colour): the carved STATUE STONE "
            "(head crest, shoulder plates, chest rings, buckle) pale weathered limestone (#C4BEA6); the inner / hidden faces "
            "of the statue stone and every carved groove line darker stone (#8C8878); the FOREST ROCK (forearm boulders, "
            "palms, finger stones, the hanging shards, the orb) dark earthy grey-brown (#6E685C); MOSS moss green (#629C48); "
            "vines and the antler leaves deeper green (#46803E); the antler branches and the tree roots warm brown "
            "(#805836); the seed heart and the floating leaves bright jade green (#40CE8C) with their vein and spiral lines "
            "darker green (#1E9668); every outline dark-brown ink (#2B2118). Only these colours. NO blue, NO purple, NO white "
            "stone, NO gold, NO crystals."),
}

FRAME = {
    "pha_le": ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
               "visible, nothing cut by the edges. As in the guide, the whole creature is about 800 px wide (from about "
               "x = 370 to x = 1165) and about 765 px tall (from the top of the head crest at about y = 130 to the lowest "
               "finger stone at about y = 892)."),
    "gac": ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
            "visible, nothing cut by the edges. As in the guide, the whole creature is about 800 px wide (from about x = 370 "
            "to x = 1165) and about 860 px tall (from the antler tips at about y = 30 to the lowest finger stone at about "
            "y = 892)."),
}

POSE = ("POSE (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): hovering still "
        "in a calm, clean resting pose, exactly as in the guide. EVERY piece is one closed shape with its own closed ink "
        "outline, and the floating pieces keep clear white gaps between them as in the guide (shoulder plate / forearm "
        "boulder / hand / each finger stone / each small floating piece / the hanging rock shards). No dust, no sparkles, no "
        "glow, no motion lines, no falling pebbles, no ground, no grass, no props.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The "
        "layout guide is a stiff flat computer diagram with rough, jagged edges and a mechanical dripping moss edge: take "
        "only the placement, the sizes, the overlaps and the colour of each kind of piece from it, never its line, its jagged "
        "edge noise or its exact blobs. Draw the moss as soft rounded cushions with a bumpy scalloped edge (not as dripping "
        "paint), the stones as bold chunky blocks, the vines as simple curling stems with two or three small leaves.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with "
        "a dark-brown ink pen (#2B2118), an outline about 6 px thick on this canvas around every stone piece, moss cap, root "
        "and big crystal or seed, and about 4 px for small details (finger stones, small floating pieces, vines, leaves); the "
        "carved grooves and the facet lines are thin darker pencil lines about 4 px, not ink; every area coloured with "
        "coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the outline), "
        "kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed: no small cracks all "
        "over, no pebbly texture, no realistic rock rendering.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side of a stone, no lighter patches or blotches, no shadows of any kind (no "
        "cast shadow of one piece on another, no shadow under the figure or on the background), no white highlights or shine "
        "spots, no gloss, no reflections on the crystal or seed, no glow, no rim light, no gradients, no 3D look. A different "
        "tone appears only where the design itself lists a different colour (inner faces, facets, moss).")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the creature.")

TEN = {"pha_le": "lõi pha lê lục, mào đá khắc hình lá", "gac": "gạc cây trên mào đá, lõi là hạt mầm, lá bay"}


def refs(kieu):
    them = ("the green crystal heart in the chest and the small green crystal shards between shoulders and forearms"
            if kieu == "pha_le" else
            "the two brown branch antlers with leaves on the head crest, the green seed heart in the chest and the small green "
            "leaves between shoulders and forearms")
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature showing where every floating "
         "piece goes on the canvas, how big it is and which piece overlaps which (pale statue stone: the wide head crest on top, "
         "the two big shoulder plates, the chest rings and the buckle; darker stone: the inner faces; dark grey-brown: the orb "
         "under the crest, the two forearm boulders, the hands and finger stones, the pointed shards under the chest; green "
         f"caps: moss; brown bands: the root bracelets; dark green: vines; {them}). Use it for placement, size and overlap "
         "only; redraw everything in the hand-drawn style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): các khối đá lơ lửng tô phẳng theo nhóm màu (đá tượng kem xám: mào "
         "đầu rộng, hai tấm vai, vòng ngực, khoá; đá tảng nâu xám: quả cầu cổ, hai cẳng tay, bàn tay, ngón, chóp đá dưới ngực; "
         "mảng lục: rêu; đai nâu: rễ quấn cổ tay; lõi lục giữa ngực). Lấy chỗ đặt, cỡ, thứ tự chồng"),
        (CACTUS,
         "an approved hero of the same game and the same island (a round cactus monster), 1536x1024, white background: match "
         "EXACTLY its wobbly dark-brown pen line, its visible crayon hatching, its completely flat colouring and its bold, "
         "simple, chunky level of detail. Do NOT copy its species, its design or its colours.",
         "Xương rồng tròn đã duyệt (1536 × 1024, nền trắng): quả cầu lục miệng to nanh kem. Lấy nét bút rung, vân sáp, tô phẳng, mức "
         "chi tiết gọn"),
        (SPIRIT,
         "another approved hero of the same island (a chubby jelly forest spirit), 1536x1024, white background: the same line "
         "and flat crayon colouring, the same calm muted colours; see how its leaves are drawn. Do NOT copy its species, "
         "design or colours.",
         "Tinh linh rừng mập đã duyệt (1536 × 1024, nền trắng): thạch lục mầm hai lá. Lấy nét, tô phẳng, cách vẽ lá"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching) and the way its rocks and mossy stones are simplified, nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp, cách giản lược đá và rêu"),
    ]


CHECK = [
    "**Không mặt, không chân**: các mảnh đá **lơ lửng**, có khe trắng giữa tấm vai / cẳng tay / bàn tay / ngón; mỗi mảnh viền mực kín.",
    "Đủ: mào đầu rộng, quả cầu cổ, lồng ngực vòng đá hở giữa lộ **lõi lục**, khoá đá, ba chóp đá dưới ngực, hai tấm vai (tấm bên "
    "trái ở trước, tấm bên phải ở sau), hai tảng cẳng tay có **rễ nâu quấn cổ tay**, hai bàn tay mỗi bàn **bốn ngón đá rời**.",
    "**Rêu** phủ mặt trên mào, hai vai, hai cẳng tay (mảng lục mép lượn, không nhỏ giọt); ba dây leo có lá.",
    "Hướng `pha_le`: lõi là **pha lê lục** thoi nhọn hai đầu + bảy mảnh pha lê nhỏ; mào khắc hình lá, một mầm dương xỉ. Hướng `gac`: "
    "hai **nhánh gạc cây** nâu có lá trên mào; lõi là **hạt mầm** lục có mầm hai lá; bảy chiếc lá bay.",
    "Màu: đá tượng kem xám, đá tảng nâu xám, rêu lục, rễ nâu, lõi lục tươi; **không** lam, không tím, không đá trắng.",
    "Tô phẳng: **không** bóng, không mảng sáng tối trên đá, không điểm sáng, lõi không phát sáng; nền trắng tinh.",
]

FIX = [
    ("Vẽ thêm mắt, mặt, chân", "It has NO face and NO legs: remove the eyes / mouth / legs. It is only floating stone pieces."),
    ("Các mảnh dính liền nhau thành một khối", "The pieces FLOAT apart: keep clear white gaps between each shoulder plate, its "
                                               "forearm boulder, its hand and every finger stone, exactly as in image 1."),
    ("Có bóng, mảng sáng tối, đá vẽ nổi khối", "Flat colour only: remove every shadow, highlight, darker side and gradient; each "
                                               "stone is one even colour with two or three thin groove lines; keep the crayon "
                                               "hatching as texture only."),
    ("Lõi phát sáng, có tia, quầng", "The heart is flat colour: remove the glow, the rays and the sparkles."),
    ("Quá nhiều vết nứt, sỏi, chi tiết", "Simplify: bold chunky blocks, at most two or three groove or crack lines per piece."),
    ("Pha lê màu lam", "The crystals are emerald GREEN (#40CE8C / #1E9668), not blue."),
    ("Rêu nhỏ giọt như sơn chảy", "Draw the moss as soft rounded cushions lying on the top faces, with a bumpy scalloped lower "
                                  "edge, not as dripping paint."),
    ("Bố cục khác sơ đồ", "Follow image 1 exactly for the place and size of every piece: the near arm at the left in front, "
                          "the far arm at the right behind, the head crest on top resting on the orb."),
]


def main():
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    gd = [f"# Gói gửi GPT: `{CODE}` dạng {K} (tinh linh tượng đá cổ giữ rừng, tướng thứ 3 đảo Mộc, tên chưa đặt)", "",
          "Làm 2026-11-12: dựng trên rig của con gốc `monster_3423` (mọi mảnh cứng, lơ lửng); hình từng mảnh, màu, chi tiết là đề "
          "xuất của Claude, chờ người dùng chọn hướng và duyệt concept. Ghi chú: `ArtGen/Spine/inbox/tuong_da_ghichu.md`.", "",
          "Lượt 2 (mảnh) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    ra = []
    for kieu in ("pha_le", "gac"):
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
              INTRO, HEAD[kieu], BODY.split("\n")[0], BODY.split("\n")[1], CORE[kieu], "\n".join(BODY.split("\n")[2:]), "",
              PALETTE[kieu], "", FRAME[kieu], "", POSE, "", SOFT, LINE, FLAT, BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd += [f"## Hướng `{kieu}`: {TEN[kieu]}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{K}/luot_1_concept_{kieu}.txt` (thêm "
               "`--note \"...\"` để sửa nhanh).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += [""]
    gd += ["Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/tuong_da.py bo_cuc`).",
           "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    open(os.path.join(pk(), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 1b: người dùng chọn hướng "gac" (2026-11-12) và dặn sửa:
# "chỗ nối vai với tay thay lá thành những viên đá nhỏ"; "phần đầu nhìn bị giống con gốc quá, đổi kiểu dáng"
DAU_MOI = {
    "tru": ("a short, broad STONE DRUM, like the top section of a broken temple pillar or a tree stump made of stone: seen from "
            "the front one chunky block about 270 px wide and 215 px tall (from about x = 690 to x = 960, y = 170 to y = 385), "
            "with a flat top, nearly straight sides that taper slightly toward the bottom, and rounded, chipped corners; a small "
            "piece is broken off its upper right corner",
            "khối trụ đá cụt (như khúc cột đền gãy / gốc cây bằng đá), rộng ~270, cao ~215"),
    "vom": ("a rounded STONE DOME, like a big egg-shaped boulder or an old stone helmet: seen from the front one chunky rounded "
            "shape about 300 px wide and 215 px tall (from about x = 675 to x = 975, y = 170 to y = 385), round on top and at "
            "the sides, almost flat underneath, with one chipped notch in its lower left edge",
            "vòm đá tròn (như tảng đá hình trứng / mũ đá cổ), rộng ~300, cao ~215"),
}


def build_sua():
    nhap = os.path.join(save_dir(), "L1_gac.png")
    if not os.path.exists(nhap):
        raise SystemExit("thiếu bản nháp " + Wp(nhap))
    ra = []
    gd = ["", "## Lượt 1b: sửa hướng `gac` (2026-11-12)", "",
          "Người dùng chọn hướng `gac` và dặn: chỗ nối vai với tay thay lá bằng **những viên đá nhỏ**; phần đầu giống con gốc quá, **đổi "
          "kiểu dáng**. Lượt này vẽ lại y hệt bản nháp `L1_gac.png`, chỉ đổi hai thứ đó. Hai kiểu đầu để người dùng chọn.", ""]
    for kieu, (en, vi) in DAU_MOI.items():
        out = os.path.join(save_dir(), f"L1b_{kieu}.png")
        p = os.path.join(pk(), f"luot_1b_dau_{kieu}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(nhap)}: the DRAFT of this creature, 1536x1024, white background: an ancient stone guardian spirit made "
             "of floating statue pieces overgrown with moss: a WIDE winged stone head crest with two brown branch antlers, a round "
             "spiral orb under it, two big mossy shoulder plates, a chest of stone rings holding a green seed, a square buckle, "
             "pointed rock shards under the chest, two dark boulder forearms with brown root bracelets and stone fists, and seven "
             "small green LEAVES floating between the shoulder plates and the forearms. This is the design, the line and the "
             "colouring to keep.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as L1b_{kieu}_2.png, L1b_{kieu}_3.png ... in the same folder. Do not "
             "edit, move or delete any other file.", "",
             "TASK: redraw image 1 as ONE picture, changing ONLY the two things listed under CHANGE.", "",
             "KEEP IDENTICAL to image 1, in the same place and at the same size (if the new picture were laid over image 1, "
             "everything else must coincide): the round spiral orb (centre at about x = 825, y = 412), both shoulder plates with "
             "their moss caps, vines and carved grooves, the chest rings, the green seed heart with its sprout, its spiral and its "
             "brown roots, the square buckle with its spiral, the three pointed rock shards under the chest, both forearm boulders "
             "with their moss, both brown root bracelets, both stone hands with their finger stones, every colour, the wobbly "
             "dark-brown ink line, the crayon hatching, the completely flat colouring, the white background. Still NO face (no "
             "eyes, no mouth) and NO legs.", "",
             "CHANGE 1, THE HEAD. Remove the wide winged head crest of image 1 completely (the broad slab whose two ends sweep "
             f"outward and up). In its place draw a NEW, COMPACT head of the same pale statue stone: {en}. It is centred above "
             "the orb (centre line at about x = 825) and its underside rests on the orb exactly where the old crest did; the orb "
             "stays in front of it. A thick cushion of moss with a bumpy scalloped lower edge lies on its whole top. On its front "
             "one simple carved spiral groove, as on the old crest, and one or two short curved groove lines. NO face on it: no "
             "eyes, no mouth, no holes that read as eyes.",
             "KEEP THE TWO BRANCH ANTLERS, but plant them on the new head: they grow out of the moss on its top, one near its "
             "left end rising up and outward to the LEFT (tips at about x = 560-700, y = 15-110), one near its right end rising "
             "up and outward to the RIGHT (tips at about x = 950-1090, y = 15-110); the same brown bark, each forking into three "
             "short twigs with one green leaf at each tip, a little bigger than in image 1, like the antlers of a young stag.",
             "Because the new head is much narrower than the old crest, the parts of the two shoulder plates and of the far "
             "shoulder plate's inner side that the old crest used to cover are now visible: complete them (their rounded tops, "
             "moss caps and outlines) in the same style. Leave a clear white gap between the head and each shoulder plate.", "",
             "CHANGE 2, THE FLOATING PIECES BETWEEN SHOULDERS AND FOREARMS. Replace each of the seven small green floating LEAVES "
             "(three under the left shoulder plate, four under the right one) with ONE small floating STONE in the same place: "
             "small chunky pebbles and angular chips of the dark forest rock (the same dark grey-brown as the forearm boulders, "
             "#6E685C), each about 45-80 px, each a different simple shape (round pebble, flat chip, little wedge), each with its "
             "own closed ink outline and at most one facet line; two of them carry a tiny dab of moss on top. They float freely "
             "with white gaps around them, like a loose chain of rubble linking each shoulder to its forearm. No leaves there any "
             "more, no crystals.", "",
             "Do not add anything else: no extra stones elsewhere, no dust, no glow, no effects.", "", FLAT, BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd += [f"### Kiểu đầu `{kieu}`: {vi}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
               f"| 1 | `{Wp(nhap)}` | Bản nháp hướng gạc cây (1536 × 1024, nền trắng): tượng đá lơ lửng phủ rêu, mào đầu rộng hai cánh có hai "
               "nhánh gạc, lõi hạt mầm lục, bảy chiếc lá bay ở khớp vai – tay |", ""]
    gd += ["Kiểm: đầu là một khối gọn (không còn mào rộng hai cánh), có rêu trên đỉnh, hai nhánh gạc mọc từ đỉnh, một hình xoắn khắc, không "
           "mặt; bảy viên đá nhỏ nâu xám thay bảy chiếc lá; mọi thứ khác trùng bản nháp; hai tấm vai vẽ đủ phần trước bị mào che."]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 1b")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 2: mảnh "đúng chỗ, đúng cỡ" từ concept đã duyệt (L1_duyet.png = L1b_tru)
# Mọi mảnh của rig là mảnh CỨNG một xương: mỗi lượt giữ lại vài mảnh KHÔNG chồng nhau, vẽ đủ phần khuất, bỏ hết thứ khác.
MANH_CHUNG = ("TASK: redraw image 1, but keep ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the "
              "SAME SIZE as in image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). "
              "REMOVE everything else and leave pure white (#FFFFFF) there. Every kept part must be ONE COMPLETE CLOSED SHAPE with "
              "the dark-brown ink outline running all the way around it: where a part is hidden behind another part in image 1, "
              "DRAW the hidden portion as described. The kept parts must NOT touch each other: clear white between them. Same "
              "wobbly ink line, same colours, same crayon hatching, same completely flat colouring as image 1. Do not add "
              "anything: no shadows, no glow, no dust, no labels.")
MANH2 = {
    "A": ("đầu (trụ đá + rêu + hai nhánh gạc), tấm vai XA vẽ đủ, chóp đá to vẽ đủ",
          ["1. THE HEAD: the stone drum head with the moss cushion on its top and BOTH branch antlers with all their leaves (from "
           "about x = 515 to x = 1085, y = 5 to y = 380). In image 1 the round spiral orb overlaps the middle of its lower edge: "
           "remove the orb and complete the underside of the head as one smooth, slightly curved edge with an ink line.",
           "2. THE RIGHT SHOULDER PLATE: the big curved stone plate at the viewer's RIGHT (its visible part from about x = 905 to "
           "x = 1200, y = 288 to y = 556) with its moss cap and its hanging vine. In image 1 its left part is hidden behind the "
           "chest ring: complete it. The complete plate is the mirror image of the left shoulder plate of image 1: a broken piece "
           "of a stone dome, rounded on top, about 330 px wide (reaching left to about x = 870), with the moss cap continuing "
           "along its top, the carved arc grooves continuing, and its jagged lower edge with the darker inner-stone underside "
           "continuing to its left end.",
           "3. THE BIG HANGING SHARD: the big pointed shard of dark rock under the chest (its visible part from about x = 665 to "
           "x = 835, y = 705 to y = 880, its point down at about x = 750, y = 878). In image 1 its top is hidden behind the lower "
           "hoop and the buckle: complete it upward into one chunky faceted rock shaped like a spinning top: widest at about "
           "y = 705, with a low blunt faceted top reaching up to about y = 640. Do NOT keep the two small rock splinters beside it."]),
    "B": ("vòng ngực đứng vẽ đủ (lỗ giữa để trắng), hai khối lòng bàn tay vẽ đủ (không ngón, không rễ)",
          ["1. THE UPRIGHT CHEST RING: the big round stone ring that stands upright in the middle of the chest (outer edge from "
           "about x = 660 to x = 985, y = 400 to y = 700; the band about 55 px wide), with the two moss patches on its top and "
           "the small sprouting vine at its upper left. Complete it into ONE full closed ring, like a thick stone hoop seen from "
           "the front: in image 1 its top is partly covered by the round spiral orb, its lower part by the lower hoop, the brown "
           "roots and the buckle, its left side by the left shoulder plate: draw all those portions of the band. The round hole "
           "in the middle is EMPTY, pure white: no seed, no sprout, no roots, no darker stone inside.",
           "2. THE LEFT PALM: the main block of the LEFT stone hand: the chunk of dark rock directly below the left root "
           "bracelet (about x = 410 to x = 610, y = 835 to y = 945), WITHOUT the round finger stones and WITHOUT the root "
           "bracelet. Complete it into one chunky rounded block of dark forest rock about 200 px wide and 115 px tall, with one "
           "or two thin facet lines, a closed ink outline all round.",
           "3. THE RIGHT PALM: the same for the RIGHT stone hand: the chunk of dark rock directly below the right root bracelet "
           "(about x = 955 to x = 1135, y = 830 to y = 925), WITHOUT finger stones and WITHOUT the bracelet: one chunky rounded "
           "block about 180 px wide and 100 px tall."]),
    "C": ("vòng ngực nằm (đai dưới) vẽ đủ thành một vành bầu dục kín + hai rễ nâu móc lên",
          ["1. THE LOWER HOOP of the chest: the wide stone hoop that lies almost flat around the bottom of the chest, like a belt "
           "seen slightly from above (outer edge from about x = 583 to x = 1000, y = 505 to y = 705). Its FRONT is the pale "
           "stone band that runs across the bottom of the chest (through about x = 600 to x = 1000, y = 600 to y = 700, behind "
           "the buckle and up the left side to about x = 590, y = 560). Its REAR, seen through the opening, is the darker "
           "inner-stone wall (visible in image 1 at about x = 640-700, y = 555-625 and as the dark band across the middle at "
           "about y = 515-545). Complete it into ONE full closed elliptical hoop: the pale outer band in front, the darker inner "
           "wall at the back, both ends joined on the right as on the left. Where the buckle, the upright ring, the seed and the "
           "shoulder plates covered it in image 1, continue the band. The opening in the middle of the hoop is EMPTY, pure "
           "white. No buckle, no seed, no upright ring.",
           "2. THE TWO BROWN ROOTS, joined to the hoop (part of the same shape): the two short thick brown roots that grow up "
           "from the front band (the left one from about x = 705, y = 650 up to about x = 770, y = 575; the right one from about "
           "x = 930, y = 650 up to about x = 870, y = 590) and curl inward like two little hooks; complete their rounded tips."]),
    "D": ("hạt mầm lục vẽ đủ hình trứng (có mầm hai lá), không rễ",
          ["1. THE SEED HEART: the bright green seed with the dark-green spiral on it and the two-leaf sprout on its top (from "
           "about x = 755 to x = 890, y = 470 to y = 650). In image 1 its sides are held by the brown roots and its bottom is "
           "covered by the buckle: REMOVE the roots and complete the seed into one smooth closed egg shape, rounded at the "
           "bottom (lowest point at about x = 822, y = 660), flat bright green with the same spiral. Nothing else."]),
    "E": ("quả cầu cổ, tấm vai GẦN, khoá, hai tảng cẳng tay + đai rễ (không bàn tay), hai chóp đá nhỏ, bảy viên đá nhỏ",
          ["1. THE ORB: the round dark spiral orb (centre at about x = 820, y = 412, about 95 px across), complete circle.",
           "2. THE LEFT SHOULDER PLATE (about x = 325 to x = 662, y = 262 to y = 560) with its moss cap, its vine and leaf: as in "
           "image 1 (it is fully visible).",
           "3. THE BUCKLE: the square stone buckle with the spiral (about x = 785 to x = 905, y = 648 to y = 735), complete.",
           "4. THE LEFT FOREARM: the big dark boulder with its moss cap (about x = 322 to x = 580, y = 645 to y = 880) together "
           "with the brown root bracelet wound around its lower end (about x = 380 to x = 640, y = 790 to y = 905), WITHOUT the "
           "hand: remove the palm block and all the round finger stones below the bracelet; complete the lower edge of the "
           "bracelet and let the boulder end just below it in a short blunt faceted end.",
           "5. THE RIGHT FOREARM: the same for the right boulder with its moss cap (about x = 968 to x = 1198, y = 660 to "
           "y = 850) and its root bracelet (about x = 975 to x = 1145, y = 795 to y = 860), WITHOUT the hand.",
           "6. THE TWO SMALL ROCK SPLINTERS beside the big hanging shard: the one at the left (about x = 648-708, y = 775-886) "
           "and the one at the right (about x = 830-875, y = 745-825), each complete. Do NOT keep the big shard between them.",
           "7. THE SEVEN SMALL FLOATING STONES between the shoulder plates and the forearms (three at the left at about "
           "x = 453, y = 552; x = 383, y = 609; x = 485, y = 629; four at the right at about x = 1063, y = 570; x = 1161, "
           "y = 597; x = 1047, y = 641; x = 1108, y = 632), each complete with its own closed outline, and with a small white "
           "gap between the lowest right one and the moss of the right forearm."]),
}


# dạng 1 "Mầm Đá": cùng cách chia, toạ độ đo trên concept dạng 1 đã duyệt (2026-11-12); chỉ bốn viên đá nhỏ, không gạc, không dây leo
MANH1 = {
    "A": ("đầu (chum đá tròn + rêu + mầm hai lá), tấm vai XA vẽ đủ, chóp đá to vẽ đủ",
          ["1. THE HEAD: the round stone pot head with the moss cushion on its top and the small two-leaf sprout (from about "
           "x = 625 to x = 950, y = 56 to y = 395). In image 1 the round spiral orb overlaps the middle of its lower edge: remove "
           "the orb and complete the underside of the head as one smooth round edge with an ink line.",
           "2. THE RIGHT SHOULDER PLATE: the curved stone plate at the viewer's RIGHT (from about x = 890 to x = 1130, y = 350 to "
           "y = 555) with its moss patch and its carved arc. In image 1 its lower left corner is slightly hidden behind the chest "
           "ring: complete it into one closed shape, the mirror image of the left shoulder plate.",
           "3. THE BIG HANGING SHARD: the pointed shard of dark rock under the chest (its visible part from about x = 685 to "
           "x = 820, y = 745 to y = 875, its point down at about x = 750, y = 873). In image 1 its top is hidden behind the lower "
           "hoop and the buckle: complete it upward into one chunky faceted rock shaped like a spinning top: widest at about "
           "y = 745, with a low blunt faceted top reaching up to about y = 690. Do NOT keep the two small rock splinters beside it."]),
    "B": ("vòng ngực đứng vẽ đủ (lỗ giữa để trắng), hai khối lòng bàn tay vẽ đủ (không ngón, không rễ)",
          ["1. THE UPRIGHT CHEST RING: the round stone ring that stands upright in the middle of the chest (outer edge from about "
           "x = 655 to x = 950, y = 450 to y = 725; the band about 50 px wide), with the moss patch on its top. Complete it into "
           "ONE full closed ring, like a thick stone hoop seen from the front: in image 1 its top is partly covered by the round "
           "spiral orb, its lower part by the lower hoop, the brown roots and the buckle: draw all those portions of the band. "
           "The round hole in the middle is EMPTY, pure white: no seed, no roots, no darker stone inside.",
           "2. THE LEFT PALM: the main block of the LEFT stone hand: the chunk of dark rock directly below the left root ring "
           "(about x = 420 to x = 580, y = 868 to y = 945), WITHOUT the round finger stones and WITHOUT the root ring. Complete it "
           "into one chunky rounded block of dark forest rock about 160 px wide and 85 px tall, with one thin facet line, a "
           "closed ink outline all round.",
           "3. THE RIGHT PALM: the same for the RIGHT stone hand: the chunk of dark rock directly below the right root ring "
           "(about x = 945 to x = 1090, y = 860 to y = 930), WITHOUT finger stones and WITHOUT the root ring: one chunky rounded "
           "block about 145 px wide and 75 px tall."]),
    "C": ("vòng ngực nằm (đai dưới) vẽ đủ thành một vành bầu dục kín + hai rễ nâu móc lên",
          ["1. THE LOWER HOOP of the chest: the wide stone hoop that lies almost flat around the bottom of the chest, like a belt "
           "seen slightly from above (outer edge from about x = 592 to x = 960, y = 540 to y = 732). Its FRONT is the pale stone "
           "band that runs across the bottom of the chest (through about x = 600 to x = 955, y = 640 to y = 730, behind the "
           "buckle and up the left side to about x = 595, y = 600). Its REAR, seen through the opening, is the darker "
           "inner-stone wall. Complete it into ONE full closed elliptical hoop: the pale outer band in front, the darker inner "
           "wall at the back, both ends joined on the right as on the left. Where the buckle, the upright ring, the seed and the "
           "shoulder plates covered it in image 1, continue the band. The opening in the middle of the hoop is EMPTY, pure "
           "white. No buckle, no seed, no upright ring.",
           "2. THE TWO BROWN ROOTS, joined to the hoop (part of the same shape): the two short thick brown roots that grow up "
           "from the front band (the left one from about x = 700, y = 680 up to about x = 765, y = 608; the right one from about "
           "x = 925, y = 680 up to about x = 860, y = 612) and curl inward like two little hooks; complete their rounded tips."]),
    "D": ("hạt mầm lục chưa nảy, vẽ đủ hình trứng, không rễ",
          ["1. THE SEED HEART: the bright green closed seed with the dark-green spiral on it (from about x = 735 to x = 875, "
           "y = 528 to y = 675), with NO sprout. In image 1 its sides are held by the brown roots and its bottom is covered by "
           "the buckle: REMOVE the roots and complete the seed into one smooth closed egg shape, rounded at the bottom (lowest "
           "point at about x = 805, y = 690), flat bright green with the same spiral. Nothing else."]),
    "E": ("quả cầu cổ, tấm vai GẦN, khoá, hai tảng cẳng tay + vòng rễ (không bàn tay), hai chóp đá nhỏ, bốn viên đá nhỏ",
          ["1. THE ORB: the round dark spiral orb (centre at about x = 795, y = 415, about 95 px across), complete circle.",
           "2. THE LEFT SHOULDER PLATE (about x = 396 to x = 653, y = 324 to y = 545) with its moss patch and its carved arc: as "
           "in image 1 (it is fully visible).",
           "3. THE BUCKLE: the square stone buckle with the spiral (about x = 770 to x = 880, y = 678 to y = 760), complete.",
           "4. THE LEFT FOREARM: the dark rounded boulder with its moss tuft (about x = 363 to x = 568, y = 678 to y = 880) "
           "together with the thin brown root ring wound around its lower end (at about y = 815 to y = 875), WITHOUT the hand: "
           "remove the palm block and all the round finger stones below the root ring; complete the lower edge of the root ring "
           "and let the boulder end just below it in a short blunt rounded end.",
           "5. THE RIGHT FOREARM: the same for the right boulder with its moss tuft (about x = 960 to x = 1147, y = 689 to "
           "y = 870) and its thin root ring (at about y = 815 to y = 862), WITHOUT the hand.",
           "6. THE TWO SMALL ROCK SPLINTERS beside the big hanging shard: the one at the left (about x = 651-698, y = 791-872) "
           "and the one at the right (about x = 815-859, y = 777-852), each complete. Do NOT keep the big shard between them.",
           "7. THE FOUR SMALL FLOATING STONES between the shoulder plates and the forearms (two at the left at about x = 472, "
           "y = 581 and x = 400, y = 637; two at the right at about x = 1050, y = 601 and x = 1130, y = 645), each complete "
           "with its own closed outline."]),
}
MANH = MANH1 if K == 1 else MANH2
MO_TA_EN = ("an ancient stone guardian spirit made of floating statue pieces overgrown with moss: a stone drum head with two branch "
            "antlers, a round spiral orb under it, two big mossy shoulder plates, a chest made of an upright stone ring and a lower "
            "stone hoop holding a green seed with brown roots, a square buckle, pointed rock shards under the chest, two dark "
            "boulder forearms with brown root bracelets, two stone hands with round finger stones, and seven small stones floating "
            "between the shoulder plates and the forearms." if K == 2 else
            "a young stone guardian spirit made of floating statue pieces: a round stone pot head with a moss cushion and one small "
            "two-leaf sprout, a round spiral orb under it, two small mossy shoulder plates, a chest made of an upright stone ring "
            "and a lower stone hoop holding a closed green seed with brown roots, a square buckle, pointed rock shards under the "
            "chest, two dark rounded boulder forearms each with a thin brown root ring, two stone hands with round finger stones, "
            "and four small stones floating between the shoulder plates and the forearms.")
MO_TA_VI = ("tượng đá lơ lửng phủ rêu, đầu trụ đá có hai nhánh gạc, lõi hạt mầm lục trong hai vòng ngực, hai tấm vai, hai tảng cẳng tay "
            "quấn rễ, bàn tay đá, bảy viên đá nhỏ ở khớp vai – tay" if K == 2 else
            "tượng đá non lơ lửng: đầu chum đá tròn có một mầm hai lá, lõi hạt mầm lục chưa nảy trong hai vòng ngực, hai tấm vai nhỏ, hai "
            "tảng cẳng tay tròn quấn một vòng rễ, bàn tay đá, bốn viên đá nhỏ ở khớp vai – tay")


def build_manh():
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    if not os.path.exists(duyet):
        raise SystemExit("chưa có concept duyệt " + Wp(duyet))
    ra = []
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ (2026-11-12, sau khi người dùng chọn đầu kiểu A = `L1b_tru.png` → `L1_duyet.png`)", "",
          "Mọi mảnh của rig là mảnh cứng một xương. Mỗi file vẽ lại concept đã duyệt nhưng chỉ giữ vài mảnh không chồng nhau, vẽ đủ phần "
          "khuất, bỏ hết thứ khác (nền trắng). Ảnh mẫu duy nhất của cả năm file:", "",
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
           "chạm nhau, phần khuất đã vẽ đủ, nền trắng tinh, không bóng. Claude cắt bằng `tuong_da_manh.py`."]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ---------------------------------------------------------------- DẠNG 1 "Mầm Đá" (người dùng 2026-11-12: "làm 2 dạng thôi, con vừa rồi là
# dạng 2, lát nữa bạn làm dạng 1"). Cùng rig, cùng clip: mỗi mảnh nằm quanh đúng chỗ của dạng 2, chỉ đổi cỡ và chi tiết.
# Thiết kế là ĐỀ XUẤT của Claude (người dùng không tả): bản non, chibi hơn: đầu to, chưa mọc gạc (một mầm hai lá), hạt mầm chưa nảy,
# vai và tay nhỏ, ít rêu, không dây leo.
def build_dang1():
    d2 = os.path.join(save_dir(2), "L1_duyet.png")
    if not os.path.exists(d2):
        raise SystemExit("chưa có concept dạng 2 đã duyệt " + Wp(d2))
    os.makedirs(pk(1), exist_ok=True)
    os.makedirs(save_dir(1), exist_ok=True)
    out = os.path.join(save_dir(1), "L1_concept.png")
    p = os.path.join(pk(1), "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(d2)}: the APPROVED picture of the GROWN form (second evolution stage) of this creature, 1536x1024, white "
         "background: an ancient stone guardian spirit made of floating statue pieces overgrown with moss: a stone drum head with "
         "two branch antlers, a round spiral orb under it, two big mossy shoulder plates with vines, a chest made of an upright "
         "stone ring and a lower stone hoop holding a sprouted green seed with brown roots, a square buckle, pointed rock shards "
         "under the chest, two dark boulder forearms with brown root bracelets, two stone hands with round finger stones, and "
         "seven small stones floating between the shoulder plates and the forearms. Use it for the design language, the line, "
         "the colours, the crayon hatching and the PLACEMENT of every piece.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not "
         "edit, move or delete any other file.", "",
         "TASK: draw the YOUNG form (FIRST evolution stage) of the creature of image 1 as ONE picture: the same stone guardian "
         "when it has just awakened: smaller pieces, rounder, a little chibi and cute but still a brave little guardian ready to "
         "fight; clearly the same creature as image 1, and clearly younger. Same hand-drawn style as image 1.", "",
         "CONSTRUCTION (very important: this picture will be animated on the SAME skeleton as image 1): it has the SAME kinds "
         "of floating pieces as image 1, and EVERY piece is CENTRED at the SAME PLACE on the canvas as the matching piece of "
         "image 1; only its size and details change as listed below. Because most pieces are smaller, the white gaps between "
         "the floating pieces are WIDER than in image 1. Still NO face (no eyes, no mouth), NO legs: it hovers. Three-quarter "
         "front view turned slightly to the viewer's RIGHT, exactly like image 1.", "",
         "WHAT CHANGES, piece by piece:",
         "- HEAD (centred at about x = 805, y = 285): the same stone drum, but ROUNDER and a little BIGGER in proportion (about "
         "290 px wide, 230 px tall), like a chubby stone pot; a thinner moss cushion on its top; NO antlers and no branches: "
         "instead ONE small green SPROUT with two round leaves grows from the middle of the moss (about 75 px tall, its top at "
         "about y = 95). The same single carved spiral on the front, no other grooves.",
         "- ORB (centre at about x = 820, y = 412): the same round dark spiral orb, same size.",
         "- SHOULDER PLATES (the left one centred at about x = 495, y = 410; the right one at about x = 1050, y = 420, partly "
         "behind the chest): the same broken-dome stone plates but only about THREE QUARTERS of the size (about 250 px wide), "
         "smoother and rounder, each with only ONE small moss patch on its top and ONE carved arc groove; NO vines, NO leaves on "
         "them.",
         "- CHEST (centred at about x = 820, y = 560): the same upright stone ring and the same lower stone hoop with the two "
         "small brown roots, about 90% of the size, with one small moss patch on top of the ring and no sprouting vine. Inside "
         "it the SEED HEART (centre at about x = 822, y = 575): the same bright green seed with its darker-green spiral, a "
         "little smaller, still CLOSED: NO sprout on it yet, a smooth egg.",
         "- BUCKLE (centred at about x = 845, y = 692): the same square spiral buckle, about 85% of the size.",
         "- UNDER THE CHEST: the big pointed rock shard, shorter (about 70% as long, centred at about x = 750, y = 760) and the "
         "two small rock splinters beside it, a little smaller.",
         "- FOREARMS (the left one centred at about x = 455, y = 760; the right one at about x = 1085, y = 750): the same dark "
         "boulders, but about 80% of the size and rounder, like big river pebbles with two facet lines; a small moss tuft on "
         "top; around the lower end ONE single thin brown root ring instead of the double twisted bracelet.",
         "- HANDS (the left one centred at about x = 540, y = 930; the right one at about x = 1010, y = 900): a small dark rock "
         "block with FOUR small round finger stones, about 80% of the size of image 1, close under each forearm.",
         "- SMALL FLOATING STONES: only FOUR instead of seven: two between the left shoulder plate and the left forearm (at "
         "about x = 453, y = 552 and x = 383, y = 609) and two between the right shoulder plate and the right forearm (at about "
         "x = 1063, y = 570 and x = 1161, y = 597), small round pebbles, no moss on them.",
         "- Exactly: one head with one sprout, one orb, one upright ring, one lower hoop with two roots, one closed seed, one "
         "buckle, one big shard and two splinters, two shoulder plates, two forearms each with one root ring, two hands with "
         "four finger stones each, four small floating stones.", "",
         "COLOURS: exactly the colours of image 1 (pale weathered statue stone, darker inner stone, dark grey-brown forest "
         "rock, moss green, deeper leaf green, warm brown roots, bright jade-green seed with darker-green spiral, dark-brown "
         "ink). Less moss than image 1: the stone looks cleaner and younger.", "",
         "CANVAS AND FRAMING: landscape 1536x1024, pure-white background, no ground line. Everything is visible, nothing cut by "
         "the edges. Every piece is one closed shape with its own closed ink outline; the floating pieces keep clear white "
         "gaps between them. No dust, no sparkles, no glow, no motion lines, no props.", "",
         LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = [f"# Gói gửi GPT: `{CODE}` dạng 1 (Mầm Đá: bản non của Gạc Đá, tướng thứ 3 đảo Mộc)", "",
          "Làm 2026-11-12. Người dùng: \"làm 2 dạng thôi, con vừa rồi là dạng 2, lát nữa bạn làm dạng 1\"; không tả dạng 1 nên thiết kế là "
          "đề xuất của Claude (đầu to tròn hơn, chưa mọc gạc mà chỉ có một mầm hai lá, hạt mầm chưa nảy, vai và tay nhỏ, ít rêu, không "
          "dây leo, bốn viên đá nhỏ), chờ duyệt concept. Cùng rig, cùng clip với dạng 2 nên mỗi mảnh phải nằm quanh đúng chỗ của dạng 2. "
          "Ghi chú: `ArtGen/Spine/inbox/tuong_da_ghichu.md`.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
          "Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tuong_da_1/luot_1_concept.txt` (thêm `--note \"...\"` để sửa nhanh).",
          "", "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(d2)}` | Concept dạng 2 đã duyệt (1536 × 1024, nền trắng): tượng đá lơ lửng phủ rêu, đầu trụ đá có hai nhánh gạc, lõi hạt "
          "mầm lục đã nảy mầm trong hai vòng ngực, hai tấm vai có dây leo, hai tảng cẳng tay quấn rễ, bàn tay đá, bảy viên đá nhỏ. Lấy nét, "
          "màu, kiểu dáng và CHỖ ĐẶT từng mảnh |", "",
          "## Kiểm", "",
          "- Cùng con với dạng 2 nhưng non hơn: đầu tròn to hơn, **không gạc**, một mầm hai lá; hạt mầm **chưa nảy**; vai, tay nhỏ lại; ít "
          "rêu, không dây leo; chỉ bốn viên đá nhỏ.",
          "- Mỗi mảnh nằm quanh đúng chỗ của mảnh tương ứng ở dạng 2 (chồng hai ảnh lên nhau thì tâm các mảnh trùng); khe trắng rộng hơn.",
          "- Không mặt, không chân; mỗi mảnh viền mực kín; tô phẳng, không bóng, lõi không phát sáng; nền trắng tinh.", "",
          "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|",
          "| Vẫn có gạc cây | `No antlers and no branches on the head: only ONE small sprout with two round leaves.` |",
          "| Các mảnh dời chỗ, bố cục khác dạng 2 | `Every piece must be centred at the same place as the matching piece of image 1; only the sizes change.` |",
          "| Hạt mầm đã nảy mầm | `The seed is still closed: remove the sprout from the seed.` |",
          "| Có bóng, sáng tối | `Flat colour only: remove every shadow, highlight and gradient.` |",
          "| Thêm mắt, mặt | `It has NO face: remove the eyes and mouth.` |"]
    open(os.path.join(pk(1), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    print(p)


if __name__ == "__main__":
    if K == 2:
        main()
        if os.path.exists(os.path.join(save_dir(), "L1_gac.png")):
            build_sua()
        if os.path.exists(os.path.join(save_dir(), "L1_duyet.png")):
            build_manh()
    if os.path.exists(os.path.join(save_dir(2), "L1_duyet.png")):
        build_dang1()
    if K == 1 and os.path.exists(os.path.join(save_dir(1), "L1_duyet.png")):
        build_manh()
