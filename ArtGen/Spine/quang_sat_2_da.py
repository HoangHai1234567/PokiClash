# -*- coding: utf-8 -*-
"""Tinh linh quặng sắt DẠNG 2 (dạng cuối; mã làm việc quang_sat_2). Người dùng 2026-11-16: "làm dạng 2 của nó"; dòng có 2 dạng; đòn, chiêu như dạng 1
nhưng mạnh hơn; rig: "tự nghĩ" → Claude chọn dựng trên CHÍNH rig monster_3371 (dạng khác trên cùng rig: đòn húc / phóng hai tay / chui đất cần hai
tay rời + thân vòm; đôi mắt là nét nhận dòng người dùng chủ ý giữ). Bóng dáng phải khác hẳn dạng 1 (luật 0a: dạng cuối đổi màu chủ đạo, thêm giáp,
đổi dáng chi tiết nhận diện), giữ dải mặt + hai mắt.

    quang_sat_2_da.py concept    ba file prompt concept → gui_gpt/quang_sat_2/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
Ảnh mẫu duy nhất: concept dạng 1 đã duyệt (của mình), cùng khung 1536 × 1024 nên mảnh dạng 2 đặt thẳng lên rig như dạng 1."""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quang_sat as G  # noqa: E402

GUI = os.path.join(HERE, "gui_gpt", "quang_sat_2")
TAI = os.path.join(HERE, "inbox", "quang_sat_2", "tai_ve")
D1 = os.path.join(G.TAI, "L1_duyet.png")
MUC = "#2B2118"


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


ANH1 = ("STAGE 1 of our character (approved design), 1536x1024, white background: a chubby round blue-grey STONE dome spirit, a wide dark "
        "face band (V dip on top, wavy zigzag bottom) with two upright cyan oval eyes, two small silver studs above the band, three black-iron "
        "double-pointed octahedron crystals with silver ridge lines on its head and two floating black crystals as its hands. Hand-drawn: "
        "wobbly dark-brown ink line, crayon hatching, flat colours.")

KEEP = [
    "the POSE and VIEW (front, turned slightly to the viewer's right, sitting low on the ground, no legs, no arms) and the PLACE on the canvas;",
    "the DARK FACE BAND across the lower half of the body: same shape (V dip on top, wavy zigzag bottom), same place, same size, flat dark "
    "charcoal #2A2C33;",
    "the two EYES exactly: two upright flat cyan #5FD8EE ovals with one tiny white dot each, no pupils, no brows drawn on the eyes, the left "
    "eye a little bigger, same places (left eye about x = 775 to 842, y = 592 to 681; right eye about x = 991 to 1047, y = 597 to 684) and "
    "same sizes: the eyes are the character's expression and must not change;",
    "the BODY PLAN: one big dome body, pieces standing on top of the head, and two separate floating HANDS that do not touch the body (the "
    "long one at the lower left in front of the body edge, about x = 260 to 575, y = 600 to 890; the shorter one at the lower right beside "
    "the body edge, about x = 1120 to 1300, y = 610 to 890).",
]

