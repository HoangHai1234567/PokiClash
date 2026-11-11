# -*- coding: utf-8 -*-
"""Gói GPT vẽ concept dòng tm09 "Hàn Ngạc" (lô 10 tướng mới đảo Thủy, 2026-11-11; đặc tả ArtGen/Spine/quai/DAC_TA_LO_THUY.md).

Con gốc tham khảo: monster_3281 (thú bò sát bốn chân, sừng cong lớn, hàm to, pha lê ở đuôi) = DẠNG 2 của dòng. Thiết kế của
mình khác hẳn, chỉ giữ chủ đề "thú bò sát bốn chân thấp người, sừng cong, hàm khỏe, pha lê ở đuôi" và đổi hẳn sang hệ Thủy:
cá sấu băng vực sâu. Dạng 2 vẽ trước (ải 60, legend, ngay trước boss cuối), dạng 1 (chibi, con non) vẽ sau khi dạng 2 được
chọn, đính concept dạng 2 làm ảnh mẫu. Không đính ảnh con gốc / ảnh chụp trang xem (luật mục 3 đặc tả).

    py -3 -I ArtGen/Spine/build_tm09.py                 dựng gui_gpt/tm09_2/luot_1_concept.txt (+ tm09_1 khi đã có L1_duyet của dạng 2)
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm09_2/luot_1_concept.txt
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm09_1/luot_1_concept.txt
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm09"


def W(p):
    return os.path.normpath(p)


def pk(k):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def duyet(k):
    return os.path.join(save_dir(k), "L1_duyet.png")


WORLD_STYLE = W(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
HAI_LONG = os.path.join(HERE, "inbox", "hai_long", "tai_ve", "L1_duyet.png")
VAY_LAM = os.path.join(HERE, "inbox", "vay_lam_3", "tai_ve", "L1_lien.png")

# Bảng màu riêng của dòng (không trùng Thương Lam / Kuba: pha lê lam nhạt; Vây Lam: lam hoàng gia; Hải Long: ngọc lam sáng)
PAL = {
    "body2": "#1F5566",     # dạng 2: xanh petrol sẫm (nước vực sâu)
    "body1": "#3C8396",     # dạng 1: petrol sáng hơn, trẻ con
    "plate": "#3F7585",     # vảy sừng (osteoderm) trên vai, hông, gáy
    "belly": "#D9E6EA",     # tấm bụng xám băng
    "ice": "#E6F1F4",       # băng sông băng đục: sừng, gờ lưng, pha lê đuôi
    "ice_dk": "#9DBAC6",    # vạch cạnh của băng
    "eye": "#F2B544",       # mắt hổ phách
    "mouth": "#1B4F66",     # lòng miệng xanh thẫm
    "tongue": "#4A9BB5",    # lưỡi
    "teeth": "#F6FBFD",     # răng
    "claw": "#2B3F4A",      # móng
    "body2_far": "#1A4756",  # chân xa dạng 2 (tối hơn một chút)
    "body1_far": "#336F80",  # chân xa dạng 1
}

LINE = ("LINE AND COLOUR: the hand-drawn look of the style images: drawn by hand on paper with a dark-brown ink pen (#2B2118), "
        "an outline about {n} px thick on this canvas, the same weight on every edge, slightly wobbly like a real pen; every "
        "area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner "
        "than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, nothing on the ground or "
        "background), no white highlights or shine spots, no gloss, no glow, no rim light, no gradients, no 3D look, no "
        "transparency effects on the ice (the ice is an opaque flat pale colour with a few thin ink facet lines). The only "
        "white allowed is one small catchlight dot in each eye and the teeth. A darker tone appears only where the design "
        "itself has a darker colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure. No text, no labels, no frame, no ground line, no water, no ice floor, no mist, no snowflakes, "
      "no particles, no other creature.")
RIG = ("POSE FOR A CUT-OUT ANIMATION RIG (important): side view, slightly three-quarter, the creature FACES THE VIEWER'S RIGHT. "
       "Standing on all four legs on an invisible flat ground, legs clearly separated from each other and from the belly (white "
       "gaps between the legs), no leg crossing another, the tail stretched out to the LEFT and clearly separated from the hind "
       "legs, the head clearly separated from the shoulders by a visible neck. The mouth is HALF OPEN (about a quarter of the "
       "way) so the inside of the mouth and the tongue are visible between the upper and lower teeth. Nothing overlaps the eye.")

SPECIES = ("THE CREATURE: a crocodile-like sea reptile of the deep cold ocean, a water-element battle pet. Body plan: long low "
           "body carried close to the ground, four short strong legs set slightly apart, a long flat crocodile snout with a strong "
           "lower jaw, a long tail. It is a pet-like fantasy animal with a determined fighting face: fierce and ready to strike, "
           "appealing, NOT a cheerful mascot and NOT horror. Its horns, back ridge and tail tip are made of OPAQUE pale "
           "glacier ice (flat colour, thin ink facet lines), never clear blue gemstone.")

FORM2 = (f"FORM 2, the adult \"Frost Crocodile King\" (final form, a legendary-tier fighter): adult proportions, the head about "
         f"one quarter of the body length, long and flat like a crocodile's, heavy brow ridges over sharp amber eyes ({PAL['eye']}) "
         f"with a vertical slit pupil. Colours: skin deep petrol blue-green {PAL['body2']} all over the back, head, legs and tail; "
         f"a row of wide pale belly plates {PAL['belly']} along the underside from throat to tail tip; chunky rounded armour scales "
         f"in a slightly lighter petrol {PAL['plate']} on the shoulders, hips and the back of the neck (like a crocodile's bony "
         f"plates, drawn as a few big rounded bumps with ink lines, not many small scales). TWO BIG HORNS of opaque glacier ice "
         f"{PAL['ice']} (with two or three thin ink facet lines and a few {PAL['ice_dk']} edge bands) growing from the back of the "
         f"skull: thick at the root, sweeping BACKWARD and then curving UP into sharp points like two sickle blades, each about as "
         f"long as the head. A RIDGE of jagged glacier-ice plates {PAL['ice']} along the spine from between the horns to the middle "
         f"of the tail, tallest over the shoulders, getting smaller toward the tail (like small icebergs standing on its back). "
         f"The TAIL ends in a heavy MACE of three or four chunky glacier-ice crystals {PAL['ice']} clustered together. Mouth: "
         f"big cream-white teeth {PAL['teeth']} of different sizes standing along both jaws (a few bigger fangs at the front), the "
         f"inside of the mouth deep blue-green {PAL['mouth']}, the tongue {PAL['tongue']}. Claws {PAL['claw']}, three per foot. "
         f"A few short curved ink lines on the cheek and throat suggest tough skin folds; keep detail moderate.")

FORM1 = (f"FORM 1, the baby \"Frost Croc Hatchling\" (first form): the SAME species and the same family look as the adult of the "
         f"last reference image, but a CHIBI hatchling: the head about 45% of the total body length, big round amber eyes "
         f"({PAL['eye']}) with a small vertical pupil, a short stubby snout, a small round body, four short chubby legs, a short "
         f"thick tail. Colours a lighter, younger version of the adult: skin {PAL['body1']} (lighter petrol teal than the adult), "
         f"pale belly plates {PAL['belly']} from throat to tail, no armour scales yet. Instead of the adult's big horns it has TWO "
         f"SHORT ICE HORN BUDS of opaque glacier ice {PAL['ice']} (thumb-sized, pointing back and slightly up) on the back of the "
         f"head; only THREE small glacier-ice spikes along its back; the tail tip has ONE small glacier-ice crystal. Mouth half open "
         f"with a few small pointed baby teeth {PAL['teeth']} (two little fangs poking down from the upper jaw at the front), inside "
         f"of the mouth {PAL['mouth']}, tongue {PAL['tongue']}. Tiny claws {PAL['claw']}. Expression: brave and stubborn (brows "
         f"down, eyes fixed on the enemy), cute but a fighter, not smiling, not sad.")


def refs2():
    return [(WORLD_STYLE, "the game's approved hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen "
                          "outline + coloured pencil / wax crayon hatching), nothing of its content",
             "Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét"),
            (HAI_LONG, "an approved water-element boss creature of the same game, 1536x1024, white background: match its pen "
                       "line, crayon texture, flat colouring and level of detail. Do NOT copy its species, colours or pose",
             "Hải Long Ngũ Đầu đã duyệt (1536 × 1024, nền trắng): rồng biển năm đầu, lấy nét bút, vân sáp, mức chi tiết"),
            (VAY_LAM, "an approved four-legged water-element beast of the same game, 1536x1024, white background: this is the "
                      "KIND OF POSE wanted (side view facing right, standing on four separated legs, fierce face) and the line "
                      "weight. Do NOT copy its species (shark), its blue colours, fins or markings",
             "Vây Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): thú cá mập bốn chân xanh lam, chỉ lấy kiểu dáng đứng và nét")]


def refs1():
    return refs2() + [(duyet(2), "the APPROVED ADULT (form 2) of THIS creature line, 1536x1024: the hatchling you draw is the "
                                 "baby of this exact species: same kind of snout, same opaque glacier-ice horns / spikes / tail "
                                 "crystal (smaller and fewer), same petrol skin colour family (lighter), same pale belly plates. "
                                 "Do NOT redraw the adult and do not copy its proportions: the baby is chibi",
                       "Concept dạng 2 (Hàn Ngạc Vương) đã chọn (1536 × 1024, nền trắng): cá sấu băng trưởng thành")]


def check(refs):
    missing = [W(p) for p, _, _ in refs if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def write_prompt(k, refs, form_text, size_text, extra):
    os.makedirs(pk(k), exist_ok=True)
    os.makedirs(save_dir(k), exist_ok=True)
    out = os.path.join(save_dir(k), "L1_concept.png")
    p = os.path.join(pk(k), "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(pth)}: {en}" for i, (pth, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not "
          "edit, move or delete any other file.", "",
          "TASK: design and draw ONE fantasy battle creature as ONE full picture, in the hand-drawn style of the style images.",
          "", SPECIES, "", form_text, "", RIG, "", size_text, ""] + extra + [LINE.format(n=6), FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return p, out


def huong_dan(k, p, out, refs, kiem):
    gd = [f"# Gói gửi GPT: dòng Hàn Ngạc, dạng {k} (`{CODE}_{k}`)", "",
          "Cá sấu băng vực sâu, dòng tướng mới đảo Thủy (thay suất ải 60). Dạng 2 (trưởng thành) vẽ trước; dạng 1 (con non chibi) "
          "vẽ sau khi dạng 2 được chọn và đính dạng 2 làm ảnh mẫu.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT lưu ảnh vào `{W(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_1_concept.txt`.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(pth)}` | {vi} |" for i, (pth, _, vi) in enumerate(refs, 1)]
    gd += ["", "## Bảng màu của dòng", "", "| Vùng | Mã |", "|---|---|"]
    gd += [f"| {n} | `{c}` |" for n, c in PAL.items()]
    gd += ["", "## Kiểm concept", ""] + kiem
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `gen.py ... --note \"...\"`)", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Có bóng, mảng sáng tối, băng trong suốt | `Flat colour only: remove every shadow, highlight, gradient and transparency; the ice is an opaque flat pale colour with thin ink facet lines.` |",
           "| Quay sang trái | `The creature must face the viewer's RIGHT.` |",
           "| Chân dính nhau, đuôi dính chân | `Separate the four legs and the tail with white gaps; no leg crosses another.` |",
           "| Miệng ngậm | `The mouth must be half open, showing the inside of the mouth and the tongue between the teeth.` |",
           "| Có nước, băng dưới chân, hơi lạnh | `Nothing around the creature: no water, no ice floor, no mist, no snowflakes.` |",
           "| Dạng 2 vẫn chibi | `Not chibi at all: adult crocodile proportions, head about one quarter of the body length.` |",
           "| Dạng 1 chưa chibi | `Make it a chibi hatchling: head about 45% of the body length, short snout, chubby short legs.` |"]
    open(os.path.join(pk(k), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")


PIECES = ("THIS IS A SHEET OF SEPARATE PARTS for a 2D cut-out animation rig, NOT a scene and NOT a whole creature: every part is "
          "drawn COMPLETE and on its own, flat on the white page like stickers laid out on a table, with at least 60 px of pure "
          "white between any two parts and between a part and the image edge. No part touches or overlaps another. Do not draw "
          "a whole creature, do not draw extra parts, do not draw labels, numbers, arrows or guide lines.")
ICE = (f"ICE PARTS are opaque pale glacier ice {PAL['ice']} (flat colour, crayon hatching) with two or three thin ink facet lines "
       f"and a few {PAL['ice_dk']} edge bands, NOT clear blue gemstone.")


def steps_of(k):
    """(bước, tiêu đề, mô tả tiếng Anh, ghi chú tiếng Việt) cho tờ mảnh của dạng k."""
    body = PAL["body2"] if k == 2 else PAL["body1"]
    far = PAL["body2_far"] if k == 2 else PAL["body1_far"]
    if k == 2:
        head = ("- top-left cell: the HEAD, UPPER PART ONLY, side view facing the viewer's RIGHT: skull, heavy brow, the amber eye "
                "with its vertical pupil, the long flat crocodile snout and the upper lip with the upper teeth hanging along its "
                "bottom edge, the armour bumps on the top of the skull. NO lower jaw, NO horns, NO neck, NO tongue. The back end of "
                "the head (where the neck attaches) is a smooth rounded stump. About 440 px wide.\n"
                "- top-middle cell: the LOWER JAW alone, side view facing right: one long wedge, pale belly colour "
                f"({PAL['belly']}) on the underside and {body} on the side, the lower teeth standing along its top edge, a thin strip "
                f"of the deep blue-green inner mouth ({PAL['mouth']}) visible above the gum line; the back end (the jaw hinge) is a "
                "rounded knob. NO tongue. About 380 px wide.\n"
                f"- top-right cell: a MOUTH INTERIOR patch: one simple soft rounded blob of flat {PAL['mouth']} with a slightly darker "
                "throat spot in the middle, brown ink outline, about 240 px wide and 170 px tall. No teeth.\n"
                "- bottom-left cell: ONE HORN of glacier ice: the root is a rounded stump at the LEFT, the horn sweeps to the right "
                "and then curves UP into a sharp point like a sickle blade, thick at the root, about 420 px wide and 330 px tall. "
                "(Only one horn: it is used for both sides.)\n"
                f"- bottom-middle cell: TWO separate small parts with white between them: (a) above, ONE TONGUE: a soft flat tongue "
                f"lying perfectly STRAIGHT and horizontal, root at the LEFT (rounded), tip at the RIGHT (rounded, slightly narrower), "
                f"about 250 px long and 60 px thick, flat {PAL['tongue']} with one thin darker centre line; (b) below, TWO CLOSED "
                f"EYELIDS side by side: each a small leaf-shaped patch of the head's skin colour {body} with the brown ink outline "
                "all round and ONE thick dark-brown curved line across its lower half (the shut eye, a stern frown), the big one "
                "about 120 px wide and 80 px tall, the small one about 100 px wide and 66 px tall.\n"
                "- bottom-right cell: the TAIL MACE: a cluster of four chunky glacier-ice crystals grown together, with a short "
                f"rounded stump of {body} skin on its LEFT side where the tail attaches, about 320 px wide and 300 px tall.")
        trunk = ("- top row: the BODY TRUNK laid out horizontally, side view: from the neck stump at the RIGHT end to the tail-root "
                 "stump at the LEFT end, one long rounded tube deeper at the chest than at the hips, about 1100 px long and 340 px "
                 f"tall; back and sides {body} with the big rounded armour scales ({PAL['plate']}) on the shoulder area, the hip area "
                 f"and the neck; a row of wide pale belly plates ({PAL['belly']}) along the whole underside. NO legs, NO back ridge, "
                 "NO head, NO tail: both ends closed and rounded.\n"
                 "- middle row: the TAIL laid out perfectly STRAIGHT and horizontal like a ruler: the thick rounded root at the "
                 "LEFT end, tapering to the right to a narrower rounded tip at the RIGHT end (the ice mace is NOT drawn, it is a "
                 f"separate part), about 1000 px long and 180 px thick at the root; {body} on top, a row of pale belly plates "
                 f"({PAL['belly']}) along the underside, a row of SMALL glacier-ice scallops along the top edge.\n"
                 "- bottom row, three separate parts with white between them, each with a FLAT bottom edge: (a) the SHOULDER "
                 "RIDGE: three tall jagged glacier-ice plates of different heights joined at one flat base, about 400 px wide and "
                 "280 px tall; (b) the MID-BACK RIDGE: three smaller ice plates on one flat base, about 320 px wide and 190 px tall; "
                 "(c) the HIP RIDGE: three small ice plates on one flat base, about 260 px wide and 130 px tall.")
        vi = ("đầu trên (sọ, mắt, mõm, răng trên; không hàm dưới, không sừng), hàm dưới (răng dưới, dải lòng miệng), mảng lòng "
              "miệng, một sừng băng liềm (gốc trái), lưỡi duỗi thẳng + hai mí nhắm, chùy pha lê đuôi",
              "thân nằm ngang (cổ bên phải, gốc đuôi bên trái; vảy sừng vai hông; không chân, không gờ), đuôi duỗi thẳng (gốc trái), "
              "ba mảnh gờ băng đáy phẳng (vai, lưng, hông)",
              "bốn chân đứng hơi gập gối: trước gần, sau gần, trước xa (tối hơn), sau xa (tối hơn); ba móng chĩa phải")
        lw = ((260, 500), (300, 500), (240, 480), (280, 480))
    else:
        head = ("- top-left cell: the HEAD, UPPER PART ONLY, side view facing the viewer's RIGHT: the chibi hatchling's big round "
                "skull, the big round amber eye with a small vertical pupil, the stern brow, the SHORT stubby snout and the upper lip "
                "with two little fangs poking down at the front. NO lower jaw, NO horn buds, NO neck, NO tongue. The back end of the "
                "head is a smooth rounded stump. About 440 px wide.\n"
                "- top-middle cell: the LOWER JAW alone, side view facing right: a short rounded wedge, pale belly colour "
                f"({PAL['belly']}) on the underside and {body} on the side, three or four tiny pointed baby teeth along its top edge, "
                f"a thin strip of the deep blue-green inner mouth ({PAL['mouth']}) above the gum line; the back end is a rounded "
                "knob. NO tongue. About 300 px wide.\n"
                f"- top-right cell: a MOUTH INTERIOR patch: one simple soft rounded blob of flat {PAL['mouth']} with a slightly darker "
                "throat spot in the middle, brown ink outline, about 200 px wide and 150 px tall. No teeth.\n"
                "- bottom-left cell: ONE HORN BUD of glacier ice: a short thick thumb-shaped bud, rounded stump at the LEFT, the "
                "tip pointing to the right and slightly up, about 220 px wide and 150 px tall. (Only one: used for both sides.)\n"
                f"- bottom-middle cell: TWO separate small parts with white between them: (a) above, ONE TONGUE: a soft flat tongue "
                f"lying perfectly STRAIGHT and horizontal, root at the LEFT (rounded), tip at the RIGHT (rounded), about 190 px long "
                f"and 56 px thick, flat {PAL['tongue']} with one thin darker centre line; (b) below, TWO CLOSED EYELIDS side by side: "
                f"each a round patch of the head's skin colour {body} with the brown ink outline all round and ONE thick dark-brown "
                "curved line across its lower half (the shut eye, a stern frown), the big one about 150 px wide and 120 px tall, the "
                "small one about 120 px wide and 96 px tall.\n"
                "- bottom-right cell: the TAIL CRYSTAL: one chunky glacier-ice crystal with a short rounded stump of "
                f"{body} skin on its LEFT side where the tail attaches, about 220 px wide and 200 px tall.")
        trunk = ("- top row: the BODY TRUNK laid out horizontally, side view: from the neck stump at the RIGHT end to the tail-root "
                 "stump at the LEFT end, one plump rounded tube (a chubby hatchling belly), about 900 px long and 380 px tall; back "
                 f"and sides {body}, a row of wide pale belly plates ({PAL['belly']}) along the whole underside, NO armour scales, NO "
                 "legs, NO back spikes, NO head, NO tail: both ends closed and rounded.\n"
                 "- middle row: the TAIL laid out perfectly STRAIGHT and horizontal like a ruler: the thick rounded root at the "
                 "LEFT end, tapering to the right to a narrower rounded tip at the RIGHT end (the ice crystal is NOT drawn, it is a "
                 f"separate part), about 760 px long and 190 px thick at the root; {body} on top, a row of pale belly plates "
                 f"({PAL['belly']}) along the underside.\n"
                 "- bottom row: THREE separate small BACK SPIKES of glacier ice with white between them, each a short triangular "
                 "ice plate with a FLAT bottom edge, about 170, 150 and 130 px tall, 170 px wide each.")
        vi = ("đầu trên chibi (sọ tròn, mắt to, mõm ngắn, hai nanh sữa; không hàm dưới, không chồi sừng), hàm dưới, mảng lòng miệng, "
              "một chồi sừng băng (gốc trái), lưỡi duỗi thẳng + hai mí nhắm, pha lê đuôi",
              "thân mập nằm ngang (cổ phải, gốc đuôi trái; không chân, không gai), đuôi duỗi thẳng (gốc trái), ba gai băng rời đáy phẳng",
              "bốn chân mập đứng hơi gập gối: trước gần, sau gần, trước xa (tối hơn), sau xa (tối hơn)")
        lw = ((260, 440), (290, 440), (240, 420), (270, 420))
    legs = ("- top-left: the NEAR FRONT LEG: the whole leg of the creature's side nearest the viewer, from the rounded shoulder "
            "stump at the top down to the foot, standing, the knee slightly bent forward (to the viewer's right) like a "
            "crocodile's stance, the foot flat on the invisible ground with THREE claws pointing to the right, about "
            f"{lw[0][0]} px wide and {lw[0][1]} px tall; skin {body}, claws {PAL['claw']}, a few ink lines for skin folds at the knee.\n"
            f"- top-right: the NEAR HIND LEG: same way, thicker thigh, about {lw[1][0]} px wide and {lw[1][1]} px tall.\n"
            f"- bottom-left: the FAR FRONT LEG: like the near front leg but the skin a little darker ({far}), about {lw[2][0]} px "
            f"wide and {lw[2][1]} px tall.\n"
            f"- bottom-right: the FAR HIND LEG: like the near hind leg but the skin a little darker ({far}), about {lw[3][0]} px "
            f"wide and {lw[3][1]} px tall.")
    return [("M01", "head, jaw, horn, tongue, eyelids, tail ice",
             "Canvas 1536 x 1024. Lay the parts out in a 3 x 2 grid of 512 px cells, one part group centred in each cell:\n" + head, vi[0]),
            ("M02", "body trunk, tail, back ridge",
             "Canvas 1536 x 1024. Three rows, parts drawn horizontally:\n" + trunk, vi[1]),
            ("M03", "four legs",
             "Canvas 1536 x 1024. Four parts in a 2 x 2 grid of 768 x 512 px cells, one leg centred in each cell:\n" + legs, vi[2])]

WHAT3 = ("WHAT THIS IS: two replacement part sheets for the 2D cut-out rig of the frost crocodile of image 4. The earlier parts did "
         "not match the concept's shape, so THESE parts must have EXACTLY THE SAME SILHOUETTE AND PROPORTIONS as the corresponding "
         "parts of the creature in image 4 (trace its shapes), just drawn separately and complete (also the areas hidden in image 4). "
         "Same colours, same line and crayon texture as image 4.")


def steps3_of(k):
    body = PAL["body2"] if k == 2 else PAL["body1"]
    if k == 2:
        trunk = ("- ONE part only, centred: the BODY TRUNK of the creature of image 4, laid out exactly as it is in image 4 (side "
                 "view, neck at the RIGHT, tail root at the LEFT), traced from image 4 with the SAME silhouette and proportions: "
                 "the THICK NECK rising at the right end up to the back of the skull, with the wide pale throat plates "
                 f"({PAL['belly']}) running from under the jaw down the front of the neck into the chest; the DEEP chest; the deep "
                 f"belly with its row of wide pale belly plates; the big rounded armour scales ({PAL['plate']}) on the shoulder, the "
                 "hip and the neck; the back line without the ice ridge. Draw it COMPLETE: fill in the areas that the legs, the "
                 "horns and the head cover in image 4. NO head, NO legs, NO tail, NO ice ridge: the neck ends in a smooth rounded "
                 "stump (the head will be laid over it), the tail root is a rounded stump. About 1300 px long and 560 px tall.")
        head = ("- top-left cell: the HEAD, UPPER PART ONLY, traced from image 4 with the SAME silhouette and proportions: the big "
                "skull with its armour bumps, the heavy brow, the amber eye with vertical pupil, the long flat snout, the upper lip "
                "with the upper teeth along its bottom edge. NO lower jaw, NO horns, NO neck, NO tongue; the back of the head is a "
                "rounded stump. About 470 px wide.\n"
                "- top-middle cell: the LOWER JAW alone, as BIG and as deep as the lower jaw in image 4 but drawn CLOSED "
                "(horizontal, as it would sit under the snout): one long deep wedge, pale belly colour underside "
                f"({PAL['belly']}) and {body} side, lower teeth along its top edge, a thin strip of the deep blue-green inner mouth "
                f"({PAL['mouth']}) above the gum line; the back end (jaw hinge) is a rounded knob. NO tongue. About 420 px wide and "
                "150 px tall.\n"
                f"- top-right cell: a MOUTH INTERIOR patch: a soft rounded blob of flat {PAL['mouth']} with a slightly darker throat "
                "spot, brown ink outline, about 260 px wide and 180 px tall. No teeth.\n"
                "- bottom-left cell: ONE SHORT TONGUE lying perfectly straight and horizontal, root at the LEFT (rounded), tip at the "
                f"RIGHT (rounded), SHORT and flat: about 200 px long and 70 px thick, flat {PAL['tongue']} with one thin darker "
                "centre line (it must fit inside the lower jaw).\n"
                f"- bottom-middle cell: TWO CLOSED EYELIDS side by side: leaf-shaped patches of {body} skin with the brown ink "
                "outline all round and ONE thick dark-brown curved line across the lower half (shut eye, stern), about 130 x 85 px "
                "and 105 x 70 px.\n"
                "- bottom-right cell: leave EMPTY (pure white).")
    else:
        trunk = ("- ONE part only, centred: the BODY TRUNK of the hatchling of image 4, laid out exactly as it is in image 4 (side "
                 "view, neck at the RIGHT, tail root at the LEFT), traced from image 4 with the SAME silhouette and proportions: the "
                 f"plump round belly with its row of wide pale belly plates ({PAL['belly']}), the THICK short neck rising at the "
                 "right end up to the back of the big skull, with the pale throat running from under the jaw down the front of the "
                 "neck into the chest. Draw it COMPLETE: fill in the areas that the legs and the head cover in image 4. NO head, NO "
                 "legs, NO tail, NO ice spikes, no armour scales: the neck ends in a smooth rounded stump (the head will be laid over "
                 "it), the tail root is a rounded stump. About 1100 px long and 560 px tall.")
        head = ("- top-left cell: the HEAD, UPPER PART ONLY, traced from image 4 with the SAME silhouette and proportions: the "
                "hatchling's big round skull, the big round amber eye with small vertical pupil, the stern brow, the short stubby "
                "snout and the upper lip with two little fangs poking down at the front. NO lower jaw, NO horn buds, NO neck, NO "
                "tongue; the back of the head is a rounded stump. About 520 px wide.\n"
                "- top-middle cell: the LOWER JAW alone, as BIG and as deep as the lower jaw in image 4 but drawn CLOSED "
                f"(horizontal): a deep rounded wedge, pale belly colour underside ({PAL['belly']}) and {body} side, three or four "
                f"tiny baby teeth along its top edge, a thin strip of the inner mouth ({PAL['mouth']}) above the gum line; the back "
                "end is a rounded knob. NO tongue. About 360 px wide and 150 px tall.\n"
                f"- top-right cell: a MOUTH INTERIOR patch: a soft rounded blob of flat {PAL['mouth']} with a slightly darker throat "
                "spot, brown ink outline, about 220 px wide and 160 px tall. No teeth.\n"
                "- bottom-left cell: ONE SHORT TONGUE lying perfectly straight and horizontal, root at the LEFT, tip at the RIGHT, "
                f"about 160 px long and 60 px thick, flat {PAL['tongue']} with one thin darker centre line (it must fit inside the "
                "lower jaw).\n"
                f"- bottom-middle cell: TWO CLOSED EYELIDS side by side: round patches of {body} skin with the brown ink outline all "
                "round and ONE thick dark-brown curved line across the lower half (shut eye, stern), about 160 x 125 px and 130 x 100 "
                "px.\n"
                "- bottom-right cell: leave EMPTY (pure white).")
    return [("M08", "body trunk traced from the concept", "Canvas 1536 x 1024.\n" + trunk,
             "thân nằm ngang bám đúng hình concept: cổ dày vươn lên bên phải, tấm họng nhạt từ dưới hàm xuống ngực, ngực và bụng sâu, "
             "vẽ đủ phần chân che; không đầu, chân, đuôi, gờ"),
            ("M09", "head, big lower jaw, mouth, short tongue, eyelids",
             "Canvas 1536 x 1024. Lay the parts out in a 3 x 2 grid of 512 px cells, one part group centred in each cell:\n" + head,
             "đầu trên bám hình concept, hàm dưới to bản vẽ khép, lòng miệng, lưỡi ngắn, hai mí; ô dưới phải để trống")]


def write_sheets(k, steps=None, fname="luot_2_manh.txt", tieu_de="Lượt 2 (tờ mảnh)", what=None):
    """luot_2_manh.txt (hoặc lượt khác) của dạng k (cần concept đã chọn L1_duyet.png của dạng đó)."""
    refs = refs2() + [(duyet(k), "the APPROVED CONCEPT of this creature, 1536x1024: every part you draw belongs to THIS creature: "
                                 "same species, same colours, same line and crayon texture, same head, horns, ice and tail design. "
                                 "Use it only to know what the parts look like; do not redraw the whole creature",
                       f"Concept dạng {k} đã chọn (1536 × 1024, nền trắng)")]
    check(refs)
    steps = steps or steps_of(k)
    order = [s[0] for s in steps]
    p = os.path.join(pk(k), fname)
    t = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image per reply and "
         "save each one as its step says. Do not reply with text only.", "",
         "REFERENCE IMAGES (open each file from its full path):"]
    t += [f"image {i} = {W(pth)}: {en}" for i, (pth, en, _) in enumerate(refs, 1)]
    t += ["", what or ("WHAT THIS IS: sheets of separate, complete parts of the frost crocodile creature of image 4, for a 2D cut-out "
          "animation rig. The animation software bends the straight tail and the legs with bones, opens the lower jaw, blinks the "
          "eyelids and swings the horns, so every part must be drawn whole (also the areas that are hidden in image 4), clean, "
          "and well separated from the others."), "",
          f"SAVE: every step's image goes into {W(save_dir(k))} under the step's name (for example {order[0]}.png). If that file "
          "already exists, add _2, _3 ... before .png. Do not change, move or delete any other file.", "",
          f"ORDER: draw step {order[0]} now, save it and stop. Each time I say \"next\", draw the next step, save it and stop, in "
          f"this order: {', '.join(order[1:])}.", "", SPECIES, "", FORM2 if k == 2 else FORM1, "", ICE, ""]
    for sc, title, en, _ in steps:
        t += [f"=== STEP {sc} ({title}) ===", PIECES, en, "", LINE.format(n=6), FLAT, BG,
              f"SAVE this step: save it as a PNG to {W(os.path.join(save_dir(k), sc + '.png'))} (create the folder if it is "
              f"missing; if that file already exists, save it as {sc}_2.png, {sc}_3.png ... in the same folder instead). Do not "
              "change, move or delete any other file.", ""]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = ["", f"## {tieu_de}: `{W(p)}`", "",
          f"Ba bước {', '.join(order)}, gõ `next` sau mỗi ảnh; GPT lưu vào `{W(save_dir(k))}`. Ảnh mẫu thêm: ảnh 4 = concept dạng {k} "
          f"đã chọn. Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/{fname} --steps {','.join(order)}`.",
          "", "Mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ≥ 60 px:"]
    gd += [f"- **{sc}**: {vi}" for sc, _, _, vi in steps]
    gd += ["- Kiểm: thân và đuôi **thẳng, nằm ngang**, hai đầu tròn; đầu trên không có hàm dưới, không sừng; sừng / chồi gốc bên trái; "
           "lưỡi thẳng; băng đục tô phẳng; mảnh không chạm nhau.", ""]
    with open(os.path.join(pk(k), "HUONG_DAN.md"), "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(gd) + "\n")
    return p


def build():
    refs = refs2()
    check(refs)
    size2 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background. The whole creature is visible, nothing cut by the "
             "edges, at least 60 px of white margin all round; the creature is about 1380 px long from tail mace to snout tip and "
             "about 760 px tall from the claws to the horn tips, centred.")
    p2, out2 = write_prompt(2, refs, FORM2, size2, [])
    huong_dan(2, p2, out2, refs, [
        "- Cá sấu bốn chân thấp người, nhìn nghiêng **quay sang phải**, bốn chân rời nhau, đuôi duỗi sang trái rời chân sau, có cổ.",
        "- Tỉ lệ trưởng thành (đầu khoảng 1/4 chiều dài), mắt hổ phách đồng tử dọc, mày gồ, mặt quả quyết.",
        "- Thân xanh petrol sẫm `#1F5566`, tấm bụng xám băng, vảy sừng to ở vai, hông, gáy.",
        "- Hai sừng băng đục lớn cong ra sau rồi vút lên như lưỡi liềm; gờ băng răng cưa dọc sống lưng; đuôi kết thúc bằng chùy 3–4 pha lê băng.",
        "- Băng **đục, tô phẳng, màu `#E6F1F4`**, chỉ có vài nét mực cạnh; không phải pha lê lam trong (kẻo giống Thương Lam, Kuba).",
        "- Miệng hé, răng kem to, lòng miệng xanh thẫm, thấy lưỡi.",
        "- Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), không nước, không băng dưới chân, nền trắng tinh.",
        "- Không giống con gốc tham khảo: không thân trắng, không sừng đen, không lòng miệng tím."])
    made = [p2]
    if os.path.exists(duyet(2)):
        refs1_ = refs1()
        check(refs1_)
        size1 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background. The whole creature is visible, nothing cut by "
                 "the edges, at least 100 px of white margin all round; the hatchling is about 1050 px long from tail tip to snout "
                 "and about 700 px tall from the claws to the top of the horn buds, centred.")
        p1, out1 = write_prompt(1, refs1_, FORM1, size1, [])
        huong_dan(1, p1, out1, refs1_, [
            "- Chibi: đầu khoảng 45% chiều dài, mõm ngắn, thân tròn, chân mập ngắn, đuôi ngắn; vẫn bốn chân rời nhau, quay sang phải.",
            "- Cùng loài với dạng 2: mõm cá sấu, bụng tấm nhạt, băng đục cùng màu; nhưng chỉ hai chồi sừng, ba gai lưng nhỏ, một pha lê đuôi nhỏ.",
            "- Thân `#3C8396` sáng hơn dạng 2, không vảy sừng.",
            "- Mặt gan lì (mày cụp, nhìn thẳng), miệng hé thấy hai răng nanh sữa, lòng miệng xanh thẫm, lưỡi.",
            "- Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh, không nước."])
        made.append(p1)
    for k in (2, 1):
        if os.path.exists(duyet(k)):
            made.append(write_sheets(k))
            made.append(write_sheets(k, steps3_of(k), "luot_3_than_dau.txt", "Lượt 3 (thân, đầu vẽ lại bám hình concept)", WHAT3))
    for p in made:
        print(W(p))
    if len(made) == 1:
        print("(chưa dựng dạng 1: chưa có", W(duyet(2)) + ")")


if __name__ == "__main__":
    build()
