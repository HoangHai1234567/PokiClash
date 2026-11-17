# -*- coding: utf-8 -*-
"""Bùn Ngoạm Nhi (mã làm việc quai_bun_non): DẠNG 1 của tướng 8 đảo Thổ (ải 50, id `ho_kim_cuong`, dạng 2 = quái bùn `quai_bun`).
Người dùng 2026-11-17: "ok cho vào game, làm dạng 1 đi"; chọn "cùng rig 3668" (đổi tỉ lệ ngay trên rig quái bùn, như Giác Mộc Non /
Thanh Long dạng 1), tên "tùy bạn đặt, đặt dễ hiểu là được". Rig, lưới, chuyển động gốc là của nhà phát hành game tham khảo (monster_3668):
chỉ dùng nội bộ, không đăng công khai.

Quy trình (skill pokiclash-spine-rig, "DẠNG KHÁC trên CÙNG rig gốc"): tỉ lệ trước (mau/ti_le.json, chụp bố cục bằng da cũ:
mo_xe/atomik_bocuc.py), concept vẽ trên bố cục đó, người dùng duyệt, rồi mới làm mảnh + rig (quai_bun_rig.py chế độ dạng non).

    quai_bun_non.py concept     file prompt từng hướng → gui_gpt/quai_bun_non/luot_1_concept_<k>.txt + HUONG_DAN.md
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5  # noqa: E402

CODE = "quai_bun_non"
BASE = os.path.join(HERE, "inbox", CODE)
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
GUI = os.path.join(HERE, "gui_gpt", CODE)
# khung nhìn của bo_cuc.png (đơn vị rig, x0, y0, x1, y1) trên 1536x1024: 1,01 px / đơn vị
KHUNG = (-760.0, -80.0, 760.0, 933.0)
TI_LE = os.path.join(MAU, "ti_le.json")   # bone2 0,8; đầu bone5 1,45; tay bone7 / bone19 0,85; dải bùn bone50 / lujing_04 0,4

R1 = (os.path.join(MAU, "bo_cuc.png"),
      "the PROPORTION GUIDE, 1536x1024, white background: our adult hero re-proportioned as its YOUNG form on the same skeleton (bigger "
      "head and jaw, smaller body hump, smaller arms and fists, short strands), still wearing the adult's skin. Keep its pose, its facing, "
      "its size and place on the canvas and where every part is; redraw the surface as the young form described below",
      "Bố cục dạng non: rig quái bùn đổi tỉ lệ (đầu + hàm to, thân gù nhỏ, tay nhỏ, dải bùn ngắn), còn mang da dạng 2, nền trắng 1536×1024. "
      "Giữ dáng, chỗ, cỡ từng bộ phận")
R2 = (os.path.join(HERE, "inbox", "quai_bun_1", "tai_ve", "L1_duyet.png"),
      "the APPROVED ADULT form of the same hero, 1536x1024, white background: the young form must clearly be the SAME creature at a "
      "younger age: same materials (chocolate mud, grey river stones, amber mouth), same colours, same pen line, crayon hatching and "
      "flat colouring. Do NOT copy its adult proportions (image 1 gives the proportions)",
      "Concept dạng 2 (quái bùn) đã duyệt: lấy chất liệu, màu, nét bút, vân sáp; không lấy tỉ lệ người lớn")

PLAN = (
    "BODY PLAN (from image 1, keep it; it is animated with the same skeleton as image 2): a young blob-brute of wet mud turned to the "
    "RIGHT. (1) BODY: a SMALL rounded hump at the upper left, behind the head. (2) HEAD: BIG for the body, at the upper right; two eyes "
    "side by side on the upper face (three-quarter view to the right). (3) MOUTH (keep this construction exactly): the mouth opens "
    "DOWNWARD from under the head; the head is the UPPER jaw, the big round tan belly under it is the LOWER jaw; teeth along the rim of "
    "both jaws; the amber inside of the mouth is the tall area right of the centre. (4) NEAR ARM on the LEFT: a short arm from the hump "
    "down to a SMALL fist resting at the lower left of centre. (5) FAR ARM on the RIGHT: a short arm behind the head down to a small fist "
    "resting on the belly at the lower right. (6) BASE: no legs: the body melts into a flat mud puddle spreading to the lower LEFT. "
    "(7) STRANDS: only a few SHORT mud drips on the back, where image 1 has them. Same size and same place on the canvas as image 1; "
    "every part keeps about the same size and outline as in image 1.")

CHUNG = [
    "MATERIAL: the same thick wet MUD as image 2 but a little lighter and smoother, like fresh young mud: chocolate brown #6E4C37 on the "
    "faces turned to the viewer, #523826 on the faces turned away; the belly / lower jaw a lighter muddy tan #9A7552. Two small round mud "
    "bubbles on the hump, nothing else.",
    "EYES: BIGGER than image 2 for a youngster: two round flat amber-yellow eyes #F2B33A with a dark pupil and ONE small white dot each, "
    "under a short mud brow that is FROWNING: a determined, ready-to-fight little face (fierce-cute, not sad, not silly).",
    "MOUTH: the inside a flat amber-ochre #E9A63B (darker #C98426 back wall); SMALL rounded baby PEBBLE TEETH in pale stone #D6D0C0, "
    "fewer and smaller than image 2, with gaps between them.",
    "FISTS: each a small bunch of THREE rounded grey river pebbles #9A968B (side faces #77736A) held in mud (image 2 has big stone fists; "
    "the young one only has pebbles).",
    "STRANDS: three or four SHORT stubby mud drips on the back, each ending in a round drop; no long strands.",
    "BASE: a smaller wet mud puddle, one or two drip blobs on its edge, one small pebble in it.",
    "NO plants, no moss, no glow.",
]

HUONG = {
    "A": ("bùn non sừng cuội nhú",
          "như dạng 2 nhưng non: bùn sô-cô-la sáng hơn, mắt hổ phách to, răng cuội sữa thưa, nắm tay ba viên sỏi, hai SỪNG CUỘI NHÚ tí "
          "trên đầu (dạng 2 thành sừng đá), vài giọt bùn ngắn trên lưng",
          ["HEAD: a smooth rounded MUD head with a short frowning brow ridge; TWO tiny round grey river-stone NUBS #A7A397 just poking "
           "out of the top of the head (the stubs of the adult's stone horns, a third of their length)."]),
    "B": ("bùn non đội VỎ TRỨNG ĐÁ vỡ",
          "điểm nhấn: nửa VỎ TRỨNG ĐÁ CUỘI vỡ răng cưa đội trên đầu như mũ (con non mới nở từ trứng đá; lớn lên mảnh vỏ thành hai sừng "
          "đá), hai mắt to dưới mép vỏ, phần còn lại như hướng A",
          ["HEAD: a rounded MUD head wearing the broken top HALF OF A STONE EGG like a helmet: a smooth pale grey river-stone shell "
           "#B9B5A9 (side faces #96928A) with a jagged zig-zag broken rim sitting low over the brow, ONE small crack line on it; the big "
           "frowning eyes peek out just under the rim. No horns (the shell shards become the adult's stone horns later)."]),
}

DETAIL = ("DETAIL: about as much detail as image 2 or less: big simple rounded masses, each a flat colour, at most one or two inner lines "
          "per piece; only the details listed under DESIGN.")
MOOD = ("MOOD: the YOUNG form of a fierce earth brute: chunky, a big head, small limbs, a determined frown, ready to fight; likeable, "
        "not a mascot, not babyish-silly, not horror.")


def task():
    return ("TASK: redraw image 1 as the YOUNG FORM (first evolution stage) of the hero in image 2. Keep image 1's pose, facing, size, place "
            "on the canvas and the outline of every part (it is animated with the same skeleton); give it the surface, materials and "
            "colours of image 2 made younger, as described below. Every limb and the head stay joined to the body (no white gaps).")


def concept():
    R = [R1, R2]
    hd = ["# Gói gen: Bùn Ngoạm Nhi (`quai_bun_non`), dạng 1 tướng 8 đảo Thổ (ải 50)", "",
          "Rig: `monster_3668` (game tham khảo) đổi tỉ lệ. Ảnh mẫu 1 mang lưới / da dựng từ rig đó: chỉ dùng trong máy, không đăng công khai.", "",
          "## Lượt 1: concept dạng 1, hai hướng (2026-11-17, Magnific GPT 2.6, 1k high, 95 credit / ảnh)", "",
          "Người dùng: \"ok cho vào game, làm dạng 1 đi\", chọn dựng trên cùng rig quái bùn. Ảnh 1 là bố cục dạng non (tỉ lệ đã đổi trên rig, "
          "còn mang da dạng 2); ảnh 2 là concept dạng 2 đã duyệt để giữ nhận diện.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{tho5.Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, rieng) in HUONG.items():
        out = os.path.join(TAI, f"L1_{k}.png")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {tho5.Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {tho5.Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.",
              "", task(), "", PLAN, "", "DESIGN:"] + [f"- {d}" for d in rieng + CHUNG] + ["", DETAIL, "", tho5.style(), "", MOOD, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same "
              "place and size as in image 1. No sparkles, no glints, no glow, no aura round the character, no smoke, no speed lines, no "
              "labels, no frame."]
        tho5.ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): file prompt `{tho5.Wp(p)}`; ảnh lưu vào `{tho5.Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, chỗ, cỡ từng bộ phận như ảnh 1 (đầu + hàm dưới to, thân gù nhỏ, tay ngắn, nắm tay nhỏ đúng chỗ, vũng bùn loang "
           "trái); rõ là cùng loài với ảnh 2 (bùn sô-cô-la, đá cuội xám, lòng miệng hổ phách); mặt quả quyết; nét bút mực rung, vân sáp, tô "
           "phẳng, không bóng, không quầng sáng; nền trắng tinh.",
           "", "Câu sửa nhanh: \"too many details: simplify\"; \"remove the shading / highlights / glow, flat colour only\"; \"keep every part "
           "at the same place and size as image 1\"."]
    tho5.ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


# ================================================================ mảnh (concept A duyệt 2026-11-17)
# Phần lớn mảnh dạng 2 chỉ ĐỔI MÀU (giữ lưới); chỉ gen lại chỗ khác hẳn: đầu (sừng nhú, răng sữa trên), hàm dưới (răng sữa), mặt quả bóng.
# Mảnh đầu / hàm cắt trên khung concept dạng 1 rồi quy về khung concept dạng 2 bằng nghịch đảo phép biến đổi của cây xương đầu (bone5).
DUYET = os.path.join(TAI, "L1_duyet.png")
ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: a YOUNG MUD MONSTER turned to the right: a small chocolate-"
        "brown mud body hump on the left with two small mud bubbles and three short mud drips, a BIG rounded mud head at the upper right "
        "with a short frowning brow ridge, two big round amber eyes and two tiny grey river-stone nubs on top, a mouth opening downward from "
        "under the head (amber-ochre inside, small rounded pale pebble baby teeth with gaps), a big light-tan round belly that is the lower "
        "jaw, two small fists of three grey pebbles, a flat mud puddle as its base. Hand-drawn: wobbly dark-brown ink line, crayon hatching, "
        "flat colours.")
STYLE = ("Same wobbly dark-brown ink line (about 7 px), same colours, same crayon hatching, same completely flat colouring as image 1 (no "
         "shading, no highlights, no glow, no shadows).")
VIEN = ("complete it into ONE CLOSED SHAPE with the dark-brown ink outline all the way round; where it is hidden behind another part in "
        "image 1, draw the hidden portion as it would continue (plain mud of the same colour, same flat crayon colouring)")
TAM = {"dau": (1010, 450), "ham": (900, 800)}
NHOM = {
    "dau": ("the HEAD = the UPPER JAW: the big rounded mud head at the upper right with its short frowning brow ridge, its blunt rounded "
            "snout at the right (right edge at about x 1200, between y 400 and y 565), the two tiny grey river-stone NUBS on its top (at about "
            "(945-1030, 305-370) and (1085-1150, 340-395)), and the row of small rounded pale pebble UPPER TEETH hanging down along the TOP "
            "edge of the mouth (at about (885-940, 525-560), (1005-1060, 552-582) and (1100-1140, 588-610)); its lower-left part, the cheek "
            "left of the mouth, comes down to about (745-840, 600); its back (left) side meets the body hump at about x 830",
            "draw it WITHOUT the two eyes: where the big amber eyes are (about (985-1075, 430-500) and (1100-1162, 468-522)), plain mud face, "
            "with the frowning brow ridge kept above them; WITHOUT any mud drip; WITHOUT the lower teeth, the amber inside of the mouth and "
            "the belly: the lower edge of the head in front is the row of upper teeth (outlined in ink); the back of the head on the left, "
            "hidden behind the body hump, is a rounded edge reaching left to about x 800. " + VIEN),
    "ham": ("the BELLY = the LOWER JAW: the big light-tan round belly in the middle, from about x 690 to x 1145 and from the bottom lip of "
            "the mouth (about y 580 at its upper-left corner) down to about y 985 (its rounded bottom resting on the puddle), with the row of "
            "small rounded pale pebble LOWER TEETH standing along its rim on the LEFT and BOTTOM edges of the mouth (at about (815-858, "
            "578-622), (865-920, 640-685), (970-1030, 698-738) and (1062-1112, 722-768))",
            "draw it WITHOUT the amber inside of the mouth (the rim of the belly with its teeth is its upper edge), WITHOUT the pebble fist "
            "(continue the plain tan belly where the three grey pebbles at about (915-1030, 755-830) cover it), WITHOUT the upper teeth, the "
            "head and the puddle; its left side, hidden behind the body, continues as a rounded edge. " + VIEN),
}
BONG_NEN = os.path.join(MAU, "bong_mat_nen.png")      # bong_mat dạng 2 (596x699) giữa nền trắng 1536x1024, chỗ đặt ở bong_mat_nen.json


def luu(ten):
    out = os.path.join(TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {tho5.Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


def prompt_manh():
    ra = []
    for nh, (mt, kh) in NHOM.items():
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {tho5.Wp(DUYET)}: {ANH1}", ""] + save + ["",
             "TASK: redraw image 1 with ONLY the part described under KEEP, in exactly the SAME POSITION and at exactly the SAME SIZE as in "
             "image 1 (if the new picture were laid over image 1, the kept part must coincide with image 1). REMOVE everything else (leave "
             "pure white there). " + STYLE + " Do not move, resize, rotate or redesign anything.",
             "", f"KEEP: {mt}: {kh}.",
             "", "CANVAS: landscape 1536x1024, plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles, no loose drops."]
        tho5.ghi(p, t)
        ra.append((nh, p, out))
        print(p)
    out, save = luu("M_bong")
    p = os.path.join(GUI, "luot_2_bong.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {tho5.Wp(BONG_NEN)}: the ADULT form of our hero curled into a round mud BALL with a strained face (bulging eyes, lips "
         "pressed shut, one small tooth poking out, two grey stone fists hugging the light belly, two drips and two stone horns on top), "
         "alone in the middle of a 1536x1024 white canvas",
         f"image 2 = {tho5.Wp(DUYET)}: {ANH1} This is the YOUNG form; its ball must look like it.", ""] + save + ["",
         "TASK: redraw image 1 as the YOUNG form's ball. Keep EXACTLY the same round outline, the same size and the same position on the "
         "canvas (laid over image 1 the ball must coincide), the same pressed-shut mouth with one small tooth poking out, the same strained "
         "expression and the same two hands hugging the belly at the same places. Change ONLY:",
         "1. COLOURS: the lighter young mud of image 2: chocolate brown #6E4C37 (side faces #523826), the belly light tan #9A7552.",
         "2. HORNS: replace the two grey stone horns by two TINY grey river-stone nubs #A7A397 at the same places (like image 2's nubs, a "
         "third of the horns' size).",
         "3. EYES: BIGGER round amber eyes #F2B33A like image 2's (dark pupil, one small white dot), still wide open and strained, under a "
         "frowning brow.",
         "4. HANDS: each hand becomes a small bunch of THREE round grey pebbles #9A968B held in mud, like image 2's fists, at the same "
         "places.",
         "5. TOP: keep at most two SHORT stubby mud drips on top of the ball.",
         "", STYLE.replace("image 1", "image 2"), "No other changes, no new details.",
         "", "CANVAS: landscape 1536x1024, plain pure-white background (#FFFFFF), the ball where it is in image 1, no labels, no shadows, "
         "no sparkles, no loose drops."]
    tho5.ghi(p, t)
    ra.append(("bong", p, out))
    print(p)
    hd = ["# Gói gen: Bùn Ngoạm Nhi (`quai_bun_non`), lượt 2: mảnh", "",
          "Concept duyệt: `" + tho5.Wp(DUYET) + "` (hướng A, người dùng chọn 2026-11-17). Phần lớn mảnh dạng 2 chỉ đổi màu bằng mã; ba "
          "tờ dưới gen lại chỗ khác hẳn (Magnific GPT 2.6, 1k high, 95 credit / tờ).", "",
          "| Tờ | File prompt | Ảnh mẫu | Lưu vào |", "|---|---|---|---|",
          f"| Đầu (hàm trên: sừng nhú, răng sữa trên, bỏ mắt) | `{tho5.Wp(ra[0][1])}` | concept duyệt (con non quay phải, nền trắng 1536×1024) "
          f"| `{tho5.Wp(ra[0][2])}` |",
          f"| Hàm dưới (bụng be + răng sữa dưới) | `{tho5.Wp(ra[1][1])}` | như trên | `{tho5.Wp(ra[1][2])}` |",
          f"| Quả bóng mặt căng | `{tho5.Wp(ra[2][1])}` | ảnh 1: quả bóng dạng 2 (596×699) giữa nền trắng 1536×1024; ảnh 2: concept duyệt "
          f"| `{tho5.Wp(ra[2][2])}` |", "",
          "Kiểm: mảnh đúng chỗ, đúng cỡ như concept (đặt chồng lên thì trùng), viền mực kín, phần khuất vẽ tiếp bằng bùn trơn; đầu không có "
          "mắt; quả bóng giữ nguyên viền tròn và chỗ đặt, chỉ đổi màu, sừng, mắt, tay. Câu sửa nhanh: \"keep it at the same place and size "
          "as image 1\"; \"remove the eyes, plain mud face there\"; \"flat colour only, no shading\"."]
    tho5.ghi(os.path.join(GUI, "HUONG_DAN_luot_2.md"), hd)


# ================================================================ cắt mảnh → inbox/quai_bun_non/manh/ (khung concept DẠNG 2)
MANH2 = os.path.join(HERE, "inbox", "quai_bun_1", "manh")
MANH = os.path.join(BASE, "manh")
EYE_BOX = (975, 420, 1175, 528)                   # vùng hai mắt trên concept dạng 1 (px)
EYE_TAM = [(1030, 465), (1131, 495)]


def ma_tran():
    """affine 2x3: px concept dạng 1 → px concept dạng 2 (qua đơn vị rig dạng 1 → nghịch đảo biến đổi cây đầu bone5 ở khung 0 idle →
    đơn vị rig dạng 2 → px concept dạng 2 theo goc_ca_con.json)."""
    import json
    import numpy as np
    import cv2
    sys.path.insert(0, os.path.join(HERE, "mo_xe"))
    import atomik_dang as A
    to_rig_b, _, _ = A.canvas_map(KHUNG, 1536, 1024)
    T = np.array(json.load(open(os.path.join(MAU, "T_idle0.json")))["bone5"])
    j = json.load(open(os.path.join(HERE, "inbox", "quai_bun_1", "mau", "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    P = np.array([[0.0, 0.0], [1536.0, 0.0], [0.0, 1024.0]], np.float32)
    R = to_rig_b(P)
    Ra = (np.linalg.inv(T) @ np.c_[R, np.ones(3)].T).T[:, :2]
    Q = np.c_[1536 / 2 + (Ra[:, 0] - cx) * s, 1024 / 2 - (Ra[:, 1] - cy) * s].astype(np.float32)
    return cv2.getAffineTransform(P, Q)


def ve_sang_khung2(rgba, M):
    """ảnh RGBA cả khung concept dạng 1 → khung dạng 2 (nhân sẵn alpha khi nội suy), cắt sát; trả (ảnh, hộp px dạng 2)."""
    import numpy as np
    import cv2
    from PIL import Image
    a = rgba.astype(np.float32) / 255.0
    pre = np.dstack([a[..., :3] * a[..., 3:4], a[..., 3:4]])
    w = cv2.warpAffine(pre, M, (1536, 1024), flags=cv2.INTER_CUBIC, borderValue=(0, 0, 0, 0))
    al = np.clip(w[..., 3], 0, 1)
    rgb = np.where(al[..., None] > 1e-3, w[..., :3] / np.maximum(al[..., None], 1e-3), 0)
    out = (np.dstack([np.clip(rgb, 0, 1), al]) * 255).astype(np.uint8)
    ys, xs = np.nonzero(out[..., 3] > 8)
    x0, y0, x1, y1 = xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3
    return Image.fromarray(out[y0:y1, x0:x1], "RGBA"), [int(x0), int(y0), int(x1), int(y1)]


def cat_manh():
    import json
    import shutil
    import numpy as np
    import cv2
    from PIL import Image, ImageDraw
    import quai_bun_manh as QM                     # rgba_tu, nen, dong_lo, el (chỉ dùng hàm)
    os.makedirs(MANH, exist_ok=True)
    DAT = json.load(open(os.path.join(MANH2, "dat.json"), encoding="utf-8"))
    for f in os.listdir(MANH2):                   # mảnh dạng 2 dùng lại nguyên (màu concept dạng 1 đo ra trùng màu mảnh dạng 2)
        if f.endswith(".png") and not f.startswith("_"):
            shutil.copyfile(os.path.join(MANH2, f), os.path.join(MANH, f))
    M = ma_tran()
    C = np.asarray(Image.open(DUYET).convert("RGB").resize((1536, 1024), Image.LANCZOS)).astype(np.int32)
    # mắt mở: cụm vàng hổ phách trong vùng mắt (bao lồi, nới 5 px lấy vành mực); mắt nhắm: tô da + một nét mí cong
    x0, y0, x1, y1 = EYE_BOX
    sub = C[y0:y1, x0:x1]
    vang = (sub[..., 0] > 200) & (sub[..., 1] > 120) & (sub[..., 2] < 120) & (sub[..., 0] - sub[..., 2] > 110)
    vang = cv2.morphologyEx(vang.astype(np.uint8), cv2.MORPH_CLOSE, QM.el(8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(vang, 8)
    ids = [min(range(1, n), key=lambda i: np.hypot(cen[i][0] + x0 - tx, cen[i][1] + y0 - ty)) for tx, ty in EYE_TAM]
    full = np.zeros((1024, 1536), bool)
    hulls = []
    for i in ids:
        ys, xs = np.nonzero(lab == i)
        hull = cv2.convexHull(np.stack([xs + x0, ys + y0], 1).astype(np.int32))
        cv2.fillPoly(full.view(np.uint8), [hull], 1)
        hulls.append(hull.reshape(-1, 2))
    full = cv2.dilate(full.astype(np.uint8), QM.el(5)).astype(bool)
    mo = np.asarray(QM.rgba_tu(C.astype(np.uint8).copy(), full))
    im, hop = ve_sang_khung2(mo, M)
    im.save(os.path.join(MANH, "mat.png"))
    DAT["mat"] = dict(hop=hop, nguon="quai_bun_non L1_duyet.png (cắt thẳng, quy về khung dạng 2)")
    print("mat", hop, im.size)
    vung = C[350:560, 940:1200].reshape(-1, 3)
    nau = vung[(vung[:, 0] > 95) & (vung[:, 0] < 170) & (vung[:, 2] < 90) & (vung[:, 0] - vung[:, 2] > 50)]
    da = np.median(nau, 0).astype(np.uint8)
    a = mo.copy()
    trong = cv2.erode(full.astype(np.uint8), QM.el(4)).astype(bool)
    a[trong, :3] = da
    can = Image.fromarray(a, "RGBA")
    d = ImageDraw.Draw(can)
    for hull in hulls:
        xa, xb = hull[:, 0].min() + 1, hull[:, 0].max() - 1
        ym, hh = (hull[:, 1].min() + hull[:, 1].max()) / 2, hull[:, 1].max() - hull[:, 1].min()
        pts = [(xa + (xb - xa) * u, ym + 0.20 * hh * np.sin(np.pi * u)) for u in np.linspace(0, 1, 14)]
        d.line(pts, fill=QM.INK + (255,), width=6, joint="curve")
    im2, hop2 = ve_sang_khung2(np.asarray(can), M)
    im2.save(os.path.join(MANH, "mat_nham.png"))
    DAT["mat_nham"] = dict(hop=hop2, nguon=f"dựng từ mặt nạ mắt dạng 1 (tô da {da.tolist()} + mí), quy về khung dạng 2")
    # đầu, hàm dưới: tờ gen (khung dạng 1) → tách nền → khung dạng 2
    for nh in ("dau", "ham"):
        src = os.path.join(TAI, f"M_{nh}.png")
        if not os.path.exists(src):
            print(nh, "chưa gen")
            continue
        S = np.asarray(Image.open(src).convert("RGB").resize((1536, 1024), Image.LANCZOS)).astype(np.int32)
        fg = ~QM.nen(S)
        n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        tx, ty = TAM[nh]
        ids = [i for i in range(1, n) if st[i, 4] > 2000 or (st[i, 4] > 30 and np.hypot(cen[i][0] - tx, cen[i][1] - ty) < 260)]
        m = QM.dong_lo(np.isin(lab, ids))
        rg = np.asarray(QM.rgba_tu(S.astype(np.uint8).copy(), m))
        im, hop = ve_sang_khung2(rg, M)
        im.save(os.path.join(MANH, f"{nh}.png"))
        DAT[nh] = dict(hop=hop, nguon=f"quai_bun_non M_{nh}.png, quy về khung dạng 2")
        print(nh, hop, im.size, f"{len(ids)} cụm")
    # quả bóng: cắt đúng ô của bong_mat dạng 2 (cùng khung, cùng hop)
    src = os.path.join(TAI, "M_bong.png")
    if os.path.exists(src):
        o = json.load(open(os.path.join(MAU, "bong_mat_nen.json")))
        S = np.asarray(Image.open(src).convert("RGB").resize((1536, 1024), Image.LANCZOS)).astype(np.int32)
        fg = ~QM.nen(S)
        n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        big = 1 + int(np.argmax(st[1:, 4]))
        m = QM.dong_lo(lab == big)
        rg = np.asarray(QM.rgba_tu(S.astype(np.uint8).copy(), m))
        crop = rg[o["y0"]:o["y0"] + o["h"], o["x0"]:o["x0"] + o["w"]]
        Image.fromarray(crop, "RGBA").save(os.path.join(MANH, "bong_mat.png"))
        a2 = np.asarray(Image.open(os.path.join(MANH2, "bong_mat.png")).convert("RGBA"))[..., 3] > 127
        a1 = crop[..., 3] > 127
        print("bong_mat IoU với dạng 2", round((a1 & a2).sum() / (a1 | a2).sum(), 3), "(thừa ra ngoài khung:",
              int(m.sum() - a1.sum()), "px)")
    json.dump(DAT, open(os.path.join(MANH, "dat.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "concept":
        concept()
    elif cmd == "manh":
        prompt_manh()
    elif cmd == "cat":
        cat_manh()
    else:
        print(__doc__)
