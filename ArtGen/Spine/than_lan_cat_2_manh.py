# -*- coding: utf-8 -*-
"""Sa Tích DẠNG 2 (than_lan_cat_2, rig monster_3530; ghi chú inbox/than_lan_cat_2_ghichu.md): mảnh "ĐÚNG CHỖ, ĐÚNG CỠ".

Concept duyệt (tai_ve/L1_duyet.png = L1_A, người dùng 2026-11-17: "ok concept 3 con kia ổn rồi làm đi") giữ thiết kế dạng 1 nhưng dáng còn
nằm rạp như dạng 1, to hơn khung rig. Bước 1 (`tuthe`): một ảnh vẽ lại ĐÚNG thiết kế đó trong ĐÚNG dáng, chỗ, cỡ của con gốc 3530 (ngồi xổm
thẳng lưng, hai tay buông trước bụng) → tai_ve/L2_tuthe.png = "concept nắn". Bước 2: các tờ mảnh cắt từ concept nắn (như than_lan_cat_manh).

Mảnh (tên ảnh → slot của họ, xem than_lan_cat_2_rig.SLOT):
    than                 thân + bụng kem (gộp chest1..3, tail1..3)             T1
    dau                  đầu (mõm, mày giáp đá), KHÔNG mắt                     T2
    duoi                 đuôi + khoanh phiến                                   T2
    tay_xa / tay_gan     tay trước xa (phải, sau thân) / gần (trái, trước)       T3 / T2
    chan_xa / chan_gan   chân sau xa (phải) / gần (trái), không phiến           T3
    p1..p6               sáu phiến đất nung lưng / mũ trùm (beici1..6)          T4, T5
    pc                   phiến trên gáy (weici4)                                T5
    pd1..pd3             ba phiến đuôi (weici1..3)                              T3
    sl / sr              hai phiến mào dựng sau đầu (thay hai sừng râu jiaol/r)  T4
    ml / mr              mảng mày giáp đá (thay mml / mmr)                      cắt thẳng từ concept nắn
    lg1 lg2 / lx1 lx2    phiến giáp chân gần / xa (thay lá footl_3/1, footr_3/4) T5
    mat / mat_nham       mắt mở (cắt thẳng) / mắt nhắm (dựng từ mặt nạ mắt)

    than_lan_cat_2_manh.py tuthe        file prompt concept nắn → gui_gpt/than_lan_cat_2/luot_2_tuthe.txt
    than_lan_cat_2_manh.py so_tuthe     chồng hình bóng con gốc lên concept nắn, IoU → mau/_so_tuthe.png
    than_lan_cat_2_manh.py prompt       sáu tờ mảnh trên concept nắn → gui_gpt/than_lan_cat_2/luot_3_T1..T6.txt
    than_lan_cat_2_manh.py cat [tờ]     cắt tờ (tai_ve/M_<tờ>.png) → manh/<tên>.png + manh/dat.json
    than_lan_cat_2_manh.py mat          mắt mở cắt thẳng từ concept nắn + mắt nhắm dựng từ mặt nạ → manh/mat*.png
    than_lan_cat_2_manh.py duoi         bỏ khối đùi thừa GPT vẽ dính vào mảnh đuôi
    than_lan_cat_2_manh.py ham          tách hàm dưới + dựng lòng miệng từ mảnh đầu
    than_lan_cat_2_manh.py lot          lớp lưng da khaki sau mũ trùm (gốc phiến cắm lên lưng, không khe nền)
    than_lan_cat_2_manh.py ghep         ghép mọi mảnh theo thứ tự vẽ cạnh concept nắn → manh/_ghep.png + IoU
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5  # noqa: E402
import tho5_dang2 as D2  # noqa: E402

G = D2.dat2("than_lan_cat")
W, H = 1536, 1024
DUYET = os.path.join(G.TAI, "L1_duyet.png")
TUTHE = os.path.join(G.TAI, "L2_tuthe.png")
GOC = os.path.join(G.MAU, "goc_ca_con.png")
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "than_lan_cat_2")


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


def prompt_tuthe():
    out, save = luu("L2_tuthe")
    p = os.path.join(GUI, "luot_2_tuthe.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(GOC)}: the POSE GUIDE (a game reference painted in a smooth digital style, 1536x1024, white background): a squat "
         "spiky lizard sitting UPRIGHT on its haunches, facing right. Use it ONLY for the pose, the layout of the body parts, the size and "
         "the place on the canvas; do NOT copy its colours, its leaf shapes, its spikes, its face or its painting style.",
         f"image 2 = {Wp(DUYET)}: our APPROVED character (1536x1024, white background): an armoured desert lizard with a short wedge head, "
         "a heavy faceted sandstone brow helmet, a fierce yellow slit-pupil eye, small fangs, dusty khaki-ochre skin, a cream throat and "
         "belly, a raised hood of overlapping terracotta clay plates with cream rims, clay armour plates on the limbs and a tail ringed "
         "with clay plates. It is drawn in our hand-drawn style. Keep THIS character's design, colours and style exactly.",
         ""] + save + ["",
         "TASK: redraw the character of image 2 in EXACTLY the pose of image 1: if the new picture were laid over image 1, every body part "
         "must sit where the matching part of image 1 is, at the same size, pointing the same way. Only the DESIGN changes (it is image "
         "2's character), never the pose, the layout or the size.",
         "",
         "WHAT GOES WHERE (left / right as seen by the viewer):",
         "- BODY: the same round upright body as image 1 (sitting on its haunches, the round belly low in the middle); dusty khaki-ochre "
         "#B9A06A skin, the cream #EEDDB0 throat and belly exactly where image 1's pale belly is.",
         "- HEAD: image 2's head exactly where image 1's head is (upper right), the same size as image 1's head: short blunt wedge head, "
         "khaki, the heavy faceted cream sandstone #EAD3A6 brow helmet over the eyes (where image 1's two white brow crests are), the "
         "near eye big (yellow iris #F2C640, black slit pupil, one small white dot) exactly where image 1's left eye is and the far eye "
         "just peeking where image 1's right eye is, a closed mouth line with two small fangs at the corner.",
         "- CREST: the two thin horns on top of image 1's head become two TALL NARROW terracotta #B5603A clay crest plates with cream rims, "
         "in the same places, the same height and the same direction as those horns.",
         "- HOOD AND BACK: every big yellow spike of image 1 behind the head and down the back becomes ONE flat terracotta #B5603A clay "
         "plate with a cream #EAD3A6 rim and a blunt point, in the same place, size and direction as that spike; together they form a "
         "raised hood behind the head (like image 2), overlapping like armour scales.",
         "- TAIL: image 1's short tail at the lower left, khaki with two terracotta ring plates; its small yellow spikes become small "
         "terracotta plates.",
         "- FRONT ARMS: both front arms hang in front of the belly exactly as in image 1 (the near arm on the left side of the belly, the "
         "far arm at the right, partly behind the body); khaki skin, ONE terracotta clay armour plate on each forearm (where image 1's "
         "big leaf on the arm is), three short dark-brown #5E4330 claws at each hand.",
         "- BACK LEGS: the two thick folded back legs at the bottom exactly as in image 1, khaki; each light leaf-shaped piece on the legs "
         "becomes a terracotta clay armour plate, and the feet end in short dark-brown claws.",
         "- NO green, no yellow spikes, no leaves, no white brows.",
         "",
         "DRAWING STYLE: exactly image 2's style: a wobbly dark-brown ink outline (#2B2118, about 7 px) round every piece, thinner ink lines "
         "(about 4 px) for the few inner lines, every area ONE flat colour with visible coloured-pencil / wax-crayon hatching; no shading, "
         "no highlights, no gradients, no glow, no shadows, no shine. Few details: nothing beyond what is listed.",
         "",
         "MOOD: a cute but battle-ready pet creature, a fierce determined face.",
         "",
         "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow, the character at the same place and "
         "size as in image 1. No sparkles, no glow, no dust, no labels, no frame."]
    ghi(p, t)
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().rstrip("\n").split("\n")
    if "luot_2_tuthe" not in "\n".join(cu):
        cu += ["", "## Lượt 2: concept nắn về dáng rig 3530 (2026-11-17, agent dạng 2)", "",
               "Concept duyệt (L1_A) giữ dáng nằm rạp của dạng 1, to hơn khung rig. Lượt này vẽ lại đúng thiết kế đó trong đúng dáng, chỗ, cỡ "
               "của con gốc 3530 để các mảnh lắp đúng lưới.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
               f"| 1 | `{Wp(GOC)}` | Con gốc 3530 khung 0 idle (chỉ lấy dáng, chỗ, cỡ) |",
               f"| 2 | `{Wp(DUYET)}` | Concept dạng 2 đã duyệt (thiết kế, màu, nét) |", "",
               f"- Chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`.",
               "- Kiểm: chồng lên con gốc thì từng phần trùng chỗ (đầu, hai tay trước bụng, hai chân sau, đuôi, các phiến thay gai); đúng màu, "
               "nét của concept duyệt; không còn xanh lá, gai vàng."]
        ghi(hd, cu)
    print(p)


def _mat_na(p):
    a = np.asarray(Image.open(p).convert("RGB").resize((W, H)), np.int16)
    m = Image.fromarray((((255 - a).max(2) > 28) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    f = m.copy()
    ImageDraw.floodfill(f, (0, 0), 128)
    return np.asarray(f) != 128


def so_tuthe(ten="L2_tuthe.png"):
    p = os.path.join(G.TAI, ten)
    g, m = _mat_na(GOC), _mat_na(p)
    iou = (g & m).sum() / max(1, (g | m).sum())
    gi = Image.fromarray((g * 255).astype(np.uint8))
    vien = np.asarray(gi.filter(ImageFilter.MaxFilter(5))) ^ np.asarray(gi.filter(ImageFilter.MinFilter(3)))
    im = np.asarray(Image.open(p).convert("RGB").resize((W, H))).copy()
    im[vien > 0] = (230, 30, 30)
    Image.fromarray(im).save(os.path.join(G.MAU, "_so_tuthe.png"))
    print(ten, f"IoU với con gốc {iou:.3f}")


# ================================================================ tờ mảnh trên concept nắn (L2_tuthe.png)
NAN = TUTHE
# tâm dự kiến (px concept nắn) để gán cụm cắt ra đúng tên
TAM = {"than": (860, 690), "dau": (960, 460), "duoi": (480, 700), "chan_xa": (930, 840), "tay_gan": (770, 680), "tay_xa": (1010, 680),
       "p3": (815, 270), "chan_gan": (620, 800), "p2": (640, 370), "sr": (1065, 240), "pe2": (745, 535), "p1": (760, 355),
       "p5": (600, 505), "p4": (1000, 280), "sl": (930, 240), "p6": (620, 590), "pe1": (765, 445), "pc": (1048, 300)}
VIEN = ("complete it into ONE CLOSED SHAPE with the dark-brown ink outline all the way round; where it is hidden behind another part in "
        "image 1, draw the hidden portion as it would continue (same colours, same flat crayon colouring)")
NHOM2 = {
    "T1": [("than", "the BODY: the neck under the head, the round upright torso sitting on its haunches, the dusty khaki-ochre skin and the "
            "cream throat and belly running down its front (about x 650-1060, y 420-900)",
            "draw it WITHOUT the head, WITHOUT any clay plate, WITHOUT the arms, WITHOUT the legs and WITHOUT the tail: the top of the neck, "
            "hidden behind the head, continues as a plain rounded khaki neck; the back, hidden under the clay plates, continues as plain khaki "
            "skin with a rounded outline; where the arms and legs cover it, continue the khaki side and the cream belly; the bottom is a "
            "rounded belly resting on the ground")],
    "T2": [("dau", "the HEAD: the short wedge head with the heavy faceted cream sandstone brow helmet on top (from about (800, 400) to "
            "(1110, 395)), the khaki face and snout ending at the right at about x 1110, the closed mouth line and the two small fangs, "
            "down to the jaw line at about y 560",
            "draw it WITHOUT the eyes: where the two yellow eyes are, plain khaki face skin (the helmet's lower edge stays where it is). "
            "Its back, hidden behind the clay plates and crest, continues as a rounded back of the head; its lower edge is the jaw and "
            "throat line (the neck is not drawn)"),
           ("duoi", "the TAIL at the lower left: the khaki tail curling up to the pointed tip at about (430, 620), with its terracotta "
            "ring plates (the plate on the tip, the ring at the bottom near (470, 760)) and the small pointed terracotta plate standing "
            "behind it at about (570, 660)",
            "complete its root, hidden behind the body and the back leg, as a thick rounded tail base"),
           ("chan_xa", "the FAR BACK LEG at the bottom right: the khaki leg and foot with its terracotta armour plate and its dark-brown "
            "claws at about (890-990, 860-910)", "complete its top, hidden behind the belly and the far arm, as a rounded thigh")],
    "T3": [("tay_gan", "the NEAR FRONT ARM (the left one, hanging in front of the belly): the terracotta armour plate on it (about x "
            "690-830, y 560-760) and the hand with its dark-brown claws at about (790-870, 765-810)",
            "complete the upper arm, hidden under the clay plates, as a rounded khaki shoulder"),
           ("tay_xa", "the FAR FRONT ARM (the right one): the terracotta armour plate on it (about x 955-1070, y 580-760) and the hand with "
            "its dark-brown claws at about (960-1030, 760-805)", "complete its top, hidden behind the jaw and the throat, as a rounded "
            "khaki shoulder"),
           ("p3", "the TALL clay plate at the top middle: its sharp tip at about (765, 165), terracotta inside with a cream rim, its lower "
            "part going down behind the other plates to about y 380", VIEN)],
    "T4": [("chan_gan", "the NEAR BACK LEG at the bottom left: the big khaki thigh with its terracotta armour plate (about x 540-700, "
            "y 690-860) and the foot with its dark-brown claws at about (610-700, 860-910)",
            "complete its top and its left side, hidden behind the tail and the belly, as a rounded thigh"),
           ("p2", "the BIG clay plate at the far upper left: its sharp tip at about (525, 280), reaching right to about (780, 470)", VIEN),
           ("sr", "the TALL NARROW crest plate at the far right of the crest: its sharp tip at about (1043, 145), going down to the helmet "
            "at about y 340", VIEN + "; its bottom, hidden behind the helmet, continues straight down to about y 380"),
           ("pe2", "the small clay plate lying on the side of the neck below the hood: its tip pointing left at about (673, 500), reaching "
            "right to about (815, 567)", VIEN)],
    "T5": [("p1", "the clay plate just below and left of the tall top plate: its sharp tip pointing up-left at about (700, 293), reaching "
            "right and down to about (840, 420)", VIEN),
           ("p5", "the clay plate pointing LEFT at the middle of the hood: its sharp tip at about (500, 500), reaching right to about "
            "(720, 560)", VIEN),
           ("p4", "the MIDDLE crest plate between the two tall crest plates: its sharp tip at about (1003, 210), going down behind the "
            "helmet to about y 350", VIEN + "; its bottom, hidden behind the helmet, continues down to about y 380")],
    "T6": [("sl", "the BIG CURVED crest plate (the tallest one, left of the middle crest plate): its sharp tip at about (968, 118), "
            "curving down to the helmet at about (880-960, 360)", VIEN + "; its bottom, hidden behind the helmet, continues down to about "
            "y 400"),
           ("p6", "the LOWEST clay plate of the hood on the left: its tip pointing left at about (545, 600), reaching right to about "
            "(700, 620)", VIEN),
           ("pe1", "the clay plate lying on the neck just left of the helmet: its tip pointing left at about (700, 447), reaching right "
            "under the helmet to about (830, 470)", VIEN),
           ("pc", "the SMALL clay plate between the middle crest plate and the tall right crest plate: about x 1033-1062, y 265-340", VIEN)],
    # T3 vẽ p3 thành bản sao mào cong (sl): vẽ lại riêng, tả rõ hình tam giác to bên TRÁI mào
    "T7": [("p3", "the BIG TRIANGULAR clay plate that forms the top of the hood LEFT of the crest: its sharp tip at about (765, 165) is the "
            "highest point of the hood left of the tall curved crest; its left edge runs from the tip down to about (745, 300) and its right "
            "edge from the tip down to about (890, 330); a broad triangle (about 140 px wide at y 300), terracotta inside with a wide cream "
            "rim. It is NOT the tall curved crest plate standing at x 880-975 and NOT any plate right of x 880",
            VIEN + "; its lower part, hidden behind the plates below it and the helmet, continues down as a broad base to about y 400")],
}
ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: an armoured desert lizard sitting upright on its haunches, "
        "turned to the right: a short wedge head with a heavy faceted cream sandstone brow helmet, a fierce yellow slit-pupil eye, small "
        "fangs, dusty khaki-ochre skin, a cream throat and belly, a raised hood of many overlapping terracotta clay plates with cream rims "
        "behind the head and down the back, three tall crest plates on top of the head, a terracotta armour plate on each front arm and "
        "back leg, dark-brown claws, a curled tail ringed with clay plates. Hand-drawn: wobbly dark-brown ink line, crayon hatching, flat "
        "colours.")
STYLE = ("Same wobbly dark-brown ink line (about 7 px), same colours, same crayon hatching, same completely flat colouring as image 1 (no "
         "shading, no highlights, no glow, no shadows).")


def prompt_manh():
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 3")[0].rstrip("\n")
    gd = ["", "## Lượt 3: mảnh đúng chỗ, đúng cỡ trên concept nắn (2026-11-17)", "",
          f"Ảnh mẫu duy nhất (ảnh 1) = `{Wp(NAN)}`: concept nắn về dáng rig 3530 (1536 × 1024, nền trắng). Mỗi tờ vài mảnh không chạm nhau, "
          "đúng chỗ, đúng cỡ, vẽ đủ phần bị che. Hai mắt Claude cắt thẳng từ concept nắn, mắt nhắm dựng từ mặt nạ mắt.", ""]
    for nh, ds in NHOM2.items():
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_3_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(NAN)}: {ANH1}", ""] + save + ["",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as in "
             "image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else (leave "
             "pure white there). " + STYLE + " Do not move, resize, rotate or redesign anything. Keep a clear white gap (at least 20 px) "
             "between the kept parts: where two kept parts would touch, shorten the hidden portion rather than letting them touch.",
             "", "KEEP:"]
        t += [f"{i}. {mt}: {kh}." for i, (_, mt, kh) in enumerate(ds, 1)]
        t += ["", "CANVAS: landscape 1536x1024, plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        ghi(p, t)
        gd += [f"- **{nh}** ({', '.join(x for x, _, _ in ds)}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    gd += ["", "Kiểm: từng mảnh trùng chỗ, cỡ với concept nắn (`than_lan_cat_2_manh.py ghep`); phần bị che vẽ đủ, viền kín; đầu không còn mắt; "
           "nền trắng tinh."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))



# ================================================================ cắt, mắt, ghép (như than_lan_cat_manh)
import json  # noqa: E402

import cv2  # noqa: E402


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def nen(A):
    trang = (A.min(2) > 236).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == W or y + h == H:
            bg |= lab == i
    return bg


def moi_nhat(ten):
    fs = sorted([f for f in os.listdir(G.TAI) if (f == ten + ".png" or f.startswith(ten + "_")) and f.endswith(".png")],
                key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
    return os.path.join(G.TAI, fs[-1]) if fs else None


def khu_vien(rgb, mm, r=2):
    mm = mm.astype(bool)
    toi = cv2.erode(rgb, np.ones((2 * r + 1, 2 * r + 1), np.uint8))
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(r)).astype(bool)
    ngoai = cv2.dilate(mm.astype(np.uint8), el(2)).astype(bool) & ~mm
    out = rgb.copy()
    out[vien | ngoai] = toi[vien | ngoai]
    return out


def luu_manh(A, m, ten, DATJ, nguon):
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(W, xs.max() + 4), min(H, ys.max() + 4)
    rgb = A[y0:y1, x0:x1].astype(np.uint8).copy()
    mm = m[y0:y1, x0:x1]
    rgb = khu_vien(rgb, mm)
    al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
    sang = rgb.min(2).astype(np.float32)
    al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
    os.makedirs(MANH, exist_ok=True)
    Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA").save(os.path.join(MANH, ten + ".png"))
    DATJ[ten] = dict(hop=[int(x0), int(y0), int(x1), int(y1)], nguon=nguon)
    return x0, y0, x1, y1


def nap_dat():
    pd = os.path.join(MANH, "dat.json")
    return json.load(open(pd)) if os.path.exists(pd) else {}


def ghi_dat(DATJ):
    os.makedirs(MANH, exist_ok=True)
    json.dump(DATJ, open(os.path.join(MANH, "dat.json"), "w"), indent=1)


def cat(chi=None):
    DATJ = nap_dat()
    for nh, ds in NHOM2.items():
        if chi and nh not in chi:
            continue
        src = moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        slots = [x for x, _, _ in ds]
        A = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        fg = ~nen(A)
        n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        cum = [i for i in range(1, n) if st[i, 4] > 30]
        gan = {x: [] for x in slots}
        for i in cum:
            c = cen[i]
            best = min(slots, key=lambda x: np.hypot(c[0] - TAM[x][0], c[1] - TAM[x][1]))
            d = np.hypot(c[0] - TAM[best][0], c[1] - TAM[best][1])
            if d < 260 or st[i, 4] > 20000:
                gan[best].append(i)
            else:
                print(f"  {nh}: bỏ cụm ở ({c[0]:.0f}, {c[1]:.0f}), {st[i, 4]} px")
        print(f"{nh} ({os.path.basename(src)}):")
        for x, ids in gan.items():
            if not ids:
                print(f"  {x:10s} KHÔNG THẤY MẢNH")
                continue
            b = luu_manh(A, np.isin(lab, ids), x, DATJ, os.path.basename(src))
            big = max(ids, key=lambda i: st[i, 4])
            print(f"  {x:10s} hộp {b}, {len(ids)} cụm (to nhất {st[big, 4]} px, tâm {cen[big][0]:.0f},{cen[big][1]:.0f})")
    ghi_dat(DATJ)


MAT_HOP = (870, 420, 1112, 515)


def mat():
    """hai mắt mở cắt thẳng từ concept nắn (bao lồi vùng vàng từng mắt + con ngươi + chấm sáng, nới 5 px lấy vành mực); mắt nhắm dựng từ
    cùng mặt nạ: tô màu da mặt + một nét mực cong xuống ngang giữa (mí khép)."""
    DATJ = nap_dat()
    A = np.asarray(Image.open(NAN).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    x0, y0, x1, y1 = MAT_HOP
    sub = A[y0:y1, x0:x1]
    vang = (sub[..., 0] > 205) & (sub[..., 1] > 150) & (sub[..., 2] < 110) & (sub[..., 0] - sub[..., 2] > 130)
    vang = cv2.morphologyEx(vang.astype(np.uint8), cv2.MORPH_CLOSE, el(12))
    n, lab, st, _ = cv2.connectedComponentsWithStats(vang, 8)
    ids = [i for i in range(1, n) if st[i, 4] > 120]
    m = np.zeros_like(vang)
    hulls = []
    for i in ids:
        ys, xs = np.nonzero(lab == i)
        hull = cv2.convexHull(np.stack([xs, ys], 1).astype(np.int32))
        cv2.fillPoly(m, [hull], 1)
        hulls.append(hull.reshape(-1, 2) + np.array([x0, y0]))
    m = cv2.dilate(m, el(5)).astype(bool)
    full = np.zeros((H, W), bool)
    full[y0:y1, x0:x1] = m
    print("mat", luu_manh(A, full, "mat", DATJ, "L2_tuthe.png (cắt thẳng)"), f"{len(ids)} cụm vàng")
    # mắt nhắm
    hx0, hy0, hx1, hy1 = DATJ["mat"]["hop"]
    im = np.asarray(Image.open(os.path.join(MANH, "mat.png")).convert("RGBA")).copy()
    da = np.array([185, 160, 106], np.uint8)                         # da mặt khaki của concept nắn
    al = im[..., 3] > 0
    trong = cv2.erode(al.astype(np.uint8), el(5)).astype(bool)
    im[trong, :3] = da
    can = Image.fromarray(im, "RGBA")
    d = ImageDraw.Draw(can)
    for hull in hulls:
        hx = hull[:, 0] - hx0
        hy = hull[:, 1] - hy0
        xa, xb, ym = hx.min() + 2, hx.max() - 2, (hy.min() + hy.max()) / 2
        pts = [(xa + (xb - xa) * u, ym + 0.22 * (hy.max() - hy.min()) * np.sin(np.pi * u)) for u in np.linspace(0, 1, 12)]
        d.line(pts, fill=(43, 33, 24, 255), width=6, joint="curve")
    can.save(os.path.join(MANH, "mat_nham.png"))
    DATJ["mat_nham"] = dict(hop=DATJ["mat"]["hop"], nguon="dựng từ mặt nạ mắt (tô da + mí)")
    ghi_dat(DATJ)


THU_TU = ["duoi", "chan_xa", "than", "lot", "chan_gan", "p3", "p4", "sl", "sr", "p2", "p1", "pe1", "p5", "pe2", "p6", "tay_xa", "tay_gan",
          "long_mieng", "ham", "dau", "mat"]


def ghep():
    DATJ = nap_dat()
    can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    thieu = []
    for x in THU_TU:
        if x not in DATJ:
            thieu.append(x)
            continue
        x0, y0, _, _ = DATJ[x]["hop"]
        can.alpha_composite(Image.open(os.path.join(MANH, x + ".png")).convert("RGBA"), (x0, y0))
    C = np.asarray(Image.open(NAN).convert("RGB").resize((W, H))).astype(np.int32)
    Gp = np.asarray(can.convert("RGB")).astype(np.int32)
    a, b = ~nen(C), ~nen(Gp)
    iou = (a & b).sum() / max(1, (a | b).sum())
    so = np.full((H, W, 3), 255, np.uint8)
    so[a & b] = (175, 175, 175)
    so[a & ~b] = (230, 60, 60)
    so[b & ~a] = (60, 180, 60)
    out = Image.new("RGB", (W * 3 // 2, H // 2), (255, 255, 255))
    for i, im in enumerate([Image.fromarray(C.astype(np.uint8)), can.convert("RGB"), Image.fromarray(so)]):
        out.paste(im.resize((W // 2, H // 2), Image.LANCZOS), (i * W // 2, 0))
    pp = os.path.join(MANH, "_ghep.png")
    out.save(pp)
    can.convert("RGB").save(os.path.join(MANH, "_ghep_to.png"))
    print(pp, f"IoU hình bóng {iou:.3f}", ("thiếu: " + ", ".join(thieu)) if thieu else "")



def duoi_sach():
    """GPT vẽ mảnh đuôi dính thêm một khối đùi + phiến giáp (chỗ chân sau gần): bỏ phần đuôi nằm sâu trong chân gần (mặt nạ chân gần co vào
    55 px), phần khuất còn lại tô da đuôi trơn → gốc đuôi chui sâu dưới chân (không hở khi đuôi / chân lệch nhau ở hit), khối đùi thừa không lộ."""
    DATJ = nap_dat()
    if "duoi_goc" not in DATJ:
        Image.open(os.path.join(MANH, "duoi.png")).save(os.path.join(MANH, "duoi_goc.png"))
        DATJ["duoi_goc"] = dict(DATJ["duoi"])
    d = np.asarray(Image.open(os.path.join(MANH, "duoi_goc.png")).convert("RGBA")).copy()
    x0, y0, x1, y1 = DATJ["duoi_goc"]["hop"]
    g = np.asarray(Image.open(os.path.join(MANH, "chan_gan.png")).convert("RGBA"))
    gx0, gy0, gx1, gy1 = DATJ["chan_gan"]["hop"]
    m = np.zeros((H, W), np.uint8)
    m[gy0:gy1, gx0:gx1] = (g[..., 3] > 128).astype(np.uint8)
    sau = cv2.erode(m, el(55)).astype(bool)[y0:y1, x0:x1]              # bỏ hẳn: sâu hơn 55 px trong chân gần
    khuat = m.astype(bool)[y0:y1, x0:x1] & ~sau                          # gốc đuôi khuất dưới chân (lộ khi đuôi / chân lệch nhau ở hit)
    # phần khuất: tô da đuôi trơn (bỏ phiến, vành kem của khối đùi thừa GPT vẽ), giữ nét mực
    dd = d[..., :3].astype(np.int32)
    tong = dd.sum(2)
    da_duoi = np.median(dd[(d[..., 3] > 250) & (tong > 380) & (tong < 560) & (dd[..., 0] - dd[..., 2] > 50) & ~khuat & ~sau], axis=0)
    d[sau, 3] = 0
    vien_ngoai = ~cv2.erode((d[..., 3] > 20).astype(np.uint8), el(7)).astype(bool)   # chỉ giữ nét mực viền ngoài
    k2 = khuat & (d[..., 3] > 20) & ~vien_ngoai
    lech = float(np.std(tong[(d[..., 3] > 250) & (tong > 380) & (tong < 560) & ~khuat])) / 3.0
    d[k2, :3] = van_sap(d.shape[0], d.shape[1], da_duoi, lech, seed=11)[k2]
    d[k2, 3] = 255
    n, lab, st, _ = cv2.connectedComponentsWithStats((d[..., 3] > 20).astype(np.uint8), 8)       # giữ cụm lớn nhất + phiến nhỏ sau đuôi
    giu = np.zeros(lab.shape, bool)
    for i in range(1, n):
        if st[i, 4] > 1500:
            giu |= lab == i
    d[~giu, 3] = 0
    ys, xs = np.nonzero(d[..., 3] > 0)
    d = d[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    Image.fromarray(d, "RGBA").save(os.path.join(MANH, "duoi.png"))
    DATJ["duoi"] = dict(hop=[int(x0 + xs.min()), int(y0 + ys.min()), int(x0 + xs.max() + 1), int(y0 + ys.max() + 1)],
                        nguon=DATJ["duoi_goc"]["nguon"] + " (bỏ khối đùi thừa dưới chân gần)")
    ghi_dat(DATJ)
    print("duoi", DATJ["duoi"]["hop"])



HAM_Y = 165                                                          # y cục bộ (mảnh đầu GPT) từ đó trở xuống mới tìm vùng kem hàm dưới


def tach_ham():
    """mảnh đầu GPT có hàm dưới màu kem dưới đường miệng (nanh chĩa xuống). Tách: `ham` = vùng kem đó + vành mực quanh nó (bám xương hàm,
    há được); `dau` = phần còn lại (giữ đường miệng + nanh); `long_mieng` = lòng miệng nâu đỏ cùng hình hàm, dời LÊN 0,9 bề cao của nó
    (nấp sau đầu khi ngậm, bám xương hàm: há thì lộ ra ở khe miệng)."""
    DATJ = nap_dat()
    if "dau_goc" not in DATJ:
        Image.open(os.path.join(MANH, "dau.png")).save(os.path.join(MANH, "dau_goc.png"))
        DATJ["dau_goc"] = dict(DATJ["dau"])
    im = np.asarray(Image.open(os.path.join(MANH, "dau_goc.png")).convert("RGBA")).astype(np.int32)
    x0, y0, x1, y1 = DATJ["dau_goc"]["hop"]
    r, g, b, a = im[..., 0], im[..., 1], im[..., 2], im[..., 3]
    kem = (a > 150) & (r > 225) & (g > 195) & (b > 140)
    kem[:HAM_Y] = False
    n, lab, st, _ = cv2.connectedComponentsWithStats(kem.astype(np.uint8), 8)
    k = 1 + int(np.argmax(st[1:, 4]))
    trong = cv2.morphologyEx((lab == k).astype(np.uint8), cv2.MORPH_CLOSE, el(4)).astype(bool)
    ham = cv2.dilate(trong.astype(np.uint8), el(7)).astype(bool) & (a > 20)
    ham[:HAM_Y - 12] = False
    hm = im.copy()
    hm[~ham, 3] = 0
    ys, xs = np.nonzero(hm[..., 3] > 0)
    hx0, hy0 = int(xs.min()), int(ys.min())
    Image.fromarray(hm[hy0:ys.max() + 1, hx0:xs.max() + 1].astype(np.uint8), "RGBA").save(os.path.join(MANH, "ham.png"))
    DATJ["ham"] = dict(hop=[x0 + hx0, y0 + hy0, x0 + int(xs.max()) + 1, y0 + int(ys.max()) + 1], nguon="tách từ dau (vùng kem dưới miệng)")
    up = im.copy()
    # đầu trên: theo từng cột, bỏ mọi điểm của hàm từ mép trên vùng kem trở xuống (cả vành mực dưới hàm), giữ đường miệng + nanh
    ytop = np.full(im.shape[1], 10 ** 6)
    cy, cx = np.nonzero(trong)
    np.minimum.at(ytop, cx, cy)
    yy = np.arange(im.shape[0])[:, None]
    duoi_top = (yy >= ytop[None, :]).astype(np.uint8)
    duoi_top = cv2.dilate(duoi_top, np.ones((1, 25), np.uint8))       # phủ cả hai đầu hàm (cột không có lòng kem)
    bo = (cv2.dilate(trong.astype(np.uint8), el(12)).astype(bool) & duoi_top.astype(bool)) | trong
    up[bo, 3] = 0
    mep = (up[..., 3] > 60) & cv2.dilate(bo.astype(np.uint8), el(4)).astype(bool)   # nét mực mới dọc chỗ cắt
    up[mep, :3] = (43, 33, 24)
    up[mep, 3] = 255
    Image.fromarray(up.astype(np.uint8), "RGBA").save(os.path.join(MANH, "dau.png"))
    DATJ["dau"] = dict(hop=[x0, y0, x1, y1], nguon=DATJ["dau_goc"]["nguon"] + " (bỏ hàm dưới)")
    # lòng miệng: cùng hình vùng kem, tô nâu đỏ, vành mực 4 px
    ys2, xs2 = np.nonzero(trong)
    lm = np.zeros(im.shape, np.uint8)
    vanh = cv2.dilate(trong.astype(np.uint8), el(4)).astype(bool)
    lm[vanh] = (43, 33, 24, 255)
    lm[trong] = (122, 46, 38, 255)
    lm = lm[ys2.min() - 4:ys2.max() + 5, xs2.min() - 4:xs2.max() + 5]
    Image.fromarray(lm, "RGBA").save(os.path.join(MANH, "long_mieng.png"))
    cao = int(ys2.max() - ys2.min())
    dy = int(round(0.9 * cao))
    lx0, ly0 = x0 + int(xs2.min()) - 4, y0 + int(ys2.min()) - 4 - dy
    DATJ["long_mieng"] = dict(hop=[lx0, ly0, lx0 + lm.shape[1], ly0 + lm.shape[0]], nguon=f"dựng từ vùng hàm (dời lên {dy} px)")
    # bản lề hàm: đầu trái đường miệng (điểm trái nhất của vùng kem), toạ độ concept nắn
    j = np.argmin(xs2)
    DATJ["_ban_le"] = [int(x0 + xs2[j]), int(y0 + ys2.min())]
    ghi_dat(DATJ)
    print("ham", DATJ["ham"]["hop"], "long_mieng", DATJ["long_mieng"]["hop"], "bản lề", DATJ["_ban_le"])



def van_sap(h, w, da, lech, seed=7):
    """nền màu da + nét sáp chéo ngắn sáng / tối (như vân chì sáp của mảnh GPT), ảnh h × w × 3."""
    rng = np.random.default_rng(seed)
    van = Image.new("L", (w, h), 128)
    dv = ImageDraw.Draw(van)
    for _ in range(int(26000 * h * w / (W * H)) + 50):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        L_ = rng.uniform(14, 34)
        g_ = math.radians(rng.normal(-38.0, 6.0))
        dv.line([(x, y), (x + L_ * math.cos(g_), y + L_ * math.sin(g_))], fill=int(128 + rng.choice([-1, 1]) * rng.uniform(0.6, 1.6) * lech),
                width=int(rng.integers(1, 3)))
    van = np.asarray(van.filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32) - 128.0
    return np.clip(np.asarray(da, np.float32)[None, None, :] + van[..., None], 0, 255).astype(np.uint8)


PHIEN_LOT = ["p1", "p2", "p3", "p5", "p6", "pe1", "pe2"]          # không lấy ba phiến mào: giữa các mào là nền trống như concept


def lot():
    """LỚP LƯNG sau mũ trùm (người dùng 2026-11-17: "phần vảy không gắn vào người mà bay lơ lửng"): mỗi phiến GPT là một hình kín, gốc bo
    tròn ngắn, không chạm lưng / gáy → khe nền giữa gốc phiến và thân. Dựng một mảng da khaki (màu thân) phủ vùng GỐC các phiến tới lưng,
    cổ, gáy: hợp hình các phiến co vào 24 px, chỉ giữ phần trong 170 px quanh thân + đầu, nối liền với thân và gáy; viền mực 5 px. Rig vẽ nó
    ngay sau thân, trước mọi phiến: gốc phiến cắm lên lưng như vảy giáp, khe giữa các phiến lộ da (không lộ nền), phiến bay đi ở cast thì
    lộ lưng."""
    DATJ = nap_dat()

    def mask(ten):
        m = np.zeros((H, W), np.uint8)
        x0, y0, x1, y1 = DATJ[ten]["hop"]
        a = np.asarray(Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA"))[..., 3] > 100
        m[y0:y1, x0:x1] |= a.astype(np.uint8)
        return m

    U = np.zeros((H, W), np.uint8)
    for t in PHIEN_LOT:
        U |= mask(t)
    than, dau = mask("than"), mask("dau")
    U = cv2.morphologyEx(U, cv2.MORPH_CLOSE, el(30))                    # lấp khe giữa các phiến
    loi = cv2.erode(U, el(24))
    gan = cv2.dilate(than | dau, el(170))
    B = (loi & gan).astype(np.uint8)
    B |= cv2.erode(dau, el(10)) & cv2.dilate(U, el(10))                  # chui dưới gáy (phần đầu che)
    B |= cv2.erode(than, el(10)) & cv2.dilate(U, el(40))                 # chui dưới lưng (phần thân che)
    B = cv2.morphologyEx(B, cv2.MORPH_CLOSE, el(25))
    B = cv2.morphologyEx(B, cv2.MORPH_OPEN, el(8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(B, 8)
    k = 1 + int(np.argmax(st[1:, 4]))
    B = (lab == k).astype(np.uint8)
    f = B.copy()                                                         # lấp lỗ
    cv2.floodFill(f, None, (0, 0), 2)
    B[f == 0] = 1
    # mép tròn như cái lưng gù (lộ ra khi phiến bay đi ở cast / rơi ở die): khỏi răng cưa theo hình phiến
    B = (cv2.GaussianBlur(B.astype(np.float32), (0, 0), 16) > 0.5).astype(np.uint8)
    # vân da: ô vuông khaki THUẦN lấy từ chính mảnh thân (có nét sáp), lát kín lớp lưng
    T_ = np.asarray(Image.open(os.path.join(MANH, "than.png")).convert("RGBA")).astype(np.int32)
    tr, tg, tb, ta = T_[..., 0], T_[..., 1], T_[..., 2], T_[..., 3]
    tong = tr + tg + tb
    kh = (ta > 250) & (tong > 380) & (tong < 560) & (tr - tb > 50)            # khaki (không kem bụng, không mực)
    da = np.median(T_[kh][:, :3], axis=0)
    kh &= (np.abs(T_[..., :3] - da).sum(2) < 70)
    # nền khaki + nét sáp chéo ngắn (sáng / tối ±7 %) như vân chì sáp của mảnh GPT; độ lệch màu đo trên mảnh thân
    lech = float(np.std(T_[kh][:, :3].sum(1))) / 3.0
    rgb = van_sap(H, W, da, lech)
    vien = B.astype(bool) & ~cv2.erode(B, el(5)).astype(bool)
    rgb[vien] = (43, 33, 24)
    luu_manh(np.dstack([rgb]).astype(np.int32), B.astype(bool), "lot", DATJ, "dựng: lớp lưng sau mũ trùm (da thân)")
    ghi_dat(DATJ)
    print("lot", DATJ["lot"]["hop"], "màu da", da.astype(int).tolist())


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "tuthe":
        prompt_tuthe()
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "mat":
        mat()
    elif cmd == "duoi":
        duoi_sach()
    elif cmd == "ham":
        tach_ham()
    elif cmd == "lot":
        lot()
    elif cmd == "ghep":
        ghep()
    elif cmd == "prompt":
        prompt_manh()
    elif cmd == "so_tuthe":
        so_tuthe(*(sys.argv[2:3] or []))
    else:
        print(__doc__)
