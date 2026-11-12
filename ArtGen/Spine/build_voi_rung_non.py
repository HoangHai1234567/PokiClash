# -*- coding: utf-8 -*-
"""Gói GPT vẽ DẠNG 1 của ma mút rừng (voi con; mã voi_rung, dạng 1). Người dùng 2026-11-12: "sau đó làm thêm dạng 1 nữa" (không
dặn hình: hai hướng dưới đây là ĐỀ XUẤT của Claude, chờ người dùng chọn). Cùng dòng với dạng 2 đã duyệt (inbox/voi_rung_2/tai_ve/
L1_duyet.png): cùng góc nhìn, cùng cách dựng (ụ lá của thân, mái lá của đầu, vòi, hai ngà, bốn chân, đuôi) để dùng lại bộ rig
voi_rung.py; chibi chỉ ở dạng 1 (đầu to, vòi ngắn, ngà mới nhú, lá non ít hơn, màu tươi hơn).

    py -3 -I ArtGen/Spine/build_voi_rung_non.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/voi_rung_1/luot_1_concept_<hướng>.txt [--note "..."]
Lượt 2, 3 (mảnh, lớp lá) dùng lại prompt của dạng 2 (build_voi_rung.py chạy với VR_DANG=1) sau khi có tai_ve/L1_duyet.png.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_voi_rung as B  # noqa: E402

K = 1
Wp, _dau, _viet, check = B.Wp, B._dau, B._viet, B.check
LON = B.chosen(2)

HUONG = {
    "ao_choang": dict(
        ten="áo choàng lá non ngắn (hai tầng), bụng và chân để trần, mầm xoắn trên đầu",
        mantle="a SHORT CAPE of young leaves lies over its back and shoulders: only TWO overlapping tiers of big rounded-pointed "
               "leaves (the same kind of leaf as in image 1, but fewer and bigger in proportion: about five or six leaves in the "
               "upper tier, seven or eight in the lower). The cape hangs only to the middle of the flank: the belly, the chest "
               "and the whole of all four legs stay bare. On the head a small CAP of four or five of the same leaves, its "
               "short fringe just touching the brow (the whole eye stays visible), and on top of the cap ONE little curled "
               "SPROUT standing up (a short stem ending in a small spiral, like a fern shoot, about 70 px tall)"),
    "nam_la": dict(
        ten="ụ lá non tròn phủ gần kín thân (ba tầng) như dạng lớn, mầm xoắn trên u vai",
        mantle="a round BALL of young leaves covers its whole back, shoulders and flanks, like the mantle of image 1 but younger "
               "and smaller: THREE overlapping tiers of big rounded-pointed leaves hanging to about the height of the knees, "
               "the outline a bold zigzag of leaf tips; only the lower legs, the face and the trunk are bare. On the head a "
               "CAP of five or six of the same leaves with a fringe hanging over the brow so that the eye peeks out under it. "
               "On top of the hump ONE little curled SPROUT standing up (a short stem ending in a small spiral, like a fern "
               "shoot, about 80 px tall)"),
}


def body(kieu):
    M = HUONG[kieu]
    return "\n".join([
        "CREATURE: the CHILD form of the forest mammoth of image 1: the same species before it grows up, a small round chubby "
        "MAMMOTH CALF for a monster-collecting game. Character: a brave, stubborn little fighter, planted firmly and ready to "
        "charge even though it is small; cute and appealing, but with a determined look, not a smiling baby mascot, not sleepy.",
        "- VIEW: exactly the same three-quarter front view as image 1: it faces the viewer's RIGHT and is turned partly toward "
        "the viewer; the head and trunk at the right front, the body behind it to the left.",
        "- PROPORTIONS (chibi, very different from image 1): the HEAD is huge, about as big as the body (about 45% of the total "
        "height); the body is a short round barrel; a low rounded back (no high hump); four very short stubby legs. The whole "
        "creature is only about 1.15 times as wide as it is tall.",
        f"- LEAVES: {M['mantle']}. The upper leaves are fresh leaf green (#63B04A), the lowest tier and the fringe tips light "
        "spring green (#A6D34F); centre veins a darker green (#3F8A45); the sprout light spring green. Two or three tiny cream "
        "dots on the leaves. No dark forest green anywhere (that is the colour of the adult).",
        "- HIDE: smooth thick hide of slate blue, a little lighter and softer than the adult's (#6E8597): the face, the trunk, "
        "the belly and the legs.",
        "- FACE: ONE eye visible (the near one), clearly BIGGER than the adult's in proportion: a round amber eye (#F2B43A) with a "
        "big black pupil and one tiny white dot, its upper lid a straight ink line slanting down toward the trunk (determined). "
        "Under the root of the trunk a short, closed, slightly down-turned mouth line.",
        "- TRUNK: short and thick, only about half as long as the adult's: it hangs down in front of the chest at the right, "
        "ends well above the ground and its blunt round tip curls up and to the right, with two small dark nostril dots. Three "
        "curved wrinkle lines across it.",
        "- TUSKS: only two small TUSK BUDS, just beginning to grow from the corners of the mouth: short, thick, slightly curved "
        "nubs of the same pale honey-coloured root wood as in image 1 (#E3C98A, one or two grain lines), about 70 px long, "
        "pointing forward and a little up, each with a tiny tuft of moss at its root. The near bud is in front of the trunk "
        "root; the far bud shows on the other side of the trunk. No big curled tusks.",
        "- LEGS: four very short, thick pillar legs of bare hide, each with THREE rounded toenails of pale honey wood (#E3C98A). "
        "All four feet visible, apart, on the same ground. No rings or bands.",
        "- TAIL: short and thin at the far left, ending in ONE small light-green leaf.",
        "- No ears visible (hidden under the leaves). No mushrooms, no flowers, no stone, no armour.",
        "",
        "COLOURS (use exactly these, each area ONE flat colour): hide (#6E8597); leaves (#63B04A) and (#A6D34F) with veins "
        "(#3F8A45); tusk buds and toenails (#E3C98A); moss tufts (#63B04A); eye (#F2B43A); every outline dark-brown ink "
        "(#2B2118). Only these colours.",
    ])


FRAME = ("CANVAS AND FRAMING: landscape 1536x1024, pure-white background, NO ground line, no cast shadow. The whole creature is "
         "visible, nothing cut by the edges. Draw it LARGE (it will be scaled down later): about 880-960 px wide and about "
         "780-840 px tall, centred, its feet standing at about y = 930.")

POSE = ("POSE (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): standing still, "
        "planted on all four legs, in the same clean resting pose as image 1: legs straight and apart, not crossing, not walking; "
        "the trunk hanging free in front (it does not touch the ground, the legs or the tusk buds); the mouth closed. No falling "
        "leaves, no dust, no sparkles, no glow, no motion lines, no ground, no grass, no props.")

LINE = ("LINE AND COLOUR: exactly the look of image 1: the same bold dark-brown ink outline (#2B2118, about 6 px on this canvas "
        "around every big part, about 4 px for small details), leaf veins and trunk wrinkles as thinner darker lines, every "
        "area filled with coloured pencil / wax crayon, the strokes visible as loose diagonal hatching, texture only.")


def build(kieu):
    R = [(LON, "the approved ADULT form of this creature, 1536x1024, white background: a huge forest mammoth in three-quarter "
               "view facing the viewer's right, covered by a mantle of big dark-green leaves in tiers, with a leaf fringe over "
               "the brow, one fierce amber eye, dark slate-blue hide, a thick trunk and two big curled honey-coloured root-wood "
               "tusks. Use it for the SPECIES, the VIEW, the kind of leaf, the line and the crayon colouring. You will draw its "
               "CHILD form: do not copy its proportions, its size of tusks or its dark greens.",
          "Dạng 2 đã duyệt (1536 × 1024, nền trắng): ma mút rừng áo lá lục sẫm xếp tầng, da đá lam, hai ngà rễ gỗ màu mật cuộn to, "
          "nhìn ba phần tư sang phải. Lấy loài, góc nhìn, kiểu lá, nét và cách tô")]
    check(R)
    out = os.path.join(B.save_dir(K), f"L1_{kieu}.png")
    p = os.path.join(B.pk(K), f"luot_1_concept_{kieu}.txt")
    t = _dau(R, out, f"L1_{kieu}")
    t += ["TASK: draw ONE creature hero as ONE picture, in a clean animation-ready resting pose: the CHILD form of the creature of "
          "image 1.", "", body(kieu), "", FRAME, "", POSE, "", LINE, B.FLAT, B.BG]
    _viet(p, t)
    return p, R, out


INTRO1 = ("a forest mammoth CALF in three-quarter view facing the viewer's right, 1536x1024, white background: a small chubby "
          "body covered by a round ball of big fresh-green leaves in three tiers, a cap of the same leaves on its huge head with a "
          "fringe over the brow and one big determined amber eye under it, slate-blue hide on the face, trunk and legs, a short "
          "thick trunk with its tip curled forward, two small honey-coloured tusk buds each with a moss tuft, four short pillar "
          "legs with three honey toenails each, a thin tail with a small leaf tuft at the far left, and one curled green sprout "
          "standing on top of the back")


def build_sua():
    """lượt 1b: người dùng chọn hướng B (nam_la) 2026-11-12. Vẽ lại y hệt, chỉ đổi lá về tô phẳng (luật: không chuyển màu)."""
    nhap = os.path.join(B.save_dir(K), "L1_nam_la.png")
    if not os.path.exists(nhap):
        raise SystemExit("thiếu bản nháp " + Wp(nhap))
    out = os.path.join(B.save_dir(K), "L2.png")
    p = os.path.join(B.pk(K), "luot_1b_to_phang.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(nhap)}: the DRAFT of this creature: {INTRO1}. This is the design, the pose, the line and the colours to "
         "keep.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as L2_2.png, L2_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: redraw image 1 as ONE picture, changing ONLY the colouring of the leaves as listed under CHANGE.", "",
         "KEEP IDENTICAL to image 1, in the same place and at the same size (if the new picture were laid over image 1, every "
         "ink line must coincide): the whole creature, its pose and its view; the outline and the vein lines of every leaf; the "
         "cream dots; the curled sprout; the eye and its lid line; the mouth line; the trunk with its wrinkle lines and nostril "
         "dots; both tusk buds with their moss tufts; all four legs and toenails; the tail and its leaf tuft; the colours of "
         "everything that is not a leaf; the bold dark-brown ink outline; the white background.", "",
         "CHANGE, FLAT LEAF COLOURS: in image 1 the leaves fade softly from green into yellow-green toward their tips. Remove "
         "every such fade: each leaf is entirely ONE flat colour from its stalk to its tip.",
         "- all the leaves of the two UPPER tiers of the body, and all the leaves of the cap on the head: fresh leaf green "
         "(#63B04A);",
         "- all the leaves of the LOWEST tier of the body (the row whose tips hang over the legs), the small leaf tuft of the "
         "tail and the curled sprout: light spring green (#A6D34F).",
         "No gradient anywhere, no lighter tips.", "",
         "Colouring as in image 1: every area filled with coloured pencil / wax crayon, the strokes visible as loose diagonal "
         "hatching, texture only.", "", B.FLAT, B.BG]
    _viet(p, t)
    return p, nhap, out


# ---------------------------------------------------------------- lượt 2 (mảnh) và lượt 3 (lớp lá) của dạng 1: cùng cách chia như dạng 2
PARTS = {
    "ao": dict(
        src="L1_duyet", out="B01", vi="ụ lá của thân kèm mầm xoắn (bỏ đầu, vòi, ngà, bốn chân, đuôi)",
        what="THE LEAF BALL OF ITS BODY",
        role="In the animation this ball of leaves is the body; the head, the tusk buds, the legs and the tail are separate parts "
             "laid over it or behind it.",
        keep="the whole ball of leaves that covers the back and the flanks: the two upper tiers of fresh-green leaves, the lowest "
             "tier of light yellow-green leaves with its hanging pointed tips, every leaf, vein line and cream dot exactly as "
             "drawn, and the curled sprout standing on top",
        remove="the whole head (its own cap of leaves, the face, the eye, the trunk), both tusk buds with their moss tufts, all "
               "four legs with their toenails, and the tail with its leaf tuft",
        complete=["where the head, its leaf cap and the near tusk bud covered the leaf ball (its right part): continue the ball "
                  "as the same overlapping tiers of big leaves, down to the same light yellow-green lowest tier with hanging "
                  "pointed tips at the same height as on the flank, so the ball is a complete round hill of leaves whose right "
                  "edge is about where the middle of the head was;",
                  "between the hanging tips of the lowest tier, where the legs and the belly showed: pure white page (do not "
                  "draw legs, hide or belly);",
                  "where the tail was attached at the left: the plain leaf outline of the ball."]),
    "dau": dict(
        src="L1_duyet", out="H01", vi="đầu: mái lá + mặt + mắt + vòi (bỏ hai ngà nhú và túm rêu, thân, chân)",
        what="ITS HEAD TOGETHER WITH ITS TRUNK",
        role="In the animation the head nods and the trunk swings and curls; the two tusk buds are separate parts.",
        keep="the cap of fresh-green leaves on the head with its cream dot and its fringe of leaf tips hanging over the brow and "
             "down both sides of the face, the slate-blue face with the big eye, its lid line and the mouth line, and the whole "
             "short trunk with its wrinkle lines, curled tip and nostril dots. Face and trunk are ONE continuous slate-blue shape",
        remove="both tusk buds completely, each together with its moss tuft, the whole leaf ball of the body with the sprout, all "
               "four legs and the tail",
        complete=["where the near tusk bud and its moss tuft covered the cheek: plain slate-blue hide; the cheek is a round jaw "
                  "whose outline runs from under the leaf fringe at the left down and around to the underside of the trunk "
                  "root; the mouth line continues to its natural end;",
                  "where the far tusk bud sat at the right edge of the face: the plain outline of the face running down into "
                  "the trunk;",
                  "the head with its cap and trunk is ONE CLOSED SHAPE; outside it pure white page."]),
    "nga": dict(
        src="L1_duyet", out="T01", vi="hai ngà mới nhú, mỗi ngà kèm túm rêu ở gốc (ngà xa vẽ đủ phần bị che)",
        what="ITS TWO TUSK BUDS",
        role="In the animation the tusk buds are small rigid parts fixed to the head.",
        keep="(1) the near tusk bud with its grain lines, together with the moss tuft at its root; (2) the far tusk bud at the "
             "right with its moss tuft. Two separate shapes, each exactly where it is in image 1",
        remove="everything else: the head with its leaf cap, the face, the eye, the trunk, the leaf ball of the body, the sprout, "
               "the legs and the tail",
        complete=["each tusk bud is ONE closed shape with an ink outline all the way around;",
                  "the far tusk bud is drawn COMPLETE: continue it about 40 px to the left, where the face hid its root, and "
                  "close it there with a rounded root end under its moss tuft;",
                  "everything else: pure white page."]),
    "chan": dict(
        src="L1_duyet", out="G01", vi="ba chân (chân ngoài cùng bên trái, chân thứ hai từ trái, chân trước to bên phải) vẽ đủ phần bị lá che + đuôi",
        what="THREE OF ITS LEGS AND ITS TAIL",
        role="In the animation the legs stand behind the hanging leaves and the tail swings from the rump; each is a separate "
             "part.",
        keep="(1) the leftmost leg; (2) the second leg from the left; (3) the big front leg at the right, the one below the head; "
             "each with its flat foot and three honey toenails; and (4) the thin tail with its leaf tuft at the far left. Four "
             "separate shapes, each exactly where it is in image 1",
        remove="the leaf ball, the sprout, the head, the trunk, both tusk buds, and the small fourth leg that is partly hidden "
               "between the second leg and the big front leg",
        complete=["each leg is drawn COMPLETE as ONE CLOSED thick pillar: continue it upward, where the hanging leaves or the "
                  "head hid it, with the same width, up to about y = 650, and close it there with a round top; plain "
                  "slate-blue hide, ink outline all the way around;",
                  "the tail is ONE closed shape: continue its thin stem up and to the right for about 50 px, where the leaves "
                  "hid it, and close it with a small round end;",
                  "between and around the four shapes: pure white page."]),
}
MANTLE1 = ("the leaf ball of a forest mammoth calf, alone on a white 1536x1024 page: a round mound of big overlapping leaves in "
           "three tiers: two upper tiers of fresh-green leaves (some carry a small cream dot) and one lowest tier of LIGHT "
           "yellow-green leaves hanging along the bottom, with one curled sprout standing on top")
HEAD1 = ("the head of a forest mammoth calf, alone on a white 1536x1024 page: a slate-blue face with one big amber eye and a "
         "mouth line, a short thick trunk hanging down to the right with a curled tip and two nostril dots, and on top a cap of "
         "fresh-green leaves whose fringe hangs over the brow and down both sides of the face")
LOP = {
    "la_day": dict(
        src="B01", out="C01", vi="tầng lá dưới cùng (lục vàng) vẽ đủ phần bị lá trên che", intro=MANTLE1,
        what="ITS LOWEST TIER, THE LIGHT YELLOW-GREEN LEAVES",
        keep="every light yellow-green leaf of the lowest tier, with its hanging pointed tip, its outline and its vein, exactly "
             "where it is",
        remove="all the fresh-green leaves (the two tiers above), the cream dots and the sprout",
        complete=["each light leaf continues UPWARD, where the fresh-green leaves hid it, as a full leaf of the same light "
                  "yellow-green with its centre vein, up to about y = 620; the leaves overlap each other like roof tiles and "
                  "together form ONE connected band across the whole width of the mound;",
                  "the top edge of the band is a row of rounded leaf tops at about y = 600-630, with an ink outline;",
                  "above the band and below the tips: pure white page."]),
    "la_giua": dict(
        src="B01", out="C02", vi="tầng lá giữa (lục tươi, mũi lá rủ thấp hơn y ≈ 580) vẽ đủ phần bị tầng trên che", intro=MANTLE1,
        what="THE MIDDLE TIER OF FRESH-GREEN LEAVES",
        keep="the fresh-green leaves of the middle tier: every fresh-green leaf whose pointed TIP hangs below about y = 580 (the "
             "row just above the light yellow-green tier, all the way from the left edge of the mound to its right edge), each "
             "with its outline and veins exactly where it is",
        remove="the light yellow-green lowest tier (pure white where it showed below and between the tips), and all the UPPER "
               "leaves: the big leaves at the top that carry the cream dots, every leaf whose tip ends above about y = 580, and "
               "the sprout",
        complete=["each kept leaf continues UPWARD, where the upper leaves hid it, as a full fresh-green leaf with its centre "
                  "vein, up to about y = 420; together the kept leaves form ONE connected mass across the whole width of the "
                  "mound;",
                  "the top edge of that mass is a row of rounded leaf tops at about y = 400-440, with an ink outline;",
                  "above it and below the tips: pure white page."]),
    "la_tren": dict(
        src="B01", out="C03", vi="các lá phía trên (lá to có chấm kem, mũi lá cao hơn y ≈ 580) kèm mầm xoắn", intro=MANTLE1,
        what="THE UPPER LEAVES AND THE SPROUT",
        keep="the upper part of the mound exactly as drawn: the big fresh-green leaves at the top that carry the cream dots, "
             "every leaf whose pointed TIP ends above about y = 580, with all outlines, veins and dots, and the curled sprout "
             "standing on top",
        remove="everything below them: the middle tier of fresh-green leaves (every leaf whose tip hangs below about y = 580) and "
               "the light yellow-green lowest tier",
        complete=["nothing was hidden: the kept leaves and the sprout stay exactly as they are and form ONE connected mass with "
                  "an ink outline all the way around; its lower edge is the jagged row of its own hanging leaf tips;",
                  "below and between those tips, where the removed leaves were: pure white page."]),
    "so": dict(
        src="H01", out="H02", vi="đầu TRỌC (không lá) liền vòi: sọ tròn, mắt to vẽ đủ", intro=HEAD1,
        what="ITS HEAD AND TRUNK WITHOUT ANY LEAVES",
        keep="the slate-blue face with the mouth line, the eye, and the whole trunk with its wrinkle lines, curled tip and "
             "nostril dots, exactly where they are",
        remove="the whole cap of fresh-green leaves with its fringe and its cream dot",
        complete=["where the leaf cap was: a BALD rounded skull of the same slate-blue hide: a big smooth dome whose top is at "
                  "about y = 340 and whose sides run down into the cheeks and into the trunk root; plain hide, no hair, no "
                  "leaves;",
                  "the EYE is drawn complete: the same big round amber eye in the same place and size as in image 1, with its "
                  "black pupil and tiny white dot, its upper edge a thick straight ink lid line slanting down toward the trunk "
                  "(the same determined look), and one short thick brow stroke just above it;",
                  "head and trunk are ONE closed slate-blue shape; outside it pure white page."]),
    "mai": dict(
        src="H01", out="F01", vi="mái lá của đầu (vòm lá lục tươi, các lọn mái rủ trước trán và hai bên mặt)", intro=HEAD1,
        what="THE LEAF CAP OF ITS HEAD",
        keep="the whole cap of fresh-green leaves on the head with its cream dot, and the fringe of leaf tips hanging over the "
             "brow and down both sides of the face, every leaf exactly where it is",
        remove="the slate-blue face, the eye, the mouth line and the whole trunk",
        complete=["nothing was hidden: the leaves stay exactly as they are and form ONE connected shape with an ink outline all "
                  "the way around; the lower edge is the jagged row of hanging leaf tips;",
                  "where the face and the eye showed between and below the leaf tips: pure white page (no blue, no eye)."]),
}
VI_NGUON = {"L1_duyet": "Voi con đã duyệt (1536 × 1024, nền trắng): ụ lá non tròn ba tầng, mái lá che trán, mắt hổ phách to, vòi ngắn, "
                        "hai ngà mới nhú, mầm xoắn trên lưng",
            "B01": "Ảnh mảnh ụ lá của thân voi con (B01, 1536 × 1024, nền trắng): hai tầng lá lục tươi, tầng dưới cùng lục vàng, mầm xoắn",
            "H01": "Ảnh mảnh đầu voi con (H01, 1536 × 1024, nền trắng): mặt da đá lam một mắt hổ phách to, vòi ngắn, mái lá lục tươi"}


def build_manh(ten, d, luot):
    src = os.path.join(B.save_dir(K), d["src"] + ".png")
    intro = ("the approved creature: " + INTRO1) if d["src"] == "L1_duyet" else d["intro"]
    R = [(src, intro + f". You will redraw this picture keeping ONLY {d['what']}, in exactly the same place.",
          VI_NGUON[d["src"]] + ". Lấy đúng " + d["vi"] + ", giữ nguyên chỗ, cỡ")]
    check(R)
    out = os.path.join(B.save_dir(K), d["out"] + ".png")
    p = os.path.join(B.pk(K), f"luot_{luot}_{ten}.txt")
    t = _dau(R, out, d["out"])
    vai = d.get("role", "In the animation the leaf layers sway in the wind independently, so every layer must be complete even "
                        "where another layer lies over it.")
    t += [f"TASK: redraw image 1 with ONLY {d['what']}: separate, complete part(s) for a 2D cut-out animation. {vai}", "",
          f"KEEP EXACTLY AS DRAWN in image 1, in the SAME POSITION on the canvas and at the SAME SIZE (if the new picture were "
          f"laid over image 1, every kept line must coincide): {d['keep']}. Same outline, same colours, same crayon hatching.", "",
          f"REMOVE completely: {d['remove']}. No trace of them may remain.", "",
          "COMPLETE what was hidden, so that every kept part is ONE CLOSED SHAPE with an ink outline all the way around:"]
    t += ["- " + c for c in d["complete"]]
    t += ["", B.PAGE, "", B.SAME, "", B.FLAT2]
    _viet(p, t)
    return p, src, out


def main():
    os.makedirs(B.pk(K), exist_ok=True)
    os.makedirs(B.save_dir(K), exist_ok=True)
    gd = ["# Gói gửi GPT: `voi_rung` dạng 1 (voi con của ma mút rừng, tướng thứ 5 đảo Mộc)", "",
          "Làm 2026-11-12 sau khi rig dạng 2 xong. Hình dạng 1 là ĐỀ XUẤT của Claude (hai hướng), chờ người dùng chọn. Ghi chú: "
          "`ArtGen/Spine/inbox/voi_rung_ghichu.md`.", ""]
    for kieu, M in HUONG.items():
        p, R, out = build(kieu)
        print(p)
        gd += [f"## Hướng `{kieu}`: {M['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/voi_rung_1/luot_1_concept_{kieu}.txt`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += [""]
    if os.path.exists(os.path.join(B.save_dir(K), "L1_nam_la.png")):
        p, nhap, out = build_sua()
        print(p)
        gd += ["## Lượt 1b: người dùng chọn hướng B (`nam_la`) 2026-11-12", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Ảnh mẫu duy nhất: `{Wp(nhap)}` (bản nháp hướng B, 1536 × 1024, nền trắng: voi con ụ lá non tròn ba tầng, mái lá che "
               "trán, mắt hổ phách to, ngà mới nhú, mầm xoắn trên lưng). Vẽ lại y hệt, chỉ đổi lá về tô phẳng: hai tầng trên và mái lá "
               "lục tươi, tầng dưới cùng + lá đuôi + mầm lục vàng, không chuyển màu.", "",
               "Kiểm: đặt chồng lên bản nháp phải khít mọi nét; không còn chuyển màu trên lá. Bản đạt chép thành `tai_ve/L1_duyet.png`.", ""]
    for luot, bang, can, tieu_de in ((2, PARTS, ["L1_duyet"], "Lượt 2: mảnh (đúng chỗ, đúng cỡ như concept đã duyệt)"),
                                     (3, LOP, ["B01", "H01"], "Lượt 3: tách lớp lá (ảnh mẫu là ảnh mảnh lượt 2)")):
        if all(os.path.exists(os.path.join(B.save_dir(K), n + ".png")) for n in can):
            gd += [f"## {tieu_de}", "", "| File prompt (chỉ gửi GPT đường dẫn này) | Ảnh mẫu | Ảnh ra | Là gì |", "|---|---|---|---|"]
            for ten, d in bang.items():
                p, src, out = build_manh(ten, d, luot)
                print(p)
                gd += [f"| `{Wp(p)}` | `{Wp(src)}` ({VI_NGUON[d['src']]}) | `{Wp(out)}` | {d['vi']} |"]
            gd += ["", "Kiểm: đặt chồng lên ảnh mẫu thì phần giữ lại phải khít; mỗi mảnh / lớp một hình kín viền mực; nền trắng tinh; "
                   "không bóng.", ""]
    gd += ["## Kiểm", "",
           "- Voi con **chibi**: đầu to gần bằng thân, vòi ngắn mập (chóp cong lên, không chạm đất), hai **ngà mới nhú** (mẩu ngắn có "
           "túm rêu), mắt to hơn dạng lớn nhưng vẫn quả quyết; cùng góc ba phần tư nhìn sang phải.",
           "- Lá **non, lục tươi và lục vàng** (không có lục sẫm của dạng lớn); một **mầm xoắn**; đủ bốn chân tách nhau, đuôi một lá.",
           "- Tô phẳng, không bóng; nền trắng tinh; cả con không bị cắt mép.", ""]
    _viet(os.path.join(B.pk(K), "HUONG_DAN.md"), gd)


if __name__ == "__main__":
    main()
