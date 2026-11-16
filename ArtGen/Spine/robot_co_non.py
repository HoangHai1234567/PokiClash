# -*- coding: utf-8 -*-
"""Robot hủy diệt cổ đại DẠNG 1 NON (robot_co_non): dạng trước của robot sắt cổ gỉ sét (dạng 2, inbox/robot_co_1), trên CÙNG rig monster_3613.

Người dùng 2026-11-16 (xem rig dạng 2): "ok ổn rồi làm dạng 1 đi" → như quỷ xích: dạng vừa làm là dạng 2 (dạng cuối), làm thêm dạng 1 non. Tỉ
lệ đổi ở rig trước (robot_co_rig.py RC_DANG=non: giáp vai × 0,82, cẳng tay + nắm đấm × 0,88, ống xả × 0,72), hình bố cục dựng bằng da dạng 2
làm ảnh mẫu cho concept. Đầu vòm nằm chung mảnh cứng với thân nên không phóng bằng xương: concept vẽ đầu to tròn hơn (mảnh thân gen lại).

    robot_co_non.py khung      bố cục (mau/bo_cuc.png) đặt vào khung 1536 × 1024 nền trắng → mau/bo_cuc_khung.png (+ .json)
    robot_co_non.py concept    ba file prompt concept → gui_gpt/robot_co_non/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
"""
import json
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "inbox", "robot_co_non")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
GUI = os.path.join(HERE, "gui_gpt", "robot_co_non")
DANG2 = os.path.join(HERE, "inbox", "robot_co_1", "tai_ve", "L1_duyet.png")
W, H = 1536, 1024
MUC = "#2B2118"


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def khung():
    im = Image.open(os.path.join(MAU, "bo_cuc.png")).convert("RGB")
    k = 900.0 / im.height
    im2 = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    can = Image.new("RGB", (W, H), (255, 255, 255))
    ox, oy = (W - im2.width) // 2, (H - im2.height) // 2
    can.paste(im2, (ox, oy))
    p = os.path.join(MAU, "bo_cuc_khung.png")
    can.save(p)
    json.dump(dict(k=k, ox=ox, oy=oy), open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"k {k:.3f}, lệch {ox},{oy}")


GIU = ("KEEP (they make it the same family line as image 2): the front-facing crouching robot pose with both fists resting on the ground, "
       "the rounded DOME head with ONE round amber eye #E8A33F (flat, a small white dot, no glow) inside a small square VISOR with a little "
       "grille of slots under the eye, the short neck with a row of small round holes, the TWO curved CHEST PLATES meeting in the middle "
       "round the small round amber light, the round dark lower body with the two pale curved plates on its sides, the huge round barrel "
       "FOREARMS with the round FIST SOCKET (amber ring) and three thick dark fingers on each hand, the short dark legs, the strips hanging "
       "from the waist, the shoulder pads and the small exhaust pipes on the shoulders.")

YOUNG = ("YOUNG FORM PROPORTIONS: the HEAD is clearly BIGGER and ROUNDER than in image 1 (the dome about 1.3 times as big, growing upward "
         "and to both sides from the neck, the visor and the eye a bit bigger too), the fin on top only a short rounded stub. Everything "
         "else stays at the place and size of image 1 (shoulder pads, pipes, chest plates, forearms, fists, legs, strips).")

