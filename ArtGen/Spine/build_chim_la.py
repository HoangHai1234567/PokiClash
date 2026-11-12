# -*- coding: utf-8 -*-
"""Gói GPT vẽ chim bảo hộ rừng cánh lá (mã làm việc chim_la, con gốc của rig: monster_3630). Tướng thứ 6 đảo Mộc.

Người dùng (2026-11-12): "concept Chim bảo hộ rừng, reskin lại phần cánh thành lá cây, đuôi vẫn có thể để là đá, làm khác con gốc
đi". Không dặn màu, kiểu mào: ba hướng dưới đây là ĐỀ XUẤT của Claude, chờ người dùng chọn.
Giữ cách dựng hình của con gốc (chim săn mồi lơ lửng nhìn sang phải, lộ một mắt, hai cánh xoè, hai chân vuốt giơ trước, sáu lông đuôi
dài rủ, bốn chuỗi đá); hình là của mình: cánh = cành cây + tán lá + từng chiếc lá, mào đổi hẳn dáng, vòng cổ lá, bùa đá.
Không đính ảnh con gốc; đính sơ đồ bố cục tự dựng bằng mã (chim_la.py bo_cuc).

    py -3 -I ArtGen/Spine/chim_la.py bo_cuc
    py -3 -I ArtGen/Spine/build_chim_la.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/chim_la_1/luot_1_concept_<hướng>.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "chim_la"
K = 1
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
    "nau": dict(
        ten="A · đại bàng rừng: lông nâu vỏ cây, ngực kem, cánh lá lục, mào quạt lá",
        vai="a FOREST EAGLE the colour of bark and leaves",
        long="warm bark brown (#9A6B42)", long_dam="dark brown (#5E4028)", bung="cream (#F1E3BC)",
        dau="dark brown (#5E4028)", ma="cream (#F1E3BC)",
        la="fresh forest green (#5FA646)", la_nhat="light spring green (#9CCB58)", gan="dark green (#2F6B34)",
        tan="deep green (#3B7F43)", choi="pale yellow-green (#C4DE6E)", canh="brown branch wood (#7A5232)",
        da="grey stone (#8C8A7E)", da_dam="dark grey stone (#5C5A52)", reu="moss green (#6FAE4B)",
        mo="amber yellow (#EDAE3C)", chan="ochre yellow (#D9A23E)", vuot="near-black brown (#3A322C)",
        mat="golden yellow (#F4C23C)", ngoc="amber (#F2B43E)", mao="quat", hoa=False,
        cam="NO blue, NO purple, NO pink, NO teal"),
    "ngoc": dict(
        ten="B · chim ngọc rừng mưa: lông lục lam, ngực đỏ, lá vàng chanh, mào hai tàu dương xỉ",
        vai="a RAINFOREST SPIRIT BIRD with jade-teal plumage and a red breast",
        long="jade teal (#1F8C7C)", long_dam="deep teal (#135E58)", bung="warm crimson red (#C9463A)",
        dau="deep teal (#135E58)", ma="jade teal (#1F8C7C)",
        la="bright leaf green (#6DBB4A)", la_nhat="lime yellow-green (#C2E062)", gan="dark green (#2C7A3C)",
        tan="mid green (#3E9A4E)", choi="pale lime (#E2EC84)", canh="dark brown branch wood (#5A3F2C)",
        da="blue-grey basalt stone (#6A6C72)", da_dam="dark basalt (#44464C)", reu="moss green (#7DBB52)",
        mo="golden yellow (#F2C83E)", chan="dark warm grey (#55504C)", vuot="cream (#F1E3BC)",
        mat="golden yellow (#F4D03C)", ngoc="crimson red (#C9463A)", mao="duong_xi", hoa=False,
        cam="NO purple, NO pink, NO pure blue, NO white plumage"),
    "bach": dict(
        ten="C · linh điểu trắng: lông trắng kem, mũ lục xám, cánh lá lục sẫm, cành cánh nở hoa hồng, mào quạt lá",
        vai="a WHITE FOREST SPIRIT BIRD whose wing branches are in blossom",
        long="warm cream white (#F4EFDC)", long_dam="soft sage green (#7E9E7A)", bung="warm cream white (#F4EFDC)",
        dau="soft sage green (#7E9E7A)", ma="warm cream white (#F4EFDC)",
        la="deep leaf green (#4C9A52)", la_nhat="light green (#93C663)", gan="dark green (#2A6A3A)",
        tan="dark forest green (#2F7646)", choi="light green (#93C663)", canh="brown branch wood (#7A5638)",
        da="warm grey stone (#9A968A)", da_dam="darker grey stone (#66625A)", reu="moss green (#6FAE4B)",
        mo="orange (#EE8A3E)", chan="orange (#EE8A3E)", vuot="dark brown (#4A3A30)",
        mat="orange (#EE8A3E)", ngoc="rose pink (#EE86A6)", mao="quat", hoa=True,
        cam="NO blue, NO purple, NO teal; pink ONLY on the small blossoms and the amulet gem"),
}


def crest(M):
    if M["mao"] == "quat":
        return ("- CREST (this is the creature's signature silhouette): a raised FAN OF FIVE BIG LEAVES, like a cockatoo's or a "
                "hoopoe's crest made of foliage. All five are rooted close together on the crown (about x = 750 to x = 835, "
                "y = 298), stand up behind the head and fan out backward and upward: tips at about (596, 262), (618, 176), "
                "(690, 92) (the tallest: about 230 px long and 65 px wide), (790, 118), and one small front leaf with its tip at "
                f"about (862, 206). Each is a broad, lance-shaped leaf with ONE centre vein of {M['gan']}; they alternate "
                f"{M['la']} and {M['la_nhat']}. Across the forehead, where the leaves are rooted, sits a narrow carved WOODEN "
                f"CIRCLET of {M['canh']} (a plain band about 120 px long and 14 px thick, from about x = 728 to x = 852, "
                "y = 290 to y = 312). No long thin curled plumes, no antennae, no crystals on the head.")
    return ("- CREST (this is the creature's signature silhouette): TWO LONG FERN FRONDS rising from the crown. Each is a thin "
            f"stem of {M['canh']} lined on BOTH sides with pairs of small pointed leaflets that get shorter toward the tip "
            f"(the longest, near the base, about 45 px; alternating {M['la']} and {M['la_nhat']}), so each frond reads as one "
            "long feather-shaped leaf about 85 px wide at its base tapering to a point. The longer frond starts at about "
            "(792, 296), leans back to the left and then rises to its tip at about (668, 98); the shorter one starts at about "
            "(832, 298) and rises to about (756, 132). Behind them, three short plain pointed leaves sweep back from the nape "
            f"(tips at about (640, 250), (690, 214) and (628, 292)) in {M['la']}. Across the forehead, where the fronds are "
            f"rooted, sits a narrow carved WOODEN CIRCLET of {M['canh']} (a plain band from about x = 728 to x = 852, y = 290 "
            "to y = 312). No smooth ribbon-like plumes, no crystals on the head.")


def body(kieu):
    M = MAU[kieu]
    face = (f"the FACE is a patch of {M['ma']} from the brow down over the cheek to the throat, with a ragged feathered lower "
            "edge" if M["ma"] != M["dau"] and kieu != "ngoc" else
            f"the FACE (brow, cheek, throat) is {M['ma']}, a little lighter than the hood, with a ragged feathered lower edge")
    hoa = (" On each wing's branch grow three or four small five-petal BLOSSOMS of soft pink (#F2A6BC) with an orange centre "
           "(each about 26 px), like a cherry branch in bloom." if M["hoa"] else "")
    return "\n".join([
        f"CREATURE: a FOREST GUARDIAN BIRD, a plant-element monster for a monster-collecting game: {M['vai']}, a big bird of "
        "prey whose WINGS ARE MADE OF LEAVES AND BRANCHES instead of feathers, and that carries chains of floating mossy "
        "STONES in its long tail. It hovers in the air with both wings spread and both taloned feet raised in front of it. "
        "Character: the proud, stern protector of the forest, battle-ready, glaring at an enemy to the right; appealing and "
        "noble, not scary, not a smiling cute mascot. Bold, clear, readable shapes.",
        "Follow the LAYOUT GUIDE (image 1) for WHERE every part is on the canvas, HOW BIG it is and WHICH part overlaps which. "
        "The outlines in the guide are only rough computer blobs: design the real outline of every part yourself as described "
        "below, but keep every part in its place and at its size.",
        "- VIEW: the bird faces the viewer's RIGHT, body seen in three-quarter view, upright and leaning slightly forward; the "
        "head is in PROFILE turned to the right, so only ONE eye is visible. It floats: no ground.",
        "- HEAD (about x = 636 to x = 868, y = 276 to y = 385; about 230 px wide, 105 px tall; small compared with the wings): "
        "an eagle's head. A rounded skull; the back of the head ends in three short pointed feather tips sweeping back to the "
        f"left. A HOOD of {M['dau']} covers the top and the back of the head down to the nape; {face}. ONE eye only, at about "
        f"(826, 333): a fierce, slanted almond eye of {M['mat']} with a round dark pupil and one tiny white dot, under a heavy "
        "dark brow stroke that slants DOWN toward the beak (a stern, determined glare). No second eye.",
        f"- BEAK (about x = 836 to x = 882, y = 342 to y = 382): a strong, short, sharply HOOKED raptor beak of {M['mo']}, the "
        "tip pointing down and to the right; closed, with one clean mouth line between the upper and lower beak.",
        crest(M),
        f"- NECK AND CHEST (about x = 554 to x = 808, y = 310 to y = 522): a thick feathered neck and a deep chest of "
        f"{M['long']}; the FRONT (the right side: throat and breast) is a big BIB of {M['bung']} with a soft zigzag feather "
        "edge. A tuft of three pointed feathers sticks out behind the neck at the left.",
        f"- LEAF COLLAR (about x = 611 to x = 827, y = 342 to y = 556): around the base of the neck, over the breast and the "
        f"near shoulder, a RUFF of eight to ten broad pointed LEAVES of {M['la_nhat']} (each about 60-110 px long, one centre "
        f"vein of {M['gan']}), overlapping like roof tiles, their tips pointing outward and up, the lower edge a row of leaf "
        "tips. Leaves, not crystals, not fur.",
        f"- STONE AMULET on the collar: in the middle of the breast, at about (775, 515), a carved STONE pendant of "
        f"{M['da']}: a chunky rounded-diamond plate about 60 px tall with one small diamond-shaped gem of {M['ngoc']} set in "
        "its centre and a stone RING (about 40 px) hanging under it (down to about y = 575). Two hook-shaped stone clasps of "
        "the same stone hold the collar: one at the left (about x = 675 to x = 760, y = 442 to y = 510), one small at the "
        "right edge of the collar (about x = 805 to x = 827, y = 465 to y = 520).",
        f"- LOWER BODY (about x = 524 to x = 773, y = 417 to y = 640): a round feathered belly of {M['long']} with a few "
        f"scalloped feather lines; on its right side, just under the collar (about x = 615 to x = 695, y = 478 to y = 534), "
        f"one small patch of {M['reu']} moss with a bumpy edge.",
        "- WINGS: two big wings spread wide and slightly raised. The NEAR wing is at the viewer's LEFT (about x = 151 to "
        "x = 637, y = 172 to y = 680), in front of the body, its tip pointing left and DOWN; the FAR wing is at the viewer's "
        "RIGHT (about x = 778 to x = 1384, y = 175 to y = 538), behind the head and the body, its tip pointing right and "
        "slightly down. Each wing is built of four clearly separate things:",
        f"  (a) the WING ARM is a gnarled BRANCH of {M['canh']} running along the top (leading) edge of the wing from the "
        "shoulder out to the wrist, about 30-40 px thick, with three or four short hooked side-twigs that curl down over the "
        f"canopy like tendrils (thick, chunky, blunt; bare wood, a few grain lines).{hoa}",
        f"  (b) under the branch, the inner two thirds of the wing are a CANOPY of {M['tan']}: one broad mass of small "
        "overlapping rounded leaves, drawn as two or three scalloped rows like the crown of a tree (it replaces a bird's "
        "covert feathers); its outer edge is a line of small leaf tips.",
        f"  (c) the FLIGHT FEATHERS ARE LEAVES: a row of about twelve LONG pointed leaves of {M['la']} grows from the lower and "
        "outer edge of the canopy and fans out toward the wing tip, overlapping like real primaries (the longest, at the wing "
        "tip, about 230 px long and 45 px wide; shorter toward the body). Each one is a single simple lance-shaped LEAF with "
        f"ONE centre vein of {M['gan']} and a pointed tip. A second row of about ten SHORT leaves of {M['la_nhat']} (each "
        "about 50-70 px, with a centre vein) lies over the roots of the long ones along the lower edge of the canopy.",
        f"  (d) at the wrist (the top outer corner of the canopy: about (350, 205) on the near wing, about (1085, 225) on the "
        f"far wing) one small curled SPROUT of two or three young leaves of {M['choi']}, about 90 px.",
        f"- LEGS: an eagle's legs. THIGHS: two short thick 'trousers' of {M['long_dam']} feathers under the belly. Lower legs "
        f"and toes: scaly bird skin of {M['chan']} (a few scale lines), each foot with FOUR toes ending in a big curved CLAW "
        f"of {M['vuot']} (each claw about 50-70 px). The NEAR leg hangs straight down in front of the tail (about x = 561 to "
        "x = 709, y = 566 to y = 758), its talons spread open, claws pointing down. The FAR leg is stretched forward to the "
        "right (about x = 731 to x = 981, y = 565 to y = 684), its foot at the right end with the talons half closed, claws "
        "curving down, ready to grab.",
        f"- TAIL PLUMES (about x = 368 to x = 951, y = 537 to y = 891): SIX big, long, soft plume feathers hang down from the "
        "hips and fan out like a long ragged skirt: four hang down and to the left, two sweep down and to the right under the "
        f"far leg. Each is one broad curved plume about 250-330 px long with a slightly ragged pointed tip and two or three "
        f"thin feather lines; they alternate {M['long']} and {M['long_dam']}.",
        f"- FOUR CHAINS OF FLOATING STONES hang among the plumes like strings of beads (the stones do not touch each other, "
        f"small gaps between them): each chain is a line of four to six small, chunky, angular stones of {M['da_dam']} (each "
        f"about 25-50 px) and ends in ONE bigger pointed boulder of {M['da']} (about 100-140 px long) whose outer half is "
        f"capped with {M['reu']} moss and carries one tiny two-leaf sprout. Chain 1 runs down the left side (about x = 392 to "
        "x = 539, y = 593 to y = 826); chain 2 down the middle to the bottom (about x = 525 to x = 691, y = 610 to y = 919); "
        "chain 3 down and to the right (about x = 593 to x = 883, y = 610 to y = 891); chain 4 trails out sideways to the "
        "right under the far leg, its end boulder floating free at about x = 955 to x = 1092, y = 665 to y = 760. Plain "
        "faceted rock: no crystals, no glow.",
        "- Exactly: one head with one visible eye and a hooked beak, one crest, one leaf collar with one stone amulet, two "
        "leaf wings (each: one branch arm, one canopy, a row of long leaves, a row of short leaves, one sprout), two taloned "
        "legs, six tail plumes, four stone chains.",
        "",
        f"COLOURS, a calm, slightly muted palette (use exactly these, each area one flat colour): body plumage {M['long']}; "
        f"hood, thighs and every second tail plume {M['long_dam']}; bib {M['bung']}; face {M['ma']}; long wing leaves "
        f"{M['la']}; short wing leaves and the collar leaves {M['la_nhat']}; leaf veins {M['gan']}; wing canopy {M['tan']}; "
        f"wrist sprouts {M['choi']}; wing branches and the head circlet {M['canh']}; amulet, clasps and end boulders "
        f"{M['da']}; small chain stones {M['da_dam']}; moss {M['reu']}; beak {M['mo']}; legs and toes {M['chan']}; claws "
        f"{M['vuot']}; eye {M['mat']}; amulet gem {M['ngoc']}; every outline dark-brown ink (#2B2118). Only these colours. "
        f"{M['cam']}.",
    ])


FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the whole creature is about 1235 px wide (from the near wing tip at about "
         "x = 151 to the far wing tip at about x = 1384) and about 830 px tall (from the crest tip at about y = 92 to the lowest "
         "stone at about y = 919).")

POSE = ("POSE (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): hovering, wings "
        "spread, in a clean readable pose exactly as in the guide. Every part listed above is a clear shape with its own ink "
        "outline: each long wing leaf, each crest leaf, each collar leaf, each tail plume, each stone, each toe and claw. The "
        "wings do not cover the head; the two legs do not cross. No falling leaves, no dust, no sparkles, no glow, no motion "
        "lines, no wind lines, no ground, no perch, no props.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram with rough, jagged edges: take only the placement, the sizes, the overlaps and "
        "the colour of each kind of part from it, never its line, its jagged edge noise or its exact blobs. Draw the leaves as "
        "simple bold leaf shapes, the branches as smooth chunky wood, the stones as clean chunky faceted rocks, the plumage as "
        "broad simple feather masses.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 6 px thick on this canvas around every big part (head, neck and body, "
        "wing canopies, wing branches, long wing leaves, crest, collar, legs, tail plumes, big stones), and about 4 px for small "
        "parts (short leaves, sprouts, toes, claws, small stones, the amulet, the eye, the beak line); leaf veins, feather "
        "lines, wood grain and rock facet lines are thin darker pencil lines about 3 px, not ink; every area coloured with "
        "coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the outline), "
        "kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed: no realistic feather "
        "barbs, no bark cracks all over, no tiny leaves everywhere.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker underside, no lighter patches or blotches, no shadows of any kind (no cast "
        "shadow of one part on another, no shadow under the figure or on the background), no white highlights or shine spots "
        "(except the one tiny dot in the eye), no gloss, no glow, no rim light, no gradients, no 3D look. A different tone "
        "appears only where the design itself lists a different colour.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the creature.")


def refs(kieu):
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature showing where every part "
         "goes on the canvas, how big it is and which part overlaps which (the bird hovers facing right; the two big green "
         "fans are the leaf wings: brown hooked bands = the branch wing arms, dark green mass = the leaf canopy, the many "
         "pointed green shapes with a centre line = the individual wing leaves, pale curls at the top corners = the sprouts; "
         "the leaf shapes on top of the head = the crest; the pale leafy mass on the breast with grey shapes = the leaf collar "
         "and the stone amulet; yellow / dark shapes in the middle = the two legs and their claws; the big hanging shapes at "
         "the bottom = the six tail plumes; grey shapes among them = the four stone chains, the half-green ones = the mossy "
         "end boulders). Use it for placement, size and overlap only; redraw everything in the hand-drawn style of the "
         "approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): chim lơ lửng nhìn sang phải, hai cánh xoè, tô phẳng theo nhóm màu "
         "(dải nâu có móc: cành cây làm xương cánh; mảng lục sẫm: tán lá; các hình nhọn có gân giữa: từng chiếc lá cánh; túm nhạt ở "
         "góc trên cánh: chồi non; lá trên đỉnh đầu: mào; mảng lá nhạt + hình xám ở ngực: vòng cổ lá và bùa đá; vàng / sẫm ở giữa: "
         "hai chân và vuốt; các mảng lớn rủ phía dưới: sáu lông đuôi; hình xám xen giữa: bốn chuỗi đá, viên nửa lục là tảng cuối phủ "
         "rêu). Chỉ lấy chỗ đặt, cỡ, thứ tự chồng"),
        (DEER,
         "an approved hero of the same game and the same island (a wooden stag-giraffe with a leaf mane), 1536x1024, white "
         "background: match EXACTLY its wobbly dark-brown pen line, its visible crayon hatching, its completely flat colouring "
         "and its bold level of detail; see how its LEAVES (shape, one centre vein), its wood and its stones are drawn. Do NOT "
         "copy its species, its design or its colours.",
         "Hươu gỗ cổ dài đã duyệt (1536 × 1024, nền trắng): thân gỗ bạch dương đốm nâu, bờm lá phong đỏ cam, pha lê lục trên lưng. "
         "Lấy nét bút rung, vân sáp, tô phẳng, cách vẽ lá, gỗ, đá"),
        (STONE,
         "another approved hero of the same island (a floating stone guardian with moss and wooden antlers), 1536x1024, white "
         "background: the same line and flat crayon colouring; see how its chunky faceted STONES, its moss and its wooden "
         "branches are drawn. Do NOT copy its design or its colours.",
         "Tượng đá giữ rừng đã duyệt (1536 × 1024, nền trắng): các khối đá lơ lửng phủ rêu, đầu trụ đá có hai nhánh gạc. Lấy nét, tô "
         "phẳng, cách vẽ đá tảng, rêu, cành cây"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching) and the way its trees, leaves and rocks are simplified, nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp, cách giản lược cây, lá, đá"),
    ]


CHECK = [
    "Chim **lơ lửng nhìn sang phải**, đầu nghiêng **lộ một mắt** xếch dữ, mỏ quặp ngậm; không cười, không đáng sợ.",
    "**Cánh là lá**: mỗi cánh có cành cây nâu làm xương cánh (vài nhánh móc), tán lá sẫm, một hàng lá dài nhọn có gân giữa, một hàng lá "
    "ngắn nhạt, một chồi non ở góc trên. Không còn lông vũ hay pha lê trên cánh.",
    "**Mào đổi hẳn dáng**: hướng A, C là quạt năm chiếc lá to; hướng B là hai tàu dương xỉ dài + ba lá ngắn sau gáy; có vòng gỗ ở trán.",
    "Vòng cổ lá + bùa đá có viên ngọc nhỏ và vòng đá treo; mảng rêu nhỏ trên bụng.",
    "Hai chân vuốt (chân gần buông xuống, chân xa vươn sang phải), sáu lông đuôi dài rủ, **bốn chuỗi đá** (đá nhỏ rời nhau, tảng cuối "
    "phủ rêu có mầm lá); chuỗi thứ tư vắt ngang sang phải.",
    "Hướng A: nâu vỏ cây, ngực kem, lá lục. Hướng B: lục lam, ngực đỏ, lá vàng chanh, đá bazan. Hướng C: trắng kem, mũ lục xám, "
    "cành cánh có hoa hồng nhỏ, mỏ chân cam.",
    "Tô phẳng: **không** bóng, không mảng sáng tối, không phát sáng, không điểm sáng trắng (trừ một chấm trong mắt); nền trắng tinh; "
    "không lá rơi; cả con không bị cắt mép.",
]

FIX = [
    ("Hai mắt, mặt quay chính diện", "Only ONE eye is visible: the head is in profile turned to the viewer's right as in image 1; "
                                     "remove the second eye."),
    ("Cánh vẫn là lông vũ", "The wings have NO feathers: the flight feathers are individual pointed LEAVES with one centre vein, "
                            "the inner wing is a canopy of small leaves, the wing arm is a bare brown branch."),
    ("Mào là lông dài cong", "Replace the crest: no thin curled plumes; draw the leaf crest exactly as described under CREST."),
    ("Có bóng, mảng sáng tối, phát sáng", "Flat colour only: remove every shadow, highlight, gradient and glow; each area one even "
                                          "colour; keep the crayon hatching as texture only."),
    ("Đá có pha lê / phát sáng", "The stones are plain grey faceted rock with moss; no crystals, no glow."),
    ("Mặt hiền, cười", "Make the face stern and battle-ready: slanted eye under a heavy brow slanting down to the beak, beak "
                       "closed, no smile."),
    ("Bố cục khác sơ đồ", "Follow image 1 exactly for the place and size of every part; the creature faces the viewer's right."),
    ("Quá nhiều chi tiết vụn", "Simplify: bold simple leaves, broad feather masses, chunky stones; remove tiny leaves and "
                               "texture lines."),
]


def main():
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    gd = [f"# Gói gửi GPT: `{CODE}` (chim bảo hộ rừng cánh lá, tướng thứ 6 đảo Mộc, tên chưa đặt)", "",
          "Làm 2026-11-12: dựng trên rig của con gốc `monster_3630`; màu, kiểu mào và chi tiết là đề xuất của Claude, chờ người dùng "
          "chọn hướng và duyệt concept. Ghi chú: `ArtGen/Spine/inbox/chim_la_ghichu.md`.", "",
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
    gd += ["Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/chim_la.py bo_cuc`).",
           "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    open(os.path.join(pk(), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ================================================================ LƯỢT 2: mảnh theo khung part (hướng C đã duyệt 2026-11-12)
import json  # noqa: E402

CON = ("a white forest guardian bird (an eagle-like spirit bird): cream-white plumage, a sage-green feather hood, an orange hooked "
       "beak and orange scaly legs with dark claws; its WINGS are made of plants (a brown branch as the wing arm with small pink "
       "blossoms, a dark-green canopy of small leaves, rows of long and short green leaves as flight feathers); a fan of five big "
       "leaves as a crest with a wooden circlet; a collar of light-green leaves with a grey stone amulet; six long tail plumes "
       "(cream and sage) and four chains of grey stones ending in mossy boulders with tiny sprouts")
C = dict(la="#4C9A52", la_nhat="#93C663", gan="#2A6A3A", tan="#2F7646", gan_tan="#1F5634", canh="#7A5638", long="#F4EFDC", sage="#7E9E7A",
         da="#9A968A", da_dam="#66625A", reu="#6FAE4B", cam="#EE8A3E", vuot="#4A3A30", ngoc="#EE86A6", hoa="#F2A6BC")

# mô tả từng ô (theo tên vùng, bỏ 'P_'); ô không có ở đây lấy mô tả chung của nhóm
O = {
    "tou_01": "the bird's HEAD in profile, facing RIGHT, drawn WITHOUT its beak and WITHOUT its crest (those are separate parts): a "
              "rounded skull whose back (the left end) breaks into three or four pointed feather tips. A sage-green HOOD "
              f"({C['sage']}) covers the crown and the whole back of the head; the FACE (front, cheek and throat) is cream "
              f"({C['long']}); the border between them is a soft zigzag feather edge drawn as a thin ink line. ONE fierce, slanted "
              f"almond EYE exactly where image 2 has it: orange iris ({C['cam']}), round dark pupil, one tiny white dot, a clean ink "
              "rim, and above it a heavy dark BROW stroke slanting DOWN toward the front (right): a stern glare. The right end of "
              "the head, where the beak will be attached, is plain rounded cream. Same face as on image 1",
    "zui_01": f"the UPPER BEAK: a strong hooked raptor mandible, orange ({C['cam']}), one thin darker-orange line near its upper edge",
    "zui_02": f"the LOWER BEAK: a small pointed lower mandible, orange ({C['cam']})",
    "mao_01": f"a TUFT of three pointed cream ({C['long']}) feathers (it sits behind the neck), with two or three thin feather lines",
    "xiongjia_05": f"the big LEAF COLLAR (a ruff): light-green ({C['la_nhat']}) broad pointed LEAVES overlapping like roof tiles and "
                   "radiating outward; every spike of the silhouette is one leaf tip; each leaf has one thin centre vein "
                   f"({C['gan']}) and thin ink lines separate the overlapping leaves",
    "xiongjia_06": f"a small cluster of four or five of the same light-green ({C['la_nhat']}) pointed leaves, overlapping, each with a "
                   "centre vein",
    "xiongjia_07": f"two tiny light-green ({C['la_nhat']}) leaf tips, one above the other",
    "xiongjia_02": f"the STONE AMULET: a chunky carved plate of grey stone ({C['da']}) with ONE small diamond-shaped rose-pink gem "
                   f"({C['ngoc']}) in its middle (thin ink rim around the gem, no glow) and two or three thin facet lines",
    "xiongjia_01": f"a hook-shaped CLASP of grey stone ({C['da']}), chunky, with two thin facet lines",
    "xiongjia_03": f"a small hook of grey stone ({C['da']})",
    "xiongjia_04": f"a RING of grey stone ({C['da']}); keep its hole (the hole stays pure white)",
    "datuiR_01": f"a feathered THIGH (a bird's 'trouser'): a soft mass of sage-green ({C['sage']}) feathers, a few scalloped feather "
                 "lines, the narrow lower end ragged with two or three feather tips",
    "datuiL_01": f"the other feathered THIGH, sage green ({C['sage']}), with a few scalloped feather lines and small feather tips at "
                 "its narrow end",
    "mao_1": "CREST LEAF 1", "mao_2": "CREST LEAF 2", "mao_3": "CREST LEAF 3 (the biggest)", "mao_4": "CREST LEAF 4", "mao_5": "CREST LEAF 5 (the smallest)",
    "vong": f"the wooden CIRCLET of the crest: a slightly curved band of brown wood ({C['canh']}) with rounded ends and two or three "
            "thin grain lines along it",
    "mam": f"a tiny SPROUT: a short green stem ({C['reu']}) with two rounded young leaves ({C['la_nhat']}), each with a centre vein",
    "hoa": f"a small five-petal BLOSSOM seen from the front: soft pink ({C['hoa']}) rounded petals, an orange ({C['cam']}) centre",
}
NHOM = {
    "la_gan": ("WING LEAVES. Every shape is ONE LEAF of the bird's wing (its flight feathers are leaves): a simple lance-shaped leaf, "
               f"pointed at both ends as in image 2. Dark shapes are {C['la']}, light shapes are {C['la_nhat']} (keep which is "
               f"which). Each leaf has ONE centre vein (a thin {C['gan']} pencil line where image 2 shows the line) and, on the big "
               "leaves only, three to five pairs of short faint side veins. Nothing else on them", "lá cánh gần"),
    "tan": (f"WING CANOPY. Every shape is one piece of the wing's leaf canopy, dark forest green ({C['tan']}): a dense mass of small "
            f"overlapping rounded leaves, drawn as rows of scallops (thin {C['gan_tan']} pencil lines, about as big and as dense as "
            "the scallops of image 2, a little irregular), like the crown of a tree or roof tiles. Where the silhouette is jagged, "
            "the points are leaf tips. No big veins, no branches", "tán lá"),
    "canh": (f"WING BRANCHES AND SPROUTS. The brown shapes are pieces of the gnarled BRANCH that is the wing's arm ({C['canh']}): "
             "smooth chunky bare wood, slightly curved, tapering to blunt rounded ends, with two or three thin darker grain lines "
             "running along each piece; some pieces have one or two short blunt side twigs, exactly as the silhouettes show. No "
             "leaves, no flowers, no moss on the branches. The two light-green curly "
             f"shapes are SPROUTS ({C['la_nhat']}): a curl of two or three young leaves that follows the curly silhouette, each "
             f"leaf with a thin centre vein ({C['gan']})", "cành cánh + chồi"),
    "duoi": (f"TAIL PLUMES. Every shape is ONE big soft tail plume feather, cream ({C['long']}) or sage green ({C['sage']}) as in "
             "image 2 (keep which is which): a broad curved plume with three or four thin feather lines along its length (about "
             "where image 2 has faint lines) and a slightly ragged tip. No stones, no leaves on them", "lông đuôi"),
    "da": (f"TAIL STONES. Dark-grey shapes ({C['da_dam']}): small chunky angular STONES; a cell that holds two or three separate "
           "small stones keeps them separate, each with its own closed outline. Lighter-grey shapes "
           f"({C['da']}) with a green top: bigger BOULDERS capped with MOSS ({C['reu']}) exactly on the part image 2 shows green; "
           "the lower edge of the moss is bumpy and scalloped, drawn as a thin ink line. Every stone has two or three thin facet "
           "lines (darker grey pencil). Plain rock: no crystals, no sprouts, no glow", "đá đuôi"),
    "chan": (f"LEGS, TOES AND CLAWS. Orange shapes ({C['cam']}): pieces of the bird's scaly legs and toes (shank, foot pad, toe "
             "segments): smooth bird skin with two to four thin curved scale lines (darker orange pencil) across each piece. "
             f"Dark-brown pointed shapes ({C['vuot']}): CLAWS, smooth and sharp, with one thin line along the curve. No shine "
             "spots", "chân, ngón, vuốt"),
    "dau": ("HEAD, BEAK, COLLAR, AMULET, THIGHS. Each shape is described below by its position on the sheet", "đầu, mỏ, vòng cổ lá, bùa đá, đùi"),
    "X": ("CREST AND SMALL EXTRAS. The five tall shapes are the five LEAVES OF THE CREST, each drawn upright: the flat cut end at "
          "the bottom is the root (it will be hidden behind the head), the pointed end at the top is the tip; a broad lance-shaped "
          f"leaf, {C['la']} or {C['la_nhat']} as in image 2, with ONE centre vein ({C['gan']}) and four to six pairs of faint side "
          "veins", "năm lá mào, vòng gỗ, mầm, hoa"),
}
NHOM["la_xa"] = (NHOM["la_gan"][0], "lá cánh xa")
NHOM["la_lat"] = (NHOM["la_gan"][0], "lá mặt kia của cánh gần")
NHOM["tan_lat"] = (NHOM["tan"][0].replace("WING CANOPY. Every shape is", "WING CANOPY AND BRANCH. The two big green shapes are each")
                   + f". The two brown shapes are pieces of the wing's BRANCH ({C['canh']}): smooth chunky bare wood with two or three "
                   "thin grain lines, blunt rounded ends and short blunt side twigs as the silhouettes show", "tán + cành mặt kia của cánh gần")

FLAT2 = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no "
         "darker side, no highlights, no shine spots, no gradients, no cast shadows, no glow. Pure white (#FFFFFF) background "
         "between the shapes; no text, no labels, no numbers, no frames, no guide lines.")


def _vi_tri(v):
    return f"at about x = {v['x'] + v['w'] // 2}, y = {v['y'] + v['h'] // 2} ({v['w']} x {v['h']} px)"


def build_part():
    muc = json.load(open(os.path.join(mau_dir(), "part_muc.json")))
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    if not os.path.exists(duyet):
        raise SystemExit("chưa có concept duyệt " + Wp(duyet))
    ra, gd = [], ["", "## Lượt 2: mảnh theo khung part (hướng C đã duyệt 2026-11-12)", "",
                  "Mỗi tờ hướng dẫn do `py -3 -I ArtGen/Spine/chim_la_manh.py to` dựng: mỗi part của rig một ô đúng khung ảnh vùng, trong "
                  "ô là hình bóng kín tô phẳng theo thiết kế. GPT vẽ lại sạch, GIỮ NGUYÊN hình bóng, chỗ, cỡ. Mỗi tờ một file prompt; "
                  "**chỉ gửi GPT đường dẫn file prompt**. Claude tự gen bằng `py -3 -I ArtGen/Spine/gen.py <file prompt>` rồi cắt bằng "
                  "`py -3 -I ArtGen/Spine/chim_la_manh.py cat <mã tờ>`.", "",
                  f"Ảnh mẫu 1 của mọi tờ: `{Wp(duyet)}` (concept đã duyệt, 1536 × 1024, nền trắng: chim trắng kem cánh lá, cành cánh nở "
                  "hoa hồng, mào quạt lá). Ảnh mẫu 2 là tờ hướng dẫn của tờ đó (1536 × 1024, nền trắng, các hình phẳng viền sẫm rời nhau).",
                  "", "| Tờ | File prompt | Tờ hướng dẫn (ảnh mẫu 2) trông như thế nào | Ảnh lưu vào |", "|---|---|---|---|"]
    for ma, g in muc.items():
        kh = json.load(open(os.path.join(mau_dir(), f"part_{ma}.json"), encoding="utf-8"))
        gdp = os.path.join(mau_dir(), f"part_{ma}.png")
        out = os.path.join(save_dir(), f"N_{ma}.png")
        p = os.path.join(pk(), f"luot_2_manh_{ma}.txt")
        z = max(v["z"] for v in kh.values())
        zmin = min(v["z"] for v in kh.values())
        to_, nho_ = (11, 8) if g == "X" else (round(4.0 * zmin), round(2.85 * zmin))
        mo_ta, vi = NHOM[g]
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(duyet)}: the APPROVED creature, 1536x1024, white background: {CON}. It gives the design, the colours, "
             "the wobbly dark-brown ink line, the crayon hatching and the look of every material.",
             f"image 2 = {Wp(gdp)}: PART GUIDE, 1536x1024, white background, drawn by computer: {len(kh)} separate flat shapes with "
             "dark outlines, each one a single part of this creature laid out apart from the others for a 2D animation rig. It gives "
             "the exact silhouette, size, orientation and place of every part and its flat colours.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as N_{ma}_2.png, N_{ma}_3.png ... in the same folder. Do not edit, move "
             "or delete any other file.", "",
             "TASK: redraw image 2 cleanly in the hand-drawn style of image 1, landscape 1536x1024, pure-white background. Keep "
             "EXACTLY every silhouette of image 2: the same outline, the same size, the same orientation, the same place on the "
             "sheet (if your picture were laid over image 2, every shape must coincide). A program will cut each shape out of its "
             "place and wrap it onto the animation mesh of that part, so do not add, remove, move, rotate, mirror, merge or resize "
             f"any shape, and draw nothing outside the shapes. There are exactly {len(kh)} shapes.", "",
             "WHAT THE SHAPES ARE: " + mo_ta + "."]
        rieng = [(k, v) for k, v in kh.items() if k.replace("P_", "") in O]
        if rieng:
            t += ["", "SHAPE BY SHAPE (positions are the centres of the shapes on the sheet):"]
            t += [f"- {_vi_tri(v)}: {O[k.replace('P_', '')]}." for k, v in sorted(rieng, key=lambda kv: (kv[1]["y"], kv[1]["x"]))]
        t += ["",
              f"OUTLINE: every shape has its own CLOSED dark-brown ink outline (#2B2118) all the way around, lying just INSIDE the "
              f"edge of the silhouette of image 2, about {to_} px thick on this sheet for the big shapes and about {nho_} px for the "
              "small ones, slightly wobbly like a real pen. The inner detail lines (veins, feather lines, grain, facets, scales) are "
              "thin darker pencil lines, much thinner than the outline, not ink.",
              "COLOUR: keep the flat colours of image 2 for every area; colour with coloured pencil and wax crayon, the strokes "
              "visible as loose diagonal hatching inside the outline, as on image 1.", "", FLAT2]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd.append(f"| `{ma}` | `{Wp(p)}` | `{Wp(gdp)}`: {len(kh)} hình ({vi}), phóng {zmin:g}–{z:g} lần ảnh vùng của rig | `{Wp(out)}` "
                  "(trùng tên thì `_2`, `_3`…) |")
    # tờ thân liền
    gdl = os.path.join(mau_dir(), "lien.png")
    outl = os.path.join(save_dir(), "N_L.png")
    pl = os.path.join(pk(), "luot_2_than_lien.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(duyet)}: the APPROVED creature, 1536x1024, white background: {CON}. It gives the colours, the ink line, the "
         "crayon hatching and the look of the cream plumage.",
         f"image 2 = {Wp(gdl)}: BODY GUIDE, 1536x1024, white background, drawn by computer: ONE big flat cream silhouette = the "
         "bird's feathered BODY alone (neck, chest and belly fused into one shape; the head would sit at the top right, the tail "
         "below), with one green oval = a patch of moss on the belly. It gives the exact silhouette, size and position.",
         "", f"SAVE: save it as a PNG to {Wp(outl)}",
         "If a file with that name already exists, save as N_L_2.png, N_L_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: redraw image 2 cleanly in the hand-drawn style of image 1, landscape 1536x1024, pure-white background. Keep EXACTLY "
         "the silhouette of image 2: the same outline, the same size, the same position (if your picture were laid over image 2, "
         "the shapes must coincide). A program will cut this sheet into the body parts of a 2D animation rig.", "",
         "VERY IMPORTANT, ONE CONTINUOUS SURFACE: the shape is ONE mass of cream-white plumage. Draw the dark-brown ink outline "
         "(#2B2118, about 15 px thick on this sheet, wobbly like a real pen) ONLY around the OUTSIDE of the silhouette, lying just "
         "inside its edge. INSIDE the silhouette draw NO ink lines at all: no line between neck and chest, none between chest and "
         "belly, no folds, no creases.", "",
         f"- PLUMAGE: warm cream white ({C['long']}) everywhere, with loose diagonal crayon hatching, and eight to twelve small, "
         "soft, scalloped feather marks (short thin curved pencil lines, slightly darker cream #CEC6AA, NOT ink) scattered evenly "
         "over the whole shape. Where the silhouette has small pointed bumps, they are feather tips.",
         f"- MOSS: one patch of moss ({C['reu']}) exactly where image 2 has the green oval, with a bumpy scalloped edge drawn as a "
         "thin ink line and two or three tiny darker dots.",
         "Draw nothing else: no head, no eye, no beak, no wings, no leaves, no legs, no tail, no stones, no amulet.", "", FLAT2]
    open(pl, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    ra.append(pl)
    gd += [f"| `L` (thân liền) | `{Wp(pl)}` | `{Wp(gdl)}`: MỘT hình bóng kem = cổ – ngực – bụng liền nhau, viền sẫm chỉ ở ngoài, một "
           f"bầu dục lục = mảng rêu | `{Wp(outl)}` |", "",
           "Kiểm từng tờ: số hình đúng, hình bóng trùng tờ hướng dẫn (Claude đo IoU, dưới 0,9 thì gen lại), mỗi hình viền kín, tô phẳng, "
           "nền trắng tinh, không chữ. Tờ `L`: trong hình KHÔNG có nét mực nào ngoài viền mảng rêu.", "",
           "Gửi thêm khi GPT vẽ sai: `Keep exactly the silhouettes, sizes and positions of image 2; do not move or merge shapes.` · "
           "`Flat colour only: remove every shadow, highlight and gradient.` · `Each shape needs its own closed ink outline.`"]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2:")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ================================================================ DẠNG 1 (chim non): concept trên bố cục dựng từ rig đã đổi tỉ lệ
# Người dùng 2026-11-12: "ok ổn đấy... làm dạng 1 đi". Không dặn hình, màu: hai hướng dưới là ĐỀ XUẤT của Claude, chờ người dùng chọn.
NON = {
    "kem": dict(ten="A · chim non lông kem (gần màu dạng lớn, nhạt hơn)",
                long="soft cream (#F7EFCB)", sage="light sage green (#A8C690)", la="spring green (#7FC25A)",
                la_nhat="light yellow-green (#B8DC72)", tan="fresh mid green (#4FA052)", gan="green (#3C8C46)",
                canh="light brown young wood (#9A6E48)", cam="soft orange (#F2A04A)", vuot="brown (#6A4A36)",
                da="light warm grey stone (#A8A498)", reu="moss green (#7FBE58)", nu="pink (#F2A6BC)"),
    "to_vang": dict(ten="B · chim non lông tơ vàng",
                    long="downy chick yellow (#F5DC86)", sage="olive green (#8FB36A)", la="spring green (#7FC25A)",
                    la_nhat="light yellow-green (#B8DC72)", tan="fresh mid green (#4FA052)", gan="green (#3C8C46)",
                    canh="light brown young wood (#9A6E48)", cam="orange (#F0923C)", vuot="brown (#6A4A36)",
                    da="light warm grey stone (#A8A498)", reu="moss green (#7FBE58)", nu="pink (#F2A6BC)"),
}


def build_non():
    lon = os.path.join(save_dir(), "L1_duyet.png")
    bc = os.path.join(HERE, "inbox", "chim_la_non", "mau", "bo_cuc.png")
    sd = os.path.join(HERE, "inbox", "chim_la_non", "tai_ve")
    pkn = os.path.join(HERE, "gui_gpt", "chim_la_non")
    for f in (lon, bc):
        if not os.path.exists(f):
            raise SystemExit("thiếu ảnh mẫu " + Wp(f))
    os.makedirs(sd, exist_ok=True)
    os.makedirs(pkn, exist_ok=True)
    gd = ["# Gói gửi GPT: `chim_la_non` (DẠNG 1 của chim bảo hộ rừng cánh lá: chim non; tướng thứ 6 đảo Mộc)", "",
          "Làm 2026-11-12. Dạng 1 dùng CHUNG rig với dạng lớn (`monster_3630`), đổi tỉ lệ ở rig (đầu to, cánh, đuôi, chuỗi đá ngắn lại, bỏ "
          "bùa đá, hoa, vòng gỗ; mào còn hai lá chữ V). Bố cục = hình rig dạng non dựng bằng da dạng lớn (`CL_DANG=non py -3 -I "
          "ArtGen/Spine/chim_la_rig.py bo_cuc`). Màu và chi tiết là đề xuất của Claude, chờ người dùng chọn. Ghi chú: "
          "`ArtGen/Spine/inbox/chim_la_ghichu.md`.", ""]
    ra = []
    for kieu, M in NON.items():
        out = os.path.join(sd, f"L1_{kieu}.png")
        p = os.path.join(pkn, f"luot_1_concept_{kieu}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(bc)}: PROPORTION GUIDE, 1536x1024, white background: a computer-assembled puppet of the YOUNG form of this "
             "bird, built from the grown bird's own parts rescaled on the animation skeleton (big head, plump body, small wings, short "
             "tail). It gives the exact pose, the proportions, and the place and size of every part. Its colours and its details are "
             "those of the GROWN form and must be changed as described below.",
             f"image 2 = {Wp(lon)}: the approved GROWN form of the same creature, 1536x1024, white background: {CON}. It gives the "
             "drawing style (wobbly dark-brown ink line, crayon hatching, completely flat colour) and the family look. The young form "
             "must clearly be the same species at a much younger age.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "",
             "TASK: draw the YOUNG FORM (the first evolution stage, a fledgling) of the forest guardian bird of image 2, as ONE picture, "
             "landscape 1536x1024, pure-white background, in the same hand-drawn style. Keep EXACTLY the pose, the proportions and the "
             "place and size of every part of image 1 (the picture will be mapped back onto that skeleton): the bird hovers facing the "
             "viewer's RIGHT, head in profile with ONE eye, both small wings spread, both feet raised in front, the short tail hanging.",
             "",
             "CHARACTER: a brave little fledgling who already wants to protect the forest: plump, big-headed and endearing, but with a "
             "determined, battle-ready little glare; not a smiling baby mascot, not scary.", "",
             "WHAT TO DRAW (each item stays where image 1 has it):",
             f"- HEAD (about x = 600 to x = 1040, y = 230 to y = 450): a BIG round fledgling head of soft down. A light HOOD of "
             f"{M['sage']} on the crown and the back of the head, ending in three short fluffy tufts at the back (left); the FACE (front, "
             f"cheek, throat) is {M['long']} with a soft zigzag feather edge. ONE eye at about (940, 330): clearly BIGGER and ROUNDER "
             f"than the grown bird's eye (about 44 px wide): {M['cam']} iris, big round dark pupil, one tiny white dot, a clean ink rim, "
             "and a SHORT slanted brow stroke above it tilting down toward the beak (a determined frown, not angry, not sad). No second eye.",
             f"- BEAK (about x = 975 to x = 1040, y = 350 to y = 412): a SHORT, stubby, slightly hooked beak of {M['cam']}, closed, one "
             "mouth line.",
             f"- CREST: only TWO young leaves standing up from the crown in a V, like a seedling's first pair of leaves: one leaning "
             f"slightly back (tip at about (830, 80)), one upright (tip at about (940, 105)); the taller is {M['la']}, the other "
             f"{M['la_nhat']}; each a simple pointed leaf with one centre vein. NO fan of five leaves, NO wooden circlet.",
             f"- BODY: a plump round body and thick neck of fluffy {M['long']} down with a few small scalloped down marks; one small "
             f"patch of {M['reu']} moss on the belly at about (700, 610).",
             f"- COLLAR (about x = 655 to x = 870, y = 455 to y = 640): a SMALL ruff of five or six little pointed leaves of "
             f"{M['la_nhat']} around the base of the neck, each with a centre vein. NO stone amulet, no ring, no clasps.",
             "- WINGS: small fledgling wings, spread. The NEAR wing is at the viewer's LEFT (about x = 225 to x = 610, y = 245 to "
             "y = 660), the FAR wing at the right behind the head and body (about x = 880 to x = 1310, y = 280 to y = 560). Each wing: "
             f"a THIN young BRANCH of {M['canh']} as the wing arm along the top edge, with two or three closed BUDS of {M['nu']} (small "
             f"pointed buds, NOT open flowers); under it a small CANOPY of little rounded leaves in {M['tan']} drawn as scalloped rows; "
             f"a row of SHORT pointed leaves of {M['la']} as flight feathers (the longest about 150 px) with a second row of tiny "
             f"{M['la_nhat']} leaves over their roots; each leaf has one centre vein of {M['gan']}; one small curled sprout of "
             f"{M['la_nhat']} at the wrist.",
             f"- LEGS: thighs are small trousers of {M['sage']} down; the scaly lower legs and BIG clumsy feet are {M['cam']} (near foot "
             "hanging at about x = 520 to x = 700, y = 660 to y = 900; far leg reaching right to about x = 1030, y = 790), four toes "
             f"each with a short curved claw of {M['vuot']}.",
             f"- TAIL (about x = 400 to x = 810, y = 650 to y = 950): six SHORT soft plume feathers, alternating {M['long']} and "
             f"{M['sage']}, each with two or three thin feather lines and a slightly ragged tip.",
             f"- STONES: only TWO short strings of three or four small rounded pebbles of {M['da']} hang among the tail plumes (about "
             f"x = 540 to x = 790, y = 860 to y = 955), the last pebble of each a little bigger with a cap of {M['reu']} moss. No big "
             "boulders, no sprouts on them.",
             "- Exactly: one head with one eye and a short beak, two crest leaves, one small leaf collar, two small leaf wings, two "
             "legs, six short tail plumes, two short strings of pebbles. No amulet, no circlet, no open blossoms.", "",
             f"COLOURS (use exactly these, each area one flat colour): body and face down {M['long']}; hood, thighs and every second "
             f"tail plume {M['sage']}; long wing leaves and the taller crest leaf {M['la']}; short leaves, collar, sprouts and the other "
             f"crest leaf {M['la_nhat']}; wing canopy {M['tan']}; leaf veins {M['gan']}; branches {M['canh']}; buds {M['nu']}; beak, "
             f"legs, toes and iris {M['cam']}; claws {M['vuot']}; pebbles {M['da']}; moss {M['reu']}; every outline dark-brown ink "
             "(#2B2118). The young form is LIGHTER and softer in colour than the grown form of image 2. Only these colours.", "",
             "CANVAS AND FRAMING: as in image 1 the whole bird is about 1090 px wide (x = 225 to x = 1310) and about 880 px tall "
             "(y = 75 to y = 955); nothing cut by the edges; no ground, no cast shadow.", "", POSE, "",
             "HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly like a real pen; "
             "loose crayon hatching inside every area. Image 1 is a rough machine-assembled puppet: take its pose, proportions, "
             "placement and sizes, but redraw every part cleanly as described (do not copy its seams, its blurred edges or its adult "
             "details).",
             LINE.replace("images 2 and 3", "image 2"), FLAT, BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd += [f"## Hướng `{kieu}`: {M['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/chim_la_non/luot_1_concept_{kieu}.txt`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
               f"| 1 | `{Wp(bc)}` | Bố cục chim non (1536 × 1024, nền trắng): hình rig dạng non ghép bằng da dạng lớn: đầu to, thân mập, hai "
               "cánh lá nhỏ xoè, hai lá mào chữ V, đuôi ngắn. Lấy dáng, tỉ lệ, chỗ đặt; màu và chi tiết phải đổi |",
               f"| 2 | `{Wp(lon)}` | Concept dạng lớn đã duyệt (1536 × 1024, nền trắng): chim trắng kem cánh lá, mào quạt lá, bùa đá. Lấy "
               "nét vẽ, tô phẳng, vẻ cùng loài |", ""]
    gd += ["## Kiểm", "",
           "- Chim non **nhìn sang phải**, đầu to, **một mắt** to tròn có nét mày quả quyết (không cười, không buồn), mỏ ngắn.",
           "- Mào chỉ **hai lá chữ V**; vòng cổ lá nhỏ; **không** bùa đá, vòng gỗ, hoa nở (cành có nụ hồng).",
           "- Cánh nhỏ vẫn là cành + tán lá + lá; đuôi sáu lông ngắn; hai chuỗi sỏi ngắn.",
           "- Màu nhạt hơn dạng lớn; tô phẳng, không bóng; nền trắng; bố cục trùng ảnh 1.", "",
           "Gửi thêm khi sai: `Keep the pose and proportions of image 1 exactly.` · `Flat colour only, remove shadows and highlights.` · "
           "`Only one eye, head in profile facing right.`"]
    open(os.path.join(pkn, "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    for p in ra:
        print(p)


if __name__ == "__main__":
    if sys.argv[1:2] == ["non"]:
        build_non()
    elif sys.argv[1:2] == ["manh"]:
        build_part()
    else:
        main()