# ba hướng (Claude đề xuất, chờ người dùng chọn): (tên Việt, mô tả Việt, các dòng CHANGE tiếng Anh)
HUONG = {
    "A": ("giáp thép rèn + vương miện năm gai từ thạch",
          "vỏ thành mũ giáp sắt rèn sẫm, một tấm mày giáp chữ V chìa ra trên dải mặt (nhìn dữ hơn), hai núm trán thành hai sừng thép ngắn vuốt "
          "ra sau; chỏm đầu thành vương miện NĂM gai bát diện cao vút xoè quạt; hai tay thành cụm hai tinh thể to ghép như găng sắt",
          ["BODY: the stone dome becomes a heavy ARMOURED HELMET-DOME of dark forged iron, a little bigger and taller than in image 1 (top of "
           "the dome about y = 285, sides about x = 455 to 1225, bottom about y = 885): main colour #565C68, the thick lower lip under the "
           "face band darker #3E434D; ONE thick armoured BROW PLATE in lighter steel #8E96A3 overhangs the top edge of the face band, "
           "following its V shape (a sterner frown). No speckles, no seam lines, no rivets.",
           "STUDS: the two little studs become two SHORT STEEL HORNS #8E96A3 at the upper corners of the face band, swept back and up.",
           "TOP OF THE HEAD: instead of three crystals, a CROWN of FIVE tall black magnetite octahedron SPIKES fanning out like a crown: the "
           "middle one very tall (its tip about y = 60), two on each side getting shorter and leaning outward; all black iron (lit facets "
           "#434751, facets turned away #2A2D34) with ONE thin silver ridge line #C3CAD3 each; their bases sit into the top of the dome.",
           "HANDS: each hand becomes a heavier GAUNTLET of TWO black octahedron crystals grown together side by side (same colours, silver "
           "ridge lines), about 20 % bigger than in image 1, in the same places."]),
    "B": ("quặng hematit đỏ + đá bazan có mạch cam",
          "vỏ đá bazan đen xám có ba mạch quặng cam phẳng, mày giáp đá; chỏm đầu thành chùm gai quặng hematit đỏ gỉ lởm chởm (một gai giữa "
          "cao, bốn gai quanh), hai tay thành cục quặng đỏ lởm chởm to; mắt giữ xanh lơ",
          ["BODY: the stone dome becomes a heavier dome of dark BASALT rock, a little bigger and taller than in image 1 (top of the dome about "
           "y = 285, sides about x = 455 to 1225, bottom about y = 885): main colour #4A474F, the thick lower lip under the face band darker "
           "#35333A; THREE thin flat ORANGE ore seams #E07A2E run over the dome (flat colour lines with an ink edge, no glow); ONE thick rock "
           "BROW ridge #5E5A63 overhangs the top edge of the face band following its V shape (a sterner frown).",
           "STUDS: the two little studs become two small rusty-red ore nubs #9A3B2C.",
           "TOP OF THE HEAD: instead of three crystals, a CLUSTER of FIVE jagged rusty-red HEMATITE ore SPIKES: one tall in the middle (its "
           "tip about y = 70), two on each side, shorter, leaning outward; each spike a long pointed crystal with flat facets: lit facets "
           "#9A3B2C, facets turned away #6B2620, one thin steel-grey ridge line #A3ABB6.",
           "HANDS: each hand becomes a bigger JAGGED chunk of red hematite ore (same colours), about 20 % bigger than in image 1, pointed, "
           "in the same places."]),
    "C": ("nam châm móng ngựa thép",
          "vỏ thép xám lam có mày giáp; trên đầu hai sừng tinh thể cong to vòng vào nhau thành NAM CHÂM MÓNG NGỰA (đầu một sừng đỏ, đầu sừng "
          "kia bạc), một tinh thể bát diện nhỏ ở giữa; hai tay thành hai khối cực nam châm (nửa đỏ nửa bạc)",
          ["BODY: the stone dome becomes a heavier dome of brushed STEEL, a little bigger and taller than in image 1 (top of the dome about "
           "y = 285, sides about x = 455 to 1225, bottom about y = 885): main colour #7D8DA6, the thick lower lip under the face band darker "
           "#5D6B82; ONE thick steel BROW PLATE #9AA8BE overhangs the top edge of the face band following its V shape (a sterner frown). No "
           "speckles, no seam lines.",
           "STUDS: the two little studs become two small round steel bolts #9AA8BE.",
           "TOP OF THE HEAD: instead of three crystals, TWO big curved crystal HORNS growing from the two upper sides of the dome and curving "
           "up and inward toward each other so that together they form a HORSESHOE MAGNET shape (a wide U, its two tips about y = 90, a gap "
           "between the tips); each horn black iron (#434751 / #2A2D34) with a broad flat band near its tip: RED #C8372D on the left horn "
           "tip, SILVER #D4DAE2 on the right horn tip; one small black octahedron crystal with a silver ridge stands in the middle between "
           "them.",
           "HANDS: each hand becomes a thick blocky MAGNET-POLE chunk (a short six-sided bar with flat ends), half red #C8372D and half silver "
           "#D4DAE2, about 20 % bigger than in image 1, in the same places and at the same slant."]),
}

STYLE = (f"DRAWING STYLE (very important): exactly the hand-drawn look of image 1: a wobbly dark-brown INK outline ({MUC}, about 7 px) running "
         "all the way round every piece, thinner ink lines (about 4 px) for the few inner edges (crystal facets, the brow plate, the face "
         "band), every area ONE flat colour with visible coloured-pencil / wax-crayon hatching. No shading, no highlights, no white shine "
         "streaks, no gradients, no glow, no shadows, no gloss, no sparkles. The only exception: one tiny white dot in each eye. VERY SIMPLE "
         "DESIGN, FEW DETAILS: nothing that is not listed (no extra spikes on the body, no chains, no runes, no cracks all over, no mouth, no "
         "arms, no legs).")


def prompt_concept():
    hd = ["# Gói GPT: tinh linh quặng sắt DẠNG 2 (quang_sat_2), tướng 3 đảo Kim", "",
          "Người dùng 2026-11-16: \"làm dạng 2 của nó\"; dòng 2 dạng (dạng 2 là dạng cuối); đòn, chiêu như dạng 1 nhưng mạnh hơn; rig do Claude "
          "chọn: cùng rig `monster_3371` với dạng 1. Ảnh mẫu duy nhất là concept dạng 1 đã duyệt (của mình).", "",
          "## Lượt 1: concept dạng 2, ba hướng", "",
          f"| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(D1)}` | Concept dạng 1 đã duyệt (1536 × 1024, nền trắng): vòm đá xám lam, dải mặt tối, hai mắt bầu dục xanh lơ, ba tinh thể "
          "bát diện sắt đen trên đầu, hai tinh thể làm tay |", ""]
    for k, (vi, vi2, doi) in HUONG.items():
        out, save = luu(f"L1_{k}")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(D1)}: {ANH1}", ""] + save + ["",
             "TASK: draw STAGE 2, the FINAL evolved form of the creature of image 1: the grown-up, battle-ready form: heavier, armoured, "
             "fiercer, clearly a different and stronger creature at first glance, while still recognisably the same line (same face band, "
             "same eyes). Determined and ready to fight; still cute, not scary. ONE picture on a 1536x1024 canvas.", "",
             "KEEP IDENTICAL:"] + [f"- {x}" for x in KEEP] + ["", "CHANGE:"] + [f"- {d}" for d in doi] + ["",
             STYLE, "",
             "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the creature at the same place as "
             "in image 1. No labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: dải mặt và hai mắt y như dạng 1 (dáng, chỗ, cỡ, màu); hai tay rời thân, đúng hai chỗ; bóng dáng (vỏ, chỏm đầu, tay) khác hẳn dạng 1; "
           "nét mực rung, vân sáp, tô phẳng, không bóng, không phát sáng; nền trắng.", "",
           "Câu sửa nhanh: \"keep the eyes exactly as in image 1\"; \"the two hands must float apart from the body\"; \"flat colour only, no "
           "highlights\"."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "concept":
        prompt_concept()
    else:
        print(__doc__)
