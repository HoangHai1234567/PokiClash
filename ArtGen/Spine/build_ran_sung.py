"""Gói GPT vẽ concept dòng rắn nước có sừng (tướng thứ 5 đảo Thủy, 2026-11-11, người dùng lên ý tưởng). Mã làm việc: ran_sung.

Ý người dùng: rắn nước có sừng: hai chùm lông trắng trên đầu con gốc đổi thành hai sừng đen; chót đuôi cũng là sừng đen, nhọn kiểu
kunai (cứng, không mềm như con gốc). Idle như con gốc, sửa nhẹ. Đòn thường lao tới cắn nhanh; chiêu mana há nhẹ mồm bắn nước;
chiêu cuối dùng đuôi quật chém liên tiếp nhiều phát, nhanh. Cái khó: dáng idle và độ mềm uyển chuyển của rắn. Dạng 2 dài hơn, to
hơn, chiêu mạnh hơn. Mỗi dạng <= 0,5 MB. Rig và nhịp học từ một con rắn của game tham khảo (ghi chú: inbox/ran_sung_ghichu.md).
Không đính ảnh con gốc vào prompt; nét vẽ là nét của dự án (bút mực nâu + chì sáp, tô phẳng). Màu là đề xuất của Claude (người
dùng chỉ dặn sừng đen), chờ duyệt.

  dạng 1  rắn con mập, đầu to, lưng lam cô-ban đốm bong bóng, bụng lam băng, mắt hổ phách, hai sừng đen, chót đuôi là sừng đen dáng lá hơi hướng kunai
  dạng 2  dài và to hơn (thêm một vòng cuộn), lưng chàm đậm, sừng dài có nhánh, lộ nanh, sừng đuôi to có ngạnh

Lượt 1 mỗi dạng: concept trọn con một ảnh, miệng khép. Dạng 2 chỉ dựng khi đã có inbox/ran_sung_1/tai_ve/L1_duyet.png.
Lượt 2 (dáng duỗi để lao cắn, miệng há, mắt nhắm...) viết sau khi duyệt concept.

    py -3 -I ArtGen/Spine/build_ran_sung.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ran_sung_1/luot_1_concept.txt [--note "..."]
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ran_sung_2/luot_1_concept.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "ran_sung"
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
SHARK = os.path.join(HERE, "inbox", "vay_lam_1", "tai_ve", "L1_lien.png")     # nét, tô sáp phẳng, mắt dữ (Thủy, đã duyệt)
DROP = os.path.join(HERE, "inbox", "ti_tach_1", "tai_ve", "L1_duyet.png")     # tướng khởi đầu Thủy đã duyệt: độ đơn giản, nét rung


def W(p):
    return os.path.normpath(p)


def pk(k):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def chosen(k):
    return os.path.join(save_dir(k), "L1_duyet.png")


def ref1():
    """Ảnh dạng 1 làm mẫu cho dạng 2: bản đã duyệt, chưa có thì bản nháp mới nhất (chỉ để gen thử dạng 2)."""
    for n in ("L1_duyet.png", "L1_sua.png"):
        p = os.path.join(save_dir(1), n)
        if os.path.exists(p):
            return p
    return chosen(1)


# ---------------------------------------------------------------- thiết kế (tiếng Anh, dán vào prompt)
PALETTE1 = ("COLOURS (use exactly these, each area one flat colour): back and top of the head cobalt blue (#2E6FD8); round "
            "bubble spots on the back light aqua (#86D6F0); belly, throat, lips, cheeks and lower jaw pale ice blue (#DDF0F7, "
            "never left as bare white paper) with thin belly lines a little darker (#A9CFE2); both head horns and the tail "
            "horn charcoal black (#26252C) with a few thin dark-grey ridge lines (#5B5B68); eyes amber orange (#FFA92E) with "
            "a black vertical slit pupil; every outline dark-brown ink (#2B2118).")

# Hướng nhìn, đầu, miệng: học cách dựng của con gốc (nhìn gần chính diện từ trên xuống, đầu cúi, hai mắt ở hai bên đầu, miệng nhỏ
# có mỏm nhọn giữa môi trên), hình là của mình.
VIEW_HEAD = (
    "- VIEW OF THE HEAD (very important): the snake LOOKS AT THE VIEWER. The head is seen from the FRONT and a little from "
    "above, turned only slightly toward the viewer's right, with the chin tucked in and the snout dipping DOWN: the snake "
    "lowers its head and stares out of the picture from under its brows. We see the whole top of the head and the whole "
    "face at once, with one eye on the left side and one eye on the right side of the head. It is NOT a side view, NOT a "
    "profile: the snout does not stick out sideways.\n"
    "- HEAD SHAPE: a real SNAKE head, big for the body (about 330 px wide and 300 px tall): a tall rounded dome like an egg "
    "standing on its narrow end: a wide smooth crown on top, widest at eye level, then narrowing downward to a short, "
    "blunt, rounded snout at the BOTTOM of the head, a little right of centre. A smooth simple shape: NO long muzzle, NO "
    "forehead bump, NO chin beard: not a lizard, not a dinosaur, not a dragon, not a dog-like snout.\n"
    "- FACE COLOURS: the cobalt blue of the crown comes down the middle of the face between the two eyes as a broad rounded "
    "tongue shape that ends just above the mouth. Everything beside and below it (the cheeks under the eyes, the lips, the "
    "chin) is pale ice blue.\n"
    "- SNAKE MOUTH, closed, SMALL and LOW, at the very bottom of the face on the snout tip: the upper lip overhangs and "
    "forms one small point in the middle, so the mouth line is a small shallow upside-down V (like the Greek letter "
    "lambda): from that little point a short curved line runs out to each side and stops under the inner corner of each "
    "eye. Directly under it sits a small round pale chin. The whole mouth is only about 110 px wide. The corners do NOT "
    "turn up: NO smile, no grin, no long mouth line across the face, no teeth, no fangs, no tongue. Two tiny ink nostril "
    "dots just above the lip point.\n"
    "- EYES: very large, set far apart on the two SIDES of the head at its widest part; the outer edge of each eye lies on "
    "the side outline of the head and bulges out of it a little, as on a real snake. The left eye is the bigger one (about "
    "100 px wide and 110 px tall); the right eye is seen a little narrower (about 75 px wide and 105 px tall). Each eye: "
    "amber orange with a tall black vertical slit pupil and ONE small white catchlight dot; its upper inner part is covered "
    "by a heavy cobalt-blue eyelid with a thick ink edge that slants DOWN toward the middle of the face: a cold, focused, "
    "challenging snake stare straight at the viewer.\n")

HORN_TAIL1 = (
    "- TWO HEAD HORNS (charcoal black): one on the upper LEFT and one on the upper RIGHT of the crown, above the eyes, like "
    "the two ears of a cat seen from the front. Each grows straight out of the skin: at its base the blue skin and the "
    "black horn meet in a small zigzag edge of three or four little points, with no ring and no socket. Each horn is a "
    "smooth, solid, slightly curved horn with a wide base and a needle-sharp tip, rising UP and leaning outward, its tip "
    "curling a little inward like a flame; the left horn about 160 px long, the right horn about 135 px. Elegant and clean: "
    "no branches, no fluff. Two thin dark-grey ridge lines near each base.\n"
    "- TAIL HORN (charcoal black, the same horn material): the END OF THE TAIL ITSELF has hardened into one big black horn, "
    "as big as the head is tall. It is NOT a knife, NOT a weapon tied on, NOT a separate object: no handle, no ring, no "
    "collar, no binding, no guard. The blue tail narrows to about 55 px and the horn grows seamlessly out of it; blue skin "
    "and black horn meet in a zigzag edge of four or five little points, exactly like at the base of the head horns. "
    "SHAPE: graceful and organic, with only a HINT of a kunai / spearhead: a slender leaf-shaped blade about 290 px long "
    "and 120 px wide; from its narrow base it swells in two smooth curves to its widest point at about one third of its "
    "length, then tapers in two long, slightly concave curves to a needle-sharp tip; the whole horn leans in one gentle "
    "curve like a talon or a tongue of flame, its tip pointing UP and curling slightly to the right. One small sharp "
    "back-pointing barb on each side near the base. One thin dark-grey ridge line along its centre, following the curve. "
    "Smooth flowing edges drawn by hand: no straight ruler lines, no hard geometric diamond. It is rigid like a horn: not "
    "soft, not a fin, not a tuft.")

FORM1 = ("CREATURE: a HORNED WATER SNAKE monster of the water element for a monster-collecting game: a small, chubby sea "
         "serpent with two black horns on its head, whose tail ends in a big black horn. Cute and compact, but with a cold, "
         "determined, ready-to-strike attitude: not a cheerful mascot and not scary. A pure snake: NO arms, NO legs, NO "
         "fins, NO wings, NO hair or fur tufts, NO whiskers.\n"
         "FORM 1, the first and smallest form (a young snake, chubby and short):\n"
         "- BODY, one smooth, FAT, chubby tube (about 190 px thick on the neck, more than half as wide as the head; it gets "
         "thinner only toward the tail). Short and plump like a sausage, not a thin rope. Read it from head to tail:\n"
         "  1. the HEAD is at the upper left-centre of the figure, held high;\n"
         "  2. the NECK drops from the head down to the ground in a gentle S, leaning to the right as it goes down. We see "
         "it from the front: its broad pale BELLY faces the viewer and fills most of its width; the blue back shows only as "
         "a band along its LEFT edge;\n"
         "  3. on the ground the body makes ONE round COIL: from the bottom of the neck it sweeps to the LEFT and curls "
         "around like a snail spiral lying on the ground at the lower left of the figure; here we see the blue back of the "
         "body (a big round blue loop, as tall as one third of the figure), which passes BEHIND the bottom of the neck. The "
         "neck with its pale belly stands in front of the loop. This is the only place where the body overlaps itself;\n"
         "  4. the TAIL: the body comes out from behind the neck on the RIGHT at ground level, runs to the right along the "
         "ground for about 150 px (blue back on top) while getting thinner, then turns UP at the far right, where the big "
         "TAIL HORN rises, standing up like a scorpion's sting held ready.\n"
         "- BACK AND BELLY: the back of the body and the top of the head are cobalt blue; the belly, the throat and the "
         "underside are pale ice blue. The two colours meet along one smooth line running the whole length of the body. On "
         "the belly, four or five thin curved cross lines (belly scales), widely spaced. On the blue back, five or six "
         "round light-aqua BUBBLE SPOTS of different sizes (20 to 45 px), scattered in a loose row. No other pattern, no "
         "scales, no swirls.\n"
         + VIEW_HEAD + HORN_TAIL1)

FRAME1 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
          "visible, nothing cut by the edges. The whole figure is about 760 px wide and about 720 px tall (from the horn tips "
          "to the bottom of the coil), centred horizontally; the bottom of the coil is about 140 px above the bottom edge of "
          "the image. The tip of the tail horn is about level with the snake's eyes.")

PALETTE2 = ("COLOURS (use exactly these, each area one flat colour; the back is now much darker than form 1): back and top of "
            "the head deep navy indigo (#22388F); round bubble spots on the back light aqua (#86D6F0); a row of small pointed "
            "back plates along the spine cobalt blue (#2E6FD8); belly, throat and lower jaw pale ice blue (#DDF0F7, never left "
            "as bare white paper) with belly lines a little darker (#A9CFE2); horns and the tail horn charcoal black "
            "(#26252C) with thin dark-grey ridge lines (#5B5B68); fangs cream (#FBF1D2); eyes amber orange (#FFA92E) with a "
            "black vertical slit pupil; every outline dark-brown ink (#2B2118).")

FORM2 = ("CREATURE: the GROWN, FIERCER FORM of the horned water snake of image 1 (form 1, approved): the same creature and "
         "the same drawing style, but clearly LONGER, BIGGER, darker and more dangerous: an adult sea serpent, no longer a "
         "chubby baby. A pure snake: NO arms, NO legs, NO fins, NO wings, NO hair or fur tufts, NO whiskers.\n"
         "FORM 2:\n"
         "- PROPORTIONS: adult, not chibi: the head is only about one quarter of the figure's height, the body is much "
         "longer (about twice the length of form 1) and powerful, about 170 px thick, thinner only in its last third.\n"
         "- BODY, read from head to tail:\n"
         "  1. the HEAD is at the upper left-centre, held very high, lowered a little and looking out at the viewer, like a "
         "cobra about to strike;\n"
         "  2. the NECK rises tall in a strong S-curve, seen from the front as in image 1: its broad pale belly faces the "
         "viewer, the dark back shows as a band along its left edge; from the head it goes down, swings to the right like "
         "a puffed chest, then back to the left, down to the ground. It is about twice as tall as the neck of image 1;\n"
         "  3. on the ground, at the lower left and behind the bottom of the neck, the body makes TWO big round COILS (a wide "
         "loop lying on the ground and a second loop resting on it and a little behind it), showing the dark back with its "
         "bubble spots; together they are wider and taller than the single coil of image 1. The neck stands in front of "
         "the coils. Every place where the body passes in front of itself has a clear ink outline, and the body never "
         "crosses itself anywhere else;\n"
         "  4. the TAIL comes out of the coils on the RIGHT, runs along the ground to the right while getting thinner, then "
         "bends UP and rises high on the right side of the figure, like a scorpion's sting held ready, ending in the big "
         "TAIL HORN.\n"
         "- BACK AND BELLY: back and top of the head deep navy indigo; belly, throat and underside pale ice blue, the two "
         "colours meeting along one smooth line the whole length of the body. Thin cross lines (belly scales) on the belly. "
         "On the back, eight to ten round light-aqua bubble spots of different sizes. Along the spine of the neck, a row of "
         "five small pointed cobalt-blue back plates (low triangles, about 35 px).\n"
         "- HEAD: the same snake head and the same view as image 1 (seen from the front and a little from above, chin tucked "
         "in, staring at the viewer from under its brows, one eye on each side of the head, the blue of the crown coming "
         "down between the eyes), but adult: longer, flatter and more angular, a broad viper spade shape with strong jaw "
         "corners and a wedge-shaped snout at the bottom. The same small low snake mouth shaped like an upside-down V with a "
         "little point in the middle, closed, no smile; but now TWO cream FANGS (about 40 px long) hang down from the upper "
         "lip, one on each side of the lip point. Two ink nostril slits.\n"
         "- EYES: narrower and meaner than form 1: amber orange with a black vertical slit pupil, one small white catchlight "
         "dot, the upper half covered by a very heavy navy eyelid with a thick ink edge slanting down toward the middle of "
         "the face. The left eye about 85 px wide and 65 px tall, the right eye about 65 px wide.\n"
         "- TWO HEAD HORNS (charcoal black), much bigger than form 1, in the same places and growing out of the skin through "
         "the same zigzag edge: each a long curved horn rising UP and outward, about 240 px long (left) and 200 px (right), "
         "each with ONE short sharp side prong near its middle. Thin dark-grey ridge lines near the base.\n"
         "- TAIL HORN (charcoal black), bigger and more dangerous than in image 1 but the same idea: the end of the tail "
         "itself hardened into a horn, growing seamlessly out of the tail through a zigzag edge (no handle, no ring, no "
         "collar), a graceful curved leaf / spearhead shape that only hints at a kunai, about 380 px long and 150 px wide, "
         "needle-sharp tip pointing UP and curling slightly to the right, now with TWO sharp back-pointing barbs on each "
         "side near the base and a thin dark-grey ridge line along its centre. Smooth flowing hand-drawn edges.")

FRAME2 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
          "visible, nothing cut by the edges. The whole figure is about 980 px wide and about 900 px tall (from the horn tips "
          "to the bottom of the coils), centred horizontally; the bottom of the coils is about 50 px above the bottom edge of "
          "the image.")

POSE = ("VIEW AND POSE (very important: the picture will be cut into separate parts and animated with a 2D skeleton): "
        "front three-quarter view seen a little from above: the snake rests still, coiled and alert, its head lowered and "
        "looking out at the viewer, its body opening toward the viewer's RIGHT (coil on the left, tail on the right). The "
        "raised tail horn stands completely clear of the neck and the head: at least 60 px of pure white between the tail "
        "horn and the neck all the way up, and the tail horn touches nothing. The head does not overlap the "
        "coil: the chin is at least 40 px above the coil. The body tube keeps a clear ink outline wherever one part of it "
        "passes in front of another. No water, no bubbles in the air, no splashes, no rocks, no effects anywhere.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn curves, a little lopsided like a real animal, not "
        "perfect circles; the ink line is visibly wobbly and uneven in thickness like a real pen, not a vector stroke; loose "
        "crayon hatching is clearly visible inside every area, also inside the black horns (dark crayon strokes on charcoal).")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images: drawn by hand on paper with a dark-brown "
        "ink pen (#2B2118), an outline about 7 px thick on this canvas, the same weight on every edge, a closed outline "
        "around every part; every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal "
        "hatching (strokes thinner than the outline), kept inside the outline. Clean and appealing, few details, neither a "
        "crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, no shadow under the figure, "
        "on the ground or on the background), no white highlights or shine spots (also none on the black horns), "
        "no gloss, no wet look, no reflections, no glow, no rim light, no gradients, no 3D look. The only white allowed is "
        "one small catchlight dot in each eye. A different tone appears only where the design itself lists a different colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no frame, no props, no effects around "
      "the creature.")


def refs_of(k):
    style = [
        (DROP, "an approved hero of the same game (a water-blob creature), 1536x1024, white background: match EXACTLY its "
               "wobbly pen line, its visible crayon hatching and its completely flat colouring. Do NOT copy its species, "
               "design, face or colours.",
         "Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): giọt nước lam mắt bầu dục. Chỉ lấy nét bút rung, vân sáp, tô phẳng"),
        (SHARK, "another approved hero of the same game (a blue shark beast), 1536x1024, white background: see how fierce "
                "eyes and a determined expression are drawn simply in this style. Do NOT copy its species, design or "
                "colours.",
         "Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): cá mập xanh lam bốn chân. Lấy cách vẽ mắt dữ, nét mặt quả quyết"),
        (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + "
                      "coloured pencil / wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp"),
    ]
    if k == 1:
        return style
    return [(ref1(), "FORM 1 of THIS creature, 1536x1024, white background: keep its front view from slightly above, its "
                     "lowered head staring at the viewer, its snake face, its coil at the lower left and tail raised on "
                     "the right, its blue back with bubble spots and broad pale belly, its amber slit eyes, its two black "
                     "head horns, its black tail horn and its drawing style. Form 2 is the same snake grown longer, "
                     "bigger and fiercer, with a darker back. Do NOT copy its chubby baby proportions.",
             "Rắn sừng dạng 1 đã chọn (1536 × 1024, nền trắng): rắn con lam cô-ban cuộn một vòng, sừng đen, sừng đen ở chót đuôi")
            ] + style


FORMS = {1: ("rắn nước có sừng dạng 1", FORM1, PALETTE1, FRAME1), 2: ("rắn nước có sừng dạng 2", FORM2, PALETTE2, FRAME2)}

CHECK = {
    1: ["Rắn con **mập**, nhìn **gần chính diện từ trên xuống**, đầu cúi, mắt nhìn ra người xem; bụng nhạt quay ra trước, thân "
        "**cuộn một vòng** ở dưới trái, đuôi vươn sang phải rồi **dựng lên**.",
        "**Đầu rắn** hình trứng, hai mắt to ở **hai bên đầu**, mảng lam từ đỉnh đầu chạy xuống giữa hai mắt; **miệng nhỏ, thấp**, "
        "hình chữ V ngược có mỏm nhọn ở giữa; không cười, không mõm dài.",
        "**Hai sừng đen** trên đỉnh đầu (chỗ chùm lông của con gốc): chóp nhọn, cứng, không nhánh, không lông.",
        "**Chót đuôi là sừng đen** mọc liền từ đuôi (mép răng cưa, không cán, không vòng), dáng lá thon cong, chóp nhọn, chỉ hơi "
        "hướng kunai; cứng, không phải vây hay chùm lông.",
        "Lưng lam cô-ban có vài đốm bong bóng lam nhạt, bụng lam băng có vạch ngang; mắt hổ phách con ngươi dọc, mày xếch; miệng khép.",
        "Đuôi và sừng đuôi **tách hẳn** khỏi cổ, đầu (khe trắng ≥ 60 px); cằm không đè lên vòng cuộn; chỗ thân đè nhau có viền mực rõ.",
        "Tô phẳng: **không** bóng, không điểm sáng (trừ chấm mắt), sừng đen không bóng loáng; viền mực nâu; nền trắng tinh; không nước, bong bóng bay."],
    2: ["Cùng con với dạng 1 nhưng **dài, to, dữ hơn**: không còn chibi (đầu chừng 1/4 chiều cao), **hai vòng cuộn**, cổ dựng cao chữ S.",
        "Lưng **chàm đậm**, hàng vảy nhọn lam trên sống cổ, nhiều đốm bong bóng hơn.",
        "Sừng dài hơn hẳn, mỗi sừng **một nhánh nhọn**; **hai nanh kem** lộ ra dù miệng khép; mắt hẹp, mày rất dày.",
        "Sừng đuôi **to hơn, mỗi bên hai ngạnh** ở gốc; đuôi dựng cao bên phải, tách hẳn khỏi cổ.",
        "Tô phẳng, không bóng, nền trắng tinh; chỗ thân đè nhau có viền mực rõ."],
}

FIX = [("Có bóng, mảng sáng tối, điểm sáng trên sừng", "Flat colour only: remove every shadow, highlight, shine spot and "
                                                       "gradient, also on the black horns; keep the crayon hatching "
                                                       "as texture only."),
       ("Đuôi đè lên cổ, đầu hoặc chạm sừng", "Move the raised tail further to the right: at least 60 px of pure white between "
                                              "the tail horn and the neck, head and horns."),
       ("Chót đuôi mềm như vây, lá, chùm lông", "The tail ends in a HARD black horn growing seamlessly out of the tail: a "
                                                "slender curved leaf shape with a needle-sharp tip, stiff like a horn."),
       ("Chót đuôi thô như con dao gắn vào (có cán, vòng, hình thoi thẳng)",
        "The tail horn is not a knife or a separate object: remove the handle, ring and collar; it grows out of the tail "
        "through a zigzag edge, with smooth flowing hand-drawn curves and a gently curved tip, only hinting at a kunai."),
       ("Đầu nhìn nghiêng, mõm chìa ngang, miệng cười dài",
        "Redraw the head seen from the FRONT and slightly from above, chin tucked in, looking at the viewer: an egg-shaped "
        "snake head with one big eye on each side, the snout at the bottom, and a small low mouth shaped like an "
        "upside-down V with a little point in the middle. No smile, no long muzzle."),
       ("Sừng có nhánh, có lông, hoặc thành tai", "The two head horns are plain smooth charcoal-black cones, slightly curved, "
                                                 "sharp tips, no branches, no fur, not ears."),
       ("Thân cuộn rối, nhiều chỗ đè nhau", "Simplify the body: ONE flat loop on the ground only; the neck stands in front of "
                                           "it; the tail leaves to the right. No other crossing."),
       ("Quay sang trái hoặc nhìn thẳng", "Turn the snake three-quarters toward the viewer's RIGHT: snout and both eyes on "
                                          "the right side of the head, tail raised on the right."),
       ("Có tay, chân, vây, râu, lưỡi thè, nước", "Remove them: only the snake body, head, eyes, two horns and the tail "
                                                  "horn, mouth closed, on pure white."),
       ("Dạng 2 không khác dạng 1 mấy", "Make form 2 much longer and bigger in the frame, adult proportions with a smaller "
                                        "head, a deep navy back, two coils, long pronged horns, visible fangs and a larger "
                                        "barbed tail horn.")]


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
          "Tướng thứ 5 đảo Thủy, làm 2026-11-11 theo ý người dùng: rắn nước có hai sừng đen, chót đuôi là sừng đen nhọn kiểu "
          "kunai. Màu thân là đề xuất của Claude, chờ người dùng duyệt. Ghi chú thiết kế và mổ xẻ con gốc: "
          "`ArtGen/Spine/inbox/ran_sung_ghichu.md`.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{W(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_1_concept.txt` "
          "(thêm `--note \"...\"` để sửa nhanh).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(r)}` | {vi} |" for i, (r, _, vi) in enumerate(refs, 1)]
    gd += ["", "Không đính ảnh con gốc của game tham khảo; thiết kế chỉ tả bằng lời.", "",
           f"Chỗ lưu: `{W(save_dir(k))}`. Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK[k]]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    open(os.path.join(pk(k), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p


# ---------------------------------------------------------------- lượt sửa dạng 1: giữ bản nháp, vẽ lại đầu theo sơ đồ bố cục
# Người dùng (2026-11-11, sau L1_sua.png): "nhìn kĩ lại phần miệng và đầu rắn, hơi nghiêng sang bên kia chứ không chính diện, phần
# miệng làm giống con gốc". Đầu con gốc quay ba phần tư sang phải nhìn từ trên xuống: mắt gần to lùi vào trong viền trái, mắt xa
# hẹp nằm trên viền phải, mõm lệch xuống dưới phải; miệng là đường cong chữ U mềm ôm đáy mặt, khấc nhỏ ở mõm; mảng màu lưng dừng
# trên môi, môi trên và hàm dưới màu bụng. Tả lời hai lượt đều lệch (nhìn nghiêng hẳn, rồi chính diện mõm nhọn chữ V) nên đính sơ đồ
# bố cục tự vẽ (ran_sung_bo_cuc.py).
GUIDE = os.path.join(HERE, "inbox", CODE + "_1", "mau", "dau_bo_cuc.png")
DRAFT = os.path.join(HERE, "inbox", CODE + "_1", "tai_ve", "L1_sua.png")

FIX_HEAD = (
    "REDRAW THE HEAD, following the LAYOUT of image 2. In image 1 the head is seen straight from the front and its snout is "
    "a sharp V like a beak; that is wrong. The head must be turned THREE-QUARTERS toward the viewer's RIGHT and seen a "
    "little from above, with a soft rounded snake snout. Same place on the neck, same size as now (about 330 px wide and "
    "300 px tall without the horns), same colours. Copy from image 2 where things are, not how they are drawn:\n"
    "- OUTLINE: a smooth rounded egg / dome, no corners: a big round crown on top, widest at eye level, the lower part a "
    "soft, blunt, ROUNDED snout that sits at the lower RIGHT of the head (not in the middle, not pointed).\n"
    "- THE TWO EYES ARE DIFFERENT because the head is turned: the LEFT (near) eye is big and almost round (about 115 px "
    "wide, 110 px tall), fully visible, and sits INSIDE the face: between it and the left outline of the head there is a "
    "strip of blue head about 40 px wide. The RIGHT (far) eye is a tall narrow oval (about 55 px wide, 105 px tall) lying ON "
    "the right outline of the head, its outer edge bulging slightly out of the silhouette. The gap between the two eyes "
    "(the forehead and bridge of the snout) is wide, about 190 px, and blue.\n"
    "- EYE DETAILS: amber orange, a tall black vertical slit pupil, ONE small white catchlight dot. The top of each eye is "
    "covered by a heavy cobalt-blue eyelid whose lower edge is one thick straight ink line slanting DOWN toward the middle "
    "of the face (toward the right for the left eye, toward the left for the right eye): a cold, focused stare. Both "
    "pupils sit low and toward the snout: the snake looks down and to the right. No separate eyebrow strokes.\n"
    "- COLOUR AREAS: cobalt blue covers the crown, the strip left of the near eye, and comes down between the two eyes as "
    "a broad band with a ROUND bottom end that stops about 30 px ABOVE the mouth. Pale ice blue: a band under both eyes "
    "and under that round blue end (the upper lip), and the lower jaw.\n"
    "- MOUTH (make it exactly this shape): ONE long, smooth, gently curved line, like a wide shallow letter U, hugging the "
    "bottom of the face: it starts under the outer (left) corner of the near eye, sweeps down and to the right along the "
    "bottom of the face, and rises again at the far right to end on the right outline of the head just below the far eye. "
    "At the snout tip, about two thirds of the way from left to right, the line makes ONE small upward notch, a tiny "
    "pointed peak about 25 px tall and 45 px wide (like a small letter A without the bar): the little gap a snake flicks "
    "its tongue through. Everywhere else the line is a calm round curve: no V-shaped beak, no zigzag, no smile corners "
    "curling up, no frown. Under the line, the lower jaw shows as a thin pale crescent (about 22 px thick at the snout, "
    "fading to nothing toward the left), forming the bottom outline of the head. Mouth closed: no teeth, no fangs, no "
    "tongue.\n"
    "- NOSTRILS: two tiny short ink slits on the blue snout just above the notch.\n"
    "- HEAD HORNS: where image 2 shows them, on the upper left and upper right of the crown, drawn like the horns of "
    "image 1 (charcoal black, smooth, curved, sharp tips, growing out of the skin with a short zigzag edge), the left one "
    "a little bigger. Short thin dark-grey ridge lines near the base only, no long light streaks.")

FIX_HORN = (
    "TIDY THE TAIL HORN a little: keep its place, size, charcoal black colour, the single thin dark-grey centre line and "
    "the way it grows out of the blue tail. Make its outline a clean, elegant, slightly curved leaf / spearhead (a soft "
    "hint of a kunai blade): smooth edges on both sides, widest at one third of its length, needle-sharp tip, and exactly "
    "ONE small sharp back-pointing barb on each side near the base. No other notches, no ragged or feathery edge. The "
    "zigzag where blue skin meets the black horn is short: three small points.")

FIX_KEEP = (
    "KEEP EVERYTHING ELSE EXACTLY AS IN IMAGE 1: the size and place of the figure in the frame, the fat neck with its broad "
    "pale belly and belly lines, the blue back as a band on the left with its bubble spots, the big round blue coil at the "
    "lower left with its spiral line, the tail running to the right along the ground and turning up at the far right, all "
    "colours, the wobbly dark-brown ink outline (about 7 px), the visible crayon hatching, the completely flat colouring. "
    "Because the head now turns to the right, the neck may meet it a little more from the left; nothing else moves.")

FIX_STYLE = (
    "Image 2 is only a LAYOUT DIAGRAM: flat computer shapes with clean lines. Take from it the direction the head is "
    "turned, the position and size of the eyes, the colour areas and the shape and place of the mouth line. Do NOT copy "
    "its smooth vector look: draw the head in the hand-drawn style of image 1, with the same wobbly ink line and crayon "
    "hatching, so that head and body look drawn by the same hand.")


def build_fix():
    """Lượt sửa dạng 1 trên bản nháp L1_sua.png + sơ đồ bố cục đầu → L1_sua_2.png (trùng tên thì _3...)."""
    k = 1
    refs = [(DRAFT, "OUR CURRENT DRAFT of this creature, 1536x1024, white background: a chubby blue horned water snake, "
                    "coiled, with a black tail horn. Its body, coil, tail, colours, framing and drawing style are right "
                    "and must be kept. Its HEAD is wrong (seen straight from the front, with a pointed V-shaped snout) and "
                    "must be redrawn.",
             "Bản sửa 1 (1536 × 1024, nền trắng): rắn lam mập cuộn một vòng ở dưới trái, đuôi dựng bên phải có sừng đen; đầu "
             "nhìn chính diện, mõm nhọn chữ V. Giữ thân, màu, nét; vẽ lại đầu"),
            (GUIDE, "a LAYOUT DIAGRAM of the head only, 700x700, white background, flat computer-drawn shapes: it shows the "
                    "head turned three-quarters to the viewer's right and seen from above, the big near eye inside the face "
                    "on the left, the narrow far eye on the right outline, the blue area coming down between the eyes, the "
                    "pale lips, the long U-shaped mouth line with one small notch at the snout, and where the two horns "
                    "stand. Use it for layout only, not for style.",
             "Sơ đồ bố cục đầu tự vẽ (700 × 700, nền trắng, hình phẳng): đầu lam quay ba phần tư sang phải, mắt trái to tròn, "
             "mắt phải hẹp trên viền, môi nhạt, đường miệng chữ U có khấc nhỏ lệch phải, hai sừng đen. Chỉ lấy bố cục"),
            (DROP, "an approved hero of the same game, 1536x1024: reference for the wobbly pen line, the crayon hatching "
                   "and the flat colouring only. Do NOT copy its design.",
             "Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): chỉ lấy nét bút rung, vân sáp, tô phẳng")]
    check(refs)
    out = os.path.join(save_dir(k), "L1_sua_2.png")
    p = os.path.join(pk(k), "luot_1_sua.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as L1_sua_3.png, L1_sua_4.png ... in the same folder. Do not edit, "
          "move or delete any other file.", "",
          "TASK: redraw the creature of image 1 as ONE new picture: the same snake, same pose, same size, with its head "
          "redrawn in the layout of image 2 and its tail horn tidied.", "",
          FIX_KEEP, "", FIX_HEAD, "", FIX_STYLE, "", FIX_HORN, "", PALETTE1, "", SOFT, LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = [f"# Gói gửi GPT: dòng `{CODE}` dạng 1, lượt sửa (đầu rắn quay ba phần tư, miệng chữ U có khấc)", "",
          "Người dùng chê: bản 1 đuôi thô, đầu miệng không giống rắn, hướng nhìn sai; bản sửa 1 đầu chính diện, mõm nhọn chữ V "
          "(\"hơi nghiêng sang bên kia chứ không chính diện, phần miệng làm giống con gốc\"). Lượt này giữ thân của bản sửa 1, "
          "vẽ lại đầu theo **sơ đồ bố cục tự vẽ** (`py -3 -I ArtGen/Spine/ran_sung_bo_cuc.py`), gọn lại sừng đuôi.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{W(out)}` (trùng tên thì `_3`, `_4`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_1/luot_1_sua.txt`.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(r)}` | {vi} |" for i, (r, _, vi) in enumerate(refs, 1)]
    gd += ["", "## Kiểm", "",
           "- Đầu **quay ba phần tư sang phải**, nhìn từ trên xuống: mắt trái to tròn nằm trong mặt (còn dải lam bên trái nó), "
           "mắt phải hẹp nằm **trên viền phải**; mõm tù tròn ở **dưới phải**.",
           "- **Miệng**: một đường cong chữ U mềm ôm đáy mặt, **một khấc nhọn nhỏ** ở mõm (khoảng 2/3 từ trái sang); không chữ V "
           "nhọn, không cười; hàm dưới là vành nhạt mỏng.",
           "- Mảng lam từ đỉnh đầu chạy xuống giữa hai mắt, **đáy tròn, dừng trên miệng**; môi trên và hàm dưới lam băng.",
           "- Mí lam dày, mép mực xếch vào giữa mặt; con ngươi dọc nhìn xuống phải.",
           "- Sừng đuôi dáng lá gọn, mỗi bên một ngạnh nhỏ; thân, vòng cuộn, màu, nét, cỡ hình giữ như bản sửa 1.",
           "- Đầu vẫn nét vẽ tay (viền rung, vân sáp), không nhẵn như sơ đồ."]
    open(os.path.join(pk(k), "HUONG_DAN_sua.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p


# ---------------------------------------------------------------- dạng 2: giữ thân bản thử, vẽ lại đầu theo đầu dạng 1 đã chốt
# Bản thử dạng 2 (L1_thu.png) gen theo bản nháp cũ của dạng 1 nên đầu còn nhìn chính diện, mõm nhọn chữ V. Dạng 1 đã chốt
# (L1_duyet.png: đầu quay ba phần tư sang phải, miệng chữ U có khấc). Lượt này giữ thân, vòng cuộn, sừng của bản thử, vẽ lại đầu.
DRAFT2 = os.path.join(HERE, "inbox", CODE + "_2", "tai_ve", "L1_thu.png")

FIX2_HEAD = (
    "REDRAW THE HEAD of image 1 so that it is the ADULT version of the head of image 2 (form 1, approved). In image 1 the "
    "head is seen straight from the front with a sharp V-shaped beak-like snout; that is wrong. Same place on top of the "
    "neck, about the same size as now, same deep navy colour. Take the construction from image 2:\n"
    "- VIEW: turned THREE-QUARTERS toward the viewer's RIGHT and seen a little from above, head lowered, chin tucked in.\n"
    "- OUTLINE: a smooth rounded dome on top, widest at eye level, with a soft blunt rounded snout at the lower RIGHT; a "
    "little longer, flatter and more angular at the jaw corners than the baby head of image 2, but clearly the same head.\n"
    "- EYES, as in image 2: the LEFT (near) eye big, fully visible, sitting inside the face with a strip of navy head left "
    "of it; the RIGHT (far) eye a tall narrow oval lying on the right outline of the head. Amber orange, black vertical "
    "slit pupil, one small white catchlight dot. FIERCER than image 2: the heavy navy eyelids cover the upper half of each "
    "eye and their thick ink lower edges slant STEEPLY down toward the middle of the face (an angry, threatening glare, "
    "not sleepy); pupils low and toward the snout.\n"
    "- COLOUR AREAS, as in image 2: navy on the crown and between the eyes, ending in a round shape above the mouth; pale "
    "ice blue on the band under the eyes (upper lip) and on the lower jaw.\n"
    "- MOUTH, the same as image 2: ONE long, smooth, wide U-shaped lip line hugging the bottom of the face, from under the "
    "outer corner of the near eye to the right outline below the far eye, with ONE small upward pointed notch at the snout "
    "tip (about two thirds of the way from left to right); a thin pale lower-jaw crescent under it. Mouth closed, no smile. "
    "NEW in form 2: TWO cream FANGS (#FBF1D2), each about 45 px long and 16 px wide, slightly curved, hang DOWN from the "
    "upper lip over the lower jaw, one on each side of the notch (about 45 px away from it). No tongue.\n"
    "- NOSTRILS: two short ink slits on the navy snout above the notch.\n"
    "- HORNS: keep the two big pronged black horns of image 1 exactly as they are (place, size, shape); where the head "
    "turns they stay on the upper left and upper right of the crown.")

FIX2_KEEP = (
    "KEEP EVERYTHING ELSE EXACTLY AS IN IMAGE 1: the tall S-shaped neck with its broad pale belly and belly lines, the row "
    "of cobalt-blue back plates along the back of the neck, the two big navy coils with their light-aqua bubble spots, the "
    "tail running to the right and rising, the big black tail horn with its barbs and centre line, all colours, the wobbly "
    "dark-brown ink outline (about 7 px), the visible crayon hatching, the completely flat colouring.")

FIX2_FRAME = (
    "FRAMING: draw the whole figure a little smaller than in image 1, so that there are at least 70 px of pure white "
    "between the figure (horn tips, tail horn, coils) and every edge of the 1536x1024 canvas. Nothing cut by the edges.")


def build_fix2():
    """Dạng 2: bản thử L1_thu.png + đầu dạng 1 đã chốt → L1_concept_2.png (trùng tên thì _3...)."""
    k = 2
    refs = [(DRAFT2, "OUR CURRENT DRAFT of form 2 of this creature, 1536x1024, white background: a big dark navy horned "
                     "sea serpent with two coils, a tall neck, pronged black horns and a large black tail horn. Its body, "
                     "coils, tail, horns, colours and drawing style are right and must be kept. Its HEAD is wrong and must "
                     "be redrawn.",
             "Bản thử dạng 2 (1536 × 1024, nền trắng): rắn chàm đậm hai vòng cuộn, cổ cao, sừng có nhánh, sừng đuôi to; đầu "
             "nhìn chính diện, mõm nhọn. Giữ thân, vẽ lại đầu"),
            (chosen(1), "FORM 1 of this creature (approved), 1536x1024, white background: the small chubby baby form. Use "
                        "its HEAD as the model for the view (turned three-quarters right, seen from above), the eye "
                        "placement, the colour areas and the U-shaped mouth line with one small notch. Do NOT copy its "
                        "baby proportions or its lighter blue.",
             "Rắn sừng dạng 1 đã chốt (1536 × 1024, nền trắng): rắn con lam, đầu quay ba phần tư sang phải, miệng chữ U có "
             "khấc. Lấy cách dựng đầu, miệng"),
            (DROP, "an approved hero of the same game, 1536x1024: reference for the wobbly pen line, the crayon hatching "
                   "and the flat colouring only. Do NOT copy its design.",
             "Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): chỉ lấy nét bút rung, vân sáp, tô phẳng")]
    check(refs)
    os.makedirs(pk(k), exist_ok=True)
    out = os.path.join(save_dir(k), "L1_concept_2.png")
    p = os.path.join(pk(k), "luot_1_sua.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as L1_concept_3.png, L1_concept_4.png ... in the same folder. Do "
          "not edit, move or delete any other file.", "",
          "TASK: redraw the creature of image 1 as ONE new picture: the same big snake in the same pose, with its head "
          "redrawn as the adult version of the head of image 2.", "",
          FIX2_KEEP, "", FIX2_HEAD, "", FIX2_FRAME, "", PALETTE2, "", SOFT, LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = [f"# Gói gửi GPT: dòng `{CODE}` dạng 2, lượt sửa (đầu theo dạng 1 đã chốt)", "",
          "Dạng 1 đã chốt 2026-11-11 (`L1_duyet.png`). Bản thử dạng 2 đúng thân nhưng đầu còn nhìn chính diện, mõm nhọn. Lượt "
          "này giữ thân của bản thử, vẽ lại đầu: quay ba phần tư sang phải, miệng chữ U có khấc như dạng 1, thêm hai nanh, mí "
          "xếch dốc cho dữ.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{W(out)}` (trùng tên thì `_3`, `_4`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_2/luot_1_sua.txt`.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(r)}` | {vi} |" for i, (r, _, vi) in enumerate(refs, 1)]
    gd += ["", "## Kiểm", "",
           "- Đầu **quay ba phần tư sang phải** như dạng 1: mắt trái to trong mặt, mắt phải hẹp trên viền phải, mõm tù ở dưới phải.",
           "- **Miệng chữ U có một khấc nhỏ** như dạng 1, thêm **hai nanh kem** hai bên khấc; không cười.",
           "- Mí chàm dày, **xếch dốc** vào giữa mặt: dữ, không lừ đừ.",
           "- Thân, hai vòng cuộn, hàng vảy sống cổ, sừng có nhánh, sừng đuôi to giữ như bản thử; hình cách mép khung ≥ 70 px.",
           "- Tô phẳng, không bóng, nền trắng tinh."]
    open(os.path.join(pk(k), "HUONG_DAN_sua.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p


# ---------------------------------------------------------------- lượt 2: RESKIN: vẽ đè da mới lên tờ mảnh của rig gốc
# Người dùng chốt 2026-11-11: "xóa hết đi mà xây lại, gen y hệt con gốc rồi reskin thôi". Giữ nguyên rig Spine gốc (monster_3247: xương,
# lưới, trọng số, animation), chỉ vẽ lại DA từng mảnh. `ran_sung.py to k` dựng hai tờ mảnh gốc phóng 3 lần (goc_A: thân, goc_B: đầu);
# GPT vẽ đè lên, GIỮ hình bóng, chỗ, cỡ từng mảnh; `ran_sung.py nhan k` cắt về. Ảnh mảnh gốc được đính làm mẫu (người dùng cho phép,
# như hình aola): không đăng công khai.
RESKIN_TASK = (
    "TASK (RESKIN): image 2 is a sheet of separate PARTS of a cartoon snake, used for 2D skeletal animation: each part is "
    "attached to an animation skeleton by its exact outline. Repaint EVERY part as the matching part of OUR snake (image 1), "
    "changing only its colours, its surface details and its drawing style. Each part must keep exactly its SILHOUETTE, its "
    "PLACE and its SIZE on the sheet: laid over image 2, the outline of each new part coincides with the old one within a "
    "few pixels (unless a part below says otherwise). Do not add, remove, move, rotate, mirror, resize or merge parts; do "
    "not draw the whole snake.")

RESKIN_COLOUR = (
    "COLOUR CHANGE, for all parts:\n"
    "- every TEAL / grey-green area (the snake's back) becomes cobalt blue (#2E6FD8). Remove the darker blotches and the "
    "angular key-shaped pattern lines of the old parts; instead put two to four round light-aqua BUBBLE SPOTS (#86D6F0, flat "
    "discs without outline, different sizes) on each larger blue area;\n"
    "- every PINKISH CREAM area (the snake's belly) becomes pale ice blue (#DDF0F7, never left as bare white paper); keep the "
    "border between back and belly exactly where it is;\n"
    "- black outlines become a wobbly hand-drawn dark-brown ink line (#2B2118), about 6 px thick on this sheet, following "
    "exactly the old outline. Where an old part has a SOFT pale edge instead of a black outline (the lower ends of some body "
    "pieces), keep it soft: draw that edge as a light-blue line (#A9CFE2), not in ink;\n"
    "- style of image 1: flat colours with visible coloured-pencil / wax-crayon hatching, no shading, no highlights, no "
    "gradients, no glow.")

RESKIN_A = (
    "THE PARTS OF THIS SHEET (image 2):\n"
    "Top row, from left to right:\n"
    "1. UPPER NECK (a tall bean): blue back band along its left side, pale belly on the rest; add two thin curved belly "
    "lines (#A9CFE2) across the belly; its lower end keeps its soft light-blue edge.\n"
    "2. CHEST (a kidney bean): blue back on its left, pale belly; add two thin curved belly lines; its lower-left end keeps "
    "its soft edge.\n"
    "3. COIL SEGMENT (a bean bent like a saddle): blue with bubble spots where it is teal, pale where it is cream.\n"
    "4. BACK OF THE HEAD (a round ball): cobalt blue; pale where it is cream; no pattern.\n"
    "Bottom row, from left to right:\n"
    "5. LONG BACK BODY (a long S-shaped tube): blue with bubble spots; the cream strip along its lower edge becomes pale ice "
    "blue.\n"
    "6. TAIL TIP (a tapering leaf-shaped piece): blue; its thin cream edge becomes pale ice blue.\n"
    "7. TAIL TUFT (the cream flame-shaped tuft with a swirl): REPLACE it by the BLACK TAIL HORN of image 1: a hard horn of "
    "charcoal black (#26252C), a slender, slightly curved leaf / spearhead shape with a needle-sharp tip and one thin "
    "dark-grey line (#5B5B68) along its centre, one small back-pointing barb on each side near its base. Its BASE (the end "
    "that joins the tail) sits exactly where the swirl at the lower left of the old tuft is; its TIP points to where the tip "
    "of the old tuft is (top, upper right). Its base end is simply rounded off, with an ink outline all around the horn. It "
    "is as tall as the old tuft and stays inside the bounding box of the old tuft (it may be narrower). No swirl, no fluff, "
    "no blue fur, no shine.")

RESKIN_B = (
    "THE PARTS OF THIS SHEET (image 2):\n"
    "Top row, from left to right:\n"
    "1. FACE MASK (the front of the head, with two EYE HOLES): cobalt blue where it is teal, with no pattern and no "
    "blotches; pale ice blue where it is cream (the cheek at the lower left, the lip band along the bottom). Keep the two "
    "EYE HOLES exactly where they are, with their ink rings, and leave them EMPTY: pure white paper inside (they are "
    "cut-outs). Keep the outline of the mouth notch at the bottom. Add two tiny ink nostril slits just above the notch.\n"
    "2. EYE BACKING (the pale plate with two white eyeballs, no outline): it lies behind the face mask. Paint the plate "
    "cobalt blue and the two eyeballs flat amber orange (#FFA92E), plain: no pupil, no shading, no grey crescent (the pupils "
    "are separate parts below). Still no outline around the plate, same shape.\n"
    "3. INSIDE OF THE MOUTH (the pink ball with a cream strip at the bottom): dark raspberry (#8E2F4F) with a rounded "
    "lighter-pink tongue (#EC8098) in its lower half; the strip at the bottom (the lower jaw) becomes pale ice blue; ink "
    "outline all around.\n"
    "4 and 5. TWO EAR TUFTS (cream flame-shaped tufts with a swirl): REPLACE each by a BLACK HEAD HORN of image 1 (part 4 = "
    "the bigger horn on the left of the head in image 1, part 5 = the smaller horn on the right): a smooth, solid, curved "
    "crescent horn of charcoal black (#26252C) with a sharp tip and two short thin dark-grey ridge lines (#5B5B68) near its "
    "base, ink outline all around, base end simply rounded off. Its BASE sits exactly where the swirl at the bottom of the "
    "old tuft is, its TIP where the tip of the old tuft is (at the top); it is as tall as the old tuft and stays inside the "
    "bounding box of the old tuft. No swirl, no fluff, no blue fur, no shine.\n"
    "Second row, from left to right:\n"
    "6 and 7. TWO UPPER EYELIDS (teal half-moon shapes): cobalt blue, same shape, ink outline.\n"
    "8 and 9. TWO PUPIL DISCS (pink ovals): they slide over the amber eyeballs. Each becomes a flat amber orange (#FFA92E) "
    "oval of the same size and place, WITHOUT any outline (drop the black ring), with a tall, thin black vertical slit pupil "
    "in its middle and ONE small white catchlight dot at the upper left of the slit.\n"
    "10 and 11. TWO SQUINT MARKS (the black > and < strokes): keep them as they are, in dark-brown ink.")

RESKIN_RULES = (
    "LAYOUT: canvas 1536 x 1024, pure-white background (#FFFFFF), every part where image 2 has it, white space between the "
    "parts as in image 2. No labels, no numbers, no arrows, no frames, no shadows, no extra marks.")


# Dạng 2 (concept duyệt 2026-11-11): lưng chàm đậm, sừng đầu to có nhánh phụ, lưỡi đuôi to có ngạnh, thêm nanh và gai lưng. Hai mảnh
# thêm (nanh, gai) là hình giữ chỗ xám do `ran_sung.py to 2` vẽ vào tờ B; rig đặt 2 nanh và 5 gai từ hai mảnh đó.
NAVY = "deep navy indigo (#22388F)"
THEM_B2 = (
    "\nTwo EXTRA parts at the right of the second row (light-grey placeholder shapes in image 2; repaint them the same way, "
    "keeping silhouette, place and size):\n"
    "12. FANG (the small grey tooth pointing down): one curved snake fang, cream (#FBF1D2), ink outline all around, needle "
    "tip at the bottom.\n"
    "13. BACK SPIKE (the grey shark-fin shape pointing up): one pointed back plate of the spine, bright cobalt blue "
    "(#2E6FD8), flat, ink outline along its two slanted sides only; leave its bottom edge (the base) WITHOUT outline.")


def reskin_text(k):
    """(RESKIN_COLOUR, RESKIN_A, RESKIN_B) của dạng k."""
    if k == 1:
        return RESKIN_COLOUR, RESKIN_A, RESKIN_B
    col = RESKIN_COLOUR.replace("becomes cobalt blue (#2E6FD8)", "becomes " + NAVY + ", clearly darker than a medium blue")
    a = RESKIN_A.replace("cobalt blue", NAVY)
    a = a.replace(
        "a slender, slightly curved leaf / spearhead shape with a needle-sharp tip and one thin dark-grey line (#5B5B68) "
        "along its centre, one small back-pointing barb on each side near its base.",
        "the big tail blade of image 1: a long, slightly curved leaf / spearhead blade with a needle-sharp tip and one thin "
        "dark-grey line (#5B5B68) along its centre, and TWO curved back-pointing prongs on each side near its base.")
    a = a.replace("(it may be narrower)", "(it may be up to one fifth taller and wider than that box: this form's blade is bigger)")
    b = RESKIN_B.replace("cobalt blue", NAVY)
    b = b.replace(
        "a smooth, solid, curved crescent horn of charcoal black (#26252C) with a sharp tip",
        "a bigger, solid, curved crescent horn of charcoal black (#26252C) with a sharp tip and ONE small extra prong on its "
        "outer side as in image 1")
    b = b.replace("stays inside the bounding box of the old tuft. No swirl",
                  "may be up to one quarter taller and wider than the old tuft (this form's horns are bigger). No swirl")
    assert a != RESKIN_A and b != RESKIN_B and col != RESKIN_COLOUR
    assert "TWO curved back-pointing prongs" in a and "ONE small extra prong" in b and "one quarter taller" in b
    return col, a, b + THEM_B2


def build_reskin(k):
    """Lượt 2 dạng k: hai tờ reskin (A thân, B đầu). Cần `ran_sung.py to k` dựng tờ mảnh gốc trước."""
    ra = []
    r_col, r_a, r_b = reskin_text(k)
    them = "" if k == 1 else "; thêm hai hình giữ chỗ xám: một chiếc nanh, một chiếc gai lưng"
    for ten, buoc, parts, vi in (("A", "R01", r_a, "bảy mảnh thân: cổ trên, ngực, khúc vòng cuộn, gáy, thân sau dài, chóp đuôi, chùm đuôi"),
                                 ("B", "R02", r_b, "mười một mảnh đầu: mặt nạ có lỗ mắt, nền mắt, khối miệng, hai chùm tai, hai mí, hai mống mắt, hai dấu mắt nheo" + them)):
        goc = os.path.join(HERE, "inbox", f"{CODE}_{k}", "mau", f"goc_{ten}.png")
        refs = [(chosen(k), f"OUR snake (form {k}, approved), 1536x1024, white background: the colours, the wobbly dark-brown "
                            "ink line, the crayon hatching, the bubble spots, the amber slit eyes and the black horns that "
                            "the repainted parts must have. Do not redraw the whole snake.",
                 f"Rắn sừng dạng {k} đã chốt (1536 × 1024, nền trắng): lấy màu, nét, vân sáp, đốm bong bóng, mắt hổ phách, sừng đen"),
                (goc, "the ORIGINAL PARTS SHEET, 1536x1024, white background: separate parts of a cartoon snake (teal back, "
                      "pinkish-cream belly) laid apart on a white page. Keep every part's silhouette, place and size; "
                      "repaint it.",
                 f"Tờ mảnh của rig gốc phóng 3 lần (1536 × 1024, nền trắng): {vi}; màu gốc lục lam và kem")]
        check(refs)
        out = os.path.join(save_dir(k), buoc + ".png")
        p_ = os.path.join(pk(k), f"luot_2_reskin_{ten}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
        t += ["", f"SAVE: save it as a PNG to {W(out)}",
              f"If a file with that name already exists, save as {buoc}_2.png, {buoc}_3.png ... in the same folder. Do not "
              "edit, move or delete any other file.", "", RESKIN_TASK, "", r_col, "", parts, "", RESKIN_RULES]
        open(p_, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        ra.append((p_, out, refs, vi))
    gd = [f"# Gói gửi GPT: dòng `{CODE}` dạng {k}, lượt 2: RESKIN rig gốc", "",
          "Người dùng chốt 2026-11-11: giữ nguyên rig Spine của con gốc (`monster_3247`: xương, lưới, trọng số, animation), chỉ **vẽ lại "
          "da từng mảnh**. GPT vẽ đè lên tờ mảnh gốc, **giữ hình bóng, chỗ, cỡ từng mảnh**; riêng chùm tai và chùm đuôi đổi thành sừng "
          "đen (gốc sừng đúng chỗ gốc chùm lông). Tờ mảnh gốc dựng bằng `py -3 -I ArtGen/Spine/ran_sung.py to "
          f"{k}`; ảnh về cắt bằng `py -3 -I ArtGen/Spine/ran_sung.py nhan {k}`.", "",
          "Ảnh mảnh gốc là của hãng làm game tham khảo: chỉ dùng làm mẫu trong máy, **không đăng công khai**.", ""]
    for p_, out, refs, vi in ra:
        gd += [f"## {os.path.basename(p_)}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{W(p_)}` → lưu `{W(out)}` (trùng tên thì `_2`, `_3`…).",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/{os.path.basename(p_)}`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{W(r)}` | {v} |" for i, (r, _, v) in enumerate(refs, 1)]
        gd += [""]
    gd += ["## Kiểm", "",
           "- Mỗi mảnh **đúng chỗ, đúng cỡ, đúng hình bóng** của mảnh gốc (đặt đè lên tờ gốc thì viền trùng trong vài pixel).",
           ("- Lưng lam cô-ban có đốm bong bóng, bụng lam băng; hết hoa văn chữ triện và mảng sẫm của con gốc." if k == 1 else
            "- Lưng CHÀM ĐẬM (sẫm hơn hẳn dạng 1) có đốm bong bóng, bụng lam băng; sừng đầu có nhánh phụ, lưỡi đuôi có ngạnh; "
            "mảnh nanh màu kem và mảnh gai lam cô-ban đúng chỗ hai hình giữ chỗ xám."),
           "- Mép mềm của mảnh gốc (đầu dưới các khúc thân) vẫn là nét lam nhạt, không thành viền mực.",
           "- Mặt nạ: **hai lỗ mắt để trắng**; nền mắt lam có hai tròng vàng; mống mắt vàng có con ngươi dọc; mí lam.",
           "- Chùm tai và chùm đuôi đã thành **sừng đen**, gốc đúng chỗ gốc chùm lông, nằm trong vùng của chùm lông cũ.",
           "- Tô phẳng, không bóng, nền trắng tinh, không nhãn chữ.", "",
           "## GPT vẽ sai thì gửi thêm (`--note`)", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Mảnh bị dời, đổi cỡ, đổi dáng | `Every part must keep the exact silhouette, place and size it has in image 2; only "
           "colours, surface and style change.` |",
           "| Tô kín lỗ mắt | `The two eye holes of the face mask stay empty: pure white inside their ink rings.` |",
           "| Vẫn còn hoa văn chữ triện, mảng sẫm | `Remove the angular key pattern and the dark blotches; plain cobalt blue with a "
           "few round light-aqua bubble spots.` |",
           "| Sừng to quá vùng chùm lông, hoặc vẫn có xoáy | `Each horn stays inside the area of the old tuft, base where the "
           "swirl was, tip where the tuft's tip was; no swirl, no fluff.` |"]
    open(os.path.join(pk(k), "HUONG_DAN_luot_2.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return [q[0] for q in ra]


if __name__ == "__main__":
    for kk in (1, 2):
        if os.path.exists(chosen(kk)) and os.path.exists(os.path.join(HERE, "inbox", f"{CODE}_{kk}", "mau", "goc_A.png")):
            print(f"lượt 2 dạng {kk} (reskin):", *build_reskin(kk))
    if os.path.exists(DRAFT2) and os.path.exists(chosen(1)):
        print("lượt sửa dạng 2:", build_fix2())
    if os.path.exists(DRAFT) and os.path.exists(GUIDE):
        print("lượt sửa dạng 1:", build_fix())
    print("dạng 1:", build_form(1))
    # Dạng 2 theo bản đã duyệt của dạng 1. Người dùng muốn xem thử cả hai dạng trước khi duyệt (2026-11-11): gọi thêm tham số
    # "thu2" thì dựng dạng 2 theo bản nháp mới nhất của dạng 1 (L1_sua.png).
    if os.path.exists(chosen(1)) or ("thu2" in sys.argv and os.path.exists(ref1())):
        print("dạng 2 (theo", os.path.basename(ref1()) + "):", build_form(2))
    else:
        print("dạng 2: chưa dựng (chưa có", W(chosen(1)) + ")")
