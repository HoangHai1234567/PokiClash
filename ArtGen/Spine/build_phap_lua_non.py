# -*- coding: utf-8 -*-
"""Gói GPT vẽ dạng 1 của Viêm Sư (pháp sư lửa con CHIBI; mã làm việc phap_lua_non, suất hong_lien = tướng thứ 6 đảo Hỏa).

Người dùng (2026-11-14, máy ổ D): "suất 6 cho vào game rồi làm thêm dạng 1". Luật của người dùng: chibi chỉ ở dạng 1. Hai hướng dưới đây là
ĐỀ XUẤT của Claude:
  theo_bo_cuc  giữ chỗ đặt từng bộ phận như hình bố cục (dựng từ rig dạng 2 đổi tỉ lệ xương), vẽ lại thành một con chibi hẳn hoi
  tron_hon     chibi mạnh hơn: mũ trùm tròn như quả chuông chiếm nửa người, thân áo bé xíu, trượng ngắn như đũa phép

Hình bố cục dựng THẲNG từ .atomik dạng 2 (inbox/phap_lua_1/rig/phap_lua_1.atomik, mo_xe/atomik_dang.py, không cần Chrome): đổi tỉ lệ xương
theo TI_LE, vẽ khung 0 của idle. Tỉ lệ ghi ra inbox/phap_lua_non/mau/ti_le.json để lúc dựng rig dùng lại.

    py -3 -I ArtGen/Spine/build_phap_lua_non.py          hình bố cục (inbox/phap_lua_non/mau/bo_cuc.png) + hai file prompt + HUONG_DAN.md
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/phap_lua_non/luot_1_concept_<hướng>.txt [--note "..."]
"""
import copy
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
SRC = os.path.join(HERE, "inbox", "phap_lua_1", "rig", "phap_lua_1.atomik")
PK = os.path.join(HERE, "gui_gpt", "phap_lua_non")
BASE = os.path.join(HERE, "inbox", "phap_lua_non")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
DANG2 = os.path.join(HERE, "inbox", "phap_lua_1", "tai_ve", "L1_duyet.png")
BO_CUC = os.path.join(MAU, "bo_cuc.png")
W, H = 1536, 1024

# tỉ lệ xương dạng non (nhân lên dáng gốc của rig dạng 2): đầu mũ trùm to, tóc theo đầu, trượng ngắn (cầu lửa co và dời theo đầu trượng),
# đuôi áo + lửa dưới áo ngắn, hai bàn tay nhỏ
TI_LE = {"bone6": 1.45, "bone61": 1.2, "bone56": 0.72, "cau_goc": {"s": 0.72, "dx": 36, "dy": -62}, "bone25": 0.85, "bone11": 0.82,
         "bone42": 0.9}


def Wp(p):
    return os.path.normpath(p)


