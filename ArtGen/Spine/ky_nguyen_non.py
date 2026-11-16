# -*- coding: utf-8 -*-
"""Vong Kỵ Nhi: DẠNG 1 (kỵ sĩ non) của kỵ sĩ cổ đại bị nguyền (dạng 2, inbox/ky_nguyen_1), trên CÙNG rig monster_3642.

Người dùng 2026-11-16: "ok cho vào game, làm thêm các fx hiệu ứng nữa rồi làm dạng 1 của tướng này". Tỉ lệ đổi ở rig trước
(ky_nguyen_rig.py KN_DANG=non: đầu × 1,4, lửa trên mũ thu lại, tay × 0,85, bàn tay × 1,1, giáp vai × 0,8, kiếm × 0,8, áo choàng × 0,85),
hình bố cục dựng bằng da dạng 2 làm ảnh mẫu cho concept. KIẾM GIỮ NGUYÊN hình dạng 2 (cùng vết gãy): chiêu cuối vá kiếm dùng lại phần vá.

    ky_nguyen_non.py khung      bố cục (mau/bo_cuc.png) đặt vào khung 1536 × 1024 nền trắng → mau/bo_cuc_khung.png (+ .json)
    ky_nguyen_non.py concept    ba file prompt concept → gui_gpt/ky_nguyen_non/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
"""
import json
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "inbox", "ky_nguyen_non")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
GUI = os.path.join(HERE, "gui_gpt", "ky_nguyen_non")
DANG2 = os.path.join(HERE, "inbox", "ky_nguyen_1", "tai_ve", "L1_duyet.png")
W, H = 1536, 1024
MUC = "#2B2118"


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def khung():
    im = Image.open(os.path.join(MAU, "bo_cuc.png")).convert("RGB")
    k = 960.0 / im.height
    im2 = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    can = Image.new("RGB", (W, H), (255, 255, 255))
    ox, oy = (W - im2.width) // 2, (H - im2.height) // 2
    can.paste(im2, (ox, oy))
    p = os.path.join(MAU, "bo_cuc_khung.png")
    can.save(p)
    json.dump(dict(k=k, ox=ox, oy=oy), open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"k {k:.3f}, lệch {ox},{oy}")


GIU = ("KEEP (they make it the same family line as image 2): a HOLLOW suit of black rusty iron armour with NO body inside and NO legs, "
       "floating; the dark void inside (near-black #1F2321) with small GREEN SOUL FIRE tongues along its edges; the two narrow slanted eyes "
       "flat bright green #B6FF7A with one small white dot each (no glow); the blackened iron colours (flat dark iron #3A3C44 on the faces "
       "turned to the viewer, darker iron #26272D on the faces turned away); the dark wine-red cloth (#5E2430 tabard, #4E1F2A cape); the "
       "open black iron gauntlet on the right, reaching forward; the five small pieces floating under the chest; and the SWORD EXACTLY AS IN "
       "IMAGE 1: the same black-iron blade broken off with the same jagged broken end, the same rust patches, the same straight crossguard "
       "with a ring round the base of the blade, the same green gem in the pommel, the same size and place, held by the near fist.")

FIRE = ("GREEN SOUL FIRE is drawn as flat flame shapes with the same ink outline, in TWO flat tones only: bright soul green #8FEA5E outside "
        "and pale green #D6FFA8 for one simple inner tongue. No glow, no halo, no light rays, no gradient.")

