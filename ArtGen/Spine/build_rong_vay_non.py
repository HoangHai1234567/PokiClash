# -*- coding: utf-8 -*-
"""Gói prompt cho DẠNG 1 của rồng vây (rồng non, mã làm việc `rong_vay_non`; người dùng 2026-11-12: "làm dạng 1 đi").
Hình đang có (`rong_vay_1`, rồng trưởng thành bám con gốc) là dạng 2 trong game. Dạng 1 chạy trên CÙNG rig, cùng lưới, cùng clip:
chỉ đổi tỉ lệ dáng gốc (đầu to 1,26; cánh 0,6: `rong_vay_rig.py`, RV_DANG=non) và vẽ lại da trong cùng khung part.

Lượt 1 (file này): concept cả con để người dùng duyệt. Ảnh 2 là hình bố cục do rig dựng với tỉ lệ rồng non (da còn của dạng 2):
    RV_DANG=non py -3 -I ArtGen/Spine/rong_vay_rig.py bo_cuc <inbox>/rong_vay_non/mau/bo_cuc.png
    py -3 -I ArtGen/Spine/build_rong_vay_non.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/rong_vay_non/luot_1_concept.txt
Lượt 2 (từng tờ part) chỉ dựng sau khi có tai_ve/L1_duyet.png."""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "rong_vay_non"
W = os.path.normpath
PK = os.path.join(HERE, "gui_gpt", CODE)
TAI = os.path.join(HERE, "inbox", CODE, "tai_ve")
BO_CUC = os.path.join(HERE, "inbox", CODE, "mau", "bo_cuc.png")
LON = os.path.join(HERE, "inbox", "rong_vay_1", "tai_ve", "L1_duyet.png")
# bản nháp concept lượt trước: người dùng ưng MẶT ("mặt nhìn non hơn rồi") nhưng bảo "thân bạn cũng phải làm ngắn hơn" → bố cục mới
# (rig co thân 0,72 dọc chiều dài), giữ nguyên thiết kế đầu, màu, nụ sừng, cánh, vây của bản nháp
NHAP = os.path.join(TAI, "L1_concept_3.png")
# lượt 4: người dùng xem L1_concept_3 (vây đã ngắn): "phần đuôi vẫn dài, thu ngắn các part thân/đuôi lại chút" → rig: thân sau 0,62, đuôi 0,54
# lượt 3: người dùng xem L1_concept_2 (thân đã ngắn): "làm vây của nó ngắn hơn chút nữa" → rig co vây (lưng 0,74; tai 0,80; đuôi 0,82)

DESIGN = [
    "WHO: the JUVENILE form of the creature in image 1 (a winged sea-serpent dragon). Same species, clearly younger: it will grow "
    "into image 1. Cute but with a fighter's look: a determined, focused face, ready to fight; not a smiling mascot, not scary.",
    "",
    "WHAT CHANGES from the adult (image 1 / the skin in image 2):",
    "- BODY COLOUR: a lighter, fresher blue: periwinkle blue (#6C86DC) instead of the adult's deep indigo. Belly plates stay cream "
    "(#F3E6C4) with thin ink lines between the plates.",
    "- HEAD: bigger and rounder for its body (as in image 2). ONE big round amber eye (#F2A21E) with a dark slit pupil and one "
    "small white dot; a short straight dark brow line above it for the determined look. The beak is shorter and blunter, "
    "charcoal black (#26252C).",
    "- HORNS: NO long horns. In their place only two SHORT, rounded charcoal-black horn BUDS (about as long as the eye is wide) "
    "on top of the head.",
    "- WINGS: small, as in image 2 (the wings have not grown yet): pale aqua web (#9CD3D6) on a few dark-blue rays (#3B4CA8), "
    "one or two round cream spots on each wing, softly scalloped trailing edge.",
    "- FINS (ear fins, back fins, tail fin): the same places and sizes as in image 2, pale aqua web (#9CD3D6) with dark-blue "
    "rays (#3B4CA8), slightly softer and rounder tips than the adult's.",
    "- NO scallop shells on the back (the adult wears them; the juvenile's back is plain periwinkle).",
    "",
    "- FIN LENGTH: every fin is SHORT, exactly as long as in image 2 (the back fins reach only a little above the back; the "
    "ear fins and the tail fin are small). Do not lengthen any fin.",
    "- BODY AND TAIL LENGTH: the juvenile's serpent body is clearly SHORTER and more compact than the adult's, exactly as image 2 "
    "shows: a short, stubby body; the rear body makes ONE small tight coil (the hole inside the coil is very small); the tail "
    "is short and its fin sits close behind the chest. Same body thickness. Do not lengthen the body, the coil or the tail.",
    "",
    "WHAT STAYS EXACTLY AS IN IMAGE 2: the pose, the facing (head at the upper right, looking right), the body's coil, the place, "
    "size and angle of the head, neck, body loop, tail, every fin and both wings. Image 2 is the exact layout: if the result "
    "were laid over image 2, the head, body loop, tail fin, wings and fins would sit on the same places at the same sizes. Only "
    "the horns become short buds and the skin is redrawn.",
]
LOOK = ("LOOK (same as image 1): drawn by hand on paper with an ink pen: a slightly wobbly dark-brown ink outline (#2B2118) of "
        "the same thickness as in image 1, filled with coloured pencil and wax crayon (loose hatching is only texture). FLAT "
        "COLOUR, NO LIGHT, NO SHADOW: every area one even colour; no shading, no highlights, no gloss, no glow, no gradients, "
        "no cast shadow, no ground shadow. Only the one small white dot in the eye.")
