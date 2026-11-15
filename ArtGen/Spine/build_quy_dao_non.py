# -*- coding: utf-8 -*-
"""Gói GPT vẽ dạng 1 của Viêm Đao (quỷ lửa con CHIBI vác đao; mã làm việc quy_dao_non, suất giap_long = tướng thứ 7 đảo Hỏa).

Người dùng (2026-11-14, máy ổ D): "làm dạng 1 cho tướng thứ 7 đảo hỏa". Hai dạng của suất đang dùng chung rig quy_dao_1 (chỉ khác cỡ).
Luật của người dùng: chibi chỉ ở dạng 1, dạng sau dữ và ngầu hơn. Hai hướng dưới đây là ĐỀ XUẤT của Claude, chờ người dùng chọn:
  theo_bo_cuc  giữ chỗ đặt từng bộ phận như hình bố cục (dựng từ rig dạng 2 đổi tỉ lệ xương), vẽ lại thành một con chibi hẳn hoi
  tron_hon     chibi mạnh hơn: đầu gần nửa chiều cao, thân tròn lùn, đao ngắn bè như dao phay

Máy ổ D không có dữ liệu quét monster_3655 nên hình bố cục dựng THẲNG từ .atomik trong game (mo_xe/atomik_dang.py, không cần Chrome):
đổi tỉ lệ xương theo TI_LE, ẩn râu lửa, vẽ khung 0 của idle. Tỉ lệ ghi ra inbox/quy_dao_non/mau/ti_le.json để lúc dựng rig dùng lại.

    py -3 -I ArtGen/Spine/build_quy_dao_non.py           hình bố cục (inbox/quy_dao_non/mau/bo_cuc.png) + hai file prompt + HUONG_DAN.md
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/quy_dao_non/luot_1_concept_<hướng>.txt [--note "..."]
"""
import copy
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources", "quy_dao_1", "quy_dao_1.atomik")
PK = os.path.join(HERE, "gui_gpt", "quy_dao_non")
BASE = os.path.join(HERE, "inbox", "quy_dao_non")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
DANG2 = os.path.join(HERE, "inbox", "quy_dao_1", "tai_ve", "L1_duyet.png")
BO_CUC = os.path.join(MAU, "bo_cuc.png")
W, H = 1536, 1024

# tỉ lệ xương dạng non (nhân lên dáng gốc của rig dạng 2): đầu to, sừng mầm, bờm lửa nhỏ, đao ngắn, thân và chân nhỏ lại
TI_LE = {"lian_01": 1.45, "dajiao_r": 0.5, "dajiao_l": 0.5, "toufa_07": 0.62, "toufa_03": 0.62, "toufa_014": 0.62,
         "toufa_02": 0.5, "toufa_01": 0.5, "wuqi_03": 0.72, "dabi_r": 0.86, "dabi_l": 0.9, "bone2": 0.9}