HUONG = {
    "A": ("cận vệ tập sự",
          "mũ sắt TRÒN thấp (mũ chỏm cầu), một khe mắt ngang; trên đỉnh một túm lửa xanh nhỏ năm lưỡi; giáp ít rỉ (1–2 mảng nhỏ mỗi tấm), "
          "viền đồng xỉn mảnh; giáp vai MỘT tấm tròn trơn; giáp ngực trơn có một vết nứt nhỏ lộ lửa; KHÔNG mũi tên, không giáo; vạt và áo "
          "choàng đỏ rượu ngắn, mép rách ít; mảnh bay dưới thân là mảnh sắt vụn",
          ["HELMET: a NEW SHAPE, not the crowned helm of image 2: a LOW ROUND iron helmet like a dome (a simple bascinet) with ONE horizontal "
           "eye slit across its front (the two green eyes in it), one thin dull-bronze #7A6440 band round its lower rim. NO crown, no points.",
           "FLAME CREST: on the very top of the dome a SMALL TUFT of green soul fire: five SHORT flame tongues in the same places and "
           "directions as the five flames of image 1 but clearly smaller and rounder, like a young flame.",
           "RUST: the armour is LESS rusty than image 2: only ONE or TWO small rounded rust patches #A4532B on each big plate, no rust along "
           "the edges.",
           "BIG SHOULDER: a NEW SHAPE: ONE plain rounded iron plate (a simple dome) with a thin dull-bronze rim, no broken edge, no flanges.",
           "CHEST PLATE: a plain breastplate with ONE SHORT crack in its middle; a little green fire shows through the crack.",
           "NO WEAPONS STUCK IN THE ARMOUR: no arrows, no spear, nothing sticking out of the shoulder, the arm or the chest (it has not "
           "fought its great battles yet). The near vambrace plain with ONE small green rune (a circle with a line through it).",
           "TABARD and CAPE: dark wine-red, SHORTER than in image 2, with only a few small tears at the lower edge and a thin dull-bronze "
           "border.",
           "FLOATING PIECES: five small plain iron SHARDS floating under the chest."]),
    "B": ("hiệp sĩ giáp vá",
          "mũ trụ CHÓP NHỌN có thanh che mũi giữa hai mắt; lửa xanh phụt ra từ chóp như chùm lông; giáp VÁ chằng (đinh tán, dây da buộc); "
          "giáp vai là tấm sắt tròn buộc dây da; MỘT mũi tên gãy cắm trên giáp vai; vạt đỏ rượu ngắn, áo choàng ngắn rách; mảnh bay là "
          "mảnh khiên gỗ bịt sắt",
          ["HELMET: a NEW SHAPE, not the crowned helm of image 2: a POINTED conical iron helm (a simple spangenhelm) with a short NOSE GUARD "
           "bar running down between the two green eyes; a few rivets round its rim. NO crown.",
           "FLAME CREST: the five flames become a SMALL PLUME of green soul fire streaming back from the tip of the helm (five short tongues "
           "in the same places and directions as in image 1, clearly smaller).",
           "PATCHED ARMOUR: the iron plates are mismatched and PATCHED: a few round rivets, one or two brown leather straps #6A4030 with "
           "small iron buckles holding plates together; only one or two small rust patches #A4532B per plate.",
           "BIG SHOULDER: a NEW SHAPE: a round iron plate like a small buckler, strapped to the shoulder with a brown leather strap; no "
           "flanges.",
           "CHEST PLATE: a plain breastplate with one riveted iron patch on it and a thin crack beside the patch; a little green fire shows "
           "through the crack.",
           "WEAPONS STUCK IN THE ARMOUR: only ONE short BROKEN ARROW (wooden shaft, grey fletching) stuck in the big shoulder, pointing up and "
           "to the left; no spear, nothing else sticking out.",
           "TABARD and CAPE: dark wine-red, SHORTER than in image 2, plain edges with a few tears.",
           "FLOATING PIECES: five small pieces of a broken WOODEN SHIELD with iron rims floating under the chest."]),
    "C": ("mũ thùng sứt, hồn non",
          "mũ thùng đỉnh phẳng hơi quá cỡ, MÓP một góc, khe mắt chữ thập, không vương miện; lửa xanh nhỏ lách ra từ khe đỉnh; giáp mỏng, "
          "KHE HỞ lộ lửa xanh nhiều hơn; giáp vai nhỏ mép răng cưa hai tấm; một mũi tên gãy ở cẳng tay; vạt và áo choàng đỏ rượu rách tua "
          "ngắn; mảnh bay là đá đen có vệt nứt xanh",
          ["HELMET: a NEW SHAPE, not the crowned helm of image 2: a flat-topped BUCKET helm, a little too big for the body, with ONE DENT in "
           "its upper right corner and a CROSS-shaped eye slit (the two green eyes in the horizontal slit). NO crown, no points.",
           "FLAME CREST: the five flames become SMALL green flame tongues slipping out of a thin gap along the top rim of the bucket (same "
           "places and directions as in image 1, clearly smaller).",
           "MORE SOUL SHOWING: the armour plates are thinner and leave WIDER GAPS between them where the void shows, with more small green "
           "flame tongues along the gaps. Only one or two small rust patches #A4532B per plate.",
           "BIG SHOULDER: a NEW SHAPE: TWO small overlapping iron plates with a jagged saw-tooth lower rim.",
           "CHEST PLATE: a plain breastplate with a small notch in its upper edge.",
           "WEAPONS STUCK IN THE ARMOUR: only ONE short BROKEN ARROW stuck in the near forearm; no spear, nothing else sticking out.",
           "TABARD and CAPE: dark wine-red, SHORTER than in image 2, the lower edge torn into short tatters.",
           "FLOATING PIECES: five small black rocks with one thin green crack line each."]),
}

STYLE = (f"DRAWING STYLE: exactly the hand-drawn style of image 2: a wobbly dark-brown ink outline ({MUC}, about 7 px) round every piece, "
         "thin ink lines for the few inner lines, every area ONE flat colour with visible coloured-pencil / wax-crayon hatching. No shading, "
         "no highlights, no white shine streaks, no gradients, no glow, no shadows. VERY SIMPLE DESIGN, FEW DETAILS: nothing beyond what is "
         "listed.")


