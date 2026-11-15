# -*- coding: utf-8 -*-
"""Hổ lửa DẠNG 1 (hổ con "Viêm Hổ Nhi"; mã hoa_ho_non, suất hoa_tinh = tướng thứ 9 đảo Hỏa).

Người dùng 2026-11-14 (máy ổ D): "Ok cho vào game rồi làm dạng 1". Cùng bộ xương, lưới, clip với dạng 2 (hoa_ho_rig.py, HH_DANG=non).
Khác dạng 2 (thiết kế do Claude đề xuất, người dùng chưa duyệt concept riêng):
- đầu to (xương đầu phóng 1,4), MẮT TRÒN TO vẽ bằng mã (lưới mắt phóng theo trục của nó), không dải mày đỏ đè mắt, không nanh dài;
- không vòng vàng cổ chân; lửa non màu cam lõi vàng (đổi sắc bằng mã từ da dạng 2); thân, chân, đuôi, mây: dùng lại da dạng 2.
- mảnh vẽ lại: nửa đầu trên P_tou (tờ N_DAU: Codex vẽ lại đúng hình bóng, bỏ dải hốc mắt đỏ).

    hoa_ho_non.py to      tờ hướng dẫn inbox/hoa_ho_non/mau/part_DAU.png + prompt gui_gpt/hoa_ho_non/luot_1_manh_DAU.txt (+ HUONG_DAN.md)
    hoa_ho_non.py cat     cắt tờ đã gen → inbox/hoa_ho_non/manh/part/P_tou.png (đo IoU)
    hoa_ho_non.py bo_cuc  (bản chibi) hình bố cục từ rig với tỉ lệ CHIBI → inbox/hoa_ho_non/mau/bo_cuc_chibi.png
    hoa_ho_non.py concept (bản chibi) hai prompt concept gui_gpt/hoa_ho_non/luot_0_concept_<A|B>.txt (+ HUONG_DAN_concept.md)
    hoa_ho_non.py mat     mắt mở tròn to + mắt nhắm → inbox/hoa_ho_non/manh/part/P_yanjing.png, P_biyan.png
  Rig: HH_DANG=non py -3 -I hoa_ho_rig.py → inbox/hoa_ho_non/rig/
Xương, lưới, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai."""
import glob
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
BASE = os.path.join(HERE, "inbox", "hoa_ho_non")
TAI = os.path.join(BASE, "tai_ve")
MAU = os.path.join(BASE, "mau")
MANH = os.path.join(BASE, "manh", "part")
GUI = os.path.join(HERE, "gui_gpt", "hoa_ho_non")
LON = os.path.join(HERE, "inbox", "hoa_ho_1")
W, H = 1536, 1024
K_TO = 2.2                                           # tờ hướng dẫn phóng ảnh part P_tou của dạng 2 lên K_TO lần
INK = (43, 33, 24)
MAT_VANG = (248, 196, 60)
# khung ảnh mắt của dạng 1 (px): rộng, cao. Lưới mắt của rig được kéo theo đúng tỉ lệ này (hoa_ho_rig.py, MAT_NON)
MAT_WH = (300, 300)


def Wp(p):
    return os.path.normpath(p)


