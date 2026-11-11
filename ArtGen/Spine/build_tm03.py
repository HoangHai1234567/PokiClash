"""Gói GPT dòng tm03 của lô 10 tướng mới đảo Thủy (đặc tả: ArtGen/Spine/quai/DAC_TA_LO_THUY.md).

Con gốc tham khảo: một con nòng nọc / ếch tròn của game khác (chỉ giữ chủ đề "ếch / nòng nọc tròn có hình xoắn ốc"; hình, màu,
chi tiết, diễn xuất là của mình; KHÔNG đính ảnh con gốc vào prompt).

Thiết kế (tên đề xuất):
  dạng 1  Nòng Xoáy   nòng nọc vừa nhú chân, thân tròn, đuôi vây cuộn xoắn ốc như ngọn dương xỉ / vỏ ốc (chibi)
  dạng 2  Ếch Lốc     ếch sừng trưởng thành phục thấp thế vồ, lam cô-ban đốm xoáy đen chàm, sừng mày xoắn, túi kêu vàng
                      trơn có gợn, áo choàng lá súng (dạng cuối: đổi màu đậm, thêm đồ, đổi chi tiết đặc trưng, đổi dáng).
                      Tránh trùng lô: dòng 1 đã có giáp vai vỏ ốc xoắn; dạng 2 của dòng 1, 4, 5, 6, 8 đều chàm đậm.

Pha 1 chỉ có concept trọn con (một ảnh mỗi dạng). Dạng 2 chỉ dựng khi đã chọn concept dạng 1 (CHOSEN).

    py -3 -I ArtGen/Spine/build_tm03.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm03_1/luot_1_concept.txt
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm03_2/luot_1_concept.txt
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm03"
INBOX = os.path.join(HERE, "inbox")
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))

# concept Claude đã chọn của từng dạng (tên file trong inbox/tm03_<k>/tai_ve/); None = chưa chọn
# dạng 1: bản 1 (mặt quả quyết nhất, chân tay tách rõ); _2 mặt chán, _3 mặt chính diện
# dạng 2 lượt đầu: bản 1, 2 bị điều phối trả (xoắn ốc khắp lưng, sừng cừu); gen lại lần 3 theo thiết kế mới
# dạng 2 bản 3 (L1_concept_3.png): tự chọn theo ủy quyền của điều phối (đốm tròn + vòng gợn, sừng mí vuốt sau, lá súng lục lam)
CHOSEN = {1: "L1_duyet.png", 2: "L1_concept_3.png"}  # dạng 1 do Claude điều phối duyệt (chép từ L1_concept.png)


def W(*p):
    return os.path.normpath(os.path.join(*p))


def save_dir(k):
    return W(INBOX, f"{CODE}_{k}", "tai_ve")


def pack_dir(k):
    return W(HERE, "gui_gpt", f"{CODE}_{k}")


def ref(name):
    return W(INBOX, name, "tai_ve", "L1_lien.png")


LINE = ("LINE AND COLOUR: the hand-drawn look of the style images: drawn by hand on paper with a dark-brown ink pen (#2B2118), "
        "an outline about {n} px thick on this canvas, the same weight on every edge, slightly wobbly like a real pen; every "
        "area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner "
        "than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, no shadow under the feet, "
        "nothing on the background), no white highlights or shine spots on the skin, no gloss, no wet look, no glow, no rim "
        "light, no gradients, no 3D look. The only white allowed is one small catchlight dot in each eye. A darker tone appears "
        "only where the design itself has a darker colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure. No text, no labels, no frame, no ground line, no water, no bubbles, no effects around the "
      "creature.")
SPIRIT = ("an ANIMAL creature of the water element (no human face, no human body, no human clothes; it wears only the gear "
          "listed below, if any), designed like a creature of a "
          "monster-collecting game: appealing, simple readable shapes. Its face is DETERMINED and ready to fight: lowered "
          "brows, confident focused eyes looking to the viewer's right, mouth slightly open; never a happy mascot grin, never "
          "scary.")

FORMS = {
    1: {
        "name": "Nòng Xoáy",
        "refs": [
            (ref("canh_cut_1"),
             "another hero of the same game, 1536x1024, white background: copy its framing, its pose logic (three-quarter side "
             "view facing right, a round body with short limbs separated by white gaps) and its hand-drawn pen line and flat "
             "crayon colouring. Do NOT copy its species, design or colours",
             "Cánh Cụt Con đã duyệt (1536 × 1024, nền trắng): chim cánh cụt tròn xanh mòng két cầm chảo, nhìn sang phải. Lấy "
             "khung, cách đứng tách chân tay, nét"),
            (ref("kuba_1"),
             "another approved hero of the same game, 1536x1024, white background: match EXACTLY its hand-drawn pen line, crayon "
             "texture, flat colouring, simple readable shapes and determined expression. Do NOT copy its species, design or "
             "colours",
             "Kuba dạng 1 đã duyệt (1536 × 1024, nền trắng): cua cam đeo pha lê, mặt quả quyết. Lấy nét bút, vân sáp, nét mặt"),
            (WORLD_STYLE,
             "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured "
             "pencil / wax crayon hatching), nothing of its content",
             "Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét"),
        ],
        "who": (
            "THE CREATURE: a WHIRLPOOL TADPOLE, a tadpole that is just turning into a little frog. It hatched in the eye of a "
            "whirlpool and spins its coiled tail like a propeller to stir up whirlpools.\n"
            "FORM 1, the young stage: clearly chibi like a monster-collecting game starter, the head-and-body ball is most of "
            "its size, big expressive eyes, tiny limbs. Cute but already brave.\n\n"
            "DESIGN (follow exactly):\n"
            "- BODY: ONE big round plump ball (head and body are a single shape, like a fat tadpole), a little wider than tall. "
            "The back and the top of the head are cerulean blue (#3FA9E0) with three or four short navy (#24407F) curved stripe "
            "marks on the back, each mark curling at its end into a small spiral hook. The belly, the chin and the throat are "
            "lemon cream (#F6E28C), one clean area with a smooth edge.\n"
            "- EYES: two big round bulging frog eyes sitting on TOP of the head, the near one big and the far one peeking out "
            "behind it. Golden amber iris (#F2B23A) with a HORIZONTAL dark-brown pupil (a frog's pupil), one small white "
            "catchlight dot. A thick cerulean lid drawn low across the top of each eye gives a lowered, determined brow.\n"
            "- MOUTH: a wide frog mouth along the front of the ball (on the viewer's right), SLIGHTLY OPEN: we can see the flat "
            "deep-rose inside of the mouth (#C9506A) and the rounded tip of a pink tongue (#E58A9C) lying in it. No teeth.\n"
            "- LEGS: two short newly sprouted hind legs under the rear half of the ball, the near one in front and the far one "
            "peeking out behind it, each ending in a webbed foot with three round tangerine toe pads (#F28A3C) flat on the "
            "ground. Two tiny stubby front legs under the chin, also with tangerine toe pads, held a little forward.\n"
            "- TAIL (the signature): a long fat tadpole tail growing from the rear of the ball on the viewer's LEFT, with a wide "
            "pale-aqua fin (#9FE1F0) running round its whole edge, COILED UP INTO A BIG FLAT SPIRAL of about two and a half "
            "turns, like a fern fiddlehead or a snail shell, standing up behind the rear of the body. Navy (#24407F) bands run "
            "along the coil so the spiral reads clearly; the core of the tail is cerulean like the back. The coil is about as "
            "tall as the body ball. It touches the body only at its root; white space between the coil and the eyes and head.\n"
            "- Nothing else: no horns, no hair, no fins on the head, no shell, no accessories, no water drops."),
        "pose": (
            "- Side three-quarter view turned toward the viewer's RIGHT; the mouth and the eyes face the viewer's right.\n"
            "- It sits low on its hind feet, all feet flat on one level ground line (no ground drawn), leaning slightly forward, "
            "a grounded ready-to-fight stance.\n"
            "- White gaps between the two hind legs, between the front legs and the hind legs, and between each front leg and "
            "the belly where possible.\n"
            "- The coiled tail is on the viewer's LEFT behind the body and never crosses the body, the legs or the eyes.\n"
            "- Nothing covers the face."),
        "size": "about 600 px tall from the top of the eyes to the feet, and about 760 px wide including the tail",
        "check": [
            "Nòng nọc tròn mập, **nhìn sang phải**, mắt to lồi trên đỉnh đầu, tròng vàng hổ phách, **con ngươi ngang**, mí dày hạ "
            "xuống cho mặt quả quyết (không cười).",
            "Lưng xanh cerulean có 3–4 vằn lam đậm cuộn móc; bụng, cằm vàng chanh kem.",
            "Miệng rộng **hé**, thấy lòng miệng hồng đậm và chóp lưỡi hồng; không răng.",
            "Hai chân sau ngắn, hai chân trước tí hon, đệm ngón cam; các chân tách nhau và tách bụng bằng khe trắng.",
            "**Đuôi cuộn xoắn ốc** (khoảng 2,5 vòng) dựng sau mông bên trái, vây xanh nước nhạt, vằn lam đậm chạy theo vòng; "
            "đuôi không đè lên thân, mắt.",
            "Tô phẳng, không bóng, không điểm sáng trên da (trừ chấm mắt), nền trắng tinh, không giọt nước, không bong bóng."],
    },
    2: {
        "name": "Ếch Lốc",
        "refs": [
            (ref("vay_lam_3"),
             "another hero of the same game, 1536x1024, white background: copy its framing, its pose logic (a low, forward "
             "leaning ready-to-pounce stance on four limbs, three-quarter side view facing right, limbs separated by white "
             "gaps) and its fierce determined attitude, its hand-drawn pen line and flat crayon colouring. Do NOT copy its "
             "species, design or colours",
             "Vây Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): cá voi sát thủ bốn chân xanh lam, phục thấp thế vồ, nhìn sang "
             "phải. Lấy khung, thế đứng, thần thái dữ, nét"),
            (None,
             "FORM 1 of this same creature (approved), 1536x1024, white background: keep the same species, the same golden "
             "frog eyes with horizontal pupils, the lemon-cream belly, the navy hook stripe marks (now only on the lower legs), the tangerine toe "
             "pads and the drawing style, so the line clearly grows up; the new form is much bigger, stronger and cooler. Do "
             "NOT copy its chibi proportions, its round ball body or its coiled tail",
             "Concept dạng 1 đã chọn (1536 × 1024, nền trắng): nòng nọc tròn xanh cerulean, đuôi cuộn xoắn ốc"),
            (WORLD_STYLE,
             "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + coloured "
             "pencil / wax crayon hatching), nothing of its content",
             "Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét"),
        ],
        "who": (
            "THE CREATURE: the WHIRLPOOL HORNED FROG, the grown-up form of the whirlpool tadpole of image 2. Its tail is gone; "
            "the whirlpool power now lives in its swept-back brow horns and its huge throat sac, and its croak sends spinning "
            "rings of water. It wears the lily pad of the old pond king as a mantle.\n"
            "FORM 2, the FINAL stage of this two-stage line: fully grown and NOT chibi at all: a big, heavy, broad horned frog "
            "with a powerful athletic body, the head about one third of its body length, sharp narrowed eyes. The coolest and "
            "most beautiful design of the line: fierce, proud and battle-hardened, but NOT scary or monstrous. A sturdy, wide, "
            "heavy frog (not a slim ninja frog, not a human-like frog warrior).\n\n"
            "DESIGN (follow exactly):\n"
            "- COLOURS (deeper and bolder than form 1, like a poison-dart frog): back, head top and the outside of the legs "
            "vivid deep cobalt blue (#2457C5). PATTERN ON THE BODY AND HEAD: round black-navy (#1A1F3D) spots of different "
            "sizes, and on the back and the thighs a few RIPPLE MARKS: a black-navy dot with one or two thin concentric rings "
            "around it, like a raindrop falling on a pond. ABSOLUTELY NO SPIRALS, NO SWIRLS and NO CURLS anywhere on the body, "
            "the head or the belly. Only on the outside of the four lower legs: two or three short black-navy curved hook "
            "stripes, like the stripe marks of form 1. The belly, the chin and the inside of the legs are saffron lemon "
            "(#F5CE3A), plain.\n"
            "- HEAD: a wide flat frog head with a broad mouth. Two big golden amber eyes (#F09A2A) with HORIZONTAL dark pupils "
            "set high on the head, narrowed under heavy lowered brows, one small white catchlight dot each. BROW HORNS: from "
            "the top of each upper eyelid grows one pointed flat horn, like the eyelid horns of a real horned frog: a short "
            "leaf-shaped skin spike, cobalt with a pale aqua (#7FD3E0) back edge, swept straight BACKWARD and a little upward "
            "as if blown back by a whirlwind, its tip pointing to the viewer's LEFT. The two horns are straight or gently "
            "curved, never curled, never rolled into a spiral, never ram or goat horns, no rings on them.\n"
            "- MOUTH: the wide mouth SLIGHTLY OPEN in a fierce snarl: the mouth corners turn DOWN (never a smile, never a "
            "smirk); we see the flat deep-rose inside of the mouth (#B8405A), a pink tongue lying in it, and a row of small "
            "pointed cream teeth along the jaws with two slightly bigger fangs.\n"
            "- THROAT SAC: under the chin a round throat sac about as wide as the head, half inflated like a ball, plain "
            "saffron lemon with NO spiral on it, only two or three short thin black-navy ripple arcs along its lower edge. It "
            "hangs below the chin, in front of the chest, and does NOT cover the front legs.\n"
            "- MANTLE AND GEAR: a big round LILY PAD worn as a short mantle over the shoulders and the top of the back: flat "
            "TEAL-GREEN (#2F8A7A, a blue-green water-plant colour, not grass green) with lighter teal (#5FB8A6) vein lines "
            "radiating from its centre and the typical notch cut into its edge, its rim slightly wavy. It is tied across the "
            "chest with a twisted reed rope (straw #D8B867) fastened by one round gold clasp (#E2A93B) engraved with a small "
            "spiral (the only spiral of the design). The mantle stays on the shoulders and back: it does not hang over the legs "
            "or the face. Each front forearm wears a band of the same twisted reed rope. No shells, no metal armour plates.\n"
            "- LIMBS: thick strong front legs with webbed hands of three long fingers, each finger ending in a round tangerine "
            "pad (#EE7F38) with a short dark claw. Huge folded hind legs (big frog thighs) with long webbed feet, tangerine toe "
            "pads.\n"
            "- No tail, no hair, no cloth cape (the lily pad is the only mantle), no weapon, no water or effects."),
        "pose": (
            "- Side three-quarter view turned toward the viewer's RIGHT; the head is at the right, the eyes look to the "
            "viewer's right.\n"
            "- A low crouched READY-TO-POUNCE stance on all four limbs, all hands and feet flat on one level ground line (no "
            "ground drawn): the two front legs straight and planted wide apart under the chest, the near front leg in front, "
            "the far front leg peeking out behind it with a white gap between them; the big hind legs folded at the rear on "
            "the viewer's left, the near hind leg in front, the far hind foot visible behind it with a white gap. The head is "
            "raised forward, the mouth toward the viewer's right.\n"
            "- White gaps between the front legs and the hind legs, and between the front legs and the throat sac.\n"
            "- Nothing covers the face; the swept-back brow horns, the lily-pad mantle and the throat sac do not cross each other or the eyes."),
        "size": ("about 660 px tall from the top of the horns to the feet, and about 1150 px wide, with at least 100 px of "
                 "white margin on every side"),
        "check": [
            "Ếch sừng to, nặng, **phục thấp bốn chi thế vồ**, nhìn sang phải; không chibi, không mảnh kiểu ninja, không đứng như "
            "người.",
            "Lưng **lam cô-ban** đậm tươi, **đốm tròn đen chàm và vòng gợn đồng tâm** (như giọt rơi xuống mặt nước); **không xoắn "
            "ốc nào trên thân, đầu, bụng**; vằn móc chỉ ở cẳng chân; bụng, cằm vàng chanh nghệ trơn.",
            "Mắt hổ phách con ngươi ngang, mày nặng hạ xuống; **sừng mí mắt nhọn dẹt vuốt thẳng ra sau** (cô-ban, mép sau lam "
            "nhạt), không cuộn, không giống sừng cừu Ma Kết.",
            "Miệng hé **khoé trễ xuống, gầm dữ** (không cười, không nhếch), thấy lòng miệng hồng đậm, lưỡi, hàng răng nhỏ và hai nanh.",
            "**Túi kêu** vàng trơn phồng dưới cằm (rộng cỡ đầu), chỉ có 2–3 gợn đen chàm ở mép dưới, không xoắn ốc; không che chân "
            "trước.",
            "**Áo choàng lá súng lục lam** (`#2F8A7A`, gân `#5FB8A6`, có khía) phủ vai và lưng, buộc chéo ngực bằng dây sậy vàng rơm, "
            "khoá tròn vàng khắc xoắn ốc nhỏ (xoắn ốc duy nhất); băng dây sậy ở cẳng tay trước. Không vỏ ốc, không giáp kim loại.",
            "Không đuôi; chân trước, chân sau tách nhau bằng khe trắng; tô phẳng, không bóng, nền trắng tinh."],
    },
}


def check(refs):
    missing = [p for p, _, _ in refs if not p or not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(str(m) for m in missing))


def refs_of(k):
    out = []
    for p, en, vi in FORMS[k]["refs"]:
        if p is None:  # concept đã chọn của dạng trước
            if not CHOSEN.get(k - 1):
                return None
            p = W(save_dir(k - 1), CHOSEN[k - 1])
        out.append((p, en, vi))
    return out


def build_form(k):
    f = FORMS[k]
    refs = refs_of(k)
    if refs is None:
        return None
    check(refs)
    pk, sd = pack_dir(k), save_dir(k)
    os.makedirs(pk, exist_ok=True)
    os.makedirs(sd, exist_ok=True)
    out = W(sd, "L1_concept.png")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {p}: {en}." for i, (p, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {out}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not "
          "edit, move or delete any other file.", "",
          "TASK: design and draw ONE creature hero as ONE full-body picture, in a clean animation-ready pose, in the hand-drawn "
          "style of the reference images. It is a NEW design of our own: do not copy any existing creature or character.", "",
          "CREATURE: " + SPIRIT, "", f["who"], "",
          "CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. The whole creature "
          "is visible, nothing cut by the edges, at least 60 px of white margin all round. It is centred, " + f["size"] + "; "
          "its lowest point is about 120 px above the bottom edge.", "",
          "POSE (very important: the picture will be cut into parts and animated with a 2D skeleton, so body parts must be "
          "readable and must not overlap):", f["pose"], "",
          LINE.format(n=7), FLAT, BG]
    p1 = W(pk, "luot_1_concept.txt")
    open(p1, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: dòng tm03, dạng {k} ({f['name']})", "",
          "Lô 10 tướng mới đảo Thủy (đặc tả `ArtGen/Spine/quai/DAC_TA_LO_THUY.md`), pha 1: concept trọn con một ảnh. Ghi chú "
          f"thiết kế cả dòng: `{W(INBOX, 'tm03_ghichu.md')}`.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{p1}`. GPT tự mở ảnh mẫu theo đường dẫn ghi trong file và lưu ảnh vào `{out}` "
          "(trùng tên thì `L1_concept_2.png`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_1_concept.txt` (chạy nền; thêm "
          "`--note \"...\"` để sửa nhanh).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{p}` | {vi} |" for i, (p, _, vi) in enumerate(refs, 1)]
    gd += ["", "Không đính ảnh con gốc (game khác) hay ảnh chụp trang xem: thiết kế chỉ tả bằng lời.", "",
           "## Kiểm ảnh", ""]
    gd += [f"- {c}" for c in f["check"]]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Có bóng, mảng sáng tối, điểm sáng trên da | `Flat colour only: remove every shadow, highlight, shine spot and "
           "gradient; keep the crayon hatching as texture; only one small catchlight dot in each eye.` |",
           "| Quay sang trái | `Mirror the creature so it faces the viewer's RIGHT.` |",
           "| Mặt cười, vui tươi | `More determined face: heavy lowered brows, focused eyes, mouth slightly open, not a happy "
           "grin.` |",
           "| Miệng khép | `Open the mouth slightly so the deep-rose inside of the mouth and the tongue are visible.` |",
           "| Chân tay dính nhau, dính thân | `Leave clear white gaps between the legs and between the legs and the body.` |"]
    if k == 1:
        gd += ["| Đuôi không cuộn xoắn hoặc đè lên thân | `The tail must coil up into a big flat spiral (about two and a half "
               "turns) standing behind the body on the viewer's left, touching the body only at its root.` |",
               "| Giống một con vật quen trong game khác (bụng trắng có xoắn ốc) | `The belly is plain lemon cream with no "
               "spiral; the only spirals are on the coiled tail and the small stripe hooks on the back.` |"]
    else:
        gd += ["| Còn chibi, đầu to | `Not chibi at all: a big heavy grown-up horned frog, the head about one third of its "
               "body length, powerful limbs.` |",
               "| Đứng hai chân như người, hoặc mảnh như ninja | `It crouches low on all four limbs like a real frog, heavy "
               "and broad, ready to pounce.` |",
               "| Còn đuôi | `No tail: the grown frog has lost its tail.` |"]
    open(W(pk, "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p1


# ---------------------------------------------------------------- lượt 2: tờ mảnh (cách lai, DAC_TA mục 5)
# Thân chính cắt thẳng từ concept; tờ GPT chỉ cho phần phải tách / bị che và làm nguồn vẽ bù.
PIECES = ("THIS IS A SHEET OF SEPARATE PARTS for a 2D cut-out animation rig, NOT a scene: every part is drawn COMPLETE and on "
          "its own, flat on the white page like stickers laid out on a table, with at least 60 px of pure white between any two "
          "parts and between a part and the image edge. No part touches or overlaps another. Do not draw a whole creature, do "
          "not draw extra parts, do not draw labels, numbers, arrows or guide lines.")
SAME = ("Every part must look EXACTLY like the same part on the approved concept (image 1): same silhouette and proportions, "
        "same size as on image 1 (the sheet is drawn at the same scale as image 1), same colours, same markings, same pen line "
        "and crayon texture. Only add what is hidden on image 1.")

PARTS = {
    1: [
        ("M01", "ball, mouth, eyes",
         "Canvas 1536 x 1024.\n"
         "- LEFT HALF (x 0-760): the BODY BALL alone, at the same size as on image 1 (about 475 px wide and 410 px tall): the "
         "round head-and-body ball with the same silhouette, colours and markings as on image 1 (cerulean back with the navy "
         "hook stripe marks, the lemon belly with its curved edge, the wide frog mouth at the front on the viewer's right, open "
         "as on image 1 with the deep-rose inside and the tongue). Draw it WITHOUT the two eye bumps (the top of the ball is a "
         "complete smooth round dome there), WITHOUT legs and WITHOUT the tail: where they attach on image 1, draw the hidden "
         "belly, back and bottom of the ball complete, with the outline closed all round.\n"
         "- RIGHT HALF (x 780-1536): a grid of 2 columns x 3 rows of small parts, each centred in its cell:\n"
         "  row 1 left: the NEAR EYE CLOSED: the big near eye bump of image 1 (a cerulean dome about 190 px wide and 160 px "
         "tall, with its rounded bottom) with the eye SHUT: the whole dome cerulean, one thick dark-brown curved line across "
         "its lower half where the eye is closed (a stern frown sloping down toward the front), no iris, no pupil.\n"
         "  row 1 right: the FAR EYE CLOSED: the smaller far eye bump of image 1 (about 135 px wide and 120 px tall), drawn "
         "complete, shut the same way.\n"
         "  row 2 left: the MOUTH INSIDE: one soft rounded patch of flat deep rose (#C9506A), about 190 px wide and 130 px tall, "
         "with a slightly darker throat spot (#9E3550) in its upper middle and a pink tongue (#E58A9C) lying in its lower half; "
         "brown ink outline all round; no teeth, no lips.\n"
         "  row 2 right: a TONGUE alone: one soft pink tongue (#E58A9C) drawn perfectly straight and horizontal, the root on "
         "the LEFT, about 190 px long and 48 px thick, the tip on the right rounded, one thin darker rose line along its middle.\n"
         "  row 3: empty.",
         "quả bóng thân (không mắt, không chân, không đuôi; nguồn vẽ bù), mắt gần nhắm, mắt xa nhắm, lòng miệng có lưỡi, lưỡi duỗi"),
        ("M02", "tail and legs",
         "Canvas 1536 x 1024.\n"
         "- TOP ROW: the TAIL UNCOILED: the same tail as the coiled spiral tail of image 1, but laid out perfectly STRAIGHT and "
         "horizontal like a long ribbon seen from the side, the root (where it joins the body) at the LEFT, the tip at the RIGHT, "
         "about 1400 px long. The root end is thick (about 115 px from the top edge of the fin to the bottom edge of the fin) "
         "and it tapers smoothly and evenly to a narrow rounded tip (about 24 px). A cerulean (#3FA9E0) core band runs along the "
         "middle, with the pale-aqua fin (#9FE1F0) along the WHOLE top edge and the WHOLE bottom edge (each fin band about a "
         "quarter of the thickness), and navy (#24407F) bands crossing the core at regular intervals (about 11 bands, a little "
         "closer together toward the tip). The root end is a rounded stump. No curl, no spiral, no bend at all: a ruler-straight "
         "ribbon.\n"
         "- BOTTOM ROW, three parts from left to right with white between them, each drawn as ONE piece:\n"
         "  (a) the NEAR HIND LEG from the hip to the toes, in the bent pose of the near hind leg of image 1, but about 15% "
         "SHORTER and clearly CHUBBIER (a plump round thigh, a short thick shin), the webbed foot flat on the ground with three "
         "round tangerine (#F28A3C) toe pads; the top (hip) end is a big rounded stump that will sit under the body ball.\n"
         "  (b) the NEAR FRONT LEG from the shoulder to the toes, as the front leg under the belly on image 1 but about 15% "
         "shorter and chubbier, standing almost straight, the foot flat with three tangerine toe pads, the top end a rounded "
         "stump.\n"
         "  (c) the FAR FRONT LEG, the same design as (b) but a little smaller and standing straight.",
         "đuôi duỗi thẳng (1400 px, gốc 115 px thuôn còn 24 px, vây hai mép, 11 vằn), chân sau gần, chân trước gần, chân trước xa "
         "(ngắn hơn concept 15 %, mập hơn)"),
    ],
    2: [
        ("M01", "body without legs, mouth, eyelids",
         "Canvas 1536 x 1024.\n"
         "- LEFT PART (x 0-960): the BODY WITHOUT ITS FOUR LEGS, at the same size and in the same pose as on image 1 (about 900 "
         "px wide from the rump to the snout): the torso with its cobalt skin, black-navy spots and ripple marks, the saffron "
         "belly, the lily-pad mantle, the reed rope with the gold clasp, the throat sac, and the head exactly as on image 1 "
         "(horns, eyes, the open snarling mouth with its teeth). Leave out all four legs: where they attach on image 1 (the big "
         "hind thigh, the near front leg, the far legs), draw the hidden side of the torso, the hip and the belly complete, with "
         "the body outline closed all round.\n"
         "- RIGHT PART (x 1000-1536): four small parts, one below the other, centred, with white between them:\n"
         "  (a) the MOUTH INSIDE: one soft patch shaped like the open mouth of image 1 (a long low lens, about 300 px wide and "
         "95 px tall), flat deep rose (#B8405A) with a darker throat spot (#8E2F48) at its left (back) end and a pink tongue "
         "(#E27C92) lying along its lower half; brown ink outline; NO teeth, no lips.\n"
         "  (b) a TONGUE alone: one soft pink tongue (#E27C92) drawn perfectly straight and horizontal, root on the LEFT, about "
         "220 px long and 46 px thick, rounded tip, one thin darker line along its middle.\n"
         "  (c) the NEAR EYELID CLOSED: a patch of cobalt skin (#2457C5, crayon hatching) shaped like the big near amber eye of "
         "image 1 together with its heavy brow (about 110 px wide and 80 px tall), with one thick dark-brown curved line across "
         "it where the eye is shut, sloping down toward the snout (a fierce frown); no iris, no pupil.\n"
         "  (d) the FAR EYELID CLOSED: the same for the small far eye of image 1 (about 70 px wide and 60 px tall).",
         "thân không bốn chân (nguồn vẽ bù chỗ chân che), lòng miệng có lưỡi, lưỡi duỗi, mí mắt gần nhắm, mí mắt xa nhắm"),
        ("M02", "far legs",
         "Canvas 1536 x 1024. Two parts side by side with at least 150 px of white between them, each drawn as ONE piece at the "
         "same size as on image 1:\n"
         "  (a) on the left, the FAR HIND LEG complete, as the hind leg seen at the far left of image 1 but drawn whole: the "
         "thigh (hidden on image 1 behind the big near thigh) with its rounded hip end at the top, the bent lower leg and the "
         "long webbed foot flat on the ground with its tangerine toe pads and dark claws, the hook stripe marks on the lower leg.\n"
         "  (b) on the right, the FAR FRONT LEG complete, as the front leg at the far right of image 1 but drawn whole: the "
         "upper arm with its rounded shoulder end at the top (hidden on image 1 behind the throat sac), the forearm with its reed "
         "band and hook stripes, the webbed hand flat on the ground with three long fingers, tangerine pads and dark claws.",
         "chân sau xa trọn (cả đùi bị che), chân trước xa trọn (cả cánh tay trên bị che)"),
    ],
}


def build_parts(k):
    """lượt 2 (tờ mảnh) của dạng k: chỉ dựng khi đã có concept duyệt của dạng k."""
    if not CHOSEN.get(k) or k not in PARTS:
        return None
    concept = W(save_dir(k), CHOSEN[k])
    refs = [(concept, "the APPROVED CONCEPT of this creature, 1536x1024: every part you draw belongs to THIS creature and is "
                      "drawn at the SAME SCALE as this picture", f"Concept dạng {k} đã duyệt (1536 × 1024, nền trắng)"),
            (WORLD_STYLE, "the game's hand-drawn map: use ONLY its line and colouring style (brown ink pen outline + coloured "
                          "pencil / wax crayon hatching)", "Ảnh mốc nét vẽ (1024 × 1536)")]
    check(refs)
    sd, pk = save_dir(k), pack_dir(k)
    steps = PARTS[k]
    order = [s[0] for s in steps]
    t = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image per step "
         "and save each one as its step says. Do not reply with text only.", "",
         "REFERENCE IMAGES (open each file from its full path):"]
    t += [f"image {i} = {p}: {en}." for i, (p, en, _) in enumerate(refs, 1)]
    t += ["", f"WHAT THIS IS: sheets of separate, complete parts of the creature of image 1, for a 2D cut-out animation rig. The "
              "main body is cut from image 1 itself; these parts are the ones that must move on their own or are hidden on "
              "image 1, so each must be drawn whole, clean, and well separated from the others.", "",
          f"SAVE: every step's image goes into {sd} under the step's name (for example {order[0]}.png). If that file already "
          "exists, add _2, _3 ... before .png. Do not change, move or delete any other file.", "",
          f"ORDER: draw step {order[0]} now, save it and stop. Each time I say \"next\", draw the next step, save it and stop, in "
          f"this order: {', '.join(order[1:]) or '(none)'}.", "", SAME, ""]
    for sc, title, en, _ in steps:
        t += [f"=== STEP {sc} ({title}) ===", PIECES, en, "", SAME, LINE.format(n=7), FLAT, BG,
              f"SAVE this step: save it as a PNG to {W(sd, sc + '.png')} (if that file already exists, save it as {sc}_2.png, "
              f"{sc}_3.png ... in the same folder instead). Do not change, move or delete any other file.", ""]
    p2 = W(pk, "luot_2_manh.txt")
    open(p2, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = [open(W(pk, "HUONG_DAN.md"), encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")]
    gd += ["", "## Lượt 2: tờ mảnh (cách lai: thân chính cắt từ concept, tờ này chỉ cho phần tách / bị che)", "",
           f"**Chỉ gửi GPT đường dẫn:** `{p2}`, các bước {', '.join(order)} (gõ `next` sau mỗi ảnh). GPT lưu vào `{sd}`.", "",
           f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_2_manh.txt --steps "
           f"{','.join(order)}`.", "",
           "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{p}` | {vi} |" for i, (p, _, vi) in enumerate(refs, 1)]
    gd += ["", "Kiểm: mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ≥ 60 px, đúng cỡ và hình như trên concept, tô phẳng.", ""]
    gd += [f"- **{sc}**: {vi}" for sc, _, _, vi in steps]
    gd += ["", "| Sai | Gửi thêm |", "|---|---|",
           "| Mảnh khác hình, khác cỡ concept | `Draw each part with the same silhouette, proportions and size as on image 1.` |",
           "| Đuôi vẽ cong | `The tail must be a ruler-straight horizontal ribbon, root on the left, tapering to the tip on the right.` |",
           "| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |"]
    open(W(pk, "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p2


def build():
    for k in sorted(FORMS):
        p = build_form(k)
        if p:
            print(p)
        else:
            print(f"(chưa dựng dạng {k}: chưa chọn concept dạng {k - 1}, sửa CHOSEN trong build_tm03.py)")
        p2 = build_parts(k)
        if p2:
            print(p2)


if __name__ == "__main__":
    build()
