# -*- coding: utf-8 -*-
"""Thằn lằn áo choàng đất nung (than_lan_cat, tướng 2 đảo Thổ, rig monster_3257): mảnh "ĐÚNG CHỖ, ĐÚNG CỠ" gen từ concept đã duyệt
(tai_ve/L1_duyet.png = L1_D, người dùng chọn 2026-11-17: thằn lằn giáp, đầu nêm mày giáp đá, mắt vàng, áo choàng phiến đất nung dựng sau
đầu như mũ trùm, da vàng xám đất, bụng kem, đuôi khoanh phiến đất nung). Concept vẽ cùng khung với hình cả con gốc ở khung 0 idle
(mau/goc_ca_con.json) nhưng tỉ lệ khác con gốc ("gần giống"), nên mỗi mảnh đặt theo chỗ của nó trên concept rồi gắn vào xương / lưới của họ
(than_lan_cat_rig.py: gắn theo lưới, chi gộp nhiều part của họ thành một mảnh liền).

Mảnh (tên = tên ảnh; rig tra slot ở than_lan_cat_rig.SLOT):
    than        thân + cổ + bụng kem (không chân, không phiến, không đầu)        S1
    dau         đầu trên: mày giáp đá, mặt, mõm trên, răng nanh trên (KHÔNG mắt)   S2
    duoi        đuôi + ba khoanh phiến đất nung                                    S2
    chan_xa     chân sau xa (hai ngón nhỏ lộ ra dưới bụng)                         S2
    ham         hàm dưới + cằm (phần khuất trên = lòng miệng nâu đỏ)               S3
    ao3 / ao1   phiến áo choàng trên cùng / phiến thứ ba                           S3
    chan_gan    chân sau gần + ngón                                                S3
    ao2 / ao4   phiến thứ hai (mũi chĩa trái) / phiến thứ tư (trên lưng)           S4
    tay_xa      chân trước xa (bên phải) + bốn ngón                               S4
    mat_nham    hai mắt nhắm (đúng chỗ hai mắt)                                    S4
    tay_gan     chân trước gần + ba ngón                                           S5
    luoi        lưỡi chẻ (vẽ ở góc trống; rig đặt vào chỗ lưỡi của họ)             S5
    mat         hai mắt mở: cắt thẳng từ concept (mat)

    than_lan_cat_manh.py prompt       file prompt từng tờ → gui_gpt/than_lan_cat_1/luot_2_<tờ>.txt (+ nối HUONG_DAN.md)
    than_lan_cat_manh.py mat          cắt hai mắt mở thẳng từ concept → manh/mat.png
    than_lan_cat_manh.py cat [tờ]     cắt ảnh tờ (tai_ve/M_<tờ>.png) → manh/<tên>.png + manh/dat.json (hộp trên concept)
    than_lan_cat_manh.py ghep         ghép mọi mảnh theo thứ tự vẽ cạnh concept → manh/_ghep.png + IoU hình bóng
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5  # noqa: E402

G = tho5.dat("than_lan_cat")
W, H = 1536, 1024
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "than_lan_cat_1")

# tâm dự kiến (px concept) của từng mảnh, để gán cụm cắt ra cho đúng tên (đọc trên concept có lưới toạ độ)
TAM = {"than": (820, 760), "dau": (990, 390), "duoi": (370, 640), "chan_xa": (940, 885), "ham": (1020, 565), "ao3": (830, 150),
       "ao1": (610, 520), "chan_gan": (570, 815), "ao2": (560, 340), "ao4": (660, 655), "tay_xa": (1080, 790), "mat_nham": (960, 420),
       "tay_gan": (755, 820), "luoi": (1330, 170)}

NHOM = {
    "S1": [("than", "the BODY: the neck, the round sitting torso (dusty khaki-ochre) and the cream throat and belly running down its middle",
            "draw it WITHOUT the head, WITHOUT the jaw, WITHOUT any clay plate, WITHOUT the legs and WITHOUT the tail: the top of the neck, "
            "hidden behind the head, continues up as a plain rounded neck; the back, hidden under the clay plates, continues as plain khaki "
            "skin with a rounded top outline; the lower edge, hidden behind the legs, continues as a plain rounded belly resting on the "
            "ground. One complete closed shape")],
    "S2": [("dau", "the HEAD above the mouth line: the heavy rock-plated brow helmet (the big faceted light sandstone plate and the "
            "upright plate at its right end), the khaki face, the snout with its nostril and the two small UPPER fangs hanging from the "
            "mouth line",
            "draw it WITHOUT the eyes: where the two eyes are, plain khaki face skin (the helmet's lower edge stays where it is). Its lower "
            "edge is the mouth line with the two fangs (the lower jaw and the throat are NOT drawn). Its back, hidden behind the clay "
            "plates, continues as a rounded back of the head"),
           ("duoi", "the TAIL at the left: the khaki tail curling up to a pointed tip with its three terracotta clay ring plates",
            "complete its root, hidden behind the body and the clay plates, as a thick rounded tail base"),
           ("chan_xa", "the FAR BACK FOOT: the two small dark-brown toes peeking out at the bottom between the front leg and the belly "
            "(about x 880-990, y 840-920)", "complete it as a small rounded khaki foot with those two toes (its hidden top as a short "
            "rounded leg stump)")],
    "S3": [("ham", "the LOWER JAW: the khaki lower jaw and chin just below the mouth line (from the corner of the mouth to the snout tip, "
            "down to the chin line)",
            "complete its upper side, hidden behind the head, as the FLOOR OF THE MOUTH: a flat dark red-brown #7A2E26 area inside the "
            "jaw rim, so that it reads as the inside of the lower jaw when the mouth opens; no tongue, no teeth inside"),
           ("ao3", "the TOP clay plate: the big plate whose jagged top edge forms the top of the picture (from about x 480 up over x 880 "
            "to x 1110), terracotta with its cream rim",
            "complete its lower part, hidden behind the head and the second plate, as the plate continues (terracotta inside, cream rim, "
            "a smooth rounded lower edge)"),
           ("ao1", "the THIRD clay plate (from the top): the plate between y 420 and y 610 whose tip points LEFT at about (430, 520)",
            "complete its hidden parts (under the second plate, behind the head and the neck) as the plate continues"),
           ("chan_gan", "the NEAR BACK LEG: the big round khaki thigh at the lower left with its foot and three dark-brown toes",
            "complete its top, hidden under the clay plates and the tail, as a rounded thigh")],
    "S4": [("ao2", "the SECOND clay plate (from the top): the plate whose sharp tip points to the far LEFT at about (370, 390)",
            "complete its hidden parts (under the top plate, under the third plate, behind the head) as the plate continues"),
           ("ao4", "the FOURTH clay plate: the lowest plate lying on the back and the shoulder (between y 560 and y 750)",
            "complete its hidden parts as the plate continues"),
           ("tay_xa", "the FAR FRONT LEG at the right: the round khaki leg bulge on the right side with its four dark-brown toes along "
            "the right edge", "complete its top, hidden behind the throat, as a rounded shoulder"),
           ("mat_nham", "the two EYES, but now CLOSED: each eye keeps exactly the outline and size of the eye in image 1 (the big near "
            "eye and the small far eye peeking at the right edge of the head) but is filled with the khaki face colour, with ONE thick "
            "dark-brown ink line across its middle bowing slightly down (the shut lid)", "nothing else of the face, only the two shut "
            "eyes")],
    # vẽ lại phiến thứ hai cho ĐẶC (lượt S4 vẽ thành dải cong mảnh, để hở một mảng trắng giữa phiến trên và phiến thứ ba)
    "S6": [("ao2", "the SECOND clay plate as ONE BROAD plate (not a thin strip): its visible outline runs from its sharp LEFT tip at "
            "about (370, 395) up along a jagged cream rim to about (480, 225), then right along the lower edge of the top plate to about "
            "(700, 250), down behind the back of the head to about (720, 400), and back to the tip along its jagged lower rim through "
            "about (650, 420), (560, 440) and (470, 455); terracotta inside with a cream rim all round, and the small cream diamond "
            "plate near the back of the head (about x 600-720, y 345-400) is part of it",
            "complete its upper part, hidden under the top plate, and its right part, hidden behind the head, as the plate continues "
            "(terracotta inside, cream rim, a rounded outline): it must FILL the whole area between the top plate and the third plate")],
    "S5": [("tay_gan", "the NEAR FRONT LEG: the round khaki leg in the bottom middle (between the thigh and the cream belly) with its "
            "three big dark-brown toes", "complete its top, hidden under the clay plates, as a rounded shoulder"),
           ("luoi", "a long forked LIZARD TONGUE drawn ALONE in the empty upper right area of the canvas (centre about x = 1330, "
            "y = 170): about 300 px long and 45 px thick, lying diagonally from its rounded ROOT at the upper left to its FORKED TIP at "
            "the lower right, pink-red #D9605A with one lighter #F08F86 stripe along it", "it is not in image 1: draw it new, in the same "
            "style")],
}

ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: a stocky armoured desert lizard sitting low, turned to the "
        "right, a short wedge head with a heavy faceted sandstone brow helmet, a fierce yellow eye with a slit pupil (the far eye peeking "
        "at the right edge of the head), small fangs, a dusty khaki-ochre body with a cream throat and belly, a raised hood-like mantle of "
        "four overlapping terracotta clay plates with cream rims behind the head and on the back, short legs with dark-brown toes and a "
        "curled tail with three terracotta ring plates. Hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours.")
STYLE = ("Same wobbly dark-brown ink line (about 7 px), same colours, same crayon hatching, same completely flat colouring as image 1 (no "
         "shading, no highlights, no glow, no shadows).")


def Wp(p):
    return os.path.normpath(p)


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


def prompt():
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ từ concept đã chọn (2026-11-17; người dùng chọn D = `L1_duyet.png`)", "",
          f"Ảnh mẫu duy nhất (ảnh 1) = `{Wp(CONCEPT)}`: concept đã chọn (1536 × 1024, nền trắng): thằn lằn giáp mày đá, mắt vàng, áo choàng "
          "bốn phiến đất nung, da vàng xám đất, bụng kem, đuôi khoanh phiến. Mỗi tờ chỉ giữ vài mảnh không chồng nhau, đúng chỗ, đúng cỡ, vẽ "
          "đủ phần bị che. Hai mắt mở Claude cắt thẳng từ concept; lưỡi vẽ mới ở góc trống tờ S5.", ""]
    for nh, ds in NHOM.items():
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(CONCEPT)}: {ANH1}", ""] + save + ["",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as in "
             "image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else (leave "
             "pure white there). COMPLETE each kept part into ONE CLOSED SHAPE with the dark-brown ink outline running all the way around it: "
             "where a part is hidden behind another part in image 1, draw the hidden portion as it would continue, in the same style, colours "
             "and flat crayon colouring. " + STYLE + " Do not move, resize, rotate or redesign anything. Keep a clear white gap (at least "
             "20 px) between the kept parts: where two kept parts would touch, shorten the hidden portion rather than letting them touch.",
             "", "KEEP:"]
        t += [f"{i}. {mt}: {kh}." for i, (_, mt, kh) in enumerate(ds, 1)]
        t += ["", "Plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        ghi(p, t)
        gd += [f"- **{nh}** ({', '.join(s for s, _, _ in ds)}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    gd += ["", "Kiểm: từng mảnh trùng chỗ, cỡ với concept (Claude ghép lại so bằng `than_lan_cat_manh.py ghep`); phần bị che vẽ đủ, viền kín; "
           "đầu không còn mắt; hàm có lòng miệng nâu đỏ ở phần khuất; mắt nhắm đúng chỗ hai mắt; nền trắng tinh."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


# ---------------------------------------------------------------- cắt
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
    for nh, ds in NHOM.items():
        if chi and nh not in chi:
            continue
        src = moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        slots = [s for s, _, _ in ds]
        A = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        fg = ~nen(A)
        n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        cum = [i for i in range(1, n) if st[i, 4] > 30]
        gan = {s: [] for s in slots}
        for i in cum:
            c = cen[i]
            best = min(slots, key=lambda s: np.hypot(c[0] - TAM[s][0], c[1] - TAM[s][1]))
            d = np.hypot(c[0] - TAM[best][0], c[1] - TAM[best][1])
            if d < 300 or st[i, 4] > 20000:
                gan[best].append(i)
            else:
                print(f"  {nh}: bỏ cụm ở ({c[0]:.0f}, {c[1]:.0f}), {st[i, 4]} px")
        print(f"{nh} ({os.path.basename(src)}):")
        for s, ids in gan.items():
            if not ids:
                print(f"  {s:10s} KHÔNG THẤY MẢNH")
                continue
            b = luu_manh(A, np.isin(lab, ids), s, DATJ, os.path.basename(src))
            big = max(ids, key=lambda i: st[i, 4])
            print(f"  {s:10s} hộp {b}, {len(ids)} cụm (to nhất {st[big, 4]} px, tâm {cen[big][0]:.0f},{cen[big][1]:.0f})")
    ghi_dat(DATJ)


# ---------------------------------------------------------------- hai mắt mở cắt thẳng từ concept
MAT_HOP = (850, 350, 1205, 495)


def mat():
    """vùng vàng của hai mắt (mắt gần to, mắt xa lấp ló ở mép phải đầu) + con ngươi + chấm sáng, lấp kín, nới 5 px lấy vành mực."""
    DATJ = nap_dat()
    A = np.asarray(Image.open(CONCEPT).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    x0, y0, x1, y1 = MAT_HOP
    sub = A[y0:y1, x0:x1]
    vang = (sub[..., 0] > 215) & (sub[..., 1] > 140) & (sub[..., 2] < 95) & (sub[..., 0] - sub[..., 2] > 140)
    vang = cv2.morphologyEx(vang.astype(np.uint8), cv2.MORPH_CLOSE, el(14))        # nối hai bên con ngươi dọc
    n, lab, st, _ = cv2.connectedComponentsWithStats(vang, 8)
    ids = [i for i in range(1, n) if st[i, 4] > 200]
    m = np.zeros_like(vang)
    for i in ids:                                                       # bao lồi từng mắt: lấp con ngươi dọc chạm mép trên + chấm sáng
        ys, xs = np.nonzero(lab == i)
        hull = cv2.convexHull(np.stack([xs, ys], 1).astype(np.int32))
        cv2.fillPoly(m, [hull], 1)
    m = cv2.dilate(m, el(5)).astype(bool)
    full = np.zeros((H, W), bool)
    full[y0:y1, x0:x1] = m
    print("mat", luu_manh(A, full, "mat", DATJ, "L1_duyet.png (cắt thẳng)"), f"{len(ids)} cụm vàng")
    ghi_dat(DATJ)


CAM_Y = 130                                                         # đường cằm trong ảnh hàm GPT (px cục bộ của ham_goc.png)


def tach_ham():
    """GPT vẽ hàm dưới như đang há (lòng miệng nâu đỏ lộ ra dưới đường miệng) → tách: ham = phần kem (bỏ vùng đỏ, giữ nét mực ranh giới
    làm mép trên hàm); long_mieng = vùng đỏ + vành mực, dời LÊN đúng bằng bề cao của nó để nấp sau đầu khi ngậm (bám xương hàm: hàm há
    thì nó xoay theo ra khe miệng)."""
    DATJ = nap_dat()
    if "ham_goc" not in DATJ:                                       # giữ bản GPT gốc để chạy lại được
        Image.open(os.path.join(MANH, "ham.png")).save(os.path.join(MANH, "ham_goc.png"))
        DATJ["ham_goc"] = dict(DATJ["ham"])
    im = np.asarray(Image.open(os.path.join(MANH, "ham_goc.png")).convert("RGBA")).astype(np.int32)
    x0, y0, x1, y1 = DATJ["ham_goc"]["hop"]
    r, g, b, a = im[..., 0], im[..., 1], im[..., 2], im[..., 3]
    do = (a > 100) & (r > 90) & (r - g > 55) & (r - b > 55) & (g < 110)
    n, lab, st, _ = cv2.connectedComponentsWithStats(do.astype(np.uint8), 8)
    k = 1 + int(np.argmax(st[1:, 4]))
    do = lab == k
    do_vanh = cv2.dilate(do.astype(np.uint8), el(5)).astype(bool) & (a > 100)
    kem = im.copy()
    # hàm ngậm: lòng đỏ tô màu kem của hàm; nét mực ranh giới đỏ – kem (không nằm sát mép ngoài mảnh) cũng tô kem, viền ngoài giữ
    trong = (a > 100) & ~cv2.dilate((a <= 100).astype(np.uint8), el(9)).astype(bool)
    sang = (r + g + b) > 560
    mau_kem = np.median(im[sang & (a > 200) & ~do][:, :3], axis=0) if (sang & (a > 200) & ~do).any() else np.array([246, 214, 160])
    muc_giua = cv2.dilate(do.astype(np.uint8), el(8)).astype(bool) & ((r + g + b) < 300) & trong
    ys_do = np.nonzero(do)[0]
    muc_giua |= ((r + g + b) < 540) & trong & (np.arange(im.shape[0])[:, None] < ys_do.max() + 25)   # vụn mực của ranh giới cũ
    kem[do | muc_giua, :3] = mau_kem.astype(np.int32)
    # GPT vẽ hàm kèm cả cổ họng (tới y 740 trên concept): hàm há thì cả khối họng xoay theo như một tấm. Cắt ở đường cằm (nét trong
    # GPT đã vẽ ở y cục bộ ~128–132, kéo ngang sang trái tới viền ngoài), kẻ nét mực mới dọc chỗ cắt; cổ họng do mảnh thân lo.
    hh, ww = kem.shape[:2]
    xs_ = np.arange(ww)[None, :]
    y_cat = CAM_Y + 14.0 - 34.0 * (xs_ / ww) + 10.0 * np.sin(np.pi * xs_ / ww)    # cằm dốc lên về phía mõm, hơi tròn
    yy_ = np.arange(hh)[:, None]
    giu = yy_ < y_cat
    muc = giu & (yy_ >= y_cat - 5.5) & (kem[..., 3] > 100)
    kem[~giu, 3] = 0
    kem[muc, :3] = (43, 33, 24)
    Image.fromarray(kem.astype(np.uint8), "RGBA").save(os.path.join(MANH, "ham.png"))
    DATJ["ham"] = dict(hop=[x0, y0, x1, y1], nguon=DATJ["ham_goc"]["nguon"] + " (lòng đỏ tô kem: hàm ngậm)")
    ys, xs = np.nonzero(do_vanh)
    cao_do = int(ys.max() - ys.min())
    lm = np.zeros_like(im)
    lm[do_vanh] = im[do_vanh]
    lm = lm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    Image.fromarray(lm.astype(np.uint8), "RGBA").save(os.path.join(MANH, "long_mieng.png"))
    dy = int(round(0.92 * cao_do))
    DATJ["long_mieng"] = dict(hop=[int(x0 + xs.min()), int(y0 + ys.min() - dy), int(x0 + xs.max() + 1), int(y0 + ys.max() + 1 - dy)],
                              nguon="tách từ ham (dời lên %d px)" % dy)
    ghi_dat(DATJ)
    print("ham: bỏ", int(do.sum()), "px đỏ; long_mieng", DATJ["long_mieng"]["hop"])


def chan_xa_tu_gan():
    """chân sau xa: GPT chỉ vẽ bàn chân cụt (concept chỉ lộ hai ngón) → nhổm lên ở attack thì bàn chân nằm lại trên đất, rời thân. Dùng lại
    ảnh chân sau gần, tối đi 12 %, đặt vào khung bao của chân sau xa của họ (đùi + cẳng + ngón, idle 0, toạ độ concept); nấp sau thân, chỉ
    ngón lộ ra như concept."""
    DATJ = nap_dat()
    if "chan_xa_gpt" not in DATJ and "chan_xa" in DATJ:
        Image.open(os.path.join(MANH, "chan_xa.png")).save(os.path.join(MANH, "chan_xa_gpt.png"))
        DATJ["chan_xa_gpt"] = dict(DATJ["chan_xa"])
    _, imgs, atts = G.nap("att_idle0.json")
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts if a["slot"] in ("P_jiao04", "P_jiao03", "P_jiaozhi02")])
    px = np.stack([W / 2 + (P[:, 0] - cx) * s, H / 2 - (P[:, 1] - cy) * s], 1)
    bx0, by0, bx1, by1 = px[:, 0].min(), px[:, 1].min(), px[:, 0].max(), px[:, 1].max()
    g = Image.open(os.path.join(MANH, "chan_gan.png")).convert("RGBA")
    k = min((bx1 - bx0) / g.width, (by1 - by0) / g.height) * 1.05
    g = g.resize((max(2, round(g.width * k)), max(2, round(g.height * k))), Image.LANCZOS)
    A = np.asarray(g).astype(np.float32)
    A[..., :3] *= 0.88
    g = Image.fromarray(A.clip(0, 255).astype(np.uint8), "RGBA")
    g.save(os.path.join(MANH, "chan_xa.png"))
    x0 = int(round((bx0 + bx1) / 2 - g.width / 2))
    y0 = int(round(by1 - g.height))                                  # đáy bàn chân trùng đáy chân của họ
    DATJ["chan_xa"] = dict(hop=[x0, y0, x0 + g.width, y0 + g.height], nguon="chan_gan tối 12 %, khung chân sau xa của họ")
    ghi_dat(DATJ)
    print("chan_xa", DATJ["chan_xa"]["hop"], "khung họ", [round(v) for v in (bx0, by0, bx1, by1)])


THU_TU = ["tay_xa", "chan_xa", "duoi", "than", "chan_gan", "tay_gan", "ao3", "ao2", "ao1", "ao4", "long_mieng", "ham", "dau", "mat"]


def ghep():
    DATJ = nap_dat()
    can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    thieu = []
    for s in THU_TU:
        if s not in DATJ:
            thieu.append(s)
            continue
        x0, y0, _, _ = DATJ[s]["hop"]
        can.alpha_composite(Image.open(os.path.join(MANH, s + ".png")).convert("RGBA"), (x0, y0))
    C = np.asarray(Image.open(CONCEPT).convert("RGB").resize((W, H))).astype(np.int32)
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
    p = os.path.join(MANH, "_ghep.png")
    out.save(p)
    print(p, f"IoU hình bóng {iou:.3f}", ("thiếu: " + ", ".join(thieu)) if thieu else "")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "prompt":
        prompt()
    elif cmd == "mat":
        mat()
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "ghep":
        ghep()
    elif cmd == "ham":
        tach_ham()
    elif cmd == "chan_xa":
        chan_xa_tu_gan()
    else:
        print(__doc__)