def ghi(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(s)


def to():
    src = Image.open(os.path.join(LON, "manh", "part", "P_tou.png")).convert("RGBA")
    g = src.resize((round(src.width * K_TO), round(src.height * K_TO)), Image.LANCZOS)
    x0, y0 = (W - g.width) // 2, (H - g.height) // 2
    sheet = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    sheet.alpha_composite(g, (x0, y0))
    os.makedirs(MAU, exist_ok=True)
    p_to = os.path.join(MAU, "part_DAU.png")
    sheet.convert("RGB").save(p_to)
    json.dump(dict(x0=x0, y0=y0, w=g.width, h=g.height, k=K_TO), open(os.path.join(MAU, "part_DAU.json"), "w"))
    con = os.path.join(LON, "tai_ve", "L1_duyet.png")
    out = os.path.join(TAI, "N_DAU.png")
    os.makedirs(TAI, exist_ok=True)
    txt = f"""IMAGES (attached in this order; open each from its path):
image 1 = {Wp(con)}: the ADULT creature, 1536x1024, white background: a cream-white FIRE TIGER facing right with charcoal zigzag stripes, fire-cloud mane and a spiral mark on its cheek. It gives the drawing style only: the wobbly dark-brown ink line, the loose crayon hatching, the flat colours.
image 2 = {Wp(p_to)}: ONE PART of the adult's 2D animation rig, 1536x1024, white background: the UPPER HEAD of the tiger (skull, forehead, cheek, nose and upper lip; no lower jaw, no ears), three-quarter view facing RIGHT, the muzzle at the lower right, jagged cheek-fur points at the left and bottom. A long vermilion band with a brow line runs across it from the ear side to the nose: that is the adult's eye socket.

SAVE: save it as a PNG to {Wp(out)}
If a file with that name already exists, save as N_DAU_2.png, N_DAU_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: redraw image 2 as the head of the tiger's CUB (the same animal, very young), landscape 1536x1024, pure-white background. Keep EXACTLY the silhouette of image 2: the same outline with the same jagged fur points, the same size, the same angle, the same position on the sheet (if your picture were laid over image 2 the two outlines must coincide). A program will cut this sheet by position.

WHAT CHANGES INSIDE THE SHAPE (cub face, soft and simple):
- REMOVE the long vermilion eye-socket band and its heavy brow line completely. Where it was, draw plain cream-white fur (#F2ECDE), the same as the rest of the head.
- Do NOT draw any eye, eyelid, iris, pupil or eyebrow anywhere: the eye is a separate piece added later. The middle of the face stays plain cream fur.
- KEEP the small dusty-rose nose (#C8706A) with its dark nostril at the tip of the muzzle and the curved line of the upper lip, exactly where image 2 has them.
- KEEP ONE spiral swirl painted on the cheek at the same place, but make it ORANGE (#EE8A2E) instead of vermilion, and a little smaller.
- On the forehead and the back of the skull: only two small charcoal (#5A5458) zigzag stripe marks. No other marks.
- A few short soft fur strokes near the cheek-fur points. Nothing else.

OUTLINE: ONE closed dark-brown ink outline (#2B2118), about 11 px thick on this sheet, wobbly like a real pen, lying just INSIDE the edge of the silhouette (never outside it). Inner detail lines are thinner (about 5 px).
COLOUR: cream-white fur filled with visible loose diagonal crayon / coloured-pencil hatching as in image 1, kept inside the outline.
The shape is a complete, closed object on its own: do not draw ears, lower jaw, flames, neck or the rest of the creature.

FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no darker side, no highlights or shine spots, no glow, NO GRADIENTS (two colours always meet at a clean edge), no cast shadows, no 3D look. Pure white (#FFFFFF) background; no text, no labels, no numbers, no frames, no guide lines.
"""
    p = os.path.join(GUI, "luot_1_manh_DAU.txt")
    ghi(p, txt)
    ghi(os.path.join(GUI, "HUONG_DAN.md"), f"""# Hổ lửa dạng 1 (hổ con, hoa_ho_non): gói gửi GPT

Dạng 1 dùng lại gần hết da của dạng 2 (thân, chân, đuôi, mây lửa đổi sang màu cam bằng mã). Chỉ có MỘT mảnh phải vẽ lại.

## Lượt 1: mảnh đầu
- File prompt: `{Wp(p)}`
- Ảnh mẫu 1: `{Wp(con)}` — concept hổ lớn đã duyệt, 1536x1024, nền trắng (chỉ để lấy nét vẽ).
- Ảnh mẫu 2: `{Wp(p_to)}` — nửa đầu trên của hổ lớn (không hàm dưới, không tai), phóng {K_TO} lần, 1536x1024, nền trắng; có dải đỏ hốc mắt chạy ngang.
- GPT lưu vào: `{Wp(out)}` (trùng tên thì `_2`, `_3`).

## Cách kiểm
- Hình bóng trùng ảnh mẫu 2 (cùng chỗ, cùng cỡ, cùng răng cưa lông má).
- Không còn dải đỏ, không vẽ mắt; còn mũi, viền môi trên, một vòng xoáy cam trên má, hai vệt vằn nhỏ.
- Tô phẳng, không bóng, không điểm sáng.

## Câu sửa nhanh
- Còn vẽ mắt: "Remove the eye completely; leave plain cream fur there."
- Lệch hình bóng: "Keep exactly the silhouette of image 2: same outline, same size, same position."
""")
    print(p_to, "\n", p)


def cat():
    cfg = json.load(open(os.path.join(MAU, "part_DAU.json")))
    ds = sorted(glob.glob(os.path.join(TAI, "N_DAU*.png")), key=os.path.getmtime)
    src = Image.open(os.path.join(LON, "manh", "part", "P_tou.png")).convert("RGBA")
    al0 = np.asarray(src)[..., 3] > 127
    tot = None
    for p in ds:
        g = Image.open(p).convert("RGB")
        if g.size != (W, H):
            g = g.resize((W, H), Image.LANCZOS)
        c = g.crop((cfg["x0"], cfg["y0"], cfg["x0"] + cfg["w"], cfg["y0"] + cfg["h"])).resize(src.size, Image.LANCZOS)
        A = np.asarray(c).astype(np.int32)
        nen = (A.min(2) > 238)                                     # giấy trắng
        # nền = trắng nối với mép ô (trắng kín bên trong hình là kem nhạt của lông, giữ)
        n, lab = cv2.connectedComponents(nen.astype(np.uint8), connectivity=4)
        mep = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])
        ngoai = np.isin(lab, [k for k in mep if k]) & nen
        m = ~ngoai
        iou = (m & al0).sum() / max(1, (m | al0).sum())
        print(os.path.basename(p), f"IoU {iou:.3f}")
        if tot is None or iou > tot[0]:
            tot = (iou, c, m)
    iou, c, m = tot
    A = np.asarray(c).copy()
    # cắt theo hình bóng dạng 2 (lưới của rig ôm hình bóng đó); chỗ GPT vẽ hụt lấy màu kem
    hut = al0 & ~m
    A[hut] = (242, 236, 222)
    out = np.dstack([A, np.asarray(src)[..., 3]])
    os.makedirs(MANH, exist_ok=True)
    Image.fromarray(out.astype(np.uint8), "RGBA").save(os.path.join(MANH, "P_tou.png"))
    json.dump({"P_tou": round(float(iou), 3)}, open(os.path.join(MANH, "_iou.json"), "w"))
    print("P_tou.png", src.size, f"IoU {iou:.3f}, vẽ hụt {int(hut.sum())} px")