HUONG = {
    "A": ("robot con thép mới",
          "thép sáng mới đúc, KHÔNG gỉ; mỗi vai MỘT ống xả nhỏ; giáp vai tròn nhỏ hai đinh; đầu vòm to tròn, vây thành mẩu nhỏ, mắt hổ phách to; "
          "giáp ngực trơn hai đinh; vải eo thành vải bố vàng nhạt; cẳng tay một đai",
          [f"METAL: bright NEW light steel #A9AEB6 on the main faces, a lighter steel #C9CDD3 for rims and bands, NO rust at all (it is "
           f"freshly built); the inner body, the legs, the fingers and the inside of the fist sockets dark iron #4A4B50.",
           "PIPES: only ONE small short exhaust pipe on each shoulder (a stubby tube with a thick rim), light steel.",
           "SHOULDER PADS: small smooth rounded steel pads with only two round rivets each.",
           "CHEST PLATES: plain steel, one rim along the inner curve, two rivets each.",
           "FOREARMS: the same round barrel shape in light steel with ONE plain band; the fist socket with an amber ring.",
           "WAIST: the strips become three short strips of pale khaki canvas cloth #CDB98A with a stitched hem (no leather, no rivets).",
           "LEGS: dark iron with a small steel plate on the outer side and a tiny rounded cap on top (no spike)."]),
    "B": ("robot đồng thau học việc",
          "đồng thau vàng ấm + khớp sắt sẫm, sạch bóng không gỉ; mỗi vai một ống còi đồng nhỏ; đầu vòm đồng to tròn có ăng-ten nhỏ thay vây; "
          "giáp vai đồng tròn viền sắt; giáp ngực đồng; vải eo thành dải da nâu sáng ngắn; mắt hổ phách to",
          ["METAL: warm BRASS #C9A05A on the main faces, darker brass #9E7A3E on the faces turned away, dark iron #4A4B50 for the inner body, "
           "the joints, the legs and the fingers. No rust, no stains (flat colour only).",
           "HEAD: instead of the fin, a short thin ANTENNA with a small round brass ball on its tip on top of the bigger brass dome.",
           "PIPES: one small brass WHISTLE pipe on each shoulder (a short tube that flares a little at its open top).",
           "SHOULDER PADS: small rounded brass pads with a dark iron rim, no rivets.",
           "CHEST PLATES: plain brass with a dark iron rim along the inner curve.",
           "FOREARMS: brass barrel shells with one dark iron band; the fist socket with an amber ring.",
           "WAIST: three short light brown leather strips #9A6A45 with one small brass stud each.",
           "LEGS: dark iron with a brass plate on the outer side, a small brass cap on top (no spike)."]),
    "C": ("robot gỗ đai sắt sơ khai",
          "nguyên mẫu đầu tiên: thân gỗ sáng ghép tấm, đai sắt và đinh tán; đầu vòm gỗ to có vành sắt, vây thành chốt gỗ ngắn; mỗi vai một ống "
          "phễu sắt nhỏ; giáp vai gỗ viền sắt; giáp ngực gỗ hai đinh sắt; vải eo thành dây thừng buộc; mắt hổ phách to",
          ["MATERIALS: the big armour plates (dome, shoulder pads, chest plates, forearms) are pale WOOD #C49A6C with two or three thin plank "
           "lines, held by dark iron BANDS #55565C with round rivets; the inner body, the joints, the legs and the fingers dark iron #4A4B50; "
           "the visor dark iron. No rust.",
           "HEAD: the bigger dome is wood with an iron band round its lower rim; instead of the fin a short round WOODEN PEG on top.",
           "PIPES: one small iron FUNNEL pipe on each shoulder (a short tube that widens at its top).",
           "SHOULDER PADS: small rounded wooden pads with an iron rim and one rivet.",
           "CHEST PLATES: wooden with an iron rim along the inner curve and two iron rivets.",
           "FOREARMS: wooden barrel shells with two iron bands; the fist socket iron with an amber ring.",
           "WAIST: instead of the leather straps, two short ROPES #B08A55 hanging down with knotted ends.",
           "LEGS: dark iron with a small wooden plate on the outer side, a rounded iron cap on top (no spike)."]),
}

STYLE = (f"DRAWING STYLE: exactly the hand-drawn style of image 2: a wobbly dark-brown ink outline ({MUC}, about 7 px) round every piece, "
         "thin ink lines for the few inner lines, every area ONE flat colour with visible coloured-pencil / wax-crayon hatching. No shading, "
         "no highlights, no white shine streaks, no gradients, no glow, no shadows. VERY SIMPLE DESIGN, FEW DETAILS: nothing beyond what is "
         "listed.")


