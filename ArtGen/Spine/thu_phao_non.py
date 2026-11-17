# -*- coding: utf-8 -*-
"""Thú giáp pháo non: DẠNG 1 của thú giáp pháo (dạng 2, inbox/thu_phao_1: giáp thép bạc viền vàng, mũ hiệp sĩ), trên CÙNG rig monster_3629.

Người dùng 2026-11-17: "ok làm dạng 1 cho tướng này". Tỉ lệ đổi ở rig trước (thu_phao_rig.py TP_DANG=non: đầu × 1,45, tai × 0,8 (tương
đối), pháo × 0,78, đuôi × 0,85; chân giữ vì bàn chân là đích IK), hình bố cục dựng bằng da dạng 2 làm ảnh mẫu cho concept. KHỐI PHÁO giữ đúng
phối cảnh ba phần tư của bố cục (bài học dạng 2: pháo vẽ phẳng nhìn ngang bị chê "2D quá").

    thu_phao_non.py khung      bố cục (mau/bo_cuc.png) đặt vào khung 1536 × 1024 nền trắng → mau/bo_cuc_khung.png (+ .json)
    thu_phao_non.py concept    ba file prompt concept → gui_gpt/thu_phao_non/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
    thu_phao_non.py dau        lượt 1b (người dùng: "A ổn nhưng cái đầu nhìn không liên quan gì đến dạng 2"): sửa ĐẦU trên bản A cho cùng dòng
                               mũ hiệp sĩ dạng 2, ba kiểu → gui_gpt/thu_phao_non/luot_1b_dau_<1|2|3>.txt → tai_ve/L2_<1|2|3>.png
"""
import json
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "inbox", "thu_phao_non")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
GUI = os.path.join(HERE, "gui_gpt", "thu_phao_non")
DANG2 = os.path.join(HERE, "inbox", "thu_phao_1", "tai_ve", "L1_duyet.png")
W, H = 1536, 1024
MUC = "#2E2012"


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def khung():
    im = Image.open(os.path.join(MAU, "bo_cuc.png")).convert("RGB")
    k = min(900.0 / im.height, 1350.0 / im.width)
    im2 = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    can = Image.new("RGB", (W, H), (255, 255, 255))
    ox, oy = (W - im2.width) // 2, (H - im2.height) // 2
    can.paste(im2, (ox, oy))
    p = os.path.join(MAU, "bo_cuc_khung.png")
    can.save(p)
    json.dump(dict(k=k, ox=ox, oy=oy), open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"k {k:.3f}, lệch {ox},{oy}")


GIU = ("KEEP (they make it the same family line as image 2): a low, wide FOUR-LEGGED armoured beast turned to the right, standing on four "
       "short block legs with short claws; a rounded back shell of overlapping plates; four curved TAIL SCALES curling down at the rear; "
       "and on its back the CANNON EXACTLY AS BUILT IN IMAGE 1, IN THE SAME THREE-QUARTER PERSPECTIVE: a box-shaped housing with a sloping "
       "TOP FACE, a raised block with a round boss on its front face, and a MUZZLE BLOCK whose side face continues the housing and whose "
       "FRONT FRAME holds the glowing arched cannon mouth (the mouth exactly as wide as the front frame allows), a round core ring at the "
       "rear end of the housing, two small wings on top. Same places and sizes as image 1. The glow inside the cannon mouth, the core and "
       "the eyes is flat golden yellow #F8C44C with one pale #EFDFA7 inner shape (no glow, no rays).")