def mat():
    """mắt hổ con: tròn to. Khung MAT_WH; mí mực dày, mống hổ phách, con ngươi bầu dục đứng to, một chấm sáng nhỏ."""
    w, h = MAT_WH
    S = 4
    im = np.zeros((h * S, w * S, 4), np.uint8)
    cx, cy = w * S // 2, h * S // 2
    rx, ry = int(w * S * 0.47), int(h * S * 0.47)
    net = int(13 * S)
    cv2.ellipse(im, (cx, cy), (rx, ry), 0, 0, 360, INK + (255,), -1, cv2.LINE_AA)
    cv2.ellipse(im, (cx, cy + int(net * 0.15)), (rx - net, ry - net), 0, 0, 360, MAT_VANG + (255,), -1, cv2.LINE_AA)
    cv2.ellipse(im, (cx + int(rx * 0.10), cy), (int(rx * 0.40), int(ry * 0.66)), 0, 0, 360, INK + (255,), -1, cv2.LINE_AA)
    cv2.circle(im, (cx - int(rx * 0.18), cy - int(ry * 0.36)), int(rx * 0.17), (255, 250, 236, 255), -1, cv2.LINE_AA)
    # mí trên dày hơn (vẻ quả quyết): một cung mực đè lên mép trên
    mi = np.zeros((h * S, w * S), np.uint8)
    cv2.ellipse(mi, (cx, cy), (rx, ry), 0, 0, 360, 255, -1, cv2.LINE_AA)
    cat_ = np.zeros_like(mi)
    cv2.line(cat_, (cx - rx - 10, cy - int(ry * 0.50)), (cx + rx + 10, cy - int(ry * 0.80)), 255, int(ry * 0.9), cv2.LINE_AA)
    tren = (mi > 127) & (cat_ > 127) & (np.arange(h * S)[:, None] < cy - int(ry * 0.52) + (np.arange(w * S)[None, :] - cx) * (-0.3 * ry / rx))
    im[tren] = INK + (255,)
    os.makedirs(MANH, exist_ok=True)
    Image.fromarray(im, "RGBA").resize((w, h), Image.LANCZOS).save(os.path.join(MANH, "P_yanjing.png"))
    # mắt nhắm: một cung mực cong xuống giữa khung
    b = np.zeros((h * S, w * S, 4), np.uint8)
    cv2.ellipse(b, (cx, cy - int(ry * 0.15)), (int(rx * 0.92), int(ry * 0.5)), 0, 20, 160, INK + (255,), int(15 * S), cv2.LINE_AA)
    Image.fromarray(b, "RGBA").resize((w, h), Image.LANCZOS).save(os.path.join(MANH, "P_biyan.png"))
    print("P_yanjing, P_biyan", MAT_WH)


