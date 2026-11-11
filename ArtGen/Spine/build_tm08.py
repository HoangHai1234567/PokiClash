# -*- coding: utf-8 -*-
"""Gói GPT cho dòng tm08 (lô 10 tướng mới đảo Thủy, 2026-11-11): rắn rồng nước thân dài, thay suất ải 50 (Thương Lam, epic).

Con gốc tham khảo (monster_3247, Sword x Staff) là DẠNG 2 của dòng. Theo đặc tả `quai/DAC_TA_LO_THUY.md` mục 3: thiết kế khác hẳn,
chỉ giữ chủ đề "rắn rồng nước thân dài cuộn"; không đính ảnh con gốc. Tên đề xuất: dòng **Uyên Xà** (rắn vực sâu): dạng 1
**Uyên Nhi** (chibi, bé con), dạng 2 **Uyên Xà** (trưởng thành, chiến).

Thứ tự làm: dạng 2 trước (con gốc là dạng 2), chọn concept chép thành `inbox/tm08_2/tai_ve/L1_duyet.png`, rồi mới dựng prompt dạng 1
(đính concept dạng 2 làm ảnh mẫu). Script này dựng cả hai nếu đủ ảnh.

    py -3 -I ArtGen/Spine/build_tm08.py                 dựng gui_gpt/tm08_2/luot_1_concept.txt (+ tm08_1 nếu đã có L1_duyet dạng 2)
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm08_2/luot_1_concept.txt
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm08_1/luot_1_concept.txt
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm08"
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
DRAGON_ADULT = os.path.join(HERE, "inbox", "thuong_lam_3", "tai_ve", "L1_lien.png")
DRAGON_CHIBI = os.path.join(HERE, "inbox", "thuong_lam_1", "tai_ve", "L1_lien.png")
FOX_CHIBI = os.path.join(HERE, "inbox", "kuba_1", "tai_ve", "L1_duyet.png")  # nếu có: concept chibi khác loài đã duyệt


def W(p):
    return os.path.normpath(p)


def pk(k):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def concept_chosen(k):
    return os.path.join(save_dir(k), "L1_duyet.png")


# ---- bảng màu của dòng (không trùng Thủy Long cobalt + ngọc lam, Thương Lam băng, Hải Long xanh ngọc + đỏ san hô, con gốc xanh ngọc + hồng)
COL = {
    "body2": "#2E2F6E",   # dạng 2: chàm vực sâu (indigo đậm)
    "body1": "#5058A8",   # dạng 1: chàm xám nhạt hơn
    "belly": "#D8F3EA",   # bụng: bạc hà trăng
    "fin": "#8FE3D0",     # vây: bạc hà bọt biển
    "spot": "#8FE3D0",    # chấm đèn lồng dọc sườn
    "bone": "#F3EBD9",    # gai sừng xương, răng
    "eye": "#F2B544",     # mắt hổ phách
    "mouth": "#5A2A5E",   # lòng miệng mận tím
    "tongue": "#C56A9A",  # lưỡi
    "lantern": "#C9F7EA", # hạt đèn ở đầu râu
}

LINE = ("LINE AND COLOUR: the hand-drawn look of the style images: drawn by hand on paper with a dark-brown ink pen (#2B2118), "
        "an outline about {n} px thick on this canvas, the same weight on every edge, slightly wobbly like a real pen; every "
        "area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner "
        "than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, nothing on the background), no "
        "white highlights or shine spots, no gloss, no glow, no rim light, no gradients, no 3D look. The only white allowed is "
        "one small catchlight dot in each eye. A darker tone appears only where the design itself has a darker colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure. No text, no labels, no frame, no ground line, no water, no rocks, no other creature.")

DESIGN2 = (
    "THE CREATURE (adult form of a water-element monster line): a DEEP-SEA SERPENT DRAGON, a long legless eel-like sea serpent "
    "with no wings and no legs, grown-up proportions, fierce and ready to fight, NOT cute, NOT a chibi, NOT scary-horror. "
    "Think of a moray eel crossed with an eastern dragon, but drawn as a creature of its own.\n"
    f"- BODY: one long muscular tube, thick behind the head and tapering slowly to the tail; back and sides deep abyss "
    f"indigo ({COL['body2']}); along the whole underside a row of wide belly plates in pale moon-mint ({COL['belly']}) "
    f"separated by thin ink lines; along the upper side ONE row of round flat pale-mint spots ({COL['spot']}), about twelve "
    f"spots from the neck to the tail, getting smaller toward the tail (flat dots, no glow).\n"
    f"- DORSAL SAIL: a tall continuous fin runs along the top of the back from the nape to the tail, like the sail of an oarfish: "
    f"flat seafoam mint ({COL['fin']}) with thin ink fin-rays, its outer edge a soft wavy line (NOT spikes, NOT flames); its "
    f"height about one body thickness.\n"
    f"- TAIL: the body ends in a wide crescent-shaped paddle fin (two rounded lobes, like a whale fluke seen from the side), "
    f"seafoam mint with ink rays.\n"
    f"- HEAD: long and narrow, seen exactly from the side, facing the viewer's RIGHT: a long snout with a slightly hooked upper "
    f"lip, a strong underbite lower jaw, a heavy brow ridge frowning down over the eye, one amber eye ({COL['eye']}) with a "
    f"dark vertical slit pupil and one small white catchlight, a determined fierce look. The mouth is HALF OPEN: inside it the "
    f"flesh is deep plum ({COL['mouth']}), the teeth are cream ({COL['bone']}): two long fangs in the upper jaw and small "
    f"teeth along the lower jaw. On the back of the skull a crown of THREE backward-pointing bone-white spines "
    f"({COL['bone']}), the middle one longest. NO ears, NO ear fins, NO antlers, NO mane.\n"
    f"- BARBELS: two long thin whiskers grow from the chin, one on each side, trailing DOWN and BACK below the jaw in a gentle "
    f"S-curve, body-coloured indigo, each ending in one small round pale lantern bead ({COL['lantern']}, a flat circle).\n"
    f"- PECTORAL FINS: one pair of small pointed fins just behind the head on the sides of the neck (only the near one fully "
    f"visible, the far one peeking behind), seafoam mint with ink rays, swept back.\n"
    "- No arms, no legs, no claws, no wings, no clothes, no weapon, no jewellery.")

POSE2 = (
    "POSE AND COMPOSITION (important, for a cut-out animation rig): the serpent is seen from the side and its body makes ONE "
    "open S-shape lying from left to right, with NO part crossing or overlapping another part:\n"
    "- The TAIL is at the far LEFT, lying low; the paddle fin at the very end is turned so it points up and to the left and is "
    "fully visible.\n"
    "- From the tail the body runs to the right along the bottom, rises into ONE big rounded hump in the middle of the picture, "
    "comes down again, and then the front third of the body REARS UP steeply at the right side into an upright curve.\n"
    "- The HEAD is at the top right, held high, looking to the viewer's RIGHT and slightly down, as if watching an enemy "
    "standing to the right; mouth half open. The two barbels hang below the jaw, both fully visible against white.\n"
    "- The dorsal sail is visible along the whole top edge of the body; the belly plates along the whole lower edge.\n"
    "- Nothing overlaps: the tail does not pass behind or in front of the body, the barbels do not cross the neck, the head "
    "does not cover the sail. Keep at least 40 px of white between any two parts of the body that come near each other.\n"
    "CANVAS AND FRAMING: landscape 1536x1024, pure-white background. The whole creature is visible, nothing cut by the edges, "
    "at least 60 px of white margin all round; the figure is about 1350 px wide and 850 px tall, centred. The head is about "
    "one sixth of the figure's height (adult proportions).")

DESIGN1 = (
    "THE CREATURE: the BABY (first form) of the deep-sea serpent dragon in the concept image, a chibi pet-like monster of the "
    "water element, round and small but with a brave, determined face (NOT a cheerful mascot, NOT scary).\n"
    f"- PROPORTIONS: chibi: the head is about 45% of the whole height, big round eyes, a short plump body.\n"
    f"- HEAD: big and rounded, seen from the side facing the viewer's RIGHT: a short rounded snout with a tiny hooked upper lip, "
    f"a small underbite lower jaw with ONE small cream tooth showing, a heavy little brow frowning over one big round amber eye "
    f"({COL['eye']}) with a dark round pupil and one small white catchlight. Mouth slightly open, deep plum inside "
    f"({COL['mouth']}). On the back of the head ONE short soft bone-white nub ({COL['bone']}) where the adult's spines will "
    f"grow. NO ears, NO ear fins, NO antlers.\n"
    f"- COLOURS: body slate-indigo ({COL['body1']}), clearly lighter than the adult's deep indigo; belly plates pale moon-mint "
    f"({COL['belly']}); THREE round flat pale-mint spots ({COL['spot']}) on the upper side of the body; fins seafoam mint "
    f"({COL['fin']}) with thin ink rays.\n"
    f"- DORSAL SAIL: a soft, oversized, floppy mint fin on top of the head and neck like a mohawk, folding over to the back, "
    f"continuing as a low fin along the short back.\n"
    f"- TAIL: short, ending in a small rounded paddle fin (two little lobes).\n"
    f"- BARBELS: two SHORT chin whiskers, each ending in a small round pale lantern bead ({COL['lantern']}, a flat circle).\n"
    f"- PECTORAL FINS: two tiny rounded fins behind the head.\n"
    "- No arms, no legs, no wings, no clothes, no weapon.")

POSE1 = (
    "POSE AND COMPOSITION (for a cut-out animation rig): side view, the baby rests on its coiled tail like a little spring: the "
    "tail makes ONE low loop lying on the ground at the bottom (the paddle fin sticking out to the LEFT, fully visible), the body "
    "rises from the loop in a short upright curve, the big head sits on top looking to the viewer's RIGHT, chin up, brave. The "
    "barbels hang below the chin against white. Nothing crosses: the tail loop is open (a C-shape, not a closed ring), the fins "
    "do not cover the face.\n"
    "CANVAS AND FRAMING: landscape 1536x1024, pure-white background. The whole creature is visible, at least 80 px of white "
    "margin all round; the figure is about 900 px tall and 800 px wide, centred.")


def refs2():
    return [(WORLD_STYLE, "the game's approved hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen "
                          "outline + coloured pencil / wax crayon hatching), nothing of its content",
             "Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét"),
            (DRAGON_ADULT, "an approved adult monster of the same game, 1536x1024, white background: match EXACTLY its pen line, "
                           "crayon texture, flat colouring, level of detail and adult (non-chibi) proportions. Do NOT copy its "
                           "design, colours, wings, legs or pose: the creature you draw is a legless sea serpent",
             "Rồng băng Thương Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): lấy nét bút, vân sáp, tỉ lệ trưởng thành; không chép dáng, màu")]


def refs1():
    r = [(WORLD_STYLE, "the game's approved hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen "
                       "outline + coloured pencil / wax crayon hatching), nothing of its content",
          "Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét"),
         (DRAGON_CHIBI, "an approved CHIBI monster of the same game, 1536x1024, white background: match EXACTLY its pen line, "
                        "crayon texture, flat colouring and chibi proportions (big head, big eyes). Do NOT copy its design, "
                        "colours, wings or legs",
          "Rồng băng Thương Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): lấy nét, tỉ lệ chibi; không chép dáng, màu"),
         (concept_chosen(2), "the APPROVED ADULT FORM of the creature you draw, 1536x1024, white background: your baby is the "
                             "first form of THIS line: same species, same colour family (lighter body), same mint fins, same "
                             "belly plates, same lantern-tipped barbels, same brow and underbite, but chibi and simpler",
          "Concept dạng 2 (Uyên Xà) đã chọn (1536 × 1024, nền trắng): cùng dòng, bé con phải nhận ra là cùng loài")]
    return r


def check(refs):
    missing = [W(p) for p, _, _ in refs if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def write_prompt(k, refs, design, pose, vi_name, vi_check):
    folder = pk(k)
    os.makedirs(folder, exist_ok=True)
    os.makedirs(save_dir(k), exist_ok=True)
    out = os.path.join(save_dir(k), "L1_concept.png")
    p = os.path.join(folder, "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(pth)}: {en}" for i, (pth, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not "
          "edit, move or delete any other file.", "",
          "TASK: design and draw ONE monster as ONE full picture, in the hand-drawn style of the style images.", "",
          design, "", pose, "", LINE.format(n=6), FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: {vi_name} (`{CODE}_{k}`)", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT lưu ảnh vào `{W(out)}` (trùng tên thì `_2`, `_3`...).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py {W(p)}` (thêm `--note \"...\"` để sửa nhanh).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(pth)}` | {vi} |" for i, (pth, _, vi) in enumerate(refs, 1)]
    gd += ["", "## Kiểm concept", ""] + [f"- {c}" for c in vi_check]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Có bóng, mảng sáng tối, điểm sáng | `Flat colour only: remove every shadow, highlight, glow and gradient; keep the crayon hatching as texture.` |",
           "| Nhìn sang trái | `The head must face the viewer's RIGHT.` |",
           "| Có chân, tay, cánh | `This is a legless, wingless sea serpent: remove all legs, arms, claws and wings.` |",
           "| Thân vắt chéo nhau | `The body must be ONE open S-curve: no part of the body passes in front of or behind another part.` |",
           "| Có tai, vây tai, gạc | `No ears, no ear fins, no antlers: only the three bone-white spines on the back of the skull (one soft nub for the baby).` |",
           "| Có nước, đất, nền | `Pure white background only: no water, no ground, no rocks.` |",
           "| Dạng 2 vẫn chibi | `Not chibi at all: adult proportions, the head about one sixth of the figure's height, small fierce eye.` |"]
    open(os.path.join(folder, "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p


PIECES = ("THIS IS A SHEET OF SEPARATE PARTS for a 2D cut-out animation rig, NOT a scene: every part is drawn COMPLETE and on "
          "its own, flat on the white page like stickers laid out on a table, with at least 60 px of pure white between any two "
          "parts and between a part and the image edge. No part touches or overlaps another. Do not draw a whole creature, do "
          "not draw extra parts, do not draw labels, numbers, arrows or guide lines.")

# tờ mảnh dạng 2 (Uyên Xà): (bước, tiêu đề, mô tả tiếng Anh, ghi chú tiếng Việt)
STEPS2 = [
    ("M01", "head, jaw, mouth, eyelid, fin, barbel, tail paddle",
     "Canvas 1536 x 1024. Lay the parts out in a 3 x 2 grid of 512 px cells, one part group centred in each cell:\n"
     f"- top-left cell: the HEAD, UPPER PART ONLY, side view facing the viewer's RIGHT: skull, heavy frowning brow, one amber eye "
     f"({COL['eye']}, dark vertical slit pupil, one small white catchlight), the long snout with its slightly hooked upper lip, "
     f"the two long cream fangs ({COL['bone']}) hanging from the upper lip, and the crown of THREE backward-pointing bone-white "
     f"spines ({COL['bone']}) on the back of the skull, the middle one longest. Skin deep abyss indigo ({COL['body2']}). NO lower "
     f"jaw, NO neck, NO barbels, NO fins. The back end of the head (where the neck attaches, below and behind the spines) is a "
     f"smooth rounded stump. About 430 px wide (snout to the back of the skull, spines not counted).\n"
     f"- top-middle cell: the LOWER JAW alone, side view facing right, hinge at the LEFT: one long wedge with a strong rounded "
     f"underbite chin, pale moon-mint ({COL['belly']}) underside and indigo side, a row of small cream teeth standing along its "
     f"top edge, and a strip of the deep plum inner mouth ({COL['mouth']}) visible above the gum line; the back end (the hinge) "
     f"is a rounded knob. About 300 px wide.\n"
     f"- top-right cell: TWO separate parts, one above the other with white between them: (a) a MOUTH INTERIOR patch: one soft "
     f"rounded blob of flat deep plum ({COL['mouth']}) with a slightly darker plum throat spot in the middle, about 220 px wide "
     f"and 150 px tall, no teeth; (b) below it, the TONGUE: a soft flat tongue drawn perfectly STRAIGHT and horizontal, root at "
     f"the LEFT (rounded, about 48 px thick) narrowing to a slightly forked tip at the RIGHT, about 230 px long, flat rose "
     f"({COL['tongue']}) with one thin darker line along the middle.\n"
     f"- bottom-left cell: TWO separate parts, one above the other: (a) a CLOSED EYELID: a small almond-shaped patch of the "
     f"head's indigo skin with the brown ink outline all round and ONE thick dark-brown curved line across its lower half (the "
     f"shut eye, curving down toward the snout like a stern frown), about 120 px wide and 76 px tall; (b) below it, ONE "
     f"PECTORAL FIN: a pointed, slightly curved fin of flat seafoam mint ({COL['fin']}) with thin ink rays, its root a rounded "
     f"stump at the LEFT and its point at the RIGHT, about 250 px long and 130 px tall.\n"
     f"- bottom-middle cell: ONE BARBEL: a single thin whisker drawn perfectly STRAIGHT and horizontal, root at the LEFT about "
     f"20 px thick, thinning to the right, body-coloured indigo ({COL['body2']}), ending at the RIGHT in one round flat pale "
     f"lantern bead ({COL['lantern']}) about 46 px across; the whole part about 430 px long.\n"
     f"- bottom-right cell: the TAIL PADDLE FIN alone: a wide crescent fin of two rounded lobes (like a whale fluke seen from "
     f"the side) in flat seafoam mint ({COL['fin']}) with thin ink rays, joined at a short rounded indigo root stump on the "
     f"LEFT, the two lobes spreading up-right and down-right, about 330 px wide and 330 px tall.",
     "đầu (phần trên, có ba gai gáy, nanh), hàm dưới rời, mảng lòng miệng + lưỡi thẳng, mí nhắm + một vây ngực, một râu thẳng có "
     "hạt đèn ở đầu phải, vây đuôi mái chèo hai thuỳ gốc bên trái"),
    ("M02", "body tube",
     "Canvas 1536 x 1024. ONLY ONE part, centred on the page: the BODY of the serpent laid out perfectly STRAIGHT and "
     "horizontal like a long tube seen from the side, about 1450 px long. The LEFT end is the NECK END: the tube is about 150 px "
     "thick there (not counting the sail) and closed with a rounded stump; it tapers slowly and evenly to about 70 px thick at the "
     f"RIGHT end (the tail end), also a closed rounded stump. Colouring along the whole tube: the upper two thirds deep abyss "
     f"indigo ({COL['body2']}); the lower third a row of about 35 wide belly plates in pale moon-mint ({COL['belly']}) separated "
     f"by thin ink lines; along the middle of the indigo part ONE row of round flat pale-mint spots ({COL['spot']}), about 13 "
     f"spots spaced about 105 px apart, about 44 px across at the left shrinking to about 18 px at the right. Along the TOP edge "
     f"runs the DORSAL SAIL: a continuous fin of flat seafoam mint ({COL['fin']}) about 100 px tall on the left half, lowering "
     f"gradually to about 45 px near the right end, its outer edge a soft wavy line (no spikes, no flames), with thin ink "
     f"fin-rays about every 40 px; the base of the sail sits directly on the top outline of the tube with no gap. No head, no "
     f"tail fin, no fins other than the sail, nothing else on the page.",
     "ống thân duỗi thẳng nằm ngang ~1450 px: trái = đầu cổ (dày 150), phải = đuôi (dày 70), vây lưng liền dọc mép trên, hàng "
     "chấm, tấm bụng mép dưới"),
]

# tờ mảnh dạng 1 (Uyên Nhi)
STEPS1 = [
    ("M01", "head, jaw, mouth, eyelid, fin, crest, barbel, tail paddle",
     "Canvas 1536 x 1024. Lay the parts out in a 3 x 2 grid of 512 px cells, one part group centred in each cell:\n"
     f"- top-left cell: the HEAD, UPPER PART ONLY, side view facing the viewer's RIGHT: a big rounded chibi skull, a heavy little "
     f"frowning brow, one big round amber eye ({COL['eye']}, dark round pupil, one small white catchlight), the short rounded "
     f"snout with a tiny hooked upper lip, and ONE short soft bone-white nub ({COL['bone']}) on the back of the head. Skin "
     f"slate-indigo ({COL['body1']}). NO lower jaw, NO neck, NO crest fin, NO barbels. The back-bottom of the head (where the neck "
     f"attaches) is a smooth rounded stump. About 440 px wide.\n"
     f"- top-middle cell: the LOWER JAW alone, side view facing right, hinge at the LEFT: a short rounded underbite chin, pale "
     f"moon-mint ({COL['belly']}) underside and slate-indigo side, ONE small cream tooth standing up near its front, a strip of "
     f"deep plum inner mouth ({COL['mouth']}) above the gum line; the hinge end is a rounded knob. About 230 px wide.\n"
     f"- top-right cell: TWO separate parts, one above the other: (a) a MOUTH INTERIOR patch: one soft rounded blob of flat deep "
     f"plum ({COL['mouth']}) with a slightly darker throat spot, about 170 px wide and 110 px tall, no teeth; (b) below it, the "
     f"TONGUE: a small soft tongue drawn perfectly STRAIGHT and horizontal, root at the LEFT, about 160 px long and 36 px thick, "
     f"flat rose ({COL['tongue']}).\n"
     f"- bottom-left cell: TWO separate parts, one above the other: (a) a CLOSED EYELID: a round-ish patch of the head's "
     f"slate-indigo skin with the brown ink outline and ONE thick dark-brown curved line across its lower half (the shut eye, a "
     f"stern frown), about 135 px wide and 90 px tall; (b) below it, ONE small PECTORAL FIN: a rounded fin of flat seafoam mint "
     f"({COL['fin']}) with thin ink rays, root a rounded stump at the LEFT, about 170 px long and 110 px tall.\n"
     f"- bottom-middle cell: the CREST FIN alone (the baby's big floppy mohawk): a tall soft fin of flat seafoam mint "
     f"({COL['fin']}) with thin ink rays, drawn standing UP: its root is a straight flat base along the BOTTOM edge about 260 px "
     f"wide, from which three or four soft rounded lobes rise upward and lean over to the LEFT; about 400 px wide and 330 px tall.\n"
     f"- bottom-right cell: TWO separate parts, one above the other: (a) ONE short BARBEL: a thin whisker drawn perfectly "
     f"STRAIGHT and horizontal, root at the LEFT about 16 px thick, slate-indigo, ending at the RIGHT in one round flat pale "
     f"lantern bead ({COL['lantern']}) about 40 px across, the whole part about 200 px long; (b) below it, the small TAIL "
     f"PADDLE FIN: two rounded mint lobes joined at a short rounded slate-indigo root stump on the LEFT, about 200 px wide and "
     f"190 px tall.",
     "đầu tròn (phần trên, có mấu xương), hàm dưới nhỏ, lòng miệng + lưỡi, mí + vây ngực, mào vây to dựng đứng gốc ở mép dưới, "
     "râu ngắn có hạt đèn + vây đuôi nhỏ"),
    ("M02", "body tube",
     "Canvas 1536 x 1024. ONLY ONE part, centred on the page: the BODY of the baby serpent laid out perfectly STRAIGHT and "
     "horizontal like a short plump tube seen from the side, about 950 px long. The LEFT end is the NECK END, about 150 px thick "
     "(not counting the fin), closed with a rounded stump; it tapers evenly to about 55 px thick at the RIGHT end (the tail end), "
     f"also a closed rounded stump. Colouring: the upper two thirds slate-indigo ({COL['body1']}); the lower third a row of about "
     f"22 belly plates in pale moon-mint ({COL['belly']}) separated by thin ink lines; THREE round flat pale-mint spots "
     f"({COL['spot']}) about 48 px across on the indigo part of the left half, spaced about 110 px apart. Along the TOP edge runs "
     f"a LOW DORSAL FIN of flat seafoam mint ({COL['fin']}) about 40 px tall at the left, lowering to about 20 px at the right, "
     f"soft wavy outer edge, thin ink rays, its base sitting directly on the top outline of the tube with no gap. No head, no "
     f"tail fin, nothing else on the page.",
     "ống thân ngắn duỗi thẳng ~950 px: trái = cổ (dày 150), phải = đuôi (dày 55), vây lưng thấp mép trên, ba chấm, tấm bụng"),
]


# lượt 3 (Claude điều phối yêu cầu 2026-11-11 sau khi soi so_concept): vây lưng gợn rời cho dạng 2; thân cong đúng dáng concept cho dạng 1
STEPS2B = [
    ("M03", "frilled dorsal fin",
     "Canvas 1536 x 1024. ONLY ONE part, centred on the page: the DORSAL FIN of the serpent on its own, the same frilled dorsal fin "
     "as on the back of the creature in the concept image (same mint colour, same soft scallops, same thin ink fin-rays), drawn "
     "perfectly STRAIGHT and horizontal, about 1450 px long. Its ROOT edge (where it grows out of the back) is the BOTTOM edge: one "
     "straight horizontal line from end to end. The LEFT end is the neck end, the RIGHT end the tail end. Its OUTER (top) edge is a "
     "row of big soft rounded scallops like a frill: the fin is about 170 px tall at the left half, lowering gradually to about "
     f"70 px near the right end. Flat seafoam mint ({COL['fin']}) with thin dark-brown ink fin-rays from the root edge to the "
     "scallop tips about every 45 px. Brown ink outline all round including along the straight root edge. No body, no head, "
     "nothing else on the page.",
     "vây lưng gợn rời duỗi thẳng ~1450 px, mép gốc thẳng ở dưới, mép ngoài gợn to, trái = cổ (cao 170), phải = đuôi (cao 70)"),
]
STEPS1B = [
    ("M03", "curved body",
     "Canvas 1536 x 1024. ONLY ONE part, centred on the page, about 1000 px wide and 850 px tall: the BODY of the baby serpent in "
     "the concept image drawn EXACTLY in the same pose, same silhouette and same proportions as in the concept (do not straighten "
     "it): the short neck rising to the top right, the plump round belly, the body curving down and around to the left, and the "
     "thin tail curling forward to the LEFT and ending in a rounded stump (NO tail paddle). Include the low mint dorsal fin along "
     f"the back and the three pale-mint spots. Colours as in the concept: slate-indigo ({COL['body1']}), belly plates pale moon-mint "
     f"({COL['belly']}) with thin ink lines, dorsal fin seafoam mint ({COL['fin']}). WITHOUT the head (the neck ends at the top in "
     "a closed rounded stump where the head sits), WITHOUT the crest, WITHOUT the pectoral fins, WITHOUT the barbels, WITHOUT the "
     "tail paddle. Draw the parts of the body that the head and the pectoral fins hide in the concept as complete body. Nothing "
     "else on the page.",
     "thân cong đúng dáng concept (cổ lên, bụng tròn, đuôi mảnh vòng ra trước), không đầu, không mào, không vây ngực, không vây đuôi"),
]


def write_parts(k, steps, vi_name, refs_base, ten_file="luot_2_manh.txt"):
    """file prompt tờ mảnh cho dạng k: đính concept đã chọn của dạng đó; mỗi bước một tờ."""
    folder, sd = pk(k), save_dir(k)
    refs = refs_base + [(concept_chosen(k), "the APPROVED CONCEPT of this creature, 1536x1024, white background: every part you "
                                            "draw belongs to THIS creature: same species, same colours, same line and crayon "
                                            "texture, same head design. Use it only to know what the parts look like; do not "
                                            "redraw the scene", f"Concept {vi_name} đã chọn (1536 × 1024, nền trắng)")]
    check(refs)
    order = [s[0] for s in steps]
    p = os.path.join(folder, ten_file)
    t = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image per reply and "
         "save each one as its step says. Do not reply with text only.", "",
         "REFERENCE IMAGES (open each file from its full path):"]
    t += [f"image {i} = {W(pth)}: {en}" for i, (pth, en, _) in enumerate(refs, 1)]
    ci = len(refs)
    t += ["", f"WHAT THIS IS: sheets of separate, complete parts of the sea serpent of image {ci}, for a 2D cut-out animation rig. "
          "The animation software bends the straight body tube, the barbels and the tongue with bones, opens the jaw and swings "
          f"the fins, so every part must be drawn whole (also the areas that are hidden in image {ci}), clean, and well separated "
          "from the others. Same colours, same ink line and crayon texture as the concept.", "",
          f"SAVE: every step's image goes into {W(sd)} under the step's name (for example {order[0]}.png). If that file already "
          "exists, add _2, _3 ... before .png. Do not change, move or delete any other file.", "",
          f"ORDER: draw step {order[0]} now, save it and stop. Each time I say \"next\", draw the next step, save it and stop, in "
          f"this order: {', '.join(order[1:])}.", ""]
    for sc, title, en, _ in steps:
        t += [f"=== STEP {sc} ({title}) ===", PIECES, en, "", LINE.format(n=6), FLAT, BG,
              f"SAVE this step: save it as a PNG to {W(os.path.join(sd, sc + '.png'))} (create the folder if it is missing; if "
              f"that file already exists, save it as {sc}_2.png, {sc}_3.png ... in the same folder instead). Do not change, move "
              "or delete any other file.", ""]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = [f"", f"## Tờ mảnh `{ten_file}`: `{W(p)}`", "",
          f"Các bước {', '.join(order)}, gõ `next` sau mỗi ảnh; GPT lưu vào `{W(sd)}`. Ảnh mẫu thêm: ảnh {ci} = `{W(concept_chosen(k))}`.",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py {W(p)} --steps {','.join(order)}`.", "",
          "Kiểm: mỗi tờ 1536 × 1024, nền trắng, mảnh rời nhau ≥ 60 px, không vẽ cả con; ống thân, râu, lưỡi **thẳng nằm ngang**, "
          "gốc bên trái; đầu chỉ phần trên (không hàm dưới, không cổ)."]
    gd += [f"- **{sc}**: {vi}" for sc, _, _, vi in steps]
    gd += ["", "| Sai | Gửi thêm |", "|---|---|",
           "| Vẽ cả con | `This must be a sheet of separate parts laid flat on white, not a creature or a scene. Redraw only the parts listed.` |",
           "| Ống thân cong | `The body tube must be perfectly straight and horizontal, like a ruler, both ends rounded.` |",
           "| Đầu dính hàm dưới / cổ | `The head part is the UPPER part only: no lower jaw, no neck; the lower jaw is its own separate part.` |",
           "| Mảnh chạm nhau | `Leave at least 60 px of pure white between every two parts.` |"]
    with open(os.path.join(folder, "HUONG_DAN.md"), "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(gd) + "\n")
    return p


def build():
    made = []
    r2 = refs2()
    check(r2)
    made.append(write_prompt(2, r2, DESIGN2, POSE2, "Uyên Xà (dạng 2, trưởng thành)", [
        "Rắn biển thân dài không chân, không cánh, nhìn nghiêng sang **phải**; thân một đường S hở: đuôi trái, bướu giữa, phần trước dựng đứng, không vắt chéo.",
        f"Thân chàm vực sâu `{COL['body2']}`, bụng bạc hà trăng `{COL['belly']}` chia tấm, một hàng chấm tròn bạc hà dọc sườn, vây lưng liền một dải bạc hà `{COL['fin']}` có vân tia, đuôi vây mái chèo hai thuỳ.",
        f"Đầu dài hẹp, hàm dưới trề, mày nhíu, mắt hổ phách `{COL['eye']}` đồng tử dọc; miệng hé thấy lòng miệng mận `{COL['mouth']}`, hai nanh kem; ba gai xương trắng sau gáy; hai râu cằm đầu hạt đèn.",
        "Tỉ lệ trưởng thành (đầu ~1/6 chiều cao), vẻ chiến; không tai, không gạc, không bờm.",
        "Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh, không nước, không đất."]))
    if os.path.exists(concept_chosen(2)):
        r1 = refs1()
        check(r1)
        made.append(write_prompt(1, r1, DESIGN1, POSE1, "Uyên Nhi (dạng 1, chibi)", [
            "Bé rắn biển chibi (đầu ~45%), nhìn sang **phải**, ngồi trên vòng đuôi hở hình chữ C, vây đuôi nhỏ chìa sang trái.",
            f"Thân chàm xám `{COL['body1']}` nhạt hơn dạng 2, bụng bạc hà, ba chấm tròn, vây mào bạc hà mềm to như mào gà úp về sau, hai râu cằm ngắn đầu hạt đèn.",
            "Mắt to tròn hổ phách, mày nhíu, hàm dưới trề nhỏ một răng; một mấu xương trắng sau gáy.",
            "Nhận ra cùng dòng với concept dạng 2 nhưng dễ thương, quả quyết; không linh vật vui tươi.",
            "Tô phẳng, không bóng, nền trắng, không nước, không đất."]))
    else:
        print("(chưa dựng dạng 1: chưa có", W(concept_chosen(2)) + ")")
    # lượt 2: tờ mảnh (chỉ khi concept dạng đó đã chọn)
    if os.path.exists(concept_chosen(2)):
        made.append(write_parts(2, STEPS2, "Uyên Xà dạng 2", r2))
    if os.path.exists(concept_chosen(1)):
        made.append(write_parts(1, STEPS1, "Uyên Nhi dạng 1", refs1()[:2]))
    # lượt 3: vây lưng gợn rời (dạng 2), thân cong đúng dáng (dạng 1)
    if os.path.exists(concept_chosen(2)):
        made.append(write_parts(2, STEPS2B, "Uyên Xà dạng 2", r2, "luot_3_vay_lung.txt"))
    if os.path.exists(concept_chosen(1)):
        made.append(write_parts(1, STEPS1B, "Uyên Nhi dạng 1", refs1()[:2], "luot_3_than_cong.txt"))
    for p in made:
        print(W(p))


if __name__ == "__main__":
    build()
