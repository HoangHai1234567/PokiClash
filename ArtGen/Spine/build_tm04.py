"""Gói GPT concept dòng tm04 của lô 10 tướng mới đảo Thủy (đặc tả: ArtGen/Spine/quai/DAC_TA_LO_THUY.md).

Dòng: Hà Bá (tên đề xuất), hà mã nước: dạng 1 "Hà Mã Con" (chibi tròn), dạng 2 "Hà Bá" (chiến mã hà mã trưởng thành, giáp đồng).
Điểm xuất phát (chỉ chủ đề, không lấy hình): thú tròn miệng rộng, vây/ngạnh lưng, đuôi linh hồn nước. Thiết kế, màu, chi tiết
là của dự án; không đính ảnh con gốc hay ảnh chụp trang xem cho GPT.

    py -3 -I ArtGen/Spine/build_tm04.py                  dựng file prompt (dạng 2 chỉ dựng khi đã chọn concept dạng 1)
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm04_1/luot_1_concept.txt
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm04_2/luot_1_concept.txt

Concept đã chọn của dạng k: inbox/tm04_<k>/tai_ve/L1_duyet.png (người dùng duyệt) hoặc L1_chon.png (Claude chọn ở pha 1).
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm04"
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
INBOX = os.path.join(HERE, "inbox")
SWIRL = os.path.join(ROOT, "Assets", "03 Art", "Fx", "xoay_nuoc.png")


def W(p):
    return os.path.normpath(p)


def pk(k):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return os.path.join(INBOX, f"{CODE}_{k}", "tai_ve")


def chosen(k):
    for n in ("L1_duyet.png", "L1_chon.png"):
        p = os.path.join(save_dir(k), n)
        if os.path.exists(p):
            return p
    return None


def approved(name):
    return os.path.join(INBOX, name, "tai_ve", "L1_lien.png")


LINE = ("LINE AND COLOUR: the hand-drawn look of the style images: drawn by hand on paper with a dark-brown ink pen (#2B2118), "
        "an outline about {n} px thick on this canvas, the same weight on every edge, slightly wobbly like a real pen; every "
        "area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner "
        "than the outline), kept inside the outline. Clean and appealing, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, no shadow under the feet, "
        "nothing on the background), no white highlights or shine spots, no gloss, no glow, no rim light, no gradients, no 3D "
        "look. The only white allowed is one small catchlight dot in each eye and the white foam of the water. A darker tone "
        "appears only where the design itself has a darker colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure. No text, no labels, no frame, no ground line, no puddle, no splash under the feet.")
RIG = ("POSE FOR A 2D BONE RIG (important): all four legs are clearly separated from each other and from the belly, none "
       "crossing another; the far legs show a little behind and between the near legs, not hidden; the tail and its water "
       "spirit stand free from the body with white between them and the back; the mouth is open enough to see inside it.")
WATER = ("THE WATER SPIRIT, in the look of the game's water of image 4: plump rounded water shapes, broad flat bands of three "
         "blues following the flow (deep #2B7FD6, sky #4FB6EE, pale #A6DEF8), round bumpy white foam scallops (#F4FCFF) on "
         "the curl, brown ink outline. It is WATER, not fire: no flame tongues, no flickering points, no glow.")

DESIGN = {
    1: ("THE CREATURE: \"Little River Hippo\", form 1 of 2 of a water-element pet monster: a young, plump, CHIBI WATER HIPPO. "
        "It looks determined and ready to fight (a little warrior), cute but not a smiling mascot and not scary.\n"
        "- BODY: CHIBI and ROUND: a compact ball almost as tall as it is long; the head is BIG, about half of the whole "
        "figure and as big as the body, with a short round body behind it; NOT a long horizontal body like a turtle, a pig "
        "or a dinosaur. EXACTLY FOUR short, thick, stubby legs and four feet in total: the near front and near hind legs in "
        "front (bigger), the far front and far hind legs behind them (smaller, each visible just to the left of its near "
        "leg), never a fifth foot; the legs are clearly visible below the belly (about one sixth of the figure height) and "
        "separated from each other; each foot is round with three small cream toenails.\n"
        "- HEAD: a wide, rounded hippo MUZZLE in front, shaped like a big bean, with two small round nostril bumps on top of "
        "its tip. The MOUTH is open about 30 degrees: we see the rose inside of the mouth and a short pink tongue lying on the "
        "lower jaw; two short stubby cream TUSKS stick UP from the front of the lower jaw, and a few small rounded cream teeth "
        "sit along the jaws. Two big round EYES sit HIGH on top of the head like little domes (hippo style): golden-yellow "
        "irises (#F2C230), a big dark pupil, one small white catchlight dot, and a thick determined frowning brow above each "
        "eye. Two small EARS shaped like little rounded fins stand on top of the head behind the eyes.\n"
        "- BACK FINS: a crest of THREE rounded SAIL FINS runs along the middle of the back from behind the ears to the hips, "
        "the middle one the tallest (about one fifth of the figure's height); each is a soft webbed fin with three or four "
        "dark spines and a scalloped wavy edge, leaning back. Rounded and soft, NOT pointed blades or leaves.\n"
        "- TAIL: a short, thick, tapering tail stub at the rear, visible between the rump and the water; from its tip rises a living WATER SPIRIT: one plump curling "
        "wave crest of water, about half as tall as the head, curling up and forward over itself with a round foam scallop "
        "on the curl, attached to the tail tip.\n"
        "- COLOURS (keep exactly): body SLATE BLUE-GREY (#7A93BE, a greyish blue like a wet river stone, NOT lavender, NOT "
        "purple) on the head, back, sides and legs; muzzle, chin, throat and "
        "belly PALE PEACH (#F6D5C0); a few round pale-blue spots like bubbles (#BFD0EA) scattered on the back and the top of "
        "the head; sail fins and fin-ears SEAFOAM MINT (#86DCC4) with dark teal spines (#2D8C86); inside of the mouth rose "
        "(#C9506A), tongue pink (#EE8C9C); tusks, teeth and toenails cream (#F8EBD0); the water spirit as described below.\n"
        "- NOT a fish, NOT a frog, NOT a whale, NOT a pig: clearly a little hippo with fins."),
    2: ("THE CREATURE: \"River Lord Hippo\", form 2 of 2 (the FINAL form) of the water-element pet monster of image 5: the same "
        "hippo grown into a big, heavy, battle-hardened WAR HIPPO, the lord of the river. It must look clearly STRONGER, "
        "FIERCER and MORE IMPRESSIVE than image 5, and a different silhouette, while you can still tell it is the same line.\n"
        "- PROPORTIONS: NOT chibi at all. Adult hippo proportions: the head is about one third of the figure; a massive barrel "
        "body, broad powerful shoulders and four thick pillar legs with big round feet and cream toenails. A LOW, wide, "
        "forward-leaning CHARGING stance: the shoulders lower than the rump line, the head LOWERED and thrust forward toward "
        "the right at shoulder height (not raised up), front legs braced wide apart with the near front leg stepping "
        "forward.\n"
        "- HEAD: the same broad hippo muzzle and nostril bumps as image 5 but heavier, a strong square lower jaw; the mouth "
        "OPEN about 40 degrees in a battle roar showing the rose inside, the tongue and the teeth; two LONG curved ivory TUSKS "
        "(#F3E6C8) curving up from the lower jaw, each with a bronze ring near its base. Eyes still high on top of the head "
        "but now narrower and fierce: amber irises (#F0A030) with a dark pupil, one small white catchlight dot, heavy angry "
        "brows. Small fin-ears, now dark teal with a notch.\n"
        "- ARMOUR (bronze, moderate, not a full knight suit): a bronze war-helm plate over the forehead and the top of the "
        "muzzle (#C28A3E) with a wave-crest shaped ridge on top and small teal patina inlays (#4FB3A0); a bronze collar "
        "around the neck holding one round cream pearl at the front; a curved bronze plate on the near shoulder.\n"
        "- BACK FINS: a row of FOUR tall SAIL FINS along the back, each shaped like a curling WAVE CREST leaning forward: deep "
        "teal (#1F8A8A) with a few dark spines (#165F63) and a scalloped white foam cap (#F4FCFF) on the curled tip, the "
        "front ones the tallest, sharper and more dramatic than the rounded fins of image 5.\n"
        "- TAIL: a short thick tail stub, visible between the rump and the water, whose tip carries a much BIGGER WATER "
        "SPIRIT: a large twin-crested breaking wave curling forward over the hips, two foam-tipped curls, plus two or three "
        "small loose water drops near it (flat sky blue, NO white shine marks on the drops); white between the tail wave and "
        "the back fins.\n"
        "- COLOURS (keep exactly): body DEEP INDIGO-SLATE (#404C86, a muted greyish indigo like a river at dusk, clearly "
        "blue-grey: NOT a bright royal blue, NOT purple, NOT violet) on the head, back, sides and legs, with a few darker "
        "stripes (#2B3360) like war paint on the shoulders and thighs;muzzle, chin, throat and belly SAND CREAM (#EBD8B2); a few round pale bubble spots (#AEB9DE) "
        "on the back; fins as above; armour bronze with teal patina; inside of the mouth deep rose (#B8405A), tongue "
        "(#E27C92).\n"
        "- LEGS: EXACTLY FOUR legs and four feet, placed like a real four-legged animal seen from the side: the two HIND legs "
        "under the rump at the left (the near hind leg in front, the far hind leg just to its right and partly behind it), "
        "the two FRONT legs under the shoulders (the near front leg in front under the bronze shoulder plate, the far front "
        "leg just to its right and partly behind it); no leg under or in front of the head, never a fifth foot.\n"
        "- Keep from image 5 so the line reads as one family: the bean-shaped hippo muzzle with two nostril bumps, the dome "
        "eyes on top of the head, fin-shaped ears, sail fins along the back, and the wave-crest water spirit on the tail. Do "
        "NOT copy image 5's proportions, colours or pose."),
}

FRAMING = {
    1: ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background. The whole creature is visible, nothing cut by the "
        "edges, at least 90 px of white margin all round; the figure is about 860 px wide and 760 px tall including the fins "
        "and the water spirit, centred.\n"
        "VIEW AND POSE: seen from the side in a slight three-quarter view, the creature faces the viewer's RIGHT. It stands "
        "on all four legs in a sturdy, ready-to-fight stance, the head a little lowered and pushed forward toward the right "
        "as if about to bite."),
    2: ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background. The whole creature is visible, nothing cut by the "
        "edges, at least 70 px of white margin all round; the figure is about 1200 px wide and 820 px tall including the fins "
        "and the water spirit, centred.\n"
        "VIEW AND POSE: seen from the side in a slight three-quarter view from the front-right (both eyes show), the "
        "creature faces the viewer's RIGHT, in the low charging stance described above, roaring mouth wide open."),
}


def refs(k):
    r = [(WORLD_STYLE, "the game's approved hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen "
                       "outline + coloured pencil / wax crayon hatching), nothing of its content",
          "Ảnh mốc nét vẽ đã duyệt (1024 × 1536): bản đồ vẽ tay, viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét")]
    if k == 1:
        r += [(approved("huyen_vu_1"), "an approved four-legged creature of the same game, 1536x1024, white background: match "
                                       "EXACTLY its pen line, crayon texture, flat colouring, level of detail, and its clear "
                                       "four-legged side stance with separated legs. Do NOT copy its species, shell, colours "
                                       "or face",
               "Rùa Ngọc (Huyền Vũ dạng 1) đã duyệt (1536 × 1024, nền trắng): rùa xanh lá chibi bốn chân tách rời, quay phải. "
               "Lấy nét, vân sáp, dáng bốn chân; không chép loài, mai, màu"),
              (approved("canh_cut_1"), "another approved chibi creature of the same game, 1536x1024, white background: match "
                                       "its chibi proportions, its determined frowning eyes and its flat crayon colouring. "
                                       "Do NOT copy its species, colours, crest or pan",
               "Cánh Cụt Con đã duyệt (1536 × 1024, nền trắng): chim cánh cụt chibi cầm chảo, mắt cau quả quyết. Lấy tỉ lệ chibi, "
               "mắt, cách tô; không chép loài, màu"),
              (SWIRL, "the game's approved swirling water (384x362): the look of the game's water and its curled wave crests, "
                      "for the water spirit on the tail",
               "Vòng nước xoáy đã duyệt của game (384 × 362, nền trong): mào sóng cuộn, ba màu lam phẳng, bọt trắng. Mẫu cho "
               "linh hồn nước ở đuôi")]
    else:
        r += [(approved("vay_lam_3"), "an approved FINAL-form creature of the same game, 1536x1024, white background: match "
                                      "its pen line and flat crayon colouring, and its fierce, adult, battle-ready attitude and "
                                      "low four-legged stance. Do NOT copy its species, its shark fins, its white stripes, "
                                      "its scar, its colours or its face",
               "Cá Mập Vây Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): cá mập bốn chân dữ, thế lao. Lấy nét, vẻ dữ, thế đứng; "
               "không chép loài, màu"),
              (approved("ma_ket_3"), "another approved FINAL-form creature of the same game, 1536x1024, white background: "
                                     "the level of armour and ornament allowed (moderate metal pieces with simple patterns) and "
                                     "how armour is drawn in flat crayon colour. Do NOT copy its species, horns or colours",
               "Ma Kết Thánh Giáp dạng 3 đã duyệt (1536 × 1024, nền trắng): dê giáp vàng. Lấy mức giáp, cách vẽ giáp tô phẳng; "
               "không chép loài, sừng, màu"),
              (SWIRL, "the game's approved swirling water (384x362): the look of the game's water and its curled wave crests, "
                      "for the water spirit on the tail",
               "Vòng nước xoáy đã duyệt của game (384 × 362, nền trong): mào sóng cuộn. Mẫu cho linh hồn nước ở đuôi"),
              (chosen(1), "FORM 1 of THIS creature (its chosen concept), 1536x1024: the earlier, chibi form. The new picture is "
                          "the same line grown up: keep its family features (named below) and its line and crayon texture, "
                          "change everything else as described",
               "Concept dạng 1 đã chọn (1536 × 1024, nền trắng): Hà Mã Con chibi xanh xám, vây bạc hà, đuôi sóng nước")]
    return r


def check(rs):
    missing = [W(p) for p, _, _ in rs if not p or not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))


def build_one(k):
    rs = refs(k)
    check(rs)
    os.makedirs(pk(k), exist_ok=True)
    os.makedirs(save_dir(k), exist_ok=True)
    out = os.path.join(save_dir(k), "L1_concept.png")
    p = os.path.join(pk(k), "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(q)}: {en}" for i, (q, en, _) in enumerate(rs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not "
          "edit, move or delete any other file.", "",
          "TASK: design and draw ONE creature as ONE full picture, in the hand-drawn style of the style images. Every design "
          "detail below is required; the reference creatures give only the drawing style and attitude, never their design.", "",
          DESIGN[k], "", WATER, "", FRAMING[k], "", RIG, "", LINE.format(n=6), FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return p, out, rs


# ---------------------------------------------------------------- lượt 2: tờ mảnh (cách lai, đặc tả mục 5)
# Thân, đầu trên, vây, đuôi sóng, chân gần, giáp, hàm dưới cắt thẳng từ concept (tm04.py). GPT chỉ vẽ phần bị che hoặc không có
# trên concept: mảng lòng miệng (lộ thêm khi há to), mí nhắm hai mắt, hai chân phía xa vẽ trọn (concept chỉ lộ bàn chân).
PIECES = ("THIS IS A SHEET OF SEPARATE PARTS for a 2D cut-out animation rig, NOT a scene: every part is drawn COMPLETE and on "
          "its own (also the areas that are hidden in the concept), flat on the white page like stickers laid out on a table, "
          "with at least 70 px of pure white between any two parts and between a part and the image edge. No part touches or "
          "overlaps another. Every part keeps exactly the colours, markings, outline weight and crayon texture of the approved "
          "concept (image 1), with the SAME SILHOUETTE AND PROPORTIONS as the matching part in image 1, at the same scale as "
          "image 1. Do not draw a whole creature, do not draw extra parts, do not draw labels, numbers, arrows or guide lines.")
SHEET = {
    2: ("M01", "mouth, eyelids, far legs",
        "Canvas 1536 x 1024. Lay the parts out in a 3 x 2 grid of 512 px cells, one part centred in each cell:\n"
        "- top-left cell: a MOUTH INTERIOR patch: one soft rounded blob of flat deep rose (#B8405A) with a darker rose throat "
        "spot (#8E2F48) in the middle-left, brown ink outline, about 300 px wide and 220 px tall (bigger than the inside of the "
        "mouth seen in image 1, because the jaw opens wider in the animation). No teeth, no tongue, no lips.\n"
        "- top-middle cell: the NEAR CLOSED EYELID: covers the big near (left) eye of image 1 completely when the eye shuts: "
        "an almond patch of the head's indigo-slate skin (#404C86, crayon hatching), about 110 px wide and 80 px tall, the "
        "heavy angry brow along its top edge like in image 1, and ONE thick dark-brown curved line across its lower half "
        "(the shut eye, a fierce squint), brown ink outline all round. Nothing else.\n"
        "- top-right cell: the FAR CLOSED EYELID: the same design for the smaller far (right) eye, about 80 px wide and 65 px "
        "tall.\n"
        "- bottom-left cell: the FAR FRONT LEG drawn COMPLETE and STANDING upright, from the rounded shoulder top down to the "
        "foot: the same thick pillar leg as the near front leg of image 1 (indigo-slate #404C86 with two dark war-paint "
        "stripes #2B3360, a round foot with four cream toenails #F3E6C8 along its front-bottom edge, flat sole), facing "
        "right; the top end is a smooth rounded stump (it plugs in behind the body). About 260 px wide and 400 px tall. NO "
        "shoulder plate.\n"
        "- bottom-middle cell: the FAR HIND LEG drawn COMPLETE and STANDING upright, from the rounded hip top down to the "
        "foot: the same heavy thigh and leg as the near hind leg of image 1 (indigo-slate with dark stripes, a round foot "
        "with four cream toenails), facing right; the top end is a smooth rounded stump. About 280 px wide and 400 px tall.\n"
        "- bottom-right cell: leave EMPTY (pure white).",
        "mảng lòng miệng to (300 × 220), mí nhắm mắt gần (110 × 80), mí nhắm mắt xa (80 × 65), chân trước xa vẽ trọn (260 × "
        "400), chân sau xa vẽ trọn (280 × 400), ô cuối để trống"),
    1: ("M01", "mouth, eyelids, far legs",
        "Canvas 1536 x 1024. Lay the parts out in a 3 x 2 grid of 512 px cells, one part centred in each cell:\n"
        "- top-left cell: a MOUTH INTERIOR patch: one soft rounded blob of flat rose (#C9506A) with a darker rose throat spot "
        "(#9A3550) in the middle-left, brown ink outline, about 220 px wide and 150 px tall (bigger than the inside of the "
        "mouth seen in image 1, because the jaw opens wider in the animation). No teeth, no tongue, no lips.\n"
        "- top-middle cell: the NEAR CLOSED EYELID: covers the big round near (left) eye of image 1 completely when the eye "
        "shuts: a round patch of the head's slate blue-grey skin (#7A93BE, crayon hatching), about 110 px wide and 105 px "
        "tall, the thick dark frowning brow along its top edge like in image 1, and ONE thick dark-brown curved line across "
        "its lower half (the shut eye, a determined squint), brown ink outline all round. Nothing else.\n"
        "- top-right cell: the FAR CLOSED EYELID: the same design for the smaller far (right) eye, about 70 px wide and 85 px "
        "tall.\n"
        "- bottom-left cell: the FAR FRONT LEG drawn COMPLETE and STANDING upright: the same short stubby leg as the near "
        "front leg of image 1 (slate blue-grey #7A93BE, a round foot with three small cream toenails #F8EBD0, flat sole), "
        "facing right, but drawn longer at the top (the upper part hides under the belly): a smooth rounded top stump. About "
        "120 px wide and 170 px tall.\n"
        "- bottom-middle cell: the FAR HIND LEG drawn COMPLETE and STANDING upright, the same design as the near hind leg of "
        "image 1, rounded top stump, about 120 px wide and 170 px tall.\n"
        "- bottom-right cell: leave EMPTY (pure white).",
        "mảng lòng miệng (220 × 150), mí nhắm mắt gần (110 × 105), mí nhắm mắt xa (70 × 85), chân trước xa vẽ trọn (120 × "
        "170), chân sau xa vẽ trọn (120 × 170), ô cuối để trống"),
}
HAI_LONG_M01 = os.path.join(INBOX, "hai_long", "tai_ve", "M01.png")


def build_sheet(k):
    cpt = os.path.join(save_dir(k), "L1_duyet.png")
    if not os.path.exists(cpt):
        return None
    rs = [(cpt, f"the APPROVED CONCEPT of this creature (form {k}), 1536x1024: every part you draw belongs to THIS creature: "
                "same species, same colours, same markings, same line and crayon texture, same proportions and scale. Use it "
                "only to know what each part looks like; do not redraw the whole creature",
           f"Concept dạng {k} đã duyệt (1536 × 1024, nền trắng)"),
          (HAI_LONG_M01, "an approved PARTS SHEET of another creature of the same game, 1536x1024: shows how a sheet of separate "
                         "parts is laid out (parts complete, apart on white). Copy only that layout idea, nothing of its content",
           "Tờ mảnh đầu Hải Long đã duyệt (1536 × 1024, nền trắng): chỉ để GPT hiểu cách bày tờ mảnh"),
          (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style, nothing of its content",
           "Ảnh mốc nét vẽ (1024 × 1536): bản đồ vẽ tay; chỉ lấy nét")]
    check(rs)
    sc, title, en, vi = SHEET[k]
    p = os.path.join(pk(k), "luot_2_manh.txt")
    sd = save_dir(k)
    t = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image and save "
         "it as the step says. Do not reply with text only.", "",
         "REFERENCE IMAGES (open each file from its full path):"]
    t += [f"image {i} = {W(q)}: {e}" for i, (q, e, _) in enumerate(rs, 1)]
    t += ["", f"WHAT THIS IS: a sheet of separate, complete parts of the hippo creature of image 1, for a 2D cut-out animation "
          "rig. The animation software opens the jaw wider, shuts the eyes and moves the legs, so these parts (hidden or only "
          "partly visible in image 1) must be drawn whole, clean, and well separated.", "",
          f"SAVE: the image goes into {W(sd)} under the step's name ({sc}.png). If that file already exists, add _2, _3 ... "
          "before .png. Do not change, move or delete any other file.", "",
          f"=== STEP {sc} ({title}) ===", PIECES, en, "", LINE.format(n=6),
          FLAT.replace(" and the white foam of the water", ""), BG,
          f"SAVE this step: save it as a PNG to {W(os.path.join(sd, sc + '.png'))} (create the folder if it is missing; if that "
          f"file already exists, save it as {sc}_2.png, {sc}_3.png ... in the same folder instead). Do not change, move or "
          "delete any other file.", ""]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    return p, rs, sc, vi


CHECK = {
    1: ["Hà mã con chibi tròn như quả bóng (đầu khoảng nửa hình, rộng ≈ cao), **quay sang phải**, **đúng bốn chân** (đếm "
        "bàn chân: 4) ngắn, tách rời nhau, không chéo.",
        "Thân xanh xám đá `#7A93BE`, mõm/cằm/bụng hồng đào nhạt, vài đốm bọt xanh nhạt trên lưng.",
        "Ba vây buồm tròn màu bạc hà có gai sẫm dọc lưng (không phải hai lá nhọn vàng), tai hình vây nhỏ.",
        "Mõm hà mã hình hạt đậu có hai lỗ mũi, miệng hé thấy lòng miệng hồng và lưỡi, hai nanh cụt nhô lên từ hàm dưới.",
        "Hai mắt tròn nằm cao trên đỉnh đầu, tròng vàng, mày cau quả quyết (không cười kiểu linh vật).",
        "Đuôi ngắn, chóp là một mào sóng nước cuộn có bọt trắng (không phải ngọn lửa), đứng tách khỏi lưng.",
        "Tô phẳng, không bóng (kể cả dưới chân), không điểm sáng (trừ chấm mắt), nền trắng tinh, không đường đất."],
    2: ["Hà mã trưởng thành to, nặng, **không chibi** (đầu khoảng 1/3 hình), thế lao thấp, quay sang phải.",
        "Thân chàm xám đậm `#404C86` (không tím, không lam tươi của Vây Lam) có vằn sẫm, mõm/bụng kem cát; nhìn bóng dáng đã "
        "thấy khác dạng 1.",
        "Đúng bốn chân đặt như thú bốn chân: hai chân sau dưới mông (bên trái), hai chân trước dưới vai; không chân nào mọc "
        "dưới đầu.",
        "Giáp đồng vừa phải: tấm che trán có gờ hình mào sóng, vòng cổ có ngọc, giáp vai; ngà dài cong có khâu đồng.",
        "Bốn vây buồm cao hình mào sóng cuộn, xanh két sẫm, mũ bọt trắng; đuôi mang con sóng hai mào to.",
        "Mắt hẹp, dữ, tròng hổ phách; miệng há gầm thấy lòng miệng, răng.",
        "Còn nhận ra cùng dòng: mõm hạt đậu hai lỗ mũi, mắt trên đỉnh đầu, tai vây, vây buồm lưng, đuôi sóng.",
        "Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh."],
}

FIX = [("Có bóng, mảng sáng tối, bóng dưới chân",
        "Flat colour only: remove every shadow (also under the feet), highlight and gradient; keep the crayon hatching as texture."),
       ("Quay sang trái", "The creature must face the viewer's RIGHT: muzzle and eyes toward the right edge."),
       ("Đuôi thành ngọn lửa", "The tail spirit is WATER: one plump curling wave crest with round white foam, no flame shapes."),
       ("Chân dính nhau, chéo nhau", "All four legs clearly separated, none crossing; the far legs visible between the near legs."),
       ("Dạng 1 cười kiểu linh vật", "Determined, ready-to-fight face with frowning brows, mouth open but not smiling."),
       ("Dạng 2 vẫn chibi", "Not chibi at all: adult heavy war hippo, head about one third of the figure, thick pillar legs.")]


def guide(made, sheets=None):
    sheets = sheets or {}
    gd = [f"# Gói gửi GPT: dòng tm04 (đề xuất tên **Hà Bá**, hà mã nước)", "",
          "Lô 10 tướng mới đảo Thủy, dòng 4 (thay suất ải 15, Mi Nhi). Hai dạng: **Hà Mã Con** (chibi) → **Hà Bá** (dạng cuối, "
          "chiến mã hà mã giáp đồng). Mỗi dạng một file prompt, gen dạng 1 trước; file dạng 2 chỉ có sau khi đã chọn concept "
          "dạng 1 (`inbox/tm04_1/tai_ve/L1_chon.png` hoặc `L1_duyet.png`).", "",
          "Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm04_<k>/luot_1_concept.txt` (thêm `--note \"...\"` "
          "để sửa nhanh). Người dùng tự gửi thì **chỉ gửi GPT đường dẫn file prompt**, GPT tự mở ảnh mẫu và tự lưu.", ""]
    for k, (p, out, rs) in made.items():
        gd += [f"## Dạng {k}", "", f"**File prompt:** `{W(p)}`", "", f"**GPT lưu ảnh vào:** `{W(out)}` (trùng tên thì `_2`, `_3`…)", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{W(q)}` | {vi} |" for i, (q, _, vi) in enumerate(rs, 1)]
        gd += ["", "**Kiểm:**", ""] + [f"- {c}" for c in CHECK[k]] + [""]
    if 2 not in made:
        gd += ["## Dạng 2", "", "Chưa dựng: cần concept dạng 1 đã chọn. Chạy lại `py -3 -I ArtGen/Spine/build_tm04.py` sau khi chép "
               "ảnh dạng 1 đã chọn thành `inbox/tm04_1/tai_ve/L1_chon.png`.", ""]
    for k, s in sheets.items():
        p, rs, sc, vi = s
        gd += [f"## Lượt 2, dạng {k}: tờ mảnh (cách lai)", "",
               "Thân, đầu trên, vây, đuôi sóng, chân gần, giáp, hàm dưới cắt thẳng từ concept đã duyệt (`ArtGen/Spine/tm04.py`). "
               "GPT chỉ vẽ phần bị che hoặc không có trên concept.", "",
               f"**File prompt:** `{W(p)}`; GPT lưu `{W(os.path.join(save_dir(k), sc + '.png'))}`.", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm04_{k}/luot_2_manh.txt`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{W(q)}` | {v} |" for i, (q, _, v) in enumerate(rs, 1)]
        gd += ["", f"**Kiểm {sc}:** {vi}; mỗi mảnh rời nhau ít nhất 70 px, nền trắng, đúng màu concept, chân đứng thẳng có đầu "
               "trên tròn, mí che kín mắt.", ""]
    gd += ["## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    for k in made:
        open(os.path.join(pk(k), "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")


def build():
    made = {1: build_one(1)}
    if chosen(1):
        made[2] = build_one(2)
    sheets = {k: s for k in (1, 2) for s in [build_sheet(k)] if s}
    guide(made, sheets)
    for k, (p, _, _) in made.items():
        print(W(p))
    for k, s in sheets.items():
        print(W(s[0]))
    if 2 not in made:
        print("(chưa dựng dạng 2: chưa có concept dạng 1 đã chọn)")


if __name__ == "__main__":
    build()
