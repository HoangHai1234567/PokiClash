"""Gói GPT vẽ concept dòng tm02 (lô 10 tướng mới đảo Thủy, 2026-11-11, đặc tả ArtGen/Spine/quai/DAC_TA_LO_THUY.md).

Dòng "Thạch Giải" (tên đề xuất): cua ẩn sĩ cõng tảng đá làm nhà. Thay suất ải 5 đảo Thủy (Tiểu Y, common).
Chỉ giữ chủ đề "giáp xác mang đá trên lưng" của con tham khảo; hình, màu, chi tiết, diễn xuất là của mình. Không đính ảnh con
tham khảo hay ảnh chụp trang xem: ảnh mẫu chỉ là ảnh đã duyệt của dự án.

    py -3 -I ArtGen/Spine/build_tm02.py                 dựng file prompt (dạng 2 chỉ dựng khi đã chọn concept dạng 1, CHON)
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm02_1/luot_1_concept.txt
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm02_2/luot_1_concept.txt

Pha 1 chỉ có concept. Tờ mảnh (pha 2) dựng sau khi người dùng duyệt concept.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm02"
INBOX = os.path.join(HERE, "inbox")
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
VAY_LAM_1 = os.path.join(INBOX, "vay_lam_1", "tai_ve", "L1_lien.png")
MA_KET_1 = os.path.join(INBOX, "ma_ket_1", "tai_ve", "L1_lien.png")
VAY_LAM_3 = os.path.join(INBOX, "vay_lam_3", "tai_ve", "L1_lien.png")

# concept Claude đã chọn cho từng dạng (tên file trong inbox/tm02_<k>/tai_ve/); dạng sau chỉ dựng khi dạng trước đã chọn
CHON = {1: "L1_concept_2.png"}


def W(p):
    return os.path.normpath(p)


def save_dir(k):
    return os.path.join(INBOX, f"{CODE}_{k}", "tai_ve")


def chosen(k):
    f = CHON.get(k)
    return os.path.join(save_dir(k), f) if f else None


LINE = ("LINE AND COLOUR: the hand-drawn look of the style images: drawn by hand on paper with a dark-brown ink pen (#2B2118), "
        "an outline about {n} px thick on this canvas, the same weight on every edge, slightly wobbly like a real pen; every "
        "area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner "
        "than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind, no white highlights or shine spots, no gloss, "
        "no glow, no rim light, no gradients, no 3D look. The only white allowed is one small catchlight dot in each eye (and "
        "the cream colours named in the design). A darker tone appears only where the design itself has a darker colour.")
NOSHADOW = ("NO SHADOWS: no drop shadow, no hard offset shadow, no cast shadow, no shadow under the feet or on the ground or "
            "background.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure. No text, no labels, no frame, no ground line, no water, no splashes, no bubbles, no "
      "other creature, no other rocks than the creature's own house.")

# ---------------------------------------------------------------- dạng 1
DESIGN1 = (
    "THE CREATURE (the FIRST form of its line, a common fighter of the water element): a young HERMIT CRAB that lives inside "
    "a heavy SEA BOULDER and carries it on its back like a house. Chibi proportions: short chunky limbs, the head plate and "
    "the eyes big for its body. Personality: the tough, stubborn little guard of the tide pools; determined frowning face, "
    "ready to fight. NOT a smiling mascot, NOT scary.\n"
    "\n"
    "BODY PARTS AND COLOURS:\n"
    "- BOULDER HOUSE (on its back, the left part of the figure): one big, rounded, lumpy sea boulder, a little bigger than "
    "the crab's own front body, with a wide round opening on its RIGHT side out of which the crab's front body comes. Colour: "
    "dark wet basalt, flat charcoal blue-grey (#4B5160), with a few thin lighter grey crack lines (#7A8290). On it: a cluster "
    "of five small cream barnacles (#F4EEDC; little cones with a dark slit on top), two or three flat coral-pink crust "
    "patches (#EE8C8C) shaped like lichen, and ONE small tuft of three green seaweed ribbons (#5DB34F) growing from the top "
    "and flopping back to the left. The crab's body fills the opening; only a thin dark crescent of the inside of the "
    "opening (#2E3240) shows around it.\n"
    "- HEAD AND FRONT BODY: a rounded shield-shaped head plate in flat slate blue (#6A8BBB) with two small blunt points "
    "above the eyes; its lower part and the face around the mouth are pale sea-foam aqua (#BFE6E2).\n"
    "- EYES: two SHORT, THICK eye stalks (slate blue) rising from the top of the head plate, side by side; each eye has an "
    "amber-gold iris (#F2B33D), a large dark pupil and ONE small white catchlight dot; a slate-blue armoured eyelid cap over "
    "the top of each eye gives a stern, frowning look.\n"
    "- ANTENNAE: two long thin coral-pink antennae (#E98A86) from between the eye stalks, sweeping up and back over the "
    "boulder in gentle curves, apart from each other.\n"
    "- MOUTH: a small mouth under the eyes, between two little pale-aqua mouth flaps, slightly open so the deep rose inside "
    "(#C2505E) shows.\n"
    "- BIG CLAW (on the near side, the viewer's side): a chunky HAMMER CLAW: the palm is a big rounded block about as big as "
    "the head plate, slate blue with a pale-aqua inner side and a few flat darker slate-blue round bumps (#56749F); two short, "
    "thick fingers with dark navy tips (#2E3B57), slightly open. It sits on a short, thick, two-segment arm.\n"
    "- SMALL CLAW (on the far side): a slim little pincer on a thin two-segment arm, slate blue with dark navy finger tips, "
    "open.\n"
    "- LEGS: four short walking legs (two on the near side in front, two on the far side behind them), each with three "
    "slate-blue segments, pale-aqua joint bands and a pointed dark navy tip.")
POSE1 = (
    "POSE (important: the picture will be cut into parts for a 2D bone animation rig):\n"
    "- 3/4 side view facing the viewer's RIGHT: the boulder on the left half, the crab's face and claws on the right half.\n"
    "- The crab stands on its four walking legs, spread apart: no leg crosses another leg, every leg tip clearly separate. "
    "The boulder rests on the crab's back; its bottom stays above the leg tips (it does not touch the ground).\n"
    "- The big claw is held forward and low on the right, in front of the chest, slightly open; it does NOT cover the face "
    "or the legs. The small claw is raised up beside the eye stalks, open. Leave white gaps between the claws, the legs and "
    "the body wherever possible.\n"
    "- The mouth is slightly open so the inside of the mouth shows. Both eyes visible.")
CHECK1 = [
    "Cua ẩn sĩ **nhìn sang phải**, góc 3/4; tảng đá bazan xám than (không phải đá be) bên trái, có hà kem, mảng san hô hồng, "
    "một túm rong xanh; thân cua ló ra từ cửa đá.",
    "Vỏ cua xanh lam ngả xám (slate), mặt dưới lam bọt nhạt; mắt vàng hổ phách trên **hai cuống ngắn** có nắp mí giáp; hai "
    "râu hồng san hô dài vắt ra sau.",
    "Một **càng búa to** phía gần (thấp, trước ngực, không che mặt, không che chân), một **càng nhỏ** giơ lên cạnh cuống mắt; "
    "bốn chân bò tách nhau, không chéo; đáy tảng đá không chạm đất.",
    "Miệng hé thấy lòng miệng hồng sẫm; mặt quả quyết, không cười tươi.",
    "Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), không nước, không đất, nền trắng tinh.",
    "Khác hẳn Kuba (cua đỏ cam, pha lê xanh trên lưng, hai mắt tròn trắng, hai càng tròn bằng nhau) và khác con tham khảo "
    "(đá be, một mắt đỏ trong hốc tối, hai càng lưỡi hái băng nhìn thẳng).",
]
FIX1 = [
    ("Có bóng, mảng sáng tối", "Flat colour only: remove every shadow, highlight and gradient; keep the crayon hatching as texture."),
    ("Quay sang trái / nhìn thẳng", "The creature must face the viewer's RIGHT in a 3/4 side view: boulder on the left, face and claws on the right."),
    ("Chân chéo, càng che mặt", "Spread the legs so none crosses another; the big claw stays low in front of the chest, not over the face or legs."),
    ("Đá màu be, giống đá cát", "The boulder is dark charcoal blue-grey basalt (#4B5160), not beige or sand coloured."),
    ("Dễ thương quá, cười", "Make the face stern and determined (frowning eyelid caps, small open mouth), not smiling, not a mascot."),
]

# ---------------------------------------------------------------- dạng 2 (dạng cuối)
DESIGN2 = (
    "THE CREATURE (the FINAL, second form of the same line as image 3): the young hermit crab of image 3 has grown into a "
    "fierce, heavily armoured SIEGE FIGHTER whose house is now a tall jagged sea-stack tower. ADULT proportions, NOT chibi: "
    "the head plate is small compared with the body (about one fifth of the figure's height), narrow sharp eyes, heavy "
    "armour, a planted battle stance. Determined and fierce, cool and strong; NOT cute, NOT a horror monster.\n"
    "\n"
    "KEEP FROM IMAGE 3 (so it reads as the same line): a hermit crab carrying a rock house on its back, amber eyes on short "
    "stalks, coral-pink antennae, ONE big hammer claw on the near side and one smaller claw on the far side, cream "
    "barnacles, coral accents. EVERYTHING ELSE CHANGES: colours deeper, armour added, a different silhouette.\n"
    "\n"
    "BODY PARTS AND COLOURS:\n"
    "- TOWER HOUSE (on its back, rising high above the crab on the left): a tall, jagged BASALT SEA-STACK, clearly taller "
    "than wide, with three or four sharp stepped peaks and layered rock strata. Flat black-blue basalt (#3A3D48) with thin "
    "lighter grey strata lines (#6E7280); clusters of cream barnacles (#EFE6D2); a CROWN of branching deep coral-red coral "
    "(#D9545F) growing from the peaks like antlers; two dark green kelp strands (#3F8F5A) hanging down its left side. The "
    "crab's body comes out of a wide opening low on the tower's right side.\n"
    "- ARMOUR BODY: the head plate, the front body and every leg are covered with deep indigo-slate armour plates (#3D5486) "
    "edged with rows of short bone-white spikes (#EFE6D2); the joints and the underside are sea-green aqua (#7DCBC4).\n"
    "- EYES: two short armoured eye stalks with spiky brow plates; narrow, slanted, fierce amber eyes (#F0A030) with a dark "
    "vertical slit pupil and ONE small white catchlight dot each.\n"
    "- ANTENNAE: two long whip antennae, deep coral red (#C84B4B), sweeping back over the tower in long curves.\n"
    "- MOUTH: armoured mouthparts with two small cream tusk-like mandibles; the mouth open in a battle cry, deep rose inside "
    "(#B8405A).\n"
    "- HAMMER CLAW (near side): a MASSIVE claw, as big as the crab's whole front body, its palm encased in a STONE GAUNTLET "
    "of fused black basalt plates studded with barnacles; two thick fingers with near-black navy tips (#232C44). Held RAISED "
    "high in front of the body, ready to smash.\n"
    "- BLADE CLAW (far side): a long slender pincer in indigo-slate armour with a saw-toothed inner edge, raised and pointing "
    "forward to the right.\n"
    "- LEGS: four armoured walking legs with spiked joints and pointed near-black tips, planted wide.")
POSE2 = (
    "POSE (important: the picture will be cut into parts for a 2D bone animation rig):\n"
    "- 3/4 side view facing the viewer's RIGHT: the tower on the left, the crab's face and claws on the right.\n"
    "- Battle stance on the four walking legs, spread wide: no leg crosses another leg, every leg tip clearly separate. The "
    "tower rests on the crab's back; its bottom stays above the leg tips (it does not touch the ground).\n"
    "- The hammer claw is raised high to the right of the face, NOT covering the face or the eyes; the blade claw is raised "
    "forward below it on the far side, visible. Leave white gaps between the claws, the legs and the body wherever "
    "possible.\n"
    "- The mouth is open so the inside of the mouth shows. Both eyes visible.")
CHECK2 = [
    "Nhận ra cùng dòng với dạng 1 (cua ẩn sĩ cõng nhà đá, mắt hổ phách trên cuống, râu hồng, một càng búa + một càng nhỏ, hà "
    "kem) nhưng **khác hẳn**: tháp đá bazan đen cao lởm chởm (cao hơn rộng), vương miện san hô đỏ, rong nâu xanh rủ.",
    "Tỉ lệ trưởng thành (đầu nhỏ, mắt hẹp xếch đồng tử dọc), giáp chàm đậm viền gai trắng ngà, khớp lam lục.",
    "Càng búa **bọc găng đá bazan** to bằng cả thân trước, giơ cao bên phải mặt (không che mặt); càng lưỡi cưa phía xa thấy rõ.",
    "Nhìn sang phải, bốn chân giáp tách nhau, không chéo; đáy tháp không chạm đất; miệng há có hai nanh kem.",
    "Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh.",
]
FIX2 = [
    ("Vẫn chibi", "Not chibi at all: adult proportions, head plate about one fifth of the height, narrow fierce eyes, heavy armour."),
    ("Giống dạng 1 quá", "The final form must look clearly different from image 3: tall jagged black basalt tower with a coral crown, deep indigo armour with bone-white spikes, a stone-gauntlet hammer claw raised high."),
    ("Có bóng, mảng sáng tối", "Flat colour only: remove every shadow, highlight and gradient; keep the crayon hatching as texture."),
    ("Càng búa che mặt", "Raise the hammer claw to the right of the face; both eyes and the open mouth must stay fully visible."),
]


def refs_common():
    return [(WORLD_STYLE, "the game's approved hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen "
                          "outline + coloured pencil / wax crayon hatching), nothing of its content",
             "Ảnh mốc nét vẽ (1024 × 1536, bản đồ thế giới vẽ tay, nền xanh biển): viền mực nâu hơi rung, tô chì màu và sáp màu. "
             "Chỉ lấy nét")]


def refs_form(k):
    r = refs_common()
    if k == 1:
        r += [(VAY_LAM_1, "an approved creature of the same game, 1536x1024, white background: match EXACTLY its pen line, "
                          "outline weight, crayon texture, flat colouring and fierce determined look. Do NOT copy its "
                          "species, design, colours or pose",
               "Cá voi sát thủ Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): con cá xanh lam bụng trắng, mắt vàng cau "
               "có, nhìn sang phải. Lấy nét bút, độ dày viền, vân sáp, vẻ quả quyết; không chép loài, màu, dáng"),
              (MA_KET_1, "another approved creature of the same game, 1536x1024, white background: match its chibi first-form "
                         "proportions, crayon texture and level of detail. Do NOT copy its species, design, colours or pose",
               "Dê cá Ma Kết dạng 1 đã duyệt (1536 × 1024, nền trắng): dê con xanh lục đuôi cá, sừng xám, lông kem. Lấy tỉ "
               "lệ chibi dạng 1, vân sáp, mức chi tiết; không chép loài, màu, dáng")]
    else:
        r += [(VAY_LAM_3, "an approved FINAL-form creature of the same game, 1536x1024, white background: match its pen line, "
                          "crayon texture, flat colouring, and its fierce, mature fighting attitude. Do NOT copy its "
                          "species, design, colours or pose",
               "Vây Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): cá mập xanh lam đậm dạng cuối, mắt xếch, nhe nanh, thế "
               "chồm, nhìn sang phải. Lấy nét và thần thái; không chép loài, màu, dáng"),
              (chosen(1), "the chosen FIRST FORM of THIS creature's line, 1536x1024, white background: the creature you draw "
                          "is what it grows into. Keep the features listed below, change everything else",
               "Concept dạng 1 đã chọn của dòng (1536 × 1024, nền trắng): cua ẩn sĩ vỏ xanh slate cõng tảng đá bazan có hà, "
               "san hô, rong")]
    return r


FORMS = {
    1: dict(name="Thạch Giải (dạng 1)", design=DESIGN1, pose=POSE1, size=(1000, 760), line=7, check=CHECK1, fix=FIX1),
    2: dict(name="Thạch Thành Giải (dạng 2, dạng cuối)", design=DESIGN2, pose=POSE2, size=(1100, 880), line=7, check=CHECK2,
            fix=FIX2),
}


def check(refs):
    missing = [W(p) for p, _, _ in refs if not p or not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def build_form(k):
    f = FORMS[k]
    pk = os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")
    sd = save_dir(k)
    refs = refs_form(k)
    check(refs)
    os.makedirs(pk, exist_ok=True)
    os.makedirs(sd, exist_ok=True)
    out = os.path.join(sd, "L1_concept.png")
    p1 = os.path.join(pk, "luot_1_concept.txt")
    w, h = f["size"]
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(p)}: {en}" for i, (p, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not "
          "edit, move or delete any other file.", "",
          "TASK: design and draw ONE creature as ONE full picture, in the hand-drawn style of the style images. The reference "
          "creatures only show the drawing style: do not copy their species, design, colours or pose.", "",
          f["design"], "", f["pose"], "",
          f"CANVAS AND FRAMING: landscape 1536x1024, pure-white background. The whole creature is visible, nothing cut by the "
          f"edges; it is about {w} px wide and {h} px tall, centred, with at least 70 px of white margin all round.", "",
          LINE.format(n=f["line"]), FLAT, NOSHADOW, BG]
    open(p1, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: dòng tm02, {f['name']}", "",
          "Lô 10 tướng mới đảo Thủy (đặc tả `ArtGen/Spine/quai/DAC_TA_LO_THUY.md`), dòng tm02 thay suất ải 5 (Tiểu Y). "
          "Cua ẩn sĩ cõng tảng đá làm nhà. Pha 1 chỉ có concept trọn con; tờ mảnh dựng sau khi người dùng duyệt.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p1)}`. GPT tự mở ảnh mẫu theo đường dẫn ghi trong file và lưu ảnh vào "
          f"`{W(out)}` (trùng tên thì `L1_concept_2.png`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}_{k}/luot_1_concept.txt` (chạy nền, khoá "
          "Codex chung, khoảng 2 phút một ảnh).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(p)}` | {vi} |" for i, (p, _, vi) in enumerate(refs, 1)]
    gd += ["", f"Ảnh ra: 1536 × 1024, nền trắng tinh, con vật khoảng {w} × {h} px ở giữa, viền mực khoảng {f['line']} px.", "",
           "## Kiểm", ""]
    gd += [f"- {c}" for c in f["check"]]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `gen.py ... --note \"...\"`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in f["fix"]]
    open(os.path.join(pk, "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    return p1


# ---------------------------------------------------------------- lượt 2 (pha 2): tờ mảnh, cách lai
# Thân, nhà đá, chân, càng, râu, rong cắt thẳng từ concept đã duyệt (tm02_lai.py). Tờ GPT chỉ cho phần không có trên concept:
# mắt nhắm (mí), lòng miệng; thêm ngón càng động vẽ đủ gốc (phần khuất trong lòng càng) làm nguồn vẽ bù.
PARTS = {
    2: dict(
        eye="the eyes of image 2 have an orange-amber iris with a dark vertical slit pupil under a deep indigo-slate armoured "
            "eyelid cap with short bone-white spikes",
        lid="#3D5486",
        size_l="about 180 px wide", size_r="about 190 px wide",
        mouth="deep rose (#B8405A) with a rose-pink tongue (#E27C92) lying in its lower half",
        finger_a="the UPPER FINGER of the big HAMMER CLAW of image 2 (the near-black navy #232C44 curved finger at the top right of "
                 "the stone gauntlet), alone, same size and same curve as in image 2, pointing to the RIGHT; its root continues "
                 "LEFT about 90 px further than what is visible in image 2 (the part hidden inside the gauntlet) and ends in a "
                 "rounded stump",
        finger_b="the UPPER BLADE of the BLADE CLAW of image 2 (the long slender indigo-slate pincer finger at the lower right), "
                 "alone, same size and same curve as in image 2, pointing to the RIGHT; its root continues LEFT about 70 px "
                 "further (the part hidden inside the claw) and ends in a rounded stump",
    ),
    1: dict(
        eye="the eyes of image 2 have an amber-gold iris with a big dark pupil under a slate-blue armoured eyelid cap",
        lid="#6A8BBB",
        size_l="about 240 px wide", size_r="about 230 px wide",
        mouth="deep rose (#C2505E) with a small rose-pink tongue (#E8899A) in its lower half",
        finger_a="the UPPER FINGER of the big HAMMER CLAW of image 2 (the curved finger with a dark navy #2E3B57 tip at the top "
                 "right of the big round claw), alone, same size and same curve as in image 2, pointing to the RIGHT; its root "
                 "continues LEFT about 80 px further than what is visible in image 2 (the part hidden inside the claw palm) and "
                 "ends in a rounded stump",
        finger_b="the UPPER FINGER of the SMALL CLAW of image 2 (the little raised pincer at the right of the eye stalks), alone, "
                 "same size and same curve as in image 2, its root continuing about 40 px further into a rounded stump",
    ),
}


def build_parts(k):
    c = os.path.join(save_dir(k), "L1_duyet.png")
    if not os.path.exists(c):
        return None
    f = PARTS[k]
    pk = os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")
    sd = save_dir(k)
    refs = refs_common() + [(c, "the APPROVED concept of this creature, 1536x1024: every part you draw belongs to THIS creature: "
                                "same colours, same line weight and crayon texture, same shapes. Use it only to know what the "
                                "parts look like; do not redraw the whole creature",
                             "Concept đã duyệt của dạng này (1536 × 1024, nền trắng)")]
    check(refs)
    out = os.path.join(sd, "M01.png")
    p2 = os.path.join(pk, "luot_2_manh.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(p)}: {en}" for i, (p, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as M01_2.png, M01_3.png ... in the same folder. Do not edit, move or "
          "delete any other file.", "",
          "WHAT THIS IS: ONE sheet of separate, complete parts of the hermit crab of image 2, for a 2D cut-out animation rig "
          "(the body itself is cut straight from image 2; this sheet only adds the parts that image 2 does not show). Draw "
          "each part with the SAME SILHOUETTE, PROPORTIONS, COLOURS and DETAILS as on image 2.", "",
          PIECES_TXT, "",
          "Canvas 1536 x 1024. Lay the parts out in a 3 x 2 grid of 512 px cells, one part centred in each cell:",
          f"- top-left cell: the LEFT EYE (the one further left on image 2) CLOSED, drawn TWICE as big as on image 2 ({f['size_l']}): "
          f"{f['eye']}; draw the same eye with the eyelid SHUT: the round eye is completely covered by the eyelid skin "
          f"({f['lid']}, crayon hatching), with ONE thick dark-brown curved line across its lower half (the shut eye, curving "
          "down like a stern frown); the armoured cap on top unchanged; no iris, no pupil, no catchlight, no eye stalk.",
          f"- top-middle cell: the RIGHT EYE CLOSED in the same way, TWICE as big as on image 2 ({f['size_r']}).",
          f"- top-right cell: a MOUTH INTERIOR patch: one simple soft rounded blob, {f['mouth']}, brown ink outline, about "
          "230 px wide and 190 px tall. No teeth, no tusks, no lips.",
          f"- bottom-left cell: {f['finger_a']}.",
          f"- bottom-middle cell: {f['finger_b']}.",
          "- bottom-right cell: leave empty (pure white).", "",
          "The eyes and the mouth patch are drawn twice as big as on image 2, so give them an outline about 14 px thick; the two "
          "fingers are drawn at the size of image 2 with an outline about 7 px thick.",
          LINE.format(n=7).replace("an outline about 7 px thick on this canvas, ", ""), FLAT, NOSHADOW,
          "Plain pure-white background (#FFFFFF): no paper colour, no white border or sticker outline around the parts. No text, "
          "no labels, no numbers, no arrows, no frame, no ground line."]
    open(p2, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = ["", "## Lượt 2 (pha 2, cách lai): tờ mảnh M01", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p2)}`. GPT lưu vào `{W(out)}` (trùng tên thì `M01_2.png`…).", "",
          "Thân, nhà đá, chân, càng, râu, rong cắt thẳng từ concept đã duyệt (`ArtGen/Spine/tm02_lai.py`); tờ này chỉ thêm phần concept "
          "không có. Đang dùng: lòng miệng (ô trên phải). Mắt nhắm làm từ chính mắt concept (phủ kín đúng tròng) nên hai mắt nhắm GPT vẽ "
          "chỉ để dự phòng; hai ngón càng cũng dự phòng (ngón cắt từ concept, gốc vẽ bù).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    gd += [f"| {i} | `{W(p)}` | {vi} |" for i, (p, _, vi) in enumerate(refs, 1)]
    gd += ["", "Ảnh ra: 1536 × 1024 nền trắng, lưới 3 × 2 ô 512: mắt trái nhắm, mắt phải nhắm, lòng miệng (hồng sẫm có lưỡi), ngón trên "
           "càng búa, ngón càng còn lại, ô cuối trống.", "",
           "Kiểm: mảnh rời nhau, không bóng, đúng màu concept; lòng miệng là một mảng tròn không răng.", ""]
    with open(os.path.join(pk, "HUONG_DAN.md"), "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(gd))
    return p2


PIECES_TXT = ("THIS IS A SHEET OF SEPARATE PARTS, NOT a scene: every part is drawn COMPLETE and on its own, flat on the white page "
              "like stickers laid out on a table, with at least 60 px of pure white between any two parts and between a part and "
              "the cell edge. No part touches or overlaps another. Do not draw a whole creature, do not draw extra parts.")


def build():
    made = [build_form(1)]
    c1 = chosen(1)
    if c1 and os.path.exists(c1):
        made.append(build_form(2))
    else:
        print("(chưa dựng dạng 2: chưa chọn concept dạng 1, CHON[1])")
    for k in (1, 2):
        p = build_parts(k)
        if p:
            made.append(p)
    for p in made:
        print(W(p))


if __name__ == "__main__":
    build()