def concept():
    bc = os.path.join(MAU, "bo_cuc_khung.png")
    R = [(bc, "the POSE AND PROPORTION GUIDE, 1536x1024, white background: OUR cursed knight redrawn by computer at the proportions of its "
              "YOUNG first form (a much bigger helmet, shorter arms, a smaller shoulder plate, a smaller sword, a shorter cape), still wearing "
              "the armour of its final form (small seams between pieces are only computer artefacts). It gives the exact POSE, the "
              "PROPORTIONS and the PLACE and SIZE of every part: helmet, eyes, flames, shoulder, chest, near arm and fist, sword, far arm "
              "and open hand, tabard, cape, floating pieces. Keep them. Change the outfit as described.",
          "Hình bố cục dạng 1 (1536 × 1024, nền trắng): rig dạng 2 đổi tỉ lệ (đầu × 1,4, lửa nhỏ, tay × 0,85, giáp vai, kiếm nhỏ lại, áo "
          "choàng ngắn), da tạm dạng 2. Giữ dáng, tỉ lệ, chỗ và cỡ từng bộ phận; kiếm giữ y nguyên"),
         (DANG2, "the APPROVED FINAL FORM of the same character (a floating hollow knight in black rusty iron armour with a jagged iron "
                 "crown on its helm and green soul fire rising out of it, broken arrows and a broken spear stuck in the armour, a dark "
                 "wine-red cape and a broken sword), 1536x1024, white background. The young form must look clearly YOUNGER, SMALLER and "
                 "LESS BATTLE-WORN, but of the same family line.",
          "Concept dạng 2 đã duyệt (vua chiến trận cổ): lấy nét vẽ, màu giáp sắt đen, lửa hồn xanh, mắt xanh, vải đỏ rượu; dạng 1 non hơn, "
          "ít vết trận hơn, không vương miện")]
    hd = ["# Gói GPT: Vong Kỵ Nhi, dạng 1 của kỵ sĩ cổ đại bị nguyền (ky_nguyen_non), tướng 8 đảo Kim", "",
          "## Lượt 1: concept dạng 1, ba hướng (2026-11-16)", "",
          "Dạng vừa làm (vua chiến trận cổ, concept C) là dạng 2. Dạng 1 trên cùng rig: tỉ lệ đã đổi ở rig (đầu × 1,4, lửa trên mũ nhỏ, tay "
          "× 0,85, bàn tay × 1,1, giáp vai × 0,8, kiếm × 0,8, áo choàng × 0,85). Ba hướng giữ: giáp rỗng lơ lửng, khoảng rỗng tối có lửa hồn "
          "xanh, mắt xanh, sắt đen, vải đỏ rượu, găng mở bên phải, kiếm gãy y như dạng 2 (để chiêu cuối vá kiếm dùng lại phần vá). Bỏ vương "
          "miện, bớt rỉ, bớt hoặc bỏ mũi tên, mũ đổi dáng.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out = os.path.join(TAI, f"L1_{k}.png")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "",
              "TASK: draw the YOUNG FIRST FORM of our cursed knight as ONE picture: the SAME pose and proportions as image 1, every part in "
              "the same place and at the same size (if the new picture were laid over image 1, the helmet, eyes, flames, shoulder, chest, "
              "arms, fists, sword, tabard, cape and floating pieces must coincide), but a new, lighter outfit described below, in the "
              "drawing style of image 2.", "",
              GIU, "",
              FIRE, "",
              "CHANGE:"] + [f"- {d}" for d in doi] + ["",
              STYLE, "",
              "Mood: a young cursed knight just risen, small but stubborn and ready to fight (a game hero's first form), determined eyes; "
              "cute but not a mascot, not scary: no skulls, no bones, no blood. Both arms stay attached to the body exactly as in image 1; "
              "the near fist really grips the sword; the far hand is open, reaching forward; no legs, the cape hangs down.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same place "
              "and size as in image 1. No sparkles, no dust, no glow, no speed lines, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, tỉ lệ, chỗ và cỡ từng bộ phận như ảnh 1; kiếm y như ảnh 1 (cùng vết gãy); vẫn nhận ra cùng dòng với ảnh 2 (giáp "
           "sắt đen rỗng, lửa hồn xanh, mắt xanh, vải đỏ rượu); không vương miện, ít vết trận hơn; tô phẳng, không bóng; tay nắm chuôi kiếm; "
           "nền trắng tinh.", "",
           "Câu sửa nhanh: \"keep the sword exactly as in image 1\"; \"the helmet must be a new shape, no crown\"; \"flat colours only, no "
           "shading, no glow\"; \"same pose and size as image 1\"."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "khung":
        khung()
    elif cmd == "concept":
        concept()
    else:
        print(__doc__)