def bo_cuc():
    """dáng nghỉ (khung 0 idle) của rig dạng 2 sau khi đổi tỉ lệ xương, đặt giữa khung 1536 × 1024 nền trắng; trả khung bao hình (px)."""
    import numpy as np
    from PIL import Image
    import atomik_dang as A
    J, img, _ = A.load(SRC)
    J = copy.deepcopy(J)
    A.scale_bones(J, TI_LE)
    ci = [i for i, c in enumerate(J["anims"]) if c["name"] == "idle"][0]
    P = A.Pose(J).at(ci, 0.0)
    b = A.bounds(P)
    box = (b[0] - 8, b[1] - 8, b[2] + 8, b[3] + 8)
    ti = min((W - 420) / (box[2] - box[0]), (H - 190) / (box[3] - box[1]))
    im = A.render(J, img, P, box, ti, bg=(255, 255, 255), ss=2).convert("RGB")
    o = Image.new("RGB", (W, H), (255, 255, 255))
    o.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    os.makedirs(MAU, exist_ok=True)
    o.save(BO_CUC)
    json.dump({"ti_le": TI_LE, "nguon": "inbox/phap_lua_1/rig/phap_lua_1.atomik", "px_moi_don_vi": round(ti, 4)},
              open(os.path.join(MAU, "ti_le.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    a = np.asarray(o).min(2) < 240
    ys, xs = np.nonzero(a)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


CHUNG = (
    "CREATURE: the BABY (first-stage) form of the floating fire-mage spirit of image 2, for a monster-collecting game: the same kind "
    "of little hooded fire spirit (a deep charcoal hood with no face inside, only two burning eyes; pale smoke-like hair; a red robe "
    "that ends in fire instead of legs; two floating clawed hands; a staff holding a ball of fire), but YOUNG and SMALL, drawn "
    "CHIBI. A tiny apprentice sorcerer spirit. It is a creature (an elemental spirit), NOT a human child, NOT a ghost in a bed "
    "sheet, NOT a robot.\n\n"
    "CHIBI PROPORTIONS (the whole point of this picture): a VERY BIG hooded head, {dau} of the whole figure's height; a tiny short "
    "body; everything rounder, simpler and chunkier than image 2. It is still a fighter: the two fire eyes are slanted and tilted "
    "down toward the middle, a determined, plucky, ready-to-fight look. NOT a smiling mascot, NOT scary, NOT horror.\n\n"
    "WHAT IT KEEPS FROM IMAGE 2 (same species, same colours, same materials): hood and shoulder cape dark charcoal (#3C353B) with a "
    "pale gold (#E2B24C) hem; inside the hood flat darkness (#1F1A1E) with two eyes of fire (orange #F7902A, yellow #FFD45A centre), "
    "no nose, no mouth, no skin; a small diamond-shaped yellow gem (#FFD45A) on the brow of the hood; hair and wrists pale ash-cream "
    "(#E9E1D2) like wisps of smoke; robe deep crimson red (#A32E22) with a pale gold braided cord down its front; staff, fingers "
    "and claws charcoal black (#2F2A30); every fire in three flat nested zones red-orange (#E0441F) outside, orange (#F7902A), "
    "yellow (#FFD45A) inside; dark-brown wobbly ink outline (#2B2118), visible crayon hatching, completely flat colouring. Only "
    "these colours: NO blue, NO green, NO purple, NO pink.\n\n"
    "WHAT IS DIFFERENT (it is a baby):\n"
    "- THE HOOD is the biggest thing in the picture: a big soft rounded cowl seen almost from the front, turned a little to the "
    "right, with a broad gold hem around the big dark face opening; its pointed TIP is short and droops back to the upper LEFT; "
    "two short rounded lappets hang down at the sides of the opening. The two fire eyes are BIGGER than in image 2 (each about a "
    "quarter of the opening's width), still almond-shaped and slanted.\n"
    "- HAIR: only two or three short soft tufts of the pale smoke-hair peeking out behind the hood at the upper left and the "
    "right. Much less hair than in image 2.\n"
    "- SHOULDER CAPE: a small charcoal collar-cape with the gold hem, just covering the shoulders, with one short pointed tail "
    "swept back to the lower left. No long cape.\n"
    "- BODY: a tiny short red robe under the cape, about as tall as one third of the hood, with the gold braided cord. Under the "
    "robe, instead of legs, a SHORT skirt of four or five plump little flame tongues pointing down (the spirit floats: no feet, "
    "no legs, no ground).\n"
    "- HANDS: two small floating clawed hands, each a little puff of pale smoke (the wrist) ending in a small charcoal-black hand "
    "with short blunt claws. The hand at the viewer's LEFT holds the staff; the hand at the viewer's RIGHT floats open beside the "
    "hood, fingers curled, ready to scratch. The hands are NOT joined to the body by arms.\n"
    "- THE STAFF: {truong}. Its top is the same open claw-shaped crook as in image 2, and INSIDE the crook floats a small BALL OF "
    "FIRE (a round ball with a yellow heart and three or four small flame tongues licking up from it). The lower end of the staff "
    "is a short zigzag point. No eye, no gem, no smoke on the staff.\n\n"
    "SAME VIEW AS IMAGE 2: floating upright, seen from the front in a slight three-quarter view, FACING THE VIEWER'S RIGHT; the "
    "staff with its fireball at the viewer's left of the body; the free clawed hand at the viewer's right.")

D = {
    "theo_bo_cuc": dict(
        ten="theo hình bố cục: chỗ đặt từng bộ phận giữ như rig đổi tỉ lệ, vẽ lại thành một con chibi hẳn hoi (mũ trùm khoảng 45 % chiều cao)",
        dau="about 45 %",
        truong="a SHORT staff, about as tall as the whole little spirit, held upright and leaning a little to the left",
        rieng=("FOLLOW THE LAYOUT GUIDE (image 1) CLOSELY for where every part sits and how big it is: the big hood with its dark "
               "opening and two fire eyes, the hair tufts behind it, the small shoulder cape with its tail to the lower left, the "
               "little red robe, the skirt of flames, the staff with the fireball at the left, the two floating hands. Image 1 is "
               "a rough computer paste-up made by shrinking and enlarging parts of the adult, so its parts do not fit together "
               "well and it still has the adult's long hair and cape: redraw it as ONE properly designed chibi creature, every "
               "shape rounder and plumper, the hair and the cape reduced as described.")),
    "tron_hon": dict(
        ten="chibi mạnh hơn: mũ trùm tròn như quả chuông chiếm nửa người, thân áo bé xíu, trượng ngắn như đũa phép",
        dau="about half (50 %)",
        truong="a VERY SHORT staff like a wand, clearly shorter than the little spirit is tall, held upright",
        rieng=("Use the LAYOUT GUIDE (image 1) only for the general arrangement and the view (which part is where, what overlaps "
               "what). Push the chibi look further than the guide: the hood a big round bell shape taking half of the figure, "
               "the robe a tiny round body, the flame skirt four short fat flame tongues, the two hands small round paws with "
               "tiny claws, the hair two little tufts, the staff a short wand with its little fireball. Image 1 is a rough "
               "computer paste-up: never copy its mismatched parts.")),
}

POSE = ("ANIMATION-READY (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): calm, clean "
        "resting pose. Draw every piece as a clear, simple, closed shape with its own complete ink outline, so the pieces can be "
        "separated: the hood, each hair tuft, the shoulder cape, the robe, the flame skirt, the staff, the fireball, each hand, "
        "each wrist puff. The pieces touch or overlap but are NOT melted into one blob. No sparks, no embers, no smoke clouds, no "
        "glow, no speed lines, no ground, no shadow, no props, no second character.")
SIMPLE = ("VERY SIMPLE DESIGN, FEW DETAILS: big clean chunky shapes, each piece ONE flat colour with at most ONE inner line (the fire "
          "keeps its three nested zones); NO runes, NO stars, NO patterns on the cloth, NO chains, NO skulls, NO horns, NO extra "
          "flames. The ONLY fire-coloured things are: the two eyes, the fireball on the staff and the flame skirt under the robe.")
LINE = ("LINE AND COLOUR: exactly the hand-drawn look of image 2: dark-brown ink pen (#2B2118), outline about 5 px thick around every "
        "big piece and about 3 px for small details (the eyes, the fingers, the cord); coloured-pencil and wax-crayon hatching "
        "visible inside every area, kept inside the outline. FLAT COLOUR, NO LIGHT, NO SHADOW: every area one even colour, the "
        "pencil strokes are texture only; no shading, no darker underside, no cast shadow, no white highlights or shine spots, no "
        "glow around the fire or the eyes, no gradients.")
BG = ("Plain pure-white background (#FFFFFF), no paper grain outside the drawing, no white border or sticker outline around the "
      "figure (the game adds that itself), no text, no labels, no frame.")


def ghi(p, lines):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def main():
    for p in (SRC, DANG2):
        if not os.path.exists(p):
            raise SystemExit("thiếu: " + Wp(p))
    x0, y0, x1, y1 = bo_cuc()
    os.makedirs(PK, exist_ok=True)
    os.makedirs(TAI, exist_ok=True)
    gd = ["# Gói gửi GPT: `phap_lua_non` (Viêm Sư dạng 1, pháp sư lửa con chibi; suất `hong_lien` đảo Hỏa)", "",
          "Làm 2026-11-14 (máy ổ D). Người dùng: \"suất 6 cho vào game rồi làm thêm dạng 1\". Hai hướng là đề xuất của Claude. Ghi chú: "
          "`ArtGen/Spine/inbox/phap_lua_ghichu.md` mục 9.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(BO_CUC)}` | Hình bố cục dựng từ rig dạng 2 đổi tỉ lệ xương (1536 × 1024, nền trắng): mũ trùm to, áo đỏ và váy lửa "
          "ngắn, trượng ngắn có cầu lửa bên trái, hai bàn tay vuốt lơ lửng; ghép thô từ mảnh dạng 2 (tóc và áo choàng còn dài). Lấy chỗ "
          "đặt, cỡ từng bộ phận |",
          f"| 2 | `{Wp(DANG2)}` | Concept dạng 2 đã duyệt (1536 × 1024, nền trắng): pháp sư lửa mũ trùm than viền vàng, mắt lửa, tóc khói "
          "ngà, áo đỏ cháy thành lửa, trượng có cầu lửa. Lấy loài, màu, chất liệu, nét vẽ |", ""]
    for kieu, d in D.items():
        out = os.path.join(TAI, f"L1_{kieu}.png")
        p = os.path.join(PK, f"luot_1_concept_{kieu}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(BO_CUC)}: LAYOUT GUIDE, 1536x1024, white background: a rough computer paste-up of the baby creature in "
             "its resting stance (a small floating fire-mage spirit with a very big hood, a short robe ending in flames, a short "
             "staff with a fireball at the left and two floating clawed hands), made from resized parts of the adult. Use it for "
             "the arrangement and sizes, not for its drawing quality.",
             f"image 2 = {Wp(DANG2)}: the APPROVED ADULT form of this creature, 1536x1024, white background: take the species, every "
             "colour, the materials and EXACTLY the hand-drawn line and colouring style from it.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "",
             "TASK: draw ONE creature as ONE picture, in a clean animation-ready resting pose.", "",
             CHUNG.format(dau=d["dau"], truong=d["truong"]), "", d["rieng"], "",
             f"CANVAS AND FRAMING: landscape 1536x1024. The figure floats in the middle, about as big as in the guide (in image 1 it "
             f"spans about x = {x0} to x = {x1}, y = {y0} to y = {y1}, staff included); everything visible, nothing cut by the "
             "edges.", "",
             SIMPLE, "", POSE, "", LINE, BG]
        ghi(p, t)
        gd += [f"## Hướng `{kieu}`: {d['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/phap_lua_non/luot_1_concept_{kieu}.txt` (thêm "
               "`--note \"...\"` để sửa nhanh).", ""]
        print(p)
    gd += ["## Kiểm", "",
           "- Chibi thật: mũ trùm gần nửa chiều cao, thân áo bé, váy lửa ngắn; vẫn mặt \"chiến\" (hai mắt lửa xếch chúi vào giữa), không cười.",
           "- Cùng loài với dạng 2: mũ trùm than viền vàng có viên ngọc vàng, trong mũ tối đen chỉ có hai mắt lửa, tóc khói ngà, áo đỏ dây vàng.",
           "- Tóc **ít** (hai ba búi ngắn), áo choàng vai **ngắn**, trượng **ngắn** có cầu lửa nhỏ trong móc vuốt; không khói.",
           "- Hai bàn tay vuốt nhỏ **lơ lửng** (cổ tay là búi khói ngà), không có cánh tay; không chân, váy lửa thay chân.",
           "- Nhìn sang phải, trượng bên trái người xem; từng khối có viền kín.",
           "- Tô phẳng, không bóng, không quầng sáng; nền trắng.", "",
           "## GPT vẽ sai thì gửi thêm", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Chưa đủ chibi | `Make it more chibi: the hood must be about half of the whole height, the robe tiny, the flame skirt short, the staff shorter.` |",
           "| Mặt cười / hiền | `Not cute-smiling: two slanted fierce fire eyes tilted down toward the middle, no mouth, no face.` |",
           "| Có mặt người / da | `Inside the hood there is NO face: only flat darkness and two eyes of fire.` |",
           "| Có cánh tay / chân | `The hands FLOAT, joined to nothing (a puff of pale smoke as the wrist); no arms, no legs, no feet: a short skirt of flames under the robe.` |",
           "| Tóc, áo choàng dài như dạng 2 | `Much less hair (two or three short tufts) and only a small collar-cape with one short tail.` |"]
    ghi(os.path.join(PK, "HUONG_DAN.md"), gd)


if __name__ == "__main__":
    main()