PAGE = ("CANVAS: 1536x1024, landscape. The whole creature inside the canvas with a margin, at the same place and size as in "
        "image 2. Pure-white background (#FFFFFF): no paper grain, no ground line, no water, no bubbles, no effects, no text, "
        "no labels, no frame, no white sticker border. Exactly one creature, nothing else.")
CHECK = ["Một con, nền trắng, không bóng, không chữ, không viền trắng kiểu sticker.",
         "Bố cục trùng `mau/bo_cuc.png`: đầu to ở góc trên phải nhìn sang phải, THÂN NGẮN cuộn một vòng nhỏ, vây đuôi bên phải, hai cánh nhỏ.",
         "Thân lam nhạt (khác hẳn chàm đậm của dạng 2), bụng kem; KHÔNG có ba vỏ sò trên lưng.",
         "Không có sừng dài: chỉ hai nụ sừng ngắn màu đen than.",
         "Mắt to tròn màu hổ phách, nét mày thẳng: mặt quả quyết, dễ thương, không cười toe, không đáng sợ.",
         "Tô phẳng: không mảng sáng tối, không bóng loáng; chỉ một chấm sáng nhỏ trong mắt."]
FIX = [("Vòng cuộn, đuôi vẫn dài như bản nháp", "The coil and the tail must be as SHORT and tight as in image 2: a small tight coil, a short tail with its fin close behind the chest."),
       ("Vây vẫn dài như bản nháp", "Every fin must be as SHORT as in image 2: shorten the back fins, the ear fins and the tail fin."),
       ("Thân vẫn dài như bản nháp", "The body must be as SHORT and compact as in image 2: do not lengthen the body or widen the loop."),
       ("Có sừng dài như dạng 2", "No long horns: only two short rounded charcoal horn buds on top of the head."),
       ("Thân vẫn chàm đậm", "The body is LIGHT periwinkle blue #6C86DC, clearly lighter than the adult in image 1."),
       ("Đổi dáng, đổi hướng, cánh to lại", "Keep image 2's layout exactly: same pose, same facing, same small wings, same places and sizes."),
       ("Vẫn còn vỏ sò trên lưng", "Remove the scallop shells: the juvenile's back is plain periwinkle."),
       ("Có bóng, mảng sáng tối", "Flat colour only: remove all shading, highlights and shadows."),
       ("Mặt cười hiền như linh vật", "Determined fighter's face: straight brow line, closed beak, focused eye; cute but serious.")]