# ---------------------------------------------------------------- bản CHIBI (2026-11-14 tối, người dùng: "Hổ con xấu quá, gen lại chibi hơn")
# Tỉ lệ đổi ngay trên rig (HH_KDAU đầu, HH_CHAN chân, HH_DUOI đuôi) → hình bố cục → concept GPT → người dùng chọn → mới làm mảnh.
CHIBI = dict(HH_KDAU="2.0", HH_CHAN="0.68", HH_DUOI="0.6", HH_MAT="298,765,45")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no darker side, no "
        "cast shadow, no shadow under the feet, no white highlights or shine spots (except ONE tiny light dot in the eye), no glow around the "
        "fire, NO GRADIENTS (two colours always meet at a clean edge), no 3D look.")


def bo_cuc():
    """hình bố cục 1536x1024 nền trắng: dáng đứng khung 0 idle của rig với tỉ lệ CHIBI, da tạm của bản cũ (chỉ để GPT lấy dáng và tỉ lệ)."""
    for k, v in CHIBI.items():
        os.environ.setdefault(k, v)
    os.environ["HH_DANG"] = "non"
    import hoa_ho_rig as R
    sk, info = R.dung()
    ve0 = R.soi.Ve(sk)
    clips = R.lam_clip(sk, info)
    P0 = R.hoat.nuong(sk, clips[1])[0]
    b = ve0.bao(P0)
    sc = min((W * 0.74) / (b[2] - b[0]), (H * 0.80) / (b[3] - b[1]))
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    box = (cx - W / 2 / sc, cy - H / 2 / sc, cx + W / 2 / sc, cy + H / 2 / sc)
    im = ve0.ve(P0, box, sc, bg=(255, 255, 255), ss=2).convert("RGB").resize((W, H), Image.LANCZOS)
    os.makedirs(MAU, exist_ok=True)
    p = os.path.join(MAU, "bo_cuc_chibi.png")
    im.save(p)
    json.dump(dict(sc=sc, box=box, chibi=CHIBI), open(os.path.join(MAU, "bo_cuc_chibi.json"), "w"))
    print(p, f"{sc:.3f} px / đơn vị")


