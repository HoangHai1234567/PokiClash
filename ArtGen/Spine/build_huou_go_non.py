# -*- coding: utf-8 -*-
"""Gói GPT vẽ DẠNG 1 của hươu gỗ (mã huou_go, dạng 1 = khúc gỗ non; con gốc của rig: monster_3304). Tướng thứ 4 đảo Mộc.

Người dùng (2026-11-12, sau khi chọn hướng màu B cho con hươu cổ dài): "lấy con này làm dạng 1" (ảnh chụp monster_3304). Con hươu cổ
dài (monster_3504) thành dạng 2. Màu theo hướng B đã chọn (gỗ bạch dương, lá phong đỏ cam, pha lê lục bảo). Người dùng dặn dạng 2 "bỏ
mắt đi, làm mặt chiến hơn, mồm tách hàm"; dạng 1 chưa dặn mặt → hai kiểu mặt để người dùng chọn (ĐỀ XUẤT của Claude):
  mat       giữ hai ụ mắt của con gốc thành HỐC GỖ rỗng (không con ngươi), nét mày xếch
  khong_mat không mắt: ụ mắt thành mấu cành cụt có vân vòng, mũ vỏ cây sẫm trên trán (như tấm trán dạng 2)
Giữ cách dựng hình của con gốc (khúc gỗ dựng đứng bốn chân, nhìn sang phải, hai cành gạc có lá, ba lá đuôi, mồm trên thân gỗ).

    HG_DANG=1 py -3 -I ArtGen/Spine/huou_go.py bo_cuc
    py -3 -I ArtGen/Spine/build_huou_go_non.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/huou_go_1/luot_1_concept_<kiểu>.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_huou_go import SOFT, FLAT, BG, CACTUS, WORLD_STYLE, Wp, pk, save_dir, mau_dir  # noqa: E402

CODE = "huou_go"
K = 1
DANG2 = os.path.join(save_dir(2), "L1_thu.png")          # hướng màu người dùng đã chọn cho dạng 2 (thân, lá, pha lê; mặt đang sửa)

MAT = {
    "mat": (
        "- THE TWO KNOT STUBS (its \"eyes\"): at the viewer's LEFT side of the face, one short, thick, round BRANCH STUB sticks "
        "out of the log toward the viewer's left (from about x = 635 to x = 765, y = 391 to y = 527), like a sawn-off branch; "
        "its round end (about x = 635 to x = 706, y = 397 to y = 492) is a deep, dark, empty HOLLOW (dark brown #4A3626): a "
        "knothole that reads as an eye socket. NO pupil, NO eyeball, NO shine in it. At the RIGHT edge of the log, partly "
        "behind it, the second stub shows only as a rounded wooden bump (about x = 885 to x = 1005, y = 391 to y = 532), its "
        "hollow turned away. Above the left stub, one short thick ink stroke as an angry BROW, slanting down toward the mouth.",
        "hai ụ mắt là hốc gỗ rỗng (không con ngươi), nét mày xếch"),
    "khong_mat": (
        "- NO EYES AT ALL: no eye, no pupil, no eye socket, no dark hole, no dot that could read as an eye. Where the two "
        "stubs are: at the viewer's LEFT side of the face, one short, thick, round BRANCH STUB sticks out of the log toward "
        "the viewer's left (from about x = 635 to x = 765, y = 391 to y = 527), a sawn-off branch whose round end (about "
        "x = 635 to x = 706, y = 397 to y = 492) is plain pale wood with two thin tree-ring lines; at the RIGHT edge of the "
        "log, partly behind it, a second such stub shows only as a rounded wooden bump (about x = 885 to x = 1005, y = 391 to "
        "y = 532).\n"
        "- BARK CAP: the top of the log (from its top edge at about y = 331 down to a hard, straight lower edge that slants "
        "DOWN toward the viewer's right: at about y = 395 at the left side of the log and about y = 460 at its right side) is "
        "covered by ONE plate of dark brown bark (#7C5C40), like a little helmet pulled low over the face; this slanted edge "
        "gives the face a stern, determined look. A solid plate: no eye opening, no slit.",
        "không mắt: ụ mắt thành mấu cành cụt có vân vòng, mũ vỏ cây sẫm trên trán"),
}


def body(kieu):
    return "\n".join([
        "CREATURE: a young FOREST LOG-FAWN, a small plant-element monster for a monster-collecting game: the YOUNG, first form "
        "of the forest stag-giraffe shown in image 2. It is a little four-legged beast whose head and chest are ONE short, "
        "upright LOG of living pale birch wood (like a walking tree stump), with two small twig antlers that carry autumn "
        "leaves, a tail of three leaves, and four stubby legs with stone hooves. Character: small, chubby and appealing (a "
        "baby creature, chibi proportions), but brave and stubborn, in a battle-ready stance; not a smiling cute mascot, not "
        "scary. Chunky, bold, simple shapes with few details (the way a Pokemon is designed).",
        "Follow the LAYOUT GUIDE (image 1) for WHERE every part is on the canvas, HOW BIG it is and WHICH part overlaps which. "
        "The outlines in the guide are only rough computer blobs: design the real outline of every part yourself as described "
        "below, but keep every part in its place and at its size.",
        "- VIEW: three-quarter view; the creature faces the viewer's RIGHT. The upright log is in front (at the right), a small "
        "round rump with the tail is behind it at the lower left.",
        "- THE LOG (head and chest in one, from about x = 649 to x = 977, y = 331 to y = 809): a tall, rounded, upright log of "
        "pale birch wood, a little wider at the bottom, with a softly rounded top. Smooth carved wood with two or three thin "
        "grain lines. On it, a loose GIRAFFE PATTERN of four or five angular patches of dark brown bark (each an irregular "
        "four- to six-sided plate about 40-70 px), as on the adult form in image 2.",
        MAT[kieu][0],
        "- MOUTH (on the front of the log, to the right of the left stub, about x = 800 to x = 910, y = 455 to y = 510): a "
        "small closed mouth drawn as a bold JAGGED ZIGZAG seam, like a crack where the wood splits into two interlocking jaws: "
        "four or five small pointed wooden teeth meshed together (same pale wood, not white fangs). Level or slightly "
        "downturned at the corners: gritted, determined, no smile. No tongue.",
        "- RUMP (behind the log, at the lower left, from about x = 566 to x = 795, y = 585 to y = 807): a small round hind body "
        "of the same wood with one or two bark patches. On top of the rump, just in front of the tail leaves, at about "
        "x = 640-720, y = 545-625: ONE tiny bud of two small emerald-green CRYSTALS (the taller about 65 px, the darker facet "
        "on its right) sitting in a little tuft of moss: the first sprout of the crystals of the adult form.",
        "- TWIG ANTLERS (dark brown branch wood, each with one thin vein of emerald-green sap): two small Y-shaped twigs "
        "growing from the top of the log. The LEFT one (about x = 566 to x = 781, y = 228 to y = 388) forks up and to the left "
        "and carries one big three-lobed red-orange MAPLE LEAF at its outer tip (about x = 443 to x = 610, y = 251 to y = 438) "
        "and one small yellow leaf at its upper tip (about x = 639 to x = 715, y = 182 to y = 266). The RIGHT one (about "
        "x = 854 to x = 1038, y = 216 to y = 393) forks up and to the right and carries two red-orange leaves (one standing "
        "up at about x = 845-932, y = 143-248, one at its right tip at about x = 987-1111, y = 207-338) and one small yellow "
        "leaf below that (about x = 998-1124, y = 308-373). Each leaf has a centre vein.",
        "- TAIL (behind the rump, at the left): three big leaves fanning out from one point on the rump: one red-orange leaf "
        "standing up (about x = 503 to x = 633, y = 439 to y = 657), one red-orange leaf partly behind the rump (about "
        "x = 593 to x = 746, y = 510 to y = 678), and one yellow leaf pointing to the left (about x = 414 to x = 618, y = 577 "
        "to y = 696). Simple pointed maple-like leaves with a centre vein and two side veins.",
        "- LEGS: four short, stubby legs of the same pale wood, each ending in a small chunky HOOF of grey stone (the lower "
        "third of the leg). Near hind leg at about x = 568-649, y = 710-864; far hind leg at about x = 741-823, y = 721-863; "
        "near front leg at about x = 697-807, y = 721-880, in front of the log; far front leg at about x = 894-1004, "
        "y = 735-866. Legs apart, not crossing.",
        "- Exactly: one log with a zigzag mouth, two stubs, two twig antlers with six leaves in all, one rump with one tiny "
        "crystal bud, three tail leaves, four legs with four stone hooves.",
        "",
        "COLOURS, the same calm, slightly muted palette as the adult form in image 2 (use exactly these, each area one flat "
        "colour): all the wood (log, stubs, rump, legs) pale birch wood (#E2D6BA); the bark patches dark brown bark "
        "(#7C5C40); the twig antlers dark brown branch wood (#7C5C40) with a sap vein of emerald green (#40CE96); the big "
        "leaves autumn maple red-orange (#D66C32) with veins of darker rust red (#A8481E); the small leaves autumn yellow "
        "(#F0AC3E); the crystal bud emerald green (#40CE96) with its darker facet (#1E966E); moss (#629C48); hooves grey "
        "stone (#8C887C); every outline dark-brown ink (#2B2118). Only these colours. NO blue, NO purple, NO pink.",
    ])


FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the whole creature is about 710 px wide (from the yellow tail leaf at about "
         "x = 414 to the right antler leaves at about x = 1124) and about 740 px tall (from the top leaf at about y = 143 to the "
         "hooves at about y = 880).")

POSE = ("POSE (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): standing still on "
        "all four legs in a calm, clean resting pose, exactly as in the guide; the mouth closed. Every part listed above is a "
        "clear, readable shape with its own ink outline (the log, each stub, each twig, each leaf, the rump, each leg). No "
        "falling leaves, no dust, no sparkles, no glow, no motion lines, no ground, no grass, no props.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images (images 2 and 3): drawn by hand on paper with a "
        "dark-brown ink pen (#2B2118), an outline about 7 px thick on this canvas around every big part (log, rump, legs, "
        "stubs, twigs, big leaves), and about 5 px for small details (small leaves, crystal bud, moss, bark patches, the mouth "
        "seam); leaf veins, wood grain and tree rings are thin darker pencil lines about 4 px, not ink; every area coloured "
        "with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the "
        "outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")


def refs(kieu):
    return [
        (os.path.join(mau_dir(K), f"bo_cuc_{kieu}.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature showing where every part "
         "goes on the canvas, how big it is and which part overlaps which (pale wood: the tall upright log, the round stub at "
         "its left and the bump at its right, the small rump at the lower left, the four stubby legs; dark brown: the two "
         "twig antlers and the bark patches" + (", and the bark cap on top of the log" if kieu == "khong_mat" else
                                                ", and the dark hollow of the left stub") +
         "; red-orange and yellow shapes: the leaves on the twigs and the three tail leaves; the zigzag line: the mouth; grey "
         "bands at the feet: stone hooves). Use it for placement, size and overlap only; redraw everything in the hand-drawn "
         "style of the approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): khúc gỗ dựng đứng bốn chân nhìn sang phải, tô phẳng (gỗ sáng: khúc "
         "gỗ, ụ tròn bên trái, u bên phải, mông nhỏ, bốn chân; nâu sẫm: hai cành gạc, mảng vỏ" +
         (", mũ vỏ trên trán" if kieu == "khong_mat" else ", lòng hốc mắt") +
         "; đỏ cam và vàng: lá trên gạc và ba lá đuôi; nét răng cưa: mồm; dải xám: móng đá). Lấy chỗ đặt, cỡ, thứ tự chồng"),
        (DANG2,
         "the ADULT form of the same creature (a forest stag-giraffe), 1536x1024, white background, already approved for its "
         "body, colours and style: take from it the exact pale birch wood with dark bark patches, the red-orange and yellow "
         "maple leaves, the emerald crystals on moss, the grey stone hooves, the dark branch antlers with green sap veins, the "
         "wobbly ink line and the flat crayon colouring. The creature to draw is its small young form: do NOT copy the adult's "
         "long neck, its big mane or its face.",
         "Dạng 2 (hươu gỗ cổ dài, hướng màu B đã chọn; 1536 × 1024, nền trắng): gỗ bạch dương đốm vỏ sẫm, bờm lá phong đỏ cam, pha "
         "lê lục bảo trên rêu, móng đá. Lấy màu, chất gỗ, lá, pha lê, nét; không chép cổ dài, bờm, mặt"),
        (CACTUS,
         "an approved hero of the same game and the same island (a round cactus monster), 1536x1024, white background: match "
         "its wobbly dark-brown pen line, its visible crayon hatching, its completely flat colouring and its bold, simple, "
         "chunky, chibi level of detail. Do NOT copy its species, its design or its colours.",
         "Xương rồng tròn đã duyệt (1536 × 1024, nền trắng): quả cầu lục miệng to nanh kem. Lấy nét bút rung, vân sáp, tô phẳng, mức "
         "chi tiết gọn, tỉ lệ chibi"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu, vân chì sáp"),
    ]


CHECK = [
    "**Khúc gỗ dựng đứng bốn chân nhìn sang phải**, chibi; mông nhỏ và ba lá đuôi ở phía sau bên trái; chân thẳng, tách nhau.",
    "Hai cành gạc chữ Y có sáu lá (đỏ cam + vàng); gỗ bạch dương có **mảng vỏ sẫm kiểu đốm hươu cao cổ**; bốn **móng đá xám**; một nụ "
    "pha lê lục bảo tí hon trên mông.",
    "**Mồm là khe răng cưa** ngậm (không cười). Kiểu `mat`: ụ trái là **hốc gỗ rỗng sẫm** (không con ngươi) + nét mày xếch. Kiểu "
    "`khong_mat`: **không mắt**, ụ trái là mấu cành cụt có vân vòng, **mũ vỏ sẫm** trên trán mép xếch.",
    "Màu đúng dạng 2: gỗ bạch dương, lá phong đỏ cam / vàng, pha lê lục bảo; **không** lam, không tím.",
    "Tô phẳng: **không** bóng, không điểm sáng, pha lê không phát sáng; nền trắng tinh; không lá rơi.",
]

FIX = [
    ("Vẽ mắt có con ngươi, mắt cười", "No eyeballs and no pupils: the left stub is only a dark empty knothole (or, in the no-eye "
                                      "version, plain wood with tree rings). Remove any drawn eye."),
    ("Miệng cười", "The mouth is a closed jagged zigzag seam of small wooden teeth, level, gritted; no smile."),
    ("Thành con hươu cổ dài thu nhỏ", "It is NOT a small copy of the adult: its body is ONE short upright log with the face on "
                                     "it, no neck, no mane; follow image 1."),
    ("Có bóng, mảng sáng tối", "Flat colour only: remove every shadow, highlight, gradient and glow; keep the crayon hatching as "
                               "texture only."),
    ("Bố cục khác sơ đồ", "Follow image 1 exactly for the place and size of every part; the creature faces the viewer's right."),
]


def main():
    os.makedirs(pk(K), exist_ok=True)
    os.makedirs(save_dir(K), exist_ok=True)
    gd = [f"# Gói gửi GPT: `{CODE}` dạng {K} (khúc gỗ non: dạng 1 của hươu gỗ cổ dài, tướng thứ 4 đảo Mộc, tên chưa đặt)", "",
          "Làm 2026-11-12: người dùng chọn `monster_3304` làm con gốc của dạng 1 (dạng 2 = hươu cổ dài, `monster_3504`). Màu theo hướng "
          "B người dùng đã chọn; kiểu mặt là đề xuất của Claude, chờ người dùng chọn. Ghi chú: `ArtGen/Spine/inbox/huou_go_ghichu.md`.", "",
          "Lượt 2 (mảnh) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", ""]
    ra = []
    for kieu in MAT:
        R = refs(kieu)
        missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
        if missing:
            raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
        out = os.path.join(save_dir(K), f"L1_{kieu}.png")
        p = os.path.join(pk(K), f"luot_1_concept_{kieu}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "",
              "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
              "approved hero images.", "", body(kieu), "", FRAME, "", POSE, "", SOFT, LINE, FLAT, BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd += [f"## Kiểu mặt `{kieu}`: {MAT[kieu][1]}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{K}/luot_1_concept_{kieu}.txt` (thêm "
               "`--note \"...\"` để sửa nhanh).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += [""]
    gd += ["Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`HG_DANG=1 py -3 -I ArtGen/Spine/huou_go.py bo_cuc`).",
           "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    open(os.path.join(pk(K), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 1b: người dùng chọn kiểu B (`mat`) 2026-11-12 và dặn:
# "dạng 1 theo hướng B nhưng làm mắt kiểu lác lác ngơ ngơ". Hai cách vẽ con mắt lác để người dùng chọn (đề xuất của Claude).
LAC = {
    "nhan": (
        "1. THE LEFT EYE (the round end of the branch stub at the viewer's left, about x = 622 to x = 730, y = 375 to y = 500): "
        "the dark knothole now holds a big round EYEBALL: a flat cream-white disc (#F4EEDC) that fills most of the hollow, "
        "leaving a thick ring of the dark hollow (#4A3626) visible all around it like an eye socket. On the eyeball ONE small "
        "solid dark-brown PUPIL, a plain round dot about 24 px across, placed far OFF-CENTRE, pushed against the UPPER-LEFT rim "
        "of the eyeball: this eye stares up and outward to the left.\n"
        "2. THE RIGHT EYE: turn the rounded bump at the right edge of the log (about x = 965 to x = 1025, y = 384 to y = 507) "
        "into the second branch stub seen a little from the front, so that its end is visible as a narrower upright oval "
        "(about 50 px wide, 95 px tall) at its right side: the same dark socket ring with a cream-white eyeball in it, and ONE "
        "small dark-brown pupil pushed against the LOWER rim, slightly to the right: this eye stares DOWN. The two pupils "
        "point in clearly different directions: a wall-eyed, dopey, absent-minded look.",
        "tròng mắt kem tròn nằm trong hốc gỗ, con ngươi chấm nhỏ sẫm; hai con ngươi nhìn hai hướng"),
    "dom": (
        "1. THE LEFT EYE (the round end of the branch stub at the viewer's left): keep the deep dark knothole (#4A3626) "
        "exactly as in image 1, and put ONE small round pale PUPIL DOT in it: a plain flat cream-white dot (#F4EEDC) about "
        "26 px across, placed far OFF-CENTRE, pushed against the UPPER-LEFT rim of the hollow: this eye stares up and outward "
        "to the left. No eyeball, no glow: just the one flat dot in the dark hole.\n"
        "2. THE RIGHT EYE: turn the rounded bump at the right edge of the log (about x = 965 to x = 1025, y = 384 to y = 507) "
        "into the second branch stub seen a little from the front, so that its end is visible as a narrower upright dark oval "
        "knothole (about 46 px wide, 90 px tall) at its right side, with ONE small flat cream-white pupil dot (about 22 px) "
        "pushed against its LOWER rim: this eye stares DOWN. The two dots point in clearly different directions: a "
        "wall-eyed, dopey, absent-minded look.",
        "giữ hốc gỗ sẫm, con ngươi là một chấm kem nhỏ trong hốc; hai chấm nhìn hai hướng"),
}


def build_lac():
    nhap = os.path.join(save_dir(K), "L1_mat.png")
    if not os.path.exists(nhap):
        raise SystemExit("thiếu bản nháp " + Wp(nhap))
    ra = []
    gd = ["", "## Lượt 1b: mắt lác (2026-11-12)", "",
          "Người dùng chọn kiểu B (`mat`) và dặn: **làm mắt kiểu lác lác ngơ ngơ**. Lượt này vẽ lại y hệt `L1_mat.png`, chỉ đổi hai con "
          "mắt (hai con ngươi nhìn hai hướng khác nhau, ụ mắt bên phải quay ra cho lộ mắt) và bỏ nét mày xếch. Hai cách vẽ để chọn.", ""]
    for kieu, (en, vi) in LAC.items():
        out = os.path.join(save_dir(K), f"L1b_lac_{kieu}.png")
        p = os.path.join(pk(K), f"luot_1b_lac_{kieu}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(nhap)}: the DRAFT of this creature, 1536x1024, white background: a small forest log-fawn facing the "
             "viewer's right: an upright log of pale birch wood with dark bark patches, a zigzag mouth, a round branch stub at "
             "its left whose end is a dark empty knothole, a rounded bump at its right edge, one slanted angry brow stroke on "
             "its forehead, two twig antlers with green sap veins carrying red-orange and yellow maple leaves, a small rump "
             "with a tiny emerald crystal bud on moss, tail leaves, and four stubby legs with grey stone hooves. This is the "
             "design, the line and the colouring to keep.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as L1b_lac_{kieu}_2.png, L1b_lac_{kieu}_3.png ... in the same folder. "
             "Do not edit, move or delete any other file.", "",
             "TASK: redraw image 1 as ONE picture, changing ONLY the EYES as listed under CHANGE.", "",
             "KEEP IDENTICAL to image 1, in the same place and at the same size (if the new picture were laid over image 1, "
             "everything except the eyes and the brow must coincide): the log with its bark patches and wood grain, the left "
             "branch stub itself (its shape, size and place), the zigzag mouth, both twig antlers with all their leaves, the "
             "rump, the crystal bud and moss, the tail leaves, the four legs and stone hooves, every colour, the wobbly "
             "dark-brown ink line, the crayon hatching, the completely flat colouring, the white background.", "",
             "CHANGE, THE EYES: give the creature two funny, WALL-EYED, DOPEY eyes that look in two different directions (a "
             "goofy, dazed, slightly dim little creature; still appealing, not creepy).",
             en.replace("\n", "\n"),
             "3. REMOVE the slanted angry brow stroke on the forehead of image 1 completely: plain wood there. No brows at all.",
             "No eyelids, no eyelashes, no shine spots, no glow, no blush. Everything else exactly as in image 1.", "", FLAT, BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append(p)
        gd += [f"### Cách `{kieu}`: {vi}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
               f"| 1 | `{Wp(nhap)}` | Bản nháp kiểu B (1536 × 1024, nền trắng): khúc gỗ bạch dương nhìn sang phải, ụ bên trái là hốc gỗ "
               "rỗng sẫm, một nét mày xếch, miệng răng cưa, hai cành gạc lá phong, nụ pha lê trên mông, bốn chân móng đá |", ""]
    gd += ["Kiểm: hai con mắt **nhìn hai hướng khác nhau** (trái: lên – ra ngoài; phải: xuống), vẻ ngơ ngơ; không còn nét mày; mọi thứ "
           "khác trùng bản nháp; tô phẳng, nền trắng."]
    hd = os.path.join(pk(K), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 1b")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in ra:
        print(p)


# ---------------------------------------------------------------- lượt 2: bốn tờ mảnh theo khung part (sau khi người dùng chốt
# mắt lác cách 2: tai_ve/L1_duyet.png = L1b_lac_dom.png, 2026-11-12)
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
PART_MAU = ("COLOURS (exactly as on image 1): pale birch wood #E2D6BA; bark patches and twigs dark brown #7C5C40; sap vein emerald "
            "#40CE96; big leaves maple red-orange #D66C32 with veins of rust red #A8481E; small leaves autumn yellow #F0AC3E with "
            "veins of darker orange #C97E22; eye dark brown #4A3626 with a cream dot #F4EEDC; crystals emerald #40CE96 with the "
            "darker facet #1E966E; moss #629C48; hooves grey stone #8C887C; ink #2B2118.")


def _o(khung, ten):
    v = khung[ten]
    return f"centre at about x = {v['x'] + v['w'] // 2}, y = {v['y'] + v['h'] // 2}, about {v['w']} px wide and {v['h']} px tall"


def build_part():
    """bốn file prompt lượt 2 (tờ A–D): ảnh 1 = concept đã duyệt, ảnh 2 = tờ hướng dẫn theo khung part (HG_DANG=1 huou_go.py nhom_part)."""
    import json
    duyet = os.path.join(save_dir(K), "L1_duyet.png")
    if not os.path.exists(duyet):
        return []
    Kh = {to: json.load(open(os.path.join(mau_dir(K), f"part_{to}.json"), encoding="utf-8")) for to in "ABCD"
          if os.path.exists(os.path.join(mau_dir(K), f"part_{to}.json"))}
    if len(Kh) < 4:
        print("chưa có tờ hướng dẫn: chạy HG_DANG=1 huou_go.py nhom_part")
        return []
    A, B, C, D = Kh["A"], Kh["B"], Kh["C"], Kh["D"]
    noi = {
        "A": ("five parts of the head-body: the log, the rump, two round stubs and one eye", 6,
              ["- THE LOG (left, the biggest part; " + _o(A, "P_tou") + "): the COMPLETE upright log body as if the stubs, the "
               "eyes, the mouth, the antlers and the legs had all been taken off: plain pale birch wood with two or three thin "
               "wavy wood-grain lines running from top to bottom (pencil, about 4 px, not ink) and the dark brown bark patches "
               "exactly where the guide shows them (each an angular plate with a thin ink outline). There is NO face on it: no "
               "eye, no mouth, no hole, no empty patch. A closed ink outline all around the log.",
               "- THE RUMP (top, second from left; " + _o(A, "P_shenti") + "): the small hind body: plain pale wood with one "
               "bark patch where the guide shows it and one or two grain lines; closed ink outline. No crystal, no moss, no tail "
               "on it.",
               "- TWO ROUND STUBS (top right; " + _o(A, "YanR_02") + " and " + _o(A, "YanL_01") + "): each is the round end of a "
               "sawn-off branch: plain pale wood, closed ink outline, ONE thin tree-ring line near its edge. NO eye on them, no "
               "dark hole.",
               "- THE EYE (bottom left; " + _o(A, "YanR_01") + "): one upright oval eye exactly as the big left eye of image 1: "
               "flat dark brown (#4A3626) with a bold ink outline and ONE small round cream dot (#F4EEDC) in its upper left, "
               "where the guide shows it. Nothing else."]),
        "B": ("two twig antlers and five leaves", 6,
              ["- TWO TWIGS (top left; " + _o(B, "JiaoR_01") + " and " + _o(B, "JiaoL_01") + "): each a small forked twig of "
               "dark brown branch wood, exactly its silhouette, with ONE thin emerald-green sap vein (about 6 px) running along "
               "the middle of the stem and into the fork, as on the antlers of image 1; closed ink outline. No leaves on them.",
               "- THE LEAF CLUSTER (top, third; " + _o(B, "JiaoR_03") + "): one red-orange maple leaf with three lobes, exactly "
               "the three-pointed silhouette of the guide; a centre vein in each lobe; closed ink outline.",
               "- TWO YELLOW LEAVES (" + _o(B, "JiaoR_02") + "; and " + _o(B, "JiaoL_03") + "): simple pointed autumn-yellow "
               "leaves, each with a centre vein and two short side veins; closed ink outline.",
               "- TWO RED-ORANGE LEAVES (bottom row; " + _o(B, "JiaoL_02") + "; and " + _o(B, "JiaoL_04") + "): simple pointed "
               "red-orange leaves, each with a centre vein and two or three side veins; closed ink outline.",
               "The veins are thin darker pencil lines (about 4 px), not ink."]),
        "C": ("three big tail leaves, a closed mouth line, an open mouth, a crystal bud and a second eye", 6,
              ["- THREE TAIL LEAVES (top row: " + _o(C, "Weiba_01") + ", red-orange; " + _o(C, "Weiba_02") + ", autumn yellow; "
               + _o(C, "Weiba_03") + ", red-orange): three big simple pointed leaves, each exactly its silhouette, with a centre "
               "vein and three or four side veins (thin darker pencil lines); closed ink outline.",
               "- THE CLOSED MOUTH (top right; " + _o(C, "zuiba") + "): ONLY one bold zigzag ink line (about 8 px), exactly as "
               "the guide shows it: the gritted zigzag mouth of image 1. No fill, no outline around it, nothing else: just the "
               "line on white.",
               "- THE OPEN MOUTH (bottom left; " + _o(C, "mieng_ha") + "): the same mouth wide open: a lens-shaped opening whose "
               "upper and lower edges are rows of pointed teeth (as in the guide), filled flat dark brown (#4A3626), with a bold "
               "ink outline following the teeth. No tongue, nothing inside.",
               "- THE CRYSTAL BUD (bottom, second; " + _o(C, "pha_le") + "): the tiny bud of two emerald crystals on a tuft of "
               "moss, exactly as on the rump of image 1 and as the guide shows it: two chunky pointed prisms (the darker facet "
               "on the right side of each), a low moss cushion with a bumpy scalloped edge under them; ink outlines.",
               "- THE SECOND EYE (bottom, third; " + _o(C, "mat_xa") + "): the end of a branch stub seen at an angle: an upright "
               "oval ring of pale wood with a bold ink outline, and inside it an upright oval eye, flat dark brown (#4A3626) "
               "with an ink outline and ONE small round cream dot (#F4EEDC) near its BOTTOM, where the guide shows it."]),
        "D": ("eight leg parts", 6,
              ["- EIGHT LEG PARTS, each exactly its silhouette, each with a closed ink outline. The four parts that are all "
               "pale wood (" + "; ".join(_o(D, t) for t in ("P_tuiR_H_1", "P_tuiL_H_1", "P_tuiR_Q_1", "P_tuiL_Q_1"))
               + "): plain pale birch wood with one or two short grain lines, nothing else.",
               "- The four parts whose lower part is grey in the guide (" + "; ".join(_o(D, t) for t in
               ("P_tuiR_H_2", "P_tuiL_H_2", "P_tuiR_Q_2", "P_tuiL_Q_2")) + "): the lower leg with its hoof: pale wood above, "
               "a chunky grey STONE hoof below, with one ink line between wood and stone exactly where the guide shows the "
               "border. The stone is flat grey with one tiny chip line.",
               "No patches, no leaves, no moss on any leg part."]),
    }
    out = []
    for to, (gi, net, ds) in noi.items():
        luu = os.path.join(save_dir(K), f"N_{to}.png")
        p = os.path.join(pk(K), f"luot_2_manh_{to}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(duyet)}: the APPROVED creature, 1536x1024, white background: a small forest log-fawn: an upright log "
             "of pale birch wood with dark bark patches, two big dopey dark eyes on round branch stubs, a zigzag mouth, two twig "
             "antlers with green sap veins carrying red-orange and yellow leaves, a small rump with a tiny emerald crystal bud on "
             "moss, tail leaves, four stubby legs with grey stone hooves. It gives the design, the colours, the ink line and the "
             "crayon hatching.",
             f"image 2 = {Wp(os.path.join(mau_dir(K), f'part_{to}.png'))}: PART SHEET GUIDE, 1536x1024, white background: {gi}, "
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
    gd = ["", "## Lượt 2: bốn tờ mảnh theo khung part (2026-11-12, sau khi người dùng chốt mắt lác cách 2 → `L1_duyet.png`)", "",
          "Mỗi tờ một file prompt; ảnh 1 là concept đã duyệt, ảnh 2 là tờ hướng dẫn (hình bóng phẳng từng part đúng khung ảnh vùng "
          "của rig, dựng bằng `HG_DANG=1 py -3 -I ArtGen/Spine/huou_go.py nhom_part`). Codex lưu `N_A.png` … `N_D.png` vào "
          f"`{Wp(save_dir(K))}`.", "",
          "| Tờ | File prompt | Tờ hướng dẫn (1536 × 1024, nền trắng) trông như thế nào |", "|---|---|---|",
          f"| A | `{Wp(out[0])}` | Khúc gỗ lớn có bốn mảng vỏ sẫm (trái), mông nhỏ có một mảng vỏ, hai ụ tròn gỗ, một con mắt bầu dục "
          "nâu sẫm có chấm kem (góc dưới trái) |",
          f"| B | `{Wp(out[1])}` | Hai cành gạc nâu chữ Y, một lá ba thuỳ đỏ cam, hai lá vàng, hai lá đỏ cam |",
          f"| C | `{Wp(out[2])}` | Ba lá đuôi lớn (đỏ cam, vàng, đỏ cam), một nét răng cưa (mồm ngậm), một mồm há hình thấu kính răng cưa "
          "nâu sẫm, nụ hai pha lê lục trên rêu, một ụ mắt bầu dục đứng có chấm kem ở dưới |",
          f"| D | `{Wp(out[3])}` | Tám khúc chân gỗ; bốn khúc dưới có móng đá xám ở đáy |",
          "", "Kiểm (Claude tự làm): `HG_DANG=1 huou_go.py cat_part <tờ>` in IoU từng ô với hình bóng (dưới 0,9 thì gen lại tờ đó), "
          "`so_part` vẽ tờ so (đỏ = thiếu, xanh lá = thừa)."]
    hd = os.path.join(pk(K), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2:")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in out:
        print(p)
    return out


# ---------------------------------------------------------------- lượt 3: cánh cổng rừng của appear (dùng chung hai dạng)
def build_cong():
    duyet = os.path.join(save_dir(K), "L1_duyet.png")
    if not os.path.exists(duyet):
        return
    out = os.path.join(save_dir(K), "cong.png")
    p = os.path.join(pk(K), "luot_3_cong.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(duyet)}: an approved creature of the game (a small forest log-fawn), 1536x1024, white background: use "
         "ONLY its look: the wobbly dark-brown ink pen line, the loose crayon hatching, the completely flat colours, the way its "
         "branch wood, its autumn leaves and its little emerald crystal are drawn. Do NOT draw the creature.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as cong_2.png, cong_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: draw ONE game prop as ONE picture, portrait 1024x1536, pure-white background: a magical FOREST PORTAL, the "
         "teleport gate through which the forest creature of image 1 steps into the world.", "",
         "THE PORTAL: a tall upright OVAL HOOP standing on the ground, seen at a three-quarter angle so that it looks like a "
         "tall narrow ellipse: about 560 px wide and 1380 px tall, centred on the canvas (centre at about x = 512, y = 770; "
         "from about y = 80 at the top to about y = 1460 at the bottom).",
         "- THE HOOP: two living tree branches of dark brown branch wood (#7C5C40), twisted around each other like a rope, bent "
         "into the oval; the band of the hoop is about 75 px thick all the way round, with a closed ink outline on its outer "
         "and inner edge. A thin vein of emerald-green sap (#40CE96) runs along it. Eight to ten small autumn leaves grow from "
         "the hoop pointing OUTWARD (red-orange #D66C32 and yellow #F0AC3E, each about 60-90 px, with a centre vein), spread "
         "evenly around it; at the very top of the hoop sits ONE small emerald-green crystal (two little prisms). No moss, no "
         "green leaves on the hoop: nothing green on the hoop except the thin sap vein and the crystal.",
         "- INSIDE THE HOOP: the whole opening is filled, edge to edge, with a flat magical SWIRL in two greens: a base of "
         "forest green (#2F8F5A) with one big simple spiral band of lighter spring green (#8ED27C) turning three times toward "
         "the centre, like a whirlpool seen from the front, squeezed into the oval. The spiral is drawn with flat colour and "
         "thin darker-green pencil edges, NOT with ink lines. A few small pale-green leaf shapes ride on the spiral. No glow, "
         "no light rays, no sparkles, no transparency, no gradients.",
         "- Nothing else: no ground, no grass, no roots spreading out, no stones, no creature, no shadow.", "",
         "LINE AND COLOUR: the game's hand-drawn look of image 1: dark-brown ink pen outline (#2B2118) about 7 px thick around "
         "the hoop, about 5 px around the leaves and the crystal, visibly wobbly like a real pen; every area coloured with "
         "coloured pencils and wax crayons, the strokes visible as loose diagonal hatching, kept inside the outline.", "",
         FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = ["", "## Lượt 3: cánh cổng rừng (appear, dùng chung hai dạng)", "",
          f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(duyet)}` | Concept dạng 1 đã duyệt (1536 × 1024, nền trắng): khúc gỗ non mắt lác. Chỉ lấy nét, vân sáp, tô phẳng |", "",
          "Kiểm: một vành bầu dục đứng (hai cành cây nâu xoắn vào nhau, lá phong đỏ cam / vàng chĩa ra ngoài, một nụ pha lê trên đỉnh), "
          "lòng cổng là xoáy hai tông lục tô phẳng (không viền mực, không phát sáng); trên vành không có gì màu lục ngoài vân nhựa và "
          "pha lê (mã tách lòng cổng theo màu lục); nền trắng. Claude tách lớp bằng `HG_DANG=1 huou_go.py cat_cong`."]
    hd = os.path.join(pk(K), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 3:")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    print(p)


if __name__ == "__main__":
    main()
    if os.path.exists(os.path.join(save_dir(K), "L1_mat.png")):
        build_lac()
    build_part()
    build_cong()