HUONG = {
    "A": ("thú con giáp bạc nhẹ, lộ mặt",
          "vẫn bạc viền vàng như dạng 2 nhưng GIÁP NHẸ: ít tấm, ít đinh, viền vàng mảnh; mũ đổi dáng: MŨ TRÒN HỞ MẶT (như nồi sắt úp) lộ MẶT "
          "THÚ CON: da xanh xám đá, mắt tròn to vàng, mõm nhỏ có hai lỗ mũi; hai tai giáp thành hai tai thú ngắn tròn bọc viền vàng; pháo cùng "
          "dáng, bạc viền vàng mảnh",
          ["ARMOUR: the same family colours as image 2 (flat silver #C6C9D1 on faces turned to the viewer, darker silver #9BA0AB on side "
           "faces, gold #DFAD46 trims) but LIGHTER ARMOUR: thinner gold trims, only ONE rivet or none on each plate, simpler plates.",
           "HEAD: a NEW SHAPE, not the closed knight helm of image 2: a ROUND OPEN-FACED silver helmet (like a small upturned iron pot with a "
           "thin gold rim) that shows the FACE of a young beast under it: slate blue-grey skin #7C8C9E, TWO BIG ROUND golden-yellow eyes "
           "#F8C44C with dark pupils and one small white dot each, determined small brows, a short rounded snout with two small nostrils "
           "and a small closed mouth. The head is the same size and in the same place as in image 1.",
           "EARS: the two tall pointed ear guards become TWO SHORT ROUNDED beast EARS sticking out of the helmet, slate blue-grey with a thin "
           "gold rim (in the same places, shorter).",
           "CANNON: exactly the shape of image 1, silver with thinner gold trims; the two small wings stay; the round core a gold ring with "
           "a small golden sun."]),
    "B": ("đồng thau học việc",
          "giáp ĐỒNG THAU sáng + khớp thép; mũ tròn kín đồng thau một khe mắt ngang, hai mắt vàng nhỏ xếch; hai tai thành hai núm sừng đồng "
          "ngắn; pháo đồng thau đai thép; cánh thành hai vây đồng nhỏ",
          ["ARMOUR: polished-looking but FLAT BRASS armour: flat brass #D9B060 on faces turned to the viewer, darker brass #B08A40 on side "
           "faces, and plain steel #9BA0AB joints and bands; very few rivets.",
           "HEAD: a NEW SHAPE, not the knight helm of image 2: a ROUND closed brass helmet like a small diving helmet with ONE horizontal eye "
           "slit, TWO small slanted golden eyes #F8C44C with one white dot each in the slit, a short steel band round its middle.",
           "EARS: the two tall ear guards become TWO SHORT stubby brass HORN STUDS on top of the helmet (in the same places, much shorter).",
           "CANNON: exactly the shape of image 1, brass with two steel bands; the two wings become two small flat brass fins."]),
    "C": ("giáp gỗ đai sắt sơ khai",
          "giáp GỖ SÁNG đai sắt đinh tán (như được đóng tạm cho thú non); mũ gỗ hình thùng nhỏ khoét hai lỗ mắt tròn, mắt vàng; hai tai thành "
          "hai chốt gỗ; pháo gỗ đóng đai sắt, khung họng sắt; vuốt sắt",
          ["ARMOUR: LIGHT WOOD plates #C99A5B (darker wood #A87A42 on side faces) held by plain dark iron bands #64656A with a few iron "
           "rivets, like armour hammered together for a young beast; the claws plain dark iron.",
           "HEAD: a NEW SHAPE, not the knight helm of image 2: a small round WOODEN BUCKET helmet with an iron rim and TWO ROUND EYE HOLES, "
           "TWO big round golden eyes #F8C44C with one white dot each looking out of them.",
           "EARS: the two tall ear guards become TWO short wooden pegs (in the same places, much shorter).",
           "CANNON: exactly the shape of image 1, made of wooden planks bound by iron bands, the front frame of the muzzle plain dark iron "
           "around the glowing mouth; the two wings become two small wooden fins; the round core an iron ring with a small golden sun."]),
}

STYLE = (f"DRAWING STYLE: exactly the hand-drawn style of image 2: a wobbly dark-brown ink outline ({MUC}, about 7 px) round every piece, "
         "thin ink lines for the few inner lines (face / side edges of the blocks), every area ONE flat colour with visible coloured-pencil "
         "/ wax-crayon hatching. No shading, no highlights, no white shine streaks, no gradients, no glow, no shadows. VERY SIMPLE DESIGN, "
         "FEW DETAILS: nothing beyond what is listed.")


