"""Gói GPT vẽ concept dòng sò đột biến (tướng thứ 4 đảo Thủy, 2026-11-11, người dùng lên ý tưởng). Mã làm việc: so_gai.

Ý người dùng: con sò đột biến, trong có lưỡi, có mắt ở mai trên; idle như con gốc; đòn thường há hai mai to rồi đớp mạnh; chiêu
mana khép hai mai chu môi nhổ ngọc trai (đạn ngọc trai vẽ riêng); chiêu cuối lè lưỡi lao tới quật vài phát; dạng 2 y vậy nhưng to
hơn, chiến hơn; mỗi dạng <= 0,5 MB. Rig và nhịp học từ một con sò gai của game tham khảo (ghi chú: inbox/so_gai_ghichu.md).
Không đính ảnh con gốc vào prompt; nét vẽ là nét của dự án (bút mực nâu + chì sáp, tô phẳng).

  dạng 1  sò tròn mai lam lục, vành và gai cam san hô, mai dưới trắng xà cừ, hai mắt vàng trên mai trên, lưỡi hồng
  dạng 2  to nặng hơn, mai chàm đậm, vương miện gai, nanh to, có vết nứt, lưỡi dài thò mép

Lượt 1 mỗi dạng: concept trọn con một ảnh, miệng hé (để cắt rời hai mai). Dạng 2 chỉ dựng khi đã có
inbox/so_gai_1/tai_ve/L1_duyet.png. Lượt 2 (tờ mảnh: lưỡi duỗi thẳng, môi chu, ngọc trai, mắt nhắm) viết sau khi duyệt concept.

    py -3 -I ArtGen/Spine/build_so_gai.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/so_gai_1/luot_1_concept.txt [--note "..."]
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/so_gai_2/luot_1_concept.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "so_gai"
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
SHARK = os.path.join(HERE, "inbox", "vay_lam_1", "tai_ve", "L1_lien.png")     # nét, tô sáp phẳng (Thủy, đã duyệt)
DROP = os.path.join(HERE, "inbox", "ti_tach_1", "tai_ve", "L1_duyet.png")     # tướng khởi đầu Thủy vừa duyệt: độ đơn giản, nét rung


def W(p):
    return os.path.normpath(p)


def pk(k):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def chosen(k):
    return os.path.join(save_dir(k), "L1_duyet.png")


# ---------------------------------------------------------------- thiết kế (tiếng Anh, dán vào prompt)
PALETTE1 = ("COLOURS (use exactly these, each area one flat colour): upper shell deep teal (#157A82) with lighter teal ribs "
            "(#2FA9A6); lower shell mother-of-pearl pinkish white (#F1E4EC, never left as bare white paper) with thin lilac rib "
            "lines (#C9B6DA); both wavy rim bands and all spikes coral orange (#F08A4B); barnacles and all fangs cream "
            "(#FBF1D2); inside of the mouth dark plum (#3A2147); tongue raspberry pink (#E0567F) with a darker pink centre "
            "line (#B83A62); eyes golden yellow (#FFD23F) with a black slit pupil; every outline dark-brown ink (#2B2118).")

FORM1 = ("CREATURE: a MUTANT CLAM monster of the water element for a monster-collecting game: a living sea clam that has grown "
         "eyes, fangs and a big tongue. Cute and round but with a tough, ready-to-bite attitude. A creature made only of its "
         "shell, eyes, fangs and tongue: NO arms, NO legs, NO feet, NO tail, NO fins, NO pearl.\n"
         "FORM 1, the first and smallest form:\n"
         "- OVERALL SHAPE: a plump, almost ball-shaped clam, a little wider than tall, made of TWO SHELL HALVES joined by a "
         "hinge at the BACK (the viewer's LEFT): an UPPER SHELL (a dome, the top 55 percent of the height) and a LOWER SHELL "
         "(a round bowl). Three-quarter view turned toward the viewer's RIGHT: the mouth (the opening between the two halves) "
         "faces right.\n"
         "- MOUTH HALF OPEN: at the far left the two rims meet at the hinge; toward the right they spread apart like a "
         "half-open jaw, the gap growing to about 110 px at its widest near the right side. Through the gap we see the dark "
         "plum inside and the tongue. The two shell halves do NOT overlap each other anywhere.\n"
         "- UPPER SHELL: a smooth dome of deep teal with five or six curved RIBS fanning out from the hinge side toward the "
         "rim, every second rib a lighter teal stripe. Along its whole lower edge runs a thick wavy RIM BAND of coral orange "
         "(about 26 px thick, four or five gentle scallops), from the hinge on the left to the front on the right.\n"
         "- EYES, on the upper shell (never on the lower shell): two fierce eyes on the front-right part of the dome, a little "
         "above the rim band. The NEAR eye is the bigger one (about 85 px wide, 60 px tall); the FAR eye is narrower (about "
         "45 px wide), close to the right edge of the dome but fully inside it. Each eye: a golden-yellow shape with a flat "
         "top, as if cut by a heavy lid, a black vertical slit pupil, ONE small white catchlight dot, and a thick ink brow "
         "line on top slanting DOWN toward the front (toward the right for the near eye): an angry, determined glare.\n"
         "- UPPER FANGS: three cream fangs (pointed triangles, about 45 px long) hang DOWN from the underside of the upper rim "
         "band, on its right half. Their tips do NOT reach the lower rim (at least 30 px of dark gap below each tip).\n"
         "- UPPER SPIKES: four coral-orange cone spikes stand on the upper shell: ONE big spike on top, a little right of the "
         "middle, about 110 px tall, and three smaller ones (about 50 px): one at the back-left, one at the upper-left, one at "
         "the right near the far eye. Simple cones, each with its base sitting on the shell.\n"
         "- BARNACLES (the mutation): two small cream barnacle bumps, like tiny volcano cones with a dark hole, on the "
         "back-left of the upper shell.\n"
         "- LOWER SHELL: a round bowl of mother-of-pearl pinkish white with three or four thin lilac rib lines following its "
         "curve. Its top edge is its own thick wavy coral-orange RIM BAND, like a lower lip, mirroring the upper one. Two small "
         "cream fangs (about 30 px) stand UP from the lower rim band near the front; their tips do not reach the upper rim. "
         "Three small coral-orange cone spikes on the OUTSIDE of the bowl: one at the back-left pointing left, one at the "
         "lower-left pointing down-left, one at the lower-right pointing down-right. The very bottom of the bowl is round and "
         "rests on the ground; no spike under it.\n"
         "- INSIDE AND TONGUE: the inside of the mouth is flat dark plum. A thick, fat raspberry-pink TONGUE lies inside on the "
         "lower shell, filling the lower half of the gap; its rounded tip rests just behind the front of the lower rim band "
         "(the tongue does NOT hang out of the mouth); one darker pink centre line along it.")

FRAME1 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
          "visible, nothing cut by the edges. The clam is centred horizontally, about 640 px wide (shell only) and about "
          "620 px tall from the tip of the big spike to the bottom of the bowl; the bottom of the bowl is about 150 px above "
          "the bottom edge of the image.")

PALETTE2 = ("COLOURS (use exactly these, each area one flat colour; the upper shell is now much darker than form 1): upper "
            "shell deep navy indigo (#1D3A6B) with teal ribs (#2FA9A6); lower shell mother-of-pearl pinkish white (#F1E4EC, "
            "never left as bare white paper) with lilac rib lines (#C9B6DA) and a lilac lower third (#C9B6DA); both wavy rim "
            "bands and all spikes coral orange (#F08A4B), the tips of the big spikes dark red (#B8402E); barnacles and all "
            "fangs cream (#FBF1D2); inside of the mouth dark plum (#3A2147); tongue raspberry pink (#E0567F) with a darker "
            "pink centre line (#B83A62); eyes golden yellow (#FFD23F) with a black slit pupil; the scar line dark red "
            "(#B8402E); every outline dark-brown ink (#2B2118).")

FORM2 = ("CREATURE: the GROWN, FIERCER FORM of the mutant clam of image 1 (form 1, approved): the same creature and the same "
         "drawing style, but clearly BIGGER, heavier, darker and more dangerous. A creature made only of its shell, eyes, "
         "fangs and tongue: NO arms, NO legs, NO feet, NO tail, NO fins, NO pearl.\n"
         "FORM 2:\n"
         "- OVERALL SHAPE: the same kind of ball-shaped clam of two shell halves hinged at the BACK (viewer's LEFT), "
         "three-quarter view turned toward the viewer's RIGHT, but more massive: a broader, heavier lower bowl and a taller "
         "upper dome with a slightly angular, armoured outline.\n"
         "- MOUTH HALF OPEN exactly like image 1: rims meeting at the hinge on the left and spreading toward the right, the "
         "gap about 130 px at its widest. The two shell halves do NOT overlap each other anywhere.\n"
         "- UPPER SHELL: deep navy indigo with six or seven curved ribs fanning from the hinge, every second rib a teal "
         "stripe. A thick wavy coral-orange RIM BAND (about 30 px, sharper scallops than form 1) along its whole lower edge. "
         "One dark-red SCAR: a jagged crack line across the upper-left of the dome.\n"
         "- EYES on the upper shell, the same kind as image 1 but narrower and meaner: golden yellow with a black slit pupil, "
         "one small white catchlight dot, cut flat on top by a very thick ink brow slanting down toward the front. The NEAR "
         "eye about 95 px wide and 55 px tall, the FAR eye about 50 px wide, close to the right edge of the dome.\n"
         "- UPPER FANGS: FIVE cream fangs hang DOWN from the underside of the upper rim band on its right half, the two in "
         "the middle long (about 75 px), the others about 45 px. Their tips do NOT reach the lower rim.\n"
         "- CROWN OF SPIKES: SEVEN coral-orange cone spikes on the upper shell: three BIG ones in a row along the top like a "
         "crown (the middle one about 150 px tall, the two beside it about 110 px), with dark-red tips, and four smaller ones "
         "(about 60 px) around the back, the upper-left and the right near the far eye.\n"
         "- BARNACLES: four cream barnacle bumps (tiny volcano cones with a dark hole) on the back-left of the upper shell.\n"
         "- LOWER SHELL: a broad heavy bowl, mother-of-pearl pinkish white on its upper two thirds and lilac on its lower "
         "third, with lilac rib lines. Its top edge is its own thick wavy coral-orange RIM BAND. THREE cream fangs (about "
         "45 px) stand UP from the lower rim band near the front; their tips do not reach the upper rim. FIVE coral-orange "
         "cone spikes on the OUTSIDE of the bowl pointing left, down-left, down-right and right. The very bottom of the bowl "
         "is round and rests on the ground; no spike under it.\n"
         "- INSIDE AND TONGUE: flat dark plum inside. A very thick raspberry-pink TONGUE lies inside on the lower shell, "
         "filling the lower half of the gap; its fat rounded tip pokes OUT over the front of the lower rim band by about "
         "40 px, licking its lip (it does not hang down below the bowl); one darker pink centre line along it.")

FRAME2 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
          "visible, nothing cut by the edges. The clam is centred horizontally, about 800 px wide (shell only) and about "
          "860 px tall from the tip of the tallest spike to the bottom of the bowl; the bottom of the bowl is about 60 px "
          "above the bottom edge of the image.")

POSE = ("VIEW (very important: the picture will be cut into separate parts and animated with a 2D skeleton): three-quarter "
        "view turned toward the viewer's RIGHT, resting still and upright on the round bottom of its bowl. The upper shell "
        "and the lower shell are two clearly separate solid pieces, touching only at the hinge on the left. Spikes of the "
        "lower shell never cross the upper shell, and spikes or fangs of the upper shell never cross the lower shell. No "
        "bubbles, no water, no splashes, no sand, no pearl anywhere.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn curves, a little lopsided like a real sea shell, not "
        "perfect circles; the ink line is visibly wobbly and uneven in thickness like a real pen, not a vector stroke; loose "
        "crayon hatching is clearly visible inside every area.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images: drawn by hand on paper with a dark-brown "
        "ink pen (#2B2118), an outline about 7 px thick on this canvas, the same weight on every edge, a closed outline "
        "around every part; every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal "
        "hatching (strokes thinner than the outline), kept inside the outline. Clean and appealing, few details, neither a "
        "crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, no shadow under the figure, "
        "on the ground or on the background), no white highlights or shine spots, no gloss, no pearly sheen, no wet look, no "
        "reflections, no glow, no rim light, no gradients, no 3D look. The only white allowed is one small catchlight dot in "
        "each eye. A different tone appears only where the design itself lists a different colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no frame, no props, no effects around "
      "the creature.")


def refs_of(k):
    style = [
        (DROP, "an approved hero of the same game (a water-blob creature), 1536x1024, white background: match EXACTLY its "
               "wobbly pen line, its visible crayon hatching and its completely flat colouring. Do NOT copy its species, "
               "design, face or colours.",
         "Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): giọt nước lam mắt bầu dục. Chỉ lấy nét bút rung, vân sáp, tô phẳng"),
        (SHARK, "another approved hero of the same game (a blue shark beast), 1536x1024, white background: see how fangs, "
                "fierce eyes and a determined expression are drawn simply in this style. Do NOT copy its species, design or "
                "colours.",
         "Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): cá mập xanh lam bốn chân. Lấy cách vẽ nanh, mắt dữ, nét mặt quả quyết"),
        (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + "
                      "coloured pencil / wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp"),
    ]
    if k == 1:
        return style
    return [(chosen(1), "FORM 1 of THIS creature (approved), 1536x1024, white background: keep its two-shell construction, its "
                        "half-open mouth, its wavy coral rim bands, its eyes on the upper shell, its fangs, spikes, barnacles "
                        "and tongue, its view and its drawing style. Form 2 is the same creature grown bigger and fiercer, "
                        "with a darker upper shell.",
             "Sò đột biến dạng 1 đã chọn (1536 × 1024, nền trắng): sò tròn mai lam lục, vành cam, mắt vàng, lưỡi hồng, miệng hé")
            ] + style


FORMS = {1: ("sò đột biến dạng 1", FORM1, PALETTE1, FRAME1), 2: ("sò đột biến dạng 2", FORM2, PALETTE2, FRAME2)}

CHECK = {
    1: ["Con sò tròn gần như quả bóng, **hai mai rời nhau**, bản lề bên trái, miệng hé về bên **phải**; hai mai không chồng lên nhau.",
        "Mai trên lam lục có gân quạt, **hai mắt vàng con ngươi dọc** nằm trên mai trên (mắt gần to, mắt xa hẹp), mày mực xếch.",
        "Vành mép hai mai là dải cam lượn sóng; ba nanh kem thả xuống từ mép trên, hai nanh nhỏ dựng lên từ mép dưới, **không chạm mép đối diện**.",
        "Bốn gai cam trên mai trên (một gai to trên đỉnh), ba gai trên mai dưới; hai u hà kem ở lưng.",
        "Trong miệng tím than, **lưỡi hồng mập nằm trong miệng**, không thò ra ngoài.",
        "Tô phẳng: **không** bóng, không điểm sáng (trừ chấm mắt), không ánh xà cừ; viền mực nâu; nền trắng tinh; không có ngọc trai, bong bóng."],
    2: ["Cùng con với dạng 1 nhưng **to, nặng, dữ hơn**: mai trên **chàm đậm**, đường viền góc cạnh hơn, có vết sẹo nứt đỏ sẫm.",
        "**Vương miện ba gai to** trên đỉnh (chóp đỏ sẫm) cùng bốn gai nhỏ; năm gai ở mai dưới.",
        "Năm nanh trên (hai cái giữa dài), ba nanh dưới; không chạm mép đối diện.",
        "Mắt vàng hẹp hơn, mày rất dày; bốn u hà.",
        "Lưỡi rất mập, **chóp thò qua mép dưới** một chút như liếm mép.",
        "Hai mai rời nhau, miệng hé về bên phải; tô phẳng, không bóng, nền trắng tinh."],
}

FIX = [("Có bóng, mảng sáng tối, điểm sáng, ánh xà cừ", "Flat colour only: remove every shadow, highlight, shine spot, pearly "
                                                         "sheen and gradient; keep the crayon hatching as texture only."),
       ("Hai mai dính liền hoặc chồng lên nhau", "The upper shell and the lower shell are two separate solid pieces touching "
                                                "only at the hinge on the left; open the mouth wider so a dark gap separates "
                                                "the two rim bands all the way from the middle to the right."),
       ("Mắt nằm ở mai dưới hoặc trong miệng", "Both eyes sit on the outside of the UPPER shell, above its rim band."),
       ("Nanh, gai chạm hoặc đè lên mai đối diện", "Shorten the fangs and move the spikes so that nothing of one shell touches "
                                                    "or crosses the other shell."),
       ("Quay sang trái hoặc nhìn thẳng", "Turn the clam three-quarters toward the viewer's RIGHT: hinge on the left, mouth "
                                          "opening and both eyes on the right."),
       ("Có tay, chân, ngọc trai, bong bóng, nước", "Remove them: only the two shell halves, eyes, fangs, spikes, barnacles "
                                                     "and the tongue, on pure white."),
       ("Dạng 2 không khác dạng 1 mấy", "Make form 2 much bigger in the frame, with a darker navy upper shell, a crown of three "
                                        "big spikes, longer fangs and a scar.")]


def check(refs):
    missing = [W(p) for p, _, _ in refs if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def build_form(k):
    name, form, palette, frame = FORMS[k]
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
          form, "", palette, "", frame, "", POSE, "", SOFT, LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: dòng `{CODE}` dạng {k} ({name})", "",
          "Tướng thứ 4 đảo Thủy, làm 2026-11-11 theo ý người dùng: sò đột biến có mắt ở mai trên, có lưỡi. Ghi chú thiết kế và "
          "mổ xẻ con gốc: `ArtGen/Spine/inbox/so_gai_ghichu.md`.", "",
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


# ---------------------------------------------------------------- lượt 2: tờ mảnh concept không có (dùng chung hai dạng)
# Hai mai (kèm mắt, nanh, gai, u hà) cắt thẳng từ concept bằng code (so_gai.py). GPT chỉ vẽ: lưỡi duỗi thẳng, lòng miệng, môi chu,
# hai mí mắt, viên ngọc trai. Dạng 2 dùng lại tờ này (co lớn lên; mí đổi màu theo mai dạng 2 bằng code).
PART_SHEET = ("THIS IS A SHEET OF SEPARATE PARTS for a 2D cut-out animation of the clam creature of image 1, NOT a creature and "
              "NOT a scene. Draw ONLY the five loose parts listed below, each one alone on the pure-white page like stickers "
              "laid out on a table, with at least 70 px of pure white between any two parts and between a part and the image "
              "edge. Do NOT draw the clam itself, its shells, spikes or fangs. No labels, no numbers, no arrows, no guide "
              "lines, no grid lines, no frames. Every part has exactly the colours, the wobbly brown ink outline (about 7 px) "
              "and the crayon hatching of image 1, at the same scale as image 1.")

PART_CELLS = ("LAYOUT: canvas 1536 x 1024.\n"
              "- TOP HALF of the page (the band from y = 0 to y = 470), ONE part, centred: the TONGUE, pulled all the way out of "
              "the mouth and laid perfectly STRAIGHT and HORIZONTAL, seen from the side. It is about 1150 px long. Its LEFT end "
              "is the root: a blunt rounded stump about 170 px thick. It keeps almost the same thickness along most of its "
              "length and narrows only a little toward the RIGHT end, which is a fat rounded tip about 120 px thick. Flat "
              "raspberry pink (#E0567F), ONE darker pink centre line (#B83A62) running along the middle from the root and "
              "stopping about 70 px before the tip, brown ink outline all around. No drool, no drops, no wrinkles.\n"
              "- BOTTOM HALF of the page (the band from y = 520 to y = 1024): FOUR parts in a row, each centred in its own cell "
              "of 384 px width, from left to right:\n"
              "  1. MOUTH BACK WALL: the dark inside of the mouth that shows when the clam opens wide. ONE plain half-disc: a "
              "straight flat bottom edge and a round dome top, about 320 px wide and 230 px tall, flat dark plum (#3A2147) with "
              "crayon hatching, brown ink outline all around. Nothing inside it.\n"
              "  2. PUCKERED LIPS: the clam's two coral rim bands squeezed together into a kissing, whistling mouth that sticks "
              "out, in three-quarter view pointing toward the viewer's RIGHT. ONE plump round ring of coral-orange lips "
              "(#F08A4B), like a fat little donut, about 190 px wide and 200 px tall, with five or six short ink wrinkle lines "
              "radiating from the hole, and a small round dark-plum hole (#3A2147, about 50 px) a little right of its centre: "
              "the opening it spits from. Brown ink outline.\n"
              "  3. TWO EYELID PATCHES, side by side with 70 px of white between them, for shutting the two eyes of image 1. "
              "Each is a soft rounded patch of flat deep teal (#157A82, the colour of the upper shell) with crayon hatching and "
              "NO ink outline around the patch. Across each patch ONE thick dark-brown ink stroke (about 10 px, slightly "
              "curved): the squeezed-shut angry eye. LEFT patch (for the near eye): about 150 px wide and 105 px tall, its "
              "stroke runs from the upper-left down to the lower-right. RIGHT patch (for the far eye): about 85 px wide and "
              "95 px tall, its stroke runs from the upper-right down to the lower-left.\n"
              "  4. PEARL: ONE round pearl, the bullet the clam spits, about 150 px across: flat mother-of-pearl pinkish white "
              "(#F1E4EC, never bare white paper) with one curved lilac crescent marking (#C9B6DA) along the inside of its "
              "lower-left edge and one small lilac dot near the upper right, brown ink outline. Perfectly simple.")

PART_STYLE = ("FLAT COLOUR, NO LIGHT, NO SHADOW on every part: each area one even colour, crayon strokes as texture only; no "
              "shading, no highlights, no shine spots, no pearly sheen, no wet look, no gloss, no glow, no gradients, no "
              "shadows, no 3D look. Pure-white background (#FFFFFF) with no paper grain.")

CHECK2 = ["Năm mảnh rời trên nền trắng: nửa trên là **lưỡi duỗi thẳng nằm ngang** (dài ~1150 px, gốc bên trái tù tròn, chóp bên "
          "phải mập tròn, một đường giữa đậm); nửa dưới bốn mảnh xếp hàng.",
          "Lòng miệng: nửa hình tròn tím than trơn, đáy phẳng. Môi chu: vòng môi cam mập như bánh vòng, lỗ tím nhỏ lệch phải, vài "
          "nếp nhăn toả quanh lỗ.",
          "Hai mí: mảng lam lục **không viền mực**, mỗi mảng một nét mực nhắm mắt (trái: chéo xuống phải; phải: chéo xuống trái).",
          "Ngọc trai: viên tròn trắng xà cừ, một vệt lưỡi liềm tím nhạt, viền mực; không bóng sáng.",
          "Không vẽ con sò, không nhãn chữ, không khung ô; tô phẳng, không bóng."]

FIX2 = [("Vẽ cả con sò hoặc mai", "Draw only the five loose parts on pure white; remove the clam and its shells."),
        ("Lưỡi cong, cuộn hoặc ngắn", "The tongue is perfectly straight and horizontal, about 1150 px long, root on the left, "
                                      "rounded tip on the right."),
        ("Mí mắt có viền mực quanh mảng", "The eyelid patches have NO outline around them: only flat teal with one ink stroke "
                                         "across each."),
        ("Có nhãn chữ, số, khung ô", "Remove every label, number, frame and grid line."),
        ("Ngọc trai, môi có bóng sáng", "Flat colour only: no highlights, no shine, no pearly sheen.")]


def build_parts():
    refs = [(chosen(1), "the approved clam creature (form 1), 1536x1024, white background: copy its colours, its wobbly brown "
                        "ink line, its crayon hatching and its scale for every part: the tongue and the dark inside of the "
                        "mouth are visible between its two shell halves, the coral rim bands are its lips, the two golden "
                        "eyes sit on its teal upper shell. Do not redraw the creature.",
             "Sò đột biến dạng 1 đã duyệt (1536 × 1024, nền trắng): sò tròn mai lam lục, vành cam, mắt vàng, lưỡi hồng trong "
             "miệng tím. Lấy màu, nét, vân sáp, tỉ lệ")]
    check(refs)
    out = os.path.join(save_dir(1), "M01.png")
    p = os.path.join(pk(1), "luot_2_manh.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as M01_2.png, M01_3.png ... in the same folder. Do not edit, move "
          "or delete any other file.", "",
          "TASK: draw ONE sheet of five loose parts (tongue, mouth back wall, puckered lips, two eyelid patches, pearl) for "
          "the clam creature of image 1.", "",
          PART_SHEET, "", PART_CELLS, "", PART_STYLE]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: dòng `{CODE}`, lượt 2: tờ mảnh (dùng chung dạng 1 và 2)", "",
          "Hai mai (kèm mắt, nanh, gai, u hà) **không** nhờ GPT vẽ lại: cắt thẳng từ concept đã duyệt bằng "
          "`ArtGen/Spine/so_gai.py` (khớp concept 100 %). GPT chỉ vẽ thứ concept không có đủ: lưỡi duỗi thẳng (để quật), lòng "
          "miệng (lộ ra khi há to), môi chu (chiêu nhổ ngọc), hai mí mắt, viên ngọc trai (đạn của lớp VFX).", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{W(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_1/luot_2_manh.txt` "
          "(thêm `--note \"...\"` để sửa nhanh).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(r)}` | {vi} |" for i, (r, _, vi) in enumerate(refs, 1)]
    gd += ["", "## Kiểm", ""] + [f"- {c}" for c in CHECK2]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX2]
    open(os.path.join(pk(1), "HUONG_DAN_luot_2.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p


# ---------------------------------------------------------------- lượt 2b: HÀM DƯỚI vẽ lại (mỗi dạng một ảnh)
# Người dùng 2026-11-11: "hàm dưới bạn gen lỗi quá, gen lại đi" (lòng bát vẽ bằng mã bị gãy khúc; mép dưới chóp lưỡi dạng 2 vá máy
# bị vỡ). GPT vẽ lại đúng concept nhưng bỏ mai trên và lưỡi, để thấy lòng bát và VÀNH TRONG PHÍA XA như cách con gốc tách hàm dưới.
JAW_ARC = {1: 210, 2: 270}
JAW_KEEP = {1: "two small cream fangs standing up from the near rim, three coral-orange cone spikes on the outside of the bowl, thin "
               "lilac rib lines on the mother-of-pearl bowl",
            2: "three cream fangs standing up from the near rim, five coral-orange cone spikes on the outside of the bowl, lilac "
               "rib lines, the upper two thirds of the bowl mother-of-pearl pinkish white and the lower third lilac"}


def build_jaw(k):
    refs = [(chosen(k), f"the approved clam creature (form {k}), 1536x1024, white background. Its LOWER SHELL is the round bowl at "
                        "the bottom with the wavy coral-orange rim band along its top edge. You will redraw this picture keeping "
                        "ONLY that lower shell, in exactly the same place.",
             f"Sò đột biến dạng {k} đã duyệt (1536 × 1024, nền trắng): lấy đúng mai dưới (cái bát có vành cam), giữ nguyên chỗ, cỡ")]
    check(refs)
    out = os.path.join(save_dir(k), "H01.png")
    p = os.path.join(pk(k), "luot_2_ham_duoi.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as H01_2.png, H01_3.png ... in the same folder. Do not edit, move or "
          "delete any other file.", "",
          "TASK: redraw image 1 with ONLY ITS LOWER SHELL, for a 2D cut-out animation in which the clam opens its mouth wide.", "",
          "REMOVE completely: the whole upper shell (its dome, its rim band, the eyes, the brows, the upper fangs, its spikes, the "
          "barnacles, the scar) and the tongue. Nothing of them may remain.", "",
          "KEEP EXACTLY AS DRAWN in image 1, in the SAME POSITION on the canvas and at the SAME SIZE: the lower shell: the round "
          f"bowl, its outline, its wavy coral-orange NEAR RIM band along the front top edge, {JAW_KEEP[k]}, the small rim knot at "
          "the hinge on the far left, the same colours, the same wobbly brown ink outline and the same crayon hatching. Where the "
          "tongue or the upper shell used to cover the near rim, complete the rim band so it runs unbroken from the hinge on the "
          "left to its front end on the right.", "",
          "ADD what the removed parts were hiding, the INSIDE OF THE BOWL, seen slightly from above:",
          "- The hollow inside of the bowl is flat DARK PLUM (#3A2147). It is completely empty: no tongue, no pearl, no flesh, no "
          "teeth, nothing.",
          "- Behind the hollow runs the FAR RIM of the bowl: the same coral-orange rim band continuing around the back. It starts "
          "at the hinge knot on the far left, rises in ONE big smooth arc, and comes down to meet the front end of the near rim on "
          f"the right. At its highest point, above the middle of the bowl, the far rim is about {JAW_ARC[k]} px above the near rim. "
          "The far rim band is a little thinner than the near rim (about 20 px), gently wavy, with the same brown ink outline on "
          "both of its edges.",
          "- So the opening of the bowl is one big almond / lens shape: near rim in front, far rim behind, dark plum inside. The "
          "lower fangs stand in front of the dark inside.", "",
          "CANVAS: 1536x1024, pure-white background (#FFFFFF), no ground line, no shadow, no text, no labels, no frame, no paper "
          "grain. Nothing else on the page.", "",
          "FLAT COLOUR, NO LIGHT, NO SHADOW: every area one even colour, crayon strokes as texture only; no shading inside the "
          "bowl, no darker depths, no highlights, no pearly sheen, no gloss, no gradients, no 3D look."]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = [f"# Gói gửi GPT: dòng `{CODE}` dạng {k}, lượt 2b: hàm dưới vẽ lại", "",
          "Vẽ lại concept nhưng **chỉ còn mai dưới** (bỏ mai trên, bỏ lưỡi), thấy lòng bát tím và **vành trong phía xa** như cách "
          "con gốc tách hàm dưới. `so_gai.py cat` căn ảnh này trùng mai dưới của concept rồi lấy phần lòng bát + vành xa làm lớp sau "
          "lưỡi, và lấy chỗ vành bị lưỡi che (dạng 2) để vá mặt trước.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{W(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_2_ham_duoi.txt --timeout 420`.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(r)}` | {vi} |" for i, (r, _, vi) in enumerate(refs, 1)]
    gd += ["", "## Kiểm", "",
           "- Chỉ còn mai dưới, **đúng chỗ, đúng cỡ** như trong concept (chồng lên concept thì bát trùng nhau).",
           "- Vành gần liền mạch từ bản lề tới đầu miệng, nanh dưới và gai còn đủ.",
           "- Lòng bát tím than trơn, trống; phía sau là **vành xa** một cung trơn cao, mỏng hơn vành gần.",
           "- Không còn gì của mai trên, không lưỡi; tô phẳng, nền trắng.",
           "", "## GPT vẽ sai thì gửi thêm", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Còn sót mai trên, mắt, lưỡi | `Remove every remaining piece of the upper shell and the tongue; only the lower shell.` |",
           "| Bát bị dời chỗ, đổi cỡ | `Keep the lower shell in exactly the same position and size as in image 1.` |",
           "| Vành xa thấp, dẹt | `Raise the far rim: one big smooth arc, much higher above the near rim in the middle.` |",
           "| Lòng bát có bóng, có thịt, có lưỡi | `The inside is flat dark plum and completely empty.` |"]
    open(os.path.join(pk(k), "HUONG_DAN_luot_2b.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p


if __name__ == "__main__":
    print("dạng 1:", build_form(1))
    if os.path.exists(chosen(1)):
        print("dạng 2:", build_form(2))
        print("lượt 2 (tờ mảnh):", build_parts())
        print("lượt 2b (hàm dưới dạng 1):", build_jaw(1))
        if os.path.exists(chosen(2)):
            print("lượt 2b (hàm dưới dạng 2):", build_jaw(2))
    else:
        print("dạng 2, lượt 2: chưa dựng (chưa có", W(chosen(1)) + ")")
