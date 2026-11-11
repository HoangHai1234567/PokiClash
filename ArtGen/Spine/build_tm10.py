"""Gói GPT cho dòng 10 đảo Thủy (lô 2026-11-11): hai dạng đầu của dòng Hải Long, dẫn tới dạng 3 là Hải Long Ngũ Đầu đã duyệt
(ArtGen/Spine/inbox/hai_long/tai_ve/L1_duyet.png, rig hai_long.py). Mã làm việc `tm10` cho dạng 1, 2; dạng 3 giữ mã `hai_long`.

  dạng 1  Hải Long Nhi      rồng biển con MỘT đầu, chibi, xanh ngọc nhạt, sừng mới nhú, bờm hồng san hô nhỏ
  dạng 2  Hải Long Tam Thủ  rồng biển trẻ BA đầu, tỉ lệ trưởng thành, xanh ngọc vừa, sừng thẳng, bờm san hô ngắn
  dạng 3  Hải Long Ngũ Đầu  năm đầu, xanh ngọc đậm, gạc vàng phân nhánh, ngọc trán, bờm đỏ san hô lớn (đã có)

Pha 1 chỉ gen concept trọn con (một ảnh, nền trắng, dáng dễ tách mảnh). Gen dạng 2 trước (đính dạng 3), chọn xong chép thành
inbox/tm10_2/tai_ve/L1_duyet.png rồi mới dựng được prompt dạng 1 (đính cả dạng 2 và dạng 3).

    py -3 -I build_tm10.py            dựng gui_gpt/tm10_2/luot_1_concept.txt (và tm10_1 nếu dạng 2 đã có L1_duyet.png) + HUONG_DAN.md
    py -3 -I gen.py gui_gpt/tm10_2/luot_1_concept.txt
    py -3 -I gen.py gui_gpt/tm10_1/luot_1_concept.txt
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))


def W(p):
    return os.path.normpath(p)


WORLD_STYLE = W(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
DRAGON = W(os.path.join(HERE, "inbox", "thuong_lam_3", "tai_ve", "L1_lien.png"))
FORM3 = W(os.path.join(HERE, "inbox", "hai_long", "tai_ve", "L1_duyet.png"))


def pk(k):
    return W(os.path.join(HERE, "gui_gpt", f"tm10_{k}"))


def save_dir(k):
    return W(os.path.join(HERE, "inbox", f"tm10_{k}", "tai_ve"))


def duyet(k):
    return W(os.path.join(save_dir(k), "L1_duyet.png"))


LINE = ("LINE AND COLOUR: the hand-drawn look of the style images: drawn by hand on paper with a dark-brown ink pen (#2B2118), "
        "an outline about {n} px thick on this canvas, the same weight on every edge, slightly wobbly like a real pen; every "
        "area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner "
        "than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, nothing on the background), no "
        "white highlights or shine spots, no gloss, no glow, no rim light, no gradients, no 3D look. The only white allowed is "
        "one small catchlight dot in each eye, and the white foam of the water. A darker tone appears only where the design "
        "itself has a darker colour.")
WATER = ("THE WATER, exactly in the style of the water in image 3: stylised hand-drawn waves, plump curling crests like the waves "
         "of an old woodblock print but simple and chunky: three flat blues (deep #1E68BE, sky #3A96E2, pale #8CD0F6) in broad "
         "bands that follow the flow of each wave, and flat white foam (#F4FCFF) as round bumpy scallops on the crests, all with "
         "the same brown ink outline.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure. No text, no labels, no frame, no ground line, no sky, no rocks, no other creature.")
RIG = ("DRAWN FOR A CUT-OUT ANIMATION RIG: the pose must be easy to cut into parts: each head clearly separate from the others "
       "and from the body with white or water behind it; necks not crossing each other; mouth slightly open so a strip of the "
       "rose inner mouth shows; whiskers and fins not covering the eyes or the mouth; the tail fin apart from the body.")

FORMS = {
    2: dict(
        name="Hải Long Tam Thủ",
        canvas="landscape 1536x1024",
        size="about 1250 px wide and 820 px tall, centred",
        design=(
            "THE CREATURE: a THREE-HEADED YOUNG SEA DRAGON, an eastern-style water dragon (long serpent necks, no wings, no legs "
            "visible), the SECOND form of the creature line whose FINAL form is image 3. It is the same species as image 3 but "
            "YOUNGER and SIMPLER: three heads instead of five, and everything a step lighter and plainer. Proportions are those "
            "of a young adult, NOT chibi: long snout, brow ridge, sharp almond eyes, small fangs, determined fierce look, "
            "neither cute nor scary-horror.\n"
            "Colours, the same on all three heads and necks: scales jade-green (#45B8A4, clearly LIGHTER and fresher than the "
            "deep jade of image 3) on the back and sides; belly plates cream-gold (#F2D9A0) as a row of wide segments along the "
            "underside of each neck; a low coral (#E8664A) fin ridge along the back of each neck and a SHORT coral fin mane "
            "behind each head (three or four short lobes, much smaller than the big mane of image 3); two STRAIGHT plain golden "
            "horns (#E9B84A) per head, smooth spikes curving gently back, NO branches, NO forehead pearl; amber eyes (#F0A030) "
            "with a dark slit pupil; inside of the mouth deep rose (#B8405A), teeth cream. Only the CENTRE head has two short "
            "cream whiskers (#F4EEDC); the side heads have none. The centre head is the leader: about 20% bigger than the others."),
        comp=(
            "COMPOSITION (important):\n"
            "- The three necks rise out of ONE churning mass of water at the bottom centre and fan out upward. ALL three heads "
            "are seen from the side and ALL face the viewer's RIGHT, mouths slightly open, as if watching an enemy on the right.\n"
            "- The CENTRE head is the highest, its neck an upright S-curve. The LEFT head is a little lower, its neck leaning "
            "back to the left and then curving so the head still faces right. The RIGHT head is the lowest, its neck reaching "
            "forward to the right. The three heads do NOT overlap each other, each is fully visible.\n"
            "- A ring of curling waves around the place where the necks come out, lower and fewer than in image 3; one hump of "
            "the coiled body arches out of the water at the far left; the coral tail fin rises out of the water at the far "
            "right, smaller than in image 3. The front waves overlap the bottoms of the necks so no neck base is seen. A few "
            "drops fly above the waves."),
        refs_extra=[],
        vi="Rồng biển trẻ BA đầu (đầu giữa to hơn 20%), xanh ngọc #45B8A4 nhạt hơn dạng 3, bụng kem vàng, vây và bờm san hô "
           "ngắn, sừng vàng THẲNG không nhánh, không ngọc trán, chỉ đầu giữa có râu ngắn; nước ít và thấp hơn dạng 3; vòng thân "
           "trái, chóp đuôi phải",
    ),
    1: dict(
        name="Hải Long Nhi",
        canvas="landscape 1536x1024",
        size="about 900 px wide and 800 px tall, centred",
        design=(
            "THE CREATURE: a BABY SEA DRAGON with ONE head, the FIRST form of the creature line whose later forms are image 3 "
            "(three heads) and image 4 (five heads, the final form). Same species, drawn as a chibi hatchling: the head is big, "
            "about 40% of the whole creature's height; big round amber eyes (#F0A030) with a dark slit pupil and one small "
            "catchlight; a short rounded snout with a small brow ridge pushed down a little so the face reads brave and "
            "determined, not sad and not grinning; the mouth slightly open showing two tiny cream fangs and a strip of deep "
            "rose (#B8405A) inside.\n"
            "Colours: scales pale mint-jade (#6ED3BF, LIGHTER than the two later forms) on the back and sides; belly plates pale "
            "cream (#F8EBC8) as a row of wide segments along the underside; two tiny golden horn NUBS (#E9B84A, short rounded "
            "bumps, no branches); a small tuft of coral-pink (#F28B70) fin mane on the back of the head, three short rounded "
            "lobes; a low coral-pink fin ridge of small rounded lobes along the back; two very short cream whisker stubs "
            "(#F4EEDC) at the snout. No pearl, no antlers."),
        comp=(
            "COMPOSITION (important):\n"
            "- The body is a short plump serpent: it rises out of a small mass of water at the bottom centre in ONE gentle "
            "S-curve, the neck clearly visible between the water and the head, and the head at the top facing the viewer's "
            "RIGHT (side view, three-quarter at most), as if watching an enemy on the right. No legs, no wings.\n"
            "- Behind it, to the RIGHT of the body, a small coral-pink fan tail fin of three rounded lobes pokes up out of the "
            "water, not touching the body.\n"
            "- The water: a small ring of two or three little curling waves and round foam around the place where the body "
            "leaves the water, a few drops flying up. The front wave overlaps the bottom of the body so no body base is seen. "
            "Much less water than in the later forms."),
        refs_extra=[(duyet(2), "FORM 2 of THIS same creature line (approved), 1536x1024, white background: three heads; the baby "
                               "must clearly be the same species (head shape, fin mane, belly plates, water) but one-headed, "
                               "chibi and lighter in colour",
                     "Concept dạng 2 đã chọn (1536 × 1024, nền trắng): rồng biển trẻ ba đầu")],
        vi="Rồng biển con MỘT đầu, chibi (đầu ~40% chiều cao), mắt to tròn màu hổ phách, mõm ngắn, hai nanh nhỏ; vảy xanh "
           "ngọc nhạt #6ED3BF, bụng kem nhạt, sừng mới nhú tròn, bờm hồng san hô ba lọn, râu cụt; thân chữ S một khúc trồi từ "
           "vũng nước nhỏ, vây đuôi hồng san hô nhô lên bên phải; nước ít",
    ),
}


def refs_for(k):
    refs = [(WORLD_STYLE, "the approved hand-drawn map of the project, 1024x1536: use ONLY its line and colouring style (brown ink "
                          "pen outline + coloured pencil / wax crayon hatching), nothing of its content",
             "Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét"),
            (DRAGON, "an approved dragon creature of the same project, 1536x1024, white background: match EXACTLY its pen line, "
                     "crayon texture, flat colouring and level of detail. Do NOT copy its design, colours, wings or pose",
             "Rồng băng Thương Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): lấy nét bút, vân sáp, mức chi tiết; không chép dáng"),
            (FORM3, "the FINAL FORM (five heads) of THIS same creature line, approved, 1536x1024, white background: the new picture "
                    "is a YOUNGER form of exactly this species: same head shape, eyes, fin mane, belly plates, horns colour and the "
                    "same kind of water, but fewer heads, simpler and lighter as described below. Do not redraw this picture",
             "Concept Hải Long Ngũ Đầu dạng 3 đã duyệt (1536 × 1024, nền trắng): năm đầu rồng xanh ngọc trồi lên từ sóng")]
    return refs + FORMS[k]["refs_extra"]


def check(refs):
    missing = [p for p, _, _ in refs if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def build(k):
    f = FORMS[k]
    refs = refs_for(k)
    check(refs)
    os.makedirs(pk(k), exist_ok=True)
    os.makedirs(save_dir(k), exist_ok=True)
    out = W(os.path.join(save_dir(k), "L1_concept.png"))
    p = W(os.path.join(pk(k), "luot_1_concept.txt"))
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {pth}: {en}" for i, (pth, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {out}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not "
          "edit, move or delete any other file.", "",
          f"TASK: design and draw ONE creature as ONE full picture, in the hand-drawn style of images 1 and 2. It is form {k} of a "
          f"three-form creature line; its final form is image 3.", "",
          f["design"], "", WATER, "",
          f"CANVAS AND FRAMING: {f['canvas']}, pure-white background. The whole creature and its water are visible, nothing cut by "
          f"the edges, at least 60 px of white margin all round; the group is {f['size']}.", "",
          f["comp"], "", RIG, "", LINE.format(n=6), FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return p, out, refs


def huong_dan(made):
    gd = ["# Gói gửi GPT: dòng Hải Long, dạng 1 và 2 (`tm10`)", "",
          "Dạng 3 của dòng là Hải Long Ngũ Đầu đã duyệt (`inbox/hai_long/tai_ve/L1_duyet.png`). Pha 1 chỉ gen concept trọn con cho "
          "hai dạng đầu; gen dạng 2 trước (đính dạng 3), chọn xong chép bản chọn thành `inbox/tm10_2/tai_ve/L1_duyet.png`, chạy lại "
          "`build_tm10.py` để có prompt dạng 1 (đính cả dạng 2 và 3).", "",
          "| Dạng | Tên | File prompt (chỉ gửi GPT đường dẫn này) | GPT lưu ảnh vào |", "|---|---|---|---|"]
    for k, (p, out, _) in sorted(made.items()):
        gd.append(f"| {k} | {FORMS[k]['name']} | `{p}` | `{out}` |")
    gd += ["", "Claude tự gen: `py -3 -I gen.py gui_gpt/tm10_<k>/luot_1_concept.txt` (chạy nền, khoảng 2 phút một ảnh; sửa nhanh "
           "thêm `--note \"...\"`).", "", "## Ảnh mẫu", "", "| Ảnh | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    seen = set()
    for k, (_, _, refs) in sorted(made.items()):
        for i, (pth, _, vi) in enumerate(refs, 1):
            if pth not in seen:
                seen.add(pth)
                gd.append(f"| {i} (dạng {k}) | `{pth}` | {vi} |")
    gd += ["", "## Kiểm concept", ""]
    for k in sorted(made):
        gd.append(f"- **Dạng {k} ({FORMS[k]['name']})**: {FORMS[k]['vi']}.")
    gd += ["- Chung: con vật nhìn sang **phải** người xem, miệng hé thấy lòng miệng hồng; đầu không che nhau, không che đuôi; "
           "sóng trước che chỗ thân mọc ra.",
           "- Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), không quầng; nền trắng tinh; không chữ, không đường đất.",
           "- Dạng 1 phải **chibi** (đầu to, mắt to), dạng 2 **không** chibi (mõm dài, mắt sắc); dạng 3 phải trông khác hẳn hai dạng "
           "trước (đậm màu hơn, năm đầu, gạc phân nhánh, ngọc trán, bờm lớn).", "",
           "## GPT vẽ sai thì gửi thêm (cùng chat)", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Có bóng, mảng sáng tối | `Flat colour only: remove every shadow, highlight and gradient; keep the crayon hatching as texture.` |",
           "| Vẽ đủ năm đầu hoặc chép ảnh 3 | `Do not redraw image 3: this is a YOUNGER form with exactly the number of heads described.` |",
           "| Dạng 2 vẫn chibi | `Not chibi: adult proportions, long snout, head about one fifth of the creature's height, sharp eyes.` |",
           "| Dạng 1 không chibi | `Chibi hatchling: the head is about 40% of the creature's height, eyes big and round.` |",
           "| Quay sang trái | `Every head must face the viewer's RIGHT.` |",
           "| Nhiều nước quá | `Much less water: a small ring of two or three little waves only.` |"]
    open(os.path.join(pk(2), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    if 1 in made:
        open(os.path.join(pk(1), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")


# ---------------------------------------------------------------- lượt 2: tờ mảnh (pha 2, chỉ khi dạng đó đã có L1_duyet.png)
PIECES_RULE = ("THIS IS A SHEET OF SEPARATE PARTS for a 2D cut-out animation rig, NOT a scene: every part is drawn COMPLETE and on "
               "its own, flat on the white page like stickers laid out on a table, with at least 60 px of pure white between any two "
               "parts and between a part and the image edge. No part touches or overlaps another. Do not draw a whole creature, do "
               "not draw extra parts, do not draw labels, numbers, arrows or guide lines.")
HL_M01 = W(os.path.join(HERE, "inbox", "hai_long", "tai_ve", "M01.png"))
HL_M02 = W(os.path.join(HERE, "inbox", "hai_long", "tai_ve", "M02.png"))

# dạng 2: tờ M01 (đầu, hàm, lòng miệng, mí, lưỡi, râu) bố cục 4 cột × 3 hàng ô 384 × 341; tờ M02 (cổ to, cổ nhỏ, vòng thân, đuôi)
SHEETS = {
    2: [
        ("M01", "heads, jaws, eyelids, tongues, whisker", HL_M01,
         "Canvas 1536 x 1024, laid out as a 4 x 3 grid of cells 384 px wide and 341 px tall; one part centred in each cell, left to "
         "right, top to bottom. Draw the parts of THE CENTRE (leader) HEAD and of A SIDE HEAD of the three-headed dragon of image 3; "
         "follow image 4 for WHAT KIND of part each one is (upper head without lower jaw, lower jaw alone, mouth patch...), but with "
         "THIS dragon's design: jade #45B8A4 scales, STRAIGHT plain golden horns (#E9B84A) with NO branches, NO forehead pearl, a "
         "SHORT coral (#E8664A) fin mane of three or four lobes, amber eye (#F0A030) with dark slit pupil and one catchlight, cream "
         "teeth, deep-rose (#B8405A) mouth interior.\n"
         "- row 1, cell 1: the LEADER HEAD, UPPER PART ONLY, side view facing the viewer's RIGHT: skull, brow ridge, eye, long snout "
         "and the upper lip with its upper teeth along the bottom edge, two straight golden horns, the short coral fin mane sweeping "
         "back from the back of the skull. NO lower jaw, NO neck, NO whiskers; the back end (where the neck attaches) is a smooth "
         "rounded stump. About 360 px wide.\n"
         "- row 1, cell 2: the LEADER LOWER JAW alone, facing right: one long wedge, cream-gold (#F2D9A0) underside, jade side, lower "
         "teeth standing along its top edge, a strip of deep-rose inner mouth and the rose tongue lying inside visible above the gum "
         "line; the back end (jaw hinge) is a rounded knob. About 280 px wide.\n"
         "- row 1, cell 3: a MOUTH INTERIOR patch: one soft rounded blob of flat deep rose (#B8405A) with a slightly darker rose throat "
         "spot (#8E2F48) in the middle, brown ink outline, about 210 px wide and 150 px tall. No teeth.\n"
         "- row 1, cell 4: the LEADER'S CLOSED EYELID: a small leaf-shaped patch of the head's jade skin (#45B8A4, crayon hatching) with "
         "the brown ink outline all round and ONE thick dark-brown curved line across its lower half (the shut eye, curving down "
         "toward the snout like a stern frown), about 110 px wide and 72 px tall.\n"
         "- row 2, cell 1: a SIDE HEAD, UPPER PART ONLY, same species, same view, a little smaller and simpler (shorter horns, smaller "
         "mane). NO lower jaw, NO neck, NO whiskers; rounded stump at the back. About 320 px wide.\n"
         "- row 2, cell 2: the SIDE HEAD'S LOWER JAW alone, like the leader's but smaller, about 250 px wide.\n"
         "- row 2, cell 3: the LEADER'S TONGUE: one long soft flat tongue hanging limp, drawn perfectly STRAIGHT and horizontal, root "
         "on the LEFT, tip on the RIGHT, about 280 px long, 56 px thick at the rounded root, narrowing to about 32 px near the tip, the "
         "tip ending in two short rounded lobes (a small fork); flat rose pink (#E27C92), clearly lighter than the mouth interior, with "
         "ONE thin darker rose line (#B8405A) along the middle. No teeth, no mouth, no drool.\n"
         "- row 2, cell 4: the SIDE HEAD'S CLOSED EYELID, same design as cell 4 of row 1, about 92 px wide and 60 px tall.\n"
         "- row 3, cell 1: ONE long whisker: a single cream tendril (#F4EEDC), thick at the root and tapering to a fine curled tip, "
         "drawn as a gentle S-curve running left to right, about 330 px long and 24 px thick at the root.\n"
         "- row 3, cell 2: the SIDE HEAD'S TONGUE, same design as the leader's, about 230 px long and 46 px thick at the root.\n"
         "- row 3, cells 3 and 4: EMPTY (pure white).",
         "đầu thủ lĩnh (trên), hàm dưới thủ lĩnh, mảng lòng miệng, mí thủ lĩnh; đầu phụ (trên), hàm phụ, lưỡi thủ lĩnh, mí phụ; râu, "
         "lưỡi phụ; hai ô cuối trống"),
        ("M02", "necks, body coil, tail", HL_M02,
         "Canvas 1536 x 1024. Three rows, parts drawn horizontally, the same KINDS of parts as image 4 but with THIS dragon's design "
         "(jade #45B8A4, cream-gold #F2D9A0 belly plates, SHORT coral #E8664A fin ridge of small rounded lobes):\n"
         "- top row: the THICK NECK of the leader head, laid out perfectly STRAIGHT and horizontal like a long tube seen from the "
         "side, about 1380 px long and 170 px thick, the same thickness for most of its length and a little thinner toward the RIGHT "
         "end (the head end). Along the TOP edge runs the low coral fin ridge (small rounded lobes, a regular row); the upper two "
         "thirds of the tube are jade with a few simple curved scale marks; the lower third is the row of cream-gold belly plates "
         "(about 16 wide segments separated by thin ink lines). BOTH ends are closed and rounded (round stumps). No head, no tail.\n"
         "- middle row: a THIN NECK, the same design, perfectly straight and horizontal, about 1380 px long and 125 px thick, a "
         "little thinner toward the right end, both ends rounded.\n"
         "- bottom row, two parts side by side with white between them: (a) on the left, a BODY COIL: one arch of the dragon's body "
         "shaped like an upside-down U (a hump rising out of water), jade with the coral fin ridge along its outer (upper) curve and "
         "the cream-gold belly plates along its inner curve, the two leg ends pointing straight down and cut off flat at the bottom, "
         "about 480 px wide and 280 px tall, tube thickness about 135 px; (b) on the right, the TAIL TIP: the last tapering part of "
         "the tail lying horizontal, about 480 px long, thick rounded stump on the left tapering to the right into a coral fan-shaped "
         "tail fin of three rounded lobes.",
         "cổ to duỗi thẳng (1380 × 170), cổ nhỏ duỗi thẳng (1380 × 125), vòng thân chữ U úp, chóp đuôi có vây"),
    ],
    # dạng 1 (chibi một đầu): M01 lưới 3 × 2 ô 512 × 512: đầu (trên), hàm dưới, lòng miệng / mí, lưỡi, râu cụt; M02: thân-cổ duỗi
    # thẳng (một dải), vây đuôi
    1: [
        ("M01", "head, jaw, mouth, eyelid, tongue, whisker stubs", HL_M01,
         "Canvas 1536 x 1024, laid out as a 3 x 2 grid of cells 512 px wide and 512 px tall; one part centred in each cell, left to "
         "right, top to bottom. Draw the parts of the BABY sea dragon of image 3 (chibi: big head, big round eye); follow image 4 "
         "only for WHAT KIND of part each one is (upper head without lower jaw, lower jaw alone, mouth patch...). Design: pale "
         "mint-jade #6ED3BF skin, two tiny golden horn NUBS (#E9B84A, rounded bumps), a small coral-pink (#F28B70) fin mane of three "
         "rounded lobes at the back of the head, big round amber eye (#F0A030) with a dark slit pupil and one catchlight, tiny cream "
         "fangs, deep-rose (#B8405A) mouth interior.\n"
         "- row 1, cell 1: the HEAD, UPPER PART ONLY, side view facing the viewer's RIGHT: big round skull, brow, the big eye, short "
         "rounded snout and the upper lip with two tiny fangs along the bottom edge, the two horn nubs, the small coral-pink mane "
         "sweeping back. NO lower jaw, NO neck, NO whiskers; the back end (where the neck attaches) is a smooth rounded stump. About "
         "430 px wide.\n"
         "- row 1, cell 2: the LOWER JAW alone, facing right: a short plump wedge, pale cream (#F8EBC8) underside and mint-jade side, "
         "two tiny lower fangs along its top edge, a strip of deep-rose inner mouth visible above the gum line; the back end (jaw "
         "hinge) is a rounded knob. About 300 px wide.\n"
         "- row 1, cell 3: a MOUTH INTERIOR patch: one soft rounded blob of flat deep rose (#B8405A) with a slightly darker rose throat "
         "spot (#8E2F48) in the middle, brown ink outline, about 220 px wide and 160 px tall. No teeth.\n"
         "- row 2, cell 1: the CLOSED EYELID: a round-ish leaf-shaped patch of the head's mint-jade skin (#6ED3BF, crayon hatching) with "
         "the brown ink outline all round and ONE thick dark-brown curved line across its lower half (the shut eye, a gentle downward "
         "curve), about 150 px wide and 110 px tall.\n"
         "- row 2, cell 2: the TONGUE: a short soft flat tongue drawn perfectly STRAIGHT and horizontal, root on the LEFT, tip on the "
         "RIGHT, about 220 px long and 60 px thick at the rounded root, narrowing a little, the tip ending in two short rounded lobes; "
         "flat rose pink (#E27C92) with ONE thin darker rose line (#B8405A) along the middle.\n"
         "- row 2, cell 3: TWO short whisker stubs stacked one above the other with white between them: each a small cream (#F4EEDC) "
         "tendril, thick at the root and tapering to a soft curled tip, drawn as a gentle S-curve running left to right, about 160 px "
         "long and 22 px thick at the root.",
         "đầu (trên, mắt to), hàm dưới, lòng miệng; mí mắt, lưỡi, hai râu cụt"),
        ("M02", "body and tail fin", HL_M02,
         "Canvas 1536 x 1024. Two rows, parts drawn horizontally, with THIS baby dragon's design (pale mint-jade #6ED3BF, pale cream "
         "#F8EBC8 belly plates, a low coral-pink #F28B70 fin ridge of small rounded lobes):\n"
         "- top row: the BODY of the baby dragon (neck and body are one plump tube), laid out perfectly STRAIGHT and horizontal like "
         "a long tube seen from the side, about 1300 px long and 230 px thick, the same thickness for most of its length and a "
         "little thinner toward the RIGHT end (the head end). Along the TOP edge runs the low coral-pink fin ridge (small rounded "
         "lobes, a regular row); the upper two thirds of the tube are mint-jade with a few simple curved scale marks; the lower third "
         "is the row of pale cream belly plates (about 12 wide segments separated by thin ink lines). BOTH ends are closed and rounded "
         "(round stumps). No head, no tail fin.\n"
         "- bottom row: the TAIL TIP: the last tapering part of the tail lying horizontal, about 520 px long, thick rounded stump on "
         "the left tapering to the right into a coral-pink fan-shaped tail fin of three rounded lobes, about 260 px tall at the fin.",
         "thân-cổ duỗi thẳng (1300 × 230), chóp đuôi có vây hồng san hô"),
    ],
}


def build_sheets(k):
    if not os.path.exists(duyet(k)):
        print(f"(chưa dựng tờ mảnh dạng {k}: chưa có {duyet(k)})")
        return []
    made = []
    for sc, title, example, en, vi in SHEETS[k]:
        refs = refs_for(k)[:2] + [
            (duyet(k), f"the APPROVED CONCEPT of this dragon (form {k}), 1536x1024, white background: every part you draw belongs to "
                       "THIS creature: same species, same colours, same line and crayon texture, same head design. Use it only to "
                       "know what the parts look like; do not redraw the scene", f"Concept dạng {k} đã duyệt"),
            (example, "an approved PARTS SHEET of the FINAL form of the same creature line, 1536x1024: shows HOW the parts are cut "
                      "(upper head without lower jaw, lower jaw alone, straight necks...) and the outline weight. Copy the KIND of "
                      "parts and their cleanliness, NOT its design (it has branching antlers, a pearl and a big mane; this form has "
                      "straight horns, no pearl, a short mane)", "Tờ mảnh dạng 3 đã duyệt (mẫu cách cắt mảnh)")]
        check(refs)
        out = W(os.path.join(save_dir(k), sc + ".png"))
        p = W(os.path.join(pk(k), f"luot_2_{sc}.txt"))
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {pth}: {d}" for i, (pth, d, _) in enumerate(refs, 1)]
        t += ["", f"SAVE: save it as a PNG to {out}",
              f"If a file with that name already exists, save as {sc}_2.png, {sc}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "",
              f"TASK: draw ONE sheet of separate, complete parts ({title}) of the three-headed sea dragon of image 3, for a 2D cut-out "
              "animation rig. The animation software bends the straight necks with bones, opens the jaws and blinks the eyelids, so "
              "every part must be drawn whole (also the areas hidden in image 3), clean, and well separated from the others.", "",
              PIECES_RULE, "", en, "", LINE.format(n=6), FLAT, BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        made.append((sc, p, out, vi))
    gd = [f"# Lượt 2 (tờ mảnh) dạng {k} {FORMS[k]['name']}", "", "Mỗi tờ một file prompt, chỉ gửi GPT đường dẫn file:", "",
          "| Tờ | File prompt | GPT lưu vào | Kiểm |", "|---|---|---|---|"]
    gd += [f"| {sc} | `{p}` | `{out}` | {vi} |" for sc, p, out, vi in made]
    gd += ["", "Claude tự gen: `py -3 -I ArtGen/Spine/gen.py <file prompt>` (hoặc `chay_hoa.py` chạy tách). Mỗi tờ 1536 × 1024, nền "
           "trắng, mảnh rời nhau ≥ 60 px, tô phẳng; đầu là PHẦN TRÊN (không hàm, không cổ); cổ THẲNG như thước.", "",
           "| Sai | Gửi thêm |", "|---|---|",
           "| Cổ vẽ cong | `The necks must be perfectly straight horizontal tubes, like a ruler, both ends rounded.` |",
           "| Đầu dính hàm hoặc cổ | `The head part is the UPPER part only: no lower jaw, no neck; the lower jaw is its own separate part.` |",
           "| Có gạc phân nhánh / ngọc | `Straight plain horns, no branches, no pearl: this is the younger form.` |",
           "| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |"]
    open(os.path.join(pk(k), "HUONG_DAN_luot_2.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    for _, p, _, _ in made:
        print(p)
    return made


def main():
    made = {2: build(2)}
    if os.path.exists(duyet(2)):
        made[1] = build(1)
    else:
        print("(chưa dựng dạng 1: chưa có", duyet(2) + ")")
    huong_dan(made)
    for k, (p, _, _) in sorted(made.items()):
        print(p)
    for k in SHEETS:
        build_sheets(k)


if __name__ == "__main__":
    main()
