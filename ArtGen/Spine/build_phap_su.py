"""Gói GPT vẽ concept dòng pháp sư nước bí ẩn (tướng thứ 6 đảo Thủy, 2026-11-11, người dùng lên ý tưởng). Mã làm việc: phap_su.

Ý người dùng: pháp sư nước bí ẩn, không thấy mặt (mũ che kín mặt). Idle, die làm giống con gốc, sửa đi chút. Đòn thường như
skill_01 của con gốc: chĩa gậy bắn tia nước; chiêu mana dùng lại động tác đó, đổi kiểu tia. Chiêu cuối như skill_02: giơ gậy
triệu hồi các mũi kim nước, dậm gậy xuống thì kim bắn vào đối thủ. Ra sân: một vòng tròn triệu hồi hiện ra rồi tướng trồi lên.
Dạng 2 cao lớn hơn. Cái khó: rig kỹ quần áo, áo choàng. Rig và nhịp học từ một con pháp sư của game tham khảo (ghi chú:
inbox/phap_su_ghichu.md). Không đính ảnh con gốc vào prompt; hình là thiết kế riêng, nét của dự án (bút mực nâu + chì sáp, tô
phẳng). Màu và chi tiết là đề xuất của Claude (người dùng chỉ dặn ý tưởng), chờ duyệt.

  dạng 1  pháp sư lùn chibi: mũ chóp chàm to sụp kín mặt (dưới vành chỉ một khoảng tối), áo dài chuông lam ngọc, khăn vai và vạt
          trước lam băng, áo choàng chàm sau lưng viền lượn sóng, gậy gỗ lũa đầu móc hình ngọn sóng ôm một quả cầu nước
  dạng 2  cùng bộ đồ, cao lớn hẳn (mũ còn 1/3 chiều cao), áo choàng to gấu bốn lượn viền cam, gậy cao có thêm cầu nhỏ

Lượt 1 mỗi dạng: concept trọn con một ảnh. Dạng 2 chỉ dựng khi đã có inbox/phap_su_1/tai_ve/L1_duyet.png.
Lượt 2 (vòng tròn triệu hồi, phần khuất nếu cần) viết sau khi duyệt concept.

    py -3 -I ArtGen/Spine/build_phap_su.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/phap_su_1/luot_1_concept.txt [--note "..."]
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/phap_su_2/luot_1_concept.txt [--note "..."]
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "phap_su"
WORLD_STYLE = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
DROP = os.path.join(HERE, "inbox", "ti_tach_1", "tai_ve", "L1_duyet.png")     # tướng khởi đầu Thủy đã duyệt: độ đơn giản, nét rung
FISH = os.path.join(HERE, "inbox", "ca_den_1", "tai_ve", "L1_duyet.png")      # tướng thứ 3 đảo Thủy đã duyệt: tô phẳng, vân sáp


def W(p):
    return os.path.normpath(p)


def pk(k):
    return os.path.join(HERE, "gui_gpt", f"{CODE}_{k}")


def save_dir(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve")


def chosen(k):
    return os.path.join(save_dir(k), "L1_duyet.png")


# ---------------------------------------------------------------- thiết kế (tiếng Anh, dán vào prompt)
PALETTE1 = ("COLOURS (use exactly these, each area one flat colour): hat and back cloak deep indigo (#2A3580); robe and "
            "sleeves sea teal (#2F9FB3); shoulder capelet, sleeve cuffs, front panel and hat band pale ice blue (#DDF0F7, "
            "never left as bare white paper); the dark opening under the hat, the mitten hand and the boot tips night navy "
            "(#151A33); the bead on the hat tip, the gem on the hat band and the two charms on the staff coral orange "
            "(#F2845C); the staff driftwood grey-brown (#9A7B63); the water orb on the staff light aqua (#86D6F0); the "
            "small drop emblem on the front panel sea teal (#2F9FB3); every outline dark-brown ink (#2B2118).")

FORM1 = ("CREATURE: a small MYSTERIOUS WATER MAGE for a monster-collecting game: a short, squat little being completely "
         "wrapped in a huge hat and robes, so that NO face and NO skin can be seen at all. It is a pet-sized creature, not a "
         "human: nobody knows what is inside the clothes. Quiet, confident, a little eerie, standing ready with its staff: "
         "not a cheerful mascot and not scary.\n"
         "FORM 1, the first and smallest form (chibi proportions: the hat is almost half of the whole height). Read it from "
         "top to bottom:\n"
         "- HAT (deep indigo), the biggest part of the figure: a soft, heavy, pointed wizard hat. Its CONE is wide at the "
         "bottom (about 300 px) and rises about 300 px; near the top it folds over and its last third droops BACK toward "
         "the viewer's LEFT, ending in one round coral-orange BEAD (about 45 px). Its BRIM is wide (about 460 px from side "
         "to side), thick and floppy, with a gently wavy edge, and it is pulled down low: the front of the brim dips over "
         "where the face would be. Around the base of the cone runs a pale ice-blue HAT BAND (about 40 px tall) with one "
         "coral-orange teardrop GEM at its front (on the viewer's right side of the band). The two loose ends of the band "
         "hang down behind the hat on the viewer's LEFT as two short ribbon tails (each about 110 px long and 30 px wide, "
         "with a notched end).\n"
         "- THE FACE IS HIDDEN: under the front of the brim there is only a dark OPENING: one flat night-navy shape (about "
         "150 px wide and 70 px tall) between the brim above and the capelet below. Inside it: NOTHING. No eyes, no glowing "
         "dots, no mouth, no nose, no skin, no hair. Just the flat dark shape.\n"
         "- SHOULDER CAPELET (pale ice blue): a short round collar-cape lying over both shoulders like a small poncho, "
         "about 270 px wide and 90 px tall, its lower edge cut into five soft rounded scallops like little waves. It hides "
         "the neck and the shoulders completely; both sleeves come out from under it.\n"
         "- ROBE (sea teal): one simple bell-shaped robe from under the capelet down to the ground, about 230 px wide at "
         "the chest and widening to about 340 px at the hem; the hem is a soft wavy line just above the ground. No legs "
         "are visible: only the two small rounded night-navy BOOT TIPS (each about 60 px wide and 30 px tall) peek out "
         "from under the hem, side by side, pointing to the viewer's right.\n"
         "- FRONT PANEL (pale ice blue): one long narrow cloth panel hanging from under the capelet straight down the "
         "front of the robe, about 100 px wide and 230 px long, ending in a pointed tip about 70 px above the hem. In its "
         "middle one simple sea-teal WATER-DROP emblem (about 50 px). It lies on the robe a little toward the viewer's "
         "right of the body's centre (the body is turned three-quarters to the right).\n"
         "- BACK CLOAK (deep indigo): a cloak hanging from under the capelet down the BACK of the figure. Because the mage "
         "faces right, the cloak is seen on the viewer's LEFT side, behind the robe: one big simple shape about 170 px "
         "wide sticking out to the left of the robe, falling from shoulder height to about 30 px above the ground, flaring "
         "out a little toward the bottom; its lower hem is cut into three big rounded wave scallops. The robe is in front "
         "of it.\n"
         "- ARM ON THE VIEWER'S LEFT (the far, resting arm): a wide bell SLEEVE (sea teal, with a pale ice-blue CUFF band "
         "about 35 px wide at its opening) comes out from under the capelet and hangs down and slightly outward to the "
         "left, in front of the cloak, about 190 px long, its opening pointing down. NO hand is visible: the sleeve "
         "opening is just a small flat night-navy oval.\n"
         "- ARM ON THE VIEWER'S RIGHT (the staff arm): the same wide bell sleeve with the pale cuff comes out from under "
         "the capelet and reaches out to the RIGHT, slightly raised, about 180 px long. From its cuff comes ONE small "
         "round night-navy MITTEN hand (a simple ball about 55 px, thumb on top, no separate fingers) gripping the staff.\n"
         "- STAFF (driftwood grey-brown), held upright in the mitten, standing on the ground to the RIGHT of the figure: a "
         "slightly crooked wooden pole about 30 px thick, from the ground up to a little above the top of the hat cone "
         "(about 760 px long). Its HEAD curls forward (to the viewer's right) and around into an open hook shaped like a "
         "curling WAVE CREST, about 170 px across. Inside the hook sits one round WATER ORB (light aqua, about 100 px, a "
         "plain flat ball with a clear ink outline and one short curved ink line inside as a ripple; not glowing). From "
         "the neck of the staff, just under the hook, hang two short cords (about 70 px), each with one small "
         "coral-orange shell-shaped CHARM at its end.")

FRAME1 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
          "visible, nothing cut by the edges. The whole figure with its staff is about 720 px wide and about 800 px tall "
          "(from the top of the staff head to the boot tips), centred horizontally; the boot tips and the foot of the staff "
          "stand at the same level, about 90 px above the bottom edge of the image.")

PALETTE2 = ("COLOURS (exactly the colours of image 1, each area one flat colour): hat and back cloak deep indigo (#2A3580); "
            "robe and sleeves sea teal (#2F9FB3); shoulder capelet, sleeve cuffs, front panel and hat band pale ice blue "
            "(#DDF0F7, never left as bare white paper); the dark opening under the hat, the mitten hand and the boot tips "
            "night navy (#151A33); the bead on the hat tip, the gem on the hat band, the trim line on the cloak and the "
            "charms on the staff coral orange (#F2845C); the staff driftwood grey-brown (#9A7B63); the water orbs light aqua "
            "(#86D6F0); every outline dark-brown ink (#2B2118).")

FORM2 = ("CREATURE: the GROWN FORM of the mysterious water mage of image 1 (form 1, approved): the same being, the same "
         "clothes, the same colours and the same drawing style, but clearly TALLER, BIGGER and more imposing: a grown "
         "archmage instead of a squat little apprentice. Still NO face and NO skin visible at all; still a creature wrapped "
         "in clothes, not a human. Calm, confident and a little eerie, not scary.\n"
         "FORM 2 (what changes compared with image 1; everything not listed stays as in image 1):\n"
         "- PROPORTIONS: tall and slender instead of chibi. The hat is now only about ONE THIRD of the figure's height (in "
         "image 1 it was almost half); the robe below the capelet is about twice as long as in image 1. The whole figure "
         "without the staff is about 880 px tall.\n"
         "- HAT (deep indigo): the same soft pointed hat with the pale band, the coral teardrop gem and the two ribbon "
         "tails, the same low brim hiding the face; the cone is a little taller and its drooping tip is LONGER, hanging "
         "further back to the viewer's left, still ending in the coral bead. The two ribbon tails are longer (about 170 "
         "px). Under the front of the brim the same flat night-navy OPENING with nothing inside: no eyes, no glowing dots.\n"
         "- SHOULDER CAPELET (pale ice blue): the same scalloped collar-cape, a little wider, now with a short standing "
         "COLLAR rising about 50 px behind the dark opening.\n"
         "- ROBE (sea teal): the same bell-shaped robe, now LONG: narrow at the chest (about 220 px), falling straight "
         "and flaring only near the ground to about 360 px at the wavy hem; one pale ice-blue band (about 30 px) runs "
         "around the robe just above the hem. Two night-navy boot tips peek out under the hem, pointing right.\n"
         "- FRONT PANEL (pale ice blue): the same narrow panel with the sea-teal water-drop emblem, now about 380 px "
         "long, ending in a pointed tip about 90 px above the hem.\n"
         "- BACK CLOAK (deep indigo): bigger and longer: seen on the viewer's LEFT behind the robe, about 230 px wide, "
         "falling from the shoulders to about 30 px above the ground, flaring out toward the bottom; its lower hem is cut "
         "into FOUR big rounded wave scallops, and one thin coral-orange trim line (about 10 px) follows the hem.\n"
         "- ARM ON THE VIEWER'S LEFT (resting): the same wide bell sleeve with the pale cuff, longer (about 260 px), "
         "hanging down and slightly outward in front of the cloak; no hand visible, the opening a flat night-navy oval.\n"
         "- ARM ON THE VIEWER'S RIGHT (staff arm): the same sleeve reaching out to the right, slightly raised, about "
         "220 px long, one round night-navy mitten gripping the staff.\n"
         "- STAFF (driftwood grey-brown): taller and grander than in image 1: an upright crooked pole about 34 px thick "
         "and about 940 px long, standing on the ground to the RIGHT of the figure, its head a little higher than the top "
         "of the hat cone. The head curls forward into the same open WAVE-CREST hook, now about 220 px across, holding "
         "one big round WATER ORB (light aqua, about 140 px, a plain flat ball with one short curved ink ripple line; "
         "not glowing). A second, small water orb (about 55 px) sits on the very tip of the hook. From the neck of the "
         "staff hang THREE short cords with coral-orange shell charms.")

FRAME2 = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. Everything is "
          "visible, nothing cut by the edges. The whole figure with its staff is about 760 px wide and about 950 px tall "
          "(from the top of the staff head to the boot tips), centred horizontally; the boot tips and the foot of the staff "
          "stand at the same level, about 35 px above the bottom edge of the image; the top of the staff is about 35 px "
          "below the top edge.")

POSE = ("VIEW AND POSE (very important: the picture will be cut into separate parts and animated with a 2D skeleton): "
        "three-quarter view, the mage faces the viewer's RIGHT, standing still and upright, calm, the staff planted "
        "vertically on the ground on the right. Keep these parts clear of each other:\n"
        "- the STAFF stands completely free: at least 45 px of pure white between the pole and the robe all the way down, "
        "and between the staff head (hook, orb, charms) and the hat brim; the staff touches only the mitten hand. The hat "
        "brim does not reach the staff;\n"
        "- the drooping HAT TIP with its bead and the two ribbon tails touch nothing; they hang in the white on the left;\n"
        "- the STAFF ARM is held away from the body: white paper is visible between the underside of that sleeve and the "
        "robe;\n"
        "- the RESTING SLEEVE on the left overlaps only the cloak behind it, with a clear ink outline all around it;\n"
        "- every piece of clothing (hat, band, capelet, sleeves, cuffs, front panel, robe, cloak) has its own closed ink "
        "outline where it lies on another piece.\n"
        "No water, no bubbles, no sparkles, no magic circle, no splashes, no effects anywhere.")

SOFT = ("HAND-DRAWN, NOT A LOGO: organic, slightly irregular hand-drawn curves, a little lopsided, soft heavy cloth with "
        "only two or three simple fold lines per piece; the ink line is visibly wobbly and uneven in thickness like a real "
        "pen, not a vector stroke; loose crayon hatching is clearly visible inside every area, also inside the dark "
        "indigo and night-navy areas (darker crayon strokes on the dark colour).")

LINE = ("LINE AND COLOUR: the game's hand-drawn look of the approved hero images: drawn by hand on paper with a dark-brown "
        "ink pen (#2B2118), an outline about 7 px thick on this canvas, the same weight on every edge, a closed outline "
        "around every part; fold lines and inner lines thinner (about 4 px); every area coloured with coloured pencils and "
        "wax crayons, the strokes visible as loose diagonal hatching (strokes thinner than the outline), kept inside the "
        "outline. Clean and appealing, few details, neither a crude scribble nor overly detailed.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour; the pencil and crayon strokes are texture only, they "
        "do not model light. No shading, no darker side, no shadows of any kind (no cast shadow, no shadow under the figure "
        "or under the hat brim, on the ground or on the background), no white highlights or shine spots (also none on the "
        "water orb, the bead and the gem), no gloss, no wet look, no reflections, no glow, no rim light, no gradients, no "
        "transparency, no 3D look. The dark opening under the hat is a flat colour area of the design, not a shadow. A "
        "different tone appears only where the design itself lists a different colour.")
BG = ("Plain pure-white background (#FFFFFF): no paper colour or paper grain outside the drawing, no white border or sticker "
      "outline around the figure (the game adds that itself). No text, no labels, no frame, no props, no effects around "
      "the creature.")


def refs_of(k):
    style = [
        (DROP, "an approved hero of the same game (a water-blob creature), 1536x1024, white background: match EXACTLY its "
               "wobbly pen line, its visible crayon hatching and its completely flat colouring. Do NOT copy its species, "
               "design, face or colours.",
         "Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): giọt nước lam mắt bầu dục. Chỉ lấy nét bút rung, vân sáp, tô phẳng"),
        (FISH, "another approved hero of the same game (a lantern-fish creature), 1536x1024, white background: see how few "
               "details, flat crayon colour and dark areas with visible hatching are drawn in this style. Do NOT copy its "
               "species, design or colours.",
         "Cá đèn lồng dạng 1 đã duyệt (1536 × 1024, nền trắng): cá hai chân màu chàm. Lấy độ ít chi tiết, mảng màu đậm vẫn có vân sáp"),
        (WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + "
                      "coloured pencil / wax crayon hatching), nothing of its content.",
         "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp"),
    ]
    if k == 1:
        return style
    return [(chosen(1), "FORM 1 of THIS creature (approved), 1536x1024, white background: keep its clothes, its colours, its "
                        "hidden face (a flat dark opening under the hat brim), its pose facing right with the staff planted "
                        "on the right and the cloak on the left, its view and its drawing style. Form 2 is the same mage "
                        "grown tall. Do NOT copy its squat chibi proportions.",
             "Pháp sư nước dạng 1 đã duyệt (1536 × 1024, nền trắng): pháp sư lùn mũ chàm sụp kín mặt, áo lam ngọc, gậy ôm cầu nước")
            ] + style


FORMS = {1: ("pháp sư nước dạng 1", FORM1, PALETTE1, FRAME1), 2: ("pháp sư nước dạng 2", FORM2, PALETTE2, FRAME2)}

CHECK = {
    1: ["Pháp sư lùn quay về bên **phải**, đứng thẳng; **không thấy mặt**: dưới vành mũ chỉ một khoảng tối phẳng, không mắt, không chấm sáng.",
        "**Mũ chóp chàm** to gần nửa chiều cao, chóp gập ngả về **trái** có hạt cam ở đầu; đai mũ lam băng có viên đá cam; hai dải đai buông sau mũ.",
        "**Khăn vai** lam băng viền lượn sóng che hết cổ vai; **áo dài chuông** lam ngọc chấm đất, chỉ ló hai mũi giày tối; **vạt trước** lam băng có hình giọt nước.",
        "**Áo choàng chàm** sau lưng lộ ở bên trái, gấu ba lượn sóng; tay áo trái buông, không thấy bàn tay.",
        "**Gậy gỗ** dựng bên phải, cao hơn chóp mũ, đầu gậy móc hình ngọn sóng ôm **quả cầu nước**, hai dây treo hạt cam; chỉ bàn tay tối chạm gậy.",
        "Gậy **tách hẳn** khỏi áo và vành mũ (khe trắng ≥ 45 px); tay cầm gậy hở khỏi thân; chóp mũ và dải đai không chạm gì.",
        "Tô phẳng: **không** bóng (kể cả dưới vành mũ), không điểm sáng, cầu nước không phát sáng; viền mực nâu; nền trắng tinh; không hiệu ứng."],
    2: ["Cùng con, cùng bộ đồ, cùng màu với dạng 1 nhưng **cao lớn hẳn**: mũ chỉ còn chừng 1/3 chiều cao, áo dài gấp đôi; vẫn **không thấy mặt**.",
        "Chóp mũ và hai dải đai dài hơn; khăn vai có **cổ dựng** thấp; áo có một dải lam băng gần gấu; vạt trước dài.",
        "Áo choàng chàm **to dài hơn**, gấu bốn lượn sóng, có đường viền cam; tay áo trái buông dài, không thấy bàn tay.",
        "Gậy **cao hơn chóp mũ**, móc ngọn sóng to ôm cầu nước lớn, thêm **một cầu nhỏ** ở đầu móc, ba hạt vỏ sò treo.",
        "Gậy tách hẳn khỏi áo và vành mũ (khe trắng ≥ 45 px); tay cầm gậy hở khỏi thân; chóp mũ, dải đai không chạm gì.",
        "Tô phẳng, không bóng, không phát sáng; nền trắng tinh; không hiệu ứng; không bị cắt mép ảnh."],
}

FIX = [("Có bóng, mảng sáng tối, điểm sáng trên cầu nước", "Flat colour only: remove every shadow, highlight, shine spot, glow "
                                                           "and gradient, also on the water orb and under the hat brim; keep "
                                                           "the crayon hatching as texture only."),
       ("Lộ mặt, có mắt hoặc chấm sáng dưới mũ", "The face must be completely hidden: under the hat brim only ONE flat "
                                                 "night-navy shape, with no eyes, no glowing dots, no mouth, no skin."),
       ("Gậy đè lên áo, vành mũ hoặc bắt chéo người", "Move the staff further to the right: it stands upright, at least 45 px "
                                                      "of pure white between the pole and the robe and between the staff "
                                                      "head and the hat brim; only the mitten hand touches it."),
       ("Quay sang trái hoặc nhìn thẳng", "Turn the mage three-quarters toward the viewer's RIGHT: staff on the right, back "
                                          "cloak and the drooping hat tip on the left."),
       ("Thành người (thấy chân, cổ, tóc, ngón tay)", "It is a small squat creature wrapped in clothes, not a human: no legs "
                                                      "(only two boot tips under the hem), no neck, no hair, no fingers "
                                                      "(one round mitten), chibi proportions with the hat almost half of "
                                                      "the height."),
       ("Quá nhiều chi tiết, hoa văn, nếp vải", "Simplify: plain cloth with two or three fold lines per piece, no patterns "
                                                "except the one drop emblem on the front panel, no extra belts, pouches, "
                                                "books or jewellery."),
       ("Có lông vũ, cánh, sao, trăng, mắt trên mũ", "Remove them: the hat has only its band, one teardrop gem, the bead on "
                                                     "its tip and two ribbon tails."),
       ("Có nước, bong bóng, vòng phép quanh người", "Remove every effect: only the mage and its staff on pure white."),
       ("Dạng 2 không cao hơn dạng 1 mấy", "Make form 2 clearly taller and more slender: the hat only one third of the height, "
                                           "the robe twice as long as in image 1, a taller staff with a bigger orb.")]


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
          "TASK: draw ONE creature hero as ONE picture, in a clean animation-ready standing pose, in the hand-drawn style of "
          "the approved hero images.", "",
          form, "", palette, "", frame, "", POSE, "", SOFT, LINE, FLAT, BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    gd = [f"# Gói gửi GPT: dòng `{CODE}` dạng {k} ({name})", "",
          "Tướng thứ 6 đảo Thủy, làm 2026-11-11 theo ý người dùng: pháp sư nước bí ẩn, mũ che kín mặt. Màu và chi tiết là đề "
          "xuất của Claude, chờ người dùng duyệt. Ghi chú thiết kế và mổ xẻ con gốc: `ArtGen/Spine/inbox/phap_su_ghichu.md`.", "",
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


def build_vong():
    """Lượt 2: vòng tròn triệu hồi (clip appear). Vẽ nhìn thẳng từ trên xuống, tròn đều; rig tự bóp dẹt thành elip nằm trên đất và
    xoay. Không dùng màu lam băng (gần trắng giấy, khó tách nền); không cần ảnh concept nên dựng được ngay."""
    refs = [(WORLD_STYLE, "the game's hand-drawn map, 1024x1536: use ONLY its line and colouring style (brown ink pen outline + "
                          "coloured pencil / wax crayon hatching), nothing of its content.",
             "Bản đồ vẽ tay đã duyệt (1024 × 1536): chỉ lấy nét bút mực nâu và vân chì sáp"),
            (DROP, "an approved hero of the same game, 1536x1024, white background: match its wobbly pen line, its visible "
                   "crayon hatching and its completely flat colouring. Do NOT draw this creature.",
             "Tí Tách dạng 1 đã duyệt (1536 × 1024, nền trắng): chỉ lấy nét bút rung, vân sáp, tô phẳng")]
    check(refs)
    os.makedirs(pk(1), exist_ok=True)
    os.makedirs(save_dir(1), exist_ok=True)
    out = os.path.join(save_dir(1), "V01.png")
    p = os.path.join(pk(1), "luot_2_vong_trieu_hoi.txt")
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          "If a file with that name already exists, save as V01_2.png, V01_3.png ... in the same folder. Do not edit, move "
          "or delete any other file.", "",
          "TASK: draw ONE flat water-magic SUMMONING CIRCLE, seen EXACTLY from straight above (a perfectly round circle, not "
          "an ellipse, no perspective), as a hand-drawn game effect sprite. It will later be laid flat on the ground under a "
          "small water mage and rotated, so it must be the same all the way around.", "",
          "CANVAS: square 1024x1024, pure-white background (#FFFFFF). The circle is centred exactly in the middle of the "
          "canvas, about 900 px across, nothing cut by the edges. Nothing else in the picture.", "",
          "DESIGN, from the outside to the centre (everything concentric, evenly spaced around the centre, six-fold "
          "symmetry):\n"
          "- OUTER RING: one closed band about 34 px thick, light aqua (#86D6F0), outer diameter about 900 px.\n"
          "- WAVE RING: just inside it, a ring of TWELVE identical small curling WAVE-CREST shapes (each about 90 px long "
          "and 50 px tall, a fat comma shape like a little breaking wave), sea teal (#2F9FB3), all curling the same way "
          "(clockwise), evenly spaced, not touching each other and not touching the rings.\n"
          "- INNER RING: a second closed band about 26 px thick, deep indigo (#2A3580), diameter about 620 px.\n"
          "- SIX DROPS: inside the inner ring, SIX identical water-drop shapes (each about 110 px long and 70 px wide, "
          "light aqua (#86D6F0)), arranged like the petals of a flower around the centre, their pointed tips pointing "
          "OUTWARD toward the inner ring, their round ends toward the centre, not touching each other.\n"
          "- CENTRE: one small closed ring about 22 px thick, sea teal (#2F9FB3), diameter about 150 px, with white paper "
          "inside it.\n"
          "All the space between these shapes is PURE WHITE paper (it will be made transparent): no filled disc, no "
          "background colour inside the circle, no runes, no letters, no stars, no thin scribbled lines.", "",
          "COLOURS: only these three: light aqua (#86D6F0), sea teal (#2F9FB3), deep indigo (#2A3580), plus the dark-brown "
          "ink outline (#2B2118). No pale or whitish colours, no white fill inside any shape.", "",
          "LINE AND COLOUR: drawn by hand on paper with a dark-brown ink pen, a closed outline about 5 px thick around "
          "every band and every shape (bands are outlined on both their outer and inner edge); the line is slightly wobbly "
          "like a real pen and the rings are hand-drawn, slightly uneven in thickness, but clearly round. Every shape is "
          "coloured with wax crayons, the strokes visible as loose diagonal hatching, kept inside the outline.",
          "FLAT COLOUR, NO LIGHT: every shape one even colour. No glow, no light rays, no sparkles, no gradients, no "
          "transparency, no shadows, no highlights, no 3D look, no water splashes.",
          "No text, no labels, no frame, no creature, no white border or sticker outline."]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = ["", "## Lượt 2: vòng tròn triệu hồi (clip ra sân)", "",
          f"File prompt: `{W(p)}`. GPT lưu vào `{W(out)}` (trùng tên thì `_2`, `_3`…). Ảnh mẫu: bản đồ vẽ tay "
          f"(`{W(WORLD_STYLE)}`, 1024 × 1536) và Tí Tách dạng 1 (`{W(DROP)}`, 1536 × 1024, nền trắng), chỉ lấy nét.", "",
          "Kiểm: vòng **tròn đều nhìn từ trên xuống** (không elip), nằm giữa khung 1024 × 1024, nền trắng tinh; vành ngoài lam "
          "nhạt, vòng 12 ngọn sóng lam ngọc, vành trong chàm, 6 giọt nước xoè như cánh hoa, vòng nhỏ ở tâm; giữa các hình là "
          "giấy trắng (không tô nền); không phát sáng, không chữ rune.", "",
          "Sai thì gửi thêm: `Seen exactly from straight above: a perfectly round circle centred on the canvas, flat crayon "
          "colours only, no glow, pure white paper between the shapes.`"]
    hd = os.path.join(pk(1), "HUONG_DAN.md")
    cur = open(hd, encoding="utf-8").read().split("\n## Lượt 2: vòng tròn triệu hồi")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cur + "\n" + "\n".join(gd) + "\n")
    return p


if __name__ == "__main__":
    print("dạng 1:", build_form(1))
    print("vòng triệu hồi:", build_vong())
    if os.path.exists(chosen(1)):
        print("dạng 2:", build_form(2))
    else:
        print("dạng 2: chưa dựng (chưa có", W(chosen(1)) + ")")
