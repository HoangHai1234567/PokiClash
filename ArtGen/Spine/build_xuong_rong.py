# -*- coding: utf-8 -*-
"""Gói GPT vẽ xương rồng tròn (mã làm việc xuong_rong, con gốc của rig: monster_3229). Tướng đầu tiên đảo Mộc, DẠNG 1.

Người dùng (2026-11-12): "concept quái vật xương rồng thân tròn không mặt"; dạng 2 to hơn, chiến hơn, form người vẫn vậy. Không dặn
màu, chi tiết: thiết kế dưới đây là ĐỀ XUẤT của Claude, chờ duyệt. Chỉ lấy của con gốc cách dựng (dáng, chỗ đặt, thứ tự chồng của 26
part); hình là của mình: xương rồng thùng tròn lục lam có múi dọc và nốt gai, cái miệng khổng lồ là cả "mặt" (không mắt, không mũi),
lòng miệng đỏ rượu như ruột quả xương rồng, nanh là gai kem to, vành hoa xương rồng hồng trên đỉnh (thay mào đỏ), hai tay nắm tròn
ba gai, năm gai to trên thân, hai chân ngắn.
Không đính ảnh con gốc vào prompt; đính sơ đồ bố cục tự dựng bằng mã (xuong_rong.py bo_cuc).

    py -3 -I ArtGen/Spine/xuong_rong.py bo_cuc
    py -3 -I ArtGen/Spine/build_xuong_rong.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/xuong_rong_1/luot_1_concept.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "xuong_rong"
K = 1
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
WHALE = os.path.join(HERE, "inbox", "ca_voi_1", "tai_ve", "L1_duyet.png")
DRAGON = os.path.join(HERE, "inbox", "rong_vay_1", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def pk(k=K):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def mau_dir(k=K):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "mau")


PALETTE = ("COLOURS, a calm, slightly muted palette (use exactly these, each area one flat colour): the whole skin (ball body, lips, "
           "arms, fists, legs) cactus BLUE-GREEN (#569668); the vertical rib grooves of the cactus drawn as thin lines in darker "
           "green (#2F6248); every thorn, every fang and the small toe nubs warm CREAM (#EEE2BE); the tiny round thorn-buds "
           "(areoles) dotted along the ribs the same cream; the cactus-flower crown on top MAGENTA PINK (#D6548A); the inside of "
           "the mouth deep WINE RED (#682442), like the flesh of a cactus fruit, one flat colour; every outline dark-brown ink "
           "(#2B2118). Only these colours. NO yellow-green, NO red crest, NO blue, NO orange, NO white teeth.")

# A POSE (người dùng 2026-11-12: "tay bên phải có thể làm thõng xuống tức là A pose, không nhất thiết giống con gốc là giơ tay lên")
BACK_ARM = ("- BACK ARM (at the viewer's right, partly BEHIND the body), in an A-POSE, mirroring the front arm: the same kind of "
            "short thick arm coming out from behind the RIGHT side of the ball at about mid height (about x = 1045, y = 440) and "
            "HANGING DOWN and outward to the right, relaxed, NOT raised; its upper part is hidden behind the ball; it ends in a "
            "round FIST ball about 150 px across (centre at about x = 1110, y = 535), fully visible to the right of the ball, "
            "with THREE cream thorns on it (one pointing right at about x = 1190, y = 530, one pointing right-down at about "
            "x = 1180, y = 610, and one pointing down-left at about x = 1050, y = 640, tucked against the edge of the ball).")

FORM = ("CREATURE: a ROUND CACTUS MONSTER of the plant element for a monster-collecting game, first evolution stage: a barrel "
        "cactus shaped like a big BALL that is almost all MOUTH. It has NO FACE: NO eyes, NO eyebrows, NO nose, NO cheeks; the "
        "one giant fanged grin IS its face. Small, chubby and compact (stage 1, a little chibi), but a scrappy, bold, "
        "battle-ready little brawler: a wide cocky grin full of thorn fangs, one fist raised. Appealing, not a smiling cute "
        "mascot and not scary. Everything on it is cactus: smooth cactus skin with ribs, thorns, one flower. NO clothes, NO "
        "pot, NO leaves, NO vines, NO tail, NO horns, NO hair.\n"
        "Follow the LAYOUT GUIDE (image 1) closely for the construction, the placement, the size and the overlap order of every "
        "part listed here:\n"
        "- VIEW: three-quarter front view; the creature is turned slightly toward the viewer's RIGHT.\n"
        "- BODY: one big ball, about 615 px wide and 580 px tall, from about x = 453 to x = 1068 and y = 228 to y = 807: a "
        "barrel cactus. Thin darker-green vertical RIB lines run over the ball like the lines of longitude on a globe (they "
        "meet at the top of the ball under the flower and at the bottom), about six visible, curving with the ball; along "
        "each rib two or three tiny round cream thorn-buds. The ribs are visible on the top, on the left side and at the "
        "bottom of the ball; the mouth covers the rest.\n"
        "- MOUTH: one HUGE open grin taking up most of the front of the ball, centred slightly right of the middle: about "
        "430 px wide and 330 px tall, from about x = 615 to x = 1025 and y = 440 to y = 760; the upper edge of the mouth sags "
        "in the middle and both corners turn UP (a wide bowl-shaped grin). Around the opening runs a smooth LIP band of the "
        "same green skin, about 45 px wide, with an ink line only along the edge of the opening. Inside, flat wine red.\n"
        "- FANGS: the teeth are big cream CACTUS THORNS, irregular and jagged, not a neat row: the UPPER set hangs from "
        "the upper lip as one cream band with four or five pointed fangs of different sizes (two long ones, at about x = 740 "
        "and x = 960, reaching down to about y = 590); the LOWER set rises from the lower lip as one cream band with four "
        "fangs pointing up (the longest at about x = 780 and x = 920). Upper and lower fangs interlock like a zipper with "
        "the wine-red inside showing between them as a zigzag.\n"
        "- FLOWER CROWN: on the top of the ball, shifted to the left (from about x = 525 to x = 920, y = 175 to y = 290), a "
        "crown of about seven short, pointed, slightly ragged cactus-flower PETALS in magenta pink standing up side by side "
        "like a low mohawk and following the curve of the ball; its base is hidden behind the top of the ball.\n"
        "- BODY THORNS: FIVE big cream cone-shaped thorns, each about 90 px long, with a round base and one point, sticking "
        "out of the ball: one on the far left edge pointing left (tip at about x = 425, y = 465, partly behind the ball), one "
        "on the upper left of the front pointing up-left (about x = 595, y = 400), one on the upper right pointing up "
        "(about x = 876, y = 335), one behind the upper right edge pointing up-right (about x = 990, y = 350), and one at the "
        "lower right edge pointing right-down (about x = 1005, y = 675).\n"
        "- FRONT ARM (at the viewer's left, in front of the body): a short thick arm of two round chubby segments coming out "
        "of the left side of the ball at about x = 560, y = 560 and reaching LEFT and slightly down, ending in a round FIST "
        "ball about 180 px across (centre at about x = 430, y = 630) with THREE cream thorns on it like knuckle spikes "
        "(pointing up-left, up and left-down).\n"
        + BACK_ARM + "\n"
        "- LEGS: two very short thick legs under the ball, wide apart: the front one at the lower left (about x = 530-705, "
        "y = 640-850), in front of the ball; the back one at the lower right (about x = 825-1005, y = 680-845), behind the "
        "ball. Each ends in a small round foot with two little cream toe nubs. The feet stand flat at about y = 848.\n"
        "- Exactly one ball body, one mouth, one flower crown, two arms, two legs, five body thorns and three thorns on each "
        "fist.")

FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is visible, "
         "nothing cut by the edges. As in the guide, the whole creature is about 880 px wide (from about x = 330 to x = 1210) and "
         "about 675 px tall (from the petal tips at about y = 175 to the feet at about y = 850).")

POSE = ("POSE (very important: the picture will be cut into separate parts and animated with a 2D skeleton): standing still in "
        "a calm, clean resting pose, exactly as in the guide. Every part is clearly separated by its own closed ink outline: "
        "the ball, each arm segment, each fist, each thorn, each leg, each foot, the flower crown, the upper fangs, the lower "
        "fangs. No dust, no sparkles, no motion lines, no sweat drops, no drool, no ground, no sand, no props.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn curves; the ink line is visibly wobbly and uneven in "
        "thickness like a real pen, not a vector stroke; loose crayon hatching is clearly visible inside every area. The "
        "layout guide is a stiff flat computer diagram with rough, jagged edges and broken outlines: take the construction, the "
        "placement, the proportions and the overlaps from it, never its mechanical line, its jagged edge noise, its cut-off "
        "edges or its empty flat fills. Redraw every shape cleanly, rounded and with character: the thorns as neat fat cones, "
        "the fangs as bold jagged thorn-teeth, the petals as real pointed flower petals with one short centre line each.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images: drawn by hand on paper with a dark-brown ink "
        "pen (#2B2118), an outline about 6 px thick on this canvas for the ball, the mouth, the arms, the fists, the legs, the "
        "fangs and the big thorns and about 4 px for small details (toe nubs, thorn-buds, petal lines); the rib lines are thin "
        "darker-green pencil lines about 4 px, not ink; a closed outline around every part; every area coloured with coloured "
        "pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the outline), kept "
        "inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they do "
        "not model light. No shading, no darker side of the ball, no lighter patches or blotches on the skin, no shadows of "
        "any kind (no cast shadow, no shadow inside the mouth, under the lip, under the figure, on the ground or on the "
        "background), no white highlights or shine spots, no gloss, no reflections, no glow, no rim light, no gradients, no 3D "
        "look. A different tone appears only where the design itself lists a different colour.")

BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no numbers, no frame, no props, no effects "
      "around the creature.")


def refs():
    return [
        (os.path.join(mau_dir(), "bo_cuc.png"),
         "LAYOUT GUIDE, 1536x1024, white background: a flat computer-made diagram of THIS creature showing how it is built, where "
         "every part goes on the canvas, how big it is and which part overlaps which (the green ball body with its rib lines; "
         "the huge grin with the cream thorn fangs and the wine-red inside; the magenta flower crown on the top left; the front "
         "arm with its three-thorn fist at the left; the raised back arm with its three-thorn fist at the upper right; the two "
         "short legs; the five cream thorns on the ball). Follow it closely; redraw everything in the hand-drawn style of the "
         "approved heroes.",
         "Sơ đồ bố cục tự dựng bằng mã (1536 × 1024, nền trắng): quả cầu xương rồng lục lam, miệng cười khổng lồ nanh kem lòng đỏ "
         "rượu, vành hoa hồng trên đỉnh lệch trái, tay trước nắm ba gai bên trái, tay sau giơ lên bên phải, hai chân ngắn, năm gai "
         "kem trên thân. Lấy cách dựng, chỗ đặt, tỉ lệ, thứ tự chồng"),
        (WHALE,
         "an approved hero of the same game (a little whale monster with a huge open mouth, first evolution stage), 1536x1024, "
         "white background: match EXACTLY its wobbly pen line, its visible crayon hatching, its completely flat colouring, and "
         "the chibi-but-fierce level of a stage-1 monster; see how its mouth inside is flat colour and its fangs are simple "
         "cream shapes with an ink outline. Do NOT copy its species, its design or its colours.",
         "Cá voi biến dị dạng 1 đã duyệt (1536 × 1024, nền trắng): cá voi lam nhỏ há miệng to, nanh kem. Lấy nét bút rung, vân sáp, tô "
         "phẳng, mức chibi mà chiến của dạng 1, cách vẽ miệng và nanh"),
        (DRAGON,
         "another approved hero of the same game (a winged sea-serpent), 1536x1024, white background: the same line and flat "
         "crayon colouring, the same calm muted colours. Do NOT copy its species, design or colours.",
         "Rồng vây đã duyệt (1536 × 1024, nền trắng): rồng rắn chàm tím có cánh vây. Lấy nét, tô phẳng, tông màu trầm"),
        (WORLD_STYLE,
         "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured pencil / "
         "wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp"),
    ]


CHECK = [
    "**Không mặt**: không mắt, mày, mũi; cái miệng cười khổng lồ đầy nanh là cả mặt. Thân là **một quả cầu** xương rồng lục lam có "
    "**múi dọc** (nét lục sẫm) và nốt gai kem nhỏ.",
    "Miệng hình bát, hai khoé vểnh lên; **nanh là gai kem to**, lởm chởm, trên dưới cài nhau; lòng miệng **đỏ rượu** phẳng.",
    "**Vành hoa hồng** bảy cánh nhọn trên đỉnh lệch trái (không phải mào đỏ). **Năm gai to** trên thân; mỗi nắm tay **ba gai**.",
    "Tay trước (bên trái người xem) chĩa sang trái; tay sau (bên phải) giơ lên, nấp sau thân; hai chân ngắn dạng rộng, ngón chân kem.",
    "Mỗi bộ phận có viền mực kín riêng. Tô phẳng: **không** bóng, không mảng sáng tối trên thân, không điểm sáng; nền trắng tinh.",
]

FIX = [
    ("Vẽ thêm mắt, mũi, mặt", "It has NO face: remove the eyes, eyebrows and nose. The giant fanged mouth is the only feature."),
    ("Có bóng, mảng sáng tối, loang màu trên thân", "Flat colour only: remove every shadow, highlight, lighter blotch and gradient; "
                                                    "the ball is one even green with thin rib lines; keep the crayon hatching as "
                                                    "texture only."),
    ("Quá dễ thương, cười hiền", "Make it a cocky little brawler: bigger jagged thorn fangs, a wider grin, the fist raised. Not a "
                                 "sweet mascot."),
    ("Quá đáng sợ, quái dị", "Keep it appealing: chubby, compact, clean shapes, no gore, no drool, no cracks."),
    ("Thân không tròn, hoặc thành cây xương rồng có nhánh", "The body is ONE round ball (a barrel cactus), almost all mouth; no "
                                                            "branches, no column, no pot."),
    ("Mào đỏ, tóc, lá", "On top there is only a low crown of magenta-pink pointed cactus-flower petals: no red crest, no hair, no "
                        "leaves."),
    ("Bố cục khác sơ đồ", "Follow image 1 exactly: the front arm at the left reaching left, the back arm raised at the upper right, "
                          "the mouth slightly right of the middle, the flower crown on the top left."),
    ("Răng trắng đều như răng người", "The teeth are big irregular cream cactus THORNS, jagged and interlocking, not neat white teeth."),
]


def main():
    R = refs()
    missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
    os.makedirs(pk(), exist_ok=True)
    os.makedirs(save_dir(), exist_ok=True)
    out = os.path.join(save_dir(), "L1_concept.png")
    p = os.path.join(pk(), "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
    t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not "
          "edit, move or delete any other file.", "",
          "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of the "
          "approved hero images.", "",
          FORM, "", PALETTE, "", FRAME, "", POSE, "", SOFT, LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: `{CODE}` dạng {K} (xương rồng tròn không mặt, tướng đầu tiên đảo Mộc, tên chưa đặt)", "",
          "Làm 2026-11-12: reskin theo khung part của con gốc `monster_3229`; màu và chi tiết là đề xuất của Claude, chờ người dùng "
          "duyệt concept. Ghi chú: `ArtGen/Spine/inbox/xuong_rong_ghichu.md`.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{K}/luot_1_concept.txt` (thêm `--note \"...\"` để "
          "sửa nhanh).", "",
          "Lượt 2 (tờ mảnh theo khung part) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    gd += ["", "Không đính ảnh con gốc của game tham khảo; bố cục đưa bằng sơ đồ tự dựng (`py -3 -I ArtGen/Spine/xuong_rong.py bo_cuc`).",
           "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    # lượt 1b: bản nháp đã có (người dùng xem 2026-11-12, chỉ dặn đổi tay sau sang A pose) → vẽ lại y hệt, chỉ đổi tay sau
    nhap = os.path.join(save_dir(), "L1_concept.png")
    p2 = None
    if os.path.exists(nhap):
        out2 = os.path.join(save_dir(), "L1_apose.png")
        p2 = os.path.join(pk(), "luot_1b_apose.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(nhap)}: the DRAFT of this creature, 1536x1024, white background: a round green cactus-ball monster "
             "with no face, a huge fanged grin with a wine-red inside, a crown of pink flower petals on top, a front arm with a "
             "three-thorn fist at the left, a back arm RAISED at the upper right, two short legs. This is the design, the line "
             "and the colouring to keep.",
             f"image 2 = {Wp(os.path.join(mau_dir(), 'bo_cuc.png'))}: LAYOUT GUIDE, 1536x1024, white background: a flat computer-made "
             "diagram of the same creature in the NEW resting pose. The only difference from image 1 is the BACK ARM at the "
             "viewer's right: it now HANGS DOWN at the right side of the ball instead of being raised. Use it only for the "
             "placement and size of that arm; never copy its mechanical line or its flat fills.",
             "", f"SAVE: save it as a PNG to {Wp(out2)}",
             "If a file with that name already exists, save as L1_apose_2.png, L1_apose_3.png ... in the same folder. Do not "
             "edit, move or delete any other file.", "",
             "TASK: redraw image 1 as ONE picture, changing ONLY the back arm.", "",
             "KEEP IDENTICAL to image 1, in the same place and at the same size (if the new picture were laid over image 1, "
             "everything except the back arm must coincide): the ball body with its rib lines and thorn-buds, the huge grin with "
             "its lip, its cream thorn fangs and its flat wine-red inside, the pink flower-petal crown, the five cream thorns on "
             "the ball, the front arm with its three-thorn fist at the left, both legs and feet, every colour, the wobbly "
             "dark-brown ink line, the crayon hatching, the flat colouring, the white background. Still NO face: no eyes, no nose.",
             "",
             "CHANGE only this: REMOVE the raised back arm at the upper right of image 1 (its two arm segments, its fist and its "
             "three thorns) and draw it in the new position shown in image 2:",
             BACK_ARM,
             "Where the raised arm used to be, complete the outline of the ball and keep the cream thorn that sticks out behind "
             "the upper right edge of the ball (tip at about x = 1030, y = 280) and the cream thorn at the lower right edge of "
             "the ball (about x = 1075, y = 710). The hanging fist must not cover that lower-right thorn completely: the fist "
             "sits above and to the right of it.",
             "", "Exactly two arms in total: the front one at the left, unchanged, and the back one hanging at the right. "
             "Draw the new arm in exactly the same style as the front arm: same green, same 6 px ink outline, same crayon "
             "hatching, same cream thorns.", "", FLAT, BG]
        open(p2, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        gd += ["", "## Lượt 1b: A pose (2026-11-12)", "",
               "Người dùng xem bản nháp `L1_concept.png` và dặn: tay bên phải (tay sau) thõng xuống kiểu A pose, không cần giơ lên như "
               "con gốc. Lượt này vẽ lại y hệt bản nháp, chỉ đổi tay sau.", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p2)}`. Ảnh lưu vào `{Wp(out2)}`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
               f"| 1 | `{Wp(nhap)}` | Bản nháp concept (1536 × 1024, nền trắng): xương rồng cầu lục, miệng cười nanh kem lòng đỏ rượu, vành hoa "
               "hồng, tay sau còn giơ lên bên phải trên |",
               f"| 2 | `{Wp(os.path.join(mau_dir(), 'bo_cuc.png'))}` | Sơ đồ bố cục dáng mới (1536 × 1024, nền trắng): như trên nhưng tay sau "
               "thõng xuống bên phải quả cầu, nắm tay ngang nửa dưới thân |",
               "", "Kiểm: mọi thứ ngoài tay sau trùng bản nháp; tay sau thõng bên phải, nắm tay lộ hẳn ngoài quả cầu, đủ ba gai; hai gai "
               "thân bên phải (trên, dưới) còn nguyên; vẫn không có mặt."]
    # lượt 1c: người dùng xem bản A pose (2026-11-12): "cảm giác như có phần môi ở trên, bỏ line vẽ môi đi" → vẽ lại y hệt, bỏ nét môi
    apose = os.path.join(save_dir(), "L1_apose.png")
    p3 = None
    if os.path.exists(apose):
        out3 = os.path.join(save_dir(), "L1_khong_moi.png")
        p3 = os.path.join(pk(), "luot_1c_bo_moi.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(apose)}: the DRAFT of this creature, 1536x1024, white background: a round green cactus-ball monster "
             "with no face, a huge fanged grin with a wine-red inside, a crown of pink flower petals on top, two arms with "
             "three-thorn fists (one at the left, one hanging at the right), two short legs. Above the mouth there is a long wavy "
             "ink line that makes it look as if the creature had a thick UPPER LIP: that line is the mistake to remove.",
             "", f"SAVE: save it as a PNG to {Wp(out3)}",
             "If a file with that name already exists, save as L1_khong_moi_2.png, L1_khong_moi_3.png ... in the same folder. Do "
             "not edit, move or delete any other file.", "",
             "TASK: redraw image 1 as ONE picture, changing ONLY the lip line.", "",
             "KEEP IDENTICAL to image 1, in the same place and at the same size (if the new picture were laid over image 1, "
             "everything else must coincide): the ball body and its outline, the opening of the mouth with its ink outline, the "
             "cream thorn fangs, the flat wine-red inside, the pink flower-petal crown, the five cream thorns on the ball, both "
             "arms with their fists and thorns, both legs and feet, every colour, the wobbly dark-brown ink line, the crayon "
             "hatching, the flat colouring, the white background. Still NO face: no eyes, no nose.",
             "",
             "CHANGE only this: REMOVE the long wavy ink line that runs ABOVE the mouth, from the base of the cream thorn at the "
             "upper left of the ball (about x = 625, y = 385), dipping and rising across the ball above the mouth (through about "
             "x = 750, y = 345 and x = 880, y = 365), to the right edge of the ball (about x = 1060, y = 400). The creature has "
             "NO LIPS: there is no lip band, no lip outline, no fold of skin around the mouth. The green skin of the ball runs "
             "directly to the edge of the mouth opening; the ONLY line around the mouth is the ink outline of the opening itself.",
             "Where the lip line and the lip band used to be, fill with the same green as the rest of the ball, with the same "
             "crayon hatching, and CONTINUE the thin darker-green vertical rib lines of the ball downward until they reach the "
             "edge of the mouth opening (the ribs that are now cut off at the lip line must run on, curving with the ball), with "
             "one or two of the tiny cream thorn-buds on them. Do the same below and beside the mouth if any lip line is drawn "
             "there. Do not add anything else.", "", FLAT, BG]
        open(p3, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        gd += ["", "## Lượt 1c: bỏ nét môi (2026-11-12)", "",
               "Người dùng xem bản A pose: \"cảm giác như có phần môi ở trên, bỏ line vẽ môi đi\". Lượt này vẽ lại y hệt `L1_apose.png`, chỉ bỏ "
               "nét mực lượn phía trên miệng (nét làm thành vành môi trên); múi dọc của thân chạy tiếp xuống tới mép miệng.", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p3)}`. Ảnh lưu vào `{Wp(out3)}`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
               f"| 1 | `{Wp(apose)}` | Bản A pose (1536 × 1024, nền trắng): xương rồng cầu lục, miệng cười nanh kem lòng đỏ rượu, vành hoa hồng, hai "
               "tay nắm ba gai; phía trên miệng có nét mực lượn làm thành vành môi trên |",
               "", "Kiểm: không còn nét môi, không dải môi; da thân chạy thẳng tới mép lỗ miệng, múi dọc chạy tiếp tới mép miệng; mọi thứ khác "
               "trùng bản A pose; vẫn không có mặt."]
    open(os.path.join(pk(), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    print(p)
    for x in (p2, p3):
        if x:
            print(x)


# ---------------------------------------------------------------- lượt 2: ba tờ mảnh theo khung part (sau khi concept được duyệt)
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
PART_MAU = ("COLOURS (exactly as on image 1): cactus green skin #4CB469; rib lines darker green #195434; thorns, fangs and toe nubs "
            "warm cream #FEECA9; flower petals pink #EF4F91; inside of the mouth wine red #991A46; earth brown #96704A with "
            "darker brown #684A30; ink #2B2118.")


def _o(khung, ten):
    v = khung[ten]
    return f"centre at about x = {v['x'] + v['w'] // 2}, y = {v['y'] + v['h'] // 2}, about {v['w']} px wide and {v['h']} px tall"


def build_part():
    """ba file prompt lượt 2 (tờ A, B, C): ảnh 1 = concept đã duyệt, ảnh 2 = tờ hướng dẫn theo khung part (xuong_rong.py nhom_part)."""
    import json
    duyet = os.path.join(save_dir(), "L1_duyet.png")
    if not os.path.exists(duyet):
        return []
    K_ = {to: json.load(open(os.path.join(mau_dir(), f"part_{to}.json"), encoding="utf-8")) for to in "ABC"
          if os.path.exists(os.path.join(mau_dir(), f"part_{to}.json"))}
    if len(K_) < 3:
        print("chưa có tờ hướng dẫn: chạy xuong_rong.py nhom_part")
        return []
    A, B, C = K_["A"], K_["B"], K_["C"]
    noi = {
        "A": ("three big parts of the head-body: the ball, the skin ring around the mouth, the inside of the mouth", 4,
              ["- THE BALL (left; " + _o(A, "P_shenti") + "): the COMPLETE round barrel-cactus body as if the mouth, the arms, the "
               "legs, the thorns and the flower had all been taken off: one even cactus green ball; thin darker-green RIB lines "
               "(about 4 px, pencil, not ink) run from the top of the ball to the bottom like lines of longitude, curving with "
               "the ball, exactly where the guide shows them; a tiny round cream thorn-bud with a thin ink ring at each dot of "
               "the guide. There is NO mouth, no hole and no empty patch on this ball: the ribs and the green cover all of it. "
               "A closed ink outline all around the ball.",
               "- THE SKIN RING (middle; " + _o(A, "P_zuichun") + "): a ring of the same green skin with a big empty hole (the "
               "mouth opening); the hole stays PURE WHITE. Draw a bold ink line ONLY along the edge of the hole, all the way "
               "around it. The OUTER edge of the ring has NO ink outline at all: there the green, with its crayon hatching, simply "
               "ends at the silhouette edge (this ring will be laid on the ball and must melt into it; it is not a lip). No rib "
               "lines, no dots on the ring.",
               "- THE INSIDE OF THE MOUTH (right; " + _o(A, "P_kouqiang") + "): one flat blob of wine red with crayon hatching, "
               "filling its silhouette. No ink outline needed, no teeth, no tongue, no throat, no darker area."]),
        "B": ("twelve parts: the two rows of fangs, the flower crown, the arm segments, the fists, the legs and the feet", 6,
              ["- UPPER FANGS (top left; " + _o(B, "P_shangya") + "): one cream band with big pointed cactus-thorn fangs hanging "
               "DOWN from it, exactly the silhouette; flat cream; closed ink outline.",
               "- LOWER FANGS (top middle; " + _o(B, "P_xiaya") + "): one cream crescent band with pointed fangs rising UP from "
               "it, exactly the silhouette; flat cream; closed ink outline.",
               "- FLOWER CROWN (second row, left; " + _o(B, "P_toufa") + "): SEVEN pointed pink cactus-flower petals standing "
               "side by side in a fan, as on image 1 and exactly as on the guide (the middle petals in front of the outer ones), "
               "each petal with its own ink outline and one short ink centre line; flat pink; the straight-ish lower edge is the "
               "base of the crown.",
               "- NINE GREEN LIMB PARTS (the remaining parts: " + "; ".join(_o(B, t) for t in ("P_shouL1", "P_shouR2", "P_shouR3"))
               + "; and the others where the guide shows them): each is ONE plain rounded segment of an arm or a leg (upper arm, "
               "forearm, round fist, thigh), exactly its silhouette: flat cactus green, closed ink outline, nothing on it: no "
               "thorns, no ribs, no dots, no fingers.",
               "- TWO FEET (bottom row, the two parts with small cream shapes; " + _o(B, "P_tuiL2") + " and "
               + _o(B, "P_tuiR2") + "): a small green foot with TWO little cream toe nubs at its bottom edge, where the guide "
               "shows them, each nub with a thin ink outline; closed ink outline around the foot."]),
        "C": ("eleven cactus thorns, two longer thorns and one mound of earth", 9,
              ["- ELEVEN THORNS (first and second row): each is ONE cream cone-shaped cactus thorn, a fat cone with a rounded base "
               "and one sharp point, exactly the silhouette, the size and the DIRECTION of the guide (every thorn points a "
               "different way; keep each one as it is). Flat cream, closed ink outline, nothing else on it.",
               "- A LONGER THORN (second row, right; " + _o(C, "gai_vua") + "): the same kind of thorn but longer, lying "
               "horizontally, rounded base at the LEFT, sharp point at the RIGHT; flat cream; closed ink outline.",
               "- A VERY LONG NEEDLE THORN (third row, left; " + _o(C, "gai_dai") + "): the same thorn stretched into a long, "
               "thin, very sharp spike, lying horizontally, rounded base at the LEFT, needle point at the RIGHT; flat cream; "
               "closed ink outline.",
               "- A MOUND OF EARTH (third row, right; " + _o(C, "u_dat") + "): a low heap of freshly broken soil seen from the "
               "side, flat at the bottom, made of a few rounded clods: earth brown with a few short darker-brown crack lines and "
               "two or three tiny clods; closed ink outline; no grass, no stones, no shadow."]),
    }
    out = []
    for to, (gi, net, ds) in noi.items():
        luu = os.path.join(save_dir(), f"N_{to}.png")
        p = os.path.join(pk(), f"luot_2_manh_{to}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(duyet)}: the APPROVED creature, 1536x1024, white background: a round green cactus-ball monster with "
             "no face, a huge fanged grin with a wine-red inside, a crown of seven pink flower petals, two arms with three-thorn "
             "fists, two short legs. It gives the design, the colours, the ink line and the crayon hatching.",
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
             "closed all the way around each part and lying exactly on the edge of its silhouette, except where a part below "
             "says it has no outline.", "",
             "THE PARTS:"] + ds + ["", PART_MAU, PART_FLAT]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        out.append(p)
    gd = ["", "## Lượt 2: ba tờ mảnh theo khung part (2026-11-12, sau khi người dùng duyệt `L1_duyet.png`)", "",
          "Mỗi tờ một file prompt; ảnh 1 là concept đã duyệt, ảnh 2 là tờ hướng dẫn (hình bóng phẳng từng part đúng khung ảnh vùng "
          "của rig, dựng bằng `py -3 -I ArtGen/Spine/xuong_rong.py nhom_part`). Codex lưu `N_A.png`, `N_B.png`, `N_C.png` vào "
          f"`{Wp(save_dir())}`.", "",
          "| Tờ | File prompt | Tờ hướng dẫn (1536 × 1024, nền trắng) trông như thế nào |", "|---|---|---|",
          f"| A | `{Wp(out[0])}` | Ba hình lớn: quả cầu lục có múi dọc và nốt gai (trái), vành da quanh lỗ miệng chỉ viền mực ở mép lỗ "
          "(giữa), khối đỏ rượu lòng miệng (phải) |",
          f"| B | `{Wp(out[1])}` | Mười hai hình: hàm nanh trên, hàm nanh dưới (kem), vành hoa bảy cánh hồng, chín khúc tay chân lục, "
          "trong đó hai bàn chân có ngón kem |",
          f"| C | `{Wp(out[2])}` | Mười một gai nón kem mỗi gai một hướng, một gai dài và một gai kim rất dài nằm ngang chĩa sang phải, "
          "một ụ đất nâu |",
          "", "Kiểm (Claude tự làm): `xuong_rong.py cat_part <tờ>` in IoU từng ô với hình bóng (dưới 0,9 thì gen lại tờ đó), "
          "`xuong_rong.py so_part` vẽ tờ so (đỏ = thiếu, xanh lá = thừa)."]
    hd = os.path.join(pk(), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2:")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in out:
        print(p)
    return out


# ---------------------------------------------------------------- DẠNG 2: concept (người dùng 2026-11-12: "ok ổn rồi, dạng 2 đâu")
# Lời dặn ban đầu: "dạng 2 sẽ to hơn chiến hơn chút nhưng form người vẫn vậy". Cùng rig, cùng khung part: chỉ đổi tỉ lệ vài xương
# (gai dài hơn, nắm tay to hơn, cánh hoa lớn hơn: TI_LE trong xuong_rong_rig.py) và vẽ lại da. Màu, chi tiết dưới đây là ĐỀ XUẤT của
# Claude, chờ duyệt. Sơ đồ bố cục = chính hình dạng 1 đã duyệt dựng trên rig với tỉ lệ dạng 2:
#   XR_DANG=2 XR_MANH=<inbox/xuong_rong_1/manh> py -3 -I ArtGen/Spine/xuong_rong_rig.py bo_cuc <inbox/xuong_rong_2/mau/bo_cuc.png>
BEAST2 = os.path.join(HERE, "inbox", "ca_voi_2", "tai_ve", "L1_duyet.png")


def build_dang2():
    k = 2
    bo = os.path.join(mau_dir(k), "bo_cuc.png")
    d1 = os.path.join(save_dir(1), "L1_duyet.png")
    R = [(bo, "LAYOUT, 1536x1024, white background: the FIRST evolution stage of this creature (a round green cactus-ball "
              "monster with no face, a huge fanged grin, a crown of pink petals, two arms with three-thorn fists, two short "
              "legs) already put into the PROPORTIONS of the second stage: longer thorns, bigger fists, a taller petal crown. "
              "It gives the pose, the construction, the placement and the size of every part of the new picture. Its colours "
              "and its details are still those of stage 1.",
          "Hình dạng 1 đã duyệt dựng trên rig với tỉ lệ dạng 2 (1536 × 1024, nền trắng): gai dài hơn, hai nắm tay to hơn, vành hoa cao "
          "hơn; màu và chi tiết vẫn của dạng 1. Lấy dáng, cách dựng, chỗ đặt, cỡ từng bộ phận"),
         (d1, "the approved FIRST stage of the same creature, 1536x1024, white background: match EXACTLY its wobbly dark-brown "
              "pen line, its visible crayon hatching and its completely flat colouring; the new picture is the same creature "
              "grown up.",
          "Concept dạng 1 đã duyệt (1536 × 1024, nền trắng). Lấy nét bút, vân sáp, tô phẳng; con mới là chính nó lớn lên"),
         (BEAST2, "an approved SECOND-stage hero of the same game (a mutant whale monster), 1536x1024, white background: the "
                  "level of menace and of detail a second stage should have (bigger, sharper fangs, darker colours). Do NOT "
                  "copy its species, design or colours.",
          "Cá voi biến dị dạng 2 đã duyệt (1536 × 1024, nền trắng): mức \"dữ\" và mật độ chi tiết của một dạng 2")]
    missing = [Wp(p) for p, _, _ in R if not os.path.exists(p)]
    if missing:
        print("dạng 2: thiếu ảnh mẫu: " + ", ".join(missing))
        return None
    os.makedirs(pk(k), exist_ok=True)
    os.makedirs(save_dir(k), exist_ok=True)
    out = os.path.join(save_dir(k), "L1_concept.png")
    p = os.path.join(pk(k), "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
    t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not "
          "edit, move or delete any other file.", "",
          "TASK: draw the SECOND EVOLUTION STAGE of the round cactus monster as ONE picture: the same creature grown bigger and "
          "FIERCER, a real brawler now, no longer a cute little one. Same body plan, same pose.", "",
          "KEEP from image 1 (if the new picture were laid over image 1, the construction must coincide): the three-quarter "
          "view turned slightly to the viewer's right; the big ball body in the same place and at the same size; the huge mouth "
          "opening in the same place and at the same size; the petal crown, the two arms (the front one reaching left, the back "
          "one hanging at the right in an A-pose), the fists, the two short legs and EVERY thorn in the same place, at the same "
          "size and pointing the same way as on image 1. Still NO FACE: no eyes, no eyebrows, no nose; the fanged grin is the "
          "whole face. Still no lips and no lip line: the skin of the ball runs directly to the edge of the mouth opening. Exactly "
          "five big thorns on the ball and three on each fist, as on image 1.", "",
          "CHANGE (this is what makes it stage 2):",
          "- SKIN: a deeper, darker cactus green (#2F8A56) instead of the fresh green; the rib lines very dark green (#123F28), "
          "a little bolder (about 5 px).",
          "- SMALL SPIKES: the tiny round thorn-buds along the ribs are now tiny SHARP cream spikes (little cones about 22 px "
          "long, each with an ink outline) pointing outward from the ball, three or four on each rib.",
          "- THORNS: the five big thorns on the ball and the six thorns on the fists are LONG and SHARP as on image 1, warm "
          "cream (#FEECA9) from base to point, ONE flat colour: no coloured tip, no pink, no red on the thorns.",   # người dùng 2026-11-12: "bỏ màu hồng ở gai dạng 2 đi"
          "- FANGS: bigger, longer, sharper and more jagged than on image 1: about five fangs in the upper row and five in the "
          "lower row, two of the upper ones and two of the lower ones long like tusks, interlocking like a bear trap; cream with "
          "ink outline. The inside of the mouth is a darker wine red (#701238), one flat colour.",
          "- PETAL CROWN: the seven petals are longer, narrower and pointed like blades, as tall as on image 1, deep crimson "
          "pink (#D42A6B) with one darker (#8E1840) centre line each: a spiked war crown rather than a soft flower.",
          "- FISTS: big round spiked maces as on image 1 (clearly bigger than in stage 1).",
          "- ATTITUDE: heavier and meaner: the grin wider at the corners and tilted into a snarl. Fierce and battle-ready, "
          "still appealing, not gory, not scary.", "",
          "COLOURS: only the ones listed above (dark cactus green, very dark green ribs, warm cream, crimson "
          "pink petals, dark wine mouth) and the dark-brown ink (#2B2118). No blue, no purple, no orange, no grey, no metal, no "
          "armour, no clothes.", "",
          "CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow; everything visible, "
          "nothing cut by the edges; the creature fills the canvas exactly as on image 1.", "",
          POSE, "", LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = [f"# Gói gửi GPT: `{CODE}` dạng 2 (xương rồng tròn không mặt, to hơn và chiến hơn; cùng rig với dạng 1)", "",
          "Làm 2026-11-12. Lời dặn của người dùng: \"dạng 2 sẽ to hơn chiến hơn chút nhưng form người vẫn vậy\". Màu và chi tiết là đề "
          "xuất của Claude, chờ duyệt concept. Ghi chú: `ArtGen/Spine/inbox/xuong_rong_ghichu.md`.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_2/luot_1_concept.txt`.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    gd += ["", "## Kiểm", "",
           "- Cùng dáng, cùng chỗ đặt với ảnh 1: thân cầu, miệng, vành hoa, hai tay (tay sau thõng A pose), hai chân, đủ 5 gai thân + "
           "3 gai mỗi nắm tay. **Không mặt, không môi.**",
           "- Da lục **sẫm hơn**, múi lục rất sẫm; nốt gai thành **gai nhỏ nhọn**; gai lớn **dài, kem trơn một màu** (không mũi hồng, đỏ).",
           "- Nanh **to, dài, lởm chởm hơn**, có nanh dài như ngà; lòng miệng đỏ rượu sẫm.",
           "- Vành hoa bảy cánh **dài nhọn như lưỡi dao**, hồng đỏ sẫm. Nắm tay to như chùy gai.",
           "- Tô phẳng, không bóng, nền trắng tinh.",
           "", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Vẽ thêm mắt, mũi, môi | `It has NO face and NO lips: remove the eyes, eyebrows, nose and any lip line.` |",
           "| Đổi dáng, đổi chỗ bộ phận | `Follow image 1 exactly for the pose and the placement of every part; only the colours and details change.` |",
           "| Vẫn hiền như dạng 1 | `Make it fiercer: longer jagged fangs, a snarling grin, blade-like petals.` |",
           "| Có bóng, mảng sáng tối | `Flat colour only: remove every shadow, highlight and gradient.` |"]
    # lượt 1b: người dùng xem bản nháp (2026-11-12): "bỏ màu hồng ở gai dạng 2 đi" → vẽ lại y hệt, gai kem trơn
    nhap = os.path.join(save_dir(k), "L1_concept.png")
    if os.path.exists(nhap):
        out2 = os.path.join(save_dir(k), "L1_gai_kem.png")
        p2 = os.path.join(pk(k), "luot_1b_gai_kem.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(nhap)}: the DRAFT of this creature, 1536x1024, white background: a round dark-green cactus-ball "
             "monster with no face, a huge grin full of long cream fangs with a dark wine-red inside, a crown of seven blade-like "
             "crimson-pink petals, two arms with spiked fists, two short legs, small cream spikes on the ball, and long cream "
             "thorns whose POINTS are coloured crimson pink: those coloured thorn tips are the mistake to remove.",
             "", f"SAVE: save it as a PNG to {Wp(out2)}",
             "If a file with that name already exists, save as L1_gai_kem_2.png, L1_gai_kem_3.png ... in the same folder. Do not "
             "edit, move or delete any other file.", "",
             "TASK: redraw image 1 as ONE picture, changing ONLY the colour of the thorn tips.", "",
             "KEEP IDENTICAL to image 1, in the same place and at the same size (if the new picture were laid over image 1, "
             "everything must coincide): the ball body with its rib lines and its small cream spikes, the mouth with its fangs "
             "and its dark wine-red inside, the crimson-pink petal crown, both arms, both fists, both legs and feet, the shape, "
             "the size and the direction of every thorn, every other colour, the wobbly dark-brown ink line, the crayon hatching, "
             "the flat colouring, the white background. Still NO face and NO lip line.",
             "",
             "CHANGE only this: every big thorn (the five on the ball and the three on each fist) is now warm CREAM (#FEECA9) "
             "from its base to its point, ONE flat colour with crayon hatching: REMOVE the crimson-pink tip, and remove the "
             "little ink line that separates the tip from the rest of the thorn. No pink, no red, no second colour on any thorn. "
             "The petal crown and the inside of the mouth keep their colours.", "", FLAT, BG]
        open(p2, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        gd += ["", "## Lượt 1b: gai kem trơn (2026-11-12)", "",
               "Người dùng xem bản nháp `L1_concept.png`: \"bỏ màu hồng ở gai dạng 2 đi\". Lượt này vẽ lại y hệt bản nháp, chỉ bỏ mũi "
               "hồng đỏ của các gai lớn (gai kem một màu từ gốc tới mũi).", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p2)}`. Ảnh lưu vào `{Wp(out2)}`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
               f"| 1 | `{Wp(nhap)}` | Bản nháp dạng 2 (1536 × 1024, nền trắng): xương rồng cầu lục sẫm, nanh dài, vành hoa lưỡi dao hồng đỏ, "
               "gai lớn kem có mũi hồng đỏ |",
               "", "Kiểm: mọi gai lớn kem trơn, không còn mũi hồng và nét ngăn; mọi thứ khác trùng bản nháp."]
        print(p2)
    open(os.path.join(pk(k), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    print(p)
    return p


if __name__ == "__main__":
    main()
    build_part()
    build_dang2()