def concept():
    lon = os.path.join(LON, "tai_ve", "L1_duyet.png")
    bc = os.path.join(MAU, "bo_cuc_chibi.png")
    chibi = os.path.join(HERE, "inbox", "quy_dao_non", "tai_ve", "L1_duyet.png")
    net = os.path.normpath(os.path.join(HERE, "..", "Islands", "refs", "world_style.png"))
    os.makedirs(TAI, exist_ok=True)
    huong = {
        "A": ("theo bố cục",
              "Follow image 2 closely: the same proportions and the same placement of head, body, legs and tail on the canvas."),
        "B": ("tròn hơn",
              "Follow the pose and placement of image 2, but push it ROUNDER and even more chibi: the body is a plump round ball, the four legs "
              "are very short stubs so that mostly the big round paws show under the belly (each leg still clearly visible and separate), the "
              "head is slightly bigger than in image 2, the eye is larger, the cheeks are fuller."),
    }
    hd = [f"# Hổ lửa dạng 1 bản CHIBI (hoa_ho_non): concept\n",
          "Người dùng 2026-11-14: \"Hổ con xấu quá, gen lại chibi hơn\". Hai hướng concept, chọn một rồi Claude mới làm mảnh.\n",
          "## Ảnh mẫu (cả hai file dùng chung, theo thứ tự)",
          f"1. `{Wp(lon)}` — concept hổ LỚN đã duyệt, 1536x1024, nền trắng: lấy loài, màu, nét vẽ.",
          f"2. `{Wp(bc)}` — hình bố cục máy dựng từ rig, 1536x1024, nền trắng: hổ đầu to gấp đôi, chân ngắn, đuôi ngắn, nhìn thô và còn chi tiết của hổ lớn; chỉ để lấy dáng và tỉ lệ.",
          f"3. `{Wp(chibi)}` — dạng 1 chibi đã duyệt của một tướng khác (quỷ con vác đao), nền trắng: lấy MỨC chibi và độ đơn giản.",
          f"4. `{Wp(net)}` — ảnh mốc nét vẽ tay của game (bản đồ vẽ bút mực, tô chì màu).\n"]
    for ma, (vi, cau) in huong.items():
        out = os.path.join(TAI, f"L1_{ma}.png")
        txt = f"""IMAGES (attached in this order; open each from its path):
image 1 = {Wp(lon)}: the ADULT creature, already approved, 1536x1024, white background: a cream-white FIRE TIGER facing right with charcoal zigzag stripes, a mane of flat flame-cloud scrolls, a spiral mark on its cheek. It gives the species, the colours and the drawing style (wobbly dark-brown ink line, loose crayon hatching, flat colours).
image 2 = {Wp(bc)}: PROPORTION AND POSE GUIDE, 1536x1024, white background, assembled by computer from the animation rig: the same animal with a head twice as big, short legs and a short tail, standing on four legs facing right. It is crude and still carries the adult's details (too many flames, big claws, too many stripes). Use it ONLY for the pose, the proportions and where each body part sits on the canvas.
image 3 = {Wp(chibi)}: an approved CHIBI baby form of a different creature from the same set, white background. It shows the level of chibi wanted: huge simple head, tiny body, few details, bold clean shapes. Do not copy that creature.
image 4 = {Wp(net)}: the hand-drawn look of the whole set: ink pen on paper, filled with coloured pencil and wax crayon.

SAVE: save it as a PNG to {Wp(out)}
If a file with that name already exists, save as L1_{ma}_2.png, L1_{ma}_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: design and draw the CUB (the baby form) of the fire tiger of image 1 as a cute CHIBI creature. One single creature, whole body, landscape 1536x1024, pure-white background (#FFFFFF), side view facing RIGHT, standing on all four legs. {cau}

PROPORTIONS: the head is huge and round, about half of the creature's total length and taller than the body. The body is small and plump. Four short, thick, stubby legs with big round paws. A short thick tail held up behind the body.

HEAD AND FACE: seen in three-quarter side view facing right, so ONE big eye is visible. The eye is big and round: dark ink rim, amber-yellow iris (#F8C43C), a large dark pupil, ONE tiny light dot. A short firm upper eyelid gives a brave, determined look (cute but ready to fight, not sleepy, not scary). Small dusty-rose nose (#C8706A) at the tip of a short rounded muzzle. Mouth closed: one curved lip line, with ONE tiny ivory fang tip peeking out. Full round cheek with ONE small orange spiral mark painted on it. Under the muzzle a rounded chin with short soft fur points. Two rounded ears with soft rose (#EEAA96) inside. Two small charcoal zigzag stripes on the forehead.

FUR AND STRIPES: cream-white fur (#F2ECDE). Only a FEW bold charcoal (#5A5458) zigzag stripes: four or five on the back and flank, two rings on the tail, one or two on each visible leg. The two far legs are a slightly darker cream (#E2D6C4).

FIRE (young fire, much less than the adult): flat flame-cloud curls in ORANGE (#F08A2E) with GOLDEN-YELLOW (#F8C84A) cores and one spiral curl each, drawn like the adult's flame clouds but small. Only: a small ruff of FOUR or FIVE curls on the back of the neck and shoulders; TWO tiny flame tufts on the brow; ONE small flame at the tip of the tail. No flames anywhere else.

PAWS: big, round and soft, with three or four tiny charcoal claw tips each. No long claws.

NOT ON THE CUB: no horn, no bell, no bangles, no jewellery, no armour, no long fangs, no whisker curls.

KEEP IT EASY TO ANIMATE: all four legs clearly visible and separate from each other, placed as in image 2 (do not hide a leg behind the body or behind fur). The tail does not overlap the body. Nothing covers the face. The flame ruff sits behind the head and does not cover the ear.

LINE AND COLOUR: exactly the hand-drawn look of images 1 and 4: ONE wobbly dark-brown ink pen outline (#2B2118), about 7 px thick around the creature and around each body part, about 4 px for inner details; every area filled with visible loose diagonal coloured-pencil / wax-crayon hatching kept inside the lines. Drawn carefully and cleanly, not scribbled, not glossy, not digital-looking.

{FLAT}

Pure white background. No ground, no ground shadow, no text, no labels, no numbers, no frame, no white sticker border around the creature. Leave a white margin of at least 60 px on every side.
"""
        p = os.path.join(GUI, f"luot_0_concept_{ma}.txt")
        ghi(p, txt)
        hd += [f"## Hướng {ma} ({vi})", f"- File prompt: `{Wp(p)}`", f"- GPT lưu vào: `{Wp(out)}` (trùng tên thì `_2`, `_3`).\n"]
        print(p)
    hd += ["## Cách kiểm",
           "- Một con hổ con, nhìn ngang quay phải, đứng bốn chân, đầu to khoảng nửa chiều dài, bốn chân đều thấy rõ.",
           "- Một mắt to tròn màu hổ phách, vẻ quả quyết; lửa ít (ruff 4–5 cụm sau gáy, hai chỏm trên mày, một ngọn ở chót đuôi), màu cam lõi vàng.",
           "- Không sừng, không chuông, không vòng, không nanh dài. Tô phẳng, không bóng, không điểm sáng (trừ một chấm trong mắt).\n",
           "## Câu sửa nhanh",
           "- Chưa đủ chibi: \"Make the head bigger and rounder and the legs shorter; fewer details.\"",
           "- Chân bị che: \"Show all four legs clearly, separate from each other, as in image 2.\"",
           "- Có bóng: \"Remove every shadow and highlight; flat colours only.\""]
    ghi(os.path.join(GUI, "HUONG_DAN_concept.md"), "\n".join(hd) + "\n")