def concept():
    bc = os.path.join(MAU, "bo_cuc_khung.png")
    R = [(bc, "the POSE AND PROPORTION GUIDE, 1536x1024, white background: OUR robot redrawn by computer at the proportions of its YOUNG "
              "first form (smaller shoulder pads, shorter pipes, slightly smaller forearms and fists), still painted with the look of its "
              "final form. It gives the exact POSE and the PLACE and SIZE of every body part. Keep them (except the bigger head described "
              "below). Change the look as described.",
          "Hình bố cục dạng non (1536 × 1024, nền trắng): rig dạng 2 đổi tỉ lệ (giáp vai × 0,82, cẳng tay + nắm đấm × 0,88, ống xả × 0,72), da "
          "tạm dạng 2. Giữ dáng, chỗ và cỡ từng bộ phận (trừ đầu vẽ to hơn)"),
         (DANG2, "the APPROVED FINAL FORM of the same character (a heavy ancient war robot of rusty gunmetal iron: a dome helmet with a tall fin, "
                 "a square visor with one amber eye, two exhaust pipes on each shoulder, big riveted shoulder pads, riveted chest plates, "
                 "leather straps, huge riveted barrel forearms), 1536x1024, white background. The young form must look clearly YOUNGER, "
                 "SMALLER-ARMOURED and NEWER, but of the same family line.",
          "Concept dạng 2 đã duyệt (robot sắt cổ gỉ sét): lấy nét vẽ, mắt, mặt nạ, dáng; dạng 1 phải non hơn, ít giáp hơn, mới hơn")]
    hd = ["# Gói GPT: robot hủy diệt cổ đại dạng 1 non (robot_co_non), tướng 7 đảo Kim", "",
          "## Lượt 1: concept dạng 1 non, ba hướng (2026-11-16)", "",
          "Người dùng: \"ok ổn rồi làm dạng 1 đi\": robot sắt gỉ vừa làm là dạng 2; làm thêm dạng 1 non trên cùng rig. Tỉ lệ đã đổi ở rig (giáp vai "
          "× 0,82, cẳng tay + nắm đấm × 0,88, ống xả × 0,72); đầu vẽ to tròn hơn ở concept. Ba hướng: giữ dáng, một mắt hổ phách trong mặt nạ "
          "vuông, giáp ngực ôm đèn tròn, cẳng tay thùng, ổ nắm đấm; mới hơn, ít giáp hơn, sáng màu hơn dạng 2.", "",
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
              "TASK: draw the YOUNG FIRST FORM of our robot as ONE picture: the SAME pose as image 1, every body part in the same place and "
              "at the same size (if the new picture were laid over image 1, the shoulder pads, pipes, chest plates, forearms, fists, "
              "fingers, legs and waist strips must coincide), but a new, lighter and newer look described below, in the drawing style of "
              "image 2.", "",
              YOUNG, "",
              GIU, "",
              "CHANGE:"] + [f"- {d}" for d in doi] + ["",
              STYLE, "",
              "Mood: a small, brave, determined young robot ready to fight (a game hero's first form), cute but not a mascot, not scary. "
              "Both arms and both legs stay attached to the body exactly as in image 1; both fists rest on the ground; the two chest plates "
              "meet in the middle round the round amber light.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same place "
              "and size as in image 1. No sparkles, no dust, no glow, no smoke, no speed lines, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, chỗ và cỡ từng bộ phận như ảnh 1, đầu to tròn hơn; vẫn nhận ra cùng dòng với ảnh 2 (một mắt hổ phách trong mặt nạ "
           "vuông, giáp ngực ôm đèn tròn, cẳng tay thùng, ổ nắm đấm); ít giáp hơn, mới hơn; tô phẳng, không bóng; hai nắm đấm chống đất; nền "
           "trắng tinh."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "khung":
        khung()
    elif cmd == "concept":
        concept()
    else:
        print(__doc__)
