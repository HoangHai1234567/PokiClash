"""Gói GPT vẽ concept dòng Tí Tách (làm lại 2026-11-11 theo ý người dùng, thay bản tm01 có tay chân của lô cũ).

Ý người dùng: giọt nước mập dáng vòm (kiểu slime nước), mắt là hai hình bầu dục trắng viền lam không tròng; dạng 2 chỉ là giọt
to hơn, nhiều giọt nhỏ bay trên đầu hơn. Rig và nhịp animation học từ một con quái giọt nước của game tham khảo (ghi chú mổ xẻ:
ArtGen/Spine/inbox/ti_tach_ghichu.md). Không đính ảnh con gốc vào prompt; nét vẽ là nét của dự án (bút mực nâu + chì sáp, tô phẳng).

  dạng 1  Tí Tách      giọt vòm nhỏ, 2 giọt con bay trên đầu
  dạng 2  (chưa đặt)   giọt vòm to nặng, 5 giọt con xếp vòng cung như vương miện

Lượt 1 mỗi dạng: concept trọn con một ảnh. Dạng 2 chỉ dựng khi đã có inbox/ti_tach_1/tai_ve/L1_duyet.png (bản dạng 1 được chọn).
Lượt 2: một tờ nét mặt và miệng dùng chung hai dạng (gui_gpt/ti_tach_1/luot_2_net_mat.txt -> tai_ve/M01.png); thân, mắt mở,
vệt má, giọt con cắt thẳng từ concept bằng ti_tach.py.

    py -3 -I ArtGen/Spine/build_ti_tach.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ti_tach_1/luot_1_concept.txt [--note "..."]
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ti_tach_2/luot_1_concept.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "ti_tach"
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
SHARK = os.path.join(HERE, "inbox", "vay_lam_1", "tai_ve", "L1_lien.png")      # nét, tô sáp phẳng (Thủy, đã duyệt)
PENGUIN = os.path.join(HERE, "inbox", "canh_cut_1", "tai_ve", "L1_lien.png")   # chibi tròn, ít chi tiết (Thủy, đã duyệt)


def W(p):
    return os.path.normpath(p)


def pk(k):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def chosen(k):
    """Concept đã chọn của dạng k (chép từ L1_concept*.png)."""
    return os.path.join(save_dir(k), "L1_duyet.png")


# ---------------------------------------------------------------- thiết kế (tiếng Anh, dán vào prompt)
PALETTE = ("COLOURS (use exactly these, each area one flat colour): body bright aqua blue (#35BFE6); the bubble spots inside "
           "the body and inside the beads pale aqua (#9FE3F5); the small floating beads the same bright aqua (#35BFE6); eye "
           "fill very pale ice blue (#EAF8FC, never left as bare white paper); the thick ring around each eye deep ocean blue "
           "(#1B4F8F); the cheek marks medium blue (#2A8FD0); every outer outline dark-brown ink (#2B2118).")

FORM1 = ("CREATURE: a small LIVING BLOB OF WATER, the STARTER creature of the water element in a monster-collecting game: "
         "iconic, appealing, as simple as possible, readable at a tiny size.\n"
         "FORM 1, the first and smallest form:\n"
         "- BODY: ONE plump DOME of water, like a big drop of water resting on a table. The bottom is wide and sits flat on "
         "the ground with softly rounded lower corners; the top is a smooth round dome; the shape is a little lopsided like "
         "soft jelly (slightly fuller at the back, on the viewer's left). It is about 1.4 times WIDER than tall. NO pointed "
         "tip, NO curl, NO arms, NO hands, NO legs, NO feet, NO tail, NO fins, NO ears, NO clothes. Nothing sticks out of the "
         "dome.\n"
         "- EYES (the signature of this creature): two TALL UPRIGHT OVALS, each filled with flat very pale ice blue and "
         "surrounded by a THICK deep-ocean-blue ring (about 10 px). The ovals are completely EMPTY: no pupil, no iris, no "
         "dot, no lash, no brow. A calm, blank, slightly stubborn stare. Because the body is turned three-quarters to the "
         "viewer's RIGHT, both eyes sit on the RIGHT half of the dome at mid height: the NEAR eye is the bigger one (about "
         "65 px wide, 95 px tall), a little right of the centre of the body; the FAR eye is narrower (about 42 px wide, "
         "90 px tall), close to the right edge of the body but fully inside it, tilted very slightly.\n"
         "- CHEEK MARKS: under each eye one short soft horizontal dash of medium blue (about 70 px long under the near eye, "
         "about 35 px under the far eye), a flat crayon mark with no outline.\n"
         "- NO MOUTH, no nose: the face is only the two eyes and the two cheek marks.\n"
         "- BUBBLE SPOTS: inside the body, on the lower-left (back) part, four small round pale-aqua spots of different "
         "sizes (15 to 35 px), flat circles with no outline, like bubbles inside the water. They are markings, not light "
         "reflections.\n"
         "- BEADS: floating in the air just above the top of the dome, a little LEFT of the centre, TWO small round beads of "
         "water that do NOT touch the body and do NOT touch each other: a bigger one about 85 px across, and up and to the "
         "left of it a smaller one about 55 px across. Each bead is a plain circle of bright aqua with the same brown ink "
         "outline and ONE small pale-aqua bubble spot inside. The lower bead hovers about 30 px above the dome.")

FRAME1 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
          "visible, nothing cut by the edges. The dome is centred horizontally, about 600 px wide and about 430 px tall; "
          "its flat bottom is about 190 px above the bottom edge of the image. The beads float above it; at least 120 px of "
          "white above the top bead.")

FORM2 = ("CREATURE: the GROWN FORM of the living water blob of image 1 (form 1, approved): the same creature, the same "
         "design language, the same colours, the same drawing style, but clearly BIGGER, HEAVIER and more imposing. It must "
         "be instantly recognisable as the same line.\n"
         "FORM 2:\n"
         "- BODY: ONE big, heavy DOME of water, the same kind of shape as in image 1 (wide flat bottom with softly rounded "
         "lower corners, smooth round top, slightly lopsided like soft jelly), but taller and more massive: about 1.3 times "
         "wider than tall, with a broad, weighty base. NO pointed tip, NO arms, NO legs, NO feet, NO tail, NO fins, NO ears, "
         "NO clothes. Nothing sticks out of the dome.\n"
         "- EYES: exactly the same kind of eyes as in image 1: two TALL UPRIGHT OVALS filled with flat very pale ice blue, "
         "each surrounded by a THICK deep-ocean-blue ring (about 12 px), completely EMPTY inside (no pupil, no iris, no dot, "
         "no brow). To make the body read as big, the eyes are SMALLER relative to the body than in image 1 and sit a little "
         "below mid height: the NEAR eye about 95 px wide and 135 px tall, a little right of the centre; the FAR eye about "
         "60 px wide and 125 px tall, close to the right edge but fully inside the body. Three-quarter view turned to the "
         "viewer's RIGHT.\n"
         "- CHEEK MARKS: under each eye one short soft horizontal dash of medium blue, a flat crayon mark with no outline.\n"
         "- NO MOUTH, no nose.\n"
         "- BUBBLE SPOTS: inside the body, on the lower-left (back) part, seven small round pale-aqua spots of different "
         "sizes (15 to 45 px), flat circles with no outline.\n"
         "- CROWN OF BEADS: floating in the air above the top of the dome, FIVE round beads of water arranged in a loose "
         "ARC like a crown, centred a little left of the middle of the dome: the middle bead is the biggest (about 110 px "
         "across) and the highest; the beads get smaller toward both ends of the arc (about 80 px, then about 55 px). The "
         "beads do NOT touch the body and do NOT touch each other (at least 20 px of white between them; the lowest beads "
         "hover about 35 px above the dome). Each bead is a plain circle of bright aqua with the same brown ink outline and "
         "ONE small pale-aqua bubble spot inside.")

FRAME2 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
          "visible, nothing cut by the edges. The dome is centred horizontally, about 860 px wide and about 640 px tall; its "
          "flat bottom is about 70 px above the bottom edge of the image. The crown of beads floats above it; at least 50 px "
          "of white above the top bead.")

SOFT = ("SOFT LIVING JELLY, NOT A LOGO: the outline is an organic, slightly irregular hand-drawn curve, NOT a perfect "
        "semicircle. The body is a little lopsided: the top of the dome leans slightly toward the right, the back on the left "
        "is fuller and bulges out a little lower down. The bottom is NOT a straight ruler line: the sides curve inward and "
        "tuck UNDER the body, and the underside is a gentle shallow curve, like a heavy drop of jelly sitting on a table. The "
        "eyes are slightly irregular hand-drawn ovals; the cheek marks are soft loose crayon smudges with ragged ends, not "
        "clean rounded rectangles. The ink line is visibly wobbly and uneven in thickness like a real pen, not a vector "
        "stroke; loose crayon hatching is clearly visible inside the body.")

POSE = ("VIEW (very important: the picture will be cut into separate parts and animated with a 2D skeleton): three-quarter "
        "view turned toward the viewer's RIGHT, resting still and upright on its flat bottom, not squashed, not jumping, not "
        "tilted. The beads are separate shapes with clear white space all around each of them. No splashes, no drips, no "
        "extra drops, no puddle, no spray anywhere.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images: drawn by hand on paper with a dark-brown "
        "ink pen (#2B2118), an outline about 7 px thick on this canvas, the same weight on every edge, slightly wobbly like "
        "a real pen, a closed outline around the dome and around each bead; every area coloured with coloured pencils and "
        "wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the outline), kept inside the "
        "outline. Clean and appealing, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. The water is drawn as an OPAQUE flat aqua shape: no shading, no darker side, no darker rim, no "
        "shadows of any kind (no cast shadow, no shadow under the figure, on the ground or on the background), no white "
        "highlights or shine spots, no gloss, no glassy or transparent jelly look, no reflections, no glow, no rim light, no "
        "gradients, no 3D look. A different tone appears only where the design itself lists a different colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no frame, no props, no effects around "
      "the creature.")


def refs_of(k):
    style = [
        (SHARK, "an approved hero of the same game (a blue shark beast), 1536x1024, white background: match EXACTLY its "
                "pen line, crayon texture and flat colouring. Do NOT copy its species, design, face or colours.",
         "Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): cá mập xanh lam bốn chân. Chỉ lấy nét bút, vân sáp, cách tô phẳng"),
        (PENGUIN, "another approved hero of the same game (a chibi penguin), 1536x1024, white background: see how simple, "
                  "round and readable a first form is in this style. Do NOT copy its species, design, face or props.",
         "Cánh Cụt dạng 1 đã duyệt (1536 × 1024, nền trắng): chim cánh cụt chibi. Lấy độ đơn giản, tròn trịa của dạng 1"),
        (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + "
                      "coloured pencil / wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp"),
    ]
    if k == 1:
        return style
    return [(chosen(1), "FORM 1 of THIS creature (approved), 1536x1024, white background: keep its body shape language, its "
                        "empty oval eyes with the thick blue ring, its cheek marks, its bubble spots, its floating beads, "
                        "its colours and its drawing style. Form 2 is the same creature grown big.",
             "Tí Tách dạng 1 đã chọn (1536 × 1024, nền trắng): giọt vòm lam, mắt bầu dục trắng viền lam, 2 giọt con trên đầu")
            ] + style


FORMS = {1: ("Tí Tách", FORM1, FRAME1), 2: ("dạng 2 (chưa đặt tên)", FORM2, FRAME2)}

CHECK = {
    1: ["Một khối nước **dáng vòm** đáy bằng, rộng hơn cao (~1,4 lần), hơi lệch như thạch mềm; không chóp nhọn, không tay chân đuôi.",
        "Mắt là **hai hình bầu dục đứng, trắng lam nhạt, viền lam đậm dày, trống trơn** (không tròng, không chấm); mắt gần to, "
        "mắt xa hẹp sát mép phải; dưới mỗi mắt một vệt má lam. **Không có miệng.**",
        "**Hai giọt con** tròn bay trên đỉnh, lệch trái, không chạm thân, không chạm nhau.",
        "Vài đốm bong bóng lam nhạt bên trong thân, phía dưới trái.",
        "Nhìn nghiêng 3/4 sang **phải**; không nước toé, không vũng nước.",
        "Tô phẳng: **không** bóng, không điểm sáng, không kiểu thạch trong suốt bóng loáng; viền mực nâu; nền trắng tinh."],
    2: ["Cùng con với dạng 1 nhưng **to, nặng hơn hẳn**: vòm cao hơn (rộng ~1,3 lần cao), đáy bè; chiếm gần hết khung.",
        "Mắt cùng kiểu dạng 1 nhưng **nhỏ hơn so với thân** và đặt thấp hơn một chút (để thân trông to).",
        "**Năm giọt con** xếp vòng cung như vương miện trên đỉnh, giọt giữa to nhất; không chạm thân, không chạm nhau.",
        "Nhiều đốm bong bóng hơn (khoảng bảy) bên trong thân.",
        "Nhìn nghiêng 3/4 sang **phải**; không tay chân, không miệng, không nước toé.",
        "Tô phẳng: không bóng, không điểm sáng, không bóng loáng; viền mực nâu; nền trắng tinh."],
}

FIX = [("Có bóng, mảng sáng tối, điểm sáng trắng trên thân", "Flat colour only: remove every shadow, highlight, shine spot, "
                                                              "darker rim and gradient; keep the crayon hatching as texture "
                                                              "only."),
       ("Thành thạch trong suốt bóng loáng", "The body is an opaque flat aqua colour with crayon texture, not glassy jelly: "
                                            "no reflections, no transparency, no shine."),
       ("Mắt có tròng, có chấm sáng, có mày", "The eyes are completely empty ovals: very pale ice-blue fill and a thick deep "
                                             "blue ring, nothing inside, no pupils, no dots, no brows."),
       ("Có miệng", "Remove the mouth: the face is only the two oval eyes and the two cheek marks."),
       ("Quay sang trái hoặc nhìn thẳng", "Turn the creature three-quarters toward the viewer's RIGHT: both eyes on the right "
                                          "half of the dome, the far eye narrower and close to the right edge."),
       ("Có chóp nhọn, tay, chân, đuôi", "The body is only a smooth dome: remove the tip, arms, legs, feet and tail."),
       ("Giọt con dính thân hoặc dính nhau, có nước toé", "The beads float clear of the body and of each other with white "
                                                           "space around each; remove every splash, drip and extra drop."),
       ("Dạng 2 không to hơn hẳn dạng 1", "Make the dome much bigger and heavier in the frame (about 860 px wide, 640 px "
                                          "tall) and the eyes smaller relative to the body.")]


def check(refs):
    missing = [W(p) for p, _, _ in refs if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def build_form(k):
    name, form, frame = FORMS[k]
    refs = refs_of(k)
    check(refs)
    os.makedirs(pk(k), exist_ok=True)
    os.makedirs(save_dir(k), exist_ok=True)
    out = os.path.join(save_dir(k), "L1_concept.png")
    p = os.path.join(pk(k), "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do "
          "not edit, move or delete any other file.", "",
          "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose, in the hand-drawn style of "
          "the approved hero images.", "",
          form, "", SOFT, "", PALETTE, "", frame, "", POSE, "", LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: dòng `{CODE}` dạng {k} ({name})", "",
          "Tướng khởi đầu hệ Thủy (ải 1 đảo Thủy), làm lại 2026-11-11 theo ý người dùng: giọt nước dáng vòm, mắt bầu dục "
          "trắng viền lam. Ghi chú thiết kế và mổ xẻ con gốc: `ArtGen/Spine/inbox/ti_tach_ghichu.md`.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{W(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_1_concept.txt` "
          "(thêm `--note \"...\"` để sửa nhanh).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(r)}` | {vi} |" for i, (r, _, vi) in enumerate(refs, 1)]
    gd += ["", "Không đính ảnh con gốc của game tham khảo; thiết kế chỉ tả bằng lời.", "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK[k]]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    open(os.path.join(pk(k), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p


# ---------------------------------------------------------------- lượt 2: tờ nét mặt và miệng (dùng chung hai dạng)
# Thân, mắt mở, vệt má, giọt con cắt thẳng từ concept bằng code (ti_tach.py); GPT chỉ vẽ thứ concept không có.
FACE_SHEET = ("THIS IS A SHEET OF SEPARATE FACE PARTS for a 2D cut-out animation, NOT a creature and NOT a scene. The creature of "
              "image 1 has a face made only of two empty oval eyes; the game swaps these eyes for other expressions and adds "
              "a mouth when it spits water. Draw ONLY the loose face parts listed below, each one alone on the pure-white "
              "page like stickers laid out on a table. Do NOT draw the body, the blue body colour, the cheek marks, the "
              "beads, or any background shape behind the parts. No labels, no numbers, no arrows, no guide lines, no grid "
              "lines, no frames.")

FACE_STYLE = ("STYLE OF EVERY PART: exactly the look of the eyes in image 1: drawn by hand with a thick DEEP OCEAN BLUE crayon "
              "line (#1B4F8F), about 12 px thick, round ends, slightly wobbly and uneven like a real crayon, NOT a vector "
              "stroke. Flat colours only: no shading, no highlights, no shine, no glow, no gradients, no shadows. The only "
              "colours on the whole sheet are deep ocean blue (#1B4F8F), very pale ice blue (#EAF8FC), dark navy (#123466) "
              "and medium blue (#2A8FD0), on pure white (#FFFFFF). No brown ink outline on these parts.")

FACE_PAIR = ("EYE PAIRS: each eye expression is a PAIR drawn side by side exactly as the two eyes sit in image 1 (three-quarter "
             "view turned to the viewer's right): the LEFT symbol of the pair replaces the NEAR eye and is the bigger one "
             "(it fits a box about 125 px wide and 160 px tall); the RIGHT symbol replaces the FAR eye and is narrower (it "
             "fits a box about 80 px wide and 145 px tall); the centres of the two symbols are about 205 px apart and at "
             "the same height. Nothing else is drawn between or around them.")

FACE_CELLS = ("LAYOUT: canvas 1536 x 1024, an invisible 3 x 2 grid of 512 x 512 px cells, ONE group centred in each cell, at "
              "least 90 px of pure white between a group and the cell borders:\n"
              "- top-left cell, SQUINT pair (pain, effort): two chevrons pointing at each other like '> <': the near symbol "
              "is a '>' (two thick strokes meeting in a point on the RIGHT), the far symbol is a '<' (two thick strokes "
              "meeting in a point on the LEFT). Just the strokes, no fill, no oval.\n"
              "- top-middle cell, DIZZY pair: the same two ovals as the open eyes of image 1 (thick deep-blue ring, very pale "
              "ice-blue fill), and inside each oval ONE deep-blue spiral line making about two and a half turns from the "
              "centre out to the ring, stroke about 8 px.\n"
              "- top-right cell, HAPPY CLOSED pair: two upward arches like '^ ^' but rounded, each ONE thick curved stroke, "
              "open at the bottom. Just the strokes, no fill.\n"
              "- bottom-left cell, BLINK pair (calm closed eyes): two gentle downward curves like closed eyelids, each ONE "
              "thick stroke shaped like a shallow smile '‿', the near one about 115 px wide, the far one about 70 px wide. "
              "Just the strokes, no fill.\n"
              "- bottom-middle cell, SMALL MOUTH (alone, not a pair): a small round 'o' mouth: a thick deep-blue ring about "
              "60 px wide and 66 px tall, filled with flat dark navy (#123466). Nothing inside.\n"
              "- bottom-right cell, BIG OPEN MOUTH (alone, not a pair), the mouth wide open to spit a jet of water toward the "
              "viewer's right: an upright rounded egg-shaped opening about 150 px wide and 185 px tall, a thick deep-blue "
              "ring (about 13 px), filled with flat dark navy (#123466); resting on the bottom inside edge a small rounded "
              "tongue bump of flat medium blue (#2A8FD0), about 80 px wide and 45 px tall, with a thin deep-blue line along "
              "its top. No teeth, no lips, no drool, no water.")

CHECK2 = ["Sáu nhóm rời trên nền trắng, mỗi ô một nhóm, không chạm nhau; **không** vẽ thân, không vệt má, không nhãn chữ.",
          "Bốn cặp mắt: `> <` · bầu dục có xoáy · `^ ^` bo tròn · hai nét cong nhắm mắt. Trong mỗi cặp, **bên trái to hơn** "
          "(mắt gần), bên phải hẹp hơn (mắt xa), tâm cách nhau khoảng 205 px.",
          "Hai miệng: chữ `o` nhỏ lòng xanh chàm; miệng há to hình trứng đứng, viền lam dày, lòng xanh chàm, có u lưỡi lam.",
          "Nét lam đậm dày, hơi rung như sáp, cùng kiểu viền mắt trong concept; tô phẳng, không bóng, không điểm sáng."]

FIX2 = [("Vẽ cả thân hoặc nền lam sau các mảnh", "Draw only the loose face parts on pure white: remove the body, the blue "
                                                 "background shapes and the cheek marks."),
        ("Có nhãn chữ, số, khung ô", "Remove every label, number, frame and grid line; only the six groups on pure white."),
        ("Hai mắt trong cặp bằng nhau", "In every pair the LEFT symbol is the bigger near eye (about 125 x 160 px) and the "
                                        "RIGHT symbol is the narrower far eye (about 80 x 145 px)."),
        ("Nét mảnh hoặc đều như vector", "Thicker strokes, about 12 px, slightly wobbly like a wax crayon, round ends."),
        ("Miệng có răng, có bóng, có điểm sáng", "The mouth is a flat dark-navy opening with a thick deep-blue ring and a "
                                                 "small flat blue tongue bump: no teeth, no shading, no shine.")]


def build_faces():
    """Tờ nét mặt và miệng: một tờ dùng cho cả hai dạng (cỡ mắt hai concept chênh ~1,1 lần, rig tự co)."""
    refs = [(chosen(1), "the approved creature (form 1), 1536x1024, white background: look ONLY at its two eyes: the thick "
                        "deep-blue crayon ring, the very pale ice-blue fill, their sizes and how far apart they sit. The "
                        "new parts must look as if drawn by the same hand with the same crayon, at the same scale. Do not "
                        "redraw the creature.",
             "Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): giọt vòm lam, hai mắt bầu dục trắng viền lam. Chỉ lấy kiểu "
             "nét, cỡ và khoảng cách hai mắt")]
    check(refs)
    out = os.path.join(save_dir(1), "M01.png")
    p = os.path.join(pk(1), "luot_2_net_mat.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as M01_2.png, M01_3.png ... in the same folder. Do not edit, move "
          "or delete any other file.", "",
          "TASK: draw ONE sheet of loose face parts (four eye expressions and two mouths) for the creature of image 1.", "",
          FACE_SHEET, "", FACE_PAIR, "", FACE_CELLS, "", FACE_STYLE]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: dòng `{CODE}`, lượt 2: tờ nét mặt và miệng (dùng chung dạng 1 và 2)", "",
          "Thân, mắt mở, vệt má và các giọt con **không** nhờ GPT vẽ lại: cắt thẳng từ concept đã duyệt bằng "
          "`ArtGen/Spine/ti_tach.py` (khớp concept 100 %). GPT chỉ vẽ thứ concept không có: mắt lúc trúng đòn, choáng, "
          "cười, chớp, và miệng há để bắn nước.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{W(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_1/luot_2_net_mat.txt` "
          "(thêm `--note \"...\"` để sửa nhanh).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(r)}` | {vi} |" for i, (r, _, vi) in enumerate(refs, 1)]
    gd += ["", "## Kiểm", ""] + [f"- {c}" for c in CHECK2]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX2]
    open(os.path.join(pk(1), "HUONG_DAN_luot_2.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p


if __name__ == "__main__":
    print("dạng 1:", build_form(1))
    if os.path.exists(chosen(1)):
        print("dạng 2:", build_form(2))
        print("lượt 2 (tờ nét mặt):", build_faces())
    else:
        print("dạng 2, lượt 2: chưa dựng (chưa có", W(chosen(1)) + ")")