# ---------------------------------------------------------------- mảnh của bản CHIBI: gen "đúng chỗ, đúng cỡ" từ concept đã chọn (A)
DUYET = os.path.join(TAI, "L1_duyet.png")
TO_C = {
    "THAN": ("thân (không đầu, chân, đuôi, lửa)",
             "ONLY THE BODY (the torso): the plump cream bean-shaped trunk with its charcoal zigzag stripes, from the rump at the left (where "
             "the tail starts, about x = 420) to the chest at the right (about x = 900); its top line is at about y = 560, its belly at about "
             "y = 780. REMOVE the head with its chin fur, the flame ruff, all other flames, the tail, all four legs and paws. COMPLETE the body "
             "into ONE CLOSED SHAPE: where the head, the flames, the tail and the legs covered it or joined it, continue the body's own "
             "rounded outline and cream fur. The front end is a smooth rounded chest that reaches to about x = 930 (under where the head was); "
             "the top line runs on smoothly under where the flame ruff was; the rump is round; the underside is ONE smooth belly line with NO "
             "leg stumps and no gaps. Add one or two more zigzag stripes of the same kind where the flames used to cover the back."),
    "CHAN": ("bốn chân rời nhau",
             "ONLY THE FOUR LEGS, as FOUR SEPARATE closed shapes, each in the same position and at the same size as in image 1: leg 1 = the "
             "big striped leg at the far left (paw at about x = 340 to 520, y = 800 to 915); leg 2 = the smaller plain leg just right of it "
             "(about x = 555 to 700), which keeps its slightly darker cream; leg 3 = the striped leg in the middle (about x = 735 to 910); "
             "leg 4 = the striped leg at the right (about x = 950 to 1130). REMOVE the body, the head, the tail and all flames. COMPLETE every "
             "leg: where the body covered its top, extend the leg upward by about 70 px and close it with a ROUNDED top end, like a short "
             "plump sausage standing on a big round paw; keep the stripes and the tiny charcoal claw tips. The four shapes must NOT touch each "
             "other: keep clear white space between them."),
    "DUOI": ("đuôi + bờm lửa",
             "ONLY TWO THINGS, as two separate closed shapes in the same positions and at the same sizes as in image 1: (a) the TAIL with the "
             "flame on its tip (about x = 310 to 470, y = 285 to 640): complete its hidden base by extending the lower end about 50 px further "
             "down and to the right, into where the body was, and close it with a rounded end; (b) the FLAME RUFF: the group of orange "
             "flame-cloud curls behind the head (about x = 480 to 790, y = 290 to 600) as ONE closed shape: where the head and the ear covered "
             "its right side, complete it with more flame curls of the same kind reaching about 80 px further right; where it touched the "
             "body, close its lower edge with rounded flame curls. REMOVE the head, the body, the legs and the two small brow flames."),
    "DAU": ("đầu (cả tai, hai chỏm lửa trên mày, mắt, cằm)",
            "ONLY THE HEAD: the whole big round head with both ears, the two small flames on the brow, the forehead stripes, the eye, the "
            "spiral on the cheek, the nose, the mouth with its tiny fang, the chin and the jagged cheek fur (about x = 700 to 1235, y = 100 to "
            "690). REMOVE the body, the legs, the tail and the flame ruff behind the head. COMPLETE the head into ONE CLOSED SHAPE: where the "
            "flame ruff and the body touched it at the lower left, continue the jagged cheek-fur outline all the way around. Do not change the "
            "face."),
}


