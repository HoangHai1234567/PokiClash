"""Gói GPT vẽ concept dòng tm01 của lô 10 tướng mới đảo Thủy (2026-11-11, đặc tả ArtGen/Spine/quai/DAC_TA_LO_THUY.md).

Dòng: sinh vật giọt nước, thay suất ải 1 đảo Thủy, TƯỚNG KHỞI ĐẦU hệ Thủy. Chủ đề lấy từ một con giọt nước của game tham khảo
(chỉ giữ ý "giọt nước sống"); thiết kế, màu, chi tiết, diễn xuất là của mình. Không đính ảnh con gốc vào prompt.

  dạng 1  Tí Tách   giọt mưa con chibi, mào sóng cuộn, băng đô đỏ, nắm đấm nhỏ
  dạng 2  Sóng Thần võ sĩ thủy triều trưởng thành, thú rồng kỳ giông đứng thế tấn: chàm đậm, bờm mào sóng, găng nước,
          giáp vỏ ốc, khăn đỏ dài, đai ngọc giọt nước, đuôi mào sóng

Lượt 1 mỗi dạng: concept trọn con một ảnh (chỉ làm mốc cho pha 2; pha 2 vẽ tờ mảnh rời theo cách Hải Long).
Dạng 2 chỉ dựng khi đã chọn concept dạng 1 (chép bản chọn thành inbox/tm01_1/tai_ve/L1_duyet.png).

    py -3 -I ArtGen/Spine/build_tm01.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm01_1/luot_1_concept.txt [--note "..."]
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm01_2/luot_1_concept.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm01"
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
FX_ART = os.path.normpath(os.path.join(HERE, "..", "..", "Assets", "03 Art", "Fx"))
SPLASH = os.path.join(FX_ART, "no_nuoc.png")
PENGUIN = os.path.join(HERE, "inbox", "canh_cut_1", "tai_ve", "L1_lien.png")   # chibi hai chân đã duyệt (Thủy)
SHARK = os.path.join(HERE, "inbox", "vay_lam_1", "tai_ve", "L1_lien.png")      # nét, mặt quả quyết (Thủy)
SHARK3 = os.path.join(HERE, "inbox", "vay_lam_3", "tai_ve", "L1_lien.png")     # dạng cuối dữ, đậm (Thủy)
GUARD = os.path.join(HERE, "inbox", "lam_quan_2", "tai_ve", "L1_lien.png")     # dạng sau có đồ, giáp (Thủy)


def W(p):
    return os.path.normpath(p)


def pk(k):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def chosen(k):
    """Concept Claude đã chọn của dạng k (chép từ L1_concept*.png)."""
    return os.path.join(save_dir(k), "L1_duyet.png")


# ---------------------------------------------------------------- thiết kế (tiếng Anh, dán vào prompt)
PALETTE1 = ("COLOURS (use exactly these, each area one flat colour): body bright aqua (#35BFE6); wave stripes on the back deep "
            "ocean blue (#1F5DB5); belly patch and foam trims pale foam aqua (#D6F2FA, never left as white paper); headband "
            "and its ribbon tails tomato red (#E2483A) with a thin darker red (#A8302A) knot; eye whites light cream (#FBF6EA); "
            "irises deep navy (#1C3A7A) with a black pupil; brows deep ocean blue (#1F5DB5); inside of the mouth deep rose "
            "(#B8405A); the fang cream (#FBF6EA).")

FORM1 = ("CREATURE: a small LIVING RAINDROP of the water element, the STARTER creature of a monster-collecting game: instantly "
         "recognisable, iconic, appealing, simple readable shapes and few details. A creature, not a human and not a slime "
         "puddle: no human face, no clothes except the headband.\n"
         "FORM 1, the first and smallest form, chibi:\n"
         "- BODY AND HEAD are ONE plump water-drop shape, wide and round at the bottom, narrowing upward. The top is NOT a "
         "straight point: it rises into a tip that CURLS OVER to the viewer's RIGHT like a small breaking wave crest, with "
         "a scalloped pale-foam trim along the curl. The curl stays high above the eyes.\n"
         "- On the upper back (left side of the drop) two or three short wavy deep-blue stripes, like little wave lines.\n"
         "- On the front of the body a pale-foam BELLY PATCH shaped like an upside-down water drop.\n"
         "- FACE on the right half of the drop: two big round eyes (cream whites, deep navy irises, one small catchlight dot "
         "each), short thick brows slanting down toward the middle, a small mouth slightly OPEN as if shouting a battle cry, "
         "showing the deep-rose inside and ONE small fang at the upper lip. DETERMINED, brave, ready to fight; never a "
         "happy mascot grin, never scary.\n"
         "- HEADBAND: a red cloth band tied around the head just above the eyes, the knot at the back of the head (viewer's "
         "left) with TWO short ribbon tails fluttering back to the left, clear of the body, not crossing each other.\n"
         "- ARMS: two short stubby aqua arms ending in small round clenched fists (no fingers drawn), sticking out from the "
         "sides of the drop.\n"
         "- FEET: two short stubby round aqua feet with flat soles.\n"
         "- TAIL: a small water-splash tail at the lower back on the viewer's left: a short tapering aqua curl with a "
         "pale-foam tip that curls upward.")

POSE1 = ("POSE (very important: the picture will be cut into separate parts and animated with a 2D skeleton, so parts must "
         "be readable and must not overlap):\n"
         "- Three-quarter side view turned toward the viewer's RIGHT; the face is on the right, the eyes look to the "
         "viewer's right.\n"
         "- Stands on its two stubby feet, both soles flat on one level ground line (no ground drawn), a little boxer's "
         "stance: body leaning slightly forward, feet a little apart with white space between them.\n"
         "- The near arm (on the right) is raised forward and up with its fist at about eye height in front of the body; "
         "the far arm (on the left) is raised a little behind, its fist peeking out from behind the back. Each arm is "
         "clear of the body outline with a thin white gap where possible; the arms never cross the face.\n"
         "- The tail sticks out behind on the lower left, the two headband ribbons fly out behind on the upper left; tail, "
         "ribbons, arms and the crest curl do not touch each other.")

FRAME1 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. The whole "
          "creature is visible, nothing cut by the edges, at least 60 px of white margin all round. It is centred, about "
          "620 px tall from the top of the crest curl to the soles of its feet; its feet are about 140 px above the bottom "
          "edge.")

PALETTE2 = ("COLOURS (use exactly these, each area one flat colour; the main colour is now much deeper than form 1): body "
            "deep indigo blue (#2C3E9E); wave stripes, fin edges and the big crest bright aqua (#35BFE6); chest, belly and "
            "the foam trims pale foam aqua (#D6F2FA, never left as white paper); the water gauntlets bright aqua with pale "
            "foam rims; sash, headband and ribbon tails tomato red (#E2483A) with darker red (#A8302A) knots; shell armour "
            "warm sand cream (#F1DDB0) with tomato-red stripes; the chest gem bright aqua; eye whites light cream "
            "(#FBF6EA), irises deep navy (#1C3A7A); claws and fangs cream (#FBF6EA); inside of the mouth deep rose "
            "(#B8405A).")

FORM2 = ("CREATURE: the FINAL FORM of the living-raindrop creature of image 3 (form 1, approved), the starter creature of a "
         "monster-collecting game, now grown up into a fierce TIDE WARRIOR. A creature, not a human: creature head, "
         "creature body, no clothes except the items listed.\n"
         "FORM 2, adult proportions, NOT chibi: the head is about 28 percent of its height. NOT a human bodybuilder: no "
         "human chest muscles, no abs, no human shoulders or human hands. It has the build of a big upright WATER-DRAGON "
         "NEWT BEAST: a thick rounded creature torso and belly, slightly hunched forward, digitigrade creature legs with big "
         "clawed feet, a longer creature muzzle. It must look clearly different from form 1 (new silhouette, deeper "
         "colour, armour) while keeping the family traits listed below.\n"
         "- HEAD: a creature head with a longer strong muzzle, a firm lower jaw, big sharp narrowed eyes (cream whites, "
         "deep navy irises, one small catchlight dot each) under a hard brow ridge, two small fangs; the mouth slightly OPEN "
         "in a battle snarl showing the deep-rose inside. Fierce and confident, not scary.\n"
         "- CREST (family trait, grown from form 1's curl): from the top of the head a big swept-back MANE OF THREE WAVE "
         "CRESTS, bright aqua, each curling over at its tip with a scalloped pale-foam trim, flowing back to the viewer's "
         "left, layered but not crossing each other.\n"
         "- HEADBAND (family trait): the red headband is now a long red sash tied around the brow, its knot at the back, "
         "with TWO LONG ribbon tails streaming back to the left behind the crest.\n"
         "- BODY: deep indigo; a pale-foam chest and belly; bright aqua wavy stripes on the shoulders, upper arms and "
         "thighs. A red cloth belt with a small bright aqua gem shaped like a WATER DROP on its buckle (family trait: the "
         "drop).\n"
         "- ARMS: strong arms; on the outside of each forearm a short aqua fin with a pointed tip pointing back toward the "
         "elbow; each forearm wrapped in a WATER GAUNTLET: a thick swirl of bright aqua water with a foam rim, a solid "
         "flat shape with a closed ink outline; big clenched fists with short cream claws on the knuckles.\n"
         "- ARMOUR: one big spiral CONCH-SHELL PAULDRON on the near (right-side) shoulder and shell plates on the shins, "
         "sand cream with red stripes, simple shapes.\n"
         "- LEGS AND FEET: strong legs, big three-toed feet with short cream claws.\n"
         "- TAIL: a long thick tail behind on the viewer's left, ending in a curling wave-crest tip with a foam trim.")

POSE2 = ("POSE (very important: the picture will be cut into separate parts and animated with a 2D skeleton, so parts must "
         "be readable and must not overlap):\n"
         "- The WHOLE body (not only the head) in a true three-quarter side view turned toward the viewer's RIGHT, not "
         "facing the viewer; the head is at the upper right, the eyes look to the viewer's right.\n"
         "- Stands on its two feet in a wide, grounded FIGHTING STANCE, both soles flat on one level ground line (no ground "
         "drawn): the near leg forward on the right, the far leg back on the left, a clear white gap between the legs.\n"
         "- The near gauntleted fist is thrust forward on the right at chest height, out in front of the body; the far arm "
         "is pulled back on the left behind the body, its fist low. Arms do not cross the face or the chest; each arm has "
         "white space around it where possible.\n"
         "- The tail sweeps out behind on the lower left, clear of the legs; the crest mane and the two long ribbon tails "
         "flow back on the upper left; tail, ribbons, crest and arms do not cross each other.")

FRAME2 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. The whole "
          "creature is visible, nothing cut by the edges, at least 60 px of white margin all round. It is centred, about "
          "800 px tall from the top of its crest to the soles of its feet; its feet are about 90 px above the bottom edge.")

WATER = ("WATER PARTS (crest curls, foam trims, tail tip, gauntlets) look like the game's water in the water-splash image: "
         "plump rounded shapes, round bumpy foam scallops, flat blues, the same brown ink outline. They are SOLID parts of "
         "the creature with closed outlines: no loose drops, bubbles, splashes or spray floating around it.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images: drawn by hand on paper with a dark-brown "
        "ink pen (#2B2118), an outline about 7 px thick on this canvas, the same weight on every edge, slightly wobbly like "
        "a real pen; every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal "
        "hatching (strokes thinner than the outline), kept inside the outline. Clean and appealing, neither a crude "
        "scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, no shadow under the "
        "figure, on the ground or on the background), no white highlights or shine spots, no gloss, no glassy or "
        "transparent jelly look, no glow, no rim light, no gradients, no 3D look. The only white allowed is one small "
        "catchlight dot in each eye. A darker tone appears only where the design itself has a darker colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no frame, no props, no effects around "
      "the creature.")


def refs_of(k):
    if k == 1:
        return [
            (PENGUIN, "another approved hero of the same game (a chibi penguin cook on two legs), 1536x1024, white "
                      "background: copy its framing, its chibi two-legged pose logic (three-quarter view facing right, arms "
                      "apart from the body), its hand-drawn pen line and its flat crayon colouring. Do NOT copy its "
                      "species, design, colours, crest, beak or props.",
             "Cánh Cụt dạng 1 đã duyệt (1536 × 1024, nền trắng): chim cánh cụt chibi hai chân cầm chảo. Lấy khung, dáng chibi "
             "hai chân, nét bút, tô sáp; không chép loài, màu"),
            (SHARK, "another approved hero of the same game (a blue shark beast), 1536x1024, white background: match EXACTLY "
                    "its pen line, crayon texture, flat colouring, simple readable shapes and determined expression. Do NOT "
                    "copy its species, design or colours.",
             "Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): cá mập xanh lam bốn chân, mặt quả quyết. Lấy nét, độ chi "
             "tiết, nét mặt"),
            (SPLASH, "the game's approved water splash, 512x505, transparent background: the look of the game's water "
                     "(plump pointed water shapes, round foam bumps, flat blues, brown ink outline) for the crest curl, the "
                     "foam trims and the tail tip only.",
             "Vụ nước toé đã duyệt (512 × 505, nền trong): mũi nước mập, bọt tròn, lam phẳng. Lấy dáng nước cho mào, đuôi"),
            (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline "
                          "+ coloured pencil / wax crayon hatching), nothing of its content.",
             "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp"),
        ]
    return [
        (SHARK3, "another approved hero of the same game (the final form of a shark line), 1536x1024, white background: "
                 "match its pen line, crayon texture and flat colouring, and the level of fierceness of a final form "
                 "(sharp eyes, strong build, ready to fight). Do NOT copy its species, design, colours or pose.",
         "Vây Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): cá mập xanh đậm dạng cuối, dữ. Lấy nét, độ dữ của dạng cuối"),
        (GUARD, "another approved hero of the same game (a later form that wears armour and accessories), 1536x1024, white "
                "background: see how armour pieces and cloth are drawn simply in this style. Do NOT copy its species, "
                "design or colours.",
         "Lam Quân dạng 2 đã duyệt (1536 × 1024, nền trắng): kỳ lân lam mang chuông, giáp. Lấy cách vẽ giáp, vải đơn giản"),
        (chosen(1), "FORM 1 of THIS creature (approved), 1536x1024, white background: keep its colour family (aqua, deep "
                    "blue, pale foam, tomato-red headband), its wave-crest curl, its drop-shaped belly patch, its eyes and "
                    "its drawing style, so the line clearly grows up. Do NOT copy its chibi proportions, its round drop "
                    "body or its pose: form 2 is a tall adult warrior.",
         "Tí Tách dạng 1 đã chọn (1536 × 1024, nền trắng): giữ họ màu, mào sóng, băng đô đỏ, mắt; không chép tỉ lệ chibi"),
        (SPLASH, "the game's approved water splash, 512x505, transparent background: the look of the game's water (plump "
                 "pointed water shapes, round foam bumps, flat blues, brown ink outline) for the crest, the gauntlets, the "
                 "foam trims and the tail tip only.",
         "Vụ nước toé đã duyệt (512 × 505, nền trong): dáng nước cho bờm sóng, găng nước, chóp đuôi"),
        (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + "
                      "coloured pencil / wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp"),
    ]


FORMS = {1: ("Tí Tách", PALETTE1, FORM1, POSE1, FRAME1), 2: ("Sóng Thần", PALETTE2, FORM2, POSE2, FRAME2)}

CHECK = {
    1: ["Giọt nước mập đáy tròn, chóp **cuộn sang phải như mào sóng** có viền bọt, không phải chóp nhọn thẳng.",
        "Có tay ngắn nắm đấm, hai bàn chân ngắn, đuôi giọt toé nhỏ; **băng đô đỏ**, nút sau đầu, hai dải bay sang trái.",
        "Mảng bụng nhạt hình giọt nước ngược, vài sọc sóng lam đậm trên lưng.",
        "Mắt to tròng kem, tròng đen xanh chàm, mày xếch, miệng hé thấy lòng miệng và một răng nanh nhỏ: quả quyết, không cười.",
        "Nhìn sang **phải**, tay chân tách thân, không chéo nhau; không giọt nước, bong bóng bay quanh.",
        "Tô phẳng: **không** bóng, không điểm sáng (trừ chấm trong mắt), không kiểu thạch trong suốt bóng loáng; nền trắng tinh."],
    2: ["Thú rồng kỳ giông nước đứng hai chân thế tấn, đầu khoảng 28% chiều cao, **không chibi**, **không thân người lực "
        "sĩ** (không cơ ngực, cơ bụng, vai người); cả thân nghiêng 3/4 sang phải; bóng dáng khác hẳn dạng 1.",
        "Màu chủ đạo **chàm đậm**, sọc và bờm lam sáng, ngực bụng bọt nhạt.",
        "Bờm ba mào sóng cuộn ra sau, khăn đỏ hai dải dài, găng nước trên cẳng tay, giáp vỏ ốc ở vai gần và ống chân, "
        "đai đỏ có ngọc hình giọt nước.",
        "Mắt sắc, nanh, miệng hé gầm thấy lòng miệng; dữ, chiến, không đáng sợ.",
        "Nhìn sang **phải**, tay chân tách thân, không chéo; đuôi dài có chóp mào sóng bên trái.",
        "Tô phẳng: không bóng, không điểm sáng (trừ chấm mắt), không quầng; nền trắng tinh."],
}

FIX = [("Có bóng, mảng sáng tối, điểm sáng", "Flat colour only: remove every shadow, highlight, shine spot and gradient; keep "
                                            "the crayon hatching as texture only."),
       ("Thành thạch trong suốt bóng loáng", "The body is an opaque flat aqua colour with crayon texture, not glassy jelly: "
                                            "no reflections, no transparency, no shine."),
       ("Quay sang trái", "Mirror the creature so it faces the viewer's RIGHT."),
       ("Tay dính thân, chéo nhau", "Keep both arms apart from the body with a thin white gap; nothing crosses the face."),
       ("Có giọt, bong bóng bay quanh", "Remove every loose drop, bubble and splash around the creature; only the creature "
                                        "on pure white."),
       ("Dạng 2 vẫn chibi", "Not chibi at all: adult proportions, the head about one quarter of the total height, tall "
                            "lean warrior body."),
       ("Dạng 2 thành người lực sĩ, nhìn thẳng", "Much less human: no human chest muscles, abs, shoulders or hands; the build "
                                                "of an upright water-dragon newt beast; turn the whole body to a true "
                                                "three-quarter side view facing the viewer's right.")]


def check(refs):
    missing = [W(p) for p, _, _ in refs if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def build_form(k):
    name, palette, form, pose, frame = FORMS[k]
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
          "TASK: design and draw ONE creature hero as ONE full-body picture, in a clean animation-ready pose, in the "
          "hand-drawn style of the approved hero images.", "",
          form, "", palette, "", WATER, "", frame, "", pose, "", LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: dòng `{CODE}` dạng {k} ({name})", "",
          "Lô 10 tướng mới đảo Thủy, dòng 1 (thay suất ải 1, tướng khởi đầu hệ Thủy). Đặc tả: "
          "`ArtGen/Spine/quai/DAC_TA_LO_THUY.md`; ghi chú thiết kế: `ArtGen/Spine/inbox/tm01_ghichu.md`.", "",
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


# ---------------------------------------------------------------- lượt 2: tờ mảnh rời (pha 2, sau khi concept được duyệt)
PIECES = ("THIS IS A SHEET OF SEPARATE PARTS for a 2D cut-out animation rig, NOT a scene: every part is drawn COMPLETE and on "
          "its own (also the areas that are hidden in the concept), flat on the white page like stickers laid out on a table, "
          "with at least 60 px of pure white between any two parts and between a part and the image edge. No part touches or "
          "overlaps another. Every part keeps exactly the colours, markings, outline weight and crayon texture of the "
          "approved concept. Do not draw a whole creature, do not draw extra parts, do not draw labels, numbers, arrows or "
          "guide lines.")
SHEET_REF = os.path.join(HERE, "inbox", "hai_long", "tai_ve", "M01.png")

# (bước, tiêu đề, mô tả tiếng Anh, ghi chú tiếng Việt). Cỡ ghi theo cỡ trong concept (1536 x 1024) để mảnh cùng tỉ lệ.
STEPS2 = [
    ("M01", "head and soft parts",
     "Canvas 1536 x 1024. Lay the parts out in a 3 x 2 grid of 512 px cells, one group centred in each cell:\n"
     "- top-left cell: the HEAD, UPPER PART ONLY, side view facing the viewer's RIGHT, exactly like the head in the concept: "
     "the skull with its rounded top drawn complete (the crest mane is NOT on it), the big fierce open eye with its cream "
     "white, navy iris and one catchlight dot, the thick blue brow, the upper muzzle with the nostril and the two cream upper "
     "fangs hanging along the bottom edge of the upper lip, the aqua cheek fin at the back of the head, and the red headband "
     "around the brow with its round red knot at the back of the head. NO lower jaw, NO crest mane, NO ribbon tails, NO neck. "
     "The back-bottom of the head (where the neck joins) is a smooth rounded stump. About 300 px wide, 190 px tall.\n"
     "- top-middle cell: the LOWER JAW alone, side view facing right: a long wedge, indigo on the outside with a pale-foam "
     "underside, two small cream lower fangs standing on its top edge near the front, a strip of the deep-rose inner mouth "
     "and the rose tongue lying inside it visible above the gum line; the back end (the jaw hinge) is a rounded knob. About "
     "190 px wide, 70 px tall.\n"
     "- top-right cell, two separate small parts with white between them: (a) a MOUTH INTERIOR patch: one soft rounded blob "
     "of flat deep rose (#B8405A) with a darker rose throat spot (#8E2F48), brown ink outline, about 170 px wide, 110 px tall, "
     "no teeth; (b) below it, a CLOSED EYELID patch: an indigo (#2C3E9E) almond shape a little bigger than the open eye of "
     "the head (about 90 px wide, 70 px tall), with ONE curved dark-brown lash line across its lower half (a calm closed eye), "
     "nothing else.\n"
     "- bottom-left cell: TWO separate WAVE CRESTS of the mane, one above the other: (a) a BIG crest about 320 px wide and "
     "160 px tall; (b) a SMALLER crest about 250 px wide and 130 px tall. Each one: bright aqua water with a pale-foam "
     "scalloped trim, a blunt rounded BASE at its bottom-left (where it plugs into the head), rising and curling over to the "
     "RIGHT into a plump hook, like the crests of the concept.\n"
     "- bottom-middle cell: the TWO RED RIBBON TAILS of the headband, one above the other, each drawn lying STRAIGHT and "
     "horizontal like a strip of cloth, with gently wavy long edges: (a) about 300 px long, 44 px wide; (b) about 250 px long, "
     "40 px wide. The RIGHT end of each is cut square (it goes into the knot), the LEFT end is cut into a V notch.\n"
     "- bottom-right cell: the TAIL alone, drawn STRAIGHT and horizontal: a thick rounded stump on the LEFT (about 110 px "
     "thick, where it joins the hip), indigo with the aqua wavy stripes and a pale-foam underside, tapering toward the RIGHT, "
     "and at the right end the WAVE-CREST TAIL TIP: the tail ends in a plump aqua wave hook with a pale-foam scalloped trim "
     "that curls UPWARD and back over the tail. About 470 px long overall, the tip about 170 px tall.",
     "đầu phần trên (sọ đủ, mắt mở, mày, mõm trên có nanh, vây má, băng đô có nút; không hàm, không bờm, không dải) · hàm dưới có "
     "lòng miệng và nanh · mảng lòng miệng + mí mắt nhắm · hai mào sóng của bờm (to, nhỏ) · hai dải khăn duỗi thẳng · đuôi duỗi "
     "thẳng có chóp mào sóng"),
    ("M02", "body and limbs",
     "Canvas 1536 x 1024. Lay the parts out in a 4 x 2 grid of 384 x 512 px cells, one part centred in each cell:\n"
     "- top row, cell 1: the TORSO alone, three-quarter side view facing right like the concept: a thick rounded creature "
     "trunk, indigo on the back (left side) with the bright aqua wavy stripes, the pale-foam chest and belly on the front "
     "(right side), the red cloth belt around the waist with the round bright aqua WATER-DROP gem buckle on the front-right; "
     "a short rounded neck stump at the top right; the shoulders and hips are smooth rounded areas. NO head, NO arms, NO "
     "legs, NO tail, NO shoulder shell, NO hanging belt flap. About 320 px wide, 350 px tall.\n"
     "- top row, cell 2: ONE ARM drawn STRAIGHT and horizontal from shoulder to wrist: a rounded shoulder end on the LEFT, "
     "the indigo upper arm with one aqua wavy stripe, the elbow, then the forearm wrapped in the bright aqua WATER GAUNTLET "
     "(a thick swirl of aqua water with a pale-foam rim at each end) with a small pointed aqua fin on its top edge pointing "
     "back toward the elbow; the wrist end on the RIGHT is a rounded stump. NO hand. About 320 px long, the upper arm about "
     "70 px thick, the gauntlet about 110 px thick.\n"
     "- top row, cell 3: ONE CLENCHED FIST alone, side view, knuckles to the RIGHT, short cream claws on the knuckles, indigo; "
     "the wrist end on the LEFT is a rounded stump. About 120 px wide, 110 px tall.\n"
     "- top row, cell 4: ONE OPEN HAND alone, pushing forward: palm facing the viewer's right, the four thick fingers "
     "together pointing UP, the thumb in front, short cream claws on the fingertips, indigo; the wrist end at the bottom-left "
     "is a rounded stump. About 120 px wide, 140 px tall.\n"
     "- bottom row, cell 1: ONE LEG drawn STRAIGHT and vertical from hip to ankle: a rounded hip end at the TOP, the thick "
     "indigo thigh with one aqua wavy stripe, the knee, the shin wearing the sand-cream scallop-SHELL shin guard with red "
     "stripes; the ankle end at the BOTTOM is a rounded stump. NO foot. About 115 px thick, 300 px long.\n"
     "- bottom row, cell 2: ONE FOOT alone, side view facing right: a big three-toed creature foot, flat sole along the "
     "bottom, short cream claws on the toe tips, indigo; the ankle end at the top-left is a rounded stump. About 200 px wide, "
     "110 px tall.\n"
     "- bottom row, cell 3: the CONCH-SHELL PAULDRON alone: a spiral conch shell, sand cream with red stripes, like the "
     "shoulder guard of the concept. About 170 px wide, 150 px tall.\n"
     "- bottom row, cell 4: the HANGING BELT FLAP alone: the red cloth flap that hangs from the belt knot, drawn STRAIGHT and "
     "vertical, the TOP end cut square, the BOTTOM end cut into a V notch, gently wavy long edges. About 70 px wide, 200 px "
     "long.",
     "thân (không đầu, tay, chân, đuôi, giáp vai, dải đai) · một cánh tay duỗi thẳng vai → cổ tay có găng nước + vây · nắm đấm · "
     "bàn tay xoè đẩy · một chân duỗi thẳng hông → cổ chân có giáp vỏ sò · bàn chân ba ngón · giáp vai vỏ ốc · dải đai thả"),
]

STEPS1 = [
    ("M01", "body, face parts and limbs",
     "Canvas 1536 x 1024. The LEFT part of the canvas (x from 0 to 600) holds the body; the RIGHT part (x from 600 to 1536) "
     "is a 2 x 2 grid of cells about 468 x 512 px:\n"
     "- left part: the BODY alone, exactly like the concept, three-quarter view facing the viewer's RIGHT: the plump aqua "
     "water-drop body WITH its wave-crest curl on top (the curl and its pale-foam trim are part of this piece), the deep-blue "
     "wave stripes on the upper back, the pale-foam belly patch shaped like an upside-down drop, the red headband painted "
     "around the head with its round knot at the back (NO ribbon tails), the two eyes (the big near eye on the left, the "
     "smaller far eye on the right) with their thick blue brows. The face has NO MOUTH: the place of the mouth is plain "
     "aqua. NO arms, NO feet, NO tail. About 480 px wide including the crest curl and 600 px tall; the bottom of the drop is "
     "round and complete.\n"
     "- right part, top-left cell: FOUR separate MOUTHS for this face, in a 2 x 2 arrangement with white between them, each "
     "drawn alone on white as it would sit on the aqua face: (a) the battle-shout mouth of the concept: slightly open, deep "
     "rose inside, a small rose tongue, one small cream fang hanging from the upper lip, about 80 x 70 px; (b) a WIDE-OPEN "
     "round mouth (a big O as when spitting water), deep rose inside, small tongue, one small fang, about 100 x 100 px; (c) a "
     "CLOSED determined mouth: a short slightly wavy dark-brown line, a little lower at the corners, about 60 x 20 px; (d) a "
     "GRITTED-TEETH mouth: a wide flat mouth showing a row of cream clenched teeth, about 90 x 45 px.\n"
     "- right part, top-right cell: FOUR separate EYE COVERS on aqua (#35BFE6) patches, in a 2 x 2 arrangement: (a) a "
     "CLOSED EYE for the big near eye: an aqua oval a little bigger than that eye (about 120 x 110 px) with one curved "
     "dark-brown closed-eye line across its lower half; (b) the same for the smaller far eye (about 80 x 105 px); (c) a "
     "SQUEEZED-SHUT eye for the near eye: an aqua oval of the same size as (a) with a thick dark-brown '>' mark; (d) the same "
     "for the far eye with a '<' mark, the size of (b).\n"
     "- right part, bottom-left cell, two separate parts: (a) ONE ARM drawn STRAIGHT and horizontal: a rounded shoulder end "
     "on the LEFT (it tucks under the body), the short stubby aqua arm, and at the RIGHT end a small round clenched fist (no "
     "fingers drawn, one curved line for the folded fingers), about 190 px long, 70 px thick, the fist about 90 px; (b) below "
     "it, ONE FOOT: a short stubby round aqua foot seen from the side, toe to the right, flat sole, about 140 px wide, 80 px "
     "tall.\n"
     "- right part, bottom-right cell, three separate parts: (a) the TAIL drawn STRAIGHT and horizontal: a rounded stump on "
     "the LEFT (about 70 px thick, where it joins the body), aqua, tapering to the RIGHT into a little wave-curl splash tip "
     "with a pale-foam scalloped trim curling UPWARD, about 230 px long, the tip about 100 px tall; (b) and (c) the TWO RED "
     "RIBBON TAILS of the headband, each lying STRAIGHT and horizontal with gently wavy long edges, about 200 x 42 px and "
     "170 x 40 px, the RIGHT end cut square (it goes into the knot), the LEFT end cut into a V notch.",
     "thân giọt nước có mào cuộn, sọc, bụng, băng đô có nút, hai mắt + mày, KHÔNG miệng · bốn miệng (hét, há tròn, mím, nghiến răng) · "
     "bốn mảng mắt (nhắm mắt gần, nhắm mắt xa, mắt `>` gần, mắt `<` xa) · tay duỗi thẳng có nắm đấm + bàn chân · đuôi duỗi thẳng "
     "chóp toé + hai dải băng đô"),
]


def refs_sheet(k):
    """ảnh mẫu tờ mảnh: concept đã duyệt của dạng (ảnh 1), tờ mảnh mẫu của dự án, nước, nét."""
    return [(chosen(k), f"the APPROVED CONCEPT of this creature (form {k}), 1536x1024: every part you draw belongs to THIS "
                        "creature: same species, same colours, same markings, same line and crayon texture, same proportions. "
                        "Use it only to know what each part looks like; do not redraw the whole creature",
             f"Concept dạng {k} đã duyệt (1536 × 1024, nền trắng)"),
            (SHEET_REF, "an approved PARTS SHEET of another creature of the same game, 1536x1024: shows how a sheet of separate "
                        "parts is laid out (parts complete, apart on white). Copy only that layout idea, nothing of its "
                        "content, species or colours",
             "Tờ mảnh M01 của Hải Long đã duyệt (1536 × 1024): cách bày mảnh rời trên giấy trắng; không chép nội dung"),
            (SPLASH, "the game's approved water splash, 512x505, transparent background: the look of the game's water for the "
                     "wave crests, foam trims, gauntlets and the tail tip",
             "Vụ nước toé đã duyệt (512 × 505, nền trong)"),
            (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style, nothing of its content",
             "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét")]


def build_sheets(k):
    steps = STEPS1 if k == 1 else STEPS2
    name, palette = FORMS[k][0], FORMS[k][1]
    refs = refs_sheet(k)
    check(refs)
    sd = save_dir(k)
    p = os.path.join(pk(k), "luot_2_manh.txt")
    order = [s[0] for s in steps]
    what = ("the chibi living raindrop of image 1" if k == 1 else "the tide-warrior water-dragon newt of image 1")
    t = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image per step "
         "and save each one as its step says. Do not reply with text only.", "",
         "REFERENCE IMAGES (open each file from its full path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
    t += ["", f"WHAT THIS IS: sheets of separate, complete parts of {what}, for a 2D cut-out animation rig. The animation "
          "software bends the straight limbs, tail and ribbons with bones, opens the mouth and swaps the eye covers, so every "
          "part must be drawn whole (also the areas that are hidden in image 1), clean, at the same scale as image 1, and well "
          "separated from the others.", "",
          f"SAVE: every step's image goes into {W(sd)} under the step's name (for example {order[0]}.png). If that file "
          "already exists, add _2, _3 ... before .png. Do not change, move or delete any other file.", ""]
    if len(order) > 1:
        t += [f"ORDER: draw step {order[0]} now, save it and stop. Each time I say \"next\", draw the next step, save it and "
              f"stop, in this order: {', '.join(order[1:])}.", ""]
    t += [palette, "", WATER, ""]
    for sc, title, en, _ in steps:
        t += [f"=== STEP {sc} ({title}) ===", PIECES, en, "", LINE, FLAT, BG,
              f"SAVE this step: save it as a PNG to {W(os.path.join(sd, sc + '.png'))} (create the folder if it is missing; "
              f"if that file already exists, save it as {sc}_2.png, {sc}_3.png ... in the same folder instead). Do not change, "
              "move or delete any other file.", ""]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gp = os.path.join(pk(k), "HUONG_DAN.md")
    gd = open(gp, encoding="utf-8").read().rstrip("\n").split("\n")
    gd += ["", f"## Lượt 2: tờ mảnh rời (pha 2, sau khi concept {name} được duyệt)", "",
           f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`" + (f", {len(order)} bước {', '.join(order)}, gõ `next` sau mỗi ảnh" if
                                                      len(order) > 1 else "") + f". GPT lưu vào `{W(sd)}`.", "",
           f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_2_manh.txt --steps "
           f"{','.join(order)}`.", "", "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(r)}` | {vi} |" for i, (r, _, vi) in enumerate(refs, 1)]
    gd += ["", "Kiểm: mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ít nhất 60 px, mảnh dài (tay, chân, đuôi, dải) duỗi thẳng, "
           "đúng màu concept, tô phẳng không bóng.", ""]
    gd += [f"- **{sc}**: {vi}" for sc, _, _, vi in steps]
    gd += ["", "| Sai | Gửi thêm |", "|---|---|",
           "| Vẽ cả con thay vì mảnh rời | `This must be a sheet of separate parts laid flat on white, not a creature. Redraw only the parts listed.` |",
           "| Tay, chân, đuôi, dải vẽ cong | `The limbs, the tail and the ribbons must be drawn perfectly straight, like a ruler.` |",
           "| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |"]
    open(gp, "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p


# lượt 3 dạng 2 (Claude điều phối soi 2026-11-11): chân cũ chỉ có ống chân + bọc vỏ sò, thiếu đùi to như concept; vẽ lại chân liền
# cả chi (đùi to, gối, ống, bọc vỏ sò), hai đầu tròn kín (không vẽ miệng ống); kèm đuôi có chóp mào sóng to như concept.
STEP3 = ("M03", "whole leg and tail",
         "Canvas 1536 x 1024, two parts side by side with plenty of white between them:\n"
         "- LEFT half: ONE WHOLE LEG of this creature drawn STRAIGHT and vertical, from the hip at the TOP to the ankle at the "
         "BOTTOM, exactly the leg of the concept but straightened: a BIG, THICK, rounded creature THIGH in the upper half (indigo "
         "with one bright aqua wavy stripe, about 200 px wide at its widest, much thicker than the shin, like the heavy thighs of "
         "the concept), the knee, then the shin wearing the sand-cream scallop-SHELL shin guard with red stripes, and a short "
         "indigo ankle below the guard. The TOP end (hip) is a smooth closed rounded dome and the BOTTOM end (ankle) is a smooth "
         "closed rounded end: do NOT draw them as cut tube openings, no ellipse or cap line at either end. NO foot. About 470 "
         "px tall.\n"
         "- RIGHT half: the TAIL alone, drawn STRAIGHT and horizontal like the concept's tail but straightened: a thick closed "
         "rounded stump on the LEFT (about 130 px thick, where it joins the hip, no tube opening), indigo with bright aqua wavy "
         "stripes and a pale-foam underside, tapering toward the RIGHT, ending in a BIG WAVE-CREST TAIL TIP as large as in the "
         "concept: a plump bright aqua wave hook with a pale-foam scalloped trim curling UPWARD and back over the tail, the tip "
         "about 230 px tall and 230 px wide. About 640 px long overall.",
         "chân liền cả chi (đùi to, gối, ống chân, bọc vỏ sò), hai đầu tròn kín, không bàn chân · đuôi duỗi thẳng có chóp mào sóng to "
         "như concept")


def build_luot3():
    refs = refs_sheet(2) + [(os.path.join(save_dir(2), "M02.png"), "the earlier parts sheet of THIS creature, 1536x1024: match the "
                             "colours, outline and crayon texture of its leg and shell guard; the new leg must have a much bigger "
                             "thigh than the leg on this sheet", "Tờ M02 cũ của dạng 2: lấy màu, nét của chân và bọc vỏ sò")]
    check(refs)
    sd = save_dir(2)
    p = os.path.join(pk(2), "luot_3_chan.txt")
    sc, title, en, vi = STEP3
    t = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image and save it "
         "as the step says. Do not reply with text only.", "", "REFERENCE IMAGES (open each file from its full path):"]
    t += [f"image {i} = {W(r)}: {en_}" for i, (r, en_, _) in enumerate(refs, 1)]
    t += ["", "WHAT THIS IS: one more sheet of separate, complete parts of the tide-warrior water-dragon newt of image 1, for a 2D "
          "cut-out animation rig (the software bends the straight leg at the knee and the tail with bones).", "",
          PALETTE2, "", WATER, "", f"=== STEP {sc} ({title}) ===", PIECES, en, "", LINE, FLAT, BG,
          f"SAVE this step: save it as a PNG to {W(os.path.join(sd, sc + '.png'))} (if that file already exists, save it as "
          f"{sc}_2.png, {sc}_3.png ... in the same folder instead). Do not change, move or delete any other file.", ""]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gp = os.path.join(pk(2), "HUONG_DAN.md")
    gd = open(gp, encoding="utf-8").read().rstrip("\n").split("\n")
    gd += ["", "## Lượt 3: chân liền cả chi + đuôi chóp to (sau lần soi của Claude điều phối)", "",
           f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT lưu `{W(os.path.join(sd, 'M03.png'))}`. Claude tự gen: "
           "`py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm01_2/luot_3_chan.txt`.", "", f"- **{sc}**: {vi}",
           "- Kiểm: đùi to rõ ràng (gần gấp đôi ống chân), hai đầu chân tròn kín không có nắp ống; đuôi chóp cuộn to; tô phẳng."]
    open(gp, "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p


def build():
    made = [build_form(1)]
    if os.path.exists(chosen(1)):
        made.append(build_form(2))
    for k in (1, 2):
        if os.path.exists(chosen(k)):
            made.append(build_sheets(k))
    if os.path.exists(os.path.join(save_dir(2), "M02.png")):
        made.append(build_luot3())
    for p in made:
        print(W(p))
    if not os.path.exists(chosen(1)):
        print("(chưa dựng dạng 2: chưa có", W(chosen(1)) + ")")


if __name__ == "__main__":
    build()
