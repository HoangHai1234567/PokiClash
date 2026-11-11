"""Gói GPT vẽ MẢNH cho dòng sò đột biến (so_gai), làm lại từ đầu 2026-11-11.

Người dùng: "đập đi gen lại từ đầu", "lòi xòm nhiều quá, đọc lại skill tôi mới note dịch ngược file spine xem các mảnh của họ".
Bộ cũ cắt hai mai ra từ concept rồi vá bằng mã (lòng bát, vách khoé miệng, mí...) nên mép rách, lòi mẩu vụn. Bộ này chia mảnh
MỘT – MỘT theo con gốc (skill pokiclash-spine-rig mục 00; tờ mổ ở D:/Ripper/SwordxStaff/scan/monster_3237/manh_*.png):

  con gốc (sau → trước)            của mình                       GPT vẽ
  P_xiaba1  vòm tối, viền ở dây    long      vòm tím sau lưỡi      tờ mảnh P01, ô A
  P_shetou  lưỡi (đổi ảnh khi lè)  luoi      lưỡi nằm / lưỡi dài   tờ mảnh P01, ô D và F
  P_xiaba   mặt trước mai dưới     mai_duoi  bát + vành gần + nanh  D01 (đúng chỗ, đúng cỡ như concept)
  P_tou1    vòm mai trên kín       mai_tren  vòm + vành + gai + nanh U01 (đúng chỗ, đúng cỡ, KHÔNG có mắt)
  P_yanjing1/2 mắt đổi ảnh         mat       mắt mở / mắt nhắm      tờ mảnh P01, ô B và C
  (không có)                       moi       môi chu (chiêu nhổ ngọc) tờ mảnh P01, ô E

Gai và nanh của họ là mảnh rời nhưng bám cùng xương với mai, không động riêng: của mình vẽ liền vào mai (ít mảnh, không hở chân gai).
Mỗi mảnh là MỘT hình kín viền mực do GPT vẽ; mã chỉ tách nền trắng, không vá, không cắt theo màu.

    py -3 -I ArtGen/Spine/build_so_gai2.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/so_gai_<k>/luot_2_mai_tren.txt --timeout 420
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/so_gai_<k>/luot_2_mai_duoi.txt --timeout 420
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/so_gai_<k>/luot_2_to_manh.txt --timeout 420
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_so_gai as B  # noqa: E402

W, pk, save_dir, chosen, check = B.W, B.pk, B.save_dir, B.chosen, B.check

FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area one even colour, the crayon strokes are texture only; no shading, no "
        "darker side, no highlights, no shine spots, no pearly sheen, no gloss, no glow, no gradients, no shadows of any kind, "
        "no 3D look.")
PAGE = ("CANVAS: 1536x1024, pure-white background (#FFFFFF) everywhere outside the drawing: no paper grain, no ground line, no "
        "shadow, no text, no labels, no frame, no white sticker border. Nothing else on the page.")
SAME = ("Same hand-drawn look as image 1: wobbly dark-brown ink outline (#2B2118) of the same thickness as in image 1, the same "
        "flat colours, the same loose crayon hatching.")

# ---- điều riêng từng dạng
U_KEEP = {1: "the teal dome with its lighter ribs, the four coral-orange cone spikes, the two cream barnacles, the wavy "
             "coral-orange rim band along its lower edge with the round rim knot at the hinge on the far left, and the three "
             "cream fangs hanging down from the underside of the rim band",
          2: "the navy dome with its teal ribs, the crown of coral-orange cone spikes with red tips, the four cream barnacles, "
             "the red zigzag scar, the wavy coral-orange rim band along its lower edge with the round rim knot at the hinge on "
             "the far left, and all the cream fangs hanging down from the underside of the rim band"}
U_EYE = {1: "the two yellow eyes together with their pupils and their brow lines",
         2: "the two yellow eyes together with their pupils and their two thick dark brow bars"}
D_KEEP = {1: "the round mother-of-pearl bowl with its thin lilac rib lines, the three coral-orange cone spikes on its outside, "
             "the wavy coral-orange NEAR RIM band along its top edge, and the two cream fangs standing up from that rim band",
          2: "the round bowl (upper two thirds mother-of-pearl pinkish white, lower third lilac) with its lilac rib lines, the "
             "five coral-orange cone spikes on its outside, the wavy coral-orange NEAR RIM band along its top edge, and the "
             "three cream fangs standing up from that rim band"}
D_EXTRA = {1: "",
           2: " The pink tongue tip that hangs over the rim on the right is part of the tongue: remove it and draw the rim band "
              "and the bowl that were behind it."}
DOME = {1: (640, 300), 2: (760, 360)}
TONGUE = {1: "REST TONGUE: the tongue as it lies inside the mouth in image 1, drawn complete: a wide, low, soft mound, about "
             "470 px wide and 150 px tall, round on top, with a flat slightly wavy bottom edge, its right end a rounded tip a "
             "little higher than its left end. Raspberry pink (#E0567F) with ONE short darker pink line (#B83A62) near the top "
             "middle, as in image 1.",
          2: "REST TONGUE: the tongue as it lies in the mouth in image 1, drawn complete: a wide, thick, soft slab about 620 px "
             "wide and 150 px tall, round on top with a flat slightly wavy bottom edge; at its RIGHT end it bends over and hangs "
             "DOWN as a fat rounded tip about 110 px wide that reaches about 120 px below the slab's bottom edge (the tip that "
             "hangs over the lip in image 1). Hot pink (the tongue colour of image 1) with ONE long darker pink line along the "
             "top, as in image 1."}
EYE_SIZE = {1: "the NEAR eye about 110 px wide, the FAR eye about 65 px wide", 2: "the NEAR eye about 185 px wide, the FAR eye "
               "about 95 px wide"}
LONG = {1: 1300, 2: 1300}


def _viet(p, t):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")


def _dau(refs, out, ten):
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {W(r)}: {en}" for i, (r, en, _) in enumerate(refs, 1)]
    t += ["", f"SAVE: save it as a PNG to {W(out)}",
          f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move "
          "or delete any other file.", ""]
    return t


def build_upper(k):
    refs = [(chosen(k), f"the approved clam creature (form {k}), 1536x1024, white background. Its UPPER SHELL is the big dome on "
                        "top, with the wavy coral-orange rim band along its lower edge. You will redraw this picture keeping ONLY "
                        "that upper shell, in exactly the same place.",
             f"Sò đột biến dạng {k} đã duyệt (1536 × 1024, nền trắng): lấy đúng mai trên (vòm có vành cam), giữ nguyên chỗ, cỡ")]
    check(refs)
    out = os.path.join(save_dir(k), "U01.png")
    p = os.path.join(pk(k), "luot_2_mai_tren.txt")
    t = _dau(refs, out, "U01")
    t += ["TASK: redraw image 1 with ONLY ITS UPPER SHELL: one separate, complete part for a 2D cut-out animation in which the "
          "upper shell swings up and down around the hinge like a lid.", "",
          f"KEEP EXACTLY AS DRAWN in image 1, in the SAME POSITION on the canvas and at the SAME SIZE: {U_KEEP[k]}. "
          "Same outline, same colours, same crayon hatching.", "",
          "REMOVE completely:",
          "- the whole lower shell (its bowl, its rim band, its spikes, its fangs);",
          "- the tongue and the dark inside of the mouth;",
          f"- {U_EYE[k]}: where they were, continue the shell colour and its ribs so the dome is plain there, as if the creature "
          "never had eyes. No trace of eyes, pupils, lids or brows may remain (the eyes will be separate parts).", "",
          "COMPLETE THE PART so it is ONE CLOSED SHAPE with an ink outline all the way around:",
          "- the rim band runs unbroken along the whole lower edge of the dome, from the rim knot at the hinge on the far left to "
          "its front end on the right, with an ink outline on its upper and on its lower edge;",
          "- below the rim band there is NOTHING except the fangs hanging from it: pure white page between and under the fangs. "
          "Do not draw the inside or underside of the shell, no dark area, no second rim.", "",
          PAGE, "", SAME, "", FLAT]
    _viet(p, t)
    return p


def build_lower(k):
    refs = [(chosen(k), f"the approved clam creature (form {k}), 1536x1024, white background. Its LOWER SHELL is the round bowl at "
                        "the bottom, with the wavy coral-orange rim band along its top edge. You will redraw this picture keeping "
                        "ONLY the outside of that lower shell, in exactly the same place.",
             f"Sò đột biến dạng {k} đã duyệt (1536 × 1024, nền trắng): lấy đúng mặt ngoài mai dưới (bát có vành cam), giữ nguyên chỗ, cỡ")]
    check(refs)
    out = os.path.join(save_dir(k), "D01.png")
    p = os.path.join(pk(k), "luot_2_mai_duoi.txt")
    t = _dau(refs, out, "D01")
    t += ["TASK: redraw image 1 with ONLY THE FRONT OF ITS LOWER SHELL: one separate, complete part for a 2D cut-out animation. "
          "This part is drawn in FRONT of the tongue; the dark inside of the mouth is another part and must NOT be drawn here.", "",
          f"KEEP EXACTLY AS DRAWN in image 1, in the SAME POSITION on the canvas and at the SAME SIZE: {D_KEEP[k]}. "
          "Same outline, same colours, same crayon hatching.", "",
          "REMOVE completely: the whole upper shell (dome, rim band, rim knot, eyes, brows, fangs, spikes, barnacles), the tongue, "
          "and the dark plum inside of the mouth." + D_EXTRA[k], "",
          "COMPLETE THE PART so it is ONE CLOSED SHAPE with an ink outline all the way around:",
          "- the near rim band runs unbroken along the whole top edge of the bowl, from a small rounded end at the hinge on the far "
          "left to its front end on the right, with an ink outline on its upper and on its lower edge;",
          "- ABOVE the rim band there is NOTHING except the fangs standing on it: pure white page behind and above the fangs. No "
          "dark plum, no inside of the bowl, no far rim, no tongue.", "",
          PAGE, "", SAME, "", FLAT]
    _viet(p, t)
    return p


def build_sheet(k):
    refs = [(chosen(k), f"the approved clam creature (form {k}), 1536x1024, white background: the colours, the ink line, the "
                        "crayon hatching, the eyes and the tongue to copy. Do not draw the clam itself.",
             f"Sò đột biến dạng {k} đã duyệt: mẫu màu, nét, mắt, lưỡi")]
    check(refs)
    out = os.path.join(save_dir(k), "P01.png")
    p = os.path.join(pk(k), "luot_2_to_manh.txt")
    dw, dh = DOME[k]
    t = _dau(refs, out, "P01")
    t += ["TASK: a SHEET OF SIX SEPARATE LOOSE PARTS of the clam creature of image 1, for a 2D cut-out animation. NOT a creature "
          "and NOT a scene: only the loose parts listed below, each alone on the pure-white page like stickers laid on a table, "
          "at least 70 px of pure white between any two parts and between a part and the image edge. Do NOT draw the clam, its "
          "shells, spikes or fangs. No labels, no numbers, no arrows, no guide lines, no cell borders.", "",
          "Every part is ONE CLOSED SHAPE with a wobbly dark-brown ink outline all the way around (same thickness as the outlines "
          "of image 1), flat colour and loose crayon hatching, at the SAME SCALE as image 1.", "",
          "LAYOUT (canvas 1536x1024), six cells:",
          f"A. TOP LEFT (x 40 to 800, y 30 to 420): MOUTH BACK, the dark inside of the mouth seen when the clam opens wide. ONE "
          f"plain half-dome: a round arched top and an almost straight bottom edge, about {dw} px wide and {dh} px tall. Flat "
          "dark plum (#3A2147) with crayon hatching. Along the straight bottom edge runs a thin coral-orange band (#F08A4B, about "
          "18 px thick, very gently wavy) from corner to corner. Ink outline all around. Completely empty: no tongue, no teeth, "
          "no throat, nothing inside.",
          f"B. TOP RIGHT, upper row (x 880 to 1500, y 30 to 210): EYES OPEN: the two eyes of image 1, copied exactly, side by "
          f"side with 80 px of white between them: left the bigger NEAR eye, right the smaller FAR eye, each with its own brow "
          f"exactly as in image 1 (the brow is joined to its eye, one closed shape). Same size as in image 1 ({EYE_SIZE[k]}). "
          "Golden yellow (#FFD23F), black slit pupil, one tiny white dot, dark brow.",
          "C. TOP RIGHT, lower row (x 880 to 1500, y 240 to 420): EYES SHUT: the same two eyes, same sizes, same brows in the "
          "same places and angles, but squeezed shut: under each brow, instead of the yellow eye, ONE thick dark ink curve "
          "bulging downward (the closed lid line), joined to the brow at its two ends so the shape reads as a fierce shut eye. "
          "No yellow, no pupil. Left the near eye, right the far eye, 80 px of white between them.",
          f"D. MIDDLE LEFT (x 40 to 800, y 470 to 730): {TONGUE[k]} Ink outline all around.",
          "E. MIDDLE RIGHT (x 880 to 1500, y 470 to 730): PUCKERED LIPS: the clam's two coral rim bands pressed together and "
          "pushed forward into a whistling, spitting mouth, seen from the front: an upper lip and a lower lip of coral orange "
          "(#F08A4B), together about 250 px wide and 150 px tall, thick and plump in the middle and tapering to a point at the "
          "left and at the right end, with ONE small round dark-plum hole (#3A2147, about 40 px) in the centre between the two "
          "lips and four short ink wrinkle lines around the hole. Ink outline all around.",
          f"F. BOTTOM (x 40 to 1500, y 780 to 1000): LONG TONGUE, pulled all the way out and laid STRAIGHT and HORIZONTAL: about "
          f"{LONG[k]} px long. Its LEFT end is the root: a blunt rounded stump about 150 px thick. It tapers smoothly and slowly "
          "to the RIGHT end: a rounded tip about 80 px thick with a small notch in the middle of the tip. Its upper and lower "
          "edges are gently wavy, not ruler-straight. Same pink as the rest tongue, ONE darker pink centre line running from the "
          "root and stopping 80 px before the tip. Ink outline all around. No drool, no drops.", "",
          "PURE WHITE (#FFFFFF) page, no paper grain.", "", FLAT]
    _viet(p, t)
    return p


BACK_H = {1: 270, 2: 390}


def build_back(k):
    """vòm tím sau lưỡi, đúng chỗ đúng cỡ concept (thay ô A của tờ mảnh: vành miệng nhìn chéo nên dây cung thẳng không khít khoé miệng)."""
    refs = [(chosen(k), f"the approved clam creature (form {k}), 1536x1024, white background. Between its two wavy coral rim bands we "
                        "see the DARK PLUM INSIDE of the mouth. You will redraw this picture keeping ONLY that dark inside, in exactly "
                        "the same place, completed into one closed shape.",
             f"Sò đột biến dạng {k} đã duyệt (1536 × 1024, nền trắng): lấy đúng mảng tím trong miệng, giữ nguyên chỗ, cỡ")]
    check(refs)
    out = os.path.join(save_dir(k), "L01.png")
    p = os.path.join(pk(k), "luot_2_vom_tim.txt")
    t = _dau(refs, out, "L01")
    t += ["TASK: redraw image 1 with ONLY THE DARK INSIDE OF ITS MOUTH: one separate, complete part for a 2D cut-out animation. "
          "In the animation this part sits BEHIND the tongue and behind both shells; when the upper shell swings up like a lid, "
          "this part is the dark hollow of the lower jaw that we see behind the tongue.", "",
          "KEEP EXACTLY where it is visible in image 1, in the SAME POSITION on the canvas and at the SAME SIZE: the dark plum "
          "area between the two rim bands, including its RIGHT-HAND EDGE at the front of the mouth (the ink line that runs between "
          "the front ends of the upper and the lower rim band).", "",
          "REMOVE completely: both shells with their rim bands, rim knot, spikes, barnacles, eyes and all fangs, and the tongue.", "",
          "COMPLETE THE PART into ONE CLOSED HALF-DOME SHAPE, flat dark plum (#3A2147) everywhere, with a dark-brown ink outline "
          "all the way around:",
          "- where the tongue and the fangs covered it: plain dark plum;",
          "- BOTTOM: it continues down behind the place of the lower rim band and ends about 35 px below the TOP edge of that rim "
          "band, following the same gentle sagging curve, from the hinge on the far left to the front end on the right;",
          f"- TOP: it continues up behind the place of the upper shell as ONE big smooth round arc from the hinge on the left to "
          f"the front on the right; the highest point of the arc is above the middle of the mouth, about {BACK_H[k]} px above the "
          "lower rim band. The arc stays well inside the area that the upper shell covers in image 1;",
          "- completely empty: no tongue, no teeth, no throat, no rim band, no lighter or darker patches.", "",
          PAGE, "", SAME, "", FLAT]
    _viet(p, t)
    return p


def build_tongue2():
    """dạng 2: lưỡi nằm trọn vẹn, đúng chỗ đúng cỡ concept (thay ô D của tờ mảnh: chóp vắt mép phải đúng cỡ concept)."""
    k = 2
    refs = [(chosen(k), "the approved clam creature (form 2), 1536x1024, white background. Its hot-pink TONGUE lies in the mouth and "
                        "its tip hangs over the lower rim on the right. You will redraw this picture keeping ONLY the tongue, in "
                        "exactly the same place, completed into one closed shape.",
             "Sò đột biến dạng 2 đã duyệt: lấy đúng cái lưỡi, giữ nguyên chỗ, cỡ")]
    check(refs)
    out = os.path.join(save_dir(k), "T01.png")
    p = os.path.join(pk(k), "luot_2_luoi_nam.txt")
    t = _dau(refs, out, "T01")
    t += ["TASK: redraw image 1 with ONLY ITS TONGUE: one separate, complete part for a 2D cut-out animation.", "",
          "KEEP EXACTLY AS DRAWN in image 1, in the SAME POSITION on the canvas and at the SAME SIZE: every visible part of the "
          "tongue: the wide pink slab lying in the mouth with its long darker pink line, and the rounded tip that hangs over the "
          "lower rim on the right. Same colours, same outline, same crayon hatching.", "",
          "REMOVE completely: both shells with their rim bands, spikes, barnacles, eyes and all fangs, and the dark plum inside of "
          "the mouth.", "",
          "COMPLETE THE PART so it is ONE CLOSED SHAPE with an ink outline all the way around:",
          "- where fangs or the rim band covered the tongue: plain pink tongue;",
          "- the slab continues DOWN behind the place of the lower rim band for about 45 px below the top edge of that rim band and "
          "closes there with a smooth, gently curved bottom edge;",
          "- its LEFT end (the root, deep in the mouth) is a blunt rounded end;",
          "- the slab and the hanging tip are one continuous piece.", "",
          PAGE, "", SAME, "", FLAT]
    _viet(p, t)
    return p


def build_tip2():
    """dạng 2: chóp lưỡi vắt qua mép, mảnh riêng vẽ TRƯỚC mai dưới (con gốc cũng tách lưỡi hai ảnh khi lưỡi vắt qua hàm: P_shetou1 / P_shetou2)."""
    k = 2
    refs = [(chosen(k), "the approved clam creature (form 2), 1536x1024, white background. On the right, the rounded TIP of its "
                        "hot-pink tongue hangs over the lower rim band, in front of the lower shell. You will redraw this picture "
                        "keeping ONLY that hanging tip, in exactly the same place.",
             "Sò đột biến dạng 2 đã duyệt: lấy đúng chóp lưỡi vắt qua vành dưới, giữ nguyên chỗ, cỡ")]
    check(refs)
    out = os.path.join(save_dir(k), "T02.png")
    p = os.path.join(pk(k), "luot_2_chop_luoi.txt")
    t = _dau(refs, out, "T02")
    t += ["TASK: redraw image 1 with ONLY THE TIP OF THE TONGUE THAT HANGS OVER THE LOWER RIM: one small separate part for a 2D "
          "cut-out animation. This part is drawn in FRONT of the lower shell.", "",
          "KEEP EXACTLY AS DRAWN in image 1, in the SAME POSITION on the canvas and at the SAME SIZE: only the part of the tongue "
          "that lies in front of the lower rim band and the lower shell: the rounded pink flap hanging down, from the top edge of "
          "the lower rim band downward. Same colour, same outline, same crayon hatching.", "",
          "REMOVE completely: everything else: both shells, rim bands, spikes, fangs, eyes, the dark inside, and the rest of the "
          "tongue above the rim.", "",
          "COMPLETE THE PART so it is ONE CLOSED SHAPE with an ink outline all the way around: a simple rounded tongue-tip shape "
          "hanging straight down, only as wide as the hanging tip seen in image 1 (about 85 px), widest near its bottom; close its "
          "top with a short, almost straight ink line (the fold of the tongue) exactly at the top edge of the lower rim band. No "
          "tail, no point, nothing extending to the left of the hanging tip along the rim. If a fang overlapped the flap, plain "
          "pink there.", "",
          PAGE, "", SAME, "", FLAT]
    _viet(p, t)
    return p


# Người dùng 2026-11-11 (lần ba): "con này không có thịt trong... sao bạn cứ gen cái mảng tím, đây là 2 hàm trên dưới của con sò, xóa
# mảng tím". Lớp sau lưỡi KHÔNG phải khối tím: nó là NỬA SAU CỦA HÀM DƯỚI (mặt trong vỏ sò, mép trên là vành xa màu cam), như
# P_xiaba1 của con gốc (mặt trong tối cùng tông với vỏ, có dải vành). Thấp: chỉ cao hơn khe miệng lúc nghỉ một chút.
BACK2_H = {1: 165, 2: 240}
BACK2_BEND = {1: 60, 2: 110}   # vành xa rời vành trên, vòng xuống ở cách đầu miệng bao nhiêu px (sớm quá thì lúc nghỉ hở một khe dưới nanh trên)
BACK2_COL = {1: "deep dark teal (#0F3A42): the shadowed inner side of the same shell, the dark version of the teal of the upper shell",
             2: "deep dark navy (#141D40): the shadowed inner side of the same shell, the dark version of the navy of the upper shell"}


def build_back2(k):
    """NỬA SAU CỦA HÀM DƯỚI = mặt trong cái bát, như P_xiaba1 của con gốc (xem tờ mổ đã sửa chiều xoay: mép TRÊN là vành xa gần
    thẳng nối hai đầu vành gần, bụng tối thõng XUỐNG khuất sau vách trước). Miệng bát là một hình hạt hạnh khép kín: vành xa
    vòng lại gặp đầu vành gần ở phía trước, KHÔNG chếch lên theo vành trên (người dùng trả bản B01_2: "nó phải vòng vào trong
    chứ tự nhiên lại chếch chéo lên trên")."""
    refs = [(chosen(k), f"the approved clam creature (form {k}), 1536x1024, white background. Its LOWER SHELL is a bowl; in image 1 we "
                        "see the front wall of the bowl with the wavy coral rim band along its top (the NEAR rim). You will draw the "
                        "INSIDE of that same bowl (its back wall with the FAR rim), in exactly the right place.",
             f"Sò đột biến dạng {k} đã duyệt (1536 × 1024, nền trắng): mai dưới là cái bát; vẽ mặt trong của bát (vách sau + vành xa), đúng chỗ, đúng cỡ")]
    check(refs)
    out = os.path.join(save_dir(k), "B01.png")
    p = os.path.join(pk(k), "luot_2_ham_duoi_sau.txt")
    t = _dau(refs, out, "B01")
    t += ["TASK: draw ONLY THE INSIDE OF THE LOWER SHELL of image 1 (the back wall of the bowl with its far rim): one separate, "
          "complete part for a 2D cut-out animation. The clam is just two hard shell halves, an upper jaw and a lower jaw; there "
          "is NO flesh and NO soft mass inside. The lower jaw is a bowl seen a little from above: its opening is a closed ALMOND "
          "shape, with the NEAR rim (already in image 1) as the front edge and the FAR rim as the back edge; the two rims meet at "
          "the hinge on the left and meet again at the front end on the right. In the animation this part is drawn behind the "
          "tongue, and the front wall of the bowl is drawn in front of the tongue, so the tongue lies inside the bowl.", "",
          "PLACE AND SIZE: same canvas as image 1; the part sits exactly on the lower shell of image 1.", "",
          "SHAPE, one closed shape with a dark-brown ink outline all the way around:",
          "- TOP edge = the FAR RIM of the bowl: ONE smooth, gently wavy arch. It starts at the hinge on the far left (where the "
          "near rim starts), rises, runs for most of its length just behind the LOWER edge of the upper rim band of image 1 (about "
          f"12 px above that lower edge, so there it would be hidden behind the upper shell) and stays behind the upper rim band "
          f"as far forward as possible; only about {BACK2_BEND[k]} px before the front end of the near rim it turns DOWN in a "
          "round bend, like the rim of a bowl coming around toward the viewer, "
          "and JOINS the front end of the near rim band of image 1. The front of the bowl opening is ROUND. The far rim must NOT "
          "go up to the front end of the upper rim, and there is no corner, no point and no hook at the front.",
          "- Along the whole far rim, from the hinge to the front end, runs the rim band: the same coral-orange (#F08A4B) gently "
          "wavy band as the near rim of image 1, a little thinner (about 20 px), with an ink line on both of its edges. At the "
          "hinge it simply ends in a small rounded end (do NOT draw the round rim knot).",
          f"- BELOW the far rim band: the inner surface of the bowl, flat {BACK2_COL[k]}. Plain and empty: no tongue, no teeth, no "
          "flesh, no throat, no purple, no patches.",
          "- BOTTOM edge: the belly of the bowl, hidden behind the front wall: it follows the same sagging curve as the near rim "
          "band of image 1 but about 45 px LOWER than the top edge of that near rim band, from the hinge on the left to the front "
          "end on the right, where it closes under the round bend of the far rim.", "",
          "Do NOT draw anything else: no upper shell, no eyes, no fangs, no spikes, no tongue, no front wall of the bowl.", "",
          PAGE, "", SAME, "", FLAT]
    _viet(p, t)
    return p


def build_jaw2(k):
    """CẢ HÀM DƯỚI trong MỘT ảnh (bát + vành gần + nanh, gai + lòng bát + vành xa), đúng chỗ đúng cỡ concept. Người dùng trả bản hai
    ảnh rời (D01 vách trước + B01 mặt trong): "mép nối đầu miệng không match bị lệch", "dạng 1 lệch hẳn còn không khớp nhau":
    hai ảnh GPT vẽ riêng thì hai đầu vành không bao giờ trùng. Một ảnh thì hai vành là MỘT vòng liền. so_gai2.py dùng cả ảnh làm
    lớp sau lưỡi, và lấy vách trước (từ mép trên vành gần trở xuống, kèm nanh) ra từ CHÍNH ảnh này làm lớp trước lưỡi: hai lớp
    cùng nét vẽ, cùng xương nên chỗ nối không thể lệch."""
    refs = [(chosen(k), f"the approved clam creature (form {k}), 1536x1024, white background. Its LOWER SHELL is the round bowl at "
                        "the bottom, with the wavy coral-orange rim band along its top edge (the NEAR rim). You will redraw this "
                        "picture keeping ONLY that lower shell, in exactly the same place, and showing the inside of the bowl.",
             f"Sò đột biến dạng {k} đã duyệt (1536 × 1024, nền trắng): lấy đúng mai dưới (cái bát có vành cam), giữ nguyên chỗ, cỡ, vẽ thêm lòng bát")]
    check(refs)
    out = os.path.join(save_dir(k), "J01.png")
    p = os.path.join(pk(k), "luot_2_ham_duoi.txt")
    t = _dau(refs, out, "J01")
    t += ["TASK: redraw image 1 with ONLY ITS LOWER SHELL (the lower jaw), complete, for a 2D cut-out animation in which the clam "
          "opens its mouth wide. The clam is just two hard shell halves, an upper jaw and a lower jaw; there is NO flesh and NO "
          "soft mass inside. The lower jaw is a bowl seen a little from above, so we look into it.", "",
          "REMOVE completely: the whole upper shell (dome, rim band, rim knot, eyes, brows, upper fangs, spikes, barnacles), the "
          "tongue, and the dark plum area of image 1." + D_EXTRA[k], "",
          f"KEEP EXACTLY AS DRAWN in image 1, in the SAME POSITION on the canvas and at the SAME SIZE: {D_KEEP[k]}. Same outline, "
          "same colours, same crayon hatching. Where the tongue or the upper shell covered the near rim band, complete it so it "
          "runs unbroken from the hinge on the far left to its front end on the right.", "",
          "ADD the inside of the bowl, which the removed parts were hiding:",
          "- THE FAR RIM: the rim of the bowl continues around the back. The opening of the bowl is ONE closed ALMOND shape and "
          "the coral-orange rim band is ONE continuous ring around it: the near rim (from image 1) is its front half, the far rim "
          "is its back half, and they are joined seamlessly at the hinge on the left and at the front end on the right, where the "
          "band simply turns around in a smooth round U-bend. Same coral orange (#F08A4B), the far half a little thinner (about "
          "20 px), ink line on both edges, gently wavy.",
          "- COURSE OF THE FAR RIM: from the hinge it rises, then runs just behind the LOWER edge of the upper rim band of image 1 "
          "(about 12 px above that lower edge: if this drawing were put back behind the upper shell, the far rim would be hidden "
          f"by the upper rim band), stays there as far forward as possible, and only about {BACK2_BEND[k]} px before the front end "
          "it turns down in the round U-bend and becomes the near rim. It must NOT go up to the front end of the upper rim; no "
          "corner, no point, no hook, no loose end anywhere: one ring.",
          f"- INSIDE the ring: the inner surface of the bowl, flat {BACK2_COL[k]}. Plain and completely empty: no tongue, no flesh, "
          "no throat, no purple, no patches. The fangs of the near rim stand in front of this dark inside.", "",
          PAGE, "", SAME, "", FLAT]
    _viet(p, t)
    return p


def build_drool():
    """tờ mảnh DÃI (dùng chung hai dạng): người dùng 2026-11-11 "cho nó chảy dãi, chiêu cuối cũng bắn dãi lung tung".
    Sợi dãi rủ từ vành dưới lúc nghỉ (rig kéo dài rồi nhỏ giọt), giọt dãi văng theo lưỡi ở chiêu cuối."""
    k = 1
    refs = [(chosen(k), "the approved clam creature (form 1), 1536x1024, white background: the ink line and the crayon hatching to "
                        "copy. Do not draw the clam itself.",
             "Sò đột biến dạng 1 đã duyệt: mẫu nét mực và nét sáp")]
    check(refs)
    out = os.path.join(save_dir(k), "S01.png")
    p = os.path.join(pk(k), "luot_2_dai.txt")
    t = _dau(refs, out, "S01")
    t += ["TASK: a SHEET OF FIVE SEPARATE LOOSE PARTS for a 2D cut-out animation: the DROOL (saliva) of the clam creature of image "
          "1. NOT a creature and NOT a scene: only the five parts listed below, each alone on the pure-white page like stickers "
          "laid on a table, at least 90 px of pure white between any two parts and between a part and the image edge. No labels, "
          "no numbers, no arrows, no guide lines.", "",
          "Every part is ONE CLOSED SHAPE: slimy saliva in ONE flat colour, pale watery aqua (#BFE8E6), with a wobbly dark-brown "
          "ink outline (#2B2118, the same thickness as the outlines of image 1) all the way around and loose crayon hatching "
          "inside. Inside each part ONE small curved mark in a slightly darker aqua (#8CCFD0) near one edge; nothing else. No "
          "white highlight, no shine, no gloss, no gradient, no transparency, no shadow.", "",
          "LAYOUT (canvas 1536x1024), five parts in one row, their centres at about x = 200, 520, 830, 1100, 1340:",
          "1. LONG DROOL STRAND, hanging straight down: about 130 px wide at the very top (a flat, slightly wavy top edge: there "
          "it hangs from the lip), quickly narrowing to a thin thread about 34 px wide, and ending at the bottom in a fat round "
          "drop about 120 px wide. About 760 px tall in total.",
          "2. SHORT DROOL DRIP, hanging straight down: the same idea but short and thick: flat top about 120 px wide, a short neck "
          "about 50 px wide, a round drop about 110 px wide at the bottom. About 330 px tall.",
          "3. BIG FLYING DROP: a teardrop with its pointed tail straight UP and its round belly at the bottom, about 150 px wide "
          "and 230 px tall.",
          "4. MEDIUM FLYING DROP: the same teardrop, about 105 px wide and 160 px tall, the tail slightly bent.",
          "5. SMALL FLYING DROP: an almost round little blob with a very short tail up, about 80 px wide and 95 px tall.", "",
          "PURE WHITE (#FFFFFF) page, no paper grain.", "", FLAT]
    _viet(p, t)
    return p


def huong_dan(k, ps):
    gd = [f"# Gói gửi GPT: dòng `so_gai` dạng {k}, lượt 2 làm lại (mảnh theo cách tách của con gốc)", "",
          "Mỗi file prompt một ảnh. **Chỉ gửi GPT đường dẫn từng file**; GPT tự mở ảnh mẫu và tự lưu (trùng tên thì `_2`, `_3`…; "
          "`so_gai2.py cat` lấy bản mới nhất).", "",
          "| File prompt | Ảnh ra | Là gì |", "|---|---|---|",
          f"| `{W(ps[0])}` | `{W(os.path.join(save_dir(k), 'U01.png'))}` | mai trên riêng, đúng chỗ đúng cỡ, không mắt, vành liền, nanh treo |",
          f"| `{W(ps[1])}` | `{W(os.path.join(save_dir(k), 'D01.png'))}` | mặt trước mai dưới riêng, đúng chỗ đúng cỡ, phía trên vành là nền trắng |",
          f"| `{W(ps[2])}` | `{W(os.path.join(save_dir(k), 'P01.png'))}` | tờ 6 mảnh: vòm tím (dự phòng), mắt mở, mắt nhắm, lưỡi nằm, môi chu, lưỡi dài |",
          f"| `{W(ps[3])}` | `{W(os.path.join(save_dir(k), 'B01.png'))}` | nửa sau của hàm dưới: mặt trong vỏ màu tối cùng tông vỏ (KHÔNG tím), mép trên và mép trước là vành xa màu cam; đúng chỗ đúng cỡ |"]
    if k == 2:
        gd += [f"| `{W(ps[4])}` | `{W(os.path.join(save_dir(k), 'T01.png'))}` | lưỡi nằm trọn vẹn, đúng chỗ đúng cỡ (dùng thay ô D của tờ mảnh) |",
               f"| `{W(ps[5])}` | `{W(os.path.join(save_dir(k), 'T02.png'))}` | chóp lưỡi vắt qua mép, mảnh nhỏ vẽ trước mai dưới: nửa tròn, mép trên là nếp gấp thẳng, không có đuôi |"]
    gd += [
          "", "Ảnh mẫu (cả ba file): `" + W(chosen(k)) + "` (concept đã duyệt, 1536 × 1024, nền trắng, con sò miệng hé).", "",
          "## Kiểm", "",
          "- U01, D01: chồng lên concept thì trùng khít; mỗi mảnh một hình kín, không còn gì của mảnh kia, không có vùng tím.",
          "- U01 không còn mắt, mày; chỗ mắt là màu mai trơn có gân.",
          "- P01 đủ sáu mảnh rời, cách nhau, mỗi mảnh viền mực kín; tô phẳng.",
          "- B01: thấp, mép trên chạy ngay sau vành trên của concept (không hở khe nào giữa hai vành), có vành cam ở mép trên và "
          "mép trước, lòng màu tối cùng tông vỏ, không tím, không có gì bên trong.",
          "- T01, T02 (dạng 2): chồng lên concept thì phần thấy được trùng khít; phần khuất nối trơn, một hình kín.", "",
          "## GPT vẽ sai thì gửi thêm", "", "| Sai | Gửi thêm |", "|---|---|",
          "| Mảnh bị dời chỗ, đổi cỡ | `Keep the part in exactly the same position and size as in image 1.` |",
          "| Còn mắt trên mai trên | `Remove the eyes and brows completely; plain shell colour and ribs there.` |",
          "| Còn vùng tím, lưỡi, vành xa | `Remove every dark plum area and the tongue; pure white there.` |",
          "| Có bóng, điểm sáng | `Flat colour only: no shading, no highlights.` |"]
    _viet(os.path.join(pk(k), "HUONG_DAN_luot_2_lam_lai.md"), gd)


if __name__ == "__main__":
    print(W(build_drool()))
    for k in (1, 2):
        ps = [build_upper(k), build_lower(k), build_sheet(k), build_back2(k)]              # build_back (vòm tím) đã bỏ
        print(W(build_jaw2(k)))
        if k == 2:
            ps += [build_tongue2(), build_tip2()]
        huong_dan(k, ps)
        for p in ps:
            print(W(p))