def manh_prompt():
    hd = ["# Hổ lửa dạng 1 bản CHIBI (hoa_ho_non): lượt mảnh\n",
          f"Concept đã chọn (A): `{Wp(DUYET)}`, 1536x1024, nền trắng: hổ con chibi đứng bốn chân quay phải. Mỗi tờ GPT vẽ lại MỘT phần của "
          "concept, đúng chỗ, đúng cỡ, bỏ hết phần khác và vẽ bù phần bị che thành hình kín.\n"]
    for ma, (vi, cau) in TO_C.items():
        out = os.path.join(TAI, f"C_{ma}.png")
        txt = f"""IMAGES (attached in this order; open each from its path):
image 1 = {Wp(DUYET)}: the APPROVED creature, 1536x1024, white background: a chibi cream-white tiger cub facing right, standing on four short legs, with a huge round head, charcoal zigzag stripes, an orange flame ruff behind the head, two small flames on the brow and a flame on the tip of its short tail. Coordinates below are pixels on this image, x from the left, y from the top.

SAVE: save it as a PNG to {Wp(out)}
If a file with that name already exists, save as C_{ma}_2.png, C_{ma}_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: redraw image 1 with {cau}

SAME POSITION, SAME SIZE: landscape 1536x1024; if your picture were laid over image 1, every part you keep must coincide with the same part there. Do not move, scale, rotate or re-pose anything. A program will cut this picture by position and assemble the pieces.

LINE AND COLOUR: exactly the look of image 1: the same wobbly dark-brown ink pen outline (#2B2118), about 7 px thick, closed all the way around each shape, about 4 px for inner details; the same colours; the same loose diagonal crayon / coloured-pencil hatching inside every area.

{FLAT}

Pure white (#FFFFFF) background everywhere else: no ground, no shadow, no text, no labels, no numbers, no frame, no white sticker border.
"""
        p = os.path.join(GUI, f"luot_2_chibi_{ma}.txt")
        ghi(p, txt)
        hd += [f"## Tờ {ma}: {vi}", f"- File prompt: `{Wp(p)}`", f"- Ảnh mẫu: concept ở trên.", f"- GPT lưu vào: `{Wp(out)}` (trùng tên thì `_2`, `_3`).\n"]
        print(p)
    hd += ["## Cách kiểm", "- Chồng lên concept thì phần giữ lại trùng chỗ, trùng cỡ; mỗi hình có viền mực kín; nền trắng tinh.",
           "- Tờ CHAN: bốn chân rời nhau, đầu trên bo tròn. Tờ THAN: bụng trơn không mẩu chân. Tô phẳng, không bóng.\n",
           "## Câu sửa nhanh", "- Lệch chỗ: \"Keep exactly the position and size of image 1.\"",
           "- Hình chưa kín: \"Close the ink outline all the way around every shape.\""]
    ghi(os.path.join(GUI, "HUONG_DAN_manh_chibi.md"), "\n".join(hd) + "\n")


if __name__ == "__main__":
    lenh = sys.argv[1] if len(sys.argv) > 1 else ""
    if lenh == "to":
        to()
    elif lenh == "cat":
        cat()
    elif lenh == "mat":
        mat()
    elif lenh == "bo_cuc":
        bo_cuc()
    elif lenh == "concept":
        concept()
    elif lenh == "manh_prompt":
        manh_prompt()
    else:
        print(__doc__)