AN = ["huzi"]                                     # con non chưa có râu lửa


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
    S = A.si(J)
    for s in J["slots"]:
        if s["name"].split("@")[0] in AN or s["name"] == "vet":
            s["att"] = -1
    ci = [i for i, c in enumerate(J["anims"]) if c["name"] == "idle"][0]
    P = A.Pose(J).at(ci, 0.0)
    b = A.bounds(P)
    box = (b[0] - 8, b[1] - 8, b[2] + 8, b[3] + 8)
    ti = min((W - 420) / (box[2] - box[0]), (H - 170) / (box[3] - box[1]))
    im = A.render(J, img, P, box, ti, bg=(255, 255, 255), ss=2).convert("RGB")
    o = Image.new("RGB", (W, H), (255, 255, 255))
    o.paste(im, ((W - im.width) // 2, H - 80 - im.height))
    os.makedirs(MAU, exist_ok=True)
    o.save(BO_CUC)
    json.dump({"ti_le": TI_LE, "an": AN, "nguon": "Resources/quy_dao_1/quy_dao_1.atomik", "px_moi_don_vi": round(ti, 4)},
              open(os.path.join(MAU, "ti_le.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    a = np.asarray(o).min(2) < 240
    ys, xs = np.nonzero(a)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


CHUNG = (
    "CREATURE: the BABY (first-stage) form of the fire demon with the giant dao of image 2, for a monster-collecting game: the same "
    "kind of horned fire demon with a rigid black demon mask, hair of living fire, one big armoured shoulder and a big single-edged "
    "chopping sabre (a dao) carried on its back, but YOUNG and SMALL, drawn CHIBI. A little imp that already carries a blade too big "
    "for it. It is a creature (an elemental monster), NOT a human child, NOT a knight, NOT a robot.\n\n"
    "CHIBI PROPORTIONS (the whole point of this picture): a VERY BIG head, {dau} of the whole figure's height (not counting the "
    "weapon); a short, round, pudgy body; short stubby arms and legs; everything rounder, simpler and chunkier than image 2. It is "
    "still a fighter: the heavy brow of the mask comes down over the eyes, a determined, plucky, ready-to-fight look. NOT a smiling "
    "mascot, NOT scary, NOT horror.\n\n"
    "WHAT IT KEEPS FROM IMAGE 2 (same species, same colours, same materials): pale warm ash-grey skin (#CEC4BA); the mask, the "
    "shoulder guard, the bracers, the belt plates, the knee cap and the claws black iron (#3A3840, the mask a little darker "
    "#322E36); both horns deep charcoal black (#1E1C21); loincloth, shorts and shin wraps dark red (#7C2A26); the dao blade "
    "blue-grey steel (#585A66) with a hot orange band (#F7902A) along its cutting edge, its small oval guard and ring pommel black "
    "iron, its handle wrap dark red; the fire in three flat nested zones red-orange (#E0441F) outside, orange (#F7902A), yellow "
    "(#FFD45A) inside; the two eyes flat yellow (#FFD45A) with no pupils; dark-brown wobbly ink outline (#2B2118), visible crayon "
    "hatching, completely flat colouring. Only these colours: NO blue, NO green, NO purple, NO pink.\n\n"
    "WHAT IS DIFFERENT (it is a baby):\n"
    "- HORNS: only two short blunt cone HORN BUDS growing from the two upper corners of the mask (the near one at the left of the "
    "mask, about one third of the mask's height; the far one smaller at the right). Smooth, whole, not broken.\n"
    "- FIRE HAIR: a SMALL mane: only three plump flame locks growing from the back of the head, sweeping back (to the viewer's "
    "left) and up, reaching no lower than the shoulder guard. Each lock is a real hand-drawn flame with two or three soft pointed "
    "tongues. NO fire beard under the mask.\n"
    "- MASK: the same angular demon mask covering the whole face, turned three-quarters to the right, but rounder and simpler: a "
    "low crest of three short points on top, a heavy angry brow, TWO slanted fierce yellow eyes that are BIGGER than in image 2, a "
    "small pointed chin. No mouth, no teeth, no ears.\n"
    "- SHOULDER GUARD: one round domed pauldron on the near shoulder, smaller than in image 2 (about as big as the mask), with a rim "
    "band along its lower edge and one round boss. NO spike on it.\n"
    "- THE DAO: the same design as in image 2 (ring pommel, wrapped handle, small oval guard, ONE cutting edge, blade getting wider "
    "toward a slanted clipped tip, thick straight back with one square notch, orange band along the cutting edge on the lower-left "
    "side) but SHORTER and CHUNKIER: {dao}. Not a sword: no cross-guard, no second edge.\n"
    "- BODY: a small round pudgy chest and belly, mostly hidden behind the shoulder guard and the near arm. The NEAR arm is still "
    "the bigger one but short and chubby, with a chunky black-iron bracer and a small open clawed hand with four short thick "
    "fingers and small blunt claws, held in front of the blade without touching it. The FAR arm goes up behind the head: only its "
    "bracer and the little fist gripping the dao handle show.\n"
    "- WAIST AND LEGS: a simple belt of two dark plates, a short ragged dark-red loincloth, two very short bent legs in dark-red "
    "shorts and shin wraps with simple blunt feet, a small knee cap on the far leg. Both feet flat on the same ground level.\n\n"
    "SAME BUILD AND VIEW AS IMAGE 2: three-quarter view, FACING THE VIEWER'S RIGHT, leaning a little forward; the masked head low "
    "at the right; the fire hair streaming to the left; the far hand up behind the head gripping the handle; the dao carried "
    "diagonally behind the body: ring pommel at the top (upper left of the head), blade coming down behind the body to the lower "
    "right, its tip resting on the ground.")

D = {
    "theo_bo_cuc": dict(
        ten="theo hình bố cục: chỗ đặt từng bộ phận giữ như rig đổi tỉ lệ, vẽ lại thành một con chibi hẳn hoi (đầu khoảng 45 %)",
        dau="about 45 %",
        dao="about as long as the little demon is tall, the blade broad",
        rieng=("FOLLOW THE LAYOUT GUIDE (image 1) CLOSELY for where every part sits and how big it is: the big masked head with its "
               "two horn buds, the small fire mane behind it, the round shoulder guard, the near arm with bracer and clawed hand, "
               "the small body, the two short legs, and the dao behind everything (ring pommel at the top, blade at the lower "
               "right). Image 1 is a rough computer paste-up made by shrinking and enlarging parts of the adult, so its parts do "
               "not fit together well, its flames have a stiff saw-tooth edge and its shoulder guard still has the adult's spike: "
               "redraw it as ONE properly designed chibi creature: every block rounder and plumper, the flames soft natural "
               "flame shapes, the horn buds sitting neatly on the corners of the mask, no spike on the shoulder guard.")),
    "tron_hon": dict(
        ten="chibi mạnh hơn: đầu gần nửa chiều cao, thân tròn lùn như củ khoai, tay chân ngắn hẳn, đao ngắn bè như dao phay",
        dau="almost half (about 50 %)",
        dao="clearly shorter than the little demon is tall, with a very broad blade like an oversized cleaver",
        rieng=("Use the LAYOUT GUIDE (image 1) only for the general arrangement and the view (which part is where, what overlaps "
               "what). Push the chibi look further than the guide: the head and mask even bigger and rounder, the body a short "
               "round lump about as wide as it is tall, the arms and legs very short round stumps, the shoulder guard a small "
               "round dome without a spike, the fire mane three fat little flame locks, the dao short and very broad. Image 1 is "
               "a rough computer paste-up: never copy its stiff saw-tooth flame edges or its mismatched parts.")),
}

POSE = ("ANIMATION-READY (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): calm, clean "
        "resting pose. Draw every piece as a clear, simple, closed shape with its own complete ink outline, so the pieces can be "
        "separated: the dao, each flame lock, the mask, each horn bud, the shoulder guard, the upper arm, the forearm with its "
        "bracer, the hand, each finger, the chest, the belt plates, each thigh, each shin. The pieces touch or overlap but are NOT "
        "melted into one blob. Every limb is clearly attached to the body (no white background between a limb and the body). No "
        "sparks, no embers, no smoke, no glow, no speed lines, no ground, no shadow, no props, no second character.")
SIMPLE = ("VERY SIMPLE DESIGN, FEW DETAILS: big clean chunky shapes, each piece ONE flat colour with at most ONE inner line; NO lava "
          "cracks, NO glowing lines, NO runes, NO scars, NO chains, NO skulls, NO extra spikes, NO extra horns, NO extra flames. The "
          "ONLY fire-coloured things are: the fire hair, the two eyes and the heated edge band of the dao.")
LINE = ("LINE AND COLOUR: exactly the hand-drawn look of image 2: dark-brown ink pen (#2B2118), outline about 5 px thick around every "
        "big piece and about 3 px for small details (the eyes, the fingers, the handle wrap); coloured-pencil and wax-crayon "
        "hatching visible inside every area, kept inside the outline. FLAT COLOUR, NO LIGHT, NO SHADOW: every area one even colour, "
        "the pencil strokes are texture only; no shading, no darker underside, no cast shadow, no white highlights or shine spots "
        "except one tiny dot in each eye, no metal reflections, no glow around the fire, the eyes or the blade edge, no gradients.")
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
    gd = ["# Gói gửi GPT: `quy_dao_non` (Viêm Đao dạng 1, quỷ lửa con chibi vác đao; suất `giap_long` đảo Hỏa)", "",
          "Làm 2026-11-14 (máy ổ D). Người dùng: \"làm dạng 1 cho tướng thứ 7 đảo hỏa\". Hai hướng là đề xuất của Claude, chờ người dùng "
          "chọn. Ghi chú: `ArtGen/Spine/inbox/quy_dao_ghichu.md` mục 8.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(BO_CUC)}` | Hình bố cục dựng từ rig dạng 2 đổi tỉ lệ xương (1536 × 1024, nền trắng): quỷ con đầu to, hai sừng "
          "mầm, bờm lửa nhỏ, đao ngắn; ghép thô từ mảnh dạng 2 (lửa còn răng cưa, giáp vai còn gai). Lấy chỗ đặt, cỡ từng bộ phận |",
          f"| 2 | `{Wp(DANG2)}` | Concept dạng 2 đã duyệt (1536 × 1024, nền trắng): quỷ lửa da tro, mặt nạ + giáp sắt đen, sừng đen, "
          "bờm và râu lửa, đao lớn một lưỡi. Lấy loài, màu, chất liệu, nét vẽ |", ""]
    for kieu, d in D.items():
        out = os.path.join(TAI, f"L1_{kieu}.png")
        p = os.path.join(PK, f"luot_1_concept_{kieu}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(BO_CUC)}: LAYOUT GUIDE, 1536x1024, white background: a rough computer paste-up of the baby creature in "
             "its resting stance (a small fire demon with a very big masked head, two short horn buds, a small fire mane, a round "
             "shoulder guard and a short broad dao on its back), made from resized parts of the adult. Use it for the arrangement "
             "and sizes, not for its drawing quality.",
             f"image 2 = {Wp(DANG2)}: the APPROVED ADULT form of this creature, 1536x1024, white background: take the species, every "
             "colour, the materials and EXACTLY the hand-drawn line and colouring style from it.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "",
             "TASK: draw ONE creature as ONE picture, in a clean animation-ready resting pose.", "",
             CHUNG.format(dau=d["dau"], dao=d["dao"]), "", d["rieng"], "",
             f"CANVAS AND FRAMING: landscape 1536x1024. The figure stands in the middle, about as big as in the guide (in image 1 it "
             f"spans about x = {x0} to x = {x1}, y = {y0} to y = {y1}, weapon included); everything visible, nothing cut by the "
             "edges.", "",
             SIMPLE, "", POSE, "", LINE, BG]
        ghi(p, t)
        gd += [f"## Hướng `{kieu}`: {d['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/quy_dao_non/luot_1_concept_{kieu}.txt` (thêm "
               "`--note \"...\"` để sửa nhanh).", ""]
        print(p)
    gd += ["## Kiểm", "",
           "- Chibi thật: đầu gần nửa chiều cao (không tính đao), thân tròn lùn, tay chân ngắn; vẫn mặt \"chiến\" (mày đè xuống mắt), không cười.",
           "- Cùng loài với dạng 2: da tro nhạt, mặt nạ + giáp sắt đen, sừng đen than, vải đỏ sẫm, đao thép xám lam có dải lưỡi cam.",
           "- Hai **sừng mầm** ngắn (lành lặn); bờm lửa **nhỏ, ba búi**; **không râu lửa**; giáp vai vòm tròn **không gai**.",
           "- **Đao một lưỡi** ngắn và bè (khâu tròn ở chuôi, bản loe về mũi, sống có một khấc), vẫn to quá khổ so với con non.",
           "- Nhìn sang phải, tay xa vòng lên sau đầu nắm cán đao, mũi đao chống đất bên phải; tay chân dính thân; từng khối có viền kín.",
           "- Tô phẳng, không bóng, không quầng sáng; nền trắng.", "",
           "## GPT vẽ sai thì gửi thêm", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Chưa đủ chibi | `Make it more chibi: the head must be about half of the whole height, the body shorter and rounder, the arms and legs shorter.` |",
           "| Mặt cười / hiền | `Not cute-smiling: the heavy brow of the mask comes down over the eyes, a determined fierce look, no mouth.` |",
           "| Sừng dài / có râu lửa / giáp vai có gai | `Only two short horn buds, NO fire beard under the mask, NO spike on the shoulder guard.` |",
           "| Đao thành kiếm | `The weapon is a DAO: one cutting edge only, blade widening toward a slanted clipped tip, thick back with one notch, small oval guard, ring pommel. No cross-guard.` |",
           "| Quay sang trái | `The creature FACES THE VIEWER'S RIGHT: mask at the right, fire hair streaming to the left.` |"]
    ghi(os.path.join(PK, "HUONG_DAN.md"), gd)


if __name__ == "__main__":
    main()
