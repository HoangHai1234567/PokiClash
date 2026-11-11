"""Gói GPT vẽ concept dòng ếch xanh (mã tạm `ech_xanh`, tướng thứ 2 đảo Thủy; người dùng lên ý 2026-11-11, chưa đặt tên).

Ý người dùng: một con ếch xanh, lưỡi đỏ thè ra khỏi miệng buông trước bụng; idle bụng thở phình co, lưỡi đung đưa; đánh thường há
miệng bắn lưỡi dài; chiêu bắn nước chỉ há miệng; chiêu cuối phình bụng rồi ợ ra cầu nước; chết ngã ngửa lè lưỡi; dạng 2 to hơn,
chiến hơn. Rig và nhịp animation học từ một con quái ếch của game tham khảo (ghi chú mổ xẻ: ArtGen/Spine/inbox/ech_xanh_ghichu.md).
Không đính ảnh con gốc vào prompt; thiết kế tả bằng lời; nét vẽ là nét của dự án (bút mực nâu + chì sáp, tô phẳng).

  dạng 1  ếch tròn nhỏ, lưỡi đỏ buông trước bụng. Người dùng chọn bản có hai tay trước (L1_concept_2.png, gen bằng --note) và
          dặn chân sau bên kia phải khuất sau thân lúc nghỉ; `ech_xanh.py bo_chan_xa` xoá chân đó -> L1_sua.png = L1_duyet.png
  dạng 2  cùng con, to hơn, chiến hơn (ý người dùng); ảnh mẫu là L1_duyet.png của dạng 1

Lượt 1: concept trọn con một ảnh, miệng khép. Lượt 2 (thân không lưỡi, dáng há miệng, lòng miệng, lưỡi ngắn, lưỡi dài, chân rời)
viết sau khi người dùng duyệt concept.

    py -3 -I ArtGen/Spine/build_ech_xanh.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/ech_xanh_1/luot_1_concept.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "ech_xanh"
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
SHARK = os.path.join(HERE, "inbox", "vay_lam_1", "tai_ve", "L1_lien.png")      # nét, tô sáp phẳng (Thủy, đã duyệt)
PENGUIN = os.path.join(HERE, "inbox", "canh_cut_1", "tai_ve", "L1_lien.png")   # chibi tròn, mặt quả quyết (Thủy, đã duyệt)


def W(p):
    return os.path.normpath(p)


def pk(k):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def chosen(k):
    """Concept đã chọn của dạng k (chép từ L1_concept*.png sau khi người dùng duyệt)."""
    return os.path.join(save_dir(k), "L1_duyet.png")


# ---------------------------------------------------------------- thiết kế (tiếng Anh, dán vào prompt)
PALETTE = ("COLOURS (use exactly these, each area one flat colour): back, head, eyelids, legs and feet fresh leaf green "
           "(#5DB947); the round spots on the back darker green (#3C8C3A); belly and throat pale cream (#F4EBCB, never left "
           "as bare white paper); tongue bright red (#D93A32) with a thin darker red centre line (#A8231F); eyeballs pale "
           "yellow (#F7E37E); pupils and the two nostril dots dark brown-black (#2B2118); one tiny white dot in each pupil; "
           "every outline dark-brown ink (#2B2118).")

FORM1 = ("CREATURE: a small, plump GREEN FROG, a pet-like battle creature of the water element in a monster-collecting game: "
         "iconic, appealing, as simple as possible, readable at a tiny size. Cute but with a determined, ready-to-fight "
         "face. It is an original design: do not imitate any existing franchise character.\n"
         "FORM 1, the first and smallest form:\n"
         "- BODY: head and body are ONE big round shape with NO neck, like a round dumpling sitting on the ground, a little "
         "wider than tall (about 1.15 to 1). The UPPER part (top of the head and the back) is leaf green, like a smooth cap "
         "that covers the top and the back (viewer's left) side. The LOWER FRONT part is one big, round, bulging pale-cream "
         "BELLY (throat and belly are one single round bulge) that takes a bit more than half of the front of the body. The "
         "belly is completely plain: no marks, no navel, no folds.\n"
         "- MOUTH: the border between the green upper part and the cream belly at the front IS the mouth: ONE long, very "
         "wide, CLOSED mouth line that runs from the far right edge of the face, across the front, to the left cheek, a "
         "smooth curve with the corners turned slightly DOWN (determined, not smiling). The green upper lip overhangs the "
         "cream belly a little, like the brim of a cap. No teeth. Two tiny nostril dots on the green part just above the "
         "middle of the mouth.\n"
         "- EYES: two round bulging frog eyes that sit ON TOP of the head like two domes sticking up above the head's "
         "outline. The NEAR eye (on the viewer's left of the two) is the bigger one, about 125 px across; the FAR eye, to "
         "the right of it, is about 100 px across and is partly hidden behind the curve of the head. Each eye: a pale-yellow "
         "eyeball, a big dark horizontal-oval pupil looking toward the viewer's RIGHT, one tiny white dot in the pupil, and "
         "a heavy GREEN upper eyelid that covers the top third of the eyeball and slants down toward the nose: a calm, "
         "stubborn, battle-ready stare. No eyelashes, no eyebrows, no spiral or swirl pattern in or on the eyes.\n"
         "- TONGUE (the signature of this creature): a long, flat, bright RED tongue hangs OUT of the closed mouth. It comes "
         "out from under the upper lip at the front of the mouth (a little to the right of the centre of the body) and "
         "hangs straight DOWN in front of the cream belly like a soft ribbon. It is about 80 px wide at the mouth, widens "
         "slightly to about 95 px near the tip, and is about 230 px long; the tip is rounded with one small notch in the "
         "middle; a thin darker red line runs down its centre. It has its own closed ink outline, lies flat over the belly, "
         "and its tip ends about 90 px ABOVE the bottom of the belly: it touches neither the ground nor the feet.\n"
         "- LIMBS: two short FRONT legs (arms) and two hind legs, but only THREE limbs are visible. NEAR front leg: a short "
         "chubby green arm that comes out of the side of the body just below the left end of the mouth line and reaches down "
         "to the ground at the lower-centre-left, ending in a small hand with three round fingers planted flat on the ground; "
         "it stays left of the tongue with clear cream belly between them. NEAR hind leg: at the lower-left of the body, a "
         "big round folded green thigh pressed against the side of the body, and under it one flat webbed foot with three "
         "short round toes pointing right. FAR front leg: only its small three-fingered hand peeks out from under the belly "
         "at the lower-right, on the ground. The FAR HIND leg is completely hidden behind the body: do NOT draw it; exactly "
         "ONE limb is visible on the far (right) side.\n"
         "- MARKINGS: four round darker-green spots of different sizes (25 to 60 px) on the back, on the upper-left part of "
         "the body; flat spots with no outline. NO spiral, NO swirl, NO stripes anywhere on the creature. No tail, no fins, "
         "no clothes, no accessories.")

FRAME1 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
          "visible, nothing cut by the edges. The frog is centred horizontally; the round body is about 560 px wide and about "
          "490 px tall, the eyes rise about 70 px above it; the soles of both feet are on one horizontal level about 170 px "
          "above the bottom edge of the image. At least 150 px of white above the eyes.")

PALETTE2 = ("COLOURS (use exactly these, each area one flat colour): back, head, eyelids, brow ridges, legs and feet deep "
            "forest green (#3F9A3C), clearly darker than image 1; the spots and the back bumps dark green (#2A6B33); belly and "
            "throat pale cream (#F4EBCB, never left as bare white paper); tongue deep red (#C92A2A) with a thin darker red "
            "centre line (#8E1B1B); eyeballs amber yellow (#F2C94C); pupils and the two nostril dots dark brown-black "
            "(#2B2118); one tiny white dot in each pupil; every outline dark-brown ink (#2B2118).")

FORM2 = ("CREATURE: the GROWN FORM of the green frog of image 1 (form 1, approved): the same creature, the same design "
         "language and drawing style, in the SAME pose and the same layout of parts, but clearly BIGGER, HEAVIER and more "
         "of a FIGHTER: a burly bullfrog brawler. It must be instantly recognisable as the same line. Tough and "
         "battle-hardened, not cute-chubby, not scary, not evil.\n"
         "FORM 2:\n"
         "- BODY: head and body are still ONE big round mass with no neck, but broader and heavier: wide powerful "
         "shoulders, a wide heavy jaw, about 1.25 times wider than tall. The upper part (top of the head and the back) is "
         "deep forest green; the lower front is one big round pale-cream BELLY (throat and belly as one bulge), completely "
         "plain: no marks, no navel, no folds, no muscles drawn on it.\n"
         "- MOUTH: exactly as in image 1, the border between the green upper part and the cream belly IS the mouth: ONE "
         "long, very wide, CLOSED mouth line from the far right edge of the face to the left cheek, corners turned clearly "
         "DOWN in a hard scowl. The green upper lip overhangs the belly like the brim of a cap. No teeth, no fangs. Two "
         "tiny nostril dots above the middle of the mouth.\n"
         "- EYES: two bulging frog eyes on top of the head as in image 1, but SMALLER relative to the body (near eye about "
         "120 px across, far eye about 95 px and partly hidden behind the head), so the body reads as big. Amber-yellow "
         "eyeballs, dark horizontal-oval pupils looking toward the viewer's RIGHT, one tiny white dot in each. Each eye has "
         "a heavy green upper eyelid that covers the top HALF of the eyeball and slants steeply down toward the nose, and "
         "above each eye the eyelid rises into ONE short, blunt, pointed BROW RIDGE like a small horn swept backward (about "
         "45 px long): a fierce, narrow, battle-ready glare. No eyelashes, no spiral or swirl pattern.\n"
         "- TONGUE (the signature and the weapon of this creature): a long, thick, flat deep-RED tongue hangs OUT of the "
         "closed mouth exactly as in image 1: it comes out from under the upper lip a little to the right of the centre of "
         "the body and hangs straight DOWN in front of the cream belly. It is longer and heavier than in image 1: about 95 "
         "px wide at the mouth, about 300 px long, and its tip swells into a heavy rounded club about 135 px wide with one "
         "small notch in the middle, like a boxing glove on a ribbon; a thin darker red line runs down its centre. It has "
         "its own closed ink outline, lies flat over the belly, and its tip ends about 80 px ABOVE the bottom of the belly: "
         "it touches neither the ground nor the hands or feet.\n"
         "- LIMBS: exactly the same three visible limbs as in image 1, in the same places, but thicker and stronger. NEAR "
         "front leg: a thick, strong green arm that comes out of the side of the body just below the left end of the mouth "
         "line and reaches down to the ground at the lower-centre-left, ending in a big hand with three round fingers "
         "planted firmly on the ground, the elbow pushed slightly outward like a wrestler bracing; it stays left of the "
         "tongue with clear cream belly between them. NEAR hind leg: at the lower-left, a big round folded thigh pressed "
         "against the body and under it a wide webbed foot with three round toes pointing right. FAR front leg: only its "
         "three-fingered hand peeks out from under the belly at the lower-right, on the ground. The FAR HIND leg is "
         "completely hidden behind the body: do NOT draw it; exactly ONE limb is visible on the far (right) side.\n"
         "- MARKINGS: five round dark-green spots of different sizes (30 to 70 px) on the back, on the upper-left part of "
         "the body, flat spots with no outline; and along the top of the back, behind the near eye, a row of THREE small "
         "blunt rounded bumps (each about 35 px wide, 20 px high) that break the outline like a low crest. NO spiral, NO "
         "swirl, NO stripes anywhere. No tail, no fins, no clothes, no armour, no accessories, no scars.")

FRAME2 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
          "visible, nothing cut by the edges. The frog is much bigger in the frame than in image 1: centred horizontally, "
          "the body is about 900 px wide and about 720 px tall, the eyes and brow ridges rise about 70 px above it; the "
          "undersides of the hands and of the foot are on one horizontal level about 70 px above the bottom edge of the "
          "image. At least 50 px of white above the brow ridges and at least 60 px of white left and right.")

POSE = ("VIEW (very important: the picture will be cut into separate parts and animated with a 2D skeleton): three-quarter "
        "view turned toward the viewer's RIGHT, sitting still and upright on the ground, mouth CLOSED, the tongue hanging "
        "relaxed and straight, not swinging, not curled. Not jumping, not leaning, not squashed. The only overlaps are: the "
        "tongue in front of the belly, the near arm and the near thigh in front of the body, and the belly in front of the "
        "far hand. No drool, no drops, no splashes, no puddle, no flies, no lily pad, nothing around the frog.")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images: drawn by hand on paper with a dark-brown "
        "ink pen (#2B2118), an outline about 7 px thick on this canvas, the same weight on every outer edge, slightly wobbly "
        "like a real pen; closed outlines around the body, each eye, the tongue, the near thigh and each foot; the mouth "
        "line and eyelid lines drawn with the same pen, about 5 px. Every area coloured with coloured pencils and wax "
        "crayons, the strokes visible as loose diagonal hatching (strokes thinner than the outline), kept inside the "
        "outline. Clean and appealing, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no darker rim, no shadows of any kind (no cast shadow, no shadow "
        "under the figure, under the tongue, on the ground or on the background), no white highlights or shine spots on the "
        "skin, belly or tongue, no gloss, no wet or slimy look, no reflections, no glow, no rim light, no gradients, no 3D "
        "look. The only white dot allowed is the tiny one inside each pupil. A different tone appears only where the design "
        "itself lists a different colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no frame, no props, no effects around "
      "the creature.")


def refs_of(k):
    style = [
        (SHARK, "an approved hero of the same game (a blue shark beast), 1536x1024, white background: match EXACTLY its "
                "pen line, crayon texture and flat colouring. Do NOT copy its species, design, face or colours.",
         "Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): cá mập xanh lam bốn chân. Chỉ lấy nét bút, vân sáp, cách tô phẳng"),
        (PENGUIN, "another approved hero of the same game (a chibi penguin), 1536x1024, white background: see how simple, "
                  "round and readable a first form is in this style and how determined its face looks. Do NOT copy its "
                  "species, design, face, colours or props.",
         "Cánh Cụt dạng 1 đã duyệt (1536 × 1024, nền trắng): chim cánh cụt chibi. Lấy độ đơn giản, tròn trịa, vẻ quả quyết"),
        (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + "
                      "coloured pencil / wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp"),
    ]
    if k == 1:
        return style
    return [(chosen(1), "FORM 1 of THIS creature (approved), 1536x1024, white background: keep its body shape language, its "
                        "pose, the layout of its parts (mouth line = border of green and cream, tongue hanging in front of "
                        "the belly, near arm, near thigh, far hand), its line and its colouring style. Form 2 is the same "
                        "frog grown big, heavy and fierce; do not simply enlarge it.",
             "Ếch xanh dạng 1 đã duyệt (1536 × 1024, nền trắng): ếch xanh lá tròn, bụng kem, lưỡi đỏ buông trước bụng, tay gần "
             "chống đất, đùi gần bên trái, bàn tay xa ló bên phải")] + style


FORMS = {1: ("ếch xanh dạng 1 (chưa đặt tên)", FORM1, FRAME1, PALETTE),
         2: ("ếch xanh dạng 2 (chưa đặt tên)", FORM2, FRAME2, PALETTE2)}

CHECK = {
    1: ["Một con **ếch xanh lá tròn như cục bánh**, đầu liền thân không cổ, hơi rộng hơn cao; nửa trên lưng và đầu xanh, nửa "
        "dưới phía trước là **bụng kem to tròn, trơn**.",
        "**Miệng khép** là đường ranh xanh và kem, rất rộng, hai khoé hơi trễ xuống (quả quyết, không cười).",
        "**Lưỡi đỏ** dẹt thè ra từ miệng, buông thẳng trước bụng như dải ruy băng, có viền mực riêng, đầu lưỡi tròn có khía "
        "nhỏ; **không chạm đất, không chạm chân**.",
        "Hai **mắt ếch lồi** trên đỉnh đầu, tròng vàng nhạt, con ngươi bầu dục ngang nhìn sang phải, mí trên xanh sụp một "
        "phần ba; **không có hình xoắn ốc** ở đâu cả.",
        "**Ba chi lộ ra**: tay gần chống đất phía trước đùi, đùi gần to tròn bên trái dưới với bàn chân màng ba ngón, bàn tay "
        "xa ló dưới bụng bên phải. **Chân sau bên kia khuất hẳn** (bên phải chỉ thấy một chi). Không đuôi.",
        "Vài đốm xanh đậm trên lưng (phía trái trên). Nhìn nghiêng 3/4 sang **phải**, ngồi yên.",
        "Tô phẳng: **không** bóng, không điểm sáng, không ướt bóng; viền mực nâu; nền trắng tinh."],
    2: ["Cùng con với dạng 1, **cùng dáng ngồi và cùng cách xếp các phần**, nhưng **to, nặng, bè vai hơn hẳn** (chiếm gần hết "
        "khung), xanh **đậm hơn**.",
        "Mặt **dữ hơn**: mí sụp nửa mắt, xếch mạnh, mỗi mắt có một **gờ mày nhọn tù** như sừng nhỏ; khoé miệng trễ hẳn. Không "
        "răng nanh, không ác.",
        "**Lưỡi dài, dày hơn**, đầu lưỡi phình như găng đấm; vẫn buông thẳng trước bụng, có viền riêng, không chạm đất, tay, chân.",
        "Tay gần **to khoẻ**, khuỷu hơi bạnh; đùi gần to; bàn tay xa ló bên phải. **Chân sau bên kia khuất hẳn** (bên phải chỉ "
        "thấy một chi).",
        "Ba u tròn nhỏ dọc sống lưng sau mắt gần; năm đốm xanh đậm trên lưng; bụng kem trơn; không xoắn ốc.",
        "Nhìn nghiêng 3/4 sang **phải**; tô phẳng, không bóng, không điểm sáng; viền mực nâu; nền trắng tinh."],
}

FIX = [("Có bóng, mảng sáng tối, điểm sáng trắng trên da, bụng, lưỡi",
        "Flat colour only: remove every shadow, highlight, shine spot, darker rim and gradient; keep the crayon hatching as "
        "texture only. The only white dot is the tiny one inside each pupil."),
       ("Miệng há hoặc cười toe", "The mouth is CLOSED: one long wide line where the green meets the cream belly, corners "
                                  "turned slightly down; the tongue comes out from under the upper lip."),
       ("Lưỡi cong, vắt sang bên, chạm đất hoặc chạm chân", "The tongue hangs straight down in front of the belly like a "
                                                           "flat ribbon and ends about 90 px above the bottom of the "
                                                           "belly; it touches neither the ground nor the feet."),
       ("Bên phải thấy hai chi (thừa chân)", "On the far (right) side exactly ONE limb is visible: the small far hand under "
                                             "the belly. Remove the far hind leg completely; it is hidden behind the body."),
       ("Mắt có xoắn ốc hoặc bụng có hoa văn", "No spiral or swirl anywhere: plain pale-yellow eyeballs with a horizontal "
                                               "oval pupil; the belly is plain cream with no marks."),
       ("Quay sang trái hoặc nhìn thẳng", "Turn the frog three-quarters toward the viewer's RIGHT: pupils look right, the "
                                          "far eye is smaller and partly hidden, the near thigh is at the lower-left."),
       ("Mặt hiền, cười, quá dễ thương", "Give it a determined, stubborn, battle-ready face: heavy upper eyelids slanting "
                                         "down toward the nose, mouth corners turned down. Still cute, not scary."),
       ("Dạng 2 chỉ là dạng 1 phóng to, vẫn dễ thương", "Form 2 is a burly fighter, not an enlarged baby: broader shoulders "
                                                          "and jaw, smaller eyes relative to the body, eyelids covering "
                                                          "half of each eye and slanting steeply, blunt brow ridges, a "
                                                          "hard scowl, a thick arm, a longer tongue with a heavy club tip."),
       ("Dạng 2 đổi dáng, đổi chỗ các phần", "Keep exactly the pose and layout of image 1: sitting three-quarters to the "
                                             "right, mouth closed, tongue hanging straight in front of the belly, near arm "
                                             "planted on the ground, near thigh at the lower-left, far hand at the lower-right."),
       ("Có đất, vũng nước, lá sen, ruồi", "Remove everything around the frog: pure white background, no ground, no props.")]


def check(refs):
    missing = [W(p) for p, _, _ in refs if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def build_form(k):
    name, form, frame, palette = FORMS[k]
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
          form, "", palette, "", frame, "", POSE, "", LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: dòng `{CODE}` dạng {k} ({name})", "",
          "Tướng thứ 2 đảo Thủy, người dùng lên ý 2026-11-11: ếch xanh lưỡi đỏ; dạng 2 cùng con, to hơn, chiến hơn. Ghi chú thiết kế và mổ xẻ con gốc: "
          "`ArtGen/Spine/inbox/ech_xanh_ghichu.md`.", "",
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


if __name__ == "__main__":
    print("dạng 1:", build_form(1))
    if os.path.exists(chosen(1)):
        print("dạng 2:", build_form(2))
    else:
        print("dạng 2: chưa dựng (chưa có", W(chosen(1)) + ")")
