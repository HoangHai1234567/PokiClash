# -*- coding: utf-8 -*-
"""Thạch Giáp DẠNG 2 (cong_da_2, rig monster_3528): mảnh "ĐÚNG CHỖ, ĐÚNG CỠ" gen từ concept đã duyệt (inbox/cong_da_2/tai_ve/L1_duyet.png =
L1_B, người dùng duyệt 2026-11-17: tatu lớn cõng núi đá nhiều tấm, ba hốc pha lê hổ phách, chân tatu ngắn mập dưới váy đá, đuôi khoanh xoắn).
Concept to hơn con gốc ~1,2 lần nên mỗi mảnh đặt theo chỗ trên concept rồi gắn vào xương / lưới gần nhất của họ (cong_da2_rig.py).

Lớp trên concept (sau → trước): bốn chân < MAI (các tấm đá phía trên, sau thân) < THÂN + ĐẦU < mắt < VÁY (vòng tấm đá tròn buông phía dưới,
trước thân, kể cả tấm sát bên trái mặt) < ĐUÔI; pha lê nằm trên mai (gốc chìm trong hốc).

Mảnh (tên = tên slot của họ khi có; mảnh thêm có tên riêng):
    mai        núi đá phía trên (ba hốc trống, không pha lê), vẽ đủ phần khuất sau thân, đầu, váy        M1  (bám nhiều khối fangkuai_*)
    vay        vòng tấm đá phía dưới trước thân (vẽ đủ phần khuất sau đuôi)                              M2  (bám yao)
    tinh_the   cụm pha lê lớn trên đỉnh                                                                   M2  (xương pha_le)
    phach_t    cụm pha lê hốc trái                                                                        M2  (xương phach_t, bay ở cast)
    phach_p    cụm pha lê hốc phải                                                                        M2  (xương phach_p, bay ở cast)
    yezi_1     mảnh pha lê nhỏ trên đỉnh trái (thay mầm hai lá)                                           M2  (bay ở cast)
    tou        thân + đầu (tai, mày, mũi, miệng; KHÔNG mắt), vẽ đủ phần khuất sau váy                     M3
    weiba_1    đuôi khoanh (chỉ phần lộ, gốc dừng ở mép tấm váy)                                          M3
    jiao_l / shou_l / jiao_r / shou_r   chân sau gần / trước gần / sau xa / trước xa (vẽ đủ đùi khuất)     M4
    yankuang   CẢ con mắt (vành, tròng, con ngươi, chấm sáng) cắt thẳng từ concept (mat); yanjin_1 bỏ trống

    cong_da2_manh.py prompt       file prompt từng nhóm → gui_gpt/cong_da_2/luot_2_<nhóm>.txt (+ nối HUONG_DAN.md)
    cong_da2_manh.py mat          cắt mắt, con ngươi thẳng từ concept → manh/*.png
    cong_da2_manh.py cat [nhóm]   cắt ảnh nhóm (tai_ve/M_<nhóm>.png) → manh/<tên>.png + manh/dat.json (hộp trên concept)
    cong_da2_manh.py ghep         ghép mọi mảnh theo thứ tự vẽ cạnh concept → manh/_ghep.png + IoU hình bóng
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5_dang2  # noqa: E402
import cong_da_manh as M1_  # noqa: E402  (dùng lại hàm cắt: nen, khu_vien, el; G của nó trỏ dạng 1 nên không dùng luu_manh của nó)

G = tho5_dang2.dat2("cong_da")
W, H = 1536, 1024
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "cong_da_2")

TAM = {"mai": (740, 380), "vay": [(470, 760), (760, 770), (1060, 740), (730, 620)], "tinh_the": (820, 150), "phach_t": (460, 420),
       "phach_p": (1010, 390), "yezi_1": (517, 185), "tou": [(950, 630), (700, 690)], "weiba_1": (600, 815),
       "jiao_l": (470, 915), "shou_l": (725, 925), "jiao_r": (820, 900), "shou_r": (985, 915)}

NHOM = {
    "M1": [("mai", "the UPPER STONE MOUND: all the big curved grey-beige stone plates ABOVE and BEHIND the furry orange body and head (the "
            "whole top and back part of the mound, with its three geode holes: one on top, one on the left side, one on the right above "
            "the face)",
            "draw the three geode holes EMPTY: each a flat dark-brown opening with its rocky rim, the amber crystals are NOT drawn (and the "
            "small amber shard on the top left is NOT drawn: plain plate there). COMPLETE the mound downward as ONE closed shape: where the "
            "furry body, the head, the ear and the lower ring of round stone plates cover it in image 1, the same upper plates continue "
            "(plain grey-beige plates with the same plate lines) down to about the height of the snout; its lower edge is then a simple "
            "rounded line. No body, no head, no legs, no tail, no lower round plates")],
    "M2": [("vay", "the LOWER STONE SKIRT: the ring of big ROUND stone plates that hang IN FRONT of the furry body around the bottom of the "
            "creature, from the far left round under the body to the right under the face, INCLUDING the big rounded plate just to the left "
            "of the face that covers the body",
            "draw them exactly as in image 1 (their top edges where they cover the body and the chin stay exactly as in image 1); where the "
            "curled ringed tail covers them, complete the plates (plain plates there, the tail is NOT drawn). Between the plates, where the "
            "orange body or the legs showed, leave pure white. No body, no head, no legs, no tail, no upper plates"),
           ("tinh_the", "the big cluster of AMBER CRYSTALS standing in the geode hole on TOP of the mound",
            "complete their bottoms: the crystals stand on a short common amber base that would sit inside the hole (draw that base as the "
            "crystals continue); no rock rim"),
           ("phach_t", "the cluster of AMBER CRYSTALS in the geode hole on the LEFT side of the mound",
            "complete their bottoms into a short common amber base; no rock rim"),
           ("phach_p", "the cluster of AMBER CRYSTALS in the geode hole on the RIGHT side of the mound (above the face)",
            "complete their bottoms into a short common amber base; no rock rim"),
           ("yezi_1", "the single small AMBER SHARD standing on the top LEFT of the mound", "complete its bottom as a short pointed base")],
    "M3": [("tou", "the FURRY BODY AND HEAD: the armadillo head with its round ear, the angry brow stroke, the short pointed snout with the "
            "round dark-brown nose, the frowning mouth line and the cream face patch, and the orange furry body band that runs from the head "
            "down to the left under the mound",
            "draw it WITHOUT the EYE (no eye white, no pupil, no eye outline: plain orange fur there; the brow stroke stays). Where the lower "
            "round stone plates cover the body and the chin in image 1, COMPLETE it as a plain rounded furry body with a cream belly (a "
            "complete chubby armadillo body under the skirt); its top edge against the upper stone plates stays exactly as in image 1. No "
            "stone plates, no legs, no tail"),
           ("weiba_1", "the curled ringed TAIL at the lower left", "ONLY the part visible in image 1: its root ends exactly where it goes "
            "behind the round stone plate on its left, closed there by a short ink line")],
    "M4": [("jiao_l", "the BACK LEFT LEG (far left, lower left) with its foot and cream claws",
            "complete its top, hidden under the stone skirt, as a rounded thigh going up about as high again as the visible part"),
           ("shou_l", "the FRONT LEFT LEG (bottom middle-left, the lowest foot) with its foot and cream claws",
            "complete its top, hidden under the stone skirt, as a rounded thigh going up about as high again as the visible part"),
           ("jiao_r", "the FAR BACK LEG (bottom middle, just right of it, a little higher) with its foot and cream claws",
            "complete its top, hidden under the stone skirt, as a rounded thigh going up about as high again as the visible part"),
           ("shou_r", "the FAR FRONT LEG (lower right, under the face) with its foot and cream claws",
            "complete its top, hidden under the stone skirt, as a rounded thigh going up about as high again as the visible part")],
}

ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: a big armadillo carrying a huge mound of grey-beige stone "
        "plates with three amber crystal clusters in geode holes (top, left, right) and a small amber shard on the top left; its sandy-orange "
        "head with a round ear, an angry eye and a pointed snout peeks out at the lower right under the mound; a ring of big round stone "
        "plates hangs low round the bottom like a skirt; four short stubby orange legs with cream claws below; a curled ringed tail at the "
        "lower left. Hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours.")
STYLE = M1_.STYLE

el = M1_.el
nen = M1_.nen
khu_vien = M1_.khu_vien


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


def prompt():
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 3")[0].rstrip("\n")
    gd = ["", "## Lượt 3: mảnh đúng chỗ, đúng cỡ từ concept đã duyệt (2026-11-17; `L1_duyet.png` = L1_B)", "",
          f"Ảnh mẫu duy nhất (ảnh 1) = `{Wp(CONCEPT)}`: concept đã duyệt (1536 × 1024, nền trắng): tatu lớn cõng núi đá nhiều tấm, ba cụm pha "
          "lê hổ phách, mảnh pha lê nhỏ trên đỉnh trái, đầu ló dưới mai bên phải, váy tấm đá tròn, bốn chân ngắn, đuôi khoanh. Mỗi nhóm chỉ giữ "
          "vài mảnh không chồng nhau, đúng chỗ, đúng cỡ, vẽ đủ phần bị che. Mắt Claude cắt thẳng từ concept.", ""]
    for nh, ds in NHOM.items():
        if nh in ("M5", "M6"):                             # gen lại riêng: luot_4_duoi.txt, luot_5_than.txt
            continue
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_3_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(CONCEPT)}: {ANH1}", ""] + save + ["",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as in "
             "image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else (leave "
             "pure white there). COMPLETE each kept part into ONE CLOSED SHAPE with the dark-brown ink outline running all the way around it "
             "(unless told to keep only the visible part): where a part is hidden behind another part in image 1, draw the hidden portion as "
             "it would continue, in the same style, colours and flat crayon colouring. " + STYLE + " Do not move, resize, rotate or redesign "
             "anything. Keep a clear white gap between the kept parts.", "", "KEEP:"]
        t += [f"{i}. {mt}: {kh}." for i, (_, mt, kh) in enumerate(ds, 1)]
        t += ["", "CANVAS: landscape 1536x1024 (the same frame as image 1), plain pure-white background (#FFFFFF), no labels, no shadows, "
              "no sparkles."]
        ghi(p, t)
        gd += [f"- **{nh}** ({', '.join(s for s, _, _ in ds)}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    gd += ["", "Kiểm: từng mảnh trùng chỗ, cỡ với concept (Claude ghép lại so bằng `cong_da2_manh.py ghep`); phần bị che vẽ đủ, viền kín; mai có "
           "ba hốc trống; thân không có mắt; nền trắng tinh."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


# ---------------------------------------------------------------- cắt
def moi_nhat(ten):
    fs = sorted([f for f in os.listdir(G.TAI) if (f == ten + ".png" or f.startswith(ten + "_")) and f.endswith(".png")],
                key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
    return os.path.join(G.TAI, fs[-1]) if fs else None


def luu_manh(A, m, ten, DATJ, nguon, sua=None):
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(W, xs.max() + 4), min(H, ys.max() + 4)
    rgb = A[y0:y1, x0:x1].astype(np.uint8).copy()
    mm = m[y0:y1, x0:x1]
    if sua is not None:
        rgb = sua(rgb, mm, x0, y0)
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

            def kc(s):
                ts = TAM[s] if isinstance(TAM[s], list) else [TAM[s]]
                return min(np.hypot(c[0] - x, c[1] - y) for x, y in ts)
            best = min(slots, key=kc)
            if kc(best) < 300 or st[i, 4] > 20000:
                gan[best].append(i)
            else:
                print(f"  {nh}: bỏ cụm ở ({c[0]:.0f}, {c[1]:.0f}), {st[i, 4]} px")
        print(f"{nh} ({os.path.basename(src)}):")
        masks = {s: np.isin(lab, ids) for s, ids in gan.items() if ids}
        for truoc, sau in TACH.get(nh, []):                     # hai mảnh GPT vẽ dính nhau: tách theo mảng màu bên trong
            chung = masks.get(truoc, np.zeros((H, W), bool)) | masks.get(sau, np.zeros((H, W), bool))
            if chung.any():
                masks[truoc], masks[sau] = tach(A, chung, truoc, sau)
        for s in slots:
            ids = gan[s] if s not in masks else [1]
            if not masks.get(s, np.zeros(1, bool)).any():
                print(f"  {s:10s} KHÔNG THẤY MẢNH")
                continue
            b = luu_manh(A, masks[s], s, DATJ, os.path.basename(src))
            print(f"  {s:10s} hộp {b}, {int(masks[s].sum())} px")
    ghi_dat(DATJ)


NHOM["M5"] = [("weiba_1", "the whole curled ringed TAIL with its root completed (luot_4_duoi.txt)", "")]   # gen lại 2026-11-17
NHOM["M6"] = [("tou", "the whole tail-less armadillo BODY + head (luot_5_than.txt)", "")]                # gen lại 2026-11-17: thân trước váy

# mảnh GPT vẽ dính nhau trong một ảnh nhóm: (mảnh nằm TRƯỚC, mảnh nằm sau)
TACH = {"M3": [("weiba_1", "tou")], "M4": [("shou_l", "jiao_r")]}


def tach(A, chung, truoc, sau):
    """tách vùng dính: mảng màu (không phải nét mực) gán theo tâm TAM gần nhất; mỗi mảnh = các mảng của nó nở 7 px (lấy lại viền mực) ∩
    vùng dính; chỗ hai mảnh chồng thì thuộc mảnh nằm trước; điểm mực còn lại theo mảnh gần nhất."""
    muc = A.mean(2) < 110
    mau = chung & ~muc
    n, lab, st, cen = cv2.connectedComponentsWithStats(mau.astype(np.uint8), 4)

    def kc(c, s):
        ts = TAM[s] if isinstance(TAM[s], list) else [TAM[s]]
        return min(np.hypot(c[0] - x, c[1] - y) for x, y in ts)
    mt, ms = np.zeros_like(chung), np.zeros_like(chung)
    for i in range(1, n):
        if st[i, 4] < 4:
            continue
        (mt if kc(cen[i], truoc) <= kc(cen[i], sau) else ms)[lab == i] = True
    mt = cv2.dilate(mt.astype(np.uint8), el(7)).astype(bool) & chung
    ms = cv2.dilate(ms.astype(np.uint8), el(7)).astype(bool) & chung & ~mt
    con = chung & ~mt & ~ms
    if con.any():
        dt = cv2.distanceTransform((~mt).astype(np.uint8), cv2.DIST_L2, 3)
        ds = cv2.distanceTransform((~ms).astype(np.uint8), cv2.DIST_L2, 3)
        mt |= con & (dt <= ds)
        ms |= con & (dt > ds)
    return _cum_lon(mt), _cum_lon(ms)


def _cum_lon(m, ti=0.15):
    """bỏ vụn (nét mực của mảnh kia dính sang): giữ các cụm ≥ ti × cụm to nhất."""
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n <= 2:
        return m
    lon = st[1:, 4].max()
    return np.isin(lab, [i for i in range(1, n) if st[i, 4] >= ti * lon])


# ---------------------------------------------------------------- mắt cắt thẳng từ concept
MAT_HOP = (880, 588, 965, 662)                     # hộp quanh tròng (px concept), mày nằm trên, không lấy


def mat():
    """CẢ con mắt (vành mực + tròng trắng + con ngươi + chấm sáng) cắt thẳng từ concept → yankuang (chớp mắt = bóp dọc cả mắt; tou vẽ không
    mắt nên chỗ bóp lộ lông). Con ngươi chạm vành nên không tách riêng; yanjin_1 bỏ trống."""
    DATJ = nap_dat()
    A = np.asarray(Image.open(CONCEPT).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    x0, y0, x1, y1 = MAT_HOP
    sub = A[y0:y1, x0:x1]
    trang = sub.min(2) > 215
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang.astype(np.uint8), 8)
    k = 1 + int(np.argmax(st[1:, 4]))
    tr = (lab == k).astype(np.uint8)
    cs, _ = cv2.findContours(tr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    hull = cv2.drawContours(np.zeros_like(tr), [cv2.convexHull(np.concatenate(cs))], -1, 1, -1)
    gan = cv2.dilate(hull, el(9)).astype(bool)
    toi = (sub.mean(2) < 120) & gan                                   # vành mực + con ngươi quanh tròng
    m = (tr.astype(bool) | toi).astype(np.uint8)
    n2, lab2, st2, _ = cv2.connectedComponentsWithStats(m, 8)
    k2 = lab2[tuple(np.argwhere(tr)[len(np.argwhere(tr)) // 2])]
    m = (lab2 == k2).astype(np.uint8)
    cs3, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    m = cv2.drawContours(np.zeros_like(m), cs3, -1, 1, -1)            # lấp chấm sáng, khe trong
    full = np.zeros((H, W), bool)
    full[y0:y1, x0:x1] = cv2.dilate(m, el(1)).astype(bool)
    print("yankuang", luu_manh(A, full, "yankuang", DATJ, "L1_duyet.png (cắt thẳng, cả mắt)"))
    DATJ.pop("yanjin_1", None)
    p = os.path.join(MANH, "yanjin_1.png")
    if os.path.exists(p):
        os.remove(p)
    ghi_dat(DATJ)


# ---------------------------------------------------------------- sửa lớp (người dùng 2026-11-17: "lỗi layer và đuôi cũng lỗi")
# mép phải tấm váy trái chỗ gốc đuôi chui vào (px concept, đọc trên lưới phóng to): bên trái đường này đuôi khuất sau tấm
# viền dưới của đuôi trên concept từ chỗ gặp mép tấm trái (gốc lòi dưới đường này bị xoá, đường này thành viền đuôi)
VIEN_DUOI_DUOI = [(514, 848), (517, 860), (527, 878), (545, 889), (600, 894), (632, 886)]
MEP_TAM_TRAI = [(515, 690), (513, 740), (512, 800), (514, 848), (500, 860), (470, 872), (430, 884), (380, 895)]
def sua_lop():
    """Lớp theo ý người dùng (2026-11-17, lần 2: "phần đá vẫn bị nằm trên vỏ"): THÂN + ĐẦU tatu nằm TRƯỚC váy đá dưới (váy chỉ lộ quanh
    viền dưới, hai bên, sau thân), mai đá trên vẫn trùm phía trên lưng, thân là một khối liền tròn (lưng, bụng kem, hông), đuôi mọc từ
    mông, gốc chui dưới mép tấm váy trái. Lớp: chân < mai < váy < thân < mai_truoc < mắt < đuôi < vay_truoc < pha lê.
    - vay: bản gốc (không khoét).
    - tou: thân tròn đủ GPT vẽ (M3, bản gốc, KHÔNG vá concept: miếng vá cũ thành mẩu cam nhọn), lấp khuyết ở mông (chỗ đuôi M3 tách ra).
    - mai_truoc: LƯỚI CON trên chính ảnh mai (rig dựng): phủ dải lưng trên mà concept để mai trùm (điểm concept không ấm, không phải váy,
      nằm trong thân) → mép trên thân là mép dưới mai như concept; đầu, tai vẫn trước mai.
    - weiba_1: đuôi liền M5 (dời khớp concept), gốc lòi xuống dưới đáy tấm trái xoá theo viền dưới đuôi concept (mực concept làm viền).
    - vay_truoc: LƯỚI CON trên ảnh váy, che gốc đuôi bên trái mép tấm trái, TRỪ chỗ thân (không đè thân).
    Lần đầu chép bản gốc thành <tên>_goc.png; chạy lại luôn tính từ bản gốc."""
    DATJ = nap_dat()
    C8 = np.asarray(Image.open(CONCEPT).convert("RGB").resize((W, H), Image.LANCZOS))
    C = C8.astype(np.int32)
    for ten in ("vay", "tou"):
        g = os.path.join(MANH, ten + "_goc.png")
        if not os.path.exists(g):
            Image.open(os.path.join(MANH, ten + ".png")).save(g)
            DATJ[ten + "_goc"] = DATJ[ten]
    # --- váy: bản gốc
    Vg = np.asarray(Image.open(os.path.join(MANH, "vay_goc.png")).convert("RGBA")).copy()
    x0, y0 = DATJ["vay_goc"]["hop"][:2]
    Image.fromarray(Vg, "RGBA").save(os.path.join(MANH, "vay.png"))
    DATJ["vay"] = dict(DATJ["vay_goc"])
    vm = np.zeros((H, W), bool)
    vm[y0:y0 + Vg.shape[0], x0:x0 + Vg.shape[1]] = Vg[..., 3] > 128
    # --- thân: bản gốc + lấp khuyết ở mông (đóng hình 25 px chỉ ở góc dưới trái, màu lấp bằng inpaint từ điểm quanh)
    To = np.asarray(Image.open(os.path.join(MANH, "tou_goc.png")).convert("RGBA")).copy()
    ox, oy = DATJ["tou_goc"]["hop"][:2]
    pad = 20
    T2 = np.zeros((To.shape[0] + 2 * pad, To.shape[1] + 2 * pad, 4), np.uint8)
    T2[pad:-pad, pad:-pad] = To
    m = T2[..., 3] > 128
    dong = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, el(25)).astype(bool)
    goc = np.zeros_like(m)
    gx, gy = 640 - ox + pad, 760 - oy + pad                         # chỉ góc dưới trái của thân (x concept < 640, y > 760)
    goc[gy:, :gx] = True
    khuyet = dong & ~m & goc
    if khuyet.sum() >= 300:                                         # M6 (thân liền) không còn khuyết; lõm nhỏ ở mép là dáng thân, để nguyên
        bgr = np.ascontiguousarray(T2[..., :3][..., ::-1])
        fill = cv2.inpaint(bgr, khuyet.astype(np.uint8) * 255, 7, cv2.INPAINT_TELEA)[..., ::-1]
        T2[khuyet, :3] = fill[khuyet]
        T2[khuyet, 3] = 255
    ys, xs = np.nonzero(T2[..., 3] > 0)
    bx = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    Tn = T2[bx[1]:bx[3], bx[0]:bx[2]]
    Image.fromarray(Tn, "RGBA").save(os.path.join(MANH, "tou.png"))
    hx, hy = ox - pad + bx[0], oy - pad + bx[1]
    DATJ["tou"] = dict(hop=[int(hx), int(hy), int(hx + Tn.shape[1]), int(hy + Tn.shape[0])], nguon=DATJ["tou_goc"]["nguon"] + " (lấp khuyết mông)")
    tm_than = np.zeros((H, W), bool)
    tm_than[hy:hy + Tn.shape[0], hx:hx + Tn.shape[1]] = Tn[..., 3] > 128
    print(f"tou: lấp khuyết {int(khuyet.sum())} px, hộp {DATJ['tou']['hop']}")
    # --- mai_truoc: dải lưng trên mà concept để mai trùm
    am_c = ((C[..., 0] - C[..., 2]) > 75) & (C.mean(2) > 95)
    nen_c = C.min(2) > 236
    da_c = (C.mean(2) < 210) & (C.mean(2) > 95) & ((C[..., 0] - C[..., 2]) < 58) & ((C.max(2) - C.min(2)) < 62)   # màu đá xám
    muc_c = (C.mean(2) <= 95) & cv2.dilate(da_c.astype(np.uint8), el(4)).astype(bool)                              # mực sát đá
    mai_c = (da_c | muc_c) & ~nen_c & ~cv2.dilate(vm.astype(np.uint8), el(3)).astype(bool)
    # chỉ dải lưng trên: trong 80 px dưới mép trên của thân, bỏ vùng đầu (x concept > 830: đầu, tai trước mai)
    cot = np.where(tm_than.any(0), tm_than.argmax(0), H)
    yy = np.arange(H)[:, None]
    dai = (yy < cot[None, :] + 80) & (np.arange(W)[None, :] < 830)
    vung = tm_than & mai_c & dai
    # 2026-11-17: mép lưng của thân GPT (M3) đã trùng mép dưới mai trên concept: phần chồng chỉ ~550 px vụn, vẽ ra thành khấc trên mép
    # lưng → bỏ (mai nằm sau lưng, mép lưng giữ nét mực liền của thân). Giữ mã để dùng lại nếu mảnh thân đổi.
    vung[:] = False
    vung = cv2.morphologyEx(vung.astype(np.uint8), cv2.MORPH_OPEN, el(2)).astype(bool)
    n, lab, st, _ = cv2.connectedComponentsWithStats(vung.astype(np.uint8), 8)
    vung = np.isin(lab, [k for k in range(1, n) if st[k, 4] >= 200])
    vung = cv2.dilate(vung.astype(np.uint8), el(3)).astype(bool)
    Mg = Image.open(os.path.join(MANH, "mai.png"))
    mx, my = DATJ["mai"]["hop"][:2]
    mk = vung[my:my + Mg.height, mx:mx + Mg.width] & (np.asarray(Mg.convert("RGBA"))[..., 3] > 0)
    Image.fromarray((mk * 255).astype(np.uint8), "L").save(os.path.join(MANH, "mai_truoc_mask.png"))
    print(f"mai_truoc: {int(mk.sum())} px")
    # --- đuôi (M5 đã cắt bằng `cat M5`): dời khớp đuôi lộ concept, xoá gốc lòi dưới đáy tấm trái
    if "weiba_1_m5" not in DATJ or not os.path.exists(os.path.join(MANH, "weiba_1_m5.png")):
        Image.open(os.path.join(MANH, "weiba_1.png")).save(os.path.join(MANH, "weiba_1_m5.png"))
        DATJ["weiba_1_m5"] = dict(DATJ["weiba_1"])
    T = Image.open(os.path.join(MANH, "weiba_1_m5.png")).convert("RGBA")
    tx, ty = DATJ["weiba_1_m5"]["hop"][:2]
    ta = np.asarray(T)[..., 3] > 40
    hop_d = np.zeros((H, W), bool)
    hop_d[max(ty - 30, 740):ty + T.height + 30, max(0, tx - 30):tx + T.width + 30] = True
    lo = cv2.morphologyEx((am_c & hop_d).astype(np.uint8), cv2.MORPH_CLOSE, el(5)).astype(bool)
    n3, lab3, st3, _ = cv2.connectedComponentsWithStats(lo.astype(np.uint8), 8)
    lo = lab3 == (1 + int(np.argmax(st3[1:, 4])))
    best = (-1.0, 0, 0)
    for dy in range(-24, 25, 2):
        for dx in range(-24, 25, 2):
            tmm = np.zeros((H, W), bool)
            tmm[ty + dy:ty + dy + T.height, tx + dx:tx + dx + T.width] = ta
            ov = (tmm & lo).sum() / max(1, lo.sum())
            if ov > best[0] + 1e-6:
                best = (ov, dx, dy)
    _, dx, dy = best
    tx, ty = tx + dx, ty + dy
    DATJ["weiba_1"] = dict(DATJ["weiba_1_m5"], hop=[tx, ty, tx + T.width, ty + T.height])
    tm = np.zeros((H, W), bool)
    tm[ty:ty + T.height, tx:tx + T.width] = ta
    print(f"weiba_1: dời ({dx}, {dy}) px cho khớp concept")
    tam_trai = np.zeros((H, W), np.uint8)
    cv2.fillPoly(tam_trai, [np.array(MEP_TAM_TRAI + [(380, 690)], np.int32)], 1)
    tam_trai = tam_trai.astype(bool)
    khuat = tm & tam_trai
    trai = np.zeros((H, W), np.uint8)
    cv2.fillPoly(trai, [np.array([(515, 690), (513, 740), (512, 800)] + VIEN_DUOI_DUOI + [(700, 960), (300, 960), (300, 690)], np.int32)], 1)
    xoa = tm & trai.astype(bool) & ~tam_trai
    Ta = np.asarray(T).copy()
    if xoa.any():
        Ta[xoa[ty:ty + T.height, tx:tx + T.width], 3] = 0
        vien = np.zeros((H, W), np.uint8)
        cv2.polylines(vien, [np.array(VIEN_DUOI_DUOI, np.int32)], False, 1, 15)
        muc = vien.astype(bool) & (C.mean(2) < 120) & cv2.dilate(tm.astype(np.uint8), el(4)).astype(bool)
        sub_m = muc[ty:ty + T.height, tx:tx + T.width]
        Ta[sub_m, :3] = C8[ty:ty + T.height, tx:tx + T.width][sub_m]
        Ta[sub_m, 3] = 255
        tm = (tm & ~xoa) | muc
    Image.fromarray(Ta, "RGBA").save(os.path.join(MANH, "weiba_1.png"))
    print(f"weiba_1: xoá {int(xoa.sum())} px gốc lòi dưới đáy tấm trái")
    # --- vay_truoc: che gốc đuôi bên trái mép tấm trái, trừ chỗ thân
    kv = cv2.dilate(khuat.astype(np.uint8), el(8)).astype(bool) & cv2.dilate(tam_trai.astype(np.uint8), el(4)).astype(bool) & ~tm_than
    kv = kv[y0:y0 + Vg.shape[0], x0:x0 + Vg.shape[1]] & (Vg[..., 3] > 0)
    Image.fromarray((kv * 255).astype(np.uint8), "L").save(os.path.join(MANH, "vay_truoc_mask.png"))
    F = Vg.copy()
    F[~kv, 3] = 0
    ys, xs = np.nonzero(F[..., 3] > 0)
    if len(xs):
        fb = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
        Image.fromarray(F[fb[1]:fb[3], fb[0]:fb[2]], "RGBA").save(os.path.join(MANH, "vay_truoc.png"))
        DATJ["vay_truoc"] = dict(hop=[int(x0 + fb[0]), int(y0 + fb[1]), int(x0 + fb[2]), int(y0 + fb[3])], nguon="vay (lưới con che gốc đuôi)")
    print(f"vay_truoc: {int(kv.sum())} px")
    ghi_dat(DATJ)
    lap_lo(["weiba_1", "tou"])
    hoc_pha_le()


# ---------------------------------------------------------------- hốc pha lê hai lớp (người dùng 2026-11-17: "mấy cục đá vàng kia phải ở
# giữa lõm, bạn phải tách thành 2 layer"; memory lo-hai-lop): nửa vành SAU + lòng hốc sẫm (trong mai, vẽ sau pha lê) → pha lê → nửa vành
# TRƯỚC (lưới con trên chính ảnh mai, vẽ trước gốc pha lê). Hướng mọc của từng cụm (x, y concept; y xuống):
HUONG_HOC = {"tinh_the": (0.0, -1.0), "phach_t": (-0.35, -1.0), "phach_p": (0.35, -1.0)}
VANH = {"tinh_the": "vanh_d", "phach_t": "vanh_t", "phach_p": "vanh_p"}


def hoc_pha_le():
    """mỗi cụm pha lê mọc từ một hốc trên mai (lỗ hai lớp): lòng hốc = khối sẫm (mean < 95) trên ảnh mai gần gốc cụm nhất, làm trơn (đóng /
    mở 6 px). Gốc cụm (trọng tâm 20 % điểm thấp nhất theo hướng mọc) đặt dưới tâm hốc 0,3 bán kính; cụm rộng hơn 92 % miệng hốc ở ngang
    tâm hốc thì thu nhỏ quanh gốc (gốc vật hẹp vừa miệng lỗ). Bỏ điểm pha lê phía GỐC của đường cắt (qua tâm, vuông góc hướng mọc) mà nằm
    ngoài lòng hốc. Nửa vành trước = vành (nở 26 px) từ mép trong lòng hốc lấn vào 7 px (phủ nét mực mép trong), phía gốc của đường cắt,
    chờm qua 5 px → manh/<vanh>_mask.png (toạ độ ảnh mai; rig dựng thành lưới con trên chính ảnh mai, vẽ ngay sau cụm)."""
    DATJ = nap_dat()
    Mi = np.asarray(Image.open(os.path.join(MANH, "mai.png")).convert("RGBA"))
    mx, my = DATJ["mai"]["hop"][:2]
    mh, mw = Mi.shape[:2]
    sam = (Mi[..., :3].astype(np.int32).mean(2) < 95) & (Mi[..., 3] > 128)
    khoi = cv2.morphologyEx(sam.astype(np.uint8), cv2.MORPH_OPEN, el(4))
    n, lab, st, cen = cv2.connectedComponentsWithStats(khoi, 8)
    yy, xx = np.mgrid[0:mh, 0:mw]
    for ten, vanh in VANH.items():
        g = os.path.join(MANH, ten + "_goc.png")
        if not os.path.exists(g) or ten + "_goc" not in DATJ:
            Image.open(os.path.join(MANH, ten + ".png")).save(g)
            DATJ[ten + "_goc"] = dict(DATJ[ten])
        P0 = Image.open(g).convert("RGBA")
        px, py = DATJ[ten + "_goc"]["hop"][:2]
        d = np.array(HUONG_HOC[ten], float)
        d /= np.hypot(*d)
        a0 = np.asarray(P0)[..., 3] > 128
        ys, xs = np.nonzero(a0)
        proj = xs * d[0] + ys * d[1]
        thap = proj <= np.percentile(proj, 20)
        goc_l = np.array([xs[thap].mean(), ys[thap].mean()])                    # gốc cụm trong ảnh cụm
        goc = goc_l + (px, py)
        best = None
        for k in range(1, n):
            if st[k, 4] < 400:
                continue
            c = np.array([cen[k][0] + mx, cen[k][1] + my])
            dd = np.hypot(*(c - goc))
            if best is None or dd < best[0]:
                best = (dd, k, c)
        _, k, c = best
        hoc = cv2.morphologyEx(cv2.morphologyEx((lab == k).astype(np.uint8), cv2.MORPH_CLOSE, el(6)), cv2.MORPH_OPEN, el(6)).astype(bool)
        r = math.sqrt(hoc.sum() / math.pi)
        dich_goc = c - 0.30 * r * d                                            # chỗ đặt gốc cụm (toạ độ concept)
        # bề ngang cụm / miệng hốc ở ngang tâm hốc (hàng vuông góc hướng mọc qua tâm, ±3 px)
        cm = (c[0] - mx, c[1] - my)
        hang_h = np.abs((xx - cm[0]) * d[0] + (yy - cm[1]) * d[1]) <= 3
        ngang = np.array([-d[1], d[0]])
        def be_ngang(mask, X, Y, o):
            v = ((X - o[0]) * ngang[0] + (Y - o[1]) * ngang[1])[mask]
            return float(v.max() - v.min()) if v.size else 0.0
        hw = be_ngang(hoc & hang_h, xx, yy, cm)
        Yp, Xp = np.mgrid[0:a0.shape[0], 0:a0.shape[1]]
        Xc, Yc = Xp - goc_l[0] + dich_goc[0], Yp - goc_l[1] + dich_goc[1]       # điểm ảnh cụm sau khi dời (toạ độ concept)
        hang_p = np.abs((Xc - c[0]) * d[0] + (Yc - c[1]) * d[1]) <= 3
        pw = be_ngang(a0 & hang_p, Xc, Yc, c)
        f = 1.0 if pw <= 0.92 * hw or pw == 0 else max(0.7, 0.92 * hw / pw)
        P = P0 if f == 1.0 else P0.resize((max(2, round(P0.width * f)), max(2, round(P0.height * f))), Image.LANCZOS)
        P = np.asarray(P).copy()
        goc_l2 = goc_l * f
        nx, ny = int(round(dich_goc[0] - goc_l2[0])), int(round(dich_goc[1] - goc_l2[1]))
        # bỏ điểm pha lê phía gốc của đường cắt mà nằm ngoài lòng hốc
        hoc_c = np.zeros((H, W), bool)
        hoc_c[my:my + mh, mx:mx + mw] = hoc
        Yc2, Xc2 = np.mgrid[ny:ny + P.shape[0], nx:nx + P.shape[1]]
        phia_goc = ((Xc2 - c[0]) * d[0] + (Yc2 - c[1]) * d[1]) < 0
        trong = np.zeros(P.shape[:2], bool)
        y0c, x0c = max(0, ny), max(0, nx)
        y1c, x1c = min(H, ny + P.shape[0]), min(W, nx + P.shape[1])
        trong[y0c - ny:y1c - ny, x0c - nx:x1c - nx] = hoc_c[y0c:y1c, x0c:x1c]
        bo = phia_goc & ~trong & (P[..., 3] > 0)
        P[bo, 3] = 0
        Image.fromarray(P, "RGBA").save(os.path.join(MANH, ten + ".png"))
        DATJ[ten] = dict(DATJ[ten + "_goc"], hop=[nx, ny, nx + P.shape[1], ny + P.shape[0]])
        # nửa vành trước
        vanh_m = (cv2.dilate(hoc.astype(np.uint8), el(26)).astype(bool) & ~cv2.erode(hoc.astype(np.uint8), el(7)).astype(bool)
                  & (Mi[..., 3] > 0))
        truoc = ((xx - cm[0]) * d[0] + (yy - cm[1]) * d[1]) < 5
        vm_ = vanh_m & truoc
        Image.fromarray((vm_ * 255).astype(np.uint8), "L").save(os.path.join(MANH, vanh + "_mask.png"))
        print(f"{ten}: hốc tâm ({c[0]:.0f}, {c[1]:.0f}) r {r:.0f}, miệng {hw:.0f} px, cụm {pw:.0f} px → thu {f:.2f}; gốc tại "
              f"({dich_goc[0]:.0f}, {dich_goc[1]:.0f}); bỏ {int(bo.sum())} px; {vanh}: {int(vm_.sum())} px")
    ghi_dat(DATJ)


# ---------------------------------------------------------------- lấp lỗ (Claude chính 2026-11-17: chấm trắng giữa vòng xoắn đuôi)
KHONG_LAP = ("yankuang",)                 # tròng trắng + chấm sáng trong mắt là cố ý


def lap_lo(chi=None):
    """mọi lỗ TRẮNG (giấy concept lọt vào: min RGB > 232) hay TRONG SUỐT bị kẹp KÍN bên trong một mảnh (không nối ra mép ảnh), nhỏ hơn
    3000 px: tô bằng màu trung vị của các điểm KHÔNG phải mực trong vành 3–14 px quanh lỗ (màu da / lòng xoắn), độ đậm 255."""
    DATJ = nap_dat()
    for ten in DATJ:
        if ten.endswith("_goc") or ten.endswith("_m5") or ten in KHONG_LAP or (chi and ten not in chi):
            continue
        pth = os.path.join(MANH, ten + ".png")
        if not os.path.exists(pth):
            continue
        A = np.asarray(Image.open(pth).convert("RGBA")).copy()
        rgb = A[..., :3].astype(np.int32)
        dac = A[..., 3] > 128
        ok = dac & ~(rgb.min(2) > 232)
        n, lab, st, cen = cv2.connectedComponentsWithStats((~ok).astype(np.uint8), 4)
        hh, ww = ok.shape
        sua = 0
        for k in range(1, n):
            x, y, w, h, area = st[k]
            if x == 0 or y == 0 or x + w >= ww or y + h >= hh or area >= 3000:
                continue                                   # nền ngoài mảnh hoặc vùng to (không phải lỗ lọt)
            lo = lab == k
            vanh = cv2.dilate(lo.astype(np.uint8), el(14)).astype(bool) & ~cv2.dilate(lo.astype(np.uint8), el(3)).astype(bool)
            mau = vanh & ok & (rgb.mean(2) > 110)
            if mau.sum() < 5:
                mau = vanh & ok
            if mau.sum() < 5:
                continue
            c = np.median(rgb[mau], axis=0).astype(np.uint8)
            A[lo, :3] = c
            A[lo, 3] = 255
            sua += 1
            print(f"  {ten}: lấp lỗ {area} px ở ({cen[k][0] + DATJ[ten]['hop'][0]:.0f}, {cen[k][1] + DATJ[ten]['hop'][1]:.0f}) màu {tuple(int(v) for v in c)}")
        if sua:
            Image.fromarray(A, "RGBA").save(pth)


THU_TU = ["jiao_r", "shou_r", "jiao_l", "shou_l", "mai", "vay", "tou", "yankuang", "weiba_1", "vay_truoc", "tinh_the", "phach_t", "phach_p",
          "yezi_1"]


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
    elif cmd == "sua_lop":
        sua_lop()
    elif cmd == "lap_lo":
        lap_lo(sys.argv[2:] or None)
    elif cmd == "hoc":
        hoc_pha_le()
    else:
        print(__doc__)