def main():
    for f in (BO_CUC, LON, NHAP):
        if not os.path.exists(f):
            raise SystemExit("thiếu ảnh mẫu: " + W(f))
    os.makedirs(PK, exist_ok=True)
    os.makedirs(TAI, exist_ok=True)
    out = os.path.join(TAI, "L1_concept.png")
    p = os.path.join(PK, "luot_1_concept.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {W(LON)}: the APPROVED picture of the ADULT form of the creature (a winged sea-serpent dragon), 1536x1024, "
         "white background. Use it for the species, the hand-drawn look, the ink line and the crayon texture.",
         f"image 2 = {W(BO_CUC)}: LAYOUT of the JUVENILE form, 1536x1024, white background: the same creature assembled by a "
         "computer with juvenile proportions (bigger head, small wings) but still wearing the ADULT's skin (deep indigo body, "
         "long black horns, scallop shells). Its pose, proportions (note the SHORT, compact body) and the place of every part "
         "are exact; its skin, colours and horns are NOT final.",
         f"image 3 = {W(NHAP)}: an earlier draft of the juvenile, 1536x1024, white background. Its DESIGN is approved: the round "
         "head with the big amber eye and straight brow, the short blunt charcoal beak, the two short horn buds, the periwinkle "
         "body, the cream belly plates, the pale-aqua wings and fins with dark-blue rays and cream spots, the plain back, the "
         "short fins. Only its BODY LOOP AND TAIL ARE STILL TOO LONG: the coiled rear body and the tail must be as SHORT and "
         "tightly coiled as image 2 shows (image 2 is newer than image 3; follow image 2 for every size and place).",
         "", f"SAVE: save it as a PNG to {W(out)}",
         "If a file with that name already exists, save as L1_concept_2.png, L1_concept_3.png ... in the same folder. Do not "
         "edit, move or delete any other file.", "",
         "TASK: redraw image 2 as ONE finished picture of the juvenile form: the LAYOUT and proportions of image 2 (short compact "
         "body, short fins, small wings), the DESIGN, face and colours of image 3.", ""]
    t += DESIGN + ["", LOOK, "", PAGE]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    gd = [f"# Gói gửi GPT: `{CODE}` (rồng vây non = dạng 1 trong game; tên chưa đặt)", "",
          "Làm 2026-11-12 (người dùng: \"làm dạng 1 đi\"). Hình đang có (`rong_vay_1`, rồng trưởng thành) là dạng 2. Dạng 1 chạy trên "
          "cùng rig, cùng clip, chỉ đổi tỉ lệ (đầu to 1,26; cánh 0,6) và vẽ lại da. Màu và chi tiết dưới đây là ĐỀ XUẤT của Claude, "
          "chờ người dùng duyệt concept. Ghi chú: `ArtGen/Spine/inbox/rong_vay_ghichu.md`.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{W(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{W(out)}` (trùng tên thì `_2`, `_3`…).", "",
          f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/{CODE}/luot_1_concept.txt` (thêm `--note \"...\"` để "
          "sửa nhanh).", "",
          "Lượt 2 (các tờ part đúng khung rig) chỉ dựng sau khi concept được duyệt (`tai_ve/L1_duyet.png`).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{W(LON)}` | Concept đã duyệt của dạng 2 (rồng trưởng thành): thân chàm, sừng đen dài, ba vỏ sò trên lưng, cánh lớn; "
          "1536 × 1024, nền trắng. |",
          f"| 2 | `{W(BO_CUC)}` | Hình bố cục rồng non do rig dựng (khung 0 của idle): đầu to hơn, cánh nhỏ, da còn của dạng 2; "
          "1536 × 1024, nền trắng. Dựng lại: `RV_DANG=non py -3 -I ArtGen/Spine/rong_vay_rig.py bo_cuc <đường dẫn này>`. |",
          f"| 3 | `{W(NHAP)}` | Bản nháp concept rồng non lượt trước (mặt, màu, nụ sừng, vây ngắn đã ưng; vòng cuộn và đuôi còn dài); 1536 × 1024, nền trắng. |",
          "", "Người dùng 2026-11-12 sau bản nháp: \"mặt nhìn non hơn rồi nhưng thân bạn cũng phải làm ngắn hơn\" → rig co thân dọc chiều dài "
          "còn 0,72 (`K_THAN`), bố cục dựng lại. Sau `L1_concept_2`: \"làm vây của nó ngắn hơn chút nữa\" → rig co vây (lưng 0,74; tai 0,80; đuôi 0,82); Sau `L1_concept_3`: \"phần đuôi vẫn dài, thu ngắn các part thân/đuôi lại chút\" → rig: thân trước 0,70, thân sau 0,62, đuôi 0,54; lượt này giữ thiết kế của bản nháp trên bố cục mới.",
          "", "Đề xuất dạng 1: thân lam nhạt `#6C86DC`, bụng kem; mắt to tròn màu hổ phách, mày thẳng; mỏ ngắn tù; hai nụ sừng ngắn; "
          "cánh và vây lam ngọc nhạt `#9CD3D6`; lưng trơn, không vỏ sò.", "", "## Kiểm", ""]
    gd += [f"- {c}" for c in CHECK]
    gd += ["", "## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `--note`)", "", "| Sai | Gửi thêm |", "|---|---|"]
    gd += [f"| {a} | `{b}` |" for a, b in FIX]
    open(os.path.join(PK, "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    print(W(p))
    print(W(os.path.join(PK, "HUONG_DAN.md")))


if __name__ == "__main__":
    main()
