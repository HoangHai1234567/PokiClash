# -*- coding: utf-8 -*-
"""Gói GPT vẽ hươu gỗ cổ dài (mã làm việc huou_go, con gốc của rig: monster_3504). Tướng thứ 4 đảo Mộc.

Người dùng (2026-11-12): "concept sinh vật lai hươu và hươu cao cổ, thân gỗ, lông là lá cây, kết hợp pha lê, đá...; điểm khác với con
gốc con này bạn làm thêm mồm cho tôi há/đóng được". Không dặn màu: hai hướng dưới đây là ĐỀ XUẤT của Claude, chờ người dùng chọn.
Giữ cách dựng hình của con gốc (nhìn sang phải, cổ dài dựng đứng, lộ một mắt, bốn chân, bờm lá sau cổ, cụm pha lê ở vai); hình là của
mình. Không đính ảnh con gốc; đính sơ đồ bố cục tự dựng bằng mã (huou_go.py bo_cuc).

    py -3 -I ArtGen/Spine/huou_go.py bo_cuc
    py -3 -I ArtGen/Spine/build_huou_go.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/huou_go_2/luot_1_concept_<hướng>.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "huou_go"
K = 2                                            # con hươu cổ dài là DẠNG 2 (người dùng 2026-11-12: lấy monster_3304 làm dạng 1)
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
CACTUS = os.path.join(HERE, "inbox", "xuong_rong_1", "tai_ve", "L1_duyet.png")
STONE = os.path.join(HERE, "inbox", "tuong_da_1", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def pk(k=K):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def mau_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "mau")


# màu theo hướng: (tên tiếng Anh + mã) cho từng nhóm
MAU = {
    "he": dict(
        go="warm light oak wood (#CDA670)", dom="darker brown bark (#8E623C)", sung="dark branch wood (#704C30)",
        la="fresh forest green (#569646)", la_nhat="light spring green (#92C458)", gan="darker green (#3C7436)",
        pha_le="amber, like hardened golden tree resin (#F2B43E)", pha_le_dam="deeper amber (#D68620)",
        nhua="amber (#F2B43E)", cam="NO blue, NO purple, NO pink, NO white fur",
        ten="lá lục, pha lê hổ phách (nhựa cây), gỗ sồi"),
    "thu": dict(
        go="pale birch wood (#E2D6BA)", dom="dark brown bark (#7C5C40)", sung="dark brown branch wood (#7C5C40)",
        la="autumn maple red-orange (#D66C32)", la_nhat="autumn yellow (#F0AC3E)", gan="darker rust red (#A8481E)",
        pha_le="emerald green (#40CE96)", pha_le_dam="deeper emerald (#1E966E)",
        nhua="emerald green (#40CE96)", cam="NO blue, NO purple, NO pink",
        ten="lá phong đỏ cam, pha lê lục bảo, gỗ bạch dương"),
}


def body(kieu):
    M = MAU[kieu]
    return "\n".join([
        "CREATURE: a FOREST STAG-GIRAFFE, a plant-element monster for a monster-collecting game: a four-legged beast that is a "
        "cross between a DEER and a GIRAFFE, whose body is made of living WOOD, whose fur is LEAVES, and that carries CRYSTALS "
        "and a little STONE. It has a deer's wide branching antlers and a giraffe's long, thick, upright neck and patchwork "
        "pattern. Character: a proud, calm guardian of the forest standing firm and battle-ready, head held high; appealing and "
        "noble, not scary, not a smiling cute mascot. Chunky, bold, simple shapes with few details (the way a Pokemon is "
        "designed).",
        "Follow the LAYOUT GUIDE (image 1) for WHERE every part is on the canvas, HOW BIG it is and WHICH part overlaps which. "
        "The outlines in the guide are only rough computer blobs: design the real outline of every part yourself as described "
        "below, but keep every part in its place and at its size.",
        "- VIEW: three-quarter view; the creature faces the viewer's RIGHT. The body is seen slightly from the front-right: the "
        "chest and the long neck are at the right half, the hindquarters and the tail at the left. The head sits on top of the "
        "upright neck and is turned so that only ONE eye is visible.",
        f"- NECK AND CHEST (one piece, from about x = 756 to x = 994, y = 317 to y = 831): a long, thick, straight trunk of "
        f"{M['go']} that rises almost vertically like a giraffe's neck and widens at the bottom into a round chest. Smooth "
        f"carved wood. On it, a loose GIRAFFE PATTERN of five to seven angular patches of {M['dom']} (each an irregular "
        "four- to six-sided plate about 35-60 px, with narrow lighter wood between them), like plates of bark. No fur on it.",
        f"- BODY (behind the chest, to the left, from about x = 577 to x = 833, y = 619 to y = 823): a short, compact barrel of "
        f"the same wood with three or four of the same bark patches; the rump at the left.",
        "- HEAD (skull centred at about x = 905, y = 338, about 185 px wide; muzzle reaching down-right to about x = 1035, "
        "y = 500): a gentle deer / giraffe head of the same wood: a round skull and a clearly separate, fairly long, blunt "
        "MUZZLE pointing down and to the right. ONE eye only, on the visible side of the face at about x = 892, y = 350: a "
        "CLOSED eye drawn as one short thick curved ink stroke (calm, like a serene forest spirit), with a tiny brow line above "
        "it. One small dark nostril near the muzzle tip. A clear MOUTH: one ink line that runs from the front of the muzzle "
        "(about x = 1030, y = 470) back along the muzzle to the cheek (about x = 916, y = 458), closed, calm, very slightly "
        "upturned at the back; below this line the LOWER JAW reads as its own distinct chunky part (the mouth will open in "
        "animation). One bark patch on the cheek. No teeth showing, no tongue.",
        f"- ANTLERS ({M['sung']}, like living branches; thin veins of {M['nhua']} sap run along them as two or three narrow "
        "stripes on each): FOUR beams growing from the top of the skull. At the viewer's LEFT (in front of the mane): one big "
        "upper beam sweeping up and to the left from about x = 866, y = 377 to its tips at about x = 419-640, y = 93-200, "
        "forking into three blunt tines, and one lower beam from about x = 868, y = 330 reaching left to about x = 502, y = 400 "
        "with one short tine. At the viewer's RIGHT: one upper beam sweeping up and to the right to its tip at about x = 1160, "
        "y = 70 (two tines), and one lower beam reaching right to about x = 1194, y = 400 (one short tine). Blunt, chunky "
        f"tines. Two or three of the tine tips carry one small {M['la_nhat']} leaf bud. The open space between the left and "
        "right antlers above the head stays EMPTY of antler (the mane shows there).",
        f"- EARS: two big LEAF-shaped ears of {M['la_nhat']}, each one large drooping leaf with a few lobes and a centre vein: "
        "the near one hangs down-left from the side of the head (from about x = 669 to x = 859, y = 323 to y = 578), in front "
        "of the mane; the far one hangs at the right of the head (about x = 945 to x = 1069, y = 315 to y = 571), partly "
        "behind the head.",
        f"- MANE (behind the neck, the head and the antler roots, from about x = 515 to x = 1149, y = 144 to y = 658): a huge "
        f"round RUFF OF LEAVES in {M['la']}: big overlapping pointed leaves (each about 90-150 px long, with one centre vein in "
        f"{M['gan']}), arranged in two or three layered rows that radiate outward like a lion's mane made of foliage, so the "
        "edge of the mane is a ring of clear leaf tips. One mass, about 630 px wide. Not fluffy fur, not a smooth ball.",
        f"- CRYSTALS: a cluster of FOUR big crystals of {M['pha_le']} grows out of the near shoulder / back, in front of the "
        "body and to the left of the neck (from about x = 666 to x = 884, y = 552 to y = 782): tall pointed prisms leaning "
        f"slightly outward, the tallest about 215 px, each with two or three flat facets, the facet on its right side "
        f"{M['pha_le_dam']}. Two more crystals of the same kind show at the far shoulder, at the right of the chest (about "
        "x = 947 to x = 1051, y = 585 to y = 754). Flat colour: no glow, no sparkle, no transparency.",
        "- AT THE FOOT OF EACH CRYSTAL CLUSTER: a low cushion of moss (#629C48) with a bumpy scalloped edge (near one about "
        "x = 678 to x = 910, y = 700 to y = 838; far one about x = 937 to x = 1057, y = 720 to y = 811), with two or three "
        "small grey STONES (#8C887C) sitting in the moss.",
        "- LEGS: four sturdy, fairly short legs of the same wood, like carved posts, slightly wider at the bottom, each ending "
        "in a chunky HOOF of grey stone (#8C887C), the lower quarter of the leg. Near hind leg at about x = 537-675, "
        "y = 710-960; far hind leg at about x = 702-842, y = 696-950, behind the body; "
        "near front leg at about x = 755-896, y = 725-959, in front of the chest; far front leg at about "
        "x = 918-1076, y = 706-953. All four hooves stand on the same ground level at about y = 955. One bark patch on each "
        f"upper leg. On the thigh of the near hind leg, one small tuft of three {M['la']} leaves (about x = 541-646, "
        "y = 734-859).",
        f"- TAIL (at the left): a thin wooden stem, like a giraffe's tail, rising from the rump at about x = 645, y = 640 up "
        f"and to the left to about x = 365, y = 565, ending in a big TUFT of five or six {M['la']} leaves (about x = 340 to "
        f"x = 570, y = 540 to y = 772), with one small {M['la_nhat']} leaf standing up at its tip (about x = 362-415, "
        "y = 456-573).",
        "- Exactly: one head with one visible closed eye and a closed mouth, four antler beams, two leaf ears, one leaf mane, "
        "one neck-and-chest trunk, one body, four legs with four stone hooves, one tail with a leaf tuft, four near crystals "
        "and two far crystals, two moss cushions with small stones.",
        "",
        f"COLOURS, a calm, slightly muted palette (use exactly these, each area one flat colour): all the wood of the body "
        f"(neck, chest, body, head, legs, tail stem) {M['go']}; the giraffe / bark patches {M['dom']}; the antlers "
        f"{M['sung']} with sap veins of {M['nhua']}; the mane, the tail tuft and the leg tuft {M['la']} with veins of "
        f"{M['gan']}; the two ears, the small tail-tip leaf and the antler buds {M['la_nhat']}; the crystals {M['pha_le']} "
        f"with their darker facets {M['pha_le_dam']}; moss (#629C48); hooves and small stones grey stone (#8C887C); every "
        f"outline dark-brown ink (#2B2118). Only these colours. {M['cam']}.",
    ])


FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the whole creature is about 855 px wide (from the tail tuft at about x = 340 "
         "to the right antler at about x = 1194) and about 890 px tall (from the antler tips at about y = 70 to the hooves at "
         "about y = 960).")

POSE = ("POSE (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): standing still on "
        "all four legs in a calm, clean resting pose, exactly as in the guide: legs straight and apart, not crossing; the neck "
        "upright; the mouth closed. Every part listed above is a clear, readable shape with its own ink outline (each antler "
        "beam, each ear, each crystal, each leg, the mane, the tail tuft). No falling leaves, no dust, no sparkles, no glow, no "
        "motion lines, no ground, no grass, no props.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn shapes; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The layout "
        "guide is a stiff flat computer diagram with rough, jagged edges: take only the placement, the sizes, the overlaps and "
        "the colour of each kind of part from it, never its line, its jagged edge noise or its exact blobs. Draw the leaves as "
        "simple bold leaf shapes, the wood as smooth carved timber with at most two or three thin grain lines per part, the "
        "crystals as clean chunky prisms.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 6 px thick on this canvas around every big part (head, neck, body, legs, "
        "antlers, mane, ears, tail tuft, big crystals), and about 4 px for small details (leaf buds, small stones, moss edge, "
        "bark patches, the eye, the mouth line); leaf veins, wood grain and crystal facet lines are thin darker pencil lines "
        "about 3-4 px, not ink; every area coloured with coloured pencils and wax crayons, the strokes visible as loose "
        "diagonal hatching (strokes thinner than the outline), kept inside the outline. Clean and appealing, neither a crude "
        "scribble nor overly detailed: no realistic bark texture, no knots and cracks all over, no tiny leaves everywhere.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker underside, no lighter patches or blotches, no shadows of any kind (no cast "
        "shadow of one part on another, no shadow under the figure or on the background), no white highlights or shine spots, "
        "no gloss, no reflections on the crystals, no glow, no rim light, no gradients, no 3D look. A different tone appears "
        "only where the design itself lists a different colour (bark patches, crystal facets, leaf veins).")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the creature.")


def refs(kieu):
    M = MAU[kieu]
    return [
        (os.path.join(mau_dir(), f"bo_cuc_{kieu}.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature showing where every part "
         "goes on the canvas, how big it is and which part overlaps which (light wood: the head with its muzzle, eye arc and "
         "mouth line, the tall neck-and-chest trunk, the body, the four legs, the tail stem; dark brown: the four antler beams "
         "and the bark patches; the big leaf-coloured mass behind the neck: the leaf mane; the two lighter leaf shapes beside "
         "the head: the ears; the leaf shapes at the left: the tail tuft; the pointed two-tone prisms at the shoulders: the "
         "crystals; green cushions under them: moss; grey bands at the feet: stone hooves). Use it for placement, size and "
         "overlap only; redraw everything in the hand-drawn style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): con bốn chân nhìn sang phải, cổ dài dựng đứng, tô phẳng theo nhóm "
         "màu (gỗ sáng: đầu có mõm + nét mắt nhắm + khe miệng, cổ liền ngực, thân, bốn chân, cán đuôi; nâu sẫm: bốn nhánh gạc và "
         "mảng vỏ cây; mảng lá lớn sau cổ: bờm; hai lá nhạt cạnh đầu: tai; cụm lá bên trái: đuôi; lăng trụ hai tông ở vai: pha lê; "
         "đệm lục: rêu; dải xám ở chân: móng đá). Lấy chỗ đặt, cỡ, thứ tự chồng"),
        (CACTUS,
         "an approved hero of the same game and the same island (a round cactus monster), 1536x1024, white background: match "
         "EXACTLY its wobbly dark-brown pen line, its visible crayon hatching, its completely flat colouring and its bold, "
         "simple, chunky level of detail. Do NOT copy its species, its design or its colours.",
         "Xương rồng tròn đã duyệt (1536 × 1024, nền trắng): quả cầu lục miệng to nanh kem. Lấy nét bút rung, vân sáp, tô phẳng, mức "
         "chi tiết gọn"),
        (STONE,
         "another approved hero of the same island (a floating stone guardian with moss and wooden antlers), 1536x1024, white "
         "background: the same line and flat crayon colouring; see how its wooden branch antlers, its leaves, its moss cushions "
         "and its stones are drawn. Do NOT copy its design or its colours.",
         "Tượng đá giữ rừng đã duyệt (1536 × 1024, nền trắng): các khối đá lơ lửng phủ rêu, đầu trụ đá có hai nhánh gạc. Lấy nét, tô "
         "phẳng, cách vẽ gạc cây, lá, rêu, đá"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching) and the way its trees, leaves and rocks are simplified, nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp, cách giản lược cây, lá, đá"),
    ]


CHECK = [
    "Con **bốn chân nhìn sang phải**, cổ dài dựng đứng kiểu hươu cao cổ, đầu trên đỉnh cổ, **lộ một mắt** (nhắm, một nét cong), có "
    "**khe miệng** rõ dọc mõm (ngậm), hàm dưới đọc ra là một khối riêng.",
    "Đủ: bốn nhánh gạc cành cây (hai trái, hai phải, khoảng giữa trên đầu để trống), hai tai lá, bờm là **vòng lá to xếp lớp** (không "
    "phải lông xù), cổ + ngực một khối có **mảng vỏ cây kiểu đốm hươu cao cổ**, thân, bốn chân **móng đá xám**, đuôi cán gỗ + chùm lá.",
    "Bốn pha lê ở vai gần + hai ở vai xa, dưới chân mỗi cụm có đệm rêu và vài viên đá nhỏ.",
    "Hướng `he`: gỗ sồi sáng, lá lục, pha lê hổ phách. Hướng `thu`: gỗ bạch dương, lá phong đỏ cam, tai lá vàng, pha lê lục bảo.",
    "Tô phẳng: **không** bóng, không mảng sáng tối, pha lê không phát sáng, không điểm sáng trắng; nền trắng tinh; không lá rơi.",
    "Bố cục trùng sơ đồ: chân thẳng, tách nhau, không chéo; cả con không bị cắt mép.",
]

FIX = [
    ("Hai mắt, mặt quay chính diện", "Only ONE eye is visible: the head is turned to the viewer's right as in image 1; remove the "
                                     "second eye."),
    ("Không có khe miệng / miệng cười to", "Draw the mouth as ONE closed ink line along the muzzle from its tip back to the cheek, "
                                           "calm, with the lower jaw as a distinct part below it."),
    ("Bờm là lông xù", "The mane is made of big overlapping LEAVES with centre veins in layered rows, not fur."),
    ("Có bóng, mảng sáng tối, pha lê phát sáng", "Flat colour only: remove every shadow, highlight, gradient and glow; each area "
                                                 "one even colour; keep the crayon hatching as texture only."),
    ("Quá nhiều vân gỗ, nứt, lá vụn", "Simplify: smooth carved wood with at most two or three grain lines per part, bold simple "
                                      "leaves."),
    ("Cổ ngắn như hươu thường", "The neck is long, thick and upright like a giraffe's, as tall as in image 1."),
    ("Bố cục khác sơ đồ", "Follow image 1 exactly for the place and size of every part; the creature faces the viewer's right."),
]


def main():
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    gd = [f"# Gói gửi GPT: `{CODE}` dạng {K} (hươu gỗ cổ dài: lai hươu và hươu cao cổ, tướng thứ 4 đảo Mộc, tên chưa đặt)", "",
          "Làm 2026-11-12: dựng trên rig của con gốc `monster_3504`; màu và chi tiết là đề xuất của Claude, chờ người dùng chọn hướng "
          "và duyệt concept. Ghi chú: `ArtGen/Spine/inbox/huou_go_ghichu.md`.", "",
          "Lượt 2 (mảnh) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    ra = []
    for kieu in MAU:
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
              "approved hero images.", "", body(kieu), "", FRAME, "", POSE, "", SOFT, LINE, FLAT, BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd += [f"## Hướng `{kieu}`: {MAU[kieu]['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{K}/luot_1_concept_{kieu}.txt` (thêm "
               "`--note \"...\"` để sửa nhanh).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += [""]
    gd += ["Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/huou_go.py bo_cuc`).",
           "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    open(os.path.join(pk(), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 1b: người dùng chọn hướng "thu" (2026-11-12) và dặn sửa:
# "t thích hướng B hơn nhưng bỏ mắt đi, làm mặt chiến hơn mồm tách hàm"
def build_sua():
    nhap = os.path.join(save_dir(), "L1_thu.png")
    if not os.path.exists(nhap):
        raise SystemExit("thiếu bản nháp " + Wp(nhap))
    out = os.path.join(save_dir(), "L1b_thu.png")
    p = os.path.join(pk(), "luot_1b_mat_chien.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(nhap)}: the DRAFT of this creature, 1536x1024, white background: a forest stag-giraffe made of pale birch "
         "wood with dark bark patches, facing the viewer's right, with four dark branch antlers (green sap veins, yellow leaf "
         "buds), a big mane of red-orange maple leaves, two yellow leaf ears, emerald crystals on moss cushions with small grey "
         "stones at its shoulders, four legs with grey stone hooves and a leaf-tuft tail. Its head has one closed smiling eye and "
         "a smiling mouth line. This is the design, the line and the colouring to keep.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as L1b_thu_2.png, L1b_thu_3.png ... in the same folder. Do not edit, "
         "move or delete any other file.", "",
         "TASK: redraw image 1 as ONE picture, changing ONLY the HEAD (the face) as listed under CHANGE.", "",
         "KEEP IDENTICAL to image 1, in the same place and at the same size (if the new picture were laid over image 1, "
         "everything except the face must coincide): all four antler beams with their green veins and yellow buds, the whole "
         "leaf mane, both yellow leaf ears, the long neck-and-chest trunk with its bark patches, the body, the four legs and "
         "stone hooves, the leg leaf tuft, the tail and its leaf tuft, all the crystals, the moss cushions and small stones, "
         "every colour, the wobbly dark-brown ink line, the crayon hatching, the completely flat colouring, the white "
         "background. The head stays in the same place, at about the same size (skull centred at about x = 905, y = 340; "
         "muzzle tip at about x = 1035, y = 445), turned the same way (to the viewer's right), on the same neck, with the "
         "antlers and ears attached at the same spots.", "",
         "CHANGE, THE FACE: make it the face of a FIERCE, battle-ready forest guardian instead of a happy smiling one.",
         "1. NO EYES. Remove the closed eye and the brow line of image 1 completely. The creature has no eyes at all: no eye, "
         "no eyelid line, no pupil, no eye socket, no hole, no dot that could read as an eye. Where the eye was there is only "
         "wood.",
         "2. A STERN BROW PLATE instead: the upper part of the face (the forehead and the area where an eye would be, from "
         "about x = 845 to x = 965, y = 285 to y = 375) is covered by ONE angular plate of the dark brown bark (#7C5C40, the "
         "same colour as the bark patches), like the brow of a carved wooden war mask or a helmet visor: its lower edge is a "
         "hard, straight line that slants steeply DOWN toward the muzzle (high at the back of the head, low at the front), and "
         "it juts forward a little over the muzzle as a blunt point. This slanted brow gives the face its angry, determined "
         "look. It is a solid flat plate: no eye opening in it, no slit.",
         "3. A LONGER, HARDER MUZZLE: the muzzle is a little longer and more angular than in image 1, a blunt wedge of pale "
         "wood with a flat top and a squared tip, pointing to the right and slightly down. Keep one small dark nostril near "
         "the tip.",
         "4. SPLIT JAWS (very important): the mouth is no longer a smile line. The UPPER JAW and the LOWER JAW are two clearly "
         "separate pieces of wood, and the gap between them is a bold JAGGED ZIGZAG seam, like a log split into two "
         "interlocking halves: four or five big, chunky, pointed wooden TEETH on each side that fit into each other (sawtooth, "
         "each tooth about 20-28 px), running from the tip of the muzzle (about x = 1030, y = 462) all the way back to the "
         "cheek below the brow plate (about x = 890, y = 455). The teeth are part of the wood (same pale wood colour), not "
         "white fangs. The jaws are CLOSED, the teeth meshed, with only a thin dark gap line between them; the seam slants "
         "slightly DOWN toward the back corner (a grim, set mouth: no smile, no upturned corner). The LOWER JAW is a strong, "
         "square, heavy chin piece with its own closed ink outline, from about y = 462 down to about y = 512, hinged at the "
         "back under the cheek with a small round wooden peg mark. No tongue, no drool.",
         "5. Remove the round bark patch on the cheek of image 1 (the brow plate replaces it). Keep the faint wood grain "
         "lines.",
         "The whole head is still pale birch wood (#E2D6BA) except the dark brow plate. Chunky, bold and simple, appealing "
         "rather than horrific: a proud wooden beast with a war-mask face, not a monster skull, no cracks, no blood, no glow.", "",
         "Do not add anything else. Everything outside the head exactly as in image 1.", "", FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = ["", "## Lượt 1b: sửa hướng `thu` (2026-11-12)", "",
          "Người dùng chọn hướng B (`thu`) và dặn: **bỏ mắt đi, làm mặt chiến hơn, mồm tách hàm**. Lượt này vẽ lại y hệt bản nháp "
          "`L1_thu.png`, chỉ đổi mặt: không mắt; tấm vỏ cây sẫm phủ trán có mép dưới xếch xuống phía mõm (vẻ dữ); mõm dài, vuông hơn; "
          "hai hàm tách rời bằng khe răng cưa (răng gỗ đan nhau), hàm dưới là một khối cằm vuông có viền kín.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(nhap)}` | Bản nháp hướng thu (1536 × 1024, nền trắng): hươu gỗ bạch dương cổ dài nhìn sang phải, bờm lá phong đỏ "
          "cam, gạc cành cây vân lục, pha lê lục bảo trên đệm rêu, móng đá; mặt có một mắt nhắm cười và khe miệng cười |", "",
          "Kiểm: **không còn mắt** (không hốc, không chấm); tấm vỏ sẫm trên trán mép xếch; khe miệng răng cưa từ chóp mõm tới má, không "
          "cười; hàm dưới là khối riêng viền kín; mọi thứ ngoài đầu trùng bản nháp; vẫn tô phẳng, nền trắng."]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 1b")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    print(p)


# ---------------------------------------------------------------- lượt 1c (2026-11-12; người dùng gửi nhầm sang phiên tuong_da, phiên đó
# chuyển tiếp nguyên văn): "dạng 2 bỏ phần nâu ở trên đầu cũng đốm nâu đi, phần bụi rêu và pha lê cho ra sau lưng"
def build_sua2():
    nhap = os.path.join(save_dir(), "L1b_thu.png")
    if not os.path.exists(nhap):
        return
    out = os.path.join(save_dir(), "L1c_thu.png")
    p = os.path.join(pk(), "luot_1c_dau_dom_pha_le_lung.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(nhap)}: the DRAFT of this creature, 1536x1024, white background: a forest stag-giraffe made of pale birch "
         "wood with dark brown bark patches, facing the viewer's right, with four dark branch antlers (green sap veins, yellow "
         "leaf buds), a big mane of red-orange maple leaves, two yellow leaf ears, an eyeless head with a dark brown bark plate "
         "over its forehead and jagged split wooden jaws, emerald crystals on moss cushions with small grey stones at its "
         "shoulders (in front of the body, beside the front legs), four legs with grey stone hooves and a leaf-tuft tail. This "
         "is the design, the line and the colouring to keep.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as L1c_thu_2.png, L1c_thu_3.png ... in the same folder. Do not edit, "
         "move or delete any other file.", "",
         "TASK: redraw image 1 as ONE picture, changing ONLY the two things listed under CHANGE.", "",
         "KEEP IDENTICAL to image 1, in the same place and at the same size (if the new picture were laid over image 1, "
         "everything else must coincide): all four antler beams with their green veins and yellow buds, the whole leaf mane, "
         "both yellow leaf ears, the shape of the head with its long squared muzzle, its nostril, its jagged zigzag split jaws, "
         "its separate lower jaw and hinge peg, the long neck-and-chest trunk, the body, the four legs and stone hooves, the leg "
         "leaf tuft, the tail and its leaf tuft, every colour, the wobbly dark-brown ink line, the crayon hatching, the "
         "completely flat colouring, the white background. Still NO eyes anywhere on the head.", "",
         "CHANGE 1, THE HEAD: remove the dark brown bark plate that covers the forehead and the top of the muzzle in image 1. "
         "The whole head is now the same pale birch wood as the neck, and it carries the same GIRAFFE PATTERN as the body: "
         "three or four angular dark brown bark patches (#7C5C40), each an irregular four- to six-sided plate about 30-50 px "
         "(one on the forehead, one on the cheek, one small one on the top of the muzzle, one small one on the lower jaw). "
         "Keep the head's outline, the muzzle, the jaws and the teeth exactly as they are; no eyes, no eye sockets, no brow.",
         "CHANGE 2, THE CRYSTALS AND MOSS: remove BOTH crystal clusters with their moss cushions and small grey stones from "
         "the shoulders (the big cluster in front of the body beside the near front leg, and the smaller cluster at the right "
         "of the chest); where they were, complete the body, the chest and the tops of the front legs as plain pale wood with "
         "their bark patches. Instead, put ONE cluster on the creature's BACK: a moss cushion (#629C48) with a bumpy "
         "scalloped edge lies on top of the back like a saddle (on the top line of the body, between the base of the neck and "
         "the tail, at about x = 560 to x = 760, y = 590 to y = 650), with two or three small grey stones in it, and FOUR "
         "emerald-green crystals (the same chunky pointed prisms as in image 1, the tallest about 190 px, the darker facet on "
         "the right side of each) grow straight UP out of that moss, leaning slightly apart like a little crown on its back, "
         "in front of the leaf mane. Nothing else changes.", "",
         "Do not add anything else: no extra crystals elsewhere, no glow, no effects.", "", FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = ["", "## Lượt 1c: đầu đốm nâu, rêu + pha lê ra sau lưng (2026-11-12)", "",
          "Người dùng (gửi nhầm sang phiên khác, được chuyển tiếp nguyên văn): \"dạng 2 bỏ phần nâu ở trên đầu cũng đốm nâu đi, phần bụi "
          "rêu và pha lê cho ra sau lưng\". Lượt này vẽ lại y hệt `L1b_thu.png`, chỉ đổi: bỏ tấm vỏ nâu trên trán, cả đầu là gỗ sáng có "
          "mảng đốm nâu như thân; bỏ hai cụm pha lê + rêu ở vai, đặt MỘT cụm (bốn pha lê trên đệm rêu có đá nhỏ) trên sống lưng.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(nhap)}` | Bản nháp 1b (1536 × 1024, nền trắng): hươu gỗ bạch dương cổ dài nhìn sang phải, không mắt, tấm vỏ nâu "
          "phủ trán, hai hàm răng cưa, hai cụm pha lê lục bảo trên rêu ở hai vai, bờm lá phong đỏ cam |", "",
          "Kiểm: đầu **không còn tấm nâu**, có ba bốn mảng đốm nâu; vẫn không mắt, hàm răng cưa giữ nguyên; **không còn pha lê / rêu ở "
          "vai**, một cụm bốn pha lê trên đệm rêu nằm **trên lưng**; mọi thứ khác trùng bản nháp."]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 1c")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    print(p)


# ---------------------------------------------------------------- lượt 2 (dạng 2): bốn tờ mảnh theo khung part + hai tờ "đúng chỗ,
# đúng cỡ" cho đầu, cụm pha lê lưng, hàm dưới (người dùng duyệt L1c_thu.png 2026-11-12: "ok dạng 2 mới ổn" → L1_duyet.png)
PART_RULE = ("HOW TO DRAW EVERY PART: image 2 is a stiff computer-made sheet: each part is a flat silhouette in its exact place. "
             "Redraw the sheet cleanly in the hand-drawn style of image 1 and keep, for EVERY part, EXACTLY its silhouette: the same "
             "outline, the same size, the same orientation and the same position on the canvas (if your picture were laid over "
             "image 2, every part must coincide with its silhouette). Do NOT move, rotate, resize, straighten, merge, add or remove "
             "any part; do not assemble the parts into a creature; keep the white gaps between the parts. Take from image 1 only "
             "the look: the wobbly dark-brown ink pen line (#2B2118), the loose diagonal crayon hatching inside every area, the "
             "exact colours. Smooth away the jagged pixel noise of the guide edges, nothing more.")
PART_FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no "
             "darker side, no highlights, no gloss, no gradients, no cast shadows. Pure white (#FFFFFF) background everywhere "
             "between and around the parts; no text, no labels, no numbers, no frames, no guide lines, no extra marks.")
PART_MAU = ("COLOURS (exactly as on image 1): pale birch wood #E2D6BA; bark patches and antlers dark brown #7C5C40; sap vein emerald "
            "#40CE96; mane, tail tuft and leg tuft maple red-orange #D66C32 with veins of rust red #A8481E; ears and small leaves "
            "autumn yellow #F0AC3E with veins of darker orange #C97E22; hooves grey stone #8C887C; ink #2B2118.")
CREATURE2 = ("the APPROVED creature, 1536x1024, white background: a forest stag-giraffe of pale birch wood with dark brown bark "
             "patches, an eyeless spotted head with jagged split wooden jaws, four dark branch antlers with green sap veins, a big "
             "mane of red-orange maple leaves, two yellow leaf ears, emerald crystals on a moss cushion on its back, four legs with "
             "grey stone hooves and a leaf-tuft tail. It gives the design, the colours, the ink line and the crayon hatching.")


def _o(khung, ten):
    v = khung[ten]
    return f"centre at about x = {v['x'] + v['w'] // 2}, y = {v['y'] + v['h'] // 2}, about {v['w']} px wide and {v['h']} px tall"


def build_part2():
    import json
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    if not os.path.exists(duyet):
        return []
    Kh = {to: json.load(open(os.path.join(mau_dir(), f"part_{to}.json"), encoding="utf-8")) for to in "ABCD"
          if os.path.exists(os.path.join(mau_dir(), f"part_{to}.json"))}
    if len(Kh) < 4:
        print("chưa có tờ hướng dẫn: chạy HG_DANG=2 huou_go.py nhom_part")
        return []
    A, B, C, D = Kh["A"], Kh["B"], Kh["C"], Kh["D"]
    noi = {
        "A": ("two big parts: the leaf mane and the neck-and-chest trunk", 6,
              ["- THE MANE (left; " + _o(A, "P_toufa") + "): the COMPLETE mane as one mass, as if the head, the neck, the ears and "
               "the antlers had been taken away from in front of it: it is made of big overlapping red-orange MAPLE LEAVES (each "
               "about 150-230 px on this sheet, with a centre vein and side veins), arranged in two or three layered rows that "
               "radiate outward from the middle; the pointed tips of the outer leaves form the jagged edge of the silhouette: "
               "follow the silhouette of the guide exactly, every point of it is a leaf tip. The middle of the mass is also "
               "covered with leaves (no hole, no empty patch, no wood showing). A closed ink outline around the whole mass, thinner "
               "ink lines between the leaves.",
               "- THE NECK-AND-CHEST TRUNK (right; " + _o(A, "P_bozi") + "): the COMPLETE long neck with the round chest at its "
               "bottom, as if the head, the mane and the legs had been taken off: pale birch wood with two or three thin wavy "
               "grain lines running along it and the dark brown bark patches of the giraffe pattern exactly where the guide shows "
               "them (each an angular plate with a thin ink outline). A closed ink outline all around."]),
        "B": ("five parts: the body and four antler beams", 6,
              ["- THE BODY (top left; " + _o(B, "P_shenti") + "): the barrel of the body: pale birch wood with the bark patches "
               "where the guide shows them and one or two grain lines; closed ink outline. No crystals, no moss, no legs, no tail "
               "on it.",
               "- FOUR ANTLER BEAMS (" + "; ".join(_o(B, t) for t in ("P_y_jiao1", "P_z_jiao1", "P_y_jiao", "P_z_jiao")) + "): "
               "each a branching antler beam of dark brown branch wood, exactly its silhouette with all its tines, with ONE thin "
               "emerald-green sap vein (about 6 px) running along the middle of the beam and into each tine, as on image 1; "
               "closed ink outline. No leaves, no buds on them."]),
        "C": ("two leaf ears, the tail tuft, the tail stem, two small leaves and a leg tuft", 6,
              ["- TWO EARS (top left; " + _o(C, "P_y_er") + " and " + _o(C, "P_z_er") + "): each one big drooping autumn-yellow "
               "maple leaf with a few lobes, exactly its silhouette, with a centre vein and side veins; closed ink outline.",
               "- THE TAIL TUFT (top, third; " + _o(C, "P_weiba3") + "): a bunch of five or six red-orange maple leaves fanning "
               "out, exactly the jagged silhouette (every point is a leaf tip), each leaf with a centre vein; closed ink outline "
               "around the bunch, thinner ink lines between the leaves.",
               "- THE TAIL STEM (bottom left; " + _o(C, "P_weiba1") + "): a thin bent stem of pale birch wood, exactly its "
               "silhouette, with one grain line and no patches; closed ink outline.",
               "- TWO SMALL YELLOW LEAVES (" + _o(C, "P_weiba") + "; and " + _o(C, "P_weiba2") + "): small autumn-yellow leaves "
               "(the first a little three-pointed leaf, the second a simple pointed leaf), each with a centre vein; closed ink "
               "outline.",
               "- THE LEG TUFT (bottom right; " + _o(C, "P_y_houmaofa") + "): a small sprig of two or three red-orange leaves, "
               "exactly the jagged silhouette, with centre veins; closed ink outline.",
               "The veins are thin darker pencil lines (about 4 px), not ink."]),
        "D": ("ten leg parts", 6,
              ["- TEN LEG PARTS in two rows, each exactly its silhouette, each with a closed ink outline: pale birch wood with "
               "one or two grain lines and the dark brown bark patches where the guide shows them (angular plates with a thin ink "
               "outline; keep them few and bold, as on the legs of image 1).",
               "- The four parts whose lower part is grey in the guide (" + "; ".join(_o(D, t) for t in
               ("P_y_houzhi2", "P_z_houzhi2", "P_y_qianzhi", "P_z_qianzhi1")) + "): the lower leg with its hoof: wood above, a "
               "chunky grey STONE hoof below, with one ink line between wood and stone exactly where the guide shows the border; "
               "the stone is flat grey with one tiny chip line, no patches on it.",
               "No leaves, no moss, no crystals on any leg part."]),
    }
    out = []
    for to, (gi, net, ds) in noi.items():
        luu = os.path.join(save_dir(), f"N_{to}.png")
        p = os.path.join(pk(), f"luot_2_manh_{to}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(duyet)}: {CREATURE2}",
             f"image 2 = {Wp(os.path.join(mau_dir(), f'part_{to}.png'))}: PART SHEET GUIDE, 1536x1024, white background: {gi}, "
             "each drawn by computer as a flat silhouette lying in its exact place on the canvas. It gives, for every part, the "
             "silhouette, the size, the orientation and the position.",
             "", f"SAVE: save it as a PNG to {Wp(luu)}",
             f"If a file with that name already exists, save as N_{to}_2.png, N_{to}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "",
             "TASK: draw ONE part sheet, landscape 1536x1024: the SEPARATE body parts of the creature of image 1, laid out exactly "
             "as on image 2, for a 2D cut-out animation rig.", "",
             PART_RULE, "",
             f"INK OUTLINE: about {net} px thick on this canvas for every outline on this sheet (the parts are drawn enlarged), "
             "closed all the way around each part and lying exactly on the edge of its silhouette.", "",
             "THE PARTS:"] + ds + ["", PART_MAU, PART_FLAT]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        out.append(p)
    # hai tờ "đúng chỗ, đúng cỡ": mảnh của mình (rig gốc không có) lấy thẳng từ concept
    CHUNG = ("TASK: redraw image 1, but keep ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the "
             "SAME SIZE as in image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). "
             "REMOVE everything else and leave pure white (#FFFFFF) there. Every kept part must be ONE COMPLETE CLOSED SHAPE with "
             "the dark-brown ink outline running all the way around it: where a part is hidden behind another part in image 1, "
             "DRAW the hidden portion as described. The kept parts must NOT touch each other. Same wobbly ink line, same colours, "
             "same crayon hatching, same completely flat colouring as image 1. Do not add anything: no shadows, no glow, no "
             "labels.")
    E = {"E1": ("đầu (không hàm dưới) + cụm pha lê trên đệm rêu",
                ["1. THE HEAD WITHOUT ITS LOWER JAW (at about x = 830 to x = 1075, y = 245 to y = 500): the skull and the long "
                 "squared muzzle with the nostril, the bark patches, and the UPPER row of pointed wooden teeth along its lower "
                 "edge. REMOVE the lower jaw completely (everything below the zigzag gap, with its teeth and its round hinge peg) "
                 "and remove the antlers, the ears, the mane and the neck. Complete the head into one closed shape: where the "
                 "antlers and the ears covered its top and back in image 1, draw the rounded top and back of the skull in pale "
                 "wood; its lower edge is the row of upper teeth (four or five pointed teeth pointing down) from the muzzle tip "
                 "back to the cheek, then a smooth rounded jaw corner at the back. NO eyes.",
                 "2. THE CRYSTAL CLUSTER (at about x = 540 to x = 770, y = 450 to y = 670): the four emerald crystals together "
                 "with the moss cushion and the small grey stones, as one group. Remove the body under it and the leaf ear and "
                 "mane behind it; complete the crystals where the ear overlapped them, and complete the underside of the moss "
                 "cushion as one soft rounded bumpy edge."]),
         "E2": ("hàm dưới",
                ["1. THE LOWER JAW ONLY (at about x = 840 to x = 1050, y = 455 to y = 525): the heavy square chin piece with its "
                 "round hinge peg at the back and its row of pointed wooden teeth along its TOP edge (four or five teeth pointing "
                 "up). REMOVE everything else, including the upper head and its upper teeth. Complete the lower jaw into one "
                 "closed shape: draw every one of its teeth as a full pointed triangle (in image 1 they are meshed between the "
                 "upper teeth), and continue its back end a little under where the cheek covered it, rounded. Keep its bark "
                 "patch."])}
    for ma, (vi, giu) in E.items():
        luu = os.path.join(save_dir(), f"M_{ma}.png")
        p = os.path.join(pk(), f"luot_2_manh_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(duyet)}: {CREATURE2}",
             "", f"SAVE: save it as a PNG to {Wp(luu)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "", CHUNG, "", "KEEP:"] + giu + ["", FLAT, BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        out.append(p)
    gd = ["", "## Lượt 2: mảnh dạng 2 (2026-11-12, sau khi người dùng duyệt `L1c_thu.png` → `L1_duyet.png`)", "",
          "Bốn tờ theo khung part (ảnh 1 = concept đã duyệt, ảnh 2 = tờ hướng dẫn `mau/part_<tờ>.png` dựng bằng `HG_DANG=2 py -3 -I "
          f"ArtGen/Spine/huou_go.py nhom_part`; Codex lưu `N_A..D.png` vào `{Wp(save_dir())}`) và hai tờ \"đúng chỗ, đúng cỡ\" chỉ có "
          "ảnh 1 (lưu `M_E1.png`, `M_E2.png`).", "",
          "| Tờ | File prompt | Ảnh hướng dẫn trông như thế nào |", "|---|---|---|",
          f"| A | `{Wp(out[0])}` | Tờ hướng dẫn 1536 × 1024 nền trắng: khối bờm lá đỏ cam mép răng cưa (trái), khúc cổ liền ngực gỗ sáng có "
          "mảng vỏ sẫm (phải) |",
          f"| B | `{Wp(out[1])}` | Thân gỗ có mảng vỏ, bốn nhánh gạc nâu |",
          f"| C | `{Wp(out[2])}` | Hai tai lá vàng, chùm lá đuôi đỏ cam, cán đuôi gỗ, hai lá vàng nhỏ, túm lá chân |",
          f"| D | `{Wp(out[3])}` | Mười khúc chân gỗ có mảng vỏ; bốn khúc dưới có móng đá xám |",
          f"| E1 | `{Wp(out[4])}` | (chỉ concept) giữ đầu không hàm dưới + cụm pha lê trên rêu |",
          f"| E2 | `{Wp(out[5])}` | (chỉ concept) giữ riêng hàm dưới |",
          "", "Kiểm: `HG_DANG=2 huou_go.py cat_part <tờ>` (IoU), `so_part`; E1, E2: mảnh nằm trùng chỗ concept, viền kín, phần khuất đã vẽ."]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2:")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in out:
        print(p)
    return out


if __name__ == "__main__":
    main()
    if os.path.exists(os.path.join(save_dir(), "L1_thu.png")):
        build_sua()
    build_sua2()
    build_part2()