def concept():
    bc = os.path.join(MAU, "bo_cuc_khung.png")
    R = [(bc, "the POSE AND PROPORTION GUIDE, 1536x1024, white background: OUR armoured cannon beast redrawn by computer at the "
              "proportions of its YOUNG first form (a much bigger head, a smaller cannon, a shorter tail), still wearing the armour of its "
              "final form (small seams between pieces are only computer artefacts). It gives the exact POSE, the PROPORTIONS, the "
              "THREE-QUARTER PERSPECTIVE of every block and the PLACE and SIZE of every part: head, ears, shell plates, four legs, claws, "
              "tail scales, cannon housing, muzzle block, core, wings. Keep them. Change the materials and the head as described.",
          "Hình bố cục dạng 1 (1536 × 1024, nền trắng): rig dạng 2 đổi tỉ lệ (đầu × 1,45, tai ngắn, pháo × 0,78, đuôi × 0,85), da tạm dạng 2. "
          "Giữ dáng, tỉ lệ, phối cảnh ba phần tư từng khối, chỗ và cỡ từng bộ phận"),
         (DANG2, "the APPROVED FINAL FORM of the same character (a siege beast in silver-white knight armour with gold rims, a knight helm "
                 "with a T-shaped visor and yellow eyes, tall pointed ear guards, a cannon on its back), 1536x1024, white background. It "
                 "gives the hand-drawn style. The young form must look clearly YOUNGER, CUTER and LESS ARMOURED, but of the same family "
                 "line. NOTE: image 2 draws the cannon flat from the side; do NOT copy that, keep the three-quarter cannon of image 1.",
          "Concept dạng 2 đã duyệt (bạc viền vàng, mũ hiệp sĩ): lấy nét vẽ và nét chung của dòng; dạng 1 non hơn, ít giáp hơn; pháo theo "
          "ảnh 1, không theo pháo phẳng của ảnh này")]
    hd = ["# Gói GPT: thú giáp pháo non, dạng 1 (thu_phao_non), tướng 9 đảo Kim", "",
          "## Lượt 1: concept dạng 1, ba hướng (2026-11-17)", "",
          "Dạng vừa làm (giáp bạc viền vàng, mũ hiệp sĩ) là dạng 2. Dạng 1 trên cùng rig: tỉ lệ đã đổi ở rig (đầu × 1,45, tai × 0,8, pháo "
          "× 0,78, đuôi × 0,85). Ba hướng giữ: thú bốn chân thấp, mai, bốn vảy đuôi, khẩu pháo ba phần tư y như bố cục (thân hộp, khối họng, "
          "lõi, hai cánh), lòng sáng vàng; đổi đầu và chất liệu cho non hơn.", "",
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
              "TASK: draw the YOUNG FIRST FORM of our armoured cannon beast as ONE picture: the SAME pose, proportions and three-quarter "
              "perspective as image 1, every part in the same place and at the same size (if the new picture were laid over image 1, the "
              "head, ears, shell, legs, claws, tail scales and every block of the cannon must coincide), but the new materials and the new "
              "head described below, in the drawing style of image 2.", "",
              GIU, "",
              "CHANGE:"] + [f"- {d}" for d in doi] + ["",
              STYLE, "",
              "Mood: a young armoured beast, small but stubborn and ready to fight (a game hero's first form), determined eyes; cute but not "
              "a mascot, not scary. All four feet stand on the ground; the cannon mouth points to the right.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same place "
              "and size as in image 1. No sparkles, no dust, no glow, no smoke, no speed lines, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, tỉ lệ, chỗ và cỡ từng bộ phận như ảnh 1; khẩu pháo GIỮ phối cảnh ba phần tư (mặt trên, mặt bên, khung mặt trước "
           "chứa miệng sáng) như ảnh 1, không vẽ phẳng nhìn ngang; vẫn nhận ra cùng dòng với ảnh 2; tô phẳng, không bóng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"keep the cannon exactly as in image 1, three-quarter view\"; \"same pose and size as image 1\"; \"flat colours "
           "only, no shading, no glow\"."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


# ---------------------------------------------------------------- lượt 1b: đầu cùng dòng với dạng 2
DAU = {
    "1": ("mũ hiệp sĩ non khép, mắt tròn to",
          "HEAD: the SAME KIND of helmet as the final form in image 2, a silver KNIGHT HELM with the T-SHAPED VISOR SLIT, gold rims and a gold "
          "crest ridge, but YOUNGER: rounder and softer (a big round dome, no sharp angles), the gold crest only a SHORT rounded stub on top, "
          "the T-slit WIDER and shorter so that TWO BIG ROUND golden-yellow eyes #F8C44C (dark pupils, one small white dot each, small "
          "determined brows drawn on the visor) look out of the horizontal bar of the T. Same place and size as the head of image 1.",
          "EARS: the two short rounded ears become TWO SHORT pointed armour EAR GUARDS like those of image 2 but stubby and rounded at the "
          "tip, silver with a gold rim, same places as in image 1."),
    "2": ("mũ hiệp sĩ mở tấm che, lộ mặt thú con",
          "HEAD: the SAME knight helm as the final form in image 2 (silver, gold rims, gold crest ridge, the visor with the T-shaped slit) "
          "but its VISOR IS RAISED: the visor plate is pushed up onto the forehead of the helm, and under it the FACE of the young beast of "
          "image 1 shows (slate blue-grey skin #7C8C9E, two big round golden-yellow eyes #F8C44C with dark pupils and one small white dot "
          "each, determined small brows, a short rounded snout with two nostrils). The helm is rounder and a little too big for the young "
          "beast. Same place and size as the head of image 1.",
          "EARS: the two short rounded ears become TWO SHORT pointed armour EAR GUARDS like those of image 2 but stubby, silver with a gold "
          "rim, same places as in image 1."),
    "3": ("mũ hiệp sĩ khoét chữ T, mặt thú nhìn qua",
          "HEAD: the SAME knight helm as the final form in image 2 (silver, gold rims, a short gold crest ridge), rounder and younger, whose "
          "T-SHAPED opening is cut WIDE: through the opening the FACE of the young beast of image 1 shows (slate blue-grey skin #7C8C9E): the "
          "two big round golden-yellow eyes #F8C44C (dark pupils, one small white dot each, determined brows) in the horizontal bar of the "
          "T, the short rounded snout with two nostrils in the vertical bar. Same place and size as the head of image 1.",
          "EARS: the two short rounded ears become TWO SHORT pointed armour EAR GUARDS like those of image 2 but stubby, silver with a gold "
          "rim, same places as in image 1."),
}


def dau():
    a = os.path.join(TAI, "L1_A.png")
    R = [(a, "the DRAFT to edit (the chosen young form A), 1536x1024, white background: the young armoured cannon beast in light silver "
             "armour with gold trims, a round open-faced helmet showing a slate blue-grey beast face, two short rounded ears, a three-quarter "
             "box cannon on its back. Keep EVERYTHING of it except the head and the ears."),
         (DANG2, "the APPROVED FINAL FORM of the same character, 1536x1024: look at its HEAD: a silver knight helm with a T-shaped visor "
                 "slit, two slanted yellow eyes, a gold crest ridge, gold rims, two tall pointed armour ear guards. The young form's head "
                 "must clearly belong to the same family line: the same KIND of knight helm, younger. Its cannon is drawn flat from the "
                 "side: ignore its cannon.")]
    hd = ["", "## Lượt 1b: sửa đầu bản A cho cùng dòng dạng 2 (2026-11-17)", "",
          "Người dùng: \"A ổn nhưng cái đầu nhìn không liên quan gì đến dạng 2, sửa lại đi\". Ảnh mẫu 1 = bản A (giữ y nguyên, chỉ đổi đầu "
          "+ tai), ảnh 2 = dạng 2 (lấy kiểu mũ hiệp sĩ).", ""]
    for k, (vi, d1, d2) in DAU.items():
        out = os.path.join(TAI, f"L2_{k}.png")
        p = os.path.join(GUI, f"luot_1b_dau_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L2_{k}_2.png, L2_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "",
              "TASK: EDIT image 1. Redraw image 1 IDENTICALLY (if the new picture were laid over image 1, everything must coincide), and "
              "change ONLY the head and the two ears as described below.", "",
              "KEEP IDENTICAL: the pose, the size and place of the character; the back shell plates and their gold trims; the four legs and "
              "claws; the dark belly; the four tail scales; the WHOLE CANNON (the box housing with its top face and raised block, the muzzle "
              "block with the gold front frame and the glowing mouth, the round core, the two small wings) in the same three-quarter view; "
              "the colours; the drawing style.", "",
              "CHANGE ONLY:", f"- {d1}", f"- {d2}", "",
              "The head must look like a YOUNGER version of the head of image 2: same family, cuter and rounder, determined, ready to fight; "
              "not a mascot.", "",
              f"STYLE: exactly the style of image 1: wobbly dark-brown ink outline ({MUC}, about 7 px), thin ink lines for the few inner lines, "
              "every area ONE flat colour with visible crayon hatching. No shading, no highlights, no gradients, no glow, no shadows.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Kiểu {k}** ({vi}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    hd_p = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd_p, encoding="utf-8").read().split("\n## Lượt 1b")[0].rstrip("\n")
    ghi(hd_p, (cu + "\n" + "\n".join(hd)).split("\n"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "khung":
        khung()
    elif cmd == "concept":
        concept()
    elif cmd == "dau":
        dau()
    else:
        print(__doc__)
